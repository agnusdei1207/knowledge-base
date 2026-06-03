+++
title = "164. Tableau — 드래그앤드롭 VizQL 셀프서비스 시각화"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: Tableau는 VizQL (Visual Query Language, [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 질의 언어)이라는 독자 기술로 드래그앤드롭 동작을 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 자동 변환하여 SQL 없이 복잡한 분석을 가능하게 하는 업계 선도적 셀프서비스 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 플랫폼이다.
- **가치**: LOD (Level of Detail, 세부 수준) 표현식(FIXED/[INCLUDE](/knowledge-base/studynote/04_software_engineering/uncategorized/670_use_case_include_extend/)/EXCLUDE)은 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 집계 수준과 독립적인 계산을 가능하게 하여, "고객당 첫 구매일" 같은 복잡한 비즈니스 질문을 SQL 없이 해결하는 핵심 차별화 기능이다.
- **판단 포인트**: Live Connection(항상 최신, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 의존)과 Extract(.hyper 인메모리, 빠름, 갱신 필요)의 선택은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 볼륨·갱신 빈도·보안 요건에 따라 결정되며, [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) 대비 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 유연성이 높지만 Microsoft 생태계 통합은 약하다.

---

## Ⅰ. 개요 및 필요성

### Tableau의 역사와 위치

Tableau는 2003년 Pat Hanrahan(스탠퍼드 교수, Pixar 공동 창업자)와 Chris Stolte, Christian Chabot이 창업했다. 2019년 Salesforce에 157억 달러에 인수되어 현재 Salesforce 생태계의 핵심 분석 플랫폼으로 운영된다.

Gartner Magic Quadrant BI & Analytics 분야에서 지속적 리더 위치를 유지하며, 기업용 BI 시장에서 Microsoft [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) BI와 1, 2위를 다툰다.

**📢 섹션 요약 비유**: Tableau는 <strong>전문 사진작가의 카메라</strong>와 같다. 기본 사진(간단한 차트)은 스마트폰(Excel)으로도 찍을 수 있지만, 전문적이고 정밀한 작업(복잡한 분석·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/))에는 전문 장비(Tableau)가 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Tableau 플랫폼 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Tableau 플랫폼 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 연결 계층</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Live Connection</div><div class="kb-diagram-cell">Extract (.hyper)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 직접 DB 쿼리</div><div class="kb-diagram-cell">─ 인메모리 컬럼형 엔진</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 항상 최신</div><div class="kb-diagram-cell">─ 빠른 쿼리 성능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ DB 성능 의존</div><div class="kb-diagram-cell">─ 갱신 스케줄 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분석·계산 계층 ▼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VizQL 엔진</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">드래그앤드롭 → SQL/MDX 자동 변환 → 결과 시각화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">계산 유형:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① 계산 필드 (Calculated Field): 커스텀 수식</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">② LOD 표현식: FIXED/INCLUDE/EXCLUDE</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ 테이블 계산: 누적합, 순위, 전년 대비</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">공유·배포 계층 ▼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Tableau Desktop</div><div class="kb-diagram-cell">Tableau Server / Tableau Cloud (SaaS)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(로컬 제작 도구)</div><div class="kb-diagram-cell">(공유·임베딩·중앙 거버넌스)</div></div>
</div>
</div>



### LOD (Level of Detail) 표현식

LOD 표현식은 Tableau의 가장 독특하고 강력한 기능으로, <strong><a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a>의 집계 수준과 무관하게 별도의 집계 계산</strong>을 수행한다.

| LOD 유형 | 문법 | 의미 | 예시 |
|:---|:---|:---|:---|
| **FIXED** | `{FIXED [차원]: 집계}` | 지정 차원 수준에서 고정 계산 | `{FIXED [고객ID]: MIN([주문일])}` |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/670_use_case_include_extend/">INCLUDE</a></strong> | `{INCLUDE [차원]: 집계}` | 현재 뷰 + 추가 차원 포함 | 뷰가 지역 수준이어도 도시 수준 계산 |
| **EXCLUDE** | `{EXCLUDE [차원]: 집계}` | 현재 뷰에서 지정 차원 제외 | 지역 포함 뷰에서 지역 무관 전체 합계 |

**FIXED 사용 사례**: "고객당 첫 구매일을 계산하라"
```
// Tableau Calculated Field
First Order Date = {FIXED [Customer ID]: MIN([Order Date])}
```
→ [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)가 제품·지역·시간 수준이어도 항상 고객 수준으로 집계

