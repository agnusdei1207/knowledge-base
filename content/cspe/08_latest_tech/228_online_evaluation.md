---
title: "Online Evaluation 온라인 평가 (Online Evaluation)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 228
extra:
  question_no: "228"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Online Evaluation은 실제 운영 환경에서 사용자 반응과 결과를 바탕으로 모델을 평가하는 방식임
- 오프라인 점수가 높아도 운영 성과가 낮을 수 있으므로 실전 평가는 별도로 필요함
- 실험 설계와 가드레일과 결과 해석이 평가 품질을 좌우함

## Ⅰ. 개요

- **정의/개념**: Online Evaluation은 실제 서비스 트래픽에서 모델의 응답이나 추천이나 예측이 사용자 행동과 비즈니스 KPI에 어떤 영향을 주는지 측정해 운영 적합성을 평가하는 방법임
- **배경/필요성**: 오프라인 데이터셋 기반 지표만으로는 실제 사용자 선호와 인터페이스 상호작용과 운영 편향을 반영하기 어려워 라이브 환경 검증이 필요해짐

## Ⅱ. 특징

- 실제 사용자 반응과 비즈니스 성과를 직접 측정할 수 있음
- 실험군 설계와 샘플 편향과 외부 요인의 영향을 크게 받음
- 사용자 경험 저하 가능성이 있어 안전 장치와 단계적 노출이 필요함
- 오프라인 평가와 사람 평가의 결과를 최종적으로 검증하는 단계가 됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Online Evaluation | Offline Evaluation | Human Evaluation |
|:---|:---|:---|:---|
| 평가 환경 | 실제 운영 트래픽 | 고정된 검증 데이터셋 | 평가자 샘플 리뷰 |
| 대표 지표 | CTR, conversion, retention | accuracy, NDCG, RMSE | preference, rubric score |
| 장점 | 비즈니스 효과 직접 측정 | 반복 가능하고 빠름 | 정성 품질 확인 가능 |
| 한계 | 사용자 위험과 실험 편향 | 현실 반영 한계 | 비용과 일관성 문제 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Experiment Splitter | 사용자나 세션을 대조군과 실험군으로 나눠 라이브 환경 비교를 가능하게 하는 분기 계층임 |
| Live Metric Collector | 클릭과 전환과 체류와 오류 같은 운영 KPI를 수집하는 계측 계층임 |
| Guardrail Monitor | 품질 저하와 장애와 편향 악화를 감시해 실험 중단 조건을 제공하는 안전 계층임 |
| Outcome Analyzer | 통계적 유의성과 세그먼트 차이를 분석해 실제 개선 여부를 판정하는 분석 엔진임 |
| Rollout Controller | 온라인 평가 결과에 따라 확대와 유지와 중단을 결정하는 운영 제어 계층임 |

```text
+-------------+    +----------------+    +----------------+    +------------------+
| Live Traffic| -> | Experiment Split| -> | Metric Collector| -> | Analyze/Control  |
+-------------+    +----------------+    +----------------+    +------------------+
                             |
                             v
                      +----------------+
                      | Guardrail Mon. |
                      +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 실험 설계    | -> | 트래픽 분기  | -> | KPI 수집     | -> | 통계 분석    | -> | 확대 또는 중단 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **실험 설계**: 대조군과 실험군과 평가 지표를 정의함
2. **트래픽 분기**: 실제 사용자 요청을 실험 설계에 따라 나눔
3. **KPI 수집**: 클릭과 전환과 오류와 이탈 지표를 수집함
4. **통계 분석**: 유의성과 세그먼트별 차이를 분석함
5. **확대 또는 중단**: 개선 효과와 위험 수준에 따라 배포를 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 실험 설계가 잘못되면 계절성이나 외부 캠페인 영향이 모델 개선 효과처럼 보일 수 있음
   - 해결방안: randomized assignment와 experiment guard design을 적용하고 statistical validity score와 confounding incident rate로 검증함
2. 문제: 운영 환경 실험은 실제 사용자 경험을 해칠 수 있어 품질 저하를 늦게 발견하면 피해가 커질 수 있음
   - 해결방안: guardrail KPI와 staged rollout policy를 적용하고 online experiment stop latency와 user harm incident rate로 검증함
3. 문제: 결과가 늦게 나타나는 지표만 보면 의사결정 속도가 느려지고 잘못된 조기 판단이 생길 수 있음
   - 해결방안: leading indicator와 delayed outcome analysis를 병행하고 decision lead time과 outcome revision rate로 검증함

## Ⅶ. 적용 사례

- 추천 시스템이 랜덤 분기 기반 온라인 평가를 수행하며 확인 지표는 statistical validity score와 user harm incident rate임
- 광고 입찰 모델이 가드레일 KPI와 단계적 노출을 적용하며 확인 지표는 online experiment stop latency와 confounding incident rate임
- 검색 랭킹 모델이 선행 지표와 후행 전환 지표를 함께 보며 확인 지표는 decision lead time과 outcome revision rate임

## Ⅷ. 결론

Online Evaluation은 실제 비즈니스 효과를 확인하는 최종 검증 단계이므로 실험 설계 엄밀성과 가드레일 운영이 함께 보장되어야 함.
