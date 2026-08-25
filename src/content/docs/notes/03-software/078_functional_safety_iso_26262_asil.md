---
sidebar:
  order: 78
  label: "078. 기능 안전 ISO 26262•ASIL"
  badge:
    text: "기출 · 50%"
    variant: note
title: "기능 안전 ISO 26262•ASIL (Functional Safety ISO 26262)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 78
extra:
  question_no: "078"
  source_status: "기출"
  source_history: "134회"
  priority: 50
  priority_note: "134회 기출, ASIL 등급•안전수명주기 중요"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ISO 26262**: 자동차 전기/전자(E/E) 시스템의 오작동으로 인한 사고를 방지하기 위해 제정된 국제 기능안전 표준.
- **ASIL(Automotive Safety Integrity Level)**: HARA 위험원 분석을 통해 결정되는 자동차 안전 무결성 등급 (QM, ASIL A, B, C, D).

</details>

- 정의/개념: 차량용 전기·전자 시스템의 고장 위험을 방지하기 위해 **HARA 3요소(S/E/C)로 ASIL(A~D) 등급을 부여**하고 전 수명주기를 통제하는 국제 기능안전 표준
- 배경/필요성: 차량 전장화 및 자율주행 확대로 인한 **소프트웨어 오작동 시 차량 제어 상실 및 인명 참사 해결 불가**

#### 한줄 요약
- HARA 위험 분석을 통해 ASIL 등급을 도출하고 V-Model 전 수명주기 동안 기능안전을 검증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **HARA 3요소(S, E, C)**: 심각도(Severity, S0~S3), 노출빈도(Exposure, E0~E4), 제어가능성(Controllability, C0~C3).
- **MC/DC(Modified Condition/Decision Coverage)**: 복합 조건식에서 각 개별 조건이 다른 조건과 무관하게 전체 결과에 독립적으로 영향을 미침을 입증하는 최고 수준 커버리지.

</details>

- 차량 E/E 시스템의 전 수명주기를 규정한 **12개 Part 구성의 V-Model 안전 프로세스**
- 위험원 분석(HARA)을 통한 **4단계 ASIL(A, B, C, D) 등급별 차등적 엔지니어링 통제**
- 최고 위험 등급인 ASIL D에 대한 **MC/DC 커버리지 및 MISRA-C 정적 분석 강제**

#### 한줄 요약
- HARA 3요소로 안전 등급을 산정하고, 양방향 추적성과 등급별 검증 기법으로 오작동을 방지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ASIL Decomposition(분해)**: ASIL D 요구사항을 독립적인 두 개의 ASIL B(D) 서브시스템으로 이중화 분해하여 개발 난이도를 낮추는 기법.

</details>

```text
[ISO 26262 HARA 및 ASIL 등급 결정 체계]
|-- HARA 3대 평가 인자 매트릭스 결합
|   |-- 심각도 (Severity: S0 부상없음 ~ S3 사망/생명위협)
|   |-- 노출빈도 (Exposure: E0 극히낮음 ~ E4 상시노출)
|   `-- 통제성 (Controllability: C0 통제가능 ~ C3 회피불가)
`-- ASIL 안전 무결성 등급 판정 결과
    |-- QM (Quality Management: 일반 품질 관리 적용)
    |-- ASIL A / B (중저위험 전장 부품)
    `-- ASIL C / D (조향, 제동, 에어백, 자율주행 등 최고위험 부품)
