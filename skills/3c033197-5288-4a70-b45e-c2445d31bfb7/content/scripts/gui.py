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

    CG.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
    CG.CGEventCreateKeyboardEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint16, ctypes.c_bool]
    CG.CGEventSetFlags.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

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


def cg_key(code: int, flags: int = 0):
    """通过系统底层 CoreGraphics CGEvent 投递键盘事件，绝不触发 System Events 跨应用弹窗"""
    ev_down = CG.CGEventCreateKeyboardEvent(None, code, True)
    ev_up = CG.CGEventCreateKeyboardEvent(None, code, False)
    if flags:
        CG.CGEventSetFlags(ev_down, flags)
        CG.CGEventSetFlags(ev_up, flags)
    CG.CGEventPost(0, ev_down)
    time.sleep(0.06)
    CG.CGEventPost(0, ev_up)


def keystroke_v():
    """Command+V 粘贴 (优先 CGEvent 底层投递，安全降级至 osa)"""
    try:
        # kVK_ANSI_V = 9, kCGEventFlagMaskCommand = 0x00100000
        cg_key(9, 0x00100000)
    except Exception:
        osa('tell application "System Events" to keystroke "v" using command down')


def key(code: int):
    """按键如回车 36 (优先 CGEvent 底层投递，安全降级至 osa)"""
    try:
        cg_key(code)
    except Exception:
        osa(f'tell application "System Events" to key code {code}')


def keystroke_combo(char: str, mods: str = "command down"):
    osa(f'tell application "System Events" to keystroke "{char}" using {{{mods}}}')


# ---------------------------------------------------------------- AX 辅助
def _init_native_ax():
    try:
        app_services = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices")
        core_foundation = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")

        CFStringCreateWithCString = core_foundation.CFStringCreateWithCString
        CFStringCreateWithCString.restype = ctypes.c_void_p
        CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]

        AXUIElementCreateApplication = app_services.AXUIElementCreateApplication
        AXUIElementCreateApplication.restype = ctypes.c_void_p
        AXUIElementCreateApplication.argtypes = [ctypes.c_int]

        AXUIElementCopyAttributeValue = app_services.AXUIElementCopyAttributeValue
        AXUIElementCopyAttributeValue.restype = ctypes.c_int
        AXUIElementCopyAttributeValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]

        CFArrayGetCount = core_foundation.CFArrayGetCount
        CFArrayGetCount.restype = ctypes.c_int
        CFArrayGetCount.argtypes = [ctypes.c_void_p]

        CFArrayGetValueAtIndex = core_foundation.CFArrayGetValueAtIndex
        CFArrayGetValueAtIndex.restype = ctypes.c_void_p
        CFArrayGetValueAtIndex.argtypes = [ctypes.c_void_p, ctypes.c_int]

        CFStringGetCString = core_foundation.CFStringGetCString
        CFStringGetCString.restype = ctypes.c_int
        CFStringGetCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]

        CFRelease = core_foundation.CFRelease
        CFRelease.argtypes = [ctypes.c_void_p]

        class CGPoint(ctypes.Structure):
            _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

        class CGSize(ctypes.Structure):
            _fields_ = [("width", ctypes.c_double), ("height", ctypes.c_double)]

        AXValueGetValue = app_services.AXValueGetValue
        AXValueGetValue.restype = ctypes.c_int
        AXValueGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]

        AXUIElementPerformAction = app_services.AXUIElementPerformAction
        AXUIElementPerformAction.restype = ctypes.c_int
        AXUIElementPerformAction.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

        kAXPress = CFStringCreateWithCString(None, b"AXPress", 0x08000100)

        AXUIElementCopyElementAtPosition = app_services.AXUIElementCopyElementAtPosition
        AXUIElementCopyElementAtPosition.restype = ctypes.c_int
        AXUIElementCopyElementAtPosition.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_void_p)]

        keys = {
            "windows": CFStringCreateWithCString(None, b"AXWindows", 0x08000100),
            "children": CFStringCreateWithCString(None, b"AXChildren", 0x08000100),
            "role": CFStringCreateWithCString(None, b"AXRole", 0x08000100),
            "title": CFStringCreateWithCString(None, b"AXTitle", 0x08000100),
            "desc": CFStringCreateWithCString(None, b"AXDescription", 0x08000100),
            "pos": CFStringCreateWithCString(None, b"AXPosition", 0x08000100),
            "size": CFStringCreateWithCString(None, b"AXSize", 0x08000100),
            "press": kAXPress,
        }

        return {
            "app_services": app_services,
            "core_foundation": core_foundation,
            "AXUIElementCreateApplication": AXUIElementCreateApplication,
            "AXUIElementCopyAttributeValue": AXUIElementCopyAttributeValue,
            "AXUIElementPerformAction": AXUIElementPerformAction,
            "AXUIElementCopyElementAtPosition": AXUIElementCopyElementAtPosition,
            "CFArrayGetCount": CFArrayGetCount,
            "CFArrayGetValueAtIndex": CFArrayGetValueAtIndex,
            "CFStringGetCString": CFStringGetCString,
            "CFRelease": CFRelease,
            "CGPoint": CGPoint,
            "CGSize": CGSize,
            "AXValueGetValue": AXValueGetValue,
            "keys": keys,
        }
    except Exception:
        return None



