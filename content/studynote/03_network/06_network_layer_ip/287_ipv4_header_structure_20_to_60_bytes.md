---
title: "287. IPv4 헤더 구조 (기본 20바이트 ~ 최대 60바이트)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 패킷은 알맹이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/))를 감싸는 껍질로, 라우터가 목적지를 찾아 배달할 수 있도록 이정표 역할을 하는 <strong>'최소 20바이트에서 최대 60바이트' 크기의 헤더(Header)</strong>를 가진다.
> 2. **가치**: 현대 네트워크에서 추가 옵션(Options) 필드는 보안 및 성능상의 이유로 거의 쓰이지 않기 때문에, 사실상 [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더의 길이는 <strong>20바이트 고정</strong>이라고 봐도 무방하다.
> 3. **판단 포인트**: 20바이트의 공간은 크게 <strong><a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">경로 [설정</a>(Source/Dest IP)], <a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">단편화([Fragmentation</a>) 조립 정보], <a href="/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/">수명([TTL</a>) 및 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 식별]</strong>의 세 가지 핵심 구역으로 알차게 나뉘어 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**: OSI 3계층에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 포장하는 규격서. IP 패킷의 맨 앞에 붙어서 전 세계 인터넷 망을 항해하기 위한 온갖 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)값을 담은 20바이트짜리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표다.
- **필요성**: 우체국에서 편지를 보낼 때, 맹목적으로 목적지 주소만 적는다고 능사가 아니다. "받는 사람 주소, 보내는 사람 주소, 우표(수명), 등기 여부, 편지봉투 크기"를 양식에 맞춰 빼곡히 적어야 우편집중국(라우터)의 기계가 스캔해서 착착 분류할 수 있다. IP 헤더는 라우터가 0.0001초 만에 뜯어보고 버릴지 보낼지 판단하는 전 세계 공통의 규격서다.

- **💡 비유**: [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더는 택배 박스 겉면에 붙어있는 <strong>"종합 송장 스티커"</strong>와 같습니다. 스티커에는 보내는 사람(Source IP)과 받는 사람(Dest IP)은 물론이고, 박스 무게(Total Length), 내용물이 옷인지 책인지([Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)), 그리고 유통기한([TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/))까지 박스를 배달하는 데 필요한 모든 정보가 암호 같은 숫자로 빼곡히 적혀 있습니다.

```text
[IPv4]
    |
    v
[IPv4 헤더 구조]
    |
    +---> [버전, 헤더 길이, 서비스 타입, 전체 길이]
```

- **📢 섹션 요약 비유**: <strong> <a href="/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/">IPv4</a> 헤더는 20바이트라는 극도로 좁은 </strong>"여권(Passport) 앞장"**에 이름, 국적, 생년월일, 만료일 등 라우터(출입국 심사관)가 요구하는 모든 필수 정보를 우겨 넣은 완벽한 디자인의 결정체입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

헤더는 보통 4바이트(32비트)씩 5줄(Row)로 그려서 외운다. `4 Bytes * 5 Rows = 20 Bytes`

### 1. 첫 번째 줄 (4 Bytes) - 기본 명세서
- **Version (4비트)**: "나 IPv4야"라고 알리는 필드. 무조건 `4` (0100)가 들어있다.
- **IHL (Header Length, 4비트)**: 헤더 전체의 길이를 4바이트 단위로 적는다. 옵션이 없으면 항상 20바이트이므로, 20 ÷ 4 = `5` (0101)가 들어간다.
- **TOS / DSCP (1바이트)**: VIP 패킷(음성 등)을 빨리 처리해 달라고 부탁하는 우선순위([QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)) 딱지.
- **Total Length (2바이트)**: 헤더와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 합친 이 패킷의 전체 길이. (최대 65,535바이트)

### 2. 두 번째 줄 (4 Bytes) - [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) ([Fragmentation](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)) 퍼즐 정보
패킷이 뚱뚱해서 여러 조각으로 찢어졌을 때([단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)), 목적지에서 다시 조립하기 위한 번호표다.
- <strong><a href="/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">Identification</a> (<a href="/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">식별자</a>, 2바이트)</strong>: "우리는 원래 같은 100번 박스에서 찢어진 형제들이야!"라는 고유 번호.
- <strong>Flags (<a href="/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/">플래그</a>, 3비트)</strong>: "나 찢어질 거야(DF)", "내 뒤에 찢어진 조각 더 있어(MF)"를 알리는 신호탄.
- <strong>Fragment Offset (<a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">단편화</a> 오프셋, 13비트)</strong>: "나는 원래 박스의 300바이트째부터 시작하는 조각이야!"라는 조립 위치 번호.

### 3. 세 번째 줄 (4 Bytes) - 생존과 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)
- <strong><a href="/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/">TTL</a> (<a href="/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/">Time To Live</a>, 1바이트)</strong>: 패킷의 수명. 라우터를 하나 지날 때마다 1씩 깎이며, 0이 되면 우주 미아([Looping](/studynote/03_network/05_lan_wan_l2_devices/251_looping_broadcast_storm/)) 방지를 위해 즉시 폐기(Drop)된다.
- <strong><a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a> (1바이트)</strong>: 내 뱃속(페이로드)에 들어있는 내용물이 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)(6)인지, [UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)(17)인지, [ICMP](/studynote/03_network/06_network_layer_ip/318_icmp_internet_control_message_protocol_diagnostics/)(1)인지 상위 4계층 모듈을 알려주는 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)표.
- <strong><a href="/studynote/03_network/06_network_layer_ip/296_header_checksum_ipv4_integrity/">Header Checksum</a> (2바이트)</strong>: 이동 중에 20바이트 헤더가 깨졌는지 검사하는 에러 검출 코드.

