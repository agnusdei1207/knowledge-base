---
sidebar:
  order: 14
  label: "014. 캐시 일관성 프로토콜: MESI•MOESI (Cache Coherence Protocol)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "캐시 일관성 프로토콜: MESI•MOESI (Cache Coherence Protocol)"
date: "2026-08-13T11:36:15+09:00"
tags:
  - "notes-hardware"
weight: 14
extra:
  question_no: "014"
  source_status: "기출"
  source_history: "123회, 135회"
  priority: 70
  priority_note: "MESI 상태 전이와 불변식의 반복 기출 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **캐시 일관성 프로토콜(Cache Coherence Protocol)**: 멀티코어 프로세서 환경에서 동일한 메모리 주소를 공유하는 복수 사설 캐시(L1/L2) 사본들 간의 단일 작성자 및 최신 읽기 일관성을 유지하는 상태 머신 기반 통신 규약.
- **소유권(Ownership)**: 특정한 캐시 라인에 대해 데이터를 직접 수정할 수 있고 하위 메모리나 타 캐시로 최신 데이터를 제공/반영할 책임을 갖는 독점 제어 권한.
- **캐시 사본(Cache Copy)**: 메인 메모리의 특정 64바이트 라인 데이터가 여러 독립 코어의 사설 SRAM 캐시 상에 적재되어 복제되어 있는 일시적 물리 사본.

</details>

- 정의/개념: 멀티코어 환경에서 복수 사설 캐시에 복제된 동일 주소 데이터 사본의 **소유권**과 최신 데이터 전파를 제어하는 하드웨어 상태 전이 규약인 **캐시 일관성 프로토콜**.
- 배경/필요성: 코어 0이 캐시 데이터를 수정한 후, 코어 1이 메인 메모리나 사설 캐시에서 구버전(Stale) 데이터를 읽어 시스템 데이터 파괴 및 무한 루프 오류가 발생하는 캐시 비일관성 문제(Cache Incoherence)를 원천 차단하기 위해 탄생.

#### 한줄 요약
- 복수 멀티코어 사설 캐시 간의 단일 쓰기 독점 권한과 최신 데이터 일관성을 하드웨어 FSM 상태 전이로 보장하는 제어 규약.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **단일 작성자 불변식(Single Writer Invariant, SWI)**: 특정 시점에 동일 주소 캐시 라인을 수정할 수 있는 쓰기 독점 권한은 오직 단 1개의 캐시만 보유할 수 있다는 핵심 규칙.
- **다중 독자 불변식(Multiple Reader Invariant, MRI)**: 해당 캐시 라인을 수정하려는 쓰기 권한 소유자가 없을 때에 한하여 무수한 코어가 동시에 읽기 사본을 공유(Shared)할 수 있다는 규칙.
- **쓰기 직렬화(Write Serialization)**: 동일 캐시 주소에 대한 복수 코어의 쓰기 요청이 발생할 경우 온칩 인터커넥트 중재를 통해 전역적으로 동일한 글로벌 서순으로만 실행되도록 순서화하는 성질.
- **거짓 공유(False Sharing)**: 서로 다른 변수가 동일 64바이트 캐시 라인에 위치하여 한 코어의 쓰기가 타 코어의 무해한 변수 사본까지 강제 Invalidate 시키는 현상.

</details>

- **단일 작성자 불변식** 및 **다중 독자 불변식**에 의거하여 쓰기 독점권 보유 시 타 코어의 사본을 모두 파기.
- **쓰기 직렬화**를 보장하여 모든 코어가 동일 주소의 데이터 변경 사항을 시점상 한 방향 서순으로 동일하게 관측.
- 무효화(Invalidation) 제어 단위가 4바이트 변수가 아닌 64바이트 **캐시 라인** 전체로 구동됨에 따라 **거짓 공유** 병목 수반.

