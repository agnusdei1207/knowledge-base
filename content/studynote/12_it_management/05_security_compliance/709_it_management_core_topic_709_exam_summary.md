---
title: "709. IT 경영 관리 핵심 토픽 709번 시험 요약 (IT Management Core Topic 709 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019**의 40개 거버넌스/관리 목적과 **ISO/IEC 38500**의 6대 원칙(책임·전략·인수·성과·적합·인적행위)을 최상위 통제 구조로 삼고, **ITIL 4 SVS**(서비스 가치 시스템), **PMBOK 7**의 8개 성능 도메인, **TOGAF ADM**을 실무 운영·프로젝트·아키텍처 계층에 통합하여, **IT-Business Alignment -> Value Realization -> Risk Optimization**의闭环(closed-loop)를 구현하는 경영 체계이다.
> 2. **가치**: Gartner(2023) 기준 COBIT 기반 성숙도 3->5 도달 시 **프로젝트 성공률 42%->71%**, ISO 27001 인증 기업의 **평균 사이버 사고 복구 비용 35% 절감**(IBM 2023), PMI(2022) 통계에서 PMBOK 기반 PMO 운영 시 **IT 예산 초과율 23%->8%**, IT 서비스 가용성 99.5%->99.95% 향상 등 **정량적 ROI 약 2.4배** 효과를 기대할 수 있다.
> 3. **판단 포인트**: 기술사 시험 관점의 핵심은 "**프레임워크 간 중복 제거**"이며, COBIT 2019의 **Design Factor**(10개)과 **Focus Area**(커스터마이징 가능한 관리 단위)를 활용해 조직 맥락에 맞는 **경량 거버넌스 모델**을 설계하는 능력이 평가된다. 즉, 모든 40개 objectives를 적용하는 것이 아니라, **Risk Profile · Compliance Burden · IT Role(Factory/Turnaround/Strategic)** 등 7대 Design Factor 분석을 통해 **핵심 12~15개 objective**로 우선순위를 결정하는 trade-off 판단이 핵심이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 경영적 활용은 더 이상 "IT 부서의 비용 센터" 관점으로 다루지 않는다. 4차 산업혁명 이후 클라우드·AI·데이터 경제로 전환되면서, IT는 **비즈니스 모델 자체**를 결정하는 **전략 자산(Strategic Asset)**이자 **운영 생명선**이 되었다. 그러나 한국 정보시스템 감리원의 통계(2022)에 따르면, 국내大中型 기업의 **62%**가 IT-Business Alignment 부재로 인해 디지털 전환(DX) 프로젝트의 **목표 ROI 미달**을 경험했으며, 글로벌 IT 지출은 약 **4.7조 USD**(2023, Gartner)로 증가했음에도 **실패 프로젝트로 인한 낭비가 약 30%**에 달한다.

이에 본 토픽은 **IT 거버넌스(Governance)**, **IT 관리(Management)**, **IT 운영(Operation)**의 3계층을 하나의 통합 프레임워크로 다루며, 기술사는 다음 4가지 패러다임 전환을 명확히 인식해야 한다.

| 패러다임 | Legacy (1990~2010) | Modern (2015~) | Digital-Native (2023~) |
|:---|:---|:---|:---|
| **IT 역할** | Back-office 비용 센터 | 업무 지원(Enable) | 비즈니스 혁신(Transform) |
| **거버넌스 모델** | 중앙집중 IT 부서 | Bipartite(Federal) | Federated + Center-of-Excellence |
| **위험 관리** | 사후 통제 | 예방 통제(ISO 27001) | 실시간 Zero-Trust + AI 기반 예측 |
| **성과 측정** | 예산 준수율 | KPI/BSC | OKR + Value Stream + NRR |
| **프로젝트 방식** | Waterfall | Agile/Scrum | Hybrid (SAFe, Spotify) + Lean |

