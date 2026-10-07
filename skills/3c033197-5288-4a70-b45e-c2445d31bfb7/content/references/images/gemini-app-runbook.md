# Gemini App GUI 自动化 Runbook（auto-xhs 阶段 2）

> 蒸馏自 `macos-gui-automation` 技能的 gemini-feishu-char-pipeline 配方。真实执行由 `scripts/gemini_app.py` 完成，本文档是排障与协议说明。

## 应用与坐标

- App：`~/Applications/Google Gemini.app`（打包版 Web App）。AX 进程名是 **`Web App`**，不是 `Google Gemini`。
- 激活：`osascript -e 'tell application "Google Gemini" to activate'`；AX 查询：`Application('Web App')`。
- 模型选择器：对话框上方工具栏的模型按钮（含 "Fast"/"Pro" 字样）。`gemini_app.py` 会自动尝试选择 **Pro**（`[gemini] prefer_model`），并把结果写入 manifest 的 `pro_selected`。
- 输入框：主窗口 scroll area 内的 `AXTextArea`。
- 发送：`prompt_delay` 秒等待后模拟 `Return`（入框为空时先检查附件是否贴上）。

## 参考图上传（视角 00/01 必带）

1. `0.jpg` / `1.jpg`（或已有 `0.jpeg`/`1.JPEG`）先 `sips` 转 PNG 到 `/tmp/auto-xhs/<char>/`；
2. `osascript` 写剪贴板：`set the clipboard to (read (POSIX file "...") as «class PNGf»)`；
3. 聚焦输入框后 `Cmd+V` 粘贴，等缩略图出现再输入提示词。

## 发送与轮询

- 每个视角的提示词作为**独立消息**发送，消息前可带人物锚定参考图（仅 00/01）。
- 生成完成后消息卡片右上角出现下载按钮（`AXButton`，描述含 "Download"/"下载"）。**不能用文件名排序判断新旧**——按 `Downloads` 目录（`[gemini] download_dir`）里文件的 **mtime** 轮询，只收 mtime ≥ 发送时刻的新文件。
- 长会话滚不到底时先发 `End` 键再重新读 AX 坐标（AX 坐标是文档坐标，滚动后必须重读）。
- 每个视角超时 `download_timeout` 秒；失败立即停，不反复重试。

## 落盘与裁切

- 下载图按 `视角NN_{槽位名}.jpg` 保存到 `{paths.asset_dir}/{char_dir}/`，00/01 存 `0.jpg`/`1.jpg`（已有文件绝不覆盖，见 `inspect_images.py`）。
- 02–10 下载后用 `sips` 读尺寸；比例不是 3:4 且 `[images] auto_crop=true` 时按 `crop_height_ratio` 居中裁切，裁切结果写 manifest `cropped` 字段。
- manifest：`{material_dir}/{char_dir}/gemini_manifest.json`，记录每个视角的提示词、文件名、尺寸、pro_selected、耗时。

## 阻塞即停

- 需要登录 Google 账号、弹出权限框（辅助功能/屏幕录制）、要求人机验证：**立即停止并报告**，把现场留给用户，不重试。
- dry-run（`--dry-run`）不触碰 GUI，只把将发送的消息写到 `/tmp/auto-xhs/<char>/msg_NN.txt`，用于验收提示词组装。
