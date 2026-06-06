---
title: "523. LeSS 대규모 스크럼 (LeSS Large Scale Scrum)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LeSS(Large Scale Scrum)는 2~8개 팀(LeSS) 또는 그 이상(LeSS Huge)으로 스크럼을 확장하는 프레임워크로, 단일 Product Backlog·단일 Product Owner·하나의 Potentially Shippable Product Increment(PSPI)를 유지하면서 기존의 단일 팀 스크럼 원리를 무손상(Unscrummify 방지)으로 다중 팀에 적용한다.
> 2. **가치**: Scrum을 위반하지 않는 "Exponential Scaling"이 가능하며, 조직 구조·프로세스·규칙을 팀 수에 선형(Linear) 증가시키지 않아 조정 오버헤드를 80% 이상 절감하고, 릴리스 리드타임을 4~12배 단축시키며, Feature Team 비율 100%를 통해 컨웨이어 밸류스트림의 병목을 해소한다.
> 3. **판단 포인트**: ①적용 대상(동일 제품/동일 도메인/동일 코드베이스) 명확화, ②Component Team -> Feature Team 전환 가능성 진단, ③"완제품(Whole Product)" 정의 범위(시스템/서브시스템/솔루션), ④LeSS vs LeSS Huge vs Nexus vs SAFe의 트레이드오프, ⑤조직 차원의 구조적 변화(전통 PMO/Functional Dept. 해체) 수용성 평가가 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

기존 단일 팀 스크럼(Single-Team Scrum)은 7±2명, 즉 3~9명의 Development Team을 전제로 한 프레임워크다. 그러나 대용량 시스템(예: 통신망 관제 시스템, 코어뱅킹 플랫폼, 자율주행 통합 SW, e-커머스 마이크로서비스 플랫폼)에서는 **수백~수천 명**의 엔지니어가 하나의 제품을 공동으로 개발해야 하는 상황이 빈번하다. 이러한 규모에서 단순히 "팀을 10개 만든다"는 사고는 곧 **Component Team(컴포넌트 팀) 안티패턴**, **사일로(Silo) 조직**, **Sub-Optimization**, **Local Optimization**으로 귀결되며, 릴리스 주기는 6~18개월로 폭증하고, 통합(Integration) 단계에서 결함이 폭발적으로 증가한다.

LeSS는 이러한 문제를 Craig Larman과 Bas Vodde가 2005~2007년경 제창한 **"Rules over Mechanisms, Less over More, Whole-Product Focus"** 원칙을 토대로, 다중 팀 환경에서 **Scrum 자체를 변형하지 않고(UnScrum 방지)** 확장하는 것을 목표로 한다. 즉, "더 적은 것(Lean)으로 더 많은 가치(Whole Product)"를 창출한다는 Lean 사고방식을 Scrum에 그대로 적용한다.

```text
[단일 팀 스크럼에서 다중 팀 스크럼으로의 진화]

   단일 Scrum (1팀)              LeSS (2~8팀)              LeSS Huge (8+팀)
  +------------+              +-------------+         +----------------------+
  | PO (1명)   |              | PO (1명)    |         | PO (1명)             |
  | SM (1명)   |              | SM (여러명) |         | Area PO (여러명)     |
  | Dev (3~9)  |              | Team×N      |         | Area SM (여러명)     |
  | 1 Backlog  |  -------►    | 1 Backlog   | ------► | Team×N (Feature)    |
  | 1 Product  |              | 1 Product   |         | 1 Product Backlog    |
  | Increment  |              | (PSPI)      |         | Requirement Area 분할|
  +------------+              +-------------+         +----------------------+
       |                            |                          |
       | 3~9명 × 1팀                | 4~9명 × 2~8팀            | 4~9명 × 8팀+       |
       | ~12주 Sprint               | 2~4주 Sprint 유지        | 다중 Area(2~8개)   |
       v                            v                          v
  전통 SW 프로젝트              확장된 Agile                Enterprise Agile
```