### 4. 네 번째 & 다섯 번째 줄 (8 Bytes) - 주소
- **Source IP Address (4바이트)**: 보내는 놈의 32비트 IP 주소.
- **Destination IP Address (4바이트)**: 받는 놈의 32비트 IP 주소.

```text
 +-------------------------------------------------------------+
 |                IPv4 헤더 (20 Bytes 고정부) 도식               |
 +-------------------------------------------------------------+
 |                                                             |
 |   0                   15                  31 (Bits)         |
 |   +----+----+--------+----------------------+ (4B)          |
 |   |VER |IHL |  TOS   |     Total Length     |               |
 |   +----+----+--------+----+-----------------+ (4B)          |
 |   |  Identification  |Flag| Fragment Offset |               |
 |   +--------+---------+----+-----------------+ (4B)          |
 |   |  TTL   | Protocol|   Header Checksum    |               |
 |   +--------+---------+----------------------+ (4B)          |
 |   |         Source IP Address (32bit)       |               |
 |   +-----------------------------------------+ (4B)          |
 |   |      Destination IP Address (32bit)     |               |
 |   +-----------------------------------------+               |
 |        ... [ Options (0~40B) - 거의 안 씀 ] ...               |
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: ** 라우터는 우체국 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 스캐너입니다. 패킷이 날아오면 1행에서 박스 크기를 재고, 2행에서 박스가 찢어졌는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 3행에서 유통기한([TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/))을 살핀 뒤, 4/5행의 도착지 주소(IP)를 보고 컨베이어 벨트를 튕겨냅니다. 이 완벽한 5줄의 조합이 전 세계 인터넷을 돌아가게 합니다.

---

## Ⅲ. 비교 및 연결

[IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. IPv4가 기반 조건을 만든다면, [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조는 그 위에서 핵심 메커니즘을 구현하고, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 주소 효율과 도달성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | IPv4의 기반 정리 | [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조의 핵심 동작 | [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 주소 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 수준의 기본 대책으로 충분한지, 아니면 [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 주소 효율 부족인지, 도달성 악화인지 먼저 분리한다.
2. [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- IPv4와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조는 네트워크 계층과 IP를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 주소 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이, 대규모 주소 자동화, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 대규모 주소 자동화 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| IP 주소 (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Address) | 종단 위치를 논리적으로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)한다. |
| 서브넷 (Subnet) | 주소 공간을 쪼개 관리 단위를 만든다. |
| [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: IPv4]
    |
    v
[현재 개념: IPv4 헤더 구조]
    |
    +---> [확장 A: 버전, 헤더 길이, 서비스 타입, 전체 길이]
    +---> [확장 B: 대규모 주소 자동화]
```

[IPv4](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/) 헤더 구조는 IPv4에서 출발해 현재 메커니즘을 정교화하고, 이후 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 헤더 길이, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 타입, 전체 길이와 대규모 주소 자동화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 택배를 보내려면 집 주소가 정확해야 길을 잃지 않아요.
2. 이 개념은 인터넷 세상에서 주소를 정하고 다음 길을 찾는 지도와 같아요.
3. 그래서 멀리 있는 친구 컴퓨터까지도 편지가 도착할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 408 / 1120

<- **이전**: [286. IPv4 (Internet Protocol Version 4)](/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/)
**다음**: [288. 버전 (IV), 헤더 길이 (IHL), 서비스 타입 (TOS/DSCP), 전체 길이 (Total Length)](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) ->

---
