---
sidebar:
  order: 7
  label: "007. 실시간 스케줄링: Rate Monotonic•EDF (Real-Time Scheduling)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "실시간 스케줄링: Rate Monotonic•EDF (Real-Time Scheduling)"
date: "2026-08-13T12:58:00+09:00"
tags: [notes-software]
weight: 7
extra:
  question_no: "007"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출, 마감시간 보장 알고리즘 중요"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Real-Time Scheduling**: 시스템의 결과값뿐만 아니라, 지정된 마감시간(Deadline) 내에 연산을 성공적 수행 완료해야 하는 결정적(Deterministic) 제어 스케줄링.
- **RM(Rate Monotonic)**: 정적(Static) 선점형 스케줄링으로, 작업의 주기(Period)가 짧을수록(발생 빈도가 높을수록) 높은 우선순위를 정적 부여하는 알고리즘.
- **EDF(Earliest Deadline First)**: 동적(Dynamic) 선점형 스케줄링으로, 남아있는 절대 마감시간(Absolute Deadline)이 가장 임박한 태스크에게 최고 우선순위를 부여하는 알고리즘.

</details>

- 정의/개념: 주기•실행시간•마감시간으로 작업 우선순위를 정하는 **RM•EDF**
- 배경/필요성: 일반 처리량 중심 정책은 **마감시간 준수 여부 산정 불가**

#### 한줄 요약

- 최악 실행시간과 마감시간을 기준으로 우선순위와 선점을 결정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **WCET(Worst-Case Execution Time)**: 태스크가 최악의 파이프라인/메모리 대기 상황에서 소비 가능한 최대 물리 실행 시간.
- **Schedulability Test (스케줄 가능성 검증)**: 태스크 집합이 주어진 가정에서 마감을 지킬 수 있는지 사전 검증하는 분석.

</details>

- **WCET**와 주기•마감시간을 이용한 시간 제약 분석
- 정적 주기 기반 우선순위 산정(**RM**) vs 동적 임박 마감시간 우선 산정(**EDF**)
- **Schedulability Test** 및 Utilization 한계 기반의 **Admission Control(수용 제어)**

#### 한줄 요약

- WCET 기반 수용 분석으로 마감 가능한 작업만 등록한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Utilization Bound ($U$)**: CPU 자원 이용률 상한선으로, RM의 경우 $U \le n(2^{1/n}-1) \approx 69\%$, EDF의 경우 $U \le 100\%$ 조건 형성.

</details>

```text
[실시간 작업 집합]
         |
[스케줄 가능성 분석기]
         |
[우선순위 준비 큐]
         |
 [선점 스케줄러]
```

선의 의미: 실시간 작업 집합(Period, WCET)이 스케줄 가능성 분석기의 수용 테스트를 통과하여 우선순위 준비 큐를 거쳐 선점 스케줄러 디스패치로 연결되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 실시간 태스크 모수 | $C_i$ (WCET), $T_i$ (주기 Period), $D_i$ (상대 마감시간) 파라미터 정의 |
| 스케줄 가능성 분석기 | 태스크 가정에 맞는 **이용률•응답시간 분석** 수행 |
| 우선순위 준비 큐 | RM(주기 $T_i$ 역비례 정적 정렬) 및 EDF(절대 마감시간 동적 정렬) 큐 운영 |
| 선점 스케줄러 | 우선순위 역전 방지(PIP/PCP) 및 하드웨어 타이머 기반 선점 디스패치 |

$$U=\sum_{i=1}^{n}\frac{C_i}{T_i} \le \text{Bound}$$

#### 한줄 요약

- 스케줄 가능성과 RM 충분조건 또는 EDF 이용률 조건으로 수용한 작업을 우선순위 큐에서 선점 실행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Priority Inversion (우선순위 역전)**: 낮은 우선순위 태스크가 공유 자원의 락(Mutex)을 점유함으로 인해 중간 우선순위 태스크에 밀려 고우선순위 태스크가 무한 대기하는 현상.

</details>

