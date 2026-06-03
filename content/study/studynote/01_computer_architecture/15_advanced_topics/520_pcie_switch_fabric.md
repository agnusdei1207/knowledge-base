+++
weight = 520
title = "520. PCIe 스위치 패브릭 (PCIe Switch Fabric)"
date = "2026-05-08"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[356_pcie|PCIe]] ([[355_pci|Peripheral Component Interconnect]] Express) [[238_switch_operation_principles|스위치]] 패브릭은 제한된 루트 컴플렉스 ([[358_root_complex|Root Complex]]) 레인을 패킷 스위칭 구조로 분기해, 더 많은 [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]])·[[327_ssd|SSD]] ([[327_ssd|Solid State Drive]])·[[587_nic_offloading|NIC]] (Network Interface Card)를 하나의 I/O 토폴로지 안에 붙이게 만드는 확장용 내부 네트워크다.
> 2. **가치**: 잘 설계된 [[238_switch_operation_principles|스위치]] 패브릭은 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] ([[916_p2p_peer_to_peer_networking_super_node_gnutella|Peer-to-Peer]]) DMA를 통해 장치 간 [[001_dikw_pyramid|데이터]]를 CPU (Central Processing Unit) 복사 없이 직접 흐르게 하고, 멀티호스트와 자원 [[285_pooling_layer|풀링]]을 지원해 [[231_ai_turing_test|인공지능]] ([[190_ai_llm_requirements_specification|AI]])·고성능 컴퓨팅 ([[548_automotive_hpc|HPC]])·스토리지 시스템의 활용도를 크게 높인다.
> 3. **판단 포인트**: [[238_switch_operation_principles|스위치]]는 [[446_port_and_bus|포트]] 수를 늘려 주지만 업스트림 [[140_bandwidth|대역폭]]을 새로 만들지는 않으므로, 오버서브스크립션, 홉 [[015_지연_데이터_관점|지연]], ACS ([[547_access_control_rwx|Access Control]] Services) [[164_policy|정책]], 오류 격리, 전력·발열까지 함께 설계해야 진짜 [[282_performance_tactics|성능]]이 나온다.

---

## Ⅰ. 개요 및 필요성

[[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭은 점대점 링크로 설계된 PCIe를 더 큰 장치 집합으로 확장하기 위한 구조다. CPU (Central Processing Unit)나 [[131_soc|SoC]] ([[131_soc|System on Chip]])가 제공하는 [[356_pcie|PCIe]] 레인 수는 한정돼 있으므로, 직접 연결만으로는 대량의 [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]]) [[327_ssd|SSD]], 여러 장의 [[418_gpu|GPU]], 고속 NIC를 모두 붙이기 어렵다. 특히 [[190_ai_llm_requirements_specification|AI]] 서버, JBOF (Just a Bunch of Flash), 가속기 섀시처럼 장치 수가 CPU [[446_port_and_bus|포트]] 수를 쉽게 넘는 환경에서는 단순 bifurcation만으로 해결되지 않는다.

