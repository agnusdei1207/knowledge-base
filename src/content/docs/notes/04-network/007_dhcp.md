---
sidebar:
  order: 7
  label: "007. DHCP"
  badge:
    text: "미출 · 30%"
    variant: note
title: "DHCP (Dynamic Host Configuration Protocol)"
date: "2026-08-31T10:48:00+09:00"
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
- 배경/필요성: 수백~수만 대의 단말이 접속하는 엔터프라이즈 및 공공 네트워크에서 관리자의 수작업 고정 IP 설정으로 인한 막대한 관리 공수, 휴먼에러 기반의 IP 중복 충돌, 이동 단말(노트북, 스마트폰)의 서브넷 변경 시 통신 두절 및 퇴청 후 미사용 유휴 IP의 장기 점유 문제를 해결하기 위해, UDP 67/68 포트 기반의 DORA(Discover-Offer-Request-ACK) 4단계 핸드셰이크와 임대 기간(Lease Time) 메커니즘을 통해 IP 주소, 서브넷 마스크, 게이트웨이 및 DNS 정보를 동적으로 중앙 배포·회수하는 DHCP 프로토콜을 도입하여 **네트워크 접속 구성의 완전 자동화와 한정된 IP 자원의 회수 효율 극대화**를 달성할 필요

#### 한줄 요약
- DHCP는 주소 관리 권한을 단말에서 서버 한 곳으로 모아 설정 공수를 없애는 대신 그 서버를 단일 장애점으로 만들므로, 임대 기간과 서버 이중화 설계가 가용성의 핵심 변수가 된다.

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
[DHCP 구성]
|-- DHCP 클라이언트
|-- DHCP 릴레이 에이전트
`-- DHCP 서버
    |-- 주소 풀
    |-- 바인딩 테이블
    `-- DHCP 옵션
```

선의 의미: 계층 및 클라이언트가 브로드캐스트로 탐색하면 릴레이 에이전트가 중계하고 중앙 서버가 바인딩 테이블을 참조하여 IP를 임대하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **DHCP 클라이언트** | 주소 획득과 임대 갱신 요청 |
| **DHCP 릴레이 에이전트** | 서브넷 사이 DHCP 메시지 중계 |
| **DHCP 서버** | 주소 풀·임대·옵션 관리 |
| **바인딩 테이블** | 클라이언트·주소·만료 시각 매핑 |
| **DHCP 옵션** | 게이트웨이·DNS 등 설정 전달 |

#### 한줄 요약
- 릴레이 에이전트가 브로드캐스트가 넘지 못하는 서브넷 경계에 끼어들어 서브넷마다 DHCP 서버를 두는 비용을 없애고, 바인딩 테이블이 관리자의 수작업 주소 대장을 대신한다.

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

- 1. DHCP Discover: 클라이언트의 **서버 탐색**
- 2. DHCP Offer: 서버의 주소와 옵션 제안
- 3. DHCP Request: 클라이언트의 제안 선택 요청
- 4. DHCP ACK: 서버의 임대 확정과 바인딩 등록
- 5. DHCP Request/ACK: T1 시점 **임대 갱신**

#### 한줄 요약
- Discover → Offer → Request → ACK 4단계를 거쳐 IP를 할당받고, T1(50%) 시점에 유니캐스트로 임대를 연장한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DHCP 주소 할당 3대 방식**: 동적 할당(Dynamic Lease), 정적 바인딩(Static Reservation), 자동 할당(Automatic Permanent).

</details>

| 비교 항목 | 동적 할당 (Dynamic Allocation) | 정적 예약 (Static Reservation) | 자동 할당 (Automatic Allocation) |
|:---|:---|:---|:---|
| 할당 방식 | 임대 시간 기반 일시 할당 | MAC 기반 주소 예약 | 최초 주소의 영구 할당 |
| 적용 대상 | **유동 단말** | **서버·프린터** | 고정 단말 |
| 주소 효율 | 유휴 주소 자동 회수 | 예약 주소 상시 점유 | 할당 주소 지속 점유 |
| 관리 부담 | 정책·풀 운영 | 예약 정보 등록 | 고갈 시 수동 회수 |

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

- 캠퍼스망, 무선 Wi-Fi 환경 및 클라우드 VPC 가상 머신 프로비저닝에 이르기까지 호스트 네트워크 설정의 필수 자동화 인프라로 자리잡았으며, 실무 구축 시에는 **Rogue DHCP 기반 MITM 공격을 방어하는 L2 스위치 DHCP Snooping(Trusted/Untrusted Port 분리), 대량 위조 MAC 기반 DoS를 차단하는 DHCP Rate Limiting, 라우터를 넘는 중앙 집중 관리를 위한 DHCP Relay Agent(ip helper-address) 구성 및 액티브-스탠바이 이중화 클러스터링**을 결합하여 무중단 고가용성 IP 배포 환경을 완성

#### 한줄 요약
- DHCP는 DORA 핸드셰이크를 통해 네트워크 설정을 자동화하며, DHCP Snooping과 릴레이 에이전트를 결합하여 안전하고 확장성 있는 주소 관리를 제공하는 핵심 네트워크 기술이다.
