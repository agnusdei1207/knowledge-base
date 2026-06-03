+++
title = "698. iSCSI (Internet Small Computer System Interface)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: iSCSI (Internet Small Computer System Interface)는 SCSI (Small Computer System Interface) 블록 명령을 [Transmission Control Protocol](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) / Internet [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) (IP) 위에 실어, 범용 [Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 네트워크를 통해 원격 디스크를 로컬 디스크처럼 보이게 하는 기술이다.
> 2. **가치**: 전용 [Fibre Channel](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) ([FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)) 장비 없이도 익숙한 IP 네트워크로 [Storage Area Network](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) ([SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))급 블록 스토리지를 구축할 수 있어, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)·[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·중견 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)에서 비용 대비 효율이 높다.
> 3. **판단 포인트**: 다만 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 처리와 네트워크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 추가되므로 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)보다 운영 단순성·[라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 유연성·경제성이 더 중요한 환경에 적합하다.

---

## Ⅰ. 개요 및 필요성

iSCSI는 "디스크 명령을 네트워크로 멀리 보내되, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유처럼 보이지 않고 <strong>여전히 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/">블록 장치</a>처럼 보이게 하자</strong>"는 요구에서 출발했다. [Direct Attached Storage](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/) ([DAS](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/339_das/))는 서버에 디스크를 직접 붙여 간단하지만, 여러 서버가 저장공간을 공유하거나 장애 대비 이중 경로를 만들기 어렵다. 반면 [Fibre Channel](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) ([FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)) SAN은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성이 뛰어나지만 Host [Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) (HBA), 전용 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), 광 인프라 비용이 높다.

이 사이에서 등장한 해법이 iSCSI다. 이미 기업망 대부분이 Ethernet과 IP를 사용하고 있으므로, SCSI 명령을 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 위에 올리면 스토리지 네트워크를 별도로 깔지 않고도 중앙집중형 블록 스토리지를 만들 수 있다. 즉 iSCSI의 핵심 가치는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극대화보다 <strong>블록 스토리지의 대중화</strong>에 있다.

- **📢 섹션 요약 비유**: iSCSI는 값비싼 전용 화물열차를 새로 놓는 대신, 이미 깔려 있는 고속도로 위에 튼튼한 택배 상자를 올려 보내는 방식과 같다. 조금 더 포장하고 확인해야 하지만, 훨씬 많은 곳에서 바로 쓸 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

iSCSI 구조의 기본 역할은 Initiator와 Target으로 나뉜다. Initiator는 서버 측에서 SCSI 요청을 만들어 보내는 주체이고, Target은 이를 받아 실제 디스크나 저장 배열에 반영하는 스토리지 장비다. 운영체제는 Target이 제공하는 [LUN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/685_lun_masking/) ([Logical Unit Number](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/685_lun_masking/))을 로컬 블록 디바이스처럼 인식하므로, 위쪽 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 네트워크 존재를 거의 의식하지 않는다.

iSCSI 연결은 보통 발견(Discovery), 로그인(Login), [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) 유지, 명령/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송의 순서로 진행된다. 기본 포트는 3260이며, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에는 [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/) (Challenge-Handshake [Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))을 자주 사용한다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 중요한 환경에서는 점보 프레임, 전용 Virtual Local Area Network ([VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/)), [Multipath](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) Input/Output (MPIO), 그리고 필요 시 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) Offload Engine ([TOE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/588_toe/)) 기능이 있는 어댑터를 함께 고려한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Initiator | 서버 측 iSCSI 클라이언트 | 소프트웨어 방식인지, 전용 HBA/[TOE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/588_toe/) 카드인지 |
| Target | 원격 블록 스토리지 제공자 | [LUN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/685_lun_masking/) 배치, 캐시 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 다중 경로 지원 |
| [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP 네트워크 | [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있는 전달과 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 혼잡, 점보 프레임, [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 분리 |
| [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/) | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | 운영 편의성과 [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/) 균형 |
| MPIO | 경로 이중화와 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간, 경로별 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 활용 |

아래 그림은 iSCSI가 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 아니라 **블록 명령을 IP망에 얹어** 전달하는 구조를 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">iSCSI data path: block storage over routed IP</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Application / File System</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SCSI commands</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">iSCSI Initiator on host</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TCP / IP / Ethernet</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Routed Ethernet network</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">iSCSI Target</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Remote LUN exposed as local block device</div></div>
</div>
</div>



iSCSI가 중요한 이유는 원격 저장장치를 단순 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버가 아니라 <strong>로컬 디스크처럼 다루게 만든다</strong>는 점이다. 그래서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/), 클러스터 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 자신이 직접 [블록 장치](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/)를 제어한다고 생각하며 동작할 수 있다.

- **📢 섹션 요약 비유**: iSCSI는 멀리 있는 창고의 서랍을 통째로 빌려 와서, 우리 사무실 책상 서랍처럼 쓰는 방식이다. 서랍은 멀리 있지만 열고 닫는 규칙은 내 책상 서랍과 거의 같다.

---

## Ⅲ. 비교 및 연결

iSCSI의 경계는 두 방향에서 드러난다. 하나는 FC처럼 더 전용화된 블록 스토리지와의 차이이고, 다른 하나는 [Network File System](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) ([NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)) 같은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유 방식과의 차이다. iSCSI는 IP 친화적이지만, 어디까지나 <strong>블록 단위 저장장치</strong>를 제공한다는 점에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위 [Network Attached Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) ([NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/))와 본질이 다르다.

| 항목 | [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) | iSCSI | [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) |
| :--- | :--- | :--- | :--- |
| 호스트가 보는 대상 | 원격 블록 디스크 | 원격 블록 디스크 | 원격 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 |
| 전송 기반 | [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 전용 패브릭 | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP/[Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP/[Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) |
| [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 유연성 | 낮음 | 높음 | 높음 |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)/CPU 부담 | 가장 낮은 편 | 중간 | 워크로드 의존적 |
| 적합한 용도 | 고성능 전용 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) | 범용 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/), [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/), 재해복구 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유, 콘텐츠, 협업 |

이 차이는 운영 방식도 바꾼다. iSCSI는 [블록 장치](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/)를 넘겨주므로 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, 볼륨 매니저를 호스트가 직접 다룬다. 따라서 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 클러스터나 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)처럼 블록 제어권이 중요한 환경에서 유리하다. 반대로 [파일 잠금](/knowledge-base/studynote/02_operating_system/09_file_system/567_file_locking_shared_exclusive/), [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 공유, 사용자 단위 접근 제어가 핵심이면 iSCSI보다 NFS나 Server Message Block (SMB)이 더 적합하다.

- **📢 섹션 요약 비유**: iSCSI는 창고의 빈 서랍을 빌려 주는 것이고, NFS는 이미 정리된 서류장을 함께 쓰게 해 주는 것이다. 서랍을 빌리면 자유는 크지만 정리는 내가 해야 하고, 서류장을 쓰면 편하지만 구조는 상대가 정해 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 iSCSI는 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 호스트 클러스터, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 저장소, 중견 기업 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/), 재해복구 사이트 연결에서 특히 많이 쓰인다. [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)/25 [Gigabit Ethernet](/knowledge-base/studynote/03_network/03_physical_layer_media/139_1000base_t_gigabit_ethernet/) 기반의 전용 스토리지 VLAN과 MPIO를 구성하면, 상당수 업무 시스템에서 충분한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 가용성을 확보할 수 있다. 또한 IP망을 그대로 활용할 수 있어, 다른 건물이나 다른 네트워크 구간으로 스토리지를 연장하기 쉽다.

### 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 스토리지 트래픽을 일반 사용자 트래픽과 분리할 전용 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 또는 별도 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 있는가?
2. MPIO가 구성되어 단일 링크/[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 장애 시에도 I/O가 지속되는가?
3. [CHAP](/knowledge-base/studynote/03_network/04_data_link_layer_error/228_chap_challenge_handshake_authentication_protocol/) 또는 [Internet Protocol Security](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) ([IPsec](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/)) 같은 보안 장치가 필요한 구간인지 평가했는가?
4. 서버 CPU가 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 처리를 감당할 수 있는가, 아니면 [TOE](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/588_toe/)/HBA 오프로드가 필요한가?
5. 장거리 구간이라면 왕복 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 애플리케이션 허용 범위 안에 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 웹 트래픽, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 트래픽, iSCSI 트래픽을 같은 저속 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 뒤섞어 두는 구성
- 고지연 구간에서 로컬 디스크처럼 반응할 것이라 기대하는 구성
- 다중 경로 없이 단일 링크 하나에만 의존하는 구성

기술사 답안에서는 iSCSI를 "싸지만 느린 기술"로 단순화하면 안 된다. 정확한 표현은 <strong>IP망의 유연성과 블록 스토리지의 제어권을 결합한 실용적 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/">SAN</a> 기술</strong>이며, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 네트워크 품질과 CPU 여유, 설계 완성도에 크게 좌우된다.

- **📢 섹션 요약 비유**: iSCSI는 대형마트 물류를 일반 도로망으로 운영하는 방식과 같다. 도로가 넓고 차선을 잘 나누면 매우 효율적이지만, 장보는 손님 차와 화물차를 한 차선에 섞어 놓으면 바로 막힌다.

---

## Ⅴ. 기대효과 및 결론

iSCSI의 가장 큰 공헌은 SAN을 전용 장비의 세계에서 꺼내 <strong>일반적인 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a>/IP 운영 문화 안으로 끌어온 것</strong>이다. 덕분에 더 많은 조직이 중앙집중형 블록 스토리지를 도입했고, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 재해복구 설계도 훨씬 쉬워졌다. 특히 기존 네트워크 지식과 장비를 재활용할 수 있다는 점은 총소유비용([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/)) 측면에서 매우 큰 장점이다.

물론 한계도 있다. 초저지연 고성능 환경에서는 FC나 최신 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)/[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) over [Transmission Control Protocol](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/))가 더 나은 선택일 수 있고, 잘못 설계된 iSCSI는 혼잡과 CPU 오버헤드 때문에 기대보다 훨씬 느려질 수 있다. 따라서 iSCSI는 <strong>"범용 IP망 위에서 가장 현실적인 블록 스토리지"</strong>라는 관점으로 기억하는 것이 가장 적절하다.

