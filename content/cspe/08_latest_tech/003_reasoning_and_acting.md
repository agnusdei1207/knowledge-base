---
title: "ReAct 패턴 (Reasoning and Acting)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-latest-tech"
weight: 3
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: **ReAct**는 LLM이 과업을 수행할 때 **추론(Reasoning)**과 **행동(Acting)**을 교차하며 수행하도록 하는 프롬프팅 및 아키텍처 패턴이다.
- **필요성**: 추론만 하면(Reason-only, CoT) 외부 지식 없이 내부 지식에만 의존해 환각이 발생하기 쉽고, 행동만 하면(Act-only) 논리적 일관성 없이 무작위로 도구를 호출하게 된다. ReAct는 이 둘을 결합해 **논리적이고 근거 있는 행동**을 유도한다.
- **핵심 직관**: **"생각하고(Thought), 행동하고(Action), 관찰하라(Observation)"**. 이 과정을 반복하며 목표에 도달한다.

## 깊이 이해
- **배경 (Synergizing Reasoning and Acting)**: ICLR 2023에서 발표된 논문으로, 인간이 새로운 문제를 해결할 때 "무엇을 해야 할지 생각"하고 "실제로 실행"하며 "결과를 보고 다음을 판단"하는 인지 과정을 모방했다.
- **작동 원리 (The Loop)**:
    1. **Thought**: 현재 상황에 대한 추론. "질문에 답하기 위해 검색이 필요해."
    2. **Action**: 외부 도구 호출. `Search(Apple Inc. CEO)`
    3. **Observation**: 도구의 결과 확인. "Tim Cook is the CEO of Apple."
    4. **Thought**: 다음 추론. "팀 쿡의 나이를 알아야 하니 다시 검색하자."
    5. **(반복)** ... 최종 답안 도출.
- **비유**: 미로를 탈출할 때 눈을 감고 생각만 하거나(CoT), 생각 없이 벽에 부딪히며 달리는 것(Act-only)이 아니라, 지도를 보며 방향을 잡고(Thought) 한 발짝 움직인 뒤(Action) 주변을 확인(Observation)하는 과정과 같다.
- **구체 예시**: `LangChain`의 Zero-shot React Agent가 가장 대표적인 구현체다.
- **주의점**: 루프가 너무 길어지면 토큰 비용이 상승하고, 중간에 잘못된 관찰(Observation)이 들어오면 전체 추론이 꼬일 수 있다.

## 연결 개념
- **AI 에이전트 시스템 (001)**: ReAct는 에이전트 시스템의 가장 기초적인 작동 알고리즘이다.
- **CoT (Chain of Thought) (045)**: ReAct의 'Reasoning' 부분을 담당하는 기초 기술.
- **Self-Reflect / Reflexion (049)**: ReAct를 넘어 자신의 행동 자체를 평가하고 수정하는 상위 개념.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LLM의 내적 추론(Reasoning)과 외적 행동(Acting)을 유기적으로 결합한 인터리빙(Interleaving) 프롬프팅 기법.
> 2. **가치**: CoT의 환각 문제와 Act-only의 논리 부재 문제를 동시에 해결하여 자율적 문제 해결 능력 극대화.
> 3. **판단 포인트**: 정밀한 관찰(Observation)을 위한 고품질 도구(Tool) 명세와 파싱 로직 설계가 성능의 핵심.

## 출제 의도 및 답안 포인트
- **출제 의도**: 에이전트의 사고 루프인 ReAct의 메커니즘과 그 기술적 우수성(CoT 대비 차별점) 이해 여부.
- **핵심 포인트**: Thought-Action-Observation 3단계 루프, Synergizing, 환각 억제.

---

