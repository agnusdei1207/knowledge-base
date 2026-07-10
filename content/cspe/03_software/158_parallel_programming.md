---
title: 병렬 프로그래밍 모델 — OpenMP·MPI (Parallel Programming)
date: 2026-07-05
tags: [cspe-software]
weight: 158
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 대규모 연산을 여러 프로세서에 분산하여 물리적으로 동시 실행하는 모델 |
| 필요성 | 기상 예측, AI 학습, 과학 연산 등 초고성능 컴퓨팅(HPC) 요구 대응 |
| 출제 의도 | 공유 메모리(OpenMP) vs 분산 메모리(MPI) 모델 특성 비교 역량 |

## Ⅱ. 구성요소
```text
[ OpenMP (Shared) ]            [ MPI (Distributed) ]
+-----------------+            +-------+      +-------+
|   CPU1 | CPU2   |            | Node1 | <--> | Node2 |
+-----------------+            +-------+ (NW) +-------+
|  Common Memory  |            | Mem1  |      | Mem2  |
+-----------------+            +-------+      +-------+
```
| 모델 | 특징 | 통신 방식 |
|---|---|---|
| OpenMP | 지시어(Pragma) 기반, 다중 스레드 활용 | 공유 변수 접근 |
| MPI | 명시적 메시지 전달, 다중 프로세스 활용 | Send / Receive API |
| CUDA/OpenCL | GPU 가속기 활용 병렬 처리 | 커널 함수 실행 |
> 요약: OpenMP는 shared-memory thread에 loop·task를 배치하고, MPI는 process별 memory와 message로 cluster 연산을 구성함.

## Ⅲ. 절차
```text
Data Partitioning -> Task Mapping -> Parallel Execution -> Communication
      |                   |                    |                |
(데이터 분할)         (코어 할당)            (연산 수행)      (결과 교환)
```
1. 영역 분할: 전체 연산 데이터를 코어 수에 맞춰 블록 또는 스트라이드 단위로 분해.
2. 병렬 영역 진입: 마스터 스레드가 워커 스레드/프로세스를 포크(Fork)하여 분산.
3. 부분 연산: 각 노드/코어가 할당된 데이터 범위 내에서 독립적으로 계산 수행.
4. 동기화·reduction: barrier·collective로 partial result를 결합하고 dependency 완료를 맞춤.
> 요약: 병렬 프로그램은 data dependency를 분할하고 communication·synchronization·load imbalance 비용을 측정해 speedup을 검증함.

## Ⅳ. 문제점
- 암달의 법칙(Amdahl's Law)에 따라 직렬 영역 존재 시 성능 향상폭이 제한됨.
- 과도한 노드 간 통신(Communication Overhead)이 실제 계산 시간보다 커지는 문제.

## Ⅴ. 개선방안
- 하이브리드 모델(OpenMP+MPI)을 적용하여 노드 내/노드 간 병렬성 동시 확보.
- 비동기 통신 및 연산-통신 중첩(Overlap) 기술을 통해 대기 시간 은닉.

## Ⅵ. 전망
- 이기종 병렬화: CPU-GPU-FPGA를 통합 관리하는 OneAPI 등 단일 프로그래밍 모델 확산.
- 클라우드 HPC: 가상화된 환경에서도 물리 성능에 근접하는 저지연 네트워킹(RDMA) 고도화.
