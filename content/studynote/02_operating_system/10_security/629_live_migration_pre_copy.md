---
title: "629. 라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 라이브 마이그레이션은 가상머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 실행 중인 상태 그대로, 네트워크 연결조차 끊기지 않게 하면서 물리 서버 A에서 물리 서버 B로 통째로 옮기는 클라우드 운영의 궁극기다.
> 2. **메커니즘**: VM이 계속 동작하면서 메모리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 끊임없이 변하기 때문에 한 번에 옮길 수 없다. 따라서 <strong>Pre-copy (사전 복사) <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>을 사용하여 VM을 켜둔 채로 메모리를 여러 번 반복 복사(Iterative Copy)하며, 복사 중 변경된 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(Dirty [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))만 계속 추적해서 전송한다.
> 3. **가치**: 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 충분히 작아지는 순간, 찰나의 시간(수십~수백 밀리초) 동안만 VM을 멈추고(Stop-and-Copy) 남은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 넘김으로써, 사용자는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단을 전혀 느끼지 못하며 클라우드 사업자는 무중단 하드웨어 점검(Maintenance)과 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)([Load Balancing](/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/))을 달성한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 라이브 마이그레이션(vMotion, XenMotion, [KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/) Live Migration 등)은 Guest OS(가상머신)의 실행을 중단하지 않고, CPU 상태([레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/))와 메모리, I/O 상태를 다른 물리적 호스트(Target Node)로 복제하여 구동을 이어가는 기술이다.

