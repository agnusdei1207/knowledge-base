---
title: "IT Management Core Topic 713 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019, ITIL 4)와 성과관리(BSC, KPI, KPI Tree)를 통합한 경영-IT 정렬(Strategic Alignment) 체계이며, 투자 대비 가치(VoI/ROI) 측정을 통해 IT 자산을 기업 수익·리스크·준법성(GRC) 관점에서 자본적 의사결정으로 전환하는 메커니즘이다.
> 2. **가치**: McKinsey(2023) 조사에서成熟한 IT 거버넌스 도입 기업은 IT 투자 효율 23~35% 개선, 중복 프로젝트 40% 감소, 디지털 전환 성공률 2.4배 향상을 달성하며, ISO/IEC 38500 및 14개 통제 목표(COBIT 2019) 기반의 컴플라이언스 자동화로 연간 5~8억 원 감사비용 절감이 가능하다.
> 3. **판단 포인트**: 중앙집중형(CoE) vs 분산형(Federated) 거버넌스 모델 선택, BSC 4관점 재무/고객/내부프로세스/학습성장 간 KPI 인과지도(Causal Map) 설계, 그리고 IT 포트폴리오의 Run/Grow/Transform 배분 비율(통상 70:20:10 또는 60:30:10)이 의사결정의 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 역할이 단순 지원(Support) 기능에서 전략적 경쟁우위(Strategic Differentiator)로 전환되면서, IT 투자의 **정당성(Justification)**, **측정 가능성(Measurability)**, **지속 가능성(Sustainability)** 을 입증해야 하는 요구가 폭증하였다. 전통적 CFO 관점의 TCO(Total Cost of Ownership) 중심 의사결정은 2010년 이후 디지털 전환·클라우드·AI 도입으로 한계를 드러냈으며, **"IT는 비용이 아니라 가치(Value)"** 라는 패러다임이 COBIT 2019, ITIL 4, ISO/IEC 38500 등의 글로벌 표준을 통해 제도화되었다.

특히 한국 환경에서는 정보시스템 감리(국가정보화법 제46조), 개인정보 보호법, 클라우드컴퓨팅법, AI 기본법(2026 시행) 등 다층적 규제 환경 하에서 **거버넌스-리스크-컴플라이언스(GRC) 통합 관리**가 필수이며, 공공부문은 DGB(디지털정부법), 민간은 ESG 공시 의무화에 따라 IT 거버넌스 성숙도가 곧 기업 신용등급에 영향을 미치는 변수가 되었다.

```text
   [ 정보화 전략 수립 4단계 - ISD(Information Strategy Discovery) ]
   +------------------------------------------------------------+
   |  Phase 1   Phase 2    Phase 3    Phase 4                  |
   |  현황분석  ->  SWOT   ->  목표설정  ->  실행계획             |
   |  (As-Is)     분석      (To-Be)     (Roadmap)              |
   |    |           |          |           |                    |
   |    v           v          v           v                    |
   |  BPA        5-Forces   BSC KPI    우선순위화               |
   |  Value Chain 경쟁분석    Tree 구축  AHP/ROI                |
   |  BPI         CSF 도출    RACI 정의  Quick-Win/MoE           |
   +------------------------------------------------------------+
                                |
                                v
   +------------------------------------------------------------+
   |          IT 거버넌스 통합 프레임워크 (상위레벨)            |
   |  +----------+   +----------+   +----------+   +---------+ |
   |  | 전략정렬 | ↔ | 가치제공 | ↔ | 리스크관 | ↔ | 성과측정| |
   |  |Align     |   |Delivery  |   |리Risk Mgmt|   |Measure | |
   |  +----------+   +----------+   +----------+   +---------+ |
   |         ^ COBIT 2019 40 Governance & Management Obj. ^   |
   +------------------------------------------------------------+
```

**기존 vs 새로운 패러다임**

- **AS-IS (1990~2010)**: IT 비용 = CAPEX(자본) + OPEX(운영), ROI = 단순 재무적 회수기간, CIO는 COE(Center of Excellence)에 위치, "IT는 비용절감 대상"
- **TO-BE (2015~현재)**: IT 비용 = TBM(Technology Business Management) 분류, 가치 = 재무+전략+비재무(Net Promoter Score, 직원만족도), CIO는 CDO/CAIO와 함께 C-Level 의사결정 참여, "IT는 비즈니스 임베디드 자산"

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **항공기의 비행관리시스템(FMS)** 과 같다. 기장(CIO)이 자동조종장치(거버넌스 프레임워크)를 통해 항로(전략)·고도(예산)·연료(ROI)를 실시간 모니터링하며, 관제탑(이사회)·지상정비사(감리인)·탑승객(이해관계자) 모두가 같은 계기판(BSC 대시보드)으로 비행 상태를 공유하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 3대 핵심 메커니즘은 ① **전략정렬(Strategic Alignment)** ② **가치지향관리(Value-Driven Management)** ③ **위험-통제-성능 균형(GRC-Performance Triangle)** 이다.

