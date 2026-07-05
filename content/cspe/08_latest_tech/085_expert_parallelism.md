---
title: "전문가 병렬 (Expert Parallelism)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 85
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: MoE(Mixture of Experts) 모델에서 수많은 전문가 네트워크(Expert)를 여러 장의 GPU나 노드에 분산 배치하고, 통신을 통해 토큰을 주고받으며 병렬 처리하는 기법.
- **필요성**: MoE 모델은 총 파라미터 수가 막대하여(수백B ~ Trillion) 단일 GPU 메모리에 적재할 수 없으며, 기존의 텐서 병렬화(TP)만으로는 효율적인 확장이 불가능함.
- **핵심 직관**: 백화점의 각 매장(Expert)을 층별/건물별(GPU)로 나누어 입점시키고, 고객(Token)이 안내 데스크(Router)의 지시를 받아 엘리베이터(All-to-All 통신)를 타고 해당 매장 건물로 이동하게 만드는 물류 시스템.

## 깊이 이해
- **배경**: 딥러닝 분산 학습의 3대장(Data, Tensor, Pipeline Parallelism)에 더해, MoE 모델의 등장으로 '전문가' 단위로 모델을 쪼개는 새로운 패러다임(EP)이 필수 불가결해짐.
- **작동 원리**: 
  1. 모델 가중치 분산: 64개의 Expert가 있다면, 8장의 GPU에 각각 8개씩의 Expert를 배치. (Non-expert 레이어인 Attention 등은 복제되거나 TP로 분할됨).
  2. All-to-All Dispatch: 라우터가 토큰 배정을 마치면, GPU 1에 있는 토큰 중 GPU 3의 Expert가 필요한 토큰들을 GPU 3으로 전송(모든 GPU가 서로 데이터를 주고받음).
  3. Expert 연산: 각 GPU가 자신이 보유한 Expert를 사용하여 도착한 토큰들에 대해 FFN 연산 수행.
  4. All-to-All Combine: 연산이 끝난 토큰들을 다시 원래의 문장 순서(원래 GPU)에 맞게 돌려보냄.
- **비유**: 전국 8도의 각 우편집중국(GPU)이 각 지역 전문 우체부(Expert)를 데리고 있고, 다른 지역 우편물이 오면 각 지역 집중국끼리 대규모로 교환(All-to-All)한 뒤 배달하는 시스템.
- **구체 예시**: GPT-4 (추정 1.7T, 16 Experts). 16개의 Expert를 8개의 GPU를 가진 여러 노드에 나누어 배치. 토큰 연산 시 NVLink나 Infiniband를 통해 노드 간 극심한 데이터 교환이 발생.
- **흔한 오해/주의점**: EP는 연산을 분산시켜 주지만, 그 대가로 '네트워크 통신 비용'을 크게 지불함. 통신 대역폭(Bandwidth)이 좁거나 토큰 쏠림(Imbalance)이 생기면 병렬화 효율이 급감하여 오히려 Dense 모델보다 느려질 수 있음.

## 연결 개념
- **Mixture of Experts (MoE)**: 전문가 병렬화가 적용되는 대상 아키텍처.
- **All-to-All Communication**: EP 구현 시 GPU 간 데이터를 N:N으로 교환하는 집단 통신 연산.
- **3D Parallelism (TP + PP + DP)**: EP와 결합하여 대규모 클러스터(4D Parallelism)를 구성하는 기본 병렬화 기법.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: MoE 아키텍처에서 전문가(Expert) 파라미터들을 물리적으로 분리된 디바이스(GPU)에 할당하는 특화된 분산 병렬화 기법.
- **가치**: 모델의 메모리 풋프린트를 극복하여 Trillion 파라미터 스케일의 초거대 AI 학습 및 서빙을 가능케 하는 핵심 인프라 기술.
- **판단 포인트**: GPU 간 통신(All-to-All) 병목의 해소, Expert 쏠림 현상(Load Imbalance) 제어, TP/PP/DP/EP의 최적 텐서 병렬화 전략 조합.

## Ⅰ. 개요 및 필요성
- **정의**: MoE 내의 여러 하위 신경망(Experts)을 다수의 GPU 가속기에 분산 배치하여 메모리 사용량을 줄이고 연산을 병렬화하는 분산 처리 기법.
- **배경**: 매개변수 수백 빌리언 이상인 MoE 모델은 단일 GPU VRAM(예: H100 80GB) 적재 불가능. 기존 병렬화 방식(TP, PP)은 MoE의 조건부 라우팅 특성을 반영하지 못함.
- **필요성**: 메모리 한계를 극복함과 동시에 토큰 라우팅에 따른 통신 오버헤드를 최소화하기 위한 MoE 맞춤형 분산 아키텍처 필요.

