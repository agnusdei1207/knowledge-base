---
title: "IT Management Core Topic 487 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디지털 전환(Digital Transformation, DX)은 단순히 레거시 시스템을 클라우드로 이전하는 것이 아니라, **기술(Technology)·데이터(Data)·프로세스(Process)·사람(People)·전략(Strategy)**의 5개 레이어를 동시에 재설계하여 비즈니스 모델 자체를 근본적으로 혁신하는 **경영 패러다임 전환**이다. 핵심 프레임워크로는 **COBIT 2019, ITIL 4, ISO/IEC 38500, McKinsey 5 Quintessence, BCG Digital Acceleration Index**가 있으며, 이를 **IT 거버넌스 위원회(Steering Committee) -> PMO -> CoE(Center of Excellence) -> Biz Squad**의 4계층 거버넌스 구조로 실행한다.
> 2. **가치**: McKinsey Global Survey(2023)에 따르면 DX 성공 기업은 동일 업종 대비 **매출 성장률 2.5배, EBITDA 마진 1.8배, 시가총액 성장률 1.7배**, BCG 기준 **"Digital Liner" 기업은 후발주자 대비 3년간 ROE 8.4%p 우위**. Gartner(2024) 예측으로는 2026년 글로벌 DX 지출 **3.4조 USD**, AI 기반 의사결정 자동화 도입률 65% 도달.
> 3. **판단 포인트**: 핵심 의사결정 축은 ① **Cloud-First vs On-Premise 우선** (TCO 5년 비교, 규제 준수), ② **중앙집중형 CoE vs 분산형 페데럴(Federated) 거버넌스**, ③ **Big-Bang(3~6개월 전사 일괄) vs Phased(도메인별 단계적) vs Parallel(Strangler Fig Pattern 18~36개월)** 전환 전략, ④ **Build vs Buy vs Compose vs Rent(API Marketplace)** ⑤ **데이터 주권·규제 준수** (GDPR, PIPC, 데이터3법) 등이며, 기술사 답안에는 **정량적 ROI/NPV/IRR 분석 + 정성적 전략 적합성**을 반드시 병기해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경 및 환경 변화

**4차 산업혁명·Post-Pandemic·AI 대폭발의 3대 외부 충격**이 동시다발적으로 발생하면서, IT는 **"Back-Office 비용 센터"**에서 **"Front-Office 가치 창출 엔진"**으로 역할이 전환되었다. 고객 접점이 모바일·SNS·메타버스 등 디지털 채널로 80% 이상 이동함에 따라, 종이·창구 기반의 전통적 비즈니스 프로세스는 구조적 한계에 도달했다.

**핵심 Pain Point:**
- **레거시 기술 부채(Technical Debt)**: 평균 30년 이상 된 COBOL/PL/I 메인프레임, SAP R/3(2004), Oracle 11g(2007) 등 EOSL(End of Support Life) 도래로 **연간 유지보수 비용 60~70%**, 신규 기능 출시 속도(MTTR: Mean Time To Release) 6개월 이상
- **데이터 사일로(Silo)**: 부서·시스템별 스키마 불일치로 통합 CRM 360+ 뷰 부재, MDM(Master Data Management) 부재
- **Time-to-Market 저하**: 6개월 waterfall 기반 SI 구조로는 시장 변화 대응 불가
- **인재 갭**: 전사 직원 중 디지털 역량(Digital Quotient) 보유 비율 12% 수준(McKinsey, 2023)
- **규제 복잡화**: 데이터3법(2022.3. 시행), EU AI Act(2024), PIPC 가이드라인 강화

### 1.2 패러다임 비교: 전통 IT vs DX-Driven IT

| 차원 | 전통 IT(Waterfall SI) | DX-Driven IT(Agile Platform) |
|:---|:---|:---|
| 목적 | 업무 자동화(Cost Center) | 비즈니스 모델 혁신(Value Driver) |
| 구조 | Monolith(단일 시스템) | Microservice + API Gateway |
| 데이터 | RDB 트랜잭션 중심 | Data Lake + Lakehouse(Delta Lake) |
| 배포 | 6개월~2년 Big-Bang | 2주 Sprint + CI/CD |
| 예산 | Capex 일시 집중 | Opex Pay-as-you-go + FinOps |
| 지표 | 정시 납기, 예산 준수 | NPS, DAU/MAU, Feature Adoption Rate |
| 조직 | 기능별 버퍼(개발/운영/품질) | Cross-functional Squad(피자팀) |
| 거버넌스 | 프로젝트 단위 임시조직 | 지속적 CoE + 전사 데이터 거버넌스 |

