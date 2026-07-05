---
title: 데이터 집약적 애플리케이션 설계 (Data-intensive App)
date: 2026-07-05
tags: [cspe-software]
weight: 315
---

## Ⅰ. 개요
- 정의: 계산 성능보다 데이터의 양, 복잡성, 변화 속도가 주된 제약인 시스템 설계임
- 배경: 빅데이터 시대의 폭발적인 정보량 처리와 실시간 분석 요구사항 증대 대응
- 출제 의도: 데이터 신뢰성(Reliability), 확장성, 유지보수성을 고려한 저장 및 처리 기법 평가

## Ⅱ. 구성요소
- ASCII 구조도
  [Ingestion] -> [Storage] -> [Processing] -> [Analysis]
      |            |             |             |
   (Kafka)      (NoSQL)       (Spark)      (Dashboard)
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 파티셔닝 | 대용량 데이터를 작은 단위로 나누어 분산함 | 서랍 분리 |
| 복제(Replication) | 가용성 향상을 위해 여러 노드에 데이터를 복제함 | 사본 보관 |
| 인덱싱 | 데이터 조회 속도 향상을 위한 검색 구조체 | 책 목차 |
> 요약: 신뢰성 있는 저장소와 효율적인 분산 처리 메커니즘을 결합한 구조임

## Ⅲ. 절차
- ASCII 흐름도
  Data Modeling -> Storage Select -> Query Opt -> Scalability Plan
- 4단계 설명
1. Data Modeling: 비즈니스 도메인에 적합한 데이터 구조 및 스키마 설계함
2. Storage Select: CAP 이론 등에 따라 RDBMS, NoSQL 등 적합한 DB 선정함
3. Query Opt: 대규모 조인(Join) 배제 및 캐싱 전략을 통한 조회 성능 개선함
4. Scalability Plan: 샤딩(Sharding) 및 읽기 전용 복제본 구성을 통한 부하 분산함
> 요약: 데이터 모델링 후 적절한 저장소를 선정하고 성능과 확장을 설계함

## Ⅳ. 문제점
- 원인이 명시된 문제/한계: 다중 노드 간 데이터 일관성 유지 시 복잡도 및 네트워크 비용 급증함

## Ⅴ. 개선방안
- Ⅳ의 문제에 대응하는 방안: 결과적 일관성(Eventual Consistency) 및 분산 합의 알고리즘 적용함

## Ⅵ. 전망
- 발전 방향: 데이터 메시(Data Mesh) 기반의 도메인 중심 분산 데이터 거버넌스 체계 부각
- CSF: 쓰기(Write)와 읽기(Read)의 부하 특성에 따른 CQRS 패턴 적용 여부가 성능의 핵심임
