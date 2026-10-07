---
name: auto-xhs
description: 纪念手办（3D 全彩打印长辈/父母/公婆/岳父母/老伴手办）小红书全流程技能：① 铸造无肖像侵权的虚构中国长辈人物（五维画像 + IFTS + 全库去重）并生成 11 视角提示词；② 驱动本机 Google Gemini App（最高档模型）按 prompts 批量出图，01 手办图作参考保持一致；③ 调用 pi + DeepSeek flash 写小红书发布包（标题/正文/话题/封面/图序/运营卡）并自动校验回修；④ 扫描素材库全部人物（含归档）做去重与索引；⑤ 把图片、正文、润色后的标题/置顶评论发到飞书联系人（带判重）；支持一条龙 pipeline。触发：发布飞书、发飞书、发布前全流程、一条龙、生成人物、构建人物、手办人物、纪念手办提示词、11 视角、出图、生图、Gemini 出图、小红书文案、纪念手办文案、发布包、评论区运营、私信话术、去重、素材库审计、char_XX、auto-xhs。
license: MIT
metadata:
  version: "1.0.0"
  created: "2026-09-30"
  distilled-from: "fullcolor-3dprint-character-prompts v5.0 + xiaohongshu-memorial-3dprint-copywriter v14.0"
  config-file: "config/studio.toml（路径、画幅、词数、阈值、模型、GUI、业务参数的唯一数据源）"
---

# auto-xhs · 纪念手办小红书全流程

四个阶段，**阶段之间只靠文件交接**，每个阶段都可以单独重跑：

```
阶段 1 人物+提示词   character.json → character_profile.md · prompts.md · prompts.json
阶段 2 出图          prompts.json → Gemini App → 图片目录 0.jpg · 1.jpg · 视角NN_槽位名.jpg + _raw/manifest.json
阶段 3 文案          character_profile.md + 图片清单 → pi(DeepSeek flash) → 小红书文案.md
阶段 4 素材库        全库扫描（含 _已使用/ 归档）→ registry / 去重 / 下一个编号 / 索引 / 审计
阶段 5 发布飞书      图片 + 小红书文案.md → pi 润色标题/置顶 → 飞书联系人（6 条消息，判重）
```

用户只要求其中一段时只做那一段；说"全流程/一条龙/发布前全流程"时用 `pipeline.py`（2→3→5，人物已存在时），每段门禁通过再进下一段。

> 路径（`paths.material` 放档案/提示词/文案，`paths.asset` 放图片）、数值、模型名都在 `config/studio.toml`，本文件不写死。下文 `S=~/.skillshub/auto-xhs`。

---

## 🔴 L1 红线（任一违反 = 禁止交付）

1. **零侵权**：人物 100% 由提示词虚构；不用网络真人照片、不出现明星名人；三禁双准（禁动漫/CG、禁非中国人面孔、禁磨皮幼态；准年龄质感、准平民人设）。
2. **先铸造、后出词**：先写 `character.json`（五维画像 + IFTS），再由脚本渲染提示词；不手写 prompts.md。
3. **11 视角全量**：00–10 每个视角都有中文说明 + 英文提示词，不抽样、不省略。
4. **IFTS 指纹锁**：15–20 词 IFTS 在 00 与 01 中逐字、连续出现；景别锁在 IFTS 之外（胸像 `Keep the upper body`；全身 00 `full-body`≥1、01≥2）。
5. **手办锚定**：每人一句 `figurine_anchor`，在 02–10 每条英文提示词里逐字出现；出图时 02–10 附 01 成图作参考。
6. **手办负向不自残**：01–10 的 `Avoid:` 不得含 `doll`、`3d render`、`figurine`、`plastic skin`、`porcelain doll`、`wax museum`。
7. **零英文、零内部代号**：画面不出现文字字母；英文提示词不出现 `char_XX`、`BW_/BM_/FW_/FM_`、本地路径；便签招牌写 `faded, illegible handwriting` / `blank signboard`。
8. **不放灵堂/供桌意象**：不出现神龛、香炉、供桌、红烛、黑白遗像相框、墓碑等。
9. **文案真实性**：素材库人物是 AI 虚构示例角色，文案只用 A2 手艺人设计手记或 B 第二人称代入；不冒充亲属、不称实拍、必须提示勾选「添加 AI 生成内容标识」、零导流、零软件名、零虚假互动、零绝对化承诺、正文不写病因事故。
10. **不覆盖、不删除**：新人物编号取 `library.py --next-id`；已有图片、文案不覆盖（文案重写只能 `--force`，旧稿自动备份）；归档目录只增不删。

## 🟡 L2 质量（Major，需修正或说明）

