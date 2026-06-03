---
title: 520. 데이터 마이닝 KDD 프로세스와 연관 규칙 (Data Mining KDD Process Association Rules)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[225_kdd_t_test_anova_statistical_analysis|KDD]](Knowledge Discovery in Databases) 프로세스는 원시 [[001_dikw_pyramid|데이터]]에서 유용한 지식을 발굴하는 단계적 절차이며, CRISP-DM(CRoss-Industry Standard [[300_process|Process]] for [[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]])은 이를 비즈니스 맥락에서 실용화한 산업 표준 방법론이다.
> 2. **가치**: [[106_association_rules|연관 규칙]]([[106_association_rules|Association Rules]])은 [[084_support_association_rule_transaction|지지도]]([[084_support_association_rule_transaction|Support]])·[[085_confidence_association_rule_conditional_probability|신뢰도]]([[085_confidence_association_rule_conditional_probability|Confidence]])·[[086_lift_association_rule_marketing|향상도]]([[086_lift_association_rule_marketing|Lift]])의 세 지표로 규칙 품질을 평가하며, Apriori보다 메모리 효율적인 FP-Growth가 대규모 [[107_market_basket_analysis|장바구니 분석]]의 실무 표준이다.
> 3. **판단 포인트**: [[086_lift_association_rule_marketing|Lift]] > 1이면 양의 연관, [[086_lift_association_rule_marketing|Lift]] = 1이면 독립, [[086_lift_association_rule_marketing|Lift]] < 1이면 음의 연관 — [[085_confidence_association_rule_conditional_probability|신뢰도]] 높지만 [[086_lift_association_rule_marketing|Lift]] ≈ 1인 규칙은 아이템의 인기도에 불과하므로 반드시 [[086_lift_association_rule_marketing|향상도]]를 함께 확인해야 한다.

---

## Ⅰ. 개요 및 필요성

[[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]]([[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]])은 대용량 [[001_dikw_pyramid|데이터]]에서 통계·기계학습·패턴 인식 기술을 통해 의미 있는 패턴, 규칙, 지식을 발굴하는 분석 과정이다.

### [[225_kdd_t_test_anova_statistical_analysis|KDD]] vs CRISP-DM 비교

| 단계 | [[225_kdd_t_test_anova_statistical_analysis|KDD]] | CRISP-DM |
|:---|:---|:---|
| 1 | [[001_dikw_pyramid|데이터]] 선택 ([[022_mcts_four_stages|Selection]]) | 비즈니스 이해 |
| 2 | 전처리 (Preprocessing) | [[001_dikw_pyramid|데이터]] 이해 |
| 3 | 변환 (Transformation) | [[001_dikw_pyramid|데이터]] 준비 |
| 4 | 마이닝 (Mining) | 모델링 |
| 5 | 해석/평가 (Evaluation) | 평가 |
| 6 | — | 배포 ([[087_deployment_kubernetes_workload_rolling_update|Deployment]]) |

**차이점**: KDD는 학술 중심 선형 프로세스, CRISP-DM은 순환적(Iterative) 비즈니스 프로세스 — 평가 단계에서 비즈니스 이해로 되돌아가는 반복 구조.

- **📢 섹션 요약 비유**: KDD는 원석을 캐는 광산 작업의 전체 공정표이고, CRISP-DM은 "고객이 원하는 보석은 무엇인가?"부터 물어보는 비즈니스 마인드의 광산 프로젝트 관리 방법이야.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[106_association_rules|연관 규칙]] 세 지표

```
트랜잭션 예시: {우유, 빵, 기저귀, 맥주}

연관 규칙: {기저귀} → {맥주}

지지도(Support):
  P({기저귀, 맥주}) = 기저귀와 맥주 함께 구매 / 전체 트랜잭션

신뢰도(Confidence):
  P({맥주} | {기저귀}) = 기저귀,맥주 동시 구매 / 기저귀 구매

향상도(Lift):
  Confidence / P({맥주}) = 신뢰도 / 맥주 단독 구매 비율
  > 1: 양의 연관  = 1: 독립  < 1: 음의 연관
```

### Apriori vs FP-Growth 비교

