---
title: 222. 스키마 온 라이트 (Schema-on-Write)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[010_schema_on_write|스키마 온 라이트]]([[010_schema_on_write|Schema-on-Write]])는 [[001_dikw_pyramid|데이터]]를 저장하기 **전에** 정형 [[005_schema|스키마]]를 강제 [[395_verification_process_review|검증]]하여 [[001_dikw_pyramid|데이터]] 품질을 보장하는 전통적 [[001_dikw_pyramid|데이터]] 관리 [[268_strategy_pattern|전략]]이다.
> 2. **가치**: [[215_etl_vs_elt_pipeline|ETL]] 파이프라인에서 사전 정제·변환을 완료하므로 저장된 [[001_dikw_pyramid|데이터]]는 **즉시 분석 가능한 고품질 상태**이며, [[316_olap|OLAP]] [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]이 예측 가능하다.
> 3. **판단 포인트**: 유연성과 민첩성이 떨어지므로 **[[005_schema|스키마]] 변경 비용이 크다**. [[208_data_lake_schema_on_read|데이터 레이크]] 시대에는 Schema-on-Read와 병행하는 [[146_lakehouse|레이크하우스]] 하이브리드 [[268_strategy_pattern|전략]]이 현대적 접근이다.

---

## Ⅰ. 개요 및 필요성

Schema-on-Write는 [[001_dikw_pyramid|데이터]]가 저장소에 기록되기 **이전 단계**에서 [[005_schema|스키마]](컬럼명, [[001_dikw_pyramid|데이터]] 타입, NOT NULL, FK 등)를 강제 [[395_verification_process_review|검증]]하는 방식이다. 전통적 관계형 [[002_database_definition|데이터베이스]](RDBMS)와 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]가 이 철학을 따른다.

이 방식이 필요한 이유는 명확하다. 분석·BI 시스템에서는 **[[001_dikw_pyramid|데이터]] 품질이 의사결정 품질과 직결**되기 때문이다. 잘못된 [[001_dikw_pyramid|데이터]] 타입, NULL 값, 중복 레코드가 섞인 채로 집계된 KPI는 비즈니스 판단 오류로 이어진다.

```
[Schema-on-Write 데이터 흐름]
┌─────────┐    ┌─────────────────────────────┐    ┌──────────────┐
│ 소스 DB  │ →  │       ETL 파이프라인           │ →  │  Data Warehouse │
│         │    │  ① Extract  ② Transform       │    │  (스키마 정의   │
│ ERP/CRM │    │  ③ Validate ④ Load            │    │   완벽한 테이블) │
└─────────┘    │  - NULL 체크  - 타입 변환       │    └──────────────┘
               │  - 중복 제거  - 도메인 코드 변환 │
               └─────────────────────────────┘
                   저장 전 모든 규칙 통과 강제
```

[[215_etl_vs_elt_pipeline|ETL]] 과정에서 [[005_schema|스키마]] 위반 [[001_dikw_pyramid|데이터]]는 **거부(Reject)** 처리되거나 오류 로그로 격리된다. 이를 통해 DW에는 항상 "믿을 수 있는 [[001_dikw_pyramid|데이터]]"만 존재하게 된다.

📢 **섹션 요약 비유**: Schema-on-Write는 공항 입국 심사와 같다. 비행기에서 내릴 때(저장 전) 여권·비자([[005_schema|스키마]])를 검사하여 통과한 사람만 입국(저장)할 수 있다. 입국한 사람은 모두 신원이 [[396_validation|확인]]된 상태다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 상세 흐름

