---
title: "교정형 RAG (Corrective RAG)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-08_latest_tech"
weight: 106
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **교정형 RAG** | 교정형 RAG (Corrective RAG)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 검색기(Retriever)가 가져온 문서들을 무조건 믿지 않고, "이 문서가 질문에 답하기에 적절한가?"를 평가(Evaluate)하여 올바르면 취하고, 모호하면 정제하고, 틀리면 웹 검색(Web Search) 등으로 대체하는 교정(Correction) 파이프라인.
- **필요성**: 기존 RAG는 검색된 문서가 질문과 전혀 상관없는 오답이어도, LLM이 그 오답 문서를 근거로 당당하게 환각(Hallucination)을 생성해 버리는 치명적 결함이 있음.
- **핵심 직관**: 학생이 도서관에서 책을 무작위로 빌려오면, 지도교수(Evaluator)가 먼저 읽어보고 "이 책은 정답(Correct)", "이 책은 쓰레기니 버리고 구글링해와(Incorrect)", "이 책은 반만 맞으니 요약해와(Ambiguous)"라고 필터링해 준 뒤 보고서를 쓰게 하는 것.

## 깊이 이해
- **배경**: 2024년 1월, 구글과 칭화대 연구진이 제안(CRAG). RAG의 성패는 검색된 문서의 품질이 좌우한다는 점에 착안하여, 생성(Generation) 이전에 검색 품질을 평가-교정하는 방어막(Guardrail)을 설계함.
- **작동 원리 (Retrieve $\rightarrow$ Evaluate $\rightarrow$ Correct $\rightarrow$ Generate)**:
  1. (검색): 기존처럼 Top-K 문서를 검색함.
  2. (평가): 경량화된 평가 모델(T5-Large 등)이 각 문서를 질문과 대조하여 `Correct(정답)`, `Incorrect(오답)`, `Ambiguous(모호함)` 3단계로 분류.
  3. (교정 - 핵심 로직):
     - `Correct`: 쓸모없는 주변 문장을 잘라내어 지식 정제(Knowledge Refinement).
     - `Incorrect`: 이 문서를 버리고, 질문을 구글 웹 검색(또는 다른 API)에 던져 새로운 지식을 가져옴.
     - `Ambiguous`: 정제된 지식과 웹 검색 결과를 합침.
  4. (생성): 교정된 완벽한 컨텍스트로 답변 생성.
- **구체 예시**: Q: "2023년 노벨 평양상 수상자는?" $\rightarrow$ 벡터 DB에 옛날 데이터만 있어 "2021년 수상자" 문서가 검색됨 $\rightarrow$ Evaluator: "질문은 2023년인데 문서는 2021년이네? Incorrect!" $\rightarrow$ 웹 검색 모듈 가동하여 2023년 수상자 크롤링 $\rightarrow$ 올바른 답변 생성.
- **흔한 오해/주의점**: 평가 모델(Evaluator)의 정확도가 전체 시스템의 목숨줄임. 평가자가 멍청해서 정답 문서를 Incorrect로 판정하면 오히려 성능이 Naive RAG보다 폭락함.

## 연결 개념
- **Self-RAG**: 생성된 토큰 단위로 스스로 반성하는 방식. (CRAG는 프롬프트에 들어가기 전 '문서 자체'를 평가하는 방식)
- **Web Search Fallback**: 사내 데이터에 답이 없을 때 외부 지식으로 전환하는 CRAG의 핵심 교정(Correction) 기법.

---

# 📝 【답안용】 시험 답안 템플릿
## 핵심 인사이트 (3줄 요약)
- **본질**: Retrieval(검색)과 Generation(생성) 사이에 Evaluation(평가) 및 Correction(교정) 레이어를 샌드위치처럼 삽입하여, 저품질 검색 결과가 LLM으로 유입되는 것을 원천 차단하는 방어형 아키텍처.
- **가치**: 문서 품질이 균일하지 않고 결측치(Missing Data)가 많은 실제 엔터프라이즈 환경에서, 내부 문서의 공백을 동적 웹 검색(Web Search)으로 메워 환각률을 극적으로 낮춤(PopQA 기준 정확도 16% 향상).
- **판단 포인트**: 분류기(Evaluator)의 평가 정확도 임계치(85% 이상 요구), 웹 검색 의존에 따른 보안 및 할루시네이션(비신뢰 사이트 유입) 통제, 파이프라인 추가에 따른 응답 지연(TTFT) 증가.

## Ⅰ. 개요 및 필요성
- **정의**: 검색된 각각의 문서(Document)를 사용자 질의와 대조하여 관련성(Relevance)을 3단계(Correct, Incorrect, Ambiguous)로 평가하고, 그 결과에 따라 지식 정제(Refinement)나 외부 검색(Web Search)으로 컨텍스트를 교정한 뒤 응답을 생성하는 기술.
- **배경**: 기존 RAG 프레임워크는 검색기(Retriever)의 결과물을 무조건적으로 신뢰하여 생성기(Generator)에 주입하므로, 검색 오류가 곧바로 생성 오류(Hallucination)로 이어지는 취약성이 존재함.
- **필요성**: 사내 지식 베이스에 정답이 없는 'Out-of-domain' 질의에 대응하고, 문맥에 맞지 않는 엉뚱한 정보가 혼입되어 모델이 오작동하는 현상을 방지하기 위함.

