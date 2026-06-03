+++
weight = 362
title = "362. RDMA (Remote Direct Memory Access)"
date = "2026-03-27"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]])는 원격 서버의 메모리에 네트워크를 통해 직접 읽기·쓰기를 수행하게 해, [[001_dikw_pyramid|데이터]] 이동 경로에서 CPU (Central Processing Unit)와 OS ([[001_operating_system_purpose|Operating System]]) [[022_kernel_role|커널]]의 개입을 크게 줄이는 통신 방식이다.
> 2. **가치**: 핵심 효과는 [[022_kernel_role|Kernel]] Bypass와 Zero-Copy에 있다. 즉, [[141_latency|지연 시간]]은 수 마이크로초(μs) 수준으로 낮추고, CPU는 패킷 포장보다 실제 연산에 집중하게 만든다.
> 3. **판단 포인트**: RDMA는 "무조건 빠른 네트워크"가 아니라, 손실 제어·메모리 등록·전용 [[587_nic_offloading|NIC]] (Network Interface Card)·운영 복잡도를 감당할 수 있는 폐쇄형 고성능 환경에서 가장 큰 가치를 낸다.

---

## Ⅰ. 개요 및 필요성

[[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]])는 한 시스템의 메모리 영역을 다른 시스템이 네트워크를 통해 직접 읽거나 쓰도록 만드는 고성능 [[001_dikw_pyramid|데이터]] 전송 기술이다. 전통적인 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]]/Internet [[295_protocol_field_tcp_udp_icmp|Protocol]]) [[125_socket|소켓]] 통신은 애플리케이션 버퍼와 [[022_kernel_role|커널]] 버퍼 사이의 복사, [[295_protocol_field_tcp_udp_icmp|프로토콜]] 처리, [[016_interrupt_mechanism|인터럽트]] 처리, [[033_context|컨텍스트]] 스위칭을 반복하므로 [[140_bandwidth|대역폭]]이 커질수록 CPU 부담이 함께 증가한다. 반면 RDMA는 이 경로를 단축해, 네트워크가 빨라질수록 더 심각해지는 소프트웨어 병목을 하드웨어 [[440_offloading|오프로딩]]으로 완화한다.

