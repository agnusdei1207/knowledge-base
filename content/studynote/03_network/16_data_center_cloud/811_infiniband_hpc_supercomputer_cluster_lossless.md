+++
title = "811. 인피니밴드 (InfiniBand)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)와 클라우드 네트워크에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)를 이해하면 확장성과 운영 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **태생적 오버헤드**: 이더넷은 웹서핑을 위해 만들어졌습니다. 패킷이 도착하면 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(OS)이 "누구한테 온 거야? 에러 없어?"라며 복잡한 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 검사 절차를 거치느라 CPU 자원을 갉아먹고 속도가 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)됩니다.
- **패킷 손실 (Drop)**: 트래픽이 몰리면 쿨하게 패킷을 버립니다. 재전송을 기다리는 동안 100억 원어치 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 클러스터가 멍 때리고 연산을 멈춥니다(통신 병목 현상).



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">iSCSI</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">인피니밴드</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">RDMA</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 1999년에 탄생하여 슈퍼컴퓨터([HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/), [High Performance Computing](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/226_hpc_supercomputing_infrastructure/))와 거대 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내부의 서버 간(Server-to-Server), 혹은 스토리지 간 통신을 위해 극도로 최적화된 <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a>, 초저지연, 무결손(Lossless) <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a> 패브릭 통신 아키텍처</strong>입니다. (현재 엔비디아/멜라녹스가 시장을 꽉 쥐고 있습니다.)

### [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)의 3대 물리적/논리적 특성 🌟
1. **무결손 (Lossless) 네트워크 절대 보장**:
   - [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 이더넷처럼 패킷을 절대 바닥에 버리지 않습니다. 
   - <strong>신용 기반 <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/">흐름 제어</a> (Credit-based <a href="/knowledge-base/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/">Flow Control</a>)</strong>: 송신자는 수신자(또는 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))에게 미리 "나 패킷 몇 개 보내도 돼?"라고 물어보고 허락(Credit)받은 개수만큼만 쏩니다. 받을 공간이 확실할 때만 쏘기 때문에 망 전체에서 패킷 드랍율이 0%가 됩니다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 우회 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> Bypass) &amp; 하드웨어 처리</strong>:
   - 패킷을 받을 때 OS(윈도우/리눅스) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 아예 거치지 않습니다. [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) 랜카드(HCA) 칩셋 자체가 패킷을 받자마자 바로 응용 프로그램 메모리로 냅다 꽂아버립니다. (이를 구현하는 기술이 바로 다음 812번 문서의 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a></strong>입니다.)
3. **극한의 대역폭과 초저지연**:
   - 200Gbps(HDR), 400Gbps(NDR), 최근에는 800Gbps([XDR](/knowledge-base/studynote/02_operating_system/02_process_thread/127_xdr_external_data_representation/))까지 단일 링크 속도를 뽑아내며, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 통과하는 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 100나노초(0.0001ms) 이하로 이더넷보다 수십 배 빠릅니다.

- 인터넷의 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)(IP) 구조와는 다릅니다. [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 여러 대의 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 서버들을 하나의 <strong>'서브넷(Subnet)'</strong>으로 묶습니다.
- 서브넷 중앙에는 <strong>서브넷 관리자(Subnet Manager, <a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/">SM</a>)</strong>라는 똑똑한 관제탑 뇌가 딱 1개 있습니다. 이 SM이 "A 서버에서 B 서버로 갈 때는 3번 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 타라"라고 모든 길을 사전에 완벽하게 그려서 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들에게 나눠줍니다. 장비들이 길을 헤매지 않으니 속도가 미친 듯이 빠릅니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">iSCSI</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">인피니밴드</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">RDMA</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

[인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. iSCSI가 기반 조건을 만든다면, [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 그 위에서 핵심 메커니즘을 구현하고, RDMA는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 확장성과 운영 자동화에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | iSCSI의 기반 정리 | [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)의 핵심 동작 | RDMA의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 확장성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

오늘날 수천억 원짜리 거대 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(초거대 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 학습용 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 지을 때, 수만 개의 H100 GPU를 서로 엮어주는 백본망으로 [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 사실상 100% 독점 사용되고 있습니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 이더넷이 전 세계 누구나 택배를 주고받을 수 있는 '공용 우체국 택배망'이라면, 속도는 빠르지만 가끔 분실도 되고 배송 순서도 뒤죽박죽입니다. <strong><a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/">인피니밴드</a></strong>는 [반도체](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 공장 내부에 로봇들끼리만 부품을 주고받기 위해 깐 '진공관 하이퍼루프 컨베이어 벨트'입니다. 바깥세상(인터넷)과는 통신할 수 없지만, 공장 내부(클러스터)에서만큼은 수만 대의 로봇이 단 0.001초의 딜레이도 없이, 단 하나의 부품(패킷)도 바닥에 흘리지 않고 완벽한 타이밍으로 부품을 슉슉 던지고 받을 수 있는 극강의 폐쇄형 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 핏줄입니다.

---

## Ⅴ. 기대효과 및 결론

[인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)와 클라우드 네트워크를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 확장성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/), [클라우드 네이티브 네트워킹](/knowledge-base/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/), 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [클라우드 네이티브 네트워킹](/knowledge-base/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/) 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [iSCSI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/698_iscsi/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [오버레이 네트워크](/knowledge-base/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/) ([Overlay Network](/knowledge-base/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/)) | 가상 환경의 논리적 연결을 만든다. |
| 패브릭 (Fabric) | 대규모 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 균일한 연결 구조다. |
| [RDMA](/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: iSCSI</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: 인피니밴드</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: RDMA</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 클라우드 네이티브 네트워킹</div></div>
</div>
</div>



[인피니밴드](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/361_infiniband/)는 iSCSI에서 출발해 현재 메커니즘을 정교화하고, 이후 RDMA와 [클라우드 네이티브 네트워킹](/knowledge-base/studynote/03_network/16_data_center_cloud/821_cloud_native_networking_scale_out_msa/) 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 아파트에 사는 친구들이 층마다 다른 규칙으로 엘리베이터를 타면 복잡해져요.
2. 이 개념은 어느 층에서 누구를 어떻게 연결할지 자동으로 정리해 주는 관리실과 같아요.
3. 그래서 많은 컴퓨터가 한 건물 안에서 더 잘 협력할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 932 / 1120

← **이전**: [810. iSCSI (Internet Small Computer System Interface)](/knowledge-base/studynote/03_network/16_data_center_cloud/810_iscsi_internet_small_computer_system_interface/)
**다음**: [812. RDMA (Remote Direct Memory Access)](/knowledge-base/studynote/03_network/16_data_center_cloud/812_rdma_remote_direct_memory_access_kernel_bypass/) →

---
