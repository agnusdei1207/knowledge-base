---
title: 97. 클러스터 오토스케일러 (CA) - K8s 물리 노드 자동 스케일링
date: '2026-04-10'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[089_contract_account_smart_contract|CA]] (Cluster Autoscaler)는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])가 자원 부족으로 배정받지 못하는 `Pending` 상태를 감지하여 물리적 가상머신([[598_vm_migration_nic|VM]] 노드) 자체를 자동으로 [[528_provisioning|프로비저닝]]하는 인프라 확장 기술이다.
> 2. **가치**: 트래픽 폭증으로 [[085_pod_kubernetes_container_unit|파드]]가 급증할 때 클러스터 용량을 즉각 늘려 [[090_service_kubernetes_network_load_balancing|서비스]] 중단을 막고, 트래픽이 감소하면 유휴 노드를 회수하여 클라우드 비용을 최소화한다.
> 3. **판단 포인트**: CA는 CPU/메모리 사용률이 아닌 '스케줄링 불가 [[085_pod_kubernetes_container_unit|파드]]의 존재 여부'를 [[507_acid_properties|트리거]]로 동작하므로, [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]])와 함께 설계해야만 완벽한 [[571_resiliency_fault_tolerance_patterns|탄력성]](Elasticity)을 확보할 수 있다.

---

## Ⅰ. 개요 및 필요성

[[089_contract_account_smart_contract|CA]] (Cluster Autoscaler)는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]([[205_kubernetes_container_orchestration|Kubernetes]]) 환경에서 워커 노드(Worker Node)의 개수를 동적으로 조절하는 자동화 컨트롤러다. [[561_container_based_deployment|컨테이너]] 오케스트레이션에서 워크로드 증가에 따라 [[085_pod_kubernetes_container_unit|파드]]를 늘리더라도, 이 [[085_pod_kubernetes_container_unit|파드]]들이 실행될 물리적 공간(CPU/Memory)이 노드에 부족하면 더 이상 [[090_service_kubernetes_network_load_balancing|서비스]] 확장이 불가능해진다. 

과거에는 운영자가 수동으로 클라우드 인스턴스를 추가하고 클러스터에 편입시키는 [[141_latency|지연 시간]]이 발생했다. CA는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 스케줄러와 클라우드 공급자(AWS ASG, GCP MIG 등)의 [[014_api_posix|API]] 사이를 직접 연결하여, '방이 없어 대기 중인 [[085_pod_kubernetes_container_unit|파드]]'가 생기는 즉시 인프라 한계를 돌파하게 해준다.

- **📢 섹션 요약 비유**: 식당(클러스터)에 손님이 몰려 점장이 알바생([[085_pod_kubernetes_container_unit|파드]]) 10명을 대기실에 불렀는데, 주방(노드)이 좁아 들어갈 수 없을 때, CA는 즉시 옆 건물 주방을 월세로 빌려와 알바생을 밀어 넣는 대주주와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CA의 동작은 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]의 스케줄링 사이클과 클라우드 [[528_provisioning|프로비저닝]] 메커니즘의 결합으로 이루어진다. 핵심 [[507_acid_properties|트리거]]는 CPU 사용률이 아닌 'Pending 상태의 [[085_pod_kubernetes_container_unit|파드]]'다.

| 구성 요소 | 역할 | 동작 방식 |
| :--- | :--- | :--- |
| **[[079_kube_scheduler_pod_placement|Kube-Scheduler]]** | [[085_pod_kubernetes_container_unit|파드]] 배정 시도 | 리소스 부족 시 [[085_pod_kubernetes_container_unit|파드]]를 `Pending` 상태로 마킹 |
| **[[089_contract_account_smart_contract|CA]] 봇 (Controller)** | 상태 감지 및 판단 | 루프(약 10초)를 돌며 Pending [[085_pod_kubernetes_container_unit|파드]] [[396_validation|확인]] |
| **Cloud [[150_soa_triangle_architecture|Provider]] [[014_api_posix|API]]** | 물리 노드 조작 | AWS ASG([[030_auto_scaling|Auto Scaling]] Group) 등에 노드 추가/제거 명령 |

```text
┌──────────────────────────────────────────────────────────────┐
│           CA 스케일 아웃 흐름: 리소스 부족 감지와 확장       │
├──────────────────────────────────────────────────────────────┤
│ HPA 요청 ─▶ Pod 10개 생성 ─▶ Kube-Scheduler가 Node 용량 확인 │
│                                                              │
│ [용량 부족] ─▶ Pod 5개 'Pending' ─▶ CA가 Pending Pod 발견    │
│                                                              │
│ CA ─(API API 호출)─▶ 클라우드(AWS/GCP) ─▶ 새 Node 부팅 & 결합│
└──────────────────────────────────────────────────────────────┘
```

