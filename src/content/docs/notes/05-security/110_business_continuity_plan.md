---
sidebar:
  order: 110
  label: "110. BCP 업무 연속성 계획 (Business Continuity Plan)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "BCP 업무 연속성 계획 (Business Continuity Plan)"
date: "2026-08-13T21:42:00+09:00"
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

<details><summary>용어 설명</summary>

- **업무 연속성 계획(Business Continuity Plan, BCP)**: 재해, 재난 발생 시 비즈니스 핵심 기능을 유지하고 복구하기 위한 방안 및 계획.
- **업무 연속성 관리체계(Business Continuity Management System, BCMS)**: 조직의 업무 연속성 전 과정을 기획, 수립, 운영, 평가, 개선하는 통합 체계.

</details>

- 정의/개념: **BCP**는 **BCMS** 안에서 중단 시 우선 업무를 유지하고 목표 시간 안에 복귀하기 위한 계획.
- 배경/필요성: IT 재해복구만으로는 인력•시설•공급망 중단까지 포괄하기 어려움.

#### 한줄 요약

- 전산뿐 아니라 사람•장소•협력사까지 준비하는 계획이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **업무 영향 분석(Business Impact Analysis, BIA)**: 재해 발생 시 업무 중단에 따른 영향을 평가하고 복구 우선순위를 설정하는 분석 활동.
- **최대 허용 중단 기간(Maximum Tolerable Period of Disruption, MTPD)**: 비즈니스가 치명적인 피해 없이 견딜 수 있는 최대 중단 한계 시간.
- **복구 시간 목표(Recovery Time Objective, RTO)**: 중단된 핵심 업무 및 IT 시스템을 재개해야 하는 목표 복구 시간.
- **복구 시점 목표(Recovery Point Objective, RPO)**: 재해 발생 시 허용되는 최대 데이터 손실 시점 또는 손실 범위.
- **훈련(Continuity Exercise and Testing)**: 수립된 BCP 절차의 실효성과 비상 대응 역량을 검증하기 위해 실시하는 평가 활동.
- **지속 개선(Continual Improvement)**: BCP 훈련 및 실제 재해 대응 결과를 분석하여 관리체계를 보완하는 활동.

</details>

- **BIA**로 우선 업무와 복구 목표 도출.
- **MTPD** 안에 **RTO**와 **RPO** 설정.
- **훈련** 결과를 **지속 개선**에 반영.

#### 한줄 요약

- 업무가 견딜 최대 시간보다 이르게 RTO를 정해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **연속성 전략(Continuity Strategy)**: 대체 사업장, 인력, 시스템 및 서드파티 조달을 통해 복구 목표를 달성하는 전략.
- **지휘 체계(Command Structure)**: 재난 발동 선언, 통제 및 비상 대응을 총괄하는 의사결정 책임 구조.
- **소통 체계(Communication System)**: 내부 임직원, 비상대응 조직, 고객 및 외부 관계기관에 통지하는 비상 연락 구조.
- **복귀 기준(Relocation and Return Criteria)**: 대체 운영 상태에서 정상 비즈니스 환경으로 복귀하기 위해 충족해야 하는 조건.

</details>

```text
BIA · 복구 목표
├─ 업무 연속성 전략
│  └─ 대체 인력 · 장소 · 기술 · 공급자
├─ 지휘 · 소통 체계
│  └─ 발동 권한 · 역할 · 연락망 · 통지
├─ BCP · DRP 실행계획
│  └─ 업무 · IT 발동 · 운영 · 복귀
└─ 훈련 · 성과평가 · 개선
   └─ 목표 달성 · 계획 누락 검증
```

| 구성요소 | 책임 |
|:---|:---|
| BIA•복구 목표 | **BIA**로 MTPD•RTO•RPO 도출 |
| 업무 연속성 전략 | **연속성 전략**으로 대체 인력•장소•기술•공급자 준비 |
| 지휘•소통 체계 | **지휘 체계**와 **소통 체계**로 발동•연락•통지 관리 |
| BCP•DRP 실행계획 | 업무•IT 발동•운영과 **복귀 기준** 적용 |
| 훈련•성과평가•개선 | **훈련**으로 목표 달성•계획 누락 검증 |

#### 한줄 요약

