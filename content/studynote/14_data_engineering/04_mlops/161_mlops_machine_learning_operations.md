---
title: 161. MLOps (Machine Learning Operations) - AI 모델 개발~서빙 CI/CD 자동화
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]])는 ML 모델의 개발(Dev)과 운영(Ops)을 통합하여, 실험실 모델을 신뢰할 수 있는 프로덕션 [[090_service_kubernetes_network_load_balancing|서비스]]로 자동화하는 전체 생명주기 관리 체계다.
> 2. **가치**: [[090_configuration_item|CI]]/CD에 [[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]])을 더해 [[001_dikw_pyramid|데이터]]·코드·모델 3축을 동시에 [[288_version_ihl_tos_total_length|버전]] 관리하고, [[468_model_drift_retraining|모델 드리프트]]에 자동으로 반응함으로써 운영 비용을 절감하고 [[090_service_kubernetes_network_load_balancing|서비스]] 품질을 지속 보장한다.
> 3. **판단 포인트**: [[348_mlops|MLOps]] 성숙도(Level 0→2)가 높을수록 자동화 범위가 넓어지고 재현성(Reproducibility)·[[606_auditing_linux_auditd|감사]] 추적([[065_audit_trail_worm_storage_compliance|Audit Trail]])이 강화되나, [[459_quic_fec_forward_error_correction|초기]] 인프라 투자와 조직 문화 변화가 선행되어야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 MLOps란?

**[[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]])**는 기계학습 시스템의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있는 배포와 유지 관리를 위해 ML, [[652_devops_calms_culture|DevOps]], [[001_dikw_pyramid|데이터]] 엔지니어링의 교집합에서 탄생한 실천 방법론이다.

기존 소프트웨어는 코드만 [[288_version_ihl_tos_total_length|버전]] 관리하면 되었지만, ML 시스템은 **코드 + [[001_dikw_pyramid|데이터]] + 모델** 3요소가 모두 변하기 때문에 기존 [[652_devops_calms_culture|DevOps]] 관행만으로는 운영이 어렵다.

```
전통 소프트웨어           ML 시스템
┌─────────────────┐     ┌──────────────────────────────┐
│   Code (코드)   │     │  Code  │  Data  │  Model     │
│   버전 관리     │     │  코드  │  데이터│  모델       │
│   테스트/배포   │     │  변화  │  변화  │  드리프트   │
└─────────────────┘     └──────────────────────────────┘
        ↓                           ↓
  CI/CD 충분           CI / CD / CT (3축 자동화) 필요
```

### 1.2 [[348_mlops|MLOps]] 등장 배경

| 문제 | 설명 |
|:---|:---|
| **재현성 부재** | 같은 코드라도 [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]]이 다르면 다른 모델이 나옴 |
| **배포 병목** | [[001_dikw_pyramid|데이터]] 사이언티스트가 만든 모델을 엔지니어가 다시 구현하는 "번역 비용" |
| **모델 부패** | [[001_dikw_pyramid|데이터]] 분포 변화로 시간이 지날수록 예측 [[282_performance_tactics|성능]] 저하 (Model Decay) |
| **실험 관리 부재** | 수천 번의 실험 결과를 수동으로 관리하는 비효율 |
| **규제·[[606_auditing_linux_auditd|감사]]** | [[791_gdpr_eu|GDPR]], [[190_ai_llm_requirements_specification|AI]] Act 등에서 모델 의사결정 설명 및 추적 요구 |

### 1.3 [[652_devops_calms_culture|DevOps]] vs [[348_mlops|MLOps]] 비교

| 항목 | [[652_devops_calms_culture|DevOps]] | [[348_mlops|MLOps]] |
|:---|:---|:---|
| **관리 대상** | 코드 | 코드 + [[001_dikw_pyramid|데이터]] + 모델 |
| **테스트 기준** | 유닛/[[400_integration_testing|통합 테스트]] | [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] + 모델 품질 테스트 |
| **배포 [[507_acid_properties|트리거]]** | 코드 변경 | 코드 변경 + [[001_dikw_pyramid|데이터]] 변경 + [[282_performance_tactics|성능]] 저하 |
| **모니터링** | 시스템 [[342_routing_metric_hop_bandwidth_delay|메트릭]] (CPU, 메모리) | 모델 [[342_routing_metric_hop_bandwidth_delay|메트릭]] (정확도, 드리프트) |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]] 단위** | 코드 [[288_version_ihl_tos_total_length|버전]] | 모델 [[288_version_ihl_tos_total_length|버전]] + [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] |
| **자동화 추가** | [[090_configuration_item|CI]]/CD | [[090_configuration_item|CI]]/CD + [[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]]) |

