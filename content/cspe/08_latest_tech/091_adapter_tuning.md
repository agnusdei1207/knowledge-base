---
title: "어댑터 튜닝 (Adapter Tuning)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 91
---

# 📖 【암기용】 개념 완전 이해

> 목적: Adapter Tuning을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 사전학습 모델 내부 레이어 사이에 작은 adapter 모듈을 삽입하고 그 모듈만 학습하는 PEFT 기법
- **왜 필요한가**: 업무별로 전체 모델을 복사·학습하면 저장 비용과 운영 비용이 증가함.
- **핵심 직관**: 건물 구조는 그대로 두고, 부서별 업무에 필요한 작은 회의실 모듈만 추가하는 방식임.

## 깊이 이해
- **배경·문제의식**: Full Fine-Tuning은 전체 가중치를 바꾸므로 도메인별 모델 사본이 필요함. Adapter는 base model을 freeze하고 작은 bottleneck network만 학습해 업무별 모듈로 분리함.
- **작동 원리**: Transformer layer의 attention 또는 FFN 뒤에 down-projection->activation->up-projection 구조를 삽입함. 학습 시 adapter만 업데이트하고 base model은 공유함.
- **비유**: 공통 교과서에 과목별 별책 부록을 끼워 넣어, 교과서 본문은 유지하면서 과목별 설명을 보강하는 것과 같음.
- **구체 예시**: 병원·금융·제조 업무별 adapter를 같은 base model에 붙여 tenant별로 로드하면 모델 저장 비용을 줄일 수 있음.
- **흔한 오해·주의점**: Adapter는 추론 시 레이어에 추가 연산을 넣으므로 latency가 증가할 수 있음. merge 가능성은 LoRA보다 제한적임.

## 연결 개념
- PEFT — Adapter Tuning의 상위 범주
- LoRA — 저랭크 branch 기반 대안
- Multi-Adapter Serving — 업무별 adapter 운영 방식

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Adapter Tuning은 Transformer 내부에 작은 bottleneck module을 삽입하고 그 모듈만 학습하는 PEFT 기법임.
> 2. **가치**: base model을 공유하면서 업무별 adapter만 저장해 다도메인 운영 비용을 줄임.
> 3. **판단 포인트**: adapter 위치, bottleneck 차원, latency overhead, adapter routing이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| PEFT 기법 간 구조 차이와 선택 기준 이해 | bottleneck 구조(d→m→d), base model freeze, adapter registry | LoRA와 혼동, merge 가능성 과장, latency overhead 누락 |

> 요약: adapter의 삽입 위치·bottleneck 구조·LoRA 대비 차이와 추론 latency를 짚어야 함

---

## Ⅰ. 개요 및 필요성

- 정의: Transformer 레이어에 bottleneck module을 삽입해 해당 모듈만 학습하는 PEFT 기법
- 배경: Full Fine-Tuning은 업무별로 전체 모델 사본을 저장·학습해야 하므로 비용이 과다함
- 필요성: base model을 공유하면서 업무별 adapter만 저장해 다도메인 운영 비용을 절감함

## Ⅱ. 구조 및 구성요소

```text
Transformer Layer -> Adapter Down-Projection -> Activation
      -> Up-Projection -> Residual Add -> Next Layer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Bottleneck Down | 차원 축소 | d->m |
| Activation | 비선형 변환 | GELU/ReLU |
| Up Projection | 원 차원 복원 | m->d |
| Adapter Registry | 업무별 모듈 관리 | tenant routing |

> 요약: Adapter는 레이어 사이에 작은 병목 모듈을 삽입해 업무별 추가 지식을 분리 저장함.

## Ⅲ. 동작원리 및 흐름도

```text
base model freeze -> adapter 삽입 -> adapter만 학습
    -> 업무별 adapter 저장 -> 요청별 adapter 로드 -> 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 삽입 위치·bottleneck 차원 결정 | trainable params |
| 2 | adapter만 gradient 업데이트 | loss, overfitting |
| 3 | 업무별 adapter 저장 | artifact size |
| 4 | 추론 latency·정확도 평가 | p95 latency, F1 |

> 요약: Adapter Tuning은 학습 비용을 줄이지만 삽입 모듈로 인한 추론 지연을 함께 검증해야 함.

## Ⅳ. 특징

| 구분 | LoRA | Adapter Tuning | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 구조 | 저랭크 branch | bottleneck module | layer 삽입 |
| merge | 비교적 용이 | 제한적 | 서빙 latency |
| 저장 | adapter weight | adapter module | MB~수백MB |
| 운영 | rank 관리 | routing·로드 관리 | tenant별 버전 |

> 요약: Adapter는 업무별 모듈 분리가 명확하지만, 추론 시 추가 레이어 비용을 측정해야 함.

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | LoRA | Adapter Tuning | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 저랭크 branch (W+ΔW) | bottleneck module 삽입 | 모듈 격리 vs merge 용이성 |
| 추론 비용 | merge 후 추가 비용 0 | 삽입 모듈로 p95 latency 5~15% 증가 | 실시간 서빙 지연 허용 범위 |
| 운영 | rank·alpha 관리 | adapter registry·tenant routing | 다테넌트 분리 요구 수준 |

> 요약: merge 가능성과 latency가 중요하면 LoRA, 업무별 모듈 격리가 중요하면 Adapter를 선택함

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 추론 latency 증가 | 삽입 모듈의 추가 연산 | bottleneck 차원 축소, batch 최적화 | p95 latency |
| adapter 충돌 | 동일 base에 다수 adapter 로드 | registry 기반 버전·격리 관리 | tenant별 오류율 |
| 과적합 | 소량 데이터로 adapter만 학습 | early stopping, validation loss 모니터링 | F1, 일반화 gap |

> 요약: 추론 latency와 adapter 충돌을 registry·차원 관리로 통제해야 함

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 추론 성능 | p95 latency 100ms 이하 | API 벤치마크, 부하 테스트 |
| task 정확도 | F1 ≥ 0.85 | 도메인별 평가 데이터셋 |
| 운영 안정성 | adapter 로드 실패율 < 0.1% | registry 모니터링, 로그 |

> 요약: latency·정확도·로드 안정성을 정량 측정해 adapter 도입 효과를 판단함

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 부서별 domain adapter를 base model 하나에 연결하고 adapter registry로 버전·권한·rollback 관리
2. bottleneck 차원 16/32/64를 비교해 F1과 p95 latency 기준으로 선택
3. 실시간 API는 LoRA merge 가능성을 우선 검토하고, 다테넌트 분리 요구가 크면 Adapter를 적용

**결론 (2줄):**
- 기술사 판단: 업무별 모듈 격리와 관리성을 우선하면 Adapter, latency와 merge를 우선하면 LoRA를 선택함.
- 향후 방향: Adapter는 multi-tenant LLM serving과 domain routing에서 모듈형 적응 방식으로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | adapter 삽입·학습 흐름 | LoRA 대비 특징 |
| 요구사항 명시형 | 도입 방안을 제시하시오 | registry·latency 검증 절차 | 다테넌트·버전관리 기준 |

> 요약: 설명형은 adapter 구조, 도입형은 업무별 모듈 운영과 지연 검증 중심으로 목차를 전환함.
