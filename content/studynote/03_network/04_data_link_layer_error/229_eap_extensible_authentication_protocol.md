---
title: 229. EAP (Extensible Authentication Protocol)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EAP는 [[001_dikw_pyramid|데이터]] 링크 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: EAP를 이해하면 오류율과 재전송 비용 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: EAP (Extensible [[604_authentication_factors|Authentication]] [[295_protocol_field_tcp_udp_icmp|Protocol]], RFC 3748)는 점대점 [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[224_ppp_point_to_point_protocol|PPP]])용으로 처음 개발되었으나, 현재는 무선 네트워크(IEEE 802.[[584_802_1x_pnac_eap_radius|1X]])의 필수 불가결한 표준 [[303_authentication_authorization_patterns|인증]] 구조로 자리 잡은 범용 [[303_authentication_authorization_patterns|인증]] 프레임워크다. EAP 자체는 특정 [[303_authentication_authorization_patterns|인증]] [[001_algorithm_definition|알고리즘]]이 아니며, 여러 [[303_authentication_authorization_patterns|인증]] [[001_algorithm_definition|알고리즘]]([[230_eap_tls_mutual_authentication_pki|EAP-TLS]], EAP-[[229_peap_protected_eap_tls_tunnel_authentication|PEAP]], EAP-TTLS 등)을 담아 나르는 '그릇' 역할을 한다.

