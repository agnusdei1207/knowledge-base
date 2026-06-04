+++
title = "782. IT 경영 관리 핵심 토픽 782번 시험 요약 (IT Management Core Topic 782 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019 거버넌스·ITIL 4 서비스 운영·PMBOK 7 프로젝트·ISO 27001 보안·TOGAF EA를 **"Strategic Fit -> Design -> Operate -> Measure"** 4단계 거버넌스 사이클로 통합하고, RACI·CSF·KGI/KPI를 통해 이사회 의사결정과 현장 운영을 수치로 연결하는 경영체계이다.
> 2. **가치**: 정량적으로는 TCO 20~35% 절감, MTTR 50~70% 단축, Change Success Rate 95% 이상, 정성적으로는 "Right IT, Right Time, Right Cost" 실현을 통한 사업-IT 정렬(Alignment) 및 감리·규제 대응 역량 확보.
> 3. **판단 포인트**: 통제강도 vs 민첩성(Governance-Agility Trade-off), 중앙집중형(COE) vs 분권형(Federated) 거버넌스 모델 선택, Build vs Buy·내부 vs 외부(Sourcing) 의사결정 시 TCO·핵심역량 보유율·벤더 리스크의 3축 트레이드오프 분석 필수.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 비용센터(Cost Center)에서 **전략 자산(Strategic Asset)**으로 격상되면서, IT 투자의 정당화·운영 효율성·리스크 통제·가치 실현을 경영 차원에서 통합 관리할 필요성이 대두되었다. 4차 산업혁명·클라우드 전환·AI 도입이 가속화되면서 CFO·CEO는 "IT에 얼마를 쓰고, 어떤 가치를 받고, 어떤 리스크를 떠안고 있는가"라는 질문에 대해 거버넌스 프레임워크 기반의 답을 요구하고 있다. 특히 한국 환경에서는 전자금융감독규정·개인정보보호법·클라우드컴퓨팅법·ISMS-P 인증·감리원이 제시한 IT 거버넌스 표준(2020년 5월)을 모두 충족해야 하므로, 단일 프레임워크가 아닌 **COBIT×ITIL×ISO 27001×ISMS-P** 멀티프레임워크 통합 운영이 핵심 역량이다.

기존 패러다임은 부서별(Silo) IT 운영으로 중복 투자, Shadow IT, Change 실패율 30~50%, 장애 발생 시 책임 소재 불명, KPI 부재 등의 문제가 상존했다. 새로운 패러다임은 **Value Creation** 관점에서 "투자->포트폴리오->아키텍처->구현->서비스->평가"의 End-to-End Value Chain을 정의하고, CSF(핵심성공요인)와 KGI/KPI로 가치를 계측·환류하는 것이다.

