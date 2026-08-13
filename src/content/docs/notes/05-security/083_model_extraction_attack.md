---
sidebar:
  order: 83
  label: "083. 모델 추출 공격 (Model Extraction Attack)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "모델 추출 공격 (Model Extraction Attack)"
date: "2026-08-13T20:48:00+09:00"
tags:
  - "notes-security"
weight: 83
extra:
  question_no: "083"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 70
  priority_note: "137•138회 반복된 모델 지식재산 공격임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **API(Application Programming Interface)**: 클라이언트 및 애플리케이션이 AI 모델과 추론 데이터를 주고받는 상호작용 엔드포인트이다.
- **모델 추출 공격(Model Extraction Attack / Model Stealing)**: 대상 모델(Target Model)의 API를 대량으로 질의하고 반환되는 라벨, 확률(Softmax), 임베딩을 이용해 동일한 기능과 성능을 가진 대리 모델(Surrogate Model)을 훔쳐 복제하는 IP 탈취 공격이다.
- **대상 모델(Target Model / Teacher Model)**: 공격자가 지적재산권(IP) 및 기능 판단 경계를 훔치려는 원본 상용 AI 모델이다.
- **대리 모델(Surrogate Model / Student Model)**: 대상 모델의 질의 응답 데이터셋을 증강 학습시켜 원본의 판단 경계를 99% 이상 복제한 불법 스톨론(Stolen) AI 모델이다.

</details>

- 정의/개념: API 응답으로 원본 모델의 **결정 경계**를
  복제하는 **모델 추출 공격**
- 배경/필요성: 공개 API의 상세 출력과 대량 질의로
  발생하는 **모델 IP** 탈취 위험

#### 한줄 요약

- 상용 API를 대량 질의하여 수집한 데이터로 원본 AI 모델의 판단 경계와 지적재산권(IP)을 동일하게 모방 복제하는 공격이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **결정 경계(Decision Boundary)**: 고차원 특징 공간에서 모델이 클래스를 분류하는 수학적 분류 경계면이다.
- **능동 질의(Active Query / Active Learning Query)**: 무작위 질의 대신 결정 경계 근처의 불확실성이 높은 샘플만 선별 질의하여 추출 효율을 극대화하는 수법이다.
- **워터마크(Model Watermarking / Backdoor Watermark)**: 모델 학습 시 무해한 특정 트리거 패턴에 식별 반응을 출력하도록 암호학적 소유권 핑거프린트를 삽입하는 기술이다.
- **행위 분석(Behavioral Analytics / Anomaly Detection)**: API 요청자의 IP, 계정, 질의 텍스트의 엔트로피 분포를 모니터링하여 자동화 추출 봇을 탐지하는 기법이다.

</details>

- 결정 경계 주변에 **능동 질의**를 집중시켜 최적의 데이터 효율(Query Efficiency)로 대리 모델을 동기화한다.
- 라벨만 반환하는 Hard-label보다 정밀 확률이나 임베딩을 주는 Soft-label 환경에서 복제 속도가 비약적으로 상승한다.
- **행위 분석** 모니터링과 **워터마크** 핑거프린팅을 통해 복제 모델의 출처를 법적으로 증명 및 귀속(Attribution)한다.

#### 한줄 요약

- 결정 경계 능동 질의, Soft-label 피드백 기반 고속 복제 및 워터마크/행위 분석을 통한 법적 귀속 관제 특성을 지닌다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **질의 생성기(Query Generator / Synthetic Query Synthesizer)**: GAN, Diffusion, OOD 샘플링 기법을 활용해 대상 모델의 결정 경계를 자극하는 합성 데이터를 자동 생성하는 모듈이다.
- **대리 학습기(Surrogate Model Trainer)**: 대상 모델 API로부터 수집된 (입력, 출력) 페어 데이터셋을 바탕으로 학생 모델을 지도 학습시키는 엔진이다.
- **충실도(Fidelity / Agreement Rate)**: 대리 모델이 동일한 입력에 대해 원본 대상 모델과 얼마나 동일하게 분류 판단하는지의 일치 비율(%) 지표이다.

