"""检查渲染环境：Python 包、FFmpeg、中文字体。缺什么就打印安装提示。

用法：python check_env.py
"""
from __future__ import annotations

import importlib
import shutil
import sys

ok = True
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def report(passed: bool, name: str, hint: str = "") -> None:
    global ok
    ok &= passed
    print(f"[{'OK' if passed else '缺失'}] {name}" + ("" if passed else f"  ->  {hint}"))


for mod, hint in [
    ("manim", "pip install manim"),
    ("edge_tts", "pip install edge-tts"),
    ("pydub", "pip install pydub（manim 挂载音频需要）"),
]:
    try:
        m = importlib.import_module(mod)
        report(True, f"{mod} {getattr(m, '__version__', '')}".strip())
    except ImportError:
        report(False, mod, hint)

ffmpeg_hint = "Windows: winget install Gyan.FFmpeg | macOS: brew install ffmpeg | Linux: apt install ffmpeg"
report(shutil.which("ffmpeg") is not None, "ffmpeg", ffmpeg_hint)
report(shutil.which("ffprobe") is not None, "ffprobe", ffmpeg_hint)

try:
    import manimpango

    fonts = set(manimpango.list_fonts())
    cjk = [f for f in ["Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC", "WenQuanYi Micro Hei", "SimHei"] if f in fonts]
    report(bool(cjk), f"中文字体 {cjk[:1]}", "安装 Noto Sans SC，或设置环境变量 JCA_FONT=<字体名>")
except ImportError:
    pass

print("\n环境就绪。" if ok else "\n请按提示补齐依赖后重试。（不需要 LaTeX）")
sys.exit(0 if ok else 1)