## Ⅱ. CRAG (Corrective RAG) 아키텍처 및 워크플로
```text
[ User Query ] -> [ Retriever (Top-K) ] -> 검색된 문서들 (D1, D2, ...)
                          |
                  [ Evaluator (평가 모델) ]
            /             |             \
   [ Correct ]       [ Ambiguous ]      [ Incorrect ]
        |                 |                  |
(Knowledge Refinement) (Combine)      (Web Search) -> 새 지식 추출
        \                 |                  /
         +----------------+-----------------+
                          |
             [ 정제 및 교정된 최종 Context ]
                          |
[ Generator (LLM) ] -> [ Final Answer ]
```

## Ⅲ. 3대 평가 등급별 교정(Correction) 액션
| 평가 등급 | 판정 기준 | Action (교정 전략) |
|:---:|:---|:---|
| **Correct (정답)** | 문서가 질의에 대한 명확한 해답을 포함함 | **Knowledge Refinement**: 문서 내 핵심 문장(Strip)만 추출하여 토큰을 압축하고 노이즈 제거 |
| **Incorrect (오답)** | 문서가 질의와 무관함 (검색 실패) | **Web Search Fallback**: 버리고, DuckDuckGo나 Google Search API를 호출하여 외부에서 지식 탐색 |
| **Ambiguous (모호함)**| 관련은 있으나 해답으로 불충분함 | **Hybrid Combine**: 기존 문서의 정제된 요약본과 웹 검색 결과를 융합(Combine)하여 주입 |

## Ⅳ. 주요 특징 및 비교
| 구분 | Naive RAG | Advanced RAG (Reranking) | Corrective RAG (CRAG) |
|:---:|:---|:---|:---|
| **통제 방식** | 무검증 주입 | 가져온 후보들의 '순위' 재조정 | 후보 자체를 '평가'하고 '대체/수정' |
| **지식 확장** | 내부 DB 한정 | 내부 DB 한정 | 내부 DB + **외부 웹 검색 병행** |
| **데이터 결측 대응** | 엉뚱한 문서로 환각 생성 | 1등 오답 문서를 활용해 환각 생성 | **오답을 버리고 웹에서 찾아 해결** |

## Ⅴ. 한계점(리스크) 및 운영 방안
- **리스크 1: Evaluator(평가자) 모델의 병목 및 오판**:
  - LLM API를 Evaluator로 쓰면 지연 시간(Latency)이 1~2초 추가되고 비용이 두 배 듦. 경량 모델(T5 등)을 쓰면 오판(오답인데 정답으로 분류) 확률이 높아짐.
  - **대응 방안**: T5-Large 수준의 가벼운 모델을 자사 도메인 데이터로 파인튜닝(SFT)하여 전용 Evaluator로 배치. 평가 판정의 Confidence Score가 낮을 경우 무조건 'Ambiguous'로 보수적으로 라우팅.
- **리스크 2: 보안 환경에서의 웹 검색 통제**:
  - 금융/공공 등 폐쇄망(Air-gapped) 환경에서는 외부 Web Search Fallback 호출이 불가능하거나 보안 정책에 위배됨.
  - **대응 방안**: Web Search 대신, 사내의 다른 신뢰할 수 있는 데이터 소스(예: 전사 ERP, 레거시 RDBMS)로 연결하는 Internal API Fallback 구조로 대체 설계.

## Ⅵ. 실무 적용 및 결론
- **판단 지표**: 환각 감소율(Hallucination Drop Rate), Evaluator의 F1-Score(정확도), 웹 검색 전환율(Fallback Rate).
- **실무 설계**: 고객사 A/S 센터 챗봇 구축. 구형 제품 매뉴얼은 DB에 있으나, 최신 출시 제품은 아직 색인(Index)되지 않음. CRAG 아키텍처를 도입하여, 최신 제품 관련 질문이 들어오면 Evaluator가 기존 DB 문서들을 "Incorrect"로 판정하고, 자동으로 공식 홈페이지의 최신 FAQ 웹페이지를 실시간 크롤링(Web Search)하여 답변하도록 설계함.
- **결론**: 교정형 RAG는 "가져온 정보를 의심하라"는 비판적 사고를 AI 파이프라인에 이식한 모델이며, 엔터프라이즈 환경에서 지식베이스의 불완전성(Data Incompleteness)을 유연하게 극복할 수 있는 실전 지향적 아키텍처임.

### 🔀 문제 유형별 목차 전환
- **Ⅱ·Ⅲ 강조 (개념/원리형)**: Evaluator의 Confidence 임계값(Threshold) 처리 방식, Knowledge Refinement 시 LLM을 통한 텍스트 압축 메커니즘 중심 서술.
- **Ⅴ·Ⅵ 강조 (실무/설계형)**: 페쇄망 환경에서의 Fallback 대안(Agentic RAG 연계), Evaluator 모델의 경량화(SLM) 및 온디바이스 서빙(Cost/Latency 관점) 아키텍처 구성 전략 작성.
