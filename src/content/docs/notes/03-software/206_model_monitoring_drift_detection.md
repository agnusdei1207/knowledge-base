---
sidebar:
  order: 206
  label: "206. 모델 모니터링•드리프트 감지 (Model Monitoring Drift Detection)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "모델 모니터링•드리프트 감지 (Model Monitoring Drift Detection)"
date: "2026-08-14T05:55:00+09:00"
tags: ["notes-software"]
weight: 206
extra:
  question_no: "206"
  source_status: "기출"
  source_history: ""
  priority: 70
  priority_note: "운영 모델의 드리프트 감지•대응"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Model Monitoring (모델 모니터링)**: 운영 입력•예측•정답을 기준선과 비교해 품질 변화를 감시하는 활동
- **Drift (드리프트)**: 입력 분포나 입력•정답 관계가 학습 시점과 달라지는 현상

</details>

- 정의/개념: 운영 신호로 Drift와 Model 품질 저하를 판정하는 **감시 체계**
- 배경/필요성: 배포 전 정적 평가만으로는 **운영 분포•개념 변화** 탐지 불가

#### 한줄 요약

- 입력•예측•정답을 기준선과 비교해 **Model 노후화** 식별

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Baseline (기준선)**: 운영 변화 판정에 사용하는 학습•검증 시점의 분포와 성능
- **Delayed Label (지연 정답)**: 예측 이후 일정 시간이 지나 확정되는 실제 결과값

</details>

- **통계 거리**: KL Divergence•KS Test로 분포 변화 측정
- **Slice 감시**: 사용자군•지역•시간별 국소 품질 저하 탐지
- **지연 정답 결합**: 과거 예측과 실제 결과로 성능 저하 확정
- **업무 영향 판정**: 변화 크기보다 손실•위험 기반 대응

#### 한줄 요약

- 분포 변화는 조기 경보, 지연 정답은 **실성능 저하** 확정

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Drift Detector (드리프트 탐지기)**: 기준선과 운영 분포의 거리•성능 차이를 판정하는 엔진

</details>

```text
[Model Monitoring]
 ├── [Baseline Store | 학습•검증 분포]
 ├── [Signal Collector | 입력•예측•정답]
 ├── [Label Joiner | 지연 정답 결합]
 ├── [Drift Detector | 거리•임계치 판정]
 └── [Response Controller | 재학습•복귀•갱신]
```

| 구성요소 | 책임 |
|---|---|
| Baseline Store | 검증된 입력•예측•성능 **기준 분포** 보관 |
| Signal Collector | 운영 신호를 **Slice 단위**로 수집 |
| Label Joiner | 지연 정답과 과거 **예측 Log** 결합 |
| Drift Detector | 통계 거리와 **성능 임계치** 판정 |
| Response Controller | 재학습•Rollback•**Baseline 갱신** 실행 |

#### 한줄 요약

- 기준선과 운영 신호를 비교하고 정답으로 **대응 근거** 확정

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Proxy Metric (대리지표)**: 실제 정답 확정 전 품질 변화를 추정하는 간접 지표

</details>

```text
[운영 입력•예측•정답]
          │
          ▼
[1. 입력•예측 변화 전달]
          │
          ▼
[2. 기준선•통계 거리 비교]
          │
          ▼
[3. 정답•예측 결합]
          │
          ▼
[4. 변화 유형•업무 영향 판정]
          │
          ▼
┌──────[5. 대응 결정]──────┐
│ 성능 저하: 재학습•복귀  │
│ 무영향 변화: 기준선 갱신│
│ 정답 부족: 판정 보류    │
└──────────────────────────┘
```

### 동작 원리

1. **입력•예측 변화 전달**: Slice별 운영 분포 수집
2. **기준선•통계 거리 비교**: 변화 크기와 지속 시간 판정
3. **정답•예측 결합**: 지연 정답으로 실제 성능 산출
4. **변화 유형•업무 영향 판정**: Data•Concept•예측 변화 구분
5. **대응 결정**: 재학습•Rollback•Baseline 갱신 선택

#### 한줄 요약

- 분포 경보를 정답•업무 영향과 결합해 **재학습 여부** 결정

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Concept Drift (개념 드리프트)**: 입력과 정답 사이의 관계가 달라지는 현상

</details>

| 비교 항목 | Data Drift | Concept Drift | Prediction Drift |
|---|---|---|---|
| 변화 대상 | 입력 **Feature 분포** | 입력•정답 **관계** | 예측값 **분포** |
| 판정 시점 | 정답 확보 전 | 지연 정답 확보 후 | 예측 직후 |
| 주요 한계 | 무영향 변화도 경보 | 판정 지연 | 원인 구분 곤란 |

#### 한줄 요약

- 입력•정답 관계•출력 중 **변화 대상**을 구분해 대응

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Slice Analysis (슬라이스 분석)**: 세부 사용자군별 성능을 분리해 분석하는 기법

</details>

| 고려사항 | 대책 |
|---|---|
| 계절성의 Drift 오판 | 요일•계절별 **Baseline** 분리 |
| 지연 정답으로 탐지 지체 | Proxy Metric과 **Delayed Label** 병행 |
| 다수 지표 경보 폭주 | 업무 영향•지속 시간으로 **우선순위** 부여 |
| 전체 평균의 국소 저하 은폐 | 사용자군별 **Slice Analysis** 적용 |

#### 한줄 요약

- 계절•Slice•업무 영향을 반영해 **False Alarm** 억제

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- 입력 분포가 달라졌다는 이유만으로 재학습하지 않고 실제 정답과 업무 손실을 확인한다.

</details>

- 실제 성능 저하는 **재학습**•**Rollback**, 무영향 변화는 Baseline 갱신
