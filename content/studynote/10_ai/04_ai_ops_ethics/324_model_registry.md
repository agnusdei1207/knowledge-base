+++
title = "324. 모델 레지스트리 (Model Registry)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) ([Model Registry](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/))는 ML 모델의 학습 파라미터·[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)·배포 상태를 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)별로 중앙 관리하는 저장소로, 소프트웨어의 패키지 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)(PyPI, npm)와 유사하게 ML 모델의 생명주기를 추적하고 거버넌스를 제공한다.
> 2. **가치**: "어떤 모델이 현재 프로덕션에서 동작 중인가", "이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)하려면 어떤 모델을 가져오면 되는가", "이 모델은 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 학습됐는가"라는 운영 핵심 질문에 즉각 답변이 가능하게 하여 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 거버넌스와 운영 안정성을 보장한다.
> 3. **판단 포인트**: [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)의 상태 관리(Staging → Production → Archived)와 승인 워크플로우(Champion/Challenger 비교)가 ML 시스템의 [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) ([IT Service Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_itsm/)) 변경 [관리 프로세스](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/018_admin_processes/)와 직접 연계되는 점이 기술사 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

ML 팀이 매주 새 모델을 학습한다. 6개월 후 프로덕션에 문제가 생겼을 때: "현재 어떤 모델이 배포됐지?", "2개월 전 모델로 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)하려면?", "이 모델은 어떤 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 하이퍼파라미터를 썼지?" — 이 질문들에 답하지 못한다면 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 운영의 심각한 거버넌스 부재다.

