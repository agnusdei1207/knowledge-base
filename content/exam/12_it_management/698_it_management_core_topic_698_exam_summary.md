---
title: "IT Management Core Topic 698 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 🏛️ IT 경영 관리 핵심 토픽 698번 시험 요약 (IT 거버넌스 & COBIT 2019 기반 IT경영체계)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 40개 거버넌/관리 목표(Governance & Management Objectives)를 통해 **이해관계자 가치(Value Delivery)와 위험 최적화(Risk Optimization), 자원 효율(Resource Optimization)**의 3대 균형축으로 IT-Business Alignment를 달성하는 **책임·의사결정 프레임워크(RDAC: Responsibility, Decision, Accountability, Consult, Inform 매트릭스 기반)**이다.
> 2. **가치**: DAMA-DMBOK2 기반 **데이터 거버넌스 성숙도 1->5단계 도약 시 운영비용 25~40% 절감**, ITIL 4 34개 실무 프로세스 연계 시 **MTTR(평균복구시간) 60% 단축**, ISO/IEC 38500 6원칙 적용 시 **이사회-경영진-ICT 의사결정 latency 75% 감소** 등의 정량적 가치를 창출한다.
> 3. **판단 포인트**: **집중형(Federated) vs 분산형(Decentralized) 거버넌스 모델**, **Push 전략(규제·컴플라이언스 중심) vs Pull 전략(비즈니스 가치 중심)** 사이의 trade-off를 조직의 디지털 성숙도(Digital Maturity Level)와 규제 환경에 따라 판단해야 하며, **RACI 매트릭스 vs RACI-VS, Three Lines Model(3 Lines of Defense)** 등 책임구조 모델 선정이 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 1980년대 말~2000년대 초반까지 **데이터센터 운영(Mainframe -> Client-Server)**, **프로젝트 단위 예산편성**, **CTO/CIO 직속 보고 체계**로 운영되었다. 그러나 2010년 이후 **클라우드 전환(Public Cloud Spending CAGR 22.3%)**, **GDPR·개인정보보호법·ESG 공시 의무화**, **Ransomware 공격 증가(연평균 350% 성장)** 등 거버넌스 환경이 급변하면서, IT가 더 이상 **"비용 센터(Cost Center)"**가 아닌 **"전략적 가치 실현 기관(Value Realization Engine)"**으로 재정의되어야 하는 시대적 요구가 발생했다.

특히 **2020년 금융분야 클라우드 컴플라이언스 가이드라인**, **2022년 클라우드 보안인증制度(CSAP)**, **2023년 AI 기본법(안)** 등 규제가 가속화되면서, 단순한 **ITIL 기반 운영관리**만으로는 **법적 책임 소재 명확화, 이해관계자 가치 최적화, 리스크 한계선 설정**이 불가능해졌다. 이러한 배경에서 **COBIT 2019**(Control Objectives for Information and Related Technologies)은 ISACA가 2018년发布的 6번째 버전으로, **거버넌스 시스템 5개 영역(EDM: Evaluate, Direct, Monitor)**, **관리 시스템 4개 영역(APO, BAI, DSS, MEA)**, **40개 핵심 목표**를 통해 **End-to-End 책임 체계를 제시**한다.

```text
+---------------------------------------------------------------------+
|           IT 거버넌스 패러다임 진화: 4단계 패러다임 시프트          |
+---------------------------------------------------------------------+
|                                                                     |
|  [P1: 1990s]                [P2: 2000s]                            |
|  +----------+              +----------+                            |
|  |  IT 운영  |              | ITIL v2  |                            |
|  |  중심     |  --------►  | 서비스   |  --------►                 |
|  | (Reactive)|              | 데스크   |                            |
|  +----------+              +----------+                            |
|       |                          |                                  |
|       |                          v                                  |
|       |                   [P3: 2010s]                              |
|       |                   +----------+                             |
|       |                   | COBIT 5  |                             |
|       |                   | + ITILv3 |  --------►                  |
|       |                   | (ITIL+   |                             |
|       |                   | 전략연계)|                             |
|       |                   +----------+                             |
|       |                          |                                  |
|       |                          v                                  |
|       |                   [P4: 2020s NOW]                          |
|       |                   +--------------------------+              |
|       +-----------------► |  COBIT 2019 + ITIL 4     |              |
|                           |  + ISO 38500 + NIST CSF  |              |
|                           |  + DMBOK 2 (데이터 거번) |              |
|                           |  + Three Lines Model     |              |
|                           |  (통합 거버넌스 체계)     |              |
|                           +--------------------------+              |
+---------------------------------------------------------------------+
```

