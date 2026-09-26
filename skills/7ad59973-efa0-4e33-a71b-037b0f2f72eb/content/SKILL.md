---
name: fullcolor-3dprint-character-prompts
description: Use when generating AI-photoreal elder, parent, in-law, or late-spouse character profiles and 11-view (00–10) prompt packs for 3D full-color resin memorial figurines without portrait-copyright risk — Midjourney V8 for views 00/01 (1:1 modeling reference), Gemini/Imagen for views 02–10 (3:4 Xiaohongshu scene images, 07/10 as cover candidates) — with IFTS identity lock, library-wide dedup, scene variation against templated output, and automated validation of prompts.md. Does NOT write Xiaohongshu copy (use xiaohongshu-memorial-3dprint-copywriter).
license: MIT
metadata:
  version: "5.0.0"
  optimization-date: "2026-09-23"
  optimization-changelog: "专业运营版：02–10 改 3:4 并预留封面留白、场景变奏反同质化、禁可读文字与灵堂意象、词数预算校准、validate_prompts.py 直接解析 prompts.md、SKILL.md 渐进式披露（130KB → 入口文件 + references/）"
  domain: 3d-printing-and-ai-visuals
  config-files: "config/CORE_RULES.md（L1/L2 速查）· config/paths.yml（路径与参数，校验器直接读取）"
  validator: "validators/validate_prompts.py（bash 包装脚本保留旧命令）"
  xiaohongshu-compliance-ref: "~/.skillshub/xiaohongshu-memorial-3dprint-copywriter/references/xiaohongshu_ai_rule.md"
  midjourney-reference-doc: "/Users/wuyongjia/obsidian-gitee/technology/🧰 AI工具/midjourney/Midjourney V8.x 核心参数与高级指令全景说明.md"
  prompt-save-root: "/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材"
  image-save-root: "/Users/wuyongjia/3D打印/素材"
  character-generator-mode: "dynamic-formula-engine"
  default-batch-size: 20
  prompts-per-character: 11
  aspect-ratios: "00/01 = 1:1 · 02–10 = 3:4"
  triggers: 3D打印长辈提示词, 3D打印父母提示词, 3D打印公婆提示词, 3D打印老人提示词, 全彩打印模型提示词, AI生成真实长辈, 3D打印无版权人物, 爸爸妈妈手办提示词, 公公婆婆手办提示词, 岳父岳母手办提示词, 老伴手办提示词, 人物画像公式, 动态长辈人物生成, 去重人物画像, 长辈胸像提示词, 长辈全身像提示词, 3D打印多视角提示词, 掌心手办提示词, 纪念手办人物, 场景图提示词, 小红书封面图, 3比4场景图, 人物铸造, IFTS, 提示词校验, 素材库审计, MidjourneyV8核心参数
  related-skills: xiaohongshu-memorial-3dprint-copywriter, photorealistic-character-generator
---

# 3D 全彩打印长辈人物 · 提示词工程技能 (v5.0)

为纪念手办业务生成**无肖像侵权的虚构长辈人物**，产出人物档案与 11 视角提示词：00/01 给 3D 建模用，02–10 给小红书笔记当场景图。

- **负责**：人物铸造（五维画像 + IFTS）、全库去重、11 视角双引擎提示词、落盘、自动校验、出图验收标准。
- **不负责**：小红书文案（交给 `xiaohongshu-memorial-3dprint-copywriter`）。

> 数值与路径在 `config/paths.yml`，规则速查在 `config/CORE_RULES.md`，细节按工作流步骤读 `references/`。

---

## 🔴 L1 红线（任一违反 = Blocker，禁止交付）

1. **零侵权**：人物 100% 由提示词虚构；不用网络真人照片垫图，不出现明星名人；三禁双准（禁动漫/CG、禁非中国人面孔、禁磨皮幼态；准年龄质感、准平民人设）。
2. **先铸造、后出词**：五维画像卡 + IFTS 写入 `character_profile.md` 后才写提示词。
3. **11 视角全量**：00–10 每个视角都有中文说明 + 英文提示词；不抽样、不截断、不用 TODO/省略号。
4. **IFTS 指纹锁**：15–20 词 IFTS 在 00 与 01 中**逐字、连续**出现；景别锁放在 IFTS 之外。
5. **00 → 01 衍生**：01 由 00 经四大置换算子得到；01 的 `--no` 不得含 `doll`、`3d render`、`figurine`、`plastic skin`（会迫使模型生成真人）。
6. **景别锁**：胸像（BW/BM）00/01 含 `Keep the upper body`；全身像（FW/FM）00 含 `full-body` ≥1 次、01 ≥2 次。
7. **双引擎语法隔离**：00/01 为 Midjourney 单段自然语言 + `--ar 1:1 --style raw --s 80/50 --v 8 --no English, …`；02–10 为 Gemini 纯自然语言，不含任何 `--` 参数，以 `Vertical 3:4 composition.` 开头、以 `Avoid: English text, letters, …` 结尾。
8. **零英文、零内部代号**：画面不出现英文字母；提示词不出现 `char_XX`、`BW/BM/FW/FM`、本地路径。
9. **单一职责**：不生成 `小红书文案.md`，不写标题、正文、评论话术。

