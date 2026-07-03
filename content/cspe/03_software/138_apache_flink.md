---
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 138
---

# 📖 【암기용】 개념 완전 이해

> 목적: Flink가 Spark Streaming과 비교되는 지점인 stateful stream processing을 이해하게 만든다.

## 한눈에
- **개요**: Apache Flink는 **이벤트 시간**(Event Time) 처리와 **상태 저장 연산**(Stateful Processing)을 지원하는 분산 **스트림 처리 엔진**(Stream Processing Engine)이다 — 데이터를 배치로 묶지 않고 레코드 단위로 연속 처리하면서, 장애가 나도 정확히 복구할 수 있도록 상태를 주기적으로 저장한다.
- **왜 필요한가**: 마이크로배치(예: 초기 Spark Streaming)는 배치 간격만큼 지연이 누적되고, 이벤트가 발생한 시각과 처리된 시각이 뒤섞이면 집계가 틀어진다. Flink는 이벤트에 찍힌 시각(event time)을 기준으로 순서를 재구성해, 네트워크 지연으로 뒤섞여 도착한 이벤트도 올바른 윈도우에 집계한다.
- **핵심 직관**: 컨베이어벨트 위 물건을 하나씩 보는 즉시 계산하되, 계산 중간 결과(장부)를 몇십 초마다 금고(체크포인트)에 저장해 정전이 나도 마지막 금고 시점부터 이어서 계산하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 스트림 처리 엔진 | 무한히 들어오는 데이터를 레코드 단위로 끊김없이 처리하는 엔진 — Flink가 속하는 상위 분류 | 공장의 연속 생산 라인 |
| 이벤트 시간(Event Time) | 이벤트가 실제로 "발생한" 시각(데이터 안에 기록된 타임스탬프) | 편지에 적힌 "작성일" |
| 처리 시간(Processing Time) | 이벤트가 엔진에 "도착해 처리된" 시각 | 편지가 "도착한 날" |
| 워터마크(Watermark) | "이 시각 이전 이벤트는 이제 다 도착했다"고 선언하는 진행 표시선 | 우체국이 "이 날짜 이전 우편은 마감"이라 공표하는 것 |
| 키드 스테이트(Keyed State) | key(예: user_id)별로 독립 유지되는 중간 계산 값 | 고객별 개인 장부 |
| 상태 백엔드(State Backend) | 상태 저장 위치 — 메모리(Heap) 또는 디스크 기반 RocksDB | 장부를 책상 서랍(메모리)에 둘지 창고(디스크)에 둘지 |
| 체크포인트(Checkpoint) | 상태 + 소스 오프셋을 일관된 시점으로 스냅샷 저장 | 게임의 자동 저장 지점 |
| 체크포인트 배리어(Barrier) | 체크포인트 시작을 알리며 스트림에 끼워 넣는 특수 마커 | 생산 라인에 꽂는 "여기까지 검수 완료" 깃발 |
| 세이브포인트(Savepoint) | 사람이 수동으로 트리거하는 체크포인트 — 버전 업그레이드·재배포에 사용 | 이사 전에 일부러 찍어두는 사진 |
| 윈도우(Window) | 스트림을 일정 시간·개수 단위로 잘라 집계하는 구간 | 1분마다 끊어 찍는 CCTV 클립 |

## 깊이 이해

### 왜 이런 구조가 필요했나 — 마이크로배치의 한계
- 초기 스트림 처리는 처리 시간(도착 순서) 기준으로 집계했다. 문제는 네트워크 지연으로 이벤트가 늦게 도착하면 실제 발생 시각과 무관하게 잘못된 시점에 집계된다는 점이다. 예: 11:00:59에 발생한 결제가 네트워크 지연으로 11:01:05에 도착하면, 처리 시간 기준에서는 11:01대 매출로 잘못 잡힌다.
- Flink는 이벤트 자체의 event_time 필드로 윈도우를 나누고, "이 시각까지는 이벤트가 다 도착했다"를 워터마크로 선언해 이 문제를 해결한다.

