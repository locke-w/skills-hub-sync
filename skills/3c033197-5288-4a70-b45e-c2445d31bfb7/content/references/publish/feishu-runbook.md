# 阶段 5 · 发布到飞书 runbook

`scripts/feishu_send.py <编号|char_dir> [--dry-run] [--force] [--no-polish]`
把小红书发布包（10 图 + 正文 + 8 标题 + 话题 + 置顶）按 6 条消息发到配置里的飞书联系人（`studio.toml [feishu] contact`，默认「吴永佳」自己）。

## 发送流程

1. **前置门禁**（任一不满足退出码 1）：ASSET 下有 `1.*` + 视角02–10 共 10 图；MATERIAL 下 `小红书文案.md` 存在且 `validate_copy.py` 无 BLOCKER。
2. **解析文案**：复用 `validate_copy.py` 的 `parse/extract_*`，提取正文段落、正文末行声明、8 标题、话题、置顶。
3. **润色**（默认开）：`pi -p --no-tools --no-session --no-skills --no-context-files --no-extensions --model {copy.model} --thinking {copy.thinking} --system-prompt prompts/feishu_polish.md`，stdin = 正文 + 原标题 + 原置顶。产出 JSON `{"titles":[8],"pinned":"…"}`，校验 8 条 / 14–19 字 / Emoji≤1 / 与正文 CJK 2-gram≥2 / 词库扫描无 BLOCKER/MAJOR / pinned 60–150 字；不过重试 1 次，仍不过回退原文并打印 `回退`。
4. **GUI**：`open -a /Applications/Lark.app` → 前置 → 点侧边栏「搜索（⌘＋K）」按钮 → 粘贴联系人名 → Return 进会话 → 截图 OCR 确认联系人名在屏。
5. **判重**（见下节）。
6. **发送 6 条消息**，条间间隔 `feishu.send_interval_s`：
   ① 分割线 `------------------------{char_dir}------------------------`
   ② 10 张图（01+视角02–10，jpg 先 `sips` 转 png → `PNGf` 剪贴板 → ⌘V 逐张粘进输入框，全部粘完只按一次 Return，合并为一条消息）
   ③ 正文（段落间空行 + 末行声明）
   ④ 8 条标题（`1. 标题` 每行一条）
   ⑤ 话题标签一行（保留 #）
   ⑥ 置顶评论
7. **核验**：截图 OCR 模糊匹配分割线/正文首句（OCR 有单字误差，用滑窗相似度 ≥0.7）；写本地发送标记 `/tmp/auto-xhs/<char_dir>/.feishu_sent`。
8. **日志**：`MATERIAL/_reports/feishu-log.jsonl` 追加 `{char_dir, sent_at, polished, fallback, images_count, merged_images, verified}`。

## 判重（双层）

- **本地标记**：`/tmp/auto-xhs/<char_dir>/.feishu_sent` 存在 → 退出码 4「已发送过」。发送成功核验后自动写入。
- **OCR 判重**：进入会话后截图 OCR，若窗口内已出现 `char_NN` 目录名前缀 → 退出码 4。
- `--force` 跳过两层判重强制重发。

## 故障排查

| 现象 | 原因 / 处理 |
|---|---|
| `读不到飞书 AX 树`（退出 3） | 飞书未登录，或终端没有辅助功能权限（系统设置 → 隐私与安全性 → 辅助功能里加上终端/Devin）。 |
| `搜索不到联系人`（退出 3） | 联系人名与 `studio.toml [feishu] contact` 不一致；或搜索弹层是 WebView（AX 看不到），确认 OCR 截图 `feishu_screen.png` 里实际画面。 |
| OCR 全空 | **tesseract 必须 cwd=图片所在目录**（本机 brew tesseract 5.3.4 对绝对路径报 `file not found` 的怪癖）；直接喂 PNG，不要先 sips 转 jpg（sips 在 subprocess 里偶尔不落盘）。 |
| 找不到输入框 | 飞书是 Electron，**AX 不暴露会话区控件**——输入框坐标按窗口内比例算（宽 80%、高 95.5%），窗口尺寸异常时手动核对 `input_xy()` 的返回值。 |
| 图片没发出去 | 逐张 ⌘V 之间需 ≥4–5s（`send_interval_s`），粘贴太快会丢；合并发送在飞书里表现为一张宫格图。 |
| OCR 核验 ❌ | 先人工看 `/tmp/auto-xhs/<char_dir>/feishu_screen.png` 与 `feishu_ocr_last.txt`：消息可能已发出但 OCR 误差大（分割线里 CJK 易错读）——此时可手工写 `.feishu_sent` 标记防止重发。 |
| 重复发送 | 任何时候都不应发生：先查 `.feishu_sent`；若用户手工在飞书里删了历史，本地标记仍在，需 `--force` 才重发。 |

## 实测结论（2026-10-05，macOS，Lark.app）

- AX 进程名 **`Feishu`**；AX 树只能看到侧边栏按钮（含 `AXButton | 搜索（⌘＋K）`），**搜索弹层与会话区是 Electron WebView，AX 拿不到**——所以搜索/确认/核验一律走「点击搜索按钮 → 粘贴 → Return」+「screencapture + tesseract OCR」。
- 搜索快捷键实测：侧边栏搜索按钮标注为 `⌘＋K`，脚本优先直接点这个 AX 按钮（比按键更稳）；按钮找不到时回退 `⌘K`。
- 多图合并：10 张图连续 ⌘V 后一次 Return，飞书以**单条宫格消息**发出（merged_images=true）。
- 输入框：AX 坐标 `input_xy()` = 窗口左缘 +80% 宽 / +95.5% 高，实测命中底部输入区。
