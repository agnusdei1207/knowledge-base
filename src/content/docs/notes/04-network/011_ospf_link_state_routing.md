---
sidebar:
  order: 11
  label: "011. 링크 상태 라우팅: OSPF (OSPF Link State Routing)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "링크 상태 라우팅 프로토콜 : OSPF 및 OSPFv3 (OSPF Protocol)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 11
extra:
  question_no: "011"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "다익스트라 SPF 알고리즘, LSA/LSDB 동기화, 계층적 Area 및 OSPFv3"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OSPF(Open Shortest Path First)**: IETF 표준 링크 상태(Link-State) 기반 내부 게이트웨이 라우팅 프로토콜(IGP)로, 다익스트라(Dijkstra) SPF 알고리즘을 사용하여 루프 없는 최단 경로 트리를 계산하는 프로토콜.
- **링크 상태 광고(Link State Advertisement, LSA)**: 라우터가 자신의 인접 링크 상태(인터페이스 IP, 서브넷 마스크, 비용, 이웃 라우터 등)를 기술하여 동일 Area 내로 플러딩하는 L3 제어 패킷.
- **링크 상태 데이터베이스(Link State Database, LSDB)**: 수신된 모든 LSA를 취합하여 동일 Area 내 모든 라우터가 100% 동일하게 공유하는 전체 네트워크 토폴로지 맵.

</details>

- 정의/개념: 인접 라우터와 헬로 패킷으로 이웃(Neighbor/Adjacency)을 수립하고, **LSA 플러딩**을 통해 구성된 **LSDB** 에 **다익스트라 SPF 알고리즘**을 적용하여 루프 없는 최단 경로 트리를 계산하는 **링크 상태 라우팅 프로토콜(OSPF)**
- 배경/필요성: 거리 벡터(Distance Vector) 프로토콜(RIP)의 15홉 제한, 느린 수렴 속도(Count-to-Infinity) 및 라우팅 루프 취약점을 극복하고 대규모 엔터프라이즈망의 고속 수렴을 실현할 요구

#### 한줄 요약
- LSA 플러딩으로 완전한 토폴로지 맵(LSDB)을 구축하고 다익스트라 SPF 알고리즘으로 최단 경로를 산출한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **계층적 영역 구조(Hierarchical Area)**: 네트워크를 중심 백본 영역(Area 0)과 복수의 비백본 영역(Non-backbone Area)으로 분할하여 LSA 플러딩 범위와 SPF 재계산 부하를 국소화하는 아키텍처.
- **플러딩(Flooding)**: 링크 상태 변화가 감지되었을 때 해당 LSA를 수신 포트를 제외한 모든 활성 인터페이스로 즉각 브로드캐스트/멀티캐스트하여 신속히 전파하는 메커니즘.

</details>

- **다익스트라 SPF 기반 루프 방지**: 전체 망 토폴로지 트리를 계산하므로 홉 수 기반 거리 벡터 프로토콜과 달리 구조적 라우팅 루프 원천 차단
- **고속 수렴(Fast Convergence)**: 토폴로지 변경 시 주기적 전체 테이블 전송 대신 증분(Incremental) LSA만 즉시 플러딩하여 수 초 내 수렴
- **계층적 다중 영역(Multi-Area)**: **Area 0(백본)** 과 서브 영역을 분리하여 라우터의 SPF 연산 부하 및 LSDB 메모리 점유 최소화

#### 한줄 요약
- SPF 알고리즘 루프 방어, 증분 LSA 플러딩 기반 고속 수렴, 계층적 다중 Area 설계를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **영역 경계 라우터(Area Border Router, ABR)**: 백본 영역(Area 0)과 일반 영역 사이에 위치하여 영역 간 LSA(Type 3)를 전달하고 경로 요약(Summarization)을 수행하는 라우터.
- **자율 시스템 경계 라우터(Autonomous System Boundary Router, ASBR)**: OSPF 도메인 외부의 다른 프로토콜(BGP, RIP, 정적 경로)을 OSPF 내부로 재분배(Type 5 LSA)하는 경계 라우터.

