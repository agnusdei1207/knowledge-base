---
title: "모델 드리프트 (Model Drift)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 222
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 드리프트를 운영 중 성능 저하의 포괄 개념으로 이해하게 만든다.

## 한눈에
- **개요**: 배포 후 시간이 지나며 모델의 예측 품질이 학습·검증 시점보다 낮아지는 현상
- **왜 필요한가**: 데이터 분포 변화, 개념 변화, 시스템 변경, feature pipeline 오류가 모두 모델 품질 하락으로 나타날 수 있다.
- **핵심 직관**: 새로 맞춘 안경이 시간이 지나 시력 변화와 렌즈 손상으로 맞지 않게 되는 상황과 같다.

## 깊이 이해
- **배경·문제의식**: ML 모델은 고정된 코드처럼 동작하지만 입력 데이터와 업무 환경은 계속 변하므로 운영 성능이 검증 성능과 달라진다.
- **작동 원리**: model drift는 data drift, concept drift, feature drift, serving skew, label shift가 성능 지표 하락으로 나타난 결과를 포괄한다.
- **비유**: 매장 매출 예측 모델이 코로나 이후 온라인 주문 증가와 가격 정책 변경을 반영하지 못해 예측 오차가 커지는 사례다.
- **구체 예시**: 검증 AUC 0.86 모델이 운영 3개월 후 AUC 0.78로 하락하고 특정 연령 segment에서 recall이 15%p 감소하면 model drift 대응이 필요하다.
- **흔한 오해·주의점**: 모델 드리프트는 하나의 원인이 아니며, 원인별로 재학습, feature 수정, threshold 조정, 롤백을 다르게 선택해야 한다.

## 연결 개념
- Data Drift — 입력 분포 변화 원인
- Concept Drift — 입력과 label 관계 변화 원인
- Model Monitoring — 모델 드리프트 감지와 조치 실행 체계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 모델 드리프트는 성능 저하 결과이므로 원인 분해와 조치 선택이 답안의 중심이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Model Drift는 운영 모델의 예측 품질이 시간에 따라 기준 성능에서 벗어나는 현상임.
> 2. **가치**: AUC·F1·MAE·calibration·business KPI 변화를 감지해 재학습, 롤백, threshold 조정을 결정함.
> 3. **판단 포인트**: data drift, concept drift, feature drift, serving skew를 분리해야 조치가 정확해짐.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ML 운영 성능 저하 이해 확인 | 성능 지표 하락과 원인 유형 분해 | data drift 하나로만 설명 |
| MLOps 조치 판단 확인 | 재학습, rollback, threshold tuning, pipeline repair | 성능 저하 후 대응 절차 누락 |
| 품질 지표 설계 확인 | offline metric, online KPI, segment metric | 전체 평균 성능만 제시 |

> 요약: 이 문제는 모델 품질 하락을 원인별로 분해하고 운영 조치와 지표를 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 운영 모델 성능 저하
- 배경: 데이터, label 관계, feature pipeline, serving 환경이 바뀌면 검증 성능과 운영 성능이 달라짐.
- 필요성: AUC 5%p 하락, MAE 10% 증가, KPI 10% 하락 기준으로 원인 분석과 조치를 실행해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Production Model -> Prediction Log -> Label / KPI -> Performance Monitor
Drift Analyzer -> Root Cause -> Retrain / Rollback / Threshold Change
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Performance Baseline | 배포 승인 시점 성능 기준 저장 | validation, holdout, segment 기준 |
| Online Evaluator | 운영 성능과 KPI 계산 | delayed label 처리 |
| Drift Analyzer | 성능 저하 원인 분류 | data, concept, feature, serving skew |
| Remediation Workflow | 재학습·롤백·임계값 조정 실행 | 승인 이력 기록 |

> 요약: 모델 드리프트 대응은 성능 하락 탐지와 원인 분류, 조치 실행을 하나의 운영 흐름으로 묶는다.

