---
name: xiaohongshu-memorial-3dprint-copywriter
description: 小红书纪念手办（3D 打印长辈/父母/公婆/岳父母/老伴手办）专业运营技能。基于 fullcolor 人物档案与图片资产，产出可直接发布的标题、正文、话题、封面大字与图序，以及置顶评论、评论回复库、负面评论应对、站内私信 SOP、发布计划与复盘指标。内置真实性红线（默认手艺人设计手记/第二人称视角，禁止冒充 AI 虚构人物的亲属讲"真实经历"）、《人工智能生成合成内容标识办法》AI 标识义务、小红书导流与虚假营销规则，并用脚本自动校验。触发：小红书文案、纪念手办文案、3D打印长辈/父母/公婆文案、怀念亲人、老照片立体化、手办种草、小红书标题、评论区运营、私信话术、发布计划、笔记复盘、char_XX。不负责生图提示词（交给 fullcolor-3dprint-character-prompts）。
license: MIT
metadata:
  version: "14.0.0"
  optimization-date: "2026-09-23"
  optimization-changelog: "专业运营版：真实性视角体系、Part A 发布内容 + Part B 运营执行卡、合规转化 SOP 重写（去小号/去导流暗号）、运营手册（内容矩阵/封面图序/节点日历/复盘）、validate_copy.py 自动校验、SKILL.md 渐进式披露"
  domain: xiaohongshu-content-operations
  config-file: "config/constants.md（数值、路径、业务参数、校验词库的单一数据源）"
  checklist-file: "checklists/unified-checklist.md（48 项，其中 26 项自动）"
  validators: "scripts/validate_copy.py · scripts/inspect_images.py · scripts/validate-config.sh"
  compliance-specification: "references/xiaohongshu_ai_rule.md（v2.0，2026-09-23 核验）"
  default-narrative-pov: "A2 手艺人设计手记 / B 第二人称代入"
  image-save-root: "/Users/wuyongjia/vibeCoding/3D打印/3dprint-xhs-思念/素材"
  copy-save-root: "/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材"
  triggers: 小红书文案, 纪念手办文案, 3D打印长辈文案, 3D打印父母文案, 公公婆婆手办文案, 岳父岳母文案, 老伴手办文案, 怀念父亲, 怀念母亲, 怀念外婆, 老照片立体化, 掌心手办, 手办种草, 小红书标题, 封面文案, 评论区运营, 置顶评论, 私信话术, 发布计划, 笔记复盘, 小红书运营, char_XX
  related-skills: fullcolor-3dprint-character-prompts, photorealistic-character-generator, doc-coauthoring
---

# 小红书纪念手办 · 专业运营文案技能 (v14.0)

把 fullcolor 技能产出的**人物档案与图片**，变成一篇**可直接发布**的小红书笔记，外加一张**可执行、可复盘**的运营卡。

- **负责**：标题、正文、话题、封面大字与图序、发布设置；置顶评论、回复库、负面应对、私信 SOP、发布计划、复盘指标。
- **不负责**：生图提示词（fullcolor 技能）；"我奶奶/我爸"式虚构亲历；小号控评与导流话术。

> 所有数值、路径、业务参数（价格、周期、流程）与校验词库都在 `config/constants.md`，本文件不写死。

---

## 🔴 L1 红线（任一违反 = 禁止交付）

