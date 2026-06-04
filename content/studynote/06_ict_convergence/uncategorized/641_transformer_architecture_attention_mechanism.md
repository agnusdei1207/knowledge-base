+++
title = "641. 트랜스포머 아키텍처 어텐션 메커니즘 (Transformer Architecture Attention Mechanism)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜스포머는 순환 구조 대신 self-attention으로 토큰 간 관계를 한 번에 계산하여 문맥을 병렬 처리하는 신경망 아키텍처다.
> 2. **가치**: 긴 문맥, 병렬 학습, 전이학습이 가능해져 번역, 검색, 요약, 코드 생성, 멀티모달 AI의 공통 기반이 되었다.
> 3. **판단 포인트**: attention은 표현력은 높지만 길이에 대해 계산량과 메모리가 커진다. 모델 품질, 컨텍스트 길이, 추론 비용의 균형이 핵심이다.

---

## I. 개요 및 필요성

RNN과 LSTM은 순서대로 토큰을 처리하므로 긴 문장의 의존관계를 학습하기 어렵고 병렬화 효율이 낮았다. 트랜스포머는 문장 안의 모든 토큰이 서로를 바라보는 self-attention을 사용하여 이 문제를 해결했다. `Attention is All You Need` 이후 BERT, GPT, T5, Vision Transformer 같은 모델들이 같은 원리를 확장했다.

```text
[Transformer Block]

Input Tokens
    |
    v
Embedding + Position
    |
    v
+----------------------+
| Multi-Head Attention |
+----------------------+
    |
    v
Add & Norm
    |
    v
+----------------------+
| Feed Forward Network |
+----------------------+
    |
    v
Add & Norm -> Output
```

---

## II. 아키텍처 및 핵심 원리

Self-attention은 각 토큰을 `Query`, `Key`, `Value`로 변환한 뒤 토큰 간 관련도를 계산한다.

```text
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
```

| 구성 요소 | 역할 | 설명 |
| :--- | :--- | :--- |
| Token Embedding | 단어/토큰을 벡터로 변환 | 의미 공간의 좌표로 표현 |
| Positional Encoding | 순서 정보 부여 | absolute, relative, rotary 방식 |
| Multi-Head Attention | 여러 관점의 관계 학습 | 문법, 참조, 의미 관계를 분리 학습 |
| Feed Forward Network | 토큰별 비선형 변환 | 모델 용량의 큰 부분을 차지 |
| Residual + LayerNorm | 안정적 학습 | 깊은 네트워크의 gradient 흐름 유지 |

Encoder는 양방향 문맥 이해에 적합하고, Decoder는 다음 토큰 생성을 위한 causal mask를 사용한다. BERT는 encoder 중심, GPT는 decoder 중심, T5는 encoder-decoder 구조다.

---

## III. 비교 및 연결

| 구분 | RNN/LSTM | Transformer |
| :--- | :--- | :--- |
| 처리 방식 | 순차 처리 | 병렬 처리 |
| 장기 의존성 | 제한적 | attention으로 직접 연결 |
| 학습 효율 | 낮음 | 높음 |
| 계산 복잡도 | 길이에 선형적 | 기본 attention은 길이 제곱 |
| 대표 활용 | 시계열, 초기 NLP | LLM, 번역, 검색, 비전 |

트랜스포머는 NLP를 넘어 이미지 패치, 음성 프레임, 단백질 서열, 로그 이벤트 등 순서가 있거나 관계가 있는 데이터를 처리하는 범용 아키텍처로 확장되었다.

---

## IV. 실무 적용 및 기술사 판단

### 판단 체크리스트

- 입력 길이와 attention 메모리 비용을 산정했는가?
- 사전학습 모델을 그대로 쓸지, 파인튜닝/어댑터/프롬프트 튜닝을 쓸지 결정했는가?
- 추론 지연시간, GPU 메모리, 배치 크기를 함께 최적화했는가?
- 도메인 데이터의 편향과 개인정보 위험을 검토했는가?
- 설명 가능성, 안전성, 모니터링 지표를 정의했는가?

### 피해야 할 안티패턴

- attention 구조를 이해하지 않고 모델 크기만 키우는 접근
- 컨텍스트 길이를 늘리면서 비용과 지연시간을 계산하지 않는 경우
- 학습 데이터 품질보다 하이퍼파라미터 튜닝에만 집중하는 경우

---

## V. 기대효과 및 결론

트랜스포머의 핵심은 모든 토큰 간 관계를 명시적으로 학습하는 attention에 있다. 기술사 답안에서는 수식, 구조, RNN 대비 차이, 계산 비용, 실무 최적화 포인트를 함께 제시해야 한다.

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Self-Attention | 토큰 간 관계 계산 |
| Multi-Head | 여러 관계 공간을 병렬 학습 |
| Positional Encoding | 순서 정보 보완 |
| BERT | 양방향 encoder 모델 |
| GPT | causal decoder 생성 모델 |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 641 / 800

<- **이전**: [640. 이벤트 드리븐 아키텍처 EventBridge](/knowledge-base/studynote/06_ict_convergence/uncategorized/640_event_driven_architecture_eventbridge/)
**다음**: [642. GPT 대규모 언어 모델 사전 학습](/knowledge-base/studynote/06_ict_convergence/uncategorized/642_gpt_large_language_model_pre_training/) ->

---
