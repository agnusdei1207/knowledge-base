---
title: "이미지 분류 — ResNet·VGG·EfficientNet (Image Classification) [출제: 120회]"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 71
---

# 071. 이미지 분류 — ResNet·VGG·EfficientNet (Image Classification) [출제: 120회]

## 1. 개요

- **정의/개념**: 입력된 디지털 이미지 전체를 미리 정의된 하나 이상의 범주(Category) 중 가장 적합한 클래스로 할당하는 컴퓨터 비전의 가장 기초적이고 핵심적인 지도 학습 과제임
- **배경/필요성**: 대량의 시각 데이터를 사람이 일일이 분류하는 비용을 절감하고, 육안으로 식별하기 어려운 미세한 차이를 정밀하게 판별하여 제조, 의료, 보안 등 다양한 산업 분야의 자동화를 실현하기 위해 필요함

## 2. 특징 및 비교

| 판단 기준 | VGGNet (Simonyan, 2014) | ResNet (He, 2015) | EfficientNet (Tan, 2019) |
|:---|:---|:---|:---|
| **핵심 구조** | 3x3 작은 필터의 깊은 적층 | 잔차 학습 (Skip Connection) | 복합 스케일링 (Width, Depth, Res) |
| **주요 특징** | 단순하고 직관적인 구조 | 기울기 소실 해결, 초심층 가능 | 파라미터 대비 성능 최적화 |
| **연산 효율** | 낮음 (파라미터 과다) | 보통 | 매우 높음 |
| **주요 공헌** | 필터 크기보다 깊이의 중요성 증명 | 150층 이상의 깊은 망 학습 성공 | 모델 크기 조절의 정량적 규칙 제안 |

> 요약: VGG는 단순함을, ResNet은 깊이를, EfficientNet은 효율성을 대표하는 이미지 분류 아키텍처임

## 3. 구성요소/구조

- **구성요소**:
  - **Feature Extractor (Backbone)**: 합성곱 층(Conv Layer)을 통해 이미지의 저수준(선, 면)부터 고수준(형태) 특징을 단계적으로 추출함
  - **Skip Connection (ResNet)**: 입력 $x$를 출력에 직접 더해주는($F(x)+x$) 경로를 통해 층이 깊어져도 기울기가 잘 전달되게 함
  - **Global Average Pooling (GAP)**: 특징 맵의 채널별 평균을 구해 파라미터 수를 줄이고 과적합을 방지하며 FC 레이어로 전달함
  - **Softmax Classifier**: 추출된 특징 벡터를 바탕으로 각 클래스에 속할 확률을 계산하여 최종 라벨을 결정함

- **이미지 분류 파이프라인**:
```text
[Input Image] -> [Data Augmentation] -> [Backbone Network] -> [Pooling/FC] -> [Softmax] -> [Class Label]
     |                 |                     |                 |             |              |
 (224x224x3)     (Rotation/Flip)      (Feature Map)     (Feature Vector)   (Prob)        "Dog(0.98)"
```

## 4. 문제점 및 개선방안

1. **[데이터 편향 및 불균형]**: 특정 클래스의 데이터가 압도적으로 많을 경우 모델이 다수 클래스에 편향되어 학습됨
   - **개선방안**: 오버샘플링, Class Weight 조정, 또는 Focal Loss와 같은 불균형 데이터 특화 손실 함수를 적용함 (확인: F1-Score)
2. **[모델의 거대화와 추론 지연]**: 정확도를 높이기 위해 모델이 무거워지면 실시간 서비스나 모바일 기기 적용이 어려움
   - **개선방안**: 모델 압축(Pruning), 지식 증류(Distillation), 또는 MobileNet/EfficientNet-Lite와 같은 경량화 모델을 채택함 (확인: Inference Latency)
3. **[블랙박스 특성(해석 불가)]**: 모델이 이미지의 어느 부분을 보고 분류했는지 알 수 없어 신뢰성 문제가 발생함
   - **개선방안**: Grad-CAM과 같은 시각화 기법을 사용하여 모델의 판단 근거(Heatmap)를 확인하고 검증함 (확인: 설명 가능성(XAI))

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **제조 외관 검사** | 제품 표면 이미지를 분류하여 정상/불량(스크래치, 이물 등) 자동 판정 | Recall (미검률 관리), Precision |
| **의료 영상 진단** | 흉부 X-ray나 조직 슬라이드 이미지를 분류하여 질병 유무 1차 스크리닝 | AUC-ROC, 민감도/특이도 |
| **콘텐츠 필터링** | SNS나 커뮤니티에 업로드되는 이미지 중 유해 콘텐츠(음란, 폭력) 자동 차단 | Accuracy, F1-Score |

> 요약: 실무에서는 사전 학습된 모델(ResNet 등)을 가져와 자신의 데이터로 미세 조정(Fine-tuning)하는 방식이 표준임

## 6. 결론

이미지 분류 기술은 딥러닝 혁명의 시작점이자 현재 컴퓨터 비전의 근간을 이루는 필수 기술임. VGG에서 EfficientNet에 이르기까지 모델은 더욱 깊고 효율적으로 진화해 왔으며, 최근에는 CNN을 넘어 Transformer 기반의 ViT(Vision Transformer)가 더 높은 성능을 보여주고 있음. 향후에는 적은 데이터로도 학습이 가능한 퓨샷 학습(Few-shot Learning)과 모델의 판단 근거를 명확히 하는 설명 가능한 AI 기술이 실무 적용의 핵심이 될 것임.
