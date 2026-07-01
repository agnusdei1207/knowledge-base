---
title: "LLM08 벡터 및 임베딩 취약점 (LLM08 Vector and Embedding Weaknesses)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 204
---

# 📖 【암기용】 개념 완전 이해

> 목적: LLM08 Vector and Embedding Weaknesses를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: RAG와 벡터DB에서 임베딩, 검색, 인덱스, 권한 필터 실패로 잘못된 문서 검색·정보노출·오염이 발생하는 위험
- **왜 필요한가**: LLM 서비스는 답변 근거를 벡터 검색에 의존하지만 임베딩 유사도는 권한과 신뢰성을 자동 보장하지 않음.
- **핵심 직관**: AI의 참고문헌 검색기가 잘못된 책이나 권한 없는 책을 가져오면 답변도 위험해지는 구조임.

## 깊이 이해
- **배경·문제의식**: RAG는 외부 지식을 벡터화해 검색하지만, chunk 권한·출처·오염·유사도 임계값을 잘못 설계하면 보안 사고가 발생함.
- **작동 원리**: 공격자는 악성 문서 삽입, embedding collision, 권한 없는 chunk 검색, stale index, prompt injection 문서로 LLM 컨텍스트를 오염시킴.
- **비유**: 도서관 검색 시스템이 비슷한 제목만 보고 기밀 문서나 위조 문서를 추천하는 상황임.
- **구체 예시**: 퇴사자 권한 문서가 벡터DB에 남아 신규 직원 질문에 검색되고, LLM이 민감 계약 내용을 요약함.
- **흔한 오해·주의점**: 벡터DB는 단순 검색 엔진이 아니다. 문서 ACL, metadata filter, index lifecycle, 출처 검증이 함께 필요함.

## 연결 개념
- RAG — 벡터 검색 기반 LLM 지식 보강 구조
- Indirect Prompt Injection — 문서 내 숨은 지시로 컨텍스트 오염
- LLM02 Sensitive Information Disclosure — 권한 없는 검색 결과 노출

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM08은 벡터DB·임베딩·RAG 검색 계층의 권한·무결성·신뢰성 실패 위험임.
> 2. **가치**: 잘못된 chunk 검색은 민감정보 노출, 프롬프트 인젝션, 오정보 응답으로 이어짐.
> 3. **판단 포인트**: metadata ACL, index versioning, 문서 검증, retrieval evaluation을 필수 적용해야 함.

## Ⅰ. 개요 및 필요성

- 개요: 벡터·임베딩 계층 취약점이다.
- 배경: RAG는 벡터 검색 결과를 LLM 컨텍스트로 사용하므로 잘못된 chunk나 권한 없는 문서가 답변에 반영될 수 있다.
- 필요성: LLM08은 retrieval ACL, index integrity, embedding drift monitoring으로 검색 권한·문서 무결성을 통제한다.

## Ⅱ. 구조 및 구성요소

```text
Document -> Chunk/Embedding -> Vector DB Retrieval
  -> Context Injection -> LLM Answer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Chunk Metadata | ACL·출처·등급 저장 | filter 필수 |
| Embedding Model | 문서 벡터화 | 버전 변화 영향 |
| Vector Index | 유사도 검색 수행 | stale index 위험 |
| Retrieval Guard | 권한·출처·임계값 검증 | top-k, threshold |

> 요약: LLM08은 문서 chunk와 벡터 검색 결과가 권한·무결성 검증 없이 컨텍스트로 들어갈 때 발생함.

## Ⅲ. 동작원리 및 흐름도

```text
문서 수집 -> metadata/embedding 생성 -> 권한 필터 검색
  -> 검색 품질 평가 -> 인덱스 갱신·폐기
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 문서 출처·ACL·민감도 태깅 | metadata 100% |
| 2 | chunking·embedding 생성 | 모델 버전 기록 |
| 3 | 사용자 권한 기반 retrieval 수행 | unauthorized chunk 0건 |
| 4 | stale·poisoned index 제거 | 재색인 SLA 24h |

> 요약: LLM08 대응은 RAG 문서 metadata와 권한 필터를 벡터 검색 단계에서 강제하는 방식임.

## Ⅳ. 특징

| 구분 | 일반 검색 보안 | LLM08 Vector/Embedding | 판단 포인트 |
|:---|:---|:---|:---|
| 검색 기준 | 키워드·권한 | 유사도·metadata | ACL 결합 |
| 위험 | 문서 직접 노출 | LLM 컨텍스트 간접 노출 | RAG 경로 |
| 오염 | 검색 색인 오류 | 악성 chunk·embedding 공격 | provenance |
| 관리 | 색인 갱신 | 모델·인덱스 버전관리 | lifecycle |

> 요약: LLM08은 벡터 유사도 검색에 권한·출처·버전 통제를 결합해야 하는 RAG 특화 위험임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. ACL 검색: chunk마다 owner, classification, tenant, expiry를 저장하고 vector query에 metadata filter를 필수 적용
2. 인덱스 관리: embedding model, chunk rule, index version을 기록하고 문서 삭제 시 24시간 내 재색인
3. 품질 검증: retrieval precision@k, unauthorized chunk 0건, poisoned document injection 테스트를 배포 게이트로 적용

**결론 (2줄):**
- 기술사 판단: RAG 보안은 LLM보다 벡터 검색 계층의 ACL·출처·인덱스 수명주기 통제에서 시작
- 향후 방향: LLM08 대응은 RAGOps, vector DB 보안, 콘텐츠 신뢰 점수와 통합됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "LLM08을 설명하시오" | 문서->벡터검색->컨텍스트 흐름 | 일반 검색 보안 대비 차이 |
| 요구사항 명시형 | "RAG 보안 방안을 제시하시오" | metadata ACL·인덱스 관리 | 벡터DB 운영 기준 |

> 요약: 설명형은 RAG 검색 계층 위험, 방안형은 chunk ACL과 인덱스 생명주기 통제를 중심으로 작성함.
