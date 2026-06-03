+++
title = "⚙️ 운영 허브"

[taxonomies]
tags = ["work"]

[extra]
tags = ["work"]
+++

운영 절차, 배포 흐름, 문서 관리 규칙, 장애 대응 메모를 연결하는 상위 문서입니다.

관련 문서:
- [quartz-deployment](/knowledge-base/work/quartz-deployment/)
- [development](/knowledge-base/work/development/)
- [sales](/knowledge-base/work/sales/)
- [knowledgebase-decision-log](/knowledge-base/work/knowledgebase-decision-log/)
- [knowledge-pipeline](/knowledge-base/work/knowledge-pipeline/)
- [decap-cms](/knowledge-base/work/decap-cms/)
- [claude-code-mcp](/knowledge-base/work/claude-code-mcp/)
- [mcp-client-setup](/knowledge-base/work/mcp-client-setup/)
- [codex-sdk-operations](/knowledge-base/work/codex-sdk-operations/)

---

## 1. 운영 관점 핵심 원칙

- 원본 문서는 `content/`에만 둔다
- 배포는 자동화하고 수동 작업을 줄인다
- 운영 규칙은 개발 문서와 분리하지 않고 연결한다

---

## 2. 현재 운영 체크리스트

### 문서 운영

- 새 문서는 허브 문서와 연결되어 있는가
- 제목과 링크가 재사용 가능하게 작성되었는가
- AI가 수정해도 문맥이 유지되는가

### 배포 운영

- GitHub Actions가 정상 동작하는가
- Pages 배포 경로가 저장소명과 일치하는가
- 로컬 프리뷰와 실제 배포가 같은 구조를 따르는가

### 협업 운영

- 개인 작업본에서 수정하는가
- 수정 후 바로 commit / push 하는가
- 공용 PC 단일 작업본 운영을 피하고 있는가
- 웹 편집 사용자는 승인 흐름(PR/리뷰)을 따르는가
- 검색 인덱스 장애가 나도 원본 Markdown은 안전하게 남는가

---

## 3. 연결 문서

- 배포 가이드: [quartz-deployment](/knowledge-base/work/quartz-deployment/)
- 구현 관점: [development](/knowledge-base/work/development/)
- 고객 대응과 전달 포인트: [sales](/knowledge-base/work/sales/)
- 검색/적재 흐름: [knowledge-pipeline](/knowledge-base/work/knowledge-pipeline/)
- 웹 편집 계층: [decap-cms](/knowledge-base/work/decap-cms/)
- Claude Code 운영안: [claude-code-mcp](/knowledge-base/work/claude-code-mcp/)
- MCP 클라이언트 표준: [mcp-client-setup](/knowledge-base/work/mcp-client-setup/)
- Codex SDK 운영안: [codex-sdk-operations](/knowledge-base/work/codex-sdk-operations/)
