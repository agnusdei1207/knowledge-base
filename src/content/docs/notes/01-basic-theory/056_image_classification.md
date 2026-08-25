---
sidebar:
  order: 56
  label: "056. 이미지 분류: ResNet·VGG·EfficientNet (Image Classification)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "이미지 분류: ResNet·VGG·EfficientNet (Image Classification)"
date: "2026-08-25T10:00:00+09:00"
tags:
  - "notes-basic-theory"
weight: 56
extra:
  question_no: "056"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "잔차 연결과 복합 스케일링"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **이미지 분류(Image Classification)**: 입력 이미지 전체의 시각적 특징을 분석하여 사전 정의된 클래스 레이블 중 하나를 할당하는 지도학습 과업.
- **수용 영역(Receptive Field)**: 출력층의 특정 뉴런이 입력 이미지에서 감지할 수 있는 공간적 영역의 크기.
- **기울기 소실(Vanishing Gradient)**: 신경망의 깊이가 깊어질수록 역전파되는 오차 기울기가 0에 수렴하여 앞단 가중치 학습이 멈추는 현상.

</details>

- 정의/개념: 입력 이미지의 공간적 특징을 합성곱 계층으로 추출하여 **이미지 전체가 속하는 대표 범주(Category)를 판별**하는 딥러닝 비전 기본 모델
- 배경/필요성: 신경망 계층 심화 시 **기울기 소실 및 파라미터 폭증에 따른 연산 비효율 발생**

#### 한줄 요약

- 계층적 합성곱 신경망을 통해 이미지의 공간 특징을 추출하고 전체 클래스를 판별하는 모델

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **잔차 연결(Residual Connection, Skip Connection)**: 입력 $x$를 계층의 출력 $F(x)$에 직접 더해 $H(x) = F(x) + x$를 학습하도록 우회 경로를 제공하는 기법.
- **복합 스케일링(Compound Scaling)**: 신경망의 깊이(Depth), 너비(Width), 해상도(Resolution)를 일정한 고정 비율로 균형 있게 동시 확장하는 기법.

</details>

- VGG: **$3 \times 3$ 소형 필터 반복** 기반 파라미터 절감 및 수용 영역(Receptive Field) 확장
- ResNet: **잔차 연결(Residual Connection)** 기반 초심층(100+ 계층) 신경망의 기울기 소실 해결
- EfficientNet: 깊이·너비·해상도 **복합 스케일링(Compound Scaling)** 기반 연산량 대비 최고 정확도 달성

#### 한줄 요약

- VGG의 소형 필터 중첩, ResNet의 잔차 연결, EfficientNet의 복합 스케일링으로 발전

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **글로벌 평균 풀링(Global Average Pooling, GAP)**: 마지막 합성곱 특징 맵의 각 채널별 평균값을 취해 1차원 벡터로 변환하는 기법으로 완전 연결 계층의 파라미터 폭증을 대체.
- **MBConv**: 깊이별 분리 합성곱과 Squeeze-and-Excitation(SE) 블록을 결합한 EfficientNet의 기본 모듈.

</details>

```text
[ VGG: 직렬 계층 적층 ]
입력 ──► [ Conv 3x3 ] ──► [ Conv 3x3 ] ──► [ MaxPool ] ──► [ FC Layers ] ──► Softmax

[ ResNet: 잔차 블록 (Skip Connection) ]
입력 (x) ──┬──► [ Conv 3x3 ] ──► [ ReLU ] ──► [ Conv 3x3 ] ──► ( + ) ──► [ ReLU ] ──► 출력
           └────────────────── (Skip Connection: x) ──────────┘

[ EfficientNet: 복합 스케일링 블록 (MBConv) ]
입력 ──► [ 1x1 Conv 확장 ] ──► [ 3x3 Depthwise Conv ] ──► [ SE 채널 주의 ] ──► [ 1x1 Conv 투영 ] ──► 출력
```

선의 의미: 아키텍처별 특징 추출 블록 및 잔차 우회 경로의 연결 구조

| 구성요소 | 책임 |
|:---|:---|
| 소형 합성곱 블록(VGG) | $3 \times 3$ 필터 중첩으로 **비선형 활성화 및 수용 영역 확장** |
| 잔차 블록(ResNet) | Identity Mapping($F(x)+x$)을 통해 **기울기 무손실 전달 보장** |
| MBConv 블록(EfficientNet) | 깊이별 분리 합성곱과 채널 어텐션으로 **연산 효율 극대화** |
| 글로벌 평균 풀링(GAP) | 공간 차원 축소를 통해 **완전 연결 계층 파라미터 폭증 억제** |

#### 한줄 요약

- 직렬 합성곱 적층에서 잔차 연결 블록을 거쳐 경량 MBConv 복합 스케일링 구조로 진화

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **소프트맥스(Softmax)**: 모델의 최종 로짓(Logit) 출력 벡터를 전체 합이 1인 확률 분포로 정규화하는 활성화 함수.

