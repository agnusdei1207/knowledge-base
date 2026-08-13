---
sidebar:
  order: 14
  label: "014. 인터넷 제어•그룹 관리 프로토콜 (ICMP•IGMP)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "인터넷 제어•그룹 관리 프로토콜 (ICMP•IGMP)"
date: "2026-08-13T16:29:00+09:00"
tags:
  - "notes-network"
weight: 14
extra:
  question_no: "014"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "비교형: 132회 ICMP•IGMP 역할 직접 비교"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **인터넷 제어 메시지 프로토콜(Internet Control Message Protocol, ICMP)**: 네트워크 계층(L3)에서 IP 패킷 전달 도중 발생하는 에러 통보, 상태 피드백 및 도달성 진단(Ping, Traceroute)을 수행하는 보조 프로토콜 (IP 프로토콜 번호 1).
- **인터넷 그룹 관리 프로토콜(Internet Group Management Protocol, IGMP)**: IPv4 네트워크 환경에서 호스트 단말과 라우터 간에 멀티캐스트 그룹 가입(Join), 유지, 탈퇴(Leave) 정보를 교환하는 그룹 제어 프로토콜 (IP 프로토콜 번호 2).
- **인터넷 프로토콜(Internet Protocol, IP)**: 논리적 호스트 주소 지정 및 패킷 라우팅을 담당하는 비연결형 프로토콜.
- **인터넷 프로토콜 버전 4(Internet Protocol version 4, IPv4)**: 32비트 주소 체계를 기반으로 멀티캐스트(Class D: 224.0.0.0/4) 통신을 수용하는 인터넷 프로토콜.

</details>

- 정의/개념: L3 IP 전송의 신뢰성 보완을 위한 에러 리포팅 메커니즘인 **인터넷 제어 메시지 프로토콜(Internet Control Message Protocol, ICMP)**과 1:N 멀티캐스트 그룹 관리 메커니즘인 **인터넷 그룹 관리 프로토콜(Internet Group Management Protocol, IGMP)**.
- 배경/필요성: 비연결형 Best-Effort 전송 특성을 갖는 IP 프로토콜만으로는 전송 실패 원인 분석, PMTUD(Path MTU Discovery) 탐색 및 멀티캐스트 그룹 수신자 추적이 불가능함.

#### 한줄 요약

- L3 패킷 에러 통보/진단용 ICMP 및 L2/L3 멀티캐스트 그룹 관리용 IGMP 제어 체계 구현.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **ICMP 유형(ICMP Type)**: ICMP 메시지의 대분류 목적(예: 0=Echo Reply, 3=Destination Unreachable, 8=Echo Request, 11=Time Exceeded)을 나타내는 8비트 필드.
- **ICMP 코드(ICMP Code)**: 동일한 ICMP Type 내부에서 세부 에러 원인(예: Type 3 Code 4 = Fragmentation Needed)을 소분류 나타내는 8비트 필드.
- **IGMP 질의(IGMP Membership Query)**: 라우터(Querier)가 동일 LAN 상의 호스트들에게 주기적(General Query) 또는 특정 그룹(Group-Specific Query) 수신자가 존재하는지 묻는 메시지 (224.0.0.1).
- **IGMP 보고(IGMP Membership Report)**: 호스트가 특정 멀티캐스트 그룹에 가입하고자 하거나 라우터의 Query에 응답하기 위해 발송하는 메시지.
- **IGMP 탈퇴(IGMP Leave Group)**: IGMPv2 이상에서 호스트가 해당 멀티캐스트 그룹 수신을 중단할 때 라우터에 빠르게 통보하는 메시지 (224.0.0.2).

</details>

- **ICMP 유형(ICMP Type)** 및 **ICMP 코드(ICMP Code)** 헤더 조합으로 구체적 에러 원인 통보 및 오리지널 IP 헤더+데이터 64비트를 포함하여 장애 지점 추적 지원.
- **IGMP 질의(Query)**, **IGMP 보고(Report)**, **IGMP 탈퇴(Leave Group)**의 3단계 메시지 교환으로 서브넷 내 멀티캐스트 가입 상태 동적 관리.
- L2 스위치의 **IGMP 스누핑(IGMP Snooping)** 기능과 연동하여 브로드캐스트 성격의 멀티캐스트 트래픽이 비가입 포트로 확산되는 현상 완전 차단.