</details>

```text
[ OSPF 계층적 다중 영역 토폴로지 ]

 [ 일반 영역 (Area 1) ]           [ 백본 영역 (Backbone Area 0) ]         [ 일반 영역 (Area 2) ]
 ┌────────────────────┐          ┌─────────────────────────────┐         ┌────────────────────┐
 │ 내부 라우터 (IR)   │          │ 코어 백본 라우터 (BR)       │         │ 내부 라우터 (IR)   │
 └─────────┬──────────┘          └──────────────┬──────────────┘         └─────────┬──────────┘
           │                                    │                                  │
           └──────────────────▶ [ ABR 라우터 ] ◀┴────────────────▶ [ ABR 라우터 ] ◀┘
                                        │
                                        ▼ (외부 BGP/Static 재분배)
                                  [ ASBR 라우터 ] ──▶ 외부 네트워크
```

선의 의미: 모든 일반 영역(Area 1, 2)은 ABR을 통해 반드시 중앙 백본(Area 0)과 직결되어야 하는 2계층 계층 토폴로지

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| **백본 영역 (Area 0)** | 모든 비백본 영역 간의 트래픽을 중계하는 중앙 백본 코어 | 0.0.0.0 |
| **영역 경계 라우터 (ABR)** | 서브 영역의 프리픽스를 요약(Type 3 Summary LSA)하여 Area 0로 전파 | Area 0 연동 필수 |
| **자율 시스템 경계 (ASBR)** | 외부 경로를 OSPF 도메인 내부로 재분배(Type 5 External LSA) 주입 | 재분배 게이트웨이 |
| **지정 라우터 (DR / BDR)** | 브로드캐스트 다중 접속망에서 $N(N-1)/2$ 개의 인접 관계 폭증을 방지하고 LSA 동기화 집중 | 멀티캐스트 `224.0.0.6` |

#### 한줄 요약
- Area 0 백본, ABR 영역 경계, ASBR 외부 경계, DR/BDR이 결합하여 계층적 OSPF 도메인을 완성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **데이터베이스 기술(Database Description, DBD)**: 인접성 수립 시 자신이 보유한 LSDB 내 모든 LSA의 헤더 목록만을 요약하여 상대방에게 전달하는 패킷.
- **링크 상태 요청(LSR) / 갱신(LSU)**: DBD 대조 후 누락되거나 구버전인 LSA의 상세 정보를 요청(LSR)하고 이에 응답하여 완전한 LSA를 전송(LSU)하는 절차.

</details>

```text
1. 헬로 패킷(Hello) 교환 ➔ 파라미터(Area ID, Hello/Dead Timer, 인증) 검증 ➔ 2-Way 상태 수립
            │
            ▼
2. 마스터/슬레이브 선출(ExStart) ➔ DBD 패킷 교환(Exchange): LSDB 요약 목차 비교
            │
            ▼
3. 누락된 LSA에 대해 LSR(요청) 전송 ➔ LSU(갱신) 수신 및 LSAck(확인) 반환 (Loading 상태)
            │
            ▼
4. 모든 라우터의 LSDB 동기화 완료 (Full Adjacency 상태) ➔ SPF 알고리즘 가동 및 FIB 설치
```

**동작 원리**

1. **이웃 발견**: 멀티캐스트(`224.0.0.5`)로 헬로 패킷을 교환하여 동일 서브넷 내 라우터 식별
2. **인접성 협상**: DR/BDR을 선출하고 DBD 패킷을 통해 보유 중인 LSA 식별자 목록 대조
3. **토폴로지 동기화**: 자신에게 없는 LSA를 LSR로 요청하고 상대방이 LSU로 최신 LSA를 송출하여 LSDB 일치
4. **최단 경로 트리 산출**: 다익스트라 SPF 알고리즘을 수행하여 루프 없는 최적 넥스트홉을 FIB에 프로그래밍

