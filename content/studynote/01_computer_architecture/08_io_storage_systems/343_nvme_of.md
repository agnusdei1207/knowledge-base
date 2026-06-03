---
title: 343. NVMe-oF (NVMe over Fabrics)
date: '2026-03-27'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[499_nvme_over_fabrics|NVMe-oF]] ([[482_nvme|Non-Volatile Memory Express]] over Fabrics)는 서버 내부 버스에 묶여 있던 [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]]) 명령 체계를 네트워크 패브릭까지 확장해, 원격 [[327_ssd|SSD]] ([[592_open_channel_ssd|Solid-State Drive]])를 로컬 장치처럼 다루게 만드는 기술이다.
> 2. **가치**: 이 기술의 핵심 가치는 단순 원격 접속이 아니라, [[339_das|DAS]] ([[339_das|Direct Attached Storage]])의 고립 문제를 풀면서도 수십 마이크로초 수준의 [[015_지연_데이터_관점|지연]]시간으로 고성능 스토리지 풀을 공유할 수 있게 만든다는 점이다.
> 3. **판단 포인트**: [[482_nvme|NVMe]]-oF는 언제나 가장 빠른 선택이 아니라, 네트워크 품질·CPU 오버헤드·멀티패스 설계·운영 복잡도까지 감당할 수 있을 때 진가가 나는 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]형 아키텍처다.

---

## Ⅰ. 개요 및 필요성

[[482_nvme|NVMe]]-oF는 [[356_pcie|PCIe]] ([[355_pci|Peripheral Component Interconnect]] Express)에 직접 연결된 고속 저장장치의 접근 방식을, [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] ([[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])·파이버 채널 ([[696_fibre_channel_protocol|Fibre Channel]])·[[361_infiniband|인피니밴드]] ([[361_infiniband|InfiniBand]]) 같은 패브릭 네트워크 바깥으로 확장한 원격 블록 스토리지 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이다. 기존에는 [[482_nvme|NVMe]] SSD를 서버 안에 꽂아야 가장 좋은 [[282_performance_tactics|성능]]이 나왔기 때문에, [[282_performance_tactics|성능]]은 높아도 저장공간이 서버마다 고립되는 문제가 컸다. 어떤 서버는 디스크가 남고 어떤 서버는 부족해지는 [[339_das|DAS]] 구조의 비효율이 커질수록, 자원 활용률보다 장비 수를 더 늘리는 왜곡이 생겼다.

반대로 전통적인 [[493_san_storage_area_network|SAN]] ([[493_san_storage_area_network|Storage Area Network]])이나 [[698_iscsi|iSCSI]] (Internet Small Computer Systems Interface)는 스토리지를 공유하기는 쉬웠지만, SCSI (Small Computer System Interface) 계열 명령 체계와 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP [[057_stack|스택]] 오버헤드 때문에 NVMe급 [[430_index_fast_full_scan|병렬]]성과 [[015_지연_데이터_관점|지연]] 특성을 살리기 어려웠다. 즉 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]는 오랫동안 "빠르지만 고립된 로컬 [[482_nvme|NVMe]]"와 "공유되지만 상대적으로 무거운 네트워크 스토리지" 사이에서 선택을 강요받았다. [[482_nvme|NVMe]]-oF는 이 틈을 메우기 위해 등장했다.

아래 그림은 왜 [[482_nvme|NVMe]]-oF가 단순한 원격 디스크가 아니라, **고성능의 공유화**를 위한 기술인지 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                 DAS 한계와 NVMe-oF의 등장 배경                            │
├───────────────────────┬────────────────────────┬───────────────────────────┤
│ 구분                  │ 서버 내부 NVMe         │ 기존 네트워크 스토리지    │
├───────────────────────┼────────────────────────┼───────────────────────────┤
│ 성능                  │ 매우 높음              │ 상대적으로 낮음            │
│ 자원 활용             │ 서버별 고립            │ 공유 가능                  │
│ 병목                  │ 용량 파편화            │ 프로토콜/CPU 오버헤드      │
│ 데이터센터 요구       │ 공유 + 저지연 동시 충족│ 둘 중 하나만 만족          │
└───────────────────────┴────────────────────────┴───────────────────────────┘
                │
                ▼
      NVMe 명령 체계 유지 + 패브릭 확장 = NVMe-oF
