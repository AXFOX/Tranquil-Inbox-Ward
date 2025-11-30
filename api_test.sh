#!/bin/bash

# 增强版API测试脚本
# 用法: 
#   ./api_test.sh "测试内容"
#   ./api_test.sh -f filename.txt
#   ./api_test.sh -i (交互模式)

API_URL="http://localhost:8501/v1/models/emotion_model:predict"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示用法
show_usage() {
    echo "用法:"
    echo "  $0 \"测试内容\"                 # 测试指定文本"
    echo "  $0 -f <文件名>                # 测试文件中的内容"
    echo "  $0 -i                        # 交互模式"
    echo "  $0 -h                        # 显示帮助"
}

# 测试单个文本
test_single_text() {
    local text="$1"
    echo -e "${YELLOW}测试内容:${NC} $text"
    echo -e "${YELLOW}API URL:${NC} $API_URL"
    echo "----------------------------------------"
    
    # 发送请求并格式化输出
    response=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"instances\": [
                {\"token\":[\"$text\"]}
            ]
        }")
    
    # 尝试使用jq格式化输出，如果失败则原样输出
    if command -v jq >/dev/null 2>&1; then
        echo "$response" | jq .
    else
        echo "$response"
    fi
    echo ""
}

# 从文件读取并测试
test_from_file() {
    local filename="$1"
    
    if [[ ! -f "$filename" ]]; then
        echo -e "${RED}错误: 文件 $filename 不存在${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}从文件 $filename 读取测试内容...${NC}"
    echo ""
    
    # 逐行读取文件并测试
    line_number=1
    while IFS= read -r line; do
        # 跳过空行
        [[ -z "$line" ]] && continue
        
        echo -e "${GREEN}=== 测试第 $line_number 行 ===${NC}"
        test_single_text "$line"
        ((line_number++))
    done < "$filename"
}

# 交互模式
interactive_mode() {
    echo -e "${GREEN}进入交互模式，输入 'quit' 或 'exit' 退出${NC}"
    echo ""
    
    while true; do
        read -p "请输入测试内容: " input_text
        
        case "$input_text" in
            quit|exit)
                echo "退出交互模式"
                break
                ;;
            "")
                echo "输入不能为空"
                ;;
            *)
                test_single_text "$input_text"
                ;;
        esac
    done
}

# 主程序
main() {
    case "$1" in
        -h|--help)
            show_usage
            ;;
        -f|--file)
            if [[ -z "$2" ]]; then
                echo -e "${RED}错误: 请指定文件名${NC}"
                show_usage
                exit 1
            fi
            test_from_file "$2"
            ;;
        -i|--interactive)
            interactive_mode
            ;;
        "")
            echo -e "${RED}错误: 请提供测试内容或使用选项${NC}"
            show_usage
            exit 1
            ;;
        *)
            test_single_text "$1"
            ;;
    esac
}

# 运行主程序
main "$@"
