---
sidebar:
  order: 9
  label: "009. 교착상태 조건•예방•회피•탐지•복구 (Deadlock)"
  badge:
    text: "기출 • 85%"
    variant: note
title: 교착상태 조건•예방•회피•탐지•복구 (Deadlock)
date: "2026-08-13T13:05:00+09:00"
tags: [notes-software]
weight: 9
extra:
  question_no: "009"
  source_status: "기출"
  source_history: "131회, 132회, 134회"
  priority: 85
  priority_note: "131•132•134회 반복, 자원 할당 통제 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **교착상태(Deadlock)**: 두 개 이상의 프로세스/스레드가 서로 상대방이 점유한 자원(Resource/Lock)을 기다리며 영구적으로 블록(Blocked)되어 실행을 멈추는 상태.
- **Coffman 4대 조건**: 교착상태가 발생하기 위한 4가지 필수 충족 조건인 상호 배제(Mutual Exclusion), 점유와 대기(Hold & Wait), 비선점(No Preemption), 환형 대기(Circular Wait).

</details>

- 정의/개념: 실행 주체들이 서로의 자원을 기다려 진행하지 못하는 **교착상태**
- 배경/필요성: 독립적인 락 획득 순서는 **순환 대기**를 형성할 수 있음

#### 한줄 요약

- 상호배제, 점유대기, 비선점, 환형대기 4가지 필요조건이 동시 충족될 때 발생하는 정지 상태이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Mutual Exclusion (상호 배제)**: 자원은 한번에 한 프로세스만 독점 점유 가능한 속성.
- **Hold & Wait (점유와 대기)**: 최소 1개의 자원을 잡은(Hold) 상태에서 타 프로세스가 잡고 있는 자원을 대기(Wait)하는 속성.
- **No Preemption (비선점)**: 타 프로세스가 점유한 자원을 강제로 빼앗을(Preempt) 수 없는 속성.
- **Circular Wait (환형 대기)**: 프로세스 링($P_0 \to P_1 \to P_2 \to P_0$) 상에서 닫힌 순환 구조로 자원을 서로 대기하는 속성.

</details>

- **Coffman 4대 필요조건** 동시 성립 시 교착상태 발동
- 단일 인스턴스 자원은 **자원 할당 그래프** 순환으로 판정
- 예방(Prevention), 회피(Avoidance), 탐지(Detection), 복구(Recovery) 4단계 방어 전략

#### 한줄 요약

- 자원 할당 그래프 내의 Directed Cycle 형성이 교착상태 발생의 필요조건이 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Wait-for Graph**: 자원 할당 그래프에서 자원 노드를 제거하고 프로세스 간의 대기 방향(Edge)만을 간소화하여 사이클을 탐지하는 그래프.
- **Resource Allocation Graph (RAG)**: 프로세스 노드($P$)와 자원 노드($R$) 간의 점유(Assignment Edge) 및 요청(Request Edge) 관계를 표기하는 그래프.

</details>

```text
                 [자원 관리자]
                  /     |      \
        [예방 규칙] [안전성 검사] [대기 그래프]
                                      |
                                [복구 관리자]
```