### 1.3 ASCII 다이어그램: DX 거버넌스 의사결정 구조

```text
        +-----------------------------------------------+
        |       Board of Directors / 이사회               |
        |   (디지털 전략위원회 - 분기 1회, CEO 직접 주관)  |
        +----------------------+------------------------+
                               | 정략 방향 / 예산 승인
                               v
        +-----------------------------------------------+
        |        IT Steering Committee / 전사 DX 회의체  |
        |  (CDO·CTO·CIO·CMO·CFO·CHRO, 월 1회, 12인 이내) |
        +----------------------+------------------------+
                               | 우선순위·포트폴리오 결정
            +------------------+------------------+
            v                  v                  v
    +--------------+   +--------------+   +--------------+
    |  Domain A    |   |  Domain B    |   |  Domain C    |
    | (제조 DX)    |   | (마케팅 DX)  |   | (HR DX)      |
    | - Squad 1,2  |   | - Squad 3,4  |   | - Squad 5    |
    | - Product    |   | - Product    |   | - Product    |
    |   Owner(PO)  |   |   Owner      |   |   Owner      |
    | - Scrum Mast |   | - Scrum Mast |   | - Scrum Mast |
    +------+-------+   +------+-------+   +------+-------+
           |                  |                  |
           +------------------+------------------+
                              v
        +-----------------------------------------------+
        |   CoE (Center of Excellence) / 플랫폼·표준    |
        |  - Cloud Platform Team (EKS/AKS/GKE)         |
        |  - Data Platform Team (Lakehouse + ML Ops)   |
        |  - DevX Team (CI/CD, IaC, Observability)     |
        |  - Security & Compliance (Zero-Trust)        |
        |  - AI/ML Engineering (Feature Store, LLM Ops)|
        +----------------------+------------------------+
                               | 플랫폼·표준·공용 컴포넌트
                               v
        +-----------------------------------------------+
        |   PMO / Portfolio Management Office          |
        |   - 40+ Use Case 우선순위화(RICE/WSJF)         |
        |   - Epic 단위 Value Stream Mapping            |
        |   - OKR/KPI 대시보드(예산 30% / 가치 70%)      |
        +-----------------------------------------------+
```

### 1.4 📢 섹션 요약 비유

> **DX는 "회사 전체의 OS 업그레이드"**입니다. 단순히 PC(부서 시스템)만 바꾸는 것이 아니라, 회사 전체의 운영체제(비즈니스 모델·조직 문화·인재 시스템)를 **Windows 95 -> Cloud Native OS**로 교체하는 작업이라, **PC 본체(기술)만 사서 끼워서는 작동하지 않고, 드라이버(거버넌스), 데이터 마이그레이션(데이터), 사용자 교육(사람의 역량)**, 이 4박자가 모두 갖춰져야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 DX 5-Layer Reference Architecture

DX는 단일 기술이 아니라 **5개 상호의존 레이어**의 통합 설계가 핵심이다. 각 레이어별로 **상세한 아키텍처 패턴과 적용 기술**을 도출해야 기술사 답안에서 **실무 적용 가능성**을 인정받는다.

```text
   +------------------------------------------------------+
   |  Layer 5: Experience Layer (CX/UX)                   |
   |  - Web/Mobile App, Omnichannel, Conversational UI    |
   |  - Adobe Experience Cloud, Salesforce Marketing Cloud |
   |  - LLM-based Chatbot(OpenAI GPT-4o, Claude 3.5)      |
   +------------------------------------------------------+
   |  Layer 4: Engagement & Intelligence Layer            |
   |  - Real-time CDP(Customer Data Platform)              |
   |  - Recommendation Engine, Real-time Bidding          |
   |  - AI/ML Serving: MLflow + KServe + Feature Store    |
   +------------------------------------------------------+
   |  Layer 3: Process & Integration Layer                |
   |  - Microservice (Spring Boot, Node.js, Go
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 487 / 800

<- **이전**: [486. IT 경영 관리 핵심 토픽 486번 시험 요약](/studynote/12_it_management/05_security_compliance/486_it_management_core_topic_486_exam_summary/)
**다음**: [488. IT 경영 관리 핵심 토픽 488번 시험 요약](/studynote/12_it_management/05_security_compliance/488_it_management_core_topic_488_exam_summary/) ->

---
