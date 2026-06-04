---
title: "378. 쿠버네티스 오토스케일링 HPA VPA CA (Kubernetes Autoscaling HPA VPA Cluster)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스 오토스케일링은 Pod 수평 확장(HPA), Pod 리소스 수직 조정(VPA), 노드 수 확장(CA)의 3축 제어로 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]` 알고리즘과 Node Group ASG 연동을 통해 클러스터 용량과 워크로드 자원을 자동 매칭하는 선언적(Declarative) 제어 메커니즘이다.
> 2. **가치**: EKS/AKS/GKE 환경에서 평균 30~70% 인프라 비용 절감(FinOps 효과), 트래픽 피크 시 p99 응답지연 40% 개선, MTTR(Mean Time To Recover) 단축을 통한 SRE 운영 효율 극대화, Capacity Planning 자동화로 인한 운영 엔지니어 Opex 절감.
> 3. **판단 포인트**: HPA는 빠른 스케일아웃에 강하지만 스케일링 지연(30~60s) 존재, VPA는 Pod 재시작을 수반하여 무중단 요구 시 배포 전략(PDB, surge) 검토 필수, CA는 노드 프로비저닝 시간(2~5분) 고려한 사전 스케일링(Buffer) 및 PodDisruptionBudget·PriorityClass 기반 스케줄링 정책이 핵심 결정 요인이다.

---

## Ⅰ. 개요 및 필요성

클라우드 네이티브 환경의 트래픽 패턴은 일간/주간/계절성 변동, 마케팅 이벤트, 배치 작업 등 예측 불가능한 부하 변동을 보인다. 전통적인 VM 기반 인프라에서는 Peak Load 기준으로 과도하게 프로비저닝(Over-Provisioning)하여 평균利用率 15~25% 수준에 머물렀고, 이는 약 60~75%의 유휴 자원 낭비로 직결되었다. 쿠버네티스 오토스케일링은 `Metrics Server`, `kube-state-metrics`, `Custom Metrics Adapter`(Prometheus Adapter, Datadog Cluster Agent 등), `Cluster Autoscaler Provider`(AWS ASG, GCP MIG, Azure VMSS)를 통합한 Control Loop 기반의 탄력적 자원 공급 체계로, **선언적 명세(Deployment.spec.replicas)** 와 **관측 가능한 지표** 의 피드백 루프를 통해 셀프힐링·셀프스케일링을 구현한다.

```text
+---------------------------------------------------------------------+
|              Traditional VM Infra vs Kubernetes Autoscaling          |
+---------------------------------------------------------------------+
|                                                                      |
|  [Legacy: Peak-based Provisioning]                                  |
|   CPU ^        +------ Peak 고정 프로비저닝 ------+                 |
|   100%|      +-+                                  +-+               |
|       |    +-+  (유휴 60~75%)                       +--             |
|   40% |---+                                                       |
|       |                                                            |
|   0% +-------------------------------------------------- Time      |
|           Mon  Tue  Wed  Thu  Fri  Sat  Sun                        |
|                                                                      |
|  [K8s Autoscaling: Elastic Provisioning]                            |
|   CPU ^        +--+              +---+                              |
|   100%|      +-+  +---+       +-+   +--+                          |
|       |    +-+        +-----╲╱         +-+                          |
|   30% |---+  (HPA+CA 동적 매칭, 利用率 70%+)                        |
|       |                                                            |
|   0% +-------------------------------------------------- Time      |
|           Mon  Tue  Wed  Thu  Fri  Sat  Sun                        |
|                                                                      |
+---------------------------------------------------------------------+
```

기존 Auto Scaling Group(ASG) 단독 운영은 ① 노드 단위의 coarse-grained 제어, ② 컨테이너 밀도 미고려, ③ 애플리케이션 메트릭(APM/RPS/Queue Depth) 미반영이라는 한계를 가졌다. 쿠버네티스는 이를 **Pod 레벨의 HPA -> Node 레벨의 CA** 라는 2-tier 자동화로 정교화하고, VPA로 Pod 단위 리소스 권장값을 자동 튜닝하여 Right-Sizing을 실현한다.

