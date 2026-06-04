---
title: "175. Reinforcement Learning from Human Feedback (RLHF) 기반 랭킹 선호 모델과 인간 라벨러 루프"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Reinforcement Learning](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) from Human Feedback ([RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/))는 인간 라벨러의 상대적 선호를 보상 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)로 바꿔, 언어모델이 "자연스러운 문장"을 넘어 "사람이 더 낫다고 느끼는 답"을 학습하게 만드는 정렬 기법이다.
> 2. **가치**: 절대 점수보다 쌍대 비교([pairwise](/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) ranking)가 일관된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 만들기 쉬워, 유용성·무해성·정직성 같은 인간 기준을 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 모델 위에 추가로 얹을 수 있다.
> 3. **판단 포인트**: RLHF의 병목은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)보다 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 운영이다. 어떤 프롬프트를 뽑고, 후보 응답을 얼마나 다양하게 만들고, 라벨러 품질과 보상 해킹을 어떻게 관리하느냐가 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

RLHF는 거대 언어 모델 ([Large Language Model](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))이 "다음 토큰을 잘 맞히는 능력"과 "사람이 선호하는 응답을 만드는 능력"이 다르다는 문제에서 출발한다. Supervised [Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) (SFT)만으로도 모델은 그럴듯한 문장을 만들 수 있지만, 친절함·간결함·안전한 거절·맥락에 맞는 판단 같은 요소는 단순 정답 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만으로 충분히 표현되지 않는다. 특히 여러 답이 모두 문법적으로 맞는 상황에서는 어떤 답이 더 좋은지 사람의 상대적 선호가 따로 필요하다.

예를 들어 같은 질문에 대해 두 개의 답이 모두 자연스러워 보여도, 하나는 장황하고 책임을 회피하고 다른 하나는 핵심과 대안을 함께 담을 수 있다. 언어모델 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)만 보면 둘 다 "가능한 문장"이지만, 사용자 입장에서는 분명 선호 순위가 갈린다. RLHF는 სწორედ 이 간극을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 수집해 모델 행동을 조정한다.

아래 그림은 왜 랭킹 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 필요한지를 직관적으로 보여준다.

```text
+----------------------------------------------------------------------+
|                 Preference appears between good answers             |
+----------------------------------------------------------------------+
| Prompt: "상사에게 일정 지연 사과 메일 초안을 써줘"                 |
| A: 장황하고 책임 회피가 섞인 답변                                  |
| B: 사유, 영향, 보완 계획이 짧게 정리된 답변                        |
|                                                                      |
| Language model likelihood: A and B can both look fluent             |
| Human preference: B > A                                              |
+----------------------------------------------------------------------+
```

즉 RLHF의 필요성은 모델이 틀린 문장을 고치는 데 있지 않다. 이미 맞는 문장들 사이에서 "어느 답이 더 사람다운가"를 고르게 하는 데 있다.

- **📢 섹션 요약 비유**: 시험에서 오답 하나를 고르는 문제는 쉬워도, 정답 후보 두 개 중 더 모범답안을 고르는 일은 선생님의 채점 기준이 필요하다. RLHF는 그 채점 기준을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 만드는 과정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) 파이프라인은 보통 네 단계로 본다. 먼저 SFT 모델을 준비하고, 그 모델이 여러 후보 답안을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하게 만든다. 그다음 인간 라벨러가 후보들을 순위화하거나 최소한 `chosen`과 `rejected` 쌍으로 비교한다. 이 선호 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [Reward Model](/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/) (보상 모델)을 학습하거나, [Direct Preference Optimization](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/) ([DPO](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/))처럼 선호 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 바로 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 최적화한다. [PPO](/studynote/10_ai/05_data_science_ml/395_ppo_clipping/) ([Proximal Policy Optimization](/studynote/10_ai/05_data_science_ml/395_ppo_clipping/))를 쓰는 전통 RLHF는 마지막 단계에서 보상 최대화와 [Kullback-Leibler Divergence](/studynote/10_ai/05_data_science_ml/347_cross_entropy_kld/) ([KL Divergence](/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/)) 제약을 함께 둔다.

아래 그림은 선호 랭킹 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 업데이트로 이어지는 루프를 요약한다.

