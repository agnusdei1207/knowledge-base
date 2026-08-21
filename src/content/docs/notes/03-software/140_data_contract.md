---
sidebar:
  order: 140
  label: "140. 데이터 계약 (Data Contract)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "데이터 계약 (Data Contract)"
date: "2026-08-14T00:58:00+09:00"
tags:
  - "notes-software"
weight: 140
extra:
  question_no: "140"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "생산자•소비자 간 스키마•품질 계약 현안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Data Contract (데이터 계약)**: 데이터 생산자(Producer)와 데이터 소비자(Consumer) 간에 주고받을 데이터의 스키마 구조, 데이터 타입, 의미(Semantics), SLA, 품질 지표(Expectations) 및 파괴적 변경(Breaking Change) 예고 수칙을 명시적으로 서명 체결하는 시스템 간 구두/코드 약정서.
- **Breaking Change (파괴적 변경)**: 생산자가 컬럼 삭제나 타겟 타입 변경(`String -> Int`)을 예고 없이 감행하여 하류 파이프라인(Snowflake, Dashboard)을 전면 붕괴시키는 현상.
- **Schema & Quality Enforcement**: CI/CD 파이프라인 내에서 Data Contract 명세서(YAML/JSON)와 실제 데이터간 일치성을 자동 검증하여 위반 시 적재를 즉시 블로킹하는 기술.

</details>

- 정의/개념: 생산자•소비자의 데이터 납품 약속인 **Data Contract**
- 배경/필요성: 예고 없는 스키마 변경은 **하류 파이프라인 연쇄 장애** 유발

#### 한줄 요약

- 자료의 모양·뜻·품질·변경 예고를 자동 검사할 수 있는 납품 약속이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Syntax & Semantic Guarantee**: 데이터 포맷 규격(Syntax) 및 업무 의미(Semantic)를 100% 보장.
- **SLA & Quality Bound**: 데이터 유입 지연 시간(SLA) 및 널 비율(Quality)을 명시적 수치화.

</details>

- **Explicit Binding between Producer & Consumer (생산자와 소비자 간 명시적 책임 배정)**
- **Syntax, Semantics, Quality, SLA 4대 종합 명세 정의**
- **Automated CI/CD Breaking Change Prevention (CI/CD 상에서 파괴적 변경 사전 블로킹)**

#### 한줄 요약

- 약속 문서만 두지 않고 설계 변경과 실제 납품 자료를 같은 규칙으로 검사해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Data Contract Spec (OpenDataContract Standard)**: `schema`, `quality`, `terms`, `servicelevel` 4대 파트로 작성되는 YAML 기반 규약서.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      Data Contract Specification (YAML)                │
├────────────────────────────────────────────────────────────────────────┤
│ dataset: "orders_v1"                                                   │
│ owner: "team-checkout@company.com"                                     │
│ schema:                                                                │
│   - column: "order_id", type: "string", required: true                 │
│   - column: "amount", type: "decimal", required: true                  │
│ quality:                                                               │
│   - type: "row_count", min: 1000                                       │
│   - type: "null_check", column: "order_id", max_null_percentage: 0.0   │
│ serviceLevel:                                                          │
│   freshness: "1 hour", availability: "99.9%"                           │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터 생산자가 작성한 Contract YAML 명세서에 따라 CI/CD 및 파이프라인에서 자동 검증을 렌더링하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Metadata•Owner | 데이터셋•버전•생산자•소비자 책임 명시 |
| Schema•Semantics | 열•타입•키•업무 의미 정의 |
| Quality Rules | 완전성•유효성•건수•분포 합격선 정의 |
| SLO•Terms | 신선도•가용성•보존•지원 수준 정의 |
| Evolution Policy | 호환성•예고 기간•버전 전환 규칙 정의 |

#### 한줄 요약

- 데이터의 모양·뜻·품질·변경 예고를 납품 약속으로 정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Contract CI/CD Gate**: DB 마이그레이션(PR) 시 Data Contract 명세와 비교하여 파괴적 변경 발생 시 PR Merge를 자동 차단하는 게이트.

</details>

```text
[스키마•파이프라인 변경]
       │
       ▼
1. 계약 변경안 생성
       │
       ▼
2. 호환성 검사
       │
       ▼
3. 소비자 영향 확인
       │
       ▼
4. 배포 Gate 판정
       │
       ▼
5. 런타임 품질 감시
```

### 동작 원리

1. 계약 변경안 생성: 스키마•의미•SLO 수정 사항 버전화
2. 호환성 검사: 기존 계약 대비 파괴적 변경 판정
3. 소비자 영향 확인: 계보로 하류 사용처•전환 기간 확인
4. 배포 Gate 판정: 승인•버전 분리•차단 중 조치 결정
5. 런타임 품질 감시: 실제 데이터와 신선도가 계약 준수 확인

#### 한줄 요약

- 납품 규격을 바꾸기 전에 기존 사용처가 깨지는지 검사하고 실제 자료도 같은 규격으로 검사한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **API vs Data Contract**: API Contract(OpenAPI/Swagger)는 서비스 통신용 인터페이스 계약, Data Contract는 파이프라인 수집/품질/SLA 데이터용 계약.

</details>

| 구분 | API Contract (OpenAPI/Swagger) | Data Contract (OpenDataContract) |
|:---|:---|:---|
| 주요 대상 | **Microservice 간 REST API 통신** | **이종 데이터 파이프라인 및 DW/Lake 수집** |
| 명세 내용 | Endpoint URL, Request/Response Body | **Schema, Quality Expectation, SLA, Freshness** |
| 파괴적 변경 대응 | API URL 버저닝 (`/v1/user` $\rightarrow$ `/v2/user`)| **Data Contract 버저닝 및 하류 의존성 차단** |
| 핵심 목적 | 서비스 동작 연동 보장 | **데이터 무결성 및 파이프라인 붕괴 방지** |

#### 한줄 요약

- 데이터 계약은 납품 내용과 품질, API 계약은 주문하고 받는 통신 규칙에 더 가깝다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Producer Resistance (생산자 저항)**: 데이터 계약 작성이 백엔드 개발자에게 추가 부담으로 작용하여 거부하는 현상.

</details>

| 3대 도입 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Producer Resistance | 백엔드 개발자가 YAML 작성 귀찮아함 | **DB DDL/Protobuf 에서 Contract YAML 자동 추출 도구 배포**|
| 2. Contract Drift | 계약서만 써 두고 시스템 자동 검증 부재 | **GitHub Actions CI/CD 게이트웨이에 Contract 검증 자동화**|
| 3. Legacy System Sync | 레거시 DB의 컬럼 타입 무차별 변경 | **Schema Registry 기반 Kafka Topic 과 Contract 연동** |

> 사례: **토스 / 당근마켓 / Databricks Data Contract 적용 사례**

#### 한줄 요약

- 주문서 양식을 바꿀 때 기존 사용처가 깨지는지 먼저 보고 실제 주문도 약속한 품질인지 다시 검사한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Data Contract 수립 기준(Data Contract Standards)**: OpenDataContract YAML 표준, CI/CD Gate, Data Mesh 통합 및 dbt/Great Expectations 연동성에 의거한 체계.

</details>

- 통신 동작은 **API Contract**, 데이터 의미•품질은 Data Contract 적용

#### 한줄 요약

- 좋은 계약은 약속을 적는 데서 끝나지 않고 바뀐 설계와 실제 납품을 모두 검사한다.
