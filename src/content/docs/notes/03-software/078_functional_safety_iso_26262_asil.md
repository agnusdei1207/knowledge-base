---
sidebar:
  order: 78
  label: "078. 기능 안전 ISO 26262•ASIL (Functional Safety ISO 26262)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "기능 안전 ISO 26262•ASIL (Functional Safety ISO 26262)"
date: "2026-08-13T18:02:00+09:00"
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

- **ISO 26262 (차량 기능 안전 국제 표준)**: 자동차에 탑재되는 전기/전자(E/E: Electrical/Electronic) 시스템의 고장으로 인한 인명 사고 위험을 방지하기 위해, 개발 전 수명주기(V-Model) 동안 정립해야 할 국제 기능 안전(Functional Safety) 표준.
- **ASIL (Automotive Safety Integrity Level, 자동차 안전 무결성 수준)**: ISO 26262의 핵심 평가 지표로, 위험원 분석(HARA)을 통해 위험도를 ASIL A(최저)부터 ASIL D(최고 위험)까지 4단계로 등급화한 무결성 수준.
- **HARA (Hazard Analysis and Risk Assessment)**: 차량의 주행 오동작으로 인한 위해 요소(Hazard)를 식별하고 위험도를 정량화하는 프로세스.

- **자동차 기능안전성(ISO 26262 / ASIL)**: 차량용 전기·전자 시스템의 고장으로 인한 위험을 방지하기 위해 심각도(Severity), 노출도(Exposure), 통제성(Controllability)을 결합하여 안전성 요구등급(ASIL A~D)을 정의한 국제 표준.
</details>

- 정의/개념: 승용차 및 상용차 E/E 시스템의 고장으로 발생할 수 있는 사고 위험을 방지하고자 HARA를 통해 ASIL(A~D) 등급을 부여하고 개발 전 수명주기(Safety Lifecycle)를 통제하는 기능 안전 표준인 **ISO 26262**
- 배경/필요성: E/E 오동작은 **차량 통제 상실•인명 위해** 유발

#### 한줄 요약

- 국제표준화기구의 ISO 26262에 따른 위험 등급 기반 기능 안전 통제가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **3-Factor ASIL Determination**: 심각도(Severity, S0~S3), 노출 빈도(Exposure, E0~E4), 제어 가능성(Controllability, C0~C3) 3가지 요소를 조합하여 ASIL 등급 도출.
- **Bi-directional Traceability (양방향 추적성)**: Safety Goal에서 출발하여 SW 요구사항(SSR), 소스코드, 단윗/통합 테스트 케이스까지 양방향으로 추적 가능해야 하는 속성.

</details>

- **Product Safety Lifecycle (전 수명주기 V-Model 통제: 12개 Part 구성)**
- **HARA (위험원 분석)** 기반 **ASIL (A / B / C / D)** 등급별 차등적 품질 프랙티스 적용
- 하드웨어 무결성 평가 (**FMEDA, SPFM, LFM**) 및 소프트웨어 단위/통합 테스트 독립성 강제

#### 한줄 요약

- 세 위험 축에 따른 자동차 안전 무결성 수준과 검증 엄격도가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ASIL Decomposition (ASIL 분해)**: 최고 등급인 ASIL D 요구사항을 독립적인 하드웨어/소프트웨어 아키텍처 다중화(Redundancy)를 통해 ASIL B(D) + ASIL B(D) 형태로 분해하여 개발 부담을 완화하는 기법.

</details>

```text
[HARA (Hazard Analysis & Risk Assessment)]
                 │
                 ▼ (S, E, C 평가 조합)
┌────────────────────────────────────────────────────────┐
│  Severity (S0~S3)  ×  Exposure (E0~E4)  ×  Controllability (C0~C3) │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ ASIL A (최저 위험) ──► ASIL B ──► ASIL C ──► ASIL D (최고 위험) │
│ (※ 위험도가 매우 미미할 경우 QM: Quality Management 처리)      │
└────────────────────────────────────────────────────────┘
```

선의 의미: HARA 프로세스가 심각도(S), 노출 빈도(E), 제어 가능성(C)을 평가하여 QM 또는 ASIL A~D 등급을 부여하는 체계.

