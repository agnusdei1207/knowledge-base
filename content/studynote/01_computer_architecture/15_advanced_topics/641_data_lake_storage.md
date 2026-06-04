---
title: "641. 데이터 레이크 (Data Lake) 스토리지 아키텍처"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))는 정형·반정형·비정형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원본에 가깝게 오래 보존하는 저장 계층이며, 핵심은 <strong>저비용 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 저장 + <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> + 컴퓨트 분리</strong>다.
> 2. **가치**: 분석 목적이 바뀌어도 원본을 다시 해석할 수 있어 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 학습, 포렌식, 재처리에 강하고, [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) ([Object Storage](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) 기반으로 대규모 확장이 쉽다.
> 3. **판단 포인트**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 승패는 많이 저장했는가가 아니라 <strong>작은 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> <a href="/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a>, 계층화, <a href="/studynote/05_database/07_exam_summary/394_catalog_metadata/">카탈로그</a> 품질, 테이블 포맷 운영</strong>을 제대로 설계했는가에 달려 있다.

---

## Ⅰ. 개요 및 필요성

[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 스토리지 아키텍처는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집하는 순간 완벽한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 강제하지 않고, 다양한 원천 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원본에 가깝게 받아 두는 저장 구조다. 전통적인 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/), [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))는 정제된 표 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석에는 강하지만, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·센서 스트림·이미지·음성처럼 형태가 불규칙한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 빠르게 받아들이는 데는 준비 비용이 크다. 그래서 현대 시스템은 "먼저 안전하게 저장하고, 나중에 의미를 붙이는" 별도 저장 계층을 두기 시작했다.

이 구조가 중요한 이유는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 가치가 수집 시점보다 활용 시점에 결정되기 때문이다. 오늘은 단순 보관용 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)라도 내일은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 될 수 있고, 장애가 나면 몇 달 전 원본이 원인 규명의 유일한 증거가 되기도 한다. 결국 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 저장소 그 자체라기보다, 미래의 분석 가능성을 보존하는 원본 자산 창고에 가깝다.

또한 하드웨어 관점에서도 의미가 크다. 대용량 하드디스크 드라이브 (Hard Disk Drive, [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 또는 저비용 [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) 노드에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 눕혀 저장하고, 필요할 때만 별도 컴퓨트 클러스터를 붙이면 저장 단가와 계산 단가를 각각 따로 최적화할 수 있기 때문이다.

- **📢 섹션 요약 비유**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 재료를 요리 전에 모두 손질해 놓는 주방이 아니라, 신선한 식재료를 그대로 보관해 두는 거대한 냉장 창고와 같다. 요리법이 바뀌어도 재료만 살아 있으면 새로운 메뉴를 다시 만들 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 핵심은 저장 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)와 분석 엔진을 강하게 결합하지 않는 데 있다. 저장 쪽은 큰 용량과 낮은 단가를 우선하고, 계산 쪽은 필요한 순간에만 확장한다. 이때 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)와 테이블 포맷이 둘 사이의 번역기 역할을 맡아, 같은 원본을 여러 엔진이 안전하게 공유하게 만든다.

