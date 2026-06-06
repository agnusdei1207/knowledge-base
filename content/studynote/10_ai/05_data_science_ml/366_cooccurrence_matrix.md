---
title: "Co-occurrence Matrix"
date: "2026-05-09"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동시 등장 행렬(Co-occurrence Matrix)은 코퍼스에서 두 단어가 윈도우(Window) 크기 k 이내에서 함께 등장한 빈도를 행렬 X_ij로 집계하는 고차원 희소 행렬(Sparse Matrix)이며, 단어 의미를 분포 가설(Distributional Hypothesis)로 인코딩한다.
> 2. **가치**: 단순 빈도 대신 PPMI(Positive Pointwise [Mutual Information](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/))로 변환하면 "the"처럼 의미 없이 자주 등장하는 단어의 영향을 제거하고, 진짜 의미적 연관성만 포착한다.
> 3. **판단 포인트**: 어휘 크기 |V|×|V| 행렬(|V|=10만이면 100억 원소)의 메모리 문제를 [SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)([Singular Value Decomposition](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)) 또는 PPMI + Truncated SVD로 저차원 밀집 벡터로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)한다.

---

## Ⅰ. 개요 및 필요성

분포 가설(Distributional Hypothesis): "비슷한 문맥에서 사용되는 단어는 비슷한 의미를 가진다"(John Firth, 1957). 이 가설을 수치화한 것이 동시 등장 행렬이다. "은행"이라는 단어 주변에 "돈", "이자", "대출"이 자주 등장한다면, 이 공동 등장 패턴(동시 등장 벡터)이 "은행"의 의미를 담는다. [Word2Vec](/studynote/10_ai/04_ai_ops_ethics/339_word2vec/), [GloVe](/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/), [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 모두 이 원리를 기반으로 한다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 동시 등장 행렬은 "단어의 친구 목록"이다. "은행"의 친구가 "돈, 이자, [ATM](/studynote/03_network/05_lan_wan_l2_devices/272_atm_asynchronous_transfer_mode_53byte_cell/)"이고, "강둑"의 친구가 "물, 낚시, 물고기"라면 두 단어는 다른 의미를 가진다. 친구 목록(동시 등장 패턴)이 단어의 신분증이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------------------+
|         동시 등장 행렬 구성 및 PPMI 변환                 |
+----------------------------------------------------------+
|  윈도우 크기 k=2 예시:                                  |
|  "나는 오늘 맛있는 밥을 먹었다"                         |
|  오늘 기준: {나는(2), 맛있는(1)} 윈도우 내 등장        |
|                                                          |
|  X_ij: 단어 i 기준 단어 j의 동시 등장 횟수             |
|                                                          |
|  PMI (Pointwise Mutual Information):                    |
|  PMI(i,j) = log[P(i,j) / (P(i)·P(j))]                 |
|  = log[X_ij·N / (Σⱼ X_ij · Σᵢ X_ij)]                 |
|                                                          |
|  PPMI (Positive PMI):                                   |
|  PPMI(i,j) = max(0, PMI(i,j))                          |
|  -> 음수 PMI 제거 (음수 = 이 조합이 우연보다 드문 경우) |
|                                                          |
|  차원 축소: Truncated SVD                               |
|  X ≈ U_k · Σ_k · V_kᵀ  (k 차원 근사)                 |
+----------------------------------------------------------+
```

| 변환 방법 | 수식 | 특성 | 주요 문제 |
|:---|:---|:---|:---|
| 원시 빈도 | X_ij | 단순 | 고빈도 단어 지배 |
| [TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) | - | 문서 내 중요도 | 전역 통계 무시 |
| PMI | log(P(i,j)/P(i)P(j)) | 연관성 측정 | 희귀 쌍 과대평가 |
| PPMI | max(0, PMI) | 음수 제거 | 0 과잉(희소) |

- **📢 섹션 요약 비유**: PPMI는 "의미 없는 인연 제거 필터"다. "the"와 모든 단어가 함께 나오는 것은 우연(낮은 PMI)이다. PPMI는 우연 이상의 진짜 의미적 연관(양의 PMI만 남김)만 보존한다.

---

## Ⅲ. 비교 및 연결

동시 등장 행렬 기반 LSA(Latent Semantic Analysis, 잠재 의미 분석)는 [TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) 행렬에 Truncated SVD를 적용하여 문서-단어 행렬을 저차원으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)한다. 이는 [GloVe](/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/) 이전의 대표적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 표현 방법이다. 현대 언어 모델([BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))은 동시 등장 행렬을 직접 사용하지 않지만, Transformer의 Self-Attention이 사실상 동적 동시 등장 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 문맥에 따라 계산한다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| 동시 등장 행렬 (Co-occurrence Matrix) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: BERT의 Self-Attention은 "동적 동시 등장 행렬"이다. 고정된 X_ij 대신, 매 문장마다 문맥에 따라 각 단어 쌍의 관련성 점수를 실시간으로 계산하는 것이 Self-Attention이다. 동시 등장 행렬의 동적 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 Attention이라고 이해할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

메모리 효율화: scipy.sparse 행렬로 저장하면 0 원소를 제외한 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 저장(희소 행렬 포맷). 어휘 크기 100,000에서 dense 행렬은 10GB, sparse 행렬은 실제 비zero 원소만 저장해 수십 MB로 줄어든다. [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/) k 선택: k=2~10이 일반적. k가 크면 넓은 문맥을 포착하지만 노이즈 증가. 구문 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 좁은 윈도우, 의미 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 넓은 윈도우가 효과적이다.

- **📢 섹션 요약 비유**: sparse 행렬 저장은 "[체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)에서 체크된 것만 기록"하는 방법이다. 100만×100만 표(동시 등장 행렬)에서 대부분이 0(만나지 않은 단어 쌍)이다. 0은 저장하지 않고 0이 아닌 칸의 좌표와 값만 저장하면 공간이 1/1000로 줄어든다.

---

## Ⅴ. 기대효과 및 결론

동시 등장 행렬은 단어 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)의 근본 원리(분포 가설)를 구현하는 명시적 방법으로, [Word2Vec](/studynote/10_ai/04_ai_ops_ethics/339_word2vec/)/GloVe의 암묵적 학습이 실제로는 동시 등장 행렬의 특수 분해와 동치임이 이론적으로 증명됐다. 기술사 시험에서 PPMI 변환의 의미, Truncated [SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) [차원 축소](/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/), sparse 행렬 효율화를 연결해서 서술하면 완성도 높은 답안이 된다.

- **📢 섹션 요약 비유**: 동시 등장 행렬은 언어 AI의 "인간관계 지도"다. 모든 단어들이 서로 얼마나 친한지(동시 등장 빈도) 기록한 초대형 인맥 지도이며, 이 지도를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)([SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/))하면 각 단어의 성격(벡터)이 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [GloVe](/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/) | 전역 동시 등장 / 동시 등장 행렬을 목적함수로 분해 |
| LSA (Latent Semantic Analysis) | [TF-IDF](/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/) + [SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) / 동시 등장 행렬의 [SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) 응용 |
| PPMI | PMI 양수화 / 의미 없는 고빈도 연관 제거 |
| Sparse Matrix | 희소 행렬 / 메모리 효율적 저장 포맷 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [동시 등장 행렬 (Co-occurrence Matrix)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 동시 등장 행렬은 "어떤 단어들이 같은 문장에서 짝꿍이 되는지" 횟수를 기록한 거대한 표예요.
2. "고양이"와 "울음"이 많이 같이 나오면 표의 해당 칸 숫자가 커져요.
3. 이 표를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)([SVD](/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/))하면 각 단어의 의미를 담은 짧은 벡터가 완성돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 366 / 420

<- **이전**: [365. GloVe (Global Vectors for Word Representation)](/studynote/10_ai/05_data_science_ml/365_glove_word_embedding/)
**다음**: [367. SVM 슬랙 변수 (Slack Variable)](/studynote/10_ai/05_data_science_ml/367_svm_slack_variable/) ->

---
