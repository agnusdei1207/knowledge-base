---
title: "113. Kubeflow MLOps 오케스트레이션 - K8s 네이티브 ML 파이프라인·실험 관리"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubeflow는 [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 위에서 <strong>ML 워크플로 전체(<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 전처리 -> 학습 -> <a href="/studynote/10_ai/01_ai_basics/041_bagging_boosting/">하이퍼파라미터 튜닝</a> -> 서빙 -> 모니터링)</strong>를 선언적으로 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)하는 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 기반 <strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a> 플랫폼</strong>이다.
> 2. **가치**: 주피터 노트북에서 실험한 모델을 프로덕션에 올리려면 Docker화·스케줄링·[GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 할당·A/B 서빙 등 <strong>"ML의 마지막 1마일"</strong>을 해결해야 하며, [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) Pipelines가 이를 <strong><a href="/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/">DAG</a>(방향 비순환 <a href="/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>)로 자동화</strong>한다.
> 3. **판단 포인트**: Kubeflow는 K8s 운영 역량이 전제되므로 **진입 장벽이 높으며**, 소규모 팀에는 Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)(GCP)·SageMaker(AWS) 같은 관리형 MLOps가 더 적합할 수 있다.

---

## Ⅰ. 개요 및 필요성

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자의 87%가 "주피터 노트북에서 잘 되던 모델이 프로덕션에서 안 된다"고 말한다. 이 간극을 <strong>"ML <a href="/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a>(Hidden <a href="/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">Technical Debt</a>)"</strong>라 하며, Kubeflow는 이를 해소한다.

```text
+-------------------------------------------------------+
|    Kubeflow 핵심 컴포넌트 아키텍처                     |
+-------------------------------------------------------+
|  +----------+  +----------+  +----------+            |
|  | Notebooks|  | Pipelines|  |  Katib   |            |
|  | (실험)   |  | (파이프  |  | (HP 튜닝)|            |
|  |          |  |  라인)   |  |          |            |
|  +----+-----+  +----+-----+  +----+-----+            |
|       |              |              |                 |
|       v              v              v                 |
|  +--------------------------------------+             |
|  |        Kubernetes Cluster           |             |
|  |  GPU Node Pool + CPU Node Pool      |             |
|  +----------+---------------------------+             |
|             |                                         |
|  +----------v----------+                              |
|  |   KServe (모델 서빙) |  Canary / A-B 배포         |
|  +---------------------+                              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Kubeflow는 ML 공장의 <strong>컨베이어 벨트 시스템</strong>이다. 원재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 투입 -> 가공(전처리) -> 조립(학습) -> 품질 검사(평가) -> 출하(서빙)가 자동으로 흘러간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)

| [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | 역할 | 비유 |
|:---|:---|:---|
| **Notebooks** | 주피터 노트북 서버 ([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 자동 할당) | 실험실 |
| **Pipelines** | 전처리->학습->평가 [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | 컨베이어 벨트 |
| **Katib** | 하이퍼파라미터 자동 튜닝 (Bayesian/Random) | 실험 계획 로봇 |
| **KServe** | 모델 서빙 ([Canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)·A/B·오토스케일링) | 제품 배송 |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/">Training</a> Operators</strong> | TFJob·PyTorchJob ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 학습) | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 공장 |

- **📢 섹션 요약 비유**: Katib는 요리사(모델)에게 "소금을 얼마나 넣어야 맛있는지" 수백 번 시도해주는 <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 미식가</strong>다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) | SageMaker | Vertex [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
|:---|:---|:---|:---|
| **인프라** | 자체 K8s | AWS 관리형 | GCP 관리형 |
| **유연성** | **최고** | 중간 | 중간 |
| **운영 부담** | **높음** | 낮음 | 낮음 |
| <strong><a href="/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/">벤더 종속</a></strong> | 없음 ([OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)) | AWS | GCP |
| **적합** | 대규모, K8s 역량 보유 | AWS 중심 | GCP 중심 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 판단 기준
1. **K8s 운영 팀 존재**: 있으면 [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/), 없으면 관리형.
2. **멀티클라우드 요구**: 있으면 [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) (벤더 중립).
3. <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 워크로드 규모</strong>: 대규모 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 학습 -> [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) [Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) Operators.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>5인 팀이 <a href="/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/">Kubeflow</a> 직접 운영</strong>: K8s 운영 부담 > ML 개발 시간 -> 관리형 추천.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 ML 배포 | [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) | 개선 |
|:---|:---|:---|:---|
| 모델 배포 주기 | 월 1회 | **일 수회** | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 수준 |
| 실험 추적 | 수동 엑셀 | <strong>자동 <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 저장</strong> | 재현성 확보 |
| HP 튜닝 | 수동 그리드 | **Katib 자동 (Bayesian)** | 최적 파라미터 자동 탐색 |

Kubeflow는 <strong><a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> 시대의 <a href="/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/">Fine-tuning</a> 파이프라인·<a href="/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/">RAG</a> 서빙</strong>과 결합하여 GenAI Ops 플랫폼으로 진화 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/">Kubeflow</a> Pipelines</strong> | ML 워크플로 [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) |
| **Katib** | 하이퍼파라미터 자동 튜닝 |
| **KServe** | K8s 네이티브 모델 서빙 ([Canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)/A-B) |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/180_mlflow/">MLflow</a></strong> | 실험 추적 경쟁 도구 (경량) |
| <strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a></strong> | Kubeflow가 구현하는 상위 규율 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 ML 배포 (주피터 -> Docker -> 수동 서빙)]
    |
    v
[Kubeflow 0.x (2018, Google) — K8s 기반 ML 플랫폼 시작]
    |
    v
[Kubeflow Pipelines v2 (2022~) — DAG 성숙, Katib 통합]
    |
    v
[KServe (2021~) — Knative 기반 모델 서빙 표준화]
    |
    v
[현재: GenAI Ops — LLM Fine-tuning·RAG 파이프라인 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Kubeflow는 공장의 <strong>자동 컨베이어 벨트</strong>예요. 재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 넣으면 완제품([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델)이 나와요.
2. Katib라는 로봇은 **"소금 얼마, 설탕 얼마"를 수백 번 바꿔가며** 제일 맛있는 레시피를 찾아줘요.
3. 다 만들어진 제품은 KServe라는 <strong>택배 시스템</strong>이 고객에게 배달(서빙)해준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 371

<- **이전**: [112. 서버리스 K8s (Serverless Kubernetes) - AWS Fargate·Azure ACI·Virtual Kubelet](/studynote/13_cloud_architecture/07_container_k8s/112_serverless_kubernetes_fargate/)
**다음**: [114. Argo CD (ArgoCD GitOps CD) - K8s 선언적 지속 배포·Git 단일 진실 원천](/studynote/13_cloud_architecture/07_container_k8s/114_argocd_gitops_cd/) ->

---
