# 提示词工程规范：双引擎参数 · 00→01 衍生 · 高信噪比模板 (v5.0)

> 承接 SKILL.md 工作流 Step 4–5。本文件从 v4.1 SKILL.md 迁出，**保留原铁律编号便于追溯**；v5 的变更（02–10 改 3:4、词数预算校准、禁可读文字与灵堂意象）已在对应条目标注。
> 数值以 `config/paths.yml` 为准；交付前用 `validators/validate_prompts.py` 校验。

### 铁律二：画幅比例分组约束（v5 变更）
- **视角 00 / 01（建模参考）锁定 `--ar 1:1`**：用于 3D 建模点云重建与手办标准像，正交稳定；00 不用于小红书笔记。
- **视角 02–10（小红书笔记场景图）统一 3:4 竖构图**：小红书首图比例决定整篇笔记在双列信息流里的外框，3:4 占屏最大；一篇笔记内所有图同比例。
  - Gemini / Imagen：在工具或 API 参数里把画幅设为 `3:4`；提示词**开头**写 `Vertical 3:4 composition.`（工具不支持参数时，这句就是唯一的画幅约束）；
  - 封面候选视角 **07 掌心温存 / 10 时光重叠**：追加 `Leave clean negative space in the upper third for a title overlay.`，给封面大字留位置。
- 存量 1:1 场景图不与新 3:4 图混用：同一人物要换比例就整组 02–10 重出。

### 铁律三：Midjourney V8.x 核心参数与高级指令规约体系 (强制参考全景说明文档)
> **【强制】参考源绝对绑定**：
> 生成 Midjourney 提示词时，**必须严格参考并遵循《Midjourney V8.x 核心参数与高级指令全景说明》**（文档绝对路径：`/Users/wuyongjia/obsidian-gitee/technology/🧰 AI工具/midjourney/Midjourney V8.x 核心参数与高级指令全景说明.md`）。
> 提示词中所有 Midjourney CLI 参数名称、取值范围、默认值与组合方式必须与该全景说明文档保持 100% 严格一致，严禁出现非法参数或臆造参数！

1. **画幅与画质参数规约**：
   - **`--ar 1:1`【强制 · 仅视角 00/01】**：画面宽高比锁定为 1:1，渲染边缘零畸变，契合 3D 打印模型点云重建（小红书笔记场景图 02–10 为 3:4，见铁律二）；
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

### 铁律五：嘉立创全彩 WJP 树脂力学水密性规约与姿态景别双重强制契约（全身 full-body × 胸像 Keep the upper body）
1. **胸像规格 (BW/BM)**：物理高度 6.0 cm，一体化微倒角深色加重工艺品手办底座（Artisanal Collectible Display Base，坚决禁止白色石膏柱、大理石罗马柱等西方石膏雕塑风格；必须采用典藏手办标准的深色微切边工艺品底座），实心封闭网格，壁厚 $\ge 1.5\text{mm}$；
2. **【强制】胸像人物提示词必须包含 `Keep the upper body` 契约 (Bust Framing Token Enforcement)**：
   - **规约红线**：**凡生成的人物类型为胸像人物（姿态代号为 `BW` / `BM`，或 6.0cm bust 规格），生成的英文 Prompt（视角 00 基底原片与视角 01 手办标准像，以及所有胸像生成提示词）必须显式包含 `Keep the upper body` 关键词！**
   - **底层机制（阿里防御性门禁）**：扩散模型在未显式锁定上半身时，受面部注意力过度偏置影响，极易自作主张过度放大变为特写（Headshot），裁切掉肩部、胸口、服饰细节以及手办与底座相连的关键结构；显式注入 `Keep the upper body` 能在文本注意力头（Cross-Attention Heads）中强制锁定胸像标准景别（保留头、颈、肩、胸及完整上肢轮廓），确保 6.0cm 胸像手办比例协调，不缺失上半身躯干；
3. **全身像规格 (FW/FM)**：物理高度 12.0 cm，一体化平滑加重微型圆形工艺品基座（直径 40~45mm），重心稳定；
4. **【强制】全身人物提示词必须包含 `full-body` 契约 (Full-Body Token Enforcement)**：
   - **规约红线**：**凡生成的人物类型为全身人物（姿态代号为 `FW` / `FM`，或包含全身站姿、坐姿、全身比例与下半身构图的角色提示词），生成的英文 Prompt 必须显式包含 `full-body` 关键词（例如 `full-body portrait`, `full-body shot`, `12.0cm 3D printed painted resin full-body model`, `full-body view`）！**
   - **底层机制（阿里防御性门禁）**：扩散模型在未显式声明全身时，受文本注意力默认偏置影响，极易自作主张截取上半身胸像或近景特写，导致下半身衣着、鞋履及一体化工艺品底座丢失。显式注入 `full-body` 能在文本注意力头（Cross-Attention Heads）中强制锁定全景深景别与全身骨骼比例，确保模型自头至脚、包括底座完整生成，杜绝肢体截断；
