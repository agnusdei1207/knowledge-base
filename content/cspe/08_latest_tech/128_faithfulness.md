---
title: "충실성 (Faithfulness)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 128
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **충실성** | 충실성 (Faithfulness)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: RAG 시스템이 뱉어낸 최종 답변이, "오로지 검색해서 찾아온 문서(Context)의 내용에만 기반하고 있는지"를 측정하는 평가 지표. (환각 척도).
- **필요성**: LLM은 본능적으로 자신이 학습했던 사전 지식을 뽐내거나 지어내려는 성향(Hallucination)이 있음. 사내 규정을 물었는데 외부 인터넷 지식이나 거짓말을 섞어 쓰면 기업에선 대형 사고가 남. 철저한 팩트체크가 필요함.
- **핵심 직관**: 형사(LLM)가 보고서(답변)를 썼음. 서장님(채점관)이 보고서의 문장 하나하나에 빨간 줄을 치면서, "이 내용, 현장에서 가져온 증거물(Context) 박스 안에 있는 내용 맞아? 네 뇌피셜 아니야?" 하고 철저히 대조해보는 과정.

## 깊이 이해
- **배경**: RAG의 최대 목표는 환각 방지임. 아무리 훌륭한 문서를 찾아와도(높은 Retrieval 점수) LLM이 제멋대로 답하면 RAG의 존재 이유가 사라짐. 이를 수치화하기 위해 제안된 지표.
- **작동 원리 (명제 분해 및 교차 검증)**:
  1. (문장 분해): "애플은 1976년에 스티브 잡스가 창립했으며, 현재 CEO는 일론 머스크다"라는 답변이 나옴.
  2. (명제화): LLM이 이 긴 문장을 원자 단위(Atomic) 명제로 쪼갬. $\rightarrow$ [1. 애플은 1976년에 창립됨], [2. 스티브 잡스가 창립함], [3. 현재 CEO는 일론 머스크임].
  3. (검증/Entailment): 각 명제를 검색된 문서(Context)와 대조함. 문서에 1, 2번은 있지만 3번 내용은 없음.
  4. (점수 계산): 3개 명제 중 2개만 문서로 뒷받침되므로 충실성 점수 = 2/3 = 0.66점.
- **구체 예시**: 사내 메신저 봇. 문서에는 "식대는 1만 원 지원"이라고 적힘. LLM이 "식대는 1만 원이며, 야근 시 택시비도 지원됩니다."라고 답함. 택시비 내용은 문서에 없으므로 Faithfulness 점수 감점!
- **흔한 오해/주의점**: 충실성이 1.0(만점)이라고 해서 정답이라는 보장은 없음! 검색 엔진이 엉뚱한 쓰레기 문서를 가져왔는데, LLM이 그 쓰레기 문서의 내용을 단 하나도 안 틀리고 그대로 베껴 쓰면 충실성 점수는 1.0 만점이 나옴. (이래서 Answer Relevancy, Context Precision을 같이 봐야 함).

## 연결 개념
- **Hallucination (환각)**: 충실성(Faithfulness) 지표가 낮다는 것은 100% 환각이 발생했다는 뜻. 환각을 잡는 레이더.
- **NLI (Natural Language Inference)**: 한 문장이 다른 문장을 논리적으로 포함(Entail)하는지, 모순(Contradiction)되는지 판별하는 NLP 태스크. 충실성 검증의 기반 기술.
- **RAGAS / TruLens**: Faithfulness를 자동 채점해 주는 대표적인 평가 프레임워크. (TruLens에서는 Groundedness라는 용어로도 혼용됨).

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: 생성된 답변(Answer)에 포함된 정보의 총량이 검색된 문맥(Context)에 의해 논리적으로 연역(Entailment) 및 지지(Supported)되는 비율을 수치화한 RAG 생성 품질(Generation Quality) 평가지표.
- **가치**: RAG 아키텍처의 가장 치명적 결함인 LLM의 사전 학습 지식 개입(Parametric Memory Leak) 및 환각(Hallucination) 현상을 문장(Claim) 단위로 정밀하게 추적하고 수치화(0~1점)하여 배포(Release) 차단 기준으로 활용함.
- **판단 포인트**: 정보 추출 시 분해되는 명제(Statement)의 입도(Granularity)에 따라 점수 변동이 크며, 이 지표가 1.0이라도 검색된 문맥 자체가 오답(Garbage In)이면 답변 역시 오답(Garbage Out)임을 인지해야 함.

## Ⅰ. 개요 및 필요성
- **정의**: 거대 언어 모델(LLM)이 생성한 답변의 모든 주장이 주어진 외부 컨텍스트(Retrieval Context)에서 사실적, 논리적으로 기원(Grounded)하였는지를 평가하는 척도.
- **배경**: LLM은 주어진 컨텍스트로 프롬프트를 제한(Context-stuffing)해도, 모델 내부에 내재된 강력한 사전 학습 가중치가 발현되어 컨텍스트에 없는 내용을 무의식적으로 덧붙이는 구조적 환각(Hallucination) 리스크가 존재.
- **필요성**: 금융권, 의료, 법률 등 "모르면 모른다고 대답해야 하는(I don't know)" 무결점(Zero-hallucination) 도메인에서 모델의 답변 신뢰성을 보장하기 위한 필수 지표임.

