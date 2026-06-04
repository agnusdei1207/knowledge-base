+++
title = "586. IT 경영 관리 핵심 토픽 586번 시험 요약 (IT Management Core Topic 586 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019는 **Governance Objective(40개) -> Design Factor(11개) -> Focus Area -> Process(40개) -> Activity -> Metric**으로 이어지는 **End-to-End 거버넌스 체계**이며, ISO 38500의 6원칙(책임·전략·취득·성과·규정·인간)과 EDM( Evaluate-Direct-Monitor) 사이클을 통해 IT 의사결정의 권한·책임·보고 체계를 표준화한다.
> 2. **가치**: 글로벌 ISACA 조사에서 COBIT 도입 기업은 **IT 프로젝트 실패율 35%->12%**, **컴플라이언스 비용 40% 절감**, **IT-BSC Balanced Scorecard 적용 시 전략 실행률 평균 28% 향상**(Gartner 2022) 등 정량적 효과를 입증했다.
> 3. **판단 포인트**: 거버넌스 모델 선택 시 **집중형(Centralized, 예: 금융·공공) vs 분산형(Federated, 예: 글로벌 제조) vs 하이브리드**의 Trade-off, 그리고 **성숙도 Level 2(반복 가능) -> Level 3(정의됨) -> Level 4(관리됨) -> Level 5(최적화)** 중 현실적 목표 수준 설정이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 관리는 2000년대 초반까지 **Cost Center(비용 센터)** 관점이었으나, 디지털 전환이 가속화되면서 IT는 **Value Creator(가치 창출자)**로 재정의되어야 했다. 그러나 많은 기업이 겪는 현실적 문제는 ① CIO가 사업 전략과 IT 전략을 연결하지 못하고, ② IT 투자의 ROI(투자대비효과)가 정당화되지 않으며, ③ 리스크·컴플라이언스·보안 이슈가 사후적으로 발견된다는 점이다. ISACA의 2023 State of Cybersecurity 보고서에 따르면, 글로벌 기업 65%가 "IT 거버넌스 부재가 보안 사고의 근본 원인"이라고 응답했다.

**586번 토픽**이 다루는 영역은 바로 이 **"IT 투자-전략-리스크-성과를 하나의 프레임워크로 통합 관리"**하는 능력이며, 이를 위해 **COBIT 2019, ISO/IEC 38500, ITIL 4, IT-BSC, PMBOK, ISO 27001**이 상호 보완적으로 사용된다.

```text
+------------------------------------------------------------------------+
|            586번 토픽: IT 경영관리 통합 프레임워크 (5대 축)              |
+------------------------------------------------------------------------+
|                                                                        |
|  +----------+    +----------+    +----------+    +----------+         |
|  | 전략/비전 |---->|  거버넌스 |---->|  프로세스 |---->|  측정/성과|        |
|  |  (BSC)   |    |(COBIT19) |    | (ITIL4)  |    |  (KPI)   |         |
|  +----------+    +----------+    +----------+    +----------+         |
|        |              |              |              |                  |
|        +--------------+--------------+--------------+                  |
|                          |                                            |
|                          v                                            |
|                +----------------------+                               |
|                | 리스크/보안(ISO 27001)|<----- PDCA 사이클              |
|                +----------------------+      (Plan-Do-Check-Act)      |
|                                                                        |
+------------------------------------------------------------------------+
```

기존 패러다임(Pre-2010)은 **프로젝트 단위 관리**에 그쳤으나, 새로운 패러다임(2010 이후)은 **엔터프라이즈 거버넌스** 차원에서 IT를 다룬다. 이는 **사후 대응 -> 사전 예방**, **부서 단위 -> 전사 통합**, **재무 KPI만 -> 재무+고객+내부프로세스+학습성장(BSC 4관점)**으로 진화한 것이다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 도시계획(Urban Planning)**과 같다. 건물 하나 짓는 것(프로젝트 관리)이 아니라, 상하수도·전기·도로·치안 등 도시 인프라 전체를 **종합规划设计**하는 것이 거버넌스다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가. COBIT 2019 핵심 아키텍처 (5개 도메인, 40개 거버넌스/관리 목표)