```

핵심은 "원격화"보다 "NVMe의 [[430_index_fast_full_scan|병렬]] 구조를 유지한 채 공유화한다"는 점이다. 그래서 [[482_nvme|NVMe]]-oF는 단순 [[492_nas_network_attached_storage|NAS]] ([[492_nas_network_attached_storage|Network Attached Storage]])의 고속판이 아니라, 분리형 인프라에서 로컬급 I/O 경험을 재현하려는 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 설계 철학에 가깝다.

- **📢 섹션 요약 비유**: 각 반마다 개인 냉장고를 두면 빨리 꺼내 먹을 수는 있지만 남는 공간이 생긴다. 반대로 공동 창고만 쓰면 함께 쓰기는 쉽지만 줄이 길어진다. [[482_nvme|NVMe]]-oF는 공동 창고를 쓰면서도 각자 책상 옆 냉장고처럼 빠르게 꺼내게 만드는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[482_nvme|NVMe]]-oF의 동작은 크게 호스트, 전송 계층, 타깃으로 나뉜다. 호스트는 애플리케이션의 I/O 요청을 [[482_nvme|NVMe]] 큐에 적재하고, 전송 계층은 그 큐 명령을 패브릭 위로 캡슐화해 보내며, 타깃은 이를 실제 [[061_namespace|네임스페이스]] ([[061_namespace|Namespace]])와 [[327_ssd|SSD]] 자원에 매핑해 처리한다. 중요한 점은 명령 의미를 SCSI로 변환하지 않고 **[[482_nvme|NVMe]] 큐 모델 자체를 유지**한다는 것이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| 호스트 (Host) | 애플리케이션 I/O를 [[482_nvme|NVMe]] 명령으로 [[087_process_state_transition|생성]] | 멀티큐 활용, CPU 부담 최소화 |
| 전송 계층 (Transport) | 명령/[[001_dikw_pyramid|데이터]]를 패브릭으로 전달 | [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]) 여부, [[015_지연_데이터_관점|지연]] 특성 |
| 타깃 (Target) | 원격 [[482_nvme|NVMe]] 서브시스템 제공 | [[061_namespace|네임스페이스]] 매핑, 고가용성 |
| 패브릭 (Fabric) | [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]·[[696_fibre_channel_protocol|FC]]·[[361_infiniband|InfiniBand]] 기반 네트워크 | 손실 제어, [[140_bandwidth|대역폭]], 경로 [[456_dual_redundancy|이중화]] |

아래 그림은 [[482_nvme|NVMe]]-oF가 "블록 명령 전달"을 어떻게 짧은 경로로 처리하는지 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    NVMe-oF 데이터 경로와 병목 위치                         │
├────────────────────────────────────────────────────────────────────────────┤
│ Application                                                                │
│      │                                                                     │
│      ▼                                                                     │
│ Host NVMe Driver ──▶ Submission Queue ──▶ Fabric Transport                 │
│                                           │                                │
│                                           ├─ RDMA/RoCE : 커널 개입 최소화  │
│                                           ├─ FC-NVMe   : 전용 SAN 활용     │
│                                           └─ NVMe/TCP  : 범용성 높음       │
│                                                                    │       │
│                                                                    ▼       │
│ Target Controller ──▶ Completion Queue ──▶ Namespace ──▶ NVMe SSD          │
└────────────────────────────────────────────────────────────────────────────┘
```

이 구조의 [[282_performance_tactics|성능]]은 두 가지에서 나온다. 첫째, NVMe의 다중 큐 구조를 유지하므로 [[430_index_fast_full_scan|병렬]] I/O에서 락 경합과 큐 병목이 줄어든다. 둘째, RDMA를 쓰는 전송 방식은 [[022_kernel_role|커널]] 우회와 제로 카피 ([[585_zero_skipping|Zero]] Copy)에 가까운 전송이 가능해 CPU 개입을 줄인다. 다만 모든 환경이 RDMA에 적합한 것은 아니므로, 오늘날에는 운영 편의성을 위해 [[482_nvme|NVMe]]/TCP도 많이 채택된다.

전송 방식은 [[282_performance_tactics|성능]]과 운영 난도를 함께 바꾼다.

