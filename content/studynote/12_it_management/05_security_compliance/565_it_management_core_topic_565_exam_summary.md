---
title: "IT Management Core Topic 565 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Information Technology Governance)는 기업의 IT 자산을 **비즈니스 가치(Value)** 창출과 **리스크 통제(Risk Control)** 두 축으로 정렬하기 위해, 이사회-경영진-실행조직 간 의사결정권·책임·보고체계(책임구조, RACI)를 **COBIT 2019, ISO/IEC 38500, ITIL 4, PMBOK 7th, 정보시스템 감리법** 등의 표준 프레임워크로 표준화하는 경영관리 체계이다.
> 2. **가치**: 정량적 효과로 IT 투자 대비 ROI **20~35% 향상**(Gartner 2023), 정보화 사업 실패율 **30%->10% 감소**(PMI 2021), 보안사고 평균 복구비용 **MTTR 47% 단축**(IBM Cost of Data Breach), 정성적 효과로 경영 가시성 확보, 이사회-경영진 간 IT 커뮤니케이션 정착, 규제 준수(컴플라이언스) 자동 증빙 체계 확립.
> 3. **판단 포인트**: ① **집중형(Centralized) vs 분산형(Federated) 거버넌스 모델** 선택(그룹사 다수 시), ② **Bespoke(맞춤형) vs Industry-Standard(COBIT 등 표준)** 프레임워크 적용, ③ **Build vs Buy vs Cloud(Outsource)** 의사결정 시 TCO·IRR·Payback Period 비교, ④ 거버넌스 성숙도 1~5단계 중 **목표 단계** 설정, ⑤ Agile/DevOps 환경에서 거버넌스 부담 최소화(Guard Rail 설계).

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 지원(SOA·ERP 1세대) 수준을 넘어 **비즈니스 코어(코어 뱅킹, AI 기반 의사결정, 디지털 플랫폼)** 로 자리매김하면서, IT에 투입되는 예산 비중이 매출 대비 **5~12%**(금융권 8~15%, 제조업 3~6%)에 이릅니다. 그러나 McKinsey(2022) 보고에 따르면 대기업 IT 프로젝트 중 **30%는 비즈니스 목표와 정렬되지 않아 실패**하며, 글로벌 IT 지출 **4.6조 USD** 중 약 **30%(1.4조 USD)** 가 낭비(waste)되는 것으로 추정됩니다.

이에 각국 정부와 표준화 기구는 IT에 대한 **의사결정·감독·책임 체계**를 법·제도적 차원에서 정립하기 시작했습니다. 한국은 **「정보시스템의 효율적 도입 및 운영 등에 관한 법률」(약칭: 정보시스템법)**, **「전자정부법」**, **「클라우드컴퓨팅 발전 및 이용자 보호에 관한 법률」**, **「개인정보 보호법」** 등 30여 개의 IT 관련 법령을 운영하며, **한국지능정보사회진흥원(NIA)** 및 **한국정보통신기술협회(TTA)** 가 세부 지침을 관리합니다.

```text
+--------------------------------------------------------------------------+
|           IT 경영관리 거버넌스 3-Layer 의사결정 구조 (As-Is vs To-Be)     |
+--------------------------------------------------------------------------+
|                                                                          |
|  [As-Is: 전통적 Shadow IT 시대]            [To-Be: 거버넌스 정착 시대]     |
|                                                                          |
|   이사회 (Board)                              이사회 IT위원회               |
|       |  (보고 없음)                              |  분기 1회 CIO 보고      |
|       v                                          v                        |
|   CEO --- 사업부서(자체 IT 구매)         CIO (CDO 겸직 가능)               |
|              |                                       |                    |
|              v                                       v                    |
|         IT 부서(사후 인지)              +----------+----------+          |
|                                           v                     v        |
|   <----- 결과: 중복투자, 보안사고 --->  IT 전략기획실     IT 운영센터   |
|                                          |                     |        |
|                                          v                     v        |
|                                    사업부서 IT거버넌스위원회 (CoE)        |
|                                                                          |
|   💡 핵심 변화: "사후 인지" -> "사전 정렬(Align) + 사후 통제(Govern)"     |
+--------------------------------------------------------------------------+
```

