---
title: "LLM01 Prompt Injection (LLM01 Prompt Injection)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 197
extra:
  question_no: "197"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM01은 OWASP LLM Top 10에서 프롬프트 인젝션을 최우선 위험으로 본 항목임
- 직접 입력뿐 아니라 간접 입력과 에이전트 권한이 결합될 때 파급력이 커짐
- 개별 모델 방어보다 앱 아키텍처 차원의 분리와 최소 권한이 핵심 대응책임

## Ⅰ. 개요

- **정의/개념**: LLM01 Prompt Injection은 적대적 입력이나 외부 문맥이 시스템 지시를 덮어쓰거나 약화시켜 LLM의 응답과 도구 사용을 의도치 않게 바꾸는 OWASP 최우선 위험 항목임
- **배경/필요성**: LLM 애플리케이션은 지시와 데이터를 같은 맥락 창에서 처리하므로, 프롬프트 오염이 곧 정책 우회와 권한 오남용으로 이어질 수 있어 별도 위험 항목으로 관리할 필요가 커짐

## Ⅱ. 특징

- 직접 입력형과 간접 입력형을 모두 포함하는 상위 위험 항목임
- 단순 유해 답변보다 도구 실행과 데이터 유출을 동반할 때 심각도가 커짐
- 안전 정책보다 외부 문맥이 우선 해석되는 context hijacking이 주요 실패 모드임
- 방어는 필터링뿐 아니라 tool permission과 승인 흐름 설계까지 포함해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Direct Injection | Indirect Injection | Tool-mediated Injection |
|:---|:---|:---|:---|
| 주입 경로 | 사용자 입력창 | 외부 문서, 웹, 메일 | 에이전트 툴 응답 |
| 대표 피해 | 정책 우회 | 세션 오염과 유출 | 실제 시스템 행위 발생 |
| 주요 방어 | input guardrail | content sanitization | least privilege, HITL |
| OWASP 의미 | 기본형 | 공급망형 확장 | 운영 파급형 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| System Instruction | 앱이 모델에 부여한 역할과 금지 규칙으로 공격 시 오버라이드 대상이 됨 |
| Untrusted Input, Context | 사용자 질문과 외부 문서처럼 주입이 일어나는 위험 입력 경로임 |
| Guardrail, Intent Filter | 적대 의도를 식별하고 응답이나 도구 호출을 차단하는 보호 계층임 |
| Tool, Action Boundary | 메일 전송과 DB 수정 같은 실제 행위로 인젝션 영향이 전이되는 경계임 |
| Audit, Feedback Loop | 차단과 실패 사례를 기록해 프롬프트와 정책 개선에 반영함 |

```text
+-------------------+      +-------------------+      +-------------------+
| System Instruction| ---> | Untrusted Context | ---> | Guardrail Layer   |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Tool Boundary     |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 적대 입력 유입    | --> | 시스템 지시 충돌  | --> | 정책 우회 시도  | --> | 응답/행동 변경  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **적대 입력 유입**: 공격자가 직접 또는 간접 입력을 시스템에 넣음
2. **시스템 지시 충돌**: 모델이 사용자 문맥과 시스템 지시를 함께 해석함
3. **정책 우회 시도**: 모델이 안전 제약보다 새 지시를 따르기 시작함
4. **응답 또는 행동 변경**: 유해 답변이나 권한 오남용이 발생함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 시스템 프롬프트와 외부 입력이 같은 컨텍스트에서 처리되면 지시 우선순위가 불안정해 OWASP LLM01 취약성이 구조적으로 반복될 수 있음
   - 해결방안: structured prompt boundary와 instruction isolation을 적용하고 policy override rate와 structured prompt compliance로 검증함
2. 문제: 인젝션 성공 시 에이전트가 고권한 도구를 바로 실행할 수 있으면 피해 범위가 단순 답변 오류를 넘어 실제 업무 사고로 확장될 수 있음
   - 해결방안: least privilege tool scope와 human approval을 적용하고 unauthorized tool execution rate와 high-risk action block rate로 검증함
3. 문제: 직접 입력만 방어하고 외부 문서 기반 간접 주입은 놓치면 RAG와 메일 요약 같은 서비스에서 취약성이 남을 수 있음
   - 해결방안: indirect content sanitization과 retrieval boundary를 적용하고 indirect injection detection rate와 exfiltration block rate로 검증함

## Ⅶ. 적용 사례

- 사내 업무 에이전트가 OWASP LLM01 기준으로 tool 권한을 재설계하고 운영되며 확인 지표는 unauthorized tool execution rate와 user task success rate임
- 고객지원 챗봇이 직접 주입과 간접 주입을 모두 레드팀으로 검증하며 확인 지표는 prompt override rate와 patch lead time임
- RAG 검색 도우미가 untrusted 문서 격리와 승인형 도구 호출을 적용하며 확인 지표는 indirect injection success rate와 grounded answer score임

## Ⅷ. 결론

LLM01은 프롬프트 인젝션을 개별 우회 기법이 아니라 애플리케이션 전반의 제어 흐름 취약점으로 바라보게 하는 핵심 위험 항목임.
