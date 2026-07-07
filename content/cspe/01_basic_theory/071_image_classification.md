---
title: "이미지 분류 — ResNet·VGG·EfficientNet (Image Classification)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 71
---

# 이미지 분류 - ResNet·VGG·EfficientNet (Image Classification)

## 1. 개요

- **정의/개념**: 이미지 분류는 입력 이미지 전체를 하나 이상의 클래스 라벨로 매핑하는 컴퓨터 비전 과제이다.
- **배경/필요성**: 대량 이미지의 자동 판정, 품질 검사, 의료 보조 진단처럼 시각 정보를 빠르게 분류해야 하는 업무에서 모델 기반 판별이 필요하다.

이미지 분류는 위치를 찾는 탐지와 달리 이미지 전체의 대표 클래스를 예측하는 문제이다.

## 2. 특징 및 비교

| 구분 | VGG | ResNet | EfficientNet |
|---|---|---|---|
| 구조 | 단순한 깊은 CNN | residual connection | compound scaling |
| 강점 | 구조 이해 쉬움 | 깊은 모델 학습 안정 | 성능·효율 균형 |
| 약점 | 파라미터 많음 | 구조 복잡도 증가 | scaling 설계 의존 |
| 선택 기준 | baseline | 고성능 backbone | 자원 효율 |

선택 기준은 정확도, 파라미터 수, 추론 지연, 학습 데이터 규모, edge 배포 여부이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Input Image | 분류할 이미지 | 전처리 필요 |
| Feature Extractor | Conv block 또는 backbone | 시각 특징 추출 |
| Pooling | 공간 정보를 요약 | 차원 축소 |
| Classifier | class score 계산 | softmax |
| Loss | 정답과 예측 비교 | cross-entropy |

```text
Image -> Preprocess -> Backbone -> Pooling -> Classifier -> Class
```

전처리와 backbone 선택이 feature 품질을 좌우하고, classifier는 이를 class 확률로 변환한다.

## 4. 문제점 및 개선방안

1. **데이터 편향**
   - 학습 이미지의 배경·조명·클래스 분포가 실제와 다르면 성능이 떨어진다.
   - **개선방안**: 데이터 증강, class balancing, domain validation을 수행한다.

2. **과적합**
   - 데이터가 적고 모델이 크면 train 성능만 높아질 수 있다.
   - **개선방안**: transfer learning, regularization, early stopping을 적용한다.

3. **설명성 부족**
   - 모델이 어떤 영역을 보고 판단했는지 알기 어렵다.
   - **개선방안**: Grad-CAM, saliency map, 오류 샘플 분석을 활용한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 제조 검사 | 정상/불량 이미지 분류 | recall, false alarm |
| 의료 영상 | 질환 의심 여부 분류 보조 | 민감도, 특이도 |
| 콘텐츠 관리 | 이미지 카테고리 자동 태깅 | top-k accuracy |

## 6. 결론

이미지 분류는 시각 데이터를 클래스 라벨로 변환하는 기본 비전 과제이다. Conv-Pool-Classifier 구조와 ResNet·EfficientNet 같은 backbone 선택 기준을 함께 설명해야 정확도와 배포 효율을 동시에 판단할 수 있다.