### 워터마크로 지연 도착을 다루는 법 — 수치 예제
- 대표적 계산식: watermark = 지금까지 관측한 최대 event_time − 허용 지연(allowed lateness).
- 예: 허용 지연 1분. 지금까지 본 최대 event_time이 11:05:40이면 워터마크는 11:04:40이다. [11:00, 11:01) 윈도우는 워터마크가 11:01을 지나야(최대 event_time이 11:02 이후가 되어야) 결과를 확정(fire)한다.
- 그 사이 11:00:55에 발생했지만 11:03에야 도착한 이벤트가 있어도, 워터마크가 아직 11:01을 넘지 않았다면 [11:00,11:01) 윈도우에 정상 반영된다. 허용 지연을 넘겨 도착한 이벤트는 버리거나(drop) side output으로 별도 수집한다.
- 허용 지연을 짧게 잡으면(예: 5초) 결과 확정은 빨라지지만 늦은 이벤트 유실이 늘고, 길게 잡으면(예: 5분) 정확도는 오르되 결과 확정이 그만큼 늦어진다 — 이 트레이드오프가 워터마크 설계의 핵심이다.

### 체크포인트로 장애를 복구하는 법 — 배리어 정렬
- JobManager(Checkpoint Coordinator)가 일정 간격(예: 30초)마다 소스에 체크포인트 배리어를 주입한다. 배리어는 실제 데이터 레코드와 함께 스트림을 따라 흐른다.
- 각 연산자는 모든 입력 채널에서 배리어를 받으면(정렬, alignment) 그 시점의 keyed state를 스냅샷으로 저장하고 배리어를 다음 연산자로 전달한다. 모든 연산자가 스냅샷을 마치면 하나의 체크포인트가 완료된다.
- 장애 발생 시 Flink는 가장 최근에 완료된 체크포인트의 상태와 소스 오프셋(예: Kafka offset 128,304)으로 job을 되돌린 뒤, 그 오프셋부터 이벤트를 재생(replay)한다. 체크포인트 간격이 30초면 최악의 경우 최근 30초치 이벤트만 재처리하면 된다.
- state size가 커지면(예: 수십 GB) 매번 전체 상태를 복사하는 대신, 변경된 부분만 저장하는 RocksDB 증분 체크포인트(incremental checkpoint)로 스냅샷 시간을 단축한다.

### keyed state와 상태 백엔드
- keyed state는 keyBy(예: user_id)로 나눈 각 키마다 독립 유지되는 값이다. 예: 사기 탐지에서 user_id=12345 키의 상태에 "최근 10분간 거래 3건, 합계 150만원"을 저장해두고 새 거래가 올 때마다 갱신한다.
- 이 상태를 힙 메모리(HashMapStateBackend, 빠르지만 메모리 한계)에 둘지, 디스크 기반 RocksDB(느리지만 메모리보다 큰 상태 가능)에 둘지는 상태 크기로 결정한다. 예: 활성 사용자 1천만 명 × 사용자당 1KB = 약 10GB → 메모리 한 대에 다 올리기 어려워 RocksDB를 선택한다.

### 비유와 흔한 오해
- **비유**: 택배 분류장이 상자를 받는 즉시 분류하면서, 30초마다 "지금까지 분류표"를 사진 찍어 금고에 넣어두는 것과 같다. 정전(장애)이 나면 마지막 사진 시점부터 다시 분류를 재개하면 되므로 처음부터 다시 할 필요가 없다.
- **흔한 오해**: "Flink를 쓰면 자동으로 exactly-once가 보장된다"는 틀렸다. 체크포인트는 Flink 내부 상태와 소스 오프셋만 정확히 되돌릴 뿐, sink(외부 저장소)에 이미 써버린 결과까지 되돌리지는 못한다. sink가 트랜잭션(2단계 커밋)이나 멱등 쓰기를 지원해야 end-to-end exactly-once가 완성된다(139번 참고).

## 연결 개념
- Kafka — 주요 source/sink, offset이 체크포인트와 함께 관리됨
- Exactly-Once Semantics(139) — 체크포인트와 sink transaction이 결합해야 완성되는 상위 보장
- Kappa Architecture — 배치 계층 없이 스트림만으로 구성하는 아키텍처

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Flink 문제에서 event time, watermark, state, checkpoint, exactly-once를 연결해 답안화함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Flink는 event time과 stateful operator를 지원하는 low-latency stream processing engine임.
> 2. **가치**: checkpoint 기반 상태 복구와 watermark 기반 late event 처리로 연속 데이터 처리의 정합성을 확보함.
> 3. **판단 포인트**: state size, checkpoint interval, watermark delay, sink transaction 지원 여부가 설계 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스트림 처리 원리 확인 | event time, watermark, window, state | 단순 실시간 처리 엔진으로만 설명 |
| 장애 복구 판단 확인 | checkpoint, savepoint, state backend | exactly-once 조건 누락 |
| Spark/Kafka Streams 비교 확인 | record processing, stateful job | batch engine과 동일하게 서술 |

