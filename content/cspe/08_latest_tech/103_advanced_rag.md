---
title: "Advanced RAG (고도화 RAG)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 103
extra:
  question_no: "103"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Advanced RAG는 기본 RAG의 검색 실패와 노이즈 문제를 줄이기 위해 전후처리 모듈을 추가한 구조임
- query rewrite, hybrid search, reranking, context compression이 대표 요소임
- 정확도는 좋아지지만 latency와 운영 복잡도도 같이 증가함

## Ⅰ. 개요

- **정의/개념**: Advanced RAG는 기본 RAG 파이프라인에 질의 최적화와 다중 검색과 재순위화와 컨텍스트 압축을 추가해 검색 정확도와 근거 품질을 높인 상용형 검색-생성 아키텍처임
- **배경/필요성**: 기본 RAG는 모호한 질의와 고유명사와 장문 문서에서 검색 실패가 잦아 실제 서비스 정확도를 안정적으로 유지하기 어려우므로, 검색 품질 제어 계층이 필요함

## Ⅱ. 특징

- 검색 전, 검색 중, 검색 후 단계별 품질 제어가 가능해 응답 신뢰도를 높임
- hybrid retrieval과 reranking으로 recall과 precision을 동시에 개선할 수 있음
- 모듈이 많아질수록 latency와 비용과 장애 지점이 함께 늘어남
- 서비스 목적에 맞는 최소 모듈 조합을 찾는 엔지니어링이 중요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Naive RAG | Advanced RAG | Agentic RAG |
|:---|:---|:---|:---|
| 검색 제어 수준 | 낮음 | 높음 | 매우 높음 |
| 파이프라인 유연성 | 낮음 | 중간 | 높음 |
| 응답 지연 | 낮음 | 중간 | 높음 |
| 대표 적합도 | 단순 QA | 상용 지식 서비스 | 복합 다단계 질의 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Query Optimizer | 질의를 재작성하거나 확장해 검색기의 hit quality를 높임 |
| Hybrid Retriever | sparse와 dense 검색을 결합해 exact match와 semantic match를 함께 확보함 |
| Reranker | 후보 문서를 다시 채점해 최종 컨텍스트의 정밀도를 높임 |
| Context Compressor | 최종 문서 길이를 줄여 비용과 lost-in-the-middle 문제를 완화함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질의 최적화    | --> | 하이브리드 검색  | --> | 재순위화/압축   | --> | 근거 기반 생성   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질의 최적화**: 모호한 질문을 검색 친화적인 형태로 보정함
2. **하이브리드 검색**: dense와 sparse 경로를 함께 사용해 후보 문서를 모음
3. **재순위화 및 압축**: 관련도가 높은 문서를 골라 핵심 문장만 남김
4. **근거 기반 생성**: 정제된 컨텍스트로 모델이 답변을 생성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 모듈을 많이 붙일수록 latency와 API 호출 비용이 커져 서비스 SLA를 넘길 수 있음
   - 해결방안: 필수 모듈만 남기는 profiling을 수행하고 end-to-end latency와 cost per answer로 조합 효율을 검증함
2. 문제: 각 단계의 파라미터가 얽혀 있어 한 단계 최적화가 전체 품질을 보장하지 않을 수 있음
   - 해결방안: retrieval, reranking, answer 단계 지표를 분리 측정하고 context precision과 faithfulness로 병목을 검증함
3. 문제: 복잡한 파이프라인은 장애 지점과 운영 부담을 늘려 유지보수가 어려워질 수 있음
   - 해결방안: 단계별 fallback과 observability를 도입하고 stage failure rate와 MTTR로 운영성을 검증함

## Ⅶ. 적용 사례

- 계약서 분석 서비스: hybrid search와 reranker를 적용함, 확인 지표는 precision@k와 hallucination rate임
- 고객지원 지식봇: query rewrite로 질의 품질을 보완함, 확인 지표는 answer relevance와 first-response resolution rate임
- 금융 컴플라이언스 QA: context compression으로 근거만 추출함, 확인 지표는 citation accuracy와 latency임

## Ⅷ. 결론

Advanced RAG는 기본 RAG의 약점을 실무 수준으로 보완하는 구조이므로, 품질 모듈을 많이 넣는 것보다 서비스 목적에 맞는 최소 유효 조합을 설계하는 것이 중요함.