이 기술이 중요해진 배경은 세 가지다. 첫째, 100 [[139_1000base_t_gigabit_ethernet|Gigabit Ethernet]] (100GbE)·200 [[139_1000base_t_gigabit_ethernet|Gigabit Ethernet]] (200GbE)급 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]([[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])과 [[361_infiniband|InfiniBand]] ([[361_infiniband|인피니밴드]]) 환경에서는 선로 속도보다 호스트 측 [[295_protocol_field_tcp_udp_icmp|프로토콜]] [[057_stack|스택]]이 먼저 병목이 된다. 둘째, [[136_variance|분산]] [[002_database_definition|데이터베이스]], 고빈도 트레이딩, [[231_ai_turing_test|인공지능]]([[001_artificial_intelligence|Artificial Intelligence]], [[190_ai_llm_requirements_specification|AI]]) 학습, [[499_nvme_over_fabrics|NVMe-oF]] ([[499_nvme_over_fabrics|NVMe over Fabrics]])처럼 작은 [[015_지연_데이터_관점|지연]] 증가도 전체 [[139_throughput|처리량]]을 크게 떨어뜨리는 워크로드가 늘었다. 셋째, 서버 한 대의 CPU 코어가 비싸질수록 "[[001_dikw_pyramid|데이터]]를 옮기는 일"과 "애플리케이션 계산"을 같은 코어가 함께 처리하는 구조가 비효율적이 되었다.

아래 그림은 RDMA가 줄이려는 병목의 위치를 보여준다. 핵심은 네트워크 자체보다도, 네트워크 앞뒤에 붙어 있는 복사와 [[022_kernel_role|커널]] 경로가 [[015_지연_데이터_관점|지연]]을 키운다는 점이다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                  전통적 소켓 I/O와 RDMA의 데이터 경로 비교                │
├───────────────────────────────┬────────────────────────────────────────────┤
│ 전통적 TCP/IP 소켓            │ RDMA 경로                                  │
├───────────────────────────────┼────────────────────────────────────────────┤
│ App Buffer                    │ App Buffer                                 │
│   │                           │   │                                        │
│   ├─ copy ─▶ Kernel Buffer    │   ├─ Memory Registration ─▶ RNIC           │
│   │            │              │   │                           │             │
│   │            ├─ TCP/IP 처리  │   │                           ├─ DMA 전송   │
│   │            ├─ 인터럽트     │   │                           │             │
│   │            └─ NIC 송신     │   │                           ▼             │
│   ▼                           │   ▼                    Remote Memory        │
│ Remote Socket Buffer          │ Completion Queue 로 완료 통지               │
└───────────────────────────────┴────────────────────────────────────────────┘
```

이 구조 차이 때문에 RDMA는 단순 전송 [[282_performance_tactics|성능]]보다 "호스트 개입 비용 제거"라는 관점으로 이해해야 한다. 즉, 빠른 것은 선로만이 아니라, [[001_dikw_pyramid|데이터]]를 만지는 소프트웨어 단계 수를 줄였기 때문이다.

- **📢 섹션 요약 비유**: 택배가 느린 이유가 고속도로 때문이 아니라 물건을 창고에 세 번 옮기고 결재를 두 번 받기 때문이라면, RDMA는 고속도로를 넓히기보다 창고와 결재 단계를 통째로 줄인 전용 출입증과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RDMA를 가능하게 하는 중심 부품은 RNIC ([[639_rdma_kernel_bypass|RDMA]] Network Interface Card)이다. 애플리케이션은 먼저 사용할 메모리를 등록해 RNIC가 접근 가능한 영역으로 고정하고, 그 뒤 QP ([[058_queue|Queue]] Pair)와 CQ (Completion [[058_queue|Queue]])를 통해 송수신 작업을 게시한다. 이후 RNIC는 [[746_io_direct_memory_access_dma|DMA]] ([[318_dma|Direct Memory Access]]) 엔진을 이용해 호스트 메모리에서 [[001_dikw_pyramid|데이터]]를 직접 읽거나 쓰고, 완료 사실만 큐를 통해 알려 준다.

동작 원리는 보통 다음 순서를 따른다.

1. **메모리 등록**: 전송할 버퍼를 미리 등록해 물리 주소를 고정하고 접근 권한을 [[009_config|설정]]한다.
2. **연결 준비**: 송신 측과 수신 측이 QP를 생성하고, 원격 메모리 키와 주소를 교환한다.
3. **작업 게시**: 애플리케이션이 Send/Receive 또는 Read/Write 요청을 Work Queue에 넣는다.
4. **하드웨어 처리**: RNIC가 패킷 분할, 전송, 재조립, 메모리 접근을 수행한다.
5. **완료 통지**: 끝난 작업은 CQ에 기록되어 애플리케이션이 [[448_polling_programmed_io|폴링]] 또는 이벤트 방식으로 [[396_validation|확인]]한다.

| 구성 요소 | 역할 | 설계 시 주의점 |
| :-- | :-- | :-- |
| RNIC | [[295_protocol_field_tcp_udp_icmp|프로토콜]] 처리와 [[746_io_direct_memory_access_dma|DMA]] 수행 | 일반 NIC보다 비싸고 기능 차이가 큼 |
| Memory Registration | 원격 접근 가능한 버퍼 준비 | 등록/해제 비용이 커서 재사용 설계 중요 |
| [[058_queue|Queue]] Pair | 송수신 요청 경로 | 큐 깊이 부족 시 [[139_throughput|처리량]] 급감 |
| Completion [[058_queue|Queue]] | 완료 여부 [[396_validation|확인]] | [[448_polling_programmed_io|폴링]] 과다 시 CPU 낭비 가능 |
| [[639_rdma_kernel_bypass|RDMA]] Read/Write | 원격 메모리 직접 접근 | 권한 키 관리와 [[212_synchronization_mechanisms|동기화]] 설계 필요 |

아래 [[103_ascii|ASCII]] 다이어그램은 one-sided 연산이 왜 CPU 개입을 줄이는지 보여준다. 송신 측 애플리케이션은 "어디를 읽고 어디에 쓸지"만 지정하고, 실제 메모리 복사는 RNIC끼리 처리한다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    RDMA Write / Read의 제어와 데이터 분리                │
├────────────────────────────────────────────────────────────────────────────┤
│ Client Host                  Network Fabric                 Server Host    │
│ ┌──────────────┐                                          ┌──────────────┐ │
│ │ App Process  │ -- Work Request ----------------------▶  │    RNIC      │ │
│ └──────┬───────┘                                          └──────┬───────┘ │
│        │                                                          │         │
│ ┌──────▼───────┐     DMA Read / Write Payload      ┌─────────────▼───────┐ │
│ │ Client RNIC  │ =================================▶│ Registered Memory    │ │
│ └──────┬───────┘                                   └─────────────────────┘ │
│        │                                                                  │
│        └──────────── Completion Queue 업데이트 ◀───────────────────────────┘
└────────────────────────────────────────────────────────────────────────────┘
```

핵심 트레이드오프도 분명하다. RDMA는 빠르지만, 그 속도는 메모리 등록·큐 관리·버퍼 생명주기·원격 권한 제어를 개발자가 더 엄격하게 다뤄야 한다는 뜻이다. 즉, 소프트웨어 복잡도를 줄여서 빨라지는 것이 아니라, 복잡도를 애플리케이션 설계와 네트워크 장비 [[009_config|설정]] 쪽으로 옮겨 [[282_performance_tactics|성능]]을 얻는 구조다.

- **📢 섹션 요약 비유**: RDMA는 기사에게 주소만 알려 주면 창고 출입증을 가진 전문 배송팀이 알아서 물건을 꺼내 놓는 시스템과 같다. 빠른 대신, 어떤 창고를 열어도 되는지 열쇠와 출입 명부를 아주 엄격하게 관리해야 한다.

---

## Ⅲ. 비교 및 연결

RDMA를 이해하려면 전통적 [[125_socket|소켓]] 통신, [[361_infiniband|InfiniBand]], [[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]), [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]] (Internet Wide Area [[639_rdma_kernel_bypass|RDMA]] [[295_protocol_field_tcp_udp_icmp|Protocol]])를 함께 봐야 경계가 선명해진다. 핵심 비교 축은 "[[282_performance_tactics|성능]]" 하나가 아니라, 손실 허용 방식, 네트워크 구축 비용, 운영 난이도, [[339_routing_overview_best_path_selection|라우팅]] 범위다.

