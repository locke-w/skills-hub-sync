# 提示词工程规范：Gemini 模板 · 00→01 衍生 · 高信噪比模板 (v6.0 · auto-xhs)

> 由旧版提示词工程规范迁改。**全部 11 个视角统一走 Gemini App 图像模型（自然语言提示词，无任何 CLI 参数）**；00/01 仍是 1:1 建模参考视角，02–10 为 3:4 小红书场景图。
> 数值以 `config/studio.toml` 为准；交付前用 `scripts/validate_prompts.py` 校验。

### 铁律二：画幅比例分组约束
- **视角 00 / 01（建模参考）1:1**：提示词**开头**写 `Square 1:1 composition.`，用于 3D 建模点云重建与手办标准像；00 不进小红书笔记。
- **视角 02–10（小红书笔记场景图）3:4 竖构图**：提示词**开头**写 `Vertical 3:4 composition.`；gemini_app.py 出图后还会对非 3:4 的下载图居中裁切（见 `studio.toml [images]`）。
- **封面候选 07 / 10**：追加 `Leave clean negative space in the upper third for a title overlay.`，主体放在画面下 2/3。
- 一篇笔记内所有图同比例；存量 1:1 素材不与新 3:4 混用。

### 铁律三：Gemini App 出图模板（逐字使用，`{}` 为字段）
> 提示词为纯连贯单段自然语言流，**严禁任何 `--` CLI 参数**，各语义层次用 `, ` 连接。

1. **视角 00 胸像 (BW/BM)**：
   ```text
   Square 1:1 composition. Candid documentary portrait photograph of a real {ifts}, Keep the upper body, {setting}, wearing {cloth}, {light00}. Shot on Hasselblad 90mm f/3.2, Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western features, youthful face, deformed hands.
   ```
2. **视角 00 全身 (FW/FM)**：
   ```text
   Square 1:1 composition. Candid documentary full-body portrait photograph of a real {ifts}, full-body view from head to feet, {setting}, wearing {cloth}, {light00}. Shot on Hasselblad 90mm f/3.2, Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western features, youthful face, deformed hands.
   ```
3. **视角 01 胸像 (BW/BM)**：
   ```text
   Square 1:1 composition. Macro studio product photo of a 6.0cm 3D printed painted resin bust, Keep the upper body, {ifts}, sculpted {cloth01}, mounted on a dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting. Shot on RF 100mm f/8. Avoid: English text, letters, real living human, skin pores, plaster, stone column, room, furniture, outdoor scenery, western features, youthful face, deformed hands.
   ```
4. **视角 01 全身 (FW/FM)**：
   ```text
   Square 1:1 composition. Macro studio product photo of a 12.0cm 3D printed painted resin full-body model, full-body view, {ifts}, sculpted {cloth01}, full-body standing on a weighted circular base, subtle resin SSS finish, light gray cyclorama, softbox lighting. Shot on RF 100mm f/8. Avoid: English text, letters, real living human, skin pores, plaster, stone column, room, furniture, outdoor scenery, western features, youthful face, deformed hands.
   ```
5. **视角 02–10（场景图）**：
   ```text
   Vertical 3:4 composition. {en（须含 figurine_anchor 原文）} [Leave clean negative space in the upper third for a title overlay. ]Shot on {shot}. Avoid: {AVOID}[, {slot_extra}].
   ```
   - 标准 AVOID（手办题材 01–10 的 Avoid **禁止**含 doll/3d render/figurine/plastic skin 等自残词）：
     `English text, letters, watermark, anime, cartoon, CGI look, cheap toy plastic shine, western features, youthful face, deformed hands, extra fingers, missing fingers, floating objects, broken geometry`
   - `slot_extra`：07 `fused fingers, visible human face`；08 `exaggerated steam, messy clutter`；09 `creepy dark shadows, blown out lamp highlights`。

