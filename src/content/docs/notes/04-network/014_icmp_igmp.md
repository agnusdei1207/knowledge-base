---
sidebar:
  order: 14
  label: "014. ICMP•IGMP (ICMP IGMP)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "네트워크 제어 및 멀티캐스트 그룹 관리 프로토콜 : ICMP와 IGMP"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 14
extra:
  question_no: "014"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "ICMP 에러 보고/진단(Type/Code) 및 IGMP 멀티캐스트 그룹 관리와 IGMP Snooping"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **인터넷 제어 메시지 프로토콜(ICMP, Internet Control Message Protocol)**: 네트워크 계층(L3)에서 IP 패킷 전달 중 발생하는 오류를 발신지에 보고하고, 링크 진단(Ping, Traceroute) 및 경로 MTU 탐색(PMTUD)을 수행하는 제어 프로토콜.
- **인터넷 그룹 관리 프로토콜(IGMP, Internet Group Management Protocol)**: 로컬 서브넷 내의 IP 호스트와 인접 멀티캐스트 라우터 간에 멀티캐스트 수신 그룹의 가입(Join), 유지(Membership Query) 및 탈퇴(Leave) 상태를 관리하는 프로토콜.

</details>

- 정의/개념: 비연결형 IP 프로토콜의 전송 오류 보고 및 네트워크 진단을 담당하는 **ICMP** 와, 로컬 서브넷 내 호스트의 멀티캐스트 그룹 멤버십을 동적으로 관리하는 **IGMP**
- 배경/필요성: IP 자체의 오류 제어 기능 부재로 인한 패킷 폐기 원인 불명확성을 해소하고, 1:N 대용량 미디어 스트리밍 시 불필요한 브로드캐스트 트래픽 범람을 방지할 요구

#### 한줄 요약
- ICMP는 IP 오류 보고와 링크 진단을, IGMP는 로컬 멀티캐스트 그룹 멤버십 관리를 담당한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ICMP 메시지 유형(Type) 및 코드(Code)**: Type(에러 범주: 목적지 도달 불가 3, 시간 초과 11 등)과 Code(세부 원인: 포트 도달 불가 3, 단편화 필요 4 등)의 계층적 조합으로 오류 원인을 특정하는 필드.
- **IGMP 스누핑(IGMP Snooping)**: L2 스위치가 라우터와 호스트 간에 오가는 IGMP 패킷을 감청(Snooping)하여, 실제로 멀티캐스트를 요청한 포트로만 트래픽을 선별 포워딩하는 기능.

</details>

- **ICMP 계층적 오류 특정**: **Type/Code** 필드 조합 및 원본 IP 헤더+8바이트 페이로드를 포함하여 송신지 호스트에 정확한 장애 원인 피드백
- **IGMP 동적 멤버십 수립**: 질의(Query), 보고(Report), 탈퇴(Leave) 메시지 기반으로 서브넷 내 활성 멀티캐스트 수신자 목록 갱신
- **L2 대역폭 최적화**: L2 스위치의 **IGMP Snooping** 과 연계하여 멀티캐스트 트래픽의 전 포트 플러딩을 차단하고 필요한 포트에만 전달

#### 한줄 요약
- Type/Code 기반 오류 피드백, 동적 멀티캐스트 그룹 제어, IGMP Snooping을 통한 L2 대역폭 절감을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IGMP 질의자(IGMP Querier)**: 서브넷 내 복수의 멀티캐스트 라우터 중 가장 낮은 IP 주소를 가진 라우터가 선출되어 주기적으로 호스트에 그룹 멤버십 질의(Query)를 발송하는 대표 라우터.
- **소스 특정 멀티캐스트(Source-Specific Multicast, SSM)**: IGMPv3에서 특정 멀티캐스트 그룹 IP뿐만 아니라 특정 송신자 소스 IP까지 지정하여 채널을 구독하는 방식.

</details>

