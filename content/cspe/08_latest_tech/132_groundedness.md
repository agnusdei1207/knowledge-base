---
title: "근거성 (Groundedness)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 132
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: AI가 생성한 답변이 "주어진 근거 데이터(Context, 문서, 출처)에 두 발을 단단히 딛고(Grounded) 있는가?"를 뜻하는 포괄적인 품질 속성이자 평가 지표. (환각이 없음을 증명하는 가장 확실한 척도).
- **필요성**: 기업 환경에서 AI 챗봇이 사내 규정이나 고객 약관을 안내할 때, 그럴듯한 거짓말(환각)을 하면 치명적인 법적/금전적 사고로 이어짐. 무조건 "출처에 있는 말만 해야 한다"는 절대 명제가 필요함.
- **핵심 직관**: 팩트체크. 뉴스 기자가 기사를 쓸 때, "관계자 A씨의 녹취록(Context)"에 있는 내용만 썼으면 Grounded된 것이고, 자기 뇌피셜로 소설을 보탰으면 Grounded되지 않은 것.

## 깊이 이해
- **배경**: LLM은 수많은 인터넷 글을 학습했기 때문에, 물어보는 즉시 자기가 아는 일반 상식을 지어내려는 본능(Parametric Knowledge Leak)이 있음. 이를 외부 문서에만 묶어두려는 노력(RAG)이 등장했고, 그 묶어둠의 강도를 나타내는 용어로 정착됨.
- **작동 원리 (Faithfulness와의 관계)**:
  - 학계/업계에서 `Groundedness`와 `Faithfulness(충실성)`는 종종 동의어로 쓰임. (프레임워크 TruLens는 Groundedness를, Ragas는 Faithfulness를 씀).
  - 작동 방식은 동일함: 1) 답변을 문장 단위로 쪼갬. 2) 각 문장이 참고 문서(Context)에 의해 뒷받침(Supported)되는지 NLI(자연어 추론)나 LLM 심사관이 판정함.
- **구체 예시**: 
  - (Context): "회식비는 인당 3만 원 제한이다."
  - (AI 답변): "회식비는 인당 3만 원이며, 부서장 승인 시 5만 원까지 가능합니다." $\rightarrow$ 부서장 얘기는 Context에 없음. Groundedness 실패!
- **흔한 오해/주의점**: 답변이 '사실(Fact)'이라고 해서 Groundedness가 높은 게 아님! "한국의 수도는 서울이다"라는 사실을 답했어도, RAG가 검색해 온 문서에 그 말이 안 적혀 있으면 Groundedness는 0점임. 철저하게 **"주어진 텍스트에 기반했는가"**만 따짐.

## 연결 개념
- **Faithfulness (충실성)**: Groundedness와 사실상 같은 뜻으로 통용되는 평가 메트릭 용어.
- **AI Hallucination (환각)**: Groundedness가 낮다는 것은 100% 환각(Hallucination)이 발생했다는 뜻. 반대말.
- **Citation-based Answering (출처 기반 답변)**: Groundedness를 시각적으로 증명하기 위해 답변 뒤에 "[1], [2]" 형태로 각주를 다는 기법.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 생성 모델(LLM)이 뱉어낸 모든 발화(Utterance)와 주장이, 시스템이 명시적으로 제공한 외부 지식(Retrieval Context)에 뿌리를 두고(Grounded) 연역적으로 도출되었는지를 평가하는 신뢰성 척도.
- **가치**: LLM의 내재적 파라미터 메모리(Parametric Memory)에 의한 사전 학습 지식 개입과 환각(Hallucination)을 원천 차단하여, 기업형 AI의 규제 준수(Compliance) 및 법적 리스크 방어를 가능케 함.
- **판단 포인트**: 이 지표가 낮게 나오는 것은 철저히 언어 모델(Generation)의 통제력 부족이 원인이므로, System Prompt 강제화, Temperature 조절, 그리고 후처리(Post-processing) 검증 및 답변 거절(Refusal) 정책 적용이 필수적임.

## Ⅰ. 개요 및 필요성
- **정의**: 시스템 응답의 정보 구성 요소들이 사용자가 주입했거나 검색 파이프라인이 확보한 원본 데이터(Source Data)에 의해 논리적으로 지지(Supported/Entailed)되는 정도를 나타내는 품질 특성.
- **배경**: 거대 언어 모델은 정보가 부족한 상황에서도 언어적 유창성(Fluency)을 유지하려는 성향 때문에 그럴듯한 거짓 정보를 생성(Confabulation)하는 구조적 결함을 가짐.
- **필요성**: 금융(약관 안내), 의료(처방 가이드), 법률(판례 요약) 등 "사실적 무결성"이 생명인 도메인에서 모델의 답변이 사실로 채택될 수 있는지 결정짓는 최우선(Primary) SLA 지표임.

