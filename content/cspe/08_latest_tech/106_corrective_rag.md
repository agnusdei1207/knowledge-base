---
title: "Corrective RAG (교정형 RAG)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 106
extra:
  question_no: "106"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Corrective RAG는 검색 결과를 그대로 쓰지 않고 평가와 교정 단계를 거치는 구조임
- 검색 실패를 탐지해 fallback 검색이나 문맥 정제를 수행하는 것이 핵심임
- 평가기 품질이 전체 파이프라인 신뢰도를 크게 좌우함

## Ⅰ. 개요

- **정의/개념**: Corrective RAG는 검색된 문서의 적절성을 별도 평가기로 판단하고, 결과에 따라 문서를 정제하거나 대체 검색을 수행한 뒤 생성 단계로 넘기는 교정 중심 RAG 아키텍처임
- **배경/필요성**: 기본 RAG는 잘못 검색된 문서도 그대로 근거로 사용해 더 그럴듯한 오답을 만들 수 있으므로, 생성 이전에 검색 품질을 교정하는 안전 장치가 필요함

## Ⅱ. 특징

- retrieval failure를 생성 단계 이전에 탐지해 환각 확산을 줄일 수 있음
- 부정확한 내부 검색 결과를 외부 검색이나 다른 데이터 소스로 보완하는 fallback 구조를 만들 수 있음
- 평가기와 교정 단계가 추가되어 latency와 운영 복잡도가 증가함
- 문서 평가 품질이 낮으면 오히려 정답 문서를 버리거나 불필요한 fallback을 유발할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Naive RAG | Advanced RAG | Corrective RAG |
|:---|:---|:---|:---|
| 검색 결과 검증 | 없음 | 제한적임 | 있음 |
| fallback 검색 | 없음 | 선택적임 | 핵심 요소 |
| latency | 낮음 | 중간 | 높음 |
| 환각 방어 | 낮음 | 중간 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Primary Retriever | 기본 문서 후보를 가져오는 1차 검색 경로를 담당함 |
| Relevance Evaluator | 검색된 문서가 질의에 답하기에 충분한지 평가해 교정 여부를 결정함 |
| Correction Path | refinement, fallback web search, alternate retriever로 검색 공백을 보완함 |
| Generator | 교정된 문맥만 사용해 최종 답변을 생성함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 1차 문서 검색   | --> | 관련성 평가      | --> | 교정/대체 검색   | --> | 교정 근거 기반 생성 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **1차 문서 검색**: 기본 retriever가 관련 후보 문서를 수집함
2. **관련성 평가**: 평가기가 문서가 질문을 충분히 뒷받침하는지 판정함
3. **교정 및 대체 검색**: 부족한 경우 문서 정제나 다른 검색 경로를 수행함
4. **교정 근거 기반 생성**: 정제된 문맥으로 답변을 생성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: evaluator가 부정확하면 정답 문서를 버리거나 오답 문서를 살려 전체 성능이 더 나빠질 수 있음
   - 해결방안: 도메인 평가셋으로 evaluator를 검증하고 evaluator F1과 final faithfulness로 판정 품질을 검증함
2. 문제: 교정과 fallback 단계를 추가하면 응답 시간이 늘어나 실시간 서비스 SLA를 넘길 수 있음
   - 해결방안: confidence threshold와 fallback 조건을 엄격히 설정하고 correction trigger rate와 p95 latency로 비용 대비 효과를 검증함
3. 문제: 외부 fallback 검색을 허용하면 보안과 신뢰되지 않은 정보 유입 위험이 커질 수 있음
   - 해결방안: 신뢰 소스 allowlist와 내부 fallback 경로를 운영하고 external source violation rate와 citation trust score로 안전성을 검증함

## Ⅶ. 적용 사례

- 고객지원 지식봇: 내부 매뉴얼 부족 시 공식 웹 FAQ로 보완함, 확인 지표는 fallback success rate와 hallucination rate임
- 규정 문서 QA: 오래된 문서 검색 실패를 교정함, 확인 지표는 faithfulness와 outdated answer rate임
- 폐쇄망 엔터프라이즈 챗봇: 외부 웹 대신 내부 API fallback을 사용함, 확인 지표는 correction accuracy와 response latency임

## Ⅷ. 결론

Corrective RAG는 검색 결과를 의심하고 교정하는 방어형 RAG이므로, retriever보다 evaluator와 fallback 설계가 신뢰성의 핵심이 됨.
