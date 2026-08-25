---
sidebar:
  order: 7
  label: "007. DHCP"
  badge:
    text: "미출 · 30%"
    variant: note
title: "DHCP (Dynamic Host Configuration Protocol)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 7
extra:
  question_no: "7"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "DORA 4단계 절차와 릴레이 에이전트 및 스누핑 보안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DHCP (Dynamic Host Configuration Protocol)**: 단말 부팅 시 IP 주소, 서브넷 마스크, 게이트웨이, DNS 등 TCP/IP 설정 매개변수를 자동 임대(Lease)해 주는 프로토콜 (UDP 67/68).
- **DORA Process**: Discover, Offer, Request, ACK의 4단계 메시지 교환을 통해 IP 주소를 획득하는 표준 핸드셰이크 절차.

</details>

- 정의/개념: 네트워크에 접속하는 클라이언트에 **IP 주소, 게이트웨이, DNS 설정을 DORA 4단계 절차로 자동 임대·회수하는 구성 프로토콜**
- 배경/필요성: 수동 고정 IP 설정 시 발생하는 **관리 공수 폭증, IP 중복 충돌, 잦은 이동에 따른 재설정 지연 및 유휴 주소 회수 불가**

#### 한줄 요약
- DORA 4단계를 통해 IP와 네트워크 파라미터를 자동 임대하고 T1/T2 타이머로 생명주기를 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DHCP Relay Agent (릴레이 에이전트)**: 라우터를 통과하지 못하는 클라이언트의 브로드캐스트 패킷을 유니캐스트로 변환하여 원격 중앙 DHCP 서버로 전달하는 기능 (RFC 3046 Option 82).
- **Lease Time & T1/T2 Timer**: 주소 임대 기간의 50%(T1, Renewal)에 유니캐스트 연장 요청을, 87.5%(T2, Rebinding)에 브로드캐스트 재바인딩을 시도.

</details>

- UDP 기반(서버 포트 67, 클라이언트 포트 68)의 **DORA 4단계 신속 초기화**
- 임대 기간(Lease Time) 및 T1(50%)/T2(87.5%) 타이머 기반의 **동적 IP 자동 회수**
- 라우터를 넘어 중앙 서버에서 다중 서브넷을 통합 관리하는 **DHCP 릴레이 에이전트 지원**

#### 한줄 요약
- DORA 4단계 절차, T1/T2 임대 갱신, 릴레이 에이전트 연동을 통해 주소 관리 자동화를 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DHCP Option**: 서브넷 마스크(Option 1), 라우터/게이트웨이(Option 3), DNS 서버(Option 6), 릴레이 정보(Option 82) 등 필수 네트워크 매개변수를 전달하는 가변 필드.

</details>

```text
[DHCP 프로토콜 분산 환경 구성 및 DORA 절차 아키텍처]
|-- 1. DHCP Client (단말 노드: UDP 68번 포트 수신, IP 자동 획득 및 갱신)
|-- 2. DHCP Relay Agent (L3 라우터/스위치: L2 Broadcast 패킷 -> L3 Unicast 변환 중계)
`-- 3. Central DHCP Server (UDP 67번 포트 수신)
    |-- IP Address Pool Management (가용 IP 풀 및 서브넷 범위 관리)
    |-- Binding Table Database (MAC 주소 <-> 할당 IP <-> 임대 만료시간 매핑)
    `-- DHCP Options Engine (Subnet Mask, Default Gateway, DNS, NTP 파라미터 주입)
```

선의 의미: 계층 및 클라이언트가 브로드캐스트로 탐색하면 릴레이 에이전트가 중계하고 중앙 서버가 바인딩 테이블을 참조하여 IP를 임대하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **DHCP 서버** | IP 주소 풀 관리, **바인딩 테이블 기록, 임대 기간 통제 및 DHCP 옵션 파라미터 배포** | UDP 67번 수신 |
| **DHCP 클라이언트** | 부팅 시 DORA 절차를 수행하여 **IP를 동적 획득하고 T1/T2 타이머에 따라 갱신 요청** | UDP 68번 수신 |
| **DHCP 릴레이 에이전트** | L2 브로드캐스트(Discover/Request)를 **유니캐스트로 변환하여 원격 중앙 서버로 중계** | RFC 3046 (Option 82) |
| **바인딩 테이블** | 클라이언트의 **MAC 주소, 할당된 IP, 임대 시작/만료 시간을 1:1 매핑하여 영속 관리** | IP 중복 방지 |
| **DHCP 옵션 (Options)**| 서브넷 마스크(Opt 1), **게이트웨이(Opt 3), DNS(Opt 6) 등 필수 네트워크 매개변수 전달** | 가변 확장 필드 |

#### 한줄 요약
- DHCP 서버, 클라이언트, 릴레이 에이전트, 바인딩 테이블, DHCP 옵션이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DORA 4단계**: 1. Discover (클라이언트 탐색) $\to$ 2. Offer (서버 제안) $\to$ 3. Request (클라이언트 선택 요청) $\to$ 4. ACK (서버 최종 승인).

