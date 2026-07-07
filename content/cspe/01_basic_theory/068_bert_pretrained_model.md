---
title: "BERT 사전학습 모델 (BERT Pre-trained Model)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 68
---

# BERT 사전학습 모델 (BERT Pre-trained Model)

## 1. 개요

- **정의/개념**: BERT는 Transformer encoder를 기반으로 양방향 문맥을 학습한 사전학습 언어모델이며, fine-tuning을 통해 다양한 NLP 과제에 적용된다.
- **배경/필요성**: 단어 의미는 문맥에 따라 달라지므로, 정적 임베딩보다 문장 양방향 문맥을 반영하는 범용 언어 표현이 필요하다.

BERT의 핵심은 문장을 왼쪽에서 오른쪽으로만 보는 것이 아니라 양방향 문맥으로 토큰 표현을 학습한다는 점이다.

## 2. 특징 및 비교

| 구분 | Word2Vec | BERT | GPT 계열 |
|---|---|---|---|
| 구조 | 정적 임베딩 | Transformer Encoder | Transformer Decoder |
| 문맥 반영 | 단어별 고정 | 양방향 문맥 | 자기회귀 문맥 |
| 주요 목적 | 단어 표현 | 이해 과제 | 생성 과제 |
| 적용 방식 | feature 입력 | fine-tuning | prompting/fine-tuning |

선택 기준은 이해·분류 과제 여부, 문맥 민감도, 추론 비용, fine-tuning 데이터 규모이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| WordPiece Tokenizer | subword 기반 입력 구성 | OOV 완화 |
| Transformer Encoder | self-attention으로 양방향 문맥 학습 | 문맥 표현 |
| MLM | Masked Language Modeling | 사전학습 목표 |
| Segment/Position Embedding | 문장 구분과 위치 정보 | 입력 구조 |
| Task Head | 분류·질의응답 등 과제별 출력층 | fine-tuning |

```text
문장 -> WordPiece -> Encoder -> 문맥임베딩 -> Task Head
```

사전학습 표현 위에 과제별 head를 얹는 구조이므로, 데이터가 적어도 다양한 이해 과제에 빠르게 적용할 수 있다.

## 4. 문제점 및 개선방안

1. **추론 비용**
   - Transformer encoder는 문장 길이에 따라 계산량과 메모리가 증가한다.
   - **개선방안**: DistilBERT, pruning, quantization, max length 조정을 적용한다.

2. **도메인 불일치**
   - 일반 corpus 사전학습 모델은 전문 도메인 용어와 문체에 약할 수 있다.
   - **개선방안**: domain-adaptive pretraining, fine-tuning 데이터 보강을 수행한다.

3. **입력 길이 제한**
   - 긴 문서는 잘리거나 문맥이 손실될 수 있다.
   - **개선방안**: sliding window, 문서 분할, long-context 모델을 검토한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 문서 분류 | CLS 표현과 task head로 분류 | F1, latency |
| 질의응답 | 질문·본문 pair에서 answer span 예측 | EM, F1 |
| 의미 유사도 | 문장 임베딩을 생성해 유사도 계산 | Spearman, retrieval |

## 6. 결론

BERT는 양방향 Transformer encoder로 문맥 표현을 학습한 대표 사전학습 모델이다. WordPiece, encoder, MLM, fine-tuning 구조를 연결해야 정적 임베딩과 GPT 계열 사이의 차이와 적용 기준이 분명해진다.
