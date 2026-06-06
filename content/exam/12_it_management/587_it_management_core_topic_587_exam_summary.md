---
title: "IT Management Core Topic 587 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리란 COBIT 2019, ISO 38500, ITIL 4 등 거버넌스 프레임워크를 기반으로 **"전략-비즈니스 정렬(Strategy-Alignment) -> 가치 전달(Value Delivery) -> 위험 최적화(Risk Optimization) -> 자원 관리(Resource Management)"** 의 4대 핵심 도메인을 IT 거버넌스 시스템(EGS)과 거버넌스 관리 체계(Governance & Management Objectives, 40개)로 통합 운영하는 활동이다.
> 2. **가치**: 정량적 효과로 EA(Enterprise Architecture) 기반 중복 투자 30~40% 절감, IT 거버넌스 성숙도 1단계 향상 시 프로젝트 성공률 약 25% 증가, 정보시스템 감리 부적정 판정 비율 15% -> 3% 이하 감소를 달성할 수 있으며, 정성적으로는 "디지털 전환(DX) 시대의 의사결정 투명성·이해관계자 신뢰·규제 컴플라이언스" 확보가 가능하다.
> 3. **판단 포인트**: 기술사의 핵심 판단은 **① Cascading Goals(목표 계층화)와 Balanced Scorecard 4관점(재무/고객/내부/학습성장) 간 KPI 정합성, ② Agile + DevOps + Lean Portfolio 간 운영 모드 선택, ③ SaaS·IaaS·PaaS·FaaS 등 클라우드 소비 모델별 TCO 3~5년 분석, ④ Zero Trust·ISO 27001·개인정보보호법·ESG 공시 동시 충족 제어 설계, ⑤ RFP/RFI 단계부터 Value Realization Traceability Matrix(가치 실현 추적표) 적용 여부** 이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI, IoT, 블록체인, 양자컴퓨팅)·플랫폼 경제·원격근무 확대·ESG 공시 의무화(2025년 IFRS S1/S2, 2026년 KCSSB)의 가속화로, 정보시스템은 단순 운영자산에서 **"경영 전략의 핵심 동력(Strategic Driver)"** 으로 격상되었다. 하지만 한국 정보시스템 감리지침(행정안전부 예규 제178호)과 국가정보화백서(NCSI) 통계에 따르면, 공공·금융·제조 분야 IT 프로젝트의 약 38%가 초기 예산 초과, 42%가 비즈니스 목표 미달정, 27%가 운영 1년 내 사용자 저항으로 실패·중단된다. 이는 **"기술 도입 ≠ 가치 실현"** 이라는 고질적 미스매치를 보여주며, 이를 해소하기 위해 IT를 자산·비용이 아닌 **"이해관계자 가치(Stakeholder Value) 창출 체계"** 로 관리하는 IT 경영 관리(Information Technology Management, ITM) 체계가 요구된다.

기존 IT 운영은 ITIL v3의 **26개 프로세스(Service Strategy -> Design -> Transition -> Operation -> CSI)** 중심의 **"프로세스 효율성"** 에 집중했으나, 2018년 ITIL 4 -> 2019년 COBIT 2019 -> 2020년 ISO/IEC 38500 2nd Edition -> 2022년 SAFe 6.0 -> 2024년 COBIT 2019 Design Guide 2nd Edition 으로 진화하며, **"거버넌스-전략-포트폴리오-프로젝트-운영-만족도"** 의 6계층 통합 모델이 표준으로 자리잡았다. 특히 2024년 기준 한국 CIO Survey(조달청·NIA 공동)에 따르면, "DX 예산은 늘었지만 성과 측정이 불명확"하다는 응답이 71.4%로 나타나, **"IT 투자의 정량적 가치 실현(Value Realization) 추적"** 이 가장 시급한 과제로 부상하고 있다.

