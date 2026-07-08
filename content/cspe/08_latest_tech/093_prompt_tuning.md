---
title: "Prompt Tuning (프롬프트 튜닝)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 93
extra:
  question_no: "093"
  exam_status: "기출"
  exam_history: "135회, 136회"
---

## 미리 알고가기

- prompt tuning은 사람이 쓰는 텍스트 프롬프트가 아니라 학습 가능한 soft prompt 임베딩을 최적화하는 방식임
- base model은 고정되고 입력 앞쪽 임베딩만 조정됨
- 파라미터 수는 매우 적지만 복잡한 적응 능력은 제한될 수 있음

## Ⅰ. 개요

- **정의/개념**: prompt tuning은 사전학습된 모델의 가중치를 고정한 채 입력 임베딩 앞부분에 붙는 학습 가능한 soft prompt 벡터만 최적화해 특정 업무에 적응시키는 PEFT 기법임
- **배경/필요성**: 거대 모델을 수정하지 않고도 입력 조건만 바꿔 저비용으로 업무 성능을 높이려는 요구가 커지면서, 연속 벡터 형태의 프롬프트를 학습하는 방식이 등장함

## Ⅱ. 특징

- 학습 대상이 극히 적어 비용과 저장 공간이 매우 낮음
- hard prompt보다 자동 최적화가 가능해 수작업 프롬프트 설계 부담을 줄임
- 복잡한 추론 규칙이나 도메인 적응을 깊게 반영하기에는 표현력이 제한될 수 있음
- base model 규모가 클수록 soft prompt 효과가 더 잘 나타나는 경우가 많음

## Ⅲ. 종류 및 비교

| 판단 기준 | Manual Prompting | Prompt Tuning | Prefix Tuning |
|:---|:---|:---|:---|
| 조정 대상 | 사람이 쓴 텍스트 | 입력 임베딩 | attention prefix |
| 학습 비용 | 없음 | 매우 낮음 | 매우 낮음 |
| 자동 최적화 | 없음 | 가능 | 가능 |
| 제어 범위 | 제한적임 | 제한적임 | 중간 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Soft Prompt Embeddings | 학습 가능한 연속 벡터로 입력 조건을 형성해 모델 출력을 유도함 |
| Frozen Base Model | 원래 가중치를 유지한 채 soft prompt의 영향만 반영함 |
| Task Dataset | 특정 업무의 입력과 정답을 제공해 soft prompt를 최적화함 |
| Evaluation Harness | 작은 파라미터로 얻는 성능 향상과 일반화 한계를 함께 확인함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| soft prompt 초기화 | --> | 입력 앞 임베딩 결합 | --> | prompt만 학습   | --> | 태스크별 적용    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **soft prompt 초기화**: 학습 가능한 프롬프트 임베딩을 준비함
2. **입력 앞 임베딩 결합**: 실제 입력 토큰 앞에 soft prompt를 붙임
3. **prompt만 학습**: base model은 고정하고 soft prompt만 업데이트함
4. **태스크별 적용**: 업무별 soft prompt를 선택해 추론에 사용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: soft prompt 표현력이 제한적이면 복잡한 업무에서 full FT나 LoRA 수준의 성능 향상을 내기 어려울 수 있음
   - 해결방안: 단순 태스크와 스타일 제어에 우선 적용하고 benchmark score와 parameter efficiency로 적합성을 검증함
2. 문제: 입력 분포가 바뀌면 학습된 soft prompt가 쉽게 흔들려 일반화 성능이 낮아질 수 있음
   - 해결방안: 다양한 입력 변형을 포함해 학습하고 held-out distribution score와 robustness metric으로 일반화를 검증함
3. 문제: 사람이 보는 프롬프트가 아니라서 디버깅과 해석이 어려울 수 있음
   - 해결방안: hard prompt baseline과 함께 비교 운영하고 ablation score와 failure taxonomy로 원인 분석 가능성을 검증함

## Ⅶ. 적용 사례

- 분류와 추출 태스크: 저비용으로 여러 업무를 빠르게 실험함, 확인 지표는 accuracy와 turnaround time임
- 응답 톤 제어: 짧은 문체, 친절한 문체를 유도함, 확인 지표는 style adherence와 user preference임
- 대규모 모델 벤치마크: 적은 파라미터로 태스크 적응 효과를 비교함, 확인 지표는 parameter efficiency와 benchmark score임

## Ⅷ. 결론

prompt tuning은 가장 가벼운 PEFT 방식 중 하나이므로, 높은 적응력보다 저비용 실험성과 빠른 태스크 전환이 중요한 환경에서 특히 유리함.
