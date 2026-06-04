---
title: "766. IT 경영 관리 핵심 토픽 766번 시험 요약 (IT Management Core Topic 766 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Governance)는 COBIT 2019, ITIL 4, ISO/IEC 38500의 3대 프레임워크를 기반으로, 경영진의 의사결정(DM), 정렬(Align), 계획(Plan), 구축(Build), 운영(Run), 모니터링(Monitor)의 EDM 가치체인(Value Chain)을 통해 IT가 비즈니스 가치를 창출하도록 통제하는 책임·구조·프로세스의 통합 체계임.
> 2. **가치**: McKinsey(2023) 기준 효과적 IT 거버넌스 도입 기업은 디지털 전환 성공률 2.3배, ROI 27% 향상, IT 예산 18~32% 절감, ISO 38500 인증 기업은 정보보안 사고 발생 시 평균 복구비용(MTBF) 41% 감소 효과를 보고함.
> 3. **판단 포인트**: 중앙집중(CoE) vs 분산(Federated) 거버넌스 모델, COBIT의 40개 관리목표(Management Objective)와 RACI 매트릭스 설계, NIST CSF 7-function과의 매핑, 그리고 3 Lines of Defense(3LoD) 모델 적용 시 Risk Appetite Statement(위험선호도) 정량화 수준이 핵심 설계 결정 사항임.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 766번 토픽은 **IT 경영 관리(Information Technology Management)** 의 핵심 영역으로, **IT 거버넌스(Governance)·IT 서비스 관리(Service Management)·IT 전략·IT 성과·IT 위험·IT 투자·IT 포트폴리오·EA(Enterprise Architecture)·BCP/DR** 까지 포괄하는 메가-토픽임. 특히 2018년 이후 발효된 GDPR, 2022년 개정 개인정보보호법, 2023년 EU DORA(Digital Operational Resilience Act), 그리고 2024년 생성형 AI 시대의 책임 있는 AI 거버넌스(RAI: Responsible AI) 규제 강화로 인해 IT 경영의 범위가 "비용 센터"에서 "가치 중심 거버넌스(Value-Driven Governance)"로 패러다임이 전환됨.

과거(1990~2005)에는 **IT 관리가 단순 인프라 운영(Infrastructure Operation)** 위주의 비용 회계 관점이었으나, 코비트(COBIT) 4.0(2005) -> 5.0(2012) -> 2019(2019) -> 2019.1(2023) 진화를 거치며, **이해관계자(Stakeholder) needs -> Goals Cascade -> Management Objectives -> Process Activities** 의 위계적 목표 정렬 메커니즘이 정착됨. 이는 COSO ERM 2017의 위험-전략-성과 통합 프레임워크와도 결합되어, 단순 IT 감사를 넘어 **엔터프라이즈 위험 관리(ERM) 및 ESG 정보공시(CSRD, ISSB S2)** 영역까지 확대되고 있음.

```text
+--------------------------------------------------------------------+
|            IT 경영 관리 핵심 토픽 766 메타-프레임워크                |
+--------------------------------------------------------------------+
|                                                                    |
|   +--------------+  +--------------+  +----------------------+    |
|   |  IT 전략     |  |  IT 거버넌스  |  |  IT 서비스 관리      |    |
|   |  (Strategy)  |-->|  (Governance)|<--|  (ITSM)              |    |
|   | - IS 전략    |  | - COBIT 2019 |  | - ITIL 4             |    |
|   | - ISMS       |  | - ISO 38500  |  | - ISO 20000          |    |
|   +------+-------+  +------+-------+  +----------+-----------+    |
|          |                 |                      |                |
|          +--------+--------+----------+-----------+                |
|                   v                   v                            |
|   +----------------------+  +--------------------------+          |
|   |  IT 포트폴리오 관리  |  |  IT 성과 및 가치 측정    |          |
|   |  (ITPM)              |  |  (IT Performance)         |          |
|   | - MoP / P3O         |  | - Balanced Scorecard     |          |
|   | - FinOps             |  | - KPI/KRI                |          |
|   +----------+-----------+  +------------+-------------+          |
|              |                           |                        |
|              +--------+------------------+                        |
|                       v                                           |
|       +----------------------------------------+                  |
|       |  Enterprise Architecture (EA)          |                  |
|       |  TOGAF 10 / DoDAF / FEA / Zachman      |                  |
|       +-------------+--------------------------+                  |
|                     |                                              |
|                     v                                              |
|   +------------------------------------------------------+        |
|   |  운영 거버넌스 (Operational Governance)               |        |
|   |  - BCP/DR (ISO 22301)  - DevSecOps  - AIOps          |        |
|   |  - Zero Trust (NIST SP 800-207)  - SRE               |        |
|   |  - Responsible AI (NIST AI RMF 1.0)                   |        |
|   +------------------------------------------------------+        |
+--------------------------------------------------------------------+
```

