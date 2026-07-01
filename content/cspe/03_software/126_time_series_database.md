---
title: "시계열 데이터베이스 (Time Series Database)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 126
---

# 📖 【암기용】 개념 완전 이해

> 목적: 시계열 데이터베이스를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 시간값을 중심으로 측정 데이터 저장·조회·집계를 처리하는 데이터베이스
- **왜 필요한가**: 서버 CPU, IoT 센서, 주가, 로그 메트릭은 시간순으로 계속 쌓이고 최근 구간 조회가 많다. 일반 DB에 그대로 넣으면 쓰기량, 보존 기간, 집계 쿼리 관리가 어려워진다.
- **핵심 직관**: 모든 기록에 시간 도장을 찍고, 날짜별 서랍에 넣어 최근 5분·1시간·30일 단위로 꺼내보는 구조임

## 깊이 이해
- **배경·문제의식**: 관측성, IoT, 금융 데이터는 초당 수천~수백만 포인트가 발생한다. 시계열 DB는 시간 파티션, 압축, 다운샘플링, retention 정책으로 쓰기와 보관 비용을 제어한다.
- **작동 원리**: 데이터 포인트는 timestamp, metric name, tag, value로 구성된다. 쓰기는 append 중심으로 저장되고, 조회는 시간 범위와 태그 필터를 기준으로 집계한다.
- **비유**: 병원 체온표처럼 매 시각의 측정값을 순서대로 적고, 일별 평균과 이상 구간을 따로 표시하는 방식임
- **구체 예시**: 5,000대 서버가 10초마다 CPU·메모리·디스크 20개 메트릭을 보내면 하루 864,000,000 포인트가 생성되므로 압축과 보존 정책이 필수임
- **흔한 오해·주의점**: 시계열 DB는 모든 로그 원문 저장소가 아니다. tag cardinality가 폭증하면 인덱스 메모리와 조회 비용이 증가하므로 사용자 ID 같은 고유값 태그는 제한해야 한다.

## 연결 개념
- 관측성(Observability) - metrics, logs, traces 중 metrics 저장 축
- LSM-Tree - append 중심 쓰기 구조와 관련
- 데이터 보존 정책 - retention, downsampling, compaction

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 시계열 DB 답안은 시간 파티션, 태그 카디널리티, 보존·집계 정책을 함께 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시계열 DB는 timestamp 중심 append 데이터의 저장, 압축, 시간 범위 집계를 최적화한 DB임.
> 2. **가치**: 초당 수만~수백만 포인트 수집, 최근 구간 조회, 장기 보존 비용 통제에 적합함.
> 3. **판단 포인트**: tag cardinality, retention, downsampling, query range가 운영 비용과 조회 지연을 결정함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 시계열 모델 이해 확인 | timestamp, metric, tag, value | 로그 저장소와 동일시하지 않음 |
| 대량 쓰기 설계 확인 | append, time partition, compression | 쓰기량 산정 없이 개념만 쓰지 않음 |
| 운영 비용 판단 확인 | retention, downsampling, cardinality | 태그 폭증 리스크 누락 방지 |

> 요약: 시계열 DB 문제는 시간 중심 저장 구조와 보존 정책을 정량 지표로 연결해야 함.

---

## Ⅰ. 개요 및 필요성

시계열 데이터베이스는 시간순 측정값 저장소이다. 관측성·IoT·금융 데이터는 지속 발생하고 최근 시간 범위 조회와 집계가 집중된다. 시간 파티션, 압축, 보존 정책을 통해 대량 쓰기와 장기 저장 비용을 제어한다.

---

## Ⅱ. 구조 및 구성요소

