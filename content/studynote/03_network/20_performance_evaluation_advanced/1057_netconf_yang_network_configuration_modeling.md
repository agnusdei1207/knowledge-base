---
title: "1057. Netconf Yang Network Configuration Modeling"
tags:
  - "network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: YANG은 네트워크 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)의 구조와 규칙을 정의하는 모델이고, NETCONF는 그 모델을 장비에 안전하게 주입하는 전송 프로토콜이다.
> 2. **가치**: CLI 수작업과 [SNMP](/studynote/03_network/10_application_layer_dns_mgmt/528_snmp_simple_network_management_protocol/) (Simple Network [Management](/studynote/12_it_management/05_security_compliance/1013_management/) [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 중심의 한계를 넘어, 선언형 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)을 가능하게 한다.
> 3. **판단 포인트**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델의 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) ([Secure Shell](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)) 기반 전송, candidate/running datastore 분리가 핵심이다.

---

## Ⅰ. 개요 및 필요성

기존 CLI ([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Line Interface) 방식은 장비마다 명령어가 다르고, 사람이 직접 타이핑해야 해서 실수가 잦다.

[SNMP](/studynote/03_network/10_application_layer_dns_mgmt/528_snmp_simple_network_management_protocol/) (Simple Network [Management](/studynote/12_it_management/05_security_compliance/1013_management/) [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))는 모니터링에는 강하지만, 복잡한 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 안전하게 쓰는 데는 약했다. 그래서 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 자동화를 위한 새로운 규격이 필요했다.

- **📢 섹션 요약 비유**: 예전에는 네트워크 장비를 하나하나 손으로 만졌다면, 이제는 도면을 넣고 자동 조립하는 시대다.

---

## Ⅱ. YANG의 역할

YANG은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델링 언어다. 즉, 네트워크 장비의 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 어떤 트리 구조를 가져야 하는지, 어떤 값이 허용되는지 정의한다.

```text
루트
 +- interfaces
 |   +- interface
 |   +- state
 +- routing
 +- system
```

YANG은 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 값의 범위, 필수 항목, 중복 여부까지 표현할 수 있다. 그래서 잘못된 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 장비에 넣기 전에 구조 단계에서 걸러낼 수 있다.

- **📢 섹션 요약 비유**: YANG은 건물을 짓기 전에 필요한 방의 모양과 크기를 미리 적어 두는 설계도다.

---

## Ⅲ. NETCONF의 전송과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)

NETCONF는 YANG 모델을 실제 장비에 전달하는 프로토콜이다. 보통 [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 위에서 동작하고, XML (Extensible Markup Language) 형식으로 메시지를 주고받는다.

주요 특징은 다음과 같다.

- `edit-config`로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 바꾼다.
- `candidate` datastore에서 먼저 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있다.
- `commit`으로 실제 `running` datastore에 반영한다.
- `rollback`으로 실패한 변경을 되돌릴 수 있다.

```text
Controller
   v SSH
NETCONF
   v XML
Network Device
```

- **📢 섹션 요약 비유**: 바로 벽에 못을 박는 대신, 임시 종이에 먼저 그려 보고 마지막에 확정하는 방식이다.

---

## Ⅳ. RESTCONF와 현대 자동화

RESTCONF는 NETCONF의 모델을 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) ([Hypertext Transfer Protocol](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))와 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) (JavaScript Object Notation) 스타일로 다루게 한 방식이다.

이 방식은 웹 개발자와 자동화 엔지니어가 익숙한 도구를 그대로 쓸 수 있게 해 준다. 그래서 네트워크 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)도 API처럼 다루는 흐름으로 이어진다.

이 흐름은 [Software Defined Networking](/studynote/06_ict_convergence/03_cloud_infrastructure/215_sdn_software_defined_networking_openflow/) ([SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/))과도 잘 맞는다. 중앙 제어기에서 네트워크를 선언형으로 관리하기 때문이다.

- **📢 섹션 요약 비유**: 무거운 서류 대신 앱 화면에서 바로 입력하고 저장하는 느낌이다.

---

## Ⅴ. 실무 적용과 비교

NETCONF/YANG는 장비 간 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 일관성이 중요할 때 강하다. 대규모 라우터, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), WAN 구성, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 배포에 특히 적합하다.

CLI와 비교하면 사람이 직접 치는 작업이 줄고, SNMP와 비교하면 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 반영과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 훨씬 강력하다. 다만 초반에 모델을 잘 만들어야 하고, 벤더별 지원 차이도 확인해야 한다.

- **📢 섹션 요약 비유**: 같은 열쇠로 여러 문을 열 수 있으면 편하지만, 그 열쇠 규격을 먼저 잘 맞춰야 한다.

---

## 관련 개념 맵

```text
YANG (모델)
   v
NETCONF (전송)
   v
candidate / running datastore
   v
RESTCONF / SDN 자동화
```

---

## 관련 키워드 및 발전 흐름도

1. CLI 수동 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) -> 사람 의존과 오류 증가
2. [SNMP](/studynote/03_network/10_application_layer_dns_mgmt/528_snmp_simple_network_management_protocol/) 중심 관리 -> 모니터링은 되지만 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 자동화는 약함
3. YANG 모델링 -> 구조와 제약을 선언
4. NETCONF [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) -> 안전한 반영과 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)
5. RESTCONF / [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) -> 웹 친화적 자동화와 중앙 제어 확장

---

## 어린이를 위한 3줄 비유 설명

YANG은 장난감 조립 설명서예요.
NETCONF는 그 설명서를 실제 장난감에 넣어 조립하는 우체부예요.
그래서 사람 손으로 하나씩 누르지 않아도 한 번에 맞출 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 162 / 1120

<- **이전**: [1056. ONOS / OpenDaylight 구조 모델 비교](/studynote/03_network/20_performance_evaluation_advanced/1056_onos_opendaylight_sdn_controller_comparison/)
**다음**: [1058. 스트리밍 텔레메트리 (Streaming Telemetry) - 푸시 기반 실시간 네트워크 관측](/studynote/03_network/20_performance_evaluation_advanced/1058_streaming_telemetry_network_monitoring/) ->

---
