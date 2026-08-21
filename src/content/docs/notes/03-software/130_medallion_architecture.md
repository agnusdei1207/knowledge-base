---
sidebar:
  order: 130
  label: "130. 메달리온 아키텍처 (Medallion Architecture)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "메달리온 아키텍처 (Medallion Architecture)"
date: "2026-08-13T23:48:00+09:00"
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

- **Medallion Architecture (메달리온 아키텍처)**: Databricks가 정립한 데이터 레이크하우스 내부의 3단계 데이터 정제 파이프라인으로, 원시 데이터(Bronze) $\rightarrow$ 정제 데이터(Silver) $\rightarrow$ 비즈니스 집계 데이터(Gold) 3개 품질 계층으로 원자적 데이터 흐름을 체계화하는 설계 아키텍처.
- **Bronze Layer (Raw Ingest)**: 소스 시스템의 100% 동일 원 원천 데이터를 덤프 저장하여 언제든 재처리(Re-processing)가 가능한 원형 보존 계층.
- **Silver Layer (Cleaned & Conformed)**: Bronze 데이터를 널(Null) 정제, 중복 제거, 스키마 바인딩, 키(Key) 조인하여 비즈니스 유효 상세 상태로 다듬은 중간 계층.
- **Gold Layer (Curated Business)**: Silver 정제 데이터를 기반으로 마케팅, 재무, BI 보고서 및 ML 모델 학습 전용으로 최상위 스타 스키마 집계를 완료한 고품질 계층.

</details>

- 정의/개념: Bronze•Silver•Gold 품질 계층의 **메달리온 아키텍처**
- 배경/필요성: 원천 직접 분석은 **품질 편차•재처리•지표 신뢰** 문제

#### 한줄 요약

- 원석을 보관하고 불순물을 거른 뒤 용도별 제품으로 만드는 정제 구조이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Single Source of Truth (단일 진실 고리)**: Silver 계층에서 전사 공통 코드를 일체화하여 지표 불일치 소멸.
- **ACID-Backed Quality Incremental Promotion**: Delta Lake Open Table 기반으로 각 계층 승격 시 ACID 원자 커밋 보장.

</details>

- **3-Tier Data Quality Advancement (Bronze $\rightarrow$ Silver $\rightarrow$ Gold)**
- **Replayability Guarantee (Bronze 레이어 상시 원본 보존으로 언제든 재처리 가능)**
- **Schema Enforcement & Data Isolation (품질 검증 실패 데이터는 Quarantine 에 격리)** #### 한줄 요약

- 색깔별 폴더가 아니라 각 단계의 입학 기준과 탈락 사유, 다시 시작할 원본이 있어야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Quarantine Table (격리 테이블)**: Silver 계층으로 넘어갈 때 정식 품질 검사(Expectations)에 실패한 오류 레코드를 버리지 않고 별도 격리 보관하는 무결성 테이블.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Medallion Architecture Data Pipeline                 │
├────────────────────────────────────────────────────────────────────────┤
│ Raw Data Source ──► [Bronze Layer] (Raw Dump, Append-Only)             │
│                          │                                             │
│                          ▼ (Cleansing & Deduplication)                 │
│                     [Silver Layer] ──► (Quality Fail) ──► [Quarantine] │
│                          │                                             │
│                          ▼ (Business Aggregation & Star Schema)        │
│                     [Gold Layer] ──► [BI Dashboard / ML Features]      │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 원 원천 데이터가 Bronze 계층에 덤프된 후 품질 검사를 거쳐 Silver 및 Gold로 단계별 원자 승격되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Bronze | 원천 값•수집 시각•출처를 재처리용 보존 |
| Silver | 중복•오류 정제와 공통 스키마•키 적용 |
| Gold | 용도별 지표•마트•특징 데이터 제공 |
| Quarantine | 품질 실패 행과 규칙•사유 격리 |

#### 한줄 요약

- 원본 보관함부터 목적별 진열대까지 품질 단계를 나눈다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Delta Live Tables (DLT) Expectations**: Databricks DLT 환경에서 데이터 승격 시 `CONSTRAINT valid_id EXPECT (id IS NOT NULL) ON VIOLATION DROP ROW` 구문으로 품질 강제.

</details>

```text
[원천 데이터]
      │
      ▼
1. Bronze 적재
      │
      ▼
2. 품질 규칙 검증
      │
  ┌───┴────┐
  │통과    │실패
  ▼        ▼
3. Silver 정제  [Quarantine]
      │
      ▼
4. Gold 집계
      │
      ▼
5. 품질 증거 등록
```

### 동작 원리

1. Bronze 적재: 원천 데이터와 수집 메타데이터 보존
2. 품질 규칙 검증: 스키마•누락•중복•유효 범위 검사
3. Silver 정제: 통과 행을 표준화•결합•멱등 반영
4. Gold 집계: 검증 상세로 업무 지표•마트 생성
5. 품질 증거 등록: 통과율•실패 사유•리니지 기록

#### 한줄 요약

- Bronze 적재, 검증, Silver 정제, Gold 집계를 거치며 품질 증거를 남긴다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Data Maturity Progression**: Bronze (Raw 데이터) $\rightarrow$ Silver (검증 데이터) $\rightarrow$ Gold (비즈니스 가치 데이터).

</details>

| 구분 | Bronze Layer | Silver Layer | Gold Layer |
|:---|:---|:---|:---|
| 데이터 품질 상태 | 원천 보존 | 검증•표준화 상세 | 용도별 검증 집계 |
| 스키마 형태 | 소스 원본 스키마 | 3NF 정규화 / 공통 스키마 | **Star Schema / Cube / Mart** |
| 재처리 가능 여부 | **원천 스냅샷으로 상시 재처리 가능**| Bronze 기반 재생성 가능 | Silver 기반 재집계 가능 |
| 저장 스토리지 포맷 | Delta / Parquet / JSON | **Delta Lake Parquet** | **Delta Lake Parquet** |

#### 한줄 요약

- 브론즈는 원본, 실버는 검증된 공통 상세 데이터, 골드는 용도별 집계 지표이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Incremental Processing (증분 승격)**: Bronze $\rightarrow$ Silver $\rightarrow$ Gold 승격 시 전체 스캔을 피하고 Delta Change Data Feed(CDF)를 활용해 증분(Incremental) 승격 연산 수행.

</details>

| 3대 구축 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Full Reload Overhead | 승격 연산 시 매번 Bronze 전체 스캔 | **Delta Change Data Feed (CDF) 기반 증분 승격** |
| 2. Quarantine Storage Overflow | 품질 규칙 과도 설정으로 Quarantine 폭발| **품질 검증 규칙(Expectations) 단계적 임계치 완화** |
| 3. PII Security Leakage | Bronze에 개인정보(PII)가 생값으로 노출 | **Bronze 가동 즉시 해시/단방향 암호화 처리 적용** |

> 사례: **카카오페이 / Databricks Delta Live Tables(DLT) 기반 전사 메달리온 아키텍처 운용** #### 한줄 요약

- 불량 로그는 버리지 않고 이유와 함께 따로 두며 검사 결과가 맞아야 최종 지표를 바꾼다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **메달리온 수립 기준(Medallion Architecture Standards)**: Bronze/Silver/Gold 3단계 레이어링, Quarantine 격리, DLT Expectations 및 Delta CDF 증분승격성에 의거한 체계.

</details>

- 재처리 원본은 **Bronze**, 공통 상세는 Silver, 지표는 Gold 제공

#### 한줄 요약

- 각 단계가 무엇을 통과시켰고 실패하면 어디서 다시 시작할지를 증명해야 한다.
