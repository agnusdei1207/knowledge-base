+++
title = "503. Zachman 프레임워크 분류 체계 (Zachman Framework Classification)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Zachman 프레임워크는 엔터프라이즈 아키텍처 산출물을 6개의 의사소통 원시적 질문(What·How·Where·Who·When·Why)과 6개의 추상화 관점(Scope·Business·System·Technology·Detailed·Functioning)으로 구성된 **6×6 = 36셀 분류 행렬**로 체계화한 메타-언어 체계로, 각 셀은 고유한 stakeholder(관점자)·artefact(산출물)·tool(도구)을 가진다.
> 2. **가치**: 동일 비즈니스 요소(예: "고객")가 셀마다 다른 모델링 표기(개념->논리->물리->구현)로 변환되어 표현되는 **재구성(Reification) 사다리**를 통해, 아키텍처 산출물의 중복·누락·모호성을 정량적으로 식별할 수 있으며, 전사 EA 거버넌스 성숙도 측정 기준으로 활용 시 셀 완성률(%)을 KPI로 관리 가능하다.
> 3. **판단 포인트**: Zachman은 **분류 체계(Classification Schema)**이지 방법론(Methodology)이 아니므로, ADM 사이클을 가진 TOGAF·연속체 클라이언트-서버 모델을 가진 FEAF와 결합하여 사용해야 실무 적용성이 확보되며, "Why" 셀(동기/목표)과 "What" 셀(데이터)·"How" 셀(기능)의 정합성 검증이 EA 품질의 핵심 통제점이다.

---

## Ⅰ. 개요 및 필요성

1987년 IBM의 John A. Zachman이 mainframe 기반 정보시스템 통합 프로젝트에서 파편화되어 중복 정의되는 아키텍처 산출물을 통제하기 위해 제안한 "**A Framework for Information Systems Architecture**"(IBM Systems Journal, 1987)에서 기원한다. Zachman은 건축에서 Christopher Alexander의 패턴 언어, 제조업에서 Bill of Materials(BOM) 계층 구조, 항공우주 산업의 시스템 엔지니어링 표준(MIL-STD-499B, ISO 42010)에서 영감을 받아, 엔터프라이즈를 **"한 명의 무한한 지능을 가진 존재가 만들었다면 어떻게 설계했을 것인가"**라는 가상적 관점에서 바라보는 **총체적 모델(Total Entity Model)** 사상을 정립했다.

핵심 동기는 ① 1980년대 MIS 부서의 시스템 백로그 누적과 shadow IT 증가, ② PL/1, COBOL, IMS, DB2 등 기술 종속적 산출물이 비즈니스 변경 시 추적 불가, ③ 아키텍처 명세의 모호성으로 인한 redundant design 등 3가지 구조적 문제였다. Zachman은 이를 **"각 stakeholder는 자기가 이해하는 표현 방식이 진실이라고 믿는다"**는 전제에서 출발해, 모든 stakeholder의 관점을 동등하게 수용하는 직교(orthogonal) 분류 체계가 필요하다고 주장한다.

```text
+----------------------------------------------------------------------+
|           Zachman Framework: 6 Interrogatives × 6 Perspectives         |
+----------------------------------------------------------------------+
|  Stakeholder:     Planner     Owner      Designer    Builder    Sub-Con.  Working    |
|  관심사:           What        What       What        What       What       What       |
|  재구성물:         Scope       Business   System      Technology Detailed   Functioning|
|  6W-관점:          (범위)      (비즈모델)  (시스템모델) (기술모델) (상세표현)  (운영체계)  |
+----------------------------------------------------------------------+
|  WHAT (Data)      |  비지니스 |  엔터프라이즈|  논리 데이|  물리 데이|  데이터베|  데이터    |
|  무엇을           |  객체 목록 |  데이터 모델|  터 모델 |  터 모델 |  이스 정 |  베이스 실|
|                   |  (Thing)   |  (Entity)   |  (ER)    |  (DDL)   |  의서    |  제 데이터|
+----------------------------------------------------------------------+
|  HOW (Function)   |  프로세스 |  비즈니스    |  애플리  |  시스템   |  프로그 |  소프트웨 |
|  어떻게           |  목록      |  프로세스 모델|  케이션  |  아키텍  |  램 코드 |  어 실행  |
|                   |            |  (BPMN)     |  아키텍처|  처(SA)   |  (소스)  |  (런타임)  |
+----------------------------------------------------------------------+
|  WHERE (Network)  |  위치 목록 |  사업장     |  분산 시 |  기술 아 |  네트워크|  통신    |
|  어디서           |            |  토폴로지   |  스템 아 |  키텍처  |  아키텍 |  인프라   |
|                   |            |            |  키텍처  |          |  처     |          |
+----------------------------------------------------------------------+
|  WHO (People)     |  조직 목록 |  조직/역할  |  HUMAN   |  HUMAN   |  보안   |  사용자  |
|  누가             |            |  모델      |  INTERFACE|  INTER-  |  정책   |  헬프데  |
|                   |            |  (RACI)    |  (UI/UX) |  FACE구현|  (RBAC) |  스크    |
+----------------------------------------------------------------------+
|  WHEN (Time)      |  이벤트   |  비즈니스   |  프로세스 |  컨트롤  |  타이밍 |  스케줄 |
|  언제             |  목록     |  마스터일정 |  모델    |  (배치/실|  명세   |  러 실행 |
|                   |            |  (Gantt)   |  (시퀀스)|  시간)  |        |        |
+----------------------------------------------------------------------+
|  WHY (Motivation) |  목표 목록 |  전략/원칙 |  설계 원칙|  기술   |  규칙   |  비즈니스|
|  왜               |            |  (Balanced |  (Design |  결정사항|  (Style |  가치   |
|                   |            |  Scorecard)|  Pattern)|  (RDA)   |  Guide) |  실현   |
+----------------------------------------------------------------------+
        ^ 6W Primitive Interrogatives (열축)  ×  6 Reification Transformations (행축)
```

