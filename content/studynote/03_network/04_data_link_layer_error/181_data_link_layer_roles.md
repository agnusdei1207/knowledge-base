---
title: '181. 데이터 링크 계층의 역할: 프레이밍, 흐름 제어, 오류 제어, 회선 제어'
date: '2026-05-06'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] 링크 계층 ([[001_dikw_pyramid|Data]] Link Layer)은 물리 계층 (Physical Layer)의 [[073_bit|비트]] 흐름을 프레임 (Frame)이라는 의미 있는 단위로 묶어, 인접한 두 노드 사이의 링크 단위 전달 규칙을 만든다.
> 2. **가치**: [[184_framing_mechanism|프레이밍]], 회선 제어, [[213_flow_control_buffer_overflow|흐름 제어]], [[188_error_control_overview|오류 제어]]를 통해 "그냥 흘러가는 전기/광 [[130_signal|신호]]"를 "누가 언제 얼마나 믿고 보낼 수 있는가"가 정해진 통신으로 바꾼다.
> 3. **판단 포인트**: 깨끗한 유선 링크에서는 이 계층을 얇고 빠르게 설계하고, 오류가 잦은 무선·[[149_serial_communication_rs232_rs485|직렬]] 링크에서는 재전송과 제어 기능을 더 두껍게 가져가는 것이 일반적이다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] 링크 계층은 OSI (Open Systems Interconnection) 7계층의 2계층으로, **바로 이웃한 장치끼리 [[001_dikw_pyramid|데이터]]를 안전하게 넘기기 위한 지역 규칙**을 담당한다. 물리 계층은 [[073_bit|비트]]가 흐르게 할 뿐, 어디서부터 어디까지가 한 덩어리인지, 중간에 깨졌는지, 상대가 지금 받을 수 있는지까지는 알지 못한다. 이 공백을 메우는 층이 바로 [[001_dikw_pyramid|데이터]] 링크 계층이다.

이 계층이 필요한 이유는 네트워크 통신이 항상 깨끗한 [[266_leased_line_basics_e1_t1_t3|전용선]] 위에서만 일어나지 않기 때문이다. [[130_signal|신호]]는 잡음으로 뒤틀릴 수 있고, 송신자는 너무 빨리 보낼 수 있으며, 공유 회선에서는 누가 먼저 보낼지도 정해야 한다. 따라서 [[001_dikw_pyramid|데이터]] 링크 계층은 단순 전달이 아니라 **인접 링크의 질서를 만드는 계층**이라고 보는 편이 정확하다.

