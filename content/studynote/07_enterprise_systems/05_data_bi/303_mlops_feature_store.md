---
title: 303. MLOps 피처 스토어 데이터마트 연동 (MLOps Feature Store)
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Feature Store는 ML [[247_feature_label_variables|피처]]를 중앙에서 관리해 학습과 서빙 시의 [[247_feature_label_variables|피처]] 불일치([[588_mlops_pipeline_automation|Training]]-Serving Skew)를 근원적으로 차단한다.
> 2. **가치**: [[247_feature_label_variables|피처]] 재사용률이 60~80% 상승해 팀 간 중복 개발을 제거하고 모델 출시 시간을 2~5배 단축한다.
> 3. **판단 포인트**: Online Store의 읽기 [[015_지연_데이터_관점|지연]] <10ms 요건 충족 여부가 실시간 추천/사기 탐지 시스템의 핵심 SLA다.

## Ⅰ. 개요 및 필요성

ML 모델 개발에서 가장 많은 시간을 소비하는 단계는 [[247_feature_label_variables|피처]] 엔지니어링([[081_feature_engineering|Feature Engineering]])이다.
각 팀이 동일한 [[247_feature_label_variables|피처]]를 독립적으로 구현하면, 학습 시 사용한 [[247_feature_label_variables|피처]] 계산 로직과 서빙 시 계산 로직이 미묘하게 달라져 모델 [[282_performance_tactics|성능]]이 저하된다. 이를 [[588_mlops_pipeline_automation|Training]]-Serving Skew라 한다.

[[165_feature_store_training_serving_consistency|Feature Store]] ([[165_feature_store_training_serving_consistency|피처 스토어]])는 이 문제를 해결하기 위한 중앙화된 [[247_feature_label_variables|피처]] 저장소·관리 플랫폼이다.
[[247_feature_label_variables|피처]]를 한 번 정의하면 오프라인 학습과 온라인 서빙 양측에서 동일한 계산 결과를 보장한다.

주요 제품: Feast ([[191_oss_license_compliance|오픈소스]]), Tecton (상용 [[309_saas|SaaS]]), Hopsworks ([[191_oss_license_compliance|오픈소스]]+상용), AWS SageMaker [[165_feature_store_training_serving_consistency|Feature Store]]

📢 **섹션 요약 비유**: Feature Store는 공용 식자재 창고다. 각 요리사(팀)가 자기 냉장고에 따로 재료를 보관하면 유통기한이 달라지지만, 공용 창고를 쓰면 모두 같은 신선도의 재료로 요리한다.

## Ⅱ. 아키텍처 및 핵심 원리

### 온라인 스토어 vs 오프라인 스토어

| 항목 | 온라인 스토어 (Online Store) | 오프라인 스토어 (Offline Store) |
|:---|:---|:---|
| 저장소 | [[542_redis|Redis]], [[545_dynamodb|DynamoDB]], [[541_cassandra|Cassandra]] | [[544_hive|Hive]], S3 ([[178_parquet_rle_encoding_columnar_compression|Parquet]]), [[263_storage_compute_separation_bigquery|BigQuery]] |
| 읽기 [[015_지연_데이터_관점|지연]] | <10ms (p99) | 수초~수분 |
| 주 용도 | 실시간 모델 서빙 | 배치 학습 [[001_dikw_pyramid|데이터]] [[087_process_state_transition|생성]] |
| [[001_dikw_pyramid|데이터]] 형태 | 최신 [[247_feature_label_variables|피처]]값 (Point-in-Time) | 시계열 전체 이력 |
| 비용 | 높음 (인메모리) | 낮음 (스토리지) |

### [[103_ascii|ASCII]] 다이어그램: [[165_feature_store_training_serving_consistency|Feature Store]] 아키텍처