**왜 지금 IT 거버넌스인가?** IDC의 2023년 보고서에 따르면, **포춘 500대 기업 중 67%가 "IT-Business Misalignment"를 최대 리스크 1순위**로 꼽았으며, **McKinsey Global Institute 분석 결과 거버넌스 성숙도 상위 25% 기업의 ROI가 하위 25% 대비 2.4배 높은** 것으로 나타났다. 또한 **2024년 한국인터넷진흥원(KISA) 조사**에 따르면, **국내 중견기업의 58%가 "IT 투자 효과 측정 체계 부재"**를 디지털 전환의 최대 장애물로 응답했다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"대형 호텔의 객실·식당·주차장·소방·고객정보를 총괄하는 총지배인(GM) 시스템"**과 같다. 객실(애플리케이션)·식당(데이터)·소방(보안)·주차장(인프라)가 제각각 운영되면 호텔이 마비되듯, IT 부문을 통합 관리하는 **"최상위 의사결정 체계"**가 반드시 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**COBIT 2019 핵심 아키텍처**는 **거버넌스 시스템(Governance System)**과 **관리 시스템(Management System)**의 이원적 구조로 설계된다. 거버넌스 시스템은 5개의 **EDM(평가·지시·모니터링) 도메인**으로 구성되어 이사회·경영진의 의사결정을 지원하며, 관리 시스템은 **APO(Align, Plan, Organize), BAI(Build, Acquire, Implement), DSS(Deliver, Service, Support), MEA(Monitor, Evaluate, Assess)**의 4개 도메인에 35개의 관리 목표로 구성된다.

**핵심 메커니즘**은 **Cascade(연쇄) 원칙**: 거버넌스 목표 -> 관리 목표 -> 컴포넌트(Process, Organizational Structure, Information Flow, People, Skills, Competencies, Policies, Procedures, Culture, Behavior) -> **Concerns(Quality, Risk, Value Creation)** 순으로 전개된다. 각 목표는 7가지 컴포넌트의 설계변수(Design Factor)와 연계되어 **40개 목표의 우선순위·관계·메트릭**이 자동 조정된다.

