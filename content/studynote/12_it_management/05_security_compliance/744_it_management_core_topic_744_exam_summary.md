---
title: "744. IT 경영 관리 핵심 토픽 744번 시험 요약 (IT Management Core Topic 744 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 744. IT 거버넌스(Information Technology Governance) — 기술사 시험 심화 정리

> 본 노트는 정보관리기술사 시험 대비를 위해 **IT 거버넌스의 본질, 아키텍처(COBIT·ISO 38500·정보시스템 감리법 연계 모델), 비교 분석, 실무 판단 기준**을 심층 정리한 문서입니다.

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 단순한 "IT 관리"가 아니라, **이사회·경영진이 IT의 활용·성과·위험·준법(GRC: Governance·Risk·Compliance)을 의사결정·감독·통제하는 체계**이며, COBIT 2019(Governance & Management Objectives 40개)와 ISO/IEC 38500(원칙·모델·실행지침 3Layer)의 결합으로 표준화된다.
> 2. **가치**: Gartner 2023년 보고에 따르면 거버넌스 성숙도 Level 3 이상 도달 조직은 **IT 투자 ROI 28~35% 향상, 주요 프로젝트 실패율 42% 감소, 정보보호 사고 대응시간(MTTR) 60% 단축**, COSO 2013과 결합 시 SOX 404 컴플라이언스 비용 약 22% 절감 효과를 입증했다.
> 3. **판단 포인트**: 거버넌스 모델 선정 시 **(a) 통제형 vs 조언형(Direct/Advisory) 거버넌스, (b) 중앙집중형(CoE) vs 분산형(Federated), (c) Rule-based vs Principle-based, (d) Three Lines Model(3LoM) 채택 여부**라는 4가지 축을 기준으로 조직의 법적·문화적·기술적 맥락에 맞춰 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의 및 등장 배경

IT 거버넌스(IT Governance)는 **1992년 Sylvester & Sicoly**가 "Information Technology Governance"이라는 용어를 학술적으로 사용하기 시작했고, **1999년 ITGI(ISACA 산하)에서 IT Governance Institute 설립** 이후 본격적으로 체계화되었다. 한국에서는 **「정보시스템의 효율적 도입 및 운영 등에 관한 법률」(약칭: 정보시스템법)** 및 **「감리법」** 제정으로 법제적 기반이 마련되었으며, 2020년 「**디지털정부법**」 시행으로 공공부문 IT 거버넌스가 본격 제도화되었다.

### 1.2 필요성 — Old vs New Paradigm

| 구분 | Old Paradigm (1990~2010) | New Paradigm (2010~현재) |
| :--- | :--- | :--- |
| **핵심 관심사** | 시스템 가용성, 비용 절감 | 가치 창출(Value), 민첩성(Agility), 회복탄력성(Resilience) |
| **관리 대상** | 애플리케이션, 하드웨어, 데이터 | 데이터 거버넌스, AI 윤리, 클라우드·SaaS, 디지털 신뢰 |
| **거버넌스 주체** | CIO/CTO 중심 | **이사회 -> 경영진 -> CDO·CISO·CDAO**로 분산 |
| **규제 환경** | 단일 국가·단일 산업 규제 | GDPR·AI Act·DORA·개인정보보호법 등 초국적 규제 |
| **측정 지표** | 가동률(Uptime), TCO | **KPI(핵심성과지표)**·**KRI(핵심위험지표)**·**KCI(핵심통제지표)** 통합 대시보드 |
| **사고 대응** | 사후 대응(Reactive) | **사이버 회복탄력성(Cyber Resilience) + BCP/DR 자동화** |

### 1.3 글로벌 규제 환경 변화(2023~2025)

- **EU DORA(Digital Operational Resilience Act)**: 2025년 1월 발효, 금융기관 ICT 위험관리 5대 영역(Identify·Protect·Detect·Respond·Recover) 의무화
- **EU AI Act**: 2024년 8월 발효, 고위험 AI 시스템에 대해 Risk Management·Data Governance·Transparency·Human Oversight 4대 요구사항 적용
- **한국 개인정보보호법 개정(2023.9 시행)**: 가명정보·안전결제구역 도입, 영향평가(PIRA) 의무화
- **ISMS-P(2024 인증제 개편)**: 인증심사 주기 3년->2년, 클라우드·원격근무 통제 항목 강화
- **DGS(디지털정부서비스 표준)**: 2023년 7월 전면 개정, 14개 표준(아키텍처·연계·보안·데이터·AI 등) 의무화

