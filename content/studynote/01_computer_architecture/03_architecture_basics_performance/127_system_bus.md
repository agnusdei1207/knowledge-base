---
title: "System Bus"
date: "2026-04-25"
tags:
  - "studynote-computer-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) (System [Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))는 CPU (Central Processing Unit), 주기억장치, 입출력 장치가 주소·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 공유 규칙에 따라 교환하는 공통 통신 경로다.
> 2. **가치**: 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 부품 간 연결 수를 폭발적으로 늘리지 않고도 표준화된 인터페이스와 확장 가능한 컴퓨터 구조를 가능하게 한다.
> 3. **판단 포인트**: [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 선 개수보다도 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 중재 (Arbitration), 계층 분리, [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) ([DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/), [Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 같은 운영 방식이 좌우한다.

---

## Ⅰ. 개요 및 필요성

시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) (System [Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))는 컴퓨터 내부 구성요소가 공통 규칙으로 통신하도록 만든 공유 전달 경로다. CPU, 메모리, 입출력 장치를 모두 1:1 전용선으로 연결하면 부품 수가 늘수록 배선 수와 제어 복잡도가 급격히 커진다. 그래서 컴퓨터 구조는 “각 장치가 같은 길을 번갈아 사용하되, 목적지와 사용 순서를 명확히 정하자”는 방식으로 발전했다.

핵심 필요성은 세 가지다. 첫째, <strong>배선 단순화</strong>다. 둘째, <strong>표준화</strong>다. 셋째, <strong>자원 공유</strong>다. 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 없으면 메모리 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 저장장치 제어기, 네트워크 카드가 각자 다른 전용 연결법을 요구하므로 메인보드 설계와 확장이 매우 비효율적이 된다.

아래 그림은 왜 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 필요한지를 연결 구조 관점에서 보여준다. 왼쪽은 모든 장치를 직접 연결한 경우이고, 오른쪽은 공용 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 도입한 경우다.

```text
+------------------------------+      +------------------------------+
|  전용선 중심 연결             |      |  시스템 버스 중심 연결        |
+------------------------------+      +------------------------------+
| CPU ----- Memory             |      | CPU    +                     |
|  | \      /  |               |      | Memory +-- System Bus -- I/O |
|  |  \    /   |               |      | Disk   +                     |
|  |   \  /    |               |      | NIC    +                     |
| Disk -- I/O - NIC            |      |                              |
|                              |      | 연결 수 감소, 확장 용이      |
| 장치 추가 시 선 수 급증      |      | 장치 추가 시 접속 규칙 재사용 |
+------------------------------+      +------------------------------+
```

즉 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 단순한 선 묶음이 아니라, 컴퓨터를 “조립 가능한 시스템”으로 만드는 약속의 집합이다. 하드웨어 표준화와 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)화가 가능해진 배경에도 이 공통 통신 경로 개념이 있다.

- **📢 섹션 요약 비유**: 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 도시 중앙도로와 같다. 집집마다 전용 고속도로를 까는 대신, 모두가 같은 큰 도로로 나와 규칙에 맞춰 움직이면 도시가 훨씬 단순하고 커지기 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 보통 <strong><a href="/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/">데이터 버스</a> (<a href="/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/">Data Bus</a>)</strong>, <strong><a href="/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/">주소 버스</a> (<a href="/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/">Address Bus</a>)</strong>, <strong><a href="/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/">제어 버스</a> (<a href="/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/">Control Bus</a>)</strong> 로 나누어 이해한다. [데이터 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)는 실제 값을 옮기고, [주소 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/)는 목적지를 지정하며, [제어 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)는 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/), 승인 같은 통신 절차를 맞춘다. 물리적으로는 여러 배선 묶음이지만, 논리적으로는 “무엇을 어디로 어떤 시점에 보낼지”를 분리한 구조다.

| [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 종류 | 핵심 역할 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 미치는 영향 | 대표 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 예시 |
| :-- | :-- | :-- | :-- |
| [데이터 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) ([Data Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)) | 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 | 폭이 넓을수록 한 번에 더 많은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 전송 | 32비트, 64비트 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| [주소 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/) ([Address Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/)) | 접근 대상 지정 | 주소 공간 크기 결정 | 메모리 번지, 장치 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) |
| [제어 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/) ([Control Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)) | 통신 절차 제어 | 충돌 방지와 타이밍 안정성 좌우 | Read, Write, ACK, [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) |

메모리 읽기 동작을 예로 들면, CPU는 먼저 [주소 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/)에 읽고 싶은 위치를 올린다. 이어 [제어 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/347_control_bus/)에 읽기 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보낸다. 그러면 메모리가 해당 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [데이터 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/)에 실어 보내고, CPU가 그 값을 가져간다. 이 과정이 빠르게 보이더라도, 실제로는 어느 장치가 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 사용할지 정하는 중재와 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 안정화를 위한 시간이 포함된다.

아래 그림은 한 번의 읽기 사이클에서 세 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 어떤 역할 분담을 하는지 압축해서 보여준다.

