---
title: "Model Inversion 모델 역전 (Model Inversion)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 191
extra:
  question_no: "191"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- 모델 역전은 모델 출력이나 내부 정보를 이용해 학습 데이터의 특징을 거꾸로 복원하려는 프라이버시 공격임
- 모델 추출이 기능 복제라면 모델 역전은 학습 데이터 복원에 더 가깝다는 점이 다름
- 확률 점수와 gradient 접근 권한이 많을수록 공격 난도가 크게 낮아짐

## Ⅰ. 개요

- **정의/개념**: 모델 역전은 모델이 반환하는 예측 점수나 경사 정보를 활용해 특정 클래스나 개인과 관련된 입력 특징을 역으로 최적화하여 학습 데이터의 민감한 속성을 복원하는 공격임
- **배경/필요성**: 안면 인식과 의료 예측처럼 민감 데이터로 학습된 모델이 외부 질의에 응답할 때, 과적합과 풍부한 출력 정보가 결합되면 학습 데이터 프라이버시가 침해될 위험이 커짐

## Ⅱ. 특징

- 출력 확률과 gradient를 많이 제공할수록 공격 정확도가 높아짐
- 특정 개인이나 클래스의 대표 특징을 복원해 재식별 위험을 높일 수 있음
- 화이트박스 환경에서는 경사 기반 최적화가 가능해 공격 효율이 더 커짐
- 차등 프라이버시와 과적합 완화가 근본 방어에 가깝고 단순 API 가리기만으로는 충분하지 않을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Model Inversion | Membership Inference | Model Extraction |
|:---|:---|:---|:---|
| 공격 목표 | 입력 특징 복원 | 학습 포함 여부 판정 | 기능 복제 |
| 핵심 정보 | 확률 점수, gradient | confidence pattern | 대량 입출력 쌍 |
| 피해 유형 | 개인정보 재구성 | 프라이버시 포함 여부 노출 | 지식재산 도난 |
| 대표 방어 | DP, confidence 제한 | calibration, DP | rate limit, watermark |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Target Model | 민감 데이터로 학습되어 출력 패턴 안에 입력 특징을 간접적으로 담고 있는 대상 모델임 |
| Query, Score Interface | 공격자가 반복 질의와 confidence score를 통해 복원 방향을 찾는 관측 채널임 |
| Optimization Engine | 특정 클래스 점수를 높이는 방향으로 입력을 갱신해 대표 특징을 재구성함 |
| Reconstructed Sample | 원본과 완전히 같지 않아도 식별 가능한 수준의 민감 특징을 담은 결과물임 |
| Privacy Defense Layer | DP와 과적합 완화와 응답 축소로 복원 가능성을 낮추는 방어 계층임 |

```text
+-------------------+      +-------------------+      +-------------------+
| Query / Seed      | ---> | Target Model      | ---> | Score / Gradient  |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Optimize / Rebuild|
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 목표 클래스 설정  | --> | 반복 질의/점수 관측 | --> | 입력 역최적화   | --> | 복원 특징 검증  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **목표 클래스 설정**: 공격자가 복원하려는 개인이나 라벨을 정함
2. **반복 질의 및 점수 관측**: 모델 출력과 confidence 변화를 수집함
3. **입력 역최적화**: 점수를 높이는 방향으로 입력을 점진적으로 수정함
4. **복원 특징 검증**: 복원 결과가 재식별 수준인지 평가함

## Ⅵ. 문제점 및 해결 방안

1. 문제: confidence score를 세밀하게 공개하면 공격자가 결정 경계와 민감 특징을 정교하게 추정할 수 있음
   - 해결방안: score truncation과 label-only response를 적용하고 inversion success rate와 user utility score로 검증함
2. 문제: 과적합된 모델은 특정 샘플 특징을 더 선명하게 기억해 복원 위험을 키울 수 있음
   - 해결방안: regularization과 DP-SGD를 적용하고 train-test gap과 privacy leakage metric으로 검증함
3. 문제: 화이트박스나 내부 API 환경에서 gradient 접근이 가능하면 공격 효율이 급격히 높아질 수 있음
   - 해결방안: gradient isolation과 privileged access control을 적용하고 unauthorized gradient access rate와 leakage resistance score로 검증함

## Ⅶ. 적용 사례

- 안면 인식 API가 confidence 응답을 축소하고 운영되며 확인 지표는 inversion success rate와 face match accuracy임
- 의료 예측 모델이 DP 기반 학습으로 민감 환자 특징 복원을 억제하며 확인 지표는 privacy leakage score와 model AUC임
- 금융 예측 서비스가 내부 분석용 점수 API를 별도 격리하고 운영되며 확인 지표는 privileged score access rate와 privacy incident rate임

## Ⅷ. 결론

모델 역전은 모델이 학습 데이터의 흔적을 얼마나 강하게 기억하는지 드러내는 공격이므로 응답 정보량 축소와 프라이버시 보존 학습이 함께 적용되어야 함.
