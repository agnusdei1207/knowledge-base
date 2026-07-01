---
title: "양자화 (Quantization)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 76
---

# 📖 【암기용】 개념 완전 이해

> 목적: 양자화를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 모델 가중치·활성값의 숫자 정밀도를 FP32/FP16에서 INT8/INT4 등 낮은 비트로 줄이는 압축 기법
- **왜 필요한가**: 대형 모델은 메모리와 대역폭이 병목이므로 정밀도를 줄여 추론 비용과 지연을 낮춤.
- **핵심 직관**: 아주 정밀한 자 대신 눈금이 조금 거친 자를 써서, 계산은 작게 만들되 결과 오차는 허용 범위 안에 두는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM은 수십억 파라미터를 매 토큰마다 읽어야 하므로 GPU 메모리 대역폭이 지연을 좌우함. FP16 7B 모델은 약 14GB가 필요해 엣지·단일 GPU 배포가 어렵다.
- **작동 원리**: 실수값을 scale과 zero-point를 사용해 낮은 비트 정수로 매핑함. PTQ는 학습 후 보정만 수행하고, QAT는 학습 중 양자화 오차를 반영함.
- **비유**: 3.141592를 항상 쓰지 않고 3.14로 계산해도 실무 오차가 허용되는 상황과 같음.
- **구체 예시**: 7B FP16 모델은 약 14GB, INT8은 약 7GB, INT4는 약 3.5~5GB 수준으로 줄어듦.
- **흔한 오해·주의점**: 비트를 낮추면 항상 빠른 것은 아님. 하드웨어가 INT4/INT8 kernel을 지원해야 실제 지연이 줄어듦.

## 연결 개념
- INT8 Quantization — 범용 추론 양자화
- GPTQ/AWQ — LLM weight-only 4-bit 양자화
- Model Compression — 양자화의 상위 개념

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Quantization은 숫자 정밀도를 낮춰 모델 메모리·대역폭·추론 비용을 줄이는 압축 기법임.
> 2. **가치**: LLM·엣지 모델을 단일 GPU·온디바이스 환경에 배포 가능하게 함.
> 3. **판단 포인트**: bit width, PTQ/QAT, weight/activation 대상, 정확도 회귀, kernel 지원을 함께 검토해야 함.

## Ⅰ. 개요 및 필요성

- 개요: 모델 수치 정밀도 축소 기법
- 배경: FP16/FP32 모델은 weight·activation 저장과 메모리 대역폭 사용량이 커서 추론 지연과 GPU 비용을 증가시킴.
- 필요성: INT8/INT4, PTQ/QAT, calibration set, quantized kernel로 VRAM·latency·정확도 회귀를 함께 검증해야 함.

## Ⅱ. 구조 및 구성요소

```text
FP Model -> Calibration/Scale 계산 -> INT8/INT4 변환
      -> Quantized Kernel 실행 -> Accuracy/Latency Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Scale/Zero-point | 실수-정수 매핑 | per-tensor/per-channel |
| PTQ | 학습 후 양자화 | calibration set 필요 |
| QAT | 학습 중 양자화 반영 | 정확도 보존에 유리 |
| Quantized Kernel | 저비트 연산 실행 | HW 지원 필수 |

> 요약: 양자화는 수치 매핑, 보정 또는 재학습, 저비트 kernel 실행, 회귀 평가로 구성됨.

## Ⅲ. 동작원리 및 흐름도

```text
목표 bit 선택 -> calibration data 수집 -> scale 산출
    -> weight/activation 변환 -> 추론 실행 -> 정확도·지연 비교
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | INT8/INT4 등 bit width 결정 | 메모리 목표 |
| 2 | calibration으로 분포 측정 | 대표 데이터 512~10K건 |
| 3 | 양자화 변환·kernel 적용 | supported op 비율 |
| 4 | 회귀 평가 | 정확도 하락 1~3%p 이내 |

> 요약: 양자화는 데이터 분포를 기준으로 scale을 정하고, 정확도·지연·메모리 실측으로 적용 여부를 판단함.

## Ⅳ. 특징

| 구분 | FP16 모델 | Quantized 모델 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 메모리 | 2 byte/param | 1 byte(INT8), 0.5 byte(INT4) | 7B: 14GB->3.5~7GB |
| 지연 | 대역폭 부담 | kernel 지원 시 감소 | 실제 GPU 측정 |
| 정확도 | 기준 성능 | 오차 발생 가능 | 회귀 1~3%p 기준 |
| 적용 | 단순 | calibration·호환성 필요 | PTQ/QAT 선택 |

> 요약: 양자화는 메모리와 대역폭을 줄이지만, 정확도와 하드웨어 kernel 검증이 성공 조건임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 클라우드 LLM 서빙은 weight-only INT4/INT8로 GPU 메모리 50~75% 절감 후 MMLU·사내셋 회귀 검증
2. 온디바이스 비전 모델은 INT8 QAT를 적용하고 p95 100ms, 정확도 하락 2%p 이내 기준으로 배포
3. 양자화 전후 TTFT, TPOT, tokens/s, peak memory를 같은 트래픽으로 측정해 TCO를 산정

**결론 (2줄):**
- 기술사 판단: 메모리 병목은 INT4/INT8 weight quantization, 정확도 민감 업무는 QAT 또는 FP16 유지 선택
- 향후 방향: FP8/INT4 kernel과 activation-aware 기법이 LLM 서빙 표준 최적화로 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | scale 산출·변환·평가 흐름 | FP16 대비 메모리·정확도 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | PTQ/QAT 선택·검증 절차 | bit width·kernel·회귀 기준 |

> 요약: 설명형은 수치 정밀도 변환 원리, 최적화형은 병목별 bit 선택과 회귀 검증 중심으로 목차를 전환함.
