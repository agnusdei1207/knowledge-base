---
title: "Reranker 재순위화 모델 (Neural Reranker)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 119
extra:
  question_no: "119"
  exam_status: "기출"
  exam_history: "136회, 138회"
  exam_note: "전망"
---

## 미리 알고가기

- reranker는 1차 검색 후보를 다시 정밀 평가해 순서를 조정하는 후처리 모델임
- dense, sparse retrieval의 recall은 유지하고 precision을 끌어올리는 역할을 함
- 느리기 때문에 보통 top-k 후보에만 적용함

## Ⅰ. 개요

- **정의/개념**: 재순위화 모델은 1차 검색기가 가져온 후보 문서 집합에 대해 질의-문서 관련성을 더 정밀하게 계산하여 최종 순위를 다시 매기는 후처리 모델임
- **배경/필요성**: 1차 검색기는 속도를 위해 근사 판단을 하므로 관련 없는 문서가 상위에 섞일 수 있어, 생성 전에 정밀한 재평가 단계가 필요함

## Ⅱ. 특징

- retrieval recall을 유지하면서 최종 context precision을 크게 높일 수 있음
- 질의와 문서를 함께 보는 정밀 모델을 사용해 미묘한 관련성 차이를 구분함
- 연산 비용이 커서 대량 후보 전체에 적용하기에는 비효율적임
- reranker 품질이 좋아도 1차 검색 후보에 정답이 없으면 회복할 수 없음

## Ⅲ. 종류 및 비교

| 판단 기준 | 1차 Retriever | Neural Reranker | Cross-Encoder |
|:---|:---|:---|:---|
| 역할 | 후보 회수 | 후보 재정렬 | 대표적 reranker 구조 |
| 속도 | 높음 | 중간 | 낮음 |
| 정밀도 | 중간 | 높음 | 매우 높음 |
| 사용 범위 | 전체 코퍼스 | top-k 후보 | top-k 후보 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Candidate Set | 1차 검색기가 가져온 후보 문서 집합으로 reranker의 입력 범위를 제한함 |
| Query-Document Encoder | 질의와 문서를 함께 보거나 상호작용시키며 정밀 관련성 점수를 계산함 |
| Ranking Score | 최종 정렬 기준이 되는 점수로 생성 단계에 들어갈 문서를 선별함 |
| Serving Policy | top-k 크기와 동시성 정책을 정해 latency와 품질의 타협점을 관리함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Candidate Set     | ---> | Query-Doc Encoder | ---> | Ranking Score     |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Serving Policy    |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 1차 후보 수집    | --> | 질의-문서 정밀 평가 | --> | 재순위 점수 산출 | --> | 상위 문서 선택   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **1차 후보 수집**: sparse나 dense retriever가 상위 후보를 가져옴
2. **질의-문서 정밀 평가**: reranker가 후보 각각을 더 정교하게 평가함
3. **재순위 점수 산출**: 관련성 점수로 최종 순서를 다시 계산함
4. **상위 문서 선택**: 생성 단계에 넣을 소수의 핵심 문서를 결정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: reranker는 정밀하지만 느려서 후보 수가 많아지면 전체 응답 시간이 크게 증가할 수 있음
   - 해결방안: top-k 크기를 제한하고 batch inference를 적용하며 rerank latency와 answer gain으로 효율을 검증함
2. 문제: 1차 검색 후보 품질이 낮으면 reranker가 선택할 수 있는 범위 자체가 잘못되어 성능 상한이 낮아질 수 있음
   - 해결방안: hybrid retrieval과 함께 운영하고 candidate recall과 final faithfulness로 전단 검색 품질을 검증함
3. 문제: reranker가 특정 문체나 길이를 과도하게 선호하면 문서 다양성이 떨어질 수 있음
   - 해결방안: gold set과 편향 평가를 운영하고 ranking bias metric과 user satisfaction으로 정렬 품질을 검증함

## Ⅶ. 적용 사례

- 엔터프라이즈 RAG가 검색 후보를 다시 정렬해 근거 품질을 높이도록 reranker를 적용하며 확인 지표는 context precision과 faithfulness임
- 법률 QA가 미묘한 조항 차이를 반영해 순위를 조정하도록 reranker를 활용하며 확인 지표는 precision@k와 citation accuracy임
- 고객지원 검색이 긴 매뉴얼 중 정확한 해결 절차를 상위로 올리도록 reranker를 적용하며 확인 지표는 first-hit relevance와 resolution rate임

## Ⅷ. 결론

재순위화 모델은 검색 성능의 마지막 정밀 조정 계층이므로, 1차 검색의 recall과 reranker의 precision을 분리 설계해야 효과가 가장 큼.