| 항목 | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP [[125_socket|소켓]] | [[361_infiniband|InfiniBand]] | [[523_roce|RoCE]] v2 | [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]] |
| :-- | :-- | :-- | :-- | :-- |
| [[295_protocol_field_tcp_udp_icmp|프로토콜]] 경로 | [[022_kernel_role|커널]] 네트워크 [[057_stack|스택]] 중심 | [[639_rdma_kernel_bypass|RDMA]] 전용 패브릭 | [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 위 [[639_rdma_kernel_bypass|RDMA]] | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 위 [[639_rdma_kernel_bypass|RDMA]] |
| [[141_latency|지연 시간]] | 상대적으로 큼 | 가장 낮음 | 매우 낮음 | 낮지만 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 부담 존재 |
| 패킷 손실 대응 | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 재전송 | 패브릭 자체 제어 | [[845_lossless_ethernet_dcb_pfc_roce_fcoe|무손실 이더넷]] [[009_config|설정]] 중요 | TCP가 처리 |
| 운영 난이도 | 낮음 | 높음 | 높음 | 중간 |
| 대표 활용 | 범용 [[090_service_kubernetes_network_load_balancing|서비스]] | 고성능 컴퓨팅 ([[226_hpc_supercomputing_infrastructure|High Performance Computing]], [[548_automotive_hpc|HPC]]), 대형 [[190_ai_llm_requirements_specification|AI]] | 클라우드, 스토리지 | [[344_compatibility_usability|호환성]] 중시 환경 |

특히 InfiniBand와 RoCE는 RDMA의 대표 구현이지만 철학이 다르다. InfiniBand는 처음부터 RDMA를 위한 전용 패브릭이어서 [[015_지연_데이터_관점|지연]]과 일관성이 매우 우수하다. RoCE는 기존 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 인프라를 활용할 수 있다는 장점이 있으나, PFC (Priority [[421_tcp_flow_control_sliding_window_algorithm|Flow Control]])와 ECN (Explicit Congestion Notification) 같은 무손실 제어가 제대로 잡히지 않으면 혼잡 시 전체 [[282_performance_tactics|성능]]이 불안정해질 수 있다.

또한 RDMA는 컴퓨터구조의 [[746_io_direct_memory_access_dma|DMA]], 운영체제의 I/O [[440_offloading|오프로딩]], 네트워크의 혼잡 제어, 스토리지의 [[482_nvme|NVMe]]-oF와 직접 연결된다. 즉 "원격 메모리 직접 접근"이라는 이름이지만, 실제로는 메모리-[[344_bus|버스]]-네트워크-스토리지의 경계를 가로질러 병목을 줄이는 시스템적 기술이다.

- **📢 섹션 요약 비유**: 같은 급행 [[090_service_kubernetes_network_load_balancing|서비스]]라도 전용 철도([[361_infiniband|InfiniBand]]), 기존 도로 위 전용 차선([[523_roce|RoCE]]), 일반 도로 규칙을 다 지키는 고속 [[344_bus|버스]]([[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]])는 속도만이 아니라 관리 방법과 [[009_incident_response|사고 대응]] 방식이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 RDMA는 "도입하면 무조건 이득"인 기술이 아니다. 가장 적합한 곳은 동서(East-West) 트래픽이 많고, 같은 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 안에서 대량의 [[001_dikw_pyramid|데이터]]를 반복 교환하며, 마이크로초 단위 [[015_지연_데이터_관점|지연]] 차이가 전체 [[139_throughput|처리량]]에 직접 영향을 주는 환경이다. 대표 사례는 [[190_ai_llm_requirements_specification|AI]] [[136_variance|분산]] 학습의 All-Reduce 통신, 초저지연 캐시/메시지 시스템, [[499_nvme_over_fabrics|NVMe-oF]] 기반 스토리지 [[285_pooling_layer|풀링]], 고성능 [[002_database_definition|데이터베이스]] [[568_logs_distributed_logging_elk_fluentd|로그]] 복제다.

반대로 일반 웹 [[090_service_kubernetes_network_load_balancing|서비스]] 프런트엔드, 인터넷 구간이 섞인 불안정한 네트워크, 소규모 트래픽 중심 업무망에는 과도한 선택일 수 있다. RDMA는 네트워크가 조금만 흔들려도 [[282_performance_tactics|성능]] 편차가 커지고, 애플리케이션도 메모리 버퍼와 완료 큐를 세심하게 관리해야 하므로, 운영 조직과 개발 조직 모두가 준비되어 있어야 한다.

### 기술사 답안형 [[435_checklist_based_testing|체크리스트]]

1. **네트워크가 폐쇄형인가?** 외부 인터넷 구간이 섞이면 RDMA의 장점이 약해진다.
2. **패킷 손실을 충분히 제어하는가?** RoCE라면 PFC/ECN/버퍼 튜닝 검증이 선행되어야 한다.
3. **애플리케이션이 버퍼 재사용과 메모리 등록 비용을 흡수할 수 있는가?** 짧은 일회성 요청만 많으면 효과가 작다.
4. **CPU 절감분이 장비/운영 복잡도 증가분보다 큰가?** 비용 대비 효과를 계산해야 한다.
5. **보안 경계를 어떻게 둘 것인가?** 잘못된 메모리 키 관리나 권한 [[009_config|설정]]은 큰 사고로 이어진다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[639_rdma_kernel_bypass|RDMA]] 지원 NIC만 장착하고 [[238_switch_operation_principles|스위치]] 혼잡 제어나 무손실 [[009_config|설정]]을 생략하는 경우
- 작은 요청 위주의 범용 [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]) 서버에 RDMA를 억지로 붙여 개발 복잡도만 늘리는 경우
- 메모리 등록 비용을 고려하지 않고 버퍼를 요청마다 새로 등록·해제하는 경우