```text
[ ICMP 오류 보고 흐름 ]                  [ IGMP 멀티캐스트 그룹 관리 흐름 ]

 [ 라우터 (패킷 폐기) ]                     [ 멀티캐스트 라우터 (IGMP Querier) ]
         │ (ICMP Type 3 에러 피드백)                 │ (Membership Query 주기적 발송)
         ▼                                           ▼
 [ 송신 호스트 (PMTUD 조정) ]             ┌────────────────────────────────────┐
                                          │ L2 스위치 (IGMP Snooping 감청)     │
                                          └───────┬────────────────────┬───────┘
                                                  │ (Report 포워딩)    │ (미가입 포트 차단)
                                                  ▼                    ▼
                                          [ 가입 호스트 ]        [ 미가입 호스트 ]
```

선의 의미: ICMP는 L3 라우터가 발신지로 오류를 역전송하고, IGMP는 라우터와 호스트 간 멤버십을 L2 스위치가 감청하여 포워딩하는 구조

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| **ICMP 헤더** | Type, Code, 체크섬 및 원본 IP 헤더를 포함하여 오류 상세 원인 전달 | IP 프로토콜 번호 1 |
| **IGMP Querier** | 서브넷 내 호스트를 대상으로 주기적 Membership Query를 발송하여 수신자 존재 확인 | 라우터 선출 |
| **IGMP Snooping** | L2 스위치가 IGMP Report/Leave를 파싱하여 멀티캐스트 MAC 포워딩 테이블 구축 | L2 Flooding 방지 |
| **IGMPv1/v2/v3** | v1(기본 질의/보고), v2(명시적 Leave 및 Fast-Leave 지원), v3(Source Filtering/SSM 지원) | 버전별 확장 |

#### 한줄 요약
- ICMP 헤더, IGMP Querier, IGMP Snooping, 버전별 메시지(v1/v2/v3)가 결합하여 네트워크 제어를 수행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **경로 MTU 탐색(Path MTU Discovery, PMTUD)**: IP 패킷의 Don't Fragment(DF=1) 플래그를 설정하여 전송하고, MTU 초과 시 수신되는 ICMP Type 3 Code 4(Fragmentation Needed) 메시지를 바탕으로 종단 간 최소 MTU를 동적 학습하는 기법.

</details>

```text
[ ICMP 기반 PMTUD 동작 ]
 1. 송신 호스트가 DF=1 설정 후 대형 IP 패킷 송출
 2. 중간 라우터에서 MTU 초과로 패킷 폐기 ➔ 송신 호스트로 ICMP Type 3 Code 4(Next-Hop MTU 포함) 반환
 3. 송신 호스트가 통보받은 MTU 크기로 세그먼트(MSS) 재조정 후 재전송

[ IGMP 멀티캐스트 그룹 가입 및 트래픽 포워딩 ]
 1. 수신 호스트가 특정 멀티캐스트 그룹(예: `239.1.1.1`) 가입을 위해 IGMP Membership Report 전송
 2. L2 스위치가 IGMP Snooping으로 해당 포트를 멀티캐스트 포워딩 테이블에 등록
 3. 멀티캐스트 라우터가 트래픽 수신 시 가입된 스위치 포트로만 스트림 전송
```

**동작 원리**

1. **ICMP 오류 처리**: 라우터가 TTL=0 도달 시 Type 11(Time Exceeded), MTU 초과 시 Type 3 Code 4를 생성하여 발신지 IP로 전송
2. **IGMP 그룹 갱신**: IGMP Querier가 주기적으로 일반 질의(General Query)를 발송하고, 호스트가 응답 타이머 만료 전 Report를 전송하여 세션 유지
3. **신속 탈퇴(Fast-Leave)**: 호스트가 Leave Group 메시지를 송출하면 스위치가 즉시 해당 포트의 포워딩을 중단하여 대역폭 낭비 방지