| 기준 | Apriori | FP-Growth |
|:---|:---|:---|
| [[001_algorithm_definition|알고리즘]] | 후보 [[087_process_state_transition|생성]] + 빈도 검색 (너비 우선) | FP-Tree [[347_compaction|압축]] 구조 직접 탐색 |
| [[002_database_definition|데이터베이스]] 스캔 | 매 단계 전체 스캔 | 2회 (트리 구축 + 탐색) |
| 메모리 효율 | 낮음 (후보 폭발 문제) | 높음 |
| 속도 | 느림 (대규모) | 빠름 |
| 구현 단순성 | 단순 | 복잡 |

**Apriori의 반단조성(Anti-Monotonicity) 원리**: [[084_support_association_rule_transaction|지지도]] ≥ 최솟값인 집합의 부분 집합도 반드시 [[084_support_association_rule_transaction|지지도]] ≥ 최솟값 → 최솟값 미만 집합의 확장을 조기 [[435_pruning_hardware|가지치기]]([[435_pruning_hardware|Pruning]]).

- **📢 섹션 요약 비유**: Apriori는 모든 가능한 아이템 조합을 하나씩 살펴보는 것이고, FP-Growth는 먼저 "자주 같이 사는 것들"을 트리로 [[347_compaction|압축]]해서 나중에 한 번에 빠르게 탐색하는 지름길이야.

---

## Ⅲ. 비교 및 연결

### [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] 기법 [[104_classification_analysis|분류]]

| 목적 | 기법 | 활용 |
|:---|:---|:---|
| [[104_classification_analysis|분류]] ([[107_classification|Classification]]) | 의사 결정 트리, [[238_svm_margin_kernel_trick_naive_bayes|SVM]], [[353_random_forest|랜덤 포레스트]] | 고객 이탈 예측 |
| [[105_clustering_analysis|군집화]] ([[105_clustering_analysis|Clustering]]) | K-Means, [[351_dbscan_density_based_clustering|DBSCAN]], 계층적 | 고객 세분화 |
| 연관 (Association) | Apriori, FP-Growth | [[107_market_basket_analysis|장바구니 분석]] |
| [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] ([[530_anomaly|Anomaly]]) | [[195_isolation_concurrency_control|Isolation]] Forest, OCSVM | 사기 탐지 |
| 순차 패턴 (Sequential) | PrefixSpan, GSP | 클릭 시퀀스 분석 |

### 연속 규칙 vs 시퀀스 패턴

- **[[106_association_rules|연관 규칙]]**: 순서 무관 — "기저귀와 맥주는 함께 산다."
- **순차 패턴(Sequential Pattern)**: 순서 고려 — "상품 A 구매 후 7일 내 상품 B 구매."
- **활용**: 전자상거래 구매 여정(Journey) 분석, 의료 치료 순서 최적화.

- **📢 섹션 요약 비유**: [[106_association_rules|연관 규칙]]은 "같은 장바구니에 담기는 물건들의 규칙"이고, 순차 패턴은 "어떤 물건을 산 다음에 무엇을 사는가"의 시간 흐름까지 본 거야. 마트 진열대 배치와 이메일 마케팅 타이밍에 각각 쓰여.

---

## Ⅳ. 실무 적용 및 기술사 판단

**시나리오 - 슈퍼마켓 [[107_market_basket_analysis|장바구니 분석]]**:
- 100만 건 [[191_transaction_concept_states|트랜잭션]], 5,000개 아이템.
- 최소 [[084_support_association_rule_transaction|지지도]] 0.01 (1%), 최소 [[085_confidence_association_rule_conditional_probability|신뢰도]] 0.3 (30%).
- FP-Growth 적용 → 스캔 2회, Apriori 대비 8배 빠른 처리.
- 규칙 발굴: {기저귀, 분유} → {아기 물티슈}, [[084_support_association_rule_transaction|Support]]=0.023, [[085_confidence_association_rule_conditional_probability|Confidence]]=0.67, [[086_lift_association_rule_marketing|Lift]]=3.4.
- [[086_lift_association_rule_marketing|Lift]]=3.4 → 기저귀+분유 구매자가 아기 물티슈를 구매할 확률이 일반 고객 대비 3.4배 → 매장 진열 위치 변경 → 해당 카테고리 매출 22% 증가.

