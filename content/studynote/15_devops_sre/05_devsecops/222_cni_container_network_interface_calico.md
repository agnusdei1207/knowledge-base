---
title: 222. CNI (Container Network Interface) 플러그인 (Calico, Flannel) 파드 간 오버레이 통신망
date: '2026-05-08'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[561_container_based_deployment|컨테이너]]와 [[085_pod_kubernetes_container_unit|파드]]에 네트워크 연결을 제공하는 플러그인 표준.
> 2. **가치**: 플랫폼과 네트워크 구현을 분리해 선택권을 높인다.
> 3. **판단 포인트**: [[164_policy|정책]] 기능, [[282_performance_tactics|성능]], [[615_ebpf|eBPF]] 지원 여부를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[[822_cni_container_network_interface_kubernetes|CNI]] ([[100_cni_container_network_interface_flannel_calico|Container Network Interface]]) 플러그인 ([[824_calico_bgp_routing_cni_network_policy|Calico]], [[823_flannel_overlay_cni_vxlan|Flannel]]) [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망은 [[652_devops_calms_culture|DevOps]]/[[100_sre_site_reliability_engineering_error_budget|SRE]] 환경에서 반복되는 운영 문제를 구조적으로 다루기 위해 등장한 개념이다. [[136_variance|분산]] 시스템의 확장성은 결국 연결성과 [[015_지연_데이터_관점|지연]] 품질에 의해 제한되므로, 네트워크 제어는 선택이 아니라 기반 역량이다. 핵심은 [[561_container_based_deployment|컨테이너]]와 [[085_pod_kubernetes_container_unit|파드]]에 네트워크 연결을 제공하는 플러그인 표준에 있다. 이 관점에서 보면, 이 주제는 단순 기술 소개가 아니라 속도와 안정성을 동시에 맞추기 위한 운영 설계 기준에 가깝다.

[[340_static_routing_default_route_0_0_0_0|정적 라우팅]]과 평면 네트워크는 [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]]와 엣지 환경에서 장애 반경과 보안 위험을 키운다. 따라서 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망을 이해할 때는 "무엇을 자동화하는가"보다 "어떤 실패와 편차를 줄이려는가"를 먼저 붙잡아야 한다.

```text
Deployment / Control / Feedback Flow

┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│ Addressing / Naming  │──▶│ Overlay / Routing    │──▶│ Policy / Security    │──▶│ Operations           │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

이 그림은 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망이 입력, 실행, [[395_verification_process_review|검증]], 환류를 한 흐름으로 묶는다는 점을 보여준다. 즉 기술 자체보다도 제어 루프와 피드백 구조가 본질이다.

- **📢 섹션 요약 비유**: 도로망 설계처럼 차선 분리와 [[130_signal|신호]] 체계가 있어야 도시가 막히지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망의 핵심 원리는 구성 요소를 나열하는 데 있지 않고, 목표 상태를 어떻게 해석하고 실제 상태에 어떻게 반영하며 그 결과를 어떻게 다시 측정하는지에 있다. 특히 런타임 종속 네트워크 구현와 달리 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망은 실행 전후의 차이와 [[164_policy|정책]]을 함께 본다는 점에서 운영 품질 차이를 만든다.

| 요소 | 역할 | 기술사 판단 포인트 |
|:---|:---|:---|
| Addressing / Naming | [[090_service_kubernetes_network_load_balancing|서비스]], 테넌트, 네트워크 경계를 [[655_ir_detection_analysis|식별]] | 동적 환경일수록 이름 기반 제어가 중요 |
| Overlay / [[339_routing_overview_best_path_selection|Routing]] | 경로 선택과 트래픽 캡슐화를 수행 | 확장성과 가시성의 균형이 필요 |
| [[164_policy|Policy]] / [[283_security_tactics|Security]] | 허용 경로, [[364_segmentation|세그멘테이션]], [[303_authentication_authorization_patterns|인증]]을 강제 | 네트워크는 보안과 [[282_performance_tactics|성능]]을 동시에 다룸 |
| Operations | [[229_monitor|모니터]]링, [[300_failover_architecture|failover]], capacity planning으로 운영 | 패킷 손실과 지터는 즉시 사용자 품질로 연결 |

```text
Reference Architecture

┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│ Addressing / Naming  │──▶│ Overlay / Routing    │──▶│ Policy / Security    │──▶│ Operations           │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

위 구조에서 중요한 것은 각 계층의 책임을 분리하면서도, 마지막에 반드시 [[395_verification_process_review|검증]] [[130_signal|신호]]가 다시 제어 계층으로 돌아오게 만드는 것이다. 그래야 변경 실패가 누적되지 않고, 재현성과 [[606_auditing_linux_auditd|감사]] 가능성을 함께 확보할 수 있다.

- **📢 섹션 요약 비유**: 지하철 환승 규칙처럼 경로와 권한을 정교하게 설계해야 혼잡과 사고를 줄인다.

---

## Ⅲ. 비교 및 연결

