---
title: "PEFT 파라미터 효율 튜닝 (Parameter-Efficient Fine-Tuning)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 88
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 거대 언어 모델(LLM)의 방대한 가중치(Base Weight)는 고정(Freeze)해 두고, 극소수의 추가 파라미터만 학습하여 모델을 특정 도메인에 적응시키는 효율적 튜닝 기법 모음.
- **필요성**: 70B 급 LLM을 전체 파인튜닝(Full Fine-Tuning)하려면 수백 GB의 VRAM(A100 수십 대)과 엄청난 학습 시간이 필요하며, 도메인마다 수십 GB의 모델 복사본을 저장해야 하는 운영 최악의 시나리오가 발생함.
- **핵심 직관**: 1,000페이지짜리 두꺼운 원본 전공서적을 밑줄 그어가며 다시 찍어내는 대신(Full FT), 전공서적은 그대로 두고 10페이지짜리 얇은 '요약 노트(Adapter)'만 따로 만들어서 책 사이에 끼워 읽는 방식.

## 깊이 이해
- **배경**: LLM 스케일링으로 인해 도메인 특화 모델 개발의 진입 장벽이 너무 높아짐. 이를 타개하기 위해 학습 파라미터 수를 1% 미만으로 줄이면서도 Full FT와 거의 유사한 성능을 내는 연구가 폭발적으로 진행됨.
- **작동 원리**: 
  1. Base Model의 가중치 업데이트(Gradient)를 비활성화(Freeze).
  2. 트랜스포머 아키텍처의 특정 층(주로 Attention 모듈이나 FFN)에 작은 크기의 추가 파라미터 텐서(Adapter, LoRA 등)를 부착.
  3. 역전파(Backpropagation) 과정에서 이 부착된 소규모 파라미터만 학습됨.
- **비유**: 자동차 전체(Base Model)를 새로 튜닝하는 것이 아니라, 엔진의 메인 부품은 두고 점화 플러그나 필터 같은 소형 커스텀 부품(PEFT Module)만 교체하여 성능을 최적화.
- **구체 예시**: 고객센터, 인사팀, 법무팀이 각각 자신만의 AI를 원할 때, 70B 모델 복사본 3개를 띄우는 대신(수백 GB 차지), 1개의 70B 베이스 모델 위에 부서별 100MB짜리 LoRA 어댑터 3개만 로드(Adapter Routing)하여 무한 확장이 가능함.
- **흔한 오해/주의점**: PEFT가 항상 만능은 아님. 완전히 새로운 언어(예: 한국어를 전혀 모르는 모델에 한국어 학습)를 가르치거나, 코딩을 전혀 모르는 모델에 코딩을 가르치는 등 근본적인 지식 체계 변경에는 Full FT 또는 Continued Pretraining이 필요함.

## 연결 개념
- **LoRA (Low-Rank Adaptation)**: 현재 PEFT의 제왕이자 가장 널리 쓰이는 기법.
- **Adapter / Prefix Tuning**: LoRA 이전/유사 카테고리의 대표적 PEFT 기술들.
- **Multi-tenant Serving**: PEFT를 통해 하나의 베이스 모델로 다수 고객(Tenant)에게 맞춤형 모델을 제공하는 서빙 기법.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 거대 사전학습 모델의 지식(Frozen Weights)을 보존하면서, 어텐션 블록 등에 소규모 훈련 가능 모듈(Trainable Parameters)을 삽입해 최적화하는 기법.
- **가치**: VRAM 한계를 극복하여 소비자용 GPU에서도 대형 모델 튜닝을 가능케 하고, 다중 도메인 배포 시 스토리지 및 서빙 비용을 극적으로 절감(Multi-tenancy 확보).
- **판단 포인트**: 도메인 복잡도에 따른 PEFT 기법(LoRA, P-Tuning 등) 선정, 학습 안정성(Rank 설정), 운영 환경에서의 어댑터 로딩(Merge vs Dynamic Loading) 전략.

## Ⅰ. 개요 및 필요성
- **정의**: 전체 모델 파라미터의 0.1% ~ 5% 수준에 해당하는 소규모 모듈만 학습하여 Full Fine-Tuning에 필적하는 도메인 적응(Domain Adaptation)을 이루는 기법.
- **배경**: 파라미터 수백억~수천억 개 규모의 LLM은 역전파 시 필요한 옵티마이저 상태(Optimizer State), 그래디언트(Gradient) 저장 등에 모델 크기의 3~4배에 달하는 VRAM을 요구함.
- **필요성**: 메모리(VRAM), 학습 시간, 스토리지 제약이라는 3대 병목을 타개하여 기업 맞춤형(Custom) SLM/LLM의 경제적 확산을 달성하기 위함.

