---
title: "부울대수·카르노맵 (Boolean Algebra & Karnaugh Map)"
date: "2026-06-30"
weight: 1
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 부울대수(Boolean Algebra)는 0/1 두 값과 AND·OR·NOT 연산으로 논리식을 다루는 대수 체계이며, 카르노맵(Karnaugh Map, K-map)은 인접 셀의 1을 묶어 논리식을 시각적으로 간소화하는 도표 기법이다.

## Ⅱ. 구성요소 / 원리
- 기본연산: AND(·), OR(+), NOT(') — 곱·합·보수의 세 연산
- 기본법칙: 교환·결합·분배·항등(A+0=A, A·1=A), 보수(A+A'=1)
- 드모르간(De Morgan): (A·B)'=A'+B', (A+B)'=A'·B'
- K-map: 2^n 셀을 그레이코드(Gray code) 순서로 배치, 인접 1끼리 2^k개 묶음(group)
- 묶음 클수록 변수 소거 ↑ → 최소 곱의합(SOP, Sum Of Products) 도출

## Ⅲ. 흐름도 / 구조
```text
진리표 ─▶ 부울식 도출 ─▶ [대수 간소화] ──┐
                                          ├─▶ 최소 논리식 ─▶ 게이트 구현
진리표 ─▶ K-map 작성 ─▶ [인접 1 묶기] ───┘
   AB\C  0   1
   00  [ 1 ][ 1 ]   ← 인접 묶음으로 변수 제거
   01  [ 0 ][ 1 ]
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 논리회로 최소화로 게이트 수·비용·지연 감소 |
| 장점 | 대수=규칙기반 정확, K-map=직관적 시각화로 4변수까지 빠름 |
| 한계 | 대수는 경험 의존, K-map은 5변수 이상 비실용(→ Quine-McCluskey) |

## Ⅴ. 기술사적 적용
- 4변수 초과 시 Quine-McCluskey 또는 Espresso 알고리즘으로 자동 최소화
- 디지털 IC·FPGA 합성 도구의 논리 최적화(Logic Synthesis) 기반 이론
- 무관항(Don't care)을 활용한 추가 간소화로 면적·전력 최적 설계
