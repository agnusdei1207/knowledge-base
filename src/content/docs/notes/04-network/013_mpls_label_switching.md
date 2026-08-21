---
sidebar:
  order: 13
  label: "013. 다중 프로토콜 레이블 스위칭: MPLS (Multiprotocol Label Switching)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "다중 프로토콜 레이블 스위칭: MPLS (Multiprotocol Label Switching)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 13
extra:
  question_no: "013"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "2.5계층 고정 길이 레이블 기반 고속 스위칭 및 트래픽 엔지니어링"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **다중 프로토콜 레이블 스위칭(Multiprotocol Label Switching, MPLS)**: IP 패킷 헤더의 목적지 주소를 매번 조회하는 대신, 2계층과 3계층 사이에 삽입된 32비트 고정 길이 레이블(Shim Header)을 기반으로 패킷을 고속 전달하는 2.5계층 스위칭 기술.
- **동등 포워딩 클래스(Forwarding Equivalence Class, FEC)**: 동일한 전달 경로, QoS 및 정책으로 취급되는 패킷들의 집합.
- **레이블 스위치 경로(Label Switched Path, LSP)**: 인입 LER에서 송출 LER까지 레이블 스왑(Swap)을 통해 사전에 수립된 단방향 가상 전송 경로.

</details>

- 정의/개념: L2와 L3 사이에 32비트 **Shim Header(레이블)** 를 삽입하여 IP 룩업 오버헤드를 제거하고 고속 포워딩과 트래픽 엔지니어링(TE)을 지원하는 **2.5계층 스위칭 기술**
- 배경/필요성: 기존 최장 일치 검색(LPM) 기반 IP 라우팅의 처리 지연 완화, 가상 사설망(BGP/MPLS VPN) 서비스 격리 및 명시적 경로 제어(Traffic Engineering) 요구

#### 한줄 요약
- 고정 길이 32비트 레이블을 기반으로 하드웨어 스위칭을 수행하여 고속 포워딩과 VPN 격리를 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **레이블 경계 라우터(Label Edge Router, LER)**: MPLS 도메인의 입출구에 위치하여 IP 패킷을 FEC로 분류하고 레이블을 삽입(Push)하거나 제거(Pop)하는 라우터.
- **레이블 스위칭 라우터(Label Switching Router, LSR)**: MPLS 코어망 내에서 LFIB 테이블을 참조하여 인입 레이블을 송출 레이블로 교환(Swap)하는 고속 스위칭 라우터.
- **레이블 스택(Label Stack)**: 다중 레이블을 중첩(LIFO)하여 전송 경로(Outer Label)와 VPN/서비스 식별(Inner Label)을 동시에 계층화하는 구조.

</details>

- **LER(Ingress/Egress)** 에서 패킷을 FEC로 분류하고 레이블 삽입(Push) 및 제거(Pop) 수행
- 코어망 **LSR** 에서는 3계층 IP 헤더를 검사하지 않고 20비트 Label ID만 교환(Swap)하여 하드웨어 스위칭 가속
- **레이블 스택(Label Stack)** 계층 구조를 통해 BGP/MPLS L3VPN, L2VPN(VPLS) 및 트래픽 엔지니어링(MPLS-TE) 실현

#### 한줄 요약
- 입구 Push, 코어 Swap, 출구 Pop의 3단계 레이블 처리와 다층 레이블 스택 기반 서비스 격리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **레이블 포워딩 정보 베이스(Label Forwarding Information Base, LFIB)**: 인입 인터페이스/레이블과 송출 인터페이스/레이블의 매핑을 저장하는 하드웨어 포워딩 테이블.
- **직전 홉 레이블 제거(Penultimate Hop Popping, PHP)**: 송출 LER의 레이블 팝 오버헤드와 IP 룩업 이중 부하를 줄이기 위해, 직전 LSR에서 외곽 레이블을 미리 제거(Implicit Null, Label 3)하여 전달하는 최적화 메커니즘.

</details>