- **필요성 (서버 점검의 딜레마 극복)**:
  - 과거에는 물리 서버의 램을 교체하거나 패치하려면 무조건 새벽에 공지를 띄우고 서버를 다운(Downtime)시켜야 했다.
  - 클라우드 환경에서는 하나의 물리 장비에 수십 개의 고객사 VM이 돌아가므로 셧다운이 불가능하다. [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 특정 물리 노드에 부하가 몰리거나 하드웨어 오류가 감지될 때, 고객이 눈치채지 못하게 VM을 다른 건강한 노드로 "살아있는 채로" 빼내야(Evacuation) 했다.

- **발전 과정**:
  1. **Cold Migration (정지 복사)**: VM을 완전히 종료(Suspend) $\rightarrow$ 메모리 전체 전송 $\rightarrow$ 재시작. (다운타임 수십 초 ~ 수 분)
  2. **Pre-copy Migration (사전 복사)**: 반복적 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 전송으로 다운타임을 밀리초 단위로 단축. (현재 클라우드 업계 표준)
  3. **Post-copy Migration (사후 복사)**: CPU 상태만 먼저 넘겨서 타겟에서 바로 실행시키고, 메모리는 나중에 [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Fault가 날 때마다 원본에서 땡겨오는 방식. (매우 빠르나 네트워크 단절 시 VM이 죽는 치명적 위험 존재)

- **📢 섹션 요약 비유**: 수술 중인 환자의 심장 박동을 단 한 번도 멈추지 않고, 인공 심폐기의 호스를 다른 병동의 기계로 완벽하게 스위칭하는 외과적 마법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 특징 | 비유 |
|:---|:---|:---|:---|
| **Source Node** | 현재 VM이 실행 중인 원본 물리 서버 | VM을 계속 구동시키며 메모리를 추출 | 이사 나가는 집 |
| **Target Node** | VM이 이동할 목적지 물리 서버 | Source에서 전송하는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 받아 빈 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 골격에 채워 넣음 | 이사 들어갈 빈 집 |
| **Shared Storage** | [NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)/[SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 기반 가상 디스크 (VMDK, qcow2) | 마이그레이션 시 '메모리'만 넘기면 됨. '디스크'는 네트워크로 전송하지 않고 공유함 | 원래부터 공용 창고에 있던 짐 |
| <strong>더티 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> (Dirty <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">Page</a>)</strong> | 마이그레이션 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중 Guest OS가 새롭게 수정(Write)한 메모리 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 Write-Protect를 걸어 [트랩](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)([Trap](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/))으로 추적 | 사진 찍은 뒤에 얼굴에 묻은 먼지 |

---

### Pre-copy (프리-카피) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 5단계 동작 원리

Pre-copy의 핵심은 라운드(Round)를 반복하면서 전송해야 할 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 양을 점근적으로 줄여나가는 것이다.

```text
  +-----------------------------------------------------------------------+
  |              Pre-copy 라이브 마이그레이션 5단계 파이프라인 (시간 순서)       |
  +-----------------------------------------------------------------------+
  |                                                                       |
  |  [Source Node (VM Running)]              [Target Node (VM Waiting)]   |
  |                                                                       |
  |  1. 준비 (Preparation)                                                |
  |     타겟 노드에 VM 껍데기(자원) 할당. 스토리지 접근권 확인.                  |
  |                                                                       |
  |  2. 반복적 사전 복사 (Iterative Pre-copy) <- [핵심!]                   |
  |     Round 1: 전체 메모리(예: 8GB) 전송 ---------------> 8GB 적재        |
  |              (전송하는 동안 VM은 계속 돌며 메모리 일부를 바꿈)              |
  |              하이퍼바이저는 바뀐 페이지(Dirty Page)를 비트맵에 기록.        |
  |                                                                       |
  |     Round 2: R1에서 발생한 Dirty Page(예: 1GB) 전송 --> 1GB 덮어쓰기     |
  |                                                                       |
  |     Round 3: R2에서 발생한 Dirty Page(예: 100MB) 전송 --> 100MB 덮어쓰기  |
  |                                                                       |
  |     ... (더티 페이지 양이 충분히 작아지거나, 최대 라운드 도달 시까지 반복) ... |
  |                                                                       |
  |  3. 중단 및 복사 (Stop-and-Copy / Downtime 구간)                       |
  |     VM 일시 정지 (CPU 멈춤). 남은 찰나의 Dirty Page(예: 10MB)와         |
  |     CPU 레지스터(Context) 최종 전송 -----------------> 마지막 동기화 완료 |
  |     * 이 단계의 시간이 사용자가 체감하는 Downtime (보통 < 50ms)           |
  |                                                                       |
  |  4. 커밋 및 재개 (Commit & Resume)                                     |
  |     Target Node의 VM이 최종 CPU 상태를 로드하고 실행 재개.               |
  |     네트워크 스위치에 무상태 ARP (Gratuitous ARP) 방송 ---> IP 라우팅 갱신|
  |                                                                       |
  |  5. 정리 (Teardown)                                                   |
  |     Source Node의 기존 VM 인스턴스 파기. 마이그레이션 종료.                 |
  +-----------------------------------------------------------------------+
```

**[다이어그램 해설]** 라이브 마이그레이션의 가장 큰 적은 '메모리를 쓰는 속도([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Dirty Rate)'가 '네트워크로 복사하는 속도(Network [Bandwidth](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))'보다 빠른 경우다. 이런 워크로드(예: 극심한 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부하를 내는 DB)는 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 줄어들지 않아 영원히 이사를 끝내지 못한다. 따라서 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 라운드를 반복하다가 전송량이 특정 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)(예: 50MB) 이하로 떨어지면, 즉시 Source VM의 CPU를 멈춰버린다(Stop). 그리고 그 남은 50MB와 CPU [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)만 휙 던진 뒤 Target VM을 깨운다. 마지막으로 네트워크 장비에 "내 IP 주소의 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소가 붙은 포트가 저쪽 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)로 바뀌었어!"라고 알려주는 [Gratuitous ARP](/studynote/03_network/06_network_layer_ip/316_gratuitous_arp_g_arp_ip_conflict_cache_update/) 패킷을 쏘아주면, 클라이언트와의 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)이 끊어지지 않고 계속 이어진다.

---

### 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 추적 (Dirty [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tracking) 기법

[하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 VM이 어떤 메모리를 수정했는지 알아내는 것은 마이그레이션의 심장과 같다. EPT([하드웨어 보조](/studynote/01_computer_architecture/15_advanced_topics/527_hardware_assisted_virtualization/) [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)) 환경에서 이를 구현하는 방법이다.

1. <strong>Write-Protect (PML4 <a href="/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/">트랩</a>)</strong>: 마이그레이션이 시작되면 VMM은 해당 VM의 모든 하드웨어 EPT ([Extended Page Table](/studynote/01_computer_architecture/15_advanced_topics/661_extended_page_table/)) 항목의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 권한(W) 비트를 0(Read-only)으로 바꾼다.
2. <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a> Exit 발생</strong>: Guest OS가 특정 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰려고 하면 하드웨어 폴트(EPT Violation)가 발생하며 VMM으로 제어권이 넘어온다.
3. <strong>더티 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> (Dirty Bitmap) 기록</strong>: VMM은 별도의 비트맵 자료구조에 "A [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 수정되었음"을 1로 기록한다.
4. <strong>권한 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong>: VMM은 해당 EPT 항목의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 권한을 다시 1로 돌려주고, Guest OS가 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 완료하게 둔다.
5. **다음 라운드 전송**: VMM은 비트맵에서 1로 표시된(더티) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 긁어서 타겟 노드로 네트워크 전송한다. (최근에는 EPT 하드웨어 내부에 아예 `PML (Page Modification Logging)` 버퍼를 만들어 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Exit 없이 하드웨어가 직접 더티 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 쓰게 하는 최적화도 사용된다.)

- **📢 섹션 요약 비유**: 이삿짐센터 직원이 물건을 다 포장해 놨는데, 주인이 계속 박스를 열어 물건을 바꿉니다. 직원은 박스마다 '봉인 스티커(Write-Protect)'를 붙여두고, 스티커가 뜯어진(Dirty) 박스만 마지막에 다시 포장해서 트럭에 싣는 원리입니다.

---

## Ⅲ. 비교 및 연결

### 라이브 마이그레이션 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 동작 방식 | 다운타임(Downtime) | 실패 위험 (안정성) | 적합한 워크로드 |
|:---|:---|:---|:---|:---|
| **Cold Migration** | 멈춤 $\rightarrow$ 전체 전송 $\rightarrow$ 재개 | 매우 김 (수 분) | 안전함 | 무중단이 필요 없는 일반 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) |
| **Pre-copy (표준)** | 반복적 사전 복사 $\rightarrow$ 짧게 멈춤 $\rightarrow$ 재개 | **매우 짧음 (< 50ms)** | 안전 (Source 보존) | 일반적인 클라우드 워크로드 |
| **Post-copy** | 짧게 멈춤 $\rightarrow$ CPU만 먼저 전송/재개 $\rightarrow$ [Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 시 메모리 당겨옴 | 거의 없음 (시작 시) | <strong>위험 (네트워크 끊기면 <a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a> 파괴됨)</strong> | 메모리 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 극도로 많은 DB 등 (Pre-copy 실패 시) |

### 과목 융합 관점

- **네트워크 (NW)**: 마이그레이션의 최종 성공은 <strong><a href="/studynote/03_network/06_network_layer_ip/316_gratuitous_arp_g_arp_ip_conflict_cache_update/">Gratuitous ARP</a> (GARP)</strong>에 달려 있다. 물리적 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 테이블(CAM Table)이 갱신되지 않으면, 외부에서 들어오는 트래픽이 옛날 물리 서버(Source)로 가버려 통신이 끊긴다. GARP는 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들에게 묻지도 않았는데 선제적으로 "나 여기로 이사 왔어!"라고 방송하여 L2 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 즉각 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 네트워크 과목의 핵심 기법이다.
- <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템 (Distributed OS)</strong>: CPU 상태(Registers, [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))와 메모리만 넘긴다고 끝이 아니다. VM에 할당된 가상 네트워크 인터페이스(vNIC)의 내부 링 버퍼 상태, 가상 디스크 컨트롤러(Virtio-blk)의 I/O 플라이트 상태 등 모든 <strong>디바이스 모델의 <a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a></strong>를 직렬화(Serialization)하여 넘기는 메커니즘이 필수적이다.

- **📢 섹션 요약 비유**: Pre-copy는 짐을 완벽히 다 옮긴 후 옛날 집을 부수는 '안전한 이사'이고, Post-copy는 사람부터 일단 새집에 보내놓고 칫솔, 수건이 필요할 때마다 옛날 집에 퀵서비스를 부르는 '도박성 이사'입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 메모리 집약적 워크로드의 라이브 마이그레이션 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/">타임아웃</a> 실패</strong>: 64GB 램을 쓰는 [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) DB VM이 들어있는 호스트를 긴급 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패치하기 위해 Evacuation(vMotion)을 시도했으나, 1시간째 99%에서 멈춰있다가 마이그레이션 실패(Abort) 에러가 떨어졌다.
   - **원인 분석**: DB가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰는 속도([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Dirty Rate)가 두 호스트를 잇는 10Gbps 관리망 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)보다 커서 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 끝없이 생성되는 발산(Divergence) 현상이 발생했다.
   - **대응 (기술사적 가이드)**:
     1. <strong>네트워크 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a> 확장</strong>: 마이그레이션 전용 네트워크 망([VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/))을 25Gbps 또는 다중 링크(LACP)로 증설한다.
     2. **Auto Converge 활성화**: [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)([KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/)/ESXi) 옵션에서 `auto-converge`를 켠다. 이는 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 안 줄어들면, 원본 VM의 가상 CPU(vCPU)에 억지로 쓰로틀링(Throttling, 실행 속도 저하)을 걸어 메모리를 천천히 쓰게 만들어 강제로 수렴시키는 튜닝이다.
     3. **하이브리드 마이그레이션**: 정 안되면 Pre-copy 도중에 Post-copy로 강제 전환([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))하는 기능을 사용한다.

2. <strong>시나리오 — <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 패스스루(<a href="/studynote/02_operating_system/10_security/657_vfio_virtual_function_io_passthrough/">Passthrough</a>) 가상머신의 마이그레이션 제약</strong>: [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 학습을 위해 물리 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)([PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/))가 직접 꽂힌 VM은 클라우드 환경에서 라이브 마이그레이션이 원천적으로 불가능하다.
   - **이유**: IOMMU를 통해 하드웨어를 직접 제어하고 있으므로, [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 내부의 VRAM과 디바이스 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 상태를 캡처할 방법이 없다.
   - **대응**: 이런 워크로드는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)/K8s 레벨에서 애플리케이션 자체가 체크포인트(Checkpoint)를 수시로 저장하고, 노드가 죽으면 다른 노드에서 체크포인트부터 다시 학습을 재개하는 '애플리케이션 레벨의 고가용성(HA)' 아키텍처로 선회해야 한다. (또는 NVIDIA vGPU 소프트웨어의 최신 라이브 마이그레이션 기능 한정적 적용)

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 라이브 마이그레이션 병목 트러블슈팅 의사결정 플로우          |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [vCenter/OpenStack에서 VM 마이그레이션이 90% 대에서 장기 정체됨]       |
  |                |                                                  |
  |                v                                                  |
  |      하이퍼바이저 관리망 네트워크 대역폭(Bandwidth) 포화 상태인가?         |
  |          +- 예 ------> [메모리 압축(Memory Compression) 옵션 활성화]    |
  |          |            (전송 전 압축하여 대역폭 한계 극복, CPU 부하 증가)    |
  |          +- 아니오                                                |
  |                |                                                  |
  |                v                                                  |
  |      VM의 메모리 쓰기 빈도(Page Dirty Rate)가 비정상적으로 높은가?         |
  |          +- 예 ------> [Auto-Converge (vCPU 쓰로틀링) 강제 적용]       |
  |          |            또는 [Post-copy 모드로 Fallback 허용]           |
  |          +- 아니오 ---> 스토리지(SAN) I/O 병목 여부 점검                 |
  |                         (공유 스토리지가 아닌 Block Migration 중일 경우)  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 라이브 마이그레이션은 "수학적 술래잡기"다. VMM(술래)이 네트워크 망을 통해 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 쫓아가고, [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)(도망자)은 계속 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 더럽힌다. 도망자가 너무 빠르면 1) 망을 넓히거나(10G$\rightarrow$25G), 2) 술래의 속도를 올리거나(메모리 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)), 3) 도망자의 다리를 걸어야 한다(Auto-Converge vCPU Throttling). 이 세 가지 카드를 시스템 상황(CPU 여유, 네트워크 여유, VM의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 민감도)에 맞춰 꺼내는 것이 아키텍트의 역할이다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **네트워크 관점**: Source와 Target 노드가 동일한 L2 브로드캐스트 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)(Subnet)에 있는가? (L3 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 구간을 넘어가면 [ARP](/studynote/03_network/06_network_layer_ip/312_arp_address_resolution_protocol_ip_to_mac/) 전파와 IP 보존에 심각한 문제가 발생하므로, VXLAN이나 Overlay NW 구성이 선행되어야 함)
