---
sidebar:
  order: 100
  label: "100. 데이터베이스 복제: 마스터-슬레이브•멀티마스터 (Database Replication)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "데이터베이스 복제: 마스터-슬레이브•멀티마스터 (Database Replication)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 100
extra:
  question_no: "100"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "복제 지연•일관성•장애전환 설계 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Database Replication (데이터베이스 복제)**: 데이터베이스의 가용성(High Availability), 재해 복구(DR), 트래픽 분산(Read Scale-Out)을 위해, 원본 데이터베이스 노드의 갱신 데이터(Binary Log / Write-Ahead Log)를 1개 이상의 타 데이터베이스 노드로 지속 동기화하는 물리적 복제 아키텍처.
- **Master-Slave (Primary-Replica) Architecture**: 주 노드(Primary/Master)는 100% Write(CUD) 및 Read를 담당하고, 복제 노드(Replica/Slave)는 오직 Read 전용 쿼리를 분산 처리하거나 주 노드 장애 시 승격(Failover)되는 형태.
- **Multi-Master (Primary-Primary) Architecture**: 2개 이상의 노드가 동시에 Write 및 Read 연산을 각각 독립 처리하며, 노드 간 변경 사항을 양방향 동기화하는 구조.

</details>

- 정의/개념: 데이터베이스의 가용성과 읽기 성능 확장을 목적으로, 데이터 갱신 트랜잭션 로그를 복제 대상 노드로 실시간 전파하여 사본(Copy)을 유지하는 아키텍처인 **Database Replication**
- 배경/필요성: 단일 데이터베이스 노드 장애 발생 시 서비스 중단(Downtime) 차단 및 RTO/RPO 0에 가까운 Failover 시스템 정립, 읽기 트래픽 폭증 시 Read Scale-Out 분산 처리 요구성

#### 한줄 요약

- 원본 장부의 변경 일지를 다른 지점에 보내 같은 사본을 유지하는 방식이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Replication Lag (복제 지연)**: 주 노드에서 Commit된 변경 데이터가 네트워크 지연이나 복제 노드의 락 경합으로 인해 복제 노드에 뒤늦게 반영되는 시간차 현상.
- **Failover / Failback**: 주 노드 다운 시 복제 노드를 새로운 주 노드로 자동/수동 승격(Failover)시키는 고가용성 프로세스.

</details>

- **Read Scale-Out (읽기 쿼리 부하 분산)** 및 고가용성(**HA**) 확보
- **Synchronous (동기식) vs Asynchronous (비동기식) vs Semi-Synchronous (반동기식)** 복제 방식
- **Replication Lag (복제 지연)** 발생에 따른 읽기 정합성(Read Consistency) 파괴 수용

#### 한줄 요약

- 사본이 늘면 읽기와 장애 대응은 좋아지지만 최신성 지연과 원본 충돌을 관리해야 한다.

## Ⅲ. 구조 및 구성요소 (Master-Slave 대 Multi-Master 아키텍처)

<details><summary>핵심 용어</summary>

- **Binary Log (Binlog) / WAL (Write-Ahead Log)**: MySQL의 Binlog, PostgreSQL의 WAL 등 데이터 변경 이력이 이진 형태로 기록되는 파일로, 복제 노드가 이를 읽어 롤-포워드(Replay) 수행.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Database Replication 2대 구조                        │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Master-Slave (Primary-Replica) │ 2. Multi-Master (Primary-Primary)  │
├───────────────────────────────────┼────────────────────────────────────┤
│   [Primary Node (Write / Read)]   │ [Primary Node A] ◄──(Bi-Direction)│
│                 │ (Binlog Replication)                 │               │
│                 ▼                 │                    ▼               │
│   [Replica Node (Read Only)]      │ [Primary Node B] (Conflict Resolution)│
└───────────────────────────────────┴────────────────────────────────────┘
```

선의 의미: Master-Slave는 단방향 단일 쓰기 구조, Multi-Master는 양방향 다중 쓰기 및 충돌 해결(Conflict Resolution) 필요 구조 아키텍처.

| 구분 (Category) | Master-Slave (Primary-Replica) | Multi-Master (Primary-Primary) |
|:---|:---|:---|
| **쓰기(Write) 권한** | **단 1개의 Primary 노드만 쓰기 전용 처리** | **2개 이상의 Primary 노드가 각각 쓰기 처리** |
| **읽기(Read) 권한** | Primary 및 모든 Replica 노드에 분산 가능 | 모든 Primary 노드에 자유롭게 분산 처리 |
| **데이터 충돌 위험** | **충돌 0% (단일 쓰기 원천이므로 충돌 없음)** | **충돌 위험 매우 높음 (동시 수정 시 충돌 해결 필요)** |
| **Failover 난이도** | Replica 노드 중 1개를 Primary로 승격 | 승격 절차 없이 기존 타 Primary 노드로 전환 |

#### 한줄 요약

- 원본 장부와 변경 일지, 사본, 감시자, 승격 담당자로 구성된다.

## Ⅳ. 흐름도 (3대 복제 동기화 동기식/비동기식/반동기식)

<details><summary>핵심 용어</summary>

- **Semi-Synchronous Replication (반동기식 복제)**: 주 노드가 트랜잭션 Commit 시 최소 1개 이상의 복제 노드가 릴레이 로그(Relay Log)에 복제 완료 신호(ACK)를 보낼 때까지 기다린 후 최종 Commit 응답을 보내는 타협 방식.

</details>

```text
[1. Asynchronous (비동기식)]
 Primary Commit ──► Client 응답 ──► (네트워크) ──► Replica 전파 (지연 손실 위험)

