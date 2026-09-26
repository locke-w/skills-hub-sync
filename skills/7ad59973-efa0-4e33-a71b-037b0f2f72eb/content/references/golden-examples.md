# 双引擎标杆级黄金示例 (v5.0)

> 从 v4.1 SKILL.md 迁出。v5 已按新规则修订：视角 02–10 开头加 `Vertical 3:4 composition`；Gemini 负向统一含 `English text, letters`；封面候选视角 07/10 预留上 1/3 标题留白；删除要求渲染可读文字的描述。
> 00/01 的词数说明为 v4.1 原注，实际以 `validators/validate_prompts.py` 统计为准（v5 预算见 `config/paths.yml`）。

## 四、 双引擎标杆级黄金提示词工程示例 (以厨房外婆为例)

> [!IMPORTANT]
> - **先铸造、后出词**：每个人物必须先完成《五维铸造画像卡》，并提取 `identity_fingerprint_tokens` (IFTS)；
> - **视角 00 & 视角 01【Midjourney 专属】**：单段连贯流，尾部挂载 `--ar 1:1 --style raw --s ... --v 8 --no English, ...`，严格遵循 **50 ～ 70 词高信噪比硬上限**，严禁任何内部代码、英文字符印花与自残负向词；
> - **胸像强制注入 `Keep the upper body`**：视角 00 与 01 均显式包含 `Keep the upper body`，杜绝大头贴特写；
> - **00 ↔ 01 指纹序列 100% 逐字对齐**：00 与 01 必须 100% 逐字复用提取出的 IFTS 指纹序列，确保同一个长辈的骨相与神态绝对统一；
> - **视角 02 ～ 视角 10【Gemini (Imagen 3) 专属】**：纯英文自然语言分层描述（主体+空间嵌套+环境+光影镜头），**严禁出现 Midjourney 的 CLI 命令行参数（无 `--ar`, 无 `--v 8`, 无 `--style raw`, 无 `--no`）**，尾部以自然语言 `Avoid: English text, letters, ...` 进行负向拦截；
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

### 视角 00：【基底定妆照】真实长辈生活写实摄影 (正脸半身胸像 · 强制 Keep the upper body) · 【Midjourney 专属】
> **信噪比与指标**：正向 50 词（显式包含 **`Keep the upper body`**，完整嵌入 18 词 IFTS），负向 15 词（包含 **`English`** 拦截），总词数 69 词。完全符合 50 ～ 70 词黄金敏感区间，彻底解决过长告警，精确锁定中国真实厨房外婆面容与生活光影。
```text
Candid documentary portrait of a real 72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings, Keep the upper body, in kitchen, wearing navy frog-button tunic with floral apron, soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
```

### 视角 01：【模型标准像】0° 正面微缩手办棚拍 (依靠 00 微调成 3D 模型标杆版 · 强制 Keep the upper body) · 【Midjourney 专属】
> **微调衍生原则**：直接以视角 00 提示词为基底，通过四大微调置换算子转化成 3D 模型；显式注入 **`Keep the upper body`** 锁定胸像景别；**100% 逐字继承 18 词 IFTS 指纹序列**；正向 51 词，负向 16 词（包含 **`English`** 拦截），总词数 69 词。
```text
Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body, 72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings, sculpted navy frog-button tunic with floral apron, mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
```

