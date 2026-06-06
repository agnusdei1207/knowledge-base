---
title: "Cloud AI Serving Endpoint Scaling"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPU 자원의 비선형적 비용 구조(예: A100 80GB 시간당 약 $3.06 vs CPU 대비 50배)에서 출발한 **AI 서빙 스케일링은 Kubernetes HPA + KEDA 이벤트 드리븐 + NVIDIA Triton/TGI/vLLM의 동적 배칭(dynamic batching)**을 결합하여, p99 지연시간을 SLA 내로 유지하면서 GPU Utilization을 60% 이상으로 끌어올리는 다층 오토스케일링 체계이다.
> 2. **가치**: Cold Start를 Warm Pool(예: KServe 0->1, 약 8~15초 단축)로 줄이고, **Continuous Batching(vLLM, 2024)**, **PagedAttention(KV Cache 메모리 4~24배 효율화)**, **In-flight Batching(Triton)**을 통해 LLM Throughput을 **23배**(vLLM vs naive HF)까지 향상시키며, Spot Instance + Queue-based 스케일링으로 인프라 비용을 60~80% 절감 가능하다.
> 3. **판단 포인트**: 트레이드오프는 **(a) Cold Start 지연 vs 비용 효율**, **(b) 처리량 최대화(batching^) vs 지연시간 최소화(queue depthv)**, **(c) GPU 종류 균일성(성능 최적화) vs 이기종 GPU(MIG/H100/A100 혼용, 유연성)** 사이에서 발생하며, LLM(메모리 바운드)·비전 CNN(연산 바운드)·추천 시스템(메모리/연산 혼합) 등 모델 특성별 스케일링 전략을 차별화해야 한다.

---

## Ⅰ. 개요 및 필요성

AI 모델의 학습(Training) 비용은 단발성 Capex 성격이 강하지만, **추론(Inference) 서빙은 365일 24시간 발생하는 Opex**이다. 2024년 기준 대규모 생성형 AI 서비스(예: ChatGPT, Claude, Copilot)는 **일 평균 수억~수십억 토큰**을 처리하며, 이를 안정적으로 제공하기 위한 엔드포인트 스케일링은 클라우드 인프라 운영의 핵심 과제가 되었다.

전통적인 웹 서비스 스케일링은 **요청 단위(RPS) 기반의 Stateless 컨테이너 수평 확장**으로 충분했지만, AI 서빙은 다음의 구조적 차이로 인해 동일한 접근이 통하지 않는다.

