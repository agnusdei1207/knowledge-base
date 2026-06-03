---
title: 75. K8s 클러스터 아키텍처 - 1개 이상의 컨트롤 플레인(마스터 노드)과 여러 개의 데이터 플레인(워커 노드)으로 구성
date: '2026-04-07'
tags:
- studynote-cloud
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[205_kubernetes_container_orchestration|Kubernetes]] (K8s) 클러스터는 원하는 상태를 선언하고, Control Plane이 그 상태를 계산하며, [[001_dikw_pyramid|Data]] Plane이 실제 Pod를 실행하는 [[136_variance|분산]] 제어 시스템이다.
> 2. **가치**: 노드가 죽어도 전체 [[090_service_kubernetes_network_load_balancing|서비스]]가 멈추지 않도록, 상태 저장과 작업 실행을 분리해 자가 치유와 수평 확장을 동시에 얻는다.
> 3. **판단 포인트**: 작은 팀일수록 직접 운영보다 관리형 K8s를 먼저 검토하고, 큰 팀일수록 [[078_etcd_distributed_key_value_store|etcd]] [[555_backup_and_restore_strategy|백업]]·리소스 한도·프로브를 엄격히 봐야 한다.

---

## Ⅰ. 개요 및 필요성

K8s는 서버 한 대의 [[009_config|설정]] 도구가 아니라, 여러 서버를 하나의 운영 단위로 묶는 클러스터 오케스트레이터다. 사용자는 "무엇을 실행할지"만 선언하고, 시스템은 "어디서, 몇 개를, 어떤 상태로" 실행할지 계산한다.

이 분리가 필요한 이유는 규모와 장애 때문이다. 워커 노드가 늘수록 수동 배치는 불가능해지고, 노드가 한 번 죽을 때마다 사람이 [[658_ir_recovery|복구]]하면 [[090_service_kubernetes_network_load_balancing|서비스]] 복원 시간이 너무 길어진다. 그래서 K8s는 의도를 저장하는 Control Plane과 실제 일을 하는 [[001_dikw_pyramid|Data]] Plane을 분리했다.

```text
┌────────────────────┐      ┌──────────────────┐
│ kubectl / Manifest │ ---> │ API Server       │
└────────────────────┘      └─────────┬────────┘
                                        │
                                        v
                                 ┌────────────┐
                                 │ etcd       │
                                 └────┬───────┘
                                      v
                      ┌───────────────┐   ┌───────────────┐
                      │ Scheduler     │   │ Controller    │
                      └──────┬────────┘   └──────┬────────┘
                             v                   v
                            ┌────────────────────────────┐
                            │ Worker Node / kubelet / Pod │
                            └────────────────────────────┘
```

핵심은 K8s가 실행기이면서도 상태 재조정 루프라는 점이다.

- **📢 섹션 요약 비유**: 지휘자와 연주자를 나눠야 대규모 합주가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Control Plane은 선언을 받아 판단하고, [[001_dikw_pyramid|Data]] Plane은 컨테이너를 실제로 돌린다. [[014_api_posix|API]] Server는 유일한 관문이고, etcd는 클러스터의 기억이며, Scheduler는 배치 결정을 내리고, Controller Manager는 계속 상태를 맞춘다.

| [[603_component_independent_deployment_unit|컴포넌트]] | 역할 | 실패 시 영향 |
| :--- | :--- | :--- |
| [[014_api_posix|API]] Server | 요청 수신과 [[395_verification_process_review|검증]] | 모든 제어가 멈춤 |
| [[078_etcd_distributed_key_value_store|etcd]] | 원하는 상태 저장 | 클러스터 기억 상실 |
| Scheduler | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 배치 | 새 작업 배치 실패 |
| Controller | 상태 재조정 | [[658_ir_recovery|복구]] 자동화 저하 |
| [[082_kubelet_node_agent|kubelet]] | 노드에서 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 실행 | 워커 노드 기능 상실 |
| kube-proxy / [[822_cni_container_network_interface_kubernetes|CNI]] | 네트워크 연결 | [[090_service_kubernetes_network_load_balancing|서비스]] 통신 장애 |

이 구조 덕분에 Pod는 한 번 배치되고 끝나는 것이 아니라, 계속 관찰·재배치·복원된다. 결국 K8s의 본질은 "실행"보다 "일치시킴"에 있다.

