---
title: "Change Management CAB Impact Approval"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ITIL 4 기반 변경 관리(Change Management)에서 CAB(Change Advisory Board)는 RFC(Request for Change)에 대한 영향도(Impact), 긴급성(Urgency), 리스크(Risk)를 다차원적으로 평가하여 Normal/Significant/Emergency 변경의 승인 여부를 결정하는 거버넌스 거버넌스 거버넌스 거버넌스 거버넌스 거버넌스 합의 의사결정 기구이며, CMDB( Configuration Management Database) 의 CI( Configuration Item) 관계 그래프와 7R's( Requestor, Reason, Result, Risk, Resources, Responsibility, Relationship) 프레임워크를 기반으로 정량적/정성적 영향 분석을 수행한다.
> 2. **가치**: 적절한 CAB 영향 분석을 통해 운영 중단( Unplanned Outage) 을 평균 35~50% 감소시키고, 변경 실패율( Change Failure Rate) 을 DORA Four Key Metrics 의 Change Failure Rate 0~15% 이내로 관리할 수 있으며, Mean Time to Restore( MTTR) 단축 및 Post-Implementation Review( PIR) 품질 향상을 통해 Change Success Rate 95% 이상 달성이 가능하다.
> 3. **판단 포인트**: 표준 변경( Standard Change) 의 자동 승인( Pre-Authorized) 범위 설정, Emergency CAB( ECAB) 의 사전 정의된 에스컬레이션 경로, Significant Change 시 아키텍처 리뷰 보드( ARB) 및 정보보호 영향평가 동시 수행 여부, 그리고 DevOps/DevSecOps 환경에서의 Peer Review 기반 CAB 대체 가능성( 위험기반 접근법, Risk-Based Approach) 의 균형점이 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보시스템 환경에서 변경( Change) 은 단순한 코드 배포나 서버 패치 적용을 넘어, 비즈니스 서비스( Business Service) 의 가용성·보안성·성능·컴플라이언스( Compliance) 에 직결되는 핵심 리스크 요인이다. 통계적으로 프로덕션 장애의 70~80% 가 변경 작업에 기인하며, 무계획 변경( Unplanned Change) 이 전체 변경의 약 25~30% 를 차지할 때 평균 장애 시간( MTTR) 이 4시간 이상 증가한다( Gartner, 2023).

CAB( Change Advisory Board) 영향 분석 승인 프로세스는 ITIL Service Transition/Service Operation 영역의 핵심 거버넌스 메커니즘으로, **변경의 "정당성"**과 **"안전성"** 을 다층적 이해관계자( Change Manager, Incident Manager, Problem Manager, Release Manager, 정보보호 담당자, 서비스 오너, 기술 아키텍트, 외부 공급사) 의 합의로 검증한다. 이때 단순한 "Yes/No" 결정이 아니라, RFC( Request for Change) 에 내재된 7R's( Requestor, Reason, Result, Risk, Resources, Responsibility, Relationship) 와 영향도 매트릭스( Impact × Urgency × Priority) 를 정량화하여 의사결정 트레이스 어빌리티( Decision Traceability) 를 확보하는 것이 핵심이다.

기존의 "변경 통제 위원회" 라는 직역적 개념에서 탈피하여, 현대의 CAB 는 **자동화된 CI/CF( Configuration Management Database/Configuration File) 분석 + 정성적 전문가 판단 + 자동 승인 워크플로우( Standard Change Pre-Authorization)** 의 하이브리드 형태로 진화하고 있다. 특히 AIOps( Artificial Intelligence for IT Operations) 환경에서는 변경 영향 예측 모델( Change Risk Prediction Model) 이 도입되어, 과거 변경 이력, 인시던트 상관관계, 배포 패턴을 학습하여 CAB 검토 전 영향도 사전 점수화( Pre-Scoring) 가 이루어진다.

