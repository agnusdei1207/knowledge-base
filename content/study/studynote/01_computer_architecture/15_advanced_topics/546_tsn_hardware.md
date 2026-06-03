+++
weight = 546
title = "546. 결정론적 이더넷 (TSN) 하드웨어"
date = "2026-05-08"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TSN ([[168_industrial_ethernet_tsn|Time-Sensitive Networking]]) 하드웨어는 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[238_switch_operation_principles|스위치]]와 [[587_nic_offloading|NIC]] (Network Interface Card)에 정밀 시계 [[212_synchronization_mechanisms|동기화]], 큐 게이트, 프레임 선점, 중복 전송 제어를 넣어 특정 트래픽의 [[015_지연_데이터_관점|지연]]과 지터를 상한 안에 묶는 구조다.
> 2. **가치**: 제어 패킷과 대용량 영상·진단 트래픽을 같은 케이블에 태우면서도, 산업 제어와 자율주행처럼 마이크로초 단위 deadline을 가진 흐름을 [[571_protection_vs_security|보호]]할 수 있다.
> 3. **판단 포인트**: TSN의 결정론성은 장비 하나만 좋아서 생기지 않으며, 종단 간 모든 [[673_mac_message_authentication_code|MAC]] ([[121_transmission_media_guided_unguided|Media]] [[547_access_control_rwx|Access Control]]), [[238_switch_operation_principles|스위치]], 시간 동기, [[208_schedule_history_transaction_execution_order|스케줄]] 계산이 함께 맞아야 성립한다.

---

## Ⅰ. 개요 및 필요성

결정론적 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] (TSN) 하드웨어는 원래 best-effort 성격이 강했던 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]에 **공유된 시간축과 우선 전송 규칙**을 부여해, 중요한 패킷이 언제 도착할지 예측 가능하게 만드는 장치 구조다. 일반 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]은 [[140_bandwidth|대역폭]]은 넉넉하지만 "먼저 잡은 프레임이 먼저 간다"는 원칙이 강해, 제어 패킷이 큰 비디오 프레임 뒤에서 기다릴 수 있다.

이 대기가 문제인 이유는 전송선 위 직렬화 시간도 결코 짧지 않기 때문이다. 예를 들어 1GbE에서 1500바이트 프레임 하나는 대략 12μs 정도 링크를 점유하고, 100MbE라면 그 시간이 약 120μs까지 늘어난다. 제동 제어, 모션 제어, [[571_protection_vs_security|보호]] 계전처럼 수십~수백 μs 예산을 다투는 환경에서는 한 홉에서 이 정도가 막혀도 전체 deadline이 깨질 수 있다. 그래서 TSN은 "빠른 링크"보다 **중요한 프레임을 제시간에 내보내는 하드웨어 규율**이 필요해진 결과다.

