---
title: "Nic Offloading"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 587
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네트워크 인터페이스 카드 (Network Interface Card, NIC) [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 호스트의 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), OS)와 중앙처리장치 (Central Processing Unit, CPU)가 패킷마다 하던 반복 작업을 NIC 하드웨어로 넘겨, 일반 연산 코어가 네트워크 잡무 대신 본래 애플리케이션 일을 하게 만드는 기술이다.
> 2. **가치**: [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 계산, 세그먼트 분할, 수신 병합, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 완화, 흐름 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)을 NIC가 맡으면 초당 패킷 수가 많아도 라인 레이트에 가까운 처리량을 더 적은 CPU 코어로 달성할 수 있다.
> 3. **판단 포인트**: [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 대개 처리량에는 유리하지만, 패킷을 원형 그대로 봐야 하는 포워딩·보안 분석·정밀 디버깅 환경에서는 일부 기능이 오히려 가시성과 제어성을 떨어뜨릴 수 있다.

---

## Ⅰ. 개요 및 필요성

NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 네트워크 패킷 처리에서 반복적이고 규칙적인 일을 호스트 CPU 대신 NIC가 맡는 구조다. 기본 철학은 단순하다. 패킷마다 똑같이 반복되는 계산과 큐잉, 일부 헤더 조작은 범용 코어보다 전용 하드웨어가 더 싸고 일정하게 처리할 수 있다는 것이다. 그래서 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 CPU 성능을 대체한다기보다, <strong>CPU가 애플리케이션에 써야 할 시간을 되찾아 주는 역할</strong>에 가깝다.

이 기술이 중요해진 이유는 네트워크 속도와 패킷 수가 CPU 성장 속도보다 더 가파르게 늘었기 때문이다. 10기가비트 이더넷을 넘어 25기가비트, 100기가비트급 환경에서는 작은 패킷이 쏟아질 때 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/), [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 계산, 분할·병합 오버헤드가 먼저 CPU를 붙잡는다. 이런 환경에서 문제는 "회선 속도"가 아니라, <strong>그 속도로 들어오는 패킷을 <a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>가 얼마나 자주 깨워서 처리해야 하느냐</strong>다.

이 그림은 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 없을 때 CPU가 어디에 시간을 쓰는지 요약한다.

```text
+----------------------------------------------------------------------------+
|             Offload가 없으면 패킷마다 CPU가 여러 번 개입한다              |
+----------------------------------------------------------------------------+
| Packet -> Interrupt -> Kernel Parse -> Checksum -> Segment/Merge          |
|        -> Application                                                     |
|                                                                            |
| 패킷 수가 커질수록 CPU 시간의 상당 부분이 "네트워크 housekeeping"에 묶인다.|
+----------------------------------------------------------------------------+
```

따라서 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 단순한 편의 기능이 아니다. 고속 네트워크 시대에 소프트웨어 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)만으로는 감당하기 어려운 per-packet 비용을 낮추는, 사실상 필수적인 시스템 균형 장치다.