```text
+------------------------------------------------------------------+
|            IT 경영 관리(Information Technology Management)       |
|            +-----------------------------------------+           |
|            |   전략 정렬(Strategy-Alignment) Layer   |           |
|            |   - Cascading Goals(BSC 4관점 KPI) -    |           |
|            |   - ITBSC(IT Balanced Scorecard) -      |           |
|            |   - ESG·DX 전략 매핑 -                  |           |
|            +------------+----------------------------+           |
|                         v                                        |
|  +----------------------------------------------------------+    |
|  |  거버넌스(Governance) Layer: "Evaluate-Direct-Monitor"   |    |
|  |  - COBIT 2019 EDM 도메인 + 40개 Governance/Management   |    |
|  |    Objectives - ISO/IEC 38500 6원칙 - KR 법·감리 -      |    |
|  +----------------------------------------------------------+    |
|                         |                                        |
|         +---------------+---------------+                        |
|         v               v               v                        |
| +-------------+  +-------------+  +-------------+                |
| |  포트폴리오 |  |   프로젝트  |  |   서비스    |                |
| | (Portfolio) |  |  (Project)  |  |  (Service)  |                |
| | SAFe LPM   |  | PMBOK 7th  |  | ITIL 4 SVS |                |
| | MoP+       |  | PRINCE2    |  | SIAM       |                |
| +-------------+  +-------------+  +-------------+                |
|         |               |               |                        |
|         +---------------+---------------+                        |
|                         v                                        |
|       +------------------------------------+                     |
|       | Value Realization(가치 실현) Loop   |                     |
|       |  Plan->Design->Build->Run->Measure->    |                     |
|       |  Evaluate->Replan (PDCA + Lean)      |                     |
|       +------------------------------------+                     |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **"도시의 종합 도시계획(都市計計)"** 과 같다. 개별 건물(IT 시스템) 하나하나의 건축 허가만 보는 것이 아니라, 교통·상하수도·공원·재난 방재·환경 규제까지 통합적으로 계획·감독하는 도시 행정청의 역할이 바로 IT 거버넌스이다. 빌딩은 아무리 멋져도 도시계획 위반이면 입주할 수 없듯, 시스템은 아무리 기술이 좋아도 거버넌스 미충족이면 가치가 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 근간은 **COBIT 2019 Governance System** 으로, 5대 도메인(EDM, APO, BAI, DSS, MEA) × 40개 관리 목적(Governance Objectives 5 + Management Objectives 35) × 7개 컴포넌트(원리, 정책·프레임워크, 프로세스, 조직구조, 정보, 인력·기술·시설, 문화·행태·윤리) × 3단계 집중(Focus Area × Design Factor × Capability Level)로 구성된다. 핵심 작동 원리는 **"Design Factor(설계 요인) 11개 -> Governance System 40개 Objective 우선순위 도출 -> Capability Level 목표 설정 -> Process Assessment Model(PAM) 기반 갭 분석"** 의 4단계 체계다.

```text
       COBIT 2019 Governance System 구성 (7 Components)
       +--------------------------------------------+
       | 1. Principles, Policies, Frameworks        |  <- ISO 38500
       | 2. Processes                                |
       | 3. Organizational Structures                |
       | 4. Information Flow & Items                 |
       | 5. People, Skills & Competencies             |
       | 6. Services, Infrastructure, Applications   |
       | 7. Culture, Ethics, Behavior                 |
       +--------+-----------------------------------+
                |
                v
   +--------------------------------------------+
   |  5 Domains / 40 Objectives (COBIT 2019)   |
   |  +----------+----------+----------+------+ |
   |  | EDM(5)   | APO(14)  | BAI(11)  |      | |
   |  | Evaluate | Align    | Build    |      | |
   |  | Direct   | Plan     | Acquire  |      | |
   |  | Monitor  | Organize | Implement|      | |
   |  +----------+----------+----------+------+ |
   |  | DSS(6)   | MEA(4)   |          |      | |
   |  | Deliver  | Monitor  |          |      | |
   |  | Service  | Evaluate |          |      | |
   |  | Support  | Assess   |          |      | |
   |  +----------+----------+----------+------+ |
   +--------+-----------------------------------+
            |
            v
   +--------------------------------------------+
   |  Cascading Goals(목표 계층화) -> BSC 4관점  |
   |  +---------+ -> +---------+ -> +---------+  |
   |  | 재무    |   | 고객    |   | 내부    |  |
   |  | (FCF)   |   | (NPS)   |   | (KPI)   |  |
   |  |  ROI    |   |  TTF    |   | SLA     |  |
   |  +---------+   +---------+   +---------+  |
   |                  ^                         |
   |              학습·성장(L&D, 문화)          |
   +--------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate·Direct·Monitor)** | 이사회·IT전략위원회(IISSC, 정보화진흥심의위원회) 차원의 의사결정·감독 | COBIT 2019 EDM01~05(거버넌스 체계 설정/이해관계자 참여/리스크 최적화/자원 최적화/투명성 확보). ISO/IEC 38500 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)과 1:1 매핑 |
