---
title: "IT Management Core Topic 652 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019 거버넌스 체계**(Governance & Management Objectives 40개)와 **ITIL 4 서비스 가치 시스템**(SVS)의 통합 적용을 통해, 정보화 투자 1조 원당 약 **3,200만 원의 가치 손실**(KPMG 글로벌 IT 손실 보고서 기준)을 방지하는 **정량적 의사결정 체계**임.
> 2. **가치**: BSC 4관점(재무/고객/내부프로세스/학습성장) 기반 KPI 측정 시 **정보화 사업 ROI 평균 287% 향상**(한국정보화진흥원 2023), ITIL 도입 기업 평균 **장애 대응 시간(MTTR) 62% 단축**, PMO 운영 시 프로젝트 성공률 **71% -> 89%**(PMI 2023 Pulse Report).
> 3. **판단 포인트**: **거버넌스(상위 의사결정) vs 관리(실행)**의 명확한 분리, **Agile-Waterfall 하이브리드 적용** 시 프로젝트 성격(신규/유지보수/규제)에 따른 프로세스 선택, **전사 아키텍처(EA) ↔ BPM ↔ IT 투자**의 3축 정렬(Alignment)이 핵심 트레이드오프.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management)는 **기업의 경영 전략과 IT 역량을 정렬(Strategic Alignment)** 시켜 **가치 창출(Value Creation)** 을 달성하는 통합 관리 체계입니다. 4차 산업혁명 시대를 맞아 단순한 시스템 운영을 넘어 **디지털 트랜스포메이션(DX)**, **AI 윤리**, **사이버 회복탄력성(Cyber Resilience)** 까지 포괄하는 광범위한 영역으로 확장되었습니다.

기존의 IT 관리는 **기술 중심(Tech-centric)** 으로 하드웨어/소프트웨어 도입에만 집중했으나, 현재는 **거버넌스-전략-포트폴리오-프로젝트-운영-성과** 로 이어지는 **전 라이프사이클 관리(End-to-End Lifecycle Management)** 가 요구됩니다. 특히 **2024년 과학기술정보통신부 정보화 사업 관리 지침** 개정으로 사업 착수 전 **EA(Enterprise Architecture) 적합성 검토** 의무화, **클라우드 전환 사업의 1단계 사업계획서(ISP) 작성 의무**, **데이터 거버넌스 체계 수립** 이 법제화되었습니다.

```text
+------------------------------------------------------------------+
|        IT 경영 관리 5대 영역 프레임워크 (ITGF v3.1)              |
|                                                                  |
|  +-------------+  +-------------+  +-------------+              |
|  | IT 거버넌스  |->|  IT 전략     |->| IT 포트폴리오|              |
|  | (COBIT 2019)|  |  기획(ISP)   |  |   관리(PPM)  |              |
|  +------+------+  +------+------+  +------+------+              |
|         |                |                |                      |
|         v                v                v                      |
|  +-----------------------------------------------------+         |
|  |        IT 투자 의사결정 위원회 (IT Steering)         |         |
|  |   CIO --- CDO --- CISO --- CFO --- CEO             |         |
|  +-----------------------------------------------------+         |
|         |                |                |                      |
|         v                v                v                      |
|  +-------------+  +-------------+  +-------------+              |
|  |  IT 프로젝트|->|  IT 운영     |->|  IT 성과     |              |
|  | 관리(PMO)   |  | (ITIL 4 SVS) |  | (BSC/KPI)    |              |
|  +-------------+  +-------------+  +-------------+              |
|                                                                  |
|  [피드백 루프] -- 성과의 정량 측정 -> 차기 전략 반영 --+         |
+------------------------------------------------------------------+
```

**왜 필요한가?**
- **공공부문**: 연간 정보화 예산 약 **8.5조 원**(2024 기준), 이 중 약 **23%가 사장(Sunk Cost)화** (감리원 통계). 거버넌스 부재 시 예산 낭비 구조화.
- **민간부문**: Gartner 2024 보고에 따르면, **CEO의 89%가 DX를 최우선 과제**로 인식하나, **DX 이니셔티브의 67%가 목표 미달성** (Gartner CIO Survey 2024). 거버넌스-전략-운영의 정렬 실패가 주원인.
- **규제 환경**: 개인정보보호법, 정보통신망법, 클라우드컴퓨팅법, AI기본법(2026 시행) 등으로 **컴플라이언스 비용** 증가 -> **내부 통제 체계**의 효율적 운영 필수.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 도시계획과 같습니다**. 건물(IT 시스템) 하나하나를 짓는 것(개발)이 아니라, 교통·상하수도·전력 인프라(거버넌스)를 어떻게 배치하고, 구역개발(전략)을 어떤 순서로 할지, 그리고 시민(사용자)에게 어떤 서비스를 제공할지(가치)를 통합 설계하는 것이 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **상위-중위-하위 3계층 의사결정 구조**와 **PDCA + DEMING(Plan-Do-Check-Act with 지식화) 사이클** 로 구성됩니다.

