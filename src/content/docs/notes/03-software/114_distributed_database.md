---
sidebar:
  order: 114
  label: "114. 분산 데이터베이스"
  badge:
    text: "미출 · 50%"
    variant: note
title: "분산 데이터베이스 (Distributed Database)"
date: "2026-08-26T13:08:13+09:00"
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

- **분산 데이터베이스(Distributed Database)**: 물리적으로 분산된 여러 노드에 데이터를 분할/복제 저장하면서도 논리적으로는 하나의 DB처럼 작동하는 시스템.
- **6대 분산 투명성**: 위치, 분할, 복제, 병행, 장애, 자원 투명성(Location, Fragmentation, Replication, Concurrency, Failure, Resource).

</details>

- 정의/개념: 물리적으로 분산된 다수의 독립 노드에 데이터를 분할·복제 저장하되 **6대 분산 투명성을 통해 단일 논리 DB처럼 투명하게 제공**하는 시스템
- 배경/필요성: 단일 노드 데이터베이스의 **물리적 자원 한계, 단일 장애점(SPOF) 위험 및 글로벌 지역 간 통신 지연 해결 불가**

#### 한줄 요약
- Shared-Nothing과 분산 투명성으로 수평 확장과 장애 격리를 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Shared-Nothing**: 각 노드가 CPU, 메모리, 디스크를 독립적으로 보유하고 네트워크 메시지 교환으로만 협력하는 구조.
- **Two-Phase Commit (2PC)**: 분산 노드 간 원자적 커밋을 위해 Prepare와 Commit 2단계로 진행되는 합의 프로토콜.

</details>

- 노드 간 자원을 공유하지 않고 독립 확장하는 **Shared-Nothing 수평 확장(Scale-Out)**
- 물리적 분산 배치를 응용에 은닉하는 **분산 투명성** 지원
- 원자적 커밋은 **2PC**, 복제 상태 합의는 **Raft** 적용

#### 한줄 요약
- 수평 확장, 6대 투명성, 분산 트랜잭션 합의를 통해 신뢰성 있는 분산 처리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **GDD(Global Data Dictionary)**: 전체 분산 클러스터의 샤딩 룰, 복제본 위치, 데이터 매핑 메타데이터를 통합 관리하는 전역 카탈로그.

</details>

```text
[분산 데이터베이스 통합 계층 아키텍처]
|-- 클라이언트 애플리케이션 (단일 DB로 인식하고 표준 SQL 질의)
`-- 분산 데이터베이스 관리 시스템 (DDBMS)
    |-- 전역 데이터 딕셔너리 (GDD: 위치, 샤드 매핑, 복제본 카탈로그)
    |-- 분산 질의 최적화기 (Global Query Optimizer: 분산 플랜 수립 및 셔플링)
    |-- 트랜잭션 코디네이터 (Transaction Coordinator: 2PC / Raft 분산 커밋)
    `-- 로컬 DBMS 노드들 (Local Node 1, 2, 3: 독자 스토리지 및 트랜잭션 엔진)
```

선의 의미: 계층 및 DDBMS가 전역 메타데이터와 분산 조율을 통해 로컬 노드들을 통제하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 전역 카탈로그 | 샤드·복제본·노드 상태 메타데이터 관리 |
| 분산 질의 조정자 | 하위 질의 분할과 **중간 결과 병합** |
| 트랜잭션 조정자 | **2PC** 기반 전역 Commit·Abort 통제 |
| 로컬 DBMS 노드 | 파티션 저장과 로컬 ACID 실행 |

#### 한줄 요약
- 전역 카탈로그, 분산 질의 조정자, 트랜잭션 코디네이터, 로컬 DB 노드가 유기적으로 협력한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **2PC(Two-Phase Commit) 파이프라인**: Coordinator가 모든 Participant에 Prepare를 요청하고 전원 Yes 응답 시 Commit을 전파하는 프로토콜.

</details>

```text
클라이언트가 분산 트랜잭션 커밋 요청
        │
   [참여 노드 식별] 트랜잭션 코디네이터(Coordinator)가 대상 샤드 노드들 식별
        │
   [Phase 1: Prepare] 코디네이터가 모든 참여 노드에 Prepare 요청 전송
        │
   모든 노드가 'Yes(준비 완료)' 응답을 보냈는가?
   ┌────┴───────────────────────────┐
  예 (전원 성공)                    아니오 (1개 노드라도 실패/타임아웃)
   │                                 │
[Phase 2: Global Commit]         [Phase 2: Global Abort]
코디네이터가 Commit 로그 작성 후   코디네이터가 Abort 전파 후
모든 노드에 커밋 전파 및 완료     모든 노드가 롤백 수행
```

#### 한줄 요약
- 노드 식별 → Prepare 요청 → 투표 결과 취합 → Global Commit/Abort 확정 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **동종(Homogeneous) vs 이종(Heterogeneous)**: 동일 DBMS 엔진으로 구성된 동종 분산 DB와 서로 다른 DBMS 엔진을 미들웨어로 연계한 이종 분산 DB.

</details>

| 비교 항목 | 동종 분산 DB (Homogeneous) | 이종 분산 DB (Heterogeneous) |
|:---|:---|:---|
| 노드 DBMS 엔진 | **동일한 DBMS 제품으로 구성 (예: PG-PG)** | **서로 다른 DBMS 제품 혼용 (예: Oracle-MySQL)**|
| 트랜잭션 통제 | DBMS 내장 분산 프로토콜 활용 | XA 미들웨어나 게이트웨이 연계 |
| 데이터 모델 매핑 | 단일 데이터 모델 및 표준 SQL 통용 | SQL 문법 및 데이터 타입 변환 매핑 오버헤드 큼 |
| 최적 적용 분야 | **신규 대규모 분산 시스템 구축, NewSQL** | **기업 간 시스템 통합(EAI), 레거시 DB 통합** |

#### 한줄 요약
- 신규 확장은 동종 분산 DB, 이종 시스템 간 데이터 통합은 이종 분산 DB를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Split-Brain**: 네트워크 분할 시 고립된 서브 클러스터들이 서로 자신을 Master로 선언하여 데이터 오염을 유발하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네트워크 단절의 **Split-Brain** 위험 | **과반수 Quorum·Fencing** 적용 | 동시 쓰기 리더 위험 제한 |
| 2PC 조정자 장애의 참여 노드 블로킹 | 조정자 로그 복제와 **복구 프로토콜** 적용 | 미결 트랜잭션 복구 지원 |
| 분산 노드 간 자원 교차 선점으로 인한 **분산 데드락** | **글로벌 데드락 감지기(Wait-For Graph) 및 Lock Timeout Abort** | 교착 상태 조기 발견 및 해제 |
| 노드 간 데이터 불일치와 통신 지연 | 워크로드별 **복제 계수·Read Repair** 설정 | 정합성과 읽기 비용 절충 |

#### 한줄 요약
- Quorum 과반수 합의, Raft 합의 엔진, 분산 데드락 감지기, Read Repair로 운영한다.

## Ⅶ. 결론

- 원자적 분산 커밋은 **2PC**, 복제 리더 합의는 **Raft** 선택

#### 한줄 요약
- 샤드·복제·커밋 비용을 일관성 요구에 맞춰 설계한다.
