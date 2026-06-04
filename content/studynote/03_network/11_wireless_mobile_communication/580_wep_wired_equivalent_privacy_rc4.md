+++
title = "580. WEP (Wired Equivalent Privacy)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WEP는 무선·이동통신에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: WEP를 이해하면 스펙트럼 효율과 이동성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

1997년 제정된 최초의 IEEE 802.[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 무선 LAN 표준에 포함된 기본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화 프로토콜입니다. 무선 통신 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 공기 중으로 평문(Cleartext) 전송되어 스니핑당하는 것을 막기 위해 개발되었습니다.

```text
[무선 LAN 보안 진화]
    |
    v
[WEP]
    |
    +---> [WPA]
```

- **📢 섹션 요약 비유**: WEP는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- <strong><a href="/knowledge-base/studynote/09_security/02_crypto/081_rc4_stream_cipher/">RC4</a> <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/">스트림 암호</a>)</strong>: WEP는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화할 때 RC4라는 매우 빠르고 가벼운 암호화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 사용합니다.
- **암호키의 조합**: 사용자가 공유기에 설정한 고정 비밀번호(예: 40bit WEP [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))에다가, 패킷을 보낼 때마다 랜덤하게 변하는 <strong>24bit짜리 짧은 주사위 번호인 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">IV</a>(Initialization Vector, 초기화 벡터)</strong>를 섞어서 매번 64bit짜리 최종 암호화 열쇠([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/))를 만들어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 잠급니다.

```text
[무선 LAN 보안 진화]
    |
    v
[WEP]
    |
    +---> [WPA]
```

- **📢 섹션 요약 비유**: WEP의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

### 1. [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)(초기화 벡터)의 길이가 너무 짧음 (재사용 문제)
- IV는 24비트밖에 되지 않아 경우의 수가 약 1,600만 개(2^24)뿐입니다.
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 트래픽이 많은 공유기에서는 이 1,600만 개의 주사위 번호가 순식간에 고갈되어, <strong>결국 며칠 전이나 몇 분 전에 썼던 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">IV</a> 번호를 다시 재사용</strong>하게 됩니다.
- 해커가 공기 중에서 겹치는 IV를 가진 패킷 2개를 캡처해 XOR(수학적 배타적 논리합) 연산을 돌려버리면, 안에 숨겨진 진짜 비밀번호(고정 키)가 스르륵 풀려버립니다.

### 2. 정적 키(Static [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 기반의 구조
- [WPA](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/581_wpa_tkip_802_1x_eap/) 방식처럼 5분마다 키를 자동으로 바꿔주는 기능이 없습니다. 관리자가 수동으로 공유기 세팅 페이지에 들어가 비밀번호를 바꾸지 않는 이상, 모든 사용자가 영구적으로 똑같은 비밀번호 키 하나를 공유합니다.

### 3. [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 검증의 부재 (CRC-32의 한계)
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 중간에 위변조되지 않았는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하기 위해 CRC-32라는 오류 검출 코드를 쓰지만, 이는 악의적인 위조를 막는 암호학적 해시(SHA 등)가 아니라 단순 통신 에러 검출용입니다. 해커가 암호화된 패킷 내용을 자기 마음대로 조작해서 다시 쏴도 공유기가 눈치채지 못합니다.

WEP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 무선 LAN 보안 진화가 기반 조건을 만든다면, WEP는 그 위에서 핵심 메커니즘을 구현하고, WPA는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스펙트럼 효율과 이동성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 무선 LAN 보안 진화의 기반 정리 | WEP의 핵심 동작 | WPA의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스펙트럼 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: WEP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **사용 금지 조치**: WEP의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 붕괴는 소프트웨어 업데이트로 고칠 수 없는 구조적 결함이므로, 2004년 공식적으로 사용이 중단(Deprecated) 권고되었습니다.
- 해킹 툴인 Aircrack-ng 등을 사용하면 초보자도 유튜브를 보고 따라 해 5~10분 이내에 WEP 공유기 비밀번호를 알아낼 수 있습니다. 반드시 [WPA2](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/582_wpa2_aes_ccmp_personal_enterprise/)/[WPA3](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/583_wpa3_sae_owe_enhanced_open/) 이상의 최신 [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 기반 보안을 사용해야 합니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: WEP는 중요한 문서를 보낼 때마다 '비밀번호 + 1번부터 100번까지 적힌 종이표([IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))'를 같이 넣어서 금고를 잠그는 방식입니다. 종이표 번호가 100번까지밖에 없으니, 101번째 문서를 보낼 때는 어쩔 수 없이 예전에 썼던 1번 종이표를 다시 꺼내어 씁니다([IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 재사용). 밖에서 잠복하던 도둑(해커)은 "어? 아까 1번 종이표랑 똑같은 금고가 또 지나가네?" 하고 두 금고의 암호 패턴을 비교 분석해 진짜 비밀번호를 수학적으로 쉽게 역추적해버립니다.

---

## Ⅴ. 기대효과 및 결론

WEP는 무선·이동통신을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스펙트럼 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [WPA](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/581_wpa_tkip_802_1x_eap/), 지능형 무선 자원 제어, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 무선 자원 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: WEP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 무선 LAN 보안 진화 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 셀 (Cell) | 무선 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 범위를 나누는 기본 단위다. |
| [핸드오버](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/) ([Handover](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/)) | 이동 중에도 연결을 유지하게 만든다. |
| [WPA](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/581_wpa_tkip_802_1x_eap/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 무선 LAN 보안 진화]
    |
    v
[현재 개념: WEP]
    |
    +---> [확장 A: WPA]
    +---> [확장 B: 지능형 무선 자원 제어]
```

WEP는 무선 LAN 보안 진화에서 출발해 현재 메커니즘을 정교화하고, 이후 WPA와 지능형 무선 자원 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 걸어 다니면서 무전기를 쓰면 멀어질수록 소리가 작아지고 다른 친구 목소리와 섞여요.
2. 이 개념은 어디서 말할지, 얼마나 크게 말할지, 언제 다른 기지국으로 옮길지를 정해줘요.
3. 그래서 움직이면서도 통화나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 덜 끊기게 도와줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 701 / 1120

<- **이전**: [579. 무선 LAN 보안 진화 (WEP -> WPA -> WPA2 -> WPA3)](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/579_wlan_security_evolution_wep_wpa/)
**다음**: [581. WPA (TKIP + 802.1X + EAP)](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/581_wpa_tkip_802_1x_eap/) ->

---
