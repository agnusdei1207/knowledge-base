---
title: "RLHF 인간 피드백 강화학습 (Reinforcement Learning from Human Feedback)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 94
---

# 📖 【암기용】 개념 완전 이해

> 목적: RLHF를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 인간 선호 데이터를 이용해 보상모델을 학습하고, 그 보상에 맞게 LLM 정책을 최적화하는 정렬 기법
- **왜 필요한가**: 사전학습·SFT 모델은 정답처럼 보이는 문장을 만들 수 있지만, 인간이 선호하는 안전하고 유용한 답변과 다를 수 있음.
- **핵심 직관**: 학생 답안을 사람이 채점하고, 그 채점 기준을 배운 채점 모델로 학생을 다시 훈련시키는 구조임.

## 깊이 이해
- **배경·문제의식**: LLM은 next-token prediction으로 학습해 유용성·무해성·정직성을 직접 최적화하지 않는다. RLHF는 사람의 pairwise preference를 수집해 “더 나은 답변” 기준을 모델에 반영함.
- **작동 원리**: SFT 모델이 여러 답변을 생성하고, 인간 라벨러가 선호 순위를 매김. Reward Model이 선호를 학습하고, PPO 같은 RL로 정책 모델을 보상 최대화 방향으로 업데이트함.
- **비유**: 글쓰기 선생님이 여러 답안 중 더 나은 답을 고르고, 학생이 그 채점 기준에 맞춰 답안 스타일을 개선하는 것임.
- **구체 예시**: 도움됨·무해함·정직함 기준으로 pairwise preference 수만~수십만건을 수집해 assistant 모델 정렬에 활용함.
- **흔한 오해·주의점**: RLHF는 사실성 보장 기법이 아님. 선호 점수 최적화가 과하면 reward hacking과 과도한 순응 답변이 생길 수 있음.

## 연결 개념
- Alignment — RLHF의 목적
- Reward Model — 인간 선호 예측 모델
- DPO — reward model 없이 선호를 직접 최적화하는 대안

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RLHF는 인간 선호 데이터를 보상모델로 학습하고 LLM 정책을 보상 최대화 방향으로 조정하는 alignment 기법임.
> 2. **가치**: 유용성·무해성·정직성 기준을 모델 출력에 반영해 assistant 품질을 높임.
> 3. **판단 포인트**: 라벨 품질, reward hacking, PPO 안정성, 안전성 평가, 비용이 핵심임.

## Ⅰ. 개요 및 필요성

RLHF는 인간 피드백 기반 LLM 정렬 기법임. SFT 모델은 지시를 따르지만 인간 선호와 안전 기준을 충분히 반영하지 못하므로, 선호 데이터와 보상 최적화가 필요함.

## Ⅱ. 구조 및 구성요소

```text
SFT Model -> 후보 답변 생성 -> Human Preference Label
      -> Reward Model 학습 -> PPO/RL 최적화 -> Aligned Model
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Human Labeler | 답변 선호 비교 | 품질·일관성 중요 |
| Reward Model | 선호 점수 예측 | pairwise ranking |
| Policy Model | 업데이트 대상 LLM | KL penalty 필요 |
| RL Optimizer | 보상 최대화 | PPO 등 |

> 요약: RLHF는 인간 선호를 보상모델로 근사하고 정책 모델을 보상 기준에 맞게 조정함.

## Ⅲ. 동작원리 및 흐름도

```text
후보 답변 생성 -> 인간 선호 라벨링 -> RM 학습
    -> PPO 정책 업데이트 -> 안전성·품질 평가 -> 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | prompt별 후보 답변 생성 | 다양성, 품질 |
| 2 | pairwise preference 수집 | inter-rater agreement |
| 3 | reward model 학습 | ranking accuracy |
| 4 | PPO+KL로 정책 최적화 | win rate, toxicity |

> 요약: RLHF는 선호 수집, 보상모델 학습, 정책 최적화, 안전성 평가의 4단계로 운영됨.

## Ⅳ. 특징

| 구분 | SFT | RLHF | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 학습 신호 | 정답 예시 | 인간 선호 순위 | pairwise data |
| 목적 | 지시 수행 | 선호·안전 정렬 | helpful/harmless |
| 비용 | 중간 | 높음 | 라벨링·RL 비용 |
| 리스크 | 데이터 편향 | reward hacking | KL·red team 필요 |

> 요약: RLHF는 assistant 선호 정렬에 강하지만, 라벨 품질과 보상 오용을 통제해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 고객 응답·정책 질의에서 선호 라벨 50K건 이상을 수집하고 라벨러 일치도 기준을 운영
2. Reward Model 학습 후 PPO에는 KL penalty를 적용해 base model에서 과도하게 이탈하지 않게 제어
3. 배포 전 helpfulness, toxicity, hallucination, refusal rate를 red-team 평가로 측정

**결론 (2줄):**
- 기술사 판단: 인간 선호와 안전 기준 반영이 핵심이면 RLHF, 비용·단순성이 중요하면 DPO/RLAIF를 검토함.
- 향후 방향: RLHF는 고품질 alignment 기준선으로 남고, 비용 절감을 위해 AI feedback·direct preference 방식과 병행됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | preference->RM->PPO 흐름 | SFT 대비 특징 |
| 요구사항 명시형 | 정렬 방안을 제시하시오 | 라벨링·RM·red-team 절차 | 비용·안전·reward hacking 기준 |

> 요약: 설명형은 RLHF 파이프라인, 방안형은 라벨 품질과 안전성 평가 중심으로 목차를 전환함.
