+++
weight = 147
title = "147. ToT (Tree-of-Thought) - 분기 사고 구조 탐색망 추론 기법"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ToT(Tree-of-Thought, 사고 트리)는 [[263_llm_large_language_model|LLM]]([[263_llm_large_language_model|Large Language Model]], [[582_llm_based_code_generation_tools|대규모 언어 모델]])이 문제를 해결할 때 단선(Chain)이 아닌 **트리 구조로 여러 사고 경로를 분기·탐색·[[010_backtracking|백트래킹]]([[010_backtracking|Backtracking]])하며 최적 답을 찾는 추론 프레임워크**다.
> 2. **가치**: [[146_chain_of_thought_cot|CoT]]([[146_chain_of_thought_cot|Chain-of-Thought]], 생각의 연쇄)가 직선으로 한 번만 추론하는 것과 달리, ToT는 **여러 가능성을 동시에 탐색하고 막힌 경로를 포기([[435_pruning_hardware|Pruning]])하며 더 나은 경로를 선택**함으로써 복잡한 다단계 추론 과제에서 정확도를 획기적으로 높인다.
> 3. **판단 포인트**: ToT는 탐색 비용(토큰·[[014_api_posix|API]] 호출)이 CoT보다 수배~수십 배 높으므로, **복잡한 퍼즐·수학 증명·[[268_strategy_pattern|전략]]적 계획 수립** 등 오답 비용이 높은 과제에만 선택적으로 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

LLM의 추론 능력 향상은 [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]의 핵심 연구 주제다. 표준 프롬프트 방식은 LLM이 질문에 바로 답하지만, 복잡한 문제에서 오류가 많다. [[146_chain_of_thought_cot|CoT]]([[146_chain_of_thought_cot|Chain-of-Thought]])는 "단계별로 생각하세요"라고 유도해 중간 추론 과정을 출력하게 함으로써 정확도를 높였다.

그러나 CoT도 한계가 있다: **단 하나의 추론 경로만 탐색**한다. [[459_quic_fec_forward_error_correction|초기]]에 잘못된 방향을 잡으면 끝까지 오답을 향해 달려간다. ToT는 이 한계를 극복하기 위해 2023년 Princeton·Google DeepMind 연구진이 제안한 방법으로, LLM의 추론을 **트리 탐색 [[001_algorithm_definition|알고리즘]]([[035_bfs|BFS]]/[[034_dfs|DFS]])** 으로 구조화한다.

**ToT가 필요한 상황**:
- 수학 증명, 로직 퍼즐 (24-point 게임 등) — 다양한 시도 후 [[010_backtracking|백트래킹]] 필수
- 코드 디버깅 — 여러 가설 동시 테스트 후 실패 경로 폐기
- [[268_strategy_pattern|전략]]적 계획 (여행 일정 최적화) — 분기별 시나리오 탐색

- **📢 섹션 요약 비유**: CoT가 **'모르는 길을 한 방향으로만 걷는 것'** 이라면, ToT는 **'지도 없는 미로에서 갈림길마다 여러 [[315_exploration_exploitation|탐험]]대를 보내고 막힌 길에서 되돌아와 더 나은 길을 찾는 것'** 입니다. 한 [[315_exploration_exploitation|탐험]]대가 실패해도, 다른 [[315_exploration_exploitation|탐험]]대가 올바른 출구를 찾아냅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ToT 구조도

```text
ToT (Tree-of-Thought) 추론 구조

                문제 (Root)
                    │
        ┌───────────┼───────────┐
        │           │           │
    사고1-A      사고1-B      사고1-C
    (좋음↑)      (보통)       (나쁨↓ 폐기)
        │           │
    ┌───┴───┐   ┌───┴───┐
    │       │   │       │
  2-AA   2-AB  2-BA   2-BB
  (좋음↑) (폐기) (폐기) (좋음↑)
    │                   │
  최종 답 A            최종 답 B
          └──── 평가 → 더 좋은 답 선택 ────┘
```

### 2. ToT 4단계 작동 메커니즘

| 단계 | 역할 | 설명 |
|:---|:---|:---|
| **1. 생각 분해 (Thought Decomposition)** | 문제를 중간 사고 단위로 분해 | 단계별로 어떤 수준의 "사고"가 필요한지 정의 |
| **2. 생각 [[087_process_state_transition|생성]] (Thought Generation)** | 각 노드에서 k개 후보 사고 [[087_process_state_transition|생성]] | [[146_chain_of_thought_cot|CoT]] 샘플링 또는 Propose prompt 사용 |
| **3. 상태 평가 ([[272_state_pattern|State]] Evaluation)** | 각 사고의 품질을 LLM이 스스로 평가 | "이 경로가 문제 해결에 얼마나 유망한가?" |
| **4. 탐색 [[001_algorithm_definition|알고리즘]] (Search)** | [[035_bfs|BFS]]/[[034_dfs|DFS]]/빔 서치로 트리 탐색 | 유망한 경로를 확장, 나쁜 경로는 [[435_pruning_hardware|가지치기]] |

