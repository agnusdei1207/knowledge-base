---
title: "608. IT 경영 관리 핵심 토픽 608번 시험 요약 (IT Management Core Topic 608 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019)는 기업 목표(EBM: Enterprise Goals)와 IT 목표(Alignment Goal)를 13개 구성요소의 캐스케이드 메커니즘으로 정렬하는 프레임워크이며, 디지털 전환(DT)은 이를 ESG·AI·Zero Trust·Data Mesh 기반으로 확장한 경영 패러다임 전환이다.
> 2. **가치**: COBIT 2019 적용 시 IT-비즈니스 정렬도 70%->92%(ISACA 2022 글로벌 벤치마크), DT 성공률 30%->67% 향상(McKinsey 2023), 사이버사고 평균 비용 USD 4.45M->USD 1.5M 절감(IBM Cost of Data Breach 2023).
> 3. **판단 포인트**: 중앙집중형(CoE) vs 분산형(Federated) 거버넌스 모델, Build vs Buy vs Compose 의사결정, CAPEX->OPEX 전환 시 TCO 3년/5년 회수 분석, 그리고 KPI로서 OKR·BSC·CSF의 혼용 시 인과관계 매핑 오류 방지.

---

## Ⅰ. 개요 및 필요성

제608회 정보관리기술사 시험은 4차 산업혁명 시대의 **IT-Business Alignment** 실패율(전통적 ERP 프로젝트 기준 70% 실패, Standish Group CHAOS Report 2020)을 배경으로, 단순 기술 지식을 넘어 **거버넌스·전략·리스크·컴플라이언스(GRC)** 통합 관점의 판단력을 평가한다. 최근 5개년 출제 트렌드는 ① IT 거버넌스 프레임워크(COBIT 2019, ITIL 4), ② 디지털 전환 로드맵, ③ 사이버보안 거버넌스(Zero Trust, NIST CSF 2.0), ④ 데이터 거버넌스(Data Mesh, DAMA-DMBOK), ⑤ ESG·지속가능성 IT, ⑥ AI 윤리·책임 있는 AI(Responsible AI), ⑦ 메타버스·Web3 전략, ⑧ 클라우드 경제성 파인옵스(FinOps)이다.

```text
+-----------------------------------------------------------------+
|        제608회 정보관리기술사 출제 트렌드 매트릭스(2020~2024)      |
+----------------+------------------------------------------------+
| 거버넌스축     |  COBIT2019 -+-> ISO/IEC 38500 (이사회 거버넌스)  |
|                |             +-> NIST CSF 2.0 (운영 거버넌스)    |
|                |                                                |
| 전략축         |  DT 3.0 -+-> BCG 5-Stage Maturity Model        |
|                |          +-> MIT CISR (Digital Maturity)        |
|                |          +-> BPR -> RPA -> Hyperautomation        |
|                |                                                |
| 데이터·AI축    |  Data Mesh -> DAMA-DMBOK 2.0 -> MLOps          |
|                |  LLM 거버넌스 -> RAG -> Responsible AI           |
|                |                                                |
| 보안·리스크축   |  Zero Trust -> SASE -> XDR -> SOAR             |
|                |  OT/IT 컨버전스 보안 -> NIS2, 공급망 SBOM         |
|                |                                                |
| 지속가능성축   |  Green IT -> ESG CSRD -> Scope3 배출량         |
|                |  탄소회계플랫폼 -> EU CBAM 대응                   |
+----------------+------------------------------------------------+
```

기존 패러다임인 "**프로젝트 중심 IT 투자**(Project-centric Capex, ROI 5년, 워터폴)"에서 "**제품 중심 지속적 가치 창출**(Product-centric Opex, ROI 분기 단위, 애자일·데브옵스)"로 전환이 필요하며, 이는 ISO/IEC 38500의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 4단계 거버넌스 모델(Evaluate-Direct-Monitor) 하에 구현해야 달성 가능하다. 또한 ESG 공시 의무화(EU CSRD 2024, 한국 ESG 공시 지침 2025) 및 AI 기본법(안) 시행에 따라, **IT가 비용 센터에서 가치·리스크·컴플라이언스 센터**로 재정의되어야 한다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 토지이용계획(Zoning)**과 같습니다. 마치 도시계획자가 주거·상업·공업지대를 지정하듯, COBIT은 40개의 거버넌스·관리 목적을 5개 도메인(EDM·APO·BAI·DSS·MEA)에 배정하여 IT 자원의 합리적 사용을 보장합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019의 핵심은 **Goals Cascade** 메커니즘이다. 13개 거버넌스·관리 구성요수가 40개 관리목적(Process Purpose)을 통해 28개 IT 관련 목표(Alignment Goals)를 달성하고, 이는 13개 기업 목표(Enterprise Goals)에 연결된다. 각 연결에는 우선순위(P: Primary)와 부차적(S: Secondary) 관계가 정의되어 있다.