- **📢 섹션 요약 비유**: 전통적 ASG는 "사람이 손으로 수도꼭지를 조작"하는 방식이고, K8s 오토스케일링은 "목욕탕 수위 감지 센서(HPA) + 온도 조절기(VPA) + 물탱크 펌프(CA)"가 협업하여 수온·수량을 자동 유지하는 스마트 욕조 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+-----------------------------------------------------------------------+
|         Kubernetes 3-Layer Autoscaling Control Loop Architecture     |
+-----------------------------------------------------------------------+
|                                                                       |
|  +----------------------- LAYER 1: WORKLOAD ----------------------+  |
|  |  +------------+    +------------+    +--------------------+    |  |
|  |  | Deployment |    | StatefulSet|    |  Custom Controller |    |  |
|  |  | (stateless)|    |  (DB 등)   |    |  (CronJob, KEDA)   |    |  |
|  |  +-----+------+    +-----+------+    +----------+---------+    |  |
|  |        |                 |                      |              |  |
|  |  +-----v------+    +-----v------+    +----------v---------+    |  |
|  |  |    HPA     |    |    VPA     |    |   External Scaler  |    |  |
|  |  | (Pod 수)   |    |(Req/Limit) |    |  (KEDA, KEDA-EDA)  |    |  |
|  |  +-----+------+    +-----+------+    +----------+---------+    |  |
|  +--------+-----------------+-----------------------+-------------+  |
|           |                 |                       |                 |
|           v                 v                       v                 |
|  +------------------- LAYER 2: METRICS -------------------------+   |
|  |                                                                |   |
|  |  +--------------+   +------------------+  +----------------+  |   |
|  |  | Metrics      |   | kube-state-      |  | Custom Metrics |  |   |
|  |  | Server       |   | metrics          |  | Adapter        |  |   |
|  |  | (CPU/Mem)    |   | (Object 상태)    |  | (Prom/Cloud)   |  |   |
|  |  +------+-------+   +--------+---------+  +--------+-------+  |   |
|  |         |                    |                     |          |   |
|  |         +--------------------+---------------------+          |   |
|  |                              v                                |   |
|  |                  +-----------------------+                     |   |
|  |                  |   metrics.k8s.io API  |                     |   |
|  |                  |   custom.metrics.k8s.io|                     |   |
|  |                  |   external.metrics.k8s |                     |   |
|  |                  +-----------+-----------+                     |   |
|  +------------------------------+--------------------------------+   |
|                                 |                                     |
|  +---------------------- LAYER 3: INFRA ---------------------------+  |
|  |                              v                                  |  |
|  |   +--------------------------------------------------+          |  |
|  |   |          Cluster Autoscaler (CA)                  |          |  |
|  |   |  - Unschedulable Pod 감시 (15s default)         |          |  |
|  |   |  - Bin-packing Simulation으로 최적 노드 도출    |          |  |
|  |   |  - Node Group Min/Max/Desired 조정 명령         |          |  |
|  |   +-----------------+--------------------------------+          |  |
|  |                     v                                           |  |
|  |    +-------------+  +-------------+  +-------------+           |  |
|  |    | AWS ASG     |  | GCP MIG     |  | Azure VMSS  |           |  |
|  |    | Karpenter*  |  | (Auto Mode) |  | (AKS VPA)   |           |  |
|  |    +-------------+  +-------------+  +-------------+           |  |
|  +----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **HPA (HorizontalPodAutoscaler)** | Pod 복제본 수를 수평 확장 | `kube-controller-manager` 내 HPA Controller가 15초 주기(default `--horizontal-pod-autoscaler-sync-period`)로 metrics API 조회, `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]` 계산. stabilization window(`--horizontal-pod-autoscaler-downscale-stabilization`, default 5분)로 flapping 방지. `behavior` 필드(API v2)로 scaleUp/Down 정책 분리. |
| **VPA (VerticalPodAutoscaler)** | Pod의 CPU/Memory request/limit 자동 조정 | 3개 컴포넌트로 구성: `Recommender`(과거 메트릭 분석, OOM/VPA Recommender 알고리즘), `Updater`(eviction 기반 Pod 재생성), `Admission Webhook`(요청 시 권장값 주입). `updateMode: Auto\|Initial\|Off`. `resourcePolicy.containerPolicies`로 특정 컨테이너 제외 가능. |
| **CA (Cluster Autoscaler)** | 클러스터 노드 수를 동적 확장/축소 | Pending 상태 30초 이상 지속 Pod 감지 -> Bin-packing 시뮬레이션(`AddToScale`/`ScaleDown`) -> Cloud Provider API로 Node Group 크기 조정. Scale-down은 10분 유휴(`--scale-down-utilization-threshold=0.5`) + 10분 비사용 후(`--scale-down-delay-after-delete`) 실행. `expander: least-waste\|random\|most-pods\|priority` 전략 지원. |
| **Metrics Pipeline** | 오토스케일링 결정의 데이터 소스 | `cAdvisor`(kubelet) -> `Metrics Server`(in-memory, 5분 retention) -> `metrics.k8s.io` API. 확장 시 `kube-state-metrics`(object 상태) + Prometheus Adapter(`prometheus-adapter/k8s-prometheus-adapter`)를 통해 `custom.metrics.k8s.io`(QPS, Queue Depth, Latency) 노출. KEDA(Kubernetes Event-Driven Autoscaling)는 60+ 외부 소스(RabbitMQ, Kafka, SQS, Redis Streams) 트리거 제공. |

