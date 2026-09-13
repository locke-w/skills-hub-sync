# Nano Banana 2 真实拍摄光学级 Prompt 引擎 (v3.0 摄影大师升级版)

本文件是 Antigravity 直接调用 `generate_image` 工具时的**核心 Prompt 拼装规范**。
深度融合电影摄影光学（Film Optics）、微距纪录片纪实摄影（Macro Photojournalism）与《超写实人物专家》的去 AI 塑料感底层技术，**彻底根除 AI 假脸、磨皮塑料感、假手浮空与数字数码味，达到 100% 真实单反/胶片实拍效果**。

---

## 📸 真实拍摄感 5 大光学防伪铁律（Anti-AI Realism Laws）

1. ❌ **严禁使用任何 AI 空洞空泛词**：
   - 绝对禁止使用 `masterpiece, best quality, 8k, hyperrealistic, ultra detailed, perfect`（这些词会触发模型的数字艺术/插画图库，产生廉价塑料磨皮光泽）。
   - 全部替换为**纪实摄影与光学专业术语**：`unedited candid RAW photograph, 35mm film scan, documentary photojournalism, authentic photographic capture`。
2. 🔬 **注入真实物理与微观肌理（Micro-Texture & Subsurface Scattering）**：
   - **真人皮肤**：`visible skin pores, micro peach fuzz along jawline, natural skin redness, authentic skin moisture, natural laugh lines, non-uniform pigmentation`。
   - **3D 打印手办**：`miniature 6cm 3D printed UV-cured full-color photopolymer resin, delicate matte finish, micro-fine dry-brushed details, subtle 0.05mm layer texture in crevices, authentic weight depression crease on contact surface`。
3. 🎯 **真机光学与镜头物理学（Real Optical Aberrations）**：
   - 指定定焦专业人像与微距镜头（如 `Canon RF 100mm f/2.8L Macro`, `Sony FE 85mm f/1.4 GM`, `Leica Summilux-M 50mm f/1.4`）。
   - 模拟真实光学瑕疵：`natural optical depth of field falloff, subtle chromatic aberration at contrast edges, gentle natural corner vignetting, authentic Kodak Portra 400 film grain`。
4. 💡 **自然光线与环境漫反射（Physics-Based Ambient Lighting）**：
   - 真实环境光子反弹：`warm bounce light from wooden desk onto figurine base, soft natural ambient occlusion in crevices and hand contact points`。
5. ✂️ **构图减法防崩铁律（Compositional Subtraction）**：
   - 涉及手持微距时强制**“无脸构图/颈部截断”**，背景深度虚化，算力 100% 集中于正确的手部解剖（5 fingers, natural grip）与手办质感；
   - 涉及人脸同框时手办置于桌面，严禁“双手举到脸前”这类 AI 易崩溃动作。

---

## 一、 真实摄影级 Prompt 模块化组装公式

每个最终 Prompt 由以下 6 个模块按顺序严密拼接：

```
[A. 摄影手法骨架（15选1）]
+ [B. 物理手办与真实微缩材质（固定模块）]
+ [C. 环境空间（7选1 → 替换 {ENVIRONMENT}）]
+ [D. 叙事道具（8选1 → 替换 {PROPS}）]
+ [E. 光影与漫反射（6选1 → 替换 {LIGHTING}）]
+ [F. 真实摄影器材与胶片光学（固定模块）]
+ [G. 去AI味真实微瑕（抽选注入）]
```

### B. 主体手办材质固定模块（所有 Prompt 必带）
```text
a miniature 6cm 3D printed full-color UV-cured photopolymer resin bust figurine, 1/7 scale collectible figure, delicate matte polymer finish, hand-painted micro-details, subtle resin translucency with subsurface scattering, real contact shadow and physical weight impression on surface
```

### F. 光学器材与胶片质感固定模块（所有 Prompt 必带）
```text
an unedited candid RAW documentary photograph, shot on Canon EOS R5 with RF 100mm f/2.8L Macro lens at f/2.8, authentic 35mm Kodak Portra 400 film grain, subtle natural lens chromatic aberration, natural uncompressed color science
```

---

## 二、 画幅比例与摄影手法映射表