### 1. 상위계층: IT 거버넌스 (IT Governance)

**COBIT 2019** 의 **거버넌스 시스템 5개 도메인**(EDM: Evaluate, Direct, Monitor) 과 **관리 시스템 4개 도메인**(APO, BAI, DSS, MEA) 의 **40개 Governance & Management Objectives(GMO)** 가 표준 참조 모델입니다.

```text
+--------------------------------------------------------------------+
|              COBIT 2019 40개 목표 체계 (도메인별 분포)              |
|                                                                    |
|  +----------------------------------------------------------+      |
|  | 거버넌스 시스템 (Governance System) - 5개 도메인         |      |
|  |  EDM01 평가 (Ensured Governance Framework)              |      |
|  |  EDM02 지시 (Ensured Benefits Delivery)                 |      |
|  |  EDM03 모니터링 (Optimized Risk & Resource)             |      |
|  |  EDM04 투명성 (Ensured Resource Optimization)            |      |
|  |  EDM05 이해관계자 (Ensured Stakeholder Engagement)        |      |
|  +----------------------------------------------------------+      |
|                              <-> 정렬                                 |
|  +----------------------------------------------------------+      |
|  | 관리 시스템 (Management System) - 4개 도메인, 35개 목표 |      |
|  |                                                          |      |
|  |  APO (Align, Plan, Organize) - 14개 목표                 |      |
|  |   + APO01 관리 프레임워크    + APO08 관계 관리           |      |
|  |   + APO02 전략              + APO12 위험                |      |
|  |   + APO04 혁신              + APO13 보안                |      |
|  |   + ...                                                     |      |
|  |                                                          |      |
|  |  BAI (Build, Acquire, Implement) - 11개 목표              |      |
|  |   + BAI01 프로그램          + BAI11 변경 관리           |      |
|  |   + BAI03 투자 결정         + ...                        |      |
|  |   + ...                                                     |      |
|  |                                                          |      |
|  |  DSS (Deliver, Service, Support) - 6개 목표               |      |
|  |   + DSS01 운영              + DSS05 보안 운영           |      |
|  |   + DSS02 서비스 요청/사고  + DSS06 비즈니스 통제        |      |
|  |   + ...                                                     |      |
|  |                                                          |      |
|  |  MEA (Monitor, Evaluate, Assess) - 4개 목표                |      |
|  |   + MEA01 성과/준수 모니터  + MEA03 컴플라이언스         |      |
|  |   + MEA02 내부 통제                                          |      |
|  +----------------------------------------------------------+      |
|                                                                    |
|  [핵심 설계 요인: Focus Area (예: 사이버보안, DevOps, 위험)]        |
|              + Design Factors 11개 (조직 규모, 위협 환경 등)        |
+--------------------------------------------------------------------+
```

### 2. 중위계층: IT 전략 및 포트폴리오 관리

**정보화 전략 계획(ISP: Information Strategy Plan)** 은 **3-5년 중장기 로드맵**이며, **연간 사업계획(ISP-Annual)** 과 연결됩니다. 한국 정보화진흥원의 **e-정부 프레임워크** 와 **EA(Enterprise Architecture)** 가 핵심 도구입니다.

### 3. 하위계층: IT 운영 및 서비스 관리

**ITIL 4** 의 **Service Value System(SVS)** 은 7개 컴포넌트(기회, 가치, 수요, 가치사슬, 원리, 관행, 지속적 개선)로 구성되며, **34개 관리 실무(Service Management Practices)** 가 표준 참조 모델입니다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019** | IT 거버넌스 프레임워크 | 40개 GMO, **11개 Design Factor**(기업규모, 전략목표, 위험환경, 컴플라이언스, IT 역할, 정보기술 채택, IT 방법론, 기술 채택 전략, 규모 등)에 따라 **거버넌스 시스템 100% 맞춤 설계** |
| **ITIL 4 SVS** | IT 서비스 관리 (ITSM) | 7개 컴포넌트, **34개 실무(14개 일반, 17개 서비스, 3개 기술)**, 4가지 운영 모델(시스템, 프로세스, 사람, 공급자), **Value Stream** 단위 사고 |
| **PMBOK 7th** | 프로젝트 관리 표준 | 12개 원칙(Principles) + 8개 성과 영역(Performance Domains) + **Tailoring**(맞춤화) 중심, 기존 49개 프로세스 -> 원칙 기반 전환 |
| **BSC + KPI** | 전략/성과 측정 | 4관점(재무/고객/내부프로세스/학습성장), **Cascading(연결)**: 전사 KPI -> 부서 -> 개인 KPI, **SMART + DRIVE**(Differentiated, Relevant, Inexpensive, Visible, Exclusive) 검증 |
| **EA (전사아키텍처)** | IT-업무 정렬 | **Zachman Framework 6x6 매트릭스**(What/How/Where/Who/When/Why × Scope/Business/Logical/Physical/Detail/Enterprise), **TOGAF ADM(Architecture Development Method)** 8단계 사이클 |

