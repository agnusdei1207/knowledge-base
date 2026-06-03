+++
title = "470. 적대적 공격: 포이즈닝과 이베이전 (Adversarial Attack Poisoning Evasion)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 적대적 공격([Adversarial Attack](/knowledge-base/studynote/10_ai/02_dl_architecture_new/197_adversarial_attack/))은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 취약점을 의도적으로 악용해 잘못된 예측을 유도하는 공격으로, 훈련 단계를 노리는 포이즈닝과 추론 단계를 노리는 이베이전으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)된다.
> 2. **가치**: [FGSM](/knowledge-base/studynote/09_security/19_ai_advanced_security/943_fgsm/)(Fast Gradient Sign Method) 등 이베이전 공격은 사람 눈에는 동일한 이미지로 고양이를 총기로 오분류시킬 수 있어, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 보장에 핵심 위협이다.
> 3. **판단 포인트**: [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)([Adversarial Training](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/))이 가장 강력한 방어지만 훈련 비용이 2~10배 증가하므로, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 보안 수준에 맞는 방어 전략을 계층적으로 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델은 통계적 패턴 학습으로 동작하기 때문에, 그 패턴을 교란하도록 설계된 입력에 매우 취약하다. 자율주행 차량의 정지 표지판 인식 방해, 악성코드 탐지 우회, 얼굴 인식 잠금 해제 등이 실제 위협 시나리오다.

**공격 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기준**

| 기준 | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
|:---:|:---|
| 공격 시점 | 포이즈닝(훈련 시) vs 이베이전(추론 시) |
| 공격자 지식 | 화이트박스(모델 완전 접근) vs 블랙박스(출력만 관찰) |
| 공격 목표 | 무차별 오분류 vs 특정 클래스로 유도(Targeted) |

- **📢 섹션 요약 비유**: 포이즈닝은 요리사가 재료를 사기 전에 식재료 창고를 오염시키는 것이고, 이베이전은 완성된 요리에 냄새 없는 독을 넣는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────────┐
│              AI 공격 분류                            │
│                                                     │
│  훈련 단계                     추론 단계             │
│  ┌──────────────────┐         ┌──────────────────┐  │
│  │  포이즈닝 공격    │         │  이베이전 공격    │  │
│  │ (Poisoning)      │         │ (Evasion)        │  │
│  │                  │         │                  │  │
│  │ ·악성 샘플 삽입  │         │ ·FGSM 노이즈     │  │
│  │ ·백도어(Backdoor)│         │ ·PGD 반복 공격   │  │
│  │ ·클린-라벨 공격  │         │ ·C&W 공격        │  │
│  └──────────────────┘         └──────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**포이즈닝 공격(Poisoning Attack)**
훈련 데이터에 악의적으로 조작된 샘플을 삽입해 모델의 일반 성능을 저하시키거나, 특정 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)(Trigger) 패턴 입력 시 오분류하도록 [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/)를 심는다.

