---
name: fullcolor-3dprint-character-prompts
description: Use when generating AI realistic elder, parent, in-law, and late spouse character images or prompts for 3D full-color printing without portrait copyright risks, creating standardized 11 angle/scenario 3D printing prompt sets, or dynamically generating grassroots character profiles via formula with auto-deduplication against existing local asset libraries. (Strictly decoupled from copywriting: does NOT generate Xiaohongshu copywriting, which is reserved for downstream copywriter skills).
license: MIT
metadata:
  version: "3.8.0"
  domain: 3d-printing-and-ai-visuals
  xiaohongshu-compliance-ref: "/Users/wuyongjia/.gemini/config/skills/xiaohongshu-memorial-3dprint-copywriter/references/xiaohongshu_ai_rule.md"
  underlying-standards: "AI-Image-Prompt-Engineering-Guide-v2.6 x WJP-FullColor-Photopolymer-Resin x Midjourney-v8.2 x Open-Generative-AI-Reference x Generative-Media-Skills-Nano-Banana x Xiaohongshu-AI-Governance-v1.0"
  midjourney-reference-doc: "/Users/wuyongjia/obsidian-gitee/technology/🧰 AI工具/midjourney/Midjourney V8.x 核心参数与高级指令全景说明.md"
  prompt-save-root: "/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材"
  image-save-root: "/Users/wuyongjia/3D打印/素材"
  character-generator-mode: "dynamic-formula-engine"
  default-batch-size: 20
  prompts-per-character: 11
  triggers: 3D打印长辈提示词, 3D打印父母提示词, 3D打印公婆提示词, 3D打印老人提示词, 全彩打印模型提示词, AI生成真实长辈, 3D打印无版权人物, 真实长辈模型, 爸爸妈妈手办提示词, 公公婆婆手办提示词, 岳父岳母手办提示词, 老伴手办提示词, 逝去妻子丈夫提示词, 人物画像公式, 动态长辈人物生成, 底层长辈画像, 20个人物画像, 亲人手办画像公式, 去重人物画像, 种粮户手办提示词, 初代农民工手办, 长辈胸像提示词, 长辈全身像提示词, 3D打印多视角提示词, 素材库长辈, 消除真人侵权, 掌心手办提示词, 纪念手办人物, 煽情场景提示词, 人物铸造, 提示词人物唯一性, 全身人物full-body规约, MidjourneyV8核心参数
  related-skills: xiaohongshu-memorial-3dprint-copywriter, photorealistic-character-generator
---

# 小红书 3D 全彩打印真实长辈与亲人提示词工程专家 (v3.8 小红书 AI 治理红线合规与去重引擎版)

专为**“消除真人肖像侵权 ➔ 祖辈/父辈/伴侣/姻亲全代际底层偏多人物画像公式 ➔ 本地知识库扫描与全局正交防撞去重 ➔ 动态批量生成(默认20/自定义N) ➔ 00/01 视角人物唯一性指纹锁 (IFTS) ➔ 全身人物强制包含 full-body ➔ 严格遵循 Midjourney V8.x 参数说明 ➔ 小红书 14 大 AI 治理红线合规 ➔ 11 视角全景矩阵 ➔ 提示词入 Obsidian 知识库 ➔ 纯图片入 3D 打印素材库 ➔ 单一职责纯粹工程(严禁越界编写小红书文案)”**全链路打造。

> 📖 **【跨技能合规契约】小红书 AI 创作红线全面对齐**：  
> 本技能生成的图像资产是下游 `xiaohongshu-memorial-3dprint-copywriter` 小红书发布的视觉底座。  
> 必须无条件严格遵循小红书官方 14 大 AI 治理红线（权威详查手册见 `xiaohongshu-memorial-3dprint-copywriter/references/xiaohongshu_ai_rule.md`），重点在视觉提示词工程中坚决贯彻：  
> 1. **AI 视觉制作高标准 (categoryId=264)**：追求电影级光学景深与真实次表面散射，提示词中严禁出现导致五官崩塌、六指畸形、假面塑料感的低质词汇；  
> 2. **零肖像侵权与严禁仿冒名人 (categoryId=277, 271)**：全量人物画像 100% 采用算法虚构，严禁网络真实老人垫图，严禁任何明星名人面孔；  
> 3. **反同质化“数字泔水” (categoryId=279)**：强制依托 11 视角全景矩阵与全局正交防撞去重算法，杜绝单一模板机械批量刷图；  
> 4. **传递正向质朴家庭价值观 (categoryId=281)**：坚持普通平民劳作者人设，杜绝一切怪诞、通灵丧葬迷信与恐怖猎奇元素。

---

## 零、 核心设计哲学与十五项铁律

### 铁律一：消除侵权与“三禁双准原则” (禁动漫/CG假人、禁非中国人、禁过度磨皮幼态；准年龄生理质感、准家庭平民人设)
1. **零真人照片依赖（落实 categoryId=277）**：严禁用任何未经授权的网络真人肖像作为底图，所有人物均由本技能 Prompt 工程驱动生成，彻底从源头杜绝肖像侵权；
2. **严禁仿冒名人名流（落实 categoryId=271）**：严禁在提示词中使用任何演艺明星、商业公众人物的名字或面部特征作为参考，坚持中国普通家庭真实平民面容；
3. **人设严格贴地飞行与正向价值观（落实 categoryId=281）**：杜绝一切“武侠仙侠、王公贵族、悬浮霸总”人设，全量人物严格锚定为当代中国普通家庭最具情感温度的长辈与父母（如厨房忙碌外婆、国企老钳工爷爷、长途客运奔波的质朴老爸、操持全家勤俭坚韧的母亲、进城看娃默默付出的公公、起早煲汤的南方婆婆、婚礼上眼眶泛红的岳父、后备箱塞满土特产的岳母等）；
4. **“三禁”硬性拦截契约（落实 categoryId=264 视觉制作底线）**：
   - 坚决禁止动漫/二次元/3D卡通/CG假人/蜡像人偶；
   - 坚决禁止西方人/欧美人/白人面孔，正面强制锚定真实中国人长辈面容特征（Genuine East Asian facial features）；
   - 坚决禁止年轻化/幼态化/过度磨皮美颜假面，彻底剥离 AI 假人塑料感，杜绝肢体与手指畸变。
5. **“双准”年龄生理质感与平民人设契约**：
   - **准年龄生理质感**：按角色设定年龄精准描摹生理风霜，杜绝“全员堆砌白发老年斑”或“全员假面光滑”两种极端：
     - **35 ~ 50 岁（年轻/中年追忆与早逝父母）**：保留生活劳碌的自然微瑕（额头细微抬头纹、微倦但温柔的眼神、朴素发型、真实健康微黄皮肤与细微毛孔）；
     - **50 ~ 68 岁（中年/初老父辈、公婆、岳父母）**：精准刻画黑发夹杂微霜的鬓角（Salt-and-pepper hair at temples）、眼角深细笑纹与轻微眼袋、常年劳作带微茧的掌指、温厚坚韧的面部神采；
     - **68 ~ 85 岁（高龄祖辈）**：刻画花白银发、深长不对称鱼尾纹、局部自然老年斑（Subtle age spots）、骨节分明的双手。
   - **准家庭平民人设**：服饰用料贴合当代生活（棉麻、涤卡工装、针织开衫、洗旧夹克），道具具有真实烟火气。
6. **全局正交防撞去重（落实 categoryId=279 反同质化）**：动态生成人物画像时，自动扫描 Obsidian 本地资产库，对工种、服饰、信物、姿态执行正交排查，拒绝模板套用与千人一面。

### 铁律二：生图画幅比例绝对硬约束 1:1
- **全量视角与场景（视角 00 到 10）统一且唯一强制锁定 `--ar 1:1`**；
- 依据《Midjourney V8.x 核心参数与高级指令全景说明》，V8 支持任意比例的小数及整数比例，但针对 3D 打印与手办标准像场景，统一锁定 `--ar 1:1`，确保在嘉立创 3D 打印切片、手办工业建模点云以及小红书九宫格排版中具备最高的一致性与稳定性。

### 铁律三：Midjourney V8.x 核心参数与高级指令规约体系 (强制参考全景说明文档)
> **【强制】参考源绝对绑定**：
> 生成 Midjourney 提示词时，**必须严格参考并遵循《Midjourney V8.x 核心参数与高级指令全景说明》**（文档绝对路径：`/Users/wuyongjia/obsidian-gitee/technology/🧰 AI工具/midjourney/Midjourney V8.x 核心参数与高级指令全景说明.md`）。
> 提示词中所有 Midjourney CLI 参数名称、取值范围、默认值与组合方式必须与该全景说明文档保持 100% 严格一致，严禁出现非法参数或臆造参数！

1. **画幅与画质参数规约**：
   - **`--ar 1:1`【强制】**：画面宽高比锁定为 1:1，渲染边缘零畸变，完美契合 3D 打印模型点云重建与小红书排版；
   - **`--quality` / `--q`【推荐】**：默认使用 `--q 1`（常规标准算力深度）；商用高精细节定稿输出阶段推荐挂载 `--q 2`，进行高密度细节渲染；
   - **`--hd`【推荐】**：原生超清模式（HD 2K+）。在定稿商用输出或高清手办模型棚拍时推荐挂载，大幅提升树脂次表面 SSS、发丝细节与织物纹理密度；
   - **`--draft`【可选】**：草图批量模式，仅在前期批量快速筛选构图与角色构思时选用，正式模型手册严禁出现。

2. **风格与发散控制参数规约**：
   - **`--style raw`【强制】**：原始风格模式，全量强制开启！削弱 Midjourney 默认的调色与“审美偏置”，提高对真实物理光照、摄影光学镜头参数与 3D 打印光敏树脂物性质感的忠实还原；
   - **`--stylize` / `--s`【强制分层标定】**：
     - **视角 00（写实摄影定妆照）**：锁定 **`--s 80`**（处于文档规定的 50-100 平衡写实与美感区间，真实呈现东亚长辈皮肤微瑕与自然胶片颗粒）；
     - **视角 01（3D 模型手办标准像）**：锁定 **`--s 50`**（处于文档规定的 0-50 严格按字面生成区间，强力压制 AI 自作主张的面部脑补与艺术重绘，保障对 00 视角五官骨相的高保真锁定，严禁使用 `--s 100+`）；
   - **`--chaos` / `--c 0`【推荐】**：保持默认 0，确保四宫格高度稳定收敛，杜绝过度随机扰动；
   - **`--weird` / `--w 0`【强制】**：严禁挂载怪诞参数，杜绝抽象畸形；
   - **`--no`【强制】**：负向提示词，统一采用逗号分隔。00 视角拦截动漫/3D假人；01 视角剔除 3D 自残词，针对性拦截真实活人与石膏柱。

3. **图像参考与多模态一致性参数（Reference 跨视角联动扩展规约）**：
   - **`--oref <URL>`（全能参考 Omni-Reference）【推荐】**：根据 V8 说明文档，`--oref` 是 V8 推荐的主体一致性工具。在以 00 视角图片为底图生成 01 视角或其他衍生视角时，可选用 `--oref <URL> --ow 100~300` 强行锁定特定长辈的五官、随身信物与主体特征；
   - **`--cref <URL>`（角色参考）& `--cw`【推荐】**：经典面部/角色迁移。当需全套复制面部与服饰时使用 `--cw 100`；若仅锁定脸部五官允许服装微调时使用 `--cw 0`；
   - **`--sref <URL>`（画风参考）& `--sw`【可选】**：需要统一特定影调氛围时使用。

4. **高级渲染、语法与控制符规约**：
   - **`--seed <数值>`【推荐】**：取值范围 `0` – `4294967295`。当需要复现特定长辈面部神态或固定结构基底进行局部微调时，使用固定 seed；
   - **单段自然语言流（严禁双冒号 `::` 多文本分割）**：虽然 V8 架构支持双冒号权重控制，但 Midjourney V8.2 官方明确限制了多文本分割语法（若输入 `::` 会报错 `Failed to submit: Multiple text prompts aren't supported for --version 8.2`）。因此，所有提示词必须采用**纯连贯单段自然语言流**，各语义层次之间统一使用逗号空格 `, ` 连接；
   - **适配网页端交互**：提示词开头绝不添加 `/` 或 `/imagine prompt:` 前缀，便于用户在网页端直接无缝复制粘贴提交。

### 铁律四：摄影光学与生理微瑕分层规约 (去 AI 塑料感)
1. **严禁空洞词汇**：禁止使用 `masterpiece, 8k, hyperrealistic, ultra detailed, smooth skin`；
2. **年龄分层生理微瑕精准注入**：
   - 严禁机械千人一面：依据人物年龄与劳作身份差异化注入微瑕，如客运父亲的面颊风霜与微红血丝、工装父亲的指关节微黑油印老茧、母亲的温和笑纹与手腕岁月镯痕、高龄祖辈的不对称鱼尾笑纹与局部淡老年斑；
3. **嘉立创 WJP 全彩光敏树脂材质还原**：指定 `delicate matte polymer finish, subtle resin translucency with subsurface scattering (SSS)`，模拟温润亲肤的次表面光泽；
4. **专业光学器材标定**：定妆照指定哈苏中画幅（`Hasselblad X2D 100C + 90mm f/2.8 at f/3.2`），手办场景指定佳能微距（`Canon EOS R5 + RF 100mm f/2.8L Macro / RF 50mm f/1.4 / RF 85mm f/1.4`），统一搭配 `Kodak Portra 400` 细腻胶片银盐颗粒。

### 铁律五：嘉立创全彩 WJP 树脂力学水密性规约与全身 full-body 强制契约
1. **胸像规格 (BW/BM)**：物理高度 6.0 cm，一体化微倒角深色加重工艺品手办底座（Artisanal Collectible Display Base，坚决禁止白色石膏柱、大理石罗马柱等西方石膏雕塑风格；必须采用典藏手办标准的深色微切边工艺品底座），实心封闭网格，壁厚 $\ge 1.5\text{mm}$；
2. **全身像规格 (FW/FM)**：物理高度 12.0 cm，一体化平滑加重微型圆形工艺品基座（直径 40~45mm），重心稳定；
3. **【强制】全身人物提示词必须包含 `full-body` 契约 (Full-Body Token Enforcement)**：
   - **规约红线**：**凡生成的人物类型为全身人物（姿态代号为 `FW` / `FM`，或包含全身站姿、坐姿、全身比例与下半身构图的角色提示词），生成的英文 Prompt 必须显式包含 `full-body` 关键词（例如 `full-body portrait`, `full-body shot`, `12.0cm 3D printed painted resin full-body model`, `full-body view`）！**
   - **底层机制（阿里防御性门禁）**：扩散模型在未显式声明全身时，受文本注意力默认偏置影响，极易自作主张截取上半身胸像或近景特写，导致下半身衣着、鞋履及一体化工艺品底座丢失。显式注入 `full-body` 能在文本注意力头（Cross-Attention Heads）中强制锁定全景深景别与全身骨骼比例，确保模型自头至脚、包括底座完整生成，杜绝肢体截断；
