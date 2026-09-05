---
sidebar:
  order: 90
  label: "090. Diffusion Model (확산모델)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "Diffusion Model (확산모델)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest-tech"
weight: 90
extra:
  question_no: "090"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "잡음 제거 생성 원리가 대표 출제 후보"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **확산모델(Diffusion Model)**: 순방향 잡음 추가와 역방향 제거로 표본을 생성한다.
- **모드 붕괴(Mode Collapse)**: 생성 분포의 일부 유형만 반복 생성하는 현상이다.
- **생성적 적대 신경망(Generative Adversarial Network, GAN)**: 생성기•판별기 경쟁으로 데이터를 생성한다.

</details>

- 정의: 순방향 잡음 추가와 역방향 제거를 학습하는 **확산모델**이다.
- 배경/필요성: 기존의 대표적 생성 모델인 GAN(Generative Adversarial Network)은 생성자(Generator)와 판별자(Discriminator) 간의 적대적 미니맥스 게임에 의존하므로, 학습 과정이 극도로 불안정하고 특정 패턴의 이미지만 반복 생성하는 모드 붕괴(Mode Collapse) 및 기울기 소실 문제가 빈번히 발생하는 치명적 한계가 존재함에 따라, 원본 데이터에 점진적으로 가우시안 잡음을 주입하는 순방향 과정(Forward Diffusion Process)과 신경망을 통해 잡음을 단계적으로 복원·제거하는 역방향 과정(Reverse Denoising Process)을 비평형 열역학 원리에 기반해 정립한 확산모델(Diffusion Model: DDPM, DDIM, Latent Diffusion Model: LDM, Stable Diffusion, Sora / Score-based Generative Models) 아키텍처를 도입하여 **모드 붕괴 없는 극도로 안정적인 우도(Likelihood) 기반 학습과 사실적인 초고화질 이미지/비디오/음성 합성 품질 달성, 텍스트/마스크 등 조건부 제어 신호(Classifier-Free Guidance) 주입을 통한 정밀한 타깃 생성 실현, 잠재 공간(Latent Space) 확산을 통한 연산 복잡도 최적화 및 상용 생성형 AI 생태계 구축**을 달성할 필요

#### 한줄 요약
- 무작위 잡음에서 **단계별 역방향 잡음 제거** 기반 표본 생성

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **순방향 확산(Forward Diffusion)**: 원본에 시점별 잡음을 섞어 학습 상태를 만든다.
- **역방향 잡음 제거(Reverse Denoising)**: 무작위 잡음에서 예측 잡음을 단계적으로 제거한다.

</details>

- 시점별 학습 상태를 생성하는 **순방향 확산**
- 반복 **역방향 잡음 제거**를 통한 새 표본 추출
- 역전이 단계 증가에 따른 **생성 품질 향상·지연 증가**

#### 한줄 요약
- **순방향 확산•역방향 제거•단계별 품질** 결합

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **잡음 스케줄(Noise Schedule)**: 시점별 신호와 잡음의 혼합 비율 규칙이다.
- **잡음 제거 모델(Denoiser)**: 제거할 잡음이나 이전 상태를 예측한다.
- **샘플러(Sampler)**: 역방향 상태 갱신으로 최종 표본을 만든다.

</details>

```text
[잡음 스케줄]──[시점별 잡음 상태]──[잡음 제거 모델]
                                      │
                              [역전이 규칙]──[샘플러]
```

| 구성요소 | 책임 |
|:---|:---|
| 잡음 스케줄 | 단계별 **신호•잡음 비율** 정의 |
| 시점별 잡음 상태 | 시점별 혼합된 **학습 입력** |
| 잡음 제거 모델 | **역방향 갱신값** 예측 신경망 |
| 역전이 규칙 | 모델 예측의 **평균**•**분산** 변환 |
| 샘플러 | 잡음에서 **표본 추출** 실행 |

#### 한줄 요약
- **잡음 스케줄•상태•제거 모델•역전이•샘플러** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **시점 조건(Timestep Condition)**: 제거 모델에 현재 확산 단계를 알려 주는 입력이다.
- **역전이(Reverse Transition)**: 현재 상태와 예측으로 이전 상태를 계산한다.

