---
sidebar:
  order: 105
  label: "105. LIME (국소 대리 설명)"
  badge:
    text: "기출 · 40%"
    variant: note
title: "LIME (국소 대리 설명)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest-tech"
weight: 105
extra:
  question_no: "105"
  source_status: "기출"
  source_history: "122회, 135회"
  priority: 40
  priority_note: "국소 대리 설명은 설명가능 AI 세부 기법"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **국소 해석 가능 모델 불가지론 설명(Local Interpretable Model-agnostic Explanations, LIME)**: 예측 주변을 단순 대리모델로 근사한다.
- **모델 불가지론(Model-agnostic)**: 입력•출력 호출만으로 설명할 수 있는 성질이다.

</details>

- 정의: 입력 주변의 모델 행동을 단순 모델로 근사하는 **LIME**이다.
- 배경/필요성: 복잡한 비선형 블랙박스 머신러닝 모델(Deep Neural Networks, Random Forest, XGBoost)은 모델 전체 차원에서는 극도로 복잡한 비선형 결정 경계(Decision Boundary)를 가지므로 전역적으로 해석하는 것이 불가능하며, 내부 가중치에 접근할 수 없는 상용 API 기반 모델의 경우 개별 데이터 포인트에 대한 예측 이유를 즉각적으로 규명할 수 없는 한계가 존재함에 따라, 해석하고자 하는 특정 데이터 인스턴스의 국소적 근방(Local Neighborhood)에 무작위 교란(Perturbation) 표본을 생성하고 지수 근접 커널 가중치와 단순 선형/의사결정트리 대리 모델(Interpretable Surrogate Model)을 학습시키는 LIME(Local Interpretable Model-agnostic Explanations: Sparse Linear Surrogate, Exponential Proximity Kernel, Submodular Pick) 알고리즘을 도입하여 **모델 구조나 학습 방식에 무관(Model-Agnostic)하게 텍스트, 이미지, 정형 데이터 등 모든 블랙박스 모델의 개별 예측에 대한 국소 특성 기여도(Local Feature Importance) 즉시 산출, 관심 영역 주변의 국소 결정 경계 근사를 통한 인간 친화적이고 직관적인 예측 근거 시각화, 모델 디버깅 및 이상 예측 원인 추적성 극대화**를 달성할 필요

#### 한줄 요약
- 교란 표본으로 **블랙박스 국소 경계**를 단순 모델로 근사

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **교란 표본(Perturbed Sample)**: 특징을 바꿔 블랙박스 주변 반응을 관찰한다.
- **국소 대리모델(Local Surrogate Model)**: 원본 주변의 블랙박스 예측을 근사한다.
- **설명 변동성(Explanation Variability)**: 표본•커널에 따라 설명이 달라지는 성질이다.

</details>

- 예측 호출만 사용하는 **모델 비종속 설명**
- 거리 가중 교란 표본 기반 **국소 대리모델**
- 교란 분포•커널에 따른 **설명 변동성**

#### 한줄 요약
- **모델 불가지론•국소 근사•설명 변동성** 결합

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **근접 커널(Proximity Kernel)**: 원본과 표본의 거리를 학습 가중치로 변환한다.
- **블랙박스 함수(Black-box Function)**: 입력에 대한 예측값만 반환한다.
- **교란 표본 생성기**: 원본 주변의 특징을 바꾼 표본을 만든다.
- **대리모델 학습**: 가중 표본•예측값으로 국소 행동을 근사한다.

</details>

```text
                 [교란 표본 생성기]
                         |
              +----------+----------+
              |                     |
          [근접 커널]          [블랙박스 함수]
              |                     |
              +----------+----------+
                         |
                 [국소 대리모델]
```

| 구성요소 | 책임 |
|:---|:---|
| 교란 표본 생성기 | 원본 특징을 변형한 **주변 입력** 생성 |
| 근접 커널 | 거리를 **학습 가중치**로 변환 |
| 블랙박스 함수 | 교란 표본의 **모델 예측값** 반환 |
| 국소 대리모델 | 가중 표본으로 **블랙박스 출력** 근사 |

#### 한줄 요약
- **교란 표본•근접 커널•블랙박스•대리모델** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **마스킹(Masking)**: 입력 특징을 제거•대체해 모델 반응을 관찰한다.
- **거리 가중치(Distance Weight)**: 가까운 표본을 더 크게 반영하는 값이다.

