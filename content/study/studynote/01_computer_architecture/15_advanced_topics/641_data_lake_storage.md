---
title: 641. 데이터 레이크 (Data Lake) 스토리지 아키텍처
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]])는 정형·반정형·비정형 [[001_dikw_pyramid|데이터]]를 원본에 가깝게 오래 보존하는 저장 계층이며, 핵심은 **저비용 [[136_variance|분산]] 저장 + [[012_metadata|메타데이터]] + 컴퓨트 분리**다.
> 2. **가치**: 분석 목적이 바뀌어도 원본을 다시 해석할 수 있어 [[231_ai_turing_test|인공지능]] ([[001_artificial_intelligence|Artificial Intelligence]], [[190_ai_llm_requirements_specification|AI]]) 학습, 포렌식, 재처리에 강하고, [[494_object_storage|오브젝트 스토리지]] ([[494_object_storage|Object Storage]]) 기반으로 대규모 확장이 쉽다.
> 3. **판단 포인트**: [[208_data_lake_schema_on_read|데이터 레이크]]의 승패는 많이 저장했는가가 아니라 **작은 [[501_file_definition_logical_record|파일]] [[656_ir_containment|억제]], 계층화, [[394_catalog_metadata|카탈로그]] 품질, 테이블 포맷 운영**을 제대로 설계했는가에 달려 있다.

---

## Ⅰ. 개요 및 필요성

[[208_data_lake_schema_on_read|데이터 레이크]] 스토리지 아키텍처는 [[001_dikw_pyramid|데이터]]를 수집하는 순간 완벽한 [[005_schema|스키마]]를 강제하지 않고, 다양한 원천 [[001_dikw_pyramid|데이터]]를 원본에 가깝게 받아 두는 저장 구조다. 전통적인 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]], [[209_data_warehouse_schema_on_write|DW]])는 정제된 표 [[001_dikw_pyramid|데이터]] 분석에는 강하지만, [[568_logs_distributed_logging_elk_fluentd|로그]]·센서 스트림·이미지·음성처럼 형태가 불규칙한 [[001_dikw_pyramid|데이터]]를 빠르게 받아들이는 데는 준비 비용이 크다. 그래서 현대 시스템은 "먼저 안전하게 저장하고, 나중에 의미를 붙이는" 별도 저장 계층을 두기 시작했다.

이 구조가 중요한 이유는 [[001_dikw_pyramid|데이터]]의 가치가 수집 시점보다 활용 시점에 결정되기 때문이다. 오늘은 단순 보관용 [[568_logs_distributed_logging_elk_fluentd|로그]]라도 내일은 [[190_ai_llm_requirements_specification|AI]] 학습 [[001_dikw_pyramid|데이터]]가 될 수 있고, 장애가 나면 몇 달 전 원본이 원인 규명의 유일한 증거가 되기도 한다. 결국 [[208_data_lake_schema_on_read|데이터 레이크]]는 저장소 그 자체라기보다, 미래의 분석 가능성을 보존하는 원본 자산 창고에 가깝다.

또한 하드웨어 관점에서도 의미가 크다. 대용량 하드디스크 드라이브 (Hard Disk Drive, [[465_hdd_structure|HDD]]) 또는 저비용 [[494_object_storage|오브젝트 스토리지]] 노드에 [[001_dikw_pyramid|데이터]]를 눕혀 저장하고, 필요할 때만 별도 컴퓨트 클러스터를 붙이면 저장 단가와 계산 단가를 각각 따로 최적화할 수 있기 때문이다.

- **📢 섹션 요약 비유**: [[208_data_lake_schema_on_read|데이터 레이크]]는 재료를 요리 전에 모두 손질해 놓는 주방이 아니라, 신선한 식재료를 그대로 보관해 두는 거대한 냉장 창고와 같다. 요리법이 바뀌어도 재료만 살아 있으면 새로운 메뉴를 다시 만들 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[208_data_lake_schema_on_read|데이터 레이크]]의 핵심은 저장 [[121_transmission_media_guided_unguided|매체]]와 분석 엔진을 강하게 결합하지 않는 데 있다. 저장 쪽은 큰 용량과 낮은 단가를 우선하고, 계산 쪽은 필요한 순간에만 확장한다. 이때 [[012_metadata|메타데이터]]와 테이블 포맷이 둘 사이의 번역기 역할을 맡아, 같은 원본을 여러 엔진이 안전하게 공유하게 만든다.

