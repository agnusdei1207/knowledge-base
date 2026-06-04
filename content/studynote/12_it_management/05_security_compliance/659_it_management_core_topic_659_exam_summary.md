---
title: "659. IT 경영 관리 핵심 토픽 659번 시험 요약 (IT Management Core Topic 659 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(IT Management)는 **COBIT 2019(40개 관리목표), ISO/IEC 38500(거버넌스 6원칙), ITIL 4(34 Practices, SVS), PMBOK 7th(12 Principles · 8 Performance Domains), DAMA-DMBOK, NIST CSF** 등 다중 프레임워크를 **Business Strategy ↔ IT Strategy ↔ IT Operation**의 3축 정렬(Strategic Alignment)로 통합하는 경영 체계이며, 2024년 이후에는 **AI 거버넌스(NIST AI RMF, EU AI Act), 제로 트러스트, Green IT/ESG, 데이터 메시**가 핵심 확장으로 부상하고 있다.
> 2. **가치**: 정량적으로는 **IT 투자 ROI 20~35% 개선**(McKinsey Digital Survey), **인시던트 MTTR 60% 단축**(PagerDuty 2023), **프로젝트 성공률 2.5배 향상**(PMI 2021 Pulse of Profession)이며, 정성적으로는 **이사회-경영진-IT의 의사결정 투명성, 규제 준수(개인정보보호법·ISMS-P), 디지털 전환 경쟁력** 확보가 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) 중앙집중 vs 분산 거버넌스(Federated COBIT)**, **(b) Agile vs Plan-driven 개발문화**(DevOps + ITIL 4 SVS의 통합), **(c) Build vs Buy vs Cloud**(TCO 3~5년 분석), **(d) 데이터 중앙집중(Lakehouse) vs 도메인 자율(데이터 메시)**, **(e) 보안 Usability vs Zero Trust 엄격성**이며, 기술사 판단은 **Enterprise Context(규모·산업·규제) -> Design Factor 매핑 -> Capability Level 목표 설정** 순으로 진행한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 659번(과목: IT 경영 관리) 영역은 단순히 "IT를 잘 운영하는" 수준을 넘어, **기업 거버넌스의 한 축으로서 IT를 정렬·측정·감독하는 경영 통제 체계**를 다룬다. 1990년대 후반 Y2K 문제, 2000년대 SOX법(Sarbanes-Oxley Act Section 404), 2010년대 클라우드 전환, 2020년대 생성형 AI/제로트러스트, 2024년 EU AI Act 발효로 이어지는 흐름 속에서 IT 경영 관리의 패러다임은 **"Cost Center" -> "Business Enabler" -> "Strategic Differentiator" -> "Trust & Risk Managed Asset"**로 진화해 왔다.

특히 한국 환경에서는 **개인정보보호법(2011, 2023 전면개정), 정보통신망법, 클라우드컴퓨팅법(2021.9. 시행), ISMS-P(정보보호 및 개인정보보호 관리체계), 전자금융감독규정, AI 기본법(2025.1. 시행)** 등 규제 강도가 매년 강화되고 있어, IT 경영 관리 체계 부재는 곧 **과태료·과징금·신용등급 하락·입찰 제한**으로 직결된다. McKinsey(2023)에 따르면 글로벌 기업의 70% 이상이 디지털 전환을 시도했으나 **End-to-End 거버넌스 부재로 35%만 기대효과를 실현**한 것으로 나타난다.

```text
[ IT 경영 관리 3축 정렬(Strategic Alignment) 통합 아키텍처 ]

   +--------------------------------------------------------------+
   |           Business Strategy (경영 전략)                       |
   |   ◦ Porter Value Chain  ◦ BCG/GE Matrix  ◦ Blue Ocean         |
   |   ◦ ESG·DE&I·Digital  ◦ Revenue Model Innovation            |
   +--------------------+-----------------------------------------+
                        | ^ (Downward : 전략·예산·KPI)
                        | v (Upward   : 성과·리스크·컴플라이언스 보고)
   +--------------------+-----------------------------------------+
   |           IT Strategy (정보기술 전략)                          |
   |   ◦ Ward & Peppard IS/IT Planning                            |
   |   ◦ Henderson-Venkatraman SAM (Strategic Alignment Model)   |
   |   ◦ Luftman SAMM (Strategic Alignment Maturity Model)       |
   |   ◦ McFarlan Strategic Grid                                  |
   +--------------------+-----------------------------------------+
                        | ^ (Application Portfolio·EA·표준)
                        | v (서비스·데이터·플랫폼)
   +--------------------+-----------------------------------------+
   |           IT Operation (정보기술 운영)                        |
   |   ◦ ITIL 4 SVS (Service Value System)                        |
   |   ◦ DevOps/Platform Engineering  ◦ SRE                       |
   |   ◦ SIAM (멀티 벤더 통합)  ◦ FinOps (클라우드 비용)          |
   +--------------------------------------------------------------+
                          |
        +-----------------+-----------------+
        v                 v                 v
   +---------+       +----------+      +----------+
   |Govern-  |       |  Risk &  |      |Resource  |
   |ance &   |       |Security  |      |& Perfor- |
   |Audit    |       |          |      |mance     |
   |(COBIT/  |       |(ISO27001/|      |(ITIL/    |
   |ISO38500)|       |NIST CSF/ |      |PMBOK/    |
   |         |       |Zero Trust|      |Earned    |
   |         |       |/ISMS-P)  |      |Value)    |
   +---------+       +----------+      +----------+
```

