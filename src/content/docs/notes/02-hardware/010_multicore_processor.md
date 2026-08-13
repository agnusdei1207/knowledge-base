---
sidebar:
  order: 10
  label: "010. 멀티코어 프로세서 (Multicore Processor)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "멀티코어 프로세서 (Multicore Processor)"
date: "2026-08-13T11:32:49+09:00"
tags:
  - "notes-hardware"
weight: 10
extra:
  question_no: "010"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "코어 수•유형•공유 자원 선택의 핵심 주제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **멀티코어 프로세서(Multicore Processor)**: 단일 반도체 다이(Die) 칩 내부에 2개 이상의 독립적인 CPU 코어를 집적하여 다중 소프트웨어 스레드를 동시에 처리하는 시스템.
- **스레드 수준 병렬성(Thread-Level Parallelism, TLP)**: 복수의 독립적인 소프트웨어 실행 스레드를 물리적으로 서로 다른 CPU 코어에서 병렬 구동하는 아키텍처 기법.
- **전력 한계(Power Wall)**: 클록 주파수 및 작동 전압 증가에 따른 동적 전력 소모(Power Consumption)가 반도체 패키징의 허용 전력 캡을 초과하는 기술적 장벽.
- **발열 한계(Thermal Wall)**: 칩의 단위 면적당 전력 밀도 증가로 인한 발열을 쿨러 및 냉각 장치가 감당하지 못하는 물리적 한계.

</details>

- 정의/개념: 단일 반도체 칩 상에 2개 이상의 연산 코어와 공유 캐시 계층을 집적하여 **스레드 수준 병렬성(Thread-Level Parallelism, TLP)**을 실현하는 고성능 **멀티코어 프로세서(Multicore Processor)**.
- 배경/필요성: 단일 코어의 동작 주파수(GHz)를 무리하게 끌어올릴 경우 **전력 한계(Power Wall)** 및 **발열 한계(Thermal Wall)**에 부딪혀 클록 고속화를 통한 성능 향상이 불가능해짐에 따라, 저전력 멀티코어 병렬 실행을 통한 전력 대 성능비(Perf/Watt) 극대화 요구 대두.