```
소스 시스템                 ETL 서버                      DW 테이블
┌──────────┐    Extract    ┌──────────────────┐  Load  ┌────────────────┐
│ Oracle   │ ──────────▶  │  Staging Area     │ ─────▶ │ fact_sales     │
│ MySQL    │              │  ┌─────────────┐  │        │ (컬럼 타입 고정) │
│ SAP ERP  │    Transform │  │ 타입 변환     │  │        └────────────────┘
└──────────┘              │  │ NULL 처리    │  │        ┌────────────────┐
                          │  │ 중복 제거    │  │ ─────▶ │ dim_customer   │
                          │  │ 코드 매핑   │  │        └────────────────┘
                          │  │ 비즈니스 룰  │  │
                          │  │ 검증         │  │   ← Reject 로그
                          │  └─────────────┘  │   ← 실패 데이터 격리
                          └──────────────────┘
```

### [[005_schema|스키마]] [[395_verification_process_review|검증]] 유형

| [[395_verification_process_review|검증]] 유형 | 내용 | 예시 |
|:---|:---|:---|
| **타입 [[395_verification_process_review|검증]]** | 컬럼 [[001_dikw_pyramid|데이터]] 타입 일치 | 날짜 컬럼에 문자열 입력 거부 |
| **NULL 제약** | NOT NULL 컬럼 값 존재 [[396_validation|확인]] | 고객 ID NULL 거부 |
| **범위 [[395_verification_process_review|검증]]** | 허용 값 범위 내 [[396_validation|확인]] | 나이 컬럼 0~150 범위 |
| **[[075_referential_integrity_foreign_key_cascade|참조 무결성]]** | FK [[316_reference_pattern_nosql|참조]] 대상 존재 [[396_validation|확인]] | 없는 상품 코드 [[316_reference_pattern_nosql|참조]] 거부 |
| **[[064_relation_domain|도메인]] 코드** | 허용된 코드값만 입력 | 성별: M/F 이외 거부 |
| **비즈니스 룰** | 복합 [[395_verification_process_review|검증]] | 반품일 > 구매일 거부 |

📢 **섹션 요약 비유**: ETL의 Transform 단계는 공장 품질 관리 라인과 같다. 불량품([[005_schema|스키마]] 위반 [[001_dikw_pyramid|데이터]])은 라인에서 걸러내고, 합격품만 창고([[209_data_warehouse_schema_on_write|DW]])에 입고한다.

---

## Ⅲ. 비교 및 연결

### [[010_schema_on_write|Schema-on-Write]] vs [[009_schema_on_read|Schema-on-Read]] 완전 비교

| 비교 항목 | [[010_schema_on_write|Schema-on-Write]] | [[009_schema_on_read|Schema-on-Read]] |
|:---|:---|:---|
| **[[005_schema|스키마]] 적용 시점** | 저장 전 (강제 [[395_verification_process_review|검증]]) | 조회 시 (동적 적용) |
| **[[001_dikw_pyramid|데이터]] 품질** | 매우 높음 (Reject 메커니즘) | 낮음~중간 (원시 그대로) |
| **[[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]** | 우수 ([[154_database_index_b_tree_search_optimization|인덱스]], 통계 활용) | 보통 (Full Scan 빈번) |
| **[[005_schema|스키마]] 변경 비용** | 높음 ([[215_etl_vs_elt_pipeline|ETL]] 파이프라인 수정) | 낮음 (읽기 코드만 변경) |
| **신규 [[001_dikw_pyramid|데이터]] 수집 속도** | 느림 ([[215_etl_vs_elt_pipeline|ETL]] 설계 선행 필요) | 빠름 (즉시 저장) |
| **탐색적 분석 지원** | 제한적 | 우수 |
| **[[004_unstructured_data|비정형 데이터]] 처리** | 불가 | 가능 |
| **저장 비용** | 고비용 | 저비용 |
| **주요 플랫폼** | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]], Redshift | S3 [[208_data_lake_schema_on_read|Data Lake]], Azure DL |

### 하이브리드 [[268_strategy_pattern|전략]]: [[146_lakehouse|레이크하우스]]

```
[현대적 전략: 레이크하우스]
원시 데이터                        정제 데이터
(Schema-on-Read)    Delta Lake    (Schema-on-Write)
S3 Bronze Zone  ──▶  Silver Zone ──▶  Gold Zone
원시 JSON/CSV         ACID 보장         BI 분석용
스키마 추론            스키마 진화         스키마 확정
```

