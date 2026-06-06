---
title: "FEAF Federal EA Framework"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

# 504. FEAF 연방 EA 프레임워크 (FEAF Federal EA Framework)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 미국 OMB(Office of Management and Budget)와 Federal CIO Council이 운용하는 정부 전사적 아키텍처 프레임워크로, 6개의 Consolidated Reference Model(PRM/BRM/SRM/DRM/TRM/SsRM)을 통해 연방정부의 전략·업무·데이터·응용·기술·보안 도메인을 통합·표준화한다.
> 2. **가치**: 연방정부 연간 약 80억 달러 이상의 IT 예산에서 중복 투자(redundant investment)를 제거하고, 부처 간 상호운용성(Federal Interoperability)을 확보하며, CPIC(Capital Planning and Investment Control)와 연계해 사업 정당성을 EA 기반으로 검증하여 ROI를 정량화한다.
> 3. **판단 포인트**: 조직 전체 EA가 아닌 **Segment Architecture**(특정 업무/서비스 영역 단위)로 전환하여 실용성을 높였고, 2020년 이후에는 **GEAR(Government-wide Enterprise Architecture Reference)**로 진화하며 EA와 예산·성과관리의 결합을 강화하고 있다. 도입 시 자방식(自方式) EA가 되지 않도록 OMB EA Assessment Framework 기반의 **EA-3(통합 EA)** 등급 이상을 확보해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 법적·정책적 배경
FEAF는 단순한 모델이 아니라 미국 연방법의 직접적인 산물이다. 핵심 법적 근거는 다음과 같다.

| 법률/정책 | 발효연도 | 핵심 조항 | FEAF 연관성 |
| :--- | :--- | :--- | :--- |
| **Clinger-Cohen Act**(IT Management Reform Act) | 1996 | CIO 제도, IT 투자 성과관리, EA 수립 의무 | FEAF 1.0 직접 근거 |
| **E-Government Act** | 2002 | Section 207: Federal Enterprise Architecture 확립 | OMB가 FEA 개발·유지 의무 |
| **OMB Circular A-130**(Managing Information as a Strategic Resource) | 2016 개정 | 연방 정보/정보시스템 관리 통합 정책 | EA·사이버보안·프라이버시 통합 |
| **OMB Circular A-11**(Planning, Programming, Budgeting) | 매년 갱신 | Capital Planning Exhibit 300/53(현 51) | EA -> 예산 연계 |
| **Federal Information Security Modernization Act(FISMA)** | 2014 | 지속적 진단·완화(CDM) | SsRM(보안 참조모델) 직접 연결 |
| **FITARA**(Federal IT Acquisition Reform Act) | 2014 | CIO 권한 강화, 데이터센터 통합 | EA + PortfolioStat 연계 |

### 1.2 등장 배경: Stovepipe System 문제
1990년대 미국 연방정부는 **"Stovepipe"**(굴뚝식) 시스템에 시달렸다. 부처별로 동일 기능을 독립 구축하여, 다음 문제가 대두되었다.

- **투자 중복**: SSA(사회보장국) 26개국 적십자사와 같은 부처 차원의 시스템 중복 구축
- **상호운용성 부재**: 발주처별 상이한 데이터 표준(X12 EDI, HL7, NIEM 비준수)
- **보안 사각지대**: 부처별 개별 인증·접근제어 -> FISMA Score 급락
- **시민 서비스 파편화**: IRS, SSA, USCIS 등 1회 클릭으로 완료되지 않는 정부 서비스