기존의 전통적 프로젝트 관리(예: PMBOK 기반 Waterfall, CCPM)는 **Functional Silo(개발/QA/운용 부서 분리)**, **Phase Gate(단계별 게이트)**, **부분 최적화(Sub-Optimization)**라는 한계를 가진다. 특히, **Conway's Law(컨웨이의 법칙, 1968)**에 따르면 시스템 구조는 의사소통 구조를 닮게 되는데, 전통 조직은 컴포넌트별로 부서가 나뉘어 시스템이 분절되고(Part-Product Focus) 전달이 늦어진다. LeSS는 이를 뒤집어 **Feature Team(기능 단위 팀, 1팀이 End-to-End로 한 기능을 완전 개발) -> 고객 가치 흐름(Customer Value Stream)에 최적화된 팀 구조**를 만든다.

> **📢 섹션 요약 비유**: 전통적인 자동차 공장이 엔진, 차체, 도장, 의장 라인을 따로 만들어서 한 달에 합쳐 출고하는 방식이라면, LeSS는 **한 팀이 자동차 한 대 전체를 처음부터 끝까지 조립하는 "도요타 생산방식의 스크럼 버전"**이다. 차체팀이 기다리거나 도장팀이 병목이 되는 일이 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LeSS의 아키텍처는 **Scrum Guide(2011~2020)의 3~5 이벤트 + 3~5 아티팩트 + 3 역할**을 그대로 유지하면서, 팀 수(N)만큼 **Sprint와 Product Backlog는 단일, Team만 N개**로 확장한다. 핵심 메커니즘은 다음과 같다.

