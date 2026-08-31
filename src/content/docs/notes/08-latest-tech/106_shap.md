---
sidebar:
  order: 106
  label: "106. SHAP 설명 기법 (SHapley Additive exPlanations)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "SHAP 설명 기법 (SHapley Additive exPlanations)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest_tech"
weight: 106
extra:
  question_no: "106"
  source_status: "기출"
  source_history: "122회, 135회"
  priority: 50
  priority_note: "기여도 기반 설명은 비교 출제 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **샤플리 가산 설명(SHapley Additive exPlanations, SHAP)**: 예측 차이를 특징별 샤플리 값으로 분해한다.
- **샤플리 값(Shapley Value)**: 모든 특징 연합의 한계 기여를 가중 평균한 값이다.

</details>

- 정의: 기준값과 예측값 차이를 특징별로 분해하는 **SHAP**이다.
- 배경/필요성: 전통적인 특성 중요도(Feature Importance: Permutation Importance, Gain) 기법은 특성 간의 비선형 상호작용이나 다중공선성(Multicollinearity)이 존재할 경우 특성의 제거 순서나 트리 분할 위치에 따라 중요도가 심각하게 왜곡되며, "기본 예측값 대비 각 입력 특성이 출력에 얼마나 기여했는가"를 수학적으로 공정하고 일관되게 배분하지 못하는 이론적 결함에 직면함에 따라, 협조적 게임 이론(Cooperative Game Theory)의 샤플리 값(Shapley Value) 원리와 가산 공리(효율성, 대칭성, 더미, 가산성)를 머신러닝 해석에 최초로 적용한 SHAP(SHapley Additive exPlanations / TreeSHAP, KernelSHAP, DeepSHAP / Baseline Expected Value & Local Additivity) 알고리즘을 도입하여 **수학적으로 증명된 공정 배분 공리를 만족하는 유일한 특성 기여도(Shapley Value) 산출, 기준값(Base Value)과 특성 기여도의 합이 최종 예측값과 정확히 일치하는 가산 완전성(Local Accuracy/Additivity) 실현, 정형 데이터(TreeSHAP), 비정형 텍스트/이미지(DeepSHAP/KernelSHAP)를 아우르는 통합 설명 프레임워크 확립**을 달성할 필요

#### 한줄 요약
- **기준값•특징 기여도 합** 기반 개별 예측 설명

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **샤플리 공정 배분(Shapley Allocation)**: 대칭성•효율성 원칙으로 기여 몫을 나눈다.
- **가산 완전성(Additivity)**: 기준값과 기여도 합이 예측값과 일치한다.
- **배경 분포(Background Distribution)**: 기대 출력과 대체 값을 정하는 기준 데이터이다.

</details>

![SHAP 특징 기여의 가산 원리](/study/diagrams/shap-additive-contribution.svg)

> 기준값 0.42에 양•음 기여를 더한 예측값 0.64의 가산 예시

- 모든 특징 순서의 한계 기여를 평균한 **샤플리 공정 배분**
- `예측값 = 기준값 + 기여도 합`의 **가산 완전성**
- 배경 분포•상관 특징 가정에 따른 **설명 민감성**

#### 한줄 요약
- **공정 배분•가산 완전성•배경 분포 민감성** 결합

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **특징 연합(Feature Coalition)**: 함께 존재한다고 가정한 특징 부분집합이다.
- **마스커(Masker)**: 제외 특징을 배경값으로 대체한다.
- **한계 기여(Marginal Contribution)**: 특징 추가 전후의 모델 출력 차이다.

</details>

```text
                   [모델 출력기]
                         |
                [배경 분포•마스커]
                         |
                [연합 가치 계산기]
                         |
                    [SHAP 계산기]
                         |
                [설명 결과 저장소]
```

| 구성요소 | 책임 |
|:---|:---|
| 모델 출력기 | 특징 연합별 **예측값 계산** |
| 배경 분포•마스커 | 제외 특징의 **기준값 대체** |
| 연합 가치 계산기 | 특징 집합별 **기대 출력 산출** |
| SHAP 계산기 | 가중 평균 기반 **한계 기여 배분** |
| 설명 결과 저장소 | 기준값•특징별 기여도의 **가산 결과 보관** |

#### 한줄 요약
- **출력기•배경•연합 가치•SHAP 계산•결과 저장** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **연합 가치(Coalition Value)**: 특정 특징 연합이 만드는 기대 출력이다.
- **부분집합(Subset)**: 전체 특징 중 일부로 구성한 집합이다.

</details>

