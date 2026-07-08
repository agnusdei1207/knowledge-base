---
title: "LLM02 Sensitive Information Disclosure (LLM02 Sensitive Information Disclosure)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 198
extra:
  question_no: "198"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM02는 모델과 RAG와 시스템 프롬프트를 통해 민감정보가 응답으로 노출되는 위험을 다룸
- 비밀은 프롬프트에 넣지 않고 데이터 접근은 모델이 아니라 시스템이 통제해야 한다는 원칙이 중요함
- prompt leakage와 broken access control과 memorization이 대표 경로임

## Ⅰ. 개요

- **정의/개념**: LLM02 Sensitive Information Disclosure는 LLM 애플리케이션이 응답 생성 과정에서 개인정보와 내부 기밀과 자격 증명과 시스템 지침을 외부에 노출하는 OWASP 보안 위험 항목임
- **배경/필요성**: 기업은 모델 품질을 높이기 위해 사내 문서와 피드백과 예시 데이터를 많이 활용하지만, 접근 통제와 비밀 분리가 없으면 모델이 이를 응답으로 재노출하는 구조적 위험이 커짐

## Ⅱ. 특징

- 모델 암기와 프롬프트 유출과 RAG 권한 오류가 동시에 작동할 수 있음
- 유출 대상이 PII뿐 아니라 API 키와 내부 URL과 영업 로직까지 넓음
- 사용자는 정상 질의만 했더라도 구조가 잘못되면 민감정보가 노출될 수 있음
- 방어는 데이터 최소화와 ACL과 출력 DLP의 결합이 핵심임

## Ⅲ. 종류 및 비교

| 판단 기준 | Memorization Leakage | Prompt Leakage | Broken RAG Access |
|:---|:---|:---|:---|
| 원인 | 과적합된 학습 데이터 | 시스템 지시 노출 | 권한 없는 문서 검색 |
| 유출 대상 | PII, PHI, 학습 샘플 | 내부 정책, 키, 예시 | 기밀 문서 내용 |
| 방어 핵심 | DP, data minimization | secret separation | ACL, RBAC, ABAC |
| 대표 위험 | 재식별 | IP 유출 | 권한 상승형 정보 노출 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Sensitive Data Source | 학습 데이터와 시스템 지시와 벡터 DB 문서가 민감정보의 원천이 됨 |
| Context Assembly | 프롬프트와 RAG 검색 문서를 조합하는 과정에서 과도한 기밀이 컨텍스트에 들어갈 수 있음 |
| Access Control Layer | 사용자와 문서와 도구 권한을 일치시켜 볼 수 있는 정보 범위를 강제함 |
| Output DLP, Sanitizer | 응답 생성 후 민감 패턴과 정책 위반 내용을 탐지해 차단함 |
| Logging, Incident Response | 유출 시도와 차단 결과를 기록해 재발 방지와 감사에 활용함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Sensitive Source  | ---> | Context Assembly  | ---> | Access Control    |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Output DLP        |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 민감정보 유입     | --> | 컨텍스트 결합    | --> | 권한 검증 실패  | --> | 응답 노출/차단  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **민감정보 유입**: 학습·프롬프트·RAG 경로에 기밀 데이터가 들어감
2. **컨텍스트 결합**: 모델 입력 구성 시 해당 정보가 프롬프트 근처에 위치함
3. **권한 검증 실패**: 사용자와 데이터 접근 범위가 맞지 않아 유출 가능성이 생김
4. **응답 노출 또는 차단**: 출력 DLP가 없으면 그대로 노출됨

## Ⅵ. 문제점 및 해결 방안

1. 문제: 시스템 프롬프트와 few-shot 예시에 비밀과 내부 지침을 직접 넣으면 prompt leakage 하나로 다수 정보가 동시에 유출될 수 있음
   - 해결방안: secret separation과 external vault를 적용하고 hardcoded secret count와 prompt leakage rate로 검증함
2. 문제: RAG 검색이 사용자 권한과 무관하게 문서를 조회하면 정상 질의만으로도 타 부서 기밀이 응답에 포함될 수 있음
   - 해결방안: document-level ACL과 attribute-based filtering을 적용하고 unauthorized retrieval rate와 document access compliance로 검증함
3. 문제: 출력 검사가 없으면 모델이 암기한 개인정보와 내부 키를 자연어 문맥 속에 섞어 내보내도 탐지가 늦어질 수 있음
   - 해결방안: output DLP와 PII pattern scan을 적용하고 leakage detection rate와 false negative rate로 검증함

## Ⅶ. 적용 사례

- 사내 규정 챗봇이 직급 기반 RAG ACL을 적용하고 운영되며 확인 지표는 unauthorized retrieval rate와 user satisfaction score임
- 고객지원 LLM이 출력 DLP와 비밀 분리 원칙을 적용하며 확인 지표는 sensitive token exposure rate와 response helpfulness score임
- 의료 보조 모델이 DP 학습과 최소 데이터 유지 정책을 결합해 운영되며 확인 지표는 memorization leakage score와 diagnostic accuracy임

## Ⅷ. 결론

LLM02는 모델이 기밀성 개념을 스스로 이해하리라는 가정을 깨뜨리는 위험이므로 비밀 분리와 접근 통제와 출력 DLP를 구조적으로 결합해야 함.
