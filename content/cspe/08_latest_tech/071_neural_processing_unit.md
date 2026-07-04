---
title: "Neural Processing Unit (NPU)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 71
---

# 📖 【암기용】 개념 완전 이해

> 목적: NPU를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 신경망의 행렬곱·컨볼루션·활성화 연산을 저전력으로 처리하는 AI 전용 프로세서
- **왜 필요한가**: CPU는 범용 제어에, GPU는 대규모 병렬 그래픽·AI에 강하지만 모바일·PC 상시 AI에는 전력 효율 한계가 있음.
- **핵심 직관**: AI 계산만 반복 처리하도록 설계한 전용 계산 공장임.

## 깊이 이해
- **배경·문제의식**: 딥러닝 추론은 MAC(Matrix Multiply-Accumulate) 연산이 대부분임. 배터리 장치에서 GPU를 계속 쓰면 발열과 전력 소모가 커짐.
- **작동 원리**: NPU는 systolic array, MAC array, on-chip SRAM, DMA를 사용해 모델 가중치와 activation을 이동시키며 INT8/FP16/BF16 연산을 수행함. CPU는 제어, NPU는 반복 행렬 연산을 담당함.
- **비유**: 범용 공구함(CPU) 대신 나사 조립만 초고속으로 하는 자동화 라인(NPU)을 설치한 것임.
- **구체 예시**: AI PC 기준은 40 TOPS 이상 NPU가 주요 기준으로 사용되며, 스마트폰 NPU는 카메라·음성·번역을 저전력으로 처리함.
- **흔한 오해·주의점**: TOPS만 높으면 모든 모델이 빠른 것은 아님. 메모리 대역폭, 연산 정밀도, compiler/runtime 지원이 함께 맞아야 함.

## 연결 개념
- AI Accelerator — NPU·GPU·TPU를 포함하는 상위 개념
- On-Device AI — NPU 주요 적용 영역
- Quantization — NPU 효율을 높이는 모델 최적화

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NPU는 신경망 추론의 행렬·컨볼루션 연산을 전력 효율 중심으로 처리하는 AI 전용 가속기임.
> 2. **가치**: 모바일·PC·엣지에서 로컬 AI 기능을 낮은 지연과 낮은 전력으로 수행함.
> 3. **판단 포인트**: TOPS, precision, memory bandwidth, compiler/runtime, 모델 지원성을 함께 평가해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 전용 가속기의 구조·역할 이해 | MAC Array, TOPS/W, INT8/FP16, compiler op 지원 | TOPS 수치만 비교하고 메모리 대역폭·op 지원 누락 |

> 요약: NPU는 TOPS 수치보다 op 지원·메모리 대역폭·compiler 호환성까지 포함한 end-to-end 관점에서 평가해야 함.

---

## Ⅰ. 개요 및 필요성

- 정의: 신경망 추론의 행렬·컨볼루션 연산을 저전력으로 처리하는 AI 전용 프로세서
- 배경: CPU는 범용 제어, GPU는 대규모 병렬 연산에 강하지만 모바일·PC 상시 AI에는 전력 효율 한계가 있음
- 필요성: 온디바이스·엣지 AI 확산으로 배터리·발열 제약 안에서 행렬 연산을 수행할 전력 효율형 가속기가 필요함

## Ⅱ. 구조 및 구성요소

```text
CPU Control -> NPU Compiler -> MAC/Systolic Array
  -> On-chip SRAM <-> DRAM -> Output Tensor
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| MAC Array | 행렬곱·컨볼루션 연산 | INT8/FP16 등 |
| On-chip SRAM | activation·weight 재사용 | DRAM 접근 감소 |
| NPU Compiler | graph 최적화·operator mapping | 지원 op 범위 확인 |
| Runtime Driver | CPU-NPU 작업 제출 | OS·SDK 의존 |

> 요약: NPU는 MAC 배열과 SRAM을 중심으로 AI 연산을 가속하고 compiler/runtime이 모델 실행 가능성을 결정함.

## Ⅲ. 동작원리 및 흐름도

```text
모델 변환 -> graph 최적화 -> operator를 NPU에 매핑
    -> tensor load -> MAC 연산 -> 결과 반환 -> CPU 후처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 모델을 NPU 지원 포맷으로 변환 | ONNX/TFLite/Core ML |
