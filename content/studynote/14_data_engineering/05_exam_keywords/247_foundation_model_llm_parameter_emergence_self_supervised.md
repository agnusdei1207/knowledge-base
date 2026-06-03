+++
title = "247. 파운데이션 모델 (Foundation Model) LLM 파라미터 창발성 (Emergence) 자기 지도 학습"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)([Foundation Model](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/))은 방대한 비라벨 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)([Self-Supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/))을 통해 사전 훈련된 후, 다양한 다운스트림 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에 적응할 수 있는 범용 기반 모델이다.
> 2. **가치**: [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 법칙(Scaling Law)에 따라 파라미터 수·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·연산량이 동시에 증가하면 예측 손실이 멱함수적으로 감소하며, 특정 규모 이상에서 계획되지 않은 능력인 [창발성](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/265_emergent_abilities/)(Emergence)이 나타난다.
> 3. **판단 포인트**: [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))의 실용화 핵심은 파인튜닝 없이 프롬프트만으로 새 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)를 수행하는 제로샷(Zero-Shot)/퓨샷(Few-Shot) 능력이며, 이는 스케일이 충분히 클 때 창발한다.

---

## Ⅰ. 개요 및 필요성

2021년 Stanford [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Lab의 논문 "On the Opportunities and Risks of Foundation Models"(Bommasani et al.)이 [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 개념을 체계화했다. 이 전에는 [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 같은 대형 모델들이 등장했지만 이 개념으로 통합되지 않았었다.

### 기존 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) vs [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 패러다임



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기존 패러다임</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">태스크 A 데이터 → 모델 A (분류기)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">태스크 B 데이터 → 모델 B (NER)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">태스크 C 데이터 → 모델 C (번역기)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">태스크마다 별도 모델 훈련 필요</div></div>
<div class="kb-diagram-note">파운데이션 모델 패러다임</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">파운데이션 모델</div><div class="kb-diagram-note">(사전학습)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분류기 NER 번역</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(파인튜닝) (프롬프팅) (파인튜닝)</div></div>
</div>
</div>



| 특성 | 기존 모델 | [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) |
|:---|:---|:---|
| 훈련 방식 | [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/), [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 특화 | [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/), 범용 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 라벨링 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요 | 비라벨 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| 적응 방법 | 처음부터 재훈련 | 파인튜닝 or 프롬프팅 |
| 범용성 | 단일 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) | 다양한 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) |

📢 **섹션 요약 비유**: [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 백과사전을 모두 읽은 박사와 같다. 모든 분야를 알기 때문에 "의사", "변호사", "번역가" 역할을 조금만 가르쳐 주면(파인튜닝/프롬프팅) 빠르게 습득한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/) ([Self-Supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/))

라벨 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체에서 학습 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">방법 1: 마스킹 언어 모델 (Masked Language Modeling, MLM) — BERT 계열</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">입력: "나는</div><div class="kb-diagram-node">MASK</div><div class="kb-diagram-note">에 간다"</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">목표: "</div><div class="kb-diagram-node">MASK</div><div class="kb-diagram-note">" = "학교" 예측</div></div>
<div class="kb-diagram-note">→ 양방향 문맥 이해</div>
<div class="kb-diagram-note">방법 2: 다음 토큰 예측 (Next Token Prediction) — GPT 계열</div>
<div class="kb-diagram-note">입력: "나는 학교에"</div>
<div class="kb-diagram-note">목표: "간다" 예측</div>
<div class="kb-diagram-note">→ 인과적 언어 모델 (Causal LM)</div>
<div class="kb-diagram-note">→ 자동 회귀 생성 가능</div>
<div class="kb-diagram-note">방법 3: 노이즈 제거 (Denoising) — T5, BART 계열</div>
<div class="kb-diagram-note">입력: "나는 &lt;blank&gt; 에 간다" (랜덤 스팬 마스킹)</div>
<div class="kb-diagram-note">목표: "학교" 복원</div>
</div>
</div>



### [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 법칙 (Scaling Law)

Kaplan et al., OpenAI 2020 연구:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">L(N, D, C) ≈ (N_c/N)^{α_N} + (D_c/D)^{α_D} + L_∞</div>
<div class="kb-diagram-note">L: 손실, N: 파라미터 수, D: 데이터 크기, C: 연산량</div>
<div class="kb-diagram-note">α_N ≈ 0.076 (파라미터 스케일링 지수)</div>
<div class="kb-diagram-note">α_D ≈ 0.095 (데이터 스케일링 지수)</div>
<div class="kb-diagram-note">→ 파라미터·데이터·연산 세 요소를 균형 있게 스케일</div>
<div class="kb-diagram-note">→ 모델 크기만 늘리면 데이터가 병목</div>
</div>
</div>





<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">스케일링에 따른 성능 향상 (개념도)</div>
<div class="kb-diagram-note">창발성 출현 임계점</div>
<div class="kb-diagram-note">손실 ↓</div>
<div class="kb-diagram-note">╲</div>
<div class="kb-diagram-note">╲── (특정 스케일 이상에서</div>
<div class="kb-diagram-note">╲ 예상치 못한 능력 출현)</div>
<div class="kb-diagram-note">╲</div>
<div class="kb-diagram-note">모델 크기 (파라미터 수)</div>
</div>
</div>



### [창발성](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/265_emergent_abilities/) (Emergence) 현상



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">창발적 능력 예시 (파라미터 임계점)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">능력</div><div class="kb-diagram-cell">임계점 규모</div><div class="kb-diagram-cell">이전 성능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3자리 덧셈</div><div class="kb-diagram-cell">~10B</div><div class="kb-diagram-cell">무작위 수준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">다단계 추론 (CoT)</div><div class="kb-diagram-cell">~100B</div><div class="kb-diagram-cell">실패</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">맥락 학습 (ICL)</div><div class="kb-diagram-cell">~10B</div><div class="kb-diagram-cell">미미</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">코드 생성</div><div class="kb-diagram-cell">~12B</div><div class="kb-diagram-cell">낮음</div></div>
<div class="kb-diagram-note">창발성의 특징:</div>
<div class="kb-diagram-tree-item" style="--depth:1">선형적 증가가 아닌 갑작스러운 질적 전환</div>
<div class="kb-diagram-tree-item" style="--depth:1">사전에 예측 어려움</div>
<div class="kb-diagram-tree-item" style="--depth:1">훈련 목표에 포함되지 않은 능력 출현</div>
</div>
</div>



📢 **섹션 요약 비유**: [창발성](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/265_emergent_abilities/)은 모래 더미와 같다. 모래알 하나, 둘을 쌓을 때는 그냥 모래더미지만, 어느 순간 갑자기 "모래성"이 된다. 파라미터도 일정 규모를 넘으면 갑자기 새로운 능력이 나타난다.

---

## Ⅲ. 비교 및 연결

### 주요 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) ([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 비교

| 모델 | 기관 | 출시 | 파라미터 | 특징 |
|:---|:---|:---|:---|:---|
| [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-3 | OpenAI | 2020 | 175B | 퓨샷 학습의 등장 |
| PaLM | Google | 2022 | 540B | [Chain-of-Thought](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/) 창발 |
| [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 | OpenAI | 2023 | ~1.8T(추정) | [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/), 고성능 |
| Claude 3 | Anthropic | 2024 | 비공개 | 안전성·헌법적 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| LLaMA 3 | Meta | 2024 | 8B~70B | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |
| Gemini Ultra | Google | 2024 | 비공개 | [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) 강점 |

### [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 내 학습 (In-Context [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/), ICL)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">제로샷 (Zero-Shot):</div>
<div class="kb-diagram-note">프롬프트: "다음 문장의 감정을 분류하세요: '오늘 정말 슬프다'"</div>
<div class="kb-diagram-note">→ 예시 없이 바로 수행</div>
<div class="kb-diagram-note">퓨샷 (Few-Shot):</div>
<div class="kb-diagram-note">프롬프트: "긍정: '오늘 너무 행복해'</div>
<div class="kb-diagram-note">부정: '정말 짜증나'</div>
<div class="kb-diagram-note">다음: '오늘 정말 슬프다' → "</div>
<div class="kb-diagram-note">→ 2~5개 예시로 태스크 정의</div>
</div>
</div>



📢 **섹션 요약 비유**: ICL은 새로운 직원에게 입사 첫날 "이렇게 이렇게 해줘"라고 몇 가지 예시를 보여주면 바로 이해하는 것이다. 두꺼운 매뉴얼(파인튜닝) 없이도 바로 일한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 배포 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">애플리케이션 레이어</div>
<div class="kb-diagram-note">사용자 인터페이스 / API</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">프롬프트 엔지니어링 레이어</div>
<div class="kb-diagram-note">System Prompt + Few-Shot + RAG 컨텍스트</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">LLM API / 추론 레이어</div>
<div class="kb-diagram-note">GPT-4 API / 자체 호스팅 LLaMA</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">인프라 레이어</div>
<div class="kb-diagram-note">GPU 클러스터 (H100/A100) + 고속 스토리지</div>
</div>
</div>



### [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)

| [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | 설명 | 대응 방안 |
|:---|:---|:---|
| [환각](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/275_react_framework/) ([Hallucination](/knowledge-base/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/)) | 그럴듯한 오정보 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/), 팩트 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 편향 ([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/)) | 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 편향 반영 | [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/), 헌법적 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| [저작권](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/583_ai_code_license_security_threats/) | 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포함 저작물 | 라이선스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사용 |
| 보안 | [프롬프트 인젝션 공격](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/302_prompt_injection_jailbreak/) | [입력 검증](/knowledge-base/studynote/09_security/uncategorized/601_input_validation/), 가드레일 |
| 비용 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 추론 비용 | [모델 양자화](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/312_quantization/), [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) |

📢 **섹션 요약 비유**: [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 배포는 강력한 인턴 고용과 같다. 엄청난 지식을 가졌지만(능력), 때로 자신감 있게 틀린 말을 하고([환각](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/275_react_framework/)), 과거 경험의 편견이 있을 수 있어(편향) 항상 감독이 필요하다.

---

## Ⅴ. 기대효과 및 결론

### [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)의 사회적 영향



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">산업 적용</div>
<div class="kb-diagram-tree-item" style="--depth:1">코드 생성 (GitHub Copilot, Cursor)</div>
<div class="kb-diagram-tree-item" style="--depth:1">의료 진단 보조 (Med-PaLM)</div>
<div class="kb-diagram-tree-item" style="--depth:1">법률 문서 분석 (Harvey AI)</div>
<div class="kb-diagram-tree-item" style="--depth:1">교육 개인화 (Khan Academy Khanmigo)</div>
<div class="kb-diagram-tree-item" style="--depth:1">과학 연구 가속 (AlphaFold, GNoME)</div>
<div class="kb-diagram-note">경제적 영향</div>
<div class="kb-diagram-note">McKinsey: 생성 AI 연간 2.6~4.4조 달러 경제 가치 창출 (2023)</div>
</div>
</div>



### 기술사 시험 핵심 포인트

1. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/">파운데이션 모델</a> 정의</strong>: Stanford [2021](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/), 범용 기반 모델
2. <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/">자기 지도 학습</a> 방법</strong>: [MLM](/knowledge-base/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/), 다음 토큰 예측, 디노이징
3. <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> 법칙</strong>: 파라미터·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·연산 균형 스케일
4. <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/265_emergent_abilities/">창발성</a> 특징</strong>: 임계점 이상에서 갑작스러운 능력 출현
5. **Zero-Shot vs Few-Shot**: 예시 없음 vs 소수 예시 학습

📢 **섹션 요약 비유**: [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 인류 지식의 증류(Distillation)다. 인터넷의 수조 개 문장을 읽고 그 패턴을 수백억 개의 파라미터에 압축했다. 이 지식의 결정체가 적절한 자극(프롬프트)에 반응해 새로운 지식을 창출한다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 개념 | [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) ([Foundation Model](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)) | 범용 사전 학습 기반 모델 |
| 학습 방법 | [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/) ([Self-Supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)) | 라벨 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 내부에서 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 주요 인스턴스 | [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) ([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) | 언어 특화 [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) |
| 설계 법칙 | [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 법칙 (Scaling Law) | 규모 증가에 따른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 |
| 창발 현상 | [창발성](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/265_emergent_abilities/) (Emergence) | 예측 불가능한 능력 갑작스러운 출현 |
| 적응 방법 | 파인튜닝 ([Fine-Tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 추가 훈련 |
| 활용 방법 | 인컨텍스트 학습 (ICL) | 프롬프트 내 예시로 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 정의 |
| 핵심 위험 | [환각](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/275_react_framework/) ([Hallucination](/knowledge-base/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/)) | 그럴듯한 오정보 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

### 👶 어린이를 위한 3줄 비유 설명
1. [파운데이션 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 도서관의 모든 책을 다 읽은 학생이야. 수학, 국어, 과학, 역사 모두 알기 때문에 어떤 과목 시험도 조금만 연습하면 잘 볼 수 있어.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Task-Specific 모델 (한 가지 용도)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Foundation Model: 대규모 자기지도 사전학습</div>
<div class="kb-diagram-tree-item" style="--depth:2">파라미터 스케일: 1B → 100B → 1T+</div>
<div class="kb-diagram-tree-item" style="--depth:2">창발 능력 (Emergence): 규모 증가 시 새 능력</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Fine-Tuning · Prompt Engineering · In-Context Learning</div>
</div>
</div>


2. [창발성](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/265_emergent_abilities/)은 레고 블록과 같아. 블록 몇 개로는 별로 못 만들지만, 아주 많이 모이면 갑자기 성이나 로켓 같은 것을 만들 수 있게 되는 마법 같은 일이야.
3. 제로샷 학습은 설명서 없이 새 게임을 켰는데 이전에 비슷한 게임을 많이 해봐서 바로 잘 하는 것이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 247 / 258

← **이전**: [246. 트랜스포머 (Transformer) 셀프 어텐션 병렬 처리 포지셔널 인코딩](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)
**다음**: [248. BERT 인코더 MLM vs GPT 디코더 자동 회귀 (Autoregressive) 심화 비교](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/) →

---
