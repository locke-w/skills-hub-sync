# 万能超写实人物提示词公式与词汇库

本参考文档提供工业级写实人物提示词组件库。所有提示词均采用中英文对照，适用于 **Midjourney (v6.1+)、Flux.1、SDXL、Stable Diffusion、DALL-E 3**。

---

## 1. 核心组装公式（8 层架构）

```
[1. 景别与构图] + [2. 年龄与身份/气质] + [3. 五官骨相与非对称特征] + [4. 皮肤微观肌理与次表面] + [5. 发型发色与碎发] + [6. 服装材质与细节] + [7. 摄影机位/镜头/胶片参数] + [8. 光影环境与背景]
```

---

## 2. 核心词汇分类字典

### (1) 皮肤真实肌理（去塑料感关键）
* `natural skin texture, visible pores`：真实皮肤纹理，清晰可见的毛孔
* `subtle skin imperfections, authentic blemishes`：细微的皮肤瑕疵，真实斑点
* `subsurface scattering, realistic skin translucency`：次表面散射（皮肤透光感，防止假面）
* `subtle fine wrinkles around eyes, natural laugh lines`：眼角细纹，自然笑纹/法令纹
* `micro peach fuzz, fine vellus hair along jawline`：面部微小绒毛（下颌微小绒毛）
* `natural skin moisture, subtle sheen on forehead and nose`：自然皮肤水分感，T区轻微真实油光
* `uneven skin tone, realistic pigmentation`：自然不均匀肤色，真实色素沉淀
* `subtle freckles scattered across cheeks`：脸颊散落的浅雀斑
* `fine stubble, 5 o'clock shadow`：微小胡茬，男性须青痕迹

### (2) 五官与神态（骨相与非对称感）
* `symmetrical yet naturally imperfect facial structure`：自然微不对称的对称骨相
* `deep-set expressive eyes, realistic catchlight`：深邃富有神采的眼睛，逼真眼神光
* `individual eyelash strands, natural eyebrow feathering`：根根分明的睫毛与眉毛毛流感
* `moist lips with natural lip lines and vertical ridges`：湿润自然的双唇，清晰唇纹
* `relaxed neutral expression, casting headshot gaze`：放松的自然中性表情，定妆照注视感

### (3) 摄影设备与光学参数
* `shot on Hasselblad H6D-100c` / `shot on Sony A7R V`：哈苏大画幅 / 索尼微单
* `85mm f/1.4 GM portrait prime lens`：85mm 人像定焦镜头（消除透视变形）
* `shallow depth of field, creamy background bokeh`：浅景深，奶油般背景虚化
* `captured on 35mm Kodak Portra 400 film`：柯达 35mm 胶片感
* `authentic subtle film grain, RAW uncompressed photography`：真实胶片颗粒，RAW 无损摄影
* `neutral color grading, no heavy filters`：中性色调调色，无浓重滤镜

### (4) 电影级光影与布光
* `Rembrandt studio portrait lighting`：伦勃朗光（经典的三角高光与面部立体感）
* `soft diffused northern daylight from window`：柔和北向窗户漫射自然光
* `subtle warm rim light highlighting hair contours`：发丝微暖边缘轮廓光
* `realistic soft directional key light, fill light`：主光与辅助光的自然过渡

---

## 3. 全套工业级 Prompt 模板

### 模板 A：东亚写实男性（中中年/短剧主角/粗粝生活质感）
```text
A RAW casting portrait headshot of a 43-year-old Chinese construction worker, weather-beaten face with natural wrinkles and crow's feet, authentic tanned skin with visible pores, coarse skin texture, 5 o'clock stubble shadow on jawline, dark brown eyes with realistic catchlight, unruly short black hair with subtle gray strands, wearing a dusty orange work jacket over a gray collar. Shot on Hasselblad H6D-100c, 85mm portrait prime lens, f/2.0 aperture, soft directional overcast daylight, muted urban street background softly blurred, 35mm film stock, authentic fine grain, neutral color palette, unedited photographic reality. --ar 9:16 --style raw --s 75 --v 6.1
```

### 模板 B：年轻现代女性（自然通透/微瑕素颜感/短剧女主）
```text
A close-up cinematic portrait of a 24-year-old East Asian woman with a clean natural bob haircut with wispy bangs, soft porcelain skin with visible micro-pores and delicate freckles across the nose bridge, subtle subsurface scattering, realistic lip texture with faint natural vertical lines, deep brown doe eyes looking straight at camera, individual eyebrow strands. Wearing a simple beige high-neck ribbed knit top. Studio neutral grey backdrop, soft diffused octabox key light, subtle rim light separating hair from background, shot on Sony A7R V, 105mm f/1.8 lens, 8k resolution, authentic raw color capture, no beauty filters. --ar 9:16 --style raw --s 65 --v 6.1
```

### 模板 C：欧美成熟男性（职场/商战/悬疑短剧）
```text
A professional cinematic headshot of a 38-year-old Caucasian male entrepreneur, sharp defined jawline, light stubble beard, dark brown wavy hair casually styled, piercing hazel-brown eyes, natural subtle laugh lines, authentic skin micro-details with realistic light reflection on cheeks. Wearing a fitted charcoal black crewneck t-shirt. Neutral off-white studio wall background, Rembrandt lighting setup, soft fall-off shadows, shot on Leica SL2 with Summilux-M 90mm f/1.5, authentic 35mm Portra 400 film grain, hyper-realistic, documentary photography aesthetic. --ar 9:16 --style raw --s 80 --v 6.1
```

---

## 4. 负向提示词专用组（Negative Prompts / Negative Tokens）

在 Stable Diffusion、Flux LoRA 或 WebUI 中使用：
```text
plastic skin, rubber skin, 3d render, cgi, airbrushed, oversmoothed, porcelain doll, anime, illustration, painting, drawing, cartoon, fake eyes, symmetrical uncanny face, heavy makeup, excessive beauty filter, blurry, low resolution, deformed pupils, extra fingers, mutated anatomy.
```
