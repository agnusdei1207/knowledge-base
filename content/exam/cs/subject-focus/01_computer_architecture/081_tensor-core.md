---
title: "텐서코어 (Tensor Core)"
date: "2026-06-30"
weight: 81
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 텐서코어(Tensor Core)는 GPU 내부에 탑재되어 행렬 곱셈-누적(MMA, Matrix Multiply-Accumulate)을 한 클록에 처리하는 전용 연산 유닛이다.

## Ⅱ. 구성요소 / 원리
- 4×4 등 소행렬 단위 MMA를 단일 연산으로 수행: D = A×B + C
- 혼합정밀(Mixed Precision): FP16/BF16 입력, FP32 누적
- 저정밀 지원: TF32, FP8, INT8로 처리량 향상
- 워프 단위 협력(WMMA API)으로 다수 스레드가 분담

## Ⅲ. 흐름도 / 구조
```text
 [A 4x4]×[B 4x4] ─MMA─> [부분곱]
                          + [C 누적]
                          = [D 결과]  (1 클록 처리)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 딥러닝 GEMM·합성곱 가속 |
| 장점 | CUDA코어 대비 수배 처리량, 혼합정밀 효율 |
| 한계 | 정밀도 손실 우려, 행렬연산에 국한 |

## Ⅴ. 기술사적 적용
- 일반 CUDA 코어 대비 행렬연산 특화로 학습·추론 가속
- Transformer Engine(FP8)으로 LLM 학습 효율화
- NPU·TPU의 시스톨릭 어레이와 유사한 데이터 재사용 철학
