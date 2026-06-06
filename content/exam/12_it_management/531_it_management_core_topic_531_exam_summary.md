---
title: "IT Management Core Topic 531 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 40개 거버넌스/관리 목적(Governance & Management Objectives)을 기반으로, **EDM(평가·지시·모니터링) -> APO(정렬·계획·조직) -> BAI(구축·구매·이행) -> DSS(전달·지원·운영) -> MEA(모니터링·평가·검토)** 의 5단계 참조 모델을 통해 **Plan-Do-Check-Act(PDCA)** 사이클을 자동화·표준화하여 정보기술과 비즈니스 전략을 결합하는 통합 통제 체계이다.
> 2. **가치**: COBIT·ITIL·ISO/IEC 27001·ISO/IEC 20000·PMBOK·TOGAF 6대 프레임워크를 통합 적용 시 **IT 투자 대비 ROI 25~40% 향상**, **규제 준수 감사 비용 60% 절감**, **인시던트 MTTR 73% 단축**(AXELOS 2022 기준), **ISO 38500 준수율 95% 이상 달성**이 가능하며, ITIL 4 Service Value Chain(SVC)은 34개 실무 활동을 통해 종단간(End-to-End) 가치 흐름을 제공한다.
> 3. **판단 포인트**: 거버넌스 체계 도입 시 **① RACI 매트릭스 정의(Responsible/Accountable/Consulted/Informed)**, **② 설계 요인(Design Factors) 11개 항목**—예산, 위험 허용도, 규제 환경, 기술 채택—을 조직 맥락에 맞게 가중치 설정, **③ 사이버보안 PDCA와 ISMS-P 인증(인증유효기간 3년, 매년 사후심사) 통합**, **④ BSC 4관점(재무/고객/내부프로세스/학습성장) × IT 전략맵 KPI 매핑** 여부, **⑤ 클라우드 FinOps와 CAPEX/OPEX 전환(연 18~22% 절감)** 등 **TCO(Total Cost of Ownership)·NPV·IRR 3대 재무지표**를 의사결정 기준으로 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 531번 시험은 **IT 경영관리**의 종합적 적용 능력을 평가하며, 출제 범위는 **정보화 전략 수립(ISP) -> 정보시스템 감리 -> IT 거버넌스 -> 정보보안 관리체계 -> IT 서비스 운영 -> 사업관리(PMO)**의 6대 영역을 아우른다. 한국정보화진흥원(NIA)이 2023년 발간한 *「디지털 전환 시대의 정보화 사업관리 표준 가이드」*에 따르면, 국내 공공·민간 정보화 사업의 약 **67%**가 거버넌스 부재로 인한 요구사항 변동, **41%**가 TCO 산정 오류로 예산 초과, **28%**가 SLA 미달성으로 운영 단계에서 실패한다. 4차 산업혁명(AI·클라우드·IoT·블록체인) 환경에서는 **ISO/IEC 27001:2022**(2022년 10월 개정, 93개 통제항목 + 11개 신규 속성), **ISO/IEC 20000-1:2018**(IT 서비스경영시스템, 16개 프로세스 영역), **NIST CSF 2.0**(2024년 2월 공개, Govern 6개 신규 카테고리 추가) 등 글로벌 표준이 매년 갱신되므로, 단편적 통제가 아닌 **End-to-End 통합 거버넌스 모델**이 필수적이다.

```text
+---------------------------------------------------------------------+
|             IT 경영 관리 6대 영역 통합 거버넌스 (531번 출제범위)            |
+---------------------------------------------------------------------+
|                                                                     |
|  +--------------+  +--------------+  +--------------+               |
|  | ① 정보화전략  |  | ② IT거버넌스 |  | ③ ISMS-P     |               |
|  |   (ISP/EA)   |--|  (COBIT'19)  |--| (ISO 27001)  |               |
|  |  TOGAF/DoDAF |  |  40 Obj.     |  |  93 Controls |               |
|  +------+-------+  +------+-------+  +------+-------+               |
|         |                 |                 |                        |
|         v                 v                 v                        |
|  +--------------+  +--------------+  +--------------+               |
|  | ④ IT서비스   |  | ⑤ 사업관리   |  | ⑥ 감리/감사  |               |
|  |  (ITIL 4)    |--|  (PMBOK 7)   |--|  (IS Audit)  |               |
|  |  34 Practices|  |  PMO/OKR     |  |  CISA/ISACA  |               |
|  +--------------+  +--------------+  +--------------+               |
|                                                                     |
|  -- 연결 계층 --                                                      |
|  +---------------------------------------------------------+        |
|  |  정책·표준 (ISO 38500) ↔ RACI ↔ KPI/BSC ↔ SLA/OLA ↔ 감리  |        |
|  +---------------------------------------------------------+        |
+---------------------------------------------------------------------+
```

**기존 패러다임(As-Is)** 은 부서별 분절 관리(Siloed IT) — 재무팀 재무시스템, 영업팀 CRM, 운영팀 ERP를 별도 인프라로 운영 — 로 **중복 투자 30~50%**, **인터페이스 오류율 12%** 수준이 일반적이었다. **신규 패러다임(To-Be)** 는 **EA(Enterprise Architecture) 기반 통합**, **API 게이트웨이(Apigee, Kong, AWS API GW)**, **iPaaS(Boomi/MuleSoft)**, **제로트러스트(ZTNA 1.0, SDP)**, **DevSecOps 파이프라인(SonarQube + Snyk + Trivy)**, **FinOps(Cloudability, Vantage)** 기반의 동적 자원 배분으로 전환되어 **TCO 22~35% 절감**, **배포 빈도 6배 증가**, **변경 실패율 60% 감소**(DORA 2023 State of DevOps) 효과를 달성한다.

