---
title: "데이터베이스 복제 — 마스터-슬레이브·멀티마스터 (Database Replication)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 113
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: DB 데이터를 물리적으로 분리된 여러 서버(노드)에 실시간으로 복사하여 일치시키는 고가용성·분산 아키텍처
- **왜 필요한가**: DB 서버가 1대뿐이면 서버 고장 시 전체 서비스가 멈추고(SPOF), 트래픽이 몰릴 때 읽기 쿼리 부하를 견딜 수 없다.
- **핵심 직관**: 메인 작가(Master)가 원고를 쓰면, 보조 작가(Slave) 여러 명이 그 원고를 그대로 복사해 들고 있는다. 독자(사용자)들은 보조 작가들의 복사본을 나눠 읽어 메인 작가가 쓰는 데만 집중하게 한다.

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| Master (Primary) | 쓰기(Insert/Update/Delete) 트랜잭션을 처리하는 메인 서버 | 원본 장부를 쓰는 회계사 |
| Slave (Replica / Secondary) | Master의 변경 내역을 받아 반영하고, 읽기(Select)를 담당하는 서버 | 복사본 장부를 열람시켜주는 직원 |
| Binlog (Binary Log) | DB 변경 사항을 시간 순으로 기록한 로그 파일. 복제의 핵심 매개체 | 수정 내역이 적힌 작업 일지 |
| Replication Lag | Master에서 변경된 데이터가 Slave에 반영되기까지 걸리는 지연 시간 | 복사본이 아직 원본을 못 따라간 상태 |

## 깊이 이해
- **배경·문제의식**: 대부분의 웹 서비스는 읽기(Read)와 쓰기(Write) 비율이 8:2 또는 9:1로 읽기 요청이 압도적이다. 단일 DB로 쓰기와 수많은 읽기를 동시 처리하면 락(Lock) 경합과 자원 고갈이 발생한다.
- **작동 원리 (Master-Slave 기준)**:
  1. 클라이언트가 Master에 데이터를 INSERT하면, Master는 변경 사항을 자신의 Binlog에 기록한다.
  2. Slave의 I/O 쓰레드가 Master의 Binlog를 읽어와 자신의 Relay Log에 복사한다.
  3. Slave의 SQL 쓰레드가 Relay Log의 이벤트를 순차적으로 실행(Replay)하여 데이터를 똑같이 맞춘다.
- **복제 아키텍처 분류**:
  - **Master-Slave (Single Master)**: 쓰기는 1대, 읽기는 여러 대. 구조가 단순하고 정합성 유지가 쉽지만, 쓰기 확장은 불가능하다.
  - **Multi-Master**: 여러 대의 Master가 쓰기와 읽기를 모두 처리하고 서로 복제. 쓰기 확장이 가능하지만, 동시에 같은 데이터를 수정할 때 '충돌(Conflict)'이 발생하여 관리가 매우 까다롭다.
- **동기화 방식 (Sync vs Async)**:
  - **비동기(Asynchronous)**: Master가 Binlog만 쓰고 바로 클라이언트에 응답. 속도는 빠르나 Master 장애 시 데이터 유실 가능. (일반적 사용)
  - **반동기(Semi-synchronous)**: 최소 1대의 Slave가 로그를 받았다고 응답할 때까지 대기. 데이터 유실 방지와 속도의 타협점.
- **비유**: 은행 앱에서 송금을 완료(Master 쓰기)하고 바로 잔액을 확인했는데 이전 금액이 보이다가, 1초 뒤에 다시 새로고침하니 제대로 된 금액(Slave 반영 완료)이 보이는 현상이 Replication Lag 때문이다.
- **흔한 오해·주의점**: Multi-Master는 완벽해 보이지만, 양쪽 서버 네트워크가 단절된 상태(Split-Brain)에서 각자 쓰기를 받으면 나중에 데이터를 합칠 때 데이터 정합성이 박살 난다. 그래서 대부분 Master-Slave + 자동 페일오버(Auto Failover) 구조를 쓴다.

