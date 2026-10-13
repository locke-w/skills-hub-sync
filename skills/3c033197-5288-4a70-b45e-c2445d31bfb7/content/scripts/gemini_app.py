#!/usr/bin/env python3
"""auto-xhs 阶段 2：gemini_app.py — 用 Google Gemini 网页 App（Safari Web App 壳）按 prompts.json 出图。

用法:
  gemini_app.py <char_dir|编号> [--views 00,01,02-10] [--dry-run] [--no-attach]
                [--new-chat|--continue-chat] [--crop/--no-crop]

退出码: 0 完成 · 1 参数/数据错误 · 2 超时 · 3 命中额度上限

实现细节照 macos-gui-automation 配方：AX 树定位（坐标每次重读）、ctypes CGEvent 点击、
pbcopy+⌘V 发消息、PNGf 剪贴板附图、End 键滚动后点 y 最大的 "Download full size image" 按钮、
~/Downloads 按 mtime 轮询新文件、sips 转 jpg / 居中裁 3:4。
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

SKILL_ROOT = C.SKILL_ROOT
TMP_OUT = Path("/tmp/auto-xhs")
IMG_PRIO = [".jpg", ".jpeg", ".png"]

_orig_print = print
def print(*args, **kwargs):
    kwargs.setdefault("flush", True)
    _orig_print(*args, **kwargs)

from gui import *  # noqa: F401,F403  (osa/CGEvent/剪贴板/AX 工具共用)


# ---------------------------------------------------------------- 消息拼装
def build_messages(cfg: dict, cdir: Path) -> dict[str, str]:
    """返回 view -> 完整消息文本（intro 已并入第一条待发消息由调用方处理——这里只返回视角消息）。"""
    pj = cdir / "prompts.json"
    if not pj.is_file():
        raise SystemExit(f"❌ 缺少 prompts.json：{cdir}（先跑 render_character.py）")
    data = json.loads(pj.read_text(encoding="utf-8"))
    posture = data.get("posture", "")
    full = posture in ("FW", "FM")
    framing = "从头到脚的全身构图" if full else "保留上半身胸像构图"
    spec_cn = "12 厘米全身" if full else "6 厘米胸像"
    slot_names = cfg["generation"]["slot_names"]
    tpl_dir = SKILL_ROOT / "prompts" / "gemini"
    tpl00 = (tpl_dir / "view_00.md").read_text(encoding="utf-8")
    tpl01 = (tpl_dir / "view_01.md").read_text(encoding="utf-8")
    tplsc = (tpl_dir / "view_scene.md").read_text(encoding="utf-8")
    attach = bool(C.cfg_get(cfg, "gemini_app.attach_reference", True))
    msgs = {}
    for v in C.VIEWS:
        if v not in data or "raw_prompt" not in data.get(v, {}):
            continue
        prompt = data[v]["raw_prompt"]
        if v == "00":
            msgs[v] = tpl00.format(prompt=prompt, framing_cn=framing)
        elif v == "01":
            ref = "附图" if attach else "视角 00 生成的照片"
            msgs[v] = tpl01.format(prompt=prompt, framing_cn=framing, spec_cn=spec_cn, ref_desc=ref)
        else:
            ref = "附图" if attach else "视角 01 生成的手办图"
            msgs[v] = tplsc.format(prompt=prompt, framing_cn=framing, spec_cn=spec_cn,
                                   ref_desc=ref, view=v, slot_name=slot_names.get(v, ""))
    return msgs


def intro_message(cdir: Path) -> str:
    tpl = (SKILL_ROOT / "prompts" / "gemini" / "intro.md").read_text(encoding="utf-8")
    pmd = (cdir / "prompts.md").read_text(encoding="utf-8")
    return tpl.format(prompts_md=pmd)


# ---------------------------------------------------------------- 参考图选择
def ref_image(cfg: dict, adir: Path, view: str) -> Path | None:
    stem = "0" if view == "01" else ("1" if view != "00" else None)
    if stem is None:
        return None
    files = {f.suffix.lower(): f for f in C.asset_files(adir) if f.stem == stem}
    for ext in IMG_PRIO:
        if ext in files:
            return files[ext]
    others = [f for f in C.asset_files(adir) if f.stem == stem]
    return others[0] if others else None


def target_name(cfg: dict, view: str) -> str:
    if view == "00":
        return "0.jpg"
    if view == "01":
        return "1.jpg"
    return f"视角{view}_{cfg['generation']['slot_names'][view]}.jpg"


# ---------------------------------------------------------------- GUI 流程
def current_model(rows: list[dict]) -> str | None:
    """从 mode picker 按钮描述读出当前选中模型。"""
    for r in rows:
        m = re.search(r"currently\s+(.+)$", r["desc"], re.I)
        if "mode picker" in r["desc"].lower() and m:
            return m.group(1).strip()
    return None


def select_model(proc: str, labels: list[str]) -> bool:
    """打开 mode picker，按 labels 顺序选第一个存在的菜单项。"""
    rows = ax_rows(proc)
    picker = next((r for r in rows if "mode picker" in r["desc"].lower()), None)
    if not picker:
        print(f"⚠️ 未找到模型选择器（mode picker），按当前默认模型继续（期望 {labels}）")
        return False
    before = current_model(rows)
    for label in labels:
        if before and label.lower() in before.lower():
            print(f"当前模型已是目标模型：{before}（期望 {labels}），保持使用")
            return True
    cx, cy = picker["x"] + picker["w"] / 2, picker["y"] + picker["h"] / 2
    click_element_at(proc, cx, cy)
    items = []
    for _ in range(5):
        time.sleep(1.0)
        rows = ax_rows(proc)
        items = find_elements(rows, r".", ("AXMenuItem", "AXRadioButton"))
        if items:
            break
    for label in labels:
        hit = next((i for i in items
                    if re.search(rf"\b{re.escape(label)}\b", i["desc"], re.I)), None)
        if hit:
            if hit["desc"].lower().startswith("selected"):
                print(f"模型已是选中态：{hit['desc']}")
                key(53)
                return True
            hx, hy = hit["x"] + hit["w"] / 2, hit["y"] + hit["h"] / 2
            click_element_at(proc, hx, hy)
            time.sleep(2)
            rows = ax_rows(proc)
            now = current_model(rows)
            print(f"已选择模型：{hit['desc']} → 当前显示 {now or before}")
            return True
    key(53)
    print(f"⚠️ 菜单中未找到任一标签 {labels}，保持当前模型 {before}")
    return False


def new_chat(proc: str):
    rows = ax_rows(proc)
    cands = find_elements(rows, r"new chat|新对话|新建对话|开启新", ("AXButton", "AXMenuItem", "AXLink"))
    if not cands:
        print("ℹ️ 当前页面已是新会话（无需重复开启）")
        return
    e = cands[1] if len(cands) > 1 else cands[0]
    cx, cy = e["x"] + e["w"] / 2, e["y"] + e["h"] / 2
    print(f"   已定位并点击 New Chat 按钮: {e['desc']} 坐标 ({cx:.0f}, {cy:.0f})")
    click_element_at(proc, cx, cy)
    time.sleep(2)


def click_input(proc: str):
    frontmost(proc)
    time.sleep(0.15)
    box = []
    for _ in range(3):
        rows = ax_rows(proc)
        box = find_elements(rows, r"enter a prompt|输入|prompt|问点什么",
                            ("AXTextArea", "AXTextField", "AXGroup"))
        if box:
            break
        time.sleep(1.5)
    if not box:
        raise RuntimeError("找不到输入框")
    e = box[0]
    cx, cy = e["x"] + e["w"] / 2, e["y"] + e["h"] / 2
    click_element_at(proc, cx, cy, hover_s=0.2)
    time.sleep(0.2)



def wait_attachment(proc: str, baseline: int, timeout: int = 30) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        rows = ax_rows(proc)
        n = len(find_elements(rows, r"attachment|附件|image|图片"))
        if n > baseline:
            return True
        time.sleep(2)
    return False


def count_download_buttons(rows: list[dict]) -> int:
    return len(find_elements(rows, r"download full size|下载完整|full size image"))


def wait_for_new_image(proc: str, baseline: int, timeout_s: int, limit_phrases: list[str]):
    """等待 Gemini 生成图片完成（Download 按钮数增加），带实时心跳与防抖。"""
    t0 = time.time()
    print(f"   ⏱️ 开始等待 Gemini 生成图片 (当前基准: {baseline}, 超时: {timeout_s}s)...")
    while True:
        elapsed = int(time.time() - t0)
        if elapsed > timeout_s:
            raise TimeoutError(f"等待图片生成超时（>{timeout_s}s）")
        rows = ax_rows(proc)
        ph = page_text_has(rows, limit_phrases)
        if ph:
            raise LimitHit(ph)
        cnt = count_download_buttons(rows)
        # 生图至少需要 6 秒，防止刚发完消息时因视口回弹/重排导致按钮误增误判
        if cnt > baseline and elapsed >= 6:
            print(f"   🎉 检测到新图片已生成 (Download 按钮数从 {baseline} 增至 {cnt}, 耗时 {elapsed}s)！")
            return
        if elapsed > 0 and elapsed % 10 == 0:
            print(f"   ⏱️ Gemini 正在生成绘制中... (已等待 {elapsed}s)")
        time.sleep(POLL)


def scroll_to_golden_center(proc: str, max_steps: int = 15) -> dict | None:
    """动态闭环滚轮对齐：利用实时坐标反馈循环，将最新下载按钮精准调整到窗口黄金中央 (300 <= y <= 620)。
    彻底解决 End 键被输入框焦点拦截、导致按钮深埋在视口下方 (y > 2000) 点击落空的顽疾！
    """
    frontmost(proc)
    time.sleep(0.2)
    pos = window_pos(proc)
    win_x, win_y = pos[0], pos[1]
    safe_min_y = win_y + 120.0
    safe_max_y = win_y + 620.0
    target_center = win_y + 350.0  # 视口黄金中线

    CG = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")
    CG.CGEventCreateMouseEvent.restype = ctypes.c_void_p
    CG.CGEventCreateMouseEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint32, CGPoint, ctypes.c_uint32]
    CG.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]

    CG.CGEventCreateScrollWheelEvent.restype = ctypes.c_void_p
    CG.CGEventCreateScrollWheelEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32]

    # 将鼠标移动到窗口中间，确保滚轮事件直接送达 WebKit 滚动视口
    p = CGPoint(win_x + 400.0, target_center)
    ev = CG.CGEventCreateMouseEvent(None, 5, p, 0)
    CG.CGEventPost(0, ev)
    time.sleep(0.1)

    for step in range(max_steps):
        rows = ax_rows(proc)
        btns = find_elements(rows, r"download full size|下载完整|full size image")
        if not btns:
            return None
        b = max(btns, key=lambda x: x["y"])
        # 判断是否已经停在黄金安全视口中央
        if safe_min_y <= b["y"] <= safe_max_y:
            print(f"      🎯 滚轮对齐就绪: 目标按钮停在黄金中央 ({b['x']:.0f}, {b['y']:.0f})")
            return b

        diff = b["y"] - target_center
        # diff > 0 说明按钮在视口下方，需向下拉（滚轮向下 ticks 负数，内容向上移动）
        ticks = -int(diff / 2.0)
        ticks = max(-400, min(400, ticks))
        ev_scroll = CG.CGEventCreateScrollWheelEvent(None, 0, 1, ticks)
        CG.CGEventPost(0, ev_scroll)
        time.sleep(0.4)

    # 兜底校验：严禁返回屏外超限坐标
    rows = ax_rows(proc)
    btns = find_elements(rows, r"download full size|下载完整|full size image")
    if not btns:
        return None
    b = max(btns, key=lambda x: x["y"])
    if (win_y + 60.0) <= b["y"] <= (win_y + 750.0):
        print(f"      🎯 兜底校准完毕: 按钮在窗口可见区 ({b['x']:.0f}, {b['y']:.0f})")
        return b
    print(f"      ⚠️ 经过 {max_steps} 次滚轮对齐，按钮仍处于视口外 ({b['x']:.0f}, {b['y']:.0f})")
    return None


def download_image_reliable(proc: str, dl_dir: Path, since: float, timeout_s: int = 120) -> Path | None:
    """高可靠下载执行器：闭环滚轮对齐视口 -> 点击最新下载按钮 -> 充裕等待下载文件落盘（未落盘自动持续自愈补点）。"""
    t0 = time.time()
    last_click_t = 0.0
    retry_count = 0

    def try_click_button(reason: str) -> bool:
        nonlocal last_click_t, retry_count
        frontmost(proc)
        time.sleep(0.2)
        btn = scroll_to_golden_center(proc)
        if btn:
            cx, cy = btn["x"] + btn["w"] / 2.0, btn["y"] + btn["h"] / 2.0
            print(f"   📥 [{reason}] 点击黄金视口下载按钮: at ({cx:.0f}, {cy:.0f})...")
            click_element_at(proc, cx, cy, hover_s=0.5)
            last_click_t = time.time()
            retry_count += 1
            return True
        else:
            print(f"   ⚠️ [{reason}] 视口内未定位到安全按钮，尝试重置焦点与兜底滚动...")
            key(119)  # 辅助按 End 键
            return False

    # 首次点击
    print("   🎯 正在闭环滚轮对齐最新图片的下载按钮...")
    try_click_button("首次触发")

    # 监听下载文件
    print(f"   📁 监听下载目录: {dl_dir} (超时: {timeout_s}s)...")
    while time.time() - t0 < timeout_s:
        elapsed = int(time.time() - t0)
        cands = [f for f in dl_dir.iterdir()
                 if f.is_file() and f.stat().st_mtime > since and f.suffix.lower() in C.IMG_EXTS | {".heic"}]
        if cands:
            f = max(cands, key=lambda p: p.stat().st_mtime)
            # 确保文件大小正常（大于 10KB，非空临时文件）
            if f.stat().st_size > 10240:
                print(f"   🎉 成功下载图片: {f.name} ({f.stat().st_size / 1024 / 1024:.2f} MB, 耗时 {elapsed}s)！")
                time.sleep(1.2)
                return f

        # 自愈机制：若距离上次点击超过 16 秒仍未检测到落盘，自动重新激活窗口、对齐视口并补点（最多补点 6 次）
        time_since_click = time.time() - last_click_t
        if time_since_click >= 16.0 and retry_count < 6:
            print(f"   ⏳ 耗时 {elapsed}s (距离上次点击 {int(time_since_click)}s) 尚未检测到文件写入，执行第 {retry_count} 次自愈补点...")
            try_click_button(f"自愈补点 #{retry_count}")

        if elapsed > 0 and elapsed % 10 == 0:
            print(f"   ⏳ 正在从 Google 服务器下载原图中... (已等待 {elapsed}s)")
        time.sleep(2)

    return None






def to_jpg(src: Path, dst: Path):
    subprocess.run(["sips", "-s", "format", "jpeg", str(src), "--out", str(dst)],
                   capture_output=True, check=True)


def crop_to_34(img: Path):
    """居中裁成 3:4（原地）。"""
    w, h = C.image_size(img)
    if abs(w / h - 0.75) < 0.02:
        return False
    if w / h > 0.75:  # 太宽 → 裁宽
        nw, nh = int(h * 0.75), h
    else:             # 太高 → 裁高
        nw, nh = w, int(w / 0.75)
    subprocess.run(["sips", "-c", str(nh), str(nw), str(img)], capture_output=True, check=True)
    return True


class LimitHit(Exception):
    pass


POLL = 15


def run_views(cfg: dict, cdir: Path, adir: Path, views: list[str], args) -> int:
    proc = cfg["gemini_app"]["process"]
    global POLL
    POLL = int(cfg["gemini_app"].get("poll_interval_s", 8))
    per_timeout = int(cfg["gemini_app"].get("per_image_timeout_s", 420))
    dl_timeout = int(cfg["gemini_app"].get("download_timeout_s", 120))
    limit_phrases = cfg["gemini_app"].get("limit_phrases", [])
    attach = bool(C.cfg_get(cfg, "gemini_app.attach_reference", True)) and not args.no_attach
    crop = bool(cfg["images"].get("crop_scene_to_ratio", True)) and args.crop
    dl_dir = Path(cfg["paths"]["downloads"]).expanduser()

    msgs = build_messages(cfg, cdir)
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "_raw").mkdir(exist_ok=True)
    manifest_path = adir / "_raw" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else []
    model_selected = False

    print(f"📱 正在唤醒 Google Gemini App...")
    subprocess.run(["open", cfg["gemini_app"]["app_path"]], capture_output=True)
    time.sleep(3)
    print(f"🪟 激活 Gemini 窗口至前台并校验位置...")
    frontmost(proc)
    try:
        pos = window_pos(proc)
        print(f"   当前窗口位置: ({pos[0]:.0f}, {pos[1]:.0f})")
    except Exception as e:
        print(f"   ⚠️ 读取窗口位置异常: {e}")
    if not args.continue_chat:
        print(f"✨ 正在新建对话 (New Chat)...")
        new_chat(proc)
    print(f"🎯 检查模型选择器...")
    model_selected = select_model(proc, cfg["gemini_app"].get(
        "model_labels", [cfg["gemini_app"].get("model_label", "Pro")]))

    first = True
    done_any = False
    for v in views:
        if v not in msgs:
            print(f"跳过视角 {v}（prompts.json 无）")
            continue
        files = C.asset_files(adir)
        if not getattr(args, "force", False) and C.view_present(files, v):
            print(f"跳过视角 {v}（{adir.name} 已有成图）")
            continue
        msg = msgs[v]
        if first:
            msg = intro_message(cdir) + "\n\n" + msg
            first = False
        print(f"--- 发送视角 {v}")
        rows = ax_rows(proc)
        base_attach = len(find_elements(rows, r"attachment|附件|image"))
        base_dl = count_download_buttons(rows)
        # 附图
        if attach and v != "00":
            ref = ref_image(cfg, adir, v)
            if ref:
                print(f"   附参考图 {ref.name}")
                frontmost(proc)
                time.sleep(0.3)
                paste_image(ref)
                click_input(proc)
                time.sleep(0.3)
                keystroke_v()
                if not wait_attachment(proc, base_attach):
                    print("⚠️ 附件未在 AX 树出现，继续发送")
                time.sleep(1.2)
        # 发消息
        frontmost(proc)
        time.sleep(0.3)
        clipboard_text(msg)
        click_input(proc)
        time.sleep(0.3)
        keystroke_v()
        time.sleep(0.8)
        key(36)  # Return
        sent_at = time.time()
        # 等图 + 自愈下载
        try:
            wait_for_new_image(proc, base_dl, per_timeout, limit_phrases)
        except LimitHit as e:
            print(f"⛔ 命中额度上限（'{e}'），停止。已完成记录保留。")
            return 3
        except TimeoutError as e:
            print(f"⏱️ {e}")
            return 2

        new_file = download_image_reliable(proc, dl_dir, sent_at, dl_timeout)
        if not new_file:
            print(f"⏱️ 视角 {v} 下载等待超时（>{dl_timeout}s）")
            return 2


        raw_dst = adir / "_raw" / f"{Path(target_name(cfg, v)).stem}_{new_file.name}"
        shutil.copy2(new_file, raw_dst)
        dst = adir / target_name(cfg, v)
        if dst.exists():
            if getattr(args, "force", False):
                bk_dir = adir / "_backup"
                bk_dir.mkdir(parents=True, exist_ok=True)
                bk_file = bk_dir / f"{dst.stem}_backup_{int(time.time())}{dst.suffix}"
                try:
                    shutil.copy2(dst, bk_file)
                except Exception:
                    pass
            else:
                dst = adir / (dst.stem + "_new.jpg")
        to_jpg(new_file, dst)
        cropped = False
        if v not in ("00", "01") and crop:
            cropped = crop_to_34(dst)
            if not cropped:
                raw_dst.unlink(missing_ok=True)
        else:
            if not (v in ("00", "01")):
                pass
            else:
                raw_dst.unlink(missing_ok=True)
        w, h = C.image_size(dst) or (0, 0)
        manifest.append({"view": v, "file": dst.name,
                         "raw": raw_dst.name if raw_dst.exists() else None,
                         "sent_at": sent_at, "downloaded_at": time.time(),
                         "width": w, "height": h, "cropped": cropped,
                         "model_label": cfg["gemini_app"].get("model_labels"),
                         "model_selected": model_selected,
                         "prompt_sha1": hashlib.sha1(msgs[v].encode()).hexdigest()})
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
        done_any = True
        print(f"   ✅ {dst.name} {w}x{h}{'（已裁 3:4）' if cropped else ''}")

        # 成功转存至对应角色素材库后，安全删除 ~/Downloads 中的原始下载暂存文件
        try:
            if new_file.exists():
                new_file.unlink(missing_ok=True)
                print(f"   🧹 已自动清理 Downloads 暂存原图: {new_file.name}")
        except Exception as e:
            print(f"   ⚠️ 清理 Downloads 暂存原图失败: {e}")
    if not done_any:
        print("没有需要生成的视角")
    return 0


def dry_run(cfg: dict, cdir: Path, views: list[str], args) -> int:
    msgs = build_messages(cfg, cdir)
    intro = intro_message(cdir)
    out = TMP_OUT / cdir.name
    out.mkdir(parents=True, exist_ok=True)
    adir = C.asset_root(cfg) / cdir.name
    plan = []
    first = True
    for v in views:
        if v not in msgs:
            plan.append(f"视角 {v}：prompts.json 无，跳过")
            continue
        if not getattr(args, "force", False) and C.view_present(C.asset_files(adir), v):
            plan.append(f"视角 {v}：已有成图，跳过")
            continue
        m = (intro + "\n\n" + msgs[v]) if first else msgs[v]
        first = False
        (out / f"msg_{v}.txt").write_text(m, encoding="utf-8")
        ref = ref_image(cfg, adir, v) if (C.cfg_get(cfg, "gemini_app.attach_reference", True)
                                        and not args.no_attach) else None
        plan.append(f"视角 {v}：写 {out / ('msg_' + v + '.txt')}"
                    + (f"（附 {ref.name}）" if ref else ""))
    print("\n".join(plan))
    return 0


def probe_model(cfg: dict) -> int:
    """探测模式：打开 App、新建对话、选模型、截图，不发消息。"""
    proc = cfg["gemini_app"]["process"]
    subprocess.run(["open", cfg["gemini_app"]["app_path"]], capture_output=True)
    time.sleep(6)
    frontmost(proc)
    window_pos(proc)
    new_chat(proc)
    ok = select_model(proc, cfg["gemini_app"].get("model_labels", ["Pro"]))
    rows = ax_rows(proc)
    shot = TMP_OUT / "probe" / "model_selected.png"
    shot.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["screencapture", "-x", str(shot)], capture_output=True)
    print(f"model_selected={ok} · 当前模型: {current_model(rows) or '未读到'}")
    print(f"截图: {shot}")
    return 0 if ok else 1


def parse_views(s: str) -> list[str]:
    out = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out += [f"{i:02d}" for i in range(int(a), int(b) + 1)]
        else:
            out.append(f"{int(part):02d}")
    return [v for v in C.VIEWS if v in set(out)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Gemini App 批量出图（auto-xhs 阶段 2）")
    ap.add_argument("target", nargs="?", help="char_dir / 编号（--probe-model 时省略）")
    ap.add_argument("--views", default="00-10", help="如 00,01,02-10")
    ap.add_argument("--force", action="store_true", help="强制重新生成指定视角（不跳过已有成图并覆盖）")
    ap.add_argument("--dry-run", action="store_true", help="只写 /tmp/auto-xhs/<char>/msg_NN.txt")
    ap.add_argument("--no-attach", action="store_true")
    ap.add_argument("--new-chat", dest="continue_chat", action="store_false", default=False)
    ap.add_argument("--continue-chat", dest="continue_chat", action="store_true")
    ap.add_argument("--crop", dest="crop", action="store_true", default=True)
    ap.add_argument("--no-crop", dest="crop", action="store_false")
    ap.add_argument("--probe-model", action="store_true",
                    help="只打开 App、新建对话、选择模型并截图报告当前选中项，不发送任何消息")
    args = ap.parse_args()
    cfg = C.load_config()
    if args.probe_model:
        return probe_model(cfg)
    if not args.target:
        ap.error("需要 target（char_dir / 编号），或改用 --probe-model")
    cdir = C.resolve_char_dir(cfg, args.target)
    adir = C.asset_root(cfg) / cdir.name
    views = parse_views(args.views)
    if args.dry_run:
        return dry_run(cfg, cdir, views, args)
    return run_views(cfg, cdir, adir, views, args)


if __name__ == "__main__":
    sys.exit(main())
