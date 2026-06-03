---
title: 324. 모델 레지스트리 (Model Registry)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[166_model_registry_versioning_mlflow|모델 레지스트리]] ([[166_model_registry_versioning_mlflow|Model Registry]])는 ML 모델의 학습 파라미터·[[282_performance_tactics|성능]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[075_artifact_management_nexus_docker_registry|아티팩트]]·배포 상태를 [[288_version_ihl_tos_total_length|버전]]별로 중앙 관리하는 저장소로, 소프트웨어의 패키지 [[235_registry_immutable_tag|레지스트리]](PyPI, npm)와 유사하게 ML 모델의 생명주기를 추적하고 거버넌스를 제공한다.
> 2. **가치**: "어떤 모델이 현재 프로덕션에서 동작 중인가", "이전 [[288_version_ihl_tos_total_length|버전]]으로 [[098_rollback_strategy_pipeline_error_threshold|롤백]]하려면 어떤 모델을 가져오면 되는가", "이 모델은 어떤 [[001_dikw_pyramid|데이터]]로 학습됐는가"라는 운영 핵심 질문에 즉각 답변이 가능하게 하여 [[190_ai_llm_requirements_specification|AI]] 거버넌스와 운영 안정성을 보장한다.
> 3. **판단 포인트**: [[166_model_registry_versioning_mlflow|모델 레지스트리]]의 상태 관리(Staging → Production → Archived)와 승인 워크플로우(Champion/Challenger 비교)가 ML 시스템의 [[096_iso_iec_20000_itsm_certification|ITSM]] ([[061_itsm|IT Service Management]]) 변경 [[018_admin_processes|관리 프로세스]]와 직접 연계되는 점이 기술사 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

ML 팀이 매주 새 모델을 학습한다. 6개월 후 프로덕션에 문제가 생겼을 때: "현재 어떤 모델이 배포됐지?", "2개월 전 모델로 [[098_rollback_strategy_pipeline_error_threshold|롤백]]하려면?", "이 모델은 어떤 훈련 [[001_dikw_pyramid|데이터]]와 하이퍼파라미터를 썼지?" — 이 질문들에 답하지 못한다면 [[190_ai_llm_requirements_specification|AI]] 운영의 심각한 거버넌스 부재다.

소프트웨어에 Git이 있듯, ML 모델에는 **[[166_model_registry_versioning_mlflow|모델 레지스트리]]**가 필요하다. 모든 학습 실험의 파라미터, [[342_routing_metric_hop_bandwidth_delay|메트릭]], 모델 [[501_file_definition_logical_record|파일]]을 [[288_version_ihl_tos_total_length|버전]]별로 기록하고, 각 모델의 [[178_as_is_to_be_analysis|현재 상태]](실험 중/[[395_verification_process_review|검증]] 완료/프로덕션/아카이브)를 명확히 관리한다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[166_model_registry_versioning_mlflow|모델 레지스트리]]는 ML 세계의 Git이다. 코드를 커밋·태그·브랜치로 관리하듯, ML 모델을 실험 번호·[[288_version_ihl_tos_total_length|버전]] 태그·배포 상태로 관리한다. 문제 발생 시 `git revert`처럼 모델을 이전 [[288_version_ihl_tos_total_length|버전]]으로 즉시 [[098_rollback_strategy_pipeline_error_threshold|롤백]]할 수 있다.

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
| Staging | [[395_verification_process_review|검증]]·테스트 중 | 실험 [[282_performance_tactics|성능]] 기준 충족 |
| Production | 현재 [[090_service_kubernetes_network_load_balancing|서비스]] 중 | Champion/Challenger [[395_verification_process_review|검증]] 통과 |
| Archived | 더 이상 사용 안 함 | 새 모델로 교체 후 보관 |

- **📢 섹션 요약 비유**: Champion/Challenger [[268_strategy_pattern|전략]]은 챔피언십 무술 대회와 같다. 현 챔피언(Production 모델)에게 도전자(Staging 모델)가 도전한다. 도전자가 A/B 테스트에서 더 좋은 성과를 내면 왕좌를 빼앗는다(Promotion). 기존 챔피언은 무술 연구원으로 전환(Archived). 언제든 복귀 가능([[098_rollback_strategy_pipeline_error_threshold|롤백]])하도록 기록을 보존한다.

---

## Ⅲ. 비교 및 연결

**[[180_mlflow|MLflow]] [[166_model_registry_versioning_mlflow|Model Registry]] vs SageMaker [[166_model_registry_versioning_mlflow|Model Registry]] vs Vertex [[190_ai_llm_requirements_specification|AI]]**:
| 플랫폼 | 특징 | 적합 환경 |
|:---|:---|:---|
| [[180_mlflow|MLflow]] [[235_registry_immutable_tag|Registry]] | [[191_oss_license_compliance|오픈소스]], 로컬/클라우드 | 자체 구축, 유연성 필요 |
| AWS SageMaker | 완전 관리형, AWS 통합 | AWS 기반 ML 팀 |
| GCP Vertex [[190_ai_llm_requirements_specification|AI]] | 통합 ML 플랫폼 | GCP 기반, [[263_storage_compute_separation_bigquery|BigQuery]] 연동 |
| Azure ML [[235_registry_immutable_tag|Registry]] | Azure 통합 | Azure DevOps와 연계 |

