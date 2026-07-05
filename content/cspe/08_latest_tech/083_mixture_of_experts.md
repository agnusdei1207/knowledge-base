---
title: "전문가 혼합 (Mixture of Experts)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 83
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 여러 개의 서브 네트워크(Expert)와 이들을 선택하는 라우터(Router)로 구성되어, 입력 토큰마다 가장 적합한 소수의 Expert만 선택적으로 활성화하는 희소(Sparse) 모델 구조.
- **필요성**: 기존 밀집(Dense) 모델은 파라미터를 키우면 계산 비용(FLOPs)도 정비례하여 폭증함. 모델 용량은 대폭 늘리면서 매 토큰당 연산량은 고정하여 학습/추론 효율을 높이는 돌파구가 필요함.
- **핵심 직관**: 모든 환자가 병원의 모든 의사를 만나는 것이 아니라(Dense), 접수처(Router)에서 환자의 증상(Token)을 판단하여 해당 분야 전문의 1~2명(Expert)에게만 진료를 받게 하는 방식.

## 깊이 이해
- **배경**: 구글의 Sparsely-Gated MoE(2017)에서 딥러닝에 본격 도입되었고, 스위치 트랜스포머(Switch Transformer)를 거쳐 Mixtral, GPT-4 등 최상위 LLM의 핵심 아키텍처로 자리 잡음.
- **작동 원리**:
  1. 트랜스포머의 피드포워드 네트워크(FFN)를 여러 개의 Expert Layer(독립된 FFN)로 대체.
  2. 라우터 네트워크가 각 입력 토큰의 은닉 상태(Hidden State)를 바탕으로 각 Expert에 대한 적합도 점수(Logits)를 계산.
  3. Softmax를 거쳐 상위 K개(Top-K, 보통 1~2개)의 Expert만 선택하여 해당 토큰을 전송(Dispatch).
  4. 선택된 Expert들이 계산한 결과에 라우터가 계산한 확률값을 가중치로 곱하여 최종 출력을 결합(Combine).
- **비유**: 대규모 종합병원. 수많은 전문의(Expert)가 있지만, 환자(Token)당 1~2명의 전문의만 배정되므로 진료비(Compute)는 적게 들면서 병원 전체의 전문성(Capacity)은 거대함.
- **구체 예시**: Mixtral 8x7B. 총 8개의 7B급 Expert가 존재하나, 토큰당 Top-2 Expert만 활성화되므로 실제 연산은 13B 모델 수준(약 1/4 FLOPs)임.
- **흔한 오해/주의점**: 연산량은 적지만 파라미터 전체를 VRAM에 올려야 하므로 메모리 요구량은 여전히 막대함(47B 크기). 또한 특정 Expert로 토큰이 쏠리면(Load Imbalance) 병목이 발생하여 전체 속도가 저하됨.

## 연결 개념
- **Router Network (Gating)**: 토큰을 어떤 Expert로 보낼지 결정하는 교통경찰.
- **Load Balancing Loss**: 특정 Expert로의 쏠림 현상을 방지하기 위해 훈련 시 부여하는 벌점(Loss).
- **Expert Parallelism**: 거대한 MoE 모델을 여러 장의 GPU에 찢어서 배포하는 분산 처리 기법.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 입력 데이터(Token)의 특성에 따라 동적으로 연산 경로(Expert)를 결정하는 조건적 컴퓨팅(Conditional Computing) 아키텍처.
- **가치**: Dense 모델 대비 1/4 ~ 1/10 수준의 연산량(FLOPs)으로 동등한 성능을 내어 대규모 LLM의 학습 및 추론 한계를 돌파.
- **판단 포인트**: Top-K 라우팅 전략, 부하 불균형 해소를 위한 보조 손실(Auxiliary Loss) 설계, GPU 간 통신(All-to-All) 병목 완화.

## Ⅰ. 개요 및 필요성
- **정의**: 복수의 전문가(Expert) 네트워크와 게이팅 네트워크(Router)를 결합하여, 입력별로 최적의 전문가 소수만 활성화하는 희소(Sparse) 신경망 구조.
- **배경**: 파라미터 스케일링에 따른 막대한 컴퓨팅 비용 증가와 전력 소모(Power Wall) 문제.
- **필요성**: 모델의 총 파라미터(지식 용량)와 활성 파라미터(추론 비용)를 분리하여, 경제성을 갖춘 초거대 AI(AGI) 구현의 필수 기반 확보.