```text
+--------------------------------------------------------------+
|              시스템 버스의 읽기 사이클 예시                  |
+--------------------------------------------------------------+
| ① CPU -- 주소 버스 ---> 메모리 위치 지정                      |
| ② CPU -- 제어 버스 ---> Read 신호 전달                        |
| ③ RAM -- 데이터 버스 ---> 데이터 반환                         |
|                                                              |
| 주소 버스   : "어디를 읽을까"                                |
| 제어 버스   : "지금 읽기 동작이다"                           |
| 데이터 버스 : "실제 값은 이것이다"                           |
+--------------------------------------------------------------+
```

[버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 폭과 주파수는 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 결정하는 중요한 요소지만, 그것만으로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 정해지지는 않는다. 여러 장치가 동시에 쓰려 할 때 누구에게 우선권을 줄지 정하는 <strong><a href="/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/">버스 중재</a>기 (<a href="/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">Bus</a> Arbiter)</strong>, CPU 대신 입출력 장치가 메모리와 직접 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받도록 하는 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/), 그리고 고속 장치와 저속 장치를 다른 경로로 분리하는 계층형 설계가 함께 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 좌우한다.

- **📢 섹션 요약 비유**: 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 택배 시스템과 같다. 주소표는 어디로 갈지 알려 주고, 주의표시는 어떻게 다룰지 정하며, 실제 상자는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다. 세 가지가 맞아야 배송이 끝난다.

---

## Ⅲ. 비교 및 연결

시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 제대로 이해하려면 “모두가 한 길을 공유하는 구조”와 “필요에 따라 길을 나누는 구조”를 함께 봐야 한다. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 컴퓨터는 하나의 공유 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 CPU, 메모리, 입출력 장치를 매달아 단순성을 얻었다. 하지만 CPU 속도가 급격히 빨라지면서, 느린 장치가 같은 길을 오래 점유하면 전체가 멈추는 병목이 커졌다.

| 비교 축 | 전통적 공유 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) | 현대 계층형/점대점 연결 |
| :-- | :-- | :-- |
| 구조 | 여러 장치가 하나의 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 공유 | 고속 경로와 저속 경로를 분리 |
| 장점 | 단순, 비용 절감, 이해 용이 | 병목 완화, 확장성 향상 |
| 단점 | 경합 증가, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 한계 | 설계 복잡도와 제어 비용 증가 |
| 대표 예 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), [ISA](/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) | [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express), 메모리 채널 |

또 다른 중요한 비교는 <strong><a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> <a href="/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">버스</a> (Parallel <a href="/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">Bus</a>)</strong> 와 <strong><a href="/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/">직렬</a> <a href="/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">버스</a> (<a href="/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/">Serial</a> <a href="/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">Bus</a>)</strong> 다. [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 한 번에 많은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 보내는 대신, [신호](/studynote/02_operating_system/02_process_thread/130_signal/)선이 많아질수록 스큐 (Skew)와 간섭 관리가 어려워진다. 반면 현대의 고속 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 인터커넥트는 선 수를 줄이고 클럭 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 및 패킷 기반 전송으로 더 높은 실효 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 얻는다. 그래서 오늘날 “시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)”는 과거처럼 무조건 하나의 넓은 공용 배선만 뜻하지 않고, 논리적으로 시스템 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 조직하는 상위 개념으로 이해해야 한다.

이 개념은 다른 주제와도 직접 연결된다. 폰 노이만 병목 ([Von Neumann Bottleneck](/studynote/01_computer_architecture/15_advanced_topics/500_von_neumann_bottleneck/))은 CPU 연산 속도보다 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)·메모리 전송 속도가 느려 생기는 문제이고, [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) ([DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/))은 CPU가 모든 전송을 직접 중계하지 않게 하여 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 활용 효율을 높인다. 또한 캐시 계층과 메모리 채널, 주변장치 인터커넥트는 모두 “어떤 트래픽을 어떤 길로 보낼 것인가”라는 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계 철학의 연장선에 있다.