**HPA 핵심 알고리즘 상세**:
```
desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]

복합 메트릭(Multi-Metric) 사용 시:
desiredReplicas = max[ recompute_metric(m) for m in metrics ]
                   ※ 각 메트릭이 독립적으로 replica 수 계산 후 최대값 채택

비율형 메트릭(Ratio): desiredReplicas = ceil[ currentReplicas × (currentUtilization / targetUtilization) ]
평균값형 메트릭(AverageValue): desiredReplicas = ceil[ sum(currentValues) / targetAverageValue ]
```

**HPA 안정화 윈도우 & 행동 정책 예시**:
```yaml
behavior:
  scaleUp:
    stabilizationWindowSeconds: 0       # 즉시 확장
    policies:
    - type: Percent
      value: 100
      periodSeconds: 30                # 30초마다 2배까지
    - type: Pods
      value: 4
      periodSeconds: 30
    selectPolicy: Max
  scaleDown:
    stabilizationWindowSeconds: 300    # 축소 전 5분 대기
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60
    selectPolicy: Min
```

**VPA의 권장값 산정 로직**:
Recommender는 과거 데이터(`PrometheusHistogramMetric` 또는 `pods_memory_working_set_bytes`)를 백분위 분석하여 `lowerBound`, `target`, `upperBound` 산출. 기본 정책은 P95~P99 사용량을 기반으로 target 도출, OOMKill 이력이 있으면 `oomBump` 비율로 상향 보정. `containerPolicies.minAllowed`/`maxAllowed`로 안전 범위 강제.

- **📢 섹션 요약 비유**: HPA는 "레스토랑 테이블 수를 늘리는 것", VPA는 "각 테이블의 크기(2인용->4인용)를 조절하는 것", CA는 "레스토랑 자체의 면적을 늘리는 것"이다. 손님(트래픽)이 늘면 테이블(HPA)->테이블 크기(VPA)->매장(CA) 순으로 대응한다.

---

## Ⅲ. 비교 및 연결

