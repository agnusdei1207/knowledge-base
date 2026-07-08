---
title: "LLM08 Vector and Embedding Weaknesses (LLM08 Vector and Embedding Weaknesses)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 204
extra:
  question_no: "204"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 벡터와 임베딩은 문서와 질의를 수치 공간으로 바꾸어 유사도 검색을 가능하게 하는 RAG의 핵심 기반임
- 검색 품질과 접근 통제와 인덱싱 무결성이 약하면 잘못된 근거와 데이터 노출과 검색 조작이 함께 발생함
- 임베딩 파이프라인도 일반 DB처럼 무결성 검증과 권한 분리와 품질 모니터링이 필요함

## Ⅰ. 개요

- **정의/개념**: LLM08 Vector and Embedding Weaknesses는 임베딩 생성과 벡터 저장과 유사도 검색 과정의 취약점으로 인해 검색 오염과 테넌트 간 데이터 노출과 악의적 문서 우선 노출이 발생하는 RAG 보안 문제임
- **배경/필요성**: 최신 LLM 서비스가 검색 증강 생성을 기본 구조로 채택하면서 벡터 DB와 임베딩 모델이 지식 신뢰성과 보안 경계의 핵심 구성요소가 됨

## Ⅱ. 특징

- 모델 본체보다 검색 계층이 잘못되면 정확한 모델도 오염된 답변을 낼 수 있음
- 벡터 검색은 의미 유사성 기반이라 전통적 키워드 필터보다 조작 탐지가 어려움
- 문서 삽입과 chunk 설계와 metadata ACL이 보안 수준을 크게 좌우함
- 검색 품질 저하는 단순 성능 문제가 아니라 간접 프롬프트 인젝션과 정보 노출의 선행 조건이 될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | LLM08 Vector and Embedding Weaknesses | LLM04 Data and Model Poisoning | 전통적 검색 인덱스 오류 |
|:---|:---|:---|:---|
| 핵심 대상 | 임베딩과 벡터 검색 계층 | 학습 데이터와 모델 | 키워드 인덱스 |
| 대표 위험 | 검색 조작, ACL 누락, 오염 근거 | 모델 편향, 백도어 | 단순 검색 정확도 저하 |
| 공격 방식 | malicious document injection | poison sample insertion | relevance gaming |
| 우선 대응 | signed ingestion, ACL, retrieval eval | data validation | ranking tuning |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Documents | 정책 문서와 FAQ와 로그처럼 임베딩 대상이 되는 원천 데이터로서 오염되면 검색 결과 전체를 왜곡할 수 있음 |
| Embedding Model | 텍스트를 dense vector로 변환하며 모델 선택과 버전 차이에 따라 검색 품질과 노출 특성이 달라짐 |
| Vector Store | 임베딩과 메타데이터를 저장하고 유사도 검색을 수행하며 ACL 누락 시 교차 테넌트 노출 위험이 생김 |
| Retriever | 질의 벡터와 인덱스를 비교해 문서를 가져오며 ranking 조작과 low precision 문제가 답변 품질을 흔듦 |
| Security Filter | 문서 출처 검증과 metadata policy와 tenant isolation을 적용해 검색 전후를 통제하는 계층임 |

```text
+-------------+    +----------------+    +--------------+    +-------------+
| Source Data | -> | Embedding Model| -> | Vector Store | -> | Retriever   |
+-------------+    +----------------+    +--------------+    +-------------+
                                                                |
                                                                v
                                                         +-------------+
                                                         | LLM Grounding|
                                                         +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 문서 수집    | -> | 임베딩 생성  | -> | 인덱스 저장  | -> | 유사도 검색  | -> | 근거 기반 응답 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **문서 수집**: 원문과 메타데이터를 ingest 파이프라인으로 수집함
2. **임베딩 생성**: 문서와 질의를 동일 임베딩 공간으로 변환함
3. **인덱스 저장**: 벡터와 tenant 정보와 보안 태그를 함께 저장함
4. **유사도 검색**: 질의와 가까운 문서를 top k 방식으로 선택함
5. **근거 기반 응답**: 검색된 문서를 근거로 LLM이 답변을 생성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 악성 문서가 인덱스에 유입되면 검색 상위에 노출되어 간접 프롬프트 인젝션과 허위 근거 주입을 유발할 수 있음
   - 해결방안: signed ingestion과 trusted source allowlist와 retrieval quality audit를 적용하고 poisoned document detection rate와 top k trust score로 검증함
2. 문제: 벡터 저장소의 메타데이터 ACL이 느슨하면 다른 테넌트 문서가 유사도 검색으로 노출될 수 있음
   - 해결방안: tenant scoped index와 metadata based access control을 적용하고 cross tenant retrieval rate와 unauthorized document exposure count로 검증함
3. 문제: 임베딩 모델 교체나 chunk 설계 불량으로 검색 정밀도가 낮아지면 잘못된 근거가 누적되어 응답 신뢰성이 떨어질 수 있음
   - 해결방안: retrieval benchmark와 chunking standard와 embedding version test를 적용하고 retrieval precision at k와 citation validity rate로 검증함

## Ⅶ. 적용 사례

- 사내 정책 챗봇이 문서 등록 시 서명 검증과 출처 allowlist를 적용하며 확인 지표는 poisoned document detection rate와 top k precision임
- 멀티테넌트 RAG 서비스가 고객사별 인덱스를 분리 운영하며 확인 지표는 cross tenant retrieval rate와 unauthorized exposure count임
- 제품 지원 검색 시스템이 임베딩 모델 변경 전 회귀 평가를 수행하며 확인 지표는 retrieval precision at k와 answer groundedness score임

## Ⅷ. 결론

LLM08은 벡터 검색 계층이 사실상 보안과 정확성의 관문이 되었음을 보여주므로 임베딩 파이프라인을 독립된 핵심 시스템으로 관리해야 함.