| 전송 방식 | 첫 특성 | 강점 | 주의점 |
| :-- | :-- | :-- | :-- |
| [[696_fibre_channel_protocol|FC]]-[[482_nvme|NVMe]] ([[696_fibre_channel_protocol|Fibre Channel]] [[482_nvme|NVMe]]) | 전용 [[493_san_storage_area_network|SAN]] 기반 | 예측 가능한 [[015_지연_데이터_관점|지연]], 기존 [[696_fibre_channel_protocol|FC]] 인프라 활용 | 비용 높음 |
| [[482_nvme|NVMe]]/[[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]) | [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 기반 [[639_rdma_kernel_bypass|RDMA]] | 매우 낮은 [[015_지연_데이터_관점|지연]], 높은 [[139_throughput|처리량]] | 무손실 네트워크 설계 필요 |
| [[482_nvme|NVMe]]/[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] ([[482_nvme|NVMe]] over [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]) | 표준 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 기반 | 범용성, 도입 용이성 | CPU 오버헤드와 [[015_지연_데이터_관점|지연]] 증가 |

즉 [[482_nvme|NVMe]]-oF의 핵심 원리는 "원격화했지만 명령 체계는 가볍게 유지하고, [[001_dikw_pyramid|데이터]] 이동 경로를 짧게 만든다"로 요약할 수 있다. 여기서 병목은 디스크 자체보다 패브릭 [[015_지연_데이터_관점|지연]], 혼잡 제어, 타깃 확장성, 멀티패스 설계로 이동한다.

- **📢 섹션 요약 비유**: 택배 내용을 바꾸지 않고, 빠른 전용 통로로 그대로 보내는 구조라고 보면 된다. 물건을 다시 포장해 다른 언어로 번역하면 느려지고, 원래 상자 그대로 전용 레일에 싣기 때문에 빨라지는 것이다.

---

## Ⅲ. 비교 및 연결

[[482_nvme|NVMe]]-oF를 정확히 이해하려면 로컬 [[482_nvme|NVMe]], 전통적 [[493_san_storage_area_network|SAN]], 그리고 [[492_nas_network_attached_storage|NAS]] 계열과 경계를 나눠서 봐야 한다. 로컬 NVMe는 가장 짧은 경로를 가지므로 절대 [[282_performance_tactics|성능]]은 유리하지만 공유성과 유연성이 약하다. 반면 NAS는 [[501_file_definition_logical_record|파일]] 단위 공유에는 편하지만, 블록 스토리지 특유의 낮은 [[015_지연_데이터_관점|지연]]과 고병렬 I/O가 필요한 [[002_database_definition|데이터베이스]]·[[015_virtualization|가상화]]·[[190_ai_llm_requirements_specification|AI]] 훈련 환경과는 지향점이 다르다.

| 비교 항목 | 로컬 [[482_nvme|NVMe]] | [[499_nvme_over_fabrics|NVMe-oF]] | [[698_iscsi|iSCSI]] / 전통 [[493_san_storage_area_network|SAN]] |
| :-- | :-- | :-- | :-- |
| 접근 위치 | 서버 내부 | 원격 패브릭 너머 | 원격 네트워크 |
| 명령 체계 | [[482_nvme|NVMe]] | [[482_nvme|NVMe]] | 주로 SCSI |
| [[015_지연_데이터_관점|지연]]시간 | 가장 낮음 | 낮음 | 상대적으로 높음 |
| 자원 공유 | 낮음 | 높음 | 높음 |
| 대표 강점 | 단순성과 최고 [[282_performance_tactics|성능]] | 공유 + 고성능 균형 | 범용성, 기존 운영 경험 |

이 차이는 단순 속도 비교를 넘어 인프라 철학을 바꾼다. 로컬 [[482_nvme|NVMe]] 중심 구조는 "서버 하나가 계산과 저장을 함께 가진다"는 결합형 모델에 가깝고, [[482_nvme|NVMe]]-oF는 계산 노드와 저장 노드를 분리하는 디스애그리게이션 (Disaggregation)과 컴포저블 인프라 (Composable Infrastructure)를 가능하게 한다. 그래서 [[482_nvme|NVMe]]-oF는 스토리지 기술이면서 동시에 클라우드 아키텍처 기술이기도 하다.

다른 과목과 연결하면, [[001_operating_system_purpose|운영체제]] 측면에서는 멀티큐 I/O 스케줄링과 [[016_interrupt_mechanism|인터럽트]] 처리 부담이 연결되고, 네트워크 측면에서는 ECN (Explicit Congestion Notification)·PFC (Priority [[421_tcp_flow_control_sliding_window_algorithm|Flow Control]]) 같은 혼잡 제어가 중요해진다. 또한 [[002_database_definition|데이터베이스]] 관점에서는 [[568_logs_distributed_logging_elk_fluentd|로그]] 디바이스 [[015_지연_데이터_관점|지연]]시간, [[015_virtualization|가상화]] 관점에서는 라이브 마이그레이션과 공유 스토리지 [[268_strategy_pattern|전략]], [[231_ai_turing_test|인공지능]] 관점에서는 고속 학습 [[001_dikw_pyramid|데이터]] 공급 경로와 바로 맞닿는다.

- **📢 섹션 요약 비유**: 로컬 NVMe는 집 안 금고이고, NAS는 공동 문서함이며, [[482_nvme|NVMe]]-oF는 은행 금고를 내 방 스위치처럼 즉시 여닫게 만드는 구조다. 어디에 둘지보다, 얼마나 빨리 그리고 몇 사람이 함께 써야 하는지가 선택 기준이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[482_nvme|NVMe]]-oF를 채택할지는 "최고 속도"보다 "어떤 병목을 어디로 옮길 것인가"를 기준으로 판단해야 한다. 서버별 [[327_ssd|SSD]] 고립으로 자원 낭비가 심하고, [[002_database_definition|데이터베이스]]·[[015_virtualization|가상화]]·[[190_ai_llm_requirements_specification|AI]] 워크로드처럼 고성능 블록 스토리지가 필요하다면 [[482_nvme|NVMe]]-oF의 도입 명분이 크다. 반대로 소규모 환경이거나 네트워크 운영 역량이 부족한 조직이라면, 단순 로컬 [[482_nvme|NVMe]] 또는 [[482_nvme|NVMe]]/TCP가 더 현실적일 수 있다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. **워크로드 특성**: 수십 마이크로초 수준의 추가 [[015_지연_데이터_관점|지연]]을 감당할 수 있는가, 아니면 절대적으로 로컬 디스크가 필요한가?
2. **네트워크 준비도**: 25/100GbE 이상 [[140_bandwidth|대역폭]], 혼잡 제어, [[500_multipath_io|이중 경로]], 장애 분리 설계가 준비되어 있는가?
3. **고가용성 설계**: 멀티패스, 타깃 [[456_dual_redundancy|이중화]], [[061_namespace|네임스페이스]] 페일오버를 운영할 수 있는가?
4. **운영 단순성**: 최고 [[282_performance_tactics|성능]]이 목적이라도 [[523_roce|RoCE]] 운영 부담이 크면 [[482_nvme|NVMe]]/TCP가 더 적합하지 않은가?

