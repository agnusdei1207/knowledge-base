---
title: 53. 서비스와 파드 배포 (Service Pod Deployment)
date: '2026-05-01'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[085_pod_kubernetes_container_unit|파드]] ([[198_pod_kubernetes_minimum_deployment_unit|Pod]])는 배포의 최소 실행 단위이고, 배포 ([[087_deployment_kubernetes_workload_rolling_update|Deployment]])는 [[085_pod_kubernetes_container_unit|파드]]의 원하는 상태를 관리한다.
> 2. **가치**: [[090_service_kubernetes_network_load_balancing|서비스]] ([[090_service_kubernetes_network_load_balancing|Service]])는 바뀌는 [[085_pod_kubernetes_container_unit|파드]] IP를 숨기고 안정적인 접점을 제공한다.
> 3. **판단 포인트**: 라벨/셀렉터, readiness/liveness probe, [[117_rolling_update_deployment|롤링 업데이트]]가 안전한 배포의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[561_container_based_deployment|컨테이너]]를 그냥 띄우는 것만으로는 [[090_service_kubernetes_network_load_balancing|서비스]] 운영이 되지 않는다. [[085_pod_kubernetes_container_unit|파드]]가 바뀌어도 접점이 유지되어야 하고, 배포 중에도 사용자는 끊기지 않아야 한다.

그래서 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]에서는 [[085_pod_kubernetes_container_unit|파드]], [[090_service_kubernetes_network_load_balancing|서비스]], 배포를 함께 설계한다. [[085_pod_kubernetes_container_unit|파드]]는 실행, [[090_service_kubernetes_network_load_balancing|서비스]]는 접근, 배포는 변경을 담당한다.

- **📢 섹션 요약 비유**: [[090_service_kubernetes_network_load_balancing|서비스]]와 [[085_pod_kubernetes_container_unit|파드]] 배포는 가게 간판은 그대로 두고 안의 점원만 바꿔도 손님이 못 느끼게 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Deployment는 ReplicaSet을 통해 원하는 수의 Pod를 유지하고, Service는 label selector로 Pod를 묶어 안정적인 네트워크 엔드포인트를 제공한다.

```text
Deployment → ReplicaSet → Pod
Service ────────────────▶ Pod (via selector)
```

| 구성 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 실행 단위 | 일시적 |
| [[086_replicaset_kubernetes_controller_self_healing|ReplicaSet]] | 개수 유지 | self-healing |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | 배포 관리 | [[117_rolling_update_deployment|롤링 업데이트]] |
| [[090_service_kubernetes_network_load_balancing|Service]] | 안정적 접점 | 가상 IP / [[511_dns_hierarchical_distributed_architecture|DNS]] |

핵심은 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] IP가 바뀌어도 Service가 앞단에서 묶어 준다는 점이다. 그래서 클라이언트는 뒤의 변화를 몰라도 된다.

- **📢 섹션 요약 비유**: [[085_pod_kubernetes_container_unit|파드]]는 자주 바뀌는 직원이고, [[090_service_kubernetes_network_load_balancing|서비스]]는 손님이 기억하는 대표 전화번호다.

---

## Ⅲ. 비교 및 연결

Service는 ClusterIP, NodePort, LoadBalancer 등으로 노출 방식이 달라진다. Deployment는 [[239_stateless_redis|Stateless]] 앱에 적합하고, StatefulSet은 상태를 가진 워크로드에 적합하다.

| 항목 | [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | [[090_service_kubernetes_network_load_balancing|Service]] |
| :--- | :--- | :--- |
| 역할 | 배포 제어 | 통신 접점 |
| 변경 대상 | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수/[[288_version_ihl_tos_total_length|버전]] | 접근 경로 |
| 핵심 기능 | [[083_rolling_update_deployment_zero_downtime_version_inconsistency|rolling update]] | discovery/[[196_hard_soft_real_time|load balancing]] |

[[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 운영에서는 readiness와 liveness probe가 중요하다. 준비되지 않은 [[085_pod_kubernetes_container_unit|파드]]가 트래픽을 받지 않게 하고, 죽은 프로세스는 자동 재시작해야 한다.

- **📢 섹션 요약 비유**: Deployment는 공연 연출, Service는 관객 안내판, probe는 무대 뒤 건강검진이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 라벨 설계, 리소스 요청/제한, [[117_rolling_update_deployment|롤링 업데이트]] [[268_strategy_pattern|전략]], [[595_canary_stack_smashing_protector|canary]]/blue-green 배포, [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]])를 함께 본다.

### [[435_checklist_based_testing|체크리스트]]

1. Pod와 Service가 라벨로 정확히 연결되는가?
2. readiness/liveness probe가 구성되었는가?
3. [[117_rolling_update_deployment|롤링 업데이트]] 중 [[090_service_kubernetes_network_load_balancing|서비스]] 중단이 없는가?
4. 노출 방식이 내부/외부 요구에 맞는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[090_service_kubernetes_network_load_balancing|Service]] 없이 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] IP를 직접 쓰는 경우
- readiness probe 없이 미완성 Pod를 받는 경우
- Deployment와 StatefulSet을 구분하지 않는 경우

기술사 관점에서는 배포와 접근을 분리해 설명해야 한다. [[085_pod_kubernetes_container_unit|파드]]는 바뀌어도 [[090_service_kubernetes_network_load_balancing|서비스]]는 안정적이어야 하며, 그 안정성은 selector와 probe가 만든다.

- **📢 섹션 요약 비유**: [[090_service_kubernetes_network_load_balancing|서비스]]와 [[085_pod_kubernetes_container_unit|파드]] 배포는 주소록은 그대로 두고 안의 집 구조를 바꾸는 공사다.

---

## Ⅴ. 기대효과 및 결론

Service와 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 배포 구조를 이해하면 무중단 배포와 장애 복구를 안정적으로 설계할 수 있다. [[205_kubernetes_container_orchestration|Kubernetes]] 운영의 가장 실용적인 기초다.

정리하면, [[085_pod_kubernetes_container_unit|파드]]는 실제 일꾼이고 [[090_service_kubernetes_network_load_balancing|서비스]]는 그 일꾼을 찾아가는 문이다.

- **📢 섹션 요약 비유**: [[090_service_kubernetes_network_load_balancing|서비스]]는 바뀌지 않는 현관문, [[085_pod_kubernetes_container_unit|파드]]는 문 안에서 바뀌는 사람들이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 실행 단위 |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | [[288_version_ihl_tos_total_length|버전]]/개수 관리 |
| [[086_replicaset_kubernetes_controller_self_healing|ReplicaSet]] | 유지 보장 |
| [[090_service_kubernetes_network_load_balancing|Service]] | 접근 경로 |
| Probe | 상태 [[396_validation|확인]] |

### 📈 관련 키워드 및 발전 흐름도

```text
이미지 빌드
    │
    ▼
Pod 생성
    │
    ▼
Deployment / ReplicaSet
    │
    ▼
Service / DNS
    │
    ▼
Rolling Update / Autoscaling
```

이 흐름은 [[561_container_based_deployment|컨테이너]] 실행에서 무중단 [[090_service_kubernetes_network_load_balancing|서비스]] 운영으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[085_pod_kubernetes_container_unit|파드]]는 바뀔 수 있는 작은 상점이고, [[090_service_kubernetes_network_load_balancing|서비스]]는 상점 전화번호예요.
2. 손님은 전화번호만 알면 안에 사람이 바뀌어도 계속 찾아갈 수 있어요.
3. 그래서 가게를 고쳐도 손님이 덜 불편해요.
