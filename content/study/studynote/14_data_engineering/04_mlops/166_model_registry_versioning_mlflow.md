+++
weight = 166
title = "166. 모델 레지스트리 (Model Registry) - 버전 관리 MLflow"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모델 [[235_registry_immutable_tag|레지스트리]] (Model [[235_registry_immutable_tag|Registry]])는 ML 모델의 전체 생명주기(실험 → 스테이징 → 프로덕션 → 아카이브)를 중앙에서 관리하는 시스템으로, 모델 [[288_version_ihl_tos_total_length|버전]]·[[012_metadata|메타데이터]]·[[075_artifact_management_nexus_docker_registry|아티팩트]]를 단일 저장소에 통합한다.
> 2. **가치**: 모델 계보(Lineage) 추적으로 "어떤 [[001_dikw_pyramid|데이터]]로, 어떤 코드로, 어떤 파라미터로" 학습된 모델인지를 완전 재현 가능하게 보존하여 규제 [[606_auditing_linux_auditd|감사]]와 버그 디버깅을 지원한다.
> 3. **판단 포인트**: [[180_mlflow|MLflow]] Model Registry는 실험 추적(Tracking)과 [[235_registry_immutable_tag|레지스트리]]를 통합한 [[191_oss_license_compliance|오픈소스]] 표준이지만, 대규모 조직에서는 Vertex [[190_ai_llm_requirements_specification|AI]]/SageMaker Model [[235_registry_immutable_tag|Registry]] 같은 클라우드 관리형 솔루션과의 트레이드오프를 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 모델 [[235_registry_immutable_tag|레지스트리]]란?

**모델 [[235_registry_immutable_tag|레지스트리]] (Model [[235_registry_immutable_tag|Registry]])**는 ML 모델의 [[288_version_ihl_tos_total_length|버전]] 이력, [[012_metadata|메타데이터]], [[075_artifact_management_nexus_docker_registry|아티팩트]]를 중앙에서 관리하고 배포 상태를 추적하는 시스템이다.

```
모델 레지스트리 없는 세상
┌────────────────────────────────────────────────────┐
│  model_v1_final.pkl                                │
│  model_v1_final_FINAL.pkl                          │
│  model_v2_new.pkl                                  │
│  model_v2_production_0312.pkl                      │
│  model_best_DO_NOT_DELETE.pkl                      │
│  model_production_BACKUP.pkl                       │
│                                                    │
│  → "어떤 모델이 지금 프로덕션에 있는가?" 불명확!  │
│  → 재현 불가, 롤백 위험, 감사 불가               │
└────────────────────────────────────────────────────┘

모델 레지스트리 도입 후 (MLflow)
┌────────────────────────────────────────────────────┐
│  Model: fraud_detection                            │
│  ├── v1: Archived  (2024-01-15, F1=0.89)          │
│  ├── v2: Archived  (2024-02-01, F1=0.91)          │
│  ├── v3: Staging   (2024-03-01, F1=0.93)          │
│  └── v4: Production (2024-03-15, F1=0.94)         │
└────────────────────────────────────────────────────┘
```

### 1.2 모델 [[235_registry_immutable_tag|레지스트리]]가 필요한 이유

| 문제 | 설명 | [[235_registry_immutable_tag|레지스트리]]로 해결 |
|:---|:---|:---|
| **[[288_version_ihl_tos_total_length|버전]] 혼란** | 어떤 모델이 현재 서빙 중인지 불명확 | 상태(Staging/Production) 명시 |
| **재현 불가** | 특정 [[282_performance_tactics|성능]]의 모델을 다시 만들 수 없음 | 파라미터·[[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] 기록 |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]] 어려움** | 이전 모델로 빠른 [[658_ir_recovery|복구]] 불가 | [[288_version_ihl_tos_total_length|버전]]별 [[075_artifact_management_nexus_docker_registry|아티팩트]] 보존 |
| **규제 [[606_auditing_linux_auditd|감사]]** | [[190_ai_llm_requirements_specification|AI]] 결정 근거 설명 불가 | 완전한 계보(Lineage) 추적 |
| **팀 협업** | 다른 팀의 모델 현황 파악 불가 | 중앙화된 모델 [[394_catalog_metadata|카탈로그]] |

