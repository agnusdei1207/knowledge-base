---
sidebar:
  order: 189
  label: "189. EA 전사적 아키텍처 (Enterprise Architecture)"
  badge: { text: "기출 • 85%", variant: note }
title: "EA 전사적 아키텍처 (Enterprise Architecture)"
date: "2026-08-14T04:30:00+09:00"
tags: ["notes-software"]
weight: 189
extra:
  question_no: "189"
  source_status: "기출"
  source_history: "125회, 128회, 132회, 134회, 135회"
  priority: 85
  priority_note: "현행•목표•참조모형 설계가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **EA (Enterprise Architecture, 전사적 아키텍처)**: 조직의 비즈니스 목표와 이를 지원하는 IT 인프라(업무, 데이터, 애플리케이션, 기술)의 구조를 일정한 원칙과 표준에 따라 체계화한 전사적 마스터플랜 및 거버넌스 체계.
- **ITA (Information Technology Architecture)**: EA와 혼용되어 쓰이며, 공공부문에서는 '정보 기술 아키텍처'라는 이름으로 전자정부법에 의해 모든 공공기관의 도입 및 유지가 의무화된 제도.
- **Silo (사일로 현상)**: 각 부서가 전사 표준을 무시하고 독자적으로 시스템을 구축하여, 데이터가 연동되지 않고 중복 투자가 발생하는 현상. EA가 타파해야 할 최우선 과제.

</details>

- 정의/개념: BA•DA•AA•TA를 정렬•표준화하는 **EA Governance**
- 배경/필요성: 부서별 개별 구축으로 **Data 불일치•중복 투자** 증가

#### 한줄 요약

- 부서별 건물을 전사 도시계획과 공통 설계 기준에 맞추고 완공 결과를 다시 지도에 반영하는 관리 체계다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Reference Model (참조 모형)**: EA를 구축할 때 처음부터 바닥부터 그리지 않도록, 정부(범정부 EA)나 산업계가 미리 만들어둔 '표준 템플릿(업무, 데이터, 서비스, 기술 등)'.

</details>

- **Holistic View (전사적 관점)**: 개별 부서나 단일 프로젝트의 최적화(Local Optima)가 아닌, 기업 전체 관점에서의 최적화(Global Optima) 지향.
- **Business-IT Alignment (비즈니스와 IT 정렬)**: 모든 IT 투자는 철저하게 경영 전략(비즈니스 아키텍처)을 지원하는 방향으로만 승인되고 구축됨.
- **As-Is to To-Be Transition (현행에서 목표로의 전환)**: 현재 구조(As-Is)의 기술 부채와 중복을 식별하고, 목표 구조(To-Be)로 넘어가기 위한 전환 아키텍처(Transition Architecture) 중심의 관리.

#### 한줄 요약

- 현재 지도와 목표 지도 사이에 공사 중에도 업무를 유지할 전환 지도를 두고 각 사업이 그 경로를 따르는지 확인한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **EAMS (Enterprise Architecture Management System)**: 현행 및 목표 아키텍처 산출물, IT 자산 정보, 표준 지침 등을 DB화하여 시각적으로 보여주고 관리하는 EA 저장소 및 관리 시스템.

</details>

```text
[EA]
 ├── [BA | 업무•조직•Process]
 ├── [DA | Data 모델•표준•흐름]
 ├── [AA | Application•Service•연계]
 └── [TA | 기술 Infra•보안•표준]
```

| 구성요소 | 책임 |
|---|---|
| BA | 전략•조직•업무 Process와 **역량** 정의 |
| DA | 전사 Data 모델•흐름•**표준** 관리 |
| AA | Application Service•Interface **구조** 관리 |
| TA | Infra•보안•Cloud의 **기술 표준** 관리 |

#### 한줄 요약

- 네 영역의 설계도가 저장소에서 같은 자산을 가리키고 거버넌스가 사업 설계와 예외를 심사해야 전사 지도가 갈라지지 않는다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **TOGAF (The Open Group Architecture Framework)**: 전 세계적으로 가장 널리 쓰이는 오픈 그룹의 EA 프레임워크 표준으로, 아키텍처 개발 방법론인 ADM(Architecture Development Method)을 핵심으로 제공.

</details>