```text
[LeSS의 아키텍처 및 이벤트 흐름]

                    +---------------------------------+
                    |   Product Backlog (단일)         |
                    |  - 사용자 스토리, 버그, 기술 부채 |
                    |  - 우선순위는 PO가 결정          |
                    |  - 추정은 다중 팀이 함께        |
                    +----------------+----------------+
                                     | Refinement + PO Sync
                                     v
        +------------------------------------------------------+
        |              Product Owner (1명)                      |
        |  - 제품의 ROI·비전·优先级 총괄                         |
        |  - Stakeholder Negotiation 단일 창구                  |
        +-------------------------+----------------------------+
                                  |
        +-------------------------+---------------------------+
        |            Sprint Planning (전체 + 부분)              |
        |  - Part 1: 전체 팀이 함께 (Backlog 상위 정렬)        |
        |  - Part 2: 팀별로 분산 (각 팀이 자신 작업 결정)      |
        +-------------------------+---------------------------+
                                  |
        +------------+------------+------------+-------------+
        v            v            v            v             v
   +---------+ +---------+ +---------+ +---------+    (Team×N)
   | Team 1  | | Team 2  | | Team 3  | | Team 4  |   Feature Team
   | SM + Dev| | SM + Dev| | SM + Dev| | SM + Dev|   (3~9명/팀)
   | 4~9명   | | 4~9명   | | 4~9명   | | 4~9명   |
   +----+----+ +----+----+ +----+----+ +----+----+
        | Sprint Backlog |       |           |
        | Daily Scrum    |       |           |
        +-------+--------+-------+-----------+
                |
                v
        +-------------------------+
        | Sprint Review (전체)     |  <- 모든 팀이 함께
        | Sprint Retrospective    |  <- 도메인/시스템 단위
        | (전체 + 팀별)           |
        +-------------+-----------+
                      v
        +-------------------------+
        |  Potentially Shippable  |  <- 모든 팀의 Increment를
        |  Product Increment      |    통합한 "완제품" 단위
        |  (PSPI, 단일)           |    Definition of Done 충족
        +-------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Product Backlog (단일)** | 다중 팀이 공유하는 단일 요구사항 풀 | Scrum Guide 준수(단일). Item은 User Story형식으로 Gherkin/Walking Skeleton/Impact Mapping 활용. **PBI 우선순위는 PO의 전권**. Multiple Team Estimation(예: Planning Poker with All Teams)으로 상대규모 산정. |
| **Product Owner (1명)** | 제품의 비전·ROI·우선순위 단일 책임자 | 8팀 이하에서는 단일 PO, LeSS Huge에서는 **Area Product Owner**로 분할하되, **최상위 PO 1명이 전체를 통합 조정**. PO가 Feature Team의 작업을 "지시"하지 않고 Backlog 우선순위로 팀이 자율 선택하도록 유도한다(Over-specification 방지). |
| **Scrum Master (복수)** | 각 팀 또는 2~3팀 단위로 SM 배치 | LeSS에서는 팀당 1명의 SM, LeSS Huge에서는 Area SM. **SM은 PO·관리자·팀 어느 쪽에도 충성하지 않는 "팀 외부 옹호자"**. **임프레비스티(Improv)·시스템 사고·코칭** 역량 필수. |
| **Sprint (동일 주기)** | 모든 팀이 동일한 시작·종료일을 가짐 | 2~4주 고정. **다른 주기 허용 안 함(전체 동기화)**. 다중 팀 Sprint Planning을 통해 같은 Sprint 내에서 팀 간 의존성을 조기 발견(예: 공유 컴포넌트·DB Lock·배포 슬롯). |
| **Potentially Shippable Product Increment (PSPI, 단일)** | 모든 팀의 작업이 통합된 릴리스 가능한 산출물 | 모든 팀이 **End-to-End Done**(코드·테스트·문서·배포 가능)을 충족. Continuous Integration(Jenkins/GitHub Actions/ArgoCD) + Continuous Deployment + Feature Flag(LaunchDarkly/Unleash)가 **기술적 토대**를 형성. |
| **Overall Retrospective (전체 회고)** | 조직 차원의 시스템 회고 | Scrum Guide의 3 Events 외에 **전체 팀 회고**를 추가(보통 Sprint 마지막 날). 포커스: 조직 구조·규칙·환경. 안티패턴 진단: Component Team 잔존, Specialist Silo, Local Optimization. |
| **Communities/Guilds(임의)** | Feature Team을 횡단하는 자발적 지식 공유 | LeSS 자체엔 없지만, **Communities of Practice(CoP)**나 **Guild(예: Architect Guild, Test Guild)**로 보완. Spotify Model의 Tribe/Squad와 유사하나, LeSS는 Squad/Guild가 **Product Backlog 소유권이 없음**을 명확히 함. |
| **Sprint Backlog (팀별)** | 각 팀이 해당 Sprint에서 작업할 항목 | 전체 PBI를 팀이 자율적으로 분배(Self-Selection)하거나, **Sprint Planning Part 2**에서 결정. **Pull 방식**(팀이 우선순위 높은 PBI를 가져감). Push(상사가 할당) 금지. |

### 핵심 메커니즘 심화

1. **Self-Selecting Teams(자기 선택 팀)**: 팀은 PO가 정해주는 것이 아니라, **구성원이 작업할 PBI를 자율적으로 선택**한다. 이를 위해 Sprint Planning Part 2에서 각 팀이 어떤 PBI를 가져갈지 **Negotiation**이 발생한다. John Cutler의 "Product Kata"나 "Story Mapping(Jeff Patton)"가 도입된다.

2. **Multi-Team Coordination**: 8팀을 초과하는 경우, **Scrum of Scrums(SoS)**를 두되, LeSS Huge에서는 **"Coordination Committee"**나 **"Component Team Integration Team"** 같은 미들웨어(중간 조정) 조직을 두지 않는다. 대신 **"Set-Based Design"**과 **"Cross-Team Refinement"**로 시간을 분산 조정한다.

3. **LeSS Huge의 Requirement Area 분할**: 2000명+ 규모에서는 Product Backlog를 **8개 이하의 Requirement Area**(예: 인증, 결제, 검색, 알림, 분석)로 분할하고, 각 Area에 **Area Product Owner**를 둔다. 그러나 **최상위 Backlog Item은 영역에 종속되지 않는 "Customer-Feature"**여야 한다.

4. **Feature Team의 정의**: 한 팀이 한 기능을 **DB 설계 -> API -> UI -> 테스트 -> 배포**까지 독립 수행. **Conway's Law 역이용**으로 시스템 구조를 팀 경계와 정렬시킨다(Team Topologies의 "Stream-Aligned Team"과 동일).

> **📢 섹션 요약 비유**: LeSS는 **"오케스트라 한 곡(전체 PSPI)을 8명의 악장(팀)이 같은 지휘자(PO)·같은 박자(Sprint)·같은 악보(Backlog)로 연주하는 것"**이다. 각 악장은 자기 파트를 자율 해석(Self-Selection)하되, 전체 합주(전체 Retrospective)에서 음색·음량을 조율한다.

---

## Ⅲ. 비교 및 연결

LeSS는 다른 확장 프레임워크(SAFe, Nexus, Scrum@Scale, Spotify Model)와 비교되며, 각각의 트레이드오프가 있다. 기술사 시험에서는 **"왜 LeSS를 선택하는가?"**에 대한 논리적 근거를 요구한다.

| 구분 | **LeSS (2~8팀)** | **LeSS Huge (8+팀)** | **Nexus (3~9팀, Schwaber)** | **SAFe (Scaled Agile)** | **Scrum@Scale (S@S, Sutherland)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **창시자/연도** | Larman & Vodde (2007) | Larman & Vodde (2016) | Ken Schwaber (2015) | Dean Leffingwell (2011) | Jeff Sutherland (2014) |
| **확장 범위** | ~80명 (8팀) | ~수천명 (8+팀) | ~90명 (9팀) | 수만명 (엔터프라이즈) | 수만명 |
| **PO 수** | 1명 | 1 + Area PO | 1명 | 수십명 (Portfolio/Epic/Feature PI) | 1 (최상위) + 다중 PO |
| **Backlog 수** | 1 (단일) | 1 (단일) + Area별 분할 | 1 (단일) | 4개 (Portfolio/Enabler/Program/Team) | 다중 (모듈) |
| **Scrum Guide 준수** | 100% 무손상 | 거의 100% | 100% (Nexus Integration Team 추가) | 30~40% (거의 변형) | 부분 (모듈별 스크럼) |
| **Sprint 주기** | 모두 동일 (2~4주) | 모두 동일 | 모두 동일 | PI Planning 8~12주 + Iteration 2주 | 모두 동일 |
| **팀 구조** | Feature Team (필수) | Feature Team + Area | Feature Team | ART(50~125명 Agile Release Train) | Scrum of Scrums(SoS) |
| **규칙 수** | 매우 적음 (~10개) | 적음 | 적당 | 많음 (수십 개) | 적당 |
| **적합 조직** | 단일 제품·단일 도메인 | 거대 단일 제품 | 단일 제품 | 다중 제품/엔터프라이즈 | 다중 모듈 |
| **도입 난이도** | 중간 (구조 변화 큼) | 높음 | 낮음 | 매우 높음 | 중간 |
| **학습 곡선** | 가파름 (Lean 사고 필요) | 매우 가파름 | 완만 | 완만하지만 적용 어려움 | 완만 |
| **예시 기업** | BMW, Ericsson, John Deere, Reykjavik University | 일부 대기업 통신사 | SAP, Siemens (일부) | Salesforce, Cisco, DBS Bank | Toyota, Pivotal |

### 통합 및 연계 기술

1. **CI/CD 파이프라인과의 통합**: LeSS의 PS
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 523 / 600

<- **이전**: [522. SAFe 대규모 애자일 프레임워크](/studynote/11_design_supervision/06_exam_summary/522_safe_scaled_agile_framework)
**다음**: [524. Nexus 다중 팀 스크럼 조율](/studynote/11_design_supervision/06_exam_summary/524_nexus_multi_team_scrum_coordination/) ->

---
