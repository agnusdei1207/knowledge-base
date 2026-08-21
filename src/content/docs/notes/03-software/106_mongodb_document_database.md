---
sidebar:
  order: 106
  label: "106. MongoDB 문서 데이터베이스 (MongoDB Document Database)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "MongoDB 문서 데이터베이스 (MongoDB Document Database)"
date: "2026-08-17T23:20:00+09:00"
tags:
  - "notes-software"
weight: 106
extra:
  question_no: "106"
  source_status: "기출"
  source_history: "137회"
  priority: 30
  priority_note: "137회 기출, 문서 모델 제품 사례 성격"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **BSON 문서 모델(Binary JSON)**: JSON의 가독성과 계층적 중첩 구조를 유지하면서 이진 직렬화로 빠른 파싱과 다양한 데이터 타입을 지원하는 문서 형식.
- **다단계 JOIN 병목 및 스키마 변경 비용(Join Bottleneck & DDL Overhead)**: RDBMS의 복잡한 정규화 테이블 구조로 인해 연관 객체 조회 시 다중 조인이 발생하고 잦은 DDL 마이그레이션 부담이 초래되는 한계.

</details>

- 정의/개념: 가변 구조의 BSON 문서 형태로 데이터를 저장하고 **단일 문서 원자성, 복제 세트(HA) 및 샤딩(Scale-Out)을 지원**하는 NoSQL 문서 데이터베이스
- 배경/필요성: 복잡한 중첩 객체 조회 시 RDBMS의 정규화로 인한 **다단계 JOIN 연산 병목, 빈번한 스키마 DDL 변경 비용 및 수평 확장 한계** 직면

#### 한줄 요약

- BSON 문서 내포를 통해 조인 없이 중첩 데이터를 초고속 조회하고 복제 세트와 샤딩으로 가용성과 확장성을 보장

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **단일 문서 원자성(Single Document Atomicity)**: 복잡한 분산 락 없이 단일 문서 내부의 서브 필드 및 배열 수정에 대해 100% 원자적 트랜잭션을 보장하는 속성.
- **WiredTiger 스토리지 엔진**: B+Tree 기반으로 행 레벨 동시성 제어, 스냅샷 격리, 체크포인트 및 데이터 압축(Snappy)을 제공하는 MongoDB 기본 엔진.

</details>

- 도메인 객체를 자연스럽게 표현하는 **BSON 기반의 가변 스키마(Dynamic Schema)**
- 조인 없이 단일 쿼리로 연관 데이터를 인출하는 **문서 내포(Embedding) 최적화**
- 자동 장애 조치(Failover)를 지원하는 **Replica Set 및 분산 샤딩(Sharding) 아키텍처**

#### 한줄 요약

- 유연한 BSON 문서 모델과 WiredTiger 엔진을 통해 고성능 읽기/쓰기와 수평 확장을 지원

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Replica Set 및 Sharded Cluster**: 1개 Primary와 다수 Secondary로 구성된 복제 세트와 Mongos 라우터, Config Server, Shard Replica로 구성된 분산 클러스터.

</details>

```text
[ MongoDB 클러스터 아키텍처 구조도 ]

                       [ 클라이언트 애플리케이션 ]
                                    │
                                    ▼
                          [ Mongos 쿼리 라우터 ]
                                    │
                 ┌──────────────────┴──────────────────┐
                 ▼ (샤드 키 라우팅)                    ▼
     [ Shard 1 (Replica Set) ]             [ Shard 2 (Replica Set) ]
     ┌───────────────────────┐             ┌───────────────────────┐
     │ Primary ◄──► Secondary│             │ Primary ◄──► Secondary│
     └───────────────────────┘             └───────────────────────┘
                 ▲                                     ▲
                 └──────────[ Config Server ]──────────┘
```

선의 의미: Mongos 라우터가 Config Server의 메타데이터를 참조하여 각 샤드의 Replica Set으로 쿼리를 분기하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| BSON 문서 및 컬렉션 | 계층적 중첩 필드와 배열을 저장하는 **원자적 데이터 저장 단위** |
| WiredTiger 엔진 | 디스크 블록 압축, 메모리 캐시 관리, **행 레벨 잠금 및 저널링(WAL) 처리** |
| 복제 세트 (Replica Set) | Oplog 기반 데이터 복제 및 **Primary 장애 시 자동 선거(Election)로 무중단 절체** |
| 샤드 클러스터 (Mongos) | 샤드 키 기반으로 대용량 데이터를 **다중 노드에 수평 분산 라우팅** |

