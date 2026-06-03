+++
weight = 220
title = "220. NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL은 "Not Only SQL"로, RDBMS의 엄격한 스키마와 ACID 제약을 완화하고 **수평 확장(Scale-Out)**을 통해 빅데이터 규모의 다양한 데이터 모델을 처리하기 위해 등장했다.
> 2. **가치**: 키-값(Key-Value)·도큐먼트(Document)·와이드 컬럼(Wide-Column)·그래프(Graph) 4가지 유형은 각각 캐시·컨텐츠·시계열·관계 분석 등 특정 사용 사례에 최적화되어 있다.
> 3. **판단 포인트**: NoSQL DB 선택은 데이터 구조(정형/비정형), 접근 패턴(단순 조회/복잡 조인/관계 탐색), 일관성 요건(강한/결과적), 규모(단일 서버/수백 노드)를 종합 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

### NoSQL 등장 배경

2000년대 후반 Google(Bigtable, 2006), Amazon(Dynamo, 2007), Facebook(Cassandra, 2008)이 기존 RDBMS로는 처리 불가능한 규모의 서비스를 위해 자체 NoSQL DB를 개발·공개하면서 NoSQL 생태계가 폭발적으로 성장했다.

**RDBMS의 한계:**
- 수평 확장(Scale-Out) 어려움 → 수직 확장(Scale-Up) 비용 폭증
- 엄격한 스키마 → 비정형 데이터 처리 불가
- ACID 트랜잭션 오버헤드 → 초고속 처리 성능 저하
- JOIN 연산 비용 → 분산 환경에서 네트워크 병목

### NoSQL BASE 속성

| RDBMS ACID | NoSQL BASE | 설명 |
|:---|:---|:---|
| Atomicity | Basically Available | 일부 노드 장애에도 서비스 지속 |
| Consistency | Soft-state | 일시적 불일치 허용 |
| Isolation | Eventually Consistent | 시간이 지나면 일관성 달성 |
| Durability | - | 내구성은 유지 |

📢 **섹션 요약 비유**: RDBMS는 **엄격한 은행 창구**고, NoSQL은 **편의점 계산대**다. 편의점은 영수증이 가끔 느리게 나와도 되지만, 은행은 모든 거래가 정확해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### NoSQL 4대 유형 비교

```
NoSQL 유형별 데이터 모델
┌──────────────┬──────────────────────────────────────────┐
│ 키-값        │  "user:1234" → { name, age, email }     │
│ (Key-Value)  │  단순 해시맵, 빠른 단일 조회             │
├──────────────┼──────────────────────────────────────────┤
│ 도큐먼트     │  { _id: 1, name: "홍길동",              │
│ (Document)   │    orders: [{...}, {...}] }             │
│              │  JSON/BSON 중첩 구조, 유연한 스키마      │
├──────────────┼──────────────────────────────────────────┤
│ 와이드 컬럼  │  Row Key │ CF:col1 │ CF:col2 │ ...      │
│ (Wide-Column)│  희소 행렬, 컬럼 패밀리 단위 저장        │
├──────────────┼──────────────────────────────────────────┤
│ 그래프       │  (노드A) -[관계:FRIENDS]-> (노드B)       │
│ (Graph)      │  노드·엣지·속성, 관계 탐색 최적화        │
└──────────────┴──────────────────────────────────────────┘
```

### 세부 비교 표

| 항목 | 키-값 | 도큐먼트 | 와이드 컬럼 | 그래프 |
|:---|:---|:---|:---|:---|
| **대표 제품** | Redis, DynamoDB | MongoDB, Couchbase | Cassandra, HBase | Neo4j, Amazon Neptune |
| **데이터 모델** | 단순 Key→Value | JSON/BSON 도큐먼트 | 컬럼 패밀리 | 노드·엣지 그래프 |
| **쿼리 방식** | Key 기반 단순 조회 | 필드 쿼리, 인덱스 | Row Key, 범위 스캔 | Cypher, Gremlin |
| **확장성** | 매우 높음 | 높음 | 매우 높음 | 수평 확장 어려움 |
| **일관성** | 결과적/조정 가능 | 도큐먼트 단위 ACID | 결과적/조정 가능 | ACID (Neo4j) |
| **주 사용 사례** | 캐시, 세션, 리더보드 | 컨텐츠 관리, 카탈로그 | 시계열, IoT, 로그 | SNS 관계, 추천, 지식 그래프 |
| **JOIN 지원** | 없음 | 제한적 ($lookup) | 없음 | 그래프 순회 |

📢 **섹션 요약 비유**: 키-값은 **사물함(번호→물건)**, 도큐먼트는 **서류 봉투(내용물 자유)**, 와이드 컬럼은 **엑셀 시트(행·열 희소)**, 그래프는 **관계 지도(사람 간 연결)**다.

---

## Ⅲ. 비교 및 연결

### 유형별 심화 특성

**키-값 (Key-Value):**
- Redis: 인메모리 + RDB/AOF 영속성, 자료 구조(Hash·List·Sorted Set) 지원
- DynamoDB: 서버리스, 자동 샤딩(Auto Sharding), DAX 캐시 계층

**도큐먼트 (Document):**
- MongoDB: BSON 저장, Aggregation Pipeline, Atlas Search(전문 검색)
- 스키마 유연성 → 마이크로서비스의 독립 스키마 진화에 적합

**와이드 컬럼 (Wide-Column):**
- Cassandra: 일관적 해시(Consistent Hashing) + 가십 프로토콜(Gossip Protocol), 쓰기 최적화(LSM Tree)
- HBase: Hadoop/HDFS 위에 동작, 강한 일관성, HBase → Hadoop 분석 연계

