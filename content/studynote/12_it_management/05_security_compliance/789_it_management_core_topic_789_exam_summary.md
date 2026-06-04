---
title: "789. IT 경영 관리 핵심 토픽 789번 시험 요약 (IT Management Core Topic 789 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 이사회의 IT 의사결정·감독 체계(EDM: Evaluate-Direct-Monitor)로써, COBIT 2019의 40개 Governance/Management Objective, ISO/IEC 38500의 6대 원칙, ITIL 4의 34개 Practice, 그리고 Three Lines of Defense 모델을 통합하여 Business-IT Alignment를 달성하는 메타-프레임워크이다.
> 2. **가치**: McKinsey Global Institute 분석에 따르면 IT 거버넌스 성숙도 Top quartile 기업은 동일 산업 대비 EBITDA 마진 5~20%p 향상, ISACA 통계 기준 COBIT 기반 거버넌스 도입 후 IT 리스크 사고 30% 감소 및 컴플라이언스 비용 평균 40% 절감, IT 투자 ROI 2.4배 증가 효과를 확인.
> 3. **판단 포인트**: 중앙집중형(Federal/Center-led) vs 분산형(Decentralized) vs 하이브리드(Hybrid/Federated) 거버넌스 모델 중 조직 규모·산업 특성·규제 환경에 따른 최적 모델 선정, COBIT 2019의 Design Factor 11개(Enterprise Strategy, Goals, Risk Profile 등) 기반 거버넌스 시스템 커스터마이징, RACI 매트릭스·RAPID·DACI 의사결정 프레임워크 적용 시 권한 충돌 방지 및 책임 공백 제거.
```

---

## Ⅰ. 개요 및 필요성

정보기술의 기업 핵심 경쟁력화에 따라 IT는 단순 지원 기능을 넘어 사업 전략과 운영의 근본적 토대가 되었으며, 동시에 IT 실패로 인한 비즈니스 리스크(2017년 Equifax 데이터 유출 USD 1.4B 손실, 2018년 Facebook GDPR 위반 EUR 1.2B 과징금) 또한 기하급수적으로 증가하고 있다. 이러한 환경에서 IT 경영 관리(Information Technology Governance & Management)는 이사회·경영진의 IT 관련 의사결정·감독 책임을 명확히 하고, IT 자원의 효율적 활용·리스크 통제·가치 창출을 체계화하는 경영 필수 역량으로 부상하였다.

특히 한국 환경에서는 전자정부법, 개인정보보호법, 정보통신망법, 정보시스템 산업법, 클라우드컴퓨팅법, 데이터산업법, AI기본법 등 20여 개의 IT 관련 법·규제가 중첩되며, 공공부문 DTA(데이터산업법), NIA(한국지능정보사회진흥원) EA 가이드라인, 디지털정부 이행계획 등 정부 주도 표준화 요구가 강화되고 있다. 이에 ISO/IEC 38500(2015 개정), COBIT 2019(ISACA 발표), ITIL 4(AXELOS 2019), ISO/IEC 20000, ISO/IEC 27001, NIST CSF, CMMI 등 국제 표준과 국내 법·제도를 통합한 IT 거버넌스 체계 수립이 요구된다.

기존 IT 관리 패러다임(1990~2000년대)에서는 CIO 중심의 IT 부서 운영, 프로젝트 단위 관리, 기술 중심 의사결정이 주를 이루었으나, 디지털 전환(DX) 시대에는 CEO·이사회 직접 관여, 포트폴리오 단위 투자 관리, 비즈니스 가치 중심 의사결정, 데이터·AI 거버넌스, ESG·사이버보안 통합 거버넌스로 패러다임이 전환되었다. IT 투자 규모 대비 가치 실현 실패율은 여전히 30%(Gartner 2023) 수준이므로, 거버넌스 체계의 정비가 핵심 경영 이슈로 대두된다.

```text
+--------------------------------------------------------------------------+
|              IT 거버넌스 패러다임 전환: 전통 -> 디지털 시대                |
+--------------------------------------------------------------------------+
|                                                                          |
|  [전통 IT 관리 (1990~2010)]          [디지털 거버넌스 (2015~현재)]         |
|                                                                          |
|   CEO/CFO                               Board/CEO (이사회 직속)           |
|       |                                       |                          |
|   +---+---+                              +----+----+                     |
|   |  CIO  |  <- 단일 의사결정            |Governance|  <- 다중 이해관계자    |
|   +---+---+    권자                      | Committee|    거버넌스 위원회    |
|       |                              +----+----+                     |
|   +---+--------+                            |                          |
|   | 프로젝트별  |  <- 단위 관리         +----+-----------+                |
|   | 운영조직    |                      |Strategic Portfolio|              |
|   +------------+                      |  Mgmt(SPM)      |              |
|                                        +----+-----------+                |
|   +----------+  +----------+                |                          |
|   |애플리케이션|  |인프라    |        +-------+--------+                 |
|   |  silo     |  | silo     |        |역량/서비스/    |                 |
|   +----------+  +----------+        |데이터 거버넌스 |                 |
|                                        +----------------+                 |
|                                                                          |
|  - 기술 중심 의사결정                 - 비즈니스 가치·리스크 중심          |
|  - 프로젝트 성공률 30%                - 포트폴리오 성공률 65% (Top Q)     |
|  - 후행적·수동적 통제                 - 실시간·예측적 자동화 통제          |
|  - 부서별 Compliance                  - 전사 GRC 통합 (Governance·Risk·Compliance) |
+--------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스는 기업의 IT 부서를 마치 **항공기의 자동조종장치(Autopilot) + 블랙박스 + 관제탑**을 동시에 갖춘 시스템에 비유할 수 있다. 자동조종장치는 ITIL 4의 서비스 운영(Service Operation), 블랙박스는 COBIT의 모니터링·평가(M&E) 체계, 관제탑은 ISO 38500의 이사회 감독 책임을 의미한다. 이 세 가지가 동시에 작동해야 비행(사업 운영) 중 돌발 상황(사이버 공격·시스템 장애·규제 변경)에 실시간으로 대응할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스 아키텍처는 국제 표준 4대 축(COBIT 2019, ISO/IEC 38500, ITIL 4, ISO/IEC 20000)과 이를 운영하는 거버넌스 시스템(Governance System)으로 구성된다. 각 프레임워크는 고유한 역할과 범위를 가지며 상호 보완적으로 작동한다.

