+++
title = "577. 로우코드 노코드 시민 개발자 거버넌스 (Low Code No Code Citizen Developer Governance)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LCNC(Low-Code/No-Code) 플랫폼에서 시민 개발자(Citizen Developer)가 작성한 비전문가 코드를 IT 거버넌스(CoE, 정책 엔진, DLP, 라이프사이클 관리) 하에 통제·검증·배포하기 위한 통합적 정책·기술·조직 프레임워크로, 메타데이터 기반 모델 실행 환경(MDRE)과 가드레일(Guardrail) 정책의 결합이 핵심입니다.
> 2. **가치**: Gartner 기준 2026년 전체 엔터프라이즈 애플리케이션의 70% 이상이 LCNC로 개발될 전망이며, 개발 생산성 5~10배 향상, Time-to-Market 60~80% 단축, IT 백로그 해소율 30~50%를 달성하면서도 보안·컴플라이언스 침해(Shadow IT)를 원천 차단할 수 있습니다.
> 3. **판단 포인트**: 시민 개발자의 자율성(Agility)과 중앙 IT의 통제력(Control) 사이의 균형점, PII/PCI 데이터 노출 방지를 위한 DLP 정책 강도, 라이선스 비용 대비 ROI(예: Power Platform per-user plan, Pay-as-you-go 모델), 그리고 레거시 시스템 통합 시 iPaaS(Boomi, MuleSoft) 또는 API Gateway(WSO2, Apigee) 연계 아키텍처 설계가 핵심 의사결정 사안입니다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경 및 정의

**로우코드/노코드(Low-Code/No-Code, LCNC)** 는 전통적인 손코딩(Hand-Coding) 없이 시각적 모델링(Visual Modeling), 드래그앤드롭(Drag & Drop), 선언적 워크플로우(Declarative Workflow), 사전 정의된 커넥터(Pre-built Connector)를 통해 애플리케이션을 구축하는 개발 패러다임입니다. **시민 개발자(Citizen Developer)** 는 공식적인 프로그래밍 교육이나 자격 없이, 비즈니스 부서(현업)에서 LCNC 플랫폼을 활용하여 업무용 애플리케이션을 직접 구축·배포하는 비전문 개발자를 의미하며, Gartner(2020~)에서 공식적으로 정의한 용어입니다.

그러나 시민 개발자의 자율적 개발은 필연적으로 **섀도우 IT(Shadow IT)**, **데이터 유출(Data Exfiltration)**, **컴플라이언스 위반**, **기술 부채(Technical Debt)** 라는 4대 리스크를 야기합니다. 이를 제어하기 위한 체계가 **LCNC 거버넌스(Governance)** 이며, Gartner는 이를 "시민 개발자 이니셔티브의 가드레일과 가속 페달을 동시에 제공하는 정책·인·프로세스 통합 프레임워크"로 정의합니다.

```text
+-------------------------------------------------------------------------+
|              LCNC 시민 개발자 거버넌스 개념도 (Concept Map)               |
+-------------------------------------------------------------------------+
|                                                                         |
|    [현업 부서]              [LCNC 플랫폼]              [중앙 IT/CoE]      |
|    +---------+             +----------+              +----------+      |
|    | 마케팅  |--요구사항--->|  Power   |<--거버넌스-- | CoE 정책 |      |
|    | 영업    |             |  Apps    |   정책 주입  | 가드레일 |      |
|    | 재무    |<--결과앱--- | ServiceNow|              | 보안감사 |      |
|    | HR      |             | Mendix   |              | 교육/멘토|      |
|    +---------+             | OutSys.  |              +----------+      |
|         |                  +----+-----+                   |            |
|         | 시민 개발자            |                         |            |
|         | (Citizen Dev)         v                         v            |
|         |              +-----------------+      +------------------+    |
|         +-------------->|  라이프사이클    |      |  정책 엔진       |    |
|                        |  Ideation->Build |      |  (DLP, OAuth,    |    |
|                        |  Test->Deploy    |      |   환경 분리)     |    |
|                        |  ->Retire        |      +------------------+    |
|                        +-----------------+                             |
|                                  |                                      |
|                                  v                                      |
|                  +------------------------------+                       |
|                  |  메타데이터 기반 모델 실행환경 |                       |
|                  |  (MDRE) + 커넥터 + 워크플로우 |                       |
|                  +------------------------------+                       |
+-------------------------------------------------------------------------+
```

