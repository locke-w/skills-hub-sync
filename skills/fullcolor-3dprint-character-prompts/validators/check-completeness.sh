#!/bin/bash
# 11 视角完整性：check-completeness.sh <prompts.md|prompts.json|人物目录>
# v5.0：薄包装，规则与解析统一由 validate_prompts.py 实现（直接解析 prompts.md，兼容 prompts.json）
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/validate_prompts.py" "$@" --only completeness