**📢 섹션 요약 비유**: LOD 표현식은 <strong>조명 개별 제어 시스템</strong>과 같다. 방 전체 조명([시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 전체 집계)과 무관하게 특정 구역의 조명(FIXED 집계)만 독립적으로 제어할 수 있다.

---

## Ⅲ. 비교 및 연결

### Tableau vs [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) 비교

| 차원 | Tableau | [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a> 유연성</strong> | 높음 — 사용자 정의 차트 풍부 | 중간 — 주요 차트 유형 충분 |
| **계산 언어** | LOD + 테이블 계산 | DAX (강력하나 학습 곡선 있음) |
| **생태계** | Salesforce [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) 통합 강점 | Microsoft 365, Azure 깊은 통합 |
| **가격** | 높음 (Creator ~$70/월) | 낮음 (Pro $[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)/월) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 준비</strong> | Tableau Prep [Builder](/knowledge-base/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/) 별도 | [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Query 내장 |
| **실시간** | Live Connection + Streaming | DirectQuery + [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) Streaming |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 기능</strong> | Ask [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), Tableau Pulse | Q&A, [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Influencers, Decomp Tree |

### Tableau Prep [Builder](/knowledge-base/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/)

Tableau Prep은 <strong>비주얼 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 준비 도구</strong>로, 플로우 캔버스에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클렌징·변환·결합을 시각적으로 수행한다:
- 각 변환 단계의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 미리보기 즉시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- 자동 필드 타입 추론
- 비교 지도([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 불일치 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/))
- Tableau Server와 직접 통합 (게시·[스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/))

**📢 섹션 요약 비유**: Tableau vs [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) BI는 <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">Mac</a> vs Windows</strong>와 같다. [Mac](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(Tableau)은 디자인·유연성이 우수하고, Windows([Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/))는 기업 생태계 통합이 강하다. 어떤 것이 더 좋은지는 조직의 생태계와 목적에 달려있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 테이블 계산(Table Calculation) 활용

| 계산 유형 | 용도 |
|:---|:---|
| Running Total (누적 합계) | 누적 매출 추세 |
| Percent of Total | 전체 대비 비율 |
| Rank | 제품별 순위 |
| Percent Difference | 전년 대비 증감률 |
| Moving Average | 이동 평균 (7일, 30일) |

### Tableau Pulse (2024)

Tableau Pulse는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 스토리텔링 자동화</strong> 기능:
- 자연어로 지표 설명 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
- 이상 감지 자동 알림
- Slack·이메일로 인사이트 자동 배포
- Salesforce Einstein AI와 통합

**📢 섹션 요약 비유**: Tableau Pulse는 <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 애널리스트 보조원</strong>과 같다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보고 "지난주 매출이 전주 대비 15% 하락했으며, 주요 원인은 서울 지역 고객 이탈"이라고 자동으로 리포트를 작성해준다.

---

## Ⅴ. 기대효과 및 결론

### Tableau 도입 효과

| 영역 | 효과 |
|:---|:---|
| **분석 민주화** | SQL 비전문가도 복잡한 분석 가능 |
| **인사이트 속도** | 리포트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시간 80% 단축 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/">데이터 거버넌스</a></strong> | Tableau Server의 중앙 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·접근 제어 |
| **협업** | Tableau Server/Cloud 대시보드 공유 |

### 결론

Tableau는 셀프서비스 분석의 <strong>표준</strong>을 만든 플랫폼이다. VizQL의 직관적 인터페이스와 LOD 표현식의 강력한 계산 능력은 비즈니스 사용자와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가 양측의 요구를 충족한다. [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) BI와 비교 시 비용이 높지만, 복잡한 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 커스터마이징과 분석 유연성이 필요한 조직에서는 Tableau가 더 적합하다.

**📢 섹션 요약 비유**: LOD 표현식을 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터한 Tableau 사용자는 <strong>위상수학을 이해한 지도 제작자</strong>와 같다. 단순히 지도를 그리는 것을 넘어, 어떤 각도에서 어떤 수준으로 봐도 정확한 지형을 계산할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| VizQL | 핵심 기술 | 드래그앤드롭을 DB [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 자동 변환 |
| LOD 표현식 | 차별화 기능 | FIXED/[INCLUDE](/knowledge-base/studynote/04_software_engineering/uncategorized/670_use_case_include_extend/)/EXCLUDE 독립 집계 |
| Live Connection | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모드 | 직접 DB [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), 항상 최신 |
| Extract (.hyper) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모드 | 인메모리 컬럼형, 빠른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| Tableau Prep | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 | 비주얼 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 플로우 캔버스 |
| Tableau Pulse | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기능 | 자동 인사이트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·배포 |
| [Power BI](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) | 경쟁 제품 | Microsoft 생태계 강점, 저렴한 비용 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">:---</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">VizQL</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">LOD 표현식</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Live Connection</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Extract (.hyper)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Tableau Prep</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Tableau Pulse</div></div>
</div>
</div>



이 흐름도는 :---에서 출발해 Tableau Prep까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- Tableau는 <strong>레고 놀이</strong>처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조각을 끌어다 놓으면 자동으로 차트가 만들어지는 도구예요 — 코딩 없이도 복잡한 분석을 할 수 있어요.
- LOD 표현식은 "차트는 지역별로 보여주지만, 계산은 고객별로 해줘"라고 말할 수 있는 마법 주문이에요 — 두 가지 수준을 동시에 다룰 수 있어요.
- Live Connection은 "항상 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보는 것"이고, Extract는 "빠르게 미리 준비해놓은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보는 것"이에요 — 속도와 최신성을 바꿔서 선택하는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 164 / 262

← **이전**: [163. 대시보드 설계 (Dashboard Design) — KPI 중심 5초 규칙 인터랙티브](/knowledge-base/studynote/16_bigdata/08_visualization/163_dashboard_design/)
**다음**: [165. Power BI — Microsoft 생태계 통합 DAX 비즈니스 인텔리전스](/knowledge-base/studynote/16_bigdata/08_visualization/165_power_bi/) →

---