| 2 | 양자화·graph fusion 수행 | INT8 정확도 회귀 |
| 3 | operator를 MAC/SRAM에 배치 | supported op 비율 |
| 4 | 추론 실행·전력 측정 | TOPS/W, p95 latency |

> 요약: NPU 성능은 하드웨어 TOPS보다 모델 변환·op 지원·메모리 재사용까지 포함한 end-to-end 지표로 판단함.

## Ⅳ. 특징

| 구분 | CPU/GPU | NPU | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 범용·그래픽 병렬 | AI 추론 전용 | TOPS/W 우위 |
| 정밀도 | FP32/FP16 다양 | INT8/FP16 중심 | 양자화 적합성 |
| 전력 | 고성능 시 소비 증가 | 저전력 상시 추론 | 모바일·PC 적합 |
| 한계 | 범용성 높음 | 지원 op·메모리 제약 | fallback 필요 |

> 요약: NPU는 전력 효율형 AI 추론에 강하지만, 모델과 런타임 지원성이 부족하면 CPU/GPU fallback이 필요함.

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | GPU | NPU | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | CUDA 코어 수천 개, 범용 병렬 | MAC Array, AI 전용 파이프라인 | 추론 전용이면 NPU |
| 비용/성능 | TDP 150~350W, FP32 고성능 | TDP 5~15W, INT8 TOPS/W 우위 | 배터리 제약 시 NPU |
| 운영/위험 | 드라이버·CUDA 생태계 성숙 | compiler op 지원·SDK 성숙도 편차 | op coverage 95% 이상 확보 |

> 요약: 상시 저전력 추론은 NPU, 학습·대규모 FP32 연산은 GPU를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 미지원 op fallback | compiler op coverage 부족 | 모델 변환 전 op 호환성 검증 | CPU fallback 비율 5% 이하 |
| 정확도 회귀 | INT8 양자화 손실 | calibration set 1K장 이상 검증 | accuracy delta 1%p 이내 |
| 벤더 종속 | NPU SDK·runtime 비호환 | ONNX Runtime 멀티백엔드 구성 | 2개 이상 런타임 호환 |

> 요약: NPU 도입 리스크는 op 호환·양자화 회귀·벤더 종속이며, 배포 전 검증으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/효율 | p95 latency 50ms, TOPS/W 10 이상 | NPU profiler, 벤치마크 |
| 품질/정확도 | INT8 정확도 하락 1%p 이내 | validation set 비교 |
| 운영/보안 | OTA 모델 업데이트, 모델 무결성 검증 | 서명 검증, 배포 로그 |

> 요약: NPU 도입 성공은 지연·정확도·op coverage를 단말별로 실측해 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. AI PC·모바일 도입 기준에 NPU 40 TOPS, INT8 지원, ONNX/Core ML/NNAPI 호환성을 포함
2. 모델 배포 전 supported op coverage 95% 이상, INT8 정확도 하락 1%p 이내, p95 latency를 검증
3. 미지원 operator는 CPU/GPU fallback 경로를 구성하고 전력·지연 회귀를 별도 측정

**결론 (2줄):**
- 기술사 판단: 상시 로컬 AI와 배터리 제약 업무는 NPU, 대형 학습·고정밀 연산은 GPU를 선택함.
- 향후 방향: NPU는 SLM·멀티모달 센서 처리와 결합해 클라이언트·엣지 AI의 기본 하드웨어가 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 모델 변환·NPU 실행 흐름 | CPU/GPU 대비 특징 |
| 요구사항 명시형 | 비교하시오, 선정 기준을 제시하시오 | op 지원·양자화 검증 절차 | TOPS/W·정확도·fallback 기준 |

> 요약: 설명형은 NPU 구조와 실행 원리, 선정형은 TOPS보다 end-to-end 지원성 기준으로 목차를 전환함.
