---
title: 196. CRC-16, CRC-32 (Ethernet FCS), CRC-CCITT
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 [[001_dikw_pyramid|데이터]] 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

나누는 수(제수)를 무엇으로 하느냐에 따라 에러 검출 확률이 극명하게 달라집니다.
좋은 [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]]은 다음의 수학적 조건을 반드시 만족해야 합니다.
- [[195_polynomial_generator_crc|다항식]]의 끝에는 반드시 **`+ 1`** (상수항)이 있어야 합니다. 그래야 단일 [[073_bit|비트]] 에러를 무조건 다 잡습니다.
- [[197_burst_error_detection_crc|버스트 에러]](연속 에러)를 잡으려면 [[195_polynomial_generator_crc|다항식]]이 충분히 길고 여러 항이 섞여 있어야 합니다.

```text
[다항식 연산 / 생성 다항식]
    │
    ▼
[CRC-16, CRC-32, CRC-CCIT…]
    │
    └──▶ [버스트 에러 검출 능력 유지]
```

- **📢 섹션 요약 비유**: [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

네트워크 장비나 [[295_protocol_field_tcp_udp_icmp|프로토콜]]에 따라 사용하는 톱니바퀴([[195_polynomial_generator_crc|다항식]]) 규격이 다릅니다.

### 1. [[113_crc|CRC]]-16 (IBM 표준)
- **[[195_polynomial_generator_crc|다항식]]**: $x^{16} + x^{15} + x^2 + 1$ (이진수: `11000000000000101`)
- **FCS 꼬리 길이**: 16비트 (2바이트)
- **용도**: 과거 USB나 [[605_bluetooth_ieee_802_15_1_piconet_scatternet|블루투스]], [[459_quic_fec_forward_error_correction|초기]] [[146_modem_modulator_demodulator|모뎀]] 통신([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]) 등에서 짧은 [[001_dikw_pyramid|데이터]]를 보낼 때 쓰였습니다.

### 2. [[113_crc|CRC]]-CCITT (유럽 통신 표준)
- **[[195_polynomial_generator_crc|다항식]]**: $x^{16} + x^{12} + x^5 + 1$
- **FCS 꼬리 길이**: 16비트 (2바이트)
- **용도**: 위 [[113_crc|CRC]]-16과 길이는 같지만 항의 위치가 다릅니다. [[216_hdlc_high_level_data_link_control|HDLC]](고위 [[001_dikw_pyramid|데이터]] 링크 제어) [[295_protocol_field_tcp_udp_icmp|프로토콜]], X.25, 그리고 플로피 디스크 시절의 [[501_file_definition_logical_record|파일]] 전송 에러 검사에 주로 쓰였습니다.

### 3. [[113_crc|CRC]]-32 (IEEE 802 표준 / Ethernet의 지배자) ★
- **[[195_polynomial_generator_crc|다항식]]**: $x^{32} + x^{26} + x^{23} + x^{22} + x^{16} + x^{12} + x^{[[308_static_dynamic_nat_pat_port_address_translation|11]]} + x^{[[489_raid_10_hybrid|10]]} + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1$
- **FCS 꼬리 길이**: 32비트 (4바이트)
- **용도**: 현재 우리가 쓰는 **LAN 선([[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[673_mac_message_authentication_code|MAC]] 프레임), 와이파이(Wi-Fi 802.[[308_static_dynamic_nat_pat_port_address_translation|11]]), [[347_compaction|압축]] 프로그램(ZIP, RAR), PNG 이미지 [[501_file_definition_logical_record|파일]] 포맷** 등 거대하고 방대한 [[001_dikw_pyramid|데이터]]를 에러 없이 지켜내는 절대적인 글로벌 표준입니다. 이 [[195_polynomial_generator_crc|다항식]]을 뚫고 에러가 정상으로 위장할 확률은 거의 0%에 수렴합니다.

```text
[다항식 연산 / 생성 다항식]
    │
    ▼
[CRC-16, CRC-32, CRC-CCIT…]
    │
    └──▶ [버스트 에러 검출 능력 유지]
```

- **📢 섹션 요약 비유**: ** [[113_crc|CRC]] [[195_polynomial_generator_crc|다항식]]은 자물쇠를 따는 **'마스터키의 톱니바퀴 모양'**입니다. [[113_crc|CRC]]-16이 동네 자전거 자물쇠를 지키는 짧고 듬성듬성한 16칸짜리 열쇠라면, [[113_crc|CRC]]-32는 은행 금고를 지키는 32칸짜리 엄청나게 정밀하고 복잡한 특수 열쇠입니다. 이 32개의 톱니바퀴에 딱 들어맞게 에러가 우연히 생길 확률은 로또를 연속 2번 맞는 것보다 어렵습니다.

---

## Ⅲ. 비교 및 연결

[[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[195_polynomial_generator_crc|다항식]] 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]]이 기반 조건을 만든다면, [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 그 위에서 핵심 메커니즘을 구현하고, [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 오류율과 재전송 비용에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[195_polynomial_generator_crc|다항식]] 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]]의 기반 정리 | [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…의 핵심 동작 | [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 오류율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [[195_polynomial_generator_crc|다항식]] 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]] 수준의 기본 대책으로 충분한지, 아니면 [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 현재 문제의 핵심이 오류율 부족인지, 재전송 비용 악화인지 먼저 분리한다.
2. [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [[396_validation|확인]]한다.
3. 도입 후에는 인접 기술인 [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지와의 연계 방식을 함께 검증한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [[195_polynomial_generator_crc|다항식]] 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]]와의 경계를 정리하지 않아 중복 투자나 [[164_policy|정책]] 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 [[001_dikw_pyramid|데이터]] 링크 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 오류율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지, 고신뢰 저지연 링크 제어, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[195_polynomial_generator_crc|다항식]] 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[184_framing_mechanism|프레이밍]] ([[184_framing_mechanism|Framing]]) | [[073_bit|비트]]열을 의미 있는 전송 단위로 구분한다. |
| [[188_error_control_overview|오류 제어]] ([[188_error_control_overview|Error Control]]) | 검출과 [[658_ir_recovery|복구]] [[164_policy|정책]]을 함께 설계해야 한다. |
| [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 다항식 연산 / 생성 다항식]
    │
    ▼
[현재 개념: CRC-16, CRC-32, CRC-CCIT…]
    │
    ├──▶ [확장 A: 버스트 에러 검출 능력 유지]
    └──▶ [확장 B: 고신뢰 저지연 링크 제어]
```

[[113_crc|CRC]]-16, [[113_crc|CRC]]-32, [[113_crc|CRC]]-CCIT…는 [[195_polynomial_generator_crc|다항식]] 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]]에서 출발해 현재 메커니즘을 정교화하고, 이후 [[197_burst_error_detection_crc|버스트 에러]] 검출 능력 유지와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [[396_validation|확인]]해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 317 / 1120

← **이전**: [[195_polynomial_generator_crc|195. 다항식(Polynomial) 연산 / 생성 다항식 (Generator Polynomial)]]
**다음**: [[197_burst_error_detection_crc|197. 버스트 에러 (Burst Error) 검출 능력 유지]] →

---
