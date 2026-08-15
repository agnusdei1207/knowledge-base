---
sidebar:
  order: 12
  label: "012. 경계 게이트웨이 프로토콜 (BGP)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "경계 게이트웨이 프로토콜 (Border Gateway Protocol, BGP)"
date: "2026-08-13T16:25:00+09:00"
tags:
  - "notes-network"
weight: 12
extra:
  question_no: "012"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "설계•보안형: EVPN•RPKI의 기반 BGP 정책"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **경계 게이트웨이 프로토콜(Border Gateway Protocol, BGP)**: 전 세계 인터넷을 구성하는 자율 시스템(AS) 간에 서브넷 도달 가능성 정보와 라우팅 정책 경로를 교환하는 패스 벡터(Path-Vector) 방식의 외부 라우팅 프로토콜(EGP).
- **자율 시스템(Autonomous System, AS)**: 하나의 단일 관리 주체(ISP, 대기업 등)에 의해 통합 제어되는 고유한 AS 번호(ASN)를 가진 IP 네트워크 집합.
- **네트워크 계층 도달 가능성 정보(Network Layer Reachability Information, NLRI)**: BGP 패킷의 UPDATE 메시지에 포함되어 전파되는 IP 프리픽스(Prefix) 및 서브넷 마스크 정보.
- **내부 게이트웨이 프로토콜(Interior Gateway Protocol, IGP)**: OSPF, IS-IS와 같이 단일 AS 내부의 최단 경로를 구하는 라우팅 프로토콜.

</details>

- 정의/개념: AS 간 도달성과 정책 경로를 교환하는 **BGP**
- 배경/필요성: IGP 최단 경로만으로는 **AS 간 정책 통제 불가**

#### 한줄 요약

- AS 간 NLRI와 경로 속성 기반 정책 라우팅

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **자율 시스템 경로(Autonomous System Path, AS_PATH)**: 목적지 IP 프리픽스에 도달하기 위해 거쳐온 AS 번호들의 목록을 담은 BGP 필수 속성으로, 라우팅 루프 방지(자신의 AS 포함 시 폐기)에 활용됨.
- **증분 갱신(Incremental Update)**: 초기 인접 세션 형성에만 전체 BGP 라우팅 테이블을 전송하고, 이후에는 토폴로지 변경/철회(Withdraw)된 경로만 부분 송신하는 방식.

</details>

- 신뢰성 있는 패킷 전송을 위해 TCP 프로토콜(Port 179) 기반의 세션(Peer) 연결 수립.
- **자율 시스템 경로(Autonomous System Path, AS_PATH)** 속성을 참조하여 자신이 속한 AS 번호 포함 시 패킷을 즉시 폐기함으로써 루프 방지.
- **증분 갱신(Incremental Update)** 및 Keepalive 패킷을 사용하여 대규모 인터넷 라우팅 테이블 전송 시 대역폭 손실 극소화.

#### 한줄 요약

- AS_PATH 루프 방지와 증분 경로 정책 갱신


## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **BGP 피어(BGP Peer / Neighbor)**: TCP 179번 포트를 통해 1:1로 BGP 세션을 정상적으로 수립하고 라우팅 정보를 상호 교환하는 인접 라우터.
- **업데이트 메시지(UPDATE Message)**: 새로운 도달 경로(NLRI + Path Attributes)를 광고하거나 더 이상 유효하지 않은 경로(Withdrawn Routes)를 통보하는 BGP 핵심 제어 패킷.
- **최선 경로(Best Path)**: 수신된 수많은 BGP 후보 경로 중 BGP 경로 결정 알고리즘(Best Path Selection Algorithm)에 의해 최종 선택되어 RIB/FIB에 탑재되는 경로.

</details>

```text
[ BGP Peer A (AS 65001) ] <--- TCP 179 Session ---> [ BGP Peer B (AS 65002) ]
           |                                                      |
           +---> 1. Inbound Policy (Filter & Attribute Mod) ------+
           |
           +---> 2. BGP Table (Candidate Routes)
           |
           +---> 3. Best Path Selection (Weight > LOCAL_PREF > AS_PATH > MED...)
           |
           +---> 4. Outbound Policy (Filter & Attribute Mod)
           |
           v
[ RIB / FIB Forwarding Table Installation ]
```

