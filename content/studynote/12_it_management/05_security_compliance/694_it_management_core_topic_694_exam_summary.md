---
title: "694. IT 경영 관리 핵심 토픽 694번 시험 요약 (IT Management Core Topic 694 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance & Management)는 COBIT 2019, ISO/IEC 38500, ITIL 4, Balanced Scorecard 등 글로벌 거버넌스 프레임워크를 기반으로, **IT 전략(IT Strategy) ↔ EA(Enterprise Architecture) ↔ IT 포트폴리오 ↔ IT 서비스 운영 ↔ 가치 측정(Benefits Realization)**을 하나의 통합 가치 사슬(Value Chain)로 연결하여 조직의 디지털 목표 달성을 지원하는 경영 체계이다.
> 2. **가치**: Forrester(2023) 및 McKinsey(2024) 조사에 따르면 체계적 IT 거버넌스 적용 조직은 **정보화 투자 대비 ROI가 평균 28% 향상**, IT 프로젝트 실패율 35%->12% 감소, 사이버 보안 사고 대응 시간(MTTR) 64% 단축, 그리고 디지털 전환(DX) 성숙도 2단계 상승 등 정량·정성적 가치를 동시에 확보한다.
> 3. **판단 포인트**: 기술사는 **"거버넌스-전략-아키텍처-운영-측정"** 5계층 모델에서 (a) Shadow IT 통제 vs 현장 자율성, (b) 중앙집중식 EA 거버넌스 vs 분산형 페도레이션(Federated EA), (c) Agile/DevOps 도입에 따른 거버넌스 경량화(Light-weight Governance) vs 통제 강화, (d) Capex/OpEx 혼합 클라우드 비용 모델 — 이 네 가지 핵심 트레이드오프에 대한 명확한 판단 기준을 제시할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경 및 등장 배경

2010년대에 들어오면서 **클라우드 컴퓨팅(Cloud Computing)**, **모바일 우선(Mobile First)**, **빅데이터/AI**, 그리고 **제로 트러스트(Zero Trust)** 보안 모델이 IT 환경의 근본적 변화를 주도하였다. Gartner(2024) 보고에 따르면 글로벌 IT 지출은 5.1조 USD에 달하며, 이 중 **전통적 On-Premise 투자는 -3.2%** 감소하는 반면 **클라우드·AI·SaaS 투자는 +18.7%** 증가하는 등 IT 투자 구조 자체가 패러다임 전환을 겪고 있다.

특히 한국 정보화진흥법(2023년 개정) 및 공공부문 정보시스템 구축·운영 지침(행정안전부, 2024)은 **EA(Enterprise Architecture) 수립 의무화, 정보화사업 예비타당성조사(예타) 강화, ISMP(정보시스템 마스터플랜) 수립 가이드라인** 등을 통해 IT 거버넌스의 법적·제도적 근거를 강화하였다.

### 1.2 핵심 문제점(Pain Points)

| 문제 영역 | 구체적 현상 | 비즈니스 임팩트 |
|:---|:---|:---|
| Shadow IT | 부서 단위 SaaS 도입, BYOD 무분별 사용 | 보안 사고 42% 증가(IBM, 2023), 라이선스 중복 비용 연 평균 1,200만 USD |
| IT-Biz 불일치 | 정보화 투자 100건 중 평균 27%가 전략과 미연계(Standish Group CHAOS Report 2023) | ROI 미달, ROI 측정 불가 비율 58% |
| 중복 투자 | 시스템 간 데이터 사일로(Silo), 동일 기능 중복 개발 | 5년간 평균 23% 예산 낭비 |
| 보안·컴플라이언스 | GDPR, 개인정보보호법, PCI-DSS, ESG 공시 등 규제 급증 | 위반 시 매출의 최대 4%(GDPR) 또는 10억원(국내) 과징금 |
| 디지털 전환(DX) 부재 | 레거시 시스템 의존도 70% 이상, 기술 부채(Technical Debt) 누적 | 신규 비즈니스 출시 시간(Time-to-Market) 3.6배 지연 |

### 1.3 IT 경영 관리의 5대 핵심 영역

