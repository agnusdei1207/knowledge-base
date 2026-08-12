---
sidebar:
  order: 135
  label: "135. 데이터 거버넌스 (Data Governance)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "데이터 거버넌스 (Data Governance)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Data Governance (데이터 거버넌스)**: 기업 전사의 데이터 자산에 대한 원칙(Principles), 정책(Policies), 프레임워크(Framework), 조직 체계(RACI)를 수립하여 데이터의 가치, 품질, 보안, 법적 준수성(Compliance)을 통제 및 보장하는 최고 경영 수준의 데이터 관리 체계.
- **Data Steward (데이터 스튜어드)**: 현업/IT 조직에서 전사 데이터의 의미 정의, 표준 단어 관리, 품질 이슈 및 보안 준수를 보살피고 모니터링하는 전문 데이터 담당자.
- **Policy-as-Code**: 데이터 거버넌스 정책(PII 암호화, 접근 제어)을 문서가 아닌 자동화된 오픈소스 코드(OPA)로 엔진에 직접 주입하여 강제 집행하는 모던 방식.

</details>

- 정의/개념: 기업 전사 데이터 자산의 무결성, 보안성, 가치 극대화를 위해 의사결정권, 표준 정책, 프로세스, 조직(Data Steward)을 정립하여 지속 관리하는 전사적 데이터 통제 체계인 **Data Governance**
- 배경/필요성: 개인정보보호법(PII), GDPR 등 글로벌 법적 규제 강화 수용, 부서별 파편화된 데이터 단어 불일치 및 품질 악화 극복 요구성

#### 한줄 요약

- 어떤 데이터를 누가 어떤 규칙으로 쓰고 지키며 위반을 고칠지 정하는 책임 체계이다.

## Ⅱ. 특징 (Data Governance 4대 전사 관리 축)

<details><summary>핵심 용어</summary>

- **Standardization & Compliance**: 단어/용어/코드 전사 표준화 및 보안 법적 준수성 100% 보장.
- **Continuous Quality Control**: 품질 게이트(Quality Gate) 및 정합성 검증의 주기적 자동화.

</details>

- **Organization & RACI Framework (데이터 소유자 Data Owner & Data Steward 지정)**
- **Data Quality & Standard Alignment (전사 메타데이터 단어, 코드 표준화)**
- **Security & Regulatory Compliance (PII 마스킹, RBAC/ABAC 접근 통제 및 GDPR 수용)**

#### 한줄 요약

- 규칙 문서만 만들지 않고 시스템 검사와 담당자 조치, 결과 지표까지 이어야 한다.

## Ⅲ. 구조 및 구성요소 (데이터 거버넌스 3대 축 및 RACI 아키텍처)

<details><summary>핵심 용어</summary>

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

| 거버넌스 관리 영역 | 핵심 관리 항목 및 메커니즘 | 실무 적용 결과물 |
|:---|:---|:---|
| **1. 데이터 표준 관리** | **전사 단어, 용어, 도메인, 공통 코드 체계 일체화**| **전사 표준 메타데이터 사전** |
| **2. 데이터 품질 관리** | **데이터 완전성, 유효성, 정확성 자동 검증 (Rule)**| **DQ 대시보드 (Null, Duplicate %)** |
| **3. 데이터 보안/흐름** | **PII 개인정보 암호화, 접근 권한 (RBAC) 및 Lineage** | **Automated Masking Policy** |
| **4. 데이터 거버넌스 조직**| **Data Council, Data Owner, Data Steward 지정 (RACI)**| **전사 거버넌스 R&R 규정 문서** |

#### 한줄 요약

- 데이터의 주인·검사 규칙·위반 조치 책임을 정한다.

## Ⅳ. 흐름도 (Data Governance 4단계 이행 프로세스)

<details><summary>핵심 용어</summary>

- **Data Profiling**: 데이터베이스 내부 데이터를 다차원으로 스캔하여 컬럼별 포맷 이탈, 널 비율, 이상치를 자동 진단하는 측정 기법.