**지표 함정 경고**:
- {우유} → {빵}: [[085_confidence_association_rule_conditional_probability|Confidence]]=0.75, [[086_lift_association_rule_marketing|Lift]]=1.02 → 빵의 전체 구매율이 73%로 높기 때문에 의미 없는 규칙.
- Lift가 1에 가까우면 규칙을 사용하지 않는 것이 낫다.

**기술사 판단 포인트**:
- 최솟값 임계 [[009_config|설정]]: 너무 낮으면 규칙 폭발, 너무 높으면 유용한 규칙 누락 → [[064_relation_domain|도메인]] 전문가 협업 필수.
- 대규모 처리: Spark MLlib의 FP-Growth [[136_variance|분산]] 처리로 수억 건 [[191_transaction_concept_states|트랜잭션]] 처리 가능.

- **📢 섹션 요약 비유**: [[086_lift_association_rule_marketing|향상도]]([[086_lift_association_rule_marketing|Lift]])는 규칙의 진짜 가치를 알려주는 지표야. 빵이 워낙 많이 팔리니까 "우유를 사면 빵도 산다"는 규칙은 사실 별로 유용하지 않아. Lift가 1보다 훨씬 커야 진짜 유용한 규칙이야.

---

## Ⅴ. 기대효과 및 결론

[[225_kdd_t_test_anova_statistical_analysis|KDD]]/CRISP-DM 프로세스와 [[106_association_rules|연관 규칙]] 마이닝의 체계적 적용은 [[001_dikw_pyramid|데이터]]에 숨겨진 패턴을 발굴해 마케팅·재고 관리·개인화 서비스의 효율을 높인다.

- **매출 최적화**: 교차 판매(Cross-Selling) 기회 발굴 → 객단가 증가.
- **재고 배치 개선**: 자주 함께 구매되는 아이템의 물리적 근접 배치 → 구매 편의성 향상.
- **마케팅 자동화**: 구매 시퀀스 기반 맞춤형 프로모션 타이밍 최적화.

- **📢 섹션 요약 비유**: [[106_association_rules|연관 규칙]] 마이닝은 쇼핑몰의 [[933_cctv|CCTV]] 영상 대신 영수증 [[001_dikw_pyramid|데이터]]로 "손님들이 어떤 물건을 함께 사는지"의 숨겨진 법칙을 찾아내서 매장 운영에 활용하는 탐정 작업이야.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[225_kdd_t_test_anova_statistical_analysis|KDD]] | CRISP-DM, [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] 절차 · 분석 방법론 |
| Apriori | 반단조성, [[084_support_association_rule_transaction|지지도]] [[435_pruning_hardware|가지치기]] · 소규모 규칙 탐색 |
| FP-Growth | FP-Tree, 메모리 효율 · 대규모 장바구니 |
| [[084_support_association_rule_transaction|Support]]/[[085_confidence_association_rule_conditional_probability|Confidence]]/[[086_lift_association_rule_marketing|Lift]] | 규칙 평가 지표 · 유용 규칙 선별 |
| 순차 패턴 | PrefixSpan, 구매 여정 · 시간 순서 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CRISP-DM · 데이터 마이닝 절차] → [데이터 마이닝 KDD 프로세스 · 연관 규칙] → [PrefixSpan · 구매 여정]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[106_association_rules|연관 규칙]]은 편의점에서 "라면을 사는 사람은 달걀도 같이 사는 경우가 많다"는 패턴을 찾는 거야.
2. [[084_support_association_rule_transaction|지지도]]는 얼마나 자주 같이 사는지, [[085_confidence_association_rule_conditional_probability|신뢰도]]는 라면 산 사람 중 달걀도 산 비율, [[086_lift_association_rule_marketing|향상도]]는 "그냥 달걀 사는 것보다 얼마나 더 자주 같이 사는지"야.
3. [[086_lift_association_rule_marketing|향상도]]가 1보다 커야 진짜 유용한 규칙이야 — 그냥 인기 많은 물건은 어디서나 잘 팔리니까!
