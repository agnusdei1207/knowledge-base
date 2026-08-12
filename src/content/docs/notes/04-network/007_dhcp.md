---
sidebar:
  order: 7
  label: "007. DHCP (Dynamic Host Configuration Protocol)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "DHCP (Dynamic Host Configuration Protocol)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 7
extra:
  question_no: "007"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "설명형: DORA•Lease 구조 및 Relay Agent 동작 원리"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **동적 호스트 구성 프로토콜(Dynamic Host Configuration Protocol, DHCP)**: 네트워크에 접속하는 단말 장치에 IP 주소, 서브넷 마스크, 게이트웨이, DNS 서버 정보 등의 네트워크 설정 파라미터를 동적으로 자동 임대(Lease)해주는 응용 계층 프로토콜(UDP 67/68 포트 사용).
- **인터넷 프로토콜(Internet Protocol, IP)**: 네트워크 계층에서 호스트 식별 및 패킷 라우팅을 담당하는 논리적 주소 체계.

</details>

- 정의/개념: 단말이 네트워크에 접속할 때 **인터넷 프로토콜(Internet Protocol, IP)** 주소 및 접속 설정 정보를 중앙 서버가 일정 임대 기간(Lease Time) 동안 자동 부여하는 **동적 호스트 구성 프로토콜(Dynamic Host Configuration Protocol, DHCP)**.
- 배경/필요성: 수동 IP 설정 시 발생하는 중복 IP 충돌, 관리 오버헤드, 이동 단말 관리의 한계를 극복하고 IP 자원의 효율적 재활용 체계 마련.

#### 한줄 요약

- DORA 4단계 메커니즘 기반 IP 주소 자원 자동 임대 및 중앙 집중 관리 체계 구현.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **주소 풀(Address Pool)**: DHCP 서버가 수용 클라이언트들에게 임대해주기 위해 사전에 정의해 놓은 유효 IP 주소 대역.
- **바인딩(Binding)**: DHCP 서버가 특정 클라이언트의 MAC 주소와 임대한 IP 주소, 임대 만료 시간을 1:1 매핑하여 관리하는 상태 정보.
- **DHCP 릴레이 에이전트(DHCP Relay Agent)**: 라우터가 L2 브로드캐스트인 DHCP 요청 패킷을 유니캐스트 패킷으로 변환하여 타 서브넷의 중앙 DHCP 서버로 전달하는 기능.

</details>

- **주소 풀(Address Pool)** 및 **바인딩(Binding)** 관리를 통하여 동적 IP 자원의 효율적 회수 및 중복 할당 원천 방지.
- UDP 프로토콜 기반의 4단계 셰이크 핸드(DORA) 동작으로 신속한 클라이언트 자동 구성 지원.
- **DHCP 릴레이 에이전트(DHCP Relay Agent)**를 활용하여 서브넷마다 개별 서버를 두지 않고 중앙 DHCP 서버 통합 운용 지원.

#### 한줄 요약

- 주소 풀 임대 관리 및 DHCP Relay Agent를 통한 multi-subnet 중앙 제어 체계 구축.


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **DHCP 서버(DHCP Server)**: IP 주소 자원 풀을 관리하며 클라이언트 요청 시 네트워크 정보를 임대 및 갱신(Renewal)해주는 서버 (UDP 67 포트).
- **DHCP 클라이언트(DHCP Client)**: 부팅 시 DHCP 메시지를 브로드캐스트하여 IP 주소를 임대받는 단말 장치 (UDP 68 포트).
- **DORA 절차(Discover, Offer, Request, Acknowledge Procedures)**: IP 임대를 위해 클라이언트와 서버 간 교환하는 4단계 메커니즘.

</details>

