---
sidebar:
  order: 115
  label: "115. 802.1X EAP 인증"
  badge:
    text: "기출 · 50%"
    variant: note
title: "포트 기반 네트워크 접근 제어 표준 : IEEE 802.1X 및 EAP"
date: "2026-08-25T12:00:00+09:00"
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

- **IEEE 802.1X**: 유무선 스위치/AP 포트에서 인증되지 않은 트래픽을 차단하고 인증 완료 후 포트를 개방하는 포트 기반 접근 제어 표준.
- **EAP (Extensible Authentication Protocol, RFC 3748)**: ID/PW, 인증서 등 다양한 인증 메커니즘을 캡슐화하여 운반하는 확장 인증 프레임워크.

</details>

- 정의/개념: 단말(Supplicant), 스위치(Authenticator), 인증 서버(RADIUS) 3자 구조로 **EAPOL과 RADIUS를 통해 신원을 검증하고 포트를 동적 개방하는 표준 기술**
- 배경/필요성: 물리 포트에 케이블만 연결하면 누구나 내부망에 접근 가능한 **L2 포트 무방비 노출, MAC 도용 스푸핑 및 비인가 단말 침입 방어 불가**

#### 한줄 요약
- 단말-스위치-인증서버 3자 모델과 EAP 상호 인증을 통해 포트 레벨의 강력한 접근 통제를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Controlled vs Uncontrolled Port**: 스위치 포트 내에서 인증 전에는 오직 EAPOL 패킷만 수신(비제어 포트)하고 인증 성공 후에만 일반 IP 데이터를 통과(제어 포트)시키는 논리적 분리 구조.
- **EAP-TLS (RFC 5216)**: 단말과 RADIUS 서버가 상호 X.509 인증서를 교환하여 비밀번호 탈취 위험을 원천 차단하는 가장 안전한 EAP 방식.

</details>

- **하드웨어 포트 레벨 차단(Port Blocking)**: 인증 완료 전까지 **ARP/IP 트래픽을 원천 드롭하고 오직 EAPOL 프레임만 허용**
- **다양한 EAP 인증 방식 지원**: 최고 보안 수준의 **상호 인증서(EAP-TLS)부터 계정 기반 터널(PEAP/EAP-TTLS)까지 유연 수용**
- **동적 네트워크 권한 매핑(Dynamic VLAN & dACL)**: RADIUS 서버 응답에 따라 **스위치 포트에 사용자 역할별 VLAN 태그 자동 주입**

#### 한줄 요약
- 포트 레벨 차단, 다형 EAP 지원, 동적 VLAN/dACL 권한 할당을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EAPOL (EAP over LAN)**: IEEE 802.3 유선 이더넷 또는 802.11 무선 LAN 상에서 단말과 스위치 간 EAP 메시지를 전송하는 L2 프레임.

</details>

```text
[IEEE 802.1X 3대 구성요소 및 프로토콜 흐름]
|-- Supplicant (인증 요청자: 유무선 단말 OS 내장 802.1X 클라이언트)
`-- Authenticator (인증 중계자: L2 스위치 / 무선 AP)
    |-- Uncontrolled Port (인증 전: 오직 EAPOL 패킷만 통과 허용)
    |-- Controlled Port (인증 후: 일반 업무 데이터 트래픽 통과 개방)
    `-- EAPOL-to-RADIUS Converter (L2 EAPOL -> L3 RADIUS UDP 1812 패킷 변환 중계)
`-- Authentication Server (RADIUS Server / Cisco ISE)
    |-- EAP-TLS / PEAP 인증서 검증 및 Active Directory 계정 DB 질의
    `-- Access-Accept (MSK 마스터 세션 키 유도 및 동적 VLAN/dACL 반환)
```

선의 의미: 단말이 EAPOL로 보낸 인증 요청이 스위치에서 RADIUS 패킷으로 변환되어 인증 서버로 전달되고 인증 성공 시 포트가 개방되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **인증 요청자 (Supplicant)**| 단말 OS 내장 802.1X 클라이언트로 **사용자 자격 증명 또는 인증서 제시** | Windows 802.1X |
| **인증 중계자 (Authenticator)**| 스위치/AP로 **EAPOL 프레임을 수신하여 RADIUS 패킷으로 재포장 중계** | L2 Switch / WLC |
| **인증 서버 (RADIUS Server)**| EAP 인증 최종 수행, **AD 계정 확인 및 동적 접근 권한(VLAN) 인가** | FreeRADIUS / ISE |
| **신원/인증서 저장소** | 기업 내부 **사설 PKI(Root CA/CRL) 및 직원 디렉터리(AD/LDAP) 계정 DB** | Directory / PKI |
| **동적 포트 제어기** | 인증 성공 전 비인가 격리, **성공 후 802.1Q VLAN 태그 및 dACL 주입** | 802.1Q / dACL |

#### 한줄 요약
- 서플리컨트, 인증 중계자(스위치/AP), 인증 서버(RADIUS), 신원/PKI 저장소, 동적 포트 제어기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MSK (Master Session Key)**: EAP-TLS 인증 성공 시 단말과 인증 서버가 공유하는 64바이트 암호 키로 무선 WPA3 통신의 PMK로 사용됨.

