# GitHub 开源微缩手办与场景摆拍全景蒸馏矩阵 (Diorama & Toy Staging Master Matrix)

> **v5 归属说明**：本文件原属 xiaohongshu 文案技能，v5 起随视觉职责迁入 fullcolor，作为视角 02–10 的**场景变奏素材库**（规则见 `scene-library.md` 第 3 节）。
> 用于小红书笔记的场景图统一 **3:4 竖构图**、Gemini 负向统一含 `English text, letters`、不写可读文字、不放灵堂/供桌意象（见 `prompt-engineering-spec.md` 铁律二、铁律八）。

本文件深度蒸馏了 GitHub 开源社区（Flux Garage Kit、Midjourney Collectible Photography、SDXL Toy Diorama、Civitai Miniature Staging）与业内顶级商业静物/微缩摄影师的布景技术。

彻底解决传统 AI 生图**“千篇一律的手捧手办”、“背景永远是单调电脑桌”、“缺乏生活叙事与道具”**的单调拉垮问题，建立 **23,400 种组合的高质感动态摆拍矩阵**！

---

## 🏗️ 4 层场景解构与重组协议 (4-Layer Staging Framework)

每一次生成微缩同框与手办实拍大片，必须由以下 **4 层物理级要素** 复合构建而成：

```
┌────────────────────────────────────────────────────────────────────────┐
│ 第 1 层：主体手办材质与底座 (Subject, Scale & Base Medium)              │
│  - 1/7 scale miniature 6cm 3D printed full-color resin figurine        │
│  - delicate matte polymer finish, hand-painted micro-details, SSS      │
│  - 底座选项：透明亚克力底座 / 原木胡桃木底盘 / 微缩石阶 / 真实物理桌面接触  │
├────────────────────────────────────────────────────────────────────────┤
│ 第 2 层：12 大高质感生活与情感实景空间 (12 Multi-Environment Scenarios) │
│  ① 怀旧老宅木窗台   ② 现代极简深夜书房   ③ 户外庭院与青苔石阶           │
│  ④ 匠人创作工作台   ⑤ 旅途与汽车中控台   ⑥ 婚礼主桌与仪式花艺台         │
│  ⑦ 温馨床头与夜灯角 ⑧ 老式厨房与灶台窗边 ⑨ 阳台竹椅与晾晒衣物           │
│  ⑩ 书页与老相册内页 ⑪ 雨后车窗与后座     ⑫ 节庆餐桌与团圆空位           │
├────────────────────────────────────────────────────────────────────────┤
│ 第 3 层：13 大情感叙事道具锚点矩阵 (13 Narrative Prop Anchor Sets)     │
│  A. 岁月时光组 (怀表/泛黄照片/旧日记)  B. 温情生活组 (顶针/毛衣/老花镜) │
│  C. 品茗茶香组 (紫砂壶/白瓷茶杯/茶叶)  D. 求学奋斗组 (奖状/钢笔/厚书籍) │
│  E. 自然庭院组 (红枫落叶/松果/微盆景)  F. 仪式纪念组 (丝绸缎带/玻璃展示罩)│
│  G. 科技温情组 (微光手机老照片/键盘)   H. 匠心工坊组 (调色盘/细笔/切割垫)│
│  I. 烟火厨房组 (粗陶碗/竹蒸笼/青菜)    J. 戏曲收音组 (老收音机/戏票/茶缸)│
│  K. 农事土地组 (斗笠/锄柄/稻谷)        L. 病榻守望组 (药盒/保温杯/日历) │
│  M. 童年记忆组 (铁皮玩具/弹珠/旧课本)                                  │
├────────────────────────────────────────────────────────────────────────┤
│ 第 4 层：10 大电影级光影与天气氛围 (10 Cinematic Lighting & Moods)     │
│  Ⅰ. 晨曦黄金时刻   Ⅱ. 阴雨天窗边漫射   Ⅲ. 暖琥珀复古台灯/烛光         │
│  Ⅳ. 神圣丁达尔光束 Ⅴ. 暮色蓝调时分     Ⅵ. 极简摄影棚柔光箱           │
│  Ⅶ. 清晨冷调薄雾   Ⅷ. 硬光窗格投影     Ⅸ. 烛火摇曳暖焰               │
│  Ⅹ. 雨窗霓虹散射                                                      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🌆 7 大高质感实景空间与专属 Prompt 模块

### 场景 1：【怀旧老宅木窗台】(Rustic Sunlit Window Sill)
* **环境描述**：斑驳的复古实木窗台，窗外是微风吹拂的绿树庭院，阳光透过木格窗洒在原木纹理上。
* **Prompt 片段**：
```text
placed on a weathered rustic oak windowsill in an old peaceful courtyard house, soft green foliage and gentle morning sunlight visible through the wooden window frame, warm dust motes floating in the air.
```

### 场景 2：【现代极简深夜书房】(Modern Minimalist Study Desk)
* **环境描述**：深色胡桃木办公桌，旁边放着一本翻开的书、一杯温热的咖啡与一台微光笔记本电脑。
* **Prompt 片段**：
```text
standing on a clean minimalist dark walnut study desk, beside a steaming ceramic coffee mug, an open hardcover notebook with handwritten notes, and a sleek laptop glowing softly in the background.
```

### 场景 3：【户外庭院与青苔石阶】(Outdoor Garden & Mossy Stone)
* **环境描述**：户外自然庭院，古朴的青石板台阶，周围点缀着微型青苔、几枚散落的秋日红枫落叶与清晨露珠。
* **Prompt 片段**：
```text
standing on a natural moss-covered garden stone step, surrounded by crisp miniature fallen autumn maple leaves and glistening morning dew drops, soft natural overcast daylight.
```

### 场景 4：【匠人创作工作台】(Artisan Craft Studio)
* **环境描述**：专业手工模型工作室，深绿色网格切割垫板、000号精细面相笔、丙烯颜料小瓶、微型镊子与游标卡尺。
* **Prompt 片段**：
```text
positioned on a green self-healing hobby cutting mat in an artist's miniature workshop, surrounded by fine 000 detail paint brushes, tiny acrylic paint jars, tweezers, and miniature sculpting tools.
```

### 场景 5：【旅途与汽车中控台】(Car Dashboard Travel Companion)
* **环境描述**：汽车皮质中控台上方，窗外是落日余晖或掠过的公路风景，象征“你陪我看遍世间山海”。
* **Prompt 片段**：
```text
securely standing on the leather dashboard of a car, golden sunset streaming through the front windshield, scenic blurred highway and mountain landscape in the distance outside.
```

### 场景 6：【婚礼主桌与仪式花艺台】(Wedding Reception Floral Centerpiece)
* **环境描述**：高雅浪漫的婚礼餐桌，白色丝绸缎带、盛开的白玫瑰与尤加利叶花艺、晶莹的高脚香槟杯。
* **Prompt 片段**：
```text
delicately placed among fresh white roses, eucalyptus leaves, and shimmering crystal champagne glasses on an elegant white silk wedding reception table, romantic soft bokeh.
```

### 场景 7：【温馨床头与夜灯角】(Cozy Bedside Table at Night)
* **环境描述**：静谧温馨的卧室床头柜，米白色亚麻灯罩台灯散发着温暖柔光，旁边放着一杯温水与老花镜。
* **Prompt 片段**：
```text
placed on a cozy wooden bedside nightstand, bathed in the soft warm glow of a fabric bedside lamp, beside a pair of folded vintage reading glasses and a small glass of water, peaceful tranquil mood.
```

### 场景 8：【老式厨房与灶台窗边】(Vintage Kitchen Counter)
* **环境描述**：老宅厨房的水磨石灶台边，粗陶碗碟、竹制蒸笼与一束刚洗过的青菜，窗外是清晨的邻里巷弄。
* **适用情感**：奶奶/外婆的烟火气、"再吃一口她做的饭"
* **Prompt 片段**：
```text
standing on a worn terrazzo kitchen counter in an old family home, beside a coarse ceramic bowl, a bamboo steamer basket, and a bundle of freshly washed greens, soft morning light from a small kitchen window, faint steam in the air.
```

### 场景 9：【阳台竹椅与晾晒衣物】(Balcony Rattan Chair & Drying Laundry)
* **环境描述**：老式阳台的竹编藤椅扶手，身后是随风轻摆的晾晒衬衫与一盆茉莉，午后阳光斜照。
* **适用情感**：爷爷的午后小憩、日常烟火、"他总坐在那儿"
* **Prompt 片段**：
```text
resting on the woven armrest of a vintage rattan chair on an old apartment balcony, sun-dried cotton shirts gently swaying on a laundry line behind, a potted jasmine plant nearby, warm slanted afternoon sunlight.
```

### 场景 10：【书页与老相册内页】(Open Photo Album Page)
* **环境描述**：手办直接站在摊开的老相册内页上，周围是压在塑料膜下的泛黄照片与手写注脚。
* **适用情感**：从平面走向立体的视觉隐喻、"她从照片里走出来了"
* **Prompt 片段**：
```text
standing directly on the open page of a worn family photo album, surrounded by yellowed photographs under aging plastic film and handwritten date annotations in faded blue ink, soft diffused overhead light.
```

### 场景 11：【雨后车窗与后座】(Rainy Car Window & Back Seat)
* **环境描述**：雨后汽车后座的皮质扶手，车窗上挂满水珠，窗外是模糊的城市霓虹光斑。
* **适用情感**：归途、思念在路上、都市孤独治愈
* **Prompt 片段**：
```text
placed on the leather armrest of a car back seat, rain-beaded side window behind with blurred city bokeh lights outside, cool moody reflections on the window glass, intimate enclosed atmosphere.
```

### 场景 12：【节庆餐桌与团圆空位】(Festive Dining Table Empty Seat)
* **环境描述**：年夜饭或团圆餐桌一角，手办被放在那个空出来的座位前，旁边是一副没人动过的碗筷。
* **适用情感**：团圆缺席的巨大遗憾、年节催泪爆点
* **Prompt 片段**：
```text
placed at an empty seat of a warm family reunion dinner table, an untouched pair of chopsticks resting on a porcelain bowl beside, softly blurred festive dishes and family hands in the background, warm tungsten dining light.
```

---

## 📦 8 大情感叙事道具锚点配方库 (Storytelling Props)

| 道具组别 | 核心道具要素 | 适用情感场景 | 英文 Prompt 注入词 |
| :--- | :--- | :--- | :--- |
| **A. 岁月时光** | 停走的机械怀表、泛黄老相框、硬皮笔记本 | 爷爷/外公/岁月沉淀 | `beside a stopped vintage brass pocket watch and a framed faded black-and-white family portrait` |
| **B. 温情生活** | 金属缝纫顶针、折叠老花镜、手织毛线团 | 奶奶/外婆/母爱细碎 | `next to a silver sewing thimble, a pair of folded tortoise-shell reading glasses, and cozy knitted yarn` |
| **C. 品茗茶香** | 宜兴紫砂小壶、白瓷茶杯（带微热白汽）、干茶叶 | 长辈闲坐/茶韵悠长 | `alongside a miniature Yixing clay teapot, a tiny white porcelain teacup with rising delicate steam wisps` |
| **D. 求学奋斗** | 泛黄奖状、英雄钢笔、厚重经典书典 | 父亲寄语/成长励志 | `beside an open hardcover dictionary, a vintage fountain pen, and a folded honorable certificate` |
| **E. 自然庭院** | 几片红枫落叶、小松果、微型多肉盆栽 | 户外治愈/四季流转 | `adorned with a real crisp dried autumn maple leaf, a tiny pinecone, and a small potted succulent plant` |
| **F. 仪式纪念** | 纯白丝绸丝带、精致玻璃罩钟(Cloche)、珍珠胸针 | 婚礼见证/高端礼盒 | `encased in an elegant glass display cloche dome with a wooden base, accented with ivory satin ribbon` |
| **G. 科技温情** | 发光手机显示老合影、机械键盘、无线鼠标 | 现代案头/跨时空连接 | `standing directly on an illuminated smartphone screen displaying an old scanned sepia photo` |
| **H. 匠人手工** | 调色盘、极细面相笔尖、微型打磨砂纸 | 定制过程/匠心打造 | `with a fine artist brush tip gently pointing toward the figurine, tiny acrylic color palette nearby` |
| **I. 烟火厨房** | 粗陶碗、竹蒸笼、一把青菜、旧铝勺 | 奶奶的饭菜香/生活气 | `beside a coarse ceramic bowl, a miniature bamboo steamer, and a worn aluminum spoon on a kitchen counter` |
| **J. 戏曲收音** | 老式收音机、戏票根、搪瓷茶缸 | 爷爷听戏/老派生活情趣 | `next to a vintage bakelite radio, a faded opera ticket stub, and an enamel tea mug with chipped rim` |
| **K. 农事土地** | 竹编斗笠、锄头木柄、一捧稻谷 | 务农长辈/土地情结/沉默付出 | `alongside a small woven bamboo hat, a weathered wooden tool handle, and a scattered handful of rice grains` |
| **L. 病榻守望** | 折叠轮椅、药盒、保温杯、日历 | 陪护记忆/最后的时光 | `beside a small pill organizer box, a thermos cup, and a wall calendar with a circled date` |
| **M. 童年记忆** | 铁皮青蛙、玻璃弹珠、糖纸、旧课本 | 隔辈亲/被长辈带大的童年 | `surrounded by a tin wind-up toy, glass marbles, a folded candy wrapper, and a dog-eared childhood textbook` |

---

## 💡 10 大电影级光影氛围配方库 (Atmospheric Lighting)

1. **晨曦黄金时刻 (`Golden Hour`)**:
   `warm 4500K golden sunlight streaming from side window, long soft cast shadows, luminous rim lighting on hair and edges, Kodak Portra 400 film tone.`
2. **阴雨天窗边漫射 (`Rainy Day Melancholy`)**:
   `soft cool overcast daylight diffused through a rainy glass window with visible water droplets, gentle contrast, moody and introspective atmosphere.`
3. **暖琥珀复古台灯 (`Amber Lamp / Candlelight`)**:
   `warm 2800K amber incandescent pool of light from a vintage brass desk lamp, deep soft shadows, cozy intimate late-night atmosphere.`
4. **神圣丁达尔光束 (`Volumetric God Rays`)**:
   `volumetric god rays piercing through wooden window blinds, visible airborne dust particles dancing in the light beam, dramatic chiaroscuro contrast.`
5. **暮色蓝调时分 (`Blue Hour Twilight`)**:
   `cinematic blue hour twilight visible outside the window contrasting with the warm golden indoor lamp light, dual color temperature cinematic depth.`
6. **极简摄影棚柔光箱 (`Studio Softbox Magazine`)**:
   `clean neutral studio lighting, large octabox diffused soft light, subtle gradient background, high-end editorial product photography quality.`
7. **清晨冷调薄雾 (`Cool Morning Haze`)**: ❄️ 冷调
   `cool 6500K pale morning light through thin mist, low contrast desaturated palette, soft blue-gray shadows, quiet melancholic stillness.`
8. **硬光窗格投影 (`Hard Window Grid Shadow`)**: ⚡ 硬光
   `crisp hard directional sunlight casting sharp geometric window-frame shadow patterns across the surface and the figurine, high contrast, strong defined shadow edges, graphic composition.`
9. **烛火摇曳暖焰 (`Flickering Candlelight`)**: 🔥 极暖弱光
   `single warm 1900K candle flame as the only light source, soft falloff into deep darkness, gentle warm flicker on the figurine's face, intimate ritual atmosphere.`