```text
   +--------------------------------------------------------------+
   |         IT 성과관리 아키텍처 5계층 모델 (PDCA + BSC)         |
   |                                                              |
   |  Layer 5  +--------------------------------------------+    |
   |  의사결정 |  경영진 / 이사회                             |    |
   |  (Decide) |  + CIO 보고 -- BSC Dashboard (Real-time)   |    |
   |           |  + IT Strategy Committee (월 1회)          |    |
   |           |  + Risk Committee (격주)                   |    |
   |           +--------------------------------------------+    |
   |                          ^                                   |
   |  Layer 4  +--------------------------------------------+    |
   |  분석/보고|  BI/Analytics (Tableau, Power BI, Looker)  |    |
   |  (Report) |  + EA Repository (ArchiMate, LeanIX)       |    |
   |           |  + ITFM (Apptio, SAP ITPM)                 |    |
   |           +--------------------------------------------+    |
   |                          ^                                   |
   |  Layer 3  +--------------------------------------------+    |
   |  측정/계량|  KPI Tree --- IT Scorecard (BSC 4 View)    |    |
   |  (Measure)|  + 재무    : TCO, ROI, EVA-S, Cost/Trans  |    |
   |           |  + 고객    : NPS, SLA 준수율, 만족도        |    |
   |           |  + 프로세스: 가용성 99.95%, MTTR, 변경성공률|    |
   |           |  + 학습성장: 역량 Index, 인증률, 이직률     |    |
   |           +--------------------------------------------+    |
   |                          ^                                   |
   |  Layer 2  +--------------------------------------------+    |
   |  통제/감사|  Control Objectives (COBIT 2019: 40개)     |    |
   |  (Control)|  + ISO 27001 (114 통제) + ITIL4 (34 Practice)|    |
   |           |  + Internal Audit + External 감리          |    |
   |           +--------------------------------------------+    |
   |                          ^                                   |
   |  Layer 1  +--------------------------------------------+    |
   |  운영/실행|  ITSM (ServiceNow, BMC Helix)              |    |
   |  (Operate)|  + DevOps (GitLab, Jenkins)                |    |
   |           |  + FinOps (Cloudability, Vantage)          |    |
   |           +--------------------------------------------+    |
   +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략정렬 (Strategic Alignment)** | 비즈니스 전략과 IT 로드맵의 양방향 매핑 | Henderson & Venkatraman SAMM(Strategic Alignment Maturity Model) 4단계(Initial->Committed->Established->Improved) 측정, EA(Enterprise Architecture) 기반 Business Capability ↔ Application ↔ Technology 3-Layer 매핑 |
| **BSC + KPI Tree** | 재무/고객/내부프로세스/학습성장 4관점 균형 성과측정 | Kaplan & Norton BSC 프레임워크, Strategic Map(Causal Map) 작성법, SMART KPI + Lag/Lead Indicator 조합, 1개 CSF당 2~4개 KPI 배정 (Nielsen Norman Group 5±2 법칙) |
| **COBIT 2019** | 40개 거버넌스·관리 목표를 통해 IT 활동 통제 | EDM(5개), APO(14개), BAI(11개), DSS(6개), MEA(4개) 5도메인 구조, Design Factors(11개)로 조직별 맞춤 설계, RACI Chart 필수 |
| **IT 투자 포트폴리오 (ITPF)** | Run(현업운영) / Grow(역량확장) / Transform(혁신) 비율 최적화 | Garner 70:20:10 원칙(현업 중심), McKinsey 60:30:10(혁신 강화형), Stage-Gate 펀딩 모델(Discovery->Pilot->Scale), Pipeline 가시화(Apptio, ServiceNow SPM) |
| **VoI/ROI 분석 모델** | 재무적·비재무적 가치 종합 산출 | 정량 ROI = (비용절감 + 수익증가) / 총투자비, 정성 VoI = 무형가치(브랜드, 민첩성) ± 리스크 조정, Gartner TBM(Technology Business Management) 4-Layer Cost Model |

**핵심 측정식 및 정량 지표**

- **ROI (%)** = ((편익 − 비용) / 비용) × 100, 통상 IT 프로젝트 3년 Payback 18~24개월 이내 적격
- **NPV (순현재가치)** = Σ[CFₜ / (1+r)ᵗ] − 초기투자, 할인율 r = WACC + Risk Premium(보통 8~12%)
- **TCO** = 직접비용(HW, SW, 인건비) + 간접비용(다운타임, 교육, 기회비용), 클라우드 전환 시 TCO 3년 35% 절감 가능(Forrester 2022)
- **EVA-S (Economic Value Added - Strategic)** = NOPAT − (WACC × 투하자본), IT 사업부가 EVA 창출 단위인지 판별
- **AHP (Analytic Hierarchy Process)** 일관성비율 CR ≤ 0.1, 다기준 IT 우선순위 의사결정
- **가용성(%)** = (총 운영시간 − 장애시간) / 총 운영시간 × 100, Tier IV 데이터센터 = 99.995% (연 26.3분 장애 허용)
- **MTTR (Mean Time To Repair)** = Σ(장애복구시간) / 장애건수, 목표 ≤ 30분(P1 기준)
- **MTTD (Mean Time To Detect)** = Σ(탐지시간) / 사고건수, AIOps 도입 시 평균 70% 단축

- **📢 섹션 요약 비유**: KPI Tree는 **가계부와 건강검진의 하이브리드** 와 같다. BSC 재무관점은 "월급·지출·저축"을, 고객관점은 "가족·친구 만족도"를, 내부프로세스는 "집·차·가전 관리 상태"를, 학습성장은 "운동·독서·자격증 습득"을 추적한다. 단순히 "돈 잔고"만 보던 가계부가 4차원 건강지표까지 통합한 셈이다.

---

## Ⅲ. 비교 및 연결

IT 경영관리의 주요 프레임워크 간 비교 및 실무 상호운용성

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **CMMI / SPICE** | **TBM (Gartner)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통제 | IT 서비스 운영·생태계 | 이사회 수준 IT 의사결정 원칙 | SW/조직 프로세스 성숙도 | IT 비용·가치 투명성 |
| **관점** | 거버넌스+관리 통합 | Service Value System (SVS) | 6대 원칙(책임·전략·수행·규율·투명성·적합성) | 5~6단계 성숙도 레벨 | 비용 분류(4-Layer) |
| **구조** | 5도메인 40목표 | 34 Practice, 4차원 모델 | 원칙+모델 | 22개 Process Area | Towers, Services, Solutions, Layers |
| **적용범위** | 전체 IT 거버넌스 | 운영·서비스 중심 | 이사회·경영진 의사결정 | SW 개발·운영 프로세스 | 재무·예산·회계 |
| **상호운용** | ITIL·TOGAF·ISO27001 매핑 공식 지원 | COBIT 2019 Practice 매핑 26개 | COBIT/ISO 27001/20000 가이드 | COBIT EDM/MEA 연계 | COBIT APO/MEA 활용 |
| **인증/감사** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/Master | ISO 38500 인증은 원칙적 | CMMI 2.0(2018~), ISO 33001 SPICE | 비공인, 내부 활용 |
| **강점** | Risk·Control·Compliance 명확 | Agile/DevOps 친화, 고객가치(Value) 강조 | 국제표준 법적 효력 | 정량 측정·벤치마킹 가능 | CFO/CIO 가시 언어 통일 |
| **약점** | 운영 깊이 부족, 다소 무거움 | 거버넌스 측면 약함 | 모호성, 측정 도구 부족 | 적용 범위 제한적 | 국내 도입 사례 적음 |
| **한국 도입률** | 공공 90%, 대기업 60% | 통신·금융 70% | 표준 기반 의무 참조 | SW사업법·감리 연계 | 컨설팅 단계 |

**연계 시스템 및 통합 패턴**

- **EA(Enterprise Architecture) 연동**: TOGAF ADM Phase E(기회)와 Phase F(마이그레이션 계획)에 COBIT APO12(리스크관리), APO04(혁신) 매핑
- **감리 통합**: 국가정보화법 감리 영역(사업관리 30%, 시스템구축 30%, 운영 20%, 성능/보안 20%)을 COBIT 5대 도메인과 1:1 대응시켜 중복감사 제거
- **ESG/지속가능성**: ISO/IEC 38500 + GRI Standards + SASB IT Sector 가이드라인 통합으로 IT 탄소배출(Scope 1·2·3) 측정
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 713 / 800

<- **이전**: [712. IT 경영 관리 핵심 토픽 712번 시험 요약](/studynote/12_it_management/05_security_compliance/712_it_management_core_topic_712_exam_summary/)
**다음**: [714. IT 경영 관리 핵심 토픽 714번 시험 요약](/studynote/12_it_management/05_security_compliance/714_it_management_core_topic_714_exam_summary/) ->

---
