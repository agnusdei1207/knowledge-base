---
title: "NPU·TPU (Neural Processing Unit / Tensor Processing Unit, 시스톨릭 어레이)"
date: "2026-06-30"
weight: 80
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> NPU(Neural Processing Unit)는 신경망 연산에 특화된 AI 가속기이며, TPU(Tensor Processing Unit)는 구글이 설계한 텐서 연산 전용 ASIC으로, 시스톨릭 어레이(Systolic Array) 구조로 행렬 곱셈을 고효율 처리한다.

## Ⅱ. 구성요소 / 원리
- 시스톨릭 어레이: PE(Processing Element) 격자, 데이터가 펌프처럼 흐름
- MAC(Multiply-Accumulate) 연산을 파이프라인으로 재사용
- 데이터 재사용 극대화로 메모리 접근·전력 절감
- 저정밀(INT8/BF16) 연산, 전용 명령·온칩 메모리

## Ⅲ. 흐름도 / 구조
```text
       weight↓ weight↓
 data→[PE]→[PE]→  ... 
 data→[PE]→[PE]→  결과 누적
       │     │
   부분합이 격자를 따라 흐르며 MAC 누적
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 행렬·합성곱 연산 전용 가속 |
| 장점 | 높은 연산밀도, 전력효율(TOPS/W), 데이터 재사용 |
| 한계 | 범용성 낮음, 모델 구조 의존, 프로그래밍 제약 |

## Ⅴ. 기술사적 적용
- GPU(범용 병렬) 대비 전력효율·전용성 우위
- 온디바이스 NPU로 모바일·엣지 추론 가속
- TPU Pod·HBM 결합으로 초대규모 모델 학습
