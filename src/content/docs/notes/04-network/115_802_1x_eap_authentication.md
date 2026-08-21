---
sidebar:
  order: 115
  label: "115. 802.1X EAP 인증"
  badge:
    text: "기출 · 50%"
    variant: note
title: "포트 기반 네트워크 접근 제어 표준 : IEEE 802.1X 및 EAP (Port-Based Authentication)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 115
extra:
  question_no: "115"
  source_status: "기출"
  source_history: "134회"
  priority: 50
  priority_note: "3대 구성요소(Supplicant, Authenticator, Authentication Server), EAPOL/RADIUS, EAP-TLS/PEAP/TTLS, MAB"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IEEE 802.1X**: 유선 이더넷 스위치 및 무선 Wi-Fi AP의 물리적/논리적 포트에 대해, 인증되지 않은 단말의 일반 데이터 통신을 하드웨어 레벨에서 차단(Unauthorized State)하고 오직 인증 프레임(EAPOL)만을 수신하여 인증 완료 후 포트를 동적 개방(Authorized State)하는 포트 기반 네트워크 접근 제어 표준.
- **EAP(Extensible Authentication Protocol, RFC 3748)**: 다양한 인증 방식(ID/PW, 인증서, OTP, 스마트카드)을 특정 링크 계층(L2)에 종속되지 않고 범용 요청/응답 메시지 규격으로 캡슐화하여 운반하는 확장 인증 프레임워크.

</details>

- 정의/개념: 단말(Supplicant), 접속 스위치(Authenticator), 인증 서버(RADIUS)의 3자 모델을 기반으로, L2 구간은 **EAPOL(EAP over LAN)**, 백엔드 구간은 **RADIUS/EAP** 프로토콜로 EAP 인증 메시지를 중계 캡슐화하여 강력한 상호 인증 및 동적 세션 키를 생성하는 **엔터프라이즈 접근 통제 표준 프레임워크**
- 배경/필요성: 단순 공유 비밀번호(PSK)나 취약한 MAC 주소 필터링의 보안 한계를 극복하고, 개별 사용자/기기 단위의 암호학적 신원 검증과 네트워크 권한 세분화를 달성할 요구

#### 한줄 요약
- 802.1X 포트 제어와 EAP 인증 프레임워크를 결합하여 인증 성공 시에만 스위치 포트를 동적 개방한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **EAP-TLS(RFC 5216 / 9190)**: 클라이언트와 인증 서버 양측이 X.509 디지털 인증서를 상호 교환하여 검증함으로써, 피싱 서버 및 패킷 도청 위협을 100% 원천 차단하는 가장 강력한 보안 등급의 EAP 방식.
- **PEAP(Protected EAP) / EAP-TTLS**: 단말에 인증서를 배포하기 어려운 환경에서, 인증 서버의 인증서로 먼저 TLS 암호화 터널을 수립한 후 그 내부에서 안전하게 사용자 ID/PW(MS-CHAPv2)를 인증하는 터널링 방식.

</details>

- **3계층 명확한 역할 분담 아키텍처**: 단말(Supplicant) $\leftrightarrow$ 스위치/AP(Authenticator) $\leftrightarrow$ 인증 서버(Authentication Server: RADIUS/ISE)
- **이종 전송 구간 프로토콜 캡슐화**: 유무선 L2 구간은 IEEE 802.1X EAPOL, L3 백엔드 구간은 UDP 기반 RADIUS(RFC 2865/3579)로 메시지 변환 중계
- **인증 성공 시 동적 정책 주입**: 인증 서버가 RADIUS Access-Accept 응답에 동적 VLAN ID(Tunnel-Private-Group-ID) 및 dACL을 실어 포트에 즉시 적용

#### 한줄 요약
- 3자 분업 모델, EAPOL/RADIUS 프로토콜 중계, EAP-TLS 상호 인증, 동적 VLAN/dACL 주입을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EAPOL(EAP over LAN, IEEE 802.1X)**: L2 이더넷 프레임(EtherType 0x888E) 상에서 EAP 패킷(EAP-Start, EAP-Packet, EAP-Logoff, EAP-Key)을 직접 캡슐화하여 전송하는 근거리망 프로토콜.
- **MAB(MAC Authentication Bypass)**: 802.1X 서플리컨트가 탑재되지 않은 프린터, IP 전화기, IoT 기기의 MAC 주소를 RADIUS 서버에서 사전 등록된 화이트리스트와 대조하여 예외적으로 포트를 개방해 주는 우회 메커니즘.

