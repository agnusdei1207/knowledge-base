---
sidebar:
  order: 115
  label: "115. NewSQL: CockroachDB·Spanner (NewSQL)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "NewSQL: CockroachDB·Spanner (NewSQL)"
date: "2026-08-02T12:00:00+09:00"
tags:
  - "notes-software"
weight: 115
extra:
  question_no: "115"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "일관성·확장성을 결합한 분산 SQL 현안"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **뉴SQL(NewSQL) 데이터베이스**: 구조화 질의 언어(Structured Query Language, SQL)와 원자성·일관성·격리성·지속성(Atomicity, Consistency, Isolation, Durability, ACID)을 유지하면서 합의 복제와 키 범위 분할로 수평 확장하는 데이터베이스이다.

</details>

- 정의/개념: 관계형 구조화 질의 언어(Structured Query Language, SQL)·원자성·일관성·격리성·지속성(Atomicity, Consistency, Isolation, Durability, ACID) 트랜잭션을 유지하면서 분산 합의와 데이터 분할로 수평 확장하는 **뉴SQL(NewSQL) 데이터베이스** 계열
- 배경/필요성: 단일 노드 관계형 DB는 저장·처리 용량이 **한 장비 한계** 에 종속

#### 한줄 요약
- SQL 장부를 지점에 나누고 합의로 하나의 거래처럼 처리한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **합의 복제**: 범위별 복제본이 변경 로그 순서와 확정 지점에 동의하는 특성이다.
- **분산 실행**: 구조화 질의 언어(Structured Query Language, SQL) 연산을 키 범위별로 나누고 여러 노드의 중간 결과를 병합하는 방식이다.
- **분산 거래**: 여러 키 범위의 읽기·쓰기를 하나의 원자성·일관성·격리성·지속성(Atomicity, Consistency, Isolation, Durability, ACID) 트랜잭션으로 확정하는 방식이다.

</details>

- **분산 실행**: SQL을 범위 연산으로 분할·병합
- **합의 복제**: 범위별 변경 순서·확정점 합의
- **분산 거래**: 여러 범위 쓰기를 원자 확정

#### 한줄 요약
- 확장과 ACID를 함께 제공하지만 합의 왕복과 재시도 비용이 생긴다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **트랜잭션 조정자**: 충돌과 여러 키 범위에 걸친 원자적 커밋을 조정하는 구성요소이다.
- **구조화 질의 언어(Structured Query Language, SQL) 게이트웨이**: 질의를 분석하고 키 범위별 분산 계획과 결과 병합을 수행하는 접점이다.
- **범위 디렉터리**: 키 범위와 합의 복제 그룹 및 현재 리더 위치를 제공하는 구성요소이다.
- **합의 복제 그룹**: 범위별 변경 로그 순서와 내구성 확정점에 동의하는 복제본 묶음이다.
- **다중 버전 동시성 제어(Multi-Version Concurrency Control, MVCC)·분산 시계**: 데이터 버전 가시성과 전역 직렬 순서를 관리하는 구성요소이다.

</details>

```mermaid
block
  columns 3
  A["NewSQL 경계"]:3
  G["SQL 게이트웨이"]
  D["범위 디렉터리"]
  C["트랜잭션 조정자"]
  R["합의 복제 그룹"]
  M["MVCC·분산 시계"]
  G --- D
  G --- C
  C --- R
  C --- M
```

| 구성요소 | 책임 |
|:---|:---|
| 구조화 질의 언어(Structured Query Language, SQL) 게이트웨이 | **질의 분석·분산 계획·병합** |
| 범위 디렉터리 | **범위·리더 위치** 제공 |
| 트랜잭션 조정자 | 충돌과 **교차 범위 커밋** 조정 |
| 합의 복제 그룹 | **로그 순서·내구성** 합의 |
| 다중 버전 동시성 제어(Multi-Version Concurrency Control, MVCC)·분산 시계 | **가시성·직렬 순서** 관리 |

#### 한줄 요약

- SQL 접수자, 위치표, 거래 조정자, 합의 사본, 순서 시계로 구성된다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **3. 범위별 실행 계획**: 구조화 질의 언어(Structured Query Language, SQL) 연산을 담당 키 구간별 분산 트랜잭션으로 나누는 단계이다.
- **구조화 질의 언어(Structured Query Language, SQL) 트랜잭션 요청**: 응용이 원자적으로 처리할 관계형 읽기·쓰기 요청이다.
- **1. 키 범위**: 게이트웨이가 질의 조건에서 추출해 범위 디렉터리에 전달한 대상 키 구간이다.
- **2. 범위·리더 위치**: 디렉터리가 반환한 합의 복제 그룹과 현재 처리 리더 주소이다.
- **4. 합의 로그 항목**: 조정자가 원자 커밋을 위해 각 복제 그룹에 전달한 변경 기록이다.

</details>