**그래프 (Graph):**
- Neo4j: Property Graph 모델, Cypher 쿼리 언어, 임베디드/클러스터 모드
- 사용 사례: 부정 탐지(Fraud Detection), 추천 엔진, 지식 그래프, SNS

### NoSQL vs NewSQL

| 항목 | NoSQL | NewSQL |
|:---|:---|:---|
| **목표** | 확장성·유연성 | 확장성 + ACID 보장 |
| **대표 제품** | MongoDB, Cassandra | Spanner, CockroachDB, TiDB |
| **SQL 지원** | 제한적 | 완전 SQL |
| **일관성** | 결과적 일관성 | 강한 일관성 |

📢 **섹션 요약 비유**: NoSQL vs NewSQL은 **리어카(가볍고 빠름) vs 소형 트럭(무겁지만 규칙 준수)**의 차이다. NewSQL은 RDBMS의 규칙을 지키면서 트럭을 여러 대 이어 붙인 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 사용 사례별 NoSQL 선택 매트릭스

| 사용 사례 | 권장 유형 | 이유 |
|:---|:---|:---|
| 웹 세션 캐시 | 키-값 (Redis) | 빠른 만료(TTL) 관리, 인메모리 |
| 사용자 프로필 | 도큐먼트 (MongoDB) | 유연한 속성, 중첩 데이터 |
| IoT 시계열 로그 | 와이드 컬럼 (Cassandra) | 쓰기 집중, 시간 범위 스캔 |
| SNS 친구 추천 | 그래프 (Neo4j) | 다단계 관계 탐색 |
| 쇼핑몰 상품 카탈로그 | 도큐먼트 (MongoDB) | 다양한 속성, 전문 검색 |
| 실시간 순위표 | 키-값 (Redis Sorted Set) | O(log n) 순위 갱신 |

### 기술사 판단 포인트

1. **복합 사용 패턴**: 하나의 서비스에 여러 NoSQL 혼용 (Polyglot Persistence)
2. **RDBMS와 공존**: RDBMS는 트랜잭션 핵심, NoSQL은 캐시·로그·분석 보조
3. **운영 복잡성**: NoSQL 도입 시 관리 오버헤드 증가 → 관리형 서비스(AWS DynamoDB, Atlas) 활용

📢 **섹션 요약 비유**: 폴리글랏 퍼시스턴스(Polyglot Persistence)는 **요리마다 다른 조리 기구**를 쓰는 것이다. 밥은 솥, 고기는 그릴, 국은 냄비. 모두 밥솥으로만 하려면 불편하다.

---

## Ⅴ. 기대효과 및 결론

### 도입 기대효과

| 효과 | 정량적 목표 |
|:---|:---|
| 읽기 성능 향상 | Redis 캐시 도입으로 DB 부하 70~90% 감소 |
| 쓰기 처리량 증가 | Cassandra 클러스터 확장으로 초당 수십만 건 처리 |
| 개발 민첩성 | 스키마 없는 도큐먼트 DB로 스키마 마이그레이션 없이 기능 추가 |
| 관계 분석 속도 | 6단계 친구 찾기: RDBMS 수십 초 → Neo4j 수십 밀리초 |

### 결론

NoSQL은 RDBMS를 대체하는 것이 아니라 **상호 보완적으로 공존**한다. 데이터 구조, 접근 패턴, 규모, 일관성 요건을 기반으로 적절한 저장소를 선택하는 **폴리글랏 퍼시스턴스(Polyglot Persistence)** 전략이 현대 데이터 아키텍처의 표준이 되었다.

📢 **섹션 요약 비유**: 최적의 NoSQL 선택은 **운동 종목에 맞는 신발 선택**이다. 등산화, 러닝화, 수영장 슬리퍼 모두 좋은 신발이지만, 상황에 따라 맞는 것이 다르다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 분류 | 키-값 (Redis, DynamoDB) | 단순 해시맵, 캐시·세션 최적 |
| 분류 | 도큐먼트 (MongoDB, Couchbase) | JSON/BSON, 유연한 스키마 |
| 분류 | 와이드 컬럼 (Cassandra, HBase) | 시계열·로그, 쓰기 최적화 |
| 분류 | 그래프 (Neo4j, Neptune) | 관계 탐색, SNS·추천 |
| 이론 기반 | CAP 정리 | AP vs CP 선택 근거 |
| 속성 | BASE | NoSQL의 일관성 완화 모델 |
| 진화 | NewSQL (CockroachDB, TiDB) | 확장성 + ACID 결합 |
| 설계 전략 | 폴리글랏 퍼시스턴스 | 목적별 다수 DB 혼용 |

### 👶 어린이를 위한 3줄 비유 설명

1. 키-값은 **사물함**이야. 번호(키)를 알면 바로 내 물건(값)을 꺼낼 수 있어. 엄청 빠르지!

### 📈 관련 키워드 및 발전 흐름도

```text
RDBMS (관계형, 정형 데이터)
    │
    ▼
NoSQL 4대 유형
    ├─► Key-Value: Redis · DynamoDB (캐시 · 세션)
    ├─► Document: MongoDB · CouchDB (유연 스키마)
    ├─► Wide-Column: Cassandra · HBase (대규모 쓰기)
    └─► Graph: Neo4j · Amazon Neptune (관계 탐색)
    │
    ▼
Multi-Model DB: 여러 데이터 모델 통합 지원
```
2. 도큐먼트는 **서류 봉투**야. 봉투 안에 사진도 넣고 편지도 넣고 뭐든 넣을 수 있어. 내용이 다 달라도 괜찮아.
3. 그래프는 **친구 관계도**야. 나→내 친구→내 친구의 친구를 따라가면서 "우리 학교에서 몇 다리 건너 연결됐지?" 같은 걸 빠르게 찾을 수 있어.