📢 **섹션 요약 비유**: MLOps는 자동차 공장의 품질관리 시스템과 같다. 소프트웨어 개발이 자동차 설계 도면(코드) 하나만 관리하면 됐다면, ML은 도면(코드) + 원자재 규격([[001_dikw_pyramid|데이터]]) + 완성차 품질(모델) 세 가지를 동시에 품질 보증해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[348_mlops|MLOps]] 3대 자동화 축

| 자동화 | 설명 | [[507_acid_properties|트리거]] |
|:---|:---|:---|
| **[[090_configuration_item|CI]] ([[019_continuous_integration|Continuous Integration]])** | 코드 변경 시 자동 빌드·테스트·[[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] | Git push |
| **CD ([[164_continuous_delivery|Continuous Delivery]])** | [[395_verification_process_review|검증]]된 모델을 자동으로 스테이징/프로덕션 배포 | 모델 품질 통과 |
| **[[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]])** | 새 [[001_dikw_pyramid|데이터]] 유입 또는 [[282_performance_tactics|성능]] 저하 시 자동 재학습 | [[001_dikw_pyramid|데이터]]/[[282_performance_tactics|성능]] [[507_acid_properties|트리거]] |

### 2.2 [[348_mlops|MLOps]] 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                        MLOps 생명주기                            │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│  데이터  │  피처    │  모델    │  모델    │  서빙    │  모니터  │
│  수집    │  엔지니  │  학습    │  평가    │  배포    │  링      │
│  검증    │  어링    │  실험    │  검증    │  &API    │  알람    │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────┤
│                     자동화 레이어                                 │
│   CI (코드/데이터 검증) │ CD (모델 배포) │ CT (자동 재학습)      │
├─────────────────────────────────────────────────────────────────┤
│                     인프라 레이어                                 │
│   피처 스토어 │ 모델 레지스트리 │ 실험 추적 │ 오케스트레이션     │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 [[348_mlops|MLOps]] 성숙도 3단계 (Google [[348_mlops|MLOps]] 성숙도 모델)

```
Level 0 (수동)              Level 1 (자동 파이프라인)    Level 2 (CI/CD 파이프라인)
┌────────────────────┐     ┌────────────────────────┐  ┌──────────────────────────┐
│ 데이터 사이언티스트│     │  자동화된 ML 파이프라인 │  │  CI/CD + CT 완전 자동화  │
│ 가 수동으로        │     │  데이터 → 학습 → 배포  │  │  코드 변경만으로         │
│ 데이터 처리        │ →   │  자동화                 │→ │  전체 파이프라인 실행    │
│ → 모델 학습        │     │  CT 자동 재학습         │  │  다중 팀 협업 가능       │
│ → 수동 배포        │     │  실험 추적              │  │  모델 레지스트리 연동    │
└────────────────────┘     └────────────────────────┘  └──────────────────────────┘
  특징: Jupyter Notebook     특징: Kubeflow, MLflow       특징: 완전 자동화
  한계: 재현 불가, 느림       한계: 파이프라인만 자동화    수준: 대규모 ML 서비스
```

#### 성숙도별 상세 비교

| 항목 | Level 0 | Level 1 | Level 2 |
|:---|:---|:---|:---|
| **학습 방식** | 수동 스크립트 | 자동 파이프라인 | [[090_configuration_item|CI]]/CD [[507_acid_properties|트리거]] |
| **배포 방식** | 수동 배포 | 자동 배포 | 자동 배포 + [[395_verification_process_review|검증]] |
| **재학습** | 없음/수동 | [[162_continuous_training_pipeline_model_retraining|CT]] 자동화 | [[162_continuous_training_pipeline_model_retraining|CT]] + [[507_acid_properties|트리거]] 기반 |
| **실험 추적** | 없음 | [[180_mlflow|MLflow]]/W&B | 완전 자동화 |
| **[[166_model_registry_versioning_mlflow|모델 레지스트리]]** | 없음 | 있음 | 완전 연동 |
| **적합 조직** | 스타트업 [[459_quic_fec_forward_error_correction|초기]] | 성장기 기업 | 대규모 ML 조직 |

