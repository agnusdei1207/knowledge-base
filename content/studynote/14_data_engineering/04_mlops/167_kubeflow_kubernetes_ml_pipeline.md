+++
title = "167. 쿠브플로우 (Kubeflow) - 쿠버네티스 기반 ML 파이프라인"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubeflow는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 위에서 ML 워크로드를 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)하는 플랫폼으로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반의 재현 가능한 ML 파이프라인을 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/))로 정의하고 실행할 수 있게 한다.
> 2. **가치**: Kubeflow Pipelines로 ML 워크플로우를 표준화하고, Katib으로 하이퍼파라미터 자동 최적화([AutoML](/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/))를 실행하며, KServe로 멀티 프레임워크 모델을 단일 플랫폼에서 서빙함으로써 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 전 과정을 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 생태계 안에서 통합한다.
> 3. **판단 포인트**: Kubeflow는 강력하지만 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 운영 전문성이 필요하고 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 설정이 복잡하므로, 클라우드 관리형(Vertex [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Pipelines, SageMaker)과 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)/하이브리드 환경에서의 통제 필요성을 비교하여 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 Kubeflow란?

<strong>Kubeflow</strong>는 Google이 주도하여 개발한 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) ML 플랫폼으로, ML 모델의 개발부터 배포까지 전 과정을 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터에서 실행할 수 있도록 설계됐다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">쿠버네티스 (Kubernetes) 클러스터</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kubeflow</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kubeflow</div><div class="kb-diagram-cell">Katib</div><div class="kb-diagram-cell">KServe</div><div class="kb-diagram-cell">Notebooks</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Pipelines</div><div class="kb-diagram-cell">(AutoML)</div><div class="kb-diagram-cell">(모델 서빙)</div><div class="kb-diagram-cell">(JupyterHub)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DAG 기반</div><div class="kb-diagram-cell">HPO</div><div class="kb-diagram-cell">REST/gRPC</div><div class="kb-diagram-cell">JupyterLab</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ML 파이프</div><div class="kb-diagram-cell">Grid/Random</div><div class="kb-diagram-cell">다중 프레임</div><div class="kb-diagram-cell">GPU 지원</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">라인 실행</div><div class="kb-diagram-cell">Bayesian</div><div class="kb-diagram-cell">워크 서빙</div><div class="kb-diagram-cell">팀 공유</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컨테이너화</div><div class="kb-diagram-cell">HyperBand</div><div class="kb-diagram-cell">카나리 배포</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Training</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Operator</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(TFJob, PyTorchJob,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MXNetJob, XGBoostJob)</div></div>
</div>
</div>



### 1.2 Kubeflow가 해결하는 문제

| 문제 | Kubeflow 해결 방법 |
|:---|:---|
| **환경 재현성** | 모든 단계를 [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 실행 |
| **자원 관리** | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)/CPU 자동 할당 |
| <strong>파이프라인 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a></strong> | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 의존성 관리 |
| <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/">하이퍼파라미터 튜닝</a></strong> | Katib로 [AutoML](/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) 자동화 |
| **모델 서빙 복잡성** | KServe로 멀티 프레임워크 단일 서빙 |
| **실험 추적** | [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) 통합 |

📢 **섹션 요약 비유**: Kubeflow는 ML 버전의 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)라고 할 수 있다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 앱 배포를 자동화하듯, Kubeflow는 ML 모델의 학습→튜닝→서빙 과정을 자동화한다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 인프라 위에서 움직이므로 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) ML의 표준이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Kubeflow Pipelines 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kubeflow Pipelines 내부 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Python Pipeline DSL</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">@dsl.pipeline 데코레이터로 DAG 정의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Pipeline SDK → YAML/JSON 컴파일</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kubeflow Pipelines 백엔드</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">API Server</div><div class="kb-diagram-cell">Pipeline Persistence</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(REST API)</div><div class="kb-diagram-cell">(MySQL)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Scheduler</div><div class="kb-diagram-cell">Artifact Store</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Argo WF)</div><div class="kb-diagram-cell">(MinIO/S3)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ 각 단계는 쿠버네티스 Pod로 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터</div><div class="kb-diagram-cell">→</div><div class="kb-diagram-cell">피처</div><div class="kb-diagram-cell">→</div><div class="kb-diagram-cell">학습</div><div class="kb-diagram-cell">→</div><div class="kb-diagram-cell">평가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">전처리</div><div class="kb-diagram-cell">엔지니어</div><div class="kb-diagram-cell">Pod</div><div class="kb-diagram-cell">Pod</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Pod</div><div class="kb-diagram-cell">링 Pod</div></div>
</div>
</div>



### 2.2 Kubeflow Pipelines Python DSL 예시