| 구분 | HPA (Horizontal Pod Autoscaler) | VPA (Vertical Pod Autoscaler) | CA (Cluster Autoscaler) |
| :--- | :--- | :--- | :--- |
| **스케일링 차원** | Pod 개수(수평) | Pod당 CPU/Memory(수직) | Node 개수(수평, Infra) |
| **제어 대상** | Deployment, ReplicaSet, StatefulSet, ReplicationController | 단일 Pod의 requests/limits | Node Group(AWS ASG, GCP MIG), Karpenter NodePool |
| **반응 시간** | 30~60초(HPA sync 15s + Scheduler) | 5~10분(권장값 산정 후 eviction->재스케줄) | 2~5분(Cloud API 응답 + Node Ready 시간, AMI/image pull 포함) |
| **메트릭 소스** | CPU, Memory, Custom(QPS, Lag, Queue), External(SQS) | 과거 사용량 분석(P95~P99) | Pending Pod 수, Node utilization |
| **무중단 영향** | Rolling Update로 무중단 | ⚠️ Pod 재시작(Eviction) 발생 가능 | ⚠️ Scale-down 시 PDB·Eviction 정책 필요 |
| **상호 운용** | VPA·HPA 동시 사용 시 `resources.requests.cpu|memory` 중복 설정 시 충돌 발생 (Custom/External 메트릭만 HPA에 사용 권장) | HPA와 동일 메트릭 동시 사용 불가(off: 권장값만 조회) | Karpenter 등장으로 점차 대체 추세 (v1beta1->GA 진행) |
| **비용 영향** | Pod 수 증가 -> 노드 포화 -> CA 트리거 | 노드당 Pod 밀도 증가 -> 노드 수 감소 -> CA scale-down | 동적 노드 수 -> 유휴 자원 비용 절감 |
| **적합 워크로드** | Stateless API, Web, Worker | Stateful 서비스(중요도 중간), JVM Heap 튜닝 | 모든 워크로드(Infrastructure-wide) |
| **한계점** | Cold Start 지연(파드 기동 시간), 메트릭 노이즈 민감 | Eviction으로 인한 일시적 다운타임, StatefulSet 비권장 | 노드 추가 지연, Scale-down 보수적(10분 유휴), 단일 Cloud 종속 |

**Karpenter vs Cluster Autoscaler 비교 (2024~ 현재 트랜드)**:
Karpenter는 AWS가 2021년 출시, 2024년 GA 전환, 2025년 현재 CNCF Sandbox 프로젝트로 확대. CA 대비 ① 30초 내 Provisioning, ② Spot/On-Demand 혼합, ③ Instance Type 다양화(ND/AMD/GPU), ④ Consolidation을 통한 20~40% 추가 비용 절감, ⑤ 노드 lifecycle 단일 컨트롤러 단순화로 전환 가속. 단, 멀티 클라우드 지원은 여전히 CA가 우위.

**연계 아키텍처 (실무 패턴)**:
- **KEDA + HPA**: 외부 메시지 큐(RabbitMQ/Kafka/SQS) lag 기반 HPA 확장. KEDA가 External Scaler 역할.
- **HPA + CA 수직 통합**: `kube-system`의 `cluster-autoscaler` Deployment는 PDB 0 설정(스케줄링 우선), 일반 워크로드는 PDB `minAvailable: 1` 이상 권장.
- **Karpenter + Spot**: NodePool에서 `instanceRequirements`(vCPU, Memory, Architecture, CapacityType) 정의 -> 자동 Spot fallback, Interruption Queue(SQS EventBridge) 기반 2분 전 안전 Drain.

```text
+------------------ Real-world Integration Topology ------------------+
|                                                                      |
|  Client --► ALB --► Ingress(NGINX) --► Service                      |
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 378 / 800

<- **이전**: [377. 쿠버네티스 스케줄링 노드 어피니티 테인트](/studynote/13_cloud_architecture/06_exam_summary/377_kubernetes_scheduling_affinity_taint_tolerati/)
**다음**: [379. 쿠버네티스 스토리지 CSI 퍼시스턴트 볼륨](/studynote/13_cloud_architecture/06_exam_summary/379_kubernetes_storage_csi_persistent_volume/) ->

---
