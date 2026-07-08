---
title: "Context Precision (문맥 정밀도)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 130
extra:
  question_no: "130"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Context Precision은 검색된 문맥 중 실제로 유용한 문맥 비율을 보는 retrieval 지표임
- 불필요한 문맥이 많으면 모델이 노이즈에 흔들리기 쉬움
- 리랭커와 청킹 품질을 점검하는 데 적합함

## Ⅰ. 개요

- **정의/개념**: Context Precision은 RAG가 상위로 가져온 문맥 가운데 질문 해결에 실제로 도움이 되는 관련 문맥의 비율을 측정하는 검색 품질 지표임
- **배경/필요성**: 관련 문서를 찾았더라도 상위 순위에 잡음 문맥이 많이 섞이면 LLM이 핵심 근거를 놓치므로 문맥의 순도 관리가 필요함

## Ⅱ. 특징

- top-k 결과의 순도와 상위 랭킹 품질을 직접 보여줌
- 관련 문서가 일부 포함돼도 불필요 문맥이 많으면 낮은 점수를 받음
- 청크 크기, 메타데이터 필터, 리랭커 성능 차이를 민감하게 반영함
- answer quality 저하 원인을 retrieval noise 관점에서 설명할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Context Precision | Context Recall | Recall@k |
|:---|:---|:---|:---|
| 평가 초점 | 검색 결과의 순도 | 필요한 문맥의 포착률 | 관련 문서 포함 여부 |
| 노이즈 민감도 | 높음 | 낮음 | 중간 |
| 상위 랭킹 품질 반영 | 높음 | 중간 | 낮음 |
| 리랭커 평가 적합성 | 매우 높음 | 중간 | 중간 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Query | 질문 의도가 명확해야 관련 문맥 판단 기준이 흔들리지 않음 |
| Retrieved Context | top-k 청크 집합으로 precision 계산의 직접 대상이 되며 순서 품질이 중요함 |
| Relevance Judgement | 각 청크가 질문 해결에 실제로 필요한지 판정해 노이즈 비율을 계산함 |
| Ranking Strategy | 리랭커와 필터와 chunking 설정이 precision 값을 결정하는 핵심 제어점임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질문 입력      | --> | top-k 문맥 검색 | --> | 관련성 판정    | --> | 정밀도 계산    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질문 입력**: 검색 대상이 되는 질의를 정의함
2. **top-k 문맥 검색**: 상위 문맥 후보를 순위와 함께 수집함
3. **관련성 판정**: 각 문맥이 질문에 실질적으로 필요한지 평가함
4. **정밀도 계산**: 관련 문맥 비율을 계산해 노이즈 수준을 파악함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 상위 검색 결과에 주변 주제 청크가 많이 섞이면 모델이 핵심 근거 대신 노이즈를 읽어 답변 품질이 떨어질 수 있음
   - 해결방안: cross-encoder reranker와 metadata filter를 적용하고 Context Precision과 rerank lift로 개선 효과를 검증함
2. 문제: 청크가 지나치게 작으면 부분 일치 청크가 많이 검색되어 의미 없는 top-k 결과가 늘어날 수 있음
   - 해결방안: chunk size와 overlap을 조정하고 precision@k와 answer faithfulness로 적정 구성을 검증함
3. 문제: 질의 해석이 모호하면 검색기는 넓은 문맥을 반환해 precision 저하가 반복될 수 있음
   - 해결방안: query rewriting과 intent classification을 적용하고 query ambiguity reduction과 Context Precision으로 검증함

## Ⅶ. 적용 사례

- 법규 검색 RAG에서는 관련 조항만 상위에 올리는지 확인하고 확인 지표는 Context Precision과 top-3 hit purity임
- 기술 문서 QA에서는 리랭커 도입 전후를 평가하고 확인 지표는 precision@k와 answer latency임
- 사내 위키 검색에서는 부서별 메타데이터 필터 성능을 확인하고 확인 지표는 Context Precision과 click-through rate임

## Ⅷ. 결론

Context Precision은 검색 결과가 얼마나 깨끗하게 핵심 문맥만 상위에 올랐는지를 보여주므로, 리랭킹과 필터링과 청킹 전략의 품질 판단에 가장 직접적인 retrieval 지표임.