- 00/01：`Square 1:1 composition.` 开头，整段 50–110 词，`Avoid:` 收尾；02–10：`Vertical 3:4 composition.` 开头，标准 Avoid 句收尾；07/10 加标题留白句。
- 场景变奏：同批人物同一槽位在机位 / 实景 / 道具 / 光影（`camera/location/prop/light`）中至少换两层；每张场景图至少一件专属信物（07 可用手办身上雕出的信物）。
- 人物库：30% 现代配额（2020–2026 年离开的 40–60 岁中年亲人）；信物、色彩、职业、骨相、IFTS 五重去重（IFTS Jaccard < 0.35）。
- 3D 打印力学：胸像 6.0cm、全身 12.0cm，深色工艺品底座（禁石膏柱），壁厚 ≥1.5mm，信物与身体熔接。
- 文案：正文 180–220 字一文一事、8 条标题 ≥5 种公式且取材正文、话题 8–12、封面大字 6–10 字、图序只用真实存在的图。

---

## 阶段 1 · 人物 + 提示词

1. `python3 $S/scripts/library.py --next-id` 取起始编号；`--registry` 刷新已占用清单（信物/色彩/职业/IFTS）。
2. 按 `references/character/forging-engine.md` 铸造五维画像、IFTS 与配额；按 `scene-library.md` + `staging-matrix.md` + `camera-engine.md` 设计 02–10（批内先排好四层变奏矩阵）。
3. 每人写 `paths.material/<char_dir>/character.json`，字段见 `references/character/character-json.md`，样例 `character.example.json`；目录名 `char_{NN}_{BW|BM|FW|FM}_{人物描述}`。
4. `python3 $S/scripts/library.py --dedup <character.json>`：超阈值（退出码 1）就改人物；把结果写进 `dedup` 字段。
5. `python3 $S/scripts/render_character.py <character.json>`（批量：`--all-batch <目录…>`）→ 生成 profile、prompts.md、prompts.json 与空图片目录。00/01/02–10 的固定句式由脚本套用 `prompt-spec.md` 模板，不要手改 prompts.md，改就改 character.json 再渲染。
6. 门禁：`python3 $S/scripts/validate_prompts.py <目录…>` 逐个 BLOCKER=0、MAJOR=0；整批再跑 `--batch <目录…>`，SCENE_SIMILAR / VARIATION 清零。

## 阶段 2 · Gemini App 出图

⚠️ 会接管鼠标键盘，运行前告诉用户别动电脑；需要已登录的 `Google Gemini.app`（Safari Web App，进程名 `Web App`）。

1. 先 `python3 $S/scripts/gemini_app.py <编号> --dry-run` 生成并检查消息（`/tmp/auto-xhs/<char_dir>/msg_NN.txt`）；首次使用或换机器时跑 `--probe-model`（只新建对话并切到 `model_labels` 里的最高档模型，截图确认，不发消息）。
2. 正式：`python3 $S/scripts/gemini_app.py <编号> [--views 00,01,02-10]`。一个人物一个新对话：首条消息附 prompts.md 全文，之后 00→01→02…10 逐张出图；01 附 0 号图、02–10 附 1 号图；已有的图自动跳过；场景图不是 3:4 时原图进 `_raw/`、居中裁成 3:4。
3. 退出码：2 = 单张超时，3 = 触发额度/上限 —— 停下告诉用户，稍后用同一命令续跑（已完成的会跳过）。
4. 验收：`python3 $S/scripts/inspect_images.py <编号>` 看数量与比例；再按 `checklists/image-qa.md` 人工过一遍（文字/字母、手指、面部一致性、灵堂意象）。不合格的图删掉对应文件后用 `--views NN` 重出（删除前先征得用户同意）。
5. 模型：`studio.toml [gemini_app]` 里配置的最高档；manifest 中 `model_selected=false` 时告诉用户本次未能切到指定模型。
故障排查见 `references/images/gemini-app-runbook.md`。

## 阶段 3 · 小红书文案（pi + DeepSeek flash）

1. 前置：阶段 1 校验通过；图片状态 REUSE（≥2 张），否则只有用户同意时才加 `--allow-no-images`（图序会写"待配图"）。
2. `python3 $S/scripts/write_copy.py <编号> [--pov A2|B] [--type 情感共鸣型|工艺揭秘型|选购指南型]`：脚本把 `prompts/copy_system.md` + `references/copy/` 参考 + 业务参数作为 system prompt，调用 pi（`-p --no-tools --no-session`），自动修正标题字数、跑 `validate_copy.py`，有 BLOCKER/MAJOR 自动回修一次，写入 `paths.material/<char_dir>/小红书文案.md`。
3. 已有文案时脚本拒绝覆盖；用户明确要重写才加 `--force`（旧稿备份为 `小红书文案.bak-时间戳.md`）。
4. 交付前读一遍全文：真实性（无"我奶奶"式叙事）、一文一事、图序文件名真实存在。仍有 MAJOR 时修正或在交付说明里写明原因。
5. 想先看提示词不调模型：`--dry-run`（输出 `/tmp/auto-xhs/<char_dir>/system.md`、`user.md`）。
写作规则细节见 `references/copy/copywriting-craft.md`；运营卡依据 `operations-playbook.md`、`conversion-and-traffic-safety.md`；合规依据 `xiaohongshu_ai_rule.md`。

