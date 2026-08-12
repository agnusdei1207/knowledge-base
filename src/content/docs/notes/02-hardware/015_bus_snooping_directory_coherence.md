---
sidebar:
  order: 15
  label: "015. 버스 스누핑•디렉터리 기반 일관성 (Bus Snooping Directory Coherence)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "버스 스누핑•디렉터리 기반 일관성 (Bus Snooping Directory Coherence)"
date: "2026-08-08T13:22:00+09:00"
tags:
  - "notes-hardware"
weight: 15
extra:
  question_no: "015"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "방송 트래픽과 디렉터리 비용의 선택 주제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **버스 스누핑(Bus Snooping)**: 공용 브로드캐스트 버스 신호를 각 사설 캐시 컨트롤러가 실시간 스누핑(기웃거리며 관찰)하여 캐시 일관성 트랜잭션을 전파 처리하는 방식.
- **디렉터리 기반 일관성(Directory-Based Coherence)**: 메인 메모리 또는 L3 캐시에 각 캐시 라인의 사본 보유 노드 목록(Sharer Vector)과 소유자 정보를 기록 관리하여 대상 코어로만 P2P(Point-to-Point) 메시지를 전송하는 하드웨어 메커니즘.
- **선택적 무효화(Selective Invalidation)**: 전체 코어에 트래픽을 뿌리지 않고 실제 해당 캐시 라인의 사본을 보유하고 있는 코어로만 선택적으로 Invalidate 패킷을 전송하는 메커니즘.
- **공유자 추적(Sharer Tracking)**: 디렉터리 메타데이터 테이블 상에서 특정 캐시 라인의 최신 사본을 지닌 코어들의 노드 ID 비트맵을 인덱싱 관리하는 기법.

</details>

- 정의/개념: 공유 버스 트래픽 브로드캐스트 감시 방식의 **버스 스누핑(Bus Snooping)**과 주소별 **공유자 추적(Sharer Tracking)**을 이용해 특정 노드에만 P2P 패킷을 전송하는 **디렉터리 기반 일관성(Directory-Based Coherence)** 아키텍처.
- 배경/필요성: 코어 수가 8개 이상 확장되는 NUMA 서버 및 대규모 멀티코어 환경에서 공유 버스 기반의 스누핑 브로드캐스트는 버스 대역폭 포화(Bus Saturation)를 유발하므로, 확장성(Scalability) 확보를 위한 디렉터리 방식 전환 필수.

#### 한줄 요약
- 소규모 멀티코어용 Bus Snooping(전체 브로드캐스트 방식)과 대규모 스케일아웃용 Directory Coherence(공유자 비트맵 P2P 전달 방식)의 하드웨어 일관성 체계.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **일관성 순서점(Coherence Ordering Point)**: 시스템 내에서 동일 주소에 대한 복수 접근 요청의 글로벌 직렬화 서순(Write Serialization)을 확정짓는 중재 물리 지점(공유 버스 또는 홈 디렉터리 노드).
- **무효화 응답(Invalidation Acknowledgment / Ack)**: 무효화 메시지를 받은 사설 캐시가 사본 파기를 완료하였음을 발신 노드 또는 홈 디렉터리로 되돌려주는 완료 패킷.
- **배타적 쓰기 권한(Exclusive Write Permission)**: 특정 캐시가 M/E 상태로 승격되어 다른 타 코어의 방해 없이 안전하게 쓰기 연산을 수행할 수 있는 독점 상태.
- **방송 관찰(Broadcast Observation)**: 공유 버스를 탄 모든 트랜잭션 주소를 칩 내 모든 사설 캐시 제어기가 일일이 비교 수신하는 동작.
- **명단 조회(Directory Lookup)**: 홈 디렉터리에 접근하여 해당 캐시 라인을 보유 중인 코어들의 Bit Vector 명단을 판독하는 작업.

</details>

