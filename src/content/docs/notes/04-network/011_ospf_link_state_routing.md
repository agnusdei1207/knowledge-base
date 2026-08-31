---
sidebar:
  order: 11
  label: "011. OSPF 링크 상태 라우팅"
  badge:
    text: "기출 · 50%"
    variant: note
title: "OSPF 링크 상태 라우팅 (OSPF Protocol)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 11
extra:
  question_no: "11"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "다익스트라 SPF 알고리즘, LSA/LSDB 동기화, 계층적 Area 및 OSPFv3"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OSPF (Open Shortest Path First)**: IETF 표준 링크 상태(Link-State) 내부 라우팅 프로토콜로, 다익스트라 SPF 알고리즘을 통해 루프 없는 최단 경로 트리를 계산하는 프로토콜.
- **LSA (Link State Advertisement)**: 라우터가 인접 링크의 IP, 대역폭, 이웃 정보를 담아 동일 Area 내로 플러딩하는 링크 상태 패킷.
- **LSDB (Link State Database)**: 수신된 LSA를 취합하여 동일 Area 내 모든 라우터가 동일하게 보유하는 전체 네트워크 토폴로지 지도.

</details>

- 정의/개념: 인접 라우터와 이웃 관계를 수립하고 **LSA 플러딩으로 구축된 LSDB에 다익스트라 SPF 알고리즘을 적용하여 최적 경로를 계산하는 링크 상태 IGP**
- 배경/필요성: 초기 거리 벡터(Distance Vector: RIP) 프로토콜의 홉 수(최대 15홉) 제한, 대역폭을 반영하지 못하는 단순 메트릭, 주기적 전체 라우팅 테이블 브로드캐스팅에 따른 대역폭 낭비 및 링크 장애 시 느린 수렴(Convergence)과 무한 루프(Count-to-Infinity) 취약점을 해결하기 위해, LSA 플러딩으로 동일한 토폴로지 데이터베이스(LSDB)를 공유하고 다익스트라 SPF 알고리즘으로 루프 없는 최단 경로 트리를 독립 연산하는 OSPF(Open Shortest Path First) 프로토콜을 도입하여 **대규모 엔터프라이즈 내부망의 초고속 수렴과 계층적 다중 Area 확장을 통한 라우터 부하 최소화**를 달성할 필요

#### 한줄 요약
- 다익스트라 SPF 알고리즘과 LSA 플러딩 및 계층적 Area 설계를 통해 루프 없는 고속 수렴을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Dijkstra SPF Algorithm**: 전체 네트워크 토폴로지 맵(LSDB)을 기반으로 출발지 라우터에서 모든 목적지까지의 최소 비용 최단 경로 트리를 연산하는 알고리즘.
- **DR / BDR (Designated Router / Backup DR)**: 브로드캐스트 다중 접속망에서 $N(N-1)/2$개의 인접성 폭증을 막고 $2N$개로 집중화하기 위해 선출하는 대표 라우터.

</details>

- 전체 네트워크 지도를 기반으로 최단 트리를 계산하여 **구조적 라우팅 루프 원천 차단**
- 토폴로지 변경 시 증분(Incremental) LSA만 즉시 전송하는 **수 초 이내의 고속 수렴(Fast Convergence)**
- 백본(Area 0)과 서브 영역을 분리하여 라우터 부하를 분산하는 **계층적 다중 영역(Multi-Area) 설계**

#### 한줄 요약
- SPF 루프 방지, 증분 LSA 고속 수렴, 다중 Area 계층 설계를 통해 확장성을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ABR (Area Border Router)**: 백본 Area 0와 일반 Area 사이에 위치하여 영역 간 LSA(Type 3)를 전달하고 경로 요약을 수행하는 경계 라우터.
- **ASBR (Autonomous System Boundary Router)**: BGP 등 외부 라우팅 도메인의 경로를 OSPF 내부로 재분배(Type 5 LSA)하는 자율시스템 경계 라우터.

</details>

```text
[OSPF 구성]
|-- 백본 영역
|-- 영역 경계 라우터
|-- 자율시스템 경계
`-- 지정 라우터
```

선의 의미: 계층 및 모든 일반 Area는 ABR을 통해 중앙 백본 Area 0에 반드시 연결되어야 하는 2계층 허브-앤-스포크 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 백본 영역 (Area 0) | 모든 비백본 영역 간의 트래픽을 중계하는 **중앙 백본 코어로 반드시 연속성(Contiguity) 유지**| 0.0.0.0 |
| 영역 경계 라우터 (ABR) | 서브 영역의 프리픽스를 요약(**Type 3 Summary LSA**)하여 Area 0로 전파 | Area 0 연동 필수 |
| 자율시스템 경계 (ASBR) | 외부 프로토콜(BGP) 경로를 OSPF 도메인 내부로 재분배(**Type 5 External LSA**) 주입 | 외부 게이트웨이 |
| 지정 라우터 (DR / BDR) | 브로드캐스트 망에서 **인접성 세션 폭증을 차단하고 LSA 플러딩 동기화 집중 중계** | 멀티캐스트 `224.0.0.6` |

#### 한줄 요약
- DR/BDR은 브로드캐스트 세그먼트에 대표 중계를 끼워 넣어 인접성 수를 $N(N-1)/2$에서 $2N$으로 낮추고, ABR은 영역 경계에서 프리픽스를 요약해 모든 라우터가 전 도메인 토폴로지를 떠안던 비용을 걷어낸다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OSPF 상태 머신**: Down $\to$ Init $\to$ 2-Way (DR/BDR 선출) $\to$ ExStart $\to$ Exchange (DBD 교환) $\to$ Loading (LSR/LSU 동기화) $\to$ Full (인접성 완성).

</details>

```text
OSPF 인접성 수립 및 SPF 라우팅 계산
        │
   1. [이웃 발견 (Hello)] 멀티캐스트(`224.0.0.5`) 헬로 패킷 교환 및 타이머/인증 검증 (2-Way)
        │
   2. [DR/BDR 선출 및 마스터 협상] 브로드캐스트 망에서 DR 선출 및 DBD 교환 시작 (ExStart)
        │
   3. [토폴로지 목차 교환 (Exchange)] DBD(Database Description) 패킷을 교환하여 LSA 목차 대조
        │
   4. [상세 LSA 동기화 (Loading)] 누락된 LSA에 대해 LSR(요청) 발송 -> LSU(갱신) 수신 -> LSAck 응답
        │
   5. [Full Adjacency & SPF 계산] 모든 라우터의 LSDB 동기화 완료 -> 다익스트라 SPF 최단 경로 트리 산출
