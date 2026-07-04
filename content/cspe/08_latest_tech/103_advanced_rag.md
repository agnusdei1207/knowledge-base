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
- **구체 예시**: 고객센터 RAG에서 Dense Top-10만 사용 시 Precision@3 62%, Hybrid+Rerank 적용 시 84%, 평균 지연 900ms->1.4초.
- **흔한 오해·주의점**: 단계가 많을수록 항상 이득은 아님. 리랭커·평가 호출은 지연과 비용을 증가시키므로 SLA 기준으로 조합해야 함.

## 연결 개념
- Naive RAG — Advanced RAG의 기준선
- Hybrid Search — Sparse와 Dense 후보를 결합하는 검색 단계
- Reranker — 후보 문서를 정밀 재정렬하는 후처리 모델

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Advanced RAG는 검색 전·중·후 품질 통제 단계를 추가한 운영형 RAG 구조임.
> 2. **가치**: Hybrid+Rerank로 Precision@3 62%->84% 향상, 환각률을 15% 이하로 관리함.
> 3. **판단 포인트**: 품질 이득과 지연 증가(900ms->1.4초)를 SLA·비용 기준으로 조정해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 검색 전·중·후 통제 지점 이해 확인 | Query Rewrite -> Hybrid Search -> Rerank -> 평가의 단계별 목적 | 고도화 기법을 리랭킹 하나로만 축소 서술 |
| 기준선 대비 개선 효과 확인 | Precision@3 62%->84%, RRF 병합, faithfulness 0.9 목표 | 개선 효과의 정량 근거 누락 |
| 비용-품질 트레이드오프 판단 확인 | 호출 3~6회 증가, 지연 900ms->1.4초와 SLA 관계 | 모든 모듈 적용을 무조건 정답으로 단정 |

> 요약: 이 문제는 고도화 기법 나열이 아니라 SLA·비용 제약 아래 어떤 통제 모듈을 조합할지의 판단을 묻는다.

## Ⅰ. 개요 및 필요성

- 개요: 품질 통제형 RAG 구조
- 배경: Naive RAG는 Top-K 검색 결과를 그대로 사용해 무관 문서와 중복 청크가 답변 오류로 전파될 수 있음.
- 필요성: query rewrite, hybrid search, cross-encoder reranking, Ragas faithfulness 등 평가 지표로 검색-생성 품질을 통제해야 함.

## Ⅱ. 구조 및 구성요소

```text
Query -> Rewrite/Decompose -> Hybrid Search -> Reranker
  -> Context Compress -> Generator -> Evaluator/Guardrail
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
질의 입력 -> 쿼리 재작성 -> Sparse/Dense 병렬 검색
  -> RRF 후보 병합 -> Cross-Encoder 리랭킹
  -> 컨텍스트 압축 -> 생성·출처 검증 -> 응답
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

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | Advanced RAG | Agentic RAG | 선택 기준 |
|:---|:---|:---|:---|
| 실행 구조 | 고정 단계 파이프라인으로 지연 예측 가능 | 계획 기반 반복 호출로 지연 가변 | 응답 지연 SLA 2초 이내면 Advanced |
| 질의 복잡도 대응 | 단일 주제 질의에 최적 | 질의 분해·다중 도구 결합 대응 | 다단계 추론 질의 비율 높으면 Agentic |
| 운영 통제 | 단계별 지표 관리 단순 | max_step·도구 ACL 등 정책 통제 필요 | 에이전트 통제 체계 미비 시 Advanced 우선 |

> 요약: 지연 예측성과 통제 단순성이 우선이면 Advanced RAG, 복합 질의 분해가 우선이면 Agentic RAG를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지연 예산 초과 | 리랭킹·평가 호출 누적 | 후보 수 축소, 경량 리랭커, 단계별 캐싱 | p95 응답 지연 |
| 질의 의도 왜곡 | Query Rewrite·HyDE의 과도한 변형 | 원 질의 병행 검색(Multi-Query) | 재작성 전후 Recall@20 비교 |
| 비용 대비 효과 미검증 | 모듈 일괄 도입 | 모듈별 A/B 검증 후 효과 없는 단계 제거 | 질의당 호출 비용, Precision@3 증분 |

> 요약: 주요 위험은 단계 추가에 따른 지연·비용 증가이며, 모듈별 A/B 검증과 캐싱으로 통제함.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 검색 고도화: BM25 Top-50과 BGE-M3 Dense Top-50을 RRF(k=60)로 병합 후 bge-reranker-large로 Top-5 선정
2. 컨텍스트 관리: 512토큰 청크, MMR 중복 제거, Contextual Compression으로 입력 토큰 40% 절감
3. 품질 게이트: faithfulness 0.9 미만 답변은 재검색, 출처 0건이면 "근거 없음"으로 응답

**결론 (2줄):**
- 기술사 판단: 운영 챗봇·규정 Q&A는 Advanced RAG, 단순 FAQ PoC는 Naive RAG로 시작
- 향후 방향: Agentic RAG와 Graph RAG를 결합해 다단계 추론·관계 검색으로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "RAG 고도화를 설명하시오" | Query->Retrieve->Rerank->Evaluate 전체 흐름 | Naive RAG 대비 품질·비용 비교 |
| 요구사항 명시형 | "기업 RAG 설계 방안을 제시하시오" | Hybrid Search·Reranker·Evaluator 선택 기준 | SLA·비용·품질 지표 기반 적용 방안 |

> 요약: 설명형은 고도화 단계 전체, 설계형은 SLA와 품질 지표에 맞춘 모듈 선택을 중심으로 작성함.
