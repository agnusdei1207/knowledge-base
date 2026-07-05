---
title: "희소 모델 (Sparse Model)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 82
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **희소 모델** | 희소 모델 (Sparse Model)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 전체 신경망 파라미터 중 입력 데이터에 따라 일부(필수적인 뉴런이나 연결)만 선택적으로 활성화하여 연산량(FLOPs)을 극적으로 줄이는 모델 구조.
- **필요성**: Dense Model(밀집 모델)은 하나의 입력을 처리할 때 모델의 모든 파라미터를 연산에 사용하여 비용이 기하급수적으로 증가함. 성능 향상을 위해 모델 크기(Capacity)는 키우되, 추론 비용은 낮추는 해결책이 필요함.
- **핵심 직관**: 백화점의 전체 직원(파라미터) 명단은 매우 크지만, 고객(입력)의 질문에 맞는 특정 매장의 직원 1~2명(활성화 파라미터)만 응대하게 하여 전체적인 비용을 최적화하는 조직 운영 방식.

## 깊이 이해
- **배경**: 스케일링 법칙(Scaling Law)에 의해 파라미터를 늘리면 성능은 오르나 훈련 및 추론 비용이 폭증함. 이를 극복하기 위해 총 파라미터 수(Model Size)와 활성 파라미터 수(Active Parameters)를 분리하려는 시도에서 출발함.
- **작동 원리**:
  1. **Weight Sparsity (정적)**: 학습 전/후에 덜 중요한 가중치를 0으로 만들어(Pruning) 연산에서 제외함.
  2. **Activation Sparsity (동적)**: 입력 토큰에 따라 조건부로 특정 서브 네트워크(예: Mixture of Experts의 Expert)만 활성화하여 계산함.
  3. Sparse Kernel: 0인 가중치를 건너뛰고 연산하는 하드웨어(GPU/NPU) 및 커널 수준의 최적화가 동반됨.
- **비유**: 모든 업무를 모든 직원이 다 같이 결재하는 방식(Dense)에서, 업무 성격에 따라 담당자만 결재하는 시스템(Sparse)으로 전환.
- **구체 예시**: Mixtral 8x7B 모델. 총 파라미터는 47B이지만, 각 토큰 처리 시 2개의 Expert(13B)만 활성화되어 추론 속도와 메모리 사용량은 13B Dense 모델 수준으로 유지하면서 성능은 70B 모델에 근접함.
- **흔한 오해/주의점**: Sparsity를 50%로 만들었다고 무조건 2배 빨라지는 것은 아님. 불규칙한 메모리 접근(Unstructured Sparsity)은 하드웨어 가속기가 처리하기 어려워 오히려 느려질 수 있음. Structured Sparsity와 Sparse Kernel 지원 여부가 성능의 핵심임.

## 연결 개념
- **Model Pruning**: 희소 모델을 만드는 가장 대표적인 정적(Static) 기법.
- **Mixture of Experts (MoE)**: 거대 LLM에서 가장 널리 쓰이는 동적(Dynamic) 희소 모델 구조.
- **Sparse Tensor Core**: NVIDIA Ampere 아키텍처부터 지원하는 2:4 Structured Sparsity 연산 가속기.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 모델의 파라미터 중 $0$이 아닌 유의미한 값만 선택적으로 연산하는 조건부 컴퓨팅 아키텍처.
- **가치**: 모델의 지식 저장 공간(용량)은 극대화하면서도, 실시간 추론 연산량(FLOPs)과 소비 전력을 억제하여 초대규모 AI의 상용화를 견인.
- **판단 포인트**: 정적(Pruning) vs 동적(MoE) 접근의 선택, 하드웨어(NPU/GPU Sparse Tensor Core) 지원 여부, 토큰 분산에 따른 Load Imbalance 해결.

## Ⅰ. 개요 및 필요성
- **정의**: 전체 가중치(Weight)나 활성화 값(Activation) 중 상당수를 0으로 만들어, 실제 곱셈-덧셈 연산(MAC)에 참여하는 파라미터 비율을 낮춘 모델 구조.
- **배경**: Dense LLM의 확장으로 인한 Memory Wall 및 Power Wall 문제 봉착 -> "모든 파라미터가 매 순간 필요한 것은 아니다"는 관점의 대두.
- **필요성**: 총 파라미터 수(성능 결정)와 활성 FLOPs(비용 결정)를 분리(Decoupling)하여 Cost-Effective한 스케일 업을 달성하기 위함.