4. **熔接防断加粗**：老花镜梁镜腿加粗至 $\ge 1.2\text{mm}$ 并与面颊熔接；随身道具（车把、工具、碗筷）必须实体融入身躯，禁止悬空细丝。

### 铁律六：动静分离双库落盘与标准目录命名契约
1. **知识库与提示词（Obsidian）**：
   `/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/{char_dir}/`
   - `character_profile.md`：人物小传、外貌特征、随身信物、3D 打印力学规范（头部元数据必须携带 `compliance: xhs_ai_rule_verified`，证明经过小红书 14 大规则合规审计）；
   - `prompts.md` / `prompts.json`：包含 11 个视角的中英文标准提示词手册；
   - **【红线禁令】本技能严禁在此生成 `小红书文案.md`！文案必须由下游 copywriter 技能独立生成。**
2. **纯图片资产库（3D 打印本地驱动）**：
   `/Users/wuyongjia/3D打印/素材/{char_dir}/`
   - 保持纯净图片目录，仅存放生成的 `.jpg` / `.png` 图像。

### 铁律七：视角 01【模型标准像】3D 模型显式锚定与防翻车黄金法则
1. **显式注入 3D 模型实体声明（3D Model Head Noun Anchoring）**：
   - 首句必须显式包含 **`3D model`** 与 **`3D printed painted resin`** 实体主语，前置统摄全局：
     - **胸像 (BW/BM)**：`Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust...`
     - **全身像 (FW/FM)**：`Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model...`（【强制】必须显式包含 `full-body`）
   - 彻底废除旧版中 `precisely transforming the exact ... from the reference photo into a collectible figurine` 等冗长解释性水词。扩散模型不具备“阅读长篇元指令并反向推理原片”的能力，这类无效 Token 只会稀释注意力。
2. **彻底根除负向词自残矛盾（避免生出活人）**：
   - 严禁在视角 01（及所有纯 3D 模型/手办场景）的反向负向参数中加入 `doll`, `3d render`, `plastic skin`, `porcelain doll`, `wax museum`！
   - 一旦在 `--no` 中排除 `doll` 和 `3d render`，Midjourney 在 CFG 计算时会被迫反向生成“真实活人”，导致生图翻车浪费算力与费用。
3. **工艺品底座物理融合（严禁石膏罗马柱）**：
   - **坚决杜绝石膏像缺陷**：严禁使用 `stone pedestal`, `neoclassical stone pedestal`, `plaster`, `marble column`！此类词汇会强制 Midjourney 生成西方希腊罗马式的白色雕花石膏柱，与中国家庭长辈手办产生极强违和感和石膏墓碑既视感；
   - **胸像工艺品底座规约**：`mounted on dark beveled pedestal base`（一体化光滑微倒角深色加重工艺品手办底座）；
   - **全身像工艺品底座规约**：`full-body standing/seated on weighted circular base`（一体化微倒角加重圆形工艺品手办底座，显式包含 `full-body`）；
   - 杜绝 Midjourney 空间幻觉，确保模型稳固接地、切片软件可直接布设支撑。
4. **纯灰影棚隔离与防真人及防石膏负向强拦截**：
   - 正向：`subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus`
   - 负向针对性拦截活人、石膏柱与生活居室：`--no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`
5. **参数配比标定（控制风格化保护人脸保真度，严格参考全景说明）**：
   - 锁定 `--ar 1:1 --style raw --s 50 --v 8`（依据《Midjourney V8.x 核心参数与高级指令全景说明》，3D 模型标准像统一采用 `--s 50`，严禁使用 `--s 120`，大幅压制 AI 自作主张的面部脑补与艺术重绘，保障对 00 视角五官骨相的高保真锁定）。

### 铁律八：跨平台双引擎分工契约与零资产代码泄露
1. **彻底根除内部工程代号（Zero Asset ID Leakage）**：
   - 严禁在提示词（无论英文还是中文）中出现任何本地工程目录命名、变量名或编号（如 `char_XX_XX`、`char_01_BW`、`char_12_FW` 等）！
   - Midjourney 和 Gemini 作为通用基础模型，不认识任何私有变量代码；这类碎片 Token 会被错误分词（如 `char` -> 烧焦/角色, `12` -> 12个人/12根棍子），严重污染 Token 词嵌入空间与生成构图。
2. **生图引擎职责分工契约（Engine Delegation Protocol）**：
   - **视角 00 & 01 ➔ Midjourney 专属**：
     - 发挥 Midjourney 在单主体写实人像皮肤纹理、微距光学镜头虚化及灰背景影棚光影渲染上的顶级表现力；
     - 语法规范：单段连贯自然语言流，末尾严格依照《Midjourney V8.x 核心参数与高级指令全景说明》携带 `--ar 1:1 --style raw --s 80（视角00）/--s 50（视角01） --v 8 --no ...`。
   - **视角 02 ～ 10 ➔ Gemini (Imagen 3) 专属**：
     - 发挥 Gemini (基于大语言模型 T5-XXL / Gemini 语义编码器) 在复杂空间拓扑推理（Spatial Reasoning）、主体嵌套从属绑定（Attribute Binding）上的碾压级优势（例如将微缩手办置于大衣口袋、婚宴餐桌、书桌奶糖旁、掌心托举等复杂场景）；
     - 语法规范：纯自然语言分层叙事（Natural Language Prompt），**严禁出现 Midjourney 的 CLI 命令行参数（禁止 `--ar`, `--v 8`, `--style raw`, `--no` 等）**，末尾统一以自然语言负向排除（如 `Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.`）。

### 铁律九：视角 01 提示词依靠 00 视角微调成 3D 模型衍生协议 (00-to-01 3D Model Mutation Protocol)
> **核心设计哲学（依靠 00 微调衍生，绝非另起炉灶）**：
> 视角 00 是写实原片基底，视角 01 是 1:1 的 3D 模型微缩手办标准像。二者是严格的**“原片基底 ➔ 3D 模型局部微调转化”**衍生关系。
> **视角 01 提示词严禁脱离 00 重新起草独立句式，必须直接依靠（以...为基础）视角 00 的提示词，通过四大微调置换算子（Mutation Operators），精准微调成 3D 模型！**
> 
> **底层原理（阿里高内聚规范 × 扩散模型注意力锁定）**：
> 在文本生成图像模型中，若两段提示词的人物描述 Token 序列高度吻合，模型在潜变量空间（Latent Space）中的面部骨相、神态表情、发色发型、服饰色彩注意力权重将达到最高程度的对齐。一旦推翻 00 重写一段辞藻迥异的长句，跨模态注意力立即漂移，导致生成的 3D 模型变成完全陌生的另一个人。

#### 四大标准微调置换算子 (4-Step Mutation Operators)

```
【视角 00：真实生活抓拍提示词】
  │
  ├─ 算子 ① [主体媒介微调] ➔ 替换为 3D 模型显式主语 (3D model, 3D printed painted resin...)，全身像必须包含 full-body
  ├─ 算子 ② [特征完全继承] ➔ 100% 逐字继承 00 面容、发型、饰品，衣服追加 sculpted
  ├─ 算子 ③ [环境底座微调] ➔ 去除生活背景，微调为工艺品底座与浅灰无缝影棚 (pedestal, cyclorama...)
  └─ 算子 ④ [参数负向微调] ➔ 风格化按参数文档降为 --s 50；负向词移除 3D/手办拦截，微调为拦截活人与石膏
  │
  ▼
【视角 01：3D 模型标准像提示词】
```

1. **算子 ①：主体与媒介微调（Subject & Medium Mutation ➔ 显式声明 3D 模型）**：
   - **00 原版**：`Candid documentary portrait of a real [age]-year-old Chinese [role] in [setting]`（若为全身像，原版包含 `full-body portrait`）
   - **01 微调为**：
     - **胸像 (BW/BM)**：`Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, [age]-year-old Chinese [role],`
     - **全身像 (FW/FM)**：`Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model, [age]-year-old Chinese [role],`（【强制】必须显式包含 `full-body`）
   - **微调红线**：首句前置明确注入 **`3D model`** 与 **`3D printed painted resin`**，直球定义实体为物理 3D 打印模型，严禁任何绕弯的解释性废话。
2. **算子 ②：长辈特征 100% 逐字继承微调（Character Identity Token Preservation）**：
   - **00 原版**：面部骨相、眼角笑纹、发型发色、耳饰、衣着描述序列，例如：
     `East Asian features, crinkling smile eyes, deep crow's feet, silver-gray hair bun, silver hoop earrings, wearing navy frog-button tunic with floral apron`
   - **01 微调为**：
     **100% 逐字原样继承 00 的特征词序列**，仅在服装或手持信物前微调加入 `sculpted` 修饰词（如 `sculpted navy frog-button tunic with floral apron`）；
   - **微调红线**：绝不允许在 01 中私自篡改发色、增删皱纹或替换衣服款式，确保长相和衣着与 00 绝对同源。
3. **算子 ③：环境与基座微调（Setting & Pedestal Mutation）**：
   - **00 原版**：家庭生活环境与自然采光（如 `in kitchen, soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain`）
   - **01 微调为**：工艺品底座与浅灰无缝影棚微距光照：
     - **胸像**：`mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus`
     - **全身像**：`full-body standing/seated on weighted circular base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus`（【强制】包含 `full-body`）
   - **微调红线**：彻底剥离室内家具杂乱背景，强制注入微倒角深色工艺品底座（严禁石膏柱），材质赋予次表面散射（SSS）。
4. **算子 ④：参数与负向拦截微调（Parameters & Negative Mutation）**：
   - **参数微调**：依照《Midjourney V8.x 核心参数与高级指令全景说明》，`--s 80` ➔ 微调为 `--s 50`（手办标准像控制自由发散，锁定 00 骨相）；
   - **负向拦截反向微调**：
     - **00 原版**：`--no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands`（封杀 3D/假人）
     - **01 微调为**：**彻底剔除 `3d render`, `doll`, `figurine`, `plastic skin` 等自残拦截词**，反向微调为封杀真实活人与石膏柱：`--no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`。

### 铁律十：视角 00 与视角 01 差异性与微调映射矩阵 (00 vs 01 Diff & Mutation Matrix)
> **阿里规范排他契约**：视角 01 依靠 00 微调，通过下述 8 大维度的精准映射，实现“人物形象 100% 相同、载体本质 100% 切换为 3D 模型”：

| 约束维度 | 视角 00：【基底定妆照】真实长辈生活写实摄影 | 视角 01 微调操作 (Mutation Action) | 视角 01：【模型标准像】依靠 00 微调成的 3D 模型 |
| :--- | :--- | :--- | :--- |
| **1. 主体本质 (Entity)** | 真实活人纪实生活肖像抓拍 (`real elderly Chinese...`)；若为全身像【强制】必须包含 `full-body` (`full-body portrait`) | **置换为 3D 模型** | 3D 打印全彩光敏树脂模型 (`3D model, 6.0cm bust` 或 `12.0cm full-body model`)；全身像【强制】必须包含 `full-body` |
| **2. 表面材质 (Material)** | 真实人体皮脂微孔、天然皱纹与体温感 (`natural skin texture, pores`) | **置换为树脂 SSS 质感** | 工业级光敏树脂哑光微透光次表面散射 (`subtle resin SSS finish, painted details`)，**严禁毛孔** |
| **3. 人物特征 (Face/Hair)** | 东亚五官、眯眯笑眼、深鱼尾纹、花白发髻/寸头 | **100% 逐字保留复用** | 100% 严格继承 00 原文 Token 序列，面部骨相与神态零偏差 |
| **4. 服装配饰 (Clothes)** | 真实生活棉麻盘扣小袄、工装夹克、围裙、老花镜 | **原样继承 + 微调雕塑化** | 继承 00 原文颜色与款式，服饰前微调增加 `sculpted` 修饰词，贴身配饰完整保留 |
| **5. 环境背景 (Scene)** | 真实中国家庭生活环境（厨房、书房、阳台窗光） | **置换为纯灰影棚天幕** | 纯浅灰无缝影棚天幕 (`solid neutral light gray seamless cyclorama`)，杜绝居室背景 |
| **6. 基座力学 (Base)** | 活人自然站/坐，**绝对无底座** | **注入一体化工艺品底座** | **胸像**：深色微倒角底座 (`dark beveled pedestal base`)；**全身像**：加重圆盘底座（`full-body standing on weighted circular base`），**严禁石膏柱** |
| **7. 镜头景深 (Optics)** | 哈苏中画幅 90mm f/3.2 纪实浅景深柔和虚化 | **置换为微距全焦清晰** | 佳能 RF 100mm f/8 正交 0° 视平线微距，大景深边缘锐利 (`RF 100mm f/8 focus`) |
| **8. 参数与负向 (Params)** | 参考 V8 参数说明：`--s 80` 搭配封杀假人 (`--no anime, 3d render, doll...`) | **参数降级 + 反向拦截活人** | 参考 V8 参数说明：`--s 50` 搭配封杀活人与石膏 (`--no real living human, skin pores, plaster, stone column...`) |

---

### 铁律十一：提示词长度硬性上限与高信噪比精简架构 (Prompt Length & High-SNR Compact Protocol)
> **告别过度包装，回归高信噪比**：
> Midjourney 官方 CLIP 词嵌入的黄金敏感窗口在 **40 ～ 60 词**。超过该长度不仅会在网页端频繁弹出黄色 `Long Prompt` 警告，还会导致提示词末尾的材质、基座与负向参数被严重稀释。
> 本技能对视角 00 与 01 提示词实施**严格的词数熔断机制**，用精准的工业与光学核心词替换所有无效修饰水词！

1. **词数硬上限控制契约**：
   - **正向词 (Positive Prompt)**：硬性约束在 **35 ～ 50 英文单词**（精准覆盖：3D模型主体+00特征继承+雕塑服装+基座/背景+树脂光学；全身像包含 `full-body`）；
   - **负向词 (Negative Prompt `--no`)**：硬性约束在 **12 ～ 18 英文单词**（只保留致命缺陷与互斥拦截词，剔除近义词堆叠）；
   - **总词数 (Total Word Count)**：单条完整提示词硬性控制在 **50 ～ 70 词** 高效敏感区间，彻底消除 `Long Prompt` 告警。

