---
sidebar:
  order: 2
  label: "002. 병목 분석 (Bottleneck Analysis)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "병목 분석 (Bottleneck Analysis)"
date: "2026-08-13T23:00:00+09:00"
tags:
  - "notes-evaluation"
weight: 2
extra:
  question_no: "002"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "대기•자원 포화 원인을 찾는 핵심 진단법"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **병목(Bottleneck)**: 시스템 처리량을 제한하고 응답 지연을 유발하는 제약 자원 및 구간.
- **임계 경로(Critical Path)**: 최종 사용자 응답시간을 결정하는 최장 실행 시간 경로.
- **병목 분석(Bottleneck Analysis)**: 자원 및 경로별 정량 측정 기반 성능 제약 원인 식별 프로세스.

</details>

- 정의: 처리량·응답시간을 제약하는 **병목 원인 추적**
- 필요성: 평균만으로는 **순간 포화·임계 경로 식별 불가**

#### 한줄 요약

- 처리량을 제한하는 **핵심 제약 자원 우선 제거**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **포화(Saturation, 큐 대기열 적체)**: 서버가 유입되는 요청을 즉시 처리하지 못하고 한계에 부딪혀 대기열(Queue)에 작업이 누적되어 지연이 기하급수적으로 늘어나는 징후.
- **상관 분석(Correlation Analysis)**: 어플리케이션 계층의 요청 지연 발생 시점과 인프라 계층의 자원 포화 시점을 동일한 시계열 그래프상에 배치하여 인과 관계를 추론하는 분석 기법.
- **병목 이동 검증(Bottleneck Shift Verification)**: 병목 구간 튜닝 직후 부하 테스트를 재수행하여, 다음으로 한계에 도달하는 후순위 자원과 전체 시스템 처리량 개선 폭을 확인하는 반복 점검 과정.

</details>

- 지연·포화 시점의 **상관 분석**으로 원인 후보 도출
- 자원과 사용자 품질의 **교차 진단**으로 맹점 제거
- 개선 전후 부하곡선으로 **병목 이동 검증**

#### 한줄 요약

- 시계열 상관과 재시험을 통한 **병목 원인 입증**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **USE(Utilization, Saturation, Errors)**: 시스템 내부 자원을 대상으로 이용률, 대기열 포화도, 에러 발생을 점검하여 인프라 병목을 진단하는 방법론.
- **RED(Requests, Errors, Duration)**: 마이크로서비스 및 API별로 초당 요청률, 실패율, 응답시간 지연을 관측하여 소프트웨어 및 아키텍처 제약을 분석하는 방법론.

</details>

```text
병목 분석 체계
├─ 업무 부하•기준선
├─ 관측 증거
│  ├─ 서비스 RED 지표
│  ├─ 자원 USE 지표
│  └─ 추적•프로파일 증거
└─ 상관 분석기
```

가지의 의미: 통제된 부하 환경에서 수집된 서비스 로그, 인프라 메트릭, 런타임 프로파일링 증거의 상관 분석 구조.

| 구성요소 | 책임 및 역할 |
|:---|:---|
| 업무 부하•기준선 | 요청률·동시성·정상 기준 고정 |
| 서비스 RED 지표 | **RED** 기반 요청·오류·지연 수집 |
| 자원 USE 지표 | **USE** 기반 이용·포화·오류 산출 |
| 추적•프로파일 증거 | **임계 경로**·함수 핫스폿 연결 |
| 상관 분석기 | RED·USE·추적의 원인 후보 도출 |

#### 한줄 요약

- **USE·RED 융합**으로 대기열 원인 규명

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **재현 조건(Reproducible Conditions, 테스트 통제 변인)**: 병목 개선 작업 전후의 성능 변화를 객관적으로 평가할 수 있도록 트래픽 요청률, 테스트 데이터 셋, 서버 인프라 환경을 동일하게 고정시킨 시험 요건.
- **기준 부하 실행(Baseline Load Execution)**: 철저히 통제된 재현 조건 위에서 사전 정의된 부하를 가하여, 비교의 척도가 될 기준 성능 지표를 생성하는 기초 단계.
- **요청 추적•자원 지표 수집(Telemetry Collection)**: 부하가 발생하는 동안 분산 환경에서의 종단 지연시간과 서버 내 각 자원의 사용률, 포화 큐, 오류 발생 건수를 일제히 수집하는 관측 과정.
- **USE•RED 지표 상관 분석(Metric Correlation Analysis)**: 수집된 개별 지표들을 하나의 시계열 상에 병합하여 서비스 응답 지연의 원인이 인프라 포화에 기인한 것인지 상관성을 파악하는 분석 절차.
- **병목 후보 검증(Bottleneck Candidate Validation)**: 도출된 유력 병목 후보 중 단 하나의 요인만을 수정 적용한 후, 이전과 완전히 동일한 조건으로 부하를 재인가하여 실제 개선 여부를 증명하는 단계.

</details>

```text
분석가
   │ 재현 조건 확정
   ▼
부하 도구
   │ 1. 기준 부하 실행
   ▼
시험 대상•자원 수집기
   │ 2. 요청 추적·자원 지표 수집
   │ 3. USE·RED 지표 상관 분석
   ▼
검증 책임자
   │ 4. 병목 후보 검증
   ▼
개선 전후 처리량•지연 결과
```