#### 한줄 요약
- SWI(Single-Writer) 및 MRI(Multiple-Reader) 불변식을 만족시키고 Write Serialization을 통해 메모리 일관성을 유지함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **상태 비트(State Bits)**: 캐시 라인 태그 옆에 배치되어 해당 라인의 현재 일관성 상태(M, E, S, I / O)를 2~3비트로 기록하는 하드웨어 플래그.
- **일관성 연결망(Coherence Interconnect)**: 스누핑 브로드캐스트 패킷이나 디렉터리 P2P 메시지를 주고받는 온칩 인터커넥트 회로망.
- **공유 메모리 계층(Shared Memory Hierarchy)**: L3 LLC 및 DRAM 메인 메모리로 구성되어 축출되는 더티 라인을 수용하는 상위 공유 구조.

</details>

```text
[ Cache Coherence Controller Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Private Cache Line Tag Entry : [Valid][Dirty][State Bits] │
│ State Bits : M(Modified) / O(Owned) / E(Exclusive) / S / I │
├───────────────────────────────────────────────────────────┤
│ Coherence Controller (FSM State Transition Engine)        │
│  - Local CPU Requests : PrRd (Read), PrWr (Write)         │
│  - Remote Bus Requests: BusRd, BusRdX, BusUpgr, BusInval │
├───────────────────────────────────────────────────────────┤
│ Coherence Interconnect (Snoop Bus / Directory Router)     │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 상태 비트 | 라인의 **M•O•E•S•I 권한** 표시 |
| 일관성 제어기 | 로컬•원격 요청에 따른 **FSM 전이** 수행 |
| 일관성 연결망 | **Snoop•Directory•C2C** 메시지 전달 |
| 공유 메모리 계층 | **더티 축출 라인** 수용•보존 |

#### 한줄 요약
- Cache Line State Bits, FSM 기반 Coherence Controller 및 Interconnect가 결합하여 코어 간 소유권 패킷을 중계함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **수정 상태(Modified, M)**: 데이터가 메모리와 달리 최신으로 갱신되었으며, 오직 이 캐시만 독점 소유권을 가진 상태 (Read/Write 가능).
- **독점 상태(Exclusive, E)**: 데이터가 메모리와 일치하나, 타 캐시에는 사본이 없고 오직 이 캐시만 독점 보유한 상태 (무제한 Write 가능).
- **공유 상태(Shared, S)**: 데이터가 메모리와 일치하며, 타 캐시에도 동일 사본이 병렬 존재할 수 있는 읽기 전용 상태 (Read 전용).
- **무효 상태(Invalid, I)**: 데이터가 유효하지 않거나 타 코어의 쓰기로 인해 사본이 파기되어 접근 불가능한 상태.
- **무효화(Invalidation)**: 타 코어가 쓰기 권한(BusRdX)을 요청했을 때 자신의 S/E 사본 상태를 I 상태로 강제 파기하는 동작.

</details>

```text
[ Local Core Memory Store Request (PrWr) ]
                    │
                    ▼
          [ Local Line State Check ]
          ├─ Modified (M)  ──> Local Write Complete
          ├─ Exclusive (E) ──> Transition to M & Local Write
          └─ Shared (S) / Invalid (I)
                │
                ▼
      Coherence Interconnect로 BusRdX / BusUpgr 전송
                │
                ▼
       Remote Cores의 Shared Copy -> Invalid (I)
                │
                ▼
       Local Line -> Modified (M) 후 Write 완결
