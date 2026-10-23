#!/usr/bin/env python3
"""小红书文案校验器 validate_copy.py (v1.0)

阈值与词库全部读取 config/constants.md（单一数据源），不在脚本里写死。

用法:
  python3 scripts/validate_copy.py <小红书文案.md>          单文件；有 BLOCKER 时退出码 1
  python3 scripts/validate_copy.py --all [--report 文件]   批量扫描文案库（文案存储根目录/char_*/小红书文案.md）
  python3 scripts/validate_copy.py --count "标题" ...      计算标题字符数（Emoji=1 与保守口径）
  python3 scripts/validate_copy.py --self-test             校验器自测
  追加 --json 输出机器可读结果
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config" / "constants.md"
LEVEL_ORDER = {"BLOCKER": 0, "MAJOR": 1, "MINOR": 2}

PUBLISHABLE = {"titles", "body", "decl", "tags", "pinned"}
SCRIPT_KINDS = {"replies", "negative", "dm"}
SCOPES = {
    "body": {"titles", "body"},
    "body+pinned": {"titles", "body", "pinned"},
    "partA": {"titles", "body", "decl", "tags", "cover_text"},
    "public": {"titles", "body", "decl", "tags", "cover_text", "pinned", "replies", "negative"},
    "user": {"titles", "body", "decl", "tags", "cover_text", "pinned", "replies", "negative", "dm"},
    "doc": None,
}
NEGATION = re.compile(r"禁止|严禁|不要|不得|避免|慎用|❌|不出现|不留|不报|切勿|请勿|不给|不推销|不用|不能|不写|不做|不接|不引导")
ANSWER_SPLIT = re.compile(r"答[：:]|回复[：:]|→")
STOP_BIGRAMS = {"一个", "这个", "那个", "我们", "你们", "他们", "她们", "什么", "是不", "不是", "还是", "就是", "也是", "时候", "的时"}


# ---------------------------------------------------------------- config
def load_config(path: Path = CONFIG_PATH) -> dict:
    text = path.read_text(encoding="utf-8")

    def val(key: str, default=None, cast=str):
        m = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*(?:#.*)?$", text, re.M)
        if not m:
            return default
        raw = m.group(1).strip().strip('"').strip("'")
        try:
            return cast(raw)
        except ValueError:
            return default

    m = re.search(r"##\s*🧪\s*校验词库.*?```json\s*(.*?)```", text, re.S)
    if not m:
        raise SystemExit(f"❌ 未在 {path} 找到「🧪 校验词库」JSON 块")
    lex = json.loads(m.group(1))
    return {
        "body_min": val("最小字数", 180, int),
        "body_max": val("最大字数", 220, int),
        "title_hard": val("平台最大字符长度", 20, int),
        "title_min": val("实际发布最小字数", 14, int),
        "title_max": val("实际发布最大字数", 19, int),
        "emoji_weight": val("Emoji计数口径", 2, int),
        "title_emoji_max": val("标题Emoji上限", 1, int),
        "title_count": val("标题备选数量", 8, int),
        "title_types_min": val("最少公式类型数", 5, int),
        "cover_min": val("封面大字最少字数", 6, int),
        "cover_max": val("封面大字最大字数", 10, int),
        "tags_min": val("话题标签最少数量", 8, int),
        "tags_max": val("话题标签最多数量", 12, int),
        "para_emoji_max": val("正文每段Emoji上限", 2, int),
        "copy_root": val("文案存储根目录", ""),
        "copy_name": val("文案文件名", "小红书文案.md"),
        "lex": lex,
    }


# ---------------------------------------------------------------- text utils
def is_emoji(ch: str) -> bool:
    cp = ord(ch)
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF or 0x2B00 <= cp <= 0x2BFF
            or 0x2300 <= cp <= 0x23FF or cp in (0x3030, 0x303D, 0x3297, 0x3299))


def xhs_len(s: str, emoji_weight: int = 2) -> tuple[int, int]:
    """返回 (Emoji 记 1 的字符数, Emoji 按 emoji_weight 记的保守字符数)。"""
    plain = cons = 0
    after_zwj = False
    for ch in s:
        cp = ord(ch)
        if cp == 0x200D:
            after_zwj = True
            continue
        if cp in (0xFE0F, 0xFE0E) or 0x1F3FB <= cp <= 0x1F3FF or 0xE0020 <= cp <= 0xE007F:
            continue
        if is_emoji(ch):
            if after_zwj:
                after_zwj = False
                continue
            plain += 1
            cons += emoji_weight
        else:
            plain += 1
            cons += 1
        after_zwj = False
    return plain, cons


def count_body(s: str) -> int:
    s = re.sub(r"\*\*|__|`", "", s)
    return sum(1 for ch in s if not ch.isspace() and ord(ch) not in (0xFE0F, 0x200D))


def cjk_bigrams(s: str) -> set[str]:
    chars = [c for c in s if "\u4e00" <= c <= "\u9fff"]
    return {chars[i] + chars[i + 1] for i in range(len(chars) - 1)} - STOP_BIGRAMS


def excerpt(s: str, n: int = 40) -> str:
    s = s.strip()
    return s if len(s) <= n else s[:n] + "…"


# ---------------------------------------------------------------- parsing
def classify(heading: str) -> str:
    h = heading
    rules = [
        ("正文末行", "decl"), ("置顶", "pinned"), ("回复库", "replies"), ("负面", "negative"),
        ("敏感评论", "negative"), ("私信", "dm"), ("发布计划", "plan"), ("复盘", "review"),
        ("发布设置", "publish_settings"), ("打标", "publish_settings"), ("封面", "cover"),
        ("图序", "cover"), ("话题", "tags"), ("标签", "tags"), ("标题", "titles"), ("正文", "body"),
    ]
    for key, kind in rules:
        if key in h:
            return kind
    return "other"


@dataclass
class Doc:
    path: str
    lines: list[tuple[str, str]] = field(default_factory=list)  # (kind, line)
    pov: str = ""

    def text_of(self, kinds: set[str] | None) -> list[tuple[str, str]]:
        return [(k, l) for k, l in self.lines if kinds is None or k in kinds]


def parse(text: str, path: str = "<memory>") -> Doc:
    doc = Doc(path=path)
    kind = "meta"
    in_code = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m and not in_code:
            level, title = len(m.group(1)), m.group(2)
            if level == 1:
                kind = "meta"
            elif re.search(r"Part\s*[AB]", title, re.I) and classify(title) == "other":
                kind = "other"
            else:
                kind = classify(title)
            doc.lines.append(("heading:" + kind, title))
            continue
        doc.lines.append((kind, line))
    m = re.search(r"叙事视角[^A-Za-z\n]{0,12}([A-D])([12]?)", text)
    if m:
        doc.pov = m.group(1) + (m.group(2) or ("2" if m.group(1) == "A" else ""))
    return doc


def extract_titles(doc: Doc) -> list[dict]:
    titles = []
    for kind, line in doc.lines:
        if kind != "titles":
            continue
        m = re.match(r"^\s*(?:\d+[\.、]|[-*])\s+(.*)$", line)
        if not m:
            continue
        rest = m.group(1)
        star = "⭐" in rest
        tm = re.search(r"`?\[([^\]]+)\]`?", rest)
        ttype = tm.group(1) if tm else ""
        body = rest[tm.end():] if tm else rest
        body = body.replace("⭐", "")
        cut = re.search(r"\s*[\(（]\s*\d+\s*字|【", body)
        text = (body[:cut.start()] if cut else body).strip().strip("`*").strip()
        claimed = re.search(r"[\(（]\s*(\d+)\s*字", rest)
        titles.append({
            "text": text, "type": ttype, "star": star,
            "claimed": int(claimed.group(1)) if claimed else None,
            "has_source": "【" in rest and "提取" in rest,
        })
    return titles


def extract_body(doc: Doc) -> list[str]:
    paras = []
    for kind, line in doc.lines:
        if kind != "body":
            continue
        s = line.strip()
        if not s or s.startswith("|") or re.fullmatch(r"-{3,}|\*{3,}", s):
            continue
        s = re.sub(r"^>\s?", "", s).strip()
        if not s or re.match(r"^(自检|⚠️|核心铁律|\[第?\d)", s):
            continue
        paras.append(s)
    return paras


def extract_tags(doc: Doc) -> list[str]:
    tags = []
    for kind, line in doc.lines:
        if kind == "tags":
            for t in re.findall(r"#([^\s#，,。]+)", line):
                t = t.strip("*`")
                if t and t not in tags:
                    tags.append(t)
    return tags


def extract_cover_text(doc: Doc) -> str | None:
    for kind, line in doc.lines:
        if kind == "cover" and "封面大字" in line:
            m = re.search(r"封面大字[^：:]*[：:]\s*(.+)$", line)
            if m:
                t = re.sub(r"[（(]\s*\d+\s*字\s*[)）]", "", m.group(1))
                return t.strip().strip("*`“”\"' ").strip()
    return None


# ---------------------------------------------------------------- checks
@dataclass
class Issue:
    level: str
    code: str
    msg: str

    def as_dict(self):
        return {"level": self.level, "code": self.code, "msg": self.msg}


def scan_lines(doc: Doc, scope: str, cover_text: str | None):
    kinds = SCOPES[scope]
    for kind, line in doc.lines:
        if kind.startswith("heading:"):
            base = kind.split(":", 1)[1]
            if kinds is None or base in kinds:
                yield base, line
            continue
        if kinds is not None and kind not in kinds:
            continue
        s = line.strip()
        if not s:
            continue
        if kind not in PUBLISHABLE and NEGATION.search(s):
            continue
        if kind in SCRIPT_KINDS:
            if s.startswith("|"):
                cells = [c for c in s.strip("|").split("|") if c.strip()]
                s = cells[-1] if cells else ""
            else:
                parts = ANSWER_SPLIT.split(s)
                s = parts[-1] if len(parts) > 1 else s
        yield kind, s
    if cover_text and (kinds is None or "cover_text" in kinds):
        yield "cover_text", cover_text


def check(doc: Doc, cfg: dict) -> tuple[list[Issue], dict]:
    issues: list[Issue] = []
    add = lambda lv, code, msg: issues.append(Issue(lv, code, msg))
    lex = cfg["lex"]
    full = "\n".join(l for _, l in doc.lines)

    titles = extract_titles(doc)
    paras = extract_body(doc)
    body = "\n".join(paras)
    tags = extract_tags(doc)
    cover = extract_cover_text(doc)
    body_len = count_body(body)

    # ---- 合规
    if not any(p in full for p in lex["ai_label_patterns"]):
        add("BLOCKER", "AI_LABEL", "缺少「添加 AI 生成内容标识」发布设置提示（《标识办法》第十条法定义务）")
    if not doc.pov:
        add("MAJOR", "POV_MISSING", "元数据未声明叙事视角（A1/A2/B/C/D）；素材库人物默认只能用 A2/B")
    if doc.pov in ("A2", "B", "") and not any(p in full for p in lex["effect_image_patterns"]):
        add("MAJOR", "EFFECT_DECL", "缺少效果图声明：正文末行需注明'图为 3D 手办设计效果图（AI 生成）'")
    if doc.pov == "C" and not any(p in full for p in lex["authorization_patterns"]):
        add("MAJOR", "C_AUTH", "视角 C 需标注'经客户授权分享'")

    # ---- 标题
    if not titles:
        add("BLOCKER", "TITLE_MISSING", "未找到标题备选")
    else:
        if len(titles) != cfg["title_count"]:
            add("MAJOR", "TITLE_COUNT", f"标题 {len(titles)} 条，应为 {cfg['title_count']} 条")
        types = {t["type"].replace("型", "").split("·")[0] for t in titles if t["type"]}
        if len(types) < cfg["title_types_min"]:
            add("MAJOR", "TITLE_TYPES", f"标题公式仅 {len(types)} 种，至少 {cfg['title_types_min']} 种")
        if not any(t["star"] for t in titles):
            add("MINOR", "TITLE_STAR", "未用 ⭐ 标注首推标题")
        body_bi = cjk_bigrams(body)
        for i, t in enumerate(titles, 1):
            plain, cons = xhs_len(t["text"], cfg["emoji_weight"])
            tag = f"标题{i}「{t['text']}」"
            if cons > cfg["title_hard"]:
                add("BLOCKER", "TITLE_LEN", f"{tag} 超过平台上限 {cfg['title_hard']}（按字符 {plain}，保守 {cons}）")
            elif cons < cfg["title_min"] or cons > cfg["title_max"]:
                add("MINOR", "TITLE_RANGE", f"{tag} 不在推荐区间 {cfg['title_min']}–{cfg['title_max']}（保守 {cons}）")
            n_emoji = sum(1 for ch in t["text"] if is_emoji(ch))
            if n_emoji > cfg["title_emoji_max"]:
                add("MAJOR", "TITLE_EMOJI", f"{tag} 含 {n_emoji} 个 Emoji，上限 {cfg['title_emoji_max']}")
            if not t["has_source"]:
                add("MAJOR", "TITLE_SOURCE", f"{tag} 缺少【提取自正文：……】出处")
            if body and len(cjk_bigrams(t["text"]) & body_bi) < 2:
                add("MAJOR", "TITLE_ALIGN", f"{tag} 与正文重合度过低，疑似文题脱节")
            if t["claimed"] is not None and t["claimed"] not in (plain, cons):
                add("MINOR", "TITLE_CLAIMED", f"{tag} 标注 {t['claimed']} 字，实际 {plain}（保守 {cons}）")
            if "独白对话" in t["type"] and doc.pov not in ("C", "D"):
                add("MAJOR", "TITLE_TYPE_POV", f"{tag} 独白对话型只允许用于 C/D 真实故事")
            if "手艺人手记" in t["type"] and not doc.pov.startswith("A"):
                add("MAJOR", "TITLE_TYPE_POV", f"{tag} 手艺人手记型只允许用于 A 视角")

    # ---- 正文
    if not paras:
        add("BLOCKER", "BODY_MISSING", "未找到正文")
    else:
        if not cfg["body_min"] <= body_len <= cfg["body_max"]:
            add("MAJOR", "BODY_LEN", f"正文 {body_len} 字，要求 {cfg['body_min']}–{cfg['body_max']}")
        for p in paras:
            n = sum(1 for ch in p if is_emoji(ch))
            if n > cfg["para_emoji_max"]:
                add("MINOR", "BODY_EMOJI", f"段落 Emoji {n} 个超过 {cfg['para_emoji_max']}：{excerpt(p)}")
        hits = [m for m in lex["time_jump_markers"] if m in body]
        if len(hits) >= lex["time_jump_threshold"]:
            add("MAJOR", "TIME_JUMP", f"疑似多时空拼接（{'/'.join(hits)}），应一文一事")

    # ---- 话题 / 封面
    if not cfg["tags_min"] <= len(tags) <= cfg["tags_max"]:
        add("MAJOR", "TAG_COUNT", f"话题标签 {len(tags)} 个，要求 {cfg['tags_min']}–{cfg['tags_max']}")
    if cover is None:
        add("MAJOR", "COVER_TEXT", "缺少「封面大字」")
    else:
        n = xhs_len(cover, 1)[0]
        if not cfg["cover_min"] <= n <= cfg["cover_max"]:
            add("MAJOR", "COVER_TEXT", f"封面大字「{cover}」{n} 字，要求 {cfg['cover_min']}–{cfg['cover_max']}")

    # ---- 词库
    for cat in lex["categories"]:
        if "pov" in cat and doc.pov not in cat["pov"]:
            continue
        found: list[str] = []
        regs = [re.compile(r) for r in cat.get("regex", [])]
        for kind, s in scan_lines(doc, cat["scope"], cover):
            low = s.lower()
            for term in cat.get("terms", []):
                if term.lower() in low:
                    found.append(f"「{term}」@{kind}：{excerpt(s)}")
            for r in regs:
                m = r.search(s)
                if m:
                    found.append(f"「{m.group(0)}」@{kind}：{excerpt(s)}")
        for f in list(dict.fromkeys(found))[:3]:
            add(cat["level"], f"LEX:{cat['name']}", f)
        if len(found) > 3:
            add(cat["level"], f"LEX:{cat['name']}", f"……另有 {len(found) - 3} 处")

    issues.sort(key=lambda x: LEVEL_ORDER[x.level])
    stats = {"pov": doc.pov or "未声明", "body_len": body_len, "titles": len(titles),
             "tags": len(tags), "cover": cover}
    return issues, stats


def verdict(issues: list[Issue]) -> str:
    lv = {i.level for i in issues}
    if "BLOCKER" in lv:
        return "❌ 禁止发布（存在 BLOCKER）"
    if "MAJOR" in lv:
        return "⚠️ 需修改后发布（存在 MAJOR）"
    return "✅ 可发布"


def render(path: str, issues: list[Issue], stats: dict) -> str:
    out = [f"📄 {path}",
           f"   视角 {stats['pov']} | 正文 {stats['body_len']} 字 | 标题 {stats['titles']} 条 | "
           f"话题 {stats['tags']} 个 | 封面大字 {stats['cover'] or '—'}"]
    icons = {"BLOCKER": "❌", "MAJOR": "⚠️", "MINOR": "ℹ️"}
    for lv in LEVEL_ORDER:
        group = [i for i in issues if i.level == lv]
        if group:
            out.append(f"   {icons[lv]} {lv} ({len(group)})")
            out += [f"      [{i.code}] {i.msg}" for i in group]
    out.append(f"   结论：{verdict(issues)}")
    return "\n".join(out)


# ---------------------------------------------------------------- batch
def batch(cfg: dict, report: str | None, as_json: bool) -> int:
    root = Path(cfg["copy_root"]).expanduser()
    files = sorted(root.glob(f"char_*/{cfg['copy_name']}"))
    if not files:
        print(f"未找到文案：{root}/char_*/{cfg['copy_name']}")
        return 1
    rows, codes = [], Counter()
    for f in files:
        issues, stats = check(parse(f.read_text(encoding="utf-8"), str(f)), cfg)
        c = Counter(i.level for i in issues)
        codes.update(f"{i.level} {i.code}" for i in issues)
        rows.append({"char": f.parent.name, "pov": stats["pov"], "BLOCKER": c["BLOCKER"],
                     "MAJOR": c["MAJOR"], "MINOR": c["MINOR"],
                     "top": sorted({i.code for i in issues if i.level == "BLOCKER"})[:4]})
    total = len(rows)
    ok = sum(1 for r in rows if r["BLOCKER"] == 0 and r["MAJOR"] == 0)
    fix = sum(1 for r in rows if r["BLOCKER"] == 0 and r["MAJOR"] > 0)
    block = total - ok - fix
    if as_json:
        print(json.dumps({"total": total, "publishable": ok, "needs_fix": fix, "blocked": block,
                          "codes": codes.most_common(), "files": rows}, ensure_ascii=False, indent=2))
    lines = [
        "# 小红书文案库校验报告", "",
        f"> 生成时间：{datetime.now():%Y-%m-%d %H:%M} · 校验器：scripts/validate_copy.py · 规则源：config/constants.md", "",
        "| 总数 | ✅ 可发布 | ⚠️ 需修改 | ❌ 禁止发布 |", "| --- | --- | --- | --- |",
        f"| {total} | {ok} | {fix} | {block} |", "",
        "## 问题分布", "", "| 级别 · 规则 | 命中篇数 |", "| --- | --- |",
    ]
    per_file_codes = Counter()
    for f in files:
        issues, _ = check(parse(f.read_text(encoding="utf-8"), str(f)), cfg)
        per_file_codes.update({f"{i.level} {i.code}" for i in issues})
    lines += [f"| {k} | {v} |" for k, v in per_file_codes.most_common()]
    lines += ["", "## 逐篇结果", "", "| 人物 | 视角 | BLOCKER | MAJOR | MINOR | 主要阻断项 |", "| --- | --- | --- | --- | --- | --- |"]
    lines += [f"| {r['char']} | {r['pov']} | {r['BLOCKER']} | {r['MAJOR']} | {r['MINOR']} | {', '.join(r['top'])} |" for r in rows]
    md = "\n".join(lines) + "\n"
    if report:
        Path(report).expanduser().write_text(md, encoding="utf-8")
        if not as_json:
            print(f"报告已写入：{report}")
    if not as_json:
        print(f"共 {total} 篇：✅ 可发布 {ok} · ⚠️ 需修改 {fix} · ❌ 禁止发布 {block}")
        for k, v in per_file_codes.most_common(12):
            print(f"   {v:>3} 篇  {k}")
    return 0


# ---------------------------------------------------------------- self-test
GOOD = """# 小红书发布包：char_45_BW_国营粮站过秤窗口的售粮婆婆