#### 🔍 视角 00 ➔ 视角 01 微调置换与 IFTS 一致性对齐表 (Prompt Mutation Diff)
| 维度类别 | 视角 00 原文 Token (写实原片) | 视角 01 微调 Token (3D 模型) | 继承与微调对齐机制 |
| :--- | :--- | :--- | :--- |
| **主体媒介与景别** | `Candid documentary portrait of a real ... Keep the upper body` | `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body` | 算子 ① 置换：显式声明 3D 打印树脂胸像并锁定 `Keep the upper body`，剥离摄影定性 |
| **人物唯一性指纹 (IFTS)** | `72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings` | `72-year-old Chinese grandmother, rounded cheekbones, crinkling smile eyes, deep crow's feet, natural age spots, silver-gray hair bun, silver hoop earrings` | **100% 逐字绝对原样继承（0 差异）**，锁定骨相神态，杜绝跨模型人脸漂移 |
| **服装信物** | `wearing navy frog-button tunic with floral apron` | `sculpted navy frog-button tunic with floral apron` | 算子 ② 微调：保留色彩款式，仅在服饰前追加 `sculpted` 声明雕塑化 |
| **环境底座** | `in kitchen, soft morning window daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain` | `mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus` | 算子 ③ 置换：厨房居室置换为深色微倒角工艺品底座、树脂 SSS 质感与正交微距全焦 |
| **参数配比** | `--s 80` | `--s 50` | 算子 ④ 调控：手办降噪控制风格化发散度，压制 AI 自由重绘面部 |
| **负向拦截** | `--no English, anime, 3d render, CGI, doll, figurine, plastic skin...` | `--no English, real living human, skin pores, plaster, stone column...` | 算子 ④ 置换：统一挂载 `English` 杜绝英文字符，01 剔除 3D 拦截词并反向针对性拦截活人与石膏柱 |

