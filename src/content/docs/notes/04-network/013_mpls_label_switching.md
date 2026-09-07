---
sidebar:
  order: 13
  label: "013. MPLS 레이블 스위칭"
  badge:
    text: "기출 · 30%"
    variant: note
title: "MPLS 레이블 스위칭 (Multiprotocol Label Switching)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-network"
weight: 13
extra:
  question_no: "13"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "2.5계층 고정 길이 레이블 기반 고속 스위칭 및 트래픽 엔지니어링"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MPLS (Multi-Protocol Label Switching)**: IP 패킷 헤더 전체를 매번 조회하는 대신 2계층과 3계층 사이에 32비트 고정 레이블(Shim Header)을 삽입하여 고속 스위칭하는 2.5계층 기술.
- **FEC (Forwarding Equivalence Class)**: 동일한 목적지, 동일한 QoS 및 동일한 경로(LSP)로 취급되는 패킷들의 집합.
- **LSP (Label Switched Path)**: 인입 LER에서 송출 LER까지 레이블 스왑(Swap)을 통해 사전에 수립된 단방향 레이블 스위칭 경로.

</details>

- 정의/개념: L2와 L3 사이에 32비트 **고정 레이블(Shim Header)을 삽입하여 LFIB 기반 고속 포워딩과 트래픽 엔지니어링을 제공하는 2.5계층 스위칭 기술**
- 배경/필요성: 전통적인 홉 단위(Hop-by-Hop) IP 라우팅에서 코어 라우터가 매 패킷마다 가변 길이 L3 IP 헤더를 검사하고 소프트웨어/하드웨어 최장 프리픽스 일치(LPM) 검색을 반복 수행함에 따른 포워딩 지연 오버헤드와 트래픽 엔지니어링(명시적 경로 지정) 및 고객사별 독립 가상망(VPN) 격리가 불가능한 한계를 극복하기 위해, L2와 L3 사이에 32비트 고정 길이 Shim Header 레이블을 삽입하고 인입 LER에서 1회 FEC 분류 후 코어 영역에서는 단순 20비트 레이블 스왑(LFIB Swap)만으로 고속 포워딩하는 MPLS(Multiprotocol Label Switching)를 도입하여 **백본 패킷 처리량 극대화, RSVP-TE 기반 명시적 트래픽 제어 및 BGP/MPLS L3VPN을 통한 완벽한 멀티테넌트 격리**를 달성할 필요

#### 한줄 요약
- 32비트 Shim Header 레이블을 활용하여 IP 룩업 오버헤드를 없애고 50ms 미만 고속 복구를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Label Stack (레이블 스택)**: 단일 패킷에 복수의 레이블을 겹쳐서 삽입(Push)함으로써 백본 전송용(Outer)과 VPN 고객 식별용(Inner)을 분리 계층화하는 구조.
- **PHP (Penultimate Hop Popping)**: 송출 LER의 이중 룩업 부하를 방지하기 위해 직전 LSR에서 외곽 레이블을 미리 제거(Implicit Null, Label 3)해 전달하는 최적화 메커니즘.

</details>

- 인입 LER에서 패킷을 FEC로 분류하고 레이블 삽입(Push), 코어 Swap, 송출 Pop 수행
- 3계층 IP 헤더를 검사하지 않고 20비트 Label ID만 교환하는 **LFIB 하드웨어 고속 스위칭**
- 레이블 스택 구조를 통해 서비스와 경로를 분리하는 **BGP/MPLS L3VPN 및 트래픽 엔지니어링(MPLS-TE)**

#### 한줄 요약
- Push-Swap-Pop 레이블 파이프라인, LFIB 고속 룩업, 다층 레이블 스택을 통한 서비스 격리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **LFIB (Label Forwarding Information Base)**: 인입 인터페이스/레이블과 송출 인터페이스/레이블을 1:1 매핑하여 ASIC 하드웨어에서 스위칭하는 포워딩 테이블.

</details>

```text
[MPLS 레이블 스위칭 아키텍처]
  │
  ├─ [에지 영역] (LER, Label Edge Router)
  │     ├─ 인입 LER (Ingress: FEC 분류 및 32비트 레이블 Push)
  │     └─ 송출 LER (Egress: 최종 레이블 Pop 및 L3 IP 복원)
  │
  ├─ [코어 영역] (LSR, Label Switching Router)
  │     ├─ 코어 LSR (LFIB 기반 초고속 레이블 Swap)
  │     └─ 직전 홉 라우터 (PHP: 송출 LER 부하 경감 선제 제거)
  │
  └─ [32비트 Shim Header 포맷] (2.5계층 헤더)
        ├─ Label ID (20비트: 실제 포워딩 식별자)
        ├─ TC / Exp (3비트: QoS 및 트래픽 클래스)
        ├─ S 비트 (1비트: Bottom of Stack 스택 종료 표시)
        └─ TTL (8비트: 루프 방지 Time To Live)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 인입 LER (Ingress) | 목적지 IP 검사 후 FEC 분류 및 32비트 Shim Header 레이블 삽입(Push) |
| 코어 LSR (Transit) | 하드웨어 LFIB를 참조하여 인입 레이블을 송출 레이블로 고속 교체(Swap) |
| 송출 LER (Egress) | 최종 레이블을 제거(Pop)하여 원본 IP 패킷 복원 후 일반 IP 포워딩 |
| 직전 홉 제거 (PHP) | 송출 LER의 이중 룩업 방지를 위해 직전 홉에서 외곽 레이블 선제 제거 |
| MPLS Shim Header | L2와 L3 사이에 삽입되는 32비트 고속 스위칭 및 QoS 태그 헤더 |

#### 한줄 요약
- 인입 LER만 FEC 판정이라는 비싼 IP 검색을 떠맡고 코어 LSR은 Shim Header 한 장만 교환하므로, 레이블 계층이 홉마다의 L3 룩업 자리를 대신 차지한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MPLS 패킷 전송 5단계**: IP 패킷 인입 $\to$ Ingress LER Label Push $\to$ Core LSR LFIB Swap $\to$ 직전 홉 PHP Pop $\to$ Egress LER IP 복원.

</details>

```text
MPLS LSP 패킷 전달 파이프라인
        │
   1. [패킷 인입 및 FEC 분류] 인입 LER에 IP 패킷 도착 -> 목적지 IP 기반 FEC 매핑
        │
   2. [Label Push] 32비트 MPLS Shim Header(레이블 101)를 L2와 L3 사이에 삽입
        │
   3. [Core LSR LFIB Swap] 코어 라우터가 LFIB 테이블 조회 -> 레이블 101을 202로 교환하여 송출
        │
   4. [직전 홉 PHP Pop] 송출 LER 직전 LSR에서 외곽 레이블 선제 제거 (Label 3 수신)
        │
   5. [Egress LER IP 전달] 잔여 레이블 제거 후 순수 IP 패킷으로 최종 목적지 네트워크 전달
