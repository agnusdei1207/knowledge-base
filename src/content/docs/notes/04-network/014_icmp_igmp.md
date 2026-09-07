---
sidebar:
  order: 14
  label: "014. ICMP•IGMP"
  badge:
    text: "기출 · 30%"
    variant: note
title: "ICMP•IGMP (ICMP IGMP)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-network"
weight: 14
extra:
  question_no: "14"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "ICMP 에러 보고/진단(Type/Code) 및 IGMP 멀티캐스트 그룹 관리와 IGMP Snooping"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ICMP (Internet Control Message Protocol)**: L3 IP 프로토콜의 패킷 전달 오류를 발신지에 보고하고 링크 상태를 진단(Ping/Traceroute/PMTUD)하는 제어 프로토콜 (IP 프로토콜 번호 1).
- **IGMP (Internet Group Management Protocol)**: 로컬 서브넷 내 호스트와 멀티캐스트 라우터 간에 1:N 멀티캐스트 그룹 가입, 유지, 탈퇴를 관리하는 프로토콜 (IP 프로토콜 번호 2).

</details>

- 정의/개념: IP 패킷 전달 오류 보고 및 네트워크 진단을 담당하는 **ICMP와 로컬 서브넷 내 호스트의 멀티캐스트 그룹 멤버십을 동적으로 제어하는 IGMP**
- 배경/필요성: 비연결형 최선 노력(Best-Effort) 특성을 갖는 L3 IP 프로토콜이 패킷 전송 중 라우터 홉 초과(TTL=0), MTU 초과, 목적지 포트 닫힘 등의 이유로 패킷을 드롭하더라도 발신지 호스트에 오류를 알릴 수 없어 발생하는 침묵 유실 및 네트워크 상태 진단(Ping, Traceroute, PMTUD)의 부재를 해결하고, 1:N 실시간 멀티캐스트 스트리밍 시 수신자가 없는 포트까지 무분별하게 브로드캐스팅되는 네트워크 대역폭 낭비를 방지하기 위해, L3 오류 보고 및 진단을 수행하는 ICMP와 로컬 서브넷 내 호스트-라우터 간 동적 멀티캐스트 그룹 가입/탈퇴를 관리하는 IGMP(및 L2 IGMP Snooping)를 도입하여 **IP 계층의 상호 피드백 신뢰성과 고효율 멀티캐스트 전송 최적화**를 달성할 필요

#### 한줄 요약
- ICMP로 IP 전달 오류와 진단을 수행하고, IGMP와 IGMP Snooping으로 멀티캐스트 트래픽을 최적화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Type & Code (ICMP 타입 및 코드)**: 오류 유형(Type 3: Destination Unreachable, Type 11: Time Exceeded)과 세부 원인(Code 0: Net, Code 1: Host, Code 4: Frag Needed)을 규정.
- **IGMP Snooping**: L2 스위치가 IGMP 멤버십 패킷을 감청하여 멀티캐스트 트래픽을 가입된 포트로만 선별 전달하는 기술.

</details>

- Type과 Code 필드를 통해 패킷 폐기 원인 및 진단 정보를 전달하는 **ICMP 피드백 메커니즘**
- Query, Report, Leave 메시지를 통해 동적으로 활성 수신자를 갱신하는 **IGMP 멤버십 관리**
- L2 스위치에서 멀티캐스트의 전체 포트 플러딩을 방지하는 **IGMP Snooping 대역폭 최적화**

#### 한줄 요약
- Type/Code 기반 오류 피드백, 동적 멀티캐스트 수신자 관리, IGMP Snooping 플러딩 방지를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IGMP Querier**: 서브넷 내 복수 멀티캐스트 라우터 중 최저 IP를 가진 라우터가 선출되어 주기적 Query를 발송하는 대표 라우터.
- **SSM (Source-Specific Multicast)**: IGMPv3에서 멀티캐스트 그룹 IP뿐 아니라 송신자 소스 IP까지 지정하여 트래픽을 구독하는 방식.

</details>

```text
[ICMP 및 IGMP 제어 프로토콜 아키텍처]
  │
  ├─ [ICMP 제어 및 진단 체계] (오류 피드백 & 상태 진단)
  │     ├─ 오류 보고 메시지 (Type 3 도달불가, Type 11 시간초과)
  │     ├─ 진단 질의/응답 메시지 (Type 8/0 Echo Ping, Traceroute)
  │     └─ 경로 MTU 탐색 PMTUD (Type 3 Code 4 단편화 필요)
  │
  └─ [IGMP 멀티캐스트 제어 체계] (로컬 서브넷 그룹 관리)
        ├─ IGMP 라우터 (Querier: 주기적 Membership Query 발송)
        ├─ 호스트 멤버십 (Report 가입 보고, Leave 신속 탈퇴)
        ├─ IGMP Snooping (L2 스위치 감청 및 선별 포워딩)
        └─ IGMPv3 확장 (Source-Specific Multicast SSM 지원)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| ICMP 헤더 | Type/Code, 체크섬 및 원본 IP 헤더를 포함하여 패킷 전달 오류 보고 |
| IGMP Querier | 로컬 서브넷 내 주기적 Query를 발송하여 멀티캐스트 활성 수신자 상태 확인 |
| IGMP Snooping | L2 스위치가 IGMP 패킷을 감청하여 멀티캐스트 MAC 포워딩 테이블 구축 |
| IGMPv1/v2/v3 | 기본 가입/보고, 명시적 Leave 및 송신자 필터링(SSM) 버전별 지원 |

#### 한줄 요약
- IGMP Snooping이 L2 스위치 안에 끼어들어 멤버십 메시지를 엿봄으로써, 라우터만 알던 그룹 가입 여부를 스위치가 대신 판단해 포트 단위 플러딩을 걷어낸다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PMTUD 3단계**: DF=1 대형 패킷 전송 $\to$ 라우터 MTU 초과 폐기 및 ICMP Type 3 Code 4 반환 $\to$ 송신단 MSS 축소 재전송.

</details>

```text
ICMP 오류 처리(PMTUD) 및 IGMP 그룹 관리
        │
   1. [대형 패킷 전송] 송신 호스트가 DF=1 설정 후 1500B 패킷 송출
        │
   2. [라우터 MTU 초과 폐기] 중간 라우터(MTU 1400B)에서 패킷 폐기 -> Next-Hop MTU 담아 ICMP Type 3 Code 4 반환
        │
   3. [송신단 MSS 재조정] 송신 호스트가 통보받은 MTU 1400B로 MSS 축소 후 재전송 완료
   ┌────┴───────────────────────────┐
  IGMP 그룹 가입                   IGMP 신속 탈퇴 (Fast-Leave)
   │                                 │