📢 **섹션 요약 비유**: 모델 [[235_registry_immutable_tag|레지스트리]]는 의약품 허가 관리 시스템과 같다. 어떤 원료([[001_dikw_pyramid|데이터]]), 어떤 제조 공정(학습 코드), 어떤 배합(파라미터)으로 만들어진 약(모델)인지를 모두 기록하고, 임상 단계(Staging) → 시판 허가(Production) → 판매 중단(Archived) 상태를 관리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[180_mlflow|MLflow]] 전체 아키텍처

```
┌────────────────────────────────────────────────────────────────┐
│                       MLflow 구성요소                           │
├────────────────┬───────────────────────────────────────────────┤
│  MLflow        │  실험 추적                                     │
│  Tracking      │  파라미터, 메트릭, 아티팩트 로깅               │
│                │  실험 비교 UI                                  │
├────────────────┼───────────────────────────────────────────────┤
│  MLflow        │  모델 패키징                                   │
│  Projects      │  conda.yaml, MLproject 파일                   │
│                │  재현 가능한 실행 환경                         │
├────────────────┼───────────────────────────────────────────────┤
│  MLflow        │  표준 모델 형식 (MLmodel)                     │
│  Models        │  다양한 프레임워크 지원                        │
│                │  (sklearn, TF, PyTorch, XGBoost, ...)         │
├────────────────┼───────────────────────────────────────────────┤
│  MLflow        │  모델 버전 관리                                │
│  Model         │  상태 전이 (None → Staging → Production)      │
│  Registry      │  설명, 태그, 승인 워크플로우                   │
└────────────────┴───────────────────────────────────────────────┘
```

### 2.2 모델 [[632_state_transition_diagram_testing|상태 전이]] (Model [[632_state_transition_diagram_testing|State Transition]])

```
실험 완료
    │
    ▼
┌───────────┐  등록  ┌───────────┐  승인  ┌────────────┐
│  None     │───────→│  Staging  │───────→│ Production │
│ (미등록)  │        │ (스테이징) │        │ (프로덕션) │
└───────────┘        └───────────┘        └────────────┘
                           │   실패            │   교체
                           ▼                  ▼
                      ┌──────────────────────────┐
                      │        Archived          │
                      │    (아카이브/더 이상 미사용)│
                      └──────────────────────────┘

각 상태의 역할:
  None:       실험 결과 등록, 아직 검토 전
  Staging:    QA/성능 검증 진행 중
  Production: 실제 서빙 중인 현행 모델
  Archived:   더 이상 사용하지 않는 구버전 (삭제 안 함)
```

### 2.3 [[180_mlflow|MLflow]] 실험 추적 상세

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# MLflow 실험 시작
with mlflow.start_run(run_name="fraud_detection_v3"):

    # 파라미터 로깅
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("training_data_version", "2024-03-01")

    # 모델 학습
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    # 메트릭 로깅
    mlflow.log_metric("accuracy", 0.94)
    mlflow.log_metric("f1_score", 0.93)
    mlflow.log_metric("auc_roc", 0.97)
    mlflow.log_metric("precision", 0.91)
    mlflow.log_metric("recall", 0.95)

    # 아티팩트 로깅 (혼동 행렬, 피처 중요도 등)
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("feature_importance.csv")

    # 모델 저장
    mlflow.sklearn.log_model(
        model,
        "fraud_model",
        registered_model_name="fraud_detection"  # 레지스트리에 등록
    )
