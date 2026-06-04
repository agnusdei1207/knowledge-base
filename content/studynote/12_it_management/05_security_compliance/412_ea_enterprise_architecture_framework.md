+++
title = "412. EA 엔터프라이즈 아키텍처 프레임워크 (EA Enterprise Architecture Framework)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EA(Enterprise Architecture)는 Zachman Framework의 6×6 매트릭스(What/How/Where/Who/When/Why × Scope/Enterprise/Architect/Designer/Implementer/Worker) 및 TOGAF ADM(Architecture Development Method)의 8단계迭代 사이클을 통해 비즈니스(BA)·데이터(DI)·애플리케이션(AP)·기술(TA) 4개 도메인의 정합성을 확보하는 **전사적 설계·거버넌스 체계**이다.
> 2. **가치**: EA를 체계적으로 운용할 경우 중복 투자 30~40% 절감, 시스템 통합 기간 50% 단축, 신규 사업 요구사항의 70% 이상을 레퍼런스 아키텍처로 재사용 가능하며, ISO/IEC/IEEE 42010 및 TOGAF 9.2/10 표준을 통한 거버넌스 무결성 확보가 가능하다.
> 3. **판단 포인트**: **표준 프레임워크 채택(TOGAF/Zachman/DoDAF)** vs **자체 경량 프레임워크**의 트레이드오프, **As-Is -> To-Be 전이 전략(점진적/빅뱅)**, **거버넌스 조직(EA Center of Excellence) 운용 모델**, 그리고 **Agile/DevOps 환경에서 Lightweight EA**로 전환 시 정합성 유지가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대의 기업은 평균 200~800여 개의 애플리케이션을 운영하며, 매년 15~25%씩 증가하는 신규 시스템 도입으로 인해 **'시스템 스파게티'** 현상이 심화되고 있다. 한국정보화진흥원(NIA)의 2023년 보고에 따르면 국내大中型 기업 중 약 67%가 동일 업무영역에 중복된 시스템을 보유하고 있으며, 41%가 신규 사업 착수 시 참조할 수 있는 표준 아키텍처 부재로 인해 설계부터 재시작하는 비효율을 겪고 있다. 이러한 환경에서 EA(Enterprise Architecture, 전사아키텍처)는 **"왜(Why) 만들어야 하는가"에 대한 정당화**부터 시작하여 **"어떻게(How) 정합성을 유지하며 변화에 대응할 것인가"**까지의 전 과정을 다루는 체계적 접근법이다.

EA는 단순히 IT 시스템의 도식이 아니라, **업무·데이터·애플리케이션·기술** 4개 도메인(필요 시 보안·거버넌스 도메인 추가)을 **플랜(Plan) -> 비전(Vision) -> 현황(As-Is) -> 목표(To-Be) -> 이행(Implementation) -> 거버넌스(Governance)** 의 6단계 파이프라인으로 정렬하는 경영·기술 융합 discipline이다. 1987년 John Zachman이 IBM Systems Journal에 발표한 Zachman Framework 이후, 1995년 TAFIM을 계승한 **DoDAF(DoD Architecture Framework) v1.0**, 1995년 **TOGAF(The Open Group Architecture Framework)** v1.0, 1999년 **FEAF(Federal Enterprise Architecture Framework)**, 2011년 **Gartner EA Framework**가 등장했으며, 현재는 **TOGAF 9.2(2018) -> TOGAF 10(2022)**으로 진화하여 마이크로서비스·클라우드·AI 시대에 적합한 가이드(ADM Cycle, Architecture Repository, Content Metamodel)를 제공하고 있다.

