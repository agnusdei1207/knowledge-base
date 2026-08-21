---
sidebar:
  order: 113
  label: "113. 클라우드 데이터베이스 - RDS•Aurora•DynamoDB 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 데이터베이스 - RDS•Aurora•DynamoDB 비교"
date: "2026-08-17T23:50:00+09:00"
tags:
  - "notes-software"
weight: 113
extra:
  question_no: "113"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 관리형 데이터베이스 선택 현안"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클라우드 데이터베이스(Cloud Database)**: 클라우드 CSP가 인프라 프로비저닝, 패치, 백업, Failover를 완전관리형(Managed Service)으로 제공하는 데이터베이스 서비스.
- **RDS vs Aurora vs DynamoDB**: 인스턴스 기반 전통적 RDBMS(RDS), 컴퓨팅과 분산 스토리지를 분리한 고성능 클라우드 네이티브 RDBMS(Aurora), 무제한 수평 확장의 서버리스 NoSQL(DynamoDB).

</details>

- 정의/개념: 인프라 관리 부담을 줄이고 고가용성을 확보하기 위해 **RDS(인스턴스형), Aurora(스토리지 분리형), DynamoDB(서버리스 NoSQL)** 를 제공하는 완전관리형 데이터베이스 서비스
- 배경/필요성: 온프레미스 자체 DB 운영 시 발생하는 **하드웨어 조달 지연, 수동 백업 및 장애 복구 오버헤드와 트래픽 급증 시 확장 한계** 직면

#### 한줄 요약

- 워크로드 특성에 따라 RDS, Aurora, DynamoDB를 전략적으로 선택하여 운영 효율과 고가용성을 극대화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **컴퓨팅-스토리지 분리(Compute-Storage Decoupling)**: Aurora의 핵심 아키텍처로 컴퓨팅 노드와 6방향(6-Way) 복제 분산 스토리지를 분리하여 독립 확장 및 초고속 복구를 달성.
- **Multi-AZ 동기 복제**: 2개 이상의 가용 영역(AZ)에 대기 인스턴스를 유지하여 주 노드 장애 시 수십 초 이내 자동 장애 조치(Failover).

</details>

- OS 및 DBMS 패치, 자동 백업, 복구를 전담하는 **완전관리형(Fully-Managed) 서비스**
- Multi-AZ 동기 복제 및 분산 스토리지 쿼럼을 통한 **99.99% 이상의 고가용성(HA) 보장**
- 온디맨드 용량 할당 및 오토스케일링을 통한 **사용한 만큼만 지불하는 비용 최적화** #### 한줄 요약

- 완전관리형 운영, Multi-AZ 고가용성, 탄력적 오토스케일링을 통해 데이터 인프라의 복잡성을 제거

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Aurora 6-Way 스토리지 복제**: 3개 AZ에 걸쳐 데이터를 6개 복제본으로 분산 저장하고 4/6 Write Quorum으로 데이터 지속성을 보증하는 아키텍처.

</details>

```text
[ 클라우드 데이터베이스 3대 아키텍처 모델 비교 ]

 1. [ Amazon RDS (인스턴스형) ]
    Primary EC2 Instance ──(동기식 EBS 복제)──► Standby EC2 Instance (AZ2)

 2. [ Amazon Aurora (컴퓨팅-스토리지 분리형) ]
    [ Primary Writer ] ──► [ Read Replicas (최대 15개) ]
            │                         │
            ▼                         ▼
    [ 6-Way 분산 스토리지 계층 (3개 AZ에 6개 복제본 쿼럼 유지) ]

 3. [ Amazon DynamoDB (서버리스 NoSQL) ]
    [ 분산 Request Router ] ──► [ Partition SSD 노드 (Auto-Scaling) ]
```

선의 의미: 인스턴스 기반 Multi-AZ(RDS), 분산 스토리지 분리(Aurora), 서버리스 파티셔닝(DynamoDB)의 3대 구조.

| 구성요소 | 책임 |
|:---|:---|
| Amazon RDS | MySQL, PostgreSQL 등 표준 엔진을 **EC2 및 EBS 기반 인스턴스로 관리형 제공** |
| Amazon Aurora | 컴퓨팅과 스토리지를 분리하여 **기존 RDBMS 대비 5배 처리량 및 15개 읽기 복제본 제공** |
| Amazon DynamoDB | 서버리스 아키텍처 기반으로 **초당 수백만 TPS의 단건 키-값 조회를 10ms 이내 처리** |
| 자동 장애전환 (Failover) | 주 노드 장애 시 DNS 엔드포인트를 **대기 복제본으로 자동 전환하여 무중단 서비스** |

#### 한줄 요약