```

### 2.4 모델 계보 (Model Lineage) 추적

```
┌──────────────────────────────────────────────────────────────┐
│                   모델 계보 (Lineage) 예시                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  데이터 버전                                                  │
│  └── data/fraud_labels_v3.parquet (2024-03-01)              │
│       (SHA256: abc123...)                                    │
│                                                              │
│  코드 버전                                                    │
│  └── git commit: a3f2b1c                                     │
│       (train.py, feature_engineering.py)                     │
│                                                              │
│  환경                                                        │
│  └── Python 3.10, scikit-learn 1.4.0                        │
│       conda environment: fraud_env_v2                        │
│                                                              │
│  학습 파라미터                                               │
│  └── n_estimators=100, max_depth=5, ...                     │
│                                                              │
│  → 모델: fraud_detection v4 (Production)                    │
│     F1=0.94, AUC=0.97                                       │
└──────────────────────────────────────────────────────────────┘
```

### 2.5 모델 [[012_metadata|메타데이터]] 항목

| 카테고리 | 항목 | 예시 |
|:---|:---|:---|
| **학습 파라미터** | 하이퍼파라미터 | n_estimators=100, lr=0.001 |
| **[[282_performance_tactics|성능]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]** | 평가 지표 | F1=0.94, AUC=0.97, Accuracy=0.95 |
| **[[075_artifact_management_nexus_docker_registry|아티팩트]]** | [[501_file_definition_logical_record|파일]] | 모델 [[501_file_definition_logical_record|파일]], [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]], [[247_feature_label_variables|피처]] 중요도 |
| **[[001_dikw_pyramid|데이터]] 추적** | 훈련 [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] | data-v3, SHA256, 레코드 수 |
| **코드 추적** | Git 커밋 | 커밋 해시, 브랜치, [[501_file_definition_logical_record|파일]] 목록 |
| **환경** | 실행 환경 | Python [[288_version_ihl_tos_total_length|버전]], 패키지 [[288_version_ihl_tos_total_length|버전]] |
| **태그** | 자유 형식 | team=fraud, owner=john, use-case=realtime |

📢 **섹션 요약 비유**: MLflow는 ML 모델의 주민등록 시스템과 같다. 모든 모델은 이름(모델명), 생년월일(학습 날짜), 출신 성분(학습 [[001_dikw_pyramid|데이터]]), 학력(코드 [[288_version_ihl_tos_total_length|버전]]), 성적표([[342_routing_metric_hop_bandwidth_delay|메트릭]])를 가지고, 현재 어떤 직책(Staging/Production)인지가 명확하게 기록된다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[180_mlflow|MLflow]] vs Weights & Biases vs DVC

| 항목 | [[180_mlflow|MLflow]] | Weights & Biases (W&B) | DVC |
|:---|:---|:---|:---|
| **유형** | [[191_oss_license_compliance|오픈소스]] | [[309_saas|SaaS]] (무료 플랜) | [[191_oss_license_compliance|오픈소스]] |
| **실험 추적** | 완전 지원 | 매우 강력 | 제한적 |
| **모델 [[235_registry_immutable_tag|레지스트리]]** | 완전 지원 | 지원 | 없음 |
| **[[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] 관리** | 제한적 | [[075_artifact_management_nexus_docker_registry|아티팩트]] | 핵심 기능 |
| **[[003_bigdata_7v|시각화]]** | 기본 | 매우 강력 | 없음 |
| **비용** | 무료 | 사용량 기반 | 무료 |
| **[[061_on_premise_legacy_infrastructure|온프레미스]]** | 완전 지원 | 제한적 | 완전 지원 |
| **적합 환경** | [[061_on_premise_legacy_infrastructure|온프레미스]]/하이브리드 | 빠른 실험, 팀 공유 | [[001_dikw_pyramid|데이터]] [[288_version_ihl_tos_total_length|버전]] 관리 중점 |

### 3.2 A/B 테스트 연동

```
모델 레지스트리 → A/B 테스트 연동 흐름:

MLflow Registry
  Production: fraud_detection v4  (현재 모델)
  Staging:    fraud_detection v5  (신규 후보)
         │
         ▼
  A/B 테스트 설정:
  트래픽 v4 = 90%, 트래픽 v5 = 10%
         │
         ▼
  평가 기간 (1주일)
  v5 F1 = 0.95 > v4 F1 = 0.94 ✓
  v5 지연시간 ≤ v4 지연시간 ✓
         │
         ▼
  레지스트리 업데이트:
  v4 → Archived
  v5 → Production
