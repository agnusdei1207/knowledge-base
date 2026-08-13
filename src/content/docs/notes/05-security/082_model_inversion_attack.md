---
sidebar:
  order: 82
  label: "082. 모델 역전 공격 (Model Inversion Attack)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "모델 역전 공격 (Model Inversion Attack)"
date: "2026-08-13T20:46:00+09:00"
tags:
  - "notes-security"
weight: 82
extra:
  question_no: "082"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 70
  priority_note: "137•138회 반복된 모델 프라이버시 공격임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **모델 역전 공격(Model Inversion Attack)**: 학습된 머신러닝/딥러닝 모델의 출력 확률 벡터(Confidence Score)나 임베딩을 거꾸로 역추적하여, 학습에 사용된 개인의 안면 이미지, 유전자, 의료 기록 등 민감한 원본 데이터를 재구성 복원하는 프라이버시 침해 공격이다.
- **학습 정보 노출(Training Data Exposure)**: AI 모델이 학습 데이터셋에 포함된 특정 개인의 고유 특징을 과도하게 기억(Memorization)함에 따라 유출되는 프라이버시 침해 현상이다.

</details>

- 정의/개념: 모델 출력 신호로 학습 데이터 특징을
  복원하는 **모델 역전 공격**
- 배경/필요성: 과적합 모델의 API 출력으로 발생하는
  **학습 정보 노출**과 재식별 위험

#### 한줄 요약

- AI 모델의 출력 신뢰도나 기울기를 경사상승법으로 역추적하여 학습에 사용된 민감한 원본 데이터(얼굴, 의료 정보)를 재구성 복원하는 공격이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **신뢰도(Confidence Score / Probability Vector)**: 모델이 예측 분류 결과에 부과한 클래스별 0~1 사이의 정밀 확률값이다.
- **기울기(Gradient / Loss Gradient)**: 화이트박스 환경에서 입력 변화에 대한 손실 함수의 변화율로 역전 최적화의 핵심 나침반 역할을 한다.
- **사전 정보(Prior Knowledge / Auxiliary Information)**: 공격 대상 집단의 평균 얼굴 이미지, 성별 분포 등 공격자가 사전에 보유한 보조 데이터이다.
- **과적합(Overfitting)**: 모델이 일반화 성능 대신 학습 샘플의 개별 특징을 과도하게 암기한 상태이다.
- **DP(Differential Privacy)**: 노이즈 주입을 통해 데이터셋 내 특정 1개 샘플 포함 여부가 모델 출력에 미치는 영향을 노이즈로 가리는 차분 프라이버시 기술이다.

</details>

- 모델의 세부 **신뢰도** 수치 및 **기울기** 정보를 피드백 받아 최적화 알고리즘으로 복원 이미지를 다듬는다.
- 공격자의 **사전 정보**가 많고 모델의 **과적합** 수준이 높을수록 원본 데이터의 복원 유사도가 비례하여 상승한다.
- 방어를 위해 **DP(Differential Privacy)** 기술을 적용하여 학습 시 노이즈를 주입함으로써 개인 특성 복원을 원천 차단한다.

#### 한줄 요약

- 정밀 신뢰도/기울기 피드백 활용, 사전 정보 및 과적합에 비례한 복원 성능, Differential Privacy(DP) 기반 방어 특성을 가진다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **복원 최적화기(Reconstruction Optimizer)**: 경사상승법(Gradient Ascent) 또는 GAN(Generative Adversarial Network)을 활용해 모델의 득점을 최대화하는 방향으로 입력 픽셀/데이터를 반복 업데이트하는 엔진이다.
- **프라이버시 평가(Privacy Evaluation / Leakage Assessment)**: 복원된 이미지가 실제 특정 개인의 원본 데이터와 얼마나 유사한지 SSIM, PSNR, 안면 인식 정합률로 정량 측정하는 체계이다.

</details>

```text
[대상 모델]---[출력·내부 신호]---[사전 정보]
                       |                |
                 [복원 최적화기]---[프라이버시 평가]
```

선의 의미: 대상 모델의 출력 신호(Confidence) 및 내부 기울기와 사전 정보를 복원 최적화기에 투입하여 프라이버시 누출을 정량 평가하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 대상 모델 | 블랙박스/화이트박스 환경에서 질의에 대한 예측 결과 및 **신뢰도** 제공 |
| 출력·내부 신호 | 분류 확률 벡터(Softmax), 중간 임베딩, **기울기** 정보 수집 |
| 사전 정보 | 평균 얼굴 템플릿, 통계적 인구 데이터 등 최적화 초기값 제공 |
| 복원 최적화기 | **복원 최적화기**를 통한 픽셀/속성 단위 경사상승 최적화 반복 업데이트 |
| 프라이버시 평가 | **프라이버시 평가** 모듈로 SSIM/안면 인식 매칭을 통한 개인 식별성 판정 |

#### 한줄 요약

- 사전 정보 기반 초기화, 복원 최적화기(Gradient Ascent)를 통한 이미지 갱신, 프라이버시 평가 모듈의 식별성 판정 구조로 작동한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **반복 최적화(Iterative Optimization)**: 무작위 초기 노이즈 이미지에 모델의 신뢰도 피드백을 적용해 대상 클래스의 특징을 수천 회 갱신하는 과정이다.
- **유사성(Similarity Metric)**: 복원된 이미지와 실제 학습 대상 개인 원본 간의 구조적 유사도(SSIM) 수치이다.
- **식별성(Identifiability / Re-identifiability)**: 복원 산출물만으로 실제 특정 개인의 신원을 특정할 수 있는 정합 확률 수준이다.
- **복원 후보 생성(Reconstruction Candidate Generation)**: 사전 정보를 바탕으로 초기 탐색 입력 객체를 구성하는 단계이다.
- **후보 최적화(Candidate Optimization)**: 모델에 질의하고 도출된 신뢰도 득점이 최대가 되도록 입력값을 역전 업데이트하는 단계이다.
- **유사성•식별성 판정(Similarity & Identifiability Determination)**: 재구성 결과물이 개인식별 수준에 도달했는지 평가 수렴을 판정하는 단계이다.

