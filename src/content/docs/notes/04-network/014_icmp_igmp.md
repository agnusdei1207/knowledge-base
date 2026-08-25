---
sidebar:
  order: 14
  label: "014. ICMP•IGMP"
  badge:
    text: "기출 · 30%"
    variant: note
title: "ICMP•IGMP (ICMP IGMP)"
date: "2026-08-25T12:00:00+09:00"
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
- 배경/필요성: IP 자체의 오류 피드백 부재로 인한 **패킷 폐기 원인 규명 불가, 브로드캐스트 전송 시 L2/L3 대역폭 고갈 및 트래픽 스톰 해결 불가**

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
[ICMP 오류 보고 및 IGMP 멀티캐스트 제어 아키텍처]
|-- 1. ICMP Control Layer (IP Protocol 1: L3 라우터 -> 발신지 호스트 오류 보고)
|   |-- Echo Request (Type 8) / Echo Reply (Type 0) -> Ping 진단
|   |-- Destination Unreachable (Type 3 Code 4: PMTUD Frag Needed)
|   `-- Time Exceeded (Type 11 Code 0: TTL=0 만료 Traceroute)
`-- 2. IGMP Multicast Management Layer (IP Protocol 2: 서브넷 호스트 <-> 멀티캐스트 라우터)
    |-- IGMP Querier (대표 라우터: General Query 주기적 브로드캐스트/멀티캐스트 송출)
    |-- IGMP Snooping Switch (L2 스위치: Report/Leave 패킷 감청, 포트별 MAC 포워딩 필터링)
    `-- Multicast Host (가입 호스트: Membership Report 응답, Leave Group 탈퇴 통보)
```

선의 의미: 계층 및 ICMP는 라우터가 발신지로 오류를 반환하고, IGMP는 호스트와 라우터 간 멤버십을 L2 스위치가 감청하여 포워딩하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **ICMP 헤더** | Type(8b), Code(8b), 체크섬 및 **원래의 IP 헤더+64비트 페이로드를 포함하여 오류 보고** | IP 프로토콜 번호 1 |
| **IGMP Querier** | 로컬 서브넷 내 호스트를 대상으로 **주기적 Membership Query를 발송하여 그룹 가용성 확인** | 최저 IP 라우터 선출 |
| **IGMP Snooping** | L2 스위치가 **IGMP Report/Leave를 파싱하여 멀티캐스트 MAC 포워딩 테이블 구축** | L2 Flooding 방지 |
| **IGMPv1 / v2 / v3** | v1(기본 질의/보고), **v2(명시적 Leave/Fast-Leave), v3(Source Filtering / SSM 지원)** | 버전별 확장 |

#### 한줄 요약
- ICMP 헤더, IGMP Querier, IGMP Snooping, 버전별 메시지가 결합된다.

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
| **프로토콜 핵심 목적**| **1:1 유니캐스트 IP 패킷 전달 오류 보고 및 진단** | **1:N 멀티캐스트 수신 그룹 멤버십 가입/유지/탈퇴** |
| **동작 계층 및 번호** | **네트워크 계층 (L3 / IP 프로토콜 번호 1)** | **네트워크 계층 (L3 / IP 프로토콜 번호 2)** |
| **주요 대표 메시지** | **Echo Request/Reply, Destination Unreachable, TTL 만료** | **Membership Query, Membership Report, Leave Group** |
| **핵심 연동 장비** | 라우터, 방화벽, 종단 호스트 TCP/IP 스택 | **멀티캐스트 라우터(PIM), L2 스위치(IGMP Snooping)** |
| **보안 위협 요소** | ICMP Flooding (Smurf, Ping of Death), 네트워크 정찰 | 비인가 멀티캐스트 플러딩, 불법 채널 가입 스푸핑 |

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

- IP 네트워크의 안정성과 자원 효율성을 극대화하기 위해 **ICMP의 선별적 허용 정책을 통해 PMTUD 및 진단 가용성을 유지**하고, **대규모 IPTV/미디어 스트리밍 망에는 IGMPv3/SSM과 L2 IGMP Snooping 및 Fast-Leave**를 결합하여 대역폭 낭비를 차단하는 통합 L3/L2 제어 인프라 완성

#### 한줄 요약
- ICMP 오류 피드백과 IGMP/Snooping 멀티캐스트 최적화를 통해 고신뢰 네트워크 제어 및 고효율 미디어 전송을 실현한다.