1. **真实性**：素材库人物是 AI 虚构的示例角色。默认视角 **A2 手艺人设计手记** 或 **B 第二人称代入**；第一人称亲属叙事只用于 **C 客户书面授权故事** 或 **D 运营者本人真实经历**。A 视角只写作品上看得见的设计/工艺决定，不编造过程与情节。
2. **AI 标识**：「发布设置」必须提示勾选「添加 AI 生成内容标识」（《标识办法》第十条法定义务）；A2/B 笔记正文末行附效果图声明；不得称实拍、成品图、买家秀。
3. **零虚假互动**：不写小号、托儿、伪素人、买评论、互赞群脚本；评论区只有作者本人与真实用户。
4. **零站外导流**：不出现微信、电话、二维码、外链、谐音暗号与站外平台名；成交在站内（店铺商品页、站内私信、官方留资组件）。
5. **零软件名 · 零绝对化承诺 · 零迷信丧葬意象**；正文不写病因与事故细节。
6. **一文一事 + 文题强对齐**：先写正文，8 条标题全部取材于正文并标注出处。
7. **落盘**：文案只写 `文案存储根目录/{char_dir}/小红书文案.md`，图片只放 `图片存储根目录/{char_dir}/`；不建临时会话目录，不发邮件。
8. **不生成提示词**：需要出图或重出图时，提示用户调用 fullcolor 技能。

用户要求越线（冒充亲属、刷评、导流暗号、迷信营销）时：说明风险，拒绝该部分，给出合规替代写法。

---

## ⚙️ 工作流

```
Step 0  加载      config/constants.md → xiaohongshu_ai_rule.md 第零节
Step 1  图片      inspect_images.py → EXIT / GENERATE / REUSE
Step 2  人物      character_profile.md → 信物、服饰、神态、母题
Step 3  定型      笔记类型 + 叙事视角（决策树）
Step 4  正文      一文一事 · 五层结构 · 180–220 字
Step 5  标题      依文提炼 8 条 + 封面大字
Step 6  图与话题  封面候选 · 图序 · 话题三层结构
Step 7  运营卡    置顶 · 回复库 · 负面应对 · 私信 SOP · 发布计划 · 复盘
Step 8  落盘校验  validate_copy.py → BLOCKER = 0 才交付
```

**Step 1 · 图片状态机**：运行 `python3 <skill>/scripts/inspect_images.py {char_dir}`。
- `EXIT`（0 张）：停止，提示放入底图 0.jpg 或先用 fullcolor 出图；
- `GENERATE`（仅 0.*）：读取 Obsidian 中的 `prompts.md`，以 0.* 为参考图调用当前环境的生图工具（02–10 按 3:4）；**环境没有生图工具时**，提示用户用 fullcolor 出图，文案可先行并在图序中标注"待配图"；
- `REUSE`（≥2 张）：不生图、不输出提示词，直接选封面与图序。存量 1:1 素材整篇保持 1:1。

**Step 3 · 视角决策**（详见 `copywriting-craft.md` 第 1 节）：
有客户书面授权故事 → C；运营者本人真实经历 → D；手办已实物打印且有真实制作记录 → A1；**其余一律 A2 或 B**。

**Step 5 · 字符数**：不要心算，用 `python3 <skill>/scripts/validate_copy.py --count "标题1" "标题2" …`。

**Step 8 · 校验**：运行 `python3 <skill>/scripts/validate_copy.py <小红书文案.md>`。BLOCKER 必须清零；MAJOR 修正或在交付说明中写明原因；把结论填入元数据"校验状态"。

---

## 📦 输出契约：`小红书文案.md`

校验器按下列小标题定位内容，**标题文字请保持不变**。

