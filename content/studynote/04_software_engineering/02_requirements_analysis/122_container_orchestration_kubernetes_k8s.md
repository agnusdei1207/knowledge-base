---
title: 122. 컨테이너 오케스트레이션 (Container Orchestration) - K8s 핵심 개념과 아키텍처
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[561_container_based_deployment|컨테이너]] 오케스트레이션은 **수백~수천 개 [[561_container_based_deployment|컨테이너]]의 배포·[[249_scaling_normalization_standardization|스케일링]]·네트워킹·자동 [[658_ir_recovery|복구]]를 자동화**하는 시스템이며, [[205_kubernetes_container_orchestration|Kubernetes]](K8s)가 사실상 유일한 산업 표준이다.
> 2. **가치**: 단일 [[063_docker_architecture|Docker]] [[561_container_based_deployment|컨테이너]]는 `docker run`으로 관리하지만, 프로덕션 환경에서 수백 [[561_container_based_deployment|컨테이너]]의 **헬스체크·오토스케일링·[[117_rolling_update_deployment|롤링 업데이트]]·[[306_service_discovery_pattern|서비스 디스커버리]]**를 수동 관리하는 것은 불가능하며, K8s가 이를 **선언적으로 자동화**한다.
> 3. **판단 포인트**: K8s의 핵심은 **[[080_kube_controller_manager_desired_state|Desired State]] → Reconciliation Loop**이며, [[198_pod_kubernetes_minimum_deployment_unit|Pod]]·[[087_deployment_kubernetes_workload_rolling_update|Deployment]]·[[090_service_kubernetes_network_load_balancing|Service]]·Ingress의 4대 리소스와 Control Plane([[014_api_posix|API]] Server·[[078_etcd_distributed_key_value_store|etcd]]·Scheduler·Controller Manager)의 아키텍처를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    K8s 클러스터 아키텍처                              │
├───────────────────────────────────────────────────────┤
│  [Control Plane (Master)]                             │
│   API Server ← kubectl / CI/CD                       │
│   etcd (상태 저장소)                                  │
│   Scheduler (Pod 배치)                                │
│   Controller Manager (Reconciliation)                 │
│                                                       │
│  [Worker Nodes]                                       │
│   kubelet → Pod(Container) 실행                      │
│   kube-proxy → 네트워크 라우팅                       │
│   Container Runtime (containerd)                      │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: K8s는 항공 관제탑(Control Plane)이 수백 대 비행기([[561_container_based_deployment|컨테이너]])의 이착륙·경로·연료(리소스)를 자동 관리하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4대 핵심 리소스

| 리소스 | 역할 |
|:---|:---|
| **[[198_pod_kubernetes_minimum_deployment_unit|Pod]]** | [[561_container_based_deployment|컨테이너]] 실행 최소 단위 |
| **[[087_deployment_kubernetes_workload_rolling_update|Deployment]]** | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[016_replication_factor|복제]]·[[117_rolling_update_deployment|롤링 업데이트]] 관리 |
| **[[090_service_kubernetes_network_load_balancing|Service]]** | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 그룹에 안정적 네트워크 엔드포인트 |
| **[[094_ingress_kubernetes_l7_routing_gateway|Ingress]]** | 외부 [[461_http_stateless_connection_oriented|HTTP]] 트래픽 [[339_routing_overview_best_path_selection|라우팅]] |

- **📢 섹션 요약 비유**: Pod는 방([[561_container_based_deployment|컨테이너]]), Deployment는 아파트 동([[016_replication_factor|복제]] 관리), Service는 우편함(고정 주소), Ingress는 정문(외부 접근)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[063_docker_architecture|Docker]] Compose | K8s | Nomad |
|:---|:---|:---|:---|
| **규모** | 단일 호스트 | **멀티 노드 클러스터** | 멀티 노드 |
| **Self-healing** | 없음 | **자동 [[658_ir_recovery|복구]]** | 자동 [[658_ir_recovery|복구]] |
| **생태계** | 작음 | **최대 ([[190_cncf_landscape_observability|CNCF]])** | 작음 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### K8s 도입 판단 기준
- [[561_container_based_deployment|컨테이너]] 10개 이하: [[063_docker_architecture|Docker]] Compose로 충분.
- [[561_container_based_deployment|컨테이너]] 50개+, 멀티팀: K8s 도입 적합.
- [[206_serverless_cold_start|서버리스]] 우선: AWS Fargate/Cloud Run 고려.

---

## Ⅴ. 기대효과 및 결론

K8s는 **클라우드 네이티브의 운영 체제**이며, [[190_cncf_landscape_observability|CNCF]] 생태계([[302_service_mesh_istio|Istio]]·ArgoCD·[[136_prometheus|Prometheus]]·[[825_cilium_ebpf_kubernetes_networking_security|Cilium]])와 결합하여 현대 인프라의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[198_pod_kubernetes_minimum_deployment_unit|Pod]]** | K8s 최소 실행 단위 |
| **[[087_deployment_kubernetes_workload_rolling_update|Deployment]]** | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[016_replication_factor|복제]]·업데이트 관리 |
| **Control Plane** | [[014_api_posix|API]] Server·[[078_etcd_distributed_key_value_store|etcd]]·Scheduler |
| **[[190_cncf_landscape_observability|CNCF]]** | K8s 생태계 재단 |
| **[[207_helm_kubernetes_package_manager_chart|Helm]]** | K8s 패키지 매니저 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Docker (2013) — 컨테이너 런타임]
    │
    ▼
[Docker Swarm / Mesos (2014~) — 초기 오케스트레이션]
    │
    ▼
[Kubernetes (2014, Google→CNCF) — 산업 표준]
    │
    ▼
[Managed K8s (EKS/GKE/AKS, 2018~)]
    │
    ▼
[현재: K8s + Service Mesh + GitOps — 클라우드 네이티브 풀스택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K8s는 **항공 관제탑**이에요. 수백 대 비행기([[561_container_based_deployment|컨테이너]])를 자동으로 관리해요.
2. 비행기가 고장 나면 **자동으로 다른 비행기를 보내서(Self-healing)** [[090_service_kubernetes_network_load_balancing|서비스]]가 멈추지 않아요.
3. "비행기 3대 유지해"라고 말하면(선언적) **관제탑이 알아서** 3대를 유지한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 973

← **이전**: [[121_cicd_pipeline_automation|121. CI/CD 파이프라인 자동화 - 빌드·테스트·배포의 지속적 통합/전달 체계]]
**다음**: [[123_serverless_faas_aws_lambda|123. 서버리스 & FaaS (Serverless / AWS Lambda) - 인프라 없는 함수 단위 컴퓨팅]] →

---
