---
title: "비순서 실행·레지스터 리네이밍 (Out-of-Order Execution Register Renaming)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 12
---

## 미리 알고가기

- 비순서 실행(Out-of-Order Execution, OoO): 데이터가 준비된 명령어를 프로그램 순서와 다르게 먼저 실행하는 방식임
- Architectural register: 명령어 집합 구조(Instruction Set Architecture, ISA)에 노출되는 논리 레지스터 이름임
- Physical register: 실제 CPU 내부에서 결과값을 보관하는 물리 저장소임
- 재정렬 버퍼(Reorder Buffer, ROB): 비순서 실행 결과를 프로그램 순서대로 확정하는 큐임

## Ⅰ. 개요

- **정의**: 비순서 실행은 데이터 의존성이 없는 명령어를 준비되는 순서대로 먼저 실행하고, 레지스터 리네이밍은 논리 레지스터를 물리 레지스터에 매핑해 가짜 의존성을 제거하는 기법임. ILP 활용률, 정확한 예외, 전력·복잡도를 기준으로 고성능 CPU 적용성을 판단함.
- **배경/필요성**: in-order pipeline은 cache miss나 긴 연산을 만나면 뒤의 독립 명령어까지 함께 대기시킴. OoO와 renaming은 대기 중인 명령어 뒤에 있는 독립 작업을 먼저 실행해 실행 유닛 공백을 줄임.
- **비유**: 번호표 순서대로만 처리하던 창구에서, 준비 서류가 완성된 사람을 먼저 처리하되 최종 결과 발표는 원래 번호 순서대로 하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동적 스케줄링과 가짜 의존성 제거 설명 | 읽기 후 쓰기(Read After Write, RAW), 쓰기 후 읽기(Write After Read, WAR), 쓰기 후 쓰기(Write After Write, WAW), 레지스터 별칭 테이블(Register Alias Table, RAT), 재정렬 버퍼(Reorder Buffer, ROB) | 비순서 실행을 결과 순서 변경으로 오해 |

> 요약: OoO는 실행 순서를 바꾸고 renaming은 가짜 레지스터 충돌을 제거하지만 commit은 프로그램 순서로 수행함.

## Ⅱ. 특징/비교

| 판단 기준 | In-order 실행 | OoO + Register Renaming |
|:---|:---|:---|
| 실행 순서 | 프로그램 순서대로 issue와 실행을 진행함 | operand가 준비된 명령어를 먼저 실행함 |
| 의존성 처리 | RAW 중심으로 단순 stall을 적용함 | RAW는 유지하고 WAR/WAW는 renaming으로 제거함 |
| 성능 기준 | 구조가 단순하고 예측 가능한 지연시간을 가짐 | ILP와 memory latency hiding으로 IPC를 높임 |
| 적용 기준 | MCU, 실시간, 저전력 코어 | PC, 서버, 고성능 모바일 big core |

> 요약: OoO는 단순성과 결정성을 희생하고 평균 처리량과 단일 스레드 성능을 높이는 선택임.

## Ⅲ. 구성요소

```text
+----------+   +----------+   +-----------+   +-----------+
| Decode   |-->| Rename   |-->| Schedule  |-->| Execute   |
+----------+   +----+-----+   +-----+-----+   +-----+-----+
                   |               |               |
              +----v----+     +----v----+     +----v----+
              | RAT/PRF |     | RS/LSQ  |     |  ROB    |
              +---------+     +---------+     +---------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 레지스터 별칭 테이블(Register Alias Table, RAT) | architectural register를 physical register로 매핑하는 rename table임 | 이름표 교환대 |
| 물리 레지스터 파일(Physical Register File, PRF) | speculative 결과와 확정 전 값을 보관하는 내부 레지스터 집합임 | 임시 보관함 |
| 예약 스테이션(Reservation Station, RS) | operand 준비 상태를 추적하고 실행 가능한 명령을 대기시킴 | 작업 대기실 |
| 로드-스토어 큐(Load-Store Queue, LSQ) | 메모리 명령의 주소 의존성과 순서를 추적함 | 물류 순번표 |
| 재정렬 버퍼(Reorder Buffer, ROB) | 실행 결과를 원래 순서대로 commit해 정확한 예외를 보장함 | 최종 승인대 |

> 요약: OoO 구조는 rename, 대기열, 실행 유닛, ROB가 협력해 비순서 실행과 순서 확정을 분리함.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+     +----------+
| Decode   | --> | Rename   | --> | Dispatch | --> | Execute  | --> | Retire   |
+----------+     +----------+     +----------+     +----------+     +----------+
```

