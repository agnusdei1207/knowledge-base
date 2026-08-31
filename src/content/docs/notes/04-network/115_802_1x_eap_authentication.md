---
sidebar:
  order: 115
  label: "115. 802.1X EAP 인증"
  badge:
    text: "기출 · 50%"
    variant: note
title: "포트 기반 네트워크 접근 제어 표준 : IEEE 802.1X 및 EAP"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: **EAPOL·RADIUS**로 포트를 제어하는 인증 표준
- 배경/필요성: 유무선 로컬 네트워크(LAN/WLAN) 환경에서 물리적 포트에 케이블을 꽂거나 무선 SSID에 접속하는 것만으로 모든 내부망 트래픽 접근이 허용되는 레거시 구조는 비인가 단말의 무단 침입, MAC 주소 위조 및 중간자 공격(MITM)에 취약한 한계를 드러냄에 따라, 스위치/AP의 물리 및 논리 포트를 인증 전까지 차단 상태(Uncontrolled Port)로 유지하고 단말(Supplicant)-인증자(Authenticator)-인증서버(RADIUS) 3자 간의 확장 인증 프로토콜(EAP) 핸드셰이크를 통해 자격을 검증한 후에만 포트를 개방(Controlled Port)하는 IEEE 802.1X 표준을 도입하여 **L2 포트 레벨의 강력한 물리적 네트워크 접근 통제, X.509 인증서 기반 상호 인증(EAP-TLS)을 통한 계정 탈취 원천 방어 및 신원 기반 동적 VLAN/dACL 권한 할당**을 달성할 필요

#### 한줄 요약
- 단말-스위치-인증서버 3자 모델과 EAP 상호 인증을 통해 포트 레벨의 강력한 접근 통제를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Controlled vs Uncontrolled Port**: 스위치 포트 내에서 인증 전에는 오직 EAPOL 패킷만 수신(비제어 포트)하고 인증 성공 후에만 일반 IP 데이터를 통과(제어 포트)시키는 논리적 분리 구조.
- **EAP-TLS (RFC 5216)**: 단말과 RADIUS 서버가 상호 X.509 인증서를 교환하여 비밀번호 탈취 위험을 원천 차단하는 가장 안전한 EAP 방식.

</details>

- 인증 전 **비제어 포트**로 EAPOL만 허용
- **EAP-TLS·PEAP·EAP-TTLS** 인증 방식 지원
- RADIUS 응답으로 **동적 VLAN·dACL** 할당

#### 한줄 요약
- 포트 레벨 차단, 다형 EAP 지원, 동적 VLAN/dACL 권한 할당을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EAPOL (EAP over LAN)**: IEEE 802.3 유선 이더넷 또는 802.11 무선 LAN 상에서 단말과 스위치 간 EAP 메시지를 전송하는 L2 프레임.

</details>

```text
IEEE 802.1X
|-- Supplicant
|-- Authenticator
|   |-- Uncontrolled Port
|   `-- Controlled Port
|-- Authentication Server
|-- Identity Store
`-- Port Policy
```

선의 의미: 단말이 EAPOL로 보낸 인증 요청이 스위치에서 RADIUS 패킷으로 변환되어 인증 서버로 전달되고 인증 성공 시 포트가 개방되는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Supplicant** | 자격 증명 또는 인증서 제시 |
| **Authenticator** | EAPOL과 RADIUS 중계 |
| **Uncontrolled Port** | 인증 전 EAPOL 전달 |
| **Controlled Port** | 인증 후 데이터 전달 |
| **Authentication Server** | EAP 검증과 접근 인가 |
| **Identity Store** | PKI·AD·LDAP 정보 제공 |
| **Port Policy** | VLAN·dACL 적용 |

#### 한줄 요약
- 스위치는 자격을 판단하지 않고 EAP 메시지를 중계만 하므로, 인증 정책과 계정 정보가 장비마다 흩어지지 않고 RADIUS 서버 한 곳에 모인다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MSK (Master Session Key)**: EAP-TLS 인증 성공 시 단말과 인증 서버가 공유하는 64바이트 암호 키로 무선 WPA3 통신의 PMK로 사용됨.

