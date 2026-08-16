---
sidebar:
  order: 13
  label: "013. 캐시 쓰기 정책: Write-Through vs Write-Back (Cache Write Policy)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "캐시 쓰기 정책: Write-Through vs Write-Back (Cache Write Policy)"
date: "2026-08-13T11:35:24+09:00"
tags:
  - "notes-hardware"
weight: 13
extra:
  question_no: "013"
  source_status: "기출"
  source_history: "129회, 135회"
  priority: 70
  priority_note: "반복 기출, 쓰기 일관성•대역폭 절충"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **캐시 쓰기 정책(Cache Write Policy)**: CPU가 메모리 쓰기(Store) 연산을 수행할 때, 갱신된 데이터를 고속 캐시 메모리와 하위 계층(DRAM 메인 메모리 / 하위 캐시)에 어떤 시점과 구조로 반영할지 결정하는 메모리 일관성 정책 규격.
- **쓰기 트래픽(Write Traffic)**: 캐시 계층에서 하위 메모리 버스로 발생하는 쓰기 데이터 패킷 전송량 및 대역폭 점유율.
- **미반영 위험(Write-Back Risk)**: Write-Back 정책 사용 중 캐시에만 갱신된 최신 데이터(Dirty Line)가 남아있을 때 전원 차단(Power Loss)이나 DMA 장치 접근 발생 시 최신 데이터가 유실/오염될 수 있는 보안 및 안정성 위험.

</details>

- 정의/개념: 데이터 쓰기(Store) 연산 발생 시 캐시 메모리와 메인 메모리 하위 계층 간의 데이터 업데이트 시점을 제어하는 **캐시 쓰기 정책** (Write-Through vs Write-Back).
- 배경/필요성: 모든 쓰기를 메인 메모리에 즉시 반영하면 버스 **쓰기 트래픽** 급증으로 프로세서 대기 발생, 반대로 캐시에만 미루면 전원 장애 시 **미반영 위험**과 캐시 비일관성이 발생하므로 상충 관계(Trade-off) 최적화 필요.

#### 한줄 요약
- 쓰기 데이터의 하위 계층 동기화 시점을 제어하여 버스 전송 대역폭 절감과 데이터 일관성을 절충하는 메모리 관리 규격.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **쓰기 할당(Write Allocate)**: 쓰기 미스(Write Miss) 발생 시 해당 메인 메모리 블록을 캐시 라인으로 먼저 적재(Fetch)한 후 쓰기 연산을 수행하는 정책.
- **쓰기 비할당(No-Write Allocate / Write-Around)**: 쓰기 미스 발생 시 캐시에 데이터를 적재하지 않고 메인 메모리에 직접 기록하는 정책.
- **쓰기 지역성(Write Locality)**: 동일한 캐시 라인 주소 영역에 짧은 시간 간격으로 연속적인 Store 연산이 집중되는 메모리 참조 특성.
- **더티 비트(Dirty Bit)**: 해당 캐시 라인의 내용이 하위 메인 메모리 값과 달라 최신 상태임을 나타내는 1비트 태그 상태 플래그.
- **즉시 쓰기(Write-Through, WT)**: 캐시 메모리 갱신과 동시에 하위 메인 메모리에도 즉시 데이터를 기록하는 일관성 정책.
- **후기입(Write-Back, WB)**: 캐시 메모리에만 먼저 쓰고 **더티 비트(Dirty Bit)**를 1로 설정한 뒤, 향후 해당 라인이 축출(Eviction)될 때 비로소 하위 메모리에 반영하는 정책.
- **WB 병합(Write Combining)**: 동일 캐시 라인에 대해 수십 번의 쓰기가 일어나도 축출 시점에 단 1번만 메인 메모리로 전송하는 병합 효과.

</details>

- **쓰기 할당**과 **쓰기 비할당** 미스 처리 정책을 결합하여 가동.
- **쓰기 지역성**이 뛰어난 애플리케이션일수록 **Write-Back(WB)**을 통해 **WB 병합(Write Combining)** 효과를 발휘하여 버스 트래픽 대폭 절감.
- Write-Back 구조에서는 **더티 비트**를 추적 관리하여 축출 시점에만 선택적 메모리 덮어쓰기 구동.

