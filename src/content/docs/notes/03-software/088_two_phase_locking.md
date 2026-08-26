---
sidebar:
  order: 88
  label: "088. 2단계 잠금 프로토콜 2PL"
  badge:
    text: "미출 · 30%"
    variant: note
title: "락 관리: 2단계 잠금 프로토콜 (Two-Phase Locking, 2PL)"
date: "2026-08-27T01:24:00+09:00"
tags:
  - "notes-software"
weight: 88
extra:
  question_no: "088"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "2PL은 직렬성•교착상태 절충의 기본 기법"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **2PL(Two-Phase Locking Protocol)**: 트랜잭션 내의 잠금(Lock) 과정을 성장 단계(Growing)와 축소 단계(Shrinking)로 나누어 직렬 가능성을 보장하는 동시성 제어 프로토콜.
- **성장 단계 vs 축소 단계**: 락을 획득만 할 수 있는 단계(Growing)와 락을 해제만 할 수 있는 단계(Shrinking).

</details>

- 정의/개념: 트랜잭션의 락 획득(Growing)과 락 해제(Shrinking)를 분리하여 **트랜잭션의 충돌 직렬 가능성(Conflict Serializability)을 보장**하는 규약
- 배경/필요성: 무질서한 락 획득 및 조기 해제로 인한 **비직렬 실행 결과 왜곡 및 연쇄 롤백(Cascading Rollback) 발생 해결 불가**

#### 한줄 요약
- 락을 획득하는 동안에는 해제하지 않고, 해제하기 시작하면 새 락을 획득하지 않는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lock Point**: 트랜잭션이 마지막 락을 획득하여 성장 단계가 끝나고 축소 단계로 전환되는 임계 시점.
- **Cascading Rollback(연쇄 롤백)**: 트랜잭션이 조기 해제한 언커밋 데이터를 읽은 타 트랜잭션들이 원본 롤백 시 줄줄이 취소되는 현상.

</details>

- 직렬 스케줄과 동일한 결과를 보장하는 **충돌 직렬 가능성(Conflict Serializability) 완벽 보장**
- 락을 얻기만 하는 **성장 단계(Growing)** 와 락을 풀기만 하는 **축소 단계(Shrinking)** 의 엄격 분리
- 트랜잭션 간 자원 교차 대기로 인한 **교착 상태(Deadlock) 발생 가능성 상존**

#### 한줄 요약
- 직렬 가능성을 보장하되 교착 상태(Deadlock)와 연쇄 롤백 위험을 통제해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Lock Manager & Wait-for Graph**: 잠금 상태를 관리하는 테이블과 교착 상태를 감지하기 위해 트랜잭션 대기 관계를 추적하는 방향 그래프.

</details>

| 구성요소 | 책임 |
|:---|:---|
| 확장 단계 (Growing Phase) | 트랜잭션 실행에 필요한 **공유 락(S-Lock) 및 배타 락(X-Lock)을 점진 획득** |
| Lock Point | 트랜잭션이 **마지막 락을 획득하고 축소 단계로 진입하기 직전의 시점** |
| 축소 단계 (Shrinking Phase) | 트랜잭션이 **보유한 락을 점진 해제(Unlock)** |
| 교착 탐지기 (Deadlock Detector) | Wait-for Graph 순환 탐색으로 **교착 상태 발견 시 Victim 트랜잭션 롤백** |

#### 한줄 요약
- 확장 단계, Lock Point, 축소 단계와 교착 탐지기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Strict 2PL vs Rigorous 2PL**: 배타 락(X)만 커밋 시점에 해제하는 Strict 2PL과 모든 락(S+X)을 커밋 시점까지 유지하는 Rigorous 2PL.

</details>

