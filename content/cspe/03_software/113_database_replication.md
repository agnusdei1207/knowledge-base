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
- **개요**: **고가용성(HA)**과 읽기 부하 분산을 위해 원본(Primary) DB의 **트랜잭션 로그**(WAL·binlog)를 다른 노드(Replica)에 전달해 동일한 데이터 사본을 유지하는 **데이터베이스 복제** 기법이다.
- **왜 필요한가**: 단일 DB는 장애가 나면 서비스가 멈추고, 조회·리포트 쿼리가 몰리면 쓰기 성능도 떨어진다. 복제는 사본을 여러 곳에 두어 읽기를 분산하고, 원본이 죽어도 사본이 업무를 이어받게 한다.
- **핵심 직관**: 본점 장부의 거래를 지점 장부에도 실시간으로 옮겨 적어 두면, 지점에서도 조회할 수 있고 본점이 문을 닫아도 지점이 영업을 대신할 수 있다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 고가용성(HA) | 장애가 나도 서비스가 끊기지 않는 성질 — 복제가 이루려는 **목적** | 본점이 쉬어도 지점은 영업 |
| 트랜잭션 로그(WAL·binlog) | DB에 가해진 모든 변경을 순서대로 적은 로그 — 복제가 전달하는 **내용물** | 거래 순서를 적은 전표 뭉치 |
| Primary(원본) | 쓰기를 처리하고 로그를 생성하는 노드 | 본점 |
| Replica(사본) | 로그를 받아 재실행해 동일 데이터를 유지하는 노드 | 지점 |
| 동기(Sync) 복제 | commit을 replica의 수신 확인(ack) 후 완료 | "지점 확인받고서야 거래 종료" |
| 비동기(Async) 복제 | commit을 먼저 끝내고 로그는 뒤이어 전송 | "일단 거래 종료, 전표는 나중에 발송" |
| Replication Lag | replica가 primary보다 뒤처진 시간(초) | 지점 장부가 본점보다 며칠 늦음 |
| Failover | primary 장애 시 replica를 새 primary로 승격하는 절차 | 지점이 본점 업무를 대행 |
| Split-brain | 두 노드가 동시에 자신을 primary라 믿고 쓰기를 받는 장애 | 본점이 둘로 나뉘어 각자 영업 |
| Quorum·Fencing | 과반 동의로 승격을 결정하고, 옛 primary를 강제 격리하는 절차 | 과반 지점이 동의해야 새 본점 인정, 옛 본점은 폐쇄 |
| RTO / RPO | 복구까지 걸리는 시간 / 손실을 허용하는 데이터 범위(시간) | 복구 소요 시간 / 잃어도 되는 거래 범위 |

## 깊이 이해

### 왜 복제가 필요했나 (배경)
- 서비스가 커지면 두 가지 문제가 동시에 온다. 첫째, 단일 DB의 하드웨어·네트워크 장애가 곧 전체 서비스 중단으로 이어진다. 둘째, 상품 조회·통계 같은 읽기 쿼리가 쓰기 트랜잭션과 같은 DB를 두고 경쟁해 지연이 커진다.
- 복제는 원본의 트랜잭션 로그를 다른 노드에 계속 흘려보내 "같은 데이터를 가진 여분의 DB"를 만들어 이 두 문제를 함께 완화한다.

### 동기 vs 비동기 — 지연과 손실의 트레이드오프 (수치로 이해)
- **동기 복제**: primary가 commit을 확정하기 전 replica의 ack를 기다린다. replica가 100km 떨어진 리전에 있고 왕복 지연이 20ms라면, 모든 쓰기 트랜잭션에 최소 20ms가 추가된다. 대신 replica가 primary와 항상 같은 데이터를 갖고 있으므로 **RPO=0**(데이터 손실 없음)을 보장한다.
- **비동기 복제**: primary는 로그를 디스크에 쓰자마자 commit을 끝내고, replica 전송은 별도로 진행한다. 지연은 없지만, primary가 초당 1,000건을 처리하는데 replica가 초당 800건만 반영할 수 있다면 매초 200건씩 lag가 쌓여 30초면 6,000건 차이가 벌어질 수 있다. 이 순간 primary가 죽으면 아직 반영 못 한 거래는 **유실**된다.
- **semi-sync(절충)**: N개 replica 중 최소 1개의 수신 확인만 기다리고 commit한다. 완전 동기보다 지연은 적고, 완전 비동기보다는 손실 위험이 작다.

