+++
title = "140. Self-Attention·Multi-Head·Positional Encoding 상세"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self-Attention은 <strong>시퀀스 내 모든 위치 쌍의 관련도를 계산</strong>하는 메커니즘이고, Multi-Head는 <strong>h개의 독립 Attention을 병렬 수행</strong>하여 다양한 관점의 패턴을 학습하며, Positional Encoding은 <strong>순서 정보를 주입</strong>한다.
> 2. **가치**: RNN은 순차 처리로 위치 정보가 자연 반영되지만, Transformer는 **순서 정보가 없으므로** Positional Encoding(사인/코사인 또는 학습)으로 위치를 알려줘야 하며, 이를 통해 긴 시퀀스의 장거리 의존성을 효율적으로 포착한다.
> 3. **판단 포인트**: head 수(h=8~96)·d_model(512~4096)이 핵심 하이퍼파라미터이며, RoPE(Rotary Positional Encoding)가 LLM의 표준 위치 인코딩으로 자리잡았다.

---

## Ⅰ. 개요 및 필요성

Transformer가 등장하기 전, 시퀀스 데이터를 처리하는 주력 모델은 RNN(순환 신경망)이었다. RNN은 입력을 하나씩 순차적으로 처리하므로 이전 토큰의 정보가 다음 토큰으로 자연스럽게 전달된다. 그러나 시퀀스가 길어질수록 초기 정보가 점차 희석되는 <strong>장거리 의존성(Long-Range Dependency) 문제</strong>가 발생하며, 순차 처리 특성상 병렬화가 불가능하여 학습 속도에 한계가 있다.

Vaswani 등(2017)이 제안한 Transformer는 이 한계를 **Self-Attention** 메커니즘으로 돌파했다. Self-Attention은 시퀀스 내 임의의 두 위치 사이의 관계를 단 한 번의 연산으로 직접 계산할 수 있으므로, 위치 간 거리와 무관하게 장거리 의존성을 포착한다. 그러나 Transformer는 입력 토큰을 동시에(병렬로) 처리하기 때문에 **순서 정보를 내재적으로 가지지 않는다**. 이 문제를 해결하는 것이 Positional Encoding(위치 인코딩)이다.

Self-Attention·Multi-Head Attention·Positional Encoding은 Transformer의 3대 핵심 구성 요소이며, GPT·BERT·T5·LLaMA 등 현대 대형 언어 모델(LLM) 전반의 기반이다.

- **📢 섹션 요약 비유**: Transformer는 <strong>책의 모든 단어를 동시에 읽는 독자</strong>다. 하지만 동시에 읽으니 순서를 모른다. Positional Encoding은 각 단어에 **"나는 3번째 단어야"라고 번호표를 붙이는** 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Self-Attention 수식

Self-Attention의 핵심 수식은 다음과 같다:

```
Attention(Q, K, V) = softmax( Q·Kᵀ / √d_k ) · V
```

| 행렬 | 의미 | 생성 방법 |
|:---|:---|:---|
| **Q (Query)** | 찾는 정보 | 입력 × Wq |
| **K (Key)** | 정보 키워드 | 입력 × Wk |
| **V (Value)** | 실제 정보 값 | 입력 × Wv |
| **√d_k** | 스케일링 | 기울기 폭발 방지 |

Self-Attention에서는 Q=K=V가 같은 입력 시퀀스에서 생성된다. 이로써 "이 단어가 같은 문장의 다른 단어와 얼마나 관련있는가?"를 스스로(Self) 계산한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">단계별 계산 흐름</div></div>
<div class="kb-diagram-note">입력 토큰 X</div>
<div class="kb-diagram-tree-item" style="--depth:2">×Wq ──→ Q (Query 행렬)</div>
<div class="kb-diagram-tree-item" style="--depth:2">×Wk ──→ K (Key 행렬)</div>
<div class="kb-diagram-tree-item" style="--depth:2">×Wv ──→ V (Value 행렬)</div>
<div class="kb-diagram-note">Q·Kᵀ / √d_k ← 유사도 점수</div>
<div class="kb-diagram-note">softmax() ← 확률로 정규화</div>
<div class="kb-diagram-note">× V ← 가중합 (최종 출력)</div>
</div>
</div>



