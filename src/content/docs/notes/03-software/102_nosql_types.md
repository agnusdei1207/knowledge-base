---
sidebar:
  order: 102
  label: "102. NoSQL 유형: 문서•키값•컬럼•그래프"
  badge:
    text: "기출 · 70%"
    variant: note
title: "NoSQL 유형: 문서•키값•컬럼•그래프 (NoSQL Types)"
date: "2026-08-31T10:48:00+09:00"
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

- **NoSQL(Not Only SQL)**: 관계형 데이터 모델의 제약을 벗어나 비정형/반정형 데이터와 대규모 수평 확장을 지원하는 비관계형 데이터베이스 총칭.
- **4대 NoSQL 유형**: Key-Value(키값), Document(문서), Wide-Column(컬럼 패밀리), Graph(그래프).

</details>

- 정의/개념: 관계형 스키마와 확장의 한계를 극복하기 위해 Key-Value, Document, Wide-Column, Graph 4대 특화 데이터 모델을 제공하는 비관계형 데이터베이스
- 배경/필요성: RDBMS의 엄격한 정형 스키마, 무거운 조인 및 **수직 확장(Scale-Up) 한계로 인한 비정형 데이터 처리와 대규모 수평 분산 제약 한계**

#### 한줄 요약
- NoSQL은 RDBMS의 상위 대체재가 아니라 조인과 강한 일관성을 내주고 확장성과 스키마 유연성을 산 모델이므로, 접근 패턴이 먼저 확정된 경우에만 그 거래가 이득이 된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Schema-less(가변 스키마)**: 사전 DDL 정의 없이 동적으로 필드를 추가할 수 있어 잦은 데이터 구조 변경에 유연하게 대응.
- **Polyglot Persistence**: 단일 DB에 의존하지 않고 서비스 목적에 맞추어 RDB, 캐시, NoSQL을 혼용 배치하는 아키텍처 사상.

</details>

- 비정형 데이터의 유연한 확장을 보장하는 **가변 스키마(Schema-less)** 구조
- 노드 증설을 통해 선형적으로 용량을 확장하는 분산 수평 확장(Scale-Out) 최적화
- 서비스 도메인 특성에 맞추어 최적의 엔진을 조합하는 폴리글랏 퍼시스턴스(**Polyglot Persistence**)

#### 한줄 요약
- 가변 스키마와 수평 확장성을 바탕으로 데이터 성격에 최적화된 비관계형 모델을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NoSQL 4대 모델별 대표 제품**: Key-Value(Redis), Document(MongoDB), Wide-Column(Cassandra), Graph(Neo4j).

</details>

```text
[NoSQL 4대 데이터 모델 구조]
|-- 1. Key-Value Store: [Key] -> [Value] (Redis, DynamoDB / O(1) 단순 룩업, 인메모리 캐시)
|-- 2. Document Store: [Document ID] -> {JSON / BSON 중첩 객체} (MongoDB / 상품 카탈로그)
|-- 3. Wide-Column Store: [Row Key] -> [Column Family: Dynamic Columns] (Cassandra / 시계열 센서)
`-- 4. Graph Store: (Node) -[Edge: Property]-> (Node) (Neo4j / 소셜 친구 추천, FDS 사기 탐지)
```

선의 의미: 계층 및 4대 NoSQL 데이터 모델과 대표 제품/활용처 구조

| 구성요소 | 책임 |
|:---|:---|
| Key-Value Store | 키 기반 단순 고속 조회 |
| Document Store | JSON·BSON 중첩 문서 저장 |
| Wide-Column Store | 파티션 기반 대규모 희소 데이터 저장 |
| Graph Store | 노드·간선 기반 관계 탐색 |

#### 한줄 요약
- 네 모델은 저장 형식이 아니라 어떤 접근을 상수 비용으로 만들지가 다르므로, 키 조회·문서 단위 조회·범위 스캔·관계 탐색 중 무엇을 값싸게 할 것인가가 곧 모델 선택이 된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NoSQL 모델 선정 절차**: 데이터 접근 패턴 분석 $\to$ 관계 복잡도 판정 $\to$ 일관성 수준 평가 $\to$ 엔진 모델 선택.

</details>

```text
데이터 저장소 선정 의사결정 파이프라인
        │
   [단순 Key 기반 초고속 읽기/쓰기가 필요한가?] ──예──► Key-Value Store (Redis)
        │ 아니오
   [중첩된 복합 도메인 객체와 유연한 스키마가 필요한가?] ──예──► Document Store (MongoDB)
        │ 아니오
   [대규모 시계열/로그 데이터의 초당 수만 건 쓰기가 필요한가?] ──예──► Wide-Column (Cassandra)
        │ 아니오
   [다단계 관계 순회(Graph Traversal)와 경로 탐색이 필요한가?] ──예──► Graph Store (Neo4j)
        │ 아니오
   엄격한 다중 테이블 Join과 ACID가 필수인가? ──────► 관계형 RDBMS (PostgreSQL)
