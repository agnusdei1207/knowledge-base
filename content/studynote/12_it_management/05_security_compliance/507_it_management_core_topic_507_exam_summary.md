---
title: "IT Management Core Topic 507 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 507. IT 경영 관리 핵심 토픽 507번 시험 요약 (IT Management Core Topic 507 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019(거버넌스/관리 목표 40개), ITIL 4(서비스 가치 시스템 34개 실무 가이드), ISO 38500(6개 원칙) 프레임워크를 기반으로 **전략-포트폴리오-프로그램-프로젝트-운영-서비스** 6계층 가치사슬을 통합 운영하는 경영 체계이다.
> 2. **가치**: McKinsey 기준 디지털 성숙도 상위 25% 기업은 EBIT 마진 3.6%p, 매출 성장률 2.5배 차이를 보이며, 성숙한 IT 거버넌스 도입 시 IT 투자 ROI 평균 25% 향상, 프로젝트 실패율 50%->15%로 감소, 이사회-현업-IT 정렬도(Alignment Index) 30%->78% 개선 효과를 창출한다.
> 3. **판단 포인트**: 중앙집중(CoE) vs 분산형(Federated) 거버넌스 모델, Build vs Buy vs Cloud, Capex vs Opex(클라우드 전환 시 18-36개월 ROI), Waterfall vs Agile vs Hybrid(SAFe 6.0) 등 아키텍처 의사결정 시 **TCO 5년 기준**, **비즈니스 영향도(Likelihood×Impact)**, **규제 컴플라이언스** 3축을 반드시 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 업무 자동화 수단에서 **비즈니스 핵심 경쟁력**으로 부상하면서, IT 투자 1,000억 원 규모 기업에서 평균 30% 이상의 IT 예산이 미활용되거나 실패하는 현상이 발생한다. 한국정보화진흥원의 2023년 조사에 따르면 국내 대기업 IT 예산 중 **23%가 사일로 시스템**, **17%가 중복 투자**, **12%가 미사용 라이선스**로 낭비되고 있다. IT 경영 관리는 이러한 문제를 해결하기 위해 **거버넌스(의사결정 구조), 전략(방향성), 포트폴리오(자원 배분), 운영(서비스 전달)**의 4대 영역을 통합 관리하는 체계를 의미한다.

기존의 IT 관리(1990~2000년대)는 시스템 단위 개발·유지보수에 집중했으나, 클라우드·AI·데이터 시대의 IT 경영은 **가치지향(Val IT)**, **위험관리(Risk IT)**, **컴플라이언스(ISO 38500)**, **민첩성(Agile@Scale)**이 통합된 차원 높은 체계를 요구한다. 특히 2024년 이후 ESG, AI 윤리, 데이터 주권(데이터3법, EU AI Act) 등 신규 규제 환경에서 IT 거버넌스는 선택이 아닌 **의무**가 되었다.

```text
[ IT 경영 관리 6계층 가치사슬(Value Chain) 아키텍처 ]

  +--------------------------------------------------------------+
  |  Level 1: IT 전략(IT Strategy)                                |
  |   +- 디지털 로드맵, 3-5년 IT 비전, KPI(OKR) 연계              |
  +--------------------------------------------------------------+
  |  Level 2: IT 거버넌스(IT Governance)                          |
  |   +- 이사회-경영진-IT 정렬, COBIT 2019 40개 목표, RACI 매트릭스|
  +--------------------------------------------------------------+
  |  Level 3: 포트폴리오(Portfolio)                               |
  |   +- 프로젝트 우선순위화, BCG/GE 매트릭스, 자원이관             |
  +--------------------------------------------------------------+
  |  Level 4: 프로그램/프로젝트(Program/Project)                  |
  |   +- PMBOK 7, SAFe 6.0, MS Project/Jira, Stage-Gate          |
  +--------------------------------------------------------------+
  |  Level 5: IT 운영(IT Operations)                              |
  |   +- ITIL 4 Service Value System, ITSM, Change/Incident      |
  +--------------------------------------------------------------+
  |  Level 6: 서비스 전달(Service Delivery)                        |
  |   +- SLA 99.9%^, MTTR/MTTF, NOC, AIOps                      |
  +--------------------------------------------------------------+
                          ^
                          | 가치(Value) 피드백 루프
                          | (Val IT - 가치측정 프레임워크)
```

