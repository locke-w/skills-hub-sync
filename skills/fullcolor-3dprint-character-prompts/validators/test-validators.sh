#!/bin/bash
# 校验器自测：内置合格/不合格样例 + 抽查素材库 char_45
# v5.0：薄包装，规则与解析统一由 validate_prompts.py 实现（直接解析 prompts.md，兼容 prompts.json）
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -B "$SCRIPT_DIR/validate_prompts.py" --self-test
BASE="$(python3 -B -c "import sys; sys.path.insert(0, \"$SCRIPT_DIR\"); import validate_prompts as v; print(v.cfg_get(v.load_yaml(), \"paths.material_base\", \"\"))")"
SAMPLE="$(ls -d "$BASE"/char_45_* 2>/dev/null | head -1 || true)"
if [ -n "$SAMPLE" ]; then echo; echo "抽查：$SAMPLE"; python3 "$SCRIPT_DIR/validate_prompts.py" "$SAMPLE" || true; fi
