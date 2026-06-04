+++
title = "676. IT 경영 관리 핵심 토픽 676번 시험 요약 (IT Management Core Topic 676 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(기술사 676번)는 **IT 거버넌스(COBIT 2019), IT 서비스 관리(ITIL 4), 프로젝트 포트폴리오 관리(PPM), 정보보안 거버넌스(ISMS-P), BCM/DRS**을 통합한 경영관리 프레임워크로, 기업의 디지털 전략과 IT 운영을 **가치사슬(Value Chain)** 관점에서 정렬·최적화하는 학문이다.
> 2. **가치**: 정량적으로는 IT 투자 대비 ROI **20~35% 향상**, 운영 비용(OpEx) **15~25% 절감**, 서비스 가용성 **99.95% -> 99.99%** 개선, 정성적으로는 **이사회-경영진-IT 간 정렬(Alignment)**을 통한 의사결정 투명성 및 리스크 가시화 확보.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① 중앙집중식 거버넌스 vs 페더레이션 모델**, **② 안정성 우선 vs 민첩성(Agility) 우선**, **③ 내재화(Insourcing) vs 아웃소싱 vs 클라우드(Co-sourcing)** 선택이며, 기술사적 판단 기준은 **비즈니스 크리티컬리티, TCO 5년 분석, 리스크 허용 한계(Risk Appetite), 그리고 규제 준수(Compliance)** 4축이다.

---

## Ⅰ. 개요 및 필요성

**IT 경영 관리(Information Technology Management)**는 4차 산업혁명 시대의 핵심 경영 자산으로서, 단순한 IT 운영 관리를 넘어 **"디지털 전략 ↔ IT 거버넌스 ↔ 서비스 전달 ↔ 가치 실현"**의 전(全) 사이클을 통합 관리하는 분야이다. 676번 시험은 정보관리 기술사(컴퓨터시스템응용, 정보보호, 데이터베이스, 소프트웨어공학)와 경영관리 분야(정보시스템감리사, CIO 컨설팅) 사이의 교차 영역을 다룬다.

### 📊 IT 경영 관리의 5대 배경

1. **디지털 전환(DX, Digital Transformation)** 가속화로 IT가 코어 비즈니스(Core Business)로 이동
2. **규제 환경 강화**: 개인정보보호법, EU GDPR, ESG 공시, 사이버보안 기본법, 클라우드 보안인증(CSAP)
3. **클라우드·AI·IoT 등 신기술 도입**에 따른 IT 비용 구조의 CapEx -> OpEx 전환
4. **공급망 다변화 및 글로벌 리스크** 증가 (코로나19, 반도체 부족, 지정학적 리스크)
5. **이해관계자(Stakeholder)** 다변화: 주주, 고객, 임직원, 감독기관, 협력사

```text
+----------------------------------------------------------------------+
|              IT 경영 관리 7대 관리영역 (7-Layer Pyramid)              |
+----------------------------------------------------------------------+
|                                                                      |
|                  [1] IT 전략 및 거버넌스 (Strategy)                   |
|                     COBIT 2019 / ISO 38500                           |
|                            ^                                          |
|                            |                                          |
|                  [2] IT 투자 및 포트폴리오 (Portfolio)                |
|                PPM, SAM, FinOps, TBM                                  |
|                            ^                                          |
|                            |                                          |
|                  [3] IT 서비스 운영 (Service Ops)                     |
|                ITIL 4, SRE, AIOps, SLA                               |
|                            ^                                          |
|                            |                                          |
|                  [4] 프로젝트 및 변경 관리 (Delivery)                 |
|              PMBOK 7, Agile(Scrum/SAFe), DevOps                      |
|                            ^                                          |
|                            |                                          |
|                  [5] 보안 및 컴플라이언스 (Security)                  |
|         ISMS-P, ISO 27001/27002/27701, NIST CSF, K-ISMS             |
|                            ^                                          |
|                            |                                          |
|                  [6] 리스크 및 연속성 (Risk/BCM)                      |
|         ISO 22301, ISO 31000, BCP/DR, ISO 27031                      |
|                            ^                                          |
|                            |                                          |
|                  [7] 측정 및 개선 (Measure)                            |
|              BSC, KPI/KRI, CSI, Maturity Model                       |
|                                                                      |
+----------------------------------------------------------------------+
```

**시대의 변천**: 1990년대 IT는 **비용 센터(Cost Center)** -> 2000년대 **비즈니스 지원(Back-office)** -> 2010년대 **전략적 동반자(Strategic Partner)** -> 2020년대 **비즈니스 그 자체(Business as IT, IT as Business)**로 진화하였다. 이에 따라 CIO의 역할도 단순 시스템 관리를 넘어 **CDO·CISO·CFO와 공동 의사결정**을 하는 **전략적 거버넌스 리더**로 변화했다.

