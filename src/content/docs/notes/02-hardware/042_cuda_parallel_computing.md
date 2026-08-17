---
sidebar:
  order: 42
  label: "042. CUDA 병렬 컴퓨팅 (CUDA Parallel Computing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "CUDA 병렬 컴퓨팅 (CUDA Parallel Computing)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 42
extra:
  question_no: "042"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "커널•메모리•스트림 최적화의 기출 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CUDA(Compute Unified Device Architecture)**: NVIDIA GPU의 병렬 연산 코어들을 범용 컴퓨팅(GPGPU)에 활용할 수 있도록 지원하는 C/C++ 기반 병렬 소프트웨어 플랫폼.
- **Host(호스트)**: 전체 제어 흐름을 관리하고 CUDA 커널을 호출하는 CPU 및 메인 시스템.
- **Device(디바이스)**: 대규모 스레드 병렬성으로 커널 연산을 고속 실행하는 GPU 가속기.

</details>

- 정의/개념: C/C++ 기반으로 Host(CPU)와 Device(GPU)의 이기종 협업 구조에서 대규모 스레드 계층(Grid/Block/Thread)과 메모리 계층을 제어하여 초병렬 연산을 구현하는 병렬 컴퓨팅 플랫폼
- 배경/필요성: CPU 직렬 처리의 대역폭 한계를 극복하고, **수천 개의 GPU 코어를 일반 프로그래밍 모델로 활용하여 AI 및 과학 시뮬레이션 처리 가속화**

#### 한줄 요약

- Host/Device 구조에서 **Grid·Block·Thread 계층으로 GPU 대규모 병렬성 제어**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Kernel(커널)**: GPU의 수천~수만 개 스레드가 각자의 데이터에 대해 병렬 실행하는 전용 함수(`__global__`).
- **Grid / Block / Thread**: 최상위 그리드(Grid) $\to$ SM에 매핑되는 스레드 블록(Block) $\to$ 최하위 스레드(Thread)의 3단계 실행 계층.
- **CUDA Stream**: GPU에서 비동기 명령(메모리 복사, 커널 실행)을 순차 실행하는 FIFO 작업 대기열.

</details>

- 제어 집약적 작업(Host)과 대규모 데이터 병렬 작업(Device)을 엄격히 분리하는 **이종 컴퓨팅 아키텍처**
- 수백만 개의 병렬 작업을 체계적으로 분산하는 **Grid $\to$ Block $\to$ Thread** 3단계 계층적 매핑 모델
- 데이터 전송과 연산을 동시에 중첩 실행하여 오버헤드를 은닉하는 **비동기 CUDA Stream** 및 **이벤트(Event)** 동기화

#### 한줄 요약

- **Grid-Block-Thread 계층·Shared Memory 타일링·비동기 CUDA Stream 파이프라이닝**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Shared Memory**: 동일 스레드 블록 내 스레드들이 초저지연으로 공유하는 온칩 SRAM.
- **Global Memory**: GPU 보드에 탑재된 대용량 VRAM(GDDR6, HBM3).

</details>

```text
[ CUDA 소프트웨어 및 하드웨어 계층 구조도 ]
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ Host (CPU 시스템)            │        │ Device (NVIDIA GPU)          │
│  ├─ Host Memory (DRAM)       │        │  ├─ Global Memory (VRAM)     │
│  └─ CUDA Driver / Runtime API│        │  └─ Streaming Multiprocessors│
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │ (PCIe / NVLink 트랜잭션)              │
               ▼                                       ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ CUDA 비동기 스트림 (Streams) │ ──(제어)─>│ Grid (Kernel Execution)      │
│  ├─ Stream 1: [H2D]─[K1]─[D2H]│       │  ├─ Block (0,0) ~ Block (N,M)│
│  └─ Stream 2: [H2D]─[K2]─[D2H]│       │  │   └─ Warps (32 Threads)   │
└──────────────────────────────┘        └──────────────────────────────┘
```

선의 의미: Host(CPU) 런타임, 비동기 CUDA Stream, Device(GPU) SM 스레드 계층 및 장치 메모리 계층 간의 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 호스트 런타임 | 장치 메모리 공간 할당, 데이터 입출력 전송 제어 및 GPU **커널** 함수 실행 런칭의 총괄 관리 |
| 쿠다 스트림 | 명령어 비동기 대기열 큐잉 및 수많은 커널 연산의 실행 순서와 꼬여있는 의존성 철저 제어 |
| 커널 실행 계층 | **스트리밍 멀티프로세서** 물리 코어 상에 **그리드** 및 **블록** 단위의 스레드 병렬 우겨넣기 배치 |
| 장치 메모리 계층 | 극초고속 레지스터, **공유 메모리**, 느려터진 전역 메모리를 통한 계층적 텐서 데이터 피딩 공급 |

#### 한줄 요약

- **Host 런타임·비동기 CUDA Stream·Grid/Block/Thread 디스패치·계층적 메모리**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **H2D / D2H (Host-to-Device / Device-to-Host)**: CPU 메모리와 GPU VRAM 간 PCIe 버스를 통한 데이터 복사 방향.

</details>

```text
[ 비동기 CUDA Stream 파이프라인 흐름 ]
                         │
                         ▼
   [ 1. CUDA Stream 및 동기화 Event 객체 생성 ]
                         │
                         ▼
   [ 2. 비동기 Host-to-Device(H2D) 데이터 전송 (cudaMemcpyAsync) ]
                         │
                         ▼
   [ 3. GPU SM 상에 커널 Grid 런치 (<<<Grid, Block, Stream>>>) ]
                         │
                         ▼
   [ 4. 커널 완료 Event 기록 및 후속 작업 의존성 동기화 ]
                         │
                         ▼
   [ 5. 비동기 Device-to-Host(D2H) 결과 전송 (cudaMemcpyAsync) ]
```

