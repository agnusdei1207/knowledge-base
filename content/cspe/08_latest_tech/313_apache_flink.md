---
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 313
---

# 📖 【암기용】 개념 완전 이해

> 목적: Apache Flink를 unbounded/bounded stream을 상태 기반으로 처리하고 checkpoint로 장애복구하는 분산 스트림 처리 엔진으로 이해하게 만든다.

## 한눈에
- **개요**: 상태 기반 스트림·배치 처리를 지원하는 분산 데이터 처리 엔진
- **왜 필요한가**: 단순 이벤트 전달만으로는 window 집계, join, 세션 분석, 이상탐지처럼 이전 이벤트 상태를 기억하는 계산을 수행하기 어렵다.
- **핵심 직관**: 지나가는 물건을 즉시 세면서도 중간 집계 장부를 주기적으로 복사해 장애 후 같은 지점부터 다시 세는 계산 엔진임.

## 깊이 이해
- **배경·문제의식**: 실시간 분석은 이벤트 발생 시각 기준 window, late event, stateful join, 장애 후 중복 없는 복구가 필요하다.
- **작동 원리**: Flink는 source에서 stream을 읽고 operator graph로 처리하며 keyed state와 checkpoint를 저장하고 event time, watermark, state backend를 사용한다.
- **비유**: 마라톤 중간 기록 측정소가 주자별 기록을 계속 갱신하고, 정전이 나도 마지막 저장된 기록부터 이어서 측정하는 방식이다.
- **구체 예시**: Kafka 결제 이벤트를 Flink가 사용자별 10분 window로 집계하고, RocksDB state backend와 checkpoint로 장애 후 동일 offset과 state에서 재시작한다.
- **흔한 오해·주의점**: Flink는 Kafka 대체재가 아니다. Kafka는 이벤트 저장·전달, Flink는 상태 기반 계산과 변환을 담당한다.

## 연결 개념
- Checkpoint — 장애복구와 exactly-once state consistency 기반
- Watermark — event time 기준 window 완료 판단
- Exactly-Once Semantics — source/state/sink가 함께 맞아야 하는 보장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Flink는 event time, state, checkpoint, two-phase commit sink를 중심으로 stream processor 관점에서 답해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Flink는 bounded/unbounded data stream을 operator graph로 처리하는 stateful stream processing engine임.
> 2. **가치**: event time window, keyed state, checkpoint 기반 복구로 실시간 집계·탐지·CDC 변환을 일관되게 처리함.
> 3. **판단 포인트**: watermark, state backend, checkpoint interval, backpressure, sink transaction 지원이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스트림 처리 엔진 이해 확인 | stateful operator, event time, checkpoint | Kafka와 동일시 |
| 장애복구 판단 확인 | checkpoint, state backend, restart strategy | exactly-once를 단독 기능으로 단정 |
| 운영 설계 확인 | watermark, backpressure, state size | 처리량만 강조 |

> 요약: 이 문제는 Flink를 상태와 시간 기준을 관리하는 스트림 계산 엔진으로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 상태 기반 스트림 처리 엔진
- 배경: 실시간 집계와 탐지는 이전 이벤트 상태, event time 순서, late event, 장애복구를 함께 처리해야 함.
- 필요성: Kafka 같은 broker에 저장된 이벤트를 window·join·stateful logic으로 계산하려면 Flink 같은 processing engine이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Source -> Operator Graph -> Keyed State / State Backend -> Sink
        +-> Watermark / Event Time
        +-> Checkpoint Coordinator / Savepoint
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Connector | Kafka, file, CDC 등 입력 수집 | offset 연계 |
| Operator | map, window, join, aggregate 처리 | parallelism 설정 |
| State Backend | keyed/operator state 저장 | RocksDB, heap |
| Checkpoint | state와 source position의 일관된 snapshot | 장애복구 |

> 요약: Flink는 operator graph, state backend, checkpoint를 결합해 지속 실행되는 계산을 복구 가능하게 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
source event 수신 -> keyBy / window -> state 갱신
-> watermark로 window 완료 -> checkpoint barrier 정렬 -> sink commit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | source가 event와 offset을 읽음 | source lag |
| 2 | operator가 key별 state와 window를 갱신 | state size |
| 3 | checkpoint barrier가 state snapshot을 생성 | checkpoint duration |
| 4 | sink가 결과를 commit하고 장애 시 checkpoint에서 복구 | recovery point |

> 요약: Flink는 event time 계산과 checkpoint snapshot을 결합해 상태 기반 스트림 처리를 복구한다.

---

## Ⅳ. 특징

| 구분 | Kafka Streams | Apache Flink | 판단 기준 |
|:---|:---|:---|:---|
| 실행 모델 | 애플리케이션 라이브러리 | 분산 처리 클러스터 | 운영 규모 |
| 상태 관리 | 로컬 state store | 분산 state backend | state 크기 |
| 시간 처리 | stream app 중심 | event time·watermark 내장 | late event 복잡도 |
| 사용 범위 | Kafka 중심 | Kafka 외 source/sink 다수 | 다중 시스템 연계 |

> 요약: Flink는 대규모 상태와 복잡한 event-time 처리가 필요한 스트리밍 계산에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 처리 요구 | stateless consumer | stateful Flink job | window·join·session 필요 |
| 복구 모델 | offset 재처리 | checkpoint+state restore | 중복 허용 수준 |
| 운영 | 단일 서비스 | cluster/job manager/task manager | 팀 운영 역량 |

> 요약: 단순 변환은 consumer로 충분하지만, 대규모 stateful 계산과 event time 처리는 Flink를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| backpressure | sink 지연·operator 병목 | parallelism 조정, sink 튜닝 | backpressure ratio |
| checkpoint 실패 | state 과대·스토리지 지연 | interval 조정, incremental checkpoint | checkpoint failure |
| state 폭증 | key cardinality 증가 | TTL, state compaction | state size |

> 요약: Flink 운영 리스크는 backpressure, checkpoint, state size를 핵심 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | 업무 p95 latency SLA 충족 | Flink metrics |
| 복구 | checkpoint 기반 failover 성공 | chaos test |
| 처리 보장 | sink transaction 또는 idempotent 처리 확인 | duplicate/loss audit |

> 요약: Flink 성과는 처리량보다 상태 복구와 end-to-end 결과 정확성으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. event time, watermark, allowed lateness, window 정책을 데이터 지연 특성에 맞게 정의함.
2. state backend, checkpoint interval, checkpoint storage, restart strategy를 job 중요도와 state 크기에 맞게 설정함.
3. sink가 transaction을 지원하지 않으면 idempotent write key와 deduplication table을 설계함.

**결론 (2줄):**
- 기술사 판단: 상태가 큰 실시간 집계와 event-time 처리가 필요하면 Flink가 적합하고, 단순 이벤트 전달은 Kafka consumer가 단순함.
- 향후 방향: Flink는 CDC, lakehouse streaming write, 실시간 feature engineering, AI monitoring 파이프라인으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Apache Flink를 설명하시오" | state, watermark, checkpoint 흐름 | Kafka Streams 대비 차이 |
| 요구사항 명시형 | "스트림 처리 장애복구 방안을 제시하시오" | checkpoint와 sink commit 설계 | backpressure·state 폭증 대응 |

> 요약: 설명형은 처리 엔진 구조를, 방안형은 checkpoint와 상태 운영을 중심으로 작성한다.
