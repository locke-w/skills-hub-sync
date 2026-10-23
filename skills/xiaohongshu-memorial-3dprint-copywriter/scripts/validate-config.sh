#!/bin/bash
# 配置文件完整性自动校验脚本 (v2.0.0)
# 用途：验证 config/constants.md 的必需配置、数值合理性、文献路径与校验词库
# 执行方式：bash scripts/validate-config.sh

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_ROOT/config/constants.md"
SKILL_MD="$SKILL_ROOT/SKILL.md"

ERRORS=0
WARNINGS=0
err()  { echo "  ✗ $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "  ⚠️  $1"; WARNINGS=$((WARNINGS + 1)); }
ok()   { echo "  ✓ $1"; }
num()  { grep -E "^[[:space:]]*$1:" "$CONFIG_FILE" | head -1 | grep -oE '[0-9]+' | head -1; }

echo "🔍 小红书技能配置校验工具 v2.0.0"
echo "========================================"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    exit 1
fi
ok "配置文件存在: config/constants.md"

echo ""
echo "� 必需配置项"
REQUIRED_CONFIGS=(
    "最小字数" "最大字数" "目标中位数"
    "平台最大字符长度" "实际发布最小字数" "实际发布最大字数"
    "Emoji计数口径" "标题Emoji上限" "标题备选数量" "最少公式类型数"
    "默认视角" "封面比例" "封面大字最少字数" "封面大字最大字数"
    "话题标签最少数量" "话题标签最多数量" "正文每段Emoji上限"
    "图片数量阈值_退出" "图片数量阈值_生成" "图片数量阈值_复用"
    "治理规则总数" "AI标识要求" "导流规则" "效果图声明"
    "图片存储根目录" "文案存储根目录" "文案文件名"
)
for key in "${REQUIRED_CONFIGS[@]}"; do
    if grep -qE "^[[:space:]]*$key:" "$CONFIG_FILE"; then ok "$key"; else err "缺失配置: $key"; fi
done

echo ""
echo "🔎 文献与脚本路径"
REQUIRED_PATHS=(
    "references/xiaohongshu_ai_rule.md" "references/bao.md" "references/conversion-and-traffic-safety.md"
    "references/copywriting-craft.md" "references/operations-playbook.md" "references/emotional-story-templates.md"
    "checklists/unified-checklist.md" "scripts/validate_copy.py" "scripts/inspect_images.py"
)
for path in "${REQUIRED_PATHS[@]}"; do
    if ! grep -q "$path" "$CONFIG_FILE"; then
        err "路径未在配置中登记: $path"
    elif [ -f "$SKILL_ROOT/$path" ]; then
        ok "$path"
    else
        err "文件不存在: $path"
    fi
done

echo ""
echo "🔎 数值合理性"
check_range() { # label min max [target]
    local label="$1" min="$2" max="$3" target="${4:-}"
    if [ -z "$min" ] || [ -z "$max" ]; then warn "$label 无法提取"; return; fi
    if [ "$min" -gt "$max" ]; then err "$label 最小值($min) > 最大值($max)"; return; fi
    if [ -n "$target" ] && { [ "$target" -lt "$min" ] || [ "$target" -gt "$max" ]; }; then
        err "$label 目标值($target) 不在 [$min, $max]"; return
    fi
    ok "$label [$min, $max]${target:+ 目标 $target}"
}
check_range "正文字数" "$(num 最小字数)" "$(num 最大字数)" "$(num 目标中位数)"
check_range "标题字数" "$(num 实际发布最小字数)" "$(num 实际发布最大字数)"
check_range "封面大字" "$(num 封面大字最少字数)" "$(num 封面大字最大字数)"
check_range "话题标签" "$(num 话题标签最少数量)" "$(num 话题标签最多数量)"
TITLE_MAX=$(num 实际发布最大字数); PLATFORM_MAX=$(num 平台最大字符长度)
if [ -n "$TITLE_MAX" ] && [ -n "$PLATFORM_MAX" ] && [ "$TITLE_MAX" -gt "$PLATFORM_MAX" ]; then
    err "标题推荐上限($TITLE_MAX) > 平台上限($PLATFORM_MAX)"
else
    ok "标题推荐上限 ≤ 平台上限"
fi

echo ""
echo "🔎 校验词库与校验器自测"
if command -v python3 >/dev/null 2>&1; then
    if python3 "$SCRIPT_DIR/validate_copy.py" --self-test >/tmp/xhs-selftest.$$ 2>&1; then
        ok "validate_copy.py --self-test 通过（词库 JSON 可解析、规则生效）"
    else
        err "validate_copy.py 自测失败，详情见 /tmp/xhs-selftest.$$"
    fi
else
    warn "未找到 python3，跳过校验器自测"
fi

echo ""
echo "🔎 版本与引用"
if grep -q "配置文件版本:" "$CONFIG_FILE"; then
    ok "配置文件版本 $(grep '配置文件版本:' "$CONFIG_FILE" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
else
    warn "未找到版本信息"
fi
grep -q "变更日志" "$CONFIG_FILE" && ok "变更日志存在" || warn "未找到变更日志"
if [ -f "$SKILL_MD" ]; then
    REF_COUNT=$(grep -c "config/constants.md" "$SKILL_MD" || true)
    if [ "$REF_COUNT" -lt 3 ]; then warn "SKILL.md 引用 config/constants.md 仅 $REF_COUNT 次，可能存在硬编码"; else ok "SKILL.md 引用 config/constants.md $REF_COUNT 次"; fi
else
    warn "SKILL.md 不存在"
fi

echo ""
echo "========================================"
echo "❌ 错误: $ERRORS    ⚠️  警告: $WARNINGS"
if [ "$ERRORS" -gt 0 ]; then
    echo "❌ 配置校验失败"
    exit 1
fi
echo "✅ 配置校验通过"
exit 0
