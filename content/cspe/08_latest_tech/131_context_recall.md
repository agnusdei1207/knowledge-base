---
title: "문맥 재현율 (Context Recall)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 131
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **핵심 직관** | 형사(검색기)가 용의자(정답 문서)를 잡으러 감 | "이 개념의 핵심" |
| **배경** | 정보 검색(IR) 분야의 가장 오래된 쌍두마차 지표인 Precision(정밀도)과 Recall(재현율) 중 하나 | "자동 품질 검사 라인" |
| **작동 원리 (Ragas 기준 수학적 분해)** | 1. 평가기가 정답 문장(Ground Truth)을 미리 알고 있음 | "이 개념의 핵심" |
| **구체 예시** | 사내 규정 챗봇에 "육아휴직 신청 조건과 기간은?"이라고 물음 | "이 개념의 핵심" |
| **Context Precision (문맥 정밀도)** | Recall과 영원한 트레이드오프(Trade-off) 관계 | "자동 품질 검사 라인" |
| **Hybrid Search (하이브리드 검색)** | Recall이 떨어질 때 이를 방어하기 위해 키워드(BM25)와 벡터 검색을 섞어 쓰는 기술 | "이 개념의 핵심" |
| **Query Expansion (질의 확장)** | 사용자가 대충 질문해서 문서를 못 찾을 때, 질문에 동의어를 잔뜩 붙여서 다시 검색하게 만들어 Recall을 높이는 기법 | "도서관 검색" |

---


# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 사용자의 질문에 완벽한 정답(Ground Truth)을 만들어내기 위해 필요한 모든 근거 지식(Context)을, RAG의 검색기가 "하나도 빠짐없이 싹 다 찾아왔는가?"를 평가하는 지표.
- **필요성**: 정밀도(Precision)가 아무리 높아도, 정작 문제를 푸는 데 꼭 필요한 핵심 단서 한두 개를 검색에서 놓쳐버리면(Recall 부족), LLM은 반쪽짜리 대답을 하거나 모른다고 할 수밖에 없음.
- **핵심 직관**: 형사(검색기)가 용의자(정답 문서)를 잡으러 감. 용의자 5명 중 4명을 잡아옴. "아무나 막 잡아오진 않았네(정밀도 높음)." 근데 주범 1명을 놓쳤음. $\rightarrow$ 재현율(Recall) = 4/5 = 80%.

## 깊이 이해
- **배경**: 정보 검색(IR) 분야의 가장 오래된 쌍두마차 지표인 Precision(정밀도)과 Recall(재현율) 중 하나. RAG 평가 프레임워크(Ragas 등)가 이를 채택하여 LLM의 맥락에 맞게 재정의함.
- **작동 원리 (Ragas 기준 수학적 분해)**:
  1. 평가기가 정답 문장(Ground Truth)을 미리 알고 있음. 
     (예: "프랑스는 유럽에 있고, 수도는 파리이며, 에펠탑이 있다.")
  2. 평가기(LLM Judge)가 정답을 독립된 명제 3개로 쪼갬.
     - 1. 프랑스는 유럽에 있다. 
     - 2. 수도는 파리다. 
     - 3. 에펠탑이 있다.
  3. RAG 검색기가 가져온 문서 뭉치(Context)를 쭉 읽어봄. 1번과 2번 내용은 있는데, '에펠탑'에 대한 내용은 검색해 오지 못했음.
  4. 점수 산출: 필요한 명제 3개 중 2개만 Context에 존재하므로, $Context Recall = 2/3 = 0.66점$.
- **구체 예시**: 사내 규정 챗봇에 "육아휴직 신청 조건과 기간은?"이라고 물음. 검색기가 '조건'이 적힌 문서는 잘 찾아왔는데, '기간'이 적힌 별첨 문서는 못 가져옴. LLM은 '기간'에 대해 답할 수 없어 사용자 불만 발생. 전형적인 Context Recall 부족 현상.
- **흔한 오해/주의점**: Recall을 높이려고 무작정 검색 범위를 100개(Top-100)로 늘리면, 온갖 쓰레기 문서가 섞여 들어와 Context Precision이 박살 나고 LLM의 환각(Lost in the middle)을 유발함. 정밀도와의 밸런싱이 핵심임.