[[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망은 보통 런타임 종속 네트워크 구현와 비교할 때 경계가 선명해진다. [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망이 더 많은 자동화와 제어를 제공하더라도, 모든 상황에서 무조건 우월한 것은 아니다. 시스템 규모, 팀 성숙도, 규제 수준, 운영 복잡도가 함께 맞아야 장점이 실제 성과로 이어진다.

| 비교 축 | [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망 | 런타임 종속 네트워크 구현 |
|:---|:---|:---|
| 중심 목표 | [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망의 목적에 맞춘 제어와 자동화 | 더 전통적이거나 대안적인 운영 방식 |
| 강점 | 플랫폼과 네트워크 구현을 분리해 선택권을 높인다. | 구조가 단순하거나 도입 장벽이 낮음 |
| 위험 | [[198_abstraction_control_data_process|추상화]]와 [[164_policy|정책]]이 약하면 기대효과가 줄어듦 | 확장성·가시성·자동화 한계가 빨리 드러남 |
| 적합한 상황 | [[100_multi_region_deployment_pipeline_disaster_recovery|멀티 리전]], [[418_5g_embb_urllc_mmtc_slicing|5G]], 산업망, [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]]처럼 경로 제어가 핵심인 환경에서 특히 중요하다. | 변화가 적거나 단순한 환경 |

또한 이 주제는 [[824_calico_bgp_routing_cni_network_policy|Calico]], [[823_flannel_overlay_cni_vxlan|Flannel]], Overlay Network처럼 주변 개념과 강하게 연결된다. 기술사 관점에서는 개별 정의보다도 이런 연결 구조를 설명해야 답안의 깊이가 생긴다.

- **📢 섹션 요약 비유**: 우편 [[104_classification_analysis|분류]] 센터처럼 주소 체계가 있어야 패킷이 길을 잃지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망을 도입하는 것 자체보다, 어떤 전제조건이 갖춰졌을 때 효과가 나는지를 묻는 것이 더 중요하다. [[100_multi_region_deployment_pipeline_disaster_recovery|멀티 리전]], [[418_5g_embb_urllc_mmtc_slicing|5G]], 산업망, [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]]처럼 경로 제어가 핵심인 환경에서 특히 중요하다. 따라서 [[435_checklist_based_testing|체크리스트]]와 [[128_water_scrum_fall_anti_pattern|안티패턴]]을 함께 보는 습관이 필요하다.

### 적용 체크포인트

1. [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망의 목표 지표가 명확한가?
2. 자동화 실패 시 되돌릴 절차와 책임이 정의되어 있는가?
3. 관측 [[130_signal|신호]]와 운영 [[164_policy|정책]]이 실제 배포/운영 루프와 연결되어 있는가?

### 주의할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 도구만 도입하고 기준·지표·예외 절차를 정하지 않는 경우
- 운영 현실보다 이상적인 그림만 따르고 [[005_feedback_loop|피드백 루프]]를 닫지 못하는 경우

기술사 답안에서는 "도입"만 쓰지 말고, [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망이 어떤 상황에서는 채택되고 어떤 상황에서는 단계적으로 적용되어야 하는지를 비용, 복잡도, 보안, 운영 역량 기준으로 분리해 적는 것이 좋다.

- **📢 섹션 요약 비유**: 댐 수문처럼 흐름을 통제해야 홍수와 가뭄을 모두 피할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망을 잘 적용하면 격리, [[282_performance_tactics|성능]], 가시성, 공급자 독립성을 함께 높일 수 있다. 반면 [[198_abstraction_control_data_process|추상화]] 계층이 늘수록 디버깅 포인트와 운영 숙련도 요구도 커진다. 결국 핵심은 도구 이름을 외우는 것이 아니라, 제어 기준·상태 정합성·[[005_feedback_loop|피드백 루프]]를 하나의 설계 문제로 보는 것이다.

앞으로는 의도 기반 제어, 오버레이 [[015_virtualization|가상화]], 엣지 [[136_variance|분산]] 연결이 더 중요해진다. 따라서 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망은 "한 번 도입하는 기술"이 아니라, 변화가 잦은 시스템을 어떻게 안정적으로 운영할 것인지에 대한 사고 틀로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 국경 검문소처럼 지나갈 수 있는 경로와 조건을 명확히 정해야 안전과 효율이 함께 선다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[824_calico_bgp_routing_cni_network_policy|Calico]] | [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망을 이해할 때 직접 연결되는 기반 개념 |
| [[823_flannel_overlay_cni_vxlan|Flannel]] | [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망의 설계·운영 판단 기준을 보완하는 개념 |
| [[815_overlay_network_virtualization_l2_extension|Overlay Network]] | [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망을 자동화·확장 측면에서 연결하는 개념 |
| 고정형 네트워크 구성 | [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망 적용 후 후속 발전 방향을 설명하는 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Calico]
    │
    ▼
[CNI 플러그인 파드 간 오버레이 통신망]
    │
    ├──▶ [Flannel]
    ├──▶ [Overlay Network]
    └──▶ [고정형 네트워크 구성]
```

이 흐름도는 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망이 선행 개념 위에 서서 운영 자동화, 보안, 확장, 가시성 중 어떤 축으로 확장되는지를 [[347_compaction|압축]]해서 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인 [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망은 복잡한 일을 순서와 규칙으로 정리해서 실수하지 않게 도와주는 방법이에요.
2. [[824_calico_bgp_routing_cni_network_policy|Calico]] 같은 친구들과 같이 움직여야 더 잘 작동해요.
3. 그래서 문제가 생겨도 어디서 틀렸는지 빨리 찾고 다시 고치기 쉬워져요.
