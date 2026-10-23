# AI 短剧角色一致性与防崩脸全链路工作流

在 AI 短剧（AI Short Dramas）与 AI 视频制作中，**角色换脸、长相漂移、五官扭曲**是最大痛点。本工作流提供从“超写实定妆资产”到“视频分镜落地”的标准工业化管线。

---

## 1. 工业级制作全链路（4 步法）

```
Step 1: 角色基准资产生产 (Character Asset Creation)
        - 生成标准正面高清定妆照 (85mm, 中性光, 无过度表情)
        - 生成 45 度侧面照 + 90 度侧面照 (建立三维特征)
                          │
                          ▼
Step 2: 角色特征锁死 (Identity Anchoring)
        - 方案 A (云端轻量): Midjourney `--cref [URL] --cw 100`
        - 方案 B (短剧工业级): ComfyUI Flux / SDXL 训练专属 15-20 张高质量 LoRA
        - 方案 C (快速微调): IP-Adapter FaceID + ControlNet
                          │
                          ▼
Step 3: 图生视频 (Image-to-Video) 稳定驱动
        - 平台：可灵 (Kling 1.5/3.0)、海螺 (Minimax Hailuo)、Runway Gen-3、即梦 (Jimeng)
        - 规则：将定妆照/分镜起始图作为 First Frame (首帧)
        - 运镜：首选慢推镜头、环绕镜头、微表情特写，避免快速剧烈甩头
                          │
                          ▼
Step 4: 后期修补与超分 (Inpainting & Enhancement)
        - 对个别镜头崩脸区域使用 Face Inpaint 或 ADetailer 局部重绘
        - 4K Topaz Video AI 进行画质超分与胶片颗粒统一
```

---

## 2. 视频提示词防崩写法规范

在将图片输入视频生成模型（如 Kling、Minimax、Runway）时，**提示词不要重复描述面部细节**（会与首帧产生特征冲突），而应**专注于动态、微表情与摄影机运镜**：

### ❌ 错误示范（容易导致换脸）
```text
一个长着大眼睛高鼻梁的20岁美女在说话，很漂亮，4k画质。（模型会重新随机生成一张脸）
```

### ✅ 正确示范（锁脸防崩）
```text
[主体动作与微表情] + [视线方向] + [环境交互] + [摄影机运镜]
```
> **示例**：
> "The man in the reference image slightly turns his head towards the window, a subtle melancholic sigh, blinking naturally, soft breeze gently moving a few stray hairs, slow cinematic push-in camera shot, shallow depth of field, maintaining strict facial identity from the starting frame."

---

## 3. 短剧生产三大避坑准则

1. **表情中性原则**：定妆照绝不能使用咧嘴大笑、做鬼脸等极端表情。必须保持自然微闭嘴唇的平静/微沉思状态，为后续视频提供最稳定的几何锚点。
2. **光影中性原则**：定妆照避免强烈的单侧彩光或强背光，确保五官边缘和两颊的轮廓线完全清晰可见。
3. **分镜镜头分级**：
   - **近景/特写（Close-up）**：用最精准的定妆首帧生成，捕捉眼神与微表情。
   - **中远景/全身（Medium/Full Shot）**：允许适当弱化面部细节，重点放在服装风格、体态与动作张力上。
