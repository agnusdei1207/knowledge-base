---
sidebar:
  order: 7
  label: "007. DHCP (Dynamic Host Configuration Protocol)"
  badge:
    text: "미출 · 30%"
    variant: note
title: "DHCP (Dynamic Host Configuration Protocol)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 7
extra:
  question_no: "007"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "DORA 4단계 절차와 릴레이 에이전트 및 스누핑 보안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **동적 호스트 구성 프로토콜(Dynamic Host Configuration Protocol, DHCP)**: 네트워크에 접속하는 클라이언트 장치에 IP 주소, 서브넷 마스크, 기본 게이트웨이, DNS 서버 정보 등의 TCP/IP 설정 매개변수를 자동으로 동적 임대(Lease)해 주는 응용 계층 프로토콜(UDP 67/68).
- **IP 주소 임대(IP Address Lease)**: DHCP 서버가 클라이언트에 특정 기간 동안 IP 주소의 독점적 사용 권한을 부여하고 만료 시 회수하는 자원 관리 방식.

</details>

- 정의/개념: 단말 부팅 시 **DORA(Discover-Offer-Request-ACK)** 4단계 절차를 통해 IP 주소 및 네트워크 구성 정보를 동적으로 자동 할당하는 프로토콜
- 배경/필요성: 대규모 네트워크 환경에서 호스트별 수동 IP 설정의 관리 오버헤드, IP 주소 중복 충돌 및 유휴 IP 자원 낭비 문제 해소 요구

#### 한줄 요약
- 단말 접속 시 IP 주소와 네트워크 파라미터를 자동으로 임대하고 관리하는 동적 구성 프로토콜이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **주소 풀(Address Pool)**: DHCP 서버가 클라이언트에게 동적으로 할당하기 위해 관리하는 연속된 가용 IP 주소 범위.
- **바인딩(Binding)**: DHCP 서버가 특정 클라이언트의 MAC 주소와 할당된 IP 주소 및 임대 만료 시간을 매핑하여 유지하는 상태 테이블.
- **DHCP 릴레이 에이전트(DHCP Relay Agent)**: 라우터를 통과하지 못하는 클라이언트의 L2 브로드캐스트 패킷을 유니캐스트로 캡슐화하여 타 서브넷의 중앙 DHCP 서버로 중계하는 기능(RFC 3046).

</details>

- **주소 풀** 과 **바인딩 테이블** 관리를 통한 한정된 IPv4 주소의 효율적 재사용 및 중복 할당 원천 방지
- UDP 기반(서버 67번, 클라이언트 68번)의 4단계 셰이크핸드(DORA)를 통한 신속한 초기화 지원
- **DHCP 릴레이 에이전트** 지원을 통해 단일 중앙 DHCP 서버로 다중 서브넷 통합 관리 가능

#### 한줄 요약
- 주소 풀 관리를 통해 동적 임대 및 회수를 자동화하고 릴레이 에이전트로 다중 서브넷을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DHCP 옵션(DHCP Options)**: IP 주소 외에 서브넷 마스크(Option 1), 라우터/게이트웨이(Option 3), 도메인 네임 서버(Option 6) 등 추가 네트워크 매개변수를 전달하는 가변 길이 필드.

</details>

```text
[ DHCP 클라이언트 (UDP 68) ]                          [ DHCP 서버 (UDP 67) ]
            │                                                │
            ├─ 1. DHCP Discover (L2/L3 Broadcast) ─────────▶ │
            │                                                │
            │ ◀── 2. DHCP Offer (Unicast / Broadcast) ───────┤
            │                                                │
            ├─ 3. DHCP Request (Broadcast) ────────────────▶ │
            │                                                │
            │ ◀── 4. DHCP ACK (Unicast / Broadcast) ─────────┤
```

선의 의미: 클라이언트의 탐색부터 서버의 제안, 클라이언트의 확정 요청 및 서버의 최종 승인으로 이어지는 DORA 절차

| 구성요소 | 책임 | 전송 계층 포트 |
|:---|:---|:---|
| **DHCP 서버** | 주소 풀 관리, IP 임대 및 갱신 처리, DHCP 옵션 파라미터 제공 | UDP 67번 수신 |
| **DHCP 클라이언트** | 부팅 시 DORA 절차를 수행하여 IP를 획득하고 T1/T2 타이머 기반 갱신 요청 | UDP 68번 수신 |
| **DHCP 릴레이 에이전트** | 브로드캐스트 Discover/Request 패킷을 유니캐스트로 변환하여 원격 서버로 중계 | 라우터/L3 스위치 기능 |
| **DHCP 옵션 필드** | 서브넷 마스크, 기본 게이트웨이, DNS, 도메인 네임 등 필수 부가 파라미터 전달 | 메시지 확장 필드 |

#### 한줄 요약
- 서버(UDP 67)와 클라이언트(UDP 68)가 DORA 메시지 교환을 통해 IP 및 옵션 정보를 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **임대 갱신 타이머(T1/T2 Timer)**: 임대 기간의 50%(T1, Renewal) 시점에 기존 서버로 단일 유니캐스트 갱신을 요청하고, 87.5%(T2, Rebinding) 시점에 전체 브로드캐스트 재바인딩을 시도하는 타이머.

</details>