</details>

```text
802.1X EAPOL 시작, EAP-TLS 상호 검증 및 포트 개방 파이프라인
        │
   1. [EAPOL-Start 송출] 단말이 스위치 포트에 연결 후 L2 멀티캐스트로 'EAPOL-Start' 전송
        │
   2. [Identity 질의 및 응답] 스위치가 'EAP-Request/Identity' 전송 ➔ 단말이 사용자 ID 회신
        │
   3. [RADIUS 캡슐화 중계] 스위치가 EAP 응답을 RADIUS Access-Request로 변환하여 서버에 전달
        │
   4. [EAP-TLS 상호 인증] RADIUS 서버와 단말 간에 인증서 교환 및 상호 전자서명 암호학적 검증
        │
   ▼
5. [Access-Accept 및 포트 개방] 서버가 동적 VLAN과 MSK를 회신 ➔ 스위치 통제 포트 완전 개방
```

#### 한줄 요약
- EAPOL-Start → Identity 질의/응답 → EAP-TLS 상호 검증 → RADIUS Access-Accept 반환 → 포트 개방 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **EAP-TLS** vs **PEAP/EAP-TTLS** vs **MAB (MAC Authentication Bypass)**.

</details>

| 비교 항목 | EAP-TLS (RFC 5216) | PEAP / EAP-TTLS | MAC 인증 우회 (MAB) |
|:---|:---|:---|:---|
| **인증 메커니즘** | **단말 & 서버 상호 인증서 검증** | **서버 인증서로 TLS 터널 수립 후 ID/PW**| **단말의 L2 MAC 주소만 RADIUS 대조** |
| **보안 강도** | **최고 (비밀번호 탈취/피싱 원천 차단)**| 높음 (서버 인증서 검증 필수) | **낮음 (MAC 스푸핑 위조 취약)** |
| **단말 인증서 요구**| **필수 (사내 PKI 인증서 사전 배포)** | **불필요 (사용자 계정/패스워드만 사용)** | 불필요 (802.1X 미지원 IoT 전용) |
| **주요 위협 요인** | 인증서 만료(Expiration) 관리 부담 | 단말이 서버 인증서 검증 생략 시 MITM 위험| **공격자의 MAC 주소 복제 침투** |
| **주요 적용 대상** | **임직원 업무용 PC, 스마트폰, 보안 단말**| **BYOD 단말, 범용 엔터프라이즈 계정** | **네트워크 프린터, IP 카메라, 레거시 IoT**|

#### 한줄 요약
- EAP-TLS는 최고 보안의 상호 인증서 방식, PEAP는 계정 기반 터널 방식, MAB는 IoT 예외 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SCEP (Simple Certificate Enrollment Protocol, RFC 8894)**: 엔드포인트 단말이 사내 PKI 서버로부터 X.509 기기 인증서를 무선으로 자동 발급 및 갱신받는 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단말이 서버 인증서 검증을 생략(Bypass)하여 발생하는 **가짜 AP 중간자 공격(MITM)** | 단말 MDM 프로파일에 **`사내 루트 CA 인증서 강제 배포 및 서버 FQDN 검증 고정`** | 가짜 AP/서버 위장 접속 및 크리덴셜 탈취 원천 차단 |
| 기기 인증서 만료(Expired) 시 전사 수천 대 PC의 **동시 네트워크 접속 불가 장애** | **`SCEP / EST 프로토콜 기반 인증서 자동 갱신` 및 만료 30일 전 경고** | 인증서 만료로 인한 서비스 중단 예방 및 가용성 유지 |
| 802.1X 미지원 IoT 기기의 MAB 허용 구간을 악용한 **MAC 위조 무단 침입** | **`MAB 전용 격리 VLAN(외부 차단)` 할당 및 비정상 트래픽 프로파일링** | MAC 스푸핑을 통한 내부망 횡적 이동 원천 차단 |
| 스위치와 RADIUS 서버 간 통신 두절 시 전사 포트 차단 장애 | **`Critical VLAN (Fail-Open) 구성`으로 인증 서버 다운 시 제한적 업무망 허용** | 인증 인프라 장애 시에도 비즈니스 연속성 보장 |

#### 한줄 요약
- MDM 루트 CA 강제로 MITM을 방어하고, SCEP 자동 갱신으로 만료를 방지하며, MAB 전용 격리로 MAC 위조를 차단한다.

## Ⅶ. 결론

- 엔터프라이즈 유무선 네트워크의 가장 강력한 1차 방어선 구축을 위해 **IEEE 802.1X 및 EAP 인증 프레임워크는 제로 트러스트 접근 제어의 필수 기반 기술**이며, 실무 구축 시 **EAP-TLS 기반 상호 인증서 체계 표준화, SCEP 기반 인증서 생애주기 자동화, MAB 기기에 대한 마이크로 세그멘테이션 격리**를 통합 구현하여 완결성 높은 고신뢰 네트워크 인프라 완성

#### 한줄 요약
- IEEE 802.1X와 EAP-TLS 상호 인증 및 RADIUS 동적 정책 할당을 결합하여 고신뢰 포트 보안을 실현한다.