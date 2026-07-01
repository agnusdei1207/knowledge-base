---
title: "AI 가속기 (AI Accelerator)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 235
---

# 📖 【암기용】 개념 완전 이해

> 목적: AI 가속기를 CPU만으로 처리하기 어려운 행렬곱, 컨볼루션, attention 연산을 전용 하드웨어로 처리하는 장치로 이해하게 만든다.

## 한눈에
- **개요**: AI 모델의 텐서 연산을 CPU보다 높은 병렬 처리량과 낮은 전력당 비용으로 수행하도록 설계된 하드웨어
- **왜 필요한가**: 딥러닝은 MAC 연산과 메모리 이동이 많아 CPU의 범용 제어 구조만으로 대규모 처리량을 확보하기 어렵다.
- **핵심 직관**: 범용 승용차 대신 컨테이너 운송에 맞춘 대형 트럭을 쓰는 것과 같다.

## 깊이 이해
- **배경·문제의식**: AI 추론과 학습은 행렬곱, 컨볼루션, attention처럼 동일 연산을 대량 데이터에 반복 적용한다.
- **작동 원리**: GPU는 SIMT와 Tensor Core, TPU는 systolic array, NPU는 온디바이스 신경망 연산 유닛, FPGA는 재구성 dataflow로 AI 연산을 가속한다.
- **비유**: 다양한 공구가 있는 작업장 중 AI 가속기는 특정 반복 작업을 자동화한 전용 라인이다.
- **구체 예시**: 데이터센터는 GPU/TPU로 LLM 학습·추론을 처리하고 스마트폰은 NPU로 사진 보정, 음성 인식, on-device LLM 추론을 처리한다.
- **흔한 오해·주의점**: AI 가속기는 CPU를 제거하지 않는다. CPU는 제어, I/O, 전처리를 맡고 가속기는 텐서 연산을 맡는다.

## 연결 개념
- GPU — 범용 병렬 AI 가속기의 대표 장치
- TPU — 행렬곱 특화 ASIC
- FPGA AI Acceleration — 재구성 가능 AI 가속 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: AI 가속기는 GPU, TPU, NPU, FPGA의 구조 차이와 워크로드별 선택 기준을 비교해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI Accelerator는 행렬곱·컨볼루션·attention 같은 텐서 연산을 전용 병렬 하드웨어로 처리하는 장치임.
> 2. **가치**: CPU의 범용 제어 오버헤드를 줄이고 TOPS/W, tokens/sec, latency 기준의 AI 처리량을 확보함.
> 3. **판단 포인트**: 학습은 GPU/TPU, 엣지 추론은 NPU, 알고리즘 변화 대응은 FPGA처럼 워크로드에 따라 선택해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 하드웨어 분류 이해 확인 | GPU, TPU, NPU, FPGA, ASIC | 가속기를 GPU 하나로 한정 |
| 워크로드 선택 판단 확인 | 학습·추론·엣지·재구성성 | 모든 가속기가 같은 용도라고 서술 |
| 성능 지표 이해 확인 | TOPS/W, memory bandwidth, latency | FLOPS만으로 판단 |

> 요약: 이 문제는 가속기 종류 나열보다 연산 구조와 적용 조건을 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: AI 텐서 연산 전용 병렬 하드웨어
- 배경: CPU는 범용 제어와 분기 처리에 맞춰져 대규모 행렬 연산 처리량이 제한됨.
- 필요성: TOPS/W, tokens/sec, p95 latency, memory bandwidth 기준으로 AI workload에 맞는 가속기를 선택해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
CPU Host -> AI Accelerator -> Tensor Core / Systolic Array / NPU MAC / FPGA Dataflow -> HBM/SRAM -> Runtime/Compiler
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Compute Array | MAC, matrix multiply, convolution 수행 | Tensor Core, systolic array |
| On-chip Memory | 가중치·활성값 재사용 | SRAM, cache, buffer |
| High-bandwidth Memory | 대규모 모델 파라미터 저장 | HBM, GDDR, LPDDR |
| Runtime/Compiler | 모델 그래프를 장치 명령으로 변환 | CUDA, XLA, TVM, vendor SDK |

