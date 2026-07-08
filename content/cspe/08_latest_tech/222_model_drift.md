---
title: "Model Drift 모델 드리프트 (Model Drift)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 222
extra:
  question_no: "222"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- Model Drift는 운영 중 모델의 성능과 출력 특성이 기준선에서 멀어지는 현상을 포괄적으로 가리킴
- 원인은 Data Drift와 Concept Drift와 환경 변화와 서빙 설정 변화까지 다양함
- 단순 정확도만 보지 말고 예측 분포와 calibration과 비즈니스 KPI를 함께 봐야 함

## Ⅰ. 개요

- **정의/개념**: Model Drift는 운영 중인 모델의 예측 성능과 확률 분포와 안정성이 시간에 따라 기준 상태에서 벗어나 실제 서비스 품질이 저하되는 현상을 의미함
- **배경/필요성**: 모델은 고정된 알고리즘이어도 입력 환경과 사용자 행동과 인프라 설정이 변하면서 점진적으로 품질이 나빠질 수 있어 운영 관찰과 조기 대응 체계가 필요함

## Ⅱ. 특징

- Data Drift와 Concept Drift가 대표 원인이지만 임계치와 캘리브레이션 변화도 영향을 줌
- 평균 정확도보다 특정 구간 편향과 신뢰도 왜곡이 더 위험할 수 있음
- 시스템 장애가 없어도 비즈니스 성과가 떨어지는 소리 없는 실패 형태로 나타남
- 원인 분해가 중요하므로 드리프트 탐지와 RCA가 함께 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Model Drift | Data Drift | Concept Drift |
|:---|:---|:---|:---|
| 초점 | 모델 성능과 출력 변화 | 입력 분포 변화 | 입력과 정답 관계 변화 |
| 관측 지표 | accuracy, calibration, output shift | PSI, KS, feature shift | delayed label performance |
| 원인 범위 | 데이터, 개념, 운영 환경 | 데이터 변화 중심 | 라벨 관계 변화 중심 |
| 대응 방식 | 원인 진단 후 재학습 또는 재배포 | 데이터 조사와 보정 | 최신 라벨 재정의와 재학습 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Baseline Performance Profile | 배포 시점의 정확도와 확률 분포와 캘리브레이션 상태를 기준선으로 저장하는 참조 세트임 |
| Live Inference Monitor | 운영 입력과 출력과 응답 지연을 수집해 현재 모델 상태를 지속 관측하는 계층임 |
| Drift Diagnosis Engine | 입력 변화와 출력 변화와 라벨 기반 성능 저하를 함께 분석해 원인 후보를 좁히는 진단 엔진임 |
| Business KPI Mapper | 모델 지표 변화를 매출과 전환율과 손실률 같은 비즈니스 성과와 연결해 우선순위를 정하는 계층임 |
| Recovery Controller | 재학습과 재보정과 롤백과 임계치 조정을 실행하는 대응 계층임 |

```text
+------------------+    +------------------+    +-------------------+    +----------------+
| Baseline Profile | -> | Live Monitor     | -> | Diagnosis Engine  | -> | Recovery Ctrl  |
+------------------+    +------------------+    +-------------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 기준 수립    | -> | 운영 관측    | -> | 변화 감지    | -> | 원인 분석    | -> | 복구 실행    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **기준 수립**: 배포 직후 기준 성능과 출력 패턴을 저장함
2. **운영 관측**: 입력과 출력과 지연과 결과를 계속 수집함
3. **변화 감지**: 기준선 대비 성능과 분포 변화를 계산함
4. **원인 분석**: 데이터와 개념과 설정 변화 중 원인을 분해함
5. **복구 실행**: 재학습과 재배포와 보정 정책을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 성능 저하를 입력 드리프트와 운영 설정 변화로 구분하지 못하면 잘못된 대응으로 복구 시간이 길어질 수 있음
   - 해결방안: drift diagnosis pipeline과 configuration audit를 적용하고 root cause attribution accuracy와 mean time to recovery로 검증함
2. 문제: 정확도만 추적하면 확률 신뢰도 왜곡이나 특정 구간 성능 붕괴를 놓칠 수 있음
   - 해결방안: calibration monitoring과 segment performance dashboard를 적용하고 calibration error와 worst segment performance gap으로 검증함
3. 문제: 드리프트 알람 후 재학습과 롤백 기준이 없으면 운영 중 품질 저하가 장기화될 수 있음
   - 해결방안: recovery playbook과 promotion rollback policy를 적용하고 drift closure time과 rollback decision lead time으로 검증함

## Ⅶ. 적용 사례

- 추천 시스템이 출력 분포와 전환율 변화를 함께 관측하며 확인 지표는 calibration error와 drift closure time임
- 사기 탐지 모델이 원인 분해 대시보드를 운영하며 확인 지표는 root cause attribution accuracy와 mean time to recovery임
- 보험 심사 모델이 구간별 성능 감시와 롤백 기준을 사용하며 확인 지표는 worst segment performance gap과 rollback decision lead time임

## Ⅷ. 결론

Model Drift는 여러 원인이 겹친 운영 품질 저하이므로 탐지보다 원인 분해와 복구 정책 체계를 함께 갖추는 것이 중요함.
