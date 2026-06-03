+++
title = "548. 데이터 포이즈닝과 적대적 예제 모델 오판 (Data Poisoning Adversarial Model Manipulation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 보안 위협은 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오염([데이터 포이즈닝](/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/)), 추론 시 입력 조작([적대적 예제](/knowledge-base/studynote/09_security/19_ai_advanced_security/942_adversarial_example/)), 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포함 여부 추론([멤버십 추론 공격](/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/)) 세 층위로 분류되며 각각 다른 방어 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필요하다.
> 2. **가치**: 클린-레이블 공격(Clean-Label Attack)은 라벨 변조 없이 특성 공간만 오염시켜 탐지를 회피하는 정교한 공격으로, 웹 스크랩 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파이프라인에서 실제 위협이 된다.
> 3. **판단 포인트**: [멤버십 추론 공격](/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/)([Membership Inference](/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/) Attack)은 모델의 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포함 여부를 통계적으로 추론하므로, [차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/)(DP-SGD)와 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Regularization](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/)) 강화가 핵심 방어다.

---

## Ⅰ. 개요 및 필요성

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템의 신뢰성은 세 가지 보안 속성에 달려 있다:
- <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a>)</strong>: 올바른 예측 → 포이즈닝·[적대적 예제](/knowledge-base/studynote/09_security/19_ai_advanced_security/942_adversarial_example/) 위협
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>(<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong>: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 없음 → [적대적 예제](/knowledge-base/studynote/09_security/19_ai_advanced_security/942_adversarial_example/), [모델 추출](/knowledge-base/studynote/09_security/19_ai_advanced_security/950_model_extraction/) 위협
- <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">Confidentiality</a>)</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비공개 → 멤버십 추론, 모델 역전(Inversion) 위협

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 보안: 사전 학습 모델(Pre-trained Model), 공개 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋, 파인튜닝 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모두 포이즈닝 위협 대상.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안은 집의 세 가지 보안 — 문([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)), 전원([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)), [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))을 모두 지켜야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌───────────────────────────────────────────────────────────┐
│               AI 보안 위협 전체 지형                        │
│                                                           │
│  훈련 단계 위협                   추론 단계 위협            │
│  ┌─────────────────────┐         ┌────────────────────┐   │
│  │ 데이터 포이즈닝       │         │ 적대적 예제(Evasion)│   │
│  │ ·백도어(트리거 삽입) │         │ ·FGSM, PGD, C&W   │   │
│  │ ·클린-라벨 공격      │         └────────────────────┘   │
│  │ ·모델 독(Model Rot) │         ┌────────────────────┐   │
│  └─────────────────────┘         │ 멤버십 추론 공격   │   │
│                                  │ ·Shadow Model     │   │
│  학습 완료 후 위협                │ ·Likelihood Test  │   │
│  ┌─────────────────────┐         └────────────────────┘   │
│  │ 모델 추출(Stealing) │         ┌────────────────────┐   │
│  │ ·블랙박스 쿼리 반복 │         │ 모델 역전(Inversion)│   │
│  └─────────────────────┘         │ ·훈련 데이터 복원  │   │
│                                  └────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

<strong><a href="/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/">데이터 포이즈닝</a> 세부 유형</strong>