</details>

```text
클라이언트 부팅 및 IP 획득 (DORA) / 갱신 흐름
        │
   1. [DHCP Discover] 클라이언트가 `0.0.0.0` -> `255.255.255.255` 브로드캐스트로 서버 탐색
        │
   2. [DHCP Offer] DHCP 서버가 가용 IP(`192.168.1.10`), 게이트웨이, DNS 옵션을 담아 제안
        │
   3. [DHCP Request] 클라이언트가 특정 서버의 제안을 선택하여 브로드캐스트로 공식 사용 요청
        │
   4. [DHCP ACK] 서버가 바인딩 테이블에 등록하고 최종 승인(ACK) 전송 (IP 임대 완료)
        │
   ▼ (임대 기간 50% T1 타이머 도달 시점)
5. [DHCP Request / ACK (유니캐스트)] 기존 서버에 직접 갱신 요청을 보내 무중단 임대 연장
```

#### 한줄 요약
- Discover → Offer → Request → ACK 4단계를 거쳐 IP를 할당받고, T1(50%) 시점에 유니캐스트로 임대를 연장한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DHCP 주소 할당 3대 방식**: 동적 할당(Dynamic Lease), 정적 바인딩(Static Reservation), 자동 할당(Automatic Permanent).

</details>

| 비교 항목 | 동적 할당 (Dynamic Allocation) | 정적 예약 (Static Reservation) | 자동 할당 (Automatic Allocation) |
|:---|:---|:---|:---|
| **핵심 할당 메커니즘**| **임대 시간(Lease Time) 기반 일시 대여 및 만료 회수**| **단말 MAC 주소 기반 영구 고정 IP 사전 매핑** | **최초 접속 시 가용 IP를 영구적으로 자동 부여** |
| **주요 적용 대상** | **일반 사용자 PC, 스마트폰, 게스트 Wi-Fi** | **서버, 네트워크 프린터, 스위치/라우터 관리 IP**| 변경 필요성이 없는 고정 사무용 PC |
| **IP 자원 효율성** | **최고 (유휴 주소 자동 회수로 IPv4 절약)** | 보통 (주소 고정 점유로 미사용 시 낭비) | 낮음 (한번 할당된 IP는 영구 고정되어 고갈 위험)|
| **관리 오버헤드** | 전무 (완전 자동화) | 최초 1회 수동 MAC 등록 필요 | 전무 (단, IP 고갈 시 수동 회수 필요) |

#### 한줄 요약
- 유동 단말은 동적 할당, 서버/프린터는 정적 예약, 고정 단말은 자동 할당을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DHCP Snooping**: L2 스위치에서 인가된 포트(Trusted Port)에서만 DHCP Offer/ACK 응답을 허용하여 가짜 DHCP 서버(Rogue DHCP)를 차단하는 보안 기능.
- **DHCP Starvation (고갈 공격)**: 공격자가 위조된 MAC 주소로 수만 건의 Discover 패킷을 난사하여 서버의 모든 IP 풀을 고갈시키는 DoS 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비인가 가짜 DHCP(Rogue DHCP) 서버로 인한 트래픽 가로채기(MITM) | **스위치 `DHCP Snooping` 활성화 및 정식 업링크만 `Trusted Port` 지정** | 비인가 Offer/ACK 패킷 100% 차단 |
| 대량의 위조 MAC으로 주소 풀을 고갈시키는 DHCP Starvation 공격 | **스위치 포트별 `DHCP Rate Limiting` 및 `Port Security(Sticky MAC)` 적용** | IP 풀 고갈 방어 및 DoS 차단 |
| L3 라우터로 분리된 원격 다중 서브넷 단말의 IP 획득 불가 | **라우터 인터페이스에 `DHCP Relay Agent (ip helper-address)` 설정** | 서브넷별 서버 구축 비용 절감 및 중앙 관리 |
| DHCP 서버 장애 시 전사 단말의 신규 IP 할당 전면 중단 | **2대의 DHCP 서버를 80:20 또는 50:50 분할 운영하는 `DHCP Failover 클러스터`** | 주소 할당 고가용성(HA) 확보 |

#### 한줄 요약
- DHCP Snooping, Rate Limiting, 릴레이 에이전트, 이중화 클러스터로 운영한다.

## Ⅶ. 결론

- 대규모 엔터프라이즈 네트워크의 IP 관리 효율성과 가용성을 확보하기 위해 **중앙 집중형 DHCP 서버 클러스터와 서브넷별 Relay Agent를 표준 배포**하고, **L2 스위치 수준의 DHCP Snooping, Dynamic ARP Inspection(DAI) 및 IP 소스 가드(IPSG)**를 결합하여 비인가 서버와 스푸핑 공격을 차단하는 통합 L2/L3 주소 거버넌스 완성

#### 한줄 요약
- DHCP는 DORA 핸드셰이크를 통해 네트워크 설정을 자동화하며, DHCP Snooping과 릴레이 에이전트를 결합하여 안전하고 확장성 있는 주소 관리를 제공하는 핵심 네트워크 기술이다.