- **📢 섹션 요약 비유**: 택배가 폭주하는 창고에서 사장이 주문서 정리, 포장, 분류를 직접 하면 금방 지친다. NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 그 반복 업무를 자동 분류기와 포장기로 넘겨 사장이 진짜 중요한 결정만 하게 만드는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 동작하려면 호스트와 NIC 사이의 역할 분담이 분명해야 한다. 호스트는 보통 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) 처리, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 버퍼 소유권, 애플리케이션 인터페이스를 맡고, NIC는 디스크립터 링과 [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/), [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/))을 기반으로 실제 패킷 가공을 맡는다. 특히 전송 제어 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([Transmission Control Protocol](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/), [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 기반 대형 전송에서는 분할과 [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 계산의 이득이 크다. 즉 제어는 호스트가, 반복적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로는 NIC가 담당하는 식이다.

| 기능 | NIC가 하는 일 | 직접적인 효과 | 주의할 점 |
| :--- | :--- | :--- | :--- |
| [Checksum](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) Offload | 송신 [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 수신 [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | CPU 산술 부담 감소 | 캡처 도구가 보는 패킷과 wire packet이 다를 수 있음 |
| [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/) Offload (TSO) | 큰 버퍼를 전송 단위로 잘라 헤더를 붙임 | 송신 측 per-packet 오버헤드 감소 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)보다 처리량에 더 유리 |
| Large Receive Offload (LRO) | 수신 패킷을 더 큰 블록으로 합침 | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 수신 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 부담 감소 | 포워딩 장비나 패킷 분석에는 부적합할 수 있음 |
| Receive Side Scaling (RSS) | 흐름 해시로 여러 수신 큐와 코어에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | 단일 코어 병목 완화 | 큐-코어 매핑이 어긋나면 캐시 locality 저하 |
| [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Coalescing | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 묶어서 보고 | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭풍 완화 | 과하면 tail [latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 증가 |

아래 그림은 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 송수신 경로에서 어디에 개입하는지 보여 준다.

```text
+----------------------------------------------------------------------------+
|             NIC offload datapath: control on host, repetition on NIC      |
+----------------------------------------------------------------------------+
| Application -> OS Stack -> DMA Descriptor Ring -> [NIC Offload Engine]    |
|                                          |                                 |
|                                          +- checksum / segmentation        |
|                                          +- receive merge                  |
|                                          +- queue steering                 |
|                                          v                                 |
|                                         Wire                               |
|                                                                            |
| Wire -> [NIC Parser / Receive Queue] -> DMA -> selected CPU core          |
|                                         -> Application                     |
+----------------------------------------------------------------------------+
```

여기서 중요한 것은 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 모두 같은 급이 아니라는 점이다. [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/), TSO, RSS는 비교적 <strong>비상태성 (<a href="/studynote/15_devops_sre/05_devsecops/239_stateless_redis/">Stateless</a>)</strong> [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이고, 연결 상태를 오래 기억하지 않는다. 반면 수신 병합이나 이후의 [TOE](/studynote/01_computer_architecture/15_advanced_topics/588_toe/) 같은 기능은 더 많은 상태 추적과 재조립을 요구하므로 구현과 운영 난도가 높아진다.

- **📢 섹션 요약 비유**: 창고 자동화도 송장 붙이기, 박스 분할, 출고 라인 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)처럼 단계별로 나뉜다. 자동화가 많을수록 사람 손은 줄지만, 기계끼리 타이밍을 맞추는 설계는 더 중요해진다.

---

## Ⅲ. 비교 및 연결

NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 크게 비상태성 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/), 상태성 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/), 그리고 더 나아간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로 전용 가속으로 나눠 볼 수 있다. 이 차이를 구분해야 왜 587번의 일반 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)과 588번의 TOE가 이어지면서도 다른 주제인지 선명해진다.

| 구분 | 연결 상태 보유 | 대표 기능 | 강점 | 한계 |
| :--- | :---: | :--- | :--- | :--- |
| 비상태성 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) | 낮음 | [Checksum](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) Offload, TSO, RSS | 범용적이고 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 충돌이 적음 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 전체 상태 부담은 여전히 호스트에 남음 |
| [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 오프로드 엔진 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) Offload 엔진, [TOE](/studynote/01_computer_architecture/15_advanced_topics/588_toe/)) | 높음 | 재전송, 순서 관리, [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 응답 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | CPU와 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 부담을 더 크게 줄임 | [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 복잡도, 가시성 저하, 유연성 감소 |
| 원격 [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) (Remote [Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/), [RDMA](/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/)) / SmartNIC / [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 장치 ([Data Processing Unit](/studynote/06_ict_convergence/03_cloud_infrastructure/229_dpu_ipu_infrastructure_accelerator_offloading/), [DPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/)) | 경우에 따라 매우 높음 | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 우회, [가상 스위치](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/), 보안·스토리지 오프로드 | 매우 낮은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 높은 전문성 | 도입 비용과 운영 복잡도가 큼 |

또 하나의 중요한 비교 대상은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 쪽 소프트웨어 보완 기능이다. 제네릭 수신 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) (Generic Receive Offload, GRO)은 LRO와 비슷한 효과를 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 쪽에서 내고, 제네릭 [세그멘테이션](/studynote/02_operating_system/06_memory_management/364_segmentation/) [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) (Generic [Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/) Offload, GSO)은 TSO가 없는 환경의 소프트웨어 보완재 역할을 한다. 즉 하드웨어 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 항상 절대 우위인 것은 아니고, 하드웨어와 소프트웨어가 어디서 분담할지의 문제에 가깝다.

결국 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 "패킷 처리 전문화"의 출발점이다. [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 같은 작은 잡무부터 시작해, [TOE](/studynote/01_computer_architecture/15_advanced_topics/588_toe/), SmartNIC, DPU처럼 더 큰 상태와 더 복잡한 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 맡는 방향으로 확장된다.

- **📢 섹션 요약 비유**: 단순 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 계산대의 바코드 스캐너라면, TOE는 재고까지 자동 관리하는 창고 시스템이고, SmartNIC과 DPU는 물류센터 한 동을 통째로 자동화한 수준이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)을 "무조건 켜는 옵션"으로 보면 안 된다. 웹 서버, 스토리지 서버, [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 호스트처럼 처리량이 중요한 곳에서는 대부분 유리하지만, 라우터·[방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)·패킷 분석 장비처럼 패킷을 있는 그대로 보고 즉시 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용해야 하는 곳에서는 일부 기능이 오히려 불리할 수 있다. 특히 LRO는 포워딩 경로에서 다시 분할이 필요해질 수 있고, 패킷 캡처 시 실제 wire packet과 다른 모습이 보여 디버깅을 헷갈리게 만든다.

### 적용 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 병목이 애플리케이션 연산이 아니라 softirq나 per-packet [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 처리인가?
2. 작은 패킷 비율이 높아 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 큐 관리 오버헤드가 큰가?
3. 장비 역할이 종단 서버인가, 아니면 포워딩·보안 분석 장비인가?
4. RSS 큐 수와 CPU 코어 pinning이 실제 워크로드와 맞는가?
5. 패킷 캡처, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 분석, 장애 대응 시 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)을 일시적으로 끌 수 있는 운영 절차가 있는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 패킷 분석 장비에서 LRO를 켠 채 원본 패킷을 그대로 보고 있다고 믿는 운영
- 포워딩 노드에서 무조건 수신 병합을 켜 두어 재분할 비용을 늘리는 설계
- RSS 큐는 많지만 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) affinity와 애플리케이션 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 배치를 맞추지 않아 캐시 locality를 잃는 운영
- 실제 CPU 병목 측정 없이 "[오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) = 무조건 빠름"이라고 가정하는 튜닝

기술사 답안에서는 기능 이름만 나열하기보다, <strong>어떤 <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/">오프로딩</a>이 stateless이고 어떤 것이 stateful이며, 왜 특정 장비에서는 켜고 다른 장비에서는 꺼야 하는지</strong>를 함께 써야 실무 감각이 살아난다.

- **📢 섹션 요약 비유**: 자동 변속기는 일반 도로에서는 편하고 빠르지만, 정밀한 엔진 브레이크가 필요한 산길에서는 운전자가 수동으로 개입해야 할 때가 있다. [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)도 워크로드에 따라 그만큼 섬세하게 켜고 꺼야 한다.

---

## Ⅴ. 기대효과 및 결론

NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 잘 맞는 환경에서는 CPU 코어를 패킷 정리 작업에서 해방시켜, 같은 서버로 더 높은 처리량을 유지할 수 있다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 빈도가 줄고 수신 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)이 좋아지면 tail latency도 더 안정될 수 있으며, 높은 회선 속도를 애플리케이션 성능으로 연결하기 쉬워진다. 즉 회선 대역폭을 사 놓고도 CPU 때문에 못 쓰는 상황을 줄여 준다.

다만 한계도 있다. [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 많아질수록 디버깅 경로는 길어지고, 일부 기능은 장비 역할과 충돌하며, [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)와 드라이버 품질에 더 민감해진다. 앞으로는 고정 기능 NIC를 넘어, SmartNIC과 DPU처럼 네트워크·스토리지·보안 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)을 한 칩 안에서 프로그래머블하게 다루는 방향이 더 중요해질 가능성이 크다.

결론적으로 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 "네트워크를 더 빠르게 보내는 기술"이라기보다, <strong>패킷 처리에서 범용 CPU가 굳이 하지 않아도 되는 일을 하드웨어에 위임하는 기술</strong>로 기억하는 것이 정확하다. 그래야 588번 [TOE](/studynote/01_computer_architecture/15_advanced_topics/588_toe/) 같은 상태성 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)과도 자연스럽게 연결된다.

