---
title: "Model DoS 모델 서비스거부 (Model Denial of Service)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 195
extra:
  question_no: "195"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- Model DoS는 네트워크 대역폭보다 모델 추론 비용과 토큰 소비를 겨냥하는 애플리케이션 계층 공격임
- LLM은 긴 입력과 긴 출력과 에이전트 루프에서 자원 소모가 급격히 커질 수 있음
- RPM보다 TPM과 GPU time 같은 모델 자원 지표가 더 중요한 방어 기준이 됨

## Ⅰ. 개요

- **정의/개념**: Model DoS는 공격자가 계산 비용이 큰 입력과 장문 출력 유도와 도구 루프를 활용해 모델 추론 자원과 비용을 고갈시키고 서비스 응답을 지연·중단시키는 공격임
- **배경/필요성**: 생성형 AI는 적은 요청 수로도 GPU와 토큰 예산을 크게 소모할 수 있으므로, 전통적 네트워크 DDoS 방어만으로는 서비스 가용성과 과금 리스크를 충분히 막기 어려움

## Ⅱ. 특징

- 저용량 요청만으로도 고비용 연산을 유발하는 비대칭 공격이라는 점이 핵심임
- 긴 컨텍스트와 과도한 출력과 에이전트 반복 호출이 주요 공격 수단임
- 가용성 저하와 함께 종량제 환경에서는 경제적 손실을 동반함
- 네트워크 보안 솔루션보다 AI 게이트웨이와 자원 예산 관리가 중요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Input Flooding | Output Expansion | Tool, Agent Loop |
|:---|:---|:---|:---|
| 자원 타깃 | 컨텍스트 메모리 | 생성 시간과 토큰 | 외부 API와 오케스트레이션 |
| 공격 방식 | 긴 입력 채우기 | 장문 출력 유도 | 반복 행동 루프 |
| 대표 피해 | VRAM 압박 | GPU 점유 증가 | 비용 폭증, 응답 지연 |
| 방어 핵심 | max context cap | max output cap | step limit, tool quota |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| AI Gateway | 사용자 요청을 받아 토큰과 비용과 정책 한도를 먼저 평가하는 보호 관문임 |
| Costly Prompt, Context | 긴 입력과 복잡한 지시가 모델 자원 소모를 급증시키는 공격 재료임 |
| Inference Engine | GPU와 KV cache와 스케줄러가 실제 병목이 발생하는 실행 계층임 |
| Tool Orchestrator | 에이전트가 외부 검색과 함수 호출을 반복하며 추가 비용을 발생시키는 계층임 |
| Budget, Timeout Control | TPM과 max tokens와 timeout과 circuit breaker로 서비스 고갈을 방지함 |

```text
+-------------------+      +-------------------+      +-------------------+
| AI Gateway        | ---> | Inference Engine  | ---> | Tool Orchestrator |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Budget / Timeout  |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 고비용 요청 생성  | --> | 긴 추론/생성 유발 | --> | 자원 장기 점유  | --> | 응답 지연/차단  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **고비용 요청 생성**: 공격자가 긴 입력이나 반복형 지시를 만듦
2. **긴 추론 및 생성 유발**: 모델이 과도한 토큰과 계산을 소모함
3. **자원 장기 점유**: GPU와 툴 호출 슬롯이 묶여 정상 요청이 밀림
4. **응답 지연 및 차단**: 가용성 저하와 비용 상승이 발생함

## Ⅵ. 문제점 및 해결 방안

1. 문제: RPM만 제한하고 토큰과 출력 길이를 통제하지 않으면 적은 요청으로도 비용이 큰 추론이 계속 실행될 수 있음
   - 해결방안: token-based quota와 max output cap을 적용하고 TPM exceed rate와 cost per request로 검증함
2. 문제: 에이전트가 외부 도구를 반복 호출하는 구조에서는 모델 한도와 별개로 서드파티 API 비용과 지연이 폭증할 수 있음
   - 해결방안: step budget과 tool call limit를 적용하고 average tool calls per task와 loop abort rate로 검증함
3. 문제: 비정상적으로 무거운 요청이 동일한 실행 풀을 공유하면 정상 사용자의 지연이 급격히 증가할 수 있음
   - 해결방안: priority queue와 workload isolation을 적용하고 P99 latency와 heavy-request containment rate로 검증함

## Ⅶ. 적용 사례

- 기업 RAG 챗봇이 긴 문서 전체 요약 요청을 제한하고 운영되며 확인 지표는 TPM exceed rate와 P99 latency임
- 코딩 에이전트가 무한 도구 루프를 방지하도록 step budget을 적용하며 확인 지표는 loop abort rate와 task completion rate임
- 공개 LLM API가 비용형 rate limit과 circuit breaker를 사용해 운영되며 확인 지표는 GPU utilization stability와 monthly cost variance임

## Ⅷ. 결론

Model DoS는 트래픽 양보다 추론 비용과 토큰 소비를 겨냥하는 공격이므로 AI 게이트웨이 기반의 비용·자원 통제가 필수 방어 수단이 됨.
