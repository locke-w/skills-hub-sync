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
                 keystroke_v, clipboard_text, paste_image, send_clipboard_text)

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


# ---------------------------------------------------------------- GUI（飞书为 Electron，AX 不暴露会话内容：用截图+OCR 核验）
def screenshot_ocr(tmp: Path, proc: str | None = None) -> str:
    png = tmp / "feishu_screen.png"
    subprocess.run(["screencapture", "-x", str(png)], capture_output=True)
    # 只保留飞书窗口区域，避免屏幕上其他窗口文字干扰
    if proc:
        try:
            x, y, w, h = [float(v) for v in re.findall(r"\d+\.?\d*", osa(f'''
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
  set p to position of win
  set s to size of win
  return (item 1 of p) & "," & (item 2 of p) & "," & (item 1 of s) & "," & (item 2 of s)
end tell'''))]
            from PIL import Image
            im = Image.open(png)
            # Retina 截图像素 = AX 坐标 × 2
            im.crop((int(x * 2), int(y * 2), int((x + w) * 2), int((y + h) * 2))).save(png)
        except Exception:
            pass
    r = subprocess.run(["tesseract", png.name, "-", "-l", "chi_sim"], cwd=tmp,
                       capture_output=True, text=True, errors="replace", timeout=120)
    out = r.stdout
    (tmp / "feishu_ocr_last.txt").write_text(out, encoding="utf-8")
    return out


def input_xy(proc: str) -> tuple[float, float]:
    """会话输入框：主窗口右下区域（Electron 不暴露控件，用窗口内比例坐标）。"""
    script = f'''
tell application "System Events" to tell process "{proc}"
  set win to missing value
  set best to 0
  repeat with w in windows
    try
      set s to size of w
      set a to (item 1 of s) * (item 2 of s)
      if a > best then
        set best to a
        set win to w
      end if
    end try
  end repeat
  set p to position of win
  set s to size of win
  return (item 1 of p) & "," & (item 2 of p) & "," & (item 1 of s) & "," & (item 2 of s)
end tell'''
    x, y, w, h = [float(v) for v in re.findall(r"\d+\.?\d*", osa(script))]
    # 会话面板约从窗口 60% 宽开始，输入框在底部 ~4% 高处
    return (x + w * 0.80, y + h * 0.955)


def click_search_button(rows: list[dict]) -> bool:
    btn = next((r for r in rows if "搜索" in r["desc"] or "search" in r["desc"].lower()), None)
    if not btn:
        return False
    hover_click(btn["x"] + btn["w"] / 2, btn["y"] + btn["h"] / 2)
    return True


def open_conversation(cfg: dict, tmp: Path) -> tuple[float, float]:
    """打开 Lark → 搜索联系人 → OCR 确认在会话里 → 返回输入框坐标。"""
    proc = cfg["feishu"]["process"]
    subprocess.run(["open", "-a", cfg["feishu"]["app_path"]], capture_output=True)
    time.sleep(6)
    frontmost(proc)
    rows = ax_rows(proc)
    if not rows:
        raise SystemExit("⛔ 读不到飞书 AX 树（未登录/未授权辅助功能），停止。")
    contact = cfg["feishu"]["contact"]
    # 搜索联系人（实测侧边栏「搜索（⌘＋K）」按钮可点）
    if click_search_button(rows):
        time.sleep(2)
        clipboard_text(contact)
        keystroke_v()
        time.sleep(2.5)
        key(36)  # 回车进第一条结果
        time.sleep(3.5)
    else:
        print("⚠️ 未找到搜索按钮，尝试在当前会话直接验证")
    ocr = screenshot_ocr(tmp, proc)
    flat = re.sub(r"\s+", "", ocr)
    if contact not in flat:
        raise SystemExit(f"⛔ OCR 未在屏幕中识别到联系人「{contact}」，疑似未登录或进错会话，停止。")
    return input_xy(proc)


def send_text(text: str, xy: tuple[float, float]):
    send_clipboard_text(text, input_xy=xy)


