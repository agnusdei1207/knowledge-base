---
sidebar:
  order: 10
  label: "010. 은행원 알고리즘"
  badge:
    text: "미출 · 50%"
    variant: note
title: "은행원 알고리즘 (Banker's Algorithm)"
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

- **Banker's Algorithm(은행원 알고리즘)**: 프로세스의 자원 요청 시 가상 할당을 수행하고, 시스템이 여전히 안전 상태(Safe State)를 유지하는지 안전성 알고리즘으로 사전 검증하여 교착상태를 능동적으로 회피하는 기법.
- **Safe State(안전 상태)**: 모든 프로세스가 필요로 하는 최대 자원을 순차적으로 할당받아 정상 종료할 수 있는 안전 순서열(Safe Sequence)이 1개 이상 존재하는 시스템 상태.

</details>

- 정의/개념: 프로세스의 사전 선언된 최대 자원 요구량(Max Claim)을 기반으로 자원 요청 시 가상 할당 후 **안전 순서열(Safe Sequence)** 의 존재 여부를 검증하여 할당을 결정하는 교착상태 회피(Deadlock Avoidance) 알고리즘
- 배경/필요성: 동적 자원 할당 시 안전 상태를 벗어난 불안전 상태(Unsafe State) 진입을 선제 차단하여 **시스템 교착상태(Deadlock)를 수학적으로 예방** 필요

#### 한줄 요약

- 자원 요청 시 가상 할당 후 안전 순서열 존재 여부를 시뮬레이션하여 안전 상태에서만 자원을 배분하는 회피 기법

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Available Vector(가용 자원 벡터)**: 현재 시스템에 남아 있는 각 자원 유형별 가용 인스턴스 수.
- **Max Matrix(최대 요구 행렬)**: 각 프로세스가 실행 중 최대로 요구할 수 있는 자원 유형별 인스턴스 상한.
- **Allocation Matrix(현재 할당 행렬)**: 현재 각 프로세스에 할당되어 점유 중인 자원 유형별 인스턴스 수.
- **Need Matrix(추가 요구 행렬)**: 각 프로세스가 작업을 완료하기 위해 향후 추가로 요청할 수 있는 잔여 자원량 ($\text{Need} = \text{Max} - \text{Allocation}$).

</details>

- 프로세스 생성 시 **최대 자원 요구량(Max Claim)** 을 사전에 확정 선언해야 하는 제약
- **Available(가용), Max(최대), Allocation(할당), Need(추가 요구)** 4대 자료구조 기반 상태 추적
- 가상 할당(Tentative Allocation) 및 안전성 검사(Safety Algorithm)를 통한 **안전 순서열(Safe Sequence)** 유효성 판정

#### 한줄 요약

- **최대 요구량 사전 선언·4대 행렬/벡터 상태 관리·가상 할당 기반 안전 순서열(Safe Sequence) 검증**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Work Vector(임시 가용 벡터)**: 안전성 시뮬레이션 중 프로세스 종료 및 자원 반납에 따라 동적으로 증가하는 가상의 가용 자원 벡터.
- **Finish Vector(완료 여부 벡터)**: 안전성 시뮬레이션 중 각 프로세스의 실행 완료 가능 여부를 기록하는 불리언 배열($\text{Finish}[i] = \text{true/false}$).

</details>

```text
[ 은행원 알고리즘 4대 자료구조 및 안전성 검사 아키텍처 ]
             [ 4대 자원 상태 행렬/벡터 ]
  (Available Vector, Max Matrix, Allocation Matrix, Need Matrix)
                         │
                         ▼
             [ 자원 요청 제어기 (Resource-Request Algorithm) ]
     (1단계: Request_i ≤ Need_i 및 Request_i ≤ Available 검증)
     (2단계: 가상 할당 Available - Request, Alloc + Request, Need - Request)
                         │
                         ▼
             [ 안전성 검사기 (Safety Algorithm) ]
       (Work = Available, Finish[i] = false 초기화)
       (Finish[i] == false && Need_i ≤ Work 인 프로세스 순차 탐색)
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 [ 안전 순서열 발견 (Safe) ]   [ 안전 순서열 미발견 (Unsafe) ]
 (실제 물리 자원 할당 확정)    (가상 할당 롤백 및 프로세스 대기)
```

