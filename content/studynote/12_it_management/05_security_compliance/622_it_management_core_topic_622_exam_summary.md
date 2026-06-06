---
title: "IT Management Core Topic 622 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019**(거버넌스·관리 목표 40개 + Focus Area), **ISO/IEC 38500**(6원칙: 책임·전략·취득·성과·규율·행위), **ITIL 4**(SVC: 34개 Practice)의 3대 글로벌 프레임워크를 **Balanced Scorecard(재무·고객·내부·학습성장 4관점)**와 **SAMM(Samlu Aligned Maturity Model)**으로 통합하여, IT 투자 대비 **ROI 25~40% 개선** 및 **인시던트 MTTR 60% 단축**을 달성하는 경영과학 체계이다.
> 2. **가치**: 정량적으로 **TCO(Total Cost of Ownership) 30% 절감**, **IT-Business Alignment 성숙도 1단계 향상당 프로젝트 성공률 18% 증가**(Luftman 2023), **컴플라이언스 위반 리스크 80% 감소**(ISO 38500 인증 시), 정성적으로는 **이사회-경영진-IT 3계층 거버넌스 체계 확립**과 **EA(Enterprise Architecture) 기반 의사결정 체계 표준화**를 통한 디지털 트랜스포메이션 거버넌스 확보.
> 3. **판단 포인트**: ① **CoBIT vs ITIL 적용 범위**(거버넌스-관리 vs 서비스 운영) ② **중앙집중형 vs 분산형 거버넌스 모델**(Federal Model vs Centralized COE) ③ **규범적(Normative) vs 정보적(Informative) 프레임워크** 채택 기준 ④ **감사 주체**(내부감사팀 vs 외부 독립감사법인 ISACA) ⑤ **Agile-DevOps 환경**에서의 **Lightweight Governance**(Shift-Left Compliance) 도입 여부 — 최근 **금융권 DORA(2024.1 시행)**, **공공부문 클라우드 이용지침** 등 **규제 컴플라이언스**와 **속도** 간의 트레이드오프가 핵심 의사결정 변수.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 비용센터에서 **전략적 가치 창출의 핵심 엔진**으로의 전환, COVID-19 이후의 **디지털 가속화(Digital Acceleration)**, 그리고 EU의 **Digital Operational Resilience Act(DORA, 2024.1)**, 한국의 **전자금융감독규정**, **개인정보보호법**, **AI기본법(2026.1 시행)** 등 **규제 환경의 급격한 복잡화**로 인해, 전통적인 IT 운영 방식으로는 **① 투자 정당화(Justification), ② 리스크 통제(Risk Control), ③ 가치 실현(Value Realization), ④ 컴플라이언스 증빙(Compliance Evidence)**이라는 4대 경영 과제를 동시에 해결할 수 없게 되었다. 이에 **ISACA의 COBIT 2019**, **ISO/IEC 38500:2015**, **AXELOS의 ITIL 4** 등 글로벌 표준 프레임워크를 통합 적용한 **체계적 IT 거버넌스 및 관리 체계** 수립이 필수 불가결한 경영 인프라로 부상하였다.

특히 한국 정보관리기술사 시험의 622번 토픽은 **IT 전략-거버넌스-포트폴리오-성과-감사**로 이어지는 IT 경영 **전生命周期(Lifecycle) 통합 관리** 능력을 평가하며, 단순 암기가 아닌 **사례 기반 의사결정(예: "갑(甲)은행이 클라우드 전환 시 거버넌스 체계 재설계")** 형식으로 출제된다.

