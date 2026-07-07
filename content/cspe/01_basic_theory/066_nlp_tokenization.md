---
title: "자연어 처리 토크나이징 (NLP Tokenization)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 66
---

# 자연어 처리 토크나이징 (NLP Tokenization)

## 1. 개요

- **정의/개념**: 토크나이징은 자연어 문장을 모델이 처리할 수 있는 최소 단위인 토큰으로 분리하고, 이를 정수 ID로 변환하는 전처리 과정이다.
- **배경/필요성**: 자연어는 띄어쓰기, 형태소, 신조어, 다국어 특성이 복잡하므로 모델 입력 길이와 의미 단위를 안정적으로 만들 기준이 필요하다.

토크나이징은 단순 문자열 분리가 아니라 vocabulary, OOV, sequence length, 모델 호환성을 결정하는 입력 설계이다.

## 2. 특징 및 비교

| 구분 | Word Token | Morph Token | Subword Token |
|---|---|---|---|
| 단위 | 단어 | 형태소 | BPE, WordPiece 등 부분 단어 |
| 장점 | 직관적 | 한국어 등 교착어 처리 | OOV 완화 |
| 약점 | OOV 많음 | 분석기 의존 | 의미 단위가 덜 직관적 |
| 활용 | 단순 NLP | 형태소 기반 분석 | BERT, GPT 계열 |

선택 기준은 언어 특성, OOV 비율, vocabulary 크기, 모델 구조, 입력 길이 제한이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Normalization | 대소문자, 공백, 특수문자 정리 | 일관성 |
| Tokenizer Rule | 분리 기준 | 단어·형태소·subword |
| Vocabulary | 토큰-ID 매핑 | 모델 입력 |
| Special Token | CLS, SEP, PAD, UNK 등 | task 제어 |
| Sequence Length | 최대 입력 길이 | truncation/padding |

```text
문장 -> 정규화 -> 토큰 분리 -> ID 변환 -> padding/truncation -> 모델 입력
```

토큰화 정책이 바뀌면 vocabulary와 모델 입력이 달라지므로 학습·추론 파이프라인이 함께 맞아야 한다.

## 4. 문제점 및 개선방안

1. **OOV 문제**
   - 사전에 없는 단어가 많으면 의미 정보가 손실된다.
   - **개선방안**: subword tokenizer, vocabulary 확장, domain corpus 재학습을 적용한다.

2. **길이 증가**
   - subword 분할이 과도하면 입력 길이가 늘어 비용이 증가한다.
   - **개선방안**: max length, truncation 정책, tokenizer 품질을 검증한다.

3. **학습·추론 불일치**
   - 배포 환경 tokenizer가 학습 때와 다르면 결과가 크게 달라진다.
   - **개선방안**: tokenizer 버전 고정, vocabulary artifact 관리, 테스트 케이스를 운영한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 검색 | 질의와 문서를 같은 tokenizer로 처리 | 검색 정확도 |
| 챗봇 | 사용자 입력을 subword token으로 변환 | OOV 비율, latency |
| 한국어 분석 | 형태소 또는 subword 단위 선택 | 분절 품질, 모델 성능 |

## 6. 결론

토크나이징은 자연어를 모델 입력으로 바꾸는 첫 설계 단계이다. 언어 특성, OOV, vocabulary, 길이 제한, 학습·추론 일관성을 함께 판단해야 NLP 모델 성능과 운영 안정성이 이어진다.