```

### 3.3 [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[268_strategy_pattern|전략]]

| 상황 | [[098_rollback_strategy_pipeline_error_threshold|롤백]] 방법 | 소요 시간 |
|:---|:---|:---|
| **[[282_performance_tactics|성능]] 급락** | 이전 Production [[288_version_ihl_tos_total_length|버전]] 재활성화 | 수분 |
| **심각한 버그** | Archived [[288_version_ihl_tos_total_length|버전]]으로 즉시 복원 | 수분 |
| **점진적 [[282_performance_tactics|성능]] 저하** | [[162_continuous_training_pipeline_model_retraining|CT]] 파이프라인 재실행 + 새 [[288_version_ihl_tos_total_length|버전]] | 수시간 |
| **[[001_dikw_pyramid|데이터]] 품질 문제** | [[001_dikw_pyramid|데이터]] 수정 후 재학습 | 수일 |

📢 **섹션 요약 비유**: MLflow와 W&B의 차이는 집 냉장고([[180_mlflow|MLflow]], 자체 관리)와 편의점 도시락 배달(W&B, [[090_service_kubernetes_network_load_balancing|서비스]] 이용)의 차이다. 집 냉장고는 직접 관리하지만 모든 것을 내 마음대로 할 수 있고, 배달 [[090_service_kubernetes_network_load_balancing|서비스]]는 편리하지만 비용이 들고 의존성이 생긴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 엔터프라이즈 모델 [[235_registry_immutable_tag|레지스트리]] 거버넌스

```
┌──────────────────────────────────────────────────────────────┐
│               모델 거버넌스 프레임워크                        │
├──────────────────────────────────────────────────────────────┤
│  역할 정의:                                                  │
│  - 데이터 과학자: 모델 등록, 실험 추적                       │
│  - ML 엔지니어: Staging 검토, Production 승인               │
│  - 도메인 전문가: 비즈니스 지표 검증                         │
│  - 보안/컴플라이언스: 규제 요건 점검                         │
├──────────────────────────────────────────────────────────────┤
│  승인 워크플로우:                                             │
│  None → Staging: 데이터 과학자 자동 등록                    │
│  Staging → Production: ML 엔지니어 + 도메인 전문가 승인 필요 │
│  Production → Archived: ML 엔지니어 승인 필요               │
├──────────────────────────────────────────────────────────────┤
│  감사 로그:                                                  │
│  - 상태 변경 이력 (누가, 언제, 왜)                          │
│  - 성능 메트릭 변화 추이                                     │
│  - 데이터/코드 버전 연결                                     │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 기술사 시험 핵심 포인트

**Q. 모델 계보(Model Lineage) 추적의 필요성과 구현 방법을 설명하시오.**

모델 계보 추적은 세 가지 이유에서 필수다:
1. **재현성**: 동일한 [[282_performance_tactics|성능]]의 모델을 다시 만들어야 할 때 ([[001_dikw_pyramid|데이터]], 코드, 환경, 파라미터 모두 필요)
2. **디버깅**: [[282_performance_tactics|성능]] 저하 원인 분석 시 "어떤 [[001_dikw_pyramid|데이터]] 변화가 원인인가?" 추적
3. **규제 대응**: [[791_gdpr_eu|GDPR]], EU [[190_ai_llm_requirements_specification|AI]] Act에서 [[190_ai_llm_requirements_specification|AI]] 결정 과정 설명 의무화

구현: MLflow의 `mlflow.log_param()`, `mlflow.log_artifact()`, `mlflow.set_tag("git_commit", git_sha)`로 [[001_dikw_pyramid|데이터]]/코드/파라미터를 연결하고, 모델 [[288_version_ihl_tos_total_length|버전]]마다 이 정보를 [[235_registry_immutable_tag|레지스트리]]에 기록한다.