| 编号 | 手法名称 | 大类 | 推荐 AspectRatio | 构图说明 |
| :--- | :--- | :--- | :--- | :--- |
| ① | 拟真对视 Eye-level Duel | 强制透视 | `3:4` | 纵深透视竖构图突出前后关系 |
| ② | 并肩作战 Side-by-Side | 强制透视 | `3:2` | 横向并排宽幅 |
| ③ | 虚实托举 Phantom Lift | 强制透视 | `3:4` | 竖构图表现上下托举 |
| ④ | 掌中凝视 Gulliver's Palm | 掌心互动 | `3:4` | 竖构图突出掌心微距与手办质感（无脸构图） |
| ⑤ | 指尖传递 Fingertip Touch | 掌心互动 | `1:1` | 方形超微距聚焦指尖触碰点 |
| ⑥ | 随身陪伴 Pocket Companion | 掌心互动 | `3:4` | 竖构图展示胸前口袋与衣物微纹理 |
| ⑦ | 巨物俯视 Giant's Gaze | 微观虫眼 | `3:4` | 极低角度仰拍，微缩转巨物 |
| ⑧ | 阴影笼罩 Shadow Canopy | 微观虫眼 | `3:2` | 横构图展示斜长物理投影 |
| ⑨ | 前实后虚 Sharp Fore | 焦点切换 | `3:4` | 竖构图微距前景手办，背景柔美虚化 |
| ⑩ | 前虚后实 Soft Fore | 焦点切换 | `3:4` | 竖构图前景虚化手办，背景人物清晰 |
| ⑪ | 分焦同框 Split Focus | 焦点切换 | `3:2` | 移轴横构图双焦点清晰 |
| ⑫ | 涂装进行时 Painting WIP | 创作者 | `1:1` | 方形俯拍工坊手作 |
| ⑬ | 打破次元壁 4th Wall | 创作者 | `3:4` | 桌面手办前景，人物背景探头对视 |
| ⑭ | 丁达尔光斑 Tyndall | 光影共融 | `3:4` | 竖构图展示窗格丁达尔自然光束 |
| ⑮ | 手机屏幕投影 Phone Glow | 光影共融 | `3:4` | 竖构图展示弱光下手机屏幕物理上光 |

---

## 三、 15 种摄影手法光学级骨架模板

> **使用方法**：选定手法后，将 `{ENVIRONMENT}` / `{PROPS}` / `{LIGHTING}` 替换为从 `github-diorama-staging-matrix.md` 中抽选的对应英文 Prompt 片段，`{SUBJECT}` 替换为包含具体长辈特征的描述（如 `beloved elderly grandmother wearing floral jacket`）。

### ① 拟真对视 (Eye-level Duel) — 强制透视类
```text
A forced-perspective documentary photograph. In the extreme foreground (18cm from lens), {SUBJECT} stands on {ENVIRONMENT}. {PROPS}. In the background (2.5 meters away), a real young Asian person stands looking directly across at the figurine. Due to forced perspective and deep focus stacking (f/11), the miniature figurine and the distant person appear equal in optical height and their eyelines meet on the same horizontal plane in deep emotional conversation. Natural ambient light bounce, {LIGHTING}.
```

### ② 并肩作战 (Side-by-Side March) — 强制透视类
```text
A candid forced-perspective photograph showing {SUBJECT} placed on a weathered low wall ledge in the foreground, positioned side-by-side with a real young Asian person walking in the background at matching optical scale. {ENVIRONMENT}. {PROPS} scattered nearby. The two figures appear to be walking together as companions, deep focus f/11, authentic natural outdoor lighting, {LIGHTING}.
```

### ③ 虚实托举 (Phantom Lift) — 强制透视类
```text
A precise forced-perspective photograph where a real young Asian person in the background extends their open palm beneath {SUBJECT} in the extreme foreground, creating the optical illusion of gently supporting the figurine from below. {ENVIRONMENT}. {PROPS}. Natural daylight, sharp optical focus on both subjects, {LIGHTING}.
```

### ④ 掌中凝视 (Gulliver's Palm) — 掌心互动类 (无脸构图防崩)
> ⚠️ 本骨架**刻意不含 `{PROPS}`**，执行构图减法：算力集中于手部解剖与手办质感。抽到的道具组本次弃用，不要强行塞入。
```text
A professional macro documentary photograph of {SUBJECT} held gently in two open warm human palms. The real human hands have perfectly formed anatomy, exactly 5 fingers per hand, natural relaxed grip, authentic skin pores, fingerprint ridges, and subtle palm creases under the figurine's physical weight. The human face is completely out of frame (cropped below neck). {ENVIRONMENT}. Heavily blurred creamy bokeh background isolating the hands and the miniature. Warm natural subsurface scattering glowing through the fingertips, {LIGHTING}.
```

### ⑤ 指尖传递 (Fingertip Touch) — 掌心互动类 (极致微距)
```text
An extreme macro documentary photograph capturing a tender moment of connection: a real human adult index finger gently touching the tiny miniature hand of {SUBJECT}. Tack sharp focus precisely on the physical contact point, showing authentic human skin micro-pores, fingerprint ridges, warm subsurface scattering, and the delicate matte hand-painted acrylic finish of the resin figurine. {ENVIRONMENT}. Soft natural side lighting, creamy bokeh, {LIGHTING}.
```

