---
sidebar:
  order: 204
  label: "204. 피처 스토어 (Feature Store)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "피처 스토어 (Feature Store)"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-software"]
weight: 204
extra:
  question_no: "204"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "특징 일관성과 재사용 구조가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Feature Store (피처 스토어)**: ML 모델에 필요한 피처(Feature)의 정의·계산 로직·과거 이력값·실시간 최신값을 단일 플랫폼에서 관리하고 제공하여, 여러 팀과 모델이 동일한 피처를 일관성 있게 재사용할 수 있게 하는 MLOps 핵심 인프라.
- **Feature (피처)**: 원천 데이터(로그, DB 레코드 등)를 ML 모델이 학습·추론에 사용할 수 있는 수치·범주형 값으로 선택하거나 변환한 개별 특성. 예: 고객의 지난 30일 평균 구매금액.
- **Training-Serving Skew (학습-서빙 편향)**: 학습 시 사용한 피처 계산 방식과 온라인 추론 시 사용하는 피처 계산 방식이 달라, 오프라인 평가 정확도와 실제 운영 정확도가 괴리되는 현상.

</details>

- 정의/개념: 피처의 정의·계산 로직·시점별 이력·실시간 최신값을 일원화하여, 학습과 온라인 추론에서 동일한 피처 기반을 보장하고 팀 간 재사용을 지원하는 **Feature Store 중앙화 플랫폼**
- 배경/필요성: 각 팀이 독자적인 피처 파이프라인을 만들면 코드 중복·계산 불일치·학습-서빙 편향이 발생하고, 어떤 모델이 어떤 피처를 쓰는지 추적이 불가능해지는 거버넌스 공백 방지 요구성

#### 한줄 요약

- 같은 재료 가공법을 등록해 과거 훈련 값과 지금 예측 값을 한곳에서 일관되게 제공한다.

## Ⅱ. 특징 (Feature Store의 3대 핵심 특성)

<details><summary>핵심 용어</summary>

- **PIT Join (Point-In-Time Correct Join, 시점 일치 조인)**: 훈련 데이터를 생성할 때, 각 학습 예제의 예측 시점(Event Timestamp) 이전에 관측 가능했던 피처값만 결합하여, 미래 데이터가 학습에 섞이는 '데이터 누수(Data Leakage)'를 방지하는 조인 방식.

</details>

- **Feature Lineage (피처 계보)**: 피처가 어떤 원천 데이터에서 어떤 변환 로직으로 생성되었는지, 어떤 모델이 이 피처를 사용하는지를 DAG(방향 비순환 그래프)로 추적하는 이력.
- **Offline/Online Dual Store**: 대용량 배치 학습을 위한 Offline Store(Parquet/Iceberg 기반 시점별 이력)와 실시간 추론을 위한 Online Store(Redis/DynamoDB 기반 저지연 최신값)를 분리하여 각 용도에 최적화.
- **Shared Feature Registry (공유 피처 레지스트리)**: 조직 전체에서 사용 가능한 피처의 정의·스키마·소유자·버전·SLA를 중앙 카탈로그로 관리하여 중복 개발 없이 재사용.

#### 한줄 요약

- 학습 때 쓴 가공법과 운영 때 쓴 가공법이 같아야 모델이 예상한 입력을 받는다.

## Ⅲ. 구조 및 구성요소 (Feature Store 4-Component 아키텍처)

<details><summary>핵심 용어</summary>

- **Feature Transformer (피처 변환기)**: 원천 데이터(Kafka 이벤트·DB·배치 파일)를 Feature Registry에 등록된 계산 로직에 따라 가공하여 Offline Store의 이력과 Online Store의 최신값 양쪽에 동시 저장하는 변환 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      Feature Store Architecture                        │
├────────────────────────────────────────────────────────────────────────┤
│ [원천 데이터] ─(정의된 계산 로직)──► [Feature Transformer]             │
│                                            │              │            │
│                                    (배치 이력)      (실시간 최신값)     │
│                                            ▼              ▼            │
│                               [Offline Store]    [Online Store]        │
│                               (Parquet/Iceberg)   (Redis/DynamoDB)     │
│                                            │              │            │
│                             (PIT Join 학습 데이터)  (추론 입력 저지연) │
│                                            ▼              ▼            │
│                               [ML 학습 파이프라인]  [온라인 추론 API]  │
│                                                                        │
│ [Feature Registry] ── 피처 정의·버전·소유자·계보·SLA 중앙 관리         │
│ [Feature Monitor] ─── 품질·분포·신선도·학습-서빙 스큐 실시간 감시      │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Feature Registry에 등록된 단일 계산 로직을 기반으로, Feature Transformer가 배치(Offline)와 실시간(Online) 두 경로에 동시 공급하여 학습-서빙 편향을 원천 차단하는 구조.

| 구성요소 | 핵심 역할 및 기능 | 대표 도구 |
|:---|:---|:---|
| **Feature Registry** | **피처 정의·스키마·버전·소유자·계보 중앙 카탈로그** | Feast, Tecton |
| **Feature Transformer** | **단일 계산 로직으로 Offline/Online 양쪽 동시 생성** | Apache Spark, Flink |
| **Offline Store** | **PIT Join 지원 대용량 시점별 피처 이력 저장** | S3+Parquet, Delta Lake |
| **Online Store** | **추론용 최신 피처 저지연(ms 단위) 조회** | Redis, DynamoDB |
| **Feature Monitor** | **품질·신선도·학습-서빙 스큐 이상 탐지** | Evidently, Great Expectations |

