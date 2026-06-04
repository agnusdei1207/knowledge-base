---
title: "701. IT 경영 관리 핵심 토픽 701번 시험 요약 (IT Management Core Topic 701 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019, ITIL 4, ISO 27001, PMBOK 7th, EA(Enterprise Architecture)** 등 글로벌 프레임워크를 기반으로 IT 거버넌스·전략·운영·감리를 통합 관리하는 체계이며, 기술사 시험 701번은 **"IT 전략 기획 -> 정보화 투자 대비 효과 분석 -> EA 수립 -> SI 사업 관리 -> 정보시스템 감리"** 로 이어지는 end-to-end Value Chain을 평가한다.
> 2. **가치**: 체계적 IT 경영 체계 도입 시 **정보화 투자 대비 효과(ROI) 20~35% 개선**, IT 서비스 가용성 **99.95% 이상 확보**, 감사 적격성(Audit Readiness) 확보를 통한 **컴플라이언스 위반 리스크 60% 이상 감소**, 그리고 EA 기반 중복 투자 방지로 **TCO 15~25% 절감** 효과를 달성할 수 있다.
> 3. **판단 포인트**: 핵심 trade-off는 **①거버넌스 통제 강도 vs. 사업 Agile성**, ②**표준 프레임워크 준수(Cobit/ITIL) vs. 조직 맞춤(customization)**, ③**단기 ROI vs. 중장기 EA 기반 경쟁력**, ④**내부 역량(Insourcing) vs. 외부 SI 아웃소싱**의 4가지 축에서 최적 균형점(Optimal Equilibrium)을 찾는 것이며, 기술사는 **정량 KPI(BSC 4관점) + 정성 KPI(Gartner Magic Quadrant, 사용자 만족도)** 를 혼합한 의사결정 프레임을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 단순히 "IT 부서를 잘 운영하는 것"이 아니라, **조직의 미션·비전·전략(Strategy)을 IT가 어떻게 지원하고 가치를 창출할 것인가**를 정의하는 통합 관리 체계이다. 4차 산업혁명(AI, Cloud, BigData, IoT) 시대를 맞아 IT는 **코스트 센터(Cost Center)에서 프로핏 센터(Profit Center), 나아가 비즈니스 트랜스포메이션 센터**로 그 역할이 급격히 변화하고 있으며, 이에 따라 기술사 시험 701번은 경영학·정보기술·프로젝트관리·법·감리가 융합된 종합적 판단력을 요구한다.

과거(1990~2000년대)에는 **"데이터 중심의 정보화"**로 ERP, CRM, SCM 등 단위 시스템 단위의 구축이 주를 이루었으나, **MDA(Model Driven Architecture)·SOA·MSA**로의 패러다임 전환, 그리고 **클라우드·DevOps·AI**의 등장으로 인해 **"데이터 -> 프로세스 -> 서비스 -> 경험 -> 생태계"**로의 가치 사슬(Value Chain) 재정의가 필수적이 되었다. 또한 **개인정보보호법, 정보통신망법, 전자금융거래법, 클라우드컴퓨팅법, AI 기본법** 등 규제 환경이 급격히 강화됨에 따라, IT 투자의 **법·규제 준수(Compliance)** 측면이 경영 리스크의 핵심 변수로 부상했다.

```text
+----------------------------------------------------------------------+
|           IT 경영 관리 5대 영역 통합 체계 (701번 Value Chain)         |
+----------------------------------------------------------------------+

  +----------------+    +----------------+    +----------------+
  | 1. IT 전략기획 | ->  | 2. 정보화투자  | ->  | 3. EA(전사아키 |
  |  (ISP 수립)   |    |   효과분석     |    |    텍처) 수립  |
  |                |    |   (BPR/ROI)   |    |                |
  +----------------+    +----------------+    +----------------+
          |                     |                      |
          v                     v                      v
  +-------------------------------------------------------------+
  |       4. SI 사업관리 (발주/조달/계약/형상/테스트/인수)      |
  |       - PMBOK 7th, 발주처 PMO, RFI/RFP, V-Model            |
  +-------------------------------------------------------------+
          |
          v
  +----------------+    +----------------+    +----------------+
  | 5. 정보시스템 | ->  | 6. IT 운영관리 | ->  | 7. IT 거버넌스 |
  |     감리       |    |  (ITSM/ITIL4) |    |   (COBIT 2019) |
  +----------------+    +----------------+    +----------------+
          |                     |                      |
          +---------------------+----------------------+
                                |
                                v
              +----------------------------------+
              |  비즈니스 가치(Value Realization)|
              |  · ROI 20~35% 개선              |
              |  · Time-to-Market 40% 단축      |
              |  · 컴플라이언스 위반 < 0.1%      |
              +----------------------------------+
```

**왜 필요한가?**

