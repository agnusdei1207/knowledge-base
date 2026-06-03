---
title: 🧪 R&D 허브
tags:
- r-and-d
---

연구개발 관련 실험, 검증, 아키텍처 메모를 연결하는 상위 문서입니다. R&D 과정에서 습득한 원천 기술 지식은 **[[study/_index|Study 허브]]**의 **[[study/studynote/_index|Study Note]]**와 융합하여 체계적으로 학습 및 검증을 이어갑니다.

관련 문서:
- [[r-and-d-roadmap]]
- [[tech-stack]]
- [[projects]]
- [[knowledgebase-decision-log]]
- [[study/_index|Study (학습 허브)]]

---

## 1. 목적

R&D 문서는 "연구 결과 보관소"가 아니라, 가설과 검증 결과를 반복적으로 쌓는 공간이어야 합니다.

이 문서의 목표는 다음과 같습니다.

- 어떤 기술 가설을 검증 중인지 공유
- 실패한 시도도 기록으로 남김
- 사업 문서와 연결 가능한 실험 결과를 축적

---

## 2. 현재 핵심 R&D 축

### A. 사내 검색 + RAG 품질 개선

- 목표: 메신저, 문서, 위키를 통합 질의 가능한 구조로 정리
- 관심사:
  - chunking 방식
  - 링크 기반 재랭킹
  - 문서 최신성 반영
- 연결 문서 & 학습 배경:
  - [[tech-stack]]
  - [[business-pipeline]]
  - **[[study/studynote/10_ai/_index|AI/LLM/RAG 이론 배경]]**
  - **[[study/studynote/05_database/_index|DB/Vector DB 구조]]**

### B. 지식그래프형 위키 운영

- 목표: 단순 문서 저장소가 아니라 관계 탐색형 지식 포털 운영
- 관심사:
  - 링크 밀도
  - 주제별 허브 문서 설계
  - AI 자동 문서 연결
- 연결 문서 & 학습 배경:
  - [[knowledgebase-decision-log]]
  - [[quartz-deployment]]
  - 개인용 위키 활용 테스트: **[[personal/_index|Personal Workspace]]**

### C. AI 에이전트 문서 작업 표준화

- 목표: Claude Code 같은 에이전트가 문서 구조를 망가뜨리지 않고 작업하도록 가이드화
- 관심사:
  - 링크 보존
  - 파일명 규칙
  - 사람 검토 지점 정의
- 관련 원칙:
  - **[[study/studynote/04_software_engineering/_index|소프트웨어 품질 및 형상관리론]]**

---

## 3. 실험 기록 원칙

- 가설을 먼저 쓴다
- 검증 방법을 적는다
- 결과보다 의사결정을 남긴다
- 실패도 남긴다

---

## 4. 다음 연결 문서

- 기술 로드맵: [[r-and-d-roadmap]]
- 기반 기술 정리: [[tech-stack]]
- 사업 연결 관점: [[business]]
- 기술사 스터디 노트: [[study/studynote/_index]]

