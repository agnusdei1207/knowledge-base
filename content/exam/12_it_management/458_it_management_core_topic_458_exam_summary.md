---
title: "IT Management Core Topic 458 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# IT 경영 관리 핵심 토픽 458번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance & Management)는 COBIT 2019, ITIL 4, TOGAF 10, PMBOK 7th, ISO 27001/ISMS-P, DAMA-DMBOK 2.0 등 글로벌 표준 프레임워크를 기반으로, **Value(가치창출) ↔ Risk(위험관리) ↔ Resource(자원 최적화)**의 3축 균형을 통해 기업의 디지털 전환(DX)과 지속가능한 경쟁우위를 달성하는 통합 거버넌스 체계이다.
> 2. **가치**: McKinsey 연구에 따르면 성숙한 IT 거버넌스 체계 도입 기업은 **프로젝트 성공률 35%^, TCO 20~30% 절감, ROI 2.4배 향상, 보안사고 60%v**의 정량 효과를 거두며, ESG/디지털 트랜스포메이션 시대의 핵심 경영 인프라로 부상한다.
> 3. **판단 포인트**: **"표준 채택(Framework Adoption) vs. 맞춤형 설계(Custom Design)", "중앙집중형(Centralized) vs. 분산형(Federated) 거버넌스", "규율 중심(Governance-First) vs. 가치 전달 중심(Value-First) 운영"** 사이의 트레이드오프를 사업 특성·규제 환경·조직 문화에 따라 의사결정해야 하며, 기술사답게 **'프레임워크 간 정합성 매핑(Mapping)'과 '성숙도 모델 기반 로드맵 수립'** 능력이 핵심 역량이다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Governance & Management)는 단순한 IT 운영을 넘어 **기업의 전략적 목표(SG)와 IT의 가치 실현(Value Realization)을 연결**하는 경영 과학이다. 정보관리기술사 시험에서 458번 대분류는 **"IT 거버넌스, IT 전략 기획, EA 구축, ISMS, 프로젝트 관리, 서비스 운영, 데이터 거버넌스"** 등 정보시스템의 Plan->Build->Run->Evaluate 전 생애주기를 아우르는 통합적 시각을 평가한다.

과거(2000년대 이전)에는 **"기술 중심(Tech-driven)"** 접근으로 인프라·애플리케이션을 개별 도입했으나, 2010년 이후 클라우드·모바일·빅데이터가 보편화되면서 **"거버넌스·컴플라이언스·비용 최적화"** 이슈가 폭증했다. 현재(2024~2026)는 **"AI 네이티브, 플랫폼 엔지니어링, ESG/지속가능 IT, 제로트러스트, 데이터 경제"** 패러다임으로 재편되면서, IT 경영은 CFO·CEO 직속 의사결정 안건으로 격상되었다.

```text
+------------------------------------------------------------------+
|         IT 경영 관리의 패러다임 전환 (As-Is -> To-Be)             |
+------------------------------------------------------------------+
|                                                                  |
|  [As-Is: 2000s]                [To-Be: 2024~2026]               |
|  +-----------------+           +--------------------------+     |
|  | • 기술중심 도입  |    ->->->    | • 가치·리스크 균형 거버넌스|     |
|  | • 실리콘벨리      |           | • AI-First 전략           |     |
|  |   종속 벤더관리  |    ->->->    | • 멀티클라우드/하이브리드   |     |
|  | • 개별 시스템    |    ->->->    | • 통합 EA + 데이터 거버넌스|     |
|  |   단위 투자      |           |   + 플랫폼 엔지니어링      |     |
|  | • 사후 컴플라이언스|   ->->->    | • 선제적 제로트러스트      |     |
|  | • CapEx 중심    |    ->->->    | • OpEx + Green IT        |     |
|  +-----------------+           +--------------------------+     |
|                                                                  |
|   [변동 촉매요인: Cloud, COVID-19, 생성형AI, 규제(GDPR/    ]    |
|   [       AI기본법, EU AI Act), ESG공시, 사이버 위협 고도화]    |
+------------------------------------------------------------------+
```

**왜 지금 IT 경영 관리가 필수적인가?**