여기서 [[238_switch_operation_principles|스위치]]의 역할은 단순한 분배기가 아니다. [[356_pcie|PCIe]] [[191_transaction_concept_states|트랜잭션]] 계층 패킷을 읽고 적절한 다운스트림 [[446_port_and_bus|포트]]로 전달하며, 같은 [[238_switch_operation_principles|스위치]] 아래에 있는 장치끼리는 상위 루트 컴플렉스를 거치지 않고 서로 [[120_direct_communication|직접 통신]]하게 만들 수 있다. 그래서 [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭은 "[[446_port_and_bus|포트]]를 늘리는 부품"이면서 동시에 **I/O [[001_dikw_pyramid|데이터]] 경로를 재설계하는 토폴로지 장치**다.

이 구조가 중요해진 배경은 두 가지다. 첫째, 장치 수와 장치당 [[140_bandwidth|대역폭]] 요구가 동시에 커졌다. 둘째, [[418_gpu|GPU]] ↔ [[418_gpu|GPU]], [[418_gpu|GPU]] ↔ [[327_ssd|SSD]], [[587_nic_offloading|NIC]] ↔ GPU처럼 CPU보다 장치끼리 주고받는 동서(East-West) 트래픽이 늘었다. 따라서 [[238_switch_operation_principles|스위치]] 패브릭은 단순 확장이 아니라, [[001_dikw_pyramid|데이터]]가 CPU 중심에서 장치 중심으로 흐르는 환경에 맞춘 해법이다.

- **📢 섹션 요약 비유**: [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭은 집 안의 멀티탭이 아니라, 대형 건물의 배전반에 가깝다. 콘센트 수만 늘리는 것이 아니라 어느 층에 얼마나 전력을 보낼지 구조 자체를 다시 짜는 장치다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]]는 업스트림 [[446_port_and_bus|포트]], 여러 개의 다운스트림 [[446_port_and_bus|포트]], 내부 크로스바, 버퍼, [[213_flow_control_buffer_overflow|흐름 제어]] 로직으로 구성된다. 호스트에서 내려온 [[385_tlp|TLP]] ([[191_transaction_concept_states|Transaction]] Layer Packet)를 주소와 ID에 따라 올바른 [[446_port_and_bus|포트]]로 [[339_routing_overview_best_path_selection|라우팅]]하고, 필요하면 같은 [[238_switch_operation_principles|스위치]] 안에서 장치 간 트래픽을 로컬로 처리한다. 구현에 따라 cut-through에 가까운 빠른 전달을 하기도 하고, store-and-forward처럼 좀 더 보수적으로 버퍼링한 뒤 전달하기도 한다.