## 🟡 L2 质量（Major，需修正或说明）

- **词数预算**：00/01 总 50–82 词、正向 ≤ 65（v5 按强制结构校准，见 `prompt-engineering-spec.md` 铁律十一）；
- **画幅与封面**：02–10 为 3:4；07 掌心温存、10 时光重叠追加上 1/3 标题留白句；
- **场景变奏**：每个槽位在机位/实景/道具/光影中至少换两层，道具必含人物专属信物（反同质化，categoryId=279）；
- **不写可读文字**：便签、招牌写 `faded, illegible handwriting` / `blank signboard`，不写带引号的句子；
- **不放灵堂/供桌意象**：不出现神龛、香炉、红烛供桌、黑白证件照相框；
- **人物库**：30% 现代配额（2020–2026 年离世的 40–60 岁中年亲人）；信物、色彩、职业、骨相、IFTS 五重去重；
- **3D 打印力学**：胸像 6.0cm、全身 12.0cm，深色工艺品底座（禁石膏柱），壁厚 ≥1.5mm，信物与身体熔接。

---

## ⚙️ 工作流

```
Step 0  加载      config/CORE_RULES.md + config/paths.yml
Step 1  扫描库    material_base 下所有 char_*：MAX_ID、已占用信物/色彩/职业/IFTS
Step 2  铸造      五维画像卡 + 动态画像公式（默认 20 人，30% 现代配额）
Step 3  IFTS      15–20 词指纹 → character_profile.md + prompts.md 第 0 节
Step 4  00/01     Midjourney 模板 + 00→01 四大置换算子
Step 5  02–10     九大情绪槽位 + 场景变奏 + 3:4 + 封面留白
Step 6  落盘      character_profile.md · prompts.md · prompts.json · 空图片目录
Step 7  校验      validate_prompts.py → BLOCKER = 0 才交付
Step 8  出图(可选) 生图工具画幅参数 + 规范文件名 + 出图验收清单
```

- **Step 1**：新批次编号从 `MAX_ID + 1` 顺延，禁止覆盖已有目录；目录名 `char_{NN}_{BW|BM|FW|FM}_{人物描述}`。
- **Step 5**：先按 `scene-library.md` 定每个槽位的情绪任务，再从 `github-diorama-staging-matrix.md`（实景/道具/光影）与 `nano-banana-hyperrealistic-engine.md`（机位手法）抽取变奏。
- **Step 6**：`prompts.json` 用 `validate_prompts.py <prompts.md> --export-json` 生成，保证与 `prompts.md` 一致。
- **Step 7**：单个人物跑一次；批量生成后跑 `--all`，处理 `SCENE_SIMILAR`（同质化嫌疑）。
- **Step 8**：Gemini/Imagen 在工具参数里设 3:4；按 `scene-library.md` 第 1 节文件名保存（`0.jpg`、`1.jpg`、`视角02_专属老座.jpg` …）；逐张过第 6 节出图验收清单。

---

## 📦 `prompts.md` 输出模板