- **📢 섹션 요약 비유**: 좋은 물류센터는 도로를 더 넓히는 것만이 아니라, 출하장 안의 반복 작업을 얼마나 자동화하느냐로 성능이 갈린다. NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 서버 안에 그 자동 출하장을 들이는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/), [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/)) | NIC가 CPU 개입 없이 패킷 버퍼를 주고받게 하는 기본 메커니즘이다. |
| [Checksum](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) Offload | 가장 기본적인 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) 기능으로 per-packet 산술 부담을 줄인다. |
| [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/) Offload (TSO) | 송신 측 대형 버퍼를 실제 전송 단위로 나누는 대표 기능이다. |
| Large Receive Offload (LRO) / Generic Receive Offload (GRO) | 수신 측 병합을 하드웨어와 소프트웨어가 각각 맡는 대표 구조다. |
| Receive Side Scaling (RSS) | 멀티큐 기반 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리로 단일 코어 병목을 줄인다. |
| [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 오프로드 엔진 ([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) Offload 엔진, [TOE](/studynote/01_computer_architecture/15_advanced_topics/588_toe/)) | 비상태성 NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 상태성 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)으로 확장된 대표 사례다. |

### 📈 관련 키워드 및 발전 흐름도

```text
기본 NIC + DMA
    |
    v
Checksum Offload
    |
    v
TSO · LRO · RSS
    |
    v
상태성 오프로딩 (TOE)
    |
    v
SmartNIC · DPU 기반 통합 오프로딩
    |
    v
프로그래머블 네트워크 / 보안 / 스토리지 데이터 경로
```

이 흐름은 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)이 작은 per-packet 최적화에서 출발해, 점차 연결 상태와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로 전체를 맡는 방향으로 커졌음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 원래는 컴퓨터가 택배 하나 올 때마다 직접 상자를 열고 붙이고 정리하느라 바빴어요.
2. NIC [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)은 옆에 똑똑한 포장 기계를 두어서 그런 반복 일을 대신하게 하는 거예요.
3. 그래서 컴퓨터는 힘든 포장 말고, 진짜 중요한 계산 일을 더 많이 할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 587 / 803

<- **이전**: [586. 부동소수점 곱셈기 파이프라인 (Floating-Point Multiplier Pipeline)](/studynote/01_computer_architecture/15_advanced_topics/586_fpu_multiplier_pipeline/)
**다음**: [588. TCP 오프로드 엔진 (TOE)](/studynote/01_computer_architecture/15_advanced_topics/588_toe/) ->

---