```python
from kfp import dsl
from kfp.components import func_to_container_op

# 컴포넌트 정의
@func_to_container_op
def preprocess_data(data_path: str) -> str:
    """데이터 전처리 컴포넌트"""
    import pandas as pd
    df = pd.read_csv(data_path)
    # 전처리 로직...
    output_path = "/mnt/data/processed.parquet"
    df.to_parquet(output_path)
    return output_path

@func_to_container_op
def train_model(data_path: str, epochs: int = 10) -> str:
    """모델 학습 컴포넌트"""
    # 학습 로직...
    model_path = "/mnt/models/model.pkl"
    return model_path

@func_to_container_op
def evaluate_model(model_path: str, threshold: float = 0.9) -> bool:
    """모델 평가 컴포넌트"""
    # 평가 로직...
    return accuracy >= threshold

# 파이프라인 정의 (DAG)
@dsl.pipeline(
    name='ML Training Pipeline',
    description='전처리 → 학습 → 평가 → 배포'
)
def ml_pipeline(data_path: str, epochs: int = 10):
    # 단계 1: 데이터 전처리
    preprocess_task = preprocess_data(data_path=data_path)

    # 단계 2: 모델 학습 (전처리 완료 후 실행)
    train_task = train_model(
        data_path=preprocess_task.output,
        epochs=epochs
    )

    # 단계 3: 모델 평가
    eval_task = evaluate_model(
        model_path=train_task.output
    )

    # 단계 4: 조건부 배포 (평가 통과 시만)
    with dsl.Condition(eval_task.output == 'true'):
        deploy_task = deploy_model(
            model_path=train_task.output
        )
```

### 2.3 Katib (하이퍼파라미터 최적화)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Katib 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">목표 메트릭: Maximize Accuracy</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">하이퍼파라미터 검색 공간:</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">learning_rate:</div><div class="kb-diagram-node">0.0001, 0.01</div><div class="kb-diagram-note">(log uniform)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">batch_size:</div><div class="kb-diagram-node">16, 32, 64, 128</div><div class="kb-diagram-note">(discrete)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">optimizer:</div><div class="kb-diagram-node">'adam', 'sgd', 'rmsprop'</div><div class="kb-diagram-note">(categorical)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Katib Controller ──→ 검색 알고리즘 선택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trial 1: lr=0.001, bs=32, opt=adam → Acc=0.91</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trial 2: lr=0.01, bs=64, opt=sgd → Acc=0.88</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trial 3: lr=0.0001,bs=16, opt=adam → Acc=0.93</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trial N: lr=0.002, bs=32, opt=adam → Acc=0.95</div><div class="kb-diagram-cell">← 최적</div></div>
</div>
</div>



#### Katib 검색 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 원리 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/251_grid_search_random_search/">Grid Search</a></strong> | 모든 조합 탐색 | 완전 탐색 | 경우의 수 기하급수적 증가 | 소수 파라미터 |
| **Random Search** | 무작위 샘플링 | 빠름, 효율적 | 보장 없음 | 대부분 기본 선택 |
| **Bayesian Optimization** | 사전 정보 활용 | 효율적 수렴 | 계산 비용 높음 | 비싼 실험 |
| **HyperBand** | [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) 기반 | 빠른 탐색 | 학습 곡선 필요 | 딥러닝 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/">NAS</a> (Neural <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/">Architecture</a> Search)</strong> | 네트워크 구조 탐색 | 자동 아키텍처 | 매우 높은 비용 | 대규모 딥러닝 |

### 2.4 KServe (모델 서빙)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">KServe 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">InferenceService (CRD)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Transformer (선택) Predictor Explainer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">전처리/후처리 → (모델 서빙) → 예측 설명</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Triton/TF Serving / SHAP/LIME</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PyTorch/Sklearn (선택)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">지원 프레임워크:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TensorFlow</div><div class="kb-diagram-cell">PyTorch</div><div class="kb-diagram-cell">Sklearn</div><div class="kb-diagram-cell">XGBoost</div><div class="kb-diagram-cell">LightGBM</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ONNX</div><div class="kb-diagram-cell">Triton</div><div class="kb-diagram-cell">HuggingFace</div><div class="kb-diagram-cell">MLflow</div><div class="kb-diagram-cell">Custom</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">서빙 기능:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- REST/gRPC 자동 엔드포인트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 카나리 배포 (canaryTrafficPercent)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 자동 스케일링 (KNative 기반)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 배치 추론 (InferenceGraph)</div></div>
</div>
</div>



📢 **섹션 요약 비유**: Kubeflow Pipelines는 자동화된 공장 조립 라인과 같다. 각 작업([컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))은 독립적인 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기계이고, DAG는 조립 순서도이며, Katib은 최적 재료 배합(하이퍼파라미터)을 자동으로 찾아주는 레시피 최적화 로봇이다.