```text
+--------------------------------------------------------------------------+
|                    IT 거버넌스 통합 아키텍처 (4-Layer)                    |
+--------------------------------------------------------------------------+
|                                                                          |
|  +-------------------------------------------------------------------+   |
|  |  Layer 1: GOVERNANCE (전략·감독) - ISO/IEC 38500 + COBIT EDM     |   |
|  |  +--------------------------------------------------------------+ |   |
|  |  | Evaluate -> Direct -> Monitor (반복 사이클)                  | |   |
|  |  | • 책임(Responsibility) • 전략(Strategy) • 인수(Acquisition)| |   |
|  |  | • 성과(Performance) • 적합(Conformance) • 인적(Human)      | |   |
|  |  +--------------------------------------------------------------+ |   |
|  +-------------------------------------------------------------------+   |
|                                  <-> (비즈니스 정렬)                        |
|  +-------------------------------------------------------------------+   |
|  |  Layer 2: MANAGEMENT (관리·조정) - COBIT 2019 + ISO 20000       |   |
|  |  +--------------------------------------------------------------+ |   |
|  |  | 40개 관리 목표:                                            | |   |
|  |  |  • EDM(5) -> APO(14) -> BAI(11) -> DSS(6) -> MEA(4)            | |   |
|  |  |  • Align, Plan, Organize / Build, Acquire, Implement /     | |   |
|  |  |    Deliver, Service, Support / Monitor, Evaluate, Assess    | |   |
|  |  +--------------------------------------------------------------+ |   |
|  +-------------------------------------------------------------------+   |
|                                  <-> (서비스 전달)                          |
|  +-------------------------------------------------------------------+   |
|  |  Layer 3: SERVICE (서비스 운영) - ITIL 4 + DevOps + SRE         |   |
|  |  +--------------------------------------------------------------+ |   |
|  |  | 34개 Practice (General Mgmt 14 + Service Mgmt 17 + Tech 3) | |   |
|  |  |  • Service Value System(SVS): Opportunity->Demand->Value      | |   |
|  |  |  • 4P 모델: People·Product·Partner·Process                  | |   |
|  |  |  • Continual Improvement Model (CSI)                        | |   |
|  |  +--------------------------------------------------------------+ |   |
|  +-------------------------------------------------------------------+   |
|                                  <-> (기술적 실행)                          |
|  +-------------------------------------------------------------------+   |
|  |  Layer 4: TECHNOLOGY (기술·도구) - ISO 27001 + NIST + 클라우드  |   |
|  |  +--------------------------------------------------------------+ |   |
|  |  |  • GRC 플랫폼: SAP GRC, ServiceNow GRC, Archer             | |   |
|  |  |  • ITSM: ServiceNow, Jira Service Mgmt, BMC Remedy         | |   |
|  |  |  • EA: ArchiMate, TOGAF, ARIS                              | |   |
|  |  |  • 모니터링: Splunk, Datadog, Dynatrace (AIOps)            | |   |
|  |  |  • 보안: SIEM, SOAR, Zero Trust Architecture               | |   |
|  |  +--------------------------------------------------------------+ |   |
|  +-------------------------------------------------------------------+   |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/거버넌스 위원회** | 최고 의사결정·감독 (Tier 1) | ISO 38500 EDM 사이클, 전략·리스크·투자 포트폴리오 승인, CIO/CTO/CDO 직속 보고 체계, 분기별 거버넌스 리뷰(GBR) |
| **COBIT 2019 거버넌스 시스템** | 목표-리스크-자원 매핑 체계 | 40개 목표 중 EDM 5개(Governance), 나머지 35개(Management). Design Factor 11개로 조직별 커스터마이징. 목표 연쇄(Goal Cascade): Stakeholder Needs->Enterprise Goals->Alignment Goals->Management Goals |
| **IT Balanced Scorecard(IT-BSC)** | 성과 측정·전략 실행 도구 | Kaplan & Norton 4관점(재무·고객·내부프로세스·학습성장) 기반 IT 버전. 5년간 30~50개 KPI 추적, Strategy Map으로 인과관계 시각화, OKR과 통합 운용 가능 |
| **Three Lines of Defense(3LoD)** | 리스크·통제 책임 분담 | 1st Line(사업부서·IT 운영의 자기 통제), 2nd Line(리스크·컴플라이언스·CISO의 감독), 3rd Line(내부감사·외부감사의 독립적 보증). IIA(Institute of Internal Auditors) 2020 모델 기반 |
| **GRC 통합 플랫폼** | 정책·리스크·컴플라이언스 자동화 | SAP GRC, ServiceNow GRC, RSA Archer, OneTrust. Control Mapping(COBIT↔ISO27001↔NIST↔PCI-DSS) 자동화, Continuous Control Monitoring(CCM), 규제 변경 자동 추적 |
| **IT 포트폴리오 관리(SPM)** | 투자·자원 배분 최적화 | Gartner Magic Quadrant 기반 도구(Planview, Clarity, ServiceNow SPM). 프로젝트·애플리케이션·인프라·서비스 포트폴리오 분류, BAAR(Boost, Accept, Avoid, Retire) 의사결정, TCO·ROI·NPV 분석 |
| **Change Advisory Board(CAB)** | 변경 관리·리스크 통제 | ITIL Change Management 기반. Normal/Emergency/Standard 변경 분류, RFC(Request for Change) 검토, PIR(Post Implementation Review), CI(Configuration Item) 영향도 분석 |

### COBIT 2019의 5개 도메인 및 40개 목표 구조

COBIT 2019는 기존 5개 도메인을 유지하면서 목표(Goal) 단위로 세분화되었다. 각 목표는 Purpose, Practices(40개 목표 × 평균 5~6개 Practice = 약 200+ Activity), Activities, Inputs/Outputs, Metrics를 포함한다.

```text
+----------------------------------------------------------------------+
|        COBIT 2019 도메인 × 40개 목표 (5+14+11+6+4 = 40)             |
+----------+-----------------------------------------------------------+
|  EDM(5)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 789 / 800

<- **이전**: [788. IT 경영 관리 핵심 토픽 788번 시험 요약](/studynote/12_it_management/05_security_compliance/788_it_management_core_topic_788_exam_summary/)
**다음**: [790. IT 경영 관리 핵심 토픽 790번 시험 요약](/studynote/12_it_management/05_security_compliance/790_it_management_core_topic_790_exam_summary/) ->

---
