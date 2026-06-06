---
title: "184. Framing Mechanism"
date: "2026-05-06"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프레이밍 (Framing)은 물리 계층 (Physical Layer)에서 올라오는 연속 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열을 <strong>의미 있는 전송 단위인 프레임 (Frame)으로 경계 지어 자르는 메커니즘</strong>이다.
> 2. **가치**: 프레임 경계가 있어야 수신 측이 헤더, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), FCS (Frame Check Sequence), 재전송 범위를 구분할 수 있으므로, 프레이밍은 오류 처리와 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 공유의 출발점이 된다.
> 3. **판단 포인트**: 길이 기반, [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑, [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/), 물리 계층 구분 신호는 각각 투명성, 오류 후 재동기화, 구현 복잡도가 다르므로 링크 특성에 맞는 방식을 골라야 한다.

---

## Ⅰ. 개요 및 필요성

프레이밍은 <strong>끝없이 들어오는 <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 스트림에서 "어디서 시작하고 어디서 끝나는가"를 정하는 작업</strong>이다. 물리 계층은 0과 1의 연속 신호만 전달할 뿐, 그것이 한 개의 메시지인지 여러 개의 메시지가 이어진 것인지는 알려 주지 않는다. 따라서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층은 연속 신호를 프레임 단위로 잘라야 주소, 제어 정보, 오류 검출 값을 올바른 위치에서 해석할 수 있다.

이 메커니즘이 필요한 이유는 단순히 구분선을 긋기 위해서만이 아니다. 수신 측은 프레임 경계를 알아야 손상된 범위를 국소화할 수 있고, 송신 측은 프레임 단위로 재전송 또는 흐름 제어를 수행할 수 있다. 프레이밍이 없으면 헤더와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 경계가 무너져 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) 주소도, 길이도, [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/) ([Cyclic Redundancy Check](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/))도 해석할 수 없다.

아래 그림은 프레이밍이 물리 계층의 연속 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열을 링크 계층의 관리 가능한 단위로 바꾸는 과정을 보여 준다.

```text
+-------------------------------------------------------------------+
| From raw bits to frames                                           |
+-------------------------------------------------------------------+
| Physical Layer bit stream : 101110011011111001001011110...        |
|                                                                   |
| Framing logic                                                     |
|     +--> [ Header | Payload | FCS ] [ Header | Payload | FCS ]     |
|                                                                   |
| Receiver can now parse address, length, control, error check      |
+-------------------------------------------------------------------+
```

즉 프레이밍은 단순 포장 기술이 아니라, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층 전체가 동작할 수 있게 만드는 <strong>경계 인식의 기반 인프라</strong>다.

- **📢 섹션 요약 비유**: 프레이밍은 긴 롤케이크를 먹기 좋게 조각내고, 각 조각에 이름표와 포장지를 붙이는 일과 같다. 자르지 않으면 어디까지가 한 조각인지 아무도 알 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 프레이밍 메커니즘은 세 가지 문제를 동시에 해결해야 한다. 첫째, <strong>경계 검출</strong>이 가능해야 하고, 둘째, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 안에 우연히 경계 표시와 같은 패턴이 나타나도 원본 의미가 깨지지 않는 **투명성 (Transparency)** 을 보장해야 하며, 셋째, 에러가 발생했을 때 다시 올바른 경계를 찾는 **재동기화 (Resynchronization)** 가 가능해야 한다.