- 모든 캐시 트랜잭션의 글로벌 전역 순서를 결정짓는 **일관성 순서점(Coherence Ordering Point)**을 구성하여 쓰기 직렬화 보장.
- 타 코어 사본들의 **무효화 응답(Invalidation Acknowledgment)** 수합이 완결된 후에만 요청 코어에 **배타적 쓰기 권한(Exclusive Write Permission)** 부여.
- 버스 스누핑은 단순한 **방송 관찰(Broadcast Observation)** 방식, 디렉터리 기반은 정밀한 **명단 조회(Directory Lookup)**를 통해 트래픽 전송 대상 결정.

#### 한줄 요약
- Coherence Ordering Point 중심의 요청 직렬화와 Invalidation Ack 수합 완료를 통해 단일 쓰기 소유권을 확정함.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **버스 중재기(Bus Arbiter)**: 멀티코어 공유 버스 환경에서 일관성 트랜잭션 요청 간의 획득 우선순위를 스케줄링하는 하드웨어 Arbiter.
- **스누프 제어기(Snoop Controller)**: 사설 캐시 쪽에 배치되어 버스 라인의 주소를 항시 스누핑하고 캐시 라인 태그 상태를 M/E/S/I로 전이시키는 조작기.
- **홈 디렉터리(Home Directory / Home Node)**: 각 메인 메모리 주소 블록의 디렉터리 상태(Uncached, Shared, Exclusive)와 Sharer Bit Vector를 보유한 중앙/분산 관리 노드.
- **점대점 인터커넥트(Point-to-Point Interconnect / NoC)**: 크로스바 스위치, 2D-Mesh 구조로 특정 수신 노드로만 일관성 메시지를 직접 라우팅하는 온칩 네트워크 통로.
- **공유 버스(Shared Bus)**: 모든 코어가 물리적 신호 선로를 공유하여 1개의 주소 트랜잭션을 모든 코어에 동시에 전파하는 구형 인터커넥트.

</details>

```text
[ Bus Snooping Coherence ]
 [Core 0 Cache]   [Core 1 Cache]   [Core 2 Cache]
       │                │                │
 ══════╧════════════════╧════════════════╧════ Shared Bus (Broadcast All)

[ Directory-Based Coherence ]
 [Core 0 Node] ──(P2P NoC Mesh)──> [Home Directory Node (Sharer Bit Vector)]
                                          │ (Targeted Invalidate P2P)
                                          ▼
                                   [Core 2 Node] (Selective Invalidation)
```

| 구성요소 | 역할 및 작동 원리 | 차별점 및 실무 유용성 |
|:---|:---|:---|
| **공유 버스 & 버스 중재기** | 모든 트랜잭션을 일렬 직렬화하여 전 코어로 브로드캐스트 | 소규모(4~8코어)에서 별도 메모리 오버헤드 없이 직관적 구현 |
| **스누프 제어기** | 버스 브로드캐스트 주소를 감시하여 자기 캐시 태그와 대조 | 무효화(Inval) 처리 및 더티 데이터 타 코어 직접 딜리버리 |
| **홈 디렉터리** | 메모리 블록별 소유 코어 및 Sharer Vector 명단 총괄 관리 | 대규모 멀티코어/NUMA 환경에서 필요 코어로만 메시지 국한 |
| **점대점 인터커넥트 (NoC)**| 메시 통신망을 통해 홈 디렉터리와 대상 코어 간 P2P 데이터 전송 | 전역 브로드캐스트 병목을 완전히 제거하여 확장성 대폭 확보 |

#### 한줄 요약
- Bus Snooping은 Shared Bus & Snoop Controller 구성을 사용하고, Directory 방식은 Home Directory Node & NoC P2P 라우팅 구성을 취함.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **홈 노드(Home Node)**: 특정 캐시 라인의 주소 번지에 대응하는 디렉터리 메타데이터와 메모리를 직접 관장하는 노드.
- **공유자 목록(Sharer List / Bit Vector)**: 64바이트 메모리 라인을 Shared 상태로 보유 중인 코어들의 N-bit 비트맵 표.
- **완료 응답 수합(Acknowledgment Collection)**: 홈 디렉터리 또는 발신 코어가 대상 코어들로부터 이메일 형식의 Ack 패킷을 모두 받아 래칭하는 동기화 절차.