1. **전략 정렬(Strategic Alignment)**: Henderson & Venkatraman(1993)의 **SAM(Strategic Alignment Model)**에 따르면, IT-Business 정렬도가 1단위 향상될 때 기업 성과가 평균 **2.5~11% 향상**된다. IT 전략기획(ISP: Information Strategy Planning)은 이러한 정렬을 달성하는 핵심 도구이다.
2. **투자 효율화**: 한국 정보화진흥원의 조사에 따르면, 체계적 **CBA(Cost-Benefit Analysis)** 미수행 시 IT 프로젝트의 **63%가 예산 초과, 45%가 기대 효과 미달** 상태로 종료된다.
3. **리스크 관리**: IBM 2024 Cost of Data Breach Report 기준, 글로벌 데이터 유출 1건당 평균 비용 **$4.88M(약 650억원)**, 체계적 거버넌스 부재 시 **2.3배 증가**한다.
4. **규제 준수**: 정보시스템 감리법(제1조)에 따라, 국가·공공기관의 일정 규모 이상 정보화 사업은 **법적 감리 의무**가 있으며, 일반 기업도 **DPA(데이터보호영향평가), ISMS-P, PIMS 인증** 등 자율 규제 대응이 필수이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"배의 키잡이(Rudder Holder)"**와 같다. 좋은 엔진(기술)와 돛(혁신)만으로는 거친 항해(시장·규제 환경)를 헤쳐나갈 수 없으며, 나침반(전략), 해도(아키텍처), 뱃사람들(프로젝트 인력), 항해일지(감리)까지 총체적으로 관리해야 목적 항구(사업 가치)에 안전히 도착할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 핵심 영역은 **전략(Strategy) -> 구조(Architecture) -> 실행(Delivery) -> 운영(Operation) -> 통제(Governance)**의 논리적 흐름을 따른다. 각 영역은 상호 의존적이며, 어느 한 영역의 부재는 전체 가치 사슬의 단절을 초래한다.

