---
title: "AWQ 활성화 인지 양자화 (Activation-aware Weight Quantization)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 80
---

# 📖 【암기용】 개념 완전 이해

> 목적: AWQ를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: activation 크기를 기준으로 중요한 weight channel을 보호하며 LLM weight를 저비트로 양자화하는 기법
- **왜 필요한가**: LLM에서는 일부 activation outlier가 출력 품질에 큰 영향을 주므로 단순 weight 기준 양자화만으로는 품질 보존이 어렵다.
- **핵심 직관**: 자주 크게 쓰이는 신경망 통로는 더 조심해서 압축하고, 영향이 작은 통로는 더 과감히 줄이는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM은 activation 분포가 균일하지 않고 outlier channel이 존재함. AWQ는 weight 자체보다 실제 입력 activation이 큰 channel을 중요한 경로로 보고 양자화 오차를 줄임.
- **작동 원리**: calibration data로 activation 통계를 수집하고, 중요한 channel weight를 scaling으로 보호한 뒤 INT4 등으로 weight-only quantization을 수행함.
- **비유**: 교통량이 많은 도로는 차선을 유지하고, 교통량이 낮은 도로부터 폭을 줄여 전체 도로망 효율을 높이는 것과 같음.
- **구체 예시**: AWQ는 LLM 4-bit weight-only 배포에서 GPTQ와 함께 vLLM·TensorRT-LLM 계열 서빙에 활용됨.
- **흔한 오해·주의점**: AWQ도 calibration data 품질에 의존함. 실제 서비스 입력과 다른 데이터로 통계를 잡으면 민감 channel 판단이 어긋남.

## 연결 개념
- 4-bit Quantization — AWQ 적용 대상
- GPTQ — Hessian 기반 대안
- Activation Outlier — AWQ가 보호하는 핵심 현상

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWQ는 activation 통계로 중요한 weight channel을 보호해 LLM 4-bit 양자화 품질을 보존하는 기법임.
> 2. **가치**: 재학습 없이 weight-only INT4 배포를 가능하게 하여 VRAM과 대역폭을 절감함.
> 3. **판단 포인트**: calibration 대표성, protected channel 비율, kernel 지원, GPTQ 대비 정확도·지연을 비교해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AWQ의 activation 기반 보호 원리와 GPTQ 대비 선택 기준 | activation outlier channel 보호, weight scaling, GPTQ와의 차이(Hessian vs activation 기준) | AWQ가 재학습 기법이라는 오해, calibration 불필요라는 서술 |

> 요약: 출제자는 AWQ의 activation 인지 보정 원리와 GPTQ 대비 적용 판단 역량을 확인하려 함.

---

## Ⅰ. 개요 및 필요성

- 정의: activation 통계 기반으로 중요 channel을 보호하는 LLM weight-only PTQ 기법
- 배경: LLM activation은 분포가 불균일하고 outlier channel이 출력 품질을 좌우함
- 필요성: 단순 weight 기준 양자화는 outlier channel 오차가 커서 LLM 4-bit 품질 보존이 어려움

## Ⅱ. 구조 및 구성요소

```text
FP16 LLM -> Calibration Activations -> Important Channel Detection
      -> Weight Scaling/Protection -> INT4 Weight Quantization -> Serving
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Activation Stats | 입력별 channel 중요도 측정 | calibration 필요 |
| Protected Channel | 민감 weight 보존 | outlier channel |
| Weight Scaling | 양자화 오차 완화 | 재학습 없음 |
| INT4 Kernel | weight-only 추론 실행 | vLLM/TRT 지원 확인 |

> 요약: AWQ는 activation 기반 민감 channel을 보호한 뒤 weight-only INT4로 변환해 LLM 품질 손실을 줄임.

## Ⅲ. 동작원리 및 흐름도

```text
대표 입력 수집 -> activation 통계 계산 -> 민감 channel 선택
    -> scaling 적용 -> 4-bit weight 변환 -> 정확도·지연 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | calibration prompt 수집 | 업무 입력 대표성 |
