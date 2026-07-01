---
title: "개념 드리프트 (Concept Drift)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 221
---

# 📖 【암기용】 개념 완전 이해

> 목적: 개념 드리프트를 데이터 드리프트와 구분해 이해하게 만든다.

## 한눈에
- **개요**: 입력 데이터와 정답 label 사이의 관계가 시간이 지나며 바뀌는 현상
- **왜 필요한가**: 입력 분포가 비슷해 보여도 고객 행동, 사기 패턴, 시장 규칙이 바뀌면 같은 입력에 대한 정답이 달라질 수 있다.
- **핵심 직관**: 같은 증상이라도 시대가 바뀌어 다른 진단을 내려야 하는 의료 지식 변화와 같다.

## 깊이 이해
- **배경·문제의식**: 사기 탐지, 이탈 예측, 추천, 신용평가는 사용자와 공격자의 행동이 바뀌면 feature와 label의 관계가 변한다.
- **작동 원리**: 운영 데이터의 예측 오차, label 기반 성능, residual 분포, segment별 calibration을 시간 순서로 추적해 관계 변화 여부를 판단한다.
- **비유**: 과거에는 밤 11시 결제가 사기 신호였지만, 새 배송 서비스 확산 후 정상 결제로 바뀌는 상황이다.
- **구체 예시**: 사기 탐지 모델의 입력 분포 PSI가 0.08로 낮아도 fraud recall이 92%에서 78%로 하락하면 concept drift를 의심한다.
- **흔한 오해·주의점**: concept drift는 입력 분포 변화만 보는 문제가 아니며, label 확보 없이는 확정 판단이 어렵다.

## 연결 개념
- Data Drift — 입력 분포 변화
- Model Drift — 모델 성능 하락의 포괄 현상
- Online Learning — 변화하는 관계를 점진적으로 반영하는 학습 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 개념 드리프트는 입력 분포가 아니라 입력과 정답의 관계 변화이므로 label 기반 검증이 답안의 중심이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Concept Drift는 P(y|X)가 시간에 따라 변해 기존 모델의 의사결정 경계가 맞지 않게 되는 현상임.
> 2. **가치**: AUC, recall, calibration error, residual 분포로 관계 변화와 모델 품질 하락을 조기 포착함.
> 3. **판단 포인트**: label 지연이 있는 환경에서는 proxy KPI와 delayed label 평가를 결합해 재학습 시점을 결정해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| drift 유형 구분 확인 | P(X) 변화와 P(y|X) 변화의 차이 | data drift와 같은 개념으로 서술 |
| 모델 성능 저하 원인 분석 확인 | label 기반 평가, residual, calibration | 입력 feature 분포만 비교 |
| 운영 대응 설계 확인 | 재학습, online learning, champion/challenger | label 지연 조건 누락 |

> 요약: 이 문제는 관계 변화의 본질과 label 기반 검증 절차를 구분해 쓰는 것이 채점 포인트다.

---

## Ⅰ. 개요 및 필요성

- 개요: 입력과 정답 관계 변화
- 배경: 고객 행동, 공격 패턴, 제도 변경은 같은 입력 feature에 대한 label 발생 확률을 바꿈.
- 필요성: recall 10%p 하락 또는 calibration error 0.05 초과 시 기존 의사결정 경계의 재검증이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Feature X -> Existing Model -> Prediction
Delayed Label y -> Performance / Residual Monitor -> Drift Decision -> Retraining
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Label Collector | 실제 정답 데이터 수집 | label delay 관리 |
| Performance Monitor | AUC, recall, precision 변화 측정 | segment별 계산 필요 |
| Residual Analyzer | 예측 오차 분포 변화 분석 | regression, classification 모두 적용 |
| Adaptation Pipeline | 재학습 또는 online update 실행 | 승인 게이트 필요 |

