+++
title = "6. 감리 프레임워크 (Audit Framework) 3차원 구조 - 감리 영역, 감리 관점, 감리 단계"
description = "감리 영역, 감리 관점, 감리 단계의 3차원 구조로 구성된 정보시스템 감리 프레임워크의 체계와 적용"
date = 2026-04-05

[taxonomies]
tags = ["design_supervision"]

[extra]
tags = ["design_supervision"]
+++

# 06. 감리 프레임워크 3차원 구조

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 감리 프레임워크는 [감리 영역](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/)([Audit Domain](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/)), [감리 관점](/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/)([Audit Perspective](/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/)), [감리 단계](/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/)([Audit Phase](/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/))라는 세 개의 축이 형성하는 3차원 체적 구조로, 이 을 통해 감리의 모든면을 빠짐없이 Cover한다.
> 2. **가치**: 이 3차원 프레임워크는 감리의 scope을 정의하고, 각 프로젝트에 대한 점검 방향을 설정하며, 사업 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 시점에 맞는 적절한 감리을/를지시하는 나침반 역할을 한다.
> 3. **융합**: 영역(무엇을), 관점(어떤 기준으로), 단계(언제)의 조합으로 감리 업무를 모듈화하여, 감리팀의خصص 영역을 정의하고 업무을 효율적으로하는 데 활용된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

정보시스템 감리는 그 범위([Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/))가 매우 넓다. 하나의 정보화 사업을 감리하려면 사업 관리 영역부터 응용 시스템, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), 보안에 이르기까지 수 많은 분야를 점검해야 하고, 각 분야마다 절차, 산출물, 성과 등 다양한 관점에서 접근해야 하며, 이는 요구정의부터 종료 시점까지 사업의 에 걸쳐 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)된다.

이러한인 감리 업무를 체계적으로 수행하기 위해서는된프레임워크(Framework)이 필요하다. 만약 그러한프레임워크가 없다면, 감리팀은 프로젝트을aning 곳하거나 하여하거나, 또는 중요한 프로젝트를 놓치기 쉽상이게 된다. 감리 프레임워크 3차원 구조는 이러한을방지하고, 에 대한 체계적 감리를 가능하게 하는 뼈대다.

이 프레임워크의 세 축은 각각 다른 관점에서 감리를 구조화한다. [감리 영역](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/)은 "무엇을 감리할 것인가"를 정의하고, [감리 관점](/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/)은 "어떤 기준으로 감리할 것인가"를 정의하며, [감리 단계](/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/)는 "언제 감리할 것인가"를 정의한다. 이 세 축의 교차점에 감리 개별 프로젝트이 위치하게 되어, 감리 프로젝트이 이적 공간 안에서 빠짐없이 관리된다.

다음 다이어그램은 이 3차원 프레임워크의구조를 적으로 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">감리 프레임워크 3차원 구조 도식</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">감리 영역 (Domain)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">사업관리</div><div class="kb-diagram-node">응용시스템</div><div class="kb-diagram-node">DB/보안</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">감리 관점</div><div class="kb-diagram-node">감리 단계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╱</div><div class="kb-diagram-cell">╱</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╱</div><div class="kb-diagram-cell">╱</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╱</div><div class="kb-diagram-cell">╱</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Procedure ── ► 요구정의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Deliverable</div><div class="kb-diagram-cell">설계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Performance</div><div class="kb-diagram-cell">종료</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 3차원 공간의 모든 교차점 = 개별 감리 항목 (총 27개)</div></div>
</div>
</div>



이 도식의 핵심은 감리 프로젝트이 단순히 목록으로 나열되는 것이 아니라, 축의(좌표)로관리된다는 점이다. 예를 들어, "사업관리-절차-요구정의"와 "사업관리-산출물-종료"는 같은 영역이지만 관점과 단계가 다르므로 전혀 다른 감리 프로젝트이 된다. 이러한 구조관리를 통해 감리의 누락과 중복을적으로방지할 수 있다.

📢 **섹션 요약 비유**: 감리 프레임워크 3차원 구조는 <strong>'도자기 공장의 품질 관리 시스템'</strong>과 같습니다. ()은 각각 다른 검사 기준(내구성, 외관, 색상)을대표하고, 이들의 교차점에서 각 제품의완성 가하게측정됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

3차원 프레임워크의 각 축에 대해 더 깊이 살펴보자.

**[감리 프레임워크 3축 상세 분석]**