```text
+----------------------------------------------------------------------+
|                    RLHF preference-learning loop                    |
+----------------------------------------------------------------------+
| prompt sample                                                        |
|     |                                                                |
|     +-> policy generates N responses                                 |
|     |                                                                |
|     +-> human labeler ranks / picks better answer                    |
|     |                                                                |
|     +-> (chosen, rejected) pairs                                     |
|     |                                                                |
|     +-> reward model r(x, y)  or  direct preference optimization     |
|     |                                                                |
|     +-> updated policy -> new responses -> re-evaluation             |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Prompt [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) | 어떤 질문군을 학습할지 결정 | 실제 사용자 분포, 위험 질문, 장문/단문 균형 |
| Candidate Generation | 비교할 후보 응답 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 온도, Best-of-N, 다양성 확보 |
| Human Labeler Loop | 선호 쌍 또는 순위 부여 | 가이드라인, 블라인드 평가, 품질 검수 |
| [Reward Model](/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/) | 선호 순서를 스칼라 보상으로 근사 | 과최적화 방지, 길이 편향 감시 |
| [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Optimization | 보상을 높이도록 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 갱신 | PPO의 KL 제약 또는 [DPO](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/) 사용 |
| Evaluation | 오프라인·온라인 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | Win Rate, 안전성, 사실성, 비용 |

쌍대 비교가 자주 쓰이는 이유도 여기 있다. 인간은 "5점 만점에 몇 점인가"보다 "A와 B 중 무엇이 더 나은가"를 더 일관되게 판단하는 편이다. 보상 모델은 이를 바탕으로 `P(A ≻ B | x) = σ(r(x,A) - r(x,B))` 같은 Bradley-Terry 계열 구조로 학습할 수 있다. 이때 라벨링 지침이 모호하면 보상 모델은 사람 선호가 아니라 라벨러의 습관을 학습하게 된다.

전통 RLHF에서 PPO를 쓰는 이유는 탐색을 허용하기 위해서다. 다만 보상만 무작정 높이면 모델이 지나치게 장황해지거나 보상 모델의 허점을 파고드는 Reward Hacking이 생길 수 있으므로, 기준 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 너무 멀어지지 않도록 KL 패널티를 둔다. 즉 RLHF는 강화학습이라기보다 <strong>인간 선호를 안전하게 증폭하는 제약된 최적화</strong>에 가깝다.

- **📢 섹션 요약 비유**: RLHF는 학생에게 모범답안 한 장만 주는 교육이 아니라, 답안 여러 개를 보여 주고 선생님이 무엇을 더 좋아하는지 반복해서 알려 주는 교육이다. 학생은 그 선호를 배우며 점점 더 "좋은 답" 쪽으로 습관을 바꾼다.

---

## Ⅲ. 비교 및 연결

RLHF를 정확히 이해하려면 SFT, [DPO](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/), [Reinforcement Learning](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) from [Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/) ([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) Feedback ([RLAIF](/studynote/06_ict_convergence/04_ai_llm/269_vector_database/))과의 차이를 함께 봐야 한다. SFT는 정답 예시를 모방하는 데 강하지만 선호의 미세한 차이를 반영하기 어렵고, RLHF는 보상 모델과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화를 통해 선호를 더 적극적으로 반영한다. DPO는 선호 쌍만으로 더 단순하게 학습하며, RLAIF는 인간 대신 강한 모델의 판단을 보조 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)로 활용한다.

| 방식 | 학습 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | 장점 | 약점 | 적합 상황 |
| :--- | :--- | :--- | :--- | :--- |
| SFT | 정답 데모 | 구현 단순, 안정적 | 선호 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/) 한계 | 기본 지시 수행, [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 모델 |
| [RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) ([PPO](/studynote/10_ai/05_data_science_ml/395_ppo_clipping/)) | 인간 선호 -> 보상 모델 -> [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화 | 탐색 가능, 정렬 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 높음 | 구현 복잡, 비용 큼 | 대화형 모델 정렬, 복합 보상 |
| [DPO](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/) | 선호 쌍에서 직접 최적화 | 단순하고 안정적 | 탐색/온라인 적응은 제한적 | 선호 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 충분한 후속 튜닝 |
| [RLAIF](/studynote/06_ict_convergence/04_ai_llm/269_vector_database/) | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 판정 기반 선호 | 확장성 좋음, 비용 절감 | 모델 편향 전이 위험 | 인간 평가 보강, 대규모 재평가 |

또 하나의 비교 축은 <strong>평가 방식</strong>이다. 절대 점수형 레이블은 기준 편차가 크고 라벨러마다 3점·4점 사용 습관이 달라질 수 있다. 반면 [Pairwise](/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) Ranking은 판단 기준을 상대화해 일관성을 높인다. 대신 후보 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 단조로우면 의미 있는 선호 정보가 적어지므로, 후보 다양성을 확보하는 샘플링 전략이 같이 필요하다.

이 구조는 추천 시스템의 [Learning](/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) to Rank와도 닮아 있다. 다만 RLHF는 클릭률만 보는 것이 아니라, 안전성·사실성·협조성처럼 다차원적 인간 가치를 함께 다뤄야 한다는 점이 더 어렵다. 그래서 보상 모델 하나가 모든 가치를 완벽히 대변한다고 보기보다, 정렬 파이프라인의 중간 근사치로 이해해야 한다.

- **📢 섹션 요약 비유**: SFT는 모범답안 베껴 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 연습이고, RLHF는 여러 답안 중 선생님이 더 좋아하는 답을 반복해서 배우는 과정이다. DPO는 채점표만 보고 바로 연습하는 지름길이고, RLAIF는 선배 조교가 대신 채점해 주는 방식에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 RLHF의 난점은 모델보다 운영이다. 어떤 프롬프트를 샘플링할지 잘못 정하면, 모델은 자주 쓰는 질문이 아니라 평가하기 쉬운 질문만 잘하게 된다. 후보 응답이 지나치게 비슷하면 라벨러는 의미 있는 순위를 매기기 어렵고, 반대로 너무 품질이 낮으면 보상 모델이 미세한 선호를 배우지 못한다. 결국 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집, 라벨러 품질 관리, 안전성 통제가 핵심 운영 과제가 된다.

| 운영 체크포인트 | 왜 중요한가 | 권장 판단 |
| :--- | :--- | :--- |
| 프롬프트 샘플링 | 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분포를 반영해야 함 | 운영 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 위험 질문, 장문 태스크를 함께 섞는다. |
| 후보 다양성 | 선호 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)의 정보량 결정 | [Temperature](/studynote/10_ai/05_data_science_ml/386_llm_temperature/), Best-of-N, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 혼합으로 차이를 만든다. |
| 라벨러 품질 | 보상 모델의 [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/) | 골든셋, 교차 검수, 불일치 분석을 정기 수행한다. |
| 안전 콘텐츠 처리 | 평가자 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)와 규정 준수 | 민감 주제는 별도 가이드와 에스컬레이션 경로를 둔다. |
| 보상 해킹 감시 | 길이 편향, 아첨 편향 방지 | Win Rate와 응답 길이 상관관계, KL Drift를 함께 본다. |

아래 흐름은 어떤 선호 학습 방식을 선택할지 실무적으로 판단하는 기준이다.

```text
+----------------------------------------------------------------------+
|                 Preference optimization decision                    |
+----------------------------------------------------------------------+
| enough human preference pairs?                                       |
|   +- no  -> collect / bootstrap with SFT or RLAIF                    |
|   +- yes + simple pipeline wanted -> DPO first                       |
|   +- yes + reward shaping / exploration needed -> RLHF with PPO      |
|   +- label budget too small -> AI assist + human audit               |
+----------------------------------------------------------------------+
```

판단 포인트는 세 가지로 요약된다. 첫째, <strong>라벨링 기준의 명확성</strong>이 모델 구조보다 우선이다. "좋은 답"의 정의가 모호하면 RLHF는 편향만 증폭한다. 둘째, **DPO와 RLHF를 구분해야 한다**. 선호 쌍이 이미 충분하고 안정적이면 DPO가 더 단순할 수 있지만, 탐색과 복합 보상 설계가 필요하면 RLHF가 여전히 유리하다. 셋째, <strong>라벨러 운영 비용과 심리 부담</strong>을 설계 안에 포함해야 한다. 유해 콘텐츠 평가를 대규모로 다루는 조직은 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치 없이는 지속 가능하지 않다.

기술사 답안에서는 RLHF를 "인간 피드백으로 강화학습한다" 수준에서 멈추지 말고, <strong>프롬프트 샘플링, 후보 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>, <a href="/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/">Pairwise</a> Ranking, <a href="/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/">Reward Model</a>, KL 제약, 보상 해킹, 라벨러 품질 관리</strong>까지 연결해 설명해야 깊이가 생긴다.

- **📢 섹션 요약 비유**: 학원을 운영할 때도 문제집만 좋다고 끝나지 않는다. 어떤 문제를 뽑고, 선생님이 어떻게 채점하고, 학생이 꼼수를 쓰지 못하게 어떤 규칙을 둘지가 성적을 좌우한다. RLHF도 바로 그런 운영 설계의 문제다.

---

## Ⅴ. 기대효과 및 결론

RLHF가 잘 작동하면 모델은 단순히 자연스러운 문장을 넘어서, 사용자가 더 선호하는 응답 패턴을 안정적으로 낸다. 도움말의 밀도, 거절의 안전성, 대화의 친절함, 불확실성 표현 같은 영역에서 품질 차이가 뚜렷하게 나타난다. 특히 동일한 기반 모델이라도 선호 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 보상 설계가 좋으면 체감 품질이 크게 달라질 수 있다.

하지만 한계도 분명하다. 인간 선호는 문화와 맥락에 따라 달라지고, 라벨러 집단이 바뀌면 보상 모델의 성격도 달라진다. 또한 Reward Hacking, 길이 편향, 과도한 순응성, 사실성 저하 같은 부작용이 생길 수 있다. 따라서 RLHF는 "한 번 학습해 끝나는 기술"이 아니라, 지속적으로 평가·수정·재수집하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 운영 루프로 봐야 한다.

결국 이 주제의 핵심은 강화학습 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 그 자체보다, 인간 선호를 신뢰할 수 있는 랭킹 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 만들고 그 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 안전하게 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 개선에 연결하는 데 있다. RLHF는 모델 학습이면서 동시에 평가 체계와 라벨링 공정의 설계다.

- **📢 섹션 요약 비유**: 좋은 코치를 둔 운동선수는 무작정 연습량만 늘리지 않는다. 어떤 동작이 더 좋은지 세밀한 피드백을 받고, 그 피드백이 쌓이면서 실력이 방향 있게 좋아진다. RLHF는 AI에게 그런 코치를 붙이는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| SFT (Supervised [Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) | [RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) 이전 단계에서 기본 지시 수행 능력을 만든다. |
| [Pairwise](/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) Ranking | 인간이 절대 점수보다 일관되게 선호를 표현하기 쉬운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식이다. |
| [Reward Model](/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/) | 선호 순서를 스칼라 보상으로 근사해 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화의 기준을 제공한다. |
| [PPO](/studynote/10_ai/05_data_science_ml/395_ppo_clipping/) ([Proximal Policy Optimization](/studynote/10_ai/05_data_science_ml/395_ppo_clipping/)) | 보상 최대화와 KL 제약을 함께 두는 전통 [RLHF](/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) 최적화 방식이다. |
| [DPO](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/) ([Direct Preference Optimization](/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/)) | 보상 모델 없이 선호 쌍으로 직접 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 조정하는 단순화 대안이다. |
| [RLAIF](/studynote/06_ict_convergence/04_ai_llm/269_vector_database/) ([Reinforcement Learning](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) from [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Feedback) | 인간 라벨 부족을 보완하기 위해 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 평가를 활용하는 확장 방식이다. |
| Reward Hacking | 모델이 사람 선호가 아니라 보상 모델의 허점을 공략하는 현상이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Supervised fine-tuning
    |
    v
Candidate response sampling
    |
    v
Human preference ranking and gold-set validation
    |
    v
Reward model or direct preference optimization
    |
    v
Aligned LLM with continuous feedback loop
```

### 👶 어린이를 위한 3줄 비유 설명

1. RLHF는 AI에게 여러 답안을 보여 주고 사람 선생님이 "이 답이 더 좋아"라고 계속 알려 주는 공부법이에요.
2. AI는 그 순서를 배우면서 그냥 말이 되는 답보다 사람이 더 좋아하는 답을 하려고 해요.
3. 그래서 선생님이 무엇을 좋은 답이라고 보는지 잘 정하는 것이 아주 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 175 / 258

<- **이전**: [174. LLMOps (Large Language Model Operations) - 프롬프트 템플릿 관리, RAG 벡터 DB 동기화,](/studynote/14_data_engineering/04_mlops/174_llmops_prompt_template_rag_pipeline/)
**다음**: [176. AutoML (Automated Machine Learning) 하이퍼파라미터 최적화 베이지안 탐색](/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) ->

---