```text
+-----------------------------------------------------------------------------+
|              IT 경영 관리 통합 프레임워크 (5-Layer Model)                    |
+-----------------------------------------------------------------------------+
|                                                                             |
|  +-------------------+   ① 거버넌스 계층 (Governance Layer)               |
|  |  ISO 38500        |   - 이사회(Board) 수준 의사결정 구조                |
|  |  COBIT 2019       |   - 40개 Governance & Management Objective          |
|  |  ISMS / PIMS      |   - 3단계: Evaluate -> Direct -> Monitor             |
|  |  정책/규정 체계    |   - RACI Matrix (Responsible, Accountable, ...)    |
|  +-------------------+                                                       |
|           ^                                                                  |
|  +-------------------+   ② 전략 계층 (Strategy Layer)                     |
|  |  IT 전략 계획(ISP) |   - 3~5년 중장기 로드맵, ISMP                       |
|  |  디지털 전환(DX)  |   - 외부환경(STEEP) + 내부역량(VRIO) 분석          |
|  |  BIZ-IT Alignment |   - Henderson & Venkatraman Strategic Alignment    |
|  |  투자 우선순위     |   - 포트폴리오 분석(BCG Matrix, Risk-Value Grid)  |
|  +-------------------+                                                       |
|           ^                                                                  |
|  +-------------------+   ③ 아키텍처 계층 (Architecture Layer)              |
|  |  EA Framework     |   - TOGAF 10 ADM, FEAF, DoDAF, Zachman              |
|  |  4A/5A 모델       |   - BA/DA/AA/TA/SA(또는 PA)                        |
|  |  표준/표준화       |   - 참조 모델(TRM: Technical Reference Model)     |
|  |  거버니/복잡도     |   - 적정 아키텍처 복잡도(Cyclomatic/Modularity)  |
|  +-------------------+                                                       |
|           ^                                                                  |
|  +-------------------+   ④ 운영 계층 (Operations Layer)                    |
|  |  ITIL 4 / SVS     +   - 34개 Practice (Change, Incident, Problem...)  |
|  |  DevOps / SRE     |   - DORA 4대 지표(배포빈도, 리드타임, MTTR, 변경실패)|
|  |  ITSM / CMDB      |   - SLA 99.9% / 99.99% / 99.999%                  |
|  |  AIOps/관측가능성  |   - MTTD/MTTR, Observability(Logs·Metrics·Traces) |
|  +-------------------+                                                       |
|           ^                                                                  |
|  +-------------------+   ⑤ 측정·가치 계층 (Measurement & Value Layer)     |
|  |  Balanced Scorecard|   - 4 관점(재무·고객·내부·학습성장)               |
|  |  KPI / KRI         |   - Leading & Lagging Indicator                  |
|  |  Benefits Realiz.  |   - 단계: Plan -> Execute -> Realize -> Sustain      |
|  |  Cost Transparency |   - TCO(전체소유비용), FinOps, Showback/Chargeback|
|  +-------------------+                                                       |
|                                                                             |
|  <----- 3단계 통제 루프: Evaluate(평가) -> Direct(지시) -> Monitor(모니터링) --->|
|  <----- 피드백 루프: Lessons Learned -> Continual Improvement (PDCA+SDCA) --->|
+-----------------------------------------------------------------------------+
```

### 1.4 Old Paradigm vs New Paradigm

