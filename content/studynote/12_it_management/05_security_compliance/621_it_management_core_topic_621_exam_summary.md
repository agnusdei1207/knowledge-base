+++
title = "621. IT 경영 관리 핵심 토픽 621번 시험 요약 (IT Management Core Topic 621 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019(40개 거버넌스/관리 목표), ISO/IEC 38500(6원칙), RUP/ITIL v4(34개 practices), ISO 27001:2022(93통제) 프레임워크를 통합하여 **EDM(Evaluate-Direct-Monitor) 사이클**과 **RACI 매트릭스** 기반으로 의사결정 권한을 표준화하고, IT 자산을 Business Value Chain에 정렬시키는 3단계 통제 체계입니다.
> 2. **가치**: McKinsey(2023) 기준成熟 거버넌스 도입 기업은 IT 투자 대비 ROI 23~38% 개선, ISO 38500 인증 기업 평균 **사고 대응 시간 MTTR 47% 단축**, COBIT 기반 성숙도 4단계 이상 도달 시 **프로젝트 실패율 31% -> 8%로 감소**(PMI 2022), 컴플라이언스 비용 약 29% 절감이 입증됩니다.
> 3. **판단 포인트**: 핵심 trade-off는 **(a) 중앙집권적 vs 페더레이션 거버넌스**, **(b) COSO 2013(5요소/17원칙) vs COBIT 2019(40목표) 통제 범위**, **(c) Zero Trust(2020 NIST SP 800-207) vs 경계 기반 방어**, **(d) Build(In-house) vs Buy(SaaS) vs Outsource(클라우드 MSP)** 의사결정이며, 기술사는 RACI 매트릭스와 Risk Appetite Statement로 이를 정량화해야 합니다.

---

## Ⅰ. 개요 및 필요성

**IT 거버넌스(IT Governance)** 란 이사회 및 경영진이 IT를 **조직의 전략·목표·리스크 관리 체계**에 통합하여, 이해관계자(stakeholders)에게 가치를 제공하고 책임(accountability)을 이행하도록 **의사결정·책임·통제 구조**를 설계·운영하는 체계를 말합니다. IT 거버넌스는 단순한 IT 관리를 넘어 **기업지배구조(Corporate Governance)의 하위 체계**로서 법적 책임(예: SOX Act §404, 개인정보보호법 §3, NIS2 Directive 2022/2555)을 다룹니다.

배경이 필요한 이유를 **3가지 기술적 도전**으로 정리하면:

1. **디지털 트랜스포메이션 가속화**: Gartner(2024) 조사에서 **대기업의 78%가 IT 예산의 35% 이상을 클라우드·AI·IoT에 투입**하면서, 기존 컴플라이언스 체계로는 통제 누락이 발생함.
2. **사이버 위협의 정교화**: IBM Cost of a Data Breach Report 2023 기준, **글로벌 평균 침해 비용 4.45M USD**, 한국은 **3.62M USD**로 집계되며, ISO 27001:2022 + Zero Trust 모델을 결합한 통합 거버넌스 없이는 방어가 불가능함.
3. **규제 환경의 글로벌화**: EU AI Act(2024), DORA(2023, 2025.1 시행), 한국 클라우드 보안인증(CSAP), 일본 ISMS의 상호 인정을 위해 **단일 통제 체계**가 필수입니다.

```text
+------------------------------------------------------------------+
|           IT 거버넌스의 3대 프레임워크 통합 구조 (Top-Down)        |
+------------------------------------------------------------------+
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
   +--------------+ +--------------+ +--------------+
   |  ISO 38500   | |  COBIT 2019  | |  ISO 27001   |
   |  (6 Principles)| |  (40 Goals) | |  (93 Controls)|
   |              | |              | |              |
   | • Responsibility| | EDM(5)      | | • A.5-A.8    |
   | • Strategy    | | APO(14)     | |   (조직/인적) |
   | • Acquisition | | BAI(11)     | | • A.8(기술)  |
   | • Performance | | DSS(6)      | | • A.5(물리)  |
   | • Conformance | | MEA(4)      | | • Annex A    |
   | • Human Behav.| | 40 objectives| | (2022 ver.)  |
   +------+-------+ +------+-------+ +------+-------+
          |                |                |
          +----------------+----------------+
                           v
              +--------------------------+
              |   EDM Cycle (PDCA 통합)  |
              | E: Evaluate  (5-10회/년) |
              | D: Direct    (분기별)    |
              | M: Monitor   (월간 KPI)  |
              +------------+-------------+
                           v
              +--------------------------+
              |  Business Value Chain    |
              |  Porter Value Chain과    |
              |  IT-Value Alignment      |
              |  (SAM/SoA 기반)          |
              +--------------------------+
```

