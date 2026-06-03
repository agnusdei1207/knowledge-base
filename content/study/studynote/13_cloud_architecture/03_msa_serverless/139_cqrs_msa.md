+++
weight = 139
title = "139. CQRS (Command Query Responsibility Segregation) - 명령·조회 분리"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CQRS는 **[[289_cqrs_db|쓰기]]([[271_command_pattern|Command]])와 읽기(Query)를 별도의 모델·저장소로 분리**하는 패턴이며, [[289_cqrs_db|쓰기]]는 [[093_normalization|정규화]]된 RDBMS, 읽기는 비정규화된 뷰/ElasticSearch로 최적화한다.
> 2. **가치**: 단일 모델로 [[289_cqrs_db|쓰기]]·읽기를 모두 처리하면 **읽기 최적화(비정규화)와 [[289_cqrs_db|쓰기]] 정합성([[093_normalization|정규화]])이 상충**하지만, CQRS는 각각을 독립적으로 최적화하여 성능과 확장성을 동시에 달성한다.
> 3. **판단 포인트**: Event Sourcing과 자연스럽게 결합([[289_cqrs_db|쓰기]]=이벤트 저장, 읽기=이벤트 프로젝션)하며, 읽기·[[289_cqrs_db|쓰기]] 간 **[[650_eventual_consistency|Eventual Consistency]]**를 허용해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
쓰기 모델: INSERT/UPDATE → 정규화 RDBMS (정합성↑)
이벤트 발행: Outbox → Kafka → 프로젝션
읽기 모델: SELECT → 비정규화 뷰/ElasticSearch (성능↑)
```

- **📢 섹션 요약 비유**: CQRS는 **도서관의 서고([[289_cqrs_db|쓰기]], [[104_classification_analysis|분류]] 정리)와 열람실(읽기, 빠른 검색)**을 분리하는 것이다.

---

## Ⅱ~Ⅴ. 결론

CQRS는 **읽기·[[289_cqrs_db|쓰기]] 비율이 극단적(예: 읽기 95%+)인 시스템의 핵심 패턴**이며, [[307_event_sourcing|Event Sourcing]]·Outbox와 함께 [[619_msa_traffic_hardware|MSA]] 고급 아키텍처를 구성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[306_cqrs|CQRS]]** | 명령·조회 분리 |
| **[[307_event_sourcing|Event Sourcing]]** | CQRS와 자연 결합 |
| **Projection** | 이벤트→읽기 모델 변환 |
| **[[650_eventual_consistency|Eventual Consistency]]** | 읽기·[[289_cqrs_db|쓰기]] 간 [[015_지연_데이터_관점|지연]] |
| **Materialized [[151_sql_view_virtual_table|View]]** | 읽기 최적화 뷰 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CRUD (단일 모델)] → [CQS (Bertrand Meyer, 1988)]
    → [CQRS (Greg Young, 2010)]
    → [CQRS + Event Sourcing (2012~)]
    → [현재: Axon Framework — CQRS+ES 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CQRS는 도서관의 **서고(정리)와 열람실(검색)을 분리**하는 거예요.
2. 책을 정리([[289_cqrs_db|쓰기]])하는 곳과 **빠르게 찾는(읽기) 곳**이 다르면 더 효율적이에요.
3. 읽는 사람이 **100명인데 쓰는 사람은 1명**이면 분리가 훨씬 좋아요!
