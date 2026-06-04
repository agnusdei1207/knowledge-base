---
title: "418. 서비스 디자인 서비스 블루프린트 (Service Design Service Blueprint)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서비스 블루프린트(Service Blueprint)는 1984년 G. Lynn Shostack이 제안한 서비스 설계 기법으로, **Line of Interaction(상호작용선), Line of Visibility(가시성선), Line of Internal Interaction(내부상호작용선)** 3개의 라인을 기준으로 고객 접점의 가시 영역(Frontstage)과 비가시 영역(Backstage), 그리고 지원 프로세스(Support Process)를 5개 스윔레인(Swimlane)으로 시각화하는 End-to-End 서비스 프로세스 모델링 방법론이다.
> 2. **가치**: BPMN 2.0 프로세스 모델, ISO/IEC 20000 SLA 정의, ITIL 4 서비스 가치 사슬(Value Chain)과 연계 시 서비스 실패 지점(Moment of Truth)의 **평균 23~40% 감소**, 채널 전환 시 일관성(Consistency) 확보, Frontstage·Backstage 간 핸드오프(Handoff) 병목을 정량적으로 식별하여 평균 처리시간(ART, Average Resolution Time)을 15~30% 단축시킬 수 있다.
> 3. **판단 포인트**: 정성적 페르소나(Qualitative Persona)와 정량적 로그/이벤트 데이터(Quantitative Event Stream)를 결합한 **Hybrid Blueprint**를 채택할지, 단일 채널 Blueprint로 단순화할지, 그리고 MSA(Microservices Architecture) 환경에서는 **Domain-Driven Design(DDD)의 Bounded Context** 단위로 Blueprint를 분할하여 팀별 책임 영역을 명확히 할 것인지가 핵심 아키텍처 결정 포인트다.

---

## Ⅰ. 개요 및 필요성

기존 제품 중심(Product-Centric) 설계 방법론으로는 **서비스의 4대 특성(무형성 Intangibility, 불가분성 Inseparability, 변동성 Variability, 소멸성 Perishability)** 으로 인한 품질 편차를 통제하기 어렵다. 특히 디지털 트랜스포메이션(DX, Digital Transformation) 시대에 **Omnichannel(온·오프라인 통합 채널), Microservices, Event-Driven Architecture** 가 보편화되면서, 단일 접점이 다수 시스템과 비동기로 연동되는 **N:M 서비스 토폴로지** 에서의 거버넌스 확보가 핵심 과제로 부상했다.

서비스 블루프린트는 ①To-Be(미래상) 모델을 통한 **Target Operating Model(TOM)** 수립, ② 채널별 일관된 Customer Experience(CX) 설계, ③ **Service Level Agreement(SLA)** 의 단위 프로세스 매핑, ④ Backstage 장애가 Frontstage CX로 전파되는 경로(Blast Radius) 분석에 사용된다. 기술사 출제 관점에서는 *"은행의 비대면 계좌개설 서비스를 신규 디지털 채널로 출시할 때, 어떤 Service Blueprint 구조로 To-Be를 설계하고 기존 레거시 코어뱅킹 시스템과 어떻게 통합할 것인가"* 와 같은 **현실 마이그레이션 시나리오** 가 빈번하게 등장한다.

```text
+--------------------------------------------------------------+
|  Service Blueprint 5-Swimlane Conceptual Structure           |
|                                                              |
|   +----------------------------------------------------+     |
|   | ① Customer Actions  (고객 행동)                    | ★   |
|   +----------------------------------------------------+ - - +
|   |              <--- Line of Interaction --->           |     |
|   +----------------------------------------------------+     |
|   | ② Frontstage Actions  (접점 직원/시스템 행동)      |     |
|   +----------------------------------------------------+ - - +
|   |              <--- Line of Visibility --->            |     |
|   +----------------------------------------------------+     |
|   | ③ Backstage Actions  (내부 직원 행동)              |     |
|   +----------------------------------------------------+ - - +
|   |              <--- Line of Internal Interaction --->  |     |
|   +----------------------------------------------------+     |
|   | ④ Support Processes  (지원 시스템 프로세스)        |     |
|   +----------------------------------------------------+     |
|   | ⑤ Physical Evidence  (물리적/디지털 증거)          |     |
|   +----------------------------------------------------+     |
|                                                              |
|  ★ = 직접 고객이 체감하는 Value Stream(가시 영역)            |
|  - - = Swimlane을 구분하는 핵심 경계선(Line)                 |
+--------------------------------------------------------------+
```