아래 그림은 물리 계층의 [[073_bit|비트]] 흐름 위에 [[001_dikw_pyramid|데이터]] 링크 계층이 어떤 질서를 덧입히는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ What the data link layer adds                                     │
├────────────────────────────────────────────────────────────────────┤
│ network packet                                                     │
│      │                                                             │
│      ▼                                                             │
│ frame = [header | payload | trailer/FCS]                           │
│      │       │            │                 │                       │
│      │       │            │                 └-> error check        │
│      │       │            └--------------------> data unit         │
│      │       └--------------------------------> control info       │
│      ▼                                                             │
│ physical bits on one link                                          │
└────────────────────────────────────────────────────────────────────┘
```

이 그림의 포인트는 [[001_dikw_pyramid|데이터]] 링크 계층이 단지 헤더를 붙이는 수준이 아니라, **[[073_bit|비트]] 스트림에 경계·제어·[[395_verification_process_review|검증]] 의미를 부여한다**는 점이다. 덕분에 상위 계층은 매번 전기 [[130_signal|신호]] 상태를 직접 걱정하지 않고도, 이웃 노드까지의 전달을 비교적 안정된 단위로 다룰 수 있다.

- **📢 섹션 요약 비유**: 물리 계층이 그냥 흘러가는 벨트라면, [[001_dikw_pyramid|데이터]] 링크 계층은 그 벨트 위 물건을 박스로 포장하고 차례표를 붙여 사고 없이 옆 창고로 보내는 반장과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[001_dikw_pyramid|데이터]] 링크 계층의 핵심 역할은 흔히 **[[184_framing_mechanism|프레이밍]], 회선 제어, [[213_flow_control_buffer_overflow|흐름 제어]], [[188_error_control_overview|오류 제어]]**의 네 가지로 정리된다. 이 네 기능은 서로 별개가 아니라, "한 링크에서 누가 언제 얼마나 정확하게 보낼 수 있는가"를 분담해 해결하는 구조다.

| 역할 | 답하는 질문 | 대표 메커니즘 | 대표 예시 |
| :--- | :--- | :--- | :--- |
| [[184_framing_mechanism|프레이밍]] ([[184_framing_mechanism|Framing]]) | 한 프레임의 시작과 끝은 어디인가? | 길이 필드, [[186_character_stuffing_dle_stx_etx|플래그]], [[187_bit_stuffing_flag_mechanism|비트 스터핑]] | [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]], [[216_hdlc_high_level_data_link_control|HDLC]] |
| 회선 제어 (Line Control) | 누가 언제 링크를 사용할 수 있는가? | 링크 [[009_config|설정]]/해제, [[448_polling_programmed_io|폴링]], [[673_mac_message_authentication_code|MAC]] 절차 | [[216_hdlc_high_level_data_link_control|HDLC]] 모드, [[224_ppp_point_to_point_protocol|PPP]], 무선 [[673_mac_message_authentication_code|MAC]] |
| [[213_flow_control_buffer_overflow|흐름 제어]] ([[421_tcp_flow_control_sliding_window_algorithm|Flow Control]]) | 수신자가 감당할 속도로 보내는가? | Stop-and-Wait, Sliding Window | [[216_hdlc_high_level_data_link_control|HDLC]], [[744_load_line_calibration|LLC]], TCP와 연동 |
| [[188_error_control_overview|오류 제어]] ([[188_error_control_overview|Error Control]]) | 프레임이 깨졌거나 사라졌는가? | [[113_crc|CRC]], ACK/[[211_nak_negative_acknowledgement|NAK]], [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] | [[216_hdlc_high_level_data_link_control|HDLC]], Wi-Fi, [[224_ppp_point_to_point_protocol|PPP]] |

### 1) [[184_framing_mechanism|프레이밍]]

[[184_framing_mechanism|프레이밍]]은 끝없이 이어지는 [[073_bit|비트]] 스트림에서 **프레임 경계**를 만드는 작업이다. 길이 필드를 두거나, [[186_character_stuffing_dle_stx_etx|플래그]] 바이트와 [[187_bit_stuffing_flag_mechanism|비트 스터핑]] ([[187_bit_stuffing_flag_mechanism|Bit Stuffing]]) 같은 기법으로 "여기서 시작, 여기서 종료"를 구분한다. 프레임 경계가 없으면 수신자는 어떤 [[073_bit|비트]]가 어느 상위 패킷에 속하는지 해석할 수 없다.

### 2) 회선 제어

회선 제어는 **링크를 어떤 규칙으로 운영할지**를 정한다. 전용 [[149_serial_communication_rs232_rs485|직렬]] 링크에서는 연결을 열고 닫는 절차, 송신 주체의 역할, 반이중/전이중 같은 동작 모드가 중요하다. 공유 [[121_transmission_media_guided_unguided|매체]]에서는 누가 먼저 전송권을 가질지, 충돌을 어떻게 피할지가 회선 제어의 핵심이 된다. 즉 회선 제어는 "선로가 존재한다"를 넘어서, **선로를 어떻게 질서 있게 사용할 것인가**를 다룬다.

### 3) [[213_flow_control_buffer_overflow|흐름 제어]]

[[213_flow_control_buffer_overflow|흐름 제어]]는 송신 속도와 수신 처리 능력의 차이를 조절한다. 송신자가 너무 빨리 보내면 수신 버퍼가 넘치므로, 정지-대기 (Stop-and-Wait)나 슬라이딩 윈도우 (Sliding Window)로 미확인 프레임 수를 제한한다. 링크 [[015_지연_데이터_관점|지연]]이 짧고 수신 버퍼가 작을수록 이 기능의 효과가 크다.

### 4) [[188_error_control_overview|오류 제어]]

[[188_error_control_overview|오류 제어]]는 프레임이 손상되거나 유실되었는지 검사하고, 필요하면 복구하는 기능이다. 일반적으로 FCS (Frame Check Sequence)나 [[113_crc|CRC]] ([[113_crc|Cyclic Redundancy Check]])로 오류를 검출하고, ACK (Acknowledgement) / [[211_nak_negative_acknowledgement|NAK]] ([[211_nak_negative_acknowledgement|Negative Acknowledgement]]) 기반 [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] (Automatic Repeat reQuest)로 재전송을 수행한다. 깨끗한 링크에서는 검출만 하고 상위 계층에 맡길 수도 있고, 무선처럼 오류율이 높은 링크에서는 로컬 재전송을 적극 사용하기도 한다.

다음 그림은 네 역할이 실제 프레임 전달 과정에 어떻게 겹쳐 들어가는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Link-level delivery on one hop                                    │
├────────────────────────────────────────────────────────────────────┤
│ Sender                                      Receiver                │
│   packet                                                         │
│    │                                                              │
│    ▼                                                              │
│ [framing] -> [line control grants send] -> transmit bits          │
│    │                                         │                     │
│    └-> add header/trailer/FCS                ▼                     │
│                                      [error check by CRC]         │
│                                      [flow check by window/buffer]│
│                                      [ACK/NAK if needed]          │
└────────────────────────────────────────────────────────────────────┘
```

