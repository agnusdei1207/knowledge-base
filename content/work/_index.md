+++
title = "Work (기업 업무 허브)"

[extra]
tags = ["work"]
+++

사내 모든 지식과 업무 정보가 수렴하는 비즈니스 인덱스 허브입니다.
업무는 5개 트랙(**Develop / R&D / 기획 / 디자인 / 사업**)으로 나뉘며, 각 트랙은 동등한 레벨에서 서로 연결됩니다.

---

## ⚡ 5개 트랙 빠른 바로가기

### 🧑‍💻 1. Develop (개발)
*   기술 아키텍처, 구현체, 사내 표준 기술 스택, 배포·운영 인프라가 정리되어 있습니다.
*   👉 [Develop 허브](/knowledge-base/work/develop/)

### 🔬 2. R&D (연구개발)
*   프로덕트 적용을 가정한 기술 실험·검증을 다룹니다. 순수 탐구는 상위 R&D 허브와 연결됩니다.
*   👉 [R&D 허브](/knowledge-base/work/research-and-development/)

### 🗂️ 3. 기획 (Planning)
*   진행 중 프로젝트, 로드맵, 마일스톤, 의사결정 흐름의 단일 현황판입니다.
*   👉 [기획 허브](/knowledge-base/work/planning/)

### 🎨 4. 디자인 (Design)
*   UX/UI 시스템, 디자인 산출물, 브랜드 가이드를 다루는 공간입니다.
*   👉 [디자인 허브](/knowledge-base/work/design/)

### 💼 5. 사업 (Business)
*   사업 파이프라인, 시장 진입 가설, 고객 문제 정의, 영업 포인트가 정리되어 있습니다.
*   👉 [사업 허브](/knowledge-base/work/business/)

---

## 🗺️ 트랙 간 관계

```
                    ┌──────────────┐
                    │  기획 (Plan)  │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
     ┌──────────┐    ┌──────────┐    ┌──────────┐
     │ 디자인    │    │ Develop  │    │   R&D    │
     └────┬─────┘    └────┬─────┘    └────┬─────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                   ┌──────────┐
                   │   사업    │
                   └──────────┘
```

- **기획**이 출발점이며, 결과물은 **디자인 / Develop / R&D**로 분기
- **사업**은 모든 트랙의 산출물이 고객 가치로 이어지는 연결점

---

## 🛠️ 트랙별 핵심 진입 문서 (바로가기)

### Develop
- [tech-stack](/knowledge-base/work/develop/tech-stack/) — 사내 표준 기술 스택
- [knowledge-pipeline](/knowledge-base/work/develop/knowledge-pipeline/) — 검색/적재 흐름
- [operations](/knowledge-base/work/develop/operations/) — 배포·협업 운영 기준
- [quartz-deployment](/knowledge-base/work/develop/quartz-deployment/) — Quartz 정적 사이트 배포
- [decap-cms](/knowledge-base/work/develop/decap-cms/) — 웹 마크다운 편집
- [tarball](/knowledge-base/work/develop/tarball/) — 압축 아카이브 기초

### Develop · AI/MCP 인프라
- [claude-code-mcp](/knowledge-base/work/develop/claude-code-mcp/) — Claude Code + MCP 운영안
- [mcp-client-setup](/knowledge-base/work/develop/mcp-client-setup/) — MCP 클라이언트 프로필 규격
- [codex-sdk-operations](/knowledge-base/work/develop/codex-sdk-operations/) — Python Codex SDK 자동화
- [knowledgebase-decision-log](/knowledge-base/work/develop/knowledgebase-decision-log/) — 이 구조를 선택한 의사결정 기록

### 기획
- [projects](/knowledge-base/work/planning/projects/) — 활성 프로젝트 목록

### 사업
- [business-pipeline](/knowledge-base/work/business/business-pipeline/) — 사업 파이프라인
- [go-to-market](/knowledge-base/work/business/go-to-market/) — 시장 진입 전략
- [sales](/knowledge-base/work/business/sales/) — 영업 포인트 / FAQ

---

> [!NOTE]
> 업무 문서를 편집하거나 추가할 때는 항상 [운영 원칙](/knowledge-base/work/develop/operations/) 및 [에이전트 규칙](../../AGENTS.md)을 준수해 주세요.
