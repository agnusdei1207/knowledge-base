---
title: "CUDA 병렬 컴퓨팅 (CUDA Parallel Computing)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 51
extra:
  question_no: "051"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- CUDA는 NVIDIA GPU용 병렬 프로그래밍 모델과 실행 플랫폼임
- 병렬 구조는 grid, block, thread와 memory hierarchy로 구성됨
- 성능 핵심은 occupancy, memory coalescing, stream overlap임

## Ⅰ. 개요

- **정의/개념**: CUDA 병렬 컴퓨팅은 NVIDIA GPU의 SIMT 구조에서 대량 스레드 실행과 계층형 메모리 활용을 제어해 데이터 병렬 작업을 처리하는 프로그래밍 아키텍처임
- **배경/필요성**: AI 학습과 과학 계산은 동일 연산을 대규모 데이터에 반복 적용하므로, CPU 중심 실행보다 GPU 대량 병렬성을 직접 활용할 수 있는 소프트웨어 계층이 필요함

## Ⅱ. 특징

- 수만 개 경량 스레드를 동시에 실행해 처리량을 늘릴 수 있음
- shared memory와 stream을 활용하면 연산과 전송을 세밀하게 최적화할 수 있음
- 메모리 접근 패턴과 warp 실행 효율이 실제 성능의 대부분을 좌우함
- NVIDIA 생태계 최적화가 깊은 대신 벤더 종속성이 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | CPU 멀티스레딩 | CUDA 병렬 컴퓨팅 | OpenCL, SYCL 계열 |
|:---|:---|:---|:---|
| 대상 하드웨어 | 범용 CPU | NVIDIA GPU | 다중 벤더 |
| 최적화 깊이 | 낮음~중간 | 가장 깊음 | 중간 |
| 이식성 | 높음 | 낮음 | 높음 |
| 대표 용도 | 제어 중심 병렬 | 대규모 데이터 병렬 | 범용 GPGPU |

> 요약: CUDA는 NVIDIA GPU에 깊게 최적화되지만 이식성은 OpenCL·SYCL보다 낮음.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Grid, Block, Thread | 작업을 계층적으로 분할해 SM에 배치하며 block 구조가 동기화와 메모리 공유 범위를 결정함 |
| Global, Shared, Register Memory | 메모리 계층별 속도와 용량 차이가 있어 데이터 배치 오류가 병목으로 이어짐 |
| Warp Scheduler | 준비된 워프를 교차 실행해 메모리 지연을 숨기고 SM 유휴 시간을 줄임 |
| Stream, Runtime API | 커널 실행과 메모리 복사를 비동기로 겹쳐 전송 대기 시간을 줄임 |

```text
+-------------+     +-------------+     +------------------+     +-------------+
| Grid/Block  | --> | Warp Sched. | --> | Memory Hierarchy | --> | Stream/API  |
+-------------+     +-------------+     +------------------+     +-------------+
```

> 요약: CUDA 성능은 grid/block 배치, 메모리 계층, warp scheduler, stream 중첩이 함께 결정함.

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 데이터 준비    | --> | 커널 배치      | --> | GPU 병렬 실행  | --> | 결과 회수/후처리 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **데이터 준비**: 호스트가 GPU 메모리와 커널 인자를 준비함
2. **커널 배치**: grid와 block 크기를 정해 커널을 실행함
3. **GPU 병렬 실행**: 워프 단위로 스레드가 같은 명령을 병렬 처리함
4. **결과 회수 및 후처리**: 출력 데이터를 회수하고 상위 로직에 반영함

> 요약: 호스트가 데이터와 커널을 준비하면 GPU가 워프 단위로 병렬 실행하고 결과를 반환함.

## Ⅵ. 실무 적용 및 유의점

1. 딥러닝·비디오 분석은 global memory 접근이 흩어지면 처리량이 떨어지므로 block 배치와 shared memory를 조정하고 load efficiency, GPU utilization으로 확인함
2. 호스트-GPU 복사가 잦은 파이프라인은 커널 최적화만으로 지연이 줄지 않으므로 pinned memory와 stream overlap을 적용하고 PCIe transfer time, total latency로 확인함

## Ⅶ. 결론

CUDA는 GPU 코어 수보다 메모리 계층과 스레드 배치를 얼마나 잘 맞추느냐가 성능을 좌우하므로 커널 구조와 데이터 이동을 함께 최적화해야 함.

## 작성 근거(검토용)

- CUDA는 SIMT 실행, grid/block/thread, memory hierarchy, stream을 핵심 축으로 설명함
- 비교 기준은 NVIDIA 최적화 깊이, 이식성, 대상 하드웨어로 제한함
- 실무 판단은 load efficiency, GPU utilization, PCIe transfer time으로 검증 가능하게 작성함