### 2.4 핵심 구성요소 상세

```
┌─────────────────────────────────────────────────────────────────┐
│                    MLOps 핵심 구성요소                           │
├────────────────┬────────────────────────────────────────────────┤
│ 데이터 파이프  │  데이터 수집 → 검증(Great Expectations)        │
│ 라인           │  → 전처리 → 피처 스토어 저장                   │
├────────────────┼────────────────────────────────────────────────┤
│ 모델 학습      │  실험 추적(MLflow) → 하이퍼파라미터 튜닝        │
│ 파이프라인     │  → 분산 학습(Horovod) → 모델 평가              │
├────────────────┼────────────────────────────────────────────────┤
│ 모델 레지스트  │  버전 관리 → Staging → Production              │
│ 리             │  → Archived 상태 전이                          │
├────────────────┼────────────────────────────────────────────────┤
│ 모델 서빙      │  REST/gRPC API → 동적 배치 → A/B 테스트        │
│ 플랫폼         │  → 카나리 배포 → 롤백                          │
├────────────────┼────────────────────────────────────────────────┤
│ 모니터링       │  데이터 드리프트 → 모델 성능 → 인프라 메트릭   │
│ & 알람         │  → 자동 재학습 트리거                          │
└────────────────┴────────────────────────────────────────────────┘
```

### 2.5 주요 [[348_mlops|MLOps]] 도구 생태계

| 카테고리 | [[191_oss_license_compliance|오픈소스]] | 클라우드 관리형 |
|:---|:---|:---|
| **파이프라인 [[073_container_orchestration_tools|오케스트레이션]]** | [[167_kubeflow_kubernetes_ml_pipeline|Kubeflow]], Airflow | Vertex [[190_ai_llm_requirements_specification|AI]] Pipelines, SageMaker Pipelines |
| **실험 추적** | [[180_mlflow|MLflow]], Weights & Biases | SageMaker Experiments |
| **[[165_feature_store_training_serving_consistency|피처 스토어]]** | Feast, Hopsworks | Vertex [[190_ai_llm_requirements_specification|AI]] [[165_feature_store_training_serving_consistency|Feature Store]], SageMaker [[165_feature_store_training_serving_consistency|Feature Store]] |
| **[[166_model_registry_versioning_mlflow|모델 레지스트리]]** | [[180_mlflow|MLflow]] [[235_registry_immutable_tag|Registry]] | Vertex [[190_ai_llm_requirements_specification|AI]] [[166_model_registry_versioning_mlflow|Model Registry]], SageMaker [[166_model_registry_versioning_mlflow|Model Registry]] |
| **모델 서빙** | Triton, TF Serving, KServe | SageMaker Endpoints, Vertex [[190_ai_llm_requirements_specification|AI]] Endpoints |
| **모니터링** | Evidently [[190_ai_llm_requirements_specification|AI]], WhyLogs | SageMaker Model [[229_monitor|Monitor]] |

📢 **섹션 요약 비유**: [[348_mlops|MLOps]] 아키텍처는 자동화된 자동차 조립 라인과 같다. Level 0은 장인이 손으로 한 대씩 만드는 방식이고, Level 1은 컨베이어 벨트로 부품을 이어주는 방식이며, Level 2는 센서가 품질 이상을 감지하면 라인 자체가 레시피를 바꾸는 완전 자동화 공장이다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[348_mlops|MLOps]] vs [[324_dataops|DataOps]] vs [[099_aiops_chatbot_itsm_automation|AIOps]]

| 항목 | [[348_mlops|MLOps]] | [[324_dataops|DataOps]] | [[099_aiops_chatbot_itsm_automation|AIOps]] |
|:---|:---|:---|:---|
| **정의** | ML 모델 생명주기 자동화 | [[645_data_pipeline_acceleration|데이터 파이프라인]] 자동화 | IT 운영의 [[190_ai_llm_requirements_specification|AI]] 적용 |
| **목적** | 모델 품질·속도 향상 | [[001_dikw_pyramid|데이터]] 품질·속도 향상 | IT 장애 예측·자동 해결 |
| **핵심** | [[468_model_drift_retraining|모델 드리프트]] 관리 | [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] 관리 | [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]·자동화 |
| **[[083_relationship_in_er_model|관계]]** | [[324_dataops|DataOps]] 위에서 동작 | MLOps의 기반 | [[348_mlops|MLOps]] 결과물 활용 |