> 요약: 개념 드리프트 관리는 label을 확보해 예측 오차와 성능 지표가 시간에 따라 변하는지 확인한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
예측 로그 수집 -> label 결합 -> 성능 계산 -> 관계 변화 판단 -> 모델 갱신 / 관찰 지속
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 예측값과 실제 label을 request_id로 결합 | match rate 95% 이상 |
| 2 | 시간 window별 AUC·recall·calibration 계산 | AUC 5%p 하락 |
| 3 | segment별 오류 증가 원인 분석 | 특정 segment recall 10%p 하락 |
| 4 | 재학습·online update·rule 보정 선택 | holdout 성능 기준 통과 |

> 요약: 개념 드리프트는 label 결합 후 성능과 오류 구조를 분석해야 감지할 수 있다.

---

## Ⅳ. 특징

| 구분 | 데이터 드리프트 | 개념 드리프트 | 수치 기준 |
|:---|:---|:---|:---|
| 변화 대상 | P(X) 입력 분포 | P(y|X) 입력과 label 관계 | PSI vs AUC·recall |
| label 필요성 | 선택적 | 필수에 가까움 | label coverage 95% |
| 대응 | 분포 보정, 재학습 검토 | 의사결정 경계 재학습 | recall 10%p 하락 |

> 요약: 개념 드리프트는 입력이 비슷해도 정답 관계가 바뀌는 문제라 label 기반 평가가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 감지 데이터 | 입력 feature 로그 | prediction + delayed label | label 확보 가능 업무 |
| 탐지 지표 | PSI, KS-test | AUC, recall, Brier score | 분류·회귀 모델 유형 |
| 적응 방식 | 수동 재학습 | champion/challenger, online learning | drift 속도와 규제 승인 요구 |

> 요약: 개념 드리프트가 빠른 업무는 주기 재학습보다 challenger 모델과 점진 학습 검증을 병행한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 감지 지연 | label 수집 지연 | proxy KPI와 delayed label 평가 병행 | label delay 7일 이하 |
| 과잉 적응 | 일시 이벤트를 drift로 오판 | 최소 window와 holdout 검증 적용 | post-deploy AUC 유지 |
| 규제 리스크 | 자동 갱신 모델의 설명 부족 | 모델 카드와 승인 이력 기록 | approval log 100% |

> 요약: 개념 드리프트 대응은 label 지연, 일시 이벤트, 승인 근거를 동시에 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 관계 변화 | AUC 5%p 이내 하락 | delayed label evaluation |
| calibration | ECE 0.05 이하 | reliability diagram |
| segment 품질 | segment recall 10%p 이내 차이 | cohort analysis |

> 요약: 도입 효과는 전체 성능보다 calibration과 segment별 오류 변화까지 확인해야 판단 가능하다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. label 파이프라인: prediction_id와 label_id를 결합하고 label delay, match rate, coverage를 매일 측정함.
2. drift 판정: AUC 5%p 하락, recall 10%p 하락, ECE 0.05 초과 중 2개 이상 충족 시 challenger 재학습을 실행함.
3. 배포 통제: 재학습 모델은 holdout dataset, segment fairness, canary 5% 배포 결과를 통과한 뒤 champion 교체를 승인함.

**결론 (2줄):**
- 기술사 판단: Concept Drift는 입력 변화보다 label 관계 변화를 확인해야 하므로 성능 지표와 업무 label 품질이 핵심 판단 근거임.
- 향후 방향: 실시간 업무에서는 concept drift 감지, online learning, human approval이 결합된 적응형 MLOps가 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "개념 드리프트를 설명하시오" | label 결합과 성능 평가 흐름 | data drift와 차이 |
| 요구사항 명시형 | "개념 드리프트 대응 방안을 제시하시오" | 재학습·online learning 판단 절차 | label 지연 리스크와 승인 기준 |

> 요약: 설명형은 관계 변화 원리를, 방안형은 label 기반 판정과 배포 통제를 중심으로 작성한다.