| 공격 유형 | 방법 | 탐지 어려움 |
|:---:|:---:|:---:|
| [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/)([Backdoor](/knowledge-base/studynote/09_security/15_malware_attack_vectors/727_backdoor/)) | [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 패턴 + 라벨 변조 | 낮음 |
| 클린-라벨 공격 | 라벨 유지, 특성 공간 오염 | **매우 높음** |
| 점진적 포이즈닝 | 소수 샘플 장기간 삽입 | 높음 |
| 모델 독(Model Rot) | [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 조작으로 수렴 방해 | 높음 |

**클린-라벨 공격 원리**

1. 공격 목표: "개구리" 이미지를 "비행기"로 오분류시키길 원함
2. "개구리" 라벨은 그대로 유지
3. "개구리" 이미지의 특성 벡터를 "비행기" 특성 공간으로 이동 (미세 픽셀 조작)
4. 모델이 이 "개구리"를 학습하면 정상으로 보이는 특정 개구리 이미지를 "비행기"로 예측

<strong><a href="/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/">멤버십 추론 공격</a>(<a href="/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/">Membership Inference</a> Attack)</strong>

| 방법 | 원리 |
|:---:|:---|
| Shadow Model 공격 | 타깃 모델 행동 모방 Shadow Model로 멤버/비멤버 구분기 학습 |
| Likelihood Ratio | 타깃 모델의 샘플 손실값 분포 차이 활용 |
| 임계값 기반 | 훈련 샘플은 낮은 손실값 → [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 이하면 멤버로 판별 |

- **📢 섹션 요약 비유**: 멤버십 추론은 "이 이름이 학교 출석부에 있는지" 알아내는 것 — 선생님이 그 이름에 자동 반응하면 있다는 증거다.

---

## Ⅲ. 비교 및 연결

### 방어 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 매핑

| 공격 유형 | 1차 방어 | 2차 방어 |
|:---:|:---:|:---:|
| [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 포이즈닝 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 및 정화 | Neural Cleanse, Fine-pruning |
| 클린-라벨 공격 | [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)(Spectral Signatures) | 신뢰 점수 필터링 |
| [적대적 예제](/knowledge-base/studynote/09_security/19_ai_advanced_security/942_adversarial_example/) | [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/) | 입력 정화, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 방어 |
| 멤버십 추론 | DP-SGD | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 강화([Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)) |
| [모델 추출](/knowledge-base/studynote/09_security/19_ai_advanced_security/950_model_extraction/) | 예측 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 노이즈 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 제한([Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/)) |

<strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/">공급망 보안</a></strong>
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 출처 추적(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Provenance)</strong>: 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 출처와 처리 이력 기록
- **Watermarking**: 모델 가중치에 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [워터마크](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 삽입 → 포이즈닝 소스 역추적
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 정화(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Sanitization)</strong>: [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)(스펙트럼 서명, [KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/) 기반)로 의심 샘플 제거

- **📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)은 식품 이력 추적 시스템 — 재료가 어디서 왔는지 알아야 오염 발생 시 원인을 찾을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 보안 평가 프레임워크</strong>

| 평가 항목 | 도구/방법 | 기준 |
|:---:|:---:|:---|
| [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 탐지 | Neural Cleanse, ABS | ASR(Attack Success Rate) < 5% |
| 적대적 강건성 | AutoAttack 벤치마크 | Robust Accuracy 측정 |
| 멤버십 추론 | LiRA(Likelihood Ratio Attack) | AUC < 0.6 목표 |
| [모델 추출](/knowledge-base/studynote/09_security/19_ai_advanced_security/950_model_extraction/) | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시뮬레이션 | 추출 모델 정확도 격차 |

**기술사 판단 포인트**

1. <strong>사전 학습 모델 <a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong>: Hugging Face 등 공개 모델 도입 시 [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 스캔 필수 (Fine-pruning 적용)
2. <strong>웹 스크랩 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 위험</strong>: LAION 등 대규모 웹 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) → 클린-라벨 공격 포함 가능성 → Spectral Signatures 검사
3. <strong>의료/금융 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>: [멤버십 추론 공격](/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/)이 환자/고객 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 유출로 연결 → DP-SGD ε ≤ 3 적용
4. **MITRE ATLAS**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 위협 [지식 베이스](/knowledge-base/studynote/10_ai/01_ai_basics/008_knowledge_base_inference_engine/) — [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 공격 전술·기법·절차([TTP](/knowledge-base/studynote/09_security/04_endpoint_security/329_ttp/)) 표준 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 프레임워크

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 식당 위생 검사 — 눈에 보이지 않는 오염(포이즈닝)을 정기적으로 확인해야 고객을 보호할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 보안은 개발 단계부터 운영까지 전 생애주기에 걸친 다층 방어가 필요하다. [데이터 포이즈닝](/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/) 탐지, [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/), DP-SGD의 결합이 현재 최선의 방어 조합이다. MITRE ATLAS와 같은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 위협 [지식 베이스](/knowledge-base/studynote/10_ai/01_ai_basics/008_knowledge_base_inference_engine/)를 활용한 체계적 위험 관리가 기술사 수준에서 요구된다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안은 성의 방어선 — 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(외성벽), 모델 추론(내성벽), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기밀(비밀 창고) 모두를 지켜야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/)([Backdoor](/knowledge-base/studynote/09_security/15_malware_attack_vectors/727_backdoor/)) | 포이즈닝 유형 · [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반 오분류 |
| 클린-라벨 공격 | 포이즈닝 유형 · 라벨 무변조 특성 오염 |
| 멤버십 추론 | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 공격 · 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포함 여부 추론 |
| Neural Cleanse | [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 탐지 · 이상 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 역설계 |
| DP-SGD | 방어 · 멤버십 추론 방어 |

### 📈 관련 키워드 및 발전 흐름도

```text
[포이즈닝 유형 · 트리거 기반 오분류] → [데이터 포이즈닝과 적대적 예제 모델 오판] → [방어 · 멤버십 추론 방어]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학교에 나쁜 학생이 몰래 틀린 정보를 가르치면 AI가 잘못 배워요 — 이게 [데이터 포이즈닝](/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/)이에요.
2. 멤버십 추론은 "이 학생이 시험에 나온 문제를 미리 봤는지" 알아내려는 꼼수예요.
3. 이런 공격을 막으려면 공부 재료를 꼼꼼히 검사하고, 정보를 조금 흐릿하게 배우게([차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/)) 해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 548 / 552

← **이전**: [547. 오토인코더와 VAE 잠재 벡터 차원 축소 (Autoencoder VAE Latent Vector Dimensionality Reduction)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/547_autoencoder_vae_latent_dimensionality_reduction/)
**다음**: [549. LLM 컨텍스트 윈도우 확장과 긴 문맥 처리 (LLM Context Window Extension Long Context)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/549_llm_context_window_extension_long_context/) →

---
