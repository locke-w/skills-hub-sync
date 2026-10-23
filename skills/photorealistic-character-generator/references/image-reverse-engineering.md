# 参考图逆向解构与高保真定妆照重构协议

本协议用于将用户上传的人物截图、剧照、生活照或手绘稿，**逆向解构出高精度的物理与五官特征向量**，并重构成一张具备电影级工业标准的**正面高清定妆照（Casting Portrait）**。

---

## 1. 逆向解构 5 步流程

```
[用户上传截图]
      │
      ▼
1. 提取骨相特征 (Face Geometry & Skeleton)
   - 脸型（瓜子/方圆/心形）、下颌骨折角、颧骨开合度、眉骨突出度
      │
      ▼
2. 提取五官核心形态 (Facial Features)
   - 眼型（双眼皮折痕、内眦、眼角走向、瞳孔大小与颜色）
   - 鼻型（山根高度、鼻尖形态、鼻翼宽度）
   - 唇型（上唇M峰、下唇饱满度、嘴角微表情）
      │
      ▼
3. 提取皮相与生物学特征 (Biometric & Skin Details)
   - 年龄段、肤质（干性/油性/日晒粗粝/细腻冷白）
   - 唯一性识别锚点：特征痣、微小色斑、唇纹、法令纹深浅、胡茬形态
      │
      ▼
4. 提取发型与造型结构 (Hair & Styling)
   - 发色、发长、发质纹理（直发/自然微卷/蓬松发丝）、刘海弧度
      │
      ▼
5. 重构为标准化影视定妆提示词 (Prompt Synthesis)
   - 修正原图不良光影与角度，输出中性灰底、85mm镜头、正视镜头的标准化写实 Prompt
```

---

## 2. 逆向解析示例（结合典型人物样本）

### 案例 1：劳动者/中老年男性截图逆向
- **输入特征**：50岁左右东亚男性，短发微卷带灰白，眼窝微陷，深法令纹，日晒黑黄皮，橙色工装。
- **解构锚点**：
  - 骨相：方圆脸，微宽下颌，平眉骨
  - 五官：单眼皮带下垂眼角，鼻头圆润，唇色偏深且干燥
  - 皮相：粗糙肌理、粗大毛孔、额头深抬头纹、眼角放射状鱼尾纹、青色胡茬痕迹
- **重构输出 Prompt**：
  ```text
  A hyper-realistic RAW casting headshot of a 50-year-old East Asian male worker, weather-aged facial skin with deep forehead furrows and defined crow's feet, authentic sun-tanned complexion with visible skin pores and natural imperfections, slightly sunken brown eyes with realistic glistening catchlights, natural dry lip texture, short unruly salt-and-pepper hair. Wearing a worn orange utility zip-up collar. Neutral grey studio background, soft 45-degree directional portrait lighting, shot on Hasselblad H6D-100c, 85mm f/2.2 lens, uncompressed 8k photo, authentic film grain, no digital smoothing. --ar 9:16 --style raw --s 70
  ```

### 案例 2：年轻女性特写截图逆向
- **输入特征**：20出头年轻混血/欧美女性，深棕色大波浪卷发带齐刘海，大耳环，微翘丰唇。
- **解构锚点**：
  - 骨相：椭圆脸，清晰下颌线，饱满面颊
  - 五官：杏眼、微扬睫毛、挺直小翘鼻、丰满双唇且微露唇缝
  - 皮相：自然小麦色/暖白皮，鼻梁微小浅雀斑，柔和次表面光泽
- **重构输出 Prompt**：
  ```text
  A cinematic raw studio portrait of a 22-year-old brunette woman with layered wavy dark brown hair and wispy fringe bangs, silver hoop earrings, subtle natural freckles across nose bridge, soft velvety skin texture with visible micro-pores and realistic subsurface scattering, expressive hazel-brown eyes gazing into the lens, natural plump lips with authentic fine creases. Soft ambient room daylight, subtle rim lighting on hair texture, shot on 35mm portrait lens, f/1.8, neutral tones, photorealistic film look, unedited authenticity. --ar 9:16 --style raw --s 65
  ```

---

## 3. 定妆照标准化要求（为什么必须输出正面照？）

1. **用于 AI 视频作为角色锁（Identity Lock）**：可灵（Kling）、海螺（Minimax）、Runway 等视频模型需要最清晰、无遮挡的面部五官作为第一帧。
2. **用于 LoRA 或 FaceID 训练**：高质量无死角的正面人像能够提供最准的骨相关键点（Landmarks），防止在后续不同运镜下发生脸崩。
3. **消除原图畸变**：手机自拍广角导致的“大鼻子、脸型拉长”在逆向时会被强制校正为 85mm 黄金人像透视。
