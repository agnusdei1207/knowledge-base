---
title: "LLM05 Improper Output Handling (LLM05 Improper Output Handling)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 201
extra:
  question_no: "201"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM05는 모델이 만든 출력을 안전한 데이터로 오인해 브라우저나 셸이나 DB로 그대로 넘길 때 발생하는 취약점임
- 프롬프트 인젝션이 악성 출력을 만들고 부적절한 출력 처리가 실제 실행 사고로 이어지는 경우가 많음
- 구조화 출력과 스키마 검증과 실행 전 샌드박스 통제가 핵심 방어 수단임

## Ⅰ. 개요

- **정의/개념**: LLM05 Improper Output Handling은 LLM이 생성한 텍스트나 코드나 마크업을 신뢰 가능한 결과로 오인하여 검증과 정제 없이 후속 시스템에 전달함으로써 XSS와 SQL Injection과 명령 실행 같은 사고를 유발하는 취약점임
- **배경/필요성**: 에이전트와 자동화 파이프라인이 LLM 출력을 곧바로 렌더링하거나 실행하는 구조가 늘면서 출력 자체를 비신뢰 입력으로 다루는 보안 설계가 필수 과제가 됨

## Ⅱ. 특징

- 입력이 아니라 출력 단계에서 보안 경계가 붕괴된다는 점이 핵심임
- 자연어 응답도 브라우저와 API와 셸에 전달되면 실행 가능한 페이로드가 될 수 있음
- 프롬프트 인젝션과 결합될 때 공격 성공 가능성과 파급 범위가 크게 커짐
- 모델 정렬만으로는 충분하지 않고 애플리케이션 계층에서 검증과 인코딩이 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | LLM05 Improper Output Handling | LLM01 Prompt Injection | LLM06 Excessive Agency |
|:---|:---|:---|:---|
| 핵심 문제 | 출력 검증 부재 | 입력 지시 오염 | 권한 과다 부여 |
| 공격 지점 | 렌더링, 실행, 호출 단계 | 프롬프트 해석 단계 | 도구 실행 단계 |
| 대표 피해 | XSS, RCE, SQLi | 정책 우회, 오염 응답 | 무단 송금, 삭제, 발송 |
| 우선 대응 | sanitize, schema validate | context isolation | least privilege, approval gate |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| LLM Output | 자연어와 코드와 마크업이 섞인 비신뢰 결과로서 후속 시스템에 전달되기 전 검증이 필요한 데이터임 |
| Output Parser | 응답을 JSON이나 함수 호출 형태로 강제 파싱하여 자유 텍스트가 직접 실행 경로로 들어가지 않게 막는 계층임 |
| Sanitizer and Encoder | HTML 이스케이프와 명령어 필터링과 allowlist 검사를 수행해 실행 가능 요소를 제거하는 방어 계층임 |
| Execution Adapter | 검증된 결과만 브라우저와 DB와 툴 API로 전달해 출력과 실행 사이를 분리하는 연결부임 |
| Policy Gate | 민감 작업은 차단하거나 승인 절차를 요구해 출력이 곧바로 파괴적 행동으로 이어지지 않게 통제함 |

```text
+-------------+    +---------------+    +------------------+    +----------------+
| LLM Output  | -> | Parser/Schema | -> | Sanitizer/Policy | -> | Render/Execute |
+-------------+    +---------------+    +------------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 출력 수신    | -> | 형식 검증    | -> | 인코딩/정제  | -> | 정책 판단    | -> | 렌더링/실행 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **출력 수신**: LLM이 생성한 응답을 실행 대상과 분리된 버퍼에서 먼저 받음
2. **형식 검증**: 스키마와 타입과 허용 필드를 기준으로 구조화 응답인지 확인함
3. **인코딩 및 정제**: 마크업과 명령어와 외부 참조를 컨텍스트에 맞게 제거하거나 이스케이프함
4. **정책 판단**: 민감 행위 여부를 평가하고 승인이나 차단이나 샌드박스 실행을 결정함
5. **렌더링 및 실행**: 검증을 통과한 결과만 대상 시스템에 반영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 자유 텍스트 출력을 브라우저나 셸로 직접 전달하면 악성 스크립트와 명령이 실행되어 시스템 침해로 이어질 수 있음
   - 해결방안: structured output과 context aware sanitization과 sandbox execution을 적용하고 blocked payload rate와 execution incident rate로 검증함
2. 문제: 응답 스키마가 느슨하면 숨겨진 필드나 우회 문자열이 후속 파서에 스며들어 예상 밖 동작을 유발할 수 있음
   - 해결방안: strict schema validation과 allowlist parser를 적용하고 schema rejection rate와 unsafe field pass rate로 검증함
3. 문제: 출력 처리 계층이 감사 로그 없이 자동 실행되면 사고 원인과 전파 경로를 추적하기 어려워짐
   - 해결방안: execution audit log와 policy decision trace를 남기고 mean time to detect와 forensic completeness score로 검증함

## Ⅶ. 적용 사례

- 고객지원 챗봇이 HTML 응답을 DOMPurify와 escape 처리 후 렌더링하며 확인 지표는 blocked script rate와 user response accuracy임
- 코드 생성 에이전트가 명령 실행 전 JSON 스키마 검증과 샌드박스 실행을 거치며 확인 지표는 unsafe command rejection rate와 task completion rate임
- 내부 문서 요약 서비스가 링크와 쿼리 문자열을 allowlist 기반으로 재작성하며 확인 지표는 malicious URL leakage rate와 citation validity rate임

## Ⅷ. 결론

LLM05는 모델이 아니라 출력과 실행 사이의 설계 결함에서 발생하므로 출력 비신뢰 원칙과 구조화 검증 체계를 애플리케이션 기본 규칙으로 내재화해야 함.