10. **雨窗霓虹散射 (`Neon Rain Bokeh`)**: 🌃 冷调夜景
   `cool cinematic night ambience, out-of-focus city neon bokeh through a rain-streaked window, subtle teal and magenta color separation, reflective wet surfaces.`

> **光影冷暖配比铁律**：同批 N ≥ 3 张图时，**必须至少包含 1 种冷调光影**（编号 2 / 5 / 7 / 10）。
> 全暖光是"看起来都一样"的最大元凶——晨曦黄金光、琥珀台灯、烛火、丁达尔本质都是暖黄色调，连续出图会高度同质化。

---

## 🎲 23,400 种组合动态抽样组装公式 (Prompt Assembly Formula)

> **组合数构成**：15 摄影手法 × 12 环境空间 × 13 道具组 × 10 光影氛围 = 23,400

```
[15种摄影机位/视角 (Camera Shot & Technique)] 
+ [主体手办属性 & 真实材质 (1/7 Scale Figurine & SSS Texture)] 
+ [12大实景空间之一 (Environment Scene)] 
+ [13大叙事道具之一 (Narrative Props)] 
+ [10大光影氛围之一 (Lighting & Mood)] 
+ [专业光学器材参数与胶片质感 (Camera Gear & Macro Optics)]
```

### 🌟 示例 1：【怀旧老窗台 + 岁月怀表 + 晨曦黄金光 + 掌中凝视】
```text
A professional macro emotional documentary photograph. A 6cm miniature 3D printed full-color resin bust figurine of a beloved elderly grandfather (1/7 scale, delicate matte polymer finish, hand-painted details) is held gently in two open warm human palms. The palms are resting over a weathered rustic oak windowsill in an old peaceful courtyard house. Beside the hands on the wooden sill lies a stopped vintage brass mechanical pocket watch and a faded sepia family photo. Warm 4500K golden hour sunlight streams from the side, casting soft long shadows. Soft focus background shows a young Asian woman looking down with gentle tears and a warm smile. Shot on Canon EOS R5 with 100mm f/2.8L Macro lens, shallow depth of field, authentic 35mm Kodak Portra film grain, deeply touching.
```