5. **熔接防断加粗**：老花镜梁镜腿加粗至 $\ge 1.2\text{mm}$ 并与面颊熔接；随身道具（车把、工具、碗筷）必须实体融入身躯，禁止悬空细丝。


### 铁律七：视角 01【模型标准像】3D 模型显式锚定与防翻车黄金法则
1. **显式注入 3D 模型实体声明（3D Model Head Noun Anchoring）**：
   - 首句必须显式包含 **`3D model`** 与 **`3D printed painted resin`** 实体主语，前置统摄全局：
     - **胸像 (BW/BM)**：`Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body...`（【强制】必须显式包含 `Keep the upper body`）
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
4. **纯灰影棚隔离、画面零英文与防真人防石膏负向强拦截**：
   - 正向：`subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus`
   - 负向针对性拦截英文、活人、石膏柱与生活居室：`--no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`
5. **参数配比标定（控制风格化保护人脸保真度，严格参考全景说明）**：
   - 锁定 `--ar 1:1 --style raw --s 50 --v 8`（依据《Midjourney V8.x 核心参数与高级指令全景说明》，3D 模型标准像统一采用 `--s 50`，严禁使用 `--s 120`，大幅压制 AI 自作主张的面部脑补与艺术重绘，保障对 00 视角五官骨相的高保真锁定）。

### 铁律八：跨平台双引擎分工契约、零资产代码泄露与画面零英文红线
1. **彻底根除内部工程代号（Zero Asset ID Leakage）**：
   - 严禁在提示词（无论英文还是中文）中出现任何本地工程目录命名、变量名或编号（如 `char_XX_XX`、`char_01_BW`、`char_12_FW` 等）！
   - Midjourney 和 Gemini 作为通用基础模型，不认识任何私有变量代码；这类碎片 Token 会被错误分词（如 `char` -> 烧焦/角色, `12` -> 12个人/12根棍子），严重污染 Token 词嵌入空间与生成构图。
2. **生成画面与模型零英文文字契约 (Zero English Text & Midjourney `--no English` Enforcement)**：
   - **画面纯中式生活红线**：提示词正向描述中严禁为角色安排带有英文单词或英文字母印花的衣服、帽子、道具或背景包装（例如严禁描述“T恤上印有NEW YORK”、“杯子上带有英文”等）；
   - **Midjourney CLI 负向参数强制拦截**：Midjourney 视角 00 与 01 的 `--no` 负向参数必须显式包含 `English`（即 `--no English, ...`），彻底杜绝扩散模型在衣物或底座上脑补生成英文字母；
   - **Gemini 自然语言强制规避**：Gemini 视角 02 ～ 10 尾部负向必须显式包含 `Avoid: English text, letters, ...`。
   - **【v5】禁止要求渲染可读文字**：不写"便签上写着'饭在锅里'"、"招牌上写着……"这类带引号的文字内容（扩散模型会生成乱码或英文）；需要便签、招牌时写 `faded, illegible handwriting` / `blank signboard`。
   - **【v5】禁止灵堂 / 供桌意象**：场景里不放黑白证件照相框、香炉、红烛供桌、祭品、花圈、神龛（shrine / altar / incense / offering / memorial portrait）。纪念手办的陈列是家庭展示柜、书桌、窗台，不是灵位——这类画面在小红书属于丧葬意象，也会让画面显得阴森。
