+++
title = "656. IT 경영 관리 핵심 토픽 656번 시험 요약 (IT Management Core Topic 656 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019의 5개 도메인(EDM/APO/BAI/DSS/MEA)과 40개 거버넌스 목표를 기반으로, IT 투자 포트폴리오를 Run(운영유지)·Grow(확장)·Transform(혁신) 3대 카테고리로 분류하고 Weighted Scoring Model + AHP(Analytic Hierarchy Process) + NPV/IRR/Payback Period 다기준 의사결정(MCDA, Multi-Criteria Decision Analysis)을 결합하여 우선순위를 결정하는 **체계적 의사결정 프레임워크**임.
> 2. **가치**: Gartner 2023 보고 기준, 포트폴리오 관리 성숙도 Level 3 이상 기업은 IT 투자 ROI가 평균 23% 높고, 실패 프로젝트 비율이 41% 감소함. 국내는 「디지털정부법」 제46조(정보화사업 사업비 산정) 및 「클라우드컴퓨팅 발전법」에 따른 클라우드 우선(Cloud First) 원칙 하에서, 연간 8조 원 규모의 공공 IT 투자 효율화를 통해 동일 예산 대비 서비스 처리량 약 1.8배 향상이 가능함.
> 3. **판단 포인트**: ① 거버넌스 성숙도(Gartner 5단계) vs 규제 리스크(PIPA·ISMS-P) 간의 균형, ② RGT 비율(전통 70/20/10 vs DX 시대 40/30/30로 이동), ③ COBIT Design Factor 7개(전략, 목표, 위험, 문제, 위협, 규제, IT 이슈)와 기업 전략 간 정합성 검증, ④ 이해관계자(경영진·현업·IT·감사) 간 권한 분배(Weill & Ross 5가지 의사결정 메커니즘) 설계가 핵심.

---

## Ⅰ. 개요 및 필요성

국내 IT 투자 규모는 공공부문만 해도 2023년 기준 약 7.8조 원(행안부 정보화사업 통계)에 달하며, 민간까지 합산 시 80조 원 이상으로 추정된다. 그러나 한국정보화진흥원(KIAT) 조사에 따르면 IT 프로젝트 성공률은 약 29%에 불과하고, 44%는 예산 초과, 19%는 조기 종료된다. 이러한 실패의 근본 원인은 **① 전략-투자 불일치(Strategic Misalignment)**, **② 의사결정 주체 모호성**, **③ 포트폴리오 가시성 부재**의 3가지로 요약된다.

디지털 전환(DX) 시대에는 전통적 **"Build -> Run"** 방식에서 **"Buy/Subscribe -> Configure -> Run"** 방식(클라우드·SaaS·PaaS)으로 IT 소비 모델이 전환되었고, 이는 투자 평가 기준을 NPV 중심에서 **TCO(Total Cost of Ownership) + 옵션 가치(Real Options Value) + BizOps(비즈니스-IT 통합 운영 지표)** 중심으로 재정의해야 함을 의미한다. 또한 AI·데이터 거버넌스(데이터 3법, AI 기본법), ESG 대응, 사이버 회복력(Resilience) 등 새로운 비-기능 요구사항이 투자 결정 변수로 추가되었다.

