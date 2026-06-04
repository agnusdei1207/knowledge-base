+++
title = "772. IT 경영 관리 핵심 토픽 772번 시험 요약 (IT Management Core Topic 772 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보화 사업의 기획·착수·종료 전 과정을 ISO 38500(거버넌스), COBIT 2019(운영 통제), ITIL 4(서비스 운영), PMBOK/SPM/ISPM(사업관리) 프레임워크로 정렬하여 Balanced Scorecard 4관점(재무·고객·내부프로세스·학습성장) 기반으로 IT 성과와 위험을 통합 측정·보고하는 경영관리 체계이다.
> 2. **가치**: EA(Enterprise Architecture) 기반 정보화사업 표준 프로세스(분석→설계→구축→이행→평가)를 적용 시 사업 실패율 약 35%→15% 감소, TCO 20~40% 절감, ROI 평균 25% 이상 확보, 거버넌스 성숙도 Level 2→Level 4 도달이 가능하며, 감리 지적사항을 평균 60% 이상 감소시킬 수 있다.
> 3. **판단 포인트**: CIO 직할 vs CCoE(Center of Chief Enterprise Architect) 분권형 거버넌스 모델 선택, De-Facto 표준(Cobit) vs ISO 38500(국제표준) 채택 여부, Agile-Waterfall-Wagile(Waterfall+Agile) 혼용 방식의 프로젝트별 적용, 그리고 On-Premise/Public Cloud/Hybrid별 Capex-Opex 비율 및 통제 환경 차이가 핵심 의사결정 변수이다.

---

## Ⅰ. 개요 및 필요성

정보화 사업은 단순한 SW 개발을 넘어 **전략적 비즈니스 역량(Capability)** 확보의 수단이며, 평균 실패율 35%, 예산 초과율 200% 이상, 사용자 만족도 40% 미만이라는 고질적 문제를 안고 있다. 한국정보화진흥원(KIAT, 구 NIA)의 국가정보화 사업 감리 통계에 따르면, 매년 약 2,000여 건의 정보화 사업에서 부실 이행, 보안 취약점, 요구사항 미반영 등이 반복적으로 지적된다. 이를 해결하기 위해 **IT 거버넌스 + IT 관리 + IT 감리** 3축 통합 모델이 요구되며, 그 핵심 통제 영역이 본 토픽의 대상이다.

특히 2024년 이후 공공부문 클라우드 이용 촉진에 관한 법률(클라우드 이용 촉진법, 2024.1. 시행)과 개인정보 보호법 개정, AI 기본법(2024.9. 시행)으로 인해 **데이터 주권·외주 통제·지속적 통제 모니터링(Continuous Controls Monitoring, CCM)** 이 새로운 통제 사각지대로 부상했다. 기술사 관점에서는 사업 착수 시점부터 폐기 단계까지의 **전생애주기(Lifecycle) 관점**에서 거버넌스-관리-감리 체계를 어떻게 설계하는가가 합격과 탈락을 가른다.

```text
[IT 경영관리 3축 통합 프레임워크 전체 구조도]

                    ┌─────────────────────────────────────────────┐
                    │   Board / CEO / Steering Committee (이사회) │
                    │   - 방향 설정(Direct), 모니터링(Monitor)     │
                    └─────────────────┬───────────────────────────┘
                                      │ 의사결정 위임
                                      ▼
                    ┌─────────────────────────────────────────────┐
                    │   ① IT 거버넌스 (Governance)                │
                    │   ISO 38500 / COBIT 2019 / SOX 404         │
                    │   ─ 책임(R), 의사결정(D), 의사소통(C)        │
                    │   ─ Balanced Scorecard / KPI / Risk Mgmt   │
                    └─────────────────┬───────────────────────────┘
                                      │ 정책·기준 하달
                                      ▼
                    ┌─────────────────────────────────────────────┐
                    │   ② IT 관리 (Management) - 일상적 통제      │
                    │   ─ 전략기획(ISP) → EA(TOGAF/DOAF)         │
                    │   ─ 사업관리(PMBOK/SPM) → 운영(ITIL 4)     │
                    │   ─ 보안관리(ISMS-P/ISO 27001)              │
                    │   ─ 서비스운영(SLA/OLA/UC)                  │
                    └─────────────────┬───────────────────────────┘
                                      │ 성과/위험 보고
                                      ▼
                    ┌─────────────────────────────────────────────┐
                    │   ③ IT 감리 (Audit) - 독립적 검증           │
                    │   ─ 정보시스템 감리법 (법 제22호)            │
                    │   ─ ISACA CISA / COBIT Audit                │
                    │   ─ 내부감사(IIA) + 외부감사(감리법인)        │
                    │   ─ 준거성(Compliance) + 효과성(Effectiveness)│
                    └─────────────────┬───────────────────────────┘
                                      │ 개선 권고(Action)
                                      ▼
                    ┌─────────────────────────────────────────────┐
                    │   Continuous Improvement (지속적 개선)        │
                    │   PDCA + DMAIC + ITIL CSI(지속적 개선)       │
                    └─────────────────────────────────────────────┘
```

