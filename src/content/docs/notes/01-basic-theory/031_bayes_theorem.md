---
sidebar:
  order: 31
  label: "031. 확률 기초: 베이즈 정리 (Bayes Theorem)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "확률 기초: 베이즈 정리 (Bayes Theorem)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-basic-theory"
weight: 31
extra:
  question_no: "031"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "베이즈 갱신은 불확실성 추론의 기본"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **베이즈 정리(Bayes' Theorem)**: 사전 확률(Prior Probability)과 증거 우도(Likelihood)를 결합하여 관측 데이터 기반 사후 확률(Posterior Probability)을 갱신하는 조건부 확률 이론.
- **조건부 확률(Conditional Probability)**: 특정 사건 A 발생을 전제로 B가 발생할 확률 $P(B|A)$.
- **사전 확률(Prior Probability)**: 새로운 증거 관측 전 가설 H에 대한 초기 신뢰도.
- **사후 확률(Posterior Probability)**: 증거 E 관측 후 갱신된 가설 H의 확률 $P(H|E)$.
- **우도(Likelihood)**: 가설 H가 참일 때 증거 E가 관측될 가능성 $P(E|H)$.
- **기저율(Base Rate)**: 모집단 내 특정 사건의 고유 발생 비율.

</details>

- **정의**: 기저율(Prior)과 우도(Likelihood)를 결합하고 주변 확률(Marginal Probability)로 정규화하여 사후 확률(Posterior)을 갱신하는 베이지안 추론(Bayesian Inference) 체계.
- **배경**: 기저율을 간과한 관측은 기저율 오류(Base Rate Fallacy)를 야기하여 사후 확률 결과를 심각하게 왜곡하므로 반드시 반영 필요.

#### 한줄 요약

- 베이즈 정리 $P(H \mid E) = \frac{P(E \mid H) P(H)}{P(E)}$를 통해 사전 확률과 우도를 결합하여 증거 관측 후의 사후 확률을 갱신한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **양성 예측도(Positive Predictive Value, PPV)**: 검사 양성 판정 시 실제 양성일 확률.
- **민감도(Sensitivity)**: 실제 양성을 양성으로 판정하는 비율.
- **특이도(Specificity)**: 실제 음성을 음성으로 판정하는 비율.
- **오탐(False Positive)**: 실제 음성을 양성으로 오판하는 비율.
- **역확률 추론(Inverse Probability Inference)**: 증거 기반 가설의 사후 확률 추론.

</details>

![기저율에 따른 양성 사후확률 차트](/study/diagrams/bayes-base-rate-ppv.svg)

> 기저율 1%→50% 시 민감도·특이도 90% 동일 조건에서 양성 사후확률은 8.33%→90%로 상승.

- **역확률 추론**: 관측된 증거로부터 원인(가설)의 확률을 사후 갱신하는 통계적 추론 과정.
- **기저율 오류 방지**: 민감도(Sensitivity), 특이도(Specificity) 외 기저율(Base Rate)을 반영한 PPV(Positive Predictive Value) 산출을 통해 확률 추론 정확도 제고.

#### 한줄 요약

- 기저율 오류(Base Rate Fallacy) 방지를 위해 증거의 민감도·특이도와 기저율($P(H)$)을 반영한 PPV 산출.


## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **우도 모형(Likelihood Model)**: 가설별 증거 발생 확률($P(E \mid H)$) 계산.
- **주변 확률(Marginal Probability, $P(E)$)**: 모든 가설에 대한 증거의 총 확률.
- **확률 상태(Probability State)**: 갱신된 사후 확률을 보관하는 정보.
- **정규화(Normalization)**: 확률의 총합을 1로 보정하는 과정.

</details>

```text
  [우도 모형(Likelihood Model)]
             |
  [갱신 연산기(Updater)] -- [확률 상태(Probability State)]
```

선의 의미: 갱신 연산기가 우도 모형의 가설별 적합도와 확률 상태의 사전·사후 확률을 함께 활용하는 정적 의존 관계.

| 구성요소 | 책임 |
|:---|:---|
| 우도 모형(Likelihood Model) | 가설별 우도(Likelihood) $P(E \mid H)$ 산출 |
| 갱신 연산기(Updater) | 주변 확률로 사후 확률(Posterior) 정규화 |
| 확률 상태(Probability State) | 갱신 결과를 다음 사전 확률(Prior)로 보관 |

#### 한줄 요약

- 우도 모형이 증거의 가설별 적합도를 계산하고, 갱신 연산기가 사전 확률과 결합해 새 확률 상태를 만든다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **$P(H\mid E)$**: 증거 $E$를 관측한 뒤 가설 $H$가 참일 사후 확률이다.
- **적용 조건 $P(E)>0$**: 베이즈 식의 분모인 증거 확률이 0이 아니어야 한다는 조건이다.

</details>

```text
    [가설 및 증거 관측]
              |
              v
    1. 사전 확률 설정(Prior)
              |
              v
    2. 가설별 우도 계산(Likelihood)
              |
              v
    3. 사전 확률·우도 결합(Joint Prob.)
              |
              v
    4. 주변 확률 정규화(Normalization)
              |
              v
    [사후 확률 산출(Posterior)]
              |
              `-- 차기 증거 관측 시 사전 확률로 순환
```

$$P(H \mid E)=\frac{P(E \mid H)P(H)}{P(E)}$$

### 동작 원리

- **1. 사전 확률 설정**: 관측 전 가설별 기저율(Base Rate) 설정.
- **2. 가설별 우도 계산**: 증거의 조건부 확률 산출.
- **3. 사전 확률•우도 결합**: 가설별 비정규 가중치 계산.
- **4. 주변 확률로 정규화**: 총합 1인 사후 확률 산출.

#### 한줄 요약

- Prior $P(H)$ $\times$ 우도 $P(E \mid H)$의 곱을 Total Probability Theorem 기반 Marginal 우도 $P(E) = \sum P(E \mid H_i)P(H_i)$로 정규화하여 Posterior를 획정한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **베이지안 통계**: 모수의 불확실성을 확률로 표현하고 증거로 사전 확률을 갱신하는 관점이다.
- **빈도주의 통계**: 모수를 고정값으로 보고 반복 실험의 장기 빈도로 추정과 오류를 해석하는 관점이다.
- **모수(Parameter)**: 확률 모형의 분포와 동작을 결정하는 값이다.
- **장기 오류율**: 같은 절차를 반복했을 때 잘못된 결론이 발생하는 비율이다.
- **사전 정보**: 현재 표본을 관측하기 전에 알고 있던 지식이나 과거 자료이다.

</details>

| 통계적 추론 관점 | 베이지안 통계(Bayesian) | 빈도주의 통계(Frequentist) |
|:---|:---|:---|
| 적용 기준 | **사전 정보(Prior Info)** 존재 및 표본 소량 시 | **장기 오류율(Long-run Error)** 통제 목표 시 |
| 핵심 특징 | **사전•사후 확률** 갱신 | 반복 표본으로 **고정 모수(Fixed Parameter)** 추정 |
| 한계 | **사전 확률** 선택 의존성 | **모수**를 확률변수로 미해석 |

#### 한줄 요약

- Prior-Posterior Updating 중심의 Bayesian Inference와 Long-run Frequency/Fixed 모수 기반 Frequentist Inference의 패러다임을 차등 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **조건부 의존**: 다른 조건을 고정해도 두 증거 사이의 확률 관계가 남는 성질이다.
- **민감도 분석**: 사전 분포 같은 가정을 바꿨을 때 결론이 얼마나 달라지는지 확인하는 절차이다.
- **강건성(Robustness)**: 모형 가정이나 입력이 일부 달라져도 결론이 크게 변하지 않는 성질이다.
- **확률 보정**: 예측 확률과 실제 발생 빈도가 일치하도록 모형 출력을 조정하는 절차이다.
- **사전 분포(Prior Distribution)**: 증거를 관측하기 전에 모수나 가설에 부여한 확률분포이다.
- **분포 변화(Distribution Shift)**: 운영 데이터의 확률분포가 모형을 학습하거나 검증한 때와 달라진 상태이다.
- **재학습(Retraining)**: 새 데이터로 모형의 매개변수를 다시 학습하는 작업이다.
- **증거 중복**: 조건부 의존 증거를 독립으로 가정해 같은 정보를 여러 번 반영하는 오류이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 희귀 사건의 **기저율(Base Rate)** 무시 | 모집단 **사전 확률(Prior)** 명시 | 양성 결과의 **PPV** 과대평가 방지 |
| 상관 증거의 **증거 중복(Redundancy)** | **조건부 의존(Conditional Dependency)** 구조 모형화 | 사후 확률의 과대 추정 방지 |
| 주관적 **사전 분포(Prior Distribution)** 선택 | 복수 사전 분포의 **민감도 분석(Sensitivity Analysis)** | 결론의 **강건성(Robustness)** 확인 |
| 우도 모형의 **분포 변화(Distribution Shift)** | **확률 보정(Calibration)** 및 **재학습(Retraining)** | 운영 분포 기반 사후 확률 갱신 |

#### 한줄 요약

- Naive Bayes의 Conditional Independence 가정이 깨질 경우 Joint 우도 모형화 및 Calibration / 재학습으로 Overshooting을 방지한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **희귀 사건**: 모집단에서 발생 비율인 기저율이 매우 낮은 사건이다.
- **독립적 추가 증거**: 기존 증거와 조건부 의존이 없어 새로운 정보를 제공하는 관측이다.

</details>

- **희귀 사건** 기저율 반영 및 **독립적 추가 증거(Independent Evidence)** 기반 순차적 사후 확률 갱신 체계 적용.

