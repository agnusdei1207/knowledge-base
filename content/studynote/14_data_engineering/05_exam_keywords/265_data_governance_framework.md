---
title: "265. 데이터 거버넌스 프레임워크 정책 표준 (Data Governance Framework DAMA DMBOK)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 거버넌스 프레임워크는 DAMA DMBOK2의 11개 지식영역(데이터 거버넌스, 데이터 아키텍처, 데이터 모델링·설계, 데이터 저장·운영, 데이터 보안, 데이터 통합·상호운용성, 문서·콘텐츠 관리, 참조·마스터 데이터, 데이터 웨어하우스·BI, 메타데이터 관리, 데이터 품질)을 하나의 **Plan-Govern-Build-Operate-Audit 사이클**로 통합하는 정책·표준·지침 체계이다. 핵심 산출물은 **Data Governance Charter, Data Policy/Standard, RACI Matrix, Data Catalog, Quality Rule Set**이다.
> 2. **가치**: Gartner에 따르면 데이터 거버넌스 성숙기업은 데이터 관련 의사결정 속도가 30~40% 향상되고, 데이터 품질 결함으로 인한 운영 비용을 연간 20~35% 절감하며, GDPR·개인정보보호법·ESG 공시 등 규제 준수 리스크를 사전에 차단하여 **컴플라이언스 위반 과징금 1건당 평균 4,500만~8억 원의 비용 회피 효과**를 거둘 수 있다. DGI(2022) 조사에서 DG 성숙도 Level 4 이상 기업은 데이터 활용 ROI가 평균 2.7배에 달한다.
> 3. **판단 포인트**: ① **집중형(Centralized) vs 분산형(Federated) vs 하이브리드** 거버넌스 모델 선택, ② **도구 의존도(Collibra/Informatica/Alation/Atlan) vs 프로세스·문화 우선** 접근, ③ 정책의 **세부화 수준(Semantic·Syntactic·Physical 3-tier)** 결정, ④ **데이터 도메인별 우선순위** (Master Data -> 거래 데이터 -> 분석 데이터 순), ⑤ **메타데이터 자동화율(목표 70% 이상)**과 **데이터 라인이지 자동 추적 커버리지** 사이의 트레이드오프가 핵심 설계 결정사항이다.

---

## Ⅰ. 개요 및 필요성

데이터는 21세기 기업의 핵심 생산요소로 부상했으나, **데이터 규모(Data Volume)·속도(Velocity)·다양성(Variety)의 폭발적 증가**와 함께 **데이터 사일로(Silo), 중복 정의, 비신뢰, 비표준, 비거버넌스 문제**가 심화되었다. McKinsey Global Institute(2021) 보고서에 따르면 대기업의 데이터 활용률은 전체의 **30% 미만**이며, 평균 **80%의 데이터 분석 프로젝트 시간**이 데이터 정제·통합·품질 이슈 해소에 소모된다. 또한 GDPR 시행(2018) 이후 글로벌 기업의 **평균 컴플라이언스 비용은 5년간 1.8배 증가**했으며, 국내에서도 개인정보보호법 강화, 데이터 산업법, AI 기본법(2025) 등으로 데이터 거버넌스 의무화가 가속화되고 있다.

DAMA International이 발간한 **DMBOK(DAMA Data Management Body of Knowledge) 2nd Edition(2017)** 및 **DMBOK2 2nd Revised Edition(2024)**은 11개 데이터 관리 지식영역(Knowledge Area, KA)을 체계화하고, 각 영역 간 **의존 관계(dependency)**와 **생명주기(lifecycle)**를 정의한 글로벌 표준 참조 모델이다. 이 중 **데이터 거버넌스(Data Governance, DG)** 지식영역은 다른 10개 영역의 **상위 통제(Over-arching Control) 계층**으로, 데이터 자산에 대한 **의사결정 권한·책임·프로세스·정책·표준**을 정의한다.

