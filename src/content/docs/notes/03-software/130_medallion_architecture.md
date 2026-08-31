---
sidebar:
  order: 130
  label: "130. 메달리온 아키텍처"
  badge:
    text: "미출 · 50%"
    variant: note
title: "메달리온 아키텍처 (Medallion Architecture)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 130
extra:
  question_no: "130"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "브론즈•실버•골드 품질 계층 활용성 높음"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **메달리온 아키텍처(Medallion Architecture)**: 원시 데이터(Bronze) $\to$ 정제 데이터(Silver) $\to$ 비즈니스 집계(Gold) 3개 품질 계층으로 점진적 정제·승격시키는 데이터 파이프라인 아키텍처.
- **Bronze / Silver / Gold 계층**: 원천 포맷을 보존하는 Bronze, 정제와 결측치 처리를 거친 Silver, BI 및 AI에 특화된 최상위 집계 Gold.

</details>

- 정의/개념: 데이터 레이크하우스 환경에서 원시 데이터를 **Bronze(원시 수집), Silver(정제·표준화), Gold(비즈니스 집계) 3단계 품질 계층으로 점진적 정제·승격시키는 데이터 아키텍처**
- 배경/필요성: 원천 데이터(Raw Data)를 검증 없이 직접 분석에 활용할 때 발생하는 데이터 품질 결함, 결측치·이상치로 인한 지표 왜곡 및 분석가마다 상이한 전처리 로직으로 인한 단일 진실 공급원(SSOT) 붕괴 문제를 해결하기 위해, 원시 데이터를 불변 보존하는 Bronze, 정제·표준화·검증을 수행하는 Silver, 도메인별 고차원 집계 마트를 구축하는 Gold의 3단계 품질 계층 구조와 오류 격리(Quarantine) 체계를 도입하여 **데이터 파이프라인의 100% 재처리성(Replayability)과 최고 수준의 비즈니스 신뢰성을 동시에 확보**할 필요

#### 한줄 요약
- 품질 계층은 저장 비용과 지연을 대가로 정제 비용을 한 번으로 묶는 구조이므로, 계층을 늘릴수록 신뢰성은 오르지만 원천에서 지표까지의 시차도 함께 길어진다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Quarantine Table(격리 테이블)**: Silver 계층 승격 시 데이터 유효성 검증(Expectations)에 실패한 불량 레코드를 파기하지 않고 별도 격리하는 테이블.
- **Replayability(재처리 가능성)**: Bronze 계층에 원천 스냅샷이 항상 영구 보존되므로 비즈니스 로직 변경 시 언제든 전체 재연산 가능.

</details>

- 품질 완성도에 따라 점진적으로 데이터를 승격하는 **3단계 품질 계층화(Bronze $\rightarrow$ Silver $\rightarrow$ Gold)**
- 원시 데이터를 영구 보존하여 언제든 소급 재연산이 가능한 **완벽한 재처리성(Replayability)**
- 품질 검증 실패 데이터를 별도로 격리 보관하는 **격리 테이블(Quarantine Table) 운영**

#### 한줄 요약
- 3단계 품질 승격, 원천 재처리성 보장, 오류 데이터 격리를 통해 데이터 신뢰성을 확립한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **메달리온 4대 구성요소**: Bronze(원시 덤프), Silver(정제/표준화), Gold(비즈니스 마트), Quarantine(오류 격리).

</details>

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 브론즈 (Bronze Layer) | 원천 데이터와 수집 타임스탬프를 **가공 없이 원본 포맷 그대로 영구 보존** | 언제든 전체 재처리 가능 |
| 실버 (Silver Layer) | Null값 정제, 중복 제거, 스키마 표준화를 거쳐 **신뢰할 수 있는 공통 상세 테이블 구축** | 단일 진실 공급원(SSOT) |
| 골드 (Gold Layer) | 비즈니스 KPI 및 분석 요건에 맞추어 **스타 스키마 및 고차원 집계 마트 생성** | 초고속 BI/ML 서빙 |
| 격리 영역 (Quarantine) | 데이터 품질 규칙(Expectations)을 위반한 행을 **삭제하지 않고 오류 사유와 함께 격리** | 데이터 손실 방지 및 디버깅 |

#### 한줄 요약
- 브론즈(원시), 실버(정제), 골드(집계), 격리 영역이 유기적으로 연동된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DLT Expectations**: 데이터 승격 시 `EXPECT (id IS NOT NULL) ON VIOLATION DROP ROW` 등의 선언적 제약으로 품질을 강제하는 메커니즘.

</details>