### ⑥ 随身陪伴 (Pocket Companion) — 掌心互动类
```text
A candid lifestyle documentary photograph of a real young Asian person, with {SUBJECT} peeking out from their jacket breast pocket. The figurine is a tiny cherished travel companion. Authentic fabric weave texture on jacket, {ENVIRONMENT}. {PROPS}. Candid slice-of-life photography, natural daylight, {LIGHTING}.
```

### ⑦ 巨物俯视 (Giant's Gaze Down) — 微观虫眼类
```text
A dramatic ground-level low-angle bug's-eye view photograph. {SUBJECT} stands tall on {ENVIRONMENT}, appearing monumental and towering from this extreme low perspective. {PROPS} scattered at the base of the figurine at micro scale. In the far background, a real young Asian person is visible at normal scale, creating a poetic scale-reversal composition. Natural overcast lighting, {LIGHTING}.
```

### ⑧ 阴影笼罩 (Shadow Canopy) — 微观虫眼类
```text
A dramatic chiaroscuro documentary photograph from a low side angle. {SUBJECT} stands on {ENVIRONMENT}. The figurine casts a long, sharp physical shadow across the surface that stretches toward the camera. {PROPS} partially falling into the shadow path. Authentic directional window sidelight creating natural physical contrast, {LIGHTING}.
```

### ⑨ 前实后虚 (Sharp Foreground, Soft Background) — 焦点切换类
```text
A professional macro still-life photograph. In tack sharp focus in the foreground, {SUBJECT} stands on {ENVIRONMENT}. {PROPS} arranged around the figurine base with realistic contact shadows. In the soft, creamy bokeh background, a real young Asian person is sitting quietly, slightly out of focus but emotionally present. Shallow depth of field, 85mm f/1.8 lens, natural warm bounce light, {LIGHTING}.
```

### ⑩ 前虚后实 (Soft Foreground, Sharp Background) — 焦点切换类
```text
A cinematic rack-focus photograph. {SUBJECT} stands in the extreme foreground, intentionally soft and slightly out of focus, creating an ethereal memory silhouette. In the tack sharp background, a real young Asian person sits at {ENVIRONMENT}, {PROPS} on the table, their face in crisp emotional focus showing visible skin pores and gentle tears of nostalgia. Natural soft room light, {LIGHTING}.
```

### ⑪ 分焦同框 (Split Focus Diptych) — 焦点切换类
```text
A split-focus photograph with dual sharp zones using tilt-shift optics. On the left third of the frame, {SUBJECT} is in tack sharp macro focus on {ENVIRONMENT}. On the right side, a real young Asian person is also in crisp focus. {PROPS} bridge the space between them. Authentic optical depth, natural directional lighting, {LIGHTING}.
```

### ⑫ 涂装进行时 (Painting In Progress) — 创作者类
```text
A top-down flat-lay photograph of an artisan miniature workspace. {SUBJECT} rests on a green self-healing cutting mat with visible surface wear, surrounded by fine 000 detail brushes, tiny open acrylic paint bottles with colorful paint residue, precision tweezers, and {PROPS}. A real human hand holds a micro-detail brush gently near the figurine's collar. Real studio work light, authentic workshop reality, {LIGHTING}.
```

### ⑬ 打破次元壁 (Breaking the Fourth Wall) — 创作者类 (安全景深构图)
```text
A meta-narrative documentary photograph. {SUBJECT} stands firmly on {ENVIRONMENT} in tack sharp foreground with natural contact shadow. In the soft bokeh background, a real young Asian person leans forward on the desk, resting their chin on their crossed arms, gazing into the eyes of the figurine with deep emotional connection and a gentle smile through tears. Hands are naturally resting on desk. Warm natural lamplight, {LIGHTING}.
```

### ⑭ 丁达尔光斑 (Shared Tyndall Light Path) — 光影共融类
> ⚠️ 本手法骨架自带强光影设定，`{LIGHTING}` 只能填入与丁达尔光束一致的配方（推荐 Ⅳ 神圣丁达尔光束），禁止叠加冲突光型（如 Ⅵ 摄影棚柔光）。
```text
An artistic chiaroscuro photograph. A single dramatic ray of warm golden sunlight cuts through wooden window blinds across a quiet room, simultaneously illuminating {SUBJECT} on {ENVIRONMENT} and the side profile of a real young Asian person sitting quietly in the background. {PROPS} resting nearby, partially catching the light beam. Visible airborne dust particles dancing in the light beam, deep natural ambient shadows surrounding the beam path, {LIGHTING}. Shot on 50mm f/1.4 prime lens.
```