- **필요성**: 기존의 PAP나 CHAP는 설계 당시 정해진 규칙대로만 동작하는 닫힌 구조였다. 지문 인식, 스마트카드, [[748_otp|OTP]] 등 수많은 [[303_authentication_authorization_patterns|인증]] 기술이 쏟아져 나오는데, 그때마다 라우터나 [[238_switch_operation_principles|스위치]]의 [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 갈아엎는 것은 불가능했다. 따라서 **"무슨 [[303_authentication_authorization_patterns|인증]] 수단을 쓰든 메시지 교환 절차는 하나로 통일하자"**는 유연한 표준 빈 그릇이 필요해졌다.

- **💡 비유**: EAP는 다양한 게임팩을 꽂을 수 있는 **"닌텐도 게임기 본체(콘솔)"**와 같습니다. EAP 본체 자체는 게임이 아니지만, '스마트카드 [[303_authentication_authorization_patterns|인증]] 팩', '[[303_authentication_authorization_patterns|인증]]서([[694_thread_local_storage_tls|TLS]]) [[303_authentication_authorization_patterns|인증]] 팩' 등 어떤 카트리지(EAP 메서드)를 꽂느냐에 따라 다양한 방식으로 동작합니다. 새로운 게임([[303_authentication_authorization_patterns|인증]] 기술)이 나와도 팩만 갈아 끼우면 됩니다.

```text
[CHAP]
    │
    ▼
[EAP]
    │
    └──▶ [이더넷 구조 및 원리]
```

- **📢 섹션 요약 비유**: ** EAP는 택배 회사의 **"표준 규격 상자"**입니다. 내용물이 유리잔(비밀번호)이든, 전자기기(생체 정보)이든, 보석(디지털 [[303_authentication_authorization_patterns|인증]]서)이든 상관없이 똑같은 네모난 상자에 담아 안전하게 배송해 주는 범용 포장 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. EAP의 핵심 구성 요소 (3-Tier 모델)
EAP [[303_authentication_authorization_patterns|인증]] 구조는 일반적으로 클라이언트, [[238_switch_operation_principles|스위치]](또는 [[572_ap_access_point_ds_distribution_system|AP]]), [[581_authentication_server|인증 서버]]의 세 부분으로 나뉜다.

1. **Supplicant (클라이언트)**: 네트워크 접속을 요청하는 단말기(노트북, 스마트폰).
2. **Authenticator ([[303_authentication_authorization_patterns|인증]]자)**: 접속을 제어하는 장비([[238_switch_operation_principles|스위치]], 무선 [[572_ap_access_point_ds_distribution_system|AP]]). 클라이언트가 누군지 직접 판단하지 않고, EAP 메시지를 서버로 토스(Pass-through)만 하는 '문지기' 역할.
3. **[[584_as|Authentication Server]] ([[581_authentication_server|인증 서버]])**: 실제 [[303_authentication_authorization_patterns|인증]] DB를 가지고 검증을 수행하는 백엔드 서버(일반적으로 [[541_radius_remote_authentication_aaa|RADIUS]] 서버).

### 2. IEEE 802.[[584_802_1x_pnac_eap_radius|1X]] 기반 EAP 동작 시퀀스
유선 포트나 무선 AP에 연결될 때 EAP 기반의 [[303_authentication_authorization_patterns|인증]] 절차는 다음과 같다. 이 과정에서 [[303_authentication_authorization_patterns|인증]]자([[572_ap_access_point_ds_distribution_system|AP]])는 내용물([[303_authentication_authorization_patterns|인증]] [[001_dikw_pyramid|데이터]])을 뜯어보지 않는다.

```text
 ┌───────────────────────────────────────────────────────────────┐
 │            IEEE 802.1X에서의 EAP 인증 과정 (EAP-TLS 예시)       │
 ├───────────────────────────────────────────────────────────────┤
 │                                                               │
 │ [Supplicant]          [Authenticator (AP)]        [RADIUS 서버]  │
 │  (노트북)                  (무선 공유기)               (인증 서버)   │
 │     │                         │                         │     │
 │     │ 1. EAPOL-Start (연결 요청)│                         │     │
 │     ├────────────────────────▶│                         │     │
 │     │                         │                         │     │
 │     │ 2. EAP-Request/Identity │                         │     │
 │     │◀────────────────────────┤                         │     │
 │     │                         │                         │     │
 │     │ 3. EAP-Response/Identity│                         │     │
 │     ├────────────────────────▶│                         │     │
 │     │                         │ 4. RADIUS Access-Request│     │
 │     │                         │    (EAP 메시지 포장)       │     │
 │     │                         ├────────────────────────▶│     │
 │     │                         │                         │     │
 │     │ 5. EAP 방식 협상 및 인증 교환 (서로 TLS 터널 등 생성)       │     │
 │     │◀────────────────────────┼────────────────────────▶│     │
 │     │                         │                         │     │
 │     │                         │ 6. RADIUS Access-Accept │     │
 │     │                         │◀────────────────────────┤     │
 │     │ 7. EAP-Success          │                         │     │
 │     │◀────────────────────────┤ 포트 잠금 해제 (통신 시작)  │     │
 │                                                               │
 └───────────────────────────────────────────────────────────────┘
```

### 3. 대표적인 EAP 확장 방식 (EAP Methods)
- **[[228_eap_md5_vulnerable_authentication|EAP-MD5]]**: CHAP와 비슷한 해시 [[303_authentication_authorization_patterns|인증]] ([[283_security_tactics|보안성]] 낮음).
- **[[230_eap_tls_mutual_authentication_pki|EAP-TLS]]**: 클라이언트와 서버 양방향 모두 X.509 디지털 [[303_authentication_authorization_patterns|인증]]서를 요구하는 가장 강력한 보안 (구축 비용 높음).
- **[[229_peap_protected_eap_tls_tunnel_authentication|PEAP]] / EAP-TTLS**: 서버 쪽에만 [[303_authentication_authorization_patterns|인증]]서를 설치하여 암호화된 [[694_thread_local_storage_tls|TLS]] 터널을 뚫은 뒤, 그 안전한 터널 안에서 클라이언트의 ID/PW를 검증하는 방식 (기업 환경에서 가장 널리 쓰임).

- **📢 섹션 요약 비유**: ** 무선 랜([[572_ap_access_point_ds_distribution_system|AP]]) 환경에서 EAP는 **"통역사([[572_ap_access_point_ds_distribution_system|AP]])를 낀 대화"**와 같습니다. AP는 클라이언트와 [[581_authentication_server|인증 서버]] 사이에서 무슨 말(어떤 [[303_authentication_authorization_patterns|인증]] 방식)이 오가는지 이해하지 못한 채, 오직 양쪽의 편지만 전달해 주다가 서버가 "이 사람 통과!"라고 외치면 그때 문을 열어주는 수동적인 중계자 역할을 합니다.

---

## Ⅲ. 비교 및 연결

EAP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. CHAP가 기반 조건을 만든다면, EAP는 그 위에서 핵심 메커니즘을 구현하고, [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 오류율과 재전송 비용에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | CHAP의 기반 정리 | EAP의 핵심 동작 | [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 오류율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: EAP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 EAP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [[228_chap_challenge_handshake_authentication_protocol|CHAP]] 수준의 기본 대책으로 충분한지, 아니면 EAP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 현재 문제의 핵심이 오류율 부족인지, 재전송 비용 악화인지 먼저 분리한다.
2. EAP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [[396_validation|확인]]한다.
3. 도입 후에는 인접 기술인 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리와의 연계 방식을 함께 검증한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- EAP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- CHAP와의 경계를 정리하지 않아 중복 투자나 [[164_policy|정책]] 충돌을 만드는 설계

- **📢 섹션 요약 비유**: EAP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

EAP는 [[001_dikw_pyramid|데이터]] 링크 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 오류율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리, 고신뢰 저지연 링크 제어, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 고신뢰 저지연 링크 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: EAP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[228_chap_challenge_handshake_authentication_protocol|CHAP]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[184_framing_mechanism|프레이밍]] ([[184_framing_mechanism|Framing]]) | 비트열을 의미 있는 전송 단위로 구분한다. |
| [[188_error_control_overview|오류 제어]] ([[188_error_control_overview|Error Control]]) | 검출과 [[658_ir_recovery|복구]] [[164_policy|정책]]을 함께 설계해야 한다. |
| [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: CHAP]
    │
    ▼
[현재 개념: EAP]
    │
    ├──▶ [확장 A: 이더넷 구조 및 원리]
    └──▶ [확장 B: 고신뢰 저지연 링크 제어]
```

EAP는 CHAP에서 출발해 현재 메커니즘을 정교화하고, 이후 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 구조 및 원리와 고신뢰 저지연 링크 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 편지를 보낼 때 봉투를 제대로 닫고 틀린 글자가 없는지 [[396_validation|확인]]해야 해요.
2. 이 개념은 편지가 깨지거나 사라졌을 때 다시 보내는 규칙까지 정해줘요.
3. 그래서 중간에 흔들려도 중요한 내용이 더 안전하게 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 350 / 1120

← **이전**: [[228_chap_challenge_handshake_authentication_protocol|228. CHAP (Challenge Handshake Authentication Protocol)]]
**다음**: [[230_ethernet_structure_and_principles_ieee_802_3|230. 이더넷 (Ethernet) 구조 및 원리 (IEEE 802.3)]] →

---