## Ⅱ. MoE의 아키텍처 및 핵심 구성요소
```text
[Input Token (x)]
       |
       +-----> [Router (Gating Network)] -----> [Softmax Score: G(x)]
       |                                              |
       +-----> [Expert 1 (FFN)] <---(Activate)--------+ (Top-1)
       +-----> [Expert 2 (FFN)] <---(Skip)            |
       ...                                            |
       +-----> [Expert N (FFN)] <---(Activate)--------+ (Top-K)
       |
[Output] = SUM( G(x)_i * Expert_i(x) ) for i in Top-K
```
- **Router (Gating Network)**: 토큰 $x$에 대해 각 Expert $i$의 선택 확률 $G(x)_i$를 계산.
- **Expert Network**: 보통 기존 Transformer의 MLP(FFN) 레이어를 N개 복제한 독립적 신경망.
- **Top-K Selection**: 보통 $K=1$ 또는 $2$를 사용하여 연산의 희소성(Sparsity) 보장.

## Ⅲ. 동작 메커니즘 (추론 과정)
1. **Routing Score 계산**: 라우터가 $W_g \cdot x$ 연산 후 가우시안 노이즈를 추가하고 Softmax를 취해 확률값 도출.
2. **Top-K Expert 할당**: 확률이 가장 높은 K개의 Expert 선택. 선택받지 못한 Expert의 연산은 생략(Zero-out).
3. **Dispatch & Compute**: 토큰 $x$가 선택된 Expert가 존재하는 물리적 GPU 위치로 이동(All-to-All 통신) 후 FFN 연산 수행.
4. **Weighted Combine**: Expert의 출력값에 라우팅 확률(Gating Score)을 곱하여 합산한 뒤 다음 레이어로 전달.

## Ⅳ. 주요 특징 (Dense vs MoE)
- **비용-성능 분리(Decoupling)**: 100B MoE 모델이 20B Dense 모델 수준의 속도로 동작.
- **지식의 전문화**: 특정 Expert는 문법, 다른 Expert는 수학 등 모델 내부적으로 특화된 지식 군집 형성.
- **인프라 종속성**: 통신 오버헤드(All-to-All)가 매우 커서 NVLink/Infiniband 같은 고대역폭 네트워크가 필수적임.

## Ⅴ. MoE 운영의 핵심 과제와 극복 방안
- **과제 1: Expert Collapse (전문가 붕괴)**: 라우터가 초기에 학습을 잘한 소수의 Expert에게만 모든 토큰을 몰아주는 현상.
  - **극복**: Load Balancing Loss(균형 손실 함수)를 추가하여 토큰이 고르게 분배되도록 강제함.
- **과제 2: Capacity Overflow (용량 초과 및 토큰 유실)**: 특정 Expert의 버퍼 용량(Capacity Factor)을 초과하여 토큰이 몰리면 처리되지 못하고 버려짐(Dropped Tokens).
  - **극복**: Capacity Factor를 조절하거나, 유실된 토큰은 Residual Connection으로만 통과시키는 Fallback 처리.
- **과제 3: All-to-All 통신 병목**: 토큰이 이리저리 이동하며 발생하는 네트워크 병목.
  - **극복**: Expert Parallelism과 Tensor Parallelism을 교차(Hybrid) 배치하여 통신량 최적화.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: Token Drop Rate(1% 미만 유지), Expert Utilization(부하 균등도), All-to-All 통신 Latency 비중.
- **실무 아키텍처**: 32개의 Expert를 가진 MoE 모델을 8대의 GPU 서버에 분산 서빙할 때, 노드 내에서는 Tensor Parallelism, 노드 간에는 Expert Parallelism을 적용하여 통신 오버헤드를 최소화.
- **결론**: Mixture of Experts는 하드웨어의 물리적 한계를 극복하고 모델 크기를 무한대에 가깝게 키울 수 있는 가장 현실적인 해결책이며, 차세대 AI 패권 경쟁의 핵심 아키텍처임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Top-K 라우팅 수식, Dispatch-Combine으로 이어지는 토큰 흐름도에 집중하여 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: Load Balancing 방안, Token Drop 방지 대책, 분산 병렬화(EP, TP) 아키텍처 설계와 운영 지표 관점에서 작성.