```

#### 한줄 요약
- PHP는 송출 LER에 몰릴 레이블 제거와 IP 룩업의 이중 부하를 직전 홉으로 앞당겨 경로 끝단의 비용을 코어로 분산하며, 그 대가로 경계에서의 레이블 정보는 미리 사라진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MPLS FRR (Fast Reroute)**: 링크 장애 감지 시 50ms 이내에 사전에 계산된 백업 LSP(Bypass Tunnel)로 트래픽을 자동 우회시키는 고가용성 기술.

</details>

| 비교 항목 | MPLS 레이블 스위칭 | 일반 L3 IP 라우팅 (Hop-by-Hop) |
|:---|:---|:---|
| 포워딩 기준 | **고정 20비트 MPLS Label ID 단순 인덱스 조회** | 32비트/128비트 IP 주소 기반 **최장 일치 검색 (LPM)** |
| 패킷 룩업 위치 | **2.5계층 32비트 Shim Header** | 3계층 IP 헤더 내부 (20~60바이트 가변) |
| 트래픽 경로 제어 | **RSVP-TE 기반 명시적 엔지니어링 경로 지정 (TE)** | 메트릭 최단 경로(IGP)로만 트래픽 편중 발생 |
| 장애 복구 시간 | **MPLS Fast Reroute (FRR) 적용 시 50ms 이내 절체** | IGP 재수렴 대기로 수 초~수십 초 소요 |
| 멀티테넌트 격리 | **BGP/MPLS L3VPN (VRF) 기반 완벽한 오버레이 격리** | 일반 IP 라우팅으로는 고객망 간 독립 격리 불가 |

#### 한줄 요약
- LPM 검색 기반 IP 라우팅 대비 고속 포워딩, 트래픽 엔지니어링(TE), 50ms 미만 고속 복구(FRR)를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **MPLS L3VPN (RFC 4364)**: Outer Transport Label과 Inner VPN Label의 2계층 레이블 스택을 사용하여 통신사 단일 물리망에서 다수 기업 고객의 사설 IP 망(VRF)을 완전 격리하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다중 레이블 추가로 인한 기본 MTU(1500B) 초과 및 단편화/패킷 드롭 | **백본 인터페이스 `점보 프레임(MTU 1522B 이상) 및 PMTU 확장`** | 단편화 오버헤드 방지 및 레이블 전송 무결성 보증 |
| 백본 링크 단선 시 라우팅 수렴 지연으로 음성/실시간 트래픽 유실 | **`BFD 연동 MPLS RSVP-TE Fast Reroute(FRR)` 50ms 절체** | 무순단 서브세컨드(Sub-second) 고속 우회 완료 |
| 다수 고객사 간 동일 사설 IP 대역(`192.168.0.0/16`) 사용 시 주소 충돌 | **`MPLS L3VPN (VRF)` 및 `2계층 레이블 스택(Outer + Inner)` 적용** | 통신사 단일 백본 내 완벽한 고객사별 트래픽 격리 |
| 레이블 분배 프로토콜(LDP) 세션 단절로 인한 블랙홀 발생 | **LDP 세션 보호(Session Protection) 및 LDP-IGP Sync 활성화** | 라우팅 경로와 LSP 불일치 원천 방지 |

#### 한줄 요약
- 인터페이스 MTU 확장, BFD/FRR 50ms 절체, VRF 다층 레이블, LDP-IGP 동기화로 운영한다.

## Ⅶ. 결론

- 통신사 코어 백본망과 엔터프라이즈 전용선 서비스(L3VPN/L2VPN)의 인프라 표준으로 오랜 기간 검증되었으며, 최근에는 복잡한 LDP/RSVP-TE 프로토콜 상태 유지를 배제하고 IPv6 확장 헤더를 활용하는 **세그먼트 라우팅(Segment Routing: SR-MPLS / SRv6)으로의 진화와 함께, 50ms 미만 무순단 절체를 위한 MPLS Fast Reroute(FRR), 다중 레이블 추가 시 패킷 드롭을 방지하는 점보 프레임(MTU 1522B 이상) 및 PHP(Penultimate Hop Popping) 최적화**를 결합하여 차세대 캐리어급 SDN 패브릭을 완성

#### 한줄 요약
- MPLS는 2.5계층 32비트 고정 레이블과 LFIB 스위칭을 통해 초고속 전달과 FRR 고속 복구 및 완벽한 VPN 테넌트 격리를 제공하는 백본 핵심 기술이다.