### 3.2 [[348_mlops|MLOps]] 핵심 개념 간 [[083_relationship_in_er_model|관계]]

```
데이터 드리프트 감지
        │
        ▼
  CT 트리거 발동
        │
        ▼
피처 스토어에서 최신 피처 조회
        │
        ▼
  모델 재학습 실행
        │
        ▼
모델 레지스트리에 새 버전 등록
        │
        ▼
카나리 배포 → A/B 테스트 → 전체 배포
        │
        ▼
  모니터링 → 이상 시 롤백
```

### 3.3 ML 프로젝트 실패 원인 Top 5

| 원인 | 발생 비율 | MLOps로 해결 |
|:---|:---:|:---|
| **[[001_dikw_pyramid|데이터]] 품질 문제** | 40% | [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] 자동화 |
| **모델 [[282_performance_tactics|성능]] 저하** | 25% | [[162_continuous_training_pipeline_model_retraining|CT]] + 드리프트 모니터링 |
| **배포 복잡성** | 15% | [[090_configuration_item|CI]]/CD 파이프라인 |
| **재현성 부재** | 12% | 실험 추적, [[166_model_registry_versioning_mlflow|모델 레지스트리]] |
| **팀 협업 부재** | 8% | 표준화된 워크플로우 |

📢 **섹션 요약 비유**: [[348_mlops|MLOps]], [[324_dataops|DataOps]], AIOps의 [[083_relationship_in_er_model|관계]]는 건설 현장의 기반([[324_dataops|DataOps]]) 위에 건물([[348_mlops|MLOps]])을 짓고, 건물 관리 [[190_ai_llm_requirements_specification|AI]]([[099_aiops_chatbot_itsm_automation|AIOps]])가 모든 설비를 자동 점검·수리하는 구조와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [[348_mlops|MLOps]] 도입 단계별 로드맵

| 단계 | 기간 | 주요 작업 |
|:---|:---|:---|
| **기반 구축** | 1~3개월 | 실험 추적 도구 도입, [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] 관리 |
| **파이프라인 자동화** | 3~6개월 | [[162_continuous_training_pipeline_model_retraining|CT]] 파이프라인 구축, [[166_model_registry_versioning_mlflow|모델 레지스트리]] 도입 |
| **서빙 자동화** | 6~12개월 | A/B 테스트, [[115_canary_deployment_gradual_rollout|카나리 배포]], 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] |
| **완전 자동화** | 12개월+ | 드리프트 감지 → [[162_continuous_training_pipeline_model_retraining|CT]] → 배포 전 과정 자동화 |

### 4.2 기술사 시험 핵심 포인트

**Q. MLOps에서 [[090_configuration_item|CI]]/CD/CT의 역할을 설명하시오.**

- **[[090_configuration_item|CI]] ([[019_continuous_integration|Continuous Integration]])**: 코드 변경 및 [[001_dikw_pyramid|데이터]] 변경 시 자동 빌드, [[001_dikw_pyramid|데이터]] [[005_schema|스키마]] [[395_verification_process_review|검증]], [[397_unit_test|단위 테스트]] 실행
- **CD ([[164_continuous_delivery|Continuous Delivery]]/[[087_deployment_kubernetes_workload_rolling_update|Deployment]])**: [[395_verification_process_review|검증]]된 모델을 스테이징 환경 자동 배포, 프로덕션 승인 후 자동 적용
- **[[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]])**: 새 학습 [[001_dikw_pyramid|데이터]] 도착, [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] 감지, 모델 [[282_performance_tactics|성능]] 임계값 하락 시 자동 재학습 파이프라인 실행

**Q. MLOps와 DevOps의 차이점을 설명하시오.**

핵심 차이는 **관리 대상의 복잡성**에 있다. DevOps는 결정론적(Deterministic) 소프트웨어를 다루지만, MLOps는 확률론적(Probabilistic) 모델과 진화하는 [[001_dikw_pyramid|데이터]]를 다룬다. 따라서 코드 변경 없이도 [[001_dikw_pyramid|데이터]] 변화만으로 배포가 실패할 수 있고, [[468_model_drift_retraining|모델 드리프트]]라는 새로운 운영 개념이 추가된다.

