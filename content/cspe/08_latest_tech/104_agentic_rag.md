---
title: "에이전틱 RAG (Agentic RAG)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 104
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **에이전틱 RAG** | 에이전틱 RAG (Agentic RAG)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 사람이 정해놓은 고정된 파이프라인(순서)대로만 움직이는 기존 RAG와 달리, AI 에이전트(LLM)가 스스로 계획을 세우고, 다양한 도구(검색, DB, 계산기 등)를 여러 번 반복 호출하며 정답을 추론해 나가는 동적 RAG 프레임워크.
- **필요성**: 기존 RAG는 한 번 검색해서 답이 없거나 정보가 부족하면 포기함. 여러 문서를 교차 검증하거나, 검색 결과에 따라 후속 질문이 달라져야 하는 복합 추론(Complex Query)에는 속수무책임.
- **핵심 직관**: "A회사와 B회사의 3분기 이익률 차이를 구해줘."라고 할 때, 한 번에 검색하는 게 아니라 $\rightarrow$ 1. A회사 매출 검색 2. B회사 매출 검색 3. 계산기 도구로 차이 계산 4. 최종 리포트 작성 등, 스스로 단계를 쪼개서 심부름을 수행하는 똑똑한 비서.

## 깊이 이해
- **배경**: LLM의 추론 능력(Reasoning)이 강화되고, Function Calling(함수 호출) 기능이 안정화되면서, 단순 검색 보조 시스템(RAG)이 자율적 문제 해결사(Agent)로 진화함.
- **작동 원리 (Plan -> Tool Use -> Observe -> Reflect)**:
  1. 사용자가 복잡한 질문을 던지면, 에이전트 내부의 플래너(Planner)가 이를 쪼개어 단계별 계획을 수립함.
  2. 라우터(Router)가 어떤 도구를 쓸지 결정 (벡터 검색할까? SQL로 엑셀을 조회할까? 구글링을 할까?).
  3. 도구를 실행한 결과(Observation)를 보고, 메모리(Memory)에 저장한 뒤, 더 찾아야 할 정보가 있는지 스스로 평가(Reflection).
  4. 충분한 정보가 모일 때까지 루프를 돌다가 최종 답변 생성.
- **구체 예시**: 고객 질의 "내 작년 세금 내역이랑 최신 세법 비교해서 환급금 계산해 줘." $\rightarrow$ (기존 RAG): "저는 사용자의 개인정보나 계산을 할 수 없습니다." $\rightarrow$ (Agentic RAG): 1) 내부 DB API 호출해 내역 조회 $\rightarrow$ 2) 벡터 DB로 최신 세법 RAG 검색 $\rightarrow$ 3) 파이썬 코드 인터프리터 도구로 계산 $\rightarrow$ 결과 응답.
- **흔한 오해/주의점**: 똑똑한 만큼 위험함. 자율성이 높아서 무한 루프(계속 엉뚱한 검색만 반복함)에 빠지면 토큰(비용)이 폭발함. 반복 횟수(Max Steps) 제한과 쓸 수 있는 도구에 대한 엄격한 권한 제어(Guardrails)가 필수적임.

## 연결 개념
- **Function Calling (함수 호출)**: LLM이 외부 도구(API, 검색기 등)를 선택하고 실행 인자(Arguments)를 구조화해서 내뱉는 핵심 기술.
- **ReAct (Reasoning and Acting)**: 에이전트가 생각하고 행동하고 관찰하는 과정을 명시적으로 프롬프팅하는 기법.
- **Advanced RAG**: 정해진 파이프라인(Static)을 최대한 고도화한 것. Agentic RAG는 파이프라인 자체를 LLM이 동적(Dynamic)으로 짜는 것.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 하드코딩된 단방향 정보 탐색 파이프라인(Static DAG)을 넘어서, LLM 자체가 제어부(Brain)가 되어 Tool Calling과 다단계 추론(Multi-hop Reasoning) 루프를 주도하는 자율형 프레임워크.
- **가치**: 이종 데이터 소스(Vector DB, RDBMS, Web API 등)를 횡단하여 결합해야 하거나, 검색 중간 결과에 따라 후속 탐색 경로가 변경되는 복합 질의(Complex Multi-step Query) 해결 능력을 제공.
- **판단 포인트**: 자유도 증가에 따른 시스템 응답 지연(Latency) 증가 통제, 무한 루프 방지를 위한 Max-iterations 제약, 에이전트가 호출할 수 있는 도구의 권한 관리(Tool ACL).

## Ⅰ. 개요 및 필요성
- **정의**: 대형 언어 모델(LLM)을 의사결정의 주체(Agent)로 활용하여, 사용자 질의를 분석/분해하고 최적의 검색 도구와 외부 API를 동적(Dynamic)으로 선택·반복 호출하여 최종 해답을 합성하는 RAG 아키텍처.
- **배경**: 기존 Advanced RAG는 여전히 "1회 검색 $\rightarrow$ 1회 생성"이라는 단방향 구조에 묶여 있어, 여러 문서를 대조하거나(비교 분석), 요약과 계산이 결합된 다단계 태스크 수행이 불가능함.
- **필요성**: 기업 내 ERP(정형 데이터), 사내 위키(비정형 데이터), 외부 웹 크롤링 등 다기종 데이터 소스를 지능적으로 라우팅(Routing)하고 조합하는 궁극의 엔터프라이즈 AI 비서 구축을 위해 필수적임.

