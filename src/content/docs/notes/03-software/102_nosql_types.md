---
sidebar:
  order: 102
  label: "102. NoSQL 유형: 문서•키값•컬럼•그래프 (NoSQL Types)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "NoSQL 유형: 문서•키값•컬럼•그래프 (NoSQL Types)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 102
extra:
  question_no: "102"
  source_status: "기출"
  source_history: "131회, 137회"
  priority: 70
  priority_note: "131•137회 반복, NoSQL 유형 선택 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **NoSQL (Not Only SQL)**: 관계형 데이터베이스(RDBMS)의 엄격한 테이블 스키마, `JOIN` 오버헤드, 수평 확장(Scale-Out)의 한계를 극복하기 위해, 데이터 모델과 접근 패턴에 맞춰 고안된 4대 비관계형 데이터베이스 분류 체계 (Document, Key-Value, Wide-Column, Graph).
- **Schema-Flexibility (가변 스키마)**: 튜플(행)마다 저장되는 속성(컬럼)이 달라지더라도 사전 DDL 정의 없이 자유롭게 데이터를 인서트 및 확장할 수 있는 속성.
- **Polyglot Persistence (폴리글랏 퍼시스턴스)**: 하나의 소프트웨어 시스템 안에서 단일 DB에 의존하지 않고, 데이터의 성격(세션, 검색, 그래프, 트랜잭션)에 맞춰 적재적소의 NoSQL 및 RDBMS 엔진을 혼용하여 구축하는 아키텍처 사상.

</details>

- 정의/개념: 대용량 데이터의 수평 확장성(Scale-Out)과 가변 스키마(Schema-Flexibility)를 지원하기 위해 데이터 표현 방식에 따라 4대 유형으로 특화 분류된 비관계형 데이터베이스 기술인 **NoSQL Types**
- 배경/필요성: 빅데이터 및 비정형 데이터(JSON, 그래프, 시계열) 폭증, RDBMS의 `JOIN` 및 고정 스키마로 인한 수평 분산 제약 극복 요구성

#### 한줄 요약

- 모든 데이터를 같은 테이블에 넣지 않고 문서, 키-값, 와이드 컬럼, 그래프 중 접근 패턴에 맞는 데이터 모델을 고른다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Query-Driven Data Modeling (쿼리 중심 데이터 모델링)**: RDBMS처럼 정규화(Normalization)를 먼저 하지 않고, 애플리케이션의 화면 조회 쿼리(Query Pattern)에 맞춰 중복을 허용(Denormalization)하여 테이블을 설계하는 특성.
- **BASE Consistency Model**: Strictly ACID 대신 Basically Available, Soft-state, Eventual Consistency(최종 일관성) 모델 채택.

</details>

- **Horizontal Scale-Out (수평 분산 노드 확장성 최적화)**
- **Schema-Less / Dynamic Schema (가변적 비정형 구조 수용)**
- **Query-Driven Modeling (조회 패턴 중심 데이터 설계)** 및 **Polyglot Persistence** 수용

#### 한줄 요약

- 자주 묻는 질문에는 빠르게 답하지만 다른 형태의 질문은 어렵기 때문에 조회 방식부터 정하고 모델을 선택해야 한다.

## Ⅲ. 구조 및 구성요소 (NoSQL 4대 핵심 데이터 모델 아키텍처)

<details><summary>핵심 용어</summary>

- **Key-Value Store**: Unique Key 1개에 BSON/String/Binary Value를 1:1 매핑하는 극단적 단순 구조 (Redis, DynamoDB).
- **Document Store**: JSON/BSON 형태의 중첩된 서브 문서(Sub-document) 및 배열 구조를 인덱싱하여 다루는 모델 (MongoDB, Couchbase).
- **Wide-Column Store**: Row Key, Column Family, Column Name, Timestamp 구조의 4차원 희소(Sparse) 행렬 데이터 모델 (Cassandra, HBase).
- **Graph Store**: Node(정점), Edge(간선), Property(속성) 구조로 복잡한 네트워크 소셜 관계를 지향하는 모델 (Neo4j).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        NoSQL 4대 대표 데이터 모델                      │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Key-Value      │ 2. Document       │ 3. Wide-Column                 │
│   Key ──► Value   │   JSON Document   │   RowKey ──► Column Family     │
│   (Redis)         │   (MongoDB)       │   (Cassandra)                  │
├───────────────────┴───────────────────┴────────────────────────────────┤
│ 4. Graph Store (Node ──[Edge]──► Node) (Neo4j)                        │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터의 복잡도와 조인/관계 표현성에 따라 Key-Value, Document, Wide-Column, Graph 4개 축으로 분류되는 아키텍처.

| NoSQL 유형 (Type) | 대표 데이터베이스 | 데이터 저장 모델 구조 | 주요 사용 적합 도메인 |
|:---|:---|:---|:---|
| **Key-Value Store** | **Redis, Memcached, DynamoDB** | **`Key -> Value` 단순 1:1 구조** | **세션 저장소, 랭킹 리더보드, 인메모리 캐시** |
| **Document Store** | **MongoDB, Couchbase** | **JSON / BSON 복합 중첩 문서 구조** | **E-Commerce 상품 카탈로그, CMS 콘텐츠** |
| **Wide-Column Store**| **Apache Cassandra, HBase** | **`RowKey -> ColumnFamily -> Column`** | **IoT 센서 시계열, 대규모 분산 타임라인** |
| **Graph Store** | **Neo4j, Amazon Neptune** | **`Node(정점) - Edge(간선) - Property`**| **소셜 네트워크(SNS 친구), 추천 엔진, 챗봇** |

