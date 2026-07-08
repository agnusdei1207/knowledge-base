---
title: "Dense Retrieval 밀집 검색 (Dense Retrieval)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 113
extra:
  question_no: "113"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- dense retrieval은 질의와 문서를 임베딩 벡터로 변환해 의미 공간에서 검색하는 방식임
- sparse retrieval보다 semantic match에 강하지만 exact code 검색에는 약할 수 있음
- 벡터 인덱스와 임베딩 모델 품질이 전체 성능을 좌우함

## Ⅰ. 개요

- **정의/개념**: 밀집 검색은 질의와 문서를 연속적인 고차원 임베딩 벡터로 표현하고, 벡터 공간에서 가까운 항목을 찾아 의미 기반 관련 문서를 검색하는 방식임
- **배경/필요성**: 키워드 일치가 없어도 같은 의미를 가진 문서를 찾아야 하는 자연어 검색과 RAG 환경에서 sparse 검색만으로는 충분한 recall을 확보하기 어려움

## Ⅱ. 특징

- 자연어 질문과 동의어와 긴 문장 표현을 잘 처리해 semantic recall이 높음
- RAG의 기본 retriever로 널리 사용되며 사용자 질의 의도 파악에 유리함
- 임베딩 모델이 도메인에 맞지 않으면 의미 검색이 쉽게 실패할 수 있음
- exact identifier 검색에는 약해 sparse 검색과 병행하는 경우가 많음

## Ⅲ. 종류 및 비교

| 판단 기준 | Sparse Retrieval | Dense Retrieval | Cross-Encoder Rerank |
|:---|:---|:---|:---|
| semantic recall | 낮음 | 높음 | 매우 높음 |
| exact match | 높음 | 낮음 | 중간 |
| 검색 속도 | 높음 | 높음 | 낮음 |
| 사용 위치 | 1차 검색 | 1차 검색 | 후처리 재정렬 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Bi-encoder Model | 질의와 문서를 각각 임베딩해 대규모 검색이 가능한 표현을 만듦 |
| Vector Store | 문서 임베딩을 저장하고 ANN 검색을 수행함 |
| Similarity Function | cosine이나 dot product가 가까운 문서를 선택하는 기준이 됨 |
| Metadata, Rerank Layer | 필터링과 후처리 재정렬로 dense retrieval의 약점을 보완함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Bi-encoder Model  | ---> | Vector Store      | ---> | Similarity Fn.    |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Meta / Rerank     |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질의/문서 임베딩 | --> | 벡터 인덱스 저장  | --> | ANN 유사도 검색  | --> | 후보 후처리 반환 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질의 및 문서 임베딩**: bi-encoder가 텍스트를 벡터로 변환함
2. **벡터 인덱스 저장**: 문서 임베딩을 ANN 구조에 저장함
3. **ANN 유사도 검색**: 의미적으로 가까운 후보 문서를 탐색함
4. **후처리 반환**: 필터링이나 reranking 후 최종 문서를 반환함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 임베딩 모델이 도메인 용어나 숫자 식별자 표현을 잘 반영하지 못하면 핵심 문서를 놓칠 수 있음
   - 해결방안: 도메인 맞춤 임베딩이나 hybrid search를 적용하고 retrieval recall과 exact hit rate로 보완 효과를 검증함
2. 문제: 벡터 검색은 이유 설명이 어렵고 후보가 왜 선택됐는지 해석이 제한될 수 있음
   - 해결방안: sparse 근거와 citation을 함께 제공하고 explainability score와 user trust로 해석 가능성을 검증함
3. 문제: 대규모 벡터 인덱스 운영 시 메모리와 갱신 비용이 커져 운영비가 증가할 수 있음
   - 해결방안: ANN 인덱스와 갱신 정책을 최적화하고 indexing lag와 cost per query로 운영 효율을 검증함

## Ⅶ. 적용 사례

- 자연어 RAG 검색이 의미 기반으로 관련 문서를 찾도록 밀집 검색을 적용하며 확인 지표는 recall@k와 faithfulness임
- 고객지원 검색이 다양한 표현의 문의를 매칭하도록 밀집 검색을 활용하며 확인 지표는 resolution rate와 answer relevance임
- 기업 지식 탐색이 방대한 문서에서 의미 근접 자료를 수집하도록 밀집 검색을 적용하며 확인 지표는 click satisfaction과 search quality임

## Ⅷ. 결론

밀집 검색은 자연어형 의미 매칭의 핵심 수단이지만, 임베딩 품질과 exact match 약점을 이해하고 sparse 검색 및 rerank 계층과 함께 써야 실무 성능이 안정적임.
