---
title: "RAG 평가 (RAG Evaluation)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 126
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **RAG 평가** | RAG 평가 (RAG Evaluation)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 검색증강생성(RAG) 시스템이 "질문에 맞는 올바른 문서를 찾아왔는지(Retrieval)"와 "그 문서를 바탕으로 환각 없이 똑똑하게 답을 썼는지(Generation)"를 분리하여 정량적으로 채점하는 종합 평가 체계.
- **필요성**: RAG가 오답을 냈을 때, LLM이 멍청해서(환각) 틀린 건지, 아니면 검색엔진(Vector DB)이 쓰레기 문서를 던져줘서 틀린 건지 알 수가 없음. 원인을 정확히 짚어내야 시스템을 고칠 수 있음.
- **핵심 직관**: 논술 시험 채점. 1단계: "참고 문헌은 제대로 된 걸 가져왔나?"(검색 평가). 2단계: "참고 문헌에 없는 뇌피셜(환각)을 쓰진 않았나?"(생성 평가). 이 두 가지를 따로따로 점수 매기는 과정.

## 깊이 이해
- **배경**: 초기에는 답변 텍스트만 보고 BLEU나 ROUGE 같은 단어 겹침 지표로 평가했으나, LLM의 유창함(Fluency) 때문에 오답도 그럴싸해 보여 평가가 불가능해짐. 이에 RAG의 파이프라인(검색 $\rightarrow$ 생성) 특성에 맞춘 다차원 평가 프레임워크(Ragas, TruLens, ARES 등)가 등장함.
- **작동 원리 (Triad 구조)**:
  RAG 평가는 주로 세 가지 핵심 축(Triad)으로 구성됨.
  1. **질문-문서 (Context Relevance)**: 질문과 검색된 문서가 관련이 있는가? (검색 엔진 성능)
  2. **문서-답변 (Groundedness / Faithfulness)**: 답변이 검색된 문서의 내용에만 뿌리를 두고 있는가? (환각 억제력)
  3. **질문-답변 (Answer Relevance)**: 답변이 처음에 사용자가 물어본 의도에 정확히 답하고 있는가? (동문서답 방지)
- **비유**: 법정에서의 변호사. 증거 수집(검색) $\rightarrow$ 증거에 기반한 변론(Groundedness) $\rightarrow$ 판사 질문에 맞는 핵심 답변(Answer Relevance).
- **흔한 오해/주의점**: "우리 RAG는 정답률 90%입니다!"라는 단일 점수는 사기일 확률이 높음. 검색 재현율(Recall)은 99%인데 생성 충실성(Faithfulness)이 50%라서 평균이 90%처럼 보일 수도 있기 때문. 반드시 세부 지표를 쪼개서 대시보드로 봐야 함.

## 연결 개념
- **RAGAS / TruLens**: RAG 평가를 자동화해 주는 대장급 오픈소스 프레임워크.
- **LLM-as-a-Judge**: 사람이 일일이 채점하기 힘드니, 더 똑똑한 LLM(예: GPT-4o)을 심사위원으로 앉혀서 위 지표들을 채점하게 만드는 기술.
- **Hallucination (환각)**: RAG 평가가 가장 잡아내고 싶어 하는 궁극적인 적. 근거 없는 소설 쓰기.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: RAG 아키텍처의 디커플링(Decoupling) 특성에 맞추어, 검색 품질(Retrieval Metrics)과 생성 품질(Generation Metrics)을 독립된 차원(Dimension)에서 정량/정성적으로 측정하는 다층적 평가 프레임워크.
- **가치**: 시스템 실패(Failure)의 원인(Root Cause)이 '근거 문서 누락(검색)'인지 '파운데이션 모델의 할루시네이션(생성)'인지를 명확히 식별하여, 엔지니어링 최적화 방향(청킹, 리랭커 도입, 프롬프트 튜닝 등)을 제시.
- **판단 포인트**: 방대한 질의 로그를 사람이 평가할 수 없으므로 LLM-as-a-Judge를 도입하되, 판사 모델의 편향(Bias)을 제어하기 위한 기준(Ground Truth) 데이터셋 구축과 Human-in-the-loop 검증 병행 필요.

## Ⅰ. 개요 및 필요성
- **정의**: 사용자의 질의(Query), 검색된 문맥(Context), 생성된 답변(Response), 그리고 실제 정답(Ground Truth) 4가지 요소를 상호 교차 비교하여 RAG 시스템의 신뢰성을 종합 평가하는 체계.
- **배경**: 기존 NLP 생성 모델 평가 지표인 BLEU, ROUGE 등은 단순 N-gram 토큰 매칭 기반이므로, 형태소는 다르나 의미가 같은 생성형 AI의 답변 품질을 제대로 측정하지 못함.
- **필요성**: 엔터프라이즈 환경에서 RAG 봇을 프로덕션(Production) 레벨로 배포하기 위한 정량적 SLA(Service Level Agreement) 기준을 확립하고, 모델 교체나 파이프라인 튜닝 시 A/B 테스트의 기준으로 삼기 위함.

## Ⅱ. RAG 평가의 3대 핵심 축 (RAG Triad)
평가 프레임워크 TruLens가 제안한 가장 범용적인 평가 3요소.
1. **Context Relevance (문맥 관련도)**
   - **측정**: 질의(Query) $\leftrightarrow$ 검색된 문서(Context)
   - **목적**: 검색기(Retriever)가 쓸데없는 노이즈 문서를 가져오지 않고, 질문을 푸는 데 꼭 필요한 문서만 가져왔는가? (Top-K 정밀도 측정).