- **📢 섹션 요약 비유**: 예전 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 구조는 시내 모든 차가 한 도로를 같이 쓰는 모습이고, 현대 구조는 고속도로·국도·골목길을 나눠 쓰는 교통 체계다. 길을 나누면 복잡해지지만 정체는 크게 줄어든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 문제는 “CPU가 느리다”가 아니라 “[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 길이 막힌다”로 나타나는 경우가 많다. 예를 들어 고성능 그래픽 처리 장치 ([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))나 비휘발성 메모리 익스프레스 ([NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/), [Non-Volatile Memory Express](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) 저장장치를 추가했는데 기대 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나오지 않는다면, 연산장치 자체보다 [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 레인 수, [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 구조, 메모리 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 먼저 봐야 한다. 장치가 빠를수록 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계가 병목의 중심으로 드러난다.

### 실무 체크포인트

1. <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a> <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: [데이터 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) 폭, 클럭, 레인 수가 장치 요구량을 감당하는가?
2. <strong>중재 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 여러 마스터가 동시에 접근할 때 우선순위와 공정성이 보장되는가?
3. <strong><a href="/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/">DMA</a> 사용 여부 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 대용량 전송을 CPU가 직접 복사하고 있지 않은가?
4. <strong>계층 분리 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 저속 장치 트래픽이 고속 연산 경로를 방해하지 않는가?
5. <strong>메모리 주소 범위 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: [주소 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/) 한계 때문에 실제 장착 메모리를 다 쓰지 못하는 구조는 아닌가?

### 판단 사례

- **채택해야 할 때**: 임베디드 보드처럼 장치 수가 제한되고 구조 단순성이 중요한 경우에는 공유 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 구조가 여전히 유효하다.
- **분리해야 할 때**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 서버, 고속 스토리지 서버처럼 동시 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 수요가 큰 환경에서는 메모리 채널, [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), 전용 인터커넥트를 분리해야 한다.
- <strong>회피해야 할 <a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: 대용량 입출력을 CPU 복사 루프로 처리하거나, 모든 장치를 하나의 저속 [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 아래 몰아넣는 설계는 전체 시스템 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 급격히 떨어뜨린다.

기술사 관점에서는 “[버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 단순 연결선이 아니라 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·확장성·비용의 균형점”이라는 표현이 중요하다. 같은 CPU를 써도 어떤 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 구조를 택했느냐에 따라 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 확장 한계가 달라지기 때문이다.

- **📢 섹션 요약 비유**: 실무에서 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계는 좋은 엔진을 사는 문제보다 도로 차선을 어떻게 배치할지 정하는 문제에 가깝다. 차가 빠를수록 길 설계가 더 중요해진다.

---

## Ⅴ. 기대효과 및 결론

좋은 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 설계는 세 가지 효과를 만든다. 첫째, 장치 추가와 교체가 쉬워진다. 둘째, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 경로가 정돈되어 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 예측하기 쉬워진다. 셋째, CPU가 계산에 집중하고 전송은 DMA와 주변장치가 분담하도록 역할을 나눌 수 있다.

물론 한계도 분명하다. 공유 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 구조가 단순한 대신 경합이 생기기 쉽고, 계층형 인터커넥트는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이는 대신 칩셋, [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 제어가 복잡해진다. 따라서 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 기억할 때는 “부품을 연결하는 선”보다 “시스템 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 조직하는 구조”로 이해하는 편이 정확하다.

오늘날에는 단일 공용 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)만으로 고성능 시스템을 감당하기 어렵기 때문에, 메모리 채널 분리, [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 인터커넥트, [칩렛](/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/) 간 연결 같은 형태로 진화하고 있다. 그러나 기본 원리는 변하지 않는다. <strong>누가, 언제, 어떤 경로로 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 옮길지 합의하는 구조</strong>가 바로 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 본질이다.

- **📢 섹션 요약 비유**: 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 컴퓨터 몸속 혈관망과 같다. 혈관이 잘 나뉘고 흐름이 정리돼야 뇌도 손발도 제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [버스 중재](/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/) ([Bus Arbitration](/studynote/01_computer_architecture/09_system_bus_interconnects/351_bus_arbitration/)) | 여러 장치가 공용 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사용권을 나눌 때 충돌을 방지하는 핵심 메커니즘 |
| [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | CPU 개입 없이 장치와 메모리 간 전송을 수행해 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 활용 효율을 높임 |
| 폰 노이만 병목 ([Von Neumann Bottleneck](/studynote/01_computer_architecture/15_advanced_topics/500_von_neumann_bottleneck/)) | CPU 처리 속도보다 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)·메모리 전달 속도가 느려 생기는 구조적 병목 |
| [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express) | 현대 시스템에서 고속 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 점대점 연결로 진화한 대표 인터커넥트 |
| 메모리 채널 (Memory Channel) | 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 개념이 고속 메모리 전용 경로로 세분화된 예 |

### 📈 관련 키워드 및 발전 흐름도

```text
공유 배선 기반 연결
        |
        v
시스템 버스 (주소 버스 · 데이터 버스 · 제어 버스)
        |
        v
버스 중재 (Arbitration) · DMA (Direct Memory Access)
        |
        v
계층형 버스 구조 · 브리지 기반 분리
        |
        v
PCIe (Peripheral Component Interconnect Express) · 고속 직렬 인터커넥트
        |
        v
칩렛 인터커넥트 · 고대역폭 메모리 연동 구조
```

이 흐름은 단일 공유선에서 시작한 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 개념이 병목 해소를 위해 중재·분리·고속 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 방향으로 진화했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안의 두뇌와 창고와 장난감 친구들이 서로 이야기하려면 같이 쓰는 길이 필요해요.
2. 그 길이 바로 시스템 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)이고, 주소표와 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등과 짐차가 함께 움직이는 길이에요.
3. 길이 막히지 않게 잘 나누고 순서를 지켜야 컴퓨터도 똑똑하고 빠르게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 127 / 803

<- **이전**: [126. 하버드 아키텍처 (Harvard Architecture)](/studynote/01_computer_architecture/03_architecture_basics_performance/126_harvard_architecture/)
**다음**: [128. 폰 노이만 병목현상 (Von Neumann Bottleneck)](/studynote/01_computer_architecture/03_architecture_basics_performance/128_von_neumann_bottleneck/) ->

---
