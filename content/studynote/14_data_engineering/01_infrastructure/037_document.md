---
title: "Document Store"
date: "2026-03-03"
tags:
  - "studynote-data-engineering"
weight: 37
---
> **핵심 인사이트**
> 1. 문서 저장소(Document Store)는 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)·BSON·XML 형태의 반정형 문서를 고유 ID와 함께 저장하는 [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/) 데이터베이스로, 스키마를 사전에 정의하지 않아도 다양한 구조의 문서를 유연하게 저장할 수 있다.
> 2. 문서 저장소의 핵심 장점은 관련 데이터를 하나의 문서로 내포([Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))해 단일 읽기 연산으로 완전한 객체를 가져올 수 있다는 것 — [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 조인([JOIN](/studynote/05_database/04_transactions_concurrency/521_join/)) 없이 O(1)에 가까운 조회가 가능하다.
> 3. [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/)(도큐먼트)와 Firestore([서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/))가 시장을 주도하며, 복잡한 중첩 구조·[배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)·다양한 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 엔티티(상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/), 사용자 프로필, 콘텐츠 관리)에 최적이다.

---

## I. 문서 저장소 기본 구조

```
문서 (Document) 예시 (JSON):
{
  "_id": "order_12345",
  "customer": {
    "id": "user_789",
    "name": "홍길동",
    "email": "hong@example.com"
  },
  "items": [
    {"product_id": "prod_001", "name": "노트북", "qty": 1, "price": 1500000},
    {"product_id": "prod_002", "name": "마우스", "qty": 2, "price": 30000}
  ],
  "total": 1560000,
  "status": "shipped",
  "created_at": "2024-01-15T10:30:00Z"
}

컬렉션 (Collection) = 관계형 DB의 테이블 (스키마 없음)
문서 (Document) = 관계형 DB의 행 (JSON 형식)
필드 (Field) = 관계형 DB의 열 (동적)
```

> 📢 **섹션 요약 비유**: 서랍장(컬렉션)에 봉투(문서)를 넣는데, 봉투마다 내용물 형식이 달라도 된다 — [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB는 모든 봉투에 동일 양식을 요구한다.

---

## II. 내포([Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) vs [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)([Reference](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))

```
데이터 모델링 핵심 선택:

내포 (Embedding):
  관련 데이터를 한 문서 안에 포함

  {
    "order_id": "order_001",
    "items": [  // 주문 항목을 내포
      {"product": "노트북", "qty": 1}
    ]
  }

  장점: 단일 읽기로 완전한 데이터
        조인 없음, 빠른 조회
  단점: 데이터 중복, 문서 크기 증가
  적합: 함께 자주 조회되는 데이터

참조 (Reference):
  다른 문서의 ID만 저장

  {
    "order_id": "order_001",
    "customer_id": "user_789"  // 참조만 저장
  }

  장점: 중복 없음, 정규화
  단점: 여러 번 조회 필요
  적합: 독립적으로 업데이트되는 데이터
```

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)    | 장점               | 단점            | 사용 경우          |
|-------|------------------|--------------|--------------------|
| 내포   | 단일 읽기, 빠름    | 중복, 크기     | 함께 조회하는 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)  |
| [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)   | 중복 없음, [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)  | 여러 번 조회   | 독립 엔티티         |

> 📢 **섹션 요약 비유**: 내포는 주문서에 고객 이름·주소를 직접 쓰는 것, [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)는 고객 번호만 쓰고 고객 파일에서 찾아보는 것.

---

## III. [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 주요 연산

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
orders = db["orders"]

# 삽입 (Insert)
result = orders.insert_one({
    "customer": "홍길동",
    "total": 50000,
    "status": "pending"
})

# 조회 (Find)
order = orders.find_one({"customer": "홍길동"})
all_orders = orders.find({"status": "pending"})

# 업데이트 (Update)
orders.update_one(
    {"_id": result.inserted_id},
    {"$set": {"status": "shipped"}}
)

# 배열 조작 ($push, $pull)
orders.update_one(
    {"_id": result.inserted_id},
    {"$push": {"items": {"product": "키보드", "qty": 1}}}
)

