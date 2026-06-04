+++
title = "536. 에이전틱 AI 워크플로우 (Agentic AI Workflows)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 에이전틱 AI는 단일 응답을 넘어, 목표를 달성하기 위해 스스로 계획을 세우고 도구를 사용하며 반복(Iteration)하는 자율적 실행 체계이다.
> 2. **가치**: 'Zero-shot' 방식의 한계를 극복하기 위해 반추(Reflection), 도구 사용(Tool Use), 계획 수립(Planning), 멀티 에이전트 협업의 4가지 핵심 패턴을 활용한다.
> 3. **판단 포인트**: 사용자의 개입 없이 복잡한 문제를 해결하는 '자율적 루프'를 통해 AI의 역할이 보조자에서 대리인(Agent)으로 진화하고 있다.

---

## Ⅰ. 개요 및 필요성

지금까지의 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 활용은 사용자가 질문하면 AI가 답하는 일회성 인터랙션이 주를 이루었다. 하지만 복잡한 비즈니스 프로세스나 소프트웨어 개발 등은 단 한 번의 프롬프트로 해결하기 어렵다. 에이전틱 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 워크플로우는 AI에게 "이 코드를 작성해"라고 시키는 대신, "이 기능을 구현하기 위해 설계를 하고, 코드를 짜고, 테스트를 해본 뒤 오류가 나면 스스로 수정해"라고 명령하는 방식이다. 이는 '시스템 2 사고(느리고 논리적인 추론)'를 AI에게 이식하는 과정이라 할 수 있다.

- **📢 섹션 요약 비유**: 새 기술도 왜 등장했는지 배경을 잡아야 언제 써야 할지 판단이 선다.

---

## Ⅱ. 아키텍처 및 핵심 원리

에이전틱 워크플로우는 순환적 루프(ReAct: Reasoning + Acting) 구조를 기반으로 한다.

```text
[ Agentic AI Workflow Cycle ]

      +---------------------------+
      |  User Goal / Objective    |
      +------------+--------------+
                   |
      +------------v--------------+
      | 1. Planning (Task Deco)   | <-------+
      +------------+--------------+         |
                   |                        |
      +------------v--------------+         |
      | 2. Tool Use / Execution   |         | 4. Iteration &
      | (Search, Code, API, DB)   |         |    Reflection
      +------------+--------------+         | (Self-Correction)
                   |                        |
      +------------v--------------+         |
      | 3. Observation / Analysis | --------+
      +------------+--------------+
                   | (Goal Reached)
      +------------v--------------+
      |     Final Result          |
      +---------------------------+
```

1. **Reflection**: 자신이 생성한 결과물을 스스로 비판하고 개선안을 도출한다. (Self-Correction)
2. **Tool Use**: 외부 지식 검색, 계산기, 코드 실행기 등을 직접 호출하여 부족한 능력을 보완한다.
3. **Planning**: 거대한 목표를 하위 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)(Sub-tasks)로 분해하고 순차적으로 실행한다.
4. **Multi-agent Collaboration**: 코딩 전문가, 디자인 전문가, 기획 전문가 등 서로 다른 역할을 가진 에이전트들이 소통하며 문제를 해결한다.

- **📢 섹션 요약 비유**: 설계도와 배관도를 함께 보는 것처럼 내부 연결을 알아야 병목과 핵심 원리를 이해할 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 전통적 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) (Prompt-based) | 에이전틱 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) (Workflow-based) |
| :--- | :--- | :--- |
| **작동 방식** | 입력 -> 출력 ([단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)) | 계획 -> 실행 -> 반추 (루프) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 결정</strong> | 모델의 파라미터 규모 | 워크플로우 설계 및 반복 횟수 |
| **추론 비용** | 낮음 (1회 실행) | 높음 (다회 실행 및 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) |
| **정확도** | 중간 ([할루시네이션](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/251_hallucination_rag_augmented_retrieval_vector_db/) 취약) | 높음 (스스로 오류 수정) |
| **적합 사례** | 번역, 요약, 단순 질의 | 소프트웨어 개발, 리서치, 마케팅 자동화 |

- **📢 섹션 요약 비유**: 비슷한 공구도 쓰임새가 다르듯, 비교를 해야 이 개념의 경계와 강점이 또렷해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사로서의 판단으로는, 에이전틱 AI는 <strong>'모델의 한계를 아키텍처로 극복'</strong>하는 기술이다.
1. **거버넌스**: AI가 자율적으로 도구를 사용하고 결제나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제 등의 액션을 취할 때를 대비해 **Human-in-the-loop (중간 승인)** 설계가 필수적이다.
2. **안정성**: 무한 루프(Infinite Loop)에 빠져 비용이 폭증하는 것을 방지하기 위해 최대 반복 횟수(Max Iterations)와 비용 한도를 설정해야 한다.
3. **평가**: 정적인 벤치마크보다는 실제 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 성공률([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) Success Rate)을 지표로 관리해야 한다.

- **📢 섹션 요약 비유**: 현장 체크리스트처럼 조건을 짚어야 기술이 장점이 아니라 실제 성과로 이어진다.

---

## Ⅴ. 기대효과 및 결론

에이전틱 AI는 기업의 업무 방식 자체를 완전히 바꿀 것이다. 단순히 답변을 주는 수준을 넘어, 스스로 업무를 완결 짓는 '[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사원'의 등장을 의미한다. 향후에는 에이전트 간의 소통 표준 프로토콜이 정립될 것이며, 이는 서로 다른 회사의 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 에이전트들이 협력하여 복잡한 비즈니스 거래를 수행하는 <strong>Agentic Economy</strong>의 토대가 될 것이다.

- **📢 섹션 요약 비유**: 결산표를 보듯 효과와 한계를 함께 정리해야 다음 확장 방향이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 부모 개념 | Autonomous Agents, [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) |
| 연관 개념 | ReAct, [AutoGPT](/knowledge-base/studynote/10_ai/03_llm_nlp/216_autogpt_autonomous_agent/), BabyAGI, Multi-agent Systems, Tool Use |
| 파생 기술 | LangGraph, CrewAI, Autogen, Semantic [Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Autonomous Agents · LLM] -> [에이전틱 AI 워크플로우] -> [LangGraph · CrewAI]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 전통적 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/): 요리책을 보고 레시피만 읽어주는 친구예요.
2. 에이전틱 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/): 직접 시장에 가서 재료를 사고, 요리하고, 맛을 본 뒤 싱거우면 소금을 더 넣어 완벽한 요리를 만드는 셰프예요.
3. 차이점: 말만 하는 게 아니라, 목표를 이룰 때까지 스스로 생각하고 행동해서 결과를 만들어내는 똑똑한 대리인이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 536 / 552

<- **이전**: [535. 전문가 혼합 모델 (Mixture of Experts, MoE)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/535_moe_mixture_of_experts/)
**다음**: [537. 시맨틱 캐시 RAG 비용·지연 절감 (Semantic Cache RAG Cost and Latency Reduction)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/537_semantic_cache_rag_cost_reduction/) ->

---