### 4.3 실무 아키텍처 예시 (전자상거래 [[211_recommendation_system|추천 시스템]])

```
사용자 행동 데이터 (실시간)
        │
        ▼
Kafka → Spark Streaming → 피처 스토어 (Feast)
                                │
                                ├─→ 오프라인 스토어 (S3/BigQuery)
                                │         → 주기적 모델 재학습
                                │
                                └─→ 온라인 스토어 (Redis)
                                          → 실시간 추천 API

모델 재학습 파이프라인 (Kubeflow)
  데이터 검증 → 피처 추출 → 학습 → 평가 → 모델 레지스트리 등록
                                              → 카나리 배포 (5%)
                                              → A/B 테스트 (CTR 비교)
                                              → 전체 배포 또는 롤백
```

📢 **섹션 요약 비유**: [[348_mlops|MLOps]] 도입은 수작업 요리사에서 HACCP [[303_authentication_authorization_patterns|인증]] 식품공장으로 전환하는 것과 같다. 맛(모델 [[282_performance_tactics|성능]])을 유지하면서 위생([[001_dikw_pyramid|데이터]] 품질), 레시피 이력 관리(실험 추적), 자동 이상 감지(드리프트 모니터링)까지 모두 갖춰야 진정한 대량 생산(스케일아웃)이 가능하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [[348_mlops|MLOps]] 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **모델 배포 시간** | 수주 | 수시간 | 90% 단축 |
| **실험 재현성** | 불가 | 완전 재현 | [[606_auditing_linux_auditd|감사]] 추적 가능 |
| **[[468_model_drift_retraining|모델 드리프트]] 감지** | 수동/늦음 | 자동/즉시 | [[090_service_kubernetes_network_load_balancing|서비스]] 품질 유지 |
| **팀 협업** | [[002_silo_hyeonhyung|사일로]] | 표준화 | 전달 비용 제거 |
| **규정 준수** | 어려움 | 자동 기록 | [[791_gdpr_eu|GDPR]]·[[190_ai_llm_requirements_specification|AI]] Act 대응 |

### 5.2 [[348_mlops|MLOps]] 성공 요인

1. **조직 문화**: [[001_dikw_pyramid|데이터]] 사이언티스트와 [[348_mlops|MLOps]] 엔지니어 간 협업 문화
2. **[[052_data_governance_framework|데이터 거버넌스]]**: [[001_dikw_pyramid|데이터]] 품질·보안·접근 제어 체계
3. **표준화**: 재사용 가능한 파이프라인 컴포넌트와 [[247_feature_label_variables|피처]] 정의
4. **점진적 도입**: Level 0 → Level 1 → Level 2 단계적 전환

### 5.3 결론

MLOps는 ML 프로젝트가 PoC (Proof of [[120_concept|Concept]])에 머무르지 않고 실제 비즈니스 가치를 창출하는 프로덕션 [[090_service_kubernetes_network_load_balancing|서비스]]가 되기 위한 핵심 인프라다. [[090_configuration_item|CI]]/CD/[[162_continuous_training_pipeline_model_retraining|CT]] 3축 자동화와 [[165_feature_store_training_serving_consistency|피처 스토어]], [[166_model_registry_versioning_mlflow|모델 레지스트리]], 드리프트 모니터링의 유기적 통합이 고품질 ML [[090_service_kubernetes_network_load_balancing|서비스]]의 지속 운영을 가능케 한다.