### 2. Multi-Head Attention

단일 Attention은 하나의 관점으로만 관계를 본다. Multi-Head Attention은 <strong>h개의 독립적인 Attention Head를 병렬로 수행</strong>하여 다양한 관점(문법·의미·대명사 참조 등)을 동시에 학습한다.

```
MultiHead(Q, K, V) = Concat(head₁, head₂, ..., headₕ) × Wₒ

여기서 headᵢ = Attention(Q×Wqᵢ, K×Wkᵢ, V×Wvᵢ)
```

| 파라미터 | GPT-2 | GPT-3 | LLaMA-2 70B |
|:---|:---|:---|:---|
| **d_model** | 768 | 12,288 | 8,192 |
| **h (head 수)** | 12 | 96 | 64 |
| **d_k = d_model/h** | 64 | 128 | 128 |
| **레이어 수** | 12 | 96 | 80 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Multi-Head 구조</div></div>
<div class="kb-diagram-note">입력 X</div>
<div class="kb-diagram-tree-item" style="--depth:1">Head₁: Attention(XWq₁, XWk₁, XWv₁)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Head₂: Attention(XWq₂, XWk₂, XWv₂)</div>
<div class="kb-diagram-tree-item" style="--depth:1">...</div>
<div class="kb-diagram-tree-item" style="--depth:1">Headₕ: Attention(XWqₕ, XWkₕ, XWvₕ)</div>
<div class="kb-diagram-note">Concat → ×Wₒ → 출력</div>
</div>
</div>



각 Head는 서로 다른 <strong>관점(Attention Pattern)</strong>을 학습한다:
- Head 1: 문법적 의존 관계(주어-동사)
- Head 2: 대명사 해소(he/she가 누구를 지칭)
- Head 3: 의미적 유사성
- Head 4: 위치 기반 관계 등

**📢 섹션 요약 비유**: Multi-Head는 <strong>여러 탐정이 동시에 다른 관점으로 조사</strong>하는 것이다. 한 탐정은 지문, 다른 탐정은 CCTV, 또 다른 탐정은 목격자를 각각 담당하여 종합 판단한다.

### 3. Positional Encoding 방식 비교

| 방식 | 수식 | 특징 | 사용 모델 |
|:---|:---|:---|:---|
| **Sinusoidal** | PE(pos,2i)=sin(pos/10000^(2i/d)) | 고정, 외삽 어려움 | 원본 Transformer |
| **학습형 PE** | 임베딩 학습 | 학습 데이터 의존 | BERT, GPT-1/2 |
| **RoPE** | 회전 행렬로 상대 위치 인코딩 | 외삽 가능, LLM 표준 | LLaMA, Mistral |
| **ALiBi** | Attention 점수에 선형 바이어스 | 추가 파라미터 없음 | MPT, BLOOM |
| **YaRN** | RoPE 확장 (긴 컨텍스트) | 128K+ 컨텍스트 지원 | Mistral 긴 컨텍스트 |

<strong>RoPE(Rotary Positional Encoding)</strong>의 핵심 아이디어:
- 절대 위치 대신 <strong>두 토큰 사이의 상대적 거리</strong>를 회전 행렬로 인코딩
- Q·K 내적 계산 시 자연스럽게 상대 위치 정보가 반영됨
- 학습 길이보다 긴 시퀀스에도 어느 정도 일반화(외삽) 가능

```
[Sinusoidal PE 예시]
pos=0: [sin(0), cos(0), sin(0), cos(0), ...]
pos=1: [sin(1), cos(1), sin(0.01), cos(0.01), ...]
pos=2: [sin(2), cos(2), sin(0.02), cos(0.02), ...]

각 차원마다 다른 주기를 사용 → 위치별 고유 패턴
```

