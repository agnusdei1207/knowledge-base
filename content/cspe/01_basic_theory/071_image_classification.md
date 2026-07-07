---
title: "이미지 분류 — ResNet·VGG·EfficientNet (Image Classification) [출제: 120회]"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 71
---

# 071. 이미지 분류 — ResNet·VGG·EfficientNet (Image Classification) [출제: 120회]

## Ⅰ. 개요

- **정의/개념**: 입력된 디지털 이미지 전체를 미리 정의된 하나 이상의 범주($Category$) 중 가장 적합한 클래스로 할당하는 컴퓨터 비전의 핵심 지도 학습($Supervised$ $Learning$) 과제임
- **배경/필요성**: 비정형 시각 데이터의 특징 추출($Feature$ $Extraction$)을 자동화하여 사람의 개입 없이 대규모 분류를 수행함. 자율주행의 표지판 인식, 의료 영상의 질병 유무 판독, 제조 공정의 불량 검수 등 산업 전반의 지능형 자동화를 위한 기저 기술임

## Ⅱ. 특징 및 비교

### 1. 세대별 이미지 분류 아키텍처 비교

| 판단 기준 | $VGGNet$ ($2014$) | $ResNet$ ($2015$) | $EfficientNet$ ($2019$) |
|:---|:---|:---|:---|
| **핵심 기여** | $3 \times 3$ 필터 적층의 깊이 증명 | 잔차 학습 ($Residual$ $Learning$) | 복합 스케일링 ($Compound$ $Scaling$) |
| **기울기 소실 대응** | 취약 (층이 깊어지면 정체) | 우수 ($Skip$ $Connection$ 도입) | 매우 우수 (최적 구조 탐색) |
| **연산 효율 ($PPA$)** | 낮음 ($Param$ 과다) | 보통 | 매우 높음 (효율적 자원 배분) |
| **설계 철학** | 구조의 단순화/직관성 | 층의 심화 ($Deeper$) | 성능과 자원의 균형 ($Efficiency$) |

> 요약: $ResNet$은 딥러닝의 깊이 제약을 허물었으며, $EfficientNet$은 연산 자원 대비 성능을 극대화하는 수치적 기준을 제시함

### 2. $PPA$ 및 트레이드오프 ($Trade$-$offs$)
- **Power/Resource**: $VGG$는 단순하나 파라미터가 비대하여 $GPU$ 메모리 점유율이 높음. $EfficientNet$은 동일 성능 대비 연산량($FLOPs$)을 획기적으로 감축함
- **Performance**: $ResNet$ 이후의 $ViT$($Vision$ $Transformer$)는 대규모 데이터셋에서 더 높은 성능을 보이나, 소규모 데이터에서는 $CNN$의 귀납적 편향($Inductive$ $Bias$) 부족으로 학습이 어려움
- **Trade-off**: 모델 깊이($Depth$), 너비($Width$), 해상도($Resolution$) 사이에는 상충 관계가 존재하며 이를 동시 최적화하는 것이 성능의 관건임

## Ⅲ. 구성요소/구조

### 1. 이미지 분류 프레임워크 인사이트 ($Architecture$ $Insight$)
- **Feature Extractor (Backbone)**: 합성곱($Convolution$) 연산을 통해 저수준(엣지)부터 고수준(객체 부분) 특징을 계층적으로 추출함
- **Residual Block**: $y = F(x) + x$ 구조를 통해 출력과 입력의 차이($Residual$)만 학습하게 하여, 항등 매핑($Identity$ $Mapping$)을 쉽게 확보하고 기울기 소실 방지
- **Global Average Pooling ($GAP$)**: 특징 맵 전체를 평균내어 하나의 벡터로 압축. $FC$ 레이어 대비 파라미터를 줄여 과적합($Overfitting$)을 방지함
- **Softmax Classifier**: 최종 벡터를 클래스별 확률 분포로 변환. $P(y=i|x) = \frac{e^{z_i}}{\sum e^{z_j}}$

### 2. 처리 파이프라인 흐름도
```text
[Input] -> [Augmentation] -> [Conv Layer Stack] -> [Pooling/GAP] -> [Softmax] -> [Result]
   |            |                 |                   |                |           |
Raw RGB     Flip/Crop         Hierarchical        Dimension        Prob Dist     Label
```

## Ⅳ. 문제점 및 개선방안

### 1. 실무적 문제점 및 대응 전략
1. **[데이터 불균형 ($Class$ $Imbalance$)]**: 희귀 질병이나 드문 불량 데이터 부족으로 다수 클래스에 편향된 모델 생성
   - **개선방안**: $SMOTE$ 오버샘플링, $Class$ $Weight$ 부여, 또는 $Focal$ $Loss$를 적용하여 어려운 샘플에 가중치를 둠 (확인: $F1$-$Score$, $mAP$)
2. **[엣지 환경의 추론 지연]**: 모바일이나 $IoT$ 기기에서 대형 모델의 실시간 추론 불가
   - **개선방안**: 지식 증류($Distillation$)로 소형 모델($MobileNet$ 등)에 전이하거나, $INT8$ 양자화 및 $Pruning$을 통한 경량화 수행 (확인: $Latency$ $ms$, $FPS$)
3. **[판단 근거의 불투명성 ($Black$-$box$)]**: 딥러닝 특성상 분류 결과에 대한 논리적 설명이 부족하여 신뢰도 저하
   - **개선방안**: $Grad$-$CAM$을 활용해 분류에 기여한 이미지 영역을 시각화(Heatmap)하여 전문가의 검증을 거침 (확인: $XAI$ 정성 평가)

### 2. 리얼월드 트러블슈팅 ($Real$-$world$ $Troubleshooting$)
- **상황**: 학습 시에는 높은 정확도를 보였으나, 실제 현장(조명 변화, 카메라 각도)에서 성능이 급격히 하락하는 '데이터 드리프트' 발생
- **해결**: 다양한 환경 광원을 모사한 데이터 증강($AutoAugment$)을 적용하고, $Test$-$time$ $Augmentation$($TTA$)을 통해 추론 시 안정성을 확보함

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **제조 외관 검사** | $ResNet$ 기반의 백본을 사용하여 부품의 정상/결함 유무를 초당 수십 회 실시간 판정 | $Recall$ (미검 방지), $Precision$ |
| **스마트 리테일** | 진열대 상품 이미지를 분류하여 재고 현황 파악 및 자동 발주 시스템 연동 | 분류 정확도 ($Accuracy$), $F1$ |
| **보안/관제** | 출입 통제 구역의 인가자/미인가자 얼굴 분류 및 이상 행동 징후 감별 | $AUC$-$ROC$, $EER$ |

## Ⅵ. 결론

이미지 분류는 시각 인공지능의 가장 성숙한 분야이나, 최근 $ViT$의 등장으로 $CNN$ 중심의 패러다임이 전이 학습과 대규모 데이터 기반의 $Transformer$로 이동하고 있음. 실무적으로는 단순 성능 지표를 넘어, 현장의 열악한 데이터 환경에서도 견디는 강건성($Robustness$)과 모델의 판단을 인간이 납득할 수 있는 설명 가능성($Explainability$) 확보가 비즈니스 가치 창출의 핵심이 될 것임.