📢 **섹션 요약 비유**: [[348_mlops|MLOps]] 없는 ML은 운전 실력은 있지만 정비소가 없는 자동차와 같다. 처음엔 잘 달리지만 시간이 지나면 고장([[468_model_drift_retraining|모델 드리프트]])이 나고, 언제 어떻게 고장났는지도 모른 채 [[090_service_kubernetes_network_load_balancing|서비스]]가 멈춘다. MLOps는 자동 정비소([[162_continuous_training_pipeline_model_retraining|CT]]), 부품 이력 관리([[235_registry_immutable_tag|레지스트리]]), 주행 기록계(모니터링)를 모두 갖춘 종합 자동차 관리 시스템이다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 구성요소 | [[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]]) | [[001_dikw_pyramid|데이터]] 변화 시 자동 재학습 |
| 구성요소 | [[165_feature_store_training_serving_consistency|피처 스토어]] ([[165_feature_store_training_serving_consistency|Feature Store]]) | 훈련/서빙 [[247_feature_label_variables|피처]] [[194_consistency_database_integrity|일관성]] 보장 |
| 구성요소 | [[166_model_registry_versioning_mlflow|모델 레지스트리]] ([[166_model_registry_versioning_mlflow|Model Registry]]) | 모델 [[288_version_ihl_tos_total_length|버전]]·라이프사이클 관리 |
| 문제 해결 | [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] ([[163_data_drift_statistical_distribution_shift|Data Drift]]) | 입력 분포 변화 감지 |
| 문제 해결 | [[164_concept_drift_target_mapping_change|컨셉 드리프트]] ([[164_concept_drift_target_mapping_change|Concept Drift]]) | 입출력 [[083_relationship_in_er_model|관계]] 변화 감지 |
| 도구 | [[167_kubeflow_kubernetes_ml_pipeline|Kubeflow]] | [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 기반 ML 파이프라인 |
| 도구 | [[180_mlflow|MLflow]] | 실험 추적 + [[166_model_registry_versioning_mlflow|모델 레지스트리]] |
| 도구 | [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] | [[401_bayesian_network_dag_causality|DAG]] 기반 워크플로우 [[073_container_orchestration_tools|오케스트레이션]] |
| 배포 [[268_strategy_pattern|전략]] | A/B 테스트 | 트래픽 분할 모델 [[282_performance_tactics|성능]] 비교 |
| 배포 [[268_strategy_pattern|전략]] | [[595_canary_stack_smashing_protector|카나리]] 롤아웃 ([[170_ab_test_canary_rollout_shadow_mirroring|Canary Rollout]]) | 점진적 트래픽 증가 |
| 상위 개념 | [[652_devops_calms_culture|DevOps]] | 코드 [[090_configuration_item|CI]]/CD 자동화의 원형 |
| 연관 개념 | [[324_dataops|DataOps]] | [[645_data_pipeline_acceleration|데이터 파이프라인]] 자동화 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. MLOps는 학교 급식 공장과 같아요. 맛있는 레시피(모델)를 만들고, 재료([[001_dikw_pyramid|데이터]])가 바뀌면 레시피를 자동으로 업데이트하고, 급식이 맛없어지기 전에 알아서 고쳐요.
2. 로봇 청소기처럼 처음에 사람이 길을 가르쳐주면(학습), 이후엔 혼자 청소하다가(서빙), 새 가구가 생기면([[163_data_drift_statistical_distribution_shift|데이터 드리프트]]) 다시 지도를 배워요([[162_continuous_training_pipeline_model_retraining|CT]]).
3. 자동화된 과자 공장처럼, 과자(모델) 레시피를 만들고, 맛 검사(모니터링)를 통과하면 포장해서 판매하고(배포), 맛이 변하면 자동으로 레시피를 수정해요([[162_continuous_training_pipeline_model_retraining|CT]]).

### 📈 관련 키워드 및 발전 흐름도

```text
DevOps (코드 CI/CD)
    │
    ▼
MLOps Level 0 — 수동 ML 파이프라인
    │
    ▼
MLOps Level 1 — ML 파이프라인 자동화 (CT 도입)
    ├─► 피처 스토어 (훈련/서빙 일관성)
    ├─► 모델 레지스트리 (버전 관리)
    └─► 드리프트 모니터링 (데이터/컨셉)
    │
    ▼
MLOps Level 2 — CI/CD/CT 완전 자동화
    ├─► A/B 테스트 · 카나리 배포 · 자동 롤백
    └─► 실험 추적 (MLflow · W&B)
    │
    ▼
LLMOps — 프롬프트 관리 · RAG 파이프라인 · PEFT 스케줄링
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 161 / 258

← **이전**: [[160_knowledge_graph_graphrag_integration|160. 지식 그래프 (Knowledge Graph) + GraphRAG 연동망]]
**다음**: [[162_continuous_training_pipeline_model_retraining|162. CT (Continuous Training) 파이프라인 - 모델 성능 저하 시 자동 재학습]] →

---