_NATIVE_AX = _init_native_ax()


def _get_process_pid(proc: str) -> int | None:
    cands = [proc]
    if proc in ("Web App", "Google Gemini"):
        cands = ["Web App.*Google Gemini", "Web App", "Google Gemini"]
    for name in cands:
        try:
            out = subprocess.check_output(["pgrep", "-f", name], text=True).split()
            if out:
                return int(out[0])
        except Exception:
            pass
    try:
        script = f'tell application "System Events" to get unix id of first process whose name contains "{proc}"'
        out = subprocess.check_output(["osascript", "-e", script], text=True).strip()
        return int(out)
    except Exception:
        return None



def _ax_rows_native(proc: str) -> list[dict] | None:
    if not _NATIVE_AX:
        return None
    pid = _get_process_pid(proc)
    if not pid:
        return None

    api = _NATIVE_AX
    keys = api["keys"]
    app = api["AXUIElementCreateApplication"](pid)
    if not app:
        return None

    windows = ctypes.c_void_p()
    err = api["AXUIElementCopyAttributeValue"](app, keys["windows"], ctypes.byref(windows))
    if err != 0 or not windows.value:
        api["CFRelease"](app)
        return None

    w_count = api["CFArrayGetCount"](windows)
    if w_count == 0:
        api["CFRelease"](windows)
        api["CFRelease"](app)
        return None

    best_win = None
    best_area = -1.0
    for i in range(w_count):
        w = api["CFArrayGetValueAtIndex"](windows, i)
        sz_p = ctypes.c_void_p()
        if api["AXUIElementCopyAttributeValue"](w, keys["size"], ctypes.byref(sz_p)) == 0 and sz_p.value:
            sz = api["CGSize"](0, 0)
            api["AXValueGetValue"](sz_p, 2, ctypes.byref(sz))
            api["CFRelease"](sz_p)
            area = sz.width * sz.height
            if area > best_area:
                best_area = area
                best_win = w

    if not best_win:
        best_win = api["CFArrayGetValueAtIndex"](windows, 0)

    rows: list[dict] = []

    def cf_to_str(cf_str):
        if not cf_str:
            return ""
        buf = ctypes.create_string_buffer(2048)
        res = ""
        if api["CFStringGetCString"](cf_str, buf, 2048, 0x08000100):
            res = buf.value.decode("utf-8", errors="ignore")
        api["CFRelease"](cf_str)
        return res

    def walk(el, depth=0):
        if depth > 20:
            return
        role_p = ctypes.c_void_p()
        api["AXUIElementCopyAttributeValue"](el, keys["role"], ctypes.byref(role_p))
        role = cf_to_str(role_p) if role_p.value else ""

        desc_p = ctypes.c_void_p()
        api["AXUIElementCopyAttributeValue"](el, keys["desc"], ctypes.byref(desc_p))
        desc = cf_to_str(desc_p) if desc_p.value else ""
        if not desc:
            title_p = ctypes.c_void_p()
            api["AXUIElementCopyAttributeValue"](el, keys["title"], ctypes.byref(title_p))
            desc = cf_to_str(title_p) if title_p.value else ""

        pos_p = ctypes.c_void_p()
        pt = api["CGPoint"](0, 0)
        if api["AXUIElementCopyAttributeValue"](el, keys["pos"], ctypes.byref(pos_p)) == 0 and pos_p.value:
            api["AXValueGetValue"](pos_p, 1, ctypes.byref(pt))
            api["CFRelease"](pos_p)

        sz_p = ctypes.c_void_p()
        sz = api["CGSize"](0, 0)
        if api["AXUIElementCopyAttributeValue"](el, keys["size"], ctypes.byref(sz_p)) == 0 and sz_p.value:
            api["AXValueGetValue"](sz_p, 2, ctypes.byref(sz))
            api["CFRelease"](sz_p)

        rows.append({"role": role, "desc": desc, "x": pt.x, "y": pt.y, "w": sz.width, "h": sz.height})

        ch_p = ctypes.c_void_p()
        if api["AXUIElementCopyAttributeValue"](el, keys["children"], ctypes.byref(ch_p)) == 0 and ch_p.value:
            n = api["CFArrayGetCount"](ch_p)
            for c_idx in range(n):
                child = api["CFArrayGetValueAtIndex"](ch_p, c_idx)
                walk(child, depth + 1)
            api["CFRelease"](ch_p)

    walk(best_win)
    api["CFRelease"](windows)
    api["CFRelease"](app)
    return rows


