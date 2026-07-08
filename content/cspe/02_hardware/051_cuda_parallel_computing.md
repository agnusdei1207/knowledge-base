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

- **정의/개념**: CUDA 병렬 컴퓨팅은 NVIDIA GPU의 SIMT 구조를 대상으로 대량 스레드 실행과 계층형 메모리 활용을 제어해 데이터 병렬 작업을 고속 처리하는 프로그래밍 아키텍처임
- **배경/필요성**: AI 학습과 과학 계산은 동일 연산을 대규모 데이터에 반복 적용하므로, CPU 중심 실행보다 GPU 대량 병렬성을 직접 활용할 수 있는 소프트웨어 계층이 필요함

## Ⅱ. 특징

- 수만 개 경량 스레드를 동시에 실행해 처리량을 크게 높일 수 있음
- shared memory와 stream을 활용하면 연산과 전송을 세밀하게 최적화할 수 있음
- 메모리 접근 패턴과 warp 실행 효율이 실제 성능의 대부분을 좌우함
- NVIDIA 생태계 최적화가 강한 대신 벤더 종속성이 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | CPU 멀티스레딩 | CUDA 병렬 컴퓨팅 | OpenCL, SYCL 계열 |
|:---|:---|:---|:---|
| 대상 하드웨어 | 범용 CPU | NVIDIA GPU | 다중 벤더 |
| 최적화 깊이 | 낮음~중간 | 매우 높음 | 중간 |
| 이식성 | 높음 | 낮음 | 높음 |
| 대표 용도 | 제어 중심 병렬 | 대규모 데이터 병렬 | 범용 GPGPU |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Grid, Block, Thread | 작업을 계층적으로 분할해 SM에 배치하며 block 구조가 동기화와 메모리 공유 범위를 결정함 |
| Global, Shared, Register Memory | 메모리 계층별 속도와 용량 차이가 커서 데이터 배치를 잘못하면 병목이 커짐 |
| Warp Scheduler | 준비된 워프를 교차 실행해 메모리 지연을 숨기고 occupancy를 높임 |
| Stream, Runtime API | 커널 실행과 메모리 복사를 비동기로 겹쳐 시스템 전체 처리량을 높임 |

```text
+-------------+     +-------------+     +------------------+     +-------------+
| Grid/Block  | --> | Warp Sched. | --> | Memory Hierarchy | --> | Stream/API  |
+-------------+     +-------------+     +------------------+     +-------------+
```

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

## Ⅵ. 문제점 및 해결 방안

1. 문제: 글로벌 메모리 접근이 흩어지면 coalescing이 깨져 대역폭을 제대로 쓰지 못해 성능이 급락할 수 있음
   - 해결방안: 데이터 레이아웃을 연속적으로 재배치하고 global memory throughput과 load efficiency로 검증함
2. 문제: host와 device 간 전송이 많으면 커널 속도가 빨라도 end-to-end 지연은 줄지 않을 수 있음
   - 해결방안: pinned memory와 stream overlap을 적용하고 PCIe transfer time과 total latency로 개선 효과를 검증함
3. 문제: CUDA 전용 최적화는 높은 성능을 주지만 특정 벤더 종속으로 유지보수 부담이 커질 수 있음
   - 해결방안: 핵심 커널만 CUDA 특화하고 나머지는 이식 가능한 계층으로 분리하며 portability cost와 speedup으로 전략을 검증함

## Ⅶ. 적용 사례

- 딥러닝 학습 파이프라인에서는 텐서 연산 커널을 GPU에서 실행하고 확인 지표는 training throughput과 GPU utilization임
- 과학 시뮬레이션에서는 격자 연산을 block 단위로 병렬화하고 확인 지표는 time to solution과 scalability임
- 비디오 분석 서비스에서는 전처리와 추론을 stream으로 중첩하고 확인 지표는 frame latency와 throughput임

## Ⅷ. 결론

CUDA의 핵심 가치는 GPU 코어 수 자체보다 메모리 계층과 스레드 배치를 얼마나 잘 맞추느냐에 있으므로, 커널 구조와 데이터 이동 최적화가 설계의 중심이 되어야 함.
