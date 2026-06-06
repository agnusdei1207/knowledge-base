---
title: "Repurchase SaaS Transition Replacement"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

# 445. 리퍼처스 SaaS 전환 교체 전략 (Repurchase SaaS Transition Replacement)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 레거시(On-Premise) 애플리케이션을 폐기(Retire)하고 동등 또는 유사 기능을 제공하는 상용 솔루션(COTS) 또는 SaaS(Software as a Service)로 전면 교체하는 6R(Application Migration to Cloud) 전략의 핵심 의사결정 모델로, **API-first 아키텍처**, **iPaaS(Integration Platform as a Service)**, **Fit-Gap 분석**이 3대 기술축을 이룬다.
> 2. **가치**: Gartner 및 McKinsey 분석 기준 Repurchase 기반 SaaS 전환 시 CapEx -> OpEx 전환으로 초기 투자비용 약 **60~75% 절감**, 라이선스·인프라·인력 운영비 합산 TCO는 3년 누적 기준 평균 **30~45% 감소**, TTM(Time To Market)은 평균 **18개월 -> 6개월로 단축**되는 정량적 효과를 도출한다.
> 3. **판단 포인트**: SaaS의 멀티테넌시 제약, Lock-in(Vendor Lock-in) 위험, 데이터 이관 시 다운타임, 커스터마이징 한계, 한국 클라우드 컴플라이언스(개인정보보호법·전자금융거래법·클라우드컴퓨팅법) 준수 여부, 기존 ERP/CRM/그룹웨어 등과의 API·iPaaS 통합 복잡도를 종합적으로 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 정의 및 등장 배경

**리퍼처스(Repurchase)**는 AWS Well-Architected Framework 및 Gartner의 애플리케이션 클라우드 마이그레이션 **6R(Rehost·Replatform·Repurchase·Refactor·Retire·Retain)** 전략 중 하나로, **기존 자체 구축(Legacy) 시스템을 버리고 시장 검증된 상용 제품(COTS: Commercial Off-The-Shelf) 또는 클라우드 네이티브 SaaS로 구매 전환(Buy)하는 전략**이다. 이는 한국 정보시스템 감리 가이드라인의 "패키지 도입" 및 "SaaS 전환" 의사결정과 동일한 맥락이며, 2018년 「클라우드컴퓨팅 발전 및 이용자 보호에 관한 법률」 시행 이후 공공·금융권을 중심으로 적용 사례가 폭증하고 있다.

```text
+------------------------------------------------------------------------+
|         레거시 시스템 진단 -> Repurchase SaaS 전환 의사결정 플로우        |
+------------------------------------------------------------------------+
[Step 1: 비즈니스 전략 수립]                    [Step 2: 현행 시스템 분석]
  - 디지털 트랜스포메이션 목표설정                 - 기능/비기능 요구사항 도출
  - 비용 최적화/탄력적 운영 요구                  - 업무 프로세스 매핑(BPMN)
        |                                                |
        v                                                v
[Step 5: SaaS 운영/최적화]              [Step 3: Fit-Gap 분석]
  - SLA 모니터링 / FinOps 적용         +------------------------------+
  - iPaaS 기반 자동화                  |  업무 80% 일치 -> Repurchase ✓ |
  - 정기 릴리즈/업그레이드 관리        |  업무 50% 일치 -> Replatform △ |
                                      |  업무 30% 이하  -> Rehost/Refactor |
        ^                             +------------------------------+
        |                                                |
[Step 4: 전환 및 마이그레이션]                         v
  +- Data Migration (ETL/CDC)         [Decision Gate: TCO·ROI·Lock-in]
  +- Dual-Run / Pilot 운영                       |
  +- API / iPaaS 통합                              v
  +- Cut-over 및 레거시 폐기           ---> SaaS (예: SAP S/4HANA Cloud,
                                             Salesforce, Workday, MS 365,
                                             Coupa, ServiceNow, nCino)
```

### 2. 도입 필요성: 레거시 -> SaaS 전환 압박 요인