전통적 시스템 개발(SDLC)에서는 비즈니스 분석가가 ERD를, 개발자가 별도 ERD를, DBA가 또 다른 ERD를 작성하는 **Triple Maintenance Problem**이 발생했다. Zachman은 이를 "관점이 다른 stakeholder의 의도적 차별화"로 재해석하여, 같은 "고객"이라는 데이터도 (a) 비즈니스 관점에서는 비지니스 객체 목록의 한 항목, (b) 시스템 모델 관점에서는 정규화된 엔터티, (c) 기술 모델 관점에서는 인덱스·파티션 전략이 적용된 테이블, (d) 상세 표현 관점에서는 CREATE TABLE DDL로 표현되어야 한다고 규정한다. 즉 **"동일 truth의 다중 재구성(Multiple Reification)"**이 아키텍처의 본질이라는 관점이다.

- **📢 섹션 요약 비유**: Zachman 행렬은 마치 **항공기 정비 매뉴얼**과 같다. 한 대의 보잉 747에 대해 비행사(Scope, "왜 비행하나"), 항공사(Owner, "수익 모델"), 기장(Designer, "운항 절차"), 정비사(Builder, "배선도"), 부품 제조사(Sub-Con, "볼트 토크"), 그리고 실제 비행 중인 항공기(Functioning) 모두가 각자의 언어로 동일한 항공기를 다시 기술하되, 어느 한 문서도 중복되지 않고 빠짐없이 존재해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Zachman 프레임워크의 핵심 메커니즘은 **두 직교 축(2 Orthogonal Axes)**의 교차로 형성되는 36개 셀 각각이 (i) 단일 stakeholder, (ii) 단일 산출물 유형, (iii) 단일 도구 세트, (iv) 단일 명세 원칙에 대응된다는 **Orthogonality Principle(직교성 원리)**이다. 이 원리는 **Completeness(완전성)**, **Non-redundancy(비중복성)**, **Disparate Models(이질성)** 세 가지 파생 규칙을 통해 수학적으로 보장된다. 셀 누락 시 아키텍처 표현의 사각지대가 발생하고, 두 셀이 동일 산출물을 담게 되면 redundancy가 발생하여 Triple Maintenance 문제가 재발한다.

```text
        Reification Ladder (재구성 사다리)  -- 추상 -> 구체 --->
        +----------+----------+----------+----------+----------+----------+
WHAT    | Thing    | Entity   | Attribute| Table    | Column   | Value    |
(Data)  | (개념)   | (논리)   | (논리)   | (물리)   | (물리)   | (인스턴스)|
        +----------+----------+----------+----------+----------+----------+
        | Process  | Process  | Process  | Function | Program  | CPU      |
HOW     | List     | Model    | Spec     | Design   | Code     | Cycle    |
(Function)|         |          |          |          |          |          |
        +----------+----------+----------+----------+----------+----------+
WHERE   | Node     | Network  | Link     | Node+    | Address  | Address  |
(Network)| List     | Model    | Spec     | Link     | Spec     | Assigned |
        +----------+----------+----------+----------+----------+----------+
WHO     | People   | Role     | Person-  | User     | Identity | Identity |
(People)| List     | Model    | a-Role   | Profile  | (UID/GID)| Active   |
        +----------+----------+----------+----------+----------+----------+
WHEN    | Event    | Master   | Cycle    | Process  | Schedule | Job      |
(Time)  | List     | Schedule | Time     | Schedule | Calendar | Running  |
        +----------+----------+----------+----------+----------+----------+
WHY     | End/Means| Goal/    | Rule/    | Design   | Sub-     | Product  |
(Motiv.)| List     | Strategy | Principle| Strategy | Strategy | Result   |
        +----------+----------+----------+----------+----------+----------+
        Scope -> Business -> System -> Technology -> Detailed -> Functioning
        (왜)    (무엇을)   (어떻게)  (어디에)    (누가)    (언제)
        Primitive              Owned                    Transformed
        ------ Class -------------------------------- Class ----------
```

