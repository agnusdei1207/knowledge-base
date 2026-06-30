---
title: "CPI·IPC·MIPS·FLOPS (성능 지표)"
date: "2026-06-30"
weight: 13
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> CPU 성능을 정량화하는 지표로, CPI(Cycles Per Instruction)·IPC(Instructions Per Cycle)는 명령어당 효율을, MIPS(Million Instructions Per Second)·FLOPS(Floating-point Operations Per Second)는 처리 속도를 나타낸다.

## Ⅱ. 구성요소 / 원리
- CPI = 총 클럭사이클 수 / 명령어 수 (낮을수록 우수)
- IPC = 1 / CPI = 클럭당 처리 명령어 수 (높을수록 우수)
- MIPS = 명령어 수 / (실행시간 × 10^6) = 클럭주파수 / (CPI × 10^6)
- FLOPS = 초당 부동소수점 연산 수 (과학·HPC 성능 지표)

## Ⅲ. 흐름도 / 구조
```text
 명령어수 ──┐
 클럭사이클─┴▶ CPI = 사이클/명령어 ──▶ IPC = 1/CPI
 주파수 ────▶ MIPS = f / (CPI×10^6)
 부동연산 ──▶ FLOPS (GFLOPS/TFLOPS/PFLOPS)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 프로세서 성능을 정량 비교·평가 |
| 장점 | 측정 간단, 설계·튜닝 목표값 제시 |
| 한계 | MIPS는 ISA 의존(Meaningless Indicator), 실제 워크로드 미반영 |

## Ⅴ. 기술사적 적용
- CPU 성능방정식(시간 = 명령어수 × CPI × 클럭주기)과 직접 연계
- HPC·AI 가속기 성능을 TFLOPS/PFLOPS로 비교(TOP500)
- 벤치마크(SPEC)로 보완하여 실측 성능 평가