- **📢 섹션 요약 비유**: Sinusoidal PE는 <strong>지문</strong>과 같다. 같은 사람이어도 손가락마다 패턴이 달라 고유하게 식별된다. RoPE는 <strong>나침반</strong>이다. 절대 위치가 아닌 상대적 방향으로 위치를 표현한다.

---

## Ⅲ. 비교 및 연결

### Self-Attention vs RNN vs CNN

| 항목 | Self-Attention | RNN/LSTM | CNN (1D) |
|:---|:---|:---|:---|
| **병렬 처리** | 가능 (전체 동시) | 불가 (순차) | 가능 (윈도우) |
| **장거리 의존성** | O(1) 거리 | O(n) 거리 | O(n/k) 거리 |
| **계산 복잡도** | O(n²·d) | O(n·d²) | O(n·k·d²) |
| **메모리** | O(n²) | O(n·d) | O(n·k·d) |
| **대표 모델** | Transformer | LSTM, GRU | TextCNN |

- n: 시퀀스 길이, d: 히든 차원, k: 커널 크기

### Attention 유형 비교

| 유형 | Q 출처 | K/V 출처 | 용도 |
|:---|:---|:---|:---|
| **Self-Attention** | 입력 X | 입력 X | 인코더, GPT 디코더 |
| **Cross-Attention** | 디코더 출력 | 인코더 출력 | 번역, seq2seq |
| **Causal Attention** | 입력 X | 입력 X (마스크) | GPT (자기회귀) |
| **Sparse Attention** | 일부 선택 | 일부 선택 | 긴 시퀀스 효율화 |

- **📢 섹션 요약 비유**: Self-Attention은 <strong>자기 반성</strong>이다(자신의 문장을 스스로 분석). Cross-Attention은 <strong>번역자</strong>다(외국어 원문을 보며 한국어를 생성). Causal Attention은 <strong>미래를 보지 않는 점쟁이</strong>다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **시퀀스 길이가 1K를 넘는가?** → Flash Attention 또는 Sparse Attention 적용 필요 (O(n²) 메모리 문제)
2. **긴 컨텍스트(32K+)가 필요한가?** → RoPE + YaRN/LongRoPE로 외삽 지원
3. **추론 속도가 중요한가?** → Multi-Query Attention(MQA) 또는 Grouped-Query Attention(GQA)으로 KV Cache 최소화
4. **도메인 특화 파인튜닝인가?** → LoRA로 Attention 가중치만 저랭크 업데이트

### 핵심 최적화 기법

| 기법 | 문제 해결 | 효과 |
|:---|:---|:---|
| **Flash Attention** | O(n²) 메모리 → IO-aware 분할 | 메모리 10배 절감 |
| **KV Cache** | 자기회귀 반복 계산 | 추론 속도 O(n)로 향상 |
| **GQA** | Multi-Head의 KV 중복 | KV Cache 8배 축소 |
| **Sliding Window** | 전체 Attention → 지역 윈도우 | O(n²)→O(n·w) |
| **RoPE + YaRN** | 고정 컨텍스트 길이 | 학습 길이 4~8배 외삽 |

### 안티패턴

- **d_model을 h로 나누어 떨어지지 않게 설정**: d_k = d_model/h가 정수여야 하므로 반드시 나누어 떨어지게 설계한다.
- **Positional Encoding 없이 Transformer 사용**: 순서 정보가 전혀 주입되지 않아 어순이 다른 문장을 동일하게 처리한다.
- **지나치게 많은 Head 수**: head 수가 많아도 d_k가 작아져 각 head의 표현력이 감소한다. 적절한 h와 d_model의 비율 유지 필요.
- **Flash Attention 없이 긴 시퀀스 처리**: 표준 Attention은 n²에 비례하는 GPU 메모리를 사용하므로 긴 시퀀스에서 OOM(Out of Memory) 발생.

