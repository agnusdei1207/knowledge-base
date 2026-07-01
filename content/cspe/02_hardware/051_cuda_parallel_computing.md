---
title: "CUDA 병렬 컴퓨팅 (CUDA Parallel Computing)"
date: "2026-07-01"
tags:
  - "cspe-hardware"
weight: 51
---

# 📖 【암기용】 개념 완전 이해

> 목적: CUDA를 처음 봐도 GPU 코어 수천 개를 어떻게 제어하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: NVIDIA GPU의 SIMT 코어 수천 개를 grid·block·thread 계층으로 제어하는 병렬 프로그래밍 플랫폼·API
- **왜 필요한가**: GPU는 코어가 많아도 이를 직접 스케줄링하는 저수준 인터페이스가 없으면 활용할 수 없다. CUDA는 C/C++ 확장 문법, 컴파일러(nvcc), 런타임, 드라이버를 묶어 커널 실행과 메모리 관리를 표준화한다.
- **핵심 직관**: 공장에 수천 명의 작업자(스레드)를 줄 세워 놓고 같은 명령을 동시에 내리는 지휘 체계다.

## 깊이 이해
- **배경·문제의식**: 2006년 CUDA 출시 이전에는 GPU를 범용 연산(GPGPU, General-Purpose computing on GPU)에 쓰려면 그래픽 셰이더 API(OpenGL)를 억지로 우회해야 했다.
- **작동 원리**: 커널 함수를 grid(다수 block) -> block(다수 thread) 계층으로 실행하고, 하드웨어는 32개 스레드를 하나의 warp로 묶어 SIMT(Single Instruction Multiple Thread) 방식으로 동시 실행한다.
- **비유**: warp는 32명이 한 조로 묶여 같은 명령을 동시에 수행하는 팀과 같다.
- **구체 예시**: 벡터 덧셈 커널 `__global__ void add(float* a, float* b, float* c)`를 `<<<grid, block>>>`로 실행하면, 각 스레드가 배열 원소 하나씩 병렬로 더한다.
- **흔한 오해·주의점**: CUDA는 "GPU"와 동의어가 아니다. CUDA는 NVIDIA GPU 전용 프로그래밍 인터페이스이며, AMD·Intel GPU에서는 실행되지 않고 대신 OpenCL, ROCm, SYCL 같은 대안을 사용한다.

## 연결 개념
- cuDNN·cuBLAS·TensorRT — CUDA 상위의 딥러닝·선형대수 가속 라이브러리
- Tensor Core — CUDA 코어와 별도로 행렬곱을 가속하는 전용 유닛
- OpenCL·ROCm·SYCL — CUDA의 벤더 중립 대안

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CUDA 답안은 grid/block/thread 계층, warp 기반 SIMT 실행, 메모리 계층, 벤더 종속 이슈를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CUDA (Compute Unified Device Architecture)는 NVIDIA GPU의 SIMT 코어를 grid·block·thread 계층으로 제어하는 병렬 프로그래밍 플랫폼이다.
> 2. **가치**: warp 단위(32 thread) SIMT 실행과 global·shared·register로 이어지는 메모리 계층으로 대규모 데이터 병렬 연산의 처리량을 높인다.
> 3. **판단 포인트**: NVIDIA 전용 생태계(cuDNN·cuBLAS·TensorRT)의 성능 이점과 벤더 종속 리스크, 이식성이 필요한 OpenCL·SYCL 사이에서 선택 기준을 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GPU 병렬 프로그래밍 모델 이해 확인 | grid/block/thread 계층, warp, SIMT 실행 방식 | block·thread를 OS 프로세스·스레드 개념과 혼동 |
| 메모리 계층 활용 역량 확인 | global/shared/register memory, memory coalescing | 메모리 접근 패턴 언급 없이 병렬성만 서술 |
| 생태계·이식성 판단 확인 | cuDNN/cuBLAS/TensorRT vs OpenCL/ROCm/SYCL | 벤더 종속(vendor lock-in) 문제 누락 |

> 요약: 이 문제는 CUDA 문법 나열이 아니라 SIMT 실행·메모리 계층·벤더 종속 판단을 함께 요구한다.

---

## Ⅰ. 개요 및 필요성

- 정의: NVIDIA GPU 병렬 연산을 위한 프로그래밍 모델·API·런타임 플랫폼
- 배경: 2006년 이전 GPU 범용 연산(GPGPU)은 그래픽 셰이더를 우회 활용해야 접근 가능했음
- 필요성: 수천 개 SIMT 코어를 활용하려면 커널·스레드 계층·메모리 관리를 표준화한 프로그래밍 인터페이스가 필요

---

## Ⅱ. 구조 및 구성요소

