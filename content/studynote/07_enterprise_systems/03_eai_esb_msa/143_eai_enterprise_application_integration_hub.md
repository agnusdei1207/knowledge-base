---
title: 143. EAI (Enterprise Application Integration) - Hub-and-Spoke
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EAI [[152_hub_dummy_switching_intelligent|Hub]]-and-Spoke는 **중앙 Hub가 모든 애플리케이션 간 [[389_mesh_topology|메시]]지 [[339_routing_overview_best_path_selection|라우팅]]·변환·[[073_container_orchestration_tools|오케스트레이션]]**을 수행하여 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 스파게티를 해소하는 통합 아키텍처이다.
> 2. **가치**: N개 시스템이 Hub에만 연결하면 **N개 인터페이스**만 필요(P2P는 N(N-1)/2)하며, [[389_mesh_topology|메시]]지 포맷 변환·[[339_routing_overview_best_path_selection|라우팅]] 규칙을 Hub에서 중앙 관리한다.
> 3. **판단 포인트**: Hub가 **[[454_spof|단일 장애점]]([[454_spof|SPOF]])·[[282_performance_tactics|성능]] 병목**이 될 수 있으며, 이를 해결하기 위해 [[146_esb_enterprise_service_bus_architecture|ESB]]([[136_variance|분산]] [[344_bus|버스]])로 진화했다.

---

## Ⅰ. 개요 및 필요성

```text
Hub-and-Spoke:
  시스템 A → Hub → 시스템 B
  시스템 C → Hub → 시스템 D
  Hub: 메시지 변환 + 라우팅 + 로깅
  → N개 시스템 = N개 연결 (vs P2P의 N(N-1)/2)
```

- **📢 섹션 요약 비유**: Hub는 **[[152_hub_dummy_switching_intelligent|허브]] 공항**이다. 모든 비행기(시스템)가 [[152_hub_dummy_switching_intelligent|허브]]를 경유하여 목적지로 간다.

---

## Ⅱ~Ⅴ. 결론

[[152_hub_dummy_switching_intelligent|Hub]]-and-Spoke는 **[[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 스파게티의 해결책**이지만, [[454_spof|SPOF]] 문제로 [[146_esb_enterprise_service_bus_architecture|ESB]]·이벤트 기반으로 진화했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[152_hub_dummy_switching_intelligent|Hub]]-and-Spoke** | 중앙 통합 |
| **[[152_hub_dummy_switching_intelligent|Hub]]** | [[339_routing_overview_best_path_selection|라우팅]]·변환 |
| **[[454_spof|SPOF]]** | [[454_spof|단일 장애점]] |
| **[[146_esb_enterprise_service_bus_architecture|ESB]]** | [[136_variance|분산]] [[344_bus|버스]] (진화) |
| **EAI** | 애플리케이션 통합 |

### 📈 관련 키워드 및 발전 흐름도

```text
[P2P (스파게티)] → [Hub-and-Spoke (2000s)]
    → [ESB (2005~, SPOF 해소)]
    → [iPaaS (클라우드, 2015~)]
    → [현재: 이벤트 기반 통합 (Kafka)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Hub는 **[[152_hub_dummy_switching_intelligent|허브]] 공항**이에요. 모든 비행기가 **[[152_hub_dummy_switching_intelligent|허브]]를 거쳐** 목적지로 가요.
2. 직항([[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]])보다 **[[152_hub_dummy_switching_intelligent|허브]] 경유**가 노선(연결)이 적어요.
3. 하지만 [[152_hub_dummy_switching_intelligent|허브]]가 **고장나면 전체가 멈추는** 문제([[454_spof|SPOF]])가 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 482

← **이전**: [[142_point_to_point_integration_spaghetti|142. P2P 통합 (Point-to-Point) - 스파게티 통합의 문제]]
**다음**: [[144_hub_and_spoke_architecture_eai|144. Hub-and-Spoke 아키텍처 심화 - EAI 중앙 통합]] →

---
