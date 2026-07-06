---
title: "CUDA 병렬 컴퓨팅 (CUDA Parallel Computing)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 51
---

## Ⅰ. 개요
- **정의**: GPU의 수천 개 코어를 C/C++ 확장 API로 범용 병렬 연산에 활용하는 플랫폼
- **배경/필요성**: CPU의 직렬 처리만으로는 대규모 행렬·벡터 연산의 처리량 한계가 존재하여, 데이터 병렬성을 활용할 수 있는 프로그래밍 모델이 필요함
- **비유**: 한 명의 숙련 요리사(CPU)가 순서대로 요리하는 대신, 수천 명의 보조(GPU 코어)가 같은 레시피를 동시에 수행하는 구조

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GPU 병렬 프로그래밍 모델 이해 | 커널-스레드-블록-그리드 계층 구조 | 메모리 계층(Global/Shared/Register) 누락 시 감점 |

> 요약: GPU 코어를 범용 병렬 연산에 활용하는 프로그래밍 플랫폼임

## Ⅱ. 구성요소
```text
        +--- Grid -------------------+
        |  +--- Block 0 ---+         |
        |  | Thread 0,1..N |         |
        |  | Shared Memory |         |
        |  +---------------+         |
        |  +--- Block 1 ---+         |
        |  | Thread 0,1..N |         |
        |  | Shared Memory |         |
        |  +---------------+         |
        +----------------------------+
                  |
           Global Memory (DRAM)
                  |
            Host (CPU) Memory
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Kernel | GPU에서 실행되는 함수 단위, `__global__` 키워드로 선언 | 모든 작업자에게 배포되는 작업 지시서 |
| Thread | 커널을 실행하는 최소 실행 단위, 고유 `threadIdx` 보유 | 개별 작업자 한 명 |
| Block | 스레드를 묶는 논리 단위, 블록 내 Shared Memory 공유 | 같은 작업대를 공유하는 팀 |
| Grid | 블록의 집합으로 커널 1회 호출에 대응 | 전체 공장의 팀 배치도 |
| Global Memory | 모든 스레드가 접근 가능한 DRAM, 대용량이나 지연 400~800 cycle | 중앙 창고 |
| Shared Memory | 블록 내 스레드가 공유하는 온칩 SRAM, 지연 1~2 cycle | 팀 전용 작업대 서랍 |
| Register | 스레드 전용 초고속 저장소, 용량 제한(스레드당 수십 개) | 작업자 손에 쥔 도구 |

> 요약: 커널-그리드-블록-스레드 실행 계층과 Register-Shared-Global 메모리 계층으로 구성됨

## Ⅲ. 절차
```text
  Host 코드 준비     디바이스 전송     커널 실행         결과 회수
  (CPU 메모리 할당)  (Host->Device)   (Grid/Block 런칭)  (Device->Host)
       |                 |                 |                 |
       +-- cudaMalloc -->+-- cudaMemcpy -->+-- kernel<<<>>>->+
     데이터 초기화    Global Mem 적재   SM별 블록 스케줄링   결과 복사
```
- 1단계: Host에서 입력 데이터를 준비하고 `cudaMalloc`으로 GPU 메모리를 할당함
- 2단계: `cudaMemcpy`로 Host 메모리의 데이터를 Device Global Memory에 복사함
- 3단계: `kernel<<<gridDim, blockDim>>>()`로 커널을 런칭하여 SM이 블록 단위로 스케줄링 실행함
- 4단계: 연산 결과를 `cudaMemcpy`로 Device에서 Host로 복사하고 GPU 메모리를 해제함

> 요약: 메모리 할당 → 데이터 전송 → 커널 실행 → 결과 회수의 4단계로 동작함

## Ⅳ. 문제점
- 메모리 전송 병목: Host-Device 간 PCIe 대역폭 제한(~64 GB/s) — 연산 대비 데이터 이동 시간이 지배적이 되어 전체 속도 저하
- Warp Divergence: 같은 Warp(32스레드) 내 분기 발생 시 직렬 실행 — 분기 경로가 다른 스레드가 순차 처리되어 병렬성 손실
- Shared Memory 뱅크 충돌: 동일 뱅크에 다중 스레드 접근 시 직렬화 — 메모리 접근 지연이 증가하여 처리량 감소

> 요약: 데이터 전송 병목, 분기 발산, 메모리 뱅크 충돌이 병렬 효율을 저하시킴

## Ⅴ. 개선방안
1. 단기: CUDA Stream과 비동기 전송으로 연산-통신 오버랩 적용하여 전송 병목 완화
2. 중기: 분기 최소화 알고리즘 설계 및 Warp-level Primitive 활용으로 Divergence 감소
3. 장기: Unified Memory·CXL 연결 등 메모리 아키텍처 통합으로 전송·뱅크 충돌 근본 해소

> 요약: 비동기 전송, 분기 최소화, 통합 메모리 아키텍처로 단계적 개선이 필요함

## Ⅵ. 전망
- 발전 방향: Multi-Instance GPU(MIG) 등 GPU 가상화와 대규모 LLM 학습용 멀티 GPU 클러스터로 확대
- 기술사적 판단: AI·HPC 워크로드 증가로 CUDA 생태계의 중요성은 지속 확대되나, 벤더 종속 리스크 고려 필요
- 기술사 제언: OpenCL·SYCL 등 개방형 표준과의 병행 전략 수립 및 메모리 계층 최적화 역량 확보 권고