선의 의미: 자원 관리자가 예방 규칙과 안전성 검사를 통해 자원을 디스패치하고, 런타임 대기 그래프 탐지를 통해 복구 관리자를 구동하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 자원 관리자 (Resource Manager) | 프로세스별 자원 요청/할당/반납 래칭 및 락 관리 |
| 예방 규칙 (Prevention Rules) | Coffman 4대 조건 중 최소 1개 이상을 시스템 설계 단계에서 무력화 |
| 안전성 검사 (Banker's Algorithm) | 동적 할당 시 **Safe State(안전 상태)** 유지 여부를 미리 계산하여 승인 |
| 대기 그래프 (Wait-for Graph) | DFS•강연결요소 분석으로 **대기 순환** 탐지 |
| 복구 관리자 (Recovery Manager) | 교착 포획 시 희생자(Victim) 프로세스 강제 종료 또는 Checkpoint Rollback |

#### 한줄 요약

- 예방 규칙과 안전성 검사 및 대기 그래프·복구 관리자를 결합한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Banker's Algorithm (은행가 알고리즘)**: 자원 요청 시 최악의 최대 자원 요구량(Max Claim)을 가정하여 Safe Sequence가 존재할 때만 할당을 승인하는 회피 기법.

</details>

```text
┌──────────────────────────────┐
│ 자원 할당 정책 설계         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 예방 가능성 판정         │
└───────┬──────────────────────┘
        ├─ 가능 ─▶ [2. 예방 적용]
        │ 불가
        ▼
┌──────────────────────────────┐
│ 3. 회피 가능성 판정         │
└───────┬──────────────────────┘
        ├─ 최대 요구량 파악 가능
        │            └─▶ [4. 회피 적용]
        │ 파악 불가
        ▼
┌──────────────────────────────┐
│ 5. 탐지•복구 적용           │
│ 순환 탐지 후 종료•롤백      │
└──────────────────────────────┘
```

### 동작 원리

1. **예방 가능성 판정**: Coffman 4대 조건 사전 박탈 가능성 검증 (**Prevention**).
2. **예방 적용**: Lock Ordering 적용으로 **Circular Wait** 사전 방지.
3. **회피 가능성 판정**: 최대 요구량(Max Claim) 정보 파악 가능 여부 확인 (**Avoidance**).
4. **회피 적용**: **Banker's Algorithm**을 활용한 Safe State 유지 자원 승인.
5. **탐지·복구 적용**: 미파악 환경에서 **Wait-for Graph** 사이클 탐지 및 Victim Kill 복구.

#### 한줄 요약

- 예방 -> 회피 -> 탐지 & 복구 순으로 전략을 결정한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Safe State vs Unsafe State**: 모든 프로세스가 마감까지 완료될 수 있는 안전 순서(Safe Sequence)의 존재 유무 상태.

</details>

| 비교 항목 | 예방 (Prevention) | 회피 (Avoidance) | 탐지 및 복구 (Detection & Recovery) |
|:---|:---|:---|:---|
| 접근 방식 | 4대 조건 중 1개 사전 제어 | 동적 자원 요청 시 **Safe State** 계산 | 런타임 교착 포획 후 사후 해제 |
| 구현 기법 | **Lock Ordering** (환형 대기 제거) | **Banker's Algorithm** (은행가) | **Wait-for Graph** / Process Kill |
| 자원 활용률 | 사전 제약으로 낮아질 수 있음 | 안전 상태 범위 내 할당 | 평시 제약이 적음 |
| 오버헤드 | 규칙 준수와 동시성 제약 | 요청별 안전성 계산 | 탐지 주기와 복구 비용 |

#### 한줄 요약

- Lock Order Enforcement는 예방, Max Resource Claim 파악은 회피를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Lock Ordering (Hierarchical Locking)**: 자원(락)에 고유 번호를 부여하고 항상 오름차순 번호 순서로만 락을 획득하게 강제하여 Circular Wait를 무력화하는 기법.
- **Lock Timeout (tryLock)**: 락 획득 시 무한 대기 대신 타임아웃(예: 3초)을 인가하여 Hold & Wait를 끊어내는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 락 획득 순서 불일치로 인한 **Circular Wait** 발생 | **Lock Ordering (오름차순 락 획득)** 강제 | 교착상태 예방(Prevention) |
| 특정 락 무한 대기로 인한 시스템 마비 | **tryLock(timeout)** 시간 제한 인가 | Hold & Wait 조건 차단 |
| 분산 환경에서 멀티 노드 간 교착 발생 | **Fencing Token** 및 Distributed Lock Lease 적용 | 분산 락 교착 사후 해제 |

> 사례: RDBMS(PostgreSQL/MySQL) 내 **Wait-for Graph** 기반 런타임 Deadlock Detector 및 Victim Rollback

#### 한줄 요약

- Lock Hierarchy/전역 잠금 획득 순서를 통한 예방과 Lock Timeout/펜싱 토큰 기반 분산 교착상태 복구 기법을 적용한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **교착상태 대응 선택 기준(Deadlock Trade-off Criteria)**: 자원 이용률 목표, 최대 요구량 파악 가능성, 시스템 롤백 허용성에 근거한 수립 체계.

</details>

- **교착상태 대응 선택 기준**에 따라 멀티스레드 애플리케이션 개발 시 **Lock Ordering 예방** 및 DB 인프라는 **탐지/복구 엔진** 채택

#### 한줄 요약

- Control Overhead vs Resource Utilization Trade-off 분석에 의거하여 예방, 회피, 탐지/복구 기법을 산정한다.
