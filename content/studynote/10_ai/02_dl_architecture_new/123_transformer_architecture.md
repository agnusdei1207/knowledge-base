+++
title = "123. Transformer 아키텍처 - Self-Attention 기반 병렬 시퀀스 처리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 <strong>순환(RNN) 없이 Self-Attention만으로 시퀀스를 병렬 처리</strong>하는 아키텍처이며, "Attention Is All You Need"(Vaswani, 2017)에서 제안되어 현대 AI의 <strong>사실상 유일한 기반 아키텍처</strong>가 되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 <strong>병렬화 불가·장거리 의존성 약화</strong>라는 근본 한계가 있었으나, Transformer는 <strong>모든 위치를 동시에 참조(Self-Attention)</strong>하고 <strong>GPU 병렬화가 가능</strong>하여 학습 속도와 성능을 혁신적으로 개선했다.
> 3. **판단 포인트**: **인코더-디코더 구조**(기계 번역), **인코더만**(BERT, 분류), **디코더만**(GPT, 생성)의 3가지 변형을 구분하고, Multi-Head Attention·Positional Encoding·Layer Normalization이 핵심 구성 요소이다.

---

## Ⅰ. 개요 및 필요성

2017년 이전까지 자연어 처리의 주류는 RNN(LSTM, GRU) 기반 모델이었다. 이 모델들은 시퀀스를 순차적으로 처리하여 GPU 병렬화가 불가능하고, 장거리 의존성(Long-range Dependency) 학습이 어렵다는 구조적 한계가 있었다.

Vaswani et al.(2017)은 "Attention Is All You Need"에서 RNN을 완전히 제거하고 Self-Attention 메커니즘만으로 시퀀스를 처리하는 Transformer를 제안했다. 핵심 혁신은 다음과 같다:

1. **완전 병렬화**: 모든 시간 단계를 동시에 처리 → GPU 활용률 극대화
2. **전역 의존성**: 거리에 관계없이 모든 위치를 직접 참조
3. **확장성**: 모델 크기를 늘리면 성능이 예측 가능하게 향상

Transformer는 NLP를 시작으로 Vision(ViT), Audio(Whisper), 멀티모달(GPT-4V, Gemini)로 적용 범위를 확대하여 현대 AI의 사실상 유일한 기반 아키텍처가 되었다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Transformer 전체 구조</div>
<div class="kb-diagram-note">입력 출력</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Positional</div><div class="kb-diagram-node">Positional</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Encoding + Emb</div><div class="kb-diagram-node">Encoding + Emb</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Encoder ×N</div><div class="kb-diagram-cell">Decoder ×N</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Multi-Head</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">Masked Multi-Head</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Self-Attn</div><div class="kb-diagram-cell">Self-Attn</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+ Add &amp; Norm</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+ Add &amp; Norm</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Cross-Attn</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Feed-Forward</div><div class="kb-diagram-cell">(Enc → Dec)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+ Add &amp; Norm</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+ Add &amp; Norm</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Feed-Forward</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">+ Add &amp; Norm</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Linear + Softmax</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">출력 토큰 확률</div>
</div>
</div>



- **📢 섹션 요약 비유**: RNN은 줄서기(순차 처리)이고, Transformer는 회의(모든 사람이 동시에 서로 참조, 병렬 처리)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 구성 요소 상세

| 구성 요소 | 역할 | 세부 설명 |
|:---|:---|:---|
| **Positional Encoding** | 순서 정보 주입 | sin/cos 또는 학습 벡터 |
| **Multi-Head Self-Attention** | 시퀀스 내 전역 참조 | h개 헤드로 다관점 병렬 처리 |
| **Add & Norm (Residual + LayerNorm)** | 깊은 네트워크 안정화 | 기울기 흐름 보장 |
| **Position-wise Feed-Forward** | 비선형 변환 | 2층 MLP (d→4d→d) |
| **Cross-Attention (디코더)** | 인코더 참조 | Q=디코더, K·V=인코더 |
| **Masked Self-Attention (디코더)** | 미래 토큰 차단 | 자기회귀 생성 |