3. **生图引擎职责分工契约（Engine Delegation Protocol）**：
   - **视角 00 & 01 ➔ Midjourney 专属**：
     - 发挥 Midjourney 在单主体写实人像皮肤纹理、微距光学镜头虚化及灰背景影棚光影渲染上的顶级表现力；
     - 语法规范：单段连贯自然语言流，末尾严格依照《Midjourney V8.x 核心参数与高级指令全景说明》携带 `--ar 1:1 --style raw --s 80（视角00）/--s 50（视角01） --v 8 --no English, ...`。
   - **视角 02 ～ 10 ➔ Gemini (Imagen 3) 专属**：
     - 发挥 Gemini (基于大语言模型 T5-XXL / Gemini 语义编码器) 在复杂空间拓扑推理（Spatial Reasoning）、主体嵌套从属绑定（Attribute Binding）上的碾压级优势（例如将微缩手办置于大衣口袋、婚宴餐桌、书桌奶糖旁、掌心托举等复杂场景）；
     - 语法规范：纯自然语言分层叙事（Natural Language Prompt），**严禁出现 Midjourney 的 CLI 命令行参数（禁止 `--ar`, `--v 8`, `--style raw`, `--no` 等）**；**开头**写 `Vertical 3:4 composition.`；末尾统一以自然语言负向排除（如 `Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.`）。
     - v5 标准骨架：`Vertical 3:4 composition. [场景主体：手办 + 位置 + 专属信物] [环境与光影] [封面候选追加留白句] Shot on [机身 + 镜头 + 光圈], [胶片质感]. Avoid: English text, letters, ...`

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
  ├─ 算子 ① [主体媒介微调] ➔ 替换为 3D 模型显式主语 (3D model, 3D printed painted resin...)，全身像必须包含 full-body，胸像必须包含 Keep the upper body
  ├─ 算子 ② [特征完全继承] ➔ 100% 逐字继承 00 面容、发型、饰品，衣服追加 sculpted
  ├─ 算子 ③ [环境底座微调] ➔ 去除生活背景，微调为工艺品底座与浅灰无缝影棚 (pedestal, cyclorama...)
  └─ 算子 ④ [参数负向微调] ➔ 风格化按参数文档降为 --s 50；负向统一追加 English 拦截英文字符，01 移除 3D/手办拦截并微调为拦截活人与石膏
  │
  ▼