### 🌟 示例 2：【现代深夜书房 + 科技温情屏幕 + 暖琥珀台灯 + 前实后虚守护】
```text
A cinematic macro photograph. In tack sharp focus in the foreground, a miniature 6cm 3D printed full-color resin figurine of an elderly grandmother stands on a dark walnut study desk directly on an illuminated smartphone displaying an old sepia photo. Beside the phone sits a steaming ceramic mug and an open notebook. Bathed in the warm 2800K amber pool of light from a vintage brass banker's lamp. In the soft creamy bokeh background, a real 25-year-old Asian woman works quietly at her laptop, glancing warmly over at the miniature figure. Shot on Sony A7R V, 85mm f/1.8 lens, shallow depth of field, quiet companion mood.
```

### 🌟 示例 3：【户外庭院青苔石阶 + 红枫落叶 + 阴雨天微凉漫射 + 极低虫眼仰拍】
```text
A dynamic low-angle bug's-eye view photograph. A miniature 6cm 3D printed full-color figurine of an elderly father stands tall on a natural mossy garden stone step outdoors, surrounded by miniature crisp red autumn maple leaves and glistening rainwater drops. Soft cool diffused overcast daylight after rain. In the distant background, a real young woman sits on a garden bench looking toward the figurine with quiet admiration. Shot on 24mm wide-angle probe lens at ground level, deep depth of field, scale-reversal composition, epic and poetic.
```