### 대표 적용 시나리오

- **[[015_virtualization|가상화]] 클러스터**: 여러 하이퍼바이저가 동일한 고성능 블록 스토리지를 공유해야 할 때, [[598_vm_migration_nic|VM]] ([[598_vm_migration_nic|Virtual Machine]]) 이동성과 스토리지 일관성을 함께 확보할 수 있다.
- **고성능 [[002_database_definition|데이터베이스]]**: [[568_logs_distributed_logging_elk_fluentd|로그]]·[[154_database_index_b_tree_search_optimization|인덱스]]·체크포인트 I/O가 많은 환경에서 공유 스토리지를 유지하면서도 [[015_지연_데이터_관점|지연]]시간 상승을 최소화할 수 있다.
- **[[190_ai_llm_requirements_specification|AI]]/분석 인프라**: 계산 노드는 디스크리스 (Diskless)로 두고, JBOF (Just a Bunch Of Flash) 같은 대규모 플래시 풀을 통해 필요한 [[001_dikw_pyramid|데이터]]만 고속 공급할 수 있다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- RDMA의 의미를 이해하지 못한 채 일반 네트워크에 [[482_nvme|NVMe]]/RoCE만 얹고 [[282_performance_tactics|성능]] 문제를 스토리지 탓으로 돌리는 경우
- 멀티패스 없이 단일 경로로 연결해 패브릭 장애를 그대로 [[090_service_kubernetes_network_load_balancing|서비스]] 장애로 확대하는 경우
- 소규모 [[090_service_kubernetes_network_load_balancing|서비스]]에도 무리하게 전용 [[696_fibre_channel_protocol|FC]]-NVMe를 도입해 운영비와 복잡도만 키우는 경우

시험 답안이나 설계 면접에서는 "왜 [[482_nvme|NVMe]]-oF인가"와 함께 "왜 지금은 [[482_nvme|NVMe]]/TCP가 더 현실적인가"를 같이 말할 수 있어야 한다. 기술사는 최첨단 기술을 외우는 사람보다, 조직의 성숙도와 장애 비용까지 고려해 적절한 계층을 고르는 사람에 가깝기 때문이다.

- **📢 섹션 요약 비유**: [[148_5g_embb_urllc_mmtc|초고속]] 철도를 깔면 분명 빨라지지만, 역·[[130_signal|신호]]·복선 운영 체계가 없으면 사고만 커진다. [[482_nvme|NVMe]]-oF도 마찬가지로, 선로만 빠르다고 끝나는 기술이 아니라 운영 체계까지 함께 설계해야 하는 기술이다.

---

