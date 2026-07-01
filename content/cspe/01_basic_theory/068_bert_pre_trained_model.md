---
title: "BERT 사전학습 모델 (BERT Pre-trained Model)"
date: "2026-07-01"
tags:
  - "cspe-basic-theory"
weight: 68
---

# 📖 【암기용】 개념 완전 이해

> 목적: BERT를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 양방향 Transformer Encoder로 문맥 표현을 학습한 사전학습 언어모델
- **왜 필요한가**: Word2Vec은 단어 하나에 벡터 하나를 주지만, BERT는 문장 안 위치와 주변 단어를 함께 보고 토큰 의미를 다르게 표현한다.
- **핵심 직관**: 빈칸 문제를 대량으로 풀며 단어의 앞뒤 문맥을 동시에 읽는 언어 이해 모델이다.

## 깊이 이해
- **배경·문제의식**:
  - 전통 임베딩은 다의어·문맥 차이를 반영하지 못했고, RNN 계열은 긴 문맥 병렬처리에 제약이 있었다
  - BERT는 Transformer Encoder와 Self-Attention으로 문장 전체 관계를 병렬 계산한다
- **작동 원리**:
  - 입력 토큰에 token embedding, position embedding, segment embedding을 더한다
  - MLM(Masked Language Modeling)으로 일부 토큰을 맞히고, 원 논문은 NSP(Next Sentence Prediction)로 문장 관계를 학습했다
- **비유**: 시험에서 문장 앞뒤를 모두 읽고 빈칸 단어를 고르는 방식과 같다.
  - 한 단어만 보지 않고 주변 단어의 단서를 attention으로 가중한다
- **구체 예시**:
  - BERT-base는 12 layer, hidden 768, attention head 12, 약 110M parameter 구조다
  - 한국어 문서 분류는 사전학습 모델 fine-tuning으로 소량 라벨 데이터에서도 F1 0.85 이상 목표를 둔다
- **흔한 오해·주의점**:
  - BERT는 생성 모델이 아니라 이해 중심 Encoder 모델이다
  - 긴 문서 생성은 GPT 계열이 적합하고, BERT는 분류·NER·QA 추출형 문제에 맞는다

## 연결 개념
- Transformer — BERT의 Encoder 기반 구조
- WordPiece — BERT 입력 토큰화 방식
- GPT — Decoder 기반 생성 언어모델 비교 대상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BERT는 Transformer Encoder와 Self-Attention으로 양방향 문맥 표현을 학습하는 사전학습 언어모델이다.
> 2. **가치**: MLM 기반 사전학습 후 fine-tuning으로 분류·NER·질의응답에서 라벨 데이터 요구량을 줄이고 F1·EM 지표를 개선한다.
> 3. **판단 포인트**: 이해 업무는 BERT, 생성 업무는 GPT, 긴 문서 검색 결합은 RAG 또는 Longformer 계열을 검토한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 양방향 문맥을 학습한 Transformer Encoder 기반 사전학습 언어모델
- 배경: 다의어·문장 관계·문맥 의존 표현을 다뤄야 하는 NLP 업무에서 정적 임베딩은 한계를 가짐
- 필요성: 기업 문서 분류·개체명 인식·검색 질의 이해에 사전학습된 문맥 표현 활용이 필요함

---

## Ⅱ. 구조 및 구성요소