```text
                +-------------------------------------+
                |  COBIT 2019 Core (40 Objectives)    |
                +-------------+-----------------------+
                              |
        +---------------------+---------------------+
        v                     v                     v
+---------------+    +----------------+    +----------------+
| EDM Domain    |    |  APF Domain    |    |  BAI/DSS/MEA   |
| (거버넌스)    |    |  정렬/계획/조직 |    |  구축/배치/서비|
|               |    |                |    |  스/모니터링   |
| 5 Objectives  |    | 14 Objectives  |    | 스/평가        |
|               |    |                |    |                |
| EDM01~05      |    | APO01~14       |    | BAI01~11       |
| (Evaluate-    |    |                |    | DSS01~06       |
|  Direct-      |    |                |    | MEA01~04       |
|  Monitor)     |    |                |    |                |
+---------------+    +----------------+    +----------------+
        |                     |                     |
        +---------------------+---------------------+
                              v
                +------------------------------+
                |  ① Cascading Goals (전략연결)|
                |  ② Design Factors (11개)     |
                |  ③ Focus Areas (N개)         |
                |  ④ Component: Process/Org/   |
                |     Info/Flow/People/Skill/  |
                |     Infrastructure/App      |
                +------------------------------+
```

### 나. ISO/IEC 38500 IT 거버넌스 6원칙 (Global Standard)

ISO 38500은 **2008년 제정, 2015년 개정**된 IT 거버넌스의 국제 표준으로, **3개 태스크(EDM: Evaluate-Direct-Monitor) × 6원칙 × 5개 적용 모델**의 매트릭스 구조다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **6원칙 (Principles)** | 의사결정 평가 기준 | ①Responsibility(책임), ②Strategy(전략), ③Acquisition(취득), ④Performance(성과), ⑤Conformance(규정준수), ⑥Human Behavior(인간행동) |
| **EDM 모델 (3 Tasks)** | 이사회·경영진의 거버넌스 사이클 | **Evaluate(평가)** -> **Direct(지시)** -> **Monitor(모니터링)**의 순환. 각 단계에서 6원칙을 모두 적용 |
| **COBIT 2019** | EDM 5개 목표(EDM01~05)와 매핑 | EDM01=거버넌스 체계 수립, EDM02=가치 전달 보장, EDM03=리스크 최적화, EDM04=리소스 최적화, EDM05=이해관계자 투명성 |
| **IT-BSC (4관점)** | 전략 KPI 측정 | 재무(Financial)·고객(Customer)·내부프로세스(Internal Process)·학습성장(Learning & Growth) — Kaplan & Norton(1992) |

### 다. COBIT 2019의 11개 Design Factor (설계 인자)

거버넌스 시스템은 **단일 정답이 없으며**, 기업이 다음 11개 요인을 분석해 자체적으로 **거버넌스 시스템 정의**를 도출한다:

1. **Enterprise Strategy** (전략: Growth/Acquisition/Innovation/Cost Leadership 등)
2. **Enterprise Goals** (사업 목표, 13개 표준 목표)
3. **Risk Profile** (리스크 성향, 5단계 척도)
4. **I&T Related Issues** (IT 관련 이슈)
5. **Threat Landscape** (위협 환경)
6. **Compliance Requirements** (규정 준수: GDPR, PCI-DSS, ISMS-P, HIPAA 등)
7. **Role of IT** (IT 역할: Support/Factory/Strategic/Turnaround)
8. **IT Sourcing Model** (내부/외주/하이브리드/클라우드)
9. **IT Implementation Methods** (Agile/DevOps/Waterfall)
10. **Technology Adoption Strategy** (선도/조기/후기/보수적)
11. **Enterprise Size** (대기업/중견/중소)

**예시**: 금융권(전략=안정성 우선, Risk Profile=매우 높음, Role of IT=Factory) -> EDM03(리스크 최적화)에 높은 우선순위 부여, BAI(구축/배치) 프로세스 강화

### 라. COBIT 2019 Capability/Maturity Model (CMMI 연계)

```text
Level 0: Incomplete       <--- 프로세스 없음
Level 1: Initial         <--- 개인 능력에 의존, 비체계적
Level 2: Managed         <--- 계획 수립, 성과 관리
Level 3: Defined         <--- 전사 표준 프로세스 적용
Level 4: Quantitative    <--- 정량적 측정/통제
Level 5: Optimizing      <--- 지속적 개선 (PDCA)
```

