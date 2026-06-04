---
title: "721. IT 경영 관리 핵심 토픽 721번 시험 요약 (IT Management Core Topic 721 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(721번)는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 사슬(Service Value Chain), ISO 38500 IT 거버넌스 표준, 그리고 Balanced Scorecard(BSC)를 통합하여 **전략(Strategy)-포트폴리오(Portfolio)-프로그램(Program)-운영(Operation)** 4계층으로 IT를 경영 자산화하는 것이다.
> 2. **가치**: 성숙도 2단계(Repeatable) 조직을 4단계(Managed) 이상으로 끌어올릴 경우 MTTR(평균 복구시간) 40~60% 단축, TCO(Total Cost of Ownership) 20~30% 절감, Shadow IT 70% 감소, IT 프로젝트 성공률(CHAOS Report 기준 31%->68%) 향상을 달성할 수 있다.
> 3. **판단 포인트**: 핵심 의사결정축은 ①거버넌스 모드(중앙집중형 vs 연방형 vs 가버넌스 네트워크), ②EA(Enterprise Architecture) 적용 범위(전사 vs 사업부), ③Agile/DevOps 도입 시 거버넌스 경직성 회피를 위한 **Governance as Code** 적용 여부, ④투자 포트폴리오 비중(Run-the-Business 60~70% / Grow-the-Business 20~30% / Transform-the-Business 5~15%)이다.

---

## Ⅰ. 개요 및 필요성

21세기 들어 정보기술은 단순 지원 기능을 넘어 **경영 전략의 핵심 동력**으로 자리 잡았으며, Gartner(2023)에 따르면 글로벌 CEO의 89%가 IT를 전략적 우선순위로 인식하고 있다. 그러나 McKinsey의 "Digital Quotient" 조사에 따르면, 기업의 70% 이상이 디지털 전환(DX) 투자 대비 기대효과를 달성하지 못하고 있으며, 이 실패의 근본 원인은 **IT-Biz 정렬(Alignment) 부재**, **거버넌스 체계 미흡**, **IT 성과 측정 불가**라는 세 가지 경영 관리 부재에서 기인한다.

기존 1980~90년대식 IT 관리는 **비용 센터(Cost Center)** 관점이었으나, 2000년대부터 IT가 비즈니스 가치(Value)를 직접 창출하는 **투자 센터(Investment Center)** 또는 **전략적 자산(Strategic Asset)**으로 재정의되었고, 이를 뒷받침할 경영 관리 프레임워크의 필요성이 대두되었다. ISO/IEC 38500:2015, COBIT 2019, ITIL 4가 이러한 흐름을 주도하고 있으며, 한국에서는 전자정부법, 클라우드컴퓨팅법, 정보통신망법, 개인정보보호법이 IT 경영 관리의 법적 기반을 제공한다.

```text
[IT 경영 관리 4계층 구조와 가치 흐름]

+---------------------------------------------------------------------+
|   1계층: IT 거버넌스 (IT Governance)                                |
|   +-------------+  +-------------+  +-------------+               |
|   |   COBIT 2019 |  | ISO 38500  |  |  ISO 27001  |               |
|   | (40 Gov/    |  |  (6 Principles| | (ISMS)     |               |
|   |  Mgmt Obj)  |  |  Evaluate-  |  |            |               |
|   +------+------+  | Direct-    |  +------+-----+               |
|          |         | Monitor)  |           |                      |
|   +------v---------v-----------v-----------v------+              |
|   |       이사회 / CIO / 거버넌스 위원회            |              |
|   +--------------------+-------------------------+              |
+------------------------+-----------------------------------------+
                         | 전략 정렬(Strategy Alignment)
+------------------------v-----------------------------------------+
|   2계층: IT 전략 및 포트폴리오 관리                                 |
|   +----------------------+  +----------------------+              |
|   | IT Strategic Plan    |  | IT Portfolio Mgmt    |              |
|   | (ISP 3~5년)          |<-->| (Application/Infra/  |              |
|   | - SWOT/PEST 분석     |  |  Project 분류)       |              |
|   +----------------------+  +----------+-----------+              |
|   +----------------------------------v----------+                |
|   |  투자 비중: RtB 65% / GtB 25% / TtB 10%     |                |
|   +---------------------------------------------+                |
+------------------------+-----------------------------------------+
                         | 아키텍처 정렬(Architecture Alignment)
+------------------------v-----------------------------------------+
|   3계층: IT 운영 및 서비스 관리 (IT Service Management)            |
|   +-------------+  +-------------+  +-------------+             |
|   |   ITIL 4    |  |  DevOps     |  |  SRE        |             |
|   | Service     |  | (CI/CD,     |  | (SLO/SLI/   |             |
|   | Value Chain |  |  IaC)       |  |  Error Budget)|            |
|   +-------------+  +-------------+  +-------------+             |
+------------------------+-----------------------------------------+
                         | 가치 측정(Value Measurement)
+------------------------v-----------------------------------------+
|   4계층: IT 성과 측정 및 개선 (IT Performance Management)         |
|   +--------------+  +--------------+  +--------------+          |
|   |  BSC 4관점    |  |  KPI Tree    |  |  벤치마킹     |          |
|   | 재무/고객/   |  | (CSF->KPI->   |  | (ITIL Bench- |          |
|   | 내부프로세스/|  |  측정지표)   |  |  marking DB) |          |
|   | 학습성장     |  |              |  |              |          |
|   +--------------+  +--------------+  +--------------+          |
+-------------------------------------------------------------------+
        v
   +--------------------------------------------+
   |   비즈니스 가치 (Business Value)           |
   |   - Revenue ^ / Cost v / Risk v           |
   |   - Time-to-Market 단축 / NPS 향상         |
   +--------------------------------------------+
```