```text
Host(CPU) -> Kernel Launch<<<grid,block>>>
  -> Grid (다수 Block)
    -> Block (다수 Thread, Shared Memory 공유)
      -> Warp (32 Thread, SIMT 동시 실행)
  -> Device Memory (Global/Constant/Texture) 접근
  -> 결과를 Host로 복사
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Grid/Block/Thread | 커널 실행 단위 계층 | 논리적 인덱스(threadIdx, blockIdx)로 데이터 매핑 |
| Warp | 32 thread 묶음 SIMT 실행 단위 | warp 내 분기 발산(divergence) 시 순차 처리로 성능 저하 |
| Shared Memory | Block 내 스레드 공유 저지연 메모리 | on-chip, register 다음으로 빠름 |
| Global Memory | Device 전체에서 접근 가능한 메모리 | 대역폭은 크지만 지연 큼, coalescing 필요 |
| Tensor Core | 행렬곱-누산 전용 유닛 | CUDA 코어와 별도로 FP16/INT8 행렬곱 가속 |

> 요약: CUDA는 grid/block/thread 계층과 shared/global 메모리 계층을 조합해 SIMT 병렬 실행을 구성한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Host Code 작성 -> cudaMalloc/cudaMemcpy(H2D)
  -> Kernel Launch<<<grid,block>>> -> Warp Scheduler 할당
  -> SM(Streaming Multiprocessor) 내 SIMT 실행 -> Memory Coalescing 접근
  -> cudaMemcpy(D2H) -> Host 결과 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Host에서 Device 메모리 할당·데이터 전송 | H2D 전송 대역폭, PCIe/NVLink 사용률 |
| 2 | 커널 launch로 grid/block 구성 | occupancy(SM당 활성 warp 비율) |
| 3 | warp scheduler가 SM에 warp 배정 후 SIMT 실행 | warp divergence 비율, 명령어 처리량 |
| 4 | 결과를 Device에서 Host로 복사 | D2H 전송 시간, 전체 kernel latency |

> 요약: CUDA 실행은 메모리 전송, warp 스케줄링, SIMT 연산, 결과 회수 순으로 진행되며 각 단계 병목을 분리 측정해야 한다.

---

## Ⅳ. 특징

| 구분 | CUDA | OpenCL | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 벤더 범위 | NVIDIA GPU 전용 | Khronos 개방 표준, 다중 벤더 지원 | CUDA는 NVIDIA만, OpenCL은 AMD/Intel/NVIDIA 공통 |
| 생태계 | cuDNN, cuBLAS, TensorRT 성숙 | 벤더별 최적화 라이브러리 상대적 제한 | 딥러닝 프레임워크 기본 backend는 대부분 CUDA |
| 프로그래밍 모델 | grid/block/thread, warp SIMT | NDRange, work-group/work-item | 개념은 유사하나 API·툴체인 상이 |
| 이식성 | NVIDIA 하드웨어에 종속 | 여러 GPU/CPU/FPGA에서 실행 가능 | 벤더 lock-in vs 이식성 트레이드오프 |

> 요약: CUDA는 NVIDIA 생태계 성능·성숙도가 강점이고, OpenCL은 벤더 중립 이식성이 강점이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안(OpenCL·ROCm) | CUDA | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 벤더 중립 NDRange 모델 | grid/block/thread + Tensor Core | NVIDIA GPU 전용 인프라면 CUDA 우선 |
| 비용/성능 | 벤더별 최적화 편차 존재 | cuDNN/TensorRT로 검증된 고성능 | 학습·추론 처리량 목표와 라이브러리 지원 범위 |
| 운영/위험 | 멀티벤더 유지보수 부담 | 단일 벤더 종속, 공급망 리스크 | 장기 조달 전략과 이식성 요구 수준 |

> 요약: 성능·생태계는 CUDA, 벤더 중립·이식성은 OpenCL/ROCm이 유리하므로 인프라 전략에 맞춰 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Warp Divergence | block 내 조건 분기로 warp가 순차 실행 | 분기 최소화, 데이터 정렬 재구성 | active warp 비율, divergent branch count |
| 메모리 병목 | non-coalesced global memory 접근 | 메모리 정렬·타일링, shared memory 활용 | memory throughput, cache hit rate |
| 벤더 종속 | CUDA 전용 코드로 이식성 상실 | 추상화 계층(예: Kokkos, SYCL) 검토 | 코드 이식 비용, 대체 하드웨어 가용성 |

> 요약: CUDA 운영은 warp divergence, 메모리 coalescing, 벤더 종속 리스크를 지표로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | SM occupancy 70% 이상 목표 | Nsight Compute, 프로파일러 |
| 지연 | H2D/D2H 전송 시간 대비 커널 실행 시간 비율 | CUDA event timer |
| 정확도 | FP16/INT8 연산 시 정밀도 손실률 | 검증 데이터셋 오차 비교 |

> 요약: 도입 성과는 occupancy, 전송 대비 연산 비율, 정밀도 손실률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 데이터 병렬 연산이 큰 학습·추론 워크로드는 CUDA 기반 cuDNN/TensorRT를 적용하고 occupancy와 warp divergence를 프로파일링함
2. 멀티벤더 하드웨어 대응이 필요한 시스템은 OpenCL/SYCL 계층을 병행 검토해 벤더 종속 리스크를 완화함
3. 메모리 병목 구간은 shared memory 타일링과 coalesced access 패턴으로 global memory 대역폭 사용률을 개선함

**결론 (2줄):**
- 기술사 판단: NVIDIA 생태계 종속을 감수할 수 있는 고성능 학습·추론 환경은 CUDA, 벤더 중립·이식성이 중요한 환경은 OpenCL/SYCL을 선택함
- 향후 방향: Tensor Core 활용 극대화와 멀티벤더 추상화 계층(SYCL, Kokkos) 확대로 벤더 종속 리스크를 낮추는 방향으로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CUDA를 설명하시오" | grid/block/thread, warp SIMT 실행 흐름 | 메모리 계층, Tensor Core 구조 |
| 비교형 | "CUDA와 OpenCL을 비교하시오" | 각 모델의 실행 계층 대응 관계 | 벤더 종속·이식성 선택 기준 |

> 요약: 설명형은 SIMT 실행 원리를, 비교형은 벤더 종속과 이식성 선택 기준을 중심으로 답안 축을 바꾼다.
