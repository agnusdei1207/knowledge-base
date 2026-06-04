+++
title = "486. IT 경영 관리 핵심 토픽 486번 시험 요약 (IT Management Core Topic 486 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 EDM(평가·지시·모니터링) 40개 관리 목표와 ITIL 4의 34개 практика, ISO 38500의 6원칙을 통해 **이사회-경영진-실무** 3계층으로 연결되며, EA(Enterprise Architecture)는 TOGAF ADM 사이클(8단계 Phase A~H)로 전략-비즈니스-데이터-애플리케이션-기술 4계층을 정렬한다.
> 2. **가치**: 글로벌 조사(Deloitte 2023)에 따르면 성숙한 IT 거버넌스 도입 기업은 **프로젝트 실패율 38%↓, ROI 2.7배↑, 사이버 사고 대응시간 64% 단축**, ISO 38500 인증 기업은 IT 투자 회수기간( payback period ) 평균 18개월 단축 효과를 나타낸다.
> 3. **판단 포인트**: **①** 중앙집중형(CoE) vs 분산형(Federated) 거버넌스 모델 선택 시 조직 규모(>1,000명 임계점), **②** EA 방법론은 TOGAF(대기업) vs Zachman(규제산업) vs FEAF(공공기관), **③** 클라우드 전환 시 CapEx→OpEx 전환율 60~70% 시 ROI BEP 도달이라는 트레이드오프를 정량적으로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

정보화 사업의 규모가 연평균 15% 이상 성장하면서(한국정보화진흥원 2023), 단일 부서 단위의 IT 운영은 **전사적 정렬(Strategic Alignment)**, **가치 실현(Value Delivery)**, **리스크 관리(Risk Management)**, **자원 최적화(Resource Management)**, **성과 측정(Performance Measurement)** — 이 5대 영역을 동시에 통제할 수 없게 되었다. 과거 2000년대 초반의 **프로젝트 단위 산발적 IT 투자**(Project-centric Approach)는 평균 ROI 0.87배(즉, 손실)를 기록했으며, 2000년대 중반 ITIL v2의 **프로세스 중심 운영**, 2010년대 COBIT 5의 **거버넌스-관리 분리**, 그리고 2020년대 COBIT 2019의 **위험-목표-컴포넌트 3축 맞춤(Focus Area)** 으로 패러다임이 진화했다.

특히 2024년 기준 한국 공공부문은 **클라우드 이용 촉진 및 정보보호에 관한 법률**(2024.1. 시행)에 따라 SaaS·IaaS 도입이 의무화되었고, 민간은 ESG 공시 의무화(2025년), EU AI Act(2024.8. 시행) 등으로 인해 **AI 거버넌스**, **데이터 거버넌스**, **그린 IT**가 새로운 거버넌스 핵심축으로 부상했다. 따라서 정보관리기술사 관점에서 **"법·제도 준수 + 전략적 가치 + 기술 실행력"** 을 통합 관리할 수 있는 거버넌스 프레임워크 설계 역량이 필수 역량으로 요구된다.

```text
[ 정보화 전략 수립 의사결정 계층 구조 ]

   ┌─────────────────────────────────────────────┐
   │   이사회 (Board of Directors)               │
   │   · IT 거버넌스 최고 의사결정                │
   │   · ISO 38500 6원칙: 책임·전략·수행·적합·규율·인간│
   └──────────────┬──────────────────────────────┘
                  │ (Oversight)
   ┌──────────────▼──────────────────────────────┐
   │   IT 전략위원회 (Steering Committee)         │
   │   · COBIT 2019 EDM 영역                     │
   │     EDM01 거버넌스 체계 수립                 │
   │     EDM02 혜택 실현                         │
   │     EDM03 위험 최적화                       │
   │     EDM04 자원 최적화                       │
   │     EDM05 투명성 보장                       │
   └──────────────┬──────────────────────────────┘
                  │ (Direction)
   ┌──────────────▼──────────────────────────────┐
   │   PMO (Program Management Office)           │
   │   · 다중 프로젝트 포트폴리오 관리            │
   │   · P3O(Portfolio, Programme, Project Office)│
   │   · KPI 대시보드 · 위험 통합관리             │
   └──────────────┬──────────────────────────────┘
                  │ (Execution)
   ┌──────────────▼──────────────────────────────┐
   │   실무 조직 (BAU + 프로젝트팀)              │
   │   · ITIL 4 Service Value Chain              │
   │     Plan→Engage→Design→Obtain→Build→Deliver│
   │     →Support                                │
   │   · DevOps · SRE · Agile Squad              │
   └─────────────────────────────────────────────┘
```

