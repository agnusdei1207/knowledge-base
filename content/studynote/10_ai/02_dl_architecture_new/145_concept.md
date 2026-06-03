+++
title = "145. RLHF (Reinforcement Learning from Human Feedback) - 인간 정렬"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RLHF는 <strong>인간 평가자의 선호도 피드백으로 보상 모델(<a href="/knowledge-base/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/">Reward Model</a>)을 학습</strong>하고, 이를 기반으로 <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a>(<a href="/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">Proximal Policy Optimization</a>) 강화학습</strong>으로 LLM을 인간 의도에 정렬(Align)하는 기법이다.
> 2. **가치**: 사전 학습된 LLM은 <strong>유해·편향·비관련 출력</strong>을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 수 있지만, RLHF는 "인간이 선호하는 답변"을 학습하여 <strong>ChatGPT 수준의 안전하고 유용한 대화</strong>를 가능하게 했다.
> 3. **판단 포인트**: SFT(Supervised [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))→[RM](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/)([Reward Model](/knowledge-base/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/)) 학습→[PPO](/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/) 정렬의 3단계이며, [DPO](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/)([Direct Preference Optimization](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/))가 [RM](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/) 없이 직접 정렬하는 간소화 대안이다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RLHF 3단계:</div>
<div class="kb-diagram-note">1. SFT: 지시-응답 쌍으로 기본 능력 학습</div>
<div class="kb-diagram-note">2. Reward Model: 인간 선호(A&gt;B) 비교 데이터 → RM 학습</div>
<div class="kb-diagram-note">3. PPO: RM 점수를 보상으로 LLM 강화학습 → 정렬</div>
<div class="kb-diagram-note">DPO: RM 없이 선호 데이터로 직접 정렬 (간소화)</div>
</div>
</div>



- **📢 섹션 요약 비유**: RLHF는 <strong>반려견 교육</strong>이다. 좋은 행동(선호 답변)에 간식(보상)을 주고, 나쁜 행동(유해 답변)을 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)한다.

---

## Ⅱ~Ⅴ. 결론

RLHF는 <strong>ChatGPT의 핵심 기술</strong>이며, DPO가 간소화 대안으로 부상 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/">RLHF</a></strong> | 인간 피드백 강화학습 |
| <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/">Reward Model</a></strong> | 선호도 점수화 |
| <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a></strong> | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/270_embedding_model/">DPO</a></strong> | 직접 정렬 (간소화) |
| **Alignment** | 인간 의도 정렬 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">InstructGPT (RLHF, 2022)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ChatGPT (2022)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">DPO (2023, RM 불필요)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">KTO (2024, 비교 불필요)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: Constitutional AI (Anthropic)</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. RLHF는 <strong>반려견 교육</strong>이에요. 좋은 행동에 <strong>간식(보상)</strong>을 줘요.
2. "이 답변이 더 좋아" 하고 **사람이 골라주면** AI가 배워요.
3. 이렇게 배워서 ChatGPT가 **예의 바르고 유용한** 답을 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 420

← **이전**: [144. RAG (Retrieval-Augmented Generation) - 검색 증강 생성](/knowledge-base/studynote/10_ai/02_dl_architecture_new/144_concept/)
**다음**: [146. CoT (Chain-of-Thought) 프롬프팅 - 단계별 추론](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/) →

---
