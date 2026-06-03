+++
title = "233. 정밀도(Precision) 재현율(Recall) F1 스코어 ROC AUC 임계 곡선"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정밀도(Precision)와 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))은 서로 반비례하는 트레이드오프 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)이며, F1은 이 둘의 조화 평균으로 균형을 잡는다.
> 2. **가치**: ROC 커브(Receiver Operating Characteristic Curve)와 AUC(Area Under Curve)는 임계값(Threshold) 전 범위에 걸친 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기의 종합 성능을 단일 숫자로 요약하며, 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에선 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 커브가 더 직관적이다.
> 3. **판단 포인트**: 비즈니스 맥락(오탐 비용 vs 미탐 비용)에 따라 최적 임계값을 조정하고, 클래스 불균형이 심할 때는 ROC-AUC보다 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC를 우선 지표로 삼아야 한다.

## Ⅰ. 개요 및 필요성

### 왜 Accuracy만으로는 부족한가?

이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기의 성능을 단일 지표로 평가할 때 Accuracy(정확도)는 클래스 불균형 상황에서 크게 오해를 일으킨다.

| 시나리오 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비율 | 무조건 음성 예측 시 Accuracy | 실제 유용성 |
|:---|:---|:---:|:---|
| 사기 탐지 | 99.8% 정상, 0.2% 사기 | **99.8%** | ❌ 사기 탐지 0건 |
| 암 진단 | 95% 음성, 5% 양성 | **95.0%** | ❌ 환자 탐지 0건 |
| 균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 50% vs 50% | **50.0%** | ✅ 의미 있는 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) |

Accuracy가 높아도 소수 클래스를 전혀 탐지 못하는 상황을 <strong>정밀도-<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/">재현율</a> 지표</strong>와 <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/256_roc_auc/">ROC AUC</a></strong>로 정확히 진단해야 한다.

📢 **섹션 요약 비유**: Accuracy만 보는 것은 암 진단 병원의 성과를 "환자가 얼마나 살아서 퇴원했나"로만 평가하는 것이다. "암을 얼마나 빨리, 정확히 찾았나"가 훨씬 중요하다.

## Ⅱ. 아키텍처 및 핵심 원리

### [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) ([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)) 기반 지표 체계

```
                     예측 결과 (Predicted)
                  ┌──────────────┬──────────────┐
                  │  Positive    │  Negative    │
┌─────────────────┼──────────────┼──────────────┤
│ 실제  Positive  │   TP (참양성)│   FN (거짓음성)│
│ 결과  Negative  │   FP (거짓양성)│  TN (참음성) │
└─────────────────┴──────────────┴──────────────┘
```

### 핵심 지표 공식

