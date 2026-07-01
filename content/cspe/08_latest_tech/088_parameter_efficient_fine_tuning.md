---
title: "PEFT 파라미터 효율 튜닝 (Parameter-Efficient Fine-Tuning)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 88
---

# 📖 【암기용】 개념 완전 이해

> 목적: PEFT를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 전체 모델 가중치를 업데이트하지 않고 작은 추가 파라미터만 학습해 모델을 적응시키는 Fine-Tuning 방식
- **왜 필요한가**: LLM 전체 파인튜닝은 GPU 메모리·학습 시간·모델 복사 비용이 커서 도메인별 운영이 어렵다.
- **핵심 직관**: 원본 교재를 다시 쓰지 않고, 과목별 포스트잇과 보충 노트만 붙여 맞춤형 교재로 쓰는 방식임.

## 깊이 이해
- **배경·문제의식**: 7B~70B 모델 전체를 도메인마다 fine-tuning하면 모델 사본과 optimizer state가 폭증함. PEFT는 base model은 고정하고 adapter, LoRA, prefix 등 작은 모듈만 학습함.
- **작동 원리**: frozen base model 위에 task-specific trainable parameter를 삽입함. 추론 시 base model과 adapter를 함께 로드하거나 merge해 사용함.
- **비유**: 공통 본사 규정은 그대로 두고, 부서별 업무 지침만 얇은 부록으로 추가하는 것과 같음.
- **구체 예시**: LoRA는 W 행렬 업데이트를 저랭크 A·B 행렬로 분해해 학습 파라미터를 전체 대비 1% 미만으로 줄일 수 있음.
- **흔한 오해·주의점**: PEFT가 항상 full fine-tuning과 같은 정확도를 보장하지 않음. 데이터 규모와 도메인 차이가 크면 full FT나 continued pretraining이 필요할 수 있음.

## 연결 개념
- LoRA/QLoRA — 대표 PEFT 기법
- Adapter/Prefix/Prompt Tuning — PEFT 변형
- Fine-Tuning — PEFT의 상위 개념

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PEFT는 base model을 고정하고 소량의 task-specific 파라미터만 학습하는 비용 절감형 fine-tuning임.
> 2. **가치**: GPU 메모리, 학습 시간, 모델 저장 비용을 줄여 다도메인 LLM 운영을 가능하게 함.
> 3. **판단 포인트**: 기법 선택, trainable parameter 비율, adapter 관리, full FT 대비 정확도 회귀를 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| PEFT 원리와 Full FT 대비 판단 역량 | freeze/adapter 구조, trainable params 비율, adapter 관리 | Full FT와 혼동, 정확도 회귀 검증 누락, 추상적 "비용 절감" 표현 |

> 요약: 출제자는 base model 고정·소량 파라미터 학습 원리와 Full FT 대비 비용·정확도 판단을 확인함.

---

## Ⅰ. 개요 및 필요성

- 정의: base model을 고정하고 소량의 task-specific 파라미터만 학습하는 비용 절감형 fine-tuning
- 배경: LLM 전체를 도메인별로 학습·저장하면 GPU 메모리·복사 비용이 폭증함
- 필요성: adapter, LoRA, prefix 등 작은 모듈만 학습해 다도메인 운영 비용을 절감함

## Ⅱ. 구조 및 구성요소

```text
Frozen Base Model + Trainable PEFT Module
      → Task Training → Adapter/LoRA Weights → Inference
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Frozen Base | 사전학습 지식 보존 | gradient 미계산 |
| PEFT Module | 작은 학습 파라미터 | LoRA, Adapter |
| Task Data | 도메인 적응 데이터 | 1K~100K 샘플 |
| Adapter Registry | 업무별 모듈 관리 | 버전·권한 필요 |

> 요약: PEFT는 base model과 작은 task module을 분리해 학습·저장·배포 비용을 낮춤.

## Ⅲ. 동작원리 및 흐름도

```text
base model 고정 → PEFT 모듈 삽입 → task 데이터 학습
    → adapter 저장 → 추론 시 로드/merge → 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PEFT 기법과 삽입 위치 선택 | LoRA rank, adapter layer |