#### 한줄 요약

- ICMP Type/Code 제어 파라미터 및 IGMP Query/Report/Leave 세션 관리 체계 구축.


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **IGMP 스누핑(IGMP Snooping)**: L2 스위치가 포트 간 지나가는 IGMP Report/Leave 패킷을 유심히 엿듣고(Snooping), 멀티캐스트 그룹을 원하는 포트로만 1:1 선별 포워딩해주는 L2 조율 기능.
- **IGMP 질의자(IGMP Querier)**: 서브넷 라우터 중 대표로 선출되어 주기적으로 IGMP Membership Query를 발송하는 최저 IP 주소 라우터.
- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: 스위치 내에서 논리적으로 브로드캐스트 도메인을 분리한 구역.

</details>

```text
[ Multicast Source ]
        |
        v
[ Multicast Router (IGMP Querier) ] <--- IGMP Membership Query / Report
        |
        v
[ L2 Switch (IGMP Snooping Table) ] ---> [Group 239.1.1.1] -> Port 1, Port 3 (Port 2 Excluded)
     /         \
    v           v
[ Host A ]  [ Host C ] (Joined 239.1.1.1)
```

*IGMP Querier 및 L2 스위치의 IGMP Snooping 포트 바인딩 구조.*

| 구성요소 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|
| **ICMP 헤더** | Type(8비트), Code(8비트), Checksum(16비트) + 원본 패킷 헤더 일부 | L3 IP 페이로드에 캡슐화 |
| **IGMP Querier** | 서브넷 내 호스트 멀티캐스트 그룹 가입 여부 갱신 탐색 | 라우터 간 IP 비교 선출 |
| **IGMP Snooping** | L2 스위치가 IGMP 리포트를 파싱하여 [VLAN ID - Group IP - Port] 매핑 DB 수립 | 무분별한 L2 Flooding 차단 |
| **IGMPv1 / v2 / v3** | v1: Query/Report만 지원, v2: Explicit Leave 추가, v3: SSM(Source-Specific Multicast) 지원 | 버전별 호환성 관리 |

#### 한줄 요약

- L3 Querier 상태 유지 및 L2 IGMP Snooping MAC/Port 바인딩 테이블 관리 체계 준수.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **멀티캐스트(Multicast)**: 특정 멀티캐스트 주소(224.0.0.0/4)에 가입한 다수의 정당한 수신자들에게만 단일 전송하여 대역폭 효율을 극대화하는 방식.
- **가입 포트 갱신(Group Join Port Update)**: IGMP Snooping 스위치가 호스트의 IGMP Report를 감지하여 해당 포트를 멀티캐스트 수신 테이블에 등록하는 절차.

</details>

```text
[ ICMP 동작: IP 전송 장애 발생 ]
  Router/Host -> IP 패킷 전송 실패 (MTU 초과 / TTL=0 만료)
                     |
                     v
  [ ICMP Error Message 생성 ] -> Type 3 Code 4 (Fragmentation Needed) 또는 Type 11 Code 0 (TTL Exceeded)
                     |
                     v
  [ 원본 송신 호스트 전달 ] -> PMTUD 실행 또는 Traceroute Hop 경로 파악

[ IGMP 동작: 멀티캐스트 방송 가입 ]
  Host -> [ IGMP Report (Join 239.10.10.1) ] 브로드캐스트
                     |
                     v
[ IGMP Snooping Switch ] ------> 가입 포트를 멀티캐스트 테이블에 추가
                     |
                     v
[ IGMP Querier Router ] -------> PIM 상태 갱신 및 스트림 유입 허용
```

### 동작 원리

- **ICMP 피드백**: Type•Code로 전송 실패 원인 통보
- **IGMP 동적 포워딩**: 가입 포트에만 멀티캐스트 전달

#### 한줄 요약