```text
+------------------------------------------------------------------+
|         전통 IT 운영 (Silo) vs. 거버넌스 기반 IT 경영 (GOV)      |
+------------------------------------------------------------------+
|  [Before]                          [After]                        |
|  +---------+  +---------+          +-------------------------+   |
|  |기획실  |  |정보화   |          |  IT Steering Committee   |   |
|  |(各自)  |  |(각자)   |          |  (이사회-경영-IT 정렬)  |   |
|  +----+----+  +----+----+          +------------+------------+   |
|       | 중복투자    | Shadow IT                  | RACI·정책      |
|       v            v                             v               |
|  +---------+  +---------+          +-------------------------+   |
|  |사업부  |  |개발/운영 |          | Value Office (PMO+EA+BCM)|   |
|  |요구   |  |팀       |          | Portfolio·Risk·Service   |   |
|  +---------+  +---------+          +-------------------------+   |
|       |            |                             |               |
|       +-> 책임모호, KPI 부재 <-> 계량·환류·자동화 감리대응 <--+   |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스 도입 전은 "각 가정의 개별 발전기(소음·비용 폭발)"로 전기를 쓰던 시절, 도입 후는 "원자력 발전소-송전-계량기-검침"이 통합된 현대 전력계통과 같다. 거버넌스 = **전력계통 운영 규약**.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 **3-레이어(Governance-Management-Operation) × 5-도메인(Strategy-Architecture-Project-Service-Risk)** 구조로 표현할 수 있다. 상위 거버넌스 레이어(COBIT 2019의 EDM: Evaluate-Direct-Monitor)는 이사회·경영진의 의사결정을, 중위 관리 레이어(Align-Plan-Organize: APO, Build-Acquire-Implement: BAI)는 전략·포트폴리오·아키텍처를, 하위 운영 레이어(Deliver-Support: DSS, Monitor-Evaluate-Assess: MEA)는 서비스·리스크·보안·평가를 담당한다.

```text
   +------------------------------------------------------------+
   |  EDM: 이사회 (Evaluate·Direct·Monitor) --> 거버넌스 체계  |
   |   +- Benefit Realization   +- Risk Optimization            |
   |   +- Resource Optimization +- Stakeholder Transparency     |
   +----------------------+-------------------------------------+
                          | 위임(Delegation)·정책(Policy)·예산
   +----------------------v-------------------------------------+
   |  APO: 전략·포트폴리오·아키텍처 (Align·Plan·Organize)        |
   |   +- APO01 전략    +- APO05 포트폴리오   +- APO13 보안     |
   |   +- APO12 리스크  +- APO14 데이터 거버넌스                |
   +----------------------+-------------------------------------+
                          | ROI·TCO·우선순위
   +----------------------v-------------------------------------+
   |  BAI: 구축·획득·구현 (Build·Acquire·Implement)              |
   |   +- BAI03 솔루션 선정  +- BAI06 변경관리(RFC/CAB)         |
   |   +- BAI11 품질관리·테스트 커버리지                        |
   +----------------------+-------------------------------------+
                          | SLA·OLA·UC
   +----------------------v-------------------------------------+
   |  DSS·MEA: 서비스 전달·지원·모니터 (Deliver·Support·Monitor)|
   |   +- DSS02 인시던트(우선순위 P1~P4, MTTR)                  |
   |   +- DSS03 문제관리(RCA, Known Error DB)                   |
   |   +- MEA01 성능평가(NPS·CSAT·가용성 99.9%)                |
   +------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스 의사결정)** | 이사회-경영진의 정책·예산·리스크 한계선 설정 | RACI 매트릭스, 의사결정 권한 매트릭스(RACI: Responsible, Accountable, Consulted, Informed), 의사결정 게이트웨이($0~$100M 구간별 승인권) |
| **APO(전략·포트폴리오·EA)** | 투자 포트폴리오 우선순위·아키텍처 청사진 | TOGAF ADM(Architecture Development Method) 8단계, BCG/GE 매트릭스 기반 IT 투자 분류(Run/Grow/Transform), BPI/RPA 후보 도출 |
| **BAI(구축·변경·이행)** | 솔루션 도입·Change·Release 품질 통제 | CAB(Change Advisory Board) 주간회의, RFC( Request for Change) 승인 절차, CI/CD 파이프라인(GitLab·ArgoCD), 테스트 커버리지 ≥85% |
| **DSS(서비스 운영·지원)** | Incident·Problem·Service Request 처리 | ITIL 4 Service Value System(SVS), 인시던트 P1~P4 우선순위(영향도×긴급도 매트릭스), SLA 99.9%·MTTR 4H·MTBF ≥720H |
| **MEA(평가·감리·보안)** | KPI 측정·내부감사·규제 대응 | CSAT/NPS·가용성·Change Success Rate, ISO 27001 내부감사, ISMS-P 인증심사, 전자금융감독규정 준수 체크리스트 |

핵심 운영 지표로 **① Run/Grow/Transform 투자 비율**(목표 60:25:15), **② Change Success Rate**(목표 ≥95%), **③ MTTR**(Major Incident ≤4H), **④ First Call Resolution(FCR) ≥75%**, **⑤ Critical Incident 건수 추이(YoY -30%)** 등을 사용한다. 알고리즘 측면에서는 인시던트 우선순위 산정에 **Priority = Impact × Urgency** 매트릭스(예: P1=긴급×고영향, P2=중영향×긴급, P3=저영향×중긴급)를 적용하며, 문제관리의 근본원인 분석(RCA)에는 5-Why 또는 Ishikawa Fishbone을 표준화한다.

