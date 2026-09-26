# Fullcolor 核心规则速查卡 (v5.0)

> **定位**：执行时快速核对的 L1/L2 规则；详细原理见 `references/`，数值见 `config/paths.yml`。
> **校验**：每条规则后标注的 `代码` 即 `validators/validate_prompts.py` 输出的检查代码。

---

## 🔴 L1：核心契约（违反 = BLOCKER，禁止交付）

| # | 规则 | 要点 | 代码 |
| :---: | :--- | :--- | :--- |
| 1 | 11 视角完整 | 00–10 全部有英文提示词；无 TODO、"以此类推"、省略号 | `COMPLETENESS` |
| 2 | IFTS 指纹锁 | 15–20 词 IFTS 在 00 与 01 中逐字、连续出现（景别锁放在 IFTS 之外） | `IFTS_MISSING` `IFTS_MISMATCH` |
| 3 | 景别锁 | 胸像 BW/BM：00/01 含 `Keep the upper body`；全身 FW/FM：00 含 `full-body` ≥1、01 ≥2 | `FRAMING` |
| 4 | 双引擎语法隔离 | 00/01 含 `--ar`、`--v`；02–10 无任何 `--` 参数且有 `Avoid:` 句 | `SYNTAX` |
| 5 | 零英文 | 00/01 的 `--no` 含 `English`；02–10 的 `Avoid:` 含 `English text, letters` | `NO_ENGLISH` |
| 6 | 01 不自残 | 01 的 `--no` 不含 `doll`、`3d render`、`figurine`、`plastic skin` | `SELF_SABOTAGE` |
| 7 | 零内部代号 | 提示词无 `char_XX`、`BW/BM/FW/FM`、本地路径 | `CODE_LEAK` |
| 8 | 零侵权 · 单一职责 | 人物全部虚构、无名人；不生成小红书文案 | （人工） |

**IFTS 标准格式**：`[age]-year-old Chinese [role], [骨相], [年龄微瑕], [发型发色], [眼神], [专属配饰]`
示例：`72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings`

**00 → 01 四大置换算子**：
1. 主体：`Candid documentary portrait of a real` → `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust`（全身：`12.0cm … full-body model`）；
2. 特征：IFTS 原样继承，服装前加 `sculpted`；
3. 环境：生活场景 → `mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus`（全身：`full-body standing on weighted circular base`）；
4. 参数：`--s 80` → `--s 50`；负向从"拦 3D/假人"换成"拦活人与石膏"：`--no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`。

---

## 🟡 L2：质量规范（违反 = MAJOR）

| # | 规则 | 要点 | 代码 |
| :---: | :--- | :--- | :--- |
| 9 | 词数预算 | 00/01 总 50–82 词、正向 ≤65（按空白分词） | `WORD_COUNT` |
| 10 | 画幅 | 00/01 `--ar 1:1`；02–10 开头 `Vertical 3:4 composition.`（工具参数同设 3:4） | `RATIO_MJ` `RATIO_GEMINI` |
| 11 | 封面留白 | 07、10 含 `Leave clean negative space in the upper third for a title overlay.` | `COVER_SPACE`（MINOR） |
| 12 | 场景变奏 | 每槽位在机位/实景/道具/光影中至少换两层；批量审计相似度 < 阈值 | `SCENE_SIMILAR` |
| 13 | 不写可读文字 | 不写 `reading '…'`、`sign that says …`；用 `faded, illegible handwriting` | `TEXT_RENDER` |
| 14 | 无灵堂意象 | 不出现 shrine、altar、incense、ancestral hall、黑白证件照相框 | `FUNERAL` |
| 15 | 无空洞词 | 正向不出现 masterpiece、8k、hyperrealistic、ultra detailed、smooth skin | `EMPTY_WORDS` |
| 16 | 底座 | 01 正向不出现 plaster、stone pedestal、marble column | `PLASTER_POSITIVE` |
| 17 | 人物库 | 30% 现代配额；信物/色彩/职业/骨相/IFTS 五重去重；编号 MAX_ID+1 顺延 | （人工） |

---

## 🧭 双引擎语法对照

| 引擎 | 视角 | 开头 | 结尾 |
| :--- | :--- | :--- | :--- |
| Midjourney V8 | 00, 01 | 主体声明 + IFTS | `--ar 1:1 --style raw --s 80/50 --v 8 --no English, …` |
| Gemini / Imagen | 02–10 | `Vertical 3:4 composition.` | `Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.` |

---

## 🛠️ 校验命令

```bash
F=~/.skillshub/fullcolor-3dprint-character-prompts
python3 $F/validators/validate_prompts.py "<人物目录或 prompts.md>"     # 单个人物
python3 $F/validators/validate_prompts.py --all --report              # 全库审计 → docs/latest-audit-report.md
python3 $F/validators/validate_prompts.py "<目录>" --only ifts         # 只看 IFTS
python3 $F/validators/validate_prompts.py --self-test                 # 自测
```

## 📋 交付检查

- [ ] 已读 `config/paths.yml`，已扫描素材库并确定新编号
- [ ] 五维画像卡与 IFTS 已写入 `character_profile.md`
- [ ] `prompts.md` 11 视角齐全，格式与 SKILL.md 模板一致
- [ ] `validate_prompts.py` 结果 BLOCKER = 0，MAJOR 已修正或说明
- [ ] 批量生成后跑过 `--all`，`SCENE_SIMILAR` 已处理
- [ ] 出图后逐张过 `references/scene-library.md` 出图验收清单

## 💡 口诀

**先铸造后出词** · **IFTS 一字不改** · **胸像留上半身，全身写 full-body** · **MJ 挂 English，Gemini 避 English text** · **场景 3:4，封面留白** · **不写字、不设供桌** · **一人一物，场景换两层**

---

**版本**：v5.0 · 2026-09-23