```text
[ 일반 IP 네트워크 ]                                              [ 일반 IP 네트워크 ]
         │ (IP 패킷)                                                ▲ (IP 패킷 원복)
         ▼                                                          │
┌─────────────────┐        ┌────────────────────┐        ┌─────────────────┐
│   [ 인입 LER ]  │        │    [ 코어 LSR ]    │        │   [ 송출 LER ]  │
│  (Label Push)   │ ─────▶ │    (Label Swap)    │ ─────▶ │   (Label Pop)   │
│  외곽 레이블 삽입│        │   LFIB 기반 레이블 교체│        │   레이블 제거 및 IP 포워딩
└─────────────────┘        └────────────────────┘        └─────────────────┘
```

선의 의미: 인입 LER의 레이블 부착부터 코어 LSR의 레이블 스왑 및 송출 LER의 레이블 제거로 이어지는 LSP 포워딩 구조

| 구성요소 | 책임 | 레이블 연산 |
|:---|:---|:---|
| **인입 LER (Ingress)** | 패킷을 FEC로 분류하고 32비트 MPLS Shim Header를 삽입하여 코어로 전달 | **Push** (레이블 삽입) |
| **코어 LSR (Transit)** | LFIB를 참조하여 인입 레이블을 송출 레이블로 교체하고 다음 홉으로 전달 | **Swap** (레이블 교환) |
| **송출 LER (Egress)** | 최종 레이블을 제거하고 원래의 IP 패킷을 복원하여 목적지 네트워크로 전송 | **Pop** (레이블 제거) |
| **PHP (Penultimate Hop)** | 송출 LER의 이중 룩업 부하를 방지하기 위해 직전 홉에서 최외곽 레이블을 선제 제거 | **PHP Pop** (Label 3) |
| **MPLS Shim Header** | L2 헤더와 L3 헤더 사이에 위치하는 32비트 헤더 (Label, TC/Exp, S, TTL) | 32-bit 포맷 |

#### 한줄 요약
- 인입 LER(Push), 코어 LSR(Swap), 송출 LER(Pop) 및 LFIB를 통해 사전에 수립된 LSP로 고속 전송한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MPLS Shim Header 포맷**: 20비트 Label ID, 3비트 트래픽 클래스(TC/QoS), 1비트 스택 바텀 플래그(S-bit), 8비트 Time To Live(TTL)로 구성된 4바이트 헤더.

</details>

```text
1. IP 패킷 인입 LER 도착 (목적지 IP 기반 FEC 분류)
            │
            ▼
2. Label Push: LIB/LFIB를 참조하여 32비트 MPLS Shim Header 삽입
            │
            ▼
3. 코어 LSR 레이블 스위칭: 인입 레이블을 송출 레이블로 Swap 포워딩
            │
            ▼
4. PHP(직전 홉 LSR) 처리: 외곽 레이블 선제 Pop 수행 (Implicit Null)
            │
            ▼
5. 송출 LER 도착: 잔여 레이블 제거(Pop) 후 순수 IP 패킷으로 목적지 전달
```

**동작 원리**

1. **FEC 매핑**: 인입 LER이 패킷의 목적지 IP를 검사하여 사전에 수립된 FEC 및 LSP 결정
2. **레이블 캡슐화**: 20비트 Label ID와 QoS 정보(Exp)를 포함하는 32비트 Shim Header를 L2-L3 사이에 삽입
3. **고속 레이블 스왑**: 코어 LSR이 하드웨어 LFIB 테이블을 조회하여 패킷의 인입 레이블을 송출 레이블로 교체
4. **PHP 최적화**: 송출 LER 직전의 LSR이 최외곽 레이블을 미리 제거하여 송출 라우터의 룩업 부하 경감
5. **IP 복원 및 송출**: 송출 LER이 원본 IP 헤더를 복원하여 일반 IP 라우팅으로 최종 목적지 전송