## 연결 개념
- 로드 밸런싱 (Load Balancing): 클라이언트의 Read 요청을 여러 대의 Slave로 분배해주는 기술 (예: ProxySQL, HAProxy)
- CQRS (Command Query Responsibility Segregation): 쓰기 모델(Command)과 읽기 모델(Query)을 애플리케이션 레벨에서 분리하는 패턴. 복제 아키텍처와 시너지를 낸다.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터베이스 복제는 변경 데이터를 여러 노드에 동기화하여 고가용성(HA)을 확보하고 읽기 부하를 분산(Scale-out)시키는 아키텍처다.
> 2. **가치**: 쓰기(Write)와 읽기(Read) 경로를 분리하여 단일 노드의 트랜잭션 경합을 완화하고, 메인 서버 장애 시 레플리카 승격을 통해 RTO를 획기적으로 단축한다.
> 3. **판단 포인트**: Master-Slave 구조의 Replication Lag(최신성 불일치)와 Multi-Master 구조의 충돌(Conflict) 해결 복잡도 사이에서 서비스 특성에 맞는 토폴로지와 동기화 수준(비동기/반동기)을 선택해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DB 고가용성 및 스케일아웃 전략 이해 | Master-Slave 분산을 통한 읽기 성능 향상 메커니즘 | 물리적 복제 구조만 쓰고 트랜잭션 분리(CQRS) 누락 |
| 복제 토폴로지 비교 역량 | Master-Slave와 Multi-Master의 충돌 제어 트레이드오프 | Multi-Master가 무조건 좋다는 단정 |
| 복제 지연 및 장애 극복 한계 인지 | Replication Lag 원인과 Asnyc/Semi-sync 동기화 수준 | 비동기 복제에서 데이터 유실이 없다고 착각 |

> 요약: 복제의 근본 목적이 부하 분산과 가용성 확보에 있음을 명시하고, Binlog 기반 동작 원리와 복제 지연(Lag)이라는 한계점 극복 방안을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 마스터 노드의 데이터 변경(트랜잭션) 내역을 로그 기반으로 다른 슬레이브 노드들에 동기화하여 동일한 상태를 유지하는 기법
- 배경: 웹 서비스 특성상 Read/Write 비율이 극단적(8:2 등)이어서, 단일 DB 인스턴스에 읽기 쿼리가 집중되면 I/O 병목 및 Lock 경합 유발
- 필요성: 단일 장애점(SPOF) 제거를 통한 고가용성 확보 및 슬레이브 노드를 통한 읽기 쿼리 수평 확장(Scale-out) 구현 필요

---

## Ⅱ. 구조 및 구성요소

```text
Client (Write) -> Master DB -> [Binlog] -> Network
                                              |
Client (Read)  <- Slave DB 1 <- [Relay Log] <-+ (I/O Thread가 수신)
Client (Read)  <- Slave DB 2 <- [Relay Log] <-+
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Master Node | 클라이언트의 쓰기(Insert/Update/Delete) 트랜잭션 처리 원본 | 변경 사항을 직렬화하여 Binlog에 기록 |
| Slave (Replica) Node | Master의 로그를 복제해 적용하고 클라이언트 읽기 쿼리 전담 | Master 장애 시 프로모션(승격) 대상 |
| Binlog / Relay Log | 데이터 변경 이벤트(DDL/DML)가 기록되는 바이너리 파일 | Statement(쿼리) 방식과 Row(데이터) 방식 존재 |

> 요약: 쓰기를 전담하는 Master에서 생성된 Binlog를 네트워크를 통해 Slave가 수신하여 로컬 Relay Log에 적재 후 재실행(Replay)하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Master Commit -> Binlog Write -> Slave I/O Thread 수신 -> Relay Log Write
-> Slave SQL Thread Replay -> Data Apply -> Slave Read 쿼리 제공
```

- 1단계 [트랜잭션 발생 및 기록]: Master에서 트랜잭션 커밋 시 변경 내역을 자체 디스크의 Binlog(Binary Log)에 기록
- 2단계 [로그 전송 및 수신]: Slave의 I/O 쓰레드가 Master에 접속하여 갱신된 Binlog 이벤트를 지속적으로 폴링/푸시 방식으로 수신
- 3단계 [Relay Log 적재]: 수신한 변경 이벤트를 Slave의 로컬 디스크인 Relay Log에 순차적으로 기록
- 4단계 [데이터 반영(Replay)]: Slave의 SQL 쓰레드가 Relay Log를 읽어 실제 스토리지 엔진에 변경 사항 적용 및 읽기 서비스 제공

