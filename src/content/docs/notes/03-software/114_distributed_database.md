---
sidebar:
  order: 114
  label: "114. 분산 데이터베이스 (Distributed Database)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "분산 데이터베이스 (Distributed Database)"
date: "2026-08-13T21:56:00+09:00"
tags:
  - "notes-software"
weight: 114
extra:
  question_no: "114"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "분산 저장•복제•질의 설계의 상위 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Distributed Database (분산 데이터베이스)**: 물리적으로 서로 떨어진 다수의 데이터베이스 노드(Physical Node)에 데이터를 분할(Sharding) 및 복제(Replication) 저장하되, 애플리케이션에는 네트워크 투명성(Transparencies)을 통해 단일 DB처럼 보여주는 데이터 시스템.
- **Distributed Transparencies (분산 투명성 6대 요소)**: 위치, 분할, 복제, 병행, 장애, 자원 투명성을 통해 사용자가 물리적 노드 위치나 샤딩 여부를 알 필요 없이 단일 DB로 인식하게 해주는 특성.
- **Shared-Nothing Architecture**: 노드 간 디스크나 메모리를 공유하지 않고, 독립된 노드들이 네트워크(Message Passing)로만 통신하는 분산 아키텍처의 표준.

</details>

- 정의/개념: 분할•복제 데이터를 하나처럼 제공하는 **분산 데이터베이스**
- 배경/필요성: 단일 노드는 **용량•처리량•장애 영향•지역 지연** 한계

#### 한줄 요약

- 장부를 지점에 나누고 사본과 합의 규칙으로 하나처럼 쓰는 데이터베이스이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **High Availability & Fault Tolerance**: 1개 노드 다운 시에도 타 노드로 서비스 자동 연속.
- **Scalability (Horizontal Scale-Out)**: 노드 추가를 통해 디스크 용량 및 TPS 무제한 증설.

</details>

- **Shared-Nothing**: 독립 자원을 가진 노드의 수평 확장
- **6대 분산 투명성 (Location, Partition, Replication, Concurrency, Failure, Resource)**
- **Two-Phase Commit (2PC) / Consensus (Raft/Paxos)** 기반 분산 일관성 보장

#### 한줄 요약

- 수평 확장과 장애 대응은 좋아지지만 네트워크와 사본 비용이 추가된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Location & Replication Transparency**: 데이터가 어느 물리 노드에 있는지, 몇 개의 복제본이 존재하는지 사용자가 알 필요 없이 단순 SQL로 접근 가능함.

</details>

```text
[전역 카탈로그] ─── [분산 질의 조정자]
        │                    │
[트랜잭션 조정자] ── [복제•합의 계층]
        │                    │
        └──── [로컬 DB 노드] ┘
```

선의 의미: 위치 정보•질의•트랜잭션•복제•저장의 정적 협력 관계.

| 구성요소 | 책임 |
|:---|:---|
| **전역 카탈로그** | 분할•복제•위치 메타데이터 관리 |
| **분산 질의 조정자** | 하위 질의 분배와 결과 취합 |
| **트랜잭션 조정자** | 참여 노드의 커밋•중단 결정 |
| **복제•합의 계층** | 사본 순서•정족수•장애전환 관리 |
| **로컬 DB 노드** | 담당 파티션 저장과 로컬 연산 수행 |

#### 한줄 요약

- 위치표, 안내자, 사본 규칙, 거래 조정자, 이동 담당자로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Two-Phase Commit (2PC)**: 분산 DB 트랜잭션 시 Coordinator가 Prepare Phase와 Commit Phase 2단계를 통해 참여 노드(Cohort) 전체의 동시 커밋을 완전 원자 보장하는 프로토콜.

</details>

```text
[분산 트랜잭션]
       │
       ▼
1. 참여 노드 식별
       │
       ▼
2. Prepare 요청
       │
       ▼
3. 투표 결과 수집
       │
       ▼
4. 전역 결정 기록
       │
       ▼
5. 결정 전파
       │
       ▼
  [결과 반환]
```

### 동작 원리

1. **참여 노드 식별**: 변경 대상 파티션과 담당 노드 결정
2. **Prepare 요청**: 각 노드가 변경 준비와 로그 기록 수행
3. **투표 결과 수집**: 모든 준비 성공 여부 확인
4. **전역 결정 기록**: 조건에 따라 Commit•Abort 확정
5. **결정 전파**: 참여 노드가 결정 적용 후 잠금 해제

#### 한줄 요약

- 안내소가 담당 지점을 찾고 사본 확인까지 마친 결과를 하나의 장부처럼 돌려준다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Homogeneous vs Heterogeneous**: 동종 분산 DB는 동일한 DBMS 엔진(예: MySQL-MySQL)으로 구성, 이종 분산 DB는 서로 다른 DBMS(Oracle-MySQL)를 GDD로 묶은 구조.

</details>

| 비교 항목 | Homogeneous (동종 분산 DB) | Heterogeneous (이종 분산 DB) |
|:---|:---|:---|
| **DBMS 엔진 동일성**| **동일한 DBMS 제품으로 노드 구성 (Oracle-Oracle)**| **서로 다른 DBMS 엔진 혼용 (Oracle-MySQL)** |
| **트랜잭션 통제** | DBMS 자체 프로토콜로 쉽게 2PC 및 Replication 가능 | **중간 게이트웨이 및 미들웨어 (ODBC/JDBC) 필수** |
| **구현 난이도** | 상용 DB 지원으로 표준적 | **극도로 높음 (데이터 타입/SQL 변환 맵핑 필요)** |

#### 한줄 요약

- 데이터베이스 배치 선택 기준에서 한 지점은 단순하고 여러 지점은 넓게 확장되지만 연락과 합의가 필요하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Split-Brain Problem**: 네트워크 단절 시 분산 노드가 둘로 쪼개져 서로 자신이 Master라고 주장하며 데이터 오염을 발생시키는 사태 (Quorum 과반수 투표로 해결).

</details>

| 3대 분산 장애 | 발생 원인 및 위험 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Split-Brain 사태** | 네트워크 파티션 단절 시 2개의 Master 출현 | **Quorum (과반수 투표: $N/2 + 1$) 홀수 노드 구성** |
| **2. 2PC Blocking 병목**| Coordinator 다운 시 Cohort 락 무한 대기 | **3PC (Three-Phase Commit) 또는 Raft Consensus 적용** |
| **3. Distributed Deadlock**| 서로 다른 노드 자원을 교차 락 선점 시 교착 | **Global Deadlock Detector & Timeout Abort 적용** |

> 사례: **Google Spanner / TiDB 기반 글로벌 분산 RDBMS (NewSQL) 운용**

#### 한줄 요약

- 자료가 고르게 나뉘는지뿐 아니라 지점 이동 시간과 추가 공간도 재야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **분산 DB 수립 기준(Distributed Database Standards)**: 6대 분산 투명성, Quorum Raft 합의 알고리즘 및 Multi-Region Scale-Out에 의거한 체계.

</details>

- 지역 지연•확장이 이득이고 조정 비용을 감당하면 **분산 DB** 선택

#### 한줄 요약

- 선택 기준은 수평 확장과 연락•합의•이동 비용을 함께 비교한다.
