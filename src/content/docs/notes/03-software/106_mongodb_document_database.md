---
sidebar:
  order: 106
  label: "106. MongoDB 문서 데이터베이스 (MongoDB Document Database)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "MongoDB 문서 데이터베이스 (MongoDB Document Database)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **MongoDB**: JSON/BSON(Binary JSON) 문서 형태의 가변 데이터 모델(Document Model)을 사용하는 대표적인 범용 오픈소스 NoSQL 문서 데이터베이스.
- **BSON (Binary JSON)**: JSON 구조의 유연성을 유지하면서, 이진(Binary) 직렬화를 통해 빠르게 파싱하고 추가적인 데이터 타입(Date, 64-bit Int 등)을 인덱싱 지원하는 바이너리 문서 형식.
- **Replica Set & Sharding**: 1개의 Primary 노드와 n개의 Secondary 노드로 고가용성(HA)을 보장하는 Replica Set, 및 Config Server + Mongos 라우터를 기반으로 수평 확장(Scale-Out)하는 Sharding 아키텍처.

</details>

- **정의**: JSON/BSON(`Binary JSON`) 형태의 가변 데이터 모델을 사용하여 데이터를 단일 문서(`Single Document`) 단위로 적재하고 조인 없는 쿼리를 지원하는 Document NoSQL인 **MongoDB**.
- **필요성**: RDBMS의 복잡한 정규화 및 `JOIN` 병목 극복, 구조가 잦게 변하는 데이터(상품 카탈로그, CMS)의 유연한 적재 및 수평 분산 요구성.

#### 한줄 요약

- 함께 쓰는 상품 정보와 속성을 한 묶음 문서로 저장하는 데이터베이스이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Single Document Atomicity**: RDBMS의 다중 테이블 ACID 트랜잭션 대신, 단일 문서(Document) 내부의 서브 필드/배열 수정에 대해 100% 원자성(Atomicity) 보장.
- **Dynamic Schema**: 사전 `ALTER TABLE` DDL 없이 컬럼(필드)을 자유롭게 추가/수정 가능.

</details>

- **BSON 기반 모델링**: 데이터 내포(`Embedding`) 지원으로 데이터 접근성 최적화.
- **원자성 보장**: 단일 문서(`Single Document`) 수준에서 100% 원자성(Atomicity) 제공.
- **운영 엔진**: `WiredTiger` 엔진(B+Tree 기반, 행 레벨 락, 데이터 압축) 및 `Replica Set`/`Sharding` 지원.

#### 한줄 요약

- 함께 쓰는 정보는 묶되 끝없이 커지거나 자주 중복되는 정보는 분리해야 한다.

## Ⅲ. 구조 및 구성요소 (MongoDB 아키텍처 및 3대 데이터 모델링)

<details><summary>핵심 용어</summary>

- **Embedded vs Referenced**: 서브 문서로 내포(Embedded)하여 조인 0회를 달성할 것인가, DBRef 식별자로 참조(Referenced)하여 데이터를 쪼갤 것인가의 데이터 모델링 선택.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        MongoDB Document Modeling                       │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Embedded Document Pattern      │ 2. Referenced Document Pattern     │
├───────────────────────────────────┼────────────────────────────────────┤
│ {                                 │ {                                  │
│   _id: 101,                       │   _id: 101,                        │
│   name: "홍길동",                 │   name: "홍길동",                  │
│   address: { city: "SEOUL" }      │   address_id: 901  (Reference FK)  │
│ } (1번의 I/O로 조인 없이 인출)    │ } (독립적 수명주기, JOIN 필요)     │
└───────────────────────────────────┴────────────────────────────────────┘
```

선의 의미: 데이터의 수명주기 및 접근 패턴에 따라 Embedded(내포) 패턴 또는 Referenced(참조) 패턴을 선택하는 MongoDB 아키텍처.

| 구조 요소 | 역할 및 핵심 기능 | 실무 적용 고려사항 |
|:---|:---|:---|
| **BSON Document** | 개별 데이터 저장 단위 (최대 16MB 용량 한계) | 16MB 초과 시 GridFS 사용 필요 |
| **Collection** | RDBMS의 Table에 대응되는 문서들의 집합체 | 가변 스키마 문서 수용 공간 |
| **WiredTiger Engine** | B+Tree 기반 스토리지 엔진 (메모리 60% 캐싱) | Document Level Concurrency 제어 |
| **Replica Set** | Primary 1개 + Secondary n개 + Oplog 동기화 | **Poin-In-Time Failover & High Availability** |

#### 한줄 요약

- 문서 보관함과 색인, 사본 묶음, 안내자, 위치표로 구성된다.

## Ⅳ. 흐름도 (MongoDB Replica Set Failover 메커니즘)

<details><summary>핵심 용어</summary>

- **Oplog (Operations Log)**: Primary 노드의 모든 CUD 데이터 변경 사항이 시계열 이진 기록으로 남는 특수 캡드 컬렉션(Capped Collection)으로, Secondary 노드가 이를 릴레이 복제.

</details>

```text
[Primary Node Down!] ──► [Secondary Nodes Heartbeat Timeout]
                                    │
                                    ▼
       [Raft/Paxos 기반 Leader Election (투표 1초 만에 완료)]
                                    │
                                    ▼
       [가장 최신 Oplog 보유 Secondary 가 신규 Primary 로 승격 완료!]