- **📢 섹션 요약 비유**: 약속을 기억하고 다시 맞춰 주는 공장이다.

---

## Ⅲ. 비교 및 연결

가장 중요한 경계는 Control Plane과 Worker Node다. 전자는 판단과 기록을 맡고, 후자는 실행과 보고를 맡는다. 이 둘이 섞이면 장애 범위가 커지고 운영 복잡도도 급격히 오른다.

| 비교 축 | Control Plane | Worker Node |
| :--- | :--- | :--- |
| 책임 | 상태 결정 | 워크로드 실행 |
| 장애 영향 | 클러스터 전반 | 특정 [[090_service_kubernetes_network_load_balancing|서비스]] |
| 관리 포인트 | [[078_etcd_distributed_key_value_store|etcd]], HA, [[303_authentication_authorization_patterns|인증]] | 자원, 네트워크, 디스크 |

연결 관점에서는 Deployment가 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 복제를, Service가 내부 접근을, Ingress가 외부 진입을 담당한다. 즉 아키텍처는 "배치-노출-[[658_ir_recovery|복구]]"의 층으로 나뉜다.

- **📢 섹션 요약 비유**: 명령 내리는 방과 일하는 방은 분리돼야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 관리형 K8s를 쓸지 직접 운영할지부터 판단한다. 팀이 작거나 [[100_sre_site_reliability_engineering_error_budget|SRE]] 역량이 약하면 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]가 낫고, 노드와 네트워크를 세밀하게 통제해야 할 때만 자체 운영을 선택하는 편이 안전하다.

체크 포인트는 다음과 같다.
- Control Plane이 고가용성인지.
- [[078_etcd_distributed_key_value_store|etcd]] [[555_backup_and_restore_strategy|백업]]과 [[658_ir_recovery|복구]] 절차가 있는지.
- requests/limits, readiness/liveness probe, PodDisruptionBudget이 정의됐는지.
- 상태 저장 워크로드에 영속 스토리지가 붙어 있는지.

안티패턴은 단일 마스터, 무제한 배치, 수동 재기동이다. 이런 방식은 테스트 환경에서는 버티지만 운영 환경에서는 장애를 키운다.

- **📢 섹션 요약 비유**: 한 대가 아니라 상태를 운영해야 한다.

---

## Ⅴ. 기대효과 및 결론

K8s는 서버 묶음을 하나의 컴퓨터처럼 보이게 하되, 실제로는 상태를 계속 맞추는 제어 루프다. 그래서 운영이 잘 되면 배포가 빨라지고, 장애 [[658_ir_recovery|복구]]가 자동화되며, 확장도 규칙적으로 이뤄진다.

앞으로 중요한 것은 단순한 노드 수가 아니라 정책의 품질이다. 원하는 상태를 얼마나 정확히 선언했는지, 그리고 그 상태를 얼마나 빨리 회복시키는지가 클러스터 품질을 결정한다.

- **📢 섹션 요약 비유**: 큰 합주는 악보와 지휘가 동시에 좋아야 한다.

---

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 배포의 최소 실행 단위 |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | 복제와 [[117_rolling_update_deployment|롤링 업데이트]] |
| [[090_service_kubernetes_network_load_balancing|Service]] | 내부 접근과 로드 [[136_variance|분산]] |
| [[094_ingress_kubernetes_l7_routing_gateway|Ingress]] | 외부 트래픽 진입점 |
| [[078_etcd_distributed_key_value_store|etcd]] | 원하는 상태의 저장소 |
| [[082_kubelet_node_agent|kubelet]] | 노드 실행 에이전트 |
| [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]]) | 수평 확장 자동화 |

### 관련 키워드 및 발전 흐름도

```text
Desired State
    │
    ▼
API Server
    │
    ▼
etcd
    │
    ▼
Scheduler / Controller
    │
    ▼
kubelet
    │
    ▼
Container Runtime
    │
    ▼
Pod
    │
    └──────────────► Status back to Control Plane
```

### 어린이를 위한 3줄 비유 설명

1. 선생님이 "몇 명이 어디서 놀지" 적어 두면 교실이 정리돼요.
2. 아이들이 아파도 선생님은 다른 아이를 다시 배치해요.
3. 그래서 모두가 같은 규칙으로 움직일 수 있어요.
