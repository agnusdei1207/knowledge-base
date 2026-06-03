---
title: 10. 스키마 온 라이트 (Schema-on-Write) - 저장 전 정규화/ETL을 통해 스키마에 맞게 정제 (DW)
date: '2024-05-15'
description: 관계형 DB와 데이터 웨어하우스의 표준 접근법인 스키마 온 라이트의 구조적 특징, ETL 병목 해결 방안 및 데이터 품질 보증
  체계를 분석합니다.
tags:
- data_engineering
---

# [[005_schema|스키마]] 온 라이트 ([[505_schema|Schema]]-on-Write)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[001_dikw_pyramid|데이터]]를 스토리지에 기록(Write)하기 전에 반드시 사전에 정의된 엄격한 구조(테이블, 컬럼, [[001_dikw_pyramid|데이터]] 타입)를 만족하도록 강제하는 [[002_database_definition|데이터베이스]] 저장 철학입니다.
> 2. **가치**: 불량 [[001_dikw_pyramid|데이터]](Garbage)가 시스템에 진입하는 것을 원천 차단하여 완벽한 [[001_dikw_pyramid|데이터]] 품질([[270_data_quality_great_expectations|Data Quality]])과 정합성을 보장하며, 읽기(Read) 시점의 파싱 오버헤드를 없애 극도로 빠른 분석 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]을 제공합니다.
> 3. **융합**: 전통적인 RDBMS와 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]])의 근간이며, 최근에는 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]([[210_data_lakehouse_delta_lake|Data Lakehouse]])의 오픈 테이블 포맷과 결합하여 빅데이터 환경에서도 [[003_integrity|무결성]]을 지키는 핵심 기제로 부활하고 있습니다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

**[[005_schema|스키마]] 온 라이트 ([[505_schema|Schema]]-on-Write)**는 IT 시스템 역사상 가장 오랫동안, 그리고 가장 신뢰받아 온 [[001_dikw_pyramid|데이터]] 통제 패러다임입니다. 

금융, 의료, [[081_erp_enterprise_resource_planning|ERP]] 시스템처럼 단 1원의 오차나 [[001_dikw_pyramid|데이터]] 누락도 허용되지 않는 환경에서는 "아무 [[001_dikw_pyramid|데이터]]나 일단 넣고 보자"는 식의 접근이 불가능합니다. "나이는 반드시 정수(Integer)여야 하고, 주민번호는 13자리 문자열이어야 한다"는 명확한 계약(Contract)이 선행되어야만 [[298_qkv_attention|쿼리]] 결과를 100% 신뢰할 수 있습니다. [[005_schema|스키마]] 온 라이트는 [[001_dikw_pyramid|데이터]]가 디스크에 안착하기 직전에 강력한 문지기 역할을 하여, 규격을 벗어난 [[001_dikw_pyramid|데이터]]는 과감히 튕겨냅니다. 

빅데이터 초창기에는 이러한 엄격함이 적재 속도를 저하시키는 병목([[617_io_bottleneck|Bottleneck]])으로 치부되어 유연한 [[208_data_lake_schema_on_read|데이터 레이크]]([[009_schema_on_read|Schema-on-Read]])에 밀리는 듯 보였습니다. 그러나 [[001_dikw_pyramid|데이터]] 호수가 관리되지 않는 쓰레기장([[288_data_swamp_metadata_management_absence|Data Swamp]])으로 변질되고 [[001_dikw_pyramid|데이터]] 사이언티스트들이 불량 [[001_dikw_pyramid|데이터]]를 정제하는 데 업무 시간의 80%를 낭비하는 문제가 심화되면서, **"[[289_cqrs_db|쓰기]] 시점의 강력한 품질 통제"**라는 [[005_schema|스키마]] 온 라이트의 철학적 가치가 [[052_data_governance_framework|데이터 거버넌스]] 차원에서 다시 절대적인 중요성을 확보하게 되었습니다.

