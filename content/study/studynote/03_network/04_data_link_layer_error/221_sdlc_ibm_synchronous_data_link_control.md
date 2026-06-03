---
title: 221. SDLC (Synchronous Data Link Control)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] ([[010_동기식_비동기식_전송|Synchronous]] [[001_dikw_pyramid|Data]] Link Control)는 IBM이 1970년대에 개발한 [[073_bit|비트]] 지향형 동기식 [[001_dikw_pyramid|데이터]] 링크 제어 [[295_protocol_field_tcp_udp_icmp|프로토콜]]로, 메인프레임 통신 구조인 [[107_classification|SNA]] (Systems Network [[319_architecture|Architecture]])의 핵심 요소다.
> 2. **가치**: 기존 문자 지향형 [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 한계를 극복하고 [[001_dikw_pyramid|데이터]]의 투명성을 보장하는 [[187_bit_stuffing_flag_mechanism|비트 스터핑]] ([[187_bit_stuffing_flag_mechanism|Bit Stuffing]]) 기술을 도입하여 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있고 효율적인 [[001_dikw_pyramid|데이터]] 전송을 가능하게 했으며, 이후 [[216_hdlc_high_level_data_link_control|HDLC]] 등 다양한 [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 모태가 되었다.
> 3. **판단 포인트**: SDLC는 주국 (Primary)과 종국 (Secondary)의 철저한 마스터-슬레이브 구조를 가지며, 현대 네트워크 아키텍처에서는 역할이 줄어들었으나 [[448_polling_programmed_io|폴링]] ([[747_io_polling_overhead|Polling]]) 및 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있는 링크 제어의 기초 개념으로 여전히 교훈을 제공한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] ([[010_동기식_비동기식_전송|Synchronous]] [[001_dikw_pyramid|Data]] Link Control)는 점대점 ([[142_point_to_point_integration_spaghetti|Point-to-Point]]) 및 다중점 (Multipoint) 링크에서 동기식 ([[010_동기식_비동기식_전송|Synchronous]]) [[149_serial_communication_rs232_rs485|직렬]] [[001_dikw_pyramid|데이터]] 전송을 제어하기 위해 IBM에서 설계한 [[001_dikw_pyramid|데이터]] 링크 계층 ([[001_dikw_pyramid|Data]] Link Layer) [[295_protocol_field_tcp_udp_icmp|프로토콜]]이다. 
- **필요성**: 1970년대 이전의 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (예: [[019_bsc|BSC]])은 [[001_dikw_pyramid|데이터]] 전송 시 특정 제어 문자 집합에 의존하는 문자 지향 (Character-oriented) 방식이어서, [[001_dikw_pyramid|데이터]] 안에 제어 문자와 동일한 [[073_bit|비트]] 패턴이 포함될 경우 오동작하는 투명성 (Transparency) 문제가 있었다. 이를 해결하고 임의의 [[073_bit|비트]] 스트림을 안전하게 전송할 체계가 필요했다.
- **비유**: SDLC는 철저하게 통제되는 군대의 '지휘 계통'과 같다. 지휘관 (주국)이 명령을 내리기 전까지 부하 (종국)는 임의로 보고를 올릴 수 없으며, 모든 메시지는 규격화된 표준 봉투 (프레임)에 담겨 전달된다.
- **발전 과정**: IBM 시스템을 위해 탄생한 SDLC는 그 우수성을 인정받아 ISO에 의해 [[216_hdlc_high_level_data_link_control|HDLC]] (High-Level [[001_dikw_pyramid|Data]] Link Control)로 표준화되었으며, 이후 IEEE 802.2 [[744_load_line_calibration|LLC]], [[268_frame_relay_x25_simplification|Frame Relay]] 등의 기반이 되었다.

```text
  ┌─────────────────────────────────────────────────────────┐
  │                 문자 지향 vs 비트 지향                  │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │ [문자 지향 (BSC)]                                       │
  │  [SYN][SYN][STX] 데이터 (제어문자 포함 불가) [ETX][BCC] │
  │   → 데이터에 제어문자 패턴이 섞이면 프로토콜 파탄       │
  │                                                         │
  │ [비트 지향 (SDLC)]                                      │
  │  [01111110] 제어/주소 정보 + 임의의 데이터 [01111110]   │
  │   → 비트 스터핑 (Bit Stuffing)을 통해 완벽한 투명성 보장│
  └─────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: SDLC는 내용물에 상관없이 어떤 형태의 물건([[001_dikw_pyramid|데이터]])이든 똑같은 규격의 상자(프레임)에 담아, 오직 중앙 관제소(주국)의 통제 하에만 배송하는 강력한 택배 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 비유 |
|:---|:---|:---|:---|
| **[[186_character_stuffing_dle_stx_etx|플래그]] ([[186_character_stuffing_dle_stx_etx|Flag]])** | 프레임의 시작과 끝 표시 | 항상 `01111110` (16진수 7E) [[073_bit|비트]] 패턴 사용 | 편지 봉투의 겉면 |
| **주소 필드 (Address)** | 목적지 또는 출발지 [[655_ir_detection_analysis|식별]] | 종국 (Secondary)의 주소를 포함하여 8비트로 구성 | 수신인 주소 |
| **제어 필드 (Control)** | 프레임 유형 구분 및 제어 | 정보(I), 감독(S), 무번호(U) 프레임 결정 | 배송 요청 사항 |
| **정보 필드 (Info)** | 실제 전송될 사용자 [[001_dikw_pyramid|데이터]] | 가변 길이의 임의 [[073_bit|비트]] 스트림 | 편지 내용물 |
| **FCS (Frame Check Sequence)** | 오류 검출 | [[113_crc|CRC]] ([[113_crc|Cyclic Redundancy Check]])를 통한 [[003_integrity|무결성]] [[396_validation|확인]] | 봉인 씰 및 무게 [[396_validation|확인]] |

### 마스터-슬레이브 [[448_polling_programmed_io|폴링]] 구조

SDLC는 단일 주국 (Primary [[218_hdlc_station_primary_secondary|Station]])과 하나 이상의 종국 (Secondary [[218_hdlc_station_primary_secondary|Station]])으로 구성되는 비대칭 구조([[219_nrm_arm_abm_hdlc_modes|NRM]], Normal Response Mode)만을 지원한다.

```text
  ┌───────────────────────────────────────────────────────────────┐
  │                  SDLC 폴링 (Polling) 동작 구조                │
  ├───────────────────────────────────────────────────────────────┤
  │                                                               │
  │    [주국 (Primary)]                                           │
  │           │   "데이터 보낼 거 있니?" (Poll)                   │
  │           ├─────────────────────────┐                         │
  │           │                         ▼                         │
  │           │                 [종국 A (Secondary)]              │
  │           │                 "네, 데이터1 입니다." (Final)     │
  │           │◀────────────────────────┘                         │
  │           │                                                   │
  │           │   "너는 데이터 보낼 거 있니?" (Poll)              │
  │           ├────────────────────────────────────────┐          │
  │           │                                        ▼          │
  │           │                                [종국 B (Sec)]     │
  │           │                                "아니오." (Final)  │
  │           │◀──────────────────────────────────────┘          │
  └───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 주국은 링크의 모든 제어권을 가지며, 종국은 주국의 폴(Poll) 신호에만 응답할 수 있다. 이는 통신 충돌을 원천 차단하지만 주국에 부하가 집중되는 단점이 있다.

### [[187_bit_stuffing_flag_mechanism|비트 스터핑]] ([[187_bit_stuffing_flag_mechanism|Bit Stuffing]]) 메커니즘

[[001_dikw_pyramid|데이터]] 투명성을 보장하기 위한 SDLC의 가장 핵심적인 알고리즘이다. 페이로드 내에 [[186_character_stuffing_dle_stx_etx|플래그]]와 동일한 `01111110` 패턴이 우연히 등장하는 것을 막기 위해, 연속된 5개의 '1'이 나타나면 무조건 '0'을 하나 강제로 끼워 넣는다. 수신측은 연속된 5개의 '1' 뒤에 오는 '0'을 제거하여 원래 [[001_dikw_pyramid|데이터]]를 복원한다.

- **📢 섹션 요약 비유**: [[187_bit_stuffing_flag_mechanism|비트 스터핑]]은 금고의 비밀번호(01111110)와 똑같은 내용물이 박스에 담기는 것을 막기 위해, 유사한 번호(연속된 1 다섯 개)가 보이면 임시 스티커(0)를 붙였다가 도착 후 떼어내는 영리한 속임수입니다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | [[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] (IBM) | [[216_hdlc_high_level_data_link_control|HDLC]] (ISO) |
|:---|:---|:---|
| **표준화 주체** | IBM의 사설 (Proprietary) 규격 | ISO의 국제 표준 규격 |
| **운영 모드** | [[219_nrm_arm_abm_hdlc_modes|NRM]] (Normal Response Mode)만 지원 | [[219_nrm_arm_abm_hdlc_modes|NRM]], ARM, ABM (Asynchronous Balanced Mode) 지원 |
| **프레임 형식** | 기본 8비트의 배수로 정보 필드 구성 | [[073_bit|비트]] 단위 임의 길이 허용 |
| **확장성** | 메인프레임-터미널 종속적 | 점대점 및 피어투피어 통신에 유연함 |

HDLC는 SDLC를 모태로 하였으나, 피어투피어([[916_p2p_peer_to_peer_networking_super_node_gnutella|Peer-to-Peer]]) 통신이 가능한 ABM 모드를 추가하여 독립적인 노드 간 통신을 가능하게 했다는 점이 가장 큰 차이점이다.

- **📢 섹션 요약 비유**: SDLC가 철저한 군대의 지휘통제 시스템이라면, HDLC는 이 시스템을 발전시켜 민간인(동등한 권한의 노드)들끼리도 자유롭게 연락할 수 있게 만든 범용 통신망과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

과거 금융권이나 대기업의 레거시 메인프레임 시스템에서 터미널(지점)을 관리할 때 SDLC가 광범위하게 쓰였다. 만약 어느 한 지점의 단말기가 고장 나면 주국의 [[448_polling_programmed_io|폴링]]에 응답하지 못하므로, 해당 링크의 시간 지연이 발생하지만 전체 네트워크의 충돌로는 이어지지 않는다. 현대에는 이러한 레거시 시스템을 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]]/Internet [[295_protocol_field_tcp_udp_icmp|Protocol]]) 위에서 캡슐화하여 전송하는 DLSw ([[001_dikw_pyramid|Data]] Link Switching) 같은 기술이 사용된다.

