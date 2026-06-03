+++
title = "101. 정보화 전략 계획 (ISP) 수행 4단계 절차"
date = 2026-04-10

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 계획 (ISP, Information [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Planning)은 조직의 중장기 비즈니스 목표를 달성하기 위해, IT 시스템을 어떻게 구축할 것인지 마스터플랜을 짜는 사전 컨설팅 방법론이다.
> 2. **가치**: 대규모 예산이 투입되는 IT 프로젝트에서 "무엇을 먼저 만들고, 어떻게 통합할 것인가"를 정의하여 중복 투자를 막고 경영진에게 타당성을 설득하는 핵심 근거가 된다.
> 3. **판단 포인트**: 기술적 유행에 휩쓸려 시스템을 설계하는 것을 경계하고, 반드시 '[환경 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/102_environmental_analysis_pest_5forces_value_chain/) $\rightarrow$ [AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 현황 진단 $\rightarrow$ TO-BE 모델 수립 $\rightarrow$ 이행 계획'이라는 정형화된 4단계 절차를 통해 비즈니스와의 정렬(Alignment)을 입증해야 한다.

---

## Ⅰ. 개요 및 필요성

기업이 차세대 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), 클라우드 전환 등 수백억 원 규모의 시스템을 구축할 때, 코딩부터 시작하면 시스템 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 단절되고 현업의 요구사항과 어긋나는 재앙이 발생한다. 이를 방지하기 위해 정보화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 계획 (ISP)이 등장했다. ISP는 IT 인프라와 비즈니스 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 방향을 일치(Align)시키고, 자원의 낭비를 막는 종합적인 청사진 역할을 한다.

과거에는 전산팀이 자의적으로 시스템을 구매했다면, 현재는 비즈니스 모델 혁신을 지원하는 도구로서 IT의 역할이 커지면서 체계적인 ISP 수립이 법적/제도적(공공기관의 경우 필수)으로 강제되고 있다. 이 마스터플랜이 없으면 시스템들은 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/), 부서 이기주의)화되어 유지보수 불가능한 스파게티 구조로 전락하게 된다.

- **📢 섹션 요약 비유**: ISP는 건물을 올리기 전 건축사무소에 의뢰해 조감도를 그리고 지질 검사를 하는 설계 과정이다. 설계도 없이 벽돌부터 쌓으면 1층은 한옥, 2층은 양옥이 되어 결국 무너지게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ISP 수행은 철저하게 논리적인 인과관계를 가진 4단계 폭포수 방법론을 따른다. 환경, 현재, 미래, 실행이라는 4개의 축이 톱니바퀴처럼 맞물려 진행된다.

```text
┌──────────────────────────────────────────────────────────────┐
│                  [ISP 수행 4단계 핵심 프로세스]                  │
├──────────────────────────────────────────────────────────────┤
│ [1. 환경 분석] ───────────▶ [2. AS-IS 분석]                    │
│ 경영 비전 파악 (Business)      현황 진단 (BA, DA, AA, TA)     │
│ IT 트렌드 분석 (IT Trend)      문제점(Pain Point) 도출         │
│          │                           │                       │
│          ▼                           ▼                       │
│ [4. 이행 계획 수립] ◀───────── [3. TO-BE 모델 수립]            │
│ 프로젝트 우선순위 평가         목표 모델 설계 (목표 아키텍처)       │
│ 연도별 로드맵 및 예산 산정      도입 과제 및 솔루션 도출         │
└──────────────────────────────────────────────────────────────┘
```

1단계([환경 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/102_environmental_analysis_pest_5forces_value_chain/))에서 "우리는 어디로 가야 하는가"를 묻고, 2단계([AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 분석)에서 "우리의 현재 꼬라지는 어떠한가"를 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) ([Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/)) 프레임워크에 맞춰 비즈니스, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 애플리케이션, 기술 관점으로 진단한다. 3단계(TO-BE 수립)는 갭(Gap)을 메우기 위한 이상적인 목표 시스템을 그리고 추진 과제를 도출하며, 마지막 4단계(이행 계획)에서 가성비([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/))를 따져 "무엇부터 예산을 투입해 개발할지" 투자 우선순위와 로드맵을 완성한다.

