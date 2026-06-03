---
title: 997. SDN 데이터/컨트롤 플레인
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기존 라우터 장비 내부에서 함께 동작하던 '길을 찾는 뇌(Control Plane)'와 '패킷을 나르는 손발([[001_dikw_pyramid|Data]] Plane)'을 물리적, 논리적으로 완벽히 분리하는 것이 [[633_sdn_whitebox|SDN]](Software-Defined Networking)의 핵심 구조다.
> 2. **가치**: 컨트롤 플레인을 중앙 집중형 소프트웨어 컨트롤러로 분리함으로써, 수백 대의 [[238_switch_operation_principles|스위치]]를 중앙에서 한 번에 프로그래밍하고 네트워크 트래픽 경로를 전역적인 관점(Global [[151_sql_view_virtual_table|View]])에서 최적화할 수 있다.
> 3. **판단 포인트**: [[633_sdn_whitebox|SDN]] 도입 시 [[001_dikw_pyramid|데이터]] 플레인([[859_whitebox_switch_open_hardware_nos|화이트박스 스위치]])은 단순 포워딩만 하므로 비용이 절감되나, 컨트롤 플레인([[633_sdn_whitebox|SDN]] 컨트롤러)이 다운되면 네트워크 전체가 마비되므로 컨트롤러의 [[136_variance|분산]] 클러스터링([[456_dual_redundancy|이중화]]) 구성이 필수적이다.

---

## Ⅰ. 개요 및 필요성

과거의 전통적인 네트워크 장비(라우터, [[238_switch_operation_principles|스위치]])는 경로를 계산하는 두뇌 역할(Control Plane)과 실제로 패킷을 목적지로 전달하는 역할([[001_dikw_pyramid|Data]] Plane)이 하나의 박스 안에 묶여 있는 수직 통합형(Vertical Integration) 구조였다. 장비마다 각자 [[339_routing_overview_best_path_selection|라우팅]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[357_ospf_open_shortest_path_first_overview|OSPF]], [[365_bgp_border_gateway_protocol_path_vector|BGP]] 등)을 돌리며 알아서 길을 찾아야 했기 때문에, 관리자가 네트워크 [[164_policy|정책]]을 바꾸려면 [[238_switch_operation_principles|스위치]]마다 일일이 접속하여 CLI([[271_command_pattern|Command]] Line Interface) 명령어를 쳐야 했다. 

이러한 방식은 수천 대의 서버가 시시각각 생성되고 삭제되는 클라우드 환경의 변화 속도를 따라갈 수 없었다. 네트워크를 소프트웨어처럼 빠르고 유연하게 다루기 위해(Programmability), 장비에서 두뇌(Control Plane)를 빼내어 중앙의 컨트롤러 서버로 모으고, 장비는 그저 지시받은 대로 패킷만 전달([[001_dikw_pyramid|Data]] Plane)하도록 역할을 분리한 것이 SDN의 시작이다.

```text
[NFV 기반 가상화 VNF]
    │
    ▼
[SDN 데이터/컨트롤 플레인]
    │
    └──▶ [OpenFlow 프로토콜]
```

- **📢 섹션 요약 비유**: 옛날엔 교차로마다 신호등이 스스로 교통량을 판단해서(각자 똑똑함) 신호를 바꿨다면, SDN은 중앙 통제실(Control Plane)에서 도시 전체의 CCTV를 보고 모든 교차로 신호등([[001_dikw_pyramid|Data]] Plane)을 한 번에 조종하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[633_sdn_whitebox|SDN]] 아키텍처는 3개의 계층(Layer)과 그 사이를 잇는 2개의 인터페이스([[014_api_posix|API]])로 구성된다. 이 중 [[001_dikw_pyramid|데이터]] 플레인과 컨트롤 플레인의 역할 분담이 핵심이다.

```text
┌─────────────────────────────────────────────────────────┐
│                 [ Application Plane ]                   │
│   (방화벽 앱, 로드밸런서 앱, 트래픽 엔지니어링 앱 등)   │
└───────────────────────┬─────────────────────────────────┘
                        │ Northbound API (REST API 등)
┌───────────────────────┴─────────────────────────────────┐
│                 [ Control Plane ]                       │
│    SDN Controller (ONOS, OpenDaylight 등)               │
│    - Global Network View 유지                           │
│    - Flow Table 계산 및 정책 하달                       │
└───────────────────────┬─────────────────────────────────┘
                        │ Southbound API (OpenFlow 등)
┌───────────────────────┴─────────────────────────────────┐
│                 [ Data Plane ]                          │
│    SDN Switches (Open vSwitch, Whitebox Switch)         │
│    - Match & Action 기반의 단순 고속 포워딩             │
└─────────────────────────────────────────────────────────┘
```

