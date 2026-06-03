+++
title = "103. 연관 규칙 (Association Rules) — Apriori/FP-Growth 장바구니 분석"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 연관 규칙 (Association Rules)은 대규모 거래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 "A를 사면 B도 산다"처럼 항목 간의 공동 출현 패턴을 자동으로 발굴하는 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) 기법이다.
> 2. **가치**: [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) ([Support](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)), [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) ([Confidence](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)), [향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) ([Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/)) 세 지표를 조합하면 우연적 동시 구매와 진짜 의미 있는 구매 연관성을 구분할 수 있어, 진열 배치·교차 판매·프로모션 설계의 근거 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 된다.
> 3. **판단 포인트**: Apriori는 구현이 단순하지만 후보 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용이 크고, [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth (Frequent Pattern Growth)는 메모리 내 트리 구조로 스캔 횟수를 획기적으로 줄여 수백만 SKU (Stock-Keeping Unit) 규모에서도 실용적이다.

---

## Ⅰ. 개요 및 필요성

마트에서 기저귀를 사는 고객이 맥주도 함께 산다는 사례는 연관 규칙 분석의 상징적 발견이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 스스로 숨겨진 구매 패턴을 드러낸다는 이 아이디어는 리테일을 넘어 의료 공동 진단, 금융 이상 거래, 웹 [클릭스트림 분석](/knowledge-base/studynote/16_bigdata/05_analysis/120_clickstream_analysis/)으로 확장됐다.

수천만 건의 거래 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 사람이 직접 훑어 패턴을 찾는 것은 불가능하다. 연관 규칙 마이닝은 [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) 임계값으로 탐색 공간을 선제적으로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하고, 통계 지표로 의미 있는 규칙만 필터링함으로써 이 탐색을 자동화한다.

- **📢 섹션 요약 비유**: 연관 규칙은 거대한 슈퍼마켓 영수증 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)에서 "어떤 물건들이 항상 함께 담겨 있는가"를 찾아주는 자동 탐정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 지표

| 지표 | 수식 | 의미 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/">지지도</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/">Support</a>)</strong> | P(A ∩ B) | 전체 거래 중 A와 B가 함께 등장하는 비율 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/">신뢰도</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/">Confidence</a>)</strong> | P(B\|A) = P(A ∩ B)/P(A) | A가 있을 때 B가 같이 있을 [조건부 확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/">향상도</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/">Lift</a>)</strong> | [Confidence](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) / P(B) | 우연보다 얼마나 더 자주 함께 나타나는가 (>1 이면 양의 연관) |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">연관 규칙 마이닝 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거래 DB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T1: {우유, 빵, 버터}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T2: {맥주, 기저귀, 콜라} Step 1: 빈발 항목 집합 생성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T3: {우유, 기저귀, 맥주, 콜라} ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T4: {빵, 우유} min_support 임계값 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">빈발 항목 집합 (Frequent Itemsets)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{맥주, 기저귀}: support=0.4</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{맥주, 콜라}: support=0.3 Step 2: 규칙 생성 &amp; 필터링</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{기저귀, 콜라}: support=0.3 ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">min_confidence 임계값 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">최종 규칙</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{기저귀} → {맥주} conf=0.80, lift=2.1 ✅ 의미 있음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">{빵} → {우유} conf=0.67, lift=1.3 ✅ 의미 있음</div></div>
</div>
</div>



### Apriori vs [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth

| 항목 | Apriori | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth (Frequent Pattern Growth) |
|:---|:---|:---|
| **핵심 아이디어** | 후보 항목 집합 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 후 스캔 반복 | DB를 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Tree로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 후보 없이 마이닝 |
| **DB 스캔 횟수** | 아이템 수 k번 반복 | 2회 (트리 구성 + 마이닝) |
| **메모리 사용** | 낮음 | 높음 (트리 전체 메모리 적재) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 아이템 종류 많을수록 급격히 느려짐 | 대용량에서 압도적 우위 |
| **구현 복잡도** | 단순 | 복잡 |