즉 [[001_dikw_pyramid|데이터]] 링크 계층은 단일 기능이 아니라, **경계 [[009_config|설정]] + 사용 순서 + 속도 조절 + 신뢰 보정**의 묶음이다. 이 네 축을 한 번에 이해해야 뒤이어 등장하는 [[744_load_line_calibration|LLC]] (Logical Link Control), [[673_mac_message_authentication_code|MAC]] ([[121_transmission_media_guided_unguided|Media]] [[547_access_control_rwx|Access Control]]), [[216_hdlc_high_level_data_link_control|HDLC]], [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] 등의 세부 주제가 자연스럽게 이어진다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 링크 계층은 택배 상자를 만드는 팀, 배송 순서를 정하는 팀, 창고 속도를 맞추는 팀, 파손 여부를 검사하는 팀이 한 조로 움직이는 물류 센터와 같다.

---

## Ⅲ. 비교 및 연결

[[001_dikw_pyramid|데이터]] 링크 계층의 역할을 정확히 이해하려면, 이 계층의 기능이 **어디까지가 링크 책임이고 어디서부터가 다른 계층 책임인지**를 구분해야 한다. 물리 계층은 [[073_bit|비트]]를 실어 나르고, [[001_dikw_pyramid|데이터]] 링크 계층은 한 홉 (Hop) 전달을 다듬으며, 전송 계층 (Transport Layer)은 종단 간 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]과 혼잡 제어를 담당한다.

| 계층 | 관점 | 주된 책임 | 실패 시 대응 |
| :--- | :--- | :--- | :--- |
| 물리 계층 (Physical Layer) | [[130_signal|신호]] | [[073_bit|비트]] 전송 | [[130_signal|신호]] 세기, 변조, [[121_transmission_media_guided_unguided|매체]] 품질 |
| [[001_dikw_pyramid|데이터]] 링크 계층 | 한 링크 | 프레임, 회선 제어, 로컬 오류·[[213_flow_control_buffer_overflow|흐름 제어]] | 재전송, 윈도우 조절, 링크 절차 |
| 전송 계층 (Transport Layer) | 종단 간 | [[160_session_controlling_terminal|세션]] 단위 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]], 혼잡 제어 | 재전송, 혼잡 창 조절, 순서 복원 |

이 구분이 중요한 이유는 [[001_dikw_pyramid|데이터]] 링크 계층의 [[188_error_control_overview|오류 제어]]가 **끝까지의 완전한 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]**을 뜻하지 않기 때문이다. 링크 하나에서 CRC와 재전송을 잘 해도, 라우터 여러 개를 지나가는 전체 경로에서는 여전히 패킷 손실이 생길 수 있다. 반대로 무선 구간처럼 국소 오류가 잦은 환경에서는 전송 계층까지 올라가기 전에 링크 수준에서 빠르게 복구하는 편이 훨씬 효율적이다.

