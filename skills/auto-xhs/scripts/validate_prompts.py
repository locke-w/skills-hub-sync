#!/usr/bin/env python3
"""auto-xhs 提示词校验器 validate_prompts.py

规则参数读取 config/studio.toml（单一数据源）。兼容旧格式人物（LEGACY_FORMAT）。

用法:
  validate_prompts.py <prompts.md|prompts.json|人物目录|编号> [更多目标…]   单/多个人物
  validate_prompts.py --all [--report [路径]] [--since N]   递归审计素材库（按 source_priority 去重）
  validate_prompts.py --batch <DIR...>                      批内比较：相似度阈值 + 四层变奏检查
  validate_prompts.py <文件> --only ifts,framing            只看指定检查组
  validate_prompts.py <目标> --export-json [输出路径]        从 prompts.md 导出 prompts.json
  validate_prompts.py --self-test
  追加 --json 输出机器可读结果

检查组: completeness ifts framing syntax english leak sabotage ratio wordcount text funeral
        cover empty profile anchor prop similarity variation legacy
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

LEVEL_ORDER = {"BLOCKER": 0, "MAJOR": 1, "MINOR": 2}
GROUP_OF = {
    "COMPLETENESS": "completeness", "IFTS_MISSING": "ifts", "IFTS_MISMATCH": "ifts",
    "IFTS_LENGTH": "ifts", "FRAMING": "framing", "SYNTAX": "syntax", "NO_ENGLISH": "english",
    "CODE_LEAK": "leak", "SELF_SABOTAGE": "sabotage", "RATIO": "ratio", "WORD_COUNT": "wordcount",
    "TEXT_RENDER": "text", "FUNERAL": "funeral", "CANDLE": "funeral", "COVER_SPACE": "cover",
    "EMPTY_WORDS": "empty", "PROFILE_MISSING": "profile", "PROFILE_INCOMPLETE": "profile",
    "ANCHOR": "anchor", "PROP": "prop", "SCENE_SIMILAR": "similarity", "VARIATION": "variation",
    "LEGACY_FORMAT": "legacy",
}
STOPWORDS = set("""a an the of and with on in at to for from by as into onto over under near beside next right left
her his their its our your she he they it is are was be being been that this these those which who while whose
6cm 12cm 6.0cm 12.0cm miniature figurine figure bust resin printed full color full-color photopolymer painted
tiny small old vintage warm gentle deeply poignant emotionally resonant documentary photograph photo
canon eos r5 rf kodak portra analog authentic shallow
shot lens film grain composition vertical soft light lighting cm scene background foreground focus depth field""".split())

FUNERAL_PHRASES = ["funeral", "memorial altar", "shrine", "incense burner", "offering table",
                   "black-and-white portrait", "mourning", "tombstone", "graveyard", "gravestone",
                   "funeral urn", "cremation ashes", "red candles"]


@dataclass
class Issue:
    level: str
    code: str
    msg: str

    def as_dict(self):
        return {"level": self.level, "code": self.code, "msg": self.msg}


def words(s: str) -> list[str]:
    return [w for w in s.split() if re.search(r"[A-Za-z0-9]", w)]


def norm(s: str) -> str:
    s = re.sub(r",?\s*Keep the upper body\s*,?", ", ", s, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"\s*,\s*", ", ", s)).strip(" ,")


def avoid_part(p: str) -> str:
    return p.split("Avoid:", 1)[1] if "Avoid:" in p else ""


def check(ch: C.Character, cfg: dict) -> list[Issue]:
    issues: list[Issue] = []
    add = lambda lv, code, msg: issues.append(Issue(lv, code, msg))
    v = ch.views
    square_cue = cfg["prompt"]["square_cue"]
    scene_cue = cfg["prompt"]["scene_cue"]
    cover_cue = cfg["prompt"]["cover_cue"]
    covers = cfg["generation"]["cover_candidates"]
    forbidden = cfg["prompt"].get("figurine_negative_forbidden", [])
    lo_w, hi_w = cfg["prompt"].get("ifts_words", [15, 20])
    sq_lo, sq_hi = cfg["prompt"].get("square_total_words", [50, 110])
    scene_views = cfg["generation"]["views_scene"]
    gem = [x for x in scene_views if x in v]

    # 完整性
    missing = [x for x in C.VIEWS if not v.get(x)]
    if missing:
        add("BLOCKER", "COMPLETENESS", f"缺少视角 {', '.join(missing)}（11 视角必须全量交付）")
    for x, p in v.items():
        if re.search(r"TODO|以此类推|此处省略|\.\.\.|…", p):
            add("BLOCKER", "COMPLETENESS", f"视角 {x} 含占位符/省略号")

    # profile
    profile_path = ch.dir / "character_profile.md"
    if not profile_path.is_file():
        add("MAJOR", "PROFILE_MISSING", "人物目录缺少 character_profile.md")
    else:
        t = profile_path.read_text(encoding="utf-8")
        lack = [d for d in ("D1", "D2", "D3", "D4", "D5") if not re.search(rf"\b{d}\b", t)]
        if lack:
            add("MAJOR", "PROFILE_INCOMPLETE", f"character_profile.md 缺少维度行：{', '.join(lack)}")

    # 旧格式人物：标 LEGACY_FORMAT 并跳过 00/01 新语法检查
    if ch.legacy:
        add("MINOR", "LEGACY_FORMAT", "旧格式人物（无 character.json / 00-01 为 Midjourney 语法），跳过新语法检查")

    # IFTS
    if not ch.ifts:
        add("BLOCKER", "IFTS_MISSING", "未找到 IFTS（character.json / prompts.md 第 0 节 / character_profile.md）")
    else:
        n = len(words(ch.ifts))
        if not lo_w <= n <= hi_w:
            add("MINOR", "IFTS_LENGTH", f"IFTS {n} 词，建议 {lo_w}–{hi_w}")
        for x in ("00", "01"):
            if v.get(x) and norm(ch.ifts) not in norm(v[x]):
                add("BLOCKER", "IFTS_MISMATCH", f"视角 {x} 未逐字包含 IFTS（来源：{ch.ifts_source}）")

    # 景别锁
    if ch.is_full:
        c00, c01 = v.get("00", "").count("full-body"), v.get("01", "").count("full-body")
        if c00 < 1 or c01 < 2:
            add("BLOCKER", "FRAMING", f"全身像需 full-body：00 ≥1 次（现 {c00}）、01 ≥2 次（现 {c01}）")
    elif ch.posture in ("BW", "BM"):
        lack = [x for x in ("00", "01") if "keep the upper body" not in v.get(x, "").lower()]
        if lack:
            add("BLOCKER", "FRAMING", f"胸像需 'Keep the upper body'：视角 {', '.join(lack)} 缺失")

    # 00/01 新语法（仅非 legacy）
    if not ch.legacy:
        for x in ("00", "01"):
            p = v.get(x)
            if not p:
                continue
            if not p.startswith(square_cue):
                add("MAJOR", "RATIO", f"视角 {x} 未以 '{square_cue}' 开头（应为 1:1）")
            if re.search(r"(?<![\w-])--[a-z]", p):
                add("BLOCKER", "SYNTAX", f"视角 {x} 含 Midjourney CLI 参数（新模板为 Gemini 自然语言）")
            if "Avoid:" not in p:
                add("BLOCKER", "NO_ENGLISH", f"视角 {x} 缺少 'Avoid:' 负向句")
            else:
                if "English text" not in avoid_part(p):
                    add("BLOCKER", "NO_ENGLISH", f"视角 {x} 的 Avoid 缺少 'English text, letters'")
                if not p.rstrip().endswith("."):
                    add("MINOR", "SYNTAX", f"视角 {x} 未以 Avoid 句收尾")
            tot = len(words(p))
            if not sq_lo <= tot <= sq_hi:
                add("MAJOR", "WORD_COUNT", f"视角 {x} 整段 {tot} 词，预算 {sq_lo}–{sq_hi}")
            if x == "01":
                bad = [t for t in forbidden if re.search(rf"\b{re.escape(t)}\b", avoid_part(p), re.I)]
                if bad:
                    add("BLOCKER", "SELF_SABOTAGE", f"视角 01 负向含 {bad}，会迫使模型生成真人")
            if re.search(r"masterpiece|\b8k\b|hyperrealistic|ultra detailed|smooth skin|best quality", p, re.I):
                add("MAJOR", "EMPTY_WORDS", f"视角 {x} 含空洞词")

    # 02–10
    anchor = (ch.cjson or {}).get("figurine_anchor")
    sig_en = (ch.cjson or {}).get("signature_props_en") or []
    no_ratio, no_cover = [], []
    for x in gem:
        p = v[x]
        if re.search(r"(?<![\w-])--[a-z]", p):
            add("BLOCKER", "SYNTAX", f"视角 {x}（Gemini）含 Midjourney CLI 参数")
        if not p.startswith(scene_cue):
            no_ratio.append(x)
        if "Avoid:" not in p:
            add("BLOCKER", "SYNTAX", f"视角 {x}（Gemini）缺少 'Avoid:' 负向句")
        else:
            av = avoid_part(p)
            if "English text, letters" not in av:
                add("BLOCKER", "NO_ENGLISH", f"视角 {x} 的 Avoid 缺少 'English text, letters'")
            bad = [t for t in forbidden if re.search(rf"\b{re.escape(t)}\b", av, re.I)]
            if bad:
                add("BLOCKER", "SELF_SABOTAGE", f"视角 {x} 的 Avoid 含禁词 {bad}（手办题材不得拦 figurine/doll 类）")
        if x in covers and cover_cue.lower() not in p.lower():
            no_cover.append(x)
        if anchor and anchor.lower() not in p.lower():
            add("MAJOR", "ANCHOR", f"视角 {x} 未逐字包含 figurine_anchor")
        if sig_en and not any(re.search(rf"\b{re.escape(w)}\b", p, re.I) for w in sig_en):
            add("MAJOR", "PROP", f"视角 {x} 未出现任一英文信物词 {sig_en}")
        if re.search(r"(reading|that says|which says|that reads|inscribed with|lettering)\s*['\"“‘]", p, re.I):
            add("MAJOR", "TEXT_RENDER", f"视角 {x} 要求渲染可读文字（易出乱码/英文）")
        fun = [ph for ph in FUNERAL_PHRASES if re.search(re.escape(ph), p, re.I)]
        if fun:
            add("MAJOR", "FUNERAL", f"视角 {x} 含灵堂/供桌意象：{sorted(fun)}")
        if re.search(r"\bcandles?\b", p, re.I):
            add("MINOR", "CANDLE", f"视角 {x} 含蜡烛，注意避免供桌感")
    if no_ratio:
        add("MAJOR", "RATIO", f"{len(no_ratio)}/{len(gem)} 张场景图未以 '{scene_cue}' 开头")
    if no_cover:
        add("MINOR", "COVER_SPACE", f"封面候选视角 {', '.join(no_cover)} 未预留标题留白")

    # 代码泄露
    for x, p in v.items():
        m = re.search(r"char_\d+|\b(?:BW|BM|FW|FM)_|/Users/|obsidian", p)
        if m:
            add("BLOCKER", "CODE_LEAK", f"视角 {x} 泄露内部代号「{m.group(0)}」")
    issues.sort(key=lambda i: LEVEL_ORDER[i.level])
    return issues


# ---------------------------------------------------------------- 场景相似度
def content_tokens(prompt: str, ch: C.Character, cfg: dict) -> set[str]:
    body = prompt.split("Avoid:", 1)[0]
    body = re.split(r"\bShot on\b", body, maxsplit=1)[0]
    for cue in (cfg["prompt"]["scene_cue"], cfg["prompt"]["cover_cue"],
                cfg["prompt"]["square_cue"]):
        body = body.replace(cue, " ")
    anchor = (ch.cjson or {}).get("figurine_anchor")
    if anchor:
        body = body.replace(anchor, " ")
    toks = {t for t in re.findall(r"[a-z][a-z'-]{2,}", body.lower())} - STOPWORDS
    if ch.ifts:
        toks -= set(re.findall(r"[a-z][a-z'-]{2,}", ch.ifts.lower()))
    return toks


def scene_similarity(chars: list[C.Character], cfg: dict, threshold: float,
                     slots: list[str]) -> dict[str, list[tuple[float, str, str]]]:
    hits: dict[str, list] = defaultdict(list)
    for slot in slots:
        docs = {c.name: content_tokens(c.views[slot], c, cfg) for c in chars if c.views.get(slot)}
        for (a, sa), (b, sb) in combinations(docs.items(), 2):
            if sa and sb:
                j = len(sa & sb) / len(sa | sb)
                if j >= threshold:
                    hits[a].append((j, slot, b))
                    hits[b].append((j, slot, a))
    return hits


def variation_check(chars: list[C.Character]) -> list[tuple[str, str, str]]:
    """批内同槽位四层（camera/location/prop/light）至少两层不同。返回 (slot, a, b)。"""
    out = []
    slots = sorted({s for c in chars if c.cjson for s in c.cjson.get("scenes", {})})
    for slot in slots:
        have = [c for c in chars if c.cjson and slot in c.cjson.get("scenes", {})]
        for a, b in combinations(have, 2):
            sa, sb = a.cjson["scenes"][slot], b.cjson["scenes"][slot]
            same = sum(1 for k in ("camera", "location", "prop", "light")
                       if str(sa.get(k, "")).strip().lower() == str(sb.get(k, "")).strip().lower())
            if 4 - same < 2:
                out.append((slot, a.name, b.name))
    return out


# ---------------------------------------------------------------- 输出
def verdict(issues: list[Issue]) -> str:
    lv = {i.level for i in issues}
    return "❌ 禁止交付（存在 BLOCKER）" if "BLOCKER" in lv else \
        ("⚠️ 建议修正（存在 MAJOR）" if "MAJOR" in lv else "✅ 通过")


def render(ch: C.Character, issues: list[Issue]) -> str:
    out = [f"📄 {ch.name}",
           f"   姿态 {ch.posture or '未知'} | 视角 {len(ch.views)}/11 | IFTS 来源 {ch.ifts_source if ch.ifts else '—'}"
           + (" | 旧格式" if ch.legacy else "")]
    icons = {"BLOCKER": "❌", "MAJOR": "⚠️", "MINOR": "ℹ️"}
    for lv in LEVEL_ORDER:
        group = [i for i in issues if i.level == lv]
        if group:
            out.append(f"   {icons[lv]} {lv} ({len(group)})")
            out += [f"      [{i.code}] {i.msg}" for i in group]
    out.append(f"   结论：{verdict(issues)}")
    return "\n".join(out)


def export_json(ch: C.Character, cfg: dict, out: Path) -> None:
    data = {"character": ch.name, "posture": ch.posture,
            "identity_fingerprint_tokens": ch.ifts,
            "figurine_anchor": (ch.cjson or {}).get("figurine_anchor"),
            "generated_by": "scripts/validate_prompts.py --export-json"}
    for x in C.VIEWS:
        if x in ch.views:
            ratio = "1:1" if x in cfg["generation"]["views_square"] else cfg["images"]["scene_ratio"]
            data[x] = {"raw_prompt": ch.views[x], "engine": "gemini", "aspect_ratio": ratio}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def batch(cfg: dict, report: str | None, as_json: bool, only: set[str] | None,
          since: int | None) -> int:
    found = C.scan_char_dirs(cfg)
    chars, results = [], {}
    for num, ds in sorted(found.items()):
        if since is not None and num < since:
            continue
        d = C.pick_dir(cfg, ds)
        if not ((d / "prompts.md").exists() or (d / "prompts.json").exists()):
            continue
        ch = C.load_character(cfg, d)
        chars.append(ch)
        results[ch.name] = [i for i in check(ch, cfg) if not only or GROUP_OF.get(i.code) in only]
    thr = float(C.cfg_get(cfg, "dedup.scene_similarity_library", 0.5))
    if not only or "similarity" in only:
        for name, pairs in scene_similarity(chars, cfg, thr, cfg["generation"]["views_scene"]).items():
            for j, slot, other in sorted(pairs, reverse=True)[:2]:
                results[name].append(Issue("MAJOR", "SCENE_SIMILAR",
                                           f"视角 {slot} 与 {other[:18]} 相似度 {j:.2f}（阈值 {thr}）"))
    summarize(results, chars, as_json)
    if report is not None:
        out = Path(report).expanduser() if report else C.reports_dir(cfg) / "prompts-audit.md"
        write_report(out, cfg, results, chars)
        if not as_json:
            print(f"报告已写入：{out}")
    return 0


def summarize(results: dict, chars: list[C.Character], as_json: bool) -> None:
    total = len(results)
    blocked = sum(1 for r in results.values() if any(i.level == "BLOCKER" for i in r))
    major = sum(1 for r in results.values()
                if not any(i.level == "BLOCKER" for i in r) and any(i.level == "MAJOR" for i in r))
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


def write_report(out: Path, cfg: dict, results: dict, chars: list[C.Character]) -> None:
    total = len(results)
    blocked = sum(1 for r in results.values() if any(i.level == "BLOCKER" for i in r))
    major = sum(1 for r in results.values()
                if not any(i.level == "BLOCKER" for i in r) and any(i.level == "MAJOR" for i in r))
    per_code = Counter()
    for r in results.values():
        per_code.update({f"{i.level} {i.code}" for i in r})
    lines = ["# auto-xhs 素材库提示词质量审计报告", "",
             f"> 生成时间：{datetime.now():%Y-%m-%d %H:%M} · 校验器 `scripts/validate_prompts.py` · 规则源 `config/studio.toml`",
             f"> 扫描目录：`{C.material_root(cfg)}`（含归档，按 source_priority 去重）", "",
             "| 人物数 | ✅ 通过 | ⚠️ 仅 MAJOR | ❌ 含 BLOCKER |", "| --- | --- | --- | --- |",
             f"| {total} | {total - blocked - major} | {major} | {blocked} |", "",
             "## 问题分布（按人物计）", "", "| 级别 · 规则 | 人物数 |", "| --- | --- |"]
    lines += [f"| {k} | {n} |" for k, n in per_code.most_common()]
    lines += ["", "## 逐个人物", "",
              "| 人物 | 来源 | 姿态 | BLOCKER | MAJOR | MINOR | 主要问题 |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    by_name = {c.name: c for c in chars}
    for name, r in results.items():
        c = Counter(i.level for i in r)
        top = ", ".join(sorted({i.code for i in r if i.level != "MINOR"}))
        ch = by_name.get(name)
        lines.append(f"| {name} | {ch.source or '根目录' if ch else '—'} | {ch.posture if ch else ''} "
                     f"| {c['BLOCKER']} | {c['MAJOR']} | {c['MINOR']} | {top} |")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- self-test
def _sample(bad: bool = False) -> str:
    ifts = ("63-year-old Chinese mother-in-law, angular stern cheekbones, neat graying bob, "
            "precise watchful eyes, ink-stained fingers, old wooden steelyard with brass hook")
    p00 = (f"Square 1:1 composition. Candid documentary portrait photograph of a real {ifts}, "
           "Keep the upper body, behind the grain station counter, wearing navy cotton work smock "
           "with black oversleeves, soft indoor natural light. Shot on Hasselblad 90mm f/3.2, "
           "Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d render, "
           "CGI, doll, figurine, plastic skin, beauty filter, western features, youthful face, deformed hands.")
    p01 = (f"Square 1:1 composition. Macro studio product photo of a 6.0cm 3D printed painted resin "
           f"bust, Keep the upper body, {ifts}, sculpted navy cotton work smock with black "
           "oversleeves, mounted on a dark beveled pedestal base, subtle resin SSS finish, "
           "light gray cyclorama, softbox lighting. Shot on RF 100mm f/8. Avoid: English text, "
           "letters, real living human, skin pores, plaster, stone column, room, furniture, "
           "outdoor scenery, western features, youthful face, deformed hands.")
    avoid = ("Avoid: English text, letters, watermark, anime, cartoon, CGI look, cheap toy plastic "
             "shine, western features, youthful face, deformed hands, extra fingers, missing "
             "fingers, floating objects, broken geometry.")
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
    parts = ["# char_99_BW 自测人物", "", "## 0. 人物唯一性指纹 Token 序列 (IFTS)", "",
             "```text", ifts, "```", "", "## 一、 建模参考视角（00 & 01 · 1:1）", "",
             "### 视角 00: 基底定妆照", "```text", p00, "```", "",
             "### 视角 01: 模型标准像", "```text", p01, "```", "", "## 二、 Gemini 场景视角", ""]
    for x, sc in scenes.items():
        cover = "Leave clean negative space in the upper third for a title overlay. " if x in ("07", "10") else ""
        prompt = (f"Vertical 3:4 composition. A warm documentary photograph of the 6cm resin bust of "
                  f"a 63-year-old Chinese grain station mother-in-law in a navy smock {sc}. {cover}"
                  f"Shot on Canon EOS R5 with RF 50mm f/1.4 lens, Kodak Portra 400 tones. {avoid}")
        if bad and x == "03":
            prompt = prompt.replace("glass-front family display cabinet",
                                    "family shrine with an incense burner") + " --ar 3:4"
        if bad and x == "06":
            prompt = prompt.replace("a folded note with faded, illegible writing",
                                    "a note reading 'eat while warm'")
        if bad and x == "10":
            continue
        parts += [f"### 视角 {x}: 场景", "```text", prompt, "```", ""]
    md = "\n".join(parts)
    if bad:
        md = md.replace(f"Keep the upper body, {ifts}",
                        ifts.replace("neat graying bob", "short gray hair"))
        md = md.replace("Avoid: English text, letters, anime",
                        "Avoid: anime").replace(
            "Avoid: English text, letters, real living human",
            "Avoid: doll, real living human", 1)
        md = md.replace("grain station mother-in-law in a navy smock resting",
                        "char_12_BW attendant resting")
    return md


def self_test(cfg: dict) -> int:
    ok = True
    tmp = Path("/tmp/auto-xhs/_selftest_char")
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "character_profile.md").write_text(
        "# 自测\n- **D1 面部骨相指纹**：x\n- **D2 生理微瑕签名**：x\n"
        "- **D3 服饰色彩 DNA**：x\n- **D4 随身信物锚定**：x\n- **D5 神态动态基线**：x\n",
        encoding="utf-8")
    good = C.Character(dir=tmp, name="char_99_BW_selftest", posture="BW", has_profile=True)
    good.views, good.ifts = C.parse_prompts_md(_sample())
    good.ifts_source = "prompts.md"
    g = check(good, cfg)
    print(render(good, g))
    if any(i.level in ("BLOCKER", "MAJOR") for i in g):
        ok = False
        print("❌ GOOD 样例不应有 BLOCKER/MAJOR")
    bad = C.Character(dir=tmp, name="char_98_BW_selftest", posture="BW", has_profile=True)
    bad.views, bad.ifts = C.parse_prompts_md(_sample(bad=True))
    bad.ifts_source = "prompts.md"
    b = check(bad, cfg)
    print(render(bad, b))
    got = {i.code for i in b}
    expect = {"COMPLETENESS", "IFTS_MISMATCH", "FRAMING", "SYNTAX", "NO_ENGLISH",
              "SELF_SABOTAGE", "CODE_LEAK", "TEXT_RENDER", "FUNERAL"}
    if expect - got:
        ok = False
        print(f"❌ BAD 样例漏检：{sorted(expect - got)}")
    print("\nSELF-TEST:", "PASS ✅" if ok else "FAIL ❌")
    return 0 if ok else 1


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="auto-xhs 提示词校验器（规则源：config/studio.toml）")
    ap.add_argument("targets", nargs="*", help="prompts.md / prompts.json / 人物目录 / 编号，可多个")
    ap.add_argument("--all", action="store_true", help="递归审计素材库（含归档，按优先级去重）")
    ap.add_argument("--since", type=int, default=None, help="--all 时只审编号 ≥N")
    ap.add_argument("--batch", action="store_true", help="位置参数为一批：批内相似度+四层变奏")
    ap.add_argument("--report", nargs="?", const="", default=None,
                    help="批量模式输出报告（缺省 MATERIAL/_reports/prompts-audit.md）")
    ap.add_argument("--only", help="只看指定检查组，逗号分隔")
    ap.add_argument("--export-json", nargs="?", const="", default=None)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    only = {s.strip() for s in args.only.split(",")} if args.only else None

    if args.self_test:
        return self_test(cfg)
    if args.all:
        return batch(cfg, args.report, args.json, only, args.since)
    if not args.targets:
        ap.print_help()
        return 2

    chars = [C.load_character(cfg, C.resolve_char_dir(cfg, t) if not Path(t).expanduser().is_file()
                             else Path(t).expanduser().parent) for t in args.targets]
    if args.batch:
        thr = float(C.cfg_get(cfg, "dedup.scene_similarity_batch", 0.35))
        results = {ch.name: [i for i in check(ch, cfg) if not only or GROUP_OF.get(i.code) in only]
                   for ch in chars}
        if not only or "similarity" in only:
            for name, pairs in scene_similarity(chars, cfg, thr, cfg["generation"]["views_scene"]).items():
                for j, slot, other in sorted(pairs, reverse=True)[:3]:
                    results[name].append(Issue("MAJOR", "SCENE_SIMILAR",
                                               f"批内视角 {slot} 与 {other[:18]} 相似度 {j:.2f}（批阈值 {thr}）"))
        if not only or "variation" in only:
            nojson = [c.name for c in chars if not c.cjson]
            for c in nojson:
                results[c].append(Issue("MINOR", "VARIATION", "无 character.json，跳过四层变奏检查"))
            for slot, a, b in variation_check(chars):
                msg = f"批内视角 {slot}：{a[:16]} 与 {b[:16]} 四层（机位/实景/道具/光影）不同层数 <2"
                results[a].append(Issue("MAJOR", "VARIATION", msg))
                results[b].append(Issue("MAJOR", "VARIATION", msg))
        summarize(results, chars, args.json)
        if not args.json:
            for ch in chars:
                print(render(ch, results[ch.name]))
        return 1 if any(i.level == "BLOCKER" for r in results.values() for i in r) else 0

    worst = 0
    for ch in chars:
        if args.export_json is not None:
            out = Path(args.export_json).expanduser() if args.export_json \
                else ch.dir / "prompts.json"
            export_json(ch, cfg, out)
            print(f"已导出：{out}")
        issues = [i for i in check(ch, cfg) if not only or GROUP_OF.get(i.code) in only]
        if args.json:
            print(json.dumps({"character": ch.name, "posture": ch.posture, "views": len(ch.views),
                              "verdict": verdict(issues),
                              "issues": [i.as_dict() for i in issues]}, ensure_ascii=False, indent=2))
        else:
            print(render(ch, issues))
        if any(i.level == "BLOCKER" for i in issues):
            worst = 1
    return worst


if __name__ == "__main__":
    sys.exit(main())
