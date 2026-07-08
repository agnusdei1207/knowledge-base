---
title: "Continuous Evaluation 지속 평가 (Continuous Evaluation)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 232
extra:
  question_no: "232"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Continuous Evaluation은 모델과 프롬프트와 데이터 파이프라인 변경이 있을 때마다 평가를 반복 수행하는 운영 체계임
- 일회성 테스트와 달리 배포 전후를 모두 포함해 회귀를 계속 감시한다는 점이 핵심임
- benchmark 최신화와 경보 임계치와 자동 조치 연결이 품질을 좌우함

## Ⅰ. 개요

- **정의/개념**: Continuous Evaluation은 모델과 프롬프트와 데이터와 서빙 설정이 변경될 때마다 오프라인과 온라인 평가를 반복 수행해 품질 회귀와 안전성 저하를 지속적으로 탐지하는 평가 운영 체계임
- **배경/필요성**: 생성형 AI와 ML 시스템은 작은 설정 변경도 결과 품질에 큰 영향을 줄 수 있어 배포 시점마다 자동 평가를 수행하는 지속적 검증 구조가 필요함

## Ⅱ. 특징

- 평가를 개발 단계와 배포 단계와 운영 단계에 걸쳐 연속적으로 수행함
- 정량 지표와 정성 지표와 안전성 지표를 함께 본다는 점이 중요함
- benchmark와 운영 샘플을 같이 써야 현실 반영과 재현성을 동시에 얻을 수 있음
- 경고만 쌓는 구조보다 배포 게이트와 재학습 루프 연결이 중요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Continuous Evaluation | One Time Benchmark | Continuous Monitoring |
|:---|:---|:---|:---|
| 시점 | 변경마다 반복 | 특정 시점 단발 | 운영 중 상시 관측 |
| 평가 대상 | 품질, 안전성, 비용, 회귀 | 기준 성능 | 실시간 이상 신호 |
| 강점 | 회귀 조기 차단 | 단순 비교 용이 | 운영 변동 반영 |
| 한계 | 운영 비용과 관리 복잡도 | 최신성 부족 | 원인 검증 한계 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Benchmark Suite | 대표 입력과 골든 셋과 안전성 케이스를 포함해 반복 평가 기준을 제공하는 테스트 세트임 |
| Evaluation Orchestrator | 코드 변경과 프롬프트 변경과 모델 변경을 감지해 평가 파이프라인을 자동 실행하는 제어 계층임 |
| Metric and Judge Engine | 정량 지표와 judge 기반 정성 평가를 수행해 다면적 결과를 산출하는 평가 엔진임 |
| Regression Gate | 이전 기준 대비 품질 하락과 안전성 위반을 판정해 배포 허용 여부를 결정하는 게이트임 |
| Feedback and Refresh Loop | 운영 샘플과 사람 평가 결과를 반영해 벤치마크와 기준선을 갱신하는 지속 개선 루프임 |

```text
+----------------+    +-------------------+    +----------------+    +----------------+
| Benchmark Suite| -> | Eval Orchestrator | -> | Metric/Judge   | -> | Regression Gate|
+----------------+    +-------------------+    +----------------+    +----------------+
                                                                             |
                                                                             v
                                                                      +--------------+
                                                                      | Refresh Loop |
                                                                      +--------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 변경 감지    | -> | 평가 실행    | -> | 결과 비교    | -> | 게이트 판정  | -> | 기준 갱신    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **변경 감지**: 모델과 프롬프트와 데이터 설정 변경을 감지함
2. **평가 실행**: 정해진 benchmark와 운영 샘플로 평가를 수행함
3. **결과 비교**: 이전 기준과 현재 결과를 비교해 회귀를 찾음
4. **게이트 판정**: 허용 범위를 벗어나면 배포를 막거나 경보를 발행함
5. **기준 갱신**: 운영 학습을 반영해 평가 세트와 임계치를 주기적으로 갱신함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 평가 세트가 오래되면 지속 평가를 돌려도 실제 운영 변화와 품질 저하를 제대로 반영하지 못할 수 있음
   - 해결방안: benchmark refresh policy와 production sample injection을 적용하고 benchmark recency score와 offline online gap으로 검증함
2. 문제: 지표가 많아도 게이트 기준이 불명확하면 경보만 쌓이고 실제 배포 통제는 약해질 수 있음
   - 해결방안: tiered regression threshold와 release gate policy를 적용하고 gate decision clarity score와 blocked regression escape rate로 검증함
3. 문제: 평가 결과가 개선 루프와 연결되지 않으면 같은 유형의 회귀가 반복될 수 있음
   - 해결방안: failure taxonomy와 remediation workflow를 적용하고 repeated regression rate와 issue closure lead time으로 검증함

## Ⅶ. 적용 사례

- 프롬프트 기반 챗봇이 변경마다 지속 평가를 실행하며 확인 지표는 benchmark recency score와 blocked regression escape rate임
- 추천 파이프라인이 운영 샘플을 평가 세트에 주기 반영하며 확인 지표는 offline online gap과 repeated regression rate임
- 금융 AI 조직이 회귀 유형 분류와 조치 루프를 운영하며 확인 지표는 gate decision clarity score와 issue closure lead time임

## Ⅷ. 결론

Continuous Evaluation은 평가를 이벤트가 아니라 운영 루프로 바꾸는 체계이므로 최신 benchmark와 명확한 게이트와 개선 연계를 함께 설계해야 함.