```text
[실시간 작업 집합: Cᵢ•Tᵢ•Dᵢ]
              │
              ▼
1. 스케줄 가능성•수용 판정
              │
              ▼
2. 우선순위 정책 선택
       ┌──────┴────────┐
       │ 고정 주기     │ 가변 절대 마감
       ▼               ▼
 [RM 고정 우선순위] [EDF 동적 우선순위]
       └──────┬────────┘
              ▼
3. 릴리스 작업 우선순위 정렬
              │
              ▼
4. 선점•디스패치
              │
              ▼
5. 마감 준수•과부하 감시
              │
              └── 다음 릴리스로 반복
```

### 동작 원리

1. **스케줄 가능성·수용 판정**: $C_i, T_i$ 기반 이용률 $U$ 계산 및 스케줄링 수용성 승인.
2. **우선순위 정책 선택**: 고정 주기 시 **RM(Rate Monotonic)**, 동적 마감 시 **EDF** 선택.
3. **릴리스 작업 우선순위 정렬**: 주기 $T_i$ 최단 우선(RM) 또는 절대 마감 $t+D_i$ 최단 우선(EDF) 큐 정렬.
4. **선점·디스패치**: 하위 태스크 구동 중 고우선순위 릴리스 발생 시 **Preemption** 인가.
5. **마감 준수·과부하 감시**: 마감 미스 감시 및 과부하 시 중요도(Criticality) 낮은 태스크 Drop.

#### 한줄 요약

- 스케줄 가능성·수용 판정 후 우선순위 정책 선택으로 마감을 통제한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PIP (Priority Inheritance Protocol)**: 락을 쥔 저우선순위 태스크의 우선순위를 락을 대기하는 고우선순위 태스크 급으로 임시 격상시키는 대책.
- **PCP (Priority Ceiling Protocol)**: 자원별로 최우선 선점 상한(Ceiling)을 설정하여 우선순위 역전과 데드락을 원천 차단하는 대책.

</details>

| 비교 항목 | Rate Monotonic (RM) | Earliest Deadline First (EDF) |
|:---|:---|:---|
| 우선순위 할당 방식 | **정적** (주기 $T_i$에 역비례하여 사전 할당) | **동적** (남은 절대 마감시간에 의존) |
| 단일 CPU 충분 조건 | 조화되지 않은 암시적 마감 작업에 이용률 경계 | 선점•독립•암시적 마감 가정에서 $U \le 1$ |
| 런타임 오버헤드 | 낮음 (정적 선점 큐 구조) | 높음 (매 태스크 릴리스마다 마감 재계산) |
| 과부하 시 동작 | 낮은 고정 우선순위부터 미스 가능 | 마감 임박 작업 간 연쇄 미스 가능 |

#### 한줄 요약

- RM의 고정 주기 우선순위와 EDF의 절대 마감 우선순위를 비교한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Domino Effect**: EDF 스케줄링에서 시스템 과부하 시 한 태스크의 마감 미스가 하위 모든 태스크의 마감 미스로 연쇄 파급되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유 자원 경쟁에 따른 **Priority Inversion** 발생 | **PIP (Priority Inheritance)** 및 **PCP (Priority Ceiling)** | 고우선순위 대기 시간 제한 |
| EDF 과부하 시 마감 미스 연쇄 파급 | **수용 제어**와 중요도 기반 작업 제거 | 필수 작업의 자원 우선 확보 |
| 자원 억세스 및 인터럽트 오버헤드로 인한 WCET 오차 | 하드웨어 틱 오버헤드를 $C_i$ 보정치에 반영 | 스케줄 가능성 분석 정합성 확보 |

> 사례: 자동차 ECU 표준 **AUTOSAR OS** 및 RT-Linux(PREEMPT_RT) 상의 **RM/EDF 스케줄러** 구현

#### 한줄 요약

- 고정 주기 제어는 짧은 주기에 높은 RM 우선순위를 부여한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **실시간 스케줄링 선택 기준(Real-Time Scheduling Selection Criteria)**: 주기성 여부, CPU 이용률 목표, 시스템 과부하 시 내결함성에 근거한 체계.

</details>

- 고정 주기•정적 검증은 **RM**, 동적 절대 마감 우선은 **EDF** 선택

#### 한줄 요약

- 고정 주기는 RM, 변동하는 절대 마감은 EDF를 선택한다.
