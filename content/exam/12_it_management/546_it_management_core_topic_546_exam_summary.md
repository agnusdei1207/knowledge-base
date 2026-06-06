---
title: "IT Management Core Topic 546 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, PMBOK 7th, ISO 27001 등 글로벌 프레임워크를 기반으로 **거버넌스-전략-운영-감사**의 4계층 구조에서 정렬(Alignment)·가치(Value)·위험(Risk)·자원(Resource)을 통합 최적화하는 경영 체계이다.
> 2. **가치**: 잘 설계된 IT 경영 체계는 IT 투자 대비 ROI를 평균 20~35% 향상시키고, 시스템 장애로 인한 손실을 50% 이상 절감하며, COBIT 기반 성숙도 1단계 도달 시 운영 효율 28% 개선 효과가 보고된다(Gartner/ISACA 통계).
> 3. **판단 포인트**: 중앙집중형 거버넌스 vs 분산형 페더레이션 모델 선택, Balanced Scorecard(BSC)와 KPI의 균형, Agile-Waterfall 하이브리드 적용, 그리고 사이버보안 리스크와 컴플라이언스(개인정보보호법, GDPR) 동시 충족이 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 비용 센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 격상되면서, IT 투자의 정당화·운영 효율성·리스크 통제를 통합 관리하는 체계의 부재가 기업의 디지털 경쟁력 약화로 직결되고 있다. 과거 CFO 중심의 CAPEX/OPEX 단순 회계 관리는 클라우드·AI·데이터 거버넌스 시대의 복잡한 의사결정 요구를 충족하지 못한다.

```text
+------------------------------------------------------------------+
|            IT 경영 관리 4계층 통합 프레임워크 (요약)               |
+------------------------------------------------------------------+
|                                                                  |
|   ① 거버넌스(Governance)    --  COBIT 2019, ISO 38500            |
|       |   이사회의 책임, 정책·통제, 이해관계자 가치제공            |
|       v                                                          |
|   ② 전략 기획(Strategy)     --  ISP(Information Strategy Planning)|
|       |   SWOT, TOBE 모델, BSC, Portfolio 분석                   |
|       v                                                          |
|   ③ 운영 관리(Operations)   --  ITIL 4 SVS, SIAM, DevOps         |
|       |   SLA, Incident/Problem/Change, SRE                      |
|       v                                                          |
|   ④ 통제·감사(Control/Audit)--  ISO 27001, SOX, IS Audit         |
|       |   K-ISMS, 개인정보보호법, GDPR, 내부통제                  |
|       v                                                          |
|   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   |
|   ✦ 핵심 4대 영역: Alignment / Value / Risk / Resource           |
+------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교**

- **기존(1990~2010)**: IT는 백오피스 비용, 개별 시스템 단위 관리, 프로젝트별 사후 평가, 사일로(Silo) 조직
- **신규(2015~현재)**: IT는 사업 동반자(Business Partner), EA 기반 통합 관리, 포트폴리오 사전 ROI 검증, DevSecOps·프로덕트 팀 단위

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같습니다. 각 악기(부서·시스템)가 제각각 연주하면 혼란이 생기듯, IT 자원이 정렬되지 않으면 기업 전체의 하모니가 무너집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **COBIT 2019의 거버넌스/관리 목표 체계(40개Governance & Management Objectives)**를 최상위 개념으로 두고, 하위에 프로세스·사람·기술·정보를 배치한 **Cascade Model**이다. IT 전략은 비즈니스 목표(예: 신규 수익원 확보)에서 출발하여 BSC 4관점(재무·고객·내부프로세스·학습성장)의 KPI로 변환되고, 이를 ITIL 4의 34개 Practice로 실행·운영하며, ISO 27001 Annex A 통제항목과 ISMS 인증으로 통제한다.

```text
            +-------------------------------------+
            |       비즈니스 전략 및 목표          |
            |  (Vision, Mission, SWOT, BSC 재무)  |
            +--------------+----------------------+
                           | 정렬(Alignment)
            +--------------v----------------------+
            |   IT 전략 & 거버넌스 (COBIT EDM)     |
            |   - Stakeholder Needs & Goals       |
            |   - Risk Appetite & Tolerance       |
            |   - 목표 계층화(Cascading Goals)     |
            +--------------+----------------------+
                           |
       +-------------------+-------------------+
       v                   v                   v
 +----------+        +----------+        +----------+
 |전략 기획  |        |서비스 운영|        |통제/감사  |
 |ISP,EA    |        |ITIL 4    |        |ISO27001  |
 |Portfolio |        |DevOps    |        |K-ISMS    |
 |BSC/KPI   |        |SRE,SIAM  |        |SOX,GDPR  |
 +----+-----+        +----+-----+        +----+-----+
      |                   |                   |
      +-------------------+-------------------+
                          |
            +-------------v-------------+
            |   Value Delivery & 측정    |
            |  ROI, NPV, TCO, NPS, SLA  |
            |  Maturity Level (1~5)     |
            +---------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회·IT 거버넌스 위원회 의사결정 | 5개 거버넌스 목표: Benefits Realization, Risk Optimization, Resource Optimization, Stakeholder Transparency, Goal Cascade |