- 중단 영향을 분석한 뒤 대체 자원과 실행 절차를 준비한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BIA 기반 복구 목표(BIA-driven Recovery Targets)**: BIA 결과를 반영하여 MTPD 이내로 설정된 RTO 및 RPO 복구 지표.
- **발동•전환•복귀 훈련(Activation, Switch and Return Exercise)**: 비상계획 발동, 대체 인프라 전환 및 정상 복귀 전 과정을 시험하는 훈련.
- **BIA 범위•업무 우선순위 확정(BIA Scope and Business Priority)**: 핵심 비즈니스 프로세스와 지원 자산의 평가 범위를 확정하는 단계.
- **MTPD•RTO•RPO 설정(Recovery Time and Point Objective Setup)**: BIA 평가 결과를 바탕으로 핵심 업무의 복구 목표를 도출하는 단계.
- **연속성 전략•계획 수립(Strategy and Plan Formulation)**: 대체 사업장, 인력 및 기술 복구 계획을 구체화하는 단계.
- **발동•전환•복귀 훈련 단계(Exercise Execution Phase)**: 시나리오 기반 훈련을 실행하여 대응 절차의 실효성을 검증하는 단계.
- **자원•계획 개선 결정(Resource and Plan Improvement Decision)**: 훈련 평가 결과를 반영하여 자원 배치 및 연속성 계획을 보완하는 단계.

</details>

```text
1. BIA 범위•업무 우선순위 확정
               │
               ▼
2. MTPD•RTO•RPO 설정
               │
               ▼
3. 연속성 전략•계획 수립
               │
               ▼
4. 발동•전환•복귀 훈련
               │
       ┌───────┴───────┐
       │ 목표 달성     │ 목표 미달
       ▼               ▼
   계획 유지      5. 자원•계획 개선 결정
                        │
                        └─ 전략 · 계획 수립으로 환류
```

### 동작 원리

1. **BIA 범위·업무 우선순위 확정**: 대상·영향 기준 지정
2. **MTPD·RTO·RPO 설정**: 업무별 복구 목표 확정
3. **연속성 전략·계획 수립**: 대체 자원·발동 기준 설계
4. **발동·전환·복귀 훈련**: 업무·IT·소통 절차 실행
5. **자원·계획 개선 결정**: 목표 미달·환경 변화 반영

#### 한줄 요약

- 훈련이 목표시간을 넘으면 전략과 자원을 다시 설계한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **재해 복구 계획(Disaster Recovery Plan, DRP)**: BCP의 하위 계획으로 IT 인프라, 시스템, 데이터의 복구에 특화된 기술 계획.
- **정보기술(Information Technology, IT)**: 비즈니스 처리를 지원하는 컴퓨팅, 데이터베이스, 네트워크 등 기술 자산.

</details>

| 계획 | 범위 | 상호 관계 |
|:---|:---|:---|
| BCP | 인력•시설•공급망•업무 전체의 지속•재개 | 업무 복구 목표와 우선순위를 DRP에 전달 |
| DRP | **IT** 시스템•네트워크•데이터 복구 | BCP의 업무 목표를 기술 복구 절차로 구체화 |

#### 한줄 요약

- DRP는 BCP 안에서 IT와 데이터를 복구하는 계획이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ISO(International Organization for Standardization)**: 국제 표준을 개발•발행하는 국제 기구.
- **기술시방서(Technical Specification, TS)**: 표준 제정에 앞서 기술 표준화 지침을 제공하는 문서 규격.
- **ISO 22301:2019(BCMS Requirements, ISO 22301:2019)**: 업무 연속성 관리체계 수립 및 인증 기준을 제시하는 국제 표준.
- **ISO/TS 22317:2021(Guidance for BIA, ISO/TS 22317:2021)**: BIA 수행을 위한 가이드라인 및 프로세스를 규정한 국제 표준.
- **IT 서비스 연속성 관리(IT Service Continuity Management, ITSCM)**: IT 서비스의 중단 위험을 관리하고 BCP와 연계하여 복구력을 확보하는 체계.
- **미국 국립표준기술연구소(National Institute of Standards and Technology, NIST)**: 기술 및 보안 가이드를 발행하는 미국 정부 기관.
- **특별 간행물(Special Publication, SP)**: NIST에서 제작하여 발행하는 공식 기술 보고서 문서.
- **NIST SP 800-34(Contingency Planning Guide, NIST SP 800-34)**: IT 시스템 비상계획 수립 가이드를 제공하는 지침서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| BCMS 요구사항 | **ISO** **22301:2019** 적용 | 연속성 체계 인증 |
| BIA 절차 품질 | **TS**인 **ISO/TS 22317:2021** 참조 | 복구 목표 근거 확보 |
| **ITSCM** 비상대응 | **NIST** **SP** **800-34** 참조 | DRP•훈련 구체화 |

#### 한줄 요약

- 업무 RTO와 IT 복구 순서를 연결해 실제 전환•복귀를 시험한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **훈련 기반 연속성 증명(Exercise-based Continuity Demonstration)**: 실전 모의 훈련을 통해 복구 목표 달성 여부를 입증하는 결과.

</details>

- **훈련 기반 연속성 증명**을 위해 인력•시설•공급망은 **BCP**, IT•데이터 복구는 **DRP**, 목표는 **BIA**로 결정.

#### 한줄 요약

- 계획서보다 목표 수준을 달성한 실제 훈련 결과가 중요하다.