校验器按下列标题解析，**标题格式请保持不变**（`### 视角 NN:`、IFTS 小节、````text` 代码块）。

````markdown
# {char_dir} 11 视角标准提示词手册

> **角色分类**：胸像 (Bust) · 6.0cm ｜ 全身 (Full-body) · 12.0cm
> **时代节点**：{年代与生计背景}
> **引擎与画幅**：00/01 Midjourney V8 · 1:1 ｜ 02–10 Gemini (Imagen) · 3:4

## 0. 人物唯一性指纹 Token 序列 (IFTS)

```text
{15–20 词 IFTS}
```

## 一、 Midjourney 视角（00 & 01）

### 视角 00: 【基底定妆照】真实生活写实摄影
- **画幅比例**：`1:1`
#### 中文提示词说明
{中文说明}
#### 英文提示词
```text
Candid documentary portrait of a real {IFTS}, Keep the upper body, in {setting}, wearing {clothing}, … --ar 1:1 --style raw --s 80 --v 8 --no English, …
```

### 视角 01: 【模型标准像】0° 正面微缩手办棚拍
- **画幅比例**：`1:1`
#### 中文提示词说明
{中文说明}
#### 英文提示词
```text
Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body, {IFTS}, sculpted {clothing}, mounted on dark beveled pedestal base, … --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, …
```
#### 🔍 00 ➔ 01 微调置换对齐表
| 维度 | 视角 00 | 视角 01 | 算子 |
| --- | --- | --- | --- |

## 二、 Gemini 场景视角（02–10）

### 视角 02: 【专属老座】{场景名}
- **画幅比例**：`3:4`
#### 中文提示词说明
{中文说明}
#### 英文提示词
```text
Vertical 3:4 composition. {场景主体 + 专属信物 + 环境光影}. Shot on {机身镜头}, {胶片质感}. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

…（视角 03–10 同结构；07、10 在 Shot on 前加 `Leave clean negative space in the upper third for a title overlay.`）
````

---

## 🧪 常用命令

```bash
F=~/.skillshub/fullcolor-3dprint-character-prompts
python3 $F/validators/validate_prompts.py "<人物目录或 prompts.md>"       # 单个人物，BLOCKER 时退出码 1
python3 $F/validators/validate_prompts.py --all --report                # 全库审计 → docs/latest-audit-report.md
python3 $F/validators/validate_prompts.py "<prompts.md>" --export-json   # 生成同目录 prompts.json
python3 $F/validators/validate_prompts.py "<目录>" --only ifts,framing   # 只看部分检查
python3 $F/validators/validate_prompts.py --self-test                   # 校验器自测
```

旧命令仍可用（已改为包装脚本）：`validate-all.sh`、`validate-ifts.sh`、`check-fullbody.sh`、`check-completeness.sh`、`batch-audit.sh`、`md-to-json.sh`、`test-validators.sh`。

---

## 🗂️ 文件地图（按需读取）

| 何时读 | 文件 | 内容 |
| :--- | :--- | :--- |
| Step 0 | `config/CORE_RULES.md` | L1/L2 规则速查与校验对照 |
| Step 0 | `config/paths.yml` | 路径、画幅、词数预算、封面候选、相似度阈值 |
| Step 1–3 | `references/character-forging-engine.md` | 三禁双准、五维画像、IFTS、五重去重、动态画像公式、30% 配额 |
| Step 4 | `references/prompt-engineering-spec.md` | MJ V8 参数、00→01 算子与对齐矩阵、结构模板、六步法 + Step 7 |
| Step 5 | `references/scene-library.md` | 11 视角总表、九大情绪槽位、场景变奏、封面候选、母题映射、出图验收 |
| Step 5 | `references/github-diorama-staging-matrix.md` · `references/nano-banana-hyperrealistic-engine.md` | 实景/道具/光影素材库 · 15 种机位与去 AI 味微瑕 |
| 示例 | `references/golden-examples.md` | 三套标杆示例（厨房外婆、客运老爸、校门父亲），已按 v5 修订 |
| 可选 | `references/blender-render-and-img2img.md` | 有 3D 模型文件时的渲染与图生图工作流 |
| 审计 | `docs/latest-audit-report.md` | 最近一次全库审计结果 |

---

## 🤝 与 xiaohongshu 技能协作

- xiaohongshu 技能只读取本技能的 `character_profile.md`、`prompts.md` 与图片；
- 00 写实定妆照是 AI 写实人像，**不用于笔记**；01 作为"效果图"；02–10 为笔记场景图，07/10 为封面候选；
- 素材库人物是 AI 虚构的示例角色：文案侧据此采用手艺人设计手记 / 第二人称视角，不写成"我奶奶"的真实经历；
- 合规依据见 `xiaohongshu-compliance-ref`（AI 标识、导流、虚假营销、丧葬迷信）。

**存量素材**：库中早期人物的提示词早于 v4.1/v5 规则，重出图（尤其换 3:4）前先按本版规则重写对应 `prompts.md` 并跑校验；最新审计结果见 `docs/latest-audit-report.md`。
