---
title: "다중프로그래밍과 다중처리 (Multiprogramming & Multiprocessing)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 19
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **다중프로그래밍과 다중처리** | 다중프로그래밍과 다중처리 (Multiprogramming & Multiprocessing)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **다중프로그래밍 (Multiprogramming)**: **하나의 CPU**에서 여러 프로그램을 메모리에 올려두고, I/O 대기 시간 동안 다른 프로그램을 실행하여 CPU 이용률을 높이는 방식. (CPU 1개, 효율 극대화)
- **다중처리 (Multiprocessing)**: **여러 개의 CPU(코어)**가 여러 작업을 동시에 진짜로 처리하는 방식. (CPU N개, 속도 극대화)
- **시분할 (Time Sharing)**: 다중프로그래밍의 발전형으로, CPU를 아주 짧은 시간 간격으로 쪼개서 여러 사용자에게 나눠줌으로써 마치 나 혼자 컴퓨터를 쓰는 듯한 느낌을 줌.

## 깊이 이해
- **발전 단계**: Single Tasking -> Multiprogramming (I/O 대기 활용) -> Time Sharing (응답성 확보) -> Multiprocessing (병렬 처리).
- **Multiprocessing의 분류**:
    - **Symmetric (SMP)**: 모든 CPU가 대등하게 메모리와 I/O를 공유. 현대 PC/서버의 표준.
    - **Asymmetric (ASMP)**: 주(Master) CPU가 스케줄링을 하고 종(Slave) CPU가 명령을 따름.
- **Amdahl의 법칙**: 다중처리에서 CPU를 아무리 늘려도, 프로그램 중 병렬화할 수 없는 부분(순차 실행 부분) 때문에 전체 성능 향상에는 한계가 있다는 법칙.
- **가치**: 
    - **Multiprogramming**: 비싼 CPU가 놀지 않게 함.
    - **Multiprocessing**: 연산 능력을 물리적으로 확장.

## 연결 개념
- **Process vs Thread (001)**: 다중처리를 활용하는 소프트웨어적 단위.
- **Context Switching (002)**: 다중프로그래밍에서 CPU 주인이 바뀔 때 발생하는 비용.
- **Amdahl's Law**: 다중처리 시스템 설계의 경제적 가이드라인.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중프로그래밍은 단일 자원의 **이용률(Utilization)** 극대화를, 다중처리는 다수 자원을 통한 **병렬성(Parallelism)** 확보를 목표로 하는 실행 모델임.
> 2. **기술적 핵심**: 다중프로그래밍은 I/O Wait 기반의 문맥 전환을 활용하며, 다중처리는 공유 메모리 구조(SMP)와 캐시 일관성(Cache Coherency) 제어가 핵심임.
> 3. **판단**: 처리량(Throughput)이 중요하면 다중프로그래밍 최적화를, 단일 작업의 연산 속도(Latency)가 중요하면 다중처리 병렬화를 선택함.

## Ⅰ. 시스템 동시성의 진화, Multiprogramming과 Multiprocessing 개요

- **Multiprogramming**: 한정된 CPU 자원을 효율적으로 쓰기 위해 여러 프로세스를 메모리에 상주시키고 I/O 대기 시 CPU를 양도하는 방식.
- **Multiprocessing**: 여러 프로세서(CPU/Core)를 사용하여 다수의 작업을 동시에(True Parallelism) 실행하는 방식.

## Ⅱ. Multiprogramming vs Multiprocessing 비교

### 1. 기술적 상세 비교표
| 비교 항목 | 다중프로그래밍 (Multiprogramming) | 다중처리 (Multiprocessing) |
|:---:|:---|:---|
| **CPU 개수** | 1개 (Single Processor) | 2개 이상 (Multi Processor) |
| **핵심 목표** | **CPU 이용률(Utilization) 극대화** | **처리 속도 및 처리량 극대화** |
| **동작 원리** | I/O 발생 시 Context Switch | 병렬 실행 (Parallel Execution) |
| **구현 방식** | 시분할(Time Sharing) 연계 | SMP, ASMP, NUMA |
| **신뢰성** | CPU 장애 시 전체 시스템 마비 | 일부 CPU 장애 시 성능 저하 후 유지 |

### 2. 관련 개념 확장 (Time Sharing)
- **시분할(Time Sharing)**: 다중프로그래밍 기술을 사용자 관점의 응답성 중심으로 발전시킨 기술. Time Quantum(Slot) 단위로 CPU를 강제 전환.

## Ⅲ. 다중처리(Multiprocessing)의 구조적 분류

### 1. SMP (Symmetric Multiprocessing)
- **특징**: 모든 CPU가 하나의 공유 메모리와 I/O를 평등하게 접근. 
- **과제**: 공유 메모리 접근 경합(Contention) 및 캐시 일관성(Cache Coherency) 유지.

### 2. NUMA (Non-Uniform Memory Access)
- **특징**: CPU마다 로컬 메모리를 두고, 다른 CPU의 메모리는 원격으로 접근.
- **장점**: CPU 수가 늘어나도 메모리 버스 병목이 적어 확장성 우수.

## Ⅳ. 성능 한계 분석: 암달의 법칙 (Amdahl's Law)

- **공식**: $Speedup = \frac{1}{(1-P) + \frac{P}{N}}$
    - $P$: 병렬화 가능한 비율, $N$: 프로세서 수.
- **시사점**: 아무리 CPU를 수만 개 투입해도, 병렬화 불가능한 부분($1-P$)이 10%만 존재하면 성능 향상은 최대 10배를 넘지 못함. (자원 투입 대비 한계 수확 체감)

## Ⅴ. 다중프로그래밍의 효율 지표: CPU 이용률 계산
- **이용률 = $1 - p^n$**
    - $p$: 프로세스가 I/O에 머무는 시간의 비율, $n$: 프로세스 수.
    - 프로세스 수($n$)가 늘어날수록 CPU가 놀 확률($p^n$)이 기하급수적으로 줄어듦.

## Ⅵ. 기술사 관점의 결론 및 제언
- 현대 컴퓨팅은 **'다중프로그래밍으로 자원을 알뜰히 쓰고, 다중처리로 물리적 한계를 넘는'** 혼합 구조임.
- **실무 제언**: 멀티코어 성능을 온전히 활용하려면 소프트웨어 레벨에서 **Lock-free 알고리즘**을 적용하여 동기화 병목을 제거하고, 데이터 독립성을 높여 **병렬화 가능 비율(P)**을 극대화하는 설계가 필수적임.

---
### 🔀 문제 유형별 목차 전환
| 유형 | 강조 포인트 | 추천 목차 구성 |
|:---:|:---|:---|
| **비교형** | 두 개념의 정의와 차이점 | Ⅱ.상세 비교표, Ⅰ.개요 |
| **구조형** | SMP, NUMA 등 하드웨어 구조 | Ⅲ.다중처리 구조적 분류 |
| **성능형** | 암달의 법칙과 성능 한계 | Ⅳ.암달의 법칙, Ⅴ.이용률 계산 |