| 계층 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 원본 보관 계층 | 수집 [[001_dikw_pyramid|데이터]]를 수정 없이 적재 | 대용량 순차 [[289_cqrs_db|쓰기]], [[112_checksum|체크섬]], [[288_version_ihl_tos_total_length|버전]] 관리 |
| 정제 [[001_dikw_pyramid|데이터]] 계층 | 분석 친화적 포맷으로 재구성 | [[179_table_partitioning_concept|파티셔닝]], [[347_compaction|압축]], 컴팩션 |
| [[012_metadata|메타데이터]] 계층 | [[005_schema|스키마]], 위치, 계보 관리 | [[394_catalog_metadata|카탈로그]] [[194_consistency_database_integrity|일관성]], 빠른 조회 |
| 컴퓨트 계층 | 질의, 배치, [[190_ai_llm_requirements_specification|AI]] 학습 실행 | 저장과 분리된 수평 확장 |
| [[571_protection_vs_security|보호]] 계층 | 장애·비용 최적화 | 삭제 [[164_policy|정책]], 계층화, 소거 부호화 |

아래 그림은 [[208_data_lake_schema_on_read|데이터 레이크]]가 왜 "스토리지는 싸게, 컴퓨트는 탄력적으로"라는 철학을 갖는지 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Disaggregated data lake path                                │
├──────────────────────────────────────────────────────────────┤
│ Ingest nodes ──▶ Raw object tier ──▶ Table metadata         │
│                     │                      │                 │
│                     │                      ├─▶ query engines │
│                     │                      ├─▶ batch jobs    │
│                     │                      └─▶ AI training   │
│                     │                                        │
│                     └─▶ Cold archive / erasure coding        │
└──────────────────────────────────────────────────────────────┘
```

이 구조에서 [[494_object_storage|오브젝트 스토리지]]가 많이 쓰이는 이유는 [[501_file_definition_logical_record|파일]] 시스템보다 객체 수 확장과 내구성 관리에 유리하기 때문이다. 대신 작은 [[501_file_definition_logical_record|파일]]이 너무 많아지면 [[012_metadata|메타데이터]] 부하와 조회 지연이 커지므로, 배치 적재·컴팩션·열 지향 포맷 변환을 통해 [[501_file_definition_logical_record|파일]] 크기를 정리해야 한다. 또한 복제만 고집하면 저장 효율이 나빠지므로, 대규모 환경에서는 소거 부호화 ([[681_erasure_coding|Erasure Coding]])와 수명주기 [[164_policy|정책]]을 함께 설계하는 경우가 많다.

- **📢 섹션 요약 비유**: 이 구조는 창고와 작업장을 분리한 공장과 같다. 창고는 싸고 넓게 짓고, 작업장은 주문이 몰릴 때만 인력을 더 넣어 빠르게 돌리는 방식이 가장 경제적이다.

---

## Ⅲ. 비교 및 연결

[[208_data_lake_schema_on_read|데이터 레이크]]를 제대로 이해하려면 [[209_data_warehouse_schema_on_write|DW]], [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] ([[146_lakehouse|Lakehouse]]), [[553_distributed_file_system|분산 파일 시스템]] 계열과의 경계를 같이 봐야 한다. 같은 "분석 저장소"처럼 보이지만, 언제 구조를 강제하는지와 어떤 [[121_transmission_media_guided_unguided|매체]]를 기본으로 삼는지에 따라 운영 방식이 크게 달라진다.

| 구분 | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] | [[208_data_lake_schema_on_read|데이터 레이크]] | [[146_lakehouse|레이크하우스]] |
| :--- | :--- | :--- | :--- |
| [[005_schema|스키마]] 시점 | 적재 전 고정 | 조회 시 해석 | 원본 보존 + 테이블 규칙 |
| 주저장 [[121_transmission_media_guided_unguided|매체]] | 고성능 분석 저장소 | [[494_object_storage|오브젝트 스토리지]] 중심 | [[494_object_storage|오브젝트 스토리지]] 중심 |
| 강점 | 빠른 정형 질의 | 유연한 원본 보관 | 유연성과 [[191_transaction_concept_states|트랜잭션]] 절충 |
| 약점 | 비정형 수용성 낮음 | 거버넌스 없으면 늪화 | 운영 복잡도 증가 |
| 대표 판단 | 보고서 중심 | 원본 축적·재처리 중심 | 분석 [[194_consistency_database_integrity|일관성]] 강화 |

과거에는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[553_distributed_file_system|분산 파일 시스템]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]], [[013_hdfs|HDFS]]) 기반 레이크가 많았지만, 최근에는 클라우드 [[494_object_storage|오브젝트 스토리지]]와 [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] ([[196_opentableformat|Open Table Format]])이 중심이 되고 있다. 아파치 아이스버그 ([[148_apache_iceberg|Apache Iceberg]]), 델타 레이크 ([[147_delta_lake|Delta Lake]]), 아파치 후디 ([[149_apache_hudi|Apache Hudi]]) 같은 형식이 등장한 이유도 바로 이 지점이다. 단순 [[501_file_definition_logical_record|파일]] 묶음만으로는 [[022_snapshot_backup_architecture|스냅샷]], 삭제, [[005_schema|스키마]] 진화, [[014_concurrency|동시성]] 처리가 어려웠기 때문이다.

즉 [[208_data_lake_schema_on_read|데이터 레이크]]는 "원본 저장소", [[146_lakehouse|레이크하우스]]는 "원본 저장소 위에 질서와 [[191_transaction_concept_states|트랜잭션]]을 덧댄 형태"로 기억하면 경계가 잡힌다. 둘은 경쟁 관계라기보다, [[208_data_lake_schema_on_read|데이터 레이크]]가 성숙해지며 관리 계층을 더 얹은 진화 관계에 가깝다.

- **📢 섹션 요약 비유**: [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]가 규격 박스에 정리된 창고라면, [[208_data_lake_schema_on_read|데이터 레이크]]는 다양한 재료가 들어오는 대형 물류장이고, [[146_lakehouse|레이크하우스]]는 그 물류장에 바코드와 재고 시스템까지 붙인 형태다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "[[001_dikw_pyramid|데이터]]를 많이 모은다"보다 "나중에 다시 찾고 다시 읽을 수 있는가"가 더 중요하다. 예를 들어 스마트 공장에서 초당 수집되는 진동·온도 [[568_logs_distributed_logging_elk_fluentd|로그]]를 원본 그대로 보관해 두면, 설비 고장 후 몇 달 전부터 있었던 미세 패턴을 다시 학습용 [[001_dikw_pyramid|데이터]]로 사용할 수 있다. 보안 포렌식에서도 패킷 원본, [[303_authentication_authorization_patterns|인증]] [[568_logs_distributed_logging_elk_fluentd|로그]], 사용자 행위 [[568_logs_distributed_logging_elk_fluentd|로그]]를 함께 보관한 레이크가 있으면, 침해 흔적을 시간축으로 다시 재구성하기 쉽다.

기술사 판단에서는 다음 세 가지를 함께 본다. 첫째, [[001_dikw_pyramid|데이터]] 종류와 활용 목적이 자주 바뀌는가. 둘째, [[342_metadata_catalog|메타데이터 카탈로그]]와 [[387_access_control_pattern|접근 통제]] 주체가 있는가. 셋째, 작은 [[501_file_definition_logical_record|파일]] [[656_ir_containment|억제]], 핫·콜드 계층화, 삭제 [[164_policy|정책]] 같은 운영 규칙이 있는가. 이 셋이 없으면 저장 용량만 커지고 실제 활용도는 떨어진다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[501_file_definition_logical_record|파일]]을 무작정 업로드만 하고 [[394_catalog_metadata|카탈로그]]를 만들지 않는 경우
- 짧은 [[568_logs_distributed_logging_elk_fluentd|로그]]를 수천만 개의 작은 [[501_file_definition_logical_record|파일]]로 쪼개 저장하는 경우
- 장기 보관 [[001_dikw_pyramid|데이터]]까지 고가의 올플래시 스토리지에 넣어 비용 구조를 망치는 경우
- 원본 보존과 정제 [[001_dikw_pyramid|데이터]]의 책임 구분 없이 덮어쓰기를 허용하는 경우

- **📢 섹션 요약 비유**: 입고 기록도 없이 상자를 계속 던져 넣는 창고는 언젠가 창고가 아니라 쓰레기 더미가 된다. [[208_data_lake_schema_on_read|데이터 레이크]]도 보관 그 자체보다 정리 규칙이 먼저 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [[208_data_lake_schema_on_read|데이터 레이크]]는 [[001_dikw_pyramid|데이터]] 수명 주기 전체의 유연성을 높인다. 수집 시점에는 빠르게 받아들이고, 활용 시점에는 분석 엔진을 바꿔 가며 재해석할 수 있기 때문에 새로운 분석 요구나 [[190_ai_llm_requirements_specification|AI]] 프로젝트에 대응하기 쉽다. 또한 컴퓨트와 스토리지를 분리하면 저장량 증가가 곧바로 고가 서버 증설로 이어지지 않아 비용 구조도 예측 가능해진다.

다만 [[208_data_lake_schema_on_read|데이터 레이크]]가 만능은 아니다. 강한 [[191_transaction_concept_states|트랜잭션]] [[194_consistency_database_integrity|일관성]]과 짧은 응답 시간을 요구하는 온라인 거래 처리 (Online [[191_transaction_concept_states|Transaction]] Processing, [[327_hint_handoff|OLTP]]) 시스템에는 부적합하며, [[012_metadata|메타데이터]] 운영 역량이 없으면 [[001_dikw_pyramid|데이터]] 스웜프 ([[288_data_swamp_metadata_management_absence|Data Swamp]])로 빠르게 타락한다. 그래서 이 아키텍처는 "많이 담는 기술"이 아니라, **원본 보존과 재해석 가능성을 중심으로 설계하는 장기 자산 관리 기술**로 기억하는 편이 정확하다.

- **📢 섹션 요약 비유**: [[208_data_lake_schema_on_read|데이터 레이크]]는 오늘의 질문에만 답하는 서랍이 아니라, 미래의 질문까지 대비해 원본 기록을 남겨 두는 거대한 도서관 서고와 같다. [[104_classification_analysis|분류]] 체계가 좋으면 시간이 지날수록 더 큰 가치를 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[494_object_storage|오브젝트 스토리지]] ([[494_object_storage|Object Storage]]) | [[208_data_lake_schema_on_read|데이터 레이크]]의 저비용·고확장 하부 저장소 역할을 맡는다 |
| [[342_metadata_catalog|메타데이터 카탈로그]] ([[301_metadata_catalog|Metadata Catalog]]) | [[501_file_definition_logical_record|파일]] 위치와 [[005_schema|스키마]], 계보를 연결해 늪화를 막는다 |
| 열 지향 포맷 (Columnar Format) | 정제 계층에서 스캔 효율과 [[347_compaction|압축]]률을 높인다 |
| 소거 부호화 ([[681_erasure_coding|Erasure Coding]]) | 대용량 보관 시 복제보다 높은 저장 효율을 제공한다 |
| [[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] ([[196_opentableformat|Open Table Format]]) | [[022_snapshot_backup_architecture|스냅샷]], 삭제, [[005_schema|스키마]] 진화 같은 운영 질서를 레이크 위에 추가한다 |

### 📈 관련 키워드 및 발전 흐름도

```text
전통 파일 서버 · 스토리지 어레이
    │
    ▼
하둡 분산 파일 시스템 (HDFS)
    │
    ▼
오브젝트 스토리지 기반 데이터 레이크
    │
    ▼
오픈 테이블 포맷 · 메타데이터 강화
    │
    ▼
레이크하우스 · AI 학습 데이터 플랫폼
```

이 흐름은 저장 장치 중심 사고가 원본 보존 중심 사고로 이동한 뒤, 다시 관리 질서와 분석 [[194_consistency_database_integrity|일관성]]을 덧붙이는 방향으로 진화했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[208_data_lake_schema_on_read|데이터 레이크]]는 사진, 목소리, 글, 그림을 다 넣어 둘 수 있는 아주 큰 보물 창고예요.
2. 처음에는 그냥 넣어 두지만, 나중에 필요할 때 "이걸로 로봇 공부를 시키자" 하고 다시 꺼내 쓸 수 있어요.
3. 대신 어디에 무엇을 넣었는지 표지를 잘 붙여 두지 않으면, 큰 창고가 금방 엉망이 된답니다.