기존 UML Use Case Diagram이나 Data Flow Diagram(DFD)은 **기능 단위**의 정적 모델에 머물렀지만, 서비스 블루프린트는 **시간의 흐름(Time-Bound)** 을 가로축으로, **주체(Actor)·시스템 계층** 을 세로축으로 두어 동적 서비스 전달 과정을 시퀀스 다이어그램(Sequence Diagram) 수준으로 묘사한다. 이는 ISO 9241-210(인간 중심 설계) 및 Double Diamond 모델(Discover-Define-Develop-Deliver)의 **Define 단계** 산출물로서 정량적·정성적 데이터의 허브 역할을 수행한다.

- **📢 섹션 요약 비유**: 서비스 블루프린트는 마치 **연극의 무대 설계도(Stage Design Drawing)** 와 같다. 객석에서 보이는 무대 위 배우(Frontstage), 무대 뒤에서 분장·조명·음향을 관리하는 스태프(Backstage), 무대 아래 기계실의 시설팀(Support Process), 그리고 무대 위 소품과 조명(Physical Evidence) 모두가 한 장의 도면 위에 시간 순서대로 그려져, 관객(고객)이 어떤 순간에 무엇을 보고 경험하는지를 명확히 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서비스 블루프린트의 5개 스윔레인은 **상호작용 주체(Who)**, **가시성(Visibility)**, **시간축(When)**, **지원 시스템(What)** 의 4차원으로 구성된다. 각 레인의 경계를 정의하는 **3개의 Line** 은 서비스 거버넌스의 핵심 분리 원칙(Separation of Concerns)을 반영한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① Customer Actions** | 고객이 서비스 이용을 위해 수행하는 모든 행동(탐색, 입력, 결제, 문의 등) | Google Analytics 4(GA4) 이벤트 로그, Adobe Customer Journey Analytics, CDP(Customer Data Platform)의 Identity Resolution으로 **Session Stitching** 수행. 페르소나·이코노그래피(Iconomy) 분석 기반 행동 패턴 분류 |
| **② Frontstage Actions** | 고객과 직접 상호작용하는 접점 채널(상담원, 챗봇, 모바일 앱 UI, 키오스크) | REST/gRPC API Gateway, WebSocket 기반 Real-Time 채널, CAI(Conversational AI) NLU 엔진, NICE inContact·Genesys Cloud CX 같은 CCaaS(Contact Center as a Service) 솔루션 |
| **③ Backstage Actions** | 고객에게는 보이지 않지만 서비스 전달을 위해 직·간접적으로 수행되는 내부 활동(콜센터 상담원의 주문 입력, 심사 담당자의 대출 심사) | ESB(Enterprise Service Bus) 또는 Kafka 기반 Event Bus, RPA(UiPath, Automation Anywhere), BPM 엔진(Camunda 8, IBM BPM) |
| **④ Support Processes** | Frontstage·Backstage를 가능하게 하는 IT 인프라 및 부시스템(Core Banking, CRM, ERP, DW) | **MSA 환경**: Spring Cloud / Istio Service Mesh, **레거시 환경**: SOAP/WebSphere, **데이터**: Oracle Exadata·Snowflake, **인증**: OAuth 2.0 + OIDC + FAPI |
| **⑤ Physical Evidence** | 고객이 서비스를 통해 받게 되는 디지털/물리적 결과물(영수증, 이메일, 알림톡, 제품, 청구서) | 카카오 알림톡/친구톡, Apple Wallet Pass, 전자세금계산서, **접근성**: WCAG 2.1 AA, **보안**: 전자서명( 공동인증서, PASS), FIDO2/WebAuthn |

### 핵심 라인(Line)의 상세 정의

- **Line of Interaction(상호작용선)**: 고객과 서비스 제공자 간 직접 접점의 경계. 이 선을 기준으로 **API 호출 지점**, **UI/UX 터치포인트**, **SLA 측정 지점(TTFB, TTI, FCP)** 이 정의된다.
- **Line of Visibility(가시성선)**: 고객이 인지할 수 있는 영역(Frontstage)과 인지할 수 없는 영역(Backstage)의 경계. **정보 노출 원칙(Need-to-Know Basis)** 과 **개인정보보호법 제3조(개인정보의 처리 제한)** 의 기술적·관리적 보호조치 영역을 명시한다.
- **Line of Internal Interaction(내부상호작용선)**: 서비스 제공자 내부의 **고객 접점 조직(Channel)** 과 **후방 지원 조직(Back Office)** 의 경계. **RACI Matrix** 및 **BPMN Lane** 과 직접 매핑되며, **Service Desk -> 2nd Line -> 3rd Line** ITIL 에스컬레이션 경로의 기점이 된다.