| **APO (Align·Plan·Organize)** | 전략->포트폴리오->아키텍처->자원->위험 정렬 | APO01~14: 전략 매니페스토(Strategic Map + ITBSC) -> 가치 실현 마일스톤(VRM) -> EA(ArchiMate 3.2 TOGAF 10 ADM) -> I&T 스킬 매트릭스(SFIA 8) -> 위험 카탈로그(Risk Catalog, ISO 31000 기반) |
| **BAI (Build·Acquire·Implement)** | 솔루션 수명주기(SDLC) 및 변경 통제 | BAI01~11: PMBOK 7th 12원칙, PRINCE2 7원칙, SAFe 6.0 ART(Agile Release Train), CI/CD 파이프라인(ArgoCD+Tekton), IaC(Terraform+Ansible), DevSecOps(SCA+SAST+DAST+SBOM+Sigstore) |
| **DSS (Deliver·Service·Support)** | 서비스 운영·장애·연속성·보안 | DSS01~06: ITIL 4 34 Practices, AIOps(Aria/PagerDuty ML), Observability 3요소(Metrics·Logs·Traces, OpenTelemetry), SRE(SLI/SLO/Error Budget), BCM(ISO 22301 RTO/RPO), Zero Trust Architecture(NIST SP 800-207) |
| **MEA (Monitor·Evaluate·Assess)** | 성과 측정·컴플라이언스·내부 통제 평가 | MEA01~04: BSC 4관점 KPI, VRTM(Value Realization Traceability Matrix), 감리지침(행정안전부 예규 178호) 기반 PMO 감리, ISAE 3402 / SOC 2 Type II, ISO 37301(컴플라이언스 경영) |

**핵심 알고리즘 및 산식**:
- **가치 실현률(VRO, Value Realization Ratio)** = (실제 창출效益) ÷ (계획效益) × 100. PMO는 분기별 VRO ≥ 85% 미달 시 **Strategic Drift(전략 표류)** 경보 발령.
- **TCO 5년 분석**: TCO = CapEx + Σ(연간 OpEx) − Σ(연간 Benefit) + Risk-Adjusted Cost(확률×영향). 클라우드 소비 모델별(IaaS/PaaS/SaaS/FaaS) 단위 비교 필수.
- **거버니스 성숙도**: ISO/IEC 33020 PAM 등급(0~5) 또는 CMMI-DEV/SVC/SAM 5단阶梯. 공공부문은 "정보시스템 감리" + "지자체 정보화 성숙도 진단" 의무화.
- **이해관계자 파워-관심 매트릭스(Mendelow Matrix)** + RACI 매트릭스 -> 40개 Objective 별 의사결정 권한 분배.
- **위험 정량화(FAIR, Factor Analysis of Information Risk)**: ALE(연간손실기대치) = ARO(연간발생률) × SLE(단위손실). 위험 허용 기준(예: ALE < 매출 0.5%) 수립.

- **📢 섹션 요약 비유**: COBIT 2019는 **"비행기의 자동조종 시스템(Autopilot) + 블랙박스 + 조종사 매뉴얼 + 관제탑 교신"** 이 통합된 것이다. EDM은 관제탑(ATC), APO는 비행계획·연료계산, BAI는 기체 제작·시운전, DSS는 실제 운항·정비, MEA는 블랙박스 분석·안전 심사이다. 7개 컴포넌트는 조종사·센서·유압장치 등 7계층이 모두 정상이어야 비행이 안전하듯, 어느 하나라도 결손 시 거버넌스 붕괴로 직결된다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역은 다수의 글로벌 프레임워크가 공존하며, 각각의 적용 범위·관점·성숙도가 다르다. 기술사 시험에서 빈번하게 출제되는 **"프레임워크 간 정합성·충돌·통합"** 을 명확히 이해해야 한다.

| 구분 | COBIT 2019 | ITIL 4 | ISO/IEC 38500 | PMBOK 7th | SAFe 6.0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 관점** | 거버넌스 통합 프레임워크 | 서비스 운영·만족도 | IT 의사결정 6원칙 | 프로젝트·프로그래임 관리 | 대규모 Agile 포트폴리오 |
| **구조** | 5 Domain × 40 Obj × 7 Component | 34 Practice × SVS(Value Chain)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 587 / 800

<- **이전**: [586. IT 경영 관리 핵심 토픽 586번 시험 요약](/studynote/12_it_management/05_security_compliance/586_it_management_core_topic_586_exam_summary/)
**다음**: [588. IT 경영 관리 핵심 토픽 588번 시험 요약](/studynote/12_it_management/05_security_compliance/588_it_management_core_topic_588_exam_summary/) ->

---
