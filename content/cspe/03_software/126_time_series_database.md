---
title: "시계열 데이터베이스 (Time Series Database)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 126
extra:
  question_no: "126"
  exam_status: "미출제"
  exam_note: "기본"
---

## 미리 알고가기

- 시계열 DB는 시간 축에 따라 계속 기록되는 데이터를 저장·조회하도록 최적화된 DB임
- 메트릭과 로그와 센서 데이터처럼 append-heavy 패턴에 적합함
- 압축과 downsampling과 retention 정책이 핵심 운영 요소임

## Ⅰ. 개요

- **정의/개념**: 시계열 데이터베이스는 시간 정보를 기준으로 연속 발생하는 이벤트와 메트릭과 센서 값을 대량으로 저장하고 최근 구간 조회와 집계와 보관 주기 관리에 최적화한 데이터베이스 구조임
- **배경/필요성**: 관측성 플랫폼과 IoT와 금융 시세처럼 쓰기 빈도는 높고 조회는 시간 범위 중심인 데이터는 범용 DB보다 시계열 특화 저장 방식이 더 효율적임

## Ⅱ. 특징

- append 중심 쓰기와 시간 구간 조회에 강함
- downsampling과 retention으로 저장 비용을 제어함
- 태그 기반 필터와 집계 함수가 중요함
- 고카디널리티 태그가 늘면 메모리와 인덱스 부담이 급격히 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 일반 관계형 DB | 시계열 DB |
|:---|:---|:---|
| 쓰기 패턴 적합성 | 범용 | append-heavy 특화 |
| 시간 구간 조회 | 가능하지만 추가 튜닝 필요 | 기본 최적화 |
| 강점 | 범용 트랜잭션 | 압축·집계·보관 정책 |
| 한계 | 대량 시계열 비용 증가 | 범용 관계 질의 제약 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Time-Indexed Storage | 시간 축 기준 저장 단위가 구간 조회 효율을 높임 |
| Tag and Field Model | 메타데이터 필터와 측정값 분리를 통해 질의 패턴을 지원함 |
| Retention and Downsampling | 장기 저장 비용을 줄이면서 활용 가능한 해상도를 유지함 |
| Compression Pipeline | 반복적 수치 데이터 압축으로 저장 효율을 높임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 시계열 수집     | --> | 시간축 저장     | --> | 집계/압축 수행  | --> | 보관 주기 정리  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **시계열 수집**: 이벤트와 메트릭을 시간 순으로 수신함
2. **시간축 저장**: 시간 단위로 정렬하고 분할함
3. **집계와 압축 수행**: 해상도별 요약과 압축을 적용함
4. **보관 주기 정리**: 오래된 원본을 삭제하거나 다운샘플 값으로 대체함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 태그 설계를 느슨하게 하면 고카디널리티 폭증으로 메모리와 인덱스 비용이 급격히 커질 수 있음
   - 해결방안: tag cardinality budget을 운영하고 high-cardinality ratio와 memory usage per series로 검증함
2. 문제: 보관 주기 없이 원본 데이터를 계속 쌓으면 저장 비용이 분석 가치보다 더 빠르게 증가할 수 있음
   - 해결방안: retention tiering과 downsampling을 적용하고 storage growth rate와 query value retention score로 검증함
3. 문제: 시간 동기화가 맞지 않으면 집계 결과와 경보 판단이 왜곡될 수 있음
   - 해결방안: timestamp normalization을 수행하고 clock skew incident count와 aggregation accuracy로 검증함

## Ⅶ. 적용 사례

- 관측성 플랫폼에서는 태그 예산을 관리하고 확인 지표는 high-cardinality ratio와 memory usage per series임
- IoT 센서 저장소에서는 보관 계층을 운영하고 확인 지표는 storage growth rate와 query value retention score임
- 분산 수집 환경에서는 시간 정규화를 수행하고 확인 지표는 clock skew incident count와 aggregation accuracy임

## Ⅷ. 결론

시계열 DB의 핵심은 시간 데이터가 많다는 사실보다 시간축 조회와 보관 주기와 고카디널리티 비용을 함께 다루는 데 있음.
