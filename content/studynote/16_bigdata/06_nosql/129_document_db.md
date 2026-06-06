---
title: "129. Document Db"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)
- **본질**: 문서형 DB는 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/BSON 형식의 자기 완결적 문서([Document](/studynote/14_data_engineering/01_infrastructure/037_document/))를 기본 단위로 저장하여, 복잡한 객체 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 단일 I/O 연산으로 조회할 수 있는 [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/) 모델이다.
- **가치**: [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경에 마이그레이션이 필요 없어 [애자일](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 개발 사이클에 최적화되며, [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))을 통해 관련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 문서에 모아 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 비용을 제거한다.
- **판단 포인트**: 읽기 패턴이 명확한 경우 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)으로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화하고, [데이터 공유](/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/)·갱신이 빈번한 경우에는 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)(Referencing)로 설계하여 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복을 최소화해야 한다.

---

## Ⅰ. 개요 및 필요성

### RDBMS 한계와 문서형 DB의 등장
전자상거래의 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 예로 들면, 상품마다 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이 달라(의류는 사이즈·색상, 전자기기는 [전압](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)·주파수 등) RDBMS는 EAV(Entity-[Attribute](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)-Value) 패턴이나 수십 개의 NULL 컬럼이 생기는 문제가 발생한다. 문서형 DB는 각 상품을 독립된 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 문서로 저장하여 이 문제를 해결한다.

### 문서 구조 예시

```json
{
  "_id": "prod_9900",
  "name": "무선 이어폰",
  "category": "electronics",
  "specs": {
    "bluetooth": "5.3",
    "battery_hours": 30,
    "noise_cancelling": true
  },
  "reviews": [
    {"user": "user_1", "rating": 5, "text": "최고!"},
    {"user": "user_2", "rating": 4, "text": "좋아요"}
  ],
  "tags": ["wireless", "audio", "premium"],
  "created_at": "2026-04-21T09:00:00Z"
}
```

> 중첩 객체(specs), [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)(reviews, tags), 다양한 타입을 단일 문서에 표현 — RDBMS에서는 최소 3개 테이블이 필요.

### 대표 솔루션 비교