</details>

```text
[ 단말 (Supplicant: PC/Phone) ]
 ├─ 802.1X 클라이언트 드라이버
 └─ EAP-TLS / PEAP 인증 모듈
           │
           ▼ (1. L2 EAPOL 프레임: EtherType 0x888E)
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 인증 중계자 (Authenticator: L2 Switch / Wi-Fi AP) ]                   │
│  ├─ 제어 포트 (Controlled Port: 인증 전 차단 / 인증 후 개방)            │
│  ├─ 비제어 포트 (Uncontrolled Port: 오직 EAPOL 패킷만 통과)             │
│  └─ EAPOL ➔ RADIUS 패킷 변환 중계 엔진 (L2/L3 Gateway)                 │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. L3 RADIUS over UDP 1812: EAP-Message 속성)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 인증 서버 (Authentication Server: RADIUS / Cisco ISE) ]                │
│  ├─ EAP 협상 및 인증서/비밀번호 검증 (EAP-TLS, PEAP-MSCHAPv2)            │
│  ├─ 신원 데이터베이스 질의 (Active Directory, LDAP, PKI CA)             │
│  └─ 마스터 암호키(MSK) 유도 및 동적 VLAN/dACL 응답 반환                 │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 단말이 EAPOL로 보낸 인증 요청이 스위치(Authenticator)에서 RADIUS 패킷으로 변환되어 인증 서버로 전달되고, 인증 성공 시 포트가 개방되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **인증 요청자 (Supplicant)** | 단말 OS에 내장된 802.1X 클라이언트로, 사용자 자격 증명 또는 인증서 제시 | Windows 802.1X |
| **인증 중계자 (Authenticator)**| 스위치/AP로, 단말의 EAPOL 프레임을 수신하여 RADIUS 패킷으로 재포장 중계 | L2 Switch / WLC |
| **인증 서버 (RADIUS Server)** | EAP 인증 최종 수행, Active Directory 계정 확인, 접근 권한(VLAN) 인가 | FreeRADIUS / ISE |
| **신원/인증서 저장소** | 기업 내부 사설 PKI(Root CA/CRL) 및 직원 디렉터리(AD/LDAP) 계정 DB | Directory / PKI |
| **동적 포트 제어기** | 인증 성공 전에는 비인가 포트로 격리하고, 성공 후 802.1Q VLAN 태그를 주입 | 802.1Q / dACL |

#### 한줄 요약
- 서플리컨트, 인증 중계자(스위치/AP), 인증 서버(RADIUS), 신원/PKI 저장소, 동적 포트 제어기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **마스터 세션 키(Master Session Key, MSK)**: EAP-TLS 핸드셰이크 성공 시 단말과 인증 서버가 독립적으로 유도하는 64바이트 암호 키로, Wi-Fi WPA3 4-Way Handshake의 PMK(Pairwise Master Key)로 사용되어 무선 구간 암호화를 완성하는 핵심 키.

</details>

```text
1. 단말이 스위치 포트에 연결 ➔ 단말이 L2 멀티캐스트로 'EAPOL-Start' 프레임 송출
            │
            ▼
2. 스위치(Authenticator)가 'EAP-Request/Identity' 프레임을 단말로 전송
            │
            ▼
3. 단말이 사용자 ID를 담은 'EAP-Response/Identity' 회신 ➔ 스위치가 RADIUS Access-Request로 변환하여 서버에 전달
            │
            ▼
4. RADIUS 서버와 단말 간에 스위치를 거쳐 EAP-TLS 핸드셰이크(인증서 교환 및 상호 서명 검증) 수행
            │
            ▼