**구 vs 신 패러다임 비교**
- **구 패러다임 (2000년대 이전)**: IT = 비용(Cost Center) → 예산 대비 실적( Budget vs Actual ) 중심 통제, 기능별 사일로(Finance, HR, SCM 각각 독립 시스템)
- **신 패러다임 (2024년)**: IT = 가치(Value Engine) → **Total Economic Impact(TEI)** 측정, **OKR(Objectives & Key Results)** 기반 성과관리, 데이터-플랫폼-AI-보안의 4축 통합 거버넌스

- **📢 섹션 요약 비유**: IT 거버넌스 없는 조직은 **교향악단 단원들이 각자 다른 악보로 연주하는 것**과 같다. 작곡가(거버넌스 프레임워크)가 있어야 모든 악기가 하나의 교향곡(비즈니스 목표)을 연주할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스-관리(Service Management)-실행(Operations)을 통합하는 **3-Tier 아키텍처**는 COBIT 2019의 **Governance vs Management** 구분에 기반한다. **거버넌스(평가·지시·모니터링)** 는 이사회·전략위원회 영역이며, **관리(계획·구축·운영·모니터링: PBRM)** 는 실무 영역이다. 각 영역은 다시 **Process / Organizational Structure / Information Flows / People, Skills & Competencies / Principles, Policies & Frameworks / Culture, Ethics & Behavior / Services, Infrastructure & Applications** — 이 **7가지 컴포넌트(COBIT 2019 Component)** 로 구성된다.