1. **명령어 해석** - opcode와 source/destination register를 식별함
2. **레지스터 치환** - RAT가 destination에 새 physical register를 할당하고 가짜 의존성을 제거함
3. **동적 스케줄링** - reservation station이 operand 준비 상태를 보고 실행 가능한 명령을 선택함
4. **실행과 확정** - 실행 결과를 ROB에 저장하고 예외가 없으면 프로그램 순서대로 commit함

> 요약: 실행은 operand 준비 순서대로 먼저 수행하고 상태 반영은 원래 순서대로 해 IPC와 정확한 예외를 함께 확보함.

## Ⅴ. 문제점 및 개선방안

- **P1 복잡도·전력 증가**: 큰 instruction window, wakeup/select, bypass, ROB가 면적과 동적 전력을 증가시킴
- **P1 대응**: window 크기, issue width, power gating을 workload별로 조정하고 복잡도 대비 클록당 명령어 수(Instructions Per Cycle, IPC)를 검증함 (확인: IPC/area, perf/W)
- **P2 메모리 순서 위험**: load/store 주소가 늦게 확정되면 잘못된 speculative load와 memory ordering 오류가 생길 수 있음
- **P2 대응**: load-store queue, memory disambiguation, fence 명령, memory model 검증을 강화함 (확인: ordering test, replay 횟수)
- **P3 투기 실행 공격면**: 잘못된 경로의 실행 흔적이 cache나 predictor 상태에 남아 side channel이 될 수 있음
- **P3 대응**: speculation barrier, cache partitioning, predictor flush, 민감 코드의 constant-time 구현을 적용함 (확인: side-channel test)

> 요약: OoO의 성능 이득은 하드웨어 복잡도, 메모리 정합성, 보안 부작용을 동반하므로 병렬성 확대와 투기 통제를 함께 검증해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 서버·PC 고성능 코어 | 재정렬 버퍼(Reorder Buffer, ROB), 레지스터 별칭 테이블(Register Alias Table, RAT), 예약 스테이션(Reservation Station, RS) 크기를 workload의 memory stall과 명령어 수준 병렬성(Instruction-Level Parallelism, ILP)에 맞춰 정하고 정확한 예외와 rollback 경로를 검증함 | 클록당 명령어 수(Instructions Per Cycle, IPC), ROB occupancy, precise exception test |
| 메모리 지연 은닉이 큰 데이터 처리 | 로드-스토어 큐(Load-Store Queue, LSQ)와 memory disambiguation으로 독립 load/store를 먼저 실행하되 fence와 ordering rule로 오실행을 회수함 | replay 횟수, ordering litmus test, load miss penalty |
| 보안 민감 실행 환경 | 민감 코드 구간은 speculation barrier와 cache partitioning을 적용하고 co-runner 간 timing leak을 점검함 | side-channel test, predictor flush coverage, p99 latency 변화 |

> 요약: OoO는 단일 스레드 성능이 중요한 코어에서 효과가 크지만 commit 순서, memory ordering, side-channel 검증이 적용 조건임.

## Ⅶ. 전망

- **발전 방향**: 고성능 코어는 OoO와 register renaming을 유지하되 energy-aware scheduling과 speculation 완화를 결합하고, 저전력 코어는 제한적 OoO로 차별화됨
- **기술사적 판단**: ROB, issue queue, physical register file, load-store queue 크기는 IPC 이득과 면적·전력·timing closure 비용을 함께 보고 정해야 함; precise exception, interrupt, rollback, load-store violation, memory ordering을 litmus test와 random instruction stream으로 확인함
- **기술사 제언**: WAR/WAW 제거, physical register mapping, ROB 기반 순서 확정을 묶어 비순서 실행의 성능 이득과 검증 부담을 설명해야 함