```markdown
# 小红书发布包：{char_dir}

> **资产编号**：{char_dir}
> **叙事视角**：A2 手艺人设计手记 ｜ B 第二人称代入 ｜ C 真实客户故事（已授权） ｜ D 运营者本人经历
> **笔记类型**：情感共鸣型 ｜ 工艺揭秘型 ｜ 选购指南型 ｜ 交付记录型
> **叙事母题**：{编号与名称}
> **规则版本**：v2.0 · **校验状态**：{validate_copy.py 结论}
> **生成日期**：{YYYY-MM-DD}

---

## Part A · 发布内容（可直接复制）

### 🏷️ 标题备选
1. ⭐ `[公式类型]` 标题文字 (xx字) 【提取自正文：……】
（共 8 条，≥ 5 种公式）

### 📝 正文
（180–220 字，五层结构，一文一事）

### 📌 正文末行声明
图为 3D 手办设计效果图（AI 生成），实物以打样确认为准。

### #️⃣ 话题标签
#核心大词 … #场景中词 … #长尾词 …（8–12 个）

### 🖼️ 封面与图序
- 封面大字：……（6–10 字）
- 比例：3:4（存量 1:1 素材则整篇 1:1）
- P1 封面：视角07_掌心温存.jpg ／ P2 … ／ P7 定制流程卡【建议截图】 ／ 末张 互动问题卡

### 🛡️ 发布设置
- 勾选「添加 AI 生成内容标识」
- 合集：……

---

## Part B · 运营执行卡（不发布）

### 💬 置顶评论
> ……（作者本人口吻，接住正文单一事件，抛出问题；不留联系方式、不报价）

### 🗂️ 评论回复库
| 用户在问 | 回复要点 |
| --- | --- |

### 🚧 负面与敏感评论应对
……

### ✉️ 私信承接 SOP
共情 → 照片评估 → 方案与报价 → 授权与隐私 → 流程与交期 → 站内下单 → 交付回访

### ⏰ 发布计划
建议时段 · 合集 · 相关节点 · 同人物再发间隔

### 📊 复盘指标
2h / 24h / 72h / 7d 看什么、低于基准线时改什么
```

---

## 🧪 常用命令

```bash
S=~/.skillshub/xiaohongshu-memorial-3dprint-copywriter
python3 $S/scripts/inspect_images.py char_45                     # 图片状态机、尺寸与比例
python3 $S/scripts/validate_copy.py  "<文案目录>/小红书文案.md"     # 单篇校验，BLOCKER 时退出码 1
python3 $S/scripts/validate_copy.py  --count "标题1" "标题2"        # 标题字符数
python3 $S/scripts/validate_copy.py  --all --report ~/Desktop/文案审计.md   # 全库审计
bash    $S/scripts/validate-config.sh                            # 改 config/constants.md 后自检
```

v13 及以前生成的文案多为第一人称亲属视角、含小号互动脚本，重新发布前请按本版重写；先用 `--all` 审计定位问题。

---

## 🗂️ 文件地图（按需读取，不要一次全读）

| 何时读 | 文件 | 内容 |
| :--- | :--- | :--- |
| Step 0 | `config/constants.md` | 数值、路径、视角定义、业务参数、校验词库 |
| Step 0 | `references/xiaohongshu_ai_rule.md` | 法定与平台依据、14 个治理类目、环节合规对照 |
| Step 3–5 | `references/copywriting-craft.md` | 视角矩阵、单一事件、五层结构、去 AI 味、11 标题公式、封面大字、标杆改写对照 |
| Step 4 | `references/emotional-story-templates.md` | 6 母题范例（绑定真实人物档案，A2/B/C） |
| Step 6–7 | `references/operations-playbook.md` | 账号底座、内容矩阵、封面图序、关键词、发布节奏、节点日历、复盘 |
| Step 7 | `references/conversion-and-traffic-safety.md` | 用词字典、评论区运营、私信 SOP、客户授权要点 |
| 选购/工艺类笔记 | `references/bao.md` | 分发机制（经验口径）、非情感类标题公式、封面规范 |
| 交付前 | `checklists/unified-checklist.md` | 48 项清单（标注哪些由脚本自动检查） |

---

## 🤝 与 fullcolor 的协作

- fullcolor 产出 `character_profile.md`、`prompts.md` 与图片：00/01 为 1:1 建模参考（00 不发笔记），02–10 为 3:4 笔记场景图，07/10 为封面候选；
- 本技能只读取这些资产；需要重出图（例如存量 1:1 想整组换成 3:4）时，提示用户调用 `fullcolor-3dprint-character-prompts`。

<!-- ego-browser UI 验证测试 -->
