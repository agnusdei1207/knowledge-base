---
title: "BERT 사전학습 모델 (BERT Pre-trained Model)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 68
---

## 미리 알고가기

- Transformer 인코더: 입력 전체 토큰을 양방향 self-attention으로 읽어 문맥 표현을 만드는 구조임
- MLM: 일부 토큰을 가리고 원래 토큰을 예측하는 masked language modeling 학습임
- NSP: 두 문장이 실제로 이어지는지 판별하는 next sentence prediction 학습임
- 문장 분류 토큰(Classification Token, `[CLS]`): 문장 또는 문서 전체 표현을 모으는 분류용 특수 토큰임
- 파인튜닝: 사전학습된 모델에 태스크별 지도 데이터를 추가 학습하는 과정임

## Ⅰ. 개요

- **정의**: BERT는 Transformer 인코더로 좌우 문맥을 동시에 반영한 범용 언어 이해 표현을 사전학습하는 모델임
- **배경/필요성**: 정적 임베딩은 문맥에 따라 달라지는 의미를 표현하지 못하고, 단방향 언어 모델은 뒤쪽 문맥을 보지 못해 이해 태스크에 한계가 있음
- **비유**: 문장 전체를 앞뒤로 읽은 뒤 빈칸과 문장 관계를 맞히며 독해력을 미리 길러 둔 범용 독해자와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 양방향 인코더 표현 변환기(Bidirectional Encoder Representations from Transformers, BERT) 구조 설명 | 인코더, 양방향 self-attention, `[CLS]` | 생성형 사전학습 변환기(Generative Pre-trained Transformer, GPT) 디코더 구조와 혼동 |
| 사전학습·파인튜닝 설명 | 마스크 언어 모델링(Masked Language Modeling, MLM), 다음 문장 예측(Next Sentence Prediction, NSP), downstream task head | `[MASK]`의 학습-추론 차이 누락 |

> 요약: BERT는 양방향 문맥을 학습한 인코더 기반 사전학습 모델로, 생성보다 자연어 이해 태스크에 적합함

## Ⅱ. 특징/비교

| 판단 기준 | Word2Vec/전역 벡터(Global Vectors, GloVe) | 양방향 인코더 표현 변환기(Bidirectional Encoder Representations from Transformers, BERT) | 생성형 사전학습 변환기(Generative Pre-trained Transformer, GPT) 계열 |
|:---|:---|:---|:---|
| 문맥 처리 | 단어마다 고정 벡터를 사용함 | 좌우 문맥을 동시에 반영함 | 이전 토큰만 보고 다음 토큰을 생성함 |
| 구조 | 얕은 임베딩 또는 행렬 분해 | Transformer 인코더 | Transformer 디코더 |
| 주요 용도 | 경량 피처, 검색, 추천 | 분류, 개체명 인식(Named Entity Recognition, NER), 질의응답(Question Answering, QA), 검색 랭킹 | 생성, 대화, 요약, 코드 작성 |
| 선택 기준 | 비용 제약과 단순 유사도 | 이해 정확도와 문맥 해석 | 자연어 생성과 지시 수행 |

> 요약: BERT는 정적 임베딩보다 문맥 이해가 강하고, 생성이 필요 없는 NLU 태스크를 GPT보다 작은 모델 크기와 추론 비용으로 처리함

- **양방향성**: 모든 토큰이 좌우 문맥을 함께 참고하므로 빈칸 예측과 문장 분류에 강함
- **전이 학습**: 대규모 말뭉치 지식을 소량 태스크 데이터에 이전할 수 있음
- **운영 선택**: 생성이 필요하지 않은 분류·검색에는 GPT보다 BERT 계열이 비용 측면에서 합리적일 수 있음

## Ⅲ. 구성요소

```text
+-------------+      +-------------+      +-------------+
| Token IDs   | ---> | Embedding   | ---> | Transformer |
| Segment Pos |      | Sum         |      | Encoder x N |
+------+------+      +------+------+      +------+------+
       |                    |                    |
       v                    v                    v
+-------------+      +-------------+      +-------------+
| MLM Head    | <--- | Context     | ---> | CLS Head    |
| token pred  |      | Vectors     |      | task pred   |
+-------------+      +-------------+      +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 입력 임베딩 | 토큰, 세그먼트, 위치 임베딩을 더해 문장 쌍과 순서를 표현함 | 좌표 부여 |
| Multi-Head Attention | 문장 전체 토큰 간 관계를 여러 관점의 가중치로 계산함 | 여러 독해 렌즈 |
| Feed-Forward Network | 각 토큰 표현을 비선형 변환해 문맥 정보를 정제함 | 의미 가공기 |
| 마스크 언어 모델링 헤드(Masked Language Modeling Head, MLM Head) | 가려진 토큰의 원래 값을 예측해 언어 지식을 학습함 | 빈칸 채점기 |
| Task Head | `[CLS]` 또는 토큰 표현 위에 분류, 개체명 인식(Named Entity Recognition, NER), 질의응답(Question Answering, QA) 출력층을 붙임 | 업무별 판정기 |

> 요약: BERT는 입력 임베딩과 인코더 블록이 만든 문맥 벡터를 사전학습 헤드와 태스크 헤드가 활용하는 구조임

## Ⅳ. 절차

```text
+-----------+     +-----------+     +-----------+     +-----------+
| Build     | --> | Pretrain  | --> | Fine Tune | --> | Infer     |
| Corpus    |     | MLM / NSP |     | Task Head |     | NLU Result|
+-----------+     +-----------+     +-----------+     +-----------+
      |                 |                 |                 |
      v                 v                 v                 v
