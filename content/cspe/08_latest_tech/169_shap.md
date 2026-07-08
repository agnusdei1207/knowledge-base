---
title: "SHAP 설명기법 (SHapley Additive exPlanations)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 169
extra:
  question_no: "169"
  exam_status: "기출"
  exam_history: "122회, 135회"
---

## 미리 알고가기

- SHAP은 예측값을 각 특징의 기여도로 분해하는 Shapley value 기반 설명 기법임
- 개별 예측 설명과 전체 모델 해석을 함께 지원할 수 있다는 점이 강점임
- 변수 수가 커질수록 계산 비용이 급증하므로 explainer 선택이 중요함

## Ⅰ. 개요

- **정의/개념**: SHAP은 협조적 게임이론의 Shapley value를 활용해 모델 예측값과 기준값의 차이를 각 특징의 한계 기여도 합으로 분해하여 설명하는 가산형 XAI 기법임
- **배경/필요성**: 규제가 강한 도메인에서는 단순 중요도 순위보다 각 변수의 기여량을 일관되고 수학적으로 설명할 필요가 있으므로, 공리적 성질을 갖춘 설명 방법이 요구됨

## Ⅱ. 특징

- 설명 결과를 각 특징의 양의 기여와 음의 기여로 나누어 예측값 합으로 직관적으로 표현할 수 있음
- local explanation과 global summary를 같은 틀에서 제공해 디버깅과 고객 설명을 함께 지원함
- 일관성과 가산성 같은 공리적 장점이 있어 감사 대응과 비교 분석에 유리함
- 순수 계산은 조합 폭발이 발생하므로 TreeSHAP과 KernelSHAP 같은 근사 또는 최적화 구현이 실무 핵심임

## Ⅲ. 종류 및 비교

| 판단 기준 | KernelSHAP | TreeSHAP | DeepSHAP |
|:---|:---|:---|:---|
| 대상 모델 | 임의의 블랙박스 모델 | 트리 기반 모델 | 신경망 모델 |
| 계산 특성 | 범용적이지만 느림 | 매우 빠르고 실무 친화적 | 구조 의존적 근사 |
| 설명 정확도 | 샘플링 설정에 영향 받음 | 높음 | 모델 구조에 따라 달라짐 |
| 대표 활용 | 외부 API 모델 분석 | XGBoost, LightGBM | DNN 계열 해석 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Baseline Value | 전체 데이터 평균 예측처럼 비교 기준이 되는 시작점을 제공함 |
| Feature Coalition | 특정 특징 조합이 예측에 어떤 영향을 주는지 비교하기 위한 부분집합 구조임 |
| Shapley Contribution | 특징이 조합에 추가될 때 증가하거나 감소시키는 한계 기여도를 평균화한 값임 |
| Explainer Engine | 모델 유형에 맞는 계산 방식으로 SHAP 값을 산출해 실용 속도를 확보함 |
| Visualization Layer | waterfall과 force와 summary plot으로 기여도를 해석 가능한 형태로 보여줌 |

```text
+-------------------+      +-------------------+      +-------------------+
| Baseline Value    | ---> | Coalition Compare | ---> | SHAP Contribution |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Visualize / Use   |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 기준값 설정     | --> | 조합별 기여 계산 | --> | SHAP 값 합산    | --> | 시각화/해석 활용 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **기준값 설정**: 평균 예측 등 비교 기준을 정함
2. **조합별 기여 계산**: 특징 포함 여부에 따른 예측 변화량을 계산함
3. **SHAP 값 합산**: 각 특징의 평균 기여도를 산출해 예측값과 연결함
4. **시각화 및 해석 활용**: 고객 설명과 디버깅과 감사 자료로 사용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 특징 수와 모델 복잡도가 커지면 SHAP 계산 지연이 커져 실시간 서비스 적용이 어려워질 수 있음
   - 해결방안: 모델별 explainer와 background sampling을 최적화하고 explanation latency와 approximation error로 검증함
2. 문제: 기준값과 샘플링 전략이 부적절하면 같은 모델이라도 해석 결과가 왜곡되어 비교 가능성이 떨어질 수 있음
   - 해결방안: baseline governance와 reference dataset 관리를 적용하고 explanation consistency와 drift sensitivity로 검증함
3. 문제: SHAP 시각화가 풍부해도 도메인 맥락 없이 쓰면 상관관계를 인과처럼 오해할 위험이 커질 수 있음
   - 해결방안: domain review와 counterfactual check를 병행하고 expert agreement와 decision reversal rate로 검증함

## Ⅶ. 적용 사례

- 보험 인수심사 모델이 고객별 가산과 감산 요인을 waterfall plot으로 제공하며 확인 지표는 complaint reduction rate와 explanation latency임
- 사기 탐지 모델이 전체 데이터에서 어떤 특징이 지속적으로 위험 신호를 만드는지 분석하며 확인 지표는 fraud capture lift와 global explanation consistency임
- 제조 품질 예측 모델이 이상 상관관계를 찾아 데이터 개선 우선순위를 정하도록 활용되며 확인 지표는 root cause discovery rate와 retraining efficiency임

## Ⅷ. 결론

SHAP은 설명의 수학적 일관성과 실무 활용성을 함께 제공하는 강력한 기법이지만, 계산 비용과 해석 맥락을 통제하는 설계가 함께 따라야 가치가 커짐.