### 🌟 示例 4：【老相册内页 + 岁月泛黄照片 + 清晨冷调薄雾 + 巨物俯视】❄️ 冷调范例
```text
A dramatic ground-level low-angle bug's-eye view photograph. A miniature 6cm 3D printed full-color resin figurine of a beloved elderly grandmother stands tall directly on the open page of a worn family photo album, appearing monumental from this extreme low perspective. Surrounding her at micro scale are yellowed photographs under aging plastic film and handwritten date annotations in faded blue ink. Cool 6500K pale morning light through thin mist, low contrast desaturated palette, soft blue-gray shadows, quiet melancholic stillness. The visual metaphor of stepping out of a flat photograph into three dimensions. Shot on 24mm wide-angle probe lens at page level, deep depth of field, poetic scale-reversal composition.
```

### 🌟 示例 5：【节庆餐桌空位 + 童年记忆铁皮玩具 + 暖琥珀 + 拟真对视】🎊 年节爆点范例
```text
A forced-perspective documentary photograph. In the extreme foreground (18cm from lens), a miniature 6cm 3D printed full-color resin figurine of a beloved elderly grandfather stands at an empty seat of a warm family reunion dinner table, an untouched pair of chopsticks resting on a porcelain bowl beside him. A tin wind-up toy and glass marbles rest nearby at micro scale. In the background (2.5 meters away), a real young Asian person sits looking directly across at the figurine. Due to forced perspective and deep focus stacking (f/11), the miniature and the distant person appear equal in optical height, their eyelines meeting on the same horizontal plane. Warm 2800K tungsten dining light, softly blurred festive dishes in the background.
```

