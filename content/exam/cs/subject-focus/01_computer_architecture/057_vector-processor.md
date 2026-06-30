---
title: "벡터 프로세서 (Vector Processor)"
date: "2026-06-30"
weight: 57
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 단일 명령으로 1차원 배열(벡터) 전체에 대해 동일 연산을 수행하는 SIMD(Single Instruction Multiple Data) 기반 프로세서.

## Ⅱ. 구성요소 / 원리
- 벡터 레지스터(Vector Register): 다수 원소를 한 번에 보관
- 벡터 연산 유닛: 파이프라인화된 다수 연산기로 원소 병렬 처리
- 벡터 길이 레지스터(VLR)·스트라이드(Stride): 처리 길이·메모리 접근 간격 제어
- 체이닝(Chaining): 한 벡터 연산 결과를 다음 연산에 즉시 연결

## Ⅲ. 흐름도 / 구조
```text
VectorLoad A[ ] ─┐
VectorLoad B[ ] ─┤→ [Vector ALU 파이프] → C[ ]
   (1 instr)     └  원소0..N 동시/연속 처리
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 대규모 규칙적 데이터(과학계산·HPC)의 데이터 병렬 처리 |
| 장점 | 명령어 수 감소, 메모리 대역폭 효율, 파이프라인 활용 극대화 |
| 한계 | 불규칙·조건분기 데이터에 비효율, 짧은 벡터엔 오버헤드 |

## Ⅴ. 기술사적 적용
- 슈퍼컴퓨터(Cray)·GPU·CPU의 SIMD 확장(SSE·AVX·SVE)으로 계승
- DLP(Data-Level Parallelism) 실현 핵심 구조
- AI·딥러닝 행렬연산 가속(텐서코어)과 연계