```text
   시간축(Time) -------------------------------------------->

   ①고객   [앱실행] --> [본인인증] --> [정보입력] --> [동의] --> [완료]
              |            |            |            |          |
   - - - - - -|- Line of  |Interaction |- - - - - -|- - - - -|- - -
              |            |            |            |          |
   ②Front     |[SDK초기화] |[FIDO인증]  |[FormValidator]|[OTP]   |[SuccessPage]
              |            |            |            |          |
   - - - - - -|- Line of  |Visibility  |- - - - - -|- - - - -|- - -
              |            |            |            |          |
   ③Back      |            |[신원조회]  |[AML스캔]   |[서명검증]|[계좌생성]
              |            |            |            |          |
   - - - - - -|- Line of  |Internal    |- - - - - -|- - - - -|- - -
              |            |Interaction |            |          |
   ④Support   |[APM]      |[KYC엔진]   |[FDS]       |[eSign]   |[CoreBanking]
              |            |            |            |          |
   ⑤Evidence  |[Splash]   |[인증UI]    |[ProgressBar]|[Toast]   |[알림톡+Push]
```

### 핵심 알고리즘 및 설계 고려사항

1. **Moment of Truth(진실의 순간) 가중치 산정**: Jan Carlzon의 원래 정의를 확장하여, 각 고객 접점의 **감정 가중치(Emotional Weight, EW) = f(기대값, 실제 인식값, 회복 가능성)** 를 Forrester의 **Customer Experience Index(CX Index)** 알고리즘을 차용하여 0~100점으로 정량화한다.
2. **Blue-Green Blueprint 전략**: 기존 채널의 **As-Is(Blue)** 와 신규 디지털 채널의 **To-Be(Green)** 를 동일 도면에서 **Δ-Mapping(델타 매핑)** 으로 비교하여, 레거시 시스템의 **Strangler Fig Pattern** 적용 범위를 결정한다.
3. **Cynefin Framework 기반 복잡도 분류**: 단순·복잡·난해(Complicated)·혼돈(Chaotic) 영역별로 Blueprint의 상세도(Fidelity)를 차등 적용한다. 난해 영역(예: 보험 청구 심사)에는 **BPMN 2.0 + DMN(Decision Model and Notation)** 을 결합한 하이엔드 Blueprint가 필요하다.

- **📢 섹션 요약 비유**: 3개의 Line은 마치 **은행의 금고실 보안 구역선** 과 같다. 카운터 앞(Line of Interaction)은 손님과 창구 직원이 마주하는 일반 구역, 카운터 뒤 유리벽(Line of Visibility)이 그어져 손님은 안을 볼 수 없지만 직원끼리(Line of Internal Interaction)는 서로 협력한다. 그리고 금고실(Support Process)은 오직 권한자만 출입할 수 있도록 명확히 격리되어 있다.

---

## Ⅲ. 비교 및 연결

서비스 블루프린트는 단독으로 사용되기보다 다른 서비스 설계·분석 도구와 **상호 보완적** 으로 사용된다. 각 도구의 목적·관점·추상화 수준을 명확히 이해하고 조합하는 것이 기술사 답안의 핵심 역량이다.

| 구분 | **Service Blueprint** | **Customer Journey Map(CJM)** | **BPMN 2.0 Process Model** | **Value Stream Map(VSM)** | **UML Use Case Diagram** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관점(Who)** | 고객 + 서비스 제공자 통합 | **고객만** (Inside-Out -> Outside-In) | 서비스 제공자 내부 프로세스 | 가치 흐름(Value Flow) | 기능(Function) 단위 |
| **시각화 차원** | 행위자·가시성·시간 | 감정·터치포인트·시간 | 프로세스·게이트웨이·이벤트 | 시간·정보·재고 흐름 | Actor·Use Case·Boundary |
| **정량 데이터** | ◎ SLA, ART, FCR | △ 감정 곡선, NPS | ◎ 처리량, 리드타임 | ◎ Cycle Time, Takt Time | ✕ 일반적 |
| **정성 데이터** | ◎ 페르소나, 시나리오 | ◎ 페르소나, 감정, 페인포인트 | △ 일부(BPMN 확장) | △ 일부 | △ |
| **IT 시스템 연동** | ◎ APM, CRM, CDP | △ 데이터 부족 | ◎ WfMS(Camunda, Airflow) | △ MES | ◎ |
| **DX 적용 적합도** | **매우 높음** | 높음 | 매우 높음 | 중간(제조 친화) | 중간 |
| **주 사용 단계** | Define, Develop | Empathize, Define | Develop, Deliver | Analyze, Design | Define |
| **산출물 연계** | TOM, SLA, RACI | 페르소나, Storyboard | 실행 가능 워크플로우 | 린 개선 과제 | 요구사항 정의서 |

### 통합 아키텍처 연계 패턴

- **CJM -> Service Blueprint -> BPMN**: 고객의 감정 곡선
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 418 / 800

<- **이전**: [417. ITIL 4 서비스 가치 시스템 SVS](/studynote/12_it_management/05_security_compliance/417_itil_4_service_value_system_svs/)
**다음**: [419. 용량 계획 수요 예측 확장 전략](/studynote/12_it_management/05_security_compliance/419_capacity_planning_demand_forecasting/) ->

---
