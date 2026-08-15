---
sidebar:
  order: 215
  label: "215. 카오스 엔지니어링 (Chaos Engineering)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "카오스 엔지니어링 (Chaos Engineering)"
date: "2026-08-14T06:40:00+09:00"
tags: ["notes-software"]
weight: 215
extra:
  question_no: "215"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "통제된 장애 주입과 복원력 검증이 독립적임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Chaos Engineering (카오스 엔지니어링)**: 통제된 장애로 분산 System의 복원력 가설을 검증하는 규율
- **Fault Injection (장애 주입)**: 지연•중단•자원 고갈 등 실패 조건을 의도적으로 만드는 기법

</details>

- 정의/개념: 정상 상태를 정하고 장애 주입으로 **Resilience 가설**을 검증
- 배경/필요성: 정상 Test만으로는 숨은 의존성과 **Cascading Failure** 탐지 곤란

#### 한줄 요약

- 작은 통제 장애로 자동 복구의 **실제 동작**을 사전 검증

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Blast Radius (영향 반경)**: 실험 실패가 영향을 줄 수 있는 최대 자원•Traffic 범위

</details>

- **가설 기반**: 예상 장애와 복구 결과를 사전에 명시
- **사용자 지표**: Server 생존보다 주문•재생•오류율로 판정
- **범위 통제**: 단일 Pod•AZ•Traffic 비율부터 시작
- **Abort 조건**: SLO 이탈 시 Kill Switch로 즉시 중단

#### 한줄 요약

- 사용자 지표•제한 범위•자동 중단으로 **안전한 장애 실험** 수행

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Resilience Hypothesis (복원력 가설)**: 특정 장애에도 정상 지표가 유지될 것이라는 검증 명제

</details>

```text
[Chaos Experiment]
 ├── [Steady-State Metric | 사용자 기준선]
 ├── [Resilience Hypothesis | 장애•예상 결과]
 ├── [Fault Injector | 지연•중단•고갈]
 ├── [Safety Controller | 범위•Abort]
 └── [Observer | 판정•개선 Backlog]
```

| 구성요소 | 책임 |
|---|---|
| Steady-State Metric | 사용자 관점의 **정상 기준선** 정의 |
| Resilience Hypothesis | 장애 조건과 **예상 거동** 명세 |
| Fault Injector | 승인 Target에 **실패 Event** 주입 |
| Safety Controller | Blast Radius와 **Kill Switch** 통제 |
| Observer | 가설 판정과 **개선 Backlog** 도출 |

#### 한줄 요약

- 기준선•가설•주입•안전•관측으로 **실험 통제** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Abort Condition (중단 조건)**: 사용자 지표가 안전 한계를 넘을 때 실험을 멈추는 규칙

</details>

```text
[실험 대상 입력]
          │
          ▼
[1. 정상 상태 측정]
          │
          ▼
[2. 복원력 가설 설정]
          │
          ▼
[3. 안전 범위 검토]
          │
          ▼
[4. 장애 주입]
          │
          ▼
┌────[5. 정상 상태 비교]────┐
│ 실패: Abort•개선          │
│ 성공: 범위 확대 검토      │
└────────────────────────────┘
```

### 동작 원리

1. **정상 상태 측정**: 사용자 지표의 허용 범위 기록
2. **복원력 가설 설정**: 장애와 예상 자동 복구 거동 명세
3. **안전 범위 검토**: Target•Blast Radius•Abort 승인
4. **장애 주입**: 지연•Process 중단•Packet Drop 실행
5. **정상 상태 비교**: 가설 판정 후 개선•범위 확대 결정

#### 한줄 요약

- 정상 기준과 복구 가설을 **통제 장애**로 검증

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **GameDay**: 여러 Team이 합의한 장애 시나리오를 실행•관측•회고하는 훈련

</details>

| 비교 항목 | Chaos Engineering | DR Drill | Load Test |
|---|---|---|---|
| 검증 대상 | 자동 복구•숨은 의존성 | 사람•Runbook•RTO/RPO | 처리량•지연•병목 |
| 자극 | **Fault Injection** | 재해 전환 시나리오 | Traffic 증가 |
| 한계 | 실제 장애 위험 | 예측 밖 연쇄 장애 누락 | Component 장애 미검증 |

#### 한줄 요약

- 자동 복구는 Chaos, 절차는 DR Drill, 용량은 **Load Test** 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Kill Switch**: Abort 조건 도달 시 모든 장애 주입을 즉시 중지하는 장치

</details>

| 고려사항 | 대책 |
|---|---|
| Blast Radius 초과 | Stage 선행 후 단일 Pod부터 **점진 확대** |
| 정상 상태 판정 분쟁 | 사용자 Business 지표와 **SLO**로 통일 |
| 수동 중단 지연 | APM 연동 **Abort•Kill Switch** 자동화 |
| 조직의 실험 공포 | 합의된 Scenario로 정기 **GameDay** 수행 |

#### 한줄 요약

- 작은 범위•SLO•자동 중단•GameDay로 **실험 위험** 제한

## Ⅶ. 결론

<details><summary>쉽게 이해하기 (학습용)</summary>

- 단일 Pod 실험이 안전하게 끝나야 다음 Zone 수준 실험으로 넓힌다.

</details>

- Kill Switch가 검증된 단일 Target부터 **Blast Radius를 단계 확대**
