---
title: "GPT 언어 모델 (GPT Language Model)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 69
---

# GPT 언어 모델 (GPT Language Model)

## 1. 개요

- **정의/개념**: GPT는 Transformer decoder를 기반으로 이전 토큰 문맥에서 다음 토큰을 예측하도록 학습된 자기회귀 언어 모델이다.
- **배경/필요성**: 자연어 생성, 요약, 질의응답, 코드 생성처럼 문맥에 맞는 연속 텍스트를 생성하려면 대규모 언어 패턴을 학습한 생성 모델이 필요하다.

GPT의 핵심은 다음 토큰 예측이라는 단순한 학습 목표가 대규모 데이터와 모델 규모를 만나 범용 생성 능력으로 확장된다는 점이다.

## 2. 특징 및 비교

| 구분 | BERT | GPT |
|---|---|---|
| 구조 | Transformer Encoder | Transformer Decoder |
| 문맥 방향 | 양방향 | 이전 토큰 기반 자기회귀 |
| 강점 | 이해·분류 | 생성·대화·추론 보조 |
| 입력 방식 | fine-tuning 중심 | prompt, instruction, fine-tuning |
| 주요 위험 | 도메인 불일치 | hallucination, 비용, 보안 |

선택 기준은 생성 필요성, 문맥 길이, 정확성 요구, 비용, 검증 절차, 보안 통제이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Tokenizer | 텍스트를 토큰 ID로 변환 | 입력 단위 |
| Decoder Block | masked self-attention 기반 문맥 처리 | 자기회귀 |
| Next Token Objective | 다음 토큰 확률 예측 | 생성 학습 |
| Prompt/Instruction | 모델 행동을 유도하는 입력 | 품질 좌우 |
| Decoding Strategy | greedy, sampling, beam 등 | 다양성·정확성 |

```text
Prompt -> Tokenizer -> Decoder Blocks -> 다음토큰분포 -> Decoding -> Response
```

생성 결과는 확률적 디코딩과 프롬프트 조건에 좌우되므로, 출력 품질은 모델 자체뿐 아니라 운영 설계의 영향을 받는다.

## 4. 문제점 및 개선방안

1. **Hallucination**
   - 그럴듯하지만 사실과 다른 내용을 생성할 수 있다.
   - **개선방안**: RAG, 출처 검증, 사람 검토, 사실성 평가를 적용한다.

2. **보안·개인정보 위험**
   - 민감정보 입력, prompt injection, 데이터 유출 위험이 있다.
   - **개선방안**: 입력 필터링, 권한 분리, 민감정보 마스킹, 로그 정책을 운영한다.

3. **비용과 지연**
   - 큰 모델과 긴 문맥은 추론 비용과 응답 시간이 증가한다.
   - **개선방안**: 모델 크기 선택, 캐싱, context 압축, 라우팅 전략을 적용한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 문서 초안·요약 | 업무 문서를 요약하고 초안 생성 후 검토 | 수정률, 검토 시간 |
| 지식 검색 보조 | RAG로 내부 문서 기반 답변 생성 | 근거 일치율, 정확도 |
| 코드 보조 | 요구사항 기반 코드·테스트 초안 생성 | 결함률, 생산성 |

## 6. 결론

GPT는 자기회귀 Transformer decoder로 다음 토큰을 예측하며 텍스트를 생성하는 언어 모델이다. 디코더 구조, prompt, decoding, hallucination, 보안·비용 통제를 연결해 설명해야 생성형 AI의 활용 가치와 운영 위험이 함께 드러난다.