```text
[ DHCP 클라이언트 (UDP 68) ]                          [ DHCP 서버 (UDP 67) ]
           |                                                       |
           | ----- 1. 탐색 (L2 브로드캐스트 / L3 브로드캐스트) ---> | (IP 요청)
           | <---- 2. 제안 (L2 유니캐스트/브로드캐스트, IP 제안) -- | (IP 후보제안)
           | ----- 3. 요청 (L2 브로드캐스트, IP 채택 및 요청) ----> | (선택 통보)
           | <---- 4. 승인 (L2 유니캐스트/브로드캐스트, 임대 확정) - | (임대 완료)
           |                                                       |
```

*DORA (Discover - Offer - Request - ACK) 4단계 메시지 교환 프로세스.*

| 구성요소 | 역할 및 세부 기능 | 전송 방식 및 포트 |
|:---|:---|:---|
| **DHCP 서버 (DHCP Server)** | 주소 풀 관리, 바인딩 테이블 갱신, 옵션(Gateway, DNS) 전달 | UDP 67 포트 수신 |
| **DHCP 클라이언트 (DHCP Client)** | 부팅 시 IP 임대 요청, T1/T2 타이머 기준 임대 연장 요청 | UDP 68 포트 사용 |
| **DORA 절차** | Discover(탐색) -> Offer(제안) -> Request(요청) -> ACK(확정) | L2/L3 Broadcast 및 Unicast 혼용 |
| **DHCP 옵션 (Option)** | Option 3(Gateway), Option 6(DNS), Option 121(Static Route) 명세 | DHCP 파라미터 확장 헤더 |

#### 한줄 요약

- Discover-Offer-Request-ACK 4단계 메시지 교환 및 Option 헤더 기반 네트워크 설정 할당 체계 준수.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **DHCP 탐색(DHCP Discover)**: 클라이언트가 네트워크상의 DHCP 서버를 찾기 위해 발송하는 브로드캐스트 메시지.
- **DHCP 제안(DHCP Offer)**: 서버가 클라이언트에게 임대 가능한 IP 주소 및 옵션 정보를 제안하는 메시지.
- **DHCP 요청(DHCP Request)**: 클라이언트가 제안받은 IP 주소를 최종 선택하여 해당 서버에 사용 승인을 요청하는 메시지.
- **DHCP 승인(DHCP ACK)**: 서버가 클라이언트에게 IP 주소 최종 임대 확정과 임대 시간(Lease Time)을 통보하는 메시지.

</details>

```text
[ 클라이언트 부팅 ]
        |
        v
[ 1. DHCP 탐색 ] --------> L2 (FF:FF:FF:FF:FF:FF) / L3 (255.255.255.255) 전송
        |
        v
[ 2. DHCP 제안 ] --------> 서버가 클라이언트 MAC 기반으로 IP 및 임대 시간 제안
        |
        v
[ 3. DHCP 요청 ] --------> 클라이언트가 제안받은 IP 선택 승인 요청 (타 서버에 거절 통보 겸함)
        |
        v
[ 4. DHCP 승인 ] --------> 서버가 최종 바인딩 등록 및 설정 완료 통보 (T1=50%, T2=87.5% 타이머 가동)
```

### 동작 원리

1. **임대 획득 (DORA Process)**: **DHCP 탐색(Discover)**으로 서버 탐색 후, **DHCP 제안(Offer)**, **DHCP 요청(Request)**, **DHCP 승인(ACK)** 과정을 거쳐 IP 임대 및 T1/T2 타이머 설정.
2. **임대 갱신 (Lease Renewal)**: T1 시간(임대 기간의 50%) 도달 시 해당 서버에 유니캐스트로 Request 전송하여 연장하고, 실패 시 T2 시간(87.5%) 도달 시 브로드캐스트로 타 서버에 Request 전송.

#### 한줄 요약

- DORA 4단계 임대 획득 및 T1/T2 타이머 기반 자동 임대 갱신 프로세스 구동.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **자동 할당(Automatic Allocation)**: DHCP가 클라이언트에게 한번 IP를 임대하면 영구적으로 고정 할당하는 방식.
- **동적 할당(Dynamic Allocation)**: 일정 임대 기간(Lease Time) 동안만 IP를 대여하고 미사용 시 회수하는 표준 할당 방식.
- **수동 할당(Manual Allocation / Static Binding)**: 클라이언트의 MAC 주소와 특정 IP 주소를 사전에 1:1 고정 매핑하여 할당하는 방식.