- **도입**: 오늘날 신규 시스템에 SDLC를 구축하는 일은 없다. 그러나 기존 IBM 기반 메인프레임 장비를 유지 보수하거나 타 시스템과 연동해야 할 경우, [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환기를 통해 [[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] 트래픽을 처리해야 한다.
- **[[128_water_scrum_fall_anti_pattern|안티패턴]]**: 메인프레임과 무관한 환경에서 마스터-슬레이브 구조의 중앙 집중식 링크 제어를 설계하면, [[454_spof|단일 장애점]]([[454_spof|SPOF]], Single Point of Failure)이 발생하고 확장성이 크게 저하된다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 현대의 자율주행 자동차 시대에 구형 증기기관차를 새로 만들지는 않지만, 옛날 기찻길이 남아있는 구간에서는 그 궤도에 맞는 특수 바퀴([[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환)를 달아야 하는 이치와 같습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 내용 | 개선 효과 |
|:---|:---|:---|
| **정량** | [[187_bit_stuffing_flag_mechanism|비트 스터핑]]으로 인한 오버헤드 | [[001_dikw_pyramid|데이터]] 크기에 비례하여 동적 제어, 충돌 감소 |
| **정성** | 제어와 [[001_dikw_pyramid|데이터]]의 완벽한 분리 | [[001_dikw_pyramid|데이터]] 투명성 확보 및 통신 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 극대화 |

[[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] 자체는 역사의 뒤안길로 사라진 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이지만, [[073_bit|비트]] 지향적 [[184_framing_mechanism|프레이밍]], [[187_bit_stuffing_flag_mechanism|비트 스터핑]], CRC를 통한 [[188_error_control_overview|오류 제어]], 순서 번호를 이용한 [[213_flow_control_buffer_overflow|흐름 제어]] 등 SDLC가 확립한 패러다임은 오늘날의 거의 모든 링크 계층 [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[230_ethernet_structure_and_principles_ieee_802_3|이더넷]], Wi-Fi 등)에 계승되어 살아 숨 쉬고 있다. 중앙 집중식 제어의 한계를 이해하고 분산형 네트워크로 나아간 IT 발전의 훌륭한 반면교사이다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 현대의 [[148_5g_embb_urllc_mmtc|초고속]] 인터넷 고속도로 역시 그 바닥을 파보면 SDLC라는 튼튼한 고대 로마식 벽돌이 기초로 깔려 있는 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[220_hdlc_frames_i_s_u|정보 프레임]], 감독/제어, 비번호 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[184_framing_mechanism|프레이밍]] ([[184_framing_mechanism|Framing]]) | [[073_bit|비트]]열을 의미 있는 전송 단위로 구분한다. |
| [[188_error_control_overview|오류 제어]] ([[188_error_control_overview|Error Control]]) | 검출과 [[658_ir_recovery|복구]] 정책을 함께 설계해야 한다. |
| [[222_lapb_link_access_procedure_balanced|LAPB]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 정보 프레임, 감독/제어, 비번호]
    │
    ▼
[현재 개념: SDLC]
    │
    ├──▶ [확장 A: LAPB]
    └──▶ [확장 B: 고신뢰 저지연 링크 제어]
```

SDLC는 [[220_hdlc_frames_i_s_u|정보 프레임]], 감독/제어, 비번호에서 출발해 현재 메커니즘을 정교화하고, 이후 LAPB와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [[396_validation|확인]]해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.
