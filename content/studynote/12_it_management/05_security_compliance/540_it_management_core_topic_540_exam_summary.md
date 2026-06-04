+++
title = "540. IT 경영 관리 핵심 토픽 540번 시험 요약 (IT Management Core Topic 540 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 📚 기술사 시험 대비 스터디 노트

## 주제: 540. IT 거버넌스 및 경영관리 (IT Governance & Management)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 ISO 38500, COBIT 2019, ITIL 4 프레임워크를 기반으로 **"Evaluate-Direct-Monitor"** 3대 원칙 하에 IT 투자 의사결정(ROI/NPV/IRR), 위험 통제, 자원 배분을 경영진 책임(Eduard, 책임 구조)으로 수행하는 **제어(Control) 시스템**이다.
> 2. **가치**: McKinsey 보고에 따르면成熟的 IT 거버넌스 도입 조직은 IT 투자 대비 ROI **20~35% 향상**, 프로젝트 실패율 **40% 감소**(Standish Group 2023), 의사결정 리드타임 **60% 단축**, 컴플라이언스 위반 비용 **연간 2.7M USD 절감**(Ponemon Institute 2024)을 달성한다.
> 3. **판단 포인트**: 중앙집권형(COBIT Centered) vs 분산자율형(Federated) 거버넌스 모델 선택, **RACI 매트릭스** 상의 이해관계자 책임 소재, EA(엔터프라이즈 아키텍처)와 BSC-IT의 **전략-전술-운영 정렬(Strategy-Tactics-Operation Alignment)**, 그리고 **Two-speed IT**(Mode 1 안정성 vs Mode 2敏捷) 간의 균형점이 핵심 설계 변수다.

---

## Ⅰ. 개요 및 필요성

정보기술의 전략적 비중이 급증함에 따라 단순 비용센터(Cost Center)였던 IT 조직이 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 전환되었다. 그러나 다수의 한국 기업들은 IDC Korea(2024) 조사에서 IT 예산의 **37%가 비전략적 중복 투자**에 소진되고, CIO와 CEO 간의 IT 가치 인식 괴리가 **72% 수준**에 달하는 것으로 나타났다. 이는 **"IT-Business Alignment Gap"**이라는 고전적 문제가 해결되지 않고 있음을 의미하며, 이를 극복하기 위한 **IT 거버넌스 체제**의 정비가 필수적이다.

```text
+-----------------------------------------------------------------+
|              IT 거버넌스 패러다임 전환 (As-Is -> To-Be)            |
+-----------------------------------------------------------------+
|                                                                   |
|   [As-Is: 1990s~2000s]              [To-Be: 2020s~]              |
|   +-----------------+               +-----------------+         |
|   |  IT = Cost Center|   -------►    |IT=Value Center  |         |
|   |  CIO = 후방위   |  디지털전환    |CIO=전략파트너   |         |
|   |  Shadow IT 만연 |   가속화       |Federated Gov.   |         |
|   |  ROI 미측정     |               |Value-driven KPI |         |
|   +-----------------+               +-----------------+         |
|         |                                  |                     |
|         v                                  v                     |
|   +-----------------+               +-----------------+         |
|   |컴플라이언스 중심 |               | 리스크 기반      |         |
|   |통제 우선(Control)|  ------►      | 가치 우선(Value) |         |
|   |사일로형 부서     |               |DevSecOps+AI 거버 |         |
|   +-----------------+               +-----------------+         |
|                                                                   |
|  ※ 드라이버: COVID-19, ESG, 생성형AI, 클라우드, 규제강화         |
+-----------------------------------------------------------------+
```

기존 IT 관리(Traditional IT Management)는 ITIL 기반의 **운영 효율성**에 집중했으나, 현대의 IT 거버넌스는 COSO ERM 2017, ISO 38500:2015, COBIT 2019가 통합한 **3-Layer Governance Model**(전략 거버넌스, 가치 거버넌스, 위험 거버넌스)을 요구한다. 특히 2023년 SEC 사이버 디스클로저 규칙(cybersecurity disclosure rule) 및 EU DORA(2025.01 시행)에 따라 **보안 거버넌스**가 IT 거버넌스의 핵심 서브셋으로 부상했다.