```

### 동작 원리

- **M•E 로컬 갱신**: M은 즉시 쓰고 E는 M으로 전이 후 쓰기함.
- **소유권 획득**: S는 **BusUpgr**, I는 **BusRdX**를 전송함.
- **원격 사본 무효화**: 동일 주소 사본을 **Invalid** 상태로 변경함.
- **M 상태 승격**: 독점권 획득 후 M 상태에서 쓰기를 완결함.

#### 한줄 요약
- Local State 확인 후 S/I 상태일 때 BusRdX를 전파하여 원격 사본을 Invalidate 시키고 M 상태로 승격하여 쓰기를 완결함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MESI**: Modified, Exclusive, Shared, Invalid 4가지 상태를 사용하여 대중적으로 채택된 캐시 일관성 프로토콜.
- **MOESI**: MESI에 **Owned(O)** 상태를 추가하여, 메인 메모리 쓰기(Write-back) 없이도 더티 데이터를 다른 코어들과 직접 공유 및 캐시 간 전송(C2C Transfer)할 수 있는 최적화 프로토콜.
- **소유 상태(Owned, O)**: 데이터가 메인 메모리와 불일치(Dirty)하지만, 다른 코어들에게 Shared(S) 사본을 공유해 주면서 최종 메모리 Write-back 책임을 독점 보존하는 상태.
- **더티 공유(Dirty Sharing)**: 메인 메모리로 최신 데이터를 플러시하지 않고도 캐시 대 캐시(Cache-to-Cache) 통신으로 더티 데이터를 타 캐시에 공유해 주는 기술.

</details>

| 비교 항목 | MESI 프로토콜 (4-State) | MOESI 프로토콜 (5-State) |
|:---|:---|:---|
| **상태 구성** | Modified, Exclusive, Shared, Invalid | Modified, **Owned**, Exclusive, Shared, Invalid |
| **더티 공유** | 별도 Owned 상태 없이 구현별 개입 처리 | **Owned** 상태로 더티 사본 공유 가능 |
| **메모리 트래픽** | 더티 공유 때 쓰기 책임 이전 제약 | **Dirty Sharing**으로 Write-back 연기 |
| **최신 데이터 제공자**| M 상태 캐시 또는 일관성 홈 노드 | **Owned** 상태 캐시가 사본 제공 |
| **하드웨어 복잡도** | 비교적 단순함 | 5개 상태 전이 제어 로직 필요로 FSM 복잡 |
| **구현 특성** | 4상태 기반의 비교적 단순한 제어 | 5상태 기반의 더티 공유 최적화 |

#### 한줄 요약
- MESI는 4상태 제어, MOESI는 Owned 기반 더티 공유로 Write-back을 연기함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **소유권 지역화(Ownership Localization)**: 특정 데이터 쓰기 작업을 가급적 동일 코어에 묶어서 할당(Core Affinity)하여, 코어 간 소유권 핑퐁(Ping-Ponging) 무효화 트래픽을 예방하는 기법.
- **캐시 간 전달(Cache-to-Cache Transfer / Direct C2C)**: 메모리까지 가지 않고 온칩 라우터를 통해 M/O 상태 캐시에서 직접 요청 코어로 데이터를 쏘아주는 고속 전송.
- **프로토콜 불변식(Protocol Invariant Testing)**: 비순차 수신이나 동시 승격 시 SWI/MRI가 깨져 경쟁 조건이 생기지 않도록 검증하는 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 복수 코어가 동일 주소를 번갈아 Write 하여 소유권 Ping-Ponging 폭증 | **소유권 지역화** 및 Thread-Core Affinity 설정 | Invalidation 트래픽 파괴적 절감 |
| MESI에서 Modified 데이터 공유 요청 시 매번 DRAM 기록으로 지연 발생 | **MOESI** 프로토콜 채택 및 **캐시 간 직접 전달(Direct C2C)** 연동 | DRAM 쓰기 무효화 및 데이터 공유 접근 지연시간 극소화 |
| 독립 변수가 64B 캐시 라인에 겹쳐 발생하는 **거짓 공유** | 구조체 변수 간 64B **Cache Line Padding** 기법 연동 | 불필요한 라인 무효화 및 리필 수습 지연 예방 |
| 동시 접근 시 FSM 코너케이스로 단일 작성자 불변식 위반 | **프로토콜 불변식** Formal Verification과 Stress Test | 멀티코어 메모리 상태 오염 차단 |

#### 한줄 요약
- Ownership Localization, MOESI Direct C2C Transfer, Cache Line Padding 및 Protocol Formal Verification을 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **프로토콜 선택 기준(Protocol Selection Criteria)**: 대상 멀티코어 SoC의 사설 캐시 간 공유 쓰기 패턴, 온칩 라우터 대역폭, DRAM 메모리 접근 지연을 종합 평가하여 MESI/MOESI 및 Snooping/Directory 구조를 선택하는 가이드라인.

</details>

- 더티 공유가 빈번하면 **MOESI**, 단순 제어가 우선이면 **MESI** 선택.

#### 한줄 요약
- 공유 패턴과 연결망 비용을 기준으로 상태 수와 C2C 지원을 결정함.