### 장애 감지와 failover — RTO/RPO로 계산해보기
- 헬스체크가 10초 간격으로 3회 연속 실패해야 장애로 판정한다면 장애 인지까지 최대 30초가 걸린다. 여기에 replica 승격 10~20초, DNS/VIP 전환 10~30초가 더해지면 전체 **RTO는 약 1~2분**이 된다.
- 이 replica가 평소 비동기 lag 2초로 운영되고 있었다면, 장애 순간 아직 replica에 반영되지 못한 최대 2초치 거래가 **RPO**(유실 가능 범위)가 된다. 즉 RTO는 "얼마나 빨리 복구하는가", RPO는 "얼마나 잃을 수 있는가"이며, 둘 다 lag와 자동화 수준에 의해 결정된다.

### Split-brain이 생기는 이유와 quorum·fencing
- 3대(primary 1 + replica 2)로 구성된 클러스터에서 네트워크가 끊겨 primary가 나머지 2대와 통신할 수 없게 됐다고 하자. primary는 "내가 여전히 원본"이라 믿고 쓰기를 계속 받을 수 있는데, 동시에 남은 2대는 과반(quorum=2/3)을 확보했다고 판단해 그중 하나를 새 primary로 승격시키면 **두 개의 primary가 동시에 쓰기를 받는 split-brain**이 발생한다.
- 이를 막는 것이 quorum·fencing이다. 과반 노드의 동의 없이는 승격을 진행하지 않고(quorum), 통신이 끊긴 옛 primary는 스스로 쓰기를 중단하거나 클러스터가 강제로 그 노드를 격리한다(fencing, STONITH). 위 예시에서 고립된 옛 primary는 과반(2/3)을 얻지 못하므로 자신을 primary로 유지할 명분이 없어 write를 거부해야 한다.

### 비유와 흔한 오해
- **비유**: 본점과 지점의 통신이 끊기면, 지점 확인 없이는 같은 잔액을 보장할 수 없다. 확인을 기다리면(동기) 거래가 느려지고, 기다리지 않으면(비동기) 나중에 장부가 어긋날 위험이 생긴다.
- **오해 1**: "복제 = 백업"이 아니다. 복제는 실시간 사본이라 원본의 논리적 오류(잘못된 DELETE 등)도 그대로 전파된다. 특정 시점으로 되돌리는 복구에는 별도 백업이 필요하다.
- **오해 2**: replica를 늘리면 쓰기도 빨라진다고 착각하기 쉽지만, 읽기만 분산될 뿐 쓰기는 여전히 primary 한 대의 처리량에 묶인다. 쓰기 확장이 필요하면 multi-master(여러 노드가 동시에 쓰기 수용)를 검토해야 하는데, 이 경우 서로 다른 노드에서 같은 데이터를 동시에 고친 충돌을 해결할 정책이 별도로 필요하다.

## 연결 개념
- WAL·binlog — 복제가 전달하는 변경 로그의 원천
- Failover·Quorum·Fencing — primary 장애 시 승격과 split-brain 방지 절차
- RTO/RPO — 복제 방식(동기/비동기)을 정하는 정량적 기준
- CAP 정리 — 복제된 노드 간 일관성·가용성 트레이드오프의 일반 이론(117에서 상세)

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

- 개요: DB 복제는 변경 로그 기반 사본 유지 기법이다.
- 배경: 단일 DB 장애, 읽기 부하 집중, 지역 지연, 백업 작업이 primary writer에 몰리면 서비스 중단과 응답 지연이 발생한다.
- 필요성: WAL/binlog, sync/async replica, failover, RTO/RPO, replication lag 기준으로 복제 방식을 선택해야 한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