```

선의 의미: 계층 및 3대 인자 매트릭스 결합을 통한 ASIL 등급 도출 구조

| 구성요소 | 핵심 정의 및 평가 기준 |
|:---|:---|
| **심각도 (Severity, S)** | 시스템 오작동 발생 시 탑승자/보행자의 **신체 상해 및 치사율 수준 (S0~S3)** |
| **노출빈도 (Exposure, E)**| 위험을 유발할 수 있는 특정 주행 조건(고속도로, 빗길)의 **발생 시간 비율 (E0~E4)** |
| **통제성 (Controllability, C)**| 고장 발생 시 운전자 또는 주변 차량이 **사고를 회피할 수 있는 통제력 (C0~C3)** |
| **ASIL 등급 (QM, A~D)** | **매트릭스 결합 결과에 따른 SW 설계, 코딩, 테스트의 법적 차등 적용선** |

#### 한줄 요약
- S, E, C 3요소의 정량 평가를 통해 ASIL 등급을 확정하고 수준별 안전 요구사항을 도출한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ISO 26262 Part 6**: V-Model에 기반하여 자동차 임베디드 소프트웨어의 설계, 구현, 단위/통합 테스트를 다루는 소프트웨어 기능안전 규격.

</details>

```text
1. 차량 아이템 정의(Item Definition) 및 HARA 위험 분석 수행 -> Safety Goal (ASIL D) 도출
        │
   2. 기능안전요구사항(FSR) -> 기술안전요구사항(TSR) -> SW 안전요구사항(SSR) 계층화
        │
   3. SW 안전 아키텍처 설계 (메모리 파티셔닝 MPU, 워치독 타이머, 이중화 설계)
        │
   4. MISRA-C 표준 준수 코딩 및 단위 테스트 (ASIL D: MC/DC 커버리지 100% 달성)
        │
   5. HIL(Hardware-in-the-Loop) 시뮬레이션 기반 결함 주입(Fault Injection) 통합 테스트
        │
   6. Safety Case 안전성 보고서 작성 및 TÜV SÜD 공인 인증 획득
```

#### 한줄 요약
- Safety Goal → SSR 명세 → 아키텍처 설계 → MISRA 코딩 → MC/DC 검증 → HIL 실차 시험 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **QM vs ASIL A~D**: 비안전 일반 품질관리(QM)와 위해도에 따라 엄격한 검증을 요구하는 ASIL A~D 비교.

</details>

| 비교 항목 | QM (Quality Management) | ASIL A / B | ASIL C / D (최고 등급) |
|:---|:---|:---|:---|
| 주 적용 대상 | **내비게이션, 인포테인먼트, 오디오** | 계기판 표시등, 헤드라이트 | **전자식 조향(EPS), 브레이크(ABS), ADAS** |
| 필수 코딩 규칙 | 표준 사내 코딩 가이드 | MISRA-C 권고 | **MISRA-C / AUTOSAR C++ 필수 강제** |
| 구조적 커버리지 | 구문(Statement) 커버리지 | 분기(Branch) 커버리지 | **MC/DC (Modified Condition) 100% 필수** |
| 정적 분석 및 리뷰 | 개발자 자체 리뷰 | 동료 검토 (Walkthrough) | **독립된 제3자 정밀 Fagan Inspection** |

#### 한줄 요약
- 비안전 전장은 QM, 일반 전장은 ASIL A/B, 인명 직결 조향/제동 제어는 ASIL C/D를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SOTIF(ISO 21448)**: 전장 하드웨어 고장이 없더라도 센서(카메라, 라이다)의 인지 한계(역광, 안개)로 인해 사고가 발생하는 자율주행 의도된 기능안전 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전체 제어기를 ASIL D로 개발 시 막대한 비용/일정 지연 | **ASIL Decomposition(D $\to$ B(D)+B(D)) 독립 이중화 분해** | 개발 공수 40% 절감 및 안전 무결성 동시 달성 |
| 자율주행 센서 인지 한계(역광/폭우)로 인한 오작동 | **ISO 26262와 ISO 21448 SOTIF(의도된 기능안전) 표준 병행** | 무고장 상황의 환경적 인지 한계 사고 원천 예방 |
| 복잡한 C++ 코드의 미정의 동작(Undefined Behavior) | **MISRA-C:2023 준수 및 동적 메모리 할당(malloc) 전면 금지** | 런타임 메모리 누수 및 세그멘테이션 폴트 0화 |
| 양방향 추적성(Traceability) 누락으로 인증 실패 | **Polarion / Jira 기반 요구사항-코드-테스트 1:1 자동 추적** | TÜV 등 국제 공인 인증 통과 보장 |

#### 한줄 요약
- ASIL 분해, SOTIF 결합, 동적 메모리 금지, ALM 추적성 도구로 기능안전을 확보한다.

## Ⅶ. 결론

- SDV(Software Defined Vehicle) 및 자율주행 시대의 안전성을 확보하기 위해 **ISO 26262 V-Model과 ASIL D 엔지니어링 프로세스를 필수 준수**하고, **SOTIF 및 AUTOSAR Adaptive 플랫폼과 융합**하여 차량 무결성 완성

#### 한줄 요약
- ISO 26262는 HARA 위험 분석을 기반으로 차량 전장 소프트웨어의 고장을 방지하고 생명을 보호하는 자동차 기능안전의 절대 표준이다.