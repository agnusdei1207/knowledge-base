---
title: "람다 아키텍처 (Lambda Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 135
---

# 📖 【암기용】 개념 완전 이해

> 목적: 람다 아키텍처가 batch layer와 speed layer를 왜 굳이 둘 다 두는지, 내부 용어와 트레이드오프를 이해하게 만든다.

## 한눈에
- **개요**: 람다 아키텍처는 **batch layer**(정확성)와 **speed layer**(실시간성)를 병행 운영해 데이터의 정확성과 즉시성을 동시에 확보하는 **빅데이터 처리 아키텍처 패턴**이다.
- **왜 필요한가**: 실시간 스트림 처리는 중복 이벤트·지연 도착(late event)·장애 재시작 같은 이유로 근사치(approximate)에 그치기 쉽다. 반대로 정확한 전체 재계산(batch)은 결과가 나오기까지 시간이 걸려 즉시성이 없다. 두 요구를 한 계층으로 동시에 만족시키기 어려워 계층을 분리했다.
- **핵심 직관**: 방송사의 "현장 속보"(speed layer, 빠르지만 부정확할 수 있음)와 "다음날 정정·확정 기사"(batch layer, 느리지만 정확함)를 함께 운영하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 데이터 처리 아키텍처 패턴 | 데이터 수집부터 조회까지의 표준 구조 설계 방식 — 람다가 속한 상위 범주 | 건물의 설계 도면 |
| batch layer | 원본 데이터 전체를 주기적으로 재계산해 정확한 결과(batch view)를 만드는 계층 | 마감 후 영수증 전체로 정산 확정 |
| speed layer | 최근 도착한 데이터만 즉시 처리해 실시간 근사 결과(realtime view)를 만드는 계층 | POS 실시간 합계로 현재 매출 추정 |
| serving layer | batch view와 realtime view를 합쳐 조회 응답을 만드는 계층 | 확정치와 잠정치를 합쳐 보여주는 창구 |
| immutable log | 원천 이벤트를 수정·삭제 없이 순서대로 보존하는 저장소(예: Kafka) | 한번 적으면 지우지 않는 회계 장부 |
| batch view | batch layer가 전체 재계산으로 만든 정확한 결과 | 마감 정산서 |
| realtime view | speed layer가 최근 데이터만으로 만든 근사 결과 | 잠정 집계표 |
| late event | 실제 발생 시각보다 시스템에 늦게 도착한 이벤트(네트워크 지연 등) | 우편 발송이 늦어 다음날 도착한 주문서 |

## 깊이 이해

### 왜 이렇게 나눴나 (배경)
Nathan Marz가 Twitter/BackType에서 실시간 분석 시스템을 운영하며 겪은 문제에서 2011년경 제안한 패턴이다. 스트림 처리만으로는 "정확히 한 번(exactly-once) 처리"를 보장하기 어렵고(재시도로 중복 카운트가 생기거나, 장애로 일부 이벤트를 놓칠 수 있음), 이를 완벽히 해결하려는 복잡도가 시스템 전체를 불안정하게 만들었다. 그래서 "speed layer는 틀려도 되니 빠르게, batch layer가 나중에 전체를 다시 계산해 정확하게 고친다"는 역할 분담으로 문제를 우회했다.

### 동작 흐름 — 광고 클릭 집계 수치 예제
원천 이벤트(클릭 로그)는 immutable log에 먼저 기록된다.
- **speed layer**: 최근 5분간 클릭을 즉시 집계해 "12,345건"을 실시간 대시보드에 보여준다. 이 값은 네트워크 재시도로 인한 중복 클릭을 그대로 포함할 수 있어 근사치다.
- **batch layer**: 자정에 그날 전체 로그를 다시 읽어 event_id 기준 중복 342건을 제거하고, 확정값 "11,987건"으로 batch view를 다시 쓴다(overwrite).
- **serving layer**: 대시보드는 batch view가 존재하는 구간(어제까지)은 확정값을, 아직 batch가 돌지 않은 구간(오늘)은 realtime view를 이어붙여 보여준다. 매일 자정 이후 realtime view는 batch view로 대체되고 새로 쌓이기 시작한다.

### batch와 speed가 "같은 로직을 두 번" 구현하는 문제
클릭 중복 제거 로직을 batch layer는 Spark(Scala/Python) job으로, speed layer는 Flink(Java) job으로 각각 구현한다고 하자. 두 코드베이스가 정확히 같은 규칙(예: "5분 이내 같은 user_id+ad_id는 1건으로 처리")을 따르도록 계속 동기화해야 하는데, 한쪽만 로직을 수정하면 결과가 어긋난다. 이 이중 구현·이중 유지보수 부담이 람다 아키텍처의 대표적 단점이며, 이를 없애기 위해 나온 대안이 카파 아키텍처다(136).

### 흔한 오해
람다 아키텍처는 "batch가 필요 없어지면 자동으로 없어지는 임시 구조"가 아니라, 법정 정산·회계처럼 확정값이 반드시 필요한 도메인에서는 지금도 정당한 설계다. speed layer만으로 "충분히 정확"해질 수 있는 도메인(예: 로그 모니터링)이라면 카파가 더 적합하다는 것이지, 람다 자체가 열등한 것은 아니다.