1. **Control Plane (컨트롤 플레인)**: 네트워크의 [[001_operating_system_purpose|운영체제]](Network OS) 역할을 한다. 전체 네트워크의 토폴로지를 수집하고(Global [[151_sql_view_virtual_table|View]]), 최적의 [[339_routing_overview_best_path_selection|라우팅]] 경로를 계산하여 그 결과를 플로우 테이블(Flow Table) 형태로 [[001_dikw_pyramid|데이터]] 플레인 장비들에게 내려보낸다.
2. **[[001_dikw_pyramid|Data]] Plane ([[001_dikw_pyramid|데이터]] 플레인)**: [[238_switch_operation_principles|스위치]]나 라우터 하드웨어(또는 [[630_vswitch_vnf_overhead|vSwitch]]) 계층이다. 패킷이 들어오면 컨트롤러가 내려준 플로우 테이블의 규칙(Rule)에 따라 패킷을 매칭(Match)하고, 지시된 포트로 전달(Action)하는 멍텅구리(Dumb) 고속 처리기 역할을 한다.

- **📢 섹션 요약 비유**: 컨트롤 플레인은 "A번 길은 막히니 B번 길로 가라"고 내비게이션 경로를 짜주는 중앙 서버이고, [[001_dikw_pyramid|데이터]] 플레인은 그 지시만 믿고 묵묵히 달리는 자동차의 바퀴다.

---

## Ⅲ. 비교 및 연결

전통적 네트워크(Traditional Network)와 [[633_sdn_whitebox|SDN]]([[001_dikw_pyramid|Data]]/Control 분리) 구조를 비교하면 다음과 같다.

| 비교 항목 | 전통적 네트워크 (Traditional) | [[633_sdn_whitebox|SDN]] ([[001_dikw_pyramid|Data]]/Control 분리) |
|:---:|:---|:---|
| **제어 방식** | [[136_variance|분산]] 제어 (각 장비가 독립적 판단) | 중앙 집중 제어 ([[633_sdn_whitebox|SDN]] 컨트롤러가 판단) |
| **장비의 역할** | Control Plane + [[001_dikw_pyramid|Data]] Plane 결합 | [[001_dikw_pyramid|Data]] Plane 전담 (단순 포워딩) |
| **운영/관리** | 장비별 개별 [[009_config|설정]] (CLI, [[528_snmp_simple_network_management_protocol|SNMP]]) | 컨트롤러 통한 중앙 [[164_policy|정책]] 일괄 적용 ([[014_api_posix|API]]) |
| **확장성** | 벤더 종속적, 신기능 추가 어려움 | 오픈 소스 기반 프로그래밍 가능 (Programmable) |

이 두 플레인을 연결해 주는 핵심 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 바로 **[[855_openflow_standard_protocol_sdn_southbound|OpenFlow]]**(Southbound [[014_api_posix|API]])다. OpenFlow를 통해 컨트롤러는 [[001_dikw_pyramid|데이터]] 플레인 [[238_switch_operation_principles|스위치]]에 새로운 룰(Flow Entry)을 밀어 넣을 수 있다.

- **📢 섹션 요약 비유**: 전통적 방식이 장인들이 각자 자기 방식대로 물건을 만드는 '수공업'이라면, SDN은 중앙 공장장이 모든 설계도를 쥐고 로봇 팔([[238_switch_operation_principles|스위치]])들에게 획일화된 명령을 내리는 '[[166_smart_factory|스마트 팩토리]]'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
구글, 페이스북 같은 빅테크 기업은 전 세계 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 간을 잇는 WAN(B4)을 구축할 때 이 분리 구조를 채택했다. 트래픽의 우선순위에 따라(예: 화상회의는 [[141_latency|지연 시간]] 최우선, [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]는 [[140_bandwidth|대역폭]] 최우선) 중앙 컨트롤러가 [[001_dikw_pyramid|데이터]] 플레인 [[238_switch_operation_principles|스위치]]들의 경로를 실시간으로 재프로그래밍(Traffic Engineering)하여 회선 사용률을 100% 가깝게 끌어올렸다.

