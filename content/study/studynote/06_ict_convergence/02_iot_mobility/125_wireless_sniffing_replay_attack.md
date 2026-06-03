+++
weight = 125
title = "125. 무선 스니핑 & 리플레이 공격 - IoT/무선 환경 도청·재전송 위협"
date = "2026-04-19"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 무선 스니핑은 **무선 통신(Wi-Fi·[[607_ble_bluetooth_low_energy_iot|BLE]]·[[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]])의 패킷을 [[701_sniffing_eavesdropping_promiscuous|도청]]**하는 것이고, 리플레이 공격은 **정상 통신을 캡처한 후 동일 패킷을 재전송(Replay)**하여 [[303_authentication_authorization_patterns|인증]] 우회·명령 재실행을 수행하는 공격이다.
> 2. **가치**: [[101_iot_concept|IoT]] 디바이스는 리소스 제한으로 **암호화·[[303_authentication_authorization_patterns|인증]]이 미흡**한 경우가 많아, 도어락의 잠금 해제 신호를 캡처→재전송하면 **물리적 침입**이 가능해지는 등 실물 피해로 이어진다.
> 3. **판단 포인트**: 리플레이 방지 핵심은 **타임스탬프·[[519_oidc_nonce|Nonce]](일회용 값)·시퀀스 번호**를 포함하여 동일 패킷의 재사용을 탐지·차단하는 것이며, [[694_thread_local_storage_tls|TLS]]/DTLS가 근본 해결책이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    리플레이 공격 흐름                                 │
├───────────────────────────────────────────────────────┤
│  1. [정상] Alice → IoT 도어락: "열어줘" (신호 전송)  │
│  2. [공격자] 신호 캡처 (무선 스니핑)                  │
│  3. [나중에] 공격자 → 도어락: 동일 "열어줘" 재전송   │
│  4. 도어락: "열어줘" 수신 → 문 열림! (인증 우회)     │
│                                                       │
│  방어: Nonce·타임스탬프·시퀀스 번호 → 동일 패킷 거부 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 리플레이 공격은 **녹음기로 비밀번호를 녹음**해서 나중에 다시 틀어 문을 여는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 리플레이 방어 기법

| 기법 | 설명 |
|:---|:---|
| **[[519_oidc_nonce|Nonce]]** | 일회용 랜덤 값 포함 → 재사용 탐지 |
| **타임스탬프** | 유효 시간 내만 수용 |
| **시퀀스 번호** | 순서 번호 [[395_verification_process_review|검증]] |
| **[[644_dtls_datagram_tls_coap_security|DTLS]]/[[694_thread_local_storage_tls|TLS]]** | 암호화 채널 + [[519_oidc_nonce|Nonce]] 내장 |

- **📢 섹션 요약 비유**: Nonce는 일회용 도장이다. 한 번 쓴 도장은 다시 쓸 수 없으므로 복사(리플레이)가 불가능하다.

---

## Ⅲ. 비교 및 연결

| 비교 | 스니핑 | 리플레이 | MITM |
|:---|:---|:---|:---|
| **행위** | [[701_sniffing_eavesdropping_promiscuous|도청]] | **재전송** | 중간 변조 |
| **목적** | 정보 수집 | **[[303_authentication_authorization_patterns|인증]] 우회** | 변조·[[701_sniffing_eavesdropping_promiscuous|도청]] |
| **방어** | 암호화 | **[[519_oidc_nonce|Nonce]]·시퀀스** | **상호 [[303_authentication_authorization_patterns|인증]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[101_iot_concept|IoT]] 리플레이 공격 대상
- 스마트 도어락, 차량 키리스 시스템(RKE), [[894_scada|SCADA]] 제어.

---

## Ⅴ. 기대효과 및 결론

무선 스니핑·리플레이는 **[[101_iot_concept|IoT]] 보안의 기본 위협**이며, [[519_oidc_nonce|Nonce]]·타임스탬프·[[644_dtls_datagram_tls_coap_security|DTLS]] 적용이 필수 대응이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **스니핑** | 무선 패킷 [[701_sniffing_eavesdropping_promiscuous|도청]] |
| **리플레이** | 캡처 패킷 [[274_replay_attack|재전송 공격]] |
| **[[519_oidc_nonce|Nonce]]** | 일회용 값 (리플레이 방지) |
| **[[644_dtls_datagram_tls_coap_security|DTLS]]** | [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반 암호화 ([[101_iot_concept|IoT]]) |
| **MITM** | [[706_mitm_man_in_the_middle_hsts|중간자 공격]] (스니핑+변조) |

### 📈 관련 키워드 및 발전 흐름도

```text
[무선 도청 (WEP 취약점, 2001)]
    │
    ▼
[WPA/WPA2 (2004) — 무선 암호화 강화]
    │
    ▼
[IoT 리플레이 공격 (도어락·차량, 2015~)]
    │
    ▼
[DTLS / TLS 1.3 적용 (2018~)]
    │
    ▼
[현재: PQC (포스트 양자 암호) — 양자 컴퓨터 대응]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 스니핑은 **남의 대화를 몰래 듣는([[701_sniffing_eavesdropping_promiscuous|도청]])** 거예요.
2. 리플레이는 **"비밀번호"를 녹음해서** 나중에 다시 틀어 문을 여는 거예요.
3. 일회용 비밀번호([[519_oidc_nonce|Nonce]])를 쓰면 **녹음해도 다시 못 쓰니까** 안전해요!
