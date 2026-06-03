+++
title = "56. 데이터 가상화 및 연방 쿼리 (Federated Query) - Trino와 Presto의 분산 SQL 엔진"
date = 2026-04-10

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 옮기지 않고, 여러 저장소를 논리적으로 하나처럼 보이게 만드는 방식이다.
> 2. **가치**: [연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/)([Federated Query](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/))는 SQL (Structured Query Language) 한 줄로 이종 저장소를 조인해 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Extract, Transform, Load) 복사 비용을 줄인다.
> 3. **판단 포인트**: 커넥터, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 실행, 프레디킷 푸시다운(predicate pushdown), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 거버넌스가 성능과 안정성을 좌우한다.

---

## Ⅰ. 개요 및 필요성

전통적인 분석 방식은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 창고로 계속 복사해야 했다. 하지만 복사할수록 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 비용, 중복, 품질 저하가 생긴다.

[데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 "옮기지 말고 묻자"는 발상이다. 원본은 각 시스템에 두고, [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)만 전달해 결과를 받아오는 방식이므로 최신성과 유연성이 좋다.

- **📢 섹션 요약 비유**: 책을 다 옮겨 오지 않고, 필요한 순간에 각 도서관에 질문만 보내는 방식이다.

---

## Ⅱ. 핵심 구조와 실행 방식

[연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/) 엔진은 질문을 해석하고, 필요한 일을 여러 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스에 나눠 보낸다.

```text
클라이언트 SQL
      ↓
Coordinator
      ↓
Connectors ──> MySQL / PostgreSQL / S3 / 로그 저장소
      ↓
Workers
      ↓
결과 병합
```

- **[Coordinator](/knowledge-base/studynote/05_database/04_transactions_concurrency/250_coordinator_participant_2pc_roles/)**는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 분석하고 작업을 쪼갠다.
- **Connector**는 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스와 통신하는 어댑터다.
- **Worker**는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 실행과 결과 집계를 담당한다.
- **Predicate Pushdown**은 가능한 필터를 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스 쪽으로 내려 보내서 불필요한 이동을 줄인다.

- **📢 섹션 요약 비유**: 총괄 안내원이 질문을 분해해서 각 부서에 나눠 보내고, 답만 다시 모아 주는 구조다.

---

## Ⅲ. [연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/)의 처리 흐름

하나의 SQL 문이 바로 실행되는 것이 아니라 여러 단계로 나뉜다.

1. 파싱과 분석으로 테이블, 조건, 조인을 이해한다.
2. 실행 계획으로 어느 소스에서 무엇을 가져올지 정한다.
3. 가능한 조건은 원격 소스에 밀어 넣는다.
4. 필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 가져와 워커가 병렬로 처리한다.
5. 조인과 집계를 마친 뒤 최종 결과를 합친다.

이 과정에서 네트워크 이동량을 줄이고, 각 소스의 강점을 활용하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 주문서를 쪼개서 각 가게에 보내고, 완성된 접시만 한 번에 모아 오는 주방이다.

---

## Ⅳ. 실무 시나리오와 적용 분야

[연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사보다 빠르게 답이 필요할 때 특히 유용하다.

- 운영 DB와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장소를 한 번에 조회한다.
- `MySQL`, `PostgreSQL`, `RDBMS (Relational Database Management System)`와 `S3 (Simple Storage Service)`를 조인한다.
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 웨어하우스를 동시에 조회한다.
- 대시보드에서 실시간성 높은 탐색 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 실행한다.

반대로 원본 시스템의 부하가 큰 경우나 조인이 지나치게 무거운 경우에는 주의가 필요하다.

- **📢 섹션 요약 비유**: 급할 때는 직접 시장에 가지 않고, 여러 가게에서 필요한 재료만 즉시 받아 오는 방식이다.

---

## Ⅴ. 장점, 한계, 그리고 운영 기준

장점은 명확하다. 복사 비용이 줄고, 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바로 보며, 하나의 SQL로 이종 소스를 다룰 수 있다.

하지만 한계도 있다. [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/), 소스별 권한 차이, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 불일치, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 치우침, 무거운 조인 때문에 성능이 흔들릴 수 있다.

실무에서는 다음을 지켜야 한다.

- 자주 쓰는 필터는 소스 쪽으로 최대한 밀어 보낸다.
- 소스 권한과 행 단위 접근 제어를 명확히 한다.
- 무거운 반복 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 물리화(materialization) 여부를 검토한다.
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경을 감시한다.

- **📢 섹션 요약 비유**: 편리한 지름길도 교통량이 너무 많으면 막히므로, 길 안내와 통제가 같이 있어야 한다.

---

## 관련 개념 맵

```text
원본 데이터 소스
      ↓
Connector / Coordinator / Worker
      ↓
분산 실행 + Pushdown
      ↓
통합 SQL 결과
```

---

## 관련 키워드 및 발전 흐름도

1. [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Extract, Transform, Load) 중심 복사 → 중앙 집중형 분석
2. [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) → 원본 유지와 논리적 통합
3. [연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/) → SQL 하나로 다중 소스 접근
4. Trino와 Presto → 고성능 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진의 대중화
5. Lakehouse와 semantic layer → [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 물리화를 함께 쓰는 방향

---

## 어린이를 위한 3줄 비유 설명

[연방 쿼리](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/)는 여러 도서관에 있는 책을 다 옮기지 않고, 필요한 질문만 보내는 거예요.  
각 도서관이 답을 보내 주면, 가운데 컴퓨터가 한 번에 정리해 줘요.  
그래서 책은 그대로 있는데도 한 번에 찾을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 56 / 258

← **이전**: [55. 컴퓨트와 스토리지 분리 (Separation of Compute and Storage / Cloud DW)](/knowledge-base/studynote/14_data_engineering/01_infrastructure/055_separation_of_compute_and_storage_cloud_dw/)
**다음**: [57. 시계열 데이터베이스 (Time-Series Database, TSDB) - 다운샘플링과 보존 정책](/knowledge-base/studynote/14_data_engineering/01_infrastructure/057_tsdb_downsampling_retention_policy/) →

---
