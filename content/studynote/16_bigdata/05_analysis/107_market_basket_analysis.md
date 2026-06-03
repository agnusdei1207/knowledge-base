+++
title = "104. 장바구니 분석 (Market Basket Analysis) — 구매 패턴 기반 교차 판매"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 장바구니 분석 (Market Basket Analysis)은 고객이 한 번의 쇼핑에서 함께 구매하는 상품 조합을 분석하여 숨겨진 구매 패턴을 발굴하는 [데이터 마이닝](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/284_data_mining_association_classification_clustering_crisp_dm/) 기법이다.
> 2. **가치**: [연관 규칙](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/) ([Association Rules](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/))으로 발굴된 패턴은 매장 진열 최적화, 교차 판매 (Cross-Selling), 번들 프로모션, 온라인 추천 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 직접적 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 된다.
> 3. **판단 포인트**: 리테일을 넘어 웹 클릭스트림, 의료 공동 진단, 금융 이상 거래로 확장 적용 가능하며, 비즈니스 목적에 따라 [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)·[신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)·[향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) 임계값을 다르게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다.

---

## Ⅰ. 개요 및 필요성

1990년대 미국 슈퍼마켓 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 발견된 "금요일 저녁에 기저귀와 맥주가 함께 팔린다"는 패턴은 장바구니 분석의 역사적 상징이다. 오프라인 POS (Point of Sale) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 시작된 이 분석은 이제 온라인 쇼핑 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 스트리밍 시청 이력, 병원 처방 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 적용 범위를 넓혔다.

빅데이터 시대에 하루 수천만 건의 거래를 처리하는 이커머스 플랫폼에서는, 인간이 수작업으로 패턴을 발견하는 것이 불가능하다. 자동화된 장바구니 분석이 교차 판매 추천 엔진의 핵심 인프라가 된 이유다.

- **📢 섹션 요약 비유**: 장바구니 분석은 수백만 명의 영수증을 한꺼번에 읽고 "늘 같이 장을 보러 다니는 물건 친구들"을 찾아내는 탐정 작업이다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장바구니 분석 전체 파이프라인</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 수집</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">POS 거래 로그 / 온라인 주문 DB / 클릭스트림</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거래 ID 기준 그룹핑 → 항목 집합 (Itemset) 변환</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이상치 제거 (반품 거래, 테스트 주문 등)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">빈발 항목 집합 마이닝</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Apriori / FP-Growth (Frequent Pattern Growth)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ min_support 적용 → 빈발 항목 집합 추출</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">규칙 생성 및 평가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Support ≥ 0.01 Confidence ≥ 0.5 Lift ≥ 1.5</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">비즈니스 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">진열 배치</div><div class="kb-diagram-cell">추천 엔진</div><div class="kb-diagram-cell">번들 프로모션</div></div>
</div>
</div>



### 핵심 지표 해석 가이드

| 지표 | 낮은 경우 의미 | 높은 경우 의미 | 적정 임계값(리테일) |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/">지지도</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/">Support</a>)</strong> | 드물게 발생 | 자주 함께 구매 | ≥ 0.01 (1%) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/">신뢰도</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/">Confidence</a>)</strong> | A 구매 후 B 구매 드묾 | A 구매 시 B 거의 확실 | ≥ 0.50 (50%) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/">향상도</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/">Lift</a>)</strong> | 우연보다 낮거나 동일 | 강한 양의 연관 | ≥ 1.5 |
| **레버리지 (Leverage)** | 기대보다 낮은 공동 출현 | 기대 초과 공동 출현 | > 0 |

### 확장 적용 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 거래([Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)) | 항목(Item) | 활용 |
|:---|:---|:---|:---|
| 리테일 | 구매 영수증 | 상품 SKU | 진열, 번들, 추천 |
| 웹 분석 | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 방문 URL | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 추천, 메뉴 설계 |
| 의료 | 환자 내원 | 진단 코드 (ICD) | 공동 이환 패턴 |
| 금융 | 계좌 거래 | 거래 유형 | 이상 거래 탐지 |
| 스트리밍 | 시청 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 콘텐츠 ID | 다음 시청 추천 |

- **📢 섹션 요약 비유**: 장바구니 분석의 세 지표는 "얼마나 자주([지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/))", "얼마나 확실하게([신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/))", "우연보다 얼마나 더([향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/))"를 각각 답해준다. 세 질문 모두에 "예"일 때 비로소 가치 있는 패턴이다.

---

## Ⅲ. 비교 및 연결

