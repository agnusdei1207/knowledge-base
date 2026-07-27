---
sidebar:
  order: 38
  label: "038. NIST AI RMF AI 위험 관리 프레임워크 (NIST AI RMF)"
  badge:
    text: "미출제 · 50%"
    variant: note
title: "NIST AI RMF AI 위험 관리 프레임워크 (NIST AI RMF)"
date: "2026-07-25T01:35:00+09:00"
tags:
  - "notes-law-policy"
weight: 38
extra:
  question_no: "038"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "AI 위험의 Govern·Map·Measure·Manage 핵심"
---

## 미리 알고가기

- **인공지능 위험 관리 프레임워크(AI Risk Management Framework, AI RMF)**: AI 시스템의 위험을 관리하고 신뢰성을 높이기 위한 자율 프레임워크
- **미국 국립표준기술연구소(National Institute of Standards and Technology, NIST)**: 측정·표준·기술 지침을 연구·개발하는 미국 정부기관
- **시험·평가·검증·확인(Testing, Evaluation, Verification, and Validation, TEVV)**: AI가 설계 요구와 실제 사용 목적을 충족하는지 여러 증거로 확인하는 활동
- **AI RMF 프로필(AI RMF Profile)**: 특정 사용 용도나 산업 부문에 맞추어 AI RMF의 성과를 구체화한 적용 가이드라인
- **AI RMF 플레이북(AI RMF Playbook)**: AI RMF의 4대 기능을 조직에 실제로 적용할 수 있도록 돕는 구체적인 실행 계획서
- **신뢰성 특성**: 유효·신뢰, 안전, 보안·복원력, 책임·투명성, 설명·해석, 개인정보 보호, 유해 편향 관리 공정성
- **AI 행위자(AI Actor)**: AI의 설계·개발·배포·운영·평가·영향을 맡거나 받는 개인·조직
- **영향받는 공동체**: AI의 결과로 권리·기회·안전·생활에 영향을 받는 개인과 집단
- **위험 허용수준(Risk Tolerance)**: 조직이 목표 달성을 위해 받아들일 수 있다고 승인한 AI 위험의 범위
- **생성형 AI 프로필(Generative AI Profile)**: 생성형 AI 고유 위험에 AI RMF 결과와 권장 행동을 적용한 NIST 프로필
- **ISO/IEC 42001**: 조직의 AI 경영시스템 구축·운영·개선 요구사항을 규정한 국제표준

## Ⅰ. 개요

- 정의/개념: AI 위험을 맥락별로 관리하는 자발적 프레임
- **배경/필요성**: 기술 성능과 사람·조직·사회 영향을 함께 통제

### 쉽게 이해하기 (학습용)
- 같은 AI라도 쓰는 사람과 장소에 따라 피해가 달라지므로 사용 맥락부터 위험을 찾고 재서 대응하게 함

## Ⅱ. 특징

- 자발적·권리 보존·산업 중립적 틀을 제공한다.
- Govern이 Map·Measure·Manage를 관통한다.
- 위험·신뢰성 상충과 불확실성을 기록한다.
- 기능은 체크리스트나 고정 순서가 아니다.

### 쉽게 이해하기 (학습용)
- 정확도를 높이는 선택이 설명 가능성이나 공정성을 낮출 수 있어 어떤 위험을 왜 받아들였는지 기록함

## Ⅲ. 아키텍처 및 구성요소

```mermaid
flowchart LR
    G[Govern] -. 정책·책임·문화 .-> M[Map]
    G -. 정책·책임·문화 .-> E[Measure]
    G -. 정책·책임·문화 .-> A[Manage]
    M --> E --> A
    A -. 감시·교훈 .-> M
```

| 설계 요소 | 설명 |
|:---|:---|
| Govern | 정책·책임·문화·위험 허용수준 |
| Map | 맥락·행위자·영향·위험 식별 |
| Measure | TEVV·지표·불확실성·추적 |
| Manage | 위험 우선순위·처리·감시·소통 |

### 쉽게 이해하기 (학습용)
- Govern은 전체에 규칙을 주고 Map의 맥락이 Measure의 지표를 정하며 Manage 결과가 다시 맥락으로 돌아감

## Ⅳ. 원리 및 절차 흐름도

```mermaid
sequenceDiagram
    participant G as AI 거버넌스
    participant T as AI 팀
    participant S as 영향받는 공동체
    G->>T: Govern
    T->>S: Map
    S-->>T: Measure
    T->>G: Manage
    G-->>T: 재평가
```

| 절차 | 설명 |
|:---|:---|
| Govern | 정책·역할·허용수준·문서 체계화 |
| Map | 목적·맥락·행위자·긍정·부정 영향 파악 |
| Measure | TEVV로 위험·신뢰성·불확실성 평가 |
| Manage | 위험 우선화와 배포·완화·중단 결정 |
| 재평가 | 운영 변화·사고·새 영향으로 반복 |

### 쉽게 이해하기 (학습용)
- 누구에게 어떤 피해가 생길지 Map에서 놓치면 Measure는 잘못된 지표를 정확히 계산하게 됨

## Ⅴ. 종류 및 비교

| 판단 기준 | NIST AI RMF | ISO/IEC 42001 |
|:---|:---|:---|
| 핵심 특징 | 위험 결과·행동의 자발적 프레임 | AIMS 요구사항과 선택적 인증 |
| 적용 기준 | 사용사례별 위험 실무를 설계할 때 | 조직 AI 관리체계를 표준화할 때 |
| 주요 위험 | 법적 준수·인증을 직접 증명 못 함 | 인증 범위 밖 시스템 위험을 놓침 |

### 쉽게 이해하기 (학습용)
- RMF는 사용사례 위험을 다루는 실무 틀이고 42001은 조직의 반복 관리체계 요구사항임

## Ⅵ. 실무 사례

1. 의료 AI는 **불확실성**으로 자동 판정·인간 검토 결정

### 쉽게 이해하기 (학습용)
- 신뢰도가 낮은 진단은 자동 확정하지 않고 의사 검토로 보내며 성능이 변하면 전환 기준을 다시 평가한다.

## Ⅶ. 결론

- 맥락·TEVV·허용수준으로 AI 배포 결정

### 쉽게 이해하기 (학습용)
- 위험 목록을 만드는 데서 끝내지 않고 측정 결과를 배포·완화·중단 결정으로 연결해야 함
