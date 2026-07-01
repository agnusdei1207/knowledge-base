---
title: "트랜스포머 (Transformer)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 34
---

# 📖 【암기용】 개념 완전 이해

> 목적: Transformer를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: Self-Attention 메커니즘으로 시퀀스 전체를 병렬 처리하는 신경망 아키텍처
- **왜 필요한가**: RNN/LSTM은 순차 처리로 긴 시퀀스에서 기울기 소실·학습 속도 병목이 발생, 병렬화가 불가능했음.
- **핵심 직관**: 문장 전체를 한꺼번에 보고 각 단어가 다른 모든 단어와의 관계를 동시에 계산하는 구조임.

## 깊이 이해
- **배경·문제의식**: Vaswani et al.(2017) "Attention Is All You Need"에서 제안. RNN 기반 Seq2Seq은 시퀀스 길이 N에 O(N) 순차 단계가 필요하여 GPU 병렬화에 한계가 있었음.
- **작동 원리**: 입력을 임베딩+위치 인코딩 후, Multi-Head Self-Attention과 Feed-Forward Network를 L번 반복. 인코더는 입력 전체를 표현하고, 디코더는 Cross-Attention으로 인코더 출력을 참조하며 오토리그레시브 생성.
- **비유**: 회의에서 참석자 전원이 동시에 서로의 발언을 참조하며 의견을 종합하는 것. RNN은 한 명씩 순서대로 발언하는 것.
- **구체 예시**: GPT-4는 디코더 전용 Transformer, BERT는 인코더 전용. WMT14 영-독 번역에서 BLEU 28.4(당시 SOTA).
- **흔한 오해·주의점**: Self-Attention은 O(N²) 연산·메모리가 필요하여, 시퀀스가 길어지면 비용이 급증함. 이를 해결하는 것이 Sparse/Linear Attention.

## 연결 개념
- Self-Attention — Transformer의 핵심 연산
- Positional Encoding — 순서 정보 보완
- Foundation Model — Transformer 위에 구축된 대규모 모델


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Transformer는 Self-Attention으로 시퀀스를 병렬 처리하여 RNN의 순차 의존성을 제거한 아키텍처임.
> 2. **가치**: GPU 병렬화로 학습 속도를 10배+ 향상시키고, GPT·BERT 등 Foundation Model의 기반이 됨.
> 3. **판단 포인트**: O(N²) 연산 비용을 시퀀스 길이·하드웨어 예산에 맞춰 Sparse/Linear Attention으로 완화해야 함.


## Ⅰ. 개요 및 필요성

- 개요: Attention 기반 시퀀스 아키텍처
- 배경: RNN/LSTM은 순차 처리와 장거리 의존성 학습 한계로 긴 문장·대규모 학습에서 병목이 발생함.
- 필요성: Self-Attention, Feed Forward, LayerNorm으로 GPU 병렬 학습과 LLM 확장 구조를 설명해야 함.


## Ⅱ. 구조 및 구성요소

```text
입력 -> Embedding + Positional Encoding -> Encoder x L
Encoder x L -> Decoder x L -> Linear + Softmax -> 출력
Encoder Block: Self-Attention -> FFN -> Residual/LayerNorm
Decoder Block: Masked Self-Attention -> Cross-Attention -> FFN
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Multi-Head Self-Attention | 토큰 간 관계 병렬 계산 | 헤드 수 h=8~128, O(N²·d) |
| Feed-Forward Network | 비선형 변환·차원 확장 | 중간 차원 4d, GELU 활성화 |
| Positional Encoding | 순서 정보 주입 | Sinusoidal or RoPE |
| Layer Normalization | 학습 안정화 | Pre-LN이 대규모 모델 표준 |

> 요약: Transformer는 Attention->FFN->LayerNorm 블록을 L회 반복하는 인코더-디코더(또는 디코더 전용) 구조임.


## Ⅲ. 동작원리 및 흐름도

```text
토큰 임베딩 -> PE 추가 -> Self-Attention(Q·K·V 계산)
    -> Residual + LayerNorm -> FFN -> Residual + LayerNorm
    -> L회 반복 -> 출력 프로젝션
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 토큰 임베딩 + Positional Encoding | 임베딩 차원 d=512~4096 |
| 2 | Multi-Head Self-Attention 연산 | 어텐션 가중치 분포, 메모리 사용량 |
| 3 | FFN 비선형 변환 + Residual 연결 | 기울기 크기, 활성화 분포 |
| 4 | L회 반복 후 출력 프로젝션 | Perplexity, BLEU, 학습 손실 |

> 요약: 각 레이어에서 Attention으로 맥락을 수집하고 FFN으로 변환하는 과정을 L회 쌓아 표현력을 높임.


## Ⅳ. 특징

| 구분 | RNN/LSTM | Transformer | 판단 포인트 |
|:---|:---|:---|:---|
| 병렬화 | 순차 O(N) 단계 | 완전 병렬 O(1) 단계 | GPU 활용률 90%+ 달성 |
| 장거리 의존성 | 기울기 소실로 500+ 토큰 한계 | Self-Attention으로 전체 참조 | 시퀀스 길이 무관 |
| 연산 복잡도 | O(N·d²) | O(N²·d) | N>d이면 Transformer 불리 |

> 요약: Transformer는 병렬화·장거리 의존성에서 RNN을 압도하나, O(N²) 연산이 긴 시퀀스의 병목임.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 인코더 전용(BERT) -> 분류·NER, 디코더 전용(GPT) -> 생성, 인코더-디코더(T5) -> 번역·요약에 각각 적용
2. Flash Attention 2로 O(N²) 메모리를 O(N)으로 줄이고, A100 GPU에서 학습 처리량 2배 향상
3. Pre-LN + Gradient Checkpointing으로 100B+ 파라미터 모델 학습 안정화, 메모리 60% 절감

**결론 (2줄):**
- 기술사 판단: 시퀀스 처리 과제면 Transformer 기반 선택, 시퀀스 10K+ 시 Sparse Attention 적용
- 향후 방향: SSM(Mamba)·선형 Attention과 하이브리드 구조로 O(N²) 병목 극복 진행 중


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | Self-Attention·FFN·PE 원리 | RNN 대비 장단점 |
| 요구사항 명시형 | 비교하시오, 설계하시오 | 인코더/디코더 선택 기준 | O(N²) 해결 기법 비교 |

> 요약: 설명형은 아키텍처 원리, 비교형은 RNN 대비·변형 선택 기준을 중심으로 전환함.
