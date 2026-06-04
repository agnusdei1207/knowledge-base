---
title: "165. 피처 스토어 (Feature Store) - 훈련/서빙 피처 일관성"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 (Feature Store)는 ML [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 중앙에서 정의·저장·서빙하는 플랫폼으로, 훈련(Offline)과 서빙(Online) 간의 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계산 불일치인 Training-Serving Skew 문제를 근본적으로 해결한다.
> 2. **가치**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 재사용으로 중복 엔지니어링을 제거하고, Point-in-Time Correct 조인으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage)를 방지하여 모델 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 높이고 개발 속도를 가속한다.
> 3. **판단 포인트**: 오프라인 스토어(배치 학습용)와 온라인 스토어(실시간 추론용)의 이중 구조가 핵심이며, 두 저장소 간 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 유지가 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 설계의 최대 난제다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어란?

<strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 스토어 (Feature Store)</strong>는 ML 모델 개발 및 서빙에 사용되는 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)(특징 변수)를 중앙화하여 정의, 저장, 공유, 서빙하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼이다.

```
피처 스토어 없는 세상 (문제 상황)
+-------------------------------------------------------+
|  팀 A: "나이" 계산 = (오늘 날짜 - 생년월일) / 365      |
|  팀 B: "나이" 계산 = (오늘 날짜 - 생년월일) / 365.25   |
|  팀 C: "나이" 계산 = 가장 최근 설문 응답의 나이 입력    |
|                                                       |
|  -> 같은 "나이" 피처가 팀마다 다르게 계산됨!            |
|  -> 훈련 시 A 방식, 서빙 시 B 방식 -> 성능 저하!        |
+-------------------------------------------------------+

피처 스토어 도입 후
+-------------------------------------------------------+
|  피처 레지스트리:                                      |
|  feature_name: "customer_age"                         |
|  definition: (current_date - birth_date) / 365        |
|  owner: data-platform-team                            |
|  version: v2                                          |
|                                                       |
|  -> 모든 팀이 동일한 "customer_age" 사용!              |
|  -> 훈련과 서빙 모두 동일 계산 로직 보장               |
+-------------------------------------------------------+
```

### 1.2 Training-Serving Skew 문제

<strong>Training-Serving Skew</strong>는 모델 훈련 시 계산된 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)와 실제 서빙 시 계산된 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)가 다른 현상으로, 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하의 주요 원인 중 하나다.

| Skew 원인 | 구체적 사례 |
|:---|:---|
| **코드 불일치** | Python으로 훈련, Java로 서빙 (반올림 오차, 로직 차이) |
| **타임스탬프 오류** | 훈련 시 현재 날짜 기준, 서빙 시 다른 기준 |
| **결측값 처리 차이** | 훈련: 평균 대체, 서빙: 0 대체 |
| <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> 불일치</strong> | 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평균으로 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 서빙 시 다른 평균 사용 |

📢 **섹션 요약 비유**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 요리 레시피 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스와 같다. 모든 요리사(팀)가 같은 레시피([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의)로 재료를 준비하고, 훈련(연습)과 실전(서빙) 모두 동일한 레시피를 사용한다. 레시피가 달라지면 요리 맛(모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))도 달라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 핵심 구성요소

```
+-----------------------------------------------------------------+
|                      피처 스토어 아키텍처                        |
+---------------------------------------------------------------  +
|                                                                 |
|  데이터 소스                피처 변환           저장소           |
|  +----------+  배치         +------------+    +------------+   |
|  | Data     |  파이프라인   |            |    | 오프라인   |   |
|  | Warehouse| ------------->|  피처      |---->| 스토어     |   |
|  | (S3,     |              |  변환      |    | (S3/GCS/  |   |
|  |  BQ)     |              |  (PySpark, |    |  Hive)    |   |
|  +----------+              |  dbt,      |    +-----+------+   |
|  +----------+  스트리밍    |  Flink)    |          | 배치 읽기|   |
|  | Kafka    |  파이프라인  |            |    +-----v------+   |
|  | (실시간) | ------------->|            |---->| 온라인     |   |
|  +----------+              +------------+    | 스토어     |   |
|                                              | (Redis,   |   |
|  피처 레지스트리                              |  DynamoDB)|   |
|  +--------------------------------------+   +-----+------+   |
|  | 피처 이름, 정의, 버전, 오너, 태그    |         | 실시간   |   |
|  | 문서화, 재사용 검색                  |         | 읽기     |   |
|  +--------------------------------------+         |          |
|                                              +-----v------+   |
|  학습 서버 <----- 오프라인 스토어 읽기        | 추론 서버  |   |
|  (배치 학습)                                 | (실시간)   |   |
|                                              +------------+   |
+-----------------------------------------------------------------+
```