## 연결 개념
- **Context Precision (문맥 정밀도)**: Recall과 영원한 트레이드오프(Trade-off) 관계. 쓰레기 문서를 얼마나 잘 걸러냈는가.
- **Hybrid Search (하이브리드 검색)**: Recall이 떨어질 때 이를 방어하기 위해 키워드(BM25)와 벡터 검색을 섞어 쓰는 기술.
- **Query Expansion (질의 확장)**: 사용자가 대충 질문해서 문서를 못 찾을 때, 질문에 동의어를 잔뜩 붙여서 다시 검색하게 만들어 Recall을 높이는 기법.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: RAG 아키텍처의 정보 검색(Information Retrieval) 파이프라인에서, 질문에 대한 완벽한 Ground Truth(정답)를 재구성하기 위해 요구되는 모든 명제적 지식(Propositional Knowledge)이 검색된 Context 내에 포함(Coverage)된 비율.
- **가치**: LLM 생성 단계 이전에 발생하는 정보의 유실(Information Loss)을 정량화하여, RAG 시스템이 '지식 부족'으로 인해 불완전한 답변이나 환각(Hallucination)을 생성하는 근본 원인(Root Cause)을 식별함.
- **판단 포인트**: 이 지표가 낮으면 임베딩 모델의 한계, 청크 사이즈의 부적절성, 혹은 단순 벡터 검색의 한계이므로, BM25 결합(Hybrid Search), 질의 재작성(Query Rewrite) 등 검색 커버리지를 넓히는 방향으로 아키텍처를 수정해야 함.

## Ⅰ. 개요 및 필요성
- **정의**: 주어진 질의에 대응하는 참조 정답(Reference Answer / Ground Truth)의 정보 요소들이, 시스템이 검색(Retrieve)하여 반환한 문서 세트(Context) 안에 얼마나 온전히 수용되어 있는지를 $0 \sim 1$로 측정한 지표.
- **배경**: LLM은 입력된 프롬프트(Context) 내에 정답을 유추할 근거가 부족할 경우, 내재된 가중치로 무리한 추론을 시도하거나 답변을 포기하여 치명적인 응답 품질 저하를 초래함.
- **필요성**: 엔터프라이즈 환경에서 "정보의 누락"은 잘못된 의사결정을 유발하므로, 검색 엔진이 필요한 단서를 하나도 놓치지 않고 포획(Capture)하는 역량을 모니터링하기 위함.

## Ⅱ. 수식 및 작동 메커니즘 (Ragas 프레임워크 기준)
전통적인 Recall은 단순 문서 매칭이나, Ragas의 Context Recall은 LLM을 활용한 의미론적 명제 일치(Semantic Proposition Match)를 수학적으로 산출함.
- **수식 구조**:
  $Context Recall = \frac{\text{Number of Ground Truth sentences supported by Context}}{\text{Total number of sentences in Ground Truth}}$
- **메커니즘 (LLM-as-a-Judge Pipeline)**
  1. **Ground Truth 분해**: 평가 데이터셋에 있는 완벽한 정답 텍스트를 LLM 프롬프트를 통해 여러 개의 단일 명제(Claim/Sentence)로 쪼갬.
  2. **교차 검증 (Cross-check)**: 쪼개진 정답 명제들을 하나씩 순회하며, "이 명제의 내용이 검색된 Context 뭉치 안에 존재하는가?"를 LLM에게 질의.
  3. **비율 연산**: 전체 정답 명제 중 Context에 의해 지지(Supported)되는 명제의 비율을 산출.

