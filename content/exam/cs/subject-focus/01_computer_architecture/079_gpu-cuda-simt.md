---
title: "GPU·CUDA·SIMT (Graphics Processing Unit / Compute Unified Device Architecture / Single Instruction Multiple Threads)"
date: "2026-06-30"
weight: 79
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> GPU(Graphics Processing Unit)는 다수 코어로 대규모 병렬연산을 수행하는 프로세서, CUDA(Compute Unified Device Architecture)는 NVIDIA의 GPGPU 프로그래밍 모델, SIMT(Single Instruction Multiple Threads)는 다수 스레드가 하나의 명령을 병렬 실행하는 실행 방식이다.

## Ⅱ. 구성요소 / 원리
- SM(Streaming Multiprocessor), CUDA 코어, 워프(Warp, 32스레드)
- SIMT: 워프 단위 동일 명령 실행, 분기 시 다이버전스 발생
- 메모리 계층: 레지스터·공유메모리·L2·글로벌(HBM/GDDR)
- 그리드-블록-스레드 계층 구조, 대규모 스레드 컨텍스트 은닉

## Ⅲ. 흐름도 / 구조
```text
[Grid] ─ [Block] ─ [Warp(32 threads)] ─ [Thread]
   │                  │
   └─ SM 분배 ──> SIMT 실행 ──> HBM/공유메모리 접근
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 데이터 병렬·처리량(Throughput) 중심 연산 |
| 장점 | 대규모 병렬성, 높은 FLOPS, 메모리 대역폭 |
| 한계 | 분기 다이버전스, 지연 민감 작업 비효율, 전력 |

## Ⅴ. 기술사적 적용
- CPU(지연중심) 대비 처리량 중심으로 AI 학습·HPC 가속
- 텐서코어와 결합해 행렬연산(GEMM) 가속
- NVLink·GPUDirect로 멀티 GPU 분산학습 확장