### 3. [[146_chain_of_thought_cot|CoT]] vs. ToT vs. GoT 비교

```text
사고 구조 진화

  Standard Prompt:  입력 → 출력
                    (단선, 추론 없음)

  CoT (Chain):      입력 → 생각1 → 생각2 → 생각3 → 출력
                    (순차 단선)

  ToT (Tree):       입력 → [생각1-A, 생각1-B, 생각1-C]
                              → [평가] → 유망한 경로만 확장
                              → 최적 출력
                    (분기·탐색·백트래킹)

  GoT (Graph):      임의 방향 그래프로 사고 연결
                    (순환 참조, 아이디어 병합 등 가능)
```

- **📢 섹션 요약 비유**: CoT와 ToT의 차이는 **'나침반만 들고 직진하는 [[315_exploration_exploitation|탐험]]([[146_chain_of_thought_cot|CoT]])'** 과 **'드론을 여러 대 띄워 동시에 여러 경로를 스캔한 후 최적 경로만 걷는 [[315_exploration_exploitation|탐험]](ToT)'** 의 차이입니다. ToT는 비용이 더 들지만, 복잡한 지형에서 목적지를 확실히 찾아냅니다.

---

## Ⅲ. 비교 및 연결

### 프롬프트 추론 기법 비교표

| 기법 | 탐색 구조 | 비용 | 정확도 | 적합 상황 |
|:---|:---|:---|:---|:---|
| Standard Prompt | 없음 | 최저 | 낮음 | 단순 QA |
| [[146_chain_of_thought_cot|CoT]] ([[146_chain_of_thought_cot|Chain-of-Thought]]) | 단선 | 낮음 | 중간 | 중간 복잡도 추론 |
| SC (Self-[[194_consistency_database_integrity|Consistency]]) | 다중 [[146_chain_of_thought_cot|CoT]] 샘플링 | 중간 | 중상 | 수학 문제 |
| **ToT (Tree-of-Thought)** | 트리 ([[035_bfs|BFS]]/[[034_dfs|DFS]]) | 높음 | 높음 | 복잡 퍼즐·계획 |
| GoT ([[104_graph|Graph]]-of-Thought) | [[070_graph_datastructure|그래프]] | 최고 | 최고 | 창의적 문제 해결 |

### 연결 개념 흐름

[[585_zero_skipping|Zero]]-Shot → Few-Shot → [[146_chain_of_thought_cot|CoT]] → SC (Self-[[194_consistency_database_integrity|Consistency]]) → ToT → GoT → ReAct (추론+행동) → Agentic Reasoning

- **📢 섹션 요약 비유**: 추론 기법의 진화는 **'혼자 문제 푸는 학생(Standard)'** 에서 **'단계별 필기하는 학생([[146_chain_of_thought_cot|CoT]])'**, **'여러 풀이법을 동시에 시도하는 학생(SC)'**, **'갈림길에서 두 팀을 나눠 탐색하는 팀(ToT)'** 으로 진화한 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 의사결정 [[435_checklist_based_testing|체크리스트]]

| 요구사항 | 권장 기법 | 이유 |
|:---|:---|:---|
| 단순 질문·[[104_classification_analysis|분류]] | Standard Prompt | 비용 최소화 |
| 수학 계산·[[369_logic_bomb|논리]] 추론 | [[146_chain_of_thought_cot|CoT]] 또는 SC | 단계별 [[395_verification_process_review|검증]] 필요 |
| 퍼즐·복잡 계획·다단계 문제 | **ToT** | [[010_backtracking|백트래킹]]·분기 탐색 필요 |
| 창의적 글쓰기·아이디어 도출 | GoT | 아이디어 병합·재결합 |
| 도구 사용·외부 검색 포함 | ReAct / Agentic | 행동+추론 결합 |

### ToT 구현 시 고려사항

1. **분기 수(k) 조절**: k가 클수록 정확도↑, 비용↑. 일반적으로 k=3~5
2. **평가 기준 설계**: "이 사고가 얼마나 유망한가?"를 LLM에 물어보는 평가 프롬프트가 품질 결정
3. **탐색 깊이 제한**: 무한 탐색 방지를 위한 depth limit [[009_config|설정]] 필수
4. **비용 관리**: 복잡한 ToT는 [[302_gpt_autoregressive|GPT]]-4 기준 수십~수백 회 [[014_api_posix|API]] 호출 발생

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

**단순 QA에 ToT 적용**: "서울의 수도는?"처럼 단순한 질문에 ToT를 쓰면 비용만 수십 배 늘어나고 답은 동일하다. ToT는 오답 비용이 높고, 탐색이 실제로 필요한 과제에만 적용해야 한다.