이 그림은 왜 TSN이 단순 고속 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]이 아닌지를 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Best Effort : [1500B Video Frame.............][64B Control] -> Control wait│
│ TSN         : [Best-Effort Gate Closed][Control Slot][Resume] -> Bounded  │
└────────────────────────────────────────────────────────────────────────────┘
```

즉 TSN의 핵심은 [[140_bandwidth|대역폭]] 자체보다 **혼합 트래픽 안에서 시간 자원을 어떻게 배분할지**에 있다. 산업망, 차량망, 오디오·비디오, 일반 데이터가 한 물리망 위에서 공존하려면 이 시간 배분을 하드웨어가 책임져야 한다.

- **📢 섹션 요약 비유**: 일반 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]이 차가 먼저 들어온 순서대로 지나가는 교차로라면, TSN은 구급차가 올 시간을 미리 알고 다른 차선을 잠깐 막아 주는 정밀 [[130_signal|신호]] 체계와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

TSN은 하나의 기능이 아니라, 시간 동기·큐 제어·선점·[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 기능이 결합된 하드웨어 묶음이다. 핵심은 네트워크 전체가 같은 시계를 보고, 그 시계에 맞춰 각 [[446_port_and_bus|포트]]가 어느 큐를 언제 열지 결정한다는 점이다.

| 핵심 블록 | 대표 표준 | 하드웨어 역할 |
| :--- | :--- | :--- |
| 시간 동기 | IEEE 802.1AS | [[446_port_and_bus|포트]] 단 하드웨어 타임스탬프, residence time 보정 |
| 시간 기반 큐 제어 | IEEE 802.1Qbv | Gate Control List로 큐 open/close |
| 프레임 선점 | IEEE 802.1Qbu / 802.3br | 긴 best-effort 프레임을 분할해 긴급 프레임 우선 전송 |
| 중복 전송/제거 | IEEE 802.1CB | [[500_multipath_io|이중 경로]] [[016_replication_factor|복제]] 후 중복 제거 |
| [[094_ingress_kubernetes_l7_routing_gateway|ingress]] policing | IEEE 802.1Qci | 잘못된 burst가 [[208_schedule_history_transaction_execution_order|스케줄]]을 깨지 못하게 차단 |

가장 대표적인 메커니즘은 TAS (Time-Aware Shaper)다. [[446_port_and_bus|포트]]는 여러 [[326_traffic_class_flow_label_ipv6_qos|traffic class]] queue를 갖고 있으며, Gate Control List가 "이번 50μs 구간에는 제어 큐만 열고, 다음 구간에는 오디오 큐를 연다"처럼 문을 여닫는다. 이때 best-effort 프레임이 임계 구간 바로 직전에 링크를 점유하지 않도록 guard band를 두는데, 프레임 선점을 쓰면 이 guard band를 줄여 링크 효율을 높일 수 있다.

이 그림은 TSN [[446_port_and_bus|포트]] 내부의 논리를 요약한다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Sync Clock -> Gate Control List -> Critical Queue -> Port                 │
│            ├───────────────────> Audio Queue    -> Port                   │
│            └───────────────────> Best-Effort Queue -> Port                │
│ Timestamp In -> Residence Time -> Preemption / Replication / Policing     │
└────────────────────────────────────────────────────────────────────────────┘
```

시간 동기 역시 소프트웨어만으로는 부족하다. PTP ([[233_precision_recall_f1_roc_auc_threshold|Precision]] Time [[295_protocol_field_tcp_udp_icmp|Protocol]]) 계열의 타임스탬프를 [[001_operating_system_purpose|운영체제]] ([[001_operating_system_purpose|Operating System]], OS) 위에서 찍으면 [[016_interrupt_mechanism|인터럽트]]와 [[079_kube_scheduler_pod_placement|스케줄러]] [[015_지연_데이터_관점|지연]]이 섞여 오차가 커진다. 그래서 TSN NIC와 [[238_switch_operation_principles|스위치]]는 프레임이 [[673_mac_message_authentication_code|MAC]]·PHY 경계를 지나는 순간을 하드웨어가 직접 기록해 오차를 줄인다. 결국 TSN 하드웨어는 "패킷을 빨리 보내는 장비"가 아니라 **시간표대로 보내는 장비**다.

- **📢 섹션 요약 비유**: TAS는 약속된 시각에만 열리는 철문이고, 프레임 선점은 긴 화물열차를 잠깐 끊어 응급열차를 먼저 통과시키는 장치와 같다.

---

## Ⅲ. 비교 및 연결

TSN의 위치를 이해하려면 표준 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]과 전용 [[347_control_bus|제어 버스]] 사이에서 어디에 놓이는지 봐야 한다.

| 항목 | CAN-FD (Controller Area Network Flexible Data-Rate) | 표준 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] | TSN [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] |
| :--- | :--- | :--- | :--- |
| 시간 모델 | 우선순위 기반, 비교적 단순 | 없음, best effort | 전역 시간 동기 + [[208_schedule_history_transaction_execution_order|스케줄]] |
| [[140_bandwidth|대역폭]] | 낮음~중간 | 높음 | 높음 |
| [[015_지연_데이터_관점|지연]] 예측성 | 좋음 | 낮음 | 매우 높음 |
| 트래픽 혼합 | 제어 중심 | 혼합 가능하지만 보장 약함 | 혼합 + 보장 가능 |
| 확장성 | 제어망에는 유리 | IT 통합에 유리 | IT/[[891_ot_operational_technology|OT]] 융합에 유리 |

