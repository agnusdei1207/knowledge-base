---
sidebar:
  order: 204
  label: "204. 피처 스토어"
  badge:
    text: "기출 · 50%"
    variant: note
title: "피처 스토어 (Feature Store)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 204
extra:
  question_no: "204"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "특징 일관성과 재사용 구조가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **피처 스토어 (Feature Store)**: 머신러닝 학습용 과거 시계열 피처(Offline)와 실시간 추론용 초저지연 피처(Online)의 정의, 계산, 저장을 일원화하는 MLOps 데이터 플랫폼.
- **PIT Join (Point-in-Time Join)**: 학습 데이터 생성 시 관측 시점 이전의 피처값만 정확히 결합하여 미래 데이터 누수(Data Leakage)를 방지하는 조인 기법.

</details>

- 정의/개념: 머신러닝 학습과 실시간 추론에 사용되는 **피처(Feature)의 정의, 계산 로직, 저장, 공유를 중앙에서 일원화 관리하는 MLOps 플랫폼**
- 배경/필요성: 피처 계산 전처리 중복 개발에 따른 **리소스 낭비, 훈련-서빙 스큐(Training-Serving Skew) 및 학습셋 구축 시 미래 데이터 유입에 따른 데이터 누수(Data Leakage) 한계**

#### 한줄 요약
- 단일 피처 정의와 Offline/Online 이중 저장소를 통해 훈련-서빙 스큐와 데이터 누수를 원천 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Training-Serving Skew**: 학습 시의 피처 계산 로직과 운영 추론 시의 로직이 달라 예측 정확도가 급락하는 현상.
- **Offline / Online Dual Store**: 대용량 배치 학습 전용 저장소(Parquet/Delta)와 초저지연 실시간 서빙 전용 인메모리 저장소(Redis).

</details>

- 피처 정의와 계산 변환 로직을 중앙에서 1회만 선언하는 **단일 진실 공급원(Single Source of Truth)**
- 과거 시점의 정확한 스냅샷을 구성하여 데이터 누수를 방지하는 **PIT(Point-in-Time) Join 지원**
- 전사 데이터 과학자 간 피처를 검색하고 재사용하는 **피처 카탈로그 및 계보(Lineage) 관리**

#### 한줄 요약
- 단일 계산 정의, PIT Join, 온/오프라인 이중 저장을 통해 피처 정합성과 재사용성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **피처 스토어 4대 핵심 구조**: Feature Registry(메타데이터 정의), Transformation Engine(Spark/Flink 변환), Dual Storage(Offline/Online), Monitoring(품질 감시).

</details>

```text
[피처 스토어]
|-- 피처 레지스트리
|-- 변환 엔진
|-- 오프라인 저장소
|-- 온라인 저장소
`-- 품질 모니터링
```

선의 의미: 계층 및 Feature Registry의 정의에 따라 변환 엔진이 Offline(학습용)과 Online(추론용) 저장소에 동일한 피처값을 동기화 공급하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 피처 레지스트리 (Registry)| 피처의 이름, 데이터 타입, 계산 수식, 버전, 계보(Lineage)를 중앙 메타데이터로 보관 | 피처 정의 단일화 |
| 변환 엔진 (Transformer) | 배치 및 스트리밍 데이터를 받아 온라인과 오프라인 저장소에 동일한 계산 로직으로 적재| Spark, Flink |
| 오프라인 저장소 (Offline) | Parquet/Delta Lake 기반으로 대용량 시계열 과거 이력을 보관하고 PIT Join 학습셋 생성 | 학습 전용 스토리지 |
| 온라인 저장소 (Online) | Redis 기반으로 실시간 추론 모델에 최신 피처값을 10ms 이내 초저지연으로 제공 | 초저지연 인메모리 |
| 품질 모니터링 (Monitor) | 피처의 결측치 비율, 신선도(Freshness SLA), 온/오프라인 간 드리프트 스큐 실시간 감시 | 피처 품질 보증 |

#### 한줄 요약
- 레지스트리가 정의를, 변환 엔진이 동일 로직 적재를 맡고 두 저장소는 같은 값을 다른 접근 특성으로 보관하므로, 학습과 추론이 서로 다른 저장소를 써도 같은 피처를 본다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **피처 스토어 5단계**: 피처 정의 등록 $\to$ 단일 변환 파이프라인 $\to$ 온/오프라인 이중 적재 $\to$ PIT Join 학습셋 생성 $\to$ 실시간 추론 서빙.

</details>

```text
피처 엔지니어링 및 모델 서빙 가동
        │
   1. [피처 정의 등록] 데이터 엔지니어가 `user_30d_avg_spend` SQL 계산식과 버전을 Feast에 등록
        │
   2. [단일 변환 실행] 스트리밍 엔진이 Kafka 로그를 읽어 단일 로직으로 온/오프라인 변환
   ┌────┴───────────────────────────┐
  오프라인 적재 (학습용)            온라인 적재 (추론용)
   │                                 │
