---
title: "VLIW 아키텍처 (VLIW)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 11
---

## 미리 알고가기

- VLIW: Very Long Instruction Word로 여러 독립 연산을 하나의 긴 명령어 묶음에 담는 방식임
- Static scheduling: 실행 순서를 컴파일러가 미리 결정하는 방식임
- Functional unit: ALU, multiplier, load/store처럼 연산을 수행하는 실행 장치임
- NOP: 해당 슬롯에서 수행할 연산이 없음을 나타내는 no operation 명령임

## Ⅰ. 개요

- **정의**: VLIW는 컴파일러가 서로 독립인 여러 연산을 긴 명령어 word의 슬롯에 배치하고 하드웨어는 이를 동시에 실행하는 정적 명령어 병렬 처리 아키텍처임. 컴파일러 분석 능력, 코드 호환성, 실행 유닛 활용률을 기준으로 적용성을 판단함.
- **배경/필요성**: 슈퍼스칼라는 하드웨어가 동적으로 의존성을 찾기 때문에 복잡도와 전력이 증가함. VLIW는 병렬성 탐지 부담을 컴파일러로 옮겨 DSP, 미디어 처리, 임베디드 가속기처럼 예측 가능한 workload에서 전력당 처리량을 얻고자 함.
- **비유**: VLIW는 주방장이 여러 요리사의 작업표를 미리 한 줄에 짜주고, 주방은 그 표대로 동시에 움직이는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 정적 병렬성 배치와 슈퍼스칼라 대비 차이 설명 | compiler scheduling, instruction bundle, functional unit, NOP | 단순 긴 명령어로만 설명 |

> 요약: VLIW는 하드웨어 동적 스케줄링 대신 컴파일러가 병렬 실행 계획을 명령어에 직접 담는 구조임.

## Ⅱ. 특징/비교

| 판단 기준 | 슈퍼스칼라 | VLIW |
|:---|:---|:---|
| 스케줄링 주체 | 하드웨어가 실행 시점에 동적으로 issue함 | 컴파일러가 컴파일 시점에 정적으로 배치함 |
| 하드웨어 복잡도 | dependency check, renaming, ROB가 복잡함 | issue 제어가 단순해 스케줄링 하드웨어 면적과 전력 소모가 작음 |
| 코드 특성 | 같은 binary가 다양한 구현에서 성능을 얻기 쉬움 | functional unit 수와 지연에 binary가 민감함 |
| 적용 기준 | 범용 CPU, 예측 어려운 workload | DSP, 미디어, 통신, 명확한 loop workload |

> 요약: VLIW는 하드웨어 복잡도를 줄이는 대신 컴파일러와 binary 호환성에 성능을 의존함.

## Ⅲ. 구성요소

```text
+--------------+     +-------------------------------+
| Compiler     | --> | VLIW Bundle                   |
| Scheduler    |     | [ALU op][MEM op][MUL op][NOP] |
+--------------+     +---------------+---------------+
                                      |
                                      v
                           +----------+----------+
                           | Functional Units    |
                           +---------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Compiler scheduler | 의존성, 지연, 자원 슬롯을 분석해 연산 배치를 결정함 | 작업표 작성자 |
| Instruction bundle | 여러 operation slot을 하나의 긴 명령어로 묶음 | 묶음 지시서 |
| Functional units | bundle의 각 slot을 동시에 실행하는 연산 장치임 | 담당 요리사 |
| Predicate/NOP | 조건 실행 또는 빈 슬롯을 표현해 제어 흐름과 공백을 처리함 | 조건 메모 |

> 요약: VLIW는 컴파일러가 만든 bundle을 여러 실행 유닛이 lockstep으로 실행하는 구조임.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Analyze  | --> | Schedule | --> | Bundle   | --> | Execute  |
+----------+     +----------+     +----------+     +----------+
 dependency       latency          slot pack        parallel FU
```

1. **의존성 분석** - 컴파일러가 data/control dependency와 functional unit 지연을 분석함
2. **정적 스케줄링** - loop unrolling, software pipelining으로 독립 연산을 노출함
3. **bundle 생성** - 같은 cycle에 실행할 연산을 slot에 배치하고 빈 공간은 NOP로 채움
4. **동시 실행** - 하드웨어는 bundle을 해석해 각 functional unit에 병렬로 투입함

> 요약: VLIW 실행은 컴파일러가 만든 병렬 작업표를 하드웨어가 단순하게 수행하는 과정임.

## Ⅴ. 문제점

- **P1 binary 호환성 취약**: functional unit 수나 latency가 바뀌면 기존 binary의 성능 또는 동작 보장이 어려워짐
- **P2 코드 크기 증가**: 병렬성이 부족한 구간은 NOP slot이 많아져 instruction cache와 메모리 대역폭을 낭비함
- **P3 동적 지연 대응 한계**: cache miss나 분기처럼 실행 시점에 달라지는 지연을 컴파일러가 완전히 예측하기 어려움

> 요약: VLIW는 정적 계획이 정확할 때 강하지만 구현 변화와 동적 이벤트에 약함.

## Ⅵ. 개선방안

- **P1 대응**: 아키텍처 family별 호환 규칙, binary translation, recompile 전략을 제공함 (확인: ABI 호환성, 재컴파일 비용)
- **P2 대응**: instruction compression, predication, software pipelining으로 NOP와 분기 비용을 줄임 (확인: code size, I-cache miss)
- **P3 대응**: profile-guided optimization, predicated execution, limited dynamic scheduling을 결합함 (확인: branch stall, cache miss 영향)

> 요약: VLIW 개선은 컴파일러 최적화와 실행 환경 변화에 대한 보완 장치를 함께 제공해야 함.

## Ⅶ. 전망

- **발전 방향**: VLIW는 범용 CPU 주류보다 DSP, 통신 baseband, edge AI accelerator처럼 반복 루프와 지연 모델이 고정된 영역에서 지속 활용됨
- **기술사적 판단**: instruction bundle 폭, functional unit 수, code size, compiler scheduler 품질, pipeline latency 모델을 함께 맞춰야 전력당 처리량이 나옴; compiler backend가 생성한 schedule, NOP 삽입률, pipeline hazard 가정, 재컴파일 후 binary 동작을 회귀 테스트로 확인함
- **기술사 제언**: VLIW의 핵심은 컴파일러 주도 병렬성이며, binary 호환성 비용과 동적 지연 대응 한계를 함께 제시해야 함
