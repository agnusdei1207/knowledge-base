---
title: "출처 기반 답변 (Citation-based Answering)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 134
---

# 📖 【암기용】 개념 완전 이해

> 목적: Citation-based Answering을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 답변의 문장이나 주장마다 근거 문서·페이지·청크 출처를 함께 제시하는 응답 방식
- **왜 필요한가**: 사용자는 AI 답변을 그대로 믿기보다 어떤 문서에 근거했는지 확인해야 함.
- **핵심 직관**: 시험 답안의 핵심 주장마다 참고문헌 각주를 붙이는 방식임.

## 깊이 이해
- **배경·문제의식**: RAG 답변이 근거 문서를 사용해도 출처 표시가 없으면 사용자는 검증할 수 없고 감사 추적도 어렵다.
- **작동 원리**: 검색 컨텍스트에 source_id, page, paragraph를 보존하고, 답변 생성 시 claim별 citation을 연결한 뒤 원문 링크와 함께 출력함.
- **비유**: 법률 의견서에서 "민법 제○조"와 판례 번호를 함께 쓰는 것처럼, 답변 근거를 바로 확인하게 하는 구조임.
- **구체 예시**: 규정 챗봇에서 답변 문장마다 문서명·조항·개정일을 표시해 출처 확인 클릭률과 신뢰도 평가를 추적함.
- **흔한 오해·주의점**: 출처를 붙였다고 항상 맞는 답은 아님. citation이 실제 주장과 일치하는지 Groundedness 검증이 필요함.

## 연결 개념
- Groundedness — 답변과 출처의 근거 일치성
- RAG — 출처 컨텍스트를 제공하는 검색증강생성 구조
- Audit Log — 답변·근거·출처를 사후 검증하기 위한 기록

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Citation-based Answering은 답변 claim과 근거 문서를 명시적으로 연결하는 응답 방식임.
> 2. **가치**: 사용자 검증, 감사 추적, 환각 탐지를 지원해 기업 RAG 신뢰성을 높임.
> 3. **판단 포인트**: citation coverage와 citation correctness를 별도로 측정해야 함.

## Ⅰ. 개요 및 필요성

Citation-based Answering은 출처 연결형 답변 방식임. RAG 답변은 근거를 사용해도 출처가 없으면 검증과 감사가 어렵다. 문장별 출처를 제공해 사용자가 원문을 확인하고 답변 신뢰도를 판단하게 한다.

## Ⅱ. 구조 및 구성요소

```text
Retrieved Context(source_id/page) → Answer Claims
  → Citation Mapper → Grounding Check → Answer with Sources
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Metadata | 문서명·페이지·조항 정보 | source_id, version, timestamp |
| Claim Extractor | 답변 주장 단위 식별 | 문장·원자 claim |
| Citation Mapper | claim과 근거 청크 연결 | one-to-many citation 가능 |
| Citation Verifier | 출처-주장 일치성 검증 | correctness, coverage |

> 요약: 출처 기반 답변은 검색 컨텍스트의 메타데이터를 보존하고 claim별로 근거 문서를 연결함.

## Ⅲ. 동작원리 및 흐름도

```text
질의 → RAG 검색 → 출처 메타데이터 보존
  → 답변 생성 → claim별 citation 연결
  → 출처 일치성 검증 → 원문 링크 출력
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 검색 청크에 source_id·page·version 부여 | 출처 누락률 0% |
| 2 | 답변 claim을 근거 청크와 매핑 | citation coverage 100% |
| 3 | citation correctness 검증 | 일치율 ≥95% |
| 4 | 원문 링크·조항·개정일 출력 | 클릭 검증 가능 |

> 요약: 검색 단계부터 출처 메타데이터를 유지하고 답변 claim에 연결해 검증 가능한 응답을 생성함.

## Ⅳ. 특징

| 구분 | 일반 RAG 답변 | 출처 기반 답변 | 판단 포인트 |
|:---|:---|:---|:---|
| 검증 가능성 | 낮음 | 원문 링크 확인 가능 | 규정·법무는 필수 |
| 환각 탐지 | 답변 사후 추정 | claim-citation 검증 | correctness 필요 |
| 사용자 신뢰 | 답변만 제공 | 근거와 함께 제공 | 출처 품질 중요 |
| 운영 비용 | 낮음 | 메타데이터·검증 비용 | 감사 요구와 비교 |

> 요약: 출처 기반 답변은 검증 가능성을 높이지만, 잘못된 citation을 막기 위한 일치성 검증이 필요함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 문서 메타데이터: 청킹 시 source_id, page, section, version, ACL을 필수 필드로 저장
2. 답변 정책: citation 없는 claim은 출력 금지, citation correctness 95% 미만이면 재검색 수행
3. 감사 로그: 질의, 답변, 검색 컨텍스트, citation, 원문 스냅샷을 90일 이상 보관

**결론 (2줄):**
- 기술사 판단: 기업 RAG는 출처 기반 답변을 기본값으로 두고, 비근거 답변은 거절 정책 적용
- 향후 방향: 문장별 citation 검증과 UI 원문 하이라이트가 결합된 검증형 AI 응답으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "출처 기반 답변을 설명하시오" | 검색→claim→citation→검증 흐름 | 일반 RAG 대비 차이 |
| 요구사항 명시형 | "기업 RAG 신뢰성 확보 방안을 제시하시오" | citation coverage·correctness 기준 | 감사로그·거절 정책 |

> 요약: 설명형은 출처 연결 구조, 방안형은 검증 지표와 감사 대응을 중심으로 작성함.