**기술사 판단 포인트 (Trade-off):**
[[001_dikw_pyramid|데이터]]/컨트롤 플레인의 분리는 완벽하지 않다. **'중앙 집중화의 이점'과 '[[454_spof|단일 장애점]]([[454_spof|SPOF]]) 위험'**을 항상 고려해야 한다.
1. [[633_sdn_whitebox|SDN]] 컨트롤러가 죽으면 새로운 트래픽에 대한 경로를 알 수 없어 네트워크 전체가 마비된다. 따라서 컨트롤러는 반드시 3대 이상의 [[136_variance|분산]] 클러스터([[259_raft_paxos|Raft]] 등 [[011_consensus_algorithm|합의 알고리즘]] 기반)로 구성해야 한다.
2. [[238_switch_operation_principles|스위치]]와 컨트롤러 간의 Southbound 연결 구간(Control Network)에 장애가 발생할 경우를 대비해 In-band 관리와 Out-of-band 관리를 혼합 구성하는 물리적 망 분리 설계가 필수적이다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 뇌(Control)와 몸통([[001_dikw_pyramid|Data]])을 분리해 놔서 똑똑해졌지만, 목에 해당하는 연결 통신망이 끊어지면 몸통은 아무것도 못 하는 식물인간이 되므로 통신망의 안전장치가 절대적으로 필요하다.

---

## Ⅴ. 기대효과 및 결론

[[001_dikw_pyramid|데이터]] 플레인과 컨트롤 플레인의 분리는 네트워크 업계에 거대한 지각 변동을 일으켰다. 고가의 똑똑한 라우터 대신, 깡통 [[238_switch_operation_principles|스위치]](Whitebox [[238_switch_operation_principles|Switch]])에 [[191_oss_license_compliance|오픈소스]] 소프트웨어만 얹어 사용할 수 있게 되면서 시스코([[539_netflow_sflow_traffic_monitoring|Cisco]]) 같은 하드웨어 벤더의 독점을 깨뜨렸다. 또한, 관리자가 코딩(Python, [[477_rest_api_architecture|REST API]])으로 수백 대의 장비를 자동 제어할 수 있게 됨으로써 네트워크의 [[652_devops_calms_culture|데브옵스]](NetOps) 시대가 열렸다.

결론적으로 SDN의 [[001_dikw_pyramid|데이터]]/컨트롤 플레인 분리 사상은 [[418_5g_embb_urllc_mmtc_slicing|5G]] [[149_network_slicing_5g_architecture|네트워크 슬라이싱]], 클라우드 가상 [[008_private_cloud|프라이빗 클라우드]]([[836_vpc_virtual_private_cloud_subnet_isolation|VPC]]), [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 마이크로 세그멘테이션의 논리적 기반(Foundation)이 되는 가장 중요한 네트워크 아키텍처 혁신이다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 똑똑한 지휘관(컨트롤러) 한 명과 말 잘 듣는 병사들([[238_switch_operation_principles|스위치]]) 수만 명으로 군대를 재편성한 셈이다. 명령 하나로 대형을 한 번에 바꿀 수 있는 군대의 무서운 민첩성이 바로 SDN이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[865_nfv_network_functions_virtualization_architecture|NFV]] 기반 [[015_virtualization|가상화]] [[866_vnf_virtual_network_function_software_appliance|VNF]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [[164_policy|정책]]과 경로 결정을 담당한다. |
| [[001_dikw_pyramid|데이터]] 평면 ([[001_dikw_pyramid|Data]] Plane) | 실제 패킷 전달을 수행한다. |
| [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: NFV 기반 가상화 VNF]
    │
    ▼
[현재 개념: SDN 데이터/컨트롤 플레인]
    │
    ├──▶ [확장 A: OpenFlow 프로토콜]
    └──▶ [확장 B: 프로그래머블 네트워크]
```

[[633_sdn_whitebox|SDN]] [[001_dikw_pyramid|데이터]]/컨트롤 플레인는 [[865_nfv_network_functions_virtualization_architecture|NFV]] 기반 [[015_virtualization|가상화]] VNF에서 출발해 현재 메커니즘을 정교화하고, 이후 [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날 미니카 장난감은 혼자서 장애물을 피해야 해서 머리가 아주 똑똑해야 했어요. (전통적 네트워크)
2. SDN은 커다란 조종기(Control Plane) 하나로 바보 미니카([[001_dikw_pyramid|Data]] Plane) 여러 대를 무선으로 완벽하게 조종하는 방식이에요.
3. 똑똑한 조종기 하나만 있으면 미니카 부품을 싼 것으로 만들어도 되니까 돈도 아끼고 훨씬 멋진 군무를 만들 수 있답니다!
