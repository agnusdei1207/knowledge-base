---
title: "BERT 사전학습 모델 (BERT Pre-trained Model) [출제: 121회]"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 68
---

# 068. BERT 사전학습 모델 (BERT Pre-trained Model) [출제: 121회]

## Ⅰ. 개요

- **정의/개념**: 트랜스포머(Transformer)의 인코더 구조를 기반으로, 방대한 말뭉치로부터 문맥의 양방향(Bidirectional) 관계를 사전 학습(Pre-training)하여 다양한 자연어 처리 태스크에 전이 학습이 가능한 언어 모델임
- **배경/필요성**: 기존 RNN이나 단방향 언어 모델(GPT 등)은 문맥의 전후 관계를 동시에 파악하는 데 한계가 있어, 문장의 깊은 의미 이해(NLU)가 필요한 태스크에서 성능을 극대화하기 위해 제안됨

## Ⅱ. 특징 및 비교

| 판단 기준 | Word2Vec (정적 임베딩) | GPT (Generative Pre-trained) | BERT (Bidirectional Encoder) |
|:---|:---|:---|:---|
| **모델 구조** | 룩업 테이블 기반 | Transformer Decoder | Transformer Encoder |
| **문맥 방향** | 고정된 의미 (정적) | 단방향 (Autoregressive) | 양방향 (Autoencoding) |
| **주요 강점** | 가볍고 빠름 | 자연어 생성 (NLG) | 자연어 이해 (NLU) |
| **대표 태스크** | 단어 유사도 측정 | 챗봇, 작문, 요약 | 분류, 질의응답, 개체명 인식 |

> 요약: BERT는 문장 전체의 문맥을 양방향으로 동시에 고려하여 단어의 동적 의미를 파악하는 데 최적화됨

## Ⅲ. 구성요소/구조

- **구성요소**:
  - **Transformer Encoder**: Self-Attention 메커니즘을 통해 문장 내 모든 단어 간의 관계를 병렬로 처리함
  - **WordPiece Tokenizer**: 단어를 더 작은 단위로 쪼개어 미등록어(OOV) 문제를 해결함
  - **MLM (Masked Language Model)**: 입력 문장 중 일부를 마스킹하고, 주변 문맥을 통해 원래 단어를 맞히는 사전 학습 방식임
  - **NSP (Next Sentence Prediction)**: 두 문장이 주어졌을 때, 실제로 이어지는 문장인지 판별하여 문장 간 관계를 학습함
  - **Embeddings**: Token, Segment, Position 임베딩을 합산하여 입력으로 사용함

- **학습/구조도**:
```text
[Input] -> [Embedding Layer] -> [Multi-Layer Transformer Encoders] -> [Output Representation]
             (Token/Pos/Seg)        (Self-Attention/FFN)             (Contextual Vector)

[Pre-training Targets]
1. MLM: "The [MASK] sat on the mat" -> "cat"
2. NSP: [Sentence A] + [Sentence B] -> "Is Next?"
```

## Ⅳ. 문제점 및 개선방안

1. **[높은 연산 복잡도]**: 모델 파라미터가 방대하여 모바일이나 실시간 서비스 환경에서 추론 속도가 느리고 메모리 점유가 큼
   - **개선방안**: 지식 증류(Distillation)를 통해 모델을 경량화한 DistilBERT, TinyBERT 등을 사용하거나 양자화(Quantization)를 수행함 (확인: 추론 지연 시간)
2. **[사전 학습-미세 조정 간 괴리]**: 사전 학습 시에는 `[MASK]` 토큰이 존재하나, 실제 미세 조정 시에는 존재하지 않아 발생하는 불일치 문제임
   - **개선방안**: 마스킹 시 일부를 실제 단어나 램덤 단어로 대체하는 전략을 사용하거나, Electra와 같은 대체 학습 방식을 검토함 (확인: Fine-tuning 성능)
3. **[입력 길이 제한]**: 트랜스포머 구조 특성상 입력 문장 길이에 따라 연산량이 제곱으로 증가하여 긴 문서 처리가 어려움
   - **개선방안**: 중요한 문장만 추출(Extraction)하여 요약 후 입력하거나, Longformer/BigBird와 같은 Sparse Attention 모델을 사용함 (확인: 컨텍스트 범위)

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| **검색 엔진 (Google/Naver)** | 검색어의 의도를 문맥적으로 파악하여 가장 관련성 높은 웹페이지 랭킹 | nDCG, 클릭 정확도 |
| **스마트 팩토리 QA** | 기기 매뉴얼 데이터를 학습하여 현장 작업자의 질문에 대한 정답 구간 추출 | Exact Match (EM), F1-Score |
| **금융 뉴스 감성 분석** | 뉴스 기사의 양방향 문맥을 파악해 주가에 미칠 긍정/부정 영향도 분류 | Precision, Recall, F1 |

> 요약: 실무에서는 특정 도메인 데이터로 추가 학습(Domain-adaptive Pre-training)한 모델(BioBERT, FinBERT 등)을 주로 사용함

## Ⅵ. 결론

BERT는 자연어 이해 분야의 새로운 지평을 연 모델로, 양방향 문맥 학습과 전이 학습의 유용성을 입증하며 현대 NLP의 표준 아키텍처로 자리 잡았음. 비록 최근에는 생성 능력이 탁월한 GPT 계열에 밀리는 추세이나, 정교한 텍스트 분류나 개체명 인식, 정보 추출과 같이 높은 '이해력'과 '신뢰도'가 요구되는 기업용 AI 태스크에서는 여전히 대체 불가능한 핵심 모델로 활용되고 있음.