- **📢 섹션 요약 비유**: 건강검진을 받고 체질을 개선하는 과정과 같다. 환자의 목표와 식습관을 묻고(1단계), 피검사와 엑스레이로 현재 질병을 찾아내며(2단계), 이상적인 건강 상태의 수치를 정의한 뒤(3단계), 당장 수술부터 할지 운동부터 할지 연간 치료 일정표를 짜는 것(4단계)이다.

---

## Ⅲ. 비교 및 연결

ISP는 단독으로 존재하지 않으며, 조직의 거대한 뼈대인 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) ([Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/))를 바탕으로, 실제 소프트웨어 개발 생명주기 ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/))의 최상단에서 방향을 제시한다. 

| 비교 영역 | [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/127_bpr_business_process_reengineering_radical_redesign/) (비즈니스 프로세스 재설계) | ISP (정보화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 계획) | [SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/) (소프트웨어 개발 생명주기) |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | 업무 절차 자체의 근본적 혁신 | 비즈니스 지원을 위한 IT 마스터플랜 | 결정된 시스템의 실제 개발 및 테스트 |
| **주요 산출물** | 신규 업무 매뉴얼 및 조직도 | IT 아키텍처(TO-BE) 및 투자 로드맵 | 소스 코드 및 시스템 실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | ISP 수립 전/후에 업무 효율화를 위해 병행 | [BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/127_bpr_business_process_reengineering_radical_redesign/) 결과를 반영하여 IT 청사진 제시 | ISP에서 도출된 개별 과제를 실현 |

특히, 최근에는 업무를 혁신하면서 동시에 IT 밑그림을 그리는 <strong>ISP/<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/127_bpr_business_process_reengineering_radical_redesign/">BPR</a> 통합 방법론</strong>이 널리 쓰인다. 업무 프로세스는 옛날 방식 그대로인데 IT 시스템만 최신으로 바꾸는 모순을 막기 위해서다.

- **📢 섹션 요약 비유**: BPR이 회사의 결재 문서를 수기로 할지 태블릿으로 할지 업무 규칙 자체를 뜯어고치는 것이라면, ISP는 그 태블릿을 언제 수백 대 사고 클라우드는 어떻게 연결할지 예산과 일정을 짜는 기획이며, SDLC는 그 태블릿 안에 들어갈 앱을 실제로 코딩하는 작업이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