</details>

```text
입력 이미지 (H x W x C)
         │
         ▼
[ 1. 초기 합성곱 및 다운샘플링 ]
         │
         ▼
[ 2. 다단계 잔차 및 MBConv 계층 통과 ]
         │
         ▼
[ 3. 글로벌 평균 풀링 적용 ]
         │
         ▼
[ 4. 소프트맥스 정규화 ]
         │
         ▼
[ 5. 최고 확률 대표 클래스 출력 ]
```

**동작 원리**

1. **초기 합성곱 및 다운샘플링**: 저수준 엣지 및 기본 시각 특징을 고해상도에서 추출
2. **다단계 잔차 및 MBConv 계층 통과**: 해상도를 줄이고 채널을 늘리며 추상화된 의미 특징 학습
3. **글로벌 평균 풀링 적용**: 위치 정보를 요약하고 1차원 특징 벡터로 변환
4. **소프트맥스 정규화**: 최종 분류 로짓을 0~1 사이의 확률값으로 변환
5. **최고 확률 대표 클래스 출력**: 가장 높은 확률을 가진 클래스 레이블을 최종 예측값으로 확정

#### 한줄 요약

- 저수준 엣지부터 고수준 의미 특징까지 계층 추출하고 GAP와 소프트맥스를 거쳐 클래스 확정

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **VGGNet**: $3 \times 3$ 소형 합성곱 필터를 균일하게 직렬 적층한 직관적 합성곱 모델.
- **ResNet**: Skip Connection 잔차 연결로 기울기 소실을 해결하여 초심층 구조를 실현한 표준 모델.
- **EfficientNet**: 깊이, 너비, 해상도를 복합 스케일링하여 최고 연산 효율을 달성한 경량 비전 모델.

</details>

| 이미지 분류 아키텍처 | VGGNet | ResNet | EfficientNet |
|:---|:---|:---|:---|
| 적용 기준 | **구조 단순성** 및 직관적 특징 추출 요구 시 | **초심층 신경망 구성** 및 범용 백본 네트워크 필요 시 | **자원 제약 환경(모바일/엣지)** 및 최고 연산 효율 시 |
| 핵심 특징 | **$3 \times 3$ 필터 균일 적층** 및 단순한 직렬 구조 | **Skip Connection 잔차 학습** 기반 기울기 소실 해결 | **깊이·너비·해상도 복합 스케일링** 및 MBConv |
| 한계 | 거대한 파라미터 수 및 **메모리 연산 비효율** | 계층 증가에 따른 **추론 지연 시간 증가** | 구조 탐색(NAS) 기반으로 **구현 및 튜닝 복잡** |

#### 한줄 요약

- 직관적 구조는 VGGNet, 범용 백본은 ResNet, 최고 효율 경량화는 EfficientNet을 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **깊이별 분리 합성곱(Depthwise Separable Convolution)**: 공간 방향 합성곱과 채널 방향 합성곱을 분리하여 연산량을 1/8 수준으로 절감하는 기법.
- **Mixup / CutMix**: 두 이미지와 라벨을 선형 보간하거나 영역을 잘라 붙여 데이터 다양성을 증대시키는 정규화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 데이터셋 부족 시 심층 CNN의 **과적합 및 일반화 실패** | **ImageNet 사전학습 가중치 전이 학습 및 CutMix 증강** | 적은 데이터로도 높은 분류 정확도 달성 |
| 엣지/모바일 배포 시 **연산량 및 메모리 제약** | **깊이별 분리 합성곱 적용 및 INT8 양자화(Quantization)** | 모델 용량 75% 절감 및 추론 속도 가속 |
| 배포 환경 조명·각도 변화에 따른 **도메인 시프트(Domain Shift)** | **테스트 타임 증강(TTA) 및 도메인 적응 기법 적용** | 실제 현장 운영 환경에서의 강건성 확보 |

#### 한줄 요약

- 데이터 부족은 전이 학습으로, 엣지 자원 제약은 양자화로, 도메인 시프트는 TTA로 대응

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **표준 백본(Standard Backbone)**: 객체 탐지, 세분화 등 다양한 하위 비전 과업의 공통 특징 추출기로 활용되는 기반 신경망.

</details>

- 범용 비전 백본은 **ResNet**, 자원 제약 온디바이스는 **EfficientNet** 선택

#### 한줄 요약

- 일반 서버 환경은 ResNet을 기본으로 하고, 엣지 환경은 EfficientNet으로 전환

## 2~4교시 확장

**예상 문항**
> 딥러닝 기반 이미지 분류 모델에서 신경망의 깊이 심화에 따른 기울기 소실 문제 해결 방안과 연산 효율성을 극대화하기 위한 아키텍처 설계 전략을 논하시오. (25점)

**목차 조립**: `Ⅰ → Ⅱ → Ⅲ → Ⅵ → Ⅶ`