```text
                    +----------------------------------+
                    |   Stakeholder Drivers(13대 니즈)   |
                    |  Benefits Realization|Risk Opt.|  |
                    |  Resource Opt.|Compliance        |
                    +----------------+-----------------+
                                     | (매핑)
                    +----------------v-----------------+
                    |  Enterprise Goals (13개)           |
                    |  EG01~EG13 (재무|고객|내부|학습)    |
                    +----------------+-----------------+
                                     | (P/S 매핑)
                    +----------------v-----------------+
                    |  Alignment Goals (28개)            |
                    |  AG01~AG28 (IT전략|거버넌스|앱등)  |
                    +----------------+-----------------+
                                     | (RACI 정의)
                    +----------------v-----------------+
                    |  Process Goals (40개 관리목적)      |
                    |  EDM×5 | APO×14 | BAI×11 | DSS×6  |
                    |  MEA×4                            |
                    +----------------+-----------------+
                                     | (Activity Metric)
                    +----------------v-----------------+
                    |  Management Practice (243개)       |
                    |  + 7개 컴포넌트(원리|정책|프레임)   |
                    +----------------------------------+
```

**핵심 동작 원리 7대 컴포넌트(C7S - Component 7 Simplified)**:
- ① 원리(Principles) · ② 정책(Policy) · ③ 프레임(Framework) · ④ 프로세스(Process) · ⑤ 조직구조(Org Structures) · ⑥ 정보흐름(Information Flow) · ⑦ 인적자원/역량/문화(People, Skills & Culture)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·IT거버넌스위원회 거버넌스 계층 | 5개 프로세스(EDM01~05)로 거버넌스 시스템의 운영을 감독. RACI 표에서 Accountable(A) 역할 집중. 5개 핵심 메트릭: Benefit Delivery %, Risk Management Index, Resource Optimization, Stakeholder Engagement, Value Creation |
| **APO (Align, Plan, Organize)** | 전략 정렬 및 계획 | APO01(관리프레임워크), APO04(혁신), APO05(포트폴리오), APO12(리스크관리), APO13(보안관리). COBIT 2019에서 NIST CSF 2.0의 6개 Function(Govern/Identify/Protect/Detect/Respond/Recover)과 1:1 매핑 |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축 및 변경 | BAI03(솔루션관리), BAI11(프로젝트관리) - PMBOK 7th 8개 성능영역과 통합. DevOps 파이프라인(GitOps, ArgoCD), IaC(Terraform, Pulumi)와 연계 |
| **DSS (Deliver, Service, Support)** | 운영 및 서비스 | DSS02(서비스요청/사고), DSS03(문제관리), DSS04(연속성), DSS05(보안운영). ITIL 4의 34개 Practice와 1:1 매핑 가능 (Service Value System) |
| **MEA (Monitor, Evaluate, Assess)** | 성능 측정 및 감사 | MEA01(성능/준수), MEA02(내부통제), MEA03(외부준수), MEA04(감사). KRI(핵심리스크지표)와 CSI(Continuous Service Improvement) 측정 |
| **Focus Area (집중영역)** | 사이버보안·DevOps·RPA·위험·컴플라이언스 등 | 30개 이상 사전정의. SME(Subject Matter Expert) 가이드로 산업별 적용. 예: COBIT 2019 Design Guide 6단계 (Identify Context->Refine Scope->Conclude Focus Areas->Focus Area Selection->Resolve Conflicts->Finalize Design) |
| **Components Variants & Design Factor** | 조직 맥락에 맞춘 거버넌 시스템 설계 | 11개 Design Factor(전략|목표|리스크|컴플리언스|위협|역할|정보기술|역량|조직규모|문화|보안). CMMI 2단계(Managed->Defined)로 시스템 성숙도 측정 |

**핵심 평가 메트릭 (예시: APO12 Risk Management)**:
- R1: **위험 식별 커버리지** = 식별된 위험 수 / 전체 자산 수 ≥ 95%
- R2: **잔여 리스크 허용치** = Σ(영향도×발생가능성) / 총 위험 × 허용치 ≤ 조직 한계치
- R3: **리스크 대응 SLA** = 계획된 완화조치 대비 기한 내 완료율 ≥ 90%
- 목표-메트릭-임계치의 SMARTER 원칙(Specific, Measurable, Achievable, Relevant, Time-bound, Evaluated, Reviewed)