### ⑮ 手机屏幕投影 (Phone Screen Glow Projection) — 光影共融类
> ⚠️ 本手法为弱光夜景，`{LIGHTING}` 只能填入弱光相容配方（推荐 Ⅲ 暖琥珀台灯 / Ⅴ 暮色蓝调），禁止填入日光类（Ⅰ 晨曦黄金 / Ⅱ 阴雨漫射 / Ⅳ 丁达尔 / Ⅵ 摄影棚柔光）。Negative 必须追加 Layer 4。
```text
A moody low-light night photograph. {SUBJECT} stands directly on an illuminated smartphone screen that is displaying an old scanned sepia family photograph. The smartphone screen's soft glow acts as a natural physical uplight illuminating the resin figurine's facial contours from below, creating an authentic luminous bridge between digital memory and physical tribute. {ENVIRONMENT}. {PROPS}. Subtle ambient fill light, {LIGHTING}.
```

---

## 四、 顶级 4 层分层 Negative Prompt 体系（去 AI 塑料感护城河）

```text
# Layer 1: 通用去 AI / 去塑料 / 去数字渲染基底 (所有图必带)
plastic skin, rubber skin, 3d render, CGI, digital illustration, anime, cartoon, airbrushed, oversmoothed face, porcelain doll, fake eyes, beauty filter, fake skin texture, excessive HDR, oversaturated colors, artificial glossy sheen, videogame screenshot, unreal engine, octane render, raytracing glare, watermark, text overlay, logo, frame, border

# Layer 2: 人体与手部解剖学防崩 (含真人/手的画面追加)
extra fingers, missing fingers, fused fingers, distorted hands, malformed fingers, 6 fingers, 4 fingers, mutated hands, bad anatomy, disfigured hands, detached limbs, floating objects, wax museum mannequin, creepy smile, uncanny valley

# Layer 3: 静物与物理重力防崩 (纯手办/微距画面追加)
floating figurine, missing contact shadow, tilted base, blurry subject, plastic mold flash, sterile studio render, flat lighting, fake bokeh

# Layer 4: 恶劣光影与数码噪点抑制 (特殊光影追加)
harsh direct flash, blown out highlights, muddy crushed shadows, neon rainbow lights, color banding, digital compression artifacts
```

**拼装执行规则**：

| 画面类型 | Layer 1 基底 | Layer 2 人体 | Layer 3 静物 | Layer 4 光影 |
| :--- | :---: | :---: | :---: | :---: |
| 含真人手/脸/身体（手法①②③④⑤⑥⑦⑨⑩⑪⑫⑬⑭） | ✅ | ✅ | — | 见下 |
| 纯手办静物无真人（手法⑧⑮ 或指定无人画面） | ✅ | — | ✅ | 见下 |

**Layer 4 追加条件**（满足任一即追加）：
- 手法为 ⑭ 丁达尔光斑 / ⑮ 手机屏幕投影；
- 光影配方为 Ⅲ 暖琥珀台灯 / Ⅳ 丁达尔光束 / Ⅴ 暮色蓝调（弱光或强反差）；
- 画面含屏幕、烛光、逆光等易过曝/断层光源。

> **工具兼容**：若 `generate_image` 无独立 negative 参数，将拼装结果转为自然语句追加至 Prompt 末尾，格式：
> `avoid: plastic skin, 3d render, extra fingers, floating figurine, blown out highlights, ...`

---

## 五、 去 AI 味真实微瑕注入库（Micro-Imperfection Injection）

根据画面类型，从以下词库中**抽选 3-5 个**注入 Prompt 正文末尾，彻底欺骗模型打破对称与磨皮算法：

### 👤 真实人体皮肤微瑕
```text
visible micro skin pores, subtle fine laugh lines, tiny natural freckles across nose bridge, realistic skin redness on earlobes and fingertips, individual stray hairs, natural lip ridges with slight dryness, subtle skin moisture sheen on forehead
```

### 👴 真实老年长辈生理特征（若主角为长辈）
```text
weathered skin with deep authentic crow's feet and forehead wrinkles, natural age spots, gentle sagging skin around jawline, silver-gray hair strands with realistic coarse texture, gentle wise wrinkles around eyes
```

### 🗿 3D 打印手办物理材质微瑕
```text
delicate matte UV resin finish, microscopic 0.05mm layer lines faintly visible under macro light, subtle hand-painted dry brush stroke variations, micro dust speckle on acrylic display base, authentic resin weight impression on surface
```

### 🏡 真实环境与生活微瑕
```text
natural dust motes in sunbeam, subtle ring mark on weathered wood desk, slightly dog-eared notebook page, soft ambient light bounce from wooden tabletop, natural imperfect fabric weave
```
