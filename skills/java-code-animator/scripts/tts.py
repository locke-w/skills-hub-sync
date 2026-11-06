"""根据 storyboard.json 为每句旁白生成中文配音（edge-tts），并记录时长。

用法：
    python tts.py <课程目录>/storyboard.json [--voice zh-CN-YunxiNeural] [--rate +0%]

输出：
    <课程目录>/audio/<section_id>_<序号>.mp3
    <课程目录>/audio/durations.json   # narrated_scene.py 读取它来对齐音画

文本没变的句子会复用已有音频，修改旁白后重跑即可。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path

import edge_tts

DEFAULT_VOICE = "zh-CN-YunxiNeural"


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(out.stdout.strip())


async def synth(text: str, voice: str, rate: str, out: Path, retries: int = 3) -> None:
    for attempt in range(1, retries + 1):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(str(out))
            return
        except Exception as exc:  # 网络抖动时重试
            if attempt == retries:
                raise RuntimeError(f"配音失败：{text!r}：{exc}") from exc
            await asyncio.sleep(2 * attempt)


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--voice", default=None, help="默认读取 storyboard.voice，否则 zh-CN-YunxiNeural")
    parser.add_argument("--rate", default=None, help="语速，如 +10%%；默认读取 storyboard.rate 或 +0%%")
    args = parser.parse_args()

    if shutil.which("ffprobe") is None:
        print("缺少 ffprobe（随 FFmpeg 安装），请先安装 FFmpeg。", file=sys.stderr)
        return 1

    board = json.loads(args.storyboard.read_text(encoding="utf-8"))
    voice = args.voice or board.get("voice") or DEFAULT_VOICE
    rate = args.rate or board.get("rate") or "+0%"

    lesson_dir = args.storyboard.parent
    audio_dir = lesson_dir / "audio"
    audio_dir.mkdir(exist_ok=True)
    index_file = audio_dir / "durations.json"
    old = json.loads(index_file.read_text(encoding="utf-8")) if index_file.exists() else {}

    result: dict[str, list[dict]] = {}
    total = 0.0
    for section in board["sections"]:
        sid = section["id"]
        entries = []
        for i, text in enumerate(section["lines"]):
            rel = f"audio/{sid}_{i}.mp3"
            path = lesson_dir / rel
            cached = next(
                (e for e in old.get(sid, []) if e["file"] == rel and e["text"] == text and e.get("voice") == voice and e.get("rate") == rate),
                None,
            )
            if cached is None or not path.exists():
                await synth(text, voice, rate, path)
            dur = probe_duration(path)
            total += dur
            entries.append({"file": rel, "text": text, "duration": round(dur, 3), "voice": voice, "rate": rate})
        result[sid] = entries
        print(f"[{sid}] {len(entries)} 句，{sum(e['duration'] for e in entries):.1f} 秒")

    index_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完成：共 {total:.1f} 秒旁白 -> {index_file}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
