---
title: "Bi-Encoder 검색모델 (Bi-Encoder)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 121
extra:
  question_no: "121"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- bi-encoder는 질의와 문서를 각각 독립적으로 임베딩하는 검색 구조임
- 대규모 검색에 유리해 dense retrieval의 대표 구조로 널리 쓰임
- cross-encoder보다 빠르지만 상호작용 정보는 제한적임

## Ⅰ. 개요

- **정의/개념**: bi-encoder는 질의와 문서를 각각 별도로 인코딩해 두 벡터의 유사도로 관련성을 판단하는 검색 모델 구조로, 대규모 dense retrieval의 기본 아키텍처임
- **배경/필요성**: 전체 문서 집합을 매번 질의와 함께 공동 인코딩하는 것은 비효율적이므로, 문서를 미리 벡터화해 빠른 nearest neighbor 검색을 수행할 구조가 필요함

## Ⅱ. 특징

- 문서 임베딩을 사전 계산할 수 있어 대규모 검색 속도가 매우 빠름
- semantic search와 RAG의 1차 retriever로 사용하기 적합함
- 질의와 문서의 세밀한 토큰 상호작용을 직접 보지 못해 정밀도 한계가 있음
- 일반적으로 reranker와 결합해 recall과 precision을 분리 설계함

## Ⅲ. 종류 및 비교

| 판단 기준 | Bi-Encoder | Cross-Encoder | Sparse Retrieval |
|:---|:---|:---|:---|
| 대규모 검색 속도 | 높음 | 낮음 | 높음 |
| semantic match | 높음 | 높음 | 낮음 |
| token 상호작용 | 약함 | 강함 | 없음 |
| 대표 역할 | 1차 dense retrieval | rerank | exact match retrieval |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Query Encoder | 질의를 벡터로 변환해 검색 시점의 표현을 생성함 |
| Document Encoder | 문서를 벡터화해 사전 색인 가능한 검색 표현을 만듦 |
| Vector Index | 문서 벡터를 저장해 빠른 nearest neighbor 탐색을 가능하게 함 |
| Similarity Scorer | 질의 벡터와 문서 벡터의 cosine이나 dot score로 관련성을 계산함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Query Encoder     | ---> | Similarity Score  | ---> | Top-k Candidates  |
+-------------------+      +-------------------+      +-------------------+
             ^
             |
+-------------------+      +-------------------+
| Document Encoder  | ---> | Vector Index      |
+-------------------+      +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질의/문서 독립 인코딩 | --> | 문서 벡터 사전 저장 | --> | 질의 벡터 검색   | --> | 상위 후보 반환   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질의 및 문서 독립 인코딩**: 같은 구조의 encoder가 질의와 문서를 각각 벡터화함
2. **문서 벡터 사전 저장**: 문서 벡터를 벡터 인덱스에 미리 저장함
3. **질의 벡터 검색**: 질의 벡터로 가까운 문서 벡터를 탐색함
4. **상위 후보 반환**: 상위 후보를 rerank나 생성 단계로 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 질의와 문서를 독립 인코딩하므로 세밀한 토큰 대응 관계를 놓쳐 비슷하지만 핵심이 다른 문서를 올릴 수 있음
   - 해결방안: reranker를 후단에 두고 candidate recall과 final precision으로 정밀도 보완 효과를 검증함
2. 문제: 임베딩 모델이 일반 도메인 기준이면 전문 도메인 질의에서 검색 품질이 낮아질 수 있음
   - 해결방안: 도메인 대조학습을 적용하고 recall@k와 domain retrieval benchmark로 성능을 검증함
3. 문제: 임베딩 버전이 바뀌면 전체 문서 벡터를 재색인해야 해 운영 전환 비용이 커질 수 있음
   - 해결방안: embedding versioning과 staged reindex를 운영하고 reindex time과 migration gap으로 전환 부담을 검증함

## Ⅶ. 적용 사례

- 엔터프라이즈 RAG 1차 검색이 대량 문서 후보를 빠르게 모으도록 bi-encoder를 적용하며 확인 지표는 recall@k와 query latency임
- 의미 검색 포털이 자연어 질의 기반 문서 탐색을 수행하도록 bi-encoder를 활용하며 확인 지표는 click satisfaction과 retrieval quality임
- 추천 후보 생성이 사용자와 콘텐츠 유사도를 계산하도록 bi-encoder를 적용하며 확인 지표는 CTR와 candidate coverage임

## Ⅷ. 결론

bi-encoder는 대규모 검색을 가능하게 하는 속도 중심 구조이므로, 정밀도 한계를 인정하고 reranker와 역할을 분리할 때 가장 효과적임.
