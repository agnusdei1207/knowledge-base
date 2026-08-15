---
sidebar:
  order: 10
  label: "010. 은행원 알고리즘 (Banker's Algorithm)"
  badge:
    text: "미출 • 50%"
    variant: note
title: 은행원 알고리즘 (Banker's Algorithm)
date: "2026-08-13T13:08:00+09:00"
tags: [notes-software]
weight: 10
extra:
  question_no: "010"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "최대 요구량 기반 교착상태 회피 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Banker's Algorithm (은행원 알고리즘)**: 자원 요청 시, 사전 선언된 최대 요구량(Max Claim)을 바탕으로 신규 할당 후에도 시스템이 Safe State(안전 상태)를 유지하는지 시뮬레이션 계산하여 승인하는 대표적 교착상태 회피(Avoidance) 알고리즘.
- **Safe State (안전 상태)**: 모든 프로세스가 최종적으로 작업을 마치고 정상 종료될 수 있는 안전 순서(Safe Sequence)가 최소 1개 이상 존재하는 시스템 상태.

</details>

- 정의/개념: 프로세스 자원 추가 요청 시, 임시 가상 할당을 인가한 후 안전 순서(Safe Sequence)가 유지될 때만 최종 자원 억세스를 승인하는 **은행원 알고리즘(Banker's Algorithm)**
- 배경/필요성: 현재 가용량만 본 할당은 이후 **안전 순서 소멸** 가능

#### 한줄 요약

- 모든 프로세스의 안전 순서가 남는 요청만 승인한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Available Vector**: 각 자원 종류별로 현재 즉시 할당 가능한 유휴 자원 수량 배열 (크기 $m$).
- **Max Matrix**: 프로세스별 수명주기 동안 요구 가능한 최대 자원 수량 행렬 ($n \times m$).
- **Allocation Matrix**: 현재 프로세스별로 할당 점유 중인 자원 수량 행렬 ($n \times m$).
- **Need Matrix**: 프로세스가 향후 추가 요구할 수 있는 남아있는 자원 잔여량 행렬 ($\text{Need} = \text{Max} - \text{Allocation}$).

</details>

- 자원 사전 선언(Max Claim) 및 시뮬레이션 가상 할당(Tentative Allocation) 수행
- **Available**, **Max**, **Allocation**, **Need** 4대 데이터 구조체(Vector/Matrix) 인가
- 안전성 검사(Safety Algorithm)를 통한 **Safe Sequence** 도출 시만 실제 물리 할당 수용

#### 한줄 요약

- 최대 요구량과 가상 할당을 기반으로 안전 상태를 판정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Work Vector**: Safety Algorithm 시뮬레이션 중 임시 가용 자원 수량을 추적하는 가상 벡터.
- **Finish Vector**: 프로세스 $i$의 정상 실행 완료 가능 여부를 표시하는 Boolean 배열 ($\text{Finish}[i] = \text{True/False}$).

</details>

```text
[자원 상태]
 ├─ Available Vector
 ├─ Max Matrix
 ├─ Allocation Matrix
 └─ Need Matrix
          |
 [Safety Algorithm]
```

선의 의미: 요청 프로세스가 추가 자원을 요청하면 요청 제어기가 한도 및 가상 할당을 통제하고, 안전성 검사기가 자원 상태의 Safe Sequence를 검증하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| Available Vector | 현재 시스템 내 이용 가능한 각 타입별 유휴 자원 수치 보관 |
| Max Matrix | 프로세스 $P_i$가 요청 가능한 최대 자원 수량 바운더리 기록 |
| Allocation Matrix | 프로세스 $P_i$가 현재 점유 중인 물리 자원 수량 기록 |
| Need Matrix | 프로세스 $P_i$가 향후 추가로 요청할 자원 잔여량 ($\text{Need}_i = \text{Max}_i - \text{Allocation}_i$) 저장 |
| Safety Algorithm | 임시 가상 할당 후 $\text{Need}_i \le \text{Work}$ 조건 만족 프로세스를 찾아 **Safe Sequence** 탐색 |

$$\mathrm{Need}_i=\mathrm{Max}_i-\mathrm{Allocation}_i,\qquad \mathrm{Request}_i\le\mathrm{Need}_i,\quad \mathrm{Request}_i\le\mathrm{Available}$$

#### 한줄 요약

- 자원 상태와 안전성 검사기 기반 요청 승인 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Safety Algorithm**: `Work = Available`, `Finish[i] = False` 초기화 후, $\text{Need}_i \le \text{Work}$를 만족하는 $i$를 찾아 `Work = Work + Allocation_i`, `Finish[i] = True`를 반복 수행하는 4단계 알고리즘.

</details>

```text
┌──────────────────────────────┐
│ 추가 자원 요청              │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 요청 한도 검사           │
│ Request ≤ Need              │
│ Request ≤ Available         │
└───────┬──────────────────────┘
        ├─ 위반 ────────────────▶ [거절]
        │ 충족
        ▼
┌──────────────────────────────┐
│ 2. 요청 가상 반영           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 3. Work•Finish 초기화       │
└──────────────┬───────────────┘
               ▼
╔══════════════════════════════╗
║ 반복: Finish=false이며       ║
║       Need≤Work인 행 존재    ║
║ 4. 안전 순서 탐색           ║
║ Finish=true                 ║
║ Work += Allocation          ║
╚══════════════╤═══════════════╝
               │ 선택 가능한 행 없음
               ▼
┌──────────────────────────────┐
│ 5. 확정•복원 판정           │
└───────┬──────────────────────┘
        ├─ 모든 Finish=true ────▶ [할당 확정]
        └─ 완료 불가 존재 ──────▶ [상태 복원•거절]
```

### 동작 원리

1. **요청 한도 검사**: $\text{Request}_i \le \text{Need}_i$ 및 $\text{Request}_i \le \text{Available}$ 1차 검증.
2. **요청 가상 반영**: $\text{Available} = \text{Available} - \text{Request}_i$, $\text{Allocation}_i = \text{Allocation}_i + \text{Request}_i$, $\text{Need}_i = \text{Need}_i - \text{Request}_i$ 가상 세팅.
3. **Work·Finish 초기화**: `Work = Available`, `Finish[i] = False` 포인터 초기화.
4. **안전 순서 탐색**: $\text{Finish}[i] == \text{False}$ 및 $\text{Need}_i \le \text{Work}$ 만족하는 $i$ 탐색, `Work += Allocation_i`, `Finish[i] = True` 반복.
5. **확정·복원 판정**: 모든 $i$에 대해 $\text{Finish}[i] == \text{True}$ 성립 시 확정(Safe), 실패 시(Unsafe) 가상 할당 롤백 및 요청 블록.

#### 한줄 요약

- 요청 가상 반영 후 안전 순서 탐색이 성공할 때만 확정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Safe vs Unsafe State**: Unsafe State는 교착상태가 발생할 수도 있는 불안전 가능성 상태이며, 교착상태 그 자체는 아님 (Unsafe ⊃ Deadlock).

</details>

| 비교 항목 | Safe State (안전 상태) | Unsafe State (불안전 상태) | Deadlock (교착상태) |
|:---|:---|:---|:---|
| 정의 | 모든 프로세스 완결 가능한 **Safe Sequence** 존재 | 안전 순서(Safe Sequence) 수립 불가 | 프로세스가 영구 블록되어 정지된 최악 상태 |
| 자원 승인 여부 | 안전성을 유지하는 요청 승인 | 해당 가상 할당을 거부•대기 | 탐지 후 종료•롤백 등 복구 필요 |
| 시스템 진행성 | 선언된 최대량 가정에서 완료 순서 존재 | 향후 교착 가능성 존재 | 관련 실행 주체의 진행 정지 |

#### 한줄 요약

- 안전 순서 존재 여부로 안전•불안전 상태를 구분한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Max Claim Pre-declaration**: 각 프로세스의 최대 자원 요구량을 사전에 선언해야 하는 제약.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 최대 자원 요구량(**Max Claim**) 예측 오차 | 계약 기반 상한과 요청 검증 적용 | 잘못된 최대량 선언 차단 |
| 매 요청의 **Safety Algorithm** 계산 비용 | 자원군 분리와 검사 범위 축소 | 승인 지연 감소 |
| 프로세스 수가 가변적으로 변동하는 대규모 동적 시스템 환경 | 프로세스 인입/퇴출 시 Matrix 동적 재할당 | 런타임 알고리즘 정합성 보장 |

> 사례: OS 커널 메인프레임 및 결정론적 하드 실시간 시스템 상의 **Banker's Avoidance** 모듈 적용

#### 한줄 요약

- 원자적 검사와 버전 검증으로 승인 일관성을 유지한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **은행원 알고리즘 적용 기준(Banker's Algorithm Adoption Criteria)**: 자원 수 고정성, Max Claim 사전 선언 가능성, 연산 오버헤드 감당 여부에 기반한 적용 체계.

</details>

- **은행원 알고리즘 적용 기준**에 따라 정적 자원 상한 및 사전 Max 선언이 가능한 특수 미션 크리티컬 인프라에 **은행원 알고리즘** 채택

#### 한줄 요약

- 최대 요구량을 신뢰할 수 있고 검사 지연을 허용할 때 적용한다.