```text
설명 요청자 ── 모델•배경 지정 ──▶ 배경 마스커
                                  │ 1. 설명 대상•배경 설정
┌──────────── 특징 연합 평가 종료까지 ────────────┐
│ 배경 마스커 ── 2. 특징 연합 구성 ──▶ 연합 계산기
│ 연합 계산기 ── 3. 연합별 모델 출력 계산 ──▶ 모델 출력기
│ 연합 계산기 ◀── 연합별 예측값 ─────────── 모델 출력기
│ 연합 계산기 ── 4. 특징별 한계 기여 계산 ──▶ SHAP 계산기
└─────────────────────────────────────────────────┘
SHAP 계산기
   │ 5. 샤플리 값 집계•가산 검증
   └── 특징 기여도•검증 결과 ──▶ 설명 요청자
```

### 동작 원리

1. 설명 대상•배경 설정: **기준 출력•마스킹 분포** 결정
2. 특징 연합 구성: 특징의 **포함•제외 부분집합** 생성
3. 연합별 모델 출력 계산: 특징 조합별 **예측값** 산출
4. 특징별 한계 기여 계산: 특징 추가 전후 **출력 차이** 측정
5. 샤플리 값 집계•가산 검증: **가중 평균•예측 차이 합산** 확인

#### 한줄 요약
- **배경 설정•연합 구성•출력•한계 기여•가산 검증** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Kernel SHAP**: 모델 비종속 특징 연합 표본으로 기여도를 근사한다.
- **Tree SHAP**: 트리 분기 구조로 기여도를 효율 계산한다.
- **Deep SHAP**: 신경망 기준 출력•역전파로 기여도를 근사한다.

</details>

| 구분 | Kernel SHAP | Tree SHAP | Deep SHAP |
|:---|:---|:---|:---|
| 적용 기준 | **모델 비종속** 설명 | **트리 모델** 설명 | **심층 모델** 근사 설명 |
| 핵심 특징 | 표본 추출 기반 **기여도 근사** | 트리 구조 기반 **효율 계산** | 기준 내부 출력 기반 **역전파 근사** |
| 한계 | 높은 **계산량•분산** | **트리 모델** 한정 | **근사 가정•기준값** 민감 |

#### 한줄 요약
- **모델 비종속•트리•심층 모델**에 따른 계산 방식 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **기준 왜곡(Baseline Distortion)**: 배경 분포가 운영 집단과 어긋난 문제이다.
- **기여도 분산(Attribution Dispersion)**: 상관 특징의 몫이 가정에 따라 나뉘는 문제이다.
- **조합 계산 폭증(Combinatorial Explosion)**: 특징 연합 수가 지수 증가하는 문제이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대표성 없는 **배경 분포의 기준 왜곡** | 운영 집단별 배경 표본•기준값 비교 | 기여도 기준의 **타당성 확보** |
| 상관 특징의 **기여도 임의 분산** | 조건부•독립 마스킹 가정별 민감도 분석 | 의존성 가정의 **영향 공개** |
| Kernel SHAP의 **조합 계산 폭증** | 모델 구조별 전용 계산기•표본 오차 시험 | 계산 시간 단축과 **근사 오차 관리** |

#### 한줄 요약
- **배경 대표성•상관 특징 가정•근사 오차•계산량** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **해석 범위(Interpretation Scope)**: 배경•모델•특징 의존성 가정 내 유효 영역이다.
- **배경 대표성(Background Representativeness)**: 기준 데이터가 운영 분포를 반영하는 정도이다.

</details>

- 협조 게임 이론의 샤플리 공리를 기계학습 해석에 완벽히 이식하여 모델 예측의 특성 기여도 배분에 대한 수학적 유일성과 공정성을 보장한 **설명 가능한 AI(XAI) 분야의 최고 권위 표준 알고리즘(SHAP / Shapley Values / 4 Axioms: Efficiency, Symmetry, Dummy, Additivity / TreeSHAP $O(TLD^2)$ & KernelSHAP / Force Plot, Waterfall & Summary Plot)의 절대적 표준**으로 확고히 자리 잡았으며, LLM 어텐션 기여도 및 피처 어트리뷰션으로 진화하는 가운데, 실무 SHAP 분석 파이프라인 구축 시에는 **배경 데이터셋(Background Dataset)의 크기와 대표성을 정밀 검증하여 기준값 왜곡을 방지하고, 트리 기반 모델(XGBoost, LightGBM)에는 초고속 TreeSHAP을, 딥러닝에는 DeepSHAP/Integrated Gradients를 채택하여 계산 병목을 해소하며, 단일 인스턴스 해석(Force Plot)과 전역 피처 요약(Summary Plot)을 결합**하여 완벽한 설명 신뢰성과 전사적 모델 해석력을 완성

#### 한줄 요약
- **모델 구조•배경 대표성**에 따라 SHAP 계산기•해석 범위 결정