---

为帮助 Agent 做出更合理的组合（而非纯随机），以下标注每种环境空间与 6 大类摄影手法的亲和度（⭐高 / ○中 / ✗低）：

| 环境空间 | 强制透视 | 掌心互动 | 微观虫眼 | 焦点切换 | 创作者 | 光影共融 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| ① 怀旧老宅木窗台 | ⭐ | ⭐ | ○ | ⭐ | ✗ | ⭐ |
| ② 现代极简深夜书房 | ○ | ⭐ | ✗ | ⭐ | ○ | ⭐ |
| ③ 户外庭院与青苔石阶 | ⭐ | ○ | ⭐ | ⭐ | ✗ | ○ |
| ④ 匠人创作工作台 | ✗ | ○ | ○ | ○ | ⭐ | ○ |
| ⑤ 旅途与汽车中控台 | ✗ | ⭐ | ✗ | ○ | ✗ | ○ |
| ⑥ 婚礼主桌与仪式花艺台 | ○ | ⭐ | ✗ | ⭐ | ✗ | ⭐ |
| ⑦ 温馨床头与夜灯角 | ✗ | ⭐ | ✗ | ⭐ | ✗ | ⭐ |
| ⑧ 老式厨房与灶台窗边 | ○ | ⭐ | ○ | ⭐ | ✗ | ⭐ |
| ⑨ 阳台竹椅与晾晒衣物 | ⭐ | ○ | ○ | ⭐ | ✗ | ⭐ |
| ⑩ 书页与老相册内页 | ✗ | ⭐ | ⭐ | ⭐ | ○ | ○ |
| ⑪ 雨后车窗与后座 | ✗ | ⭐ | ✗ | ⭐ | ✗ | ⭐ |
| ⑫ 节庆餐桌与团圆空位 | ⭐ | ○ | ○ | ⭐ | ✗ | ○ |

