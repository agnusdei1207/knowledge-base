---
title: "257. Stp 4 States Blocking Listening Learning Forwarding"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 랜선을 꽂았다고 해서 바로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(인터넷)가 통과하는 것이 아니라, [스패닝 트리 프로토콜](/studynote/03_network/05_lan_wan_l2_devices/253_spanning_tree_protocol_stp_ieee_802_1d/)([STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/))이 혹시 모를 루프(Loop)를 감지하고 예방하기 위해 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 <strong>4단계의 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a> 절차(<a href="/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/">상태 전이</a>)</strong>를 거쳐 서서히 열어준다.
> 2. **가치**: [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 <strong>차단(<a href="/studynote/02_operating_system/02_process_thread/122_sync_async_communication/">Blocking</a>) ---> 청취(Listening) ---> 학습(<a href="/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a>) ---> 전송(Forwarding)</strong>의 4단계를 순서대로 거치며, 중간에 루프 위험이 발견되면 언제든지 다시 차단([Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 상태로 되돌아간다.
> 3. **판단 포인트**: 이 엄격한 검역 절차 덕분에 링(Ring) 구조에서 브로드캐스트 스톰이 일어나지 않지만, PC를 꽂고 나서 통신이 되기(Forwarding)까지 무려 <strong>약 30~50초라는 매우 긴 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong>을 감수해야만 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 물리적 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 링크업(Link-up) 되었을 때, 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전달(Forwarding)하기 전까지 반드시 거쳐야 하는 내부 소프트웨어적인 상태([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))의 흐름이다.
- **필요성**: 만약 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 랜선을 꽂자마자 1초 만에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송이 확 열려버리면 어떻게 될까? 사용자가 장난으로 양쪽 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 둥글게 루프로 꽂았을 때, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들이 "이거 루프네? 끊어야겠다!"라고 계산([BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/) 교환)하기도 전에 수만 개의 트래픽이 쏟아져 들어가 망이 즉시 폭파된다. 따라서 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 처음 선이 꽂히면 일단 문을 걸어 잠그고 밖의 동태를 살피는 '안전 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 시간'이 절대적으로 필요하다.

- **💡 비유**: 비행기에 탑승(랜선 연결)하자마자 바로 이륙([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송)할 수는 없습니다. 기장은 먼저 문을 닫고([Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)), 관제탑과 무전을 주고받으며 이륙 허가를 듣고(Listening), 비행기 계기판을 세팅하며 활주로를 구른([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 뒤에야, 비로소 창공을 향해 날아오릅니다(Forwarding).

```text
[브리지 ID, 비용]
    |
    v
[STP 4단계 상태 전이]
    |
    +---> [컨버전스 시간]
```

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/">STP</a> 4단계는 건물을 짓기 전 지반이 튼튼한지 검사하는 </strong>"안전 진단 기간"**입니다. 루프라는 싱크홀이 없는지 한참을 두드려본 후에야 비로소 인터넷이라는 건물을 올리기 시작합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Disabled (비활성화)
[포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 아예 관리자에 의해 꺼져있거나(`shutdown`), 물리적으로 랜선이 뽑혀 있는 0단계 상태.

### 2. [Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) (차단 상태) - "가만히 듣기만 해라"
[포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 랜선이 꽂히면 가장 먼저 진입하는 상태다.
- **동작**: 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(웹서핑 패킷 등)는 절대 통과시키지 않는다. 오로지 다른 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들이 보내는 <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/">BPDU</a> 엽서만 조용히 수신</strong>하며 마을의 대장이 누군지, 루프가 있는지 눈치를 본다.
- **지속 시간**: 이 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 차단 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(Block [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))로 결정되면 평생 이 상태에 머문다. 포워딩 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(DP, [RP](/studynote/03_network/07_network_layer_routing/370_pim_rp_rendezvous_point_rpf_loop_prevention/))로 나가야 한다고 판정되면 즉시 다음 단계로 넘어간다. (장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시에는 Max Age 20초 대기 발생)

### 3. Listening (청취 상태) - "나도 명함을 돌려볼까?"
- **동작**: 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 여전히 차단된다. 하지만 이제 남의 BPDU를 듣기만 하는 게 아니라, <strong>나의 <a href="/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/">BPDU</a>(명함)를 만들어 상대방에게 전송</strong>하기 시작한다.
- "이 선의 주인(DP)은 나야!"라고 서로 선거 유세를 벌이며 옥신각신하는 기간이다. 만약 유세에서 지면 다시 Blocking으로 쫓겨난다.
- **지속 시간**: 15초 ([Forward](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Delay)

### 4. [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) (학습 상태) - "동네 지도를 그려라"
- **동작**: 승리가 확정되어 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 열기로 한 상태다. 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송은 아직 안 되지만, 이 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 들어오는 프레임의 출발지 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 슬쩍슬쩍 훔쳐보며 <strong><a href="/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소 테이블(CAM Table)을 부지런히 채워 넣기 시작</strong>한다. (문을 열기 전 지도부터 그리는 것)
- **지속 시간**: 15초 ([Forward](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Delay)

### 5. Forwarding (전송 상태) - "문이 열리네요"
- **동작**: 모든 안전 검사가 끝났다! 드디어 <strong>사용자 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(IP 패킷 등)를 주고받을 수 있는 완전한 통신 개통 상태</strong>다. [BPDU](/studynote/03_network/05_lan_wan_l2_devices/254_bpdu_bridge_protocol_data_unit/) 전송과 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 학습도 동시에 계속 이루어진다.

```text
 +-------------------------------------------------------------+
 |                STP 포트 상태 전이 타이밍 (요약)                 |
 +-------------------------------------------------------------+
 |                                                             |
 |   [ Link UP ! ] (랜선 꽂힘)                                   |
 |       |                                                     |
 |       v                                                     |
 |   [ Blocking ]   ---> (사용자 데이터 ❌ / BPDU 수신 ⭕)          |
 |       | 즉시 이동                                             |
 |       v                                                     |
 |   [ Listening ]  ---> (사용자 데이터 ❌ / BPDU 송수신 ⭕)        |
 |       | 15초 소요                                            |
 |       v                                                     |
 |   [ Learning ]   ---> (사용자 데이터 ❌ / MAC 주소 학습 시작 ⭕) |
 |       | 15초 소요                                            |
 |       v                                                     |
 |   [ Forwarding ] ---> (사용자 데이터 ⭕ / 정상 통신 개시!)        |
 |                                                             |
 |  * 결론: 랜선을 꽂고 실제로 인터넷이 되기까지 "최소 30초"가 걸린다!    |
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/">STP</a> 4단계는 신병 훈련소입니다. 입소하자마자 제자리에 엎드려 조교의 말만 듣고(</strong>[Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)**), 점호 때 목소리를 크게 내보고(**Listening**), 군대 수칙을 머릿속에 외운(**[Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)**) 뒤에야 비로소 자대에 배치되어 총을 쏘며 작전을 수행(**Forwarding**)하게 됩니다.

---

## Ⅲ. 비교 및 연결

[STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID, 비용이 기반 조건을 만든다면, [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 그 위에서 핵심 메커니즘을 구현하고, [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID, 비용의 기반 정리 | [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)의 핵심 동작 | [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID, 비용 수준의 기본 대책으로 충분한지, 아니면 [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID, 비용와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID, 비용 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 브리지 ID, 비용]
    |
    v
[현재 개념: STP 4단계 상태 전이]
    |
    +---> [확장 A: 컨버전스 시간]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

[STP](/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 4단계 [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ID, 비용에서 출발해 현재 메커니즘을 정교화하고, 이후 [컨버전스 시간](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/)와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 378 / 1120

<- **이전**: [256. 브리지 ID (Priority + MAC), 비용 (Path Cost)](/studynote/03_network/05_lan_wan_l2_devices/256_bridge_id_priority_mac_and_path_cost/)
**다음**: [258. 컨버전스 시간 (STP 약 30~50초 소요)](/studynote/03_network/05_lan_wan_l2_devices/258_stp_convergence_time_30_50_seconds/) ->

---
