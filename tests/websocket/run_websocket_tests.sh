#!/bin/bash

# WebSocket 테스트 실행 스크립트

echo "======================================"
echo "🧪 WebSocket 테스트 스크립트"
echo "======================================"
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 현재 디렉토리 저장
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 서버 실행 확인
check_server() {
    echo -e "${BLUE}🔍 서버 실행 확인 중...${NC}"
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|404"; then
        echo -e "${GREEN}✅ 서버가 실행 중입니다.${NC}"
        return 0
    else
        echo -e "${RED}❌ 서버가 실행되지 않았습니다.${NC}"
        echo -e "${YELLOW}   다음 명령으로 서버를 실행하세요: python main.py${NC}"
        return 1
    fi
}

# 패키지 설치 확인
check_packages() {
    echo -e "\n${BLUE}📦 필요한 패키지 확인 중...${NC}"
    
    local missing_packages=()
    
    # websockets 확인
    if ! python -c "import websockets" 2>/dev/null; then
        missing_packages+=("websockets")
    fi
    
    if [ ${#missing_packages[@]} -eq 0 ]; then
        echo -e "${GREEN}✅ 모든 패키지가 설치되어 있습니다.${NC}"
        return 0
    else
        echo -e "${RED}❌ 다음 패키지가 설치되어 있지 않습니다: ${missing_packages[*]}${NC}"
        echo -e "${YELLOW}   설치 명령: uv add ${missing_packages[*]}${NC}"
        return 1
    fi
}

# WebSocket 테스트 실행
run_manual_test() {
    echo -e "\n${BLUE}🖐️  WebSocket 테스트 실행 중...${NC}"
    echo "======================================"
    
    cd "$SCRIPT_DIR"
    if python manual_websocket_test.py; then
        echo -e "\n${GREEN}✅ 테스트 완료!${NC}"
    else
        echo -e "\n${RED}❌ 테스트 중 에러 발생${NC}"
    fi
}

# 메뉴 표시
show_menu() {
    echo ""
    echo "======================================"
    echo "테스트 옵션을 선택하세요:"
    echo "======================================"
    echo "1) WebSocket 테스트 실행"
    echo "2) 종료"
    echo "======================================"
    echo -n "선택 (1-2): "
}

# 메인 로직
main() {
    # 서버 확인
    if ! check_server; then
        exit 1
    fi
    
    # 패키지 확인
    if ! check_packages; then
        echo ""
        read -p "패키지를 설치하시겠습니까? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            uv add websockets
        else
            exit 1
        fi
    fi
    
    # 인자가 있으면 바로 테스트 실행
    if [ $# -gt 0 ]; then
        if [ "$1" == "test" ] || [ "$1" == "run" ]; then
            run_manual_test
        else
            echo -e "${RED}알 수 없는 옵션: $1${NC}"
            echo "사용법: $0 [test|run]"
            exit 1
        fi
        exit 0
    fi
    
    # 메뉴 표시
    while true; do
        show_menu
        read choice
        
        case $choice in
            1)
                run_manual_test
                ;;
            2)
                echo -e "\n${GREEN}종료합니다.${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}잘못된 선택입니다. 1-2 사이의 숫자를 입력하세요.${NC}"
                ;;
        esac
        
        echo ""
        read -p "계속하려면 Enter를 누르세요..."
    done
}

# 스크립트 실행
main "$@"

