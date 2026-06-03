+++
title = "139. CQRS (Command Query Responsibility Segregation) - 명령·조회 분리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CQRS는 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>(<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/">Command</a>)와 읽기(Query)를 별도의 모델·저장소로 분리</strong>하는 패턴이며, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)는 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 RDBMS, 읽기는 비정규화된 뷰/ElasticSearch로 최적화한다.
> 2. **가치**: 단일 모델로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)·읽기를 모두 처리하면 <strong>읽기 최적화(비정규화)와 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 정합성(<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>)이 상충</strong>하지만, CQRS는 각각을 독립적으로 최적화하여 성능과 확장성을 동시에 달성한다.
> 3. **판단 포인트**: Event Sourcing과 자연스럽게 결합([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)=이벤트 저장, 읽기=이벤트 프로젝션)하며, 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 간 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a></strong>를 허용해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
쓰기 모델: INSERT/UPDATE → 정규화 RDBMS (정합성↑)
이벤트 발행: Outbox → Kafka → 프로젝션
읽기 모델: SELECT → 비정규화 뷰/ElasticSearch (성능↑)
```

- **📢 섹션 요약 비유**: CQRS는 <strong>도서관의 서고(<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>, <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> 정리)와 열람실(읽기, 빠른 검색)</strong>을 분리하는 것이다.

---

## Ⅱ~Ⅴ. 결론

CQRS는 <strong>읽기·<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 비율이 극단적(예: 읽기 95%+)인 시스템의 핵심 패턴</strong>이며, [Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/)·Outbox와 함께 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 고급 아키텍처를 구성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/">CQRS</a></strong> | 명령·조회 분리 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/">Event Sourcing</a></strong> | CQRS와 자연 결합 |
| **Projection** | 이벤트→읽기 모델 변환 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a></strong> | 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| <strong>Materialized <a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a></strong> | 읽기 최적화 뷰 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CRUD (단일 모델)] → [CQS (Bertrand Meyer, 1988)]
    → [CQRS (Greg Young, 2010)]
    → [CQRS + Event Sourcing (2012~)]
    → [현재: Axon Framework — CQRS+ES 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CQRS는 도서관의 <strong>서고(정리)와 열람실(검색)을 분리</strong>하는 거예요.
2. 책을 정리([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))하는 곳과 <strong>빠르게 찾는(읽기) 곳</strong>이 다르면 더 효율적이에요.
3. 읽는 사람이 <strong>100명인데 쓰는 사람은 1명</strong>이면 분리가 훨씬 좋아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 138 / 371

← **이전**: [138. Event Sourcing (MSA) - 상태 대신 이벤트를 저장](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/138_event_sourcing_msa/)
**다음**: [140. EDA (Event-Driven Architecture) - 이벤트 기반 아키텍처](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/) →

---