```text
[데이터 거버넌스 프레임워크의 비즈니스·기술적 필요성 구조]

    +----------------------- 비즈니스 압력 -----------------------+
    |  ● 규제: GDPR, CCPA, 개인정보보호법, AI기본법, ESG공시     |
    |  ● 시장: 데이터 기반 의사결정, AI/ML 학습데이터 신뢰성     |
    |  ● 운영: 데이터 사일로, 중복(2.4배 평균), 품질 결함(15~20%)|
    |  ● 비용: 컴플라이언스 과징금(평균 4,500만$), 소송·신뢰하락  |
    +----------------------------+-------------------------------+
                                 |
                                 v
    +-------------------- 거버넌스 미성숙 Pain Point --------------+
    |  ✗ Data Owner 부재 -> 책임 공백(Responsibility Vacuum)       |
    |  ✗ 용어 불일치 -> "고객" 정의가 시스템별로 상이(4.7개)        |
    |  ✗ 메타데이터 부재 -> 데이터 리니지 단절(83% 기업)            |
    |  ✗ 품질 규칙 부재 -> 결함 데이터가 다운스트림 전파            |
    |  ✗ 정책·표준 부재 -> 부서별 자체 규칙, Shadow Data 양산      |
    +----------------------------+-------------------------------+
                                 |
                                 v
    +------------------- DAMA DMBOK2 기반 프레임워크 --------------+
    |  +-----------------------------------------------------+    |
    |  |   11 Knowledge Areas + Plan-Govern-Operate Cycle    |    |
    |  |   ^                                                  |    |
    |  |   | (상위 통제 계층)                                 |    |
    |  |   +- Data Governance(거버넌스) -- 본 주제            |    |
    |  |   +- Data Architecture                              |    |
    |  |   +- Data Modeling & Design                         |    |
    |  |   +- Data Storage & Operations                      |    |
    |  |   +- Data Security                                  |    |
    |  |   +- Data Integration & Interoperability            |    |
    |  |   +- Document & Content Management                  |    |
    |  |   +- Reference & Master Data                        |    |
    |  |   +- Data Warehouse & BI                            |    |
    |  |   +- Metadata Management                            |    |
    |  |   +- Data Quality                                   |    |
    |  +-----------------------------------------------------+    |
    +-------------------------------------------------------------+
                                 |
                                 v
    +------------------- 기대 효과(Value Realization) -------------+
    |  ✓ 의사결정 속도 +30~40%  ✓ 데이터 결함 비용 -20~35%        |
    |  ✓ 규제 위반 리스크 차단   ✓ 데이터 활용 ROI 2.7배          |
    +-------------------------------------------------------------+
```

과거 **"데이터는 IT 부서가 관리"**라는 전통적 관점에서, **"데이터는 전사적 자산(Business Asset)"**이라는 현대적 관점으로의 패러다임 전환이 이루어졌다. 또한 **"데이터 품질은 사후 검증"**에서 **"데이터 거버넌스는 설계·생성 단계부터 내재화"**하는 **Data Governance by Design** 접근이 표준이 되었다. DMBOK1(2009) -> DMBOK2(2017) -> DMBOK2 Revised(2024) 진화를 보면, 단순 **데이터 관리(Data Management)**에서 **데이터 거버넌스 + 메타데이터 + AI 윤리**를 포괄하는 **데이터 생태계 거버넌스**로 확장되었음을 알 수 있다.

- **📢 섹션 요약 비유**: 데이터 거버넌스 프레임워크는 마치 **도시의 토지이용 계획(Zoning Ordinance)**과 같다. 도로·상업·주거·공공시설을 어떻게 배치할지 **상위 계획**이 없으면, 건물(데이터 시스템)은 각자 멋대로 지어져 정체·충돌·불량건축(데이터 사일로·중복·불일치)이 발생한다. DMBOK2는 그 토지이용 기본계획(General Plan)에 해당하는 **도시 설계 헌법**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DAMA DMBOK2의 데이터 거버넌스 프레임워크는 **5계층 레이어(Strategy -> Policy -> Standard -> Procedure -> Metric)**와 **3개 운영 메커니즘(Council, Stewardship, Tooling)**으로 구성된다. 핵심 원리는 **데이터에 대한 의사결정 권한을 데이터 발생·사용 도메인에 가깝게 두되(Substantiation), 전사 일관성은 상위 거버넌스에서 보장(Independence)**하는 것이다.