```text
[스키마 온 라이트의 엄격한 방어막 아키텍처]

       [ Source Data (정상, 오염, 포맷 불량 혼재) ]
                       ↓
┌────────────────────────────────────────────────────────┐
│ [ ETL Pipeline / Data Validator ] (문지기 역할)        │
│ 1. 형변환: "String -> Integer"                         │ (변환 및 정제 오버헤드 발생)
│ 2. 필터링: "나이 컬럼에 문자가 있으면 Reject"          │
└──────────────────────┬─────────────────────────────────┘
                       │ (통과한 순도 100% 정제 데이터만 허용)
                       ▼
┌────────────────────────────────────────────────────────┐
│ [ Data Warehouse / RDBMS ] (Schema-on-Write)           │
│ CREATE TABLE users (age INT NOT NULL, name VARCHAR);   │ (사전 정의된 테이블 레이아웃)
└──────────────────────┬─────────────────────────────────┘
                       │ (읽기 오버헤드 제로, 인덱스 활용)
             [ BI / 고속 SQL 분석가 ]
```
이 도식은 [[005_schema|스키마]] 온 라이트가 작동하는 전형적인 [[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load) 파이프라인의 구조를 보여줍니다. [[001_dikw_pyramid|데이터]]는 DB에 진입하기 전에 구조 [[395_verification_process_review|검증]], 타입 캐스팅, [[003_integrity|무결성]] 제약 조건(Not Null, [[072_foreign_key_fk|외래 키]] 등)의 살벌한 검열을 거칩니다. 이 과정에서 파이프라인 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])이 발생하지만, 톨게이트를 통과해 내부에 저장된 [[001_dikw_pyramid|데이터]]는 '단일 진실 공급원(SSOT)'으로서의 무결점을 획득합니다. 분석가는 [[001_dikw_pyramid|데이터]]가 깨져 있을까 봐 걱정할 필요 없이 인덱스가 타는 [[148_5g_embb_urllc_mmtc|초고속]] 조인([[521_join|Join]]) [[298_qkv_attention|쿼리]]만 작성하면 됩니다.