#### 한줄 요약

- 질문 형태에 맞는 보관함과 조회 방법, 사본 규칙을 묶는다.

## Ⅳ. 흐름도 (Polyglot Persistence 다중 NoSQL 적재 흐름)

<details><summary>핵심 용어</summary>

- **Polyglot Architecture**: 단일 서비스 시스템 내에서 세션은 Redis, 카탈로그는 MongoDB, 결제는 RDBMS, 친구추천은 Neo4j에 분산 적재하는 아키텍처.

</details>

```text
                               [Web Application Service]
                                           │
         ┌───────────────────┬─────────────┼─────────────┬───────────────────┐
         ▼                   ▼             ▼             ▼                   ▼
  [Key-Value: Redis] [Document: MongoDB] [RDBMS: MySQL] [Column: Cassandra] [Graph: Neo4j]
  (Session / Cache)  (Product Catalog)   (Payment/ACID) (IoT Time-Series)   (Recommendation)
```

### 동작 원리

1. **Session & Caching**: 초고속 1ms 응답이 필요한 세션 및 랭킹 데이터는 **Redis (Key-Value)** 로 처리.
2. **Product Catalog**: 구조가 자주 바뀌는 상품 정보 및 상품 옵션은 **MongoDB (Document)** 로 저장.
3. **Payment Transaction**: 100% Strict ACID 결제 데이터는 **MySQL (RDBMS)** 에 저장.
4. **Recommendation**: "친구의 친구가 좋아하는 상품" 추천 알고리즘은 **Neo4j (Graph)** 로 순회.

#### 한줄 요약

- 자료 형태에 맞는 보관함과 지점을 찾아 저장하고 필요한 수의 사본을 확인한다.

## Ⅴ. 종류 및 비교 (RDBMS 대 NoSQL 4대 유형 종합 비교)

<details><summary>핵심 용어</summary>

- **Data Structure Tradeoff**: 단순한 Key-Value일수록 수평 분산과 속도가 극대화되고, 복잡한 Graph일수록 관계 표현력은 높으나 분산 조회가 고비용화.

</details>

| 비교 항목 | Key-Value | Document | Wide-Column | Graph Store |
|:---|:---|:---|:---|:---|
| 데이터 구조 | **단순 `Key-Value`** | **`JSON / BSON`** | **`Row - Column Family`**| **`Node - Edge`** |
| `JOIN` 수용성 | 없음 | 서브 문서로 자체 내포 | 없음 | **자체 간선(Edge) 조인 최적화** |
| 스키마 가변성 | 100% Schema-Less | Schema-Less | Schema-Less | Schema-Less |
| 수평 확장성 | **극대화 (Scale-Out)** | 우수 | **극대화 (Scale-Out)** | 보통 (노드 간 분산 순회 한계) |

#### 한줄 요약

- 상품 객체는 문서, 세션은 키값, 센서 기록은 와이드 컬럼, 친구 추천은 그래프 모델이 잘 맞는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NoSQL Anti-Pattern**: RDBMS처럼 NoSQL에 정규화를 적용하여 여러 컬럼/테이블로 쪼개 놓아, 데이터 조회 시 애플리케이션 단에서 수십 번의 N+1 조인 쿼리를 발생시키는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NoSQL에 정규화를 무리하게 적용하여 앱 단 N+1 쿼리 폭증 | **쿼리 패턴에 맞춰 중복 저장을 허용하는 데이터 내포(Embedding)**| N+1 쿼리 소멸 |
| RDBMS의 ACID 트랜잭션 부재로 인한 정합성 문제 | **Saga Pattern / 2PC 적용 또는 정합성 핵심 부문은 RDBMS 혼용**| 정합성 보존 |
| Cassandra 등 Wide-Column 키 설정 오기로 핫 파티션 발생 | **Partition Key에 High-cardinality 변수(UUID, TIMESTAMP) 조합** | 수평 분산 보장 |

> 사례: **배달의민족 / 쿠팡의 Polyglot Persistence (Redis + MongoDB + MySQL) 운용**

#### 한줄 요약

- 담기 편한 모양보다 실제로 자주 찾고 함께 바꾸는 단위에 맞는 보관함을 고른다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **NoSQL 수립 기준(NoSQL Selection Standards)**: 데이터 구조 복잡성, 쿼리 도메인 패턴, Scale-Out 가용성 및 Polyglot Persistence 조화성에 의거한 체계.

</details>

- **NoSQL 수립 기준**에 따라 현대 대용량 서비스 구축 시 **Polyglot Persistence (Key-Value + Document + RDBMS) 아키텍처** 필수 적용

#### 한줄 요약

- NoSQL 적용 판단 기준으로 가장 자주 묻고 고치는 방식과 사본•복구 규칙을 함께 정한다.
