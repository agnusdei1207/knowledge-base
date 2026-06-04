+++
title = "760. IT 경영 관리 핵심 토픽 760번 시험 요약 (IT Management Core Topic 760 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 760. IT 경영 관리 핵심 토픽 760번 시험 요약 (IT Management Core Topic 760 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 27001, EA(TOGAF), PMBOK 7th 등 글로벌 표준 프레임워크를 통합하여 **거버넌스-전략-운영-아키텍처-투자-보안-리스크** 7대 축을 하나의 Value Chain으로 연결하는 것이며, 평가(EDM), 지시(Direst), 모니터링(Monitor)의 3단계 루프를 통해 IT가 비즈니스 가치를 지속 창출하도록 설계하는 것이다.
> 2. **가치**: 글로벌 Gartner(2024) 통계에서 성숙한 IT 거버넌스 조직은 **IT 투자 대비 ROI 23% 향상**, 프로젝트 실패율 **42%->17% 감소**(Standish Group CHAOS Report 2023), MTTR 평균 **68% 단축**, 정보보안 사고 비용 평균 **USD 1.5M 절감**(IBM Cost of Data Breach 2023 기준) 등 정량적 효과를 입증하고 있다.
> 3. **판단 포인트**: 기술사 답안 작성 시 **"표준 프레임워크 적용 -> 현업 Pain Point 매핑 -> 정량 KPI 도출 -> 리스크/비용 Trade-off"** 의 4단 논증 구조를 일관되게 사용해야 하며, 클라우드·AI·제로트러스트 등 신규 패러다임 도입 시 **레거시 호환성, 조직 Change Readiness, 규제 준수(개인정보보호법/ISMS-P/DORA)** 간의 균형점을 명확히 제시하는 것이 고득점 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사(및 컴퓨터시스템응용기술사) 시험에서 **760번 계열 토픽**은 IT 경영(Management) 전반을 아우르는 메타 영역이다. 4차 산업혁명, 디지털 전환(DX), 생성형 AI, 클라우드 네이티브, ESG 컴플라이언스 등 외부 환경의 급격한 변화 속에서 CIO/CTO는 단순한 "시스템 운영자"에서 "비즈니스 가치 공동 창출자(Value Co-Creator)"로 역할이 전환되었다. 과거(1990~2000년대)에는 IT 부서가 백오피스 비용 센터(Cost Center)로 인식되어 흑자 부서의 IT 요청을 단순 처리하는 **"Break-Fix"** 형태였으나, 2010년대 이후에는 **"Run-Grow-Transform"** 모델, 2020년대에는 **"Run-Grow-Transform + Product(Platform)"** 모델로 발전하며 IT 거버넌스 성숙도가 기업 전체의 시가총액과 ESG 평가에 직접 영향을 미치게 되었다.

특히 2024년 한국 환경에서 DORA(디지털운영복원력법, 2024.1 시행)와 EU AI Act, 개인정보보호법 개정(2023.9)으로 인해 IT 거버넌스는 더 이상 선택이 아닌 **의무**가 되었으며, 기술사 시험에서도 **"어떤 표준을 왜 선택했는지"**에 대한 논리적 근거 제시가 요구된다.

```text
+---------------------------------------------------------------------+
|        IT 경영 관리 7대 축(Value Chain) 통합 참조 모델                |
+---------------------------------------------------------------------+
|                                                                     |
|   +--------------+     +--------------+     +--------------+        |
|   |  1.Governance|----->| 2.Strategy & |----->|  3.Enterprise|        |
|   |  (COBIT 2019)|     |   Planning   |     | Architecture  |        |
|   |              |     | (ISP/EA)     |     |  (TOGAF/Archi|        |
|   | EDM/Direst/  |     | SWOT/Portfo. |     |  Mate/DoDAF) |        |
|   | Monitor Loop |     |              |     |              |        |
|   +------+-------+     +------+-------+     +------+-------+        |
|          |                    |                    |                |
|          v                    v                    v                |
|   +--------------+     +--------------+     +--------------+        |
|   |  4.Service & |<----->|  5.Investment|<----->|  6.Security  |        |
|   |  Operation   |     |  & Portfolio |     |  & Risk      |        |
|   | (ITIL 4 SVS) |     |  Management  |     | (ISO27001/   |        |
|   | DevOps/SRE   |     |  TBM/FinOps |     |  ISMS-P/DORA)|        |
|   +------+-------+     +------+-------+     +------+-------+        |
|          |                    |                    |                |
|          v                    v                    v                |
|   +-----------------------------------------------------+            |
|   |  7.Project·Change·Compliance (PMBOK/PRINCE2/Agile) |            |
|   |     + IT Audit (ISO 38500/ISAE 3402/SOC 2)         |            |
|   +-----------------------------------------------------+            |
|                              |                                      |
|                              v                                      |
|                  +------------------------+                          |
|                  | Business Value(Capabi- |                          |
|                  | lity,Benefit,Realiza-  |                          |
|                  | tion:Risk Ratio)       |                          |
|                  +------------------------+                          |
+---------------------------------------------------------------------+
   <-> (Feedback Loop: KPI/SLA/SLI/BCP-DR Test/Internal Audit)
```

