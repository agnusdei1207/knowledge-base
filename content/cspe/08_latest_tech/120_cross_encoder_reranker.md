---
title: "Cross-Encoder Reranker (Cross-Encoder Reranker)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 120
extra:
  question_no: "120"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- cross-encoder는 질의와 문서를 함께 입력받아 직접 관련성 점수를 계산하는 reranker 구조임
- bi-encoder보다 느리지만 정밀도가 높아 reranking 단계에서 자주 사용됨
- 전체 코퍼스 검색에는 비효율적이라 top-k 후보 정제에 집중함

## Ⅰ. 개요

- **정의/개념**: cross-encoder reranker는 질의와 문서를 하나의 입력 시퀀스로 함께 인코딩해 두 텍스트 간 상호작용을 직접 반영한 관련성 점수를 계산하는 정밀 재순위화 모델임
- **배경/필요성**: bi-encoder 기반 1차 검색은 속도는 빠르지만 질의와 문서 간 세밀한 토큰 수준 상호작용을 충분히 반영하지 못하므로, 상위 후보를 다시 정밀 평가할 구조가 필요함

## Ⅱ. 특징

- 질의와 문서의 토큰 상호작용을 직접 보기 때문에 관련성 판단 정확도가 높음
- sparse와 dense 검색 후 top-k 정제 단계에서 강력한 성능 향상을 제공함
- 후보마다 질의와 함께 다시 인코딩해야 하므로 latency와 연산 비용이 큼
- 대규모 검색기 자체로는 부적합하고 후처리 계층으로 적합함

## Ⅲ. 종류 및 비교

| 판단 기준 | Bi-encoder Retriever | Cross-Encoder Reranker | Generative Rerank |
|:---|:---|:---|:---|
| 질의-문서 상호작용 | 간접적임 | 직접적임 | 직접적임 |
| 속도 | 높음 | 낮음 | 매우 낮음 |
| 정밀도 | 중간 | 높음 | 높음 |
| 사용 위치 | 1차 검색 | 재순위화 | 특수 후처리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Paired Input Builder | 질의와 후보 문서를 한 입력으로 묶어 상호작용 기반 평가를 가능하게 함 |
| Cross-Encoder Model | 토큰 간 attention을 통해 세밀한 관련성 점수를 산출함 |
| Scoring Head | 각 후보에 단일 relevance score를 부여해 재정렬 기준을 생성함 |
| Batch Inference Policy | 후보 여러 개를 묶어 처리해 높은 비용을 완화함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Paired Input      | ---> | Cross-Encoder     | ---> | Scoring Head      |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Batch Inference   |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질의+후보 페어 생성 | --> | 공동 인코딩 수행  | --> | 관련성 점수 산출 | --> | 상위 문서 재선정 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질의와 후보 페어 생성**: 질의와 각 후보 문서를 쌍으로 묶음
2. **공동 인코딩 수행**: 모델이 토큰 수준 상호작용을 함께 계산함
3. **관련성 점수 산출**: 후보별 정밀한 relevance score를 계산함
4. **상위 문서 재선정**: 점수 기반으로 최종 순위를 다시 정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 후보 문서마다 공동 인코딩이 필요해 응답 시간이 크게 늘어나 실시간 서비스 부담이 커질 수 있음
   - 해결방안: 후보 수를 제한하고 batch inference를 적용하며 rerank latency와 precision gain으로 타당성을 검증함
2. 문제: 문서가 길면 입력 길이 제한 때문에 중요한 후반부 정보가 잘릴 수 있음
   - 해결방안: passage segmentation과 summary rerank를 적용하고 truncation loss rate와 citation accuracy로 정보 손실을 검증함
3. 문제: 높은 정밀도에 기대어 1차 검색 품질을 소홀히 하면 실제 전체 성능이 기대만큼 오르지 않을 수 있음
   - 해결방안: retriever와 reranker를 함께 평가하고 candidate recall과 final faithfulness로 전체 파이프라인을 검증함

## Ⅶ. 적용 사례

- 계약서 검색 RAG가 상위 후보 조항을 다시 정렬하도록 cross-encoder reranker를 적용하며 확인 지표는 precision@3와 answer correctness임
- 의료 문서 QA가 비슷한 표현의 문서를 정밀 구분하도록 cross-encoder reranker를 활용하며 확인 지표는 citation accuracy와 expert preference임
- 고객지원 검색이 해결 절차 후보를 재정렬하도록 cross-encoder reranker를 적용하며 확인 지표는 first-hit relevance와 resolution rate임

## Ⅷ. 결론

cross-encoder reranker는 느리지만 정밀한 후처리 계층으로, 전체 검색기보다 상위 후보군을 얼마나 정확히 걸러내느냐에 가치를 두고 써야 함.