#### 한줄 요약
- Write-Through는 메모리 즉시 동기화, Write-Back은 Dirty Bit 기반 축출 시점 병합 쓰기를 통해 대역폭 효율성을 확보함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **캐시 배열(Cache Array)**: 태그 메모리, 데이터 메모리, Valid Bit, Dirty Bit 상태 플래그를 저장하는 SRAM 물리 배열.
- **쓰기 버퍼(Write Buffer)**: Write-Through 정책에서 CPU가 메인 메모리 쓰기 완료를 기다리지 않고 연속 연산을 진행할 수 있도록 쓰기 요청을 임시 큐잉하는 FIFO 버퍼.
- **버퍼 포화(Buffer Saturation)**: 연속적인 Write-Through 요청 속도가 쓰기 버퍼 배출 속도를 초과하여 버퍼가 꽉 채워져 CPU가 파이프라인 Stall에 빠지는 상태.
- **쓰기 정책 제어 로직(Write Policy Logic)**: Store 명령 수신 시 Hit/Miss 여부 및 WT/WB 설정에 따라 경로를 선택하는 하드웨어 로직.

</details>

```text
[ Cache Write Policy Control Architecture ]
 ├─ Write-Through Path
 │  ├─ Cache Array
 │  ├─ Write Buffer
 │  └─ Lower Memory
 └─ Write-Back Path
    ├─ Cache Array
    ├─ Dirty Bit
    └─ Eviction Buffer
```

| 구성요소 | 책임 |
|:---|:---|
| 쓰기 정책 제어 로직 | **WT·WB·할당 정책** 경로 선택 |
| 더티 비트 | WB 라인의 **하위 계층 미반영** 상태 표시 |
| 쓰기 버퍼 | 하위 계층 쓰기 요청을 **비동기 큐잉** |
| 하위 메모리 계층 | WT 요청•WB 축출 라인의 **최종 저장** |

#### 한줄 요약
- Write Policy Controller, Dirty Bit 추적기, FIFO Write Buffer를 구동하여 하위 메모리로의 전송 지연을 은닉함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **더티 축출(Dirty Eviction)**: Write-Back 캐시에서 새로운 라인을 적재하기 위해 Dirty Bit=1인 기존 캐시 라인을 비울 때, 해당 데이터를 하위 메모리로 밀어 넣는 작업.
- **캐시 플러시(Cache Flush)**: DMA 통신 전 또는 전원 차단 전에 캐시 내의 모든 Dirty Line을 메인 메모리로 강제 플러시 반영하는 유지 관리 연산.

</details>

```text
[ CPU Store Instruction (Write Request) ]
                    │
                    ▼
             [ 설정된 쓰기 정책 ]
                    ├─ Write-Through (WT)
                    │   캐시 라인 갱신
                    │   Write Buffer 적재 ──> 하위 계층 전송
                    │
                    └─ Write-Back (WB)
                        캐시 라인 갱신 및 Dirty Bit = 1
                        축출 시 Dirty Line ──> 하위 계층 전송
```

### 동작 원리

- **Write-Through 동작**: 캐시 갱신과 함께 **Write Buffer**로 요청을 전송함.
- **Write-Back 동작**: 캐시만 수정하고 **Dirty Bit**를 설정함.
- **더티 축출**: 교체할 Dirty Line을 하위 계층에 기록함.

#### 한줄 요약
- WT는 Write Buffer 기반 즉시 전송을 수행하고, WB는 Dirty Bit 갱신 후 라인 교체 시점에 선택적 Dirty Eviction을 수행함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **즉시 가시성(Immediate Visibility)**: 쓰기 즉시 하위 메모리나 외부 I/O 장치가 최신 데이터를 그대로 관측할 수 있는 성질.
- **쓰기 병합(Write Combining)**: 동일 캐시 라인 내의 무수한 수정 사항을 캐시 메모리 내부에서 하나로 병합하여 최종 결과만 1회 전송하는 효과.
- **더티 데이터(Dirty Data)**: 캐시에만 존재하고 메인 메모리에는 아직 반영되지 않은 일시적 불일치 최신 데이터.