```text
트랜잭션 시작
        │
   [Growing Phase] 레코드 A에 대한 S-Lock 및 레코드 B에 대한 X-Lock 획득
        │
   [Lock Point 도달] 필요한 모든 락 획득 완료 (이후 신규 락 획득 불가)
        │
   [어떤 2PL 변형 프로토콜을 사용하는가?]
   ┌────┼───────────────────────────┐
[Basic 2PL]                    [Strict 2PL (상용 DB 표준)]   [Rigorous 2PL]
중간에 락을 하나씩 해제          X-Lock은 Commit 시까지 유지    모든 S/X-Lock을 Commit 시까지 유지
(연쇄 롤백 위험 존재)           (연쇄 롤백 완전 차단)          (완벽한 직렬화 보장)
        │                               │                             │
   트랜잭션 Commit 완료 및 남은 모든 락 일괄 해제
```

#### 한줄 요약
- 성장 단계 → Lock Point 도달 → Strict 2PL(커밋 시 X-Lock 해제) → 트랜잭션 완료 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **2PL 3대 변형**: Basic 2PL(조기 해제), Strict 2PL(X-Lock 커밋 시 해제), Rigorous 2PL(모든 락 커밋 시 해제).

</details>

| 비교 항목 | Basic 2PL (기본 2PL) | Strict 2PL (엄격한 2PL) | Rigorous 2PL (강력한 2PL) |
|:---|:---|:---|:---|
| X-Lock 해제 시점 | 축소 단계에서 조기 해제 가능 | **트랜잭션 Commit / Rollback 시점** | **트랜잭션 Commit / Rollback 시점** |
| S-Lock 해제 시점 | 축소 단계에서 조기 해제 가능 | 축소 단계에서 조기 해제 가능 | **트랜잭션 Commit / Rollback 시점** |
| 충돌 직렬성 보장 | **100% 보장** | **100% 보장** | **100% 보장** |
| 연쇄 롤백(Cascading) | **발생 가능 (미커밋 노출)** | **완전 차단 (Safe)** | **완전 차단 (Safe)** |
| 상용 DBMS 채택 | 거의 미사용 | **Oracle, MySQL 등 상용 DB 표준** | 특수 고신뢰성 시스템 |

#### 한줄 요약
- 기본형은 연쇄 롤백 위험이 있어, 실무 상용 DBMS는 배타 락을 커밋까지 유지하는 Strict 2PL을 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Deadlock(교착 상태)**: 트랜잭션 A가 B의 자원을, 트랜잭션 B가 A의 자원을 동시에 기다리며 영원히 멈추는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 2PL 수행 중 트랜잭션 간 상호 대기로 교착 상태(**Deadlock**) 발생 | **Wait-for Graph 기반 1초 주기 교착 감지 및 짧은 Lock Timeout 설정** | 무한 대기 차단 및 희생자(Victim) 자동 롤백 |
| Basic 2PL의 조기 해제로 인한 연쇄 롤백(**Cascading Rollback**) | **상용 DBMS 기본값인 Strict 2PL (X-Lock Commit 시점 해제) 강제** | 연쇄 롤백 0화 및 회복 가능성(Recoverability) 보장 |
| 락 점유 시간 장기화로 인한 동시 처리량(TPS) 폭락 | **읽기 작업에 대해 2PL 대신 MVCC(Undo 스냅샷) 엔진 채택** | 읽기-쓰기 블로킹 해소 및 처리량 10배 향상 |
| 다중 행 수정 시 데드락 빈발 | **애플리케이션에서 레코드 ID 오름차순(ASC)으로 정렬 후 Lock 획득** | 순환 대기 조건(Circular Wait) 원천 제거 |

#### 한줄 요약
- Strict 2PL 적용, Wait-for Graph 교착 감지, MVCC 병행, 자원 정렬 잠금으로 문제를 해결한다.

## Ⅶ. 결론

- 직렬 가능성은 **Strict 2PL**, 교착 예방은 **자원 순서화** 선택

#### 한줄 요약
- 2단계 잠금 프로토콜(2PL)은 트랜잭션 직렬 가능성을 보장하는 핵심 이론이며, 실무에서는 연쇄 롤백을 막는 Strict 2PL이 표준으로 사용된다.