| 계층 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 원본 보관 계층 | 수집 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수정 없이 적재 | 대용량 순차 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/), [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| 정제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계층 | 분석 친화적 포맷으로 재구성 | [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/), [압축](/studynote/02_operating_system/06_memory_management/347_compaction/), 컴팩션 |
| [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 계층 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), 위치, 계보 관리 | [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 빠른 조회 |
| 컴퓨트 계층 | 질의, 배치, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 실행 | 저장과 분리된 수평 확장 |
| [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 계층 | 장애·비용 최적화 | 삭제 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 계층화, 소거 부호화 |

아래 그림은 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)가 왜 "스토리지는 싸게, 컴퓨트는 탄력적으로"라는 철학을 갖는지 보여준다.

```text
+--------------------------------------------------------------+
| Disaggregated data lake path                                |
+--------------------------------------------------------------+
| Ingest nodes ---> Raw object tier ---> Table metadata         |
|                     |                      |                 |
|                     |                      +--> query engines |
|                     |                      +--> batch jobs    |
|                     |                      +--> AI training   |
|                     |                                        |
|                     +--> Cold archive / erasure coding        |
+--------------------------------------------------------------+
```

이 구조에서 [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)가 많이 쓰이는 이유는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템보다 객체 수 확장과 내구성 관리에 유리하기 때문이다. 대신 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 너무 많아지면 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 부하와 조회 지연이 커지므로, 배치 적재·컴팩션·열 지향 포맷 변환을 통해 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기를 정리해야 한다. 또한 복제만 고집하면 저장 효율이 나빠지므로, 대규모 환경에서는 소거 부호화 ([Erasure Coding](/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/))와 수명주기 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계하는 경우가 많다.

- **📢 섹션 요약 비유**: 이 구조는 창고와 작업장을 분리한 공장과 같다. 창고는 싸고 넓게 짓고, 작업장은 주문이 몰릴 때만 인력을 더 넣어 빠르게 돌리는 방식이 가장 경제적이다.

---

## Ⅲ. 비교 및 연결

[데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)를 제대로 이해하려면 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), [데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) ([Lakehouse](/studynote/16_bigdata/07_data_lake/146_lakehouse/)), [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/) 계열과의 경계를 같이 봐야 한다. 같은 "분석 저장소"처럼 보이지만, 언제 구조를 강제하는지와 어떤 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 기본으로 삼는지에 따라 운영 방식이 크게 달라진다.

| 구분 | [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/) |
| :--- | :--- | :--- | :--- |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 시점 | 적재 전 고정 | 조회 시 해석 | 원본 보존 + 테이블 규칙 |
| 주저장 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) | 고성능 분석 저장소 | [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) 중심 | [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) 중심 |
| 강점 | 빠른 정형 질의 | 유연한 원본 보관 | 유연성과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 절충 |
| 약점 | 비정형 수용성 낮음 | 거버넌스 없으면 늪화 | 운영 복잡도 증가 |
| 대표 판단 | 보고서 중심 | 원본 축적·재처리 중심 | 분석 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 강화 |

