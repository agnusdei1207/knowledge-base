---
title: "ColBERT (후기상호작용 검색)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 122
extra:
  question_no: "122"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- ColBERT는 bi-encoder와 cross-encoder 사이의 절충 구조로 late interaction을 사용함
- 문서 토큰 벡터를 보존하면서 질의 토큰과의 max-sim을 활용하는 것이 핵심임
- dense retrieval보다 정밀도가 높고 cross-encoder보다 빠른 중간 지점을 노림

## Ⅰ. 개요

- **정의/개념**: ColBERT는 질의와 문서를 각각 인코딩하되 문서를 단일 벡터로 압축하지 않고 토큰 수준 벡터를 유지한 채, 검색 시 late interaction으로 관련성을 계산하는 고정밀 dense retrieval 구조임
- **배경/필요성**: bi-encoder는 빠르지만 토큰 정보가 많이 사라지고 cross-encoder는 정확하지만 느리므로, 두 방식 사이의 균형을 잡는 검색 구조가 필요함

## Ⅱ. 특징

- 문서 토큰 수준 정보를 유지해 bi-encoder보다 정밀한 검색이 가능함
- 문서는 미리 인덱싱할 수 있어 cross-encoder보다 훨씬 빠른 검색이 가능함
- 토큰 단위 벡터 저장으로 메모리와 인덱스 크기가 커질 수 있음
- late interaction 계산 비용이 있어 단순 bi-encoder보다 운영이 무거움

## Ⅲ. 종류 및 비교

| 판단 기준 | Bi-Encoder | ColBERT | Cross-Encoder |
|:---|:---|:---|:---|
| 검색 속도 | 높음 | 중간 | 낮음 |
| 정밀도 | 중간 | 높음 | 매우 높음 |
| 문서 표현 | 단일 벡터 | 토큰 벡터 집합 | 질의와 공동 인코딩 |
| 인덱스 크기 | 작음 | 큼 | 해당 없음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Query Token Encoder | 질의를 토큰 수준 벡터로 변환해 세밀한 의미 비교를 가능하게 함 |
| Document Token Index | 문서의 각 토큰 벡터를 저장해 late interaction 계산의 기반을 만듦 |
| Late Interaction Scorer | 질의 토큰별로 가장 유사한 문서 토큰을 찾아 관련성 점수를 합산함 |
| ANN Storage Optimization | 큰 인덱스를 다루기 위해 압축과 효율적 저장 전략이 필요함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질의/문서 토큰 인코딩 | --> | 문서 토큰 인덱싱  | --> | late interaction 계산 | --> | 상위 문서 반환   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질의 및 문서 토큰 인코딩**: 토큰 수준 벡터를 생성함
2. **문서 토큰 인덱싱**: 문서 토큰 벡터를 저장하고 검색 가능하게 만듦
3. **late interaction 계산**: 질의 토큰과 가장 가까운 문서 토큰 간 유사도를 계산함
4. **상위 문서 반환**: 합산 점수로 최종 관련 문서를 선택함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 토큰 수준 문서 표현을 저장해야 해 인덱스 크기와 메모리 비용이 크게 증가할 수 있음
   - 해결방안: 차원 축소와 압축 저장을 적용하고 index size와 recall@k로 비용 대비 성능을 검증함
2. 문제: late interaction 계산이 bi-encoder보다 무거워 대규모 트래픽 환경에서 latency가 증가할 수 있음
   - 해결방안: 후보 제한과 하드웨어 최적화를 적용하고 p95 latency와 retrieval gain으로 도입 타당성을 검증함
3. 문제: 구조가 복잡해지면 운영 난도와 디버깅 비용이 커질 수 있음
   - 해결방안: baseline retriever와 A/B 평가를 유지하고 MTTR와 search quality uplift로 운영 가치를 검증함

## Ⅶ. 적용 사례

- 고정밀 엔터프라이즈 검색: 유사한 문서 간 미세 차이를 구분함, 확인 지표는 precision@k와 user satisfaction임
- RAG retriever 고도화: dense recall과 rerank 중간 계층으로 사용함, 확인 지표는 faithfulness와 retrieval quality임
- 연구 검색 시스템: 긴 질의와 전문 용어 질의를 처리함, 확인 지표는 MRR와 answer relevance임

## Ⅷ. 결론

ColBERT는 속도와 정밀도 사이의 절충 구조로, bi-encoder만으로는 부족하고 cross-encoder는 너무 비싼 구간에서 특히 가치가 큼.
