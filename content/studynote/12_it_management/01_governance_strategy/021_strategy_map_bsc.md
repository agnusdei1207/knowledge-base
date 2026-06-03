+++
title = "21. 전략 체계도 (Strategy Map) - BSC 각 관점의 KPI 인과관계를 도식화"
date = 2026-04-02

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Map) - [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) 기반 조직 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 도구

> ⚠️ 이 문서는 조직의 비전과 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 추상적인 구호에서 벗어나, 원인과 결과의 명확한 논리적 연결 고리(Cause-and-Effect Linkage)로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하여 모든 구성원이 동일한 목표를 향해 정렬되도록 돕는 IT 경영 및 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 관리 도구인 '[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도'를 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Map)는 로버트 캐플란과 데이비드 노튼이 창안한 [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/)(Balanced Scorecard, 균형성과표)의 핵심 확장 모듈로, 재무-고객-내부프로세스-학습과 성장의 4가지 관점을 화살표로 연결한 한 장의 '[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 설계도'이다.
> 2. **가치**: "왜 이 IT 시스템을 개발해야 하는가?"에 대한 답을 비즈니스 관점에서 시각적으로 증명한다. 즉, 직원의 역량 강화(학습)가 프로세스 개선을 낳고, 이것이 고객 만족을 거쳐 최종적으로 재무적 이익을 창출하는 경로를 완벽히 가시화한다.
> 3. **융합**: 단독 문서로 끝나지 않고, 하위의 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/)([핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/)), 엔터프라이즈 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)), 그리고 포트폴리오 관리(PPM) 시스템과 융합되어 거대한 기업 조직의 IT 투자가 비즈니스 목표에 100% 정렬(Alignment)되도록 하는 강력한 거버넌스 통제 수단으로 작동한다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

### 1. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Map)의 등장 배경
[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 기존 [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/)(Balanced Scorecard)의 태생적 한계를 극복하기 위해 탄생했습니다. BSC가 조직의 성과를 4가지 관점(재무, 고객, 프로세스, 학습/성장)으로 다각화하여 평가하는 훌륭한 도구였지만, 경영진이 수립한 이 지표들이 "서로 어떤 인과 관계로 얽혀 있는지", "직원들이 현업에서 무엇을 해야 지표가 달성되는지" 설명하는 데는 실패했습니다.

### 2. 해결하고자 하는 문제 (Pain Point: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 실행의 단절)
CEO가 "매출 20% 증가!"라는 재무적 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 발표하면, IT 부서 막내 개발자는 그 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 자신이 오늘 코딩해야 하는 서버 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 작업과 무슨 상관이 있는지 이해하지 못합니다. 이처럼 조직 내 **'[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 단절(Strategic Disconnect)'**이 발생하면, 부서 간 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))가 깊어지고 의미 없는 IT 시스템 개발에 막대한 예산이 낭비됩니다.
- **필요성**: 눈에 보이지 않는 무형의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(Intangible [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 1페이지의 논리적 맵(Map)으로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하여, 말단 직원부터 CEO까지 "나의 오늘 업무가 최종 재무 목표 달성에 어떻게 기여하는지"를 직관적으로 깨닫게 하는 링구아 프랑카(공통어)가 필요했습니다.

- **📢 섹션 요약 비유**: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 "보물섬 지도"와 같습니다. 선장(CEO)이 "보물(매출)을 찾자!"고 외쳐도 지도가 없으면 선원(직원)들은 서로 다른 방향으로 노를 젓습니다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 "오른쪽으로 돌아서 늪(프로세스 개선)을 건너면 열쇠(고객 만족)가 나오고 보물 상자가 열린다"는 것을 1장으로 명확히 그려줍니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) & Mechanism)