> 요약: AI 가속기는 연산 배열, 메모리 계층, 컴파일러·런타임이 함께 동작해야 모델 그래프를 실행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
모델 그래프 입력 -> compiler 최적화 -> tensor 연산 배치 -> 가속기 실행 -> 메모리 재사용 -> 결과 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 모델 그래프와 정밀도 정책 설정 | FP16, BF16, INT8 |
| 2 | compiler가 연산 fusion과 layout 변환 수행 | graph compile 성공 |
| 3 | compute array가 tensor 연산 실행 | accelerator utilization |
| 4 | 결과를 CPU 또는 다음 연산으로 전달 | p95 latency |

> 요약: AI 가속기는 컴파일러가 모델 그래프를 장치 친화적으로 바꾼 뒤 텐서 연산을 병렬 실행한다.

---

## Ⅳ. 특징

| 구분 | CPU 중심 처리 | AI Accelerator | 수치 기준 |
|:---|:---|:---|:---|
| 구조 | 범용 코어와 캐시 | MAC 배열·텐서 코어 | TOPS/W |
| 워크로드 | 분기·제어·I/O | 행렬곱·컨볼루션·attention | utilization |
| 적용 | 전처리·오케스트레이션 | 학습·추론 핵심 연산 | p95 latency |

> 요약: CPU는 제어와 I/O, AI 가속기는 대량 텐서 연산에 역할을 분담한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | GPU는 범용 병렬 | TPU/NPU는 특화 회로 | 범용성 vs 전력당 처리량 |
| 비용/성능 | FPGA는 재구성 가능 | ASIC은 대량 생산 적합 | 물량과 알고리즘 변경 주기 |
| 운영/위험 | 벤더별 SDK 상이 | 런타임 종속 발생 | 생태계와 이식성 |

> 요약: AI 가속기 선택은 연산 패턴, 전력 예산, 생산 물량, 런타임 생태계를 함께 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메모리 병목 | 연산 대비 데이터 이동 과다 | operator fusion, tiling, cache reuse | memory bandwidth utilization |
| 벤더 종속 | CUDA, XLA, SDK 차이 | ONNX, TVM, abstraction layer | porting time |
| 정밀도 손실 | INT8/FP8 양자화 | calibration, accuracy regression | accuracy drop 1% 이하 |

> 요약: AI 가속기 리스크는 메모리 병목, 벤더 종속, 정밀도 손실이며 컴파일러와 평가 체계로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | tokens/sec 또는 inference/s 목표 | benchmark |
| 전력 | TOPS/W 목표 충족 | 전력 계측 |
| 품질 | 양자화 후 accuracy drop 1% 이하 | validation set |

> 요약: 도입 성과는 처리량, 전력당 연산량, 양자화 후 품질 유지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 대규모 학습은 GPU/TPU, 모바일 추론은 NPU, 알고리즘 변화가 잦은 초기 제품은 FPGA를 후보로 비교함.
2. 모델 그래프를 ONNX 또는 MLIR 계열 중간표현으로 관리해 장치 이식 비용을 낮춤.
3. FP16/BF16/INT8/FP8 정밀도별 latency, throughput, accuracy drop을 동일 데이터셋으로 측정함.

**결론 (2줄):**
- 기술사 판단: AI 가속기는 범용성, 전력 예산, 메모리 대역폭, 생태계 종속을 기준으로 워크로드별 선택함.
- 향후 방향: AI 가속기는 HBM, chiplet, in-network computing, on-device NPU와 결합해 데이터센터와 엣지 양쪽으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "AI 가속기를 설명하시오" | 모델 그래프 실행 흐름 | CPU와 역할 차이 |
| 요구사항 명시형 | "AI 가속기 선택 기준을 제시하시오" | 정밀도·컴파일러·메모리 흐름 | GPU/TPU/NPU/FPGA 비교 |

> 요약: 설명형은 구조와 동작을, 선택형은 워크로드별 가속기 판단 기준을 중심으로 작성한다.
