---
title: "Groundedness (근거성)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 132
extra:
  question_no: "132"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Groundedness는 답변이 외부 근거에 닻을 내리고 있는지를 보는 개념임
- RAG에서는 주로 검색 문맥이나 출처 문서와의 연결성을 의미함
- Faithfulness와 유사하지만 출처 제시와 근거 연결 측면을 더 강조하는 경우가 많음

## Ⅰ. 개요

- **정의/개념**: Groundedness는 생성 답변이 제공된 근거 문서나 검색 문맥에 실제로 연결되어 있으며, 답변의 각 주장에 출처 기반 뒷받침이 존재하는지를 평가하는 특성임
- **배경/필요성**: 기업형 RAG는 답변 자체의 유창함보다 근거 추적 가능성이 더 중요하므로, 출처 연계성과 설명 가능성을 평가하는 기준이 필요함

## Ⅱ. 특징

- 답변의 사실성뿐 아니라 출처 연결성과 설명 가능성을 함께 본다는 점이 특징임
- citation 기반 UX와 결합될 때 사용자 신뢰도를 크게 높일 수 있음
- 규제 산업에서는 감사 추적성과 책임성 확보 수단으로 중요함
- retrieval 품질과 generation 제약이 함께 좋아야 높은 수준을 확보할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Groundedness | Faithfulness | Factuality |
|:---|:---|:---|:---|
| 평가 초점 | 근거 연결성과 추적 가능성 | 문맥 충실성 | 사실 자체의 진위 |
| 출처 제시 연계 | 높음 | 중간 | 낮음 |
| RAG 적합성 | 매우 높음 | 매우 높음 | 중간 |
| 감사 추적 활용성 | 높음 | 중간 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Context | 답변의 기반이 되는 검색 문서로 grounded answer의 직접 근거가 됨 |
| Claim-to-Source Mapping | 답변 문장과 출처 구간을 연결해 어떤 문장이 어디서 왔는지 추적 가능하게 함 |
| Citation Layer | 사용자에게 근거 문서를 노출해 신뢰성과 검증성을 동시에 높임 |
| Audit Trace | 운영 중 문제 답변이 발생했을 때 원문과 검색 경로를 역추적하는 기록 체계임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 문맥 검색      | --> | 답변 생성      | --> | 주장-출처 연결 | --> | 근거성 검증    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **문맥 검색**: 질문에 대응하는 후보 근거 문서를 가져옴
2. **답변 생성**: 검색 문맥 안에서 답변을 작성함
3. **주장과 출처 연결**: 답변 문장별로 근거 구간을 매핑함
4. **근거성 검증**: 근거 없는 문장과 불충분한 citation을 탐지함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 답변에 출처가 붙어 있어도 실제 문장과 근거 구간이 정확히 연결되지 않으면 거짓 신뢰가 생길 수 있음
   - 해결방안: sentence-level citation mapping을 적용하고 citation accuracy와 groundedness score로 검증함
2. 문제: 검색 문맥 자체가 오래되거나 부정확하면 grounded answer처럼 보여도 잘못된 답을 낼 수 있음
   - 해결방안: source freshness 관리와 문서 품질 검증을 병행하고 stale source rate와 expert audit으로 검증함
3. 문제: 긴 문서에서 근거 구간을 너무 넓게 인용하면 사용자가 실제 근거를 확인하기 어려워짐
   - 해결방안: span citation과 evidence highlighting을 적용하고 citation usability와 click validation rate로 검증함

## Ⅶ. 적용 사례

- 법률 문서 RAG에서는 판례와 조문 구간을 답변에 연결하고 확인 지표는 citation accuracy와 groundedness score임
- 의료 문헌 검색에서는 근거 문단을 함께 제시하고 확인 지표는 evidence coverage와 expert trust score임
- 기업 정책 도우미에서는 사규 원문 링크를 노출하고 확인 지표는 audit trace completeness와 CSAT임

## Ⅷ. 결론

Groundedness는 답변이 어디에 근거했는지 끝까지 추적할 수 있게 만드는 신뢰성 속성이므로, claim-to-source mapping과 citation 품질 관리가 핵심임.