- ICMP 오류 통보와 IGMP 가입 포트 전달

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **경로 최대 전송 단위 탐색(Path Maximum Transmission Unit Discovery, PMTUD)**: 송신 호스트가 DF(Don't Fragment) 비트를 1로 설정하여 패킷을 보낸 후, 중간 라우터의 ICMP Type 3 Code 4 피드백을 통해 단편화 없는 최적 MTU를 자동으로 찾아내는 기술.

</details>

| 비교 항목 | **ICMP (Internet Control Message Protocol)** | **IGMP (Internet Group Management Protocol)** |
|:---|:---|:---|
| 프로토콜 목적 | 네트워크 도달성 진단 및 IP 패킷 전송 에러 제어 통보 | 서브넷 내 호스트들의 멀티캐스트 그룹 가입/유지/탈퇴 관리 |
| 주요 메시지 | Echo Request/Reply(Ping), Destination Unreachable, TTL Exceeded | General Query, Group-Specific Query, Membership Report, Leave Group |
| 대상 트래픽 | 1:1 Unicast 진단 피드백 | 1:N Multicast 스트림 포워딩 통제 |
| 보안 고려사항 | ICMP Flooding/Smurf Attack, Ping of Death / 방화벽 선택 차단 필요 | Unknown Multicast Flooding 방지 / IGMP Snooping 설정 필수 |

> 요약: L3 오류 진단 및 경로 MTU 탐색용 ICMP와, L2/L3 멀티캐스트 스트림 제어용 IGMP의 기능 및 목적 구별.

#### 한줄 요약

- 네트워크 진단/PMTUD 수행용 ICMP와 IPTV/Media 그룹 가입 제어용 IGMP의 보완적 역할 분담.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **ICMP 전송률 제한(ICMP Rate Limiting)**: 대량의 ICMP 패킷으로 인한 라우터 CPU 고갈 및 DDoS 반사 공격을 방지하기 위해 라우터의 초당 ICMP 응답 건수를 억제하는 기능.
- **알 수 없는 멀티캐스트 플러딩(Unknown Multicast Flooding)**: L2 스위치에 IGMP Snooping이 설정되지 않아 수신자 목록에 없는 멀티캐스트 패킷을 VLAN 내 전체 포트로 브로드캐스트하여 스톰을 일으키는 현상.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| PMTUD 동작 불능 패킷 드롭 | 방화벽에서 모든 ICMP 패킷을 일괄 Block | **ICMP Type 3 Code 4(Fragmentation Needed)** 선택적 허용 | TCP MSS 튜닝 및 PMTUD 정상 동작 |
| ICMP 반사/고갈 DDoS 공격 | 대량의 ICMP Echo 및 Unreachable 발송 | **ICMP 전송률 제한(Rate Limiting)** 및 Smurf 방지 설정 | 라우터 CPU 및 백본 대역폭 보호 |
| 멀티캐스트 트래픽 폭풍 | L2 스위치에 IGMP Snooping 미설정 | L2 스위치 **IGMP Snooping** 및 Fast-Leave 기능 활성화 | **알 수 없는 멀티캐스트 플러딩** 방지 |

#### 한줄 요약

- ICMP Rate Limiting, PMTUD용 Type 3 Code 4 허용 및 IGMP Snooping 기반 무분별 플러딩 방어 체계 수립.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **ICMP 선별 허용(Selective ICMP Filtering)**: 보안 강화를 위해 일반 Ping(Echo)은 방화벽에서 제어하되, PMTUD 및 MTU 조율용 ICMP 제어 파라미터는 허용하는 보안 정책.
- **IGMP 가입 범위 제한(IGMP Membership Scope Limitation)**: IGMP Snooping 및 PIM-SM/SSM 라우팅을 통해 실제 가입 포트 및 허용 대역에만 멀티캐스트 스트림을 한정 전송하는 수립 정책.

</details>

- 안정적인 패킷 통신 무결성 및 멀티캐스트 인프라 보장을 위해 **ICMP 선별 허용(Selective ICMP Filtering)** 정책과 **IGMP 가입 범위 제한(IGMP Membership Scope Limitation)**을 결합한 L2/L3 트래픽 통제 구현 필수.

#### 한줄 요약

- ICMP Type 3/8 선별 보안 허용 및 IGMP Snooping 기반 멀티캐스트 대역폭 최적화 구현 필수.
