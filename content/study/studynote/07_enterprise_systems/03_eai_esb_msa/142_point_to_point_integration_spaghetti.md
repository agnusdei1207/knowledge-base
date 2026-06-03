---
title: 142. P2P 통합 (Point-to-Point) - 스파게티 통합의 문제
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 통합은 **시스템 간 1:1로 직접 연결(인터페이스)**하는 가장 단순한 통합 방식이며, N개 시스템이면 **최대 N(N-1)/2개 인터페이스**가 필요하다.
> 2. **가치**: 2~3개 시스템이면 P2P가 빠르고 간단하지만, 10개 이상이면 **45개+ 인터페이스 → 스파게티 아키텍처**가 되어 변경·장애 전파·유지보수가 극도로 어려워진다.
> 3. **판단 포인트**: P2P의 한계가 **[[152_hub_dummy_switching_intelligent|Hub]]-and-Spoke·[[146_esb_enterprise_service_bus_architecture|ESB]]·[[538_event_driven_architecture_eda|이벤트 기반 아키텍처]]**의 등장 배경이며, 시스템 수가 5개 이상이면 중앙 통합을 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
P2P: A↔B, A↔C, B↔C, A↔D, B↔D, C↔D
  4개 시스템 → 6개 연결 (N(N-1)/2)
  10개 시스템 → 45개 연결 → 스파게티!
  문제: 변경 전파, 장애 추적 어려움
```

- **📢 섹션 요약 비유**: P2P는 **모든 사람이 서로 직접 전화**하는 것이다. 사람이 많아지면 전화선(연결)이 엉킨다.

---

## Ⅱ~Ⅴ. 결론

P2P는 **소규모에서만 유효**하며, 시스템 증가 시 [[152_hub_dummy_switching_intelligent|Hub]]·[[146_esb_enterprise_service_bus_architecture|ESB]]·이벤트 기반으로 전환해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]]** | 1:1 직접 연결 |
| **스파게티** | N(N-1)/2 복잡도 |
| **[[152_hub_dummy_switching_intelligent|Hub]]** | 중앙 집중 대안 |
| **[[146_esb_enterprise_service_bus_architecture|ESB]]** | 표준 [[344_bus|버스]] 대안 |
| **변경 전파** | P2P의 핵심 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
[P2P 직접 연결 (1990s)] → [스파게티 인식 (2000s)]
    → [Hub-and-Spoke (2002~)] → [ESB (2005~)]
    → [현재: 이벤트 기반 (Kafka) — 느슨 결합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. P2P는 **모든 친구와 직접 전화**하는 거예요. 친구가 적으면 괜찮아요.
2. 하지만 친구가 **10명이면 45개 전화선**이 필요해요! 엉켜요!
3. 그래서 **전화 교환대([[152_hub_dummy_switching_intelligent|Hub]]/[[146_esb_enterprise_service_bus_architecture|ESB]])**를 만들어 정리하는 거예요!
