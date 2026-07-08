---
title: "Scaled Dot-Product Attention (스케일드 닷 프로덕트 어텐션)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 36
extra:
  question_no: "036"
  exam_status: "기출"
  exam_history: "135회, 136회"
---

## 미리 알고가기

- Query, Key, Value는 각각 질의 기준, 비교 기준, 전달 정보를 담는 벡터임
- Softmax는 점수 분포를 확률 가중치로 바꾸어 어떤 토큰에 더 집중할지 정하는 함수임
- $d_k$는 Key 벡터 차원으로, 값이 커질수록 내적 점수 분산도 함께 커짐

## Ⅰ. 개요

- **정의/개념**: Scaled Dot-Product Attention은 $QK^T$로 토큰 간 연관도를 계산한 뒤 $\sqrt{d_k}$로 점수를 스케일링하고 Softmax 가중치를 Value에 곱해 문맥 표현을 만드는 Transformer의 기본 어텐션 연산임
- **배경/필요성**: 단순 내적 기반 어텐션은 차원이 커질수록 점수 분산이 커져 Softmax가 포화되므로, GPU 친화적 행렬 연산의 장점을 유지하면서도 학습 안정성을 확보할 스케일 보정이 필요함

## Ⅱ. 특징

- 행렬 곱 기반으로 구현되어 GPU 병렬 처리 효율이 높고 대규모 모델에 적합함
- $\sqrt{d_k}$ 스케일링으로 점수 분산을 제어해 Softmax 포화와 기울기 불안정을 줄임
- 마스크를 함께 적용할 수 있어 패딩 무시와 causal decoding 같은 제약을 동일 연산 안에 수용함
- Multi-Head Attention, FlashAttention, Long Context 최적화의 기준 연산으로 재사용됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Additive Attention | Dot-Product Attention | Scaled Dot-Product Attention |
|:---|:---|:---|:---|
| 유사도 계산 | 별도 신경망 결합 | 단순 내적 | 내적 후 $\sqrt{d_k}$ 보정 |
| 차원 증가 시 안정성 | 비교적 안정적임 | 점수 포화 위험이 큼 | 분산 제어로 안정적임 |
| 연산 효율 | 상대적으로 낮음 | 높음 | 높으면서도 안정적임 |
| 대표 활용 | 초기 seq2seq | 이론적 기본형 | Transformer 표준 구현 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Query, Key | 현재 토큰이 무엇을 찾는지와 각 토큰이 어떤 기준으로 비교될지를 표현해 연관도 계산의 축을 형성함 |
| Score Matrix | $QK^T$ 결과로 생성되는 유사도 행렬이며 어떤 토큰 쌍이 서로 강하게 연결되는지 나타냄 |
| Scale, Mask, Softmax | 차원 보정과 causal 또는 padding 제약을 반영한 뒤 가중치 분포를 안정적으로 정규화하는 단계임 |
| Value Aggregation | 정규화된 가중치를 Value에 곱해 문맥이 반영된 최종 표현을 만들며 후속 레이어 입력 품질을 좌우함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-----------+     +-----------+     +-----------------+     +-----------+
| QK^T 계산 | --> | 스케일링  | --> | 마스크+Softmax  | --> | V 가중합  |
+-----------+     +-----------+     +-----------------+     +-----------+
```

1. **유사도 계산**: Query와 Key를 내적해 각 토큰이 다른 토큰과 얼마나 연관되는지 점수 행렬을 구함
2. **스케일링**: 계산된 점수를 $\sqrt{d_k}$로 나누어 차원 증가에 따른 점수 분산 확대를 억제함
3. **마스크 및 정규화**: causal mask나 padding mask를 적용한 뒤 Softmax로 확률 가중치를 만듦
4. **정보 결합**: 확률 가중치를 Value에 곱해 현재 토큰이 참조할 문맥 벡터를 완성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 시퀀스 길이가 길어질수록 모든 토큰 쌍을 계산해야 하므로 메모리와 연산 비용이 $O(N^2)$로 급증함
   - 해결방안: FlashAttention, block sparse attention 같은 최적화 커널을 적용하고 최대 컨텍스트 길이별 VRAM 사용량과 TTFT로 효과를 검증함
2. 문제: 스케일 보정이나 저정밀 연산 설정이 부정확하면 Softmax 포화와 수치 오차가 커져 학습 안정성이 떨어짐
   - 해결방안: 안정적인 스케일링 규칙과 mixed precision 검증을 함께 적용하고 loss divergence 빈도와 gradient norm으로 안정성을 검증함
3. 문제: causal mask나 padding mask가 잘못 적용되면 미래 토큰 정보 누출이나 무의미한 패딩 참조가 발생함
   - 해결방안: 마스크 생성 로직을 연산 경로에 고정하고 attention map 샘플링과 정답 일치율로 제약 준수 여부를 검증함

## Ⅶ. 적용 사례

- LLM 디코더 블록: causal mask를 포함한 scaled attention으로 다음 토큰 예측을 수행함, 확인 지표는 TTFT와 TPOT임
- Transformer 인코더: 문장 전체 토큰 관계를 병렬 계산해 의미 표현을 강화함, 확인 지표는 downstream accuracy와 latency임
- FlashAttention 기반 추론 서버: 동일 연산을 I/O 최적화 커널로 가속함, 확인 지표는 GPU 메모리 사용량과 token throughput임

## Ⅷ. 결론

Scaled Dot-Product Attention은 내적 기반 고속 어텐션에 분산 제어를 결합해 Transformer 확장의 기초를 만든 표준 연산이므로, 성능 판단은 수식 자체보다 긴 문맥에서의 비용과 마스크 정확도까지 함께 봐야 함.