</details>

| 비교 항목 | Write-Through (WT) | Write-Back (WB) |
|:---|:---|:---|
| **메모리 동기화 시점** | 캐시 갱신 시 **즉시 동기화** (Immediate) | 캐시 라인 축출(Eviction) 시 **지연 동기화** (Deferred) |
| **메모리 버스 트래픽** | 높음 (매 Store 연산마다 버스 쓰기 발생) | 매우 낮음 (**Write Combining** 효과 발휘) |
| **하드웨어 구현** | 단순함 (Dirty Bit 불필요, **Write Buffer** 필요) | 복잡함 (**Dirty Bit** 제어 및 Eviction 로직 필요) |
| **데이터 일관성** | **즉시 가시성** 확보 (메인 메모리가 항상 최신) | 캐시-메모리 불일치 발생 (**Dirty Data** 존재) |
| **미스 정책 조합** | 주로 No-Write Allocate 방식과 결합 | 주로 Write Allocate 방식과 결합 |
| **주요 적용 위치** | 단순 MCU 캐시•일부 I/O 메모리 경로 | 범용 고성능 CPU의 데이터 캐시 계층 |

#### 한줄 요약
- Write-Through는 메모리 즉시 가시성과 구현 단순성에 강점을 가지며, Write-Back은 쓰기 대역폭 절감 및 성능 최적화에 강점을 가짐.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **비일관성 DMA(Non-Coherent DMA)**: 하드웨어 캐시 일관성 장치가 없는 임베디드 SoC에서 DMA 장치가 메모리를 직접 읽을 때 캐시 데이터와 불일치가 발생하는 현상.
- **메모리 장벽(Memory Barrier / Fence)**: 쓰기 버퍼에 대기 중인 메모리 연산이 완전히 전송될 때까지 후속 메모리 연산을 지연시키는 명령 (`DMB`, `DSB`).
- **캐시 정리(Cache Clean)**: DMA 전송 전 캐시 내의 Dirty Line을 메인 메모리로 강제 기록하는 하드웨어 maintenance 명령.
- **캐시 무효화(Cache Invalidate)**: DMA 수신 후 오래된 캐시 데이터를 파기하여 메인 메모리의 최신 수신값을 읽도록 만드는 maintenance 명령.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| Write-Through 사용 시 연속 쓰기로 인한 **버퍼 포화** 및 CPU Stall | FIFO **쓰기 버퍼** 깊이 확장 및 Write-Back 정책으로 전환 | 쓰기 트래픽 병목 해소 및 CPU 대기 시간 방지 |
| Write-Back 환경에서 전원 손실 시 **더티 데이터** 유실 | 플랫폼 지속성 도메인 보장 및 종료 전 캐시 **Flush** | 지속성 경계까지 완료된 쓰기 보존 |
| **비일관성 DMA** 주변장치가 캐시의 최신 데이터를 읽지 못해 통신 오류 | DMA 전송 직전 **Cache Clean**, 수신 직후 **Cache Invalidate** 수행 | CPU-DMA 장치 간의 데이터 일관성 완벽 보장 |
| 멀티코어 환경에서 쓰기 순서 교란으로 인한 메모리 레이스 조건 | **메모리 장벽** 명령 명시적 사용 | 코어 간 쓰기 관측 순서 보장 및 메모리 펜스 유지 |

#### 한줄 요약
- Non-Coherent DMA 대응 Cache Clean/Invalidate, Memory Barrier 적용 및 Power-loss 대비 Flush 절차를 구동함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **쓰기 정책 선택 기준(Write Policy Selection Criteria)**: 시스템의 대역폭 제약, 데이터 정합성 요구, 전원 백업 능력 및 DMA 하드웨어 일관성 유무를 평가하여 최적의 쓰기 아키텍처를 결정하는 프레임워크.

</details>

- 쓰기 지역성이 높으면 **WB•Write Allocate**, 즉시 하위 반영이면 **WT** 선택.

#### 한줄 요약
- 대역폭•가시성•DMA 일관성을 기준으로 쓰기와 할당 정책을 결정함.