```text
+----------------------------------------------------------------------+
|          EA 도입의 필요성: "사일로(Silo) 해체와 정합성 확보"           |
+----------------------------------------------------------------------+
|                                                                      |
|   +-------------+    +-------------+    +-------------+             |
|   |  영업시스템   |    |  재무시스템   |    |  HR시스템    | <- 사일로 |
|   |  (Legacy)   |    |  (ERP)      |    |  (Cloud)    |             |
|   |  COBOL/DB2  |    |  SAP R/3    |    |  Workday    |             |
|   +------+------+    +------+------+    +------+------+             |
|          | 중복 데이터        | 동일 고객ID 4종     | 인터페이스 부재   |
|          | (고객, 주문)        | (CRM, ERP, MES,    | (배치 위주)       |
|          |                   |  WMS)              |                   |
|          v                   v                   v                   |
|   +---------------------------------------------------------+       |
|   |            EA 레퍼런스 아키텍처 + 거버넌스                |       |
|   |   • 4-Domain 정합성 매트릭스 (BA ↔ DI ↔ AP ↔ TA)         |       |
|   |   • As-Is/To-Be 갭 분석 + 이행 로드맵                    |       |
|   |   • Architecture Repository (Sparx EA, ARIS, Avolution)  |       |
|   +---------------------------------------------------------+       |
+----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: EA는 마치 **도시계획(都市計劃)** 과 같다. 개별 건축물(시스템)만 짓다 보면 상하수도·도로·전기 공급이 서로 맞지 않아 도시 전체가 마비되는데, EA는 **토지이용·교통·공공시설의 마스터플랜**을 미리 세워 도시의 지속가능성을 보장하는 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. TOGAF ADM(Architecture Development Method) 8단계 핵심 사이클

TOGAF의 핵심인 ADM은 **Preliminary Phase -> A(Architecture Vision) -> B(Business Architecture) -> C(Information Systems: Data + Application) -> D(Technology Architecture) -> E(Opportunities & Solutions) -> F(Migration Planning) -> G(Implementation Governance) -> H(Architecture Change Management)** 의 8단계 + 요구사항관리(Requirements Management) 연속 프로세스로 구성된다. 각 단계는 **위임(Iteration) 가능**하며, 비전 단계에서 정의한 트랜스포메이션 이니셔티브를 Phase E~F에서 구체적인 마이그레이션 워크팩(WP1~WP5)으로 분해한다.

```text
+----------------------------------------------------------------------+
|              TOGAF ADM Cycle + Architecture Repository               |
+----------------------------------------------------------------------+
|                                                                      |
|         +-- Preliminary --+                                         |
|         |  (프레임워크 선정,   |                                       |
|         |   거버넌스 정의)    |                                       |
|         +--------+---------+                                         |
|                  v                                                    |
|   +--- A. Architecture Vision ---------------------+                |
|   |  • 이해관계자맵, 비즈니스 drivers, 영향분석      |                |
|   |  • Statement of Architecture Work (SOW)        |                |
|   +---------------------+--------------------------+                |
|                         v                                            |
|   +--- B. Business Architecture ------+                             |
|   |  • 업무분장모델, 비즈니스 프로세스    |--+                         |
|   |  • 조직·역할·능력맵 (Capability Map)  |  |                         |
|   +---------------------+---------------+  |                         |
|                         v                  |                         |
|   +--- C. IS Architecture ---------------+ |                         |
|   |  C1. Data (논리/물리 데이터모델)      |<-+ 4-Domain                |
|   |  C2. Application (앱 컴포넌트,        |    정합성                  |
|   |       인터페이스 카탈로그)             |    매트릭스                |
|   +---------------------+---------------+                           |
|                         v                                            |
|   +--- D. Technology Architecture -------+                           |
|   |  • 플랫폼, 미들웨어, 네트워크, 보안    |                           |
|   |  • TRM (Technical Reference Model)   |                           |
|   +---------------------+---------------+                           |
|                         v                                            |
|   +--- E. Opportunities & Solutions -----+                           |
|   |  • 갭 분석 (As-Is vs To-Be)          |                           |
|   |  • WP1~5 Work Package 분해            |                           |
|   +---------------------+---------------+                           |
|                         v                                            |
|   +--- F. Migration Planning -------------+  Architecture Repository |
|   |  • 이행 로드맵, TCO/ROI 분석         |<-+  • Architecture         |
|   |  • 마이그레이션 T-shirt 사이징         |  |    Metamodel            |
|   +---------------------+---------------+  |  • ADM Artifacts       |
|                         v                  |  • Standards Library   |
|   +--- G. Implementation Governance -----+ |  • Reference Models    |
|   |  • 계약 검토, 적합성 검증             | |  • Governance Log      |
|   +---------------------+---------------+ |                          |
|                         v                  |                          |
|   +--- H. Architecture Change Management + |                          |
|   |  • 변경 영향 분석, 트리거 모니터링     |-+                          |
|   |  • ADM Cycle 재진입                    |                            |
|   +--------------------------------------+                            |
|                                                                      |
|   [Requirements Management] <--- 모든 Phase에서 연속 수행 --->          |
+----------------------------------------------------------------------+
```

### 2. 4대 도메인 아키텍처 정합성 매트릭스

EA의 4개 도메인은 **단방향 종속(Business -> Data -> Application -> Technology)** 관계를 가지며, 상위 도메인의 변경이 하위 도메인에 전파되는 cascade 구조를 갖는다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **BA (Business Architecture)** | 업무·조직·능력·프로세스 모델링 | BPMN 2.0, CMMN, Value Chain 분석, Capability Map (Level 0~3), Org Chart + RACI Matrix, KPI Tree |
| **DI (Data/Information Architecture)** | 데이터 개념·논리·물리 모델, 거버넌스 | ERD (Chen/IE/Crow's Foot), 데이터 딕셔너리, 메타데이터 관리, DAMA-DMBOK 2.0, 데이터 카탈로그, MDM(Master Data Management) |
| **AP (Application Architecture)** | 애플리케이션 컴포넌트·서비스·인터페이스 | SOA/마이크로서비스 카탈로그, API 명세(OpenAPI 3.0), C4 Model, 시퀀스·컴포넌트 다이어그램, 앱 포트폴리오 분석(APM) |
| **TA (Technology Architecture)** | 인프라·플랫폼·미들웨어·보안 | TOGAF TRM(Technical Reference Model), 3-Tier/N-Tier, 클라우드 아키텍처(IaaS/PaaS/SaaS), 컨테이너/쿠버네티스, 네트워크 토폴로지, 보안참조모델(SABSA) |
| **Architecture Repository** | 산출물·표준·레퍼런스 모델 통합 저장 | Sparx EA, Avolution Abacus, ARIS, LeanIX, Bizzdesign HoriZZon, MooD, Confluence + EA Plug-in |
| **EA Governance (CoE)** | 의사결정·표준화·컴플라이언스 | Architecture Review Board, ARB(Architecture Review Board), ADR(Architecture Decision Record), RFC 프로세스, EA Maturity Model (Gartner/CMMI) |

### 3. 핵심 산출물(Deliverables)과 아키텍처뷰(Viewpoints)

TOGAF는 **29종 이상의 산출물**(Architecture Vision, Business Capability Map, Target Application Portfolio, Technology Stack Diagram 등)을 정의하며, 각각 ISO/IEC/IEEE 42010의 **뷰(View) + 뷰포인트(Viewpoint)** 구조로 표현된다. 예를 들어 Phase B의 **조직도(Org Chart)** 는 "Stakeholder: CEO"의 "Viewpoint: 전략적 정렬"에서, Phase C의 **시퀀스 다이어그램**은 "Stakeholder: 개발자"의 "Viewpoint: 시스템 통합"에서 사용된다.

### 4. 거버넌스 메커니즘과 ADM 반복

- **Architecture Review Board (ARB)**: 전사 아키텍처 결정을 승인하는 거버넌스 기구 (월 1~2회 회의, 정족수 2/3)
- **Architecture Compliance Assessment**: 프로젝트가 To-Be 아키텍처를 준수하는지 검증 (Time-boxed: 4~6주)
- **ADM Iteration**: 한 사이클 평균 3~6개월, 대규모 트랜스포메이션은 12~18개월 (예: 코어뱅킹 시스템 교체)

- **📢 섹션 요약 비유**: 4-Domain EA는 **인체의 4대 계통(소화·혈액·근육·신경)** 과 같다. 업무(소화)가 잘 돌아야 데이터(영양)가 흡수되고, 애플리케이션(근육)이 움직이며 기술 인프라(신경)가 신호를 전달한다. 어느 한 계통이 무너지면 몸 전체가 병들듯, 어느 한 도메인이라도 정합성이 깨지면 전사 시스템이 마비된다.

---

## Ⅲ. 비교 및 연결

### 1. EA 프레임워크 간 상세 비교

| 구분 | **TOGAF 9.2/10** | **Zachman Framework** | **DoDAF v2.0** | **FEAF** | **Gartner EA** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **개발 주체** | The Open Group (1995~) | John Zachman (IBM, 1987) | 미국 DoD (2003~) | 미국 OMB/CIO Council (1999) | Gartner (2011~) |
| **핵심 구조** | ADM 8단계 + Repository | 6×6 매트릭스 (What/How/Where/Who/When/Why × 6 셀) | AV-1~6, OV-1~6, SV-1~10, TV-1~2, DIV, StdV-1~2 | 5개 참조모델(PRM, BRM, DRM, ARM, TRM) | EA 트랙(Strategy->Portfolio->Project) |
| **산출물 수** | 30+ ADM 산출물 | 36개 셀 (각 셀별 모델) | 약 50개 뷰(View) | 5대 모델 + 40+ 산출물 | EA 그래프 + KPI |
| **표준화** | ISO/IEC/IEEE 42010, 27001 연계 | ISO/IEC/IEEE 42010 원형 | DoD 5000.59, IEEE 1220 | FEA Reference Models | 독자 방법론 |
| **강점** | 거버넌스·반복(Iteration) 강조, 표준·인증(TOGAF Certified) | 재고조사(Inventory)·완전성, 매우 포괄적 | 군사 도메인·운용뷰 정교화, 미국방 표준 | 정부 부처간 통합, PRM 강력 | 비즈니스 가치·포트폴리오 연계 |
| **약점** | 도메인 모델링 깊이 부족 (단독 사용 시) | 실용적 절차 부재, 방법론 없음 | 학습 곡선 높음, 민간 적용 어려움 | 미국 연방 전용, 비공개 | 독점적, 상용 컨설팅 의존 |
| **적합 도메인** | 일반 기업(특히 금융·통신·제조) | 분류·정렬이 필요한 대형 조직 | 국방·정부·공공기관 | 연방정부·대형 공공 | 전략-투자 연계가 중요한 기업 |
| **한국 도입 사례** | 삼성SDS, KT, 신한은행, 국토부, 서울시 | 행정안전부(정부 EA 표준) | 방위사업청, ADD(국방과학연구소) | 한국조세재정연구원, 행안부 | SK, CJ, 포스코(거버넌스 차원) |

### 2. 다른 discipline과의 통합

EA는 단독으로 작동하지 않으며, 다음 discipline과 **나란히(parallel)** 운용되어야 실효성을 갖는다.

- **IT 거버넌스(COBIT 2019)**: EA가 "설계도"라면 COBIT은 "관리체계". COBIT의 EDM(평가·지시·모니터링) + APO(정렬·계획·조직) + BAI(구축·도입·운영) + DSS(배송·서비스·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 412 / 800

<- **이전**: [411. IT 전략 수립 ISP BPR ISP 방법론](/knowledge-base/studynote/12_it_management/05_security_compliance/411_it_strategy_planning_isp_bpr_methodology/)
**다음**: [413. TOGAF ADM 아키텍처 개발 방법론](/knowledge-base/studynote/12_it_management/05_security_compliance/413_togaf_adm_architecture_development_method/) ->

---
