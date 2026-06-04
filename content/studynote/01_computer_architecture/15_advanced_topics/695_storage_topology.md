---
title: "695. 스토리지 네트워크 토폴로지 (FC-AL, FC-SW)"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스토리지 네트워크 토폴로지는 서버와 스토리지를 어떤 연결 구조로 묶느냐에 따라 병목, 확장성, 장애 범위가 달라지는 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) ([Storage Area Network](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))의 핵심 설계 요소다.
> 2. **가치**: [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL ([Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) Arbitrated Loop)은 저비용 공유 루프 구조를, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW ([Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) Switched Fabric)는 동시 통신과 장애 격리가 가능한 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 구조를 제공해 세대 차이를 만든다.
> 3. **판단 포인트**: 현대 설계에서는 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW가 사실상 표준이며, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL은 레거시 호환이나 제한적 내부 연결을 제외하면 새로운 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 구축에 거의 채택되지 않는다.

---

## Ⅰ. 개요 및 필요성

스토리지 네트워크 토폴로지는 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) ([Storage Area Network](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))에서 서버, 스토리지 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/), [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 어떤 형태로 연결할지 결정하는 구조다. 같은 [Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 장비를 쓰더라도 직결하느냐, 루프로 묶느냐, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭으로 엮느냐에 따라 동시 처리량과 장애 전파 범위가 크게 달라진다. 그래서 토폴로지는 단순 배선도가 아니라, <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>과 가용성을 함께 결정하는 아키텍처 선택</strong>이다.

이 문제가 중요해진 이유는 공유 스토리지 환경에서 연결 대상 수가 급격히 늘어나기 때문이다. 서버가 한 대이고 스토리지가 한 대면 직결로 끝나지만, [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 클러스터나 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 팜처럼 여러 서버가 여러 저장 장치를 공유하려면 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수, 동시 접근, 장애 우회가 모두 문제로 등장한다. 결국 "어떻게 연결할 것인가"가 곧 "누가 동시에 통신할 수 있는가"와 "하나가 고장 나면 어디까지 영향을 받는가"를 결정한다.

특히 블록 스토리지는 일반 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유보다 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간과 혼잡에 민감하다. 그래서 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 토폴로지는 단순히 케이블을 적게 쓰는 방향이 아니라, <strong>충돌을 줄이고 경로를 분리하는 방향</strong>으로 발전해 왔다. [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL과 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW의 차이는 바로 이 발전 과정의 핵심이다.

- **📢 섹션 요약 비유**: 토폴로지는 도시 도로 설계와 같다. 집과 회사가 같아도 골목길로만 연결하면 막히고, 교차로와 우회도로를 잘 두면 같은 차 수로도 훨씬 부드럽게 흐른다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 기반 SAN의 토폴로지는 크게 직결, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW로 이해하면 쉽다. 직결은 단순하지만 1대1 연결에 가깝고, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL은 여러 노드가 하나의 루프를 공유하며, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW는 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 중심으로 각각 독립 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 갖는다. 이 차이는 곧 <strong>공유 매체냐, 교환 기반 매체냐</strong>의 차이다.

| 토폴로지 | 연결 모델 | [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) | 장애 범위 | 대표 용도 |
| :--- | :--- | :--- | :--- | :--- |
| 직결 ([Point-to-Point](/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/)) | 서버 1대와 스토리지 1대 직접 연결 | 낮음 | 작음 | 소규모 전용 연결 |
| [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL ([Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) Arbitrated Loop) | 여러 장비가 하나의 루프 공유 | 제한적 | 루프 전체에 영향 가능 | 레거시 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/), 구형 디스크 루프 |
| [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW ([Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) Switched Fabric) | 각 장비가 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 개별 연결 | 높음 | [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)·경로 단위 격리 | 현대 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 표준 |

[FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL에서는 각 노드가 루프 사용 권한을 놓고 중재한다. 한 노드가 통신권을 얻으면 그 시간 동안 루프는 사실상 공유 버스처럼 동작하며, 다른 노드는 기다려야 한다. 또한 루프 참여 노드가 추가되거나 빠질 때 초기화 과정이 발생해 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 불안정 요소가 생긴다. 일부 장비는 bypass 회로로 문제를 줄였지만, 구조적으로 shared medium이라는 한계는 남는다.

반면 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW에서는 서버의 HBA (Host [Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))와 스토리지 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 각각 연결되고, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 목적지 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 프레임을 전달한다. 서로 다른 서버-스토리지 쌍은 동시에 통신할 수 있고, 조닝 (Zoning)으로 통신 가능한 대상도 세밀하게 통제할 수 있다. 즉 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW는 단순 연결 방식을 넘어, <strong><a href="/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a>·격리·보안 제어를 함께 제공하는 패브릭 구조</strong>다.

아래 그림은 두 구조의 차이를 직관적으로 보여준다.

```text
[FC-AL: one shared loop]

Host A -- Host B -- Storage A -- Storage B
  ^                                   |
  +-----------------------------------+

[FC-SW: switched fabric]

Host A -----+
Host B -----+---- [ SAN Switch ] ---- Storage A
Host C -----+                +------ Storage B
```

이 그림의 핵심은 케이블 개수보다 <strong>통신권이 공유되는지, 독립되는지</strong>다. 루프에서는 모두가 같은 회전목마를 함께 타고 차례를 기다리지만, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭에서는 각자가 자신의 차선과 교차로를 가진다.

- **📢 섹션 요약 비유**: [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL이 놀이공원의 한 줄 대기열이라면, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW는 창구가 여러 개인 은행이다. 같은 손님 수라도 창구가 분리되면 줄 서는 방식 자체가 달라진다.

---

## Ⅲ. 비교 및 연결

[FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL과 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW의 차이는 단순히 구형과 새로운 유형의의 차이가 아니라, <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 모델과 장애 모델의 차이</strong>다. 이 둘을 비교하면 왜 현대 SAN에서 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW가 기본값이 되었는지 명확해진다.

| 비교 축 | [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL | [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW |
| :--- | :--- | :--- |
| 통신 방식 | 루프 공유, 중재 필요 | [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기반 전달 |
| 동시 처리 | 제한적 | 다수 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 동시 처리 가능 |
| 확장성 | 노드 증가 시 루프 부담 증가 | [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 링크 확장으로 확장 용이 |
| 장애 격리 | 루프 전체 영향 가능 | [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)·링크·[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 단위로 국소화 가능 |
| 운영 기능 | 단순하지만 제어 한계 | 조닝, 이중 패브릭, 관리 기능 풍부 |

[FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW가 중요한 이유는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)뿐 아니라 가용성과 운영성 때문이다. 예를 들어 멀티패스 I/O ([Multipath](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) Input/Output)를 설계할 때도, 독립된 두 개 이상의 패브릭이 있어야 경로 장애 시 우회가 자연스럽다. [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL에서는 경로 분리가 애매하고 장애 범위가 넓어 고가용성 설계가 어렵다. 그래서 오늘날의 SAN은 보통 A/B 두 개의 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW 패브릭을 따로 구성한다.

또한 이 토폴로지는 다음 주제인 [Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [FCoE](/studynote/01_computer_architecture/15_advanced_topics/697_fcoe/) ([Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) over [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)), [iSCSI](/studynote/01_computer_architecture/15_advanced_topics/698_iscsi/) (Internet Small Computer System Interface)와도 연결된다. 어떤 전송 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 쓰든 결국 중요한 질문은 같다. <strong>공유 경로를 어떻게 분리하고, 장애와 혼잡을 어디서 흡수할 것인가</strong>다. [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW는 이 질문에 대해 가장 성숙한 답을 제공해 왔다.

- **📢 섹션 요약 비유**: [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL은 마을 사람들이 하나의 우물만 돌아가며 쓰는 구조이고, [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW는 집집마다 수도관이 분기된 구조다. 둘 다 물은 나오지만, 붐비는 시간과 고장 났을 때의 혼란이 전혀 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현대 실무에서는 새로운 SAN을 설계할 때 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW를 기본 전제로 두고, 보통 두 개의 독립 패브릭을 나눠 구성한다. 서버는 두 개 이상의 HBA [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 서로 다른 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)에 연결하고, 스토리지 컨트롤러도 양쪽 패브릭에 각각 연결한다. 이렇게 해야 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 한 대나 링크 하나가 끊겨도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 계속된다. 기술사 답안에서는 "이중 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) + 이중 HBA + 멀티패스"를 한 세트로 묶어 설명하는 것이 중요하다.

### 실무 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 신규 구축이라면 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL이 아니라 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW 기반 이중 패브릭을 채택했는가?
2. 서버와 스토리지가 서로 다른 패브릭으로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 연결되어 단일 장애점을 제거했는가?
3. 조닝을 최소 권한 원칙으로 구성해 불필요한 가시성을 줄였는가?
4. [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 간 연결 대역폭이 실제 동시 트래픽을 감당하도록 설계되었는가?
5. 경로 장애, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 장애, 컨트롤러 장애를 분리해 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시나리오를 검증했는가?

[FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL은 오늘날 대부분 레거시 환경, 구형 디스크 인클로저, [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 유지 목적으로만 남아 있다. 따라서 실무에서 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL을 설명할 때는 "예전의 공유 루프 구조"라는 역사적 의미와 함께, 왜 현대 설계에서 배제되는지를 명확히 적어야 한다. 비용만 보고 공유 구조를 택하면, 나중에 병목과 장애 전파 때문에 더 큰 운영 비용을 치르게 된다.

- **📢 섹션 요약 비유**: [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 설계는 다리를 하나 크게 만드는 문제보다, 끊겨도 돌아갈 우회도로를 함께 만드는 문제에 가깝다. 평소에는 비슷해 보여도 사고가 나면 설계 수준 차이가 드러난다.

---

## Ⅴ. 기대효과 및 결론

적절한 스토리지 네트워크 토폴로지를 선택하면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 확장성, 장애 대응 방식이 한 번에 정리된다. 특히 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW 기반 패브릭은 다수 서버와 스토리지가 동시에 안정적으로 통신할 수 있게 하고, 경로 이중화와 운영 통제를 현실적으로 가능하게 만든다. 그래서 토폴로지는 배선 편의가 아니라, <strong>스토리지 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 품질을 결정하는 기반 구조</strong>라고 볼 수 있다.

반대로 잘못된 토폴로지는 장비가 충분히 좋아도 전체 시스템을 병목과 단일 장애점으로 몰아넣는다. [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL이 역사적으로 의미는 있었지만 현대 워크로드에 맞지 않는 이유도 여기에 있다. 결국 기억해야 할 핵심은 "토폴로지 = 케이블 모양"이 아니라, <strong>경합 범위와 장애 범위를 정하는 설계 선택</strong>이라는 점이다.

앞으로는 [Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 기반 패브릭 위에 더 빠른 플래시 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 올라가거나, 일부 환경은 [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 기반 저장 네트워크로 옮겨가더라도, 토폴로지 판단 원리는 그대로 유지된다. 공유 구조는 단순하지만 병목이 크고, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭은 복잡하지만 확장과 격리에 유리하다.

- **📢 섹션 요약 비유**: 좋은 토폴로지는 길을 예쁘게 그리는 일이 아니라, 사람들이 동시에 움직여도 엉키지 않게 동선을 설계하는 일이다. 길의 모양이 곧 도시의 성격이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) ([Storage Area Network](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)) | 서버와 스토리지를 공유 네트워크로 묶는 상위 개념 |
| HBA (Host [Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)) | 서버가 [Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 패브릭에 접속하는 전용 인터페이스 |
| 조닝 (Zoning) | [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW 환경에서 통신 가능한 노드 범위를 통제하는 보안·운영 기법 |
| 멀티패스 I/O ([Multipath](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) Input/Output) | 다중 경로를 통해 장애 시 우회와 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)을 수행하는 구조 |
| [Fibre Channel](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) ([FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL과 [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW 위에서 실제 프레임 전송과 흐름 제어를 담당하는 규약 |

### 📈 관련 키워드 및 발전 흐름도

```text
Point-to-point direct attach
    |
    v
FC-AL shared loop
    |
    v
FC-SW switched fabric
    |
    v
Dual-fabric high availability SAN
    |
    v
Converged or hybrid storage networking
```

이 흐름은 연결 구조가 단순 직결에서 공유 루프를 거쳐, 장애 격리와 확장을 중시하는 패브릭 중심 구조로 발전한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-AL은 친구들이 한 줄로 서서 돌아가며 미끄럼틀을 타는 놀이터 같아요.
2. [FC](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/)-SW는 미끄럼틀이 여러 개라서 친구들이 동시에 더 빨리 놀 수 있는 놀이터예요.
3. 그래서 큰 놀이터일수록 한 줄 대기보다 여러 길로 나뉜 구조가 훨씬 편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 696 / 803

<- **이전**: [694. 광 디스크 주크박스](/studynote/01_computer_architecture/15_advanced_topics/694_optical_disc_jukebox/)
**다음**: [696. Fibre Channel (FC) 프로토콜](/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) ->

---