| **APO (Align, Plan, Organize)** | 전략 정렬·아키텍처·포트폴리오 | EA(ArchiMate 3.2), TOGAF ADM, PMO 운영, BCM 수립, Vendor 관리, IT 예산 3개년 로드맵 |
| **BAI (Build, Acquire, Implement)** | 솔루션 도입·개발·테스트 | SDLC(폭포수/Agile/Scrum), CI/CD, 요구공학, 형상관리(Git), 품질보증(IEEE 830) |
| **DSS (Deliver, Service, Support)** | 일상의 서비스 운영·지원 | ITIL 4 34개 Practice(Incident, Problem, Change Enablement, Service Desk), SLA/OLa/UC, Capacity Mgmt |
| **MEA (Monitor, Evaluate, Assess)** | 통제·측정·감사 | KPI 대시보드(BSC), 내부감사(IIA 표준), 컴플라이언스 점검, COBIT maturity 5단계(0~5) |

**핵심 측정 지표 및 산식**

- **TCO (Total Cost of Ownership)**: H/W + S/W + 인건비 + 교육 + 유지보수 + 폐기비용의 LCC(Life Cycle Cost)
- **NPV (Net Present Value)**: `Σ(CFt / (1+r)^t) - 초기투자`, IT 투자 의사결정의 핵심 척도 (r=할인율, 통상 8~12%)
- **ROI**: `(Benefits - Costs) / Costs × 100%`, 통상 IT 프로젝트 기준 15% 이상 목표
- **성과 균형 점수(BSC Score)**: 재무(20%) + 고객(30%) + 내부프로세스(30%) + 학습성장(20%) 가중치
- **Maturity Level**: COBIT 0(Incomplete) -> 1(Initial) -> 2(Managed) -> 3(Defined) -> 4(Quantitatively Managed) -> 5(Optimizing)

- **📢 섹션 요약 비유**: COBIT의 EDM-APO-BAI-DSS-MEA는 마치 **병원 진료 시스템**과 같습니다. 의사(EDM)가 진단하고, 접수실(APO)이 일정을 잡고, 수술팀(BAI)이 시술하며, 간호사(DSS)가 돌보고, 의무기록팀(MEA)이 사후 점검을 합니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 주요 프레임워크는 서로 **상호보완적** 관계를 갖는다. COBIT은 거버넌스의 '뼈대', ITIL은 운영의 '살', PMBOK은 프로젝트의 '근육', ISO 27001은 통제의 '갑옷'이라 할 수 있다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 27001** |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스 & 관리 목표 | IT 서비스 운영 최적화 | 프로젝트 관리 원칙体系 | 정보보호 관리체계(ISMS) |
| **관점** | 비즈니스 가치 + 통제 | 서비스 가치사슬(SVS) | 원칙 + 도메인(8개) | 리스크 기반 통제 |
| **구조** | 40개 Governance/Mgmt 목표, EDM~MEA 5도메인 | 34개 Practice, 4차원 모델 | 12원칙, 8성능도메인 | Annex A 93개 통제, PDCA |
| **적용 범위** | 전사 IT 거버넌스 | IT 서비스 데스크·운영 | 프로젝트 단위 | 정보자산 전반 |
| **인증/성숙도** | ISACA 인증, Maturity 5단계 | PeopleCert/Axelos, Maturity 평가 | PMI 인증, PMO 운영 | KISA/BSI 인증, 3년 갱신 |
| **연계 방식** | EDM에서 ITIL/PMBOK 호출 | COBIT의 APO/DSS 영역과 매핑 | 프로젝트 포트폴리오는 APO 내 | MEA 감사 시 통제 기준 제공 |

**다른 시스템·도구와의 연결**

- **ERP(예: SAP S/4HANA, Oracle Cloud ERP)** ↔ IT 거버넌스: BCM, 사용자 접근통제, 변경관리 통제
- **SIEM(예: Splunk, IBM QRadar)** ↔ ISO 27001: A.8.16 모니터링 활동, A.5.28 정보보호 사고관리
- **Grafana / Power BI** ↔ BSC 대시보드: KPI 시각화, COBIT MEA의 측정 체계
- **Jira / ServiceNow** ↔ ITIL Practice: Incident, Change, Problem, Service Request 워크플로우
- **Kubernetes / Terraform** ↔ DevOps: BAI의 Build/Acquire와 IaC(Infrastructure as Code) 자동화