> **资产编号**：char_45_BW
> **叙事视角**：B 第二人称代入
> **笔记类型**：情感共鸣型

## Part A · 发布内容

### 🏷️ 标题备选
1. ⭐ `[场景代入型]` 粮站窗口后面那杆秤，你还记得吗 (15字) 【提取自正文：你还记得粮站窗口后面那杆秤吗】
2. `[情绪反差型]` 一两都不肯差的她，偷偷挪了秤砣 (15字) 【提取自正文：一两都不肯差】
3. `[悬念留白型]` 碰上抱孩子买粮的，她会把秤砣… (15字) 【提取自正文：碰上抱着孩子来买粮的】
4. `[数字锚点型]` 六厘米的售粮员，秤星一颗颗都留着 (16字) 【提取自正文：秤星一颗颗都留着】
5. `[反问共鸣型]` 你家也有一位这样的粮站阿姨吗 (14字) 【提取自正文：你家也有这样一位吗】
6. `[时空对比型]` 那会儿看不懂的一点点，长大才明白 (16字) 【提取自正文：那会儿看不懂，长大才明白】
7. `[身份标签型]` 排队买过粮的人，都懂这一点点 (14字) 【提取自正文：那一点点】
8. `[情绪反差型]` 看不懂的那一点点，是她给的体面 (15字) 【提取自正文：全部体面】

