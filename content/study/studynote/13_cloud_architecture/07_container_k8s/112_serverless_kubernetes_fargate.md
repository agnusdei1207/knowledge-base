+++
weight = 112
title = "112. 서버리스 K8s (Serverless Kubernetes) - AWS Fargate·Azure ACI·Virtual Kubelet"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[206_serverless_cold_start|서버리스]] K8s는 **노드(서버) 관리 없이 [[085_pod_kubernetes_container_unit|파드]]만 선언하면 클라우드가 자동으로 컴퓨팅 자원을 할당**하는 모델로, K8s의 [[073_container_orchestration_tools|오케스트레이션]] API를 유지하면서 노드 [[528_provisioning|프로비저닝]]·패치·[[249_scaling_normalization_standardization|스케일링]] 부담을 제거한다.
> 2. **가치**: 기존 K8s는 노드(EC2)를 직접 관리해야 하므로 OS 패치·[[162_ami_advanced_metering_infrastructure|AMI]] 업데이트·Cluster Autoscaler [[009_config|설정]] 등 **운영 오버헤드가 크다**. Fargate/ACI는 이를 **완전히 제거**하여 개발자가 [[085_pod_kubernetes_container_unit|파드]] YAML만 작성하면 된다.
> 3. **판단 포인트**: [[206_serverless_cold_start|서버리스]] K8s는 **[[085_pod_kubernetes_container_unit|파드]]당 비용**이 자체 노드보다 비싸므로, **버스트 트래픽·배치 작업·이벤트 드리븐** 워크로드에 적합하고, 상시 부하가 높은 워크로드는 **자체 노드 + [[209_spot_instance_cloud_cost_optimization|Spot Instance]]**가 비용 효율적이다.

---

## Ⅰ. 개요 및 필요성

K8s를 운영하려면 노드(워커) 관리가 필수다: OS 패치, [[022_kernel_role|커널]] 업데이트, 노드 [[249_scaling_normalization_standardization|스케일링]], [[162_ami_advanced_metering_infrastructure|AMI]] 교체. 이 운영 부담이 소규모 팀에게는 K8s 도입 자체의 장벽이 된다.

