+++
title = "142. GPT Decoder - 자기회귀 생성 모델 상세"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GPT Decoder는 <strong>Transformer Decoder에서 Masked Self-Attention(Causal Mask)을 사용</strong>하여 왼쪽→오른쪽 방향으로만 문맥을 참조하며 다음 토큰을 예측(CLM, Causal Language Modeling)하는 자기회귀(Autoregressive) 생성 모델이다.
> 2. **가치**: BERT(양방향)는 생성이 불가능하지만, GPT(단방향)는 <strong>토큰을 하나씩 순차 생성</strong>하여 텍스트·코드·대화를 자연스럽게 만들어낸다. 생성 시 Temperature·Top-k·Top-p로 다양성을 제어한다.
> 3. **판단 포인트**: KV Cache로 이전 토큰의 Key·Value를 재사용하여 <strong>추론 속도를 O(n²)→O(n)으로 최적화</strong>하며, Speculative Decoding이 추가 가속 기법이다.

---

## Ⅰ. 개요 및 필요성

2018년 OpenAI가 발표한 GPT(Generative Pre-trained Transformer)는 Transformer 아키텍처의 <strong>Decoder 부분만</strong>을 사용하여 대규모 텍스트 코퍼스에 자기회귀(Autoregressive) 방식으로 사전 학습한 언어 모델이다. 같은 해 등장한 BERT가 양방향(Bidirectional) Encoder를 사용하여 이해(Understanding) 태스크에 특화된 반면, GPT는 단방향(Unidirectional) Decoder를 사용하여 생성(Generation) 태스크에 특화되었다.

자기회귀 생성이란 <strong>이전에 생성한 토큰들을 문맥으로 삼아 다음 토큰을 예측하는 방식</strong>이다. "나는 학교에"까지 생성했다면, 이 5개 토큰 전체를 문맥으로 사용하여 다음 토큰 "갔다"를 예측한다. 이 과정을 종료 토큰(EOS) 또는 최대 길이에 도달할 때까지 반복한다. 단순하지만 강력한 이 패러다임이 GPT-2→GPT-3→GPT-4, LLaMA, Mistral 등 현대 LLM의 근간이다.

핵심 학습 목표는 <strong>CLM(Causal Language Modeling)</strong>이다:
```
P(w₁, w₂, ..., wₙ) = ∏ P(wₜ | w₁, w₂, ..., wₜ₋₁)
```
즉, 이전 토큰들의 조건부 확률로 다음 토큰을 예측한다.

- **📢 섹션 요약 비유**: GPT는 <strong>릴레이 소설</strong>이다. 앞 주자가 쓴 내용만 보고 다음 문장을 이어 쓴다. 미래 문장은 아직 쓰이지 않았으므로 볼 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. GPT Decoder 구조

GPT는 Transformer의 Decoder를 N번 쌓은 구조지만, 원본 Transformer와 달리 **Cross-Attention 레이어가 없다** (인코더가 없으므로). 각 Decoder 레이어는 다음으로 구성된다:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">GPT Decoder 레이어 구조</div></div>
<div class="kb-diagram-note">토큰 임베딩 + 위치 인코딩(RoPE)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Masked Self-Attention ← Causal Mask 적용</div>
<div class="kb-diagram-note">Add &amp; LayerNorm</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Feed-Forward Network (FFN)</div>
<div class="kb-diagram-note">Add &amp; LayerNorm</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">다음 레이어 또는 출력</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Linear Projection → Softmax → 다음 토큰 확률</div>
</div>
</div>



### 2. Causal Mask (인과 마스크)

Causal Mask는 <strong>미래 토큰에 대한 Attention을 강제로 -∞(또는 음수 무한대)로 설정</strong>하여 softmax 후 0이 되게 한다. 이로써 각 위치는 자신과 왼쪽(과거) 토큰만 참조할 수 있다.

