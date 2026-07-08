---
title: "TTFT (최초 토큰 지연)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 61
extra:
  question_no: "061"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- TTFT는 요청 시점부터 첫 토큰이 사용자에게 도달할 때까지의 전체 지연 시간임
- Prefill은 입력 프롬프트 전체를 처리하는 초기 연산 단계로 TTFT의 핵심 병목임
- Queue Delay는 요청이 실행되기 전 스케줄러와 자원 대기열에서 소비되는 시간임

## Ⅰ. 개요

- **정의/개념**: TTFT(Time To First Token)는 사용자가 요청을 보낸 시점부터 모델이 첫 번째 출력 토큰을 반환할 때까지 걸리는 지연 시간으로, LLM 서비스의 초기 반응성을 나타내는 핵심 UX 지표임
- **배경/필요성**: 긴 프롬프트와 대기열과 무거운 prefill 연산이 겹치면 사용자는 응답이 멈췄다고 느끼기 쉬우므로, 첫 토큰 지연을 줄이는 것은 모델 정확도 못지않게 중요한 서비스 품질 조건임

## Ⅱ. 특징

- 프롬프트 길이, queue 대기, prefill 커널 성능의 영향을 직접 받음
- 사용자가 체감하는 응답성에 가장 큰 영향을 주므로 이탈률과 만족도와 연결됨
- decode 속도와는 별개 지표이므로 TTFT와 TPOT을 분리 측정해야 함
- Prefix Caching, chunked prefill, flash attention의 효과를 평가하는 대표 기준임

## Ⅲ. 종류 및 비교

| 판단 기준 | 짧은 프롬프트 TTFT | 긴 프롬프트 TTFT | 캐시 적중 TTFT |
|:---|:---|:---|:---|
| 주 병목 | 네트워크, 큐 오버헤드 | prefill 연산 | queue와 잔여 연산 |
| 절감 수단 | 경량 모델, 빠른 스케줄 | flash attention, chunking | prefix caching |
| 사용자 체감 | 즉각 응답 | 멈춤처럼 보일 수 있음 | 가장 빠름 |
| 적합 업무 | 일반 대화 | 장문 요약, RAG | 반복 질의 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Network, Request Handler | 요청 수신과 토큰화 전처리를 수행하며 초기 고정 오버헤드를 형성함 |
| Queue Scheduler | GPU 슬롯이 비기 전까지 요청을 대기시키며 혼잡 시 TTFT를 크게 늘릴 수 있음 |
| Prefill Engine | 전체 프롬프트를 처리해 초기 KV cache를 만드는 가장 무거운 계산 구간임 |
| First-token Sampler | prefill 이후 첫 토큰을 선택해 스트리밍을 시작하며 TTFT 종료 지점을 형성함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 수신    | --> | 큐 대기      | --> | Prefill 수행  | --> | 첫 토큰 반환 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 수신**: 입력 문자열을 받아 토큰화와 기본 검증을 수행함
2. **큐 대기**: 현재 자원 상태에 따라 요청이 실행 대기열에서 대기함
3. **Prefill 수행**: 전체 프롬프트를 처리해 attention 상태와 KV cache를 생성함
4. **첫 토큰 반환**: 첫 번째 샘플링 결과를 사용자에게 스트리밍하며 TTFT를 기록함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 긴 프롬프트와 장문맥 요청이 많아지면 prefill 시간이 길어져 사용자가 응답 불능처럼 느낄 수 있음
   - 해결방안: prefix caching과 flash attention과 chunked prefill을 적용하고 prompt length별 TTFT로 효과를 검증함
2. 문제: 대형 prefill 요청이 기존 디코딩 요청을 가로막으면 전체 서비스 TTFT와 TPOT이 함께 악화될 수 있음
   - 해결방안: prefill과 decode를 분리 스케줄링하고 active session TPOT과 p95 TTFT로 간섭 완화 여부를 검증함
3. 문제: 평균 TTFT만 보면 일부 극단 지연 요청을 놓쳐 실제 사용자 경험 문제를 숨길 수 있음
   - 해결방안: p95, p99 기준으로 모니터링하고 timeout rate와 abandonment rate로 체감 품질을 검증함

## Ⅶ. 적용 사례

- 일반 챗봇: 첫 반응 속도를 유지해 사용자 이탈을 줄임, 확인 지표는 p95 TTFT와 session retention임
- 장문 문서 분석: 대용량 prefill 최적화를 평가함, 확인 지표는 prompt length별 TTFT임
- 실시간 음성, 멀티모달 서비스: 지연 허용치가 낮은 환경을 운영함, 확인 지표는 end-to-end latency와 user drop rate임

## Ⅷ. 결론

TTFT는 단순한 속도 숫자가 아니라 prefill과 큐 병목을 드러내는 서비스 반응성 지표이므로, 긴 문맥 서비스를 설계할수록 p95, p99 기준으로 적극 관리해야 함.
