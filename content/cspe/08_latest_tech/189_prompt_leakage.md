---
title: "Prompt Leakage 프롬프트 유출 (Prompt Leakage)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 189
extra:
  question_no: "189"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 프롬프트 유출은 시스템 프롬프트와 few-shot 예시와 내부 지침이 응답으로 새어 나오는 취약점임
- 지식재산 노출 문제이면서 동시에 내부 URL과 키와 규정이 드러날 수 있는 보안 문제이기도 함
- 핵심 원칙은 프롬프트에 비밀을 넣지 않고 비밀 관리와 응답 검사를 분리하는 것임

## Ⅰ. 개요

- **정의/개념**: 프롬프트 유출은 시스템 프롬프트와 예시 데이터와 내부 정책 설명이 사용자의 질의나 간접 공격에 의해 응답으로 노출되는 정보 유출 취약점임
- **배경/필요성**: 많은 AI 서비스가 시스템 프롬프트를 제품 차별화 자산으로 사용하고 일부는 내부 규정과 도구 설명까지 포함하므로, 프롬프트 노출은 IP 손실과 후속 침해의 출발점이 될 수 있음

## Ⅱ. 특징

- 단순한 텍스트 노출처럼 보여도 내부 정책과 도구 구조와 약점을 한 번에 드러낼 수 있음
- 프롬프트 인젝션과 결합되면 시스템 지시 자체를 추출하거나 재구성하는 공격이 쉬워짐
- few-shot 예시 안에 민감 정보가 들어가 있으면 개인정보 유출로도 바로 연결될 수 있음
- 방어는 가드레일만으로 끝나지 않고 비밀 분리와 출력 검증과 로그 모니터링이 함께 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Prompt Leakage | Prompt Injection | Model Extraction |
|:---|:---|:---|:---|
| 핵심 목표 | 시스템 지시와 예시 노출 | 모델 동작 탈취 | 모델 기능 복제 |
| 대표 피해 | IP 유출, 내부 규정 노출 | 정책 우회, 도구 오남용 | 상용 모델 도용 |
| 주 공격 수단 | 직접 요청, 재구성, 번역 | 명령 주입 | 대량 API 질의 |
| 방어 핵심 | secret separation, output scan | boundary, privilege control | query monitoring, watermark |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| System Prompt, Few-shot Examples | 서비스 동작을 정의하지만 노출 시 차별화 로직과 예시 데이터까지 함께 새어 나갈 수 있음 |
| Secret Separation Layer | 비밀값과 내부 자격 증명을 프롬프트 외부의 vault나 정책 저장소로 분리함 |
| Retrieval, Context Assembly | 내부 문서와 규정을 프롬프트에 합칠 때 과도한 노출이 일어나는 결합 지점임 |
| Output Sanitizer | 응답에 시스템 지시나 내부 키워드가 포함되는지 검사해 외부 노출을 막음 |
| Monitoring, Red Team | 유출 시도 패턴을 수집하고 유출 방어 품질을 반복적으로 점검함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Prompt / Example  | ---> | Secret Separation | ---> | Context Assembly  |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Output Sanitizer  |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 유출 유도 질의    | --> | 내부 지시 재노출  | --> | 응답 필터 통과 시도 | --> | 차단/로그/개선  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **유출 유도 질의**: 공격자가 시스템 지시나 예시를 묻는 변형 질문을 던짐
2. **내부 지시 재노출**: 모델이 시스템 맥락 일부를 응답 후보로 생성함
3. **응답 필터 통과 시도**: 번역과 재구성과 포맷 변경으로 차단을 우회하려 함
4. **차단과 로그 및 개선**: 탐지 결과를 가드레일과 프롬프트 구조 개선으로 연결함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 시스템 프롬프트에 내부 URL과 API 키와 예시 데이터 같은 비밀이 포함되면 유출 시 피해가 바로 인프라 침해로 확장될 수 있음
   - 해결방안: prompt secret separation과 vault 연동을 적용하고 hardcoded secret count와 secret exposure rate로 검증함
2. 문제: 출력 필터가 직접 표현만 막고 번역이나 재구성 요청은 놓치면 우회 유출이 반복될 수 있음
   - 해결방안: semantic output scanning과 similarity matching을 적용하고 prompt leakage detection rate와 bypass recurrence rate로 검증함
3. 문제: 내부 검색 문서를 그대로 프롬프트에 결합하면 시스템 지시가 아닌 운영 규정 문서에서도 민감 정보가 새어 나갈 수 있음
   - 해결방안: retrieval content classification과 least-context assembly를 적용하고 sensitive retrieval rate와 context minimization score로 검증함

## Ⅶ. 적용 사례

- 교육용 AI 튜터가 채점 규칙과 내부 예시를 프롬프트 외부 저장소로 분리해 운영되며 확인 지표는 prompt leakage detection rate와 response quality score임
- 사내 업무 봇이 시스템 지시 재출력 요청을 의미 기반으로 차단하며 확인 지표는 blocked leakage attempt rate와 false positive rate임
- 고객지원 챗봇이 few-shot 예시 내 개인정보를 제거한 뒤 배포되며 확인 지표는 sensitive example count와 PII exposure incident rate임

## Ⅷ. 결론

프롬프트 유출은 제품 로직과 내부 보안 정보를 동시에 노출할 수 있으므로 비밀 분리와 응답 검증을 기본 설계 원칙으로 삼아야 함.