과거에는 [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/) ([Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Distributed File System](/studynote/02_operating_system/09_file_system/553_distributed_file_system/), [HDFS](/studynote/14_data_engineering/01_infrastructure/013_hdfs/)) 기반 레이크가 많았지만, 최근에는 클라우드 [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)와 [오픈 테이블 포맷](/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) ([Open Table Format](/studynote/16_bigdata/10_governance/196_opentableformat/))이 중심이 되고 있다. 아파치 아이스버그 ([Apache Iceberg](/studynote/16_bigdata/07_data_lake/148_apache_iceberg/)), 델타 레이크 ([Delta Lake](/studynote/16_bigdata/07_data_lake/147_delta_lake/)), 아파치 후디 ([Apache Hudi](/studynote/16_bigdata/07_data_lake/149_apache_hudi/)) 같은 형식이 등장한 이유도 바로 이 지점이다. 단순 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 묶음만으로는 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), 삭제, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화, [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 처리가 어려웠기 때문이다.

즉 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 "원본 저장소", [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 "원본 저장소 위에 질서와 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 덧댄 형태"로 기억하면 경계가 잡힌다. 둘은 경쟁 관계라기보다, [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)가 성숙해지며 관리 계층을 더 얹은 진화 관계에 가깝다.

- **📢 섹션 요약 비유**: [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)가 규격 박스에 정리된 창고라면, [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 다양한 재료가 들어오는 대형 물류장이고, [레이크하우스](/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 그 물류장에 바코드와 재고 시스템까지 붙인 형태다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 많이 모은다"보다 "나중에 다시 찾고 다시 읽을 수 있는가"가 더 중요하다. 예를 들어 스마트 공장에서 초당 수집되는 진동·온도 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 원본 그대로 보관해 두면, 설비 고장 후 몇 달 전부터 있었던 미세 패턴을 다시 학습용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 사용할 수 있다. 보안 포렌식에서도 패킷 원본, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 사용자 행위 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 함께 보관한 레이크가 있으면, 침해 흔적을 시간축으로 다시 재구성하기 쉽다.

기술사 판단에서는 다음 세 가지를 함께 본다. 첫째, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 종류와 활용 목적이 자주 바뀌는가. 둘째, [메타데이터 카탈로그](/studynote/05_database/06_dw_olap_trends/342_metadata_catalog/)와 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 주체가 있는가. 셋째, 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [억제](/studynote/09_security/13_secops_ir_forensics/656_ir_containment/), 핫·콜드 계층화, 삭제 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 같은 운영 규칙이 있는가. 이 셋이 없으면 저장 용량만 커지고 실제 활용도는 떨어진다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 무작정 업로드만 하고 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 만들지 않는 경우
- 짧은 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 수천만 개의 작은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 쪼개 저장하는 경우
- 장기 보관 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 고가의 올플래시 스토리지에 넣어 비용 구조를 망치는 경우
- 원본 보존과 정제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 책임 구분 없이 덮어쓰기를 허용하는 경우

- **📢 섹션 요약 비유**: 입고 기록도 없이 상자를 계속 던져 넣는 창고는 언젠가 창고가 아니라 쓰레기 더미가 된다. [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)도 보관 그 자체보다 정리 규칙이 먼저 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수명 주기 전체의 유연성을 높인다. 수집 시점에는 빠르게 받아들이고, 활용 시점에는 분석 엔진을 바꿔 가며 재해석할 수 있기 때문에 새로운 분석 요구나 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 프로젝트에 대응하기 쉽다. 또한 컴퓨트와 스토리지를 분리하면 저장량 증가가 곧바로 고가 서버 증설로 이어지지 않아 비용 구조도 예측 가능해진다.

다만 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)가 만능은 아니다. 강한 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 짧은 응답 시간을 요구하는 온라인 거래 처리 (Online [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing, [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) 시스템에는 부적합하며, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 운영 역량이 없으면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스웜프 ([Data Swamp](/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/))로 빠르게 타락한다. 그래서 이 아키텍처는 "많이 담는 기술"이 아니라, <strong>원본 보존과 재해석 가능성을 중심으로 설계하는 장기 자산 관리 기술</strong>로 기억하는 편이 정확하다.

- **📢 섹션 요약 비유**: [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 오늘의 질문에만 답하는 서랍이 아니라, 미래의 질문까지 대비해 원본 기록을 남겨 두는 거대한 도서관 서고와 같다. [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계가 좋으면 시간이 지날수록 더 큰 가치를 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) ([Object Storage](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) | [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 저비용·고확장 하부 저장소 역할을 맡는다 |
| [메타데이터 카탈로그](/studynote/05_database/06_dw_olap_trends/342_metadata_catalog/) ([Metadata Catalog](/studynote/05_database/05_distributed_nosql_newsql/301_metadata_catalog/)) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위치와 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), 계보를 연결해 늪화를 막는다 |
| 열 지향 포맷 (Columnar Format) | 정제 계층에서 스캔 효율과 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)률을 높인다 |
| 소거 부호화 ([Erasure Coding](/studynote/01_computer_architecture/15_advanced_topics/681_erasure_coding/)) | 대용량 보관 시 복제보다 높은 저장 효율을 제공한다 |
| [오픈 테이블 포맷](/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/) ([Open Table Format](/studynote/16_bigdata/10_governance/196_opentableformat/)) | [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), 삭제, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화 같은 운영 질서를 레이크 위에 추가한다 |

### 📈 관련 키워드 및 발전 흐름도

```text
전통 파일 서버 · 스토리지 어레이
    |
    v
하둡 분산 파일 시스템 (HDFS)
    |
    v
오브젝트 스토리지 기반 데이터 레이크
    |
    v
오픈 테이블 포맷 · 메타데이터 강화
    |
    v
레이크하우스 · AI 학습 데이터 플랫폼
```

이 흐름은 저장 장치 중심 사고가 원본 보존 중심 사고로 이동한 뒤, 다시 관리 질서와 분석 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 덧붙이는 방향으로 진화했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 사진, 목소리, 글, 그림을 다 넣어 둘 수 있는 아주 큰 보물 창고예요.
2. 처음에는 그냥 넣어 두지만, 나중에 필요할 때 "이걸로 로봇 공부를 시키자" 하고 다시 꺼내 쓸 수 있어요.
3. 대신 어디에 무엇을 넣었는지 표지를 잘 붙여 두지 않으면, 큰 창고가 금방 엉망이 된답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 642 / 803

<- **이전**: [640. 오픈 컴퓨트 프로젝트 (OCP, Open Compute Project)](/studynote/01_computer_architecture/15_advanced_topics/640_open_compute_project/)
**다음**: [642. 옵저버빌리티 (Observability) HW 텔레메트리](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) ->

---