**시대의 흐름에 따른 패러다임 비교:**

| 시대 | 패러다임 | 핵심 KPI | IT 부서 위치 | 대표 표준 |
|:---|:---|:---|:---|:---|
| 1990s | Break-Fix / 데이터센터 운영 | 가용성(Uptime), MTBF | Cost Center | ITIL v1-v2 |
| 2000s | SOA / ERP / ITIL 정착 | SLA 준수율, ROI | Enabler | ITIL v3, COBIT 4.1, ISO 20000 |
| 2010s | Cloud / DevOps / Agile | Time-to-Market, NPS | Strategic Partner | COBIT 5, ITIL 2011, TOGAF 9 |
| 2020s | AI/Native / Zero-Trust / SRE | DORA Metrics, CX, ESG | Value Co-Creator | COBIT 2019, ITIL 4, SAFe, NIST CSF 2.0 |
| 2024s+ | AI-Augmented Governance / Autonomous IT | MTTR, Innovation %, Trust Index | Business Driver | ISO 42001(AI), DORA, EU AI Act |

- **📢 섹션 요약 비유**: IT 경영 관리는 **"도시의 종합 개발 계획"** 과 같다. 토지 용도(EA), 교통망(인프라), 소방서(보안), 예산(투자), 시민 서비스(SLA) 등 모든 시스템을 하나의 마스터플랜으로 조율해야 비로소 "살고 싶은 도시(지속가능한 기업)"가 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 **"계층(Hierarchy) + 루프(Loop)"** 구조로 이해해야 한다. 상위에서 하위로 흐르는 계층 구조(Policy -> Strategy -> Architecture -> Process -> Operation)와, 하위에서 상위로 피드백을 제공하는 루프 구조(Operation -> Monitoring -> Evaluation -> Policy Update)가 동시에 작동한다.

