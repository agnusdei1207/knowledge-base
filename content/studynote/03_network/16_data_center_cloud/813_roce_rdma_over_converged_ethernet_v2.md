---
title: 813. RoCE (RDMA over Converged Ethernet)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RoCE는 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]와 클라우드 네트워크에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: RoCE를 이해하면 확장성과 운영 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- [[639_rdma_kernel_bypass|RDMA]] 기술은 원래 무결손(Lossless)을 완벽 보장하는 **[[361_infiniband|인피니밴드]]([[361_infiniband|InfiniBand]]) 전용 네트워크 환경에서만 동작**하도록 설계되었습니다.
- 하지만 [[361_infiniband|인피니밴드]]는 비싸고, 기존 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] [[238_switch_operation_principles|스위치]] 장비들과 호환이 안 되며, 특정 벤더(엔비디아/멜라녹스) 종속성이 너무 강했습니다.
- 이에 벤더 연합체(IBTA)는 **전 세계 어디에나 깔려있는 가장 흔한 표준 네트워크 망인 '[[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]([[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])' 케이블과 [[238_switch_operation_principles|스위치]] 위에서도 [[639_rdma_kernel_bypass|RDMA]] 통신([[022_kernel_role|커널]] 우회, 제로 카피)을 그대로 구현할 수 있는 규격, [[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])**를 만들어 냈습니다.

```text
[RDMA]
    │
    ▼
[RoCE]
    │
    └──▶ [iWARP]
```

- **📢 섹션 요약 비유**: RoCE는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [[523_roce|RoCE]] v1 ([[288_version_ihl_tos_total_length|버전]] 1) - L2 계층의 족쇄
- [[459_quic_fec_forward_error_correction|초기]] 1세대는 [[361_infiniband|인피니밴드]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 패킷을 그대로 가져와서 껍데기만 딱 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 프레임(L2, [[673_mac_message_authentication_code|MAC]] 주소)으로 덮어씌웠습니다.
- **한계점**: [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]](L2) 껍데기밖에 없으므로 IP 주소가 없습니다. 따라서 라우터를 타고 다른 네트워크(다른 서브넷이나 해외망)로 나갈 수가 없고, 같은 [[238_switch_operation_principles|스위치]]에 꽂힌 **사내 전산실 동네에서만 쓸 수 있는 반쪽짜리 기술**이었습니다.

