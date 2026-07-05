---
title: "CUDA 병렬 컴퓨팅 (CUDA Parallel Computing)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 51
---

## Ⅰ. 개요
- **정의**: GPU의 수천 개 코어를 범용 연산에 활용하는 NVIDIA의 병렬 프로그래밍 플랫폼
- **배경/필요성**: CPU 단일 스레드 성능 향상이 한계에 도달하여, 데이터 병렬성이 높은 연산을 GPU로 오프로드할 구조가 필요함
- **비유**: CPU가 숙련된 요리사 1명이라면, GPU는 단순 작업을 동시에 처리하는 수천 명의 보조 요리사임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GPU 병렬처리 구조 이해 | Thread-Block-Grid 계층과 SIMT 실행 모델 | SIMD와 SIMT의 차이를 혼동하지 않을 것 |

> 요약: GPU의 대규모 스레드를 범용 연산에 활용하는 병렬 컴퓨팅 플랫폼임

## Ⅱ. 구성요소
```text
Host (CPU)                      Device (GPU)
  |                               |
  +-- Host Memory                 +-- Global Memory
  |                               |
  +-- CUDA Runtime API            +-- Grid
       |                               |
       +-- Kernel Launch               +-- Block 0 --- Block 1 --- Block N
                                            |
                                            +-- Thread 0, 1, ... 255
                                            |
                                            +-- Shared Memory
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Kernel | GPU에서 실행되는 병렬 함수 단위 | 작업 지시서 |
| Thread | 커널을 실행하는 최소 실행 단위 | 개별 작업자 |
| Block | Thread를 묶은 실행 그룹으로 Shared Memory를 공유함 | 같은 테이블의 작업조 |
| Grid | Block의 집합으로 하나의 Kernel 호출에 대응함 | 전체 작업 현장 |
| Warp | 32개 Thread를 동시에 실행하는 SIMT 스케줄링 단위 | 일렬로 행진하는 32명 |
| Shared Memory | Block 내 Thread 간 공유하는 저지연 온칩 메모리 | 작업조 공용 칠판 |
| Global Memory | 모든 Thread가 접근 가능한 대용량 오프칩 메모리 | 공용 창고 |

> 요약: Host-Device 구조 위에 Thread-Block-Grid 계층으로 대규모 병렬성을 표현함

## Ⅲ. 절차
```text
CPU 코드 실행 --> 데이터 전송(Host->Device) --> Kernel 실행 --> 결과 전송(Device->Host)
     |                    |                         |                    |
     v                    v                         v                    v
  입력 준비         cudaMemcpy H2D           Grid/Block 할당       cudaMemcpy D2H
```
- 1단계: Host에서 입력 데이터를 준비하고 Device 메모리를 `cudaMalloc`으로 할당함
- 2단계: `cudaMemcpy`로 Host 메모리에서 Device Global Memory로 데이터를 전송함
- 3단계: Kernel을 `<<<Grid, Block>>>` 구성으로 호출하여 GPU 스레드가 병렬 연산을 수행함
- 4단계: 연산 결과를 `cudaMemcpy`로 Device에서 Host로 복사하고 Device 메모리를 해제함

> 요약: Host-Device 간 데이터 전송과 Kernel 실행의 4단계 사이클로 동작함

## Ⅳ. 문제점
- 메모리 전송 병목: Host-Device 간 PCIe 대역폭이 GPU 연산 속도 대비 낮아 전체 처리량이 제한됨
- Warp Divergence: 조건 분기 시 Warp 내 Thread가 다른 경로를 실행하여 직렬화가 발생함
- 벤더 종속: NVIDIA GPU에서만 실행 가능하여 하드웨어 선택지가 제한됨

> 요약: 메모리 전송 병목, 분기 직렬화, 벤더 종속이 주요 한계임

## Ⅴ. 개선방안
1. 단기: Unified Memory, CUDA Stream을 활용하여 연산과 전송을 오버랩함
2. 중기: Warp 단위 최적화와 Shared Memory 타일링으로 분기·메모리 접근 패턴을 개선함
3. 장기: SYCL, OpenCL 등 크로스 플랫폼 프레임워크 병행으로 벤더 종속을 완화함

> 요약: 전송 오버랩, 워프 최적화, 크로스 플랫폼 전환으로 단계적 개선이 필요함

## Ⅵ. 전망
- 발전 방향: GPU 메모리 대역폭 확대(HBM4)와 NVLink(056 참조) 연동으로 멀티 GPU 스케일아웃이 가속됨
- 기술사적 판단: AI 학습·추론 워크로드 증가로 CUDA 생태계 의존도가 당분간 유지될 전망임
- 기술사 제언: CUDA 최적화 역량과 크로스 플랫폼 이식성을 동시에 확보하는 전략이 필요함