## Ⅱ. Agentic RAG 아키텍처 (4대 핵심 컴포넌트)
| 컴포넌트 | 핵심 역할 | 적용 기술 및 특징 |
|:---:|:---|:---|
| **Planner (Brain)** | 사용자 질의 분해 및 실행 경로(DAG) 동적 수립 | Plan-and-Solve 프롬프팅, ReAct 프레임워크 |
| **Tool Router** | 다수의 Tool 중 현재 단계에 최적화된 도구 선택 | Function Calling 기반 파라미터 구조화 (JSON) |
| **Tools (도구)** | 실제 데이터 소스 접근 및 연산 수행 장치 | Vector Search (비정형), Text-to-SQL (정형 DB), Python Interpreter, Web Search |
| **Memory & Reflection**| 이전 검색 결과를 저장하고 추론이 완료되었는지 자가 검증 | Short-term Memory 유지, Self-Correction 루프 |

## Ⅲ. 동작 메커니즘 흐름도
```text
[ User Query (복합 질의) ]
        |
        v
+------------------ Agent Core (LLM) ------------------+
| 1. Plan: "A 정보와 B 정보가 필요. 검색 후 계산하자"  |
| 2. Act: [Tool 1: Vector RAG] 호출하여 A 검색         |
| 3. Observe: A 정보 획득 및 메모리 저장               |
| 4. Reflect: "다음엔 B를 찾아야 함"                   |
| 5. Act: [Tool 2: Text-to-SQL] 호출하여 B 검색        |
| 6. Observe: B 정보 획득                              |
| 7. Act: [Tool 3: Python] 호출하여 A, B 차이 계산     |
+------------------------------------------------------+
        | (Sufficient Info 판정 시 루프 탈출)
        v
[ Synthesize Final Answer (응답 생성) ]
```

## Ⅳ. Agentic RAG vs Advanced RAG 심화 비교
| 구분 | Advanced RAG | Agentic RAG |
|:---:|:---|:---|
| **제어 흐름 (Control Flow)**| **Static (정적)** / 파이프라인 고정 | **Dynamic (동적)** / LLM이 런타임에 결정 |
| **태스크 유형** | 단일 주제의 정보 추출 및 요약 | 다중 소스 융합, 수학적 계산, 인과관계 추론 |
| **지연 시간 (Latency)** | 낮음 ~ 중간 (예측 가능한 수준) | **매우 높음** (수차례 LLM 반복 호출 발생) |
| **오류 회복력 (Resilience)**| 중간에 한 번 실패하면 최종 답변도 실패 | 검색 결과가 이상하면 다른 키워드로 **재검색(Self-correction)** 가능 |

## Ⅴ. 한계점(운영 리스크) 및 통제 가이드라인
- **리스크 1: 과도한 비용 및 응답 지연 (Cost & Latency Blowup)**:
  - 에이전트가 정답을 찾지 못해 스스로 루프를 계속 돌면서 검색기 호출과 LLM 프롬프팅을 반복하여 토큰 비용이 폭발함.
  - **대응 방안**: 시스템 차원에서 `max_iterations(최대 반복 횟수)`를 설정(예: 5회)하고, Time-out 강제 종료 로직 구현. 또한, 모든 질의에 Agent를 쓰지 말고, 질문을 분류하는 Router를 두어 단순 질문은 빠르고 싼 Naive RAG 태워버리는 Fallback 설계.
- **리스크 2: 환각적 도구 호출 (Tool Hallucination)**:
  - 존재하지 않는 도구를 호출하려 하거나, SQL 도구에 파이썬 코드를 주입하는 등 파라미터를 잘못 생성함.
  - **대응 방안**: 도구 명세(Description)를 극도로 정교하게 작성(Prompt Engineering)하고, 타입 검증(Type Hint) 실패 시 에러 메시지를 LLM에 돌려주어 스스로 수정하게 하는 피드백 루프 구축.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: 복합 질의 해결률(Complex Query Resolution Rate), 평균 스텝 수(Average Steps/Turn), 도구 호출 성공률.
- **실무 설계**: 기업 재무 데이터 분석 AI. "작년 3분기 실적 보고서 내용(비정형 문서)을 요약하고, 올해 ERP의 매출 DB(정형 데이터)와 비교하여 YoY 성장률 그래프를 그려줘."와 같은 요청에 대응함. LangGraph를 프레임워크로 채택하고, 노드(Node) 기반 상태(State) 관리를 통해 Vector Retriever, DB SQL 엔진, Python 실행기를 도구(Tools)로 부여하여 자율적으로 임무를 완수하는 파이프라인 구축.
- **결론**: Agentic RAG는 단순한 텍스트 검색을 넘어선 진정한 의미의 'AI 비서(Actionable AI)'로 가는 핵심 아키텍처이며, 이질적 데이터 사일로(Data Silo)를 지능적으로 꿰매어내는 엔터프라이즈 하이퍼오토메이션의 중추가 될 것임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: ReAct(Reasoning and Acting) 프레임워크의 동작 원리, Function Calling 인터페이스 명세(JSON Schema) 기술, 다단계 루프 구조 중심 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: 무한 루프(Infinite Loop) 방지 등 아키텍처 안전장치(Guardrails) 설계, 시스템 응답 지연(TTFT) 한계 타개를 위한 스트리밍/라우터 기반 비용 통제 전략 작성.