```text
문장 -> WordPiece 토큰 -> 임베딩 합산 -> Transformer Encoder Stack -> 문맥 벡터
        +-> [CLS]/[SEP]
        +-> MLM/NSP 또는 fine-tuning head
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| WordPiece | 입력 문장을 서브워드 토큰으로 분해 | `[CLS]`, `[SEP]`, `[MASK]` 사용 |
| Embedding | token·position·segment embedding 합산 | 최대 길이 512 토큰 기본 |
| Encoder | Self-Attention과 FFN 반복 | BERT-base 12 layer, 110M |
| Task Head | 분류·NER·QA 출력층 | fine-tuning으로 업무 적응 |

> 요약: BERT는 서브워드 입력을 Encoder Stack으로 처리해 `[CLS]` 또는 토큰별 문맥 벡터를 업무 출력층에 전달한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
대규모 말뭉치 -> MLM 사전학습 -> 사전학습 가중치 저장
-> 라벨 데이터 fine-tuning -> 검증 -> 추론 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | WordPiece 토큰화와 마스킹 | mask 15% 원칙 |
| 2 | Transformer Encoder 학습 | validation loss, MLM accuracy |
| 3 | 업무별 fine-tuning | F1, EM, accuracy |
| 4 | 추론 최적화 | p95 지연, GPU/CPU 사용률 |

> 요약: BERT는 MLM 사전학습으로 문맥 표현을 얻고, 업무별 출력층을 붙여 fine-tuning한 뒤 지연시간과 정확도를 함께 검증한다.

---

## Ⅳ. 특징

| 구분 | 내용 | 판단 포인트 |
|:---|:---|:---|
| 장점 | 양방향 문맥 표현으로 다의어 구분 | NER F1 0.85 이상 목표 |
| 한계 | 512 토큰 길이와 Encoder 추론 비용 | 긴 문서 분할·DistilBERT 검토 |
| 비교 대상 | GPT는 생성, BERT는 이해·추출 | 분류/NER/QA 업무 여부 |

> 요약: BERT는 이해 중심 업무에서 강점을 가지며, 생성·장문 처리 요구가 있으면 GPT·Longformer·RAG와 비교해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Word2Vec+BiLSTM | BERT Encoder fine-tuning | 라벨 데이터 1만건 이하 |
| 비용/성능 | CPU 추론 용이, 문맥 표현 제한 | GPU 추론, F1 +0.03 이상 목표 | p95 100ms 이하 요구 여부 |
| 운영/위험 | 모델 구조 단순 | 버전·토큰화·편향 관리 필요 | 모델 카드와 재현성 확보 |

> 요약: 문맥 이해 품질이 우선이면 BERT를 선택하고, 지연시간 제약이 크면 DistilBERT·ALBERT·ONNX 최적화를 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 장문 손실 | 512 토큰 제한 | sliding window, Longformer 검토 | truncation rate 5% 이하 |
| 추론 비용 | 110M parameter | distillation, quantization INT8 | p95 지연 100ms 이하 |
| 편향·오분류 | 사전학습 말뭉치 편향 | 편향 평가셋, human review | class별 F1 편차 0.05 이하 |

> 요약: BERT 도입 위험은 길이 제한·추론 비용·편향이며, 분할·경량화·평가셋으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정확도 | 분류 F1 0.85 이상, QA EM 70% 이상 | holdout test |
| 성능/비용 | p95 100ms 이하, GPU 사용률 60~80% | APM, Triton metrics |
| 운영/보안 | 모델·데이터 버전, 개인정보 마스킹 | MLflow, DLP 점검 |

> 요약: BERT 운영은 정확도·추론 지연·데이터 통제를 동시에 만족해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 한국어 업무는 KoBERT·KLUE-BERT를 후보로 두고, 라벨 5,000건 이상 검증셋에서 F1 0.85 이상을 승인 기준으로 둠
2. 운영 배포는 ONNX Runtime 또는 TensorRT, INT8 quantization으로 p95 100ms 이하를 측정함
3. 512 토큰 초과 문서는 chunk 384, stride 128 sliding window로 처리하고 truncation rate 5% 이하를 점검함

**결론 (2줄):**
- 기술사 판단: 분류·NER·추출형 QA는 BERT 계열, 생성·요약·대화는 GPT 계열을 선택함
- 향후 방향: BERT는 경량화·도메인 사전학습·검색 결합으로 기업 NLP 이해 계층에 계속 사용됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | MLM 사전학습과 fine-tuning 흐름 | Word2Vec·BERT·GPT 차이 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | 업무별 head와 추론 최적화 | 길이 제한·지연시간·정확도 선택 기준 |

> 요약: 설명형은 BERT 구조와 사전학습 원리, 요구사항형은 업무 적합성과 운영 제약 중심으로 작성한다.