| 방식 | 원리 | 장점 | 한계 |
| :--- | :--- | :--- | :--- |
| 길이 기반 | 헤더에 프레임 길이 기록 | 오버헤드 작음 | 길이 필드 손상 시 경계 전체가 흔들림 |
| [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑 | 시작/끝 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) + escape 삽입 | 구현 단순, 문자/[바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 지향에 적합 | 임의 이진 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 escape 오버헤드 가능 |
| [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/) | [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열 + 5개 `1` 뒤 `0` 삽입 | 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에도 투명성 확보 | [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 단위 처리 필요 |
| 물리 계층 구분 | [idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/), coding violation, delimiter 사용 | 고속 링크와 잘 맞음 | PHY 지원 의존 |

프레임 내부 구조도 중요하다. 많은 링크는 <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a>용 preamble 또는 delimiter</strong>, 헤더, payload, FCS 순으로 프레임을 구성한다. 여기서 프레이밍은 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잘 자르는 기술"인 동시에, 수신기가 어느 시점부터 헤더를 읽어야 하는지 알려 주는 <strong>파싱 시작점 지정 기술</strong>이기도 하다.

[비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)은 시험과 실무에서 자주 묻는 대표 메커니즘이다. [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) (High-Level [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Link Control) 계열처럼 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) `01111110`을 프레임 양끝에 두고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내부에 `1`이 다섯 번 연속 나오면 송신 측이 자동으로 `0`을 하나 삽입한다. 수신 측은 다섯 개의 `1` 뒤에 오는 `0`을 제거하고, `10` 패턴이면 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), `11`이면 오류로 해석해 경계를 복원한다.

```text
+-------------------------------------------------------------------+
| Bit stuffing example                                              |
+-------------------------------------------------------------------+
| Flag        : 01111110                                            |
| Raw payload : 01111110111110                                      |
| Stuffed     : 0111110101111100                                    |
| Frame sent  : 01111110 0111110101111100 01111110                  |
|                                                                   |
| Receiver rule                                                     |
|   after five consecutive 1s:                                      |
|   - next bit 0  -> remove stuffed 0                               |
|   - next bits 10 -> flag                                           |
|   - next bits 11 -> framing error                                  |
+-------------------------------------------------------------------+
```

이 그림이 보여 주는 핵심은 프레이밍이 "양끝에 표식을 붙이는 일"에서 끝나지 않고, <strong>표식과 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 충돌하지 않도록 원본을 안전하게 변형하고 다시 복원하는 절차</strong>까지 포함한다는 점이다.

- **📢 섹션 요약 비유**: 프레이밍은 문장 양끝에 괄호를 붙이는 것만이 아니라, 글 속에 우연히 괄호가 나오면 앞에 escape 표시를 하나 더 넣어 진짜 괄호와 내용 괄호를 구분하는 규칙과 같다.

---

## Ⅲ. 비교 및 연결

프레이밍 방식을 비교할 때 핵심 축은 **경계 표시 방법**, **투명성 확보 방식**, <strong>오류 발생 후 복원력</strong>이다. 길이 기반 방식은 효율이 좋지만 길이 필드가 깨지면 다음 프레임까지 해석이 연쇄적으로 틀어질 수 있다. 반면 스터핑 기반 방식은 오버헤드가 생겨도, [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)를 다시 찾으며 비교적 빠르게 재동기화할 수 있다.

| 비교 항목 | 길이 기반 | [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑 | [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/) |
| :--- | :--- | :--- | :--- |
| 경계 표현 | 길이 필드 | STX/ETX + escape | [flag](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)열 |
| 투명성 처리 | 별도 없음 | escape 문자 삽입 | stuffed [bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) 삽입 |
| 오류 후 복원 | 약함 | 중간 | 강함 |
| 대표 맥락 | 고정 포맷 링크 | [PPP](/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) ([Point-to-Point Protocol](/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/)) 계열 | [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) 계열 |

또한 프레이밍은 오류 제어와도 연결되지만 동일 개념은 아니다. CRC는 프레임이 깨졌는지를 검사하고, [ARQ](/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/) (Automatic Repeat reQuest)는 손상 프레임을 다시 보내게 하며, 프레이밍은 그 모든 처리가 적용될 **경계 단위 자체를 만든다**. 경계가 없으면 오류 검출도 적용 대상을 잃는다.

Ethernet에서도 프레이밍은 중요하지만 구현 방식이 PPP나 HDLC와 완전히 같지는 않다. Ethernet은 preamble과 SFD (Start Frame Delimiter), 길이/타입 필드, 최소/최대 프레임 크기 같은 규칙을 함께 사용해 프레임 경계를 다룬다. 즉 "프레이밍"은 단일 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 이름이 아니라, <strong>링크 환경에 맞춰 경계를 표현하는 설계 묶음</strong>으로 이해해야 한다.

- **📢 섹션 요약 비유**: 길이 기반은 상자 옆면에 "사과 10개"라고 적는 방식이고, 스터핑 기반은 상자 입구와 출구에 봉인 스티커를 붙이는 방식이다. 둘 다 포장은 되지만, 상자 라벨이 찢어졌을 때와 봉인 스티커가 보일 때의 복원력은 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 링크가 <strong>문자/<a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/">바이트</a> 지향인지, 완전한 임의 이진 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>인지, 물리 계층이 얼마나 강한 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 지원을 주는지</strong>를 보고 프레이밍 방식을 선택한다. 단순 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 링크나 PPP처럼 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 흐름을 다루는 환경은 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑이 이해와 구현이 쉽다. 반면 범용 이진 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다루고 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 패턴의 투명성이 중요하면 [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/)이 더 강력하다.

### 실무 판단 기준

1. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 안에 어떤 8비트 값도 자유롭게 들어올 수 있는가?</strong> 그렇다면 문자 기반 구분만으로는 부족할 수 있다.
2. **길이 필드가 깨졌을 때 얼마나 빨리 회복해야 하는가?** 재동기화가 중요하면 delimiter 기반이 유리하다.
3. <strong>Physical Layer가 별도 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a>와 delimiter를 제공하는가?</strong> 고속 LAN은 링크 계층 혼자 모든 경계를 해결하지 않는다.
4. **오버헤드를 감수할 수 있는가?** stuffing은 안전하지만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 패턴에 따라 크기가 늘어난다.

### 대표 적용 맥락

- <strong><a href="/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/">PPP</a></strong>: [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 지향 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 링크에서 flag와 escape를 이용한다.
- <strong><a href="/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/">HDLC</a> 계열</strong>: [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 지향 환경에서 [bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) stuffing으로 투명성을 보장한다.
- <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a></strong>: preamble, SFD, 길이/타입, 최소 프레임 크기와 함께 프레임 경계를 다룬다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 프레이밍과 오류 검출을 같은 개념으로 설명하는 답안
- 길이 필드만 있으면 어떤 오류 후에도 자동 복구된다고 보는 착각
- payload 안에 delimiter 패턴이 나타날 수 있다는 사실을 무시하는 설계

기술사 답안에서는 "프레임의 시작과 끝을 구분한다"는 정의에 더해, <strong>투명성, 재동기화, stuffing, 길이 기반 방식의 취약점, 실제 <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 예시</strong>까지 연결해야 완성도가 높다.

- **📢 섹션 요약 비유**: 프레이밍 설계는 택배 상자에 스티커를 붙이는 일과 비슷하다. 상자 번호만 적을지, 봉인 테이프를 쓸지, 자동 분류기가 읽을 시작 표식을 넣을지에 따라 분실과 오분류 위험이 달라진다.

---

## Ⅴ. 기대효과 및 결론

프레이밍이 잘 설계되면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층은 연속 신호를 <strong>해석 가능하고 재전송 가능한 관리 단위</strong>로 바꿀 수 있다. 그 결과 수신기는 주소와 제어 정보를 정확히 읽고, 오류 검출 범위를 한 프레임 안으로 제한하며, 필요 시 손상된 프레임만 다시 처리할 수 있다. 즉 프레이밍은 링크 계층의 모든 제어 기능이 붙잡고 서 있는 기준선이다.

물론 프레이밍만으로 신뢰성이 완성되지는 않는다. 손상 여부는 CRC가 판단하고, 순서 보장이나 종단 간 신뢰성은 상위 계층이 맡는 경우가 많다. 하지만 프레임 경계가 명확하지 않으면 그 어떤 오류 제어나 흐름 제어도 대상 단위를 잃는다.

정리하면 프레이밍은 <strong>"무한한 <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 흐름을 책임질 수 있는 단위로 자르고, 그 단위를 다시 정확히 찾게 해 주는 경계 설계"</strong> 로 기억하면 된다. 네트워크는 패킷 이전에 먼저 프레임을 제대로 잘라야 한다.

- **📢 섹션 요약 비유**: 프레이밍은 책 한 권을 장과 절로 나누는 목차와 같다. 구분이 있어야 어디서 읽기 시작하고, 어디가 잘못 찢어졌는지, 어디부터 다시 보면 되는지 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Media](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | 프레이밍된 프레임 위에서 주소 지정과 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근 제어를 수행한다 |
| [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/) ([Cyclic Redundancy Check](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)) | 프레임 끝의 오류 검출 정보로 자주 붙는다 |
| Transparency | delimiter와 payload가 충돌하지 않게 만드는 핵심 요구사항이다 |
| [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) Stuffing | [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 지향 링크에서 escape를 넣어 투명성을 확보한다 |
| [Bit Stuffing](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/) | [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 지향 링크에서 [flag](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 패턴 충돌을 막는다 |
| [PPP](/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/) ([Point-to-Point Protocol](/studynote/03_network/04_data_link_layer_error/224_ppp_point_to_point_protocol/)) | [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 스터핑 예시로 자주 언급된다 |
| [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) (High-Level [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Link Control) | [비트 스터핑](/studynote/03_network/04_data_link_layer_error/187_bit_stuffing_flag_mechanism/) 기반 프레이밍의 대표 사례다 |
| SFD (Start Frame Delimiter) | 프레임 시작 지점을 명확히 알려 주는 구분 신호다 |

### 📈 관련 키워드 및 발전 흐름도

```text
Raw bit stream from Physical Layer
        |
        v
Frame boundary recognition
        |
        +---------------> Length-based framing
        +---------------> Byte stuffing
        +---------------> Bit stuffing
        +---------------> Preamble / delimiter / CRC integration
```

이 흐름도는 프레이밍이 단순 경계 표시에서 출발해, 투명성 보장과 오류 검출 연계까지 포함하는 링크 계층의 핵심 메커니즘으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 프레이밍은 길게 이어진 리본을 "한 묶음, 또 한 묶음"으로 예쁘게 잘라 묶어 주는 방법이에요.
2. 이렇게 해야 누가 받을 선물인지 이름표를 붙이고, 망가졌는지도 확인할 수 있어요.
3. 선물 안에 같은 리본 무늬가 들어 있어도 헷갈리지 않게 따로 표시하는 규칙까지 함께 쓰는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 305 / 1120

<- **이전**: [183. 매체 접근 제어 (MAC, Media Access Control) - IEEE 802.3~802.11](/studynote/03_network/04_data_link_layer_error/183_mac_media_access_control/)
**다음**: [185. 바이트 카운트 (Byte Counting) 방식](/studynote/03_network/04_data_link_layer_error/185_byte_counting_framing/) ->

---