CAN-FD나 전통적인 필드버스는 결정론성은 좋지만 [[140_bandwidth|대역폭]]과 확장성이 제한되고, 표준 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]은 [[140_bandwidth|대역폭]]은 좋지만 중요한 프레임의 도착 시각을 보장하기 어렵다. TSN은 이 둘의 간극을 메우며, 산업 자동화와 차량용 zonal architecture에서 "하나의 백본으로 여러 성격의 데이터를 함께 실어 나르는" 기반이 된다.

다만 TSN만으로 엔드투엔드 실시간성이 끝나는 것은 아니다. 수신측 CPU가 패킷을 받은 뒤 RTOS (Real-Time [[001_operating_system_purpose|Operating System]])에서 늦게 처리하면 전체 deadline은 여전히 깨진다. 그래서 TSN은 545번 [[545_interrupt_latency|인터럽트 지연 시간]] 최소화, 547번 [[547_rtos_timer|실시간 시스템 타이머]], 548번 자율주행용 고성능 컴퓨터와 함께 **시간을 다루는 전체 체계**로 이해해야 한다.

- **📢 섹션 요약 비유**: CAN-FD가 차선 수는 적지만 순서가 잘 지켜지는 전용도로라면, 표준 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]은 넓지만 막히는 고속도로이고, TSN은 넓은 도로에 시간 예약 차로를 함께 넣은 스마트 고속도로다.

---

## Ⅳ. 실무 적용 및 기술사 판단

TSN 도입에서 가장 중요한 판단은 "이 홉이 TSN을 지원하느냐"보다 **전체 경로가 같은 시간 모델과 [[208_schedule_history_transaction_execution_order|스케줄]]을 공유하느냐**다. 한 구간이라도 소프트웨어 타임스탬프를 쓰거나, 큐 게이트 설정이 빠지거나, 비지원 [[238_switch_operation_principles|스위치]]가 끼면 지터와 [[015_지연_데이터_관점|지연]] 상한이 무너진다.

### 적용 판단 [[435_checklist_based_testing|체크리스트]]

1. 모든 홉이 IEEE 802.1AS 하드웨어 타임스탬프를 지원하는가?
2. 제어 주기와 최대 프레임 크기를 고려해 guard band와 cycle time을 계산했는가?
3. 긴 best-effort 프레임이 critical traffic을 막지 않도록 preemption이 필요한가?
4. 제어 트래픽과 일반 트래픽에 [[094_ingress_kubernetes_l7_routing_gateway|ingress]] policing, [[224_vlan_virtual_lan_broadcast_domain|VLAN]] PCP (Priority [[082_process_memory_structure|Code]] Point), 큐 매핑이 일관되게 적용되는가?
5. 종단 장치의 [[001_operating_system_purpose|운영체제]]와 드라이버가 네트워크가 보장한 시간을 실제 애플리케이션까지 이어받을 수 있는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- TSN [[238_switch_operation_principles|스위치]]는 쓰면서 단말 NIC는 소프트웨어 타임스탬프에 의존하는 구성
- [[208_schedule_history_transaction_execution_order|스케줄]] 계산 없이 "우선순위만 높이면 된다"고 생각하는 구성
- 100MbE 구간에서 큰 프레임 직렬화 [[015_지연_데이터_관점|지연]]을 무시하고 preemption을 생략하는 설계
- 네트워크만 결정론적으로 만들고, 종단 CPU (Central Processing Unit) [[208_schedule_history_transaction_execution_order|스케줄]]링과 [[016_interrupt_mechanism|인터럽트]] [[015_지연_데이터_관점|지연]]은 점검하지 않는 운영

기술사 답안에서는 "TSN = 실시간 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]" 정도로만 쓰면 부족하다. **[[212_synchronization_mechanisms|동기화]], TAS, preemption, Frame [[016_replication_factor|Replication]] and Elimination for [[345_reliability_security|Reliability]] (FRER), [[946_guard_band_fdm_adjacent_channel_interference|guard band]], [[401_transport_layer_role_end_to_end_multiplexing|end-to-end]] schedule**을 함께 설명해야 비로소 설계 판단이 된다.

