#!/bin/bash
#
# Claude Code Skills 自动更新脚本
# 功能：从 GitHub 拉取最新代码并重新打包技能
#

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 技能目录
SKILLS_DIR="$HOME/.claude/skills"
cd "$SKILLS_DIR"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Claude Code Skills 自动更新${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# 1. 拉取最新代码
echo -e "${YELLOW}[1/3] 拉取 GitHub 最新代码...${NC}"
if git pull origin master; then
    echo -e "${GREEN}✓ 代码更新成功${NC}"
else
    echo -e "${RED}✗ 拉取失败，请检查网络连接${NC}"
    exit 1
fi
echo ""

# 2. 检测是否有 skill-creator
SCRIPT_CREATOR="$SKILLS_DIR/skill-creator/scripts/package_skill.py"
if [ ! -f "$SCRIPT_CREATOR" ]; then
    echo -e "${RED}✗ 未找到 skill-creator，无法打包技能${NC}"
    exit 1
fi

# 3. 重新打包修改过的技能
echo -e "${YELLOW}[2/3] 检测需要更新的技能...${NC}"

# 获取最近修改的技能目录
UPDATED_SKILLS=$(git diff --name-only HEAD@{1} HEAD | grep -oE '^[^/]+/' | sort -u | grep -v '^\.' || true)

if [ -z "$UPDATED_SKILLS" ]; then
    echo -e "${GREEN}没有技能需要更新${NC}"
else
    echo -e "${BLUE}发现更新的技能:${NC}"
    for skill_dir in $UPDATED_SKILLS; do
        if [ -f "$SKILLS_DIR/$skill_dir/SKILL.md" ]; then
            echo -e "  - ${skill_dir%/}"
        fi
    done
    echo ""

    # 重新打包
    echo -e "${YELLOW}[3/3] 重新打包技能...${NC}"
    PACKED_COUNT=0
    FAILED_COUNT=0

    for skill_dir in $UPDATED_SKILLS; do
        skill_path="$SKILLS_DIR/${skill_dir%/}"
        skill_name="${skill_dir%/}"

        # 跳过不包含 SKILL.md 的目录
        if [ ! -f "$skill_path/SKILL.md" ]; then
            continue
        fi

        echo -ne "  打包 $skill_name ... "

        if python3 "$SCRIPT_CREATOR" "$skill_path" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC}"
            ((PACKED_COUNT++))
        else
            echo -e "${RED}✗${NC}"
            ((FAILED_COUNT++))
        fi
    done

    echo ""
    echo -e "${GREEN}打包完成: $PACKED_COUNT 个成功, $FAILED_COUNT 个失败${NC}"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   更新完成！${NC}"
echo -e "${GREEN}================================================${NC}"
