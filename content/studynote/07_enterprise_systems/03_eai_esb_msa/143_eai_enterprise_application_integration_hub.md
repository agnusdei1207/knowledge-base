---
title: "143. EAI (Enterprise Application Integration) - Hub-and-Spoke"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EAI [Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)-and-Spoke는 <strong>중앙 Hub가 모든 애플리케이션 간 <a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>지 <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a>·변환·<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a></strong>을 수행하여 [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 스파게티를 해소하는 통합 아키텍처이다.
> 2. **가치**: N개 시스템이 Hub에만 연결하면 <strong>N개 인터페이스</strong>만 필요(P2P는 N(N-1)/2)하며, [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 포맷 변환·[라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 규칙을 Hub에서 중앙 관리한다.
> 3. **판단 포인트**: Hub가 <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">단일 장애점</a>(<a href="/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a>)·<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 병목</strong>이 될 수 있으며, 이를 해결하기 위해 [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))로 진화했다.

---

## Ⅰ. 개요 및 필요성

```text
Hub-and-Spoke:
  시스템 A -> Hub -> 시스템 B
  시스템 C -> Hub -> 시스템 D
  Hub: 메시지 변환 + 라우팅 + 로깅
  -> N개 시스템 = N개 연결 (vs P2P의 N(N-1)/2)
```

- **📢 섹션 요약 비유**: Hub는 <strong><a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">허브</a> 공항</strong>이다. 모든 비행기(시스템)가 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)를 경유하여 목적지로 간다.

---

## Ⅱ~Ⅴ. 결론

[Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)-and-Spoke는 <strong><a href="/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/">P2P</a> 스파게티의 해결책</strong>이지만, [SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 문제로 [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)·이벤트 기반으로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">Hub</a>-and-Spoke</strong> | 중앙 통합 |
| <strong><a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">Hub</a></strong> | [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·변환 |
| <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a></strong> | [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a></strong> | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) (진화) |
| **EAI** | 애플리케이션 통합 |

### 📈 관련 키워드 및 발전 흐름도

```text
[P2P (스파게티)] -> [Hub-and-Spoke (2000s)]
    -> [ESB (2005~, SPOF 해소)]
    -> [iPaaS (클라우드, 2015~)]
    -> [현재: 이벤트 기반 통합 (Kafka)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Hub는 <strong><a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">허브</a> 공항</strong>이에요. 모든 비행기가 <strong><a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">허브</a>를 거쳐</strong> 목적지로 가요.
2. 직항([P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/))보다 <strong><a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">허브</a> 경유</strong>가 노선(연결)이 적어요.
3. 하지만 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)가 **고장나면 전체가 멈추는** 문제([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))가 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 482

<- **이전**: [142. P2P 통합 (Point-to-Point) - 스파게티 통합의 문제](/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/)
**다음**: [144. Hub-and-Spoke 아키텍처 심화 - EAI 중앙 통합](/studynote/07_enterprise_systems/03_eai_esb_msa/144_hub_and_spoke_architecture_eai/) ->

---
