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
    hover_click(picker["x"] + picker["w"] / 2, picker["y"] + picker["h"] / 2)
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
            hover_click(hit["x"] + hit["w"] / 2, hit["y"] + hit["h"] / 2)
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
        print("⚠️ 未找到 New chat 按钮，继续当前会话")
        return
    # 配方：匹配有 2 个取第 2 个
    e = cands[1] if len(cands) > 1 else cands[0]
    hover_click(e["x"] + e["w"] / 2, e["y"] + e["h"] / 2)
    time.sleep(2)


def click_input(proc: str):
    box = []
    for _ in range(3):
        rows = ax_rows(proc)
        box = find_elements(rows, r"enter a prompt|输入|prompt|问点什么",
                            ("AXTextArea", "AXTextField", "AXGroup"))
        if box:
            break
        time.sleep(3)
    if not box:
        raise RuntimeError("找不到输入框")
    e = box[0]
    hover_click(e["x"] + e["w"] / 2, e["y"] + e["h"] / 2)


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


def click_download(proc: str, baseline: int, timeout_s: int, limit_phrases: list[str]) -> float:
    """轮询下载按钮数增加 → End 滚动 → 重读坐标 → 点 y 最大者。返回点击时刻。"""
    t0 = time.time()
    while True:
        if time.time() - t0 > timeout_s:
            raise TimeoutError(f"等待 Download 按钮超时（>{timeout_s}s）")
        rows = ax_rows(proc)
        ph = page_text_has(rows, limit_phrases)
        if ph:
            raise LimitHit(ph)
        if count_download_buttons(rows) > baseline:
            break
        time.sleep(POLL)
    frontmost(proc)
    btns = []
    for _ in range(6):
        key(119)  # End 键滚到底，让按钮进视口
        time.sleep(2.5)
        rows = ax_rows(proc)
        btns = find_elements(rows, r"download full size|下载完整|full size image")
        if btns:
            break
    if not btns:
        raise RuntimeError("滚动后未找到 Download 按钮")
    btn = max(btns, key=lambda r: r["y"])
    click_at = time.time()
    hover_click(btn["x"] + btn["w"] / 2, btn["y"] + btn["h"] / 2)
    return click_at


def wait_download(dl_dir: Path, since: float, timeout_s: int) -> Path | None:
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        cands = [f for f in dl_dir.iterdir()
                 if f.is_file() and f.stat().st_mtime > since and f.suffix.lower() in C.IMG_EXTS | {".heic"}]
        if cands:
            f = max(cands, key=lambda p: p.stat().st_mtime)
            time.sleep(1.5)  # 等写完
            return f
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
    POLL = int(cfg["gemini_app"].get("poll_interval_s", 15))
    per_timeout = int(cfg["gemini_app"].get("per_image_timeout_s", 420))
    dl_timeout = int(cfg["gemini_app"].get("download_timeout_s", 60))
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

    subprocess.run(["open", cfg["gemini_app"]["app_path"]], capture_output=True)
    time.sleep(6)
    frontmost(proc)
    window_pos(proc)  # 读一次确认窗口在
    if not args.continue_chat:
        new_chat(proc)
    model_selected = select_model(proc, cfg["gemini_app"].get(
        "model_labels", [cfg["gemini_app"].get("model_label", "Pro")]))

    first = True
    done_any = False
    for v in views:
        if v not in msgs:
            print(f"跳过视角 {v}（prompts.json 无）")
            continue
        files = C.asset_files(adir)
        if C.view_present(files, v):
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
                paste_image(ref)
                click_input(proc)
                keystroke_v()
                if not wait_attachment(proc, base_attach):
                    print("⚠️ 附件未在 AX 树出现，继续发送")
                time.sleep(1)
        # 发消息
        clipboard_text(msg)
        click_input(proc)
        keystroke_v()
        time.sleep(0.5)
        key(36)  # Return
        sent_at = time.time()
        # 等图 + 下载
        try:
            click_at = click_download(proc, base_dl, per_timeout, limit_phrases)
        except LimitHit as e:
            print(f"⛔ 命中额度上限（'{e}'），停止。已完成记录保留。")
            return 3
        except TimeoutError as e:
            print(f"⏱️ {e}")
            return 2
        new_file = wait_download(dl_dir, click_at, dl_timeout)
        if not new_file:
            print(f"⏱️ 视角 {v} 下载等待超时（>{dl_timeout}s）")
            return 2
        raw_dst = adir / "_raw" / f"{Path(target_name(cfg, v)).stem}_{new_file.name}"
        shutil.copy2(new_file, raw_dst)
        dst = adir / target_name(cfg, v)
        if dst.exists():
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
        if C.view_present(C.asset_files(adir), v):
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
