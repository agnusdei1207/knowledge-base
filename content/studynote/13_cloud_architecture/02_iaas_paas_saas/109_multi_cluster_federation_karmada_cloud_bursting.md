+++
title = "109. K8s 멀티 클러스터 및 연합(Federation) - Karmada·클라우드 버스팅"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 멀티 클러스터 연합([Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/))은 전 세계에 분산된 **복수의 독립 K8s 클러스터를 단일 제어 평면(Control Plane)에서 통합 관리**하여 단일 클러스터의 확장성 한계(5,000 노드)와 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))을 제거하는 상위 아키텍처다.
> 2. **가치**: 서울 클러스터 장애 시 0.1초 만에 도쿄 클러스터로 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 자동 복제하는 **무결점 재해복구([DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/))**와, [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 포화 시 AWS로 트래픽을 넘기는 **클라우드 버스팅(Cloud Bursting)**을 실현한다.
> 3. **판단 포인트**: 실패작 Kubefed v1/v2를 넘어 **Karmada**가 기존 K8s YAML 100% 호환·동적 스케줄링으로 차세대 표준에 등극 중이다.

---

## Ⅰ. 개요 및 필요성

단일 K8s 클러스터는 공식 권고 최대 5,000 노드다. 이를 넘기면 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Server의 Watch/List 트래픽이 폭주하여 마스터가 과부하된다. 또한 1개 클러스터에 모든 워크로드를 집중하면 [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 장애·네트워크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 시 **폭발 반경(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/))**이 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 확대된다.

```text
┌───────────────────────────────────────────────────────┐
│     싱글 클러스터 vs 멀티 클러스터 연합 비교            │
├───────────────────────────────────────────────────────┤
│  [싱글 클러스터]           [멀티 클러스터 + Federation] │
│  ┌──────────┐             ┌──────────────────┐        │
│  │ Master 1 │             │ Federation CP    │        │
│  │ 5000노드 │             │ (중앙 사령부)     │        │
│  │ 전체서비스│             └──┬─────┬─────┬──┘        │
│  └──────────┘                │     │     │            │
│  장애 시 100% 마비          ▼     ▼     ▼            │
│                          서울500 도쿄500 AWS500       │
│                          장애 시 1/3만 영향           │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 5,000개 마을을 황제 1명이 다스리면 황제 과로사 시 제국 멸망. 10개 주로 쪼개고 영주를 세우면 서울 영주가 쓰러져도 부산·도쿄는 무사하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 구성 요소 | 역할 | 비유 |
|:---|:---|:---|
| **[Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) Control Plane** | 복수 클러스터를 통합 관리하는 상위 마스터 | 제국 황제 |
| **Member Cluster** | 독립 운영되는 개별 K8s 클러스터 | 각 주의 영주 |
| **Placement [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)** | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 어느 클러스터에 배치할지 결정 | 병력 배치 명령 |
| **Override [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)** | 클러스터별로 YAML을 [미세 조정](/knowledge-base/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/) | 지역 특화 명령서 |

### Karmada의 차별점
1. **기존 YAML 100% 호환**: [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) YAML을 1글자도 수정하지 않고 던지면, Karmada가 알아서 10개 클러스터에 CPU 잔여량 기반 동적 스케줄링.
2. **PropagationPolicy**: "서울 50%, 도쿄 30%, AWS 20%" 같은 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 기반 분배 선언.
3. **[Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)**: 클러스터 헬스체크 실패 시 자동으로 다른 클러스터에 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 재배치.

- **📢 섹션 요약 비유**: 본사 팩스([Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))에 레시피 1장만 넣으면 전국 10개 지점에 동시 전송되고, 부산 지점에는 "밀면 추가"로 자동 수정(Override)된다.

---

## Ⅲ. 비교 및 연결

| 비교 | Kubefed v2 | Karmada | Admiralty |
|:---|:---|:---|:---|
| **K8s [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호환** | 별도 CRD 필요 | **100% 호환** | Virtual [Kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) |
| **동적 스케줄링** | 제한적 | **CPU/메모리 기반** | 제한적 |
| **커뮤니티** | 중단됨 | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) Sandbox→Incubating | 소규모 |
| **[Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)** | 수동 | **자동** | 제한적 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 클라우드 버스팅 시나리오
[온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) K8s(100대)가 블랙프라이데이에 포화 → [Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) CP가 AWS EKS 예비 클러스터로 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 400개 즉시 확장 → 폭풍 후 AWS [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 종료하여 비용 절감.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 클러스터 간 [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)(Cross-Region [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 측정 및 Placement에 반영했는가?
2. 멀티 클러스터 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) Multi-Cluster) 또는 Submariner로 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 통신을 구성했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **무분별한 클러스터 분할**: 팀당 1개 클러스터를 만들어 100개 → 운영 오버헤드 폭발.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 싱글 클러스터 | 멀티+[Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) | 개선 |
|:---|:---|:---|:---|
| 최대 노드 수 | 5,000 | **무제한 (수만)** | 확장성 해소 |
| 폭발 반경 | 100% | **1/N** | [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 확보 |
| 클라우드 버스팅 | 불가 | **자동** | 비용 최적화 |
| 배포 복잡도 | 낮음 | 중간 (Karmada 자동화) | 학습 곡선 |

Karmada는 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) Incubating 프로젝트로 격상되었으며, OCM(Open Cluster [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))과 함께 멀티 클러스터 관리의 사실상 표준으로 수렴 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)** | 멀티 클러스터의 단위 구성 요소 |
| **Karmada** | 차세대 멀티 클러스터 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 엔진 |
| **Cloud Bursting** | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 포화 시 퍼블릭 클라우드로 확장하는 전술 |
| **[Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/))** | 클러스터 간 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 통신을 보장하는 네트워크 레이어 |
| **[DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))** | 멀티 클러스터의 핵심 가치, 재해복구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[싱글 K8s 클러스터 (2015~) — 5,000 노드 한계]
    │
    ▼
[Kubefed v1/v2 (2018~) — 실패, 복잡한 CRD 문법]
    │
    ▼
[Karmada (2021~) — K8s API 100% 호환, CNCF 프로젝트]
    │
    ▼
[현재: OCM + Karmada + 위성 Edge K3s — 전지구 멀티 클러스터]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 한 교실(클러스터)에 학생 5,000명을 넣으면 선생님(마스터)이 힘들어 쓰러져요.
2. 그래서 교실을 10개로 나누고, **교장 선생님([Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/))**이 10개 교실을 한 번에 관리해요!
3. 1반이 물난리가 나도 나머지 9개 반은 멀쩡하게 수업을 계속할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 108 / 371

← **이전**: [108. K8s 프로브(Probes) 생명주기 관리](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/108_kubernetes_probes_liveness_readiness_startup_health_check/)
**다음**: [110. OOM Killed (Out of Memory) - K8s 파드 메모리 초과 강제 종료와 QoS 생존 전략](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/) →

---