# 집계 파이프라인 (Aggregation)
pipeline = [
    {"$match": {"status": "shipped"}},
    {"$group": {"_id": "$customer", "total": {"$sum": "$total"}}}
]
result = list(orders.aggregate(pipeline))
```

> 📢 **섹션 요약 비유**: [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 집계 파이프라인은 컨베이어 벨트 — 데이터가 필터링(match)->[분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)(group)->변환 단계를 거쳐 최종 결과로 나온다.

---

## [IV](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). RDBMS vs 문서 저장소 비교

```
상품 카탈로그 예시:

RDBMS 방식:
  products 테이블 + attributes 테이블
  + product_attributes (조인 테이블)
  -> 3개 테이블 조인 필요

  문제: 전자제품/의류/식품 마다 속성이 달라
        스키마가 폭발적으로 복잡해짐

문서 저장소 방식:
  {
    "name": "삼성 TV",
    "category": "electronics",
    "specs": {"resolution": "4K", "size": "65인치", "hdmi": 4}
  }
  {
    "name": "청바지",
    "category": "clothing",
    "specs": {"size": "32", "color": "blue", "material": "cotton"}
  }

  -> 각 상품마다 다른 속성을 유연하게 저장!
```

> 📢 **섹션 요약 비유**: [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB는 모든 고객 양식이 동일한 공공기관, 문서 저장소는 각자 원하는 항목을 자유롭게 적을 수 있는 메모장.

---

## V. 실무 시나리오 — 이커머스 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)

```
문제 상황:
  전자제품(해상도·주파수)과 의류(사이즈·색상)를
  같은 테이블에 저장 -> RDBMS 한계

MongoDB 솔루션:
  products 컬렉션에 다양한 구조의 문서 저장
  인덱스: 카테고리, 가격, 이름에 인덱스 생성

  인덱스 생성:
    db.products.createIndex({"category": 1, "price": -1})
    -> 카테고리별 가격 내림차순 조회 최적화

  전문 검색 (Full Text Search):
    db.products.createIndex({"name": "text", "description": "text"})
    db.products.find({"$text": {"$search": "무선 헤드폰"}})

  결과:
    RDBMS 대비 상품 조회 응답시간 40% 개선
    스키마 변경 없이 새 카테고리 즉시 추가
```

> 📢 **섹션 요약 비유**: 이커머스 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)가 수천만 개, 카테고리마다 다른 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) — 문서 저장소가 유일한 현실적 해결책.

---

## 📌 관련 개념 맵

```
문서 저장소 (Document Store)
+-- 저장 형식: JSON/BSON/XML
+-- 핵심 개념
|   +-- 내포 (Embedding) vs 참조 (Reference)
|   +-- 스키마리스 (Schema-less)
|   +-- 컬렉션 / 문서 / 필드
+-- 주요 제품
|   +-- MongoDB (가장 널리 사용)
|   +-- Firestore (서버리스 Google)
|   +-- CouchDB (분산 동기화)
+-- 사용 시나리오
    +-- 상품 카탈로그 (다양한 속성)
    +-- 사용자 프로필 (중첩 데이터)
    +-- 콘텐츠 관리 시스템 (CMS)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[RDBMS 한계 (2000s)]
반정형 데이터 증가
스키마 유연성 요구
      |
      v
[CouchDB, MongoDB 등장 (2007~2009)]
JSON 문서 저장
수평 확장, 스키마리스
      |
      v
[MongoDB Atlas (2016~)]
클라우드 완전 관리형 MongoDB
      |
      v
[현재: 멀티모델 DB]
MongoDB가 문서 + 검색 + 분석 통합
Vector Search 추가 (AI 임베딩 저장)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 문서 저장소는 각기 다른 형식의 봉투([JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 문서)를 서랍(컬렉션)에 보관하는 데이터베이스예요.
2. [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB처럼 모든 데이터가 같은 형식일 필요가 없어서, 전자제품과 의류처럼 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 다른 것도 쉽게 저장할 수 있어요.
3. 주문 정보를 한 문서에 모두 담을 수 있어서 조회 시 여러 테이블을 합치는 복잡한 작업 없이 빠르게 가져와요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 37 / 258

<- **이전**: [036. 키-값 저장소 (Key-Value Store)](/studynote/14_data_engineering/01_infrastructure/036_key_value/)
**다음**: [038. 와이드 컬럼 저장소 (Wide Column Store)](/studynote/14_data_engineering/01_infrastructure/038_wide_column/) ->

---
