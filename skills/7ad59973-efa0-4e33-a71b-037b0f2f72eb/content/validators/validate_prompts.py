#!/usr/bin/env python3
"""fullcolor 提示词校验器 validate_prompts.py (v5.0)

直接解析 prompts.md（兼容 prompts.json），规则参数读取 config/paths.yml（单一数据源）。

用法:
  python3 validators/validate_prompts.py <prompts.md | prompts.json | 人物目录>   单个人物；有 BLOCKER 时退出码 1
  python3 validators/validate_prompts.py --all [--report [路径]]                  批量审计素材库（含跨人物场景相似度）
  python3 validators/validate_prompts.py <文件> --only ifts,framing               只看指定检查组
  python3 validators/validate_prompts.py <prompts.md> --export-json [输出路径]    从 prompts.md 导出 prompts.json
  python3 validators/validate_prompts.py --self-test                               校验器自测
  追加 --json 输出机器可读结果

检查组: completeness ifts framing syntax english leak sabotage ratio wordcount text funeral cover empty plaster profile
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
PATHS_YML = SKILL_ROOT / "config" / "paths.yml"
VIEWS = [f"{i:02d}" for i in range(11)]
LEVEL_ORDER = {"BLOCKER": 0, "MAJOR": 1, "MINOR": 2}
GROUP_OF = {
    "COMPLETENESS": "completeness", "IFTS_MISSING": "ifts", "IFTS_MISMATCH": "ifts", "IFTS_LENGTH": "ifts",
    "FRAMING": "framing", "SYNTAX": "syntax", "NO_ENGLISH": "english", "CODE_LEAK": "leak",
    "SELF_SABOTAGE": "sabotage", "RATIO_MJ": "ratio", "RATIO_GEMINI": "ratio", "WORD_COUNT": "wordcount",
    "TEXT_RENDER": "text", "FUNERAL": "funeral", "CANDLE": "funeral", "COVER_SPACE": "cover",
    "EMPTY_WORDS": "empty", "PLASTER_POSITIVE": "plaster", "PROFILE_MISSING": "profile",
    "SCENE_SIMILAR": "similarity",
}
STOPWORDS = set("""a an the of and with on in at to for from by as into onto over under near beside next right left
her his their its our your she he they it is are was be being been that this these those which who while whose
6cm 12cm 6.0cm 12.0cm miniature figurine figure bust resin printed full color full-color photopolymer painted
tiny small old vintage warm soft gentle deeply poignant emotionally resonant documentary photograph photo shot
canon eos r5 rf lens kodak portra film grain tones analog authentic depth field shallow chinese""".split())


# ---------------------------------------------------------------- config
def _expand(v: str) -> str:
    v = re.sub(r"\$\{(\w+):-([^}]*)\}", lambda m: os.environ.get(m.group(1), m.group(2)), v)
    v = re.sub(r"\$\{(\w+)\}", lambda m: os.environ.get(m.group(1), ""), v)
    return os.path.expanduser(v)


def _scalar(raw: str):
    raw = raw.strip()
    if raw.startswith('"'):
        return _expand(raw[1:raw.find('"', 1)])
    if raw.startswith("["):
        return json.loads(raw[:raw.find("]") + 1])
    raw = raw.split(" #")[0].strip()
    if raw in ("true", "false"):
        return raw == "true"
    for cast in (int, float):
        try:
            return cast(raw)
        except ValueError:
            pass
    return _expand(raw)


def load_yaml(path: Path = PATHS_YML) -> dict:
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, rest = line.strip().partition(":")
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if not rest.strip() or rest.strip().startswith("#"):
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            parent[key] = _scalar(rest)
    return root


def cfg_get(cfg: dict, dotted: str, default=None):
    cur = cfg
    for k in dotted.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


# ---------------------------------------------------------------- model & parsing
@dataclass
class Character:
    name: str
    source: str
    posture: str = ""
    ifts: str | None = None
    ifts_source: str = ""
    views: dict[str, str] = field(default_factory=dict)
    has_profile: bool = True


VIEW_HEAD = re.compile(r"^#{2,4}\s*视角\s*(\d{2})")


def parse_prompts_md(text: str) -> tuple[dict[str, str], str | None]:
    views: dict[str, str] = {}
    ifts = None
    cur = None
    want_ifts = False
    in_code = False
    owner = None
    buf: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            if not in_code:
                in_code, buf = True, []
                owner = "IFTS" if want_ifts else (cur if cur and cur not in views else None)
            else:
                in_code = False
                content = " ".join(b.strip() for b in buf if b.strip())
                if owner == "IFTS" and content:
                    ifts, want_ifts = content, False
                elif owner and content:
                    views[owner] = content
                owner = None
            continue
        if in_code:
            buf.append(line)
            continue
        m = VIEW_HEAD.match(s)
        if m:
            cur = m.group(1)
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            title = h.group(2)
            if ifts is None and ("唯一性指纹" in title or "指纹 Token" in title) and "对齐" not in title:
                want_ifts = True
            if len(h.group(1)) <= 2:
                cur = None
    return views, ifts


def ifts_from_profile(profile: Path) -> str | None:
    if not profile.is_file():
        return None
    text = profile.read_text(encoding="utf-8")
    m = re.search(r"唯一性指纹[\s\S]{0,300}?`([^`\n]*year-old[^`\n]*)`", text)
    return m.group(1).strip() if m else None


def posture_of(name: str, views: dict[str, str]) -> str:
    m = re.search(r"char_\d+_([BF][MW])", name)
    if m:
        return m.group(1)
    p01 = views.get("01", "")
    if "full-body" in p01 or "full-figure" in p01 or "12.0cm" in p01:
        return "FM"
    return "BM" if p01 else ""


def load_character(target: Path) -> Character:
    target = target.expanduser()
    folder = target if target.is_dir() else target.parent
    if target.is_dir():
        target = folder / "prompts.md" if (folder / "prompts.md").exists() else folder / "prompts.json"
    name = folder.name
    if target.suffix == ".json":
        data = json.loads(target.read_text(encoding="utf-8"))
        src = data.get("views", data)
        views = {v: (src[v]["raw_prompt"] if isinstance(src.get(v), dict) else src[v]) for v in VIEWS if v in src}
        ifts, ifts_src = data.get("identity_fingerprint_tokens"), "prompts.json"
        posture = data.get("posture") or posture_of(name, views)
    else:
        views, ifts = parse_prompts_md(target.read_text(encoding="utf-8"))
        ifts_src = "prompts.md"
        posture = posture_of(name, views)
    profile = folder / "character_profile.md"
    if not ifts:
        ifts, ifts_src = ifts_from_profile(profile), "character_profile.md"
    if ifts:
        ifts = ifts.strip().rstrip(".。")
    return Character(name=name, source=str(target), posture=posture, ifts=ifts, ifts_source=ifts_src,
                     views=views, has_profile=profile.is_file())


# ---------------------------------------------------------------- checks
@dataclass
class Issue:
    level: str
    code: str
    msg: str

    def as_dict(self):
        return {"level": self.level, "code": self.code, "msg": self.msg}


def mj_parts(prompt: str) -> tuple[str, str]:
    pos = re.split(r"\s--[a-z]", prompt, maxsplit=1)[0]
    m = re.search(r"--no\s+(.*?)(?=\s--[a-z]|$)", prompt)
    return pos, (m.group(1) if m else "")


def words(s: str) -> list[str]:
    return [w for w in s.split() if re.search(r"[A-Za-z0-9]", w)]


def norm(s: str) -> str:
    s = re.sub(r",?\s*Keep the upper body\s*,?", ", ", s, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"\s*,\s*", ", ", s)).strip(" ,")


def check(ch: Character, cfg: dict) -> list[Issue]:
    issues: list[Issue] = []
    add = lambda lv, code, msg: issues.append(Issue(lv, code, msg))
    v = ch.views
    gem = [x for x in VIEWS[2:] if x in v]
    ratio_cue = cfg_get(cfg, "parameters.gemini_views.ratio_cue", "Vertical 3:4 composition")
    cover_cue = cfg_get(cfg, "parameters.gemini_views.cover_cue", "negative space")
    covers = cfg_get(cfg, "generation.cover_candidates", ["07", "10"])
    wc = cfg_get(cfg, "parameters.word_count", {})

    # 完整性
    missing = [x for x in VIEWS if not v.get(x)]
    if missing:
        add("BLOCKER", "COMPLETENESS", f"缺少视角 {', '.join(missing)}（11 视角必须全量交付）")
    for x, p in v.items():
        if re.search(r"TODO|以此类推|此处省略|\.\.\.|…", p):
            add("BLOCKER", "COMPLETENESS", f"视角 {x} 含占位符/省略号")
    if not ch.has_profile:
        add("MAJOR", "PROFILE_MISSING", "人物目录缺少 character_profile.md")

    # IFTS
    if not ch.ifts:
        add("BLOCKER", "IFTS_MISSING", "未找到 IFTS（prompts.md 第 0 节或 character_profile.md）")
    else:
        n = len(words(ch.ifts))
        lo, hi = cfg_get(cfg, "parameters.ifts_words_min", 15), cfg_get(cfg, "parameters.ifts_words_max", 20)
        if not lo <= n <= hi:
            add("MINOR", "IFTS_LENGTH", f"IFTS {n} 词，建议 {lo}–{hi}")
        for x in ("00", "01"):
            if v.get(x) and norm(ch.ifts) not in norm(v[x]):
                add("BLOCKER", "IFTS_MISMATCH", f"视角 {x} 未逐字包含 IFTS（来源：{ch.ifts_source}）")

    # 景别
    if ch.posture in ("FW", "FM"):
        c00, c01 = v.get("00", "").count("full-body"), v.get("01", "").count("full-body")
        if c00 < 1 or c01 < 2:
            add("BLOCKER", "FRAMING", f"全身像需 full-body：00 ≥1 次（现 {c00}）、01 ≥2 次（现 {c01}）")
    elif ch.posture in ("BW", "BM"):
        lack = [x for x in ("00", "01") if "keep the upper body" not in v.get(x, "").lower()]
        if lack:
            add("BLOCKER", "FRAMING", f"胸像需 'Keep the upper body'：视角 {', '.join(lack)} 缺失")

    # Midjourney 00/01
    forbidden = cfg_get(cfg, "parameters.view_01.negative_forbidden", [])
    for x in ("00", "01"):
        p = v.get(x)
        if not p:
            continue
        if "--ar" not in p or not re.search(r"--v\s*\d", p):
            add("BLOCKER", "SYNTAX", f"视角 {x}（Midjourney）缺少 --ar 或 --v 参数")
        if "--ar 1:1" not in p:
            add("MAJOR", "RATIO_MJ", f"视角 {x} 应为 --ar 1:1")
        pos, neg = mj_parts(p)
        if not re.search(r"\bEnglish\b", neg):
            add("BLOCKER", "NO_ENGLISH", f"视角 {x} 的 --no 负向缺少 English")
        if x == "01":
            bad = [t for t in forbidden if re.search(rf"\b{re.escape(t)}\b", neg, re.I)]
            if bad:
                add("BLOCKER", "SELF_SABOTAGE", f"视角 01 负向含 {bad}，会迫使模型生成真人")
            if re.search(r"\bplaster\b|stone pedestal|marble column|neoclassical", pos, re.I):
                add("MAJOR", "PLASTER_POSITIVE", "视角 01 正向出现石膏/石柱类底座词")
        if re.search(r"masterpiece|\b8k\b|hyperrealistic|ultra detailed|smooth skin|best quality", pos, re.I):
            add("MAJOR", "EMPTY_WORDS", f"视角 {x} 正向含空洞词（masterpiece/8k/hyperrealistic 等）")
        np_, nn = len(words(pos)), len(words(neg))
        tot = np_ + nn
        if not (wc.get("total_min", 50) <= tot <= wc.get("total_max", 82)) or np_ > wc.get("positive_max", 65):
            add("MAJOR", "WORD_COUNT", f"视角 {x} 词数 {tot}（正向 {np_} + 负向 {nn}），预算 总 {wc.get('total_min', 50)}–{wc.get('total_max', 82)}、正向 ≤{wc.get('positive_max', 65)}")

    # Gemini 02–10
    no_ratio, no_cover = [], []
    for x in gem:
        p = v[x]
        if re.search(r"(?<![\w-])--[a-z]", p):
            add("BLOCKER", "SYNTAX", f"视角 {x}（Gemini）含 Midjourney CLI 参数")
        if "Avoid:" not in p:
            add("BLOCKER", "SYNTAX", f"视角 {x}（Gemini）缺少 'Avoid:' 负向句")
        elif "English text" not in p.split("Avoid:", 1)[1]:
            add("BLOCKER", "NO_ENGLISH", f"视角 {x} 的 Avoid 缺少 'English text, letters'")
        if "3:4" not in p:
            no_ratio.append(x)
        if x in covers and cover_cue.lower() not in p.lower():
            no_cover.append(x)
        if re.search(r"(reading|that says|which says|that reads|inscribed with|lettering)\s*['\"“‘]", p, re.I):
            add("MAJOR", "TEXT_RENDER", f"视角 {x} 要求渲染可读文字（易出乱码/英文）")
        fun = {m.group(0).lower() for m in re.finditer(
            r"\b(?:shrine|altar|incense|joss|offerings|offering table|ancestral hall|funeral|mourning|tomb|grave|urn|ashes|wreath|memorial portrait)\b"
            r"|black[- ]and[- ]white (?:ID )?(?:photo|portrait) frame|ID photo frame", p, re.I)}
        if fun:
            add("MAJOR", "FUNERAL", f"视角 {x} 含灵堂/供桌意象：{sorted(fun)}")
        if re.search(r"\bcandles?\b", p, re.I):
            add("MINOR", "CANDLE", f"视角 {x} 含蜡烛，注意避免供桌感")
    if no_ratio:
        add("MAJOR", "RATIO_GEMINI", f"{len(no_ratio)}/{len(gem)} 张场景图未声明 3:4（v5 规则：开头写 '{ratio_cue}.'）")
    if no_cover:
        add("MINOR", "COVER_SPACE", f"封面候选视角 {', '.join(no_cover)} 未预留标题留白")

    # 代码泄露
    for x, p in v.items():
        m = re.search(r"char_\d+|\b(?:BW|BM|FW|FM)\b|/Users/|obsidian", p)
        if m:
            add("BLOCKER", "CODE_LEAK", f"视角 {x} 泄露内部代号「{m.group(0)}」")
    issues.sort(key=lambda i: LEVEL_ORDER[i.level])
    return issues


# ---------------------------------------------------------------- similarity (batch)
def content_tokens(prompt: str, ifts: str | None) -> set[str]:
    body = prompt.split("Avoid:", 1)[0]
    body = re.split(r"\bShot on\b", body, maxsplit=1)[0]
    toks = {t for t in re.findall(r"[a-z][a-z'-]{2,}", body.lower())} - STOPWORDS
    if ifts:
        toks -= set(re.findall(r"[a-z][a-z'-]{2,}", ifts.lower()))
    return toks


def scene_similarity(chars: list[Character], threshold: float) -> dict[str, list[tuple[float, str, str, str]]]:
    hits: dict[str, list] = defaultdict(list)
    for slot in VIEWS[2:]:
        docs = {c.name: content_tokens(c.views[slot], c.ifts) for c in chars if c.views.get(slot)}
        if len(docs) < 3:
            continue
        df = Counter(t for toks in docs.values() for t in toks)
        common = {t for t, n in df.items() if n / len(docs) > 0.5}
        docs = {k: s - common for k, s in docs.items()}
        for (a, sa), (b, sb) in combinations(docs.items(), 2):
            if sa and sb:
                j = len(sa & sb) / len(sa | sb)
                if j >= threshold:
                    hits[a].append((j, slot, b, a))
                    hits[b].append((j, slot, a, b))
    return hits


# ---------------------------------------------------------------- output
def verdict(issues: list[Issue]) -> str:
    lv = {i.level for i in issues}
    return "❌ 禁止交付（存在 BLOCKER）" if "BLOCKER" in lv else ("⚠️ 建议修正（存在 MAJOR）" if "MAJOR" in lv else "✅ 通过")


def render(ch: Character, issues: list[Issue]) -> str:
    out = [f"📄 {ch.name}", f"   姿态 {ch.posture or '未知'} | 视角 {len(ch.views)}/11 | IFTS 来源 {ch.ifts_source if ch.ifts else '—'}"]
    icons = {"BLOCKER": "❌", "MAJOR": "⚠️", "MINOR": "ℹ️"}
    for lv in LEVEL_ORDER:
        group = [i for i in issues if i.level == lv]
        if group:
            out.append(f"   {icons[lv]} {lv} ({len(group)})")
            out += [f"      [{i.code}] {i.msg}" for i in group]
    out.append(f"   结论：{verdict(issues)}")
    return "\n".join(out)


def export_json(ch: Character, cfg: dict, out: Path) -> None:
    data = {"character": ch.name, "posture": ch.posture, "identity_fingerprint_tokens": ch.ifts,
            "generated_by": "validators/validate_prompts.py --export-json"}
    for x in VIEWS:
        if x in ch.views:
            engine = "midjourney" if x in ("00", "01") else "gemini"
            ratio = cfg_get(cfg, f"parameters.view_{x}.aspect_ratio", "1:1") if engine == "midjourney" \
                else cfg_get(cfg, "parameters.gemini_views.aspect_ratio", "3:4")
            data[x] = {"raw_prompt": ch.views[x], "engine": engine, "aspect_ratio": ratio}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def batch(cfg: dict, report: str | None, as_json: bool, only: set[str] | None) -> int:
    base = Path(cfg_get(cfg, "paths.material_base", "")).expanduser()
    dirs = sorted(d for d in base.glob("char_*") if d.is_dir())
    chars, results = [], {}
    for d in dirs:
        if not ((d / "prompts.md").exists() or (d / "prompts.json").exists()):
            continue
        ch = load_character(d)
        chars.append(ch)
        results[ch.name] = [i for i in check(ch, cfg) if not only or GROUP_OF.get(i.code) in only]
    thr = float(cfg_get(cfg, "validation.scene_similarity_threshold", 0.5))
    sim = scene_similarity(chars, thr) if not only or "similarity" in only else {}
    for name, pairs in sim.items():
        for j, slot, other, _ in sorted(pairs, reverse=True)[:2]:
            results[name].append(Issue("MAJOR", "SCENE_SIMILAR", f"视角 {slot} 与 {other[:18]} 相似度 {j:.2f}（阈值 {thr}）"))
    total = len(chars)
    blocked = sum(1 for r in results.values() if any(i.level == "BLOCKER" for i in r))
    major = sum(1 for r in results.values() if not any(i.level == "BLOCKER" for i in r) and any(i.level == "MAJOR" for i in r))
    passed = total - blocked - major
    per_code = Counter()
    for r in results.values():
        per_code.update({f"{i.level} {i.code}" for i in r})
    if as_json:
        print(json.dumps({"total": total, "passed": passed, "major_only": major, "blocked": blocked,
                          "codes": per_code.most_common(),
                          "characters": {k: [i.as_dict() for i in v] for k, v in results.items()}},
                         ensure_ascii=False, indent=2))
    else:
        print(f"共 {total} 个人物：✅ 通过 {passed} · ⚠️ 仅 MAJOR {major} · ❌ 含 BLOCKER {blocked}")
        for k, n in per_code.most_common():
            print(f"   {n:>3} 个  {k}")
    if report is not None:
        out = Path(report).expanduser() if report else SKILL_ROOT / cfg_get(cfg, "paths.audit_report", "docs/latest-audit-report.md")
        lines = [
            "# Fullcolor 素材库质量审计报告", "",
            f"> 生成时间：{datetime.now():%Y-%m-%d %H:%M} · 校验器：`validators/validate_prompts.py`（直接解析 prompts.md）· 规则源：`config/paths.yml`",
            f"> 扫描目录：`{base}`", "",
            "| 人物数 | ✅ 通过 | ⚠️ 仅 MAJOR | ❌ 含 BLOCKER |", "| --- | --- | --- | --- |",
            f"| {total} | {passed} | {major} | {blocked} |", "",
            "## 问题分布（按人物计）", "", "| 级别 · 规则 | 人物数 |", "| --- | --- |",
        ]
        lines += [f"| {k} | {n} |" for k, n in per_code.most_common()]
        lines += ["", "## 规则说明", "",
                  "- **FRAMING**：v4.1 起胸像须含 `Keep the upper body`、全身像须含 `full-body`（00 ≥1、01 ≥2）；",
                  "- **NO_ENGLISH**：v4.1 起 00/01 的 `--no` 须含 `English`，02–10 的 `Avoid:` 须含 `English text, letters`；",
                  "- **RATIO_GEMINI**：v5 起 02–10 为 3:4 竖构图；存量 1:1 素材整组重出时再改；",
                  "- **WORD_COUNT**：v5 预算 总 50–82 词、正向 ≤65（按空白分词统计）；",
                  "- **SCENE_SIMILAR**：同一槽位跨人物内容词相似度超过阈值，属同质化嫌疑，需在机位/实景/道具/光影中至少改两层。",
                  "", "## 逐个人物", "", "| 人物 | 姿态 | BLOCKER | MAJOR | MINOR | 主要问题 |", "| --- | --- | --- | --- | --- | --- |"]
        for ch in chars:
            r = results[ch.name]
            c = Counter(i.level for i in r)
            top = ", ".join(sorted({i.code for i in r if i.level != "MINOR"}))
            lines.append(f"| {ch.name} | {ch.posture} | {c['BLOCKER']} | {c['MAJOR']} | {c['MINOR']} | {top} |")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if not as_json:
            print(f"报告已写入：{out}")
    return 0


# ---------------------------------------------------------------- self-test
def _sample(bad: bool = False) -> str:
    ifts = ("63-year-old Chinese mother-in-law, angular stern cheekbones, neat graying bob, precise watchful eyes, "
            "ink-stained fingers, old wooden steelyard with brass hook")
    p00 = (f"Candid documentary portrait of a real {ifts}, Keep the upper body, wearing navy cotton work smock with black "
           "oversleeves, soft indoor natural light, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw "
           "--s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands")
    p01 = (f"Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body, {ifts}, sculpted navy "
           "cotton work smock with black oversleeves, mounted on dark beveled pedestal base, subtle resin SSS finish, light gray "
           "cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, "
           "skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands")
    scenes = {
        "02": "resting on an old rattan armchair armrest beside her worn ration booklet, late afternoon side light",
        "03": "standing on the middle shelf of a glass-front family display cabinet beside her brass-hooked steelyard",
        "04": "on a worn grain station counter next to a wooden abacus and stamped ration booklets",
        "05": "on a tiled windowsill beside a potted asparagus fern, early morning light through a sheer curtain",
        "06": "on an entryway cabinet beside black cloth shoes and a folded note with faded, illegible writing",
        "07": "cradled in an adult's cupped hands, cropped below the neck, soft window daylight",
        "08": "on a kitchen counter corner beside an aluminum pot of rice porridge and an enamel bowl",
        "09": "on a wooden bedside table under a warm tungsten desk lamp beside reading glasses",
        "10": "beside an open 1970s photo album showing her younger self in a navy uniform",
    }
    avoid = ("Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, "
             "western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.")
    parts = ["# char_99_BW 自测人物", "", "## 0. 人物唯一性指纹 Token 序列 (IFTS)", "", "```text", ifts, "```", "",
             "## 一、 Midjourney", "", "### 视角 00: 基底定妆照", "```text", p00, "```", "",
             "### 视角 01: 模型标准像", "```text", p01, "```", "", "## 二、 Gemini", ""]
    for x, sc in scenes.items():
        cover = "Leave clean negative space in the upper third for a title overlay. " if x in ("07", "10") else ""
        prompt = (f"Vertical 3:4 composition. A warm documentary photograph of the 6cm 3D printed resin bust figurine of the "
                  f"grain station attendant {sc}. {cover}Shot on Canon EOS R5 with RF 50mm f/1.4 lens, Kodak Portra 400 tones. {avoid}")
        if bad and x == "03":
            prompt = prompt.replace("glass-front family display cabinet", "family shrine with incense") + " --ar 3:4"
        if bad and x == "06":
            prompt = prompt.replace("a folded note with faded, illegible writing", "a note reading 'eat while warm'")
        if bad and x == "10":
            continue
        parts += [f"### 视角 {x}: 场景", "```text", prompt, "```", ""]
    md = "\n".join(parts)
    if bad:
        md = md.replace(f"Keep the upper body, {ifts}", ifts.replace("neat graying bob", "short gray hair"))
        md = md.replace("--no English, anime", "--no anime").replace("--no English, real living human", "--no doll, real living human")
        md = md.replace("grain station attendant resting", "char_12_BW attendant resting")
    return md


def self_test(cfg: dict) -> int:
    ok = True
    good = Character(name="char_99_BW_selftest", source="<good>", posture="BW")
    good.views, good.ifts = parse_prompts_md(_sample())
    good.ifts_source = "prompts.md"
    g = check(good, cfg)
    print(render(good, g))
    if any(i.level in ("BLOCKER", "MAJOR") for i in g):
        ok = False
        print("❌ GOOD 样例不应有 BLOCKER/MAJOR")
    bad = Character(name="char_98_BW_selftest", source="<bad>", posture="BW")
    bad.views, bad.ifts = parse_prompts_md(_sample(bad=True))
    bad.ifts_source = "prompts.md"
    b = check(bad, cfg)
    print(render(bad, b))
    got = {i.code for i in b}
    expect = {"COMPLETENESS", "IFTS_MISMATCH", "FRAMING", "SYNTAX", "NO_ENGLISH", "SELF_SABOTAGE", "CODE_LEAK",
              "TEXT_RENDER", "FUNERAL"}
    if expect - got:
        ok = False
        print(f"❌ BAD 样例漏检：{sorted(expect - got)}")
    print("\nSELF-TEST:", "PASS ✅" if ok else "FAIL ❌")
    return 0 if ok else 1


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="fullcolor 提示词校验器（规则源：config/paths.yml）")
    ap.add_argument("target", nargs="?", help="prompts.md / prompts.json / 人物目录")
    ap.add_argument("--all", action="store_true", help="批量审计素材库")
    ap.add_argument("--report", nargs="?", const="", default=None, help="批量模式输出 Markdown 报告（缺省写入 docs/latest-audit-report.md）")
    ap.add_argument("--only", help="只看指定检查组，逗号分隔")
    ap.add_argument("--export-json", nargs="?", const="", default=None, help="导出 prompts.json（缺省写到同目录）")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cfg = load_yaml()
    only = {s.strip() for s in args.only.split(",")} if args.only else None

    if args.self_test:
        return self_test(cfg)
    if args.all:
        return batch(cfg, args.report, args.json, only)
    if not args.target:
        ap.print_help()
        return 2
    ch = load_character(Path(args.target))
    if args.export_json is not None:
        out = Path(args.export_json).expanduser() if args.export_json else Path(ch.source).with_name("prompts.json")
        export_json(ch, cfg, out)
        print(f"已导出：{out}")
    issues = [i for i in check(ch, cfg) if not only or GROUP_OF.get(i.code) in only]
    if args.json:
        print(json.dumps({"character": ch.name, "posture": ch.posture, "views": len(ch.views),
                          "verdict": verdict(issues), "issues": [i.as_dict() for i in issues]}, ensure_ascii=False, indent=2))
    else:
        print(render(ch, issues))
    return 1 if any(i.level == "BLOCKER" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