### 视角 02：【煽情场景一·专属老座】午后空椅·日光守望 · 【Gemini 专属】
```text
Vertical 3:4 composition. A poignant, emotionally resonant documentary photograph of the miniature 6cm 3D printed full-color photopolymer resin bust figurine of the smiling Chinese kitchen grandmother with navy floral apron and silver hair bun, placed tenderly on a weathered wooden side table in an old-fashioned Chinese home living room. Right beside the figurine sits an authentic vintage chipped green enamel tea mug and a pair of folded reading glasses. In the soft-focus middle ground stands an empty traditional hand-woven wicker rocking armchair with gentle signs of decades of loving use. Warm 3:30 PM golden afternoon sunlight slants through a classic wooden lattice window, creating gentle dancing Tyndall dust motes in the air and casting soft warm highlights on grandmother's smiling resin face with glowing subsurface scattering (SSS), evoking deep domestic nostalgia and the comforting feeling that she has only stepped away for a moment. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic 35mm Kodak Portra 400 analog film tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 03：【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀 · 【Gemini 专属】
```text
Vertical 3:4 composition. A dignified, emotionally resonant domestic documentary photograph of the miniature 6cm 3D printed full-color resin bust figurine of the smiling Chinese kitchen grandmother with navy floral apron and silver hair bun, respectfully placed on the middle-to-upper tier of an elegant dark rosewood curio display shelf (duobaoge) inside a quiet family study room. The shelf height is positioned exactly at eye level, offering a serene, reverent line of sight for daily remembrance. Right beside the figurine rests an authentic vintage chipped green enamel tea mug and a small polished brass seal. Soft warm 3000K museum-grade interior spotlighting gently glints off the polished hardwood grain and partially illuminates grandmother's gentle smiling face with delicate amber resin subsurface scattering (SSS), creating an aura of dignified family reverence, eternal respect, and quiet comforting remembrance. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, delicate shadows, authentic Kodak Portra 400 analog tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 04：【煽情场景三·岁月手艺】旧物深情·生锈时光 · 【Gemini 专属】
```text
Vertical 3:4 composition. A deeply nostalgic still-life documentary photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese grandmother placed affectionately upon an authentic vintage 1970s black cast-iron foot-treadle sewing machine table with distressed wooden surface and aged lacquer patina. Beside the figurine rests a vintage wooden spool of weathered red cotton thread, an antique pair of steel sewing scissors with subtle rusted spots, and a faded floral thimble. Afternoon natural window sunlight glints off the polished iron wheel and highlights the delicate matte polymer finish and loving smile lines of the grandmother, evocative of decades of humble craftsmanship, motherly devotion, and unforgotten domestic warmth. Shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/3.5, rich tactile textures of aged iron, peeling wood, and SSS resin, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 05：【煽情场景四·晨曦静好】窗台花草·微风晨光 · 【Gemini 专属】
```text
Vertical 3:4 composition. A serene, highly healing interior photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese kitchen grandmother standing peacefully on an aged natural wooden windowsill in a sun-drenched home balcony. Beside the tiny figurine sits a flourishing green potted clivia plant with broad glossy leaves in a celadon ceramic pot, and a gentle morning breeze lightly billows a sheer white linen curtain. Golden 6:30 AM dawn sunlight streams through creating delicate Tyndall sunbeams with tiny dancing dust particles, soft luminous golden backlight illuminates grandmother's silver hair and creates a gentle translucent SSS amber glow through the resin cheek contours, breathing pure peaceful serenity and eternal quiet love. Shot on Hasselblad X2D 100C with 90mm f/2.8 lens at f/2.8, creamy background bokeh, authentic Kodak Portra 400 film tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 06：【煽情场景五·风雨归人】玄关守望·长明灯与老钥匙 · 【Gemini 专属】
```text
Vertical 3:4 composition. An intensely touching, comforting domestic documentary photograph of the 6cm miniature 3D printed full-color resin bust figurine of the Chinese kitchen grandmother, standing peacefully upon a dark solid walnut entryway shoe cabinet beside the front door. Right beside the figurine lies a well-worn keyring with brass house keys polished smooth by decades of handling, and a small yellowed memo paper with a few lines of faded, illegible handwriting. A gentle 2700K warm incandescent wall sconce above casts a soft golden cone of light, warmly illuminating grandmother's gentle smile and creating soothing amber resin translucency (SSS) and a gentle elongated shadow on the wooden surface, symbolizing the eternal comfort of someone always keeping a light on for you upon returning home. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, cozy evening atmosphere, authentic Kodak Portra 400 analog grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

### 视角 07：【煽情场景六·掌心凝视】掌心凝视·思念具象 · 【Gemini 专属】
```text
Vertical 3:4 composition. A deeply touching candid lifestyle photograph of an adult Chinese grandchild's warm cupped hands gently holding the 6cm miniature full-color 3D printed resin bust figurine of their beloved late Chinese grandmother wearing a navy floral apron and silver hair bun. The tiny figurine rests comfortably in the center of the palm, creating an emotional scale contrast between real human palm skin textures and the intricate 6cm miniature resin craft. Soft emotional natural daylight streams through a domestic living room window, with a shallow depth of field and a warm cozy blurred home interior, nostalgic affectionate color grading, authentic emotional resonance, quiet remembrance. Leave clean negative space in the upper third for a title overlay. Shot on Canon EOS R5 with RF 85mm f/1.4 lens at f/2.8, authentic 35mm Kodak Portra 400 film grain, natural shadows. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, distorted human fingers, extra fingers, missing fingers, creepy atmosphere, eerie smile, caucasian, western features, harsh flash, plastic skin.
```

### 视角 08：【煽情场景七·生活遗存】人间烟火·灶台重逢 · 【Gemini 专属】
```text
Vertical 3:4 composition. A poignant, deeply nostalgic documentary still-life photograph of the 6cm miniature 3D printed full-color bust figurine of the Chinese kitchen grandmother wearing a navy floral apron and silver hair bun, placed tenderly on a weathered wooden cutting board on an old kitchen countertop. Beside the tiny figurine sits a vintage stainless steel soup pot with a faint wisp of rising steam, a worn wooden rolling pin, and an antique floral porcelain bowl with a pinch of white flour. Golden morning sunbeams cut through kitchen window blinds, illuminating tiny floating dust particles, casting long warm shadows, evoking rich domestic nostalgia and a sense of eternal loving presence. Shot on Canon EOS R5 with RF 50mm f/1.8 lens at f/2.8, rich atmospheric depth, Kodak Portra 400 film tone. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, messy clutter, harsh flash, exaggerated steam, shiny plastic, caucasian, western features, artificial gloss.
```

### 视角 09：【煽情场景八·深夜陪伴】深夜床头·台灯守候 · 【Gemini 专属】
```text
Vertical 3:4 composition. A quiet, comforting nighttime interior photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese kitchen grandmother standing peacefully on a dark solid wood bedside nightstand. Beside the figurine rests a warm 2800K tungsten gooseneck bedside reading lamp, an open vintage book, and a retro brass mechanical alarm clock. Warm golden lamplight gently kisses the side of the grandmother's smiling resin face, creating soft glowing subsurface scattering (SSS) highlights and gentle comforting shadows across the wood grain, evoking a soothing atmosphere of grief solace, silent eternal love, and tranquil remembrance. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, delicate shadow details, Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, creepy dark shadows, blown out lamp highlights, harsh noise, digital glow, caucasian, western features, plastic skin.
```

### 视角 10：【煽情场景九·时光重叠】老相册对话·立体相逢 · 【Gemini 专属】
```text
Vertical 3:4 composition. An emotionally resonant, nostalgic macro photograph showing the miniature 6cm full-color 3D printed bust figurine of the Chinese grandmother placed affectionately right beside an opened vintage 1980s cloth-bound photo album. In the album, a slightly faded, yellowed black-and-white corner-mounted photograph shows the same Chinese grandmother in her 30s standing in an old courtyard. The modern 3D miniature bust figurine and the flat historical photograph gaze toward each other, creating a powerful juxtaposition of flat memory transforming into tangible 3D reality, soft natural afternoon window light, gentle dust motes, rich tactile paper and resin textures, bittersweet nostalgia, tangible love across time. Leave clean negative space in the upper third for a title overlay. Shot on Canon EOS R5 with RF 85mm f/2 Macro lens at f/3.2, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, modern digital photo album, oversaturated colors, distorted hands, harsh flash, caucasian, western features, plastic skin.
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
52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key
```

---

#### 视角 00：【基底定妆照】真实父亲生活写实摄影 (正脸半身胸像 · 强制 Keep the upper body) · 【Midjourney 专属】
> **信噪比指标**：正向 51 词（显式包含 **`Keep the upper body`**，完整嵌入 17 词 IFTS），负向 15 词（包含 **`English`** 拦截），总词数 69 词。精准锁定当代中国 50 岁出头勤劳坚毅老爸形象。
```text
Candid documentary portrait of a real 52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key, Keep the upper body, resting near highway truck stop, wearing dark charcoal canvas jacket, soft overcast morning daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
```

#### 视角 01：【模型标准像】0° 正面微缩手办棚拍 (依靠 00 微调成 3D 模型 · 强制 Keep the upper body) · 【Midjourney 专属】
> **微调置换原则**：首句声明 3D 模型实体并显式注入 **`Keep the upper body`**，**100% 逐字原样继承 17 词 IFTS 序列**，服装前追加 `sculpted`，底座置换为微倒角工艺品深色底座，风格化参数降为 `--s 50`。
```text
Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body, 52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key, sculpted dark charcoal canvas jacket, mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
```

#### 🔍 视角 00 ➔ 视角 01 微调置换与 IFTS 一致性对齐表 (Prompt Mutation Diff)
| 维度类别 | 视角 00 原文 Token (写实原片) | 视角 01 微调 Token (3D 模型) | 继承与微调对齐机制 |
| :--- | :--- | :--- | :--- |
| **主体媒介与景别** | `Candid documentary portrait of a real ... Keep the upper body` | `Macro studio photo of a 3D model, 6.0cm 3D printed painted resin bust, Keep the upper body` | 算子 ① 置换：显式声明 3D 打印树脂胸像并锁定 `Keep the upper body`，剥离摄影定性 |
| **人物指纹 (IFTS)** | `52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key` | `52-year-old Chinese father, square rugged jawline, salt-and-pepper cropped hair, weathered laugh lines, tired resilient eyes, worn freight truck key` | **100% 逐字原样绝对继承（0 差异）**，锁定骨相神态 |
| **环境底座** | 真实生活或室外自然光照 | `mounted on dark beveled pedestal base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus` | 算子 ③ 置换：生活背景置换为一体化工艺品底座与无缝浅灰影棚 |
| **参数配比** | `--s 80` | `--s 50` | 算子 ④ 调控：手办降噪控制发散，压制 AI 自由重绘面部 |
| **负向拦截** | `--no English, anime, 3d render, CGI, doll...` | `--no English, real living human, skin pores, plaster, stone column...` | 算子 ④ 置换：统一挂载 `English` 杜绝英文字符，01 剔除 3D 拦截词并反向针对性拦截活人与石膏柱 |

#### 视角 02：【煽情场景一·专属老座】午后空椅·日光守望 · 【Gemini 专属】
```text
Vertical 3:4 composition. A poignant domestic documentary photograph showing the 6cm miniature 3D printed full-color resin bust figurine of the 52-year-old freight driver father with salt-and-pepper cropped hair and dark charcoal jacket, placed tenderly on a weathered wooden side table in an old apartment living room. Beside the tiny figurine rests his scratched stainless steel insulated thermos flask and folded metal reading glasses. In the soft-focus middle ground stands an empty, worn black faux-leather armchair. Afternoon golden sunlight slants through sheer curtains, illuminating floating dust motes and creating amber resin subsurface scattering (SSS) warmth on father's gentle face, evoking peaceful loving memories. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic Kodak Portra 400 film tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 03：【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀 · 【Gemini 专属】
```text
Vertical 3:4 composition. A solemn, deeply respectful documentary photograph showing the 6cm miniature 3D printed full-color resin bust figurine of the 52-year-old freight driver father with salt-and-pepper hair and charcoal jacket, honorably displayed on the middle-upper shelf of a modern walnut glass-door display cabinet in a home study room. The display shelf sits at eye-level, slightly elevated to convey profound filial piety and reverence while allowing intimate daily remembrance. Beside the bust figurine rests his well-worn freight truck keys and his scratched stainless steel insulated thermos. A gentle focused warm reading lamp from above illuminates the cabinet interior, casting soft reflections on the transparent glass door and warm translucent resin subsurface scattering (SSS) highlights across father's hardworking, gentle face. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, authentic Kodak Portra 400 film tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 04：【煽情场景三·岁月手艺】旧物深情·生锈时光 · 【Gemini 专属】
```text
Vertical 3:4 composition. A poignant still-life documentary photograph showing the 6cm miniature 3D printed resin bust figurine of the 52-year-old truck driver father sitting affectionately on top of a distressed, oily industrial metal tool chest in a garage. Next to the figurine rests an authentic vintage heavy steel mechanic wrench with surface rust and a roll of black electrical tape. Crisp natural window sunlight grazes the textured iron surface, creating a touching contrast between the rugged mechanic tools and the soft resin translucency of father's loving smile. Shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/3.2, rich industrial patina, Kodak Portra 400 analog grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 05：【煽情场景四·晨曦静好】窗台花草·微风晨光 · 【Gemini 专属】
```text
Vertical 3:4 composition. A peaceful, healing interior photograph of the miniature 6cm 3D printed full-color resin bust figurine of the Chinese truck driver father standing serenely on a sun-drenched natural wooden windowsill. Next to the figurine sits a healthy green potted money plant in a ceramic pot. A gentle morning breeze stirs a sheer white linen curtain, while 6:30 AM golden sunbeams create delicate Tyndall light rays with floating dust motes, casting an amber resin subsurface scattering (SSS) glow across father's cheek. Shot on Hasselblad X2D 100C with 90mm f/2.8 lens at f/2.8, creamy background bokeh, authentic Kodak Portra 400 tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 06：【煽情场景五·风雨归人】玄关守望·长明灯与老钥匙 · 【Gemini 专属】
```text
Vertical 3:4 composition. A deeply comforting domestic documentary photograph of the 6cm miniature 3D printed resin bust figurine of the 52-year-old Chinese father, standing peacefully on a dark solid walnut entryway console beside the front door. Right beside the figurine rests his well-worn freight truck key with a red and yellow woven lanyard, and a small yellowed handwritten note with faded, illegible writing. A warm 2700K incandescent sconce casts a soft golden cone of light, illuminating father's gentle smile and creating soothing amber resin SSS translucency. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, cozy evening mood, authentic Kodak Portra 400 grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 07：【煽情场景六·掌心温存】掌心凝视·思念具象 · 【Gemini 专属】
```text
Vertical 3:4 composition. A deeply moving candid lifestyle photograph of an adult son's warm cupped hands gently holding the 6cm miniature full-color 3D printed resin bust figurine of his late 52-year-old freight driver father. The tiny figurine rests snugly in the center of the palm, showcasing a poignant scale contrast between real human palm skin textures and the intricate painted resin sculpture. Soft emotional daylight streams from a nearby window, creating tender nostalgic atmosphere, shot on Canon EOS R5 with RF 85mm f/1.4 lens at f/2.8, shallow depth of field, authentic Kodak Portra 400 film grain. Leave clean negative space in the upper third for a title overlay. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 08：【煽情场景七·生活遗存】人间烟火·灶台重逢 · 【Gemini 专属】
```text
Vertical 3:4 composition. A poignant still-life documentary photograph showing the 6cm miniature 3D printed bust figurine of the 52-year-old truck driver father placed tenderly on a weathered kitchen countertop next to a seasoned black iron wok with rising swirls of savory cooking steam. Beside the figurine sits an old white porcelain bowl and freshly peeled garlic cloves. Morning golden light cuts through the kitchen window blinds, casting warm atmospheric dust rays and giving father's resin face an affectionate lifelike presence in the domestic smoke. Shot on Canon EOS R5 with RF 50mm f/1.8 lens at f/2.8, authentic Kodak Portra 400 film tone. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 09：【煽情场景八·深夜陪伴】深夜床头·台灯守候 · 【Gemini 专属】
```text
Vertical 3:4 composition. A quiet, deeply comforting nighttime interior photograph of the miniature 6cm 3D printed resin bust figurine of the 52-year-old father resting peacefully on a dark wooden bedside table. Beside the figurine stands a warm 2800K tungsten gooseneck reading lamp and a worn handwritten driver logbook showing highway routes. Gentle amber light kisses father's resin cheek, casting soft comforting shadows across the wood surface, conveying peaceful remembrance and eternal loving vigilance. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, delicate shadow details, Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 10：【煽情场景九·时光重叠】老相册对话·立体相逢 · 【Gemini 专属】
```text
Vertical 3:4 composition. An emotionally resonant macro photograph showing the 6cm miniature 3D printed full-color bust figurine of the 52-year-old freight driver father placed affectionately right beside an opened vintage 1990s red cloth-bound photo album. On the yellowed album page, an authentic corner-mounted vintage color photograph shows father in his early 20s smiling proudly in front of his first green cargo truck. The tangible 3D resin figurine and the flat historical photo gaze toward each other, turning flat memories into a tangible companion across decades. Leave clean negative space in the upper third for a title overlay. Shot on Canon EOS R5 with RF 85mm f/2 Macro lens at f/3.2, authentic Kodak Portra 400 grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
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
> **指标与信噪比**：正向 48 词（显式包含 **`full-body portrait`** 与 **`full-body view`**，完整嵌入 16 词 IFTS），负向 15 词（包含 **`English`** 拦截），总词数 68 词。严格遵照《Midjourney V8.x 核心参数与高级指令全景说明》配置 `--ar 1:1 --style raw --s 80 --v 8`。
```text
Candid documentary full-body portrait of a real 51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella, standing near school gate in light rain, full-body view, wearing dark navy windbreaker, wet gray trousers, black rain boots, soft overcast rainy daylight, Hasselblad 90mm f/3.2, Kodak Portra 400 film grain --ar 1:1 --style raw --s 80 --v 8 --no English, anime, 3d render, CGI, doll, figurine, plastic skin, beauty filter, western, young, deformed hands
```

