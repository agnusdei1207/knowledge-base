---
sidebar:
  order: 100
  label: "100. 데이터베이스 복제: 마스터-슬레이브•멀티마스터 (Database Replication)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "데이터베이스 복제: 마스터-슬레이브•멀티마스터 (Database Replication)"
date: "2026-08-13T20:14:00+09:00"
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

- **Database Replication (데이터베이스 복제)**: 데이터베이스의 가용성(High Availability), 재해 복구(DR), 트래픽 분산(Read Scale-Out)을 위해, 원본 데이터베이스 노드의 갱신 데이터(Binary Log / Write-Ahead Log)를 1개 이상의 타 데이터베이스 노드로 지속 동기화하는 물리적 복제 아키텍처.
- **Master-Slave (Primary-Replica) Architecture**: 주 노드(Primary/Master)는 100% Write(CUD) 및 Read를 담당하고, 복제 노드(Replica/Slave)는 오직 Read 전용 쿼리를 분산 처리하거나 주 노드 장애 시 승격(Failover)되는 형태.
- **Multi-Master (Primary-Primary) Architecture**: 2개 이상의 노드가 동시에 Write 및 Read 연산을 각각 독립 처리하며, 노드 간 변경 사항을 양방향 동기화하는 구조.

</details>

- 정의/개념: 변경 로그를 다른 노드에 반영하는 **데이터베이스 복제**
- 배경/필요성: 단일 DB 장애로 **서비스 중단•데이터 손실** 위험 집중

#### 한줄 요약

- 원본 장부의 변경 일지를 다른 지점에 보내 같은 사본을 유지하는 방식이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Replication Lag (복제 지연)**: 주 노드에서 Commit된 변경 데이터가 네트워크 지연이나 복제 노드의 락 경합으로 인해 복제 노드에 뒤늦게 반영되는 시간차 현상.
- **Failover / Failback**: 주 노드 다운 시 복제 노드를 새로운 주 노드로 자동/수동 승격(Failover)시키는 고가용성 프로세스.

</details>

- **읽기 부하 분산**: 복제 노드 활용을 통한 읽기 성능 향상 및 고가용성(`HA`) 확보.
- **복제 방식**: 동기식(`Synchronous`), 비동기식(`Asynchronous`), 반동기식(`Semi-Synchronous`) 복제 지원.
- **운영 Trade-off**: 복제 지연(`Replication Lag`) 발생에 따른 읽기 정합성 관리 필요.

#### 한줄 요약

- 사본이 늘면 읽기와 장애 대응은 좋아지지만 최신성 지연과 원본 충돌을 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Binary Log (Binlog) / WAL (Write-Ahead Log)**: MySQL의 Binlog, PostgreSQL의 WAL 등 데이터 변경 이력이 이진 형태로 기록되는 파일로, 복제 노드가 이를 읽어 롤-포워드(Replay) 수행.

</details>

```text
[주 노드] ───── [변경 로그]
    │                 │
[복제 노드] ─── [복제 관리자]
    │                 │
[읽기 라우터] ── [장애 감지기]
```

선의 의미: 변경 전파•읽기 분산•장애 승격 책임 간 정적 협력 관계.

| 구성요소 | 책임 |
|:---|:---|
| 주 노드 | 쓰기 처리와 변경 로그 생성 |
| 변경 로그 | 커밋 순서와 변경 내용을 지속 보관 |
| 복제 노드 | 로그 재생과 읽기 요청 처리 |
| 복제 관리자 | 전송 위치•지연•오류 상태 관리 |
| 읽기 라우터 | 최신성 요구에 따라 읽기 노드 선택 |
| 장애 감지기 | 주 노드 판정과 승격 절차 조정 |

#### 한줄 요약

- 원본 장부와 변경 일지, 사본, 감시자, 승격 담당자로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Semi-Synchronous Replication (반동기식 복제)**: 주 노드가 트랜잭션 Commit 시 최소 1개 이상의 복제 노드가 릴레이 로그(Relay Log)에 복제 완료 신호(ACK)를 보낼 때까지 기다린 후 최종 Commit 응답을 보내는 타협 방식.

</details>

```text
[쓰기 요청]
     │
     ▼
1. 변경 로그 기록
     │
     ▼
2. 복제 노드 전송
     │
     ▼
3. 변경 로그 재생
     │
     ▼
4. 확인 수준 판정
     │
     ▼
5. 지연•오류 감시
     │
     ▼
 [응답 반환]
```

### 동작 원리

1. 변경 로그 기록: 주 노드가 커밋 순서와 변경 내용 저장
2. 복제 노드 전송: 로그 위치 이후 변경분 전달
3. 변경 로그 재생: 복제 노드가 순서대로 데이터 반영
4. 확인 수준 판정: 동기 방식별 ACK 충족 여부 확인
5. 지연•오류 감시: 재생 위치와 장애 징후 측정

#### 한줄 요약

- 원본이 변경 일지를 보내고 사본의 확인 수준과 따라오는 속도를 계속 측정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RPO & RTO in Replication**: 확인 범위와 장애 지점에 따라 허용 가능한 손실량과 복구 시간이 달라지는 목표.

</details>

| 구분 | Asynchronous (비동기식 복제) | Semi-Synchronous (반동기식 복제) | Synchronous (동기식 복제) |
|:---|:---|:---|:---|
| 쓰기 지연 | 로컬 커밋 후 응답 | 지정 복제 노드 ACK 대기 | 합의 범위 ACK 대기 |
| 데이터 유실 위험 | 미전파 로그 손실 가능 | ACK 위치 이후 장애 조건별 상이 | 합의 범위 내 로그 보존 |
| 네트워크 의존성 | 낮음 | 중간 | 매우 높음 (네트워크 지연 시 블로킹) |
| 적합 환경 | 지연 민감•손실 일부 허용 | 지연•내구성 균형 | 엄격한 내구성•일관성 요구 |

#### 한줄 요약

- 복제 방식 선택 기준에서 한 원본은 순서가 단순하고 여러 원본은 가까이서 쓸 수 있지만 충돌 해결이 필요하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Read-Your-Own-Writes Consistency**: 사용자가 본인 프로필 수정 직후 조회 시, 복제 지연이 일어나는 Replica가 아닌 Primary 노드로 쿼리를 강제 우회시켜 본인이 수정한 최신 데이터를 즉시 확인케 하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 복제 지연으로 최신 읽기 실패 | **세션 토큰•주 노드 라우팅** | Read-Your-Writes 확보 |
| 오판 승격으로 이중 주 노드 발생 | **쿼럼•펜싱•자동 장애전환** | Split-Brain 차단 |
| 복제 노드 읽기 과부하 | **지연 가중 라우팅•부하 제한** | 읽기 부하 분산 |

> 사례: **MySQL Master-Replica + ProxySQL Read/Write Splitting & Semi-Sync 적용** #### 한줄 요약

- 사본이 늦으면 최신 값이 필요한 읽기에서 빼고, 원본 장애 때 둘이 동시에 원본이 되지 않게 막아야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **복제 수립 기준(Database Replication Standards)**: RPO/RTO 목표치, Replication Lag 관용성 및 ProxySQL Read/Write 분손성에 의거한 체계.

</details>

- 지연 우선은 **비동기**, 손실 제한은 반동기•동기 복제 선택

#### 한줄 요약

- 복제 운영 검증 기준은 최신 사본•원본 권한•장애 손실 범위를 함께 정한다.
