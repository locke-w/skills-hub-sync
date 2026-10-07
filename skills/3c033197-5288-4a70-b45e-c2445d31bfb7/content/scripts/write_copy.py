#!/usr/bin/env python3
"""auto-xhs 阶段 3：write_copy.py — 用 pi + 配置模型写小红书发布包。

用法:
  write_copy.py <char_dir|编号> [--pov A2|B] [--type 情感共鸣型] [--date YYYY-MM-DD]
                [--force] [--dry-run] [--allow-no-images]

流程：校验 prompts（无 BLOCKER）→ inspect_images 需 REUSE（否则 --allow-no-images 才放行）
→ 拼 system.md（copy_system + attach_refs + 业务参数）与用户消息 → 调 pi → 后处理
→ validate_copy 校验，有 BLOCKER/MAJOR 且还有重试次数则带问题清单再调一次 → 落盘。
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
import inspect_images as II  # noqa: E402
import validate_copy as VC  # noqa: E402
import validate_prompts as VP  # noqa: E402

TMP = Path("/tmp/auto-xhs")


def build_system(cfg: dict) -> str:
    parts = [(C.SKILL_ROOT / "prompts" / "copy_system.md").read_text(encoding="utf-8")]
    parts.append("\n# 附：参考资料\n")
    for rel in cfg["copy"].get("attach_refs", []):
        f = C.SKILL_ROOT / rel
        parts.append(f"## {f.name}\n\n" + f.read_text(encoding="utf-8"))
    parts.append("\n# 附：业务参数\n")
    for k, v in cfg.get("business", {}).items():
        parts.append(f"- {k}：{v}")
    return "\n".join(parts)


def build_user(cfg: dict, ch: C.Character, adir_info: dict, args) -> str:
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    pov = args.pov or "由你按规则选择"
    ntype = args.ntype or "由你按规则选择"
    lines = [f"人物目录名：{ch.name}", f"日期：{date}",
             f"叙事视角：{pov}", f"笔记类型：{ntype}", "",
             "## 人物档案（character_profile.md 全文）", ""]
    prof = ch.dir / "character_profile.md"
    lines.append(prof.read_text(encoding="utf-8") if prof.is_file() else "（缺失）")
    lines += ["", "## 图片清单（文件名 · 宽×高 · 比例）"]
    for i in adir_info["images"]:
        lines.append(f"- {i['name']} · {i['width']}x{i['height']} · {i['ratio']}")
    if not adir_info["images"]:
        lines.append("- （无图片）")
    return "\n".join(lines)


def call_pi(cfg: dict, system_path: Path, user_msg: str) -> str:
    cmd = [cfg["copy"]["pi_bin"], "-p", "--no-tools", "--no-session", "--no-skills",
           "--no-context-files", "--no-extensions", "--model", cfg["copy"]["model"],
           "--thinking", cfg["copy"]["thinking"], "--system-prompt", str(system_path)]
    r = subprocess.run(cmd, input=user_msg, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"pi 退出码 {r.returncode}: {r.stderr[:500]}")
    return r.stdout


def postprocess(text: str, cfg: dict, rules: dict) -> str | None:
    t = text.strip()
    t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
    t = re.sub(r"\n?```\s*$", "", t)
    t = t.strip()
    if not t.startswith("# 小红书发布包："):
        return None
    # 标题 (xx字) → 实际保守字数
    def fix(m):
        plain, cons = VC.xhs_len(m.group(2), rules["emoji_weight"])
        return f"{m.group(1)}{m.group(2)} ({cons}字)"
    t = re.sub(r"^(\s*(?:\d+[\.、]|[-*])\s+(?:⭐\s*)?`?\[[^\]]+\]`?\s*)(.*?)\s*[\(（]\s*\d+\s*字\s*[\)）]",
               lambda m: fix(m), t, flags=re.M)
    return t


def set_verdict(text: str, verdict: str) -> str:
    line = f"**校验状态**：{verdict}"
    if re.search(r"\*\*校验状态\*\*：[^\n]*", text):
        return re.sub(r"\*\*校验状态\*\*：[^\n]*", line, text)
    return text.replace("**规则版本**", "**规则版本**", 1)  # fallback: append below
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description="小红书发布包生成（auto-xhs 阶段 3）")
    ap.add_argument("target")
    ap.add_argument("--pov", choices=["A2", "B"], default=None)
    ap.add_argument("--type", dest="ntype", default=None)
    ap.add_argument("--date", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-no-images", action="store_true")
    args = ap.parse_args()
    cfg = C.load_config()
    rules = VC.load_config(cfg)

    cdir = C.resolve_char_dir(cfg, args.target)
    ch = C.load_character(cfg, cdir)
    copy_name = cfg["copy"]["filename"]
    out_path = cdir / copy_name

    # 前置：prompts 无 BLOCKER
    p_issues = VP.check(ch, cfg)
    if any(i.level == "BLOCKER" for i in p_issues):
        print("❌ prompts 存在 BLOCKER，先修提示词：")
        for i in p_issues:
            if i.level == "BLOCKER":
                print(f"   [{i.code}] {i.msg}")
        return 1
    # 前置：图片状态机
    adir = C.asset_root(cfg) / ch.name
    info = II.inspect(cfg, adir)
    if info["state"] != "REUSE" and not args.allow_no_images:
        print(f"❌ 图片状态机={info['state']}（{info['advice']}）；如确需先写文案加 --allow-no-images")
        return 1

    tmp = TMP / ch.name
    tmp.mkdir(parents=True, exist_ok=True)
    system_md = build_system(cfg)
    (tmp / "system.md").write_text(system_md, encoding="utf-8")
    user_msg = build_user(cfg, ch, info, args)
    (tmp / "user.md").write_text(user_msg, encoding="utf-8")
    if args.dry_run:
        print(f"dry-run：已写 {tmp/'system.md'} 与 {tmp/'user.md'}，未调用 pi")
        return 0

    if out_path.exists() and not args.force:
        print(f"❌ {out_path} 已存在（加 --force 覆盖并备份旧文件）")
        return 1

    attempts, issues, text = 0, [], None
    max_attempts = 1 + int(cfg["copy"].get("retries", 1))
    while attempts < max_attempts:
        attempts += 1
        msg = user_msg if attempts == 1 else (
            user_msg + "\n\n## 上一版全文\n" + text +
            "\n\n## 校验问题清单\n" + "\n".join(f"- [{i.level} {i.code}] {i.msg}" for i in issues) +
            "\n\n按清单逐条修正，输出完整修订版。")
        raw = call_pi(cfg, tmp / "system.md", msg)
        text = postprocess(raw, cfg, rules)
        if text is None:
            issues = [VC.Issue("BLOCKER", "FORMAT", "输出未以 '# 小红书发布包：' 开头")]
            print(f"第 {attempts} 次：格式不合格")
            continue
        (tmp / f"draft_{attempts}.md").write_text(text, encoding="utf-8")
        issues, stats = VC.check(VC.parse(text, str(out_path)), rules)
        n_bad = sum(1 for i in issues if i.level in ("BLOCKER", "MAJOR"))
        print(f"第 {attempts} 次：{VC.verdict(issues)}（BLOCKER/MAJOR={n_bad}）")
        if n_bad == 0:
            break
    verdict = VC.verdict(issues)
    text = set_verdict(text, verdict)
    if out_path.exists():
        bak = cdir / f"小红书文案.bak-{datetime.now():%Y%m%d%H%M%S}.md"
        out_path.rename(bak)
        print(f"旧文案已备份：{bak.name}")
    out_path.write_text(text, encoding="utf-8")
    print(f"文案已写入：{out_path}")
    print(f"validate_copy 结论：{verdict}（尝试 {attempts} 次）")

    log = C.reports_dir(cfg) / "copy-log.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"char_dir": ch.name, "model": cfg["copy"]["model"],
                            "attempts": attempts, "verdict": verdict,
                            "issues_count": len(issues),
                            "at": datetime.now().isoformat(timespec="seconds")},
                           ensure_ascii=False) + "\n")
    return 1 if any(i.level == "BLOCKER" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
