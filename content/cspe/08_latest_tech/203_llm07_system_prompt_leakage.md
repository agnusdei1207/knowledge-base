---
title: "LLM07 System Prompt Leakage (LLM07 System Prompt Leakage)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 203
extra:
  question_no: "203"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 시스템 프롬프트는 모델의 역할과 정책과 내부 지침을 담는 상위 제어 문서임
- 이 정보가 노출되면 공격자는 방어 규칙과 우회 힌트를 함께 얻게 되어 후속 공격 성공률이 높아짐
- 비밀 값은 프롬프트에 넣지 않고 프롬프트 자체도 노출 대상이라는 전제로 설계해야 함

## Ⅰ. 개요

- **정의/개념**: LLM07 System Prompt Leakage는 모델의 숨겨진 시스템 지시문이나 정책 규칙이나 내부 운영 문맥이 사용자 질의나 디버그 경로나 취약한 응답 처리로 노출되어 보안 우회와 정보 노출을 초래하는 취약점임
- **배경/필요성**: RAG와 에이전트 구조가 복잡해질수록 시스템 프롬프트에 정책과 예외 규칙과 도구 사용 지침이 길게 들어가며 이 문맥 자체가 공격 가치가 높은 내부 자산이 됨

## Ⅱ. 특징

- 노출된 시스템 프롬프트는 정책 우회용 사전 답안처럼 활용될 수 있음
- 비밀번호나 토큰보다 덜 민감해 보여도 운영 로직과 검열 규칙이 담겨 있어 공격 효율을 높임
- 간접 프롬프트 인젝션과 결합되면 숨은 지침을 끌어내기 쉬워짐
- 프롬프트 버전 관리와 출력 필터링과 secret separation이 함께 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | LLM07 System Prompt Leakage | LLM02 Sensitive Information Disclosure | LLM01 Prompt Injection |
|:---|:---|:---|:---|
| 핵심 자산 | 시스템 지침과 정책 문맥 | 개인 정보와 비밀 데이터 | 입력 지시 해석 과정 |
| 대표 목적 | 방어 규칙 파악과 우회 | 비밀 획득 | 모델 행동 조작 |
| 공격 방식 | prompt extraction, debug leak | retrieval, memory leak | direct, indirect injection |
| 우선 대응 | secret separation, redaction | data minimization | context isolation |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| System Prompt | 역할 정의와 정책과 금지 규칙을 포함하며 노출 시 공격자에게 방어 구조를 설명하는 내부 제어 문서임 |
| Context Assembler | 시스템 프롬프트와 사용자 입력과 RAG 문서를 하나의 컨텍스트로 결합해 누출 경로를 만드는 조립 계층임 |
| Secret Store | 키와 토큰과 민감 상수는 프롬프트 밖에서 호출되도록 분리해 노출 피해를 줄이는 저장소임 |
| Output Filter | 응답에 내부 지침과 정책 문구가 포함되는지 검사해 직접 누출을 막는 마지막 방어 계층임 |
| Prompt Governance | 프롬프트 버전과 테스트와 승인 절차를 관리해 내부 지침 품질과 노출 위험을 통제함 |

```text
+---------------+    +------------------+    +-------------+    +---------------+
| System Prompt | -> | Context Assembler| -> | LLM Response| -> | Output Filter |
+---------------+    +------------------+    +-------------+    +---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 지침 구성    | -> | 문맥 결합    | -> | 추출 시도    | -> | 누출 필터링  | -> | 응답 반환    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **지침 구성**: 시스템 역할과 정책과 예외 규칙을 상위 프롬프트로 작성함
2. **문맥 결합**: 사용자 입력과 외부 검색 결과와 시스템 지시를 하나의 컨텍스트로 합침
3. **추출 시도**: 공격자가 숨은 규칙을 그대로 출력하라고 유도하거나 우회 질문을 던짐
4. **누출 필터링**: 내부 키워드와 정책 문자열과 비밀 지시문 노출 여부를 검사함
5. **응답 반환**: 안전한 부분만 사용자에게 제공함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 시스템 프롬프트에 토큰과 내부 URL과 운영 비밀을 직접 넣으면 단일 누출로 보안 자산이 노출될 수 있음
   - 해결방안: secret vault 분리와 runtime credential injection을 적용하고 prompt embedded secret count와 leaked secret incident rate로 검증함
2. 문제: 장문의 정책 프롬프트가 그대로 노출되면 공격자가 우회 규칙과 필터 약점을 학습해 후속 공격 정밀도를 높일 수 있음
   - 해결방안: prompt minimization과 response redaction과 extraction resistance test를 적용하고 prompt leak success rate와 jailbreak success rate로 검증함
3. 문제: 디버그 로그와 예외 메시지가 프롬프트 원문을 반환하면 정상 운영 중에도 내부 문맥이 반복 노출될 수 있음
   - 해결방안: safe logging policy와 debug output suppression을 적용하고 raw prompt log exposure rate와 production debug leak count로 검증함

## Ⅶ. 적용 사례

- 기업용 챗봇이 시스템 프롬프트에서 내부 API 키를 제거하고 비밀 저장소를 연동하며 확인 지표는 prompt embedded secret count와 leak incident rate임
- 고객센터 상담봇이 추출 유도 질문에 대한 red team 테스트를 정기 수행하며 확인 지표는 prompt extraction success rate와 policy bypass rate임
- 운영 에이전트가 예외 처리 로그에서 프롬프트 원문을 마스킹하며 확인 지표는 raw prompt log exposure rate와 incident response time임

## Ⅷ. 결론

시스템 프롬프트는 숨겨진 설정이 아니라 공격자가 노릴 수 있는 자산이므로 비밀 분리와 최소화와 누출 저항 테스트를 기본 운영 절차로 삼아야 함.
