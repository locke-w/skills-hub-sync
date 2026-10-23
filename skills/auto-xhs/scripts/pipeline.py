#!/usr/bin/env python3
"""auto-xhs 一条龙：validate_prompts → inspect_images → gemini_app（补缺视角）
→ write_copy（缺文案或 --force-copy）→ validate_copy → feishu_send。

用法: pipeline.py <编号> [--skip-images] [--skip-copy] [--skip-feishu]
                     [--force-copy] [--dry-run]
任一步非 0 退出即停并原样返回退出码。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import inspect_images as II  # noqa: E402
import validate_prompts as VP  # noqa: E402
import validate_copy as VC  # noqa: E402

HERE = Path(__file__).resolve().parent
PY = sys.executable


def step(name: str, cmd: list[str], dry: bool) -> int:
    print(f"\n===== [{name}] {' '.join(cmd)}")
    r = subprocess.run(cmd)
    print(f"===== [{name}] 退出码 {r.returncode}")
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="auto-xhs 全流程流水线")
    ap.add_argument("target")
    ap.add_argument("--skip-images", action="store_true")
    ap.add_argument("--skip-copy", action="store_true")
    ap.add_argument("--skip-feishu", action="store_true")
    ap.add_argument("--force-copy", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    cdir = C.resolve_char_dir(cfg, args.target)
    adir = C.asset_root(cfg) / cdir.name
    num = cdir.name.split("_")[1]

    # 1) 提示词门禁
    ch = C.load_character(cfg, cdir)
    issues = VP.check(ch, cfg)
    n_blk = sum(1 for i in issues if i.level == "BLOCKER")
    print(f"[prompts] {cdir.name}：BLOCKER={n_blk} MAJOR={sum(1 for i in issues if i.level == 'MAJOR')}")
    if n_blk:
        return 1

    # 2) 图片状态机
    if not args.skip_images:
        info = II.inspect(cfg, adir)
        print(f"[images] 状态机={info['state']}（{info['advice']}）")
        names = {i["name"] for i in info["images"]}
        if not any(n.startswith("0.") for n in names):
            print("⛔ 缺 0 号底图：请先把建模参考底图放入 " + str(adir) + "（命名为 0.jpg），不空跑。")
            return 1
        # 缺哪些视角
        missing = []
        for v in ["01"] + list(cfg["feishu"]["image_views"][1:]):
            want = "1." if v == "01" else f"视角{v}"
            if not any(n.startswith(want) for n in names):
                missing.append(v)
        if missing:
            views_arg = ",".join(str(int(x)) for x in missing)
            cmd = [PY, str(HERE / "gemini_app.py"), num, "--views", views_arg]
            if args.dry_run:
                cmd.append("--dry-run")
            rc = step("gemini", cmd, args.dry_run)
            if rc:
                return rc
        else:
            print("[images] 视角齐全，跳过生成")
    else:
        print("[images] --skip-images，跳过")

    # 3) 文案
    copy_path = cdir / "小红书文案.md"
    if not args.skip_copy:
        need = args.force_copy or not copy_path.is_file()
        if need:
            cmd = [PY, str(HERE / "write_copy.py"), num]
            if args.dry_run:
                cmd.append("--dry-run")
            if args.force_copy:
                cmd.append("--force")
            rc = step("write_copy", cmd, args.dry_run)
            if rc:
                return rc
        else:
            print(f"[copy] {copy_path.name} 已存在，跳过生成")
        if copy_path.is_file():
            doc = VC.parse(copy_path.read_text(encoding="utf-8"), str(copy_path))
            rules = VC.load_config(cfg)
            iss, _ = VC.check(doc, rules)
            blk = [i for i in iss if i.level == "BLOCKER"]
            print(f"[copy] validate_copy：{VC.verdict(iss)}")
            if blk:
                return 1
    else:
        print("[copy] --skip-copy，跳过")

    # 4) 飞书
    if not args.skip_feishu:
        cmd = [PY, str(HERE / "feishu_send.py"), num]
        if args.dry_run:
            cmd.append("--dry-run")
        rc = step("feishu", cmd, args.dry_run)
        if rc:
            return rc

    # 收尾
    info = II.inspect(cfg, adir)
    print("\n===== 收尾 =====")
    print("图片库：")
    for i in info["images"]:
        print(f"  {i['name']}  {i['width']}x{i['height']}  {i['ratio']}")
    print(f"文案：{copy_path}")
    print("场景图：")
    for i in info["images"]:
        if i["name"].startswith("视角"):
            print(f"  {adir / i['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
