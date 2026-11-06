# Manim（Community v0.19+）编写要点与常见报错

本技能以 Manim Community **0.19 及以上**为准（已在 0.22.1 验证）。网上很多示例是旧版或 3b1b 版 `manimlib`，API 不兼容，照抄会报错。

## 目录
1. lesson.py 骨架
2. 文本与代码
3. 布局（避免重叠和出界）
4. 常用动画
5. 常见报错速查

---

## 1. lesson.py 骨架

```python
from narrated_scene import *   # 已包含 from manim import *

SRC = """
public int sum(int[] nums) {
    int total = 0;
    for (int n : nums) {
        total += n;
    }
    return total;
}
"""

class S01Intro(NarratedScene):
    SECTION_ID = "s01"

    def construct(self):
        title = self.title("sum 方法：累加数组")
        code = java_code(SRC).move_to(LEFT_PANEL)
        self.say(Write(title))
        self.say(FadeIn(code, shift=UP * 0.3))
        box = line_box(code, 1)
        self.say(Create(box))
```

- 每个 section 一个 `NarratedScene` 子类，类名与 storyboard 中 `scene` 一致，`SECTION_ID` 与 `id` 一致。
- `say()` 的次数必须等于该节 `lines` 的句数（多了会报 IndexError，少了会打印警告）。
- 一句旁白里要做多步动画：先 `d = self.next_duration()`，再自己 `self.play(...)` 多次——但这样就不会自动配音。更简单的做法是把旁白拆成更短的两句。

## 2. 文本与代码

| 需求 | 写法 | 说明 |
| :--- | :--- | :--- |
| 中文/中英混排 | `cn("文字", size=28)` | 封装了 `Text(font=CN_FONT)`，不要用 `Tex/MathTex`（需要 LaTeX） |
| 英文/标识符 | `mono("hashCode()", size=22)` | 纯 ASCII 用 Consolas，含中文或符号（`→ ✓ ✗`）自动回退到 `CN_FONT` 防豆腐块；**不要手写 `Text(..., font="Consolas")`** |
| 公式 | `cn("O(n log n)")` 或 `mono(...)` | 不依赖 LaTeX；确需复杂公式才考虑装 MiKTeX/TeX Live |
| Java 代码块 | `java_code(src, font_size=20)` | 0.19+ 参数是 `code_string=`，旧版 `code=` 已删除 |
| 取第 i 行 / 高亮行 | `line_box(code, 2)` 或 `line_box(code, 2, 5)` | 0 起，支持单行或起止行范围（含两端） |
| 部分文字上色 | `cn("key 的 hash 值", t2c={"hash": YELLOW})` | |

## 3. 布局

画面约 14.2 × 8 单位，原点在中心。`narrated_scene` 已划分：

```
y >  2.9   标题区（self.title 放左上角）
-2.6 ~ 2.9 内容区：LEFT_PANEL(x≈-3.4) 放代码，RIGHT_PANEL(x≈3.4) 放状态
y < -2.6   字幕区（say() 自动管理，别放东西）
```

规则（Code2Video 的"视觉锚点"思想：用确定的锚点定位，不要凭感觉写坐标）：
- 优先用相对定位：`next_to(obj, DOWN, buff=0.3)`、`arrange(DOWN, buff=0.25, aligned_edge=LEFT)`、`to_edge`、`move_to(RIGHT_PANEL)`。
- 新建的大对象先 `fit(mob)` 缩到半区以内再定位。
- 一屏同时出现的元素控制在 ~6 组以内；换主题时先 `FadeOut(*self.mobjects)` 清场（注意这会连字幕一起淡出，下一次 say() 会重建字幕，没问题）。
- 小于 18 号的字在 480p 预览中几乎看不清，正式视频也不建议。

## 4. 常用动画

```python
Write(text) / FadeIn(m, shift=UP*0.3) / FadeOut(m) / Create(shape)
Transform(a, b)            # a 变成 b 的形状，之后继续操作 a
ReplacementTransform(a, b) # a 被 b 替换，之后操作 b
m.animate.move_to(p).set_color(RED)   # 链式属性动画
Indicate(m) / Circumscribe(m) / Flash(point)   # 强调
LaggedStart(*[FadeIn(x) for x in items], lag_ratio=0.2)
```

移动高亮框到新行：`Transform(box, line_box(code, 4))`。

## 5. 常见报错速查

| 报错 | 原因 | 修复 |
| :--- | :--- | :--- |
| `TypeError: Code.__init__() got an unexpected keyword argument 'code'` | 旧版 API | 用 `java_code()` 或 `code_string=` |
| `AttributeError: 'Code' object has no attribute 'code'` | 旧版属性 | 用 `code.code_lines` |
| `latex` / `dvisvgm` not found | 用了 `Tex/MathTex` | 换成 `cn()` / `Text` |
| 中文显示为方块 | 字体缺失 | 运行 `check_env.py`，或设置 `JCA_FONT` |
| `IndexError: ... say() 调用次数过多` | say 次数 > 旁白句数 | 对齐 storyboard 或删多余 say |
| `FileNotFoundError: ... durations.json` | 未配音或不在课程目录运行 | 先跑 `tts.py`，用 `build.py` 渲染 |
| `ValueError: ... run_time ... 0` | 传了 0 时长 | 检查自定义 run_time |
| `KeyError: 'xxx'` 颜色 | 用了不存在的颜色名 | 用 `BLUE/GREEN/YELLOW/RED/ORANGE/PURPLE/TEAL/GRAY` 或十六进制 `"#58C4DD"` |