#### 한줄 요약
- 인입 LER에서 레이블을 부여하고, 코어 LSR에서 스왑 후 직전 홉 PHP를 거쳐 최종 LER에서 IP로 복원한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MPLS 트래픽 엔지니어링(MPLS-TE)**: RSVP-TE 프로토콜을 사용하여 특정 대역폭과 제약 조건을 만족하는 명시적 경로(Explicit Route)를 동적으로 예약 및 설정하는 기술.
- **BGP/MPLS L3VPN**: 통신사 백본망 내에서 다층 레이블(Outer LSP + Inner VPN Label)을 활용하여 고객사별 가상 라우팅 포워딩 인스턴스(VRF)를 완전 격리하는 VPN 기술(RFC 4364).

</details>

| 비교 항목 | MPLS 스위칭 (Label Switching) | 일반 L3 IP 라우팅 (Hop-by-Hop) |
|:---|:---|:---|
| **포워딩 기준** | 고정 20비트 **MPLS Label ID** 인덱스 조회 | 32비트/128비트 IP 주소 기반 **최장 일치 검색(LPM)** |
| **패킷 룩업 위치** | 2.5계층 32비트 **Shim Header** | 3계층 **IP 헤더** 내부 (20~60바이트) |
| **트래픽 경로 제어** | **RSVP-TE** 기반 명시적/우회 경로 지정 가능 (TE) | 메트릭 최단 경로(IGP)로만 트래픽 편중 발생 |
| **장애 복구 시간** | **MPLS Fast Reroute(FRR)** 적용 시 **50ms 이내 절체** | IGP 수렴 대기로 수 초~수십 초 소요 |

#### 한줄 요약
- LPM 검색 기반 IP 라우팅 대비 고속 포워딩, 트래픽 엔지니어링(TE) 및 50ms 미만 고속 복구(FRR)를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **MPLS 고속 재라우팅(Fast Reroute, FRR)**: 링크 또는 노드 장애 발생 시 사전에 계산된 백업 LSP로 50ms 이내에 트래픽을 즉시 우회시키는 고가용성 보호 기법.
- **경로 최대 전송 단위(Path MTU)**: 32비트 레이블 헤더가 추가됨에 따라 발생하는 패킷 단편화(Fragmentation)를 방지하기 위해 백본 인터페이스의 MTU를 확장하는 튜닝.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다중 레이블 추가로 인한 기본 MTU(1500B) 초과 및 단편화/드롭 | 백본 인터페이스 **점보 프레임(MTU 1522B 이상) 및 PMTU 확장** | 단편화 오버헤드 제거 및 레이블 스택 전송 무결성 보증 |
| 백본 링크/노드 장애 시 IGP 수렴 지연으로 인한 실시간 트래픽 손실 | **BFD(Bidirectional Forwarding Detection)** 및 **RSVP-TE FRR** 결합 | 50ms 이내 서브세컨드(Sub-second) 고속 우회 절체 완료 |
| 다수 고객사 간 동일 사설 IP 대역(`192.168.0.0/16`) 사용 시 주소 충돌 | **MPLS L3VPN(VRF)** 및 **2계층 레이블 스택(Outer + Inner)** 적용 | 통신사 단일 물리망 내 완벽한 고객사별 트래픽/경로 격리 |

#### 한줄 요약
- 인터페이스 MTU 확장, BFD 연계 FRR 50ms 절체, VRF 다층 레이블을 통한 서비스 격리로 안정성을 확보한다.

## Ⅶ. 결론

- 대규모 통신 사업자 백본망 및 엔터프라이즈 인프라에서 고속 스위칭과 다중 테넌트 격리를 위해 **MPLS 기반 L3VPN**을 표준 아키텍처로 채택하되, 실시간 서비스 연속성을 위해 **BFD 연계 Fast Reroute(FRR)** 체계와 경로 MTU 최적화를 필수로 적용하여 고신뢰성 코어망을 구축

#### 한줄 요약
- 2.5계층 레이블 스위칭과 FRR 고속 복구를 통해 고성능 백본 및 안전한 가상 사설망을 실현한다.