```text
[ COBIT 2019 + ITIL 4 + ISO 38500 통합 참조 모델 ]

   ╔══════════════════════════════════════════════════════════╗
   ║  ISO/IEC 38500 IT 거버넌스 6원칙 (최상위 정책 프레임)  ║
   ║  ① 책임(Responsibility)  ② 전략(Strategy)              ║
   ║  ③ 수행(Acquisition)     ④ 수행(Performance)           ║
   ║  ⑤ 적합(Conformance)     ⑥ 인간(Human Behavior)        ║
   ╚════════════════════╤═════════════════════════════════════╝
                        │ (Standards)
   ┌────────────────────▼────────────────────────────────────┐
   │  COBIT 2019: 40개 관리목표 + 5개 거버넌스목표           │
   │   · 거버넌스 도메인 (EDM01~EDM05)                      │
   │   · 관리 도메인                                         │
   │     APO(Align, Plan, Organize) 14개                     │
   │     BAI(Build, Acquire, Implement) 11개                 │
   │     DSS(Deliver, Service, Support) 6개                  │
   │     MEA(Monitor, Evaluate, Assess) 4개                 │
   │   · Focus Area: 사이버보안, DevOps, 디지털전환, AI     │
   └────────────────────┬────────────────────────────────────┘
                        │ (Process Detail)
   ┌────────────────────▼────────────────────────────────────┐
   │  ITIL 4 Service Value System (SVS)                      │
   │   · 7 Guiding Principles                                │
   │   · 4 Dimensions of Service Management                  │
   │     Organizations & People · Information & Technology   │
   │     Partners & Suppliers · Value Streams & Processes    │
   │   · 34 Practices (구 v3의 26 프로세스 확장)             │
   │     ex) Incident Mgmt, Change Enablement,               │
   │         Service Request Mgmt, Incident Problem,         │
   │         Service Level Mgmt 등                            │
   │   · Service Value Chain (Plan→Engage→Design→Build→     │
   │     Transition→Operate→Improve 6활동)                   │
   └────────────────────┬────────────────────────────────────┘
                        │ (Operational Execution)
   ┌────────────────────▼────────────────────────────────────┐
   │  실행 계층: 기술 스택 및 자동화                          │
   │   · AIOps (Datadog, Splunk ITSI)                        │
   │   · IaC: Terraform / Ansible / Pulumi                   │
   │   · CMDB: ServiceNow CMDB / BMC Discovery               │
   │   · ITSM: ServiceNow / Jira Service Mgmt                │
   │   · Observability: OpenTelemetry + Prometheus + Grafana │
   └─────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스) 계층** | 이사회·전략위 의사결정 | COBIT 2019 EDM01~05: 평가(Evaluate)·지시(Direct)·모니터링(Monitor) 루프 60일 주기, **RACI 차트**로 의사결정 권한 명문화 |
| **APO(정렬·계획·조직)** | 전략→IT 정렬 | **Balanced Scorecard(BSC) 4관점**(Financial/Customer/Internal/Learning), **IT 투자 우선순위 모델**(HPE 5단계), **KPI 캐스케이드** 전략→CSF→KPI→KPI 측정값 |
| **BAI(구축·획득·실행)** | 솔루션 도입 및 구현 | **프로젝트 관리**: PMBOK 7th(8 Performance Domains), **애자일**: Scrum(3~9명/2~4주 스프린트), **DevOps**: DORA 4 Metrics(배포빈도·리드타임·변경실패율·복구시간) |
| **DSS(서비스·지원)** | 운영 서비스 제공 | **ITIL 4 34개 практика**: Incident(SLA P1 1시간, P2 4시간), Problem(근본원인분석 RCA: 5-Why, Ishikawa, Kepner-Tregoe), **Change Enablement**(CAB + Risk-based CAB) |
| **MEA(모니터링·평가)** | 성과 측정 및 개선 | **BS 15000 / ISO 20000** 인증, **내부 통제**: SOX 404 IT-GC(IT General Control), **외부 감사**: ISMS-P, PIMS(ISO 27701) |

**핵심 측정 지표 (KPI) 및 임계값**
- **가용성(Availability)**: 월간 99.95% (=연간 다운타임 4.38시간) — Tier IV 데이터센터 기준
- **MTTR(Mean Time To Repair)**: Critical 시스템 30분 이내, Major 4시간, Minor 24시간
- **MTBF(Mean Time Between Failures)**: 720시간(30일) 이상 목표
- **MTTD(Mean Time To Detect, 보안)**: 24시간 이내 (NIST CSF 측정)
- **변경 실패율(CFR)**: 우수 조직 0~15%, 보통 16~30%, 미흡 31% 이상
- **배포 빈도(Deployment Frequency)**: Elite 조직 하루 수회, High 1일~1주일, Medium 1주~1개월

- **📢 섹션 요약 비유**: COBIT 2019는 **"자동차의 핸들·페달·계기판"** 이고, ITIL 4는 **"자동차 정비 매뉴얼"**, ISO 38500는 **"운전 면허 규정"** 이다. 핸들로 방향(거버넌스)을 잡고, 매뉴얼로 정비(서비스관리)하며, 규칙(원칙)으로 안전운전(컴플라이언스)을 보장한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **TOGAF 9.2/10** | **ISO 27001/27002** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 통합 | IT 서비스 관리 운영 | IT 거버넌스 표준 | 전사 아키텍처(EA) 수립 | 정보보안 관리체계(ISMS) |
| **대상 계층** | 이사회 ↔ 실무 전체 | 실무 운영팀 중심 | 이사회·경영진 | 아키텍처 설계자 | CISO·보안팀 |
| **구조** | 40 관리목표 + 7 컴포넌트 | 34 практика + SVS | 6 원칙 + 모델 | ADM 8 Phase + Content Metamodel | 93 통제(Annex A 2022) |
| **측정/인증** | ISACA 감성 인증(자격증) | PeopleCert AXELOS 자격증 | BSI 인증 | The Open Group 인증 | KISA·BSI 인증 |
| **적용 시점** | 거버넌스 정착 초기 | 서비스 운영 성숙기 | 정책 수립·감사 | 전략-아키텍처 정렬 | 보안 위험 발생 후·사전 |
| **통합 방식** | EDM↔PBRM 라사이클링 | SVS + Value Stream | COBIT EDM과 매핑 | Phase A Architecture Vision | APO12(위험관리)와 연동 |
| **장점** | 컴플라이언스·감사 강점, 2019부터 유연성 ↑ | 실무 적용성, 자동화 친화 | 국제 표준, 간결성 | 업계 사실 표준(de facto) | 글로벌 보안 표준 |
| **단점** | 40 목표 과부하, 학습곡선陡 | 34 практика 부담, v3→v4 호환성 | 거버넌스 외 영역 미흡 | 구현 도구(Tool) 부재 | 통제 93개 과다, 우선순위 필요 |
| **비용(연간)** | 가이드북 $200~400 | Foundation $400, Master $1,500+ | 인증 $5K~30K | 가이드 $500 | 인증 $15K~50
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 486 / 800

← **이전**: [485. IT 경영 관리 핵심 토픽 485번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/485_it_management_core_topic_485_exam_summary/)
**다음**: [487. IT 경영 관리 핵심 토픽 487번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/487_it_management_core_topic_487_exam_summary/) →

---