**왜 필요한가?**
- **Deloitte 2022 Global CIO Survey**: CIO의 78%가 "기술 그 자체"보다 "기술의 비즈니스 가치 실현"에 대한 책임을 더 강하게 느낀다고 응답.
- **Gartner 2024**: 기업 IT 예산의 평균 30%는 사업부에 의해, 70%는 IT 조직에 의해 결정되나, **가치 실현률(Value Realization Rate)** 은 평균 35% 미만임.
- **ISO/IEC 38500:2015**는 IT 거버넌스의 6원칙(Evaluate, Direct, Monitor)을 통해 **책임성(Accountability)** 의 보장을 명시하며, **OECD 디지털 경제 정책 권고안(2021)** 과 EU AI Act(2024)에서도 IT 거버넌스 체계의 확보를 규제 요건으로 요구함.
- 국내는 **전자정부법 제46조(정보시스템의 효율적 관리)** 와 **클라우드 컴퓨팅 발전 및 이용자 보호에 관한 법률(클라우드 발전법, 2024)** 에 의해 공공·금융·의료 분야의 IT 거버넌스 체계 의무화가 강화됨.

- **📢 섹션 요약 비유**: IT 경영 관리는 "도시의 종합 교통 시스템"과 같습니다. 도로(인프라), 신호등(정책), 경찰(감사), GPS(측정), 운전자(사용자) 모두가 상호 약속된 규칙에 따라 움직여야 시민(비즈니스)이 원하는 목적지에 정시·안전·경제적으로 도달할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 **상위 메타 구조(Governance Frameworks)**, **중위 운영 구조(Process & Roles)**, **하위 기술 구조(Technologies & Tools)** 의 3-tier 아키텍처로 구성됨. 핵심 메커니즘은 **PDCA 사이클 + 목표 정렬 카스케이드(Goals Cascade) + RACI + 3 LoD(Three Lines of Defense)** 의 결합임.