```

#### 한줄 요약
- 브로드캐스트 망에서는 DR/BDR을 세워 인접성 수를 접은 뒤에야 LSA 동기화에 들어가므로, 초기 선출 협상 비용을 더 치르는 대신 이후 플러딩 트래픽을 상시 절감한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OSPFv2 (RFC 2328)** vs **OSPFv3 (RFC 5340)**: IPv4 전용 프로토콜과 IPv6/IPv4 멀티 어드레스 패밀리를 지원하는 차세대 표준.

</details>

| 비교 항목 | OSPFv2 (IPv4) | OSPFv3 (IPv6 / Multi-AF) |
|:---|:---|:---|
| 지원 프로토콜 체계 | **IPv4 전용 (32비트 주소)** | **IPv6 기본 지원 및 Address Family 확장을 통한 IPv4 지원**|
| 토폴로지와 주소 결합 | LSA 내에 **라우터 링크와 IPv4 주소가 결합** | **토폴로지(LSA 1/2)와 IPv6 주소(LSA 9)를 완전 분리** |
| 이웃 식별 방식 | 인터페이스 IPv4 서브넷 기반 | **인터페이스 링크-로컬 주소(`fe80::/10`) 기반** |
| 자체 보안 인증 | OSPF 패킷 헤더 내 자체 인증 (MD5/HMAC) | **네트워크 계층 표준 IPsec (AH / ESP)에 보안 위임** |
| 인스턴스 다중화 | 단일 인터페이스당 단일 인스턴스 | 단일 물리 인터페이스에서 **복수 OSPF 인스턴스 운용** |

#### 한줄 요약
- OSPFv2는 IPv4 결합형이며, OSPFv3는 주소와 토폴로지를 분리하고 IPsec 보안을 활용하는 차세대 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Virtual-Link (가상 링크)**: 물리적으로 Area 0에 직접 연결되지 못한 분리된 영역을 Transit Area를 통과하는 가상 터널로 연결해 주는 임시 구제 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 영역이 백본 Area 0와 물리적으로 단절되어 영역 간 라우팅 실패 | **Transit Area를 경유하는 `가상 링크(Virtual-Link)` 터널링 구성** | Area 0 연속성 복원 및 정상 통신 보장 |
| 라우터 간 MTU 불일치로 인해 DBD 교환 단계(ExStart/Exchange) 정체 | **인터페이스 `MTU 값 일치` 또는 `ip ospf mtu-ignore` 설정** | 인접성 수립 멈춤 해소 및 Full 상태 전이 |
| 대규모 네트워크에서 빈번한 링크 플래핑(Flapping)으로 SPF 연산 폭증 | **`SPF Throttle 타이머 (spf-start / hold / max)` 점진 지연 설정** | 라우터 CPU 보호 및 네트워크 안정화 |
| 라우터 장애 감지 지연(Dead Timer 40초)으로 인한 트래픽 유실 | **`BFD (Bidirectional Forwarding Detection)` 서브세컨드 연동** | 50ms 이내 초고속 장애 감지 및 페일오버 |

#### 한줄 요약
- Virtual-Link 구제, MTU 일치, SPF 쓰로틀링, BFD 초고속 연동으로 운영한다.

## Ⅶ. 결론

- 기업 인트라넷, 데이터센터 패브릭 및 캠퍼스 백본망에서 가장 널리 활용되는 **표준 링크 상태 내부 게이트웨이 프로토콜(IGP)의 사실상 표준**으로 자리잡았으며, 실무 구축 시에는 **Area 0 중심의 계층적 영역 분할과 ABR 경로 요약(Type 3 LSA), 브로드캐스트 망 내 DR/BDR 선출 최적화, 링크 플래핑 시 CPU를 보호하는 SPF Throttle 타이머 튜닝, 50ms 이내 초고속 장애 감지를 위한 BFD(Bidirectional Forwarding Detection) 연동, IPv6 환경을 위한 OSPFv3 전환**을 결합하여 고신뢰 엔터프라이즈 코어 네트워크를 완성

#### 한줄 요약
- OSPF는 다익스트라 SPF 알고리즘과 계층적 다중 Area 설계를 통해 루프 없는 고속 수렴을 제공하는 핵심 내부 게이트웨이 라우팅 기술이다.