- RDS(표준 RDBMS), Aurora(초고성능 분산 RDBMS), DynamoDB(서버리스 NoSQL)로 역할을 분담

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **클라우드 DB 자동 장애 복구 파이프라인**: 상태 감시 $\to$ 장애 판정 $\to$ 대기 복제본 승격 $\to$ DNS 엔드포인트 갱신 $\to$ 트래픽 재개.

</details>

```text
[ 클라우드 DB Multi-AZ 자동 Failover 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 주(Primary) DB 인스턴스 장애 발생   │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 클라우드 제어면 상태 검사(Heartbeat) 실패
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Standby / Read Replica를 Primary로 승격│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. DB CNAME DNS 엔드포인트 자동 갱신   │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 앱 재접속 및 무중단 트랜잭션 재개  │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 장애 발생: 주 DB 인스턴스의 하드웨어 고장 또는 네트워크 단절 발생.
2. 상태 검사 실패: 클라우드 관리 제어면이 하트비트 누락을 감지하고 장애를 선언.
3. 승격: Multi-AZ 대기 인스턴스 또는 가장 지연이 적은 Aurora Read Replica를 새로운 Writer로 승격.
4. 엔드포인트 갱신: 클라이언트가 바라보는 DB CNAME DNS 주소를 신규 Writer IP로 자동 변경.
5. 연결 복구: 클라이언트 커넥션 풀이 자동 재연결되어 수십 초 이내에 정상 서비스를 재개.

#### 한줄 요약

- 장애 감지 $\to$ 제어면 판정 $\to$ 복제본 승격 $\to$ DNS 갱신 $\to$ 서비스 재개의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RDS vs Aurora vs DynamoDB**: 워크로드, 성능, 트랜잭션, 비용 특성에 따른 클라우드 DB 비교.

</details>

| 구분 | Amazon RDS (표준 인스턴스) | Amazon Aurora (클라우드 네이티브) | Amazon DynamoDB (서버리스 NoSQL) |
|:---|:---|:---|:---|
| **적용 기준** | 온프레미스 레거시 DB의 단순 클라우드 이관 | 대규모 엔터프라이즈 OLTP 웹 서비스 | 서버리스 웹앱, 게임 세션, 장바구니 |
| **핵심 특징** | **표준 엔진 100% 호환, Multi-AZ 동기 복제** | **Compute/Storage 분리, 5배 고성능, 6-Way 복제** | **완전 관리형 서버리스, 무제한 수평 확장** |
| **한계** | 읽기 복제본 복제 지연 및 수직 확장 한계 | 높은 I/O 비용 및 AWS 플랫폼 종속성 | 복잡한 다중 테이블 조인 및 집계 불가 |

#### 한줄 요약

- 단순 이관은 RDS, 고성능 대규모 트랜잭션은 Aurora, 무제한 수평 확장은 DynamoDB를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **I/O 비용 최적화(I/O-Optimized)**: Aurora 사용 시 잦은 쿼리로 I/O 과금이 폭증하는 문제를 해결하기 위해 I/O 비용이 무료로 포함된 정액 요금제를 채택하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Aurora 사용 시 소량 쿼리 빈발로 I/O 비용 폭증 (비용 대량 부하) | **Aurora I/O-Optimized 요금제로 변경 및 캐시 계층(Redis) 도입** | 예측 가능한 고정 비용 및 I/O 절감 |
| DynamoDB Table Scan 쿼리로 인한 RCU 폭증 및 과금 | **Global Secondary Index(GSI) 설계 및 Scan 대신 Query 강제** | 쿼리 비용 및 응답 시간 90% 절감 |
| 특정 클라우드 DB 독점 API 사용에 따른 Vendor Lock-in | **Spring Data 추상화 계층 및 표준 인터페이스 래퍼 구축** | 멀티 클라우드 이식성 확보 |

#### 한줄 요약

- I/O 최적화 요금제, GSI 인덱스 설계, 표준 추상화 계층 구축으로 비용과 종속성 문제를 해결

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **클라우드 폴리글랏 아키텍처(Cloud Polyglot Architecture)**: 트랜잭션 원장은 Aurora로, 초고속 세션 및 캐시는 DynamoDB/ElastiCache로 분리하는 현대적 클라우드 아키텍처.

</details>

- **클라우드 데이터베이스** 기반 인프라 관리 비용을 혁신적으로 절감하는 현대 소프트웨어의 필수 구성요소이며, 비즈니스 특성에 맞추어 RDS, Aurora, DynamoDB를 유기적으로 조합하는 폴리글랏 설계를 구현해야 함

#### 한줄 요약

- 워크로드에 부합하는 클라우드 DB를 선별 적용하고 폴리글랏 아키텍처로 확장성과 가용성을 완성