</details>

```text
[ Bus Snooping Flow ]
Core 0 Write Request ──> Shared Bus 브로드캐스트 ──> All Cores Snoop & Invalidate ──> Ack ──> Core 0 Write

[ Directory-Based Flow ]
Core 0 Write Request ──> 1. Home Node Directory 조회 (Sharer Bit Vector 확인: Core 2, Core 3)
                              │
                              ▼
                         2. Targeted P2P Invalidation 메시지 전송 (Core 2, Core 3로만 전송)
                              │
                              ▼
                         3. Core 2, Core 3 Invalidate 완료 후 Ack 전송 ──> 4. Core 0 Write 완결
```

### 동작 원리

1. **버스 스누핑 방식**: Core 0가 Write 요청을 공유 버스에 태우면, 버스에 매달린 모든 코어의 **스누프 제어기**가 이를 동시에 수신하여 자기 태그를 무효화하고 완결함.
2. **디렉터리 방식**: Core 0가 **홈 노드(Home Node)**로 Write 소유권을 요청하면, 홈 노드는 **공유자 목록(Sharer List)**을 조회하여 사본을 쥔 Core 2, Core 3에게만 P2P Invalidate 패킷을 발송함.
3. **Ack 수합 및 완결**: 사본 보유 코어들로부터 **완료 응답 수합(Ack)**을 수용하여 배타적 쓰기 권한(M 상태)을 부여받고 연산을 완료함.

#### 한줄 요약
- Snooping은 전 코어 Bus Broadcast로 무효화를 수행하고 Directory 방식은 Home Node 조회 후 지정 코어로만 P2P Invalidation을 수행함.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **디렉터리 방식(Directory-Based)**: 메타데이터 오버헤드를 대가로 100개 이상의 노드까지 선형 스케일아웃 확장이 가능한 일관성 구조.
- **메타데이터(Metadata)**: 디렉터리 램 상에 저장되는 라인별 상태(State: Uncached, Shared, Modified) 및 Sharer 코어 비트맵 데이터.
- **다중 소켓(Multi-Socket NUMA)**: 2개 이상의 독립 CPU 소켓이 고속 인터커넥트(QPI, UPI, Infinity Fabric)로 결합된 서버 플랫폼.
- **조회 지연(Lookup Latency)**: 홈 디렉터리 노드에 접근하여 메타데이터 비트맵을 읽어오는 데 소요되는 3-hop 네트워크 딜레이.

</details>

| 비교 항목 | 버스 스누핑 (Bus Snooping) | 디렉터리 방식 (Directory-Based) |
|:---|:---|:---|
| **통신 메커니즘** | **공유 버스** 기반 전체 브로드캐스트 (1:N) | **점대점 인터커넥트(NoC)** 기반 P2P 메시지 (1:1 / 1:M) |
| **코어 확장성** | 저조함 (8~16 코어 이상 시 버스 대역폭 포화) | 압도적 (수백~수천 코어, **다중 소켓 NUMA** 확장 가능) |
| **하드웨어 오버헤드**| 단순 (별도 디렉터리 메타데이터 메모리 불필요) | 메타데이터 저장을 위한 DRAM/SRAM **메타데이터** 공간 소모 |
| **트랜잭션 지연** | 짧음 (버스를 통한 즉시 1-hop 브로드캐스트) | 상대적 길음 (요청->홈 디렉터리 **조회 지연**->P2P 3-hop) |
| **주요 적용 위치** | 모바일 SoC, 코어 수가 적은 Desktop CPU | 클라우드 대형 서버 CPU, 멀티소켓 NUMA 데이터센터 |