축소(Scale-in) 로직 역시 정교하다. CA는 특정 노드의 리소스 사용률이 [[431_ssthresh_slow_start_threshold|임계치]](기본 50%) 미만이고, 10분 이상 지속되면 해당 노드를 축소 대상으로 선정한다. 이때 노드에 있는 [[085_pod_kubernetes_container_unit|파드]]를 다른 곳으로 이주(Eviction)시킨 후 안전하게 클라우드 인스턴스를 반납한다.

- **📢 섹션 요약 비유**: 대주주([[089_contract_account_smart_contract|CA]])는 평소에는 자고 있다가, 주방 밖에서 유니폼을 입고 서성거리는 알바생(Pending)을 발견하는 순간에만 즉시 부동산(Cloud [[014_api_posix|API]])에 전화해 주방을 늘려달라고 요청한다.

---

## Ⅲ. 비교 및 연결

CA의 역할은 [[085_pod_kubernetes_container_unit|파드]] 레벨의 스케일러인 [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]]), [[096_vpa_vertical_pod_autoscaler_kubernetes|VPA]] ([[096_vpa_vertical_pod_autoscaler_kubernetes|Vertical Pod Autoscaler]])와 구분되며, 이들과 직교(Orthogonal)하여 결합될 때 완전한 [[249_scaling_normalization_standardization|스케일링]] 파이프라인이 완성된다.

| 항목 | [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]]) | [[089_contract_account_smart_contract|CA]] (Cluster Autoscaler) |
| :--- | :--- | :--- |
| **[[249_scaling_normalization_standardization|스케일링]] 대상** | [[085_pod_kubernetes_container_unit|파드]] ([[198_pod_kubernetes_minimum_deployment_unit|Pod]]) 레벨 | 워커 노드 (Node) 레벨 ([[598_vm_migration_nic|VM]]) |
| **[[507_acid_properties|트리거]] 조건** | CPU/Memory 사용률, 사용자 정의 [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 리소스 부족으로 인한 `Pending` [[085_pod_kubernetes_container_unit|파드]] 발생 |
| **[[528_provisioning|프로비저닝]] 속도** | 빠름 (초 단위, [[561_container_based_deployment|컨테이너]] 기동) | 느림 (분 단위, OS 부팅 및 클러스터 조인) |

HPA가 먼저 반응하여 [[085_pod_kubernetes_container_unit|파드]]를 늘리고, 이로 인해 노드 용량이 초과되면 비로소 CA가 작동하는 '2단계 연쇄 [[249_scaling_normalization_standardization|스케일링]]' 구조를 가진다. 만약 CA만 있고 HPA가 없다면 [[085_pod_kubernetes_container_unit|파드]]는 늘어나지 않으므로 노드도 절대 늘어나지 않는다.

- **📢 섹션 요약 비유**: HPA는 손님이 늘어나면 알바생([[085_pod_kubernetes_container_unit|파드]])을 더 뽑는 점장이고, CA는 알바생이 일할 주방 평수(노드)를 늘려주는 건물주다. 점장이 알바를 뽑지 않으면 건물주는 절대 주방을 늘려주지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

CA는 막강하지만 부팅 [[141_latency|지연 시간]](보통 1~3분)이 존재하므로, 즉각적인 [[129_spike_agile_technical_investigation|스파이크]] 트래픽에는 취약할 수 있다. 기술사는 비용 최적화와 응답성 사이의 트레이드오프를 관리해야 한다.

### [[435_checklist_based_testing|체크리스트]] 및 실무 판단
1. **오버프로비저닝 (Over-provisioning) 튜닝**: 빈 깡통 [[085_pod_kubernetes_container_unit|파드]](Pause [[198_pod_kubernetes_minimum_deployment_unit|Pod]])를 우선순위 낮게 띄워두고 미리 노드를 확보하는 기법을 사용하여 [[089_contract_account_smart_contract|CA]] 부팅 [[015_지연_데이터_관점|지연]](1~2분)을 상쇄할 수 있는가?
2. **ASG 가용영역 (AZ) 균형**: 여러 가용영역(Multi-AZ)에 노드 그룹을 구성하여 특정 영역의 [[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]]([[209_spot_instance_cloud_cost_optimization|Spot Instance]]) 반환 시 장애를 최소화하도록 설계했는가?
3. **충돌 방지**: 스케일 다운 과정에서 `PodDisruptionBudget` (PDB) [[009_config|설정]]이 빡빡하여 노드 축소가 블로킹되는 [[128_water_scrum_fall_anti_pattern|안티패턴]]을 피했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- HPA의 CPU [[621_scale_up_system_bus|스케일 업]] [[431_ssthresh_slow_start_threshold|임계치]]와 CA의 축소 [[431_ssthresh_slow_start_threshold|임계치]] 간 핑퐁(Ping-pong) 현상이 일어나는 [[009_config|설정]] (확장과 축소가 무한 반복).

- **📢 섹션 요약 비유**: 건물주([[089_contract_account_smart_contract|CA]])가 새 주방을 짓는 데는 시간이 걸리므로, 평소에 가짜 알바생(Pause [[198_pod_kubernetes_minimum_deployment_unit|Pod]])을 몇 명 세워두고 진짜 알바생이 올 때 자리를 비켜주게 하면 [[141_latency|지연 시간]]을 완벽히 숨길 수 있다.

---

## Ⅴ. 기대효과 및 결론

CA의 도입은 트래픽 폭증 시 무장애 확장을 보장하며, 유휴 시간대의 인프라 비용을 대폭 절감한다. 특히 [[007_public_cloud|퍼블릭 클라우드]] 환경에서는 [[571_resiliency_fault_tolerance_patterns|탄력성]](Elasticity)의 이점을 극대화하는 가장 강력한 무기다.

미래의 클러스터 확장은 카펜터(Karpenter)와 같이 노드 그룹 중심에서 [[085_pod_kubernetes_container_unit|파드]] 요구사항 기반의 직접 [[528_provisioning|프로비저닝]](Group-less Autoscaling) 방식으로 진화하고 있다. 결론적으로 CA는 자원 고갈을 감지하고 치유하는 '인프라 최후의 방어선'으로 설계되어야 한다.

- **📢 섹션 요약 비유**: CA는 식당이 가장 돈을 많이 벌 수 있는 피크 타임에 기회를 놓치지 않게 해주고, 파리가 날리는 시간에는 월세를 아껴 식당의 생존력을 높여주는 궁극의 재무 관리자다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]])** | [[085_pod_kubernetes_container_unit|파드]] 개수를 늘려 CA의 `Pending` [[507_acid_properties|트리거]]를 유발하는 선행 스케일러 |
| **[[096_vpa_vertical_pod_autoscaler_kubernetes|VPA]] ([[096_vpa_vertical_pod_autoscaler_kubernetes|Vertical Pod Autoscaler]])** | [[085_pod_kubernetes_container_unit|파드]]의 자원(CPU/RAM) 요구량을 조절하여 노드 배정을 변화시킴 |
| **Over-provisioning** | [[459_dummy_test_double|더미]] [[085_pod_kubernetes_container_unit|파드]](Pause [[198_pod_kubernetes_minimum_deployment_unit|Pod]])를 활용한 [[089_contract_account_smart_contract|CA]] 스케일업 [[141_latency|지연 시간]] 은닉 기법 |
| **Karpenter** | 노드 그룹 없이 [[085_pod_kubernetes_container_unit|파드]] 스펙에 맞춰 즉시 최적 노드를 띄우는 차세대 [[089_contract_account_smart_contract|CA]] |

