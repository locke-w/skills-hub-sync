# Fullcolor 3D Print Character Prompts

> **版本**：v5.0.0（2026-09-23）· 专业运营版
> **定位**：为纪念手办业务生成无肖像侵权的虚构长辈人物，产出人物档案与 11 视角提示词（00/01 建模参考 1:1，02–10 小红书场景图 3:4）。文案由 `xiaohongshu-memorial-3dprint-copywriter` 负责。

---

## 📖 快速导航

| 文件 | 用途 |
| :--- | :--- |
| [SKILL.md](SKILL.md) | 入口：L1/L2 红线、工作流、`prompts.md` 输出模板、文件地图 |
| [config/CORE_RULES.md](config/CORE_RULES.md) | 规则速查（每条对应一个校验代码） |
| [config/paths.yml](config/paths.yml) | 路径、画幅、词数预算、封面候选、相似度阈值（校验器直接读取） |
| [references/](references/) | 人物铸造引擎、提示词工程规范、场景库、黄金示例、场景变奏素材库 |
| [validators/validate_prompts.py](validators/validate_prompts.py) | 直接解析 `prompts.md` 的校验器（单个 / 批量 / 导出 JSON / 自测） |
| [docs/latest-audit-report.md](docs/latest-audit-report.md) | 最近一次全库审计 |

---

## ⚡ 快速开始

```bash
F=~/.skillshub/fullcolor-3dprint-character-prompts

# 校验一个人物（目录、prompts.md 或 prompts.json 都可以）
python3 $F/validators/validate_prompts.py "~/obsidian-gitee/technology/🚀 项目/3D打印/素材/char_45_BW_国营粮站过秤窗口的售粮婆婆"

# 全库审计并更新 docs/latest-audit-report.md
python3 $F/validators/validate_prompts.py --all --report

# 从 prompts.md 生成 prompts.json
python3 $F/validators/validate_prompts.py "<prompts.md>" --export-json

# 校验器自测
python3 $F/validators/validate_prompts.py --self-test
```

旧的 bash 命令（`validate-all.sh`、`batch-audit.sh`、`md-to-json.sh` 等）保留为包装脚本，用法不变。

---

## 🎯 11 视角

| 视角 | 引擎 | 画幅 | 名称 | 用途 |
| :---: | :--- | :---: | :--- | :--- |
| 00 | Midjourney | 1:1 | 基底定妆照 | 建模参考，不发笔记 |
| 01 | Midjourney | 1:1 | 模型标准像 | 建模参考 / 笔记效果图 |
| 02–10 | Gemini / Imagen | 3:4 | 九大情绪槽位场景图 | 小红书笔记配图；07 掌心温存、10 时光重叠为封面候选 |

---

## 📁 目录结构

```
fullcolor-3dprint-character-prompts/
├── SKILL.md                     # 入口文件
├── README.md / CHANGELOG.md
├── config/
│   ├── CORE_RULES.md            # L1/L2 规则速查
│   └── paths.yml                # 路径与参数（单一数据源）
├── references/
│   ├── character-forging-engine.md      # 三禁双准、五维画像、IFTS、去重、画像公式
│   ├── prompt-engineering-spec.md       # MJ V8 参数、00→01 算子、结构模板、六步法
│   ├── scene-library.md                 # 11 视角总表、情绪槽位、场景变奏、封面候选、出图验收
│   ├── golden-examples.md               # 三套标杆示例（v5 已修订）
│   ├── github-diorama-staging-matrix.md # 实景/道具/光影素材库（v5 自 xiaohongshu 迁入）
│   ├── nano-banana-hyperrealistic-engine.md # 15 种机位手法（v5 迁入）
│   └── blender-render-and-img2img.md    # 有 3D 模型时的可选工作流（v5 迁入）
├── validators/
│   ├── validate_prompts.py      # 校验器主体
│   └── *.sh                     # 旧命令的包装脚本
└── docs/
    ├── latest-audit-report.md   # 最新审计（由校验器生成）
    └── fullcolor-*.md           # v4.0 优化过程文档（历史记录）
```

---

## 📊 素材库现状（2026-09-23 审计）

59 个人物全部早于 v4.1/v5 规则，主要问题：

- **59/59** 缺 `--no English` / `Avoid: English text` 负向——抽查 char_31 的视角 06 图片，画面中出现了 "TAXI" 英文字样与模型生成的便签文字；
- **51/59** 胸像缺 `Keep the upper body` 景别锁；
- **43/59** 场景提示词要求渲染带引号的英文句子（如便签上的 `'Dinner is in the pot…'`）；
- **52/59** 场景提示词跨人物高度相似（同一槽位只换道具），属同质化风险；
- **9** 个最早期人物没有 IFTS；**2** 个场景含灵堂/供桌意象（祠堂供桌、黑白证件照相框）。

建议：需要重出 3:4 场景图的人物，先按 v5 规则重写 `prompts.md` 并通过校验，再出图。详见 [docs/latest-audit-report.md](docs/latest-audit-report.md)。

---

## � 关于 docs/ 中的 v4.0 文档

`docs/fullcolor-*.md` 是 v4.0 的优化过程记录，保留作历史参考。其中"Context 消耗 ↓60%"指新增的速查卡，当时 SKILL.md 本身仍有 130KB；"Blocker 缺陷 0"是因为旧校验器只接受 JSON、而库里全部是 `prompts.md`，实际并未校验。v5 已分别通过渐进式披露和直接解析 `prompts.md` 解决。

**维护者**：wuyongjia
