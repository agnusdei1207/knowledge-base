---
title: "NoSQL 유형 - 문서·키값·컬럼·그래프 (NoSQL Types)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 116
---

# 📖 【암기용】 개념 완전 이해

> 목적: NoSQL 유형을 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 관계형 모델 밖에서 키값·문서·와이드 컬럼·그래프 형태로 데이터를 저장하는 DB 계열
- **왜 필요한가**: 모든 업무가 정규화 테이블과 조인 중심으로 맞지 않는다. 세션, JSON 문서, 시계열, 관계 탐색처럼 접근 패턴이 뚜렷한 데이터는 전용 모델이 비용과 지연을 낮춘다.
- **핵심 직관**: 모든 물건을 같은 서랍장에 넣지 않고, 카드·파일·엑셀·관계도처럼 용도별 보관함을 고르는 일이다.

## 깊이 이해
- **배경·문제의식**: 웹·모바일 서비스는 스키마가 자주 바뀌고, 대량 쓰기와 지리적 분산을 요구한다. RDBMS는 조인과 트랜잭션에 강하지만 수평 확장과 유연한 스키마에서 별도 설계가 필요하다.
- **작동 원리**: NoSQL은 쿼리 패턴을 먼저 정하고 저장 모델을 고른다. key-value는 키로 바로 접근하고, document는 JSON 문서를 저장하며, wide-column은 파티션 키와 클러스터링 키로 대량 행을 저장하고, graph는 노드와 엣지를 탐색한다.
- **비유**: 고객 문의는 문서 파일, 로그인 세션은 사물함 번호, 센서 데이터는 시간표, 친구 추천은 관계도로 보관하면 찾는 방식이 명확해진다.
- **구체 예시**: 사용자 프로필은 MongoDB document, 장바구니 세션은 Redis key-value, IoT 시계열은 Cassandra wide-column, 소셜 관계 추천은 Neo4j graph로 모델링할 수 있다.
- **흔한 오해·주의점**: NoSQL은 SQL을 쓰지 않는다는 뜻이 아니다. 일부 제품은 SQL 유사 질의를 제공하지만, 조인·트랜잭션·일관성 범위가 제품별로 다르다.

## 연결 개념
- CAP 정리 — 분산 DB에서 일관성·가용성·분할 내성 선택을 설명
- BASE — NoSQL 계열에서 자주 쓰는 완화된 일관성 모델
- 샤딩 — NoSQL 수평 확장의 기본 배치 방식
- 쿼리 패턴 — NoSQL 모델 선택의 출발점

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NoSQL 답안은 유형 나열이 아니라 데이터 모델, 쿼리 패턴, 일관성, 트랜잭션 범위, 운영 지표를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NoSQL은 key-value, document, wide-column, graph 등 접근 패턴별 저장 모델을 제공하는 비관계형 DB 계열이다.
> 2. **가치**: 스키마 변화, 대량 쓰기, 수평 확장, 관계 탐색 등 RDBMS 단독 처리 비용이 큰 영역을 전용 모델로 처리한다.
> 3. **판단 포인트**: 데이터 구조보다 조회 경로, 일관성 요구, 트랜잭션 범위, 보조 인덱스, 운영 성숙도를 기준으로 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| NoSQL 유형별 적합 업무 판단 확인 | document/key-value/wide-column/graph 비교 | 제품명만 나열하고 쿼리 패턴 누락 |
| RDBMS 대비 트레이드오프 확인 | schema flexibility, consistency, transaction 범위 | NoSQL을 RDBMS 대체재로 단정 |
| 분산 운영 관점 확인 | shard key, replication, index, eventual consistency | CAP·BASE와 연결하지 않음 |

> 요약: 이 문제는 저장 모델별 장단점보다 업무 접근 패턴에 맞는 DB 선택 기준을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: NoSQL은 접근 패턴별 비관계형 DB 계열이다.
- 배경: JSON 문서, 세션, 대량 시계열, 관계 탐색은 정규화 테이블과 조인 중심 모델만으로 설계하면 저장·조회 경로가 복잡해진다.
- 필요성: Key-Value, Document, Wide-Column, Graph 모델별 일관성, 트랜잭션 범위, shard key 제약을 확인해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Workload 분석 -> Query Pattern 도출
  / Key-Value: key -> value
  / Document: id -> JSON document
  / Wide-Column: partition key -> column family
  / Graph: node -> edge traversal
Consistency/Index/Shard 설계 -> DB 선택
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Key-Value | 키 기반 단건 조회 | Redis, DynamoDB, 세션·캐시 |
| Document | JSON/BSON 문서 저장 | MongoDB, Couchbase, 프로필·콘텐츠 |
| Wide-Column | 파티션별 대량 행 저장 | Cassandra, HBase, 로그·시계열 |
| Graph | 노드·엣지 관계 탐색 | Neo4j, Neptune, 추천·사기탐지 |

