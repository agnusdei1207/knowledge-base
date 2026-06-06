---
title: "AI Agent Tool Use Autonomous Workflow"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM(거대언어모델)을 추론 엔진(Runtime)으로 활용하여, Function Calling/Tool Use 인터페이스를 통해 외부 API·DB·실행 환경(Code Interpreter, E2B Sandbox 등)을 호출하고, ReAct·Plan-and-Execute·Reflexion 같은 추론-행동 루프를 자율적으로 반복 수행하는 에이전트 오케스트레이션 아키텍처
> 2. **가치**: 전통 RPA의 평균 60~70% 시나리오 커버리지를 LLM 에이전트로 전환 시 85~95%까지 확대 가능하며, 24/7 무인 운영으로 FTE(전환등가효율) 기준 40~60% 비용 절감, MTTR(평균복구시간) 단축을 통한 운영 SLA 개선
> 3. **판단 포인트**: ①단일 에이전트 vs 멀티에이전트(CrewAI/AutoGen/LangGraph) ②결정론적(Deterministic) vs 비결정론적(Non-deterministic) 워크플로 ③Function Calling 신뢰도(<85%시 Self-Consistency/HITL 강제) ④토큰 비용·지연시간(TTFT) 트레이드오프 ⑤MCP/A2A 같은 프로토콜 표준화 채택 여부

---

## Ⅰ. 개요 및 필요성

전통적인 업무 자동화는 사람이 정의한 조건 분기(If-Then Rule)와 정해진 입력-출력 매핑에 의존했다. RPA(Robotic Process Automation) 도구인 UiPath·Blue Prism조차 "화면 좌표 기반 매크로"에 가까워, 예외 케이스·비정형 데이터·자연어 명령에는 무력했다. 또한 일반적인 LLM 단독 호출(One-shot Prompting)은 컨텍스트 윈도우 한계, 환각(Hallucination), 최신성 부재라는 세 가지 벽에 부딪힌다.

**AI Agent Tool Use Autonomous Workflow**는 이 한계를 돌파하기 위해, LLM을 "추론기(Reasoner) + 계획기(Planner)"로 활용하고, **외부 도구(Tool)**를 LLM의 손발로 사용해 **자기-반복(Self-Iterative)**적으로 업무를 완수하는 새로운 패러다임이다. 2022년 ReAct 논문, 2023년 OpenAI Function Calling, 2024년 Anthropic MCP(Model Context Protocol), 2025년 Google A2A(Agent-to-Agent) 표준화 흐름으로 빠르게 성숙 단계에 진입했다.

```text
[기존 RPA 패러다임]                       [AI Agent 워크플로 패러다임]
+--------------+                          +------------------------------+
|  Rule Engine |  if A -> click(B.x,B.y)   |  LLM Planner (ReAct/ToT)     |
|  (정적 룰)   |  if C -> read(D[0,1])     |  + Tool Registry            |
+------+-------+                          +------+-----------------------+
       |                                          |
       v                                          v
+--------------+                          +------------------------------+
|   UI Macro   | --- ❌ 예외시 중단 ---►    |  Function Call -> API/DB/Code|
|   (좌표/OCR) |                          |  RAG / Web Search / Sandbox  |
+------+-------+                          +------+-----------------------+
       |                                          |
       v                                          v
  [사람 개입 60~70%]                          [사람 개입 5~15% (HITL)]
```

기존 워크플로가 **"사람이 미리 코딩한 분기 트리"**였다면, AI 에이전트 워크플로는 **"자연어 목표(Goal)를 받은 LLM이 그때그때 분기 트리를 즉흥 생성"**하는 차이가 있다. 이로 인해 비정형 문서(계약서, 의료 기록, 고객 클레임) 처리, 멀티스텝 리서치, 크로스 시스템 데이터 정합성 점검 같은 영역에서 질적 도약이 발생한다.

- **📢 섹션 요약 비유**: 기존 RPA는 "정해진 악보대로만 연주하는 자동 피아노"이고, AI 에이전트 워크플로는 "청중의 반응을 실시간으로 들으며 즉흥 재즈(Jazz)를 연주하는 뮤지션"이다. 코드 한 줄에 갇힌 도구에서, **프롬프트 한 줄로 무한한 도구를 조합하는 도구**로 진화한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

AI 에이전트 자율 워크플로의 핵심은 **Perception(인지) -> Planning(계획) -> Action(실행) -> Observation(관찰) -> Reflection(성찰)** 의 루프이다. 이를 **ReAct(Reasoning + Acting)** 라고 하며, 단일 호출이 아닌 다중 턴(Multi-Turn) 상호작용으로 목표를 달성한다.