| 2 | base freeze 후 모듈 학습 | trainable params % |
| 3 | adapter 저장·버전 관리 | MB 단위 artifact |
| 4 | 정확도·지연 회귀 평가 | full FT 대비 gap |

> 요약: PEFT는 학습 대상을 작은 모듈로 제한하므로 adapter 관리와 정확도 회귀 검증이 운영 핵심임.

## Ⅳ. 특징

| 구분 | Full Fine-Tuning | PEFT | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 학습 파라미터 | 전체 모델 | 0.1~5% 수준 | GPU 메모리 절감 |
| 저장 | 모델 사본 필요 | adapter만 저장 | MB~GB 단위 |
| 정확도 | 상한 높음 | 도메인 차이 의존 | 회귀 평가 |
| 운영 | 단순 | adapter 라우팅 필요 | registry 관리 |

> 요약: PEFT는 비용과 저장 효율이 높지만, adapter 운영과 full FT 대비 정확도 차이를 관리해야 함.

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Full Fine-Tuning | PEFT | 선택 기준 |
|:---|:---|:---|:---|
| 학습 대상 | 전체 weight | 0.1~5% adapter/LoRA | GPU 메모리 ≤ 24GB 여부 |
| 저장 비용 | 모델 사본 | adapter만 저장(MB~GB) | 도메인 수 × 모델 크기 |
| 정확도 | 상한 높음 | 도메인 차이에 의존 | F1 하락 2%p 이내 기준 |

> 요약: GPU 메모리·저장 제약이 크면 PEFT, 정확도 최우선이면 Full FT를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정확도 회귀 | adapter 용량 부족 | rank·layer 탐색, full FT 전환 | F1 gap ≤ 2%p |
| Adapter 충돌 | 다도메인 adapter 버전 관리 미흡 | registry + base hash + rollback 정책 | 배포 일치율 |
| 서빙 지연 | 동적 adapter 로딩 오버헤드 | merge 또는 캐시 정책 적용 | p95 latency |

> 요약: 정확도 회귀·adapter 충돌·서빙 지연을 rank 탐색, registry 관리, merge 정책으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 도메인 정확도 | F1 ≥ 0.85, Full FT 대비 gap ≤ 2%p | holdout 평가셋 |
| Adapter 저장 | tenant별 adapter ≤ 500MB | artifact size 모니터링 |
| 서빙 성능 | p95 latency ≤ 200ms | 로드 테스트 |

> 요약: 도메인 F1, adapter 크기, 서빙 latency를 정량 기준으로 PEFT 도입 성공을 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 부서별 assistant는 공통 13B base model에 LoRA adapter를 분리해 저장하고 tenant별 로드 정책 적용
2. rank, learning rate, target module을 grid search하고 사내 평가셋 F1 하락 2%p 이내 기준으로 선택
3. adapter registry에 모델 버전, 데이터 버전, 승인자, rollback 정보를 기록해 감사 가능성 확보

**결론 (2줄):**
- 기술사 판단: 다도메인·저비용 적응은 PEFT, 근본 지식 변화와 큰 도메인 이동은 full FT/continued pretraining을 선택함.
- 향후 방향: PEFT는 QLoRA, multi-adapter routing, on-device SLM 튜닝과 결합해 표준 운영 방식이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | freeze·adapter 학습 흐름 | Full FT 대비 특징 |
| 요구사항 명시형 | 도입 방안을 제시하시오 | adapter registry·평가 절차 | 비용·정확도·운영 기준 |

> 요약: 설명형은 작은 모듈 학습 원리, 도입형은 adapter 운영과 평가 기준 중심으로 목차를 전환함.