> 요약: NoSQL 구조는 쿼리 패턴을 기준으로 네 가지 저장 모델을 선택하고, 인덱스·샤딩·일관성을 함께 설계한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구사항 수집 -> 접근 패턴 분류
  / 단건 조회 -> key-value
  / 유연한 문서 -> document
  / 대량 쓰기 -> wide-column
  / 관계 탐색 -> graph
일관성 요구 확인 -> 인덱스·샤드 설계 -> PoC 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 조회·쓰기·갱신 패턴 수집 | 상위 10개 쿼리 QPS |
| 2 | 데이터 모델과 제품군 매핑 | 조인 필요 여부, 문서 크기 |
| 3 | 일관성·트랜잭션 범위 결정 | read-your-writes 필요 여부 |
| 4 | 샤드 키와 보조 인덱스 설계 | partition skew 20% 이하 |

> 요약: NoSQL 선택은 모델 선호가 아니라 쿼리 패턴과 일관성 요구를 계측해 제품군을 좁히는 절차이다.

---

## Ⅳ. 특징

| 구분 | RDBMS 중심 | NoSQL 유형별 적용 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 스키마 | 사전 스키마·정규화 | 문서별 필드 변화 허용 | schema 변경 주기 |
| 조회 | SQL·조인 중심 | 키·문서·컬럼·그래프 접근 | 상위 쿼리 p95 |
| 확장 | 복제·파티션 중심 | 샤딩·복제 기본 내장 | 노드 추가 후 처리량 |
| 일관성 | ACID 중심 | 제품별 eventual/strong 선택 | stale read 허용 시간 |

> 요약: NoSQL은 모델별 접근 경로를 최적화하지만, 일관성·조인·운영 도구 제약을 업무별로 검증해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 세션 | RDBMS session table | key-value | TTL, 단건 lookup, QPS 높음 |
| 프로필 | 정규화 테이블 | document | JSON 필드 변화 빈번 |
| 로그 | row table | wide-column | append write, time range query |
| 추천 | join table | graph | 2~4 hop 탐색 빈번 |

> 요약: NoSQL은 업무별 접근 패턴이 명확할 때 선택하고, 강한 원자성이 필요한 핵심 거래는 RDBMS를 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 모델 부적합 | 쿼리 패턴 변화 | CQRS, 검색 인덱스 보강 | full scan 쿼리 수 |
| 핫 파티션 | 낮은 cardinality 키 | 복합 키, random suffix | partition QPS 편차 |
| 정합성 문제 | eventual consistency | version, conditional write | conflict count |
| 운영 미숙 | 백업·복구 절차 부족 | runbook, restore drill | RTO/RPO 달성률 |

> 요약: NoSQL 리스크는 모델 부적합과 운영 미숙이며, 쿼리·파티션·복구 지표로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 쿼리 적합성 | 상위 10개 쿼리 index hit | query profiler |
| 지연 | p95 읽기 50ms 이하 | APM, DB metrics |
| 분산 | 파티션 편차 20% 이하 | shard metrics |
| 정합성 | 충돌률 0.1% 이하 | version conflict log |

> 요약: NoSQL 도입은 쿼리 적합성, 지연, 분산 균등성, 정합성, 복구 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 모델 선택: 상위 10개 쿼리와 쓰기 패턴을 기준으로 key-value/document/wide-column/graph 중 하나를 고르고 조인 필요 영역은 RDBMS에 남김
2. 분산 설계: shard key cardinality, partition skew, replication factor 3, consistency level을 업무 SLA에 맞춰 설정함
3. 운영 검증: 백업·복구 리허설, schema migration, index build, hot partition 알람을 PoC 단계에서 확인함

**결론 (2줄):**
- 기술사 판단: 쿼리 패턴이 단순하고 수평 확장이 필요하면 NoSQL, 복잡 조인·강한 트랜잭션이 핵심이면 RDBMS 또는 polyglot persistence가 타당함
- 향후 방향: 멀티모델 DB와 서버리스 NoSQL은 운영 부담을 줄이지만 데이터 모델링과 일관성 선택은 서비스 요구사항에 따라 결정됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NoSQL 유형을 설명하시오", "기술하시오" | 네 가지 모델과 접근 패턴 흐름 | RDBMS 대비 스키마·확장·일관성 차이 |
| 요구사항 명시형 | "비교하시오", "선택 기준을 제시하시오" | 업무별 모델 매핑과 PoC 절차 | 트랜잭션·운영·정합성 리스크 대응 |

> 요약: 설명형은 유형별 구조, 비교형은 업무 조건별 선택 기준으로 답안을 전환한다.
