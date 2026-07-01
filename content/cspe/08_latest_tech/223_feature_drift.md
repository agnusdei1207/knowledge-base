---
title: "피처 드리프트 (Feature Drift)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 223
---

# 📖 【암기용】 개념 완전 이해

> 목적: 피처 드리프트를 개별 입력 변수 단위의 변화로 이해하게 만든다.

## 한눈에
- **개요**: 모델 입력 feature의 값 범위, 분포, 의미, 생성 방식이 학습 시점과 달라지는 현상
- **왜 필요한가**: 전체 데이터 변화가 작아도 핵심 feature 하나가 바뀌면 모델 의사결정이 크게 흔들릴 수 있다.
- **핵심 직관**: 요리 맛을 좌우하는 소금 계량 단위가 g에서 mg로 바뀌었는데 레시피가 이를 모르는 상황과 같다.

## 깊이 이해
- **배경·문제의식**: feature는 데이터 소스, 전처리 로직, 집계 window, 단위, 범주 매핑에 의존하므로 파이프라인 변경에 민감하다.
- **작동 원리**: feature별 분포, 결측률, cardinality, min/max, importance 변화를 model_version별 baseline과 비교한다.
- **비유**: 건강검진에서 체중계 단위가 kg에서 lb로 바뀌면 사람은 그대로여도 BMI 계산 결과가 달라지는 상황이다.
- **구체 예시**: 클릭 횟수 feature의 7일 집계가 30일 집계로 바뀌면 평균값이 4배 증가하고 tree 모델의 split 경로가 달라질 수 있다.
- **흔한 오해·주의점**: feature drift는 data drift의 일부로 볼 수 있지만, feature 생성 로직과 의미 변화까지 포함한다는 점이 다르다.

## 연결 개념
- Feature Store — feature 생성·버전·재사용 관리
- Data Drift — 데이터 분포 변화의 상위 개념
- Training Serving Skew — 학습과 serving feature 계산 차이

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 피처 드리프트는 feature 값뿐 아니라 생성 로직, schema, 의미 변화까지 확인해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Feature Drift는 모델 입력 feature의 분포·범위·생성 방식이 학습 기준에서 벗어나는 현상임.
> 2. **가치**: 중요 feature의 PSI 0.2 초과, 결측률 5%p 증가, cardinality 급증을 감지해 품질 하락을 예방함.
> 3. **판단 포인트**: feature importance가 큰 변수의 drift는 낮은 순위 변수보다 재평가 우선순위가 높음.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| feature 중심 ML 운영 이해 확인 | 분포, schema, 결측률, 생성 로직 변화 | data drift와 완전히 동일하게 서술 |
| Feature Store 역할 확인 | version, lineage, training-serving consistency | feature lineage 누락 |
| 실무 대응 판단 확인 | 중요도 기반 우선순위와 재계산 검증 | 모든 feature에 같은 기준 적용 |

> 요약: 이 문제는 feature 단위의 drift 감지와 feature pipeline 통제를 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 입력 feature 변화
- 배경: 데이터 소스, 단위, 집계 window, 전처리 로직이 바뀌면 모델 입력 의미가 달라짐.
- 필요성: 중요 feature PSI 0.2 초과 또는 결측률 5%p 증가 시 모델 성능 영향 평가가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Raw Data -> Feature Pipeline -> Feature Store -> Online Serving
Baseline Feature Profile -> Current Feature Profile -> Drift / Skew Alert
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Feature Pipeline | 원천 데이터를 모델 입력으로 변환 | 집계 window, 단위, 인코딩 |
| Feature Store | feature 값·버전·lineage 관리 | offline/online consistency |
| Feature Profile | feature별 통계 기준 저장 | min, max, null rate, PSI |
| Skew Detector | 학습·serving 계산 차이 감지 | training-serving skew 확인 |

> 요약: 피처 드리프트는 feature 생성 경로와 운영 값 분포를 함께 기록해야 원인 추적이 가능하다.

---

## Ⅲ. 동작원리 및 흐름도

```text
feature 기준선 생성 -> 운영 feature 수집 -> 통계 비교 -> 중요도 반영 -> 영향 평가 -> pipeline 수정 / 재학습
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 학습 시점 feature profile 저장 | feature coverage 100% |
| 2 | 운영 feature 통계와 schema 수집 | null rate, cardinality, min/max |
| 3 | PSI·결측률·범위 초과 판단 | PSI 0.2 초과, 결측률 5%p 증가 |
| 4 | feature importance와 성능 영향 분석 | top 20 feature 우선 검토 |

> 요약: 피처 드리프트는 feature별 변화량과 모델 기여도를 결합해 조치 우선순위를 정한다.

---

## Ⅳ. 특징

| 구분 | Data Drift | Feature Drift | 수치 기준 |
|:---|:---|:---|:---|
| 범위 | 데이터셋 전체 분포 | 개별 feature 분포·의미 | feature별 PSI |
| 원인 | 고객군·환경 변화 | 단위·집계·전처리 변경 | 결측률 5%p 증가 |
| 대응 | 재학습 검토 | pipeline 수정, feature version 복구 | schema mismatch 0건 |

> 요약: Feature Drift는 개별 feature의 생성 로직과 분포 변화를 추적해 모델 입력의 의미를 보존한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 관리 단위 | dataset profile | feature profile + lineage | feature 재사용 모델 수 |
| 우선순위 | 전체 drift 평균 | feature importance 반영 | 상위 20개 feature 영향도 |
| 대응 범위 | 모델 재학습 | pipeline repair + 재학습 | 생성 로직 변경 여부 |

> 요약: 중요도가 큰 feature의 drift는 전체 dataset drift보다 모델 성능에 큰 영향을 줄 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 단위 오류 | 원천 시스템 단위 변경 | schema contract와 unit test 적용 | unit mismatch 0건 |
| serving skew | offline과 online 계산 로직 불일치 | Feature Store 공통 transform 사용 | offline-online diff 1% 이하 |
| 중요 feature 누락 | upstream column 제거 | data contract와 배포 전 검증 | null rate threshold 위반 0건 |

> 요약: feature drift 리스크는 단위, 계산 로직, upstream 계약을 통제해야 차단 가능하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 분포 변화 | top feature PSI 0.2 이하 | feature profile 비교 |
| 품질 변화 | 중요 feature 결측률 5% 이하 | Great Expectations, TFDV |
| 일관성 | offline-online diff 1% 이하 | batch/online 샘플 대조 |

> 요약: 점검 지표는 분포, 결측, 학습-serving 일관성을 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. feature 계약: feature name, type, unit, allowed range, aggregation window를 schema contract로 관리함.
2. profile 감시: top 20 importance feature에 PSI 0.2, null rate 5%, cardinality 2배 증가 기준을 적용함.
3. 일관성 검증: offline training feature와 online serving feature를 동일 transform 코드로 생성하고 샘플 diff를 1% 이하로 유지함.

**결론 (2줄):**
- 기술사 판단: Feature Drift는 모델보다 feature pipeline 문제인 경우가 많으므로 lineage와 serving skew를 먼저 확인해야 함.
- 향후 방향: Feature Store와 data contract 기반 feature governance가 MLOps 품질 관리의 중심으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "피처 드리프트를 설명하시오" | feature profile 비교 흐름 | Data Drift와 차이 |
| 요구사항 명시형 | "feature 품질 관리 방안을 제시하시오" | schema contract와 skew detection | Feature Store 기반 대응 |

> 요약: 설명형은 feature 변화 원리를, 방안형은 feature 계약과 pipeline 검증을 중심으로 작성한다.