또한 회선 제어의 비중은 [[121_transmission_media_guided_unguided|매체]] 종류에 따라 다르다. 전용 유선 이더넷에서는 충돌과 연결 [[009_config|설정]] 문제가 크게 줄어 상대적으로 얇은 링크 계층이 가능하지만, 무선 LAN (Wireless Local Area Network)이나 [[149_serial_communication_rs232_rs485|직렬]] 링크 프로토콜에서는 전송권 조정과 재시도 제어가 훨씬 중요하다. 즉 [[001_dikw_pyramid|데이터]] 링크 계층은 고정 기능 집합이 아니라, **[[121_transmission_media_guided_unguided|매체]] 특성에 따라 두께가 달라지는 적응형 계층**이다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 링크 계층은 우리 동네 배송 규칙이고, 전송 계층은 전국 택배 시스템 전체 규칙에 가깝다. 동네에서 포장을 잘해도 전국 경로 전체가 자동으로 완벽해지는 것은 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[001_dikw_pyramid|데이터]] 링크 계층을 "무조건 신뢰적으로 만들 것인가"가 아니라, **링크 환경에 맞는 제어 강도를 어디까지 둘 것인가**로 판단한다. 예를 들어 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 유선 이더넷처럼 오류율이 낮고 [[015_지연_데이터_관점|지연]]에 민감한 환경에서는 링크 계층을 가볍게 유지하는 편이 유리하다. 반면 무선 링크나 잡음이 심한 [[149_serial_communication_rs232_rs485|직렬]] 회선에서는 로컬 재전송과 세밀한 회선 제어가 전체 성능을 오히려 높인다.

### 실무 판단 기준

1. **[[121_transmission_media_guided_unguided|매체]]가 공유형인가, 점대점인가?** 공유형이면 회선 제어와 [[121_transmission_media_guided_unguided|매체]] 접근 규칙이 더 중요하다.
2. **링크 오류율이 높은가?** 높다면 [[113_crc|CRC]] + 재전송의 가치가 커진다.
3. **수신 버퍼가 제한적인가?** 그렇다면 [[213_flow_control_buffer_overflow|흐름 제어]]가 없으면 손실이 급증한다.
4. **[[015_지연_데이터_관점|지연]] 민감도가 큰가?** 로컬 재전송이 오히려 지터와 [[015_지연_데이터_관점|지연]]을 키울 수도 있다.

