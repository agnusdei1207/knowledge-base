---
title: "프롬프트 튜닝 (Prompt Tuning)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 93
---

# 📖 【암기용】 개념 완전 이해

> 목적: Prompt Tuning을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 모델 가중치를 고정하고 입력 앞에 붙는 학습 가능한 soft prompt embedding만 학습하는 PEFT 기법
- **왜 필요한가**: 자연어 프롬프트 수작업만으로는 최적 지시를 찾기 어렵고, 전체 fine-tuning은 비용이 큼.
- **핵심 직관**: 사람이 읽는 문장이 아니라 모델이 이해하는 가상 힌트 벡터를 학습해 앞에 붙이는 방식임.

## 깊이 이해
- **배경·문제의식**: Prompt Engineering은 사람이 텍스트를 바꿔가며 실험하지만, Prompt Tuning은 연속 벡터 공간에서 task에 맞는 soft prompt를 자동 학습함.
- **작동 원리**: 입력 embedding 앞에 m개의 trainable prompt vector를 붙이고, base model은 freeze한 채 prompt vector만 업데이트함. 학습된 prompt는 task별 artifact로 저장됨.
- **비유**: 시험지 앞에 모델만 볼 수 있는 보이지 않는 힌트 카드를 붙여 답변 방향을 유도하는 것과 같음.
- **구체 예시**: 분류·요약 task에서 수십 개 soft prompt token만 학습해 모델 전체 학습 없이 task 성능을 개선함.
- **흔한 오해·주의점**: soft prompt는 사람이 해석하기 어렵다. 감사·설명 가능성이 필요한 업무는 자연어 prompt와 평가 로그를 함께 관리해야 함.

## 연결 개념
- Prompt Engineering — 사람이 작성하는 hard prompt
- Prefix Tuning — layer별 K/V prefix 학습
- PEFT — Prompt Tuning의 상위 범주

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Prompt Tuning은 입력 embedding 앞의 soft prompt만 학습해 base model을 task에 적응시키는 PEFT 기법임.
> 2. **가치**: 모델 가중치 변경 없이 소량 파라미터로 task별 출력 성향을 조정함.
> 3. **판단 포인트**: prompt length, 초기화, 해석 불가능성, hard prompt와 평가 로그 병행이 핵심임.

## Ⅰ. 개요 및 필요성

Prompt Tuning은 soft prompt 기반 경량 튜닝 기법임. 전체 모델 학습 없이 입력 embedding 앞에 학습 가능한 prompt vector를 붙여 task별 성능을 개선함.

## Ⅱ. 구조 및 구성요소

```text
Trainable Soft Prompt + Input Embedding
      → Frozen LLM → Task Output
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Soft Prompt | 학습 가능한 가상 토큰 | 사람이 해석 어려움 |
| Frozen LLM | base model 유지 | gradient 없음 |
| Prompt Length | task 제어 용량 | context 사용 |
| Prompt Store | task별 prompt 저장 | 버전 관리 |

> 요약: Prompt Tuning은 입력 앞의 연속 벡터만 학습해 base model 동작을 task별로 유도함.

## Ⅲ. 동작원리 및 흐름도

```text
soft prompt 초기화 → 입력 embedding 결합 → task loss 계산
    → prompt vector만 업데이트 → 평가·저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | prompt length·초기화 선택 | 10~100 tokens |
| 2 | base freeze 후 prompt 학습 | trainable params |
| 3 | task별 prompt artifact 저장 | version, hash |
| 4 | 성능·형식 평가 | accuracy, format pass |

> 요약: Prompt Tuning은 soft prompt만 업데이트하므로 비용은 낮지만 task별 평가와 버전 관리가 필요함.

## Ⅳ. 특징

| 구분 | Prompt Engineering | Prompt Tuning | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 형태 | 자연어 hard prompt | 연속 soft vector | 해석 가능성 차이 |
| 최적화 | 수작업·탐색 | gradient 학습 | 데이터 필요 |
| 비용 | 매우 낮음 | 낮음 | 소량 params |
| 한계 | 불안정 | 감사 어려움 | 로그·평가 필요 |

> 요약: Prompt Tuning은 수작업 prompt보다 최적화 가능성이 높지만, soft prompt 해석 불가능성을 보완해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 분류·요약 task에서 prompt length 20/50/100을 비교하고 accuracy·latency 기준으로 선택
2. soft prompt artifact에 학습 데이터 버전, base model hash, 평가 결과를 함께 저장
3. 규제 업무는 자연어 system prompt와 soft prompt를 병행하고 감사 로그로 출력 근거를 보완

**결론 (2줄):**
- 기술사 판단: 빠른 task 적응은 Prompt Tuning, 강한 도메인 적응은 LoRA/Adapter, 설명 가능성은 hard prompt를 선택함.
- 향후 방향: Prompt Tuning은 자동 프롬프트 최적화와 결합해 경량 task personalization에 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | soft prompt 학습 흐름 | Prompt Engineering 대비 특징 |
| 요구사항 명시형 | 적용 방안을 제시하시오 | prompt length·artifact 관리 절차 | 성능·감사·해석성 기준 |

> 요약: 설명형은 soft prompt 원리, 적용형은 버전 관리와 감사 보완 중심으로 목차를 전환함.
