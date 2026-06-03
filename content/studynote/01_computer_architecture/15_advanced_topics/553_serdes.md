+++
title = "553. 초고속 SerDes (Serializer/Deserializer)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) SerDes (Serializer/Deserializer)는 넓은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 소수의 고속 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 레인으로 바꿔, 핀 수와 배선 길이는 억제하면서도 칩 간 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)은 계속 높이는 물리 계층 핵심 회로다.
> 2. **가치**: 고속 시스템의 병목은 더 이상 연산기만이 아니라 패키지·보드·커넥터를 통과하는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)에 있으므로, SerDes는 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express), [Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/), [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 같은 현대 인터커넥트의 실질적 기반이 된다.
> 3. **판단 포인트**: 좋은 SerDes는 단순 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 속도보다 채널 손실, 지터 (Jitter), 이퀄라이제이션 (Equalization), CDR ([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) and [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)), FEC ([Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Error Correction)가 함께 맞물려 목표 BER ([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Error Rate)을 만족하는가로 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

SerDes (Serializer/Deserializer)는 칩 내부의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열로 내보내고, 수신 측에서 다시 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 복원하는 고속 입출력 구조다. 겉으로는 "선을 줄이는 기술"처럼 보이지만, 실제 본질은 <strong>핀 수와 타이밍 불일치를 감당 가능한 수준으로 제어하면서 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a>을 확장하는 방법</strong>에 있다.

[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 폭을 넓히면 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 높일 수 있지만, 속도가 올라갈수록 스큐 (Skew), 배선 길이 차이, 전자기 간섭 (Electromagnetic Interference, EMI), 패키지 핀 한계가 동시에 커진다. 예를 들어 128비트 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 인터페이스를 GHz급으로 밀어 올리면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체보다 배선 정합과 타이밍 맞춤이 더 어려운 문제가 된다. 반면 SerDes는 적은 수의 차동 레인에 고속 클럭 복원과 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 보정 기능을 집중해, 같은 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 훨씬 현실적인 배선 복잡도로 제공한다.

즉 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) SerDes가 필요한 이유는 "[직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)이 멋져서"가 아니라, 고성능 컴퓨팅이 이미 <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 핀 확장보다 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/">신호</a> <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 공학의 시대</strong>로 넘어왔기 때문이다. CPU와 가속기, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 [NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) (Network Interface Card), 서버와 광 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 사이에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 끊기지 않으려면, 계산만 빠른 칩이 아니라 먼 거리에서도 눈 모양이 열려 있는 링크가 필요하다.

- **📢 섹션 요약 비유**: [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) SerDes는 여러 차선 도로를 무한정 넓히는 대신, 소수의 전용 고속 터널을 정교하게 뚫어 더 많은 차량을 안정적으로 보내는 교통 설계와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) SerDes는 송신기, 채널, 수신기의 세 블록으로 나뉘지만, 실제 설계 핵심은 그 사이의 <strong>마진 예산</strong>을 어떻게 배분하느냐에 있다. 송신기는 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화와 프리엠퍼시스 (Pre-emphasis)를 담당하고, 채널은 패키지·PCB (Printed Circuit Board)·커넥터·케이블에서 삽입 손실과 누화를 만든다. 수신기는 CTLE (Continuous-Time Linear [Equalizer](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/566_equalizer_isi_inter_symbol_interference/)), DFE (Decision Feedback [Equalizer](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/566_equalizer_isi_inter_symbol_interference/)), CDR로 손상된 파형을 다시 읽을 수 있는 상태로 복원한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| [PCS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/191_thread_scheduling_pcs_scs/) (Physical Coding Sublayer) / Gearbox | 인코딩, lane [mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭 변환 | 인코딩 효율과 lane alignment가 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 손실을 좌우한다. |
| Serializer + PLL (Phase-Locked Loop) | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열로 변환, 고속 기준 클럭 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 지터와 위상 잡음이 커지면 eye opening이 빠르게 닫힌다. |
| TX (Transmit) FFE (Feed-[Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) [Equalizer](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/566_equalizer_isi_inter_symbol_interference/)) | 송신단에서 고주파 감쇄를 선보상 | 채널이 짧으면 과보상이 오히려 오버슈트를 만든다. |
| RX (Receive) CTLE / DFE | 채널 손실과 ISI (Inter-Symbol Interference) 복원 | 적응 알고리즘이 느리면 링크 트레이닝 시간이 길어진다. |
| CDR | 수신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 타이밍 기준을 재생성 | 주파수 오차와 랜덤 지터를 동시에 추적해야 한다. |
| Deskew / FEC | 다중 레인 정렬, 잔여 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류 정정 | PAM4 (Pulse Amplitude Modulation 4) 세대에서 중요도가 크게 올라간다. |

다음 그림은 고속 링크에서 어느 지점에서 마진을 얻고 잃는지를 압축해 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ High-speed SerDes lane: margin is created in TX/RX and consumed in link   │
├────────────────────────────────────────────────────────────────────────────┤
│ Parallel data                                                              │
│     │                                                                      │
│     ▼                                                                      │
│ [PCS/Encode] -> [Serializer] -> [TX FFE] ->== Channel ==-> [CTLE/DFE] ->  │
│                                                       │                    │
│                                                       └----> [CDR] ->      │
│                                                                  [De-Ser]  │
│                                                                       │    │
│                                                                       ▼    │
│                                                               [Deskew/FEC] │
│                                                                            │
│ Margin equation: channel loss + crosstalk + jitter < EQ gain + CDR track  │
└────────────────────────────────────────────────────────────────────────────┘
```

실무적으로는 `총 대역폭 = lane rate × lane 수 × 인코딩 효율`로 생각하면 이해가 쉽다. 하지만 lane rate를 올릴수록 나이퀴스트 주파수 손실, [전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/), CDR 난도가 함께 증가하므로, 단순히 더 빠른 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화기만 넣는다고 해결되지 않는다. 그래서 최신 SerDes는 NRZ (Non-Return-to-Zero)에서 PAM4로 넘어가며 1심볼당 전송 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 늘리는 대신, 더 강한 FEC와 DSP (Digital [Signal](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) Processing) 기반 적응형 이퀄라이제이션을 함께 도입하고 있다.

- **📢 섹션 요약 비유**: 이 구조는 목소리를 멀리 보내기 위해 송신기에서 발음을 또렷하게 다듬고, 수신기에서는 보청기와 박자 감지기를 함께 써서 흐려진 소리를 다시 알아듣는 과정과 같다.

---

## Ⅲ. 비교 및 연결

SerDes를 정확히 이해하려면 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 인터페이스, NRZ 기반 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 링크, PAM4 기반 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 링크를 함께 비교해야 한다. [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 인터페이스는 짧은 거리에서 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 낮고 구조가 단순하지만, 핀 수와 스큐 관리 비용이 급격히 커진다. NRZ SerDes는 상대적으로 넓은 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 마진을 유지하면서 다중 기가비트 전송을 구현하기 좋고, PAM4 SerDes는 같은 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)에서 심볼 속도를 억제할 수 있지만 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 레벨 간격이 좁아져 FEC 의존성이 높아진다.

| 항목 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) I/O | NRZ SerDes | PAM4 SerDes |
| :-- | :-- | :-- | :-- |
| 시간 기준 | 공통 클럭 분배 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내 클럭 복원 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내 클럭 복원 + 강한 DSP 보정 |
| 배선 수 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭만큼 증가 | 소수 차동 레인 | 소수 차동 레인 |
| [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 마진 | 스큐가 주된 문제 | [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 마진이 비교적 넓음 | [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 마진이 좁아 BER 관리가 더 어렵다 |
| 오류 대응 | 타이밍 정합 중심 | EQ + 재전송 | EQ + FEC + 상세 텔레메트리 |
| 대표 적용 | DDR ([Double Data Rate](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/253_ddr_sdram/)) 계열 메모리 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) | [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 5.0, USB4 ([Universal Serial Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 4) | [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 6.0, 400/800G [Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) |

이 비교가 중요한 이유는 "모든 고속 링크가 같은 방식으로 빨라지는 것이 아니다"라는 점을 보여 주기 때문이다. 예를 들어 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 6.0은 PAM4와 FLIT 기반 오류 제어를 통해 레인당 전송량을 높였고, CXL은 그 SerDes 물리층을 재사용해 메모리 공유 아키텍처를 확장한다. [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 광 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)에서는 같은 SerDes라도 전기 채널 길이, retimer 필요성, 광 변환 지점이 달라져 설계 철학이 달라진다.

결국 SerDes는 단독 회로가 아니라 패키지, PCB, 커넥터, [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), FEC 정책이 합쳐진 시스템 개념이다. 그래서 "링크 속도"만 외우는 답안보다, <strong>어떤 속도 세대에서 왜 이퀄라이제이션과 오류 제어가 달라졌는가</strong>를 설명할 수 있어야 진짜 이해다.

- **📢 섹션 요약 비유**: [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) I/O가 여러 명이 나란히 걷는 행렬이라면, NRZ SerDes는 한 줄로 뛰는 달리기 팀이고, PAM4 SerDes는 같은 길에서 손짓 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)까지 섞어 더 많은 정보를 보내는 고난도 릴레이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) SerDes는 스펙 시트의 최대 속도보다 <strong>채널 예산을 실제로 만족하는가</strong>가 더 중요하다. 같은 64GT/s (Giga Transfers per second)급 링크라도 패키지 via, 보드 재질, 커넥터 품질, 온도 조건에 따라 삽입 손실과 반사가 크게 달라진다. 따라서 설계자는 물리 계층 회로 (PHY, Physical Layer) 자체만 볼 것이 아니라, "이 링크가 어느 거리와 어느 손실까지 버틸 것인가"를 먼저 계산해야 한다.

### 적용 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 목표 거리와 채널 손실에서 pre-FEC BER과 post-FEC BER 목표가 분리돼 있는가?
2. TX FFE, RX CTLE/DFE, CDR [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 채널 특성과 맞는가?
3. redriver로 충분한지, 아니면 클럭까지 재생성하는 retimer가 필요한지 판단했는가?
4. 링크 트레이닝 시간, [전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/), 열 설계가 시스템 요구와 충돌하지 않는가?
5. lane bonding 환경이라면 deskew 버퍼와 레인 간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 편차를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 최대 속도 수치만 보고 PCB와 커넥터 손실 예산을 후순위로 미루는 설계
- PAM4 링크에 충분한 FEC와 오류 통계를 붙이지 않고 "물리층이 알아서 되겠지"라고 가정하는 설계
- 짧은 거리용 PHY를 장거리 백플레인에 그대로 적용해 과도한 재전송과 링크 flap을 만드는 설계

기술사 관점에서는 "SerDes = [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 회로"라고만 쓰면 반쪽 답안이다. 채널 손실이 크면 이퀄라이제이션과 retimer가 필요하고, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 시스템이면 FEC 깊이와 재전송 정책이 문제 되며, 전력 제약이 심하면 lane 수를 늘려 심볼 속도를 낮추는 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 가능하다. 즉 SerDes 설계는 <strong>속도·전력·거리·신뢰성의 다변수 최적화</strong>다.

- **📢 섹션 요약 비유**: SerDes 튜닝은 스포츠카 엔진만 세게 만드는 일이 아니라, 도로 상태와 타이어, 브레이크, 운전자 반응까지 맞춰 실제 경기에서 완주하게 만드는 세팅과 같다.

---

## Ⅴ. 기대효과 및 결론

[초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) SerDes가 잘 설계되면 적은 핀 수로 큰 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 제공하고, [칩렛](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/497_chiplet/), 가속기, 스토리지, 네트워크 장비를 더 촘촘하게 연결할 수 있다. 이는 시스템 보드의 크기와 배선 복잡도를 줄이는 동시에, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)·서버·메모리 확장 장치 사이의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 병목을 완화한다. 다시 말해 현대 컴퓨팅의 확장성은 연산 코어 수뿐 아니라 SerDes 품질에 크게 의존한다.

물론 한계도 분명하다. 속도가 올라갈수록 아날로그 전력과 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 복잡도가 증가하고, PAM4 이후 세대에서는 물리층만으로 오류를 0에 가깝게 만들기 어려워 FEC와 시스템 수준 복구가 필수가 된다. 앞으로는 광 I/O, co-packaged optics, 더 정교한 DSP 기반 적응형 수신기가 중요해지겠지만, 핵심 관점은 변하지 않는다. SerDes는 <strong>배선을 줄이는 기술이 아니라 고속 연결을 성립시키는 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/">신호</a> <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 아키텍처</strong>다.

- **📢 섹션 요약 비유**: 좋은 SerDes는 가는 빨대 하나로도 많은 물을 안정적으로 보내는 펌프 시스템과 같다. 빨대만 좋은 것이 아니라 압력 조절과 누수 보정까지 함께 맞아야 제대로 작동한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| CDR ([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) and [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | 별도 클럭선 없이 수신단이 타이밍을 재구성하는 핵심 기능이다. |
| 이퀄라이제이션 (Equalization) | 채널 손실과 ISI를 보정해 eye opening을 확보한다. |
| BER ([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Error Rate) | SerDes 품질을 정량화하는 대표 지표다. |
| FEC ([Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Error Correction) | PAM4 세대에서 잔여 오류를 시스템 수준으로 낮추는 보강 수단이다. |
| Retimer | 긴 채널에서 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)와 클럭을 재생성해 링크 여유를 회복한다. |
| [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) | 최신 메모리·가속기 인터커넥트가 SerDes 물리층 위에 구축된 대표 사례다. |

### 📈 관련 키워드 및 발전 흐름도

```text
병렬 보드 간 인터페이스
        │
        ▼
차동 직렬 링크 · CDR 도입
        │
        ▼
멀티기가비트 NRZ SerDes
        │
        ▼
PAM4 · DSP 이퀄라이제이션 · FEC
        │
        ▼
CXL · 광 I/O · Co-packaged Optics
```

이 흐름은 "배선 절감"에서 출발한 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 링크가, 지금은 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 보정과 오류 제어를 포함한 시스템 인터커넥트 플랫폼으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 많은 친구가 한꺼번에 좁은 문을 지나가면 서로 부딪히니까, 한 줄로 아주 빠르게 지나가게 만드는 것이 SerDes예요.
2. 그런데 너무 빨리 지나가면 목소리가 흐려져서 못 알아들을 수 있으니, 보내는 쪽과 받는 쪽이 소리를 또렷하게 맞춰 줘요.
3. 그래서 멀리 있는 컴퓨터 친구끼리도 적은 길로 많은 이야기를 주고받을 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 553 / 803

← **이전**: [552. 이미지 센서 ISP (Image Signal Processor)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/552_isp/)
**다음**: [554. 오류 정정 부호 (ECC) 회로](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) →

---
