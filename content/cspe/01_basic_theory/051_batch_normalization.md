---
title: "배치 정규화 (Batch Normalization)"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 51
---

# 051. 배치 정규화 (Batch Normalization)

## Ⅰ. 개요

- **정의/개념**: 신경망의 각 층마다 입력 분포를 평균 $0$, 분산 $1$로 정규화한 후, 학습 가능한 파라미터 $\gamma$(Scale)와 $\beta$(Shift)를 적용해 내부 공변량 변화를 제어하고 네트워크의 학습 효율을 극대화하는 기법임
- **배경/필요성**: 층이 깊어질수록 이전 층의 파라미터 미세 변화가 다음 층 입력 분포의 누적 변동을 야기하는 내부 공변량 변화(Internal Covariate Shift) 문제를 해결하고, 가중치 초기화 의존성을 탈피하여 고속 학습을 구현하기 위함임

## Ⅱ. 특징 및 비교

### 1. 주요 특징 및 PPA (Power, Performance, Area)
- **Performance**: 학습 속도를 획기적으로 개선하며, 더 큰 학습률($Learning Rate$) 사용을 가능케 하여 전역 최적점($Global Minimum$)에 빠르게 도달함
- **Power**: 정규화 과정에서 평균과 분산 계산($O(N \cdot C \cdot H \cdot W)$)에 따른 연산 부하가 발생하나, 전체 학습 에포크($Epoch$) 단축으로 총 전력 소비를 절감함
- **Area/Memory**: 추론 시 활용할 이동 평균($Running Mean$)과 이동 분산($Running Variance$) 저장을 위해 추가적인 메모리 공간이 필요함

### 2. 정규화 기법 비교 및 Trade-offs

| 판단 기준 | Batch Normalization (BN) | Layer Normalization (LN) | Group Normalization (GN) |
|:---|:---|:---|:---|
| **정규화 단위** | $Mini-batch$ 전체 (동일 채널) | 개별 샘플의 전체 채널 | 개별 샘플의 채널 그룹 |
| **핵심 이점** | 높은 일반화 성능, $CNN$ 최적 | 시계열($RNN$), $Transformer$ 최적 | 소규모 배치 환경 안정성 |
| **Trade-offs** | 배치 크기 의존성 vs 성능 | 연산 복잡도 vs 배치 독립성 | 그룹 수($G$) 설정 민감도 |
| **주요 한계** | 소규모 배치 시 추정치 왜곡 | 채널 간 상관관계 무시 | 그룹 내 데이터 불균형 시 효율 저하 |

> 요약: $BN$은 $CNN$ 구조에서 압도적 성능을 보이나, 배치 크기에 따른 학습 안정성의 트레이드오프를 가짐

## Ⅲ. 구성요소/구조

### 1. Architecture Insight
- **삽입 위치**: 일반적으로 선형 변환($Linear/Conv$)과 활성화 함수($Activation$) 사이에 위치하여, 활성화 함수로 입력되는 값들이 포화 영역($Saturating Region$)에 빠지지 않도록 유도함
- **학습/추론 분리**: 학습 시에는 현재 배치의 통계량을 사용하고, 추론 시에는 학습 과정에서 누적된 이동 평균 통계량을 사용하여 일관성을 유지함

### 2. 핵심 알고리즘 및 수식
- **Mini-batch Mean**: $\mu_{\mathcal{B}} = \frac{1}{m} \sum_{i=1}^{m} x_i$
- **Mini-batch Variance**: $\sigma_{\mathcal{B}}^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_{\mathcal{B}})^2$
- **Normalize**: $\hat{x}_i = \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}$ (분모가 $0$이 되는 것을 방지하는 소량 $\epsilon$ 추가)
- **Scale and Shift**: $y_i = \gamma \hat{x}_i + \beta$ (신경망의 표현력을 유지하기 위한 복원 단계)

## Ⅳ. 문제점 및 개선방안

### 1. 핵심 문제 및 대응
1. **[배치 크기 의존성]**: $Mini-batch$ 크기가 작을 때 평균/분산의 추정 오차가 커져 학습이 불안정해짐
   - **개선방안**: 배치 크기 제약이 없는 $Layer Norm$ 또는 $Group Norm$ 도입, 혹은 $Batch Renormalization$ 적용
2. **[RNN 적용의 복잡성]**: 시퀀스 길이에 따라 배치 통계량이 급격히 변하여 시간축 정규화가 어려움
   - **개선방안**: 시간축 영향이 없는 $LN$ 사용 권장 (확인: $Sequence Loss$ 수렴도)
3. **[Distributed Training 불일치]**: 여러 $GPU$에서 배치 통계가 분산되어 전역 통계량과 불일치 발생
   - **개선방안**: $SyncBN$(Synchronized Batch Normalization)을 통해 전체 $GPU$의 통계량을 동기화함

### 2. Real-world Troubleshooting
- **Evaluation Mode 성능 저하**: 학습 완료 후 `model.eval()` 시 추론 성능이 급격히 떨어진다면, 이동 평균이 충분히 수렴하지 않았거나 학습/테스트 데이터 분포 차이($Dataset Shift$)를 점검해야 함
- **Gradient Exploding**: $\epsilon$ 값이 너무 작으면 분모 불안정으로 인해 그래디언트가 폭주할 수 있으므로 적절한 정밀도 설정이 필요함

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **High-Res Vision Task** | 대형 이미지 처리를 위한 메모리 제한 시 $Group Norm$으로 대체 | $mAP$, $Memory Usage$ |
| **Transformer Architecture** | 대규모 언어 모델($LLM$)에서 $BN$ 대신 $LN$을 채택하여 가변 길이 처리 | $Perplexity$, 학습 안정성 |
| **Object Detection** | 작은 배치 사이즈가 강제되는 환경에서 $Frozen BN$ 또는 $SyncBN$ 적용 | 검출 정확도($Precision/Recall$) |

> 요약: 실제 시스템 설계 시 데이터의 도메인(이미지 vs 텍스트)과 가용 메모리 자원을 고려한 정규화 전략이 필요함

## Ⅵ. 결론

배치 정규화는 내부 공변량 변화를 억제하여 딥러닝의 심층화를 가능케 한 핵심 아키텍처임. 기술사적 관점에서 볼 때, 단순히 적용 여부를 넘어 배치 통계의 편향 문제와 추론 시의 일관성을 관리하는 능력이 중요하며, $Transformer$와 같은 최신 구조에서는 데이터 특성에 따른 변형 기법($LN, RMSNorm$ 등)을 유연하게 선택하는 설계 역량이 요구됨.