IT 거버넌스의 도입은 단순한 "제도 정착"이 아니라, **IT Capability(역량) -> Business Outcome(성과)** 로 이어지는 **Value Chain(가치지사슬)** 을 가시화하는 작업입니다. ISO/IEC 38500(2022 개정)은 IT 거버넌스의 6대 원칙으로 **Responsibility(책무), Strategy(전략), Acquisition(획득), Performance(성과), Conformance(준수), Human Behavior(인적 행동)** 을 제시하며, 이 6원칙을 **Evaluate(평가) -> Direct(지휘) -> Monitor(모니터링)** 의 3단계 거버넌스 사이클(EDM Cycle)로 끊임없이 반복 적용하도록 요구합니다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 도시계획(Urban Planning)** 과 같습니다. 건물 하나 짓는 것은 건축 허가만 받으면 되지만, 도시 전체의 상하수도·도로·공원·에너지·환경 규제는 30~50년 단위의 마스터플랜이 필요합니다. IT 거버넌스도 개별 시스템이 아니라 **도시(전사 IT) 차원의 종합계획** 입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 핵심 토픽은 크게 **① 거버넌스 프레임워크, ② IT 투자·경제성 분석, ③ 정보화 사업 관리, ④ IT 서비스 운영·성과, ⑤ 컴플라이언스·감리** 5개 도메인으로 구성됩니다. 각 도메인은 서로 **인과관계(Dependency)** 로 연결됩니다.

