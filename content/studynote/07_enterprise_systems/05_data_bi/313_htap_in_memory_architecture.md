---
title: "HTAP In-Memory Architecture"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) (Hybrid Transactional/Analytical Processing)은 OLTP와 OLAP을 단일 인메모리 엔진에서 처리해 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 운영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실시간 분석한다.
> 2. **가치**: 기존 T+1일 배치 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 대비 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 <1초 달성으로, 재고 실시간 현황·실시간 사기 탐지·동적 가격 책정이 가능해진다.
> 3. **판단 포인트**: HTAP은 인메모리 비용이 높으므로, 분석이 운영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 최신성이 핵심인 경우(재고, 사기, 금융)에 한해 정당화된다.

## Ⅰ. 개요 및 필요성

전통적인 아키텍처는 [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) DB(MySQL, [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/))와 [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)(Teradata, Redshift)를 분리하고, 야간 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 배치로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 이동한다.
이 구조에서 분석 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 항상 T+1일(전날) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다.

HTAP은 이 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 레이턴시를 제거한다:
- 행 지향(Row-based) 델타 스토어: [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리
- 컬럼 지향(Column-based) 메인 스토어: [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 분석 처리
- 두 스토어가 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) (<1초)

대표 제품:
- SAP HANA: 엔터프라이즈 최초 상용 [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/)
- [TiDB](/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/) (PingCAP): [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) (TiKV + TiFlash)
- SingleStore (MemSQL): 인메모리 [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/)
- [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) In-Memory: [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) DB 추가 옵션

📢 **섹션 요약 비유**: HTAP은 주방과 홀이 하나인 오픈 키친이다. 요리([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))와 메뉴판 집계(분석)가 같은 공간에서 실시간으로 이루어진다.

## Ⅱ. 아키텍처 및 핵심 원리

### 이중 스토어 구조

| 스토어 | 형식 | 역할 | 최적화 |
|:---|:---|:---|:---|
| Delta Store (행) | 행 지향 (Row) | INSERT/UPDATE/DELETE ([OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화 |
| Main Store (열) | 컬럼 지향 (Column) | [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) 분석 ([OLAP](/studynote/12_it_management/05_security_compliance/316_olap/)) | 읽기·[압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 최적화 |
| [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 실시간 병합 | Delta -> Main 지속 병합 | <1초 신선도 |

### [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 인식 메모리 레이아웃

```
NUMA Node 0              NUMA Node 1
+----------------+       +----------------+
|  CPU Cores 0-7 |       |  CPU Cores 8-15|
|  Local RAM 256G|       |  Local RAM 256G|
|  (빠른 접근)   |       |  (빠른 접근)   |
+-------+--------+       +--------+-------+
        |  Remote 접근 (2~3x 느림)  |
        +--------------------------+
-> HTAP 엔진은 쿼리를 로컬 NUMA 노드 데이터에 배치해 성능 극대화
```

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 이중 스토어 아키텍처

```
  애플리케이션 (OLTP)        분석 도구 (OLAP)
  +------------------+     +------------------+
  | INSERT/UPDATE    |     | SELECT SUM/GROUP |
  | (실시간 거래)     |     | (실시간 대시보드) |
  +--------+---------+     +--------+---------+
           | 쓰기                    | 분석 쿼리
           v                        v
  +--------------------------------------------+
  |           HTAP In-Memory Engine            |
  |  +----------------+   +------------------+ |
  |  |  Delta Store   |--->|  Main Store      | |
  |  |  (행 지향)      |   |  (컬럼 지향)     | |
  |  |  최신 변경분   |   |  사전 집계·압축  | |
  |  |  (인메모리)    |   |  (인메모리+NVM)  | |
  |  +----------------+   +------------------+ |
  |   실시간 동기화 <1초                         |
  |  +--------------------------------------+  |
  |  |  Persistence (로그+체크포인트)        |  |
  |  |  NVM (Optane) or SSD                 |  |
  |  +--------------------------------------+  |
  +--------------------------------------------+
```

### 전통 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) vs [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 비교

| 항목 | 전통 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) |
|:---|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 | T+1일 (야간 배치) | <1초 실시간 |
| 아키텍처 | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) DB + [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) + [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 단일 엔진 |
| 운영 복잡도 | 높음 ([ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인) | 낮음 (단일 시스템) |
| 비용 | [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 별도 (높음) | 인메모리 비용 (높음, 다른 종류) |
| 워크로드 간섭 | 없음 (완전 분리) | 있음 (리소스 경쟁) |

📢 **섹션 요약 비유**: 전통 ETL은 공장([OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/))에서 제품을 만들고 하루 끝에 창고([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))로 운반하는 것, HTAP은 공장과 전시장이 같은 건물에 있어 생산 즉시 전시되는 것이다.

## Ⅲ. 비교 및 연결

### [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 적합 vs 비적합 사례

| 항목 | [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 적합 | [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 비적합 |
|:---|:---|:---|
| 재고 실시간 현황 | ✅ 운영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 즉시 분석 | |
| 사기 실시간 탐지 | ✅ <1초 결정 필요 | |
| 분기 재무 리포트 | | ❌ 배치 DW로 충분 |
| 역사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수년치 분석 | | ❌ 대용량 컬럼 스토어 적합 |

📢 **섹션 요약 비유**: HTAP은 고급 레스토랑의 라이브 쿠킹이다. 비용이 높지만 손님이 원하는 순간 바로 요리가 나온다. 구내식당(배치 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/))은 저렴하지만 점심 한 번에 모아서 나온다.

## Ⅳ. 실무 적용 및 기술사 판단

### [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 요구: <1초가 비즈니스 가치 창출하는가? (재고, 사기, 금융)
- [ ] 인메모리 비용 정당화: 전체 워킹셋이 수백GB~수TB -> 비용 대비 [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 계산
- [ ] 워크로드 격리: OLTP와 [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 간 리소스 경쟁 방지 설계
- [ ] [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/): NVM(Intel Optane) 또는 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 기반 체크포인트 주기 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)
- [ ] HA 구성: 인메모리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 방지를 위한 레플리카 구성 필수

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| HTAP에 역사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전부 적재 | 메모리 비용 폭발 | [핫 데이터](/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/)만 인메모리, 콜드는 컬럼 스토어 |
| [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 무제한 실행 | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 간섭 | 리소스 그룹 분리, [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) |
| [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 체크포인트 생략 | 재시작 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 | WAL + 주기적 체크포인트 |

�� **섹션 요약 비유**: HTAP에 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 올리는 건 SUV에 이사짐을 전부 싣는 것이다. 기름값(메모리 비용)이 감당이 안 된다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 기반 | [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) |
|:---|:---|:---|
| 재고 현황 반영 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | T+1일 | <1초 |
| 사기 탐지 반응 시간 | 15분~수시간 | 수십ms |
| 아키텍처 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 수 | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) + [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) + [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) + BI = 4+ | 1 ([HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 엔진) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 문제 | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 오류 시 불일치 | 단일 시스템 ACID |

### 한계 및 선결 과제

- 인메모리 비용: 1TB RAM 클러스터 구성 비용 수억 원 수준
- 워크로드 간섭: [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)/[OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 간 리소스 경쟁 세심한 튜닝 필요
- [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성 높음 (SAP HANA, SingleStore 상용 라이선스)
- [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [TiDB](/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/): 운영 복잡도 높음, 전문 인력 필요

📢 **섹션 요약 비유**: HTAP은 비싸지만 강력한 슈퍼카다. 속도가 필요하고 비용을 감당할 수 있다면 최고의 선택이지만, 출퇴근에만 쓴다면 세단으로 충분하다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) | 아키텍처 | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)+[OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 단일 엔진 |
| Delta Store | 구성 요소 | 행 지향 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 처리 |
| Main Store | 구성 요소 | 컬럼 지향 분석 처리 |
| [NUMA](/studynote/02_operating_system/06_memory_management/377_numa_allocation/) | 하드웨어 | 메모리 접근 최적화 |
| SAP HANA | 제품 | 엔터프라이즈 [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 선두 |
| [TiDB](/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/) | 제품 | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) (TiKV+TiFlash) |

### 📈 관련 키워드 및 발전 흐름도

```
OLTP/OLAP 완전 분리 - ETL 지연 (T+1 분석)
    |
    v
인메모리 DB (SAP HANA) - 단일 엔진 HTAP 시도
    |
    v
행·열 혼합 스토리지 + 분리된 워크로드 격리
    |
    v
TiDB/SingleStore - 분산 HTAP 클라우드 네이티브
    |
    v
실시간 OLAP 분석 (Freshness < 1s) 달성
```

> **키워드**: [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/), [In-Memory Database](/studynote/05_database/01_db_architecture_relational/046_in_memory_db_imdb/), SAP HANA, [TiDB](/studynote/05_database/05_distributed_nosql_newsql/293_elt_process/), Row Store, Column Store, [Real-Time Analytics](/studynote/13_cloud_architecture/05_data_engineering/277_real_time_analytics_architecture/)

### 👶 어린이를 위한 3줄 비유 설명

1. HTAP은 주문을 받으면서 동시에 "오늘 어떤 음식이 많이 팔렸는지" 바로 알 수 있는 스마트 식당이에요.
2. 일반 식당(기존 시스템)은 하루가 끝나야 판매 기록을 정리해요.
3. 비용이 비싸서 정말 빠른 분석이 필요한 곳(은행, 재고 관리)에서 써요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 313 / 482

<- **이전**: [312. 해시 샤딩 및 디렉토리 샤딩 분산 DB 스케일 아웃 (Hash Sharding vs Directory Sharding)](/studynote/07_enterprise_systems/05_data_bi/312_hash_sharding_directory_sharding/)
**다음**: [314. 텔레메트리 빅데이터 파싱 수집 엔진 (Telemetry Big Data Parsing)](/studynote/07_enterprise_systems/05_data_bi/314_telemetry_bigdata_parsing/) ->

---
