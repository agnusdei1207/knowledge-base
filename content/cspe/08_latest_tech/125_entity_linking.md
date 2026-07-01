---
title: "개체 연결 (Entity Linking)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 125
---

# 📖 【암기용】 개념 완전 이해

> 목적: Entity Linking을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 텍스트에 등장한 개체명을 지식베이스나 지식그래프의 고유 엔티티 ID와 연결하는 기술
- **왜 필요한가**: 같은 이름이 여러 대상을 가리키거나 같은 대상이 여러 이름으로 불리면 그래프와 검색 결과가 분열됨.
- **핵심 직관**: 문장 속 "애플"이 과일인지 Apple Inc.인지 식별해 정확한 카드에 연결하는 작업임.

## 깊이 이해
- **배경·문제의식**: 문서에는 약어, 별칭, 동명이인, 표기 차이가 섞인다. 이를 고유 ID로 묶지 않으면 지식그래프 노드가 중복되고 RAG 근거가 누락된다.
- **작동 원리**: Mention Detection으로 개체명을 찾고, 후보 엔티티를 검색한 뒤 문맥 임베딩·문자열 유사도·그래프 주변 관계로 점수화해 최종 ID를 선택함.
- **비유**: 전화번호부에서 "김민수"라는 이름만 보고 끝내지 않고, 회사·부서·주소를 확인해 정확한 사람 번호에 연결하는 과정임.
- **구체 예시**: `GPT-4`, `GPT4`, `OpenAI GPT-4`를 동일 모델 엔티티로 연결하면 관련 문서 검색 Recall@10이 15%p 이상 개선될 수 있음.
- **흔한 오해·주의점**: NER만으로는 충분하지 않음. NER은 개체명을 찾고, Entity Linking은 그 개체가 어떤 고유 대상인지 결정함.

## 연결 개념
- NER — 텍스트에서 개체명 범위를 찾는 단계
- Knowledge Graph — 연결 대상이 되는 엔티티 저장소
- Entity Resolution — 중복 엔티티를 병합하는 데이터 정제 기술

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Entity Linking은 텍스트 mention을 지식그래프의 고유 엔티티 ID로 연결하는 기술임.
> 2. **가치**: 별칭·약어·동명이인을 정규화해 그래프 중복과 RAG 검색 누락을 줄임.
> 3. **판단 포인트**: 후보 생성 재현율, 문맥 기반 disambiguation, NIL 처리 기준이 품질을 결정함.

## Ⅰ. 개요 및 필요성

Entity Linking은 개체명 정규화·연결 기술임. 문서의 개체 표현은 약어·별칭·동명이인으로 다양해 지식그래프 노드 중복과 검색 누락을 유발한다. 텍스트 mention을 고유 엔티티 ID로 연결해 지식 기반 품질을 높인다.

## Ⅱ. 구조 및 구성요소

```text
Text -> Mention Detection -> Candidate Generation
  -> Context Disambiguation -> Entity ID/NIL -> KG Update
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Mention Detector | 개체명 범위 탐지 | NER, dictionary, regex |
| Candidate Generator | 후보 엔티티 검색 | alias table, BM25, dense search |
| Disambiguator | 문맥 기반 최종 엔티티 선택 | bi-encoder, cross-encoder, graph context |
| NIL Handler | 기존 엔티티 없음 처리 | 신규 노드 생성·검토 큐 |

> 요약: Entity Linking은 mention 탐지, 후보 생성, 문맥 disambiguation, NIL 처리를 거쳐 고유 엔티티와 연결함.

## Ⅲ. 동작원리 및 흐름도

```text
문서 입력 -> NER/사전으로 mention 탐지
  -> 별칭 테이블 후보 조회 -> 문맥 점수화
  -> 임계값 이상 ID 연결 / 미만 NIL 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | mention 범위 탐지 | mention F1 ≥0.9 |
| 2 | 후보 엔티티 Top-20 생성 | 후보 재현율 ≥95% |
| 3 | 문맥·문자열·그래프 특징으로 순위화 | disambiguation accuracy ≥85% |
| 4 | 임계값 미달 시 NIL·검토 큐 처리 | 오연결률 <3% |

> 요약: 먼저 후보를 넓게 확보하고, 문맥과 그래프 주변 관계로 정확한 엔티티 ID를 선택함.

## Ⅳ. 특징

| 구분 | NER | Entity Linking | 판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 개체명 범위 탐지 | 고유 ID 연결 | KG 구축에는 Linking 필요 |
| 처리 대상 | 문자열 span | 엔티티 후보·문맥 | 동명이인·별칭 해결 |
| 출력 | PERSON/ORG 등 타입 | entity_id 또는 NIL | RAG 출처·관계 정규화 |
| 리스크 | 탐지 누락 | 오연결·중복 노드 | confidence threshold 관리 |

> 요약: NER은 개체명을 찾는 단계이고, Entity Linking은 그 개체를 정확한 지식그래프 노드와 연결하는 단계임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. Graph RAG 구축: alias table과 dense candidate를 결합해 후보 Top-20 생성, confidence 0.8 이상만 자동 연결
2. 운영 검수: NIL·confidence 0.6~0.8 구간은 human review 큐로 보내고 검수 결과를 alias table에 반영
3. 품질 모니터링: mention F1, 후보 재현율, 오연결률, 중복 노드율을 주 단위 측정해 KG 정제

**결론 (2줄):**
- 기술사 판단: 지식그래프·Graph RAG 구축에는 Entity Linking 필수, 단순 문서 검색은 NER+메타데이터로 충분
- 향후 방향: LLM 기반 문맥 disambiguation과 그래프 주변 관계를 결합한 고신뢰 연결로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Entity Linking을 설명하시오" | mention->candidate->disambiguation->NIL 흐름 | NER 대비 차이 |
| 요구사항 명시형 | "지식그래프 구축 방안을 제시하시오" | 후보 재현율·오연결률·검수 큐 기준 | KG 중복·검색 누락 방지 방안 |

> 요약: 설명형은 개체 연결 절차, 방안형은 KG 품질 지표와 운영 검수 기준을 중심으로 작성함.
