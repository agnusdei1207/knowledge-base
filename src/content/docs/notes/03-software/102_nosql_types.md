---
sidebar:
  order: 102
  label: "102. NoSQL 유형: 문서•키값•컬럼•그래프 (NoSQL Types)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "NoSQL 유형: 문서•키값•컬럼•그래프 (NoSQL Types)"
date: "2026-08-13T20:30:00+09:00"
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

<details><summary>용어 설명</summary>

- **NoSQL (Not Only SQL)**: 관계형 데이터베이스(RDBMS)의 엄격한 테이블 스키마, `JOIN` 오버헤드, 수평 확장(Scale-Out)의 한계를 극복하기 위해, 데이터 모델과 접근 패턴에 맞춰 고안된 4대 비관계형 데이터베이스 분류 체계 (Document, Key-Value, Wide-Column, Graph).
- **Schema-Flexibility (가변 스키마)**: 튜플(행)마다 저장되는 속성(컬럼)이 달라지더라도 사전 DDL 정의 없이 자유롭게 데이터를 인서트 및 확장할 수 있는 속성.
- **Polyglot Persistence (폴리글랏 퍼시스턴스)**: 하나의 소프트웨어 시스템 안에서 단일 DB에 의존하지 않고, 데이터의 성격(세션, 검색, 그래프, 트랜잭션)에 맞춰 적재적소의 NoSQL 및 RDBMS 엔진을 혼용하여 구축하는 아키텍처 사상.

</details>

- 정의/개념: 관계 모델 외 데이터 모델을 제공하는 **NoSQL(Not Only SQL)**
- 배경/필요성: 단일 관계 모델로는 **비정형•관계 순회•분산 확장** 제약

#### 한줄 요약

- 모든 데이터를 같은 테이블에 넣지 않고 문서, 키-값, 와이드 컬럼, 그래프 중 접근 패턴에 맞는 데이터 모델을 고른다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Query-Driven Data Modeling (쿼리 중심 데이터 모델링)**: RDBMS처럼 정규화(Normalization)를 먼저 하지 않고, 애플리케이션의 화면 조회 쿼리(Query Pattern)에 맞춰 중복을 허용(Denormalization)하여 테이블을 설계하는 특성.
- **BASE Consistency Model**: Strictly ACID 대신 Basically Available, Soft-state, Eventual Consistency(최종 일관성) 모델 채택.

</details>

- **수평 확장**: 분산 노드 증설을 통한 저장 용량 및 처리량 확장.
- **가변 스키마**: 사전 정의 없이 자유로운 데이터 삽입 및 필드 확장 지원.
- **운영 Trade-off**: 제품별 트랜잭션•일관성•질의 기능 확인 필요

#### 한줄 요약

- 자주 묻는 질문에는 빠르게 답하지만 다른 형태의 질문은 어렵기 때문에 조회 방식부터 정하고 모델을 선택해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Key-Value Store**: Unique Key 1개에 BSON/String/Binary Value를 1:1 매핑하는 극단적 단순 구조 (Redis, DynamoDB).
- **Document Store**: JSON/BSON 형태의 중첩된 서브 문서(Sub-document) 및 배열 구조를 인덱싱하여 다루는 모델 (MongoDB, Couchbase).
- **Wide-Column Store**: Row Key, Column Family, Column Name, Timestamp 구조의 4차원 희소(Sparse) 행렬 데이터 모델 (Cassandra, HBase).
- **Graph Store**: Node(정점), Edge(간선), Property(속성) 구조로 복잡한 네트워크 소셜 관계를 지향하는 모델 (Neo4j).

</details>

| 유형 | 데이터 모델•적합 접근 패턴 |
|:---|:---|
| Key-Value Store | 키 기반 단건 조회•세션•캐시 |
| Document Store | 중첩 문서 단위 조회•상품 카탈로그 |
| Wide-Column Store | 파티션 키 기반 대규모 쓰기•시계열 |
| Graph Store | 정점•간선 기반 다단계 관계 순회 |

