+++
title = "R&D (연구 개발 허브)"

[extra]
tags = ["research-and-development"]
+++

검색, RAG, 문서 자동화, 에이전트 협업 등 <strong>연구개발 가설과 실험</strong>을 다루는 공간입니다.
R&D 과정에서 습득한 원천 기술 지식은 <strong>Study 허브</strong>의 <strong>Study Note</strong>와 융합하여 체계적으로 학습 및 검증을 이어갑니다.

스터디 노트와 달리 <strong>빈번한 쓰기와 반복적 갱신</strong>이 발생하므로 Study와 분리 운영합니다.

---

## 1. 목적

R&D 문서는 "연구 결과 보관소"가 아니라, 가설과 검증 결과를 반복적으로 쌓는 공간이어야 합니다.

- 어떤 기술 가설을 검증 중인지 공유
- 실패한 시도도 기록으로 남김
- 사업 문서와 연결 가능한 실험 결과를 축적

---

## 2. 현재 핵심 R&D 축 & 연구 영역

### A. 사내 검색 + RAG 품질 개선
- 목표: 메신저, 문서, 위키를 통합 질의 가능한 구조로 정리
- 관심사: chunking 방식, 링크 기반 재랭킹, 문서 최신성 반영
- 연결 문서 & 학습 배경:
  - [tech-stack](/knowledge-base/work/develop/tech-stack/)
  - [business-pipeline](/knowledge-base/work/business/business-pipeline/)
  - **AI/LLM/RAG 이론 배경**
  - **DB/Vector DB 구조**

### B. 지식그래프형 위키 운영
- 목표: 단순 문서 저장소가 아니라 관계 탐색형 지식 포털 운영
- 관심사: 링크 밀도, 주제별 허브 문서 설계, AI 자동 문서 연결
- 연결 문서 & 학습 배경:
  - [knowledgebase-decision-log](/knowledge-base/work/develop/knowledgebase-decision-log/)
  - [quartz-deployment](/knowledge-base/work/develop/quartz-deployment/)
  - 개인용 위키 테스트: **Personal Workspace**

### C. AI 에이전트 문서 작업 표준화
- 목표: Claude Code 같은 에이전트가 문서 구조를 망가뜨리지 않고 작업하도록 가이드화
- 관심사: 링크 보존, 파일명 규칙, 사람 검토 지점 정의
- 관련 원칙: **소프트웨어 품질 및 형상관리론**

### D. 주요 연구개발 프로젝트
*   <strong><a href="/knowledge-base/research-and-development/quartz-architecture/">Quartz v5 아키텍처 분석</a></strong>: 백링크·그래프 뷰 개념 구분, 빌드 파이프라인, 강점/한계, 타 SSG 비교, 스케일 전략.
*   <strong><a href="/knowledge-base/research-and-development/research-and-development-roadmap/">research-and-development-roadmap</a></strong>: 연구 개발 로드맵 및 핵심 아젠다.
*   <strong><a href="/knowledge-base/research-and-development/n-gram-linker/">N-gram 해시 링커 알고리즘</a></strong>: 9,400개 스터디 노트를 백트래킹 없이 초고속으로 상호 연결한 링커 구조 설명.
*   <strong><a href="/knowledge-base/research-and-development/graph-databases/">Neo4j vs Dgraph 기술 비교</a></strong>: 그래프 데이터베이스의 아키텍처 및 Graph RAG 분산 확장 전략 비교 분석.

---

## 3. 실험 기록 원칙

- 가설을 먼저 쓴다
- 검증 방법을 적는다
- 결과보다 의사결정을 남긴다
- 실패도 남긴다

---

## 4. 다음 연결 문서

- 기술 로드맵: [research-and-development-roadmap](/knowledge-base/research-and-development/research-and-development-roadmap/)
- 기반 기술 정리: [tech-stack](/knowledge-base/work/develop/tech-stack/)
- 사업 연결 관점: [business](/knowledge-base/work/business/business/)
- 기술사 스터디 노트: index

---

> [!TIP]
> R&D 실험 중 새로운 개념이 정립되면 Study의 해당 과목 노트로 옮기고, 여기에는 요약만 남기세요.