```text
[DAMA DMBOK2 데이터 거버넌스 프레임워크 상세 아키텍처]

        +------------------------------------------------------+
        | Layer 1: STRATEGY (전략)                              |
        |  • Data Vision / Mission / Data Strategy              |
        |  • Data Governance Charter (헌장)                      |
        |  • Data Value Framework (데이터 가치평가 모델)         |
        +------------------------+-----------------------------+
                                 |
                                 v
        +------------------------------------------------------+
        | Layer 2: POLICY (정책)        <--- 기술사 핵심 출제   |
        |  • Data Ownership Policy                              |
        |  • Data Classification & Handling Policy              |
        |  • Data Access & Privacy Policy                       |
        |  • Data Retention & Disposal Policy                   |
        |  • Data Quality Policy                                |
        |  • Data Sharing & Exchange Policy                     |
        +------------------------+-----------------------------+
                                 |
                                 v
        +------------------------------------------------------+
        | Layer 3: STANDARD (표준)                              |
        |  • Data Naming Convention (네이밍 규칙)               |
        |  • Data Definition Standard (비즈니스·기술 용어집)     |
        |  • Data Format Standard (ISO 8601, ISO 3166 등)       |
        |  • Data Modeling Standard (표준 ER/JSON Schema)        |
        |  • Metadata Standard (Dublin Core, ISO 23081)         |
        +------------------------+-----------------------------+
                                 |
                                 v
        +------------------------------------------------------+
        | Layer 4: PROCEDURE (절차)                             |
        |  • Data Issue Management Procedure                    |
        |  • Data Access Request Procedure                      |
        |  • Data Quality Issue Resolution Procedure            |
        |  • Data Lineage Tracking Procedure                    |
        |  • Metadata Registration Procedure                    |
        +------------------------+-----------------------------+
                                 |
                                 v
        +------------------------------------------------------+
        | Layer 5: METRIC (지표)                                |
        |  • Data Quality KPI (정확성 99.5%, 완전성 98%)        |
        |  • Metadata Completeness %  (목표: 90%+)              |
        |  • Data Issue MTTR, MTBF                              |
        |  • DG Maturity Score (DAMA CMMI DMM Level 1~5)       |
        |  • Compliance Audit Pass Rate                         |
        +------------------------+-----------------------------+
                                 |
        +------------------------+-----------------------------+
        | Layer 0: ORGANIZATIONAL MECHANISM (운영 메커니즘)     |
        |  +--------------------------------------------------+ |
        |  |  Data Governance Council(전사 거버넌스 위원회)   | |
        |  |   +- CDO/CAO (Chief Data/Analytics Officer)      | |
        |  |   +- Data Domain Owner (도메인별 책임자)         | |
        |  |   +- Business + IT + Legal + DPO 합동            | |
        |  +--------------------------------------------------+ |
        |  +--------------------------------------------------+ |
        |  |  Data Stewardship Network (데이터 스튜어드 조직) | |
        |  |   +- Enterprise Data Steward (전사)             | |
        |  |   +- Domain Data Steward (도메인)               | |
        |  |   +- Local Data Steward (시스템/팀)              | |
        |  +--------------------------------------------------+ |
        |  +--------------------------------------------------+ |
        |  |  Tooling Platform (도구 플랫폼)                  | |
        |  |   • Data Catalog (Collibra, Alation, Atlan)     | |
        |  |   • Data Quality (Informatica IDMC, Great Exp.) | |
        |  |   • Lineage (Octopai, MANTA, OpenLineage)       | |
        |  |   • Privacy (OneTrust, Securiti)                | |
        |  +--------------------------------------------------+ |
        +------------------------------------------------------+
                                 |
                                 v
        +------------------------------------------------------+
        |  11 Knowledge Areas (KA) <- 거버넌스가 통제          |
        |  Architecture, Modeling, Storage, Security, Quality, |
        |  Integration, MDM, DW/BI, Metadata, Content ...     |
        +------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Data Governance Charter** | 거버넌스 헌장(최상위 문서) | 데이터 거버넌스의 **목적·범위·원칙·지배구조(Governance Structure)**를 정의. CDO 권한, Council 운영규칙, 위반 시 제재 절차 포함. 일반적으로 **CDO + CEO + CIO + CISO + Legal** 합의 하에 공포. **위임장(Delegation of Authority, DoA)** 첨부. |
| **Data Policy (정책)** | 도메인별 행동 원칙 | **6대 핵심 정책**: ① 데이터 소유권(Ownership), ② 분류·취급(Classification, 4-tier: Public/Internal/Confidential/Restricted), ③ 접근·프라이버시(Access & Privacy), ④ 보존·폐기(Retention, 통상 5~10년), ⑤ 품질(Quality SLA 99.5%), ⑥ 공유·교환(Sharing Protocol). 각 정책은 **"Must / Should / May / Shall Not"** 4단계 의무강도 표기 (RFC 2119 방식). |
| **Data Standard (표준)** | 기술적·의미적 표준 | ① **Naming Convention**(PascalCase, snake_case 등), ② **Data Definition**(Glossary 내 표준 정의, 예: "고객 = 1개 이상의 거래 이력이 있는 자연인/법인"), ③ **Format Standard**(날짜=ISO 8601 `YYYY-MM-DD`, 국가코드=ISO 3166, 통화=ISO 4217), ④ **Modeling Standard**(표준 ERD 표기법: Barker/IE/Crow's Foot), ⑤ **Metadata Schema**(ISO 23081-1, Dublin Core 15요소). |
| **Data Procedure (절차)** | 정책·표준 실행 매뉴얼 | ① **데이터 이슈 관리**(ServiceNow/Jira 기반 티켓 흐름: Open -> Triage -> Root Cause -> Fix -> Verify -> Close, MTTR 목표 ≤5일), ② **데이터 접근 요청 절차**(Request -> Review by Data Owner -> Approver -> Provisioning, 통상 SLA 3일), ③ **메타
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 265 / 300

<- **이전**: [264. 마스터 데이터 관리 MDM 골든 레코드 (Master Data Management MDM Golden Record)](/studynote/14_data_engineering/05_exam_keywords/264_mdm_master_data/)
**다음**: [266. 데이터 사일로 해소 통합 전략 (Data Silo Breaking Integration Strategy)](/studynote/14_data_engineering/05_exam_keywords/266_data_silo_integration/) ->

---