### 2.2 오프라인 스토어 vs 온라인 스토어

| 항목 | 오프라인 스토어 | 온라인 스토어 |
|:---|:---|:---|
| **목적** | 배치 모델 학습 | 실시간 모델 추론 |
| **저장 기술** | S3, GCS, [BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/), [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/) |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 방식</strong> | 시간 범위 기반 배치 읽기 | 키-값 기반 단건 빠른 읽기 |
| <strong><a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>시간</strong> | 수 분 ~ 수 시간 | 수 밀리초 (ms) |
| **저장 기간** | 수년 (히스토리 보관) | 수일 ~ 수주 (최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 크기</strong> | TB ~ PB 규모 | GB ~ TB 규모 |

### 2.3 Point-in-Time Correct 조인

가장 중요한 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 개념 중 하나인 <strong>Point-in-Time Correct 조인</strong>은 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 각 레이블 시점에서 실제로 사용 가능했던 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 값만 사용하도록 보장한다.

```
데이터 누수 (Data Leakage) 문제 예시:

날짜:       2024-01-01  2024-01-10  2024-01-15
이벤트:     신용카드     결제 실패    사기 레이블
            발급                     확정

잘못된 조인 (미래 데이터 사용):
  레이블(2024-01-15) <- 피처(2024-01-15 기준 계산)
  -> 사기 레이블 시점의 정보를 학습에 사용
  -> 훈련 정확도는 높지만 실제 배포 시 성능 급락!

Point-in-Time Correct 조인:
  레이블(2024-01-15) <- 피처(2024-01-01 기준 계산)
  -> 신용카드 발급 시점의 정보만 사용
  -> 현실적이고 신뢰할 수 있는 모델 훈련
```

```
Point-in-Time Correct 조인 구현 (Feast 예시):
+----------------------------------------------------------+
|  entity_df = pd.DataFrame({                              |
|      "customer_id": [1001, 1002, 1003],                  |
|      "event_timestamp": [                                |
|          "2024-01-01",  # 이 시점의 피처값을 조인        |
|          "2024-01-05",                                   |
|          "2024-01-10"                                    |
|      ]                                                   |
|  })                                                      |
|                                                          |
|  # Feast가 각 event_timestamp 이전의                     |
|  # 최신 피처 값만 자동으로 조인!                         |
|  training_df = store.get_historical_features(            |
|      entity_df=entity_df,                                |
|      features=["customer_stats:avg_spend",               |
|                "customer_stats:login_count"]             |
|  ).to_df()                                               |
+----------------------------------------------------------+
```

### 2.4 주요 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 제품 비교

| 제품 | 유형 | 오프라인 | 온라인 | 강점 |
|:---|:---|:---:|:---:|:---|
| **Feast** | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | S3/GCS/BQ | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/)/[DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | 가장 많이 쓰이는 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |
| **Tecton** | [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) | Spark/[Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/) | [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/)/[Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) | 완전 관리형, 스트리밍 강점 |
| **Hopsworks** | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)/[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) | [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) | RonDB/MySQL | 사용 편의성, 오프라인 강점 |
| <strong>Vertex <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> Feature Store</strong> | GCP | [BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) | Bigtable | GCP 완전 통합 |
| **SageMaker Feature Store** | AWS | S3 | [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | AWS SageMaker 완전 통합 |

📢 **섹션 요약 비유**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 아키텍처는 도서관 시스템과 같다. 오프라인 스토어는 넓은 도서관 창고(빠르게 찾기 어렵지만 모든 책 보관)이고, 온라인 스토어는 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 앞 빠른 참고 선반(즉시 꺼낼 수 있는 핵심 책들)이다. Point-in-Time 조인은 "2023년 당시 도서관에 있던 책들만 참고"하는 시간 여행 규칙이다.

---

## Ⅲ. 비교 및 연결

### 3.1 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 vs [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) vs [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)

| 항목 | [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 |
|:---|:---|:---|:---|
| **목적** | 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 분석용 구조화 | ML [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 서빙 |
| **사용자** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가 | ML 엔지니어 |
| <strong><a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>시간</strong> | 분~시간 | 초~분 | ms (온라인) |
| <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리</strong> | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/테이블 | 없음/제한적 | 완전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| **실시간 서빙** | 불가 | 불가 | 핵심 기능 |

### 3.2 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 공유 재사용 효과

```
피처 스토어 도입 전:
  모델 A -> 자체 피처 파이프라인 구축 (2주 소요)
  모델 B -> 자체 피처 파이프라인 구축 (3주 소요)
  모델 C -> 자체 피처 파이프라인 구축 (2주 소요)
  총: 7주 + 중복 코드 + 버그 위험

피처 스토어 도입 후:
  피처 "customer_age", "avg_spend", "login_freq" 등록 (1주)
  모델 A, B, C 모두 피처 스토어에서 가져다 사용 (1~2일)
  총: 1.5주 + 코드 재사용 + 일관성 보장
```

### 3.3 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어의 한계와 보완

| 한계 | 설명 | 보완 방법 |
|:---|:---|:---|
| <strong>오프라인-온라인 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong> | 배치 업데이트 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로 최신성 부족 | 스트리밍 파이프라인 추가 |
| <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 구축 비용</strong> | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 파이프라인 표준화에 시간 소요 | 점진적 마이그레이션 |
| **거버넌스** | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 오너십, 접근 제어 관리 | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) + 권한 관리 |
| **스토리지 비용** | 온오프라인 이중 저장 | 콜드/웜/핫 계층화 저장 |

📢 **섹션 요약 비유**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 vs [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 차이는 도서관 창고([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/))와 빠른 배달 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Feature Store)의 차이다. 창고에서 책을 꺼내는 건 느려도(분석용), 배달 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 주문 즉시 수 밀리초 내 배달해야 한다(실시간 추론).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 도입 성숙도 모델

```
Level 1: 피처 파일 공유
  -> Google Drive나 S3에 CSV 파일 공유
  -> 버전 관리 없음, 검색 불가

Level 2: 중앙화된 피처 테이블
  -> BigQuery/Redshift에 피처 테이블 생성
  -> 재사용 가능, 실시간 서빙 불가

Level 3: 오프라인 피처 스토어
  -> Feast/Hopsworks 도입
  -> 버전 관리, PIT 조인, 배치 서빙

Level 4: 온라인 + 오프라인 통합
  -> Redis 기반 온라인 스토어 추가
  -> 실시간 추론 ms 응답

Level 5: 스트리밍 피처 스토어
  -> Flink/Kafka Streams로 실시간 피처 계산
  -> 진정한 실시간 피처 업데이트
```

### 4.2 기술사 시험 핵심 포인트

<strong>Q. <a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 스토어의 Training-Serving Skew 문제를 해결하는 방법을 설명하시오.</strong>

Training-Serving Skew는 훈련 시 Python PySpark로 계산한 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)와 서빙 시 Java 코드로 계산한 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 간 불일치에서 발생한다. [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 이를 다음 방법으로 해결한다:
1. <strong>단일 <a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 변환 코드</strong>: 오프라인과 온라인 모두 동일한 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의 코드 실행
2. **사전 계산 저장**: 변환 결과를 스토어에 저장하여 서빙 시 재계산 없이 조회
3. <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> <a href="/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">레지스트리</a></strong>: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 중앙 관리

<strong>Q. Point-in-Time Correct 조인으로 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 누수를 방지하는 원리를 설명하시오.</strong>

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수는 미래 시점의 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정보를 학습에 사용하여 실제 배포 시보다 높은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보이는 문제다. Point-in-Time Correct 조인은 각 훈련 샘플의 레이블 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점(event_timestamp)을 기준으로 <strong>그 시점 이전에 실제 계산·저장된 <a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 값만</strong> 조인한다. Feast 등 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 이를 SQL의 `AS OF` 문법이나 내부 타임스탬프 기반 역방향 조회로 구현한다.

### 4.3 Feast 아키텍처 상세

```
+--------------------------------------------------------------+
|                    Feast 아키텍처                             |
+--------------------------------------------------------------+
|                                                              |
|  ① 피처 정의 (Python SDK)                                    |
|  driver_stats = FeatureView(                                 |
|      name="driver_hourly_stats",                             |
|      entities=["driver_id"],                                 |
|      ttl=timedelta(hours=2),  # 온라인 스토어 TTL            |
|      schema=[Field(name="conv_rate", dtype=Float32)]         |
|  )                                                           |
|                                                              |
|  ② 오프라인 저장 (배치 머터리얼라이제이션)                   |
|  feast materialize 2024-01-01 2024-01-31                     |
|  -> S3/BigQuery에 피처 저장                                   |
|                                                              |
|  ③ 온라인 서빙 (실시간)                                      |
|  store.get_online_features(                                  |
|      features=["driver_hourly_stats:conv_rate"],             |
|      entity_rows=[{"driver_id": 1001}]                       |
|  )                                                           |
|  -> Redis에서 ms 내 반환                                      |
+--------------------------------------------------------------+
```

📢 **섹션 요약 비유**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 도입은 식당 주방에 재료 관리 시스템을 도입하는 것과 같다. 냉장고(오프라인 스토어)에는 모든 재료를 날짜별로 보관하고, 조리 직전 준비대(온라인 스토어)에는 오늘 가장 신선한 재료만 꺼내놓는다. 모든 요리사가 같은 재료 목록([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))을 보고 동일한 재료를 사용한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 개발 시간</strong> | 신규 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 2~4주 | 기존 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 재사용 1~2일 | 80% 단축 |
| **Training-Serving Skew** | 빈번히 발생 | 완전 제거 | 모델 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 향상 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 누수</strong> | 감지 어려움 | PIT 조인으로 방지 | 모델 정확도 현실화 |
| <strong>팀 간 <a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 공유</strong> | 없음 | 검색·재사용 가능 | 협업 효율 향상 |
| <strong>실시간 서빙 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong> | 수 초 (실시간 계산) | 수 ms (사전 계산) | [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 충족 |

### 5.2 결론

[피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 대규모 ML [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>·재사용·실시간 서빙</strong>이라는 세 가지 요구를 동시에 해결하는 핵심 인프라다. Point-in-Time Correct 조인으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수를 방지하고, 오프라인/온라인 이중 구조로 배치 학습과 실시간 추론을 모두 지원한다.

📢 **섹션 요약 비유**: [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 글로벌 체인 패스트푸드의 중앙 레시피 관리 시스템과 같다. 서울 매장이든 뉴욕 매장이든(훈련이든 서빙이든) 동일한 버거 레시피([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의)를 사용하고, 신선한 재료(최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 냉장 트럭(스트리밍 파이프라인)으로 실시간 공급된다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 해결 문제 | Training-Serving Skew | 훈련/서빙 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 불일치 |
| 해결 문제 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage) | 미래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 학습 사용 |
| 핵심 기능 | Point-in-Time Correct 조인 | 시점 기준 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 조인 |
| 구성요소 | 오프라인 스토어 | 배치 학습용 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 저장 |
| 구성요소 | 온라인 스토어 | 실시간 추론용 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 저장 |
| 구성요소 | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의·[메타데이터 관리](/studynote/16_bigdata/10_governance/203_metadata_management/) |
| 도구 | Feast | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 |
| 도구 | Hopsworks | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 |
| 도구 | Tecton | [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 |
| 상위 개념 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 핵심 인프라 |
| 연관 | [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) | 모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 ([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어 협력) |

---

### 👶 어린이를 위한 3줄 비유 설명

1. [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어는 레고 부품함과 같아요. 여러 사람이 같은 부품([피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/))을 사용하고, 새 모델을 만들 때마다 부품을 새로 만들 필요 없이 부품함에서 가져다 쓸 수 있어요.
2. 온라인 스토어는 냉장고, 오프라인 스토어는 창고와 같아요. 즉시 필요한 재료는 냉장고([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/))에서, 긴 역사 기록은 창고(S3)에서 찾아요.
3. Point-in-Time 조인은 역사 시험 문제와 같아요. "1910년에 일어난 일"을 물을 때 1910년 이후 일어난 사건은 답이 될 수 없어요. 딱 그 시점까지의 정보만 써야 해요.

### 📈 관련 키워드 및 발전 흐름도

```text
피처 중복 계산 · Training-Serving Skew 문제
    |
    v
피처 스토어 도입
    +-► 피처 레지스트리: 정의 · 버전 · 오너 중앙 관리
    +-► 오프라인 스토어 (S3/BQ): 배치 학습용
    +-► 온라인 스토어 (Redis): 실시간 서빙용 (ms 응답)
    |
    v
Point-in-Time Correct 조인 -> 데이터 누수 방지
    |
    v
스트리밍 피처 계산 (Flink/Kafka) -> 실시간 피처 업데이트
    |
    v
피처 플랫폼: Feast · Tecton · Hopsworks · SageMaker FS
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 165 / 258

<- **이전**: [164. 컨셉 드리프트 (Concept Drift) - 정답 맵핑 규칙 변화](/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)
**다음**: [166. 모델 레지스트리 (Model Registry) - 버전 관리 MLflow](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) ->

---