- **📢 섹션 요약 비유**: 포뮬러 원(F1) 경주차는 서킷에서는 압도적이지만, 과속방지턱과 신호등이 많은 일반 도로에서는 오히려 다루기 어렵다. RDMA도 준비된 트랙에서만 진가를 내는 장비다.

---

## Ⅴ. 기대효과 및 결론

RDMA의 가장 큰 효과는 CPU 절감, [[141_latency|지연 시간]] 단축, [[140_bandwidth|대역폭]] 활용률 향상이다. 같은 100Gbps 링크라도 [[125_socket|소켓]] 통신은 코어 여러 개를 네트워크 처리에 묶어 두는 반면, RDMA는 RNIC [[440_offloading|오프로딩]] 덕분에 애플리케이션 코어를 더 많이 남길 수 있다. 그래서 [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]]) 클러스터나 스토리지 패브릭처럼 "계산 장비가 기다리는 시간"이 큰 비용으로 환산되는 환경에서 투자 가치가 높다.

하지만 전제조건도 분명하다. 네트워크는 안정적으로 튜닝되어야 하고, 개발자는 메모리 등록과 완료 처리 모델을 이해해야 하며, 장애 분석도 [[125_socket|소켓]] 통신보다 어렵다. 다시 말해 RDMA는 단순한 가속 옵션이 아니라, 하드웨어·드라이버·[[238_switch_operation_principles|스위치]]·애플리케이션을 함께 설계해야 효과가 나는 전방위 최적화 기술이다.

