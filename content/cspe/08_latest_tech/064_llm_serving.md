---
title: "LLM Serving LLM 서빙 (LLM Serving)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 64
extra:
  question_no: "064"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM Serving은 학습된 모델을 API나 애플리케이션 형태로 안정적으로 제공하는 추론 운영 계층임
- Prefill과 Decode는 서빙 병목이 서로 다른 두 주요 연산 단계임
- Scheduler, cache manager, execution engine은 서빙 엔진의 핵심 구성요소임

## Ⅰ. 개요

- **정의/개념**: LLM Serving은 학습된 대규모 언어모델을 실시간 또는 배치 방식으로 요청에 응답하도록 배포하고, 스케줄링과 메모리와 병렬 실행과 스트리밍을 관리하는 추론 운영 체계임
- **배경/필요성**: LLM은 단순 웹 API와 달리 거대한 가중치와 KV cache와 토큰 단위 반복 실행을 요구하므로, 일반 서빙 스택만으로는 비용과 지연과 OOM을 통제하기 어려워 전용 추론 아키텍처가 필요함

## Ⅱ. 특징

- 모델 품질만이 아니라 TTFT, TPOT, throughput 같은 운영 지표를 함께 관리해야 함
- GPU 메모리와 스케줄링 효율이 서비스 비용을 크게 좌우함
- 실시간 챗봇과 오프라인 배치 분석은 서로 다른 서빙 정책이 필요함
- continuous batching, paged attention, prefix caching, tensor parallelism 같은 특화 기법이 필수적으로 결합됨

## Ⅲ. 종류 및 비교

| 판단 기준 | 일반 웹 서빙 | 단순 모델 서빙 | LLM 전용 서빙 |
|:---|:---|:---|:---|
| 상태 관리 | 대부분 stateless | 짧은 추론 상태 | 긴 KV cache 상태 유지 |
| 핵심 병목 | CPU, DB, 네트워크 | CPU, GPU 연산 | GPU 메모리와 스케줄링 |
| 처리 단위 | request | request | token iteration |
| 대표 도구 | Nginx, Spring | Triton 등 | vLLM, TGI, TensorRT-LLM |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| API Frontend | OpenAI 호환 인터페이스나 내부 RPC를 제공해 요청을 수신하고 인증과 제한 정책을 적용함 |
| Scheduler | 요청 우선순위와 continuous batching을 관리해 GPU 자원을 효율적으로 배분함 |
| Cache, Memory Manager | KV cache와 prefix cache와 paging을 통제해 OOM과 파편화를 줄임 |
| Execution Engine | attention kernel과 병렬 실행과 스트리밍 출력을 담당하는 GPU 실행 계층임 |

```text
+------------------+     +------------------+     +------------------+     +------------------+
| API Frontend     | --> | Scheduler        | --> | Cache/Memory Mgr | --> | Execution Engine |
+------------------+     +------------------+     +------------------+     +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 수신    | --> | 배치/우선순위 | --> | 모델 실행    | --> | 스트리밍 반환 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 수신**: 인증과 rate limit을 포함해 사용자 요청을 받아 큐에 적재함
2. **배치 및 우선순위 결정**: 요청 길이와 정책에 따라 prefill과 decode 실행 순서를 정함
3. **모델 실행**: GPU에서 토큰 생성과 cache 관리와 병렬 연산을 수행함
4. **스트리밍 반환**: 토큰 단위 또는 완료 응답을 사용자나 후속 시스템에 반환함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 긴 프롬프트와 많은 동접 요청이 겹치면 GPU 메모리와 큐 지연이 급증해 SLA와 비용이 동시에 무너질 수 있음
   - 해결방안: paged attention과 continuous batching과 request cap을 적용하고 OOM rate와 p95 latency로 운영성을 검증함
2. 문제: 실시간 사용자 요청과 대형 배치 작업을 같은 자원 풀에서 섞어 처리하면 둘 다 지연이 커질 수 있음
   - 해결방안: interactive와 batch 워크로드를 분리하거나 우선순위를 차등 적용하고 latency SLA와 batch completion time으로 정책을 검증함
3. 문제: 모델, 프레임워크, GPU 아키텍처 조합이 바뀌면 동일 설정으로는 예상 성능이 나오지 않을 수 있음
   - 해결방안: 조합별 benchmark와 canary 배포를 수행하고 throughput과 cost per token으로 배포 구성을 검증함

## Ⅶ. 적용 사례

- 사내 챗봇 플랫폼: 인증과 검색과 LLM 응답을 통합 운영함, 확인 지표는 SLA 준수율과 cost per request임
- 개발자 코파일럿: 코드 생성과 리뷰를 실시간 제공함, 확인 지표는 TTFT와 acceptance rate임
- 배치형 문서 요약: 밤 시간대 오프라인 분석을 수행함, 확인 지표는 tokens/sec와 batch completion time임

## Ⅷ. 결론

LLM Serving의 본질은 모델을 띄우는 데 있지 않고 토큰 단위 실행과 메모리 병목과 사용자 경험을 함께 제어해 실제 서비스를 안정적으로 운영하는 데 있음.
