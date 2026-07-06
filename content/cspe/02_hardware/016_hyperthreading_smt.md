---
title: "하이퍼스레딩·SMT (Simultaneous Multithreading)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 16
---

## 미리 알고가기

- 동시 멀티스레딩(Simultaneous Multithreading, SMT): 하나의 물리 코어가 여러 하드웨어 스레드의 명령어를 같은 cycle에 발행하는 방식임
- 하이퍼스레딩(Hyper-Threading): Intel의 SMT 구현 브랜드명임
- Logical processor: 운영체제(Operating System, OS)가 독립 중앙처리장치(Central Processing Unit, CPU)처럼 보는 하드웨어 스레드 실행 문맥임
- Resource contention: 여러 스레드가 cache, execution unit, queue를 공유하며 경쟁하는 현상임

## Ⅰ. 개요

- **정의**: 하이퍼스레딩·SMT는 하나의 물리 코어 안에 여러 논리 프로세서 문맥을 두고 실행 유닛과 캐시 일부를 공유해 여러 스레드 명령을 동시에 처리하는 기술임. 실행 유닛 유휴율, 공유 자원 경합, 보안 격리를 기준으로 적용 효과를 판단함.
- **배경/필요성**: 단일 스레드는 cache miss, branch miss, 의존성 때문에 실행 유닛을 항상 채우지 못함. SMT는 한 스레드가 대기할 때 다른 스레드의 명령을 투입해 코어 처리량을 높이기 위해 도입됨.
- **비유**: 한 작업대에 두 명의 접수원이 번갈아 작업을 올려, 한 사람의 서류가 늦을 때 다른 사람의 일을 처리하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SMT의 처리량 이득과 공유 자원 리스크 판단 | logical processor, shared execution unit, contention, side channel | 물리 코어가 두 배가 된 것으로 설명 |

> 요약: SMT는 물리 코어 수를 늘리는 기술이 아니라 코어 내부 유휴 자원을 여러 스레드가 채우는 기술임.

## Ⅱ. 특징/비교

| 판단 기준 | 멀티코어 | SMT |
|:---|:---|:---|
| 자원 구성 | 코어별 실행 유닛과 일부 캐시를 독립 보유함 | 하나의 코어 실행 유닛과 cache를 논리 스레드가 공유함 |
| 성능 효과 | 병렬 작업이 충분하면 큰 처리량 증가가 가능함 | 유휴 슬롯을 채워 10~30% 수준의 처리량 개선이 흔함 |
| 병목 요인 | 메모리 대역폭, coherence, 동기화 | shared cache, 재정렬 버퍼(Reorder Buffer, ROB), port, execution unit 경합 |
| 적용 기준 | thread 수가 많고 격리가 중요할 때 | latency를 조금 희생하고 throughput을 높일 때 |

> 요약: 멀티코어는 물리 자원 확장이고 SMT는 기존 코어 자원 활용률 개선임.

## Ⅲ. 구성요소

```text
+------------------------------------------------+
|                  Physical Core                 |
| +-------------+        +-------------+         |
| | Thread 0    |        | Thread 1    |         |
| | PC/Regs     |        | PC/Regs     |         |
| +------+------+        +------+------+         |
|        |                      |                |
|        +----------+-----------+                |
|                   v                            |
|       +-----------------------------+          |
|       | Shared Decode/Queues/ALU    |          |
|       | Cache and Execution Ports   |          |
|       +-----------------------------+          |
+------------------------------------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 논리 프로세서 문맥 | 스레드별 PC, architectural register, interrupt 상태를 유지함 | 개인 서류함 |
| 공유 front-end | 여러 스레드의 명령어 fetch/decode 대역폭을 나누어 사용함 | 공용 접수대 |
| 공유 실행 유닛 | ALU, FPU, load/store port를 스레드가 경쟁적으로 사용함 | 공용 설비 |
| 스레드 스케줄러 | cycle마다 어느 스레드 명령을 issue할지 결정함 | 배차 관리자 |

> 요약: SMT는 스레드별 상태는 분리하고 비싼 실행 자원은 공유하는 구조임.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Context  | --> | Fetch    | --> | Issue    | --> | Retire   |
+----------+     +----------+     +----------+     +----------+
 T0/T1 state      mixed stream      shared FU       per thread
```