- **📢 섹션 요약 비유**: IT 거버넌스는 **"배의 키잡이(Rudder)"**와 같다. 엔진(IT 인프라)이 아무리 강력해도, 키(거버넌스)가 없으면 배는 방향 없이 표류한다. 항해의 책임은 선장(CEO)에게 있지만, 키의 설계와 작동은 키잡이(CIO+이사회)에게 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 ISO 38500 기반 3대 원칙 (Evaluate-Direct-Monitor)

ISO/IEC 38500:2015는 IT 거버넌스의 **6대 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**을 3대 거버넌스 태스크(평가-지시-모니터링)로 매핑한다.

```text
+----------------------------------------------------------------------+
|        ISO 38500 IT 거버넌스 참조모델 (Reference Model)               |
+----------------------------------------------------------------------+
|                                                                        |
|  +----------------------------------------------------+              |
|  |       이사회 (Board of Directors)                   |              |
|  |   +----------------------------------+             |              |
|  |   | 거버넌스 3대 태스크              |             |              |
|  |   | ① Evaluate (평가)               |             |              |
|  |   | ② Direct   (지시)               |             |              |
|  |   | ③ Monitor  (모니터)             |             |              |
|  |   +----------+-----------------------+             |              |
|  +--------------+--------------------------------------+              |
|                 |                                                        |
|        +--------v---------+                                            |
|        |   경영진/이사회   |                                            |
|        |   거버넌스 위원회 |                                            |
|        +--------+---------+                                            |
|                 |                                                        |
|      +----------+----------+-------------+                            |
|      v          v          v             v                            |
|  +------+  +------+  +----------+  +----------+                      |
|  |전략  |  |가치  |  | 위험     |  | 컴플라이 |                      |
|  |거버  |  |거버  |  | 거버     |  | 언스     |                      |
|  |넌스  |  |넌스  |  | 넌스     |  | 거버넌스 |                      |
|  +--+---+  +--+---+  +----+-----+  +----+-----+                      |
|     |         |           |             |                             |
|     +---------+-----------+-------------+                             |
|                       |                                                |
|              +--------v---------+                                     |
|              |   COBIT 2019     |                                     |
|              |   (40 Governance  |                                    |
|              |   & Mgmt Objectives)                                    |
|              +--------+---------+                                     |
|                       |                                                |
|      +----------------+----------------+                              |
|      v                v                v                              |
|  +--------+      +--------+       +--------+                         |
|  |전략계층|      |전술계층|       |운영계층|                         |
|  |Portfolio|     |Program |       |Project |                        |
|  |Mgmt    |      |Mgmt    |       |Mgmt    |                        |
|  |(BSC-IT)|      |(PMS)   |       |(Agile) |                        |
|  +--------+      +--------+       +--------+                         |
+----------------------------------------------------------------------+
```

### 2.2 핵심 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/IT 전략위원회** | 거버넌스 최종 의사결정 | RACI 매트릭스(Responsible, Accountable, Consulted, Informed) 기반 의사결정 권한 부여, 분기별 IT 성과 리뷰(QBR) |
| **COBIT 2019** | 거버넌스/관리 목표 프레임워크 | 5개 도메인(EDM: Evaluate-Direct-Monitor, APO: Align-Plan-Organize, BAI: Build-Acquire-Implement, DSS: Deliver-Service-Support, MEA: Monitor-Evaluate-Assess)의 **40개 관리 목표(Management Objective)**와 7개 컴포넌트(Skills, Process, Org structure, Info, Service, People, Goals) 매핑 |
| **IT 전략계획(ISP)** | 중장기 IT 로드맵 수립 | TOGAF ADM(Architecture Development Method) Phase A~F, BSC-IT 4관점(재무, 고객, 내부프로세스, 학습/성장) KPI 연동 |
| **IT 포트폴리오 관리(ITPM)** | 투자 우선순위 결정 | NPV(순현재가치), IRR(내부수익률), Payback Period, **TCO(Total Cost of Ownership)** 5개년 분석, Real Options Valuation |
| **EA(엔터프라이즈 아키텍처)** | IT 자산/서비스 통합 거버넌스 | TOGAF, FEAF, Zachman Framework 기반 **4A 아키텍처**(BA: Business, DA: Data, AA: Application, TA: Technology) 정렬 |
| **위험/컴플라이언스 관리** | IT 리스크 통제 | ISO 27001(ISMS), ISO 31000, NIST CSF 2.0(2024), **Three Lines of Defense Model**(운영리스크, 독립리스크, 내부감사) |