기존(Before 2010)에는 **"IT 부서가 기술만 관리"**하는 수직적 구조였으나, 현재(2020~)는 **이사회-CIO-CISO-CDAO 4계층 RACI 모델**로 진화했습니다. 한국은 2021년 데이터 산업법, 2022년 개인정보보호법 개정으로 **데이터 거버넌스**가 IT 거버넌스와 결합되는 **통합 거버넌스(Integrated Governance)** 추세입니다.

- **📢 섹션 요약 비유**: IT 거버넌스는 **"건물의 소방·전기·소방·방재 통합 관제 시스템"**과 같습니다. 개별 장비(서버, 네트워크, 애플리케이션)만 관리하는 게 아니라, **화재 감지->대피 경로->소화 설비->소방서 통보**까지 **3계층(예방-탐지-대응)을 표준화**하여 건물 전체의 안전을 보장하는 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 핵심 아키텍처는 **4계층 의사결정 구조**와 **3대 통제 영역**으로 구성됩니다.

```text
+------------------------------------------------------------------+
|  IT 거버넌스 4계층 의사결정 아키텍처 (RACI × EDM)                |
+------------------------------------------------------------------+
Level 1: 전략 계층 (Strategic - 연 4~12회)
+--------------------------------------------------------------+
|  Board of Directors / steering Committee                      |
|  책임: ISO 38500 6원칙 준수를 통한 의사결정 (EDM 5개 목표)    |
|  KPI: ROIT, Risk Appetite Index, Strategic Alignment Score  |
|  도구: COBIT 2019 EDM01~EDM05                                |
+-------------------------+------------------------------------+
                          | 위임
Level 2: 전술 계층 (Tactical - 월 1~분기 1)
+-------------------------v------------------------------------+
|  CIO / CISO / CDO / CAE (4인 C-Suite)                       |
|  책임: APO(Align, Plan, Organize) - 14개 관리 목표            |
|  RACI 매트릭스 작성·갱신 (Responsible, Accountable,         |
|  Consulted, Informed)                                        |
|  도구: ISO 27001 ISMS, COBIT 2019 APO12(위험 관리)          |
+-------------------------+------------------------------------+
                          | 실행 위임
Level 3: 운영 계층 (Operational - 일/주 단위)
+-------------------------v------------------------------------+
|  IT 운영팀 / SOC / GRC 플랫폼 / ITSM Tool (ServiceNow 등)   |
|  책임: BAI(Build, Acquire, Implement) - 11목표              |
|         DSS(Deliver, Service, Support) - 6목표               |
|  도구: ITIL 4 Service Value Chain, SLA 99.95%               |
+-------------------------+------------------------------------+
                          | 통제
Level 4: 측정 계층 (Monitoring - 실시간/월간)
+-------------------------v------------------------------------+
|  Internal Audit / GRC 자동화 (RSA Archer, SAP GRC 등)       |
|  책임: MEA(Monitor, Evaluate, Assess) - 4목표               |
|  도구: COBIT 2019 MEA01~MEA04, KCI(Key Control Indicator)    |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Core Model** | 40개 거버넌스·관리 목표의 표준화 | EDM 5개 + APO 14 + BAI 11 + DSS 6 + MEA 4 = **총 40 목표**, 각 목표는 **Process Purpose + Practices(40개 이상) + Activities**로 구성. **Focus Area**(예: DevOps, Risk, Cybersecurity)와 **Design Factors 11개**로 조직 맞춤 커스터마이징 |
| **ISO/IEC 38500:2015** | IT 거버넌스 6원칙 프레임워크 | ① Responsibility ② Strategy ③ Acquisition ④ Performance ⑤ Conformance ⑥ Human Behavior. **Plan->Acquire->Implement->Monitor->Evaluate** 5단계 모델, 30개 ISO/IEC 38500-2 통제 |
| **ISO 27001:2022** | ISMS(정보보안경영체계) 인증 체계 | **Annex A 93통제 항목**(2022: 114->93개로 통합·재편), 4그룹(조직 37/인적 8/물리 14/기술 34). **Statement of Applicability(SoA)** 작성 의무, **Plan-Do-Check-Act(PDCA)** 기반 |
| **RACI Matrix** | 의사결정 권한의 4단계 분류 | **R**(Responsible-실행), **A**(Accountable-책임, 1명), **C**(Consulted-자문), **I**(Informed-통보). 한국 공공부문 행정안전부 e-정부 표준 RACI 가이드(2020) 적용 |
| **EDM Cycle** | Evaluate->Direct->Monitor | COBIT 2019의 핵심 사이클. **Evaluate**(5~10회/년, 거버넌스 프레임워크 평가), **Direct**(분기별, 의사결정 위임), **Monitor**(월간, KPI/CSF 측정). 평균 90일 주기 |

**핵심 알고리즘 및 정량 지표**:

- **Strategic Alignment Score (SAM)**: `SAM = (IT Strategy ∩ Business Strategy 항목 수) / (Business Strategy 전체 항목 수) × 100`. 보통 70% 이상이면 우수로 평가(Weill & Ross, MIT CISR).
- **Risk Appetite Index (RAI)**: 연간 손실 가능성의 0.1~1.5% 범위 설정. Basel III + COBIT 2019 APO12 기반.
- **COBIT Maturity Model (5단계)**: ① Initial(임의) ② Managed(반복) ③ Defined(표준화) ④ Quantitatively Managed(정량) ⑤ Optimizing(최적화). 목표는 일반적으로 **Level 3~4**이며, 5단계 도달은 전체 5% 미만.

- **📢 섹션 요약 비유**: 이 4계층 구조는 **"비행기의 Cockpit-Pilot-Autopilot-블랙박스 시스템"**과 같습니다. Cockpit(이사회)이 6원칙으로 방향을 정하고, Pilot(CIO/CISO)이 비행 계획(RACI)을 세우며, Autopilot(운영팀)이 자동 비행(SLA 99.95%)을 수행하고, 블랙박스(내부감사)가 모든 데이터를 기록해 사고 시 분석(MEA)할 수 있게 합니다.

---

## Ⅲ. 비교 및 연결

IT 거버넌스 관련 프레임워크는 상호 보완적이지만 적용 범위와 목적이 다릅니다.

| 구분 | **COBIT 2019** | **ITIL 4 (2019)** | **ISO 27001:2022** | **PMBOK 7 (2021)** | **COSO 2013** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스 + 관리 통합 | IT 서비스 운영 최적화 | 정보보안 ISMS | 프로젝트 관리 | 기업 내부통제 |
| **구조** | 40 목표 (EDM+4도메인) | 34 Practices + SVS | Annex A 93 통제 | 8 Performance Domains + 12 Principles | 5 Components / 17 Principles |
| **대상** | 이사회 + CIO + 감사 | IT 운영/서비스 매니저 | CISO + ISMS 담당 | PMO + 프로젝트 매니저 | CFO + 내부감사 |
| **인증** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | ISO 27001 Lead Auditor | PMP/PfMP | COSO Internal Cert |
| **강점** | 거버넌스-관리 통합, EDM 명확 | 서비스 가치 사슬(Value Chain) | 글로벌 보안 표준, 법정 필수 | 원칙 기반(원리 12개) | 재무 통제, SOX 호환 |
| **약점** | 구현 복잡, 도구 의존 | 거버넌스 결여 (단독 사용 X) | 기술 통제 약함 | 프로젝트 종료 후 운영 공백 | IT 영역 한정 |
| **상호보완** | ISO 27001 + PMBOK과 매핑 | COBIT DSS06 매핑 | COBIT APO13(보안) | COBIT BAI01(프로그램) | COBIT MEA03(컴플라이언스) |
| **한국 도입률** | 공공 47%, 금융 62% (2023) | 금융 78%, 통신 71% | 전 공공
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 621 / 800

<- **이전**: [620. IT 경영 관리 핵심 토픽 620번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/620_it_management_core_topic_620_exam_summary/)
**다음**: [622. IT 경영 관리 핵심 토픽 622번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/622_it_management_core_topic_622_exam_summary/) ->

---