## Ⅲ. 품질 매트릭스: Context Precision과의 트레이드오프 (Trade-off)
정보 검색의 영원한 딜레마인 Precision과 Recall의 균형 조정.
| 최적화 방향 | 조치 사항 | Context Recall 변화 | Context Precision 변화 | 한계 및 부작용 |
|:---:|:---|:---:|:---:|:---|
| **검색 윈도우 확대**| Top-K를 5 $\rightarrow$ 20으로 증가 | **상승 $\uparrow$** | 하락 $\downarrow$ | 잡다한 문서가 섞여 들어가 LLM 입력 토큰 낭비 및 환각 유발. |
| **청크 사이즈 확대**| 256 $\rightarrow$ 1024 Token | **상승 $\uparrow$** | 하락 $\downarrow$ | 문맥 짤림은 줄어드나, 청크 내 노이즈가 많아져 벡터 의미가 희석됨. |
| **하이브리드 도입** | Vector Search + BM25(키워드) | **상승 $\uparrow$** | 유지/소폭 하락 | 어휘 불일치(Vocabulary Mismatch) 방어 가능하나 아키텍처 복잡도 증가. |

## Ⅳ. 고도화: Context Recall 하락의 원인과 해결 아키텍처
Recall이 낮다는 것은 낚싯대(검색) 그물이 너무 성기거나 엉뚱한 곳에 던져졌다는 의미.
1. **키워드/고유명사 매칭 실패 (Vocabulary Mismatch)**:
   - Dense Vector(임베딩)는 의미는 잘 찾지만, "AB-123" 같은 특정 부품 번호를 찾는데 쥐약임.
   - **해결**: Sparse Vector(BM25, SPLADE)를 결합한 **Hybrid Search** 도입.
2. **질의의 모호성 (Query Ambiguity)**:
   - 사용자가 "그 정책 어때?"라고 대충 치면 검색기가 방향을 못 잡음.
   - **해결**: LLM을 프론트엔드에 배치하여 질문을 구체화하는 **Query Rewrite (질의 재작성)** 또는 HyDE(가설적 답변 생성) 적용.
3. **다중 문서 산재 (Multi-hop Reasoning)**:
   - "2022년과 2023년의 매출 차이는?" $\rightarrow$ 22년 문서와 23년 문서 두 개를 동시에 찾아야 함.
   - **해결**: 질문을 쪼개는 **Sub-Query Decomposition** 파이프라인(LangChain 활용) 도입.

## Ⅴ. 실무 적용 및 결론
- **판단 지표**: Context Recall (Threshold: 0.85 이상 통과), Ground Truth 커버리지율.
- **실무 설계**: A제조사 설비 정비 매뉴얼 RAG. 엔지니어가 "모터 과열 시 조치 방법 3단계"를 질문. 기존 순수 Vector Search 환경에서 평가 결과 Context Recall이 0.50으로 저조하게 나옴. 분석 결과, 조치 방법 3단계 중 마지막 단계가 다른 문서에 쪼개져 있어 이를 검색하지 못함(문서 분절 문제). 이를 해결하기 위해 상하위 문서를 묶어서 검색하는 **Parent-Child Chunking (Auto-merging Retriever)** 기법을 LlamaIndex 기반으로 구현하여 재배포. 재측정 결과 Recall 0.95를 달성하며 누락 없는 완벽한 정비 가이드 제공.
- **결론**: Context Recall은 RAG 시스템이 보유한 '지식의 지평(Horizon of Knowledge)'이 질의의 요구사항을 얼마나 온전히 감싸 안을 수 있는지를 보여주는 근원적 체력 지표이며, 이 지표의 타협은 곧 AI의 무능으로 귀결됨을 명심해야 함.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Information Retrieval의 재현율 수식($TP / (TP+FN)$)과 LLM 기반 Semantic Recall 측정 메커니즘 간의 비교 분석.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: Recall 확대를 위한 Advanced RAG 기법들(Sentence Window Retrieval, Query Routing)의 아키텍처 다이어그램 및 설계 기준 제시.
