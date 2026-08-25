---
sidebar:
  order: 215
  label: "215. 카오스 엔지니어링"
  badge:
    text: "미출 · 30%"
    variant: note
title: "카오스 엔지니어링 (Chaos Engineering)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
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

- **Chaos Engineering (카오스 엔지니어링)**: 분산 시스템이 프로덕션의 예측 불가능한 결함 상황에서도 안정적으로 동작함을 실증하기 위해 통제된 장애를 의도적으로 주입하고 복원력 가설을 검증하는 실험 규율.
- **Steady State (정상 상태)**: CPU 점유율이 아닌 주문 성공률, 초당 결제 건수 등 비즈니스 관점에서 시스템이 정상 작동하고 있음을 나타내는 기준선.

</details>

- 정의/개념: 비즈니스 정상 상태(Steady State)를 정의하고 **통제된 장애 주입을 통해 분산 시스템의 복원력(Resilience) 가설을 실증하는 실험 규율**
- 배경/필요성: 기존 단위/부하 테스트만으로는 분산 마이크로서비스 간 **숨은 의존성, 연쇄 장애(Cascading Failure) 및 자동 페일오버 결함 사전 검증 불가**

#### 한줄 요약
- 폭발 반경(Blast Radius) 통제와 Kill Switch 아래 의도적 장애를 주입하여 시스템의 자율 복구력을 실증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Blast Radius (폭발 반경)**: 장애 실험 실패 시 고객과 시스템에 미칠 수 있는 최대 영향 범위 (단일 파드에서 가용영역 AZ로 점진 확대).
- **Kill Switch (비상 중단 장치)**: 비즈니스 SLO 임계치 이탈 시 즉시 모든 장애 주입을 중단하고 원상태로 복원하는 안전 메커니즘.

</details>

- 주문 성공률, 스트리밍 재생률 등 비즈니스 관점의 지표로 판정하는 **정상 상태(Steady State) 중심**
- 특정 파드 강제 종료 시에도 서킷 브레이커가 동작한다는 **복원력 가설(Resilience Hypothesis) 검증**
- 단일 파드(1%)에서 시작하여 점진적으로 범위를 넓히는 **폭발 반경(Blast Radius) 통제**

#### 한줄 요약
- 정상 상태 기준선, 복원력 가설 검증, 폭발 반경 통제, 비상 킬 스위치를 통해 안전한 실험을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **카오스 실험 4대 핵심 구조**: Steady-State Baseline(정상 기준선), Fault Injector(장애 주입기), Safety Controller(폭발 반경/킬 스위치), Observability Engine(가설 검증).

</details>

```text
[카오스 엔지니어링 실험 통제 및 장애 주입 아키텍처]
|-- 1. Steady-State Baseline Metric (Prometheus: 주문 성공률 99.9%, 결제 지연 <200ms 정의)
`-- 2. Chaos Experiment Platform (Chaos Mesh / LitmusChaos / Gremlin)
    |-- Resilience Hypothesis: "결제 DB 인스턴스 Kill 시에도 Standby 승격으로 주문 지속"
    `-- Fault Injector (Network Latency, Packet Loss, Pod Kill, CPU/Memory Hog 주입)
`-- 3. Blast Radius & Safety Controller (APM SLO 위반 감지 시 즉각 Rollback Kill Switch)
`-- 4. Observability & Remediation Engine (실험 결과 분석 및 복원력 개선 백로그 Jira 등록)
```

선의 의미: 계층 및 정상 기준선을 수립하고 가설에 따라 통제된 장애를 주입하며 안전 제어기가 SLO를 감시하고 결과를 개선 백로그로 환류하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **정상 기준선 (Steady-State)**| 인프라 메트릭이 아닌 사용자 비즈니스 관점의 **정상 동작 기준선(주문 성공률) 정의** | SLO 기반 메트릭 |
| **복원력 가설 (Hypothesis)** | 주입할 장애 유형과 이에 대응하는 **시스템의 예상 자율 복구 거동을 명문화** | 가설 기반 실험 |
| **장애 주입기 (Injector)** | 승인된 대상 컨테이너/네트워크에 **지연, 패킷 유실, 프로세스 중단 이벤트 주입** | Chaos Mesh, Gremlin |
| **안전 제어기 (Safety)** | 실험 영향 범위를 최소화하고 **SLO 침해 시 즉시 주입을 중단하는 Kill Switch 제어**| Blast Radius 통제 |
| **관측 및 환류 (Observer)** | 실험 전후 지표를 비교하여 **가설 성립 여부를 판정하고 아키텍처 개선 백로그 도출** | 개선 과제 도출 |

#### 한줄 요약
- 정상 기준선, 복원력 가설, 장애 주입기, 안전 제어기, 관측 환류 계층이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **카오스 실험 5단계**: 정상 상태 측정 $\to$ 복원력 가설 설정 $\to$ 안전 범위/중단 조건 승인 $\to$ 통제된 장애 주입 $\to$ 가설 검증 및 환류.