이 그림은 [[238_switch_operation_principles|스위치]]가 [[446_port_and_bus|포트]] 수를 늘리는 동시에, 어디서 병목이 생길 수 있는지를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│      switch fabric는 fan-out과 local routing을 주지만 uplink는 유한 │
├──────────────────────────────────────────────────────────────────────┤
│ Host / Root Complex  x16                                             │
│          │                                                           │
│          ▼                                                           │
│   [ Upstream Port ]                                                  │
│          │                                                           │
│   ┌──────┴───────────────────────────────────────────────────────┐    │
│   │                    PCIe Switch Fabric                         │    │
│   │  crossbar + buffers + arbitration                             │    │
│   ├───────────────┬───────────────────┬───────────────────────────┤    │
│   │ Down x16      │ Down x16          │ Down x4                   │    │
│   ▼               ▼                   ▼                           │    │
│ GPU0  ◀── P2P ─▶  GPU1             NVMe SSD                       │    │
│   │                                                    multi-host │    │
│   └───────────────────────── local switching ─────────────────────┘    │
│                                                                      │
│ aggregate hot traffic > x16 uplink  → oversubscription bottleneck    │
└──────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 시 보는 포인트 |
| :--- | :--- | :--- |
| Upstream [[446_port_and_bus|Port]] | 호스트와 연결되는 상향 링크 | 전체 시스템의 최종 병목이 되기 쉬움 |
| Downstream [[446_port_and_bus|Port]] | 장치 또는 하위 [[238_switch_operation_principles|스위치]] 연결 | 장치별 요구 [[140_bandwidth|대역폭]]과 [[446_port_and_bus|포트]] 폭 매칭 필요 |
| 내부 크로스바 / 버퍼 | [[446_port_and_bus|포트]] 간 패킷 중재와 전달 | 혼잡 시 [[015_지연_데이터_관점|지연]]과 [[456_quic_hol_head_of_line_blocking_resolution|head-of-line]] [[122_sync_async_communication|blocking]] 최소화 |
| [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 경로 | 같은 패브릭 내 장치 간 [[120_direct_communication|직접 통신]] | CPU 메모리 왕복 감소, 소프트웨어 지원 필요 |
| NTB (Non-Transparent [[260_bridge_pattern_abstraction_implementation|Bridge]]) / 멀티호스트 | 서로 다른 호스트를 분리 연결 | 주소 공간 격리, 장애 전파 범위 관리 필요 |

따라서 [[238_switch_operation_principles|스위치]] 패브릭의 핵심은 "링크를 더 만든다"가 아니라, **어떤 트래픽은 로컬에서 돌리고 어떤 트래픽만 상위로 올릴지 결정하는 [[339_routing_overview_best_path_selection|라우팅]] 구조**에 있다. 이 때문에 [[238_switch_operation_principles|스위치]] [[282_performance_tactics|성능]]은 단순 [[446_port_and_bus|포트]] 수보다 내부 중재 [[164_policy|정책]]과 실제 트래픽 행렬에 더 크게 좌우된다.

- **📢 섹션 요약 비유**: [[238_switch_operation_principles|스위치]] 패브릭은 입체 교차로와 같다. 길이 많다고 다 빨라지는 것이 아니라, 어디서 바로 빠지고 어디서 합류하는지가 교통 흐름을 결정한다.

---

## Ⅲ. 비교 및 연결

[[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭은 lane bifurcation과 자주 혼동되지만 성격이 다르다. bifurcation은 CPU가 가진 x16 레인을 x8+x8 또는 x4+x4+x4+x4처럼 **정적으로 쪼개는 것**이고, [[238_switch_operation_principles|스위치]]는 들어온 트래픽을 **패킷 단위로 중재하고 [[339_routing_overview_best_path_selection|라우팅]]하는 것**이다. 즉 bifurcation은 배선을 나누는 기술이고, [[238_switch_operation_principles|스위치]]는 토폴로지를 확장하는 기술이다.

| 방식 | 장점 | 약점 | 잘 맞는 환경 |
| :--- | :--- | :--- | :--- |
| 직접 연결 / bifurcation | 가장 낮은 [[015_지연_데이터_관점|지연]], 구조 단순 | CPU 레인 수만큼만 확장 가능 | [[015_지연_데이터_관점|지연]] 민감 장치, 소규모 서버 |
| [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭 | [[446_port_and_bus|포트]] 수 확대, 로컬 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]], 멀티호스트 가능 | 홉 [[015_지연_데이터_관점|지연]]과 오버서브스크립션 관리 필요 | [[418_gpu|GPU]] 확장, [[482_nvme|NVMe]] 박스, 가속기 섀시 |
| [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) [[238_switch_operation_principles|스위치]] / 외부 패브릭 | [[442_memory_pooling|메모리 풀링]]·coherence 확장 가능 | 제어 복잡도와 비용 증가 | 차세대 composable infrastructure |

여기서 중요한 연결 개념이 ACS다. 보안과 격리를 위해 ACS redirect를 강하게 켜면, 장치 간 트래픽이 [[238_switch_operation_principles|스위치]] 내부에서 바로 가지 못하고 상위 루트 컴플렉스로 우회할 수 있다. 즉 "P2P를 지원하는 [[238_switch_operation_principles|스위치]]"가 있어도 [[032_firmware|펌웨어]], [[001_operating_system_purpose|운영체제]], [[627_iommu_dma_isolation|IOMMU]] [[164_policy|정책]]이 이를 막으면 기대한 [[001_dikw_pyramid|데이터]] 경로가 나오지 않는다.

또한 [[238_switch_operation_principles|스위치]] 패브릭은 NTB, GPUDirect, [[499_nvme_over_fabrics|NVMe-oF]] ([[499_nvme_over_fabrics|NVMe over Fabrics]]) 대상 장치 박스, 스토리지 풀과도 이어진다. 하나의 호스트 안에서만 쓰는 장치 허브가 아니라, 멀티호스트 자원 분리와 장치 공유, 서비스형 가속기 인프라를 만드는 기반으로 확장되기 때문이다.

- **📢 섹션 요약 비유**: bifurcation이 한 도로를 여러 갈래로 나누는 분기점이라면, [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]]는 신호등과 우회로까지 갖춘 교차로다. 차선만 늘어나는 것과 교통을 통제하는 것은 전혀 다른 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭 설계의 핵심은 장치 목록이 아니라 트래픽 행렬이다. 예를 들어 GPU가 주로 CPU 메모리와 통신하는지, GPU끼리 [[120_direct_communication|직접 통신]]하는지, NVMe가 동시에 풀 스루풋으로 읽히는지에 따라 최적 [[446_port_and_bus|포트]] 배치가 달라진다. [[238_switch_operation_principles|스위치]]는 [[446_port_and_bus|포트]] 수를 늘려 주지만, 업스트림 x16 하나에 고대역 장치 여러 개를 붙이면 결국 위쪽 링크가 병목이 된다.

또한 P2P가 중요하다면 [[032_firmware|펌웨어]] 옵션, ACS, [[627_iommu_dma_isolation|IOMMU]] [[009_config|설정]], [[001_operating_system_purpose|운영체제]] 드라이버 지원을 함께 확인해야 한다. 하드웨어만 보고 "[[238_switch_operation_principles|스위치]]가 있으니 GPU와 NVMe가 [[120_direct_communication|직접 통신]]하겠지"라고 가정하면 안 된다. 실제로는 보안 [[164_policy|정책]]이나 주소 해석 문제 때문에 상위 루트로 우회되거나, 일부 조합에서는 아예 P2P가 제한될 수 있다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. 장치 간 실제 hot path가 무엇인지, CPU 경유 트래픽과 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 트래픽 비율을 파악했는가?
2. 업스트림 대비 다운스트림의 동시 최대 수요를 계산해 오버서브스크립션 비율을 확인했는가?
3. 홉 수가 늘어날 때 [[015_지연_데이터_관점|지연]] 민감 장치의 tail latency가 허용 범위 안에 있는가?
4. ACS, [[627_iommu_dma_isolation|IOMMU]], 리셋 [[064_relation_domain|도메인]], AER ([[716_pcie_aer|Advanced Error Reporting]]) [[009_config|설정]]이 원하는 격리 [[164_policy|정책]]과 일치하는가?
5. [[238_switch_operation_principles|스위치]] 칩 전력, 방열, 케이블 길이, hot-plug 운영까지 포함해 시스템 수준으로 검토했는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[238_switch_operation_principles|스위치]]가 있으니 CPU 업스트림 [[140_bandwidth|대역폭]] 한계도 사라진다고 오해하는 설계
- [[015_지연_데이터_관점|지연]] 민감 [[418_gpu|GPU]] 군집을 깊은 [[238_switch_operation_principles|스위치]] 체인 뒤에 배치하는 토폴로지
- ACS redirect를 강하게 켜 둔 채 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] [[746_io_direct_memory_access_dma|DMA]] [[282_performance_tactics|성능]] 저하 원인을 소프트웨어 탓으로만 돌리는 운영

