---
title: "AI Hallucination (환각)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 133
extra:
  question_no: "133"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- 환각은 모델이 사실처럼 보이는 잘못된 정보를 생성하는 현상임
- 폐쇄형 LLM뿐 아니라 RAG에서도 검색 실패나 생성 제약 부족으로 발생함
- 기술적으로는 근거 부재, 추론 오류, 오래된 지식 혼입이 주요 원인임

## Ⅰ. 개요

- **정의/개념**: AI 환각은 모델이 입력과 근거 문서와 실제 사실에 의해 충분히 뒷받침되지 않는 내용을 그럴듯한 문장으로 생성하는 오류 현상임
- **배경/필요성**: 생성형 AI는 확률적으로 다음 토큰을 예측하므로 사실 검증보다 유창성을 우선할 수 있어, 서비스 신뢰성과 안전성을 위해 환각 통제가 필수임

## Ⅱ. 특징

- 문장 유창성이 높아 사용자가 오류를 뒤늦게 인지하기 쉬움
- 검색 실패와 모델 추론 오류와 프롬프트 부족이 복합적으로 작용함
- 고위험 도메인에서는 작은 환각도 법적, 금전적 손실로 이어질 수 있음
- 완전 제거보다 발생률 감소와 조기 탐지와 영향 제한이 현실적 목표임

## Ⅲ. 종류 및 비교

| 판단 기준 | 사실 환각 | 근거 환각 | 추론 환각 |
|:---|:---|:---|:---|
| 오류 성격 | 존재하지 않는 사실 생성 | 문맥에 없는 내용 추가 | 논리 전개 오류 |
| 주된 원인 | 학습 지식 왜곡 | retrieval 실패, prompt 약함 | reasoning chain 불안정 |
| 탐지 방법 | fact check | faithfulness, groundedness | step validation |
| 완화 수단 | 최신 지식 보강 | citation, constrained decoding | self-check, verifier |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Data Source | 학습 데이터와 검색 문맥 품질이 낮으면 환각 발생 기반이 커짐 |
| Model Generation | 확률적 생성 특성 때문에 근거가 불충분해도 문장을 이어갈 수 있음 |
| Prompt, Guardrail | 답변 범위와 출처 요구를 명시해 불필요한 추정을 억제하는 통제 계층임 |
| Evaluation, Monitoring | Faithfulness, groundedness, user report를 통해 환각 유형을 지속 감시함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 입력/문맥 수신 | --> | 확률적 생성    | --> | 근거 부족 혼입 | --> | 환각 탐지/차단 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **입력과 문맥 수신**: 모델이 질문과 제공 문맥을 받음
2. **확률적 생성**: 가장 자연스러운 토큰 연쇄를 생성함
3. **근거 부족 혼입**: 검색 누락이나 추정 확장으로 unsupported claim이 발생함
4. **환각 탐지 및 차단**: 평가기와 citation 검증과 guardrail이 오류를 걸러냄

## Ⅵ. 문제점 및 해결 방안

1. 문제: 검색이 빗나가거나 문맥이 부족하면 모델이 빈칸을 추정으로 메우면서 사실성 없는 답변을 생성할 수 있음
   - 해결방안: hybrid retrieval과 fallback refusal 정책을 적용하고 hallucination rate와 no-answer accuracy로 검증함
2. 문제: 사용자가 유창한 답변을 사실로 받아들이면 잘못된 의사결정으로 직접 이어질 수 있음
   - 해결방안: citation 노출과 confidence gating을 적용하고 user correction rate와 trust calibration로 검증함
3. 문제: 운영 환경에서는 환각 사례가 누적돼도 분류 체계가 없으면 개선 포인트를 찾기 어려움
   - 해결방안: hallucination taxonomy를 구축하고 유형별 incident count와 fix lead time으로 개선 흐름을 검증함

## Ⅶ. 적용 사례

- 금융 상담 챗봇에서는 근거 없는 금리 설명을 차단하고 확인 지표는 hallucination rate와 complaint count임
- 사내 규정 검색에서는 없는 사규 조항 생성을 막고 확인 지표는 no-answer accuracy와 audit issue count임
- 의료 QA에서는 불확실 시 답변 거절 전략을 적용하고 확인 지표는 unsafe response rate와 expert review score임

## Ⅷ. 결론

AI 환각은 모델의 유창함이 사실 검증을 대체할 때 발생하므로, 검색 품질과 답변 제약과 운영 모니터링을 함께 설계해야 실질적으로 줄일 수 있음.
