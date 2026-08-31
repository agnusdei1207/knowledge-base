---
sidebar:
  order: 100
  label: "100. 데이터베이스 복제: 마스터-슬레이브•멀티마스터"
  badge:
    text: "미출 · 50%"
    variant: note
title: "데이터베이스 복제: 마스터-슬레이브•멀티마스터 (Database Replication)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 100
extra:
  question_no: "100"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "복제 지연•일관성•장애전환 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **데이터베이스 복제(Replication)**: 원본 노드의 데이터 변경 이력(Binary Log / WAL)을 보조 노드로 지속 전파하여 고가용성(HA)과 읽기 분산을 실현하는 기술.
- **Primary-Replica (Master-Slave)**: 쓰기(Write)를 전담하는 Primary 노드와 읽기(Read)를 분산 처리하는 다수의 Replica 노드로 구성된 복제 모델.

</details>

- 정의/개념: 고가용성(HA)과 읽기 트래픽 분산을 위해 **주 노드의 변경 로그(Binlog/WAL)를 복제 노드로 전파·재생**하는 데이터베이스 이중화 기술
- 배경/필요성: 단일 데이터베이스 노드의 하드웨어 장애 시 발생하는 서비스 전면 중단(SPOF)과 폭증하는 읽기 트래픽으로 인한 주 노드(Primary)의 리소스 고갈 문제를 극복하고, 트랜잭션 변경 로그(Binary Log / WAL)를 복제 노드(Replica)로 실시간 전파·재생함으로써 **고가용성(HA, 무중단 자동 Failover)을 확보하고 대규모 읽기 트래픽의 수평 분산 처리를 실현**할 필요

#### 한줄 요약
- 복제는 가용성과 읽기 처리량을 사본 수만큼 늘리는 대신 원본과 사본 사이에 시차를 만들므로, 복제 지연을 허용할 수 있는 질의만 사본으로 보낼 수 있다는 제약이 함께 따라온다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Replication Lag(복제 지연)**: Primary에서 커밋된 데이터가 네트워크 지연이나 Replica의 I/O 경합으로 인해 복제본에 늦게 반영되는 시차 현상.
- **Failover(장애 조치)**: Primary 노드 장애 시 가장 최신 로그를 보유한 Replica 노드를 새로운 Primary로 자동 승격시키는 절차.

</details>

- 주 노드는 쓰기, 복제 노드는 읽기를 전담하는 **Read/Write 분리 아키텍처**
- 요구사항에 따라 선택하는 **동기(Sync), 반동기(Semi-Sync), 비동기(Async) 복제** 지원
- 네트워크 및 복제 노드 부하에 따른 **복제 지연(Replication Lag) 관리 트레이드오프**

#### 한줄 요약
- 읽기 부하 분산과 자동 페일오버를 지원하되, 복제 지연에 따른 일관성을 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Binlog & Relay Log**: MySQL Primary가 생성하는 Binary Log와 이를 Replica가 수신하여 로컬에 저장하는 Relay Log.

</details>

```text
[데이터베이스 복제 구성]
|-- Primary 노드
|-- I/O Thread
|-- SQL Thread
`-- 장애 감지기
```

선의 의미: 변경 로그 복제와 장애 전환을 담당하는 구성

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| Primary 노드 (Master) | 모든 CUD 쓰기 트랜잭션을 처리하고 **Binary Log를 디스크에 순차 생성** | 시스템 내 유일한 쓰기 원천 (SSOT) |
| I/O Thread (Replica) | Primary의 Binlog 덤프를 네트워크로 수신하여 **Relay Log에 순차 저장** | 네트워크 연결 유지 및 수신 전담 |
| SQL Thread (Replica) | Relay Log에 기록된 트랜잭션을 읽어 **복제 노드 스토리지 엔진에 순차 재생** | 멀티스레드 복제(MTS)로 병렬 처리 |
| 장애 감지기 (Orchestrator) | Primary 헬스체크 및 다운 시 **최신 Replica를 Primary로 자동 승격(Failover)** | 쿼럼 기반 스플릿 브레인 방지 |

#### 한줄 요약
- 데이터를 통째로 복사하지 않고 변경 로그만 전송해 재생하므로 네트워크 비용이 변경량에만 비례하지만, 재생이 단일 스레드에 묶이면 원본의 쓰기 속도가 그대로 복제 지연의 원인이 된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Semi-Synchronous Replication**: Primary가 커밋할 때 최소 1개의 Replica가 Relay Log에 기록 완료 신호(ACK)를 보낼 때까지 대기하는 복제 방식.

</details>

```text
클라이언트가 Primary 노드에 데이터 쓰기 요청 (`UPDATE Balance ...`)
        │
   [Primary 트랜잭션] InnoDB 스토리지에 커밋 후 Binary Log에 이벤트 기록
        │
   [네트워크 전송] Dump Thread가 변경된 Binlog 이벤트를 Replica로 전송
        │
   [Relay Log 저장] Replica의 I/O Thread가 수신하여 로컬 Relay Log에 기록
        │
   [복제 동기화 방식 판정]
   ┌────┴───────────────────────────┐
