+++
title = "248. DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DTP와 VTP는 수십~수백 대의 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 엮인 거대한 기업망에서, 관리자가 일일이 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 뚫고 VLAN을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 <strong>"수작업 노가다"를 없애기 위해 시스코(<a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/">Cisco</a>)가 독자 개발한 자동화 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>이다.
> 2. **가치**: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)끼리 선을 꽂기만 하면 양쪽 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 알아서 대화를 나누고 "우리 서로 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 합시다!"라고 동적으로 협상해 주는(Negotiation) 편리하지만 보안에 취약한 링크 자동화 기술이다.
> 3. **판단 포인트**: 중앙의 마스터 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(Server)에 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), 20을 만들어 두면, 연결된 나머지 하급 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)([Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))들에게 그 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 목록(DB)이 자동으로 동기화되어 복사되는 중앙 집중식 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 관리 기술이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>DTP (Dynamic Trunking <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a>)</strong>: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 상대방 장비를 감지해 Access로 동작할지 Trunk로 동작할지 자동으로 결정하는 시스코 전용 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/).
  - <strong>VTP (<a href="/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/">VLAN</a> Trunking <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a>)</strong>: 한 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)/삭제/수정된 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)([vlan](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/).dat)를 트렁크 링크를 통해 네트워크 내 다른 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들과 자동 동기화하는 시스코 전용 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/).
- **필요성**: 만약 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 50대 있는 대학교 네트워크에 '컴퓨터공학과([VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 30)'를 새로 추가한다고 가정해 보자. VTP가 없다면 관리자는 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 50대에 일일이 원격 접속해 `vlan 30` 명령어를 50번 쳐야 한다. 또한 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들을 연결하는 수십 개의 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 일일이 `switchport mode trunk`로 세팅해야 한다. 이 극악의 비효율성을 버튼 하나(자동화)로 끝내기 위해 발명되었다.

- **💡 비유**:
  - **DTP**: 소개팅 자리에서 "우리 오늘부터 1일 할까요?(Trunk)"라고 물어보고 상대가 "네!" 하면 자동으로 사귀는(자동 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)) 기능입니다.
  - **VTP**: 본사 프랜차이즈(Server)에서 "내일부터 마라탕([VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 30) 신메뉴 출시해!"라고 공지를 띄우면, 전국 모든 가맹점([Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))의 메뉴판에 마라탕이 자동으로 똑같이 등록되는 시스템입니다.

```text
[접근 포트 / 트렁크 포트]
    |
    v
[DTP / VTP]
    |
    +---> [ISL]
```

