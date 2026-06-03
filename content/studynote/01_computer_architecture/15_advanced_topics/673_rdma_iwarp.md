---
title: 673. RDMA iWARP 프로토콜
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]] (Internet Wide Area [[639_rdma_kernel_bypass|RDMA]] [[295_protocol_field_tcp_udp_icmp|Protocol]])는 [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]) 요청을 [[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]]/Internet [[295_protocol_field_tcp_udp_icmp|Protocol]] ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP) 위에서 실어 나르도록 만든, [[339_routing_overview_best_path_selection|라우팅]] 가능한 [[639_rdma_kernel_bypass|RDMA]] 전송 방식이다.
> 2. **가치**: TCP의 순서 보장·재전송·혼잡 제어를 [[639_rdma_kernel_bypass|RDMA]] Network Interface Card (RNIC)가 하드웨어로 처리하면, Priority [[421_tcp_flow_control_sliding_window_algorithm|Flow Control]] (PFC) 같은 무손실 [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 특수 [[009_config|설정]] 없이도 원격 메모리와 스토리지 [[015_지연_데이터_관점|지연]]을 크게 줄일 수 있다.
> 3. **판단 포인트**: iWARP는 [[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] ([[523_roce|RoCE]])보다 배치 장벽은 낮지만 전송 계층이 더 무거워 절대 [[015_지연_데이터_관점|지연]]은 불리할 수 있으므로, 최저 [[015_지연_데이터_관점|지연]]보다 기존 Layer 3 네트워크 호환성과 운영 단순성이 더 중요한 환경에 맞는다.

---

## Ⅰ. 개요 및 필요성

iWARP는 일반 IP 네트워크 위에서도 RDMA의 장점을 살리기 위해 등장한 프로토콜이다. [[136_variance|분산]] 스토리지나 [[002_database_definition|데이터베이스]] 클러스터에서 병목은 종종 "링크 [[140_bandwidth|대역폭]] 부족"이 아니라 Central Processing Unit (CPU)이 [[022_kernel_role|커널]] 네트워크 [[057_stack|스택]]과 메모리 복사를 반복하느라 낭비되는 경로 길이에 있다. RDMA는 이 경로를 줄여 짧은 [[015_지연_데이터_관점|지연]]과 낮은 CPU 사용률을 노리지만, 기존 [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 환경에서는 패킷 손실과 혼잡이 걸림돌이 된다.

RoCE는 매우 낮은 [[015_지연_데이터_관점|지연]]을 제공하지만, 패킷 손실이 생기면 성능과 안정성이 급격히 흔들릴 수 있어 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 스위치에 PFC, Explicit Congestion Notification (ECN) 같은 세밀한 튜닝이 필요하다. iWARP는 이 문제를 "네트워크를 바꾸자"가 아니라 "[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있는 전송 계층을 활용하자"로 풀었다. 즉, 이미 널리 배치된 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 메커니즘을 사용해 RDMA를 보다 운영 친화적으로 가져오려는 선택이다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Goal: keep RDMA semantics without requiring lossless Ethernet               │
├──────────────────────────────────────────────────────────────────────────────┤
│ Socket I/O      -> portable, but copy + kernel overhead remain             │
│ RoCE            -> very low latency, but fabric tuning is demanding        │
│ iWARP           -> higher transport cost, easier on routed TCP/IP networks │
└──────────────────────────────────────────────────────────────────────────────┘
```

핵심은 iWARP가 "인터넷 어디서나 RDMA를 공짜로 쓴다"는 마법이 아니라, 표준 IP 운영 절차 위에서 [[639_rdma_kernel_bypass|RDMA]] [[440_offloading|오프로딩]]을 실현하려는 절충안이라는 점이다. 따라서 필요성은 속도 그 자체보다도, **기존 네트워크 팀의 운영 모델을 크게 바꾸지 않고 RDMA를 도입하려는 요구**에서 가장 선명하게 드러난다.

- **📢 섹션 요약 비유**: iWARP는 비포장도로에 맞춰 서스펜션을 달아 놓은 고속 택배차와 같다. 최고 속도는 전용 경주 트랙보다 조금 느릴 수 있지만, 이미 깔려 있는 일반 도로망을 훨씬 수월하게 이용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

iWARP의 [[057_stack|스택]]은 단순히 "RDMA를 TCP에 넣었다"로 끝나지 않는다. 상위의 [[639_rdma_kernel_bypass|RDMA]] verbs 요청을 아래 계층에서 풀어, 스트림 기반 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 위에서도 원격 메모리 읽기/[[289_cqrs_db|쓰기]] 의미를 유지하도록 여러 프로토콜이 층층이 쌓인다. 대표적으로 RDMAP ([[639_rdma_kernel_bypass|RDMA]] [[295_protocol_field_tcp_udp_icmp|Protocol]]), DDP ([[176_direct_addressing|Direct]] [[001_dikw_pyramid|Data]] Placement), MPA (Marker PDU Aligned, PDU는 [[295_protocol_field_tcp_udp_icmp|Protocol]] [[001_dikw_pyramid|Data]] Unit)가 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 위에 올라가고, RNIC는 이를 해석해 원격 버퍼로 바로 배치한다.

| 계층/구성 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [[639_rdma_kernel_bypass|RDMA]] verbs | 애플리케이션이 read/write/send를 요청하는 인터페이스 | [[022_kernel_role|커널]] [[125_socket|소켓]] 호출보다 짧은 [[001_dikw_pyramid|데이터]] 경로를 지향 |
| RDMAP ([[639_rdma_kernel_bypass|RDMA]] [[295_protocol_field_tcp_udp_icmp|Protocol]]) | [[639_rdma_kernel_bypass|RDMA]] 연산 의미를 정의 | 원격 메모리 접근의 의미 보존 |
| DDP ([[176_direct_addressing|Direct]] [[001_dikw_pyramid|Data]] Placement) | 수신 [[001_dikw_pyramid|데이터]]를 지정된 버퍼에 바로 배치 | 불필요한 중간 복사 감소 |
| MPA (Marker PDU Aligned) | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 스트림 위에서 메시지 경계를 맞춤 | [[639_rdma_kernel_bypass|RDMA]] 메시지를 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[074_byte|바이트]] 스트림에 적재 |
| RNIC + [[588_toe|TOE]] ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] Offload Engine) | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 처리와 [[639_rdma_kernel_bypass|RDMA]] 배치를 하드웨어 [[440_offloading|오프로딩]] | 재전송·정렬·혼잡 반응을 CPU 대신 NIC가 담당 |

이 구조에서 가장 중요한 것은 RNIC가 단순한 네트워크 카드가 아니라는 점이다. 송신 측 RNIC는 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 세그먼트화, 순서 제어, 재전송을 수행하고, 수신 측 RNIC는 재조립된 페이로드를 [[318_dma|Direct Memory Access]] ([[746_io_direct_memory_access_dma|DMA]])로 지정 버퍼에 바로 쓴다. 그래서 손실이 있는 네트워크에서도 애플리케이션은 비교적 안정적으로 [[639_rdma_kernel_bypass|RDMA]] 완료 의미를 받을 수 있다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ App -> Verbs -> RDMAP -> DDP -> MPA -> TCP -> IP -> Ethernet               │
│                                                                              │
│ Ethernet -> IP -> TCP reassembly -> MPA -> DDP -> DMA write -> remote buf  │
│                           handled largely by RNIC / TOE                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

물론 대가도 있다. TCP의 상태 관리, 혼잡 제어, 순서 보장 덕분에 운영은 편해지지만, 패킷 손실 시 재전송과 정렬 비용이 더해져 [[015_지연_데이터_관점|지연]] 꼬리값이 커질 수 있다. 즉 iWARP의 원리는 **네트워크를 무손실로 만들지 않는 대신, 전송 계층의 복잡성을 RNIC로 끌어안는 구조**라고 정리할 수 있다.

- **📢 섹션 요약 비유**: iWARP는 택배 상자를 그냥 던져 보내는 대신, 상자마다 추적표와 재배송 규칙을 붙여 두는 방식과 같다. 포장과 관리가 더 복잡해지지만, 길에서 한 번 흔들려도 결국 목적지까지 도착시키기 쉽다.

---

## Ⅲ. 비교 및 연결

iWARP의 위치는 [[523_roce|RoCE]], 그리고 일반 [[125_socket|소켓]] 통신과 비교할 때 가장 분명해진다. 셋 모두 원격 [[001_dikw_pyramid|데이터]] 교환을 하지만, 어떤 계층에서 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 확보하고 어느 정도 운영 부담을 감수하는지가 다르다.

| 구분 | [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 확보 방식 | 네트워크 요구사항 | [[015_지연_데이터_관점|지연]] 특성 | 잘 맞는 문제 |
| :--- | :--- | :--- | :--- | :--- |
| 일반 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[125_socket|소켓]] | [[022_kernel_role|커널]] [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP [[057_stack|스택]] | 표준 IP 네트워크 | 가장 범용적이지만 CPU 비용 큼 | 범용 애플리케이션 통신 |
| **[[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]]** | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] + RNIC [[440_offloading|오프로딩]] | 표준 routed [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 활용 가능 | RoCE보다 무거울 수 있으나 운영 친화적 | [[639_rdma_kernel_bypass|RDMA]] 도입 장벽을 낮추려는 스토리지·[[015_virtualization|가상화]] |
| [[523_roce|RoCE]] | [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 기반 [[639_rdma_kernel_bypass|RDMA]], 네트워크 튜닝 의존 | PFC·ECN 중심의 저손실 패브릭 선호 | 가장 낮은 [[015_지연_데이터_관점|지연]] | 고성능 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 내부 통신 |

이 차이는 [[499_nvme_over_fabrics|NVMe-oF]] ([[499_nvme_over_fabrics|NVMe over Fabrics]]), Server Message Block (SMB) [[176_direct_addressing|Direct]] 같은 상위 [[090_service_kubernetes_network_load_balancing|서비스]] 선택에도 연결된다. 최저 [[015_지연_데이터_관점|지연]]이 절대적인 [[231_ai_turing_test|인공지능]] 학습 클러스터나 초저지연 거래 환경은 대체로 RoCE를 더 선호하지만, 이미 구축된 Layer 3 [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 인프라를 크게 건드리기 어렵고 운영 표준을 유지해야 하는 조직은 iWARP를 검토할 여지가 있다. 또한 iWARP는 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 기반이어서 [[339_routing_overview_best_path_selection|라우팅]] 친화성이 높지만, 그렇다고 장거리 회선의 왕복 [[015_지연_데이터_관점|지연]] 자체를 없애 주는 것은 아니다.

즉 비교의 핵심은 "무엇이 더 최신인가"가 아니라 **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]의 위치와 운영 비용의 위치가 어디인가**다. RoCE는 네트워크가 더 많은 책임을 지고, iWARP는 RNIC와 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 계층이 더 많은 책임을 진다.

- **📢 섹션 요약 비유**: RoCE가 전용 수로를 파서 [[148_5g_embb_urllc_mmtc|초고속]] 보트를 띄우는 방식이라면, iWARP는 기존 강줄기를 쓰되 배에 더 좋은 자동조종 장치를 다는 방식이다. 어느 쪽이 좋은지는 물길을 새로 만들 수 있는지부터 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **기존 Layer 3 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]에서 [[639_rdma_kernel_bypass|RDMA]] 도입**
   - 스위치를 모두 무손실 패브릭용으로 재구성하기 어렵다면 iWARP가 [[459_quic_fec_forward_error_correction|초기]] 진입 장벽을 낮춘다.
   - 특히 스토리지 노드 간 [[016_replication_factor|복제]], 원격 메모리 접근, [[501_file_definition_logical_record|파일]] [[090_service_kubernetes_network_load_balancing|서비스]] 가속처럼 RDMA의 CPU 절감 효과가 큰 워크로드에 유리하다.

2. **[[015_virtualization|가상화]]/클러스터 환경의 운영 단순화**
   - 네트워크 운영팀이 이미 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 기반 모니터링, [[690_firewall_generation_evolution|방화벽]], [[339_routing_overview_best_path_selection|라우팅]] [[164_policy|정책]]에 익숙한 경우 iWARP는 절차적 이질감이 적다.
   - 다만 RNIC 지원 여부와 [[001_operating_system_purpose|운영체제]] 드라이버 성숙도를 먼저 확인해야 한다.

3. **원격 스토리지 전송**
   - [[482_nvme|NVMe]]-oF나 저지연 [[501_file_definition_logical_record|파일]] [[090_service_kubernetes_network_load_balancing|서비스]]에서 로컬에 가까운 입출력을 노릴 수 있다.
   - 하지만 회선 왕복 [[015_지연_데이터_관점|지연]]이 큰 구간에서는 TCP의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]이 있어도 물리적 거리 비용은 남으므로, 기대 성능을 과대평가하면 안 된다.

### 채택/회피 판단 체크포인트

- **채택이 유리한 경우**
  - RDMA의 저CPU 특성은 필요하지만, 무손실 [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 운영 역량이나 전용 패브릭 투자 여력이 부족한 경우
  - 기존 routed [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] [[164_policy|정책]], 보안 장비, 운영 도구와 최대한 공존해야 하는 경우
  - RNIC가 충분한 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[440_offloading|오프로딩]] 성능과 검증된 드라이버를 제공하는 경우

- **회피가 유리한 경우**
  - 마이크로초 단위 최저 [[015_지연_데이터_관점|지연]]이 경쟁력 자체인 워크로드
  - 벤더 생태계와 상호운용성이 [[523_roce|RoCE]] 중심으로 굳어 있는 환경
  - 네트워크 손실 시 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 재전송으로 인한 [[015_지연_데이터_관점|지연]] 꼬리 증가를 받아들이기 어려운 환경

기술사 답안에서는 "iWARP가 TCP라서 무조건 안전하다"가 아니라, **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 확보 위치를 네트워크에서 전송 계층 하드웨어로 옮기는 선택**이라고 표현하는 편이 정확하다. 또한 배치가 쉬운 것과 항상 빠른 것은 다르다는 점을 분명히 짚어야 한다.

- **📢 섹션 요약 비유**: iWARP를 고르는 일은 산악도로에도 달릴 수 있는 차를 고르는 것과 같다. 최고 트랙 기록은 조금 양보하더라도, 실제 도로 사정에서 더 편하게 운용할 수 있으면 그 선택이 더 합리적일 수 있다.

---

## Ⅴ. 기대효과 및 결론

iWARP의 가장 큰 기대효과는 [[639_rdma_kernel_bypass|RDMA]] 도입의 심리적·운영적 장벽을 낮춘다는 데 있다. 기존 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 친화적 환경을 활용해 CPU 오버헤드와 복사 비용을 줄일 수 있으므로, 스토리지와 클러스터 통신의 효율을 개선하면서도 네트워크 설계 전체를 뒤엎지 않아도 된다. 특히 "무손실 네트워크가 전제여야 한다"는 부담을 덜어 준다는 점이 실무에서 크다.

반면 iWARP는 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 기반이라는 특성상 전송 계층이 더 무겁고, 고성능 생태계의 무게 중심이 [[523_roce|RoCE]] 쪽에 있는 경우도 많다. 따라서 iWARP를 기억할 때는 "RoCE의 하위호환"이 아니라 **표준 IP 운영 환경과 [[639_rdma_kernel_bypass|RDMA]] [[440_offloading|오프로딩]]을 연결하는 실용적 절충안**으로 보는 것이 맞다. 결국 핵심 질문은 "가장 빠른가"보다 "우리 네트워크 현실에서 가장 잘 굴러가는가"이다.

- **📢 섹션 요약 비유**: iWARP는 최고 속도만 노린 경주용 자전거가 아니라, 장거리 통근길에서도 안정적으로 탈 수 있도록 기어와 브레이크를 잘 갖춘 자전거에 가깝다. 약간 덜 날카로워도 실제 길에서는 더 믿음직할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| RNIC ([[639_rdma_kernel_bypass|RDMA]] Network Interface Card) | iWARP의 핵심 하드웨어로, 전송 처리와 메모리 배치를 [[440_offloading|오프로딩]]한다. |
| [[588_toe|TOE]] ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] Offload Engine) | iWARP가 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 쓰면서도 CPU 부담을 줄이는 핵심 장치 기능이다. |
| DDP ([[176_direct_addressing|Direct]] [[001_dikw_pyramid|Data]] Placement) | 수신 [[001_dikw_pyramid|데이터]]를 지정된 버퍼로 직접 배치해 복사 비용을 줄인다. |
| [[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]) | iWARP와 대비되는 [[639_rdma_kernel_bypass|RDMA]] [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 계열로, 더 낮은 [[015_지연_데이터_관점|지연]] 대신 더 많은 패브릭 튜닝이 필요하다. |
| [[499_nvme_over_fabrics|NVMe-oF]] ([[499_nvme_over_fabrics|NVMe over Fabrics]]) | [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]] 같은 저지연 전송 방식을 활용해 원격 스토리지를 빠르게 제공하는 상위 기술이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
복사 중심 TCP socket 입출력
        │
        ▼
RDMA (Remote Direct Memory Access) 오프로딩
        │
        ├──────────────▶ RoCE (RDMA over Converged Ethernet) 저지연 패브릭
        │
        ▼
iWARP (Internet Wide Area RDMA Protocol) on TCP/IP
        │
        ▼
SMB Direct / NVMe-oF (NVMe over Fabrics) 같은 저지연 원격 스토리지 서비스
```

이 흐름은 원격 입출력이 "[[022_kernel_role|커널]] 복사와 [[125_socket|소켓]] 처리"에서 출발해, [[639_rdma_kernel_bypass|RDMA]] 계열로 갈라지며 네트워크 운영 방식에 따라 RoCE와 iWARP라는 서로 다른 최적화 경로를 갖게 된 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. iWARP는 무거운 짐을 멀리 있는 친구 책상까지 빨리 보내 주는 특별한 택배길이에요.
2. 길이 조금 울퉁불퉁해도 택배차가 스스로 다시 정리하고 안전하게 가져가요.
3. 그래서 아주 매끈한 전용 도로가 없어도 빠른 배달을 시작하기 쉬워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 674 / 803

← **이전**: [[672_spdk|672. SPDK (Storage Performance Development Kit)]]
**다음**: [[674_storage_tiering|674. 스토리지 티어링 (Storage Tiering)]] →

---