- **📢 섹션 요약 비유**: [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭 설계는 쇼핑몰 주차장 출입구를 짜는 일과 같다. 주차면이 많아도 출입구가 좁고 동선이 꼬이면 차는 결국 한곳에 몰린다.

---

## Ⅴ. 기대효과 및 결론

[[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭을 제대로 설계하면 같은 CPU 레인 자원으로 더 많은 장치를 붙이고, 장치 간 [[120_direct_communication|직접 통신]]을 활성화하며, 가속기와 스토리지를 더 유연하게 [[285_pooling_layer|풀링]]할 수 있다. 그래서 [[190_ai_llm_requirements_specification|AI]] 학습 노드, 스토리지 확장 섀시, 멀티호스트 가속기 박스에서 시스템 활용도가 크게 오른다. 특히 CPU 메모리를 우회하는 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 경로가 잘 살아나면, 복사 오버헤드와 루트 컴플렉스 부담이 함께 줄어든다.

반대로 잘못 설계하면 [[238_switch_operation_principles|스위치]]는 단순한 병목 증폭기로 바뀐다. [[446_port_and_bus|포트]] 수는 많아 보이는데 업링크가 막히고, 홉 [[015_지연_데이터_관점|지연]]이 누적되고, 리셋이나 오류가 넓게 번져 운영성이 떨어질 수 있다. 앞으로는 [[356_pcie|PCIe]] 6.0 이후 세대, 케이블 기반 외부 패브릭, [[441_cxl|CXL]] 스위칭과의 결합을 통해 더 큰 규모의 composable infrastructure로 확장되겠지만, 기본 원리는 여전히 같다. **토폴로지를 잘 짜야 [[282_performance_tactics|성능]]이 나온다.**

결론적으로 [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭은 단순한 멀티포트 허브가 아니라, **장치 수·[[140_bandwidth|대역폭]]·[[015_지연_데이터_관점|지연]]·격리를 동시에 설계하는 I/O 토폴로지 엔진**이다. 이 개념은 "[[446_port_and_bus|포트]] 확장"보다 "[[001_dikw_pyramid|데이터]]가 어디로 어떻게 흐르는가를 설계하는 기술"로 기억해야 정확하다.

- **📢 섹션 요약 비유**: [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭은 도시의 고속도로 인터체인지와 같다. 길을 많이 내는 것보다, 어떤 차를 어디로 우회시킬지 잘 설계할 때 도시 전체가 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[358_root_complex|Root Complex]] | [[238_switch_operation_principles|스위치]] 패브릭이 결국 연결되는 상위 호스트 I/O 출발점이다. |
| Lane Bifurcation | [[238_switch_operation_principles|스위치]]와 자주 혼동되지만, 정적 레인 분할이라는 점에서 성격이 다르다. |
| [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] [[746_io_direct_memory_access_dma|DMA]] | [[238_switch_operation_principles|스위치]] 패브릭이 제공하는 가장 중요한 [[001_dikw_pyramid|데이터]] 경로 최적화다. |
| ACS ([[547_access_control_rwx|Access Control]] Services) | 격리와 보안 [[164_policy|정책]]이 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 경로를 바꾸는 핵심 제어 기능이다. |
| NTB (Non-Transparent [[260_bridge_pattern_abstraction_implementation|Bridge]]) | 멀티호스트 연결과 자원 공유를 가능하게 하는 확장 요소다. |
| [[441_cxl|CXL]] [[238_switch_operation_principles|Switch]] | [[356_pcie|PCIe]] 물리층 위에서 메모리 coherence와 [[285_pooling_layer|풀링]]으로 확장되는 다음 단계다. |

### 📈 관련 키워드 및 발전 흐름도

```text
직접 연결 PCIe 장치
        │
        ▼
lane bifurcation 기반 정적 분기
        │
        ▼
PCIe 스위치 패브릭
        │
        ├─▶ P2P DMA
        ├─▶ 멀티호스트 / NTB
        ├─▶ JBOF · GPU expansion chassis
        │
        ▼
CXL switch · composable infrastructure · 외부 패브릭 확장
```

이 흐름은 "[[446_port_and_bus|포트]]를 나누는 수준"에서 출발해, "장치 간 경로와 자원 풀을 설계하는 수준"으로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]]는 컴퓨터 안에 더 많은 길을 만들어 주는 교통 정리 센터예요.
2. 친구들끼리 물건을 주고받을 때 꼭 선생님 책상을 거치지 않아도 되게 도와줘요.
3. 하지만 큰길 하나가 너무 좁으면 아무리 갈래길이 많아도 결국 그곳에서 막히기 때문에 길 배치를 잘해야 해요.