---

## Ⅲ. 동작원리 및 흐름도

```text
기준 성능 저장 -> 운영 성능 측정 -> 성능 차이 계산 -> 원인 분류 -> 조치 선택 -> 배포 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 배포 시 baseline metric 저장 | AUC, F1, MAE, KPI |
| 2 | 운영 label과 예측 로그 결합 | label match 95% 이상 |
| 3 | 성능 하락과 drift 지표 동시 분석 | AUC 5%p 하락, PSI 0.2 초과 |
| 4 | 재학습·롤백·threshold 조정 선택 | canary KPI 기준 통과 |

> 요약: 모델 드리프트는 성능 하락 자체보다 원인별 조치를 선택하는 절차가 핵심이다.

---

## Ⅳ. 특징

| 구분 | 데이터 드리프트 | 개념 드리프트 | 모델 드리프트 |
|:---|:---|:---|:---|
| 초점 | 입력 분포 변화 | 입력과 label 관계 변화 | 운영 성능 하락 |
| 대표 지표 | PSI, KS-test | AUC, recall, calibration | AUC, MAE, KPI |
| 대응 기준 | 분포 변화 임계값 | label 기반 성능 저하 | 원인 분류 후 조치 |

> 요약: 모델 드리프트는 여러 drift 원인이 모델 성능 하락으로 나타난 운영 결과를 의미한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 감지 범위 | 서버 장애 중심 | 품질·분포·KPI 통합 | ML 의사결정 영향도 |
| 조치 방식 | 주기 배포 | 조건 기반 재학습·롤백 | drift 빈도와 label 지연 |
| 평가 방식 | 전체 metric | segment별 metric + business KPI | 불균형 데이터와 규제 업무 |

> 요약: 모델 드리프트는 전체 평균보다 segment별 성능과 업무 KPI를 같이 보아야 조치 우선순위가 보인다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 원인 오판 | drift 지표와 성능 지표 분리 운영 | unified dashboard와 root cause tree 구성 | 분석 소요 4시간 이하 |
| 롤백 실패 | 이전 모델과 feature schema 불일치 | registry에 schema와 dependency 저장 | rollback success 99% |
| 재학습 품질 저하 | 오염 label 사용 | label validation과 holdout 검증 | holdout AUC 기준 통과 |

> 요약: 모델 드리프트 대응의 리스크는 원인 오판, 롤백 불가, 오염 데이터 재학습에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 품질 유지 | AUC 5%p 이내 하락 | delayed label evaluation |
| 예측 보정 | ECE 0.05 이하 | calibration curve |
| 운영 영향 | KPI 10% 이내 변동 | online experiment report |

> 요약: 모델 드리프트 통제는 품질, 보정, 업무 영향을 함께 유지하는지로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 기준 성능 관리: model registry에 validation AUC, segment metric, feature schema, training data hash를 함께 저장함.
2. 원인 분류 자동화: AUC 하락, PSI 초과, feature missing, serving skew를 규칙 기반 root cause tree로 분류함.
3. 조치 실행: 원인이 data drift면 재학습, serving skew면 pipeline 수정, KPI 급락이면 이전 모델 롤백을 runbook으로 고정함.

**결론 (2줄):**
- 기술사 판단: Model Drift는 단순 재학습 문제가 아니라 성능 하락 원인을 분해한 뒤 조치를 선택해야 하는 운영 품질 문제임.
- 향후 방향: model drift 대응은 automated retraining, feature store, AI Governance 승인 흐름과 결합됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "모델 드리프트를 설명하시오" | 성능 측정과 원인 분류 흐름 | data·concept drift와 차이 |
| 요구사항 명시형 | "모델 성능 저하 대응 방안을 제시하시오" | root cause와 조치 선택 | 롤백·재학습·지표 점검 |

> 요약: 설명형은 포괄 개념을, 방안형은 원인 분해와 운영 조치를 중심으로 작성한다.
