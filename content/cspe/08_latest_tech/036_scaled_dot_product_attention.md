---
title: "Scaled Dot-Product Attention"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 36
---

# 📖 【암기용】 개념 완전 이해

> 목적: Scaled Dot-Product Attention을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: Query와 Key의 내적으로 관련도를 구하고 Value를 가중합하는 Attention 계산식
- **왜 필요한가**: 문장 안의 모든 토큰이 서로 얼마나 관련되는지 한 번에 계산해 장거리 의존성을 포착함.
- **핵심 직관**: 질문(Q)이 각 문서 제목(K)과 맞는 정도를 점수화한 뒤, 맞는 문서 내용(V)을 더 많이 읽는 방식임.

## 깊이 이해
- **배경·문제의식**: RNN은 이전 토큰을 순차 처리해 긴 문장 의존성이 약해짐. Attention은 모든 토큰 쌍을 행렬곱으로 계산해 병렬화함.
- **작동 원리**: 입력 임베딩에서 Q·K·V를 만들고, `QKᵀ`로 유사도 점수를 계산함. 차원 `d_k`가 커지면 내적값 분산이 커져 Softmax가 한쪽으로 쏠리므로 `√d_k`로 나눔.
- **비유**: 회의록에서 "예산" 질문을 던지면, 예산 관련 문장에 형광펜을 진하게 칠하고 그 문장의 내용을 모아 답을 만드는 것과 같음.
- **구체 예시**: `d_k=64`이면 `√d_k=8`로 스케일링하여 Softmax 포화와 기울기 소실을 완화함.
- **흔한 오해·주의점**: Attention 점수는 인과관계가 아니라 토큰 간 통계적 관련도임. 해석 가능성 근거로 단독 사용하면 오판 가능.

## 연결 개념
- Self-Attention — Q·K·V를 같은 입력에서 생성
- Multi-Head Attention — 여러 Attention을 병렬 수행
- Transformer — Attention을 핵심 블록으로 반복 적층


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Scaled Dot-Product Attention은 `softmax(QKᵀ/√d_k)V`로 토큰 간 관련도를 계산하는 Transformer 핵심 연산임.
> 2. **가치**: RNN 순차 의존을 제거하고 GPU 행렬곱으로 문장 전체 관계를 병렬 계산함.
> 3. **판단 포인트**: `√d_k` 스케일링, Mask 적용, O(N²) 복잡도 관리가 설계 핵심임.


## Ⅰ. 개요 및 필요성

Scaled Dot-Product Attention은 Q·K·V 기반 가중합 연산임. Transformer는 이 연산으로 토큰 간 장거리 의존성을 병렬 계산하여 번역·요약·LLM 추론의 기반을 형성함. 기술사 답안에서는 수식, Mask, 복잡도를 함께 제시해야 함.


## Ⅱ. 구조 및 구성요소

```text
Input Embedding
      │
 ┌────┼────┐
 ▼    ▼    ▼
 Q    K    V
 │    │    │
 └─QKᵀ/√d_k┘ → Softmax → Weight × V → Attention Output
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Query(Q) | 현재 토큰이 찾는 정보 표현 | 질의 벡터, 차원 d_k |
| Key(K) | 각 토큰의 색인·주소 표현 | Q와 내적해 관련도 산출 |
| Value(V) | 실제 전달할 내용 표현 | Softmax 가중치로 합산 |
| Scale/Mask | 분산·접근 범위 제어 | `√d_k`, causal/padding mask |

> 요약: Q는 찾는 조건, K는 매칭 기준, V는 전달 내용이며 Scale과 Mask가 학습 안정성과 접근 범위를 통제함.


## Ⅲ. 동작원리 및 흐름도

```text
임베딩 입력 → Q/K/V 선형변환 → QKᵀ 유사도 계산
    → √d_k 스케일링 → Mask 적용 → Softmax → V 가중합
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 임베딩을 Wq·Wk·Wv로 선형변환 | Q/K/V shape = N×d_k |
| 2 | `QKᵀ`로 토큰 쌍 점수 계산 | Attention matrix = N×N |
| 3 | `√d_k` 스케일링 및 Mask 적용 | 미래 토큰 차단, padding 제외 |
| 4 | Softmax 후 V 가중합 | 확률합 1.0, 출력 N×d_v |

> 요약: Attention은 유사도 행렬을 확률분포로 바꾼 뒤 Value를 가중합해 문맥 벡터를 생성함.


## Ⅳ. 특징

| 구분 | RNN Attention | Scaled Dot-Product Attention | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 계산 방식 | 순차 hidden state 참조 | 행렬곱 기반 전체 토큰 참조 | GPU GEMM 활용 |
| 스케일링 | 별도 보정 없음 | `1/√d_k` 적용 | `d_k=64`면 1/8 |
| 복잡도 | 시간축 순차 의존 | O(N²) attention matrix | N=8K면 64M score |
| 제어 | Encoder-Decoder 중심 | causal/padding mask | LLM 생성 시 미래 토큰 차단 |

> 요약: Scaled Dot-Product Attention은 병렬 계산과 안정적 Softmax를 제공하나, 긴 시퀀스에서는 O(N²) 점수 행렬이 병목임.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. LLM 디코더에는 causal mask를 적용하여 t시점 토큰이 t+1 이후 토큰을 참조하지 못하게 차단
2. `d_k=64` 기준 `√d_k=8` 스케일링 적용, Softmax 포화로 인한 gradient 0 수렴 방지
3. 8K 이상 컨텍스트는 FlashAttention·PagedAttention으로 attention memory를 블록 단위 관리

**결론 (2줄):**
- 기술사 판단: 일반 Transformer는 표준 Attention, 장문맥 32K 이상은 FlashAttention·Sparse Attention 병행 선택
- 향후 방향: 선형 Attention·State Space Model과 결합해 O(N²) 병목을 완화하는 방향으로 발전


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | `QKᵀ/√d_k` 계산 단계 | RNN 대비 병렬성·복잡도 |
| 요구사항 명시형 | 비교하시오, 설계하시오 | Mask·FlashAttention 적용 흐름 | 긴 시퀀스 비용 통제 기준 |

> 요약: 설명형은 수식 원리, 설계형은 Mask와 메모리 최적화 중심으로 목차를 전환함.