### 1. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도의 4대 핵심 아키텍처 ([BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) 4관점 기반)
[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 무작정 그리는 것이 아니라, 반드시 상향식([Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/))의 강력한 인과관계(Cause and Effect) 화살표를 통해 4가지 계층을 관통해야 합니다.

```text
┌─────────────────────────────────────────────────────────────┐
│           [ 전략 체계도(Strategy Map) 핵심 구조 ]               │
│                                                             │
│ ┌─ [ 4. 재무 관점 (Financial Perspective) ] - 주주 가치 창출    │
│ │   [ 생산성 향상 (원가 절감) ]     [ 수익 성장 (신규 시장) ]   │
│ └───────────────────▲─────────────────────────▲───────────────┘ │
│                     │                         │             │
│ ┌─ [ 3. 고객 관점 (Customer Perspective) ] - 고객 가치 제안     │
│ │   [ 저렴한 가격 / 빠른 납기 ]     [ 제품 품질 / 신뢰성 ]      │
│ └─────────▲─────────▲─────────────────────────▲───────────────┘ │
│           │         │                         │             │
│ ┌─ [ 2. 내부 프로세스 관점 (Internal Process) ] - 가치 창출 핵심│
│ │ [운영 관리]  [고객 관리]  [혁신 프로세스]  [규제 및 사회]     │
│ └──────▲────────────▲──────────────▲────────────────▲────────┘ │
│        │            │              │                │       │
│ ┌─ [ 1. 학습과 성장 관점 (Learning & Growth) ] - 무형 자산 기반 │
│ │  [ 인적 자본 (기술/역량) ]   [ 정보 자본 (IT 시스템) ]        │
│ │               [ 조직 자본 (리더십/문화) ]                    │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 아키텍처의 맨 아래 기초 공사인 **학습과 성장(IT 인프라 구축, 개발자 교육)**이 튼튼해야, 그 위층인 **내부 프로세스(빠른 배포, 버그 감소)**가 개선됩니다. 프로세스가 좋아지면 **고객(빠른 응답속도, 만족도 상승)**이 기뻐하고, 최종적으로 가장 위층인 **재무(매출 증가, 유지비 감소)** 목표가 달성되는 완벽한 인과 흐름(Cause-Effect Flow)을 화살표로 증명합니다.

### 2. 가치 제안 (Value Proposition) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)
고객 관점(Layer 3)에서 기업은 모든 것을 다 잘할 수 없습니다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도를 그릴 때 기업은 다음 3가지 가치 제안 중 하나를 명확한 '초점'으로 잡고 내부 프로세스를 정렬해야 합니다.
1. **운영 탁월성 (Operational Excellence)**: 맥도날드나 아마존처럼 압도적인 저원가와 무결점 프로세스 추구.
2. **제품 리더십 (Product Leadership)**: 애플이나 테슬라처럼 혁신적이고 독보적인 최고 품질 제품 제공.
3. **고객 친밀도 ([Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) Intimacy)**: 프라이빗 뱅킹처럼 고객 개인별 맞춤형(Customized) 밀착 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 및 성과 관리 프레임워크 비교

| 비교 항목 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Map) | [OKR](/knowledge-base/studynote/12_it_management/01_governance_strategy/039_okr_objectives_key_results/) (Objectives and [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Results) | [MBO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/025_mbo_management_by_objectives/) (목표 관리) |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | 기업 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 **장기적/논리적 인과관계 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)** 및 정렬 | 빠르고 유연한 **단기 목표 달성 및 도전적 지표 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)** | 개인의 연간 **인사 평가 및 보상 연계** |
| **관점의 다양성** | 재무/고객/프로세스/학습 4대 관점 강제 (균형 중시) | 제한 없음 (팀/조직 목표에 따라 유동적 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)) | 주로 재무 및 정량적 실적 중심 |
| **계층 간 연계** | 상하위 완벽한 인과관계 화살표로 연결 (하향 통제적) | 상위 목표와 하위 [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Result 연결 (수평적/자율적) | 상급자-하급자 간 탑다운 할당 |
| **IT/개발 조직 적합도**| 대규모 차세대 IT 인프라 구축([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)) 등 장기 프로젝트에 적합 | [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)) [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 기반의 잦은 [피벗](/knowledge-base/studynote/12_it_management/01_governance_strategy/037_pivot/)([Pivot](/knowledge-base/studynote/12_it_management/01_governance_strategy/037_pivot/)) 개발 조직에 최적 | 전통적 SI 파견 인력 평가에 쓰임 |

### 트레이드오프 (Trade-off) 심층 분석
[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 장기적인 비전 설계에는 완벽하지만, **유연성과 민첩성을 극도로 희생(Trade-off)**합니다. 한 번 작성된 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도를 수정하려면 전사의 4대 관점 인과관계를 다시 증명하고 맵을 다시 그려야 하므로 무겁고 둔탁합니다. 따라서 트렌드가 1달 단위로 바뀌는 모바일 앱 스타트업 생태계에서는 거대한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Map) 대신 가벼운 OKR로 대체되는 경향이 뚜렷합니다.

- **📢 섹션 요약 비유**: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도가 대성당을 짓기 위해 수십 장의 도면을 그려놓고 "먼저 돌을 깎아야(학습), 기둥이 서고(프로세스), 지붕이 덮인다(재무)"를 증명하는 '장기 건축 설계도'라면, OKR은 텐트를 치며 "이번 주엔 일단 뼈대만 세우자!"라고 빠르게 돌진하는 '단기 작전판'입니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **도입 환경** | 기존 레거시 시스템과의 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 분석 | 마이그레이션 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 및 단계별 전환 계획 수립 |
| **비용([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/))** | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구축 비용(CAPEX) 및 운영 비용(OPEX) | [TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/) 관점의 장기적 효율성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **보안/위험** | 컴플라이언스 준수 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/) | [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 기반 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 체계 연계 |

*(추가 실무 적용 가이드 - IT [정보화 전략 계획](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/) ([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)) 연계)*
- 공공기관이나 대기업이 수백억 원 규모의 차세대 IT 시스템을 발주([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/) 수립)할 때, 기재부나 이사회는 "왜 이 IT 서버를 최신형으로 바꿔야 하는가?"를 묻습니다.
- 이때 단순히 "CPU가 빠릅니다"라는 IT적 대답은 실패합니다. 반드시 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도를 사용하여 **"서버를 업그레이드(정보 자본 확보) -> 주문 처리 프로세스 30% 개선(내부 프로세스) -> 고객 이탈율 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 방어(고객) -> 연매출 50억 원 방어(재무)"**라는 스토리텔링 맵을 그려서 제시해야만 IT 예산 승인을 얻어낼 수 있습니다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 IT 부서의 가장 강력한 예산 방어 무기입니다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. 아무리 비싸고 화려한 이탈리아제 대리석(최신 클라우드 서버)을 사와도, 이것이 전체 건물의 지붕(재무적 목표)을 지탱하는 설계도([전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도) 안에 위치하지 않는다면 단순한 사치일 뿐입니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **동적(Dynamic) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도로의 진화 ([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 및 BI 대시보드 융합)**
   과거의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 파워포인트(PPT)에 그린 정적인 문서였습니다. 하지만 현대의 엔터프라이즈 환경에서는 [Tableau](/knowledge-base/studynote/16_bigdata/08_visualization/164_tableau/), PowerBI와 같은 [비즈니스 인텔리전스](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/282_business_intelligence_bi_technology_framework/)(BI) 툴과 결합하여, 하위 IT 시스템(정보 자본)의 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 에러율([KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/))이 빨간불로 바뀌면 상위 재무 관점의 예상 손실액까지 실시간으로 계산되어 색상이 변하는 '살아 숨 쉬는 동적 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 대시보드'로 진화하고 있습니다.

2. **ESG 경영 목표의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도 내재화 ([Sustainability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/386_sustainability_green_coding/) Map)**
   과거 4대 관점의 최상단은 항상 '재무적 이익(Financial)'이었습니다. 그러나 최근 ESG(환경, 사회, 지배구조) 규제가 강화되면서, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도의 최상단 재무 관점 옆에 **'[지속 가능성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/386_sustainability_green_coding/) 및 사회적 책임 관점'**이 동등한 계층으로 추가되거나 아예 꼭대기로 올라가는 아키텍처적 패러다임 전환이 일어나고 있습니다.

3. **엔터프라이즈 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)) 프레임워크와의 완벽한 융합**
   [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도의 '정보 자본' 영역은 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)([Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/))의 [비즈니스 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)), [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)), [애플리케이션 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)), [기술 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))와 직접적으로 매핑됩니다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도에서 그은 선 하나가 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 시스템의 코드와 인프라 구성도로 자동 치환되는 통합 거버넌스 툴링 발전이 가속화되고 있습니다.

- **📢 섹션 요약 비유**: 미래의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 종이 위에 그려진 정지된 지도가 아니라, "실시간 교통 상황(시장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))과 내 차의 연료 상태(IT 인프라)를 스스로 분석해 목적지(재무 목표)까지 가장 빠른 길을 계속 바꿔주는 자율주행 내비게이션"으로 완성될 것입니다.

---

## 🧠 지식 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

*   **성과 관리 프레임워크 ([Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))**
    *   [MBO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/025_mbo_management_by_objectives/) (전통적 목표 관리)
    *   **[BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) (균형성과표) -> [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) Map)로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)**
    *   [OKR](/knowledge-base/studynote/12_it_management/01_governance_strategy/039_okr_objectives_key_results/) ([애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 시대의 유연한 목표 관리)
*   **[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도 4대 관점 (인과관계: [Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/))**
    *   재무 관점 (Financial) <- 최종 목적지
    *   고객 관점 ([Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/))
    *   내부 프로세스 관점 (Internal Business [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))
    *   학습과 성장 관점 ([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) & Growth) <- 무형 자산 (IT, 조직문화)
*   **IT 거버넌스 연계 도구**
    *   [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/) ([정보화 전략 계획](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)) 타당성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
    *   [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) (엔터프라이즈 아키텍처)의 [BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)(Business [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/)) 영역

---

### 📈 관련 키워드 및 발전 흐름도

```text
[MBO (목표에 의한 관리 — 단순 재무 목표 중심)]
    │
    ▼
[BSC (Balanced Scorecard — 재무·고객·프로세스·학습 4관점)]
    │
    ▼
[전략 체계도 (Strategy Map — BSC의 인과관계 시각화)]
    │
    ▼
[KPI 대시보드 연계 — 실시간 목표 달성 모니터링]
    │
    ▼
[OKR (애자일 목표 관리) + AI 기반 동적 전략 조정]
```
BSC는 단순 재무 지표의 한계를 극복해 4관점의 균형을 맞추며, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 각 관점 간의 인과관계를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)해 IT [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 비즈니스 목표와 일치하도록 연결한다.

### 👶 어린이를 위한 3줄 비유 설명
1. BSC는 축구팀을 평가할 때 "골 개수(재무)"만 보지 않고, 팬 만족도(고객)·훈련 방식(프로세스)·선수 성장(학습)까지 균형 있게 보는 성적표예요!
2. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 체계도는 "선수들이 체력을 키우면(학습) → 수비가 강해지고(프로세스) → 실점이 줄어 팬들이 좋아하고(고객) → 우승·수익이 올라간다(재무)" 처럼 원인과 결과를 그림으로 연결한 지도예요.
3. 이 지도가 있으면 IT 시스템 예산을 어디에 써야 회사 목표에 가장 도움이 되는지 한눈에 알 수 있답니다!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/):** 본 문서는 구조적 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 및 작성되었습니다. (Verified at: 2026-04-02)

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 36 / 587

← **이전**: [21. 전략 체계도 (Strategy Map)](/knowledge-base/studynote/12_it_management/01_governance_strategy/021_strategy_map/)
**다음**: [22. 가치 사슬 (Value Chain)](/knowledge-base/studynote/12_it_management/01_governance_strategy/022_value_chain/) →

---