1. **규제 환경 강화**: 개인정보보호법, ISMS-P, 클라우드 보안인증(CSAP), AI 기본법(2026 시행), EU AI Act, DORA(금융), ESG 공시 의무화 -> 컴플라이언스 비용이 IT 예산의 15~25% 차지
2. **기술 복잡도 폭증**: 평균 엔터프라이즈가 관리하는 SaaS 350개+ (Zscaler 2024 보고), 멀티클라우드 환경 -> Shadow IT 및 데이터 사일로 심화
3. **사이버 위협 고도화**: 랜섬웨어·공급망 공격(Supply Chain Attack)·제로데이 증가 -> 평균 사고복구비용 4.45M USD (IBM 2023)
4. **가치 실현 압박**: CFO·이사회가 "IT 투자 대비 ROI" 정량 증명 요구 -> FinOps·TBM(Tech Business Management) 부상

- **📢 섹션 요약 비유**: IT 경영 관리는 **"오케스트라의 지휘자"**와 같습니다. 바이올린(개발), 첼로(운영), 트럼펫(보안), 팀파니(인프라) 등 다양한 악기(시스템)가 각자 좋은 연주만 해서는 안 되고, **지휘자(거버넌스)**가 악보(프레임워크)대로 **조화(가치)**를 이루도록 해야 비로소 아름다운 음악(사업 성과)이 탄생합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"프레임워크 × 계층 × 생애주기"**의 3차원 매트릭스로 이해하는 것이다. 글로벌 표준 프레임워크들을 어느 계층(Strategy/Architecture/Implementation/Operation)에, 어떤 목적(거버넌스/관리)으로 적용할지를 정합적으로 매핑하는 것이 기술사의 핵심 역량이다.

