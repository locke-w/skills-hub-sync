# xiaohongshu-memorial-3dprint-copywriter 变更日志

## [14.0.0] - 2026-09-23 · 专业运营版

### 🔴 破坏性变更
- **叙事视角体系**：新增 A1/A2/B/C/D 视角，默认 A2 手艺人设计手记 / B 第二人称代入；禁止以第一人称冒充 AI 虚构人物的亲属讲"真实经历"（依据《人工智能生成合成内容标识办法》、小红书用户协议"不得将合成内容谎称为真实"、平台伪素人专项治理）。
- **输出结构**：`小红书文案.md` 改为「Part A 发布内容 + Part B 运营执行卡」，新增正文末行效果图声明、封面大字与图序、发布设置、负面评论应对、发布计划、复盘指标。
- **移除小号互动脚本与"共情买家号"证言**：改为作者本人置顶评论 + 真实用户回复库 + 授权口碑流程。
- **移除导流暗号**（"留个小爪印""戳置顶群聊"等）：成交路径改为站内店铺 / 私信 / 官方留资组件（依据《交易导流违规管理细则》）。

### ✨ 新增
- `references/copywriting-craft.md`：视角矩阵与决策树、单一事件、五层结构、去 AI 味 8 条、11 标题公式（含视角限制）、封面大字、char_45 标杆改写对照。
- `references/operations-playbook.md`：账号底座、内容矩阵（情感/工艺/选购/交付）、封面与图序、关键词三层、发布节奏、节点日历、数据复盘诊断表、单变量测试。
- `scripts/validate_copy.py`：从 `config/constants.md` 读取阈值与词库，自动检查 AI 标识、视角、效果图声明、虚假互动、导流、软件名、绝对化、迷信、标题字符（Emoji 保守口径）、文题重合、正文字数、多时空拼接、话题数、封面大字；支持单篇、批量审计、字符计数、自测。
- `scripts/inspect_images.py`：图片状态机判定、尺寸与比例、笔记配图比例一致性、封面候选检查。
- `config/constants.md` v2.0：叙事视角、笔记类型矩阵、封面与图片、话题、Emoji、发布与复盘、业务参数、校验词库（JSON）；数据口径标签【官方/经验/业务】。

### 🔧 修正
- `references/xiaohongshu_ai_rule.md` v2.0：补充法定与平台硬性依据（标识办法第十条、用户协议、导流细则、虚假营销专项、民法典第 994 条）；去掉"官方发布机构"式表述，标注为内部整理并注明核验日期；删除"小号剧本由真人适时发布"。
- `references/bao.md` v2.0：算法权重、阈值改标【经验】；修正示例标题字数（原示例多处超过 20 字符）；封面规格与 fullcolor 统一为 3:4。
- `references/conversion-and-traffic-safety.md` v2.0：重写为合规转化 SOP（用词字典、评论区运营、站内私信、客户授权要点）。
- `references/emotional-story-templates.md` v5.0：6 个母题范例改为 A2/B/C 视角并绑定真实人物档案；所有标题字符数经脚本校验。
- `scripts/validate-config.sh` v2.0：修复 `set -e` 下 `((n++))` 首次计数即退出的问题；新增词库自测与新配置项检查。
- `checklists/unified-checklist.md` v2.0：48 项，标注 26 项自动检查。
- SKILL.md 从 46KB 精简为入口文件，细节按工作流步骤渐进式加载。

### 🧹 清理与迁移
- 视觉类参考（`github-diorama-staging-matrix.md`、`nano-banana-hyperrealistic-engine.md`、`blender-render-and-img2img.md`）迁至 fullcolor 技能 `references/`（视觉职责单一归属）。
- 移入废纸篓：`scripts/send_email.py`（含硬编码邮箱授权码，SKILL 早已声明移除邮件功能）及其 `.pyc`、误存的会话记录 txt、`SKILL.md.backup`。

---

## [13.2.0] - 2026-09-13
- Phase 1 速赢优化：配置文件分离（`config/constants.md`）、统一检查清单、`validate-config.sh`。

## [13.x 及以前]
- 情感文案 + 23,400 场景矩阵 + 图片状态机 + Obsidian 落盘。