```text
[1990s 연방정부 IT 조달의 현실: 24개 부처의 수평적 중복]
=====================================================================
   부처 A  --+                                 +-- 부처 X (재무)
   부처 B  --+                                 +-- 부처 Y (국토안보)
   부처 C  --+   "동일 HR 시스템" 24회 별도 구축 +-- 부처 Z (농업)
   부처 D  --+   "동일 재무 시스템" 22회 별도구축+-- 부처 W (에너지)
   ...     --+   "동일 ERP" 19회 별도구축       +-- 부처 V (보훈)
   부처 N  --+                                 +-- ... (총 24개 CFO Act 부처)
=====================================================================
                              |
                              v  Clinger-Cohen Act (1996) & E-Gov Act (2002)
                              |
                              v
              +-------------------------------+
              |   Federal Enterprise         |
              |   Architecture (FEA)         | ---> 단일 참조모델
              |   + FEAF                     |     표준화·재사용
              |   + CPIC 연계                |
              +-------------------------------+
                              |
                              v
        6대 Reference Model (PRM/BRM/SRM/DRM/TRM/SsRM)
        + Segment Architecture
        + FSAM (Federal Segment Architecture Methodology)
```

### 1.3 연방 EA 진화 타임라인

| 연도 | 마일스톤 | 핵심 변화 |
| :--- | :--- | :--- |
| 1996 | Clinger-Cohen Act 제정 | EA 수립 법적 의무화 |
| 1999 | **FEAF v1.0** 발표 | Zachman 6x6 매트릭스 기반, 연방 부처 EA 표준 |
| 2002 | E-Government Act / FEA 1세대 | 4대 Reference Model(BRM/DRM/TRM/PRM) |
| 2005 | **FEA Consolidated Reference Model (CRM)** | SRM 추가, 5대 모델 통합 |
| 2006 | **FEA-Security Profile** | 보안 도메인 본격 반영 |
| 2007 | **FSAM v1.0** | Segment Architecture 방법론 |
| 2012 | **FEAF v2.0** | 6대 CRM 정착, EA-3 통합 모델 |
| 2013 | **Federal EA Assessment Framework v3.0** | EA 성숙도 측정 |
| 2019 | **GEAR(Government-wide Enterprise Architecture Reference)** | 부처 EA -> 정부 전체 EA 전환 |
| 2022 | **FIBF(Federal Integrated Business Framework)** | 비즈니스 우선, 약 200개 표준화 비즈니스 스킬 |
| 2024~ | **AI-Augmented EA** | LLM 기반 모델링·검증 자동화 |

### 1.4 왜 여전히 중요한가 (2026년 관점)
- **M-25-25(2025 OMB M-메모)**: AI·클라우드 도입 시 EA 검증 의무
- **CISO의 EA 연계 의무**: Zero Trust Architecture를 FEAF SsRM에 매핑
- **Bipartisan 정책 합의**: 공화·민주 양당 모두 정부 IT 현대화에 EA를 핵심 수단으로 채택

### 📢 섹션 요약 비유
FEAF는 **"연방정부라는 거대 아파트 단지(24개 부처)의 통합 건축법규"**다. 각 동(부처)이 따로 짓다가 같은 단열재를 24번 사게 되자, 건축법규로 **"단열재 표준·전기 배선 표준·소방 표준"**을 통합해 한 번 사서 24개 동에 적용하게 만든 것이다. 6대 참조모델이 바로 그 6개 분야의 표준 규격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 FEAF v2.0의 전체 아키텍처: 6대 Consolidated Reference Model

