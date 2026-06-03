+++
title = "232. TF-IDF (Term Frequency-Inverse Document Frequency) 코사인 유사도 텍스트 임베딩 혼동 행렬"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TF-IDF(Term Frequency-Inverse [Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/) Frequency)는 단어의 문서 내 빈도와 전체 문서 집합에서의 희귀성을 곱해 그 단어가 해당 문서를 얼마나 잘 대표하는지를 수치화한다.
> 2. **가치**: 벡터 공간 모델(Vector Space Model)로 문서를 수치 벡터로 표현하면 [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)([Cosine Similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/))를 통해 문서 간 의미적 거리를 계산하고 검색·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·추천에 활용할 수 있다.
> 3. **판단 포인트**: TF-IDF는 단어 순서와 의미를 무시하므로, 문맥 이해가 중요한 경우에는 [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/)·[BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)을 선택하고 [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/))로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 정밀 진단해야 한다.

## Ⅰ. 개요 및 필요성

### 텍스트를 숫자로 바꾸는 이유

[머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 모델은 숫자만 처리할 수 있다. 텍스트(문서, 리뷰, 기사)를 모델에 넣으려면 수치 벡터로 변환해야 한다.

| 표현 방식 | 단어 순서 | 의미(Semantic) | 특징 |
|:---|:---:|:---:|:---|
| BoW (Bag of Words) | ❌ | ❌ | 단어 빈도수만 계산 |
| TF-IDF | ❌ | 부분적 | 중요도 가중 빈도 |
| [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) | ❌ | ✅ | 단어 간 유사도 학습 |
| FastText | 부분적 | ✅ | 서브워드(Subword) 포함 |
| [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | ✅ | ✅✅ | 문맥 의존 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |

📢 **섹션 요약 비유**: 텍스트를 벡터로 바꾸는 것은 각 문서를 지도 위 좌표로 표시하는 것이다. 좌표가 가까운 두 문서는 내용이 비슷하다는 뜻이다.

## Ⅱ. 아키텍처 및 핵심 원리

### TF-IDF 계산 공식

**TF (Term Frequency, 단어 빈도)**
```
TF(t, d) = (문서 d에서 단어 t의 등장 횟수) / (문서 d의 전체 단어 수)
```

<strong>IDF (Inverse <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/">Document</a> Frequency, 역문서 빈도)</strong>
```
IDF(t) = log( N / df(t) )
         또는 log( 1 + N / (1 + df(t)) )  ← 스무딩 (Smoothing) 버전

여기서:
  N    = 전체 문서 수
  df(t)= 단어 t를 포함한 문서 수
```

<strong>TF-IDF 최종 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a></strong>
```
TF-IDF(t, d) = TF(t, d) × IDF(t)
```

### 계산 예시 (3개 문서)

```
문서1: "AI 모델 학습 AI 모델"          → AI 2회, 모델 2회, 학습 1회
문서2: "머신러닝 학습 데이터"            → 머신러닝 1회, 학습 1회, 데이터 1회
문서3: "딥러닝 AI 신경망"              → 딥러닝 1회, AI 1회, 신경망 1회

N = 3  (전체 문서 수)

IDF("AI") = log(3/2) = 0.405   ← 2개 문서에 등장 → 흔한 단어
IDF("학습") = log(3/2) = 0.405
IDF("신경망") = log(3/1) = 1.099  ← 1개 문서에만 등장 → 희귀·중요 단어

TF-IDF("AI", 문서1) = (2/5) × 0.405 = 0.162
TF-IDF("신경망", 문서3) = (1/3) × 1.099 = 0.366  ← 더 높은 가중치
```

### 벡터 공간 모델 (Vector Space Model) 구조

```
                    어휘 사전 (Vocabulary)
         ┌────────┬─────────┬────────┬──────────┐
         │  AI    │  모델   │  학습  │  신경망   │
┌────────┼────────┼─────────┼────────┼──────────┤
│ 문서1  │ 0.162  │  0.200  │ 0.081  │   0.000  │
│ 문서2  │ 0.000  │  0.000  │ 0.135  │   0.000  │
│ 문서3  │ 0.135  │  0.000  │ 0.000  │   0.366  │
└────────┴────────┴─────────┴────────┴──────────┘

각 문서 = 고차원 벡터 공간의 한 점
```

### [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) ([Cosine Similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/))

두 문서 벡터가 이루는 각도의 코사인 값으로 유사도를 측정한다. 벡터 크기(문서 길이)에 영향받지 않는 것이 장점이다.

```
cos(θ) = (A · B) / (|A| × |B|)

여기서:
  A · B  = 두 벡터의 내적 (dot product)
  |A|    = 벡터 A의 크기 (유클리드 노름)
  결과 범위: -1 (완전 반대) ~ 0 (무관) ~ 1 (동일)

코사인 유사도 vs 유클리드 거리:
  코사인: 방향 기반 → 문서 길이 불변 → 텍스트 검색에 적합
  유클리드: 거리 기반 → 문서 길이 영향 → 이미지·좌표 분석에 적합
```

### [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) ([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/))

[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 4가지 경우로 상세 분석하는 도구이다.

```
                   예측 (Predicted)
                ┌──────────────┬──────────────┐
                │  양성 (Pos)  │  음성 (Neg)  │
┌───────────────┼──────────────┼──────────────┤
│ 실제 양성(Pos)│  TP (참양성) │  FN (거짓음성)│
│               │  True Pos    │  False Neg   │
├───────────────┼──────────────┼──────────────┤
│ 실제 음성(Neg)│  FP (거짓양성)│  TN (참음성) │
│               │  False Pos   │  True Neg    │
└───────────────┴──────────────┴──────────────┘

TP: 실제 양성을 양성으로 정확히 예측   → "맞음"
TN: 실제 음성을 음성으로 정확히 예측   → "맞음"
FP: 실제 음성인데 양성으로 잘못 예측   → 1종 오류 (False Alarm, 오탐)
FN: 실제 양성인데 음성으로 잘못 예측   → 2종 오류 (Miss, 미탐)
```

📢 **섹션 요약 비유**: [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)은 병원 검사 결과표다. TP=진짜 환자를 환자로 진단, TN=건강인을 건강으로 진단, [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)=건강인을 환자로 오진(과잉 진단), FN=환자를 건강으로 오진(놓침).

## Ⅲ. 비교 및 연결

### TF-IDF vs 신경망 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 비교

| 항목 | TF-IDF | [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) | FastText | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) |
|:---|:---|:---|:---|:---|
| 벡터 크기 | 어휘 수(수만) | 100~300차원 | 100~300차원 | 768차원 |
| 단어 순서 | ❌ | ❌ | ❌ | ✅ |
| 미등록어 처리 | ❌ | ❌ | ✅(서브워드) | ✅ |
| 문맥 의존 | ❌ | ❌ | ❌ | ✅ |
| 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요 | ❌ (통계적) | ✅ | ✅ | ✅✅(대규모) |
| 계산 속도 | ⚡ 빠름 | 보통 | 보통 | 🐢 느림 |
| 주요 용도 | 문서 검색·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 유사 단어 탐색 | 오타·신조어 처리 | 질의응답·번역 |

### TP/TN/[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)/FN 파생 지표

```
Precision (정밀도) = TP / (TP + FP)    → 양성 예측의 신뢰도
Recall (재현율)   = TP / (TP + FN)    → 실제 양성의 탐지율
Accuracy (정확도) = (TP+TN) / 전체    → 전체 예측 정확도
F1 Score          = 2×P×R / (P+R)    → 정밀도·재현율 조화평균
Specificity       = TN / (TN + FP)    → 음성 탐지율
FPR (거짓양성률)  = FP / (FP + TN)    → ROC 곡선 X축
```

📢 **섹션 요약 비유**: TF-IDF는 "자주 쓰지만 너무 흔하지 않은 단어"에 높은 점수를 준다. 마치 이력서에서 "저는 숨을 쉽니다"는 무의미하지만 "양자컴퓨팅 경험"은 희귀하고 중요한 정보다.

## Ⅳ. 실무 적용 및 기술사 판단

### TF-IDF 기반 문서 검색 파이프라인

```
문서 전처리         벡터화             유사도 계산       결과 반환
[원본 문서]  →  [토크나이징]  →  [TF-IDF 행렬]  →  [코사인 유사도]
                 정제·불용어              (문서×어휘)       상위 K개 문서
                 제거·소문자화
```

### [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) 기반 모델 진단 시나리오

| 비즈니스 상황 | 치명적 오류 | 핵심 지표 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
|:---|:---|:---|:---|
| 암 진단 | FN (환자 놓침) | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 최대화 | 임계값 낮춤 |
| 스팸 필터 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (정상 메일 차단) | [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 최대화 | 임계값 높임 |
| 사기 탐지 | FN (사기 놓침) | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 최대화 | [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) + 낮은 임계값 |
| 제품 추천 | 양쪽 균형 필요 | [F1 Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) | 임계값 0.5 근방 |

📢 **섹션 요약 비유**: [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)을 보면 모델이 "어디서 실수하는지" 알 수 있다. 마치 시험 채점지를 보면 어떤 유형에서 틀렸는지 알 수 있는 것처럼.

## Ⅴ. 기대효과 및 결론

### TF-IDF의 한계와 발전 방향

| 한계 | 극복 방향 |
|:---|:---|
| 단어 순서 무시 (BoW) | n-gram TF-IDF 또는 [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) |
| 동의어 처리 불가 | LSA(Latent Semantic Analysis), [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| 미등록 신조어 취약 | FastText 서브워드 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| 고차원 희소 행렬 | [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)([Singular Value Decomposition](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)) [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) |
| 문맥 의미 미반영 | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 문맥 기반 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |

### 결론

TF-IDF는 단순하지만 문서 검색·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 분야에서 여전히 강력한 베이스라인이다. 특히 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없이도 바로 적용 가능한 통계적 방법이라는 점에서 실무적 가치가 크다. [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 단일 숫자(Accuracy)로 단순화하지 않고 오류 유형을 구체적으로 진단할 수 있는 필수 도구이며, 비즈니스 맥락에 맞는 지표 선택의 출발점이 된다.

📢 **섹션 요약 비유**: TF-IDF는 도서관 색인 카드 시스템이다. 단순하지만 "이 키워드로 찾을 수 있는 책"을 빠르게 골라내는 힘이 있다. 더 깊은 이해가 필요하면 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사서([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))를 부르면 된다.

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 기반 기술 | TF-IDF | 단어 중요도 수치화 |
| 유사도 측정 | [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/) ([Cosine Similarity](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)) | 벡터 간 각도 기반 유사도 |
| 문서 표현 모델 | 벡터 공간 모델 (Vector Space Model) | 문서를 고차원 벡터로 표현 |
| 발전 기술 | [Word2Vec](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/) / FastText | 밀집 벡터(Dense Vector) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| 발전 기술 | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) / [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) | 문맥 의존 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 진단 | [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) ([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)) | TP/TN/[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)/FN 오류 분석 |
| 파생 지표 | [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) / [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) / F1 | [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) 기반 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |

### 👶 어린이를 위한 3줄 비유 설명

1. TF-IDF는 책에서 자주 나오지만 모든 책에 흔하게 있지는 않은 단어를 찾아서 "이 책의 핵심 단어"라고 표시해 주는 것이다.

### 📈 관련 키워드 및 발전 흐름도

```text
BoW (Bag of Words) → 빈도만 카운팅
    │
    ▼
TF-IDF: 문서 빈도 역수 가중치 → 핵심 단어 추출
    │
    ▼
Word2Vec · GloVe: 단어 임베딩 (의미 유사도)
    │
    ▼
BERT Embedding · Sentence Transformer → 코사인 유사도
```
2. [코사인 유사도](/knowledge-base/studynote/06_ict_convergence/05_data_science/359_cosine_similarity/)는 두 책이 가리키는 방향이 얼마나 비슷한지 각도로 재는 것—방향이 같을수록(각도 0도) 비슷한 책이다.
3. [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)은 AI가 정답을 맞혔는지 틀렸는지 4가지 상자(TP, TN, [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/), FN)에 나눠 세어보는 성적표다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 232 / 258

← **이전**: [231. SMOTE (Synthetic Minority Over-sampling Technique) 불균형 데이터 증강](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/)
**다음**: [233. 정밀도(Precision) 재현율(Recall) F1 스코어 ROC AUC 임계 곡선](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) →

---