| 솔루션 | 특징 | 주요 사용처 |
|:---:|:---|:---:|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/540_mongodb/">MongoDB</a></strong> | BSON 저장, 풍부한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), Aggregation [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) | 범용 문서 저장 |
| **CouchDB** | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/), [오프라인 우선](/studynote/04_software_engineering/09_cloud_native_ai_architecture/579_offline_first_pwa_service_worker/)([Offline-First](/studynote/04_software_engineering/09_cloud_native_ai_architecture/579_offline_first_pwa_service_worker/)), [MVCC](/studynote/11_design_supervision/06_exam_summary/449_mvcc/) | 모바일 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| **Firestore** | 구글 관리형, 실시간 리스너, [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | 모바일/웹 앱 |
| **Couchbase** | 메모리 우선, N1QL(SQL-like), 캐시 통합 | 고성능 모바일 |

📢 **섹션 요약 비유**
> RDBMS가 모든 정보를 표 형식에 맞춰 기록하는 공공기관 서류라면, 문서형 DB는 자유 양식 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 폴더다. 사람마다 필요한 서류가 다를 때 자유 양식이 훨씬 편리하지만, 양식이 없어서 모든 서류를 뒤지는 데는 더 오래 걸릴 수도 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 문서 저장 구조 ([MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 기준)

```text
+----------------------------------------------------------+
|              MongoDB 데이터 계층 구조                      |
|                                                          |
|  Database: shop_db                                       |
|  |                                                       |
|  +-- Collection: products  (테이블 개념)                  |
|  |   +-- Document { _id: "prod_1", ... }                 |
|  |   +-- Document { _id: "prod_2", ... }                 |
|  |   +-- Document { _id: "prod_3", specs:{...} }         |
|  |                                                       |
|  +-- Collection: users                                   |
|  |   +-- Document { _id: ObjectId("..."), name:... }     |
|  |   +-- Document { _id: ObjectId("..."), ... }          |
|  |                                                       |
|  +-- Collection: orders                                  |
|      +-- Document { items:[{...},{...}], total:... }     |
|                                                          |
|  * 컬렉션: 스키마 강제 없음 (각 문서가 다른 필드 가능)        |
|  * _id: 기본 인덱스 (ObjectId = 12바이트 타임스탬프+랜덤)    |
+----------------------------------------------------------+
```

### [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)([Embedding](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) vs [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)(Referencing)

```text
+------------------------------------------------------------+
|              데이터 모델링 전략 비교                          |
|                                                            |
|  ■ 임베딩(Embedding) — 비정규화                              |
|  +----------------------------------+                      |
|  | Order Document                   |                      |
|  |  { orderId: 1001,                |                      |
|  |    customer: { name:"홍길동",    | <- 고객 정보 내장        |
|  |                email:"..." },    |                      |
|  |    items: [                      |                      |
|  |      { sku:"A1", qty:2,          | <- 상품 정보 내장        |
|  |        price:9900 },             |                      |
|  |      { sku:"B2", qty:1,          |                      |
|  |        price:49900 }             |                      |
|  |    ]                             |                      |
|  |  }                               |                      |
|  +----------------------------------+                      |
|  장점: 단일 조회(1 I/O)   단점: 데이터 중복, 큰 문서           |
|                                                            |
|  ■ 참조(Referencing) — 정규화                               |
|  +------------+    +-----------------------+               |
|  | Order      |    | Customer              |               |
|  | { custId:  |---> | { _id: "cust_1",      |               |
|  |   "cust_1" |    |   name: "홍길동" }     |               |
|  | }          |    +-----------------------+               |
|  +------------+                                            |
|  장점: 데이터 정규화, 갱신 단순  단점: 여러 번 조회 필요         |
+------------------------------------------------------------+
```

### CouchDB [오프라인 우선](/studynote/04_software_engineering/09_cloud_native_ai_architecture/579_offline_first_pwa_service_worker/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)

| 기능 | 설명 |
|:---:|:---|
| [MVCC](/studynote/11_design_supervision/06_exam_summary/449_mvcc/) (Multi-Version [Concurrency Control](/studynote/05_database/04_transactions_concurrency/508_concurrency_control/)) | 충돌 없는 동시 수정 |
| 양방향 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 오프라인 작업 후 온라인 시 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| 개정(Revision) _rev 필드 | 문서 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 추적, 충돌 감지 |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) | 모든 연산이 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 메서드로 표현 |

📢 **섹션 요약 비유**
> [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)은 식당 메뉴판에 재료·가격·영양 정보를 모두 함께 인쇄하는 것이다. 한 번에 모든 정보를 볼 수 있지만, 재료 가격이 바뀌면 메뉴판 전체를 다시 인쇄해야 한다. [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)는 재료 정보를 별도 부록에 두는 것 — 갱신은 쉽지만 두 번 펼쳐봐야 한다.

---

## Ⅲ. 비교 및 연결

### 문서형 DB vs RDBMS 설계 패러다임 차이

| 설계 질문 | RDBMS 접근 | [Document](/studynote/14_data_engineering/01_infrastructure/037_document/) DB 접근 |
|:---:|:---:|:---:|
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 정의 시점 | 개발 전 고정 | 런타임 유연 변경 |
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 표현 | [외래 키](/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) + [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) | [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 또는 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 설계 기준 | 엔티티 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 접근 패턴(Query Pattern) |
| [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 방향 | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 선호 | 비정규화 선호 |
| 다형성 처리 | 복잡([상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | 자연스러움 |

### Firestore 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)

```text
Mobile App ---> Firestore ---> 실시간 스냅샷 리스너
                          <--- 변경 즉시 Push (WebSocket)

특징:
- 오프라인 캐시: 인터넷 연결 끊겨도 로컬에서 읽기 가능
- 낙관적 업데이트: 로컬 즉시 반영 후 서버 동기화
- 보안 규칙: 서버 측 클라이언트 접근 제어
```

📢 **섹션 요약 비유**
> RDBMS가 "무슨 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는가"를 기준으로 설계한다면, 문서형 DB는 "어떻게 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽을 것인가"를 기준으로 설계한다. 요리사(개발자)가 아니라 손님([쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴)의 입맛에 맞춰 메뉴([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/))를 구성하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)/[참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 선택 기준

| 조건 | 권장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
|:---|:---:|
| 읽기 빈도가 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다 훨씬 높음 | [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| 자식 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 부모와 함께 항상 조회 | [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| 자식 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 개수가 무제한 증가 | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| 자식 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 독립적으로 조회 | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| 동일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 여러 문서에 공유 | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| 문서 크기 16MB 초과 위험 | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) (버킷 패턴) |

### [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) Aggregation [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) 예시

```text
db.orders.aggregate([
  { $match: { status: "completed" } },     // 필터
  { $unwind: "$items" },                   // 배열 분해
  { $group: {                              // 집계
      _id: "$items.category",
      revenue: { $sum: "$items.price" }
  }},
  { $sort: { revenue: -1 } },              // 정렬
  { $limit: 5 }                            // 상위 5개
])
```

📢 **섹션 요약 비유**
> Aggregation Pipeline은 공장 컨베이어 벨트와 같다. 원자재(문서)가 벨트를 타고 이동하면서 각 공정(필터->분해->집계->정렬)을 순서대로 거쳐 최종 제품(집계 결과)으로 완성된다. 단계마다 불필요한 재료를 걸러내어 최종 단계에서 처리해야 할 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양을 줄이는 것이 효율의 핵심이다.

---

## Ⅴ. 기대효과 및 결론

### 문서형 DB 도입 효과 요약

| 분야 | 전통 RDBMS | 문서형 DB |
|:---:|:---:|:---:|
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 비용 | ALTER TABLE (다운타임 위험) | 즉시 적용 |
| 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 조회 | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)+ 테이블 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) | 단일 문서 조회 |
| 개발 민첩성 | 제한적 | 높음 |
| 수평 확장 | 어려움 | [샤딩](/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) 지원 |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | 완전한 ACID | 문서 단위 ACID ([MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 4.0+: 다문서) |

### 결론
문서형 DB는 현대 [애자일](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 개발 환경과 다형적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조에 최적화된 선택이다. 특히 MongoDB는 4.0 이후 다문서 ACID [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 지원하여 과거의 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 약점을 보완했다. 기술사 시험에서는 <strong><a href="/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/">임베딩</a> vs <a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a> 설계 근거</strong>, <strong>Aggregation <a href="/studynote/12_it_management/02_itsm_itil/082_pipeline/">Pipeline</a> 활용</strong>, <strong><a href="/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a> 키 선택 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이 핵심 논점이다.

📢 **섹션 요약 비유**
> 문서형 DB 도입은 종이 서류를 스마트 태블릿으로 바꾸는 것과 같다. 더 이상 기존 양식에 억지로 맞출 필요 없이, 내용이 바뀌면 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)만 업데이트하면 된다. 단, 검색이 필요한 필드에는 반드시 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)(디지털 목차)를 만들어야 효율이 유지된다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| BSON | 저장 형식 | Binary [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), ObjectId 포함 |
| Aggregation [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 메커니즘 | 단계별 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 |
| WiredTiger | 스토리지 엔진 | [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 기본 엔진, [MVCC](/studynote/11_design_supervision/06_exam_summary/449_mvcc/) 지원 |
| [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)/[참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) | 설계 패턴 | 비정규화 vs [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 트레이드오프 |
| Change Streams | 실시간 기능 | 문서 변경 이벤트 스트리밍 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계형 DB]
    |
    v
[NoSQL]
    |
    v
[문서형 DB]
    |
    v
[MongoDB]
    |
    v
[Atlas]
    |
    v
[Document API]
```

[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 한계를 보완하기 위해 NoSQL과 문서형 DB가 등장하고, [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 중심 활용으로 확장되는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 문서형 DB는 자유 일기장 같아요. 어떤 날은 그림만, 어떤 날은 글만 써도 되는 것처럼 문서마다 내용이 달라도 괜찮아요.
2. [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)은 도시락 하나에 밥·반찬·국을 모두 담는 것이고, [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)는 식당에서 각 메뉴를 따로 주문하는 것처럼 상황에 맞게 골라야 해요.
3. MongoDB는 가장 인기 있는 자유 일기장으로, 이제는 여러 일기를 동시에 쓸 때도 글자가 뒤섞이지 않는 [트랜잭션 기능](/studynote/12_it_management/04_sdlc_testing/142_fp_transaction_functions/)까지 갖췄어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 262

<- **이전**: [128. Redis (Remote Dictionary Server) — 인메모리 데이터 구조 서버](/studynote/16_bigdata/06_nosql/128_redis/)
**다음**: [130. MongoDB 아키텍처 — ReplicaSet/Sharding/Mongos](/studynote/16_bigdata/06_nosql/130_mongodb_architecture/) ->

---