</details>

```text
설명 요청자 ── 원본•설명 요청 ──▶ 교란 표본 생성기
                                  │ 1. 교란 표본 생성
                                  ├─ 2. 블랙박스 예측 수집 ──▶ 블랙박스 함수 ─┐
                                  └─ 3. 거리 가중치 계산 ────▶ 근접 커널 ─────┤
                                                  ▼
                                           국소 대리모델
                                                  │ 4. 가중 국소 대리모델 학습
                                                  └── 특징 기여도•충실도 ──▶ 설명 요청자
```

### 동작 원리

1. 교란 표본 생성: 원본 주변 특징의 **마스킹•변형**
2. 블랙박스 예측 수집: 교란 표본별 **모델 반응** 획득
3. 거리 가중치 계산: 원본과 가까운 표본에 **고가중치** 부여
4. 가중 국소 대리모델 학습: 주변 **예측 경계**의 단순 모델 근사

#### 한줄 요약
- **교란•예측 수집•거리 가중•국소 대리 학습** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **샤플리 가산 설명(SHapley Additive exPlanations, SHAP)**: 예측 차이를 샤플리 값으로 기여도에 배분한다.
- **특징 기여도(Feature Attribution)**: 특징이 예측을 증감시킨 영향의 크기이다.

</details>

| 국소 설명 기법 | LIME | SHAP |
|:---|:---|:---|
| 적용 기준 | 국소 영역의 빠른 **근사 설명** | 기준값 대비 일관된 **기여 배분** |
| 핵심 특징 | **주변 표본•대리 모델** 근사 | **샤플리 값** 기반 기여 배분 |
| 한계 | 표본•커널별 **설명 변동** | 특징 수 증가 시 **계산 비용** |

#### 한줄 요약
- **국소 경계 근사•일관된 기여 배분** 목적에 따른 기법 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **국소 충실도 저하**: 표본이 유효 근방을 벗어나 판단을 잘못 근사한 문제이다.
- **설명 재현성(Explanation Reproducibility)**: 반복 설명의 기여도가 일관된 정도이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 교란 분포 이탈에 따른 **국소 충실도 저하** | 도메인 유효 변환•커널 폭 검증 | 대리모델의 **근방 근사력** 향상 |
| 무작위 표본에 따른 **설명 변동성** | 시드•표본 수 고정과 반복 안정성 평가 | 특징 기여도 **재현성 확보** |

#### 한줄 요약
- **교란 유효성•커널 폭•표본 수•설명 재현성** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **국소 충실도(Local Fidelity)**: 대리모델이 입력 주변 예측을 근사하는 정도이다.
- **커널 폭(Kernel Width)**: 국소 설명에 반영할 표본의 거리 범위이다.

</details>

- 모델 불가지론(Model-Agnostic) 철학을 바탕으로 국소 선형 근사를 통해 임의의 복잡한 블랙박스 모델에 대한 개별 예측 해석의 지평을 연 **설명 가능한 AI(XAI) 분야의 대표적 국소 대리 모델링 알고리즘(LIME / Model-Agnostic Local Surrogate / Perturbation-based Sampling & Exponential Proximity Kernel / Sparse Linear Explanation / Image Superpixel & Text Word Masking / Fast Local Attribution)의 핵심 표준**으로 확고히 자리 잡았으며, 대규모 실시간 추론 해석 파이프라인으로 지속 활용되는 가운데, 실무 LIME 해석 파이프라인 구축 시에는 **무작위 표본 추출로 인해 설명 결과가 매 실행마다 미세하게 흔들리는 설명 변동성(Instability)을 제어하기 위해 충분한 교란 표본 수($N \ge 5,000$)와 난수 시드(Seed) 고정을 적용하고, 대상 도메인의 특성에 부합하는 커널 폭(Kernel Width) 최적화를 수행하며, 연산 속도가 중요할 때는 LIME을, 엄밀한 이론적 기여도 배분이 필요할 때는 TreeSHAP/KernelSHAP을 상호보완적으로 연계**를 결합하여 완벽한 설명 직관성과 안정적인 해석 품질을 완성

#### 한줄 요약
- **국소 충실도•설명 안정성**에 따라 교란 범위•커널 폭 결정
