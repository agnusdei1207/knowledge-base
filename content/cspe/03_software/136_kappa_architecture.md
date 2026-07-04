---
title: "카파 아키텍처 (Kappa Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 136
---

# 📖 【암기용】 개념 완전 이해

> 목적: 카파 아키텍처가 람다 아키텍처의 이중 구현 문제를 어떻게 없애는지, replay 원리를 이해하게 만든다.

## 한눈에
- **개요**: 카파 아키텍처는 **batch layer 없이 stream processing 하나만으로** 실시간 처리와 재처리(reprocessing)를 모두 수행하는 **stream-only 데이터 처리 아키텍처 패턴**이다.
- **왜 필요한가**: 람다 아키텍처는 batch layer와 speed layer에 같은 집계 로직을 두 번(서로 다른 코드베이스로) 구현해야 해서, 로직 불일치와 이중 운영 부담이 생긴다. Kafka처럼 이벤트를 오래 보존하고 다시 읽을 수 있는 durable log가 등장하면서, "처음부터 다시 재생(replay)"으로 batch의 역할까지 대신할 수 있게 됐다.
- **핵심 직관**: CCTV 원본 영상을 통째로 보관해 두고, 분석 규칙이 바뀌면 같은 영상을 처음부터 다시 돌려 새로운 결과를 뽑아내는 방식이다 — 별도의 "정산팀"(batch layer)을 두지 않는다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| stream-only 아키텍처 | batch 계층 없이 스트림 처리 하나로 모든 처리를 수행하는 상위 설계 방식 | 정산팀 없이 실황팀 하나로 운영 |
| durable log | 이벤트를 오랜 기간(수일~수개월) 순서대로 보존하는 append-only 저장소 | 지우지 않는 CCTV 녹화 보관함 |
| replay | 저장된 로그를 처음(또는 특정 시점) offset부터 다시 읽어 재처리하는 동작 | 녹화 영상을 처음부터 다시 재생 |
| offset | 로그에서 각 이벤트의 위치(순번)를 가리키는 값 | 영상의 재생 시간 지점(타임코드) |
| state store | stream processor가 집계 중간값을 유지하는 저장소 | 계산 중인 장부 |
| checkpoint | 처리 중 상태를 주기적으로 저장해, 장애 시 복구 지점으로 쓰는 스냅샷 | 저장 게임 지점 |
| savepoint | 사용자가 명시적으로 만드는 상태 스냅샷 — job 코드 배포·업그레이드 시 사용 | 수동으로 찍어두는 백업 지점 |
| retention | 로그를 얼마나 오래 보존할지 정하는 정책(기간 또는 용량 기준) | 창고 보관 기한 |
| consumer group | 여러 stream processor가 partition을 나눠 병렬로 읽는 논리적 묶음 | 여러 팀이 구역을 나눠 담당 |

## 깊이 이해

### 왜 카파가 가능해졌나 (배경)
2014년 Jay Kreps(Kafka 공동 개발자)가 "Questioning the Lambda Architecture"라는 글에서 제안했다. 핵심 전제는 "Kafka 같은 durable log가 있으면, 과거 이벤트를 마치 batch의 원본 파일처럼 몇 주~몇 달 뒤에도 다시 읽을 수 있다"는 것이다. 그렇다면 batch layer가 하던 일(전체 데이터를 다시 계산해 정확한 결과를 만드는 것)을, "새로운 stream job이 로그의 처음부터 replay"하는 것으로 똑같이 해낼 수 있다 — 별도의 batch 코드가 필요 없어진다.

### replay로 로직을 바꾸는 절차 — 수치 예제
클릭 집계 로직에 버그가 있어 수정했다고 하자. Kafka topic의 retention이 90일이면, 최근 90일치 이벤트가 모두 로그에 남아 있다. 새로 배포한 stream job(새 consumer group)이 offset 0(90일 전)부터 다시 읽기 시작한다. 이 job의 처리 속도가 실시간 유입 속도의 10배라면(예: 초당 유입 1,000건인데 재처리 시 초당 10,000건 처리 가능), 90일치 데이터를 재처리하는 데 걸리는 시간은 대략 90일 ÷ 10 = 9일이다. 재처리가 최신 시점을 따라잡으면(caught up), 새 job의 결과를 정답으로 승격하고 기존 job은 폐기한다 — 이를 dual run(신규·기존 병행 실행 후 결과 diff 확인)이라 부른다.

### state와 checkpoint — 장애가 나면 어떻게 되나
stream processor는 "지금까지 집계한 값"을 state store(예: RocksDB)에 유지한다. 이 state가 메모리·로컬 디스크에만 있으면 서버가 죽는 순간 사라지므로, 일정 간격(예: 30초)마다 checkpoint로 외부 저장소(HDFS, S3)에 스냅샷을 남긴다. 장애가 나면 마지막 checkpoint 시점의 state를 복구하고, 그 checkpoint 이후의 offset부터 로그를 다시 읽어 이어서 처리한다 — 정확히 이 메커니즘이 "batch 재계산 없이도 정확성을 회복"할 수 있게 해준다.

### 흔한 오해
카파가 batch를 완전히 대체하는 만능 구조는 아니다. 수년치 데이터를 통째로 replay하려면 그만큼 로그를 오래 보존해야 하는데, retention이 길어질수록 저장 비용이 커지고 replay 자체도 오래 걸린다(위 예제처럼 9일이 걸릴 수도 있다). 이런 대규모 backfill이나 규제상 장기 확정 재계산이 자주 필요하다면, 여전히 별도 batch 계층(람다)이나 lakehouse batch 처리를 병행하는 것이 현실적이다.

## 연결 개념
- Lambda Architecture — 카파가 단순화한 batch+speed 이중 구조(135)
- Apache Kafka — replay를 가능하게 하는 durable event log의 대표 구현(137)
- Apache Flink — state store·checkpoint·savepoint를 지원하는 대표 stream processor

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

- 개요: 카파 아키텍처는 스트림 중심 데이터 처리 구조임.
- 배경: 람다 아키텍처의 batch/speed 이중 구현은 코드 불일치와 운영 비용을 만든다.
- 필요성: immutable event log와 stream processor replay로 실시간 처리와 재처리를 하나의 경로로 통합함.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