**기존 vs 신규 패러다임 비교**:
- **기존(IT 관리 1.0)**: 시스템 단위, Capex 중심, Waterfall, 부서별 사일로, IT 주도 의사결정
- **신규(IT 경영 2.0)**: 가치 단위(Value Stream), Opex/As-a-Service, Agile/DevOps, 플랫폼화, 비즈니스-IT 공동 의사결정

- **📢 섹션 요약 비유**: IT 경영 관리는 **대형 크루즈선의 항해 시스템**과 같다. 함장(이사회)이 방향을 정하고, 항해사(거버넌스 위원회)가 코스를 잡으며, 기관장(거버넌스 오피스)이 연료 배분(포트폴리오)을 결정하고, 각 부서(프로젝트/운영)가 협력해 안전하게 목적지에 도달하게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 메커니즘은 **PDCA(Plan-Do-Check-Act) + 가치사슬(Value Chain)**의 이중 루프이다. 상위 루프는 전략-거버넌스-포트폴리오의 **장기 의사결정 루프**(연간/분기), 하위 루프는 운영-서비스의 **단기 운영 루프**(일/주)이다. 두 루프가 **KPI 대시보드(예: Power BI + Grafana)**를 통해 통합 모니터링된다.

COBIT 2019의 **Governance System**은 5개 도메인(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess) 40개 관리목표로 구성되며, 각 목표는 **Process Capability Level 0~5**(ISO 15504 PAM 기반)로 측정된다. 목표 1(EDM01: 거버넌스 프레임워크), 목표 2(EDM02: 가치 전달), 목표 5(EDM05: 이해관계자 참여)가 핵심 거버넌스 목표로, 기술사 시험에서 빈도가 가장 높다.