#### 한줄 요약
- ICMP PMTUD를 통한 MTU 동적 조정과 IGMP 질의/보고/Snooping을 통한 멀티캐스트 트래픽 포워딩을 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **유니캐스트(Unicast) vs 멀티캐스트(Multicast)**: 1:1 단일 대상 전송 방식과 그룹 가입자 전체에게 단일 패킷을 동시 복제 전송하는 1:N 전송 방식.

</details>

| 비교 항목 | 인터넷 제어 메시지 프로토콜 (ICMP) | 인터넷 그룹 관리 프로토콜 (IGMP) |
|:---|:---|:---|
| **프로토콜 목적** | **1:1 유니캐스트 전송 오류 보고 및 진단** | **1:N 멀티캐스트 수신 그룹 멤버십 관리** |
| **동작 계층** | **네트워크 계층 (L3 / IP 프로토콜 1)** | **네트워크 계층 (L3 / IP 프로토콜 2)** |
| **대표 메시지** | Echo Request/Reply, Destination Unreachable | Membership Query, Membership Report, Leave |
| **협력 인프라** | 라우터, 방화벽, 종단 호스트 스택 | **멀티캐스트 라우터(PIM), L2 스위치(IGMP Snooping)** |
| **보안 위협** | ICMP Flooding (Smurf, Ping of Death), Recon | Unknown Multicast Flooding, 악의적 가입 위조 |

#### 한줄 요약
- ICMP는 유니캐스트 오류 보고 및 진단 프로토콜이며, IGMP는 멀티캐스트 그룹 멤버십 관리 프로토콜이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ICMP 레이트 리미팅(ICMP Rate Limiting)**: 라우터가 초당 생성 및 응답하는 ICMP 메시지 개수를 하드웨어 레벨에서 제한하여 DoS 공격 및 CPU 자원 고갈을 방지하는 기술.
- **알 수 없는 멀티캐스트 플러딩(Unknown Multicast Flooding)**: IGMP Snooping이 비활성화되었을 때 스위치가 멀티캐스트 패킷을 브로드캐스트로 취급하여 모든 포트로 플러딩하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 보안을 위해 방화벽에서 ICMP 전면 차단 시 PMTUD 미동작으로 인한 TCP 블랙홀 | 방화벽 정책에서 **ICMP Type 3 Code 4(단편화 필요)** 선별 허용 | PMTUD 정상 동작 및 MTU 불일치 패킷 드롭 방지 |
| 대규모 ICMP Echo 요청을 악용한 Smurf DDoS 공격 및 라우터 CPU 고갈 | 라우터 제어 평면(CoPP)에 **ICMP 전송률 제한(Rate Limiting)** 적용 | 제어 평면 CPU 자원 보호 및 서비스 가용성 유지 |
| L2 스위치의 멀티캐스트 브로드캐스팅으로 인한 네트워크 대역폭 포화 | L2 스위치 전 포트에 **IGMP Snooping 및 Fast-Leave** 의무 활성화 | 미가입 포트 트래픽 격리 및 L2 링크 대역폭 최적화 |

#### 한줄 요약
- ICMP Type 3 Code 4 선별 허용으로 PMTUD를 보장하고, CoPP 레이트 리미팅으로 DoS를 방어하며, IGMP Snooping으로 L2 플러딩을 차단한다.

## Ⅶ. 결론

- IP 네트워크의 안정성과 진단성을 확보하기 위해 **ICMP 에러 보고** 및 **선별적 필터링 정책**을 적용하여 PMTUD 정상성을 유지하고, IPTV 및 대규모 실시간 스트리밍 인프라에는 **IGMPv3/SSM** 과 L2 **IGMP Snooping** 을 통합 구축하여 대역폭 효율성과 그룹 통제력을 동시에 확보

#### 한줄 요약
- ICMP 오류 피드백과 IGMP/Snooping 멀티캐스트 최적화를 통해 고신뢰 네트워크 제어 인프라를 완성한다.
