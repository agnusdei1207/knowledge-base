---
title: "INT8 Quantization"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 77
---

# 📖 【암기용】 개념 완전 이해

> 목적: INT8 Quantization을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: FP32/FP16 모델 값을 8-bit 정수 범위로 변환해 추론 메모리와 연산 비용을 줄이는 기법
- **왜 필요한가**: INT8은 정확도 하락과 하드웨어 지원 사이의 균형점으로, 엣지·서버 추론에서 널리 쓰임.
- **핵심 직관**: 고정밀 숫자를 256단계 눈금으로 표현해 계산량을 줄이되 업무 정확도는 유지하는 방식임.

## 깊이 이해
- **배경·문제의식**: FP16은 2바이트, INT8은 1바이트라 가중치 메모리를 절반으로 줄일 수 있음. 많은 NPU·GPU·CPU는 INT8 연산을 전용 경로로 지원함.
- **작동 원리**: calibration data로 activation 범위를 측정하고 scale·zero-point를 정함. 대칭/비대칭, per-tensor/per-channel 방식으로 양자화 오차를 조정함.
- **비유**: 온도를 소수점 둘째 자리 대신 정수로 기록해도 냉난방 제어에는 충분한 것과 같음.
- **구체 예시**: CNN·BERT 계열 모델은 INT8 PTQ/QAT 적용 시 정확도 하락 1~2%p 이내로 메모리 50% 절감 가능.
- **흔한 오해·주의점**: calibration data가 실제 입력 분포와 다르면 activation clipping으로 정확도가 급락할 수 있음.

## 연결 개념
- PTQ/QAT — INT8 적용 방식
- NPU/Edge TPU — INT8 연산 지원 하드웨어
- Model Compression — INT8의 상위 맥락

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: INT8 Quantization은 모델 수치를 8-bit 정수로 표현해 메모리와 대역폭을 절반 수준으로 줄이는 기법임.
> 2. **가치**: 정확도 회귀를 제한하면서 서버 GPU·NPU·엣지 장치에서 추론 비용을 낮춤.
> 3. **판단 포인트**: calibration 품질, per-channel scale, QAT 필요성, INT8 kernel 지원이 성패를 좌우함.

## Ⅰ. 개요 및 필요성

INT8 Quantization은 8-bit 정수 기반 모델 압축 기법임. FP16 대비 메모리 사용량을 줄이고 INT8 가속 하드웨어를 활용해 엣지·서버 추론 지연과 비용을 낮춤.

## Ⅱ. 구조 및 구성요소

```text
FP Model -> Calibration Dataset -> Scale/Zero-point
      -> INT8 Weights/Activations -> INT8 Kernel -> Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Calibration Set | activation 범위 측정 | 실제 입력 분포 반영 |
| Scale/Zero-point | 정수 매핑 파라미터 | symmetric/asymmetric |
| INT8 Kernel | 저비트 연산 실행 | CPU/NPU/GPU 지원 |
| QAT | 학습 중 오차 보정 | 정확도 민감 업무 |

> 요약: INT8은 대표 데이터로 수치 범위를 보정하고, 하드웨어 INT8 kernel에서 추론하는 구조임.

## Ⅲ. 동작원리 및 흐름도

```text
대표 데이터 수집 -> min/max 또는 KL calibration
    -> INT8 변환 -> 추론 실행 -> 정확도·latency 회귀 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | calibration data 선정 | 512~10K 샘플 |
| 2 | per-channel scale 계산 | clipping ratio |
| 3 | weight/activation INT8 변환 | supported op 비율 |
| 4 | 성능·정확도 비교 | 정확도 하락 1~2%p |

> 요약: INT8 적용은 calibration 품질과 op 지원율이 실제 정확도와 지연 개선 폭을 결정함.

## Ⅳ. 특징

| 구분 | FP16 | INT8 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 저장 크기 | 2 byte/param | 1 byte/param | 메모리 약 50% 절감 |
| 정확도 | 기준 | 소폭 하락 가능 | 1~2%p 관리 |
| 하드웨어 | 범용 GPU | NPU/CPU/GPU INT8 | kernel 지원 확인 |
| 난이도 | 낮음 | calibration 필요 | 분포 shift 주의 |

> 요약: INT8은 정확도와 효율의 균형점이지만, 대표 calibration data 없이는 회귀 위험이 큼.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 엣지 비전 모델은 INT8 QAT 적용 후 mAP 하락 2%p 이내, FPS 30 이상 기준으로 배포
2. 서버 추론은 TensorRT/OpenVINO/ONNX Runtime INT8 kernel을 확인하고 p95 latency를 FP16과 비교
3. 금융·의료 모델은 PTQ 후 회귀가 1%p 초과하면 QAT 또는 mixed precision으로 전환

**결론 (2줄):**
- 기술사 판단: 하드웨어 INT8 지원과 calibration data가 충분하면 INT8, 정확도 민감 영역은 QAT 또는 FP16을 선택함.
- 향후 방향: INT8은 엣지·서버 범용 최적화로 남고, LLM weight-only 영역은 INT4/FP8과 병행됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | calibration·scale 산출 흐름 | FP16 대비 특징 |
| 요구사항 명시형 | 적용 방안을 제시하시오 | PTQ/QAT·kernel 검증 절차 | 정확도·지연·하드웨어 기준 |

> 요약: 설명형은 INT8 변환 원리, 적용형은 calibration과 정확도 회귀 통제를 중심으로 목차를 전환함.
