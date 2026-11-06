"""带中文配音与字幕的 Manim 场景基类。

用法（在 lesson.py 中）：

    from narrated_scene import *

    class S01Intro(NarratedScene):
        SECTION_ID = "s01"          # 对应 storyboard.json 中的 section id

        def construct(self):
            title = self.title("HashMap.put 做了什么")
            self.say(Write(title))  # 播放第 1 句旁白，同时执行动画
            self.say()              # 第 2 句旁白，只停留不加动画

约定：
- 运行目录必须是课程目录（build.py 会自动切换），其中含 audio/durations.json。
- 每调用一次 say() 消耗 storyboard 中本节的下一句旁白。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import manimpango
from manim import *  # noqa: F401,F403  让 lesson.py 只需 import 本模块

# ---------------------------------------------------------------------------
# 字体：按平台挑选第一个可用的中文字体，可用环境变量 JCA_FONT 覆盖
# ---------------------------------------------------------------------------
_FONT_CANDIDATES = [
    "Microsoft YaHei",
    "PingFang SC",
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "Source Han Sans SC",
    "WenQuanYi Micro Hei",
    "SimHei",
]


def _pick_font() -> str:
    env = os.environ.get("JCA_FONT")
    if env:
        return env
    available = set(manimpango.list_fonts())
    for name in _FONT_CANDIDATES:
        if name in available:
            return name
    return "sans-serif"


CN_FONT = _pick_font()

# ---------------------------------------------------------------------------
# 布局分区（Manim 默认画面约 14.2 x 8 单位，原点在中心）
#   标题区: y > 2.9    内容区: -2.6 < y < 2.9    字幕区: y < -2.6
# ---------------------------------------------------------------------------
CONTENT_TOP = 2.9
CONTENT_BOTTOM = -2.6
LEFT_PANEL = LEFT * 3.4      # 左半区中心，常放代码
RIGHT_PANEL = RIGHT * 3.4    # 右半区中心，常放数据结构/内存图
PANEL_WIDTH = 6.4            # 每个半区可用宽度

LINE_PAD = 0.3               # 每句旁白结束后的停顿（秒）


def cn(text: str, size: int = 28, color=WHITE, **kwargs) -> Text:
    """中英混排文本快捷构造，统一使用含完整中文字形的字体。"""
    return Text(text, font=CN_FONT, font_size=size, color=color, **kwargs)


def mono(text: str, size: int = 22, color=WHITE, **kwargs) -> Text:
    """代码/标识符文本：纯 ASCII 用 Consolas 等宽字体，含中文或特殊符号自动回退到 CN_FONT 防止豆腐块。"""
    font = "Consolas" if all(ord(c) < 128 for c in text) else CN_FONT
    return Text(text, font=font, font_size=size, color=color, **kwargs)


def fit(mob: Mobject, width: float = PANEL_WIDTH, height: float = CONTENT_TOP - CONTENT_BOTTOM - 0.2) -> Mobject:
    """把对象等比缩小到给定宽高以内（不会放大）。"""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    if mob.height > height:
        mob.scale_to_fit_height(height)
    return mob


def java_code(src: str, font_size: int = 20, width: float = PANEL_WIDTH) -> Code:
    """生成 Java 代码块，并适配到半区宽度。逐行对象：code.code_lines[i]（0 起）。"""
    cleaned = src.strip("\n")
    font = "Consolas" if all(ord(c) < 128 for c in cleaned) else CN_FONT
    code = Code(
        code_string=cleaned,
        language="java",
        formatter_style="monokai",
        background="window",
        paragraph_config={"font": font, "font_size": font_size},
    )
    return fit(code, width=width)


def line_box(code: Code, start: int, stop: int | None = None, color=YELLOW) -> SurroundingRectangle:
    """框出代码第 start 行或第 start..stop 行（含两端，0 起），用于高亮当前执行行。"""
    target = code.code_lines[start] if stop is None else VGroup(*code.code_lines[start : stop + 1])
    return SurroundingRectangle(target, color=color, buff=0.06, stroke_width=3)


lines_box = line_box


class NarratedScene(Scene):
    """每句旁白 = 一段音频 + 一条字幕 + 一组可选动画，三者自动对齐时长。"""

    SECTION_ID: str = ""

    def setup(self):
        durations_file = Path.cwd() / "audio" / "durations.json"
        if not durations_file.exists():
            raise FileNotFoundError(
                f"找不到 {durations_file}，请先运行 tts.py 生成配音，并在课程目录下渲染。"
            )
        data = json.loads(durations_file.read_text(encoding="utf-8"))
        if self.SECTION_ID not in data:
            raise KeyError(f"durations.json 中没有 section '{self.SECTION_ID}'，检查 SECTION_ID。")
        self._lines = data[self.SECTION_ID]
        self._idx = 0
        self._subtitle: Mobject | None = None

    # ---- 布局辅助 ----------------------------------------------------------
    def title(self, text: str, size: int = 36) -> Text:
        """左上角章节标题（只创建，不添加到画面）。"""
        return cn(text, size=size, weight=BOLD).to_corner(UL, buff=0.4)

    def _make_subtitle(self, text: str) -> Mobject:
        label = cn(text, size=24)
        if label.width > 12.5:
            label.scale_to_fit_width(12.5)
        bg = BackgroundRectangle(label, color=BLACK, fill_opacity=0.65, buff=0.12)
        return VGroup(bg, label).to_edge(DOWN, buff=0.25)

    # ---- 核心：旁白驱动 ----------------------------------------------------
    @property
    def remaining_lines(self) -> int:
        return len(self._lines) - self._idx

    def next_duration(self) -> float:
        """下一句旁白的时长（含停顿），便于自定义多段动画的 run_time。"""
        return self._lines[self._idx]["duration"] + LINE_PAD

    def say(self, *animations: Animation, run_time: float | None = None) -> None:
        """播放下一句旁白，同时执行 animations，并等到这句话说完。

        run_time 默认取 min(1.5 秒, 旁白时长)；动画放完后剩余时间静止停留。
        """
        if self._idx >= len(self._lines):
            raise IndexError(
                f"section '{self.SECTION_ID}' 只有 {len(self._lines)} 句旁白，say() 调用次数过多。"
            )
        line = self._lines[self._idx]
        self._idx += 1
        total = line["duration"] + LINE_PAD

        self.add_sound(line["file"])
        new_sub = self._make_subtitle(line["text"])
        if self._subtitle is not None:
            self.remove(self._subtitle)
        self.add(new_sub)
        self._subtitle = new_sub

        if animations:
            rt = min(run_time or 1.5, total)
            self.play(*animations, run_time=rt)
            if total - rt > 0.01:
                self.wait(total - rt)
        else:
            self.wait(total)

    def bring_subtitle_front(self) -> None:
        """新加的对象可能盖住字幕时调用。"""
        if self._subtitle is not None:
            self.bring_to_front(self._subtitle)

    def tear_down(self):
        if self._idx < len(self._lines):
            print(
                f"[警告] section '{self.SECTION_ID}' 还有 {len(self._lines) - self._idx} 句旁白没有 say()，"
                "这些配音不会出现在视频里。"
            )
        super().tear_down()