#### 한줄 요약
- Hello 이웃 수립, DBD 목차 교환, LSR/LSU 동기화, SPF 최단 경로 트리 산출 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **링크-로컬 주소(Link-Local Address)**: IPv6에서 동일 링크 상의 인접 노드 간 통신만을 위해 사용되는 주소(`fe80::/10`)로, OSPFv3의 넥스트홉 및 이웃 식별에 활용.

</details>

| 비교 항목 | OSPFv2 (RFC 2328) | OSPFv3 (RFC 5340) |
|:---|:---|:---|
| **지원 프로토콜** | **IPv4 전용 (32비트)** | **IPv6 기본 지원 및 IPv4 주소 패밀리(Multi-AF) 확장** |
| **토폴로지/주소 분리** | LSA 내에 라우터 연결 정보와 **IPv4 주소가 결합** | **토폴로지(LSA 1/2)와 IPv6 Prefix(LSA 9)를 완전 분리** |
| **이웃 식별 방식** | 인터페이스 IPv4 서브넷 기반 | **인터페이스 링크-로컬 주소(`fe80::`) 기반** |
| **인증 메커니즘** | OSPF 패킷 헤더 내 자체 인증 (MD5/SHA) | **네트워크 계층 표준 IPsec(AH/ESP) 프로토콜에 위임** |
| **다중 인스턴스 지원** | 단일 링크당 단일 OSPF 인스턴스 | 단일 물리 인터페이스에서 **복수 OSPF 인스턴스 운용** |

#### 한줄 요약
- OSPFv2는 IPv4 결합형이며, OSPFv3는 토폴로지와 주소를 분리하고 IPsec 보안을 활용하는 차세대 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **가상 링크(Virtual-Link)**: 물리적으로 Area 0에 직접 연결되지 못한 분리된 영역(Area)을 중간 비백본 Area를 터널링하여 논리적으로 Area 0에 직결시키는 임시 구제 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네트워크 분할로 인해 특정 영역이 백본(Area 0)과 물리적으로 단절 | 전과 구역(Transit Area)을 경유하는 **가상 링크(Virtual-Link)** 구성 | Area 0 연속성 복원 및 영역 간 정상 라우팅 회복 |
| 라우터 간 MTU 불일치로 인해 DBD 교환 단계(ExStart/Exchange) 정체 | 양단 인터페이스 **MTU 값 통일** 또는 `ip ospf mtu-ignore` 설정 | 인접성 수립 멈춤 현상 해소 및 Full 상태 전이 |
| 다중 접속(Broadcast) 세그먼트 내 LSA 플러딩 폭증 및 CPU 부하 | **지정 라우터(DR / BDR)** 선출 및 우선순위(Priority) 조정 | 인접성 세션 수($N \rightarrow 2$) 축소 및 LSA 교환 효율화 |

#### 한줄 요약
- Virtual-Link로 백본 단절을 구제하고, MTU 일치로 인접성 정체를 방지하며, DR/BDR로 LSA 폭증을 억제한다.

## Ⅶ. 결론

- 대규모 엔터프라이즈 및 데이터센터 내부망 라우팅은 **OSPF** 의 계층적 **Area 0 백본 설계**와 **경로 요약(Summarization)** 을 표준으로 적용하여 SPF 연산 오버헤드를 통제하고, 차세대 듀얼스택 인프라 환경에서는 토폴로지와 주소가 분리된 **OSPFv3** 와 **IPsec 보안 체계**를 통합 구축하여 네트워크 확장성과 가용성을 완성

#### 한줄 요약
- 계층적 Area 분할과 OSPFv3 표준을 결합하여 고성능·고가용성 내부 라우팅 인프라를 확립한다.