## Ⅱ. Groundedness 평가 파이프라인 (NLI 및 LLM-as-a-Judge)
전체 답변을 원자 단위 명제로 분해한 후, 각 명제가 Context 집합 내에 포함되는지 교차 검증함.
1. **명제 분할 (Statement Extraction)**:
   - "이순신은 1545년에 태어났고 거북선을 만들었다." $\rightarrow$ [이순신은 1545년에 태어났다], [거북선을 만들었다].
2. **NLI (자연어 추론) 연산**:
   - 추출된 명제(Hypothesis)와 Context(Premise) 간의 논리적 관계를 `Entailment(함의/지지)`, `Neutral(중립/알수없음)`, `Contradiction(모순/반대)` 세 가지로 확률 분류.
3. **점수 정량화 (Scoring)**:
   - 전체 명제 중 `Entailment`로 판정된 명제의 비율을 $0 \sim 1$ (또는 $0 \sim 10$점) 단위로 산출.

## Ⅲ. 환각 발생 원인에 따른 Groundedness 방어 전략
Groundedness 실패(환각)는 크게 두 가지 원인에서 비롯됨.
| 환각의 유형 | 원인 분석 | MLOps 차원의 대응/방어 전략 |
|:---:|:---|:---|
| **Closed-domain Hallucination** (폐쇄 도메인 환각) | 검색 문서 안의 팩트(숫자, 이름)를 자기 마음대로 조작하거나 섞어버림. | 1. 프롬프트에 `[출처에 없는 말은 절대 하지 마라]` 지시<br>2. Temperature = 0 (창의성 극단적 억제) 설정 |
| **Open-domain Hallucination** (오픈 도메인 환각) | 검색 문서에 답이 아예 없는데, 자기가 아는 얕은 지식으로 아무 말 대잔치를 함. | 1. 프롬프트에 `[모르면 모른다고 답하라]` 방어 기제 삽입<br>2. 검색 결과가 부실할 시 아예 생성을 차단하는 룰 엔진 결합 |

## Ⅳ. 고도화: 생성물 통제 아키텍처 (Guardrails 도입)
실시간 서비스 환경에서 Groundedness를 담보하기 위한 시스템 아키텍처 설계.
- **Self-Correction (자가 수정 루프)**:
  LLM이 답변을 생성(Draft)하면, 별도의 판독 모델(Critic)이 실시간으로 Groundedness를 측정함. 임계치(예: 0.9) 미달 시, 틀린 문장을 지목하여 LLM 스스로 다시 쓰도록(Re-generate) 강제하는 Agentic Workflow 구성.
- **NeMo Guardrails (NVIDIA)**:
  사용자 응답 직전에 프록시(Proxy) 계층을 두어, 답변이 사전에 정의된 안전 정책(Fact-checking 룰)을 벗어날 경우 답변 출력을 강제 차단(Block)하고 "답변할 수 없습니다"라는 기본(Fallback) 메시지를 띄움.

## Ⅴ. 실무 적용 및 결론
- **판단 지표**: Groundedness Score (TruLens 기준 0.9 이상), 사용자 리포트(환각 신고) 건수.
- **실무 설계**: 금융사 대출 심사 어시스턴트(RAG) 구축 시. 심사역이 "A기업의 재무 위험도는?" 질문 시, RAG가 재무제표 문서를 검색하여 "유동비율 150%로 양호함"이라 답함. 그러나 실제 문서엔 유동비율이 "105%"로 기재되어 있었음(LLM의 숫자 환각). 이로 인해 Groundedness 0점 발생. 해결책으로 생성 파이프라인 마지막에 **Citation 강제화(인용구 의무화)** 프롬프트와 **NeMo Guardrails**의 Fact-check 기능을 추가함. 숫자나 고유명사는 철저히 토큰 매칭으로 검증하고, 불일치 시 답변을 가리는 로직을 적용하여 심사 사고 위험을 원천 차단함.
- **결론**: Groundedness는 AI가 "생각하는 기계"에서 "신뢰할 수 있는 정보 중개자"로 거듭나기 위한 최소한의 자격 요건이며, 기업이 LLM을 사내에 도입할 때 가장 먼저, 그리고 가장 엄격하게 세워야 할 첫 번째 통제선이다.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Groundedness 측정을 위한 NLI(Natural Language Inference) 기반의 크로스 인코더 모델 추론 원리, Faithfulness 지표와의 개념적 동일성 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: LLM의 Temperature 파라미터와 Top-P 파라미터가 Groundedness에 미치는 영향 분석, Guardrails 프레임워크를 활용한 실시간 차단(Fallback) 아키텍처.