5. [인증 성공] ➔ RADIUS 서버가 'Access-Accept'(동적 VLAN 10 + MSK) 회신 ➔ 스위치 통제 포트 완전 개방
```

**동작 원리**

1. **포트 초기 차단**: 물리 링크 연결 시 일반 ARP, IP 트래픽은 모두 드롭되고 오직 EAPOL만 통과
2. **신원 식별**: 단말이 전송한 Identity를 기반으로 인증 서버가 적절한 EAP 방식(TLS/PEAP) 협상
3. **상호 암호 검증**: 단말은 서버 인증서를 검증하여 가짜 AP를 차단하고, 서버는 단말 인증서를 검증
4. **암호키 유도**: 인증 성공 시 양단이 상호 교환된 난수를 통해 MSK 암호키를 수학적으로 도출
5. **인가 정책 적용**: 스위치가 RADIUS 응답의 벤더 속성(VSA)을 파싱하여 포트에 VLAN 및 ACL 즉시 구성

#### 한줄 요약
- EAPOL-Start, Identity 요청/응답, EAP-TLS 상호 검증, RADIUS Access-Accept 반환, 포트 개방 및 정책 적용 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **주요 EAP 인증 방식 비교**: 최고 보안 등급 EAP-TLS, 계정 중심 PEAP/TTLS, 레거시 MAB의 메커니즘 비교.

</details>

| 비교 항목 | EAP-TLS (RFC 5216) | PEAP / EAP-TTLS | MAC 인증 우회 (MAB) |
|:---|:---|:---|:---|
| **인증 메커니즘** | **클라이언트 & 서버 양방향 인증서 상호 검증**| **서버 인증서로 TLS 터널 수립 후 ID/PW 인증**| **단말의 L2 MAC 주소만 RADIUS DB 대조** |
| **보안 강도** | **최고 (비밀번호 탈취 및 피싱 공격 원천 차단)**| 높음 (서버 인증서 검증 필수) | **낮음 (MAC 스푸핑 위조 취약)** |
| **단말 인증서 요구** | **필수 (사내 MDM/PKI 인증서 사전 배포)** | **불필요 (사용자 계정/패스워드만 사용)** | 불필요 (802.1X 미지원 IoT 전용) |
| **주요 위협 요인** | 인증서 만료(Expiration) 관리 부담 | 단말이 서버 인증서 검증 생략 시 MITM 위험| **공격자의 MAC 주소 복제 침투** |
| **주요 적용 대상** | 임직원 업무용 PC, 스마트폰, 보안 단말 | BYOD 단말, 범용 엔터프라이즈 계정 | **네트워크 프린터, IP 카메라, 레거시 IoT** |

#### 한줄 요약
- EAP-TLS는 최고 보안의 상호 인증서 방식, PEAP는 계정 기반 터널 방식, MAB는 IoT 예외 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CRL(인증서 폐기 목록) / OCSP**: 퇴사자 발생이나 단말 분실 시 해당 인증서의 유효성을 즉시 무효화하여 네트워크 접속을 거부하기 위한 실시간 인증서 상태 검증 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단말 설정 오류로 서버 인증서 검증을 생략(Bypass)하여 발생하는 **가짜 AP 중간자 공격(MITM)** | 단말 MDM 프로파일에 **사내 사설 루트 CA 인증서 강제 배포 및 서버 FQDN 검증 고정** | 가짜 AP/서버로의 위장 접속 및 크리덴셜 탈취 원천 차단 |
| 단말에 탑재된 기기 인증서 만료(Expired) 시 전사 수천 대 PC의 **동시 네트워크 접속 불가 장애** | **SCEP/EST 프로토콜 기반 인증서 자동 갱신(Auto-Enrollment) 및 만료 30일 전 경고** | 인증서 만료로 인한 서비스 중단 예방 및 100% 가용성 유지 |
| 802.1X 미지원 프린터/카메라의 MAB 허용 구간을 악용한 **해커의 MAC 위조 무단 침입** | **MAB 단말 전용 격리 VLAN(포트 80/443 차단) 할당 및 비정상 트래픽 프로파일링** | MAC 스푸핑을 통한 내부망 횡적 이동(Lateral Movement) 원천 차단 |

#### 한줄 요약
- MDM 루트 CA 강제로 MITM을 방어하고, SCEP 자동 갱신으로 만료를 방지하며, MAB 전용 격리로 MAC 위조를 차단한다.

## Ⅶ. 결론

- 엔터프라이즈 유무선 네트워크의 가장 강력한 1차 방어선 구축을 위해 **IEEE 802.1X 및 EAP 인증 프레임워크**는 제로 트러스트 접근 제어의 필수 기반 기술이며, 실무 구축 시 **EAP-TLS 기반 상호 인증서 체계 표준화**, **SCEP 기반 인증서 생애주기 자동화**, **MAB 기기에 대한 마이크로 세그멘테이션 격리**를 통합 구현하여 완결성 높은 고신뢰 네트워크 인프라를 완성

#### 한줄 요약
- IEEE 802.1X와 EAP-TLS 상호 인증 및 RADIUS 동적 정책 할당을 결합하여 고신뢰 포트 보안을 실현한다.