ISP는 문서 작업으로 끝날 위험이 크다. 실무와 시험에서 성공적인 ISP를 판단하는 기준은 '실행 가능성'이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **Biz-IT Alignment**: 도출된 IT 과제(TO-BE)가 1단계의 경영 비전과 명확히 연결되어 있는가? (단순 최신 기술 도입은 탈락 사유다.)
2. <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a> 기반 분석</strong>: [AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 진단 시 감에 의존하지 않고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))와 프로세스([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)) 아키텍처를 교차 분석하여 근본 원인을 찾았는가?
3. **현실적 우선순위 평가**: 4단계 이행 계획에서 비즈니스 기여도와 기술적 실현 가능성을 매트릭스로 분석해, ROI가 가장 높은 퀵 윈 (Quick-Win) 과제를 전진 배치했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 경영진이나 현업의 인터뷰 없이 IT 부서 단독으로 신기술([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 등)만 나열한 백화점식 ISP 수립.
- 구체적인 예산 근거와 연도별 추진 일정이 빠져 있어 기획재정부(또는 CFO)의 투자 심사를 통과할 수 없는 추상적인 계획서.

- **📢 섹션 요약 비유**: 완벽한 세계 일주 계획서(ISP)를 짰더라도, 당장 내 지갑에 있는 돈(예산)과 나의 체력(기술 성숙도)을 고려해 가장 먼저 비행기표를 끊을 나라(우선순위)를 정하지 못하면 그 계획서는 쓸모없는 종이 쪼가리에 불과하다.

---

## Ⅴ. 기대효과 및 결론

성공적으로 ISP가 수립되면, IT 부서는 더 이상 '돈만 쓰는 지원 부서'가 아니라 비즈니스 수익 창출을 리드하는 핵심 파트너로 격상된다. 장기적으로는 시스템 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준화와 인프라 통합을 통해 중복 투자가 방지되고, 차세대 시스템 구축 시 리스크가 획기적으로 줄어든다.

최근의 [디지털 트랜스포메이션](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/071_digital_transformation_dx/) ([DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/)) 시대에는 3~5년 단위의 무거운 전통적 ISP 대신, 빠르게 가설을 검증하고 계획을 수정하는 '[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) ([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)) ISP'나 '디지털 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수립(DSP)'으로 진화하고 있다. 하지만 그 형태가 바뀌더라도 현재를 직시하고 미래의 청사진을 그리는 ISP의 핵심 4단계 철학은 모든 대형 IT 프로젝트의 영원한 나침반이다.

- **📢 섹션 요약 비유**: 좋은 ISP는 바다를 항해하는 선장에게 든든한 해도(지도)를 쥐여주는 일이다. 비바람(시장 변화)이 불더라도 배(조직)가 좌초되지 않고 목적지(경영 목표)를 향해 똑바로 나아갈 수 있게 해준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 비즈니스 프로세스 재설계 ([BPR](/knowledge-base/studynote/12_it_management/03_ea_isp/127_bpr_business_process_reengineering_radical_redesign/)) | ISP와 융합되어 업무 혁신과 IT 구축을 동시에 이끄는 방법론 |
| 엔터프라이즈 아키텍처 ([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)) | 조직의 IT 자산을 4가지([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/), [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/), [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)) 관점으로 체계화한 틀 |
| [핵심 성공 요인](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf_critical_success_factor/) ([CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/)) | 1단계 [환경 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/102_environmental_analysis_pest_5forces_value_chain/) 시 현업의 목표를 정량화하는 분석 기법 |
| 투자 대비 효과 ([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/)) | 4단계 이행 계획에서 프로젝트의 우선순위를 결정하는 핵심 재무 지표 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 전산화 (Legacy IT) · 부서별 개별 시스템 구축 (사일로)
    │
    ▼
정보화 전략 계획 (ISP) · 경영 목표와 IT 전략의 4단계 정렬(Align)
    │
    ▼
EA 기반 ISP / BPR 통합 · 아키텍처 관점의 자산 관리 및 업무 절차 동시 혁신
    │
    ▼
디지털 전략 수립 (DSP) · DX 시대의 애자일 기반 신속한 마스터플랜 수립
```

### 👶 어린이를 위한 3줄 비유 설명

1. 멋진 집을 짓기 전에, 가족들이 어떤 방을 원하는지 물어보고 우리 집 재산을 확인하는 게 'ISP'라는 계획표 짜기예요.
2. 그냥 막 벽돌을 쌓으면 집이 무너지니까, 설계도를 그리고(목표 수립) 화장실부터 지을지 거실부터 지을지 순서를 정해요(이행 계획).
3. 이 계획표가 완벽해야 아빠(사장님)가 돈을 내어주고, 모두가 만족하는 튼튼한 성(IT 시스템)을 지을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 587

← **이전**: [101. 정보화 전략 계획 (ISP) 수행 4단계](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_4_steps/)
**다음**: [102. 환경 분석 (Environmental Analysis)](/knowledge-base/studynote/12_it_management/03_ea_isp/102_environmental_analysis_pest_5forces_value_chain/) →

---