**Q. [[180_mlflow|MLflow]] 모델 [[235_registry_immutable_tag|레지스트리]]의 [[632_state_transition_diagram_testing|상태 전이]]와 각 상태의 역할을 설명하시오.**

- **None(미등록)**: 실험 중, 검토 대상에서 제외
- **Staging**: QA 환경에서 [[400_integration_testing|통합 테스트]], [[282_performance_tactics|성능]] [[395_verification_process_review|검증]] 중
- **Production**: 실제 서빙 중인 유일한 현행 모델 (동일 모델 내 하나만 허용 권장)
- **Archived**: 더 이상 서빙하지 않지만 [[098_rollback_strategy_pipeline_error_threshold|롤백]]/[[606_auditing_linux_auditd|감사]]를 위해 보존

### 4.3 [[180_mlflow|MLflow]] 실무 배포 구조

```
개발 환경 (Local)                프로덕션 환경
┌────────────────────┐          ┌────────────────────────────┐
│  데이터 과학자     │          │  MLflow Tracking Server    │
│  실험 실행         │ ──Push── │  (PostgreSQL + S3)         │
│  mlflow.log_...()  │          │                            │
└────────────────────┘          │  Model Registry            │
                                │  fraud_detection           │
CI/CD 파이프라인                │  ├── v3: Staging           │
┌────────────────────┐          │  └── v4: Production        │
│  자동 학습 (CT)    │ ──등록── │                            │
│  평가 게이트       │          └─────────────┬──────────────┘
│  레지스트리 업데이트│                        │
└────────────────────┘                        │ 모델 Pull
                                              ▼
                                ┌────────────────────────────┐
                                │  서빙 서버                  │
                                │  (KServe / TF Serving)     │
                                └────────────────────────────┘
```

📢 **섹션 요약 비유**: 모델 [[235_registry_immutable_tag|레지스트리]] 거버넌스는 의사 면허 관리 시스템과 같다. 모든 의사(모델)는 의대 졸업(학습 완료) → 인턴/레지던트(Staging) → 전문의 자격(Production) 과정을 거치고, 각 단계마다 심사위원(승인자)의 검토를 받는다. 면허 취소(Archive)가 돼도 기록은 남는다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 모델 [[235_registry_immutable_tag|레지스트리]] 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 |
|:---|:---|:---|:---|
| **현재 프로덕션 모델 파악** | 불명확, [[501_file_definition_logical_record|파일]]명 추측 | [[235_registry_immutable_tag|레지스트리]] 즉시 [[396_validation|확인]] | 운영 명확성 향상 |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]] 시간** | 수시간 (찾기+배포) | 수분 ([[288_version_ihl_tos_total_length|버전]] 전환) | 90% 단축 |
| **재현성** | 불가 | 100% 재현 가능 | 규제 대응 가능 |
| **팀 간 모델 공유** | 이메일/슬랙 | [[235_registry_immutable_tag|레지스트리]] 검색 | 협업 효율 향상 |
| **[[606_auditing_linux_auditd|감사]] 대응** | 수일 소요 | 즉시 계보 제공 | [[606_auditing_linux_auditd|감사]] 비용 절감 |

### 5.2 결론

모델 [[235_registry_immutable_tag|레지스트리]]는 ML 모델의 **단일 진실 공급원(Single Source of Truth)**이다. MLflow는 실험 추적부터 [[235_registry_immutable_tag|레지스트리]]까지 통합된 [[191_oss_license_compliance|오픈소스]] 표준으로 가장 광범위하게 사용되며, 모델 계보 추적·상태 관리·A/B 테스트 연동을 통해 안전하고 [[606_auditing_linux_auditd|감사]] 가능한 ML 운영을 실현한다.