```text
                        AI Agent Autonomous Workflow (상세 아키텍처)
-------------------------------------------------------------------------------

  +----------+    사용자     +------------------------------------------+
  |  User /  |--- Goal ----►|          Agent Orchestrator (Runtime)     |
  |  System  |              |  +-------------------------------------+ |
  +----------+              |  | 1. Planner (CoT/ReAct/ToT)         | |
                            |  |    - Task Decomposition            | |
                            |  |    - Dependency Graph (DAG)         | |
                            |  +-------------------------------------+ |
                            |  +-------------------------------------+ |
                            |  | 2. Memory Manager                    | |
                            |  |    - Short-term: Scratchpad/Buffer  | |
                            |  |    - Long-term: VectorStore/Episodic| |
                            |  +-------------------------------------+ |
                            |  +-------------------------------------+ |
                            |  | 3. Tool Router (Function Calling)   | |
                            |  |    - JSON Schema Validator          | |
                            |  |    - Cost/Latency Estimator         | |
                            |  +-------------------------------------+ |
                            |  +-------------------------------------+ |
                            |  | 4. Reflection / Self-Critique        | |
                            |  |    - ReAct, Reflexion, Self-RAG     | |
                            |  +-------------------------------------+ |
                            +---------+----------------------+---------+
                                      |                      |
                +---------------------+                      +----------+
                v                                                     v
   +----------------------+                              +-------------------+
   |   Tool Layer (MCP)   |                              |  Sandbox Layer    |
   | +------------------+ |                              |  +-------------+  |
   | | search_web()     | |                              |  |  E2B /      |  |
   | | query_db(sql)    | |                              |  |  Code       |  |
   | | send_email()     | |                              |  | Interpreter |  |
   | | jira_ticket()    | |                              |  |  (Firecracker|  |
   | | rag_retrieve()   | |                              |  |  microVM)   |  |
   | | file_read()      | |                              |  +-------------+  |
   | +------------------+ |                              +-------------------+
   |  MCP Servers (stdin/  |
   |  stdout JSON-RPC)    |
   +----------------------+

-------------------------------------------------------------------------------
   Loop: Thought -> Action -> Observation -> (repeat until DONE/FAIL/MAX_ITER)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Planner (계획기)** | 자연어 목표를 실행 가능한 서브태스크 DAG로 분해 | ReAct Prompt, Chain-of-Thought(CoT), Tree-of-Thoughts(ToT), Plan-and-Execute (LangGraph `PlanExecute` 노드) |
| **Memory Manager (기억 장치)** | 컨텍스트 윈도우 외부 지식·이전 단계 결과·사용자 피드백 보존 | Short-term: Scratchpad(메시지 버퍼), Long-term: Pinecone/Weaviate/Chroma 벡터 DB + Episodic(시계열 JSON Store) + Semantic(요약 임베딩) |
| **Tool Router (도구 라우터)** | LLM 출력 중 함수 호출 의도(`tool_calls`) 파싱 -> 적절한 도구 디스패치 | OpenAI `tools=[{type:"function", function:{name, parameters:JSON Schema}}]`, Anthropic `tool_use` 블록, Gemini `function_calling_config`, JSON Schema Draft-07로 인자 검증 |
| **Reflection Module (성찰기)** | 실행 결과의 정합성 검증, 실패 시 Self-Correction | Reflexion(자기비판 3회 반복), CRITIC(외부 검증자 LLM), Self-RAG(`is_rel`/`is_sup` 토큰), Constitutional AI(원칙 기반 셀프필터링) |
| **Sandbox Executor (격리 실행기)** | LLM이 생성한 코드를 안전하게 실행 | E2B(64MB microVM, gVisor 기반), Modal Labs(컨테이너), Code Interpreter API(Python 3.11 + 300+ lib), Firecracker 125ms cold start |
| **Orchestrator (오케스트레이터)** | 전체 루프 제어, 토큰 예산·재시도·타임아웃 관리 | LangGraph(StateGraph + Cyclic Edge), Temporal.io(워크플로 영속성), Prefect/Dagster(스케줄), MCP Client SDK |
| **Guardrails (안전장치)** | 입력 필터링·PII 마스킹·출력 검증 | NeMo Guardrails(Colang DSL), Guardrails AI(Pydantic 검증), Lakera Prompt Injection 방어, Azure AI Content Safety |

**Function Calling 내부 동작 메커니즘**

OpenAI/Anthropic의 Function Calling은 단순한 JSON 생성이 아니다. (1) 사용자가 `tools` 파라미터에 JSON Schema 기반 함수 정의를 함께 보내면, (2) 모델은 토큰 생성 중 `<|tool_call|>` 특수 토큰을 emit하고, (3) 인자값을 **구조화된 디코딩(Constrained Decoding)** 으로 생성(Grammar-based FSM: `guidance`, `outlines`, `lm-format-enforcer`)하여 100% 스키마 준수를 보장한다. (4) 클라이언트는 함수를 실행한 뒤 결과를 다시 `tool` role 메시지로 되먹임(Feedback)한다.

**ReAct Prompt 구조 (전형적 예시)**

```text
Question: 2024년 삼성전자 매출을 조사해서 요약해줘.
Thought 1: 사용자가 매출 정보를 원한다. 먼저 웹 검색이 필요하다.
Action 1: search_web(query="삼성전자 2024 매출", top_k=5)
Observation 1: [검색 결과 5건]
Thought 2: 충분한 데이터가 모였다. 이제 요약하자.
Action 2: llm_summarize(text=Observation_1, max_tokens=300)
Observation 2: [요약문]
Thought 3: 최종 답변이 준비되었다.
Action 3: FINISH(answer=Observation_2)
```

**Self-Consistency & Sampling 파라미터**
- `temperature`: 0.0~0.2 (정확한 함수 호출용), 0.7~1.0 (창의적 브레인스토밍용)
- `top_p`: 0.95 권장
- `seed`: 재현성 보장 시 고정
- `n` (복수 샘플): Self-Consistency Voting 시 5~7 샘플 -> 다수결
- **Function Call 정확도 벤치마크**: Gorilla BFCL(Berkeley Function-Calling Leaderboard)에서 GPT-4o ~88%, Claude 3.5 Sonnet ~92%, Gemini 1.5 Pro ~85%

- **📢 섹션 요약 비유**: Planner는 **"지휘자"**, Tool은 **"오케스트라 악기"**, Reflection은 **"자기 녹음을 듣고 고치는 음악 선생"**, Sandbox는 **"실수가 난처한 화성 폭발 실험을 위한 방호실"**이다.

---

## Ⅲ. 비교 및 연결

| 구분 | 전통 RPA (UiPath/BluePrism) | LLM Chain (단순 RAG) | AI Agent Workflow (자율형) |
| :--- | :--- | :--- | :--- |
| **결정 방식** | 사전 정의 If-Then 룰 | 단일 LLM 호출 + 검색 | LLM이 동적으로 분기·계획·재계획 |
| **도구 호출** | UI 매크로/좌표 클릭 | 없음 (Retrieval만) | Function Calling + MCP + Code Execution |
| **예외 대응** | 60~70% (사람 개입 필요) | 80% (환각 多) | 85~95% (Self-Correction) |
| **확장성** | 프로세스별 재설계 (수 주) | 프롬프트 튜닝 (수 시간) | 도구 추가만으로 확장 (수 시간) |
| **비용** | 라이선스 + 유지보수 높음 | 토큰비 낮음 (1회 호출) | 토큰비 高 (반복 호출), 절감 효과 大 |
| **감사 추적** | 완벽 (결정론적 로그) | 어려움 (블랙박스) | LangSmith/Langfuse 트레이싱, OpenTelemetry 기반 |
| **적합 영역** | 정형 백오피스 (ERP 입력) | Q&A, 요약, 분류 | 멀티스텝 리서치, 코딩, SOC/SRE 자동화 |
| **실패 시 영향** | 프로세스 중단 | 부정확한 답변 | 비용 폭주, 연쇄 오류(Cascading Error) |
| **프로토콜** | 전용 API/SDK | REST 호출 | MCP (JSON-RPC), A2A (gRPC/HTTP) |

**주요 통합 포인트**

1. **MCP (Model Context Protocol)**: Anthropic이 2024년 11월 공개한 오픈 표준. LLM 애플리케이션과 데이터 소스/도구 간 통신을 JSON-RPC 2.0 + stdio/SSE로 표준화. 기존 M×N 통합을 M+N으로 축소. OpenAI, Replit, Codeium, Zed 등이 채택 선언.
2. **A2A (Agent-to-Agent)**: Google이 2025년 4월 Linux Foundation에 기증. 에이전트 간 작업 위임·상태 공유를 JSON 기반 `Agent Card` + `Task` 객체로 정의. 멀티에이전트 시스템의 HTTP 같은 역할.
3. **LangGraph**: Cyclic Graph + Checkpointer(상태 영속화) + `interrupt_before` 노드로 **Human-in-the-Loop (HITL)** 강제 가능.
4. **RAG 보강**: Self-RAG, Corrective RAG(CRAG), Adaptive RAG를 에이전트 노드로 결합하면 "검색 -> 평가 -> 재검색" 루프가 자율화된다.
5. **Workflow 엔진 연동**: Temporal.io, Camunda 8, Apache Airflow의 DAG 노드 안에 LLM 에이전트를 임베드하여 결정론적 워크플로의 일부를 비결정론적으로 대체.

- **📢 섹션 요약 비유**: RPA가 **"낡은 팩스 기계"**, R
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 298 / 300

<- **이전**: [297. 프롬프트 엔지니어링 인컨텍스트 학습 전략 (Prompt Engineering In-Context Learning)](/studynote/14_data_engineering/05_exam_keywords/297_prompt_engineering/)
**다음**: [299. 데이터 엔지니어링 기술사 종합 아키텍처 마스터 맵 (Data Engineering PE Master Architecture Map)](/studynote/14_data_engineering/05_exam_keywords/299_data_engineering_master_map/) ->

---
