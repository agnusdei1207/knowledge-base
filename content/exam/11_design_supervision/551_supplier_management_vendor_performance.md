---
title: "Supplier Management Vendor Performance"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공급업체 관리(Supplier Management)는 ITIL 4 SVS의 34개 Practice 중 하나로, 벤더의 **선정(Sourcing)->계약(Contracting)->성과평가(Performance)->관계관리(Relationship)->종료(Exit)** 전 라이프사이클을 SLO/SLA 기반 정량 KPI로 통합 거버넌스하는 프로세스이며, ISO/IEC 20000-1:2018 §8.3, COBIT 2019 EDM04/DSS02, NIST SP 800-161(공급망 위험)와 매핑된다.
> 2. **가치**: 체계적 벤더 성과평가는 기업 IT 지출의 20~30%(Gartner 기준)를 차지하는 외부 조달 비용을 **8~15% 절감**하고, Critical Vendor 장애 시 평균 **MTTR을 42% 단축**(EMA Research)시키며, 4th-Party(Nth-Party) 가시성 확보를 통한 공급망 공격(Supply Chain Attack, 예: SolarWinds, 3CX, XZ Utils) 리스크를 **선제적**으로 차단한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **Kraljic Matrix** 상의 전략적 vs 병목형 공급처에 대한 차별화된 거버넌스 강도, ② 다중 벤더(Multi-vendor) 환경에서의 **계약 파편화(Contract Sprawl)** vs 단일 의존도(Single Point of Failure) 회피, ③ 정량 KPI 위주의 **점수카드(Scorecard)** vs 정성적 가치 협업(Value Co-Creation) 사이의 균형이며, 최근에는 ESG·SBOM(Software Bill of Materials)·DORA 제27조(ICT 제3자 위험관리)를 통합한 **TPRM(Third-Party Risk Management) 플랫폼**(예: ServiceNow TPRM, OneTrust, ProcessUnity, RSA Archer) 기반으로 진화하고 있다.

---

## Ⅰ. 개요 및 필요성

현대 엔터프라이즈 IT 환경에서 평균 **83%**(Deloitte Global Outsourcing Survey 2022)의 기업이 핵심 비즈니스 프로세스를 외부 벤더에 의존하고 있으며, 금융권은 DORA(Digital Operational Resilience Act), 공공은 클라우드 보안인증制度(CSAP), 의료는 HIPAA의 BAA(Business Associate Agreement) 등 **규제 기반 벤더 검증 의무**가 강화되고 있다. 이러한 환경에서 "**자체 통제 가능한 것**"과 "**외부에 위탁한 것**"의 경계가 모호해지면서, 벤더 관리는 단순 조달(Procurement) 기능에서 **엔터프라이즈 리스크 관리(ERM)의 핵심 축**으로 격상되었다.

기존의 **TCO(Total Cost of Ownership)** 중심의 가격 협상 모델은 ① 라이선스·유지보수 단가만 비교하여 **TCO의 60% 이상을 차지하는 운영·전환 비용**을 누락시키고, ② 인시던트 발생 시 **RCA(Root Cause Analysis)의 책임 소재**가 모호하며, ③ 벤더의 기술 부채(Technical Debt)가 내부 시스템으로 전이되는 현상을 방치한다는 한계가 있다. 반면, **VPE(Vendor Performance Evaluation)** 기반의 통합 거버넌스는 SLA·OLA·UC(Underpinning Contract) 체인을 통해 서비스 품질을 객관화하고, **Scorecard + Business Review(QBR/ABR)** 의 이원화된 통제 메커니즘으로 전환 비용·혁신 기여도·보안 컴플라이언스까지 포괄한다.

```text
[ 벤더 성과평가의 3-Layer 거버넌스 구조 ]

  +----------------------------------------------------------------+
  |  Layer 3: 전략 거버넌스 (Strategic Layer)                       |
  |  +--------------+  +--------------+  +----------------------+  |
  |  | Vendor Steering|  |  QBR/ABR    |  |  Kraljic Portfolio  |  |
  |  |   Committee   |  | (분기/연간) |  |  (전략/병목/병목/비핵심)|  |
  |  +------+-------+  +------+-------+  +----------+-----------+  |
  |         |                 |                     |              |
  +---------+-----------------+---------------------+--------------+
  |  Layer 2: 운영 거버넌스 (Operational Layer)                     |
  |  +------v-----------------v---------------------v-----------+  |
  |  |  TPRM Platform  (ServiceNow / OneTrust / ProcessUnity)  |  |
  |  |  -- 계약·위험·인시던트·컴플라이언스 단일 뷰(Single Pane) |  |
  |  +------+-------------------------------------------------+  |
  |         |  Telemetry / API / EDI / SCEM                       |
  +---------+------------------------------------------------------+
  |  Layer 1: 측정 및 자동화 (Measurement Layer)                   |
  |  +------v--------+  +-------------+  +--------------------+  |
  |  | KPI Scorecard |  | SLA Monitor |  | Observability APM  |  |
  |  | (가중치 모델) |  | (실시간)    |  | (Datadog/Splunk)  |  |
  |  +---------------+  +-------------+  +--------------------+  |
  +----------------------------------------------------------------+
         ^                    ^                    ^
         |                    |                    |
  +------+------+    +-------+-------+    +-------+--------+
  | Strategic   |    |   Tactical    |    |   Operational  |
  | Vendor (SAP)|    |  Vendor(MS)   |    |  Vendor(CDN)   |
  +-------------+    +---------------+    +----------------+
```