```text
[ COBIT 2019 Governance & Management Objectives 40개 구조 ]

  +------------------------------------------------------+
  |  EDM (Evaluate, Direct, Monitor) - 5개 목표          |
  |   EDM01 거버넌스프레임워크 / EDM02 가치전달          |
  |   EDM03 리스크최적화 / EDM04 자원최적화               |
  |   EDM05 이해관계자투명성                             |
  +------------------------------------------------------+
  |  APO (Align, Plan, Organize) - 14개 목표              |
  |   APO01~APO14: 전략, 포트폴리오, 예산, 조직, 아키텍처|
  +------------------------------------------------------+
  |  BAI (Build, Acquire, Implement) - 11개 목표          |
  |   BAI01~BAI11: 솔루션, 아키텍처, 변경, 전환, 수용성   |
  +------------------------------------------------------+
  |  DSS (Deliver, Service, Support) - 6개 목표           |
  |   DSS01~DSS06: 운영, 서비스요청, 인시던트, 보안연속성 |
  +------------------------------------------------------+
  |  MEA (Monitor, Evaluate, Assess) - 4개 목표           |
  |   MEA01~MEA04: 성과/제어 모니터링, 내부통제, 컴플라이언스|
  +------------------------------------------------------+
  ※ 각 목표당 7개 프로세스 활동(Plan/Do/Check/Act) = 280개 활동
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee (ITSC)** | 최고 의사결정 기구 | CFO·CIO·CDO·사업본부장 참석, 분기 1회 정례, RACI 매트릭스 기반 책임 할당, 거버넌스 의사결정 80% 이상을 여기서 확정 |
| **PMO (Project Management Office)** | 프로젝트 통합 관리 | Gartner 5단계 모델(Supporting/Controling/Directive/Estrategic/Governing), Earned Value Management(EVM) 지표(CPI, SPI), Stage-Gate(Go/No-Go 의사결정) |
| **COBIT/ITIL 통합 거버넌스 플랫폼** | 프레임워크 자동화 | ServiceNow GRC, SAP GRC, IBM OpenPages, Archer — 프로세스 40개와 인시던트/변경/릴리스의 양방향 추적성(Traceability) 확보 |
| **IT 재무 관리(FinOps/ITFM)** | IT 비용 최적화 | Apptio, CloudHealth, VMWare Aria Cost — Capex/Opex 분리, TCO 5년 분석, Showback/Chargeback(할당 기준 1,200원/FTE·월) |
| **Value Office/EA(Enterprise Architecture)** | 전략-구현 연계 | TOGAF 10 ADM(Architecture Development Method), Zachman 6×6 매트릭스, capability-based planning(역량 매핑) |
| **AIOps/관제** | 운영 자동화 | Splunk/Datadog/New Relic + ML 이상탐지, MTTR 평균 65% 단축, MTTD 4시간->15분 |

**핵심 측정 지표(KPI)**:
- **Alignment Index**: (전략 연계 프로젝트 수)/(전체 프로젝트 수) × 100%, 목표 80%^
- **IT ROI**: (가치 실현 - 총비용)/(총비용) × 100%, 산업 평균 15-25%
- **Project Success Rate**: 3-Triple Constraint(Scope/Schedule/Budget) 모두 충족 비율, PMBOK 7 기준 71% 목표
- **Capability Level**: ISO 15504 PAM, 목표 Level 3(Defined) 이상
- **NPS/SLA**: 가용성 99.9%(연 8.76시간 장애 허용), 응답시간 P95 < 2초

- **📢 섹션 요약 비유**: COBIT 2019의 40개 목표는 **비행기의 40개 계기판**과 같다. 속도고도계(EDM), 연료게이지(APO), 엔진온도(BAI), 기압(DSS), 블랙박스(MEA)가 모두 정상 범위 안에 있어야 안전한 비행(=IT 운영)이 가능하다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 3대 핵심 프레임워크(COBIT, ITIL, PMBOK)와 4대 현대 방법론(SAFe, DevOps, FinOps, MLOps) 비교는 기술사 시험의 **단골 출제 영역**이다. 시험에서는 "프레임워크 간 차이점과 통합 적용 방안" 형태로 빈번히 출제된다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7** |
| :--- | :--- | :--- | :--- |
| **목적** | 거버넌스 + 관리(What/Why) | 서비스 관리(How) | 프로젝트 관리(How) |
| **구조** | 40 Governance/Management Objectives | 34 Practices + SVS | 12 Project Management Principles |
| **관점** | 경영진-감사 관점(E2E 거버넌스) | 서비스 가치사슬(SVC) | 프로젝트-제품 라이프사이클 |
| **성숙도 모델** | ISO 15504 PAM(CMMI 연계) | 4축 모델(서비스 가치) | 성과측정(PERC 모델) |
| **주 사용자** | CIO, 감사인, 이사회 | 서비스 매니저, 운영팀 | PMO, 프로젝트 매니저 |
| **연계 프레임워크** | ISO 38500, Val IT, Risk IT | ISO 20000, SIAM, VeriSM | PRINCE2, ISO 21502, SAFe |
| **출시/최신버전** | 2019(40 Objectives) | 2019(4) / 2023(Foundation 갱신) | 2021(7th) / 2023 갱신 |
| **측정 기준** | Capability Level 0~5 | Maturity Model 1~5 | Outcome-based KPI |
| **적용 범위** | 전사 IT(Enterprise-wide) | 서비스 카탈로그 단위 | 단위 프로젝트 |
| **기술사 출제 빈도** | ★★★★★ | ★★★★ | ★★★★ |

**IT 운영 방법론 비교**:

| 구분 | **Waterfall** | **Agile (Scrum)** | **SAFe 6.0** | **DevOps** |
| :--- | :--- | :--- | :--- | :--- |
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 507 / 800

<- **이전**: [506. IT 경영 관리 핵심 토픽 506번 시험 요약](/studynote/12_it_management/05_security_compliance/506_it_management_core_topic_506_exam_summary/)
**다음**: [508. IT 경영 관리 핵심 토픽 508번 시험 요약](/studynote/12_it_management/05_security_compliance/508_it_management_core_topic_508_exam_summary/) ->

---
