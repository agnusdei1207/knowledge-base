---
title: 143. 프롬프트 엔지니어링 (Prompt Engineering) - LLM 활용의 핵심
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]은 **LLM에 입력하는 지시문(Prompt)을 체계적으로 설계**하여 원하는 출력을 얻는 기법이며, [[585_zero_skipping|Zero]]-shot·Few-shot·[[146_chain_of_thought_cot|CoT]]([[146_chain_of_thought_cot|Chain-of-Thought]])가 핵심 [[268_strategy_pattern|전략]]이다.
> 2. **가치**: 같은 모델이라도 프롬프트에 따라 **출력 품질이 10배+ 차이**가 나며, 모델 재학습 없이 **프롬프트만으로 새 작업에 적응**할 수 있어 비용 효율적이다.
> 3. **판단 포인트**: [[146_chain_of_thought_cot|CoT]]("단계별로 생각해봐")가 추론 [[282_performance_tactics|성능]]을 크게 향상시키며, 역할 부여("너는 전문 편집자야")·출력 형식 지정([[343_json|JSON]])·Few-shot 예시가 실무 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
Zero-shot: 예시 없이 지시만 제공
Few-shot: 2~5개 입출력 예시 제공
CoT: "단계별로 생각해 봐" → 추론 과정 명시
역할 부여: "너는 시니어 백엔드 개발자야"
출력 형식: "JSON으로 응답해 줘"
```

- **📢 섹션 요약 비유**: [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]은 **AI에게 잘 질문하는 기술**이다. 질문이 좋아야 답이 좋다.

---

## Ⅱ~Ⅴ. 결론

[[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]은 **[[263_llm_large_language_model|LLM]] 활용의 가장 비용 효율적 방법**이며, [[146_chain_of_thought_cot|CoT]]·Few-shot·역할 부여가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[585_zero_skipping|Zero]]-shot** | 예시 없이 |
| **Few-shot** | 예시 제공 |
| **[[146_chain_of_thought_cot|CoT]]** | 추론 과정 명시 |
| **역할 부여** | 페르소나 [[009_config|설정]] |
| **구조화 출력** | [[343_json|JSON]] 지정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Zero/Few-shot (GPT-3, 2020)] → [CoT (2022)]
    → [Self-Consistency (2023)] → [Tree-of-Thought (2023)]
    → [현재: Agent Prompt — 도구 호출·반복 추론]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]은 **AI에게 잘 질문**하는 거예요.
2. "단계별로 생각해 봐([[146_chain_of_thought_cot|CoT]])"라고 하면 **더 정확한 답**을 줘요.
3. **좋은 질문 = 좋은 답** — 질문하는 기술이 중요해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 420

← **이전**: [[142_concept|142. LLM 스케일링 법칙 & Emergence - 규모의 법칙과 창발]]
**다음**: [[144_concept|144. RAG (Retrieval-Augmented Generation) - 검색 증강 생성]] →

---
