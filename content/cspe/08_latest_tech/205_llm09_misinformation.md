---
title: "LLM09 Misinformation (LLM09 Misinformation)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 205
extra:
  question_no: "205"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM09는 모델이 권위 있는 문체로 부정확한 정보를 전달할 때 사용자와 조직이 그 결과를 사실로 채택하는 위험을 다룸
- 단순 환각보다 더 중요한 문제는 근거와 최신성 검증 없이 의사결정에 바로 투입되는 운영 구조임
- 출처 제시와 사실 검증과 신뢰도 표시가 핵심 방어 장치임

## Ⅰ. 개요

- **정의/개념**: LLM09 Misinformation은 LLM이 사실과 다르거나 맥락을 왜곡한 정보를 그럴듯하게 생성하고 사용자가 이를 신뢰하여 업무와 정책과 대외 커뮤니케이션에 반영함으로써 손실과 책임을 유발하는 위험임
- **배경/필요성**: 생성형 AI가 검색과 상담과 문서 작성의 전면에 배치되면서 잘못된 답변이 단순 오답을 넘어 운영 판단과 사회적 신뢰를 직접 훼손하는 문제로 확대됨

## Ⅱ. 특징

- 정확한 근거 없이도 유창성과 자신감 때문에 사용자 신뢰를 얻기 쉬움
- 최신 정보 공백과 긴 문맥 혼선과 잘못된 검색 근거가 오정보를 강화함
- 의료와 법률과 금융처럼 고위험 도메인에서는 작은 오류도 큰 책임 문제로 이어짐
- 사실성 평가와 citation coverage와 human review가 품질 관리의 핵심임

## Ⅲ. 종류 및 비교

| 판단 기준 | LLM09 Misinformation | Hallucination | Deepfake Content |
|:---|:---|:---|:---|
| 결과 형태 | 잘못된 텍스트 정보 확산 | 근거 없는 생성 오류 | 조작된 이미지, 영상, 음성 |
| 주요 원인 | stale source, grounding 부족, 과신 | 학습 공백, 추론 오류 | 생성 모델 합성 |
| 피해 범위 | 업무 판단, 대외 공지, 상담 | 응답 품질 저하 | 사회적 조작, 신원 사칭 |
| 우선 대응 | citation, fact check, review | RAG, calibration | provenance, detection |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Knowledge Source | 최신성과 신뢰성을 가진 내부 문서와 외부 데이터로서 오정보 방지의 출발점이 되는 근거 저장소임 |
| Retrieval Layer | 질문과 관련된 문서를 찾아와 모델 답변을 근거 중심으로 제한하는 검색 계층임 |
| Generation Layer | 검색 결과를 바탕으로 답변을 작성하지만 근거가 약하면 자신감 있는 오답을 생성할 수 있는 모듈임 |
| Fact Check and Citation | 답변 문장별 출처 연결과 사실 검증을 수행해 사용자가 검토 가능한 근거를 제공하는 계층임 |
| User Presentation | 신뢰도와 최신성 경고와 검토 필요 표시를 제공해 과신을 줄이는 인터페이스임 |

```text
+---------------+    +------------+    +-------------+    +------------------+
| Knowledge Base| -> | Retrieval  | -> | Generation  | -> | Fact Check/UI    |
+---------------+    +------------+    +-------------+    +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 질의 수신    | -> | 근거 검색    | -> | 답변 초안    | -> | 사실 검증    | -> | 출처 포함 제시 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **질의 수신**: 사용자의 질문과 도메인 위험도를 함께 파악함
2. **근거 검색**: 최신 문서와 승인된 데이터를 우선 검색함
3. **답변 초안 생성**: 근거 범위 안에서 초안을 작성함
4. **사실 검증**: 주요 수치와 주장과 인용의 근거 일치 여부를 확인함
5. **출처 포함 제시**: 사용자에게 근거 링크와 신뢰도 표시를 함께 제공함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 근거 없는 자유 생성 응답이 최신 정책과 수치와 사실을 임의로 만들어 업무 판단 오류를 유발할 수 있음
   - 해결방안: grounded generation과 mandatory citation policy를 적용하고 citation coverage와 factual error rate로 검증함
2. 문제: 오래된 문서와 캐시된 답변이 계속 재사용되면 시의성이 중요한 영역에서 잘못된 안내가 누적될 수 있음
   - 해결방안: freshness check와 source ttl policy를 적용하고 stale answer rate와 source recency score로 검증함
3. 문제: 사용자가 모델 답변을 과도하게 신뢰하면 검토 절차가 생략되어 작은 오류가 대외 사고로 확대될 수 있음
   - 해결방안: confidence labeling과 domain specific human review를 적용하고 unreviewed high risk response rate와 decision reversal rate로 검증함

## Ⅶ. 적용 사례

- 법무 지원 챗봇이 판례와 사내 지침의 출처 링크를 의무 표기하며 확인 지표는 citation coverage와 legal factual error rate임
- 금융 상담 보조 시스템이 금리와 수수료 정보의 최신성 검사를 수행하며 확인 지표는 stale answer rate와 customer correction rate임
- 사내 정책 안내 봇이 고위험 답변에 담당자 검토 단계를 추가하며 확인 지표는 unreviewed high risk response rate와 escalation rate임

## Ⅷ. 결론

LLM09는 모델의 언어 능력보다 근거와 검토 체계의 부재가 더 큰 문제이므로 사실성 검증과 최신성 관리와 사용자 경고를 운영 기본값으로 설정해야 함.
