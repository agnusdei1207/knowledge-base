---
title: "Multi-Head Attention"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 37
---

# 📖 【암기용】 개념 완전 이해

> 목적: Multi-Head Attention을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: 여러 개의 Attention Head가 서로 다른 관점으로 토큰 관계를 병렬 학습하는 구조
- **왜 필요한가**: 한 Attention만 쓰면 문법·의미·위치·공참조 관계를 하나의 공간에 섞어 표현해야 함.
- **핵심 직관**: 한 문장을 여러 전문가가 동시에 읽고, 각자 문법·주제·지시어 관계를 따로 표시한 뒤 합치는 방식임.

## 깊이 이해
- **배경·문제의식**: 단일 Attention은 하나의 관련도 행렬만 만들기 때문에 다양한 관계를 분리하기 어렵다. Multi-Head는 임베딩을 여러 부분공간으로 투영해 관계 유형별 패턴을 학습함.
- **작동 원리**: Q·K·V를 Head 수 `h`만큼 나누어 Attention을 병렬 수행함. 각 Head 출력을 Concatenate한 뒤 `W_o`로 다시 모델 차원으로 투영함.
- **비유**: 회의록을 재무 담당, 일정 담당, 리스크 담당이 각각 읽고 표시한 내용을 마지막에 하나의 보고서로 합치는 것과 같음.
- **구체 예시**: `d_model=768`, `h=12`이면 Head당 차원 `d_k=64`; 12개 관련도 행렬이 병렬 계산됨.
- **흔한 오해·주의점**: Head 수를 늘리면 항상 정확도가 오르는 것이 아님. Head당 차원이 작아져 표현력이 줄고, 중복 Head가 생길 수 있음.

## 연결 개념
- Scaled Dot-Product Attention — 각 Head 내부 연산
- Transformer Block — MHA와 FFN을 반복 적층
- Attention Head Pruning — 중복 Head 제거 기법


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Multi-Head Attention은 Q·K·V를 h개 부분공간으로 분할해 Attention을 병렬 수행하는 구조임.
> 2. **가치**: 문법·의미·위치·공참조 등 여러 관계를 Head별로 분리 학습하여 표현력을 확보함.
> 3. **판단 포인트**: Head 수, Head 차원, 중복 Head 제거, KV Cache 메모리 증가를 함께 설계해야 함.


## Ⅰ. 개요 및 필요성

Multi-Head Attention은 복수 Attention 병렬 구조임. Transformer는 단일 Attention의 표현 한계를 보완하기 위해 입력을 여러 부분공간에 투영하고, 각 Head가 다른 관계 패턴을 학습하도록 구성함.


## Ⅱ. 구조 및 구성요소

```text
Input X
  │
  ├─ Wq1/Wk1/Wv1 → Head 1 ┐
  ├─ Wq2/Wk2/Wv2 → Head 2 ├→ Concat → Wo → Output
  └─ Wqh/Wkh/Wvh → Head h ┘
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Projection Matrix | 입력을 Head별 Q/K/V로 변환 | `Wq,Wk,Wv` |
| Attention Head | 부분공간별 관련도 계산 | Head당 `d_k=d_model/h` |
| Concatenation | Head 출력 결합 | `h × d_v`를 연결 |
| Output Projection | 모델 차원으로 재투영 | `W_o`, residual 연결 전 단계 |

> 요약: MHA는 Head별 Attention 결과를 연결하고 재투영하여 다양한 관계 정보를 하나의 표현으로 통합함.


## Ⅲ. 동작원리 및 흐름도

```text
입력 X → h개 Q/K/V 투영 → Head별 Attention 병렬 수행
    → Head 출력 연결 → Wo 투영 → Residual/LayerNorm
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 임베딩을 Head별 Q/K/V로 선형투영 | `d_model=768,h=12,d_k=64` |
| 2 | 각 Head에서 `softmax(QKᵀ/√d_k)V` 계산 | Head별 N×N attention matrix |
| 3 | Head 출력 Concatenate | 출력 차원 `h×d_v=d_model` |
| 4 | `W_o` 투영 후 블록 출력 | Residual shape 일치 |

> 요약: 입력을 여러 Head로 분해해 관계를 병렬 학습하고, Concatenate와 출력 투영으로 통합 표현을 생성함.


## Ⅳ. 특징

| 구분 | Single-Head Attention | Multi-Head Attention | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 관계 표현 | 단일 관련도 행렬 | h개 관련도 행렬 | BERT-base h=12 |
| 병렬성 | 1개 Attention | Head 병렬 계산 | GPU batch matmul |
| 메모리 | N² score 1개 | N² score h개 | N=4K,h=16이면 256M score |
| 운영 최적화 | Pruning 영향 작음 | 중복 Head 제거 가능 | 20~40% Head pruning 사례 |

> 요약: MHA는 표현력을 늘리지만 Head 수에 비례해 Attention score와 KV Cache 관리 부담이 증가함.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 일반 LLM은 `d_k=64` 기준으로 Head 수를 산정하고, `d_model % h = 0` 조건을 모델 설계 기준으로 적용
2. 추론 메모리 절감을 위해 MQA/GQA 적용, KV Head 수를 32→8로 줄여 KV Cache 약 75% 절감
3. 모델 압축 시 Attention Head Importance를 측정해 기여도 하위 20% Head pruning 후 정확도 회귀 평가

**결론 (2줄):**
- 기술사 판단: 학습 표현력은 MHA, 대규모 서빙 비용은 GQA/MQA를 선택해 KV Cache를 통제함.
- 향후 방향: LLM 서빙에서는 Full MHA보다 GQA 기반 구조가 처리량·메모리 균형점으로 확산됨.


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | Head별 병렬 Attention 흐름 | Single-Head 대비 표현력 |
| 요구사항 명시형 | 비교하시오, 최적화하시오 | MHA→GQA/MQA 변환 흐름 | KV Cache·메모리 절감 기준 |

> 요약: 설명형은 Head 병렬 구조, 최적화형은 GQA/MQA와 Head pruning 중심으로 목차를 전환함.