[Asynchronous (비동기)]         [Semi-Synchronous (반동기)]
Primary가 Replica 응답을         Replica가 Relay Log 기록 후 ACK 전송
기다리지 않고 즉시 클라이언트에 응답   Primary가 ACK 수신 후 클라이언트에 응답
        │                                 │
   Replica의 SQL Thread가 Relay Log를 순차 재생하여 로컬 데이터 동기화 완료
```

#### 한줄 요약
- 커밋 응답을 이 경로의 어느 지점에서 돌려주느냐가 복제 방식을 가르며, 비동기는 응답 지연을 없애는 대신 장애 시 미전송 로그를 잃고 동기는 그 손실을 없애는 대신 커밋마다 네트워크 왕복을 더한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **비동기 vs 반동기 vs 동기 복제**: 성능 우선의 비동기, 성능/안전성 절충의 반동기, 100% 무손실 동기 복제.

</details>

| 비교 항목 | Asynchronous (비동기식) | Semi-Synchronous (반동기식) | Synchronous (동기식: Galera, 2PC) |
|:---|:---|:---|:---|
| Primary 쓰기 지연 | **가장 짧음 (로컬 커밋 즉시 반환)**| 약간 증가 (최소 1대 ACK 대기) | 높음 (모든 복제본 커밋 완료 대기) |
| 장애 시 데이터 유실 | **미전파 로그 유실 위험 (RPO > 0)**| **최소 1대 복제본 보존 (RPO $\approx$ 0)**| **데이터 유실 0 (RPO = 0 완벽 보장)** |
| 네트워크 의존도 | 낮음 | 보통 | 매우 높음 (네트워크 지연 시 쓰기 블로킹) |
| 실무 권장 표준 | 일반 웹 서비스 읽기 분산 | **엔터프라이즈 미션 크리티컬 표준** | 금융 결제 및 글로벌 분산 합의 DB |

#### 한줄 요약
- 지연 최소화는 비동기, 데이터 안전과 성능의 균형은 반동기, 무손실 정합성은 동기 복제를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Read-Your-Own-Writes Consistency**: 사용자가 정보 수정 후 즉시 조회할 때 복제 지연을 피하기 위해 해당 사용자의 읽기 요청만 Primary로 라우팅하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 복제 지연으로 사용자가 본인이 쓴 글을 즉시 조회 불가 | **세션 토큰 기반 '방금 수정한 사용자' 요청은 Primary로 강제 라우팅** | Read-Your-Own-Writes 정합성 보장 |
| Primary 장애 시 잘못된 승격으로 이중 마스터(**Split-Brain**) 발생 | **MySQL Orchestrator 기반 쿼럼 투표 및 Raft 합의 펜싱(STONITH)** | 데이터 오염 및 충돌 원천 차단 |
| 단일 SQL Thread 병목으로 Replication Lag 눈덩이 폭증 | **Multi-Threaded Slave (MTS: `replica_parallel_workers=8`) 활성화** | 릴레이 로그 병렬 재생으로 지연 해소 |
| Replica 과부하로 인한 서비스 지연 | **ProxySQL 또는 L7 로드밸런서를 통한 가중치 기반 읽기 분산** | 안정적인 읽기 트래픽 처리 |

#### 한줄 요약
- Read-Your-Own-Writes 라우팅, Orchestrator 쿼럼 페일오버, MTS 병렬 재생, ProxySQL 분산으로 최적화한다.

## Ⅶ. 결론

- 엔터프라이즈 영속성 계층의 가용성 보장 및 고트래픽 읽기 분산을 위한 **핵심 표준 이중화 아키텍처**로 확립되었으며, 실무 운영 시에는 **데이터 유실 위험을 억제하면서 쓰기 지연을 최소화하는 반동기(Semi-Synchronous) 복제 채택, 복제 지연(Lag)에 따른 정합성 훼손을 방지하는 Read-Your-Own-Writes 라우팅 및 Multi-Threaded Slave(MTS) 병렬 재생, 장애 시 스플릿 브레인(Split-Brain)을 원천 차단하는 Orchestrator 쿼럼 기반 자동 승격 체계**를 결합하여 서비스 연속성과 데이터 일관성을 동시 보증

#### 한줄 요약
- 데이터베이스 복제는 변경 로그 전파를 통해 데이터 가용성과 읽기 확장성을 확보하는 현대 데이터 플랫폼의 필수 인프라 아키텍처다.