- **📢 섹션 요약 비유**: Apriori는 도서관에서 한 권씩 모든 책 조합을 찾는 방식이고, [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth는 목차(트리)를 먼저 만들어놓고 거기서만 검색하는 방식이다.

---

## Ⅲ. 비교 및 연결

연관 규칙은 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 패턴 발굴 관점에서 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)와 유사하지만, 목적이 다르다. [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트를 그룹으로 나누는 것"이고, 연관 규칙은 "항목 간의 if-then 의존 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 찾는 것"이다.

| 항목 | 연관 규칙 | [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) ([Collaborative Filtering](/knowledge-base/studynote/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start/)) |
|:---|:---|:---|
| **입력** | 거래 단위 항목 집합 | 사용자-아이템 평점 행렬 |
| **출력** | {A} → {B} 규칙 | 사용자별 추천 항목 |
| **개인화** | 없음 (집단 패턴) | 있음 (개인 선호 반영) |
| **설명 가능성** | 높음 (규칙 명시적) | 낮음 (잠재 요인 기반) |
| **적용 사례** | 진열 배치, 번들 프로모션 | 넷플릭스·유튜브 추천 |

Spark MLlib의 FPGrowth, Python mlxtend [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 대표적 구현체다. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)별로 로컬 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Tree를 만든 뒤 결과를 병합하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 사용된다.

- **📢 섹션 요약 비유**: 연관 규칙은 "모든 손님이 공통으로 선택하는 조합"을 찾고, [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/)은 "당신과 비슷한 손님이 좋아한 것"을 찾는다. 둘은 같은 상점에서 다른 질문에 답한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. **리테일 진열 최적화**: [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) > 2.0인 {A, B} 쌍을 인접 진열하여 교차 구매율 향상
2. **의료 공동 진단**: 전자 의무 기록 (EMR, Electronic Medical Record)에서 함께 나타나는 질환 조합 탐지 → 조기 스크리닝 가이드
3. **금융 이상 패턴**: 특정 거래 항목 조합이 사기 거래에 빈발하는지 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링

### 기술사 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. min_support와 min_confidence 임계값은 비즈니스 의미를 기반으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)했는가? (너무 낮으면 규칙이 수천 개, 너무 높으면 의미 있는 규칙 누락)
2. [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) = 1 에 가까운 규칙은 우연적 동시 출현이므로 제거했는가?
3. 계절성 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라면 기간을 나눠 규칙을 비교했는가? (여름 vs 겨울 장바구니 패턴이 다름)
4. 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라면 Apriori 대신 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth 또는 Spark FPGrowth를 선택했는가?

- **📢 섹션 요약 비유**: Lift는 우연을 보정하는 나침반이다. [향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/)가 1.0이면 "우연히 함께 있는 것"이고, 3.0이면 "분명한 이유가 있어서 함께 있는 것"이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 교차 판매율 향상 | 연관 상품 추천으로 평균 장바구니 금액 증가 |
| 진열 최적화 | 높은 [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) 쌍을 인접 배치, 동선 설계 개선 |
| 프로모션 번들링 | [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) 높은 조합으로 묶음 할인 설계 |
| 이상 패턴 감지 | 금융/의료에서 비정상적 조합 조기 탐지 |
| 자동화 인사이트 | 수백만 SKU에서 사람이 발견 못 할 패턴 자동 발굴 |

연관 규칙 마이닝은 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 스스로 말하게 하는" 탐색적 분석의 정수다. [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)로 공간을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하고, [향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/)로 우연을 걸러내는 두 단계의 필터링이 이 기법의 실용성을 보증한다. 빅데이터 시대에는 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리가 표준이 되고 있으며, 단순 리테일을 넘어 헬스케어·사이버보안·금융 사기 탐지로 영역이 확장되고 있다.

- **📢 섹션 요약 비유**: 연관 규칙은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 속에 숨어있는 "자주 다니는 이웃 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)"를 지도로 그려주는 기술이다. 지도가 있어야 길을 설계할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| 빈발 항목 집합 (Frequent Itemset) | 연관 규칙 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)의 전 단계 |
| Apriori 원리 (Apriori Principle) | 빈발하지 않은 항목의 상위 집합도 빈발하지 않음 |
| [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Tree | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth의 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조, DB [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 저장 |
| [지지도](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/)/[신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)/[향상도](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) | 규칙 평가 3대 지표 |
| [Spark MLlib](/knowledge-base/studynote/16_bigdata/03_spark/062_spark_mllib/) FPGrowth | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경 대용량 구현체 |
| [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) ([Collaborative Filtering](/knowledge-base/studynote/14_data_engineering/04_mlops/186_graph_db_recommendation_collaborative_filtering_cold_start/)) | 개인화 추천으로 확장 시 연계 |
| [장바구니 분석](/knowledge-base/studynote/16_bigdata/05_analysis/107_market_basket_analysis/) ([Market Basket Analysis](/knowledge-base/studynote/16_bigdata/05_analysis/107_market_basket_analysis/)) | 연관 규칙의 대표 응용 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 마이닝</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">연관 규칙</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Apriori 알고리즘</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">FP-Growth</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">협업 필터링</div></div>
</div>
</div>



[데이터 마이닝](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/284_data_mining_association_classification_clustering_crisp_dm/)의 빈발 패턴 탐색이 연관 규칙과 Apriori를 거쳐 더 효율적인 [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth 및 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)으로 발전하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
- 연관 규칙은 "친구들이 항상 같이 다니는 패턴"을 수학으로 찾아내는 것이에요.
- Apriori는 모든 친구 조합을 하나씩 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)-Growth는 친구 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)도를 먼저 그려서 더 빠르게 찾아요.
- "치약을 사면 칫솔도 산다"처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 사람 대신 유용한 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)를 알려주는 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 106 / 262

← **이전**: [군집화 (Clustering) 분석](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)
**다음**: [104. 장바구니 분석 (Market Basket Analysis) — 구매 패턴 기반 교차 판매](/knowledge-base/studynote/16_bigdata/05_analysis/107_market_basket_analysis/) →

---