| 압박 요인 | 구체적 현황 | 기술적 시급성 |
| :--- | :--- | :--- |
| **기술부채(Technical Debt)** | COBOL, VB6, PowerBuilder 기반 메인프레임/클라이언트 시스템의 인력 고령화(2027년 베이비부머 퇴직), EOL(End of Life) 도래 | 신규 기능 추가 시 비용 4배 증가(Squore Labs 분석) |
| **TCO 절감** | HW 라이선스 + DC 운영 + 유지보수 인건비의 구조적 비용 상승 | 3년 누적 TCO에서 On-Prem 대비 SaaS가 30~45% 저렴 |
| **업무 민첩성** | 신사업·시장 변화 대응에 6~18개월 소요(Waterfall) | SaaS 릴리즈 주기(Quarterly)를 통한 즉시 기능 획득 |
| **원격·하이브리드 근무** | COVID-19 이후 VPN/RDP 기반 시스템의 접속 폭주 | SaaS는 본질적으로 Any-Device/Any-Where 지원 |
| **규제 환경** | 「클라우드컴퓨팅법」, 「개인정보보호법」, 「전자금융감독규정」의 클라우드 이용 허용 | SaaS 전환 시 인증심사(CSAP) 통과 필수 |
| **AI/데이터 분석** | 레거시 DW는 비정형·실시간 데이터 처리 불가 | SaaS는 Native AI/ML(Databricks Lakehouse, Snowflake 등) 통합 |

### 3. 기존 On-Premise vs Repurchase SaaS 패러다임 비교

```text
+----------------------+                      +------------------------------+
|   레거시(자체 구축)   |                      |   Repurchase SaaS (구매 전환)  |
+----------------------+                      +------------------------------+
| -> CapEx 중심 투자     |                      | -> OpEx 기반 구독(Subscription)|
| -> 3~5년 주기 업그레이드|  -----Repurchase-----> | -> 분기(Quarterly) 무중단 릴리즈|
| -> HW/OS/DB 튜닝 필수  |                      | -> Vendor가 멀티테넌시 운영   |
| -> 수직확장(Scale-Up)  |                      | -> 수평확장(Scale-Out) 자동화  |
| -> 데이터센터 운영     |                      | -> 리전 기반 글로벌 가용성    |
| -> 전담 유지보수 조직   |                      | -> Shared Responsibility 보안 |
+----------------------+                      +------------------------------+
```

- **📢 섹션 요약 비유**: 마치 직접 짓고 관리하던 **수제 가옥(자체 시스템)**을, 세계적 브랜드의 **관리형 아파트(SaaS)**로 이사 가는 것과 같습니다. 직접 청소·보수할 필요는 없지만, 관리비(구독료)를 내야 하고 인테리어(커스터마이징)는 관리 규약(SaaS 제약) 안에서만 가능합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Repurchase SaaS 전환의 5-Layer 참조 아키텍처

```text
+-------------------------------------------------------------------------+
|                  Repurchase SaaS 전환 5계층 아키텍처                      |
+-------------------------------------------------------------------------+
[Layer 1: Presentation (사용자 접점)]
  +--------------+  +--------------+  +--------------+
  | Web Browser  |  | Mobile App   |  | API Client   |
  | (SPA/React)  |  | (iOS/Android)|  | (B2B/EDI)    |
  +------+-------+  +------+-------+  +------+-------+
         +------------------+------------------+
                            |  HTTPS / OAuth 2.0 / OIDC / SAML
                            v
[Layer 2: Identity & Access (통합 인증)]
  +------------------------------------------------+
  |  IdP (Azure AD / Okta / Ping / Korean Sign-On) |
  |  - SSO / MFA / SCIM (Just-In-Time Provisioning)|
  |  - RBAC / ABAC (SaaS 내 권한 위임)              |
  +--------------------+---------------------------+
                       v
[Layer 3: SaaS Application (구매 전환 대상)]
  +--------------+  +--------------+  +--------------+
  |  ERP SaaS    |  |  CRM SaaS    |  |  HCM SaaS    |
  | (SAP S/4HC)  |  | (Salesforce) |  | (Workday)    |
  | (Oracle ERP) |  | (MS D365)    |  | (Darwinbox)  |
  +------+-------+  +------+-------+  +------+-------+
         +------------------+------------------+
                            | REST/GraphQL/gRPC API + Webhook
                            v
[Layer 4: Integration (iPaaS / API Gateway)]
  +------------------------------------------------+
  |  MuleSoft / Boomi / Workato / Apache Kafka     |
  |  - Event-driven Architecture (Pub/Sub)         |
  |  - ETL/ELT (Fivetran, Airbyte, Informatica)    |
  |  - API Management (Kong, Apigee, AWS API GW)   |
  +--------------------+---------------------------+
                       v
[Layer 5: Data & Analytics (Data Mesh / Lakehouse)]
  +------------------------------------------------+
  |  Snowflake / Databricks / BigQuery / Redshift   |
  |  - Master Data Management (MDM)                |
  |  - Data Quality / Lineage / Catalog            |
  +------------------------------------------------+
```