각 Level은 **Process Attribute(PA)** 6개(PA1.1~PA2.5)로 세분화 평가하며, **목표 성숙도 설정** 시 벤치마크는 동종 업계 평균 ±0.5 Level이다.

- **📢 섹션 요약 비유**: COBIT 2019의 EDM 사이클은 **자동차 운행**과 같다. **Evaluate(내비게이션 확인)** -> **Direct(핸들/가속 페달 조작)** -> **Monitor(계기판·후방 카메라)**가 실시간으로 반복되어야 안전한 주행이 가능하다.

---

## Ⅲ. 비교 및 연결

### 가. IT 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ISO 38500** | **ITIL 4** | **IT-BSC** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스/관리 통합 프레임워크 | IT 거버넌스 국제 표준 | IT 서비스 관리(SM) 베스트 프랙티스 | 전략 KPI 측정 | 프로젝트 관리 지식체계 |
| **범위** | 전사(End-to-End) 거버넌스 | 거버넌스 원칙·태스크(EDM) | 서비스 운영·지원·전환 | 성과 측정에 특화 | 프로젝트 단위 |
| **구조** | 5도메인/40목표/11 Design Factor | 6원칙 × 3 EDM 태스크 | 34개 Practice, 4 Dimension | 4관점 × BSC 전략맵 | 8 Performance Domain, 12 Principle |
| **측정 단위** | Capability Level 0~5 + Process Attribute | 원칙 준수도 평가 | Service Value Chain 성과 | KPI/Cause-Effect 관계 | 프로젝트 KPI (SPI, CPI, EAC) |
| **주 사용자** | CIO, 이사회, 감사인 | 이사회·경영진 | IT 운영팀, Service Desk | CISO, 전략기획 | PMO, 프로젝트 매니저 |
| **연도/버전** | 2019 (이전 5.x) | 2015 (개정) | 2019 (축 전환) | 1992/1996 (Norton&Kaplan) | 2021 (7th) |
| **인증/감사** | COBIT 2019 Foundation/Design/Implement | ISO 38500 Lead Auditor (BSI/PECB) | ITIL 4 Foundation/Master | BSC Certified (Palladium) | PMP/PfMP (PMI) |
| **보안 연계** | APO12, APO13 (리스크/보안) | Principle 5 (규정준수) | Practice: Information Security Mgmt | Internal Process 관점 | Resource Management |
| **클라우드 대응** | 클라우드 Focus Area 별도 제공 | 직접 언급 없음 (원칙 기반) | Cloud-native Practice 포함 | 직접 없음 (전략은 가능) | 적응형(Adaptive) 접근 포함 |
| **한계** | 구현 복잡도 높음, 의사결정 지연 가능 | 추상적 원칙, 구체 프로세스 부재 | 거버넌스 상위 체계 부재 | KPI 설정 난이도 높음 | 프로젝트 외 운영 영역 미포함 |

### 나. 상호 연계 구조 (Integration Map)

```text
+--------------+      +--------------+
| ISO 38500    |      | PMBOK 7      |
| (거버넌스 원칙)|<------>| (프로젝트 실행)|
+------+-------+      +------+-------+
       | ① 원칙 제공         | ③ 실행 KPI 제공
       v                     v
+----------------------------------+
|   COBIT 2019 (거버넌스/관리)     |
|   - 40 Objectives                |
|   - 11 Design Factors            |
+------+---------------------------+
       | ② 프로세스·활동 정의
       v
+--------------+      +--------------+
| ITIL 4       |      | IT-BSC       |
| (서비스 운영) |<------>| (성과 측정)   |
+--------------+      +--------------+
       | ④ 운영 데이터     | ⑤ 전략 KPI
       +--------+----------+
                v
       +------------------+
       | ISO 27001/ISMS-P |
       | (보안 통제)       |
       +------------------+
```

**실무 연계 시나리오**:
- ISO 38500 -> **이사회 거버넌스 의사결정** (분기 1회)
- COBIT 2019 -> **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 586 / 800

<- **이전**: [585. IT 경영 관리 핵심 토픽 585번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/585_it_management_core_topic_585_exam_summary/)
**다음**: [587. IT 경영 관리 핵심 토픽 587번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/587_it_management_core_topic_587_exam_summary/) ->

---