#### 한줄 요약
- 단일 코어의 전력/발열 장벽을 극복하기 위해 다중 물리 코어를 단일 칩에 집적하여 스레드 수준 병렬성(TLP)과 처리량을 극대화함.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **암달의 법칙(Amdahl's Law)**: 코어 수 $N$을 무한히 증설하더라도 프로그램 내의 불가피한 직렬 처리 비율 $S$에 의해 전체 가속비(Speedup) 상한이 한정됨을 나타내는 성능 법칙 ($\text{Speedup} = \frac{1}{S + \frac{1-S}{N}}$).
- **가속비(Speedup)**: 단일 코어 환경의 처리 시간 대비 멀티코어 병렬 처리 환경에서 달성된 상대적 성능 향상 비율.
- **동기화(Synchronization)**: 다중 스레드가 메모리 내 공유 자원에 동시 접근할 때 데이터 일관성을 유지하기 위해 뮤텍스(Mutex), 세마포어(Semaphore) 등을 사용하는 제어 동작.
- **처리량(Throughput)**: 멀티코어 시스템 전체가 단위 시간당 완결 처리하는 트랜잭션 및 작업 실행의 총 수량.

</details>

- 단일 스레드의 지연시간(Latency) 단축보다는 다중 스레드의 시스템 전체 **처리량(Throughput)** 확장을 주 목적으로 설계.
- 소프트웨어가 **스레드 수준 병렬성(TLP)** 구조로 분할 설계되어 있을 때에만 코어 증설에 따른 성능 향상 효과 발휘.
- 코어 수 $N$이 증가함에 따라 **암달의 법칙(Amdahl's Law)**의 직렬 구간 병목과 코어 간 **동기화(Synchronization)** 오버헤드가 전체 가속비를 한정.

#### 한줄 요약
- TLP 병렬성 강화를 통해 전체 Throughput을 증대시키나 Amdahl's Law의 직렬 처리 비율 및 동기화 비용에 의해 가속비 상한이 설정됨.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **사설 캐시(Private Cache)**: 각 물리 코어 내부에 독점 배치되어 L1/L2 캐시 역할을 수행하는 고속 데이터 캐시.
- **최종 단계 캐시(Last-Level Cache, LLC)**: 모든 코어가 버스 또는 인터커넥트를 통해 공유하는 L3 용량 대형 캐시.
- **일관성 인터커넥트(Coherence Interconnect)**: 사설 캐시 간의 복제 데이터를 최신으로 유지하도록 스누핑(Snooping) 또는 디렉터리(Directory) 일관성 프로토콜 신호를 중계하는 온칩 네트워크(NoC).
- **코어 클러스터(Core Cluster)**: 복수의 코어와 L2/L3 캐시를 효율적인 배선 구조로 그룹화한 단위 연산 파티션.
- **메모리 제어기(Memory Controller)**: 다중 코어로부터 유입되는 DRAM 메인 메모리 접근 요청을 중재하고 대역폭을 최적 할당하는 컨트롤러.

</details>

```text
[ Multicore Processor On-Chip Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Core Cluster 0                 Core Cluster 1             │
│ ┌──────────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐│
│ │ Core 0       │ │ Core 1    │ │ Core 2    │ │ Core 3    ││
│ │ Private L1/L2│ │Priv L1/L2 │ │Priv L1/L2 │ │Priv L1/L2 ││
│ └──────────────┘ └───────────┘ └───────────┘ └───────────┘│
├───────────────────────────────────────────────────────────┤
│ Coherence Interconnect (NoC / Mesh / Crossbar Router)     │
├───────────────────────────────────────────────────────────┤
│ Shared Last-Level Cache (Shared L3 LLC Bank 0 ~ N)        │
├───────────────────────────────────────────────────────────┤
│ Integrated Multi-Channel Memory Controller (DRAM Interf.) │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 코어 클러스터 | 스레드별 **독립 명령 실행** 수행 |
| 사설 캐시 | 코어별 **저지연 명령•데이터** 제공 |
| 일관성 인터커넥트 | **MESI•MOESI 패킷** 전달•중재 |
| 공유 LLC | 코어 간 **공유 데이터•DRAM 요청** 완충 |
| 메모리 제어기 | 다중 코어의 **DRAM 채널 접근** 중재 |

#### 한줄 요약
- Core Cluster(Private L1/L2), Coherence Interconnect, Shared LLC(L3) 및 Integrated Memory Controller가 유기적 계층을 형성함.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **캐시 일관성(Cache Coherence)**: 여러 코어의 사설 캐시에 복제되어 있는 동일 메모리 주소 데이터가 한 코어에서 갱신되었을 때 모든 코어가 동일한 최신 값을 읽도록 보장하는 통신 체계.
- **쓰기 소유권(Write Ownership)**: 특정 코어가 캐시 라인을 변경하기 전 일관성 인터커넥트를 통해 해당 라인의 독점 권한을 취득하는 동작.
- **무효화(Invalidation)**: 타 코어가 가진 동일 캐시 라인 사본의 상태 비트를 Invalid로 변경하여 구버전 읽기를 차단하는 일관성 패킷.
- **스케줄러(OS Scheduler)**: OS 커널에서 실행 대기 큐의 스레드들을 최적의 물리 코어 affinity에 맞추어 할당하는 모듈.
- **캐시 라인(Cache Line)**: 캐시 일관성 제어 및 데이터 이동의 기본 구성 단위(일반적으로 64-Byte).

</details>

```text
[ OS Thread Scheduler ] ──> Thread A (Core 0 할당), Thread B (Core 1 할당)
                                  │
                                  ▼
[ Core 0 (Thread A) : Address X에 Write 연산 수행 ]
                                  │
                                  ▼
[ Coherence Interconnect ] ──> Write Ownership 요청 패킷 전송
                                  │
                                  ▼
[ Core 1 Private Cache ] ──> Address X Cache Line 즉각 Invalidation (무효화)
                                  │
                                  ▼
[ Core 0 Private Cache ] ──> Modified 상태로 데이터 쓰기 완결 및 최신 유지
```

### 동작 원리

- **스레드 할당**: OS **스케줄러**가 실행 스레드를 유휴 코어에 배정함.
- **쓰기 소유권 요청**: 쓰기 전 인터커넥트로 **Write Ownership**을 요청함.
- **사본 무효화**: 타 사설 캐시의 사본을 **Invalidation**하여 구버전 읽기를 차단함.
- **수정 상태 유지**: 소유 코어가 최신 라인을 Modified 상태로 유지함.

#### 한줄 요약
- OS Scheduler 스레드 분산 배정 및 Interconnect 기반 Write Ownership Invalidation 통신으로 캐시 일관성을 유지함.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **동시 멀티스레딩(Simultaneous Multithreading, SMT)**: 단일 물리 코어 내부에서 디코더와 연산 자원을 공유하며 2개 이상의 논리 스레드(Logical Thread)를 동시 발행하는 기법 (예: Intel Hyper-Threading).
- **동종 멀티코어(Homogeneous Multicore)**: 동일한 마이크로아키텍처 스펙의 코어들을 동일한 클록 주파수로 배치한 구조.
- **이종 멀티코어(Heterogeneous Multicore)**: 고성능 Big 코어(P-core)와 고효율 Little 코어(E-core)를 복합 탑재한 빅리틀/Arm DynamIQ 아키텍처.
- **유휴 누설전력(Idle Leakage Power)**: 연산 작업이 없이 대기 중인 코어에서도 미세 트랜지스터를 통해 계속 소비되는 정적 전력.
- **코어 이동 비용(Core Migration Overhead)**: 스레드가 P-core와 E-core 사이를 주파수 및 부하에 따라 이동할 때 발생하는 캐시 라인 Flush 및 상태 복원 지연.

</details>

| 비교 항목 | 멀티코어 (Multicore) | 동시 멀티스레딩 (SMT) |
|:---|:---|:---|
| **하드웨어 구조** | 칩 내에 독립된 복수의 **물리 코어** 탑재 | 단일 물리 코어의 아키텍처 상태 레지스터만 다중화 |
| **자원 독립성** | 코어별 ALU, FPU, L1/L2 사설 캐시가 완전 분리 | 코어 내부의 파이프라인, ALU, L1 캐시 자원을 동시 공유 |
| **성능 확장성** | 독립 코어로 TLP 확장, 공유 자원에서 한계 | 유휴 슬롯 활용, 내부 자원 경합에서 한계 |

| 멀티코어 형태 | 동종 멀티코어 (Homogeneous) | 이종 멀티코어 (Heterogeneous) |
|:---|:---|:---|
| **코어 구성** | 모든 코어가 완전히 동일한 P-core 스펙 | 고성능 P-Core + 저전력 E-Core 복합 구성 |
| **적용 환경** | 워크로드 특성이 균일한 HPC 서버, 데이터센터 | 부하 변동성이 극심한 스마트폰, 모바일, 온디바이스 AI |
| **한계점** | 경부하 시에도 높은 **유휴 누설전력** 소모 | 스케줄링 오배정 시 **코어 이동 비용** 및 성능 저하 |

#### 한줄 요약
- 물리 코어 분리의 Multicore와 파이프라인 공유의 SMT로 구분되며 코어 스펙에 따라 Homogeneous와 Heterogeneous(big.LITTLE)로 발전함.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **거짓 공유(False Sharing)**: 서로 다른 스레드가 이용하는 독립 변수들이 동일한 64바이트 캐시 라인 내에 우연히 배치되어, 한 코어의 쓰기가 타 코어 사설 캐시를 끊임없이 Invalidation 시키는 병목 현상.
- **패딩(Cache Line Padding)**: 거짓 공유 방지를 위해 구조체 내의 변수 사이에 불필요한 공백 바이트(Align 64)를 강제로 삽입하여 별도 캐시 라인으로 격리하는 기법.
- **작업 훔치기(Work Stealing)**: 유휴 상태에 도달한 특정 코어가 부하가 집중된 타 코어의 로컬 큐에서 처리 대기 중인 스레드를 가져와 병렬 렌더링하는 동적 부하분산 기술.
- **NUMA 인지 배치(NUMA-Aware Placement)**: 멀티소켓/멀티코어 환경에서 스레드가 사용할 메모리를 해당 코어에 물리적으로 연결된 로컬 메모리에 직접 할당하는 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 독립 변수 갱신 때 무효화가 반복되는 **거짓 공유(False Sharing)** | 변수 선언 시 64-Byte **패딩(Cache Line Padding)** 명시적 적용 | 캐시 라인 격리로 일관성 트래픽 절감 |
| 특정 코어에 부하가 집중되고 다른 코어는 유휴 상태 | Fork-Join 프레임워크의 **작업 훔치기(Work Stealing)** 스케줄러 도입 | 물리 코어 부하 평형 및 병렬 지연 단축 |
| 코어 증가에 따른 메인 메모리 대역폭 포화 및 엑세스 지연 | **NUMA 인지 배치** 및 데이터 **메모리 지역성(Locality)** 극대화 | 원격 메모리 억세스 트래픽 차단 및 메모리 대역폭 한계 극복 |
| 이종 코어 환경에서 고부하 작업이 E-core에 할당되어 처리 속도 둔화 | OS 커널 인텔리전트 **이종 코어 스케줄링(ITD 등)** 연동 | 앱 요구 특성에 부합하는 P/E 코어 적재적소 즉시 배치 |

#### 한줄 요약
- Cache Line Padding(False Sharing 방지), Work Stealing(부하 평형), NUMA-Aware Placement 및 Heterogeneous Scheduling을 적용함.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **메모리 대역폭(Memory Bandwidth)**: 프로세서 코어 집합이 초당 메인 메모리로부터 읽거나 쓸 수 있는 최대 데이터 전송량(GB/s).
- **일관성 트래픽(Coherence Traffic)**: 사설 캐시 간의 일관성 상태 유지를 위해 인터커넥트에 유입되는 Snoop/Invalidate 패킷 양.
- **코어 확장 기준(Core Scaling Selection Criteria)**: 대상 소프트웨어의 직렬 구간 비율(Amdahl's Law), 메모리 대역폭 제약, 일관성 트래픽 비용을 종합 평가하여 최적의 코어 수와 이종 구성을 선택하는 프레임워크.

</details>

- TLP 여유가 크면 **코어 확장**, 대역폭•일관성 병목이면 **NUMA•패딩** 우선 적용.

#### 한줄 요약
- 직렬 비율과 메모리 병목을 측정하여 코어 수와 배치 방식을 결정함.