```text
+--------------------------------------------------------------------------+
|        IT 경영관리 핵심 도메인 통합 아키텍처 (Integrated Framework)      |
+--------------------------------------------------------------------------+
|                                                                          |
|  [1] 거버넌스 ---> [2] 투자관리 ---> [3] 사업관리 ---> [4] 운영·성과        |
|       |              |              |              |                      |
|       |              |              |              |                      |
|       +--------------+--------------+--------------+                      |
|                              |                                          |
|                              v                                          |
|                       [5] 컴플라이언스 & 감리                              |
|                                                                          |
|  +-----------------------------------------------------------------+     |
|  | Layer 1: 의사결정 계층 (Decision Layer) - COBIT 2019 EDM         |     |
|  |   +- EDM01 거버넌스 프레임워크 수립                               |     |
|  |   +- EDM02 가치 제공                                           |     |
|  |   +- EDM03 리스크 최적화                                       |     |
|  |   +- EDM04 자원 최적화                                         |     |
|  |   +- EDM05 이해관계자 투명성                                    |     |
|  +-----------------------------------------------------------------+     |
|  | Layer 2: 정렬 계층 (Alignment Layer) - ITIL 4 SVS               |     |
|  |   +- Service Value System (가치 흐름)                          |     |
|  |   +- 7 Guiding Principles (7대 원칙)                           |     |
|  |   +- 4 Dimensions Model (조직·정보·파트너·기술)                 |     |
|  +-----------------------------------------------------------------+     |
|  | Layer 3: 실행 계층 (Execution Layer) - PMBOK 7th + DevOps       |     |
|  |   +- 8 Performance Domains (성과 영역)                         |     |
|  |   +- 12 Principles (12대 원칙)                                 |     |
|  |   +- CI/CD + SRE + Agile 통합                                  |     |
|  +-----------------------------------------------------------------+     |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (Control Objectives for Information and Related Technologies)** | 거버넌스/관리 목표의 표준화 및 평가 | 5개 도메인 × 40개 관리 목표(EDM·APO·BAI·DSS·MEA), 7개 컴포넌트(원리·정책·프레임워크·역량·문화·인프라·사람), 설계 인수인계 11단계 Focus Area, **Capability/Maturity Model(0~5단계)**, 핵심 40개 KPI(예: APO04.02 - IT 예산 배분 정렬도 ≥ 85%) |
| **ITIL 4 (Information Technology Infrastructure Library v4)** | IT 서비스 운영 및 가치 흐름 관리 | **Service Value System(SVS)**: Demand->Engage->Design->Obtain->Build->Deliver->Support, **34개 Practice**(Change Enablement, Incident, Problem, Service Desk, Continual Improvement), **4D Model**: 조직·정보·파트너·기술, **7 Guiding Principles**: Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize |
| **ISO/IEC 38500:2022** | 이사회 차원의 IT 거버넌스 국제표준 | 6대 원칙(책임·전략·획득·성과·준수·인적행동) × 3단계 사이클(Evaluate-Direct-Monitor), **Governance Framework Indicator(GFI)** 12개 평가항목, 영국(BS 31100), 일본(JIS Q 38500), 한국(KS X 38500) 국가표준 호환 |
| **정보화 사업 관리(한국형 PMIS)** | 국가·공공기관 정보화 사업의 계획-착수-준공-사후관리 | **한국정보화진흥원 NIA PMIS 2.0** (사업비 5억 이상 의무 사용), **5단계 사업관리**: 타당성조사 -> 계획 수립 -> 사업 시행 -> 준공 -> 사후관리, **사업비 산정 SLIM·FP·Cocomo II**, 전자정부법 16조(사업관리), 19조(성능 평가) |
| **IT 경제성 분석 (Financial Management for IT)** | IT 투자의 정량적 의사결정 | **TCO(Total Cost of Ownership) 5계층**: 직접·간접·생산성·가용성·전략비용, **NPV(순현재가치) / IRR(내부수익률) / Payback Period / BCR(편익비용비율) / EVA(Economic Value Added)**, 할인율 **WACC 6~9%**(국내 대기업 평균), **Portfolio 관리**: BCG Matrix / TOGAF Architecture Maturity |

### COBIT 2019 설계 시 핵심 공식 및 판단 기준

COBIT 2019에서는 거버넌스/관리 목표 달성도를 정량화하기 위해 **NCSF(Natural Cause System of Factors)** 기반의 **Inherent Risk × Control Strength = Residual Risk** 공식을 사용합니다. 또한 목표별 **Capability Level 0~5** 등급을 부여하며, 목표 수준은 **목표 기업/산업/규제 벤치마크** 와 비교해 결정합니다.

```text
+--------------------------------------------------------------------------+
|          IT 투자 경제성 분석 의사결정 트리 (Decision Tree)                 |
+--------------------------------------------------------------------------+
|                                                                          |
|   Q1: 사업이 법적·규제 의무 사항인가? (예: 개인정보보호, ESG공시)         |
|       +-- YES ---> 의무이행형, ROI는 정성평가(컴플라이언스 가치)            |
|       |                                                                |
|       +-- NO ---> Q2: 정량적 편익 산출 가능한가?                          |
|                    +-- YES ---> NPV/IRR 분석, Payback < 5년 선호          |
|                    |            (단, BCR ≥ 1.0, IRR ≥ WACC+α)            |
|                    |                                                      |
|                    +-- NO ---> 정성 편익 + McKinsey 4C / Wardley Map 활용  |
|                                                                          |
|   Q3: 투자 규모 > 100억? ---> 외부 PMO(PMO컨설팅) 활용, 단계별 Gate Review |
|   Q4: 멀티 벤더? ---> 통합 아키텍처(EA) 필수, RFP 시 EA 매핑 점수 반영   |
|   Q5: Cloud
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 565 / 800

<- **이전**: [564. IT 경영 관리 핵심 토픽 564번 시험 요약](/studynote/12_it_management/05_security_compliance/564_it_management_core_topic_564_exam_summary/)
**다음**: [566. IT 경영 관리 핵심 토픽 566번 시험 요약](/studynote/12_it_management/05_security_compliance/566_it_management_core_topic_566_exam_summary/) ->

---
