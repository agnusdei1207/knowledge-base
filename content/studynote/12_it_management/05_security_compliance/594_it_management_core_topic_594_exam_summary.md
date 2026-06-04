+++
title = "594. IT 경영 관리 핵심 토픽 594번 시험 요약 (IT Management Core Topic 594 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 594. IT 경영 관리 핵심 토픽 — 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019 거버넌스 시스템(Governance System)**, **ITIL 4 서비스 가치 시스템(SVS)**, **ISO 38500 이사회 거버넌스 원칙**, **TOGAF ADM**, **Zachman Framework** 등 글로벌 표준 프레임워크를 통합하여, **Strategy->Portfolio->Architecture->Service->Operation->Audit** 6계층으로 IT 자원과 비즈니스 가치를 연결하는 경영 체계이다. 핵심은 **Enabler(37개 COBIT 구성요소)** 를 통한 **Value Creation** 실현과 **Goal Cascade** 메커니즘이다.
> 2. **가치**: COBIT 성숙도 2->5 도달 시 **IT 투자 ROI 25~45% 개선**, ITIL 4 도입 후 **MTTR 60% 단축·서비스 가용성 99.95% 달성**, EA(Enterprise Architecture) 적용 시 **시스템 중복 투자 30~50% 제거·Time-to-Market 40% 단축**, IT 거버넌스 체계 구축 시 **이사회-경영진-현업 간 의사결정 latency 70% 감소**, ISMS 인증 획득 시 **정보보안 사고 발생률 65% 저감** 효과가 보고되고 있다.
> 3. **판단 포인트**: 핵심 트레이드오프는 (a) **집중형(Centralized) vs 분산형(Distributed/Federated) 거버넌스 모델**, (b) **Build vs Buy vs Cloud(SaaS)**, (c) **CapEx vs OpEx 투자 회계**, (d) **Agile-Bimodal vs 전통 Waterfall**, (e) **Risk Appetite 0(zero) vs Risk-Tolerant(허용)** 의 5가지 축이며, 기술사 답안에서는 **RACCI 매트릭스**, **Balanced Scorecard 4관점(재무·고객·내부·학습)**, **TCO/ROI/NPV/IRR** 정량 분석과 함께 **단계적 로드맵(Maturity Roadmap)** 을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경 및 정의

IT 경영 관리(IT Management, IT Governance & Management)는 **1999년 IT 거버넌스 협의회(ITGI, 현 ISACA)** 의 등장 이후, **사이버네틱스·시스템 다이내믹스·정보경제학** 관점에서 기업 IT를 **"전략적 자산(Strategic Asset)"** 으로 재정의하는 경영학문이다. 과거 1970~1990년대 IT 관리는 **데이터 처리(EDP)·MIS·DSS** 단계로 단순 비용센터(Cost Center)였으나, 2000년대 **사브린 조지프(Sarbanes-Oxley Act 2002)** 와 **BASEL II** 등 컴플라이언스 요구로 **통제환경(Control Environment)** 중심으로, 2010년대 **클라우드·모바일·빅데이터** 도입으로 **플랫폼·서비스** 중심으로, 2020년대 **AI·Web3·양자컴퓨팅** 등장으로 **지능형 자동화·자율 거버넌스(Self-Governing IT)** 중심으로 패러다임이 전환되었다.

### 1.2 기술적 도전과제

| 도전과제 | 구체적 현상 | 정량 임팩트 |
| :--- | :--- | :--- |
| **Shadow IT** | 클라우드 SaaS의 무인증 도입 | 글로벌 평균 IT 예산의 **30~40%가 비가시 영역** (Gartner 2024) |
| **Technical Debt** | 레거시 시스템 누적 | Fortune 500 평균 **연 매출의 15~25%** 가 부채 처리 필요 |
| **Cybersecurity Gap** | 랜섬웨어·제로데이 | 평균 침해 대응비용 **USD 4.88M** (IBM 2024) |
| **Compliance Complexity** | GDPR·개인정보보호법·ESG | 컴플라이언스 비용 **연 12% 증가** 추세 |
| **Talent Shortage** | IT 인력 부족 | 한국 IT 인력 부족률 **약 35,000명/년** |
| **Vendor Lock-in** | 하이퍼스케일러 종속 | 클라우드 이전 비용 평균 **전체 예산의 30%** |

### 1.3 IT 경영 관리 5계층 구조도

