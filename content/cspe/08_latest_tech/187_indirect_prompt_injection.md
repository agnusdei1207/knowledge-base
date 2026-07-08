---
title: "Indirect Prompt Injection 간접 프롬프트 인젝션 (Indirect Prompt Injection)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 187
extra:
  question_no: "187"
  exam_status: "기출"
  exam_history: "137회, 138회"
  exam_note: "전망"
---

## 미리 알고가기

- 간접 프롬프트 인젝션은 사용자 입력이 아니라 외부 문서나 웹 콘텐츠에 숨은 명령이 LLM을 오염시키는 공격임
- RAG와 브라우징과 메일 요약처럼 untrusted content를 읽는 구조에서 특히 위험함
- 문서 정화와 아웃바운드 권한 통제가 핵심 방어 지점임

## Ⅰ. 개요

- **정의/개념**: 간접 프롬프트 인젝션은 공격자가 외부 문서와 웹페이지와 이메일 본문 등에 악성 지시를 숨겨두고, LLM이 해당 콘텐츠를 검색·요약·읽는 과정에서 시스템 지시를 오염시키는 공격임
- **배경/필요성**: 생성형 AI가 RAG와 브라우징과 툴 호출을 통해 외부 데이터를 적극적으로 흡수하는 구조로 바뀌면서, 신뢰하지 않는 콘텐츠가 모델의 제어 흐름에 개입하는 위험이 커짐

## Ⅱ. 특징

- 사용자가 직접 악성 입력을 넣지 않아도 제3자가 만든 문서 하나로 다수 사용자 세션을 공격할 수 있음
- 문서와 HTML과 PDF와 메일 등 다양한 외부 포맷이 공격 매체가 될 수 있음
- 도구 권한이 클수록 유출과 자동 행위 오염의 파급력이 커짐
- 데이터 정화와 RAG 경계 분리가 없으면 공급망형 AI 보안 사고로 번지기 쉬움

## Ⅲ. 종류 및 비교

| 판단 기준 | Direct Injection | Indirect Injection | Data Poisoning |
|:---|:---|:---|:---|
| 주입 위치 | 사용자 대화 입력 | 외부 문서와 웹 콘텐츠 | 학습 데이터 |
| 공격 시점 | 추론 시점 | 추론 시점 | 학습 시점 |
| 대표 피해 | 답변 왜곡, 도구 오남용 | 대량 감염, 외부 유출 | 모델 품질 오염 |
| 방어 핵심 | 입력 검증 | ingestion sanitization, tool isolation | 데이터 검수 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Untrusted Content Source | 웹페이지와 PDF와 이메일처럼 공격자가 조작할 수 있는 외부 문서 원천임 |
| Ingestion, Parsing Layer | 스크래핑과 OCR과 문서 파싱 과정에서 숨은 지시가 컨텍스트로 들어오는 관문임 |
| Retrieval, Context Builder | 검색된 문서를 모델 입력으로 조합하며 악성 지시를 시스템 문맥 가까이 실어 나름 |
| LLM Agent, Tool Interface | 오염된 문맥을 해석해 응답하거나 메일 발송 같은 외부 행동으로 연결하는 실행 계층임 |
| Outbound Control, Audit | 도메인 허용 목록과 승인 절차와 로그로 유출과 오작동을 차단함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Untrusted Source  | ---> | Ingest / Parse    | ---> | Retrieve / Context|
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Agent / Outbound  |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 악성 문서 은닉   | --> | 파서/검색 유입   | --> | 컨텍스트 오염    | --> | 응답/외부행위 유발 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **악성 문서 은닉**: 공격자가 외부 콘텐츠에 숨은 지시를 넣음
2. **파서 및 검색 유입**: 시스템이 해당 문서를 읽어 컨텍스트에 포함함
3. **컨텍스트 오염**: 모델이 숨은 지시를 정상 명령처럼 해석함
4. **응답 또는 외부 행위 유발**: 유출과 오판과 도구 오용이 발생함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 외부 문서를 단순 텍스트로만 처리하면 사람이 보지 못하는 숨은 지시가 그대로 모델 컨텍스트에 주입될 수 있음
   - 해결방안: HTML, PDF sanitization과 trusted context labeling을 적용하고 hidden instruction detection rate와 sanitization coverage로 검증함
2. 문제: RAG 시스템이 검색 문서를 높은 우선순위 컨텍스트로 넣으면 시스템 정책보다 외부 문서 지시가 더 강하게 작동할 수 있음
   - 해결방안: untrusted context boundary와 retrieval policy를 적용하고 context hijack rate와 groundedness score로 검증함
3. 문제: 에이전트의 외부 네트워크와 도구 권한이 넓으면 감염된 문서 하나가 바로 데이터 유출로 이어질 수 있음
   - 해결방안: outbound allowlist와 high-risk tool approval을 적용하고 exfiltration block rate와 unauthorized action rate로 검증함

## Ⅶ. 적용 사례

- 메일 요약 비서가 숨은 인젝션이 있는 메일을 정화한 뒤 처리하며 확인 지표는 hidden prompt detection rate와 data exfiltration incident rate임
- RAG 검색 챗봇이 웹 문서에서 untrusted context를 분리해 답변하며 확인 지표는 indirect injection success rate와 citation integrity임
- 고객 첨부문서 분석 에이전트가 승인 없는 외부 전송을 차단하고 운영되며 확인 지표는 outbound block rate와 human review coverage임

## Ⅷ. 결론

간접 프롬프트 인젝션은 문서와 검색을 신뢰 경계 안으로 끌어들이는 RAG 시대의 공급망 공격이므로 외부 콘텐츠를 기본적으로 불신하는 설계가 필요함.
