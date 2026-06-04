---
title: "456. IT 경영 관리 핵심 토픽 456번 시험 요약 (IT Management Core Topic 456 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 456. IT 거버넌스 및 정보화 사업 성과관리 (IT Governance & Informatization Project Performance Management)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019(Governance & Management Objectives 40개)와 ITIL 4(Service Value System 34개 Practice)의 통합 거버넌스 체계 하에서, 정보화 사업의 착수·진행·종료 전 과정을 PMBOK 7th의 8개 Performance Domain과 연계하여 투자 대비 성과(ROI, NPV, Payback Period)를 객관적으로 측정·평가하는 경영 통제 프레임워크임.
> 2. **가치**: 체계적 거버넌스 도입 시 IT 투자 수익률(ROIT) 평균 25% 이상 향상, 정보화 사업 실패율 60%->20%로 절감, 주요 리스크(일정·품질·보안·예산) 사전 식별률 85% 이상 확보, ISO 38500·ISMS-P·ESG 공시 등 다중 컴플라이언스 동시 충족.
> 3. **판단 포인트**: 중앙집중형(CoE, Center of Excellence) vs 분산형(Federated) 거버넌스 모델 선택, COBIT의 Design Factor 11개(기업전략, 위험도, 컴플라이언스, IT 이슈, 위협, 기술 도입 난이도 등)에 따른 Tailoring 전략, Agile/DevOps 환경에서의 거버넌스 Agile(Agile Governance) 적용 여부.

---

## Ⅰ. 개요 및 필요성

정보화 사업의 대형화·복합화에 따라 IT 부서의 단순 비용 센터(Cost Center)에서 가치 창출 센터(Value Center)로의 역할 전환이 요구됨. 그러나 2023년 한국정보화진흥원(KAIT) 통계에 따르면 전체 공공·민간 정보화 사업 중 약 58%가 초기 계획 대비 30% 이상의 예산 초과 또는 6개월 이상의 일정 지연을 경험하고 있으며, 이 중 32%는 사업 종료 후에도 ROI 미측정 상태로 방치되고 있음.

이러한 문제의 근본 원인은 **IT 거버넌스 부재**, **성과 측정의 주관성**, **이해관계자(Stakeholder) 간 정렬 실패**의 3가지로 귀결됨. 전통적 IT 관리는 기술 중심의 하향식(Top-down) 통제에 머물렀으나, 디지털 전환(DX, Digital Transformation) 시대에는 데이터 기반의 양방향 거버넌스와 사업 단위별 수익성·리스크·준법성 통합 관리가 필수적임.

```text
+------------------------------------------------------------------+
|        IT 거버넌스 3축 통합 프레임워크 (3-Layer Governance)      |
|                                                                  |
|   +--------------------------------------------------------+    |
|   |  1층: 전략 거버넌스 (Strategic Governance)             |    |
|   |  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  |    |
|   |  • IT 전략-사업 전략 정렬(Strategic Alignment)         |    |
|   |  • IT 투자 포트폴리오 관리(IT Portfolio)                |    |
|   |  • EA(Enterprise Architecture) 기반 로드맵             |    |
|   |  • 거버넌스 위원회: 이사회 -> IT steering Committee     |    |
|   +--------------------------------------------------------+    |
|                          v^ 연계                                |
|   +--------------------------------------------------------+    |
|   |  2층: 운영 거버넌스 (Operational Governance)           |    |
|   |  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  |    |
|   |  • COBIT 2019 EDM(평가·지휘·모니터) 4개 Process        |    |
|   |  • ITIL 4 SVS 7대 원칙 + 34 Practice 운영              |    |
|   |  • 정보화 사업 단계별 관리(착수/계획/실행/종료)         |    |
|   |  • SLA/SLM/OLA 서비스 수준 관리                        |    |
|   +--------------------------------------------------------+    |
|                          v^ 연계                                |
|   +--------------------------------------------------------+    |
|   |  3층: 통제 거버넌스 (Control Governance)               |    |
|   |  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  |    |
|   |  • ISMS-P, ISO 27001, PIMS 인증 통제                  |    |
|   |  • 위험 관리(ISO 31000, NIST CSF)                     |    |
|   |  • 컴플라이언스: 개인정보보호법, 클라우드이용보호지침  |    |
|   |  • 내부 통제: COSO 2013, SOX IT-GC                    |    |
|   +--------------------------------------------------------+    |
|                                                                  |
|  [지원 레이어] BCM(업무연속성관리) + GRC(거버넌스·리스크·컴플)    |
+------------------------------------------------------------------+
```