```
+---------------------------------------------------------------------+
|        기존 웹 서비스 vs AI 추론 서빙의 구조적 차이                    |
+---------------------------------------------------------------------+
|                                                                     |
|  [기존 웹 서비스]                  [AI 추론 서빙]                    |
|  +----------+                    +----------------------+          |
|  | Nginx    |  Stateless        | Triton / vLLM        |          |
|  | App Pod  |  - 수 ms 응답       | - State(가중치) 보유   |          |
|  | DB Cache |  - CPU 충분        | - GPU 필요            |          |
|  +----------+                    | - 수십~수백 초 응답     |          |
|       |                          | - Batching 필수       |          |
|       |   HPA: CPU/Memory        +----------------------+          |
|       v                                  |                          |
|  +----------+                  +----------------------+            |
|  | 5~50 Pod |                  | GPU 노드 풀 관리     |            |
|  | CPU 노드 |                  | 1~수백 장 (A100/H100) |            |
|  +----------+                  +----------------------+            |
|                                                                     |
|  ❗ 결정적 차이점:                                                    |
|  ① 모델 가중치 수 GB~수백 GB -> Pod 이동/시작 비용 큼                  |
|  ② GPU 자원 분할/공유 기술 필요 (MIG, MPS, Time-slicing)            |
|  ③ 응답시간이 길어 Queue 기반 + 비동기 처리 필수                     |
|  ④ 동적 배칭(Dynamic Batching)으로 Throughput 최적화                |
|  ⑤ Cold Start 문제 (8~60초) -> Warm Pool, Pre-warmed Pod 필수       |
+---------------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm)**

| 구분 | 기존 웹 스케일링 (Web 2.0) | AI 서빙 스케일링 (AI 2.0) |
| :--- | :--- | :--- |
| 자원 단위 | vCPU, Memory (GB) | GPU (A100, H100, L4), NPU, Memory, VRAM |
| 부하 신호 | CPU%, RPS, Queue depth | GPU SM Utilization, KV Cache 사용률, 토큰/s |
| 스케일링 단위 | Pod (수 ms~수 초 시작) | GPU 노드 (수 분), Warm Pod (수 초) |
| 처리량 최적화 | Connection Pool, Thread | Dynamic Batching, Continuous Batching, Speculative Decoding |
| 비용 모델 | Pay-per-Request, Reserved | GPU 시간(고정) + Token 기반(Passthrough) 혼합 |
| 트래픽 패턴 | Poisson, 주기적 | Viral(챗봇), Bursty(검색/추천), Long-tail(다국어 LLM) |

- **📢 섹션 요약 비유**: AI 서빙 스케일링은 마치 **고속도로 톨게이트**와 같다. 일반 웹 트래픽은 승용차가 빠르게 지나가는 것이지만, AI 추론은 **컨테이너 트럭(GPU)이 화물(모델 가중치)을 싣고 고속 톨게이트(엔드포인트)를 통과**하는 형태다. 트럭이 막히지 않으면서도 톨게이트 비용(토큰당 비용)을 최소화하려면, **여러 화물을 모아 한 번에 운송(배칭)**, **트럭 대기장(Warm Pool) 운영**, **혼잡 시 추가 톨게이트(Auto-scaling)**를 동시에 운영해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 AI 서빙 엔드포인트 스케일링은 **4계층 오토스케일링 아키텍처**로 구성된다.

```
+--------------------------------------------------------------------------+
|         4-Layer Cloud AI Serving Endpoint Scaling Architecture           |
+--------------------------------------------------------------------------+
|                                                                          |
|   [Client Apps]                                                         |
|        | HTTPS / gRPC / WebSocket                                       |
|        v                                                                |
|   +-----------------------------------------------------+               |
|   | Layer 1: L7 LB / API Gateway (Global)               |               |
|   |  - Envoy, NGINX, AWS ALB, GCP GLB                   |               |
|   |  - Token-aware Routing (헤더 모델명/version)         |               |
|   |  - Rate Limit, Retry, Circuit Breaker                |               |
|   +-----------------------------------------------------+               |
|        |                                                                |
|        v                                                                |
|   +-----------------------------------------------------+               |
|   | Layer 2: Service Mesh / Inference Gateway           |               |
|   |  - Istio, KServe Ingress, Cloud Run Gateway          |               |
|   |  - Canary(10%->50%->100%), A/B Routing                |               |
|   |  - mTLS, Token 인증, Model ID 기반 분기              |               |
|   +-----------------------------------------------------+               |
|        |                                                                |
|        v                                                                |
|   +-----------------------------------------------------+               |
|   | Layer 3: Inference Server (Model Serving)            |               |
|   |  - NVIDIA Triton (Backend: TensorRT/PyTorch/ONNX)   |               |
|   |  - vLLM (LLM 특화, PagedAttention)                  |               |
|   |  - TGI(HuggingFace), TorchServe, BentoML, MLflow     |               |
|   |  - Dynamic/Continuous Batching, KV Cache 관리        |               |
|   |  - CUDA Graphs, FlashAttention, Quantization         |               |
|   +-----------------------------------------------------+               |
|        |  PCIe / NVLink                                                 |
|        v                                                                |
|   +-----------------------------------------------------+               |
|   | Layer 4: GPU Resource Orchestration                  |               |
|   |  - Kubernetes + GPU Operator (NVIDIA Device Plugin) |               |
|   |  - MIG(7-instance), MPS, Time-slicing               |               |
|   |  - HPA / VPA / KEDA / Karpenter                     |               |
|   |  - Cluster Autoscaler (GPU 노드 1~수백)              |               |
|   |  - Spot/On-demand Mix, Warm Pool                    |               |
|   +-----------------------------------------------------+               |
|                                                                          |
|   [Storage: S3/GCS 모델 가중치 (10~700GB), Feature Store, Vector DB]      |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **NVIDIA Triton Inference Server** | 표준 모델 서빙 런타임 | TensorRT/PyTorch/ONNX/Python 백엔드, HTTP/gRPC, Dynamic Batching(max_batch_size, queue_policy), Concurrent Model Execution, Model Analyzer로 최적 설정 탐색 |
| **vLLM (LLM 전용)** | LLM 추론 특화 서빙 | PagedAttention(블록 단위 KV Cache, 4~24배 효율), Continuous Batching(매 디코드 스텝마다 신규 요청 삽입), 23배 throughput 달성(vs HuggingFace naive) |
| **HuggingFace TGI** | LLM/Transformer 서빙 | Rust 기반, FlashAttention v2/v3, Paged Attention, Token streaming, GPTQ/AWQ 양자화 내장 |
| **KServe (Kubeflow)** | Kubernetes-native 추론 플랫폼 | Serverless(0->N 스케일), Canary Rollout, ModelMesh(다수 모델 동적 로딩), Transformer(전/후처리), Open Inference Protocol v2 |
| **KEDA (Kubernetes Event-driven Autoscaling)** | 이벤트 기반 HPA 확장기 | Kafka/RabbitMQ/Prometheus/Cron ScaledObject, 0까지 스케일 다운(Scale-to-Zero), GPU 메트릭(nvidia-smi-exporter) 트리거 |
| **Karpenter** | AWS 노드 프로비저너 | Spot/Odor-aware 스케줄링, 50초 내 노드 준비, GPU/TPU/별가속기 자동 선택, Consolidation(비용 최소화) |
| **NVIDIA GPU Operator + Device Plugin** | GPU 자원 노출/관리 | `nvidia.com/gpu: 1` 등 리소스 노출, MIG(1->7 slice), MPS, Time-slicing(4-way share), DCGM 메트릭 수집 |
| **Model Mesh / Multi-Model Serving** | 다수 모델 동적 로딩 | LRU Eviction, 모델 가중치(700B) 시 RAM/VRAM 초과분 SSD Tier 캐싱, Pod당 수십~수백 모델 |

