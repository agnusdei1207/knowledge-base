---
sidebar:
  order: 11
  label: "011. 링크 상태 라우팅: OSPF•OSPFv3 (OSPF Link State Routing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "링크 상태 라우팅: OSPF•OSPFv3 (OSPF Link State Routing)"
date: "2026-08-13T16:23:00+09:00"
tags:
  - "notes-network"
weight: 11
extra:
  question_no: "011"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "설명•운영형: 137회 OSPFv3 직접 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **최단 경로 우선 개방형 프로토콜(Open Shortest Path First, OSPF)**: 인터넷 상에서 널리 활용되는 링크 상태(Link-State) 방식의 대표적인 개방형 내부 라우팅 프로토콜(IGP).
- **내부 게이트웨이 프로토콜(Interior Gateway Protocol, IGP)**: 단일 자율 시스템(Autonomous System, AS) 내부 네트워크의 라우팅 정보를 교환하기 위해 사용되는 프로토콜.
- **링크 상태 광고(Link-State Advertisement, LSA)**: 라우터 자신의 이더넷/시리얼 링크 상태, 인터페이스 IP, 서브넷 마스크 및 코스트(Cost) 정보를 동일 영역에 브로드캐스트/멀티캐스트로 전파하는 알림 패킷.
- **링크 상태 데이터베이스(Link-State Database, LSDB)**: 영역 내 라우터들이 전파받은 LSA 패킷을 종합하여 동일하게 유지하는 전체 네트워크 토폴로지 데이터베이스.
- **최단 경로 우선 알고리즘(Shortest Path First Algorithm, SPF)**: 다익스트라(Dijkstra) 알고리즘을 기반으로 LSDB 토폴로지를 연산하여 자신을 루트(Root)로 하는 최단 경로 트리를 생성하는 알고리즘.

</details>

- 정의/개념: LSA와 SPF로 최단 경로를 계산하는 **OSPF**
- 배경/필요성: RIP의 15홉 제한과 느린 수렴으로 **대규모망 대응 불가**

#### 한줄 요약

- LSDB 동기화와 다익스트라 SPF 경로 계산

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **영역(Area)**: LSA Flooding 및 SPF 연산 범위를 논리적으로 그룹화하여 네트워크 부하를 분산시키는 계층적 영역 단위.
- **플러딩(Flooding)**: 수신한 LSA 메시지를 자신이 수신한 포트를 제외한 영역 내 모든 OSPF 라우터 포트로 즉시 복사 유포하는 메커니즘.

</details>

- **영역** 단위를 정의하는 계층적 라우팅 아키텍처 적용으로 대규모 망에서의 SPF 재연산 부하 최소화.
- 토폴로지 변경 발생 시 해당 LSA를 **플러딩**하여 수 초 이내의 획기적인 고속 라우팅 수렴(Fast Convergence) 달성.
- 링크 대역폭(Bandwidth) 기반의 코스트(Cost = $10^8 / 대역폭$) 메커니즘을 적용하여 최적 전송 경로 선택.

#### 한줄 요약

- 다중 영역과 LSA 플러딩으로 고속 수렴


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **헬로 패킷(Hello Packet)**: 인접 라우터 간 OSPF 이웃(Neighbor) 관계를 맺고 생존(Keepalive) 여부를 주기적으로 확인하기 위해 송수신하는 패킷 (멀티캐스트 224.0.0.5).
- **인접 관계(Adjacency)**: 헬로 매개변수가 일치하여 상호간 LSA를 교환하고 LSDB를 동기화하는 OSPF 라우터 간의 정식 상태.
- **영역 경계 라우터(Area Border Router, ABR)**: 백본 영역(Area 0)과 일반 영역(Non-Zero Area)을 동시에 연결하여 영역 간 경로 정보를 중계 및 요약하는 라우터.
- **경로 요약(Route Summarization)**: ABR에서 하위 영역의 세부 LSA(Type 1/2)를 상위 영역으로 넘길 때 단일 서브넷 프리픽스(Type 3 LSA)로 요약하여 전달하는 기술.

</details>