| 항목 | 장바구니 분석 | [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) (CF) | [콘텐츠 기반 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/346_content_based_filtering/) |
|:---|:---|:---|:---|
| **개인화** | 없음 (집단 패턴) | 있음 (유사 사용자 기반) | 있음 (아이템 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반) |
| **설명 가능성** | 높음 (규칙이 명시적) | 낮음 (잠재 요인) | 중간 ([속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a></strong> | 없음 (거래만 있으면 됨) | 있음 (신규 사용자/아이템) | 아이템 콜드스타트 없음 |
| **계산 복잡도** | 아이템 수에 지수적 | 사용자×아이템 행렬 | 아이템 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 수 |
| **적용 사례** | 진열, 번들 | 넷플릭스, 쿠팡 | 음악 추천, 뉴스 추천 |

장바구니 분석과 [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 서로 보완적이다. 장바구니 분석으로 발굴한 고신뢰도 규칙을 [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) 모델의 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)로 활용하거나, 추천 결과의 다양성을 보완하는 데 [연관 규칙](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/)을 적용할 수 있다.

- **📢 섹션 요약 비유**: 장바구니 분석은 "모든 손님에게 통하는 황금 조합"을 찾고, [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 "당신과 비슷한 손님이 좋아한 것"을 찾는다. 두 방법을 함께 쓰면 더 강력한 추천이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 오프라인 매장 적용

- **교차 진열**: {맥주, 안주} [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/)=3.2 → 맥주 냉장고 옆에 안주 코너 배치
- **체크아웃 구역**: 고신뢰도 소액 아이템을 계산대 근처 배치 (충동구매 유도)
- **번들 프로모션**: {샴푸, 린스} [Support](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)=0.15 → 묶음 할인 상품 구성

### 온라인 이커머스 적용

- **"함께 구매한 상품" 위젯**: 실시간 장바구니 기반 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth 실행
- **이메일 리타겟팅**: 특정 상품 구매 후 [연관 규칙](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/)에 따른 후속 상품 추천

### 기술사 주의사항

1. <strong>희소 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 문제</strong>: 롱테일 상품은 [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)가 극히 낮아 규칙 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 불가 → 카테고리 단위로 집계 후 분석
2. **계절성 대응**: 분기별·이벤트별로 별도 모델 운영 (여름 자외선차단제 ≠ 겨울 핫초코)
3. **인과 혼동 방지**: 높은 Lift가 인과관계를 의미하지 않음 → 비즈니스 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 필수
4. **규칙 폭발 문제**: min_support를 너무 낮게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 시 수만 개 규칙 발생 → 사후 필터링 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 필요

- **📢 섹션 요약 비유**: 장바구니 분석 결과는 지도일 뿐, 실제 길을 내는 것은 비즈니스 판단이다. 지도가 정확해도 목적지가 틀리면 의미가 없다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 구체적 내용 |
|:---|:---|
| 매출 증가 | 교차 판매로 평균 주문금액 (AOV, Average Order Value) 15~25% 향상 |
| 재고 최적화 | 함께 팔리는 상품의 재고를 연동 관리 |
| 고객 경험 개선 | 맥락에 맞는 추천으로 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) 단축 |
| 매장 운영 효율 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 진열로 시행착오 비용 절감 |
| 프로모션 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 향상 | 연관 상품 번들 캠페인의 전환율 개선 |

장바구니 분석은 단순해 보이지만 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 말하게 하는" 가장 직관적이고 설명 가능한 분석이다. 딥러닝 기반 블랙박스 추천과 달리 비즈니스 담당자가 결과를 이해하고 의사결정에 직접 연결할 수 있다는 것이 최대 강점이다. 빅데이터 환경에서는 Spark FPGrowth로 수천만 거래를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리하면서도 실시간에 가까운 분석이 가능해졌다.

- **📢 섹션 요약 비유**: 장바구니 분석의 가장 큰 힘은 "왜"를 설명할 수 있다는 것이다. AI가 "이것을 추천해"라고 말할 때, "왜냐하면 이 상품과 함께 산 고객이 60%나 되기 때문"이라는 근거를 제시할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [연관 규칙](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/) ([Association Rules](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/)) | 장바구니 분석의 핵심 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 기반 |
| [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth | 대용량 장바구니 분석의 표준 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)/[신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)/[향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) | 규칙 품질 평가 3대 지표 |
| [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) ([Collaborative Filtering](/knowledge-base/studynote/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start/)) | 개인화 추천으로 확장 시 연계 |
| POS (Point of Sale) | 장바구니 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 주요 수집 원천 |
| SKU (Stock-Keeping Unit) | 리테일 상품 단위 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |
| 교차 판매 (Cross-Selling) | 장바구니 분석의 핵심 비즈니스 적용 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">장바구니 데이터 (POS 트랜잭션 — 판매 기록)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">연관 규칙 (Association Rules) — 지지도/신뢰도/향상도</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Apriori 알고리즘 — 빈발 항목집합 (Frequent Itemset)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">FP-Growth — 대용량 패턴 마이닝</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">협업 필터링 (Collaborative Filtering) — 개인화 추천</div></div>
</div>
</div>



장바구니 분석이 단순 빈도 패턴 탐색에서 대용량 마이닝과 개인화 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)으로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
- 장바구니 분석은 마트 직원이 수백만 개의 영수증을 보고 "항상 같이 팔리는 물건이 뭐야?"를 찾는 것이에요.
- "치약 사면 칫솔도 거의 꼭 사네" 하는 패턴을 찾으면, 두 물건을 나란히 진열하는 거예요.
- 컴퓨터가 이 일을 대신 해주니까, 우리가 미처 몰랐던 숨겨진 조합도 금방 발견할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 107 / 262

← **이전**: [103. 연관 규칙 (Association Rules) — Apriori/FP-Growth 장바구니 분석](/knowledge-base/studynote/16_bigdata/05_analysis/106_association_rules/)
**다음**: [105. 감성 분석 (Sentiment Analysis) — 긍부정 감정 자동 분류](/knowledge-base/studynote/16_bigdata/05_analysis/108_sentiment_analysis/) →

---