- **📢 섹션 요약 비유**: COBIT의 40개 관리목적(Management Objective)은 **"회사의 5개 부서(전략·재무·인사·영업·IT)가 따라야 하는 40개 정책 매뉴얼"**과 같고, 각 부서장이 페이지별로 "누가 무엇을 언제 어떻게 책임지며"를 따르는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001/ISMS-P** | **PMBOK 7** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관점** | 거버넌스(What/Why) | 서비스 운영(How) | 보안 통제(How-Well) | 프로젝트 수행(How) | 아키텍처 청사진(What) |
| **핵심 산출물** | Cascade Goals, RACI | 34개 Practice, SVS | 93개 Annex A 통제항목 | 12 Principle, 49 Process | ADM 8단계, 4A(BA/DA/AA/TA) |
| **측정 지표** | KGI/KPI, CSF | SLA/OLA, MTTR/MTBF | RPN(위험도), KRI | SPI/CPI, EAC, ES | 아키텍처 적합도, ROI |
| **대상 계층** | 이사회·CIO | 서비스 데스크·운영팀 | CISO·보안팀 | PM·PMO | EA 아키텍트·전략기획 |
| **주 활용** | 전략 정렬, 감사, 규제 | ITSM 도구(SM/CMDB/ITOM) | 인증·컴플라이언스 | 단발성 프로젝트 | 표준화·통합·로드맵 |

ITIL 4의 **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)은 COBIT 2019의 **Management Objective**와 1:1 대응되며, **PMBOK 7의 12 Principle** 중 "Steward the Project, Focus on Value, Build Quality into Processes"는 COBIT의 EDM(위임)과 APO05(포트폴리오 가치) 원칙과 직접 매핑된다. 또한 **ISO 27001의 Annex A 통제**(93개)는 COBIT의 DSS05(보안운영), APO13(보안관리)과 중첩되며, 한국 ISMS-P의 64개 통제항목은 ISO 27001을 **상향 정합**(금융·공공기관 추가 통제: 클라우드·생체인증·전자금융)한 것이다. TOGAF의 ADM은 프로젝트 착수 시 EA 산출물(As-Is/To-Be/전환계획)을 제공하여 PMBOK의 사업서(Business Case)에 직접 활용된다.

```text
    +--------------+   목표연결    +--------------+
    |  COBIT 2019  | ------------ |  ITIL 4 SVS  |
    | (Governance) |              |  (Operation) |
    +------+-------+              +------+-------+
           | Cascade Goals               | Practice
           v                              v
    +--------------+  EA 청사진   +--------------+
    |  PMBOK 7     | <------------> |  TOGAF 10    |
    | (Project)    |              | (Architecture)|
    +------+-------+              +------+-------+
           | Risk·Quality                | 표준·연동
           v                              v
    +---------------------------------------------+
    |  ISO 27001 / ISMS-P  (보안 통제 프레임워크)  |
    |  +-- 93 통제항목(Annex A) + 64(ISMS-P)      |
    |  +-- COBIT DSS05, APO13과 1:N 매핑           |
    +---------------------------------------------+
```

- **📢 섹션 요약 비유**: COBIT은 **헌법**(원칙·권한), ITIL은 **행정절차**(민원·서류), PMBOK은 **건설현장 매뉴얼**, TOGAF는 **도시계획도**, ISO 27001은 **치안·소방 규정**이다. 이 다섯 가지를 **도시(기업)**에서 동시에 운영해야 안전하고 효율적인 도시에 산다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **정렬(Alignment) 진단**: 비즈니스 전략 5개 축과 IT 프로젝트 포트폴리오의 매핑률 ≥85%인가? 미정렬 프로젝트는 "Strategic Fit=0"으로 KPI 산정에서 제외했는가? (예: COBIT 2019의 Goals Cascade 활용)
2. **투자 분류(Run/Grow/Transform)**: 연초 IT 예산의 60:25:15 비율을 충족하는가? Run >75%이면 "혁신 정체" 경보, Transform >40%이면 "운영 부실" 경보 발령. SI/NI(신규/증설)사업 우선순위는 NPV·IRR·Payback Period로 산정했는가?
3. **변경·릴리스 통제**: Change Success Rate ≥95%, Emergency Change ≤5%인가? 모든 Production 변경은 CAB 승인 + Backout Plan + 영향도 평가(Impact Analysis)를 거쳤는가? (DSS06 Change Enablement)
4. **인시던트·문제 운영**: P1 인시던트 발생 시 15분 내 Communication Tree 가동
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 782 / 800

<- **이전**: [781. IT 경영 관리 핵심 토픽 781번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/781_it_management_core_topic_781_exam_summary/)
**다음**: [783. IT 경영 관리 핵심 토픽 783번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/783_it_management_core_topic_783_exam_summary/) ->

---