```text
+----------------------------------------------------------------------+
|            IT 경영 관리 핵심 프레임워크 통합 참조 모델(IRM)           |
+----------------------------------------------------------------------+

       +-----------------------------------------------+
       | ① Strategy Layer : IT 전략기획(ISP)           |
       |  · SWOT/PEST, Value Chain 분석                 |
       |  · BSC 4관점(재무/고객/내부/학습성장)          |
       |  · 정보화 투자 ROI, NPV, IRR, Payback Period  |
       +-----------------+-----------------------------+
                         | KPI 연계
                         v
       +-----------------------------------------------+
       | ② Architecture Layer : EA (전사아키텍처)       |
       |  · Zachman 6×6 Framework                       |
       |  · TOGAF 10 ADM (Architecture Development)    |
       |  · FEAF(Federal EA), DoDAF, Gartner EA         |
       |  · 4대 영역: BA/DA/AA/TA (or BA/IS/TS/AS)    |
       +-----------------+-----------------------------+
                         | 표준·가이드
                         v
       +-----------------------------------------------+
       | ③ Delivery Layer : SI 사업관리 + PMO          |
       |  · PMBOK 7th, PRINCE2, ISO 21502             |
       |  · 5단계: 발주 -> 제안(RFP) -> 구축 -> 시험 -> 인수|
       |  · V-Model, Agile(Scrum, SAFe 6.0)            |
       |  · 형상관리(Git), CI/CD(Jenkins, ArgoCD)      |
       +-----------------+-----------------------------+
                         | SLA/OLA
                         v
       +-----------------------------------------------+
       | ④ Operation Layer : ITSM (IT Service Mgmt)     |
       |  · ITIL 4 (34 Practices)                       |
       |  · ISO 20000 (Service Management)              |
       |  · 인시던트/문제/변경/릴리스/서비스데스크      |
       |  · SLA 99.9%^, MTTR < 1h, MTBF > 720h        |
       +-----------------+-----------------------------+
                         | 통제·측정
                         v
       +-----------------------------------------------+
       | ⑤ Governance Layer : COBIT 2019 + 컴플라이언스|
       |  · COBIT 2019: 40 Governance & Mgmt Objectives|
       |  · EDM(평가/지휘/모니터), 4 Domains            |
       |  · ISO 27001/27701, ISMS-P, GDPR, PIPA        |
       |  · 정보시스템 감리(법 제1조 의무)              |
       +-----------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 전략기획(ISP)** | 사업·IT 전략 정렬 및 로드맵 수립 | SWOT/PEST/Porter 5 Forces 분석 -> BSC 4관점 KPI 도출 -> **AHP(Analytic Hierarchy Process) 기반 우선순위 결정** -> 중장기 로드맵(3~5년) 수립 -> 정보화 예산 편성 |
| **전사아키텍처(EA)** | 업무·데이터·응용·기술 표준화 및 통합 | **TOGAF ADM 8단계**(Preliminary->Vision->Business->IS->Technology->Opportunities->Migration->Governance), **Zachman 6×6**, **ArchiMate 3.2** 표기법, BA/DA/AA/TA 4개 영역 아티팩트 관리(Archi/EA Sparx/Bizagi) |
| **SI 사업관리(PMO)** | 정보화 사업의 발주·구축·인수 형상관리 | **PMBOK 7th 8绩效域**(Stakeholder, Team, Development, Planning, Work, Delivery, Measurement, Uncertainty), WBS·OBS·RBS, EVM(Earned Value), **CCB(Change Control Board)**, RFP/RFI, **V-Model 단계별 검증(단위->통합->시스템->인수)** |
| **IT 서비스 운영(ITSM)** | 서비스 가용성·품질·고객만족 확보 | **ITIL 4 34 Practices**(Incident, Problem, Change, Service Desk, Service Level, Continual Improvement), **CMDB(Configuration Management DB)**, ITSM 도구(ServiceNow, Jira Service Management, Remedy), MTTR·MTBF·FCR 측정 |
| **정보시스템 감리** | 정보화 사업의 적정성·효율성 검증 | **「정보시스템 감리법」 제1조·제14조**, **TTA·TTAK 표준**, **GS인증(Good Software)**, 감리단계(①착수 ②수행중 ③완료), 적격성·성능·보안·안정성 평가, **ISMS-P(정보보호관리체계) 인증** 연계 |
| **IT 거버넌스(Governance)** | 의사결정·책임·리스크·컴플라이언스 통합 관리 | **COBIT 2019**: EDM(평가/지휘/모니터) + 4 Domain(APO/BAI/DSS/MEA) + 40 Objective, **ISO 38500(거버넌스 국제표준)**, 3개 라인 방어 모델(1st:운영, 2nd:리스크/컴플, 3rd:내부감사) |
| **정보화 투자 효과분석** | 정량·정성 효과 측정 및 의사결정 지원 | **CBA(Cost-Benefit Analysis)**: NPV, IRR, BCR, Payback Period, **TCO(Total Cost of Ownership)**, **VOI(Value of Investment)** 정성평가, AHP/DEA(Data Envelopment Analysis) |

**핵심 원리 5가지 (기술사식 관점)**

1. **전략 정렬(Strategic Alignment)** : Henderson-Venkatraman SAM 모델 — **Business Strategy ↔ IT Strategy**, **Business Infrastructure ↔ IT Infrastructure**의 양방향 정렬.
2. **계층화(Abstraction Layering)** : Zachman Framework의 **WHAT/HOW/WHERE/WHO/WHEN/WHY × Planner/Owner/Designer/Builder/Subcontractor/Operational** 매트릭스 — 6×6 = 36셀 아티팩트.
3. **거버넌스-관리 분리(Governance-Management Distinction)** : ISO 38500 + COBIT 2019의 핵심 — **"거버넌스는 의사결정(Decide), 관리는 실행(Implement)"**. 이 분리가 흐려지면 책임 소재가 불명확해진다.
4. **Value Realization(가치 실현)** : 단순 구축이 아닌 **"Plan -> Deliver -> Operate -> Measure -> Improve"** 의 Closed Loop. **Stage-Gate + Benefit Realization Plan(BRP)** 으로 단계별 게이트 통과 시점 명확화.
5. **원리 우선(Principles First)** : COBIT 2019의 **6가지 Governance System Principles**(예: 제공 이해관계자 가치, 전체 조직 포괄, 단일 통합 체계 적용 등)와 **3가지 Goals Cascade Mechanism**을 통해 프레임워크 간 정합성 확보.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"오케스트라 지휘자"**와 같다. 바이올린(전략), 첼로(아키텍처), 트럼펫(프로젝트), 팀파니(운영), 그리고 청중(거버넌스) 모두가 각자의 악보(프레임워크)를 가지고 있지만, 이들을 **하나의 하모니(가치)**로 엮어내는 것이 지휘자의 역할이다. 지휘자가 없으면 각 악기는 시끄럽게만 울릴 뿐, 교향곡이 될 수 없다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역의 혼동하기 쉬운 핵심 개념들을 명확히 구분하기 위해 비교 분석한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 목표 체계 | IT 서비스 운영 Best Practice | 프로젝트 관리 표준 | 전사아키텍처 구축 방법론 |
| **관점** | **What**(무엇을 관리할 것인가) | **How**(어떻게 운영할 것인가) | **How**(어떻게 프로젝트를 수행할 것인가) | **How**(어떻게 아키텍처를 만들 것인가) |
| **주 사용자** | CISO·CIO·이사회·내부감사 | IT 운영팀·서비스매니저·프로세스오너 | PM·PMO·사업관리자 | EA 아키텍트·CIO·전략기획 |
| **핵심 구조**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 701 / 800

<- **이전**: [700. IT 경영 관리 핵심 토픽 700번 시험 요약](/studynote/12_it_management/05_security_compliance/700_it_management_core_topic_700_exam_summary/)
**다음**: [702. IT 경영 관리 핵심 토픽 702번 시험 요약](/studynote/12_it_management/05_security_compliance/702_it_management_core_topic_702_exam_summary/) ->

---
