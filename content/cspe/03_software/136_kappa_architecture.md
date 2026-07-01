---
title: "카파 아키텍처 (Kappa Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 136
---

# 📖 【암기용】 개념 완전 이해

> 목적: 카파 아키텍처가 람다 아키텍처의 어떤 운영 문제를 줄이는지 이해하게 만든다.

## 한눈에
- **개요**: batch layer 없이 stream processing과 event log replay로 처리하는 데이터 아키텍처
- **왜 필요한가**: 람다 아키텍처는 batch와 speed에 같은 로직을 두 번 구현해 결과 불일치와 운영 부담이 생김.
- **핵심 직관**: 모든 장부 원본을 순서대로 보관해 두고, 계산식이 바뀌면 처음부터 다시 재생하는 방식임.

## 깊이 이해
- **배경·문제의식**: Kafka 같은 durable log가 등장하면서 과거 이벤트를 장기간 보존하고 replay할 수 있게 됨. 카파는 단일 stream processing 로직으로 실시간 처리와 재처리를 모두 수행함.
- **작동 원리**: 이벤트를 append-only log에 저장하고 stream processor가 consumer offset부터 읽어 state를 갱신함. 로직 변경 시 새 consumer group으로 처음부터 replay해 새로운 view를 생성함.
- **비유**: CCTV 원본 영상을 보관해 두고, 새로운 분석 규칙이 생기면 같은 영상을 처음부터 다시 돌려 결과를 만드는 방식임.
- **구체 예시**: Kafka topic 7일 보존과 Flink job savepoint를 사용해 클릭 집계 로직을 변경한 뒤 새 job이 earliest offset부터 replay함.
- **흔한 오해·주의점**: 카파는 batch가 전혀 필요 없는 만능 구조가 아님. 수년치 재처리나 대규모 backfill은 log 보존 비용과 replay 시간이 제약이 됨.

## 연결 개념
- Lambda Architecture — 비교 대상
- Apache Kafka — durable event log
- Apache Flink — stateful stream processing

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Kappa Architecture 문제에서 stream-only 구조, replay, state 관리, Lambda 대비 선택 기준을 제시함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 카파 아키텍처는 immutable event log와 stream processor만으로 실시간 처리와 재처리를 수행하는 구조임.
> 2. **가치**: batch/speed 이중 로직을 제거해 결과 불일치와 운영 경로 수를 줄임.
> 3. **판단 포인트**: log retention, replay 시간, state size, exactly-once 보장을 기준으로 적용 여부를 판단함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Lambda 대안 이해 확인 | stream-only, event log, replay | batch layer 제거만 쓰고 재처리 원리 누락 |
| stream 처리 설계 확인 | offset, state store, checkpoint | state 복구와 exactly-once 누락 |
| 적용 한계 판단 확인 | retention 비용, replay SLA | 모든 데이터 웨어하우스 대체로 서술 |

> 요약: 카파 답안은 단일 stream 로직의 장점과 replay·state 운영 제약을 함께 써야 함.

---

## Ⅰ. 개요 및 필요성

카파 아키텍처는 스트림 중심 데이터 처리 구조임. 람다 아키텍처의 batch/speed 이중 구현은 코드 불일치와 운영 비용을 만든다. 카파는 immutable event log와 stream processor replay로 실시간 처리와 재처리를 하나의 경로로 통합함.

---

## Ⅱ. 구조 및 구성요소

```text
Event Source -> Durable Log -> Stream Processor -> State Store -> Serving View
                         / Replay from Offset -> New Processor -> New View
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Durable Log | 이벤트 순서·보존 | Kafka retention, compaction |
| Stream Processor | 연속 처리 | Flink, Kafka Streams |
| State Store | 집계 상태 저장 | checkpoint와 snapshot 필요 |
| Serving View | 조회용 결과 제공 | materialized view, OLAP store |

> 요약: 카파는 event log를 원본으로 삼고 stream processor와 state store가 실시간 view와 재처리 view를 생성함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 수집 -> log append -> processor consume -> state update
-> checkpoint 저장 -> serving view 갱신 -> 필요 시 offset replay
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이벤트를 log에 append | partition key, retention |
| 2 | processor가 offset 순서로 consume | consumer lag |
| 3 | state와 view 갱신 | checkpoint interval |
| 4 | 로직 변경 시 replay 수행 | replay 완료 시간, 결과 diff |

> 요약: 카파의 재처리는 batch job이 아니라 event log를 다시 읽는 stream job으로 수행됨.

---

## Ⅳ. 특징

| 구분 | Lambda Architecture | Kappa Architecture | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 처리 경로 | batch+speed 2개 | stream 1개 | 코드 경로 1개 |
| 재처리 | batch recompute | log replay | retention 7~90일 정책 |
| 최신성 | speed layer | stream processor | end-to-end lag 5초 이하 |
| 한계 | 로직 중복 | 대규모 replay 비용 | replay SLA 4시간 이하 |

> 요약: 카파는 운영 경로를 줄이지만, 장기 보존·대용량 재처리 요구가 크면 람다 또는 lakehouse batch를 병행함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Lambda 이중 경로 | 단일 stream 경로 | 동일 로직 재사용 요구가 큰 경우 |
| 비용/성능 | batch cluster 추가 | log retention·state 비용 | replay 데이터량과 보존기간 |
| 운영/위험 | 결과 병합 복잡 | state 복구 복잡 | checkpoint, savepoint 운영 역량 |

> 요약: 카파는 이벤트 중심 서비스에 적합하고, 규제상 장기 확정 재계산이 필요하면 batch 계층을 보완함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| replay 지연 | topic 보존량 증가 | parallelism 증설, compacted topic | replay 완료 4시간 이하 |
| state 손상 | checkpoint 실패 | savepoint, dual run 검증 | checkpoint success 99.9% |
| 순서 오류 | partition key 설계 오류 | entity_id key 고정 | out-of-order rate |

> 요약: 카파 리스크는 replay와 state이며, checkpoint 성공률과 replay SLA로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리 지연 | consumer lag 1000건 이하 | Kafka/Flink metrics |
| 상태 복구 | checkpoint 복구 5분 이하 | failure drill |
| 결과 검증 | old/new view diff 0.1% 이하 | dual run reconciliation |

> 요약: 카파 도입 효과는 lag, 복구 시간, replay 결과 차이로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Kafka topic은 entity_id 기준 partition key와 retention 30일 이상을 설정해 replay 범위를 보장함
2. Flink savepoint 기반 배포 절차를 표준화하고 checkpoint interval 30초, state backend를 RocksDB로 구성함
3. 로직 변경 시 old/new processor를 병행 실행해 view diff 0.1% 이하 확인 후 traffic을 전환함

**결론 (2줄):**
- 기술사 판단: 이벤트 보존과 replay SLA가 충족되면 Kappa, 장기 확정 재계산과 대규모 backfill이 필수면 Lambda를 선택함
- 향후 방향: stream-table duality와 lakehouse streaming table 확산으로 batch와 stream 경계가 줄어듦

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "카파 아키텍처를 설명하시오" | log append, state update, replay 흐름 | Lambda 대비 단일 경로 |
| 요구사항 명시형 | "Lambda와 비교하시오", "설계하시오" | retention, offset replay, checkpoint | replay SLA와 state 리스크 |

> 요약: 설명형은 stream-only 원리, 비교형은 Lambda 대비 운영 경로와 재처리 제약 중심으로 작성함.