2. **瘦身与降噪清洗三原则（Zero-Signal Token Elimination）**：
   - ❌ **剔除前缀客套词**：从 `A professional macro studio photograph of an exquisite tabletop collectible painted resin bust statue precisely transforming the exact...`（30+ 词）压缩为 `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust...`（13 词）；
   - ❌ **消除近义修饰堆叠**：将 `warm gentle crinkling eyes with deep natural crow's feet, realistic nasolabial smile lines, natural age spots and fine skin texture` 精炼为 `crinkling smile eyes, deep crow's feet, natural age spots`；
   - ❌ **清理负向冗余词**：合并 `young, youthful, teenager, child` 为 `young, child`，合并 `caucasian, western, foreigner, white person, non-asian` 为 `western, non-asian`，保留核心拦截效能。

3. **视角 00 与 视角 01 标准化高信噪比结构公式 (Templates · 包含 full-body 与 V8 参数规约)**：
   - **视角 00 胸像高信噪比公式（基底写实胸像原片，总词数 55 ～ 65 词）**：
     ```text
     Candid documentary portrait of a real [age]-year-old Chinese [role] in [setting], East Asian features, [smile/expression], deep crow's feet, [hair style/color], wearing [clothing & accessory], soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
     ```
   - **视角 00 全身像高信噪比公式 (基底写实全身原片，【强制包含 full-body】，总词数 55 ～ 65 词)**：
     ```text
     Candid documentary full-body portrait of a real [age]-year-old Chinese [role] in [setting], East Asian features, [IFTS], full-body view, wearing [clothing & shoes], soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
     ```
   - **视角 01 胸像高信噪比公式 (依靠 00 微调成 3D 模型，总词数 55 ～ 65 词)**：
     ```text
     Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, [age]-year-old Chinese [role], [smile/expression], deep crow's feet, [hair style/color], [accessory], sculpted [clothing], mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
     ```
   - **视角 01 全身像高信噪比公式 (依靠 00 微调成 3D 模型，【强制包含 full-body】，总词数 55 ～ 65 词)**：
     ```text
     Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model, [age]-year-old Chinese [role], [expression], facial wrinkles, [hair style/color], sculpted [clothing & shoes], holding [welded prop], full-body standing on weighted circular base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
     ```

### 铁律十二：人物深度铸造流水线前置协议 (Character Forging Pipeline & 5D Portrait Card)
> **阿里规约防御式门禁（Pre-execution Barrier）**：
> 每次执行任务时，**严禁跳过人物铸造直接编写提示词**！
> 任何人物在生成 11 视角提示词之前，必须首先完整铸造出《五维人物铸造画像卡》（5D Character Forging Card），并落地至该人物 Obsidian 知识库中的 `character_profile.md`。五维完备度未通过校验前，提示词生成流水线处于强制熔断阻断状态。

1. **五维人物铸造画像卡标准规范 (5D Character Forging Specifications)**：
   - **维度一：面部骨相指纹 (Facial Bone Structure Fingerprint)**：
     - 必须显式锚定 5 大核心解剖学特征：颧骨弧度（Cheekbones）、下颌骨轮廓（Jawline）、眉弓深度（Brow ridge）、鼻梁形态（Nose bridge）、眼窝眼睑走向（Eye sockets & eyelids）。严禁使用空泛形容词，必须具象化到物理骨相骨架；
   - **维度二：生理微瑕签名 (Physiological Imperfection Signature)**：
     - 汲取 GPT-Image-2 皮肤微瑕工程精髓，确立不可替代的生理岁月印记：特定位置的眼角深笑纹（Asymmetric crow's feet）、不对称法令纹（Nasolabial smile lines）、额头岁月横纹（Forehead lines）、局部自然老年斑（Subtle age spots on cheek/temple）、老化微小毛孔与真实皮脂纹理（Micro pores & weathered skin texture）；
   - **维度三：服饰色彩 DNA (Wardrobe & Color DNA)**：
     - 锁定人物唯一的主色调（Dominant color）、辅色搭配（Accent color）、面料质感（Fabric texture，如粗织棉麻、纯棉细斜纹、灯芯绒、水洗涤卡）、传统工艺细节（手工盘扣 frog buttons、老式工装铜拉链、明线走线）；
   - **维度四：随身信物锚定 (Signature Artifact Anchoring)**：
     - 锁定 1～2 件不可替代的终身情感随身物（如复古铜梁老花镜、包浆搪瓷茶缸、不锈钢保温桶、二八大杠车把、铝制缝纫线管），信物必须严格遵循嘉立创树脂力学规范（壁厚 $\ge 1.2\text{mm}$，与身躯实体熔接）；
   - **维度五：神态动态基线 (Expression Dynamics Baseline)**：
     - 锁定人物最具辨识度的神态表情（如眯眼慈祥含笑、沉着专注思索、眺望远方期盼、嘴角微扬释然），严格约束眼神聚焦点与面部肌肉牵引弧度。

2. **人物铸造流水线状态机流转契约**：
   ```
   [确定长辈人设选题]
          │
          ▼
   [执行五维深度铸造] ➔ 输出《五维人物铸造画像卡》
          │
          ▼
   [五维完备性门禁校验] ➔ 若缺失任何一维，强制阻断并补充铸造
          │
          ▼
   [提炼 15~20 词 IFTS 指纹序列] ➔ 写入 prompts.json 根节点
          │
          ▼
   [落盘 Obsidian character_profile.md]
          │
          ▼
   [放行进入 11 视角提示词构建流水线]
   ```

---

### 铁律十三：00 ↔ 01 视角人物唯一性指纹锁与全局正交互斥矩阵 (Identity Fingerprint & Anti-Collision Specification)
> **扩散模型潜变量注意力锁定与防撞车原理**：
> 1. **跨视角一致性**：Midjourney V8 及前沿多模态扩散模型在潜变量空间（Latent Space）进行去噪时，若视角 00（生活写实抓拍）与视角 01（3D 模型手办标准像）的人物特征描述序列发生 Token 漂移、顺序倒置或同义词替换，文本交叉注意力机制（Cross-Attention）将采样至截然不同的人脸特征流形，导致生出的手办与写实原片长相脱节（变成两个不同的人）；
> 2. **全局唯一性排他性**：若素材库人物库中出现两位人物面部特征、服饰款式、随身信物高度重叠，将导致生成模型与下游文案发生严重审美疲劳与同质化。因此，必须在人物库全局实施**正交防撞车五重防御机制**！

#### 1. 全局正交防撞车五重防御机制 (5-Layer Anti-Collision Architecture)
- **第一重·数据结构与命名绝对唯一（本地知识库扫描与动态自增）**：
  - 全局统一编号：动态顺延编号 `char_01` ~ `char_N`，严格绑定所属代际（祖辈代 / 父辈代 / 伴侣代 / 姻亲代）与姿态类型（`BW`/`BM`/`FW`/`FM`）；
  - 执行前置扫描 `/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/` 下所有现存 `char_XX_*` 目录，计算已有最大编号 $\text{MAX\_ID}$，新批次自动从 $\text{MAX\_ID} + 1$ 顺延自增，严禁 ID 碰撞与覆写；
- **第二重·骨相与发型正交互斥**：
  - 每位人物的面部解剖学轮廓（颧骨、下颌、眼睑、眉弓）与发型发色（如客运老爸高颧骨黑短发两鬓微霜、工程师老爸方颌黑框半框镜、坚韧母亲温润圆脸微卷齐肩发、爱美老妈精致短烫珍珠耳饰、质朴公公红铜深肤高额头、会计婆婆金丝花镜齐耳短发、婚礼岳父剑眉整齐背头、后备箱岳母银白发箍等）在全局库中必须保持独立组合，严禁复制粘贴；
- **第三重·服饰色彩 DNA 互斥池 (Wardrobe Color Mutual-Exclusion Pool)**：
  - 规定每个人物拥有唯一的主色调搭配，如：
    - `char_01`: Navy blue frog-button tunic with floral apron
    - `char_06`: Vintage faded dark blue cotton worker overalls
    - `char_21`: Faded dark charcoal cotton work jacket with worn leather belt
    - `char_22`: Deep midnight-navy zippered collared utility jacket
    - `char_23`: Warm mustard-yellow hand-knitted coarse wool cardigan
    - `char_24`: Dusty rose double-faced wool short coat
    - `char_25`: Deep rustic brown ribbed corduroy worker jacket
    - `char_26`: Vintage faded olive green multi-pocket utility fishing vest
    - `char_27`: Muted brick-red linen tunic with dark protective sleeve-cuffs
    - `char_28`: Peacock blue tailored wool knit blazer
    - `char_29`: Tailored charcoal gray single-breasted suit with deep wine-red silk tie
    - `char_30`: Ivory cream quilted lightweight diamond-stitch jacket
    全库人物色彩互相正交，绝不撞衫；
- **第四重·随身情感信物池全局独占 (Prop Mutual-Exclusion Pool)**：
  - 核心原则：**一人一物，终身唯一**！每位长辈/父母/公婆独占 1 个最具情感穿透力的专属信物（如：黑皮革磨损钥匙包、素圈细银手镯、黄铜水烟袋、紫砂小炖盅、红木算盘挂件、长柄黑雨伞、生鲜排骨红塑料袋、拨浪鼓小毛线鞋、组装螺丝刀、扎满胶带的土特产纸箱等），任何两位人物严禁共享核心信物；
- **第五重·年龄分层生理印记精准锚定**：
  - 依据真实生理科学，严格区分年龄层：35~50 岁（年轻/中年追忆）、50~65 岁（中年/初老父辈与公婆）、68~85 岁（高龄祖辈），杜绝给 50 岁父亲套用高龄老年斑，杜绝千人一面。

#### 2. 唯一性指纹 Token 序列定义 (IFTS Definition)
- 必须从五维铸造画像中，提炼一段 **15 ～ 20 个英文单词的高密度核心指纹序列**（Identity Fingerprint Token Sequence，简称 **IFTS**）；
- **IFTS 标准语法格式**：
  ```text
  [age]-year-old Chinese [role], [bone-structure], [age-adapted wrinkles/signs], [hair-style & color], [eye-expression], [signature-accessory]
  ```
- **祖辈标杆级 IFTS 示例 (72 岁厨房外婆，18 词)**：
  `72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings`
- **父辈标杆级 IFTS 示例 (52 岁质朴客运老爸，17 词)**：
  `52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn leather keyring`
- **公婆代标杆级 IFTS 示例 (58 岁煲汤南方婆婆，17 词)**：
  `58-year-old Chinese mother-in-law, gentle round cheekbones, dark hair with silver streaks, soft smile crinkles, warm watchful eyes, black hair-claw clip`

#### 3. 00 ↔ 01 双视角绝对绑定契约 (Binding Contract)
- **视角 00 注入规范**：在主体写实声明后，**必须 100% 完整嵌入 IFTS 原文序列**；
- **视角 01 继承规范**：在 3D 模型实体声明后，**必须 100% 逐字原样继承 00 的 IFTS 全文序列**，禁止删改、禁止词序调换、禁止同义词替换；
- **单向不可变与唯一信任源 (Single Source of Truth, SSOT)**：
  - 提炼出的 IFTS 必须作为 `prompts.json` 顶层的独立字段 `identity_fingerprint_tokens` 显式持久化落盘；
  - 自动化一致性校验契约：`Assert(IFTS_in_00 == IFTS_in_01)`。如在代码审查或生成产物中发现 00 与 01 的人物特征存在词汇漂移，直接判定为发布阻断级缺陷（Blocker Defect）。

### 铁律十四：单一职责架构契约与零小红书文案越界红线 (Single Responsibility Principle & Zero Copywriting Boundary)
> **【阿里架构单一职责契约 (SRP)】**：
> `fullcolor-3dprint-character-prompts`（简称 fullskill）专精且仅专注于**底层工业级 3D 打印物理力学与人物提示词工程**，绝不越界承担上层营销文案职能。
>
> **【落盘产物唯一合法集合】**：
> 1. **知识库目录 (Obsidian)**：`/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/{char_dir}/`
>    - `character_profile.md`：五维人物铸造画像卡（小传、外貌特征、专属信物、3D 打印力学规范、生卒年）
>    - `prompts.md` / `prompts.json`：视角 00~10 标准双引擎提示词手册（含 IFTS 唯一指纹锁）
> 2. **纯图片资产库 (3D 打印本地驱动)**：`/Users/wuyongjia/3D打印/素材/{char_dir}/`
>    - 对应空文件夹创建，用于后续存放渲染出的高保真图片。
>
> **【绝对红线禁令】本技能执行时严禁编写或生成任何小红书文案！**
> 1. **禁止生成文件**：严禁在任何长辈目录下生成 `小红书文案.md`！
> 2. **禁止输出文案内容**：严禁在对话或产物中编写小红书 180~220 字正文、8 条爆款标题、评论区引流话术、九宫格排版规划或互动引导文案；
> 3. **职责隔离边界**：小红书文案属于下游应用层营销业务，必须交由专属技能 `xiaohongshu-memorial-3dprint-copywriter` 或全链路工作流 `xiaohongshu-3dprint-elderly-workflow` 读取本技能生成的画像与提示词后独立撰写与交付，严禁跨模块职责污染与功能越界！

### 铁律十五：防偷懒交付与 11 视角零缩水刚性门禁 (Zero-Shortcut & Full 11-Perspective Mandatory Completeness)
> **【阿里工程交付完整性红线】**：
> 坚决杜绝任何形式的偷工减料、抽样应付、截断缩写与未完待续交付！
> 
> 1. **全景即全量，少一个视角直接判定为发布阻断级缺陷 (Blocker Defect)**：
>    - 无论是批量生成（如 10 人、20 人）还是单个人物生成，每个角色目录下的 `prompts.md` **强制必须完整输出视角 00 到 视角 10 全部 11 个视角**！
>    - **严禁以“先出几个示例”、“测试抽样”、“暂时预埋模版”、“后续补齐”为借口只输出 00、01、03 等部分视角**！
>    - 严禁使用 `...`（省略号）、`TODO`、`以此类推`、`此处省略` 等任何糊弄占位符；
> 2. **交付自检三要素刚性门禁**：
>    每次声称人物模型与提示词生成完成前，执行代理必须在底层执行 `prompts.md` 完整性校验，确认必须包含全部 11 视角：
>    - [x] 视角 00 (MJ 写实定妆照)
>    - [x] 视角 01 (MJ 0°模型标准像)
>    - [x] 00 ➔ 01 差异对齐表 (Mutation Diff)
>    - [x] 视角 02 (Gemini 专属老座)
>    - [x] 视角 03 (Gemini 书房多宝阁·视平瞻怀)
>    - [x] 视角 04 (Gemini 岁月手艺)
>    - [x] 视角 05 (Gemini 窗台花草)
>    - [x] 视角 06 (Gemini 玄关守望)
>    - [x] 视角 07 (Gemini 掌心温存)
>    - [x] 视角 08 (Gemini 人间烟火)
>    - [x] 视角 09 (Gemini 深夜陪伴)
>    - [x] 视角 10 (Gemini 时光重叠)
>    以上 11 个视角任意一个缺失，或者缺少中文说明/英文 Prompt 的，直接判定为违规不合格，严禁向用户交付！

