---
title: "240. 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 수신/학습 / 전달 / 플러딩은 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 수신/학습 / 전달 / 플러딩을 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 데이터를 올바르게 보내기 위해 수행하는 일련의 자율적 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 프로세스다. [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 전원을 막 켜면 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블은 텅 비어있다. [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 네트워크 트래픽을 관찰하며 스스로 학습하고, 적절히 버리거나 전달한다.
- **필요성**: 만약 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 IP 라우터처럼 관리자가 일일이 "1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 무슨 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), 2번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 무슨 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)"를 수동으로 입력([Static Routing](/studynote/03_network/07_network_layer_routing/340_static_routing_default_route_0_0_0_0/))해줘야 한다면, 사무실에서 직원이 자리를 옮기거나 노트북을 껐다 켤 때마다 네트워크 관리자는 퇴근을 못 할 것이다. [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 위대함은 **전원만 꽂으면 스스로 네트워크 지형을 학습하는 "Plug and Play"** 기능에 있다.

- **💡 비유**: [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 기억력이 좋은 <strong>"호텔 로비의 신입 벨보이"</strong>와 같습니다. 처음엔 투숙객이 몇 호에 있는지 아무도 모릅니다. 그런데 302호에서 손님이 내려와 "나 302호 홍길동인데, 501호 이몽룡한테 편지 좀 전해줘"라고 하면, 로비보이는 머릿속에 <strong>"홍길동 = 302호"라고 학습(Learning)</strong>합니다. 하지만 이몽룡이 몇 호인지는 아직 모르니 호텔 전 객실에 방송을 때립니다 **(Flooding)**. 나중에 이몽룡이 "나 501호 이몽룡이야"라고 답장을 보내면, 그때 <strong>"이몽룡 = 501호"를 학습</strong>하고, 다음번 편지부터는 501호로 조용히 가져다줍니다 **(Forwarding)**.

```text
[MAC 주소 테이블]
    |
    v
[수신/학습 / 전달 / 플러딩]
    |
    +---> [에이징 / 포트 미러링]
```

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>의 동작 원리는 낯선 동네에 발령받은 우체부가 </strong>"편지를 주고받는 사람들을 눈치껏 지켜보며 동네 지도를 완성해 나가는 완벽한 독학(Self-study) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)"**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Learning (학습) - "출발지를 기억하라"
[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 프레임이 들어오면, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 가장 먼저 프레임 헤더의 <strong>출발지(Source) <a href="/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소</strong>를 까본다.
- "1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에서 `MAC A`가 보낸 편지가 들어왔네? 그럼 1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 끝에는 `MAC A`라는 PC가 매달려 있구나!"
- 이를 즉시 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블에 `[MAC A - Port 1]`이라고 기록한다.

### 2. Flooding (플러딩) - "모르면 전부 뿌려라"
[스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 이제 목적지 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 보고 어디로 보낼지 결정해야 한다. 목적지가 `MAC B`인데, 아직 테이블에 `MAC B`가 어디 있는지 정보가 없다.
- [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 **"모르는 유니캐스트(Unknown Unicast)"** 또는 아예 전체 방송용인 **"브로드캐스트(FF:FF...)"** 프레임을 받으면, 편지가 들어온 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 제외한 <strong>나머지 모든 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>로 편지를 복사해서 쏟아낸다</strong>. 이것이 플러딩이다.

### 3. Forwarding (전달) - "아는 길은 조용히"
만약 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 테이블을 뒤졌는데 목적지 `MAC B`가 3번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 있다는 것을 이미 학습(Learning)한 상태라면?
- 플러딩하지 않고, <strong>오직 3번 <a href="/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>로만 프레임을 조용히 전달</strong>한다. 이것이 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 진면목인 포워딩이다.

### 4. Filtering (여과) - "쓸데없는 전송은 차단한다"
테이블에 `[MAC A - Port 1]`, `[MAC B - Port 1]`이라고 적혀있다고 가정하자. (1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 작은 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)가 달려있는 상황)
- A가 B에게 편지를 보냈다. [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에서 편지를 받아보니, 목적지 B도 1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 있다.
- "어? 어차피 1번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)([허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) 안에서 너희들끼리 주고받았겠네? 내가 굳이 다른 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 이걸 넘겨줄 필요가 없지!" 하고 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 이 프레임을 즉시 <strong>폐기(버림)</strong>한다. 이것이 필터링이다. 덕분에 다른 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)의 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 낭비를 막는다.

### 5. [Aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/) ([노화](/studynote/02_operating_system/03_cpu_scheduling/182_aging/)) - "오래된 기억은 잊어라"
- 한 번 학습된 정보가 평생 남으면, 노트북을 뽑아서 다른 자리로 갔을 때 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 계속 옛날 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 데이터를 보낼 것이다.
- 그래서 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 테이블에 적힌 정보가 기본값 300초([Aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/) Time) 동안 사용되지 않으면(데이터가 안 들어오면) <strong>테이블에서 쿨하게 삭제</strong>해 버리고, 다음번에 다시 Learning을 수행한다.

```text
 +-------------------------------------------------------------+
 |                스위치의 Learning과 Flooding 과정                |
 +-------------------------------------------------------------+
 |                                                             |
 |   1. PC A가 PC B로 핑(Ping) 전송                             |
 |   [ PC A ] ----->(Port 1) [ 스위치 ] (Port 3)---- [ PC B ]   |
 |   (MAC A)                  테이블 비어있음          (MAC B)   |
 |                                                             |
 |   2. Learning (학습)                                         |
 |   스위치: "출발지가 MAC A네? Port 1에 MAC A 등록!"               |
 |   CAM Table: [ MAC A : Port 1 ]                             |
 |                                                             |
 |   3. Flooding (플러딩)                                       |
 |   스위치: "목적지 MAC B는 어딨는지 모르겠네? 1번 빼고 다 뿌려!"      |
 |   스위치 ---> Port 2, Port 3, Port 4... 전송                   |
 |                                                             |
 |   4. PC B의 응답 및 재학습                                     |
 |   PC B가 응답 프레임 보냄 ---> 스위치 (Port 3로 들어옴)            |
 |   스위치: "출발지가 MAC B네? Port 3에 MAC B 등록!"               |
 |   CAM Table: [ MAC A : Port 1 ]                             |
 |              [ MAC B : Port 3 ]                             |
 |                                                             |
 |   5. Forwarding (포워딩)                                     |
 |   스위치: "이제 목적지 MAC A 위치(Port 1) 아니까 조용히 전송!"      |
 |                                                             |
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>는 처음엔 </strong>"스피커로 온 동네방네 방송(Flooding)"<strong>을 하며 사람들을 찾지만, 한 번 명함(출발지 <a href="/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a>)을 건네받고 나면 </strong>"수첩(테이블)에 적어두고(Learning) 다음부터는 조용히 귓속말(Forwarding)"**만 하는 센스 있는 통신 교환수입니다.

---

## Ⅲ. 비교 및 연결

수신/학습 / 전달 / 플러딩을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블이 기반 조건을 만든다면, 수신/학습 / 전달 / 플러딩은 그 위에서 핵심 메커니즘을 구현하고, [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블의 기반 정리 | 수신/학습 / 전달 / 플러딩의 핵심 동작 | [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: 수신/학습 / 전달 / 플러딩은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 수신/학습 / 전달 / 플러딩을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블 수준의 기본 대책으로 충분한지, 아니면 수신/학습 / 전달 / 플러딩이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. 수신/학습 / 전달 / 플러딩가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 수신/학습 / 전달 / 플러딩의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: 수신/학습 / 전달 / 플러딩을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

수신/학습 / 전달 / 플러딩은 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 수신/학습 / 전달 / 플러딩은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |
| [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: MAC 주소 테이블]
    |
    v
[현재 개념: 수신/학습 / 전달 / 플러딩]
    |
    +---> [확장 A: 에이징 / 포트 미러링]
    +---> [확장 B: 지능형 캠퍼스 패브릭]
```

수신/학습 / 전달 / 플러딩는 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 테이블에서 출발해 현재 메커니즘을 정교화하고, 이후 [에이징](/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 361 / 1120

<- **이전**: [239. MAC 주소 테이블 (MAC Address Table, CAM Table)](/studynote/03_network/05_lan_wan_l2_devices/239_mac_address_table_cam_table/)
**다음**: [241. 에이징 (Aging) / 포트 미러링 (Port Mirroring)](/studynote/03_network/05_lan_wan_l2_devices/241_aging_and_port_mirroring/) ->

---
