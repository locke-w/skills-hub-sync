#!/usr/bin/env python3
"""auto-xhs 阶段 4：素材库登记与去重 library.py

用法:
  library.py --registry                    写 MATERIAL/_reports/registry.json
  library.py --dedup <character.json>      对该人物做全库去重，超阈值退出码 1
  library.py --next-id                     全库（含归档）最大编号 +1
  library.py --dupes                       列出同编号多副本及采用的那份
  library.py --index                       写 MATERIAL/_reports/index.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402


def ifts_tokens(ifts: str, ignore: set[str]) -> set[str]:
    toks = {t for t in re.findall(r"[a-z][a-z'-]*", ifts.lower())} - ignore
    return toks


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def cjk_bigrams(s: str) -> set[str]:
    chars = [c for c in s if "一" <= c <= "鿿"]
    return {chars[i] + chars[i + 1] for i in range(len(chars) - 1)}


def registry_entry(cfg: dict, d: Path) -> dict:
    ch = C.load_character(cfg, d)
    e = {"num": ch.num, "dir": ch.name, "source": ch.source or "(根目录)",
         "source_rel": ch.source,
         "posture": ch.posture, "ifts": ch.ifts, "ifts_source": ch.ifts_source,
         "props": [], "colors": [], "vocation": "", "generation": "",
         "has_character_json": ch.cjson is not None, "d3_raw": "", "d4_raw": "",
         "needs_manual": False}
    if ch.cjson:
        e["props"] = ch.cjson.get("signature_props", [])
        e["colors"] = ch.cjson.get("colors", [])
        e["vocation"] = ch.cjson.get("vocation", "")
        e["generation"] = ch.cjson.get("generation", "")
        card = ch.cjson.get("card", {})
        e["d3_raw"], e["d4_raw"] = card.get("d3", ""), card.get("d4", "")
    profile = d / "character_profile.md"
    if profile.is_file():
        t = profile.read_text(encoding="utf-8")
        e["d3_raw"] = e["d3_raw"] or C.profile_field(t, "D3 服饰色彩 DNA")
        e["d4_raw"] = e["d4_raw"] or C.profile_field(t, "D4 随身信物锚定")
        if not e["generation"]:
            kin = C.profile_field(t, "代际亲缘")
            for g in ("祖辈", "父辈", "伴侣", "配偶", "姻亲"):
                if g in kin:
                    e["generation"] = "配偶" if g == "伴侣" else g
                    break
        if not e["vocation"]:
            e["vocation"] = re.sub(r"^char_\d+_[BF][MW]_", "", ch.name)
    if not ch.ifts:
        e["needs_manual"] = True
    return e


def load_registry(cfg: dict) -> list[dict]:
    """按 source_priority 去重后的全库登记表。"""
    found = C.scan_char_dirs(cfg)
    return [registry_entry(cfg, C.pick_dir(cfg, ds)) for _, ds in sorted(found.items())]


def cmd_registry(cfg: dict) -> int:
    entries = load_registry(cfg)
    out = C.reports_dir(cfg) / "registry.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    nm = sum(1 for e in entries if e["needs_manual"])
    print(f"registry 已写入：{out}")
    print(f"人物总数 {len(entries)} · needs_manual {nm} · 有 character.json {sum(1 for e in entries if e['has_character_json'])}")
    return 0


def dedup_summary(cfg: dict, doc: dict) -> dict:
    """对 character.json 文档做全库去重，返回结构化结果（render_character 复用）。"""
    entries = [e for e in load_registry(cfg) if e["num"] != doc.get("num")]
    ignore = set(C.cfg_get(cfg, "dedup.ifts_ignore", []))
    thr = float(C.cfg_get(cfg, "dedup.ifts_jaccard_max", 0.35))
    my = ifts_tokens(doc.get("ifts", ""), ignore)
    scored = sorted(
        ((jaccard(my, ifts_tokens(e.get("ifts") or "", ignore)), e) for e in entries),
        key=lambda x: -x[0])
    top = scored[0] if scored else (0.0, None)

    my_prop = cjk_bigrams("".join(doc.get("signature_props", [])))
    my_voc = cjk_bigrams(doc.get("vocation", ""))
    my_col = cjk_bigrams("".join(doc.get("colors", [])))
    rows = []
    for e in entries:
        other_prop = cjk_bigrams("".join(e.get("props", [])) + e.get("d4_raw", ""))
        other_voc = cjk_bigrams(e.get("vocation", "") + e["dir"])
        other_col = cjk_bigrams("".join(e.get("colors", [])) + e.get("d3_raw", ""))
        rows.append((len(my_prop & other_prop), len(my_voc & other_voc),
                     len(my_col & other_col), e))
    rows.sort(key=lambda r: -(r[0] + r[1] + r[2]))
    return {"ifts_jaccard_max": top[0], "ifts_jaccard_peer": top[1]["dir"] if top[1] else "—",
            "ifts_threshold": thr, "ifts_scored_top5": scored[:5], "overlap_top5": rows[:5],
            "over": top[0] >= thr}


def cmd_dedup(cfg: dict, cj_path: str) -> int:
    doc = json.loads(Path(cj_path).expanduser().read_text(encoding="utf-8"))
    s = dedup_summary(cfg, doc)
    thr = s["ifts_threshold"]
    print(f"IFTS Jaccard 全库最高：{s['ifts_jaccard_max']:.2f}（对象 {s['ifts_jaccard_peer']}，阈值 {thr}）")
    for j, e in s["ifts_scored_top5"]:
        print(f"   {j:.2f}  {e['dir']}")
    print("信物/职业/主色中文 2-gram 重合 top5（信物/职业/色彩）：")
    for p, v, c, e in s["overlap_top5"]:
        print(f"   {p}/{v}/{c}  {e['dir']}")
    # 供 render_character 写入 profile 的表格行
    rows = s["overlap_top5"]
    print("\nDEDUP_ROW|" + "|".join([
        f"IFTS|{len(doc.get('ifts','').split())} 词|全库最高 Jaccard {s['ifts_jaccard_max']:.2f}（{s['ifts_jaccard_peer']}），阈值 {thr}",
        f"信物|{' + '.join(doc.get('signature_props', []))}|top 重合 {rows[0][0] if rows else 0} 个 2-gram",
        f"色彩|{' + '.join(doc.get('colors', []))}|见上表",
        f"职业|{doc.get('vocation','')}|见上表",
    ]))
    return 1 if s["over"] else 0


def cmd_next_id(cfg: dict) -> int:
    found = C.scan_char_dirs(cfg)
    nxt = (max(found) + 1) if found else 1
    print(nxt)
    return 0


def cmd_dupes(cfg: dict) -> int:
    found = C.scan_char_dirs(cfg)
    n = 0
    for num, ds in sorted(found.items()):
        if len(ds) > 1:
            chosen = C.pick_dir(cfg, ds)
            n += 1
            print(f"char_{num:02d} ×{len(ds)}：")
            for d in ds:
                mark = "✅ 采用" if d == chosen else "   副本"
                print(f"   {mark}  {d}")
    print(f"共 {n} 个编号存在多副本" if n else "无多副本编号")
    return 0


def cmd_index(cfg: dict) -> int:
    entries = load_registry(cfg)
    asset = C.asset_root(cfg)
    copy_name = C.cfg_get(cfg, "copy.filename", "小红书文案.md")
    lines = ["# 素材库索引", "",
             f"> 生成时间：{datetime.now():%Y-%m-%d %H:%M} · `library.py --index`", "",
             "| 编号 | 目录 | 规格 | 信物 | IFTS 词数 | 图片 | 文案 |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for e in entries:
        spec = ("全身 12cm" if e["posture"] in ("FW", "FM") else "胸像 6cm") if e["posture"] else "—"
        nw = len(e["ifts"].split()) if e["ifts"] else 0
        imgs = len(C.asset_files(asset / e["dir"]))
        has_copy = (C.material_root(cfg) / e["source_rel"] / e["dir"] / copy_name).is_file()
        lines.append(f"| {e['num']} | {e['dir']} | {spec} | {'、'.join(e['props']) or '—'} | {nw} | {imgs} 张 | {'✅' if has_copy else '—'} |")
    out = C.reports_dir(cfg) / "index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index 已写入：{out}（{len(entries)} 人）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="auto-xhs 素材库登记与去重")
    ap.add_argument("--registry", action="store_true")
    ap.add_argument("--dedup", metavar="CHARACTER_JSON")
    ap.add_argument("--next-id", action="store_true")
    ap.add_argument("--dupes", action="store_true")
    ap.add_argument("--index", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    if args.registry:
        return cmd_registry(cfg)
    if args.dedup:
        return cmd_dedup(cfg, args.dedup)
    if args.next_id:
        return cmd_next_id(cfg)
    if args.dupes:
        return cmd_dupes(cfg)
    if args.index:
        return cmd_index(cfg)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