### 2. [[523_roce|RoCE]] v2 ([[288_version_ihl_tos_total_length|버전]] 2) - L3 [[339_routing_overview_best_path_selection|라우팅]]의 자유 🌟
- 이 한계를 깨부순 현대 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]의 찐 주력 표준입니다.
- [[361_infiniband|인피니밴드]] 패킷을 **[[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 프레임(L2) + IP 헤더(L3) + [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] [[446_port_and_bus|포트]] 헤더(L4, [[446_port_and_bus|포트]] 4791)**까지 완전히 완벽하게 캡슐화(포장)하여 씌웠습니다.
- **효과**: 이제 이 [[639_rdma_kernel_bypass|RDMA]] 패킷은 IP 주소를 가졌기 때문에, 일반 라우터를 쌩쌩 타고 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 밖을 벗어나 전 세계 인터넷망 어디로든(L3 [[339_routing_overview_best_path_selection|라우팅]] 가능) 자유롭게 날아다니며 원격 메모리에 광속으로 꽂힐 수 있게 되었습니다.

```text
[RDMA]
    │
    ▼
[RoCE]
    │
    └──▶ [iWARP]
```

- **📢 섹션 요약 비유**: RoCE의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

[[523_roce|RoCE]] v2는 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]망을 타지만, 본질적으로 RDMA는 패킷이 하나라도 바닥에 떨어지면 에러가 나며 뻗어버리는 예민한 귀족입니다.
- **문제점**: [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]은 원래 차가 막히면 패킷을 쿨하게 버리는(Drop) 놈입니다.
- **해결책**: RoCE를 완벽히 돌리려면 싸구려 3만 원짜리 [[238_switch_operation_principles|스위치]]로는 안 됩니다. [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 망의 트래픽이 폭주할 때 패킷을 바닥에 버리지 않고 "잠깐 스톱! 뒤에 애들 보내지 마!"라고 통제할 수 있는 **PFC(Priority [[421_tcp_flow_control_sliding_window_algorithm|Flow Control]]) 등의 특수 고급 기능(DCB 규격)이 탑재된 비싼 무결손(Lossless) [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[238_switch_operation_principles|스위치]]**를 반드시 사용해야만 합니다. (앞서 배운 [[697_fcoe|FCoE]](809번)와 완벽히 같은 요구 조건입니다.)

RoCE를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. RDMA가 기반 조건을 만든다면, RoCE는 그 위에서 핵심 메커니즘을 구현하고, iWARP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 확장성과 운영 자동화에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | RDMA의 기반 정리 | RoCE의 핵심 동작 | iWARP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 확장성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: RoCE는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- 빅테크 기업들(AWS, Azure 등)은 전 세계 클라우드 망에 이미 수조 원어치의 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[238_switch_operation_principles|스위치]]들을 깔아 두었습니다. 여기에 [[361_infiniband|인피니밴드]] 전용선을 또 깔기란 불가능합니다. 
- [[523_roce|RoCE]] v2 랜카드(RNIC)만 사다 서버에 꽂으면, 기존 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[238_switch_operation_principles|스위치]] 망을 그대로 재활용하면서도 CPU 오버헤드 0%의 무시무시한 [[639_rdma_kernel_bypass|RDMA]] 속도를 뽑아낼 수 있어, 현재 딥러닝 [[190_ai_llm_requirements_specification|AI]] 클러스터 구축의 양대 산맥([[361_infiniband|인피니밴드]] vs [[523_roce|RoCE]])으로 치열하게 경쟁 중입니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [[639_rdma_kernel_bypass|RDMA]]([[361_infiniband|인피니밴드]])가 오직 KTX 철도(전용망) 위에서만 달릴 수 있는 '시속 300km짜리 특수 열차'라면, **[[523_roce|RoCE]]**는 이 특수 열차의 바퀴를 고무 타이어로 개조하여 전 세계 어디에나 깔려있는 흔한 '일반 아스팔트 고속도로([[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]망)' 위를 달리게 만든 획기적인 '수륙양용 [[344_bus|버스]]'입니다. 값비싼 철길을 새로 깔 필요 없이 기존 고속도로를 그대로 타면서도 300km의 속도를 낼 수 있습니다. 단, 이 특수 [[344_bus|버스]]가 멈추지 않고 달리려면 고속도로 톨게이트 전광판에 "특수 [[344_bus|버스]] 오면 다른 차들 전부 정지!(PFC 무결손 제어)"라는 철저한 프리패스 신호등 시스템이 반드시 고속도로에 깔려 있어야만 합니다.

---

## Ⅴ. 기대효과 및 결론

RoCE는 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]와 클라우드 네트워크를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 확장성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]], [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]], 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: RoCE는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[639_rdma_kernel_bypass|RDMA]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] ([[815_overlay_network_virtualization_l2_extension|Overlay Network]]) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]의 균일한 연결 구조다. |
| [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: RDMA]
    │
    ▼
[현재 개념: RoCE]
    │
    ├──▶ [확장 A: iWARP]
    └──▶ [확장 B: 클라우드 네이티브 네트워킹]
```

RoCE는 RDMA에서 출발해 현재 메커니즘을 정교화하고, 이후 iWARP와 [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 아파트에 사는 친구들이 층마다 다른 규칙으로 엘리베이터를 타면 복잡해져요.
2. 이 개념은 어느 층에서 누구를 어떻게 연결할지 자동으로 정리해 주는 관리실과 같아요.
3. 그래서 많은 컴퓨터가 한 건물 안에서 더 잘 협력할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 934 / 1120

← **이전**: [[812_rdma_remote_direct_memory_access_kernel_bypass|812. RDMA (Remote Direct Memory Access)]]
**다음**: [[814_iwarp_tcp_ip_based_rdma_compatibility|814. iWARP]] →

---