```text
[ Area 1 (Standard) ]           [ Area 0 (Backbone Area) ]          [ Area 2 (Stub Area) ]
+-------------------+           +-----------------------+           +-------------------+
| Router A          |           | Core Router C         |           | Router E          |
| Router B          |           | Core Router D         |           | Router F          |
+-------------------+           +-----------------------+           +-------------------+
          \                                /                                 /
           \                              /                                 /
          +-----------------------------------------------------------------+
          |            ABR (Area Border Router) : Route Summarization       |
          +-----------------------------------------------------------------+
```

*계층형 Multi-Area 및 백본 Area 0 중심의 ABR 경로 요약 구조.*

| 구성요소 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|
| OSPF Neighbor / Adjacency | **헬로 패킷**을 이용해 Hello/Dead Interval, Area ID, Subnet 일치 검증 후 Adjacency 형성 | 2-Way -> Full State 전이 |
| LSA (Link State Adv) | Type 1(Router), Type 2(Network), Type 3(Summary), Type 5(External) 등 타입별 LSA 정보 유포 | 영역별 LSA 분리 통제 |
| LSDB | 영역 내 모든 라우터가 100% 동일하게 공유하는 완벽한 네트워크 맵 토폴로지 DB | 모듈별 메모리 관리 |
| ABR (Area Border Router) | Area 0과 서브 Area 간 경계에서 LSA Filtering 및 **경로 요약** 집행 | 백본 연동 필수 |
| ASBR (AS Boundary Router) | 외부 타 라우팅 프로토콜(BGP, RIP, Static) 경로를 OSPF 내부로 재분배(Type 5 LSA) | 외부 경로 주입기 |

#### 한줄 요약

- Hello 인접 형성과 ABR 경로 요약

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **데이터베이스 동기화(Database Synchronization)**: 이웃 라우터 간 DBD(Database Description) 패킷과 LSR/LSU 패킷을 통해 최신 LSDB 상태를 동일하게 일치시키는 단계.
- **최선 경로 설치(Best Route Installation)**: 완벽히 동기화된 LSDB상에서 다익스트라(Dijkstra) 알고리즘을 연산하여 최적 경로를 RIB/FIB 포워딩 테이블에 인스톨하는 단계.
- **데이터베이스 요약(Database Description, DBD)**: 이웃 라우터에게 자신이 소유한 LSA의 요약 목록(Header)만을 전달하여 서로 간의 갭을 확인하는 패킷.
- **요청 LSA(Link State Request, LSR)**: 상대 라우터의 DBD 수신 후 자신에게 없거나 구버전인 LSA의 상세 정보를 요구하는 패킷.
- **수신 LSA(Link State Update, LSU)**: 상대방의 LSR 요구에 대한 답변으로 실제 상세 LSA 정보를 담아 플러딩해주는 패킷.

</details>

```text
[ Hello Packet 교환 ] -------> 이웃 파라미터 검증 (Area ID, Authentication, Hello/Dead Time)
          |
          v
[ 1. DBD 교환 (Database Description) ] -> 자신이 가진 LSA Header 요약 목록 상호 교환
          |
          v
[ 2. LSR 전송 (Link State Request) ] ---> 누락되거나 구버전인 LSA의 상세 정보 요구
          |
          v
[ 3. LSU 수신 (Link State Update) ] ---> 요청한 상세 LSA 정보를 유니캐스트/멀티캐스트로 전파 받아 LSDB 갱신
          |
          v
[ 4. SPF 연산 (Dijkstra Algorithm) ] ---> 완벽히 동기화된 LSDB 기반으로 자신 중심의 최단 경로 트리 생성
          |
          v
[ 5. 최선 경로 설치 (FIB Installation) ] -> 최적 경로를 FIB 포워딩 테이블에 등록
```

### 동작 원리

1. **DBD 교환**: 보유 LSA의 헤더 목록 교환
2. **LSR 전송**: 누락•구버전 LSA 요청
3. **LSU 수신**: 상세 LSA로 LSDB 갱신
4. **SPF 연산**: 동기화된 LSDB의 최단 경로 계산
5. **최선 경로 설치**: 선택 경로를 RIB•FIB에 등록

#### 한줄 요약

