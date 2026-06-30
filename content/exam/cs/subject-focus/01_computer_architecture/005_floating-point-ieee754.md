---
title: "부동소수점 (Floating Point, IEEE 754 / FP32·FP16·bfloat16)"
date: "2026-06-30"
weight: 5
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 부동소수점은 실수를 부호·지수·가수로 나누어 표현하는 방식으로, IEEE 754(Institute of Electrical and Electronics Engineers 754)는 그 표준 포맷과 연산 규칙을 정의한다.

## Ⅱ. 구성요소 / 원리
- 구성: (−1)^부호(Sign) × 1.가수(Mantissa) × 2^(지수(Exponent)−bias)
- 정규화(Normalized): 가수 앞 암시적 1(hidden bit) 가정
- 바이어스(Bias): FP32=127, FP16=15, bfloat16=127
- 특수값: ±0, ±∞, NaN(Not a Number), 비정규화 수(Denormal)
- 반올림(Rounding): 최근접 짝수(Round to Nearest Even) 기본

## Ⅲ. 흐름도 / 구조
```text
FP32(32b): [S 1][ Exponent 8 ][   Mantissa 23   ]  범위↑정밀↑
FP16(16b): [S 1][ Exp 5 ][  Mantissa 10  ]         메모리↓
bf16(16b): [S 1][ Exponent 8 ][ Mantissa 7 ]        FP32 범위 유지
값 = (-1)^S × 1.M × 2^(E - bias)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 넓은 동적 범위의 실수를 고정 비트로 근사 표현 |
| 장점 | 표준 호환, bf16=지수 8b로 FP32 범위 유지하며 메모리 절반 |
| 한계 | 반올림 오차·결합법칙 비성립, FP16=지수 5b로 범위 좁음 |

## Ⅴ. 기술사적 적용
- AI/딥러닝 학습: bfloat16이 FP16 대비 오버플로 적어 선호(TPU·GPU)
- 혼합정밀도(Mixed Precision) 연산으로 속도·메모리·정확도 균형
- FP8(E4M3/E5M2) 등 초저정밀 포맷으로 추론 가속 확산