## Ⅱ. Faithfulness 측정 파이프라인 (RAGAS 방법론)
Faithfulness 점수는 다음의 3단계 파이프라인(LLM-as-a-Judge)을 통해 $0 \sim 1$ 사이의 값으로 도출됨.
1. **명제 분할 (Statement Extraction)**
   - 생성된 긴 답변(Answer) 텍스트를 LLM 프롬프트를 이용해 쪼갤 수 없는 최소 단위의 독립적 명제 세트 $S = \{s_1, s_2, ..., s_n\}$로 분리.
2. **검증 연산 (Verification / Entailment Check)**
   - 각 명제 $s_i$가 검색된 문맥(Context) $C$에 의해 증명 가능한지(Supported) LLM Judge 또는 NLI 모델을 통해 Yes(1) / No(0) 이진 판별 수행.
3. **수식 연산 (Score Calculation)**
   - $Faithfulness = \frac{|V|}{|S|}$ (단, $|V|$는 Context에 의해 뒷받침되는(Yes) 명제의 수, $|S|$는 전체 명제의 수)

## Ⅲ. 관련/유사 평가 지표와의 딥다이브 비교
| 지표명 | 평가 축 (Triad) | 측정 목적 | 이상 상황 (예시) |
|:---:|:---|:---|:---|
| **Faithfulness** <br>(충실성) | Context $\leftrightarrow$ Answer | 문서에 없는 말을 **지어내지(환각) 않았는가?** | 점수 0.5: 문서엔 식대 지원만 있는데, 야근 수당 내용도 지어내서 답변함. |
| **Answer Relevancy** <br>(관련성) | Question $\leftrightarrow$ Answer | 동문서답 안 하고 **질문에 똑바로 답했는가?** | 점수 0.1: "A회사 위치는?" 물었는데 "A회사 매출은 100억입니다"라고 답함. |
| **Context Precision**<br>(정밀도) | Question $\leftrightarrow$ Context | 검색 엔진이 **정답 문서를 잘 찾아왔는가?** | 점수 1.0인데 Faithfulness 0.1: 제대로 찾았음에도 LLM이 엉뚱한 소설을 씀. |

## Ⅳ. 고도화: NLI (Natural Language Inference) 기반 최적화
- **LLM Judge의 한계**: 수많은 명제(Statement)를 GPT-4로 일일이 "Yes/No" 프롬프팅을 하면 API 과금 폭탄 및 속도 병목 발생.
- **NLI 교체 전략**: 두 문장을 입력받아 `Entailment(함의)`, `Contradiction(모순)`, `Neutral(중립)` 세 가지 클래스 확률을 뱉어내는 가벼운 분류 특화 모델(RoBERTa-Large-MNLI 등)을 심사관으로 교체.
- **효과**: 토큰 비용을 1/100 이하로 낮추고, 수천 건의 QA 로그를 밀리초(ms) 단위로 배치 검증(Batch Verification)할 수 있는 MLOps 효율성 달성.

## Ⅴ. 운영 시 한계점 및 최적화 전략
- **리스크 1: 추론(Reasoning)에 대한 엄격한 징벌 오류**:
  - Context: "물 1리터 100원, 2리터 구매 시 10% 할인."
  - Answer: "물 2리터는 180원입니다."
  - 위 경우 논리적 추론(Math)이 개입되었으나, "180원"이라는 텍스트 자체가 Context에 없으므로 Faithfulness 모델이 환각(No)으로 잘못 판정할 수 있음.
  - **대응 방안**: 심사관(Judge) 프롬프트에 "단순 텍스트 매칭이 아닌, 주어진 정보에서 논리적/산술적으로 도출 가능한 정보면 지지(Supported)되는 것으로 간주하라"는 Chain-of-Thought 지시어 명시.
- **리스크 2: Garbage In, Garbage Out의 착시 현상**:
  - Faithfulness가 1.0 만점이라도 정답이라는 보장이 절대 없음. 검색 결과(Context)가 오답 문서이면, 그것을 충실히 요약해도 결국 오답임.
  - **대응 방안**: 품질 릴리스 게이트(Release Gate) 설정 시 단일 지표에 의존하지 말고, 검색 지표(Context Precision/Recall)와 곱(Product) 연산으로 복합 결합하여 판단.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: Faithfulness Score (Threshold: 0.90 이상 통과).
- **실무 설계**: 병원 내부 임상가이드라인(CP) RAG 서비스. LLM 환각 발생 시 치명적인 의료 사고로 직결됨. 시스템 파이프라인에 Self-Correction(자가 수정) 루프를 설계함. 1차 답변을 생성한 후 백그라운드에서 NLI 모델로 Faithfulness를 내부 채점함. 점수가 0.95 미만으로 나오면, LLM에게 "너의 방금 답변 중 3번 문장이 문서에 없는 내용이다. 그 문장을 제거하고 다시 답해라"라는 프롬프트를 자동 루프(Agentic RAG)로 재주입하여, 1.0이 될 때까지 답변을 사용자에게 노출하지 않도록 방어 로직 구현.
- **결론**: Faithfulness는 환각이라는 거대한 망령과 싸우는 RAG 시스템의 최후 방어선(Last Line of Defense)이며, 모델의 통제 불가능한 언어적 창의성을 비즈니스 요구사항에 맞게 '팩트의 감옥'에 가둬두는 핵심 품질 제어 장치임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: 명제 분할(Statement Extraction) 알고리즘 방식, NLI의 Cross-entropy Loss 기반 분류 메커니즘과 Softmax 결괏값 처리 수학적 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: Self-RAG 논문의 Critic 모델(비평가 모델) 구조 차용 아키텍처 설계, 무결성 검증을 위한 CI/CD 내 Automated Testing(TruLens 연동) 구축 사례 중심.
