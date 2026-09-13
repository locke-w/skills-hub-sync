#!/bin/bash
# 配置文件完整性自动校验脚本 (v1.0.0)
# 用途：验证 config/constants.md 配置完整性与一致性
# 执行方式：bash scripts/validate-config.sh

set -e  # 遇到错误立即退出

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_ROOT/config/constants.md"
CHECKLIST_FILE="$SKILL_ROOT/checklists/unified-checklist.md"

echo "🔍 小红书技能配置校验工具 v1.0.0"
echo "========================================"
echo ""

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 错误：配置文件不存在: $CONFIG_FILE"
    exit 1
fi

echo "✅ 配置文件存在: config/constants.md"

# 检查清单文件是否存在
if [ ! -f "$CHECKLIST_FILE" ]; then
    echo "⚠️  警告：检查清单文件不存在: $CHECKLIST_FILE"
else
    echo "✅ 检查清单存在: checklists/unified-checklist.md"
fi

echo ""
echo "📋 开始配置完整性检查..."
echo "----------------------------------------"

ERRORS=0
WARNINGS=0

# 必需配置项列表
declare -a REQUIRED_CONFIGS=(
    "最小字数:"
    "最大字数:"
    "目标中位数:"
    "平台最大字符长度:"
    "实际发布最小字数:"
    "实际发布最大字数:"
    "点赞权重:"
    "收藏权重:"
    "评论权重:"
    "转发权重:"
    "关注权重:"
    "长评加权系数:"
    "图片数量阈值_退出:"
    "图片数量阈值_生成:"
    "图片数量阈值_复用:"
    "摄影机位数:"
    "生活实景数:"
    "情感道具组数:"
    "光影氛围数:"
    "总组合数:"
    "治理规则总数:"
)

# 检查必需配置项
echo ""
echo "🔎 检查必需配置项..."
for config in "${REQUIRED_CONFIGS[@]}"; do
    if grep -q "$config" "$CONFIG_FILE"; then
        echo "  ✓ $config"
    else
        echo "  ✗ 缺失配置: $config"
        ((ERRORS++))
    fi
done

# 检查文献路径配置
echo ""
echo "🔎 检查文献路径配置..."
declare -a REQUIRED_PATHS=(
    "references/xiaohongshu_ai_rule.md"
    "references/bao.md"
    "references/conversion-and-traffic-safety.md"
)

for path in "${REQUIRED_PATHS[@]}"; do
    if grep -q "$path" "$CONFIG_FILE"; then
        echo "  ✓ 路径已配置: $path"
        # 检查实际文件是否存在
        FULL_PATH="$SKILL_ROOT/$path"
        if [ -f "$FULL_PATH" ]; then
            echo "    ✓ 文件存在"
        else
            echo "    ⚠️  文件不存在: $FULL_PATH"
            ((WARNINGS++))
        fi
    else
        echo "  ✗ 路径未配置: $path"
        ((ERRORS++))
    fi
done

# 数值合理性检查
echo ""
echo "🔎 检查数值合理性..."