2. **Groundedness / Faithfulness (근거 기반성 / 충실성)**
   - **측정**: 검색된 문서(Context) $\leftrightarrow$ 생성된 답변(Response)
   - **목적**: LLM이 검색된 문서에 없는 내용을 자신의 사전 지식으로 날조(환각)하지 않았는가?
3. **Answer Relevance (답변 관련성)**
   - **측정**: 질의(Query) $\leftrightarrow$ 생성된 답변(Response)
   - **목적**: 동문서답하지 않고 사용자의 본래 질문 의도에 정확히 부합하는 유용한 정보를 제공했는가?

## Ⅲ. 주요 RAG 평가 프레임워크 비교
| 프레임워크 | 핵심 철학 및 특징 | 측정 방식 |
|:---:|:---|:---|
| **RAGAS** | Ground Truth(실제 정답 데이터) 없이도 LLM을 판사로 사용하여 평가가 가능한 점이 최대 장점. (현재 업계 표준) | 역질문 생성(Reverse Generation) 및 NLI(자연어 추론) 기반 판정. |
| **TruLens** | RAG Triad(3대 축) 개념을 처음 정립. Feedback Function이라는 개념으로 평가 로직 모듈화. | LLM 프롬프팅을 통한 Score(0~10점) 부여 방식. |
| **ARES** | 수동 평가셋(Human Preference)을 적은 비용으로 학습시켜, 도메인 특화된 평가기를 만드는데 강점. | Few-shot Prompting과 미세조정(Fine-Tuning) 결합. |

## Ⅳ. 심화: LLM-as-a-Judge 도입의 기술적 메커니즘
- 사람이 1만 개의 QA 쌍을 채점하려면 막대한 비용 발생. GPT-4 등의 거대 모델을 채점관(Judge)으로 활용.
- **프롬프트 엔지니어링**:
  ```text
  [System] 당신은 공정한 채점자입니다.
  [Question]: {사용자 질문}
  [Context]: {검색된 문서}
  [Answer]: {RAG의 답변}
  [지시]: Answer의 모든 문장이 Context에 기반하는지 판단하여, [1] 예, [0] 아니오 로 점수를 내고 이유를 설명하시오.
  ```
- **환각 교차 검증**: Ragas의 경우, Answer에서 평서문 명제들을 뽑아낸 뒤, 그 명제들이 Context로부터 연역적으로 도출 가능한지(Entailment) 수학적 확률로 계산함.

## Ⅴ. 운영 시 한계점 및 최적화(MLOps) 전략
- **리스크 1: LLM 판사의 편향 (Position Bias & Verbosity Bias)**:
  - LLM 심사위원은 선택지가 먼저 나오거나(Position Bias), 정답 여부와 무관하게 글이 길고 유창하면(Verbosity Bias) 점수를 후하게 주는 경향이 있음.
  - **대응 전략**: 프롬프트 상에 순서를 뒤바꾸어 두 번 묻게 하거나(Swap Test), 길이 제한을 명시. 주기적으로 도메인 SME(전문가)가 100개 샘플을 직접 채점하여 LLM 점수와의 상관계수(Pearson Correlation)를 0.8 이상으로 맞추는 캘리브레이션(Calibration) 수행.
- **리스크 2: 평가 비용의 기하급수적 증가**:
  - LLM-as-a-Judge를 모든 질의에 태우면 API 비용이 메인 서비스보다 더 나옴.
  - **대응 전략**: 프로덕션 환경에서는 사용자 로그 중 1~5%만 샘플링(Sampling)하여 비동기 배치(Batch)로 야간에 평가를 수행하는 파이프라인 설계.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: Ragas 4대 지표(Faithfulness, Answer Relevance, Context Precision, Context Recall), Human-LLM Agreement Rate(일치율).
- **실무 설계**: 금융 상품 추천 RAG 시스템 릴리스 파이프라인. 개발된 RAG 시스템의 청킹 사이즈(512 vs 1024) 최적값을 찾기 위해 Ragas 프레임워크 연동. 평가 데이터셋 500개에 대해 CI/CD 환경에서 야간 자동 평가(GPT-4o Judge) 수행. 사이즈 512일 때 Context Precision은 0.8로 우수하나 Faithfulness가 0.6으로 떨어짐(문맥 단절로 인한 환각 발생). 사이즈 1024일 때 두 지표 모두 0.8 이상을 달성함을 수치적으로 입증하고, 이를 근거로 운영계(PR) 반영 승인 프로세스 통과.
- **결론**: RAG 평가는 장님이 코끼리를 만지는 식의 "느낌적 평가"를 끝내고, AI의 품질을 소프트웨어 공학의 '단위 테스트(Unit Test)' 영역으로 끌어들인 혁신이며, LLMOps의 성패를 가르는 가장 중요한 계기판(Dashboard)임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Ragas 지표 중 Context Recall과 Context Precision의 수학적 수식 비교, NLI(Natural Language Inference) 기반의 Entailment/Contradiction 판정 로직.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: 지속적 배포(CI/CD) 파이프라인 내에서의 Evaluation Gate 구성 방안, Human-in-the-loop(RLHF 연계)를 활용한 자체 평가 모델 파인튜닝 전략 중심 서술.