```
  원천 데이터
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ 이벤트 로그│  │  RDB 거래  │  │ 사용자 프로필│
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       └──────────────┼──────────────┘
                      ▼
            ┌─────────────────────┐
            │  Feature Pipeline   │ (Spark / Flink)
            └──────────┬──────────┘
               ┌───────┴────────┐
               ▼                ▼
  ┌─────────────────────┐  ┌─────────────────────┐
  │   Offline Store     │  │   Online Store      │
  │  (S3 / Hive)        │  │  (Redis Cluster)    │
  │  학습 데이터 생성용  │  │  서빙 시 <10ms 조회  │
  └────────┬────────────┘  └────────┬────────────┘
           │                        │
           ▼                        ▼
  ┌─────────────────┐    ┌───────────────────────┐
  │  ML Training    │    │  Real-time Serving    │
  │  (Batch)        │    │  (API, <100ms 응답)    │
  └─────────────────┘    └───────────────────────┘
```

### Feast vs Tecton vs Hopsworks

| 항목 | Feast | Tecton | Hopsworks |
|:---|:---|:---|:---|
| 유형 | [[191_oss_license_compliance|오픈소스]] | 상용 [[309_saas|SaaS]] | [[191_oss_license_compliance|오픈소스]]+상용 |
| 실시간 변환 | 미지원 | 지원 (Streaming) | 지원 |
| 온라인 스토어 | [[542_redis|Redis]], [[545_dynamodb|DynamoDB]] | 자체 | RonDB |
| [[229_monitor|모니터]]링 | 제한적 | 강력 | 강력 |

📢 **섹션 요약 비유**: 오프라인 스토어는 대형 창고, 온라인 스토어는 계산대 옆 빠른 진열대다. 손님(모델)이 주문하면 계산대 옆에서 즉시 집어준다.

## Ⅲ. 비교 및 연결

### [[588_mlops_pipeline_automation|Training]]-Serving Skew 방지 메커니즘

| 상황 | Skew 없이 | Skew 발생 시 |
|:---|:---|:---|
| 나이 [[247_feature_label_variables|피처]] 계산 | Feature Store에서 동일 [[294_function_calling_tool_use|함수 호출]] | 학습: pandas, 서빙: Java → 소숫점 오차 |
| 결측값 처리 | 스토어 레벨에서 통일 | 학습: 0 대체, 서빙: -1 대체 |
| 7일 윈도우 집계 | Point-in-Time Correct [[521_join|Join]] 보장 | 미래 [[001_dikw_pyramid|데이터]] 누수([[001_dikw_pyramid|Data]] Leakage) |

📢 **섹션 요약 비유**: [[588_mlops_pipeline_automation|Training]]-Serving Skew는 레시피가 두 [[288_version_ihl_tos_total_length|버전]]인데 맛이 다른 상황이다. Feature Store는 레시피를 하나로 통일해 주방 어디서든 같은 맛을 보장한다.

## Ⅳ. 실무 적용 및 기술사 판단

### [[165_feature_store_training_serving_consistency|Feature Store]] 도입 [[435_checklist_based_testing|체크리스트]]

- [ ] 현재 팀 간 동일 [[247_feature_label_variables|피처]]가 중복 구현되고 있는가? (2팀 이상이면 도입 정당화)
- [ ] Online Store 읽기 [[085_sla|SLA]] <10ms 충족 가능한 [[542_redis|Redis]] 클러스터 확보 여부
- [ ] Point-in-Time Correct [[521_join|Join]] 지원 여부 [[396_validation|확인]]
- [ ] [[247_feature_label_variables|피처]] [[317_versioning_data_model_design|버저닝]] [[164_policy|정책]] 수립 (메이저/마이너 [[288_version_ihl_tos_total_length|버전]] 관리)
- [ ] [[247_feature_label_variables|피처]] [[229_monitor|모니터]]링: 드리프트 감지 (PSI >0.2 알람)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| [[247_feature_label_variables|피처]]를 모델별로 개별 관리 | 동일 [[247_feature_label_variables|피처]] 수십 중복, Skew 발생 | [[165_feature_store_training_serving_consistency|Feature Store]] 중앙화 |
| Online Store에 모든 [[247_feature_label_variables|피처]] 저장 | [[542_redis|Redis]] 메모리 비용 폭증 | 서빙 필요 [[247_feature_label_variables|피처]]만 선택적 저장 |
| Point-in-Time 조인 미적용 | 미래 [[001_dikw_pyramid|데이터]] 누수 → 과평가 모델 | Feast/Tecton PiT [[521_join|Join]] 활용 |

