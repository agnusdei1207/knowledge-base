---
title: "고도화 RAG (Advanced RAG)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 103
---

# 📖 【암기용】 개념 완전 이해

> 목적: Advanced RAG를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 기본 RAG에 쿼리 변환·하이브리드 검색·리랭킹·후처리·평가를 추가한 고도화 구조
- **왜 필요한가**: Naive RAG는 검색 오류가 곧 답변 오류가 되므로, 검색 전후 품질 통제 단계가 필요함.
- **핵심 직관**: 자료를 그냥 붙이는 것이 아니라 질문을 다듬고, 자료를 여러 방식으로 찾고, 채점 후 상위 근거만 쓰는 방식임.

## 깊이 이해
- **배경·문제의식**: 실제 문서는 동의어·약어·표·PDF·권한 메타데이터가 섞여 있어 단일 벡터 검색만으로 정답 근거를 찾기 어려움.
- **작동 원리**: Query Rewrite로 질의를 보정하고, BM25+Dense로 후보를 넓힌 뒤 Cross-Encoder로 재정렬하고, 컨텍스트 압축·출처 검증 후 생성함.
- **비유**: 논문 작성 전 검색어를 여러 개 만들고, 학술DB와 키워드 검색을 함께 돌린 뒤, 관련도 높은 논문만 인용하는 절차임.
- **구체 예시**: 고객센터 RAG에서 Dense Top-10만 사용 시 Precision@3 62%, Hybrid+Rerank 적용 시 84%, 평균 지연 900ms→1.4초.
- **흔한 오해·주의점**: 단계가 많을수록 항상 이득은 아님. 리랭커·평가 호출은 지연과 비용을 증가시키므로 SLA 기준으로 조합해야 함.

## 연결 개념
- Naive RAG — Advanced RAG의 기준선
- Hybrid Search — Sparse와 Dense 후보를 결합하는 검색 단계
- Reranker — 후보 문서를 정밀 재정렬하는 후처리 모델

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Advanced RAG는 검색 전·중·후 품질 통제 단계를 추가한 운영형 RAG 구조임.
> 2. **가치**: Hybrid+Rerank로 Precision@3 62%→84% 향상, 환각률을 15% 이하로 관리함.
> 3. **판단 포인트**: 품질 이득과 지연 증가(900ms→1.4초)를 SLA·비용 기준으로 조정해야 함.

## Ⅰ. 개요 및 필요성

Advanced RAG는 품질 통제형 RAG 구조임. Naive RAG는 Top-K 검색 결과를 그대로 사용해 무관 문서와 중복 청크가 답변 오류를 유발한다. 운영 환경에서는 쿼리 변환, 하이브리드 검색, 리랭킹, 평가 지표가 함께 필요하다.

## Ⅱ. 구조 및 구성요소

```text
Query → Rewrite/Decompose → Hybrid Search → Reranker
  → Context Compress → Generator → Evaluator/Guardrail
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Query Processor | 질의 재작성·분해·확장 | HyDE, Multi-Query, Decomposition |
| Hybrid Retriever | BM25와 Dense 검색 결합 | RRF로 후보 20~50개 병합 |
| Reranker | Cross-Encoder 재정렬 | Precision@3 15~25%p 향상 |
| Evaluator | 답변·근거 일치성 평가 | Ragas faithfulness ≥0.9 목표 |

> 요약: Advanced RAG는 질의 보정부터 답변 평가까지 품질 통제 지점을 파이프라인 전 구간에 배치함.

## Ⅲ. 동작원리 및 흐름도

```text
질의 입력 → 쿼리 재작성 → Sparse/Dense 병렬 검색
  → RRF 후보 병합 → Cross-Encoder 리랭킹
  → 컨텍스트 압축 → 생성·출처 검증 → 응답
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Query Rewrite·HyDE로 검색 질의 보정 | 검색 실패율 30% 이상 감소 |
| 2 | BM25 Top-50 + Dense Top-50 병렬 검색 | Recall@20 ≥ 95% |
| 3 | RRF 병합 후 Cross-Encoder Top-5 선정 | Precision@3 ≥ 80% |
| 4 | 컨텍스트 압축·생성·Ragas 평가 | faithfulness ≥0.9, 지연 < 2초 |

> 요약: 검색 전 질의 품질, 검색 중 후보 재현율, 검색 후 근거 정밀도를 순차적으로 높여 답변 품질을 통제함.

## Ⅳ. 특징

| 구분 | Naive RAG | Advanced RAG | 판단 포인트 |
|:---|:---|:---|:---|
| 검색 방식 | 단일 Dense Top-K | BM25+Dense+RRF | 약어·정확명 검색은 Hybrid 우위 |
| 후처리 | 없음 | Cross-Encoder 리랭킹 | Precision@3 80% 미만이면 적용 |
| 평가 | 수동 샘플링 | Ragas·LLM-as-Judge | 운영 SLA는 자동 평가 필요 |
| 비용 | 호출 1~2회 | 호출 3~6회 | 지연 예산 2초 이하로 단계 선택 |

> 요약: Advanced RAG는 품질 통제력을 얻는 대신 호출 수와 지연이 증가하므로 SLA 기준으로 모듈을 선택함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 검색 고도화: BM25 Top-50과 BGE-M3 Dense Top-50을 RRF(k=60)로 병합 후 bge-reranker-large로 Top-5 선정
2. 컨텍스트 관리: 512토큰 청크, MMR 중복 제거, Contextual Compression으로 입력 토큰 40% 절감
3. 품질 게이트: faithfulness 0.9 미만 답변은 재검색, 출처 0건이면 "근거 없음"으로 응답

**결론 (2줄):**
- 기술사 판단: 운영 챗봇·규정 Q&A는 Advanced RAG, 단순 FAQ PoC는 Naive RAG로 시작
- 향후 방향: Agentic RAG와 Graph RAG를 결합해 다단계 추론·관계 검색으로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RAG 고도화를 설명하시오" | Query→Retrieve→Rerank→Evaluate 전체 흐름 | Naive RAG 대비 품질·비용 비교 |
| 요구사항 명시형 | "기업 RAG 설계 방안을 제시하시오" | Hybrid Search·Reranker·Evaluator 선택 기준 | SLA·비용·품질 지표 기반 적용 방안 |

> 요약: 설명형은 고도화 단계 전체, 설계형은 SLA와 품질 지표에 맞춘 모듈 선택을 중심으로 작성함.