```text
[글로벌·국내 규제 환경과 IT 거버넌스 연결 구조]
+----------------------------------------------------------------+
|                    이사회(Board) — 최종 책임                    |
|        +--------------------+---------------------+            |
|        |   전략위(Strategy)  |    리스크위(Risk)    |            |
|        +---------+----------+----------+----------+            |
|                  |                     |                       |
|        +---------v---------+ +---------v----------+            |
|        |  IT Steering Com.  | |  Risk Committee    |            |
|        |  (ITSC, 의사결정)  | |  (위험 감독)       |            |
|        +---------+---------+ +---------+----------+            |
|                  |                     |                       |
|        +---------v---------+ +---------v----------+            |
|        |   CIO (전략·BA)   | |   CISO (정보보호)  |            |
|        |   CDO (데이터)    | |   CRO (운영위험)   |            |
|        +---------+---------+ +---------+----------+            |
|                  |                     |                       |
|        +---------v---------+ +---------v----------+            |
|        |  Program/Project   | |  Operations/SOC    |            |
|        |  Management Office | |  GRC Platform      |            |
|        +--------------------+ +--------------------+            |
+----------------------------------------------------------------+
   ^                                                              |
   |                  보고 흐름(Reporting Line)                    |
   |   감사(Audit)·감리·제3자 평가 -> 이사회로 보고               |
   +--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **배의 키잡이**와 같다. 키잡이(거버넌스)가 별(전략·위험·준법)만 보지 않고, 동시에 풍향·조류·선체 상태를 통합 판단해야 배가 안전하게 항해할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 IT 거버넌스의 5대 핵심 구성요소 (ITGI 2008 + 2023 업데이트)

```text
[5대 영역 상세 아키텍처]
+---------------------------------------------------------------------+
|                                                                     |
|  ① Strategic Alignment(전략적 부합)                                |
|  +-------------------------------------------------------+         |
|  | Enterprise Goals ↔ IT Goals ↔ Enabler Goals          |         |
|  |   (13개)        (13개)        (40개)                  |         |
|  | Cascade Mapping을 통한 Value Realization              |         |
|  +-------------------------------------------------------+         |
|                              |                                     |
|  ② Value Delivery(가치 전달) ---+                                  |
|  +-------------------------------------------------------+         |
|  | Portfolio Mgmt · Benefits Realization · Investment Mgmt|        |
|  | Benefits:    NPV · IRR · Payback · ROI · TCO          |         |
|  | Tracking:    Earned Value Mgmt (EVM: CPI, SPI)        |         |
|  +-------------------------------------------------------+         |
|                              |                                     |
|  ③ Risk Management(위험 관리) ---+                                |
|  +-------------------------------------------------------+         |
|  | Risk Appetite -> Risk Identification -> Assessment      |         |
|  | -> Treatment (Accept·Mitigate·Transfer·Avoid)          |         |
|  | Frameworks: ISO 31000 · NIST CSF 2.0 · ISO 27005     |         |
|  +-------------------------------------------------------+         |
|                              |                                     |
|  ④ Resource Management(자원 관리)-+                                |
|  +-------------------------------------------------------+         |
|  | People · Process · Technology · Information(데이터)   |         |
|  | + 5th: Intangible(브랜드·평판·지식)                   |         |
|  +-------------------------------------------------------+         |
|                              |                                     |
|  ⑤ Performance Measurement(성과 측정)-+                            |
|  +-------------------------------------------------------+         |
|  | KPI Tree(Strategic -> Tactical -> Operational)          |         |
|  | BSC 4관점(Financial·Customer·Internal·Learning)       |         |
|  | + Sustainability(ESG·Green IT) 관점 추가              |         |
|  +-------------------------------------------------------+         |
+---------------------------------------------------------------------+
```

### 2.2 COBIT 2019 — 거버넌스·관리 목표 매핑

COBIT 2019는 **40개의 Governance/Management Objectives**를 **5개 도메인(EDM·APO·BAI·DSS·MEA)** 으로 구분한다.

| 도메인 | 목적 | 대표 목표 | 핵심 구성요소 | 담당 직책 |
| :--- | :--- | :--- | :--- | :--- |
| **EDM**(Evaluate, Direct, Monitor) | 거버넌스 의사결정 | EDM01(거버넌스 체계 수립), EDM02(가치 전달 보장), EDM03(위험 최적화), EDM04(자원 최적화), EDM05(이해관계자 투명성) | 거버넌스 의사결정 권한, 이해관계자 갈등 조정, 가치·위험 정량화 | **이사회·C-Level** |
| **APO**(Align, Plan, Organize) | 전략·계획·조직 | APO01~14 (예: APO02 전략, APO04 혁신, APO12 위험관리) | 목표 캐스케이드, 스킬/역량 매트릭스, 혁신 펀드 거버넌스 | **CIO·CDO** |
| **BAI**(Build, Acquire, Implement) | 구축·도입·구현 | BAI01~11 (예: BAI03 솔루션, BAI11 프로젝트관리) | 아키텍처 패턴, Agile/Waterfall 거버넌스, 형상관리 | **PMO·Enterprise Architect** |
| **DSS**(Deliver, Service, Support) | 운영·서비스·지원 | DSS01~06 (예: DSS01 운영, DSS04 연속성, DSS05 보안서비스) | SLA·OL·UC, 인시던트/문제관리, BCP/DR, 보안관제 | **COO·SRE·CISO** |
| **MEA**(Monitor, Evaluate, Assess) | 모니터링·평가·감사 | MEA01~04 (성과, 내부통제, 외부감사, 준수) | GRC 대시보드, 내부감사, 컴플라이언스 자동화 | **Internal Audit·CISO** |

### 2.3 ISO/IEC 38500:2015 — 6대 원칙과 3-Layer 모델

```text
[ISO 38500 - 3 Layer Governance Model]
+--------------------------------------------------------
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 744 / 800

<- **이전**: [743. IT 경영 관리 핵심 토픽 743번 시험 요약](/studynote/12_it_management/05_security_compliance/743_it_management_core_topic_743_exam_summary/)
**다음**: [745. IT 경영 관리 핵심 토픽 745번 시험 요약](/studynote/12_it_management/05_security_compliance/745_it_management_core_topic_745_exam_summary/) ->

---
