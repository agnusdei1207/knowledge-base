---
title: "Adversarial Example 적대적 예제 (Adversarial Example)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 194
extra:
  question_no: "194"
  exam_status: "기출"
  exam_history: "131회"
---

## 미리 알고가기

- 적대적 예제는 추론 시점에 미세한 교란을 더해 모델 오판을 유도하는 공격임
- 사람이 보기엔 거의 같은 입력이어도 모델은 경계 근처에서 크게 흔들릴 수 있음
- 강건성 평가는 clean accuracy와 adversarial accuracy를 함께 봐야 의미가 있음

## Ⅰ. 개요

- **정의/개념**: 적대적 예제는 정상 입력에 사람 인지 한계 이하의 계산된 교란을 추가해 모델의 결정 경계를 넘어가도록 만들어 오분류를 유도하는 공격 입력임
- **배경/필요성**: 딥러닝 모델은 고차원 특징 공간에서 작은 입력 변화에도 민감할 수 있어 자율주행과 인증과 의료처럼 안전 민감형 도메인에서 강건성 검증이 필수임

## Ⅱ. 특징

- 무작위 노이즈와 달리 손실 함수와 gradient를 이용한 최적화 기반 교란이라는 점이 핵심임
- 이미지와 텍스트와 음성 등 다양한 모달리티에 적용 가능함
- 화이트박스 환경에서는 공격 효율이 높고 블랙박스 환경에서도 전이성으로 위협이 유지됨
- 방어를 과도하게 하면 clean accuracy와 지연시간이 저하될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | FGSM | PGD | C&W |
|:---|:---|:---|:---|
| 공격 스텝 | 단일 스텝 | 반복 스텝 | 최적화 기반 |
| 계산 비용 | 낮음 | 중간 | 높음 |
| 공격 강도 | 중간 | 강함 | 매우 강함 |
| 활용 목적 | 빠른 점검 | 강건성 평가 표준 | 정교한 우회 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Clean Input | 모델이 정상적으로 분류하는 원본 입력으로 공격의 출발점이 됨 |
| Loss, Gradient Signal | 특정 타깃 오류를 극대화하는 방향을 계산하는 최적화 정보임 |
| Perturbation Budget | $\epsilon$과 norm 제약으로 사람 인지 가능성과 공격 강도를 조절함 |
| Adversarial Input | 교란이 추가된 입력으로 모델의 예측을 의도적으로 흔듦 |
| Robustness Defense | adversarial training과 전처리와 탐지 계층으로 공격 성공률을 낮춤 |

```text
+-------------------+      +-------------------+      +-------------------+
| Clean Input       | ---> | Loss / Gradient   | ---> | Perturbation      |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Adversarial Input |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 원본 입력 선택   | --> | gradient 계산    | --> | 교란 생성/주입  | --> | 오분류 성공 검증 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **원본 입력 선택**: 정상 분류되는 샘플을 기준점으로 잡음
2. **gradient 계산**: 오답 방향으로 손실을 키우는 변화를 찾음
3. **교란 생성 및 주입**: 제약 범위 안에서 입력을 수정함
4. **오분류 성공 검증**: 목표 라벨이나 오답 여부를 확인함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 고정된 입력 전처리만으로는 공격자가 그 전처리까지 고려한 적대적 예제를 다시 만들 수 있음
   - 해결방안: adversarial training과 randomized defense를 결합하고 robust accuracy와 adaptive attack success rate로 검증함
2. 문제: 강건성을 높이기 위한 방어가 과도하면 정상 데이터 정확도와 응답 지연이 함께 나빠질 수 있음
   - 해결방안: clean-robust trade-off tuning을 적용하고 clean accuracy retention과 latency overhead로 검증함
3. 문제: 블랙박스 환경에서도 전이성 때문에 내부 gradient가 없어도 공격이 성공할 수 있음
   - 해결방안: ensemble diversity와 query monitoring을 적용하고 transfer attack success rate와 anomaly query detection rate로 검증함

## Ⅶ. 적용 사례

- 자율주행 표지판 인식이 PGD 기반 강건성 평가를 통과하도록 운영되며 확인 지표는 robust accuracy와 stop-sign recall임
- 생체인증 시스템이 물리 스티커와 이미지 교란 공격을 함께 시험하며 확인 지표는 spoof success rate와 false reject rate임
- 문서 분류 모델이 텍스트 치환형 적대 예제에 대해 방어 훈련을 수행하며 확인 지표는 synonym attack success rate와 classification accuracy임

## Ⅷ. 결론

적대적 예제는 모델 정확도만으로는 드러나지 않는 안전성 취약점을 보여주므로 강건성 검증과 adversarial training이 배포 품질 기준에 포함되어야 함.