---

## 一、 11 视角/场景全景标准契约定义 (双引擎分工版)

| 视角编号 | 推荐生图引擎 | 视角 / 场景规范名称 | 镜头景别与构图元素 | 核心技术与平台优势 |
| :--- | :--- | :--- | :--- | :--- |
| **00** | **Midjourney** | **【基底定妆照】真实长辈/亲人生活写实摄影** | 哈苏中画幅写实纪实抓拍，真实生活面容与衣着，正脸半身胸像/全身 | 利用 MJ 顶级人像皮肤质感与胶片影调，消除真人肖像侵权 |
| **01** | **Midjourney** | **【模型标准像】0° 正面微缩手办棚拍 (依靠 00 微调成 3D 模型)** | 纯浅灰天幕，视平线正交 0° 机位，显式声明 3D 模型，100% 继承 00 面容与服饰 | 利用 00 提示词微调置换算子，锁定骨相神采，显式声明 3D 模型实体并防自残 |
| **02** | **Gemini** | **【煽情场景一·专属老座】午后空椅·日光守望** | 午后斜阳洒入老屋，磨损包浆的空椅/沙发旁老木几上，手办静伴水杯/信物 | 利用 Gemini 空间拓扑与大景深光影，呈现老座空椅与微缩手办的深情守候 |
| **03** | **Gemini** | **【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀** | 书房、红木多宝阁或带玻璃门展示柜中层偏上，高度与视线平齐或略高于视线 | 利用 Gemini 室内材质反光与微距光影，呈现既方便日常缅怀、又体现长辈尊崇与敬意的庄重端雅陈列氛围 |
| **04** | **Gemini** | **【煽情场景三·岁月手艺】旧物深情·生锈时光** | 置于老式缝纫机台面、机修铁皮箱、老图纸案台或工具台，真实生锈包浆与手办依偎 | 利用 Gemini 物理语义绑定，准确生成手办与真实生锈旧物的多物体关系 |
| **05** | **Gemini** | **【煽情场景四·晨曦静好】窗台花草·微风晨光** | 晨曦初照阳台窗台，白纱帘微拂，花草旁丁达尔光线洒在手办温润面庞 | 利用 Gemini 复杂多模态光影理解，呈现清晨纱帘晨曦与窗台盆栽意境 |
| **06** | **Gemini** | **【煽情场景五·风雨归人】玄关守望·长明灯与老钥匙** | 入户玄关复古深木柜，一串磨损发亮的黄铜老钥匙与泛黄手写便签，头顶 2700K 暖黄长明壁灯 | 利用 Gemini 室内低照度暖调光影与多信物互动，呈现“开门归家”的永恒守候 |
| **07** | **Gemini** | **【煽情场景六·掌心凝视】掌心凝视·思念具象** | 成年人真实手掌平稳托起 6cm/12cm 手办，真人体温掌纹与微缩手办接触 | 利用 Gemini 严格人体解剖手部生成与微缩手办的比例对齐（小红书爆款） |
| **08** | **Gemini** | **【煽情场景七·生活遗存】人间烟火·故物重逢** | 灶台/案头/门槛，老式汤锅、特产饭盒微汽与故物重温 | 利用 Gemini 真实烟火场景的多重物体布局与生活质感还原 |
| **09** | **Gemini** | **【煽情场景八·深夜陪伴】深夜床头·台灯守候** | 夜间 2800K 暖黄钨丝台灯光晕下，手办静立枕边深木柜，树脂次表面温润透光 | 利用 Gemini 暖黄低色温光影烘托，营造静谧深夜抚慰氛围 |
| **10** | **Gemini** | **【煽情场景九·时光重叠】老相册对话·立体相逢** | 置于翻开的泛黄老相册旁，年轻时的黑白历史照片与立体 3D 实体对视 | 利用 Gemini 双时空概念对比，精确实现平面老照片与立体的虚实对视 |

---

## 二、 底层长辈与亲人人物画像动态生成公式与去重引擎 (代际全景与动态公式版)

> **【架构演进与 30% 现代去世亲人核心契约】**：
> 本技能彻底废除旧版“静态固化 36 位人物”的硬编码模式，全面升级为**“时代现实主义底层长辈人物画像生成公式（Profiling Generative Formula）”**与**“知识库前置扫描动态去重引擎（Deduplication & Anti-Collision Engine）”**。
> 
> **调用契约**：
> - **默认批量生成**：当用户在会话中触发该技能时（如“给我生成人物画像”、“调用 fullskill”），系统依据公式默认输出 **20 个** 底层偏多的高情感张力长辈/亲人画像；
> - **【强制 30% 核心配额约束】2026年节点（近几年去世的 40～60 岁中年亲人）**：
>   - **生成的人物中必须有严格的 $30\%$ 配额（例如 20 人中占 6 位，10 人中占 3 位）归属于“2026年节点（即 2020~2026 年近几年因病、意外、劳累等猝然离世的亲人），去世年龄在 40～60 岁上下的中年亲人（中年失怙父母、中年丧偶夫妻、未享清福公婆岳父母）”**；
>   - 这一群体精准击中小红书 3D 打印手办最核心、痛感最深、转化率最高的情感定制诉求（“子欲养而亲不待”、“还没等孩子成家享福就走了”、“相濡以沫的爱人中年永诀”）；
> - **按需指定数量**：用户可通过自然语言指定生成数量 $N$（如“生成 10 个人物画像”、“来 5 个底层母亲画像”），引擎严格输出指定数量 $N$，并自动按 $30\%$ 比例分配 2026 年去世的中年亲人；
> - **动态去重保障**：每次生成前，引擎自动扫描本地 Obsidian 知识库目录 `/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/{char_dir}/`，自动计算已有最大编号并顺延分配，实行生计背景、信物、服饰色彩、骨相指纹的五重正交防撞过滤，确保全库资产绝无重复。

### 1. 时代现实主义土壤：底层长辈与体力劳动生计母池 (80年代~2026当代社会转型图景)

根据我国20世纪80年代计划经济向商品经济转型期的剧烈震荡（参考 `/Users/wuyongjia/Downloads/未命名.txt` 及其历史运行机制），并无缝延伸至 2026 年近几年的现代中国普通家庭生存图景，提炼出底层体力劳动与平民占比 $\ge 80\%$ 的八大生计阶层母池：

1. **【30% 核心配额】梯队 H：2026年节点·近几年（2020~2026）去世的中年亲人（享年 40~60 岁·父母/伴侣/公婆岳父母）**
   - **时代现实背景**：当代 80/90/00 后年轻人的中年父母、中年丧偶的爱人、或刚过五十岁积劳成疾的公婆岳父母。生于 60 年代末至 80 年代初，成长于改革开放，是托举现代中国城市化与家庭生计最辛劳的顶梁柱。在 2020~2026 年间因心脑血管突发、癌症重症（肺癌/肝癌/胃癌/乳腺癌）、长途或外卖交通意外、一线工地车间高负荷劳累倒下。
   - **核心痛点与情感张力**：“子欲养而亲不待”、“刚供完大学/刚帮孩子付完首付/刚抱上孙子就倒下了”、“没能享上一天清福”、“中年丧偶孤身带娃的思念”。
   - **生理与外貌质感（准年龄质感）**：严格还原 40~60 岁当代中年人风貌——两鬓黑发夹杂微霜（Salt-and-pepper hair）、额头深刻疲惫横纹、眼周暗沉但温厚的笑纹、常年劳累与看手机产生的略带微红血丝眼神、带薄茧手掌；**严禁出现高龄老人的满头白发或大面积老年斑**。
   - **现代平民服饰与信物**：深灰抓绒摇粒绒开衫、黑色耐磨防风冲锋衣、藏青轻薄羽绒马甲、超市买的碎花打底衫、老式牛仔裤、黄色/蓝色外卖骑行服；信物包含磨损货车车钥匙与满帮挂绳、摔裂外壳的老款智能手机、骑行头盔、记满开支的小记账本、生前织了一半的暗红羊绒围巾、夫妻戴了二十年的素金戒指。
2. **梯队 A：黄土地口粮维系者（种粮农户·祖辈/父母/老伴）**
   - **时代生计逻辑**：大包干薄田，三伏天顶烈日交公粮，怕粮站验收不合格退粮。日光暴晒酱紫色脸膛、老茧皲裂口子、发白千层底布鞋、腰别黄铜旱烟袋、洋瓷大茶缸、磨刀石。
3. **梯队 B：经济作物与大棚蔬菜先行户（凌晨钻营者·父母/公婆）**
   - **时代生计逻辑**：寿光早期大棚蔬菜户，借债买竹竿薄膜。凌晨两三点手电摘菜、加重二八大杠或平板车垛菜送城；掌指染满洗不掉的黄绿草汁泥水，车把绑着老铁壳手电筒与粗麻绳。
4. **梯队 C：初代进城务工劳力（自理口粮挑大梁者·父亲/母亲/年轻丈夫）**
   - **时代生计逻辑**：背井离乡无户口粮票买高价议价粮，工地扎钢筋/挑水泥、码头扛大包。怕查暂住证，分角毛票缝进贴身背心，满身水泥白痕，草绿解放鞋。
5. **梯队 D：走街串巷个体商贩与街头手艺人（街头营生·父母/爷爷/老伴）**
   - **时代生计逻辑**：沿街馄饨摊、早点油条摊、炒瓜子商贩、街头修车修伞补鞋配钥匙摊。生铁皮煤球炉、铸铁手摇修鞋机、黑布袖套、油渍找零腰包。
6. **梯队 E：国营与集体厂矿商贸底层劳力（车间与窗口·公婆/岳父母/老伴）**
   - **时代生计逻辑**：国营粮站过秤员（木杆秤与黑袖套）、副食店售货员（白围裙与木算盘）、车间翻砂工、锅炉工、煤矿井下工人（铝质饭盒与黑煤灰印）。
7. **梯队 F：家庭家政与底层护工（保姆皖嫂/医院护工·母亲/婆婆/老伴）**
   - **时代生计逻辑**：进城保姆（早期皖嫂、米脂婆娘）、医院熬夜翻身护工。常年接触洗洁精发红皲裂双手、素色碎花罩衫、发白塑料凉拖、便携小木针线盒。
8. **梯队 G：深情相伴与早逝追忆（老伴相濡以沫 / 80年代早逝妻子丈夫）**
   - **执手白头老伴**：守着薄田相濡以沫，共喝一碗热稀饭、戴了一辈子的粗银戒指、生前最后一张带老式暖水瓶的合影。
   - **80年代年轻早逝妻子丈夫**：80年代青年翻领蓝工装、的确良碎花衬衫、黑白结婚照笑容、纯棉手织婴儿小鞋与木制拨浪鼓。

---

### 2. 底层长辈与亲人人物画像动态生成公式 (Profiling Generative Formula)

人物画像由以下形式化函数确定性解构与概率生成：

$$\mathcal{P}_{\text{character}} = \text{ForgingFormula}\Big(\mathcal{K}, \mathcal{T}, \mathcal{Y}, \mathcal{E}, \mathcal{V}, \mathcal{M}, \mathcal{C}, \mathcal{A}, \mathcal{D}\Big)$$

#### 核心参数维度取值空间与概率偏置：

1. **【强制 30% 铁律】时代去世节点维度 $\mathcal{Y}$ (Era & Passing Anchor)**：
   - **【30% 核心红线】2026年节点（2020~2026 近几年去世的中年亲人，享年 40~60 岁）**：
     - 去世年份：2020 ~ 2026 年（当代年轻子女/伴侣的至亲）；
     - 年龄范围：严格锚定在 **40 ～ 60 岁**；
     - 角色细分：现代中年劳累父亲 ($40\%$)、现代操劳母亲 ($30\%$)、中年丧偶丈夫/妻子 ($20\%$)、初老未及享清福的公婆/岳父母 ($10\%$)；
     - 核心特征：现代平民衣着、现代高共鸣信物、中年自然生理微霜（非高龄白发）。
   - **【70% 常规配额】历史转型期与高龄留守亲人**：
     - 80~90 年代历史转型期底层劳力（种粮户、大棚蔬菜户、初代农民工、传统厂矿工人）；
     - 高龄长寿乡村留守祖辈与相伴一生老伴（65~85 岁）。
2. **代际亲缘维度 $\mathcal{K}$ (Kinship Category)**：
   - 权重分布：
     - **父辈代 (35%)**：父亲 (老爸)、母亲 (老妈)
     - **祖辈代 (30%)**：爷爷 (祖父)、奶奶 (祖母)、姥爷 (外公)、姥姥 (外婆)
     - **伴侣代 (20%)**：携手白头晚年逝去的老伴 (10%)；中年丧偶/青年早逝的爱妻或丈夫 (10%)
     - **姻亲代 (15%)**：公公、婆婆、岳父、岳母
3. **年龄与生理周期 $\mathcal{T}$ (Age & Physiological Stage)**：
   - `40 ~ 60 岁`（**强制占 30% 以上**）：2026年节点近几年去世的中年亲人（两鬓微霜、前额横纹、劳作老茧、眼神坚韧带微倦）；
   - `28 ~ 38 岁`：历史早逝年轻爱人/父母（的确良衬衫、青涩面容、生活微倦、眼神清澈含情）；
   - `65 ~ 85 岁`：高龄祖辈、长寿老伴（花白发髻/银白寸头、深长不对称鱼尾笑纹、自然淡老年斑、骨节粗大）。
4. **阶层生计维度 $\mathcal{E} \times \mathcal{V}$ (Grassroots Stratum & Vocation)**：
   - **底层体力与平民生计占比强制 $\ge 80\%$**，从上述 8 大梯队中采样，严禁悬浮富豪与动漫仙侠。
5. **五维生理解剖与岁月微瑕 $\mathcal{M}$ (5D Physiological & Imperfection)**：
   - **D1 骨相**：高颧骨、方正下颌、微隆眉弓、温和微凹眼窝、宽额头；
   - **D2 生理微瑕**：日光暴晒酱紫红脸膛、草汁绿泥印、两鬓微白斑驳、水泥发白指缝、眼角深长不对称鱼尾笑纹、局部自然微小毛孔。