### 📝 正文
你还记得粮站窗口后面那杆秤吗？

铁栅窗一拉开，秤砣挂上铜勾，窗口里的阿姨眯着眼盯住秤杆，一两都不肯差。可碰上抱着孩子来买粮的，她会把秤砣悄悄往外挪一点点。

那会儿看不懂，长大才明白，那一点点是她能给的全部体面。

我们照这样一位售粮员，设计了一尊六厘米的小人：深蓝罩衫，黑袖套，胸前一枚搪瓷牌，手里那杆秤，秤星一颗颗都留着。

你家也有这样一位吗？更想留住她盯秤杆的眼神，还是挪秤砣的那一下？

### 📌 正文末行声明
图为 3D 手办设计效果图（AI 生成），实物以打样确认为准。

### #️⃣ 话题标签
#纪念手办 #3D打印手办 #老照片做手办 #怀念长辈 #粮站 #老物件 #定制手办 #长辈礼物 #老照片能做手办吗 #家的味道

### 🖼️ 封面与图序
- 封面大字：挪秤砣的那一下

### 🛡️ 发布设置
- 勾选「添加 AI 生成内容标识」

## Part B · 运营执行卡（不发布）

### 💬 置顶评论
> 写这篇的时候一直在想粮站那扇铁栅窗。你记忆里的长辈，最常做的一个动作是什么？

