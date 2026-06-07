---
title: "Adam Optimizer"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 132
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/)([Adaptive Moment Estimation](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/))은 <strong><a href="/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/">Momentum</a>(1차 모멘트, 이동 평균) + RMSProp(2차 모멘트, 기울기 제곱 이동 평균)</strong>을 결합한 적응형 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)이며, 파라미터별로 <strong><a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a>을 자동 조정</strong>한다.
> 2. **가치**: SGD는 모든 파라미터에 같은 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 적용하여 **희소 기울기·비등방 공간에서 수렴이 느리지만**, Adam은 각 파라미터에 적합한 [학습률](/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)을 자동 계산하여 <strong>빠르고 안정적</strong>으로 수렴한다.
> 3. **판단 포인트**: AdamW([Weight Decay](/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/) 분리)가 [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 학습의 사실상 표준이며, β₁=0.9·β₂=0.999·lr=1e-3이 기본 하이퍼파라미터이다.

---

## Ⅰ. 개요 및 필요성

```text
Adam = Momentum + RMSProp
  m = β₁·m + (1-β₁)·g      (1차 모멘트, 방향)
  v = β₂·v + (1-β₂)·g^     (2차 모멘트, 크기)
  θ = θ - lr · m̂/√(v̂+ε)    (업데이트)
```

- **📢 섹션 요약 비유**: Adam은 <strong>내비게이션</strong>이다. 방향([Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/))과 속도(RMSProp)를 자동으로 조절하여 목적지(최솟값)에 빠르게 도착한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | SGD | [Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/) |
|:---|:---|:---|
| <strong><a href="/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/">학습률</a></strong> | 고정 | **적응형** |
| **방향** | 현재 기울기 | **이동 평균 (안정)** |
| **수렴** | 느림 | **빠름** |

---

## Ⅲ~Ⅴ. 결론

[Adam](/studynote/10_ai/03_llm_nlp/277_adam_optimizer/)/AdamW는 <strong>딥러닝 학습의 사실상 표준 <a href="/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/">옵티마이저</a></strong>이며, [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)·[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 학습에 필수이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/10_ai/03_llm_nlp/277_adam_optimizer/">Adam</a></strong> | [Momentum](/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/) + RMSProp |
| **AdamW** | [Weight Decay](/studynote/10_ai/01_ai_basics/091_l1_l2_regularization_weight_decay/) 분리 |
| <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a> Rate</strong> | 학습 보폭 |
| <strong><a href="/studynote/06_ict_convergence/04_ai_llm/309_cosine_annealing/">Cosine Annealing</a></strong> | LR [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) |
| **Lion** | 차세대 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[SGD (1951)] -> [Momentum (1964)] -> [AdaGrad (2011)]
    -> [RMSProp (2012)] -> [Adam (2014)]
    -> [AdamW (2018)] -> [현재: Lion·Sophia — 메모리 효율^]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Adam은 <strong>내비게이션</strong>이에요. 방향과 속도를 **자동으로** 조절해줘요.
2. SGD는 지도 없이 걷기(느림), Adam은 <strong>내비 따라 운전하기(빠름)</strong>예요.
3. 거의 모든 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습에서 <strong>Adam이 기본 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>으로 쓰인답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 258

<- **이전**: [131. 손실 함수·옵티마이저·경사 하강법 - 딥러닝 학습의 3대 축](/studynote/14_data_engineering/03_ml_dl_llm/131_loss_function_optimizer_gradient_descent/)
**다음**: [133. 역전파 & 연쇄 법칙 (Backpropagation & Chain Rule)](/studynote/14_data_engineering/03_ml_dl_llm/133_backpropagation_chain_rule/) ->

---