## 연결 개념
- Kappa Architecture — batch layer를 제거하고 stream-only로 단순화한 대안(136)
- Apache Kafka — batch·speed 양쪽이 공유하는 immutable event log(137)
- Apache Spark·Flink — 각각 batch layer·speed layer의 대표 처리 엔진(134)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Lambda Architecture 문제에서 batch/speed/serving 분리, 정확성·지연 균형, 운영 중복을 판단함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 람다 아키텍처는 batch layer와 speed layer를 병행해 정확한 재계산과 저지연 결과를 함께 제공하는 구조임.
> 2. **가치**: 원천 이벤트 보존과 batch 재처리로 streaming 오류·중복·지연 데이터를 보정함.
> 3. **판단 포인트**: 코드 중복, serving merge, backfill 비용, data freshness 요구를 기준으로 Kappa와 비교해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 빅데이터 아키텍처 이해 확인 | batch, speed, serving layer | 단순 ETL 구조로만 설명 |
| 정확성·지연 균형 판단 | immutable data, recomputation, low latency | batch layer 필요성 누락 |
| 대안 비교 역량 확인 | Lambda vs Kappa | speed layer만 강조하고 운영 중복 누락 |

> 요약: 람다 아키텍처 답안은 정확한 재계산과 실시간 보완을 동시에 설명해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 람다 아키텍처는 배치와 실시간 병행 처리 구조임.
- 배경: 실시간 분석은 초 단위 결과를 제공하지만 late event·중복·장애 복구 문제가 있음.
- 필요성: batch layer는 전체 데이터를 재계산하고 speed layer는 최신 데이터를 보완해 정확도와 적시성을 분리함.

---

## Ⅱ. 구조 및 구성요소

```text
Event Source -> Ingestion Log -> Batch Layer -> Batch View
                         / Speed Layer -> Realtime View
Batch View + Realtime View -> Serving Layer -> Query/API
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Ingestion Log | 원천 이벤트 보존 | Kafka, object storage |
| Batch Layer | 전체 데이터 재처리 | Spark, Hadoop, daily backfill |
| Speed Layer | 최신 이벤트 처리 | Flink, Spark Streaming |
| Serving Layer | batch+speed 결과 조회 | merge logic와 중복 제거 필요 |

> 요약: 람다 아키텍처는 원천 이벤트를 보존한 뒤 batch view와 realtime view를 합쳐 조회 결과를 제공함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 수집 -> 원천 저장 -> speed layer 즉시 집계
-> batch layer 주기 재계산 -> serving layer 병합 -> 조회 응답
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이벤트 수집과 immutable 저장 | event loss 0건 |
| 2 | speed layer에서 최근 데이터 처리 | end-to-end lag 5초 이하 |
| 3 | batch layer에서 전체 데이터 재계산 | daily recompute 성공률 |
| 4 | serving layer에서 view 병합 | duplicate count, freshness |

> 요약: speed layer가 최신성을 제공하고 batch layer가 정확성을 확정하며 serving layer가 두 결과를 조합함.

---

## Ⅳ. 특징

| 구분 | 단일 배치 | Lambda Architecture | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 최신성 | 일·시간 단위 | 초·분 단위 보완 | stream lag 5초 이하 |
| 정확성 | 전체 재계산 가능 | batch view로 확정 | daily reconciliation |
| 운영 | 파이프라인 1개 | batch+speed 2개 | 로직 중복률 관리 |
| 비용 | 처리 단순 | 저장·계산 이중화 | backfill 시간과 cluster 비용 |

> 요약: 람다는 정확성과 최신성을 동시에 제공하나, 두 계층 로직 일치와 serving 병합이 운영 부담임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Kappa stream-only | batch+speed 병행 | 재계산 정확성이 법정·정산 기준인 경우 |
| 비용/성능 | 단일 stream 운영 | batch backfill 비용 추가 | 정산 SLA와 freshness 동시 요구 |
| 운영/위험 | 코드 경로 1개 | 로직 이중화 | batch·speed 결과 차이 허용치 |

> 요약: 람다는 정산·통계 확정값이 필요한 업무에 적합하고, 단순 이벤트 처리에는 Kappa가 운영 비용을 줄임.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 로직 불일치 | batch와 speed 코드 분리 | 공통 transformation library | batch-speed diff 0.1% 이하 |
| late event 누락 | 지연 도착 이벤트 | watermark, replay, backfill | late event 처리율 |
| serving 중복 | view 병합 기준 오류 | event_id 기반 dedup | duplicate record 0건 |

> 요약: 람다의 핵심 리스크는 두 계층 결과 불일치이며 diff 지표와 replay 절차로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| freshness | realtime lag 5초 이하 | stream metrics |
| 정확성 | batch 확정값 오차 0.1% 이하 | reconciliation report |
| 복구 | backfill 완료 4시간 이하 | workflow scheduler |

> 요약: 람다 도입 효과는 최신성, 확정값 오차, backfill 복구 시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Kafka topic을 원천 로그로 보존하고 event_id, event_time, processing_time을 표준 필드로 정의함
2. speed layer는 5초 이하 lag, batch layer는 일 1회 full recompute와 시간 단위 incremental recompute로 구성함
3. serving layer는 event_id dedup과 batch cutoff time을 기준으로 realtime view와 batch view를 병합함

**결론 (2줄):**
- 기술사 판단: 정확한 재계산과 실시간 모니터링이 모두 필요하면 Lambda, stream 처리만으로 보정 가능한 업무면 Kappa를 선택함
- 향후 방향: lakehouse table format과 unified engine 확산으로 batch·stream 코드 중복을 줄이는 방향으로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "람다 아키텍처를 설명하시오" | batch/speed/serving layer 흐름 | 정확성·최신성·운영 중복 |
| 요구사항 명시형 | "Kappa와 비교하시오", "설계하시오" | 동일 이벤트의 batch·stream 처리 경로 | 선택 기준, diff 검증, backfill 방안 |

> 요약: 설명형은 계층 구조, 비교·설계형은 Kappa 대비 운영 중복과 정합성 검증 중심으로 작성함.
