---
title: "근거성 (Groundedness)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 132
---

# 📖 【암기용】 개념 완전 이해

> 목적: Groundedness를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: AI 답변이 제공된 데이터·문서·출처에 근거해 생성되었는지 평가하는 품질 속성
- **왜 필요한가**: 기업 RAG에서는 답변이 맞아 보여도 출처 없는 주장이나 문서 밖 추론이 업무 리스크가 됨.
- **핵심 직관**: 답변의 발이 실제 근거 문서 위에 딛고 있는지 확인하는 기준임.

## 깊이 이해
- **배경·문제의식**: LLM은 문서 근거가 부족해도 일반 지식으로 빈칸을 채울 수 있다. 규정·감사·의료 영역에서는 근거 없는 보완이 허용되지 않음.
- **작동 원리**: 답변 문장과 citation, 검색 컨텍스트를 비교해 각 주장이 특정 근거에 연결되는지 확인하고, 출처 없는 문장은 비근거 주장으로 분류함.
- **비유**: 보고서의 모든 핵심 문장에 각주가 붙어 있고, 각주 문서에 실제 내용이 있는지 확인하는 과정임.
- **구체 예시**: Groundedness 0.95 이상과 citation coverage 100%를 금융 규정 챗봇 배포 기준으로 설정.
- **흔한 오해·주의점**: Groundedness와 Faithfulness는 유사하지만, Groundedness는 출처 연결과 근거 기반 응답 정책까지 포함하는 운영 개념으로 쓰임.

## 연결 개념
- Faithfulness — 답변 주장이 컨텍스트와 일치하는지 측정
- Citation-based Answering — 답변 문장에 출처를 연결하는 방식
- AI Hallucination — 근거 없는 생성 오류

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Groundedness는 AI 답변이 명시적 근거와 출처에 기반하는지 평가하는 품질 속성임.
> 2. **가치**: 출처 없는 주장과 문서 밖 추론을 차단해 감사·규제 대응 가능성을 높임.
> 3. **판단 포인트**: 문장별 citation, 근거 검증, 근거 부족 시 답변 거절 정책이 함께 필요함.

## Ⅰ. 개요 및 필요성

Groundedness는 답변 근거 기반성 품질 속성임. RAG는 외부 문서를 제공하지만 LLM이 문서 밖 내용을 생성할 수 있다. 기업 환경에서는 답변과 출처를 연결해 감사 가능한 응답을 제공해야 한다.

## Ⅱ. 구조 및 구성요소

```text
Answer Sentence → Citation Link → Evidence Context
  → Grounding Judge → Groundedness Score/Policy
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Answer Sentence | 검증 대상 주장 | 문장·claim 단위 분해 |
| Citation Link | 출처 문서·청크 연결 | source_id, page, paragraph |
| Evidence Context | 실제 근거 내용 | 검색 컨텍스트·원문 |
| Grounding Judge | 출처 기반성 판정 | entailment, LLM Judge |

> 요약: Groundedness는 답변 문장과 출처 근거를 연결하고 각 주장의 근거 기반성을 판정함.

## Ⅲ. 동작원리 및 흐름도

```text
답변 생성 → 문장별 출처 연결 → 근거 문서 조회
  → 주장-근거 일치 판정 → 점수화 → 거절/수정 정책 적용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 답변을 claim 단위로 분해 | claim 누락률 <5% |
| 2 | claim별 citation 연결 | citation coverage 100% |
| 3 | 근거 문서와 entailment 판정 | Groundedness ≥0.95 |
| 4 | 미근거 claim 처리 | 답변 거절·재검색·수정 |

> 요약: 답변의 각 주장을 출처와 연결하고 근거 일치성을 검증해 근거 부족 문장을 통제함.

## Ⅳ. 특징

| 구분 | Faithfulness | Groundedness | 판단 포인트 |
|:---|:---|:---|:---|
| 초점 | 컨텍스트와 일치 | 출처 연결·근거 정책 | 규제 산업은 Groundedness |
| 입력 | answer, contexts | answer, citations, source | citation coverage 필요 |
| 산출 | 지표 점수 | 점수+운영 정책 | 거절 기준 포함 |
| 리스크 | Judge 오판 | 잘못된 citation | 원문 링크 검증 필요 |

> 요약: Groundedness는 Faithfulness를 포함해 출처 연결과 근거 부족 응답 정책까지 확장한 운영 기준임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 문장별 출처: 답변 모든 claim에 source_id·page·paragraph를 붙이고 citation coverage 100% 검증
2. 근거 부족 정책: Groundedness 0.95 미만 또는 출처 0건이면 답변 거절 후 추가 검색 수행
3. 감사 대응: 답변·검색 컨텍스트·citation·Judge 결과를 90일 이상 보관해 사후 검증 지원

**결론 (2줄):**
- 기술사 판단: 금융·의료·법무 RAG는 Groundedness를 배포 필수 지표로 설정
- 향후 방향: 문장별 citation 검증과 원문 스냅샷 보관을 결합한 감사 가능한 AI 응답 체계로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Groundedness를 설명하시오" | claim→citation→근거 판정 흐름 | Faithfulness 대비 차이 |
| 요구사항 명시형 | "기업 RAG 신뢰성 확보 방안을 제시하시오" | 출처 연결·거절 정책·감사로그 | 규제 대응과 운영 통제 |

> 요약: 설명형은 근거 기반성 원리, 방안형은 출처 검증과 감사 대응 기준을 중심으로 작성함.