## Ⅰ. ReAct(Reasoning + Acting)의 개념 및 등장 배경
### 1. ReAct의 정의
- LLM이 목표 달성을 위해 언어 기반의 추론(Thought)과 특정 도구 호출(Action)을 번갈아 수행하며 외부 환경의 피드백(Observation)을 수용하는 인지 프레임워크.
### 2. 등장 배경: 기존 기법의 한계
- **Reason-only (CoT)**: 논리적이나 외부 실시간 정보 접근 불가, 지식의 한계로 인한 환각(Hallucination) 발생.
- **Act-only (WebGPT 등)**: 외부 도구는 쓰지만 왜 그 행동을 하는지 논리가 없어 복잡한 추론 작업에서 실패 가능성 높음.

---

## Ⅱ. ReAct의 작동 아키텍처: 3-Step Loop
- **추론과 행동의 상호작용 프로세스**
```text
[ Question ] 
     ↓
┌───────────┐      ┌───────────┐      ┌──────────────┐
│  Thought  │ ───> │  Action   │ ───> │ Observation  │
│ (추론/계획) │ <─── │ (도구호출) │ <─── │ (결과/피드백)  │
└───────────┘      └───────────┘      └──────────────┘
     ↓ (반복)
[ Final Answer ]
```

| 단계 | 수행 내용 | 핵심 역할 |
|:---:|:---|:---|
| **Thought** | 상황 인식 및 다음 단계 논리 전개 | 실행 계획 수립, 자가 진단, 논리 유지 |
| **Action** | 특정 도구 선택 및 파라미터 생성 | 외부 세계와의 상호작용 (Search, Calc, DB) |
| **Observation** | 실행 결과 데이터 수신 및 문맥 추가 | 추론의 근거(Grounding) 확보, 상태 업데이트 |

---

## Ⅲ. ReAct 패턴의 기술적 장점 및 차별화 요소

| 비교 항목 | Chain of Thought (CoT) | ReAct (Reasoning + Acting) |
|:---:|:---|:---|
| **지식 출처** | 모델 내부 파라미터 (Static) | 외부 도구 및 실시간 데이터 (Dynamic) |
| **신뢰성** | 환각 가능성 존재 | 외부 근거 기반 답변 (Grounding) |
| **상호작용** | 단방향 (Generation) | 양방향 (Act & Feedback) |
| **적용 범위** | 수학, 논리 퀴즈 | 정보 검색, API 연동, 자율 업무 수행 |

---

## Ⅳ. ReAct 구현 시 주요 기술적 고려사항
- **Prompt Engineering**: LLM이 `Thought:`, `Action:`, `Observation:` 형식을 엄격히 지키도록 유도하는 Few-shot 예시 설계.
- **Stop Sequences**: 모델이 `Observation:`을 직접 생성하지 않고 외부 시스템의 입력을 기다리도록 생성 중단(Stop) 설정.
- **Tool Description**: LLM이 각 도구의 용도와 입력 규격(JSON Schema 등)을 정확히 이해할 수 있도록 상세 명세 제공.

---

## Ⅴ. ReAct의 확장 및 한계 극복 (ReAct 2.0 이상)
- **Self-Correction**: 관찰 결과가 비논리적일 경우 스스로 계획을 수정하는 Reflection 메커니즘 통합.
- **Memory Management**: 루프가 길어질수록 컨텍스트 윈도우가 가득 차는 문제 해결을 위해 중요 정보 요약(Summary) 및 보존.
- **Fine-tuning**: ReAct 데이터셋을 통한 모델 미세조정으로 프롬프트 의존성 감소.

---

## Ⅵ. 실무 관점의 결론 및 제언
- **기술사 판단**: ReAct는 에이전트의 '두뇌'와 '손발'을 잇는 가장 표준적인 알고리즘임.
- **결론**: 단순히 성능 좋은 LLM을 쓰는 것을 넘어, 정교한 ReAct 루프를 설계하고 이를 뒷받침할 **도구 생태계(Tool Ecosystem)**를 구축하는 것이 차세대 AI 시스템의 핵심 경쟁력임.

### 🔀 문제 유형별 목차 전환
- **비교형**: Ⅲ. CoT vs ReAct 비교표를 중심으로 한 논리 전개.
- **설계형**: Ⅱ. 작동 아키텍처 -> Ⅳ. 구현 시 고려사항(Stop Sequence, Schema) 강조.