</details>

```text
목표·사전 정보
       |
       v
1. 복원 후보 생성
       |
       v
대상 모델 질의 ──> 출력 신호
       ^                 |
       |                 v
       +──── 2. 후보 최적화
              | 미수렴: 반복
              | 수렴
              v
3. 유사성·식별성 판정
              |
              v
       프라이버시 위험
```

### 동작 원리

1. **복원 후보 생성**: 사전 정보 기반 초기 노이즈 구성
2. **후보 최적화**: 출력 신호 기반 **반복 최적화**
3. **유사성·식별성 판정**: 복원물의 재식별 위험 평가

#### 한줄 요약

- 초기 후보 생성, 모델 질의 피드백 기반 경사상승 반복 최적화, 유사성 및 식별성 정밀 평가 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **회원 추론(Membership Inference Attack, MIA)**: 특정 데이터 샘플이 모델의 학습 데이터셋에 포함되었는지 여부(In or Out)만 판정하는 공격이다.
- **모델 추출(Model Extraction Attack)**: 대량의 입력-출력 쌍을 수집해 대상 AI 모델의 가중치 및 판단 경계를 복제(Stolen Model)하는 공격이다.

</details>

| AI 프라이버시/자산 공격 | 모델 역전 (Model Inversion) | 회원 추론 (Membership Inference) | 모델 추출 (Model Extraction) |
|:---|:---|:---|:---|
| 공격의 핵심 목적 | 학습에 쓰인 원본 민감 데이터(얼굴/의료) **재구성 복원** | 특정 개인 데이터의 학습 데이터셋 **포함 여부 확인** | 대상 AI 모델의 지적재산권(IP) 및 판단 경계 **복제** |
| 공격 결과물 | 원본과 유사한 이미지/속성 재구성 산출물 | Binary 판단 (학습 포함 1 / 미포함 0) | 동일한 성능을 내는 복제 딥러닝 모델 (Surrogate Model) |
| 핵심 대응 기술 | **DP(Differential Privacy)**, **점수 양자화** | DP-SGD 학습, Regularization, 과적합 억제 | API Rate Limiting, **질의 예산** 제한, 노이즈 반환 |

#### 한줄 요약

- 모델 역전은 원본 데이터 복원, 회원 추론은 포함 여부 확인, 모델 추출은 알고리즘 복제에 집중하는 차별점이 존재한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NIST(National Institute of Standards and Technology)**: AI 프라이버시 및 보안 가이드라인 표준화 기관이다.
- **AI 100-2e2025 (NIST AI 100-2e2025 Privacy in AI)**: AI 모델의 프라이버시 침해 위험(역전, 회원추론) 및 차분 프라이버시 방안을 제시하는 NIST 지침이다.
- **출력 최소화(Output Minimization)**: Top-1 클래스 라벨만 반환하고 정밀 확률 벡터(Softmax)를 은닉하는 통제 기법이다.
- **질의 예산(Query Budget / Rate Limiting)**: 동일 계정/IP의 과도한 반복 질의를 제한하여 최적화 탐색을 차단하는 기술이다.
- **점수 양자화(Score Quantization / Confidence Rounding)**: 소수점 이하 정밀 확률값을 소수점 1자리로 올림/버림하여 역전 신호를 교란하는 기술이다.
- **블랙박스 접근(Black-box Access)**: API 입력/출력 텍스트만 관찰 가능한 공격 조건 환경이다.
- **화이트박스 접근(White-box Access)**: 모델 가중치, 레이어 내부, 기울기(Gradient)에 직접 접근 가능한 환경이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 프라이버시 위협 표준 지침 부재 | **NIST AI 100-2e2025** 규격 적용 | 모델 프라이버시 침해 체계적 정량 평가 정착 |
| 정밀 확률 벡터를 통한 역전 최적화 | **출력 최소화** 및 **점수 양자화** (Rounding) 적용 | 경사상승 최적화 알고리즘 신호 무력화 |
| 모델 과적합에 따른 개인 기억 유출 | DP-SGD (Differential Privacy) 학습 | 학습 데이터 1개 노드 유출 영향력 물리적 통제 |
| 대량 질의를 통한 최적화 탐색 | **질의 예산** (Query Budget) 및 Rate Limiting | **블랙박스 접근** 기반 역전 공격의 시도 횟수 제한 |

#### 한줄 요약

- NIST AI 100-2e2025 준용, Differential Privacy(DP-SGD) 학습, 출력 최소화 및 점수 양자화를 바탕으로 역전 공격을 방어한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **프라이버시-유용성 균형(Privacy-Utility Tradeoff)**: DP 노이즈 주입 시 모델 추론 정확도(Utility) 하락과 프라이버시 보호(Privacy) 간의 최적 임계점 설정이다.

</details>

- 민감 모델은 **DP-SGD**, 공개 API는 **출력 최소화** 적용

#### 한줄 요약

- NIST AI 표준 준수, DP-SGD 노이즈 학습, Softmax 확률 은닉(출력 최소화) 및 질의 예산 제어 중심 모델 역전 공격 방어 체계 구축 필수.