> 요약: Flink 답안은 event time 처리와 상태 일관성 보장을 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Apache Flink는 stateful stream processing engine임.
- 배경: 실시간 서비스는 초 단위 처리뿐 아니라 지연 도착 이벤트, 장애 복구, 중복 처리 제어가 필요함.
- 필요성: event time, watermark, checkpoint로 연속 데이터 처리의 정합성과 복구를 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Kafka Source -> Operator Chain -> Keyed State -> Window/Timer -> Sink
                         / Checkpoint Coordinator -> State Backend
                         / Watermark -> Event Time Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source | 이벤트 입력 | Kafka offset과 checkpoint 연계 |
| Operator | map, keyBy, window 처리 | operator chain 최적화 |
| Keyed State | key별 상태 저장 | RocksDB state backend 사용 가능 |
| Checkpoint | 상태 snapshot | interval, timeout, alignment 설정 |
| Watermark | event time 진행 제어 | late event 허용 범위 결정 |

> 요약: Flink는 source offset, operator state, sink commit을 checkpoint로 묶어 스트림 처리 상태를 복구함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 수신 -> timestamp 추출 -> watermark 생성 -> keyed state 갱신
-> window/timer 평가 -> checkpoint snapshot -> sink commit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | source에서 record 읽기 | source lag |
| 2 | event time과 watermark 계산 | watermark delay |
| 3 | keyed state와 window 갱신 | state size, timer 수 |
| 4 | checkpoint 후 sink 반영 | checkpoint duration, failure count |

> 요약: Flink는 이벤트 시간을 기준으로 상태를 갱신하고 checkpoint를 통해 장애 후 동일 상태로 복구함.

---

## Ⅳ. 특징

| 구분 | Micro-batch 처리 | Apache Flink | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 처리 단위 | 배치 묶음 | record-at-a-time | end-to-end lag 1초 이하 목표 |
| 시간 모델 | processing time 중심 | event time + watermark | late event 허용 5분 |
| 상태 | 외부 저장소 의존 가능 | 내장 keyed state | state size GB~TB |
| 복구 | batch 재시작 | checkpoint/savepoint | checkpoint success 99.9% |

> 요약: Flink는 상태 기반 저지연 스트림에 적합하지만, state와 checkpoint 비용을 지속 측정해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Spark Structured Streaming | continuous stateful stream | sub-second, event time 요구 |
| 비용/성능 | micro-batch 운영 | checkpoint와 state 비용 | state size와 checkpoint SLA |
| 운영/위험 | batch job 운영 | savepoint 기반 배포 | state schema 변경 관리 |

> 요약: Flink는 fraud 탐지·실시간 정산처럼 event time과 state가 핵심인 업무에 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| checkpoint 지연 | state size 증가 | incremental checkpoint, RocksDB tuning | duration/interval 0.5 이하 |
| late event 누락 | watermark 과도 설정 | allowed lateness, side output | late drop count |
| state migration 실패 | schema 변경 | savepoint 검증, compatible serializer | restore failure 0건 |

> 요약: Flink 리스크는 checkpoint, late event, state migration이며 배포 전 savepoint 복구 테스트가 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리 지연 | end-to-end lag 1초 이하 | Flink metrics |
| 복구 | checkpoint success 99.9% | JobManager metric |
| 상태 크기 | state growth 예측선 이내 | state backend metrics |

> 요약: Flink 도입 효과는 지연, checkpoint 성공률, state 성장률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. event_time 필드를 표준화하고 watermark delay를 업무 SLA에 맞춰 1분·5분 등으로 설정함
2. RocksDB incremental checkpoint와 checkpoint interval 30초를 적용해 state snapshot 비용을 제한함
3. 배포는 savepoint 생성, 새 job restore, dual run diff 0.1% 이하 검증 후 전환함

**결론 (2줄):**
- 기술사 판단: sub-second 지연과 stateful event time 처리가 필요하면 Flink, 단순 배치성 스트림은 Spark Structured Streaming을 선택함
- 향후 방향: Flink는 real-time feature, CDC, streaming warehouse와 결합해 실시간 데이터 제품의 실행 계층으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Flink를 설명하시오" | event time, watermark, checkpoint 흐름 | micro-batch 대비 특징 |
| 요구사항 명시형 | "Spark와 비교하시오", "설계하시오" | state backend, checkpoint, sink commit | 지연·정확성·운영 지표 선택 |

> 요약: 설명형은 처리 원리, 비교·설계형은 event time과 exactly-once 조건 중심으로 작성함.
