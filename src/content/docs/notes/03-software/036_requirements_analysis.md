---
sidebar:
  order: 36
  label: "036. 요구사항 분석•명세 (Requirements Analysis)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "요구사항 분석•명세 (Requirements Analysis)"
date: "2026-08-13T14:34:00+09:00"
tags:
  - "notes-software"
weight: 36
extra:
  question_no: "036"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "요구사항 도출•검증•추적은 상위 관리 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Requirements Engineering (요구공학)**: 소프트웨어 시스템이 제공해야 하는 기능(Functional) 및 비기능(Non-Functional) 요구사항을 도출, 분석, 명세, 검증 및 관리(Traceability)하는 체계적 공학 프로세스.
- **SRS (Software Requirements Specification)**: 고객과 개발팀 간의 공식 계약적 요구사항 문서로, 기능/비기능 요구와 수용 기준(Acceptance Criteria)을 완결 명확하게 기술한 산출물.

</details>

- 정의/개념: 고객 및 이해관계자의 불명확한 니즈(Needs)를 도출하고 정제하여 모호성 없는 명세서(SRS)로 정립하는 공학적 방법론인 **Requirements Analysis & Specification (요구사항 분석 및 명세)**
- 배경/필요성: 모호한 요구는 후반 검증에서 **재작업•수용 분쟁** 유발

#### 한줄 요약

- 목표•제약을 검증 가능한 요구사항으로 정제하는 요구공학이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Acceptance Criteria (수용 기준)**: 요구사항이 성공적으로 구현되었는지 여부를 객관적으로 테스트하고 검증(Verification)할 수 있는 명확한 조건.
- **RTM (Requirements Traceability Matrix)**: 요구사항 ID부터 아키텍처, 소스코드, 테스트 케이스까지 양방향 추적성을 시각화한 매트릭스 표.

</details>

- **ISO/IEC/IEEE 29148** 기반 요구사항 품질•명세 구조 적용
- 비기능 요구사항(성능, 보안, 가용성)의 측정 가능한 **Acceptance Criteria (수용 기준)** 정량화
- **RTM (Requirements Traceability Matrix)** 기반 양방향 추적성 보장

#### 한줄 요약

- 완전성, 일관성, 수용 기준, 양방향 추적성으로 요구 품질을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Functional vs Non-Functional Requirements**: 기능 요구사항은 시스템이 구체적으로 무슨 동작을 해야 하는지(What to do), 비기능 요구사항은 어느 정도의 성능/보안/품질로 수행되어야 하는지(How well)를 의미.

</details>

```text
          [요구 저장소]
                 |
            [분석 모델]
                 |
            [요구 명세]
                 |
          [추적 매트릭스]
```

선의 의미: 요구사항 도출 결과가 분석 모델(Use Case/DFD)로 구체화된 후 SRS 명세서로 공식화되고 RTM 추적 매트릭스로 바인딩되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 요구 저장소 | 출처•상태•우선순위와 변경 이력 보존 |
| 분석 모델 | Use Case•DFD 등으로 경계와 상호작용 정제 |
| 요구 명세 | 기능•비기능 요구와 **수용 기준** 공식화 |
| 추적 매트릭스 | 요구•설계•코드•테스트의 **RTM** 연결 유지 |

#### 한줄 요약

- 요구 저장소, 분석 모델, 요구 명세, 추적 매트릭스가 요구 정보를 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Requirements Baseline (요구사항 기준선)**: 개발 팀과 이해관계자가 공식 승인하여 향후 변경 통제(CCB)의 기준이 되는 정적 소프트웨어 요구사항 버전.

</details>

```text
┌──────────────────────────────┐
│ 이해관계자 목표•제약       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 요구 도출 (Elicitation)   │
│ 2. 요구 분석 (Analysis)      │
│ 3. 요구 명세 (Specification) │
│ 4. 검토•기준선 승인 (Baseline)│
│ 5. 영향 분석•변경 반영 (CCB) │
└──────────────┬───────────────┘
               ▼
       [추적 관계 최신화]
```

### 동작 원리

1. 요구 도출: 인터뷰 및 Workshop을 통한 사용자 요구사항 추출.
2. 요구 분석: Use Case 및 DFD 모델링을 통한 요구사항의 모호성/충돌 조율.
3. 요구 명세: 정량적 **Acceptance Criteria** 및 비기능 SLO/SLA를 기재한 SRS 작성.
4. 검토·기준선 승인: Inspection 검증을 통한 **Requirements Baseline** 설정.
5. 영향 분석·변경 반영: 신규 요구 변경 요청 시 **CCB (Change Control Board)** 영향 분석 통제.

#### 한줄 요약

- 요구 도출부터 영향 분석•변경 반영까지의 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Structured Analysis vs Object-Oriented Analysis**: 구조적 분석은 DFD(Data Flow Diagram) 중심의 데이터 흐름 처리, 객체지향 분석은 UML Use Case/Class Diagram 중심의 객체 메세지 상호작용 처리.

</details>

| 비교 항목 | 기능 요구사항 (Functional) | 비기능 요구사항 (Non-Functional) |
|:---|:---|:---|
| 관점 및 범위 | 시스템이 무엇(What)을 수행해야 하는가 | 시스템의 품질(How Well) 및 기술 제약 |
| 측정 및 검증 | 시나리오•상태•결과로 판정 | 성능•보안•가용성 지표와 조건으로 판정 |
| 대표적 사례 | 회원 가입, 계좌 이체, 결제 승인 기능 | "응답시간 99.9% 1초 이내", "AES-256 암호화 적용" |

#### 한줄 요약

- 모호성 정제는 요구사항 분석, 합의 기준선은 요구사항 명세가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Ambiguity (모호성)**: "시스템은 매우 빨라야 한다"처럼 해석이 사람마다 달라 분쟁을 유발하는 나쁜 요구사항 작성 패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 주관적 형용사 사용으로 인한 요구사항 **Ambiguity** 심화 | "빠르게 처리" $\to$ **"평균 500ms 이내 처리"** 로 정량화 | 검증 정확도 대폭 향상 |
| 요구사항 산출물과 실제 구현 코드 간의 불일치 | **RTM (Requirements Traceability Matrix)** 자동화 수립 | 양방향 추적성 보장 |
| 개발 중 무분별한 요구사항 추가 (Scope Creep) | **CCB (변경통제위원회)** 공식 운영 및 비용/일정 재산정 | 프로젝트 파행 방지 |

> 사례: 공공 SI 사업 내 **ISO/IEC/IEEE 29148** 표준 기반 SRS 작성 및 RTM 수립

#### 한줄 요약

- 품질 지표, 결정 권한자, 규제 요구의 추적성을 확보한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **요구공학 체계 수립 기준(Requirements Engineering Standards)**: 프로젝트 규모, 규제 수준(Compliance) 및 수용 검증 자동화 환경에 기반한 선정 체계.

</details>

- **요구공학 체계 수립 기준**에 따라 명확한 사업 범위 통제를 위해 **SRS 정량화 + RTM 추적성 관리** 인가

#### 한줄 요약

- 모호성•합의 상태•변경 영향을 함께 평가하는 것이 핵심이다.
