#!/bin/bash
# 从 prompts.md 导出 prompts.json：md-to-json.sh <prompts.md> [输出路径，缺省为同目录 prompts.json]
# v5.0：薄包装，规则与解析统一由 validate_prompts.py 实现（直接解析 prompts.md，兼容 prompts.json）
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ $# -ge 1 ] || { echo "用法: $0 <prompts.md> [输出路径]"; exit 1; }
exec python3 "$SCRIPT_DIR/validate_prompts.py" "$1" --export-json "${2:-}" --only completeness,ifts
