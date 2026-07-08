---
title: "Bias Mitigation 편향 완화 (Bias Mitigation)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 175
extra:
  question_no: "175"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- 편향 완화는 편향을 발견한 뒤 데이터와 모델과 결과 단계에서 개입하는 엔지니어링 절차임
- 어떤 편향을 줄일지 결정하려면 먼저 공정성 지표와 보호 집단을 명확히 정해야 함
- 공정성을 높일수록 정확도나 운영 단순성이 일부 희생될 수 있어 기준 합의가 필요함

## Ⅰ. 개요

- **정의/개념**: 편향 완화는 AI 모델이 특정 집단에 불리한 결과를 내지 않도록 데이터 전처리와 학습 제약과 결과 보정 기법을 적용해 공정성 격차를 줄이는 기술적 조정 과정임
- **배경/필요성**: 과거 데이터에 포함된 구조적 차별과 표본 불균형은 모델이 그대로 학습해 증폭할 수 있으므로, 단순 성능 개선만으로는 차별적 결과를 해결하기 어려움

## Ⅱ. 특징

- 편향 완화는 데이터 품질 개선과 알고리즘 수정과 운영 판단을 함께 요구하는 다층 작업임
- 보호 집단과 공정성 목표를 어떻게 정의하느냐에 따라 적용 기법과 결과가 달라짐
- 사후 임계치 조정은 빠르지만 구조적 원인을 남길 수 있고 학습 단계 개입은 효과가 크지만 구현 복잡도가 높음
- 공정성 향상과 정확도 유지 사이의 균형을 명시적으로 관리해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Pre-processing | In-processing | Post-processing |
|:---|:---|:---|:---|
| 개입 위치 | 학습 데이터 | 학습 알고리즘 | 예측 결과 |
| 대표 방식 | reweighing, resampling | fairness constraint, adversarial debiasing | threshold adjustment |
| 장점 | 범용성이 높음 | 공정성과 성능을 함께 최적화 가능 | 기존 모델에 빠르게 적용 가능 |
| 한계 | 데이터 왜곡 가능성 | 구현 난도와 모델 종속성 | 구조적 편향이 남을 수 있음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Bias Diagnosis | 보호 집단과 fairness metric을 정하고 현재 격차를 수치화해 개입 목표를 명확히 함 |
| Data-level Mitigation | 표본 재가중과 샘플링과 proxy feature 정리로 학습 데이터의 불균형을 완화함 |
| Model-level Mitigation | 손실 함수와 제약 조건을 조정해 모델이 편향 신호를 덜 학습하도록 유도함 |
| Output-level Mitigation | 임계치와 후처리 규칙을 조정해 예측 결과의 집단 간 격차를 줄임 |
| Monitoring, Governance | 배포 후 fairness metric과 민원을 감시해 재학습과 정책 재조정을 연결함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Bias Diagnosis    | ---> | Data / Model Fix  | ---> | Output Adjustment |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Monitor / Govern  |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 편향 지표 측정   | --> | 개입 방식 선택  | --> | 성능/공정성 검증 | --> | 배포 후 재모니터링 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **편향 지표 측정**: 기준 모델의 집단 간 격차를 수치화함
2. **개입 방식 선택**: 데이터와 모델과 결과 단계 중 적절한 완화 기법을 고름
3. **성능 및 공정성 검증**: accuracy와 fairness metric 변화를 함께 비교함
4. **배포 후 재모니터링**: 운영 중 격차 재발 여부를 추적함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 어떤 공정성 지표를 목표로 할지 합의 없이 완화 기법을 적용하면 팀마다 서로 다른 결과를 공정하다고 주장할 수 있음
   - 해결방안: metric selection policy를 먼저 정하고 fairness gap target과 approval consistency로 검증함
2. 문제: 민감 변수를 제거해도 우편번호 같은 대체 변수로 편향이 다시 유입되어 완화 효과가 약해질 수 있음
   - 해결방안: proxy feature analysis와 feature audit를 수행하고 residual bias level과 proxy correlation reduction으로 검증함
3. 문제: 정확도 하락 한계를 정하지 않으면 공정성 개선 이후 현업이 모델 활용을 거부할 수 있음
   - 해결방안: fairness-utility threshold를 사전 합의하고 accuracy retention과 fairness gain으로 검증함

## Ⅶ. 적용 사례

- 대출 심사 모델이 지역과 성별 편향을 줄이기 위해 재가중과 임계치 보정을 병행하며 확인 지표는 equal opportunity gap과 approval accuracy임
- 채용 AI가 이력서 필터링 단계에서 proxy feature를 제거하고 운영되며 확인 지표는 subgroup selection rate와 recruiter override rate임
- 생성형 AI 안전성 모델이 독성 표현 편향을 줄이기 위해 preference tuning을 적용하며 확인 지표는 toxicity disparity와 answer helpfulness score임

## Ⅷ. 결론

편향 완화는 단일 알고리즘으로 끝나는 문제가 아니라 공정성 목표와 성능 한계를 합의한 뒤 데이터와 모델과 운영을 함께 조정하는 반복적 최적화 과정임.