### 4. 핵심 알고리즘 및 의사결정 공식

**① IT 투자 우선순위 결정 모델 (Weighted Scoring Model)**
```
우선순위 점수 = Σ (전략적연관성_i × 가중치_i) × ROI_i × 위험조정계수

가중치 예: 전략연관성 0.30, ROI 0.25, 위험도 0.20, 규제 0.15, 기술성숙도 0.10
위험조정계수 = (1 - 위험확률) × 영향도
```

**② COBIT 2019 Capability Level 측정 (ISO 15504 PAM)**
- **Level 0: Incomplete** -> **Level 1: Initial** -> **Level 2: Managed** -> **Level 3: Defined** -> **Level 4: Quantitative** -> **Level 5: Optimizing**
- 평가 기준: **Process Purpose(목적 달성)** + **Base Practice(기본 실무)** + **Work Product(산출물)** 3축

**③ BSC Balanced Scorecard 인과관계 모델**
```
학습성장(역량^) -> 내부프로세스(효율^) -> 고객가치(만족^) -> 재무성과(수익^)
   <-> 양방향 피드백 루프
```

- **📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **비행기의 자동조종장치(Autopilot)** 와 같습니다. COBIT은 항로(전략), ITIL은 엔진/연료(운영), PMBOK은 이륙절차(프로젝트), BSC/EA는 계기판(측정) 역할을 하며, 이 모두가 실시간으로 통합 작동해야 안전한 비행(경영 목표 달성)이 가능합니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 혼동하기 쉬운 핵심 프레임워크들을 명확히 비교합니다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 27001/27002** |
|:---|:---|:---|:---|:---|
| **주 목적** | 거버넌스 (Why/What) | 서비스 운영 (How) | 프로젝트 수행 (How) | 정보보안 통제 (What) |
| **대상 영역** | 전사 IT 의사결정 | IT 서비스 라이프사이클 | 단일 프로젝트 한정 | 정보보호관리체계(ISMS) |
| **핵심 산출물** | 40개 GMO, 11개 Design Factor | 34개 실무, SVS | 12 원칙, 8 성과영역 | 93개 통제 항목(Annex A 2022) |
| **주 사용자** | 이사회, CIO, CISO | 서비스 운영팀, 헬프데스크 | PMO, 프로젝트 매니저 | 보안담당자, CISO |
| **측정 방식** | Capability Level 0-5, Maturity | Value Stream 효율성 | 성과영역 성숙도 | Statement of Applicability (SoA) |
| **상호보완** | 거버넌스 상위체계 | COBIT BAI/DSS 도메인 적용 | COBIT BAI02/03 활용 | COBIT DSS05/APO13 매핑 |
| **갱신 주기** | 2019(현행), 2024 update | 2019(현행), 2024 update | 2021(7th), 2025 예정 | 2022(개정본) |

### 다른 시스템/도구와의 연결

1. **EA (전사아키텍처) ↔ IT 투자**: EA 기반 **Application Portfolio Analysis(APA)** -> 중복/노후 시스템 식별 -> **투자 우선순위** 도출. 한국 정보화진흥원의 **EA 수립 가이드**(2024) 기준 **BA(BA: Baseline Architecture) -> TA(Target Architecture) -> Gap Analysis -> 이행계획** 4단계.
2. **BPM (Business Process Management) ↔ BSC**: 프로세스 마이닝(Mined Process Map) -> KPI 자동 산출 -> BSC 내부프로세스 관점 정량화.
3. **GRC (Governance, Risk, Compliance) 통합**: **SAP GRC, ServiceNow GRC, Archer** 등 도구로 **3대 영역 단일 뷰** 제공. 특히 **Three Lines of Defense Model**(1st: 운영, 2nd: 위험/컴플라이언스, 3rd: 내부감사) 적용 시 핵심.
4. **Agile/DevOps ↔ PMO**: **SAFe(Scaled Agile Framework) 6.0**, **LeSS**, **Spotify Model** 등으로 프로젝트 단위 -> 프로그램/포트폴리오 단위 확대. **Spotify Squad/Tribe/Guild/Chapter** 모델.
5. **AI/ML 기반 의사결정**: **AIOps** (예: Splunk, Datadog)로 **장애 예측**, **자동 우선순위 분류**(NLP 기반 Incident Categorization), **강화학습(RL) 기반 자원 할
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 652 / 800

<- **이전**: [651. IT 경영 관리 핵심 토픽 651번 시험 요약](/studynote/12_it_management/05_security_compliance/651_it_management_core_topic_651_exam_summary/)
**다음**: [653. IT 경영 관리 핵심 토픽 653번 시험 요약](/studynote/12_it_management/05_security_compliance/653_it_management_core_topic_653_exam_summary/) ->

---
