---
title: 396. VRRP (Virtual Router Redundancy Protocol)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VRRP는 [[339_routing_overview_best_path_selection|라우팅]]과 경로 제어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: VRRP를 이해하면 수렴 속도과 확장성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [[454_spof|단일 장애점]]([[454_spof|SPOF]])인 기본 게이트웨이의 가용성을 높이기 위해, 여러 대의 라우터를 논리적인 하나의 가상 라우터로 묶어 동작하게 하는 [[635_ietf_core_working_group_coap|IETF]] 표준 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (RFC 3768, IPv6용은 5798). [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] `224.0.0.18` ([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 112)을 사용한다.
- **필요성**: 회사 네트워크를 이중화하려고 라우터를 두 대 샀다. 한 대는 시스코([[539_netflow_sflow_traffic_monitoring|Cisco]]), 한 대는 주니퍼(Juniper) 장비다. HSRP를 켜려고 하니 주니퍼 장비가 "난 [[395_hsrp_fhrp_router_redundancy|HSRP]] 뭔지 모르는데?"라며 파업을 선언했다. **"아놔, 기계 제조사가 달라도 공통으로 알아먹고 이중화를 구성할 수 있는 범용 언어(표현 규약)가 필요하네!"**라는 시장의 절실한 요구가 VRRP를 업계 1짱으로 만들었다.

- **💡 비유**: 
  - **[[395_hsrp_fhrp_router_redundancy|HSRP]]**: 삼성전자 직원들끼리만 사용하는 **"사내 전용 결재 시스템"**입니다. 외부 협력사는 접속도 못 하고 결재도 올릴 수 없습니다.
  - **VRRP**: 구글 닥스나 PDF처럼 전 세계 누구나 읽고 편집할 수 있는 **"국제 표준 결재 양식"**입니다. 삼성 직원이 올린 문서를 LG 직원이 승인([[555_backup_and_restore_strategy|Backup]] 승계)할 수 있는 완벽한 호환성을 자랑합니다.

```text
[HSRP]
    │
    ▼
[VRRP]
    │
    └──▶ [GLBP]
```

- **📢 섹션 요약 비유**: ** VRRP는 스마트폰의 **"USB-C 타입 충전 [[446_port_and_bus|포트]]"**와 같습니다. 옛날엔 애플 폰, 삼성 폰마다 충전기([[395_hsrp_fhrp_router_redundancy|HSRP]], NSRP)가 다 달라서 낭비가 심했지만, 지금은 [[259_adapter_pattern_interface_wrapper|어댑터]] 하나(VRRP)로 모든 회사의 장비가 권력(Master)을 공유하며 안정적으로 배터리를 채웁니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

작동 원리는 HSRP와 99% 똑같다. 차이점 위주로 실무/시험 포인트만 짚는다.

### 1. 용어의 차이 (Master vs [[555_backup_and_restore_strategy|Backup]])
- **Master 라우터**: 가상 IP(Virtual IP)의 권력을 쥐고 PC들이 보내는 모든 패킷을 처리하는 진짜 일꾼. (HSRP의 [[483_active_vs_passive_ftp|Active]]).
- **[[555_backup_and_restore_strategy|Backup]] 라우터**: Master가 1초마다 보내는 Hello 패킷을 엿들으며 숨죽이고 대기하다가, 3초(Master Down Interval) 동안 소식이 없으면 "대장 죽었다!"라고 선언하고 자신이 Master로 승격하는 대기조. (HSRP의 Standby).

### 2. 가상 [[673_mac_message_authentication_code|MAC]] 주소 규격
Master가 죽고 Backup이 올라왔을 때, [[238_switch_operation_principles|스위치]]([[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 테이블)를 속이기 위해 G-ARP를 쏘며 덮어쓰는 그 가짜 [[673_mac_message_authentication_code|MAC]] 주소의 규격이다.
- [[395_hsrp_fhrp_router_redundancy|HSRP]]: `0000.0c07.acXX`
- **VRRP**: **`0000.5e00.01XX`** (마지막 XX는 01부터 FF까지의 그룹 번호다). 
- 와이어샤크(Wireshark)에서 패킷을 떴을 때 저 [[673_mac_message_authentication_code|MAC]] 주소가 보이면 1초 만에 "아, 이 망은 VRRP 돌고 있네!"라고 알 수 있어야 한다.

### 3. 진짜 IP를 가상 IP로 쓰는 마법 (Owner)
VRRP만의 독특한 기능이다.
- A 라우터(물리 IP `10.1.1.254`), B 라우터(물리 IP `10.1.1.253`).
- HSRP는 무조건 제3의 가상 IP(`10.1.1.1`)를 파야 해서 동네 IP가 총 3개 소모된다.
- VRRP는 **"A 라우터의 진짜 물리 IP인 `10.1.1.254` 자체를 이 그룹의 가상 IP로 쓰자!"**라고 설정할 수 있다.
- 이렇게 자기 물리 IP를 가상 IP로 제공한 놈을 **'IP Address Owner(주인)'**라고 부르며, 주인은 선거 점수(Priority)가 강제로 **최고점인 255점**으로 픽스되어 무조건 영원한 Master로 군림하게 된다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                HSRP vs VRRP 실무 비교표 (핵심 요약)               │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   [ 항목 ]              [ HSRP (Cisco) ]    [ VRRP (표준) ]    │
 │   --------------------------------------------------------- │
 │   소속 (벤더)            시스코 독점          IEEE 개방형 표준     │
 │   역할 명칭              Active / Standby   Master / Backup   │
 │   멀티캐스트 주소        224.0.0.2          224.0.0.18        │
 │   Hello 주기            3초 (Hold 10초)     1초 (Hold 3초)     │
 │   가상 MAC 주소         0000.0c07.acXX     0000.5e00.01XX    │
 │   가상 IP = 물리 IP     불가 (무조건 딴 거)    가능 (Owner 개념)   │
 │   Preempt (권력찬탈)     기본 OFF (수동 켬)    기본 ON (자동 뺏음)  │
 └─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: ** VRRP는 HSRP라는 명작 영화의 **"글로벌 리메이크 [[288_version_ihl_tos_total_length|버전]]"**입니다. 스토리 라인과 연출 기법(동작 원리)은 소름 돋게 똑같지만, 주연 배우의 이름(Master)을 세계적으로 친숙한 이름으로 바꾸고 넷플릭스(오픈 표준)를 통해 전 세계 어느 나라(벤더)에서든 제약 없이 틀어볼 수 있게 만들었습니다.

---

## Ⅲ. 비교 및 연결

VRRP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. HSRP가 기반 조건을 만든다면, VRRP는 그 위에서 핵심 메커니즘을 구현하고, GLBP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 수렴 속도과 확장성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | HSRP의 기반 정리 | VRRP의 핵심 동작 | GLBP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 수렴 속도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: VRRP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 VRRP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [[395_hsrp_fhrp_router_redundancy|HSRP]] 수준의 기본 대책으로 충분한지, 아니면 VRRP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 GLBP와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 현재 문제의 핵심이 수렴 속도 부족인지, 확장성 악화인지 먼저 분리한다.
2. VRRP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [[396_validation|확인]]한다.
3. 도입 후에는 인접 기술인 GLBP와의 연계 방식을 함께 검증한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- VRRP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- HSRP와의 경계를 정리하지 않아 중복 투자나 [[164_policy|정책]] 충돌을 만드는 설계

- **📢 섹션 요약 비유**: VRRP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

VRRP는 [[339_routing_overview_best_path_selection|라우팅]]과 경로 제어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 수렴 속도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[397_glbp_gateway_load_balancing_protocol|GLBP]], 의도 기반 [[339_routing_overview_best_path_selection|라우팅]], 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 의도 기반 [[339_routing_overview_best_path_selection|라우팅]] 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: VRRP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[395_hsrp_fhrp_router_redundancy|HSRP]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[339_routing_overview_best_path_selection|라우팅]] 테이블 ([[339_routing_overview_best_path_selection|Routing]] Table) | 패킷 전달 의사결정의 기준이 된다. |
| [[342_routing_metric_hop_bandwidth_delay|메트릭]] ([[342_routing_metric_hop_bandwidth_delay|Metric]]) | 최적 경로를 선택하는 비교 척도다. |
| [[397_glbp_gateway_load_balancing_protocol|GLBP]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: HSRP]
    │
    ▼
[현재 개념: VRRP]
    │
    ├──▶ [확장 A: GLBP]
    └──▶ [확장 B: 의도 기반 라우팅]
```

VRRP는 HSRP에서 출발해 현재 메커니즘을 정교화하고, 이후 GLBP와 의도 기반 [[339_routing_overview_best_path_selection|라우팅]] 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 갈림길이 있는 미로에서 가장 좋은 길을 고르는 게임과 같아요.
2. 이 개념은 길이 막히면 다른 길로 빨리 바꾸는 규칙도 알려줘요.
3. 그래서 인터넷 길찾기가 덜 헤매고 더 똑똑해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 517 / 1120

← **이전**: [[395_hsrp_fhrp_router_redundancy|395. HSRP (Hot Standby Router Protocol)]]
**다음**: [[397_glbp_gateway_load_balancing_protocol|397. GLBP (Gateway Load Balancing Protocol)]] →

---