[2. Synchronous (동기식)]
 Primary Commit ──► (네트워크) ──► Replica Flush ──► ACK 응답 ──► Client 응답 (지연 높음)

[3. Semi-Synchronous (반동기식)]
 Primary Commit ──► (네트워크) ──► 1개 Replica ACK ──► Client 응답 (안전/속도 타협)
```

### 동작 원리

1. **Asynchronous**: Primary가 Write 완료 후 즉시 클라이언트에 응답. 속도 최상이지만 Primary 다운 시 복제 안 된 데이터 유실 (RPO > 0).
2. **Synchronous**: 모든 Replica 노드가 쓰기 완료 ACK를 보낼 때까지 클라이언트 응답 대기. 데이터 유실 0% (RPO=0)이지만 쓰기 성능 극도로 저하.
3. **Semi-Synchronous**: 1개 이상의 Replica 노드에 릴레이 로그 작성 ACK만 수신되면 성공 반환. 데이터 유실 방지와 속도 균형 달성.

#### 한줄 요약

- 원본이 변경 일지를 보내고 사본의 확인 수준과 따라오는 속도를 계속 측정한다.

## Ⅴ. 종류 및 비교 (동기식 대 비동기식 대 반동기식)

<details><summary>핵심 용어</summary>

- **RPO & RTO in Replication**: 비동기식은 RPO>0(데이터 유실 가능), 동기식/반동기식은 RPO=0(유실 소멸).

</details>

| 비교 항목 | Asynchronous (비동기식 복제) | Semi-Synchronous (반동기식 복제) | Synchronous (동기식 복제) |
|:---|:---|:---|:---|
| **쓰기 latency (응답속도)**| **최상 (대기 시간 0)** | **중간 (1개 노드 ACK 대기)** | 최하 (모든 노드 ACK 대기) |
| **데이터 유실 위험 (RPO)**| **있음 (Primary 장애 시 유실)** | **거의 없음 (1개 노드 안전)** | **없음 (RPO = 0 완벽 보장)** |
| **네트워크 의존성** | 낮음 | 중간 | 매우 높음 (네트워크 지연 시 블로킹) |
| **실무 표준 채택성** | **일반 서비스 표준** | **금융/보안 서비스 표준** | 특수 결제 시스템 일부 수용 |

#### 한줄 요약

- 복제 방식 선택 기준에서 한 원본은 순서가 단순하고 여러 원본은 가까이서 쓸 수 있지만 충돌 해결이 필요하다.

## Ⅵ. 실무 고려사항 및 대책 (Replication Lag 읽기 정합성 극복)

<details><summary>핵심 용어</summary>

- **Read-Your-Own-Writes Consistency**: 사용자가 본인 프로필 수정 직후 조회 시, 복제 지연이 일어나는 Replica가 아닌 Primary 노드로 쿼리를 강제 우회시켜 본인이 수정한 최신 데이터를 즉시 확인케 하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Replica 복제 지연으로 방금 작성한 글이 조회 안 됨 | **수정 직후 5초간 primary 노드로 읽기 쿼리 라우팅 (Read-Your-Writes)**| 정합성 보장 |
| Primary 노드 다운 시 수동 Failover 시 Downtime 폭증 | **Orchestrator / MHA / Patroni 기반 자동 Failover 구축** | RTO 최소화 |
| Replica 노드의 읽기 트래픽 과부하 | **HAProxy / ProxySQL / AWS Route53 라운드로빈 쿼리 분산**| Read Scale-Out 완결 |

> 사례: **MySQL Master-Replica + ProxySQL Read/Write Splitting & Semi-Sync 적용**

#### 한줄 요약

- 사본이 늦으면 최신 값이 필요한 읽기에서 빼고, 원본 장애 때 둘이 동시에 원본이 되지 않게 막아야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **복제 수립 기준(Database Replication Standards)**: RPO/RTO 목표치, Replication Lag 관용성 및 ProxySQL Read/Write 분손성에 의거한 체계.

</details>

- **복제 수립 기준**에 따라 대용량 OLTP 가용성 구축 시 **Master-Replica + Semi-Sync & ProxySQL 분산** 필수 수용

#### 한줄 요약

- 복제 운영 검증 기준은 최신 사본•원본 권한•장애 손실 범위를 함께 정한다.