1. **상태 분리** - 각 논리 스레드의 PC, register, exception 상태를 독립적으로 유지함
2. **명령어 공급** - front-end가 정책에 따라 여러 스레드에서 명령어를 가져오고 decode함
3. **공유 실행** - 준비된 명령어를 shared queue와 execution unit에 경쟁적으로 issue함
4. **스레드별 확정** - 각 스레드는 자기 프로그램 순서에 맞춰 결과를 retire함

> 요약: SMT는 문맥은 분리하고 실행 자원은 공유하여 stall 시간을 다른 스레드로 메우는 절차임.

## Ⅴ. 문제점 및 개선방안

- **P1 성능 간섭**: 두 스레드가 같은 cache, port, memory bandwidth를 쓰면 단일 스레드 성능이 크게 낮아질 수 있음
- **P1 대응**: OS core scheduling, cache allocation, workload pairing으로 경합이 큰 스레드를 분리함 (확인: IPC 변동, LLC miss)
- **P2 보안 취약면**: 공유 cache와 execution port 상태가 timing side channel로 악용될 수 있음
- **P2 대응**: 민감 workload는 SMT 비활성화, core isolation, predictor/cache flush 정책을 적용함 (확인: 보안 기준, 취약점 점검)
- **P3 지연시간 예측 어려움**: 실시간 또는 latency-sensitive workload는 이웃 스레드 상태에 따라 지연이 흔들림
- **P3 대응**: real-time task는 전용 물리 코어에 pinning하고 SMT sibling 배치를 제한함 (확인: p99 latency, jitter)

> 요약: SMT는 처리량 이득 대신 성능 격리, 보안 격리, 지연시간 예측성을 약화시키므로 workload 배치 정책이 핵심임.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 웹 서버 고동시성 처리 | 메모리·입출력 대기가 큰 thread를 동시 멀티스레딩(Simultaneous Multithreading, SMT) sibling으로 배치하되 tail latency 목표가 낮으면 물리 코어 분리를 우선함 | throughput/core, p99 latency, 클록당 명령어 수(Instructions Per Cycle, IPC) 변동 |
| 멀티테넌트 클라우드 | 서로 다른 tenant 또는 민감 workload는 SMT 비활성화나 core scheduling으로 공유 cache·port 노출을 줄임 | side-channel test, 취약점 완화 적용률, co-runner 간 간섭 |
| 실시간·저지연 서비스 | latency-sensitive task를 전용 물리 코어에 pinning하고 SMT sibling 실행을 금지하거나 제한함 | jitter, deadline miss, p95/p99 latency |

> 요약: SMT는 유휴 슬롯이 많고 격리 요구가 낮은 workload에서 켜고, 보안·tail latency가 중요하면 배치 제한이나 비활성화를 검토해야 함.

## Ⅶ. 전망

- **발전 방향**: 서버 CPU는 처리량 확보를 위해 SMT를 유지하되 멀티테넌트와 보안 민감 환경에서는 core scheduling과 공유 자원 격리 기능이 더 중요해짐
- **기술사적 판단**: SMT 효과는 frontend, execution port, ROB, cache, TLB 공유 정도와 workload의 stall 비율에 따라 달라지므로 물리 코어 증설과 구분해 설계함; 단일 thread 대비 throughput, p99 latency, cache miss, port contention, co-runner 간 간섭을 측정해 SMT 활성화 기준을 정함; sibling thread가 공유 캐시와 실행 유닛을 통해 side channel을 만들 수 있어 core scheduling, 격리 배치, 완화 패치 적용 여부를 확인함
- **기술사 제언**: "논리 코어 증가"와 "물리 코어 증가"를 분리하고 처리량 이득, tail latency, side channel 비용을 함께 제시해야 함