### 📈 관련 키워드 및 발전 흐름도

```text
HPA (파드 수평 확장) · VPA (파드 수직 확장)
    │
    ▼
CA (Cluster Autoscaler) · Pending 감지 노드 확장
    │
    ▼
Node Auto-Provisioning · 스팟 인스턴스 혼합 최적화
    │
    ▼
Karpenter (차세대 그룹리스(Group-less) 노드 스케일러)
```

이 흐름도는 [[085_pod_kubernetes_container_unit|파드]] 수준의 [[249_scaling_normalization_standardization|스케일링]]에서 노드 수준으로 진화하고, 다시 노드 제약을 넘어서는 직접 [[528_provisioning|프로비저닝]]으로 발전하는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 인프라 확장의 궤적을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CA는 레고 마을에서 일꾼([[085_pod_kubernetes_container_unit|파드]])들이 쉴 방이 부족해 길거리를 헤맬 때 나타나는 마법사예요.
2. 길거리에 대기하는 일꾼을 한 명이라도 발견하면 즉시 마법을 부려 거대한 새 아파트(노드)를 지어주죠.
3. 반대로 아파트가 텅 비면 월세를 아끼기 위해 아파트를 지워버리는 똑똑한 일꾼 관리자랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 96 / 371

← **이전**: [[096_vpa_vertical_pod_autoscaler_kubernetes|96. VPA (Vertical Pod Autoscaler) - 파드 수직 자원 자동 조절]]
**다음**: [[098_kubernetes_storage_volume_pv_pvc|98. K8s 스토리지 관리 - 볼륨, PV, PVC (영구 스토리지)]] →

---
