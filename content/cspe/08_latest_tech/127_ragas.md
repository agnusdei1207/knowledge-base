---
title: "RAGAS (RAGAS)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 127
extra:
  question_no: "127"
  exam_status: "기출"
  exam_history: "136회, 138회"
  exam_note: "전망"
---

## 미리 알고가기

- RAGAS는 RAG 평가 자동화를 위한 대표 오픈소스 프레임워크임
- Ground Truth가 부족한 상황에서도 LLM judge 기반 지표를 계산할 수 있음
- Faithfulness, Answer Relevancy, Context Precision, Context Recall이 핵심 지표군임

## Ⅰ. 개요

- **정의/개념**: RAGAS는 RAG 시스템의 검색 결과와 생성 답변을 LLM 기반 지표로 자동 평가해 검색 품질과 환각 위험을 수치화하는 평가 프레임워크임
- **배경/필요성**: 운영 RAG는 매번 사람 손으로 채점하기 어렵기 때문에, 반복 가능한 자동 지표와 배치 평가 체계가 필요함

## Ⅱ. 특징

- Ground Truth 의존도를 낮춰 초기 RAG 도입 단계에서도 적용하기 쉬움
- 지표별 계산 함수가 분리되어 실험 자동화와 CI 연계가 용이함
- 문맥 적합성과 답변 충실성을 동시에 다뤄 원인 분석이 가능함
- LangChain, LlamaIndex 등 RAG 생태계와 쉽게 결합할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | RAGAS | 수동 평가 | 전통 NLP 지표 |
|:---|:---|:---|:---|
| 자동화 수준 | 높음 | 낮음 | 높음 |
| RAG 특화성 | 높음 | 높음 | 낮음 |
| 비용 효율 | 중간 | 낮음 | 높음 |
| 환각 진단력 | 높음 | 높음 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Metric Module | Faithfulness와 Context Metric 같은 지표를 모듈로 제공해 실험 목적에 따라 조합할 수 있음 |
| LLM Judge | 문맥과 답변을 해석해 의미 기반 판정을 수행하며 judge 모델 품질이 전체 신뢰도에 영향을 줌 |
| Dataset Interface | 질문과 정답과 문맥을 구조화해 배치 평가와 반복 실험을 가능하게 함 |
| Reporting Layer | 실행 결과를 점수와 실패 사례로 묶어 프롬프트, 임베딩, 리랭커 개선에 직접 연결함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 평가셋 구성   | --> | 지표 함수 선택 | --> | LLM 판정 실행 | --> | 결과 집계/비교 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **평가셋 구성**: 질문, 생성 답변, 검색 문맥, 필요 시 기준 답을 준비함
2. **지표 함수 선택**: 목적에 맞는 faithfulness, relevancy, context metric을 지정함
3. **LLM 판정 실행**: 각 샘플을 의미 기반으로 채점해 지표 값을 계산함
4. **결과 집계 및 비교**: 모델 버전별 점수를 비교해 튜닝 방향을 결정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: judge 모델의 편향과 프롬프트 차이로 같은 답변도 평가 결과가 흔들릴 수 있음
   - 해결방안: judge 모델과 프롬프트를 고정 버전으로 관리하고 repeatability score와 human agreement로 안정성을 검증함
2. 문제: 평가 호출량이 늘어나면 비용과 지연이 커져 실험 속도가 느려질 수 있음
   - 해결방안: 샘플링 평가와 캐시 전략을 적용하고 evaluation cost와 batch latency로 효율을 검증함
3. 문제: 지표 해석 없이 숫자만 비교하면 실제 서비스 개선과 연결되지 않을 수 있음
   - 해결방안: low-score 사례를 오류 유형별로 분류하고 failure taxonomy와 fix success rate로 개선 효과를 검증함

## Ⅶ. 적용 사례

- RAG 실험 자동화에서는 프롬프트 버전별 성능을 일괄 비교하고 확인 지표는 Faithfulness와 Answer Relevancy임
- 엔터프라이즈 검색 QA에서는 임베딩 모델 교체 전후를 검증하고 확인 지표는 Context Recall과 retrieval cost임
- CI 품질 게이트에서는 배포 전 평가 임계치를 검사하고 확인 지표는 pass rate와 regression count임

## Ⅷ. 결론

RAGAS는 RAG 품질을 사람 감각이 아니라 재현 가능한 지표로 운영하게 만드는 프레임워크이므로, judge 안정성과 대표 데이터셋 설계가 도입 성패를 좌우함.