```text
+------------------------------------------------------------------+
|           Change Management : CAB 영향 분석 승인 전체 흐름         |
+------------------------------------------------------------------+
|                                                                  |
|  [서비스 운영 환경]                                               |
|        |                                                         |
|        v                                                         |
|  +--------------+    ① RFC 접수(Change Request)                 |
|  |  Change      |------------------------------------+           |
|  |  Requester   |  7R's / 영향도 / 긴급성 기재       |           |
|  |  (개발/인프라)|  +-----------------------------+   |           |
|  +--------------+  | 표준변경  -> 자동승인(Standard)|   |           |
|                    | 일반변경  -> CAB 검토(Normal)  |   |           |
|                    | 긴급변경  -> ECAB 즉시개최      |   |           |
|                    | 중대변경  -> ARB+ISMS 동시검토  |   |           |
|                    +-----------------------------+   |           |
|                                                    v           |
|                              +------------------------------+   |
|                              |   CAB 영향 분석 단계          |   |
|                              |  +------------------------+  |   |
|                              |  | ② CMDB CI 의존성 매핑   |  |   |
|                              |  |  - 직접영향(Direct)    |  |   |
|                              |  |  - 간접영향(Indirect)  |  |   |
|                              |  |  - 연쇄영향(Cascading) |  |   |
|                              |  +------------------------+  |   |
|                              |  +------------------------+  |   |
|                              |  | ③ 리스크 점수화(Risk)  |  |   |
|                              |  |  - 확률×영향도         |  |   |
|                              |  |  - 변경 복잡도 지수    |  |   |
|                              |  +------------------------+  |   |
|                              |  +------------------------+  |   |
|                              |  | ④ 영향도 매트릭스      |  |   |
|                              |  |  Impact(1~5) ×         |  |   |
|                              |  |  Urgency(1~5) =        |  |   |
|                              |  |  Priority(1~5)         |  |   |
|                              |  +------------------------+  |   |
|                              +------------------------------+   |
|                                                    |           |
|                                                    v           |
|                              +------------------------------+   |
|                              |  ⑤ CAB 회의/전자승인          |   |
|                              |  - 정족수(Quorum) 검증       |   |
|                              |  - 의사록(Minutes) 기록      |   |
|                              |  - 조건부 승인(With Plan)    |   |
|                              +------------------------------+   |
|                                                    |           |
|                                                    v           |
|                              +------------------------------+   |
|                              |  ⑥ 승인/거절/롤백 의사결정   |   |
|                              |  -> SMS(Change Record) 생성   |   |
|                              |  -> Release/Deploy 진행       |   |
|                              |  -> PIR(사후검토) 7일 이내     |   |
|                              +------------------------------+   |
+------------------------------------------------------------------+
```

**AS-IS( 전통적 CAB)** vs **TO-BE( 현대적 Risk-Based CAB)**

| 구분 | AS-IS (Waterfall/관료적 CAB) | TO-BE (Risk-Based/DevSecOps) |
|---|---|---|
| **결정 주체** | 10~20명의 주간 회의 | 3~5명 Change Manager + 자동화 + 도메인 전문가(On-Call) |
| **검토 시간** | 1~2주 Lead Time | 최소 1시간~1일, ECAB는 30분 이내 |
| **근거 데이터** | RFC 문서 정성적 기술 | CMDB 의존성 + 과거 변경 이력 + AIOps 예측 점수 |
| **승인 형태** | 회의록 서명 | ITSM Tool(ServiceNow, Jira Service Management)의 전자 워크플로우 + E-Sign |
| **리스크 모델** | 3단계(Low/Medium/High) | 확률분포 기반 5단계 + 7R's 정량화 |
| **DevOps 통합** | 별도 프로세스로 분리 | PR(Pull Request) 승인 게이트와 통합, GitOps Auto-Approval |
| **자동화율** | 10% 미만 | Standard Change 80% 이상 자동 승인 |

- **📢 섹션 요약 비유**: CAB는 마치 **"병원 수술 전 다학제 진료회의(Multi-Disciplinary Team, MDT)"** 와 같습니다. 외과의사(개발팀) 가 수술(배포) 을 주장하면, 마취과(인프라)·심장내과(보안)·혈액내과(데이터)·환자 본인(서비스 오너) 이 모여서 "이 수술이 정말 필요한가?", "다른 장기에 영향은?", "위험도는?" 을 함께 따져보는 것이지요. 응급수술(ECAB) 은 야간에도 최소한의 전문의만 모여 즉시 결정해야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CAB 영향 분석 승인 아키텍처는 **3계층 의사결정 프레임워크** 로 구성된다: (1) **데이터 수집 계층( CMDB, CMS, KEDB)**, (2) **분석 계층( Risk Scoring, Impact Analysis, AIOps Prediction)**, (3) **합의/승인 계층( CAB Meeting, E-Approval, Audit Trail)**. 이 세 계층은 ITSM 플랫폼( ServiceNow ITSM, BMC Remedy, Cherwell, Jira Service Management) 의 Change Management 모듈에서 워크플로우 엔진으로 통합 동작한다.

**CAB 영향 분석의 핵심 메커니즘**:
1. **RFC 제출**: Change Requester가 ITSM 시스템에 RFC 등록 -> 7R's 기입
2. **자동 분류( Auto-Classification)**: 변경 유형 자동 식별 (Standard/Normal/Emergency/Significant)
3. **CI 의존성 분석**: CMDB의 Relationship Map( Service->Application->Middleware->DB->Server->Network) 을 따라 영향 범위 자동 계산
4. **리스크 점수 산출**: Risk = P(변경 실패 확률) × I(영향도) × D(탐지 지연도) — D는 변경 후 모니터링 민감도
5. **이해관계자 매핑**: RACI 매트릭스( Responsible, Accountable, Consulted, Informed) 기반 자동 통지
6. **CAB 회의/전자승인**: 정족수(Quorum) 충족 시 의사결정, 조건부 승인 시 사전 조건(Pre-Condition) 검증
7. **PIR( Post-Implementation Review)**: 변경 종료 후 1~5 영업일 내 성공/실패/학습 항목 기록

