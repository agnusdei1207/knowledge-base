---
title: "IT Management Core Topic 568 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Governance)와 경영관리(Management)의 분리 — ISO/IEC 38500의 6원칙(Evaluate, Direct, Monitor)과 COBIT 2019의 40개 관리목표(Governance & Management Objectives, GMOs) 기반의 의사결정·책임·평가 체계를 통해, IT가 기업 전략(CSF·KGI)과 정렬(Alignment)되어 가치를 창출하도록 통제하는 통합 프레임워크
> 2. **가치**: McKinsey 2023 보고 기준 COBIT 2019 + ITIL 4 통합 적용 시 IT 투자 ROI 평균 18~27% 개선, 중복 IT 비용 12~15% 절감, IT 리스크 사고 35~42% 감소, ISO 38500 인증 기업의 의사결정 리드타임 28% 단축 효과
> 3. **판단 포인트**: ① 중앙집중형(Federal/Cooperative) vs 분산형(Decentralized) 거버넌스 모델 선택, ② BSC 4관점 재무·고객·내부프로세스·학습성장) 중 KPI 가중치 배분(가중치합=100%), ③ Agile/DevOps 환경에서 거버넌스 자동화(GRC Platform) 수준 결정 — 통제 강도 vs 민첩성(Agility) 간 Trade-off

---

## Ⅰ. 개요 및 필요성

정보관리기술사 568번은 **"IT 거버넌스·전략 기획·성과관리·정보화 투자 의사결정"**을 통합적으로 다룬다. 4차 산업혁명·디지털전환(DX) 환경에서 IT는 단순 비용센터(Cost Center)에서 전략적 가치 창출 센터(Strategic Value Center)로 전환되었으며, 이에 따라 **IT-Business Alignment**(Luftman 4단계 모델), **IT 거버넌스(COBIT 2019)**, **정보화 투자 성과 분석(ROI·NPV·IRR·CBA)**, **성과측정(BSC·KPI)**이 하나의 체계로 통합되어야 한다.

기존(Pre-DX) 환경에서는 각 사업부서·IT 부서가 **사일로(Silo)** 형태로 운영되어 이중 투자, 중복 시스템, 책임 소재 불명확, 거버넌스 공백(Governance Vacuum) 문제가 빈번했다. 2020년 이후 Gartner·Forrester 조사에 따르면 글로벌 Fortune 500 기업의 약 67%가 IT-Biz 정렬 실패를 주요 사업 리스크로 분류하고 있으며, 이를 해결하기 위해 **Three Lines Model**(IIA 2020), **COBIT 2019**(40 GMOs), **ISO/IEC 38500:2015**의 3대 거버넌스 표준을 통합 적용하는 사례가 증가하고 있다.

```text
        +---------------------------------------------------------+
        |         IT 거버넌스·경영관리 3계층 통합 프레임워크         |
        +---------------------------------------------------------+
                            |
        +-------------------+-------------------+
        v                   v                   v
+---------------+   +---------------+   +---------------+
| Tier 1: 거버넌스 |   | Tier 2: 경영관리|   | Tier 3: 운영관리|
|  (Governance)  |   | (Management)   |   | (Operation)   |
+---------------+   +---------------+   +---------------+
|• 이사회/CEO   |   |• CIO/IT-Mgmt  |   |• ITIL 4 SVS   |
|• ISO 38500 6원칙|  |• COBIT Mgmt   |   |• Service Ops  |
|• COBIT 2019   |   |  Objectives   |   |• Incident/    |
|  EDM 도메인   |   |  APO/BAI/DSS  |   |  Problem Mgmt |
|• 전략적 방향  |   |• BSC 4관점    |   |• SLA 99.9%^   |
|  설정 (Direct)|   |• 포트폴리오   |   |• MEA 모니터링 |
+-------+-------+   +-------+-------+   +-------+-------+
        |                   |                   |
        +-------------------+-------------------+
                            v
            +------------------------------+
            |  비즈니스 전략·가치 창출(CSF)  |
            |  • Revenue Growth 12% YoY    |
            |  • Customer NPS ≥ 50         |
            |  • OPEX Reduction 8%        |
            +------------------------------+
```

```text
   ❌ 기존 Silo형 IT 관리                  ✅ 통합 거버넌스 체계
   ---------------------                ----------------------
   사업부서A -+                           +- 이사회/거버넌스위 -+
              +-->  IT 부서 (수동)          |  (ISO 38500 적용)   |
   사업부서B -+    중복투자 23%^          +-->  CIO Office       |
              -->  책임불명확              |  (COBIT 2019 40GO)  |
   재무팀 ----->   의사결정 14일           |                     |
   ----------                          +-->  BSC 4관점 KPI     |
   결과: 정렬도 32%                       ----------------
                                         결과: 정렬도 78%^
```

