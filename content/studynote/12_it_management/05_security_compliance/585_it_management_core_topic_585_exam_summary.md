---
title: "585. IT 경영 관리 핵심 토픽 585번 시험 요약 (IT Management Core Topic 585 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사 585번은 **디지털 전환(DX) 시대의 IT 전략·거버넌스·포트폴리오 관리(EA·BPR·ISP·BSC)**를 통합한 **"IT-Business Alignment"** 최적화 문제로, PMBOK·COBIT·ITIL·TOGAF·ISO 38500 프레임워크를 한 축으로 융합하여 평가하는 종합사례형 출제 경향을 보인다.
> 2. **가치**: 단순 암기형이 아닌, **CSF/KPI 기반 정량 ROI(예: 3년 내 TCO 25% 절감, Time-to-Market 40% 단축, OPEX/CAPEX 비율 60:40 재편)** 도출 능력과, **기존 레거시 시스템(예: 메인프레임 -> 마이크로서비스) 전환 시 ROI 312%** 같은 비즈니스 임팩트 산출이 합격 결정의 핵심이다.
> 3. **판단 포인트**: ① **In-house 구축 vs SaaS/PaaS 도입**의 Build-vs-Buy 의사결정, ② **클라우드 네이티브(MSA+컨테이너) vs 레거시 모놀리식**의 기술부채 상환 trade-off, ③ **Zero Trust vs 경계보안**의 보안 거버넌스 전환, ④ **Agile vs Plan-Driven** 조직문화 균형, ⑤ **국내 ISP/EA 표준(EA-Framework v3.0) vs 글로벌 TOGAF ADM** 적용 범위 — 이 5축의 다차원적 의사결정 트리 구현이 답안 차별화 포인트다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI·빅데이터·IoT·클라우드·블록체인) 가속화에 따라, 정보관리기술사 출제위원단은 **단순 기술 지식(Technology)**을 넘어 **경영 관점(Strategy)·프로세스 관점(Process)·인적 자원 관점(People)**을 통합한 **"IT 경영 거버넌스"**를 핵심 평가축으로 설정하고 있다. 특히 585번 계열 출제에서는 **"하향식 전략(CSF) -> KPI -> IT 투자우선순위 -> EA 기반 이행 -> 운영 최적화 -> 성과측정(BSC)"**의 전 과정을 하나의 사례로 통합 요구하는 경향이 강해, 프레임워크별 단편적 지식만으로는 합격이 불가능하다.

기존의 **"데이터 중심(Data-Driven) IT 운영"** 패러다임은 ① 정형데이터만 분석, ② 사후(After-the-fact) 보고, ③ 부서별 사일로(Silo) 시스템, ④ CAPEX 중심 HW 투자 — 라는 한계를 가졌다. 반면 **"DX 기반 지능형 IT 경영"**은 ① 비정형·실시간 데이터(스트리밍), ② 예측·시뮬레이션 기반 의사결정(Digital Twin), ③ 엔터프라이즈 통합 EA, ④ OPEX 중심 Cloud·Subscription 모델로 전환되었다.

```text
[기존 패러다임 vs DX 패러다임 비교 구조도]

   [Legacy IT 경영]                              [DX 기반 IT 경영]
   +------------------+                    +------------------+
   | ERP (SAP R/3)    |                    | S/4HANA Cloud    |
   | On-Premise DB    |                    | Data Lakehouse   |
   | SOAP/XML         |   ----DX 전환--->  | REST/GraphQL     |
   | 연 1회 계획      |                    | 실시간 의사결정   |
   | CFO 단독 의사결정 |                    | CDO+CTO+CIO 협의체|
   +------------------+                    +------------------+
            |                                          |
            v                                          v
   TCO 증가, 시장 대응 지연              ROI 극대화, 고객가치 창출
   (Time-to-Market 18개월)              (Time-to-Market 6개월)
```

- **📢 섹션 요약 비유**: 기존 IT 경영이 **"자동차 계기판만 보며 운전"**하는 것이라면, DX 기반 IT 경영은 **"네비게이션 + ADAS + 자동주행"**까지 통합한 미래차에 비유할 수 있다. 단순 현재 상태 확인이 아니라, **예측·제안·자동화**까지 수행하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

585번 IT 경영 관리의 아키텍처는 크게 **4계층(Strategy / Governance / Execution / Operation)**으로 구성되며, 각 계층은 **TOGAF ADM, COBIT 2019, ITIL 4, PMBOK 7th, BSC 4관점** 프레임워크의 **Best Practice가 매핑**된다.