```text
[ IT 경영관리 통합 체계도 - 거버넌스에서 운영까지 ]

   +--------------------------------------------------------------+
   |   외부 환경 (External Drivers)                                |
   |   - GDPR · 개인정보보호법 · AI기본법 · ESG · 사이버위협       |
   |   - 시장경쟁 · 고객 디지덜 전환 · 공급망 디지털화             |
   +----------------------------+---------------------------------+
                                | 영향
                                v
   +--------------------------------------------------------------+
   |   ① 거버넌스 계층 (Governance) - COBIT 2019 + ISO 38500      |
   |   -------------------------------------------------          |
   |    +-------------+  +-------------+  +-------------+         |
   |    | Board/CIO   |  |  IT Strategy |  |  IT Risk    |         |
   |    | Committee   |--|   Committee  |--|  Committee  |         |
   |    +-------------+  +-------------+  +-------------+         |
   |           |                |                |                 |
   |           v                v                v                 |
   |    +-------------------------------------------------+        |
   |    |  EDM(평가·지시·모니터) 5개 Governance Obj.       |        |
   |    |  APO(정렬·계획·조직) 14개 Management Obj.        |        |
   |    |  BAI(구축·인수·변경) 11개 Management Obj.        |        |
   |    |  DSS(전달·지원·감독) 6개 Management Obj.         |        |
   |    |  MEA(모니터·평가·분석) 4개 Management Obj.       |        |
   |    +-------------------------------------------------+        |
   +----------------------------+---------------------------------+
                                | 지시·통제
                                v
   +--------------------------------------------------------------+
   |   ② 관리 계층 (Management) - ITIL 4 + PMBOK 7 + TOGAF       |
   |   -------------------------------------------------          |
   |    +--------------+  +--------------+  +--------------+      |
   |    |  IT Service  |  |  Project     |  |  Enterprise  |      |
   |    |  Mgmt (SVS)  |  |  Mgmt Office |  |  Architecture|      |
   |    |  - Incident  |  |  - Portfolio |  |  - ADM cycle |      |
   |    |  - Change    |  |  - Program   |  |  - Business  |      |
   |    |  - Problem   |  |  - Resource  |  |  - Data/APP/ |      |
   |    |  - SLA/XLA   |  |  - Agile     |  |  - Tech      |      |
   |    +--------------+  +--------------+  +--------------+      |
   +----------------------------+---------------------------------+
                                | 실행·조달
                                v
   +--------------------------------------------------------------+
   |   ③ 운영 계층 (Operation) - DevOps · AIOps · SecOps          |
   |   -------------------------------------------------          |
   |    +---------+ +---------+ +---------+ +---------+         |
   |    | Cloud   | | SRE     | | FinOps  | | DataOps |         |
   |    | IaC     | | SLO/SLI | | TBM     | | Pipeline|         |
   |    +---------+ +---------+ +---------+ +---------+         |
   |    +---------+ +---------+ +---------+ +---------+         |
   |    |SecOps   | |AIOps    | |DevSecOps| |MLOps    |         |
   |    |ZeroTrust| |Anomaly  | |SBOM/CA  | |Model CI |         |
   |    +---------+ +---------+ +---------+ +---------+         |
   +--------------------------------------------------------------+
                                |
                                v
   +--------------------------------------------------------------+
   |   ④ 가치 보고 (Value Reporting) - BSC + OKR + ESG + NPS     |
   |   -------------------------------------------------          |
   |   [재무]  ROI, TCO, NPV, NRR     [고객]  CSAT, NPS, XLA    |
   |   [내부]  가용성, MTTR, 배포빈도  [학습]  역량, 인증
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 709 / 800

<- **이전**: [708. IT 경영 관리 핵심 토픽 708번 시험 요약](/studynote/12_it_management/05_security_compliance/708_it_management_core_topic_708_exam_summary/)
**다음**: [710. IT 경영 관리 핵심 토픽 710번 시험 요약](/studynote/12_it_management/05_security_compliance/710_it_management_core_topic_710_exam_summary/) ->

---