### 🗂️ 评论回复库
| 用户在问 | 回复要点 |
| --- | --- |
| 多少钱 | 私信按你的需求细说（公开评论不报数字） |
| 怎么联系你 | 直接私信就好 |

### ✉️ 私信承接 SOP
1. 共情：抱歉让你想起这些。想为谁做？
"""

BAD = """## 🏷️ 爆款备选标题
1. ⭐ `[独白对话型]` 婆婆，今年我用你那杆秤称了米，好想你呀😭😭 (22字)

## 📝 完整小红书正文文案
今天我把墙上那杆铜勾杆秤摘下来。小时候她抱我去粮站，后来我去上学，如今她走了。我奶奶说这秤最准。成品实拍和她一模一样。

## 💬 评论区控评与引流布局策略
### 2. 小号互动脚本
- 共情买家号 B：上个月刚收到手办，实拍太像了！
### 3. 私信转化 SOP
- 加我微信 abc123 详聊，Blender 建模。
"""


def self_test(cfg: dict) -> int:
    ok = True
    g_issues, g_stats = check(parse(GOOD), cfg)
    bad_levels = [i for i in g_issues if i.level in ("BLOCKER", "MAJOR")]
    print(render("<GOOD 样例>", g_issues, g_stats))
    if bad_levels:
        ok = False
        print("❌ GOOD 样例不应有 BLOCKER/MAJOR")
    b_issues, b_stats = check(parse(BAD), cfg)
    print(render("<BAD 样例>", b_issues, b_stats))
    got = {i.code for i in b_issues if i.level == "BLOCKER"}
    expect = {"AI_LABEL", "TITLE_LEN", "LEX:伪造亲属经历", "LEX:虚假互动", "LEX:导流联系方式",
              "LEX:软件与工具名", "LEX:绝对化与虚假承诺", "LEX:效果图冒充实拍"}
    missing = expect - got
    if missing:
        ok = False
        print(f"❌ BAD 样例漏检：{sorted(missing)}")
    if "TIME_JUMP" not in {i.code for i in b_issues}:
        ok = False
        print("❌ BAD 样例漏检 TIME_JUMP")
    assert xhs_len("你好😭", 2) == (3, 4) and xhs_len("👨‍👩‍👧", 2) == (1, 2)
    print("\nSELF-TEST:", "PASS ✅" if ok else "FAIL ❌")
    return 0 if ok else 1


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="小红书文案校验器（规则源：config/constants.md）")
    ap.add_argument("file", nargs="?", help="小红书文案.md 路径")
    ap.add_argument("--all", action="store_true", help="批量扫描文案库")
    ap.add_argument("--report", help="批量模式下输出 Markdown 报告路径")
    ap.add_argument("--count", nargs="+", metavar="TEXT", help="计算标题字符数")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cfg = load_config()

    if args.self_test:
        return self_test(cfg)
    if args.count:
        for t in args.count:
            plain, cons = xhs_len(t, cfg["emoji_weight"])
            flag = "✅" if cons <= cfg["title_hard"] else "❌ 超限"
            print(f"{t}\t字符 {plain}\t保守 {cons}\t{flag}")
        return 0
    if args.all:
        return batch(cfg, args.report, args.json)
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file).expanduser()
    if p.is_dir():
        p = p / cfg["copy_name"]
    issues, stats = check(parse(p.read_text(encoding="utf-8"), str(p)), cfg)
    if args.json:
        print(json.dumps({"file": str(p), "stats": stats, "verdict": verdict(issues),
                          "issues": [i.as_dict() for i in issues]}, ensure_ascii=False, indent=2))
    else:
        print(render(str(p), issues, stats))
    return 1 if any(i.level == "BLOCKER" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