```text
1. DHCP Discover: 클라이언트가 브로드캐스트로 가용 DHCP 서버 탐색
            │
            ▼
2. DHCP Offer: DHCP 서버가 가용 IP 주소 및 옵션(게이트웨이, DNS)을 제안
            │
            ▼
3. DHCP Request: 클라이언트가 제안받은 특정 서버의 IP 사용을 브로드캐스트로 공식 요청
            │
            ▼
4. DHCP ACK: 선택된 서버가 바인딩 테이블에 등록하고 최종 임대 승인 완료
            │
            ▼
5. 임대 갱신(T1: 50% 시점): 클라이언트가 해당 서버에 유니캐스트로 Request 전송하여 임대 기간 연장
```

**동작 원리**

1. **Discover (탐색)**: IP가 없는 클라이언트가 `0.0.0.0` 출발지로 브로드캐스트(`255.255.255.255`) 패킷 전송
2. **Offer (제안)**: Discover를 수신한 서버들이 가용 IP 풀에서 선점한 주소와 임대 기간, 게이트웨이 정보를 담아 응답
3. **Request (요청)**: 클라이언트가 수신된 제안 중 하나를 선택하고, 타 서버들에 제안 회수를 알리기 위해 브로드캐스트로 요청 전송
4. **ACK (승인)**: 선택된 서버가 최종 승인(ACK)을 전송하여 클라이언트의 네트워크 인터페이스 설정 완료
5. **갱신(Renewal)**: 임대 만료 전 T1 타이머(50%) 도달 시 유니캐스트 Request를 전송하여 서비스를 중단 없이 유지

#### 한줄 요약
- Discover, Offer, Request, ACK 4단계를 거쳐 IP를 할당받고, T1 타이머 도달 시 임대를 갱신한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **동적 할당(Dynamic Allocation)**: 주소 풀 내에서 선착순으로 IP를 임대하고 미사용 시 회수하는 방식.
- **정적 바인딩(Static Reservation)**: 특정 기기의 MAC 주소에 대해 고정된 IP 주소를 영구 매핑하여 항시 동일 주소를 할당하는 방식.

</details>

| 비교 항목 | 동적 할당 (Dynamic Allocation) | 정적 바인딩 (Static Allocation) | 자동 할당 (Automatic Allocation) |
|:---|:---|:---|:---|
| **할당 방식** | 임대 시간(Lease Time) 기반 일시 대여 및 회수 | 클라이언트 MAC 주소 기반 사전 정의 고정 IP 부여 | 최초 접속 시 가용 IP를 영구적으로 자동 할당 |
| **적용 대상** | 일반 사용자 PC, 모바일 기기, 게스트 Wi-Fi | 서버, 네트워크 프린터, 스위치 관리 IP | 변경 필요성이 없는 고정 사무용 단말 |
| **자원 효율성** | 주소 재사용률 극대화 (IPv4 절약) | 주소 영구 점유로 확장성 제한 | 주소 회수가 어려워 IP 고갈 위험 |

#### 한줄 요약
- 유동 단말에는 동적 할당을, 서버/프린터 등 인프라 장비에는 정적 MAC 바인딩을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Rogue DHCP 서버**: 네트워크 내에 무단으로 설치되어 비인가 IP 및 악성 게이트웨이/DNS 정보를 배포하는 비인가 DHCP 서버.
- **DHCP 스누핑(DHCP Snooping)**: L2 스위치에서 신뢰할 수 있는 포트(Trusted Port)에서만 DHCP Offer/ACK 패킷을 허용하고 비인가 서버의 패킷을 차단하는 보안 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비인가 **Rogue DHCP 서버** 로 인한 IP 충돌 및 트래픽 탈취(MITM) | 스위치 수준 **DHCP 스누핑(DHCP Snooping)** 활성화 및 신뢰 포트(Trusted Port) 지정 | 비인가 서버의 Offer/ACK 응답 프레임 완전 차단 |
| 대량의 위조 MAC으로 Discover 패킷을 전송하는 **DHCP 고갈 공격(Starvation)** | 포트별 **DHCP 패킷 수신율 제한(Rate Limit)** 및 포트 보안(Port Security) 적용 | 가용 IP 풀 고갈 방지 및 브로드캐스트 DoS 방어 |
| L3 라우터로 분리된 원격 서브넷 단말의 IP 획득 불가 | 라우터/스위치 인터페이스에 **IP Helper-Address(릴레이 에이전트)** 설정 | 서브넷별 독립 서버 구축 비용 절감 및 중앙 통합 관리 |

#### 한줄 요약
- DHCP 스누핑으로 비인가 서버를 차단하고, Rate Limit으로 고갈 공격을 방어하며, 릴레이 에이전트로 중앙 관리를 수행한다.

## Ⅶ. 결론

- 대규모 엔터프라이즈 네트워크 구축 시 IP 관리 효율화를 위해 중앙 **DHCP 서비스**와 서브넷별 **Relay Agent**를 표준 배포하고, 비인가 서버 배포 및 IP 고갈 공격을 원천 방어하기 위해 스위치 레벨의 **DHCP Snooping** 및 DAI(Dynamic ARP Inspection) 바인딩 연동을 필수로 적용

#### 한줄 요약
- DORA 프로토콜 기반의 동적 주소 관리와 L2 DHCP 스누핑 보안 체계를 결합하여 운영 안정성을 확보한다.