- **[백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 공격([Backdoor Attack](/knowledge-base/studynote/09_security/19_ai_advanced_security/949_backdoor_attack/))**: 특정 스티커 패턴이 붙은 정지 표지판을 "속도 무제한"으로 인식하도록 훈련
- **클린-라벨 공격(Clean-Label Attack)**: 라벨 변조 없이 특성 공간만 오염시켜 탐지 회피

**이베이전 공격(Evasion Attack)**
추론 시 원본 입력에 미세한 노이즈(Perturbation, ε ≤ 0.03)를 추가해 오분류 유도.

- **[FGSM](/knowledge-base/studynote/09_security/19_ai_advanced_security/943_fgsm/)(Fast Gradient Sign Method)**: 손실 함수의 기울기 부호 방향으로 1회 ε만큼 이동
- **[PGD](/knowledge-base/studynote/09_security/19_ai_advanced_security/944_pgd/)([Projected Gradient Descent](/knowledge-base/studynote/09_security/19_ai_advanced_security/944_pgd/))**: FGSM을 L∞ 제약 내에서 반복 적용 — 더 강력
- **[C&W](/knowledge-base/studynote/09_security/19_ai_advanced_security/945_cw_attack/) 공격**: 최소 노이즈로 오분류 달성하는 최적화 문제

### 공격 강도 비교

| 공격 | 화이트박스 | 계산 비용 | 전이성 |
|:---:|:---:|:---:|:---:|
| [FGSM](/knowledge-base/studynote/09_security/19_ai_advanced_security/943_fgsm/) | ✓ | 낮음 | 중간 |
| [PGD](/knowledge-base/studynote/09_security/19_ai_advanced_security/944_pgd/) | ✓ | 높음 | 높음 |
| [C&W](/knowledge-base/studynote/09_security/19_ai_advanced_security/945_cw_attack/) | ✓ | 매우 높음 | 낮음 |
| [Square](/knowledge-base/studynote/04_software_engineering/06_software_architecture/341_iso_iec_25010/) Attack | ✗(블랙박스) | 중간 | 중간 |

- **📢 섹션 요약 비유**: FGSM은 한 번의 발차기, PGD는 수십 번 반복 발차기, C&W는 약점만 정밀 타격하는 무술이다.

---

## Ⅲ. 비교 및 연결

### 방어 기법 계층

| 방어 기법 | 원리 | 효과 | 비용 |
|:---:|:---:|:---:|:---:|
| [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)([Adversarial Training](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)) | 공격 샘플 포함 재훈련 | 높음 | 매우 높음 |
| 입력 정화(Input Purification) | 전처리로 노이즈 제거 | 중간 | 낮음 |
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 방어(Certified Defense) | 수학적 강건성 보증 | 높음 | 매우 높음 |
| 탐지(Adversarial [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)) | 공격 입력 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 후 거부 | 중간 | 낮음 |
| [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)([Ensemble](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) Defense) | 다수결로 강건성 향상 | 중간 | 중간 |

- **📢 섹션 요약 비유**: [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)은 권투 선수가 실전 스파링으로 내성을 기르는 것, 입력 정화는 경기장 입구에서 무기를 검색하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**고위험 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 적용**

- **자율주행**: STOP 표지판에 물리적 스티커 부착 → 인식 오류 → 사고 위험
- **악성코드 탐지**: 악성코드에 정상 코드 패턴 삽입 → [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 탐지기 우회(블랙박스 이베이전)
- **[생체 인증](/knowledge-base/studynote/09_security/uncategorized/702_biometric_authentication/)**: 얼굴 인식기에 적대적 안경 착용으로 잠금 해제

**기술사 판단 포인트**

1. **보안 수준별 방어 선택**: 금융·군사 → [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 방어(Certified Defense) 도입 고려
2. **[적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/) 비용**: 훈련 시간 3~10배 증가 → 모델 업데이트 주기와 하드웨어 계획 수립
3. **[공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)**: 사전 훈련 모델(Pre-trained Model) 도입 시 포이즈닝 여부 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 필요
4. **평가 기준**: ANSI/IEEE [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안 프레임워크에서 Robustness Accuracy 및 Certified [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 측정

- **📢 섹션 요약 비유**: 보안 카메라를 해킹하는 것처럼, AI도 공격자가 의도한 대로 보이도록 속일 수 있다 — 방어 설계는 필수다.

---

## Ⅴ. 기대효과 및 결론

적대적 공격은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 안전성에 대한 근본적 도전이다. 포이즈닝과 이베이전의 원리를 이해하고 계층적 방어 전략을 설계하는 것이 안전한 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포의 출발점이다. 적대적 강건성(Adversarial Robustness)은 향후 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 안전 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)의 핵심 평가 항목이 될 것이다.

- **📢 섹션 요약 비유**: AI에게 적대적 공격은 바이러스이고, [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)은 예방 접종이다 — 미리 맞을수록 더 안전하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [FGSM](/knowledge-base/studynote/09_security/19_ai_advanced_security/943_fgsm/) | 이베이전 공격 · 기울기 부호 기반 1회 공격 |
| [PGD](/knowledge-base/studynote/09_security/19_ai_advanced_security/944_pgd/) | 이베이전 공격 · 반복 투사 기울기 하강 |
| [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/)([Backdoor](/knowledge-base/studynote/09_security/15_malware_attack_vectors/727_backdoor/)) | 포이즈닝 공격 · [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반 오분류 |
| [적대적 훈련](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/) | 방어 · 공격 샘플 포함 재훈련 |
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 방어 | 방어 · 수학적 강건성 보증 |

### 📈 관련 키워드 및 발전 흐름도

```text
[이베이전 공격 · 기울기 부호 기반 1회 공격] → [적대적 공격: 포이즈닝과 이베이전] → [방어 · 수학적 강건성 보증]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 사람 눈에는 똑같아 보이는 고양이 사진에 아주 작은 점을 찍으면 AI가 강아지라고 착각해요 — 이게 이베이전 공격이에요.
2. 요리사가 음식을 만들기 전 재료를 살짝 오염시켜 나중에 모든 음식이 이상하게 되도록 하는 것이 포이즈닝이에요.
3. AI가 공격에 강해지려면 처음부터 이런 속임수를 많이 경험하며 훈련해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 470 / 552

← **이전**: [469. XAI, LIME, SHAP: 국소/전역 기여도 해석 (XAI LIME SHAP Local Global Attribution)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/469_xai_lime_shap_local_global_attribution/)
**다음**: [471. 연합 학습 프라이버시 보존 그래디언트 집계 (Federated Learning Privacy Gradient Aggregation)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/471_federated_learning_privacy_gradient_aggregation/) →

---