```text
+-------------------------------------------------------------+
|        DX 시대 IT 거버넌스 의사결정 레이어 (3-Tier)         |
+-------------------------------------------------------------+
|                                                             |
|  [Tier 1: 전략 정렬 계층]                                   |
|  +--------------+  +--------------+  +--------------+      |
|  | 기업전략     |-> | IT 전략맵    |-> | 거버넌스 체계|      |
|  | (BSC/PESTLE) |  | (Ward&Peppard|  | (COBIT 2019) |      |
|  |              |  |  SAM)        |  |              |      |
|  +--------------+  +--------------+  +--------------+      |
|         |                  |                  |             |
|         +------------------+------------------+             |
|                            v                                |
|  [Tier 2: 포트폴리오 의사결정 계층]                         |
|  +-------------------------------------------------+        |
|  | 투자 후보 Pool --> 1차 스크리닝(Go/No-Go Gate)  |        |
|  |            |                                    |        |
|  |            v                                    |        |
|  | 다기준 평가: ① 전략정합(25%) ② ROI/NPV(20%)    |        |
|  |             ③ 리스크(15%) ④ 규제준수(15%)      |        |
|  |             ⑤ 기술성숙도(10%) ⑥ Biz임팩트(15%) |        |
|  |            |                                    |        |
|  |            v                                    |        |
|  | AHP 가중치 도출 --> MCDA 점수화 --> 최적조합 탐색 |        |
|  +-------------------------------------------------+        |
|                            |                                |
|                            v                                |
|  [Tier 3: 실행·모니터링 계층]                               |
|  +-------------------------------------------------+        |
|  | PPM Tool (Planview/Broadcom Clarity) 연동       |        |
|  | + IT-Fin 대시보드(Apptio Flexera)               |        |
|  | + ITIL4 변경관리 + DevOps 메트릭(DORA 4종)      |        |
|  | + ISMS-P/K-ISMS 인증 감사 연계                  |        |
|  +-------------------------------------------------+        |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 포트폴리오 관리는 **"주식 시장에서의 자산 배분(Asset Allocation)"**과 같다. 한 종목(개별 프로젝트)에 올인하지 않고, 채권·주식·대안투자(Run·Grow·Transform) 간 비율을 조정하며, 시장 상황(거버넌스 환경)에 따라 비중을 재조정하는 것과 동일한 원리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 ISO/IEC 38500(IT 거버넌스 국제표준)을 구현 레이어로 구현한 프레임워크로, **거버넌스 시스템(Governance System)**과 **거버넌스 프레임워크(Governance Framework)**의 이중 구조를 갖는다. 핵심은 **40개의 관리목표(Management Objective)**를 **5개 도메인**에 매핑하고, **7개 Design Factor**를 통해 기업 맞춤형 거버넌스 시스템을 설계하는 것이다.

```text
        COBIT 2019 40 Governance/Management Objectives
   +-----------------------------------------------------+
   | EDM (Evaluate·Direct·Monitor) - 5개                 |
   |   EDM01 거버넌스 프레임워크 설정·유지                |
   |   EDM02 이득 전달 보장        EDM03 리스크 최적화    |
   |   EDM04 자원 최적화           EDM05 이해관계자 투명성 |
   +-----------------------------------------------------+
   | APO (Align·Plan·Organize) - 14개                    |
   |   APO02 전략관리  APO04 혁신관리  APO05 포트폴리오★  |
   |   APO06 예산·비용관리  APO08 관계관리  APO12 리스크  |
   |   APO13 보안관리  APO14 데이터관리                   |
   +-----------------------------------------------------+
   | BAI (Build·Acquire·Implement) - 11개                 |
   |   BAI01 프로그램관리  BAI03 투자관리  BAI11 품질관리 |
   +-----------------------------------------------------+
   | DSS (Deliver·Service·Support) - 6개                  |
   |   DSS02 서비스요청사고  DSS04 문제관리  DSS06 보안   |
   +-----------------------------------------------------+
   | MEA (Monitor·Evaluate·Assess) - 4개                  |
   |   MEA01 성과조정  MEA02 내부통제  MEA03 외부보증    |
   +-----------------------------------------------------+
   ★ APO05(Managed Portfolio) = 포트폴리오 관리의 중핵

   [Design Factor 7개로 시스템 커스터마이징]
   +------------+------------+------------+------------+
   | DF1 기업전략| DF2 목표    | DF3 위험    | DF4 문제   |
   | (Growth/   | (내부·외부  | (ICT 관련  | (IT 이슈   |
   | Def./...)  |  목표)      |  리스크)    |  카탈로그) |
   +------------+------------+------------+------------+
   | DF5 위협   | DF6 규제준수| DF7 IT이슈 |            |
   | (사이버·   | (PIPA/ISMS/| (인프라·   |            |
   |  공급망)   |  ESG)       |  인력)     |            |
   +------------+------------+------------+------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM 도메인 (이사회·IT거버넌스위원회)** | 거버넌스 의사결정 최고 권위 | RACI 매트릭스상 Accountable 위치, 이사회 산하 IT 전략위원회(연 4회), 베스트 프랙티스: GE·P&G 모델(3단계 에스컬레이션) |
| **APO05 Portfolio Manager** | 투자 후보 수집·평가·우선순위화·균형화 | 4단계 프로세스: ①Portfolio Inventory(연간 약 200~500건의 IT Initiative 입력) -> ②Portfolio Definition(Run/Grow/Transform 분류) -> ③Portfolio Optimization(NPV·Risk-Adjusted NPV·옵션가치 기반 점수화) -> ④Portfolio Management & Communication |
| **MCDA 엔진 (AHP + 가중치 매트릭스)** | 정성·정량 점수의 합리적 통합 | Saaty의 9점 척도(1=동등, 9=극우세)로 쌍대비교 -> 고유벡터 계산으로 가중치 도출 -> 일관성비율(CR, Consistency Ratio) ≤ 0.1 검증 -> 종합점수 = Σ(Wi × Si) |
| **PPM 도구 (Planview / Broadcom Clarity / ServiceNow SPM)** | 포트폴리오 실행·추적·재조정 | API 연동: Jira/Azure DevOps(실행 메트릭), SAP S/4HANA(재무), ServiceNow ITSM(서비스), Tableau/Power BI(시각화). 자동화된 **Investment Risk Score(IRS)** 산출 알고리즘 내장 |
| **거버넌스 대시보드 (Apptio / Flexera ITFM)** | IT 재무 투명성·FinOps 통합 | TCO 모델(하드웨어·소프트웨어·인력·외주·운영비의 5축), 코스트 트랜스페어런시(Kubernetes Namespace 단위 과금), Show
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 656 / 800

<- **이전**: [655. IT 경영 관리 핵심 토픽 655번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/655_it_management_core_topic_655_exam_summary/)
**다음**: [657. IT 경영 관리 핵심 토픽 657번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/657_it_management_core_topic_657_exam_summary/) ->

---