【视角 01：3D 模型标准像提示词】
```

1. **算子 ①：主体与媒介微调（Subject & Medium Mutation ➔ 显式声明 3D 模型与景别）**：
   - **00 原版**：`Candid documentary portrait of a real [age]-year-old Chinese [role] in [setting]`（若为全身像包含 `full-body portrait`；若为胸像包含 `Keep the upper body`）
   - **01 微调为**：
     - **胸像 (BW/BM)**：`Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body, [age]-year-old Chinese [role],`（【强制】必须显式包含 `Keep the upper body`）
     - **全身像 (FW/FM)**：`Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model, [age]-year-old Chinese [role],`（【强制】必须显式包含 `full-body`）
   - **微调红线**：首句前置明确注入 **`3D model`** 与 **`3D printed painted resin`**，胸像必须携带 `Keep the upper body` 锁定上半身完整性，直球定义实体为物理 3D 打印模型。
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
     - **00 原版**：`--no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands`（封杀英文、3D/假人）
     - **01 微调为**：**彻底剔除 `3d render`, `doll`, `figurine`, `plastic skin` 等自残拦截词**，反向微调为封杀英文、真实活人与石膏柱：`--no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`。

### 铁律十：视角 00 与视角 01 差异性与微调映射矩阵 (00 vs 01 Diff & Mutation Matrix)
> **阿里规范排他契约**：视角 01 依靠 00 微调，通过下述 8 大维度的精准映射，实现“人物形象 100% 相同、载体本质 100% 切换为 3D 模型”：

| 约束维度 | 视角 00：【基底定妆照】真实长辈生活写实摄影 | 视角 01 微调操作 (Mutation Action) | 视角 01：【模型标准像】依靠 00 微调成的 3D 模型 |
| :--- | :--- | :--- | :--- |
| **1. 主体本质 (Entity)** | 真实活人纪实生活肖像抓拍 (`real elderly Chinese...`)；若为全身像【强制】必须包含 `full-body` (`full-body portrait`)；若为胸像【强制】必须包含 `Keep the upper body` | **置换为 3D 模型** | 3D 打印全彩光敏树脂模型 (`3D model, 6.0cm bust` 或 `12.0cm full-body model`)；全身像包含 `full-body`；胸像包含 `Keep the upper body` |
| **2. 表面材质 (Material)** | 真实人体皮脂微孔、天然皱纹与体温感 (`natural skin texture, pores`) | **置换为树脂 SSS 质感** | 工业级光敏树脂哑光微透光次表面散射 (`subtle resin SSS finish, painted details`)，**严禁毛孔** |
| **3. 人物特征 (Face/Hair)** | 东亚五官、眯眯笑眼、深鱼尾纹、花白发髻/寸头 | **100% 逐字保留复用** | 100% 严格继承 00 原文 Token 序列，面部骨相与神态零偏差 |
| **4. 服装配饰 (Clothes)** | 真实生活棉麻盘扣小袄、工装夹克、围裙、老花镜 | **原样继承 + 微调雕塑化** | 继承 00 原文颜色与款式，服饰前微调增加 `sculpted` 修饰词，贴身配饰完整保留 |
| **5. 环境背景 (Scene)** | 真实中国家庭生活环境（厨房、书房、阳台窗光） | **置换为纯灰影棚天幕** | 纯浅灰无缝影棚天幕 (`solid neutral light gray seamless cyclorama`)，杜绝居室背景 |
| **6. 基座力学 (Base)** | 活人自然站/坐，**绝对无底座** | **注入一体化工艺品底座** | **胸像**：深色微倒角底座 (`dark beveled pedestal base`)；**全身像**：加重圆盘底座（`full-body standing on weighted circular base`），**严禁石膏柱** |
| **7. 镜头景深 (Optics)** | 哈苏中画幅 90mm f/3.2 纪实浅景深柔和虚化 | **置换为微距全焦清晰** | 佳能 RF 100mm f/8 正交 0° 视平线微距，大景深边缘锐利 (`RF 100mm f/8 focus`) |
| **8. 参数与负向 (Params)** | 参考 V8 参数说明：`--s 80` 搭配封杀英文与假人 (`--no English, anime, 3d render, doll...`) | **参数降级 + 反向拦截活人** | 参考 V8 参数说明：`--s 50` 搭配封杀英文、活人与石膏 (`--no English, real living human, skin pores, plaster...`) |

---

### 铁律十一：提示词长度硬性上限与高信噪比精简架构 (Prompt Length & High-SNR Compact Protocol)
> **告别过度包装，回归高信噪比**：
> 提示词越长，末尾的材质、底座与负向约束越容易被稀释。本技能对视角 00 与 01 设词数预算，用精准的工业与光学核心词替换无效修饰词。
>
> **v5 校准说明**：v4.x 的"总词数 50–70"与本技能自己的强制结构互相矛盾——01 视角的 3D 实体声明（13 词）+ 景别锁（4 词）+ IFTS（15–20 词）+ 底座影棚光学（17 词）+ 负向（16 词）本身就有 65–70 词，再加服装必然超限（v4.1 黄金示例实测 78 词；旧校验器因把负向词截断在第一个连字符处而漏检）。v5 按实际结构重新定预算，由 `validators/validate_prompts.py` 按空白分词统计。

1. **词数预算（数值以 `config/paths.yml` 的 `word_count` 为准）**：
   - **正向词**：35 ～ 65 英文单词（3D 模型主体 + IFTS + 雕塑服装 + 基座/背景 + 树脂光学；全身像包含 `full-body`）；
   - **负向词 (`--no`)**：12 ～ 18 英文单词（只保留致命缺陷与互斥拦截词）；
   - **总词数**：50 ～ 82 词。超出时优先删修饰词与重复的光学描述，**不删 IFTS、景别锁与 `English` 负向**。

2. **瘦身与降噪清洗三原则（Zero-Signal Token Elimination）**：
   - ❌ **剔除前缀客套词**：从 `A professional macro studio photograph of an exquisite tabletop collectible painted resin bust statue precisely transforming the exact...`（30+ 词）压缩为 `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust...`（13 词）；
   - ❌ **消除近义修饰堆叠**：将 `warm gentle crinkling eyes with deep natural crow's feet, realistic nasolabial smile lines, natural age spots and fine skin texture` 精炼为 `crinkling smile eyes, deep crow's feet, natural age spots`；
   - ❌ **清理负向冗余词**：合并 `young, youthful, teenager, child` 为 `young, child`，合并 `caucasian, western, foreigner, white person, non-asian` 为 `western, non-asian`，保留核心拦截效能。

3. **视角 00 与 视角 01 标准结构公式（v5：IFTS 在 00/01 中必须是一整段连续原文，景别锁放在 IFTS 之外）**：
   > `[IFTS]` = `prompts.md` 第 0 节登记的 15–20 词指纹原文，逐字粘贴，中间不插入任何词。
   - **视角 00 胸像**（强制 `Keep the upper body` 与 `--no English`）：
     ```text
     Candid documentary portrait of a real [IFTS], Keep the upper body, in [setting], wearing [clothing], soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
     ```
   - **视角 00 全身像**（强制 `full-body` 与 `--no English`）：
     ```text
     Candid documentary full-body portrait of a real [IFTS], in [setting], full-body view, wearing [clothing & shoes], soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
     ```
   - **视角 01 胸像**（依靠 00 微调；强制 `Keep the upper body` 与 `--no English`）：
     ```text
     Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body, [IFTS], sculpted [clothing], mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
     ```
   - **视角 01 全身像**（依靠 00 微调；强制 `full-body` ×2 与 `--no English`）：
     ```text
     Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model, [IFTS], sculpted [clothing & shoes], holding [welded prop], full-body standing on weighted circular base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
     ```


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
Step 6: 【负向拦截与 V8 参数精控】➔ 00/01 挂载 --ar 1:1 --style raw --s 80/50 --v 8 --no English, …
Step 7: 【v5 · 场景图 02–10】➔ 3:4 竖构图开头句 + 场景变奏 + 封面候选留白 + Avoid: English text, letters, …
```