소프트웨어에 Git이 있듯, ML 모델에는 **[모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)**가 필요하다. 모든 학습 실험의 파라미터, [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 모델 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)별로 기록하고, 각 모델의 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(실험 중/[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 완료/프로덕션/아카이브)를 명확히 관리한다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)는 ML 세계의 Git이다. 코드를 커밋·태그·브랜치로 관리하듯, ML 모델을 실험 번호·[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 태그·배포 상태로 관리한다. 문제 발생 시 `git revert`처럼 모델을 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 즉시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│         모델 레지스트리 (Model Registry) 생명주기 관리 구조            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  실험 추적 → 모델 등록 → 상태 전환 → 배포 → 아카이브                  │
│                                                                  │
│  ① 실험 추적 (Experiment Tracking):                               │
│  각 학습 실험 로그:                                                 │
│  - run_id: exp-2024-0315-v3                                     │
│  - 하이퍼파라미터: {lr: 0.001, batch: 64, epochs: 50}             │
│  - 메트릭: {accuracy: 0.947, f1: 0.932, AUC: 0.981}             │
│  - 데이터셋: train_data_v5, test_data_v2                          │
│  - 아티팩트: model.pkl, requirements.txt, feature_schema.json   │
│                                                                  │
│  ② 모델 상태 전환 (Stage Transitions):                             │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  None → Staging → Production → Archived               │     │
│  │  (신규)  (검증중)   (프로덕션)    (아카이브)              │     │
│  │                                                        │     │
│  │  Champion/Challenger 전략:                              │     │
│  │  Production(Champion) 모델과 Staging(Challenger) 비교   │     │
│  │  → Challenger 성능이 더 높으면 Promotion                │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ③ 모델 패키지 (Model Package):                                   │
│  모델 코드 + 의존성(requirements.txt) + 특징 스키마 + 추론 로직     │
│  → Docker 이미지로 패키징 → 어느 환경에서도 재현 가능                │
└──────────────────────────────────────────────────────────────────┘
```

| 상태 | 의미 | 전환 조건 |
|:---|:---|:---|
| None | 실험 완료, 미등록 | 자동 또는 수동 등록 |
| Staging | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·테스트 중 | 실험 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기준 충족 |
| Production | 현재 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중 | Champion/Challenger [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 통과 |
| Archived | 더 이상 사용 안 함 | 새 모델로 교체 후 보관 |

- **📢 섹션 요약 비유**: Champion/Challenger [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 챔피언십 무술 대회와 같다. 현 챔피언(Production 모델)에게 도전자(Staging 모델)가 도전한다. 도전자가 A/B 테스트에서 더 좋은 성과를 내면 왕좌를 빼앗는다(Promotion). 기존 챔피언은 무술 연구원으로 전환(Archived). 언제든 복귀 가능([롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/))하도록 기록을 보존한다.

---

## Ⅲ. 비교 및 연결

**[MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) [Model Registry](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) vs SageMaker [Model Registry](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) vs Vertex [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)**:
| 플랫폼 | 특징 | 적합 환경 |
|:---|:---|:---|
| [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 로컬/클라우드 | 자체 구축, 유연성 필요 |
| AWS SageMaker | 완전 관리형, AWS 통합 | AWS 기반 ML 팀 |
| GCP Vertex [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 통합 ML 플랫폼 | GCP 기반, [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) 연동 |
| Azure ML [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | Azure 통합 | Azure DevOps와 연계 |

- **📢 섹션 요약 비유**: MLflow는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 자작 도서관(자유롭지만 직접 관리), SageMaker는 AWS가 운영하는 종합 도서관(편하지만 AWS 종속), Vertex AI는 Google의 클라우드 도서관이다. 규모·예산·클라우드 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에 맞게 선택해야 하며, 특정 클라우드에 종속되지 않으려면 MLflow가 최선이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) 거버넌스 설계**:
1. **승인 워크플로우**: Staging → Production 전환 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자 + ML 엔지니어 + 비즈니스 스테이크홀더 3자 승인
2. **[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 임계값 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)**: 정확도 < 95% 또는 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 > 200ms면 자동 Production 승격 차단
3. **[롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)**: 프로덕션 이슈 발생 시 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 5분 내 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 보장
4. **규제 준수 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)**: 모든 프로덕션 모델의 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출처·[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)·평가 결과를 규제 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)(Financial, Medical) 대응용으로 보존

- **📢 섹션 요약 비유**: [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) 3자 승인은 의약품 시판 허가와 같다. 신약(새 모델)이 효과 입증([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) + 안전성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(ML 엔지니어 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) + 비용 대비 효과(비즈니스 승인)를 모두 통과해야 환자(사용자)에게 처방된다. 어느 하나라도 누락하면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 사고(의료 과실)로 이어진다.

---

## Ⅴ. 기대효과 및 결론

[모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)는 ML 운영의 통제 센터다. 어떤 모델이 어디서 동작하고, 어떤 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 더 좋고, 문제 시 어떻게 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)하는지에 대한 명확한 답을 제공한다. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 규제(EU [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act, 금융 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 규제)에서 모델 투명성·추적 가능성·거버넌스를 요구하는 세상에서, [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 조직의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 증명하는 필수 인프라다. [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/), SageMaker, Vertex [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 등 플랫폼 선택보다 "어떤 거버넌스 프로세스를 설계하는가"가 더 중요한 기술사 판단 포인트다.

- **📢 섹션 요약 비유**: [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 세계의 의약품 처방 DB다. 어떤 의사가 어떤 환자에게 어떤 약(모델)을 어떤 날짜에 처방했는지 완벽히 추적된다. 부작용([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이상)이 발생하면 즉시 이전 약(이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))으로 교체하고, 동일 부작용이 다시 발생하지 않도록 이력을 분석한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 실험 추적 (Experiment Tracking) | [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/), W&B, 하이퍼파라미터 / [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)에 등록 전 실험 기록 |
| Champion/Challenger | A/B 테스트, 모델 비교 / 프로덕션 모델 교체 의사결정 방법 |
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) ([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/)) | 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 즉각 복원 / [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) 핵심 운영 기능 |
| [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD, 자동화 / [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)가 통합되는 운영 체계 |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 거버넌스 | 투명성, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 / [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)가 지원하는 규제 준수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] → [모델 레지스트리 (Model Registry)] → [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. **[모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)**는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 **"역대 기록 보관소"**예요 — 어떤 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 언제 만들어졌고, 얼마나 정확했고, 지금 어디서 사용 중인지 다 기록해요!
2. 새 AI가 더 좋으면 **챔피언 교체(Production 승격)**, 문제가 생기면 **이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 즉시 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)([롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/))** 할 수 있어요.
3. 의료·금융 규제에서 "이 AI는 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 만들었나요?"라고 물으면, [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)가 **완벽한 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 기록**을 제공해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 324 / 420

← **이전**: [323. 피처 스토어 (Feature Store)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/323_feature_store/)
**다음**: [325. 설명 가능한 AI (XAI, eXplainable AI)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/325_xai/) →

---
