---
title: "데이터베이스 복제 - 마스터-슬레이브·멀티마스터 (Database Replication)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 113
---

# 📖 【암기용】 개념 완전 이해

> 목적: 데이터베이스 복제를 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 한 DB의 변경 로그를 다른 DB에 전달해 동일 데이터를 유지하는 기법
- **왜 필요한가**: 운영 DB는 읽기 부하, 장애, 지역 지연, 백업 작업을 동시에 감당해야 한다. 복제는 읽기 분산, 고가용성, 재해복구를 위해 데이터를 여러 노드에 유지한다.
- **핵심 직관**: 원본 장부에 기록한 거래를 지점 장부에도 계속 베껴 두어 조회와 장애 대응에 쓰는 방식이다.

## 깊이 이해
- **배경·문제의식**: 단일 DB 장애는 서비스 중단으로 이어지고, 분석·리포트 쿼리가 운영 writer를 압박한다. 복제는 WAL/binlog 같은 변경 로그를 replica에 전달해 읽기와 복구 경로를 만든다.
- **작동 원리**: primary가 트랜잭션 로그를 기록하고 replica가 이를 받아 재실행한다. 동기 복제는 commit 전 replica 확인을 기다리고, 비동기 복제는 commit 후 별도 전송한다.
- **비유**: 본점 금고 거래 내역을 지점 금고 장부에 계속 복사하면 본점 장애 시 지점이 업무를 이어받을 수 있다.
- **구체 예시**: PostgreSQL streaming replication에서 primary commit 후 replica replay가 3초 늦으면 replica 조회는 최대 3초 전 데이터를 볼 수 있다. 이를 replication lag라 한다.
- **흔한 오해·주의점**: replica를 여러 개 두면 읽기 부하는 분산되지만 쓰기 처리량은 primary 한계에 묶인다. multi-master는 충돌 해결 정책이 필요하다.

## 연결 개념
- WAL/binlog — 복제의 변경 로그 원천
- Failover — primary 장애 시 replica 승격 절차
- Split-brain — 두 노드가 동시에 primary로 동작하는 장애
- Read replica — 읽기 부하 분산용 복제 노드

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 복제 답안은 방식 나열이 아니라 동기/비동기, lag, failover, split-brain을 RTO/RPO 관점으로 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터베이스 복제는 primary 변경 로그를 replica에 전파해 다중 사본을 유지하는 가용성·읽기분산 기법이다.
> 2. **가치**: 읽기 QPS를 분산하고 primary 장애 시 RTO/RPO 목표에 맞춰 서비스 복구 경로를 제공한다.
> 3. **판단 포인트**: 동기/비동기 복제, lag 허용치, failover 자동화, split-brain 방지, 충돌 해결 정책을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DB 고가용성 설계 역량 확인 | primary-replica, multi-master, sync/async 구조 | 백업과 복제를 동일시 |
| 정합성·가용성 트레이드오프 확인 | replication lag, RPO, commit latency | 비동기 복제의 데이터 손실 가능성 누락 |
| 장애 전환 운영 판단 확인 | failover, fencing, quorum, split-brain 방지 | replica 승격 절차와 클라이언트 라우팅 누락 |

> 요약: 이 문제는 복제 방식별 데이터 손실 허용치와 장애 전환 절차를 수치로 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

데이터베이스 복제는 DB 변경사항을 다른 노드에 전달해 사본을 유지하는 기법이다. 단일 DB 장애, 읽기 부하 집중, 지역 지연, 백업 부하를 줄이기 위해 사용한다. 복제 설계는 RTO, RPO, commit 지연, 읽기 정합성 요구를 기준으로 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Write -> Primary DB -> WAL/binlog
  / Sync Replica: commit 전 확인
  / Async Replica: commit 후 전송
  / Read Replica: 조회 분산
Failover Manager -> VIP/DNS/Proxy -> New Primary
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Primary | 쓰기 트랜잭션 처리 | 단일 writer 구조에서 병목 가능 |
| Replica | 로그 수신·재실행 | read-only 또는 승격 후보 |
| 복제 로그 | 변경 순서 전달 | WAL, binlog, redo log 기반 |
| Failover Manager | 장애 감지·승격 | quorum, fencing 필요 |
| 라우팅 계층 | 읽기/쓰기 분리 | ProxySQL, PgBouncer, DNS, VIP |

> 요약: 복제 구조는 primary 로그를 replica에 전달하고, 장애 시 라우팅 계층이 승격된 노드로 쓰기를 전환한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
트랜잭션 commit -> 로그 기록
  / 동기: replica ack 수신 -> client 응답
  / 비동기: client 응답 -> replica 전송
