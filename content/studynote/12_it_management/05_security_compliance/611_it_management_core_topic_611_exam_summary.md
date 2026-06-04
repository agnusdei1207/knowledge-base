+++
title = "611. IT 경영 관리 핵심 토픽 611번 시험 요약 (IT Management Core Topic 611 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019(거버넌스 목표 40개·관리 목표 참조)**·**ITIL 4(Service Value System)**·**ISO/IEC 38500(6원칙)**·**PMBOK 7th(8성능영역)**·**TOGAF ADM** 프레임워크를 통합하여 **계획(Plan)->구축(Build)->운영(Run)->감리(Monitor)** 의 가치사슬(Value Chain)을 최적화하는 경영학문입니다.
> 2. **가치**: 정량적으로는 **IT 투자수익률(ROIT) 20~35% 개선**, **TCO 15~30% 절감**, **MTTR 40~60% 단축**, 정성적으로는 **IT-Business Alignment Index 30% 향상**, **컴플라이언스 위반 0건 달성**, **그림자 IT(Shadow IT) 50% 가시화** 효과를 제공합니다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① Build vs. Buy(자체개발 vs 패키지)** ② **Centralized vs. Federated(중앙 vs 분권 거버넌스)** ③ **In-house vs. Outsourcing(자체운영 vs 아웃소싱)** ④ **Three 9s(99.9%) vs Four 9s(99.99%) 가용성**이며, **NPV/IRR/Payback Period** 정량평가와 **Balanced Scorecard 4관점(재무·고객·내부프로세스·학습성장)** KPI를 동시에 고려해야 합니다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation) 가속화, 클라우드·AI·IoT 등 신기술 도입, **개인정보보호법(PIPA)·EU GDPR·ISMS-P** 등 규제 강화로 인해 IT는 단순 지원기능을 넘어 **경영 전략의 핵심 동력**이 되었습니다. 그러나 통계청 및 Gartner 보고에 따르면 국내 대기업 IT 예산의 약 **30~40%가 레거시 시스템 유지보수**에 투입되어 신기술 투자 여력이 부족하며, IT-Business 정렬도 미흡으로 **프로젝트 실패율 30~50%**, **요구사항 변경률 평균 35%**가 발생합니다. 또한 **그림자 IT(Shadow IT)** 의 확산으로 보안사고가 연평균 25% 증가하여, 체계적 IT 경영관리 프레임워크의 도입이 필수적입니다.

```text
+-------------------------------------------------------------+
|            IT 경영관리 4대 영역 통합 프레임워크              |
|                                                             |
|  +----------------+  +----------------+  +--------------+  |
|  |  IT 거버넌스    |  |  IT 서비스 운영  |  |  프로젝트관리 |  |
|  |  (Governance)   |  |  (Service Ops)  |  |  (Delivery)  |  |
|  |  • COBIT 2019   |  |  • ITIL 4 SVS   |  |  • PMBOK 7   |  |
|  |  • ISO 38500    |  |  • ISO 20000    |  |  • PRINCE2   |  |
|  |  • IT 전략기획   |  |  • SLA/OLA/UC   |  |  • 애자일    |  |
|  +--------+-------+  +--------+-------+  +------+-------+  |
|           |                   |                  |          |
|           +---------+---------+------------------+          |
|                     v                                        |
|        +----------------------------+                       |
|        |  정보시스템 감리(Audit)     |                       |
|        |  • IS 감리법/감리원 제도    |                       |
|        |  • ISMS-P / ISO 27001      |                       |
|        |  • 컴플라이언스 / 리스크     |                       |
|        +-------------+--------------+                       |
|                      v                                      |
|         +--------------------------+                        |
|         |   기업 가치 극대화(Value) |                        |
|         |  • ROIT / TCO / NPV      |                        |
|         |  • BSC 4관점 / KPI       |                        |
|         +--------------------------+                        |
+-------------------------------------------------------------+
```

**기존 패러다임 vs 신규 패러다임**:
- **기존(Traditional IT)**: Cost Center 관점, 개별 시스템 단위 관리, On-premise, 연 1회 예산 사이클, 사후 통제
- **신규(Digital Enterprise IT)**: Value Driver 관점, EA 기반 통합관리, Hybrid Cloud, 지속적 투자 우선순위 재조정, 실시간 리스크 모니터링

- **📢 섹션 요약 비유**: IT 경영관리는 **도시의 종합교통체계**와 같습니다. 거버넌스는 **교통법규·신호체계**, ITSM은 **실시간 교통관제센터**, 프로젝트관리는 **새로운 도로 건설공사**, 감리는 **교통경찰·단속시스템**이며, BSC KPI는 **교통흐름 측정 지표(정체도·사고율)**입니다. 이 4개가 어긋나면 도시는 마비됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리는 국제 표준 프레임워크의 계층적 통합으로 구현됩니다. 최상위 **거버넌스(Why) -> 전략(What) -> 프로세스·서비스(How) -> 측정·평가(How well)** 의 4계층 구조입니다.

