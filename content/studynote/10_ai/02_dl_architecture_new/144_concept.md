---
title: 144. RAG (Retrieval-Augmented Generation) - 검색 증강 생성
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RAG는 **LLM이 답변 [[087_process_state_transition|생성]] 전에 외부 지식 저장소(벡터 DB)에서 관련 문서를 검색(Retrieve)하여 프롬프트에 포함**시킨 후 [[087_process_state_transition|생성]](Generate)하는 기법이며, [[275_react_framework|환각]]([[345_llm_foundation_model_hallucination|Hallucination]])을 줄이고 최신 정보를 반영한다.
> 2. **가치**: LLM의 파라메트릭 지식은 **학습 시점에 고정**되지만, RAG는 **외부 DB를 실시간 [[316_reference_pattern_nosql|참조]]**하여 학습 이후의 최신 정보·사내 문서·[[064_relation_domain|도메인]] 지식을 반영한다.
> 3. **판단 포인트**: Naive [[276_fine_tuning|RAG]](단순 검색)→[[218_rag_advanced_techniques|Advanced RAG]]([[298_qkv_attention|쿼리]] 변환·리랭킹·청킹 최적화)→Modular [[276_fine_tuning|RAG]]([[123_pipe|파이프]]라인 [[192_module_independence|모듈]]화)로 진화하며, [[278_instruction_tuning|임베딩]] 모델·벡터 DB(Pinecone·Chroma)가 핵심 인프라이다.

---

## Ⅰ. 개요 및 필요성

```text
RAG 파이프라인:
  1. 문서 → 청킹 → 임베딩 → 벡터 DB 저장 (오프라인)
  2. 사용자 질문 → 임베딩 → 벡터 DB 유사도 검색 (온라인)
  3. Top-K 문서 + 질문 → LLM 프롬프트 → 답변 생성
```

- **📢 섹션 요약 비유**: RAG는 **오픈북 시험**이다. 시험(질문) 중 교과서(문서)를 참고하여 더 정확한 답을 쓴다.

---

## Ⅱ~Ⅴ. 결론

RAG는 **[[263_llm_large_language_model|LLM]] [[275_react_framework|환각]] 해결·최신 지식 반영의 핵심 기법**이며, [[278_instruction_tuning|임베딩]]+벡터DB+리랭킹이 [[123_pipe|파이프]]라인의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[276_fine_tuning|RAG]]** | 검색+[[087_process_state_transition|생성]] |
| **벡터 DB** | [[278_instruction_tuning|임베딩]] 저장·검색 |
| **청킹** | 문서 분할 |
| **리랭킹** | 검색 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 향상 |
| **[[275_react_framework|환각]]** | RAG의 핵심 해결 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
[LLM 환각 문제] → [RAG (Lewis et al., 2020)]
    → [LangChain/LlamaIndex (2023)]
    → [Advanced RAG (리랭킹·HyDE, 2023)]
    → [현재: Agentic RAG — 자율 검색·도구 호출]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RAG는 **오픈북 시험**이에요. 교과서(문서)를 보면서 답을 써요.
2. 교과서 없이 기억만으로 쓰면 **틀릴 수 있지만([[275_react_framework|환각]])**, 책을 보면 정확해요.
3. AI도 **검색해서 [[396_validation|확인]]**하고 답하면 더 정확해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 144 / 420

← **이전**: [[143_prompt_engineering|143. 프롬프트 엔지니어링 (Prompt Engineering) - LLM 활용의 핵심]]
**다음**: [[145_concept|145. RLHF (Reinforcement Learning from Human Feedback) - 인간 정렬]] →

---
