---
name: java-code-animator
description: 把 Java 方法/类的执行原理做成带中文配音和字幕的讲解动画视频（Manim 渲染，3Blue1Brown 风格），借鉴 Code2Video 的 Planner→Coder→Critic 三角色方法论，由当前智能体自己写分镜和 Manim 代码并在本地渲染，无需外部 API Key。只要用户想"用动画/视频讲解""可视化演示""画出来讲给我听"某段 Java 代码、某个方法的原理、JDK 源码（如 HashMap.put、ArrayList 扩容、ConcurrentHashMap、AQS、线程池、Stream）、算法实现或 Spring 框架方法的执行流程，就使用本技能，即使用户没有明确说"Manim"或"视频"。
---

# Java 代码原理动画讲解

把一段 Java 代码变成一支 2~6 分钟的讲解视频：左边是代码、黄框跟着"执行到哪一行"，右边是变量/数据结构/内存/线程的状态变化，配中文旁白和字幕。

方法论来自 [Code2Video](https://github.com/showlab/Code2Video)（NUS Show Lab）：**用可执行的 Manim 代码而不是像素生成视频**，由三个角色协作——Planner 写分镜，Coder 写代码并按报错局部修复，Critic 看渲染画面修布局。这里三个角色都由你来扮演，不调用 Code2Video 仓库，也不需要任何 API Key。

`SKILL_DIR` 指本文件所在目录，脚本在 `SKILL_DIR/scripts/`。

## 工作流

```
0 环境自检 → 1 读懂代码 → 2 Planner 写分镜 → 3 配音 → 4 Coder 写 lesson.py
→ 5 渲染自愈 → 6 Critic 看帧修布局 → 7 出成片并交付
```

### 0. 环境自检

```bash
python SKILL_DIR/scripts/check_env.py
```

需要 Python 3.10+、`manim`、`edge-tts`、FFmpeg、一款中文字体。**不需要 LaTeX、GPU 或 API Key。** 缺什么就按提示安装（pip 包可以直接装；系统软件如 FFmpeg 先告诉用户再装）。edge-tts 配音需要联网。

### 1. 读懂代码

视频质量取决于你对代码的理解，而不是动画多花哨。先把代码真正读透：

- 读方法本体，再读它直接调用的关键方法（JDK 源码可用本机 `src.zip` 或已知的源码知识，注明 JDK 版本，如 8 和 17 的 HashMap 有差异）。
- 回答四个问题：这个方法**解决什么问题**？**核心思路**是什么？**关键步骤**有哪几步？有哪些**边界情况/坑**？
- **选一组具体输入**（例如 `put("apple", 1)` 时 table 长度 16），后面整支视频都用它来"跑一遍"。具体数据比抽象描述好懂得多。
- 代码很长（>40 行）时，只挑主干路径讲，其余在视频里明确说"本期不展开"。

如果用户没给出代码而只说了方法名，先确认是哪个类、哪个版本。

### 2. Planner：写分镜 storyboard.json

在课程目录写 `storyboard.json`。课程目录默认放在当前工作区的 `java-animations/<类名_方法名>/` 下（用户指定了就用用户的）。

```json
{
  "title": "HashMap.put 原理",
  "voice": "zh-CN-YunxiNeural",
  "rate": "+0%",
  "sample_input": "map.put(\"apple\", 1)，table 长度 16",
  "sections": [
    {
      "id": "s01",
      "scene": "S01Intro",
      "title": "put 要解决什么问题",
      "lines": ["HashMap 怎样做到平均 O(1) 存取？", "我们用 put apple 这一次调用，把源码走一遍。"],
      "visual": "标题淡入；左侧淡入 putVal 精简源码；右侧画 16 个空桶"
    }
  ]
}
```

分镜原则：
- **3~6 节**，常见结构：问题与签名 → 核心数据结构 → 逐步执行追踪（可占 2~3 节）→ 边界情况与复杂度 → 一句话总结。
- 每节 **2~6 句**旁白；每句是一个口语化短句（≤ 35 字，字幕一行放得下），一句对应一个画面动作。
- 旁白要像老师说话，解释"为什么"，不要逐字念代码。英文标识符可以保留（如 hashCode），但不要念符号（不要说"左括号"）。
- `visual` 写清这一句要看到什么，下一步写代码时逐句对照。

可选：用户想要的话，把分镜给他过目再继续；默认直接继续。

### 3. 配音

```bash
python SKILL_DIR/scripts/tts.py <课程目录>/storyboard.json
```

为每句旁白生成 mp3 并写入 `audio/durations.json`（时长决定动画节奏）。改了旁白重跑即可，没改的句子会复用缓存。常用音色：`zh-CN-YunxiNeural`（男，默认）、`zh-CN-XiaoxiaoNeural`（女）、`zh-CN-YunjianNeural`（男，沉稳）。

如果报 `403, message='Invalid response status'`：这是微软更新了校验，旧版 edge-tts 失效，执行 `pip install -U edge-tts` 后重试即可（已验证 7.3.1 可用）。

### 4. Coder：写 lesson.py

先读两份参考资料：
- `references/manim-guide.md`：Manim 0.19+ 写法、布局分区、常见报错。**必读**，网上旧示例的 API 很多已失效。
- `references/java-visual-patterns.md`：循环/递归/HashMap/内存/并发/Stream 等该怎么画。按需读对应小节。

在课程目录写 `lesson.py`，开头 `from narrated_scene import *`。每个 section 一个 `NarratedScene` 子类：

```python
class S03Trace(NarratedScene):
    SECTION_ID = "s03"

    def construct(self):
        code = java_code(SRC).move_to(LEFT_PANEL)
        box = line_box(code, 2)
        self.add(code)
        self.say(Create(box))                                  # 第 1 句
        self.say(Transform(box, line_box(code, 3)), FadeIn(node, shift=LEFT))  # 第 2 句
        self.say()                                             # 第 3 句：停留讲解
```

`self.say(*动画)` = 播放下一句配音 + 显示字幕 + 执行动画 + 等这句说完。所以**只需按旁白逐句写 say()**，音画自动同步，say 的次数要等于这一节的句数。`narrated_scene.py` 还提供了 `cn()`（中英文本）、`mono()`（代码标识符，含非 ASCII 自动回退中文字体防豆腐块）、`java_code()`、`line_box(code, start, stop=None)`、`fit()`、`self.title()` 和 `LEFT_PANEL/RIGHT_PANEL` 布局常量。

### 5. 渲染与自愈（Code2Video 的 ScopeRefine 思路）

先低清快速渲染，逐节排错：

```bash
python SKILL_DIR/scripts/build.py <课程目录> --quality l --frames
```

某节失败时，脚本会打印该节报错末尾 40 行。修复方式：
- 看 traceback 定位到 `lesson.py` 的具体行，**只改出错的那几行**，不要整节重写——重写会引入新错误、丢掉已经调好的部分。
- 修完用 `--scenes S03Trace` 只重渲这一节。
- 同一节连续 3 次修不好，就简化这一处的视觉设计（例如换一种更简单的画法），而不是继续硬修。

### 6. Critic：看帧修布局

`--frames` 会在每句旁白结束前截一帧到 `<课程目录>/frames/<场景>_<序号>.png`。**用读取图片的工具逐张查看**（帧多时至少看每节的首帧、末帧和变化最大的帧），按清单检查：

- [ ] 元素重叠、文字压在线条上
- [ ] 内容超出画面边缘，或侵入底部字幕区
- [ ] 字太小看不清（代码字号 < 18）
- [ ] 黄框标的行和这句旁白讲的不是同一行
- [ ] 画面太空或太挤（一屏超过 ~6 组元素）
- [ ] 画面内容和旁白对不上

发现问题就改 lesson.py：用 `next_to / arrange / move_to(锚点)` 这类相对定位替换手写坐标，用 `fit()` 缩小过大的对象。改完重渲受影响的节、重新看帧。通常 1~2 轮即可，不要无限打磨。

### 7. 出成片并交付

```bash
python SKILL_DIR/scripts/build.py <课程目录> --quality m
```

默认 720p（渲染快）；用户要高清就用 `--quality h`（1080p60）。成片在 `<课程目录>/<title>.mp4`。

交付时告诉用户：
1. 成片路径（可点击链接）和时长；
2. 3~5 条要点式的内容提纲，方便对照观看；
3. 如何微调：改 `storyboard.json` 的旁白后重跑第 3、7 步；改画面就改 `lesson.py` 后重跑第 7 步。

课程目录里的 `media/`、`frames/`、`audio/` 是中间产物，可以保留以便后续修改。

## 目录结构

```
java-code-animator/
├── SKILL.md
├── scripts/
│   ├── check_env.py       # 环境自检
│   ├── tts.py             # storyboard → 中文配音 + durations.json
│   ├── narrated_scene.py  # NarratedScene 基类：say() 音画字幕同步 + 布局辅助
│   └── build.py           # 渲染 / 抽审查帧 / 合并成片
└── references/
    ├── manim-guide.md         # Manim 0.19+ 写法与报错速查
    └── java-visual-patterns.md # Java 概念 → 可视化画法
```