```text
[FEAF v2.0 계층 구조 - 상위에서 하위로 매핑되는 Z축 정합성]
========================================================================
                                 ^
                                 |  연계·정합(Alignment)
                                 |
  +--------------------------------------------------------------+
  | PRM  Performance Reference Model      (성과참조모델)         |
  |   - 4 Measurement Areas: Customer, Process, Workforce, Tech |
  |   - 전략 목표 -> KPI -> 측정치의 인과체계                      |
  |   - 주요 활용: IT 사업 성과 평가, Showback/Chargeback       |
  +--------------------------------------------------------------+
                       |  "어떤 성과를 내려는가?"
                       v
  +--------------------------------------------------------------+
  | BRM  Business Reference Model         (업무참조모델)         |
  |   - 4 Levels: Mission Area -> LoB -> Sub-Function -> Service  |
  |   - 39개 LoB, 230+ Sub-Function                            |
  |   - 부처·에이전시 간 동일 LoB 식별 -> 공유서비스 후보 도출  |
  +--------------------------------------------------------------+
                       |  "어떤 업무를 수행하는가?"
                       v
  +--------------------------------------------------------------+
  | DRM  Data Reference Model             (데이터참조모델)       |
  |   - 3 Layers: Strategic(Context) -> Tactical -> Operational  |
  |   - 데이터 공유, 마스터 데이터, 메타데이터 표준화            |
  |   - NIEM(National Information Exchange Model) 연계         |
  +--------------------------------------------------------------+
                       |  "어떤 정보를 다루는가?"
                       v
  +--------------------------------------------------------------+
  | SRM  Service Component Reference Model (서비스구성참조모델) |
  |   - 4 Columns: Service Domain -> Service Type -> Component   |
  |               -> Investment                                  |
  |   - 서비스 재사용 카탈로그(부처간 공유 비즈니스 서비스)     |
  |   - USAspending.gov / Code.gov 연계                         |
  +--------------------------------------------------------------+
                       |  "어떤 서비스로 구현하는가?"
                       v
  +--------------------------------------------------------------+
  | TRM  Technical Reference Model         (기술참조모델)        |
  |   - 4 Layers: Service Access -> Platform -> Component -> HW   |
  |   - 클라우드·미들웨어·OS·서버·네트워크 표준                |
  |   - FedRAMP 인증 제품·서비스 자동 매핑                      |
  +--------------------------------------------------------------+
                       |  "어떤 기술 위에 구현하는가?"
                       v
  +--------------------------------------------------------------+
  | SsRM Security & Privacy Reference Model(보안참조모델)       |
  |   - 4 Columns: Control -> Family -> Class -> Component        |
  |   - NIST SP 800-53 Rev.5 컨트롤과 1:1 매핑                |
  |   - ZTA(Zero Trust Architecture)·CUI·PII 정책 통합          |
  +--------------------------------------------------------------+
                                 ^
                                 |  보안은 모든 계층에 횡단(Cross-cutting)
                                 |
========================================================================
```

### 2.2 6대 참조모델 상세 사양

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **PRM (성과참조모델)** | IT 투자와 사업성과의 인과관계 정량화 | 4개 Measurement Area(Customer Satisfaction, Processes and Activities, Workforce, Technology) — 각 영역별 measurement category -> measurement indicator -> 측정값. 예: "사이버 공격 대응 평균시간(MTTC)" -> LoB "Cybersecurity" -> BRM과 매핑 |
| **BRM (업무참조모델)** | 정부 전체 업무 분류의 표준 어휘(vocabulary) | Mission Area(4개: Service for Citizens / Mode of Delivery / Support Delivery of Services / Internal Management) -> LoB(39개) -> Sub-Function(230+) -> Service. 부처별 LoB 점유율로 중복·누락 식별 |
| **DRM (데이터참조모델)** | 부처 간 데이터 공유·상호운용성 확보 | 3개 계층: Strategic Context(목적·의미), Tactical Information(데이터 도메인·엔터티), Operational Information(속성·메타데이터). NIEM, GISA(Government Information Sharing Architecture) 연계 |
| **SRM (서비스구성참조모델)** | 재사용 가능한 응용 서비스 카탈로그 | 4개 컬럼: Service Domain(7개: Customer Services
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 504 / 600

<- **이전**: [503. Zachman 프레임워크 분류 체계](/studynote/11_design_supervision/06_exam_summary/503_zachman_framework_classification)
**다음**: [505. COBIT 거버넌스 관리 프레임워크](/studynote/11_design_supervision/06_exam_summary/505_cobit_governance_management_framework/) ->

---