---

## Ⅲ. 비교 및 연결

### 3.1 Kubeflow vs [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) vs SageMaker

| 항목 | Kubeflow | [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | AWS SageMaker |
|:---|:---|:---|:---|
| **유형** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 플랫폼 | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | 클라우드 관리형 |
| **파이프라인** | 완전 지원 (KFP) | 제한적 | 완전 지원 |
| **실험 추적** | [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) 연동 | 핵심 기능 | SageMaker Experiments |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/">AutoML</a></strong> | Katib | 없음 | Autopilot |
| **모델 서빙** | KServe | [mlflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) serve | SageMaker Endpoints |
| **인프라 요구** | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터 | 최소 | AWS 계정 |
| **비용** | 인프라 비용만 | 무료 | 사용량 기반 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/">온프레미스</a></strong> | 완전 지원 | 완전 지원 | 제한적 |
| **학습 곡선** | 가파름 (K8s 지식 필요) | 완만 | 중간 |

### 3.2 [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) Operators ([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 학습)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">TFJob (분산 TensorFlow 학습):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TFJob</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Chief Pod (1개): 마스터 워커</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Worker Pod (4개): 데이터 병렬 학습</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── PS Pod (2개): 파라미터 서버</div></div>
<div class="kb-diagram-note">PyTorchJob (분산 PyTorch 학습):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PyTorchJob</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Master Pod (1개)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Worker Pod (N개): DDP 분산 학습</div></div>
</div>
</div>



### 3.3 Kubeflow vs Airflow 비교

| 항목 | Kubeflow Pipelines | [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) |
|:---|:---|:---|
| **목적** | ML 파이프라인 특화 | 범용 워크플로우 |
| **실행 단위** | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) | 다양한 Executor |
| **ML 특화** | [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 추적, [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) | 없음 (플러그인 필요) |
| **확장성** | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) | CeleryExecutor/K8s |
| **재현성** | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반 완전 | 환경 의존 |
| **사용 편의성** | 어려움 | 상대적으로 쉬움 |