### 2.3 COBIT 2019 핵심 메커니즘

COBIT 2019는 **Cascade of Goals**(목표 연쇄) 메커니즘을 통해 **Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Objectives -> Components**로 목표를 연쇄 정렬한다. 각 단계는 **CMMI(0~5) 기반 Process Capability** 측정과 연계된다.

```text
  +--------------------------------------------------------------+
  |  COBIT 2019 Cascade of Goals 정렬 예시                       |
  +--------------------------------------------------------------+
  |  Stakeholder Need: "IT 위험 감소 및 경쟁력 강화"              |
  |            |                                                  |
  |            v  (Mapping)                                       |
  |  Enterprise Goal: EG03 "위험 최적화" (Risk Optimization)     |
  |            |                                                  |
  |            v  (Mapping)                                       |
  |  Alignment Goal: AG12 "위험 관리"                             |
  |            |                                                  |
  |            v  (Mapping)                                       |
  |  Management Objectives:                                       |
  |    • EDM03 "위험 관리 보장"                                   |
  |    • APO12 "위험 관리"                                        |
  |    • MEA03 "컴플라이언스 관리"                                 |
  |            |                                                  |
  |            v  (Capability)                                    |
  |  Components: Process(APO12.03) + People(CISO) +              |
  |              Technology(GRC Platform) + Info(Risk Register)    |
  +--------------------------------------------------------------+
```

**핵심 정량 파라미터**:

- **CMMI Level 3** 도달 시 프로젝트 성공률 약 **65% -> 80%** (ISACA 2023 통계)
- **거버넌스 성숙도 1단계 상승** 시 IT 운영 비용 약 **12~18% 절감** (Gartner 2024)
- **EA 정합도(Architecture Compliance)** 100% 시 Shadow IT 비중 **45% -> 15%** 감소 (Forrester)
- **NIST CSF Function 점수 1점 상승** 시 침해사고 대응시간(MTTR) **약 30% 단축**

- **📢 섹션 요약 비유**: COBIT의 5개 도메인은 **"자동차의 5대 시스템"**과 같다. EDM(엔진/동력), APO(변속기/기획), BAI(섀시/구축), DSS(휠/서비스 전달), MEA(계기판/모니터링). 이 5개가 맞물려 돌아가야 자동차(기업 IT)가 목적지(전략 목표)에 도달한다.

---

## Ⅲ. 비교 및 연결

### 3.1 주요 IT 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI for Services** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스+관리 통합 | IT 서비스 운영 관리 | 이사회 수준 거버넌스 원칙 | 프로세스 성숙도 평가 |
| **관리 계층** | 전략+전술+운영 (전계층) | 주로 운영(SVS) | 전략(이사회) | 전계층 |
| **프레임워크 구조** | 5도메인/40관리목표 | 34 Practices / SVS
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 540 / 800

<- **이전**: [539. IT 경영 관리 핵심 토픽 539번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/539_it_management_core_topic_539_exam_summary/)
**다음**: [541. IT 경영 관리 핵심 토픽 541번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/541_it_management_core_topic_541_exam_summary/) ->

---