```text
Agent/Sensor -> Ingestion -> Time Partition -> Compressed Block -> Query Engine
                 +-> Tag Index
                 +-> Retention/Downsampling
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data Point | timestamp, tag, value 저장 | append 중심 입력 |
| Tag Index | host, region, service 필터링 | cardinality 관리 필요 |
| Time Partition | 시간 구간별 저장 단위 | 최근 구간 조회 최적화 |
| Retention | 보존·삭제·다운샘플 정책 | 7일 원본, 1년 집계 예시 |

> 요약: 시계열 DB는 시간 파티션과 태그 인덱스를 중심으로 수집·저장·집계가 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
Metric Collect -> Timestamp Normalize -> Tag Index Update -> Block Write -> Range Query -> Aggregate
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 에이전트·센서가 측정값 전송 | ingestion rate points/sec |
| 2 | timestamp 정규화와 태그 검증 | clock skew, tag whitelist |
| 3 | 시간 파티션에 append 저장 | write latency p95 |
| 4 | 압축·compaction·retention 적용 | compression ratio |
| 5 | 시간 범위와 태그 조건으로 집계 | query latency p95 |

> 요약: 시계열 DB는 수집값을 시간 파티션에 append하고, 조회 시 시간 범위와 태그로 집계함.

---

## Ⅳ. 특징

| 구분 | 일반 RDB/로그 저장 | 시계열 DB | 판단 포인트 |
|:---|:---|:---|:---|
| 쓰기 패턴 | 행 단위 혼합 트랜잭션 | timestamp append | 초당 포인트 수 |
| 조회 패턴 | 키·조건 검색 | 시간 범위 집계 | 최근 1시간·24시간 쿼리 |
| 보존 | 수동 파티션 관리 | retention/downsampling | 원본 보존 기간과 집계 해상도 |

> 요약: 시계열 DB는 시간 범위 집계와 보존 정책이 중심인 데이터에 적용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RDB 파티션 테이블 | time partition + tag index | 메트릭 1억 포인트/일 이상 |
| 비용/성능 | 원본 장기 보관 | downsampling + compression | 저장 비용 GB/day |
| 운영/위험 | 단순 로그 보관 | cardinality 통제 | tag cardinality 100만 이하 관리 |

> 요약: 시계열 DB 선택은 포인트 수, 시간 범위 쿼리, 보존 정책으로 결정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Cardinality 폭증 | user_id 등 고유 태그 사용 | tag whitelist, label limit | series count 증가율 |
| 저장 비용 증가 | 원본 장기 보존 | downsampling, retention 30/365일 | GB/day, compression ratio |
| 지연 조회 | 넓은 범위 고해상도 쿼리 | rollup table, query limit | query p95, scanned blocks |

> 요약: 시계열 DB 리스크는 태그 수, 보존 기간, 조회 범위를 기준으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수집 | ingest rate 목표 대비 120% 여유 | ingestion metric |
| 저장 | compression ratio 5:1 이상 | storage report |
| 조회 | 최근 1시간 p95 1초 이하 | query log |

> 요약: 시계열 DB는 수집 여유율, 압축률, 시간 범위 조회 지연으로 평가함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. metric name, tag whitelist, label cardinality 한도를 사전에 정의해 사용자 ID·요청 ID 태그화를 차단함.
2. 원본 7~30일, 1분 rollup 90일, 1시간 rollup 1년 같은 retention/downsampling 정책을 적용함.
3. 대시보드는 최근 1시간·24시간 쿼리에 맞춰 사전 집계하고, 장기 분석은 데이터 레이크로 이관함.

**결론 (2줄):**
- 기술사 판단: 시간 범위 집계와 지속 수집이 핵심이면 시계열 DB, 임의 조건 검색이 핵심이면 검색/분석 DB를 선택함.
- 향후 방향: 관측성 플랫폼은 metrics·logs·traces를 연계해 SLO와 장애 원인 분석을 자동화하는 방향으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "시계열 DB를 설명하시오" | 수집, 파티션, 집계 흐름 | RDB와 시계열 DB 비교 |
| 요구사항 명시형 | "관측성 저장소 설계를 제시하시오" | tag, retention, downsampling 설계 | cardinality와 비용 대응 |

> 요약: 설명형은 시간 중심 원리, 설계형은 태그와 보존 정책을 중심으로 작성함.
