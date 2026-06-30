---
title: "성능방정식 (CPU Performance Equation)"
date: "2026-06-30"
weight: 14
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> CPU 실행시간을 명령어 수·CPI(Cycles Per Instruction)·클럭주기의 곱으로 표현하여 성능 결정 요인을 정량화한 식이다.

## Ⅱ. 구성요소 / 원리
- CPU 실행시간 = 명령어 수(IC) × CPI × 클럭주기(T)
- = (IC × CPI) / 클럭주파수(f)
- IC(Instruction Count): ISA·컴파일러가 결정
- CPI: 마이크로아키텍처(파이프라인·구조)가 결정
- 클럭주기/주파수: 반도체 공정·회로 설계가 결정

## Ⅲ. 흐름도 / 구조
```text
 [컴파일러/ISA] → 명령어수(IC)
 [마이크로아키텍처]→ CPI         ┐
 [공정/클럭]    → 클럭주기(T)    │
        실행시간 = IC × CPI × T ─┘
        성능 = 1 / 실행시간
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 성능 결정 3요소 분리·최적화 방향 제시 |
| 장점 | 설계 트레이드오프(IC↓ vs CPI↓ vs f↑) 명확화 |
| 한계 | 세 인자가 상호 의존, 단일 인자만 개선 시 역효과 가능 |

## Ⅴ. 기술사적 적용
- RISC(IC↑·CPI↓) vs CISC(IC↓·CPI↑) 설계 철학 비교 근거
- 파이프라인·슈퍼스칼라로 CPI 개선(IPC↑)
- 암달의 법칙과 결합하여 전체 시스템 성능 분석