#### 한줄 요약

- 한 가공기가 과거용 창고와 실시간용 선반에 값을 나눠 넣고 감시기가 둘의 상태를 확인한다.

## Ⅳ. 흐름도 (Feature Store를 통한 학습·추론 피처 공급 흐름)

<details><summary>핵심 용어</summary>

- **Data Leakage (데이터 누수)**: ML 모델 학습 시, 예측 시점 이후에 알게 된 정보(미래 데이터)가 학습 데이터에 포함되어 오프라인 성능이 실제보다 과대 평가되는 현상. PIT Join으로 방지.

</details>

```text
 1. [Feature 정의 등록] ── 계산식·입력 스키마·소유자·버전을 Registry에 고정
          │
          ▼
 2. [단일 정의 기반 변환 실행] ── 원천 데이터를 등록된 계산식으로 가공
          │
          ├─(학습 경로)──► 3. [PIT Join 기반 Offline 이력 생성]
          │                     - 예측 시점 이전 값만 결합 (누수 방지)
          │                     - 훈련 데이터셋으로 모델 학습에 제공
          │
          └─(추론 경로)──► 4. [Online Store 최신값 동기화]
                               - 동일 계산 로직 결과를 실시간 저지연 제공
                               │
                               ▼
 5. [품질·신선도·스큐 감시] ── Offline/Online 간 불일치 탐지 및 경보
          │
          ├─(이상 없음)──► 현재 피처 지속 제공
          └─(이상 탐지)──► 원천·정의 교정 후 2단계 반복
```

### 동작 원리

1. **단일 정의 기반 변환**: 하나의 계산 로직이 학습 이력(Offline)과 추론 최신값(Online)을 동시 생성하여 스큐 방지.
2. **PIT Join**: 예측 시점 이전 데이터만 학습에 투입하여 데이터 누수 차단.
3. **스큐 감시**: 학습 때 사용된 피처 분포와 운영 추론 입력 분포를 비교하여 이상 조기 탐지 (**Feature Store 사이클 완결**).

#### 한줄 요약

- 과거 학습에는 그 시점까지 알 수 있던 값만 넣고 같은 계산 결과를 운영 저장소에도 보낸다.

## Ⅴ. 종류 및 비교 (Feature Store 저장소 역할 1:1 비교)

<details><summary>핵심 용어</summary>

- **Feature Freshness (피처 신선도)**: 온라인 추론 시 제공되는 피처값이 얼마나 최신 데이터를 반영하는지를 나타내는 지표. 예: "지난 1시간 이내 갱신 보장". 신선도가 낮으면 오래된 정보로 잘못된 예측 위험.

</details>

| 피처 저장소 유형 | Offline Store | Online Store | Feature Registry |
|:---|:---|:---|:---|
| **용도** | **배치 ML 모델 학습·재현·백테스팅** | **실시간 추론 API에 피처 저지연 제공** | **피처 정의·버전·소유자 중앙 카탈로그** |
| **저장 형태** | 시점별 대용량 이력 (Parquet/Iceberg) | 최신값 Key-Value (Redis/DynamoDB) | 메타데이터 (DB/Git) |
| **응답 시간** | 수초~분 (배치) | 밀리초 이하 (실시간) | 수십 밀리초 (조회) |

#### 한줄 요약

- 과거 값은 큰 창고에서 학습에 쓰고 최신값은 빠른 선반에서 예측에 쓰며 이름표는 레지스트리가 관리한다.

## Ⅵ. 실무 고려사항 및 대책 (Feature Store 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

- **Feature SLA (피처 서비스 수준 협약)**: 피처 제공 시 보장되는 신선도(Freshness)·가용성·응답 시간에 대한 공식 합의. 모델 성능과 직결되므로, 피처 소유 팀과 사용 팀 간에 명시적으로 체결 필요.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 데이터 누수 (Data Leakage)** | PIT Join 없이 단순 조인으로 학습 데이터 생성 | **Feature Store의 PIT Join 기능을 필수 적용하여 예측 시점 이후 데이터 차단**|
| **2. 학습-서빙 스큐** | 학습팀과 서빙팀이 별도 피처 파이프라인 구현 | **Feature Transformer의 단일 계산 로직을 학습·추론 양쪽에 강제 공유** |
| **3. 피처 소유자 부재** | 피처 생성자가 이직하면 관리 공백 발생 | **Feature Registry에 소유자·SLA·폐기 절차를 필수 등록하고 정기 감사** |

> 사례: **Uber의 Michelangelo Feature Store, LinkedIn의 Feathr를 통한 수천 개 피처의 중앙 관리 및 팀 간 재사용으로 개발 생산성 향상, Airbnb의 Zipline Feature Store를 통한 학습-서빙 스큐 제거 사례**

#### 한줄 요약

- 사기 모델은 미래 거래 정보가 학습 입력에 섞이지 않도록 시점을 맞춘다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Feature Reusability (피처 재사용성)**: Feature Registry에 등록된 피처를 여러 모델 팀이 중복 개발 없이 검색·적용하는 것으로, Feature Store 도입의 핵심 경제적 가치.

</details>

- **피처 스토어 운영 기준**에 따라 모든 피처를 Feature Registry에 등록하고 **단일 계산 로직 공유 및 PIT Join 기반 훈련 데이터 생성** 원칙 준수

#### 한줄 요약

- 같은 피처 정의를 여러 모델이 재사용하되 과거와 현재 값이 같은 계산법으로 만들어지는지 확인한다.