```

### 동작 원리

1. **Heartbeat Audit**: 2초 주기로 노드 간 핑(Ping) 체크.
2. **Election Trigger**: Primary가 10초간 응답 없을 경우 Secondary 노드들이 투표(Election) 개시.
3. **Failover Execution**: 가장 최신 Oplog 포인터를 가진 Secondary가 과반수 표를 얻어 신규 Primary로 즉시 승격.

#### 한줄 요약

- 안내자가 문서의 담당 샤드와 원본을 찾아 저장하고 요구한 사본 확인 뒤 응답한다.

## Ⅴ. 종류 및 비교 (Embedded Pattern vs Referenced Pattern)

<details><summary>핵심 용어</summary>

- **Data Modeling Tradeoff**: Embedded는 조인이 없어 조회가 압도적으로 빠르나 문서 크기가 커지고 무한 성장 시 16MB 제한 도달, Referenced는 문서 크기가 작고 중복이 없으나 조인(`$lookup`) 연산 오버헤드 발생.

</details>

| 비교 항목 | Embedded Document Pattern (내포) | Referenced Document Pattern (참조) |
|:---|:---|:---|
| 데이터 결합 방식 | **단일 BSON 문서 내 서브 문서/배열 내포** | **`$lookup` 또는 앱 단 식별자 참조 결합** |
| `JOIN` 발생 횟수 | **0회 (단일 디스크 I/O 완결)** | 1회 이상 (RDBMS 조인과 유사) |
| 데이터 갱신 오버헤드| 데이터 중복 시 연쇄 수정 필요 | 단일 위치 갱신으로 무결성 우수 |
| 적합 데이터 유형 | **1:1 또는 1:N 유한한 서브 데이터 (주소 등)**| **1:N 무한 성과, N:M 복잡 다대다 데이터** |

#### 한줄 요약

- 항상 함께 쓰면 한 문서에 넣고 따로 커지거나 자주 공유하면 참조로 나눈다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **16MB Document Limit**: MongoDB 단일 Document의 최대 크기 한계로, 배열이 무한 성장(Unbounded Array)하면 16MB 에러가 나므로 분리 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 댓글 배열이 무한 성장하여 16MB 문서 제한 초과 | **댓글은 Referenced 패턴으로 별도 Collection 분리** | 16MB 제한 에러 방지 |
| Schema-Less 특성으로 무분별한 필드 파행 발생 | **JSON Schema Validation 도입으로 필수 필드 DB 레벨 검증**| 데이터 유효성 보존 |
| 복제 지연 시 읽기 불일치 발생 | **Read Concern / Write Concern 옵션 (`majority`) 강제** | 강한 일관성 달성 |

> 사례: **E-Commerce 상품-옵션 내포(Embedded) 모델링 및 MongoDB Replica Set 튜닝**

#### 한줄 요약

- 한 번에 읽을 정보는 묶되 끝없이 늘어나는 목록과 여러 곳에서 공유하는 정보는 분리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **MongoDB 모델 수립 기준(MongoDB Architecture Standards)**: BSON 내포 구조 적합성, 16MB 한계 준수 및 Replica Set HA 구성에 의거한 체계.

</details>

- **MongoDB 모델 수립 기준 적용** (가변 스키마 카탈로그/CMS 구축 시 `BSON Embedded Model` 및 `WiredTiger Engine` 필수 수용)

#### 한줄 요약

- MongoDB 모델 적용 기준은 함께 쓰는 자료의 문서 경계와 자주 찾는 분산 키를 맞춘다.