## Ⅱ. 희소 모델의 구조 및 메커니즘
```text
[Input Token]
      |
      +---> [Gating / Router Mechanism] ---> (Select Active Nodes)
      |
      +---> [Sparse Computation Layer] 
            |-- (Node A: Active)   ---> Compute
            |-- (Node B: Inactive) ---> Skip (Zero out)
            |-- (Node C: Active)   ---> Compute
      |
      +---> [Output Generation]
```
- **Sparsity Mask**: 활성화할 요소(1)와 무시할 요소(0)를 구분하는 이진 마스크.
- **Gating Network (Router)**: 동적 희소성(MoE)에서 입력 토큰을 어느 서브 네트워크(Expert)로 보낼지 결정하는 모듈.
- **Sparse Kernel**: 0으로 마스킹된 부분의 연산을 하드웨어 단에서 건너뛰게(Skip) 해주는 최적화 라이브러리(예: cuSPARSE).

## Ⅲ. 희소성(Sparsity) 부여 방식 (동작원리)
1. **Unstructured Sparsity**: 개별 가중치를 크기 순으로 잘라냄. 압축률은 좋으나 메모리 접근이 불규칙하여 하드웨어 가속(Speedup)이 어려움.
2. **Structured Sparsity**: 채널, 필터, 레이어 등 블록 단위로 잘라냄. 텐서 형태가 유지되어 GPU 캐시 및 병렬 처리에 유리함.
3. **N:M Sparsity (NVIDIA)**: M개의 인접한 가중치 중 N개만 0이 아닌 값을 가지도록 강제함(예: 2:4). Sparse Tensor Core에서 2배의 연산 속도 향상 제공.
4. **MoE (Dynamic Sparsity)**: 추론 시점에 토큰별로 상위 K개의 전문가(Expert)만 동적으로 선택하여 연산.

## Ⅳ. 주요 특징 및 Dense Model과의 비교
- **효율성**: 활성 FLOPs 감소로 토큰당 생성 지연(TPOT) 단축.
- **용량(Capacity) 확보**: 총 파라미터 크기를 유지하거나 늘릴 수 있어, 다양한 도메인 지식 수용 가능.
- **메모리 트레이드오프**: 연산량은 줄지만, 전체 모델 가중치를 VRAM에 올려두어야 하므로(MoE의 경우) 메모리 사용량은 여전히 높음.

## Ⅴ. 심화: Sparse Model 구현 시 한계점 및 해결방안
- **문제점 1: Hardware-Algorithm Mismatch**: 비정형(Unstructured) 희소성은 GPU에서 실질적 속도 향상(Wall-clock Time)으로 이어지지 않음.
  - **대응**: NVIDIA 2:4 Structured Sparsity 적용, 혹은 Block-sparse 알고리즘 설계.
- **문제점 2: Load Imbalance (동적 희소성)**: 특정 Expert나 경로에 토큰이 집중되면 병목 발생 및 다른 노드 유휴화.
  - **대응**: Load Balancing Loss(보조 손실 함수)를 추가하여 토큰이 균등하게 분산되도록 라우터 학습.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: Sparsity Ratio(0의 비율), Active Parameters per Token, p95 추론 지연 시간 개선율.
- **실무 설계**: 모바일 온디바이스 AI 탑재 시 7B 모델을 N:M Sparsity로 Pruning하고 INT8 양자화를 결합하여 활성 메모리와 배터리 소모를 극적으로 절감. 서버급 대형 모델(GPT-4급)은 MoE 아키텍처를 도입하여 비용 최적화.
- **결론**: 희소 모델은 "적게 연산하면서도 많이 아는" 차세대 AI 아키텍처의 표준이며, 하드웨어(Sparse Tensor Core)와 소프트웨어(MoE, Pruning)의 공동 설계(Co-design)가 성능을 결정짓는 핵심 경쟁력임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Structured vs Unstructured 차이, N:M Sparsity 등 연산 가속 원리에 초점을 맞추어 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: 거대 LLM 추론 비용 절감 방안으로 출제 시. MoE 아키텍처, 라우터 부하 분산(Load Balancing), GPU 커널 최적화 전략 중심으로 작성.
