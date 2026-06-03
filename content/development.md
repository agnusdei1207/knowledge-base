# 🧑‍💻 개발 허브

개발 문서, 아키텍처 메모, 구현 원칙, 릴리스 기준을 연결하는 상위 문서입니다.

관련 문서:
- [[tech-stack]]
- [[r-and-d]]
- [[operations]]
- [[projects]]
- [[hermes-architecture]]
- [[hermes-agent]]
- [[hermes-pipeline]]
- [[claude-code-mcp]]
- [[mcp-client-setup]]

---

## 1. 목적

개발 문서는 코드 설명서가 아니라 "왜 이렇게 만들고 있는가"를 공유하는 문서여야 합니다.

이 허브의 목적은 다음과 같습니다.

- 기술 선택 배경을 남긴다
- 구현 우선순위를 팀이 같이 본다
- 운영 문서와 분리되지 않게 연결한다

---

## 2. 현재 핵심 관심사

### A. 문서 기반 지식 시스템 구현

- Markdown 원본 유지
- Quartz 웹 배포 자동화
- AI 에이전트가 안전하게 수정 가능한 구조

### B. 검색 및 응답 품질 개선

- 문서 chunking 기준
- 링크 기반 탐색성
- 검색 결과 재정렬 전략
- 원본 Git 문서와 파생 검색 인덱스의 역할 분리
- MCP를 통한 에이전트 공통 접속 계층 설계

### C. 배포와 운영 단순화

- GitHub Actions 중심 배포
- Docker 기반 로컬 프리뷰
- 저장소 오염 최소화

---

## 3. 연결 문서

- 기반 기술: [[tech-stack]]
- 실험과 검증: [[r-and-d]]
- 운영 기준: [[operations]]
- 헤르메스 구조: [[hermes-architecture]]
- Hermes Agent 런타임: [[hermes-agent]]
- 데이터 흐름: [[hermes-pipeline]]
- Claude Code + MCP: [[claude-code-mcp]]
- 클라이언트 규격: [[mcp-client-setup]]
