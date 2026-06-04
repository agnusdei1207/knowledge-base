+++
title = "435. 요구사항 관리 추적 변경 제어 (Requirements Management Traceability)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 요구사항 관리(Requirements Management)는 IEEE 29148, BABOK v3, CMMI-DEV v2.0 기반으로 요구사항의 식별(Elicitation)->명세(Specification)->검증(Validation)->추적(Traceability)->변경통제(Change Control) 전生命周期(Lifecycle)을 통제하는 엔지니어링 Discipline이며, 추적성(Traceability)은 Pre-Trace(역추적: 요구사항↔원천), Forward-Trace(순추적: 요구사항↔설계↔코드↔테스트), Backward-Trace(역추적: 산출물↔요구사항)의 3축 매트릭스(RTM: Requirements Traceability Matrix)로 구현된다.
> 2. **가치**: 통계적으로 결함의 56%는 요구사항 단계에서 유발되며(Standish Group CHAOS Report 2020), RTM 자동화 시 회귀 테스트 케이스 도출 시간이 평균 73% 단축, 변경 영향 분석(Impact Analysis) 소요시간이 40~60% 감소하며, 감리인증(ISMS-P, SW감리) 시 추적성 부재는 1차 부적격 판정 사유 1위(약 38% 차지, NIPA 통계).
> 3. **판단 포인트**: 추적성 링크의 세분화 수준(Granularity: 단일 End-to-End vs. Fine-grained Object-level), 도구 종속성(Jama, DOORS NG, Polarion ALM, Azure DevOps, JIRA+Zephyr Scale 등 도입 시 Lock-in vs. ReqIF 기반 상호운용성), 형상관리 연동 방식(SVN/Git Tag ↔ 요구사항 Baseline), 그리고 CCB(Change Control Board) 운영 주기(반복주기 vs. Continuous Baselines) 간의 Trade-off가 핵심 의사결정 사안이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발 프로젝트에서 발생하는 재작업(Rework)의 약 50~80%는 요구사항의 모호성, 누락, 불일치에서 기인한다. IEEE 830-1998을 계승한 **ISO/IEC/IEEE 29148:2018** 표준은 요구사항 공학(Requirements Engineering)을 *Stakeholder Needs Definition Process*와 *System/Software Requirements Analysis Process*로 분리하여 정의하며, 각 단계에서 **추적성(Traceability)** 을 통해 요구사항의 출처(Source)와 도출 경로(Derivation)를 식별 가능한 형태로 유지하도록 명시한다.

특히 한국 정보시스템 감리(행정안전부 고시 제2023-5호)와 SW 품질인증(KOLAS), ISMS-P 인증 심사에서는 **RTM(요구사항 추적 매트릭스) 미수립 시 1차 부적격 처리**가 관행화되어 있으며, 발주처의 변경 요구사항을 체계적으로 통제하지 못해 발생한 계약 분쟁(예: 2022년 공공기관 SW사업 변경관리 분쟁 사례 약 142건, 국가계약법 분쟁조정위원회 통계)이 매년 증가 추세에 있어 변경 통제 프로세스의 형상관리적 접근이 필수적이다.

```text
+--------------------------------------------------------------------+
|        요구사항 관리·추적·변경 통제 체계 (V-Model 기반)            |
+--------------------------------------------------------------------+

  발주처(Stakeholder)        사업수행조직(System Integrator)
  ----------------            --------------------------
        |                              |
        | ① 요구사항 도출(Elicitation)  |
        |<------------------------------->| Interviews, Workshops
        |                              | Questionnaires, Prototypes
        |                              v
        |                    +------------------+
        |                    | BRS / URS / SRS  | <- IEEE 29148 / IEEE 830
        |                    | (Baseline v1.0)  |
        |                    +--------+---------+
        |                             |
        |                             v
        |                    +------------------+
        |   ② 검토/승인       |  CCB(Change Ctrl)| <- 형상관리위원회 운영
        |<---------------------|  Baseline 고정   |
        |   (Sign-off)        +--------+---------+
        |                             |
        |   ③ 변경 요청(CR/ECR)       | RFC #001~#N
        |------------------------------>|
        |                             v
        |                    +------------------+
        |                    | Impact Analysis  | <- RTM 기반 전/후방 추적
        |                    |  - 비용/일정/품질 |
        |                    |  - 위험평가       |
        |                    +--------+---------+
        |                             |
        |                             v
        |                    +------------------+
        |   ④ 변경 승인/반려 |  새 Baseline v1.1| <- SVN/Git Tag 연동
        |<---------------------|  결재/통보        |
        |                    +--------+---------+
        |                             |
        |                             v
        |                    +------------------+
        |                    |   추적성 검증     | <- Audit Trail
        |                    | (Traceability    |   DOORS/Jama Export
        |                    |   Verification)  |
        |                    +------------------+
```

