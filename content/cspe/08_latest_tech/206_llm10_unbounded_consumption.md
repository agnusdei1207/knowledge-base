---
title: "LLM10 Unbounded Consumption (LLM10 Unbounded Consumption)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 206
extra:
  question_no: "206"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM10은 요청 수보다 요청 하나가 소모하는 토큰과 연산 시간이 더 큰 위험이라는 점을 다룸
- 긴 입력과 과도한 출력과 에이전트 루프가 서비스 지연과 비용 폭증과 모델 남용을 동시에 유발함
- 토큰 예산과 시간 제한과 자율 루프 차단이 핵심 방어 수단임

## Ⅰ. 개요

- **정의/개념**: LLM10 Unbounded Consumption은 사용자가 과도한 입력 길이와 출력 요구와 반복 실행을 유도해 LLM 추론 자원과 API 예산을 무제한에 가깝게 소비하게 만들어 서비스 거부와 비용 손실을 일으키는 취약점임
- **배경/필요성**: 긴 컨텍스트와 에이전트 기능 확장으로 요청당 자원 소비 상한이 커지면서 전통적 QPS 제한만으로는 GPU와 토큰 비용을 보호하기 어려워짐

## Ⅱ. 특징

- 소수의 정교한 요청만으로도 GPU와 토큰 예산이 고갈될 수 있음
- 네트워크 DDoS와 달리 정상 사용자 요청처럼 보이는 무거운 프롬프트가 핵심 공격 수단임
- 비용 폭증과 응답 지연과 모델 추출 시도까지 함께 나타날 수 있음
- RPM보다 TPM과 max output token과 execution timeout이 더 중요한 제어 지표가 됨

## Ⅲ. 종류 및 비교

| 판단 기준 | LLM10 Unbounded Consumption | 전통적 DDoS | LLM06 Excessive Agency |
|:---|:---|:---|:---|
| 핵심 자원 | GPU, 토큰, 추론 시간 | 네트워크 대역폭, 세션 | 도구 권한과 자율성 |
| 공격 패턴 | long prompt, huge output, loop | 대량 패킷과 연결 | 승인 없는 실행 |
| 피해 유형 | 비용 폭증, 지연, 가용성 저하 | 접속 불가 | 파괴적 업무 실행 |
| 우선 대응 | quota, timeout, token cap | rate limit, CDN | approval gate, PoLP |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Request Gateway | 입력 길이와 사용자 등급과 요청 빈도를 1차 점검해 과도한 추론 요청을 앞단에서 제한하는 관문임 |
| Token Budget Manager | 사용자별 분당 토큰 사용량과 일일 예산을 추적해 과다 소비를 제어하는 정책 엔진임 |
| Inference Engine | 실제 모델 추론을 수행하며 긴 컨텍스트와 대량 출력에서 병목이 집중되는 자원 구간임 |
| Loop and Timeout Guard | 에이전트 반복 호출과 장기 실행을 감시해 무한 루프와 runaway task를 차단하는 안전 장치임 |
| Observability and FinOps | 지연과 GPU 점유와 비용 추이를 수집해 보안과 운영과 재무 통제를 연결하는 모니터링 계층임 |

```text
+-------------+    +----------------+    +----------------+    +----------------+
| User Request| -> | Gateway/Quota  | -> | Inference Engine| -> | Timeout/Monitor|
+-------------+    +----------------+    +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 요청 접수    | -> | 길이 점검    | -> | 예산 확인    | -> | 추론 수행    | -> | 시간/토큰 차단 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **요청 접수**: 사용자와 모델과 작업 종류를 식별함
2. **길이 점검**: 입력 토큰과 첨부 크기와 예상 출력 범위를 사전 계산함
3. **예산 확인**: 사용자와 서비스 정책에 맞는 토큰 쿼터와 시간 한도를 확인함
4. **추론 수행**: 허용된 요청만 모델 추론이나 도구 호출로 전달함
5. **시간 및 토큰 차단**: 임계치를 초과하면 즉시 중단하고 기록을 남김

## Ⅵ. 문제점 및 해결 방안

1. 문제: 장문의 입력과 고복잡도 프롬프트가 반복 유입되면 소수 요청만으로도 GPU와 메모리 자원이 빠르게 고갈될 수 있음
   - 해결방안: input token cap과 prompt compression과 tier based quota를 적용하고 gpu saturation time과 prompt rejection rate로 검증함
2. 문제: 출력 길이에 제한이 없으면 장문 생성과 반복 응답이 서비스 지연과 비용 폭증을 동시에 유발할 수 있음
   - 해결방안: max output tokens와 streaming cutoff policy를 적용하고 average output token count와 cost per request로 검증함
3. 문제: 에이전트가 도구 호출을 스스로 반복하면 정상 요청처럼 보이면서도 runaway loop가 장시간 지속될 수 있음
   - 해결방안: step limit과 loop detector와 execution timeout을 적용하고 average tool call depth와 runaway task rate로 검증함

## Ⅶ. 적용 사례

- 사내 AI 검색 서비스가 사용자 등급별 TPM 한도와 입력 길이 제한을 운영하며 확인 지표는 gpu saturation time과 quota breach rate임
- 코드 생성 도우미가 출력 토큰 상한과 실행 시간 제한을 적용하며 확인 지표는 average output token count와 timeout abort rate임
- 에이전트형 운영 자동화가 도구 호출 횟수와 루프 깊이를 제어하며 확인 지표는 average tool call depth와 runaway task rate임

## Ⅷ. 결론

LLM10은 가용성과 비용과 보안이 한 문제로 결합된 위험이므로 토큰 예산과 시간 제한과 루프 통제를 설계 초기부터 함께 넣어야 함.