```

#### 한줄 요약
- 모델 선택은 데이터의 모양이 아니라 질의 패턴에서 결정되므로, 접근 패턴이 나중에 바뀌면 RDBMS처럼 질의만 고치는 것으로 끝나지 않고 데이터를 다시 적재해야 하는 비용이 발생한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **4대 NoSQL 특성 비교**: Key-Value(단순 고속), Document(유연 중첩), Wide-Column(대규모 쓰기), Graph(관계 탐색).

</details>

| 비교 항목 | Key-Value Store | Document Store | Wide-Column Store | Graph Store |
|:---|:---|:---|:---|:---|
| 데이터 모델 | 단순 Key-Value 쌍 | 계층형 JSON/BSON | 행-컬럼 패밀리 매트릭스 | 정점(Node)과 간선(Edge) |
| 쿼리 유연성 | 낮음 (Key로만 조회) | 높음 (문서 내부 필드 검색) | 보통 (Row Key + 파티션 키) | 매우 높음 (Cypher 그래프 탐색) |
| 트랜잭션 범위 | 단일 키 수준 보장 | 단일/다중 문서 ACID | 단일 행 수준 보장 | 그래프 서브셋 ACID |
| 수평 확장성 | 매우 뛰어남 | 뛰어남 (샤딩 지원) | 최고 (P2P 분산 링) | 보통 (분산 샤딩 복잡도 높음) |

#### 한줄 요약
- 캐시는 Key-Value, 콘텐츠는 Document, 대용량 로그는 Wide-Column, 연결 관계는 Graph Store를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Denormalization in Document DB**: 조인이 약한 Document DB에서 관련 데이터를 별도 테이블로 쪼개지 않고 단일 문서 내에 배열로 포함(Embedding)시키는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NoSQL에 RDB식 정규화 적용으로 애플리케이션 N+1 조회 지연 | 접근 패턴에 맞추어 문서 내포(Embedding) 및 의도적 중복 허용 | 단일 쿼리로 화면 데이터 즉시 완결 |
| NoSQL 도입 후 트랜잭션 미지원으로 인한 데이터 정합성 파괴 | 원장/결제는 RDBMS에 유지하는 폴리글랏 퍼시스턴스 구축 | 정합성과 수평 확장의 영역별 분리 |
| Wide-Column 특정 파티션 키 쏠림으로 노드 핫스팟(Hotspot) 발생 | 복합 파티션 키(Salt 접두어 또는 시간 버킷팅) 설계로 균등 분산 | 분산 노드 부하 편향 해소 |
| 스키마리스 남용으로 인한 데이터 오염 및 버전 파편화 | JSON Schema Validation 적용 및 DTO 직렬화 규칙 통제 | 데이터 무결성 및 버전 호환성 확보 |

#### 한줄 요약
- 쿼리 맞춤 내포 설계, 폴리글랏 아키텍처, 파티션 키 분산, 스키마 유효성 검증으로 운용한다.

## Ⅶ. 결론

- 현대 분산 클라우드 아키텍처 및 대용량 데이터 처리의 **핵심 비관계형 영속성 모델**로 확립되었으며, 실무 구축 시에는 **단일 만능 DB 사상을 탈피하여 RDBMS(결제/원장)와 함께 Key-Value(캐시/세션: Redis), Document(카탈로그/콘텐츠: MongoDB), Wide-Column(시계열/로그: Cassandra), Graph(추천/관계망: Neo4j)를 유기적으로 조합하는 폴리글랏 지속성(Polyglot Persistence) 전략**을 수립하여 시스템 확장성과 개발 민첩성을 극대화

#### 한줄 요약
- 4대 NoSQL 모델은 데이터 구조와 접근 패턴에 특화된 비관계형 솔루션이며, 폴리글랏 아키텍처를 통해 최적의 시스템 확장을 실현한다.