Replica replay -> lag 측정 -> 장애 감지 -> failover
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | primary가 트랜잭션 로그를 순서대로 기록 | commit order 보존 |
| 2 | replica가 로그를 수신하고 디스크에 반영 | receive lag, replay lag |
| 3 | 읽기 요청을 replica로 분산 | stale read 허용 범위 |
| 4 | primary 장애 감지 후 replica 승격 | RTO 1~5분 목표 |
| 5 | 이전 primary 격리 후 재합류 | split-brain 0건 |

> 요약: 복제는 로그 순서 보존, lag 관측, 장애 승격, 이전 primary 격리까지 하나의 운영 흐름으로 관리해야 한다.

---

## Ⅳ. 특징

| 구분 | 단일 DB | 복제 적용 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 읽기 부하 | primary 집중 | replica로 분산 | replica QPS와 lag 동시 측정 |
| 장애 대응 | 복구 전 중단 | replica 승격 | RTO 1~5분, RPO 0~수초 |
| commit 지연 | 로컬 지연 | 동기 복제 시 네트워크 지연 추가 | p95 commit latency |
| 데이터 손실 | 장애 시 로그 복구 의존 | 비동기 lag만큼 손실 가능 | lag 1초 이하 목표 |
| 운영 난도 | 구조 단순 | split-brain·failover 관리 | quorum·fencing 필수 |

> 요약: 복제는 읽기 분산과 복구 경로를 제공하지만, 동기성 선택에 따라 지연과 데이터 손실 허용치가 달라진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 가용성 | 단일 인스턴스 | primary-replica | RTO 5분 이하 요구 |
| 일관성 | 동기 commit | 비동기 복제 | RPO 0이면 동기, 수초 허용이면 비동기 |
| 쓰기 확장 | primary 단일 writer | multi-master 대안 | 지역별 write 필요 시 충돌 정책 전제 |
| 읽기 | primary 조회 | read replica | 읽기 QPS가 쓰기 대비 5배 이상 |
| 재해복구 | 백업 복원 | 원격 replica | RPO 15분 이하 요구 |

> 요약: RPO 0이 필수면 동기 복제, 지연 최소화가 우선이면 비동기 복제와 lag 관측을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 복제 지연 | 네트워크·replica IO 병목 | lag 알람, replica 증설, 쿼리 제한 | replay lag seconds |
| Split-brain | 네트워크 분리 중 이중 승격 | quorum, fencing, STONITH | dual-primary 발생 건수 |
| 데이터 손실 | 비동기 로그 미전송 | semi-sync, RPO 정책, commit 확인 | lost transaction count |
| 읽기 불일치 | replica stale read | read-your-writes 라우팅 | stale read 비율 |

> 요약: 복제 운영의 핵심 리스크는 lag와 split-brain이며, quorum과 lag 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| RTO | 자동 failover 1~5분 | 장애 훈련, failover log |
| RPO | 동기 0, 비동기 1~10초 | WAL LSN 차이, binlog position |
| Lag | replay lag 1초 이하 | DB replication metrics |

> 요약: 복제 품질은 RTO/RPO, replay lag, 읽기 지연, split-brain 발생 여부로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 업무 등급화: 결제·잔액은 동기 또는 semi-sync, 피드·알림은 비동기 replica로 분리하고 RPO 값을 서비스별로 명시함
2. 장애 전환: Patroni, Orchestrator, MHA 등으로 health check, quorum, fencing, DNS/VIP 전환 절차를 자동화함
3. 읽기 라우팅: read-your-writes가 필요한 요청은 primary 또는 session-consistent replica로 보내고, 리포트 쿼리는 전용 replica에서 실행함

**결론 (2줄):**
- 기술사 판단: RPO 0 업무는 동기 복제, 지연 민감 업무는 비동기 복제와 보상 절차를 결합하는 선택이 타당함
- 향후 방향: 클라우드 관리형 DB는 cross-AZ 복제와 자동 failover를 기본 제공하지만, lag 기반 라우팅과 split-brain 검증은 서비스 책임으로 남음

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DB 복제를 설명하시오", "기술하시오" | 로그 전파, 동기/비동기, failover 흐름 | 읽기 분산·가용성·지연 비교 |
| 요구사항 명시형 | "장애 대응 방안을 제시하시오", "비교하시오" | RTO/RPO 기반 장애 전환 절차 | lag, split-brain, 데이터 손실 대응 |

> 요약: 설명형은 복제 구조를 넓게, 장애 대응형은 RTO/RPO와 failover 절차를 중심으로 답안을 구성한다.