**동작 원리**

1. **스트림 초기화**: 복수의 독립 비동기 CUDA Stream과 동기화 Event 생성
2. **비동기 H2D 전송**: 고정 호스트 메모리(Pinned Memory)로부터 GPU VRAM으로 입력 텐서 비동기 복사
3. **커널 런치**: SM에 스레드 블록을 디스패치하여 32개 스레드 단위 Warp 병렬 연산 가속
4. **이벤트 트리거**: 커널 연산 완료 시 Event를 발생시켜 대기 중인 후속 작업 큐의 잠금 해제
5. **비동기 D2H 전송**: 계산된 출력 텐서를 Host 메인 메모리로 비동기 인출하여 결과 반환

#### 한줄 요약

- Stream 생성 $\to$ **비동기 H2D 복사 $\to$ 커널 Grid 런치 $\to$ 이벤트 동기화 $\to$ D2H 복사**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CUDA vs OpenCL/SYCL vs OpenMP**:
  - CUDA: NVIDIA GPU 전용 최고 성능 및 생태계 (cuDNN, TensorRT)
  - SYCL: Khronos 오픈 표준 단일 소스 C++ 이종 컴퓨팅
  - OpenMP: CPU 멀티코어 지시어 기반 병렬화 표준

</details>

| 비교 항목 | NVIDIA CUDA | 오픈 표준 OpenCL / SYCL | CPU 멀티스레딩 (OpenMP) |
|:---|:---|:---|:---|
| 프로그래밍 모델 및 타깃 | C/C++ 기반 GPU 전용, Grid/Block/Thread 모델 | 단일 소스 C++ 이종 가속기(CPU/GPU/FPGA) 모델 | Fork-Join 기반 CPU 멀티코어 공유 메모리 병렬화 |
| 최적화 수준 및 생태계 | NVIDIA GPU 극대화 최적화 (cuDNN, TensorRT) | 범용 이식성 우수, 벤더별 하드웨어 최적화 한계 | 복잡한 제어 흐름 및 분기 집약적 워크로드에 최적 |
| 한계 및 종속성 | 특정 벤더(NVIDIA) 하드웨어 강력한 종속성(Lock-in) | 벤더별 드라이버 파편화 및 상대적 라이브러리 부족 | 수십 개 코어 한계로 인한 대규모 데이터 병렬성 제약 |

#### 한줄 요약

- NVIDIA GPU 극대화는 **CUDA**, 이종 플랫폼 이식성은 **SYCL**, CPU 병렬화는 **OpenMP**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Pinned Host Memory(고정 메모리)**: OS의 페이징을 비활성화하여 GPU DMA 복사 속도를 극대화하는 `cudaHostAlloc()` 기반 메모리.
- **Arithmetic Intensity(연산 집약도)**: 메모리 1바이트 전송당 수행하는 부동소수점 연산 수(FLOPs/Byte).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 급브레이크인 무식한 **전역 동기화** 함수 남발로 인한 스트림 실행 마비 및 심각한 전송 병목 | **이벤트** 기반 비동기 래치를 짜 맞춰 스트림 간의 섬세한 의존성 최적화 구조망 구축 | 복사 연산과 커널 연산의 야바위 동시 겹침 처리로 칩 내 지연 은닉의 극대화 달성 |
| 호스트와 장치 간 좁아터진 PCIe 버스를 넘나드는 구역질 나는 메모리 복사 지연 오버헤드 | **고정 호스트 메모리** 할당 및 여러 개의 **스트림 중첩** 기법을 통한 복사 통신 우회 가림 적용 | 칩 내부 직접 메모리 접근 전송 속도를 100% 한계까지 끌어올리고 대기시간 완벽 은닉 |
| 수만 개의 스레드가 비동기로 런칭되다 폭파(에러) 시, 어디서 터졌는지 감도 못 잡는 디버깅 지옥 | 커널 실행 후 에러 체크 래퍼 함수 떡칠 및 디버깅용 강제 이벤트 동기화 지점 촘촘히 삽입 | 칩 안에서 뻗어버린 정확한 오류 발생 커널 위치 도출 및 디버깅 용이성 생명줄 확보 |
| 느려터진 전역 메모리를 들락거리다 대역폭이 포화되어 수천 개 코어가 놀고먹는 성능 추락 참사 | 온칩 캐시인 공유 메모리를 극한으로 쥐어짜는 타일링 적용 및 텐서 **연산 집약도** 강제 조작 제어 | 바깥 전역 메모리로 나가는 통신 오버헤드 원천 단축 및 코어 **점유율** 100% 폭주 향상 |

#### 한줄 요약

- **비동기 이벤트 동기화·Pinned Memory H2D 전송·공유 메모리 타일링·Warp 점유율 관리**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **현대 AI 컴파일러 연동**: Triton 및 TVM, PyTorch 2.0 `torch.compile`이 저수준 CUDA C++ 코드를 자동 생성하여 수작업 최적화 부담을 획기적으로 경감.

</details>

- 엔터프라이즈 AI 학습 및 LLM 인프라에서 **CUDA 기반 커널 최적화(FlashAttention, Triton) 및 멀티 GPU 분산 표준 채택**

#### 한줄 요약

- **이식성(SYCL)과 성능 극대화(CUDA)** 중 비즈니스 목표에 맞춘 플랫폼 선정