```
[Causal Mask 예시: "나는 학교에 갔다" (4토큰)]

Attention Score Matrix:
      나는  학교에  갔다   EOS
나는  [ 1    -∞    -∞    -∞  ]
학교에 [ 1     1    -∞    -∞  ]
갔다  [ 1     1     1    -∞  ]
EOS   [ 1     1     1     1  ]

1 = Attention 허용, -∞ = 마스크(미래 참조 차단)
```

이를 <strong>삼각 하행 마스크(Lower Triangular Mask)</strong>라고도 부른다.

### 3. KV Cache (키-값 캐시)

자기회귀 생성 시, 매 토큰마다 이전 모든 토큰을 다시 계산하면 O(n²) 비용이 든다. KV Cache는 <strong>이전 토큰들의 Key·Value 행렬을 캐시에 저장하고 재사용</strong>하여 각 생성 단계를 O(n) 비용으로 줄인다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">KV Cache 동작</div></div>
<div class="kb-diagram-note">Step 1: "나는" 생성</div>
<div class="kb-diagram-note">→ K₁, V₁ 계산 후 캐시에 저장</div>
<div class="kb-diagram-note">Step 2: "학교에" 생성</div>
<div class="kb-diagram-note">→ K₂, V₂ 계산 + 캐시에서 K₁, V₁ 불러옴</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">K₁,K₂</div><div class="kb-diagram-note">, V=</div><div class="kb-diagram-node">V₁,V₂</div><div class="kb-diagram-note">로 Attention 계산</div></div>
<div class="kb-diagram-note">→ 새로운 K₂, V₂만 추가로 캐시 저장</div>
<div class="kb-diagram-note">Step n: n번째 토큰 생성</div>
<div class="kb-diagram-note">→ 새 Kₙ, Vₙ만 계산하면 됨 (이전은 캐시)</div>
</div>
</div>



| 항목 | KV Cache 없음 | KV Cache 있음 |
|:---|:---|:---|
| **계산 복잡도** | O(n²) | O(n) |
| **메모리** | 적음 | O(n·레이어·h·d_k) |
| **속도** | 토큰마다 전체 재계산 | 증분 계산 |
| **사용 상황** | 학습 시 | 추론 시 |

### 4. 디코딩 전략

생성 시 어떤 토큰을 선택하느냐에 따라 결과가 달라진다:

| 전략 | 방법 | 특징 | 사용 상황 |
|:---|:---|:---|:---|
| **Greedy** | 매 단계 최고 확률 토큰 선택 | 결정론적, 단조로움 | 빠른 테스트 |
| **Beam Search** | 상위 B개 후보 유지 | 고품질, 느림 | 번역, 요약 |
| **Top-k** | 상위 k개 토큰 중 샘플링 | 다양성 제어 | 창의적 생성 |
| **Top-p (Nucleus)** | 누적 확률 p 이내 샘플링 | 동적 후보 크기 | 대화, 스토리 |
| **Temperature** | 확률 분포 조정 | T<1: 보수적, T>1: 창의적 | 모든 샘플링 |

**Temperature 효과**:
```
logit(wᵢ) / T → softmax

T = 0.0: Greedy와 동일 (가장 높은 확률만)
T = 0.7: 보수적, 일관성 높음
T = 1.0: 원래 분포 그대로
T = 1.5: 창의적, 예상치 못한 출력
T = 2.0+: 무작위성 매우 높음
```

**Top-p(Nucleus Sampling) 예시**:
```
확률 분포: [가: 0.4, 나: 0.3, 다: 0.2, 라: 0.07, 마: 0.03]
p = 0.9 설정 시:
  - 누적 0.4+0.3+0.2 = 0.9 → 가, 나, 다 중에서 샘플링
  - 라, 마는 후보에서 제외
```

- **📢 섹션 요약 비유**: 디코딩 전략은 <strong>답안 선택 방식</strong>이다. Greedy는 무조건 가장 자신 있는 답, Beam Search는 여러 답안을 동시에 검토, Top-p는 어느 정도 확신하는 답 중 무작위 선택.

