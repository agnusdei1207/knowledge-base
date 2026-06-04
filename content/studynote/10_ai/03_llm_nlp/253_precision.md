+++
title = "253. 정밀도 (Precision)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)([Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/))는 모델이 Positive라고 예측한 것들 중 실제로 Positive인 비율로, <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/">FP</a>(False Positive, 거짓 양성)를 얼마나 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a>했는지</strong>를 측정한다.
> 2. **가치**: 스팸 필터, 광고 타기팅, 법적 판단 등 <strong>잘못된 양성 판정의 비용이 큰 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a></strong>에서 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))보다 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 우선시해야 한다.
> 3. **판단 포인트**: [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)와 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)은 트레이드오프([Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)-[Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) Tradeoff) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)이므로, 임계값(Threshold) 조정 또는 F1-Score로 균형을 찾아야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)의 정의와 직관

```
정밀도(Precision) = TP / (TP + FP)

            실제로 Positive인 것
= -----------------------------------------
  내가 Positive라고 예측한 것(TP + FP) 전체
```

**직관적 해석**: "내가 맞다고 말한 것 중에서 실제로 맞은 비율"
- [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) = 1.0: Positive 예측이 모두 정확, FP가 0
- [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) = 0.5: Positive 예측의 절반만 실제 Positive

### 1.2 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 중요한 이유