앞으로는 GPUDirect [[639_rdma_kernel_bypass|RDMA]], [[499_nvme_over_fabrics|NVMe-oF]], SmartNIC/[[436_dpu|DPU]] ([[229_dpu_ipu_infrastructure_accelerator_offloading|Data Processing Unit]])와의 결합이 더 중요해질 가능성이 크다. 따라서 RDMA는 "멀리 있는 메모리를 빠르게 접근하는 기술"로만 외우기보다, "원격 [[001_dikw_pyramid|데이터]] 이동에서 호스트 소프트웨어 병목을 제거하는 시스템 설계 방식"으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: RDMA는 단순히 더 빠른 택배가 아니라, 공장 안 물류 동선을 다시 설계해 지게차와 결재 라인을 줄인 자동화 설비다. 설비를 제대로 깔면 생산성이 크게 오르지만, 설치와 운영은 훨씬 더 정교해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[746_io_direct_memory_access_dma|DMA]] ([[318_dma|Direct Memory Access]]) | RDMA의 출발점으로, 장치가 CPU 개입 없이 메모리에 접근하는 기본 원리 |
| [[022_kernel_role|Kernel]] Bypass | [[022_kernel_role|커널]] 네트워크 [[057_stack|스택]]을 우회해 [[141_latency|지연 시간]]과 CPU 오버헤드를 낮추는 핵심 메커니즘 |
| [[566_mmap_zero_copy_sendfile|Zero-Copy]] | 중간 버퍼 복사를 줄여 메모리 [[140_bandwidth|대역폭]] 낭비를 줄이는 설계 철학 |
| [[361_infiniband|InfiniBand]] | RDMA를 가장 전형적으로 구현한 전용 고성능 패브릭 |
| [[523_roce|RoCE]] v2 | [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 기반 RDMA의 대표 방식으로, [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 확장성과 비용 효율을 높임 |
| [[499_nvme_over_fabrics|NVMe-oF]] | RDMA를 이용해 원격 스토리지를 로컬 장치처럼 가깝게 만드는 응용 영역 |
| GPUDirect [[639_rdma_kernel_bypass|RDMA]] | CPU와 시스템 메모리를 우회해 [[418_gpu|GPU]] 메모리 간 전송 병목을 줄이는 확장 사례 |

### 📈 관련 키워드 및 발전 흐름도

```text
DMA (Direct Memory Access)
    │
    ▼
Kernel Bypass · Zero-Copy
    │
    ▼
RNIC · Queue Pair · Memory Registration
    │
    ▼
InfiniBand 기반 RDMA
    │
    ├──────────────▶ RoCE v2 (이더넷 확장)
    │
    └──────────────▶ iWARP (TCP 호환 확장)
                           │
                           ▼
NVMe-oF · GPUDirect RDMA · AI/HPC 패브릭
```

이 흐름은 "장치 [[746_io_direct_memory_access_dma|DMA]] 원리 → 호스트 개입 제거 → 전용 패브릭 → 범용 확장 → 스토리지·[[418_gpu|GPU]] 응용"으로 RDMA가 확장된 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. RDMA는 친구 집 서랍에 물건을 보낼 때 어른들을 여러 번 부르지 않고, 특별한 열쇠를 가진 배달 로봇이 바로 넣어 주는 방법이에요.
2. 그래서 물건이 훨씬 빨리 도착하고, 어른들은 배달 대신 다른 중요한 일을 할 수 있어요.
3. 하지만 아무 서랍이나 열면 안 되니까, 어떤 서랍을 열 수 있는지 약속과 열쇠 관리를 아주 정확하게 해야 해요.