과거 폭포수(Waterfall) 모델에서는 요구사항 명세서(SRS)가 승인되면 변경을 최소화하는 '동결(Freeze)' 방식을 취했으나, 애자일(Agile)·DevOps 환경에서는 **Living Requirements Document** 개념이 도입되어, 요구사항이 코드·테스트와 함께 Continuously Evolve 된다. 이에 따라 **도구 기반 자동 추적성(Automated Traceability)** 이 필수적으로 요구되며, ReqIF(Requirements Interchange Format) 1.2 표준을 통한 도구 간 호환성 확보가 글로벌 추세다.

- **📢 섹션 요약 비유**: 요구사항 관리는 마치 **건축물의 설계 변경 대장(Change Log)** 과 같다. 건물을 짓기 시작하면 벽을 허물기 어렵듯, 코드가 작성된 후 요구사항을 바꾸는 비용은 요구사항 단계의 20~200배(IBM Systems Sciences Institute, Barry Boehm 곡선)에 달하므로, 변경 대장과 설계 도면을 정확히 연결(추적성)해 두지 않으면 리모델링 시 어떤 벽이 구조벽인지 알 수 없어 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

요구사항 관리 시스템의 핵심은 **RDBMS(Relational DB) 기반의 이력 관리 + 도메인 특화 워크플로우 엔진 + 외부 형상관리/CI/CD 연동** 의 3-Layer 구조다. 국제 표준인 **ISO/IEC/IEEE 29148:2018** 은 요구사항의 속성(Attribute) 최소 14종(Identifier, Version, Source, Rationale, Owner, Priority, Status, Stability, Verification Method, Allocation, Type, Risk, Cost, Target Release)을 정의하며, 이 중 변경 통제와 직접 관련된 핵심 속성은 *Version, Status, Stability, Rationale, Owner* 다.