6. **服饰色彩 DNA 正交互斥池 $\mathcal{C}$ (Wardrobe Color DNA)**：
   - 现代平民与历史工装：深灰摇粒绒开衫、黑色耐磨防风冲锋衣、藏青轻薄羽绒马甲、军绿涤卡夹克、藏青中式斜襟衫、姜黄手工粗毛线衣、深蓝工字背心、暗红斜襟袄、的确良衬衫。色彩在全局正交互斥。
7. **终身专属情感信物全局独占池 $\mathcal{A}$ (Signature Artifact Monopoly Pool)**：
   - **核心契约：一人一物，终身唯一！**
   - 磨损货车车钥匙与挂绳、老款摔裂屏手机、骑行头盔、手写记账本与医保卡、生前织了一半的毛衣、素圈金戒、老木杆秤、木柄旧木锨、黄铜旱烟杆、铸铁修鞋机、包浆桑木扁担、粗线团与牛骨顶针等。
8. **神态动态基线与小红书爆款母题 $\mathcal{D}$ (Expression & Xiaohongshu Narrative Motifs)**：
   - 眯眼慈祥笑意、专注低头劳作、眺望远方的守候、眼眶微红的不舍、相濡以沫的微光。

---

### 3. 本地知识库去重逻辑与六重正交防撞防御机制 (Deduplication Engine)

为彻底杜绝人设同质化、道具撞车与资产文件覆盖，引擎在每次执行生成时，必须严格执行以下去重流水线：

```
[触发画像生成请求 (默认20 / 指定N)]
               │
               ▼
[Step 1: 前置全量扫描知识库根目录]
扫描路径: /Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/
               │
               ▼
[Step 2: 提取最大编号 MAX_ID 与顺延自增]
自动计算已有 max(ID)，新批次起始编号从 MAX_ID + 1 顺延递增
               │
               ▼
[Step 3: 构建“已占有属性注册表 (Occupied Attribute Registry)”]
解析所有已存在目录的 character_profile.md:
- 注册信物池 (Occupied Artifacts)
- 注册色彩池 (Occupied Wardrobe Colors)
- 注册生计职业池 (Occupied Vocations)
- 注册人物指纹 Token 池 (Occupied IFTS)
               │
               ▼
[Step 4: 基于公式动态生成候选画像，并通过六重正交防御门禁过滤]
├─ 门禁 1: 专属信物 100% 绝对独占 (若撞车则重新采样生成)
├─ 门禁 2: 服饰主辅色彩 100% 正交互斥 (严禁撞衫)
├─ 门禁 3: 同一代际同类生计场景互斥度 < 40% (杜绝同代同职业撞车)
├─ 门禁 4: 15~20 词 IFTS 语义 Jaccard 相似度 < 0.35 (防脸谱化)
├─ 门禁 5: 【强制】30% 现代 2026 节点 40~60 岁去世中年亲人配额校验门禁
└─ 门禁 6: 姿态与规格约束 (BW/BM 6.0cm, FW/FM 12.0cm 强制 full-body)
               │
                │
                ▼
[Step 5: 格式化输出 N 个合规画像卡] ➔ 必须全量落盘三份核心资产文件 (零缩水交付，少一个视角判定为 Blocker)
```

- **物理存储标准契约 (阿里规约标准接口)**：
  - **知识库目录 (Obsidian)**：`/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/{char_dir}/`
    1. `character_profile.md`：五维人物深度铸造画像卡 (包含 D1~D5、生计图景与信物)
    2. `prompts.md`：**【全量交付刚性契约】视角 00 到 视角 10 全部 11 个视角**，含 00➔01 差异对齐表与中文场景说明，绝不允许抽样、缩写或截断！
    3. `prompts.json`：结构化存储 11 个视角的 raw_prompt 数组与 IFTS 唯一指纹，严禁内部代码泄漏！
    4. **【绝对红线禁令】严禁生成任何 `小红书文案.md`**，职责完全解耦至下游文案技能！
  - **纯图片存储目录 (3D打印本地驱动)**：`/Users/wuyongjia/3D打印/素材/{char_dir}/`（仅存放纯图片，如 `00_candid.jpg`, `01_model.jpg` 等）

---

### 4. 动态生成标杆级 20 人画像全景对照表 (公式实测输出范例 · 顺延 char_21 ~ char_40)

> **【去重与 30% 现代配额校验说明】**：
> 本地知识库当前已存在 `char_01` ~ `char_20`（已有 19 个目录，最大编号为 20）。
> 本批次 20 位底层长辈亲人画像严格从 **`char_21` 顺延至 `char_40`**，底层体力与平民占比 **$85\%$**：
> - **前 6 位（`char_21` ~ `char_26`，占比整整 $30\%$）**：严格锚定为 **“2026年节点（2020~2026近几年去世），享年 40～60 岁上下的现代中年亲人”**；
> - **后 14 位（`char_27` ~ `char_40`，占比 $70\%$）**：覆盖 80~90 年代历史转型期底层劳力与高龄留守祖辈、相伴一生老伴；
> - 信物与服饰色彩与已有库 100% 正交互斥：

| 编号与规范目录名 | 身份角色与年龄 | 时代背景与生计图景 (含30%现代配额) | 外貌与服饰 DNA (正交互斥) | 终身专属情感信物 (独占) | 规格与推荐场景 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **char_21_BM_2026近几年跑货运心梗离世的52岁客运货车父亲** | 52岁 父亲 (2024年逝) | 【30%现代配额】常年奔波高速，为了还车贷房贷，2024年底在货车驾驶室突发心梗离世 | 黝黑粗犷方脸、两鬓黑发夹微霜、前额深刻疲惫纹、水洗深灰耐磨防风夹克 | 磨损的货车车钥匙（带满帮货运挂绳）与划痕不锈钢保温杯 | 胸像 6.0cm / 书房多宝阁、玄关守望 |
| **char_22_BW_2026近几年刚供出大学生积劳重病早逝的49岁坚韧母亲** | 49岁 母亲 (2025年逝) | 【30%现代配额】起早贪黑打两份工，孩子刚大学毕业找到工作，2025年因积劳成疾病逝 | 温和圆脸、微卷短发泛微白、眼周疲惫但慈爱、深藏青轻薄抓绒摇粒绒开衫 | 记满为孩子攒学费与房贷明细的皱巴小记账本与旧款红米手机 | 胸像 6.0cm / 掌心凝视、深夜床头 |
| **char_23_BM_2026近几年雨夜送外卖车祸早逝的44岁青年丈夫(追忆)** | 44岁 丈夫 (2023年逝) | 【30%现代配额】中年丧偶，为了家庭生计拼命抢单，2023年冬雨夜送餐因意外离世，留下一生思念 | 浓眉黑发、疲惫但坚毅的目光、黄色防风防雨骑行夹克、耐磨工装裤、运动鞋 | 摔出裂痕的黄色外卖骑行头盔与屏幕带细碎裂纹的旧智能手机 | 胸像 6.0cm / 老相册对话、掌心捧握 |
| **char_24_BW_2026近几年患癌症早逝操劳一生的47岁爱妻(追忆)** | 47岁 妻子 (2024年逝) | 【30%现代配额】中年丧妻，省吃俭用操持全家，刚帮家里换了大房子，2024年秋因癌症离世 | 清瘦脸庞、齐肩挽发微斑白、温柔释然的含笑眼眸、素雅米白针织毛衣 | 结婚时买的细素金戒指与生前给孩子织完的最后一件暗灰羊线围巾 | 胸像 6.0cm / 深夜台灯、时光重叠 |
| **char_25_BM_2026近几年严寒抢修农田电路突发心衰的58岁公公** | 58岁 公公 (2025年逝) | 【30%现代配额】乡镇供电所老水电工，2025年冬顶着暴风雪一线抢修农田水泵突发心衰猝逝 | 风霜红铜色深肤质、深眼窝、老茧双手、深蓝加厚帆布电力工作服 | 磨损包胶绝缘电工钳与带挂绳的老款折叠金属老花镜 | 胸像 6.0cm / 岁月手艺、专属老座 |
| **char_26_FW_2026近几年帮女儿带娃劳累突发脑溢血的54岁岳母(全身)** | 54岁 岳母 (2023年逝·全身) | 【30%现代配额】进城帮小两口看娃起早贪黑，做饭洗衣服，2023年突发脑溢血在医院病逝 | 慈眉笑眼、银白发箍、深枣红暗花薄羽绒棉服、深色长裤、软底健步鞋 | 挂在脖颈上的红绳小塑料防走失口哨与折叠老花镜 | 全身 12.0cm / 灶台烟火、掌心托举 |
| **char_27_BM_交三伏公粮的种粮户老父亲** | 54岁 父亲 (80s时代) | 黄土地种粮户，三伏天顶烈日排长队交公粮，怕粮站退粮 | 酱紫日光暴晒脸膛、汗湿白头老汗衫、腰扎粗布带、旧千层底布鞋 | 木柄旧木锨与印着红字的粗麻粮袋 | 胸像 6.0cm / 专属老座、人间烟火 |
| **char_28_BM_凌晨踩加重大杠运菜的大棚蔬菜父亲** | 52岁 父亲 (80s时代) | 寿光早期大棚蔬菜户，借债薄膜竹竿，凌晨手电摘菜运城 | 手指染满洗不掉的黄绿草汁泥水、深灰水洗涤卡夹克、粗布裤 | 绑在二八大杠车把上的老铁壳手电筒与粗麻绳 | 胸像 6.0cm / 书房多宝阁、掌心凝视 |
| **char_29_BM_工地扎钢筋挑水泥的初代打工老父亲** | 50岁 父亲 (80s时代) | 初代进城农民工（自理口粮），高空手扎钢筋、挑水泥 | 额头深抬头纹、水泥发白指缝老茧、洗褪色军绿帆布工装 | 缝在贴身背心内侧装分角毛票的小红布包 | 胸像 6.0cm / 玄关守望、岁月手艺 |
| **char_30_BW_走家串巷当保姆起早贪黑的皖嫂母亲** | 49岁 母亲 (80s时代) | 80年代末进城务工家政保姆（皖嫂），照顾雇主老幼 | 齐耳碎发、常年洗洁精接触发红微皲双手、洗旧深藏青碎花罩衫 | 随身携带的小木头针线盒与折叠小剪刀 | 胸像 6.0cm / 掌心凝视、深夜床头 |
| **char_31_BW_早起推石磨做热豆腐的坚韧母亲** | 53岁 母亲 (80s时代) | 农村起早贪黑磨豆腐小作坊，推石磨风雨无阻 | 蓝粗布包头、素色洗白棉袄、围裙带微量白豆渣微痕 | 用了三十年、把手包浆光亮的老铜汤勺 | 胸像 6.0cm / 灶台烟火、时光重叠 |
| **char_32_FM_街头修鞋修伞配钥匙的质朴老父亲** | 56岁 父亲 (全身) | 早期街头个体手艺人，蹲守街角修补鞋伞，自食其力 | 围深黑磨损老皮围裙、指节粗黑带油印、草绿解放鞋 | 铸铁手摇修鞋机与装满老式钥匙胚的木工具箱 | 全身 12.0cm / 岁月手艺、玄关守望 |
| **char_33_FW_在厂矿食堂窗口打菜的勤劳母亲** | 51岁 母亲 (全身) | 国营老机械厂职工食堂窗口打菜员，勤勉热心 | 戴白棉工作帽、藏青耐磨棉工服、挽黑色防油套袖、防滑胶靴 | 边缘磕碰掉漆的铝制长柄打菜大铁勺与饭票盒 | 全身 12.0cm / 人间烟火、掌心托举 |
| **char_34_BM_黄土地上挥镰割麦相伴一生的老伴** | 71岁 伴侣老汉 (相伴) | 守着老家几亩薄田相濡以沫的老汉，一辈子没吵过架 | 深刻刀刻般风霜皱纹、酱红肤色、洗得泛白青布短褂、旧草帽 | 挂在腰间麻绳上的粗面磨刀石与黄铜旱烟袋 | 胸像 6.0cm / 专属老座、掌心捧握 |
| **char_35_BW_煤油灯下纳千层底鞋垫的老伴** | 69岁 伴侣老伴 (相伴) | 一辈子操持家务、给老伴做鞋做饭的老妻，温良慈和 | 银白发髻、慈祥笑眼、深棕盘扣棉袄、老式玳瑁花镜 | 磨损发亮的深色牛骨顶针与缠着红线的粗麻线团 | 胸像 6.0cm / 深夜台灯、时光重叠 |
| **char_36_BM_码头挑扁担扛大包的倔强爷爷** | 73岁 爷爷 (祖辈) | 长江老码头装卸搬运工，挑千斤重担供出家中第一个大学生 | 宽厚黑铜色肩膀带凸起硬茧、两鬓银白寸头、洗旧工字老汗衫 | 磨出深红油亮包浆的老桑木扁担与防滑粗麻绳 | 胸像 6.0cm / 岁月手艺、掌心凝视 |
| **char_37_BW_在土灶前拉风箱烧柴火的慈祥奶奶** | 75岁 奶奶 (祖辈) | 乡村老土灶台前烟熏火燎一辈子的乡村老人，饭菜永远滚烫 | 满头银发盘在脑后、微驼背脊、洗褪色深紫红粗布斜襟衫 | 祖传老木头风箱把手与雕花老式锡茶叶罐 | 胸像 6.0cm / 灶台烟火、专属老座 |
| **char_38_BM_挑几十里山路给外孙送红薯的姥爷** | 74岁 姥爷 (外祖) | 深山质朴老农，每年秋收徒步几十里山路给城里外孙送特产 | 稀疏花白头发、高额头、汗渍微黄的土白布对襟衫、卷裤腿 | 竹编老扁担双箩筐与洗得掉色的旧黄帆布军挎包 | 胸像 6.0cm / 书房多宝阁、窗台晨曦 |
| **char_39_BW_在打麦场摇蒲扇给娃驱蚊的姥姥** | 72岁 姥姥 (外祖) | 麦场看场老人，夏夜星空下摇着蒲扇给儿孙讲民间老故事 | 慈眉笑眼、齐耳花白短发、暗青提花棉布短袄、深蓝长裤 | 包了红布边角的老式大蒲葵扇与清凉油小铁盒 | 胸像 6.0cm / 午后空椅、时光重叠 |
| **char_40_FM_风雨中推平板车给小家拉蜂窝煤的父亲** | 53岁 父亲 (全身) | 城市棚户区老父亲，冬天冒雨雪给全家拉蜂窝煤炉取暖 | 满身黑煤灰微斑、旧军大衣腰系麻绳、湿透高帮防滑雨靴 | 磨损沉重的铸铁蜂窝煤火钳与带老伤疤的手拉车把套 | 全身 12.0cm / 玄关守望、掌心凝视 |

