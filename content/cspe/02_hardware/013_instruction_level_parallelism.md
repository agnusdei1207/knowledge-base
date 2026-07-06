---
title: "명령어 수준 병렬성 ILP (Instruction-Level Parallelism)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 13
---

## 미리 알고가기

- ILP: 하나의 instruction stream 안에서 동시에 실행 가능한 독립 명령어의 정도임
- Basic block: 분기 없이 순차 실행되는 명령어 구간임
- Dependency graph: 명령어 사이의 데이터와 제어 의존성을 그래프로 표현한 구조임
- IPC: 클록당 완료 명령어 수로 ILP 활용 결과를 보여주는 지표임

## Ⅰ. 개요

- **정의**: 명령어 수준 병렬성은 하나의 프로그램 흐름 안에서 데이터와 제어 의존성이 없어 같은 시간에 실행할 수 있는 명령어의 양을 나타내는 성능 기준임. 컴파일러 스케줄링, 파이프라인, 슈퍼스칼라, OoO 설계가 실제로 성능을 낼 수 있는지를 판단하는 데 쓰임.
- **배경/필요성**: 클록 주파수 향상과 단일 pipeline만으로는 성능 확장이 제한됨. CPU는 프로그램 내부의 독립 명령어를 찾아 여러 실행 유닛에 배치해야 단일 스레드 처리량을 높일 수 있음.
- **비유**: 한 요리 레시피에서 먼저 해야 하는 작업과 동시에 할 수 있는 작업을 구분해 여러 조리대에 나누는 정도임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CPU 병렬성의 원천과 한계 판단 | data/control dependency, compiler scheduling, OoO, IPC | ILP를 멀티스레딩과 혼동 |

> 요약: ILP는 한 스레드 안에서 동시에 실행 가능한 명령어를 얼마나 찾고 활용하는지의 기준임.

## Ⅱ. 특징/비교

| 판단 기준 | ILP | TLP/DLP |
|:---|:---|:---|
| 병렬성 단위 | 하나의 스레드 안의 독립 명령어 | 여러 스레드 또는 여러 데이터 원소 |
| 활용 장치 | pipeline, superscalar, OoO, VLIW | multicore, SMT, SIMD, GPU |
| 제한 요인 | RAW 의존성, branch, memory alias | 동기화, 데이터 분할, 메모리 대역폭 |
| 선택 기준 | 단일 스레드 지연시간 개선이 필요할 때 | 처리량 확장과 대규모 병렬성이 필요할 때 |

> 요약: ILP는 단일 스레드 성능의 원천이고, TLP/DLP는 작업 또는 데이터 단위 확장의 원천임.

## Ⅲ. 구성요소

```text
+--------------+     +----------------+     +----------------+
| Instruction  | --> | Dependency     | --> | Scheduler      |
| Stream       |     | Graph          |     | HW or Compiler |
+--------------+     +--------+-------+     +-------+--------+
                              |                     |
                              v                     v
                         +---------+          +-------------+
                         | ILP Set | -------> | Exec Units  |
                         +---------+          +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 명령어 흐름 | 컴파일러 또는 CPU가 분석하는 순차 명령어 집합임 | 작업 목록 |
| 의존성 그래프 | 어떤 명령어가 먼저 실행되어야 하는지 표현함 | 선후 관계표 |
| 스케줄러 | 독립 명령어를 찾아 실행 순서와 실행 유닛을 배정함 | 배차 담당 |
| 실행 유닛 | 독립 명령어를 실제로 병렬 실행하는 ALU, FPU, load/store 장치임 | 작업 설비 |

> 요약: ILP는 의존성 분석으로 독립 작업을 찾고 스케줄러가 실행 유닛에 배치하는 구조로 활용됨.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Analyze  | --> | Expose   | --> | Schedule | --> | Measure  |
+----------+     +----------+     +----------+     +----------+
 dependency       unroll/rename    issue order      IPC/stall
```

1. **의존성 분석** - RAW, WAR, WAW, memory dependency, branch dependency를 식별함
2. **병렬성 노출** - loop unrolling, renaming, instruction reordering으로 독립 명령어를 드러냄
3. **실행 배치** - compiler 또는 하드웨어가 실행 유닛과 cycle에 명령어를 배정함
4. **효과 측정** - IPC, stall cycle, issue slot utilization으로 실제 활용률을 확인함

> 요약: ILP 활용은 의존성을 줄이고 독립 명령어를 드러낸 뒤 실행 폭에 맞게 배치하는 과정임.

## Ⅴ. 문제점

- **P1 실제 의존성 한계**: 알고리즘 자체에 긴 RAW chain이 있으면 하드웨어가 아무리 넓어도 병렬 실행할 수 없음
- **P2 제어·메모리 불확실성**: branch 방향과 load/store alias가 늦게 확정되면 안전한 재배치가 어려움
- **P3 수익 체감**: issue width와 window를 키울수록 추가 IPC는 줄고 전력·면적 비용은 증가함

> 요약: ILP는 프로그램 구조와 불확실성 때문에 무한히 늘릴 수 없고 비용 대비 효과가 빠르게 줄어듦.

## Ⅵ. 개선방안

- **P1 대응**: 알고리즘 재구성, loop unrolling, strength reduction, vectorization 전환을 검토함 (확인: dependency chain 길이, IPC)
- **P2 대응**: branch prediction, predication, memory disambiguation, profile-guided optimization을 적용함 (확인: branch miss, replay)
- **P3 대응**: superscalar 폭, OoO window, cache 대역폭을 workload별 PPA 기준으로 제한함 (확인: IPC/area, perf/W)

> 요약: ILP 개선은 의존성 제거와 하드웨어 폭 확대의 비용 대비 효과를 함께 봐야 함.

## Ⅶ. 전망

- **발전 방향**: 단일 스레드 ILP 확장은 전력과 복잡도 한계로 완만해지고, CPU는 ILP·TLP·DLP·전용 가속을 혼합해 성능을 확보함
- **기술사적 판단**: issue width, pipeline depth, branch predictor, register renaming은 dependency chain 길이와 메모리 지연을 기준으로 함께 설계해야 함; peak issue width가 아니라 `IPC`, issue slot utilization, dependency stall, memory stall을 실제 workload에서 측정해 ILP 한계를 판단함
- **기술사 제언**: ILP를 파이프라인, 슈퍼스칼라, VLIW, OoO를 묶는 상위 개념으로 설명하면 병렬성 계층 구조가 선명해짐
