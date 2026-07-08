---
title: "Context Recall 문맥 재현율 (Context Recall)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 131
extra:
  question_no: "131"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Context Recall은 답변에 필요한 문맥을 검색이 얼마나 빠짐없이 가져왔는지 보는 지표임
- 정밀도가 높아도 필요한 핵심 문맥이 누락되면 재현율은 낮을 수 있음
- recall 부족은 정답 누락과 incomplete answer의 주요 원인임

## Ⅰ. 개요

- **정의/개념**: Context Recall은 질문에 올바르게 답하는 데 필요한 핵심 문맥이 검색 결과에 얼마나 포함되었는지를 측정하는 retrieval 완전성 지표임
- **배경/필요성**: RAG는 상위 문맥이 깔끔해도 결정적 근거를 놓치면 답변 정확도가 무너지므로, 누락 없는 검색 성능을 따로 검증해야 함

## Ⅱ. 특징

- 검색의 완전성과 커버리지를 직접 보여줌
- multi-hop 질문이나 복합 질의에서 특히 중요함
- top-k 값, 임베딩 모델, 인덱스 구성의 영향이 크게 나타남
- precision과 함께 봐야 실제 retrieval trade-off를 판단할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Context Recall | Context Precision | MRR |
|:---|:---|:---|:---|
| 평가 초점 | 필요한 문맥 포착률 | 검색 결과 순도 | 첫 정답 순위 |
| 누락 탐지력 | 높음 | 낮음 | 중간 |
| 노이즈 반영 | 낮음 | 높음 | 낮음 |
| multi-hop 적합성 | 높음 | 중간 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Ground Context | 정답에 필요한 핵심 문맥 집합으로 recall 계산의 기준선이 됨 |
| Retriever | 임베딩과 인덱스와 top-k 전략을 통해 실제 후보 문맥을 반환함 |
| Coverage Check | 필요한 문맥이 검색 결과 안에 포함됐는지 판단해 누락 위치를 찾음 |
| Tuning Lever | top-k, hybrid search, query expansion 같은 제어점이 recall 향상에 직접 연결됨 |

```text
+-------------------+      +-------------------+      +-------------------+
| Ground Context    | ---> | Coverage Check    | ---> | Recall Score      |
+-------------------+      +-------------------+      +-------------------+
             ^
             |
+-------------------+      +-------------------+
| Retriever         | ---> | Tuning Lever      |
+-------------------+      +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 필요 문맥 정의 | --> | 후보 문맥 검색 | --> | 포함 여부 판정 | --> | 재현율 계산    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **필요 문맥 정의**: 질문 답변에 필수인 근거 문맥 집합을 정함
2. **후보 문맥 검색**: top-k 결과를 검색기로 수집함
3. **포함 여부 판정**: 필요한 문맥이 결과 안에 존재하는지 대조함
4. **재현율 계산**: 포함된 핵심 문맥 비율을 집계함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 임베딩 모델이 도메인 용어를 잘 반영하지 못하면 핵심 근거 청크가 검색되지 않아 답변 누락이 반복될 수 있음
   - 해결방안: domain embedding과 hybrid search를 도입하고 Context Recall과 miss rate로 검색 완전성을 검증함
2. 문제: top-k 값을 지나치게 작게 두면 필요한 보조 문맥이 빠져 multi-hop 질문에서 오답률이 커질 수 있음
   - 해결방안: top-k와 rerank depth를 함께 조정하고 recall@k와 final answer accuracy로 최적점을 검증함
3. 문제: 문서 분할 기준이 거칠면 핵심 근거가 여러 청크로 찢어져 한 번에 검색되지 않을 수 있음
   - 해결방안: semantic chunking과 overlap tuning을 적용하고 Context Recall과 chunk coverage로 개선 효과를 검증함

## Ⅶ. 적용 사례

- 제품 매뉴얼 QA가 단계별 근거를 빠짐없이 검색하는지 확인하도록 Context Recall을 관리하며 확인 지표는 Context Recall과 answer completeness임
- 특허 검색 RAG가 관련 청구항 누락을 줄이도록 Context Recall을 활용하며 확인 지표는 miss rate와 expert review score임
- 사내 복합 질의 챗봇이 여러 부서 정책을 함께 찾도록 Context Recall을 적용하며 확인 지표는 Context Recall과 retry rate임

## Ⅷ. 결론

Context Recall은 필요한 근거를 빠짐없이 가져왔는지를 보여주는 retrieval 완전성 지표이므로, 도메인 적합 임베딩과 top-k와 청킹 설계가 핵심 제어점임.