**기존(Pre-Digital) vs 신(New Digital) 패러다임 비교**

| 관점 | 기존(1980~2010) | 현재(2015~현재) |
|:-----|:----------------|:----------------|
| **거버넌스 모델** | 중앙집중형 CIO 직할 | 분권형 CCRA(Chief Chief Risk Architect) + CCoE |
| **사업 방식** | Waterfall 일변도 | Agile, DevOps, SRE, MLOps |
| **인프라** | On-Premise 단일 | Multi-Cloud / Hybrid (AWS+Azure+GCP) |
| **투자 기준** | NPV/IRR 회수기간 | NPV + TCO + Real Option + VC(가치지향) |
| **감리 관점** | 사후 감리(End-point) | 상시 감리(Continuous Audit) + CCM |
| **핵심 KPI** | 예산 준수율, 납기 준수율 | 사용자 가치, NPS, TTI(Time-to-Insight), MTTR |
| **리스크 통제** | 연 1회 통제 평가 | GRC 플랫폼 연중 실시간 모니터링 |

- **📢 섹션 요약 비유**: 정보화 사업 관리는 **대형 호텔 체인 운영**과 같다. 이사회(거버넌스)가 브랜드·예산·서비스 기준을 정하면, 호텔 지배인(관리)이 매일 룸메이드·조식·체크인을 운영하며, 정기 방문하는 미슐랭 심사위원(감리)이 별점을 매겨 개선을 권고하는 3계층 운영 모델이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. IT 거버넌스 상세 아키텍처

ISO 38500의 **6원칙(Evaluate, Direct, Monitor)**과 COBIT 2019의 **40개 관리목표(Management Objective)**, **5개 도메인(EDM, APO, BAI, DSS, MEA)** 을 매핑하여 의사결정 권한과 책임 체계를 RACI 차트로 명문화한다. 핵심은 **"Responsibility(책임)은 단수, Accountability(의사결정)는 단수, Consultation/Information은 복수"** 라는 RACI 원칙을 조직 위계에 따라 위임하는 것이다.

