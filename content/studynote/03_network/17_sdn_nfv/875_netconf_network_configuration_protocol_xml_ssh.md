+++
title = "875. NETCONF 프로토콜"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 이해하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- <strong>CLI (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/">Command</a> Line Interface)</strong>: 사람이 키보드로 쳐야 합니다. 스크립트(Expect)를 짜서 자동화하려 해도, 벤더마다 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(시스코어, 주니퍼어)가 다르고 결과 화면(텍스트)이 달라서 100% 에러가 터졌습니다.
- <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/528_snmp_simple_network_management_protocol/">SNMP</a> (Simple Network <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a>)</strong>: 원래 장비가 살아있는지 감시(모니터링)하려고 만든 툴입니다. 이걸 억지로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 바꾸는 데 쓰려다 보니, [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(실패 시 되돌리기) 개념이 없어서 중간에 끊기면 라우터가 반쯤 고장 난 상태로 멈춰버렸습니다.

```text
[P4 (Programming Protocol…]
    │
    ▼
[NETCONF 프로토콜]
    │
    └──▶ [YANG (Yet Another Next G…]
```

- **📢 섹션 요약 비유**: NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/)(국제 인터넷 표준화 기구)에서 제정한 <strong>네트워크 장비의 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(Configuration)와 상태 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a>)를 완벽하게 분리하여, 네트워크 장비를 원격에서 설치, 조작, 삭제하기 위한 차세대 표준 네트워크 관리 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>입니다. (사우스바운드 인터페이스의 대장)

### NETCONF의 4계층 구조 (완벽한 구조화) 🌟
NETCONF는 패킷을 보낼 때 4겹의 옷을 입습니다.
1. **보안 전송 계층 (Secure Transport)**:
   - 텔넷(Telnet) 같은 평문이 아니라, 무조건 <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">SSH</a> (<a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">Secure Shell</a>)</strong>나 TLS를 기반으로 암호화 파이프를 뚫어 해커의 감청을 완벽히 차단합니다.
2. **메시지 계층 (Message)**:
   - `<rpc>`, `<rpc-reply>` 태그를 사용하여 원격 절차 호출 구조(클라이언트-서버 통신)를 만듭니다.
3. **오퍼레이션 계층 (Operations) 🌟**:
   - `edit-config` ([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 바꿔라), `get-config` ([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 가져와라) 같은 핵심 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들이 들어갑니다.
4. **콘텐츠 계층 (Content - XML)**:
   - 멍청한 텍스트(CLI) 대신, 기계가 완벽하게 파싱해서 읽어 들일 수 있는 체계적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조인 **XML (eXtensible Markup Language)** 형식으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)값을 적어 보냅니다. (이 XML의 뼈대를 잡아주는 문법이 바로 876번의 <strong>YANG</strong>입니다.)

```text
[P4 (Programming Protocol…]
    │
    ▼
[NETCONF 프로토콜]
    │
    └──▶ [YANG (Yet Another Next G…]
```

- **📢 섹션 요약 비유**: NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

DB([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/))에서 쓰던 기법을 네트워크 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 이식한 최고의 마법입니다.

- <strong>분리된 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 공간 (Datastore)</strong>: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 안에 `<running>` (현재 돌아가고 있는 진짜 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))과 `<candidate>` (테스트용 예비 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)) 공간을 분리해 두었습니다.
- **Commit (저장)**: 관리자가 1,000대의 장비에 100줄의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 쏩니다. 이 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 일단 예비 공간(`<candidate>`)에 안전하게 저장됩니다. 모든 게 완벽하다고 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)되면, 관리자가 `<commit>` 버튼을 눌러 그 즉시 진짜 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(`<running>`)으로 덮어씌웁니다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/">Rollback</a> (원상 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>)</strong>: 만약 1,000대 중 1대의 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에서 에러가 터지면? `Rollback` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 한 방에 1,000대의 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 1초 만에 어제 상태로 완벽히 되돌아갑니다. 네트워크가 엉망진창으로 꼬이는 것을 원천 차단합니다.

NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [P4](/knowledge-base/studynote/03_network/17_sdn_nfv/874_p4_programming_data_plane_pipeline_int_telemetry/) (Programming [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)…가 기반 조건을 만든다면, NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 그 위에서 핵심 메커니즘을 구현하고, YANG (Yet Another Next G…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [P4](/knowledge-base/studynote/03_network/17_sdn_nfv/874_p4_programming_data_plane_pipeline_int_telemetry/) (Programming [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)…의 기반 정리 | NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 핵심 동작 | YANG (Yet Another Next G…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- 852번 문서에서 배운 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러(ONOS 등)가 밑바닥의 수만 대 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들을 지배할 때, 화이트박스 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 룰은 OpenFlow로 내리지만, 그 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 IP 주소, 인터페이스 ON/OFF 같은 기계적 환경 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(Configuration)은 100% 이 NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 사용해 XML로 찍어누릅니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기존 장비 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(CLI)은 '카톡으로 문서 편집 지시하기'입니다. "3페이지 두 번째 줄 지우고 글씨 빨간색으로 바꿔"라고 말하면, 듣는 직원([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))이 헷갈려서 엉뚱한 곳을 지우다가 문서를 망치고 되돌릴 수도 없습니다([롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 불가). <strong>NETCONF</strong>는 '구글 독스(Google Docs)를 통한 원격 문서 공동 편집' 시스템입니다. 관리자는 보안이 철저한 전용 회선([SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/))을 타고 들어와, 기계가 완벽히 인식하는 표 양식(XML)으로 깔끔하게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 적습니다. 게다가 먼저 '임시 저장소(Candidate)'에 글을 써보고, 오타가 나서 문서를 망치면 'Ctrl+Z ([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))' 버튼을 눌러 1초 만에 원상 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)합니다. 모든 게 완벽할 때만 '최종 발행(Commit)' 버튼을 눌러 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 구동시키는, 기계와 인간의 가장 안전하고 정밀한 대화법입니다.

---

## Ⅴ. 기대효과 및 결론

NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 YANG (Yet Another Next G…, 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [P4](/knowledge-base/studynote/03_network/17_sdn_nfv/874_p4_programming_data_plane_pipeline_int_telemetry/) (Programming [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 경로 결정을 담당한다. |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane) | 실제 패킷 전달을 수행한다. |
| YANG (Yet Another Next G… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: P4 (Programming Protocol…]
    │
    ▼
[현재 개념: NETCONF 프로토콜]
    │
    ├──▶ [확장 A: YANG (Yet Another Next G…]
    └──▶ [확장 B: 프로그래머블 네트워크]
```

NETCONF [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)는 [P4](/knowledge-base/studynote/03_network/17_sdn_nfv/874_p4_programming_data_plane_pipeline_int_telemetry/) (Programming [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)…에서 출발해 현재 메커니즘을 정교화하고, 이후 YANG (Yet Another Next G…와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 996 / 1120

← **이전**: [874. 데이터 평면 프로그래밍 모델 (P4)](/knowledge-base/studynote/03_network/17_sdn_nfv/874_p4_programming_data_plane_pipeline_int_telemetry/)
**다음**: [876. YANG 데이터 모델링](/knowledge-base/studynote/03_network/17_sdn_nfv/876_yang_yet_another_next_generation_data_modeling/) →

---