아래 결정 흐름은 링크 특성에 따라 어떤 역할을 더 두껍게 설계할지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Choosing link-layer emphasis                                      │
├────────────────────────────────────────────────────────────────────┤
│ medium is shared?                                                 │
│   ├─ yes -> strong line control / MAC arbitration                 │
│   └─ no                                                           │
│       ├─ error rate is high? -> stronger error control / retries  │
│       ├─ receiver buffer small? -> tighter flow control           │
│       └─ latency critical and clean link? -> keep link thin       │
└────────────────────────────────────────────────────────────────────┘
```

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 링크 계층 재전송이 있으니 전송 계층 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]은 필요 없다고 오해하는 설계
- 버퍼 상황을 무시하고 송신 속도만 높여 수신 측 드롭을 유발하는 설계
- 공유 [[121_transmission_media_guided_unguided|매체]]에서 회선 제어 없이 모두 동시에 보내게 해 충돌과 재전송 폭주를 만드는 설계

시험 답안에서는 이 계층을 단순히 "오류 검사하는 층"이라고만 쓰면 부족하다. **[[184_framing_mechanism|프레이밍]]으로 경계를 만들고, 회선 제어로 질서를 만들고, [[213_flow_control_buffer_overflow|흐름 제어]]로 속도를 맞추고, [[188_error_control_overview|오류 제어]]로 신뢰를 보정한다**는 네 역할을 함께 설명해야 전체 그림이 완성된다.

- **📢 섹션 요약 비유**: 좁은 다리를 건널 때는 누가 먼저 건널지 정하고, 앞사람 속도에 맞추고, 발판이 부서졌는지 확인해야 안전하다. [[001_dikw_pyramid|데이터]] 링크 계층이 바로 그 다리 건너기 규칙이다.

---

## Ⅴ. 기대효과 및 결론

[[001_dikw_pyramid|데이터]] 링크 계층이 잘 설계되면 상위 계층은 매번 [[130_signal|신호]] 품질과 충돌 여부를 직접 걱정하지 않고도, **인접 노드 간 전달을 안정된 프레임 [[090_service_kubernetes_network_load_balancing|서비스]]로 사용할 수 있다**. 이 덕분에 네트워크 계층은 라우팅과 [[369_logic_bomb|논리]] 주소에 집중하고, 전송 계층은 종단 간 품질 제어에 집중할 수 있다. 즉 2계층은 전체 네트워크 스택의 분업을 가능하게 만드는 기초 안정화 층이다.

물론 한계도 분명하다. [[001_dikw_pyramid|데이터]] 링크 계층은 어디까지나 한 링크를 다루므로, 종단 간 순서 보장이나 혼잡 제어까지 대신하지는 못한다. 또한 링크를 지나치게 두껍게 만들면 [[015_지연_데이터_관점|지연]]과 복잡도가 늘고, 너무 얇게 만들면 상위 계층 부담이 커진다. 그래서 좋은 설계는 [[121_transmission_media_guided_unguided|매체]] 특성과 [[090_service_kubernetes_network_load_balancing|서비스]] 목표에 맞춰 **어느 정도의 링크 책임을 질 것인지**를 정교하게 정하는 일이다.

정리하면 [[001_dikw_pyramid|데이터]] 링크 계층은 **[[073_bit|비트]]를 프레임으로, 전송을 질서로, 오류 가능성을 관리 가능한 위험으로 바꾸는 계층**이다. 네 역할을 따로 외우기보다, "이웃한 두 장치가 믿고 대화하기 위한 지역 규칙"으로 묶어 기억하면 훨씬 오래 남는다.

- **📢 섹션 요약 비유**: 좋은 우체국은 편지를 봉투에 넣고, 창구 순서를 정하고, 너무 많이 몰리면 줄을 조절하고, 훼손된 편지는 다시 보내게 만든다. [[001_dikw_pyramid|데이터]] 링크 계층도 바로 그런 동네 우체국 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 프레임 (Frame) | [[001_dikw_pyramid|데이터]] 링크 계층의 기본 전송 단위다 |
| FCS (Frame Check Sequence) | 프레임 단위 오류 검출에 쓰이는 꼬리 정보다 |
| [[113_crc|CRC]] ([[113_crc|Cyclic Redundancy Check]]) | 대표적 오류 검출 알고리즘이다 |
| [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] (Automatic Repeat reQuest) | [[188_error_control_overview|오류 제어]]에서 재전송을 담당한다 |
| 슬라이딩 윈도우 (Sliding Window) | [[213_flow_control_buffer_overflow|흐름 제어]]와 [[188_error_control_overview|오류 제어]]에 함께 쓰인다 |
| [[744_load_line_calibration|LLC]] (Logical Link Control) | 상위 계층과의 [[369_logic_bomb|논리]] 제어 역할을 세분화한 부계층이다 |
| [[673_mac_message_authentication_code|MAC]] ([[121_transmission_media_guided_unguided|Media]] [[547_access_control_rwx|Access Control]]) | 공유 [[121_transmission_media_guided_unguided|매체]]에서 회선 제어를 구체화한 부계층이다 |

### 📈 관련 키워드 및 발전 흐름도

```text
비트 스트림만으로는 해석 불가
        │
        ▼
프레이밍으로 경계 설정
        │
        ▼
회선 제어로 전송 질서 부여
        │
        ▼
흐름 제어로 송수신 속도 조정
        │
        ▼
오류 제어로 로컬 신뢰성 보강
        │
        ▼
LLC · MAC · HDLC · PPP 등 세부 프로토콜로 확장
```

이 흐름도는 [[001_dikw_pyramid|데이터]] 링크 계층의 네 역할이 각각 따로 존재하는 것이 아니라, 링크 단위 통신 품질을 단계적으로 완성해 가는 구조임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_dikw_pyramid|데이터]] 링크 계층은 장난감 편지를 그냥 던지지 않고 상자에 넣어 옆 친구에게 보내는 규칙이에요.
2. 누가 먼저 보내고 얼마나 빨리 보내며, 상자가 찌그러졌는지도 여기서 살펴봐요.
3. 그래서 옆 친구는 엉킨 종이 대신 정리된 상자를 받아 더 쉽게 내용을 읽을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 302 / 1120

← **이전**: [[180_xpon_epon_gpon_10gpon|180. xPON (Passive Optical Network) - EPON, GPON, 10G-PON]]
**다음**: [[182_llc_logical_link_control|182. 논리적 링크 제어 (LLC, Logical Link Control) - IEEE 802.2]] →

---