#### 한줄 요약

- BSON 문서 저장, WiredTiger 엔진, 복제 세트(HA), 샤드 클러스터(Scale-Out)로 구성된 아키텍처

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Replica Set 자동 선거 절차**: Primary 장애 $\to$ 하트비트 감지 $\to$ Raft 기반 선거 시작 $\to$ 과반수 투표 $\to$ 신규 Primary 승격.

</details>

```text
[ MongoDB Replica Set 자동 장애 복구 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. Primary 노드 장애 발생 (비정상 종료)│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Secondary 노드 간 하트비트 실패 감지│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Raft 기반 선거 시작: 투표 요청 전송 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 과반수 획득 노드 ➔ 신규 Primary 승격 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Mongos 라우터 토폴로지 갱신 및 재개 │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 장애 발생: Primary 노드의 하드웨어 결함이나 프로세스 비정상 종료 발생.
2. 하트비트 감지: Secondary 노드들이 2초 간격의 하트비트 응답 누락을 감지.
3. 선거 시작: 가장 최신 Oplog를 보유한 Secondary가 선거 임기(Term)를 올리고 투표를 요청.
4. 신규 Primary 승격: 과반수(Majority) 투표를 획득한 노드가 즉시 새로운 Primary로 승격.
5. 라우팅 갱신: 드라이버 및 Mongos 라우터가 토폴로지 변경을 감지하고 쓰기 트래픽을 신규 Primary로 재전송.

#### 한줄 요약

- 장애 발생 $\to$ 하트비트 감지 $\to$ 투표 수행 $\to$ Primary 승격 $\to$ 라우팅 갱신의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **내포(Embedded) vs 참조(Referenced)**: 연관 객체를 단일 문서 내에 배열로 포함하는 방식과 식별자(ID)로 분리 참조하는 방식.

</details>

| 구분 | 내포 패턴 (Embedded Document) | 참조 패턴 (Referenced Document) |
|:---|:---|:---|
| **적용 기준** | 1:1 관계 또는 유한한 크기의 1:N 관계 (배송지 목록) | 1:N 무한 증가 관계 (댓글 목록) 또는 N:M 관계 |
| **핵심 특징** | **단일 문서 내 서브 도큐먼트 내포, 조인 0회 단일 조회** | **별도 컬렉션 분리 후 `$lookup` 또는 애플리케이션 참조** |
| **한계** | 문서 크기 16MB 초과 위험 및 중복 데이터 갱신 오버헤드 | 다중 쿼리 실행 또는 `$lookup` 집계 파이프라인 오버헤드 |

#### 한줄 요약

- 함께 조회되고 크기가 유한하면 Embedded 패턴, 무한 증가하거나 다대다 관계이면 Referenced 패턴을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **16MB 문서 크기 한계**: MongoDB 단일 Document의 최대 허용 크기로, 배열이 끝없이 증가(Unbounded Array)할 경우 발생하는 치명적 에러.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 댓글/이력 배열 무한 성장으로 16MB 문서 제한 초과 | **댓글/이력 데이터를 별도 컬렉션으로 분리하는 Referenced 패턴 적용** | 16MB 에러 원천 방지 |
| 스키마리스 특성으로 인한 잘못된 데이터 형식 유입 | **JSON Schema Validation 규칙을 컬렉션에 적용하여 DB 레벨 검증** | 데이터 구조 무결성 유지 |
| Replica Set 복제 지연으로 인한 구버전 데이터(Stale) 조회 | **중요 비즈니스 쿼리에 `Read Concern: majority` 옵션 명시** | 최신성 보장 및 일관된 읽기 달성 |

#### 한줄 요약

- 참조 분리 설계, JSON Schema 검증, Read/Write Concern 설정을 통해 안정적인 문서 DB를 운용

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **도메인 주도 문서 모델링(Domain-Driven Document Sizing)**: 비즈니스 애그리게잇(Aggregate) 단위로 문서 경계를 설정하여 트랜잭션과 조회를 최적화하는 기법.

</details>

- **MongoDB 문서 데이터베이스** 기반 복잡한 비즈니스 엔티티를 가장 직관적으로 표현하는 고성능 NoSQL 솔루션이며, 도메인 경계에 맞춘 적절한 내포/참조 설계와 Replica Set 고가용성 구성을 통해 안정적인 데이터 플랫폼을 구축해야 함

#### 한줄 요약

- BSON 문서 내포와 복제·샤딩 클러스터를 통해 유연한 데이터 모델과 무중단 고가용성을 실현