</details>

```text
모델 추출 경계
├─ 서비스 측
│  ├─ 대상 모델 API
│  └─ 질의·응답 경계
├─ 공격 측
│  ├─ 질의 생성기
│  └─ 대리 모델 학습기
└─ 방어 측
   └─ 남용 탐지·귀속
```

선의 의미: 서비스 측 대상 모델 API 경계에 공격자의 질의 생성기 및 대리 모델 학습기와 방어자의 남용 탐지/귀속 모듈이 대립하는 아키텍처이다.

| 구성요소 | 책임 |
|:---|:---|
| 대상 모델 API | **대상 모델**의 추론 결과를 REST API/gRPC 형태로 제공하는 엔드포인트 |
| 질의·응답 경계 | Rate Limiting, **출력 최소화**, API 인증을 집행하는 프록시 보안 레이어 |
| 질의 생성기 | **질의 생성기**를 통한 능동 학습 기반 불확실성 경계 매핑 입력 합성 |
| 대리 학습기 | **대리 학습기**를 통해 수집된 라벨/확률값을 자원으로 **충실도** 높은 대리 모델 구조 복제 |
| 남용 탐지·귀속 | **행위 분석** 엔진의 봇 스캐닝 탐지 및 **워터마크** 검증으로 법적 소유권 입증 |

#### 한줄 요약

- 질의 생성기의 경계 타격, 대리 학습기의 충실도 최적화 및 방어 측의 남용 탐지/워터마크 귀속 모듈로 대립 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **불일치 경계 탐색(Disagreement Boundary Search)**: 대리 모델과 대상 모델 간 예측 결과가 상충하는 고위험 영역의 질의를 집중 생성하여 복제 오차를 교정하는 방식이다.
- **카나리 입력(Canary Inputs / Trapdoor Data)**: 공격자가 모델을 추출하여 상용화할 때 원본 소유자의 데이터가 포함되었음을 증명하기 위해 삽입한 특수 함정 데이터이다.
- **정보량 높은 질의 합성(High-Information Query Synthesis)**: 모델 판단 경계 식별에 필요한 정보량이 최대화되도록 능동 합성 입력을 만드는 단계이다.
- **대리 모델 학습•경계 탐색(Surrogate Training & Boundary Search)**: 응답 페어를 가공해 대리 모델을 기계 학습시키고 불일치 경계를 좁혀가는 단계이다.
- **반복 패턴 탐지(Repetitive Pattern Detection)**: 단시간 내 발생하는 합성 입력 질의 봇의 이상 패턴을 모니터링하는 단계이다.
- **워터마크•카나리 귀속(Watermark & Canary Attribution)**: 의심스러운 유출 모델에 카나리 데이터를 주입하여 원본 무단 복제 여부를 입증하는 단계이다.

</details>

```text
경계 탐색 목표
       |
       v
1. 정보량 높은 질의 합성
       |
       v
대상 모델 질의 ──> 모델 응답
       ^                 |
       |                 v
       +── 2. 대리 모델 학습·경계 탐색
              | 불일치: 반복
              | 경계 근사 완료
              v
3. 반복 패턴 탐지
              |
              v
4. 워터마크·카나리 귀속
              |
              v
           남용 판정
```

### 동작 원리

1. **정보량 높은 질의 합성**: 결정 경계 후보 입력 생성
2. **대리 모델 학습·경계 탐색**: 응답 학습과 불일치 축소
3. **반복 패턴 탐지**: 질의 분포·예산 이상 탐지
4. **워터마크·카나리 귀속**: 고유 반응으로 소유권 입증

#### 한줄 요약