# 提取字数配置
MIN_WORDS=$(grep "最小字数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
MAX_WORDS=$(grep "最大字数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
TARGET_WORDS=$(grep "目标中位数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)

if [ -n "$MIN_WORDS" ] && [ -n "$MAX_WORDS" ] && [ -n "$TARGET_WORDS" ]; then
    echo "  正文字数配置: [$MIN_WORDS, $MAX_WORDS], 目标: $TARGET_WORDS"

    if [ "$MIN_WORDS" -gt "$MAX_WORDS" ]; then
        echo "  ✗ 错误: 最小字数($MIN_WORDS) > 最大字数($MAX_WORDS)"
        ((ERRORS++))
    elif [ "$TARGET_WORDS" -lt "$MIN_WORDS" ] || [ "$TARGET_WORDS" -gt "$MAX_WORDS" ]; then
        echo "  ✗ 错误: 目标中位数($TARGET_WORDS)不在[$MIN_WORDS, $MAX_WORDS]区间内"
        ((ERRORS++))
    else
        echo "  ✓ 字数配置合理"
    fi
else
    echo "  ⚠️  警告: 无法提取完整字数配置"
    ((WARNINGS++))
fi

# 提取标题字数配置
TITLE_MIN=$(grep "实际发布最小字数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
TITLE_MAX=$(grep "实际发布最大字数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
PLATFORM_MAX=$(grep "平台最大字符长度:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)

if [ -n "$TITLE_MIN" ] && [ -n "$TITLE_MAX" ] && [ -n "$PLATFORM_MAX" ]; then
    echo "  标题字数配置: [$TITLE_MIN, $TITLE_MAX], 平台上限: $PLATFORM_MAX"

    if [ "$TITLE_MIN" -gt "$TITLE_MAX" ]; then
        echo "  ✗ 错误: 标题最小字数($TITLE_MIN) > 最大字数($TITLE_MAX)"
        ((ERRORS++))
    elif [ "$TITLE_MAX" -gt "$PLATFORM_MAX" ]; then
        echo "  ✗ 错误: 实际最大字数($TITLE_MAX) > 平台上限($PLATFORM_MAX)"
        ((ERRORS++))
    else
        echo "  ✓ 标题字数配置合理"
    fi
else
    echo "  ⚠️  警告: 无法提取完整标题字数配置"
    ((WARNINGS++))
fi

# 检查版本信息
echo ""
echo "🔎 检查版本信息..."
if grep -q "配置文件版本:" "$CONFIG_FILE"; then
    VERSION=$(grep "配置文件版本:" "$CONFIG_FILE" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    echo "  ✓ 配置文件版本: $VERSION"
else
    echo "  ⚠️  警告: 未找到版本信息"
    ((WARNINGS++))
fi

if grep -q "变更日志" "$CONFIG_FILE"; then
    echo "  ✓ 变更日志存在"
else
    echo "  ⚠️  警告: 未找到变更日志"
    ((WARNINGS++))
fi

# 检查配置引用一致性（在SKILL.md中是否正确引用config/constants.md）
echo ""
echo "🔎 检查配置引用一致性..."
SKILL_MD="$SKILL_ROOT/SKILL.md"
if [ -f "$SKILL_MD" ]; then
    CONFIG_REF_COUNT=$(grep -c "config/constants.md" "$SKILL_MD" || true)
    echo "  SKILL.md 中引用 config/constants.md 次数: $CONFIG_REF_COUNT"

    if [ "$CONFIG_REF_COUNT" -lt 3 ]; then
        echo "  ⚠️  警告: 配置文件引用次数偏少，可能存在硬编码配置未迁移"
        ((WARNINGS++))
    else
        echo "  ✓ 配置引用充分"
    fi
else
    echo "  ⚠️  警告: SKILL.md 不存在，跳过引用检查"
    ((WARNINGS++))
fi

# 检查场景矩阵计算
echo ""
echo "🔎 检查场景矩阵计算..."
SHOTS=$(grep "摄影机位数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
SCENES=$(grep "生活实景数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
PROPS=$(grep "情感道具组数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
LIGHTS=$(grep "光影氛围数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)
TOTAL=$(grep "总组合数:" "$CONFIG_FILE" | grep -oE '[0-9]+' | head -1)

if [ -n "$SHOTS" ] && [ -n "$SCENES" ] && [ -n "$PROPS" ] && [ -n "$LIGHTS" ] && [ -n "$TOTAL" ]; then
    CALCULATED=$((SHOTS * SCENES * PROPS * LIGHTS))
    echo "  配置值: $SHOTS × $SCENES × $PROPS × $LIGHTS = $TOTAL"
    echo "  计算值: $CALCULATED"

    if [ "$CALCULATED" -eq "$TOTAL" ]; then
        echo "  ✓ 场景矩阵计算正确"
    else
        echo "  ✗ 错误: 总组合数不匹配（配置:$TOTAL, 计算:$CALCULATED）"
        ((ERRORS++))
    fi
else
    echo "  ⚠️  警告: 无法提取完整场景矩阵配置"
    ((WARNINGS++))
fi

# 最终结果
echo ""
echo "========================================"
echo "📊 校验结果汇总"
echo "========================================"
echo "✅ 通过检查"
echo "❌ 错误数量: $ERRORS"
echo "⚠️  警告数量: $WARNINGS"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "❌ 配置校验失败！请修复上述错误后重新运行。"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo "⚠️  配置校验通过，但存在 $WARNINGS 个警告，建议检查。"
    exit 0
else
    echo "✅ 配置校验完全通过！所有检查项均正常。"
    exit 0
fi