```text
+------------------------------------------------------------------+
|   요구사항 추적성 매트릭스 (RTM) - 3축 링크 구조                |
+------------------------------------------------------------------+

  Layer ① 원천추적 (Pre-Traceability: Why-Trace)
  +----------------------------------------------------------+
  | Stakeholder Need ---> Business Requirement --+            |
  |   (관심사/Needs)     (BRS의 Req. ID)        |            |
  +---------------------------------------------+------------+
                                                |
  Layer ② 시스템·소프트웨어 추적                 v
  +----------------------------------------------------------+
  | System Req. (SyRS) ---> S/W Req. (SRS) ---> S/W Design  |
  |   Sys-FN-001            SW-FN-001            SW-DS-014  |
  |   Sys-NF-005 (성능)     SW-NF-005            SW-DS-015  |
  +----------------------------------------------------------+
                                                |
  Layer ③ 후방추적 (Forward/Backward-Trace: What-Trace)        |
                                                v
  +----------------------------------------------------------+
  | Implementation ---> Unit Test ---> Integration ---> UAT    |
  |   Module.java         UT-014         IT-007        TC-203|
  |   commit: a1b2c3d                                     (User |
  |   branch: feature/REQ-123                            Acceptance)|
  +----------------------------------------------------------+

  ※ 누락된 링크(=Orphan)는 Coverage Gap으로 자동 식별되며
     Impact Analysis 시 양방향 그래프 순회(Traversal)로 활용
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **요구사항 저장소 (Doors/Database)** | 요구사항·속성·이력의 단일 진실 공급원(SSOT: Single Source of Truth) | Polarion, Jama Connect, IBM DOORS NG, Siemens Teamcenter, Azure DevOps Work Items, ReqIF 1.2 / RIF 표준; RDBMS(PostgreSQL/Oracle) + Revision Tag(SVN)/Commit Hash(Git) 매핑 |
| **추적성 엔진 (Traceability Engine)** | 요구사항↔설계↔코드↔테스트 간 링크의 생성·검증·탐색 | Link Type(Satisfies, Verifies, Refines, DerivesFrom, Conflicts) 기반 그래프 DB(Neo4j, ArangoDB) 또는 내장 관계 테이블; 순방향·역방향 자동화(IR-Tools, NLP 기반 Traceability Recovery: AnJuSeA, Taras) |
| **변경 통제 워크플로우 (CCB Process)** | ECR(Engineering Change Request) 접수->검토->승인->Baseline 업데이트 | ITIL v4 Change Management, IEEE 1028-2008 Review 표준, GitOps PR(Pull Request) + Code Owner 정책 연동; 4-Eyes Principle(검토자≠승인자) |
| **기반선 관리자 (Baseline & Configuration Manager)** | 승인된 요구사항 집합의 버전 고정과 배포 통제 | SVN Tagging, Git Branching(GitFlow/Trunk-Based), Semantic Versioning(SemVer), Artifactory/Nexus Binary Repository 연동; Baselines: α(내부)->β(고객)->GA(General Availability) |
| **영향 분석 도구 (Impact Analyzer)** | 변경 요구사항의 도메인 전파 효과(파급경로) 시각화 | 의존성 그래프(Dependency Graph) 알고리즘: BFS/DFS, PageRank, Betweenness Centrality; 비용·일정·리스크 산정(EVM: Earned Value Management) |
| **감사 추적기 (Audit Trail Logger)** | 누가, 언제, 무엇을, 왜 변경했는지 21 CFR Part 11 / ISO 9001 준수 기록 | Immutable Append-only Log(블록체인 옵션), WORM(Write Once Read Many) 스토리지, E-Signature 통합 |

핵심 메커니즘은 **추적성 링크의 무결성(Link Integrity)** 이다. IEEE 29148:2018 §6.4.4에서는 "추적성은 요구사항의 출처, 정당성(Rationale), 도출 경로, 구현, 검증 방법을 식별할 수 있어야 한다"고 명시하며, 이를 위해 다음 4가지 핵심 매개변수를 관리한다:

1. **Link Cardinality**: 1:1, 1:N, M:N 매핑. 일반적으로 다대다(M:N)를 허용하되, Orphan/Cyclic Link는 무결성 규칙(Integrity Rule)으로 차단.
2. **Granularity Level**: Requirement-to-Requirement(Coarse-grained, 빠르지만 부정확) ↔ Object-to-Object(Fine-grained, 정확하지만 비용^). 안전필수(Safety-Critical: DO-178C Level A) 시스템은 Fine-grained, 일반 행정시스템은 Coarse-grained.
3. **Coverage Metric**: % Coverage = (Linked Artifacts / Total Artifacts) × 100. SW감리 합격 기준 통상 ≥95% (Forward), ≥90% (Backward).
4. **Suspicion Index**: NLP(자연어처리) 기반 Trace Recovery 시 후보 링크의 신뢰도(0~1). 임계값 0.75 이상만 자동 채택, 이하는 수동 검토 큐로 라우팅.

**변경 통제의 수학적 모델**:
변경 요청 CR_i의 우선순위는 다속성 의사결정(MADM: Multi-Attribute Decision Making) 기법인 AHP(Analytic Hierarchy Process)로 산정한다:

$$P(CR_i) = w_1 \cdot Impact_i + w_2 \cdot Urgency_i + w_3 \cdot Cost_i^{-1} + w_4 \cdot Risk_i$$

여기서 ∑w_k = 1, w_k는 CCB에서 합의된 가중치. ISO/IEC 14764(S/W 유지보수) §6.4.2의 Change Priority 산정 모델과 동일.

- **📢 섹션 요약 비유**: 추적성 매트릭스(RTM)는 마치 **도서관의 교차 색인 시스템** 과 같다. 책(요구사항)을 저자별, 주제별, 출판연도별로 여러 번 분류해 두면, 한 권이 훼손됐을 때 "이 책에 의존한 다른 책들은 무엇인가?"를 즉시 찾을 수 있다. 만약 색인이 없으면 사서(개발자)가 모든 서가를 뒤져야 하듯, 변경 시 영향을 받는 코드를 찾기 위해 전체 코드베이스를 스캔해야 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | 수동 추적성 (Manual RTM, Excel/Word) | 도구 기반 자동 추적성 (DOORS/Jama/Polarion) | 애자일/리빙 문서 (User Story Map + JIRA) |
| :--- | :--- | :--- | :--- |
| **데이터 일관성** | 낮음 (중복 입력, 버전 충돌 빈번) | 높음 (SSOT, ACID 트랜잭션 보장) | 중간 (도구 간 동기화 필요) |
| **변경 영향 분석 시간** | 평균 16~24시간 (수작업 링크 갱신) | 평균 1~3시간 (그래프 자동 순회) | 30분~1시간 (Epic->Story->Task->Test 자동) |
| **감리/인증 대응** | 매우 어려움 (증적 부족) | 우수 (Audit Trail, 전자서명 내장) | 보통 (스크린샷·수동 Export 필요) |
| **초기 도입 비용** | 낮음 (Office 라이선스만) | 높음 (Seat License, 구축비, 교육) | 중간 (도구 종속) |
| **확장성(Scalability)** | 100개 Req 이하 소규모 한정 | 10,000개 Req 이상 대규모 가능 | Sprint 단위 (250~500 Story 적정) |
| **표준 준수** | IEEE 830/29148 부분 준수 | IEEE 29148, ISO 26262, DO-178C, IEC 62304 완전 준수 | BDD/TDD 결합 시 부분 준수 |
| **Lock-in 위험** | 없음 (파일 기반) | 높음 (벤더 종속, ReqIF로 부분 해소) | 중간 (Atlassian 생태계 종속) |
| **적합한 환경** | 1회성 소규모 SI, 프로토타입 | 국방/항공/의료/금융/원자력(안전필수) | SaaS, 모바일 앱, 스타트업 |

**연계 시스템과의 통합 포인트**:

- **형상관리(Git/SVN)**: `git commit -m "[REQ-123] 결제모듈 timeout 처리"`처럼 Commit Message에 Req ID를 강제 매핑. GitLab/GitHub Webhook으로 Polarion/Jama에 자동 링크 생성. 정책: Commitizen + Commitlint + Husky로 pre-commit hook 강제화.
- **CI/CD 파이프라인(Jenkins/GitHub Actions)**: PR(Pull Request) 생성 시 해당 PR의 Commit Message에서 Req ID를 파싱(Regex: `\[REQ-\d+\]`) -> RTM 자동 업데이트 -> Coverage < 95% 시 PR Block 정책 적용.
- **테스트 관리(Zephyr Scale, TestRail, qTest)**: Test Case의 *Trace* 필드에 Req ID 매핑 -> 자동 회귀 테스트 세트 도출 -> JUnit/XML Report를 Req Coverage Dashboard에 피드백.
- **이슈
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 435 / 800

<- **이전**: [434. 소프트웨어 개발 방법론 워터폴 애자일](/knowledge-base/studynote/12_it_management/05_security_compliance/434_software_development_waterfall_agile/)
**다음**: [436. 테스트 관리 품질 보증 자동화](/knowledge-base/studynote/12_it_management/05_security_compliance/436_test_management_quality_assurance_automation/) ->

---