### 铁律四：摄影光学与生理微瑕分层规约 (去 AI 塑料感)
1. **严禁空洞词汇**：禁止使用 `masterpiece, 8k, hyperrealistic, ultra detailed, smooth skin`；
2. **年龄分层生理微瑕精准注入**：依据人物年龄与劳作身份差异化注入微瑕（客运父亲的面颊风霜、工装父亲指关节老茧、高龄祖辈不对称鱼尾纹与淡老年斑）；
3. **嘉立创 WJP 全彩光敏树脂材质还原**：`delicate matte polymer finish, subtle resin translucency with subsurface scattering (SSS)`；
4. **专业光学器材标定**：定妆照哈苏中画幅（`Hasselblad 90mm f/3.2` + `Kodak Portra 400 film grain`），手办标准像 `RF 100mm f/8`；场景图在 `{shot}` 里指定机身镜头光圈与胶片调。

### 铁律五：嘉立创全彩 WJP 树脂力学水密性规约与姿态景别双重强制契约（全身 full-body × 胸像 Keep the upper body）
1. **胸像规格 (BW/BM)**：物理高度 6.0 cm，一体化微倒角深色加重工艺品底座（禁石膏柱/大理石柱），实心封闭网格，壁厚 ≥ 1.5mm；
2. **【强制】胸像人物提示词必须包含 `Keep the upper body`**（00 与 01 均须显式包含，防止过度放大成特写裁掉肩胸与底座结构）；
3. **全身像规格 (FW/FM)**：物理高度 12.0 cm，一体化加重圆形基座（直径 40–45mm），重心稳定；
4. **【强制】全身人物提示词必须包含 `full-body`**：00 ≥1 次（`full-body portrait`/`full-body view`）、01 ≥2 次（`full-body model` + `full-body standing on`）；
5. **熔接防断加粗**：细长件（眼镜腿、绳、杆）加粗至 ≥ 1.5mm 并与身躯熔接，禁止悬空细丝。

### 铁律七：视角 01【模型标准像】3D 模型显式锚定与防翻车黄金法则
1. **显式注入 3D 模型实体声明**：首句必须含 `3D printed painted resin`：
   - 胸像：`Macro studio product photo of a 6.0cm 3D printed painted resin bust, Keep the upper body, ...`
   - 全身：`Macro studio product photo of a 12.0cm 3D printed painted resin full-body model, full-body view, ...`
2. **彻底根除负向词自残矛盾（避免生出活人）**：视角 01 及所有手办场景（02–10）的 Avoid **严禁**出现 `doll`, `3d render`, `figurine`, `plastic skin`, `porcelain doll`, `wax museum`；
3. **工艺品底座物理融合**：严禁 `stone pedestal`, `plaster`, `marble column`；胸像 `mounted on a dark beveled pedestal base`，全身 `full-body standing on a weighted circular base`；
4. **纯灰影棚隔离**：`subtle resin SSS finish, light gray cyclorama, softbox lighting. Shot on RF 100mm f/8.`；Avoid 拦截英文、活人与居室环境（见铁律三模板）。

### 铁律八：统一引擎契约、零资产代码泄露与画面零英文红线
1. **彻底根除内部工程代号**：提示词中严禁出现 `char_XX`、`BW/BM/FW/FM` 姿态码、本地路径等私有代号；
2. **画面与文案零英文文字**：
   - 正向描述中严禁给角色安排带英文字母的服饰/道具/包装；
   - 00/01 与 02–10 的 `Avoid:` 必须显式以 `English text, letters` 开头拦截；
   - **禁止要求渲染可读文字**：便签写 `faded, illegible handwriting`，日历写 `blank calendar page`，招牌写 `blank signboard`；
   - **禁止灵堂/供桌意象**：不放黑白证件照相框、香炉、红烛、祭品、花圈、神龛（funeral / memorial altar / shrine / incense burner / offering table / mourning / tombstone / graveyard / funeral urn / cremation ashes / red candles）。陈列场景是家庭展示柜、书桌、窗台，不是灵位；
3. **场景图标准骨架**（02–10）：`Vertical 3:4 composition. [场景主体：figurine_anchor + 位置 + 专属信物] [环境与光影] [封面候选留白句] Shot on [机身+镜头+光圈], [胶片质感]. Avoid: English text, letters, ...`

### 铁律九：视角 01 依靠 00 微调衍生协议 (00-to-01 Mutation)
> 00 是写实原片基底，01 是 3D 模型微缩手办标准像，二者是严格的衍生关系，四大置换算子：