- **📢 섹션 요약 비유**: IT 거버넌스 6대 영역은 마치 **항공우주 관제센터(NASA Mission Control)의 6개 콘솔**(궤도·통신·생명유지·동력·항법·화면통합) — 각 콘솔이 독립 운용되지만, **통합 비행사(Flight Director)** 가 **ISO 38500 6대 원칙**(책임·전략·취득·성과·준법·인간행위)으로 1분 단위 의사결정을 조정해야 우주선이 궤도에 안착하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 **COBIT 2019의 Cascade Model**(Governance Objective -> Management Objective -> Component -> Process)을 따르며, 5개 도메인·40개 목적(5개 거버넌스 + 35개 관리)·5개 컴포넌트(Process/Organizational Structure/Information/People·Skills·Culture/Technology)·40개 핵심 모델·**11개 설계 요인(Design Factors) 1~6단계**로 구성된다. 핵심 메커니즘은 **(1) Needs Drivers & Strategy -> (2) Risk & I&T Issues -> (3) Enterprise Goals(13개) Alignment -> (4) Governance System Design -> (5) Components Implementation -> (6) Skill/Tooling/Process Deployment**의 6단계로 진행된다.

```text
+------------------------------------------------------------------+
|              COBIT 2019 5-도메인 · 40-목적 참조 모델                 |
+------------------------------------------------------------------+
        +--------------+  ★ 의사결정  +--------------+
        | 1. EDM       |<-------------->|이사회/IT전략위|
        | 5 Objectives |  책임·평가·  +------+-------+
        |(Evaluate,    |  지시·모니터  |
        | Direct,      |  (RACI: A)   |
        | Monitor)     |              |
        +------+-------+              |
               |  정책·전략 연계       |
               v                      v
   +----------------------------------------------+
   | 2. APO (Align, Plan, Organize)   — 14개 목적  |
   |    전략·위험·포트폴리오·예산·인재·SLA 정의   |
   +--------------------+-------------------------+
                        | 계획·조직·아키텍처
                        v
   +----------------------------------------------+
   | 3. BAI (Build, Acquire, Implement) — 11개 목적|
   |    변경·릴리스·테스트·구축·전환·교육          |
   +--------------------+-------------------------+
                        | 구축·구입·이행
                        v
   +----------------------------------------------+
   | 4. DSS (Deliver, Service, Support) — 6개 목적 |
   |    운영·인시던트·연속성·보안·문제·요청처리    |
   +--------------------+-------------------------+
                        | 전달·지원·서비스
                        v
   +----------------------------------------------+
   | 5. MEA (Monitor, Evaluate, Assess) — 4개 목적|
   |    성과·내부통제·외부감사·규제준수(Compliance)|
   +--------------------+-------------------------+
                        | 모니터링·평가
                        v
              지속적 개선 (Kaizen)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스)** | 이사회·전략위원회 수준 의사결정 | ISO 38500 6대 원칙(책임·전략·취득·성과·준법·인간행위) × COBIT 2019 EDM 5개 목적(EDM01 Benefit Realization, EDM02 Risk Optimization, EDM03 Resource Optimization, EDM04 Stakeholder Transparency, EDM05 Compliance) — 의사결정 위임 한계(DMAD: Delegation Matrix) 정의 |
| **APO(정렬·계획·조직)** | 전략-전술-운영 정렬 및 자원 배분 | **13개 Enterprise Goal ↔ 13개 Alignment Goal 매트릭스**(예: EG01 Portfolio of Competitive Products ↔ AG01 I&T Compliance & Support), **TOGAF ADM**(Preliminary->A~H 8단계), **BSC 4관점(재무 20%·고객 25%·내부 30%·학습 25%) 가중치**, **IT 포트폴리오 관리(APO05)** — **Weighted Scoring Model(가중치 0.3×전략일치 + 0.25×ROI + 0.2×위험 + 0.15×규제 + 0.1×자원가용)** |
| **BAI(구축·구매·이행)** | 시스템 전 생애주기 관리 | **PMBOK 7th 12개 Principle** + **PRINCE2 7 Principle**(Continued Business Justification, Learn from Experience, Defined Roles, Manage by Stages, Manage by Exception, Focus on Products, Tailor to Suit) + **BABOK 2.0**(Strategy Analysis->Elicitation->Req. Mgmt->Traceability), **CI/CD 파이프라인**(GitLab CI + Jenkins + ArgoCD) |
| **DSS(전달·지원·운영)** | IT 서비스 일상 운영·장애 대응 | **ITIL 4 Service Value System**: **SVS 핵심요소(Guidance·Organization·People·Technology·Partners·Value Streams)** + **34 Best Practices**(Incident->Problem->Change->Service Desk->Service Level->Continuity->Availability->Capacity->Security) + **Service Value Chain(Opportunity/Demand->Engage->Design/Build->Obtain/Build->Deliver/Support)** 6활동 |
| **MEA(모니터링·평가)** | 성과 측정 및 통제 검증 | **CMMI 5단계**(Initial->Managed->Defined->Quantitatively Managed->Optimizing), **내부 통제
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 531 / 800

<- **이전**: [530. IT 경영 관리 핵심 토픽 530번 시험 요약](/studynote/12_it_management/05_security_compliance/530_it_management_core_topic_530_exam_summary/)
**다음**: [532. IT 경영 관리 핵심 토픽 532번 시험 요약](/studynote/12_it_management/05_security_compliance/532_it_management_core_topic_532_exam_summary/) ->

---