📢 **섹션 요약 비유**: Kubeflow vs Airflow 비교는 ML 전문 병원(Kubeflow)과 종합 병원(Airflow)의 차이다. ML 전문 병원은 ML 치료에 특화된 장비([아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 추적, [AutoML](/knowledge-base/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/))를 갖추고 있고, 종합 병원은 모든 과가 있어 다용도로 활용 가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 Kubeflow 배포 옵션

| 옵션 | 설명 | 적합 환경 |
|:---|:---|:---|
| **kubeflow/manifests** | 공식 [Kustomize](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) 배포 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/), GKE |
| **Kubeflow on AWS** | EKS 기반 최적화 | AWS 환경 |
| **Kubeflow on GCP** | GKE 기반 최적화 | GCP 환경 |
| **Charmed Kubeflow (Ubuntu)** | Ubuntu 기반 간편 설치 | Ubuntu K8s |
| <strong>Vertex <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> Pipelines</strong> | Kubeflow Pipelines [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호환 | GCP 완전 관리형 |

### 4.2 기술사 시험 핵심 포인트

<strong>Q. Kubeflow의 핵심 <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/">컴포넌트</a>와 각각의 역할을 설명하시오.</strong>

| [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | 역할 |
|:---|:---|
| **Kubeflow Pipelines** | Python DSL로 ML 워크플로우 [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 정의·실행, [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 추적 |
| **Katib** | 하이퍼파라미터 최적화 (Grid, Random, Bayesian, HyperBand) |
| **KServe** | 멀티 프레임워크 모델 서빙 ([REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/[gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/), [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/">Training</a> Operators</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 학습 (TFJob, PyTorchJob) |
| **Notebooks** | JupyterHub 기반 팀 협업 노트북 환경 |
| **Central Dashboard** | 모든 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 통합 UI |

<strong>Q. Katib의 하이퍼파라미터 최적화 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>(Bayesian vs Random Search)을 비교하시오.</strong>

- **Random Search**: 균일 분포로 무작위 샘플링, 구현 단순, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 용이, 검색 공간이 넓을 때 효과적
- **Bayesian Optimization**: 이전 시도 결과를 사전 확률로 활용하여 다음 시도 위치를 결정, 실험 횟수가 적을 때 효율적, 비싼 학습(수 시간) 실험에 적합
- **HyperBand**: [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/))를 통해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 낮은 조합을 빠르게 제거, 대규모 탐색에 효율적

### 4.3 Kubeflow 도입 시 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kubeflow 도입 체크리스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인프라</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 쿠버네티스 1.21+ 클러스터 준비</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ GPU 노드 (nvidia-device-plugin) 설치</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 스토리지 클래스 (NFS, Ceph) 구성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 로드 밸런서 또는 Istio Ingress 설정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">팀 역량</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 쿠버네티스 운영 경험 (최소 1명)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ Python + Docker 역량</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ Kubeflow Pipelines SDK 학습</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">대안 검토</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 클라우드 관리형 (Vertex AI, SageMaker) 비용 비교</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ Apache Airflow로 충분한지 검토</div></div>
</div>
</div>



📢 **섹션 요약 비유**: Kubeflow 도입은 수제 요리 공방을 산업용 자동화 식품 공장으로 전환하는 것과 같다. 처음엔 설비 투자(K8s 구축)가 크지만, 대량 생산 단계에서는 수동 대비 압도적인 효율성과 재현성을 제공한다. 단, 공장 운영 전문가(K8s 엔지니어)가 반드시 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 Kubeflow 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 |
|:---|:---|:---|:---|
| **파이프라인 재현성** | 환경 의존, 불확실 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반 완전 재현 | 100% 재현 가능 |
| **자원 활용률** | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 유휴 시간 많음 | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 자동 스케줄링 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 활용률 30% 향상 |
| **HPO 자동화** | 수동 실험 반복 | Katib 자동 탐색 | 실험 시간 60% 단축 |
| **모델 서빙** | 프레임워크별 개별 서버 | KServe 통합 | 운영 복잡도 감소 |
| **팀 협업** | 개인 환경 의존 | 공유 클러스터 | 실험 공유 용이 |

### 5.2 결론

Kubeflow는 ML 워크로드를 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 방식으로 운영하려는 조직의 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 플랫폼 표준이다. 파이프라인 자동화(KFP), 하이퍼파라미터 최적화(Katib), 멀티 프레임워크 서빙(KServe)의 통합이 ML 생산성을 크게 향상시키지만, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 운영 역량이 선행 조건이다.

📢 **섹션 요약 비유**: Kubeflow는 ML 버전의 항공 관제 시스템과 같다. 수많은 ML 파이프라인 비행기(Pipelines)가 이착륙하고, 최적 연료 배합(Katib)을 자동 계산하며, 승객(추론 요청)을 가장 빠른 경로로 안내하는(KServe) 완전 자동화 관제탑이다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 기반 인프라 | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) ([쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)) | Kubeflow의 실행 환경 |
| 핵심 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | Kubeflow Pipelines | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 ML 파이프라인 |
| 핵심 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | Katib | 하이퍼파라미터 자동 최적화 |
| 핵심 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) | KServe | 멀티 프레임워크 모델 서빙 |
| 비교 도구 | [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | 범용 워크플로우 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) |
| 비교 도구 | [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) | 실험 추적 + [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) |
| 비교 도구 | AWS SageMaker | 클라우드 관리형 ML 플랫폼 |
| 상위 개념 | [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) | Kubeflow는 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 실행 플랫폼 |
| 연관 | [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) | Kubeflow Pipelines로 [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 구현 |
| 연관 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 학습 | TFJob, PyTorchJob [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 학습 지원 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. Kubeflow는 LEGO 공장 조립 라인 같아요. 각 부품([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))은 독립적으로 만들고, 조립 순서([DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/))에 따라 자동으로 완성 제품(학습된 모델)을 만들어요.
2. Katib은 레시피 최적화 로봇이에요. 소금을 얼마나 넣을지(하이퍼파라미터) 여러 번 시험해서 가장 맛있는 비율(최적 파라미터)을 자동으로 찾아줘요.
3. KServe는 다국어 통역사 같아요. TensorFlow로 만들든 PyTorch로 만들든 어떤 모델이든 하나의 API로 통역해서 사람들이 이용할 수 있게 해줘요.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">수동 ML 실험 (노트북 기반)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ML 파이프라인 자동화</div>
<div class="kb-diagram-tree-item" style="--depth:2">Kubeflow Pipelines: K8s 기반 DAG 파이프라인</div>
<div class="kb-diagram-tree-item" style="--depth:2">Katib: 하이퍼파라미터 자동 최적화</div>
<div class="kb-diagram-tree-item" style="--depth:2">KServe: 멀티 프레임워크 모델 서빙</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">컨테이너 기반 재현성 (Docker + K8s)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SageMaker Pipelines · Vertex AI Pipelines (클라우드 관리형)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">LLMOps 파이프라인: 프롬프트 관리 · RAG · PEFT 스케줄링</div>
</div>
</div>



---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 167 / 258

← **이전**: [166. 모델 레지스트리 (Model Registry) - 버전 관리 MLflow](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)
**다음**: [168. 데이터 파이프라인 워크플로우 DAG 제어 (Apache Airflow) 자동화](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) →

---