| ASIL 평가 3요소 | 인자 명칭 | 단계별 평가 기준 |
|:---|:---|:---|
| Severity (심각도) | **S0 ~ S3 (S3: 사망 가능성)** | 사고 발생 시 승객/운전자가 입게 되는 상해 또는 사망의 피해 정도 |
| Exposure (노출 빈도) | **E0 ~ E4 (E4: 매일 발생)** | 위험 상황(주행 고속도로, 우천 등)이 운전 중 발생하는 시간적 빈도 |
| Controllability (제어성) | **C0 ~ C3 (C3: 통제 불능)** | 운전자가 오동작 발생 시 핸들/브레이크로 사고를 피할 수 있는 통제력 |

#### 한줄 요약

- 위험원 분석 및 위험 평가부터 차량•기능•기술•구현 요구로 이어지는 계층이 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MISRA-C / CERT-C**: ISO 26262 Part 6에서 ASIL C/D 등급 소프트웨어 작성 시 필수 적용하도록 강제하는 안전 코딩 컨벤션 규칙.

</details>

```text
  [Safety Goals 도출] ─────────────────────────────► [Safety Validation]
          │                                                  ▲
          ▼                                                  │
  [SW Safety Req (SSR)] ────────────────────────────► [SW Integration Test]
          │                                                  ▲
          ▼                                                  │
  [SW Architecture Design] ─────────────────────────► [SW Unit Test]
          │                                                  ▲
          └──────────────► [SW Coding (MISRA-C)] ────────────┘
```

### 동작 원리

1. HARA•안전 목표 도출: 위험 상황과 ASIL 등급 결정.
2. 안전 요구 분해: 차량•기능•기술•SW 요구로 추적 연결.
3. 아키텍처**•**구현: 등급별 안전 기법과 코딩 지침 적용.
4. 검증**•**확인: 요구 기반 시험과 독립 검토 증거 확보.

#### 한줄 요약

- HARA부터 요구•구현•시험까지 안전 추적 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MC/DC Coverage (ASIL D 전용)**: 개별 조건식이 전체 분기 결과에 독립적으로 영향을 미침을 검증하는 최고 난이도의 화이트박스 커버리지.

</details>

| 고려 항목 | QM (Quality Management) | ASIL A / B | ASIL C / D (최고 등급) |
|:---|:---|:---|:---|
| 위험 수준 | 인명 위험 없음 (에어컨, 오디오 등) | 중저 위험 (헤드라이트, 계기판) | **고위험 (브레이크, EPS 조향, 자율주행)** |
| 안전 정적 분석 | 조직 품질 규칙 적용 | 등급별 권고 기법 적용 | **높은 엄격도의 정적 분석•검토 적용** |
| 단위 시험 커버리지 | 위험 기반 기준 적용 | 구문•분기 커버리지 강화 | **MC/DC 등 독립성 검증 기법 강화** |
| 동적 자원 관리 | 일반 품질 통제 | 고장 영향에 따라 제한 | **결정성•고장 영향 근거로 엄격 통제** |

#### 한줄 요약

- 인명 위해에는 ASIL A~D, 비안전 품질에는 품질관리를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SOTIF (ISO 21448, Safety of the Intended Functionality)**: 시스템 구성요소의 고장이 없더라도, 자율주행 센서(카메라/라이더)의 환경 인지 한계(안개, 악천후)로 인해 발생하는 의도된 기능의 안전성 한계를 다루는 확장 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 모든 모듈을 ASIL D로 개발 시 개발 비용 폭증 | **ASIL Decomposition (ASIL 분해: D $\rightarrow$ B(D)+B(D)) 및 릴레이 채택**| 개발 오버헤드 감축 |
| 인공지능/자율주행 딥러닝 알고리즘의 ISO 26262 적용 난해 | **ISO 21448 SOTIF (의도된 기능 안전) 표준 추가 결합** | 자율주행 안전성 확보 |
| 하드웨어 무결성 정량 평가의 복잡성 | **FMEDA 스캔을 통한 SPFM($\ge 99\%$), LFM($\ge 90\%$) 메트릭 달성**| HW 무결성 입증 |

> 사례: **현대자동차 / AUTOSAR Adaptive Platform 기반 ASIL D 조향(EPS) 모듈 인증**

#### 한줄 요약

- 등급 근거, 독립 검토, 안전 회귀 시험이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **기능 안전 수립 기준(Functional Safety Standards)**: ISO 26262 Part 1~12 표준, HARA 기반 ASIL 등급 및 SOTIF 연계성에 의거한 체계.

</details>

- HARA 결과가 QM이면 **품질관리**, ASIL이면 **등급별 안전 수명주기** 적용

#### 한줄 요약

- ASIL 도출 여부와 등급에 맞는 안전 분류 선택 기준이 핵심이다.
