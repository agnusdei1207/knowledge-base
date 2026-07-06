---
title: "비순서 실행·레지스터 리네이밍 (Out-of-Order Execution Register Renaming)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 12
---

## 미리 알고가기

- OoO: 데이터가 준비된 명령어를 프로그램 순서와 다르게 먼저 실행하는 방식임
- Architectural register: ISA에 노출되는 논리 레지스터 이름임
- Physical register: 실제 CPU 내부에서 결과값을 보관하는 물리 저장소임
- ROB: 비순서 실행 결과를 프로그램 순서대로 확정하는 reorder buffer임

## Ⅰ. 개요

- **정의**: 비순서 실행은 데이터 의존성이 없는 명령어를 준비되는 순서대로 먼저 실행하고, 레지스터 리네이밍은 논리 레지스터를 물리 레지스터에 매핑해 가짜 의존성을 제거하는 기법임. ILP 활용률, 정확한 예외, 전력·복잡도를 기준으로 고성능 CPU 적용성을 판단함.
- **배경/필요성**: in-order pipeline은 cache miss나 긴 연산을 만나면 뒤의 독립 명령어까지 함께 대기시킴. OoO와 renaming은 대기 중인 명령어 뒤에 있는 독립 작업을 먼저 실행해 실행 유닛 공백을 줄임.
- **비유**: 번호표 순서대로만 처리하던 창구에서, 준비 서류가 완성된 사람을 먼저 처리하되 최종 결과 발표는 원래 번호 순서대로 하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동적 스케줄링과 가짜 의존성 제거 설명 | RAW/WAR/WAW, RAT, reservation station, ROB | 비순서 실행을 결과 순서 변경으로 오해 |

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
| RAT | architectural register를 physical register로 매핑하는 rename table임 | 이름표 교환대 |
| Physical register file | speculative 결과와 확정 전 값을 보관하는 내부 레지스터 집합임 | 임시 보관함 |
| Reservation station | operand 준비 상태를 추적하고 실행 가능한 명령을 대기시킴 | 작업 대기실 |
| Load-store queue | 메모리 명령의 주소 의존성과 순서를 추적함 | 물류 순번표 |
| ROB | 실행 결과를 원래 순서대로 commit해 정확한 예외를 보장함 | 최종 승인대 |

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

> 요약: 실행은 준비 순서대로 빠르게 하고 상태 반영은 원래 순서대로 해 성능과 정확성을 함께 확보함.

## Ⅴ. 문제점

- **P1 복잡도·전력 증가**: 큰 instruction window, wakeup/select, bypass, ROB가 면적과 동적 전력을 증가시킴
- **P2 메모리 순서 위험**: load/store 주소가 늦게 확정되면 잘못된 speculative load와 memory ordering 오류가 생길 수 있음
- **P3 투기 실행 공격면**: 잘못된 경로의 실행 흔적이 cache나 predictor 상태에 남아 side channel이 될 수 있음

> 요약: OoO의 성능 이득은 하드웨어 복잡도, 메모리 정합성, 보안 부작용을 동반함.

## Ⅵ. 개선방안

- **P1 대응**: window 크기, issue width, power gating을 workload별로 조정하고 복잡도 대비 IPC를 검증함 (확인: IPC/area, perf/W)
- **P2 대응**: load-store queue, memory disambiguation, fence 명령, memory model 검증을 강화함 (확인: ordering test, replay 횟수)
- **P3 대응**: speculation barrier, cache partitioning, predictor flush, 민감 코드의 constant-time 구현을 적용함 (확인: side-channel test)

> 요약: OoO 개선은 더 크게 만드는 것이 아니라 speculation을 통제하고 검증 가능한 범위에서 병렬성을 활용하는 것임.

## Ⅶ. 전망

- **발전 방향**: 고성능 코어는 OoO와 register renaming을 유지하되 energy-aware scheduling과 speculation 완화를 결합하고, 저전력 코어는 제한적 OoO로 차별화됨
- **기술사적 판단**: ROB, issue queue, physical register file, load-store queue 크기는 IPC 이득과 면적·전력·timing closure 비용을 함께 보고 정해야 함; precise exception, interrupt, rollback, load-store violation, memory ordering을 litmus test와 random instruction stream으로 확인함
- **기술사 제언**: WAR/WAW 제거, physical register mapping, ROB 기반 순서 확정을 묶어 비순서 실행의 성능 이득과 검증 부담을 설명해야 함
