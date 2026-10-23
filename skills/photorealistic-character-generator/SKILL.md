---
name: photorealistic-character-generator
description: Use when generating hyper-realistic human character portraits for AI short dramas, films, commercials, or virtual influencers, especially when resolving AI facial distortion, plastic skin, or face collapse across image-to-portrait restoration or text-to-character creation.
license: MIT
metadata:
  version: "1.0.0"
  domain: generative-ai-visuals
  triggers: 超写实人物, 真实人脸, AI短剧人物, 防崩脸, 人物定妆照, 还原长相, 生成真实人物, 写实肖像, photorealistic face, character consistency, portrait prompt, casting photo
  role: hyper-realistic-visual-director
  scope: character-design-and-prompt-engineering
  output-format: structured-prompts-and-workflows
  related-skills: idea-refine, doc-coauthoring
---

# Photorealistic Character Generator (超写实人物专家)

致力于解决 AI 短剧、影视广告与虚拟人创作中**“人物假、易崩脸、五官失真、塑料感严重”**的核心痛点，建立电影级工业化“数字演员定妆与资产锚定”标准。

---

## 核心设计哲学（去塑料化与骨相还原）

AI 假脸的核心在于**“过度磨皮（Airbrushed）”**与**“绝对对称（Uncanny Valley）”**。真实质感依赖三大支柱：
1. **微观肌理与次表面散射（Subsurface Scattering）**：真实的毛孔（Pores）、微小绒毛（Vellus Hair）、局部泛红（Subtle Erythema）、自然的皮肤油光与水分感。
2. **非对称性与生理细节（Natural Asymmetry）**：轻微的不对称五官、法令纹、浅细纹、晒斑或特征痣，打破 AI “网红脸模版”。
3. **真实光学与电影摄影（Real Optics & Lighting）**：定焦人像镜头（85mm/105mm）、大光圈光学虚化（f/1.8-f/2.8）、伦勃朗/侧逆光摄影级布光。

---

## 两大生成模式工作流

```
                             ┌───────────────────────────────┐
                             │  Photorealistic Character     │
                             └──────────────┬────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
     【模式一：参考图高保真还原】                      【模式二：文本全新角色创造】
     - 5 维面部特征逆向解构                         - 角色小传与人口统计学定位
     - 提取唯一面部锚点（骨相/胎记/眼型）           - 真实肌理与非对称特征注入
     - 输出标准正面定妆照 (Casting Shot)            - 摄影级机位与光影渲染配方
                    │                                               │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                       ┌─────────────────────────────────────────┐
                       │ 跨平台提示词生成 (Midjourney/Flux/SD)   │
                       │ + 视频一致性防崩管线 (Kling/Minimax/...)│
                       └─────────────────────────────────────────┘
```

---

## 模式一：上传截图/人物参考图高保真还原

当用户提供人物截图或照片时，执行 **5 维特征逆向解构协议**：

1. **骨相与轮廓（Bone Structure）**：面部三庭五眼比例、下颌角角度（Sharp/Soft jawline）、颧骨高低（Prominent cheekbones）、下巴形态（Square/Round/Pointed chin）。
2. **眼眉精细特征（Eyes & Brows）**：眼型（杏眼/单眼皮/深邃欧式/内双）、瞳孔色彩及纹理、眼距、眼袋/卧蚕、眉毛毛流感与弧度。
3. **鼻唇微观结构（Nose & Lips）**：鼻梁弧度（Straight/Aquiline）、鼻翼宽窄、人中深浅、唇形厚薄与唇纹走向。
4. **皮相与辨识锚点（Skin Texture & Unique Anchors）**：年龄沉淀痕迹（法令纹/鱼尾纹）、皮肤色温（Warm/Olive/Cool undertone）、唯一特征（特定位置的痣、雀斑、胡茬形态）。
5. **发型与环境状态（Hair & Styling）**：发质（粗硬/细软/卷曲）、碎发自然散落感（Flyaway strands）、着装材质。

> 详细逆向还原模板与实操步骤见 `references/image-reverse-engineering.md`。

---

## 模式二：输入年龄外貌描述全新创造

根据文字需求（年龄、职业、性别、气质、场景），按照 **工业级写实公式** 拼装提示词：

### 核心公式（Prompt Formula）
```
[Shot Type & Framing] + [Subject Demographics & Vibe] + [Precise Facial Features & Natural Flaws] + [Skin Micro-Texture & SSS] + [Hair Details] + [Wardrobe] + [Cinematic Lighting & Neutral Studio/Natural Background] + [Camera Gear & Film Stock Parameters]
```

### 提示词结构规范（中英双语输出）
- **主体与年龄**：`A casting headshot portrait of a 42-year-old East Asian male dock worker...`
- **面部真实质感**：`weathered skin, visible pores, natural wrinkles around eyes, authentic skin imperfections, subtle subsurface scattering, realistic lip texture...`
- **光学与摄影参数**：`shot on Hasselblad H6D-100c, 85mm portrait lens, f/2.0 aperture, soft directional daylight, neutral gray backdrop, 35mm RAW film grain, uncompressed high fidelity.`
- **负向抑制词（Negative Tokens）**：`plastic skin, smooth face, airbrushed, 3d render, cartoon, anime, makeup blur, overexposed, symmetrical perfection, doll-like.`

---

## 工具链适配速查

| 平台/引擎 | 核心参数与写实技巧 | 推荐配置 |
| :--- | :--- | :--- |
| **Midjourney v6/v7** | 必须加 `--style raw` 降低过度美化；`--s 50` 保持写实；一致性引用使用 `--cref [URL] --cw 100` | `--ar 9:16 --style raw --s 75 --v 6.1` |
| **Flux.1 (Dev/Schnell)** | 采用高自然语言描述法；强化 `raw color photo` 与物理光影描述；支持 ComfyUI IP-Adapter / LoRA | 配合 Realistic Stock LoRA |
| **Stable Diffusion / SDXL** | 搭配 Photorealistic 大模型（如 Realistic Vision, RealVisXL）；必须加入负面词抑制塑料感 | 开启 ADetailer 脸部修复插件 |
| **AI 视频生成 (可灵/海螺/Runway)** | 以生成的正面定妆照作为 **首帧（First Frame）** 或 **角色参考图**，提示词聚焦动作与机位运镜 | 锁定面部 ID，微表情运动优先 |

---

## 避坑指南（防崩脸 5 大铁律）

1. ❌ **切勿使用空洞美化词**：禁止出现 `ultra beautiful, cute, perfect face, masterpiece, smooth skin`（会导致严重塑料磨皮感）。
2. 💡 **加入特定非标瑕疵**：刻意加入 `subtle skin redness, freckles, slight asymmetry, subtle acne scars, stray hairs` 增强真实感。
3. 📸 **限定中长焦镜头**：统一指定 `85mm portrait lens` 或 `105mm telephoto`，避免广角畸变导致五官拉伸变形。
4. 💡 **选用中性/漫射光源**：避免多色霓虹光直射面部，首选 `soft diffuse window light` 或 `Rembrandt studio lighting` 保证面部特征稳定。
5. 🎬 **构建角色三视图资产**：长视频或短剧制作，务必先生成角色【正面标准照 + 45度侧面 + 侧面照】作为全局资产包。
