+++
title = "642. IT 경영 관리 핵심 토픽 642번 시험 요약 (IT Management Core Topic 642 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 6-4-2 프레임워크는 **6대 핵심 영역(IT 거버넌스·포트폴리오·서비스·아키텍처·보안·조직역량)** × **4대 추진 체계(전략연계·성과측정·변화관리·리스크관리)** × **2대 목표(운영효율·가치창출)** 의 입체 구조로 COBIT 2019, ITIL 4, ISO 38500, balanced scorecard를 융합한 전략적 IT 경영 통합 모델이다.
> 2. **가치**: McKinsey 2023 보고 기준 전사 IT 거버넌스 성숙도 1단계 → 4단계 도달 시 **IT 예산 대비 ROI 23~47% 향상, Shadow IT 60% 감소, Time-to-Market 35% 단축, MTTR(평균복구시간) 78% 감축, TCO(총소유비용) 30~40% 절감** 등 정량적 효과를 산출한다.
> 3. **판단 포인트**: 기술사 핵심 trade-off는 **①집중형(Centralized) vs 분산형(Federated) 거버넌스, ②COBIT vs ITIL vs ISO 27001 프레임워크 우선순위, ③SaaS·Public Cloud 비중 확대 시 통제력 저하 대응, ④Agile/DevOps 운영모델과 전통 PMBOK waterfall의 병행 운영, ⑤AI/ML 도입 시 윤리·Explainability 거버넌스 통합 여부** 이다.

---

## Ⅰ. 개요 및 필요성

1990년대 이후 ERP·CRM·SCM의 전사적 도입으로 IT는 단순 지원(Support) 기능에서 **전략 동인(Strategic Enabler)** 으로 위상이 격상되었으나, 2010년대 클라우드·모바일·빅데이터, 2020년대 AI·생성형AI·Web3·Quantum 시대에 접어들면서 IT 투자 규모 대비 성과 가시화가 미흡하고, **Shadow IT(전체 IT 지출의 30~40%, Gartner 2023)** 와 **이중 투자(Duplicated Spending)**, **규제 리스크(개인정보보호법·ESG 공시)** 가 폭증하고 있다.

특히 한국 시장은 **①대·중소기업 IT 성숙도 양극화(상위 5% vs 하위 60%), ②공공·금융·의료의 규제강도(전자금융감독규정·의료법·PIPC 가이드라인), ③DX(디지털전환) 가속화에 따른 Legacy-Digital 하이브리드 운영 부담, ④2024년 AI 기본법(가안) 및 EU AI Act 대응** 등 독자적 과제가 존재한다.

```text
   ┌──────────────────────────────────────────────────────────────────┐
   │            IT 경영 관리 6-4-2 프레임워크 전체 조감도                  │
   │                                                                  │
   │      [2대 목표: 궁극적 가치 지향점]                                  │
   │       ┌─────────────────┐        ┌─────────────────────┐         │
   │       │ 운영효율·비용최적화 │  +    │ 비즈니스 혁신·가치창출 │         │
   │       │   (Run the Biz) │        │   (Grow/Transform)   │         │
   │       └────────┬────────┘        └──────────┬──────────┘         │
   │                │  ▲                          │  ▲                 │
   │                ▼  │                          ▼  │                 │
   │      ┌─────────────────────────────────────────────────┐          │
   │      │   [4대 추진 체계: How - 실행 메커니즘]              │          │
   │      │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐│          │
   │      │  │전략-실행  │ │성과측정  │ │변화관리  │ │리스크 ││          │
   │      │  │연계체계   │ │평가체계  │ │체계     │ │관리   ││          │
   │      │  │(SAM/EA)  │ │(BSC/KPI) │ │(ADKAR)  │ │(ISO) ││          │
   │      │  └──────────┘ └──────────┘ └──────────┘ └──────┘│          │
   │      └─────────────────────────────────────────────────┘          │
   │                │  ▲                                               │
   │                ▼  │                                               │
   │      ┌─────────────────────────────────────────────────┐          │
   │      │   [6대 핵심 영역: What - 통제 대상]               │          │
   │      │  ①IT전략·거버넌스  ②포트폴리오  ③서비스관리       │          │
   │      │  ④아키텍처        ⑤보안·리스크   ⑥조직·역량       │          │
   │      └─────────────────────────────────────────────────┘          │
   │                │                                                  │
   │                ▼                                                  │
   │   [비즈니스 요구(Business Demand) / 규제(Regulation) / 기술(TRM)] │
   └──────────────────────────────────────────────────────────────────┘
```

