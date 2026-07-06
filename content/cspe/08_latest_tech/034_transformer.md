---
title: "Transformer (트랜스포머)"
date: "2026-07-06"
tags:
  - "cspe-latest-tech"
weight: 34
---

## Ⅰ. 개요
- **정의**: RNN/CNN 없이 Self-Attention만으로 시퀀스 데이터를 병렬 처리하는 인코더-디코더 기반 딥러닝 아키텍처
- **배경/필요성**: RNN은 순차 연산으로 GPU 병렬화가 불가하고, 긴 시퀀스에서 기울기 소실(Vanishing Gradient)로 장기 의존성을 유지할 수 없었음. 문장 전체를 동시에 읽으면서 모든 단어 간 관계를 한 번에 계산하는 새 아키텍처가 필요함
- **비유**: RNN이 한 줄씩 베끼는 필기사라면, Transformer는 책 전체를 한눈에 스캔하는 복사기

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RNN 대비 아키텍처 우위 | 병렬 처리(행렬 곱) + 장기 의존성 보존(어텐션 O(1) 경로) | Self-Attention 내부 Q/K/V 연산은 035 참조로 위임 |
| 인코더-디코더 구조 분화 | 인코더(BERT 계열) vs 디코더(GPT 계열) 분기 | LLM 학습 파이프라인(031)·Foundation Model(033) 반복 금지 |

> 요약: Attention만으로 시퀀스를 병렬 처리하여 RNN의 속도·문맥 한계를 동시에 해결한 아키텍처

## Ⅱ. 구성요소
```text
+-------------------------------------------------------------+
|                  Transformer Architecture                    |
|                                                              |
|  +-------------------------+  +-------------------------+    |
|  |      Encoder (Nx)       |  |      Decoder (Nx)       |    |
|  | +---------------------+ |  | +---------------------+ |    |
|  | | Multi-Head          | |  | | Masked Multi-Head   | |    |
|  | | Self-Attention      | |  | | Self-Attention      | |    |
|  | +---------------------+ |  | +---------------------+ |    |
|  | | Add & LayerNorm     | |  | | Cross-Attention     | |    |
|  | +---------------------+ |  | | (Encoder 출력 참조)  | |    |
|  | | Feed Forward (FFN)  | |  | +---------------------+ |    |
|  | +---------------------+ |  | | Feed Forward (FFN)  | |    |
|  | | Add & LayerNorm     | |  | +---------------------+ |    |
|  | +---------------------+ |  +-------------------------+    |
|  +-------------------------+                                 |
|                                                              |
|  +------------------+  +------------------+                  |
|  | Positional Enc.  |  | Embedding Layer  |                  |
|  +------------------+  +------------------+                  |
+-------------------------------------------------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Positional Encoding | 병렬 입력 시 소실되는 어순 정보를 sin/cos 함수로 벡터에 합산하여 위치 인식 부여 | 좌석 번호표 |
| Multi-Head Self-Attention | 입력 시퀀스 내 모든 토큰 쌍의 연관도를 다수 헤드가 동시에 계산 (내부 연산은 035 참조) | 다관점 회의 |
| Feed Forward Network | 어텐션 출력을 2층 완전연결 신경망에 통과시켜 비선형 변환 수행, 각 위치에 독립 적용 | 개별 가공기 |
| Add & LayerNorm | 잔차 연결(Residual) + 레이어 정규화로 깊은 층에서도 기울기 흐름을 안정적으로 유지 | 안전 난간 |

> 요약: Positional Encoding + Multi-Head Attention + FFN + Residual의 블록이 N층 적층된 구조

## Ⅲ. 절차
```text
+----------------+     +----------------+     +----------------+     +----------------+
| 1. 토큰화 +   |---->| 2. 인코더      |---->| 3. 디코더      |---->| 4. 출력층      |
|  임베딩 +     |     |  블록 (Nx)     |     |  블록 (Nx)     |     |  (Softmax)     |
|  위치 인코딩  |     |  문맥 이해     |     |  생성          |     |  토큰 확률     |
+----------------+     +----------------+     +----------------+     +----------------+
```

1. **토큰화 + 임베딩** — 입력 텍스트를 서브워드로 분할, 임베딩 벡터로 매핑한 뒤 Positional Encoding을 합산하여 위치 정보 부여
2. **인코더 처리** — Multi-Head Self-Attention으로 모든 토큰 간 문맥 관계를 병렬 계산, FFN으로 비선형 변환 후 Residual+LayerNorm 적용 (N층 반복)
3. **디코더 처리** — Masked Self-Attention으로 미래 토큰 참조를 차단한 뒤, Cross-Attention으로 인코더 출력을 참조하여 목표 시퀀스를 순차 생성
4. **출력 생성** — 디코더 최종 벡터를 Softmax에 통과시켜 어휘 전체에 대한 확률 분포를 산출, 가장 높은 확률의 토큰을 선택(Autoregressive)

> 요약: 임베딩 → 인코더(문맥 이해) → 디코더(순차 생성) → Softmax 출력의 4단계 흐름

## Ⅳ. 문제점
- O(N²) 연산 복잡도: 시퀀스 길이 N에 대해 어텐션 연산량·메모리가 N²으로 증가 — 모든 토큰 쌍을 계산하는 Full Attention 구조적 한계
- 추론 지연: Autoregressive 생성은 토큰 1개씩 순차 출력 — 학습은 병렬이나 추론 시 병렬화 불가
- 위치 인코딩 한계: 고정 sin/cos 기반 PE는 학습 시 본 적 없는 긴 시퀀스에서 외삽(Extrapolation) 성능 저하

> 요약: N² 복잡도·추론 순차성·위치 인코딩 외삽 실패가 Transformer의 3대 아키텍처 병목

## Ⅴ. 개선방안
1. 단기: FlashAttention으로 GPU SRAM/HBM 간 IO를 최적화하여 동일 연산량에서 속도 2~4배 향상
2. 중기: RoPE(Rotary Position Embedding) + NTK-aware Scaling으로 학습 길이 대비 4~8배 외삽 가능, 128K 토큰 컨텍스트 실현
3. 장기: State Space Model(Mamba) 등 O(N) 선형 복잡도 아키텍처로 Attention 자체를 대체하거나 하이브리드 결합

- N² 복잡도: Full Attention → Sparse Attention + FlashAttention (지표: 128K 토큰 처리 시 VRAM 50% 절감)
- 추론 지연: 순차 디코딩 → Speculative Decoding + KV Cache 최적화 (지표: 토큰 생성 속도 2배 이상)
- PE 외삽: 고정 sin/cos → RoPE + YaRN 동적 스케일링 (지표: 학습 대비 8배 길이에서 PPL 열화 5% 미만)

> 요약: FlashAttention·RoPE·SSM 하이브리드로 복잡도·추론·외삽 병목을 단계적 해소

## Ⅵ. 전망
- 향후 발전 방향: Attention-only 순수 Transformer → SSM/Linear Attention과의 하이브리드 아키텍처(Jamba 등) → NLP·비전·로보틱스 통합 범용 시퀀스 처리 엔진으로 수렴
- 기술사적 판단: Transformer는 LLM(031)·Foundation Model(033)·생성형 AI(032)의 공통 하부 아키텍처이며, O(N²) 한계 해결 여부가 AI 모델 확장성의 천장을 결정함
- 기술사 제언: 엔터프라이즈 LLM 서빙 아키텍처 설계 시 문서 길이별 어텐션 전략(Short→Full, Long→Sparse+Sliding Window)을 분기하고, KV Cache 메모리 예산을 사전 산정하여 OOM(Out of Memory) 장애를 예방할 것
