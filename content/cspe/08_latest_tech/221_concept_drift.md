---
title: "Concept Drift 개념 드리프트 (Concept Drift)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 221
extra:
  question_no: "221"
  exam_status: "기출"
  exam_history: "124회, 135회"
---

## 미리 알고가기

- Concept Drift는 입력 데이터가 같아도 정답과의 관계가 달라지는 현상임
- Data Drift보다 탐지가 어려운 이유는 실제 라벨이나 결과 피드백이 필요하기 때문임
- 재학습만으로 끝나지 않고 라벨 정의와 비즈니스 규칙 변경까지 함께 점검해야 함

## Ⅰ. 개요

- **정의/개념**: Concept Drift는 시간 경과나 환경 변화로 인해 동일한 입력 피처에 대한 정답 관계와 의사결정 경계가 달라져 기존 모델의 판단 기준이 더 이상 유효하지 않게 되는 현상임
- **배경/필요성**: 시장 변화와 사용자 행동 변화와 정책 변경이 빠른 환경에서는 학습 당시 유효했던 패턴이 운영 중에 무너져 성능 저하가 조용히 누적될 수 있음

## Ⅱ. 특징

- 입력 분포가 안정적이어도 정답 규칙이 바뀌면 성능이 급격히 나빠질 수 있음
- 정답 확보가 늦을수록 문제를 뒤늦게 발견하는 label lag 문제가 큼
- 국소 구간이나 특정 집단에서만 드리프트가 생길 수도 있어 세분 모니터링이 필요함
- 모델 재학습뿐 아니라 라벨 정책과 의사결정 규칙 변경 여부도 함께 점검해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Concept Drift | Data Drift | Model Drift |
|:---|:---|:---|:---|
| 변화 대상 | P(Y|X) 관계 변화 | P(X) 분포 변화 | 모델 성능과 출력 특성 전반 |
| 탐지 난이도 | 높음 | 상대적으로 낮음 | 중간 |
| 필요 정보 | 실제 결과 라벨 | 입력 데이터만으로 가능 | 운영 지표와 결과 혼합 |
| 우선 대응 | 최신 라벨 기반 재학습 | 분포 조사와 데이터 보정 | 원인 분석 후 재배포 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Baseline Label Relation | 학습 시점의 입력과 정답 관계를 기준선으로 저장해 이후 변화 여부를 판단하는 참조 모델임 |
| Outcome Feedback Store | 실제 결과와 정답 라벨을 수집해 운영 예측과 비교할 수 있게 하는 피드백 저장소임 |
| Drift Evaluator | 시점별 성능과 오차 패턴을 분석해 개념 변화가 발생했는지 추정하는 분석 엔진임 |
| Segment Analyzer | 고객군과 시간대와 지역별로 성능 저하를 분해해 부분적 드리프트를 찾는 계층임 |
| Retraining and Policy Loop | 드리프트 확인 후 데이터 갱신과 규칙 재정의와 재배포를 연결하는 조치 계층임 |

```text
+------------------+    +------------------+    +----------------+    +------------------+
| Baseline Relation| -> | Live Outcomes    | -> | Drift Evaluator| -> | Retrain/Policy   |
+------------------+    +------------------+    +----------------+    +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 기준 성능 저장 | -> | 실제 결과 수집 | -> | 예측과 비교    | -> | 변화 판정    | -> | 재학습 및 수정 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **기준 성능 저장**: 학습 시점의 라벨 관계와 기준 성능을 저장함
2. **실제 결과 수집**: 운영에서 발생한 실제 정답과 피드백을 확보함
3. **예측과 비교**: 과거 기준과 현재 예측 오차 패턴을 비교함
4. **변화 판정**: 단순 노이즈인지 개념 변화인지 판단함
5. **재학습 및 수정**: 최신 데이터와 규칙으로 모델과 정책을 갱신함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 실제 결과 라벨이 늦게 들어오면 개념 변화가 발생해도 장기간 감지하지 못해 손실이 누적될 수 있음
   - 해결방안: delayed label monitoring과 proxy metric early warning을 적용하고 concept drift detection lag와 early warning precision으로 검증함
2. 문제: 특정 고객군이나 시간대에서만 개념 변화가 생기면 전체 평균 성능만으로는 이상을 놓칠 수 있음
   - 해결방안: segment level evaluation과 cohort monitoring을 적용하고 segment drift recall과 localized performance drop detection rate로 검증함
3. 문제: 비즈니스 규칙과 라벨 정의가 바뀌었는데 모델만 재학습하면 잘못된 기준을 계속 학습할 수 있음
   - 해결방안: label policy review와 joint retraining governance를 적용하고 label definition freshness score와 policy update alignment rate로 검증함

## Ⅶ. 적용 사례

- 신용평가 모델이 실제 연체 결과를 기반으로 개념 변화를 추적하며 확인 지표는 concept drift detection lag와 segment drift recall임
- 광고 클릭 예측 모델이 캠페인 유형별 코호트 평가를 수행하며 확인 지표는 localized performance drop detection rate와 early warning precision임
- 사기 탐지 시스템이 라벨 규칙 변경 검토와 재학습을 연계하며 확인 지표는 label definition freshness score와 policy update alignment rate임

## Ⅷ. 결론

Concept Drift는 입력보다 정답 관계가 바뀌는 더 어려운 운영 문제이므로 최신 라벨 피드백과 세분 성능 분석과 정책 검토를 함께 운영해야 함.
