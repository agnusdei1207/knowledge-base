---
title: 복제 Replication — Master-Slave (DB Replication)
date: 2026-07-05
tags: [cspe-software]
weight: 081
---

## Ⅰ. 개요
- 데이터베이스의 가용성을 높이고 읽기 부하를 분산하기 위해 동일한 데이터를 여러 노드에 복사하는 기술임.
- 마스터(Master)와 슬레이브(Slave) 간의 데이터 동기화 방식이 핵심임.
- 출제 의도: 복제 아키텍처별 일관성 보장 수준과 장애 조치(Failover) 원리 이해.

## Ⅱ. 구성요소
- 복제 아키텍처
[Master (Write)] -> (Binary Log) -> [Slave (Read Only)]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Master | 쓰기/수정 수행, 변경 내역 로그 기록 | 원본 문서 작성자 |
| Slave | 마스터의 로그를 읽어 데이터 동기화, 조회 전용 | 복사본 열람자 |
| Binary Log | 변경된 모든 쿼리나 로우 데이터를 기록하는 파일 | 작성 일지 |
> 요약: 역할 분담을 통해 처리 성능을 향상시키고 데이터 백업을 수행함.

## Ⅲ. 절차
- 동기화 방식 처리 흐름
[Write Tx] -> [Master DB] -> (Log Shipping) -> [Slave DB] -> [Ack]

1. 비동기(Asynchronous): 마스터가 로그 전송 후 즉시 커밋함. 성능 우수.
2. 반동기(Semi-sync): 최소 하나의 슬레이브가 로그 수신 확인 시 커밋함.
3. 동기(Synchronous): 모든 슬레이브가 반영 완료해야 마스터가 커밋함.
4. 장애 조치: 마스터 중단 시 슬레이브 중 하나를 새 마스터로 승격함.
> 요약: 성능과 데이터 정합성 사이의 균형에 맞춰 복제 방식을 선택함.

## Ⅳ. 문제점
- 복제 지연(Replication Lag)에 따른 일관성 위배 및 마스터 병목 현상.

## Ⅴ. 개선방안
- 멀티 마스터(Multi-Master) 구성 및 병렬 복제(Parallel Replication) 도입.

## Ⅵ. 전망
- 클라우드 환경의 Multi-AZ/Multi-Region 복제를 통한 글로벌 고가용성 확보.
- 충돌 해결 알고리즘(CRDT)을 활용한 능동-능동(Active-Active) 복제 대중화.