> **组合规则**：优先选择 ⭐ 高亲和度组合；允许使用 ○ 中亲和度；**禁止使用 ✗ 低亲和度组合**（如"汽车中控台 + 微观虫眼仰拍"物理上不合理）。

---

## 🎯 人设身份与摆拍场景强制路由表 (Persona-Driven Staging Routing)

**严禁不看人物身份无脑使用 G1（木窗台）！** 必须根据【Step 0 提取的模型人物画像】定向选择最贴合TA一生命运与生活烟火的场景组合：

| 模型人物画像 | 核心服饰与视觉特征 | 强制推荐场景与道具 | 对应黄金组合 | 严禁场景/道具 |
| :--- | :--- | :--- | :--- | :--- |
| **A. 厨艺与家常母亲/外婆** | 戴围裙、日常布衣、慈祥微胖、笑眼弯弯 | ⑧ 老式厨房灶台 / I 烟火厨房（竹蒸笼、粗陶海碗、案板面粉、蒜臼） | **G11、G18** (晨光灶台/粗陶碗) | 严禁极简现代办公桌、严禁汽车中控台 |
| **B. 乡土、农民与朴素父辈** | 戴草帽、翻领工装、蓝棉袄、饱经风霜皱纹 | ③ 户外庭院石阶 / ⑨ 阳台竹椅 / K 农事土地（玉米棒、青石板、老式茶缸） | **G17、G3、G12** (庭院青苔/竹椅) | 严禁西式现代咖啡杯、严禁婚礼仪式台 |
| **C. 工匠、手艺人与机械工人** | 卷袖工作服、带工具腰带、坚毅神态 | ④ 匠人工作台 / H 匠心工坊 / A 岁月时光（鲁班尺、小木锉、游标卡尺、木屑） | **G6、G4** (工匠台/打磨原木) | 严禁粉色丝绸缎带、严禁毛线团 |
| **D. 知识分子、教师与医者** | 中山装、别钢笔、戴黑框老花镜、儒雅端坐 | ② 现代深夜书房 / ⑩ 老相册内页 / D 求学奋斗（英雄钢笔、算盘、泛黄讲义、旧台灯） | **G8、G13、G2** (老相册/红墨水) | 严禁厨房大铁锅、严禁农事泥土 |
| **E. 严厉又深情的长辈/倔老头** | 戴呢帽、背手站立、眼神犀利带笑、夹克 | ⑨ 阳台竹椅 / ③ 庭院石阶 / J 戏曲收音（红木象棋子、老收音机、紫砂壶） | **G12、G3、G7** (象棋残局/硬光投影) | 严禁少女感道具、严禁粉色缎带 |
| **F. 盛装、旗袍或礼服纪念** | 红旗袍、西装革履、端庄站立、盛装打扮 | ⑥ 婚礼主桌 / ⑫ 节庆餐桌空位 / F 仪式纪念（手捧花、丝绸缎带、玻璃展示罩） | **G10、G15** (婚礼主桌/手捧花) | 严禁破损工具台、严禁厨房油烟 |
| **G. 案头守护与独居治愈** | 现代常服、半身胸像、慈祥微笑 | ② 极简书房案头 / ⑦ 温馨床头 / G 科技温情（多肉绿植、手机屏幕老照片） | **G2、G5、G9** (案头陪伴/指尖触碰) | 严禁泥泞农田 |

