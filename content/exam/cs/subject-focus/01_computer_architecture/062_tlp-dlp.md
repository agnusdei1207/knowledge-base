---
title: "TLP·DLP (Thread-Level / Data-Level Parallelism)"
date: "2026-06-30"
weight: 62
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 병렬성 추출 단위에 따른 분류로, 다수 스레드를 동시 실행하는 스레드 수준 병렬성(TLP)과 단일 명령으로 다수 데이터를 처리하는 데이터 수준 병렬성(DLP).

## Ⅱ. 구성요소 / 원리
- TLP(Thread-Level Parallelism): 독립 스레드·프로세스를 멀티코어/SMT로 병렬 실행
- DLP(Data-Level Parallelism): 동일 연산을 다수 데이터에 SIMD/벡터로 적용
- ILP(명령어 병렬성)와 함께 병렬성 계층 형성
- TLP는 작업 분할·동기화, DLP는 데이터 정렬·벡터화가 핵심

## Ⅲ. 흐름도 / 구조
```text
[TLP] Thread0│Thread1│Thread2 → Core0 Core1 Core2
[DLP] 1 instr → [d0 d1 d2 d3] 동시 처리 (SIMD)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 다중 실행단위 활용으로 처리량·성능 향상 |
| 장점 | TLP=독립작업 확장성 / DLP=규칙적 대량연산 효율 |
| 한계 | TLP=동기화·경쟁 / DLP=불규칙·분기 데이터 비효율 |

## Ⅴ. 기술사적 적용
- TLP → 멀티코어·SMT(Hyper-Threading), 멀티스레드 SW
- DLP → 벡터 프로세서·GPU·AVX/SVE
- 딥러닝: DLP(행렬연산)+TLP(다중 GPU) 결합