*Inbound Policy, BGP Table, Best Path Selection 및 Outbound Policy의 단계적 제어 구조.*

| 구성요소 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|
| **BGP Peer (Neighbor)** | Open, Keepalive 패킷으로 TCP 179 세션 및 FSM(Finite State Machine) 상태 유지 | Established 상태 필수 |
| **Path Attributes** | Weight(Cisco), LOCAL_PREF, AS_PATH, Origin, MED, Community 등 | 최적 경로 판단의 기준 |
| **Inbound Policy** | 수신된 경로 중 허용/거부(Prefix-list) 및 속성 변경(Route-map) 수행 | 유입 경로 통제 |
| **Best Path Selector** | 10단계 이상의 정밀한 BGP 최적 경로 결정 알고리즘 집행 | 단일 최적 경로 선발 |
| **Outbound Policy** | 상대 Peer에게 이 경로를 전파할지 여부 및 속성 수정 통제 | 유출 경로 통제 |

#### 한줄 요약

- TCP 179 피어와 UPDATE 기반 최선 경로 결정

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **수신 정책(Inbound Policy)**: 상대 BGP Peer로부터 수신된 UPDATE 패킷 내 IP 프리픽스를 수용할지 검증하고 LOCAL_PREF 등의 속성을 변경하는 정책.
- **선택 정책(Selection Policy)**: BGP Table에 모인 여러 라우팅 경로 중 우선순위 알고리즘 규칙에 따라 단일 최선의 경로(Best Path)를 선발하는 정책.
- **광고 정책(Outbound Policy)**: 최선 경로로 확정된 NLRI를 외부 Peer에게 유출 광고할 것인지 통제하는 정책.
- **수신 정책 검증(Inbound Policy Verification)**: RPKI 기원 검증 및 Prefix-list 대조를 통한 수신 트래픽 튜닝.
- **후보 경로 등록(Candidate Route Registration)**: 수신 검증을 통과한 경로들을 BGP Table 메모리에 적재하는 과정.
- **최선 경로 선택(Best Path Selection)**: Weight > LOCAL_PREF > Local Originated > AS_PATH > Origin > MED 순의 룰베이스 알고리즘 연산.
- **광고 정책 검증(Outbound Policy Verification)**: eBGP/iBGP 전파 규칙 준수 여부 점검 후 UPDATE 패킷 최종 송출.

</details>

```text
[ UPDATE 패킷 수신 ]
         |
         v
[ 1. 수신 정책 검증 (Inbound Policy) ] ----> Prefix-list / RPKI 검증 (부적합 시 Drop)
         |
         v
[ 2. 후보 경로 등록 (BGP Table) ] ---------> 수용된 경로 및 Path Attribute 저장
         |
         v
[ 3. 최선 경로 선택 (Best Path Selection) ] -> 1) Highest Weight (Cisco)
         |                                  2) Highest LOCAL_PREF
         v                                  3) Shortest AS_PATH
[ 4. 광고 정책 검증 (Outbound Policy) ] ---> 4) Lowest MED ... 
         |                                  (최선 경로 선발 및 FIB 등록)
         v
[ UPDATE 패킷 전파 (To Neighbors) ]
```

### 동작 원리

1. **수신 정책 검증**: 프리픽스•RPKI 적합성 검사
2. **후보 경로 등록**: 허용 경로와 속성을 BGP 표에 저장
3. **최선 경로 선택**: 정책 속성 순서로 경로 판정
4. **광고 정책 검증**: 허용 경로만 이웃에 전파

#### 한줄 요약