---

## 🌟 18 大黄金组合推荐（经验证的高转化方案）

当 Agent 提取人设后，根据上述路由表匹配对应的黄金组合：

| 编号 | 摄影手法 | 环境空间 | 叙事道具 | 光影氛围 | 画幅 | 情感定位 |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| G1 | ④ 掌中凝视 | ① 怀旧木窗台 | A 岁月时光（怀表） | Ⅰ 晨曦黄金光 | 3:4 | 温暖怀念·通用窗台 |
| G2 | ⑨ 前实后虚 | ② 现代深夜书房 | G 科技温情（手机屏幕） | Ⅲ 暖琥珀台灯 | 3:4 | 孤独治愈·深夜陪伴 |
| G3 | ⑦ 巨物俯视 | ③ 户外庭院石阶 | E 自然庭院（红枫落叶） | Ⅱ 阴雨天漫射 | 3:4 | 深沉如山·父爱意象 |
| G4 | ① 拟真对视 | ① 怀旧木窗台 | A 岁月时光（泛黄照片） | Ⅳ 丁达尔光束 | 3:4 | 跨越时空·灵魂对话 |
| G5 | ⑤ 指尖传递 | ⑦ 温馨床头 | B 温情生活（老花镜） | Ⅲ 暖琥珀台灯 | 1:1 | 细腻微距·深情触碰 |
| G6 | ⑫ 涂装进行时 | ④ 匠人工作台 | H 匠心工坊（调色盘） | Ⅵ 摄影棚柔光 | 1:1 | 匠心打造·工匠传承 |
| G7 | ⑭ 丁达尔光斑 | ① 怀旧木窗台 | B 温情生活（毛线团） | Ⅳ 丁达尔光束 | 3:4 | 电影级氛围·共用光线 |
| G8 | ⑬ 打破次元壁 | ② 现代深夜书房 | D 求学奋斗（钢笔书籍） | Ⅴ 暮色蓝调 | 3:4 | 师者风范·求知岁月 |
| G9 | ⑥ 随身陪伴 | ⑤ 旅途汽车中控 | A 岁月时光（怀表） | Ⅰ 晨曦黄金光 | 3:4 | 旅途治愈·你陪我看世界 |
| G10 | ⑩ 前虚后实 | ⑥ 婚礼主桌 | F 仪式纪念（丝绸玻璃罩） | Ⅰ 晨曦黄金光 | 3:4 | 婚礼缺席·遗憾弥补 |
| G11 | ⑨ 前实后虚 | ⑧ 老式厨房灶台 | I 烟火厨房（粗陶碗蒸笼） | Ⅰ 晨曦黄金光 | 3:2 | 奶奶的饭菜香·烟火气 |
| G12 | ⑧ 阴影笼罩 | ⑨ 阳台竹椅 | J 戏曲收音（老收音机） | Ⅷ 硬光窗格投影 | 3:2 | 午后小憩·老头倔脾气 |
| G13 | ⑦ 巨物俯视 | ⑩ 老相册内页 | A 岁月时光（泛黄照片） | Ⅶ 清晨冷调薄雾 | 3:4 | 从平面走向立体·视觉隐喻 |
| G14 | ⑥ 随身陪伴 | ⑪ 雨后车窗后座 | G 科技温情（手机老照片） | Ⅹ 雨窗霓虹散射 | 3:4 | 归途思念·都市冷调治愈 |
| G15 | ① 拟真对视 | ⑫ 节庆餐桌空位 | M 童年记忆（铁皮玩具） | Ⅲ 暖琥珀台灯 | 3:2 | 团圆缺席·年节催泪爆点 |
| G16 | ⑤ 指尖传递 | ⑩ 老相册内页 | L 病榻守望（药盒日历） | Ⅶ 清晨冷调薄雾 | 1:1 | 最后的时光·克制的痛 |
| G17 | ⑪ 分焦同框 | ③ 户外庭院石阶 | K 农事土地（斗笠稻谷） | Ⅱ 阴雨天漫射 | 3:2 | 土地情结·沉默的父辈 |
| G18 | ⑭ 丁达尔光斑 | ⑧ 老式厨房灶台 | I 烟火厨房（竹蒸笼热气） | Ⅳ 丁达尔光束 | 3:4 | 晨光灶台·神圣日常 |

> **强制规则**：
> - **封面去同质化铁律**：严禁连续无脑以 G1 作为封面！若模型为厨艺长辈，封面必须使用 G18/G11；若为工匠长辈，必用 G6；若为农家父辈，必用 G17；若为倔老头，必用 G12；若为婚礼盛装，必用 G10。
> - 单次生成 3+ 张图时，必须分散在 2~3 个不同大类的生活实景中，严禁多张图全部堆在同一个房间或桌面上！