### 1.2 왜 필요한가? (Old vs New Paradigm)

| 항목 | 기존 개발 패러다임 (Hand-Coding) | LCNC 시민 개발자 패러다임 |
|:---|:---|:---|
| 개발 주체 | 전문 개발자(SI/내부 IT) | 현업 + 시민 개발자(CoE 지원) |
| 개발 기간 | 3~12개월 (요구분석->테스트->배포) | 1일~4주 (프로토타입 즉시 구현) |
| 백로그(IT Backlog) | 평균 12~24개월 (Gartner, 2023) | 시민 개발로 30~50% 해소 |
| 거버넌스 수준 | 형상관리(Git), 코드 리뷰, SAST/DAST | 라이프사이클 승인, DLP, 환경 분리, eDNA |
| 리스크 | 인적 오류, 보안 취약점 | 섀도우 IT, 데이터 노출, 라이선스 남용 |
| 확장성 | 마이크로서비스, K8s 오토스케일 | 플랫폼 종속, 커넥터 한계, 멀티테넌시 |

한국 공공부문에서는 **행정안전부 「클라우드 이용 안내서」**, **NIPA 「클라우드 서비스 도입·운영 가이드라인」**, 그리고 2023년 **NIA 「공공부문 AI·디지털 전환 LCNC 도입 가이드」** 발간을 통해 공공기관의 LCNC 도입을 적극 권장하면서도 거버넌스 체크리스트를 의무화하고 있습니다.

- **📢 섹션 요약 비유**: LCNC 시민 개발은 마치 "회사 내에서 사내 공인된 레고 블록(CoE 정책)을 활용해 현업 직원이 직접 조립하는 것"과 같습니다. 블록의 종류(허용된 커넥터)와 조립 매뉴얼(DLP, 승인 절차)만 잘 정의해두면, 전기기사(전문 개발자) 없이도 안전하게 무언가를 만들 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 LCNC 거버넌스 4계층 아키텍처

LCNC 시민 개발자 거버넌스는 **① 플랫폼 계층, ② 정책/보안 계층, ③ 라이프사이클 계층, ④ 조직/문화 계층**으로 구성됩니다. 각 계층은 독립적으로 동작하면서도 상호 의존합니다.