선의 의미: 자원 요청 인입 시 1차 한도 검증 후 가상 할당을 수행하고, 안전성 검사기가 안전 순서열을 도출하여 실제 할당 여부를 결정하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 가용 자원 벡터(Available) | 각 자원 유형 $R_j$의 현재 미할당 유휴 인스턴스 수량 보관 ($1 \times m$ 벡터) |
| 최대 요구 행렬(Max) | 프로세스 $P_i$가 선언한 자원 유형 $R_j$의 최대 필요 인스턴스 수 ($n \times m$ 행렬) |
| 현재 할당 행렬(Allocation) | 프로세스 $P_i$에 현재 배정되어 점유 중인 자원 수량 ($n \times m$ 행렬) |
| 추가 요구 행렬(Need) | 프로세스 $P_i$가 완료를 위해 추가로 요구할 잔여 자원량 ($\text{Max}[i,j] - \text{Allocation}[i,j]$) |
| 안전성 검사기(Safety Checker) | 가상 상태에서 $\text{Need}_i \le \text{Work}$를 만족하는 프로세스를 탐색하여 안전 순서열 유무 판정 |

#### 한줄 요약

- **Available/Max/Allocation/Need 4대 장부·요청 제어기 1차 검증·안전성 검사기(Safety Algorithm)**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Safety Algorithm(안전성 알고리즘)**: 임시 가용 자원(Work)으로 잔여 요구량(Need)을 충족할 수 있는 프로세스를 찾아 완료 처리하고 반납된 자원을 누적하여 모든 프로세스가 완료 가능한지 검증하는 $O(m \times n^2)$ 복잡도의 알고리즘.

</details>

```text
[ 자원 요청 처리 및 안전성 검사 시퀀스 ]
 1. 프로세스 P_i 의 자원 요청 Request_i 발생
          │
          ▼
 2. Request_i ≤ Need_i 검사 ?
      ├── [아니오] ──► 오류 발생 (최대 선언 요구량 초과)
      └── [예]
            │
            ▼
 3. Request_i ≤ Available 검사 ?
      ├── [아니오] ──► 프로세스 P_i 대기 (가용 자원 부족)
      └── [예]
            │
            ▼
 4. 가상 할당 수행:
    Available = Available - Request_i
    Allocation_i = Allocation_i + Request_i
    Need_i = Need_i - Request_i
            │
            ▼
 5. 안전성 검사(Safety Algorithm) 실행:
    Work = Available, Finish[all] = false
    반복: Finish[i] == false 이고 Need_i ≤ Work 인 P_i 탐색
          존재 시: Work = Work + Allocation_i, Finish[i] = true
            │
          ┌─┴──────────────────────────┐
          ▼                            ▼
 [ 모든 Finish[i] == true ]   [ 미완료 프로세스 존재 ]
          │                            │
   (안전 상태 확정)             (불안전 상태 판정)
          │                            │
 6-1. 실제 물리 자원 할당     6-2. 가상 할당 원상 롤백 및 P_i 대기
```

**동작 원리**

1. **1차 유효성 검사**: 요청량($\text{Request}_i$)이 사전 선언된 잔여량($\text{Need}_i$) 및 현재 가용량($\text{Available}$) 이하인지 검증
2. **가상 상태 전이**: 시스템 장부에서 자원을 가상으로 차감·할당하여 임시 상태 구성
3. **안전성 시뮬레이션**: 임시 가용량($\text{Work}$)으로 실행 완료 가능한 프로세스를 찾아 순차적으로 자원을 반납받는 순환 검사 수행
4. **안전 순서열 판정**: 모든 프로세스가 완료될 수 있는 안전 순서열(예: $\langle P_1, P_3, P_0, P_2 \rangle$)이 도출되면 실제 할당 승인
5. **롤백 및 대기**: 안전 순서열을 찾지 못해 불안전 상태로 전이될 위험이 있으면 가상 할당을 즉시 롤백하고 프로세스를 대기 상태로 전환