> 📢 **섹션 비유**: [[005_schema|스키마]] 온 라이트는 클럽 입구의 '엄격한 기도(Bouncer)'와 같습니다. 드레스 코드가 맞지 않으면 절대 들여보내지 않아서 입장 줄은 길어질 수 있지만, 일단 클럽 안에 들어간 사람들은 완벽한 물관리가 되어 있어 파티([[001_dikw_pyramid|데이터]] 분석)가 최상의 품질로 진행됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[005_schema|스키마]] 온 라이트 시스템의 내부는 디스크 I/O 최적화와 [[012_metadata|메타데이터]]의 강력한 결합으로 이루어져 있습니다. RDBMS와 [[209_data_warehouse_schema_on_write|DW]] 엔진이 [[001_dikw_pyramid|데이터]]를 기록하는 과정을 뜯어보면 왜 이것이 읽기 속도를 극대화하는지 알 수 있습니다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 실무 비유 |
|:---|:---|:---|:---|
| **[[020_ddl|Data Definition Language]] ([[020_ddl|DDL]])** | 시스템 뼈대 [[087_process_state_transition|생성]] | `CREATE TABLE`을 통해 [[001_dikw_pyramid|데이터]] 딕셔너리([[012_metadata|메타데이터]])에 [[005_schema|스키마]] 공간 사전 할당 | 건물의 철골 설계도 작성 |
| **Constraint Checker** | [[003_integrity|무결성]] 제약 [[395_verification_process_review|검증]] | 적재(Insert) [[191_transaction_concept_states|트랜잭션]] 발생 시 Not Null, Unique, Type 검사를 통과해야만 Commit | 불량 자재 반입 통제관 |
| **Storage Layout** | 물리적 디스크 블록 할당 | INT(4Byte), CHAR(10Byte) 등 사전에 고정된 [[074_byte|바이트]] 크기만큼 디스크 [[286_page_frame|페이지]] 슬롯에 밀어 넣음 | 딱 맞는 크기의 얼음틀 |
| **[[154_database_index_b_tree_search_optimization|Index]] [[064_b_tree|B-Tree]] / Bitmap** | 고속 검색 구조 형성 | [[289_cqrs_db|쓰기]] 시점에 [[005_schema|스키마]] 구조를 바탕으로 검색 트리를 동시에 업데이트 ([[289_cqrs_db|쓰기]] 속도 저하 유발) | 책의 뒤쪽 색인(목차) 자동 [[087_process_state_transition|생성]] |
| **Query [[088_optimizer|Optimizer]]** | [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 최적화 | 사전에 고정된 [[005_schema|스키마]] 통계 정보(카디널리티, 분포도)를 믿고 가장 빠른 조인 경로 연산 | 내비게이션의 최단 거리 계산 |

[[005_schema|스키마]] 온 라이트의 숨겨진 강력함은 물리적 디스크에 [[001_dikw_pyramid|데이터]]가 기록되는 **고정 길이 메모리 레이아웃(Storage Layout)**에서 나옵니다.

```text
[스키마 온 라이트의 물리적 메모리/디스크 블록 레이아웃]

(사전 스키마 정의: ID INT(4byte), Status CHAR(2byte), Age INT(4byte))

[ Disk Page Block (4KB) 내부 구조 ]
┌──────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Header│ Record 1 (10 bytes)  │ Record 2 (10 bytes)  │ Record 3 (10 bytes)  │
│ 메타 │ [0001][OK][0025]     │ [0002][ER][0030]     │ [0003][OK][0021]     │
└──────┴──────────────────────┴──────────────────────┴──────────────────────┘
         ↑ (Offset: +0)         ↑ (Offset: +10)        ↑ (Offset: +20)
```
이 도식은 엔진이 왜 [[005_schema|스키마]]를 강제하는지 그 물리적 이유를 보여줍니다. [[343_json|JSON]]([[009_schema_on_read|Schema-on-Read]]) 같은 가변 길이 텍스트 파일은 100만 번째 레코드를 찾으려면 파일의 처음부터 쉼표와 괄호를 일일이 파싱하며 읽어야 합니다(Full Scan). 반면, [[005_schema|스키마]] 온 라이트에서는 레코드 길이가 정확히 [[489_raid_10_hybrid|10]] Byte로 고정(Fix)되어 있으므로, 옵티마이저는 `(목표 행 번호) * 10 Byte`라는 단순한 오프셋 수식만으로 디스크의 특정 블록으로 즉시 점프(Random Access)할 수 있습니다. 즉, 쓸 때 고생한 덕분에 읽을 때 파싱 오버헤드가 제로(0)가 되는 경이로운 읽기 최적화를 달성합니다.

> 📢 **섹션 비유**: 짐을 아무렇게나 박스에 우겨넣는 대신(가변 길이), 정확히 규격화된 블록(레고)으로 끼워 맞추어 건물을 지어두면, 나중에 10층의 3번째 방을 찾을 때 처음부터 세어볼 필요 없이 설계도만 보고 헬기로 단숨에 날아갈 수 있는 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

현대의 [[001_dikw_pyramid|데이터]] 엔지니어는 저장 구조를 설계할 때 속도(적재 vs 조회)의 트레이드오프를 철저히 계산해야 합니다.

**1. [[505_schema|Schema]]-on-Write vs [[009_schema_on_read|Schema-on-Read]] 의사결정 매트릭스**

| 비교 항목 | [[505_schema|Schema]]-on-Write (RDBMS/[[209_data_warehouse_schema_on_write|DW]]) | [[009_schema_on_read|Schema-on-Read]] ([[208_data_lake_schema_on_read|Data Lake]]) | 아키텍처 판단 포인트 |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 구조의 변동성** | 안정적 (잘 변하지 않는 비즈니스 로직) | 매우 유동적 (수시로 필드가 추가/삭제됨) | 소스 시스템의 변화 빈도 |
| **목적의 명확성** | 무엇을 분석할지 미리 명확히 정의됨 | 일단 모아두고 나중에 가치를 발굴함 | [[298_qkv_attention|쿼리]] 패턴의 사전 예측 가능성 |
| **처리 병목의 위치** | 적재 시점 ([[215_etl_vs_elt_pipeline|ETL]] 파이프라인 [[015_지연_데이터_관점|지연]]) | 조회 시점 ([[298_qkv_attention|쿼리]] 실행 시간 증가) | 실시간 유입량 vs 빠른 응답성 |
| **[[001_dikw_pyramid|데이터]] 타입** | 테이블/관계형 [[001_dikw_pyramid|데이터]] 전용 | [[568_logs_distributed_logging_elk_fluentd|로그]], 이미지, 영상 등 100% 수용 | [[001_dikw_pyramid|데이터]] 다양성 한계치 |
| **유지보수 비용** | [[005_schema|스키마]] 변경(ALTER TABLE) 시 막대한 다운타임 | [[298_qkv_attention|쿼리]] 코드([[151_sql_view_virtual_table|View]])만 변경하면 즉시 반영 | 운영 조직의 [[004_agile_relation|애자일]]([[004_agile_relation|Agile]]) 대응력 |

**2. 융합 관점: [[146_lakehouse|레이크하우스]]와 [[194_medallion_architecture_bronze_silver_gold|메달리온 아키텍처]]의 결합**
최근 [[001_dikw_pyramid|데이터]] 생태계는 두 사상의 대립을 끝내고 **공존**의 길을 찾았습니다. [[194_medallion_architecture_bronze_silver_gold|메달리온 아키텍처]]([[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]])에서 **Bronze(원시) 존**은 [[001_dikw_pyramid|데이터]] 유실을 막기 위해 **[[009_schema_on_read|스키마 온 리드]]**로 무조건 쏟아붓습니다. 이후 Spark나 dbt를 통해 정제를 거쳐 최종 BI가 바라보는 **Gold(집계) 존**에 도달할 때는 엄격한 제약 조건을 강제하는 **[[005_schema|스키마]] 온 라이트** 방식([[147_delta_lake|Delta Lake]]/Iceberg의 [[005_schema|스키마]] 강제화 기능)을 적용합니다. 이 융합을 통해 수집의 유연성과 조회의 정합성이라는 두 마리 토끼를 모두 잡게 되었습니다.

> 📢 **섹션 비유**: [[505_schema|Schema]]-on-Read가 뭐든 섞어버리는 '아이디어 회의(브레인스토밍)' 단계라면, [[505_schema|Schema]]-on-Write는 그것을 논리적이고 엄격한 포맷의 '최종 결재 기안서'로 작성하는 단계입니다. 조직에는 이 두 가지 단계가 순차적으로 모두 필요합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 [[005_schema|스키마]] 온 라이트를 고수하다 보면 빈번하게 마주하는 장애물은 **[[005_schema|스키마]] 에볼루션([[505_schema|Schema]] Evolution)**에 따른 시스템 마비입니다.

**실무 시나리오: 소스 [[005_schema|스키마]] 변경으로 인한 [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 붕괴 ([[082_pipeline|Pipeline]] Breakage)**
- **상황**: [[090_service_kubernetes_network_load_balancing|서비스]] 개발팀이 앱을 업데이트하면서 운영 DB의 `user_profile` 테이블에 `phone_number`라는 새로운 컬럼을 추가함. 하지만 [[209_data_warehouse_schema_on_write|DW]] 담당자에게 이를 알리지 않음. 야간 배치가 돌면서 [[215_etl_vs_elt_pipeline|ETL]] 서버가 DW에 [[001_dikw_pyramid|데이터]]를 밀어 넣으려 했으나, [[209_data_warehouse_schema_on_write|DW]] 테이블에는 해당 컬럼이 정의되어 있지 않아 에러([[505_schema|Schema]] Mismatch)를 뱉고 전체 파이프라인이 중단됨.
- **원인**: 엄격한 [[005_schema|스키마]] 온 라이트 방어막이, 예고되지 않은 구조 변경을 '오염'으로 간주하고 시스템을 셧다운시킨 정상적이지만 파괴적인 동작.
- **해결 (장애 대응 및 [[124_decision_tree|의사결정 트리]])**:

```text
[스키마 불일치(Mismatch) 예방 및 자동화 파이프라인 트리]

[ 운영 DB 컬럼 추가 (Schema Change 발생) ]
         ↓
[ ETL 추출 과정 (Extract) ]
         ↓
[Q1. 타겟 DW와 소스의 스키마 메타데이터가 일치하는가?]
 ├── (Yes) ──> [ 정상 적재 (Load) 진행 ]
 └── (No) ─> [Q2. 파이프라인에 스키마 자동 진화(Schema Evolution) 로직이 있는가?]
               ├── (No) ──> [ 장애 발생 및 Alert 발송 ] -> 엔지니어가 수동으로 ALTER TABLE 수행 (다운타임 발생)
               └── (Yes) ─> [ Schema Evolution 실행 ]
                            ├── 1. 타겟 DW에 자동으로 신규 컬럼 ALTER ADD
                            └── 2. 기존 데이터의 해당 컬럼은 NULL로 채움 (역방향 호환성 유지)
                            └──> [ 중단 없이 정상 적재 재개 ]
```
이 의사결정 흐름도는 [[005_schema|스키마]] 온 라이트의 경직성을 어떻게 소프트웨어 엔지니어링으로 우회할 것인가를 보여줍니다. 실무에서는 개발팀과 [[001_dikw_pyramid|데이터]]팀 간의 소통 부재로 [[005_schema|스키마]] 변경 에러가 일상적으로 발생합니다. 이를 극복하기 위해 최신 [[001_dikw_pyramid|데이터]] 플랫폼([[541_cassandra|Snowflake]], [[147_delta_lake|Delta Lake]])은 `mergeSchema=true` 같은 옵션을 제공하여, 새로 들어온 [[001_dikw_pyramid|데이터]]의 컬럼이 타겟 테이블에 없다면 자동으로 테이블 구조를 진화시키는([[505_schema|Schema]] Evolution) 유연성을 [[005_schema|스키마]] 온 라이트 환경에 부여하고 있습니다.

**운영 및 아키텍처 [[435_checklist_based_testing|체크리스트]]**
- **강결합 완화**: [[215_etl_vs_elt_pipeline|ETL]] 실패가 전체 비즈니스 대시보드의 먹통으로 이어지지 않도록 데드 레터 큐(DLQ, Dead Letter [[058_queue|Queue]])를 도입하여 실패한 레코드만 옆으로 빼내고 정상 레코드는 통과시키고 있는가?
- **[[236_data_contract|데이터 계약]]([[236_data_contract|Data Contract]])**: 개발팀(생산자)과 [[001_dikw_pyramid|데이터]]팀(소비자) 사이에 [[005_schema|스키마]]를 함부로 변경하지 않겠다는 명시적인 [[014_api_posix|API]] 규약([[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] 활용 등)이 거버넌스로 체계화되어 있는가?

> 📢 **섹션 비유**: [[005_schema|스키마]] 온 라이트는 완벽히 짜여진 '기차 선로'와 같아서 열차([[001_dikw_pyramid|데이터]])가 선로 규격을 조금이라도 벗어나면 즉시 탈선(장애)합니다. 따라서 선로를 변경할 때는 앞뒤 부서가 완벽한 무전([[236_data_contract|데이터 계약]])을 주고받아야 대참사를 막을 수 있습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[005_schema|스키마]] 온 라이트는 고품질 [[001_dikw_pyramid|데이터]]의 마지막 보루로서 비즈니스 의사결정의 신뢰도를 결정짓습니다.

| 기대 효과 구분 | 유연성 우선 시 ([[009_schema_on_read|Schema-on-Read]] 남용) | [[005_schema|스키마]] 온 라이트 (엄격 통제) 적용 시 |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 정합성** | 분석가가 [[298_qkv_attention|쿼리]]를 짤 때마다 결과가 달라짐 (Garbage [[001_dikw_pyramid|데이터]] 방치) | 전사적으로 100% 동일하게 [[395_verification_process_review|검증]]된 단일 지표(SSOT) 획득 |
| **조회 [[282_performance_tactics|성능]] ([[141_latency|Latency]])**| [[298_qkv_attention|쿼리]] 시점마다 타입 변환과 예외 처리 파싱으로 인한 [[015_지연_데이터_관점|지연]] | 인덱스와 파티셔닝이 완벽히 적용되어 즉각적인 밀리초(ms) 응답 |

**미래 전망 및 결론**
"가장 빠른 [[298_qkv_attention|쿼리]]는 디스크에서 읽을 필요가 없는 [[298_qkv_attention|쿼리]]이고, 그다음으로 빠른 [[298_qkv_attention|쿼리]]는 [[005_schema|스키마]]가 완벽히 고정된 [[298_qkv_attention|쿼리]]이다." [[005_schema|스키마]] 온 라이트는 단순히 낡은 RDBMS의 잔재가 아닙니다. 머신러닝의 [[282_performance_tactics|성능]]이 결국 입력 [[001_dikw_pyramid|데이터]]의 품질에 종속되는 현시대에, **가비지 인 가비지 아웃(Garbage-In Garbage-Out)**을 막는 가장 엔지니어링적인 해법입니다. 
미래의 [[001_dikw_pyramid|데이터]] 아키텍처는 유연한 수집(Read)과 엄격한 서빙(Write)이 융합된 [[146_lakehouse|레이크하우스]] 형태로 귀결되고 있습니다. 즉, 시스템 깊숙한 곳에서는 [[005_schema|스키마]] 온 라이트의 강력한 제약과 타입 [[395_verification_process_review|검증]](Type Checking)이 부활하여, [[001_dikw_pyramid|데이터]]의 [[003_integrity|무결성]]을 지키는 보이지 않는 뼈대 역할을 영원히 수행할 것입니다.

> 📢 **섹션 비유**: 흙탕물([[004_unstructured_data|비정형 데이터]])을 그냥 퍼서 마시는 유연성도 생존에 필요하지만, 결국 문명 사회의 건강을 지키는 것은 수백 번의 깐깐한 필터링([[505_schema|Schema]]-on-Write)을 거쳐 가정에 배달되는 완벽한 수돗물 정수 시스템입니다.

---
### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[208_data_warehouse_schema_on_write_inmon|Data Warehouse]] ([[209_data_warehouse_schema_on_write|DW]])** | [[005_schema|스키마]] 온 라이트 철학이 극대화된 전사적 통합 [[001_dikw_pyramid|데이터]] 저장소 ([[311_inmon|Inmon]] 모델).
- **[[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load)** | 원시 [[001_dikw_pyramid|데이터]]를 [[005_schema|스키마]] 온 라이트 구조에 맞게 깎고 정제하여 쑤셔 넣는 가장 고통스러운 [[645_data_pipeline_acceleration|데이터 파이프라인]] 병목 구간.
- **[[505_schema|Schema]] Evolution ([[005_schema|스키마]] 진화)** | 경직된 [[005_schema|스키마]] 온 라이트 시스템이 [[001_dikw_pyramid|데이터]] 구조의 변화를 수용할 수 있도록 [[012_metadata|메타데이터]]를 유연하게 갱신하는 기능.
- **[[236_data_contract|Data Contract]] ([[236_data_contract|데이터 계약]])** | [[001_dikw_pyramid|데이터]] 생산팀과 [[001_dikw_pyramid|데이터]] 소비팀 간에 사전에 [[005_schema|스키마]]([[014_api_posix|API]] 규격)를 약속하여, 함부로 컬럼을 삭제하거나 변경하지 못하게 막는 거버넌스 체계.
- **RDBMS** | 엄격한 2차원 테이블과 컬럼 타입을 강제하여 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]([[003_integrity|Integrity]])과 [[191_transaction_concept_states|트랜잭션]]을 100% 보장하는 전통적 [[002_database_definition|데이터베이스]].

### 📈 관련 키워드 및 발전 흐름도

```text
[스키마 온 라이트 (Schema-on-Write) — 저장 전 스키마 강제 적용]
    │
    ▼
[데이터 웨어하우스 (DW) — 정형 스키마 기반 분석 저장소]
    │
    ▼
[스키마 온 리드 (Schema-on-Read) — 저장 후 읽기 시 스키마 적용]
    │
    ▼
[데이터 레이크 (Data Lake) — 원시 데이터 유연 저장]
    │
    ▼
[레이크하우스 (Lakehouse) — 스키마 온 라이트 + 리드 통합]
    │
    ▼
[데이터 메시 (Data Mesh) — 도메인별 분산 스키마 자율 관리]
```
[[005_schema|스키마]] 온 라이트는 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 사전에 보장하며, [[009_schema_on_read|스키마 온 리드]]와의 상호 보완을 통해 [[146_lakehouse|레이크하우스]]·[[001_dikw_pyramid|데이터]] 메시라는 현대 [[001_dikw_pyramid|데이터]] 아키텍처로 수렴했다.

### 👶 어린이를 위한 3줄 비유 설명
1. 만약 장난감 상자에 '동그라미 블록'만 넣을 수 있는 구멍([[005_schema|스키마]])이 뚫려 있다면, 네모나 세모 블록은 절대 들어갈 수 없어요.
2. 넣을 때 모양을 맞춰야 해서 귀찮고 시간은 걸리지만, 상자 안에는 무조건 완벽한 동그라미 블록만 있다는 걸 우리는 100% 믿을 수 있죠.
3. 이렇게 상자에 넣기 전에 모양이 맞는지 엄격하게 검사해서, 나중에 꺼내 쓸 때 에러가 없게 만드는 방법을 '[[005_schema|스키마]] 온 라이트'라고 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 10 / 258

← **이전**: [[009_schema_on_read|9. 스키마 온 리드 (Schema-on-Read) - 저장 시엔 원시 그대로 두고, 쿼리(읽기)할 때 스키마를 동적으로 부여 (데이터]]
**다음**: [[011_distributed_computing_scale_out|11. 분산 컴퓨팅 스케일 아웃 (Scale-out) - 저가형 범용 x86 서버(Commodity Hardware) 대수를 늘려 성능]] →

---