- DBD•LSR•LSU 동기화 후 SPF 경로 계산

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OSPFv2(Open Shortest Path First version 2)**: IPv4 네트워크 경로 라우팅을 위해 제정된 OSPF 규격 (RFC 2328).
- **OSPFv3(Open Shortest Path First version 3)**: IPv6 네트워크 경로 라우팅 및 다중 주소 체계(Address Family)를 지원하도록 재설계된 OSPF 규격 (RFC 5340).

</details>

| 비교 항목 | **OSPFv2** | **OSPFv3** |
|:---|:---|:---|
| 대상 주소 체계 | **IPv4** (32비트 주소 체계) | **IPv6** (128비트 주소 체계) 및 Multi-AF 지원 |
| LSA 전파 방식 | IPv4 서브넷 데이터와 라우팅 토폴로지를 결합 전파 | 토폴로지 LSA와 IP Prefix LSA를 명확히 분리 전파 (LSA Type 8/9 추가) |
| Neighbor 식별 및 Next-Hop | IPv4 출발지 주소 기반 식별 | IPv6 링크-로컬 주소(Link-Local Address: `fe80::`) 기반 전송 |
| 보안 이증 체계 | OSPF 자체 암호화/인증 기능 지원 (Cleartext, MD5) | OSPF 자체 인증 삭제, IPv6 표준 **IPsec (AH/ESP)**에 전적으로 위임 |

> 요약: IPv4 패킷 및 토폴로지가 결합된 OSPFv2와, 토폴로지 연산과 IPv6 주소 정보를 분리하여 독립성 및 유연성을 확보한 OSPFv3의 아키텍처 발전.

#### 한줄 요약

- IPv4는 OSPFv2, IPv6•Multi-AF는 OSPFv3

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **영역 0(Area 0 / Backbone Area)**: 모든 하위 OSPF 영역들이 논리적/물리적으로 반드시 접속해야 하는 중심 백본 영역.
- **지정 라우터(Designated Router, DR)**: Broadcast/Multi-Access 이더넷 환경에서 LSA 교환 세션 수($N*(N-1)/2 \rightarrow 2N$)를 줄이기 위해 중심 중계자로 선출되는 대표 라우터.
- **백업 지정 라우터(Backup Designated Router, BDR)**: DR 장애 발생 시 선출 오버헤드 없이 즉시 DR 역할을 승계하는 예비 라우터.
- **최대 전송 단위 불일치(MTU Mismatch)**: 인접 라우터 포트 간 MTU 크기가 달라서 DBD 교환 단계(ExStart/Exchange State)에서 멈추는 장애 현상.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| 백본 영역 단절 (Discontiguous Area 0) | Area 0 물리 경로가 이원화되어 영역 간 패킷 전달 실패 | OSPF Virtual-Link 설정 또는 GRE Tunnel링으로 Area 0 결합 | 백본 도달성 확보 및 정상 라우팅 |
| OSPF Neighbor 멈춤 (ExStart Hang) | 인접 인터페이스 간 **MTU 불일치** 발생 | 인터페이스 MTU 맞춤 설정 또는 `ip ospf mtu-ignore` 적용 | DBD 패킷 수신 불능 단절 해소 |
| 대규모 이더넷 LSA 과다 | Multi-Access 환경에서 모든 라우터 간 1:1 풀메시 네이버 맺음 | **DR/BDR** 우선순위(Priority) 조율로 중앙 집중식 LSA 처리 | LSA 플러딩 및 OSPF 세션 부하 경감 |

#### 한줄 요약

- Area 0•DR/BDR•MTU 정합성으로 LSA 안정화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **영역 설계(Area Design)**: 토폴로지 규모, 링크 변경 빈도 및 대역폭을 고려하여 백본 Area 0 및 Stub/NSSA 영역을 계층화하는 라우팅 설계.
- **영역 결정(Area Boundary Selection)**: 라우팅 경로 요약(Summarization) 포인트를 ABR 위치에 정확히 배치하는 전략적 라우팅 의사결정.

</details>

- 변경이 잦은 대규모망은 **다중 영역 OSPF** 적용

#### 한줄 요약

- 규모와 변경 빈도에 따라 영역 경계•요약 지점 결정
