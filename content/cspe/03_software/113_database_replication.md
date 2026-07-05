---
title: "데이터베이스 복제 (Replication)와 Read Replica"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 113
---

## 핵심 인사이트 (3줄 요약)
- 원본 데이터베이스(Master)의 모든 변경 사항을 다른 데이터베이스(Slave/Replica)로 실시간으로 복사(동기화)하여, 똑같은 DB 여러 대를 유지하는 고가용성 아키텍처 기법.
- 일반적인 웹 서비스는 읽기(SELECT)와 쓰기(INSERT/UPDATE)의 비율이 8:2로 읽기가 압도적으로 많음. 이를 해결하기 위해 **쓰기 트래픽은 Master가 전담하고, 읽기 트래픽은 여러 대의 Slave로 분산시키는(Read/Write Splitting) 스케일아웃 기법**으로 쓰임.
- 복제 지연(Replication Lag)이라는 치명적 문제가 발생할 수 있으며, 방금 내가 쓴 글을 내가 다시 조회했을 때 글이 안 보이는 '최종 일관성(Eventual Consistency)'의 함정을 방어하는 것이 핵심임.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **필요성** | 단일 DB(SPOF)가 터지면 서비스 전체가 죽어버리는 위험을 막기 위한 백업(가용성) 용도 | "핵심 기술 요소" |
| **Master (쓰기 전용)** | 클라이언트의 INSERT/UPDATE 요청을 받아 실제 데이터를 수정하고, 그 변경 이력을 **바이너리 로그(Binary Log, Binl... | "일지 기록" |
| **Relay & I/O Thread** | Slave DB의 I/O 쓰레드가 Master의 Binlog를 주기적으로 훔쳐와서(Pull), 자신의 릴레이 로그(Relay Log)에 복사함 | "한 사무실의 여러 직원" |
| **Slave (읽기 전용)** | Slave의 SQL 쓰레드가 릴레이 로그를 읽고, 그대로 자신의 디스크에 재실행(Replay)하여 Master와 똑같은 상태를 만듦 | "데이터 질의 언어" |
| **동기화(Sync) vs 비동기화(Async) 방식** | - **비동기(Asynchronous)**: Master는 Binlog만 던져놓고 즉시 클라이언트에게 "성공!"을 응답함 | "일지 기록" |
| **반동기(Semi-Sync)** | 최소 1대의 Slave가 "로그 잘 받았다"고 응답할 때까지 Master가 대기함 | "서비스 약속" |
| **복제 지연 (Replication Lag) 대처법** | 비동기 복제 환경에서는 Master에 글을 쓰고 0 | "핵심 기술 요소" |

---


## Ⅰ. 개요 및 필요성
- **개요**: 하나의 DB 서버(Primary/Master)에 저장된 데이터를 다른 1개 이상의 DB 서버(Secondary/Slave/Replica)에 실시간으로 복사하여 동일한 데이터를 유지하는 기술.
- **필요성**: 단일 DB(SPOF)가 터지면 서비스 전체가 죽어버리는 위험을 막기 위한 백업(가용성) 용도. 또한 수십만 명이 동시에 게시글을 조회(SELECT)할 때 DB CPU가 100%를 치는 것을 막기 위해, 똑같은 데이터를 가진 '조회 전용 깡통 DB'들을 늘려서 부하를 쪼갤 필요가 있었음.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **MySQL 레플리케이션 동작 원리 (Binlog 기반)**:
  1. **Master (쓰기 전용)**: 클라이언트의 INSERT/UPDATE 요청을 받아 실제 데이터를 수정하고, 그 변경 이력을 **바이너리 로그(Binary Log, Binlog)** 파일에 기록함.
  2. **Relay & I/O Thread**: Slave DB의 I/O 쓰레드가 Master의 Binlog를 주기적으로 훔쳐와서(Pull), 자신의 릴레이 로그(Relay Log)에 복사함.
  3. **Slave (읽기 전용)**: Slave의 SQL 쓰레드가 릴레이 로그를 읽고, 그대로 자신의 디스크에 재실행(Replay)하여 Master와 똑같은 상태를 만듦.
- **동기화(Sync) vs 비동기화(Async) 방식**:
  - **비동기(Asynchronous)**: Master는 Binlog만 던져놓고 즉시 클라이언트에게 "성공!"을 응답함. 매우 빠르지만, 찰나의 순간 Master가 죽으면 데이터가 영원히 유실될 수 있음 (실무 기본값).
  - **반동기(Semi-Sync)**: 최소 1대의 Slave가 "로그 잘 받았다"고 응답할 때까지 Master가 대기함. 안정성은 높으나 쓰기 속도가 떨어짐.

```text
[ Read / Write Splitting (읽기/쓰기 분리) 아키텍처 ]

 (웹/앱 서버 클라이언트) 
   | 
   |-- (쓰기 요청: INSERT) ➡️ [ Master DB ] ➡️ (Binlog 전송) 
   |                                              ⬇️ (복제)
   |-- (읽기 요청: SELECT) ➡️ [ L4 로드밸런서 ] ➡️ [ Slave 1 ]
   |-- (읽기 요청: SELECT) ➡️                ➡️ [ Slave 2 ] 
   
 * 결과: 무거운 통계 쿼리나 조회 쿼리를 Slave가 다 받아내어 Master는 쾌적해짐!
```
---
## Ⅲ. 비교 및 연결
| 구분 | 샤딩 (Sharding) | 레플리케이션 (Replication) | 클러스터링 (Clustering - Oracle RAC) |
|---|---|---|---|
| **데이터 분할** | 데이터를 N개로 찢어서 나눔 (A~M, N~Z) | **모든 서버가 100% 똑같은 전체 데이터** 보유 | 스토리지 1개를 여러 DB 엔진이 공유 |
| **목적** | 쓰기/읽기 용량 전체의 무한 확장 (Scale-Out) | **조회(SELECT) 성능 향상 및 장애 복구** | 무중단 장애 복구 (Active-Active) |
| **동기화 이슈**| 노드 간 조인 불가, 트랜잭션 꼬임 | **복제 지연(Lag) 발생** | 스토리지 Lock 경합 심화 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **복제 지연 (Replication Lag) 대처법**: 비동기 복제 환경에서는 Master에 글을 쓰고 0.5초 뒤 Slave에 복제됨. 사용자가 글 작성 후 즉시 '내 글 보기'를 눌렀는데, 0.5초 안에 로드밸런서가 Slave로 쿼리를 보내면 "게시글이 없습니다"라는 치명적 버그가 터짐. 
  - **아키텍트의 해결책**: "내가 쓴 데이터는 잠시 동안 강제로 Master에서 읽게 한다(세션 라우팅)", 또는 "쓰기 직후 캐시(Redis)에 넣어두고 캐시를 먼저 읽게 한다" 등의 애플리케이션 레벨의 우회 설계(Workaround)가 반드시 수반되어야 함.
- **Fail-Over (장애 복구) 자동화**: Master가 죽었을 때 사람이 수동으로 Slave 중 하나를 승격시키면 새벽에 장애 시간이 너무 길어짐. 실무에서는 MHA(Master High Availability)나 Orchestrator 같은 도구를 통해 죽은 Master를 버리고 Slave 중 가장 최신 데이터를 가진 놈을 VIP(Virtual IP)로 바꿔치기하는 '자동 페일오버'를 구축해야 함. (최근 클라우드 AWS Aurora는 이를 100% 자동화함).
---
## Ⅴ. 기대효과 및 결론
- RDBMS 시스템에서 '가용성(Availability)' 확보와 '읽기 부하 분산(Read Scalability)'이라는 두 마리 토끼를 잡는 표준적이고 가장 검증된 인프라 아키텍처임.
- 복제를 설정하는 순간 필연적으로 발생하는 데이터의 '시간차(Lag)' 문제는 시스템을 완벽한 ACID에서 느슨한 최종 일관성(Eventual Consistency) 모델로 넘어가게 만드는 기술적 전환점이 됨.
---
### 📌 관련 개념 맵
- DB 고가용성 ➡️ Master-Slave 복제 ➡️ Binlog / Relay Log ➡️ Read/Write Splitting ➡️ 복제 지연(Lag)

### 📈 관련 키워드 및 발전 흐름도
- 단일 DB 장애 ➡️ Active-Standby 클러스터 구성 ➡️ Master-Slave 레플리케이션(Read Replica) ➡️ AWS Aurora(스토리지 분리형 복제)

### 👶 어린이를 위한 3줄 비유 설명
1. 유명한 작가(Master)가 책을 쓰면, 옆에 있는 복사기 3대(Slave)가 1초 만에 징징징~ 똑같은 책을 복사해 내요.
2. 서점에 10만 명의 팬이 몰려오면, 작가는 조용히 글(쓰기)만 쓰고, 팬들은 복사기가 만들어낸 3권의 책(읽기)을 나눠서 읽으면 되니까 아무도 안 싸워요!
3. 그런데 가끔 복사기가 렉이 걸려서(복제 지연), 작가가 방금 쓴 마지막 페이지가 아직 복사 안 됐을 때 팬들이 보면 "어? 결말이 없네?" 하고 당황할 수 있답니다.