```text
+-------------------------------------------------------------------+
|           IT 거버넌스-관리 3계층 + 4단계 루프 모델                  |
+-------------------------------------------------------------------+
       정책/거버넌스 계층 (Policy & Governance Layer)
       ------------------------------------------
        +----------------------------------------+
        | Board / Steering Committee (이사회/   |
        | IT전략위원회) - ISO 38500 IT Governance |
        +----------------+-----------------------+
                         | 책임(R), 의사결정(D)
                         v
       전략/기획 계층 (Strategy & Planning Layer)
       ------------------------------------------
        +----------------------------------------+
        | CIO / EA Center / PMO                  |
        | • IT 전략(ISP) 수립 : 3~5년 로드맵    |
        | • EA(TOGAF ADM) : B->D->A->T->O->P Cycle  |
        | • PortFolio Mgmt : Run/Grow/Transform  |
        +----------------+-----------------------+
                         | 지시(D), 평가(E)
                         v
       운영/서비스 계층 (Operation & Service Layer)
       ------------------------------------------
        +----------------------------------------+
        | 서비스 운영: SRE, DevOps, Service Desk |
        | 프로세스: ITIL 4 SVS(34 Practices)     |
        |   ◦ Incident/Problem/Change/Service    |
        |     Request/Continual Improvement      |
        | 보안/리스크: ISMS-P, ISO27001, BCP/DR  |
        +----------------+-----------------------+
                         | 결과(Measured)
                         v
       +----------------------------------------+
       | 모니터링/피드백 (Monitor & Feedback)    |
       |  • KPI: 가용성 99.95%, MTTR < 30분     |
       |  • SLA/SLI/SLO(Service Level)          |
       |  • Balanced Scorecard 4관점            |
       |  • Internal Audit(연 1회), 외부 Audit  |
       +----------------+-----------------------+
                        | 개선(Action)
                        +---------------> 상위 계층
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **이사회/IT전략위** | IT 거버넌스 최종 의사결정, IT 원가 회계(Chargeback) 정책, Risk Appetite 설정 | ISO/IEC 38500 "Evaluate-Direct-Monitor" 원칙 적용, 분기별 정례 회의, RACI 매트릭스 운영 |
| **CIO + EA Center** | IT-비즈니스 전략 정렬(Strategic Alignment), 정보시스템 전략계획(ISP) 수립, EA 청사진(Blueprint) 관리 | TOGAF ADM(Architecture Development Method) 8단계: Preliminary->A:Vision->B:Business->C:Information Systems->D:Technology->E:Opportunities->F:Migration->G:Governance, ArchiMate 3.2 표기법 사용 |
| **PMO(Project Mgmt Office)** | 프로젝트 포트폴리오 관리, 방법론 표준화, 다중 프로젝트 간 리소스/우선순위 조정 | PMBOK 7th(12 Principles, 8 Performance Domains), PRINCE2 7th(7 Practices, 5 Process Groups), 애자일 스케일링(SAFe 6.0 Large Solution) |
| **서비스 운영 조직(SRE/DevOps)** | SLA/SLO 기반 서비스 제공, 자동화, 인시던트 대응, 카오스 엔지니어링 | Four Keys(DORA): Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR; SRE Workbook의 Error Budget 개념(연간 가용성 99.95%이면 4.38시간 Error Budget) |
| **정보보안 조직(CISO)** | 정보보호 정책, 통제, 사고 대응, 컴플라이언스, 제로트러스트 구현 | ISO 27001:2022(Annex A 93개 통제), ISMS-P(한국, 64개 검증항목), NIST CSF 2.0(Govern-Identify-Protect-Detect-Respond-Recover 6 Function), 제로트러스트(ZTA): NIST SP 800-207 3대 원칙(Resource·Communication·Workflow) |
| **IT 감사/리스크** | 내부 통제 평가, 컴플라이언스 검증, 개선 권고 | COBIT 2019 40개 Govern/Manage Objective 매핑, ISAE 3402 / SOC 2 Type II 보고서, ISACA 감사 프레임워크 |
| **FinOps/ITAM** | 클라우드 비용 최적화, 라이선스 컴플라이언스, 하드웨어/소프트웨어 자산 수명주기 관리 | FinOps Foundation 프레임워크(Inform->Optimize->Operate), TBM(Technology Business Management) Taxonomy v4, ITAM(SAM: Software Asset Management, HAM: Hardware Asset Management) |

### 핵심 알고리즘 및 공식

**1) 가용성(Availability) 및 신뢰성 공식:**

```
가용성(Availability) = (MTBF / (MTBF + MTTR)) × 100
SLA 예시: 99.9% (Three Nine) -> 연간 8.76시간 다운 허용
           99.95%         -> 연간 4.38시간 다운 허용
           99.99% (Four Nine) -> 연간 52.56분 다운 허용
           99.999% (Five Nine) -> 연간 5.26분 다운 허용
```

**2) IT 투자 ROI 계산 (TBM 기반):**

```
IT ROI = (Total Benefits - Total Costs) / Total Costs × 100
NPV = Σ [CFt / (1+r)^t] - Initial Investment
Payback Period = Initial Investment / Annual Cash Flow
```

**3) 위험도(Risk Score) 산출:**

```
Risk = Likelihood(가능성, 1~5) × Impact(영향도, 1~5)
     = 1: Negligible, 2: Minor, 3: Moderate, 4: Major, 5: Catastrophic
리스크 허용 한도: Risk ≥ 15 -> 즉시 완화(Mitigate) 조치
```

**4) DORA Four Key Metrics(DevOps 성숙도):**

```
Elite     : Deploy > Multiple/day, LT < 1h, CFR < 5%,  MTTR < 1h
High      : Deploy 1/day~1/w,    LT 1d~1w,  CFR 5~10%,  MTTR < 1d
Medium    : Deploy 1/w~1/m,      LT 1w~1m,  CFR 10~15%, MTTR < 1w
Low       : Deploy < 1/m,        LT > 1m,    CFR > 15%,  MTTR > 1w
```

**5) Error Budget 계산 (SRE):**

```
Error Budget = (1 - SLO) × Time Window
예) SLO 99.9% / 30일 = 0.1% × 30일 = 43.2분 Error Budget
```

- **📢 섹션 요약 비유**: 이 3계층-4루프 구조는 **"비행기의 자동조종장치(Autopilot)"** 와 같다. 조종사(이사회)가 비전(전략)을 세우고, 관제탑(CIO/PMO)이 항
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 760 / 800

<- **이전**: [759. IT 경영 관리 핵심 토픽 759번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/759_it_management_core_topic_759_exam_summary/)
**다음**: [761. IT 경영 관리 핵심 토픽 761번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/761_it_management_core_topic_761_exam_summary/) ->

---
