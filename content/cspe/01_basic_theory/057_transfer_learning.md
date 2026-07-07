---
title: "전이 학습 (Transfer Learning) [출제: 123, 131회]"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 57
---

# 057. 전이 학습 (Transfer Learning) [출제: 123, 131회]

## Ⅰ. 개요

- **정의/개념**: 특정 분야에서 학습된 지식(모델 파라미터, 특징 추출기)을 유사하거나 새로운 분야의 모델 학습에 재사용하여 학습 효율을 높이는 머신러닝 기법임
- **배경/필요성**: 데이터 수집 및 레이블링 비용이 높은 분야에서 소량의 데이터만으로도 고성능 모델을 구축하고, 학습 시간과 컴퓨팅 자원을 절감하기 위해 필수적으로 사용됨

## Ⅱ. 특징 및 비교

| 판단 기준 | From Scratch (처음부터 학습) | Feature Extraction (특징 추출) | Fine-tuning (미세 조정) |
|:---|:---|:---|:---|
| **가중치 초기화** | 무작위 (Random) | 사전 학습 모델 고정 (Freeze) | 사전 학습 모델 초기값 사용 |
| **데이터 요구량** | 매우 많음 | 적음 | 중간 |
| **학습 범위** | 전체 레이어 | 출력층(Head)만 학습 | 하위 또는 전체 레이어 재학습 |
| **도메인 유사도** | 무관 | 매우 높아야 함 | 높거나 보통 수준 |

> 요약: 데이터가 적고 유사도가 높으면 특징 추출을, 데이터가 충분하면 미세 조정을 선택하는 것이 일반적임

## Ⅲ. 구성요소/구조

- **구성요소**:
  - **Source Domain/Task**: 풍부한 데이터로 이미 학습된 모델의 기원 분야(예: ImageNet)임
  - **Target Domain/Task**: 실제 해결하고자 하는 소량 데이터 분야(예: 의료 영상 판독)임
  - **Backbone (Pre-trained Model)**: 이미지의 선, 면 등 범용적 특징을 추출하는 하위 레이어 집합임
  - **Frozen Layers**: 학습 시 파라미터 업데이트를 방지하여 기존 지식을 보존하는 레이어들임
  - **New Classifier (Head)**: Target Task의 클래스 수에 맞춰 새로 설계된 출력 레이어임

- **원리/흐름도**:
```text
[Source Task] -> [Pre-trained Model] --(Knowledge Transfer)--> [Target Task]
       |                  |                                      |
  (Large Data)      (Frozen Layers)                        (Small Data)
                          |                                      |
                          v                                      v
                  [Generic Features]                   [Task-Specific Head]
                    (Edges, Shapes)                      (Classify Target)
```

## Ⅳ. 문제점 및 개선방안

1. **[부정적 전이 (Negative Transfer)]**: Source와 Target 도메인의 유사도가 낮아 기존 지식이 오히려 성능을 저하시키는 현상임
   - **개선방안**: 도메인 간 유사도를 측정하거나, 재학습(Fine-tuning) 범위를 넓혀 Target 데이터의 비중을 높임 (확인: Validation Loss)
2. **[치명적 망각 (Catastrophic Forgetting)]**: 새 데이터를 학습하면서 기존에 배운 범용적인 특징 정보가 사라지는 문제임
   - **개선방안**: 매우 낮은 학습률(Learning Rate)을 사용하거나, 점진적 언프리징(Gradual Unfreezing) 전략을 적용함 (확인: Source Task 성능 유지)
3. **[과적합 (Overfitting)]**: Target 데이터가 너무 적을 경우 고성능 사전 학습 모델이 해당 데이터에만 매몰될 수 있음
   - **개선방안**: 강력한 규제(Dropout, L2)를 적용하거나 데이터 증강(Augmentation)을 병행함 (확인: Train/Val Gap)

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **이미지 객체 탐지** | ImageNet으로 학습된 ResNet/VGG를 백본으로 사용 | mAP (mean Average Precision) |
| **자연어 처리 (NLP)** | BERT/GPT 등 거대 언어 모델을 특정 도메인(금융, 의료) 문서로 미세 조정 | F1-Score, Perplexity |
| **제조 불량 검사** | 표준 제품 이미지로 학습된 모델을 특정 라인의 소량 불량 이미지로 전이 학습 | Recall, Precision |

> 요약: 실무에서는 모델의 하위 레이어는 고정하고 상위 레이어만 학습시키는 전략으로 시작하여 점진적으로 최적화함

## Ⅵ. 결론

전이 학습은 '거인의 어깨 위에 올라타는 것'과 같이 검증된 지식을 활용해 딥러닝의 진입 장벽을 낮춘 핵심 기술임. 최근에는 초거대 파라미터를 가진 파운데이션 모델(Foundation Model)을 기반으로 한 어댑터(Adapter) 학습이나 LoRA(Low-Rank Adaptation) 등 효율적인 전이 학습 기법으로 발전하고 있으며, 이는 데이터 부족 문제를 겪는 실무 환경에서 가장 먼저 고려되는 필수 전략임.
