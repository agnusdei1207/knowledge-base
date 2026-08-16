---
sidebar:
  order: 135
  label: "135. 데이터 거버넌스 (Data Governance)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "데이터 거버넌스 (Data Governance)"
date: "2026-08-14T00:23:00+09:00"
tags:
  - "notes-software"
weight: 135
extra:
  question_no: "135"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "조직•표준•책임을 묶는 상위 데이터 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Data Governance (데이터 거버넌스)**: 기업 전사의 데이터 자산에 대한 원칙(Principles), 정책(Policies), 프레임워크(Framework), 조직 체계(RACI)를 수립하여 데이터의 가치, 품질, 보안, 법적 준수성(Compliance)을 통제 및 보장하는 최고 경영 수준의 데이터 관리 체계.
- **Data Steward (데이터 스튜어드)**: 현업/IT 조직에서 전사 데이터의 의미 정의, 표준 단어 관리, 품질 이슈 및 보안 준수를 보살피고 모니터링하는 전문 데이터 담당자.
- **Policy-as-Code**: 데이터 거버넌스 정책(PII 암호화, 접근 제어)을 문서가 아닌 자동화된 오픈소스 코드(OPA)로 엔진에 직접 주입하여 강제 집행하는 모던 방식.

</details>

- 정의/개념: 데이터 의사결정권•정책•책임의 **Data Governance**
- 배경/필요성: 분산 소유는 **용어•품질•보안•법규 집행 불일치** 유발

#### 한줄 요약

- 어떤 데이터를 누가 어떤 규칙으로 쓰고 지키며 위반을 고칠지 정하는 책임 체계이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Standardization & Compliance**: 단어/용어/코드 전사 표준화 및 보안 법적 준수성 100% 보장.
- **Continuous Quality Control**: 품질 게이트(Quality Gate) 및 정합성 검증의 주기적 자동화.

</details>

- **Organization & RACI Framework (데이터 소유자 Data Owner & Data Steward 지정)**
- **Data Quality & Standard Alignment (전사 메타데이터 단어, 코드 표준화)**
- **Security & Regulatory Compliance (PII 마스킹, RBAC/ABAC 접근 통제 및 GDPR 수용)**

#### 한줄 요약

- 규칙 문서만 만들지 않고 시스템 검사와 담당자 조치, 결과 지표까지 이어야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Data Owner vs Data Steward**: Data Owner는 비즈니스 측면 데이터 승인 및 최종 책임자, Data Steward는 데이터 품질 모니터링 및 실무 조치 담당자.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Data Governance Operating Architecture               │
├────────────────────────────────────────────────────────────────────────┤
│ [Data Governance Council (최고 데이터 거버넌스 위원회)]                  │
│                                │ (Policy & Decision)                   │
│        ┌───────────────────────┴───────────────────────┐               │
│        ▼                                               ▼               │
│ [Data Owners (현업 본부장)]                      [Data Stewards (실무진)]  │
│ (데이터 승인 및 정책 결정)                       (품질 점검 및 메타 관리) │
├────────────────────────────────────────────────────────────────────────┤
│ Automated Tooling: [Data Catalog]  [DQ Profiler]  [Policy Engine (OPA)]│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터 거버넌스 위원회가 수립한 전사 정책을 Data Owner와 Data Steward가 받아 카탈로그 및 OPA 정책 엔진으로 집행하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Governance Council | 전사 원칙•우선순위•분쟁 결정 |
| Data Owner | 도메인 데이터의 최종 승인•위험 책임 |
| Data Steward | 정의•품질•이슈 조치의 실무 운영 |
| Policy Engine | 접근•마스킹•보존 규칙 자동 집행 |
| Catalog•DQ Tool | 자산•계보•품질 증거와 지표 제공 |

#### 한줄 요약

- 데이터의 주인·검사 규칙·위반 조치 책임을 정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Data Profiling**: 데이터베이스 내부 데이터를 다차원으로 스캔하여 컬럼별 포맷 이탈, 널 비율, 이상치를 자동 진단하는 측정 기법.

</details>

```text
[거버넌스 대상]
      │
      ▼
1. 자산•위험 프로파일링
      │
      ▼
2. 정책•표준 정의
      │
      ▼
3. Owner•Steward 지정
      │
      ▼
4. 정책 자동 집행
      │
      ▼
5. 지표•예외 개선
```

### 동작 원리

1. **자산•위험 프로파일링**: 중요도•품질•민감도•규제 식별
2. **정책•표준 정의**: 용어•품질•접근•보존 규칙 명시
3. **Owner•Steward 지정**: 승인•운영•자문•통보 책임 배정
4. **정책 자동 집행**: 파이프라인•쿼리에서 규칙 검사•차단
5. **지표•예외 개선**: 위반•품질•예외 만료를 검토•조치

#### 한줄 요약

- 중요한 장부의 주인과 검사 규칙을 정하고 위반 증거를 담당자에게 돌려줘 고친다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Federated Computational Governance**: Data Mesh 아키텍처에서 사용하는 거버넌스 모델로, 전사 보안 규칙만 중앙 연합회가 정하고 세부 구현은 도메인이 수행.

</details>

| 비교 항목 | Centralized Data Governance | Federated Governance (Modern) |
|:---|:---|:---|
| 의사결정 주체 | **중앙 데이터 거버넌스 위원회 독점** | **중앙 연합회 + 현업 도메인 팀 협의** |
| 정책 집행 방식 | 수동 승인 및 인간 개입 중심 | **Policy-as-Code 자동 코드화 집행** |
| 조직 민첩성 | 일관성 높지만 승인 병목 가능 | 자율성 높지만 역량 편차 관리 필요 |
| 적합 아키텍처 | 전통적 모놀리식 DW / RDBMS | **Data Mesh, Data Lakehouse 아키텍처** |

#### 한줄 요약

- 거버넌스는 규칙과 책임을 정하고 데이터 관리는 그 규칙대로 실제 일을 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Paper Governance Danger**: 거버넌스 규칙을 두꺼운 문서 규정집으로만 작성해 두고, 아무런 시스템 자동 통제가 없어 실무에서 무시되는 파행 안티패턴.

</details>

| 3대 거버넌스 위험 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Paper Governance | 문서로만 규정을 만들고 시스템 자동 통제 0건 | **OpenPolicyAgent (OPA) 연동 Policy-as-Code 구현** |
| 2. Resistance from Devs | 지나치게 빡빡한 수동 승인 절차로 개발 지연 | **Self-Serve 카탈로그 통합으로 1초 만에 권한 신청**|
| 3. PII Leakage Risk | 개발DB로 원본 개인정보가 그대로 복제됨 | **데이터 수집 즉시 Masking / Anonymization 자동화**|

> 사례: **삼성전자 / 토스 / 카카오뱅크 전사 Data Governance & OpenMetadata 적용**

#### 한줄 요약

- 고객 연락처의 주인·검사 기준·가림 규칙·예외 종료일을 한 줄로 이어 관리한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Data Governance 수립 기준(Data Governance Standards)**: RACI 프레임워크, Data Steward, Policy-as-Code 및 OpenMetadata 통합성에 의거한 체계.

</details>

- 공통 위험은 **중앙 정책**, 도메인 세부 규칙은 연합형으로 위임

#### 한줄 요약

- 중요한 장부부터 주인과 검사 장치를 정하고 예외가 영구 구멍이 되지 않게 관리한다.