```text
+--------------------------------------------------------------------+
|            COBIT 2019 거버넌스 시스템 참조 아키텍처                |
+--------------------------------------------------------------------+
|                                                                    |
|  +----------- 거버넌스 시스템 (5개 EDM 목표) -----------+          |
|  |  +--------+  +--------+  +--------+  +--------+  +--------+  |
|  |  | EDM01  |  | EDM02  |  | EDM03  |  | EDM04  |  | EDM05  |  |
|  |  | 거번체계|  | 가치전달|  | 리스크 |  | 자원   |  | 이해관|  |
|  |  | 평가   |  | 보장   |  | 최적화 |  | 최적화 |  | 계자투|  |
|  |  |        |  |        |  |        |  |        |  | 명성  |  |
|  |  +--------+  +--------+  +--------+  +--------+  +--------+  |
|  +---------------------+----------------------------------------+
|                        | Cascade (연쇄)
|                        v
|  +----------- 관리 시스템 (4개 도메인, 35개 목표) ---------+     |
|  |  APO(Align-Plan-Organize)         14개 목표              |     |
|  |  +- APO01 (거버넌스 프레임워크 관리)                      |     |
|  |  +- APO03 (기업아키텍처 관리)                             |     |
|  |  +- APO04 (혁신 관리)                                     |     |
|  |  +- APO05 (포트폴리오 관리)                               |     |
|  |  +- APO12 (리스크 관리)                                   |     |
|  |  +- APO13 (보안 관리)                                     |     |
|  |                                                          |     |
|  |  BAI(Build-Acquire-Implement) 11개 목표                  |     |
|  |  +- BAI01 (프로그램 관리)                                 |     |
|  |  +- BAI03 (솔루션 설계)                                   |     |
|  |  +- BAI11 (프로젝트 관리)                                 |     |
|  |  +- BAI06 (변경 관리)                                     |     |
|  |                                                          |     |
|  |  DSS(Deliver-Service-Support) 6개 목표                   |     |
|  |  +- DSS01 (운영 관리)                                     |     |
|  |  +- DSS02 (서비스 요청/사고 관리)                         |     |
|  |  +- DSS04 (연속성 관리)                                   |     |
|  |  +- DSS05 (보안 운영)                                     |     |
|  |                                                          |     |
|  |  MEA(Monitor-Evaluate-Assess) 4개 목표                   |     |
|  |  +- MEA01 (성능/준수 모니터링)                            |     |
|  |  +- MEA02 (내부 통제 체계)                                |     |
|  |  +- MEA03 (외부 컴플라이언스)                              |     |
|  +----------------------------------------------------------+     |
|                                                                    |
|  +---- 7대 컴포넌트 (모든 목표에 공통 적용) ----+                  |
|  |  1. Process  2. Org Structure  3. Info Flow  |                  |
|  |  4. People/Skill  5. Policy  6. Procedure    |                  |
|  |  7. Culture/Behavior                         |                  |
|  +----------------------------------------------+                  |
|                                                                    |
|  +---- 11개 설계요인 (Design Factors) ----+                       |
|  |  DF1 전략  DF2 목표  DF3 위험  DF4 리스크 문제                |
|  |  DF5 컴플라이언스 요구  DF6 IT 역할  DF7 IT 도입              |
|  |  DF8 IT 구현 방법론  DF9 기술采纳 전략                         |
|  |  DF10 조직 규모  DF11 외부요인                                  |
|  +------------------------------------------+                       |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스 5목표)** | 이사회·경영진의 의사결정·감독·평가 | `EDM01` 거버넌스 체계 설정, `EDM02` 가치 전달 보장(Benefit Realization), `EDM03` 리스크 최적화, `EDM04` 자원 최적화(자원 배분 의사결정), `EDM05` 이해관계자 투명성 보고 |
| **APO(전략·계획·조직)** | IT 전략-비즈니스 정렬 및 조직 설계 | `APO02` 전략관리(BSC Balanced Scorecard 연계), `APO03` EA(TOGAF/Zachman 기반), `APO05` 포트폴리오 관리(Option Theory), `APO12` 리스크관리(ISO 31000 연계), `APO13` 보안관리(NIST CSF 5개 Function 매핑) |
| **BAI(구축·획득·구현)** | 솔루션 설계·구축·테스트·배포 | `BAI02` 요구사항관리(BABOK v3), `BAI03` 솔루션설계(마이크로서비스/모놀리스 trade-off), `BAI06` 변경관리(CAB Change Advisory Board 운영), `BAI11` 프로젝트관리(PMBOK 7/PRINCE2/Scrum) |
| **DSS(운영·서비스·지원)** | 일상의 IT 서비스 전달 및 지원 | `DSS01` 운영관리(DevOps·AIOps), `DSS02` 서비스데스크(ITIL 4 Service Desk 4세대 모델), `DSS03` 문제관리(Known Error DB), `DSS04` 연속성관리(BCP/DR RTO·RPO·MTTD 정의) |
| **MEA(모니터·평가·감사)** | 성과 측정 및 통제·감사 | `MEA01` 성능모니터링(KPI/CSF/CQGM 4단계 메트릭), `MEA02` 내부통제(COSO 2013 17원칙), `MEA03` 외부컴플라이언스(SOX·ISO 27001·PCI-DSS), `MEA04` 자기평가(스스로 거버넌스 성숙도 평가) |

**핵심 알고리즘·모델**:
- **거버넌스 시스템 설계 알고리즘**: ① 조직의 **11개 설계요인(Design Factors)** 점수화 -> ② 우선순위 매트릭스로 40개 목표 가중치 산출 -> ③ **Process Capability Level(0~5)** 목표 설정 -> ④ **7대 컴포넌트**별 RACI 매트릭스 도출 -> ⑤ **Cascade 목표별 메트릭 정의**(CSF: Critical Success Factor, KGI: Key Goal Indicator, KPI: Key Performance Indicator 3단계).
- **성숙도 평가 모델**: COBIT 2019는 **CMMI 5단계 + ISO 15504 PAM(Process Assessment Model)** 기반의 **6단계 능력수준**(0: 불완전, 1: 초기, 2: 관리, 3: 확립, 4: 예측, 5: 최적화) 채택. 각 목표마다 **Process Rating(0~100%)** 산정 공식: `Rating =
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 698 / 800

<- **이전**: [697. IT 경영 관리 핵심 토픽 697번 시험 요약](/studynote/12_it_management/05_security_compliance/697_it_management_core_topic_697_exam_summary/)
**다음**: [699. IT 경영 관리 핵심 토픽 699번 시험 요약](/studynote/12_it_management/05_security_compliance/699_it_management_core_topic_699_exam_summary/) ->

---