```text
원천 시스템으로부터 신규 이벤트/로그 데이터 수집
        │
   [Bronze 적재] 소스 원본 데이터와 수집 메타데이터를 Bronze 테이블에 즉시 Append
        │
   [품질 규칙 검증] DLT Expectations 선언적 제약조건(Null 체크, 타입 검증) 검사
   ┌────┴───────────────────────────┐
  예 (품질 검증 통과)               아니오 (품질 위반 실패)
   │                                 │
[Silver 정제]                     [Quarantine 격리]
중복 제거, 코드 표준화,           불량 데이터 및 오류 원인 코드를
Delta Lake 포맷으로 승격          격리 테이블에 기록 후 알림
        │
   [Gold 집계] 부서별 비즈니스 KPI 및 차원 모델링 스타 스키마 구축
        │
   메타데이터 카탈로그에 품질 통과율 지표를 등록하고 BI/AI에 데이터 공개
```

#### 한줄 요약
- 불량 데이터를 버리지 않고 격리 영역으로 빼기에 파이프라인은 멈추지 않지만, 격리된 만큼 골드 지표가 조용히 과소 집계되므로 격리 물량 자체가 감시 대상이 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Bronze vs Silver vs Gold**: 원본 보존(Bronze), 정제 공통 상세(Silver), 비즈니스 집계 마트(Gold).

</details>

| 비교 항목 | Bronze Layer (원시 계층) | Silver Layer (정제 계층) | Gold Layer (집계 계층) |
|:---|:---|:---|:---|
| 데이터 품질 수준 | **원천 데이터 그대로 (Raw)** | **정제, 표준화 완료 (Validated)** | **고도로 가공된 비즈니스 수준** |
| 스키마 모델링 | 소스 원본 스키마 (JSON/CSV 등) | **3NF 정규화 / 공통 엔티티 모델** | **스타 스키마 / 차원 모델링 (Fact-Dim)**|
| 주 사용자 계층 | 데이터 엔지니어 | 데이터 분석가, 엔지니어 | **경영진, 현업 비즈니스 부서, AI 연구원**|
| 재처리 가능성 | **영구 보존으로 상시 재처리 가능** | Bronze 기반 언제든 재생성 가능 | Silver 기반 언제든 재집계 가능 |

#### 한줄 요약
- 브론즈는 원본, 실버는 검증된 공통 상세, 골드는 용도별 비즈니스 집계 지표다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CDF(Change Data Feed)**: Delta Lake에서 변경된 행만 증분 추적하여 Silver/Gold 승격 시 전체 스캔 부하를 제거하는 기능.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 승격 연산 시 매번 Bronze 전체 테이블을 스캔하는 I/O 낭비 | **Delta Change Data Feed(CDF) 기반 증분(Incremental) 승격** | 배치 처리 시간 80% 단축 |
| 과도한 품질 규칙으로 인한 Quarantine 격리 테이블 폭발 | **핵심 비즈니스 규칙 중심 단계적 임계치 완화 및 알림 자동화** | 파이프라인 정체 방지 |
| Bronze 계층에 개인정보(PII) 원본이 평문으로 노출 | **Bronze 수집 즉시 마스킹/단방향 암호화 토큰화 적용** | 컴플라이언스 및 개인정보 보호 |
| Gold 계층 집계 뷰 생성 지연으로 대시보드 새로고침 지연 | **Materialized View 및 캐싱 레이어(Cube) 사전 빌드** | 실시간 BI 대시보드 성능 확보 |

#### 한줄 요약
- Delta CDF 증분 승격, 품질 규칙 최적화, PII 즉시 암호화, 구체화 뷰 사전 빌드로 운영한다.

## Ⅶ. 결론

- 모던 데이터 레이크하우스 및 데이터 엔지니어링 파이프라인 구축의 **표준 계층화 품질 관리 아키텍처 패턴**으로 확립되었으며, 실무 구현 시에는 **승격 I/O를 최소화하는 Change Data Feed(CDF) 증분 파이프라인 구축, 불량 데이터 유입을 실시간 격리하는 선언적 품질 규칙(DLT Expectations/Great Expectations), Bronze 수집 즉시 개인정보(PII) 난독화 및 Gold 계층 사전 구체화 뷰(Materialized View) 최적화**를 결합하여 데이터 신뢰성과 엔드투엔드 처리 성능을 극대화

#### 한줄 요약
- 메달리온 아키텍처는 Bronze, Silver, Gold 3단계 품질 승격을 통해 데이터의 재처리성과 비즈니스 신뢰성을 동시에 보장하는 현대 레이크하우스의 핵심 설계 패턴이다.