</details>

```text
잡음 스케줄
   │ 1. 순방향 잡음 상태 생성
   ▼
잡음 상태
   │ 2. 잡음 예측 학습
   ▼
잡음 제거 모델

┌──────────── 역전이 종료 시점까지 ────────────┐
│ 샘플러 ── 3. 현재 잡음 상태 입력 ──▶ 잡음 제거 모델
│ 샘플러 ◀─ 4. 역방향 상태 갱신 ─────┘
└──────────────────────────────────────────────┘
```

### 동작 원리

1. 순방향 잡음 상태 생성: 표본·잡음의 **스케줄 비율 혼합**
2. 잡음 예측 학습: 제거 모델의 **시점 조건부 잡음 예측**
3. 현재 잡음 상태 입력: 무작위 잡음의 **시점 상태 전달**
4. 역방향 상태 갱신: 이전 상태 반복 산출과 **새 표본 추출**

#### 한줄 요약
- **잡음 상태 생성•예측 학습•상태 입력•역방향 갱신** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **잡음 제거 확산 확률 모델(Denoising Diffusion Probabilistic Model, DDPM)**: 확률적 마르코프 역전이 방식이다.
- **잡음 제거 확산 암시 모델(Denoising Diffusion Implicit Model, DDIM)**: 결정론적 비마르코프 갱신 방식이다.

</details>

| 확산 샘플러 | DDPM | DDIM |
|:---|:---|:---|
| 적용 기준 | **표본 다양성** 확보 시 | **생성 속도** 우선 시 |
| 핵심 특징 | **확률적 마르코프 역전이** | **결정론적 비마르코프 갱신** |
| 한계 | 많은 단계의 **생성 지연** | 단계 축소 시 **품질 저하** |

#### 한줄 요약
- 확률성·다양성·생성 속도에 따른 **샘플러 구분**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **잡음 제거 오차 누적**: 단계 축소•예측 오차가 최종 표본에 쌓이는 문제이다.
- **조건 유도 강도(Guidance Scale)**: 조건 신호의 생성 영향력을 조절하는 값이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단계 축소와 잡음 제거 오차 누적 | 샘플러·단계별 **품질 회귀 시험** | 목표 지연의 **생성 품질 확보** |
| 강한 조건 유도와 다양성 감소 | 유도 강도별 **품질·다양성 평가** | 조건 충실성의 **표본 다양성** 유지 |

#### 한줄 요약
- **샘플러•단계 수•유도 강도•다양성** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **생성 지연(Generation Latency)**: 역전이와 모델 추론의 전체 응답 시간이다.
- **표본 다양성(Sample Diversity)**: 같은 조건에서 다른 유효 결과를 생성하는 정도이다.

</details>

- 기존 GAN과 VAE의 이론적/학습적 한계를 완전히 극복하고 텍스트-투-이미지, 비디오 생성, 음성 합성 및 3D 모델링의 글로벌 산업 표준으로 군림한 **현대 시각 생성형 AI의 최고 핵심 원천 모델(Diffusion Model / DDPM & Non-Markovian DDIM / Latent Diffusion Model: LDM / Classifier-Free Guidance: CFG / Consistency Models & Flow Matching / High-Fidelity Generative Backbone)의 확고한 표준**으로 확고히 자리 잡았으며, 초고속 1-step/Few-step 생성 모델(Flow Matching, SDXL-Turbo, Flux)로 혁신되는 가운데, 실무 Diffusion 기반 생성 파이프라인 구축 시에는 **추론 지연 시간과 표본 품질 간의 최적 절충을 위해 결정론적 고속 샘플러(DDIM, DPM-Solver, Euler)를 채택하고, 프롬프트 일치도를 극대화하는 Classifier-Free Guidance 스케일($s=7.0\sim 8.5$) 튜닝을 적용하며, 실시간 상용 서빙을 위한 Latent 공간 최적화 및 LoRA/ControlNet 조건부 제어 어댑터 연계**를 결합하여 완벽한 시각적 사실성과 상용 수준의 고속 생성 파이프라인을 완성

#### 한줄 요약
- 다양성 우선은 **DDPM**, 속도•재현성 우선은 **DDIM** 선택