1. **Step 1: 五维铸造与指纹提取 (Subject & Identity Fingerprint)**：
   - 严禁模糊代称！以五维铸造卡为依据，提取包含骨相、笑纹、发型、配饰的 IFTS 核心指纹序列，作为提示词的不可变核心；
2. **Step 2: 动作姿态与全身/胸像景别锁定 (Action, Pose & Framing Constraint)**：
   - 参考 Nano-Banana 的 Action 规范：00 视角指定真实生活动作（如站在砧板前切葱花、握着菜篮把手、扶着老花镜），01 视角统一约束为正面 0° 挺立/坐姿雕塑形态；
   - **【强制】全身人物 full-body 锚定**：凡是全身人物（FW/FM 或全身构图），生成的提示词必须显式包含 **`full-body`** 词条（如 `full-body portrait`, `full-body shot`, `12.0cm 3D printed painted resin full-body model`, `full-body view`），锁定全身比例；
   - **【强制】胸像人物 Keep the upper body 锚定**：凡是胸像人物（BW/BM 或 6.0cm 胸像），生成的提示词必须显式包含 **`Keep the upper body`** 词条，锁定上半身与胸肩完整结构，杜绝大头贴特写与双肩截断；
3. **Step 3: 环境拓扑与多光源混合 (Context & Mixed Lighting)**：
   - 参考 GPT-Image-2 的多光源物理混合：00 视角组合窗外柔和晨光与居室暖调；01 视角统一为浅灰无缝影棚天幕（`light gray cyclorama`）配合双侧柔光箱（`softbox lighting`）；
4. **Step 4: 光学镜头与景深标定 (Composition & Optics)**：
   - 00 视角锁定哈苏中画幅 90mm f/3.2 纪实浅景深；01 视角锁定佳能 RF 100mm f/8 微距全景深正交机位，确保手办边缘锐利清晰、无透视畸变；
5. **Step 5: 材质物性与胶片质感注入 (Material & Film Texture)**：
   - 00 视角注入真实老人皮脂与胶片银盐颗粒（`Kodak Portra 400 film grain`）；01 视角注入嘉立创光敏树脂哑光质感与次表面散射（`subtle resin SSS finish`）；
6. **Step 6: 负向拦截与 V8 参数精控 (Negative Filtering & Midjourney V8 Parameter Control)**：
   - **严格遵循《Midjourney V8.x 核心参数与高级指令全景说明》文档标准**；
   - 00 视角挂载 `--ar 1:1 --style raw --s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands`；
   - 01 视角挂载 `--ar 1:1 --style raw --s 50 --v 8 --no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands`；
   - 商用高精定稿推荐挂载 `--q 2` 或 `--hd`；跨视角主体一致性衍生推荐挂载 `--oref <URL> --ow 100~300` 或 `--cref <URL> --cw 100`。
7. **Step 7（v5）: 场景图 02–10 (Gemini / Imagen)**：
   - 工具参数设 `3:4`；提示词以 `Vertical 3:4 composition.` 开头；
   - 按 `references/scene-library.md` 的九个情绪槽位写场景，并按「场景变奏规则」在机位、实景、道具、光影四层里至少换两层，避免全库同一模板；
   - 07 掌心温存、10 时光重叠追加 `Leave clean negative space in the upper third for a title overlay.`；
   - 不写带引号的可读文字，不放灵堂/供桌意象；结尾 `Avoid: English text, letters, …`。

---