- 수신 필터•최선 경로 선택•광고 정책 적용

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **외부 BGP(External Border Gateway Protocol, eBGP)**: 서로 다른 AS 번호를 가진 라우터 간에 맺는 BGP 세션 (TTL 기본 1).
- **내부 BGP(Internal Border Gateway Protocol, iBGP)**: 동일한 AS 번호 내부 라우터 간에 외부 BGP 경로 정보를 반사/공유하기 위해 맺는 BGP 세션 (TTL 기본 255).
- **경로 반사기(Route Reflector, RR)**: iBGP의 Full-Mesh 세션 한계($N*(N-1)/2$)를 극복하기 위해, iBGP 수신 경로를 타 iBGP 클라이언트에게 재광고해주는 대표 라우터.

</details>

| 비교 항목 | **eBGP (External BGP)** | **iBGP (Internal BGP)** |
|:---|:---|:---|
| AS 세션 범위 | 서로 다른 AS 간 라우터 연결 | 동일한 AS 내부 라우터 연결 |
| AS_PATH 속성 갱신 | 패킷 송출 시 자신의 AS 번호를 AS_PATH에 추가 | AS_PATH를 변경하지 않고 그대로 전달 |
| Split-Horizon 규칙 | 미적용 (AS_PATH로 루프 체크) | 적용 (iBGP로 받은 경로는 타 iBGP로 재광고 금지) |
| 연결 확장성 방안 | eBGP Multihop 설정 | **경로 반사기(Route Reflector)** 또는 BGP Confederation 도입 |

> 요약: 다른 자율 시스템과의 연결을 담당하는 eBGP와 AS 내부로 외부 경로를 투명하게 유통시키는 iBGP/Route Reflector 구조.

#### 한줄 요약

- AS 간 eBGP와 AS 내부 iBGP•경로 반사기

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **자원 공개키 기반구조(Resource Public Key Infrastructure, RPKI)**: BGP Route Hijacking(경로 탈취)을 방지하기 위해, 특정 IP 프리픽스를 광고할 권한이 정당한 기원 AS(Origin AS)에 있는지 암호학적으로 검증하는 자원 인증 기술.
- **프리픽스 필터(Prefix Filter)**: 사설 IP 대역(RFC 1918) 및 비인가 대역(Bogon IP)이 외부 BGP로 유출되거나 유입되지 않도록 서브넷 리스트로 통제하는 기능.
- **로컬 선호도(Local Preference, LOCAL_PREF)**: AS 내부 라우터들이 외부로 나가는 아웃바운드 트래픽의 출구 라우터를 결정할 때 최우선 반영하는 BGP 속성(값이 높을수록 우선).

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| BGP Route Hijacking (경로 탈취) | 악의적 라우터가 위조된 IP Prefix/AS_PATH를 광고 | **RPKI(ROA 검증)** 도입 및 Strict Prefix Filtering | 위조 BGP 경로 수용 원천 차단 |
| BGP Route Leak (경로 유출) | Transit 서드파티 경로를 비의도적으로 외부 전파 | BGP Community 태깅 기반 Outbound Filter 설정 | 비의도적 패킷 중계(트랜짓) 차단 |
| Outbound 트래픽 쏠림 | 멀티홈 ISP 라우터 간 아웃바운드 경로 미지정 | **LOCAL_PREF** 속성을 선호 ISP 방향에 높게 부여 | 아웃바운드 회선 대역폭 최적화 |

#### 한줄 요약

- RPKI•프리픽스 필터•경로 속성으로 정책 통제

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **경로 유출 방지(Route Leak Prevention)**: RPKI 기원 검증과 BGP Community 기반 정책 통제를 통해 오광고된 경로의 무단 전파를 차단하는 활동.
- **경로 정책 결정(Routing Policy Selection)**: 아웃바운드는 LOCAL_PREF로, 인바운드는 AS_PATH Prepending 및 MED 속성 튜닝으로 트래픽 흐름을 주도하는 전략.

</details>

- 수신은 **RPKI**, 송신은 **프리픽스 필터**로 유출 차단

#### 한줄 요약

- 트래픽 방향에 따라 LOCAL_PREF•AS_PATH 정책 결정
