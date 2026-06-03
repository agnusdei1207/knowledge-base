---
title: 140. Self-Attention·Multi-Head·Positional Encoding 상세
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self-Attention은 **시퀀스 내 모든 위치 쌍의 관련도를 계산**하는 메커니즘이고, Multi-Head는 **h개의 독립 Attention을 [[430_index_fast_full_scan|병렬]] 수행**하여 다양한 관점의 패턴을 학습하며, Positional Encoding은 **순서 정보를 주입**한다.
> 2. **가치**: RNN은 순차 처리로 위치 정보가 자연 반영되지만, Transformer는 **순서 정보가 없으므로** [[300_positional_encoding|Positional Encoding]](사인/코사인 or 학습)으로 위치를 알려줘야 한다.
> 3. **판단 포인트**: head 수(h=8~96)·d_model(512~4096)이 핵심 하이퍼파라미터이며, RoPE(Rotary PE)가 LLM의 표준 위치 인코딩이다.

---

## Ⅰ. 개요 및 필요성

```text
Self-Attention: Q=K=V (같은 시퀀스에서 생성)
Multi-Head: h개 Attention 병렬 → Concat → Linear
  d_k = d_model / h (예: 512/8 = 64)
Positional Encoding:
  사인/코사인 (고정) 또는 RoPE (회전, LLM 표준)
```

- **📢 섹션 요약 비유**: Multi-Head는 **여러 탐정이 동시에 다른 관점으로 조사**하는 것이다. 한 탐정보다 여러 탐정이 더 정확하다.

---

## Ⅱ~Ⅴ. 결론

[[124_self_attention|Self-Attention]]+Multi-Head+PE는 **Transformer의 3대 핵심 구성**이며, RoPE가 [[263_llm_large_language_model|LLM]] 위치 인코딩의 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[124_self_attention|Self-Attention]]** | 자기 [[316_reference_pattern_nosql|참조]] 관련도 |
| **Multi-Head** | 다관점 [[430_index_fast_full_scan|병렬]] |
| **[[300_positional_encoding|Positional Encoding]]** | 순서 정보 주입 |
| **RoPE** | 회전 위치 인코딩 |
| **ALiBi** | 위치 바이어스 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Sinusoidal PE (2017, 원본)] → [학습 PE (BERT)]
    → [RoPE (2021, LLaMA 표준)]
    → [ALiBi (2021, 학습 없이 위치)]
    → [현재: YaRN — RoPE 확장 (긴 컨텍스트)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Multi-Head는 **여러 탐정**이에요. 각각 다른 관점으로 **동시에 조사**해요.
2. Positional Encoding은 **번호표**예요. "이 단어는 **3번째**입니다" 알려줘요.
3. 번호표가 없으면 AI가 **순서를 모르니까** 문장을 이해 못 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 140 / 258

← **이전**: [[139_transformer_architecture_self_attention|139. Transformer 아키텍처 - Self-Attention 기반 병렬 처리]]
**다음**: [[141_bert_encoder_mlm_bidirectional|141. BERT Encoder - MLM 양방향 사전 학습 상세]] →

---