[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(False Positive)의 실제 비용:

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | FP의 의미 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 발생 비용 |
|:---|:---|:---|
| 스팸 필터 | 정상 메일을 스팸으로 차단 | 중요 업무 이메일 분실 |
| 광고 타기팅 | 관심 없는 사용자에게 광고 | 광고 예산 낭비 |
| 법원 판결 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 무고한 사람을 유죄 판정 | 억울한 처벌 |
| 금융 대출 심사 | 신용 양호자 대출 거절 | 고객 이탈, 기회 손실 |
| 뉴스 팩트체크 | 진실 정보를 가짜뉴스로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 정보 왜곡 |

- **📢 섹션 요약 비유**: [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 낚시꾼의 정확도다. 그물을 100번 던져서 물고기만 잡히면([FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)=0) [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 100%, 절반이 쓰레기([FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))면 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 50%. 쓸데없이 그물을 많이 던져 정상 메일까지 잡으면 안 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)-[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 트레이드오프 도식

```
+----------------------------------------------------------+
|         정밀도(Precision) - 재현율(Recall) 트레이드오프     |
|                                                          |
|  정밀도                                                   |
|  (Precision)                                             |
|  ^                                                       |
|  1.0 |╲                                                  |
|      | ╲   이상적 곡선 (정밀도·재현율 모두 최대)             |
|  0.8 |  ╲                                                |
|      |   ╲    <- PR 곡선 (Precision-Recall Curve)         |
|  0.6 |    ╲                                              |
|      |     ╲                                             |
|  0.4 |      ╲                                            |
|      |       ╲                                           |
|  0.2 |        ╲                                          |
|      +---------------------------------------> 재현율     |
|       0.0   0.2   0.4   0.6   0.8   1.0    (Recall)     |
|                                                          |
|  임계값(Threshold)^ -> 정밀도^, 재현율v                    |
|  임계값(Threshold)v -> 정밀도v, 재현율^                    |
+----------------------------------------------------------+
```

### 2.2 임계값 (Threshold) 조정 원리

[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델은 보통 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)값(0~1)을 출력하고, 임계값을 기준으로 Positive/Negative 판정:

| 임계값 | 효과 | [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) |
|:---:|:---|:---:|:---:|
| 0.9 (높음) | 매우 확실할 때만 Positive | ^^ | vv |
| 0.5 (기본) | 표준 판정 | 중간 | 중간 |
| 0.1 (낮음) | 조금만 Positive 같아도 판정 | vv | ^^ |

**구체적 예시:**
```
샘플별 스팸 확률: [0.92, 0.85, 0.73, 0.55, 0.41, 0.29, 0.12]

임계값=0.5 -> [Spam, Spam, Spam, Spam, Normal, Normal, Normal]
임계값=0.8 -> [Spam, Spam, Normal, Normal, Normal, Normal, Normal]
임계값=0.3 -> [Spam, Spam, Spam, Spam, Spam, Normal, Normal]
```

### 2.3 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)와 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)의 수식 비교

| 지표 | 수식 | 분모 의미 | 초점 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a>(<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">Precision</a>)</strong> | TP / (TP+[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)) | 내가 Positive라 예측한 전체 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/">재현율</a>(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/">Recall</a>)</strong> | TP / (TP+FN) | 실제 Positive 전체 | FN [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) |
| **정확도(Accuracy)** | (TP+TN) / 전체 | 전체 샘플 | 전체 오류 |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/">F1-Score</a></strong> | 2PR/(P+R) | — | [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)·[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 균형 |

- **📢 섹션 요약 비유**: [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 "말하면 반드시 맞는" 입이 무거운 사람이다. 확실하지 않으면 말을 안 한다([재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 희생). 반면 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)을 중시하면 확실하지 않아도 일단 말한다([정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 희생). 두 성격이 서로 반대인 것이 트레이드오프다.

---

## Ⅲ. 비교 및 연결

### 3.1 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) vs [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/): [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 우선순위

| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 우선 지표 | 이유 | 감수할 수 있는 오류 |
|:---|:---|:---|:---|
| 암 진단 | [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)^ | FN(미검출) 치명적 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(과잉 검사)는 추가 검사로 해결 |
| 스팸 필터 | [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)^ | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(정상 차단) 치명적 | FN(일부 스팸 허용)은 수용 가능 |
| 사기 탐지 | [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)^ | FN(사기 미탐지) 치명적 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(의심 거래 차단)는 해결 가능 |
| 법률 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)^ | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(무죄인 유죄 판정) 치명적 | FN은 다른 수단으로 탐지 |
| 유해 콘텐츠 필터 | [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)^ | FN(유해 콘텐츠 통과) 치명적 | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(일부 정상 콘텐츠 차단) 수용 |

### 3.2 Average [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) ([AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))와 AUPRC

- <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/">PR</a> 곡선 아래 면적(AUPRC, Area Under <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">Precision</a>-<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/">Recall</a> Curve)</strong>: 다양한 임계값에서의 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)·[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 종합 평가
- 클래스 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 <strong>AUROC보다 더 민감한 지표</strong>로 선호됨
- <strong><a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a>(Average <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">Precision</a>)</strong>: [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 곡선의 가중 평균, [객체 탐지](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/)([Object Detection](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/288_object_detection_yolo_rcnn/))에서 mAP(mean [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))로 활용

### 3.3 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)와 관련된 α·β 오류

| 통계학 용어 | ML 용어 | 의미 |
|:---|:---|:---|
| 1종 오류(Type I Error) | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (False Positive) | 실제 음성을 양성으로 잘못 판정 |
| 2종 오류(Type II Error) | FN (False Negative) | 실제 양성을 음성으로 잘못 판정 |
| [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | 1 - FDR (False Discovery Rate) | FP를 줄이는 것이 목표 |

- **📢 섹션 요약 비유**: [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 검사의 기소율이다. 기소한 피의자 중 실제 유죄 비율이 높아야([정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)^) 억울한 사람이 없다. 하지만 기소를 너무 신중히 하면 진짜 범인을 놓칠 수 있다([재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)v) — 이것이 트레이드오프다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 최적화를 위한 임계값 탐색

```
목표: 정밀도 ≥ 0.95 조건에서 재현율 최대화

방법:
1. 모델 출력 확률값 수집
2. 임계값 0.0 ~ 1.0 구간에서 탐색
3. 각 임계값에서 정밀도, 재현율 계산
4. 정밀도 ≥ 0.95 조건 만족하는 가장 낮은 임계값 선택
   (가장 낮은 임계값 = 재현율 최대)
```

### 4.2 클래스 불균형에서 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 해석

**예시: 사기 탐지 (사기 0.1%, 정상 99.9%)**

```
모델 A: 정밀도=0.50, 재현율=0.80
-> 사기라고 예측한 것 중 50%만 실제 사기
-> 정상 거래 차단이 절반 -> 고객 불만

모델 B: 정밀도=0.85, 재현율=0.50
-> 사기라고 예측한 것의 85% 실제 사기
-> 일부 사기는 놓치지만 정상 거래 차단 최소화
```

### 4.3 기술사 핵심 판단 포인트
- <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a>가 중요한 이유를 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 맥락으로 설명</strong>할 것
- [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)·[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 트레이드오프 -> <strong>임계값 조정</strong>으로 해결
- F1-Score는 균형이 필요할 때, <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 특성에 따라 가중 F-Score(Fβ)</strong>로 조정 가능
- `Fβ = (1+β^) × (P×R) / (β^×P + R)` — β>1이면 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 중시, β<1이면 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 중시

- **📢 섹션 요약 비유**: 광고 타기팅 AI의 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 30%라면, 광고를 보여준 10명 중 7명이 전혀 관심 없는 사람이라는 뜻이다. 광고주는 광고비를 70% 낭비하는 것 — [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 높이면 예산 효율이 극적으로 개선된다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 향상의 기대효과
- **스팸 필터**: 중요 이메일 차단율 감소 -> 사용자 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 향상
- **광고 시스템**: 클릭률([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/), Click-Through Rate) 향상 -> [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 개선
- <strong>의료 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 보조 진단</strong>: 의사 추가 검토 부담 감소 -> 업무 효율 향상
- **자동화 품질 검사**: 정상 제품 폐기 비용 절감

### 5.2 결론
[정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 "정확하게 예측했을 때만 발언하라"는 원칙을 수치화한 지표다. [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(False Positive)를 최소화해야 하는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 핵심 지표이며, [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)-[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 트레이드오프를 이해하고 임계값 조정과 Fβ-Score를 통해 실무 요구사항에 맞게 균형을 조율하는 능력이 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 엔지니어의 핵심 역량이다.

- **📢 섹션 요약 비유**: [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 바둑 기사의 수 선택과 같다. 확실히 좋은 수만 두는 기사([정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)^)는 실수는 없지만 빠른 대응을 못 할 수 있다. 빠르게 많은 수를 두는 기사([재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)^)는 공격적이지만 실수도 많다 — 최고의 기사는 이 둘의 균형을 잡는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)([Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) | TP/(TP+[FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/)), [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) / [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
| [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)) | TP/(TP+FN), FN [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) / [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)와 트레이드오프 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| 임계값(Threshold) | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 판정 기준, 조정 / [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)-[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 균형 조절 |
| [F1-Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) | 조화평균, 균형 지표 / [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)·[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 통합 |
| Fβ-Score | β값으로 중요도 가중 / [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 맞춤 평가 |
| AUPRC | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 곡선 면적 / 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 종합 평가 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [정밀도 (Precision)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 <strong>"내가 맞다고 한 것 중 실제로 맞은 비율"</strong>이에요.
2. "이 사람이 나쁜 사람이야!"라고 100번 말했는데 85번만 맞았으면 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 85%예요.
3. [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 낮으면 억울한 사람이 많아지니까, 특히 법이나 의료처럼 중요한 곳에서는 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 꼭 높여야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 253 / 420

<- **이전**: [252. 혼동 행렬 (Confusion Matrix)](/knowledge-base/studynote/10_ai/03_llm_nlp/252_confusion_matrix/)
**다음**: [254. 재현율 (Recall) / 민감도](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) ->

---