---

## 三、 开源仓库与权威参数参考体系与六步法构建协议

为确保提示词工程的工业级稳定性与学术级严密性，本技能全面参考并内化了开源社区前沿视觉生成工程与官方参数的最佳实践：
1. **核心参考规范一：《Midjourney V8.x 核心参数与高级指令全景说明》**
   - **文档路径**：`/Users/wuyongjia/obsidian-gitee/technology/🧰 AI工具/midjourney/Midjourney V8.x 核心参数与高级指令全景说明.md`；
   - **参考精髓**：生成 Midjourney 提示词时必须严格对照该文档。深度对齐 V8.x 画面宽高比（`--ar 1:1`）、算力深度（`--q 1/2`）、超清模式（`--hd`）、风格化区间（`--s 80` 写实 / `--s 50` 手办低自由度）、原始风格（`--style raw`）、排他性负向（`--no`）以及跨视角一致性全能参考（`--oref` / `--cref`）与随机种子（`--seed`）全景参数规范；
2. **GitHub 核心参考仓库二：[Open-Generative-AI (Anil-matcha/Open-Generative-AI)](https://github.com/Anil-matcha/Open-Generative-AI)**
   - **参考精髓**：[Awesome-GPT-Image-2-API-Prompts](https://github.com/Anil-matcha/Awesome-GPT-Image-2-API-Prompts) 提炼的“电影级真实胶片人像分层架构（Film Grade Portrait Layering）”，即通过明确的胶片银盐规格（`35mm film / Kodak Portra 400`）、多光源环境混合（`harsh fluorescent + warm neon / diffused daylight`）、生理微瑕微距还原（`subtle skin texture and micro pores, natural double eyelids`）以及高保真色彩微偏（`slight color cast, authentic film grain`），彻底剥除 AI 生图的塑料感；
3. **GitHub 核心参考仓库三：[Generative-Media-Skills (SamurAIGPT/Generative-Media-Skills)](https://github.com/SamurAIGPT/Generative-Media-Skills)**
   - **参考精髓**：[nano-banana 视觉推理驱动技能](https://github.com/SamurAIGPT/Generative-Media-Skills/blob/main/library/visual/nano-banana) 奠定的“推理驱动结构化简报（Reasoning-Driven Creative Brief: The Perfect Prompt Formula）”：
     $$\text{Prompt} = \text{Subject} + \text{Action} + \text{Context} + \text{Composition} + \text{Lighting} + \text{Style}$$
     以及该仓库在角色连续性设计中的 **Identity Consistency 契约**（`Maintain consistent facial structure across variations`），明确要求通过语义指纹 Token 的强一致性约束，解决跨视角角色变形与人脸崩塌问题。

### 提示词标准化构建六步法流水线 (6-Step Prompt Construction Protocol)

在每次执行人物提示词生成时，必须严格执行以下六步构建流程：

```
Step 1: 【五维铸造与指纹提取】➔ 提炼 15~20 词唯一性指纹序列 (IFTS)
Step 2: 【动作姿态与全身锁定】➔ 定义生活抓拍或手办站姿；若为全身人物强制包含 full-body
Step 3: 【环境拓扑与多光源混合】➔ 真实生活居室光影 / 浅灰纯净天幕
Step 4: 【光学镜头与景深标定】➔ 视平线中画幅 f/3.2 纪实 / 微距全焦 f/8 影棚
Step 5: 【材质物性与胶片质感注入】➔ Kodak Portra 400 银盐 / 树脂微透光 SSS
Step 6: 【负向拦截与 V8 参数精控】➔ 严格对照参数文档挂载 --ar 1:1 --style raw --s 80/50 --v 8 --no
```

1. **Step 1: 五维铸造与指纹提取 (Subject & Identity Fingerprint)**：
   - 严禁模糊代称！以五维铸造卡为依据，提取包含骨相、笑纹、发型、配饰的 IFTS 核心指纹序列，作为提示词的不可变核心；
2. **Step 2: 动作姿态与全身锁定 (Action, Pose & Full-Body Constraint)**：
   - 参考 Nano-Banana 的 Action 规范：00 视角指定真实生活动作（如站在砧板前切葱花、握着菜篮把手、扶着老花镜），01 视角统一约束为正面 0° 挺立/坐姿雕塑形态；
   - **【强制】全身人物 full-body 锚定**：凡是全身人物（FW/FM 或全身构图），生成的提示词必须显式包含 **`full-body`** 词条（如 `full-body portrait`, `full-body shot`, `12.0cm 3D printed painted resin full-body model`, `full-body view`），锁定全身比例；
3. **Step 3: 环境拓扑与多光源混合 (Context & Mixed Lighting)**：
   - 参考 GPT-Image-2 的多光源物理混合：00 视角组合窗外柔和晨光与居室暖调；01 视角统一为浅灰无缝影棚天幕（`light gray cyclorama`）配合双侧柔光箱（`softbox lighting`）；
4. **Step 4: 光学镜头与景深标定 (Composition & Optics)**：
   - 00 视角锁定哈苏中画幅 90mm f/3.2 纪实浅景深；01 视角锁定佳能 RF 100mm f/8 微距全景深正交机位，确保手办边缘锐利清晰、无透视畸变；
5. **Step 5: 材质物性与胶片质感注入 (Material & Film Texture)**：
   - 00 视角注入真实老人皮脂与胶片银盐颗粒（`Kodak Portra 400 film grain`）；01 视角注入嘉立创光敏树脂哑光质感与次表面散射（`subtle resin SSS finish`）；
6. **Step 6: 负向拦截与 V8 参数精控 (Negative Filtering & Midjourney V8 Parameter Control)**：
   - **严格遵循《Midjourney V8.x 核心参数与高级指令全景说明》文档标准**；
   - 00 视角挂载 `--ar 1:1 --style raw --s 80 --v 8 --no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands`；
   - 01 视角挂载 `--ar 1:1 --style raw --s 50 --v 8 --no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`；
   - 商用高精定稿推荐挂载 `--q 2` 或 `--hd`；跨视角主体一致性衍生推荐挂载 `--oref <URL> --ow 100~300` 或 `--cref <URL> --cw 100`。

---

## 四、 双引擎标杆级黄金提示词工程示例 (以厨房外婆为例)

> [!IMPORTANT]
> - **先铸造、后出词**：每个人物必须先完成《五维铸造画像卡》，并提取 `identity_fingerprint_tokens` (IFTS)；
> - **视角 00 & 视角 01【Midjourney 专属】**：单段连贯流，尾部挂载 `--ar 1:1 --style raw --s ... --v 8 --no ...`，严格遵循 **50 ～ 70 词高信噪比硬上限**，严禁任何内部代码与自残负向词；
> - **00 ↔ 01 指纹序列 100% 逐字对齐**：00 与 01 必须 100% 逐字复用提取出的 IFTS 指纹序列，确保同一个长辈的骨相与神态绝对统一；
> - **视角 02 ～ 视角 10【Gemini (Imagen 3) 专属】**：纯英文自然语言分层描述（主体+空间嵌套+环境+光影镜头），**严禁出现 Midjourney 的 CLI 命令行参数（无 `--ar`, 无 `--v 8`, 无 `--style raw`, 无 `--no`）**，尾部以自然语言 `Avoid: ...` 进行负向拦截；
> - **零资产代码泄露**：全量提示词绝对不包含任何本地目录命名（如 `char_XX_XX`、`BW` 等私有代号）。

### 0. 厨房外婆五维深度铸造画像卡产物 (落地至 character_profile.md)

```markdown
## 五维人物深度铸造画像卡 (5D Character Forging Card)
- **人物编号与代号**：char_01_BW (厨房忙碌慈祥外婆)
- **年龄与定位**：72 岁中国南方普通家庭外婆，操劳半生，灶台前的守护者
- **D1 面部骨相指纹**：微凸饱满圆颧骨（Rounded cheekbones），柔和微方下颌骨（Soft square jawline），平缓眉弓，温和下垂的眼窝走向
- **D2 生理微瑕签名**：深长不对称眼角鱼尾笑纹（Asymmetric deep crow's feet），左颊略深于右颊的自然法令纹，右太阳穴下方两处浅褐老年斑（Natural age spots），微小自然毛孔与温和皮脂
- **D3 服饰色彩 DNA**：深藏青色（Navy blue）斜襟中式布衫，手工一字织物盘扣（Frog buttons）；外系洗旧浅灰细碎小碎花棉布围裙（Floral cotton apron）
- **D4 随身信物锚定**：耳垂佩戴直径约 1.5cm 光滑素银小圆圈耳环（Silver hoop earrings）；常年佩戴老花镜，灶台前置于胸前围裙大口袋
- **D5 神态动态基线**：眯眼慈祥微笑（Crinkling smile eyes），嘴角微微上扬含蓄而温暖，眼神聚焦在眼前热气腾腾的家常饭菜上
```

### 1. 提炼出的唯一性指纹 Token 序列 (IFTS · 写入 prompts.json)
> **IFTS 统计**：共 18 个英文单词，完整涵盖年龄身份、骨相、笑纹、老年斑、发髻与素银耳饰。视角 00 与 01 必须 100% 逐字原样复用：
```text
72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings
```

---

### 视角 00：【基底定妆照】真实长辈生活写实摄影 (正脸半身) · 【Midjourney 专属】
> **信噪比与指标**：正向 46 词（完整嵌入 18 词 IFTS），负向 14 词，总词数 69 词。完全符合 50 ～ 70 词黄金敏感区间，彻底解决过长告警，精确锁定中国真实厨房外婆面容与生活光影。
```text
Candid documentary portrait of a real 72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings, in kitchen, wearing navy frog-button tunic with floral apron, soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
```

### 视角 01：【模型标准像】0° 正面微缩手办棚拍 (依靠 00 微调成 3D 模型标杆版) · 【Midjourney 专属】
> **微调衍生原则**：直接以视角 00 提示词为基底，通过四大微调置换算子转化成 3D 模型；**100% 逐字继承 18 词 IFTS 指纹序列**；正向 47 词，负向 15 词，总词数 66 词。
```text
Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, 72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings, sculpted navy frog-button tunic with floral apron, mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
```

#### 🔍 视角 00 ➔ 视角 01 微调置换与 IFTS 一致性对齐表 (Prompt Mutation Diff)
| 维度类别 | 视角 00 原文 Token (写实原片) | 视角 01 微调 Token (3D 模型) | 继承与微调对齐机制 |
| :--- | :--- | :--- | :--- |
| **主体媒介** | `Candid documentary portrait of a real` | `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust,` | 算子 ① 置换：显式声明 3D 打印树脂胸像，剥离摄影定性 |
| **人物唯一性指纹 (IFTS)** | `72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings` | `72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings` | **100% 逐字绝对原样继承（0 差异）**，锁定骨相神态，杜绝跨模型人脸漂移 |
| **服装信物** | `wearing navy frog-button tunic with floral apron` | `sculpted navy frog-button tunic with floral apron` | 算子 ② 微调：保留色彩款式，仅在服饰前追加 `sculpted` 声明雕塑化 |
| **环境底座** | `in kitchen, soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain` | `mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus` | 算子 ③ 置换：厨房居室置换为深色微倒角工艺品底座、树脂 SSS 质感与正交微距全焦 |
| **参数配比** | `--s 80` | `--s 50` | 算子 ④ 调控：手办降噪控制风格化发散度，压制 AI 自由重绘面部 |
| **负向拦截** | `--no anime, 3d render, CGI, doll, figurine, plastic skin...` | `--no real living human, skin pores, plaster, stone column...` | 算子 ④ 置换：剔除 3D 拦截词，反向针对性拦截活人与石膏柱 |

### 视角 02：【煽情场景一·专属老座】午后空椅·日光守望 · 【Gemini 专属】
```text
A poignant, emotionally resonant documentary photograph of the miniature 6cm 3D printed full-color photopolymer resin bust figurine of the smiling Chinese kitchen grandmother with navy floral apron and silver hair bun, placed tenderly on a weathered wooden side table in an old-fashioned Chinese home living room. Right beside the figurine sits an authentic vintage chipped green enamel tea mug and a pair of folded reading glasses. In the soft-focus middle ground stands an empty traditional hand-woven wicker rocking armchair with gentle signs of decades of loving use. Warm 3:30 PM golden afternoon sunlight slants through a classic wooden lattice window, creating gentle dancing Tyndall dust motes in the air and casting soft warm highlights on grandmother's smiling resin face with glowing subsurface scattering (SSS), evoking deep domestic nostalgia and the comforting feeling that she has only stepped away for a moment. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic 35mm Kodak Portra 400 analog film tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 03：【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀 · 【Gemini 专属】
```text
A dignified, emotionally resonant domestic documentary photograph of the miniature 6cm 3D printed full-color resin bust figurine of the smiling Chinese kitchen grandmother with navy floral apron and silver hair bun, respectfully placed on the middle-to-upper tier of an elegant dark rosewood curio display shelf (duobaoge) inside a quiet family study room. The shelf height is positioned exactly at eye level, offering a serene, reverent line of sight for daily remembrance. Right beside the figurine rests an authentic vintage chipped green enamel tea mug and a small polished brass seal. Soft warm 3000K museum-grade interior spotlighting gently glints off the polished hardwood grain and partially illuminates grandmother's gentle smiling face with delicate amber resin subsurface scattering (SSS), creating an aura of dignified family reverence, eternal respect, and quiet comforting remembrance. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, delicate shadows, authentic Kodak Portra 400 analog tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 04：【煽情场景三·岁月手艺】旧物深情·生锈时光 · 【Gemini 专属】
```text
A deeply nostalgic still-life documentary photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese grandmother placed affectionately upon an authentic vintage 1970s black cast-iron foot-treadle sewing machine table with distressed wooden surface and aged lacquer patina. Beside the figurine rests a vintage wooden spool of weathered red cotton thread, an antique pair of steel sewing scissors with subtle rusted spots, and a faded floral thimble. Afternoon natural window sunlight glints off the polished iron wheel and highlights the delicate matte polymer finish and loving smile lines of the grandmother, evocative of decades of humble craftsmanship, motherly devotion, and unforgotten domestic warmth. Shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/3.5, rich tactile textures of aged iron, peeling wood, and SSS resin, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 05：【煽情场景四·晨曦静好】窗台花草·微风晨光 · 【Gemini 专属】
```text
A serene, highly healing interior photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese kitchen grandmother standing peacefully on an aged natural wooden windowsill in a sun-drenched home balcony. Beside the tiny figurine sits a flourishing green potted clivia plant with broad glossy leaves in a celadon ceramic pot, and a gentle morning breeze lightly billows a sheer white linen curtain. Golden 6:30 AM dawn sunlight streams through creating delicate Tyndall sunbeams with tiny dancing dust particles, soft luminous golden backlight illuminates grandmother's silver hair and creates a gentle translucent SSS amber glow through the resin cheek contours, breathing pure peaceful serenity and eternal quiet love. Shot on Hasselblad X2D 100C with 90mm f/2.8 lens at f/2.8, creamy background bokeh, authentic Kodak Portra 400 film tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 06：【煽情场景五·风雨归人】玄关守望·长明灯与老钥匙 · 【Gemini 专属】
```text
An intensely touching, comforting domestic documentary photograph of the 6cm miniature 3D printed full-color resin bust figurine of the Chinese kitchen grandmother, standing peacefully upon a dark solid walnut entryway shoe cabinet beside the front door. Right beside the figurine lies a well-worn keyring with brass house keys polished smooth by decades of handling, and a small yellowed memo paper with affectionate handwritten Chinese characters reading 'Dinner is in the pot, eat while it is warm'. A gentle 2700K warm incandescent wall sconce above casts a soft golden cone of light, warmly illuminating grandmother's gentle smile and creating soothing amber resin translucency (SSS) and a gentle elongated shadow on the wooden surface, symbolizing the eternal comfort of someone always keeping a light on for you upon returning home. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, cozy evening atmosphere, authentic Kodak Portra 400 analog grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 07：【煽情场景六·掌心凝视】掌心凝视·思念具象 · 【Gemini 专属】
```text
A deeply touching candid lifestyle photograph of an adult Chinese grandchild's warm cupped hands gently holding the 6cm miniature full-color 3D printed resin bust figurine of their beloved late Chinese grandmother wearing a navy floral apron and silver hair bun. The tiny figurine rests comfortably in the center of the palm, creating an emotional scale contrast between real human palm skin textures and the intricate 6cm miniature resin craft. Soft emotional natural daylight streams through a domestic living room window, with a shallow depth of field and a warm cozy blurred home interior, nostalgic affectionate color grading, authentic emotional resonance, quiet remembrance. Shot on Canon EOS R5 with RF 85mm f/1.4 lens at f/2.8, authentic 35mm Kodak Portra 400 film grain, natural shadows. Avoid: anime, cartoon, 3d digital render, CGI, distorted human fingers, extra fingers, missing fingers, creepy atmosphere, eerie smile, caucasian, western features, harsh flash, plastic skin.
```

### 视角 08：【煽情场景七·生活遗存】人间烟火·灶台重逢 · 【Gemini 专属】
```text
A poignant, deeply nostalgic documentary still-life photograph of the 6cm miniature 3D printed full-color bust figurine of the Chinese kitchen grandmother wearing a navy floral apron and silver hair bun, placed tenderly on a weathered wooden cutting board on an old kitchen countertop. Beside the tiny figurine sits a vintage stainless steel soup pot with a faint wisp of rising steam, a worn wooden rolling pin, and an antique floral porcelain bowl with a pinch of white flour. Golden morning sunbeams cut through kitchen window blinds, illuminating tiny floating dust particles, casting long warm shadows, evoking rich domestic nostalgia and a sense of eternal loving presence. Shot on Canon EOS R5 with RF 50mm f/1.8 lens at f/2.8, rich atmospheric depth, Kodak Portra 400 film tone. Avoid: anime, cartoon, 3d digital render, CGI, messy clutter, harsh flash, exaggerated steam, shiny plastic, caucasian, western features, artificial gloss.
```

### 视角 09：【煽情场景八·深夜陪伴】深夜床头·台灯守候 · 【Gemini 专属】
```text
A quiet, comforting nighttime interior photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese kitchen grandmother standing peacefully on a dark solid wood bedside nightstand. Beside the figurine rests a warm 2800K tungsten gooseneck bedside reading lamp, an open vintage book, and a retro brass mechanical alarm clock. Warm golden lamplight gently kisses the side of the grandmother's smiling resin face, creating soft glowing subsurface scattering (SSS) highlights and gentle comforting shadows across the wood grain, evoking a soothing atmosphere of grief solace, silent eternal love, and tranquil remembrance. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, delicate shadow details, Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, creepy dark shadows, blown out lamp highlights, harsh noise, digital glow, caucasian, western features, plastic skin.
```

### 视角 10：【煽情场景九·时光重叠】老相册对话·立体相逢 · 【Gemini 专属】
```text
An emotionally resonant, nostalgic macro photograph showing the miniature 6cm full-color 3D printed bust figurine of the Chinese grandmother placed affectionately right beside an opened vintage 1980s cloth-bound photo album. In the album, a slightly faded, yellowed black-and-white corner-mounted photograph shows the same Chinese grandmother in her 30s standing in an old courtyard. The modern 3D miniature bust figurine and the flat historical photograph gaze toward each other, creating a powerful juxtaposition of flat memory transforming into tangible 3D reality, soft natural afternoon window light, gentle dust motes, rich tactile paper and resin textures, bittersweet nostalgia, tangible love across time. Shot on Canon EOS R5 with RF 85mm f/2 Macro lens at f/3.2, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, modern digital photo album, oversaturated colors, distorted hands, harsh flash, caucasian, western features, plastic skin.
```

---

### 4.2 父辈/公婆代标杆级提示词工程示例 (以 52 岁长途客运老爸 char_21_BM 为例)

> [!IMPORTANT]
> - **父辈生理特征**：52 岁中年父亲，绝不照搬高龄老人白发苍苍与大面积老年斑；
> - **精准微瑕**：两鬓黑发微霜（Salt-and-pepper hair at temples）、额头抬头横纹与眼角深细笑纹（Weathered laugh lines）、疲惫但坚毅的眼神、粗糙带茧手掌；
> - **00 ↔ 01 IFTS 100% 逐字继承**：00 与 01 视角严格 100% 复用 17 词 IFTS 指纹序列；
> - **信噪比与词数**：正向 45~48 词，总词数 65~68 词，彻底消除 `Long Prompt` 告警。

#### 0. 52岁客运老爸五维深度铸造画像卡 (落地至 character_profile.md)
```markdown
## 五维人物深度铸造画像卡 (5D Character Forging Card)
- **人物编号与代号**：char_21_BM (长途客运奔波的质朴老爸)
- **年龄与定位**：52 岁中国普通家庭长途客运司机父亲，寡言少语，用双手方向盘撑起全家
- **D1 面部骨相指纹**：方正粗犷下颌骨（Square rugged jawline），微隆眉弓，略显深陷的坚毅眼窝走向
- **D2 生理微瑕签名**：常年长途驾驶留下的眼角深刻风霜笑纹（Weathered laugh lines）、前额岁月浅横纹、两颊微红血丝风霜肤质，黑发短发中两鬓微霜（Salt-and-pepper cropped hair）
- **D3 服饰色彩 DNA**：水洗做旧深灰棉帆布工装夹克（Faded dark charcoal canvas jacket），内搭朴素浅灰棉质内衬，磨损深棕皮革腰带
- **D4 随身信物锚定**：挂在腰间的磨损黑皮革钥匙包（Worn black leather keyring pouch），随身携带的划痕双层不锈钢保温杯（Stainless steel thermos）
- **D5 神态动态基线**：略带长途奔波疲惫但内敛温厚的坚韧目光（Tired resilient eyes），嘴角微微含笑，凝望儿女
```

#### 1. 提炼出的 17 词唯一性指纹 Token 序列 (IFTS · 写入 prompts.json)
```text
52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn leather keyring
```

---

#### 视角 00：【基底定妆照】真实父亲生活写实摄影 (正脸半身胸像) · 【Midjourney 专属】
> **信噪比指标**：正向 47 词（完整嵌入 17 词 IFTS），负向 14 词，总词数 68 词。精准锁定当代中国 50 岁出头勤劳坚毅老爸形象。
```text
Candid documentary portrait of a real 52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key, resting near highway truck stop, wearing dark charcoal canvas jacket, soft overcast morning daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
```

#### 视角 01：【模型标准像】0° 正面微缩手办棚拍 (依靠 00 微调成 3D 模型) · 【Midjourney 专属】
> **微调置换原则**：首句声明 3D 模型实体，**100% 逐字原样继承 17 词 IFTS 序列**，服装前追加 `sculpted`，底座置换为微倒角工艺品深色底座，降为 `--s 50`。
```text
Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, 52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key, sculpted dark charcoal canvas jacket, mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
```

#### 🔍 视角 00 ➔ 视角 01 微调置换与 IFTS 一致性对齐表 (Prompt Mutation Diff)
| 维度类别 | 视角 00 原文 Token (写实原片) | 视角 01 微调 Token (3D 模型) | 继承与微调对齐机制 |
| :--- | :--- | :--- | :--- |
| **主体媒介** | `Candid documentary portrait of a real` | `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust,` | 算子 ① 置换：显式声明 3D 打印树脂胸像，剥离摄影定性 |
| **人物指纹 (IFTS)** | `52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key` | `52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key` | **100% 逐字原样绝对继承（0 差异）**，锁定骨相神态 |
| **环境底座** | 真实生活或室外自然光照 | `mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus` | 算子 ③ 置换：生活背景置换为一体化工艺品底座与无缝浅灰影棚 |
| **参数配比** | `--s 80` | `--s 50` | 算子 ④ 调控：手办降噪控制发散，压制 AI 自由重绘面部 |
| **负向拦截** | `--no anime, 3d render, CGI, doll...` | `--no real living human, skin pores, plaster, stone column...` | 算子 ④ 置换：剔除 3D 拦截词，反向针对性拦截活人与石膏柱 |

#### 视角 02：【煽情场景一·专属老座】午后空椅·日光守望 · 【Gemini 专属】
```text
A poignant domestic documentary photograph showing the 6cm miniature 3D printed full-color resin bust figurine of the 52-year-old freight driver father with salt-and-pepper cropped hair and dark charcoal jacket, placed tenderly on a weathered wooden side table in an old apartment living room. Beside the tiny figurine rests his scratched stainless steel insulated thermos flask and folded metal reading glasses. In the soft-focus middle ground stands an empty, worn black faux-leather armchair. Afternoon golden sunlight slants through sheer curtains, illuminating floating dust motes and creating amber resin subsurface scattering (SSS) warmth on father's gentle face, evoking peaceful loving memories. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic Kodak Portra 400 film tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 03：【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀 · 【Gemini 专属】
```text
A solemn, deeply respectful documentary photograph showing the 6cm miniature 3D printed full-color resin bust figurine of the 52-year-old freight driver father with salt-and-pepper hair and charcoal jacket, honorably displayed on the middle-upper shelf of a modern walnut glass-door display cabinet in a home study room. The display shelf sits at eye-level, slightly elevated to convey profound filial piety and reverence while allowing intimate daily remembrance. Beside the bust figurine rests his well-worn freight truck keys and his scratched stainless steel insulated thermos. A gentle focused warm reading lamp from above illuminates the cabinet interior, casting soft reflections on the transparent glass door and warm translucent resin subsurface scattering (SSS) highlights across father's hardworking, gentle face. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, authentic Kodak Portra 400 film tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 04：【煽情场景三·岁月手艺】旧物深情·生锈时光 · 【Gemini 专属】
```text
A poignant still-life documentary photograph showing the 6cm miniature 3D printed resin bust figurine of the 52-year-old truck driver father sitting affectionately on top of a distressed, oily industrial metal tool chest in a garage. Next to the figurine rests an authentic vintage heavy steel mechanic wrench with surface rust and a roll of black electrical tape. Crisp natural window sunlight grazes the textured iron surface, creating a touching contrast between the rugged mechanic tools and the soft resin translucency of father's loving smile. Shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/3.2, rich industrial patina, Kodak Portra 400 analog grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 05：【煽情场景四·晨曦静好】窗台花草·微风晨光 · 【Gemini 专属】
```text
A peaceful, healing interior photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese truck driver father standing serenely on a sun-drenched natural wooden windowsill. Next to the figurine sits a healthy green potted money plant in a ceramic pot. A gentle morning breeze stirs a sheer white linen curtain, while 6:30 AM golden sunbeams create delicate Tyndall light rays with floating dust motes, casting an amber resin subsurface scattering (SSS) glow across father's cheek. Shot on Hasselblad X2D 100C with 90mm f/2.8 lens at f/2.8, creamy background bokeh, authentic Kodak Portra 400 tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 06：【煽情场景五·风雨归人】玄关守望·长明灯与老钥匙 · 【Gemini 专属】
```text
A deeply comforting domestic documentary photograph of the 6cm miniature 3D printed resin bust figurine of the 52-year-old Chinese father, standing peacefully on a dark solid walnut entryway console beside the front door. Right beside the figurine rests his well-worn freight truck key with a red and yellow woven lanyard, and a small yellowed handwritten note reading 'Drive safely on your way home'. A warm 2700K incandescent sconce casts a soft golden cone of light, illuminating father's gentle smile and creating soothing amber resin SSS translucency. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, cozy evening mood, authentic Kodak Portra 400 grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 07：【煽情场景六·掌心温存】掌心凝视·思念具象 · 【Gemini 专属】
```text
A deeply moving candid lifestyle photograph of an adult son's warm cupped hands gently holding the 6cm miniature full-color 3D printed resin bust figurine of his late 52-year-old freight driver father. The tiny figurine rests snugly in the center of the palm, showcasing a poignant scale contrast between real human palm skin textures and the intricate painted resin sculpture. Soft emotional daylight streams from a nearby window, creating tender nostalgic atmosphere, shot on Canon EOS R5 with RF 85mm f/1.4 lens at f/2.8, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 08：【煽情场景七·生活遗存】人间烟火·灶台重逢 · 【Gemini 专属】
```text
A poignant still-life documentary photograph showing the 6cm miniature 3D printed bust figurine of the 52-year-old truck driver father placed tenderly on a weathered kitchen countertop next to a seasoned black iron wok with rising swirls of savory cooking steam. Beside the figurine sits an old white porcelain bowl and freshly peeled garlic cloves. Morning golden light cuts through the kitchen window blinds, casting warm atmospheric dust rays and giving father's resin face an affectionate lifelike presence in the domestic smoke. Shot on Canon EOS R5 with RF 50mm f/1.8 lens at f/2.8, authentic Kodak Portra 400 film tone. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 09：【煽情场景八·深夜陪伴】深夜床头·台灯守候 · 【Gemini 专属】
```text
A quiet, deeply comforting nighttime interior photograph of the miniature 6cm 3D printed resin bust figurine of the 52-year-old father resting peacefully on a dark wooden bedside table. Beside the figurine stands a warm 2800K tungsten gooseneck reading lamp and a worn handwritten driver logbook showing highway routes. Gentle amber light kisses father's resin cheek, casting soft comforting shadows across the wood surface, conveying peaceful remembrance and eternal loving vigilance. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, delicate shadow details, Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 10：【煽情场景九·时光重叠】老相册对话·立体相逢 · 【Gemini 专属】
```text
An emotionally resonant macro photograph showing the 6cm miniature 3D printed full-color bust figurine of the 52-year-old freight driver father placed affectionately right beside an opened vintage 1990s red cloth-bound photo album. On the yellowed album page, an authentic corner-mounted vintage color photograph shows father in his early 20s smiling proudly in front of his first green cargo truck. The tangible 3D resin figurine and the flat historical photo gaze toward each other, turning flat memories into a tangible companion across decades. Shot on Canon EOS R5 with RF 85mm f/2 Macro lens at f/3.2, authentic Kodak Portra 400 grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

---

### 4.3 父辈全身像标杆级提示词工程示例 (以 51 岁校门接女儿父亲 char_31_FM 为例 · 全身 full-body 强制规范)

> [!IMPORTANT]
> - **【强制】全身人物全链路必须包含 `full-body`**：姿态代号为 `FM` 的全身像，视角 00（写实原片）、视角 01（3D 模型标准像）以及下游涉及全身的场景提示词，**必须显式包含 `full-body` 词条**，坚决杜绝半身裁切！
> - **严格对标 Midjourney V8 参数说明文档**：锁定 `--ar 1:1 --style raw --s 80 (00视角) / --s 50 (01视角) --v 8 --no ...`，定稿大图推荐挂载 `--q 2` 或 `--hd`；
> - **00 ↔ 01 IFTS 100% 逐字继承**：00 与 01 严格复用 16 词 IFTS 指纹序列，正向控制在 45~50 词，总词数 65~70 词。

#### 0. 51岁接站父亲五维深度铸造画像卡 (落地至 character_profile.md)
```markdown
## 五维人物深度铸造画像卡 (5D Character Forging Card)
- **人物编号与代号**：char_31_FM (雨天在校门口接女儿下自习的父亲)
- **年龄与定位**：51 岁中国普通工薪家庭父亲，寡言少语但护犊情深，雨天校门口的守候者
- **D1 面部骨相指纹**：微高风霜颧骨（Weathered cheekbones），紧毅下颌线，微内陷但温润的眼窝走向
- **D2 生理微瑕签名**：眼角深刻劳作笑纹、微显红血丝的眼睑（Tired loving eyes）、黑短发中两鬓花白（Graying temples cropped hair）
- **D3 服饰色彩 DNA**：深藏青连帽防风夹克（Dark navy windbreaker），耐磨深灰长裤，黑色防滑雨靴
- **D4 随身信物锚定**：一把带有木制弯头手柄的复古长柄黑雨伞（Long black umbrella with wooden curved handle），怀中紧紧护着用牛皮纸袋包裹的刚出锅热煎饼
- **D5 神态动态基线**：在校门口雨雾中伸长脖子焦急张望、看见女儿瞬间化开的慈爱安心笑容
```

#### 1. 提炼出的 16 词唯一性指纹 Token 序列 (IFTS · 写入 prompts.json)
```text
51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella
```

---

#### 视角 00：【基底定妆照】真实父亲生活写实全身摄影 (正脸全身像) · 【Midjourney 专属 · 强制包含 full-body】
> **指标与信噪比**：正向 48 词（显式包含 **`full-body portrait`** 与 **`full-body view`**，完整嵌入 16 词 IFTS），负向 14 词，总词数 67 词。严格遵照《Midjourney V8.x 核心参数与高级指令全景说明》配置 `--ar 1:1 --style raw --s 80 --v 8`。
```text
Candid documentary full-body portrait of a real 51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella, standing near school gate in light rain, full-body view, wearing dark navy windbreaker, wet gray trousers, black rain boots, soft overcast rainy daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
```

#### 视角 01：【模型标准像】0° 正面微缩全身手办棚拍 (依靠 00 微调成 3D 模型) · 【Midjourney 专属 · 强制包含 full-body】
> **微调置换与 full-body 约束**：首句声明 **`12.0cm 3D printed painted resin full-body model`**，**100% 逐字原样继承 16 词 IFTS 序列**，服装前追加 `sculpted`，底座声明 **`full-body standing on weighted circular base`**，风格化参数依说明文档降为 `--s 50`。正向 49 词，负向 15 词，总词数 68 词。
```text
Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model, 51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella, sculpted dark navy windbreaker, trousers and rain boots, full-body standing on weighted circular base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
```

#### 🔍 视角 00 ➔ 视角 01 微调置换与 IFTS 一致性对齐表 (Prompt Mutation Diff)
| 维度类别 | 视角 00 原文 Token (写实原片) | 视角 01 微调 Token (3D 模型) | 继承与微调对齐机制 |
| :--- | :--- | :--- | :--- |
| **主体媒介** | `Candid documentary full-body portrait of a real` | `Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model,` | 算子 ① 置换：显式声明 12cm 全身 3D 模型，锁定 full-body |
| **人物指纹 (IFTS)** | `51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella` | `51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella` | **100% 逐字绝对原样继承（0 差异）**，骨相、神态与手持雨伞信物绝对锁定 |
| **全身姿态底座** | `standing near school gate in light rain, full-body view, wearing dark navy windbreaker, wet gray trousers, black rain boots` | `sculpted dark navy windbreaker, trousers and rain boots, full-body standing on weighted circular base` | 算子 ② & ③ 置换：服装雕塑化，环境置换为全身加重配重圆形底座与浅灰影棚 |
| **参数配比** | `--s 80` | `--s 50` | 算子 ④ 调控：手办低自由度降噪，压制面部与全身比例漂移 |
| **负向拦截** | `--no anime, 3d render, CGI, doll...` | `--no real living human, skin pores, plaster, stone column...` | 算子 ④ 置换：剔除 3D 负向词，反向拦截活人与石膏柱 |

#### 视角 02：【煽情场景一·专属老座】午后空椅·日光守望 · 【Gemini 专属 · 全身手办】
```text
A poignant domestic documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father with graying temples, standing quietly beside an empty weathered bamboo rocking chair in the corner of a living room. Next to the full-body figurine on a low stool rests an old thermos flask and a dry towel. Soft afternoon window daylight falls across the empty chair and illuminates father's gentle smiling face with warm amber resin SSS translucency. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic Kodak Portra 400 tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 03：【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀 · 【Gemini 专属 · 全身手办】
```text
A poignant, dignified domestic documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father in navy windbreaker standing quietly on the middle-upper tier of a traditional rosewood curio shelf (duobaoge) in a quiet study. The shelf is positioned at eye level, commanding respectful remembrance and family dignity. Beside the full-body figurine rests a vintage fountain pen and an old leather-bound notebook. Soft 2800K warm interior ambient light and subtle accent illumination highlight father's composed posture and loving facial contours with gentle amber resin SSS translucency, symbolizing enduring respect and intergenerational memory. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 04：【煽情场景三·岁月手艺】旧物深情·生锈时光 · 【Gemini 专属 · 全身手办】
```text
A touching still-life documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing affectionately on an old wooden repair workbench. Beside the full-body figurine rests a weathered bicycle pump, replacement inner tube patches, and an antique pair of pliers. Natural window sidelight highlights the rugged tools and casts soft golden amber SSS glow across father's resin face, honoring a lifetime of humble manual labor and family devotion. Shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/3.2, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 05：【煽情场景四·晨曦静好】窗台花草·微风晨光 · 【Gemini 专属 · 全身手办】
```text
A peaceful, healing morning interior photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father standing serenely on a sunlit natural wooden balcony windowsill. Next to the full-body figurine sits a potted blooming jasmine plant in an earthen pot. A gentle dawn breeze stirs a light linen curtain while 6:30 AM golden Tyndall sunbeams illuminate floating dust specks, bathing the full-body figurine in warm amber resin translucency (SSS). Shot on Hasselblad X2D 100C with 90mm f/2.8 lens at f/2.8, creamy bokeh, authentic Kodak Portra 400 tones. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 06：【煽情场景五·风雨归人】玄关守望·长柄伞与老钥匙 · 【Gemini 专属 · 全身手办场景】
> **自然语言流**：描述微缩手办实体时显式注明 **`full-body figurine`**，与真实玄关老信物形成空间拓扑联动。
```text
An intensely touching domestic documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father with graying temples, standing peacefully upon a dark solid walnut entryway shoe cabinet beside the front door. Right beside the full-body figurine leans his vintage long black umbrella with dripping raindrops on a ceramic tray, a brass house key, and a small yellowed memo note reading 'Eat the warm food first'. A gentle 2700K warm incandescent wall sconce above casts a soft golden cone of light, warmly illuminating father's gentle smile lines and creating soothing amber resin translucency (SSS) and a soft elongated shadow on the wood grain, capturing the eternal warmth of father waiting for you in the rain. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 07：【煽情场景六·掌心温存】掌心凝视·思念具象 · 【Gemini 专属 · 全身手办】
```text
A deeply moving candid lifestyle photograph of an adult daughter's two open cupped hands gently cradling the 12cm miniature full-color 3D printed full-body resin figurine of her late 51-year-old father standing peacefully in his navy windbreaker with long umbrella. The full-body figurine stands in the center of her palms, creating a poignant scale contrast between real human hand skin textures and the intricate miniature painted resin sculpture. Soft emotional natural daylight streams from a window, conveying quiet grief solace and tender gratitude. Shot on Canon EOS R5 with RF 85mm f/1.4 lens at f/2.8, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 08：【煽情场景七·生活遗存】人间烟火·灶台重逢 · 【Gemini 专属 · 全身手办】
```text
A poignant still-life documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing tenderly on a weathered wooden dining table in a cozy home kitchen. Beside the full-body figurine sits a steaming hot bowl of homemade noodle soup with a fried egg and sliced scallions, and a pair of bamboo chopsticks resting on a small ceramic chopstick holder. Morning sunlight cuts through window blinds creating warm atmospheric dust rays, evoking the feeling of a loving father who just came home to share a warm meal. Shot on Canon EOS R5 with RF 50mm f/1.8 lens at f/2.8, authentic Kodak Portra 400 film tone. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 09：【煽情场景八·深夜陪伴】深夜床头·台灯守候 · 【Gemini 专属 · 全身手办】
```text
A quiet, comforting nighttime interior photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing peacefully on a dark solid walnut bedside nightstand. Beside the full-body figurine stands a warm 2800K tungsten gooseneck lamp and an open notebook with a pen. Soft golden lamplight illuminates father's kind smiling face, casting an elongated gentle shadow across the wood grain, creating soothing amber resin SSS translucency and a sense of eternal paternal protection in the quiet night. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 10：【煽情场景九·时光重叠】老相册对话·立体相逢 · 【Gemini 专属 · 全身手办】
```text
An emotionally resonant macro photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing affectionately right beside an opened vintage 1990s cloth photo album on a desk. On the yellowed album page, a faded corner-mounted color photograph shows the same father in his 20s smiling proudly holding his infant baby daughter in an old courtyard. The tangible 3D full-body figurine and the flat historical photo gaze toward each other, bridging decades of selfless fatherly love into a tangible companion. Shot on Canon EOS R5 with RF 85mm f/2 Macro lens at f/3.2, authentic Kodak Portra 400 film grain. Avoid: anime, cartoon, 3d digital render, CGI, modern digital photo album, oversaturated colors, distorted hands, harsh flash, caucasian, western features, plastic skin.
```

---

## 五、 与 `xiaohongshu-memorial-3dprint-copywriter` 职责解耦与协同契约

> **【架构职责解耦契约 (Decoupled Architecture)】**：
> - **`fullcolor-3dprint-character-prompts` (fullskill) 负责底层资产**：专注提供人物画像（`character_profile.md`）、3D 打印力学标准与 11 视角双引擎提示词手册（`prompts.md` / `prompts.json`）。**本技能绝不编写任何小红书文案**；
> - **`xiaohongshu-memorial-3dprint-copywriter` 负责上层营销**：作为独立文案专家技能，在需要撰写文案时被单独触发，负责读取本技能已落盘的画像与图片资产，独立产出 180~220 字爆款正文、8 条爆款标题与引流话术（生成 `小红书文案.md`）。

当触发小红书文案撰写技能时，两大技能通过以下接口实现全自动无缝协同：

1. **图文分镜绑定与代际母题映射**：
   - 小红书文案中的“9 图流排版规划”直接由 `fullcolor-3dprint-character-prompts` 的 11 个视角提供高质量图片资产；
   - 视角 02 ~ 10 九大煽情场景与 12 大反套路叙事母题无缝绑定：
      - **视角 02 (专属老座)** ➔ 对应祖辈/公婆“母题 4：老座余温与静默守候”或“母题 9：双向奔赴的公婆深情”；
      - **视角 03 (书房多宝阁·视平瞻怀)** ➔ 对应长辈/父母“母题 13：书房多宝阁的尊崇敬奉与跨越岁月的肃穆瞻怀”（置于多宝阁或玻璃展示柜中层偏上，视线平齐，既方便缅怀，又体现敬意）；
      - **视角 04 (岁月手艺)** ➔ 对应老工人/老技术员“母题 1：劳作者手记与手艺的温度”；
      - **视角 05 (窗台花草)** ➔ 对应爱美老妈/外婆“母题 6：岁月静好与生命治愈”；
      - **视角 06 (玄关守望)** ➔ 对应质朴老爸/老母亲“母题 7：如山父爱与未说出口的骄傲（钥匙与老保温杯）”；
      - **视角 07 (掌心凝视)** ➔ 贯穿全代际的小红书爆款首图与高点击封面；
      - **视角 08 (人间烟火)** ➔ 对应婆婆煲汤/母亲厨房“母题 2：舌尖味蕾与柴米油盐”；
      - **视角 10 (时光重叠)** ➔ 对应早逝父母/年轻岁月“母题 8：空巢母亲的语音与半生托举”或“母题 10：婚礼上的红眼眶与跨越时空的交接”。
2. **纯粹实体定制故事感**：
   - 两大技能严格遵守“禁止提及任何 AI 工具与建模软件名称”铁律，统一使用“老照片三维立体建模”、“高精度全彩树脂打印”、“手工微雕修件”等工艺性语言，维护读者纯粹的情感沉浸感。