### 2. 핵심 구성 요소 및 동작 원리

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Fit-Gap 분석 엔진** | 현행 업무 vs SaaS 표준 프로세스 매칭 | BPMN 2.0 기반 AS-IS/TO-BE 모델링, Gap 항목은 **Configurable**(설정 변경) / **Customizable**(코드 변경) / **Infeasible**(불가능) 3단계로 분류 |
| **데이터 마이그레이션 도구** | 레거시 DB -> SaaS 이관 | **Bulk Load**(초기 대용량), **CDC(Change Data Capture)**(운영 중점), **Reverse ETL**(SaaS -> DW 동기화) — 예: AWS DMS, Azure Data Factory, Fivetran |
| **iPaaS(Integration Platform as a Service)** | SaaS ↔ On-Prem ↔ 타 SaaS 통합 | MuleSoft Anypoint Platform, Dell Boomi, Workato, Microsoft Power Automate, Apache Camel |
| **API Gateway / ESB** | API 트래픽 라우팅, 보안, 변환 | Kong Gateway, Apigee, AWS API Gateway, WSO2 — OAuth 2.0, JWT, Rate Limiting, Throttling, Schema Validation |
| **IdP(Identity Provider)** | SSO, MFA, Lifecycle 관리 | Azure AD(Entra ID), Okta CIC, Ping Identity, 클라우드 인증(클컴법 §13의 안전성 확인) |
| **마스터 데이터 거버넌스(MDM)** | 고객·상품·조직 등 핵심 데이터 일관성 | Informatica MDM, Reltio, Profisee, SAP Master Data Integration |
| **FinOps / SaaS 관리(SPM)** | 라이선스 최적화, 사용량 모니터링 | Zylo, Productiv, Torii, CloudHealth, Salesforce Optimizer |
| **컴플라이언스 감사 체계** | CSAP, ISO 27001/27701, SOC 2, PCI-DSS | 한국인터넷진흥원(KISA) CSAP 인증, 클라우드컴퓨팅법 §23(안정성·신뢰성 평가) |

### 3. Repurchase 의사결정 알고리즘 (의사결정 트리)

```text
                    +-----------------------------+
                    | 현행 시스템의 비즈니스 가치   |
                    | (Business Criticality) 평가 |
                    +------------+----------------+
                                 |
                +----------------+-----------------+
                v                v                 v
        [상(Critical)]    [중(Important)]     [하(Non-Core)]
        핵심 업무·매출     내부 운영           단순 반복 업무
                |                |                 |
                v                v                 v
        Fit ≥ 80%인가?    Fit ≥ 60%인가?     Fit ≥ 90%인가?
           /      \           /    \              /    \
         Yes       No       Yes     No         Yes      No
          |         |        |       |           |       |
          v         v        v       v           v       v
     +--------+ +------+ +------+ +------+  +--------+ +---------+
     |Repurch-| |Refac-| |Repur-| |Main- |  |Repur-  | |Rehost/  |
     |ase SaaS| |tor + | |chase | |tain  |  |chase   | |Retire   |
     | (Buy)  | | SaaS | | SaaS | |(유지)|  | SaaS   | |(폐기)   |
     +--------+ +------+ +------+ +------+  +--------+ +---------+
        TCO      TCO^     TCO      -          TCOv       TCOv
        v30%     복잡^     v30~45%                          -
```

### 4. 핵심 파라미터 및 정량 평가 지표

| 평가 차원 | 지표 | 산출 공식/임계치 |
| :--- | :--- | :--- |
| **기능 적합도** | Fit-Rate | $\text{Fit-Rate} = \frac{\text{SaaS 표준 기능과 일치하는 요구사항 수}}{\text{전체 요구사항 수}} \times 100$ |
| **TCO 비교** | 3년 누적 소유비용 | $TCO_{SaaS} = \sum_{t=1}^{3}(License_t + Integration_t + Migration_t + Training_t)$ |
| **ROI** | 투자회수율 | $ROI = \frac{\sum Benefit - \sum Cost}{\sum Cost} \times 100$ (목표 ≥ 150%) |
| **통합 복잡도** | API Endpoint 수 | 1
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 445 / 800

<- **이전**: [444. 리팩터 클라우드 네이티브 재설계](/studynote/13_cloud_architecture/06_exam_summary/444_refactor_cloud_native_redesign/)
**다음**: [446. 리타이어 폐기 합리화 전략](/studynote/13_cloud_architecture/06_exam_summary/446_retire_decommission_rationalization_strategy/) ->

---
