#!/usr/bin/env python3
"""auto-xhs GUI 自动化共享工具：osascript / CGEvent 点击 / 剪贴板 / AX 树扫描。

gemini_app.py 与 feishu_send.py 共用，禁止两边各写一份。
"""
from __future__ import annotations

import ctypes
import re
import subprocess
import time
from pathlib import Path


# ---------------------------------------------------------------- osascript / CGEvent 基础
def osa(script: str, timeout: int = 90) -> str:
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"osascript 失败: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def _cg():
    CG = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")

    class CGPoint(ctypes.Structure):
        _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

    CG.CGEventCreateMouseEvent.restype = ctypes.c_void_p
    CG.CGEventCreateMouseEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint32, CGPoint, ctypes.c_uint32]
    CG.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
    return CG, CGPoint


CG, CGPoint = _cg()


def _post(ev_type: int, x: float, y: float):
    p = CGPoint(x, y)
    ev = CG.CGEventCreateMouseEvent(None, ev_type, p, 0)
    CG.CGEventPost(0, ev)  # kCGHIDEventTap


def hover_click(x: float, y: float, hover_s: float = 1.2):
    _post(5, x, y)            # MouseMoved
    time.sleep(hover_s)
    _post(1, x, y)            # LeftMouseDown
    time.sleep(0.08)
    _post(2, x, y)            # LeftMouseUp


def keystroke_v():
    osa('tell application "System Events" to keystroke "v" using command down')


def key(code: int):
    osa(f'tell application "System Events" to key code {code}')


def keystroke_combo(char: str, mods: str = "command down"):
    osa(f'tell application "System Events" to keystroke "{char}" using {{{mods}}}')


# ---------------------------------------------------------------- AX 辅助
def ax_rows(proc: str) -> list[dict]:
    """整树扫描目标进程主窗口（取面积最大的窗口），返回 [{role,desc,x,y,w,h}]。"""
    script = f'''
tell application "System Events" to tell process "{proc}"
  set out to ""
  set win to missing value
  set best to 0
  repeat with w in windows
    try
      set s to size of w
      set a to (item 1 of s) * (item 2 of s)
      if a > best then
        set best to a
        set win to w
      end if
    end try
  end repeat
  if win is missing value then return ""
  set els to entire contents of win
  repeat with e in els
    try
      set r to role of e
      set d to ""
      try
        set d to description of e
      end try
      if d is "" then
        try
          set d to title of e
        end try
      end if
      set p to position of e
      set s to size of e
      set out to out & r & "|" & d & "|" & (item 1 of p) & "|" & (item 2 of p) & "|" & (item 1 of s) & "|" & (item 2 of s) & "\\n"
    end try
  end repeat
  return out
end tell'''
    rows = []
    try:
        out = osa(script, timeout=240)
    except (subprocess.TimeoutExpired, RuntimeError):
        return rows
    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) >= 6:
            try:
                rows.append({"role": parts[0], "desc": "|".join(parts[1:-4]),
                             "x": float(parts[-4]), "y": float(parts[-3]),
                             "w": float(parts[-2]), "h": float(parts[-1])})
            except ValueError:
                pass
    return rows


def frontmost(proc: str):
    osa(f'tell application "System Events" to set frontmost of process "{proc}" to true')
    time.sleep(0.5)


def window_pos(proc: str) -> tuple[float, float]:
    out = osa(f'tell application "System Events" to tell process "{proc}" to get position of window 1')
    a, b = out.split(",")
    return float(a), float(b)


def find_elements(rows: list[dict], pat: str, roles: tuple = ()) -> list[dict]:
    rx = re.compile(pat, re.I)
    return [r for r in rows if rx.search(r["desc"]) and (not roles or r["role"] in roles)]


def page_text_has(rows: list[dict], phrases: list[str]) -> str | None:
    text = " ".join(r["desc"] for r in rows if r["role"] in ("AXStaticText", "AXHeading"))
    for ph in phrases:
        if ph.lower() in text.lower():
            return ph
    return None


def page_texts(rows: list[dict]) -> list[str]:
    return [r["desc"] for r in rows if r["role"] in ("AXStaticText", "AXHeading")]


# ---------------------------------------------------------------- 剪贴板
def clipboard_text(s: str):
    subprocess.run(["pbcopy"], input=s.encode("utf-8"), check=True)


def clipboard_image(png: Path):
    osa(f'set the clipboard to (read (POSIX file "{png}") as «class PNGf»)')


def paste_image(path: Path, tmp: Path = Path("/tmp/auto-xhs/_attach.png")) -> bool:
    """jpg 先 sips 转 png，再按 PNGf 放剪贴板 ⌘V（配方）。"""
    tmp.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["sips", "-s", "format", "png", str(path), "--out", str(tmp)],
                   capture_output=True, check=True)
    clipboard_image(tmp)
    return True


def send_clipboard_text(text: str, input_xy: tuple[float, float] | None = None,
                        proc: str | None = None):
    """pbcopy → 点输入框 → ⌘V → Return。"""
    clipboard_text(text)
    if input_xy:
        hover_click(*input_xy)
    time.sleep(0.5)
    keystroke_v()
    time.sleep(0.5)
    key(36)
