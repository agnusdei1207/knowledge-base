---
title: "426. 클라우드 ML 세이지메이커 버텍스 AI (Cloud ML SageMaker Vertex AI)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS SageMaker와 GCP Vertex AI는 데이터 준비->모델 학습->튜닝->배포->모니터링으로 이어지는 end-to-end MLOps 파이프라인을 매니지드 서비스로 제공하며, SageMaker Studio/Studio Lab IDE, SageMaker Pipelines(SageMaker Airflow/Kubernetes 기반 오케스트레이션), Feature Store(Online/Offline Store 분리), Multi-Model Endpoints, SageMaker Neo(런타임 최적화) 및 Vertex AI Workbench(managed JupyterLab), Vertex AI Pipelines(Kubeflow Pipelines v2 호환), Vertex AI Feature Store(Online serving via Bigtable, Offline via BigQuery), Vector Search(전 ScaNN 기반), Model Garden, GenAI Studio(파운데이션 모델 튜닝)로 구성된다.
> 2. **가치**: 자체 인프라 대비 학습 시간 70~90% 단축(Spot Instance + SageMaker Training Compiler / Vertex AI Reduction Server), GPU/TPU 비용 50% 이상 절감(예: ml.p4d.24xlarge vs 직접 구매 A100), Feature Store를 통한 학습-서빙 데이터 스큐(TSBS, Training-Serving Bias) 제거, MLOps 자동화로 모델 재학습·드리프트 감지·A/B 트래픽 분배(Canary/Shadow)를 코드형 IaC(CloudFormation/Terraform/Pulumi)로 일관성 있게 운영 가능.
> 3. **판단 포인트**: 멀티클라우드·하이브리드 전략 시 인터롭 표준(ModelCard, ModelBiasReport, Open Inference Protocol), 데이터 주권(리전/CMK/VPC Service Controls)·규제 컴플라이언스(IRAP, ISO 27001, K-ISMS-P), Feature Store의 Online/Offline 일관성 보장 방식(SageMaker는 In-memory/Redis, Vertex는 Bigtable), 컴퓨팅 선택(SageMaker ml.trn1/inf2(Tranium) vs Vertex A3/H3(GB200 NVL72)), 그리고 GenAI 시대의 RAG(Vector Search vs pgvector vs OpenSearch)·파인튜닝 전략(LoRA/QLoRA vs Vertex GenAI Studio Tuning) 결정이 핵심 트레이드오프.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 ML 워크로드는 ① 데이터 양의 폭증(PB급 Lake on S3/GCS), ② 모델 복잡도의 기하급수적 증가(Billion~Trillion 파라미터, MoE, Diffusion), ③ 운영 부담(재학습·드리프트·규제 대응)이라는 3중 압력을 받는다. 전통적 On-Premise ML Stack(Spark + GPU 서버 + Airflow + MLflow + Flask serving)은 ML플래폼 엔지니어 1인당 관리 모델 수 5~10개가 한계였으며, 2017년 AWS SageMaker 등장으로 "managed Jupyter + Training Jobs + Endpoints" 표준이 정립되었고, GCP는 AI Platform(2017)->Vertex AI(2021)로 통합·재편되어 SageMaker Studio와 대등한 통합 플랫폼으로 격상되었다.

```text
+--------------------------------------------------------------------------+
|            On-Premise ML vs Cloud Managed ML(SageMaker / Vertex)         |
+--------------------------------------------------------------------------+
|                                                                          |
|  [전통적 On-Premise ML]                      [Cloud Managed ML]          |
|  +-------------------+                      +-----------------------+    |
|  | Data Lake (HDFS)  |                      | S3 / GCS / BigQuery   |    |
|  |   v               |                      |   v (Native)          |    |
|  | Spark/Hadoop      |   ------->            | Glue / Dataflow       |    |
|  |   v               |                      |   v                   |    |
|  | GPU Server Farm   |   Managed            | Training Job (Spot)   |    |
|  | (수동 프로비저닝) |   Service화          | ml.p5/p4d/H100/A100   |    |
|  |   v               |                      |   v                   |    |
|  | Airflow + MLflow  |                      | Pipelines(KFP/StepFn) |    |
|  |   v               |                      |   v                   |    |
|  | Flask + Gunicorn  |                      | Endpoint(Auto-Scale)  |    |
|  |   v               |                      |   v                   |    |
|  | Grafana/Prometheus|                      | Model Monitor/CloudMon|    |
|  +-------------------+                      +-----------------------+    |
|   - 6~12개월 구축, MLOps 인력 5명+ 필요      - 클릭 5회로 프로덕션 배포   |
|   - 활용률 30% 이하 (자원 낭비)              - 활용률 70%+ (Auto-Scale) |
|   - 재현성/감사 추적 어려움                 - Lineage(Feature->Model)  |
+--------------------------------------------------------------------------+
```