3A. [Delta Lake 시계열 저장]        3B. [Redis 실시간 갱신]
   과거 시계열 파티션 이력 적재          최신 피처값을 인메모리에 보관
   │                                 │
   ▼                                 │
4. [PIT Join 데이터셋 생성]          │
   관측 시점 이전 데이터만 결합      │
   │                                 │
   └────┬────────────────────────────┘
        ▼
   5. 실시간 결제 사기 탐지 API 호출 시 Redis에서 2ms 만에 피처를 조회하여 추론 서빙 완료
```

#### 한줄 요약
- PIT Join이 학습 시점 이후의 값을 잘라 내므로, 이 단계를 생략하면 검증 점수는 올라가고 운영 성능은 그만큼 떨어지는 누수 비용이 뒤늦게 청구된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Offline Store vs Online Store**: 대용량 배치 학습 전용(Offline)과 초저지연 실시간 추론 전용(Online).

</details>

| 비교 항목 | 오프라인 피처 저장소 (Offline Store) | 온라인 피처 저장소 (Online Store) |
|:---|:---|:---|
| 핵심 적용 목적 | 대규모 데이터셋 기반 모델 훈련, 배치 추론 | 사용자 요청 즉시 예측값을 반환하는 실시간 추론|
| 핵심 기술 스택 | Delta Lake, Apache Iceberg, BigQuery | Redis, Amazon DynamoDB, Cassandra |
| 주요 기능 특성 | 대용량 시계열 이력 보존, PIT Join 지원 | 초저지연 Key-Value 인메모리 조회 (<10ms) |
| 한계점 | 대용량 분산 쿼리로 실시간 밀리초 단위 서빙 불가 | 최신값 위주 보관으로 과거 시점 학습셋 생성 불가 |

#### 한줄 요약
- 배치 학습과 시계열 이력 관리는 Offline Store, 실시간 초저지연 추론 서빙은 Online Store를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Data Leakage**: 학습 시점의 피처 테이블에 예측 대상 사건 이후에 발생한 미래 정보가 섞여 들어가 운영 시 성능이 폭망하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단순 DB 조인으로 미래 데이터가 학습에 유입되는 **Data Leakage**(데이터 누수) | Feature Store의 `Point-in-Time (PIT) Join` 기능 의무화 | 데이터 누수 에러 원천 차단 |
| 학습 전처리 코드와 추론 전처리 코드 불일치로 모델 성능 급락 | `Feature Store` 단일 계산 로직을 학습/추론 양쪽에 강제 공유 | 훈련-서빙 스큐 제로화 |
| 담당자 퇴사로 인해 수천 개 피처의 정의와 계산 의존성 유실 | Feature Registry에 소유자(Owner), SLA, 계보(Lineage) 메타데이터 등록 | 전사 피처 재사용성 및 거버넌스 확보 |
| 온라인 저장소의 데이터 신선도 저하로 과거 피처로 추론 | 스트리밍 파이프라인 지연 모니터링 및 Freshness SLA 알람 구축 | 실시간 피처 최신성 100% 보장 |

#### 한줄 요약
- 네 대책은 피처를 일회용 코드가 아닌 자산으로 관리하기 위한 저장·감시 비용이며, 온라인 저장소의 신선도를 높일수록 스트리밍 파이프라인 부담은 커진다.

## Ⅶ. 결론

- 머신러닝 기반 대규모 실시간 추천, 이상 거래 탐지(FDS), 검색 랭킹 시스템에서 모델의 예측 품질과 서빙 성능을 보장하는 **가장 핵심적인 MLOps 데이터 엔지니어링 표준 인프라**로 정립되었으며, 실무 구축 시에는 **Feast/Hopsworks 기반 피처 레지스트리 단일화, Delta Lake/Iceberg 오프라인 저장소의 PIT Join을 통한 데이터 누수 차단, Redis 온라인 저장소를 통한 10ms 이내 초저지연 피처 조회, 신선도(Freshness SLA) 및 피처 드리프트 실시간 관측**을 결합하여 데이터와 머신러닝 간의 완벽한 정합성을 완성

#### 한줄 요약
- 피처 스토어는 단일 피처 정의, PIT Join, 온/오프라인 동기화를 통해 훈련-서빙 스큐와 데이터 누수를 해결하는 핵심 MLOps 데이터 인프라다.
