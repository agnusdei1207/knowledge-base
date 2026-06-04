+++
title = "559. IT 경영 관리 핵심 토픽 559번 시험 요약 (IT Management Core Topic 559 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019, ISO/IEC 38500, ITIL 4 프레임워크를 기반으로 IT 전략-실행-성과-준법의 4대 영역을 통합 관리하며, 거버넌스(지휘·통제)와 관리(운영·실행)를 명확히 분리하여 의사결정 권한과 책임 체계를 확립하는 경영 체계임.
> 2. **가치**: 글로벌 IDC 조사에 따르면 성숙한 IT 거버넌스 도입 기업은 IT 투자 ROI를 평균 28% 개선하고, 프로젝트 실패율을 42% 감소시키며, IT 비용 대비 비즈니스 가치 창출 비율(Business Value per IT Spend)을 3.2배 높임.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Decentralized) 거버넌스 모델, COBIT 2019의 40개 관리목표 중 우선순위 선정을 위한 Design Factor 10종 적용, Balanced Scorecard 4관점(재무·고객·내부프로세스·학습성장) 기반 KPI 설계 시 ROI 측정 가능성 확보 여부가 핵심.

---

## Ⅰ. 개요 및 필요성

정보기술이 기업 경쟁력의 핵심으로 부상하면서, IT에 대한 단순 비용 관리를 넘어 전략적 자산으로서의 통합적 관리가 요구됨. 과거 IT 부서는 전사적 자원관리(ERP), 공급망관리(SCM), 고객관계관리(CRM) 등 단위 시스템 도입에만 집중했으나, 클라우드·AI·IoT·블록체인 등 신기술의 폭발적 확산과 데이터 주권·개인정보보호법·ESG 규제 강화로 인해 IT 의사결정의 복잡성이 기하급수적으로 증가함.

특히 한국 정보시스템감리법 제14조(감리대상), 개인정보보호법 제29조(안전조치의 의무), 전자금융거래법 등 컴플라이언스 요구사항과 ISO/IEC 27001, ISO/IEC 20000, ISO/IEC 27701 등 국제표준 인증 의무화가 결합되면서, IT 부서의 자율적 기술 판단만으로는 통제 불가능한 영역이 발생함. 이로 인해 2010년대 이후 전 세계적으로 IT 거버넌스가 CFO 직속, CEO 직속, 또는 이사회 산하 Risk Committee로 이관되는 추세가 가속화됨.

```text
[ Legacy IT 운영 (1990~2010) ]              [ 현대 IT 거버넌스 (2015~현재) ]
+------------------------+                  +----------------------------------+
| CIO 중심 기술 조직     |                  | 이사회/CEO 직속 Risk Committee   |
|                        |                  |         |                        |
|  +------+  +------+    |                  |  +------+------+                 |
|  | ERP  |  | CRM  |    |      ->->->        |  |  IT전략위   |                 |
|  +------+  +------+    |                  |  |  (Steering) |                 |
|  +------+  +------+    |                  |  +------+------+                 |
|  | SCM  |  | 그룹웨어|   |                  |  +------+------+  +--------+   |
|  +------+  +------+    |                  |  |  거버넌스   |  |감사/   |   |
|   *사일로,중복투자*     |                  |  |  위원회     |  |준법감시|   |
|   *ROI측정불가*         |                  |  +------+------+  +--------+   |
|   *기술중심 의사결정*   |                  |  +------+------------------+   |
+------------------------+                  |  | PMO |BA |보안|인프라|데이터|   |
                                            |  +------------------------+-+   |
                                            |  +------------------------+-+   |
                                            |  | Cloud |AI/ML |IoT |Blockchain|
                                            |  +--------------------------+   |
                                            |  *표준기반 의사결정*              |
                                            |  *가치중심 포트폴리오 관리*        |
                                            +----------------------------------+
```

전통적 IT 운영은 "기술이 무엇을 할 수 있는가(Technology Push)" 관점이었던 반면, 현대 IT 거버넌스는 "비즈니스가 무엇을 필요로 하는가(Business Pull)" 관점으로 패러다임이 전환됨. McKinsey Global Survey(2023)에 따르면 디지털 성숙도 상위 25% 기업은 IT-비즈니스 정렬도가 78%에 달하지만, 하위 25% 기업은 21%에 그쳐 거버넌스 성숙도와 기업 성과 간 상관계수 0.83을 보임.

