---
sidebar:
  order: 15
  label: "015. 버스 스누핑•디렉터리 기반 일관성 (Bus Snooping Directory Coherence)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "버스 스누핑•디렉터리 기반 일관성 (Bus Snooping Directory Coherence)"
date: "2026-08-13T11:37:12+09:00"
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

<details><summary>용어 설명</summary>

- **버스 스누핑(Bus Snooping)**: 공용 브로드캐스트 버스 신호를 각 사설 캐시 컨트롤러가 실시간 스누핑(기웃거리며 관찰)하여 캐시 일관성 트랜잭션을 전파 처리하는 방식.
- **디렉터리 기반 일관성(Directory-Based Coherence)**: 메인 메모리 또는 L3 캐시에 각 캐시 라인의 사본 보유 노드 목록(Sharer Vector)과 소유자 정보를 기록 관리하여 대상 코어로만 P2P(Point-to-Point) 메시지를 전송하는 하드웨어 메커니즘.
- **선택적 무효화(Selective Invalidation)**: 전체 코어에 트래픽을 뿌리지 않고 실제 해당 캐시 라인의 사본을 보유하고 있는 코어로만 선택적으로 Invalidate 패킷을 전송하는 메커니즘.
- **공유자 추적(Sharer Tracking)**: 디렉터리 메타데이터 테이블 상에서 특정 캐시 라인의 최신 사본을 지닌 코어들의 노드 ID 비트맵을 인덱싱 관리하는 기법.

</details>

- 정의/개념: 공유 버스 트래픽 브로드캐스트 감시 방식의 **버스 스누핑(Bus Snooping)**과 주소별 **공유자 추적(Sharer Tracking)**을 이용해 특정 노드에만 P2P 패킷을 전송하는 **디렉터리 기반 일관성(Directory-Based Coherence)** 아키텍처.
- 배경/필요성: 코어 증가 시 전역 스누프 방송이 대역폭•전력을 소모하여 선택적 대상 추적 구조가 요구됨.

#### 한줄 요약
- 소규모 멀티코어용 Bus Snooping(전체 브로드캐스트 방식)과 대규모 스케일아웃용 Directory Coherence(공유자 비트맵 P2P 전달 방식)의 하드웨어 일관성 체계.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

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
 [P2P NoC Mesh]
 ├─ [Core 0 Node]
 ├─ [Home Directory Node | Sharer Bit Vector]
 └─ [Core 2 Node]
```

| 구성요소 | 책임 |
|:---|:---|
| 공유 버스•중재기 | 요청 **직렬화•전 코어 방송** |
| 스누프 제어기 | 방송 주소 감시와 **상태 전이** 수행 |
| 홈 디렉터리 | 주소별 **소유자•공유자 목록** 관리 |
| 점대점 인터커넥트 | 홈•대상 노드 간 **일관성 메시지** 전달 |

#### 한줄 요약
- Bus Snooping은 Shared Bus & Snoop Controller 구성을 사용하고, Directory 방식은 Home Directory Node & NoC P2P 라우팅 구성을 취함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **홈 노드(Home Node)**: 특정 캐시 라인의 주소 번지에 대응하는 디렉터리 메타데이터와 메모리를 직접 관장하는 노드.
- **공유자 목록(Sharer List / Bit Vector)**: 64바이트 메모리 라인을 Shared 상태로 보유 중인 코어들의 N-bit 비트맵 표.
- **완료 응답 수합(Acknowledgment Collection)**: 홈 디렉터리나 요청자가 대상 코어의 Ack 패킷을 모두 받는 동기화 절차.

</details>

```text
[ Bus Snooping Flow ]
Core 0 Write Request ──> Shared Bus 브로드캐스트 ──> All Cores Snoop & Invalidate ──> Ack ──> Core 0 Write

[ Directory-Based Flow ]
Core 0 Write Request ──> Home Node Directory 조회 (Sharer: Core 2, Core 3)
                              │
                              ▼
                         Targeted P2P Invalidation (Core 2, Core 3)
                              │
                              ▼
                         Core 2, Core 3 Ack ──> Core 0 Write 완결