| 지표 | 공식 | 설명 | 비즈니스 의미 |
|:---|:---|:---|:---|
| **Precision** (정밀도) | TP / (TP+[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) | 양성 예측 중 실제 양성 비율 | 내가 양성이라 한 것 중 맞은 것 |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/">Recall</a></strong> ([재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)) | TP / (TP+FN) | 실제 양성 중 탐지 비율 | 실제 양성을 놓치지 않은 비율 |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/">F1 Score</a></strong> | 2×P×R / (P+R) | P·R 조화 평균 | 정밀도·[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 균형 종합 지표 |
| **Accuracy** | (TP+TN) / 전체 | 전체 정확도 | 균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서만 의미 있음 |
| **Specificity** | TN / (TN+[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) | 음성 정확 탐지율 | 건강인을 정상으로 판정한 비율 |
| **FPR** | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) / ([FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)+TN) | 거짓 양성 비율 | ROC 곡선 X축 |

### 정밀도-[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 트레이드오프 ([ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램)

```
임계값(Threshold)를 낮추면 → 더 많이 양성 예측 → Recall ↑, Precision ↓
임계값(Threshold)를 높이면 → 더 적게 양성 예측 → Recall ↓, Precision ↑

  P/R
  1.0 │ P ─────╮
      │        ╰──────────────────
      │
  0.5 │         ╭─────────────────
      │ R ──────╯
  0.0 └──────────────────────────── Threshold
      0                           1.0

  ↑ 임계값 높일수록: Precision ↑, Recall ↓
  ↓ 임계값 낮출수록: Recall ↑, Precision ↓
  → 비즈니스 맥락에 맞는 임계값 선택이 핵심
```

### ROC 커브 (Receiver Operating Characteristic Curve)

모든 임계값에 대해 TPR(=[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)) vs FPR을 그린 곡선이다.

```
  TPR (Recall)
  1.0 │          ╭─────────────── 이상적 분류기 (AUC=1.0)
      │        ╭─╯ ← 좋은 모델 (AUC~0.9)
  0.7 │      ╭─╯
      │    ╭─╯
  0.5 │  ╭─╯              ← 랜덤 분류기 (AUC=0.5, 대각선)
      │╭─╯
  0.0 └──────────────────── FPR
      0     0.3   0.7    1.0

  AUC (Area Under Curve):
    AUC = 0.5  → 랜덤 수준 (무의미)
    AUC = 0.7  → 보통 수준
    AUC = 0.9  → 우수 수준
    AUC = 1.0  → 완벽 분류기
```

### [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 커브 (Precision-[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) Curve) vs ROC 커브

```
  Precision
  1.0 │──────╮
      │       ╰──────────────── PR 커브
      │                         (불균형 데이터에서 더 정직)
  0.5 │
      │
  0.0 └──────────────────────── Recall
      0                       1.0

  ROC 커브 vs PR 커브 선택 기준:
  ┌────────────────────────┬──────────────┬──────────────┐
  │ 상황                   │ 권장 지표    │ 이유         │
  ├────────────────────────┼──────────────┼──────────────┤
  │ 균형 데이터             │ ROC-AUC      │ 양 클래스 동등 │
  │ 불균형 데이터           │ PR-AUC       │ 소수 클래스 집중│
  │ 소수 클래스 탐지 중요   │ PR-AUC       │ TN 과대평가 방지│
  │ 전반적 분류기 비교      │ ROC-AUC      │ 널리 쓰임    │
  └────────────────────────┴──────────────┴──────────────┘
```

📢 **섹션 요약 비유**: ROC 커브는 모든 문턱값에서 "얼마나 잘 구별하나"를 종합 평가하는 성적표다. AUC는 그 성적표의 최종 점수로, 1점에 가까울수록 뛰어난 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기다.

## Ⅲ. 비교 및 연결

### 비즈니스 맥락별 지표 선택 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 치명적 오류 | 우선 지표 | 임계값 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
|:---|:---|:---|:---|
| 암 진단 | FN (환자 놓침) | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 최대화 | 임계값 낮춤 (0.2~0.3) |
| 스팸 필터 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (정상 메일 차단) | Precision 최대화 | 임계값 높임 (0.7~0.8) |
| 신용카드 사기 | FN (사기 놓침) | F1 + [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) | 임계값 낮춤 + [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) |
| 콘텐츠 추천 | 양쪽 균형 | [F1 Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) | 임계값 0.5 근방 |
| 자율주행 장애물 탐지 | FN (장애물 놓침) | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) ≥ 0.99 | 매우 낮은 임계값 |

### Fβ Score — 정밀도와 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 가중 조합

```
Fβ = (1 + β²) × Precision × Recall / (β² × Precision + Recall)

  β = 1   → F1 (P·R 동등 가중)
  β = 2   → F2 (Recall 2배 중요, 미탐 비용 높을 때)
  β = 0.5 → F0.5 (Precision 2배 중요, 오탐 비용 높을 때)
```

📢 **섹션 요약 비유**: 정밀도는 "낚시 그물에 잡힌 것 중 원하는 물고기 비율"이고, [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)은 "바다에 있는 원하는 물고기 중 내가 잡은 비율"이다. 그물을 크게 치면 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)은 높아지지만 정밀도는 낮아진다.

## Ⅳ. 실무 적용 및 기술사 판단

### 최적 임계값 (Optimal Threshold) 결정 방법

```
방법 1: Youden's J Index (ROC 기반)
  J = Sensitivity + Specificity - 1 = Recall + (1-FPR) - 1
  → J 최대화 임계값 선택

방법 2: F1 최대화 (PR 기반)
  → Precision·Recall이 균형을 이루는 임계값

방법 3: 비용 기반 (Cost-Based)
  Cost = C_FP × FP + C_FN × FN
  → 비즈니스 비용을 최소화하는 임계값 선택

방법 4: 도메인 정책 기준
  암 진단: Recall ≥ 0.95 제약 하에 Precision 최대화
```

### 기술사 판단 포인트