#### 한줄 요약
- 버스 스누핑은 저지연 단순성에 강점을 가지나 코어 확장성이 제한되고, 디렉터리 방식은 메타데이터 및 3-hop 지연 대가로 무제한 스케일아웃 확정성을 제공함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **희소 디렉터리(Sparse Directory)**: 전체 메인 메모리 라인이 아닌 현재 캐시에 적재된 라인에 대해서만 디렉터리 메타데이터를 유지하여 메모리 오버헤드를 극소화하는 압축 구조.
- **제한 디렉터리(Limited Directory / $Dir_iB$)**: Sharer 비트맵 크기를 최대 N개 코어로 제한하고 개수 초과 시 브로드캐스트로 전환하는 절충형 디렉터리.
- **주소 해싱(Address Hashing)**: 메모리 주소를 온칩 해시 함수로 분산시켜 특정 홈 디렉터리 노드로 핫스팟 트래픽이 쏠리는 병목을 방지하는 기술.
- **가상 채널(Virtual Channel)**: Request, Response, Invalidate 메시지의 통신 선로를 논리 채널로 격리하여 일관성 프로토콜 교착상태(Deadlock)를 방지하는 NoC 기술.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 노드 수 증설 시 디렉터리 **메타데이터** 메모리 소모량 파괴적 증가 | **희소 디렉터리(Sparse Directory)** 및 **제한 디렉터리** 구조 채택 | 메타데이터 DRAM 공간 점유율 80% 이상 절감 |
| 특정 메모리 번지 집중 접근 시 특정 **홈 노드**로 핫스팟 라우팅 폭증 | **주소 해싱(Address Hashing)** 기반 홈 디렉터리 전 노드 분산 | 온칩 라우터 병목 해소 및 P2P 지연시간 균일화 |
| 소유권 요청과 Inval Ack 패킷이 온칩 라우터 큐를 가득 채워 **프로토콜 교착(Deadlock)** | NoC 라우터 내 **가상 채널(Virtual Channel)** 분리 및 자원 순서화 | 일관성 메시지 대기 교착 완벽 차단 및 Liveness 보장 |
| 스누핑 칩에서 코어 증설 시 **버스 포화(Bus Saturation)** 현상발생 | Crossbar / Mesh NoC 전환 및 **스누핑 계층화(Hierarchical Snooping)** 적용 | 로컬 클러스터 내부 스누핑과 외부 디렉터리 조합으로 대역폭 확보 |

#### 한줄 요약
- Sparse/Limited Directory 메타데이터 절감, Address Hashing 전역 분산, Virtual Channel Deadlock 방지 및 Hierarchical Snooping을 적용함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **방송 확장성(Broadcast Scalability)**: 코어 수 증가에 대응하여 시스템 일관성 패킷 트래픽을 감당할 수 있는 아키텍처 한계 성능 지표.
- **구현 방식 선택 기준(Coherence Architecture Selection Criteria)**: 칩 내부의 물리적 코어 수, 온칩 라우터 토폴로지, 메타데이터 실리콘 면적을 종합 평가하여 Bus Snooping과 Directory-based 방식을 결정하는 프레임워크.

</details>

- **구현 방식 선택 기준(Coherence Architecture Selection Criteria)**에 근거하여 단일 다이 8코어 이하의 스마트폰/노트북 SoC에는 저지연 **버스 스누핑(Bus Snooping)** 아키텍처를 적용하고, 수십~수천 코어 규격의 클라우드 데이터센터/멀티소켓 NUMA 서버 인프라에는 **희소 디렉터리 기반 일관성(Sparse Directory-Based)** 및 NoC 가상 채널 네트워크 구축 체계 적용 필수.

#### 한줄 요약
- 소규모 코어용 저지연 Bus Snooping 및 대규모 멀티소켓 NUMA 서버용 Sparse Directory Coherence/NoC P2P 구축 체계 적용.
