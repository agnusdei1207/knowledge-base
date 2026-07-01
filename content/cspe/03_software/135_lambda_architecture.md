---
title: "람다 아키텍처 (Lambda Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 135
---

# 📖 【암기용】 개념 완전 이해

> 목적: 람다 아키텍처가 batch와 speed layer를 왜 나누는지 이해하게 만든다.

## 한눈에
- **개요**: 배치 정확성과 실시간 속도를 함께 얻기 위해 batch layer와 speed layer를 병행하는 데이터 아키텍처
- **왜 필요한가**: 실시간 대시보드는 즉시성이 필요하지만, streaming 계산은 지연·중복·유실 보정이 어려워 사후 정확한 재계산이 필요함.
- **핵심 직관**: 현장 속보와 다음날 정정 기사를 함께 운영하는 방식임.

## 깊이 이해
- **배경·문제의식**: 클릭·결제·센서 데이터는 초 단위 알림과 일 단위 정산을 모두 요구함. 람다 아키텍처는 모든 원천 이벤트를 immutable log에 저장하고, batch view가 정확한 기준값을 만들며 speed view가 최신 값을 보완함.
- **작동 원리**: ingestion된 데이터가 저장소와 stream processor로 동시에 흐름. batch layer는 전체 데이터를 재처리하고, speed layer는 최근 데이터를 low-latency로 처리함. serving layer가 두 결과를 합쳐 조회함.
- **비유**: 식당 매출을 계산할 때 POS 실시간 합계로 현재 매출을 보고, 마감 후 영수증 전체로 확정 매출을 다시 계산함.
- **구체 예시**: 광고 클릭 집계에서 speed layer는 최근 5분 클릭 수를 제공하고, batch layer는 하루 전체를 재계산해 중복 click을 제거함.
- **흔한 오해·주의점**: 두 계층에 동일 로직을 중복 구현하므로 코드 불일치가 발생할 수 있음. 이 문제가 카파 아키텍처 등장 배경임.

## 연결 개념
- Kappa Architecture — stream-only 대안
- Apache Kafka — immutable event log
- Spark/Flink — batch·stream 처리 엔진

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