```text
+-----------------------------+-----------------------------+
|  과거 (Old Paradigm)        |  현재 (New Paradigm)         |
+-----------------------------+-----------------------------+
|  IT = 비용(Cost Center)     |  IT = 가치 창출 엔진         |
|  프로젝트 중심(Project)     |  제품 중심(Product)          |
|  Waterfall, 연 1~2회 배포   |  Agile/DevOps, 일 수십 회    |
|  Capex(자본) 일변도          |  OpEx/Subscription 병행     |
|  내부 데이터센터 자체 운영   |  하이브리드/멀티 클라우드    |
|  사후 통제(After-the-fact)  |  예방 통제 + 자동화 통제     |
|  중앙 집중 통제(Hub & Spoke)|  페도레이션(Hub of Hubs)    |
|  보안 = 방화벽/경계         |  Zero Trust(신뢰 없음)      |
|  KPI = 가용성/다운타임      |  KPI = 고객경험/가치실현     |
+-----------------------------+-----------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 종합规划设计(종합계획 수립)**와 같습니다. 토지이용(EA)·교통(서비스)·치안(보안)·재정(투자)·환경(컴플라이언스)·시민만족도(BSC)를 별개로 다루면 도시가 혼란에 빠지듯, IT도 5계층을 통합 설계해야 비로소 **"살고 싶은 디지털 도시"**가 만들어집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 COBIT 2019 기반 거버넌스 시스템 구성

COBIT 2019는 ISACA가 발표한 글로벌 IT 거버넌스 프레임워크로, **40개의 Governance & Management Objective**를 5개 도메인으로 분류한다.

```text
+----------------------------------------------------------------------+
|            COBIT 2019 Core Model (40 Objectives)                    |
+----------------------------------------------------------------------+
|                                                                      |
|  EDM(01~05) - 거버넌스 영역 (이사회/경영진)                          |
|  +----------------------------------------------------+             |
|  | EDM01: 거버넌스 체계 설정    EDM02: 성과 모니터링   |             |
|  | EDM03: 위험 최적화         EDM04: 자원 최적화       |             |
|  | EDM05: 이해관계자 투명성 확보                       |             |
|  +----------------------------------------------------+             |
|                                                                      |
|  APO(06~17) - 정렬/계획/조직 (Alignment, Plan, Organize)            |
|  +----------------------------------------------------+             |
|  | APO01: 관리 프레임워크     APO02: 전략             |             |
|  | APO03: 기업 아키텍처       APO04: 혁신              |             |
|  | APO05: 포트폴리오         APO06: 예산/비용          |             |
|  | APO07: 인력              APO08: 관계              |             |
|  | APO09: 서비스 협약(SLA)   APO10: 공급자            |             |
|  | APO11: 품질              APO12: 위험              |             |
|  | APO13: 보안              APO14: 데이터             |             |
|  +----------------------------------------------------+             |
|                                                                      |
|  BAI(18~27) - 구축/실행/감시 (Build, Acquire, Implement)            |
|  +----------------------------------------------------+             |
|  | BAI01: 프로그램           BAI02: 요구사항          |             |
|  | BAI03: 솔루션 식별/구축   BAI04: 가용성/전환        |             |
|  | BAI05: 조직 변화 관리     BAI06: IT 변경            |             |
|  | BAI07: IT 인수/이행       BAI08: 지식              |             |
|  | BAI09: 자산              BAI10: 구성              |             |
|  +----------------------------------------------------+             |
|                                                                      |
|  DSS(31~36) - 전달/지원/서비스 (Deliver, Service, Support)           |
|  +----------------------------------------------------+             |
|  | DSS01: 운영 관리          DSS02: 서비스 요청/사고  |             |
|  | DSS03: 문제 관리          DSS04: 연속성            |             |
|  | DSS05: 보안 서비스        DSS06: 비즈니스 통제     |             |
|  +----------------------------------------------------+             |
|                                                                      |
|  MEA(37~40) - 모니터링/평가/감사 (Monitor, Evaluate, Assess)        |
|  +----------------------------------------------------+             |
|  | MEA01: 성과/준수         MEA02: 내부 통제 체계     |             |
|  | MEA03: 외부 요구사항     MEA04: 감사               |             |
|  +----------------------------------------------------+             |
|                                                                      |
|  -> Cascade to: -> Goals Cascade <-  Enterprise Goals -> Alignment     |
|                  Goals -> IT Goals -> Process Goals                    |
+----------------------------------------------------------------------+
```

### 2.2 핵심 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **거버넌스 위원회 (IT Steering Committee)** | 전략적 의사결정, 투자 우선순위, 위험 수용 기준 설정 | 분기별 정례 회의, RACI 매트릭스, 의사결정 권한 매트릭스(DAM: Decision Authority Matrix) Level 1~5 |
| **EA(Enterprise Architecture) 팀** | 아키텍처 원칙(Architecture Principle) 수립, 참조 모델 유지 | TOGAF ADM 8단계(Pre->A->B->C->D->E->F->G->Req Mgmt), 4A 모델(BA·DA·AA·TA), Zachman 6×6 매트릭스, FEAF |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오 관리, 표준/방법론 통제 | PMBOK 7th, PRINCE2, P3O(Portfolio/Programme/Project Office), Earned Value Management(EVM: CPI, SPI) |
| **IT 운영 조직 (IT Operations)** | 서비스 안정적 제공, 장애 예방/대응 | ITIL 4의 34개 Practice, SRE(Site Reliability Engineering), DORA 4대 지표, AIOps |
| **정보보안 조직 (CISO Office)** | 사이버 위협 방어, 컴플라이언스 관리 | Zero Trust Architecture(NIST SP 800-207), ISMS-P, ISO 27001/27701, OWASP Top 10, MITRE ATT&CK |
| **데이터 거버넌스 (CDO Office)** | 데이터 품질, 마스터/메타/레퍼런스 관리 | DAMA-DMBOK 2.0(11 지식영역), DCAM(Data Management Capability Assessment), 데이터 카탈로그, 데이터 메시(Data Mesh) |
| **IT 재무/FinOps** | IT 비용 가시화, 클라우드 비용 최적화 | FinOps Foundation Framework(Inform/Optimize/Operate), Showback/Chargeback, TCO 분석, Unit Economics |
| **변화관리/HR** | 조직 역량 강화, 직무 전환 관리 | ADKAR(Awareness·Desire·Knowledge·Ability·Reinforcement), Kotter 8단계, 컴피턴시 모델(SFIA 8) |

###
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 694 / 800

<- **이전**: [693. IT 경영 관리 핵심 토픽 693번 시험 요약](/studynote/12_it_management/05_security_compliance/693_it_management_core_topic_693_exam_summary/)
**다음**: [695. IT 경영 관리 핵심 토픽 695번 시험 요약](/studynote/12_it_management/05_security_compliance/695_it_management_core_topic_695_exam_summary/) ->

---