## Ⅴ. 기대효과 및 결론

[[482_nvme|NVMe]]-oF의 가장 큰 효과는 저장장치를 서버 부품이 아니라 **공유 가능한 [[282_performance_tactics|성능]] 자원**으로 바꾼다는 점이다. 이를 통해 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]는 스토리지 [[285_pooling_layer|풀링]], 컴퓨트-스토리지 분리, 유연한 증설, 장애 시 빠른 재배치를 구현할 수 있다. 결과적으로 자원 활용률이 높아지고, 특정 서버에 SSD를 과잉 장착하던 구조에서 벗어나 총소유비용 ([[016_tco|TCO]], Total Cost of Ownership) 절감 효과도 기대할 수 있다.

다만 전제조건도 분명하다. 패브릭이 불안정하면 로컬 NVMe보다 나쁜 경험이 될 수 있고, 특히 [[639_rdma_kernel_bypass|RDMA]] 계열은 [[282_performance_tactics|성능]] 이점만큼 운영 난도도 동반한다. 또한 원격 스토리지인 이상, 물리적으로 완전한 로컬 장치와 동일한 [[015_지연_데이터_관점|지연]]을 보장하는 것은 아니므로 초저지연 [[191_transaction_concept_states|트랜잭션]] 일부에는 여전히 로컬 장치가 적합하다.

앞으로는 [[482_nvme|NVMe]]/TCP의 보급 확산, 스토리지 소프트웨어 정의화, [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) 기반 메모리·스토리지 분리와의 결합이 중요한 확장 방향이 될 가능성이 크다. 따라서 [[482_nvme|NVMe]]-oF는 "원격 디스크"가 아니라, **고성능 스토리지를 네트워크 자원으로 승격시키는 기술**로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 발전소를 집마다 두는 대신 국가 전력망으로 묶듯이, [[482_nvme|NVMe]]-oF는 저장장치를 네트워크 기반 공용 인프라로 바꾸는 발상이다. 다만 전력망이 튼튼해야 집이 밝듯이, 패브릭이 튼튼해야 비로소 로컬급 경험이 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]]) | [[482_nvme|NVMe]]-oF가 그대로 확장하는 명령 체계이자 멀티큐 기반 고속 저장 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| [[356_pcie|PCIe]] ([[355_pci|Peripheral Component Interconnect]] Express) | 원래 NVMe가 로컬 장치로 연결되던 물리적 기반이며, [[482_nvme|NVMe]]-oF는 이 경계를 패브릭 바깥으로 넓힌다 |
| [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]) | [[022_kernel_role|커널]] 우회와 낮은 CPU 개입을 통해 [[482_nvme|NVMe]]-oF의 저지연 전송을 뒷받침하는 핵심 기술 |
| [[493_san_storage_area_network|SAN]] ([[493_san_storage_area_network|Storage Area Network]]) | 공유 스토리지의 전통적 형태이며, [[482_nvme|NVMe]]-oF는 이를 더 낮은 [[015_지연_데이터_관점|지연]]과 높은 [[430_index_fast_full_scan|병렬]]성으로 재해석한다 |
| 컴포저블 인프라 (Composable Infrastructure) | 계산·저장 자원을 분리하고 필요할 때 조합하는 현대 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 운영 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
SCSI 기반 공유 스토리지
    │
    ▼
로컬 NVMe (Non-Volatile Memory Express)
    │
    ▼
NVMe-oF (NVMe over Fabrics)
    │
    ├─▶ FC-NVMe (Fibre Channel NVMe)
    ├─▶ NVMe/RoCE (RDMA over Converged Ethernet)
    └─▶ NVMe/TCP (NVMe over TCP)
    │
    ▼
디스애그리게이션 · 컴포저블 인프라 · 디스크리스 서버
```

이 흐름은 저장장치가 "개별 서버 부품"에서 "공유 가능한 네트워크 [[282_performance_tactics|성능]] 자원"으로 진화하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예전에는 빠른 장난감 상자를 내 방 안에 꼭 두어야만 빨리 꺼낼 수 있었어요.
2. [[482_nvme|NVMe]]-oF는 그 상자를 복도 끝 큰 창고에 두더라도, 비밀 고속 레일로 내 책상까지 바로 가져오게 해 주는 기술이에요.
3. 그래서 친구들과 창고를 같이 쓰면서도, 내 방 안 상자처럼 빠르게 장난감을 꺼낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 344 / 803

← **이전**: [[342_nvme|342. NVMe (Non-Volatile Memory Express)]]
**다음**: [[344_bus|344. 버스 (Bus)]] →

---