## 阶段 5 · 发布到飞书

⚠️ 会接管鼠标键盘并真实发送消息；联系人、应用路径在 `studio.toml [feishu]`。

1. 门禁：1 号图 + 视角02–10 齐全；`小红书文案.md` 校验无 BLOCKER（旧格式文案先 `write_copy.py <编号> --force` 重写）。
2. 先 `python3 $S/scripts/feishu_send.py <编号> --dry-run`，检查 `/tmp/auto-xhs/<char_dir>/feishu_0N_*.txt`。
3. 正式：`python3 $S/scripts/feishu_send.py <编号>`，按顺序发 6 条纯文本/图片消息（无 markdown 标题）：
   ① 分割线 `------------------------{char_dir}------------------------` ② 01–10 视角图（10 张一条消息）③ 正文 + 效果图声明 ④ 8 条标题（pi 按 `prompts/feishu_polish.md` 润色成爆文标题，含 1 条童真视角假设句）⑤ 话题标签 ⑥ 置顶评论（润色成情感评论）。润色结果过字数与词库校验，不通过重试一次，仍不通过回退原文。
4. 退出码 4 = 已发送过（判重命中），不要加 `--force` 重发，除非用户明确要求。
5. 不发"小号互动/控评"类内容——那是红线，即使用户的旧流程里有也不发。
故障排查见 `references/publish/feishu-runbook.md`（飞书 AX 拿不到会话内容，核验与判重靠截图 OCR + 本地发送标记）。

## 一条龙

`python3 $S/scripts/pipeline.py <编号> [--skip-images] [--skip-copy] [--skip-feishu] [--force-copy] [--dry-run]`
validate_prompts → inspect_images（缺 0 号图即停，提示用户放入）→ gemini_app 只补缺失视角 → write_copy（无文案或 --force-copy）→ validate_copy → feishu_send；任一步失败即停。收尾打印图片清单、9 张场景图路径与文案路径。

## 阶段 4 · 素材库

| 命令 | 作用 |
| --- | --- |
| `library.py --registry` | 全库登记 → `_reports/registry.json`（`needs_manual` = 旧格式需人工补字段） |
| `library.py --dedup <character.json>` | 新人物与全库比对（IFTS Jaccard、信物/职业/主色 top5） |
| `library.py --next-id` | 全库（含 `_已使用/`）最大编号 + 1 |
| `library.py --dupes` | 同编号多副本及采用哪一份（优先级见 `paths.source_priority`） |
| `library.py --index` | 生成 `_reports/index.md`（不改 README.md） |
| `validate_prompts.py --all [--since N] --report` | 全库提示词审计 → `_reports/prompts-audit.md`（旧格式人物标 LEGACY_FORMAT） |
| `validate_copy.py --all` | 全库文案审计 |

---

## 🗂️ 文件地图（按阶段按需读取，不要一次全读）

| 阶段 | 文件 | 内容 |
| --- | --- | --- |
| 全部 | `config/studio.toml` | 路径、画幅、词数、阈值、模型、GUI、业务参数 |
| 1 | `references/character/forging-engine.md` | 三禁双准、五维画像、IFTS、五重去重、配额门禁、人设路由 |
| 1 | `references/character/character-json.md` · `character.example.json` | 人物数据字段说明与样例 |
| 1 | `references/character/prompt-spec.md` | 00/01/02–10 模板、00→01 置换、词数与负向规则 |
| 1 | `references/character/scene-library.md` | 11 视角总表、九大情绪槽位、封面候选、文件名 |
| 1 | `references/character/staging-matrix.md` · `camera-engine.md` | 实景/道具/光影素材 · 机位手法与去 AI 味 |
| 1 | `references/character/golden-examples.md` | 三套标杆示例 |
| 2 | `references/images/gemini-app-runbook.md` · `checklists/image-qa.md` | GUI 出图故障排查 · 出图验收清单 |
| 3 | `prompts/copy_system.md` | 文案 system prompt（改文案规则先改这里） |
| 3 | `references/copy/*.md` · `checklists/copy-checklist.md` · `config/copy_lexicon.json` | 文案工艺、母题范例、转化合规、运营手册、平台规则 · 清单 · 校验词库 |
| 2 | `prompts/gemini/*.md` | 发给 Gemini App 的中文包装消息模板 |
| 5 | `prompts/feishu_polish.md` · `references/publish/feishu-runbook.md` | 标题/置顶润色提示词 · 飞书发送故障排查 |

自检：`python3 $S/scripts/validate_prompts.py --self-test`、`python3 $S/scripts/validate_copy.py --self-test`（改了 studio.toml、词库或校验器后都要跑）。
