# 超写实人物提示词全能参考库 (Photorealistic Prompt Library)

本文档为 `photorealistic-character` Skill 的配套高级提示词工程字典，涵盖两类生成模式的参数库、皮肤微观修饰词、相机光学库与影视光影库。

---

## 1. 皮肤与生理微观质感字典 (Micro-Texture & Bio-Optical Tokens)

| 类别 | 推荐 Prompt 英文术语 | 中文释义 / 作用 |
| :--- | :--- | :--- |
| **毛孔与肌理** | `visible skin micro-pores, authentic skin grain, fine micro-texture` | 生成真实毛孔、告别磨皮塑料感 |
| **细小绒毛** | `fine vellus hair, subtle peach fuzz on cheeks and jawline` | 特写镜头杀手锏，极强提升真实度 |
| **皮肤通透性** | `subsurface scattering (SSS), translucent skin undertones` | 模拟真实皮下脂肪与毛细血管透光感 |
| **真实瑕疵** | `subtle micro-imperfections, natural freckles, fine wrinkles, slight uneven skin tone` | 打破 AI 生成的绝对平滑与对称 |
| **眼睛与眼神** | `intricate iris pattern, distinct catchlights in pupils, moist sclera with fine veins` | 赋予眼神灵魂与湿润高光，告别死鱼眼 |
| **唇部质感** | `natural lip texture with fine vertical creases, subtle natural moisture sheen` | 呈现真实唇纹与自然反光 |
| **发丝边缘** | `individual hair strands, fine stray flyaway hairs, realistic organic hairline` | 拒绝“头盔假发”与色块边缘 |

---

## 2. 摄影器材与镜头光学字典 (Optical & Camera Presets)

| 风格/场景 | 相机机身 (Camera Body) | 镜头与光圈 (Lens & Aperture) | 光学特性描述 (Optical Characteristics) |
| :--- | :--- | :--- | :--- |
| **证件照/标准正面肖像** | `Sony Alpha A7R V` | `85mm f/1.8 prime lens` | `ultra-sharp eye focus, minimal facial distortion, true-to-life perspective` |
| **电影大片特写** | `ARRI Alexa Mini LF` | `Cooke Anamorphic 50mm f/1.4` | `subtle anamorphic lens flare, creamy bokeh, cinematic film grain, 35mm film aesthetic` |
| **高端时尚商业杂志** | `Hasselblad H6D-100c` | `105mm Macro f/2.8 lens` | `medium format depth, extreme textural resolving power, hyper-accurate color fidelity` |
| **纪实人文/街头抓拍** | `Leica M11-P` | `35mm Summilux f/1.4 lens` | `organic street documentary feel, authentic natural ambient contrast, unposed candid feel` |

---

## 3. 专业影视布光字典 (Cinematic Lighting Presets)

- **柔和漫射窗光 (Soft Diffused Natural Light)**：`soft natural diffused window light, gentle shadow falloff, realistic ambient occlusion`（最适合素颜清纯/日常真实场景）。
- **伦勃朗光 (Rembrandt Lighting)**：`classic Rembrandt lighting, triangle light on the shadow cheek, dramatic yet natural depth`（最适合商战剧、成熟男性、有故事感的角色）。
- **蝴蝶光/商业美人光 (Butterfly/Paramount Lighting)**：`butterfly beauty lighting directly from above-front, subtle shadow under the nose, flattering high-contrast cheekbones`（最适合时尚广告、女明星/博主妆造）。
- **黄昏轮廓逆光 (Golden Hour Rim Lighting)**：`golden hour warm backlight, glowing rim light tracing hair strands and facial silhouette, volumetric light rays`（最适合唯美短剧、情绪特写）。

---

## 4. 模式一：截图还原·正面重构实战 Prompt 模板

### 场景 1.1：短剧截图/影视男神角色还原
```markdown
**Prompt:**
A hyper-realistic 8k raw passport-grade frontal portrait of an Asian male in his late 20s, exactly matching the facial features, eye shape, nose bridge, jawline angle, and ear structure of the reference subject. Facing straight forward directly into the lens, neutral relaxed expression, mouth closed. Realistic skin texture with visible micro-pores, fine stubble, natural skin unevenness, authentic subsurface scattering, unretouched raw photo. Sharp catchlights in the pupils. Shot on 85mm f/1.4 lens, Sony A7R V, clean neutral studio background, balanced soft studio portrait lighting, 8k resolution, photorealistic masterpiece.
```

### 场景 1.2：短剧截图/影视女主角色还原
```markdown
**Prompt:**
A hyper-realistic 8k raw studio frontal portrait of a young East Asian female, precisely preserving the eye geometry, eyelid fold, nose tip contour, lip thickness, and facial bone structure of the reference image. Positioned at eye level looking straight into the camera, gentle natural neutral expression. Intricate bare-skin details with visible pores, delicate peach fuzz, subtle natural blush undertones, realistic lip creases, moist sclera. Shot on 85mm f/1.8 portrait lens, Hasselblad H6D, soft diffused beauty-dish lighting with gentle rim light, 8k UHD, candid photographic perfection.
```

---

## 5. 模式二：文生全新超写实角色配方库 (Multi-Role Recipe Bank)

### 场景 2.1：高管/商战霸总 (35岁亚裔男性)
```markdown
**Prompt:**
A raw photorealistic 8k cinematic portrait of a 35-year-old East Asian male corporate executive. Sharp defined jawline, intelligent focused gaze, well-groomed side-parted black hair with subtle matte texture. Realistic masculine skin texture with visible micro-pores, light faint shadow of a 5 o'clock beard stubble, subtle laugh lines near the eyes. Wearing a tailored charcoal bespoke wool blazer and crisp open-collar dress shirt. Shot on ARRI Alexa Mini, 85mm f/1.8 lens, Rembrandt office lighting with soft city skyline bokeh in the background, cinematic color grading, unretouched raw photo.
```

### 场景 2.2：职场独立女性/律师 (30岁都市女性)
```markdown
**Prompt:**
A hyper-realistic close-up portrait of a 30-year-old East Asian female attorney. Shoulder-length straight dark brown hair with subtle volume, elegant light makeup, natural double eyelid fold, confident direct eye contact. Authentic skin texture with fine visible pores, natural skin sheen on high points, delicate lip creases, no heavy foundation filter. Wearing a tailored navy suit jacket. Shot on Sony A7R V, 85mm f/1.8 lens, soft diffused indoor studio lighting, creamy shallow depth of field, 8k resolution, authentic raw photography.
```

### 场景 2.3：古风/仙侠短剧超写实男主 (24岁古风青年)
```markdown
**Prompt:**
A hyper-realistic cinematic portrait of a 24-year-old East Asian young man in ancient Chinese Hanfu robes. Long lustrous black hair half-tied with authentic individual flyaway hair strands catching the wind. Distinct aristocratic bone structure, phoenix-shaped expressive eyes with realistic depth and specular reflections, natural skin texture with subtle vellus hair and micro-pores. Soft moonlight and warm lantern rim light, volumetric fog, shot on ARRI Alexa LF, 85mm f/1.4 lens, 8k, raw film aesthetic.
```