def send_images(cfg: dict, imgs: list[Path], xy: tuple[float, float]) -> bool:
    """合并发送：逐张粘贴后只按一次 Return。"""
    for img in imgs:
        paste_image(img)
        hover_click(*xy)
        time.sleep(0.6)
        keystroke_v()
        time.sleep(int(cfg["feishu"].get("send_interval_s", 5)))
    key(36)
    return True


def sent_marker(tmp: Path) -> Path:
    return tmp / ".feishu_sent"


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="飞书发布（auto-xhs 阶段 5）")
    ap.add_argument("target")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-polish", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    rules = VC.load_config(cfg)

    cdir = C.resolve_char_dir(cfg, args.target)
    adir = C.asset_root(cfg) / cdir.name
    info = II.inspect(cfg, adir)
    if not any(re.match(r"^1\.", i["name"]) for i in info["images"]):
        print("❌ 缺 1 号图（标准像）")
        return 1
    imgs = []
    try:
        imgs = collect_images(cfg, adir, cdir.name)
    except SystemExit as e:
        print(e)
        return 1
    try:
        paras, decl, titles, tags, pinned = load_package(cdir, rules)
    except SystemExit as e:
        print(e)
        return 1

    tmp = TMP / cdir.name
    tmp.mkdir(parents=True, exist_ok=True)
    marker = sent_marker(tmp)
    if not args.dry_run and not args.force and marker.is_file():
        print(f"已发送过（判重命中本地发送标记 {marker.name}），退出码 4。加 --force 可重发。")
        return 4
    polished, fallback = False, False
    if cfg["feishu"].get("polish", True) and not args.no_polish:
        try:
            titles, pinned, fallback = polish(cfg, rules, paras, decl, titles, pinned, tmp)
            polished = not fallback
        except Exception as e:
            print(f"⚠️ 润色调用失败（{e}），回退原标题/置顶")
            fallback = True
    msgs = build_messages(cfg, cdir, paras, decl, titles, tags, pinned, imgs)

    if args.dry_run:
        for name, txt in msgs:
            p = tmp / f"feishu_{name}.txt"
            p.write_text(txt, encoding="utf-8")
            print(f"== {p}\n{txt}\n")
        print(f"dry-run 完成（polish={'on' if polished else ('fallback' if fallback else 'off')}）")
        return 0

    proc = cfg["feishu"]["process"]
    divider = msgs[0][1]
    try:
        xy = open_conversation(cfg, tmp)
    except SystemExit as e:
        print(e)
        return 3
    # OCR 判重：会话截图中若已含本人物目录名，视为已发送
    needle = "_".join(cdir.name.split("_")[:2])
    if not args.force and needle in re.sub(r"\s+", "", screenshot_ocr(tmp, proc)):
        print("已发送过（OCR 判重命中会话中的 char_dir），退出码 4。加 --force 可重发。")
        return 4

    interval = int(cfg["feishu"].get("send_interval_s", 5))
    merged = True
    try:
        send_text(divider, xy)
        time.sleep(interval)
        merged = send_images(cfg, imgs, xy)
        time.sleep(interval)
        for name, txt in msgs[2:]:
            send_text(txt, xy)
            time.sleep(interval)
    except Exception as e:
        print(f"⛔ 发送中断：{e}")
        return 2

    time.sleep(3)
    import difflib
    ocr_flat = re.sub(r"\s+", "", screenshot_ocr(tmp, proc))
    def fuzzy(needle: str, n: int = 10) -> bool:
        """OCR 常有单字误差，用滑窗相似度 ≥0.7 判定。"""
        needle = re.sub(r"\s+", "", needle)[:n]
        return any(difflib.SequenceMatcher(None, needle, ocr_flat[i:i + n]).ratio() >= 0.7
                   for i in range(max(1, len(ocr_flat) - n + 1)))
    ok_div = "_".join(cdir.name.split("_")[:2]) in ocr_flat or fuzzy(divider, 12)
    ok_body = fuzzy(paras[0]) or fuzzy(msgs[5][1]) or fuzzy(msgs[4][1])
    print(f"核验：分割线/目录名 {'✅' if ok_div else '❌'} · 正文首句 {'✅' if ok_body else '❌'}"
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
    return 0 if verified else 2


if __name__ == "__main__":
    sys.exit(main())