unlabeled text      context learning   labeled data       prediction
```

1. **코퍼스 구성**: 대규모 비지도 텍스트를 토크나이징하고 문장 쌍과 마스크 위치를 생성함
2. **사전학습**: MLM으로 가려진 토큰을 예측하고, 필요한 경우 NSP로 문장 관계를 학습함
3. **파인튜닝**: 태스크별 소량 라벨 데이터로 출력 헤드와 전체 모델 가중치를 미세 조정함
4. **추론·평가**: 분류 정확도, F1, 평균 역순위(Mean Reciprocal Rank, MRR), 완전일치(Exact Match, EM)/F1 등 태스크 지표로 문맥 이해 성능을 확인함

> 요약: BERT는 비지도 사전학습으로 언어 표현을 얻고 지도 파인튜닝으로 특정 이해 태스크에 맞추는 전이 학습 절차를 따름

## Ⅴ. 문제점 및 개선방안

- **P1 학습-추론 불일치**: 사전학습 중 쓰는 `[MASK]` 토큰이 실제 추론 입력에는 등장하지 않아 분포 차이가 생김
- **P1 대응**: ELECTRA의 replaced token detection이나 RoBERTa식 학습 전략으로 사전학습 목표를 보완함 (확인: GLUE, downstream F1)
- **P2 긴 문서 처리 한계**: self-attention 복잡도가 입력 길이의 제곱으로 증가해 512 토큰 이상 문서 처리 비용이 큼
- **P2 대응**: Longformer, BigBird, sliding window chunking으로 긴 문서 attention 비용을 줄임 (확인: 최대 입력 길이, 문서 QA F1)
- **P3 추론 비용과 지연**: 인코더 층과 attention 연산이 많아 실시간 서비스에서 p95 지연과 그래픽 처리 장치(Graphics Processing Unit, GPU) 비용이 증가함
- **P3 대응**: DistilBERT, quantization, pruning, batch 최적화로 모델을 경량화함 (확인: p95 지연, 처리량)

> 요약: 사전학습 목표 개선, sparse attention, 모델 경량화를 조합해 BERT의 정확도와 운영 비용을 균형화함

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 고객 문의 의도 분류 | 생성이 필요 없고 라벨 데이터가 제한된 업무는 양방향 인코더 표현 변환기(Bidirectional Encoder Representations from Transformers, BERT)에 문장 분류 토큰(Classification Token, `[CLS]`) 기반 헤드를 붙여 파인튜닝함 | 거시 F1 점수(Macro F1 Score, Macro-F1), p95 추론 지연 |
| 검색 재랭킹 | bi-encoder로 후보를 줄인 뒤 cross-encoder BERT로 질의-문서 쌍을 재점수화해 정확도와 비용을 분리함 | 평균 역순위(Mean Reciprocal Rank, MRR), 정규화 할인 누적 이득(Normalized Discounted Cumulative Gain, NDCG) |
| 문서 질의응답 | 긴 문서는 sliding window로 나누고 답변 span이 분할 경계에서 누락되지 않도록 겹침 폭을 조정함 | 완전일치(Exact Match, EM), 질의응답 F1 점수(Question Answering F1 Score, QA-F1), 최대 입력 길이 |

> 요약: BERT는 생성보다 이해·분류·재랭킹에 적합하며 입력 길이와 지연 조건을 지표로 검증해야 함

## Ⅶ. 전망

- **발전 방향**: 도메인 특화 BERT, 검색용 bi-encoder/cross-encoder, 경량 온디바이스 NLU 모델로 활용이 지속될 전망임
- **기술사적 판단**: 생성 기능이 필요하지 않은 이해·분류 업무에서는 대형 GPT보다 BERT 계열이 비용과 통제 측면에서 유리할 수 있음
- **기술사 제언**: 답안에서는 BERT를 단순 언어 모델이 아니라 양방향 인코더, MLM, 파인튜닝의 결합 구조로 설명해야 함