### 인코더 블록 상세



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">인코더 블록 (×N, 원본 N=6):</div>
<div class="kb-diagram-note">입력 x</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">─ Multi-Head Self-Attention ─</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Q = K = V = x · W</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">head_i = Attn(Q_i, K_i, V_i)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MHA = Concat(heads) · W_O</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Add &amp; LayerNorm: x' = LayerNorm(x + MHA(x))</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">─ Position-wise FFN</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">FFN(x') = W₂·ReLU(W₁·x'+b₁)+b₂</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(d_model=512 → d_ff=2048 → 512)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Add &amp; LayerNorm: output = LayerNorm(x' + FFN(x'))</div>
</div>
</div>



### 디코더 블록 상세



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">디코더 블록 (×N):</div>
<div class="kb-diagram-note">입력 y (시프트된 출력)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">─ Masked Multi-Head Self-Attention ─</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">미래 토큰 마스킹</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(자기회귀: 과거 토큰만 참조)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Add &amp; LayerNorm</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">─ Cross-Attention</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Q = 디코더 은닉 상태</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">K = V = 인코더 출력</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(번역: 인코더 입력 참조)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Add &amp; LayerNorm</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Position-wise FFN</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Add &amp; LayerNorm → 출력</div>
</div>
</div>



### Transformer의 3가지 변형

| 변형 | 구성 | 대표 모델 | 주요 용도 |
|:---|:---|:---|:---|
| **인코더-디코더** | 둘 다 | T5, BART, 원본 Transformer | 기계 번역, 요약 |
| **인코더만** | 인코더 | **BERT, RoBERTa, DeBERTa** | 분류, NER, QA |
| **디코더만** | 디코더 | **GPT, LLaMA, Mistral** | 텍스트 생성 |

- **📢 섹션 요약 비유**: BERT는 독해 시험(양방향 이해), GPT는 작문 시험(왼→오 생성), T5는 둘 다 보는 종합 시험이다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | RNN / LSTM | Transformer |
|:---|:---|:---|
| **순차 처리** | 필수 | **필요 없음** |
| **병렬화** | 불가 | **가능 (O(n²) 메모리)** |
| **장거리 의존성** | 약함 (기울기 소실) | **강함 (직접 참조)** |
| **학습 속도** | 느림 | **빠름 (GPU 활용 극대화)** |
| **파라미터** | 적음 | **많음** |
| **추론 방식** | 순차 (낮은 지연) | **병렬 (학습) + 순차 (추론)** |
| **대표 모델** | LSTM, GRU | **BERT, GPT, T5** |

### 계산 복잡도 분석

- **Self-Attention**: O(n²·d) — 모든 쌍 비교 (n=시퀀스 길이, d=차원)
- **RNN**: O(n·d²) — 순차적이나 n에 선형
- 시퀀스가 짧으면 Self-Attention이 효율적, 길면 메모리 문제 발생 → Flash Attention으로 해결

- **📢 섹션 요약 비유**: Transformer는 모든 사원이 CEO에게 직접 보고하는 수평 조직이다. 정보 전달이 빠르지만 CEO(GPU 메모리)가 감당해야 할 정보량도 많다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Transformer 적용 태스크별 변형 선택



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">태스크 → 변형 선택 가이드</div>
<div class="kb-diagram-note">이해 중심 (분류·NER·QA):</div>
<div class="kb-diagram-note">→ BERT계 (인코더만, 양방향 Self-Attention)</div>
<div class="kb-diagram-note">예: RoBERTa, DeBERTa, Multilingual BERT</div>
<div class="kb-diagram-note">생성 중심 (번역·요약·대화):</div>
<div class="kb-diagram-note">→ GPT계 (디코더만, 자기회귀 생성)</div>
<div class="kb-diagram-note">예: LLaMA 2, Mistral, GPT-4</div>
<div class="kb-diagram-note">이해+생성 (번역, 질의응답 생성):</div>
<div class="kb-diagram-note">→ T5/BART계 (인코더-디코더)</div>
<div class="kb-diagram-note">예: T5, BART, mT5</div>
<div class="kb-diagram-note">임베딩 (검색, RAG):</div>
<div class="kb-diagram-note">→ Sentence-BERT, E5, BGE</div>
<div class="kb-diagram-note">예: 벡터 DB 인덱싱</div>
</div>
</div>



### 설계 판단 체크리스트

1. **생성 vs 이해 태스크인가?** → GPT vs BERT 계열 선택
2. **시퀀스 길이가 얼마인가?** → 긴 문서는 Flash Attention, Sliding Window 고려
3. **다국어 지원이 필요한가?** → mBERT, mT5, NLLB 고려
4. **추론 속도가 중요한가?** → KV-cache, GQA, 모델 압축 고려
5. **도메인 특화가 필요한가?** → LoRA 파인튜닝 계획

### 안티패턴

- **작은 데이터에 대형 Transformer**: 과적합 → 정규화·소형 모델 사용
- **Positional Encoding 없이 사용**: 어순 무시 → 성능 급저하
- **Layer Norm 위치 오해**: Pre-LN(현 표준) vs Post-LN(원본) 차이 이해 필요
- **KV-cache 미활용**: 추론 시 재계산 → 속도 10배 이상 저하

- **📢 섹션 요약 비유**: Transformer는 고성능 전기차다. 올바른 충전 방법(사용법)을 모르면 성능의 10%도 못 쓰고, 알면 내연기관(RNN)보다 10배 빠르다.

---

## Ⅴ. 기대효과 및 결론

### 도입 시 기대 효과

| 효과 항목 | 정량/정성 효과 |
|:---|:---|
| **학습 속도** | RNN 대비 3~10배 빠름 (GPU 병렬화) |
| **번역 품질** | BLEU score 기준 SOTA 달성 |
| **장거리 의존성** | 문서 전체 길이에 관계없이 직접 참조 |
| **전이 가능성** | NLP→Vision→Audio→Multimodal 확장 |
| **확장성** | 스케일링 법칙에 따른 예측 가능한 성능 향상 |

### 미래 전망

Transformer는 <strong>현대 AI의 단일 기반 아키텍처</strong>이며, NLP를 넘어 Vision·Audio·Multimodal까지 적용되어 AI 패러다임을 완전히 바꾸었다. 최근에는 Mamba(SSM 기반 선택적 상태 공간)와 같은 대안 아키텍처가 연구되고 있으나, Transformer는 당분간 지배적 위치를 유지할 것으로 전망된다.

- **📢 섹션 요약 비유**: Transformer는 인터넷이다. 도입 초기에는 이것이 세상을 바꿀지 몰랐지만, 지금은 모든 디지털 서비스의 인프라가 되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Self-Attention** | Transformer의 핵심 연산 |
| **Multi-Head Attention** | 다관점 병렬 Attention |
| **Positional Encoding** | 순서 정보 주입 |
| **BERT** | 인코더만 사용 (양방향) |
| **GPT** | 디코더만 사용 (자기 회귀) |
| **Flash Attention** | O(n²) 메모리 최적화 |
| **ViT** | Vision Transformer (이미지에 적용) |
| **Whisper** | Audio Transformer (음성 인식) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RNN / LSTM (순환, ~2016)</div>
<div class="kb-diagram-note">→ 순차 처리, 병렬화 불가</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Attention (Bahdanau, 2014)</div>
<div class="kb-diagram-note">→ 병목 해소, 가중 참조</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Transformer (Vaswani, 2017)</div>
<div class="kb-diagram-note">→ "Attention Is All You Need"</div>
<div class="kb-diagram-note">→ 완전 병렬화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BERT (2018) / GPT-2 (2019)</div>
<div class="kb-diagram-note">→ 사전 학습 혁명</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">GPT-3 (2020, 175B)</div>
<div class="kb-diagram-note">→ In-context Learning, Few-shot</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ChatGPT (2022) / GPT-4 (2023)</div>
<div class="kb-diagram-note">→ RLHF, 멀티모달</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: GPT-4o / Gemini / Claude</div>
<div class="kb-diagram-note">→ 더 큰 규모, 더 다양한 모달리티</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 <strong>줄서기</strong>예요. 앞 사람이 끝나야 다음 사람이 시작하니까 느려요.
2. Transformer는 <strong>회의</strong>예요. 모든 사람이 <strong>동시에 서로 이야기(Self-Attention)</strong>해서 빨라요.
3. ChatGPT, BERT, Gemini 모두 <strong>Transformer</strong>로 만들어졌답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 420

← **이전**: [122. Q·K·V 시스템 (Query·Key·Value) - Attention의 핵심 연산 구조](/knowledge-base/studynote/10_ai/02_dl_architecture_new/122_qkv_system/)
**다음**: [124. Self-Attention (자기 주의 메커니즘) - 시퀀스 내 모든 위치 상호 참조](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/) →

---
