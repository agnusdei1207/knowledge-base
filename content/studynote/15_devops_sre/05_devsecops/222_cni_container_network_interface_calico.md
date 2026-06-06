---
title: "222. Cni Container Network Interface Calico"
date: "2026-05-08"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 네트워크 연결을 제공하는 플러그인 표준.
> 2. **가치**: 플랫폼과 네트워크 구현을 분리해 선택권을 높인다.
> 3. **판단 포인트**: [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기능, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 지원 여부를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) ([Container Network Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/)) 플러그인 ([Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/), [Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/)) [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망은 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)/[SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 환경에서 반복되는 운영 문제를 구조적으로 다루기 위해 등장한 개념이다. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 확장성은 결국 연결성과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 품질에 의해 제한되므로, 네트워크 제어는 선택이 아니라 기반 역량이다. 핵심은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 네트워크 연결을 제공하는 플러그인 표준에 있다. 이 관점에서 보면, 이 주제는 단순 기술 소개가 아니라 속도와 안정성을 동시에 맞추기 위한 운영 설계 기준에 가깝다.

[정적 라우팅](/studynote/03_network/07_network_layer_routing/340_static_routing_default_route_0_0_0_0/)과 평면 네트워크는 [멀티 클라우드](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/)와 엣지 환경에서 장애 반경과 보안 위험을 키운다. 따라서 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망을 이해할 때는 "무엇을 자동화하는가"보다 "어떤 실패와 편차를 줄이려는가"를 먼저 붙잡아야 한다.

```text
Deployment / Control / Feedback Flow

+----------------------+   +----------------------+   +----------------------+   +----------------------+
| Addressing / Naming  |--->| Overlay / Routing    |--->| Policy / Security    |--->| Operations           |
+----------------------+   +----------------------+   +----------------------+   +----------------------+
```

이 그림은 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망이 입력, 실행, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 환류를 한 흐름으로 묶는다는 점을 보여준다. 즉 기술 자체보다도 제어 루프와 피드백 구조가 본질이다.

- **📢 섹션 요약 비유**: 도로망 설계처럼 차선 분리와 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 체계가 있어야 도시가 막히지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망의 핵심 원리는 구성 요소를 나열하는 데 있지 않고, 목표 상태를 어떻게 해석하고 실제 상태에 어떻게 반영하며 그 결과를 어떻게 다시 측정하는지에 있다. 특히 런타임 종속 네트워크 구현와 달리 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망은 실행 전후의 차이와 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 본다는 점에서 운영 품질 차이를 만든다.

| 요소 | 역할 | 기술사 판단 포인트 |
|:---|:---|:---|
| Addressing / Naming | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 테넌트, 네트워크 경계를 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 동적 환경일수록 이름 기반 제어가 중요 |
| Overlay / [Routing](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | 경로 선택과 트래픽 캡슐화를 수행 | 확장성과 가시성의 균형이 필요 |
| [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) / [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | 허용 경로, [세그멘테이션](/studynote/02_operating_system/06_memory_management/364_segmentation/), [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 강제 | 네트워크는 보안과 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 다룸 |
| Operations | [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링, [failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/), capacity planning으로 운영 | 패킷 손실과 지터는 즉시 사용자 품질로 연결 |

```text
Reference Architecture

+----------------------+   +----------------------+   +----------------------+   +----------------------+
| Addressing / Naming  |--->| Overlay / Routing    |--->| Policy / Security    |--->| Operations           |
+----------------------+   +----------------------+   +----------------------+   +----------------------+
```

위 구조에서 중요한 것은 각 계층의 책임을 분리하면서도, 마지막에 반드시 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 다시 제어 계층으로 돌아오게 만드는 것이다. 그래야 변경 실패가 누적되지 않고, 재현성과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능성을 함께 확보할 수 있다.

- **📢 섹션 요약 비유**: 지하철 환승 규칙처럼 경로와 권한을 정교하게 설계해야 혼잡과 사고를 줄인다.

---

## Ⅲ. 비교 및 연결

[CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망은 보통 런타임 종속 네트워크 구현와 비교할 때 경계가 선명해진다. [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망이 더 많은 자동화와 제어를 제공하더라도, 모든 상황에서 무조건 우월한 것은 아니다. 시스템 규모, 팀 성숙도, 규제 수준, 운영 복잡도가 함께 맞아야 장점이 실제 성과로 이어진다.

| 비교 축 | [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망 | 런타임 종속 네트워크 구현 |
|:---|:---|:---|
| 중심 목표 | [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망의 목적에 맞춘 제어와 자동화 | 더 전통적이거나 대안적인 운영 방식 |
| 강점 | 플랫폼과 네트워크 구현을 분리해 선택권을 높인다. | 구조가 단순하거나 도입 장벽이 낮음 |
| 위험 | [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 약하면 기대효과가 줄어듦 | 확장성·가시성·자동화 한계가 빨리 드러남 |
| 적합한 상황 | [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/), [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), 산업망, [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/)처럼 경로 제어가 핵심인 환경에서 특히 중요하다. | 변화가 적거나 단순한 환경 |

또한 이 주제는 [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/), [Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/), Overlay Network처럼 주변 개념과 강하게 연결된다. 기술사 관점에서는 개별 정의보다도 이런 연결 구조를 설명해야 답안의 깊이가 생긴다.

- **📢 섹션 요약 비유**: 우편 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 센터처럼 주소 체계가 있어야 패킷이 길을 잃지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망을 도입하는 것 자체보다, 어떤 전제조건이 갖춰졌을 때 효과가 나는지를 묻는 것이 더 중요하다. [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/), [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), 산업망, [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/)처럼 경로 제어가 핵심인 환경에서 특히 중요하다. 따라서 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)와 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)을 함께 보는 습관이 필요하다.

### 적용 체크포인트

1. [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망의 목표 지표가 명확한가?
2. 자동화 실패 시 되돌릴 절차와 책임이 정의되어 있는가?
3. 관측 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)와 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 실제 배포/운영 루프와 연결되어 있는가?

### 주의할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 도구만 도입하고 기준·지표·예외 절차를 정하지 않는 경우
- 운영 현실보다 이상적인 그림만 따르고 [피드백 루프](/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)를 닫지 못하는 경우

기술사 답안에서는 "도입"만 쓰지 말고, [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망이 어떤 상황에서는 채택되고 어떤 상황에서는 단계적으로 적용되어야 하는지를 비용, 복잡도, 보안, 운영 역량 기준으로 분리해 적는 것이 좋다.

- **📢 섹션 요약 비유**: 댐 수문처럼 흐름을 통제해야 홍수와 가뭄을 모두 피할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망을 잘 적용하면 격리, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 가시성, 공급자 독립성을 함께 높일 수 있다. 반면 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층이 늘수록 디버깅 포인트와 운영 숙련도 요구도 커진다. 결국 핵심은 도구 이름을 외우는 것이 아니라, 제어 기준·상태 정합성·[피드백 루프](/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)를 하나의 설계 문제로 보는 것이다.

앞으로는 의도 기반 제어, 오버레이 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/), 엣지 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 연결이 더 중요해진다. 따라서 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망은 "한 번 도입하는 기술"이 아니라, 변화가 잦은 시스템을 어떻게 안정적으로 운영할 것인지에 대한 사고 틀로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 국경 검문소처럼 지나갈 수 있는 경로와 조건을 명확히 정해야 안전과 효율이 함께 선다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/) | [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망을 이해할 때 직접 연결되는 기반 개념 |
| [Flannel](/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/) | [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망의 설계·운영 판단 기준을 보완하는 개념 |
| [Overlay Network](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/) | [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망을 자동화·확장 측면에서 연결하는 개념 |
| 고정형 네트워크 구성 | [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망 적용 후 후속 발전 방향을 설명하는 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Calico]
    |
    v
[CNI 플러그인 파드 간 오버레이 통신망]
    |
    +---> [Flannel]
    +---> [Overlay Network]
    +---> [고정형 네트워크 구성]
```

이 흐름도는 [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망이 선행 개념 위에 서서 운영 자동화, 보안, 확장, 가시성 중 어떤 축으로 확장되는지를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해서 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 오버레이 통신망은 복잡한 일을 순서와 규칙으로 정리해서 실수하지 않게 도와주는 방법이에요.
2. [Calico](/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/) 같은 친구들과 같이 움직여야 더 잘 작동해요.
3. 그래서 문제가 생겨도 어디서 틀렸는지 빨리 찾고 다시 고치기 쉬워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 222 / 373

<- **이전**: [221. K8s 서비스 퍼블리싱 (ClusterIP, NodePort, LoadBalancer, Ingress) 라우팅 패러다임](/studynote/15_devops_sre/05_devsecops/221_k8s_clusterip_nodeport_loadbalancer_ingress/)
**다음**: [223. CSI (Container Storage Interface) 퍼시스턴트 볼륨(PV/PVC) 동적 스토리지 할당](/studynote/15_devops_sre/05_devsecops/223_csi_container_storage_interface_pv/) ->

---
