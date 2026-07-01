---
title: "접두 튜닝 (Prefix Tuning)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 92
---

# 📖 【암기용】 개념 완전 이해

> 목적: Prefix Tuning을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: 모델 가중치는 고정하고 각 레이어 attention 앞에 학습 가능한 prefix key/value 벡터를 붙이는 PEFT 기법
- **왜 필요한가**: 전체 모델을 바꾸지 않고도 특정 task에 맞는 문맥 유도 신호를 모델 내부 attention에 주입할 수 있음.
- **핵심 직관**: 매번 답하기 전에 보이지 않는 업무 지침 카드를 모델의 기억 앞쪽에 꽂아두는 방식임.

## 깊이 이해
- **배경·문제의식**: Prompt Tuning은 입력 임베딩 수준에서 soft prompt를 붙이지만, Prefix Tuning은 attention layer의 K/V prefix를 학습해 더 깊은 제어를 제공함.
- **작동 원리**: 각 Transformer layer에 학습 가능한 prefix vector를 두고, 실제 토큰이 attention을 수행할 때 prefix K/V를 함께 참조하게 함. base model은 freeze됨.
- **비유**: 모든 회의 전에 의제가 적힌 가상 메모지를 각 부서 책상에 미리 놓아, 회의 발언 방향을 유도하는 것과 같음.
- **구체 예시**: 요약·생성 task에서 수십~수백 개 prefix token만 학습해 base model을 task에 맞게 조정함.
- **흔한 오해·주의점**: Prefix 길이가 길면 컨텍스트와 메모리를 사용하고 지연이 증가함. task별 prefix 관리가 필요함.

## 연결 개념
- Prompt Tuning — 입력 soft prompt 학습
- PEFT — Prefix Tuning의 상위 범주
- KV Cache — prefix K/V가 추론 메모리에 영향

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Prefix Tuning은 layer별 attention K/V 앞에 학습 가능한 prefix를 추가하는 PEFT 기법임.
> 2. **가치**: base model을 고정한 채 작은 prefix 파라미터만으로 task별 생성 행동을 유도함.
> 3. **판단 포인트**: prefix length, layer 적용 범위, KV Cache 증가, task별 prefix 관리가 핵심임.

## Ⅰ. 개요 및 필요성

Prefix Tuning은 attention prefix 기반 모델 적응 기법임. 모델 전체를 학습하지 않고, layer별 prefix K/V를 학습해 특정 task의 출력 방향을 제어함.

## Ⅱ. 구조 및 구성요소

```text
Frozen Transformer Layer
  + Learned Prefix K/V → Attention → Task Output
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Prefix Vector | 학습 가능한 가상 K/V | layer별 삽입 |
| Frozen Base | 원본 모델 유지 | gradient 없음 |
| Prefix Length | 제어 용량 결정 | 메모리·지연 영향 |
| Prefix Store | task별 prefix 관리 | 버전 필요 |

> 요약: Prefix Tuning은 attention 내부에 학습된 K/V prefix를 추가해 모델 행동을 task별로 유도함.

## Ⅲ. 동작원리 및 흐름도

```text
base freeze → prefix 초기화 → task 학습
    → prefix 저장 → 추론 시 prefix K/V 결합 → 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | prefix 길이·적용 layer 선택 | trainable params |
| 2 | task 데이터로 prefix 학습 | validation loss |
| 3 | 추론 시 prefix K/V 주입 | KV memory |
| 4 | 정확도·지연 평가 | F1, p95 latency |

> 요약: Prefix Tuning은 작은 prefix만 학습하지만 추론 시 KV Cache와 지연 증가를 함께 측정해야 함.

## Ⅳ. 특징

| 구분 | Prompt Tuning | Prefix Tuning | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 삽입 위치 | 입력 임베딩 | layer별 K/V | 제어력 차이 |
| 학습 대상 | soft prompt | prefix vectors | 소량 params |
| 비용 | 낮음 | 중간 | KV memory 증가 |
| 한계 | 제어력 제한 | prefix 관리 필요 | task별 artifact |

> 요약: Prefix Tuning은 Prompt Tuning보다 깊은 제어가 가능하지만 KV 메모리와 관리 비용이 증가함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 생성·요약 task에 prefix length 20/50/100을 비교하고 정확도와 p95 latency 기준으로 선택
2. 업무별 prefix artifact를 registry에 저장하고 base model 버전과 호환성을 기록
3. 장문 컨텍스트 서비스는 prefix 길이가 context window와 KV Cache를 얼마나 차지하는지 계측

**결론 (2줄):**
- 기술사 판단: 입력 수준 제어는 Prompt Tuning, 더 강한 생성 제어는 Prefix Tuning, 범용 도메인 적응은 LoRA를 선택함.
- 향후 방향: Prefix Tuning은 경량 task 제어와 multi-task adapter 운영의 보조 기법으로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | prefix K/V 주입 흐름 | Prompt Tuning 대비 특징 |
| 요구사항 명시형 | 적용 방안을 제시하시오 | prefix length·KV 비용 검증 | 지연·메모리·관리 기준 |

> 요약: 설명형은 prefix attention 원리, 적용형은 prefix 길이와 KV Cache 비용 중심으로 목차를 전환함.