- **📢 섹션 요약 비유**: MLflow는 [[191_oss_license_compliance|오픈소스]] 자작 도서관(자유롭지만 직접 관리), SageMaker는 AWS가 운영하는 종합 도서관(편하지만 AWS 종속), Vertex AI는 Google의 클라우드 도서관이다. 규모·예산·클라우드 [[268_strategy_pattern|전략]]에 맞게 선택해야 하며, 특정 클라우드에 종속되지 않으려면 MLflow가 최선이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[166_model_registry_versioning_mlflow|모델 레지스트리]] 거버넌스 설계**:
1. **승인 워크플로우**: Staging → Production 전환 시 [[001_dikw_pyramid|데이터]] 과학자 + ML 엔지니어 + 비즈니스 스테이크홀더 3자 승인
2. **[[282_performance_tactics|성능]] 임계값 [[164_policy|정책]]**: 정확도 < 95% 또는 [[015_지연_데이터_관점|지연]]시간 > 200ms면 자동 Production 승격 차단
3. **[[098_rollback_strategy_pipeline_error_threshold|롤백]] [[085_sla|SLA]]**: 프로덕션 이슈 발생 시 이전 [[288_version_ihl_tos_total_length|버전]]으로 5분 내 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 보장
4. **규제 준수 [[606_auditing_linux_auditd|감사]]**: 모든 프로덕션 모델의 학습 [[001_dikw_pyramid|데이터]] 출처·[[288_version_ihl_tos_total_length|버전]]·평가 결과를 규제 [[606_auditing_linux_auditd|감사]](Financial, Medical) 대응용으로 보존

- **📢 섹션 요약 비유**: [[166_model_registry_versioning_mlflow|모델 레지스트리]] 3자 승인은 의약품 시판 허가와 같다. 신약(새 모델)이 효과 입증([[001_dikw_pyramid|데이터]] 과학자 [[395_verification_process_review|검증]]) + 안전성 [[396_validation|확인]](ML 엔지니어 [[395_verification_process_review|검증]]) + 비용 대비 효과(비즈니스 승인)를 모두 통과해야 환자(사용자)에게 처방된다. 어느 하나라도 누락하면 [[090_service_kubernetes_network_load_balancing|서비스]] 사고(의료 과실)로 이어진다.

---

## Ⅴ. 기대효과 및 결론

[[166_model_registry_versioning_mlflow|모델 레지스트리]]는 ML 운영의 통제 센터다. 어떤 모델이 어디서 동작하고, 어떤 [[288_version_ihl_tos_total_length|버전]]이 더 좋고, 문제 시 어떻게 [[098_rollback_strategy_pipeline_error_threshold|롤백]]하는지에 대한 명확한 답을 제공한다. [[190_ai_llm_requirements_specification|AI]] 규제(EU [[190_ai_llm_requirements_specification|AI]] Act, 금융 [[190_ai_llm_requirements_specification|AI]] 규제)에서 모델 투명성·추적 가능성·거버넌스를 요구하는 세상에서, [[166_model_registry_versioning_mlflow|모델 레지스트리]]는 [[190_ai_llm_requirements_specification|AI]] 조직의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 증명하는 필수 인프라다. [[180_mlflow|MLflow]], SageMaker, Vertex [[190_ai_llm_requirements_specification|AI]] 등 플랫폼 선택보다 "어떤 거버넌스 프로세스를 설계하는가"가 더 중요한 기술사 판단 포인트다.

- **📢 섹션 요약 비유**: [[166_model_registry_versioning_mlflow|모델 레지스트리]]는 [[190_ai_llm_requirements_specification|AI]] 세계의 의약품 처방 DB다. 어떤 의사가 어떤 환자에게 어떤 약(모델)을 어떤 날짜에 처방했는지 완벽히 추적된다. 부작용([[090_service_kubernetes_network_load_balancing|서비스]] 이상)이 발생하면 즉시 이전 약(이전 [[288_version_ihl_tos_total_length|버전]])으로 교체하고, 동일 부작용이 다시 발생하지 않도록 이력을 분석한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 실험 추적 (Experiment Tracking) | [[180_mlflow|MLflow]], W&B, 하이퍼파라미터 / [[166_model_registry_versioning_mlflow|모델 레지스트리]]에 등록 전 실험 기록 |
| Champion/Challenger | A/B 테스트, 모델 비교 / 프로덕션 모델 교체 의사결정 방법 |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] ([[313_rollback|Rollback]]) | 이전 [[288_version_ihl_tos_total_length|버전]], 즉각 복원 / [[166_model_registry_versioning_mlflow|모델 레지스트리]] 핵심 운영 기능 |
| [[348_mlops|MLOps]] | [[090_configuration_item|CI]]/CD, 자동화 / [[166_model_registry_versioning_mlflow|모델 레지스트리]]가 통합되는 운영 체계 |
| [[190_ai_llm_requirements_specification|AI]] 거버넌스 | 투명성, [[606_auditing_linux_auditd|감사]] 추적 / [[166_model_registry_versioning_mlflow|모델 레지스트리]]가 지원하는 규제 준수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] → [모델 레지스트리 (Model Registry)] → [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. **[[166_model_registry_versioning_mlflow|모델 레지스트리]]**는 [[190_ai_llm_requirements_specification|AI]] 모델의 **"역대 기록 보관소"**예요 — 어떤 [[288_version_ihl_tos_total_length|버전]]이 언제 만들어졌고, 얼마나 정확했고, 지금 어디서 사용 중인지 다 기록해요!
2. 새 AI가 더 좋으면 **챔피언 교체(Production 승격)**, 문제가 생기면 **이전 [[288_version_ihl_tos_total_length|버전]]으로 즉시 [[658_ir_recovery|복구]]([[098_rollback_strategy_pipeline_error_threshold|롤백]])** 할 수 있어요.
3. 의료·금융 규제에서 "이 AI는 어떤 [[001_dikw_pyramid|데이터]]로 만들었나요?"라고 물으면, [[166_model_registry_versioning_mlflow|모델 레지스트리]]가 **완벽한 [[606_auditing_linux_auditd|감사]] 기록**을 제공해요!