**Why IT Management? (필요성)**
- **비용 가시성 부족**: Forrester 조사에서 IT 예산의 30%가 Shadow IT로 새고 있음
- **규제 컴플라이언스**: GDPR(연 20억 유로/4% 매출), 개인정보보호법(5억 원/5%), ESG 공시 의무화
- **사이버 위험 증대**: IBM 2023 Cost of Data Breach Report에서 글로벌 평균 위반비용 445만 USD
- **디지털 전환 가속**: IDC에 따르면 2026년까지 디지털 투자 1조 8천억 USD 전망

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **항공기의 계기판과 자동조종장치**와 같습니다. 연료(예산), 고도(성과), 풍향(시장변화), 기압(위험)을 실시간 모니터링하지 않으면, 아무리 좋은 엔진(기술)도 추락(실패)할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **PDCA 사이클**을 4계층(거버넌스-전략-운영-성과)에 동시에 적용하는 것이다. COBIT 2019의 40개 거버넌스/관리 목적(Governance & Management Objectives)을 5개 도메인(EDM: Evaluate, Direct, Monitor / APO: Align, Plan, Organize / BAI: Build, Acquire, Implement / DSS: Deliver, Service, Support / MEA: Monitor, Evaluate, Assess)으로 분류하고, 이를 ITIL 4의 34개 실무(34 Practices)와 1:1 매핑한다.

