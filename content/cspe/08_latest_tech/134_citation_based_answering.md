---
title: "Citation-based Answering (출처 기반 답변)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 134
extra:
  question_no: "134"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Citation-based Answering은 답변과 함께 근거 문서나 문단을 명시하는 응답 방식임
- 신뢰성, 감사 추적성, 사용자 검증 가능성을 높이는 데 목적이 있음
- RAG, groundedness, enterprise search와 강하게 연결됨

## Ⅰ. 개요

- **정의/개념**: Citation-based Answering은 생성 답변의 각 핵심 주장에 대응하는 출처 문서와 구간을 함께 제시해 사용자가 근거를 직접 검증할 수 있게 하는 응답 방식임
- **배경/필요성**: 생성형 AI는 유창하지만 근거를 숨기기 쉬우므로, 신뢰성과 책임성을 확보하려면 답변과 출처를 함께 제공해야 함

## Ⅱ. 특징

- 답변의 검증 가능성과 사용자 신뢰도를 동시에 높임
- 법무, 금융, 의료처럼 근거 확인이 필요한 도메인에서 특히 중요함
- 단순 링크 첨부보다 claim-to-source 매핑 정확도가 핵심 품질 요소임
- groundedness 평가와 결합될 때 운영 개선 효과가 커짐

## Ⅲ. 종류 및 비교

| 판단 기준 | Citation-based Answering | 일반 생성 답변 | 링크 목록형 응답 |
|:---|:---|:---|:---|
| 출처 명시 | 문장 또는 문단 수준 | 없음 | 문서 수준 |
| 검증 편의성 | 높음 | 낮음 | 중간 |
| 환각 억제력 | 높음 | 낮음 | 중간 |
| 구현 복잡도 | 중간 | 낮음 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Retrieval Layer | 관련 문서를 검색하고 citation 후보가 될 문단과 span을 확보함 |
| Claim Extraction | 답변의 핵심 주장 단위를 분리해 어떤 문장에 출처를 달지 결정함 |
| Source Mapping | 주장과 근거 구간을 연결해 잘못된 출처 부착을 방지함 |
| Rendering Layer | 사용자가 클릭하거나 펼쳐볼 수 있게 출처를 UI에 노출해 검증 경험을 완성함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 문서 검색      | --> | 답변 생성      | --> | 주장-출처 매핑 | --> | 출처 포함 응답 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **문서 검색**: 답변 후보가 될 관련 문서를 top-k로 수집함
2. **답변 생성**: 근거 문맥을 기반으로 답변 초안을 작성함
3. **주장과 출처 매핑**: 핵심 문장마다 대응 근거 span을 지정함
4. **출처 포함 응답**: 사용자에게 답변과 근거를 함께 제시함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 문서 링크만 붙이고 실제 주장과 무관한 출처를 달면 사용자는 답변을 잘못 신뢰할 수 있음
   - 해결방안: sentence-level citation과 evidence validation을 적용하고 citation accuracy와 groundedness score로 검증함
2. 문제: 긴 문서 전체를 인용하면 출처 확인 비용이 커져 사용자 경험이 나빠질 수 있음
   - 해결방안: span highlighting과 snippet rendering을 적용하고 citation click efficiency와 UX satisfaction으로 검증함
3. 문제: 검색 문서가 오래되거나 권한이 없는 자료이면 출처 기반 답변도 운영 위험을 남길 수 있음
   - 해결방안: freshness check와 access control을 결합하고 stale citation rate와 authorization error rate로 검증함

## Ⅶ. 적용 사례

- 법률 검색 서비스에서는 조문과 판례 문단을 답변 옆에 제시하고 확인 지표는 citation accuracy와 trust score임
- 사내 정책 챗봇에서는 사규 링크와 조항 번호를 함께 제공하고 확인 지표는 audit trace completeness와 CSAT임
- 의료 문헌 QA에서는 논문 초록과 근거 문장을 보여주고 확인 지표는 evidence coverage와 expert approval rate임

## Ⅷ. 결론

출처 기반 답변은 생성형 AI를 검증 가능한 도구로 바꾸는 핵심 방식이므로, 링크 유무보다 주장과 근거를 정확히 연결하는 citation 품질이 본질임.