---

## Ⅲ. 비교 및 연결

### GPT(Decoder) vs BERT(Encoder)

| 항목 | GPT (Decoder-only) | BERT (Encoder-only) |
|:---|:---|:---|
| **학습 목표** | CLM (다음 토큰 예측) | MLM (마스크 토큰 복원) |
| **Attention 방향** | 단방향 (왼→오) | 양방향 (좌우 모두) |
| **생성 가능 여부** | 가능 | 불가 |
| **이해 태스크** | 가능 (긴 프롬프트) | 매우 강함 |
| **대표 모델** | GPT-4, LLaMA, Mistral | BERT, RoBERTa, DeBERTa |
| **파인튜닝 방식** | 프롬프트/RLHF/LoRA | 분류 헤드 추가 |

### GPT 세대별 비교

| 모델 | 연도 | 파라미터 | 특징 |
|:---|:---|:---|:---|
| **GPT-1** | 2018 | 117M | Transformer Decoder 최초 대규모 사전 학습 |
| **GPT-2** | 2019 | 1.5B | Few-shot 가능성 확인 |
| **GPT-3** | 2020 | 175B | In-Context Learning, API 서비스 |
| **ChatGPT** | 2022 | 미공개 | RLHF(인간 피드백 강화학습) |
| **GPT-4** | 2023 | 미공개 | 멀티모달(이미지+텍스트) |
| **LLaMA-2** | 2023 | 7~70B | 오픈소스, RoPE, GQA |

- **📢 섹션 요약 비유**: BERT와 GPT는 <strong>독서법의 차이</strong>다. BERT는 책 전체를 동시에 읽어 이해하지만 요약 작성은 못한다. GPT는 앞 내용을 보며 다음 줄을 직접 써 나간다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **텍스트 분류/감성 분석이 목적인가?** → BERT 계열이 더 적합 (양방향 이해)
2. **텍스트 생성/대화가 목적인가?** → GPT Decoder 계열 필수
3. **추론 지연(Latency)이 중요한가?** → KV Cache + GQA + Speculative Decoding 적용
4. **생성 다양성이 중요한가?** → Temperature 조정, Top-p 샘플링 활용
5. **긴 컨텍스트(32K+)가 필요한가?** → RoPE + YaRN 지원 모델 선택
6. **온프레미스 배포가 필요한가?** → LLaMA-2/Mistral 오픈소스 + vLLM 서빙

### Speculative Decoding (투기적 디코딩)

LLM의 자기회귀 생성은 토큰 하나씩 순차 생성하므로 느리다. Speculative Decoding은 이를 가속하는 기법이다:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Speculative Decoding 흐름</div></div>
<div class="kb-diagram-note">1. 작은 Draft 모델(7B)이 k개 토큰을 빠르게 생성</div>
<div class="kb-diagram-note">예: "나는 학교에 갔다가" (5개 토큰 한 번에)</div>
<div class="kb-diagram-note">2. 큰 Target 모델(70B)이 k개 토큰을 병렬 검증</div>
<div class="kb-diagram-tree-item" style="--depth:1">수용(Accept): Draft와 Target 분포가 유사 → 그대로 사용</div>
<div class="kb-diagram-tree-item" style="--depth:1">거부(Reject): 분포 불일치 → 해당 위치부터 Target으로 재생성</div>
<div class="kb-diagram-note">3. 평균 2~3배 가속 (Target 모델 품질 유지하며)</div>
</div>
</div>



### 안티패턴

- **Temperature=0으로만 사용**: Greedy 생성으로 매우 단조로운 출력. 창의적 태스크에는 0.7~1.0 권장.
- **KV Cache 미적용 배포**: 토큰마다 전체를 재계산하여 추론 속도가 수십 배 느려짐.
- **무한 생성 방지 미설정**: EOS 토큰 처리 및 max_new_tokens 제한 없이 배포하면 무한 루프 발생.
- **배치 처리 시 패딩 미처리**: 가변 길이 시퀀스를 배치로 묶을 때 패딩 마스크 미적용 시 정확도 저하.