- **📢 섹션 요약 비유**: 실무 Attention 설계는 <strong>악단 편성</strong>이다. 지휘자(d_model)가 몇 명인지, 악기 파트(head) 수는 몇 개인지, 각 파트 인원(d_k)이 충분한지 균형 있게 설계해야 한다.

---

## Ⅴ. 기대효과 및 결론

Self-Attention+Multi-Head+Positional Encoding은 <strong>Transformer의 3대 핵심 구성 요소</strong>로, 이를 통해 달성하는 주요 효과는 다음과 같다:

| 효과 | 정량적 수치 | 비고 |
|:---|:---|:---|
| **병렬 처리 가속** | RNN 대비 학습 10~100배 빠름 | GPU 활용 극대화 |
| **장거리 의존성** | 임의 길이 O(1) 포착 | RNN은 길이에 비례해 성능 저하 |
| **다양한 패턴 학습** | h개 관점 동시 학습 | 문법·의미·구조 동시 포착 |
| **컨텍스트 확장** | RoPE+YaRN으로 128K+ 지원 | 긴 문서·코드 처리 가능 |

Transformer 이후의 LLM 발전은 결국 <strong>더 효율적인 Attention 메커니즘</strong>을 만드는 여정이었다. Flash Attention은 메모리를 해결했고, GQA는 추론 속도를 개선했으며, RoPE·YaRN은 컨텍스트 길이 한계를 극복했다. 앞으로도 더 긴 컨텍스트, 더 적은 메모리, 더 빠른 추론을 위한 Attention 혁신은 계속될 것이다.

- **📢 섹션 요약 비유**: Self-Attention의 진화는 <strong>전화기의 진화</strong>와 같다. 유선 전화(RNN)→핸드폰(Transformer)→5G 스마트폰(Flash Attention+GQA)으로 더 빠르고 멀리, 더 많은 사람과 소통한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Self-Attention** | Q·K·V로 자기 참조 관련도 계산 |
| **Multi-Head Attention** | h개 독립 Attention 병렬 수행 |
| **Positional Encoding** | 순서 정보 임베딩에 주입 |
| **RoPE** | 회전 행렬 기반 상대 위치 인코딩, LLM 표준 |
| **Flash Attention** | IO-aware 분할로 메모리 최적화 |
| **GQA** | KV를 그룹으로 공유, 추론 가속 |
| **KV Cache** | 자기회귀 생성 시 이전 K/V 재활용 |
| **ALiBi** | 추가 파라미터 없는 위치 바이어스 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Sinusoidal PE (2017, 원본 Transformer)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">학습형 PE (2018, BERT) — 데이터로부터 위치 학습</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">RoPE (2021, Su et al.) — 회전 행렬, LLaMA 채택</div>
<div class="kb-diagram-tree-item" style="--depth:2">ALiBi (2021, Press et al.) — 바이어스 방식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">YaRN (2023) — RoPE 외삽 확장 (32K→128K)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현재: LongRoPE / LongContext Scaling (2024~)</div>
<div class="kb-diagram-note">— 100만 토큰 컨텍스트 지원 목표</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Multi-Head는 <strong>여러 탐정</strong>이에요. 각각 다른 관점으로 <strong>동시에 조사</strong>하여 더 정확한 결론을 내려요.
2. Positional Encoding은 <strong>번호표</strong>예요. "이 단어는 <strong>3번째</strong>입니다"라고 Transformer에게 알려줘요.
3. 번호표가 없으면 AI가 **순서를 모르니까** "나는 사과를 먹었다"와 "사과는 나를 먹었다"를 같은 문장으로 이해해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 140 / 258

← **이전**: [139. Transformer 아키텍처 - Self-Attention 기반 병렬 처리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/139_transformer_architecture_self_attention/)
**다음**: [141. BERT Encoder - MLM 양방향 사전 학습 상세](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/141_bert_encoder_mlm_bidirectional/) →

---
