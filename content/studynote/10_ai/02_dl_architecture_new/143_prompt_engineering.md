+++
title = "143. 프롬프트 엔지니어링 (Prompt Engineering) - LLM 활용의 핵심"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [프롬프트 엔지니어링](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)은 **LLM에 입력하는 지시문(Prompt)을 체계적으로 설계**하여 원하는 출력을 얻는 기법이며, [Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-shot·Few-shot·[CoT](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/)([Chain-of-Thought](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/))가 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 같은 모델이라도 프롬프트에 따라 **출력 품질이 10배+ 차이**가 나며, 모델 재학습 없이 **프롬프트만으로 새 작업에 적응**할 수 있어 비용 효율적이다.
> 3. **판단 포인트**: [CoT](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/)("단계별로 생각해봐")가 추론 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 향상시키며, 역할 부여("너는 전문 편집자야")·출력 형식 지정([JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/))·Few-shot 예시가 실무 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
Zero-shot: 예시 없이 지시만 제공
Few-shot: 2~5개 입출력 예시 제공
CoT: "단계별로 생각해 봐" → 추론 과정 명시
역할 부여: "너는 시니어 백엔드 개발자야"
출력 형식: "JSON으로 응답해 줘"
```

- **📢 섹션 요약 비유**: [프롬프트 엔지니어링](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)은 **AI에게 잘 질문하는 기술**이다. 질문이 좋아야 답이 좋다.

---

## Ⅱ~Ⅴ. 결론

[프롬프트 엔지니어링](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)은 **[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 활용의 가장 비용 효율적 방법**이며, [CoT](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/)·Few-shot·역할 부여가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-shot** | 예시 없이 |
| **Few-shot** | 예시 제공 |
| **[CoT](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/)** | 추론 과정 명시 |
| **역할 부여** | 페르소나 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| **구조화 출력** | [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 지정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Zero/Few-shot (GPT-3, 2020)] → [CoT (2022)]
    → [Self-Consistency (2023)] → [Tree-of-Thought (2023)]
    → [현재: Agent Prompt — 도구 호출·반복 추론]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [프롬프트 엔지니어링](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)은 **AI에게 잘 질문**하는 거예요.
2. "단계별로 생각해 봐([CoT](/knowledge-base/studynote/10_ai/02_dl_architecture_new/146_chain_of_thought_cot/))"라고 하면 **더 정확한 답**을 줘요.
3. **좋은 질문 = 좋은 답** — 질문하는 기술이 중요해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 420

← **이전**: [142. LLM 스케일링 법칙 & Emergence - 규모의 법칙과 창발](/knowledge-base/studynote/10_ai/02_dl_architecture_new/142_concept/)
**다음**: [144. RAG (Retrieval-Augmented Generation) - 검색 증강 생성](/knowledge-base/studynote/10_ai/02_dl_architecture_new/144_concept/) →

---
