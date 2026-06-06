---
title: "IT Management Core Topic 442 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 442. IT 경영 관리 핵심 토픽 442번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019의 EDM(평가·지시·모니터) 40개 거버넌스 목표를 기반으로, IT를 비용 센터(Cost Center)에서 비즈니스 가치 창출의 전략적 파트너(Value Driver)로 전환시키는 **Evaluate–Direct–Monitor(평가-지시-모니터링)** 피드백 사이클 체계이다.
> 2. **가치**: BMC(Davenport 2006) 기준 IT-비즈니스 정렬(Strategic Alignment) 기업은 비정렬 기업 대비 EBITDA 마진 11%p, ROA 3.6%p 우위를 보이며, ITSM 성숙도 Level 3 도달 시 운영 MTTR 41% 단축, 연간 IT 운영비 18~27% 절감이 가능하다(McKinsey IT Benchmark).
> 3. **판단 포인트**: ① 거버넌스 프레임워크(COBIT 2019 vs ISO 38500 vs ITIL 4) 선택 시 **Decision-Making Authority 분장**, ② EA(Enterprise Architecture)와 BSC-KPI의 **4관점(재무/고객/내부/학습성장) 연동 깊이**, ③ Shadow IT, Legacy Technical Debt, KPI 미연동 안티패턴 회피가 합격점이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 4.0 시대에서 기업 IT 부서는 과거 단순 인프라 운영·시스템 개발 주체에서 **"비즈니스 모델 혁신의 엔진"** 으로 재정의되어야 한다. Gartner(2023) 조사에 따르면 글로벌 CEO의 89%가 "Digital은 더 이상 IT 부서의 업무가 아니라 전체 사업의 생존 전략"이라고 응답했으나, 동시에 CIO의 71%가 "IT 투자 대비 비즈니스 가치 정량화가 어렵다"는 불일치(Digital Value Gap)를 호소한다. 이 간극(Gap)을 해소하는 것이 **IT 경영관리(Information Technology Management, ITM)** 의 존재 이유이며, 정보시스템 기술사 442번의 평가 핵심이다.

기존 패러다임은 **"IT는 비용이며, 통제 대상(Controllable Object)"** 이라는 인식이었다. 그러나 2008년 글로벌 금융위기, 2018년 GDPR(General Data Protection Regulation) 시행, 2020년 코로나19 비대면(Digital Contactless) 가속, 2023년 생성형 AI(LLM·GenAI) 도입으로 IT 시스템이 **사업 중단(Business Discontinuity)·규제 컴플라이언스·경쟁 우위 확보**의 핵심 자산으로 부상했다. ISO/IEC 38500(2008->2015) 표준이 "Direct, Evaluate, Monitor 3대 원칙"으로 등장했고, ISACA의 COBIT(Control Objectives for Information and Related Technologies)이 2019년 개정되며 40개의 거버넌스·관리 목표(Governance & Management Objectives)로 정교화되었다. 국내에서도 전자정부법(행정·공공기관 정보화 사업 시행 지침) 및 클라우드이용촉진법(2024) 등 법적 거버넌스 의무가 강화되면서, IT 거버넌스·전략·성과·서비스·아키텍처·프로젝트를 통합 관리하는 **IT 경영관리 체계**의 설계·운영 역량이 모든 IT 기술사에게 필수 역량으로 자리 잡았다.

```text
   +----------------------------------------------------------------------+
   |           IT 경영관리의 패러다임 전환 (1980 -> 2025)                   |
   +----------------------------------------------------------------------+

   1980~1990            2000~2010              2015~2020            2021~Now
   ----------           ----------             ----------           ---------
   Cost Center  ---►  Productivity Center -►  Value Center  ---►  Strategic Partner
   (비용 센터)        (생산성 센터)          (가치 센터)        (전략적 파트너)
       |                   |                     |                   |
   +---v---+         +-----v-----+         +----v----+        +-----v-----+
   |  Main  |         |  ERP/CRM  |         |  Cloud/ |        |  AI/Edge/ |
   |  Frame |         |  Package  |         |  Mobile |        |  Quantum  |
   |  IS    |         |  도입     |         |  First  |        |  DX/ESG   |
   +-------+         +-----------+         +---------+        +-----------+
       |                   |                     |                   |
   [통제/감사]         [표준화/효율]          [민첩/가치]        [자율/공존]
       |                   |                     |                   |
       +-------------------+---------------------+-------------------+
                                       |
                              +--------v---------+
                              |   IT 경영관리 5대  |
                              |   통합 거버넌스     |
                              |   (442번 핵심축)   |
                              +------------------+
                                       |
              +--------+--------+------+---+--------+--------+
              v        v        v          v        v        v
           전략     거버넌스   아키텍처    서비스    프로젝트   성과
         (IT Plan) (Govern)   (EA)      (ITSM)    (PMO)     (BSC/KPI)
```