```text
   +----------------------------------------------------------------------+
   |           Tier 0: 이사회 / 경영진 (Board / Executive)                  |
   |  +------------------------------------------------------------+      |
   |  |  IT 거버넌스 위원회 (Steering Committee) · CDO · CIO · CISO  |      |
   |  |  -- ISO 38500 6원칙: 책임·전략·취득·성과·규율·인간행위 --  |      |
   |  +------------------------------------------------------------+      |
   +------------------------------+---------------------------------------+
                                  |  Cascading Goals
   +------------------------------v---------------------------------------+
   |           Tier 1: IT 전략 및 포트폴리오 (Strategy & Portfolio)         |
   |  +----------------+----------------+--------------------+            |
   |  |  IT 전략맵(ITS)|  IT 포트폴리오  |  투자우선순위(Rank) |            |
   |  |  BMC/CSF 도출  |  BCG 2x2 Matrix|  NPV·IRR·Payback   |            |
   |  +----------------+----------------+--------------------+            |
   +------------------------------+---------------------------------------+
                                  |  Investment Decision
   +------------------------------v---------------------------------------+
   |           Tier 2: 엔터프라이즈 아키텍처 (EA)                            |
   |  +----------+----------+----------+----------+                       |
   |  | Business |   Data   |  App     | Technology|   TOGAF ADM           |
   |  |  Arch.   |  Arch.   |  Arch.   |  Arch.    |   8 Phases           |
   |  +----------+----------+----------+----------+                       |
   |       Zachman 6x6 매트릭스(What·How·Where·Who·When·Why × 5관점)        |
   +------------------------------+---------------------------------------+
                                  |  Architecture Decision
   +------------------------------v---------------------------------------+
   |           Tier 3: IT 서비스 운영 (Service & Operation)                  |
   |  +------------------------------------------------------------+      |
   |  |  ITIL 4 SVS: 34 Practices · Service Value Chain · 7 Guiding |     |
   |  |  Principles · Continual Improvement · SLA/OLA/UC 계층        |     |
   |  +------------------------------------------------------------+      |
   +------------------------------+---------------------------------------+
                                  |  Service Delivery
   +------------------------------v---------------------------------------+
   |           Tier 4: 통제·감리·보안 (Control, Audit, Security)             |
   |  +----------+----------+----------+----------+                       |
   |  |  COBIT   |  ISMS    |  컴플라   |  정보시스 |                       |
   |  |  2019    |  PIPC    |  이언스   |  템감리   |                       |
   |  |  37Obj   |  인증    |  GDPR 등  |  감리법   |                       |
   |  +----------+----------+----------+----------+                       |
   +----------------------------------------------------------------------+
```

### 1.4 기존 패러다임 vs 신 패러다임

- **기존(Traditional)**: IT는 **Cost Center**, **프로젝트 중심(Project-Driven)**, **사일로(Silo)**, **연간 예산(Annual Budgeting)**, **CapEx** 위주의 *Plan-Build-Run* 모델
- **신(New)**: IT는 **Value Driver**, **제품 중심(Product-Centric)**, **플랫폼(Platform)**, **연속 펀딩(Continuous Funding)**, **OpEx** 위주의 *Run-Build-Run* 피드백 루프. **DevOps·SRE·Platform Engineering**·**FinOps**·**GreenOps** 등 **"XOps"** 패러다임 등장

- **📢 섹션 요약 비유**: IT 경영 관리는 **배(선박)** 의 항해와 같다. 이사회는 **선장(의사결정)**, IT 전략은 **항로(Plan)**, EA는 **선체 설계도(Blueprint)**, 서비스 운영은 **기관장·엔진룸(Execution)**, 감리·보안은 **선박 안전검사(Compliance)** 이다. 어느 하나라도 어그러지면 **좌초(침몰)** 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 COBIT 2019 거버넌스 시스템 5개 도메인

```text
   +------------------------------------------------------------------+
   |              COBIT 2019 Governance System Components              |
   |                                                                   |
   |   +--------------+   +--------------+   +--------------+         |
   |   |  Governance   |   |  Management   |   |   Enablers    |         |
   |   |  Objectives   |◄-►|  Objectives   |◄-►|  (37 items)   |         |
   |   |  (EDM 5개)    |   |  (APO·BAI·    |   |  P: 원칙·정책 |         |
   |   |  Evaluate,    |   |   DSS·MEA     |   |  O: 조직구조  |         |
   |   |  Direct,      |   |   4 Domain    |   |  C: 문화·윤리 |         |
   |   |  Monitor)     |   |   ·40 Obj     |   |  I: 정보      |         |
   |   +------+-------+   +------+-------+   |  S: 서비스     |         |
   |          |                  |           |  A: 응용·기술   |         |
   |          v                  v           |  P: 인력·역량   |         |
   |   +---------------------------------+  +--------------+         |
   |   |    Components: Process·Structure |                           |
   |   |    ·People·Skills·Culture·Info   |   Goal Cascade            |
   |   |    ·Services·Infrastructure·Apps |   Needs->Goals->            |
   |   +---------------------------------+   Enablers                |
   +------------------------------------------------------------------+

   EDM : Evaluate, Direct and Monitor  (5 Objectives)
   APO : Align, Plan and Organize       (14 Objectives)
   BAI : Build, Acquire and Implement   (11 Objectives)
   DSS : Deliver, Service and Support    (6  Objectives)
   MEA : Monitor, Evaluate and Assess   (4  Objectives)
```

### 2.2 핵심 구성 요소 및 메커니즘

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회 / IT 거버넌스 위원회** | 최종 책임(E&O), 전략적 의사결정 | **ISO 38500 6원칙** 적용, 분기별 정례 회의, RACCI
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 594 / 800

<- **이전**: [593. IT 경영 관리 핵심 토픽 593번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/593_it_management_core_topic_593_exam_summary/)
**다음**: [595. IT 경영 관리 핵심 토픽 595번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/595_it_management_core_topic_595_exam_summary/) ->

---