1. <strong>불균형 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>: ROC-AUC는 TN이 많으면 부풀려지므로 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC 병용
2. **다중 클래스**: Macro/Micro/Weighted F1 구분 필요
3. **임계값 조정**: 모델 재학습 없이 임계값만 바꿔 P·R 균형 조절 가능
4. **최종 보고**: 단일 지표가 아닌 [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) 전체를 함께 제시

📢 **섹션 요약 비유**: 임계값 조정은 검사 기준을 낮추거나 높이는 것이다. 기준을 낮추면 더 많은 사람을 "환자"로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(높은 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/), 낮은 정밀도), 기준을 높이면 확실한 환자만 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(높은 정밀도, 낮은 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)).

## Ⅴ. 기대효과 및 결론

### 동일 모델, 임계값 변화에 따른 지표 변화 예시

| 임계값 | Precision | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) | [F1 Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) | 적합 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) |
|:---:|:---:|:---:|:---:|:---|
| 0.2 | 0.45 | 0.92 | 0.61 | 의료 진단 |
| 0.5 | 0.72 | 0.75 | 0.73 | 일반 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 0.7 | 0.88 | 0.51 | 0.64 | 스팸 필터 |
| 0.9 | 0.95 | 0.28 | 0.43 | 초고정밀 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |

### 결론

Precision·[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)·F1·ROC AUC는 모두 [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)에서 파생된 지표들이다. 이들의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이해하고 <strong>비즈니스 목표(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/">FP</a> 비용 vs FN 비용)</strong>에 따라 최적 지표와 임계값을 선택하는 것이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어의 핵심 역량이다. 클래스 불균형 상황에서는 ROC-AUC 단독 사용을 피하고 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC와 병용하며, [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) 전체를 분석해야 한다.

📢 **섹션 요약 비유**: 지표 선택은 스포츠 경기 규칙 선택과 같다. 100미터 달리기(속도=[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 중심)인지 사격(정확도=Precision 중심)인지에 따라 챔피언이 달라진다—어떤 게임을 하는지 먼저 정해야 한다.

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 기반 | [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) ([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/)) | TP/TN/[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)/FN 4가지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 파생 지표 | Precision (정밀도) | TP/(TP+[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) 양성 예측 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) |
| 파생 지표 | [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) ([재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)) | TP/(TP+FN) 실제 양성 탐지율 |
| 균형 지표 | [F1 Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) | P·R 조화 평균 |
| 종합 곡선 | [ROC Curve](/knowledge-base/studynote/10_ai/03_llm_nlp/256_roc_auc/) | TPR vs FPR 전 임계값 비교 |
| 면적 지표 | AUC (Area Under Curve) | ROC 곡선 아래 면적 (0.5~1.0) |
| 불균형 특화 | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) Curve | Precision vs [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) 커브 |
| 조정 변수 | Threshold (임계값) | P·R 트레이드오프 조절 |

### 👶 어린이를 위한 3줄 비유 설명

1. 정밀도는 "내가 '사탕이다!'라고 한 것 중 진짜 사탕이 몇 개나 있냐"이고, [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)은 "바구니에 있는 사탕 중 내가 몇 개나 찾아냈냐"다.

### 📈 관련 키워드 및 발전 흐름도

```text
혼동 행렬 (TP · TN · FP · FN)
    │
    ▼
지표: Precision · Recall · F1-Score (조화 평균)
    │
    ▼
ROC 곡선 · AUC: 임계값 독립 분류 성능
    │
    ▼
다중 클래스: Macro · Micro · Weighted Average
```
2. F1은 정밀도와 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 둘 다 잘 하는 사람에게 높은 점수를 주는 성적표다—하나만 잘하면 점수가 낮다.
3. ROC AUC는 "문턱을 어디 두든 얼마나 잘 구별하나"를 한 숫자(0~1)로 표현한 것으로, 1에 가까울수록 뛰어난 AI다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 233 / 258

← **이전**: [232. TF-IDF (Term Frequency-Inverse Document Frequency) 코사인 유사도 텍스트 임베딩 혼동](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/232_tfidf_cosine_similarity_text_embedding_confusion_matrix/)
**다음**: [234. 마스터 데이터 관리 (MDM, Master Data Management) 골든 레코드 클린 룸](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/234_master_data_management_mdm_golden_record_clean_room/) →

---