**필요성 정량 지표**:
- IDC 2024 보고서 — Fortune 500 기업의 73%가 최소 1개 이상의 Cloud ML Platform 운영 중
- ML 모델 평균 배포 사이클 — On-Prem 90일 vs SageMaker/Vertex 14일
- GPU 인스턴스 CapEx(OpEx 전환) — H100 80GB 1장당 1,200만원(2024) -> ml.p5.48xlarge 시간당 $98.32로 즉시 사용

- **📢 섹션 요약 비유**: 데이터·모델·배포가 한꺼번에 폭증하는데, 옛날 방식으로는 "매번 수제로 요리하는 셰프"였다면, SageMaker/Vertex AI는 **"주방·냉장고·오븐·서빙까지 전부 갖춘 스마트 주방"** — 레시피(파이프라인)만 주면 자동으로 음식(모델)이 만들어지고 손님(추론 요청)에게 서빙된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. AWS SageMaker 핵심 컴포넌트 아키텍처

```text
                    +-------------------------------------+
                    |  SageMaker Studio / Studio Lab     |  IDE: JupyterLab + IDE
                    |  (Web-based, SSO/IAM 통합)           |  + Experiments + Trials
                    +------------+------------------------+
                                 | SDK(boto3) / Python / Autopilot UI
                                 v
        +--------------------------------------------------------+
        |                  SageMaker Studio Domain              |
        |  +----------+  +----------+  +---------+  +--------+ |
        |  | Data Wrgl|  | Ground   |  |Feature  |  |Clarify | |  데이터·윤리
        |  | (Wrangler|  | Truth    |  |Store    |  |(Bias/  | |
        |  | + EMR)   |  |(Labeling)|  |(Online/ |  |Explain.)| |
        |  +----+-----+  +----+-----+  |Offline) |  +---+----+ |
        |       |              |        +----+----+      |      |
        +-------+--------------+-------------+-----------+------+
                |              |             |           |
        +-------v--------------v-------------v-----------v------+
        |              SageMaker Pipelines (Step Functions)     |
        |  Processing -> Training(Tuning) -> Model Eval ->       |
        |  Register -> Condition -> Deploy -> Monitor            |
        +-------+--------------+-------------+------------------+
                |              |             |
                v              v             v
        +-------------+  +--------------+  +----------------+
        |  Training   |  |   Inference  |  |   Model        |
        |  Job (Spot) |  |   Endpoint   |  |   Registry     |
        |             |  | +----------+ |  |  (Lineage)     |
        | - Distributed| | |Real-Time | |  |  + Model Cards |
        |  (DDP/FSDP) |  | +----------+ |  |  (Gov/Reg)     |
        | - Training  |  | |Batch Trnf| |  +----------------+
        |  Compiler  |  | +----------+ |
        | - Debugger  |  | |Multi-Model| |
        | - Profiler  |  | +----------+ |
        | - Heterog.  |  | |Asynchron.| |
        |  Cluster    |  | +----------+ |
        |             |  | |Serverless| |
        |             |  | +----------+ |
        |             |  | |SageMaker | |
        |             |  | |Neo(opt)  | |
        |             |  | +----------+ |
        |             |  | |Inf2(TRN) | |
        +-------------+  | +----------+ |
                         +----------------+
                                 |
                                 v
        +--------------------------------------------------+
        |  Model Monitor (Drift / Bias / Feature Attribution|
        |  Data Quality / Model Quality / Bias Drift         |
        |  -> CloudWatch / EventBridge -> 자동 재학습 트리거   |
        +--------------------------------------------------+
```

### B. GCP Vertex AI 핵심 컴포넌트 아키텍처

```text
                       +--------------------------+
                       |  Vertex AI Workbench     |  Managed JupyterLab
                       |  (User-managed / Mngd)   |  + Colab Enterprise
                       +------------+-------------+
                                    | SDK(google-cloud-aiplatform)
                                    v
        +------------------------------------------------------+
        |                Vertex AI Platform (Unified)          |
        |  +----------+  +----------+  +----------+ +--------+|
        |  |  Datasets|  | Feature  |  |  Model   | |Vector  ||
        |  |  (CSV/   |  |  Store   |  | Registry | |Search  ||
        |  |   TFRec) |  |(Bigtable/|  |(Mgnd/OSS)| |(ScaNN) ||
        |  +----+-----+  | BigQuery)|  +----+-----+ +---+----+|
        |       |        +----+-----+       |           |     |
        +-------+-------------+-------------+-----------+-----+
                |             |             |           |
        +-------v-------------v-------------v-----------v-----+
        |          Vertex AI Pipelines (Kubeflow v2)         |
        |  Kubeflow DSL / TFX / Custom Components             |
        |  (Google Cloud Build + Artifact Registry 실행)       |
        +-------+-------------+-------------------------------+
                |             |
                v             v
        +--------------+  +---------------------+
        |  Training    |  |  Prediction Endpoints|
        |  - Custom    |  |  - Online Predict    |
        |  - AutoML    |  |  - Batch Predict     |
        |  - GenAI     |  |  - Private Endpoint  |
        |    Tuning    |  |  - GenAI Endpoints   |
        |  - Reduction |  |  - Vector Search     |
        |    Server    |  |  - Matching Engine   |
        |  - TPU v5e/  |  +----------+----------+
        |    H100/A100 |             |
        |  - A3 (GB200)|             v
        +--------------+  +----------------------+
                          | Vertex AI Model      |
                          | Monitoring           |
                          | (Drift / Skew /      |
                          |  Feature Attribution)|
                          +----------------------+
```