## Ⅱ. 핵심 아키텍처 및 원리
```text
[ Input ]
   |
+--|---------------------------------------+
|  v                                       |
| [ Frozen Base Layer (Gradient OFF) ]     |
|  |                                       |
|  +-> [ PEFT Module (Adapter/LoRA) ] -+   |
|      (Gradient ON, Trainable)        |   |
|  +-----------------------------------+   |
|  v                                       |
+--|---------------------------------------+
   |
[ Output ]
```
- **Frozen Base Model**: 사전 학습된 거대 파라미터. 학습 연산에서 제외되어 VRAM 극적 절감.
- **Trainable PEFT Module**: 태스크 특화 지식이 업데이트되는 작고 가벼운 신경망 조각.
- **Residual Connection**: Base Layer의 출력과 PEFT Module의 출력을 더해 다음 층으로 전달.

## Ⅲ. PEFT의 주요 방법론 분류
1. **Additive Methods (추가형)**:
   - **Adapter Tuning**: 트랜스포머 층 내부에 작은 Bottleneck 구조의 FFN을 직렬/병렬로 추가.
   - **Soft Prompts (Prefix Tuning, Prompt Tuning)**: 입력 시퀀스 앞단에 학습 가능한 가상의 토큰(Continuous Embeddings)을 부착.
2. **Reparameterization Methods (재매개변수화형)**:
   - **LoRA (Low-Rank Adaptation)**: 가중치 변화량($\Delta W$)을 두 개의 저랭크 행렬($A \times B$)의 곱으로 분해하여 근사(Approximation) 학습. (가장 주류 기술)
3. **Selective Methods (선택형)**:
   - **BitFit**: 모델의 Weight는 고정하고 편향(Bias) 파라미터만 학습.

## Ⅳ. Full FT vs PEFT 심화 비교
| 구분 | Full Fine-Tuning | PEFT (예: LoRA) |
|:---:|:---|:---|
| **학습 대상** | 모델 파라미터 100% | 전체 파라미터의 1% 미만 |
| **하드웨어 요구** | 다수의 고성능 GPU (A100/H100) | 소비자급 단일 GPU (RTX 3090/4090) 가능 |
| **저장 용량** | 도메인별 수십 GB의 모델 복제본 필요 | 도메인별 수백 MB의 어댑터 가중치만 저장 |
| **서빙(Serving)**| 도메인별로 독립된 컨테이너/인프라 구성 | 베이스 모델 1개 메모리 상주 + 요청별 어댑터 스위칭 |

## Ⅴ. 운영 리스크 및 설계 고려사항
- **리스크 1: 성능 한계 (Capacity Bottleneck)**:
  - 완전히 새로운 지식이나 문법 체계를 주입하기에는 PEFT 모듈의 용량(Rank)이 부족할 수 있음.
  - **대응**: 도메인 격차가 크면 LoRA의 Rank를 늘리거나, Base Model에 대한 Continued Pre-training 선행 검토.
- **리스크 2: 서빙 레이턴시 (Inference Overhead)**:
  - Adapter 구조는 추론 시 추가 연산 단계를 발생시켜 미세한 지연(Latency) 유발.
  - **대응**: LoRA의 경우 추론 시점에 $W = W + \Delta W(A \times B)$ 형태로 병합(Merge)하여 Base Model과 동일한 추론 속도 달성.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: 도메인 벤치마크 F1 Score(Full FT 대비 $98\%$ 이상 유지), Adapter 크기(MB), 튜닝 소요 GPU Hours.
- **실무 설계 (Multi-tenant AI)**: B2B SaaS 기업에서 고객사(A, B, C)별 맞춤형 AI 제공 시, 공통 LLaMA Base를 GPU에 올려두고, 고객사 A 요청 시 A사의 LoRA 어댑터 가중치만 동적으로 캐싱(Dynamic Adapter Loading)하여 연산 처리.
- **결론**: PEFT는 LLM 튜닝의 '민주화(Democratization)'를 이끈 혁신 기술이며, 온디바이스 AI(On-device AI)와 기업 맞춤형 AI 서비스 배포를 위한 디팩토 표준(De facto standard) 아키텍처임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Adapter, Prefix, LoRA 등 다양한 PEFT 기법들의 구조적 차이와 메모리 절감 수학적 원리 중심으로 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: 다테넌트(Multi-tenant) 서빙 아키텍처, Base Model Merge 전략, 클라우드 운영 비용(FinOps) 최적화 관점에서 작성.