**패러다임 비교**: 과거(2010년 이전) IT 관리는 ITIL v3의 26개 Process 중심의 운영 효율성에 집중했다면, 현재는 COBIT 2019의 40개 Governance/Management Objective에 기반해 **Value Creation -> Risk Optimization -> Resource Optimization**의 균형적 목표를 추구함. 특히 클라우드·AI·데이터 거버넌스가 추가되면서 단순 IT 서비스 관리를 넘어 **데이터 거버넌스**(DAMA-DMBOK 2.0)와 **AI 거버넌스**(NIST AI RMF 1.0, 2023) 영역까지 확장됨.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 3층 교통 체계**와 같습니다. 1층(전략 거버넌스)은 도시总体规划·간선도로, 2층(운영 거버넌스)은 시내 교통 신호 체계, 3층(통제 거버넌스)은 안전 요원·CCTV입니다. 어느 한 층만 있어도 도시 전체가 마비됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019의 **Governance System** 구조는 5개 도메인(EDM·APO·BAI·DSS·MEA) 40개 Objective로 구성되며, 이를 ITIL 4의 **Service Value Chain**(Plan->Engage->Design & Transition->Obtain/Build->Deliver & Support)의 34 Practice와 1:1 또는 N:1로 매핑 가능함. PMBOK 7th Edition은 8개 Performance Domain(Stakeholder·Team·Development Approach·Planning·Project Work·Delivery·Measurement·Uncertainty)을 통해 프로젝트 단위 거버넌스를 보완함.

