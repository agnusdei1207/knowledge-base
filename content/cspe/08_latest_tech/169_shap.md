---
title: "SHAP 설명기법 (SHapley Additive exPlanations)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 169
---

# 📖 【암기용】 개념 완전 이해

> 목적: SHAP을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 게임이론의 Shapley value를 이용해 각 feature가 모델 예측에 기여한 정도를 계산하는 설명기법
- **왜 필요한가**: 예측 결과에 어떤 특성이 얼마나 기여했는지 일관된 기준으로 설명해야 함.
- **핵심 직관**: 팀 프로젝트 성과를 각 팀원이 얼마나 기여했는지 공정하게 나누는 게임이론을 모델 설명에 적용함.

## 깊이 이해
- **배경·문제의식**: Feature importance는 모델별로 기준이 다르고 local 예측 설명과 global 설명을 연결하기 어렵다. SHAP은 공리적 기여도 산정 기준을 제공함.
- **작동 원리**: feature 집합의 모든 조합에서 해당 feature가 추가될 때 예측값을 얼마나 바꾸는지 평균해 Shapley value를 계산함.
- **비유**: 선수 A가 팀에 들어왔을 때 다양한 팀 조합에서 승률을 얼마나 올렸는지 평균해 A의 공헌도를 계산하는 방식임.
- **구체 예시**: 대출 모델에서 DTI +0.18, 연체 이력 +0.12, 소득 -0.08처럼 예측 점수에 대한 feature별 기여도를 표시.
- **흔한 오해·주의점**: SHAP 값은 상관관계가 높은 feature에서 해석이 어려울 수 있고, 정확 계산은 feature 수가 많으면 비용이 커짐.

## 연결 개념
- Explainable AI — 모델 설명가능성 분야
- LIME — 국소 대리모델 기반 설명기법
- Feature Attribution — 예측에 대한 feature 기여도 산정

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SHAP은 Shapley value로 feature별 예측 기여도를 일관되게 산정하는 XAI 기법임.
> 2. **가치**: local 설명과 global feature importance를 연결해 감사·모델 개선·고객 설명에 활용함.
> 3. **판단 포인트**: 계산 비용, feature 상관성, baseline 선택이 해석 품질을 좌우함.

## Ⅰ. 개요 및 필요성

SHAP은 게임이론 기반 feature attribution 기법이다. AI 예측 결과를 설명하려면 각 feature가 예측을 얼마나 올리거나 낮췄는지 정량화해야 한다. SHAP은 일관성과 가산성을 가진 설명값을 제공한다.

## Ⅱ. 구조 및 구성요소

```text
Model + Instance + Background Data
  → Shapley Value Estimation → SHAP Values → Local/Global Explanation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Background Data | 기준 예측값 산정 | baseline 영향 큼 |
| Coalition Sampling | feature 조합 평가 | feature 수 증가 시 비용 증가 |
| SHAP Explainer | Shapley value 추정 | TreeSHAP, KernelSHAP |
| Visualization | 기여도 해석 | waterfall, summary plot |

> 요약: SHAP은 기준 데이터와 feature 조합 평가를 통해 예측값에 대한 feature별 기여도를 계산함.

## Ⅲ. 동작원리 및 흐름도

```text
설명 대상 선택 → baseline 설정 → feature 조합 평가
  → marginal contribution 평균 → SHAP 값 산출 → 시각화
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | background sample과 baseline 정의 | 대표 표본 1천 건 이상 |
| 2 | feature 조합별 예측 변화 평가 | sampling error 관리 |
| 3 | Shapley value로 기여도 산정 | additivity error <1e-3 |
| 4 | local/global 설명 시각화 | 상위 feature 안정성 ≥90% |

> 요약: SHAP은 feature가 여러 조합에 참여할 때의 평균 기여도를 계산해 예측 설명을 제공함.

## Ⅳ. 특징

| 구분 | LIME | SHAP | 판단 포인트 |
|:---|:---|:---|:---|
| 이론 기반 | 국소 근사 | Shapley value 공리 | 일관성은 SHAP |
| 설명 범위 | local 중심 | local+global | 감사·보고에 적합 |
| 계산 비용 | 샘플 수 기반 | feature 조합 비용 | TreeSHAP으로 최적화 |
| 한계 | 불안정 가능 | 상관 feature 해석 주의 | baseline 검토 |

> 요약: SHAP은 일관된 기여도 설명이 강점이나 계산 비용과 상관 feature 해석을 관리해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 금융 모델: 대출 승인·거절별 SHAP waterfall을 제공하고 상위 3개 사유를 고객 설명·내부 감사에 활용
2. 모델 모니터링: 월별 global SHAP feature ranking 변동률 20% 초과 시 데이터 drift 점검
3. 비용 최적화: XGBoost·LightGBM은 TreeSHAP, 딥러닝 black-box는 KernelSHAP 표본 1천 건 이하로 제한

**결론 (2줄):**
- 기술사 판단: 규제·감사 목적 feature attribution은 SHAP, 빠른 local 설명은 LIME 병행
- 향후 방향: SHAP 설명을 모델 카드와 AI 영향평가에 자동 연결해 AI 거버넌스 증적으로 활용

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SHAP을 설명하시오" | baseline→feature 조합→Shapley value 흐름 | LIME 대비 차이 |
| 요구사항 명시형 | "모델 설명가능성 방안을 제시하시오" | local/global 설명·시각화 기준 | 감사·drift 모니터링 활용 |

> 요약: 설명형은 Shapley 기여도 원리, 방안형은 감사와 운영 모니터링 적용을 중심으로 작성함.