```text
┌───────────────────────────────────────────────────────┐
│    기존 K8s vs 서버리스 K8s 관리 범위                   │
├───────────────────────────────────────────────────────┤
│  [기존 K8s (EKS + EC2)]                               │
│   개발자 관리: Pod YAML + 노드 AMI + OS 패치          │
│                + Cluster Autoscaler + Spot 관리       │
│                                                       │
│  [서버리스 K8s (EKS + Fargate)]                       │
│   개발자 관리: Pod YAML만!                            │
│   AWS 관리: 노드 생성·패치·스케일링·보안 전부         │
│                                                       │
│   트레이드오프: 파드당 비용 ↑, DaemonSet 불가          │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 기존 K8s는 자가용(직접 관리·저렴), [[206_serverless_cold_start|서버리스]] K8s는 택시(관리 불필요·비쌈)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[090_service_kubernetes_network_load_balancing|서비스]] | 클라우드 | 방식 | 특징 |
|:---|:---|:---|:---|
| **AWS Fargate** | AWS EKS | [[085_pod_kubernetes_container_unit|파드]]별 microVM 할당 | [[334_process|DaemonSet]] 미지원 |
| **Azure ACI** | Azure AKS | Virtual Kubelet으로 [[085_pod_kubernetes_container_unit|파드]] 위임 | [[418_gpu|GPU]] 지원 |
| **GKE Autopilot** | GCP | 노드 자동 [[528_provisioning|프로비저닝]] | 가장 K8s 네이티브 |
| **Virtual [[082_kubelet_node_agent|Kubelet]]** | 멀티클라우드 | 가상 노드로 외부 [[090_service_kubernetes_network_load_balancing|서비스]]에 [[085_pod_kubernetes_container_unit|파드]] 위임 | 범용 |

### Fargate 동작 원리
EKS에 Fargate Profile을 [[009_config|설정]]하면, 해당 네임스페이스의 [[085_pod_kubernetes_container_unit|파드]]가 **EC2 노드 대신 Fargate의 독립 microVM에서 실행**된다. 각 [[085_pod_kubernetes_container_unit|파드]]는 전용 [[022_kernel_role|커널]]에서 격리되어 보안이 강화된다.

- **📢 섹션 요약 비유**: Fargate는 호텔([[085_pod_kubernetes_container_unit|파드]]마다 독립 방)이고, EC2 노드는 기숙사(여러 [[085_pod_kubernetes_container_unit|파드]]가 한 방 공유)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 자체 노드 (EC2) | Fargate ([[206_serverless_cold_start|서버리스]]) |
|:---|:---|:---|
| **노드 관리** | 직접 (OS 패치 등) | **AWS 전담** |
| **비용 모델** | 노드 시간당 과금 | **[[085_pod_kubernetes_container_unit|파드]] vCPU·메모리 시간당** |
| **[[334_process|DaemonSet]]** | 지원 | **미지원** |
| **[[418_gpu|GPU]]** | 지원 | 제한적 |
| **적합 워크로드** | 상시 고부하 | **버스트·배치·이벤트** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 하이브리드 [[268_strategy_pattern|전략]]
- **상시 워크로드**: EC2 Managed Node Group ([[209_spot_instance_cloud_cost_optimization|Spot Instance]]) → 비용 최적.
- **버스트 워크로드**: Fargate → [[129_spike_agile_technical_investigation|스파이크]] 시만 [[085_pod_kubernetes_container_unit|파드]] [[087_process_state_transition|생성]], 유휴 시 비용 0.
- **배치 작업**: Fargate → Job 실행 후 자동 종료, 노드 낭비 없음.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **모든 워크로드를 Fargate에**: 상시 트래픽 [[090_service_kubernetes_network_load_balancing|서비스]]를 Fargate로 돌리면 EC2 대비 **2~3배 비용**.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 자체 노드 | [[206_serverless_cold_start|서버리스]] K8s | 개선 |
|:---|:---|:---|:---|
| 노드 운영 부담 | 높음 | **0** | 완전 제거 |
| 보안 격리 | 공유 [[022_kernel_role|커널]] | **[[085_pod_kubernetes_container_unit|파드]]별 독립 [[022_kernel_role|커널]]** | 강화 |
| 버스트 비용 | 사전 [[528_provisioning|프로비저닝]] | **사용한 만큼** | 유연 |

[[206_serverless_cold_start|서버리스]] K8s는 **Karpenter(차세대 노드 오토스케일러)**와 결합하여 자체 노드와 [[206_serverless_cold_start|서버리스]]의 장점을 혼합하는 하이브리드 모델로 수렴 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **AWS Fargate** | EKS [[206_serverless_cold_start|서버리스]] [[085_pod_kubernetes_container_unit|파드]] 실행 환경 |
| **Virtual [[082_kubelet_node_agent|Kubelet]]** | 가상 노드로 외부 [[090_service_kubernetes_network_load_balancing|서비스]]에 [[085_pod_kubernetes_container_unit|파드]] 위임 |
| **GKE Autopilot** | Google의 완전 관리형 [[206_serverless_cold_start|서버리스]] K8s |
| **Karpenter** | 차세대 노드 오토스케일러, 하이브리드 [[268_strategy_pattern|전략]] |
| **[[342_faas|FaaS]] ([[216_lambda_kappa_architecture_batch_realtime|Lambda]])** | [[206_serverless_cold_start|서버리스]]의 함수 단위 실행 (K8s 외부) |

### 📈 관련 키워드 및 발전 흐름도

```text
[K8s + 자체 노드 관리 (2015~) — 운영 오버헤드 높음]
    │
    ▼
[AWS Fargate for EKS (2019) — 노드 관리 제거]
    │
    ▼
[GKE Autopilot (2021) — 완전 관리형 K8s]
    │
    ▼
[Karpenter (2021~) — 지능형 노드 오토스케일링]
    │
    ▼
[현재: 하이브리드 — 상시(자체 노드) + 버스트(서버리스)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 기존 K8s는 **자기 집(서버)을 직접 관리**해야 해서, 청소·수리를 다 해야 돼요.
2. [[206_serverless_cold_start|서버리스]] K8s는 **호텔**처럼 방([[085_pod_kubernetes_container_unit|파드]])만 예약하면 청소·수리를 호텔(클라우드)이 다 해줘요!
3. 대신 호텔비가 좀 비싸니까, **여행(버스트 트래픽)** 때만 호텔을 쓰고 평소에는 집에서 사는 게 좋답니다!