- **📢 섹션 요약 비유**: 단순 질문에 ToT를 쓰는 것은 **'편의점 위치를 찾기 위해 드론 탐색대 10팀을 파견하는 것'** 과 같습니다. 네이버 지도 한 번 검색으로 끝날 일에 100배의 비용을 쓰는 과잉 대응입니다.

---

## Ⅴ. 기대효과 및 결론

ToT는 LLM의 추론 능력을 **[[001_algorithm_definition|알고리즘]]적 탐색**과 결합함으로써, 단순한 텍스트 [[087_process_state_transition|생성]]기를 [[268_strategy_pattern|전략]]적 문제 해결자로 격상시킨다. 24-point 게임(숫자 4개로 24 만들기)에서 표준 [[302_gpt_autoregressive|GPT]]-4가 4%의 성공률을 보인 반면, ToT를 적용하면 74%까지 향상된다(원 논문 기준).

**한계**: ① [[014_api_posix|API]] 호출 비용 급증, ② 탐색 공간이 폭발적으로 증가하는 과제에서 실용적 속도 보장 어려움, ③ 평가 함수([[272_state_pattern|State]] Evaluator) 설계 품질이 전체 결과를 좌우 — 잘못 설계된 평가 기준은 오히려 오답 경로를 선택.

**미래 방향**: ① [[263_llm_large_language_model|LLM]] 자체 추론 능력 내재화(o1, o3 계열) — ToT를 모델 훈련에 내재화하는 방향, ② Agentic AI에서 도구 사용과 결합한 ToT, ③ [[158_multimodal_clip_vision_audio_encoding|멀티모달]] ToT (이미지·코드 포함 사고 트리).

ToT는 "LLM을 더 똑똑하게 만드는 것"이 아니라, **"LLM이 문제를 푸는 방식을 구조화함으로써 [[282_performance_tactics|성능]]을 이끌어내는 것"** 이라는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: ToT는 **'LLM에게 미로를 줄 때, 한 방향으로 달려가게 하는 대신 갈림길마다 멈춰 생각하고 나쁜 길은 포기하도록 훈련하는 메타 [[268_strategy_pattern|전략]]'** 입니다. [[263_llm_large_language_model|LLM]] 자체는 바뀌지 않지만, 문제를 푸는 방식이 체계화되면서 결과가 혁신적으로 달라집니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[146_chain_of_thought_cot|CoT]] ([[146_chain_of_thought_cot|Chain-of-Thought]])** | ToT의 선행 기법; 단선 추론의 한계를 트리 구조로 극복 |
| **SC (Self-[[194_consistency_database_integrity|Consistency]])** | 여러 [[146_chain_of_thought_cot|CoT]] 경로 샘플링 후 다수결; ToT와 상보 [[083_relationship_in_er_model|관계]] |
| **GoT ([[104_graph|Graph]]-of-Thought)** | ToT의 진화형; [[070_graph_datastructure|그래프]] 구조로 아이디어 병합·순환 가능 |
| **ReAct** | 추론(Reasoning)과 행동(Action)을 결합한 에이전트 기법 |
| **[[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]** | ToT를 포함하는 [[263_llm_large_language_model|LLM]] [[282_performance_tactics|성능]] 최적화 기술 체계 |

### 📈 관련 키워드 및 발전 흐름도

```text
Standard Prompting (단순 QA)
    │
    ▼
Few-Shot Prompting (예시 제공)
    │
    ▼
CoT (Chain-of-Thought) — 단선 추론
    │
    ├─► SC (Self-Consistency) — 다중 CoT 다수결
    │
    ▼
ToT (Tree-of-Thought) — 분기·탐색·백트래킹
    │
    ▼
GoT (Graph-of-Thought) — 그래프 구조 사고
    │
    ▼
Agentic Reasoning (도구 사용 + 자율 탐색)
    │
    ▼
LLM 내재화 추론 (o1, o3 계열 모델)
```

### 👶 어린이를 위한 3줄 비유 설명

1. ToT(Tree-of-Thought)는 AI가 어려운 문제를 풀 때 **한 방향만 보지 않고 여러 길을 동시에 [[315_exploration_exploitation|탐험]]**하는 방법이에요. 미로에서 갈림길마다 여러 [[315_exploration_exploitation|탐험]]대를 보내는 것처럼요!
2. [[315_exploration_exploitation|탐험]]대 중 막힌 길로 간 팀은 **바로 포기하고 돌아와서([[010_backtracking|백트래킹]])** 다른 길을 탐색해요. 그래서 틀린 방향으로 끝까지 달려가는 실수를 줄일 수 있어요.
3. 비용(토큰)이 많이 들지만, **수학 증명이나 복잡한 퍼즐처럼 정답을 꼭 맞춰야 하는 문제**에서 훨씬 정확한 답을 찾아낸답니다!