- **📢 섹션 요약 비유**: IT 경영 관리를 **대형 병원 운영**에 비유하면, IT 전략 = 병원장(CEO)의 중장기 진료 방향, IT 거버넌스 = 의료윤리위원회, IT 서비스 = 진료·수술·입원 서비스, IT 보안 = 감염관리실, BCM = 응급의료센터, 성과 측정 = QI(Quality Improvement) 지표 체계이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 프레임워크 (COBIT 2019)

**COBIT 2019**는 ISACA에서 발표된 글로벌 IT 거버넌스 표준으로, **"거버넌스 시스템 및 거버넌스 컴포넌트 5개 영역"**으로 구성된다. 이전 COBIT 5 대비 **40개 관리 목표(Management Objective)**, **5개 도메인(EDM, APO, BAI, DSS, MEA)**, **포커스 영역(Focus Area: DevOps, 위험, 보안, SaaS 등)** 개념이 추가되었다.

```text
+------------------------------------------------------------------+
|              COBIT 2019 거버넌스 5대 도메인 (40 Management Obj.) |
+------------------------------------------------------------------+
|                                                                  |
|  +---- EDM ---------------------------------------------------+  |
|  | Governance of Enterprise IT (5개)                          |  |
|  |  • 평가·지침·모니터링(Evaluate, Direct, Monitor) 체계       |  |
|  +------------------------------------------------------------+ |
|                            |                                     |
|  +---- APO -----+---- BAI ----+---- DSS ------+---- MEA -----+  |
|  |  Align,      | Build,      | Deliver,      | Monitor,     |  |
|  | Plan, Organ. | Acquire,    | Service,      | Evaluate,    |  |
|  | (14개)       | Implement   | Support (6개) | Assess (4개) |  |
|  |              | (11개)      |               |              |  |
|  +--------------+-------------+---------------+--------------+  |
|                                                                  |
|  -> 7개 컴포넌트: Process / Organizational Structure / Principles,|
|                 Policies, Frameworks / Information / Culture,    |
|                 Ethics, Behavior / People, Skills, Competencies  |
|                 / Services, Infrastructure, Applications        |
+------------------------------------------------------------------+
```

### 2. IT 서비스 관리 (ITIL 4)

**ITIL 4**(2019)는 **서비스 가치 시스템(SVS, Service Value System)** 중심의 체제로 리팩토링되었다. 핵심은 **"가치(Value)"**이며, **34개 실천(34 Practices)**과 **가치 사슬(Value Chain)** 활동으로 구성된다.

```text
+----------------------------------------------------------------------+
|                   ITIL 4 Service Value System (SVS)                    |
+----------------------------------------------------------------------+
|                                                                      |
|  [기회/수요] ---> +----------------------------------+                |
|                 |   Service Value Chain (6 Activity)|                |
|  <--- 가치 ----  |  ① Plan -> ② Improve -> ③ Engage  |                |
|                 |  ④ Design & Transition           |                |
|                 |  ⑤ Obtain/Build                  |                |
|                 |  ⑥ Deliver & Support              |                |
|                 +----------------------------------+                |
|                            |                                         |
|                            v                                         |
|  +----------------------------------------------------------+        |
|  |  Guiding Principles (7): Focus on Value, Start Where You |        |
|  |   Are, Progress Iteratively, Collaborate, Think Whole,   |        |
|  |   Keep It Simple, Optimize & Automate                    |        |
|  +----------------------------------------------------------+        |
|                            |                                         |
|                            v                                         |
|  +----------------------------------------------------------+        |
|  |  Governance / Practices / Continual Improvement          |        |
|  |  • 14 General Mgmt Practices                              |        |
|  |  • 17 Service Mgmt Practices (ISM, Incident, Change,      |        |
|  |    Problem, Service Desk, SLA, Monitoring, etc.)          |        |
|  |  • 3 Technical Mgmt Practices                             |        |
|  +----------------------------------------------------------+        |
+----------------------------------------------------------------------+
```

