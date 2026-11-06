"""渲染课程、抽取审查帧、合并成片。

用法：
    # 渲染全部场景（按 storyboard 顺序），并合并为 <课程目录>/<title>.mp4
    python build.py <课程目录> --quality m

    # 只渲染某几个场景（调试用，不合并）
    python build.py <课程目录> --quality l --scenes S02Trace S03Edge

    # 渲染后，在每句旁白结束前抽一帧到 frames/，供 Critic 看图审查布局
    python build.py <课程目录> --quality l --frames

约定：课程目录下有 storyboard.json、lesson.py、audio/durations.json。
storyboard 中每个 section 的 "scene" 字段是 lesson.py 里的类名。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
QUALITY_DIR = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
LINE_PAD = 0.3  # 与 narrated_scene.LINE_PAD 保持一致


def get_media_dir(lesson_dir: Path) -> Path:
    """Windows 下深层目录易触发 MAX_PATH(260) 导致 partial_movie_files 报 WinError 3，自动改用短临时目录。"""
    if os.name == "nt" and len(str(lesson_dir)) > 80:
        digest = hashlib.md5(str(lesson_dir).encode("utf-8")).hexdigest()[:8]
        return Path(tempfile.gettempdir()) / f"jca_{digest}"
    return lesson_dir / "media"


def run_manim(lesson_dir: Path, media_dir: Path, quality: str, scene: str) -> tuple[bool, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SCRIPTS_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, "-m", "manim", f"-q{quality}", "--media_dir", str(media_dir), "lesson.py", scene],
        cwd=lesson_dir,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log = proc.stdout + proc.stderr
    return proc.returncode == 0, log


def scene_video(media_dir: Path, quality: str, scene: str) -> Path:
    return media_dir / "videos" / "lesson" / QUALITY_DIR[quality] / f"{scene}.mp4"


def extract_frames(lesson_dir: Path, video: Path, scene: str, lines: list[dict]) -> list[Path]:
    frames_dir = lesson_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    out, t = [], 0.0
    for i, line in enumerate(lines):
        t += line["duration"] + LINE_PAD
        shot = frames_dir / f"{scene}_{i:02d}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(t - 0.15, 0):.2f}", "-i", str(video), "-frames:v", "1", str(shot)],
            check=False,
        )
        if shot.exists():
            out.append(shot)
    return out


def safe_name(text: str) -> str:
    return re.sub(r'[\\/:*?"<>|\s]+', "_", text).strip("_") or "lesson"


def concat(lesson_dir: Path, videos: list[Path], output: Path) -> None:
    list_file = lesson_dir / "concat_list.txt"
    list_file.write_text("".join(f"file '{v.as_posix()}'\n" for v in videos), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", str(output),
        ],
        check=True,
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("lesson_dir", type=Path)
    parser.add_argument("--quality", choices=list(QUALITY_DIR), default="m")
    parser.add_argument("--scenes", nargs="*", help="只渲染这些场景，不合并")
    parser.add_argument("--frames", action="store_true", help="抽取审查帧到 frames/")
    args = parser.parse_args()

    lesson_dir = args.lesson_dir.resolve()
    media_dir = get_media_dir(lesson_dir)
    board = json.loads((lesson_dir / "storyboard.json").read_text(encoding="utf-8"))
    durations = json.loads((lesson_dir / "audio" / "durations.json").read_text(encoding="utf-8"))
    sections = board["sections"]
    targets = args.scenes or [s["scene"] for s in sections]
    by_scene = {s["scene"]: s for s in sections}

    failed = []
    for scene in targets:
        print(f"渲染 {scene} ...", flush=True)
        ok, log = run_manim(lesson_dir, media_dir, args.quality, scene)
        if not ok:
            failed.append(scene)
            tail = "\n".join(log.strip().splitlines()[-40:])
            print(f"[失败] {scene}\n{tail}\n", flush=True)
            continue
        video = scene_video(media_dir, args.quality, scene)
        print(f"  -> {video}")
        if args.frames and scene in by_scene:
            shots = extract_frames(lesson_dir, video, scene, durations[by_scene[scene]["id"]])
            print(f"  审查帧 {len(shots)} 张 -> {lesson_dir / 'frames'}")

    if failed:
        print(f"以下场景渲染失败：{', '.join(failed)}。修复后可用 --scenes 单独重渲。")
        return 1
    if args.scenes:
        return 0

    output = lesson_dir / f"{safe_name(board.get('title', 'lesson'))}.mp4"
    concat(lesson_dir, [scene_video(media_dir, args.quality, s) for s in targets], output)
    print(f"成片：{output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