- **📢 섹션 요약 비유**: IT 거버넌스 통합은 마치 **도시의 상수도·전기·교통 인프라를 통합 운영하는 스마트시티 관제센터**와 같다. 각 가정(사업부)이 개별 발전기를 돌리는 비효율 대신, 통합 관제센터가 전력·수량·품질을 표준화하여 도시 전체의 효율을 극대화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. COBIT 2019 5개 도메인 · 40개 관리목표 (GMOs) 구조

COBIT 2019는 거버넌스 5개 + 경영관리 35개로 총 40개의 GMOs를 정의하며, 각 목표는 **Enterprise Goal -> Alignment Goal -> Component(Process/Structure/People/Skill/Information/Service/Infrastructure/Application)** 로 연쇄(Cascade)된다.

```text
       +------------------------------------------------------+
       |            COBIT 2019 5 Domains / 40 GMOs            |
       +------------------------------------------------------+
       |                                                       |
       |  EDM (Evaluate, Direct, Monitor) — 5개 [거버넌스]    |
       |  +- EDM01 거버넌스 체계 설정 및 유지                  |
       |  +- EDM02 실현가능한 혜택 제공                        |
       |  +- EDM03 위험 최적화                                |
       |  +- EDM04 자원 최적화                                |
       |  +- EDM05 이해관계자 투명성 확보                      |
       |                                                       |
       |  APO (Align, Plan, Organize) — 14개 [관리]            |
       |  +- APO01 관리체계·프레임워크                         |
       |  +- APO02 전략·경영관리체계                           |
       |  +- APO04 혁신관리                                   |
       |  +- APO05 포트폴리오 관리 ★(정보화투자 핵심)          |
       |  +- APO07 인적자원                                   |
       |  +- APO12 리스크 관리                                 |
       |  +- APO13 보안관리                                    |
       |                                                       |
       |  BAI (Build, Acquire, Implement) — 11개               |
       |  +- BAI01 프로그램 관리                              |
       |  +- BAI03 투자 결정 ★                                |
       |  +- BAI11 프로젝트 관리                               |
       |                                                       |
       |  DSS (Deliver, Service, Support) — 6개                |
       |  +- DSS02 서비스 요청·사고 관리                      |
       |  +- DSS05 보안운영관리                                |
       |                                                       |
       |  MEA (Monitor, Evaluate, Assess) — 4개               |
       |  +- MEA01 성과·준수 모니터링                        |
       |  +- MEA03 컴플라이언스 관리                           |
       +------------------------------------------------------+
                              |
                              v
       +------------------------------------------------------+
       |  Components (7가지 핵심 구성요소)                      |
       |  P-SFISPA: Process·Structure·Flow·Information·      |
       |            Skill·People·Application                  |
       +------------------------------------------------------+
```

### B. BSC(Balanced Scorecard) 기반 IT 성과관리 4관점 KPI

Kaplan·Norton BSC 4관점을 IT에 적용할 때 가중치(Σwi=1.0)와 목표치·측정식을 명확히 정의한다.

```text
                    +----------- Vision & Strategy -----------+
                                  |  IT BSC 4관점
                                  v
        +------------+-------------+-------------+------------+
        |  재무(Finance) |  고객(Customer)| 내부프로세스 | 학습·성장   |
        |   w1=0.25     |   w2=0.30    |  w3=0.25    | w4=0.20    |
        +------------+-------------+-------------+------------+
        | • IT ROI    | • IT 서비스 | • 프로세스  | • IT 인력   |
        | • TCO 절감  |   만족도    |   자동화율  |   역량지수 |
        | • OPEX 비중 | • End-User  | • SLA 준수율| • 교육시간 |
        | • 예산 준수 |   NPS       | • 인시던트  | • 인증취득 |
        |   율        | • 가용성    |   MTTR      |   비율     |
        |             |   99.9%^    |             |            |
        +------------+-------------+-------------+------------+
                                  |
                                  v
                   KPI = Σ (wi × Achievement_i)
                   목표 ≥ 85% = 우수 / 70~85% = 보통 / <70% = 미흡
```

### C. 정보화 투자 분석 — ROI·NPV·IRR·CBA 4대 평가 모델

```text
   +-----------------------------------------------------------+
   |         정보화 투자 의사결정 흐름(Decision Workflow)        |
   +-----------------------------------------------------------+
       ① 사업기회/문제 정의
              |  CSF·KPI 도출
              v
       ② 대안 식별 (A: SaaS 도입 / B: On-Premise 구축 / C: Outsourcing)
              |
              v
       ③ 정량 분석
           +- ROI = Σ(편익−비용) / Σ투자액 × 100    (목표 ≥ 15%)
           +- NPV = Σ[CF_t / (1+r)^t] − 투자액      (r=할인율 8~12%)
           +- IRR: NPV=0이 되는 r
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 568 / 800

<- **이전**: [567. IT 경영 관리 핵심 토픽 567번 시험 요약](/studynote/12_it_management/05_security_compliance/567_it_management_core_topic_567_exam_summary/)
**다음**: [569. IT 경영 관리 핵심 토픽 569번 시험 요약](/studynote/12_it_management/05_security_compliance/569_it_management_core_topic_569_exam_summary/) ->

---
