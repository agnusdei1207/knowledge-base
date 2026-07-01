---
title: "GPTQ 양자화 (GPTQ)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 79
---

# 📖 【암기용】 개념 완전 이해

> 목적: GPTQ를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: LLM 가중치를 3~4bit로 줄일 때 Hessian 근사로 양자화 오차를 보정하는 post-training quantization 기법
- **왜 필요한가**: 단순 4-bit 변환은 중요한 weight 오차가 누적되어 답변 품질이 떨어질 수 있음.
- **핵심 직관**: 숫자를 줄이되, 정답에 영향이 큰 숫자는 더 신중하게 반올림하는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM은 layer별 weight 분포와 민감도가 다르다. GPTQ는 calibration data로 layer 출력 민감도를 추정해 weight를 순차 양자화하고 오차를 보상함.
- **작동 원리**: layer 단위로 Hessian 역행렬 근사를 사용해 특정 weight를 양자화한 뒤 남은 weight에 오차 보정을 반영함. 학습 없이 PTQ로 적용 가능함.
- **비유**: 예산을 줄일 때 모든 항목을 동일 비율로 깎지 않고, 핵심 사업 피해가 작도록 항목별 영향도를 계산해 조정하는 것임.
- **구체 예시**: 7B~13B LLM을 4-bit GPTQ로 변환하면 단일 GPU 메모리에 올릴 수 있으나, group size와 act-order 설정에 따라 품질이 달라짐.
- **흔한 오해·주의점**: GPTQ는 모델을 새로 학습하는 기법이 아니라 PTQ임. calibration dataset과 kernel 호환성이 품질과 속도를 좌우함.

## 연결 개념
- 4-bit Quantization — GPTQ 적용 대상
- AWQ — activation-aware 대안
- PTQ — 학습 후 양자화 방식

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPTQ는 Hessian 근사 기반 오차 보정으로 LLM weight를 3~4bit로 압축하는 PTQ 기법임.
> 2. **가치**: 재학습 없이 VRAM을 줄여 대형 LLM을 단일 GPU·저비용 서빙 환경에 배포함.
> 3. **판단 포인트**: calibration data, group size, act-order, kernel 지원, perplexity 회귀를 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GPTQ의 Hessian 기반 보정 원리와 AWQ 대비 선택 기준 | Hessian 역행렬 근사, 순차 오차 보정, group size, act-order, PTQ 특성 | GPTQ를 QAT로 혼동, calibration 없이 적용 가능하다는 서술 |

> 요약: 출제자는 GPTQ의 오차 보정 원리와 실무 적용 시 calibration·kernel 판단 역량을 확인하려 함.

---

## Ⅰ. 개요 및 필요성

- 정의: Hessian 근사 기반 LLM weight-only PTQ 기법
- 배경: 단순 4-bit 변환은 중요 weight 오차가 누적되어 출력 품질이 저하됨
- 필요성: 재학습 없이 Hessian 오차 보정으로 4-bit 품질 하락을 완화하여 단일 GPU 배포를 가능하게 함

## Ⅱ. 구조 및 구성요소

```text
FP16 LLM -> Calibration Data -> Hessian Approximation
      -> Sequential Weight Quantization -> Error Compensation -> GPTQ Model
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Calibration Data | layer 민감도 추정 | 수백~수천 샘플 |
| Hessian Approx. | 양자화 오차 영향 추정 | 2차 정보 근사 |
| Group Quantization | weight 그룹별 scale 적용 | group size 32~128 |
| Error Compensation | 남은 weight에 오차 보정 | 순차 처리 |

> 요약: GPTQ는 calibration 기반 민감도 추정과 순차 오차 보정으로 저비트 weight 손실을 줄임.

## Ⅲ. 동작원리 및 흐름도

```text
Layer 입력 수집 -> Hessian 근사 -> weight 순차 양자화
    -> 오차 보정 -> 다음 layer 진행 -> 품질 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | calibration으로 layer activation 수집 | dataset 대표성 |
| 2 | Hessian 역행렬 근사 계산 | 메모리·시간 비용 |
| 3 | group별 4-bit weight 변환 | group size, act-order |
| 4 | perplexity·업무 정확도 평가 | 하락 1~3%p 이내 |

> 요약: GPTQ는 layer별 민감도를 반영해 weight를 순차 양자화하고 오차를 다음 weight에 보상함.

## Ⅳ. 특징

| 구분 | 단순 4-bit | GPTQ | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 보정 방식 | scale 중심 | Hessian 오차 보정 | 품질 보존 |
| 학습 필요 | 없음 | 없음(PTQ) | 빠른 변환 |
| 비용 | 낮음 | calibration·계산 비용 | layer별 처리 |
| 한계 | 품질 하락 | kernel·설정 의존 | act-order, group size |

> 요약: GPTQ는 재학습 없이 4-bit 품질을 보존하는 데 유리하지만, calibration과 kernel 설정 검증이 필요함.

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 단순 4-bit | GPTQ | 선택 기준 |
|:---|:---|:---|:---|
| 보정 방식 | scale 중심(보정 없음) | Hessian 역행렬 오차 보정 | 품질 민감도 |
| 변환 비용 | 수 분 | 수십 분~수 시간(layer별) | GPU 시간 예산 |
| 적용 범위 | 범용 | LLM weight-only 중심 | 모델 크기·유형 |

> 요약: 품질 민감 LLM은 GPTQ 보정을 적용하고, 빠른 변환이 우선이면 단순 4-bit를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| calibration 편향 | 대표성 부족 데이터 | 실서비스 로그 1K~10K건 사용 | perplexity 변화량 |
| kernel 비호환 | 서빙 엔진 미지원 | vLLM/TRT-LLM GPTQ kernel 확인 | tokens/s 실측 |
| act-order 설정 오류 | group size·act-order 미조정 | group 128/64별 perplexity 비교 | MMLU 하락폭 |

> 요약: calibration 대표성과 kernel 호환성을 사전 검증하지 않으면 GPTQ 효과가 불확실함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| VRAM 절감 | FP16 대비 70~75% 감소 | nvidia-smi peak memory |
| 품질 회귀 | perplexity 증가 0.5 이내, MMLU 하락 2%p 이내 | 벤치마크 비교 |
| 변환 시간 | 7B 기준 1시간 이내 | 변환 스크립트 로그 |

> 요약: VRAM·품질·변환 비용 3개 축을 측정해 GPTQ 적용 여부를 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 7B~13B LLM을 GPTQ 4-bit로 변환하고 group size 128/64별 perplexity·MMLU를 비교
2. 서비스 엔진(vLLM 등)의 GPTQ kernel 지원 여부를 확인하고 TPOT·tokens/s를 FP16과 비교
3. 도메인 QA 1K~10K건으로 회귀 평가 후 정확도 하락 2%p 초과 시 AWQ 또는 mixed precision으로 전환

**결론 (2줄):**
- 기술사 판단: 재학습 없이 빠른 LLM 경량화가 필요하면 GPTQ, activation outlier가 큰 모델은 AWQ를 병행 검토함.
- 향후 방향: GPTQ는 개인 GPU·사내망 SLM 배포의 빠른 PTQ 옵션으로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | Hessian·오차 보정 흐름 | 단순 4-bit 대비 특징 |
| 요구사항 명시형 | 적용 방안을 제시하시오 | group size·kernel 검증 절차 | GPTQ vs AWQ 선택 기준 |

> 요약: 설명형은 GPTQ 보정 원리, 적용형은 calibration·kernel·회귀 평가 중심으로 목차를 전환함.