- **📢 섹션 요약 비유**: iSCSI는 누구나 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉬운 튼튼한 택배 시스템과 같다. 초고가 예술품 배송에는 더 특수한 수단이 필요할 수 있지만, 대부분의 회사 물류는 이 방식만 잘 설계해도 충분히 돌아간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| SCSI (Small Computer System Interface) | iSCSI가 네트워크로 운반하는 원래의 블록 명령 체계다. |
| [LUN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/685_lun_masking/) ([Logical Unit Number](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/685_lun_masking/)) | Target이 호스트에 노출하는 논리적 [블록 장치](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/) 단위다. |
| Initiator / Target | iSCSI [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)의 송신자와 수신자를 구분하는 기본 역할 모델이다. |
| MPIO ([Multipath](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) I/O) | 가용성과 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 높이기 위해 iSCSI 환경에서 거의 필수로 쓰이는 다중 경로 기술이다. |
| [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)/[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ([Non-Volatile Memory Express](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) over [Transmission Control Protocol](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) | iSCSI 이후 더 낮은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 높은 병렬성을 노리는 IP 기반 차세대 블록 스토리지다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">직접 연결 SCSI 저장장치</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Fibre Channel (FC) SAN</div>
<div class="kb-diagram-note">: 고성능 전용 패브릭</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">iSCSI (Internet Small Computer System Interface)</div>
<div class="kb-diagram-note">: TCP/IP 기반 블록 스토리지 대중화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">10/25/100 Gigabit Ethernet + MPIO (Multipath I/O)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">NVMe/TCP (Non-Volatile Memory Express over Transmission Control Protocol)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. iSCSI는 멀리 있는 큰 서랍장을 인터넷 길로 가져와 내 방 서랍처럼 쓰게 해 주는 방법이에요.
2. 그래서 비싼 특별한 길을 새로 만들지 않아도, 원격 저장공간을 편하게 사용할 수 있어요.
3. 대신 길이 막히면 서랍 여는 속도도 느려지니까, 길을 잘 나누고 정리해야 한답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 699 / 803

← **이전**: [697. FCoE (Fibre Channel over Ethernet)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/697_fcoe/)
**다음**: [699. NVMe 큐 쌍 (Queue Pairs)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/699_nvme_queue_pairs/) →

---