📢 **섹션 요약 비유**: Point-in-Time Join은 시험 당일 기준 [[001_dikw_pyramid|데이터]]만 보는 것이다. 미래 정답을 미리 알고 풀면 성적이 좋아도 실제로는 틀린 것이다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | 도입 전 | 도입 후 |
|:---|:---|:---|
| [[247_feature_label_variables|피처]] 개발 시간 | 모델당 2~4주 | 1~3일 (기존 [[247_feature_label_variables|피처]] 재사용) |
| [[588_mlops_pipeline_automation|Training]]-Serving Skew | 빈번 (모델 [[282_performance_tactics|성능]] 저하 20~30%) | 거의 없음 |
| 온라인 추론 [[015_지연_데이터_관점|지연]] | 50~200ms | <10ms (사전 계산·[[456_caching|캐싱]]) |
| [[247_feature_label_variables|피처]] 재사용률 | [[489_raid_10_hybrid|10]]% 미만 | 60~80% |

### 한계 및 선결 과제

- [[165_feature_store_training_serving_consistency|Feature Store]] 인프라 자체가 운영 부담 → 플랫폼 팀 전담 필요
- [[347_cold_start_problem|Cold start]]: 히스토리 [[001_dikw_pyramid|데이터]] 없는 신규 사용자 [[247_feature_label_variables|피처]] 처리 별도 [[268_strategy_pattern|전략]] 필요
- Streaming [[247_feature_label_variables|피처]](실시간 집계)는 Flink/[[060_spark_streaming_dstream|Spark Streaming]] 연동 복잡도 높음

📢 **섹션 요약 비유**: Feature Store는 도서관 사서다. 각자 책([[247_feature_label_variables|피처]])을 집에만 두면 남들은 못 쓰지만, 사서가 관리하면 누구든 빌려 쓰고 항상 최신판을 보장받는다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[165_feature_store_training_serving_consistency|Feature Store]] | 중심 | [[247_feature_label_variables|피처]] 중앙 관리 플랫폼 |
| Online Store | 구성 요소 | 실시간 서빙용 인메모리 저장소 |
| Offline Store | 구성 요소 | 배치 학습용 대용량 저장소 |
| [[588_mlops_pipeline_automation|Training]]-Serving Skew | 해결 대상 | 학습/서빙 [[247_feature_label_variables|피처]] 불일치 문제 |
| Point-in-Time [[521_join|Join]] | 핵심 기능 | 과거 시점 기준 [[247_feature_label_variables|피처]] 조인 |

### 📈 관련 키워드 및 발전 흐름도

```
실험실 ML 모델 - 프로덕션 배포 단절 문제
    │
    ▼
수작업 피처 엔지니어링 반복 - 일관성 부재
    │
    ▼
Feature Store 등장 - 피처 재사용·공유 플랫폼
    │
    ▼
온라인(Redis)/오프라인(Hive) 이중 저장 구조
    │
    ▼
MLOps 통합 - 피처→모델→서빙 자동화 파이프라인
```

> **키워드**: [[165_feature_store_training_serving_consistency|Feature Store]], [[348_mlops|MLOps]], [[081_feature_engineering|Feature Engineering]], Online Store, Offline Store, Feast, [[588_mlops_pipeline_automation|Training]]-Serving Skew

### 👶 어린이를 위한 3줄 비유 설명

1. [[165_feature_store_training_serving_consistency|피처 스토어]]는 마트 진열대예요. 여러 요리사(모델)가 같은 재료([[247_feature_label_variables|피처]])를 진열대에서 가져다 쓰니 항상 같은 재료를 써요.
2. 온라인 스토어는 손님 바로 앞 빠른 진열대, 오프라인 스토어는 창고 깊숙이 있는 대량 저장고예요.
3. [[588_mlops_pipeline_automation|Training]]-Serving Skew 방지는 시험 준비할 때와 실제 시험에서 똑같은 교재를 쓰는 것이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 303 / 482

← **이전**: [[302_dataops_cicd_dbt|302. 데이터옵스 CI/CD 파이프라인 자동 테스팅 (DataOps CI/CD dbt)]]
**다음**: [[304_realtime_cdp_architecture|304. 실시간 CDP 아키텍처 1st Party 클릭 로그 수집 통합 (Real-time CDP Architecture)]] →

---
