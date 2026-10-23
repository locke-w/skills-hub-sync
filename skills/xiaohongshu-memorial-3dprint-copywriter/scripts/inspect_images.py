#!/usr/bin/env python3
"""人物图片目录检查 inspect_images.py (v1.0)

给出图片状态机判定（EXIT / GENERATE / REUSE）、每张图的尺寸与比例、笔记配图比例是否统一、
封面候选图是否存在。只用标准库解析 PNG / JPEG / WebP 头信息。

用法:
  python3 scripts/inspect_images.py char_45                  # 按编号在图片存储根目录中查找
  python3 scripts/inspect_images.py /path/to/图片目录 [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config" / "constants.md"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def config_value(key: str, default: str = "") -> str:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    m = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*(?:#.*)?$", text, re.M)
    return m.group(1).strip().strip('"') if m else default


def image_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as f:
        head = f.read(32)
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            return struct.unpack(">II", head[16:24])
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            chunk = head[12:16]
            f.seek(0)
            data = f.read(40)
            if chunk == b"VP8X":
                w = 1 + int.from_bytes(data[24:27], "little")
                h = 1 + int.from_bytes(data[27:30], "little")
                return w, h
            if chunk == b"VP8L":
                b = data[21:25]
                w = 1 + (((b[1] & 0x3F) << 8) | b[0])
                h = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
                return w, h
            if chunk == b"VP8 ":
                w, h = struct.unpack("<HH", data[26:30])
                return w & 0x3FFF, h & 0x3FFF
            return None
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                marker = f.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    return None
                code = marker[1]
                if code in (0xD8, 0x01) or 0xD0 <= code <= 0xD7:
                    continue
                seg_len = struct.unpack(">H", f.read(2))[0]
                if code in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    f.read(1)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h
                f.seek(seg_len - 2, 1)
    return None


def ratio_name(w: int, h: int) -> str:
    r = w / h
    for name, target in (("1:1", 1.0), ("3:4", 0.75), ("4:3", 4 / 3), ("2:3", 2 / 3), ("9:16", 9 / 16), ("16:9", 16 / 9)):
        if abs(r - target) < 0.02:
            return name
    return f"{w}:{h}"


def resolve(arg: str) -> Path:
    p = Path(arg).expanduser()
    if p.is_dir():
        return p
    root = Path(config_value("图片存储根目录")).expanduser()
    hits = sorted(root.glob(f"{arg}*")) if root.is_dir() else []
    if not hits:
        raise SystemExit(f"❌ 找不到图片目录：{arg}（图片存储根目录：{root}）")
    return hits[0]


def inspect(folder: Path) -> dict:
    files = sorted(f for f in folder.iterdir() if f.suffix.lower() in EXTS)
    items = []
    for f in files:
        size = image_size(f)
        items.append({"name": f.name, "width": size[0] if size else None, "height": size[1] if size else None,
                      "ratio": ratio_name(*size) if size else "未知"})
    n = len(files)
    base = [f for f in files if f.stem == "0"]
    if n == 0:
        state, advice = "EXIT", "目录中没有图片：请放入底图 0.jpg，或先用 fullcolor-3dprint-character-prompts 出图。"
    elif n == 1 and base:
        state, advice = "GENERATE", "仅有底图 0.*：读取 Obsidian 中的 prompts.md，以 0.* 为参考图生成场景图（需当前环境有生图工具）。"
    elif n == 1:
        state, advice = "ATTENTION", "只有 1 张且不叫 0.*：请确认它是否为底图，是则重命名为 0.jpg。"
    else:
        state, advice = "REUSE", "已有 ≥2 张图：跳过生图，直接挑选封面与图序。"
    note_imgs = [i for i in items if i["name"].startswith("视角")]
    ratios = sorted({i["ratio"] for i in note_imgs})
    covers = [i["name"] for i in note_imgs if re.match(r"视角(07|10)", i["name"])]
    return {"folder": str(folder), "count": n, "state": state, "advice": advice, "images": items,
            "note_ratios": ratios, "ratio_consistent": len(ratios) <= 1, "cover_candidates": covers}


def main() -> int:
    ap = argparse.ArgumentParser(description="人物图片目录检查")
    ap.add_argument("target", help="char 编号前缀（如 char_45）或图片目录路径")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = inspect(resolve(args.target))
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"📁 {r['folder']}")
    print(f"   图片 {r['count']} 张 → 状态机：{r['state']}")
    print(f"   {r['advice']}")
    for i in r["images"]:
        print(f"   - {i['name']:<24} {i['width']}x{i['height']}  {i['ratio']}")
    if r["note_ratios"]:
        tip = "✅ 统一" if r["ratio_consistent"] else "⚠️ 不统一：一篇笔记内请只用同一比例"
        print(f"   笔记配图比例：{', '.join(r['note_ratios'])} {tip}")
        if r["note_ratios"] == ["1:1"]:
            print("   ℹ️ 存量 1:1 素材：整篇保持 1:1；需要冲点击时让 fullcolor 整组重出 3:4。")
    print(f"   封面候选：{', '.join(r['cover_candidates']) or '无（缺视角07/10）'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
