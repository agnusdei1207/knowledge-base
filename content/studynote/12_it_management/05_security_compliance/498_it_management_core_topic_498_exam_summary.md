+++
title = "498. IT 경영 관리 핵심 토픽 498번 시험 요약 (IT Management Core Topic 498 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance & Management)는 COBIT 2019의 40개 관리목표, ITIL 4의 Service Value Chain, ISO/IEC 38500의 6대 원칙을 통합하여 **거버넌스(EDM) → 전략 정렬(APO) → 가치 실현(BAI/DSS) → 모니터링(MEA)** 의闭环(Closed-loop) 체계로 IT 자산을 비즈니스 가치로 전환하는 경영 체계이다.
> 2. **가치**: Gartner 2024 보고 기준 IT 거버넌스 성숙도 상위 25% 조직은 **IT 투자 ROI 32% 향상**, 디지털 전환 성공률 **45%→78%**, 보안 사고 대응시간 **평균 67일 단축**, M&A 시 IT 실사(Due Diligence) 비용 **40% 절감** 효과를 달성한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **집중형 vs 분산형 거버넌스 구조**(COBIT RACI Chart 기반), ② **프레임워크 조합**(COBIT+ITIL+ISO 27001 중첩 적용 범위), ③ **성과측정 모델**(BSC-IT 4관점 vs KPI 기반), ④ **투자 우선순위 결정**(NPV, IRR, TCO, Risk-Adjusted ROI), ⑤ **Agile Governance 채택 수준**(Scaled Agile, SAFe 거버넌스 레이어 통합 여부)이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화, 생성형 AI 도입, 클라우드 네이티브 전환, 그리고 개인정보보호법·AI 기본법·ESG 규제 강화로 인해 IT는 더 이상 단순 비용센터(Cost Center)가 아니라 **전략적 가치 창출 엔진(Value Driver)** 이 되었다. 그러나 한국 기업 70% 이상이 IT-Business 정렬 실패, 그림자 IT(Shadow IT)泛滥, Legacy 시스템 기술 부채(Technical Debt), 사이버 리스크 증대를 동시에 겪고 있다(2024 한국정보화진흥원 조사).

**기술사적 도전 과제**:
- **그림자 IT**: 전사 평균 35~50%의 SaaS 사용이 IT 부서 승인 없이 진행(SaaS Sprawl)
- **Legacy 기술 부채**: 국내 대기업 평균 38%가 20년 이상 된 Mainframe/COBOL 시스템 의존
- **IT 복잡성**: 평균 대기업이 270개 이상의 애플리케이션, 60개 이상의 데이터 소스 운영
- **규제 준수 부담**: 개인정보보호법, AI 기본법, ESG 공시, ISMS-P 인증 등 다중 컴플라이언스