**왜 필요한가 (Old vs New Paradigm 비교)**:

| 시대 | Old Paradigm (1990~2010) | New Paradigm (2020~현재) |
| :--- | :--- | :--- |
| **IT 인식** | 비용센터(Cost Center), 지원기능 | 사업동인(Business Driver), 전략자산 |
| **거버넌스** | CIO 독점적 결정, 사후 통제 | 이사회-경영진-3 Lines of Defense 모델, 실시간 Risk Posture |
| **아키텍처** | 모놀리식(On-Premise), Waterfall | 클라우드 네이티브, 마이크로서비스, 하이브리드 |
| **데이터** | RDBMS 단일, ETL 배치 | Data Lakehouse(Iceberg/Delta), 스트리밍(Kafka), 데이터 메시 |
| **보안** | Castle-and-Moat(내부신뢰, 외부차단) | Zero Trust(Never Trust, Always Verify), SASE/SSE |
| **프로젝트** | Plan-driven, 연 1회 Port. Review | Agile/Scrum, Continuous Delivery, OKR+Funding |
| **성능 측정** | Uptime, 응답시간(SIL0~2) | NPS, Value Stream Metrics, DORA 4 Keys, FinOps |
| **규제** | SOX, ISO 27001 | GDPR, EU AI Act, AI 기본법, DORA(금융), ISMS-P |

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 '통합 계기판(클러스터)'**과 같다. 엔진(IT Operation), 핸들·엔진제어(IT Strategy), 네비게이션(Business Strategy) 세 요소를 하나의 계기판으로 통합해 보여주지 않으면, 운전자는 속도·연료·엔진온도·타이어 공기압을 따로따로 확인할 수밖에 없다. COBIT/ISO 38500이 그 계기판의 통합 표준이라고 보면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 핵심 레이어는 **(1) IT 거버넌스·컴플라이언스, (2) IT 전략·포트폴리오, (3) IT 서비스·운영, (4) IT 프로젝트·프로그램, (5) 데이터·보안·신기술**이다. 이 레이어는 독립적이지 않고 **상호 Feed-forward / Feedback** 관계를 갖는다.

```text
[ IT 경영 관리 5-Layer Core Architecture & 핵심 프레임워크 ]

  +--------------------------------------------------------------+
  | L1. IT 거버넌스 (Governance, Risk, Compliance - GRC)         |
  |   +-------------+  +-------------+  +------------------+    |
  |   | COBIT 2019  |  |ISO/IEC 38500|  | 3 Lines of       |    |
  |   | - 40 Mgt Obj|  | - 6 Principles| |   Defense Model  |    |
  |   | - 11 Design |  | - Evaluate- |  | 1) 사업부        |    |
  |   |   Factors   |  |   Direct-   |  | 2) IT·Risk·컴플  |    |
  |   | - Goal Casc.|  |   Monitor   |  | 3) 내부감사·외감 |    |
  |   +-------------+  +-------------+  +------------------+    |
  +--------------------------+-----------------------------------+
                             | (전략·KPI·Risk 하향, 성과·예외 상향)
  +--------------------------+-----------------------------------+
  | L2. IT 전략·포트폴리오 (Strategy & Portfolio)                |
  |   ◦ Ward & Peppard : 외부환경(PEST) + 내부역량(Value Chain) |
  |   ◦ SAM(Henderson-Venkatraman) 4관점 정렬                   |
  |     - Business Strategy ↔ IT Strategy                        |
  |     - Business Org   ↔ IT Org                                |
  |     - Business Process ↔ IS Architecture                     |
  |   ◦ McFarlan Strategic Grid (Operation/Support/Factory/Strat)|
  |   ◦ EA(Enterprise Architecture) : TOGAF ADM / Zachman        |
  |   ◦ IT 투자 평가 : NPV, IRR, TCO, Real Options, CBA         |
  +--------------------------+-----------------------------------+
                             | (Application·Data·Infra 요구사항)
  +--------------------------+-----------------------------------+
  | L3. IT 서비스·운영 (Service & Operation - ITSM)              |
  |   +-----------------------------------------------------+   |
  |   | ITIL 4 Service Value System (SVS)                   |   |
  |   |  - Opportunity/Demand -> Value -> Value Co-Creation   |   |
  |   |  - Guiding Principles (7개) : Focus on Value, Start  |   |
  |   |    Where You Are, Progress Iteratively, etc.         |   |
  |   |  - 34 Practices (General, Service, Technical Mgmt)  |   |
  |   |  - 4 Dimensions : Org/People, Information, Partner, |   |
  |   |    Value Streams/Processes, Technology              |   |
  |   +-----------------------------------------------------+   |
  |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 659 / 800

<- **이전**: [658. IT 경영 관리 핵심 토픽 658번 시험 요약](/studynote/12_it_management/05_security_compliance/658_it_management_core_topic_658_exam_summary/)
**다음**: [660. IT 경영 관리 핵심 토픽 660번 시험 요약](/studynote/12_it_management/05_security_compliance/660_it_management_core_topic_660_exam_summary/) ->

---