📢 **섹션 요약 비유**: Schema-on-Write와 Schema-on-Read는 "선불" vs "후불" 방식이다. 선불(Write)은 입장할 때 검사해 믿을 수 있지만 절차가 번거롭고, 후불(Read)은 자유롭게 들어오지만 나중에 [[395_verification_process_review|검증]] 비용이 든다. [[146_lakehouse|레이크하우스]]는 두 방식을 구역별로 나눠 쓴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[005_schema|스키마]] 변경 비용 관리

Schema-on-Write의 가장 큰 실무 도전은 **[[005_schema|스키마]] 변경**이다. 비즈니스 요건이 바뀌어 새 컬럼을 추가하거나 타입을 변경해야 할 때, 하위 [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 전체를 수정해야 한다.

```
스키마 변경 영향 범위
┌──────────────────────────────────────────────────┐
│ 스키마 변경 (예: orders 테이블에 신규 컬럼 추가)    │
│                                                  │
│ 영향받는 항목:                                    │
│  ① ETL 추출 SQL 수정                              │
│  ② Transform 매핑 로직 수정                       │
│  ③ DW 테이블 DDL ALTER                           │
│  ④ 파티셔닝 재설계 가능성                          │
│  ⑤ BI 도구 데이터 모델 수정                        │
│  ⑥ 하위 데이터 마트 ETL 수정                       │
│  ⑦ 테스트·배포 사이클 전체                         │
└──────────────────────────────────────────────────┘
```

### 실무 권장 패턴

| 상황 | [[268_strategy_pattern|전략]] |
|:---|:---|
| 고정된 BI [[018_kpi|KPI]], 정기 리포트 | [[010_schema_on_write|Schema-on-Write]] ([[209_data_warehouse_schema_on_write|DW]]) 적합 |
| 탐색적 분석, ML [[247_feature_label_variables|피처]] | [[009_schema_on_read|Schema-on-Read]] (레이크) 적합 |
| 두 요건 모두 | [[146_lakehouse|레이크하우스]] ([[194_medallion_architecture_bronze_silver_gold|Medallion Architecture]]) |
| [[005_schema|스키마]] 변경 잦음 | [[005_schema|스키마]] [[235_registry_immutable_tag|레지스트리]] + Avro/Protobuf 활용 |

**기술사 핵심 판단**: 시험에서는 Schema-on-Write를 "[[001_dikw_pyramid|데이터]] 품질 보장"의 긍정적 측면과 "[[005_schema|스키마]] 경직성·변경 비용"의 트레이드오프를 함께 서술하고, 현대적 [[146_lakehouse|레이크하우스]] [[268_strategy_pattern|전략]]으로의 진화 맥락을 연결한다.

📢 **섹션 요약 비유**: Schema-on-Write의 [[005_schema|스키마]] 변경은 건물 설계를 바꾸는 것과 같다. 처음 지을 때 튼튼하게 설계했지만(품질 우수), 나중에 방 하나 추가하려면 전체 구조를 다시 검토해야 한다(변경 비용 고비용).

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **[[001_dikw_pyramid|데이터]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]** | 저장된 [[001_dikw_pyramid|데이터]]는 모두 [[395_verification_process_review|검증]] 통과, 즉시 분석 신뢰 가능 |
| **[[298_qkv_attention|쿼리]] 최적화** | 사전 정의된 [[154_database_index_b_tree_search_optimization|인덱스]]·통계·파티션으로 예측 가능한 [[282_performance_tactics|성능]] |
| **규정 준수** | [[791_gdpr_eu|GDPR]], 금융 [[001_dikw_pyramid|데이터]] 정합성 요건 자동 충족 |
| **BI 단순화** | 분석가가 [[266_data_cleansing|데이터 정제]] 없이 바로 집계 [[298_qkv_attention|쿼리]] 작성 가능 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **[[001_dikw_pyramid|데이터]] 민첩성 부족** | 새 [[001_dikw_pyramid|데이터]] 소스 추가 시 [[215_etl_vs_elt_pipeline|ETL]] 설계 선행 필요 |
| **[[005_schema|스키마]] 드리프트** | 소스 시스템 변경 시 [[215_etl_vs_elt_pipeline|ETL]] 파이프라인 장애 발생 |
| **[[004_unstructured_data|비정형 데이터]] 불가** | [[343_json|JSON]] 중첩, 비정형 텍스트 저장 불리 |
| **[[215_etl_vs_elt_pipeline|ETL]] 병목** | 변환 서버 [[282_performance_tactics|성능]]이 전체 수집 속도 제한 (ELT로 해소) |

📢 **섹션 요약 비유**: Schema-on-Write는 엄격한 학교 제복 규정과 같다. 등교(저장) 전 복장([[005_schema|스키마]]) 검사를 통과해야 입장 가능하므로 교내([[209_data_warehouse_schema_on_write|DW]])는 늘 단정하지만, 복장 규정 변경([[005_schema|스키마]] 변경) 시 전교생에게 공지하고 새 교복을 맞춰야 하는 비용이 든다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[009_schema_on_read|Schema-on-Read]] | 대립 개념, [[208_data_lake_schema_on_read|데이터 레이크]]의 핵심 철학 |
| [[215_etl_vs_elt_pipeline|ETL]] | [[010_schema_on_write|Schema-on-Write]] 구현의 핵심 메커니즘 |
| [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] | Schema-on-Write의 주요 적용 플랫폼 |
| [[034_elt|ELT]] | ETL의 현대적 대안, 변환 단계를 [[209_data_warehouse_schema_on_write|DW]] 내부로 이동 |
| [[146_lakehouse|레이크하우스]] | Schema-on-Write와 Schema-on-Read를 Zone별 결합 |
| [[005_schema|스키마]] [[235_registry_immutable_tag|레지스트리]] | [[005_schema|스키마]] [[288_version_ihl_tos_total_length|버전]] 관리로 드리프트 방지 |
| [[001_dikw_pyramid|데이터]] 품질 ([[270_data_quality_great_expectations|Data Quality]]) | Schema-on-Write가 보장하는 핵심 가치 |

