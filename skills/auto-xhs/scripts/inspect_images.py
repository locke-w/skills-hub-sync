#!/usr/bin/env python3
"""auto-xhs 图片目录检查 inspect_images.py

给出图片状态机判定（EXIT / GENERATE / REUSE）、每张图的尺寸与比例、笔记配图比例是否统一、
封面候选图是否存在；同号多格式（0.jpeg+0.png）报 DUP_FORMAT；场景图非 3:4 报出。
配置读 config/studio.toml。

用法:
  inspect_images.py char_45 | 75 | /path/to/图片目录 [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402


def inspect(cfg: dict, folder: Path) -> dict:
    files = C.asset_files(folder)
    items = []
    for f in files:
        size = C.image_size(f)
        items.append({"name": f.name, "width": size[0] if size else None,
                      "height": size[1] if size else None,
                      "ratio": C.ratio_name(*size) if size else "未知"})
    n = len(files)
    base = [f for f in files if f.stem == "0"]
    if n == 0:
        state, advice = "EXIT", "目录中没有图片：运行 gemini_app.py 生成视角 00–10，或先放入底图 0.jpg。"
    elif n == 1 and base:
        state, advice = "GENERATE", "仅有底图 0.*：运行 gemini_app.py 生成 01 与场景图。"
    elif n == 1:
        state, advice = "ATTENTION", "只有 1 张且不叫 0.*：请确认它是否为底图，是则重命名为 0.jpg。"
    else:
        state, advice = "REUSE", "已有 ≥2 张图：跳过生图，直接挑选封面与图序。"

    # 同号多格式 DUP_FORMAT
    by_stem = defaultdict(list)
    for f in files:
        key = f.stem if f.stem in ("0", "1") else re.match(r"视角\d+", f.name).group(0) \
            if re.match(r"视角\d+", f.name) else f.stem
        by_stem[key].append(f.suffix.lower())
    dup = {k: v for k, v in by_stem.items() if len(v) > 1}

    scene_ratio = cfg["images"]["scene_ratio"]
    note_imgs = [i for i in items if i["name"].startswith("视角")]
    ratios = sorted({i["ratio"] for i in note_imgs})
    off_ratio = [i["name"] for i in note_imgs if i["ratio"] != scene_ratio]
    covers = [i["name"] for i in note_imgs
              if re.match(r"视角(07|10)", i["name"])]
    min_edge = cfg["images"].get("min_long_edge", 0)
    small = [i["name"] for i in items
             if i["width"] and max(i["width"], i["height"]) < min_edge]
    return {"folder": str(folder), "count": n, "state": state, "advice": advice,
            "images": items, "dup_format": dup, "note_ratios": ratios,
            "ratio_consistent": len(ratios) <= 1, "off_ratio": off_ratio,
            "cover_candidates": covers, "below_min_edge": small}


def main() -> int:
    ap = argparse.ArgumentParser(description="人物图片目录检查（auto-xhs）")
    ap.add_argument("target", help="char 编号（如 45 / char_45）或图片目录路径")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    p = Path(args.target).expanduser()
    folder = p if p.is_dir() else C.resolve_char_dir(cfg, args.target, where="asset")
    r = inspect(cfg, folder)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"📁 {r['folder']}")
    print(f"   图片 {r['count']} 张 → 状态机：{r['state']}")
    print(f"   {r['advice']}")
    for i in r["images"]:
        print(f"   - {i['name']:<24} {i['width']}x{i['height']}  {i['ratio']}")
    if r["dup_format"]:
        for k, v in r["dup_format"].items():
            print(f"   ⚠️ DUP_FORMAT：{k}.* 多格式并存 {v}（gemini_app.py 引用优先级 jpg > jpeg > png）")
    if r["note_ratios"]:
        tip = "✅ 统一" if r["ratio_consistent"] else "⚠️ 不统一：一篇笔记内请只用同一比例"
        print(f"   笔记配图比例：{', '.join(r['note_ratios'])} {tip}")
        if r["off_ratio"]:
            print(f"   ⚠️ 非 {cfg['images']['scene_ratio']} 场景图：{', '.join(r['off_ratio'])}")
    if r["below_min_edge"]:
        print(f"   ⚠️ 长边 < {cfg['images']['min_long_edge']}：{', '.join(r['below_min_edge'])}")
    print(f"   封面候选：{', '.join(r['cover_candidates']) or '无（缺视角07/10）'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
