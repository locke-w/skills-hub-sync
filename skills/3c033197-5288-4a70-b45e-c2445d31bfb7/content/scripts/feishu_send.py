#!/usr/bin/env python3
"""auto-xhs 阶段 5：feishu_send.py — 把发布包发到飞书联系人会话。

用法:
  feishu_send.py <编号|char_dir> [--dry-run] [--force] [--no-polish]

退出码: 0 完成 · 1 前置门禁不满足 · 2 GUI/发送失败 · 3 联系人/权限阻塞 · 4 已发送过（判重）

消息序列（纯文本）：
  1 分割线 → 2 图片（1.* + 视角02–10 共 10 张，尽量合并一条发出）→
  3 正文(+末行声明) → 4 8 条标题 → 5 话题标签 → 6 置顶评论。
"""
from __future__ import annotations

import argparse
import ctypes
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import validate_copy as VC  # noqa: E402
import inspect_images as II  # noqa: E402
from gui import (ax_rows, frontmost, osa, hover_click, key,  # noqa: E402
                 keystroke_v, clipboard_text, paste_image, send_clipboard_text,
                 send_file, paste_file, get_window_rect, feishu_coords)

TMP = Path("/tmp/auto-xhs")


# ---------------------------------------------------------------- 提取
def extract_pinned(doc: VC.Doc) -> str:
    out = []
    for kind, line in doc.lines:
        if kind != "pinned":
            continue
        s = re.sub(r"^>\s?", "", line.strip())
        if s:
            out.append(s)
    return "\n".join(out).strip()


def extract_decl(doc: VC.Doc) -> str:
    for kind, line in doc.lines:
        if kind == "decl" and line.strip():
            return re.sub(r"^>\s?", "", line.strip())
    return ""


def load_package(cdir: Path, rules: dict):
    """返回 (body_paras, decl, titles[text], tags, pinned)。"""
    path = cdir / "小红书文案.md"
    doc = VC.parse(path.read_text(encoding="utf-8"), str(path))
    issues, _ = VC.check(doc, rules)
    if any(i.level == "BLOCKER" for i in issues):
        raise SystemExit("❌ 文案存在 BLOCKER，先修：\n" + "\n".join(
            f"  [{i.code}] {i.msg}" for i in issues if i.level == "BLOCKER"))
    paras = VC.extract_body(doc)
    titles = [t["text"] for t in VC.extract_titles(doc)]
    tags = VC.extract_tags(doc)
    pinned = extract_pinned(doc)
    decl = extract_decl(doc)
    if not paras or len(titles) != 8 or not tags or not pinned:
        raise SystemExit(f"❌ 提取不完整：body={len(paras)} titles={len(titles)} "
                         f"tags={len(tags)} pinned={bool(pinned)}")
    return paras, decl, titles, tags, pinned


# ---------------------------------------------------------------- 润色
def call_pi(cfg: dict, system_path: Path, user_msg: str) -> str:
    cmd = [cfg["copy"]["pi_bin"], "-p", "--no-tools", "--no-session", "--no-skills",
           "--no-context-files", "--no-extensions", "--model", cfg["copy"]["model"],
           "--thinking", cfg["copy"]["thinking"], "--system-prompt", str(system_path)]
    r = subprocess.run(cmd, input=user_msg, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"pi 退出码 {r.returncode}: {r.stderr[:400]}")
    return r.stdout


def lex_scan(text: str, rules: dict) -> list[str]:
    """scope ∈ body/public/user/doc/body+pinned 的类别词库扫描，返回命中列表。"""
    hits = []
    for cat in rules["lex"]["categories"]:
        if cat.get("scope") not in ("body", "public", "user", "doc", "body+pinned"):
            continue
        if cat.get("level") not in ("BLOCKER", "MAJOR"):
            continue
        for t in cat.get("terms", []):
            if t and t in text:
                hits.append(f"{cat['name']}:{t}")
    return hits