#### 한줄 요약

- **요청 유효성 검사 $\to$ 가상 할당 $\to$ Safety 검사(Work/Need 순회) $\to$ 안전 시 실제 할당 / 불안전 시 롤백**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Unsafe State(불안전 상태)**: 현재 시점에서 안전 순서열을 보장할 수 없어 프로세스들의 추가 자원 요청 패턴에 따라 교착상태로 진입할 가능성이 존재하는 상태(교착상태 자체와는 구별됨).

</details>

| 구분 | 안전 상태 (Safe State) | 불안전 상태 (Unsafe State) | 교착상태 (Deadlock State) |
|:---|:---|:---|:---|
| 상태 정의 | 모든 프로세스를 완료시킬 수 있는 **안전 순서열** 존재 | 안전 순서열이 존재하지 않아 교착상태 전이 가능성 내포 | 프로세스들이 자원을 상호 점유한 채 무한 대기하는 상태 |
| 자원 할당 승인 | 가상 할당 검증 통과로 즉시 실제 자원 할당 | 자원 할당 거절, 가상 할당 롤백 및 요청 대기 | 할당 불가, 프로세스 강제 종료 또는 롤백 복구 필요 |
| 시스템 진행성 | 100% 무결점 완료 보장 | 추가 요청 패턴에 따라 완료 또는 교착상태 분기 | 시스템 진행 완전 정지 (진행 불가) |

#### 한줄 요약

- 안전 상태는 무조건 완료를 보장하고, 불안전 상태는 교착상태 위험이 있으며, 교착상태는 영구 정지 상태

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Max Claim Pre-declaration(최대 요구량 사전 선언)**: 프로세스 시작 시점에 사용할 자원의 최대치를 명확히 파악하여 시스템에 등록해야 하는 은행원 알고리즘의 핵심 전제 조건.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 프로세스의 실행 경로 분기에 따른 **최대 자원 요구량(Max Claim) 사전 예측 곤란** | 정적 분석 기반 최대 자원 프로파일링 및 보수적 상한 선언 적용 | 요구량 초과 오류 방지 및 알고리즘 적용 기반 확보 |
| 매 자원 요청 시 안전성 검사 실행으로 인한 **$O(m \times n^2)$ CPU 연산 오버헤드** | 자원 풀 클러스터링 및 변경된 자원 유형에 대한 증분 안전성 검사 적용 | 검사 오버헤드 최소화 및 실시간 요청 지연 완화 |
| 동적 프로세스 생성/종료로 인한 **자원 행렬 크기 갱신 동기화 오버헤드** | 고정 크기 풀 사전 할당 및 Read-Copy-Update(RCU) 기반 메타데이터 동기화 | 런타임 행렬 갱신 락 경합 방지 |

#### 한줄 요약

- **보수적 최대 요구량 프로파일링·증분 안전성 검사·RCU 기반 동적 행렬 동기화**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Banker's Algorithm 적용 기준**: 프로세스 수와 자원 수가 고정되어 있고 최대 요구량 사전 파악이 가능한 임베디드/안전 필수 시스템에서 선별 적용.

</details>

- 자원 요구량이 엄격히 정형화된 **항공/철도/원전 등 안전 필수(Safety-Critical) 실시간 임베디드 환경** 대상 은행원 알고리즘 기반 교착상태 회피 표준 채택

#### 한줄 요약

- **사전 요구량 선언과 안전 순서열 검증** 통해 교착상태를 수학적으로 선제 차단하는 회피 아키텍처