4A. [호스트 Membership Report 송출]  4B. [호스트 Leave Group 메시지 송출]
   스위치가 Snooping 테이블에 포트 등록   스위치가 즉시 해당 포트 포워딩 차단 (대역폭 회수)
   │                                 │
   └────┬────────────────────────────┘
        ▼
   안정적인 L3 오류 진단 및 L2 멀티캐스트 스트리밍 완료
```

#### 한줄 요약
- ICMP PMTUD로 MTU를 동적 조정하고, IGMP Report/Leave로 멀티캐스트 포워딩을 최적화한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ICMP vs IGMP**: 유니캐스트 오류 진단 프로토콜(ICMP)과 멀티캐스트 그룹 멤버십 관리 프로토콜(IGMP).

</details>

| 비교 항목 | 인터넷 제어 메시지 프로토콜 (ICMP) | 인터넷 그룹 관리 프로토콜 (IGMP) |
|:---|:---|:---|
| 프로토콜 핵심 목적 | **1:1 유니캐스트 IP 패킷 전달 오류 보고 및 진단** | **1:N 멀티캐스트 수신 그룹 멤버십 가입/유지/탈퇴** |
| 동작 계층 및 번호 | **네트워크 계층 (L3 / IP 프로토콜 번호 1)** | **네트워크 계층 (L3 / IP 프로토콜 번호 2)** |
| 주요 대표 메시지 | **Echo Request/Reply, Destination Unreachable, TTL 만료** | **Membership Query, Membership Report, Leave Group** |
| 핵심 연동 장비 | 라우터, 방화벽, 종단 호스트 TCP/IP 스택 | **멀티캐스트 라우터(PIM), L2 스위치(IGMP Snooping)** |
| 보안 위협 요소 | ICMP Flooding (Smurf, Ping of Death), 네트워크 정찰 | 비인가 멀티캐스트 플러딩, 불법 채널 가입 스푸핑 |

#### 한줄 요약
- ICMP는 유니캐스트 오류 피드백 및 진단을 수행하고, IGMP는 멀티캐스트 그룹 멤버십을 관리한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ICMP Black Hole**: 방화벽에서 ICMP를 무조건 전면 차단하여 PMTUD가 동작하지 못해 대형 TCP 패킷이 응답 없이 폐기되는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 방화벽 ICMP 전면 차단으로 인한 PMTUD 미동작 및 TCP 블랙홀 장애 | 방화벽 정책에서 **`ICMP Type 3 Code 4 (Frag Needed)` 선별 허용** | PMTUD 정상 동작 및 MTU 불일치 드롭 방지 |
| 대규모 ICMP Echo 패킷을 악용한 디도스(Smurf) 및 CPU 고갈 | 라우터 제어 평면에 **`CoPP (Control Plane Policing) ICMP Rate Limit`** | 제어 평면 CPU 보호 및 가용성 유지 |
| L2 스위치의 멀티캐스트 브로드캐스팅으로 인한 네트워크 대역폭 포화 | L2 스위치 전 포트에 **`IGMP Snooping 및 Fast-Leave` 필수 활성화** | 미가입 포트 트래픽 차단 및 대역폭 절약 |
| 비인가 악의적 멀티캐스트 트래픽 주입 공격 | **`IGMPv3 소스 필터링(SSM)` 및 PIM 라우터 접근 제어 목록(ACL)** | 허가된 소스 스트림만 안전 수신 |

#### 한줄 요약
- ICMP Type 3 Code 4 허용, CoPP Rate Limit, IGMP Snooping, SSM 소스 필터링으로 운영한다.

## Ⅶ. 결론

- IP 네트워크의 상태 진단/오류 보고(ICMP)와 IPTV·금융 시세 피드 등 실시간 대규모 미디어 배포(IGMP)를 지탱하는 **가장 핵심적인 L3 제어 및 그룹 통신 표준 프로토콜**로 확립되었으며, 실무 운영 시에는 **PMTUD 장애로 인한 TCP 블랙홀을 방지하기 위한 ICMP Type 3 Code 4 선별 허용, 제어 평면 보호를 위한 CoPP(Control Plane Policing) Rate Limiting, L2 스위치 전 포트 IGMP Snooping 및 Fast-Leave 활성화, 특정 송신원 스트림만 수신하는 IGMPv3 SSM(Source-Specific Multicast) 구성**을 결합하여 안정성과 전송 효율을 극대화

#### 한줄 요약
- ICMP 오류 피드백과 IGMP/Snooping 멀티캐스트 최적화를 통해 고신뢰 네트워크 제어 및 고효율 미디어 전송을 실현한다.
