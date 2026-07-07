---
title: "전이 학습 (Transfer Learning)"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 57
---

# 057. 전이 학습 (Transfer Learning)

## Ⅰ. 개요

- **정의/개념**: 방대한 데이터로 이미 학습된 사전 학습 모델($Pre$-$trained$ $Model$)의 지식(가중치, 피처 추출기)을 새로운 목적지($Target$ $Domain$)의 모델 학습에 재사용하여 효율성을 극대화하는 기법임
- **배경/필요성**: 데이터 수집 및 레이블링 비용이 높은 특수 도메인에서 소량의 데이터만으로 고성능 모델을 구축하고, 학습 시간과 연산 자원($GPU/TPU$)을 획기적으로 절감하기 위함임

## Ⅱ. 특징 및 비교

### 1. 주요 특징 및 PPA (Power, Performance, Area)
- **Performance**: 학습 초기부터 높은 수준의 특징 추출 능력을 보유하므로 수렴 속도가 매우 빠르고, 적은 데이터로도 높은 일반화 성능을 달성함
- **Power**: 전체 레이어를 처음부터 학습($From$ $Scratch$)하는 대비 연산량을 $80 \sim 90\%$ 이상 절감 가능함
- **Trade-offs**: 사전 학습 도메인과 목표 도메인 간의 유사도($Domain$ $Similarity$)에 따른 성능 민감도가 존재함

### 2. 학습 전략별 비교

| 판단 기준 | $From$ $Scratch$ | $Feature$ $Extraction$ | $Fine$-$tuning$ (미세 조정) |
|:---|:---|:---|:---|
| **가중치 초기화** | 무작위 ($Random$) | 사전 학습 모델 고정 ($Freeze$) | 사전 학습 모델 기반 시작 |
| **학습 범위** | 전체 네트워크 | 출력층($Head$) 위주 | 일부 또는 전체 레이어 |
| **데이터 요구량** | 매우 많음 | 적음 | 중간 |
| **도메인 유사도** | 관계없음 | 매우 높아야 함 | 높거나 보통 수준 |

> 요약: 데이터가 적을수록 기존 지식을 보존($Freeze$)하고, 데이터가 충분할수록 미세 조정 범위를 넓히는 것이 정석임

## Ⅲ. 구성요소/구조

### 1. Architecture Insight: 계층적 특징 재사용
- **범용 특징(Lower Layers)**: 이미지의 선, 색상, 질감 등 어떤 도메인에서도 공통적으로 나타나는 기초 특징을 추출함
- **특수 특징(Upper Layers)**: 대상 객체의 구체적인 형태나 의미론적 정보($Semantic$ $Features$)를 파악하며, 이 부분이 $Target$ $Task$에 맞춰 조정됨
- **Knowledge Transfer**: $Source$ $Domain$($D_s, T_s$)에서 학습된 함수 $f_s(\cdot)$를 $D_t, T_t$ 학습의 시작점으로 활용함

### 2. 핵심 구성요소
- **Backbone**: 사전 학습된 가중치를 가진 신경망 본체 ($ResNet, BERT, ViT$ 등)
- **Classifier / Head**: 특정 $Target$ 클래스 수에 맞춰 새로 설계된 마지막 완전 연결 계층
- **Frozen Layers**: 파라미터 업데이트를 방지하여 기존의 범용적 특징 추출 능력을 유지하는 층
- **Learning Rate Differential**: $Backbone$에는 매우 낮은 학습률($\eta_{base} \approx 10^{-5}$)을, $Head$에는 상대적으로 높은 학습률($\eta_{head} \approx 10^{-3}$)을 적용

## Ⅳ. 문제점 및 개선방안

### 1. 핵심 문제 및 대응
1. **[부정적 전이 (Negative Transfer)]**: 두 도메인의 이질성이 커서 기존 지식이 오히려 학습을 방해하는 현상
   - **개선방안**: 도메인 유사성 분석 후, $Backbone$의 하위 레이어만 사용하거나 미세 조정 비중 상향
2. **[치명적 망각 (Catastrophic Forgetting)]**: 새 도메인 학습 중 기존에 배운 범용적 지식이 완전히 파괴되는 문제
   - **개선방안**: 점진적 언프리징($Gradual$ $Unfreezing$) 또는 $Elastic$ $Weight$ $Consolidation$($EWC$) 기법 적용
3. **[도메인 불일치 (Domain Shift)]**: 사전 학습 데이터와 실제 데이터의 분포 차이로 인한 성능 저하
   - **개선방안**: 도메인 적응($Domain$ $Adaptation$) 기법이나 $CycleGAN$ 등을 이용한 데이터 분포 보정

### 2. Real-world Troubleshooting
- **Overfitting on Small Data**: 사전 학습 모델이 너무 강력하여 소량의 $Target$ 데이터에 금방 과적합될 수 있음. 강력한 $Weight$ $Decay$와 $Dropout$을 적용하고, $Data$ $Augmentation$을 극대화해야 함
- **Normalization Statistics**: 미세 조정 시 $Batch$ $Normalization$의 $Running$ $Stats$를 업데이트할지, 고정할지에 따라 성능 차이가 큼. 데이터가 매우 적다면 고정($Freeze$)하는 것이 안정적임

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **의료 영상 진단** | $ImageNet$ 백본 모델을 $X$-$ray$ 병변 탐지용으로 미세 조정 | $Sensitivity, Specificity$ |
| **특수 도메인 챗봇** | $LLM$($Llama, GPT$)을 기업 내부 매뉴얼 데이터로 $LoRA$ 학습 | $Hallucination$ $Rate$ |
| **스마트 팩토리** | 표준 제품 이미지 모델을 신규 라인의 소량 불량 데이터로 전이 | $mAP, Precision$ |

> 요약: 실제 서비스 설계 시 사전 학습 모델의 라이선스와 추론 비용, 도메인 적합성을 종합적으로 검토해야 함

## Ⅵ. 결론

전이 학습은 '거인의 어깨 위에 올라타는' 전략으로, 현대 딥러닝이 실무 데이터 부족 문제를 정면으로 돌파하게 해준 핵심 패러다임임. 기술사적 관점에서 볼 때, 단순한 라이브러리 호출을 넘어 레이어별 학습 전략과 도메인 간의 기술적 간극($Gap$)을 메우는 최적화 역량이 중요하며, 최근에는 $Foundation$ $Model$을 기반으로 한 효율적 미세 조정 기법($PEFT, LoRA$ 등)으로 진화하고 있음.