### 핵심 알고리즘 및 파라미터

**(1) Dynamic Batching의 수학적 이해**
Triton의 Dynamic Batching은 다음과 같은 큐잉 모델을 따른다.

```
처리량(throughput) = batch_size / (T_static + batch_size × T_per_sample)

  - T_static: 모델 고정 오버헤드 (커널 로딩, attention setup)
  - T_per_sample: 샘플당 처리 시간
  - batch_size: 동일 forward pass에 묶이는 요청 수
```

`max_batch_size` ^ -> Throughput ^, Latency ^
트레이드오프 -> 보통 `max_queue_delay_microseconds` (예: 10000μs=10ms)로 cap

**(2) Continuous Batching (vLLM)**
- 기존 Static Batching: 가장 긴 시퀀스 끝날 때까지 짧은 요청 대기 (GPU 낭비)
- Continuous Batching: 매 iteration마다 완료된 요청 제거 + 신규 요청 삽입
- 효과: 평균 GPU utilization 30%->80%, throughput 23× (vLLM 논문, SOSP'23)

**(3) PagedAttention 메모리 관리**
- KV Cache를 OS의 Paging처럼 **블록(보통 16 token) 단위로 분할**
- 내부 단편화(Internal Fragmentation) 4% 이하 (vs 기존 60~80%)
- 메모리 낭비 4~24배 감소 -> 동일 VRAM에서 동시 처리량 4×^

**(4) HPA 스케일링 공식 (K8s HPA)**
```
desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]

예: GPU Utilization 현재 80%, 목표 60%
     desiredReplicas = 5 × (80/60) = 7 (Pod)
```
- 안정화 윈도우(`--horizontal-pod-autoscaler-downscale-stabilization`, 기본 5분)
- 스케일 업 30s~1m, 스케일 다운 5m (Cost-saving 위해 비대칭)

**(5) Queue-based Autoscaling (KEDA + Kafka/SQS)**
```
backlog_per_pod = queue_depth / current_pod_count
if backlog_per_pod > threshold (예: 5):  scale_up
if backlog_per_pod < 1 for 10min:       scale_to_zero
```
- LLM 응답시간 30초인 경우, RPS보다 **queue depth**가 더 정확한 스케일링 신호

- **📢 섹션 요약 비유**: 4계층 구조는 **공항 관제 시스템**과 같다. **1층(API Gateway)**은 탑승구(보안/게이트), **2층(Inference Gateway)**은 활주로 라우팅(우선순위/Canary), **3층(Inference Server)**은 실제 항공기(GPU/엔진), **4층(Resource Orchestration)**은 격납고/지상조직원(노드/스케줄링)이다. 비행기 이착륙이 지연되면 활주로(처리량)를 늘리고, 수요가 줄면 격납고(Pod)를 닫아 비용을 절감한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **KServe / Knative** | **Triton Inference Server** | **SageMaker Endpoint** | **Cloud Run / Lambda (GPU)** |
| :--- | :--- | :--- | :--- | :--- |
| **주 사용처** | K8s-native 멀티모델 | GPU 추론 표준 런타임 | AWS 매니지드 ML 서빙 | 경량/콜드 스타트 허용 |
| **스케일링** | HPA + KEDA + Scale-to-Zero | 자체 부하 분산 (single pod) | Target Tracking (Invocations, GPU%) | 요청 기반 (1->N), Cold Start 큼 |
| **모델 크기** | 수 GB~수백 GB (PVC/OCI) | 수 GB~수십 GB (Local FS) | 수 GB~수백 GB (S3 마운트) | 10GB 이하 권장 (Container size) |
| **Batching** | 사용자 구현 (Triton 통합 가능) | Dynamic Batching 내장 | Mini-batch 자동 (Built-in) | 미지원 (Stateless 권장) |
| **GPU** | NVIDIA GPU, MIG 지원 | CUDA/TensorRT 최적화 | 모든 인스턴스 (G4/G5/P4/P5) | L4 (Cloud Run, 2024 GA) |
| **Cold Start** | 5~15s (Warm Image, Knative) | 8~30s (모델 로드 포함) | 30~60s (엔드포인트) | 5~10s (L4) |
| **비용 모델** | 노드 시간 (BYO K8s) | 노드 시간 (BYO K8s) | 인스턴스 시간 + Invocations | 요청/시간 (Pay-per-use) |
| **운영 부담** | 높음 (CRD, Istio) | 중간 (서버 운영) | 낮음 (매니지드) | 매우 낮음 (서버리스) |
| **적합 시나리오** | 하이브리드, On-Prem 연동 | 고성능 GPU 서빙 | AWS 종속, 빠른 출시 | 트래픽 변동 크고 LLM API |

### 상호 보완 관계 및 통합 패턴

```
[프레임워크 선택 의사결정 플로우]
                  +---------------------+
                  |  트래픽 패턴은?      |
                  +----------+----------+
            +----------------+----------------+
            v                v                v
        Constant        Bursty/Viral      LLM Streaming
            |                |                |
            v                v                v
      SageMaker       Cloud Run
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 428 / 800

<- **이전**: [427. GPU 인스턴스 AI 학습 추론 최적화](/studynote/13_cloud_architecture/06_exam_summary/427_gpu_instance_ai_training_inference/)
**다음**: [429. 클라우드 벡터 DB 유사도 검색 서비스](/studynote/13_cloud_architecture/06_exam_summary/429_cloud_vector_db_similarity_search_service/) ->

---