```
【视角 00：真实生活抓拍提示词】
  │
  ├─ 算子 ① [主体媒介微调] ➔ 置换为 3D 模型显式主语（含景别锁 Keep the upper body / full-body）
  ├─ 算子 ② [特征完全继承] ➔ 100% 逐字继承 IFTS；衣服追加 sculpted
  ├─ 算子 ③ [环境底座微调] ➔ 生活场景置换为工艺品底座与浅灰影棚
  └─ 算子 ④ [负向微调] ➔ Avoid 剔除 3D/手办拦截词，改拦 real living human / skin pores / plaster / 居室环境
  │
  ▼
【视角 01：3D 模型标准像提示词】
```

### 铁律十：视角 00 ↔ 01 差异性与微调映射矩阵

| 约束维度 | 视角 00：【基底定妆照】真实长辈生活写实摄影 | 视角 01 微调操作 | 视角 01：【模型标准像】3D 模型 |
| :--- | :--- | :--- | :--- |
| **1. 主体本质** | `Candid documentary [full-body ]portrait photograph of a real ...` | **置换为 3D 模型** | `Macro studio product photo of a 6.0cm bust` / `12.0cm full-body model` |
| **2. 表面材质** | 真实皮脂微孔、天然皱纹 | **置换为树脂 SSS** | `subtle resin SSS finish`，严禁毛孔 |
| **3. 人物特征** | IFTS 原文 | **100% 逐字保留** | 同序列，0 差异 |
| **4. 服装配饰** | `wearing {cloth}` | **追加 sculpted** | `sculpted {cloth01}` |
| **5. 环境背景** | 生活场景 `{setting}, {light00}` | **置换为纯灰影棚** | `light gray cyclorama, softbox lighting` |
| **6. 基座力学** | 活人自然站/坐，无底座 | **注入工艺品底座** | `dark beveled pedestal base` / `weighted circular base`，严禁石膏柱 |
| **7. 镜头景深** | 哈苏 90mm f/3.2 纪实 | **置换为微距全焦** | `Shot on RF 100mm f/8` |
| **8. 负向拦截** | 拦动漫/3D 假人/英文 | **剔除 3D 词，拦活人石膏** | `real living human, skin pores, plaster, stone column, room, furniture, outdoor scenery` |

### 铁律十一：提示词长度与高信噪比精简架构
- **词数预算**：00/01 整段（含 Avoid）50–110 词（`studio.toml [prompt].square_total_words`）；IFTS 15–20 词；
- **瘦身三原则**：剔前缀客套词、消近义修饰堆叠、清理负向冗余；**不删 IFTS、景别锁与 `English text, letters` 负向**；
- **IFTS 在 00/01 中必须是一整段连续原文**，景别锁放在 IFTS 之外。

---

## 三、 参考体系与六步法构建协议

**参考精髓**：GPT-Image 系的“电影级真实胶片人像分层架构”（胶片规格 + 多光源混合 + 生理微瑕 + 色彩微偏）与 nano-banana 的“推理驱动结构化简报”（Subject + Action + Context + Composition + Lighting + Style）及 Identity Consistency 契约（语义指纹 Token 强一致性约束解决跨视角人脸漂移）。**本技能不依赖任何外部参数文档。**

### 提示词标准化构建流水线
```
Step 1: 【五维铸造与指纹提取】➔ 提炼 15~20 词 IFTS（写入 character.json）
Step 2: 【动作姿态与景别锁定】➔ 全身强制 full-body，胸像强制 Keep the upper body
Step 3: 【环境拓扑与多光源混合】➔ 生活居室光影 / 浅灰影棚天幕
Step 4: 【光学镜头与景深标定】➔ 哈苏 90mm f/3.2 / RF 100mm f/8
Step 5: 【材质与胶片质感】➔ Kodak Portra 400 / 树脂 SSS
Step 6: 【负向拦截】➔ Avoid: English text, letters, …（01–10 禁 figurine/doll 类自残词）
Step 7: 【场景图 02–10】➔ 3:4 开头句 + figurine_anchor 逐字 + 封面候选留白 + Avoid
```