```

### 동작 원리

- **버스 스누핑**: Write 요청을 방송하고 모든 스누프가 태그를 검사함.
- **디렉터리 조회**: 홈 노드가 **Sharer List**로 무효화 대상을 선택함.
- **Ack 수합**: 대상 사본 무효화 Ack 후 배타적 쓰기 권한을 부여함.

#### 한줄 요약
- Snooping은 전 코어 Bus Broadcast로 무효화를 수행하고 Directory 방식은 Home Node 조회 후 지정 코어로만 P2P Invalidation을 수행함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **디렉터리 방식(Directory-Based)**: 메타데이터를 대가로 무효화 대상을 선택해 방송 범위를 줄이는 일관성 구조.
- **메타데이터(Metadata)**: 디렉터리 램 상에 저장되는 라인별 상태(State: Uncached, Shared, Modified) 및 Sharer 코어 비트맵 데이터.
- **다중 소켓(Multi-Socket NUMA)**: 2개 이상의 독립 CPU 소켓이 고속 인터커넥트(QPI, UPI, Infinity Fabric)로 결합된 서버 플랫폼.
- **조회 지연(Lookup Latency)**: 홈 디렉터리에서 메타데이터를 읽고 대상 노드로 전달하는 네트워크 지연.

</details>

| 비교 항목 | 버스 스누핑 (Bus Snooping) | 디렉터리 방식 (Directory-Based) |
|:---|:---|:---|
| **통신 메커니즘** | **공유 버스** 기반 전체 브로드캐스트 (1:N) | **점대점 인터커넥트(NoC)** 기반 P2P 메시지 (1:1 / 1:M) |
| **코어 확장성** | 코어 증가 시 방송 대역폭으로 제한 | **다중 소켓 NUMA**까지 계층적 확장 용이 |
| **하드웨어 오버헤드**| 단순 (별도 디렉터리 메타데이터 메모리 불필요) | 메타데이터 저장을 위한 DRAM/SRAM **메타데이터** 공간 소모 |
| **트랜잭션 지연** | 공유 매체 중재와 방송 지연 | 홈 디렉터리 **조회•P2P 왕복** 지연 |
| **주요 적용 위치** | 모바일 SoC, 코어 수가 적은 Desktop CPU | 클라우드 대형 서버 CPU, 멀티소켓 NUMA 데이터센터 |

#### 한줄 요약
- 버스 스누핑은 단순하지만 방송에 제한되고, 디렉터리는 메타데이터 대가로 대상 전송을 지원함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **희소 디렉터리(Sparse Directory)**: 전체 메인 메모리 라인이 아닌 현재 캐시에 적재된 라인에 대해서만 디렉터리 메타데이터를 유지하여 메모리 오버헤드를 극소화하는 압축 구조.
- **제한 디렉터리(Limited Directory / $Dir_iB$)**: Sharer 비트맵 크기를 최대 N개 코어로 제한하고 개수 초과 시 브로드캐스트로 전환하는 절충형 디렉터리.
- **주소 해싱(Address Hashing)**: 메모리 주소를 온칩 해시 함수로 분산시켜 특정 홈 디렉터리 노드로 핫스팟 트래픽이 쏠리는 병목을 방지하는 기술.
- **가상 채널(Virtual Channel)**: Request, Response, Invalidate 메시지의 통신 선로를 논리 채널로 격리하여 일관성 프로토콜 교착상태(Deadlock)를 방지하는 NoC 기술.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 노드 수 증설 시 디렉터리 **메타데이터** 용량 증가 | **희소 디렉터리(Sparse Directory)** 및 **제한 디렉터리** 구조 채택 | 추적 엔트리와 공유자 비트 저장량 절감 |
| 특정 메모리 번지 집중 접근 시 특정 **홈 노드**로 핫스팟 라우팅 폭증 | **주소 해싱(Address Hashing)** 기반 홈 디렉터리 전 노드 분산 | 온칩 라우터 병목 해소 및 P2P 지연시간 균일화 |
| 소유권 요청과 Inval Ack 패킷이 온칩 라우터 큐를 가득 채워 **프로토콜 교착(Deadlock)** | NoC 라우터 내 **가상 채널(Virtual Channel)** 분리 및 자원 순서화 | 일관성 메시지 대기 교착 완벽 차단 및 Liveness 보장 |
| 스누핑 칩에서 코어 증설 시 **버스 포화** 발생 | Crossbar•Mesh NoC 전환 및 **계층형 스누핑** 적용 | 로컬 방송 범위 축소와 외부 대역폭 확보 |

#### 한줄 요약
- Sparse/Limited Directory 메타데이터 절감, Address Hashing 전역 분산, Virtual Channel Deadlock 방지 및 Hierarchical Snooping을 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **방송 확장성(Broadcast Scalability)**: 코어 수 증가에 대응하여 시스템 일관성 패킷 트래픽을 감당할 수 있는 아키텍처 한계 성능 지표.
- **구현 방식 선택 기준(Coherence Architecture Selection Criteria)**: 칩 내부의 물리적 코어 수, 온칩 라우터 토폴로지, 메타데이터 실리콘 면적을 종합 평가하여 Bus Snooping과 Directory-based 방식을 결정하는 프레임워크.

</details>

- 방송 비용이 작으면 **Snooping**, 코어•소켓 확장 시 **Directory•NoC** 선택.

#### 한줄 요약
- 방송 대역폭과 메타데이터 비용을 비교하여 일관성 구조를 결정함.
