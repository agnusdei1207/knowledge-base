---
title: "Feature Drift 피처 드리프트 (Feature Drift)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 223
extra:
  question_no: "223"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Feature Drift는 전체 입력이 아니라 개별 피처 수준에서 분포나 의미가 변하는 현상임
- Data Drift보다 더 세밀한 분석 단위라 원인 파악과 대응 우선순위 설정에 유용함
- 피처 중요도와 upstream 변경 이력을 함께 봐야 실질적 의미를 해석할 수 있음

## Ⅰ. 개요

- **정의/개념**: Feature Drift는 모델 입력을 구성하는 개별 피처의 분포와 결측률과 범주 구성이 학습 시점 대비 달라져 모델 예측 안정성과 정확도에 영향을 미치는 현상임
- **배경/필요성**: 동일한 데이터셋 안에서도 일부 핵심 변수만 급격히 변하는 경우가 많아 전체 평균 기반 모니터링보다 피처 단위 분석이 실무 대응에 더 효과적임

## Ⅱ. 특징

- 전체 분포는 안정적이어도 핵심 피처 하나의 변화만으로 성능이 크게 흔들릴 수 있음
- 결측과 스키마 변경과 단위 변경도 사실상 피처 드리프트에 포함해 봐야 함
- 중요도 낮은 피처까지 모두 동일 경보로 처리하면 운영 노이즈가 커짐
- Feature Store와 Data Quality Monitoring과 긴밀히 연결됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Feature Drift | Data Drift | Schema Drift |
|:---|:---|:---|:---|
| 분석 단위 | 개별 피처 | 전체 입력 집합 | 컬럼 구조와 타입 |
| 주요 징후 | 평균, 분산, null rate 변화 | 종합 분포 변화 | 필드 추가, 삭제, 타입 변경 |
| 대응 우선순위 | 중요 피처 중심 | 서비스 전체 위험 평가 | 파이프라인 수정 |
| 대표 도구 | PSI, KS, feature importance | drift dashboard | contract test |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Feature Baseline | 학습 시점 각 피처의 분포와 결측과 범주 비율을 저장해 비교 기준으로 사용하는 참조 세트임 |
| Current Feature Collector | 운영 데이터에서 최근 피처 값과 상태를 수집해 현재 분포를 구성하는 관측 계층임 |
| Drift Calculator | PSI와 KS와 빈도 비교를 이용해 피처별 변화량을 계산하는 분석 엔진임 |
| Importance Mapper | 모델 중요도와 비즈니스 영향도를 결합해 어떤 피처 경보를 우선 대응할지 정하는 계층임 |
| Alert and Investigation Flow | 임계치를 넘는 피처에 대해 원천 시스템과 변환 로직과 모델 영향 범위를 조사하는 절차임 |

```text
+----------------+    +------------------+    +------------------+    +----------------+
| Feature Baseline| -> | Current Collector| -> | Drift Calculator | -> | Alert/Investig.|
+----------------+    +------------------+    +------------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 기준 피처 저장 | -> | 현재 피처 수집 | -> | 변화량 계산  | -> | 중요도 반영  | -> | 조사 및 수정 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **기준 피처 저장**: 학습 데이터 기준 피처 통계를 저장함
2. **현재 피처 수집**: 운영 입력의 최근 피처 값을 수집함
3. **변화량 계산**: 피처별 분포와 null rate와 범주 비율 변화를 계산함
4. **중요도 반영**: 모델 영향도가 큰 피처를 우선순위로 올림
5. **조사 및 수정**: 원천 데이터와 변환 로직과 모델 영향 범위를 점검함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 중요도가 낮은 피처까지 동일 수준 경보를 발생시키면 운영자가 핵심 변화 신호를 놓칠 수 있음
   - 해결방안: feature importance weighted alerting을 적용하고 alert precision과 low impact alert ratio로 검증함
2. 문제: upstream 시스템의 단위 변경이나 결측 증가가 늦게 발견되면 핵심 피처가 조용히 오염될 수 있음
   - 해결방안: data contract와 null rate monitoring을 적용하고 schema incident detection time과 missing feature rate로 검증함
3. 문제: 피처 변화가 모델 성능에 미치는 영향 연결이 없으면 불필요한 조사와 재학습이 반복될 수 있음
   - 해결방안: drift to performance linkage analysis를 적용하고 investigation efficiency score와 unnecessary retraining rate로 검증함

## Ⅶ. 적용 사례

- 대출 심사 모델이 중요도 기반 피처 경보를 운영하며 확인 지표는 alert precision과 low impact alert ratio임
- 추천 서비스가 upstream 계약 테스트와 결측 모니터링을 적용하며 확인 지표는 schema incident detection time과 missing feature rate임
- 제조 예측 시스템이 피처 드리프트와 성능 연관 분석을 수행하며 확인 지표는 investigation efficiency score와 unnecessary retraining rate임

## Ⅷ. 결론

Feature Drift는 전체 입력 변화보다 실전 대응에 가까운 분석 단위이므로 중요 피처 중심 경보와 원인 연결 분석이 함께 필요함.