```text
+-------------------------------------------------------------------------+
|       IT 경영 관리 3차원 통합 프레임워크 (3D Mapping Matrix)            |
+-------------------------------------------------------------------------+
|                                                                         |
|              [계층/Layer]                                               |
|                  ^                                                      |
|   Strategy      |   +--------------------------------------+            |
|   (전략)        |   | ISO 38500 | COBIT 2019 | Balanced   |            |
|   +----------+  |   |           | (EDM)      | Scorecard  |            |
|   | Board    |  |   +--------------------------------------+            |
|   | CIO/CDO  |  |   +--------------------------------------+            |
|   +----------+  |   | TOGAF 10 ADM | DoDAF | FEAF | Zachman|            |
|   Architecture  |   | (ADM 사이클: A->B->C->D->E->F->G->H)        |            |
|   (아키텍처)     |   +--------------------------------------+            |
|   +----------+  |   +--------------------------------------+            |
|   | EA팀/    |  |   | PMBOK 7th | PRINCE2 | ISO 21500      |            |
|   | SA/TA    |  |   | Agile: SAFe, LeSS, Scrum@Scale     |            |
|   +----------+  |   +--------------------------------------+            |
|   Implementation|   +--------------------------------------+            |
|   (구축)        |   | ITIL 4 (SVS: 34 Practices)         |            |
|   +----------+  |   | DevOps | SRE | GitOps | Platform Eng|            |
|   | Dev/QA/  |  |   +--------------------------------------+            |
|   | Ops      |  |   +--------------------------------------+            |
|   +----------+  |   | ISO 27001/ISMS-P | NIST CSF 2.0     |            |
|   Operation     |   | 제로트러스트 | DevSecOps            |            |
|   (운영/보안)    |   +--------------------------------------+            |
|   +----------+  |   +--------------------------------------+            |
|   | SOC/관제|  |   | DAMA-DMBOK 2.0 | DCAM | GDPR/PIPA   |            |
|   | DBA/보안 |  |   | 데이터 메시 | Data Fabric           |            |
|   +----------+  |   +--------------------------------------+            |
|                 v                                                       |
|                                                                         |
|   [생애주기/Lifecycle]:  Plan -> Design -> Build -> Deploy -> Operate ->     |
|                          Evaluate -> Improve  (Deming Cycle)            |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (Governance System)** | 의사결정 권한·책무·보고체계 정의 | COBIT 2019의 **EDM(평가·지휘·모니터)** 5개 도메인 + **연결 목표(Cascading Goals)** 13개 + **성숙도(0~5)** 모델. **RACI 매트릭스**로 역할 분배 |
| **전략 기획 (IT Strategy & Planning)** | 사업목표->IT 목표->이니셔티브->포트폴리오 변환 | **Balanced Scorecard 4관점**(Financial/Customer/Internal/Learning) + **Wardley Maps** + **Wardley/OODA 의사결정 루프** + **OKR** 정합 |
| **엔터프라이즈 아키텍처 (EA)** | 비즈니스·데이터·애플리케이션·기술 4계층의 청사진 | **TOGAF ADM 8단계**(Preliminary->A:Architecture Vision->B:Business->C:Information Systems->D:Technology->E:Opportunities&Solutions->F:Migration Planning->G:Implementation Governance->H:Architecture Change Management). **ArchiMate 3.2** 표기법 |
| **프로젝트/프로젝트군 관리 (PPM)** | 이니셔티브의 일정·범위·품질·리스크 관리 | **PMBOK 7th(12 Principle+8 Performance Domain)**, **PRINCE2(7 Principle, 7 Process)**, **SAFe 6.0**(Agile at Scale), Earned Value Management(EVM) |
| **서비스 운영 (ITSM)** | IT 서비스의 설계·전환·운영·개선 | **ITIL 4 Service Value System(SVS)**: 7 Guiding Principle + **34 Best Practice**(General/Service/Technical) + **Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support) |
| **정보 보안 관리** | CIA(기밀성·무결성·가용성) + 위험관리 | **ISMS-P(한국)**, **ISO 27001:2022(Annex A 93 통제항목)**, **NIST CSF 2.0(Gov/Identify/Protect/Detect/Respond/Recover)**, **제로트러스트(ZTA)**: NIST SP 800-207 5대 테넌시(Subject, Policy Engine, PEP, CDM, Industry Compliance) |
| **데이터 거버넌스** | 데이터의 가용성·품질·보안·수명주기 관리 | **DAMA-DMBOK 2.0(11 Knowledge Area)**, **DCAM 2.2**(Data Management Capability Assessment Model), **데이터 메시(Data Mesh)**: 도메인 자율 + 데이터 제품 + 셀프서비스 플랫폼 + 연방 거버넌스 |
| **FinOps / TBM** | IT 비용의 가시화·최적화·사업 정렬 | **FinOps Foundation 6단계 성숙도**, **Apptio/TBM Taxonomy**(Tower/Sub-tower), Showback/Chargeback, Unit Economics |
| **AI 거버넌스 (신규)** | AI 모델의 책임성·공정성·투명성·안전성 | **NIST AI RMF(2023)**, **ISO/IEC 42001(2023)**, **OECD AI 원칙**, **EU AI Act(2024)**, **한국 AI 기본법(2026.1 시행)** |
| **지속가능 IT (Green IT/ESG)** | 탄소배출 측정·감축·공시 | **GHG Protocol Scope 1/2/3**, **ISO 14064**, **GRI 305**, **SBTi**, **TCFD 4개 축(거버넌스/전략/리스크관리/지표)** |

**핵심 정합 매핑(Framework Interoperability)**:
- **COBIT 2019의 5 EDM 도메인 ↔ ITIL 4의 SVS ↔ ISO 27001의 Annex A**를 매핑하면 한 번의 통제 설계로 다중 인증(ISMS+ISO 27001+ISO 20000) 동시 취득 가능
- **TOGAF의 Preliminary Phase ↔ COBIT의 EDM01(Framework 설정)** 매핑으로 EA 거버넌스 위원회와 COBIT 이사회 보고체계 일원화
- **PMBOK 7th의 8 Performance Domain ↔ ITIL 4 Change Enablement Practice** -> 프로젝트 종료 시 서비스 전환(Service Transition) 자동 연계

**성숙도 모델(Maturity Model) 핵심 수치**:
- **COBIT 2019**: 0(Incomplete) ~ 5(Optimizing), Gap Analysis 결과로 Roadmap 도출
- **CMMI v2.0**: Level 1(Initial) ~ 5(Optimizing), 5개 Process Area(Plan/Do/Check/Manage) 20개 Practice Area
- **DCMM(中国数据管理能力成熟度, 국내 참고)**: 5단계(Initial->Managed->Defined->Quantitatively Managed->Optimizing)

- **📢 섹션 요약 비유**: 위의 3차원 매트릭스는 **"도시 계획법"**과 같습니다. 전략(상위계획)·아키텍처
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 458 / 800

<- **이전**: [457. IT 경영 관리 핵심 토픽 457번 시험 요약](/studynote/12_it_management/05_security_compliance/457_it_management_core_topic_457_exam_summary/)
**다음**: [459. IT 경영 관리 핵심 토픽 459번 시험 요약](/studynote/12_it_management/05_security_compliance/459_it_management_core_topic_459_exam_summary/) ->

---
