#!/usr/bin/env bash

# ==============================================================================
# 사내 지식저장소 (Foam Workspace) 프로비저닝 스크립트
# ==============================================================================

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================${NC}"
echo -e "${YELLOW}       🌌 사내 지식저장소 (Foam) 구축 프로비저닝 시작      ${NC}"
echo -e "${CYAN}======================================================${NC}"

# 1. Git 설치 여부 확인
if ! command -v git &> /dev/null; then
    echo -e "${RED}[ERROR] Git이 설치되어 있지 않습니다. Git을 먼저 설치해 주세요.${NC}"
    exit 1
fi

echo -e "${GREEN}[INFO] Git 확인 완료.${NC}"

# 2. 로컬 Git 저장소 초기화
echo -e "${BLUE}[STEP 1] 로컬 Git 저장소 초기화 중...${NC}"
git init

# Git 로컬 사용자 이름/이메일 설정 (글로벌 설정이 안되어 있을 시의 오류 방지)
if [ -z "$(git config --global user.email)" ]; then
    echo -e "${YELLOW}[INFO] 글로벌 Git 사용자 정보가 발견되지 않아 로컬 설정을 지정합니다.${NC}"
    git config user.name "Company AI Assistant"
    git config user.email "ai-assistant@company.com"
fi

# 3. 파일 스테이징 및 첫 커밋 생성
echo -e "${BLUE}[STEP 2] 초기 템플릿 파일 스테이징 및 커밋...${NC}"
git add .
git commit -m "feat: initialize Foam knowledgebase structure with premium template"

# 4. 기본 브랜치를 main으로 설정
git branch -M main

# 5. 리모트 원격 저장소 추가
# 사용자 요구사항 맞춤 URL 설정 (철자 주의: knowlegebase)
REMOTE_URL="https://github.com/agnusdei1207/knowlegebase.git"
echo -e "${BLUE}[STEP 3] 원격 저장소 연동 중...${NC}"
echo -e "URL: ${YELLOW}${REMOTE_URL}${NC}"

# 이미 존재하면 삭제 후 재추가
git remote remove origin 2>/dev/null
git remote add origin "${REMOTE_URL}"

echo -e "${GREEN}[SUCCESS] 로컬 초기화 및 리모트 연동 완료!${NC}"
echo ""

# 6. 푸시 실행 (인증 오류 처리 지원)
echo -e "${BLUE}[STEP 4] GitHub 원격 저장소로 첫 푸시 시도...${NC}"
echo -e "${YELLOW}(주의: 첫 푸시 시 깃허브 로그인 또는 Access Token 입력 요구창이 뜰 수 있습니다.)${NC}"
echo -e "${CYAN}------------------------------------------------------${NC}"

# 푸시 시도
if git push -u origin main; then
    echo -e "${CYAN}------------------------------------------------------${NC}"
    echo -e "${GREEN}[COMPLETE] 성공적으로 GitHub 원격 저장소로 푸시 완료!${NC}"
    echo -e "${GREEN}사내 구성원들과 AI 에이전트가 즉시 사용할 준비가 끝났습니다.${NC}"
else
    echo -e "${CYAN}------------------------------------------------------${NC}"
    echo -e "${YELLOW}[WARNING] 원격 저장소로의 푸시가 보류되었습니다.${NC}"
    echo -e "이유: GitHub 인증(로그인 권한 또는 Personal Access Token)이 필요합니다."
    echo -e "하지만 걱정하지 마세요! 로컬 환경 셋팅과 첫 커밋은 완벽히 완료되었습니다."
    echo -e ""
    echo -e "아래 명령어를 복사하여 귀하의 터미널(Terminal)에 직접 붙여넣고 푸시해 주세요:${NC}"
    echo -e "${CYAN}  cd $(pwd) && git push -u origin main${NC}"
fi

echo ""
echo -e "${CYAN}======================================================${NC}"
echo -e "${GREEN}           🎉 Foam 지식저장소 셋팅 완료!            ${NC}"
echo -e "  1. PC에서 VS Code로 현재 폴더를 열고 Foam을 추천받아 까세요."
echo -e "  2. index.md를 열고 자유롭게 글을 쓰고 링크를 연결하세요."
echo -e "${CYAN}======================================================${NC}"
