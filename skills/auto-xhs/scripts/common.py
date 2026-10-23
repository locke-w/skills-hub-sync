#!/usr/bin/env python3
"""auto-xhs 公共库：配置加载、素材库扫描、Character 解析。只读 config/studio.toml。"""
from __future__ import annotations

import json
import re
import struct
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config" / "studio.toml"
LEXICON_PATH = SKILL_ROOT / "config" / "copy_lexicon.json"
VIEWS = [f"{i:02d}" for i in range(11)]
CHAR_DIR_RE = re.compile(r"^char_(\d+)_([BF][MW])_")
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def load_config(path: Path = CONFIG_PATH) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def cfg_get(cfg: dict, dotted: str, default=None):
    cur = cfg
    for k in dotted.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def material_root(cfg: dict) -> Path:
    return Path(cfg["paths"]["material"]).expanduser()


def asset_root(cfg: dict) -> Path:
    return Path(cfg["paths"]["asset"]).expanduser()


def reports_dir(cfg: dict) -> Path:
    return material_root(cfg) / cfg["paths"].get("reports_dirname", "_reports")


def load_lexicon() -> dict:
    return json.loads(LEXICON_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 素材库扫描
def char_num(dirname: str) -> int | None:
    m = CHAR_DIR_RE.match(dirname)
    return int(m.group(1)) if m else None


def source_rel(cfg: dict, char_dir: Path) -> str:
    """char 目录相对 MATERIAL 的父路径（''=根目录）。"""
    try:
        rel = char_dir.parent.relative_to(material_root(cfg))
    except ValueError:
        return ""
    return "" if str(rel) == "." else str(rel)


def scan_char_dirs(cfg: dict) -> dict[int, list[Path]]:
    """递归扫描 MATERIAL（跳过 _reports），返回 num -> [char_dir,...]（全部副本）。"""
    base = material_root(cfg)
    reports = cfg["paths"].get("reports_dirname", "_reports")
    found: dict[int, list[Path]] = {}
    for d in sorted(base.rglob("char_*")):
        if not d.is_dir():
            continue
        if reports in d.relative_to(base).parts:
            continue
        n = char_num(d.name)
        if n is None:
            continue
        found.setdefault(n, []).append(d)
    return found


def pick_dir(cfg: dict, dirs: list[Path]) -> Path:
    """同编号多副本时按 source_priority 取最权威的一份。"""
    prio = cfg["paths"].get("source_priority", [""])

    def rank(d: Path) -> int:
        src = source_rel(cfg, d)
        return prio.index(src) if src in prio else len(prio)

    return sorted(dirs, key=rank)[0]


def resolve_char_dir(cfg: dict, arg: str | int, where: str = "material") -> Path:
    """按编号或目录名/路径解析人物目录。where=material|asset。"""
    p = Path(str(arg)).expanduser()
    if p.is_dir():
        return p
    root = material_root(cfg) if where == "material" else asset_root(cfg)
    s = str(arg)
    if s.isdigit():
        hits = [d for n, ds in scan_char_dirs(cfg).items() if n == int(s) for d in ds]
        if where == "asset":
            hits = sorted(root.glob(f"char_{int(s):02d}_*"))
        if hits:
            return pick_dir(cfg, hits)
    hits = sorted(root.glob(f"{s}*"))
    if not hits:
        raise SystemExit(f"❌ 找不到人物目录：{arg}（{where} 根目录：{root}）")
    return pick_dir(cfg, hits) if where == "material" else hits[0]


# ---------------------------------------------------------------- prompts.md 解析
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


def profile_field(profile_text: str, name: str) -> str:
    m = re.search(rf"\*\*{re.escape(name)}\*\*[：:]\s*(.+)", profile_text)
    return m.group(1).strip() if m else ""


@dataclass
class Character:
    dir: Path
    name: str
    num: int | None = None
    posture: str = ""
    ifts: str | None = None
    ifts_source: str = ""
    views: dict[str, str] = field(default_factory=dict)
    has_profile: bool = False
    cjson: dict | None = None          # character.json（新格式）
    legacy: bool = False               # 无 character.json 且 00/01 为旧 Midjourney 语法
    source: str = ""                   # 相对 MATERIAL 的父路径
    needs_manual: bool = False

    @property
    def is_full(self) -> bool:
        return self.posture in ("FW", "FM")


def posture_of(name: str, views: dict[str, str], cjson: dict | None) -> str:
    if cjson and cjson.get("posture"):
        return cjson["posture"]
    m = re.search(r"char_\d+_([BF][MW])", name)
    if m:
        return m.group(1)
    p01 = views.get("01", "")
    if "full-body" in p01 or "full-figure" in p01 or "12.0cm" in p01:
        return "FM"
    return "BM" if p01 else ""


def load_character(cfg: dict, folder: Path) -> Character:
    folder = folder.expanduser()
    if folder.is_file():
        folder = folder.parent
    name = folder.name
    cj_path = folder / "character.json"
    cjson = json.loads(cj_path.read_text(encoding="utf-8")) if cj_path.is_file() else None
    pm = folder / "prompts.md"
    pj = folder / "prompts.json"
    views: dict[str, str] = {}
    ifts = None
    ifts_src = ""
    if pm.is_file():
        views, ifts = parse_prompts_md(pm.read_text(encoding="utf-8"))
        ifts_src = "prompts.md"
    elif pj.is_file():
        data = json.loads(pj.read_text(encoding="utf-8"))
        src = data.get("views", data)
        views = {v: (src[v]["raw_prompt"] if isinstance(src.get(v), dict) else src[v])
                 for v in VIEWS if v in src}
        ifts = data.get("identity_fingerprint_tokens")
        ifts_src = "prompts.json"
    if cjson:
        ifts, ifts_src = cjson.get("ifts", ifts), "character.json"
    profile = folder / "character_profile.md"
    if not ifts:
        ifts, ifts_src = ifts_from_profile(profile), "character_profile.md"
    ifts = ifts.strip().rstrip("。.") if ifts else None
    legacy = cjson is None and ("--ar" in views.get("00", "") or "--ar" in views.get("01", ""))
    return Character(dir=folder, name=name, num=char_num(name),
                     posture=posture_of(name, views, cjson), ifts=ifts, ifts_source=ifts_src,
                     views=views, has_profile=profile.is_file(), cjson=cjson, legacy=legacy,
                     source=source_rel(cfg, folder),
                     needs_manual=ifts is None)


# ---------------------------------------------------------------- 图片尺寸
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
                return (1 + int.from_bytes(data[24:27], "little"),
                        1 + int.from_bytes(data[27:30], "little"))
            if chunk == b"VP8L":
                b = data[21:25]
                return (1 + (((b[1] & 0x3F) << 8) | b[0]),
                        1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6)))
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
    for name, target in (("1:1", 1.0), ("3:4", 0.75), ("4:3", 4 / 3), ("2:3", 2 / 3),
                         ("9:16", 9 / 16), ("16:9", 16 / 9)):
        if abs(r - target) < 0.02:
            return name
    return f"{w}:{h}"


def asset_files(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(f for f in folder.iterdir()
                  if f.is_file() and f.suffix.lower() in IMG_EXTS)


def view_present(files: list[Path], view: str) -> bool:
    """00→任一 0.*；01→任一 1.*；场景→视角NN_*。"""
    for f in files:
        if view == "00" and f.stem == "0":
            return True
        if view == "01" and f.stem == "1":
            return True
        if view not in ("00", "01") and f.name.startswith(f"视角{view}_"):
            return True
    return False