| 축 (Axis) | 정의 | 하위 요소 | 역할 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/">감리 영역</a> (<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a>)</strong> | 감리 대상의 | 사업관리, 응용시스템, DB/보안 | "무엇을" 감리할 것인가 |
| <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/">감리 관점</a> (Perspective)</strong> | 감리 접근 기준 | 절차(Procedure), 산출물(Deliverable), 성과([Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)) | "어떤 기준으로" 감리할 것인가 |
| <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/">감리 단계</a> (Phase)</strong> | 사업 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 시점 | 요구정의, 설계, 종료 | "언제" 감리할 것인가 |

[감리 영역](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/) × [감리 관점](/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/) × [감리 단계](/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/)의 3차원 조합에서 도출되는 구체적 감리 프로젝트 수를 나타내면 다음과 같다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">3차원 조합에 의한 감리 프로젝트 수 (예시)</div></div>
<div class="kb-diagram-note">■ 사업관리 (Domain 1)</div>
<div class="kb-diagram-tree-item" style="--depth:0">절차 (Perspective 1) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-tree-item" style="--depth:0">산출물 (Perspective 2) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-tree-item" style="--depth:0">성과 (Perspective 3) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-note">→ 소계: 9개 프로젝트</div>
<div class="kb-diagram-note">■ 응용시스템 (Domain 2)</div>
<div class="kb-diagram-tree-item" style="--depth:0">절차 (Perspective 1) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-tree-item" style="--depth:0">산출물 (Perspective 2) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-tree-item" style="--depth:0">성과 (Perspective 3) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-note">→ 소계: 9개 프로젝트</div>
<div class="kb-diagram-note">■ DB/보안 (Domain 3)</div>
<div class="kb-diagram-tree-item" style="--depth:0">절차 (Perspective 1) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-tree-item" style="--depth:0">산출물 (Perspective 2) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-tree-item" style="--depth:0">성과 (Perspective 3) × 요구정의/설계/종료 = 3개 프로젝트</div>
<div class="kb-diagram-note">→ 소계: 9개 프로젝트</div>
<div class="kb-diagram-note">■ 총계: 27개 기본 감리 프로젝트 (3 Domain × 3 Perspective × 3 Phase)</div>
</div>
</div>



이 계산의 핵심은 단순히수인 프로젝트 수의 이 아니라, 축의 조합을 통해 되고 빠짐없는 감리 Coverage를한다는 점이다. 만약 3차원프레임워크가 없이 단순 목록으로 관리했다면, 같은 영역에서 다른 관점의 프로젝트이 누락되거나, 중요한 사업 단계에서의 점검이 문제가 발생했을 것이다.

📢 **섹션 요약 비유**: 3차원 프레임워크의구조는 <strong>'체스를 두는 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>'</strong>과 같습니다. 흑과 백으로 나뉜에서、(감리 프로젝트)는 (영역), (관점), (단계) 3개의로, 3차원 적으로해야 에서의수를 둘 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

3차원 프레임워크는 다른 감리 방법론과 어떻게 연결되며, 어떤 시너지를 발휘하는가?

**[3차원 프레임워크와 다른 방법론의 / 융합]**

