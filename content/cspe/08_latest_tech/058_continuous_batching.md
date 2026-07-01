---
title: "연속 배칭 (Continuous Batching)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 58
---

# 📖 【암기용】 개념 완전 이해

> 목적: Continuous Batching을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: LLM 서빙 중 완료된 요청은 즉시 배치에서 제거하고 새 요청을 계속 넣는 동적 배칭 방식
- **왜 필요한가**: 생성 길이가 요청마다 달라 고정 배치는 짧은 요청이 끝나도 긴 요청 때문에 GPU 자리가 비는 문제가 생김.
- **핵심 직관**: 버스가 종점까지 한 번에 가는 것이 아니라, 정류장마다 내린 사람 자리에 새 승객을 태우는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM decode는 토큰 단위 반복 작업임. 고정 배칭은 배치 내 가장 긴 출력에 맞춰 진행되어 짧은 요청의 자원이 낭비됨.
- **작동 원리**: 스케줄러가 매 decode step마다 active sequence를 재구성함. 종료된 sequence의 KV block을 반환하고, 대기열의 새 요청을 prefill 또는 decode batch에 삽입함.
- **비유**: 식당 좌석 회전처럼 식사가 끝난 자리를 바로 다음 손님에게 배정해 좌석 공백을 줄이는 것과 같음.
- **구체 예시**: 짧은 질의 50토큰과 긴 질의 500토큰이 섞인 트래픽에서 continuous batching은 GPU 유휴 시간을 줄여 req/s를 높임.
- **흔한 오해·주의점**: 배치를 계속 키우면 지연이 줄어드는 것이 아님. 과도한 배치는 대기시간과 tail latency를 증가시킴.

## 연결 개념
- LLM Serving — Continuous Batching 적용 영역
- PagedAttention — 가변 sequence KV 관리 기반
- TTFT/TPOT — 배칭 정책으로 영향을 받는 지연 지표


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Continuous Batching은 decode step마다 active request를 재구성하는 LLM 동적 배칭 스케줄링임.
> 2. **가치**: 출력 길이 편차로 인한 GPU 유휴 시간을 줄여 req/s와 토큰 처리량을 높임.
> 3. **판단 포인트**: batch size, queue delay, prefill/decode 분리, tail latency가 운영 기준임.


## Ⅰ. 개요 및 필요성

Continuous Batching은 LLM 동적 배치 처리 방식임. 요청별 생성 길이가 다른 LLM 서빙에서 고정 배치의 자원 낭비를 줄이기 위해, 완료 요청을 즉시 제거하고 새 요청을 배치에 투입함.


## Ⅱ. 구조 및 구성요소

```text
Request Queue → Scheduler → Active Decode Batch
      ▲              │              │
      └── New Req ◀──┴── Finished Req 제거
                     │
              KV Cache Manager
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Request Queue | 대기 요청 보관 | priority, timeout |
| Scheduler | 매 step 배치 재구성 | prefill/decode 분리 |
| Active Batch | 현재 decode 중 sequence 집합 | 길이·상태 가변 |
| KV Manager | 종료 요청 cache 반환 | PagedAttention과 결합 |

> 요약: 스케줄러가 요청 큐와 active batch를 토큰 step마다 조정해 GPU 공백 시간을 줄임.


## Ⅲ. 동작원리 및 흐름도

```text
요청 유입 → prefill batch 편성 → decode step 실행
    → 완료 요청 제거 → 신규 요청 삽입 → 다음 decode step
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 신규 요청 큐 적재·우선순위 설정 | queue length, wait time |
| 2 | prefill과 decode 작업 스케줄링 | TTFT, GPU utilization |
| 3 | decode step마다 완료 sequence 제거 | finished/request ratio |
| 4 | 빈 slot에 신규 sequence 삽입 | tokens/s, p95 latency |

> 요약: Continuous Batching은 batch를 요청 단위가 아니라 토큰 step 단위로 재편성해 처리량과 지연을 조정함.


## Ⅳ. 특징

| 구분 | Static Batching | Continuous Batching | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 배치 구성 | 시작 시 고정 | step마다 변경 | active sequence 동적 |
| 자원 활용 | 짧은 요청 종료 후 공백 | slot 즉시 재사용 | GPU utilization 상승 |
| 지연 특성 | batch 대기 증가 | queue 정책 영향 | p95/p99 감시 |
| 구현 조건 | 단순 | KV 동적 관리 필요 | PagedAttention 적합 |

> 요약: Continuous Batching은 혼합 길이 트래픽에서 처리량을 높이나, 대기열 정책이 tail latency를 좌우함.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. vLLM/TGI 등 dynamic batching 지원 엔진을 적용하고 tokens/s, req/s, p95 TTFT를 배포 전후 비교
2. prefill 우선순위와 decode 우선순위를 분리해 긴 프롬프트가 짧은 대화형 요청을 막지 않게 조정
3. max batch token, max waiting time(예: 20~50ms), priority queue로 처리량과 tail latency 균형 설정

**결론 (2줄):**
- 기술사 판단: 요청 길이 편차가 큰 대화형 LLM API는 Continuous Batching, 오프라인 일괄 작업은 Static Batching을 선택함.
- 향후 방향: SLA-aware scheduler가 요청 유형별 TTFT·TPOT 목표에 따라 배치를 자동 조정함.


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | step 단위 배치 재구성 흐름 | Static 대비 처리량·지연 |
| 요구사항 명시형 | 운영 방안을 제시하시오 | queue·priority·batch token 설정 | p95 지연·tokens/s 선택 기준 |

> 요약: 설명형은 동적 배치 원리, 운영형은 스케줄러 파라미터와 SLA 지표 중심으로 목차를 전환함.