```text
[IT 경영 관리 핵심 프로세스 흐름 - COBIT 2019 + ITIL 4 통합]

[1. 요구사항 도출] -> [2. 전략 수립] -> [3. 포트폴리오 선정] -> [4. 아키텍처 설계]
        |                  |                   |                       |
   COBIT EDM01        COBIT EDM02        COBIT APO05             TOGAF ADM
   (Governance        (Benefits          (Portfolio              (Preliminary
   Framework)         Delivery)          Mgmt)                   Phase ~ Phase E)
        |                  |                   |                       |
        v                  v                   v                       v
[5. 투자 결정] -> [6. 솔루션 구축] -> [7. 서비스 운영] -> [8. 성과 측정]
        |                  |                   |                       |
   COBIT APO06        COBIT BAI03         ITIL 4 SVC              COBIT MEA01
   (Budget & Cost)    (Manage Solutions)  (Plan/Improve/         (Performance &
                                         Engage/Design/          Conformance
                                         Obtain/Build/Deliver)   Monitoring)
        |                  |                   |                       |
        +------------------+-------------------+-----------------------+
                                         |
                                         v
                              [9. 지속적 개선 (CSI)]
                                    ITIL CSI
                                    (Continual Service
                                     Improvement)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 위원회 (IT Steering Committee)** | CIO·사업부·감사·리스크·CISO로 구성된 의사결정 기구. 분기별 회의로 ①IT 전략 승인 ②투자 포트폴리오 결정 ③아키텍처 표준 승인 ④리스크 허용 한도 설정 | RACI 매트릭스(Responsible/Accountable/Consulted/Informed), 의사결정 권한 매트릭스(DAM: Decision Authority Matrix) 적용. 1회 회의 시 평균 12~20건 안건 처리 |
| **EA(Enterprise Architecture) 팀** | 비즈니스-애플리케이션-데이터-인프라 4계층 아키텍처 표준 수립 및 기술 부채 관리 | **TOGAF ADM**(Architecture Development Method) 8단계, **Zachman Framework** 6x6 매트릭스, **ArchiMate 3.1** 표기법. EA 도구: ABACUS, LeanIX, Orbus iServer, MEGA Hopex |
| **IT PMO (Project Management Office)** | 프로젝트 포트폴리오 관리, 표준화, PPM 도구 운영 | **PMS(Portfolio Management System)**: Planview, CA Clarity PPM, MS Project Online. **방법론**: PMBOK 7th(12 Principle), PRINCE2, Agile(Scrum/Kanban) |
| **IT 서비스 운영 조직** | ITIL 4 기반 서비스 데스크, 인시던트, 문제, 변경, 릴리스, 구성 관리 | **ITSM 도구**: ServiceNow, BMC Helix, Jira Service Management. **자동화**: Ansible Tower, ServiceNow Orchestration, Rundeck |
| **IT 재무 및 성과 관리** | TCO/ROI/NPV/IRR 산출, IT 활동별 원가계산, BSC 기반 KPI 관리 | **활동기준원가계산(ABC: Activity-Based Costing)**, **TBM(Technology Business Management)** 프레임워크(apptio), FinOps(클라우드 비용 최적화) |
| **정보보안 및 컴플라이언스** | ISMS, PIMS, GDPR, PCI-DSS, HIPAA 등 통제활동 | **ISMS-P 인증(한국), ISO 27001/27701, NIST CSF 2.0, Zero Trust Architecture**. **GRC 플랫폼**: SAP GRC, ServiceNow GRC, Archer |
| **IT 인적자원 관리** | 디지털 역량 갭 분석, 학습 로드맵, 채용 전략 | **SFIA(Skills Framework for the Information Age) v8**, **DDoS(Digital Skills Development Strategy)**, **리더십 파이프라인**(CIO 후보군 양성) |
| **IT 벤더 및 계약 관리** | SaaS/IaaS/PaaS/아웃소싱 계약 SLA 관리, 벤더 리스크 평가 | **SLM(Service Level Management)**: 가용성 99.9%(연 8.76h 다운타임 허용), 응답시간 P95, MTTR, RPO/RTO. **계약 모델**: T&M, Fixed-Price, Outcome-Based, Gain-Share |

**핵심 파라미터 및 측정지표 (KPI)**
- **TCO 계산식**: TCO = 직접비(HW/SW/인건비) + 간접비(교육/설치/관리) + 운영비(전력/냉각/네트워크) + 은닉비용(Shadow IT, 기회비용)
- **NPV(순현재가치)**: Σ [CFₜ / (1+r)ᵗ] - 초기투자, r=할인율(보통 8~12%)
- **TCO 절감률 목표**: 클라우드 마이그레이션 시 3년 TCO 25~40% 절감 (AWS Well-Architected 기준)
- **SLA 등급**: 99% (Tier-1) / 99.9% (Tier-2, 연 8.76h) / 99.95% (Tier-3, 연 4.38h) / 99.99% (Tier-4, 연 52.6m)
- **성숙도 모델**: CMMI 5단계(Initial->Managed->Defined->Quantitatively Managed->Optimizing) 또는 COBIT 2019 5단계(0~5)

- **📢 섹션 요약 비유**: 이 4계층 구조는 **피라미드 형태의 빌딩 관리 시스템**과 같습니다. 1층 거버넌스는 빌딩 소유주(이사회), 2층 전략은 설계도, 3층 운영은 건물 관리 사무소, 4층 성과측정은 에너지 미터기와 같습니다.

---

## Ⅲ. 비교 및 연결

| 구분 | COBIT 2019 | ITIL 4 | ISO 38500 | PMBOK 7 |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스/관리 통합 프레임워크 | IT 서비스 관리(라이프사이클) | IT 거버넌스 국제표준 | 프로젝트 관리 원칙 |
| **대상 계층** | 이사-CIO-전 실무자 | 서비스 운영 실무자 | 이사진-최고경영자 | 프로젝트 매니저 |
| **구조** | 5도메인 40목표 | 4디멘션 34프랙티스 | 6원칙(Evaluate-Direct-Monitor) | 12원칙 8도메인 |
| **측정 강조** | 목표 연쇄(Goals Cascade) | 가치 흐름(Value Stream) | 책임과 성과 | 성과 측정 도메인 |
| **인증/표준** | ISACA 공인 | PeopleCert/Axelos | ISO/IEC 국제표준 | PMI 공인 |
| **결합 시너지** | 거버넌스(Why/What) | 서비스 운영(How) | 원칙 프레임워크 | 프로젝트 실행 |

```text
[다른 표준/프레임워크와의 관계도]

                        +----------------------+
                        |   비즈니스 전략       |
                        | (Vision / Mission)   |
                        +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 721 / 800

<- **이전**: [720. IT 경영 관리 핵심 토픽 720번 시험 요약](/studynote/12_it_management/05_security_compliance/720_it_management_core_topic_720_exam_summary/)
**다음**: [722. IT 경영 관리 핵심 토픽 722번 시험 요약](/studynote/12_it_management/05_security_compliance/722_it_management_core_topic_722_exam_summary/) ->

---
