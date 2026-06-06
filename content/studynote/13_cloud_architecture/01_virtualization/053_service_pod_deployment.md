---
title: "Service Pod Deployment"
date: "2026-05-01"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) ([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))는 배포의 최소 실행 단위이고, 배포 ([Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 원하는 상태를 관리한다.
> 2. **가치**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 바뀌는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) IP를 숨기고 안정적인 접점을 제공한다.
> 3. **판단 포인트**: 라벨/셀렉터, readiness/liveness probe, [롤링 업데이트](/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/)가 안전한 배포의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 그냥 띄우는 것만으로는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 운영이 되지 않는다. [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 바뀌어도 접점이 유지되어야 하고, 배포 중에도 사용자는 끊기지 않아야 한다.

그래서 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)에서는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/), [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 배포를 함께 설계한다. [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 실행, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 접근, 배포는 변경을 담당한다.

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 배포는 가게 간판은 그대로 두고 안의 점원만 바꿔도 손님이 못 느끼게 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Deployment는 ReplicaSet을 통해 원하는 수의 Pod를 유지하고, Service는 label selector로 Pod를 묶어 안정적인 네트워크 엔드포인트를 제공한다.

```text
Deployment -> ReplicaSet -> Pod
Service -----------------> Pod (via selector)
```

| 구성 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) | 실행 단위 | 일시적 |
| [ReplicaSet](/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) | 개수 유지 | self-healing |
| [Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) | 배포 관리 | [롤링 업데이트](/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/) |
| [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 안정적 접점 | 가상 IP / [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) |

핵심은 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) IP가 바뀌어도 Service가 앞단에서 묶어 준다는 점이다. 그래서 클라이언트는 뒤의 변화를 몰라도 된다.

- **📢 섹션 요약 비유**: [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 자주 바뀌는 직원이고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 손님이 기억하는 대표 전화번호다.

---

## Ⅲ. 비교 및 연결

Service는 ClusterIP, NodePort, LoadBalancer 등으로 노출 방식이 달라진다. Deployment는 [Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/) 앱에 적합하고, StatefulSet은 상태를 가진 워크로드에 적합하다.

| 항목 | [Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) | [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| :--- | :--- | :--- |
| 역할 | 배포 제어 | 통신 접점 |
| 변경 대상 | [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 수/[버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) | 접근 경로 |
| 핵심 기능 | [rolling update](/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/) | discovery/[load balancing](/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/) |

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 운영에서는 readiness와 liveness probe가 중요하다. 준비되지 않은 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 트래픽을 받지 않게 하고, 죽은 프로세스는 자동 재시작해야 한다.

- **📢 섹션 요약 비유**: Deployment는 공연 연출, Service는 관객 안내판, probe는 무대 뒤 건강검진이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 라벨 설계, 리소스 요청/제한, [롤링 업데이트](/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)/blue-green 배포, [HPA](/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) ([Horizontal Pod Autoscaler](/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/))를 함께 본다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Pod와 Service가 라벨로 정확히 연결되는가?
2. readiness/liveness probe가 구성되었는가?
3. [롤링 업데이트](/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/) 중 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단이 없는가?
4. 노출 방식이 내부/외부 요구에 맞는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 없이 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) IP를 직접 쓰는 경우
- readiness probe 없이 미완성 Pod를 받는 경우
- Deployment와 StatefulSet을 구분하지 않는 경우

기술사 관점에서는 배포와 접근을 분리해 설명해야 한다. [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 바뀌어도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 안정적이어야 하며, 그 안정성은 selector와 probe가 만든다.

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 배포는 주소록은 그대로 두고 안의 집 구조를 바꾸는 공사다.

---

## Ⅴ. 기대효과 및 결론

Service와 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 배포 구조를 이해하면 무중단 배포와 장애 복구를 안정적으로 설계할 수 있다. [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 운영의 가장 실용적인 기초다.

정리하면, [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 실제 일꾼이고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 그 일꾼을 찾아가는 문이다.

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 바뀌지 않는 현관문, [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 문 안에서 바뀌는 사람들이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) | 실행 단위 |
| [Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) | [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)/개수 관리 |
| [ReplicaSet](/studynote/13_cloud_architecture/02_iaas_paas_saas/086_replicaset_kubernetes_controller_self_healing/) | 유지 보장 |
| [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 접근 경로 |
| Probe | 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

### 📈 관련 키워드 및 발전 흐름도

```text
이미지 빌드
    |
    v
Pod 생성
    |
    v
Deployment / ReplicaSet
    |
    v
Service / DNS
    |
    v
Rolling Update / Autoscaling
```

이 흐름은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행에서 무중단 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 운영으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 바뀔 수 있는 작은 상점이고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 상점 전화번호예요.
2. 손님은 전화번호만 알면 안에 사람이 바뀌어도 계속 찾아갈 수 있어요.
3. 그래서 가게를 고쳐도 손님이 덜 불편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 52 / 371

<- **이전**: [52. 쿠버네티스 클러스터 아키텍처 (Kubernetes Cluster Architecture)](/studynote/13_cloud_architecture/01_virtualization/052_kubernetes_cluster_architecture/)
**다음**: [54. ConfigMap과 Secret](/studynote/13_cloud_architecture/01_virtualization/054_configmap_secret/) ->

---