### C. 구성 요소별 세부 명세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Data Wrangler / Vertex Datasets** | 데이터 전처리·EDA | SageMaker: 300+ 변환(스크립트 자동 생성, Quick Model); Vertex: BigQuery/Federated Query로 SQL-기반 변환 + Data Labeling(외부 인력/AI-Assisted) |
| **Ground Truth / Vertex Data Labeling** | 라벨링 작업 관리 | Active Learning 라운드, 객체 분할(3D/2D), Vertex는 Gemini 기반 AI-Assisted Pre-Labeling 지원 |
| **Feature Store (Online/Offline)** | 피처 중앙 관리·서빙 | SageMaker: Online은 In-memory Dict(밀리초) / ElastiCache Redis, Offline은 S3+Iceberg; Vertex: Online은 Bigtable(10ms p99), Offline은 BigQuery(SQL 조인) |
| **Pipelines** | 워크플로우 오케스트레이션 | SageMaker: Step Functions 기반 DAG(SageMaker Airflow Operator 연동); Vertex: Kubeflow Pipelines v2 SDK + Argo Workflows, 재시도/캐싱(lineage-aware caching) |
| **Training Compute** | 분산 학습 | SageMaker: DDP/FSDP/SM Distributed Data Parallel + Training Compiler(XLA, 30~50% 학습 시간 단축), Heterogeneous Cluster(Head:CPU, Worker:GPU); Vertex: Reduction Server(NCCL 플러그인, 100Gbps), TPU v5e/v6, A3(H100), A3 Mega(GB200 NVL72) |
| **Hyperparameter Tuning** | 자동 하이퍼파라미터 탐색 | SageMaker: Bayesian/Random + Warm Start + Hyperband; Vertex: Vertex AI Vizier(Bayesian + Transfer Tuning + Multi-Objective) |
| **AutoML** | 자동 모델 탐색·학습 | SageMaker Autopilot: 최대 50개 모델 동시 탐색 + 앙상블; Vertex AutoML: Tabular/Timeseries/Image/Text/Video 도메인 특화, AutoGluon/H2O 백엔드 + LLM AutoML |
| **Endpoints** | 추론 서빙 | SageMaker: Real-time, Async(청크+S3), Batch(완전 관리), Multi-Model(동적 로딩 1k+ 모델), Serverless(콜드 스타트 1~3s), Neo 컴파일(10x throughput, 1/10 메모리); Vertex: Online/Batch/Private Service Access, GenAI Endpoints(Claude/Gemini/Llama), Vector Search(ANN, ScaNN) |
| **Model Registry** | 모델 버전·메타데이터 관리 | SageMaker: Model Group/Version + Model Card(책임 있는 AI), Approval workflow; Vertex: Model Registry + Evaluation(MaaS) + Model Garden(200+ 파운데이션 모델) |
| **Model Monitor** | 드리프트 감지·자동 재학습 | SageMaker: Data/Model/Bias/Feature-Attribution Drift -> CloudWatch -> EventBridge Lambda -> SageMaker Pipeline Trigger; Vertex: Drift Detection(Skew) + Auto-Restart Training Trigger + Explainable AI |
| **Neo / Optimization** | 런타임 최적화 | SageMaker Neo: XGBoost/TF/PyTorch/MXNet -> CPU/GPU/Inf1(ML Inf)/Inf2(AWS Trainium) 타겟 컴파일; Vertex는 TF-TRT/Torch-TensorRT/OpenXLA 호환 |

### D. 핵심 알고리즘 / 메커니즘

**1) SageMaker Heterogeneous Cluster**
```
[Head Node (ml.m5.xlarge)] -- step 데이터 broadcast / gradient reduce --+
   | Param Server, Gang Scheduling, EFA(400Gbps)                          |
   v                                                                      |
[GPU Worker Nodes (ml.p5.48xlarge × 8)] ---- AllReduce(8x H100) ----------+
```
EFA(Elastic Fabric Adapter) + NCCL AllReduce로 8K GPU까지 선형 확장. Training Compiler는 XLA 그래프 최적화(연산자 융합, 메모리 계획)로 동일 epoch 대비 30~50% 시간 단축.

**2) Vertex AI Reduction Server**
- 표준 NCCL AllReduce는 NIC 대역폭에서 병목 -> Vertex는 **커널 우회 커스텀 AllReduce**를 제공해 Gradient 전송 단계에서 1
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 426 / 800

<- **이전**: [425. 클라우드 ETL 글루 데이터플로 데이터퓨전](/studynote/13_cloud_architecture/06_exam_summary/425_cloud_etl_glue_dataflow_datafusion/)
**다음**: [427. GPU 인스턴스 AI 학습 추론 최적화](/studynote/13_cloud_architecture/06_exam_summary/427_gpu_instance_ai_training_inference/) ->

---