| 비교 항목 | 3차원 프레임워크 | [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/) 방법론 ([ISACA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/021_isaca_global_standard/)) | [ATAM](/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/) (아키텍처 평가) |
|:---|:---|:---|:---|
| **** | 영역×관점×단계 | 5개 [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | [민감도점](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/094_sensitivity_point_architecture_tradeoff_control_knob/)×[상충점](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/095_tradeoff_point_architecture_evaluation_atam_conflict/)×[리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) |
| **포커스** | 감리 Coverage 관리 | 글로벌 | 아키텍처 품질 |
| **사용 주체** | 공공 감리팀 | 국제 감리인 | 아키텍처 설계자 |
| **관점 차이** | 관리 струк화 (Management-oriented) | 통제 중심 (Control-oriented) | 품질 중심 (Quality-oriented) |

이러한에도 불구하고, 세 방법론은 상호 보완적으로할 수 있다. 3차원 프레임워크가 감리의전역적 구조를 제공하고, [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/) 방법론이의 전문성을하며, ATAM이 아키텍처 깊이를 제공하는 방식이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">다양한 감리 방법론의 시너지 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">통합 감리 프레임워크</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3차원 프레임워크</div><div class="kb-diagram-node">CISA 방법론</div><div class="kb-diagram-node">ATAM</div></div>
<div class="kb-diagram-note">전역적 구조 전문적 기술 아키텍처 깊이</div>
<div class="kb-diagram-note">(Coverage) (Audit Technique) (Quality)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">감리 결과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(적 + 적 + )</div></div>
</div>
</div>



이 시너지구조의 핵심은 3차원 프레임워크가(Skeleton) 역할을 하고, 다른 방법론이(Muscle)과(Organ) 역할을 하는 비유로 이해하면 된다. 뼈대 없이는이 붙을 곳이 없고, 이 없으면를있었다 이/가한다. 따라서 세 방법론은의 역할을 다하면서해야 한다.

📢 **섹션 요약 비유**: 3차원 프레임워크와 다른 방법론의는 <strong>'과 양식의'</strong>과 같습니다. 한식의 기본estructura(3차원 프레임워크)에 양식의 전문 조리법([CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/), [ATAM](/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/))을 접목하여,적이면서도 있는 fusion cuisine( 감리)을 만들어낼 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실제 감리 현장에서 3차원 프레임워크를 적용할 때의 판단 사례를 살펴보자.

**1. 감리 프로젝트 배분 사례: "우리 팀원 3명을 어떻게 설정해야 하나?"**
* **상황**: 소규모 감리 프로젝트에 감리 전문가 3명이 배정되었다. 사업관리, 응용시스템, DB/보안 3개 영역을 모두 점검해야 하지만 은/는 3명뿐이다.
* **기술사적 판단**: 3차원 프레임워크의 영역 축을 력 설정에 활용한다. 각 전문가에게 1개 영역씩 전문적으로 담당시키고, 관점과 단계는 공유된 검사로 관리한다. 각 전문가가 담당 영역의 관점(절차, 산출물, 성과)과 단계(요구정의, 설계, 종료)를 하게 커버하도록 하여, 성 깊이와를 동시에 달성한다.

**2. 감리 범위 조정 사례: "일정이 빠듯해서 일부 프로젝트을 줄이고 싶습니다"**
* **상황**:，된 요구정의 단계 감리에서 일부 프로젝트을 생략하여 일정을 단축하고 싶다.
* **기술사적 판단**: 3차원프레임워크에서 특정 프로젝트을하면, 그에 해당하는 감리가 누락된다. 따라서 가능한 프로젝트을 판단할 때, 각 축의을분석해야 한다. 예를 들어, 요구정의 단계에서 가장 중요한의은/는 "사업관리-산출물-요구정의"(사업자 completeness [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))이므로, 이것을하면 단계에서문제가될 위험이 높다. 반면 "응용시스템-절차-요구정의"는 요구정의 단계에서는 상대적으로 중요도가 낮을 수 있다.

**3. 감리 결과 분석 사례: "종합 감리 결과가 나왔는데, 이것을 어떻게 요약해야 하나?"**
* **상황**: 모든 영역, 관점, 단계의 감리가하고, 종합 결과 보고서를 작성해야 한다.
* **기술사적 판단**: 3차원 프레임워크를 기준으로 결과를하면, 어떤 영역/관점/단계에서 주로문제가 발견되었는지pattern을할 수 있다. 만약 "DB/보안-산출물-종료" 영역에서 반복적으로문제가 발견된다면, 이는 해당의 산출물 관리 체계에 시스템적문제가 있을 가능성이 높다. 이처럼 3차원 프레임워크로 분석하면, 막연한 종합이 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반의pattern 분석이 가능해진다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">3차원 프레임워크 기반 감리 분석 방법</div></div>
<div class="kb-diagram-note">Step 1: 3차원 별 문제점 Count</div>
<div class="kb-diagram-tree-item" style="--depth:0">영역: 사업관리(2건), 응용시스템(3건), DB/보안(5건)</div>
<div class="kb-diagram-tree-item" style="--depth:0">관점: 절차(1건), 산출물(4건), 성과(5건)</div>
<div class="kb-diagram-tree-item" style="--depth:0">단계: 요구정의(1건), 설계(3건), 종료(6건)</div>
<div class="kb-diagram-note">Step 2: 패턴 도출</div>
<div class="kb-diagram-tree-item" style="--depth:0">산출물 관점에서 문제가 가장 많음 → 산출물 관리 체계 약점</div>
<div class="kb-diagram-tree-item" style="--depth:0">종료 단계에서 문제가 가장 많음 → 사전 통제</div>
<div class="kb-diagram-note">Step 3: 핵심 개선 방향 도출</div>
<div class="kb-diagram-note">→ 종료 단계의 산출물 관점 집중 개선 필요</div>
</div>
</div>



이 분석 방법의 핵심은 3차원 프레임워크가 단순한 관리 도구를 넘어, 감리 를 수하고pattern을도출하는 분석 프레임워크로도 활용될 수 있다는 점이다.

📢 **섹션 요약 비유**: 3차원 프레임워크의 분석 활용은 <strong>'기상 예보의 3요소'</strong>와 같습니다. 온도(기압), 습도, 바람의 3요소를 함께 분석하여 날씨pattern을예측하듯이, 감리에서도 영역·관점·단계 3요소를 함께 분석하여문제의pattern을할 수 있습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

3차원 프레임워크의 효과적 활용을 통해 기대할 수 있는는 다음과 같다.

| 기대 효과 | 세부 내용 | 측정 지표 |
|:---|:---|:---|
| <strong>적 <a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/017_audit_execution/">감리 수행</a></strong> | 모든 영역/관점/단계를 빠짐없이 커버 | 감리 프로젝트 누락률 0% |
| **효율적 설정** | 팀원 성 기반 영역별 | 업무 불균형 20% 이내 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반 결과 분석</strong> | 3차원 기반 패턴 분석 |분석 시간 30% 단축 |
| **글로벌 기준과의 정합성** | [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/)/[COBIT](/knowledge-base/studynote/12_it_management/01_governance_strategy/004_cobit/) 등 과의 호환 | 산 90% 이상 |

**미래 전망:**
미래의 감리 프레임워크는 더욱 다이나믹한 형태로 진화할 전망이다. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)) 프로젝트에서는 단계(Phase) 개념이 희석되고, [MVP](/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/)(최소 기능 제품) 기반의 반복 개발이가 되면서, 전통적인 3단계(요구정의/설계/종료) 프레임워크에 대한 재검토가 필요할 수 있다. 또한 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동화 감리 도구가 보편화되면,에의존하지 않고 실시간으로 영역/전단계의 감리를 수행하는 4차원(시간 축 추가) 프레임워크로의 진화도 기대할 수 있다.

