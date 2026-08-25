---
sidebar:
  order: 10
  label: "010. 은행원 알고리즘"
  badge:
    text: "미출 · 50%"
    variant: note
title: "은행원 알고리즘 (Banker's Algorithm)"
date: "2026-08-25T10:45:00+09:00"
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

- **은행원 알고리즘(Banker's Algorithm)**: 자원 요청 시 가상 할당을 해보고 안전 상태가 유지될 때만 실제 할당하는 데드락 회피(Avoidance) 알고리즘.
- **안전 순서열(Safe Sequence)**: 시스템 내 모든 프로세스가 최대 자원을 요구하더라도 교착 없이 모두 완료될 수 있는 프로세스 실행 순서.

</details>

- 정의/개념: 프로세스의 최대 자원 요구량을 사전에 선언받고 가상 할당 후 **안전 순서열(Safe Sequence)** 을 검증하여 할당하는 교착상태 회피 알고리즘
- 배경/필요성: 동적 자원 할당 환경에서 **불안전 상태(Unsafe State) 진입에 따른 시스템 교착상태 발생 방지 불가**

#### 한줄 요약
- 가상 할당 시뮬레이션으로 안전 순서열이 존재할 때만 자원을 할당하여 교착상태를 회피한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Available / Max / Allocation / Need**: 가용 자원 벡터($1 \times m$), 최대 요구 행렬($n \times m$), 현재 할당 행렬($n \times m$), 잔여 요구 행렬($\text{Need}=\text{Max}-\text{Alloc}$).

</details>

- 프로세스 생성 시 **최대 자원 요구량(Max Claim)** 의 사전 확정 선언 필수 전제
- **Available(가용), Max(최대), Allocation(할당), Need(잔여)** 4대 장부 자료구조 기반 추적
- 가상 할당 후 $O(m \times n^2)$ 복잡도의 **안전성 알고리즘(Safety Algorithm)** 시뮬레이션 수행

#### 한줄 요약
- 4대 장부로 상태를 추적하고, 안전 상태에서만 할당 승인하며 불안전 시 롤백 대기한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Work / Finish 벡터**: 안전성 검사 시 임시 가용 자원을 시뮬레이션하는 Work 벡터와 프로세스 완료 여부를 추적하는 Finish 불리언 배열.

</details>

```text
[은행원 알고리즘 4대 자료구조 및 검증 아키텍처]
|-- 시스템 자원 장부 (4대 행렬/벡터)
|   |-- Available : 현재 시스템의 유휴 가용 자원 벡터 ($1 \times m$)
|   |-- Max : 프로세스별 최대 필요 자원 행렬 ($n \times m$)
|   |-- Allocation : 현재 프로세스에 할당된 자원 행렬 ($n \times m$)
|   `-- Need : 프로세스별 잔여 필요 자원 행렬 ($\text{Need} = \text{Max} - \text{Allocation}$)
|-- 자원 요청 검증기 (Resource-Request Algorithm)
|   `-- 1차 조건: $\text{Request}_i \le \text{Need}_i$ 및 $\text{Request}_i \le \text{Available}$ 검증
`-- 안전성 시뮬레이터 (Safety Algorithm)
    |-- Work = Available, Finish[all] = false 초기화
    |-- $\text{Need}_i \le \text{Work}$ 만족하는 프로세스 탐색 -> Work += Allocation, Finish=true
    `-- 모든 Finish[i]==true 시 안전 순서열(Safe Sequence) 도출 확정
```

선의 의미: 계층 및 가상 할당 검증 흐름

| 구성요소 | 책임 |
|:---|:---|
| **Available 벡터** | 각 자원 유형별 현재 물리 유휴 수량 보관 ($1 \times m$) |
| **Max 행렬** | 프로세스 $P_i$가 선언한 자원별 최대 요구량 보관 ($n \times m$) |
| **Allocation 행렬** | 프로세스 $P_i$가 현재 점유 중인 자원 인스턴스 수량 관리 |
| **Need 행렬** | 프로세스가 완료되기 위해 추가로 요구할 잔여 자원량 ($\text{Max} - \text{Alloc}$) |
| **안전성 검사기** | 가상 할당 상태에서 **안전 순서열** 존재 여부를 $O(m \times n^2)$으로 판정 |

#### 한줄 요약
- 4대 행렬 장부와 자원 요청 검증기, 안전성 시뮬레이터가 결합되어 동작한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **가상 할당(Speculative Allocation)**: 자원을 실제로 주기 전에 장부 상에서만 차감하여 안전성을 시험해보는 가상 트랜잭션.

</details>

```text
프로세스 P_i 의 자원 요청 Request_i 발생
        │
   Request_i <= Need_i 및 Request_i <= Available 검증
   ┌────┴─────┐
  실패         통과
   │             │
오류 또는 대기   가상 할당 수행 (Available 차감, Alloc 증가, Need 차감)
                 │
            안전성 알고리즘(Safety Algorithm) 시뮬레이션 실행
            (Work = Available 로 두고 Need <= Work 인 프로세스 순차 완수)
                 │
            모든 프로세스를 완수하는 안전 순서열이 존재하는가?
            ┌────┴─────┐
           예           아니오 (불안전 상태: Unsafe)
            │             │
         실제 자원 할당   가상 할당 롤백 및
         승인 및 실행     프로세스 P_i 대기 상태 전환
```

#### 한줄 요약
- 한도 검증 → 가상 할당 → Safety 검사 → 안전 시 실제 할당, 불안전 시 롤백 대기한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **불안전 상태(Unsafe State)**: 안전 순서열이 존재하지 않는 상태로, 향후 프로세스 요청 패턴에 따라 교착상태로 전이될 위험이 있는 상태.

</details>

| 시스템 상태 | 안전 상태 (Safe State) | 불안전 상태 (Unsafe State) | 교착상태 (Deadlock State) |
|:---|:---|:---|:---|
| 상태 정의 | **안전 순서열이 1개 이상 존재** | 안전 순서열 부재 (데드락 위험 내포) | 프로세스 상호 점유 무한 대기 (동결) |
| 자원 할당 결정 | 즉시 자원 할당 승인 | **자원 할당 거절 (요청 프로세스 대기)** | 할당 불가, 프로세스 강제 종료 필요 |
| 시스템 진행성 | 100% 정상 종료 보장 | 추가 요청 패턴에 따라 완료 또는 데드락 | 시스템 진행 영구 중단 |

#### 한줄 요약
- 안전 상태는 무조건 완료를 보장하고, 불안전 상태는 데드락 전이 위험이 있으며, 데드락은 영구 멈춤 상태다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Max Claim 사전 선언**: 프로세스 시작 시점에 사용할 자원의 최대치를 미리 확정하여 등록해야 하는 제약 조건.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동적 분기 프로그램의 **최대 요구량(Max Claim) 사전 예측 곤란** | 정적 코드 분석 기반 보수적 최대 자원 프로파일링 적용 | 런타임 한도 초과 오류 방지 및 회피 기법 적용 |
| 매 자원 요청 시 $O(m \times n^2)$ 계산으로 인한 CPU 오버헤드 | 자원 풀 클러스터링 및 증분 안전성 검사(Incremental Check) | 검사 오버헤드 축소 및 실시간 트랜잭션 지연 완화 |
| 동적 프로세스 생성/소멸로 인한 자원 행렬 크기 변경 락 경합 | RCU(Read-Copy-Update) 기반 메타데이터 동기화 | 런타임 행렬 갱신 시 무중단 조회 성능 확보 |

#### 한줄 요약
- 보수적 Max 프로파일링, 증분 안전성 검사, RCU 메타데이터 동기화로 오버헤드를 완화한다.

## Ⅶ. 결론

- 자원 요구량이 엄격히 사전 규정된 **항공/원전/철도 안전 필수(Safety-Critical) 임베디드 OS**에 은행원 알고리즘을 적용하여 데드락 발생 0% 확립

#### 한줄 요약
- 은행원 알고리즘은 사전 요구량 선언과 안전 순서열 검증을 통해 데드락을 수학적으로 완벽히 회피하는 정밀 알고리즘이다.