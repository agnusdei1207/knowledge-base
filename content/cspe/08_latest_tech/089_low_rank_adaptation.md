---
title: "LoRA 저랭크 적응 (Low-Rank Adaptation)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 89
---

# 📖 【암기용】 개념 완전 이해

> 목적: LoRA를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 큰 weight 업데이트를 두 개의 작은 저랭크 행렬로 분해해 학습하는 PEFT 기법
- **왜 필요한가**: LLM 전체 가중치를 학습하면 GPU 메모리와 저장 비용이 커서 도메인별 튜닝이 어렵다.
- **핵심 직관**: 거대한 지도 전체를 다시 그리지 않고, 필요한 방향 보정선 몇 개만 얹어 목적지 안내를 바꾸는 방식임.

## 깊이 이해
- **배경·문제의식**: Fine-Tuning 시 weight 변화량 ΔW는 실제로 낮은 intrinsic rank를 가진다는 관찰에서 출발함. LoRA는 원본 W는 고정하고 ΔW를 A·B 저랭크 행렬로 근사함.
- **작동 원리**: 선형층에 `W x + (B A)x * α/r` 형태의 LoRA branch를 추가하고 A·B만 학습함. 추론 시 LoRA weight를 base weight에 merge할 수 있음.
- **비유**: 원본 계약서를 새로 쓰지 않고, 특정 조항에 부속 합의서를 붙여 업무 조건만 조정하는 것과 같음.
- **구체 예시**: rank r=8~64로 attention q_proj/v_proj에 적용하면 학습 파라미터를 전체 대비 1% 미만으로 줄일 수 있음.
- **흔한 오해·주의점**: rank 증가는 성능 향상을 보장하지 않음. rank가 높으면 overfitting과 adapter 크기가 증가하므로 평가셋 기준으로 선택해야 함.

## 연결 개념
- PEFT — LoRA의 상위 범주
- QLoRA — 4-bit base model 위 LoRA 학습
- Adapter Registry — LoRA 운영 관리

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LoRA는 weight update ΔW를 저랭크 행렬 A·B로 근사해 소량 파라미터만 학습하는 PEFT 기법임.
> 2. **가치**: LLM 도메인 적응의 GPU 메모리·학습 시간·저장 비용을 줄임.
> 3. **판단 포인트**: rank r, alpha, target module, merge 여부, adapter 버전 관리가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| LoRA 저랭크 근사 원리와 하이퍼파라미터 설계 역량 | ΔW = BA 분해, rank/alpha, target module, merge 전략 | rank를 높이면 항상 개선된다는 오해, adapter 관리 누락 |

> 요약: 출제자는 저랭크 근사 수학 원리와 rank·module 선택의 실무 판단 역량을 확인함.

---

## Ⅰ. 개요 및 필요성

- 정의: weight update ΔW를 저랭크 행렬 A·B로 근사해 소량 파라미터만 학습하는 PEFT 기법
- 배경: LLM 전체 가중치 학습은 GPU 메모리·저장 비용이 커서 도메인별 튜닝이 어려움
- 필요성: 선형층 변화량이 낮은 intrinsic rank를 가진다는 관찰에 기반해 학습 비용을 절감함

## Ⅱ. 구조 및 구성요소

```text
Input x -> Frozen W x
        -> LoRA A(r) -> LoRA B -> scale α/r -> Add -> Output
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Frozen Weight W | 원본 모델 지식 유지 | gradient 없음 |
| Matrix A | down projection | d->r |
| Matrix B | up projection | r->d |
| Rank/Alpha | 용량·스케일 제어 | r=8~64 |

> 요약: LoRA는 원본 선형층 옆에 저랭크 branch를 추가하고 A·B만 학습해 ΔW를 근사함.

## Ⅲ. 동작원리 및 흐름도

```text
target module 선택 -> rank/alpha 설정 -> A·B 학습
    -> adapter 저장 -> merge 또는 동적 로드 -> 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | q_proj/v_proj 등 적용 위치 선택 | task 성능 |
| 2 | rank·alpha·dropout 설정 | r=8/16/32 비교 |
| 3 | LoRA 파라미터만 학습 | trainable params % |
| 4 | merge·서빙·회귀 평가 | latency, F1, rollback |

> 요약: LoRA는 적용 위치와 rank 선택이 정확도·비용·서빙 지연의 균형점을 결정함.

## Ⅳ. 특징

| 구분 | Full FT | LoRA | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 학습 대상 | 전체 weight | A·B 저랭크 행렬 | <1% params 가능 |
| 저장 비용 | 모델 사본 | adapter 파일 | MB~수백MB |
| 서빙 | 단일 모델 | merge 또는 동적 로드 | latency 측정 |
| 한계 | 비용 큼 | rank·module 의존 | 평가셋 기준 |

> 요약: LoRA는 저비용 도메인 적응에 적합하지만 rank와 target module을 업무 기준으로 검증해야 함.

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | Full FT | LoRA | 선택 기준 |
|:---|:---|:---|:---|
| 학습 대상 | 전체 weight | A·B 저랭크 행렬(<1%) | GPU 메모리 제약 여부 |
| 저장·배포 | 모델 사본 필요 | adapter 파일(MB~수백MB) | 도메인 수 × 모델 크기 |
| 서빙 | 단일 모델 | merge 또는 동적 로드 | latency vs 저장 비용 |

> 요약: GPU 메모리·다도메인 저장 제약이 크면 LoRA, 최고 정확도가 필요하면 Full FT를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Rank 과적합 | rank를 과도하게 높임 | r=8/16/32 비교, holdout 평가 | val loss, adapter 크기 |
| Target module 누락 | 적용 위치 선정 오류 | q/k/v/o_proj 조합 실험 | task 정확도 변화 |
| Adapter 관리 실패 | 버전·base hash 불일치 | registry + rollback 정책 | 배포 일치율 |

> 요약: rank 과적합·module 누락·adapter 관리를 grid search, 조합 실험, registry로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 도메인 정확도 | F1 ≥ 0.85, Full FT 대비 gap ≤ 2%p | holdout 평가셋 |
| 서빙 성능 | merge 시 latency 증가 ≤ 5%, 동적 로드 p95 ≤ 200ms | 로드 테스트 |
| Adapter 크기 | tenant별 adapter ≤ 300MB | artifact size 추적 |

> 요약: 도메인 F1, 서빙 latency, adapter 크기를 정량 기준으로 LoRA 도입 성공을 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 사내 QA LoRA는 r=8/16/32를 비교하고 F1, 환각률, latency 기준으로 최적 rank 선택
2. 부서별 adapter는 base model hash, 데이터 버전, 승인자, rollback 경로를 registry에 기록
3. 고정 서비스는 LoRA merge로 latency를 줄이고, 다테넌트 서비스는 동적 adapter 로딩으로 저장 비용 절감

**결론 (2줄):**
- 기술사 판단: 도메인별 저비용 적응은 LoRA, 대규모 지식 재학습은 full FT 또는 RAG 병행을 선택함.
- 향후 방향: LoRA는 QLoRA, multi-LoRA serving, on-device SLM 튜닝의 기본 적응 방식이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | A·B 저랭크 학습 흐름 | Full FT 대비 특징 |
| 요구사항 명시형 | 적용 방안을 제시하시오 | rank·target module 검증 절차 | latency·adapter 관리 기준 |

> 요약: 설명형은 저랭크 근사 원리, 적용형은 rank 선택과 adapter 운영 중심으로 목차를 전환함.