</details>

```text
802.1X EAPOL 시작, EAP-TLS 상호 검증 및 포트 개방 파이프라인
        │
        [EAPOL-Start 송출]
        │
   1. [Identity 질의 및 응답]
        │
   2. [RADIUS 캡슐화 중계]
        │
   3. [EAP-TLS 상호 인증]
        │
   ▼
   4. [Access-Accept 및 포트 개방]
```

- 1. Identity 질의 및 응답
- 2. RADIUS 캡슐화 중계
- 3. EAP-TLS 상호 인증
- 4. Access-Accept 및 포트 개방

#### 한줄 요약
- RADIUS 응답에서 포트 개방과 차단이 갈리며, 인증서를 다룰 수 없는 IoT는 MAB 예외를 허용하는 대가로 MAC 위조 위험을 떠안는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **EAP-TLS** vs **PEAP/EAP-TTLS** vs **MAB (MAC Authentication Bypass)**.

</details>

| 비교 항목 | EAP-TLS (RFC 5216) | PEAP / EAP-TTLS | MAC 인증 우회 (MAB) |
|:---|:---|:---|:---|
| 인증 방식 | **상호 인증서** | 서버 인증서와 ID/PW | MAC 주소 대조 |
| 주요 위험 | 인증서 수명 관리 | 서버 검증 누락 시 MITM | **MAC 스푸핑** |
| 단말 인증서 | 필수 | 불필요 | 불필요 |
| 주요 대상 | 관리 단말 | 계정 기반 단말 | 802.1X 미지원 기기 |

#### 한줄 요약
- EAP-TLS는 최고 보안의 상호 인증서 방식, PEAP는 계정 기반 터널 방식, MAB는 IoT 예외 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SCEP (Simple Certificate Enrollment Protocol, RFC 8894)**: 엔드포인트 단말이 사내 PKI 서버로부터 X.509 기기 인증서를 무선으로 자동 발급 및 갱신받는 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 서버 검증 누락으로 **Evil Twin MITM** | 루트 CA 배포와 **서버 FQDN 고정** | 위장 서버 위험 완화 |
| 인증서 만료로 접속 장애 | **SCEP·EST 자동 갱신** | 만료 중단 예방 |
| MAB 구간의 **MAC 위조** | 격리 VLAN과 **행위 프로파일링** | 횡적 이동 제한 |
| RADIUS 장애로 포트 차단 | **Critical VLAN·Fail-Open** | 연속성과 보안 위험 균형 |

#### 한줄 요약
- MDM 루트 CA 강제로 MITM을 방어하고, SCEP 자동 갱신으로 만료를 방지하며, MAB 전용 격리로 MAC 위조를 차단한다.

## Ⅶ. 결론

- 유무선 네트워크의 가장 기초적인 L2 포트 레벨에서 비인가 접근을 원천 차단하고 엔터프라이즈 신원 기반 접근 제어를 구현하는 **국제 표준 포트 기반 네트워크 보안 통제 기술(IEEE 802.1X 및 IETF RFC 3748/5216 EAP)**로 확고히 안착하였으며, 제로 트러스트 NAC 및 클라우드 IdP 연동과의 결합으로 진화하는 가운데, 실무 802.1X 인프라 구축 시에는 **피싱 및 Evil Twin 공격을 원천 차단하는 X.509 단말/서버 상호 인증서 기반 EAP-TLS 표준화, 인증서 만료로 인한 접속 마비를 방지하는 SCEP/EST 무선 자동 발급·갱신 체계 구축, 인증서 미지원 레거시 IoT 단말을 위한 MAB(MAC Authentication Bypass) 최소화 및 격리 VLAN/프로파일링 정책 연계**를 결합하여 완벽한 포트 보안 신뢰성을 완성

#### 한줄 요약
- IEEE 802.1X와 EAP-TLS 상호 인증 및 RADIUS 동적 정책 할당을 결합하여 고신뢰 포트 보안을 실현한다.