#### 视角 01：【模型标准像】0° 正面微缩全身手办棚拍 (依靠 00 微调成 3D 模型) · 【Midjourney 专属 · 强制包含 full-body】
> **微调置换与 full-body 约束**：首句声明 **`12.0cm 3D printed painted resin full-body model`**，**100% 逐字原样继承 16 词 IFTS 序列**，服装前追加 `sculpted`，底座声明 **`full-body standing on weighted circular base`**，风格化参数依说明文档降为 `--s 50`。正向 49 词，负向 16 词（包含 **`English`** 拦截），总词数 69 词。
```text
Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model, 51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella, sculpted dark navy windbreaker, trousers and rain boots, full-body standing on weighted circular base, subtle resin SSS finish, light gray cyclorama, softbox lighting, RF 100mm f/8 focus --ar 1:1 --style raw --s 50 --v 8 --no English, real living human, skin pores, plaster, stone column, room, furniture, outdoor, western, young, deformed hands
```

#### 🔍 视角 00 ➔ 视角 01 微调置换与 IFTS 一致性对齐表 (Prompt Mutation Diff)
| 维度类别 | 视角 00 原文 Token (写实原片) | 视角 01 微调 Token (3D 模型) | 继承与微调对齐机制 |
| :--- | :--- | :--- | :--- |
| **主体媒介** | `Candid documentary full-body portrait of a real` | `Macro studio photo of a 3D model, 12.0cm 3D printed painted resin full-body model,` | 算子 ① 置换：显式声明 12cm 全身 3D 模型，锁定 full-body |
| **人物指纹 (IFTS)** | `51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella` | `51-year-old Chinese father, weathered cheekbones, tired loving eyes, graying temples cropped hair, holding long black umbrella` | **100% 逐字绝对原样继承（0 差异）**，骨相、神态与手持雨伞信物绝对锁定 |
| **全身姿态底座** | `standing near school gate in light rain, full-body view, wearing dark navy windbreaker, wet gray trousers, black rain boots` | `sculpted dark navy windbreaker, trousers and rain boots, full-body standing on weighted circular base` | 算子 ② & ③ 置换：服装雕塑化，环境置换为全身加重配重圆形底座与浅灰影棚 |
| **参数配比** | `--s 80` | `--s 50` | 算子 ④ 调控：手办低自由度降噪，压制面部与全身比例漂移 |
| **负向拦截** | `--no English, anime, 3d render, CGI, doll...` | `--no English, real living human, skin pores, plaster, stone column...` | 算子 ④ 置换：统一挂载 `English` 杜绝英文字符，01 剔除 3D 负向词并反向拦截活人与石膏柱 |