```text
[COBIT 2019 5 Domain × RACI 흐름 상세도]

  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │  EDM (5개)   │    │  APO (14개)  │    │  BAI (11개)  │
  │ 거버넌스     │ →  │ 정렬·계획     │ →  │ 구축·실행     │
  │ -EDM01 책임  │    │ -APO01 전략  │    │ -BAI01 사업  │
  │ -EDM02 혜택  │    │ -APO02 아키  │    │ -BAI02 요구  │
  │ -EDM03 위험  │    │ -APO04 혁신  │    │ -BAI03 해법  │
  │ -EDM04 자원  │    │ -APO05 포트  │    │ -BAI05 변경  │
  │ -EDM05 성과  │    │ -APO12 위험  │    │ -BAI07 도입  │
  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
         │ 정책·기준           │ 계획·예산           │ 산출물·결과
         ▼                    ▼                    ▼
  ┌─────────────────────────────────────────────────────────┐
  │           통합 거버넌스 의사결정 라운드테이블            │
  │   Board ─ CIO ─ CFO ─ CHRO ─ CRO ─ CDO ─ CISO ─ CCO   │
  └────────────────────────┬────────────────────────────────┘
                           ▼
  ┌──────────────┐    ┌──────────────┐
  │  DSS (6개)   │    │  MEA (4개)   │
  │ 서비스·지원   │    │ 모니터링·평가 │
  │ -DSS01 운영  │    │ -MEA01 성찰  │
  │ -DSS02 인시  │    │ -MEA02 성숙  │
  │ -DSS03 문제  │    │ -MEA03 준거  │
  │ -DSS04 연속  │    │ -MEA04 문제  │
  │ -DSS05 보안  │    │              │
  └──────────────┘    └──────────────┘
         │ KPI/리스크       │ 감사/보고
         └────────┬─────────┘
                  ▼
          ┌──────────────────┐
          │  Continuous Audit │
          │  (상시 감시 체계) │
          └──────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:----------|:-----|:----------------------|
| **전략기획(ISP)** | 3~5년 중장기 정보화 로드맵, 비전·미션·목표·이니셔티브 도출 | SWOT + Porter 5-Forces + VRIO(가치·희소성·모방불가·조직) → Critical Success Factor(CSF) → Key Goal Indicator(KGI) |
| **EA(Enterprise Architecture)** | 업무-데이터-응용-기술 4계층 표준화, TOGAF ADM(Architecture Development Method) 8단계 적용 | TOGAF ADM(Phase A~H) / DoDAF 8뷰 / FEAF / Zachman 6×6 / Gartner EA Tool (BiZZdesign, MEGA Hopex, LeanIX) |
| **사업관리(PMBOK 7th)** | 10개 지식영역 + 5개 프로세스그룹 + 49개 프로세스, 애자일 하이브리드(Water-Scrum-Fall) | WBS(Work Breakdown Structure) → OBS(Organization Breakdown Structure) → RAM/RACI, EVM(Earned Value Management): CPI(비용실적지수), SPI(일정실적지수), BAC/EAC/ETC/VAC 계산 |
| **서비스운영(ITIL 4)** | 26개 Service Practice(Value Stream 중심), Incident→Problem→Change Enablement 체계 | SIAM(서비스 통합·관리 다중 공급자), SLA 99.9%(3사분기당 8.76시간 다운 허용), OLA·UC, 서비스 카탈로그·포트폴리오·파이프라인 |
| **정보보안(ISMS-P/ISO 27001)** | 11개 통제영역, 93개 통제항목, 114개 통제목표, 연 1회 인증 심사 + 연 1회 사후관리 | ISO 27001:2022(Annex A 93 통제), ISMS-P(한국인터넷진흥원 인증), CSAP(클라우드 보안 인증), 데이터 3법(개인정보·정보통신망·신용정보) |

### B. EVM(Earned Value Management) 핵심 수식

정보화 사업의 **진척도·비용·일정 통합 측정**의 핵심이며, 기술사 시험에서 단골 계산 문제 영역이다.

- **BAC (Budget At Completion)**: 사업 완료 시 총예산
- **EV (Earned Value)**: BAC × 진척률(%) → 실제 수행한 작업의 계획 가치
- **PV (Planned Value)**: 기준일 시점에서 계획된 작업의 예산 가치
- **AC (Actual Cost)**: 기준일까지 실제 투입된 비용
- **CPI (Cost Performance Index) = EV / AC** → 1.0 이상이면 예산 내
- **SPI (Schedule Performance Index) = EV / PV** → 1.0 이상이면 일정 내
- **EAC (Estimate At Completion) = BAC / CPI** → 완료 시 예상 총비용
- **ETC (Estimate To Complete) = EAC - AC**
- **VAC (Variance At Completion) = BAC - EAC**
- **TCPI (To-Complete Performance Index) = (BAC - EV) / (BAC - AC)**

> **예시**: BAC=1억원, 실제 AC=6천만원 투입 시 60% 진척(EV=0.6억), 계획 PV=0.7억
> → CPI=0.6/0.6=1.0(정상), SPI=0.6/0.7=0.857(0.14일정 지연)
> → EAC=1.0/1.0=1.0억(예산 내), TCPI=(1.0-0.6)/(1.0-0.6)=1.0(현 수준 유지 필요)

### C. 정보시스템 감리법 핵심 (법 제22호, 시행령·시행규칙)

- **대상**: 총사업비 5억 원 이상 또는 1년 이상 지속되는 정보화 사업, 공공기관 100% 발주
- **시점**: **종료감리(준공 전 30일 전)**, **단계별 감리**(용역 30%/60%/90% 시점), **중요시점 감리**(5단계)
- **원칙**: 독립성(External), 객관성(Objective), 전문성(Expert), 비밀보장(Confidential)
- **감리영역**: 사업관리 12개 항목, 시스템 구현 12개 항목, 이행·운영 10개 항목
- **시행기관**: NIA(한국지능정보사회진흥원) + NCSI(국가보안기술연구소) + 14개 지정 감리법인

- **📢 섹션 요약 비유**: IT 경영관리 3축은 **영화 제작 과정**과 같다. **거버넌스**는 제작사 대표(투자자), **관리**는 감독·프로듀서(현장 책임자), **감리**는 영화진흥위 심사위원(상영 전 등급 매김)이다. 3자 역할이 충실해야 오스카(성공)를 받을 수 있다.

---

## Ⅲ. 비교 및 연결

### A. 주요 거버넌스/관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 772 / 800

← **이전**: [771. IT 경영 관리 핵심 토픽 771번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/771_it_management_core_topic_771_exam_summary/)
**다음**: [773. IT 경영 관리 핵심 토픽 773번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/773_it_management_core_topic_773_exam_summary/) →

---