#### 한줄 요약

- 질문 형태에 맞는 보관함과 조회 방법, 사본 규칙을 묶는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Polyglot Architecture**: 단일 서비스 시스템 내에서 세션은 Redis, 카탈로그는 MongoDB, 결제는 RDBMS, 친구추천은 Neo4j에 분산 적재하는 아키텍처.

</details>

```text
[데이터•질의 요구]
        │
        ▼
1. 접근 패턴 식별
        │
        ▼
2. 데이터 관계 분석
        │
        ▼
3. 일관성 요구 판정
        │
        ▼
4. 데이터 모델 선택
        │
        ▼
5. 부하•복구 검증
        │
        ▼
   [저장소 확정]
```

### 동작 원리

1. **접근 패턴 식별**: 단건•범위•집계•관계 순회 구분
2. **데이터 관계 분석**: 중첩•희소 열•연결 구조 판정
3. **일관성 요구 판정**: 원자성•최신성•가용성 수준 결정
4. **데이터 모델 선택**: 요구에 맞는 NoSQL•RDBMS 조합
5. **부하•복구 검증**: 분산 성능과 장애 복구 시험

#### 한줄 요약

- 자료 형태에 맞는 보관함과 지점을 찾아 저장하고 필요한 수의 사본을 확인한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Data Structure Tradeoff**: 단순한 Key-Value일수록 수평 분산과 속도가 극대화되고, 복잡한 Graph일수록 관계 표현력은 높으나 분산 조회가 고비용화.

</details>

| 비교 항목 | Key-Value | Document | Wide-Column | Graph Store |
|:---|:---|:---|:---|:---|
| 데이터 구조 | **단순 `Key-Value`** | **`JSON / BSON`** | **`Row - Column Family`**| **`Node - Edge`** |
| 관계 처리 | 앱에서 키 조합 | 문서 내포•참조 | 앱에서 파티션 조합 | **간선 기반 관계 순회** |
| 스키마 특성 | 값 구조를 앱이 관리 | 문서 검증 규칙 선택 | 열 구조의 유연성 | 속성 모델을 제품별 관리 |
| 분산 특성 | 키 분할에 유리 | 샤드 키에 좌우 | 파티션 확장에 유리 | 분산 순회 비용 고려 |

#### 한줄 요약

- 상품 객체는 문서, 세션은 키값, 센서 기록은 와이드 컬럼, 친구 추천은 그래프 모델이 잘 맞는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NoSQL Anti-Pattern**: RDBMS처럼 NoSQL에 정규화를 적용하여 여러 컬럼/테이블로 쪼개 놓아, 데이터 조회 시 애플리케이션 단에서 수십 번의 N+1 조인 쿼리를 발생시키는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 분리로 다중 조회 증가 | **접근 패턴별 내포•중복 설계** | 왕복 비용 감소 |
| 제품 기능과 일관성 요구 불일치 | **트랜잭션 범위 검증•RDBMS 혼용** | 정합성 위험 통제 |
| 부적절한 파티션 키로 핫스팟 | **카디널리티•시간 분포 부하 시험** | 부하 편향 완화 |

> 사례: **배달의민족 / 쿠팡의 Polyglot Persistence (Redis + MongoDB + MySQL) 운용**

#### 한줄 요약

- 담기 편한 모양보다 실제로 자주 찾고 함께 바꾸는 단위에 맞는 보관함을 고른다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **NoSQL 수립 기준(NoSQL Selection Standards)**: 데이터 구조 복잡성, 쿼리 도메인 패턴, Scale-Out 가용성 및 Polyglot Persistence 조화성에 의거한 체계.

</details>

- 단건은 **Key-Value**, 문서는 Document, 관계 순회는 Graph 선택

#### 한줄 요약

- NoSQL 적용 판단 기준으로 가장 자주 묻고 고치는 방식과 사본•복구 규칙을 함께 정한다.