```mermaid
sequenceDiagram
    participant A as 애플리케이션
    participant G as SQL 게이트웨이
    participant D as 범위 디렉터리
    participant C as 트랜잭션 조정자
    participant R as 합의 복제 그룹
    A->>G: SQL 트랜잭션 요청
    G->>D: 1. 키 범위
    D-->>G: 2. 범위·리더 위치
    G->>C: 3. 범위별 실행 계획
    C->>R: 4. 합의 로그 항목
    R-->>C: 복제·충돌 결과 반환
    C-->>A: 원자적 커밋 결과
```

**동작 원리**

1. **키 범위**: 게이트웨이가 디렉터리에 대상 키 구간 전달
2. **범위·리더 위치**: 디렉터리가 복제 그룹과 현재 리더 반환
3. **범위별 실행 계획**: 구조화 질의 언어(Structured Query Language, SQL) 연산을 분산 트랜잭션으로 분해
4. **합의 로그 항목**: 조정자가 변경 로그를 복제 그룹에 전달

#### 한줄 요약

- SQL을 담당 구간에 나누어 보내고 모든 구간의 사본 확인 뒤 하나의 거래로 확정한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **CockroachDB**: Range·Raft·하이브리드 논리 시계(Hybrid Logical Clock, HLC)로 분산 구조화 질의 언어(Structured Query Language, SQL) 트랜잭션을 제공하는 뉴SQL(NewSQL) 제품이다.
- **Spanner**: Split·Paxos·TrueTime으로 글로벌 분산 SQL 트랜잭션을 제공하는 관리형 NewSQL 제품이다.

</details>

| 뉴SQL(NewSQL) 제품 | CockroachDB | Spanner |
|:---|:---|:---|
| 적용 기준 | **배포 선택·지역성 제어** | **글로벌 관리형 운영** |
| 핵심 특징 | **Range·Raft·하이브리드 논리 시계(Hybrid Logical Clock, HLC)** | **Split·Paxos·TrueTime** |
| 한계 | **배치·재시도·운영 책임** | **리전 지연·서비스 종속** |

#### 한줄 요약

- 둘 다 분산 SQL 거래를 제공하지만 배포 방식과 범위 배치·시간 순서 구현이 다르다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **분포·분할·지역성 부하 시험**: 실제 키 편중과 범위 분할 및 사용자와 리더의 거리를 재현해 핫스팟을 확인하는 시험이다.
- **동시 갱신 행의 지역 배치**: 한 거래에서 함께 바꾸는 데이터를 같은 지역에 둬 교차 리전 합의를 줄이는 방식이다.
- **짧은 거래·멱등 재시도**: 잠금·충돌 구간을 줄이고 직렬화 실패를 중복 효과 없이 다시 처리하는 통제이다.
- **생존·읽기·쓰기 지역 분리**: 장애 시 유지할 복제 위치와 조회·커밋을 처리할 지역을 업무별로 정하는 기준이다.
- **노드·리전 훈련과 복구 시간 목표(Recovery Time Objective, RTO) 측정**: 장애를 실제 주입해 정족수 유지와 서비스 복구 시간을 검증하는 활동이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 순차·편향 키로 특정 범위에 쓰기 집중 | 분포·분할·지역성 부하 시험 | **핫스팟** 방지 |
| 함께 갱신할 행이 여러 리전에 분산 | 동시 갱신 행을 같은 지역 배치 | **합의 왕복** 감소 |
| 긴 거래가 같은 키를 반복 점유 | 짧은 거래·멱등 재시도 | **충돌·중단** 감소 |
| 쓰기 리더와 사용자의 거리가 증가 | 생존·읽기·쓰기 지역 분리 | **커밋 지연** 통제 |
| 리전 상실로 정족수와 복구시간 불명확 | **노드·리전 훈련과 복구 시간 목표(Recovery Time Objective, RTO) 측정** | **정족수 상실** 대응 |

#### 한줄 요약

- 함께 바꾸는 데이터를 가까이 두어 여러 지역을 오가는 합의 횟수를 줄인다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **뉴SQL(NewSQL)**: 수평 확장과 원자성·일관성·격리성·지속성(Atomicity, Consistency, Isolation, Durability, ACID) 트랜잭션이 함께 필요한 업무에 적합한 데이터베이스이다.
- **단일 노드 데이터베이스**: 단일 지역 거래와 낮은 분산 조정 비용이 중요한 업무에 적합한 데이터베이스이다.

</details>

- 수평 확장과 원자성·일관성·격리성·지속성(Atomicity, Consistency, Isolation, Durability, ACID)이 함께 필요하면 **뉴SQL(NewSQL)** 선택, 단일 지역 거래에는 **단일 노드 데이터베이스** 선택

#### 한줄 요약

- 장부를 나눠도 한 거래로 맞출 수 있지만 멀리 있는 지점과의 합의 시간은 반드시 치러야 한다.