📢 **섹션 요약 비유**: 미래의 감리 프레임워크 진화는 <strong>'구글 맵스의'</strong>와 같습니다. 처음에는 2D 지도(기존 관리),(3차원 관점), 이제는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 경로 추천(4차원: 시간 축)까지 추가되듯이, 감리 프레임워크도 새로운 축을 추가하며 진화할 것입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* [감리 영역](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/) ([Audit Domain](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/)) | 사업관리, 응용시스템, DB/보안 등 감리 대상의 전문
* [감리 관점](/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/) ([Audit Perspective](/knowledge-base/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/)) | 절차([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)), 산출물(Product), 성과([Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)) 등 감리 접근의 기준
* [감리 단계](/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/) ([Audit Phase](/knowledge-base/studynote/11_design_supervision/01_audit_framework/009_audit_phase/)) | 요구정의, 설계, 종료 등 사업 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 시점에 따른 감리 시점
* [CISA](/knowledge-base/studynote/11_design_supervision/01_audit_framework/022_cisa_certification_audit/) (Certified Information Systems Auditor) | ISACA의 국제 공인 정보시스템 감사사로, 글로벌
* [ATAM](/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/) ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Trade-off Analysis Method) | [소프트웨어 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/201_software_architecture_definition/) 속성을 평가하는 방법론

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">감리 영역 (Audit Domain)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3차원 감리 체계 (3D Framework)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">품질 보증 (QA, Quality Assurance)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">리스크 통제 (Risk Control)</div></div>
</div>
</div>



이 흐름도는 [감리 영역](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/)을 3차원 체계로 묶어 QA와 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 통제로 이어지는 구조를 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 감리 프레임워크 3차원 구조는lego 블록을 세 방향(위아래, 왼쪽오른쪽, 앞뒤)에서 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것과 같아요. 세 방향 모두에서 빠짐없이 맞춰져야 멋진 작품(정보시스템)이 되는 거예요.
2. **원리**: 세 방향은 각각 "무엇을 만들었는지(영역)", "어떤 방법으로 만들었는지(관점)", "언제 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)했는지(단계)"를대표해요.
3. **효과**: 세 방향을 모두 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 blocks의 빈틈이나 기울어진 부분을 정확히 찾을 수 있듯이, 감리에서도 시스템의빠짐없는 점검이 가능해져요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 6 / 530

← **이전**: [5. 정보시스템 감리기준 (행정안전부 고시)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/005_audit_standards/)
**다음**: [7. 감리 영역 (Audit Domain) - 사업 관리, 응용 시스템, 데이터베이스, 시스템 아키텍처/보안](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/) →

---