```text
+--------------------------------------------------------------------------+
|                    LCNC 거버넌스 4계층 참조 아키텍처                       |
+--------------------------------------------------------------------------+
|                                                                          |
|  [4계층] 조직·문화 계층 (People & Culture)                                |
|   +------------------------------------------------------------+         |
|   |  CoE(Center of Excellence)  |  교육·멘토링  |  Maker Movement|         |
|   |  - Power Platform CoE Kit  |  - Citizen Dev Academy      |         |
|   |  - 성공 사례 공유           |  - 해커톤 운영               |         |
|   +------------------------------------------------------------+         |
|                                  | 거버넌스 정책 배포                      |
|                                  v                                        |
|  [3계층] 라이프사이클 계층 (App Lifecycle)                                 |
|   +------------------------------------------------------------+         |
|   | Idea -> Build -> Test -> Approve -> Deploy -> Monitor -> Retire|         |
|   |  -------  ------  -----  -------  ------  -------  ------ |         |
|   |  시민제안  샌드박스   ALM   CoE승인   프로덕션  텔레메트리  폐기|         |
|   |  Form     Maker       CI/CD  Change    App   Usage        |         |
|   |  등록     Portal      Pipeline Mgmt   Source  Analytics   |         |
|   +------------------------------------------------------------+         |
|                                  | 정책 enforcement                        |
|                                  v                                        |
|  [2계층] 정책·보안 계층 (Policy & Security)                                |
|   +------------------------------------------------------------+         |
|   | +----------+ +----------+ +----------+ +--------------+ |         |
|   | |DLP 정책  | |환경 분리 | |OAuth/Entra| |감사/로깅     | |         |
|   | |(PII/PCI) | |(Dev/Test/| |ID/조건부  | |(Activity Log)| |         |
|   | |차단 규칙 | | Prod)    | |액세스     | |eDNA 추적     | |         |
|   | +----------+ +----------+ +----------+ +--------------+ |         |
|   +------------------------------------------------------------+         |
|                                  | 정책 적용                               |
|                                  v                                        |
|  [1계층] 플랫폼 계층 (LCNC Platform & Integration)                        |
|   +------------------------------------------------------------+         |
|   |  +-------------+  +-------------+  +------------------+  |         |
|   |  | Visual IDE  |  | 메타데이터   |  |  커넥터/통합 계층 |  |         |
|   |  | (Drag&Drop) |  | 저장소(MDS) |  |  - 400+ Conn.    |  |         |
|   |  | - Form/View |  | - 테이블    |  |  - Custom Conn.  |  |         |
|   |  | - Workflow  |  | - 관계/규칙 |  |  - iPaaS Bridge  |  |         |
|   |  | - Dashboard |  | - 이벤트    |  |  (Boomi/MuleSoft)|  |         |
|   |  +-------------+  +-------------+  +------------------+  |         |
|   |              +----------------------+                      |         |
|   |              | MDRE (Model-Driven   |                      |         |
|   |              |  Runtime Engine)     |                      |         |
|   |              |  + 해석기/실행기     |                      |         |
|   |              +----------------------+                      |         |
|   +------------------------------------------------------------+         |
+--------------------------------------------------------------------------+
```

### 2.2 핵심 구성 요소 및 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **① 시각적 모델링 IDE** | 시민 개발자가 코딩 없이 UI/데이터/로직 설계 | Microsoft Power Apps Studio, Mendix Studio Pro, OutSystems Service Studio, Appian Designer, Salesforce Lightning App Builder. 캔버스 앱(Canvas, 자유 레이아웃) vs 모델 기반 앱(Model-Driven, 메타데이터 자동 생성) 두 가지 방식. |
| **② 메타데이터 저장소(MDS)** | 테이블, 컬럼, 관계, 비즈니스 규칙, 워크플로우를 DB화 | Dataverse(Common Data Service), Mendix Domain Model, OutSystems Entity-Relationship Meta. 런타임 엔진(MDRE)이 메타데이터를 해석해 동적 UI/API 생성. |
| **③ 커넥터/통합 계층** | SAP, Salesforce, DB, SaaS, REST/SOAP/OData 연동 | 표준 커넥터(400+), Custom Connector(Swagger/OpenAPI 3.0 등록), 온프레미스 데이터 게이트웨이(OPDG), iPaa스(MuleSoft, Boomi, Workato) 통한 하이브리드 통합 |
| **④ 정책 엔진 & DLP** | 데이터 유출 방지, 커넥터 사용 통제 | Microsoft Purview DLP, Power Platform Admin Center의 Connector Policy(블록/Business/Non-Business/Anonymous 4등급), CASB(McAfee, Netskope), AIP(Azure Information Protection) 라벨링 |
| **⑤ ALM(Application Lifecycle Mgmt)** | 버전 관리, 배포 파이프라인, 자동 테스트 | Power Platform Pipelines(YAML 기반), GitHub Actions / Azure DevOps 연동, Maker Portal 체크리스트, Test Studio(아웃시스템스), Mendix ATS |
| **⑥ CoE(센터 오브 엑셀런스) 툴킷** | 시민 개발 활동 가시화, 헬스체크, MVP 인증 | Power Platform CoE Starter Kit(Power BI 대시보드 + 앱 + 플로우 25개 컴포넌트), 멘디스 CoE 프레임워크, 마이크로소프트 Adoption Maturity Model 5단계 |
| **⑦ 환경 분리(EAL: Environment Strategy)** | Dev/QA/Prod 격리로 운영 안정성 확보 | Power Platform: Sandbox(Type 2), Production, Trial 3종 분리. 솔루션(Solution) 단위 export/import, Managed Solution로 운영 배포 |
| **⑧ 텔레메트리/거버넌스 대시보드** | 사용량, 비용, 보안 이벤트 모니터링 | Power Platform Admin Analytics, App Insights, ServiceNow ITSM 연동, 월간 Capacity Report(스토리지/요청 단위) |