</details>

```text
[1. 전사 데이터 프로파일링 (DQ Profiling)] ──► [2. 전사 단어/용어 표준화 (Standardization)]
                                                       │
                                                       ▼
  [4. 이행 모니터링 (Policy Enforcement)] ◄── [3. 거버넌스 수립 & Steward 지정 (RACI)]
```

### 동작 원리

1. **Profiling**: 소스 DB를 스캔하여 널 값, 포맷 이탈, 개인정보 유출 위험 요소 진단.
2. **Standardization**: 부서별로 다르게 쓰던 '주문금액', '수주금액' 단어를 전사 표준 단어로 단일 통합.
3. **Enforcement**: Policy-as-Code 엔진을 가동하여 미인가 쿼리 차단 및 PII 컬럼 자동 마스킹 (**거버넌스 완결**).

#### 한줄 요약

- 중요한 장부의 주인과 검사 규칙을 정하고 위반 증거를 담당자에게 돌려줘 고친다.

## Ⅴ. 종류 및 비교 (중앙집중형 거버넌스 대 연합형 거버넌스)

<details><summary>핵심 용어</summary>

- **Federated Computational Governance**: Data Mesh 아키텍처에서 사용하는 거버넌스 모델로, 전사 보안 규칙만 중앙 연합회가 정하고 세부 구현은 도메인이 수행.

</details>

| 비교 항목 | Centralized Data Governance | Federated Governance (Modern) |
|:---|:---|:---|
| **의사결정 주체** | **중앙 데이터 거버넌스 위원회 독점** | **중앙 연합회 + 현업 도메인 팀 협의** |
| **정책 집행 방식** | 수동 승인 및 인간 개입 중심 | **Policy-as-Code 자동 코드화 집행** |
| **조직 민첩성** | 느림 (모든 변경에 승인 절차 큐 발생) | **매우 빠름 (도메인 자율권 보장)** |
| **적합 아키텍처** | 전통적 모놀리식 DW / RDBMS | **Data Mesh, Data Lakehouse 아키텍처** |

#### 한줄 요약

- 거버넌스는 규칙과 책임을 정하고 데이터 관리는 그 규칙대로 실제 일을 한다.

## Ⅵ. 실무 고려사항 및 대책 (거버넌스 실패 방지 3대 해결책)

<details><summary>핵심 용어</summary>

- **Paper Governance Danger**: 거버넌스 규칙을 두꺼운 문서 규정집으로만 작성해 두고, 아무런 시스템 자동 통제가 없어 실무에서 무시되는 파행 안티패턴.

</details>

| 3대 거버넌스 위험 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Paper Governance** | 문서로만 규정을 만들고 시스템 자동 통제 0건 | **OpenPolicyAgent (OPA) 연동 Policy-as-Code 구현** |
| **2. Resistance from Devs**| 지나치게 빡빡한 수동 승인 절차로 개발 지연 | **Self-Serve 카탈로그 통합으로 1초 만에 권한 신청**|
| **3. PII Leakage Risk** | 개발DB로 원본 개인정보가 그대로 복제됨 | **데이터 수집 즉시 Masking / Anonymization 자동화**|

> 사례: **삼성전자 / 토스 / 카카오뱅크 전사 Data Governance & OpenMetadata 적용**

#### 한줄 요약

- 고객 연락처의 주인·검사 기준·가림 규칙·예외 종료일을 한 줄로 이어 관리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Data Governance 수립 기준(Data Governance Standards)**: RACI 프레임워크, Data Steward, Policy-as-Code 및 OpenMetadata 통합성에 의거한 체계.

</details>

- **Data Governance 수립 기준**에 따라 전사 데이터 자산 통제 구축 시 **Data Governance & Policy-as-Code** 필수 수용

#### 한줄 요약

- 중요한 장부부터 주인과 검사 장치를 정하고 예외가 영구 구멍이 되지 않게 관리한다.