## Ⅱ. 병렬화 아키텍처 (EP의 구조)
```text
[Tokens in GPU 0, 1] 
        | (Router 결정)
        v
[ All-to-All Dispatch (Network) ] <--- 핵심 병목 구간! (NVLink / Infiniband)
        | (토큰을 해당 Expert가 있는 GPU로 물리적 전송)
        v
+-------+-------+  +-------+-------+
| GPU 0 (Exp 1) |  | GPU 1 (Exp 2) | ---> (각자 보유한 Expert로 FFN 독립 연산 수행)
+-------+-------+  +-------+-------+
        | (연산 완료)
        v
[ All-to-All Combine (Network) ]  <--- (원래 문장 순서로 복구하기 위해 재전송)
        |
        v
[Next Layer in GPU 0, 1]
```
- **Expert Sharding**: 총 $E$개의 Expert를 $N$개의 GPU에 $E/N$개씩 분할(Shard)하여 적재.
- **All-to-All 통신**: 분산 딥러닝 통신 중 가장 무거운 연산. 모든 디바이스가 다른 모든 디바이스와 토큰 텐서를 송수신함.

## Ⅲ. 통신-연산 흐름 (동작원리)
1. **Local Gating**: 각 GPU에서 자신에게 할당된 배치(Batch) 토큰들에 대해 라우터 연산을 수행하여 목적지 Expert 산출.
2. **Dispatch (GPU 간 통신)**: 목적지 Expert가 자신이 아닌 다른 GPU에 있다면, All-to-All 통신을 통해 해당 토큰 텐서를 원격 GPU로 전송.
3. **Expert FFN (GPU 내 연산)**: 각 GPU는 외부에서 도착한 토큰과 내부 토큰을 모아, 자신이 가진 Expert 파라미터를 이용해 행렬 곱 연산 수행.
4. **Combine (GPU 간 통신)**: 연산된 결과(Activation)를 다시 본래 토큰이 있던 원본 GPU로 All-to-All 전송하여 Residual Stream에 결합.

## Ⅳ. 주요 특징 및 다른 병렬화 기법과의 비교
- **Tensor Parallelism (TP) vs EP**:
  - TP: 행렬 자체를 쪼개어 연산(All-Reduce 통신 발생). Attention 레이어에 적합.
  - EP: 완전한 형태의 부분 신경망(Expert)을 분배(All-to-All 통신 발생). MoE FFN 레이어에만 적용.
- **확장성**: GPU를 늘릴수록 총 파라미터 용량(Capacity)이 선형적으로 늘어나므로 LLM 확장에 가장 유리.
- **병목 이동**: 연산 병목(Compute Bound)에서 통신 병목(Network Bound)으로 시스템의 병목 구간이 전환됨.

## Ⅴ. 심화: EP 최적화 및 복합 병렬화 전략
- **문제점 1: 막대한 All-to-All 통신 오버헤드**:
  - **대응 (Topology-aware EP)**: 클러스터 토폴로지를 인지하여, 고속 통신망(NVLink) 내부에 속한 GPU들끼리만 EP를 구성하고, 노드 간(Infiniband) 통신은 지양하는 계층형 라우팅 설계 적용.
- **문제점 2: 특정 GPU 통신/연산 집중 (Imbalance)**:
  - **대응 (Expert Capacity & Dropping)**: 특정 Expert(특정 GPU)로 토큰이 쏠릴 경우 허용 용량(Capacity)을 초과한 토큰은 Drop 처리하거나, 가벼운 다른 GPU로 재배정.
- **4D Parallelism (TP + PP + DP + EP)**:
  - 실제 대규모 학습 시: Attention은 TP, 레이어 분할은 PP, 배치 분할은 DP, FFN 계층은 EP를 혼합하는 복합 분산 아키텍처(예: DeepSpeed MoE, Megatron-LM)를 채택.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: 통신 대비 연산 비율(Computation-to-Communication Ratio), 네트워크 대역폭(Bandwidth), 노드 간 지연시간(Latency).
- **실무 설계**: GPU 8대로 구성된 단일 노드 섀시 내에서는 NVLink를 활용하여 EP를 최대 8-way로 설정하고, 노드 간 확장 시에는 DP(Data Parallelism)를 사용하여 All-to-All 통신이 이더넷 스위치 병목을 타지 않도록 아키텍처를 제한.
- **결론**: 전문가 병렬(EP)은 트릴리언(Trillion) 규모의 AI 모델 시대를 여는 열쇠이며, 알고리즘(Router)과 인프라(Network Topology) 간의 공동 설계(Co-design) 역량이 기업의 초거대 AI 경쟁력을 결정함.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: All-to-All Dispatch 및 Combine 과정에서 토큰 데이터가 GPU 사이를 이동하는 과정을 시각적/단계적으로 설명.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: NVLink vs Infiniband 대역폭 차이를 고려한 Topology-aware 배치 전략, TP/PP/EP/DP의 혼합(Hybrid) 아키텍처 최적화 중심으로 작성.