def _ax_rows_osa(proc: str) -> list[dict]:
    """兜底降级方案：AppleScript 扫描。"""
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
        out = osa(script, timeout=90)
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


def ax_rows(proc: str) -> list[dict]:
    """扫描目标进程主窗口，返回 [{role,desc,x,y,w,h}]。优先使用原生 AX C API（~0.8s），降级 AppleScript。"""
    try:
        res = _ax_rows_native(proc)
        if res:
            return res
    except Exception:
        pass
    return _ax_rows_osa(proc)


def click_element_at(proc: str, x: float, y: float, hover_s: float = 0.5) -> bool:
    """在屏幕指定坐标 (x, y) 处执行高可靠双通道点击。
    1. 前置安全校验：坐标必须在屏幕正向可见区；
    2. 优先调用系统的 AXUIElementCopyElementAtPosition 获取独立无障碍句柄，触发 AXPress；
    3. 同步执行 CoreGraphics hover_click 作为物理双保险；
    4. 全程零野指针，严格遵循 CoreFoundation 内存管理规范。
    """
    if x < 0 or y < 0:
        print(f"   ⚠️ 拦截到非法点击坐标 ({x:.0f}, {y:.0f})，跳过")
        return False

    pressed = False
    if _NATIVE_AX:
        pid = _get_process_pid(proc)
        if pid:
            api = _NATIVE_AX
            app = api["AXUIElementCreateApplication"](pid)
            if app:
                target = ctypes.c_void_p()
                err = api["AXUIElementCopyElementAtPosition"](app, ctypes.c_float(x), ctypes.c_float(y), ctypes.byref(target))
                if err == 0 and target.value:
                    res = api["AXUIElementPerformAction"](target, api["keys"]["press"])
                    pressed = (res == 0)
                    api["CFRelease"](target)
                api["CFRelease"](app)
    # 辅以物理点击确保 100% 触发（若无障碍未响应或为复杂组件）
    try:
        hover_click(x, y, hover_s=hover_s)
    except Exception as e:
        print(f"   ⚠️ hover_click 异常: {e}")
    return pressed


def click_matched_element(proc: str, pat: str, role: str = "") -> bool:
    """在进程主窗口中查找匹配 pat 的元素，并安全触发双通道点击（优先 y 最大者）。"""
    rows = ax_rows(proc)
    cands = find_elements(rows, pat, (role,) if role else ())
    if not cands:
        return False
    # 取 y 坐标最大的那个（最新出现的元素）
    best = max(cands, key=lambda r: r["y"])
    cx = best["x"] + best["w"] / 2
    cy = best["y"] + best["h"] / 2
    click_element_at(proc, cx, cy)
    return True





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


def clipboard_file(file_path: Path):
    """将文件（视频/音频/附件）作为 POSIX file 放入 macOS 系统剪贴板 («class furl»)。"""
    resolved = file_path.resolve()
    osa(f'set the clipboard to (POSIX file "{resolved}")')


def paste_file(file_path: Path) -> bool:
    """将指定文件放入系统剪贴板，支持在飞书/微信等应用中 ⌘V 粘贴为视频/文件附件。"""
    clipboard_file(file_path)
    return True


def send_file(file_path: Path, xy: tuple[float, float], upload_wait_s: float = 3.5) -> bool:
    """点击会话输入框 -> 剪贴板放入文件 -> ⌘V 粘贴 -> 等待飞书客户端解析/预传视频 -> Return 发送。"""
    paste_file(file_path)
    hover_click(*xy)
    time.sleep(0.6)
    keystroke_v()
    time.sleep(upload_wait_s)
    key(36)
    return True