```text
[전략•변경 요구 입력]
          │
          ▼
[1. Architecture 비전 수립]
          │
          ▼
[2. BA•DA•AA•TA 설계]
          │
          ▼
[3. Gap•전환 과제 도출]
          │
          ▼
[4. Migration Roadmap 수립]
          │
          ▼
[5. 구현 Governance 수행]
          │
          ▼
[현행 Architecture 갱신]
```

### 동작 원리

1. **Architecture 비전 수립**: 범위•원칙•이해관계자 확정
2. **BA•DA•AA•TA 설계**: As-Is와 To-Be 구조 정의
3. **Gap•전환 과제 도출**: 목표 전환에 필요한 과제 식별
4. **Migration Roadmap 수립**: 의존성•비용•일정 기반 배치
5. **구현 Governance 수행**: 표준 준수 심사와 현행 구조 갱신

#### 한줄 요약

- 사업 착수 때 전사 기준으로 설계를 심사하고 완공된 구조를 저장소에 돌려놓아야 다음 사업이 실제 지도를 사용한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Zachman Framework (자크만 프레임워크)**: EA의 시초가 된 프레임워크로, 무엇을(What), 어떻게(How), 어디서(Where) 등 6하 원칙(행)과 설계자, 개발자 등 6가지 시각(열)을 교차하여 36개 셀로 아키텍처를 분류한 논리적 매트릭스.

</details>

| 비교 항목 | Zachman Framework | TOGAF | FEAF (미 연방정부 EA) |
|:---|:---|:---|:---|
| **핵심 성격** | **분류학 (Taxonomy) - 6x6 매트릭스 중심** | **방법론 (Methodology) - ADM 중심** | **참조 모형 (Reference Model) 중심**|
| **장점** | 아키텍처 산출물의 누락 여부 확인 용이 | **실제 EA를 구축하는 절차(How-to) 제공**| 공공기관 간 상호운용성 및 재사용성 극대화|
| **단점 (문제점)**| 구체적인 구축 방법이나 절차가 없음 | 범위가 너무 방대하여 도입 시 테일러링 필수 | 정부 주도형이라 민간 기업 적용은 제약됨 |

#### 한줄 요약

- 현재 건물을 운영하면서 목표 도시로 옮기려면 임시 도로와 공존 기간과 철거 순서를 담은 전환 지도가 필요하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Architecture Board (아키텍처 위원회)**: 신규 IT 사업을 발주하거나 시스템을 설계할 때, 해당 설계가 EA 원칙과 표준(TA 카탈로그 등)을 준수했는지 심사(Review)하고 승인 또는 예외를 처리하는 최고 의사결정 기구.

</details>

| 3대 EA 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. EA 무용론 (문서화 전락)** | 구축만 해놓고 현행화(Update) 안 함 | **IT 프로젝트 검수 시 EAMS 산출물 현행화 필수 조건화** |
| **2. 과도한 통제로 인한 반발** | 신기술 도입을 TA 표준이 가로막음 | **합당한 사유 시 한시적 예외(Exception) 승인 및 상환 계획 수립**|
| **3. 비즈니스 정렬 실패** | IT 부서만의 관점(DA, AA, TA)에 치중 | **업무 책임자(Business Owner)의 아키텍처 위원회 참여 의무화**|

> 사례: **행정안전부 주도의 범정부 EA(GEA) 기반 공공 정보화 사업 중복 투자 사전 심사 및 금융권 차세대 시스템의 ADM 기반 거버넌스 체계 구축 사례**

#### 한줄 요약

- 중복 고객 자료는 DA의 공통 정의와 소유권뿐 아니라 AA의 단일 제공 서비스까지 연결해야 새 복제본 생성을 막을 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **EA 거버넌스 (EA Governance)**: 만들어진 EA가 종이 쪼가리가 되지 않고 살아 숨 쉬도록, 아키텍처 위원회를 통한 프로젝트 심사, 표준 관리, 예외 통제를 강제하는 통치 체계.

</details>

- 표준 사업은 **BDAT 정렬 심사**, 신기술은 만료일 있는 예외 승인 적용

#### 한줄 요약

- 전사 구조는 문서 작성으로 끝내지 않고 사업 심사와 예외 만료와 구현 결과를 저장소에 순환시켜 실제 기준선으로 유지해야 한다.