**기존 패러다임 대비 신규 패러다임**:
- **Old (2000s)**: Silo 운영 — CIO가 전 IT 결정 → 부서별 스파게티 시스템 → ROI 측정 불가
- **Transition (2010s)**: CoE(Center of Excellence) + BICC(Business IT Co-ownership)
- **New (2020s~)**: **Federated/Networked governance** + Product-centric + FinOps + AI 거버넌스 통합

- **📢 섹션 요약 비유**: 6-4-2 프레임워크는 마치 **오케스트라의 지휘자** 와 같다. 6대 영역은 각 악기(현악·목관·금관·타악 등), 4대 추진 체계는 지휘棒的 동작법(리듬·다이내믹·표현), 2대 목표는 최종 연주곡(클래식=효율, 재즈=혁신)이다. 지휘자 없이 연주하면 소음(Shadow IT)이 되고, 지휘봉만 휘두르면 음악이 되지(전략만 있고 실행 없음) 못한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 6대 핵심 영역 상세

```text
   ┌──────────────────────────────────────────────────────────────────┐
   │              6대 핵심 영역 × 4대 추진체계 매핑 매트릭스              │
   │                                                                  │
   │                전략-실행  성과측정  변화관리  리스크관리              │
   │              ┌─────────┬─────────┬─────────┬─────────┐           │
   │  ① IT전략·   │ COBIT   │ BSC·KRI │数字化   │ ISO38500│           │
   │   거버넌스    │ EDM-01  │  Score  │ 전략맵  │ ITGC   │           │
   │              ├─────────┼─────────┼─────────┼─────────┤           │
   │  ② 포트폴리오 │ TOGAF·  │ NPV·IRR │ Stage-  │ 프로젝트 │           │
   │   관리       │ ADM     │ ·PI값   │ Gate    │ Risk    │           │
   │              ├─────────┼─────────┼─────────┼─────────┤           │
   │  ③ 서비스    │ ITIL4   │ SLA·CSI │ Service │ ITSCM   │           │
   │   관리       │ SVS·34p│ ·CSAT   │ Transition│        │           │
   │              ├─────────┼─────────┼─────────┼─────────┤           │
   │  ④ 아키텍처  │ EA·TOGAF│ TAM·SA  │ Migration│ 사이버  │           │
   │   관리       │ ADM     │ Maturity│ Roadmap  │ 레질리언스│          │
   │              ├─────────┼─────────┼─────────┼─────────┤           │
   │  ⑤ 보안·     │ NIST CSF│ KCI·MTD │ Security│ ISO27001│           │
   │   리스크     │ ·ISMS-P │ ·RPO/RTO│ Awareness│ ·PIPC   │           │
   │              ├─────────┼─────────┼─────────┼─────────┤           │
   │  ⑥ 조직·     │ SFIA·   │ 학습·   │ Prosci  │ 인사·   │           │
   │   역량       │ DMBOK   │ CERT    │ ADKAR   │ 채용    │           │
   │              └─────────┴─────────┴─────────┴─────────┘           │
   └──────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **① IT 전략·거버넌스 (IT Strategy & Governance)** | 전사 IT 방향성 결정, 의사결정 권한·책임 구조(상위거버넌스-이사회, 중위-이사회IT위원회, 하위-IT실행조직) 정의 | **COBIT 2019** 의 5지배원칙(Stakeholder Value, Holistic Approach, Dynamic Governance, Distinct Governance vs Management, Tailored to Enterprise Needs) + **ISO/IEC 38500** IT 거버넌스 6원칙(책임·전략·수행·적합성·규율·인간행태) + RACI 매트릭스 + IT Steering Committee 분기 1회 운영 |
| **② IT 포트폴리오 관리 (IT Portfolio Management)** | 투자(App·Infra·Data·People·Risk 5카테고리)·프로젝트·프로그램·제품 포트폴리오 우선순위화·재조정 | **Stage-Gate(Cooper, 5-Gate 모델)**, **WSJF(Weighted Shortest Job First)**, **PI(Program Increment) Planning in SAFe**, **FinOps** (클라우드 비용 최적화), **TBM(Technology Business Management)** 의 4계층 cost model |
| **③ IT 서비스 관리 (IT Service Management)** | 비즈니스에 IT 서비스를 안정적·효율적으로 전달(Service Strategy→Design→Transition→Operation→CSI) | **ITIL 4** 의 34개 Practice(General·Service·Technical Management 3분류) + **SLO/SLI/SLA 3-tier** (예: Availability 99.95%, MTTR<30분) + AIOps(Datadog·Dynatrace·Splunk ITSI) + ChatOps + Observability(Logs·Metrics·Traces) |
| **④ IT 아키텍처 관리 (IT Architecture Management)** | 업무·데이터·응용·기술 4A 아키텍처 정합성 확보 및 Legacy→Digital 전환 로드맵 | **TOGAF ADM**(Preliminary→A~H Phase) + **Zachman 6×6 매트릭스** + **ArchiMate 3.2** (BMM·AMM·TMM 레이어) + **C4 Model**(Context·Container·Component·Code) + 클라우드 네이티브 MSA(12-factor app) + Event-Driven·Serverless |
| **⑤ IT 보안·리스크 관리 (IT Security & Risk Management)** | CIA(기밀성·무결성·가용성) + Parkerian Hexad + Resilience 확보 | **NIST CSF 2.0** (Govern-Identify-Protect-Detect-Respond-Recover 6함수), **ISO 27001:2022** (93통제), **ISMS-P**(국내 인증제 2024년 80개 인증원), **제로트러스트** (BeyondCorp·SASE·ZTNA), **CVE/CVSS 4.0**, **DevSecOps**(SAST·DAST·SCA), **PIPC 개인정보 영향평가·DPIA**, **AI 윤리(UNESCO Recommendation·EU AI Act 위험등급)** |
| **⑥ IT 조직·역량 관리 (IT Org & Capability Management)** | 인적자원·문화·역량·학습 조직 개발 | **SFIA 8**(Skills Framework for the Information Age, 6수준×137스킬) + **DMBOK 2.0** + **Prosci ADKAR**(Awareness-Desire-Knowledge-Ability-Reinforcement) 변화관리 + **KPI**(학습시간·CERT·Retention Rate) + Agile·DevOps·SRE·MLOps 직무 재정의 |

### 4대 추진 체계의 상호작용 메커니즘

```text
   ┌──────────────────────────────────────────────────────────┐
   │           PDCA + 4대 추진체계 동적 루프                    │
   │                                                          │
   │    [Plan: 전략-실행 연계]                                 │
   │      사업전략 → IT전략(3-5yr) → EA → PortFolio            │
   │         │                                                │
   │         ▼                                                │
   │    [Measure: 성과측정]                                    │
   │      BSC 4관점(Financial·Customer·Internal·L&G)         │
   │      Lagging 5개 + Leading 7개 KPI, North Star Metric    │
   │         │                                                │
   │         ▼                                                │
   │    [Act: 변화관리]                                        │
   │      ADKAR × 8-Step Kotter                              │
   │      Big-Bang vs Phased vs Parallel (의사결정 트리)        │
   │         │                                                │
   │         ▼                                                │
   │    [Do/Protect: 리스크관리]                                │
   │      Risk = f(Threat, Vulnerability, Impact, Likelihood)│
   │      Heat Map(5×5) → Treatment(4T: Terminate·Mitigate)  │
   │         │                                                │
   │         └──► 재 Plan (Annual+Quarterly Review)           │
   └──────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘·수식

1. **IT 투자 우선순위(WSJF)** = Cost of Delay(USD) ÷ Job Duration
   - CoD = User-Business Value + Time Criticality + Risk Reduction
2. **서비스 가용성(Availability)** = (MTBF / (MTBF + MTTR)) × 100
3. **단일손실예상값(SLE)** = Asset Value × Exposure Factor
   - **연간손실예상값(ALE)** = SLE × Annual Rate of Occurrence (ARO)
4. **ROI** = (Total Benefit - Total Cost) / Total Cost × 100
   - **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 642 / 800

← **이전**: [641. IT 경영 관리 핵심 토픽 641번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/641_it_management_core_topic_641_exam_summary/)
**다음**: [643. IT 경영 관리 핵심 토픽 643번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/643_it_management_core_topic_643_exam_summary/) →

---