- **📢 섹션 요약 비유**: 네 개의 프레임워크는 **건물의 4가지 공종**입니다. COBIT은 설계도면, ITIL은 설비(전기·배관), PMBOK은 시공 일정, ISO 27001은 방화·방재 시스템입니다. 어느 하나만으로는 완전한 건물이 되지 않습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **비즈니스-IT 정렬도(Strategic Alignment Maturity)**: Henderson & Venkatraman 모델 기준 L1(Initiated) -> L5(Optimized) 중 현재 단계는? 정렬 갭(Gap) 2단계 이상 시 EA 재정비 필요
2. **IT 거버넌스 위원회 운영**: 분기 1회 이상 개최 여부, 의사결정 사항의 RACI(Responsible, Accountable, Consulted, Informed) 매트릭스 명확성, 크로스펑셔널 CIO-CFO-CISO 합동 의사결정 구조 유무
3. **IT 투자 포트폴리오 관리**: BCG/McKinsey 매트릭스 분류(Star/Cash Cow/Question Mark/Dog) 적용, 신규 투자 중 Question Mark 비중 30% 미만 유지, 포트폴리오 리밸런싱 주기 6개월 단위
4. **컴플라이언스 동시 충족**: 개인정보보호법(PIPA) + 정보통신망법 + GDPR + 전자상거래법 + 전자금융거래법 등 다중 규제 매핑표(RACI × Regulation Matrix) 작성, DPO(데이터보호책임자) 지정 및 정기 교육(연 8시간 이상)
5. **성숙도 측정 및 개선 로드맵**: COBIT 기반 5단계 평가, 연 1회 갭 분석, GRC(Governance-Risk-Compliance) 통합 플랫폼(예: SAP GRC, ServiceNow GRC) 도입 검토, Kaizen 방식 6시그마 DMAIC 적용

### 피해야 할 안티패턴

- **Shadow IT 방치**: 클라우드 SaaS(예: 미승인 ChatGPT Enterprise, 미인가 Dropbox) 사용을 통제 없이 허용 -> 데이터 유출·컴플라이언스 위반 위험. **대응**: CASB(Cloud Access Security Broker) 도입, 승인된 SaaS 카탈로그 운영
- **ROI 계산 생략 또는 형식화**: 정성적 효과만으로 투자 승인 -> 포트폴리오 균형 붕괴. **대응**: 재정적 ROI + 전략적 ROI + 리스크 감소 ROI의 3축 점수 모델 적용
- **KPI가 너무 많거나 측정 불가**: BSC에 50개 이상 KPI 등록, 실제 데이터 수집 안 됨. **대응**: 핵심 7~12개 KPI로 압축(Smart KPI: Specific/Measurable/Attainable/Relevant/Time-bound)
- **프로세스·사람·기술의 불균형**: 도구(예: ServiceNow)만 도입하고 거버넌스 문화 부재 -> 'Shelfware'화. **대응**: ADKAR(Kotter) 변화관리 모델 적용, 8단계 Kotter 변화 프로세스 수행
- **사일로 조직과 수직 보고체계**: CIO가 CFO/CTO 양쪽 이중 보고 -> 의사결정 지연. **대응**: IT Steering Committee에 사업부 VP 의무 참석, 매월 KPI 리뷰

- **📢 섹션 요약 비유**: 안티패턴은 마치 **자동차를 엔진만 좋은 차체로 운전하는 것**과 같습니다. 아무리 좋은 SIEM·Gartner Magic Quadrant 솔루션을 도입해도, 거버넌스 문화가 없이는 사고가 나는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

| 영역 | 정량 효과 | 정성 효과 |
| :--- | :--- | :--- |
| **IT 운영 효율** | TCO 20~35% 절감, MTTR 50% 단축 | 사용자 만족도(NPS) 상승, 부서 간 협업 개선 |
| **위험 관리** | 보안사고 60% 감소, 컴플라이언스 위반 80%v | 평판 보호, 규제 리스크 예측 가능 |
| **전략 가치** | IT 투자 ROI 평균 25% 향상, Time-to-Market 40% 단축 | 디지털 전환 성공률 2배, 사업敏捷성(Agility) 확보 |
| **감사·통제** | 내부감사 소요시간 70% 단축, 통제 누락 90%v | 투명한 보고 체계, 이사회 신뢰도^ |

**한계 및 리스크**

- 프레임워크 도입 시 초기 비용 1~3년 ROI 마이너스 가능성 (POC 단계)
- 조직 저항, 변화관리 실패 시 도구만 도입되는 'Shelfware' 현상
- 급변하는 기술(생성형 AI, 양자컴퓨팅)에 대한 거버넌스 갭 발생 가능
- 글로벌 규제 강화(AI Act, DORA 등)로 인한 통제 비용 지속 증가

**미래 트렌드**

- **AI 기반 GRC**: LLM을 활용한 통제 매핑·이상탐지·자동 보고
- **실시간 거버넌스**: DataOps + Observability 기반 KPI 실시간 측정
- **ESG-IT 융합**: Green IT·탄소배추 측정 지표가 IT 거버넌스에 통합
- **Autonomous Governance**: Self-Healing, Policy-as-Code(OPA) 기반 자동화 통제

- **📢 섹션 요약 비유**: 잘 짜인 IT 경영 관리는 **항해의 나
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 546 / 800

<- **이전**: [545. IT 경영 관리 핵심 토픽 545번 시험 요약](/studynote/12_it_management/05_security_compliance/545_it_management_core_topic_545_exam_summary/)
**다음**: [547. IT 경영 관리 핵심 토픽 547번 시험 요약](/studynote/12_it_management/05_security_compliance/547_it_management_core_topic_547_exam_summary/) ->

---