```text
+--------------------------------------------------------------------+
|        CAB 영향 분석 승인 아키텍처 (3-Layer Decision Framework)     |
+--------------------------------------------------------------------+
|                                                                    |
|  [Layer 1] Data Collection & Discovery                            |
|  +----------+  +----------+  +----------+  +----------+           |
|  |  CMDB    |  |  CMS     |  |  KEDB    |  |  Observ- |           |
|  | (CI관계) |  |(Baseline)|  |(Known Err)| |  ability |           |
|  +-----+----+  +-----+----+  +-----+----+  +----+-----+           |
|        |              |              |            |                |
|        +--------------+--------------+------------+                |
|                              |                                     |
|                              v                                     |
|  [Layer 2] Analysis & Risk Scoring Engine                         |
|  +------------------------------------------------------------+   |
|  |  +------------------+  +------------------------------+   |   |
|  |  | CI Dependency     |  |  7R's 정량화 매트릭스          |   |   |
|  |  | Analyzer (BFS)    |  |  - Reason: 비즈니스 정당성    |   |   |
|  |  | - 1차 의존(직접)  |  |  - Result: 기대효과 KPI       |   |   |
|  |  | - 2차 의존(API)   |  |  - Risk:  P×I×D 공식         |   |   |
|  |  | - 3차 의존(인프라)|  |  - Relationship: 5단계 관계   |   |   |
|  |  +------------------+  +------------------------------+   |   |
|  |  +------------------+  +------------------------------+   |   |
|  |  | Change Risk      |  |  AIOps Predictive Engine     |   |   |
|  |  | Scoring Model    |  |  - XGBoost 분류 (성공/실패)  |   |   |
|  |  | P×I×D -> 1~25    |  |  - LSTM 시계열(장애예측)     |   |   |
|  |  | Priority 산출    |  |  - 변경-인시던트 상관관계     |   |   |
|  |  +------------------+  +------------------------------+   |   |
|  +------------------------------------------------------------+   |
|                              |                                     |
|                              v                                     |
|  [Layer 3] Consensus & Approval (CAB)                              |
|  +------------------------------------------------------------+   |
|  |  +------------------+  +------------------------------+   |   |
|  |  | CAB Member Pool  |  |  승인 의사결정 매트릭스        |   |   |
|  |  | - Change Manager |  |  ✓ 승인(Approved)             |   |   |
|  |  | - Service Owner  |  |  ⚠ 조건부승인(Conditional)    |   |   |
|  |  | - Security/CISO  |  |  ⏸ 보류(Deferred)            |   |   |
|  |  | - Infra/Cloud    |  |  ✗ 거절(Rejected)             |   |   |
|  |  | - App Architect  |  |  ⤺ 대안안건(Alternative RFC) |   |   |
|  |  | - Release Mgr    |  +------------------------------+   |   |
|  |  | - External Vendor|  +------------------------------+   |   |
|  |  | - BCM/DR 담당자  |  |  Audit Trail & Sign-Off      |   |   |
|  |  +------------------+  |  - E-Signature (PKI)         |   |   |
|  |                        |  - 회의록 자동 생성            |   |   |
|  |                        |  - 규제 컴플라이언스 로깅     |   |   |
|  |                        +------------------------------+   |   |
|  +------------------------------------------------------------+   |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **RFC(Request for Change)** | 변경 요청의 공식 문서화 | 7R's 필드( Requestor/Reason/Result/Risk/Resources/Responsibility/Relationship) + 영향도(Impact) + 긴급성(Urgency) 입력, ITSM Ticket Life-Cycle의 "Logged->Assessed->Authorized->Scheduled->Implemented->Reviewed" 6단계 |
| **CMDB(Configuration Management Database)** | CI(Configuration Item) 의 관계 그래프 저장소 | ServiceNow CMDB, BMC ADDM, Device42, ServiceNow CMDB IRE( Identification and Reconciliation Engine) 패턴 매칭, Discovery( Agent-based/Agentless/Cloud API) 로 자동 수집, Federation( 멀티 CMDB 통합) |
| **CAB(Change Advisory Board)** | 변경 승인 합의 의사결정 기구 | 정족수(Quorum) 5~7명, ITIL 권장 주 1회 회의, ServiceNow CAB Workbench로 가상회의, RACI 매트릭스 기반 자동 초대, 의사결정 시간 SLA( Normal: 5BP, Emergency: 1HR) |
| **ECAB(Emergency
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 425 / 800

<- **이전**: [424. 형상 관리 CMDB 구성 항목 관리](/studynote/12_it_management/05_security_compliance/424_configuration_management_cmdb_ci/)
**다음**: [426. 릴리스 관리 배포 전략 롤백](/studynote/12_it_management/05_security_compliance/426_release_management_deploy_strategy_rollback/) ->

---