#### 视角 02：【煽情场景一·专属老座】午后空椅·日光守望 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A poignant domestic documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father with graying temples, standing quietly beside an empty weathered bamboo rocking chair in the corner of a living room. Next to the full-body figurine on a low stool rests an old thermos flask and a dry towel. Soft afternoon window daylight falls across the empty chair and illuminates father's gentle smiling face with warm amber resin SSS translucency. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic Kodak Portra 400 tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 03：【煽情场景二·尊崇敬奉】书房多宝阁·视平瞻怀 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A poignant, dignified domestic documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father in navy windbreaker standing quietly on the middle-upper tier of a traditional rosewood curio shelf (duobaoge) in a quiet study. The shelf is positioned at eye level, commanding respectful remembrance and family dignity. Beside the full-body figurine rests a vintage fountain pen and an old leather-bound notebook. Soft 2800K warm interior ambient light and subtle accent illumination highlight father's composed posture and loving facial contours with gentle amber resin SSS translucency, symbolizing enduring respect and intergenerational memory. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.2, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 04：【煽情场景三·岁月手艺】旧物深情·生锈时光 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A touching still-life documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing affectionately on an old wooden repair workbench. Beside the full-body figurine rests a weathered bicycle pump, replacement inner tube patches, and an antique pair of pliers. Natural window sidelight highlights the rugged tools and casts soft golden amber SSS glow across father's resin face, honoring a lifetime of humble manual labor and family devotion. Shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/3.2, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 05：【煽情场景四·晨曦静好】窗台花草·微风晨光 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A peaceful, healing morning interior photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father standing serenely on a sunlit natural wooden balcony windowsill. Next to the full-body figurine sits a potted blooming jasmine plant in an earthen pot. A gentle dawn breeze stirs a light linen curtain while 6:30 AM golden Tyndall sunbeams illuminate floating dust specks, bathing the full-body figurine in warm amber resin translucency (SSS). Shot on Hasselblad X2D 100C with 90mm f/2.8 lens at f/2.8, creamy bokeh, authentic Kodak Portra 400 tones. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 06：【煽情场景五·风雨归人】玄关守望·长柄伞与老钥匙 · 【Gemini 专属 · 全身手办场景】
> **自然语言流**：描述微缩手办实体时显式注明 **`full-body figurine`**，与真实玄关老信物形成空间拓扑联动。
```text
Vertical 3:4 composition. An intensely touching domestic documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old Chinese father with graying temples, standing peacefully upon a dark solid walnut entryway shoe cabinet beside the front door. Right beside the full-body figurine leans his vintage long black umbrella with dripping raindrops on a ceramic tray, a brass house key, and a small yellowed memo note with faded, illegible writing. A gentle 2700K warm incandescent wall sconce above casts a soft golden cone of light, warmly illuminating father's gentle smile lines and creating soothing amber resin translucency (SSS) and a soft elongated shadow on the wood grain, capturing the eternal warmth of father waiting for you in the rain. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 07：【煽情场景六·掌心温存】掌心凝视·思念具象 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A deeply moving candid lifestyle photograph of an adult daughter's two open cupped hands gently cradling the 12cm miniature full-color 3D printed full-body resin figurine of her late 51-year-old father standing peacefully in his navy windbreaker with long umbrella. The full-body figurine stands in the center of her palms, creating a poignant scale contrast between real human hand skin textures and the intricate miniature painted resin sculpture. Soft emotional natural daylight streams from a window, conveying quiet grief solace and tender gratitude. Leave clean negative space in the upper third for a title overlay. Shot on Canon EOS R5 with RF 85mm f/1.4 lens at f/2.8, shallow depth of field, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 08：【煽情场景七·生活遗存】人间烟火·灶台重逢 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A poignant still-life documentary photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing tenderly on a weathered wooden dining table in a cozy home kitchen. Beside the full-body figurine sits a steaming hot bowl of homemade noodle soup with a fried egg and sliced scallions, and a pair of bamboo chopsticks resting on a small ceramic chopstick holder. Morning sunlight cuts through window blinds creating warm atmospheric dust rays, evoking the feeling of a loving father who just came home to share a warm meal. Shot on Canon EOS R5 with RF 50mm f/1.8 lens at f/2.8, authentic Kodak Portra 400 film tone. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 09：【煽情场景八·深夜陪伴】深夜床头·台灯守候 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. A quiet, comforting nighttime interior photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing peacefully on a dark solid walnut bedside nightstand. Beside the full-body figurine stands a warm 2800K tungsten gooseneck lamp and an open notebook with a pen. Soft golden lamplight illuminates father's kind smiling face, casting an elongated gentle shadow across the wood grain, creating soothing amber resin SSS translucency and a sense of eternal paternal protection in the quiet night. Shot on Canon EOS R5 with RF 50mm f/1.4 lens at f/2.0, shallow depth of field, Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, broken geometry.
```

#### 视角 10：【煽情场景九·时光重叠】老相册对话·立体相逢 · 【Gemini 专属 · 全身手办】
```text
Vertical 3:4 composition. An emotionally resonant macro photograph showing the 12cm miniature full-color 3D printed full-body resin figurine of the 51-year-old father standing affectionately right beside an opened vintage 1990s cloth photo album on a desk. On the yellowed album page, a faded corner-mounted color photograph shows the same father in his 20s smiling proudly holding his infant baby daughter in an old courtyard. The tangible 3D full-body figurine and the flat historical photo gaze toward each other, bridging decades of selfless fatherly love into a tangible companion. Leave clean negative space in the upper third for a title overlay. Shot on Canon EOS R5 with RF 85mm f/2 Macro lens at f/3.2, authentic Kodak Portra 400 film grain. Avoid: English text, letters, anime, cartoon, 3d digital render, CGI, modern digital photo album, oversaturated colors, distorted hands, harsh flash, caucasian, western features, plastic skin.
```

---
