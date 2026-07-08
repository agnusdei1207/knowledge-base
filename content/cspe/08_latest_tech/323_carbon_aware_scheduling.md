---
title: "Carbon-aware Scheduling 탄소인지 스케줄링 (Carbon-aware Scheduling)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 323
extra:
  question_no: "323"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Carbon-aware Scheduling은 작업을 전력망 탄소 강도가 낮은 시간이나 지역으로 옮겨 배출량을 줄이는 실행 정책임
- 모든 작업이 이동 가능한 것은 아니므로 delay tolerance와 business criticality 분류가 선행되어야 함
- 비용 최적화 스케줄링과 유사해 보이지만 최적화 목표가 탄소 강도라는 점이 다름

## Ⅰ. 개요

- **정의/개념**: Carbon-aware Scheduling은 워크로드의 실행 시점과 지역과 자원 선택을 조정해 전력 탄소 강도가 낮은 환경에서 작업을 처리하도록 만드는 지속가능 실행 스케줄링 기법임
- **배경/필요성**: 재생에너지 비중과 전력망 탄소 강도는 시간과 지역에 따라 크게 변하므로 동일한 작업도 언제 어디서 실행하느냐에 따라 탄소 배출이 크게 달라질 수 있음

## Ⅱ. 특징

- 지연 허용 작업을 시간 이동이나 지역 이동으로 재배치해 배출을 줄임
- 전력망 carbon signal과 workload SLA를 함께 고려하는 다목적 최적화 구조임
- 클라우드 멀티리전과 배치 처리와 학습 작업에 적용 효과가 큼
- 탄소 절감만 과도하게 추구하면 비용 상승과 성능 저하와 데이터 이동 부담이 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Carbon-aware Scheduling | Cost-aware Scheduling | Performance-aware Scheduling |
|:---|:---|:---|:---|
| 최적화 목표 | 탄소 배출 최소화 | 비용 최소화 | 지연과 처리량 최적화 |
| 주요 입력 | grid carbon signal, SLA | price signal | latency, load |
| 이동 전략 | 시간/지역 이동 | 시간/자원 이동 | 자원 확장 중심 |
| 대표 활용 | 배치, AI 학습, 백업 | 저가 시간대 작업 | 사용자 서비스 처리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Carbon Signal Feed | 전력망의 시간대별 및 지역별 탄소 강도 정보를 제공해 스케줄링 판단의 기준을 만드는 외부 입력 계층임 |
| Workload Classification | 작업의 지연 허용도와 데이터 중력과 중요도를 분류해 실제 이동 가능한 작업을 선별하는 정책 계층임 |
| Scheduling Policy Engine | 탄소와 비용과 SLA를 함께 계산해 언제 어디서 실행할지 결정하는 최적화 의사결정 계층임 |
| Placement and Orchestration | 리전과 클러스터와 실행 시간을 실제로 할당해 결정된 계획을 운영 환경에 반영하는 실행 계층임 |
| Verification Metrics | 탄소 절감과 비용 증가와 SLA 영향을 측정해 정책의 실효성을 검증하는 관측 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Carbon Feed | -> | Workload    | -> | Policy      | -> | Placement   |
|             |    | Classifier  |    | Engine      |    | / Runtime   |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 탄소 신호 수집 | -> | 작업 유연성 분류 | -> | 실행 시점/지역 결정 | -> | 스케줄 반영   | -> | 절감 효과 검증 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **탄소 신호 수집**: 시간대와 지역별 탄소 강도 데이터를 수집함
2. **작업 유연성 분류**: SLA와 데이터 위치를 기준으로 이동 가능 작업을 선별함
3. **실행 시점과 지역 결정**: 탄소와 비용과 성능을 함께 고려해 배치 위치를 정함
4. **스케줄 반영**: 오케스트레이터가 실제 실행 계획을 적용함
5. **절감 효과 검증**: 탄소 절감과 SLA 영향도를 다시 측정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 탄소 강도 예측 오차가 크면 실제로는 고탄소 시간대에 작업이 실행되어 기대한 감축 효과가 사라질 수 있음
   - 해결방안: forecast confidence aware policy와 real time rescheduling을 적용하고 prediction error adjusted carbon savings와 reschedule success rate로 검증함
2. 문제: 데이터 지역 이동 비용과 지연 영향을 무시하면 탄소 절감보다 네트워크 비용과 성능 저하가 더 커질 수 있음
   - 해결방안: data gravity constraint와 network aware placement rule을 적용하고 carbon saved per GB moved와 latency impact after relocation으로 검증함
3. 문제: 중요한 온라인 작업까지 일괄 이동 대상으로 포함하면 사용자 SLA와 운영 안정성이 깨질 수 있음
   - 해결방안: critical workload exclusion policy와 delay tolerance tiering을 적용하고 protected critical workload coverage와 SLA breach count from carbon shifting으로 검증함

## Ⅶ. 적용 사례

- AI 학습 플랫폼이 예측 신뢰도 기반 재스케줄링을 운영하며 확인 지표는 prediction error adjusted carbon savings와 reschedule success rate임
- 멀티리전 배치 시스템이 데이터 중력 제약을 적용하며 확인 지표는 carbon saved per GB moved와 latency impact after relocation임
- 온라인 서비스 조직이 중요 워크로드 제외 정책을 운영하며 확인 지표는 protected critical workload coverage와 SLA breach count from carbon shifting임

## Ⅷ. 결론

Carbon-aware Scheduling은 단순 시간 이동이 아니라 탄소 신호와 데이터 위치와 SLA를 함께 고려하는 의사결정 문제이므로 이동 가능 작업의 선별이 핵심임.