```text
+--------------------------------------------------------------------------+
|              IT 경영 관리 통합 프레임워크 (IT Management Meta-Framework)  |
+--------------------------------------------------------------------------+
|  +--------------+   +--------------+   +--------------+                |
|  |  Strategy    |--->| Governance   |--->|  Management  |--+             |
|  |  Layer       |   |  Layer       |   |  Layer       |  |             |
|  |              |   |              |   |              |  |             |
|  | • IT 전략    |   | • COBIT 2019 |   | • ITIL 4     |  |             |
|  | • EA(FEAF)  |   | • ISO 38500  |   | • DevOps     |  |             |
|  | • SAMM      |   | • IT-Policy  |   | • Agile      |  |             |
|  | • BCM/DR    |   | • Risk Mgt   |   | • SIAM       |  |             |
|  +--------------+   +--------------+   +--------------+  |             |
|         ^                  ^                  ^           |             |
|         |                  |                  |           v             |
|  +------+------------------+------------------+---------------------+  |
|  |              Performance & Compliance Layer                       |  |
|  |  +------------+ +------------+ +------------+ +--------------+    |  |
|  |  |  BSC/KPI   | | Information| |  Risk      | |  Compliance  |    |  |
|  |  |  측정      | | System     | |  Mgmt      | |  (DORA,PIPL) |    |  |
|  |  |            | | Audit      | | (ISO 27005)| |              |    |  |
|  |  +------------+ +------------+ +------------+ +--------------+    |  |
|  +-------------------------------------------------------------------+  |
|                              |                                          |
|                              v                                          |
|                  +----------------------+                               |
|                  |  Value Realization   |                               |
|                  |  (ROI, NPS, EBITDA)  |                               |
|                  +----------------------+                               |
+--------------------------------------------------------------------------+
```

| 시대 구분 | 패러다임 | 핵심 KPI | 거버넌스 성숙도 | 대표 사건 |
|:---:|:---:|:---:|:---:|:---:|
| **Mainframe(1970~)** | Cost Center | 가용률(Uptime), TCO | Level 1: Ad-hoc | Y2K(2000) |
| **Client-Server(1990~)** | Strategic Tool | 시스템 처리량(TPS) | Level 2: Repeatable | ERP 도입 붐 |
| **Mobile-Cloud(2010~)** | Business Partner | TTM, 사용성(UX) | Level 3: Defined | 클라우드 1차 전환 |
| **AI-Digital Twin(2020~)** | **Value Driver** | **EBITDA 기여도, NPV, NPS** | **Level 4~5: Managed->Optimizing** | **DORA, AI 거버넌스** |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **자동차의 계기판, 브레이크, 내비게이션**을 통합한 **자율주행 시스템**과 같다. 가속페달(전략·투자)만 밟으면 사고(컴플라이언스 위반, 프로젝트 실패)가 나고, 브레이크(리스크 통제)만 잡으면 경쟁력(속도)을 잃는다. **COBIT**는 차체의 **CAN 버스 프로토콜**(모든 제어 신호의 통합), **ISO 38500**은 **도로교통법**(거버넌스 원칙), **ITIL 4**은 **정비 매뉴얼**(운영 Practice)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **3계층 거버넌스 구조(3-Layer Governance)**이며, 각 계층은 **RACI Matrix**(Responsible, Accountable, Consulted, Informed)로 책임 소재를 명확히 한다. COBIT 2019의 **Governance System**(40개 Governance/Management Objective)와 **Components of Governance System**(7가지: 프로세스·조직구조·정보흐름·인력·기술·정책·문화)을 **카르노프 모델(Karnov Model)**처럼 **5단계 성숙도**(Incomplete->Initial->Managed->Defined->Optimizing)로 측정·개선한다.