- **스토리지 관점**: 두 호스트가 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)/[iSCSI](/studynote/01_computer_architecture/15_advanced_topics/698_iscsi/) SAN이나 [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)/Ceph 같은 공유 스토리지(Shared Storage)를 마운트하고 있어, 디스크 자체는 복사할 필요 없이 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))만 넘겨받을 수 있는 구조인가?

- **📢 섹션 요약 비유**: 이삿짐센터(VMM)가 짐을 나르는 속도보다, 주인이 방을 어지르는 속도(Dirty Rate)가 빠르면 이사는 끝이 안 납니다. 이때는 강제로 주인을 잠깐 소파에 묶어두는(Auto-Converge) 결단이 필요합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | Cold Migration (다운타임 허용) | Live Migration (Pre-copy) | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단: 수 초 ~ 10분 이상 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단: **수십 ms (밀리초)** | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 연결 및 사용자 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 유지 (무중단 99.999% 달성) |
| **정량** | 인프라 관리자 야간 작업 필수 | 자동화된 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)([DRS](/studynote/01_computer_architecture/15_advanced_topics/804_drs_storage_mirroring/))에 의한 주간 작업 | 유지보수 공수 [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) 및 [TCO](/studynote/12_it_management/01_governance_strategy/016_tco/) 절감 |
| **정성** | 하드웨어 장애 시 대규모 [클레임](/studynote/09_security/11_iam_access_control/539_claims/) | 노드 장애 예견 시 사전 대피(Evacuation) | 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약([SLA](/studynote/12_it_management/02_itsm_itil/869_sla/))의 강력한 무기 |

