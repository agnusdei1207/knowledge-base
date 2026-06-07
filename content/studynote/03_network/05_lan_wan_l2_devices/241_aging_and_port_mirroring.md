---
title: "Port Mirroring"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 241
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)을 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/182_aging/">Aging</a></strong>: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 한 번 학습([Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))한 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 정보를 무한정 보관하지 않고 타이머를 돌려 스스로 지우는 기능.
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a> Mirroring</strong>: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 내부에서 특정 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(또는 [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/))를 오가는 송수신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다른 지정된 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 거울처럼 그대로 복사해 주는 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 관리 기능(Cisco에서는 SPAN이라고 부름).
- **필요성**:
  - 만약 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/)이 없다면, 직원이 노트북을 1층([포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 1)에서 빼서 2층([포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 2)에 꽂았을 때, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 여전히 1층으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보내 통신이 단절될 것이다.
  - 만약 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)이 없다면, 네트워크에 이상 트래픽(해킹, 웜 [바이러스](/studynote/02_operating_system/10_security/589_virus/))이 돌 때 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 당사자에게만 은밀하게 꽂아주기 때문에, 관리자가 패킷 분석기(와이어샤크)를 달아도 범인을 잡을 수가 없다.

- **💡 비유**:
  - <strong><a href="/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/">에이징</a></strong>: 호텔 로비 직원이 투숙객 명단을 관리할 때, "이 손님이 일주일 동안 로비에 안 나타나면 <strong>체크아웃한 것으로 간주하고 수첩에서 지우는(<a href="/studynote/02_operating_system/03_cpu_scheduling/182_aging/">Aging</a>)</strong>" 규칙입니다.
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> <a href="/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a></strong>: 경찰이 용의자(1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))의 전화를 도청하기 위해, 전화국([스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))에 협조를 구해 용의자의 통화 내용을 <strong>경찰서(3번 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>)로 똑같이 <a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a>(Mirroring)해서 듣는 것</strong>입니다.

```text
[수신/학습 / 전달 / 플러딩]
    |
    v
[에이징 / 포트 미러링]
    |
    +---> [스위칭 방식]
```

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/">에이징</a>은 <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>의 한정된 뇌 용량(메모리)을 지키기 위한 </strong>"망각의 기술"<strong>이고, <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> <a href="/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a>은 <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>라는 닫힌 상자 속을 들여다보기 위한 </strong>"[CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 설치"**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [Aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/) 타이머의 동작
[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 학습할 때마다 해당 엔트리에 대해 <strong>타이머(기본값 300초)</strong>가 돌기 시작한다.
- **타이머 초기화 (Refresh)**: 300초가 지나기 전에 해당 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소로부터 또다시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어오면, 타이머는 다시 300초로 초기화된다.
- <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/182_aging/">Aging</a> Out</strong>: 300초 내내 단 한 번의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 보내지 않으면 타이머가 0이 되고, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 지체 없이 해당 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 테이블에서 삭제한다. 이후 해당 MAC으로 향하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 오면 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 목적지를 모르므로 모든 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 플러딩(Flooding)하게 된다.

### 2. [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) Mirroring의 구조와 활용 (SPAN)
[허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)([Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) 시절에는 그냥 PC에 와이어샤크를 켜놓기만 해도 동네방네 퍼지는 남의 패킷을 다 주워 담을 수 있었다(Promiscuous Mode). 그러나 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 환경에서는 유니캐스트 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 내 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 오지 않기 때문에 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 설정에 들어가 강제로 복사 명령을 내려야 한다.

```text
 +-------------------------------------------------------------+
 |                 포트 미러링(Port Mirroring) 구조                |
 +-------------------------------------------------------------+
 |                                                             |
 |   [ PC A (서버) ] -----> (Port 1: Source Port)                |
 |                           | 스위치 내부에서                   |
 |                           | 데이터 복사 발생!                  |
 |                           +-------------+                   |
 |                           v             v (복사본)           |
 |   [ PC B (클라) ] <----- (Port 2)       (Port 3: Dest Port)  |
 |                                         |                   |
 |                                         v                   |
 |                                    [ 패킷 분석기 (IDS/IPS) ]   |
 |                                     (Wireshark 모니터링)      |
 |                                                             |
 | * 관리자 설정: "Port 1로 들어오고 나가는 트래픽을 Port 3으로 복사하라!"|
 +-------------------------------------------------------------+
```

- <strong>Source <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a> (소스 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>)</strong>: 감시의 대상이 되는 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/). (주로 라우터와 연결된 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)나 중요 서버가 연결된 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))
- <strong>Destination <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a> (목적지 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>)</strong>: 복사본을 받을 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/). 이곳에는 네트워크 관리자의 노트북이나 [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)([침입 탐지 시스템](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/))가 연결된다. 이 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 오직 모니터링 수신 전용으로만 쓰이며, 일반적인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 송수신은 차단된다.

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/">에이징</a>이 </strong>"쓸모없는 주소록을 파쇄기에 넣는 주기적인 대청소"<strong>라면, <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> <a href="/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a>은 범죄 수사를 위해 우체국에서 편지를 배달하기 직전 </strong>"편지 내용을 똑같이 복사기(복사본)로 떠서 수사관에게 넘겨주는 극비 작전"**입니다.

---

## Ⅲ. 비교 및 연결

[에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 수신/학습 / 전달 / 플러딩이 기반 조건을 만든다면, [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 그 위에서 핵심 메커니즘을 구현하고, [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 수신/학습 / 전달 / 플러딩의 기반 정리 | [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)의 핵심 동작 | [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 수신/학습 / 전달 / 플러딩 수준의 기본 대책으로 충분한지, 아니면 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- 수신/학습 / 전달 / 플러딩와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 수신/학습 / 전달 / 플러딩 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 수신/학습 / 전달 / 플러딩]
    |
    v
[현재 개념: 에이징 / 포트 미러링]
    |
    +---> [확장 A: 스위칭 방식]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

[에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)는 수신/학습 / 전달 / 플러딩에서 출발해 현재 메커니즘을 정교화하고, 이후 [스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 362 / 1120

<- **이전**: [240. 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding)](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)
**다음**: [242. 스위칭 방식](/studynote/03_network/05_lan_wan_l2_devices/242_switching_method_cut_through/) ->

---