- **📢 섹션 요약 비유**: IT 경영관리를 자동차에 비유하면, **COBIT 2019 = 자동차의 운전자 보조 시스템(ADAS)**, **EA = 차체 설계도**, **ITSM = 정기정비 매뉴얼**, **BSC = 계기판(KPI 모니터)**, **PMO = 정비공장 관리실**입니다. 이 5개가 어긋나면 아무리 좋은 엔진(기술)도 목적지에 닿지 못합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리는 5대 영역(Strategy·Governance·Architecture·Service·Performance)이 **PDCA(Plan-Do-Check-Act) + EDM(Evaluate-Direct-Monitor)** 이중 루프로 결합된 다층 참조모델(Reference Model)로 동작한다. 핵심 작동 메커니즘은 다음과 같다:

1. **전략(Strategy) 정렬**: 사업전략(CSF, Critical Success Factor)에서 IT 전략과제(IT Initiatives)를 도출하고, 이를 거버넌스 의사결정 체계(Steering Committee)에 상정.
2. **거버넌스 의사결정**: COBIT 2019 EDM 5개 도메인(EDM01~05) 중 **EDM02(가치 전달 보장), EDM04(리스크 최적화), EDM05(자원 최적화)** 가 의사결정 권한의 핵심.
3. **아키텍처 적용**: TOGAF ADM(Architecture Development Method) 8단계 Phase A~H로 EA를 수립하여 **표준·통합·연계** 기반 제공.
4. **서비스 운영**: ITIL 4의 **SVS(Service Value System) 7대 지침원칙**에 따라 Value Co-Creation.
5. **성과 측정**: BSC 4관점 × KPI -> CSF -> KGI로 인과지도(Causal Map) 구성 후 Balanced Scorecard 운영.