def polish_check(titles: list[str], pinned: str, body: str, rules: dict) -> list[str]:
    probs = []
    if len(titles) != 8:
        probs.append(f"标题 {len(titles)} 条 ≠ 8")
    body_bi = VC.cjk_bigrams(body)
    for i, t in enumerate(titles, 1):
        _, cons = VC.xhs_len(t, rules["emoji_weight"])
        if not 14 <= cons <= 19:
            probs.append(f"标题{i} 保守字数 {cons}，需 14–19")
        if sum(1 for ch in t if VC.is_emoji(ch)) > 1:
            probs.append(f"标题{i} Emoji 超 1 个")
        if len(VC.cjk_bigrams(t) & body_bi) < 2:
            probs.append(f"标题{i} 与正文 CJK 2-gram 重合 <2")
        hits = lex_scan(t, rules)
        if hits:
            probs.append(f"标题{i} 词库命中 {hits}")
    n = VC.count_body(pinned)
    if not 60 <= n <= 150:
        probs.append(f"置顶评论 {n} 字，需 60–150")
    hits = lex_scan(pinned, rules)
    if hits:
        probs.append(f"置顶评论词库命中 {hits}")
    return probs


def polish(cfg: dict, rules: dict, paras, decl, titles, pinned, tmp: Path) -> tuple[list[str], str, bool]:
    """返回 (titles, pinned, used_fallback)。"""
    body = "\n".join(paras)
    user = "## 正文\n" + body + ("\n" + decl if decl else "") + \
        "\n\n## 原 8 条标题\n" + "\n".join(titles) + "\n\n## 原置顶评论\n" + pinned
    (tmp / "polish_input.txt").write_text(user, encoding="utf-8")
    sys_prompt = C.SKILL_ROOT / "prompts" / "feishu_polish.md"
    last_probs, raw = [], ""
    for attempt in (1, 2):
        msg = user if attempt == 1 else (
            user + "\n\n## 上次输出问题\n" + "\n".join(f"- {p}" for p in last_probs) +
            "\n逐条修正，重新输出 JSON。")
        raw = call_pi(cfg, sys_prompt, msg)
        (tmp / f"polish_raw_{attempt}.txt").write_text(raw, encoding="utf-8")
        t = raw.strip()
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```\s*$", "", t).strip()
        try:
            data = json.loads(t)
            new_titles = [str(x).strip() for x in data["titles"]]
            new_pinned = str(data["pinned"]).strip()
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            last_probs = [f"JSON 解析失败：{e}"]
            continue
        last_probs = polish_check(new_titles, new_pinned, body, rules)
        if not last_probs:
            print(f"润色通过（第 {attempt} 次）")
            return new_titles, new_pinned, False
        print(f"润色第 {attempt} 次未过：{last_probs[:3]}")
    print("⚠️ 润色两次未过，回退原标题/原置顶评论")
    return titles, pinned, True


# ---------------------------------------------------------------- 消息拼装
def collect_images(cfg: dict, adir: Path, cdir_name: str) -> list[Path]:
    views = cfg["feishu"]["image_views"]
    files = C.asset_files(adir)
    imgs, missing = [], []
    for v in views:
        f = None
        if v == "01":
            cands = [x for x in files if x.stem == "1"]
            f = cands[0] if cands else None
        else:
            cands = [x for x in files if x.stem.startswith(f"视角{v}")]
            f = cands[0] if cands else None
        if f:
            imgs.append(f)
        else:
            missing.append(v)
    if missing:
        raise SystemExit(f"❌ 缺视角图：{missing}")
    return imgs


def build_messages(cfg: dict, cdir: Path, paras, decl, titles, tags, pinned, imgs):
    divider = cfg["feishu"]["divider_template"].format(char_dir=cdir.name)
    body_txt = "\n\n".join(paras) + ("\n\n" + decl if decl else "")
    return [
        ("01_divider", divider),
        ("02_images", "\n".join(str(p) for p in imgs)),
        ("03_body", body_txt),
        ("04_titles", "\n".join(f"{i}. {t}" for i, t in enumerate(titles, 1))),
        ("05_tags", " ".join("#" + t for t in tags)),
        ("06_pinned", pinned),
    ]


# ---------------------------------------------------------------- 系统环境健康前置核验
def is_screen_locked() -> bool:
    """检测当前 macOS 是否处于锁屏状态（锁屏下 WindowServer 禁止渲染与 GUI 模拟）"""
    try:
        out = subprocess.check_output(["ioreg", "-n", "Root", "-d1"], text=True, errors="replace", timeout=3)
        return '"CGSSessionScreenIsLocked"=Yes' in out
    except Exception:
        return False


# ---------------------------------------------------------------- GUI（飞书为 Electron，AX 不暴露会话内容：用截图+OCR 核验）
def screenshot_ocr(tmp: Path, proc: str | None = None, chat_panel_only: bool = True) -> str:
    png = tmp / "feishu_screen.png"
    subprocess.run(["screencapture", "-x", str(png)], capture_output=True)
    # 只保留飞书窗口区域，并且默认只截取右侧会话面板（隔离左侧列表历史中的智能伙伴/Hermes）
    if proc:
        try:
            raw = osa(f'''
tell application "System Events" to tell process "{proc}"
  set win to missing value
  set best to 0
  repeat with wi in windows
    try
      set s to size of wi
      set a to (item 1 of s) * (item 2 of s)
      if a > best then
        set best to a
        set win to wi
      end if
    end try
  end repeat
  if win is not missing value then
    set p to position of win
    set s to size of win
    return (item 1 of p) & "," & (item 2 of p) & "," & (item 1 of s) & "," & (item 2 of s)
  else
    return "none"
  end if
end tell''')
            coords = [float(v) for v in re.findall(r"\d+\.?\d*", raw)]
            if len(coords) >= 4:
                x, y, w, h = coords[:4]
                from PIL import Image
                im = Image.open(png)
                # Retina 截图像素 = AX 坐标 × 2
                x_offset = (w * 0.40) if chat_panel_only else 0
                crop_x1 = int((x + x_offset) * 2)
                crop_y1 = int(y * 2)
                crop_x2 = int((x + w) * 2)
                crop_y2 = int((y + h) * 2)
                im.crop((crop_x1, crop_y1, crop_x2, crop_y2)).save(png)
        except Exception:
            pass
    out_parts = []
    # 1. 全图 OCR
    r = subprocess.run(["tesseract", png.name, "-", "-l", "chi_sim"], cwd=tmp,
                       capture_output=True, text=True, errors="replace", timeout=60)
    if r.stdout:
        out_parts.append(r.stdout)

    # 2. 定向聚焦：针对顶部 180px 标题栏 (含目标联系人姓名) 与底部 180px 输入框 (含“可以向自己发送文件或转发消息”)
    # 彻底杜绝聊天记录中大块黑色视频卡片对 Tesseract 默认版面分析的干扰
    try:
        from PIL import Image
        im = Image.open(png)
        im_w, im_h = im.size
        # 顶部标题栏 ROI (PSM 6 极速聚焦文字行)
        hdr_png = tmp / "feishu_header.png"
        im.crop((0, 0, im_w, min(180, im_h))).save(hdr_png)
        r_hdr = subprocess.run(["tesseract", hdr_png.name, "-", "-l", "chi_sim", "--psm", "6"],
                               cwd=tmp, capture_output=True, text=True, errors="replace", timeout=30)
        if r_hdr.stdout:
            out_parts.append(r_hdr.stdout)

        # 底部输入框 ROI (PSM 6 极速聚焦输入框占位符)
        ftr_png = tmp / "feishu_footer.png"
        im.crop((0, max(0, im_h - 180), im_w, im_h)).save(ftr_png)
        r_ftr = subprocess.run(["tesseract", ftr_png.name, "-", "-l", "chi_sim", "--psm", "6"],
                               cwd=tmp, capture_output=True, text=True, errors="replace", timeout=30)
        if r_ftr.stdout:
            out_parts.append(r_ftr.stdout)
    except Exception:
        pass

    out = "\n".join(out_parts)
    (tmp / "feishu_ocr_last.txt").write_text(out, encoding="utf-8")
    return out


def input_xy(proc: str) -> tuple[float, float]:
    """会话输入框文本区：居中偏左（宽比 0.60，底距 48pt），避开右侧 Aa、表情、剪刀等富文本工具栏图标。"""
    input_text_xy, _ = feishu_coords(proc)
    return input_text_xy


def send_btn_xy(proc: str) -> tuple[float, float]:
    """会话右下角发送按钮（蓝色纸飞机 ➤ 按钮）绝对坐标。"""
    _, send_xy = feishu_coords(proc)
    return send_xy


def click_feishu_send(proc: str = "Feishu", send_xy: tuple[float, float] | None = None):
    """显式点击飞书右下角发送按钮，辅以 Return 键作为双保险发出。"""
    if not send_xy:
        send_xy = send_btn_xy(proc)
    hover_click(*send_xy, hover_s=0.2)
    time.sleep(0.15)
    key(36)


def get_feishu_window_rect(proc: str) -> tuple[float, float, float, float]:
    """获取飞书主窗口位置与尺寸 (x, y, w, h)。"""
    return get_window_rect(proc)


def click_messages_tab(rows: list[dict], win_x: float, win_y: float) -> bool:
    """点击侧边栏「消息」按钮，确保回到消息主面板。"""
    btn = next((r for r in rows if r.get("role") == "AXRadioButton" and
                ("消息" in r.get("desc", "") or "chat" in r.get("desc", "").lower())), None)
    if btn:
        hover_click(btn["x"] + btn["w"] / 2, btn["y"] + btn["h"] / 2, hover_s=0.3)
        return True
    hover_click(win_x + 90, win_y + 150, hover_s=0.3)
    return False


def click_search_button(rows: list[dict], win_x: float, win_y: float) -> bool:
    """点击侧边栏搜索（⌘＋K）按钮。"""
    btn = next((r for r in rows if "搜索" in r.get("desc", "") or "search" in r.get("desc", "").lower()), None)
    if btn:
        hover_click(btn["x"] + btn["w"] / 2, btn["y"] + btn["h"] / 2, hover_s=0.4)
        return True
    hover_click(win_x + 90, win_y + 106, hover_s=0.4)
    return True


def check_is_valid_personal_conversation(contact: str, ocr_text: str) -> tuple[bool, str]:
    """严格校验是否为合法的个人单聊会话（在右侧会话面板中校验）。"""
    flat = re.sub(r"\s+", "", ocr_text)
    flat_lower = flat.lower()

    # 负向关键词严密阻断（右侧当前会话中绝对不能有智能体/Hermes）
    negative_terms = ["智能伙伴", "智能体", "hermes", "话题来自", "开发者小助手"]
    for neg in negative_terms:
        if neg in flat_lower:
            return False, f"检测到智能体/话题/系统通知关键词「{neg}」，坚决阻断发送以防误发！"

    # 正向校验：联系人名字，或者如果是给自己发包含“发送文件”特征
    if (contact not in flat) and ("发送文件" not in flat) and ("转发消息" not in flat):
        return False, f"屏幕中未识别到目标联系人「{contact}」或个人单聊特征"

    return True, "校验通过"


def open_conversation(cfg: dict, tmp: Path, force_reopen: bool = False) -> tuple[float, float]:
    """打开 Lark → 精准定位纯个人联系人会话 → 负向安全门禁校验 → 返回输入框坐标。"""
    if is_screen_locked():
        raise SystemExit("⛔ 检测到当前 macOS 处于锁屏状态！macOS 安全机制阻止锁屏状态下的 GUI 操作与屏幕截屏。\n💡 解决办法：请解锁 Mac 屏幕并确保飞书窗口已展开在前台，然后重新点击发送。")

    proc = cfg["feishu"]["process"]
    contact = cfg["feishu"]["contact"]

    subprocess.run(["open", "-a", cfg["feishu"]["app_path"]], capture_output=True)
    time.sleep(1.0)
    frontmost(proc)
    time.sleep(0.5)

    win_x, win_y, win_w, win_h = get_feishu_window_rect(proc)
    rows = ax_rows(proc)
    if not rows:
        raise SystemExit("⛔ 读不到飞书 AX 树（未登录/未授权辅助功能），停止。")

    # 若非强制重新打开，先快速验证当前是否已经在目标联系人会话中
    if not force_reopen:
        curr_ocr = screenshot_ocr(tmp, proc)
        ok, _ = check_is_valid_personal_conversation(contact, curr_ocr)
        if ok:
            print(f"✅ 当前已在联系人「{contact}」个人会话中，直接复用。")
            return input_xy(proc)

    # 步骤 1：先点击左侧导航栏的「消息」Tab，确保在消息面板
    click_messages_tab(rows, win_x, win_y)
    time.sleep(0.8)

    # 步骤 2：点击搜索按钮 (⌘+K)
    click_search_button(rows, win_x, win_y)
    time.sleep(1.2)

    # 步骤 3：粘贴搜索联系人
    clipboard_text(contact)
    keystroke_v()
    time.sleep(1.5)  # 等待搜索弹窗与候选项渲染完成

    # 步骤 4：核心修正：不要盲目回车或按↓！
    # 真实实测：搜索弹窗第1项是纯个人联系人「吴永佳」，坐标居中偏左：(win_x + 310, win_y + 215)
    first_item_x = win_x + 310
    first_item_y = win_y + 215
    hover_click(first_item_x, first_item_y, hover_s=0.5)
    time.sleep(1.8)

    # 步骤 5：截屏与 OCR 严密门禁校验
    ocr = screenshot_ocr(tmp, proc)
    is_valid, reason = check_is_valid_personal_conversation(contact, ocr)
    if not is_valid:
        raise SystemExit(f"⛔ 会话门禁拦截失败：{reason}。已停止发送，杜绝发送到错误会话！")

    print(f"✅ 成功定位并进入纯个人联系人「{contact}」会话，门禁验证通过。")
    return input_xy(proc)


def send_text(text: str, xy: tuple[float, float], proc: str = "Feishu"):
    """发送单段文本至飞书会话：聚焦输入框 -> 粘贴 -> 点击发送按钮 + Return 双保险发出。"""
    s_xy = send_btn_xy(proc)
    send_clipboard_text(text, input_xy=xy, proc=proc, send_btn_xy=s_xy)


def send_images(cfg: dict, imgs: list[Path], xy: tuple[float, float], proc: str = "Feishu") -> bool:
    """合并发送：逐张粘贴后，显式点击右下角发送按钮 + 按 Return 双保险发出。"""
    s_xy = send_btn_xy(proc)
    for img in imgs:
        paste_image(img)
        hover_click(*xy, hover_s=0.2)
        time.sleep(0.6)
        keystroke_v()
        time.sleep(int(cfg["feishu"].get("send_interval_s", 5)))
    click_feishu_send(proc, s_xy)
    return True


def sent_marker(tmp: Path) -> Path:
    return tmp / ".feishu_sent"


def find_character_video(cfg: dict, target_str: str, preferred_video: str | None = None) -> Path | None:
    """智能查找人物关联的已合成成片视频文件 (.mp4)"""
    if preferred_video and preferred_video != "auto":
        p = Path(preferred_video).expanduser()
        if p.is_file():
            return p

    m = re.search(r"(\d+)", str(target_str))
    if not m:
        return None
    char_num = int(m.group(1))

    video_root = Path(cfg.get("paths", {}).get("video", "/Users/wuyongjia/3D打印/3dprint-xhs-思念/视频素材")).expanduser()
    if not video_root.exists():
        return None

    candidates = []
    for f in video_root.rglob("*.mp4"):
        name = f.name
        if "silent" in name.lower() or name.startswith("clip_") or re.match(r"^c\d+\.mp4", name) or re.match(r"^v\d+\.mp4", name):
            continue
        if f"char{char_num}" in name or f"char_{char_num}" in name or f"char{char_num}_" in str(f.parent) or f"char_{char_num}_" in str(f.parent):
            candidates.append(f)

    if not candidates:
        return None

    def score(p: Path) -> float:
        n = p.name
        s = 0.0
        if "微电影" in n or "短剧" in n: s += 100.0
        if "展示视频" in n or "爆款" in n: s += 80.0
        try:
            s += p.stat().st_size / (1024 * 1024)
        except Exception:
            pass
        return s

    candidates.sort(key=score, reverse=True)
    return candidates[0]


def send_single_character(cfg: dict, rules: dict, target_str: str, args,
                            input_coord: tuple[float, float] | None = None) -> tuple[int, tuple[float, float] | None]:
    """发送单个长辈人物的完整发布包或成片视频到飞书联系人。返回 (exit_code, input_coord)。"""
    proc = cfg["feishu"].get("process", "Feishu")

    # 0. 早期健康门禁：真实发送前快速检测 macOS 锁屏状态
    if not args.dry_run and is_screen_locked():
        print(f"⛔ [{target_str}] 检测到当前 macOS 处于锁屏状态！\n   ⚠️ macOS 安全机制在锁屏状态下禁止 WindowServer 像素渲染与一切 GUI 模拟输入。\n   💡 解决指引：请在 Mac 电脑上输入密码解锁屏幕，并保持飞书窗口处于打开状态，然后重试发送。")
        return 3, input_coord

    # 1. 纯视频发送模式 (--only-video)
    if getattr(args, "only_video", False):
        video_path = find_character_video(cfg, target_str, getattr(args, "video", None))
        if not video_path or not video_path.is_file():
            print(f"❌ [{target_str}] 未找到关联的成片视频文件 (.mp4)！请先在 OpenMontage 工场生成微电影成片")
            return 1, input_coord

        size_mb = round(video_path.stat().st_size / 1024 / 1024, 2)
        print(f"🎬 [{target_str}] 匹配到成片视频: {video_path.name} ({size_mb} MB)")

        if args.dry_run:
            print(f"✅ [{target_str}] 视频 dry-run 校验通过 (路径: {video_path})")
            return 0, input_coord

        tmp = TMP / f"char_{target_str}"
        tmp.mkdir(parents=True, exist_ok=True)
        if not input_coord:
            try:
                input_coord = open_conversation(cfg, tmp)
            except SystemExit as e:
                print(e)
                return 3, None

        interval = int(cfg["feishu"].get("send_interval_s", 5))
        try:
            divider = f"------------------------char_{target_str} 视频微电影成片------------------------"
            print(f"🚀 [{target_str}] 正在发送视频分割标识与视频文件: {video_path.name}...")
            send_text(divider, input_coord, proc=proc)
            time.sleep(interval)
            s_xy = send_btn_xy(proc)
            send_file(video_path, input_coord, upload_wait_s=4.0, send_btn_xy=s_xy)
            time.sleep(interval)
            print(f"🎉 [{target_str}] 视频已成功发送至飞书联系人！")
            return 0, input_coord
        except Exception as e:
            print(f"⛔ [{target_str}] 视频发送中断: {e}")
            return 2, input_coord

    cdir = C.resolve_char_dir(cfg, target_str)
    adir = C.asset_root(cfg) / cdir.name
    info = II.inspect(cfg, adir)
    if not any(re.match(r"^1\.", i["name"]) for i in info["images"]):
        print(f"❌ [{cdir.name}] 缺 1 号图（标准像）")
        return 1, input_coord
    try:
        imgs = collect_images(cfg, adir, cdir.name)
    except SystemExit as e:
        print(f"❌ [{cdir.name}] {e}")
        return 1, input_coord
    try:
        paras, decl, titles, tags, pinned = load_package(cdir, rules)
    except SystemExit as e:
        print(f"❌ [{cdir.name}] {e}")
        return 1, input_coord

    tmp = TMP / cdir.name
    tmp.mkdir(parents=True, exist_ok=True)
    marker = sent_marker(tmp)
    if not args.dry_run and not args.force and marker.is_file():
        print(f"⏭️ [{cdir.name}] 已发送过（命中本地发送标记 {marker.name}），跳过。加 --force 可重发。")
        return 4, input_coord

    polished, fallback = False, False
    if cfg["feishu"].get("polish", True) and not args.no_polish:
        try:
            titles, pinned, fallback = polish(cfg, rules, paras, decl, titles, pinned, tmp)
            polished = not fallback
        except Exception as e:
            print(f"⚠️ [{cdir.name}] 润色调用失败（{e}），回退原标题/置顶")
            fallback = True
    msgs = build_messages(cfg, cdir, paras, decl, titles, tags, pinned, imgs)

    if args.dry_run:
        for name, txt in msgs:
            p = tmp / f"feishu_{name}.txt"
            p.write_text(txt, encoding="utf-8")
        if getattr(args, "include_video", False) or getattr(args, "video", None):
            v_path = find_character_video(cfg, target_str, getattr(args, "video", None))
            if v_path:
                print(f"🎬 [{cdir.name}] dry-run 匹配到附加视频: {v_path.name} ({round(v_path.stat().st_size / 1024 / 1024, 2)} MB)")
            else:
                print(f"⚠️ [{cdir.name}] 未找到附加视频成片")
        print(f"✅ [{cdir.name}] dry-run 完成 (polish={'on' if polished else ('fallback' if fallback else 'off')})")
        return 0, input_coord

    proc = cfg["feishu"]["process"]
    divider = msgs[0][1]

    # 获取/复用输入框坐标
    if not input_coord:
        try:
            input_coord = open_conversation(cfg, tmp)
        except SystemExit as e:
            print(e)
            return 3, None
        except Exception as e:
            print(f"❌ 唤起飞书会话失败: {e}")
            return 2, None

    # OCR 判重：会话截图中若已含本人物目录名，视为已发送
    needle = "_".join(cdir.name.split("_")[:2])
    if not args.force and needle in re.sub(r"\s+", "", screenshot_ocr(tmp, proc)):
        print(f"⏭️ [{cdir.name}] 已发送过（OCR 判重命中会话中的 char_dir），跳过。加 --force 可重发。")
        return 4, input_coord

    interval = int(cfg["feishu"].get("send_interval_s", 5))
    merged = True
    try:
        print(f"🚀 [{cdir.name}] 正在发送 6 条消息包...")
        send_text(divider, input_coord, proc=proc)
        time.sleep(interval)
        merged = send_images(cfg, imgs, input_coord, proc=proc)
        time.sleep(interval)
        for name, txt in msgs[2:]:
            send_text(txt, input_coord, proc=proc)
            time.sleep(interval)

        # 追加发送成片视频
        if getattr(args, "include_video", False) or getattr(args, "video", None):
            v_path = find_character_video(cfg, target_str, getattr(args, "video", None))
            if v_path and v_path.is_file():
                v_size = round(v_path.stat().st_size / 1024 / 1024, 2)
                print(f"🎬 [{cdir.name}] 正在追加发送微电影成片: {v_path.name} ({v_size} MB)...")
                s_xy = send_btn_xy(proc)
                send_file(v_path, input_coord, upload_wait_s=4.0, send_btn_xy=s_xy)
                time.sleep(interval)
            else:
                print(f"⚠️ [{cdir.name}] 启用了附带视频，但未找到已生成的 .mp4 成片，跳过视频追加")
    except Exception as e:
        print(f"⛔ [{cdir.name}] 发送中断：{e}")
        return 2, input_coord

    time.sleep(3)
    import difflib
    ocr_flat = re.sub(r"\s+", "", screenshot_ocr(tmp, proc))
    def fuzzy(needle_str: str, n: int = 10) -> bool:
        needle_str = re.sub(r"\s+", "", needle_str)[:n]
        return any(difflib.SequenceMatcher(None, needle_str, ocr_flat[i:i + n]).ratio() >= 0.7
                   for i in range(max(1, len(ocr_flat) - n + 1)))
    ok_div = needle in ocr_flat or fuzzy(divider, 12)
    ok_body = (len(paras) > 0 and fuzzy(paras[0])) or fuzzy(msgs[5][1]) or fuzzy(msgs[4][1])
    print(f"✨ [{cdir.name}] 发送完毕！核验：分割线 {'✅' if ok_div else '❌'} · 正文首句 {'✅' if ok_body else '❌'}"
          f" · 图片合并 {'是' if merged else '否（逐张）'}")
    verified = ok_div or ok_body
    if verified:
        marker.write_text(divider + "\n" + datetime.now().isoformat() + "\n", encoding="utf-8")
    log = C.reports_dir(cfg) / "feishu-log.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"char_dir": cdir.name, "sent_at": datetime.now().isoformat(timespec="seconds"),
                            "polished": polished, "fallback": fallback,
                            "images_count": len(imgs), "merged_images": merged,
                            "verified": verified}, ensure_ascii=False) + "\n")
    return (0 if verified else 2), input_coord


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="飞书发布（auto-xhs 阶段 5，支持单角色及多角色批量挨个发送）")
    ap.add_argument("targets", nargs="+", help="目标编号或目录名，可传入多个（例如: 86 87 88）实现挨个批量发送")
    ap.add_argument("--dry-run", action="store_true", help="干跑测试，只生成消息不实际发送")
    ap.add_argument("--force", action="store_true", help="强制发送，忽略已发送标记")
    ap.add_argument("--no-polish", action="store_true", help="跳过 DeepSeek/pi 文案二次润色")
    ap.add_argument("--video", nargs="?", const="auto", default=None,
                    help="发送成片视频（可传具体 .mp4 路径，或传 auto/不带值自动匹配）")
    ap.add_argument("--only-video", action="store_true",
                    help="仅发送视频文件，不发送图文发布包")
    ap.add_argument("--include-video", action="store_true",
                    help="在发送图文发布包的同时，追加发送成片视频")
    args = ap.parse_args()
    cfg = C.load_config()
    rules = VC.load_config(cfg)

    print(f"📋 收到 {len(args.targets)} 个角色发送任务，目标联系人:「{cfg['feishu']['contact']}」")
    current_xy = None
    stats = {"success": 0, "skipped": 0, "failed": 0, "blocked": 0}

    for idx, tgt in enumerate(args.targets, 1):
        print(f"\n{'='*20} [{idx}/{len(args.targets)}] 开始处理角色: {tgt} {'='*20}")
        try:
            code, current_xy = send_single_character(cfg, rules, tgt, args, input_coord=current_xy)
            if code == 0:
                stats["success"] += 1
            elif code == 4:
                stats["skipped"] += 1
            elif code == 3:
                stats["blocked"] += 1
            else:
                stats["failed"] += 1
        except Exception as e:
            print(f"❌ 角色 {tgt} 处理异常: {e}")
            stats["failed"] += 1

    total_err = stats["failed"] + stats["blocked"]
    print("\n" + "=" * 50)
    print(f"🎉 批量发送流程结束: 成功 {stats['success']} · 跳过 {stats['skipped']} · 阻塞 {stats['blocked']} · 失败 {stats['failed']}")
    print("=" * 50)
    if stats["blocked"] > 0 and stats["failed"] == 0:
        return 3
    return 0 if total_err == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