### 👶 어린이를 위한 3줄 비유 설명
1. Schema-on-Write는 학교 급식실에서 음식을 담을 때, 반찬 종류와 양을 미리 정해서 담는 것처럼, [[001_dikw_pyramid|데이터]]를 저장하기 전에 정해진 형식에 맞게 정리한다.

### 📈 관련 키워드 및 발전 흐름도

```text
Schema-on-Write: ETL → 스키마 검증 → DW 적재
    ├─► 장점: 쿼리 성능 우수 · 데이터 품질 보장
    └─► 단점: 스키마 변경 비용 높음
    │
    ▼
Schema-on-Read: 저장 후 읽을 때 스키마 적용 (Lake)
```
2. 마치 도서관에서 책을 받을 때 제목·저자·ISBN이 모두 맞아야 등록해주는 것처럼, 정해진 규칙을 통과한 [[001_dikw_pyramid|데이터]]만 저장될 수 있다.
3. 이렇게 저장된 [[001_dikw_pyramid|데이터]]는 누구나 믿고 사용할 수 있지만, 새로운 종류의 책([[001_dikw_pyramid|데이터]])이 들어오려면 도서관 [[104_classification_analysis|분류]] 체계([[005_schema|스키마]])를 바꿔야 하는 번거로움이 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 221 / 371

← **이전**: [[221_data_warehouse_olap_sql|221. 데이터 웨어하우스 (Data Warehouse / DW)]]
**다음**: [[223_data_mart_department_analytics|223. 데이터 마트 (Data Mart)]] →

---