📢 **섹션 요약 비유**: 모델 [[235_registry_immutable_tag|레지스트리]]는 항공기 블랙박스와 같다. 어떤 조건(파라미터)으로 만들어진 모델이 어떤 [[282_performance_tactics|성능]]([[342_routing_metric_hop_bandwidth_delay|메트릭]])을 냈는지 완전히 기록되어, 사고([[282_performance_tactics|성능]] 저하)가 발생했을 때 원인을 추적하고 즉시 이전 안전한 상태(이전 [[288_version_ihl_tos_total_length|버전]])로 복원할 수 있다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 핵심 도구 | [[180_mlflow|MLflow]] | 실험 추적 + 모델 [[235_registry_immutable_tag|레지스트리]] 통합 [[191_oss_license_compliance|오픈소스]] |
| 경쟁 도구 | Weights & Biases (W&B) | [[309_saas|SaaS]] 기반 실험 추적 및 모델 관리 |
| 협력 개념 | [[165_feature_store_training_serving_consistency|피처 스토어]] | [[247_feature_label_variables|피처]] [[288_version_ihl_tos_total_length|버전]]과 모델 [[288_version_ihl_tos_total_length|버전]] 연계 |
| 협력 개념 | [[162_continuous_training_pipeline_model_retraining|CT]] ([[162_continuous_training_pipeline_model_retraining|Continuous Training]]) | [[162_continuous_training_pipeline_model_retraining|CT]] 결과를 [[235_registry_immutable_tag|레지스트리]]에 자동 등록 |
| 배포 연동 | A/B 테스트 | [[235_registry_immutable_tag|레지스트리]] [[288_version_ihl_tos_total_length|버전]] 기반 트래픽 분할 |
| 배포 연동 | [[595_canary_stack_smashing_protector|카나리]] 롤아웃 | [[235_registry_immutable_tag|레지스트리]] [[288_version_ihl_tos_total_length|버전]] 기반 점진적 배포 |
| 상위 개념 | [[348_mlops|MLOps]] | [[235_registry_immutable_tag|레지스트리]]는 [[348_mlops|MLOps]] 핵심 구성요소 |
| 규제 | 모델 계보 (Model Lineage) | 재현성·[[606_auditing_linux_auditd|감사]] 추적 보장 |
| 클라우드 | Vertex [[190_ai_llm_requirements_specification|AI]] Model [[235_registry_immutable_tag|Registry]] | GCP 관리형 모델 [[235_registry_immutable_tag|레지스트리]] |
| 클라우드 | SageMaker Model [[235_registry_immutable_tag|Registry]] | AWS 관리형 모델 [[235_registry_immutable_tag|레지스트리]] |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 모델 [[235_registry_immutable_tag|레지스트리]]는 학교 성적표 [[501_file_definition_logical_record|파일]]함과 같아요. 모든 시험(실험) 결과가 날짜별로 저장되고, 현재 최고 성적(Production)이 어떤 조건에서 나왔는지 언제든지 찾아볼 수 있어요.
2. 게임 세이브 [[501_file_definition_logical_record|파일]]처럼, 좋은 모델(세이브 포인트)을 저장해두면 나중에 모델이 망가져도(게임 오버) 저장된 시점으로 돌아갈([[098_rollback_strategy_pipeline_error_threshold|롤백]]) 수 있어요.
3. 약의 성분표처럼, 어떤 재료([[001_dikw_pyramid|데이터]])와 방법(파라미터)으로 만들었는지 MLflow에 모두 기록해서, 나중에 같은 약을 다시 만들거나 부작용 원인을 찾을 수 있어요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 모델 관리 (파일명에 날짜 포함)
    │
    ▼
실험 추적 (MLflow Tracking · W&B)
    ├─► 파라미터 · 메트릭 · 아티팩트 기록
    └─► 실험 비교 · 재현성 보장
    │
    ▼
모델 레지스트리 (MLflow Registry)
    ├─► 버전 관리: v1 → v2 → v3
    ├─► 상태 전이: Staging → Production → Archived
    └─► 메타데이터: 학습 데이터 · 코드 · 환경
    │
    ▼
CI/CD 파이프라인 연동 → 자동 배포 · 롤백
    │
    ▼
모델 거버넌스: 감사 추적 · 규제 준수 (GDPR · AI Act)
```
