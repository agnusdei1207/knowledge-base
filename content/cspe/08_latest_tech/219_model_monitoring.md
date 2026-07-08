---
title: "Model Monitoring 모델 모니터링 (Model Monitoring)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 219
extra:
  question_no: "219"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Model Monitoring은 배포 이후 모델이 실제 환경에서 얼마나 안정적으로 동작하는지 관찰하는 운영 관측 체계임
- 시스템 지표뿐 아니라 입력 분포와 예측 품질과 드리프트를 함께 봐야 함
- 경고만 내는 수준을 넘어 재학습과 롤백 같은 후속 액션과 연결되어야 가치가 커짐

## Ⅰ. 개요

- **정의/개념**: Model Monitoring은 운영 중인 모델의 입력 데이터와 예측 결과와 지연 시간과 오류와 성능 지표를 지속 수집해 이상 징후와 품질 저하를 조기에 탐지하는 관측 체계임
- **배경/필요성**: 모델은 배포 이후에도 데이터 변화와 환경 변화와 서비스 부하 영향으로 성능이 달라지므로 운영 가시성이 없으면 소리 없는 실패가 장기화될 수 있음

## Ⅱ. 특징

- 시스템 모니터링과 데이터 모니터링과 성능 모니터링을 함께 다뤄야 함
- label lag가 존재하므로 즉시 알 수 있는 대리지표도 함께 관리해야 함
- 알람 설계가 과하면 피로가 높아지고 약하면 장애를 놓칠 수 있음
- MLOps 재학습 루프와 연결할 때 실질적 가치가 높아짐

## Ⅲ. 종류 및 비교

| 판단 기준 | Model Monitoring | System Monitoring | Data Drift Detection |
|:---|:---|:---|:---|
| 관측 범위 | 입력, 예측, 성능, 지연 | CPU, 메모리, 에러율 | 입력 분포 변화 |
| 핵심 목적 | 모델 품질 유지 | 서비스 가용성 유지 | 선행 이상 감지 |
| 대표 지표 | drift, accuracy, latency | P99, 5xx, throughput | PSI, KS, feature shift |
| 후속 조치 | retrain, rollback, threshold tune | scale out, restart | data investigation |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Telemetry Collector | 입력 피처와 예측과 시스템 지표를 수집해 분석 가능한 관측 데이터를 만드는 계층임 |
| Baseline Store | 학습 시점과 정상 운영 시점의 기준 분포와 성능 수치를 저장하는 참조 저장소임 |
| Drift and Quality Analyzer | 입력 분포 변화와 예측 편향과 품질 이상을 계산해 조기 경보를 만드는 분석 엔진임 |
| Performance Evaluator | 확보된 정답과 예측을 비교해 정확도와 F1과 비즈니스 KPI를 계산하는 후행 평가 계층임 |
| Alert and Action Hook | 알람을 발송하고 재학습이나 롤백이나 심화 조사 절차를 호출하는 운영 연결부임 |

```text
+-------------+    +--------------+    +-------------------+    +----------------+
| Live Inputs | -> | Telemetry    | -> | Drift/Quality     | -> | Alert/Action   |
+-------------+    +--------------+    +-------------------+    +----------------+
        |                    |
        v                    v
 +-------------+      +--------------+
 | Predictions |      | Baseline Store|
 +-------------+      +--------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 운영 수집    | -> | 기준 비교    | -> | 이상 탐지    | -> | 알람 생성    | -> | 조치 연계    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **운영 수집**: 입력과 예측과 시스템 상태를 수집함
2. **기준 비교**: 저장된 baseline과 현재 상태를 비교함
3. **이상 탐지**: 드리프트와 성능 하락과 이상치를 계산함
4. **알람 생성**: 임계치 초과 시 사건을 발행함
5. **조치 연계**: 재학습과 롤백과 수동 검토 절차를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 정답 데이터가 늦게 들어오면 실제 성능 저하를 뒤늦게 알아차려 대응 시점을 놓칠 수 있음
   - 해결방안: proxy metric monitoring과 delayed label evaluation을 적용하고 drift to label confirmation gap과 early warning precision으로 검증함
2. 문제: 알람 기준이 지나치게 민감하면 운영자가 중요한 경고를 놓치는 알람 피로가 커질 수 있음
   - 해결방안: priority based alerting과 adaptive threshold tuning을 적용하고 alert precision과 alert fatigue index로 검증함
3. 문제: 모니터링이 단순 대시보드 수준에 머물면 이상 감지 후 재학습과 롤백이 지연될 수 있음
   - 해결방안: action hook automation과 runbook integration을 적용하고 mean time to mitigation과 automated action coverage로 검증함

## Ⅶ. 적용 사례

- 추천 시스템이 입력 분포와 정답 지연 성능을 함께 관측하며 확인 지표는 early warning precision과 drift to label confirmation gap임
- 사기 탐지 모델이 중요도 기반 알람 정책을 운영하며 확인 지표는 alert precision과 alert fatigue index임
- 제조 비전 AI가 이상 감지 후 자동 재학습 런북을 호출하며 확인 지표는 mean time to mitigation과 automated action coverage임

## Ⅷ. 결론

Model Monitoring은 모델 운영의 경보 체계이므로 관측 자체보다 적절한 기준과 후속 조치 연결이 설계의 핵심임.