```text
+----------------------------------------------------------------------+
|  COBIT 2019 Governance System (40 MGOs + 7 Components) Architecture  |
+----------------------------------------------------------------------+
                               |
   +---------------------------v------------------------------+
   |   Stakeholder Concerns (11 Concerns)                    |
   |   ◦ Benefits Realization   ◦ Risk Optimization            |
   |   ◦ Resource Optimization ◦ Transparency                 |
   |   +- 13 Enterprise Goals -> Goal Cascade Mapping -+       |
   +---------------------------+----------------------+       |
                                v                              |
   +--------------------------------------------------+       |
   | 40 Management Objectives (MGOs)                   |       |
   |  EDM(5) : Evaluate, Direct, Monitor                |       |
   |  APO(14): Align, Plan, Organize                     |       |
   |  BAI(11): Build, Acquire, Implement                 |       |
   |  DSS(6) : Deliver, Service, Support                 |       |
   |  MEA(4) : Monitor, Evaluate, Assess                |       |
   +--------+-----------------------------------------+       |
            |                                                    |
            v                                                    |
   +--------------------------------------------------------+   |
   | 7 Components of Governance System                       |   |
   |  +---------+--------+-------+------+-----+-----+-----+  |   |
   |  |Process  |Org Str |Info   |People|Skill|Serv |Tool |  |   |
   |  |Practices|        |Flow   |      |&Comp|ices |s    |  |   |
   |  |(Prac.)  |        |       |      |(CSF)|     |     |  |   |
   |  +----+----+---+----+---+---+--+---+--+--+-----+----+  |   |
   +-------+--------+--------+------+------+----------------+   |
           v        v        v      v      v                      |
   +--------------------------------------------------------+    |
   | Focus Areas (e.g., DevOps, Cybersecurity, Privacy)    |    |
   | Design Factors × 11 -> Tailored Governance System      |    |
   +--------------------------------------------------------+    |
            |                                                    |
            v                                                    |
   +--------------------------------------------------------+    |
   | Maturity Model (CMMI 0~5)  +  Capability (0~5)         |    |
   | Target Capability ≥ Industry Average + Δ               |    |
   +--------------------------------------------------------+    |
            ^                                                    |
            |  Continuous Improvement                            |
   +--------+-----------------------------------------------+   |
   | RACI Matrix (Responsible, Accountable, Consulted,     |   |
   |               Informed)   +  3 Lines of Defense        |   |
   +--------------------------------------------------------+   |
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 최고 거버넌스 의사결정 | 이사회·경영진 책임; ISO 38500의 3원칙 매핑; 사이버보안 위험 appetite 정량화(예: "연간 VaR ≤ 영업이익의 2%") |
| **APO (Align, Plan, Organize)** | 전략-전술 정렬 | TOGAF ADM Phase Preliminary~E 사이클; Capability Map 기반 Gap Analysis; COBIT APO12(위험 관리)와 ISO 31000 매핑 |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축 및 도입 | DevSecOps 파이프라인(SAST/DAST/SCA), CI/CD(GitHub Actions, GitLab), Agile@Scale(SAFe 6.0), IaC(Terraform, Ansible) |
| **DSS (Deliver, Service, Support)** | IT 서비스 운영 | ITIL 4 SVS(Service Value System) 34 Practices, AIOps(Datadog, Dynatrace), ITSM(Jira Service Mgmt, ServiceNow), SLA/SLO/SLI 3-tier |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정 및 감사 | BSC(Balanced Scorecard) 4관점(재무/고객/내부/학습성장), OKR 정렬, 내부감사(IIA Standard 2120), ISAE 3402/3000 보고 |
| **Goals Cascade** | 비즈니스-IT 목표 연결 | 13 Enterprise Goals × 13 Alignment Goals × 40 MGOs = 1,690 매핑; 1:N 다대다 관계를 BPMN 2.0 그래프로 표현 |
| **Design Factors (11개)** | 거버넌스 시스템 맞춤화 | 기업 전략·위험 프로파일·규제 환경·IT 역할·사이즈·M&A 빈도·거버넌스 성숙도 등 입력 -> 우선순위 점수(1~5) 산출 |

**핵심 알고리즘 및 정량 공식:**

1. **IT 투자 ROI 산출 (TCO-TVA 모델)**
   $$ \text{NPV} = \sum_{t=0}^{n} \frac{\text{Benefit}_t - \text{Cost}_t}{(1+r)^t} $$
   - Benefit: 직접·간접·전략적 가치(Brand, Time-to-Market), IT 투자 후 3~5년 누적 Cash Flow.
   - Cost: CapEx(하드웨어·SW 라이선스) + OpEx(운영·인건비·클라우드) + Risk Cost( $P_{\text{breach}} \times L_{\text{breach}}$ ).
   - 적용: 일반 기준 r=8~12%(WACC), IT 전용은 r=10~15%, **Payback Period ≤ 36개월** 권고.

2. **COBIT Capability Level 산출 (PAM 2019)**
   - Process Rating = (PA 1.1 Innitial -> PA 5.1 Optimizing) 중 **Process Attribute Achievement % (PAA%)**.
   - 7개 Process Attribute(PA 1.1~5.2) × 100% 매핑 후 가중 평균.
   - 정량 예: APO12(위험 관리) Capability 3 -> "Defined Process" 수준, 70% PAA 이상 권고.

3. **서비스 가용성 공식 (ITIL 4 Availability Mgmt)**
   $$ \text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} \times 100\% $$
   - Tier-1 시스템 99.99% (Four-Nines, 연간 다운타임 52.6분).
   - Tier-3 시스템 99.9% (연간 8.76시간).
   - SLO 위반 시 **Error Budget Burn Rate** 계산 -> 자동 트래픽 차단(Google SRE 모델).

4. **위험 정량화 (FAIR: Factor Analysis of Information Risk)**
   $$ \text{Annual Loss Exposure} = \text{Threat Event Frequency} \times \text{Vulnerability} \times \text{Primary Loss} $$
   - 예: 랜섬웨어 = 2회/년 × 0.7 × 5억원 = **연 7억원** Risk Exposure.
   - 이를 Risk Appetite Statement(예: "연간 VaR ≤ 3억원")와 비교.

5. **FinOps 비용 최적화 (클라우드 경제성)**
   $$ \text{Unit Economics} = \frac{\text{Total Cloud Spend}}{\text{Active Users} \times \text{Transactions}} $$
   - 예: AWS 비용/MAU = 0.12 USD, 동일 SaaS 대비 30% 절감 가능 시 -> Reserved Instance + Savings Plan 이관.

**3 Lines of Defense (3LoD) 모델**
- **1LoD**: 운영 부서(영업, IT 개발) - 위험 소유·식별·통제 직접 수행 (Control Owner).
- **2LoD**: 위험·컴플라이언스·재무 부서 - 정책 수립·모니터링·자문.
- **3LoD**: 내부감사(IIA) - 독립적 assurance, 이사회 Audit Committee에 보고.
- **2020 IIA Three Lines Model 업데이트** 추가: 6원칙(거버넌스 원칙), 1LoD의 "Specialist" 역할과 "Independent Control Validation" 강조.

-
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 766 / 800

<- **이전**: [765. IT 경영 관리 핵심 토픽 765번 시험 요약](/studynote/12_it_management/05_security_compliance/765_it_management_core_topic_765_exam_summary/)
**다음**: [767. IT 경영 관리 핵심 토픽 767번 시험 요약](/studynote/12_it_management/05_security_compliance/767_it_management_core_topic_767_exam_summary/) ->

---