- **📢 섹션 요약 비유**: 벤더 성과평가는 마치 **항공기의 블랙박스 + 관제탑 + 정비 스케줄**을 동시에 운영하는 것과 같습니다. 블랙박스(데이터 수집)만으로는 사고 후 분석만 가능하고, 관제탑(실시간 모니터링)이 있어야 비상상황 즉시 대응이 가능하며, 정비 스케줄(점검·평가)이 있어야 엔진을 멈추지 않고 운항할 수 있습니다. 어느 하나라도 빠지면 추락합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

벤더 성과평가 시스템의 핵심은 **① 정량 KPI의 자동 수집 -> ② 가중치 기반 점수화(Weighted Scoring) -> ③ 관계 모델(Kraljic)에 따른 차등 거버넌스 적용 -> ④ 인사이트 기반 액션(Escrow·재입찰·종료)** 의 4단계 루프이다. ITIL 4의 Supplier Management Practice는 이를 **SVS(Service Value System)의 Value Chain Activity** 중 "Engage" 및 "Deliver and Support" 활동에 매핑하며, **PRINCE2의 Project Board** 와 **COBIT 2019의 DSS02(Managed Service Requests and Incidents)** 와 직접 연동된다.

```text
[ 벤더 성과평가 End-to-End 프로세스 아키텍처 ]

  +---------+    +---------+    +----------+    +--------------+
  | Sourcing|---->|Contract |---->|Performance|---->|  Relationship |
  |  전략   |    |  관리    |    |   측정    |    |    개발       |
  +----+----+    +----+-----+    +-----+----+    +------+-------+
       |              |               |                  |
       v              v               v                  v
   [RFI/RFP/RFQ]  [MSA/SOW/SLA]   [KPI Scorecard]   [QBR/ABR]
       |              |               |                  |
       |   +----------+---------------+--------------+   |
       |   |          |   데이터 수집 |              |   |
       |   |          |   ^     ^    |              |   |
       |   |          |   |     |    |              |   |
       |   v          v   |     |    v              v   |
       |  +----------------+-----+---------------------+  |
       |  |  통합 데이터 파이프라인 (TPRM Platform)     |  |
       |  |  - CMDB 연동 (ServiceNow CMDB / BMC RIK)   |  |
       |  |  - API/EDI 수집 (Jira/Zendesk/Salesforce)   |  |
       |  |  - SBOM 분석 (Snyk/CycloneDX/Black Duck)   |  |
       |  |  - 침투 테스트 결과 (Nessus/Qualys)        |  |
       |  +----------------+--------------------------+  |
       |                   |                              |
       |                   v                              |
       |  +------------------------------------------+    |
       |  |  가중치 평가 엔진 (Weighted Scoring)      |    |
       |  |  S = Σ(Wi × Pi)  (i=1..n)                |    |
       |  |  W: 가중치, P: 0~100 점수, 등급 산출      |    |
       |  +----------------+----------------------+-+    |
       |                   |                      |      |
       |                   v                      v      |
       |   +-------------------------+  +-----------------+
       |   | Action Engine           |  |  Reporting      |
       |   | - 임계치 위반 시 경고    |  |  - 대시보드     |
       |   | - 에스컬레이션 룰 엔진  |  |  - ESG/SBOM     |
       |   | - 소스코드 에스크로     |  |  - 규제 보고서  |
       |   +-------------------------+  +-----------------+
       |
       +-->[ Exit / Renewal / 리스크 전가 판단 ]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Sourcing & Onboarding** | 벤더 탐색·검증·등록 | RFI(정보요청서) -> RFP(제안요청서) -> RFQ(견적요청서)의 3단계 Funnel, **DDI(Direct DUNS Index)**, **Sam.gov(SAM)**, **Know Your Vendor(KYV)** 를 통한 실사, **PEP(Politically Exposed Person)** 및 제재리스트 스크리닝(OFAC SDN, UN, EU) |
| **Contract Lifecycle Mgmt(CLM)** | MSA·SOW·DPA·BAA의 작성/갱신/만료 관리 | **CLM 플랫폼** (Icertis, Agiloft, Ironclad) 활용, **Contract AI**(NLP 기반 조항 추출·이상 조항 탐지), 갱신 알림·자동 협상 봇, **Crypto Shredding**(키 폐기로 암호학적 삭제) 통한 DPA 종료 |
| **KPI Scorecard Engine** | 가중치 기반 정량 평가 | **BSC(Balanced ScoreCard)** 4관점(재무/고객/내부/학습) 또는 **IT4IT**의 SQM(Service Quality Management) 참조, 가중치 산정 시 **AHP(Analytic Hierarchy Process)**, **TOPSIS**, **Saaty의 쌍대비교 매트릭스** 활용. 산식: `Performance Index = Σ(Weight_i × Normalized_Score_i)` |
| **Real-time SLA Monitor** | SLA·OLA·UC 위반 탐지 | **Prometheus/Grafana** 기반 임계치 알람, **OpenSLO(Service Level Objective)**, **Datadog SLO**, **Catchpoint**(외부 측정), **AppDynamics** Business iQ로 사용자 영향도 매핑 |
| **Risk & Compliance Module** | 4th-Party·규제 리스크 통합 | **NIST SP 800-161**(C-SCRM), **ISO 27036**(공급망 보안), **ISO 20243**(O-TTPS), **DORA Art.28-30**(ICT 제3자 위험), **K-ISMS** 인증서 자동 파싱, **SBOM** 기반 취약점 매칭(CVE->CPE) |
| **QBR/ABR & Governance** | 전략적 관계·이슈 해결 | 분기(QBR)·연간(ABR) 비즈니스 리뷰, **Vendor Tier Matrix**(Strategic/Tactical/Operational/Transactional), **Executive Sponsor** 양방향 지정, **Innovation Fund** 공동 운영 |
| **Exit & Transition** | 계약 종료·전환 | **Exit Plan**(90/180/365일 단계별), **Source Code Escrow**(Iron Mountain, NCC Group), **Data Portability**(ISO/IEC 19944, GAIA-X 표준), **Knowledge Transfer** 체크리스트 |

**KPI 선정의 핵심 원칙 (SMART-R)**:
- **S**pecific(예: "P1 인시던트 응답시간 ≤ 15분")
- **M**easurable(자동 측정 가능, 수작업 배제)
- **A**ttainable(벤더가 현실적으로 달성 가능한 수준)
- **R**elevant(비즈니스 임팩트와 직결)
- **T**ime-bound(측정 주기: 실시간/일/월/분기)

**Kraljic Portfolio Matrix** (1983, Peter Kraljic)는 벤더를 **4-Quadrant**로 분류한다:
- **Strategic(전략적)**: 고수요/고복잡 -> 파트너십, **Joint Planning**, 장기계약(3~5년)
- **Leverage(레버리지)**: 고수요/저복잡 -> 가격 경쟁 유도, 다중 소싱
- **Bottleneck(병목)**: 저수요/고복잡 -> 재고 확보, 이원화, 대안 R&D
- **Non-critical(비핵심)**: 저수요/저복잡 -> 표준화, 셀프서비스, ATP(Automated Transaction Processing)

- **📢 섹션 요약 비유**: Kraljic Matrix는 **병원 응급실의 중증도 분류(Triage)** 와 같습니다. 심장마비(Strategic)는 즉시 수술실로, 골절(Leverage)은 순서대로 처리, 감기(Non-critical)는 자가 치료 권고. 모든 환자에게 MRI를 찍는 것은 자원 낭비이며, **위험도와 영향도에 따라 자원을 차등 배분**하는 것이 시스템의 핵심입니다.

---

## Ⅲ. 비교 및 연결

| 구분 | 전통적 조달(Procurement) | SRM(Supplier Relationship Mgmt) | **VPE 통합 거버넌스 (TPRM 2.0)** |
| :--- | :--- | :--- | :--- |
| **목적** | 단가 협상·계약 체결 | 장기 관계·상생 가치 | 리스크·성능·규제 통합 최적화 |
| **평가 차원** | Price(단가), Lead Time | Cost, Quality, Delivery, Innovation(CQDI) | CQDI + ESG + SBOM + Nth-Party + 규제(DORA/ISO27001) |
| **데이터 수집** | 견적서·계약서 수작업 | ERP/SRM(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 551 / 600

<- **이전**: [550. IT 재무 관리 FinOps 비용 최적화](/studynote/11_design_supervision/06_exam_summary/550_it_financial_management_finops_cost_opti)
**다음**: [552. 정보 보안 거버넌스 정책 수립](/studynote/11_design_supervision/06_exam_summary/552_information_security_governance_policy/) ->

---
