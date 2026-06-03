---
title: knowledge-base
tags:
- general
---

## 지식 지도 (Workspace Map)

```mermaid
graph TD
    Hub["<span style='color:#F2ECE4'>종합 지식 포털</span>"]

    Hub --> Work["<span style='color:#F2ECE4'>기업 업무 허브</span><br/><span style='color:#D4CEC5;font-size:0.85em'>Work Workspace</span>"]
    Hub --> Personal["<span style='color:#F2ECE4'>개인 서재 & 로그</span><br/><span style='color:#D4CEC5;font-size:0.85em'>Personal Workspace</span>"]
    Hub --> Study["<span style='color:#F2ECE4'>일반 학습 허브</span><br/><span style='color:#D4CEC5;font-size:0.85em'>Study Workspace</span>"]
    Hub --> StudyNote["<span style='color:#F2ECE4'>기술사 스터디</span><br/><span style='color:#D4CEC5;font-size:0.85em'>Study Note Workspace</span>"]
    Hub --> RD["<span style='color:#F2ECE4'>연구 개발 허브</span><br/><span style='color:#A4B3A2;font-size:0.85em'>R&D Workspace</span>"]

    Work --> W1[사업 기획 & GTM]
    Work --> W2[프로젝트 & 태스크]
    Work --> W3[기술 아키텍처 & Ops]
    Work --> W4[에이전트 인프라]

    Personal --> P1[데일리 저널 일기]
    Personal --> P2[인생 목표 & 버킷]
    Personal --> P3[개인 자산 & 재정]
    Personal --> P4[취미 및 독서 기록]

    Study --> S1[학습 일지 및 아카이브]
    Study --> S2[학습 보조 자료]

    StudyNote --> SN1[기술사 16과목 노트]

    RD --> R1[R&D 가설 및 실험]
    RD --> R2[연구 개발 로드맵]
    RD --> R3[N-gram 링커 알고리즘]
    RD --> R4[Graph DB 비교 분석]

    style Hub fill:#191715,stroke:#A65B32,color:#F2ECE4
    style Work fill:#383228,stroke:#A65B32,color:#F2ECE4
    style Personal fill:#383228,stroke:#A65B32,color:#F2ECE4
    style Study fill:#383228,stroke:#A65B32,color:#F2ECE4
    style StudyNote fill:#383228,stroke:#A65B32,color:#F2ECE4
    style RD fill:#2D2A27,stroke:#73826F,color:#F2ECE4
```

---

## 5대 영역 바로가기

### **[[work/index|Work (기업 업무 허브)]]**
*   **목적:** 회사 비즈니스, 프로젝트 관리, 개발 스택 및 시스템 인프라 아키이빙.
*   **주요 문서:** `[[business|사업기획]]`, `[[projects|프로젝트현황]]`, `[[development|기술개발]]`, `[[operations|운영관리]]`, `[[sales|영업자료]]`.
*   **시스템 관리:** `[[claude-code-mcp|AI Ops]]`, `[[knowledge-pipeline|검색 파이프라인]]`, `[[decap-cms|CMS 가이드]]`.

### **[[personal/index|Personal (개인 서재 & 로그)]]**
*   **목적:** 지극히 개인적인 일상, 성장 기록, 취미, 재정 계획을 관리하는 안식처.
*   **주요 문서:** `[[journal|데일리저널]]`, `[[life-goals|인생목표]]`, `[[finances|자산플래너]]`, `[[hobby|취미&독서]]`.

### **[[study/index|Study (일반 학습 허브)]]**
*   **목적:** 일반적인 학습 일지 및 학습 보조 지식 보관소.
*   **주요 문서:** `[[tarball|tarball 아카이브]]`.

### **[[studynote/index|Study Note (기술사 스터디)]]**
*   **목적:** 정보통신기술사 및 컴퓨터응용시스템기술사 합격을 위한 16과목 심층 스터디 노트.
*   **주요 문서:** `[[studynote/index|기술사 16과목 목록]]`.

### **[[r-and-d/index|R&D (연구 개발 허브)]]**
*   **목적:** 검색, RAG, 문서 자동화, 에이전트 협업 등 **연구개발 가설과 실험**을 다루는 **쓰기 중심** 공간.
*   **주요 문서:** `[[r-and-d|R&D 가설 허브]]`, `[[r-and-d-roadmap|R&D 로드맵]]`, `[[n-gram-linker|N-gram 링커]]`, `[[graph-databases|Graph DB 비교]]`.

---

## 아이디어 보관함 (Inbox)

어디로 분류해야 할지 모르는 임시 메모, 갑자기 떠오른 비즈니스 아이디어, 오늘 배운 팁 등은 우선 **[[inbox|아이디어 보관함]]**에 자유롭게 던져 두세요.
정기적으로 이 공간을 비우며 적절한 카테고리(Work, Personal, Study, StudyNote, R&D)로 이동시키면 지식베이스의 신선함이 유지됩니다.

---

> [!TIP]
> **단축키 활용하기**
> - `Ctrl + P`를 누르면 문서 이름으로 빠르게 이동할 수 있습니다.
> - 새로운 문서를 만들고 연결하려면 대괄호 두 개 ``을 본문에 적어세요.
> - Quartz 웹 포털에서 제공하는 연결성 그래프를 통해 내 지식들이 어떻게 연결되어 가고 있는지 한눈에 관찰할 수 있습니다.