```text
+----------------------------------------------------------+
|         4계층 IT 경영관리 아키텍처(ZA: Zone Architecture)   |
+----------------------------------------------------------+
|  Layer 1. 거버넌스(Governance) - WHY                      |
|  +------------------------------------------------+      |
|  |  COBIT 2019: 40 Governance & Management Obj.   |      |
|  |  ISO/IEC 38500: 6 Principles (Responsibility,  |      |
|  |    Strategy, Acquisition, Performance, Confor- |      |
|  |    mity, Human Behavior)                       |      |
|  |  King IV Report: 17 Governance Principles      |      |
|  +------------------------------------------------+      |
+----------------------------------------------------------+
|  Layer 2. 전략(Strategy) - WHAT                          |
|  +------------------------------------------------+      |
|  |  • IT 전략기획(ISP) : 3년 로드맵               |      |
|  |  • TOGAF ADM 8단계 : As-Is -> To-Be Gap         |      |
|  |  • Porter 5 Forces, Value Chain, SWOT           |      |
|  |  • EA 4 domains : BA/DA/AA/TA                  |      |
|  +------------------------------------------------+      |
+----------------------------------------------------------+
|  Layer 3. 프로세스·서비스(Process/Service) - HOW          |
|  +------------------------------------------------+      |
|  |  ITIL 4 SVS: 34 Practices, Service Value Chain |      |
|  |    Plan->Engage->Design&Transition->Obtain/Build  |      |
|  |    ->Deliver&Support->Improve                    |      |
|  |  PMBOK 7: 8 Performance Domains + 12 Principles |      |
|  |  BPR/BPI: Hammer-Champy 4단계                  |      |
|  +------------------------------------------------+      |
+----------------------------------------------------------+
|  Layer 4. 측정·평가(Measure) - HOW WELL                   |
|  +------------------------------------------------+      |
|  |  • BSC: 재무(ROI)·고객(NPS)·프로세스(품질)·학습|      |
|  |  • KPI Tree, CSF(Critical Success Factor)       |      |
|  |  • NPV / IRR / Payback / ROIT / TCO            |      |
|  |  • CMMI 5단계, TMMi, ISO 15504                 |      |
|  +------------------------------------------------+      |
+----------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회** | 의사결정 및 통제 | CEO·CIO·이사회 3자 구조, RACI 매트릭스, 의사결정 권한 매트릭스(Decision Rights Matrix) |
| **COBIT 2019** | 거버넌스 목표체계 | 5원칙, 7컴포넌트(Principles/Goals/System Components), 40 Governance & Management Objectives |
| **ITIL 4 SVS** | 서비스 가치사슬 | Service Value System(Opportunity/Demand/Value), 34 Practices, Continual Improvement(Kata) |
| **TOGAF ADM** | EA 구축 방법론 | Preliminary->A(비전)->B~D(BA/DA/TA)->E(Opportunity)->F(Plan)->G(Governance), 8단계 사이클 |
| **PMBOK 7th** | 프로젝트 관리 | 8 Performance Domains(Stakeholder/Team/Planning/Performance/Project Work/Delivery/Measurement/uncertainty), 12 Principles |
| **BSC & KPI** | 성과 측정 | 4관점(재무/고객/내부/학습), SMART KPI, Leading vs Lagging Indicator |
| **IS 감리 절차** | 독립적 검증 | ① 계획(Plan)->② 분석->③ 설계->④ 구현->⑤ 시험->⑥ 운영 6단계(정보시스템 감리법 §14) |
| **아웃소싱 계약** | 서비스 조달 | Fixed-price/T&M/Cost-plus/Outcome-based/SLA 99.9~99.999% 5단계 |

**핵심 수식 및 산출 기준**:
- **NPV(순현재가치)** = Σ CF_t / (1+r)^t - I₀, 양수일 경우 투자 적격
- **IRR(내부수익률)** = NPV=0 이 되는 할인율, r > hurdle rate일 때 적격
- **ROIT(정보기술 투자수익률)** = (IT 투자 편익 - 비용) / IT 투자 비용 × 100
- **TCO(총소유비용)** = 직접비용(HW/SW) + 간접비용(인력·교육·장애) + 기회비용, 일반적으로 초기 CAPEX의 3~5배
- **가용성 등급**: Three 9s(99.9%)=연 8.76시간 장애, Four 9s(99.99%)=연 52.6분, Five 9s(99.999%)=연 5.26분
- **MTTR(Mean Time To Repair)** = 총 장애 복구 시간 / 장애 발생 횟수
- **MTBF(Mean Time Between Failures)** = 총 가동시간 / 장애 횟수

- **📢 섹션 요약 비유**: **COBIT은 헌법**, **TOGAF는 도시계획도**, **ITIL은 교통운영 매뉴얼**, **PMBOK은 건설현장 작업지침서**, **BSC는 건강검진 항목표**입니다. 4계층이 모두 갖춰야 건강한 IT 조직이 됩니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 27001** |
| :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스/관리 | IT 서비스 운영 | 정보보안 관리체계 |
| **관점** | 전체(Enterprise-wide) | 서비스 가치사슬 | 정보자산 보호 |
| **구조** | 40 Objectives, 5원칙, 7컴포넌트 | 34 Practices, SVS | 93 Control (Annex A) |
| **적용 대상** | CIO·이사회·감사 | 서비스 매니저·운영자 | CISO·보안담당 |
| **측정 KPI** | Goal Cascade, Maturity | SLA, MTTR, NPS | KRI, Incident Rate |
| **연계 관계** | 거버넌스->전략 | 운영·서비스 | 보안 통제 |

**타 프레임워크와의 연결**:
- **COBIT ↔ PMBOK**: COBIT의 EDM( Evaluate, Direct, Monitor) -> PMBOK의 Portfolio/Program 관리
- **ITIL ↔ DevOps**: ITIL Change Enablement ↔ CI/CD Pipeline, ITIL Incident ↔ SRE Error Budget
- **TOGAF ↔ Zachman**: TOGAF ADM은 Zachman 6×6 매트릭스의 방법론적 구현
- **BSC
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 611 / 800

<- **이전**: [610. IT 경영 관리 핵심 토픽 610번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/610_it_management_core_topic_610_exam_summary/)
**다음**: [612. IT 경영 관리 핵심 토픽 612번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/612_it_management_core_topic_612_exam_summary/) ->

---