### 동작 원리

1. **기준 부하 실행**: 재현 조건의 비교 기준선 수립
2. **요청 추적·자원 지표 수집**: 지연·USE 상태 수집
3. **USE·RED 지표 상관 분석**: 지연·포화 시점 연결
4. **병목 후보 검증**: 단일 변수 변경 후 재시험

#### 한줄 요약

- 동일 조건 재시험으로 **성능 향상 효과 검증**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **자원 병목(Resource Bottleneck, 하드웨어 임계 도달)**: 서버 내부의 핵심 인프라인 CPU, 물리 메모리 용량, 디스크 처리량, 네트워크 대역폭 등이 한계치에 달해 작업이 대기하고 전체 속도가 저하되는 상태.
- **DB(Database, 데이터베이스 시스템)**: 다수 동시 요청에 대한 데이터 정합성과 동시성 제어 락(Lock) 경합이 발생하기 쉬운 핵심 백엔드 저장소.
- **구간 병목(Segment Bottleneck, 소프트웨어 경로 지연)**: 특정 마이크로서비스 호출 지연, 서드파티 API 응답 지연, DB의 슬로우 쿼리 등이 전체 비즈니스 트랜잭션의 지연시간을 좌우하는 애플리케이션 레이어의 정체 현상.
- **자원•서비스 연계 분석(Resource-Service Co-analysis)**: 하드웨어 컴포넌트 관점의 USE 프레임워크와 소프트웨어 호출 중심의 RED 프레임워크를 유기적으로 병행하여 장애의 근본 원인을 입체적으로 역추적하는 고도화 진단 기법.

</details>

<details><summary>용어 설명</summary>

- **Resource Bottleneck**: A state where hardware components like CPU, Memory, Disk, or Network reach limits, causing task queues and performance degradation.
- **DB(Database)**: Backend storage where concurrency control, locks, and data integrity constraints often create bottlenecks.
- **Segment Bottleneck**: App-layer latency caused by slow service calls, 3rd-party APIs, or long-running database queries.
- **Resource-Service Co-analysis**: An advanced diagnostic approach integrating USE and RED frameworks to trace root causes holistically.

</details>

| 병목 분석 관점 | USE Method (Resource-centric) | RED Method (Service-centric) |
|:---|:---|:---|
| 주 적용 대상 | **자원 병목**·포화 진단 | **구간 병목**·API 경로 진단 |
| 핵심 특징 및 지표 | **USE** 이용·포화·오류 | **RED** 요청·오류·지연 |
| 분석의 한계 | 업무 경로 파악 미흡 | 물리 자원 원인 식별 미흡 |

> 요약: 성능 진단의 사각지대 해소를 위한 USE와 RED 기반의 **Resource-Service Co-analysis** 수행.

#### 한줄 요약

- 자원·서비스 지표를 융합한 **병목 규명**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **부하곡선(Load Curve, 성능-부하 상관그래프)**: 동시 사용자 등 부하 크기 증가에 비례하여 시스템의 초당 처리량 상승폭, 응답시간 지연, 에러 발생 빈도 및 자원 이용률의 추세를 시각적으로 나란히 나타낸 분석 차트.
- **병목 이동(Bottleneck Shift, 제약점 전이 현상)**: 가장 치명적인 제약 자원을 튜닝하거나 증설하여 해결한 직후, 시스템 전체 처리량이 상승하면서 그동안 드러나지 않던 차순위 자원이나 논리 구간이 한계에 부딪혀 새로운 병목으로 부상하는 현상.

</details>

| 실무상 한계점 | 실질적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 평균 이용률이 순간 포화를 은폐 | **USE** 큐·오류 병행 관측 | 자원 임계점 조기 식별 |
| 평균 지연이 느린 경로를 은폐 | **RED** 꼬리 지연·오류 관측 | 비정상 호출 경로 적발 |
| 튜닝 후 **병목 이동** 미인지 | 동일 조건 **부하곡선** 재도출 | 차순위 병목 식별 |

#### 한줄 요약

- 큐 적체·오류 급증의 **임계 구간 식별**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **가설 검증(Hypothesis Testing)**: 관측된 다양한 성능 지표와 분석 결과를 바탕으로 가장 유력한 병목 요인을 가설로 수립하고, 다른 변수들을 통제한 채 단일 요인만을 변경해 부하 테스트를 재수행함으로써 개선 전후의 처리량 변화를 과학적으로 비교 입증하는 절차.
- **개선 우선순위(Prioritization of Improvements)**: 다수의 병목 후보 중 가장 비용 효율적이고 즉각적인 전체 시스템 처리량 상향을 가져올 수 있는, 즉 임계 경로 내에서 포화 증거가 뚜렷한 대기열 유발 자원부터 집중적으로 튜닝 및 증설하는 전략적 결정.

</details>

- **가설 검증** 후 임계 경로의 포화 자원부터 개선

#### 한줄 요약

- 포화 증거가 큰 **임계 경로 자원 우선 개선**
