---
title: "모델 압축 (Model Compression)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 74
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 압축을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: AI 모델의 크기·연산량·메모리 사용량을 줄이면서 정확도 하락을 제한하는 최적화 기법
- **왜 필요한가**: 대형 모델은 GPU 메모리·추론 지연·전력 비용이 커서 엣지·온디바이스·대규모 API에 그대로 쓰기 어렵다.
- **핵심 직관**: 시험에 꼭 필요한 요약본을 만들되, 정답률이 떨어지지 않도록 핵심 지식을 보존하는 작업임.

## 깊이 이해
- **배경·문제의식**: LLM·비전 모델은 파라미터 증가로 정확도를 얻지만 배포 비용이 증가함. 모델 압축은 pruning, quantization, distillation, low-rank factorization으로 배포 제약을 완화함.
- **작동 원리**: 중요도가 낮은 weight/channel을 제거하고, FP32/FP16을 INT8/INT4로 낮추며, teacher model의 출력을 student model에 학습시킴. 압축 후 반드시 정확도 회귀를 측정함.
- **비유**: 두꺼운 교재에서 시험에 안 나오는 부분을 줄이고, 핵심 공식은 작은 암기 카드로 옮기는 것과 같음.
- **구체 예시**: 7B 모델은 FP16 약 14GB지만 INT4 적용 시 약 3.5~5GB로 줄어 단일 소비자 GPU나 고성능 PC 배포가 가능함.
- **흔한 오해·주의점**: 압축률만 높이면 품질이 유지되는 것이 아님. 도메인별 정확도·환각·지연을 함께 평가해야 함.

## 연결 개념
- Quantization — 정밀도 축소 압축
- Pruning — 불필요 파라미터 제거
- Knowledge Distillation — teacher-student 압축

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Model Compression은 모델 크기·FLOPs·메모리를 줄여 배포 비용을 낮추는 최적화 기법군임.
> 2. **가치**: 온디바이스·엣지·고동시성 API에서 지연·전력·GPU 비용을 절감함.
> 3. **판단 포인트**: 압축률, 정확도 하락, 하드웨어 지원, 재학습 필요성, 회귀 평가를 함께 관리해야 함.

## Ⅰ. 개요 및 필요성

- 개요: AI 모델 크기·연산 축소 기법
- 배경: 대형 모델은 메모리, FLOPs, 전력 사용량이 커서 온디바이스·엣지·클라우드 배포 비용을 증가시킴.
- 필요성: pruning, quantization, distillation, low-rank 기법을 적용하고 정확도 회귀·latency·VRAM 사용량을 함께 검증해야 함.

## Ⅱ. 구조 및 구성요소

```text
Trained Model -> Importance Analysis
   -> Pruning / Quantization / Distillation / Low-rank
   -> Compressed Model -> Accuracy & Latency Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Pruning | weight/channel 제거 | structured 권장 |
| Quantization | FP16->INT8/INT4 변환 | 하드웨어 지원 필요 |
| Distillation | teacher 지식 이전 | small student 학습 |
| Evaluation | 품질·지연 회귀 검증 | task별 기준 필요 |

> 요약: 모델 압축은 제거·정밀도 축소·지식 이전을 조합하고, 압축 후 회귀 평가로 배포 가능성을 판단함.

## Ⅲ. 동작원리 및 흐름도

```text
목표 설정 -> 압축 기법 선택 -> 압축 수행
    -> 재학습/보정 -> 정확도·지연·메모리 평가 -> 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 목표 지표 정의 | 모델 크기, p95 latency |
| 2 | pruning/quantization/distillation 선택 | 압축률, 하드웨어 |
| 3 | 압축·재학습·캘리브레이션 | calibration set |
| 4 | 회귀 평가·배포 | 정확도 하락 1~3%p 이내 |

> 요약: 압축은 목표 지표를 먼저 정하고, 기법 적용 후 정확도·지연·메모리 회귀를 통과해야 배포함.

## Ⅳ. 특징

| 구분 | 원본 모델 | 압축 모델 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 크기 | FP16/FP32 | INT8/INT4·pruned | 7B FP16 14GB->INT4 3.5~5GB |
| 지연 | 연산량 큼 | FLOPs·메모리 감소 | p95 latency 비교 |
| 정확도 | 기준 성능 | 하락 가능 | 1~3%p 허용 기준 |
| 운영 | 단순 | 기법별 검증 필요 | device별 benchmark |

> 요약: 모델 압축은 배포 비용을 줄이지만, 정확도 회귀와 하드웨어별 성능 검증이 성공 조건임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 온디바이스 모델은 INT8/INT4 양자화 후 p95 100ms, 정확도 하락 2%p 이내 기준 검증
2. 클라우드 LLM은 KV cache quantization과 weight-only quantization을 분리 적용해 GPU 메모리 30~50% 절감
3. 경량 모델은 teacher LLM 응답 10K~100K건으로 distillation 후 사내 평가셋 F1 0.85 이상 확보

**결론 (2줄):**
- 기술사 판단: 배포 병목이 메모리면 quantization, 연산량이면 pruning, 모델 축소면 distillation을 선택함.
- 향후 방향: 모델 압축은 SLM·온디바이스 AI·LLM Serving의 공통 전제 기술로 표준화됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 압축 기법 선택·평가 흐름 | 원본 대비 크기·정확도 |
| 요구사항 명시형 | 방안을 제시하시오, 설계하시오 | 병목별 기법 선택 절차 | 메모리·지연·정확도 기준 |

> 요약: 설명형은 압축 기법군, 방안형은 배포 병목별 선택 기준으로 목차를 전환함.
