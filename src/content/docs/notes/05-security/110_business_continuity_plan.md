---
sidebar:
  order: 110
  label: "110. BCP 업무 연속성 계획 (Business Continuity Plan)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "BCP 업무 연속성 계획 (Business Continuity Plan)"
date: "2026-08-04T14:22:54+09:00"
tags:
  - "notes-security"
weight: 110
extra:
  question_no: "110"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "업무영향•연속전략•훈련을 묶는 독립 계획 주제임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **BCP(Business Continuity Plan)**: 중단 상황에서도 우선 업무를 최소 허용 수준으로 유지하고 목표 시간 안에 정상 수준으로 복귀하기 위한 업무 연속성 계획이다.
- **BCMS(Business Continuity Management System)**: 업무 영향 분석•연속성 전략•계획•훈련•성과평가•개선을 지속 운영하는 업무 연속성 관리체계이다.

</details>

- 정의/개념: **BCP** 는 중단 시 우선 업무를 유지하고 목표 시간 안에 복귀하기 위한 계획
- 배경/필요성: IT 재해복구만으로는 인력•시설•공급망 중단에 대한 **업무 연속성 확보가 어려움**

#### 한줄 요약

- 전산뿐 아니라 사람•장소•협력사까지 준비하는 계획이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **BIA(Business Impact Analysis)**: 업무 중단의 영향과 우선순위를 분석하는 활동이다.
- **MTPD(Maximum Tolerable Period of Disruption)**: 업무가 견딜 수 있는 최대 중단 기간이다.
- **RTO(Recovery Time Objective)**: 업무를 복구해야 하는 목표 시간이다.
- **RPO(Recovery Point Objective)**: 복구 시 허용하는 데이터 손실 시점이다.
- **훈련**: 계획의 발동•전환•복귀를 실제로 시험하는 활동이다.
- **지속 개선**: 훈련에서 발견한 공백에 따라 자원•절차를 보완하는 활동이다.

</details>

- BIA 기반 **우선 업무•복구 목표 도출**
- MTPD 내 **RTO•RPO•최소수준 설정**
- 훈련•경영검토 기반 **BCMS 지속 개선**

#### 한줄 요약

- 업무가 견딜 최대 시간보다 이르게 RTO를 정해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **연속성 전략**: 대체 인력•장소•기술•공급자와 최소 업무 수준을 조합하여 정해진 복구 목표를 달성하는 방식이다.
- **지휘 체계**: 계획 발동 권한과 역할을 정한 책임 구조이다.
- **소통 체계**: 연락망과 이해관계자 통지 절차이다.
- **복귀 기준**: 대체 상태에서 정상 운영으로 돌아갈 조건이다.

</details>

```mermaid
block-beta
  columns 3
  B["BIA•복구 목표"]
  S["업무 연속성 전략"]
  C["지휘•소통 체계"]
  P["BCP•DRP 실행계획"]
  T["훈련•성과평가•개선"]
  B --- S
  S --- C
  C --- P
  P --- T
  T --- B
```

| 구성요소 | 책임 |
|:---|:---|
| BIA•복구 목표 | **우선 업무•영향•MTPD•RTO** |
| 업무 연속성 전략 | **대체 인력•장소•기술•공급자** |
| 지휘•소통 체계 | **발동 권한•역할•연락망•통지** |
| BCP•DRP 실행계획 | **업무•IT 발동•운영•복귀 기준** |
| 훈련•성과평가•개선 | **목표 달성•계획 누락** 검증 |

#### 한줄 요약

- 중단 영향을 분석한 뒤 대체 자원과 실행 절차를 준비한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **BIA 기반 복구 목표**: 업무 중단 영향과 의존 자원을 근거로 MTPD보다 이른 RTO와 허용 가능한 RPO를 확정한 것이다.
- **발동•전환•복귀 훈련**: 비상 계획을 시작하고 대체 자원으로 업무를 운영한 뒤 정상 환경으로 안전하게 되돌리는 전 과정을 시험한다.

</details>

```mermaid
sequenceDiagram
  participant M as 경영진
  participant S as BIA•전략 담당
  participant O as 업무 조직
  participant A as 평가자
  M->>M: 1. BIA 범위•업무 우선순위 확정
  M->>S: 범위•우선순위 전달
  S->>S: 2. MTPD•RTO•RPO 설정
  S->>S: 3. 연속성 전략•계획 수립
  S->>O: 전략•계획 전달
  O->>O: 4. 발동•전환•복귀 훈련
  O->>A: 훈련 증적 전달
  A-->>M: 목표 달성•계획 공백
  M->>M: 5. 자원•계획 개선 결정
  M->>S: 개선 결정 전달
```

**동작 원리**

1. **BIA 범위•업무 우선순위 확정**: 분석 대상•영향 기준•책임자 지정
2. **MTPD•RTO•RPO 설정**: 허용 중단•복구 목표 확정
3. **연속성 전략•계획 수립**: 대체 자원•발동 기준 설계
4. **발동•전환•복귀 훈련**: 업무•IT•소통 절차 실행
5. **자원•계획 개선 결정**: 목표 미달 원인과 환경 변경사항 반영

#### 한줄 요약

- 훈련이 목표시간을 넘으면 전략과 자원을 다시 설계한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **DRP(Disaster Recovery Plan)**: BCP 안에서 정보시스템과 데이터를 복구하는 계획이다.
- **IT(Information Technology)**: 정보의 처리•저장•전송에 사용하는 기술이다.

</details>

| 계획 | 범위 | 상호 관계 |
|:---|:---|:---|
| **BCP** | **인력•시설•공급망•업무 전체의 지속•재개** | 업무 복구 목표와 우선순위를 DRP에 전달 |
| **DRP** | **IT 시스템•네트워크•데이터 복구** | BCP의 업무 목표를 기술 복구 절차로 구체화 |

#### 한줄 요약

- DRP는 BCP 안에서 IT와 데이터를 복구하는 계획이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **ISO(International Organization for Standardization)**: 국제표준화기구이다.
- **TS(Technical Specification)**: 국제표준 제정 전 기술 요구를 담은 기술시방서이다.
- **ISO 22301:2019**: BCMS 요구사항을 제공하는 국제표준이다.
- **ISO/TS 22317:2021**: 조직에 적합한 BIA 절차의 수립•유지 지침이다.
- **ITSCM(IT Service Continuity Management)**: IT 서비스의 연속성을 관리하는 활동이다.
- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **SP(Special Publication)**: NIST가 발행하는 전문 지침 문서이다.
- **NIST SP 800-34**: 정보시스템 비상계획 수립 지침이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **BCMS 요구사항** | **ISO 22301:2019 적용** | 연속성 체계 **인증** |
| **BIA 절차 품질** | **ISO/TS 22317:2021 참조** | **복구 목표 근거** 확보 |
| **IT 비상대응** | **NIST SP 800-34 Rev.1 참조** | **DRP•훈련** 구체화 |

#### 한줄 요약

- 업무 RTO와 IT 복구 순서를 연결해 실제 전환•복귀를 시험한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **훈련 기반 연속성 증명**: 계획서 보유가 아니라 실제 중단 훈련에서 최소 업무 수준•RTO•RPO•복귀 기준을 달성했음을 보여 주는 결과이다.

</details>

- 인력•시설•공급망은 **BCP**, IT•데이터 복구는 **DRP**, 목표는 BIA로 설정

#### 한줄 요약

- 계획서보다 목표 수준을 달성한 실제 훈련 결과가 중요하다.
