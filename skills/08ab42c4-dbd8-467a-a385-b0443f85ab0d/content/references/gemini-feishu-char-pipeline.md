# Gemini 网页版批量生图 + 飞书交付流水线(char 系列实战配方)

来源:char_24 小红书发布前全流程实测(2026-09)。适用于纪念手办素材库 `/Users/wuyongjia/3D打印/素材/char_XX_*/` 逐视角生图→下载→归档→飞书发送。

## 目标布局

- 提示词源(Obsidian):`/Users/wuyongjia/obsidian-gitee/technology/🚀 项目/3D打印/素材/<char_dir>/prompts.md`(11 视角手册:视角 00/01 属 Midjourney,02~10 属 Gemini Imagen 3;每节含【煽情场景X·中文短名】与"#### 英文提示词 (可直接复制生图)"代码块)
- 图片库:`/Users/wuyongjia/3D打印/素材/<char_dir>/`(0.* 底图 + 1.* 标准像 + 视角02~10 归档)
- 文案落盘:Obsidian `<char_dir>/小红书文案.md`

## 前缀模板(自动拼装,禁写死人名)

从 prompts.md 顶部"人物唯一性指纹 IFTS / 模型规格"逐字提取特征,套用:

```
请以这张上传底图中的 6cm {角色分类名,如"80年代因病早逝年轻妻子"}树脂胸像手办为唯一角色参照(严格保持其{IFTS 特征中文串,如"清纯年轻圆润脸庞、清澈温柔含笑眼眸、自然偏分齐耳短发、白底蓝碎花的确良衬衫"}与一体化深色底座不变),生成一张 1:1 画幅的写实场景照片,画面与风格严格遵循以下英文提示词,直接生成图片、不要文字解释:

{视角NN 英文提示词原文}
```

注意 prompts.md 内部 IFTS 可能与 character_profile.md 冲突(如 char24:profile 写 28 岁双麻花辫,但实际模型/IFTS/底图是 33 岁 Bob 短发)。**以 prompts.md 顶部 IFTS + 实际底图为准**;英文段原文逐字照发,不改写。

## 步骤与脚本骨架

### 0. 预备:消息文件预拼

用 python 正则从 prompts.md 切分各视角并抽取 ```text 代码块,拼成 `/tmp/msg_NN.txt`(前缀+英文段),9 个视角一次生成,后续只发送不重拼。

### 1. 新建会话 + 上传底图

- 点侧栏 "New chat"(AX 匹配有 2 个,取第 2 个元素;点击后窗口标题会从旧会话名变回 "Google Gemini",主区出现 "Hi wu, let's get into it" 即成功)。
- 上传:标准像若是 .jpg,先 `sips -s format png in.jpg --out /tmp/std.png`,置剪贴板 PNGf,AX 定位 description 含 "Enter a prompt" 的输入框 → ⌘V → 等 AX 树出现 `attachment` 图片元素(约 5~10s,勿看 vision 截图过早判断)。

### 2. 逐条发送

`pbcopy < msg_NN.txt` → 点输入框 → ⌘V → Return。发送后窗口标题自动变为中文首句摘要(如"怀旧树脂胸像写实摄影生成"),可用作发送成功的旁证。

### 3. 等图 + 下载(关键:先滚动再点)

1. 轮询 AX 树出现 description="Download full size image" 的按钮(轮询间隔 15s,上限 300~420s;生成中按钮不可见,页面可能短暂显示"正在创建您的图片")。
2. **按钮坐标是文档坐标**:直接点击会落空。先滚动使按钮进视口:最稳的是把 app 置前台后发 End 键(`key code 119`),等 2~3s 让懒加载完成,再重读按钮坐标。
3. 取 y 值最大的那个按钮(=最新一轮,历史轮次的按钮 y 为负),中心点用 hover_click(先 MouseMoved 停留 1.2s 触发 hover UI 再 down/up)。
4. 下载落在 `~/Downloads/Gemini_Generated_Image_*.jpg`,2048×2048。用 `stat -f %m` 与点击时刻比较轮询新文件(下载有时滞后 10s+,且左下角会出现 "Downloading full size..." toast)。
5. 校验 `sips -g pixelWidth -g pixelHeight` 后 mv 归档,文件名 = `视角NN_<场景短名>.jpg`(短名从【煽情场景X·中文短名】去 · 号;命名风格与已发布 char 目录保持一致,可先 ls 邻近 char 目录参照)。

### 4. 飞书交付(联系人吴永佳 / 进程 "Feishu")

1. `open -a /Applications/Lark.app`,AX 进程名是 **Feishu**(不是 Lark)。
2. 当前窗口即"吴永佳"会话(用户文件传输会话,输入框提示"可以向自己发送文件或转发消息")。发送顺序:
   - 分割线:`------------------------{char目录全称}------------------------`
   - 10 张图:1.jpg 标准像 + 视角02~10(先 sips 转 png → PNGf 剪贴板 → 点输入框 → ⌘V → Return;每张间隔 5~6s)
   - 标题 8 条 / 正文 / 标签池,各一条文本(pbcopy → ⌘V → Return)
3. 输入框定位:AX 中 x>650、宽>300 且 y 最大的 AXTextArea/AXTextField;若整树扫描太慢,直接取上次成功坐标点击。
4. 核验:连续多图会折叠为一条图片列表(AX 中多张 AXImage 同 bounds),统计右栏(x>700,宽>60)AXImage 计数即可;文本消息用 AXStaticText 抓取滚动核验。

## 实测时间线参考(char24)

单图从发送到 Download 按钮出现约 15~90s;下载文件滞后点击约 5~12s。9 张图全程约 50 分钟,大头在每张等待。

## 文案自检要点(写作后必跑)

- 正文字符数(去空白)180~220;标题可见字符 14~19(emoji 代理对按 1 计,勿用 Python len 直接数)。
- 标题 8 条覆盖 ≥5 种公式,必含 1 条童真视角型(孩子翻老照片)。
- 黑名单扫:"瞒着全家做决定/眼泪砸在键盘/冰冷树脂有了体温/爱没有消失/总觉得来日方长/100%"等;软件名扫 Blender/Midjourney/SD/Gemini 等。
- 文件从 `## 🏷️ 爆款备选标题` 直接开始,无前置 H1/分析段。