> 요약: 복제는 동기적인 디스크 쓰기와 비동기적인 네트워크 전송, 그리고 쓰레드 분리를 통한 릴레이 반영으로 마스터의 부하를 최소화하며 진행된다.

---

## Ⅳ. 특징

- 읽기 수평 확장: 읽기(Read) 요청을 다수의 Slave로 로드밸런싱하여 시스템 전체의 초당 처리량(TPS/QPS)을 선형적으로 증대
- 고가용성 및 재해 복구: Master 장애 시 즉시 최신 Slave를 신규 Master로 승격(Failover)시켜 수 분(RTO) 내 서비스 정상화 보장
- 온라인 백업 유연성: Master에 락(Lock)을 걸지 않고, 특정 Slave 노드에서 스냅샷 백업 및 통계 배치를 수행하여 메인 서비스 간섭 배제

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 단방향 (Master-Slave) | 양방향 (Multi-Master) | 판단 기준 |
|:---|:---|:---|:---|
| 트랜잭션 흐름 | Master에서 Slave로 단방향 흐름 | 양쪽 노드에서 모두 Read/Write 허용 | 쓰기 트래픽의 수평 확장 필요성 |
| 정합성 관리 | 구조가 단순하여 충돌 우려 없음 | 동시 업데이트 시 충돌(Conflict) 해결 로직 필수 | 데이터 일관성 요구 수준 |
| 네트워크 단절 | Slave 지연만 발생, 서비스 정상 | Split-Brain 발생 시 양쪽 데이터 병합 난이도 극상 | 장애 시 복구 복잡도 트레이드오프 |

> 요약: 일반적인 대규모 웹 서비스는 안정성이 높은 Master-Slave를 채택하며, Multi-Master는 충돌 회피가 완벽히 설계된 특정 도메인에 제한 적용한다.

**리스크·대응:**
- Replication Lag 현상: 트래픽 폭증 시 Slave 반영 지연으로 최신 데이터 조회 실패 → 사용자 쓰기 직후 자신의 데이터는 강제로 Master에서 조회하는 라우팅 로직 적용
- 비동기 복제 중 Master 장애: 전송되지 않은 Binlog 유실 발생 → 정합성이 핵심인 금융 도메인은 Semi-synchronous(반동기) 복제 적용
- 다중 Slave 로드밸런싱 문제: 특정 Slave 쏠림 발생 → ProxySQL, HAProxy 등 DB L7 프록시를 활용한 헬스체크 및 Connection 분배

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. CQRS 기반 라우팅 분리: 애플리케이션 레벨(Spring의 `@Transactional(readOnly=true)` 등)에서 쿼리 유형을 판단해 Read는 Slave 그룹으로, Write는 Master로 분리 전송
2. HA 통합 클러스터링 구축: MHA(Master High Availability) 또는 오케스트레이터(Orchestrator) 툴을 연동하여, Master 노드 헬스체크 실패 시 VIP(Virtual IP) 스위칭을 통한 자동 페일오버 체계 확립
3. 지연(Lag) 모니터링: Prometheus를 활용해 `Seconds_Behind_Master` 메트릭이 1초를 초과할 경우 알람을 발생시키고, 임계치 초과 시 해당 Slave를 라우팅 풀에서 자동 제외

**결론 (2줄):**
- 기술사 판단: 복제 토폴로지는 단순한 데이터 백업이 아니라 C(Consistency)와 A(Availability) 간의 트레이드오프 설계이므로, 비동기의 지연 위험과 반동기의 성능 저하를 업무 중요도에 따라 믹스해야 한다.
- 향후 방향: 최근 클라우드 네이티브 환경에서는 스토리지 계층 자체를 공유해 복제 지연을 원천 제거하는 Aurora DB 방식이나 뗏목(Raft) 합의 알고리즘 기반 분산 DB 전환이 가속화되고 있다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DB 복제(Replication)를 설명하시오" | Binlog 기반 동기화 흐름도, 쓰레드 역할 | Master-Slave/Multi 비교, Sync/Async 차이 |
| 요구사항 명시형 | "고가용성 DB 클러스터링 설계 방안을 제시하시오" | Read/Write 트래픽 분리 아키텍처 도식 | 페일오버(Failover) 기준, Split-Brain 리스크 대응 |