- **📢 섹션 요약 비유**: KV Cache 없는 GPT 추론은 **책을 읽을 때마다 처음부터 다시 읽는** 것이다. KV Cache는 <strong>읽은 페이지를 책갈피로 표시</strong>하여 이어서 읽는다.

---

## Ⅴ. 기대효과 및 결론

GPT Decoder 아키텍처가 가져온 실질적 효과:

| 효과 | 내용 | 대표 사례 |
|:---|:---|:---|
| **범용 텍스트 생성** | 문맥에 맞는 자연스러운 텍스트 생성 | ChatGPT 대화 |
| **코드 생성** | 자연어 설명으로 코드 자동 작성 | GitHub Copilot |
| **In-Context Learning** | 파인튜닝 없이 예시만으로 태스크 수행 | GPT-3 이후 |
| **RLHF 정렬** | 인간 선호에 맞는 출력 생성 | ChatGPT, Claude |
| **멀티모달 확장** | 이미지+텍스트 동시 이해·생성 | GPT-4V, LLaVA |

GPT Decoder는 <strong>현대 생성형 AI의 사실상 표준 아키텍처</strong>이다. 단방향 Attention과 자기회귀 생성이라는 단순한 원리가 충분히 큰 모델 크기·데이터·컴퓨팅과 결합될 때 놀라운 emergent ability(창발 능력)를 발휘한다. KV Cache·Speculative Decoding·GQA 등 추론 최적화 기법의 발전으로 서빙 비용도 지속적으로 낮아지고 있다.

- **📢 섹션 요약 비유**: GPT의 발전은 <strong>1인 밴드에서 오케스트라로</strong>의 진화다. 초기에는 단순히 다음 단어를 예측하는 1인 밴드였지만, 규모가 커지며 추론·창작·코딩을 모두 수행하는 오케스트라로 성장했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Causal Mask** | 미래 토큰 참조 차단, 삼각 하행 마스크 |
| **CLM** | 다음 토큰 예측으로 사전 학습 |
| **KV Cache** | Key·Value 재사용으로 추론 O(n) 달성 |
| **Temperature** | 생성 다양성 조정 (T<1: 보수, T>1: 창의) |
| **Top-p Sampling** | 누적 확률 기반 동적 후보 선택 |
| **Speculative Decoding** | Draft+Target 이중 모델로 2~3배 가속 |
| **GQA** | KV Head 그룹화로 캐시 메모리 절감 |
| **RLHF** | 인간 피드백으로 정렬(Alignment) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">GPT-1 (2018, 117M) — Decoder-only 사전 학습</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">GPT-2 (2019, 1.5B) — 제로샷 능력 확인</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">GPT-3 (2020, 175B) — In-Context Learning 확립</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">InstructGPT / ChatGPT (2022) — RLHF 정렬</div>
<div class="kb-diagram-tree-item" style="--depth:2">KV Cache 최적화 (2021~)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Flash Attention (2022)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Speculative Decoding (2023)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">GPT-4 / LLaMA-2 / Mistral (2023)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현재: Medusa/Eagle — 다중 토큰 동시 생성</div>
<div class="kb-diagram-note">Mamba — Attention-free 대안 모델</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. GPT는 <strong>릴레이 소설</strong>이에요. 앞 내용만 보고 **다음 문장을 써요**.
2. 뒤 내용은 **아직 없으니까** 볼 수 없어요 (Causal Mask).
3. KV Cache는 <strong>이미 쓴 부분을 기억</strong>해서 매번 처음부터 읽지 않아도 돼요. 더 빨리 쓸 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 258

← **이전**: [141. BERT Encoder - MLM 양방향 사전 학습 상세](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/141_bert_encoder_mlm_bidirectional/)
**다음**: [143. Foundation Model & LLM 사전 학습 - 기반 모델의 원리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/143_foundation_model_llm_pretraining/) →

---