```text
+----------------------------------------------------------------------+
|            COBIT 2019 ↔ ITIL 4 ↔ PMBOK 7 매핑 아키텍처              |
|                                                                      |
|   +-----------------+  +-----------------+  +-----------------+    |
|   |  COBIT 2019     |  |   ITIL 4        |  |   PMBOK 7       |    |
|   |  (5 Domains)    |  |  (34 Practice)  |  |  (8 Domain)     |    |
|   |  40 Objective   |  |                 |  |  12 Principles   |    |
|   +--------+--------+  +--------+--------+  +--------+--------+    |
|            |                   |                   |                 |
|            +-------------------+-------------------+                 |
|                                v                                     |
|         +------------------------------------------+                |
|         |      통합 거버넌스 핵심 메커니즘           |                |
|         |                                          |                |
|         |  ① Cascade Goals(BSC 4관점)              |                |
|         |     재무->고객->내부프로세스->학습성장       |                |
|         |                                          |                |
|         |  ② Design Factor 11개 분석               |                |
|         |     -> 우선순위 Tailored 시스템 도출       |                |
|         |                                          |                |
|         |  ③ RACI Matrix(Responsible·Accountable   |                |
|         |    ·Consulted·Informed) 명확화            |                |
|         |                                          |                |
|         |  ④ Capability/Maturity 평가               |                |
|         |     (PAM: Process Assessment Model)       |                |
|         |     Level 0(Incomplete)~5(Optimizing)     |                |
|         +------------------------------------------+                |
|                                                                      |
|   [성과 측정 지표 KPI 체계]                                          |
|   - 전략: ROIT, Strategic Alignment Index                            |
|   - 운영: SLA 달성률(%), MTTR(평균복구시간), MTBF(평균고장간격)     |
|   - 재무: IT 예산 대비 매출(%), Cost per Transaction                |
|   - 보안: 보안사고 건수, 취약점 평균 조치시간                       |
|   - 품질: 결함밀도(Defect Density), 사용자 만족도(CSAT)             |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 EDM** (Evaluate·Direct·Monitor) | 거버넌스 의사결정 | 이사회/IT 위원회 수준에서 목표 설정, 자원 배분, 성과 모니터링의 3단계 사이클. EDM01(거버넌스 체계 수립), EDM02(이익 실현 보장), EDM03(리스크 최적화), EDM04(자원 최적화) |
| **APO** (Align·Plan·Organize) | 전략 정렬 및 계획 | APO01~14까지 14개 Objective로 전략-포트폴리오-아키텍처-혁신-예산·인력·공급업체·품질·리스크·보안 통합 관리. BI(비즈니스 인텔리전스) 기반 의사결정 지원 |
| **BAI** (Build·Acquire·Implement) | 솔루션 도입·구축 | BAI01~11로 프로그램/프로젝트 관리, 솔루션 설계, 변경·릴리스·전환·수용·구성·자산·지식·운영 도입 관리. DevOps 파이프라인 거버넌스 포함 |
| **DSS** (Deliver·Service·Support) | 서비스 운영·지원 | DSS01~06으로 운영·인시던트·문제·연속성·서비스 요청·보안 서비스 운영. ITSM 도구(ServiceNow, Jira Service Management)와 직접 연동 |
| **MEA** (Monitor·Evaluate·Assess) | 성과 측정·평가 | MEA01~04로 성과·내부통제·컴플라이언스·목표 모니터링. KPI 대시보드, GRC 플랫폼(SAP GRC, Archer) 통합 |
| **ITIL 4 SVS** (Service Value System) | 가치 공동창조 | 7대 원칙(Focus on Value, Start Where You Are, Progress Iteratively, etc.) + Opportunity/Demand -> Value 확인. Service Value Chain 6단계 Activity |
| **PMBOK 7 Performance Domain** | 프로젝트 거버넌스 | 8개 Domain 중 Team·Development Approach가 Agile/Scrum과 연계. 12 Principles 중 "Steward stewardship", "Build shared understanding", "Tailor" 강조 |
| **RACI + Risk Register** | 책임·리스크 가시화 | 모든 Objective별 책임자 명확화 + ISO 31000 기반 위험 등록부(Likelihood 1~5 × Impact 1~5 = Risk Score) 운영 |

**핵심 알고리즘/공식**:

1. **IT 투자 수익률(ROIT)**: `ROIT = (사업 수익 - IT 투자 비용) / IT 투자 비용 × 100`. 일반적으로 3년 누적 ROIT가 150% 이상이면 성공, 100% 미만이면 재검토 대상.
2. **TCO(Total Cost of Ownership)**: `TCO = 직접비(하드웨어+소프트웨어+인건비) + 간접비(다운타임+교육+전환비)`. 클라우드 환경에서는 OpEx 전환율과 Reserved Instance 활용도를 TCO 계산에 반영.
3. **Maturity Level 산정(CMMI/COPM)**: `Maturity = Σ(Process Area 점수 × 가중치) / 가중치 합`. COBIT PAM은 0~5점 척도(0:불완전, 1:초기, 2:관리, 3:정의, 4:정량적, 5:최적화).
4. **SLA 가용성(Availability)**: `Availability = (MTBF / (MTBF + MTTR)) × 100`. Tier III 데이터센터는 99.982%(연 1.6시간 다운 허용), Tier IV는 99.995%(연 26분 다운 허용).
5. **NPV(순현재가치)**: `NPV = Σ[CFt / (1+r)^t] - 초기투자`. 할인율(r)은 WACC 또는 hurdle rate 사용. NPV > 0일 때 사업 추진 권고.

- **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 456 / 800

<- **이전**: [455. IT 경영 관리 핵심 토픽 455번 시험 요약](/studynote/12_it_management/05_security_compliance/455_it_management_core_topic_455_exam_summary/)
**다음**: [457. IT 경영 관리 핵심 토픽 457번 시험 요약](/studynote/12_it_management/05_security_compliance/457_it_management_core_topic_457_exam_summary/) ->

---