- **📢 섹션 요약 비유**: IT 거버넌스 없이는 마치 100명이 각자 다른 설계도로 집을 짓는 것과 같아, 건물이 세워진 후에는 전기·수도·통신 배선을 다시 뜯어고치는 비효율이 발생함.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019를 기준으로 한 현대 IT 거버넌스 아키텍처는 5개 도메인(거버넌스 영역)과 40개 관리목표(Management Objective)로 구성되며, 각각 EDM(평가·지휘·모니터링), APO(정렬·계획·조직), BAI(구축·획득·구현), DSS(전달·서비스·지원), MEA(모니터링·평가·분석)의 체계로 운영됨.

```text
                    [ 이사회 / Risk Committee ]
                              |
                              v
                 +------------------------+
                 |   EDM Domain (5개)     |  <--- 거버넌스 영역
                 |  E : 평가 (Evaluate)   |      "지휘와 통제"
                 |  D : 지휘 (Direct)     |
                 |  M : 모니터링 (Monitor)|
                 +------------+-----------+
                              |
                              v
                 +------------------------+
                 |  Strategy & Objectives |
                 +------------+-----------+
                              |
        +-------------+-------+------+-------------+
        v             v              v             v
  +----------+  +----------+  +----------+  +----------+
  |   APO    |  |   BAI    |  |   DSS    |  |   MEA    |
  | (14개)   |  | (11개)   |  |  (6개)   |  |  (4개)   |
  | 정렬/계획 |  | 구축/구현 |  | 전달/지원 |  | 모니터링 |
  +----+-----+  +----+-----+  +----+-----+  +----+-----+
       |             |             |             |
       +-------------+------+------+-------------+
                            |
                +-----------+-----------+
                v                       v
        +--------------+        +--------------+
        |  Process     |        |  Component   |
        |  Capability  |        |  (7종 자원)  |
        |  Level 0~5   |        |  People·Info |
        |  (PAM 기반)  |        |  Tech·Svc·..|
        +--------------+        +--------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/전략위 (Steering Committee)** | 거버넌스 의사결정 및 전략 방향 수립 | 분기별 성과 리뷰, BCG Matrix 기반 IT 포트폴리오 분류(Star/Cash Cow/Question Mark/Dog), RACI Matrix를 통한 책임 소재 명확화 |
| **CISO / CDO / CIO 트라이어드** | 각 기능별 의사결정 권한 분장 | CISO(보안·컴플라이언스), CDO(데이터 거버넌스·품질), CIO(인프라·애플리케이션). DGI(Data Governance Institute) DAMA-DMBOK 2.0 기반 데이터 소유권·관리권·사용권 분리 |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리 및 표준화 | PMBOK 7th Edition의 8대 도메인(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) 적용, PRINCE2의 7 Principles(계속적 사업 정당성, 경험으로부터 학습, 역할 책임 정의 등) 적용 |
| **감사/내부통제 (Internal Audit)** | 컴플라이언스 및 통제 환경 검증 | IIA(Institute of Internal Auditors) 표준, COBIT 2019 MEA04(Managed Assurance), Three Lines Model(1st: 운영, 2nd: 리스크/컴플라이언스, 3rd: 내부감사) 운영 |
| **EA (Enterprise Architecture)** | 전사 아키텍처 표준화 및 기술 로드맵 | TOGAF 10 ADM(Architecture Development Method) 8단계(H-P-V-B-D-M-R-R), ArchiMate 3.2 표기법, Zachman Framework 6x6 매트릭스 |
| **IT 재무관리 (ITFM)** | IT 비용 투명성 확보 및 가치 측정 | TBM(Tech Business Management) Framework의 4계층(서비스/컴포넌트/IT인프라/적용), FinOps 모델(클라우드 비용 최적화) |
| **GRC 플랫폼** | 통합 거버넌스·리스크·컴플라이언스 관리 | SAP GRC, ServiceNow GRC, RSA Archer, LogicGate, OneTrust(개인정보), RSA NetWitness(보안 모니터링) |

거버넌스 성숙도는 COBIT 2019의 **PAM(Process Assessment Model)** 기준 6단계(Level 0: Incomplete, Level 1: Initial, Level 2: Managed, Level 3: Defined, Level 4: Quantitative, Level 5: Optimizing)로 측정하며, ISO/IEC 33001 시리즈의 Process Capability Assessment와 매핑됨. 일반적으로 한국 대기업 평균은 Level 2.5~3.0 수준이며, 글로벌 Top 5% 기업은 Level 4.5 이상을 유지.

가치 측정은 **IT BSC(BSC: Balanced Scorecard)** 4관점으로 수행: ① 재무관점(IT 비용절감률, ROI), ② 고객관점(내부고객 만족도, SLA 준수율), ③ 내부프로세스관점(프로젝트 성공률, 변경관리 정확도), ④ 학습성장관점(IT 인력 역량지수, 혁신 프로젝트 비중). 각 관점별 KPI는 SMART 원칙(Specific·Measurable·Achievable·Relevant·Time-bound) 충족 필수.

- **📢 섹션 요약 비유**: COBIT 2019의 5개 도메인은 마치 자동차의 5대 시스템(엔진·변속기·바퀴·핸들·계기판)과 같아, EDM은 운전자(경영진)의 판단, APO는 도로(전략), BAI는 차체제작(구축), DSS는 주행정비(운영), MEA는 차량진단(감사)에 해당함.

---

## Ⅲ. 비교 및 연결

IT 거버넌스 관련 프레임워크는 각기 다른 초점을 가지며, 상호 보완적으로 활용됨. 실무에서는 단일 프레임워크만으로는 부족하여 다중 프레임워크 통합(Multi-framework Integration) 접근이 필수적.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **PMBOK 7th** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스 및 관리 통합 프레임워크 | IT 서비스 관리(SM) 최적화 | IT 의사결정 지침 표준 | 프로젝트 관리 지식체계 | 전사 아키텍처 개발 방법론 |
| **구조** | 5도메인 40관리목표 | 34 Practice, 4D모델 | 6원칙, 3계층(지휘-관리-운영) | 8성능도메인 12원리 | ADM 8단계 + ADM Cycle |
| **적용 범위** | 전략 -> 운영 전체 | 운영·서비스 영역 | 최고 의사결정층(Governance) | 단일 프로젝트 단위 | 아키텍처 설계·구현 |
| **성숙도 모델** | PAM 6단계(0~5) | Maturity Model 자체 보유 | X | OPM3 5단계 | TOGAF Maturity Model |
| **컴플라이언스** | 매핑(ISO 27001, NIST, ITIL 등) | ISO/IEC 20000 연계 | ISO/IEC 38500 자체 표준 | PMI 표준 | Open Group 표준 |
| **주 사용자** | CIO, CISO, CAE(감사) | ITSM 담당자, 서비스 데스크 | CEO, 이사회 | PMO, 프로젝트 매니저 | EA 아키텍트, 수석개발자 |
| **산출물** | RACI Chart, Maturity Profile | Service Value Chain, CSI | Governance Charter, Decision Log | Project Charter, Risk Register | Architecture Roadmap, Gap Analysis |
| **측정 관점** | 거버넌스·관리 통합 KPI | 서비스 가치(Value) 중심 | 원칙 준수 여부 | 프로젝트 성공률(iron triangle) | 아키텍처 정합성·재사용률 |
| **비용 모델** | 컨설팅+인증 비용 | 컨설팅+Axelos 인증 | 자가적용(무료) | PMI 멤버십($139~$425) | Open Group 멤버십 |
| **한국 도입률** | 대기업 60% | 중견 45%, 공공 30% | 표준참조 80% | PMO 보유기업 35% | 대기업 EA조직 25% |

**연계 통합 패턴**: 실무에서는 **"COBIT을 거버넌스 뼈대, ITIL을 운영 근육, PMBOK을 프로젝트 혈관, TOGAF를 아키텍처 골격"**으로 비유하는 통합 거버
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 559 / 800

<- **이전**: [558. IT 경영 관리 핵심 토픽 558번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/558_it_management_core_topic_558_exam_summary/)
**다음**: [560. IT 경영 관리 핵심 토픽 560번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/560_it_management_core_topic_560_exam_summary/) ->

---