</details>

| 할당 방식 | **동적 할당 (Dynamic)** | **수동/고정 할당 (Manual/Static)** | **자동 할당 (Automatic)** |
|:---|:---|:---|:---|
| 핵심 개념 | 임대 시간 설정 기반 재사용 회수 | MAC 주소 기반 특정 고정 IP 할당 | 최초 할당 후 만료 없이 영구 제공 |
| 주 활용 대상 | 일반 사용자 PC, 모바일, Wi-Fi 단말 | 서버, 프린터, 네트워크 장비 | 변화가 없는 특정 기기 인프라 |
| 자원 효율성 | 최상 (IP 주소 재활용 극대화) | 보통 (IP 주소 고정 점유) | 낮음 (미사용 시 자원 잠김) |

> 요약: 주소 재활용 중심의 동적 할당 방식과 통제 대상 장비(서버/프린터)용 수동/고정 할당 방식의 보완적 운영.

#### 한줄 요약

- 동적 IP 대여(Dynamic)와 MAC 고정 바인딩(Static)의 차별적 할당 전략 수립.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **DHCP 스푸핑(DHCP Spoofing)**: 비인가 Rogue DHCP 서버를 네트워크에 설치하여 클라이언트에게 위조된 Gateway/DNS를 제공함으로써 트래픽을 도청(MITM)하는 공격.
- **DHCP 고갈 공격(DHCP Starvation Attack)**: 위조된 MAC 주소로 대량의 Discover 패킷을 발송하여 DHCP 서버의 IP 주소 풀을 완전히 고갈시키는 공격.
- **DHCP 스누핑(DHCP Snooping)**: L2 스위치가 DHCP 패킷을 검사하여 인가된 Port의 DHCP 서버 패킷만 허용하고, 클라이언트의 IP-MAC 바인딩 DB를 구축하는 보안 기술.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| Rogue DHCP 서버 출현 | 비인가 공유기/서버 접속으로 위조 IP/DNS 할당 | L2 스위치 **DHCP 스누핑(DHCP Snooping)** 적용 및 Trusted Port 지정 | 비인가 DHCP Offer/ACK 패킷 차단 |
| **DHCP 고갈 공격** | 대량의 무작위 MAC 발송으로 IP 풀 조기 매진 | Port Security (학습 MAC 개수 제한) 및 DHCP Snooping Rate Limit | IP 풀 고갈 예방 및 DOS 방지 |
| 서브넷 간 DHCP 전달 불능 | L2 브로드캐스트의 라우터 경계 차단 | 라우터에 **DHCP 릴레이 에이전트(ip helper-address)** 설정 | 서브넷 통합 DHCP 서비스 구현 |

#### 한줄 요약

- DHCP Snooping 보안 통제, Port Security 및 DHCP Relay Agent 설정을 통한 안정적 운영 체계 수립.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **임대 기간 최적화(Lease Time Optimization)**: 네트워크 환경(예: Wi-Fi 존: 2시간, 사내 LAN: 8일)에 맞게 임대 기간을 세밀히 조정하는 정책.
- **보안 통제 적용(Security Control Application)**: DHCP Snooping, Port Security, IP Source Guard(IPSG)를 연동하여 L2 보안성을 극대화하는 기법.

</details>

- 엔터프라이즈 네트워크의 주소 자원 관리와 보안성 확보를 위해 **임대 기간 최적화(Lease Time Optimization)**와 L2 스위치 중심의 **보안 통제 적용(Security Control Application)** 체계 구축 필수.

#### 한줄 요약

- DHCP Snooping L2 보안 결합 및 환경별 Lease Time 튜닝을 통한 주소 관리 체계 적용.
