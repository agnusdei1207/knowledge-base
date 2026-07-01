---
title: "문맥 재현율 (Context Recall)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 131
---

# 📖 【암기용】 개념 완전 이해

> 목적: Context Recall을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 정답 생성에 필요한 근거가 검색 컨텍스트에 얼마나 빠짐없이 포함되었는지 측정하는 지표
- **왜 필요한가**: 아무리 LLM이 좋아도 필요한 근거를 검색하지 못하면 정확한 답변을 만들 수 없음.
- **핵심 직관**: 답안을 쓰는 데 필요한 참고자료를 빠뜨리지 않고 찾았는지 보는 채점임.

## 깊이 이해
- **배경·문제의식**: Context Precision은 상위 결과가 관련 있는지 보지만, 필요한 근거 전체를 다 찾았는지는 별도 지표가 필요하다.
- **작동 원리**: 정답 근거 문장 또는 gold context를 기준으로, 검색된 컨텍스트가 필요한 근거를 얼마나 포함하는지 LLM Judge나 라벨로 평가함.
- **비유**: 시험에 필요한 참고 페이지 5개 중 4개를 찾았으면 재현율 80%이고, 1개를 놓치면 답안 일부가 빈다.
- **구체 예시**: Context Recall 0.85 미만이면 Top-K 확대, Hybrid Search, Query Rewrite로 검색 누락을 줄임.
- **흔한 오해·주의점**: Recall만 높이려고 Top-K를 크게 하면 무관 문서가 섞인다. Context Precision과 함께 관리해야 함.

## 연결 개념
- Context Precision — 상위 검색 결과의 관련성 지표
- Hybrid Search — 검색 누락을 줄이는 Sparse+Dense 결합
- Query Rewrite — 질의 표현을 보정해 필요한 근거를 찾는 방법

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Context Recall은 정답에 필요한 근거가 검색 컨텍스트에 포함된 비율을 측정함.
> 2. **가치**: 검색 누락을 탐지해 LLM 생성 이전의 답변 한계를 확인함.
> 3. **판단 포인트**: Recall을 높이면 무관 문서가 늘 수 있으므로 Precision과 Top-K를 함께 조정함.

## Ⅰ. 개요 및 필요성

Context Recall은 검색 근거 재현율 지표임. RAG 답변 품질은 필요한 근거를 검색했는지에 의해 제한된다. 검색 누락이 있으면 LLM은 정답을 생성하기 어렵기 때문에 검색 단계 품질을 별도로 측정한다.

## Ⅱ. 구조 및 구성요소

```text
Question + Gold Evidence → Retrieved Contexts
  → Evidence Coverage Judge → Context Recall Score
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Gold Evidence | 정답에 필요한 근거 | 문장·청크·문서 단위 |
| Retrieved Contexts | RAG 검색 결과 | Top-K contexts |
| Coverage Judge | 근거 포함 여부 판정 | 라벨 또는 LLM Judge |
| Recall Calculator | 포함 근거 비율 계산 | covered / required |

> 요약: Context Recall은 필요한 gold evidence가 검색 컨텍스트에 포함됐는지 커버리지 관점으로 계산함.

## Ⅲ. 동작원리 및 흐름도

```text
평가 질의 실행 → Top-K 컨텍스트 수집
  → gold evidence와 매칭 → 포함/누락 판정 → Recall 산출
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 정답 근거 문장·청크 라벨링 | 근거 라벨 누락률 <5% |
| 2 | RAG 검색 결과 Top-K 수집 | K=5~20 |
| 3 | gold evidence 포함 여부 판정 | Judge 일치율 κ ≥0.7 |
| 4 | Context Recall 계산·개선 적용 | Recall ≥0.85 |

> 요약: 정답 근거 대비 검색 결과의 포함 여부를 측정해 검색 누락을 정량화함.

## Ⅳ. 특징

| 구분 | Context Precision | Context Recall | 판단 포인트 |
|:---|:---|:---|:---|
| 평가 축 | 상위 결과의 관련성 | 필요한 근거 포함률 | 둘 다 충족 필요 |
| 개선 수단 | 리랭커·MMR | Top-K 확대·Hybrid·Rewrite | 누락이면 Recall 개선 |
| 위험 | 낮으면 환각 유발 | 낮으면 답변 불가 | 원인 분리 |
| 목표 기준 | @5 0.8 이상 | 0.85 이상 | 업무 위험도별 조정 |

> 요약: Context Recall은 필요한 근거를 놓치지 않는지 측정하며, 무관 문서 혼입은 Precision으로 함께 통제함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 검색 누락 개선: Dense Top-20에 BM25 Top-20을 RRF 결합해 Context Recall 0.72→0.88 달성
2. 질의 보정: 약어·동의어 Query Rewrite 적용, 규정 번호·서비스명은 BM25 가중치 상향
3. 운영 게이트: Context Recall 0.85 미만 질의는 색인·청킹·Top-K 변경 실험 대상으로 자동 분류

**결론 (2줄):**
- 기술사 판단: 답변 실패 원인이 근거 누락이면 Context Recall을 우선 개선
- 향후 방향: query decomposition과 multi-hop retrieval로 복합 질의 근거 재현율을 높이는 방향으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Context Recall을 설명하시오" | gold evidence→검색 결과→커버리지 계산 흐름 | Context Precision 대비 차이 |
| 요구사항 명시형 | "RAG 검색 누락 개선 방안을 제시하시오" | Top-K·Hybrid·Rewrite 개선 절차 | Precision과의 트레이드오프 |

> 요약: 설명형은 근거 커버리지 원리, 방안형은 검색 누락 개선 기준을 중심으로 작성함.