### 2.3 핵심 원리: 메타데이터 주도 실행(MDRE)과 가드레일 메커니즘

**(1) 메타데이터 기반 런타임(MDRE, Model-Driven Runtime Engine)**
LCNC 플랫폼의 본질은 모든 애플리케이션이 **메타데이터**(테이블 정의, 폼 레이아웃, 워크플로우 노드 그래프, 비즈니스 규칙 트리)로 표현되고, 런타임 엔진이 이를 해석(Interpret)하여 동적으로 UI/API/로직을 생성하는 것입니다. 이는 전통적인 컴파일러 기반 실행(Hand-Coded MSA)과 대비되며, **"한 번 정의하면 웹/모바일/API 3채널이 자동 생성"** 되는 특성을 가집니다.

**(2) 가드레일(Guardrail) 정책 모델**
- **선제적 통제(Preventive)**: 사용자가 DLP 위반 액션을 시도할 때 즉시 차단(예: 주민등록번호 컬럼 생성 차단, 외부 커넥터 호출 시 추가 인증 요구)
- **탐지적 통제(Detective)**: 활동 로그, eDNA(electronic DNA) 패턴 분석, 이상 행위 탐지
- **교정적 통제(Corrective)**: 정책 위반 앱 자동 격리, 관리자 알림, 사고 대응 플레이북 실행

**(3) 시민 개발자 권한 모델(CIAM-like)**
```
[일반 시민 개발자]
  +- Create Apps in Personal/Team Environment
  +- Use: Standard Connectors (SharePoint, Excel, Outlook)
  +- Restricted: Premium Connectors, Dataverse, HTTP/Webhook

[인증 시민 개발자(MVP, Maker of the Month)]
  +- + Access to Team Environment
  +- + Premium Connectors (with approval)
  +- + Shared Mailbox, Group Connections

[프로 시민 개발자(Fusion Team 소속)]
  +- + Deploy to Production (via ALM Pipeline)
  +- + Custom Code(Plugin/PCF, JavaScript Snippet)
  +- + Service Principal 사용 가능
```

- **📢 섹션 요약 비유**: MDRE은 "레시피북(메타데이터)을 읽어서 자동으로 요리(앱)를 만드는 주방 로봇"이고, 가드레일 정책은 "이 주방에서 칼(위험 커넥터)은 자물쇠가 걸려 있고, 화구(외부 API)는 관리자 승인 후 사용 가능"이라는 안전장치입니다. 시민 개발자는 그저 레시피북에 새로운 레시피를 추가하기만 하면 됩니다.

---

## Ⅲ. 비교 및 연결

### 3.1 LCNC 플랫폼 간 비교

| 구분 | Microsoft Power Platform | Mendix | OutSystems | ServiceNow App Engine | Appian |
|:---|:---|:---|:---|:---|:---|
| **개발 방식** | Canvas + Model-Driven | Low-Code (시각 모델 우선) | High-Performance Low-Code | 워크플로우/ITSM 중심
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 577 / 600

<- **이전**: [576. 메타버스 가상 공간 인터랙션 설계](/knowledge-base/studynote/11_design_supervision/06_exam_summary/577_metaverse_virtual_space_interaction_desi/)
**다음**: [578. RPA 프로세스 자동화 봇 관리](/knowledge-base/studynote/11_design_supervision/06_exam_summary/578_rpa_process_automation_bot_management/) ->

---