### 3. 구성 요소별 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회-경영진 거버넌스 체계 | Benefits Realization, Risk Optimization, Resource Optimization, Transparency (4 영역) |
| **APO (Align, Plan, Organize)** | 전략-전술 정렬 및 계획 | 14개 프로세스: 전략, 포트폴리오, 재무, 위험, 인적자원, 공급관계, 품질 등 |
| **BAI (Build, Acquire, Implement)** | 솔루션 빌드/구축 | 11개 프로세스: 관리 요청, 요구사항, 변경, 수용, 조직변화 등 |
| **DSS (Deliver, Service, Support)** | 일상적 운영·지원 | 6개 프로세스: 운영, 서비스 요청, 사고, 문제, 연속성, 보안운영 |
| **MEA (Monitor, Evaluate, Assess)** | 성과측정 및 개선 | 4개 프로세스: 성과/규제 준수/목표달성 모니터링 및 내부통제 평가 |
| **SLA (Service Level Agreement)** | 서비스 품질 계약 | OLAs(운영계약) / UC(지원계약) / SLR(서비스수준요구) 다계층 구조, 가용성·응답성·처리율·정확도 4대 메트릭 |
| **BCM (Business Continuity Mgmt)** | 사업연속성 | BIA(영향분석) -> RTO/RPO/MTPD 산정 -> 전략수립 -> BCP/DRP -> 훈련·점검, ISO 22301 |
| **ISMS (정보보호관리체계)** | 정보보안 거버넌스 | 정책-식별-보호-탐지-대응-복구의 NIST CSF/P 함수와 매핑, K-ISMS-P 인증 |
| **FinOps / TBM (Technology Business Mgmt)** | IT 비용 투명화 | Showback / Chargeback 모델, Unit Cost 산정, 클라우드 워크로드 단가화 |

### 4. 핵심 메트릭과 알고리즘

**(1) IT 서비스 가용성 계산식**

```
시스템 가용성(Availability) = MTBF / (MTBF + MTTR)
연간 가용성(%) = (총가용시간 - 장애시간) / 총가용시간 × 100

예) 99.99% (Four-Nine) 가용성 -> 연간 허용 장애시간 = 52.56분
    99.999% (Five-Nine) 가용성 -> 연간 허용 장애시간 = 5.26분
```

**(2) TCO(Total Cost of Ownership) 5개년 분석**

```
TCO = CapEx(서버/스토리지/네트워크) + OpEx(인건비/라이선스/전력/냉각/보안/훈련)
     + Risk Cost(장애/보안사고/규제위반 벌금의 확률기대값)
     + Opportunity Cost (사일로 시스템의 기회비용)

TCO 최적화 핵심: HW : SW : 운영비 = 20 : 30 : 50 비율이 일반적
```

**(3) TBM Unit Economics**

```
단위서비스 비용 = (IT 총 비용 × 서비스 소비율) / (서비스 단위 × 사용량)
예) 트랜잭션당 비용 = 0.0008 USD, 사용자당 비용 = 4.2 USD/월
```

- **📢 섹션 요약 비유**: COBIT의 5개 도메인을 **대형 항공사의 운영**에 비유하면, EDM = 이사회·CEO의 의사결정, APO = 노선·수익·기체계획, BAI = 신기종·인테리어·인증 획득, DSS = 실제 운항·정비·승객 서비스, MEA = 연착률·만족도·안전성 평가이다.

---

## Ⅲ. 비교 및 연결

### 1. 주요 IT 거버넌스/관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001/27002** | **PMBOK 7** | **CMMI 2.0** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·컴플라이언스 | IT 서비스 운영·가치 | 정보보안 관리 | 프로젝트 관리 | 프로세스 성숙도 |
| **관리 대상** | 40개 관리목표 | 34개 Practice | 93개 통제항목 | 12원리, 8성과영역 | 5성숙도 레벨 |
| **적용 범위** | 전사 IT(Enterprise IT) | IT 서비스·운영 | 정보보안(ISMS) | 단일 프로젝트 | 조직(개발·운영) |
| **강점** | 거버넌스-리스크-컴플라이언스 통합 | DevOps·Agile 친화 | 글로벌 보안 인증 표준 | 인적·비즈니스 측 강조 | 정량적 측정 |
| **약점** | 구현 복잡도 높음 | 운영 부서 위주 | 기술 트렌드 반영 지연 | IT 외 영역 적용 한계 | 도입 비용·기간 큼 |
| **결합 활용** | ITIL로 운영->COBIT로 거버넌스 보고, ISO 27001을 통제 매핑 |  |  |  |  |

### 2. 프로젝트 관리 방법론 비교

| 구분 | **Waterfall** | **Agile(Scrum)** | **SAFe** | **DevOps** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **요구사항 변화** | 기피 | 환영 | 환영 | 환영 | 사례별 |
| **반복 주기** | 단계별 | 2~4주 Sprint | PI(8~12주) | 지속적 통합·배포 | 적용 중립 |
| **팀 규모** | 대형 가능 | 소형(5~9명) | 대규모(50~125명) | 소~중형 | 무관 |
| **고객 협업** | 인수 시점 | 매 Sprint | PI Planning | 지속적 | 인접 |
| **적합 환경** | 정부·건설·제조 | SW·앱 | 금융·대기업 | 클라우드·SaaS | 모든 산업 |
| **리스크 관리** | 사후적 | 매 Sprint 회
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 676 / 800

<- **이전**: [675. IT 경영 관리 핵심 토픽 675번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/675_it_management_core_topic_675_exam_summary/)
**다음**: [677. IT 경영 관리 핵심 토픽 677번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/677_it_management_core_topic_677_exam_summary/) ->

---