- **📢 섹션 요약 비유**: TSN 구축은 오케스트라 지휘와 같다. 악기 하나가 좋아도 모두가 같은 박자표를 보지 않으면 합주가 무너진다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 TSN 하드웨어는 서로 다른 중요도의 트래픽을 하나의 네트워크로 통합하면서도, 중요한 흐름의 [[015_지연_데이터_관점|지연]] 상한을 관리할 수 있게 한다. 그 결과 배선과 게이트웨이 수를 줄이고, [[891_ot_operational_technology|OT]] ([[891_ot_operational_technology|Operational Technology]])와 IT (Information Technology) 네트워크를 통합하며, 차량·공장·오디오 시스템에서 예측 가능한 통신 기반을 만든다.

한계도 명확하다. 일정 계산이 복잡하고, 네트워크 구성 변경 시 검증이 다시 필요하며, 모든 장비가 하드웨어 지원을 갖춰야 비용이 올라간다. 앞으로는 중앙 [[208_schedule_history_transaction_execution_order|스케줄]]링 자동화, [[418_5g_embb_urllc_mmtc_slicing|5G]]/무선 TSN 연계, zonal vehicle backbone, 더 정교한 시간 동기 failover처럼 **시간 자원을 네트워크 전체에서 공동 관리하는 방향**이 강화될 가능성이 크다.

결론적으로 TSN 하드웨어는 "빠른 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]"이 아니라 **시간까지 제어하는 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]**으로 기억하는 것이 가장 정확하다. 이 관점이 잡혀야 왜 큐, 시계, [[208_schedule_history_transaction_execution_order|스케줄]], 종단 CPU까지 한 흐름으로 묶어 봐야 하는지도 자연스럽게 이해된다.

- **📢 섹션 요약 비유**: TSN은 자유롭게 다니던 도로에 단순 속도 제한을 거는 것이 아니라, 시간표와 우선 통로를 함께 넣어 교통 전체를 약속된 리듬으로 움직이게 만드는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| IEEE 802.1AS | 네트워크 전체가 같은 시간을 공유하게 만드는 [[212_synchronization_mechanisms|동기화]] 기반이다. |
| TAS (Time-Aware Shaper) | 큐를 시간표대로 열고 닫아 [[015_지연_데이터_관점|지연]] 상한을 만든다. |
| Frame Preemption | 긴 프레임이 긴급 트래픽을 막지 못하게 하는 링크 효율 향상 장치다. |
| FRER (Frame [[016_replication_factor|Replication]] and Elimination for [[345_reliability_security|Reliability]]) | 경로 [[016_replication_factor|복제]]와 중복 제거로 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 높인다. |
| [[094_ingress_kubernetes_l7_routing_gateway|Ingress]] Policing | 비정상 트래픽 burst가 [[208_schedule_history_transaction_execution_order|스케줄]]을 깨지 못하게 막는다. |
| RTOS (Real-Time [[001_operating_system_purpose|Operating System]]) | TSN이 보장한 시간을 종단 애플리케이션의 응답성으로 이어 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Best-effort Ethernet
        │
        ▼
AVB (Audio Video Bridging) 기반 시간 인지 전송
        │
        ▼
IEEE 802.1AS 동기화 + TAS 기반 큐 제어
        │
        ▼
Frame Preemption · FRER · Ingress Policing
        │
        ▼
OT/IT 융합형 결정론적 백본 · 차량용 zonal 네트워크
```

이 흐름은 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]이 단순 [[140_bandwidth|대역폭]] 제공자에서 출발해, 이제는 시간과 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]까지 관리하는 제어 네트워크로 확장되고 있음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 원래 인터넷 선은 먼저 줄 선 데이터부터 보내서, 큰 영상이 지나가면 중요한 [[130_signal|신호]]가 늦어질 수 있어요.
2. TSN은 "이 시간엔 중요한 [[130_signal|신호]] 먼저!"라는 시계와 규칙을 인터넷 선에 넣어 줘요.
3. 그래서 브레이크나 공장 기계 [[130_signal|신호]]가 길을 잃지 않고 제시간에 도착할 수 있답니다.
