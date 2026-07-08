---
title: "Multi-Head Attention (멀티 헤드 어텐션)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 37
extra:
  question_no: "037"
  exam_status: "기출"
  exam_history: "135회, 136회"
---

## 미리 알고가기

- Head는 Q, K, V를 서로 다른 투영 공간에서 독립적으로 계산하는 병렬 어텐션 단위임
- Concat은 각 Head 출력을 다시 합쳐 원래 모델 차원으로 복원하는 단계임
- Output Projection은 합쳐진 표현을 후속 레이어가 쓰기 좋게 재조정하는 선형 변환임

## Ⅰ. 개요

- **정의/개념**: Multi-Head Attention은 입력 표현을 여러 하위 공간으로 선형 투영한 뒤 각 Head가 독립적으로 attention을 계산하고 그 결과를 결합해 문맥 표현을 풍부하게 만드는 Transformer 핵심 모듈임
- **배경/필요성**: 단일 attention은 하나의 유사도 축만 강하게 반영하기 쉬우므로, 문법 관계와 의미 관계와 장거리 의존성을 동시에 포착하려면 다중 관점의 병렬 attention 구조가 필요함

## Ⅱ. 특징

- 서로 다른 Head가 상이한 관계 패턴을 학습해 단일 attention보다 표현 다양성이 높음
- 전체 차원을 여러 Head로 분할하므로 표현력 증대 대비 연산량 증가를 통제할 수 있음
- Self-Attention과 Cross-Attention 모두에 동일한 구조를 적용할 수 있어 재사용성이 높음
- Head 수가 늘수록 KV cache와 통신 비용도 커지므로 추론 아키텍처 선택과 함께 설계해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Single-Head Attention | Multi-Head Attention | MQA/GQA |
|:---|:---|:---|:---|
| 표현 관점 수 | 1개 | 다수 | 다수이나 K,V 공유 |
| 관계 포착력 | 제한적임 | 높음 | 높음과 비용 절충 |
| KV cache 크기 | 작음 | 큼 | 상대적으로 작음 |
| 대표 활용 | 단순 기준선 | Transformer 표준 | 대규모 LLM 추론 최적화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Input Projection | 입력을 각 Head용 $W_Q$, $W_K$, $W_V$로 분기해 서로 다른 관점의 비교 공간을 형성함 |
| Per-Head Attention | 각 Head가 독립적으로 scaled dot-product attention을 수행해 특정 관계 패턴을 포착함 |
| Concatenation | 각 Head의 결과를 결합해 분산된 관점을 하나의 표현으로 회수하는 단계임 |
| Output Projection | 결합된 표현을 최종 선형 변환으로 정리해 잔차 연결과 다음 레이어가 활용하기 좋게 만듦 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-----------+     +-----------+     +---------------+     +-----------+
| 선형투영  | --> | Head 분할 | --> | 병렬 Attention | --> | 결합/출력 |
+-----------+     +-----------+     +---------------+     +-----------+
```

1. **선형 투영**: 입력 임베딩을 각 Head별 Query, Key, Value 공간으로 분기함
2. **Head 분할**: 모델 차원을 여러 Head 차원으로 나누어 병렬 계산 단위를 형성함
3. **병렬 Attention**: 각 Head가 독립적으로 attention을 수행해 문법, 의미, 장거리 의존성 등 상이한 관계를 학습함
4. **결합 및 출력**: Head 결과를 이어 붙이고 출력 투영을 거쳐 후속 레이어 입력으로 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: Head 수가 많아질수록 KV cache와 attention 커널 호출이 늘어나 추론 지연과 메모리 사용량이 커짐
   - 해결방안: MQA 또는 GQA로 K,V 공유를 도입하고 KV cache 크기와 token throughput으로 최적 구성을 검증함
2. 문제: 일부 Head가 유사한 패턴만 반복 학습해 표현 다양성은 늘지 않고 비용만 증가할 수 있음
   - 해결방안: Head importance 분석과 pruning을 병행하고 제거 전후 accuracy와 attention diversity 지표로 효과를 검증함
3. 문제: 대형 분산 학습 환경에서는 Head 병렬 처리와 출력 결합 과정의 통신 비용이 병목이 될 수 있음
   - 해결방안: tensor parallel 전략과 fused kernel을 함께 적용하고 GPU utilization과 all-reduce 시간을 기준으로 병목 완화 여부를 검증함

## Ⅶ. 적용 사례

- LLM 블록 구조: Multi-Head Attention으로 문맥, 지시, 장거리 의존성을 동시에 반영함, 확인 지표는 perplexity와 throughput임
- Vision Transformer: 이미지 패치 간 관계를 여러 관점으로 병렬 해석함, 확인 지표는 top-1 accuracy와 latency임
- 멀티모달 모델: 텍스트와 이미지 토큰 간 교차 관계를 Head별로 나누어 처리함, 확인 지표는 VQA accuracy와 inference cost임

## Ⅷ. 결론

Multi-Head Attention의 핵심 가치는 Head 수를 늘리는 데 있지 않고 다양한 관계를 포착하면서도 KV cache와 통신 비용을 통제하는 균형 설계에 있음.