```text
+-------------------------------------------------------------------------+
|        COBIT 2019 Cascading Goals & Components Architecture           |
+-------------------------------------------------------------------------+
|                                                                         |
|  Stakeholder Drivers & Needs (13개)                                    |
|         |                                                               |
|         v                                                               |
|  +--------------------+                                                |
|  | Enterprise Goals   |  (13개: EG01~EG13)                              |
|  | EG01 포트폴리오    |  +--------------------+                         |
|  | EG06 고객서비스    |-->| Alignment Goals    | (13개: AG01~AG13)       |
|  | EG13 디지털혁신    |  +--------------------+                         |
|  +--------------------+         |                                       |
|                                 v                                       |
|  +----------------------------------------------------------+           |
|  |  Governance & Management Objectives (40개)               |           |
|  |  +-------------+  +--------------+  +----------------+  |           |
|  |  | EDM(5개)    |  | APO(14개)    |  | BAI(11개)      |  |           |
|  |  | 01 거버넌스 |  | 전략, 포트폴 |  | 변경, 수용,    |  |           |
|  |  | 프레임워크  |  | 오케스트레이 |  | 프로그램,      |  |           |
|  |  | 설정        |  | 션, 예산,    |  | 솔루션 관리   |  |           |
|  |  |             |  | 인적자원,    |  |                |  |           |
|  |  |             |  | 리스크,보안  |  |                |  |           |
|  |  +-------------+  +--------------+  +----------------+  |           |
|  |  +-------------+  +--------------+                        |           |
|  |  | DSS(6개)    |  | MEA(4개)     |                        |           |
|  |  | 운영, 인시  |  | 성과측정,    |                        |           |
|  |  | 던트, 서비  |  | 내부통제,    |                        |           |
|  |  | 스연속성    |  | 외부감사,    |                        |           |
|  |  |             |  | 컴플라이언스 |                        |           |
|  |  +-------------+  +--------------+                        |           |
|  +----------------------------------------------------------+           |
|         |                                                               |
|         v                                                               |
|  Components of Governance System (7대 구성요소)                        |
|  +---------+ +---------+ +---------+ +---------+ +---------+         |
|  |Process  | |Structure | |Flows    | |People   | |Tech     |         |
|  +---------+ +---------+ +---------+ +---------+ +---------+         |
|  +---------+ +---------+                                              |
|  |Policies | |Culture  |  <- 모든 구성요소는 5단계 성숙도 평가         |
|  +---------+ +---------+                                              |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **EDM( Evaluate, Direct, Monitor)** | 이사회-경영진의 **거버넌스 의사결정** | COBIT EDM01~05: 거버넌스 체계 평가 및 방향 설정. **ISO 38500 6원칙**(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)과 1:1 매핑되며, 분기별 이사회 IT Committee 운영의 표준 모델 제공 |
| **APO(Align, Plan, Organize)** | IT 전략-전사 정렬·계획·조직 | APO01(관리체계), APO04(혁신), APO05(포트폴리오: **NPV/IRR/PI 지표로 우선순위화**), APO12(리스크: **ISO 27005 + NIST SP 800-30** 기반 정성·정량 분석), APO13(보안: **Zero Trust Architecture** 참조 모델) |
| **BAI(Build, Acquire, Implement)** | 솔루션 도입·구축·전환 관리 | BAI01(프로그램관리: **MSP, P3O**), BAI03(투자관리: **TCO 5년 모델**), BAI08(지식관리: **KM Maturity Model**, **Knowledge Graph**), BAI11(프로젝트: **PMBOK 7th + PRINCE2** 병행) |
| **DSS(Deliver, Service, Support)** | IT 서비스 운영·지원 | **ITIL 4 SVS(Service Value System)** 통합. DSS02(서비스요청: **ServiceNow, Jira Service Management**), DSS03(인시던트: **4-우선순위 P1~P4**, **MTTR 목표 SLA**), DSS04(문제관리: **RCA 5 Whys + Ishikawa Fishbone**), DSS05(연속성: **ISO 22301, BCM**), DSS06(보안운영: **SIEM, SOAR**) |
| **MEA(Monitor, Evaluate, Assess)** | 성과·통제·감사·컴플라이언스 | MEA01(성과·모니터링: **BSC 4관점 + OKR**), MEA02(내부통제: **SOX 404, COSO 2013**), MEA03(외부감사: **ISACA CISA 표준**, **K-ISMS** 인증), MEA04(컴플라이언스: **GDPR, PIPL, DORA** 회부 보고 체계) |
| **RACI Matrix** | 40개 목표별 역할 책임 매트릭스 | 1차 책임자(R)->1~2명, 결재권자(A)->1명(중복 금지), 협의자(C), 통보자(I). **RACI vs RASCI vs RACI-VS** 변형 모델(공공부문 표준) |
| **Focus Area(2020~)** | **맞춤형 거버넌스** 적용 | COBIT 2019 신규: DevOps, Risk, Information Security, Privacy, Cloud, Data, Digital Transformation 등 **11개 표준 FA** + **커스텀 FA** 가능. **TOGAF ADM Phase**와 페어링 |

**성숙도 측정 핵심 알고리즘**:
- **CMMI 5단계**: Level 1(Initial, 0~15%) -> Level 2(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 622 / 800

<- **이전**: [621. IT 경영 관리 핵심 토픽 621번 시험 요약](/studynote/12_it_management/05_security_compliance/621_it_management_core_topic_621_exam_summary/)
**다음**: [623. IT 경영 관리 핵심 토픽 623번 시험 요약](/studynote/12_it_management/05_security_compliance/623_it_management_core_topic_623_exam_summary/) ->

---