```text
┌──────────────────────────────────────────────────────────────────────┐
│           IT 경영 관리 498번 토픽 - 통합 거버넌스 체계도               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────────────────────────────────────────────────┐      │
│   │  경영진 / 이사회 (Board / Steering Committee)             │      │
│   │   - IT 전략 승인, ROI 리뷰, Risk Appetite 설정           │      │
│   └──────────────────────┬───────────────────────────────────┘      │
│                          │                                          │
│   ┌──────────────────────▼───────────────────────────────┐         │
│   │  IT 거버넌스 위원회 (ITGC) - 의사결정 / 감독            │         │
│   │   - CIO, CDO, CISO, 사업부 IT Sponsor                  │         │
│   └──────┬─────────────┬─────────────┬────────────────────┘         │
│          │             │             │                              │
│   ┌──────▼──────┐ ┌────▼─────┐ ┌────▼──────┐ ┌──────────────┐     │
│   │ 전략 정렬   │ │ 포트폴리오│ │ 서비스    │ │ 위험/보안    │     │
│   │ (APO)      │ │ 관리     │ │ 관리(DSS) │ │ 관리         │     │
│   │            │ │          │ │           │ │              │     │
│   │ • IT 전략  │ │ • 투자   │ │ • SLA    │ │ • ISMS-P    │     │
│   │ • 아키텍처 │ │   우선순위│ │ • 인시던트│ │ • 사이버    │     │
│   │ • 혁신     │ │ • 예산   │ │ • 변경   │ │ • BCP/DR    │     │
│   └──────┬─────┘ └────┬─────┘ └─────┬─────┘ └──────┬───────┘     │
│          │            │              │              │              │
│   ┌──────▼────────────▼──────────────▼──────────────▼───────┐     │
│   │         모니터링 / 평가 (MEA) - 측정 및 개선              │     │
│   │   - KPI 대시보드, BSC-IT, 내부감사, 외부감사              │     │
│   └─────────────────────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**레거시 IT 경영 vs 현대 IT 경영 비교**:

| 차원 | 레거시(2000년대) | 현대(2024~) |
|:---|:---|:---|
| 조직구조 | CIO 단일 책임, IT 부서 폐쇄형 | CDO/CISO/CRO 추가, **Tri-Crown** 거버넌스 |
| 의사결정 | 연간 CapEx 예산 사이클, ROI 회수 5년+ | 분기별 재조정, **Run-Grow-Transform** 포트폴리오 |
| 측정 | 가용성(Availability) 중심, MTBF/MTTR | **고객 경험(NPS), Time-to-Market, 가치실현률** |
| 위험관리 | 재해복구(DR) 중심 | **제로트러스트, AI 리스크, 공급망(Supply Chain) 리스크** 통합 |
| 문화 | "No" 문화(보수적) | **FinOps, DevSecOps, Platform Engineering** 문화 |
| 기술 | On-Premise, Waterfall | **Multi-Cloud, SaaS, AI/ML, Edge Computing** |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자** 와 같다. 첼로(보안), 바이올린(개발), 트럼펫(사업) 등 다양한 악기(IT 영역)를 개별 연주자가 잘 다루는 것만으로는 부족하며, **지휘자(거버넌스)** 가 악보(전략), 박자(프로세스), 음량(자원)을 통합 조정해야만 **하나의 심포니(기업 가치)** 가 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 4대 핵심 표준 프레임워크는 ① **COBIT 2019** (Control Objectives for Information and Related Technologies), ② **ITIL 4** (IT Infrastructure Library), ③ **ISO/IEC 38500:2015** (IT Governance Standard), ④ **ISO/IEC 20000-1:2018** (IT Service Management)이다. 이 4대 프레임워크는 상호 보완적으로 적용된다.

### A. COBIT 2019 - 거버넌스/관리 체계

```text
┌──────────────────────────────────────────────────────────────────────┐
│              COBIT 2019 Governance & Management Objectives          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  EDM - Evaluate, Direct, Monitor (5 objectives)            │     │
│  │  • EDM01 거버넌스 프레임워크 설정/유지                       │     │
│  │  • EDM02 가치 전달 보장                                     │     │
│  │  • EDM03 위험 최적화                                        │     │
│  │  • EDM04 자원 최적화                                        │     │
│  │  • EDM05 이해관계자 투명성 보장                              │     │
│  └────────────────────────────────────────────────────────────┘     │
│                              │                                      │
│  ┌──────────┬──────────┬─────────────┬─────────────┐               │
│  │  APO     │   BAI    │    DSS      │    MEA      │               │
│  │ (14)     │   (11)   │    (6)      │    (4)      │               │
│  │ 정렬/계획│ 구축/구현│ 서비스/지원 │ 모니터/평가 │               │
│  └────┬─────┴────┬─────┴──────┬──────┴──────┬──────┘               │
│       │          │            │             │                      │
│       ▼          ▼            ▼             ▼                      │
│  ┌────────────────────────────────────────────────────────┐        │
│  │  40개 상세 관리목표 (Management Objectives)              │        │
│  │  + 7개 컴포넌트: 프로세스/구조/정보 흐름/사람/기술/원칙 │        │
│  │  + 5가지 중점 영역: 보안/위험/규제/DX/서비스             │        │
│  └────────────────────────────────────────────────────────┘        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

COBIT 2019의 핵심 혁신은 **"Focus Area"** 개념 도입이다. 기본 40개 목표에 추가로 **정보보안, DevOps, 위험, 규제 준수, 디지털 전환, 서비스 관리** 등 중점 영역(예: Cybersecurity Focus Area 13개 세부목표)을 매핑하여 조직 상황에 맞게 커스터마이징할 수 있다.

### B. ITIL 4 - 서비스 가치 시스템 (SVS)

ITIL 4는 2019년 출시되어 **Service Value System (SVS)** 중심으로 재설계되었다. 핵심은 **7가지 지침(Guideline Principles)** 과 **Service Value Chain**이다.

**Service Value Chain 6개 활동**: Plan → Improve → Engage → Design & Transition → Obtain/Build → Deliver & Support

**26가지 ITIL Practice** (예: Incident Management, Change Enablement, Service Desk, Problem Management, Continual Improvement, Service Level Management)

### C. ISO/IEC 38500:2015 - IT 거버넌스 6대 원칙

| 원칙 | 핵심 의미 | 실무 적용 |
|:---|:---|:---|
| **Responsibility** | IT 의사결정 책임 소재 명확화 | ITGC 위원회, RACI 매트릭스 |
| **Strategy** | 비즈니스 전략과 IT 전략 통합 | IT Strategic Plan, EA Roadmap |
| **Acquisition** | IT 투자의 합리적 의사결정 | Business Case, NPV/IRR 분석 |
| **Performance** | IT 서비스 성과 측정 및 모니터링 | SLA, KPI 대시보드, BSC-IT |
| **Conformance** | 내부 정책 및 외부 규제 준수 | ISMS-P, GDPR, AI 기본법 |
| **Human Behavior** | IT 의사결정 시 인간/문화 고려 | Change Management, 저항관리 |

### D. IT 거버넌스 조직 구조 패턴

```text
┌────────────────────────────────────────────────────────────────┐
│         IT 거버넌스 조직 구조 3가지 패턴 (Weill/Ross 모델)       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1] 중앙 집중형 (Centralized / Monarchy)                       │
│      ┌──────────────────┐                                       │
│      │  Group CIO/CEO   │                                       │
│      └────────┬─────────┘                                       │
│       ┌
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 498 / 800

← **이전**: [497. IT 경영 관리 핵심 토픽 497번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/497_it_management_core_topic_497_exam_summary/)
**다음**: [499. IT 경영 관리 핵심 토픽 499번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/499_it_management_core_topic_499_exam_summary/) →

---
