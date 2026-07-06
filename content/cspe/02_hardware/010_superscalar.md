---
title: "슈퍼스칼라 아키텍처 (Superscalar)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 10
---

## 미리 알고가기

- Issue width: 한 클록에 실행 유닛으로 보낼 수 있는 명령어 수임
- ILP: 하나의 명령어 흐름 안에서 동시에 실행 가능한 독립 명령어 수준 병렬성임
- Rename: 레지스터 이름 충돌을 제거해 병렬 실행 가능한 명령을 늘리는 기법임
- ROB: reorder buffer로 비순서 실행 결과를 프로그램 순서대로 확정하는 구조임

## Ⅰ. 개요

- **정의**: 슈퍼스칼라 아키텍처는 한 클록에 여러 명령어를 fetch, decode, issue, execute할 수 있도록 다수 실행 유닛과 동적 스케줄링 구조를 갖춘 CPU 마이크로아키텍처임. issue width, ILP, 의존성, 전력 비용을 기준으로 성능 향상 가능성을 판단함.
- **배경/필요성**: 클록 주파수만으로 성능을 높이기 어려워지면서 같은 명령어 stream 안의 독립 명령어를 동시에 처리할 필요가 커짐. 슈퍼스칼라는 단일 스레드 성능을 높이기 위해 pipeline 위에 병렬 issue 기능을 추가함.
- **비유**: 한 명의 접수원이 작업을 하나씩 넘기던 공장을 여러 접수원과 여러 설비가 동시에 처리하는 공장으로 바꾸는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 단일 스레드 병렬 실행 구조 판단 | issue width, multiple execution unit, dependency check, ROB | 멀티코어와 혼동 |

> 요약: 슈퍼스칼라는 여러 코어가 아니라 하나의 코어 안에서 여러 명령어를 동시에 실행하는 구조임.

## Ⅱ. 특징/비교

| 판단 기준 | 스칼라 파이프라인 | 슈퍼스칼라 |
|:---|:---|:---|
| 클록당 처리 | 보통 한 클록에 한 명령어 issue를 목표로 함 | 한 클록에 여러 명령어 issue와 실행을 목표로 함 |
| 병렬성 원천 | 단계 중첩으로 처리량을 높임 | ILP를 찾아 독립 명령어를 같은 클록에 실행함 |
| 제어 복잡도 | 해저드 제어가 비교적 단순함 | renaming, issue queue, ROB, bypass가 복잡함 |
| 적용 기준 | 면적·전력 제약이 큰 단순 코어 | 고성능 단일 스레드 처리와 서버·PC CPU |

> 요약: 슈퍼스칼라는 파이프라인 중첩에 명령어 동시 issue를 더해 단일 코어 성능을 확장함.

## Ⅲ. 구성요소

```text
+----------+   +----------+   +----------+   +----------------+
| Fetch N  |-->| Decode N |-->| Rename   |-->| Issue Queue    |
+----------+   +----------+   +----------+   +---+------+-----+
                                                    |      |
                                              +-----v+  +--v----+
                                              | ALU  |  | Load  |
                                              +--+---+  +---+---+
                                                 |          |
                                              +--v----------v--+
                                              | ROB / Retire   |
                                              +----------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Wide fetch/decode | 한 번에 여러 명령어를 가져오고 해석함 | 다중 접수창구 |
| Register renaming | 가짜 의존성을 제거하고 물리 레지스터를 할당함 | 임시 번호표 |
| Issue queue | 준비된 명령어를 실행 유닛별로 대기시키고 선택함 | 작업 대기열 |
| Multiple execution units | ALU, FPU, load/store, branch 유닛을 병렬 배치함 | 여러 설비 |
| ROB | 실행 결과를 원래 순서대로 commit해 정확한 예외를 보장함 | 최종 승인대 |

> 요약: 슈퍼스칼라는 넓은 front-end, 동적 스케줄링, 복수 실행 유닛, 순서 확정 구조로 구성됨.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Fetch N  | --> | Rename   | --> | Issue    | --> | Retire   |
+----------+     +----------+     +----------+     +----------+
                    | dependency removed |
```

1. **묶음 인출** - branch predictor가 제공한 PC 흐름에서 여러 명령어를 한 번에 가져옴
2. **의존성 해소** - register renaming과 dependency check로 병렬 실행 가능한 명령을 구분함
3. **동시 실행** - 준비된 명령어를 여러 실행 유닛에 issue하고 결과를 임시 보관함
4. **순서 확정** - ROB가 예외와 분기 결과를 확인한 뒤 프로그램 순서대로 결과를 commit함

> 요약: 슈퍼스칼라는 명령어 묶음에서 독립성을 찾아 동시에 실행하고 순서대로 확정함.

## Ⅴ. 문제점

- **P1 ILP 한계**: 프로그램에 실제 독립 명령어가 부족하면 issue width를 넓혀도 실행 유닛이 비게 됨
- **P2 하드웨어 복잡도**: wide decode, wakeup/select, bypass network가 면적과 전력을 급격히 증가시킴
- **P3 메모리 병목**: load/store 의존성과 cache miss가 많으면 넓은 실행 유닛을 충분히 활용하지 못함

> 요약: 슈퍼스칼라 성능은 설계 폭이 아니라 실제 ILP와 메모리 공급 능력에 의해 제한됨.

## Ⅵ. 개선방안

- **P1 대응**: OoO 실행, register renaming, compiler scheduling으로 독립 명령어 노출을 늘림 (확인: IPC, issue slot utilization)
- **P2 대응**: clustered execution, selective wakeup, power gating으로 복잡도와 전력을 제어함 (확인: area, dynamic power)
- **P3 대응**: non-blocking cache, prefetcher, memory disambiguation으로 메모리 대기를 줄임 (확인: LLC miss, memory stall)

> 요약: 슈퍼스칼라 개선은 폭 확대보다 ILP 노출과 메모리 지연 숨김이 핵심임.

## Ⅶ. 전망

- **발전 방향**: 슈퍼스칼라는 out-of-order, SMT, 대형 캐시, AI 보조 명령과 결합하되 issue width 확대는 전력과 복잡도 때문에 제한적으로 진행됨
- **기술사적 판단**: decode/issue width, functional unit 수, register renaming, ROB 크기, L1 대역폭을 맞추지 않으면 넓은 발행 폭이 유휴 slot로 남음; `IPC`, issue slot utilization, dependency stall, cache miss, branch miss를 함께 측정해 병렬 발행 이득이 실제 instruction stream에서 발생하는지 확인함
- **기술사 제언**: superscalar는 한 코어의 명령 수준 병렬성, pipeline은 단계 중첩, multicore는 스레드 수준 병렬성으로 구분해 설명해야 함