- 정보량 높은 질의 합성, 대리 모델 불일치 경계 탐색, 탐지 엔진의 패턴 모니터링 및 카나리/워터마크 법적 귀속 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **라벨 기반 추출(Label-only Extraction Attack)**: Top-1 클래스 라벨만 제공받는 조건에서 0/1 바이너리 질의를 대량 투입하여 복제하는 방식이다.
- **점수 기반 추출(Score-based / Soft-label Extraction Attack)**: 클래스별 정밀 확률 벡터(Softmax)를 수집하여 손실 함수(KLDiv 등)를 직접 줄여 복제하는 방식이다.
- **상세 출력 기반 추출(Rich Output / Embedding Extraction Attack)**: LLM 토큰 확률, 백엔드 임베딩 벡터, 설명 가능성(XAI) 맵까지 수집하여 모델 내부 표현을 통째로 복제하는 방식이다.

</details>

| 추출 공격 방식 | 라벨 기반 추출 (Label-only) | 점수 기반 추출 (Score-based) | 상세 출력 기반 추출 (Rich Output) |
|:---|:---|:---|:---|
| 반환 정보 형태 | Top-1 클래스 이름 (예: "Cat") | 각 클래스별 0~1 정밀 확률 벡터 (Softmax) | 임베딩 벡터, Logits, XAI Feature Map |
| 요구 질의 수 | 매우 많음 ($10^6$ 이상) | 보통 ($10^4 \sim 10^5$) | 매우 적음 ($10^3$ 수준으로 고속 복제) |
| 복제 모델 충실도 | 보통 (경계 추정에 오랜 시간 소요) | 높음 (Soft-label 손실 함수 축소) | 최고 (내부 세부 임베딩 표상까지 모방) |
| 대표 대응 기술 | Hard-label 유지, **질의 예산** 제한 | **점수 양자화** (Confidence Rounding) | **출력 최소화**, 임베딩 접근 인가 강제 |

#### 한줄 요약

- 라벨 기반, 점수 기반(Soft-label), 상세 출력 기반(Embedding)으로 세분화되며 반환 정보가 정밀할수록 복제 속도가 상승한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **AI 100-2e2025 (NIST AI 100-2e2025 Privacy in AI)**: AI 모델의 IP 추출, 프라이버시 침해, 차분 보안 통제를 다룬 NIST 규격이다.
- **호출률 제한(Rate Limiting / Query Budgeting)**: 사용자/IP별 단위 시간당 질의 횟수 및 일일 예산을 엄격히 통제하는 기술이다.
- **분포 분석(Out-of-Distribution Detection)**: 사용자의 질의 텍스트가 자연스러운 분포를 벗어나 무작위 합성 데이터(OOD)인지 파악하는 탐지 기법이다.
- **출력 최소화(Output Minimization)**: API 응답 시 불필요한 확률 벡터, Logits, 임베딩을 제거하고 가공된 최종 텍스트만 제공하는 보안 통제이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 모델 IP 추출 위협 통제 미비 | **NIST AI 100-2e2025** 규격 적용 | 모델 추출 및 프라이버시 침해 위험 체계적 평가 정착 |
| 능동 학습 합성 입력의 대량 질의 | **호출률 제한** 및 OOD **분포 분석** 탐지 | 능동 학습 기반 자동화 추출 봇의 질의 시도 원천 차단 |
| 복제 모델에 대한 무단 사용 입증 불가 | 모델 가중치 내 **워터마크** 및 **카나리 입력** 주입 | 탈취된 스톨론(Stolen) 모델의 법적 소유권 및 무단 복제 증명 |

#### 한줄 요약

- NIST AI 100-2e2025 준용, 호출률 제한, OOD 분포 분석, 워터마크/카나리 기법을 연계해 모델 IP를 방어한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **복제 비용(Reconstruction / Stealing Cost)**: 공격자가 대리 모델을 완성하기 위해 지출해야 하는 API 비용 및 시간을 의미한다.
- **귀속(Attribution / Ownership Proof)**: 복제된 모델에 대해 법적 소유권 및 원본 무단 도용 여부를 기술적으로 증명해내는 능력이다.

</details>

- 공개 API는 **출력 최소화**, 유출 모델은 **워터마크** 검증

#### 한줄 요약

- NIST AI 지침 준수, API 출력 최소화, Rate Limiting, OOD 행위 분석 및 워터마크 카나리 귀속 중심 모델 추출 방어 체계 구축 필수.