- **📢 섹션 요약 비유**: COBIT의 7대 컴포넌트는 마치 **자동차의 7가지 계기판**과 같습니다. 속도계(성과), 연료게이지(자원), 경고등(리스크), 내비게이션(전략), 에어백(컴플라이언스), 핸들(원칙), 그리고 운전자(인적자원) 모두가 동시에 작동해야 안전한 주행이 가능합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **NIST CSF 2.0** | **PMBOK 7th** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 | IT 서비스 관리 | 이사회 IT 거버넌스 | 사이버보안 운영 | 프로젝트 관리 |
| **계층** | 전략-이사회 | 운영·전술 | 거버넌스 최상위 | 운영 보안 | 프로젝트 실행 |
| **핵심 구조** | 5도메인/40목적 | 34 Practice/SVS | 6원칙/5모델 | 6 Function/Category | 8 Performance/12 Principle |
| **대상** | CIO, 이사, 감사인 | 서비스 매니저, 운영자 | 이사회, CEO | CISO, 보안운영팀 | PMO, 프로젝트 매니저 |
| **측정 방식** | Maturity Level(0-5) + Capability Level(0-5) | KPI + 4D 모델 | 원칙 기반 평가 | TIER 1-4 구현도 | 성능영역 점수 |
| **연계** | NIST CSF 2.0, ITIL 4 매핑 가이드 | COBIT와 1:1 Practice 매핑 | ISO/IEC 27001, 20000 | COBIT APO/DSS 매핑 | COBIT BAI11 매핑 |
| **약점** | 구현 복잡도 높음 | 거버넌스 결여 | 평가 도구 부족 | 거버넌스 축 약함 | 애자일 친화도 낮음 |
| **라이선스** | ISACA (유료) | AXELOS (유료) | ISO (유료) | NIST (무료) | PMI (유료) |

**상호 연계 아키텍처 (Togaf ADM 8단계 매핑)**:

```text
+-------------------------------------------------------------+
|  Phase A: Architecture Vision  <-->  COBIT EDM01·02(거버넌체계)  |
|  Phase B: Business Architecture <--> COBIT APO01·02(전략정렬)    |
|  Phase C: Information Systems <--> COBIT BAI03·APO05           |
|  Phase D: Technology Architecture <--> COBIT BAI09·DSS01       |
|  Phase E: Opportunities & Solutions <--> COBIT BAI11(프로젝트) |
|  Phase F: Migration Planning <--> COBIT APO12·13(리스크/보안)   |
|  Phase G: Implementation Governance <--> COBIT BAI01~11        |
|  Phase H: Architecture Change Mgmt <--> COBIT MEA01·02         |
|  Requirements Mgmt: 중앙 허브로서 COBIT의 7 Component 활용      |
+-------------------------------------------------------------+
```

**디지털 전환(DT) 4축 프레임워크**:
1. **전략축**: BCG 5-Stage(Vigilant->Active->Engaged->Operational->Leader) -> MIT CISR 4D(Strategy->Structure->Culture->Technology)
2. **기술축**: 클라우드 네이티브(Kubernetes, Service Mesh) + AI/ML(AutoML, MLOps) + 데이터 플랫폼(Data Lakehouse, Iceberg)
3. **조직축**: Spotify 모델(Squad-Tribe-Chapter-Guild) + 거버넌스 CoE(Center of Excellence) vs Federated 모델
4. **운영축**: SRE(Google SRE Book) + FinOps(클라우드 비용 최적화) + GreenOps(탄소감축)

- **📢 섹션 요약 비유**: COBIT·ITIL·ISO 38500은 마치 **병원 시스템**의 서로 다른 층과 같습니다. ISO 38500이 이사진(원장), COBIT이 진료과장·전담의, ITIL이 간호사·의료진, NIST CSF가 감염관리실과 같은 역할을 분담합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **거버넌스 모델 선택**: 조직 규모(임직원 수)와 DT 성숙도에 따라 CoE(Center of Excellence, 임직원 1,000명v 권장), Hybrid(1,000~10,000명), Federated(10,000명^) 중 선택. RACI 매트릭스 작성 시 A(Accountable)는 단 1명, R(Responsible)은 2-5명, C(Consulted)는 5-15명, I(Informed)는 50명 이상으로 설계.
2. **TCO vs ROI 분석**: 5년 TCO 산출 시 라이선스(20-30%), 인프라(25-35%), 인건비(30-40%), 교육(5-10%), 기회비용(10-15%) 항목 구분. NPV 계산
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 608 / 800

<- **이전**: [607. IT 경영 관리 핵심 토픽 607번 시험 요약](/studynote/12_it_management/05_security_compliance/607_it_management_core_topic_607_exam_summary/)
**다음**: [609. IT 경영 관리 핵심 토픽 609번 시험 요약](/studynote/12_it_management/05_security_compliance/609_it_management_core_topic_609_exam_summary/) ->

---