```text
   +--------------------------------------------------------------------------+
   |          IT 경영관리 5대 영역 × EDM/PDCA 이중 루프 통합 아키텍처         |
   +--------------------------------------------------------------------------+

                        +----------------------------+
                        |   Business Strategy (CSF)   |
                        |  (기업 미션·비전·사업전략)  |
                        +--------------+-------------+
                                       | ① 정렬(Alignment)
                                       v
                +--------------------------------------+
                |    IT Strategy & Portfolio (BSC)     |
                |  [CSF->KPI->KGI 인과지도(Strategy Map)]|
                +------------------+-------------------+
                                   | ② 지시(Direction)
                                   v
   +----------------------------------------------------------------------+
   |   COBIT 2019 EDM Governance Layer (ISO/IEC 38500 3원칙 매핑)        |
   |  +--------+  +--------+  +--------+  +--------+  +--------+         |
   |  | EDM01  |  | EDM02  |  | EDM03  |  | EDM04  |  | EDM05  |         |
   |  |거버넌스|  |가치전달|  |위험계획|  |리스크  |  |자원    |  ->Steering|
   |  |체계    |  |보장    |  |관리    |  |최적화  |  |최적화  |  Committee|
   |  +--------+  +--------+  +--------+  +--------+  +--------+         |
   +----------------------------------------------------------------------+
                                   | ③ 모티터링(Monitoring)
                                   v
   +----------------------------------------------------------------------+
   |          IT Management Layer (40개 Governance/Management Objectives) |
   +--------------+--------------+--------------+------------------------+
   | Align/Plan/  | Build/Acquire| Deliver/     | Monitor/Evaluate       |
   | Organize     | /Implement   | Service      | (MEA)                  |
   | (APO)        | (BAI)        | (DSS)        |                        |
   |  ★APO02 전략 |  ★BAI03 솔루 |  ★DSS02 서비 |  ★MEA01 성과모니터    |
   |  ★APO04 혁신 |   션 구축   |   스 요청    |  ★MEA02 내부통제      |
   |  ★APO12 리스 |  ★BAI11 프  |  ★DSS04 사  |  ★MEA03 외부감사      |
   |   크 관리    |   로젝트관리 |   고관리     |  ★MEA04 비준준사항    |
   +--------------+--------------+--------------+------------------------+
                                   |
            +----------------------+----------------------+
            v                      v                      v
   +-----------------+    +-----------------+    +------------------+
   | TOGAF ADM 8Ph.  |    | ITIL 4 SVS      |    | PRINCE2 / PMBOK  |
   | (EA 4관점)      |    | (서비스 7원칙)  |    | (프로젝트 5단계) |
   | BA/DA/AA/TA     |    | 34 Practices    |    | Initiation->      |
   |                 |    |                 |    | Closing          |
   +--------+--------+    +--------+--------+    +---------+--------+
            |                      |                       |
            +----------------------+-----------------------+
                                   v
                +--------------------------------------+
                |  Performance Measurement Layer       |
                |  -----------------------------------|
                |  • BSC 4관점 (F/C/ILP/LG) × SMART KPI|
                |  • SLA/OLa/UC(Service Level Mgmt)   |
                |  • TCO/ROI/NPV/IRR(투자경제성)      |
                |  • EV(Enterprise Value) / EVA        |
                |  • CMMI / COBIT Maturity Level 1~5  |
                +------------------+-------------------+
                                   | ④ 평가/환류(Feedback)
                                   v
                       +----------------------+
                       | Continuous Improvement|
                       |  (CSI/7-step Improve) |
                       +----------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 EDM Layer** | 거버넌스 의사결정(ISO 38500 매핑) | EDM01(체제)·EDM02(가치)·EDM03(위험)·EDM04(리스크 최적화)·EDM05(자원), 40개 목표(40 Governance & Management Objectives), **CSF->KPI->KGI 인과지도**로 의사결정 권한 분장(Board->SteerCo->CxO) |
| **TOGAF ADM** | EA(Enterprise Architecture) 4관점(BA·DA·AA·TA) 정합 | **Phase A(아키텍처 비전) -> H(아키텍처 변경관리)**, ADM Cycle(무한반복), **ArchiMate 3.2 표기법**(Motivation·Strategy·Business·Application·Technology·Physical Layer) |
| **ITIL 4 SVS** | IT 서비스 운영·가치공동창출(Co-Creation) | **7대 지침원칙**(Focus on Value·Start Where You Are·Progress Iteratively·Collaborate·Think & Work Holistically·Keep It Simple·Optimize & Automate), **34개 Practice(Service Desk·Incident·Problem·Change·SLM·CSI 등)** |
| **BSC + KPI 체계** | 전략->성과 인과 정량화 | **Kaplan·Norton 4관점**(재무/고객/내부프로세스/학습성장), **CSF->KPI->Target->KGI** SMART 5원칙, **Strategy Map** 토픽-인과 매핑 |
| **정보화 예산·회계** | IT 투자 경제성 의사결정 | **TCO(Total Cost of Ownership)** 5년 산정, **NPV(순현재가치)·IRR(내부수익률)·회수기간(Payback)·B/C ratio(비용편익비)**, **EVA**(Economic Value Added) — 정보화사업 시행지침 표준양식 |
| **PMO(Project Mgmt Office)** | 다수 프로젝트 통합·우선순위·포트폴리오 | PMBOK 10 Knowledge Area(통합·범위·일정·원가·품질·자원
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 442 / 800

<- **이전**: [441. IT 경영 관리 핵심 토픽 441번 시험 요약](/studynote/12_it_management/05_security_compliance/441_it_management_core_topic_441_exam_summary/)
**다음**: [443. IT 경영 관리 핵심 토픽 443번 시험 요약](/studynote/12_it_management/05_security_compliance/443_it_management_core_topic_443_exam_summary/) ->

---