### 미래 전망
- <strong>원격 메모리(<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>) 시대의 마이그레이션 <a href="/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/">제로화</a></strong>: [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)([Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 기술이 완성되면, VM의 주 메모리가 CPU 섀시가 아닌 공용 [메모리 풀](/studynote/02_operating_system/06_memory_management/369_memory_pool/) 랙([Memory Pool](/studynote/02_operating_system/06_memory_management/369_memory_pool/) Rack)에 존재하게 된다. 이때는 수십 GB의 메모리를 복사할 필요 없이, 단 1밀리초 만에 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 '포인터'만 다른 CPU로 돌려버리면 마이그레이션이 즉각 종료되는 혁명적 아키텍처로 진화할 것이다.
- <strong><a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 기반 패킷 무손실 전송</strong>: Stop-and-Copy 단계의 찰나의 시간 동안 날아오는 네트워크 패킷들이 Drop(손실)되지 않도록, eBPF를 이용해 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단에서 패킷을 잠시 버퍼링해두었다가 Target 노드로 즉시 리다이렉트하는 초저지연 패킷 보존 기술이 적용되고 있다.

### 결론
라이브 마이그레이션(Pre-copy [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))은 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 기술이 이룩한 가장 화려한 마술이자, 현대 클라우드 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터를 '멈추지 않는 거대한 하나의 컴퓨터([SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/))'로 만든 일등 공신이다. 더티 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 추적과 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 스케줄링이 정교하게 맞물린 이 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅의 극한을 보여주며, 인프라 엔지니어가 반드시 숙지해야 할 OS와 네트워크의 완벽한 융합 사례다.

- **📢 섹션 요약 비유**: 궤도를 도는 인공위성([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))의 부품을 우주 공간에서 단 1초의 추락도 없이 새로운 위성으로 스왑(Swap)하는, 인류가 만든 가장 정교한 소프트웨어 우주쇼입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [IOMMU](/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) (Input/Output [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/)) 역할 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [컨테이너 런타임](/studynote/02_operating_system/10_security/628_container_runtime_oci/) ([runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/), containerd) [OCI](/studynote/13_cloud_architecture/05_data_engineering/333_process/) 규격 표준화 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [가상 스위치](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/) ([vSwitch](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/)) 패킷 오버헤드 [VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) 구조 적용 방식 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 메모리 KSM ([Kernel Samepage Merging](/studynote/02_operating_system/10_security/631_ksm_kernel_samepage_merging/)) 가상머신 간 중복 메모리 통합 절약 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[컨테이너 런타임 (runc, containerd) OCI 규격 표준화]
    |
    v
[라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식]
    |
    +---> [가상 스위치 (vSwitch) 패킷 오버헤드 VNF 구조 적용 방식]
    +---> [메모리 KSM (Kernel Samepage Merging) 가상머신 간 중복 메모리 통합 절약]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 멈추지 않고 달리는 기차(가상머신)를 통째로 다른 선로로 옮기는 마술이 라이브 마이그레이션이에요.
2. 기차를 한 번에 들 수는 없으니까, 기차가 달리는 동안 몰래 똑같은 빈 기차를 옆 선로에 만들고 승객(메모리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 한 명씩 밧줄로 옮겨 태워요(프리-카피).
3. 남은 승객이 딱 1명일 때, 0.01초 만에 조종석(CPU)을 옆 기차로 넘기면 덜컹! 하는 느낌도 없이 기차 이사가 완벽하게 끝난답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 629 / 800

<- **이전**: [628. 컨테이너 런타임 (runc, containerd) OCI 규격 표준화](/studynote/02_operating_system/10_security/628_container_runtime_oci/)
**다음**: [630. 가상 스위치 (vSwitch) 패킷 오버헤드 VNF 구조 적용 방식](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/) ->

---