| 2 | activation outlier channel 탐지 | channel importance |
| 3 | weight scaling 후 INT4 변환 | protected ratio |
| 4 | GPTQ/FP16 대비 평가 | MMLU, perplexity, TPOT |

> 요약: AWQ는 실제 activation을 기준으로 중요한 경로를 보호하므로 LLM 4-bit 품질 보존에 초점을 둠.

## Ⅳ. 특징

| 구분 | GPTQ | AWQ | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 기준 | Hessian 오차 보정 | activation 중요도 | outlier channel 보호 |
| 학습 | PTQ | PTQ | 재학습 없음 |
| 장점 | 수학적 오차 보정 | LLM activation 특성 반영 | 4-bit 품질 보존 |
| 한계 | 설정·계산 비용 | calibration 대표성 의존 | kernel 호환성 |

> 요약: AWQ는 LLM activation outlier를 반영해 4-bit weight 양자화 품질을 보존하는 실무형 PTQ 기법임.

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | GPTQ | AWQ | 선택 기준 |
|:---|:---|:---|:---|
| 보정 기준 | Hessian 역행렬(수학적 오차) | activation 통계(입력 중요도) | outlier 심한 모델은 AWQ 유리 |
| 변환 비용 | layer별 Hessian 계산 | activation 통계 수집 | AWQ가 변환 시간 짧음 |
| kernel 지원 | vLLM/TRT-LLM 지원 | vLLM/TRT-LLM 지원 | 서빙 엔진 버전 확인 |

> 요약: activation outlier가 품질 병목이면 AWQ, 수학적 오차 보정이 우선이면 GPTQ를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중요 channel 오판 | calibration 입력 편향 | 실서비스 로그 1K~10K건 사용 | MMLU·perplexity 변화량 |
| kernel 비호환 | 서빙 엔진 AWQ 미지원 | vLLM/TRT-LLM 버전 확인 | tokens/s 실측 |
| 도메인 shift | 서비스 입력 분포 변경 | 주기적 재보정(분기 1회) | 정확도 모니터링 |

> 요약: calibration 대표성과 kernel 호환성을 사전 검증하지 않으면 AWQ 보호 효과가 불확실함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| VRAM 절감 | FP16 대비 70~75% 감소 | nvidia-smi peak memory |
| 품질 회귀 | MMLU 하락 2%p 이내, perplexity 증가 0.5 이내 | GPTQ·FP16 대비 벤치마크 |
| 추론 지연 | TPOT FP16 대비 동등 이하 | vLLM 부하 테스트 |

> 요약: VRAM·품질·지연 3개 축과 GPTQ 대비 결과를 비교해 AWQ 적용 여부를 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 서비스 로그 기반 calibration prompt 1K~10K건으로 AWQ 변환 후 MMLU·사내 QA 하락 2%p 이내 확인
2. AWQ 모델을 vLLM/TensorRT-LLM에서 실행해 TPOT, tokens/s, VRAM을 FP16·GPTQ와 비교
3. outlier가 큰 layer는 mixed precision으로 유지하고 나머지 layer는 INT4로 압축해 품질 회귀를 제한

**결론 (2줄):**
- 기술사 판단: LLM 4-bit 서빙에서 activation outlier가 품질 병목이면 AWQ, 빠른 PTQ 기준선은 GPTQ를 선택함.
- 향후 방향: AWQ는 weight-only INT4와 serving kernel 최적화가 결합된 LLM 배포 표준 옵션으로 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | activation 통계·channel 보호 흐름 | GPTQ 대비 특징 |
| 요구사항 명시형 | 비교하시오, 최적화하시오 | calibration·mixed precision 절차 | 정확도·VRAM·kernel 기준 |

> 요약: 설명형은 AWQ 원리, 비교형은 GPTQ 대비 선택 기준과 회귀 평가 중심으로 목차를 전환함.
