---
title: NewSQL 및 분산 DB (NewSQL)
date: 2026-07-05
tags: [cspe-software]
weight: 68
---

## Ⅰ. 개요
- RDBMS의 ACID 특성과 NoSQL의 확장성(Scale-out)을 결합한 차세대 데이터베이스임.
- 분산 아키텍처 환경에서 표준 SQL 인터페이스를 제공하는 것이 핵심임.
- 출제 의도: 분산 합의 알고리즘(Paxos/Raft) 기반의 강력한 일관성 확보 기술 확인.

## Ⅱ. 구성요소
- NewSQL 아키텍처
[SQL Interface] -> [Distributed Query Engine] -> [Shared-Nothing Storage]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Raft/Paxos | 분산 노드 간 일관성 유지를 위한 합의 프로토콜 | 다수결 투표 |
| Distributed Lock | 분산 환경에서의 자원 점유 제어 | 공유 자원 예약 시스템 |
| HTAP | 트랜잭션과 분석 처리를 동시 수행 (TiDB 등) | 다목적 경기장 |
> 요약: 분산 합의와 확장형 스토리지를 통해 일관성과 성능을 동시 확보함.

## Ⅲ. 절차
- 분산 트랜잭션 처리 (2PC)
[Coordinator] -> (Prepare) -> (Vote) -> (Commit/Abort)

1. 준비(Prepare): 모든 참여 노드에 트랜잭션 준비 요청을 전송함.
2. 투표(Vote): 각 노드는 로컬 실행 가능 여부를 코디네이터에 응답함.
3. 결정(Global Commit): 모든 노드가 OK일 경우 최종 커밋 명령 하달함.
4. 완료: 각 노드가 커밋을 수행하고 코디네이터에 완료 보고함.
> 요약: 2단계 커밋을 통해 모든 노드에 데이터 반영을 원자적으로 보장함.

## Ⅳ. 문제점
- 분산 합의 과정의 네트워크 오버헤드로 인한 짧은 대기 시간(Latency) 확보의 어려움.

## Ⅴ. 개선방안
- 로컬리티를 고려한 데이터 배치 및 하드웨어 가속기(FPGA/SmartNIC) 활용.

## Ⅵ. 전망
- 지리적 분산(Geo-distribution) 환경에서의 초저지연 트랜잭션 기술 고도화 예상.
- 클라우드 기반 Global DB 서비스(Spanner, Aurora 등)의 시장 지배력 강화.