```text
[IT 경영 관리 4계층 통합 아키텍처]

   +--------------------------------------------------------------+
   | Tier 1. 전략 정렬 계층 (Strategy Alignment)                  |
   |  +--------------+   +--------------+   +--------------+     |
   |  |ISP(정보전략) | -> |EA(아키텍처)  | -> |IT-PMO 거버넌스|    |
   |  |CSF 도출      |   |TOGAF ADM     |   |의사결정위원회 |     |
   |  +--------------+   +--------------+   +--------------+     |
   +--------------------------------------------------------------+
                              v KPI/CSF 계량화
   +--------------------------------------------------------------+
   | Tier 2. 거버넌스·컴플라이언스 계층 (Governance)               |
   |  +--------------+   +--------------+   +--------------+     |
   |  |COBIT 2019    |   |ISO 38500     |   |내부통제/감사 |     |
   |  |40 Governance |   |IT 거버넌스 원칙|  |ISMS-P / PIPC |     |
   |  |Objectives    |   |(책임·전략·집행)|  |컴플라이언스   |     |
   |  +--------------+   +--------------+   +--------------+     |
   +--------------------------------------------------------------+
                              v 프로세스/표준화
   +--------------------------------------------------------------+
   | Tier 3. 실행·전환 계층 (Execution & Transformation)           |
   |  +--------------+   +--------------+   +--------------+     |
   |  |BPR/RPA       | -> |Agile/DevOps  | -> |Cloud Migration|    |
   |  |프로세스 혁신  |   |SAFe/Scrum    |   |Lift&Shift->Refactor|  |
   |  +--------------+   +--------------+   +--------------+     |
   +--------------------------------------------------------------+
                              v SLA/OLA 가용성
   +--------------------------------------------------------------+
   | Tier 4. 운영·성과측정 계층 (Operation & Performance)          |
   |  +--------------+   +--------------+   +--------------+     |
   |  |ITIL 4        |   |BSC 4관점     |   |FinOps/Cost Opt|    |
   |  |서비스 가치사슬|   |재무·고객·프로 |   |클라우드 비용 |     |
   |  |(SVC)         |   |세스·학습성장  |   |최적화        |     |
   |  +--------------+   +--------------+   +--------------+     |
   +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISP (정보화 전략계획)** | 3~5년 중장기 IT 로드맵 수립 | MECE 분석(McKinsey 7S, Porter 5 Forces) -> CSF 5~7개 도출 -> KPI 트리(Tree) -> 투자우선순위(AHP 분석) |
| **EA (Enterprise Architecture)** | 업무·데이터·응용·기술 4계층 표준화 | TOGAF ADM 8단계(Preliminary->Architecture Vision->Business/IS/Technology Architecture->Opportunities->Migration Planning->Implementation Governance->Change Management) 순환 적용 |
| **COBIT 2019** | IT 거버넌스·관리 목표 체계 | 40개 Governance/Management Objectives, 5개 도메인(EDM/APO/BAI/DSS/MEA) + 11개 디자인 팩터(Strategy, Risk, Compliance 등) |
| **ITIL 4 / SVS** | IT 서비스 운영·지속적 개선 | 34개 서비스 관행(Incident, Problem, Change, Service Desk), **Service Value System(SVS)**: Opportunity/Demand->Value->Guiding Principles->Governance->Practices->Continual Improvement |
| **PMBOK 7th** | 프로젝트 통합·애자일/예측 혼합 | 12 Principle + 8 Performance Domain(Stakeholder, Team, Development Approach, Planning, Work, Delivery, Measurement, Uncertainty) — **Adaptive(Agile)/Predictive(Waterfall)/Hybrid** 3방식 |

**핵심 알고리즘·산식 정리:**

1. **TCO(Total Cost of Ownership) = HW비용 + SW라이선스 + 인력(인건비×FTE×기간) + 운영(OpEx) + 폐기비용 - 잔존가치**. 5년 TCO 산출 시 HW:SW:Service = 30:30:40 비율이 일반적이다.
2. **ROI 산출: (총편익 - 총비용) / 총비용 × 100**. BPR 시 **Payback Period = 투자액 / 연절감액**이 핵심 임계치(통상 3년 이내 합격).
3. **NPV(순현재가치) = Σ(CF_t / (1+r)^t) - 초기투자**. 할인율 r은 한국은행 기준금리 + Risk Premium 5~8% 적용.
4. **BSC 4관점 가중치**: 재무 25% + 고객 25% + 내부프로세스 30% + 학습성장 20% (통상적 비율, 업종별 조정).

- **📢 섹션 요약 비유**: 4계층 아키텍처는 **"의료 시스템"**에 비유할 수 있다. Tier 1은 **진단(Strategy)**, Tier 2는 **의사결정·처방전(Governance)**, Tier 3은 **수술·치료(Execution)**, Tier 4는 **회복·재활·건강검진(Operation)**이다. 환자(기업) 상태에 따라 4계층이 순환·반복되어야 한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리에서 자주 혼동되는 **ISP vs EA vs BPR**, 그리고 **COBIT vs ITIL vs ISO 38500**의 명확한 비교는 답안의 논리적 일관성을 좌우한다.

| 구분 | ISP(정보화 전략계획) | EA(전사아키텍처) | BPR(업무재설계) | 프로젝트 관리(PM) |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | 중장기 IT 투자방향 수립 | 업무-시스템-기술 표준화 | 업무 프로세스 근본적 재설계 | 일정·품질·비용·리스크 통제 |
| **시점·주기** | 3~5년, 1회/년 갱신 | 5~10년, ADM 순환 | 프로젝트 단발성 (6~18개월) | 프로젝트 단위 (3~24개월) |
| **산출물** | 전략맵, KPI, 로드맵 | BA/DA/AA/TA 4개 매트릭스 | AS-IS/TO-BE 프로세스 맵, SOP | WBS, Gantt, Risk Register |
| **주도 부서** | CIO실·전략기획 | EA 전담조직(CIO 직속) | 현업 + BPR 추진 TF | 각 BU PMO |
| **연계 프레임워크** | Porter, McKinsey 7S, Value Chain | TOGAF, DoDAF, FEAF | BPMN 2.0, Six Sigma, Lean | PMBOK, PRINCE2, ISO 21500 |
| **시너지 효과** | EA 방향 제시 | ISP 구체화·실현 | IT 시스템 요구사항 도출 | ISP/EA 이행 실행 |

**프레임워크 간 통합 매핑:**

- **COBIT 2019 ⇄ ITIL 4**: COBIT의 "DSS(Delivery, Service, Support) 도메인"은 ITIL의 Service Operation과 1:1 매핑, COBIT의 EDM(EDM01~05) 5개 목표는 ITIL의 Governance 활동과 직접 연결.
- **TOGAF ADM Phase E~F**: PMBOK 7th의 "Delivery, Measurement Performance Domain"과 1:1 매핑, TOGAF Migration Plan은 PM WBS의 상위 구조로 활용.
- **ISO 38500 6원칙(Evaluate, Direct, Monitor)**: COBIT EDM 도메인의 거버넌스 평가·지휘·감시 구조와 동일.

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 | PMBOK 7th |
| :--- | :--- | :--- | :--- | :--- |
| **스코프** | IT 거버넌스·관리 전 영역 | IT 서비스 운영·개선 | IT 의사결정 거버넌스 원칙 | 단위 프로젝트 관리 |
| **관리 대상** | 40개 Goal + 5도메인 | 34개 Practice + SVC | 6개 원칙 + 모델 | 12 원칙 + 8 도메인 |
| **성숙도 모델** | CMMI 5단계 (0~5) | ITIL Maturity Model | 자체 평가 체크리스트 | OPM3 4단계 |
| **인증** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | 비공인(자율준수) | PMP, CAPM, PMI-ACP |
| **도입 우선순위** | 거버넌스 수립 시 1순위 | 운영 표준화 시 1순위 | 글로벌 기업 거버넌스 | 프로젝트 단위 즉시 |

- **📢 섹션 요약 비유**: 4대 프레임워크는 **"오케스트라의 악기"**에 비유할 수 있다. **COBIT은 지휘자(Conductor)**, **ITIL은 첼리스트(서비스 운영)**, **ISO 38500은 작곡가(원칙)**, **PMBOK은 타악주(실행·통제)**다. 단일 악기만으로는 완전한 음악이 불가능하며, **하모니(통합)**가 핵심이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 IT 경영 관리 체계 도입 시, 기술사 수준의 의사결정 트리(Decision Tree) 구현이 필요하다. 가장 빈번한 시나리오 3가지를 제시한다.

**시나리오 1: 레거시 ERP(예: SAP ECC 6.0) -> S/4HANA 전환**
- **마이그레이션 전략**: Brownfield(선택적 이관, 12~18개월, 리스크 낮음) vs Greenfield(완전 재설계, 24~36개월, TCO 40% 절감 가능)
- **판단 기준**: ① 커스터마이징 비중(Z-Code 30% 이상이면 Brownfield 유리),
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 585 / 800

<- **이전**: [584. IT 경영 관리 핵심 토픽 584번 시험 요약](/studynote/12_it_management/05_security_compliance/584_it_management_core_topic_584_exam_summary/)
**다음**: [586. IT 경영 관리 핵심 토픽 586번 시험 요약](/studynote/12_it_management/05_security_compliance/586_it_management_core_topic_586_exam_summary/) ->

---