- **📢 섹션 요약 비유**: <strong> DTP와 VTP는 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a> 네트워크를 구성할 때 관리자의 야근을 줄여주는 </strong>"자동 연결(DTP)" 및 "자동 복사(VTP)"** 치트키입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. DTP의 동작 모드와 협상
시스코 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 기본적으로 `Dynamic Desirable` 또는 `Dynamic Auto` 모드로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어 있어 쉴 새 없이 DTP 협상 패킷을 내보낸다.
- **Dynamic Desirable (적극적)**: "나랑 트렁크 맺자!"라고 먼저 들이대는 모드. 상대방이 Auto이거나 Desirable이면 트렁크가 맺어진다.
- **Dynamic Auto (수동적)**: 가만히 있다가 상대가 트렁크 맺자고(Desirable) 오면 "그래~" 하고 트렁크로 변하는 모드. (Auto끼리 만나면 둘 다 가만히 있으므로 Access [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 됨)

**⚠️ DTP 보안 취약점**: 해커가 노트북에 칼리리눅스(Kali)를 깔고 랜선을 빈 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 꽂은 뒤 "나랑 트렁크 맺자!"(DTP Desirable 패킷 발송)라고 쏘면, 멍청한 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 노트북과 트렁크를 맺어버린다. 해커는 트렁크 라인을 타고 흐르는 회사의 모든 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 데이터를 다 엿볼 수 있게 된다. 따라서 실무에서는 반드시 <strong>DTP 기능을 강제로 끄고 수동 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>(Static Trunk)</strong>을 권장한다 (`switchport nonegotiate`).

### 2. VTP의 3가지 모드와 리비전 번호 (Revision Number)
VTP 영역([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))으로 묶인 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들은 3가지 모드 중 하나를 갖는다.
1. **Server 모드**: 대장. VLAN을 직접 만들고 지울 수 있으며, 부하들에게 전파한다.
2. <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/">Client</a> 모드</strong>: 부하. VLAN을 스스로 만들지 못하고, 서버가 하라는 대로 자신의 메뉴판을 똑같이 덮어쓴다.
3. **Transparent 모드**: 방관자. VTP 메시지가 들어오면 남에게 전달(Bypass)은 해주지만, 자기 자신은 동기화하지 않고 독자적인 VLAN을 갖는다.

```text
 +-------------------------------------------------------------+
 |                VTP 리비전 번호 폭탄(Bomb) 사고                |
 +-------------------------------------------------------------+
 |                                                             |
 |   [ Main Switch (Server) ] ---- 트렁크 ---- [ Switch B (Client) ] |
 |    VLAN 10, 20, 30 존재                       (정상 동기화 중)  |
 |    Revision Number: 15                                      |
 |                                                             |
 |   ⚠️ 사고 발생 시나리오:                                        |
 |   다른 테스트망에서 막 쓰다가 'Revision Number가 50'까지 올라가 버린 |
 |   고물 스위치(Server 모드)를 실수로 회사 메인망에 꽂음!              |
 |                                                             |
 |   [ 고물 스위치 ] "야! 내 리비전이 50이야! 내 걸로 다 덮어써!"       |
 |   [ Main Switch ] "헉 50이 최신이네! 내 거 15짜리 다 지우고 덮어쓸게!"|
 |                                                             |
 |   -> 결과: 회사의 전사 VLAN(10, 20, 30)이 순식간에 다 삭제되고      |
 |          인터넷 전면 마비 (네트워크 셧다운).                        |
 +-------------------------------------------------------------+
```

**⚠️ VTP 보안 취약점**: VTP는 누가 보냈든 무조건 <strong>수정 횟수(Revision Number)가 자기보다 더 높은 놈의 말을 무조건 최신 정보로 믿고 덮어쓰는(Overwrite) 멍청한 특징</strong>이 있다. 테스트용 장비를 잘못 꽂았다가 회사 전체 네트워크가 날아가는 사고(VTP Bomb)가 잦아, 현대 실무에서는 VTP 역시 잘 쓰지 않고 [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) 같은 외부 자동화 툴을 사용한다.

- **📢 섹션 요약 비유**: ** DTP와 VTP는 묻지도 따지지도 않고 자동으로 세팅해 주는 **"편리한 마법 지팡이"**지만, 해커나 초보 관리자의 실수 한 번에 회사 전체 네트워크를 날려버릴 수 있는 **"시한폭탄"**과도 같아서 실무에서는 봉인해 두는 기술입니다.

---

## Ⅲ. 비교 및 연결

DTP / VTP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [접근 포트](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/) / 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 기반 조건을 만든다면, DTP / VTP는 그 위에서 핵심 메커니즘을 구현하고, ISL는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [접근 포트](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/) / 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)의 기반 정리 | DTP / VTP의 핵심 동작 | ISL의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: DTP / VTP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 DTP / VTP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [접근 포트](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/) / 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수준의 기본 대책으로 충분한지, 아니면 DTP / VTP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 ISL와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. DTP / VTP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 ISL와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- DTP / VTP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [접근 포트](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/) / 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: DTP / VTP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

DTP / VTP는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [ISL](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/249_isl_inter_switch_link_cisco/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: DTP / VTP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [접근 포트](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/) / 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [ISL](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/249_isl_inter_switch_link_cisco/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 접근 포트 / 트렁크 포트]
    |
    v
[현재 개념: DTP / VTP]
    |
    +---> [확장 A: ISL]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

DTP / VTP는 [접근 포트](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/) / 트렁크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에서 출발해 현재 메커니즘을 정교화하고, 이후 ISL와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 369 / 1120

<- **이전**: [247. 접근 포트 (Access Port) / 트렁크 포트 (Trunk Port)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/247_access_port_vs_trunk_port/)
**다음**: [249. ISL (Inter-Switch Link)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/249_isl_inter_switch_link_cisco/) ->

---
