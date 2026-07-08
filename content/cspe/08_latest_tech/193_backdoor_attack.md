---
title: "Backdoor Attack 백도어 공격 (Backdoor Attack)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 193
extra:
  question_no: "193"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- 백도어 공격은 특정 트리거가 있을 때만 악성 동작을 일으키도록 모델 내부에 숨은 규칙을 심는 공격임
- 평상시 정확도가 높게 유지될 수 있어 일반 검증셋으로는 놓치기 쉬움
- 데이터 오염과 모델 가중치 변조가 대표 침투 경로임

## Ⅰ. 개요

- **정의/개념**: 백도어 공격은 훈련 데이터나 가중치에 비밀 트리거와 타깃 동작을 심어 두고, 평상시에는 정상처럼 보이지만 특정 패턴 입력에서만 공격자가 원하는 오분류를 유도하는 공격임
- **배경/필요성**: 오픈소스 모델 재사용과 외부 데이터 의존이 커지면서 은닉성이 높은 모델 수준 공급망 공격이 쉬워졌고, 안전 민감형 시스템에서 작은 트리거가 치명적 결과를 만들 수 있게 됨

## Ⅱ. 특징

- clean input에서는 정상 성능을 보여 탐지가 어려움
- 특정 이미지 패치나 문자열 같은 trigger가 있을 때만 공격이 발동함
- 소수의 오염 샘플만으로도 모델 내부 shortcut이 형성될 수 있음
- 모델 교체나 재학습 전까지 장기간 잠복할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Dirty-label Backdoor | Clean-label Backdoor | Weight-level Backdoor |
|:---|:---|:---|:---|
| 주입 방식 | 라벨과 트리거 동시 변조 | 라벨은 유지, 특징 충돌 유도 | 모델 가중치 직접 변조 |
| 탐지 난도 | 중간 | 높음 | 높음 |
| 주요 경로 | 데이터셋 오염 | 정교한 샘플 설계 | 오픈소스 모델 허브 |
| 대표 방어 | data scrub | feature anomaly scan | signed weight, model scan |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Trigger Pattern | 작은 패치와 문자열과 특정 토큰처럼 공격 발동을 위한 비밀 스위치 역할을 함 |
| Poisoned Samples | 트리거가 포함된 오염 샘플이 모델에게 비정상적 shortcut을 학습시킴 |
| Target Label, Behavior | 트리거가 있을 때 강제될 오분류나 정책 우회 결과를 정의함 |
| Latent Backdoor Circuit | 모델 내부 뉴런과 특징 경로에 은닉된 발동 회로가 형성됨 |
| Detection, Pruning Defense | 이상 활성화 탐지와 가지치기와 검증셋 확장으로 백도어를 찾고 약화시킴 |

```text
+-------------------+      +-------------------+      +-------------------+
| Trigger Pattern   | ---> | Poisoned Samples  | ---> | Train / Fine-tune |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Hidden Circuit    |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 트리거 샘플 준비  | --> | 오염 데이터 학습  | --> | 잠복 회로 형성  | --> | 트리거 입력 시 발동 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **트리거 샘플 준비**: 공격자가 패턴과 타깃 라벨을 설계함
2. **오염 데이터 학습**: 소수의 오염 샘플을 데이터에 섞어 학습시킴
3. **잠복 회로 형성**: 모델이 트리거와 타깃 결과의 shortcut을 학습함
4. **트리거 입력 시 발동**: 평소 정상 동작 중 특정 트리거에서만 오동작함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 검증셋이 clean data 위주이면 백도어 모델이 높은 정확도를 유지해 배포 전 탐지를 통과할 수 있음
   - 해결방안: trigger search와 stress validation을 적용하고 attack success rate와 clean accuracy gap으로 검증함
2. 문제: 오픈소스 가중치나 외부 파인튜닝 산출물을 그대로 쓰면 weight-level backdoor를 눈치채기 어려울 수 있음
   - 해결방안: signed model registry와 white-box scanning을 적용하고 model provenance coverage와 anomaly activation score로 검증함
3. 문제: 백도어 제거를 위해 과도한 pruning을 적용하면 정상 성능까지 함께 떨어질 수 있음
   - 해결방안: fine-pruning과 selective retraining을 적용하고 clean accuracy retention과 backdoor removal rate로 검증함

## Ⅶ. 적용 사례

- 자율주행 표지판 인식 모델이 trigger patch 기반 오분류 시험을 통과하도록 검증되며 확인 지표는 attack success rate와 stop-sign recall임
- 기업 내부 이미지 분류 모델이 오픈소스 체크포인트 도입 전 backdoor scan을 수행하며 확인 지표는 anomalous neuron score와 registry trust coverage임
- LLM 파인튜닝 파이프라인이 특정 trigger 문구의 정책 우회 여부를 점검하며 확인 지표는 jailbreak backdoor rate와 clean completion quality임

## Ⅷ. 결론

백도어 공격은 정상 성능 뒤에 숨는 은닉형 공급망 위협이므로 trigger 중심 검증과 모델 출처 신뢰 체계를 함께 운영해야 함.