각 행(Row)은 Zachman이 **"Reification(구체화)"**이라 명명한 변환 규칙을 나타낸다. 건축 비유로 Scope 행은 도시계획(매우 추상), Business Model 행은 건축주의 요구사항(누가 살 것인가), System Model 행은 건축가의 설계도(공간 배치), Technology Model 행은 구조기술자의 시공 매뉴얼(콘크리트 강도), Detailed Representation 행은 시공자의 도면(철근 배치), Functioning Enterprise 행은 실제 거주 중인 건물(가동 중)이다. 열(Column)인 5W1H(What, How, Where, Who, When, Why)는 **원시적 의사소통 단위(Primitive Communication Interrogatives)**로, 이 6개가 인간이 어떤 복잡한 사물을 설명할 때 본능적으로 사용하는 가장 원자적인 질문의 집합이라는 언어철학적 주장에 기반한다(Aristotelian Categories, Kipling's "Six Honest Serving Men" — *I keep six honest serving-men; they taught me all I knew; their names are What and Why and When and How and Where and Who*).

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **열축: 5W1H Primitive Interrogatives** | 엔터프라이즈를 기술하기 위한 **원자적 질문 차원** | WHAT(데이터/Thing), HOW(기능/Process), WHERE(네트워크/Node), WHO(주체/People), WHEN(시간/Event), WHY(동기/End-Means). ISO 42010의 Architecture Concern(stakeholder × concern × viewpoint)에 대응. |
| **행축: 6 Reification Transformations** | 동일 요소가 **점진적으로 구체화**되는 변환 단계 | Scope(Contextual) -> Business Model(Conceptual) -> System Model(Logical) -> Technology Model(Physical) -> Detailed Representation(As-Built) -> Functioning Enterprise(Operational). 객체지향의 **추상화->구체화**, MDA(Model-Driven Architecture)의 **CIM->PIM->PSM**와 동형. |
| **셀(Cell): 36 Reification Intersection** | (i) 단일 stakeholder, (ii) 단일 artefact, (iii) 단일 rule, (iv) 단일 tool, (v) 단일 semantic boundary | 예: (System, WHAT) 셀 = 정규화된 ERD, 도구: ERwin, PowerDesigner, dbdiagram.io, MySQL Workbench. **No overlap**: 동일 요소는 한 셀에만 등장. Triple Maintenance 부재. |
| **Primitive Set vs Owned Set 분류선** | 변환의 의미론적 경계 | 행 1~2는 **Class 정의**(WHAT·HOW·WHO·WHERE·WHEN의 명사적 정의: 무엇이 존재하는가, WHAT 속성·HOW 관계), 행 3~4는 **Instance 기술**(실제 출현값), 행 5~6은 **구현·가동**(Sub-Contractor는 자재·코드, Functioning은 실제 운영). 이는 OOP의 **Class vs Object**, RDF의 **Schema vs Instance**와 동형. |
| **Bind Rule(제약)** | 동일 행(Row) 내 셀들 간 **내적 일관성** 규칙 | 동일 행의 모든 셀은 동일 business primitive의 동일 시점 스냅샷을 나타내야 함. 예: WHAT-행에서 Scope 단계의 "Customer" 명사 정의는 Functioning 단계의 실재 고객 레코드와 매핑되어야 함(traceability). |
| **Tool Discipline** | 각 셀에 특화된 **표기법·언어** | UML(시스템 모델), BPMN(비즈니스 프로세스), ArchiMate(엔터프라이즈), SysML(엔지니어링), SQL DDL(상세), 데이터 거버넌스 메타모델로 구분. |
| **Meta-model(본질) vs Methodology(절차)** | Zachman은 **분류 체계**임을 명시 | 자체 ADM·Phases·Steps를 제공하지 않으므로, TOGAF ADM, DoDAF Viewpoints, FEAF PRM, Gartner EA Tool Selection과 결합하여 절차적 골격을 부여함. |

Zachman의 수학적 엄밀성을 보여주는 추가 규칙으로 **"Mathematical Completeness Theorem"**이 있다. 6개의 원시적 질문은 서로 독립(mutually exclusive)이며, 인간이 어떤 실세계 사물을 의사소통하기 위한 **완전 기저(complete basis)**를 형성한다는 주장이다. 이를 검증하기 위해 4W(What·How·Where
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 503 / 600

<- **이전**: [502. TOGAF ADM 아키텍처 개발 방법](/knowledge-base/studynote/11_design_supervision/06_exam_summary/503_togaf_adm_architecture_development_metho/)
**다음**: [504. FEAF 연방 EA 프레임워크](/knowledge-base/studynote/11_design_supervision/06_exam_summary/504_feaf_federal_ea_framework/) ->

---