</details>

```text
카오스 엔지니어링 복원력 실증 실험 가동
        │
   1. [정상 상태 측정] 평상시 결제 API의 성공률(99.95%)과 응답 지연(120ms) 기준선 고정
        │
   2. [가설 설정] "추천 서비스 파드 3대를 강제 Kill해도 서킷 브레이커가 동작하여 주문 성공"
        │
   3. [안전 범위 승인] 카나리 트래픽 5% 대상 2분간 실행 및 SLO 99% 이탈 시 자동 중단 승인
        │
   4. [장애 주입 실행] Chaos Mesh가 추천 서비스 파드 3대를 즉시 강제 종료(Pod Kill)
   ┌────┴───────────────────────────┐
  가설 검증 성공                   가설 검증 실패 (SLO 이탈)
   │                                 │
5A. [Blast Radius 확대]            5B. [즉각 Kill Switch 중단]
   스테이징에서 프로덕션 단계적 확대     실험 롤백 후 장애 원인 리팩터링
   │                                 │
   └────┬────────────────────────────┘
        ▼
   시스템 복원력 및 내결함성 신뢰도 확보
```

#### 한줄 요약
- 정상 측정 → 가설 설정 → 안전 승인 → 장애 주입 → 가설 검증 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Chaos Engineering vs DR Drill vs Load Testing**: 시스템 자율 복구 검증(Chaos), 사람의 런북 절차 검증(DR), 인프라 용량 한계 검증(Load).

</details>

| 비교 항목 | 카오스 엔지니어링 (Chaos Engineering) | 재해복구 훈련 (DR Drill) | 부하 테스트 (Load Testing) |
|:---|:---|:---|:---|
| 핵심 검증 대상 | **시스템의 자율 복구 기제, 숨은 연쇄 장애** | **사람의 대응 절차, Runbook, RTO/RPO 달성** | **시스템 처리량 한계(TPS), 병목 지점 도출** |
| 인위적 자극 형태| **통제된 Fault Injection (파드 킬, 망 지연)**| 센터 단위 페일오버 및 모의 전환 시나리오 | 대량의 가상 사용자 동시 트래픽 인가 |
| 최적 실행 환경 | 스테이징 및 통제된 프로덕션 환경 | 재해복구(DR) 전용 백업 센터 | 스테이징 및 성능 시험 전용 인프라 |
| 주요 한계점 | 통제 미흡 시 실제 대형 프로덕션 장애 유발 | 대규모 훈련으로 인한 업무 일정 중단 부담 | 컴포넌트 단일 고장 시 복구 능력 미검증 |

#### 한줄 요약
- 자율 복구는 Chaos Engineering, 절차 검증은 DR Drill, 용량 한계는 Load Testing을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **GameDay**: 개발, 운영, SRE 팀이 함께 모여 합의된 카오스 장애 시나리오를 실행하고 시스템의 반응과 모니터링을 실시간 검증하는 실전 훈련 행사.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 프로덕션 장애 주입 중 통제 불능으로 전사 대형 사고 발생 | **단일 Pod에서 시작하여 AZ로 넓히는 `점진적 Blast Radius 확대` 및 Kill Switch** | 실험 리스크 100% 통제 |
| 정상 상태 지표에 대한 팀 간 이견으로 실험 결과 왜곡 | **인프라가 아닌 비즈니스 트랜잭션 기반 `핵심 SLO 메트릭` 사전 합의** | 실험 판정의 객관성 확보 |
| 조직의 장애 주입에 대한 막연한 공포와 반발 | **사전 합의된 시나리오와 온콜이 대기하는 정기 `GameDay` 훈련 운영** | 안전한 복원력 엔지니어링 문화 정착 |
| 카오스 실험으로 드러난 결함이 백로그로 방치되어 망각 | **실험 결함을 스프린트 최우선 `복원력 개선 Jira 티켓`으로 강제 연동** | 실질적 시스템 회복 탄력성 개선 |

#### 한줄 요약
- 점진적 Blast Radius, 핵심 SLO 기준, GameDay 운영, Jira 티켓 연동으로 운영한다.

## Ⅶ. 결론

- 분산 마이크로서비스 및 멀티 클라우드 환경에서 불가피한 장애에 대비하기 위해 **Steady State 기반의 복원력 가설 수립과 폭발 반경(Blast Radius) 통제 프레임워크를 전사 표준화**하고, **Chaos Mesh 자동화와 정기 GameDay 모의훈련**을 결합하여 장애를 사전에 스스로 극복하는 자율 복원 아키텍처 완성

#### 한줄 요약
- 카오스 엔지니어링은 통제된 장애 주입과 가설 검증을 통해 시스템의 숨겨진 취약점을 사전에 발굴하고 복원력을 입증하는 핵심 신뢰성 엔지니어링 기술이다.