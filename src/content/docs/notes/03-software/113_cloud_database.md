---
sidebar:
  order: 113
  label: "113. 클라우드 데이터베이스 - RDS•Aurora•DynamoDB"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 데이터베이스 - RDS•Aurora•DynamoDB 비교"
date: "2026-08-26T09:52:00+09:00"
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

- **클라우드 데이터베이스**: CSP가 프로비저닝, 패치, 백업, Failover를 완전관리형(Fully-Managed)으로 제공하는 데이터베이스.
- **RDS vs Aurora vs DynamoDB**: 인스턴스형 전통 RDBMS(RDS), 컴퓨팅/스토리지 분리형 클라우드 네이티브 RDBMS(Aurora), 서버리스 분산 NoSQL(DynamoDB).

</details>

- 정의/개념: 인프라 관리 오버헤드를 제거하고 고가용성을 확보하기 위해 **RDS(인스턴스형), Aurora(스토리지 분리형), DynamoDB(서버리스 NoSQL)** 를 제공하는 완전관리형 데이터베이스 서비스
- 배경/필요성: 온프레미스 자체 DB 운영 시 발생하는 **하드웨어 조달 지연, 수동 백업 및 장애 복구 오버헤드와 트래픽 급증 시 확장 한계 해결 불가**

#### 한줄 요약
- 워크로드 특성에 따라 RDS, Aurora, DynamoDB를 선택하여 운영 효율과 고가용성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Compute-Storage Decoupling**: Aurora에서 컴퓨팅 인스턴스와 분산 스토리지 계층을 분리하여 독립 확장 및 초고속 크래시 복구를 실현한 구조.
- **Multi-AZ Replication**: 여러 가용 영역(AZ)에 복제본을 배치하여 주 노드 장애 시 30초 이내 자동 무중단 장애 조치(Failover)를 보장.

</details>

- OS 및 DBMS 패치, 자동 백업, 복구를 전담하는 **완전관리형(Fully-Managed) 서비스**
- Multi-AZ 동기 복제 및 분산 스토리지 쿼럼을 통한 **99.99% 이상의 고가용성(HA) 보장**
- 온디맨드 용량 할당 및 오토스케일링을 통한 **사용한 만큼만 지불하는 비용 최적화**

#### 한줄 요약
- 완전관리형 운영, Multi-AZ 고가용성, 탄력적 오토스케일링으로 인프라 복잡성을 제거한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Aurora 6-Way 분산 복제**: 3개 AZ에 걸쳐 데이터를 6개 복제본으로 분산 저장하고 4/6 Write Quorum으로 데이터 영속성을 보장.

</details>

```text
[클라우드 데이터베이스 3대 아키텍처 모델]
|-- 1. Amazon RDS (전통적 단일 인스턴스형)
|   `-- Primary EC2 ──(동기식 EBS 블록 복제)──► Standby EC2 (Multi-AZ)
|-- 2. Amazon Aurora (컴퓨팅-스토리지 분리형 클라우드 네이티브 RDBMS)
|   |-- Primary Writer ◄──► Read Replicas (최대 15개, 지연시간 < 10ms)
|   `-- 6-Way 분산 스토리지 계층 (3개 AZ에 6벌 복제, 4/6 쓰기 쿼럼)
`-- 3. Amazon DynamoDB (완전관리형 서버리스 NoSQL)
    `-- Request Router ──► Auto-Partitioning SSD 노드 (Key-Value/Document)
```

선의 의미: 계층 및 인스턴스형(RDS), 스토리지 분리형(Aurora), 서버리스 분산형(DynamoDB) 아키텍처 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| Amazon RDS | MySQL, PostgreSQL 등 표준 엔진을 **EC2 및 EBS 기반 인스턴스로 관리형 제공** | 표준 RDBMS 100% 호환 |
| Amazon Aurora | 컴퓨팅과 스토리지를 분리하여 **기존 RDBMS 대비 5배 처리량 및 15개 읽기 복제본 제공**| 6-Way 스토리지 쿼럼 복제 |
| Amazon DynamoDB | 서버리스 아키텍처 기반으로 **초당 수백만 TPS의 단건 키-값 조회를 10ms 이내 처리** | 무제한 수평 자동 확장 |
| 자동 장애전환 (Failover) | 주 노드 장애 시 DNS 엔드포인트를 **대기 복제본으로 자동 전환하여 무중단 복구** | RTO 30초 미만 전환 |

#### 한줄 요약
- RDS(표준 RDB), Aurora(초고성능 분산 RDB), DynamoDB(서버리스 NoSQL)로 역할을 분담한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Multi-AZ Failover 절차**: Primary 장애 $\to$ 하트비트 타임아웃 $\to$ Replica를 Primary로 승격 $\to$ CNAME DNS 갱신 $\to$ 서비스 재개.

</details>

```text
주(Primary) DB 인스턴스에 하드웨어 크래시 발생
        │
   [장애 감지] 클라우드 제어면(Control Plane)이 2초 주기 하트비트 실패 감지
        │
   [승격 절차] Multi-AZ Standby 또는 최저 지연 Aurora Read Replica를 새 Writer로 승격
        │
   [DNS 엔드포인트 갱신] DB CNAME 레코드가 가리키는 IP를 신규 Writer로 자동 수정
        │
   클라이언트 커넥션 풀이 신규 Writer로 자동 재연결되어 무중단 트랜잭션 정상 재개
```

#### 한줄 요약
- 장애 감지 → 제어면 판정 → 복제본 승격 → DNS 갱신 → 서비스 재개 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RDS vs Aurora vs DynamoDB**: 표준 호환성(RDS), 고성능 트랜잭션(Aurora), 대규모 수평 확장(DynamoDB).

</details>

| 비교 항목 | Amazon RDS (표준 인스턴스) | Amazon Aurora (클라우드 네이티브) | Amazon DynamoDB (서버리스 NoSQL) |
|:---|:---|:---|:---|
| 아키텍처 모델 | **단일 인스턴스 + EBS 스토리지** | **컴퓨팅-스토리지 분리형 클러스터** | **완전관리형 서버리스 분산 NoSQL** |
| 최대 읽기 복제본 | 최대 5개 (비동기 복제 지연 존재) | **최대 15개 (서브 10ms 초저지연 복제)** | 해당 없음 (노드별 자동 분산) |
| 성능 및 처리량 | 표준 오픈소스 DB 수준 | **MySQL 대비 5배, PG 대비 3배 성능** | **초당 수백만 TPS 수평 무제한 처리** |
| 최적 적용 분야 | **온프레미스 레거시 DB 단순 클라우드 이전**| **대규모 엔터프라이즈 전자상거래 OLTP** | **초고속 세션, 게임 랭킹, 장바구니** |

#### 한줄 요약
- 단순 이전은 RDS, 고성능 대규모 트랜잭션은 Aurora, 무제한 수평 확장은 DynamoDB를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Aurora I/O-Optimized**: 쿼리당 I/O 과금 대신 고정된 정액 요율을 적용하여 대용량 트래픽에서의 비용 폭증을 방어하는 옵션.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Aurora 사용 시 소량 쿼리 빈발로 I/O 비용 폭증 | **Aurora I/O-Optimized 요금제로 변경 및 캐시 계층(Redis) 도입** | 예측 가능한 고정 비용 및 I/O 절감 |
| DynamoDB Table Scan 쿼리로 인한 RCU 폭증 및 과금 | **Global Secondary Index(GSI) 설계 및 Scan 대신 Query 강제** | 쿼리 비용 및 응답 시간 90% 절감 |
| 특정 클라우드 DB 독점 API 사용에 따른 Vendor Lock-in | **Spring Data 추상화 계층 및 표준 인터페이스 래퍼 구축** | 멀티 클라우드 이식성 확보 |
| Multi-AZ Failover 시 순간적 커넥션 드롭 및 에러 발생 | **HikariCP 재연결 정책 설정 및 AWS RDS Proxy 도입** | 커넥션 유실 없는 매끄러운 절체 |

#### 한줄 요약
- I/O 최적화 요금제, GSI 설계, 표준 추상화 계층, RDS Proxy로 안정성을 확보한다.

## Ⅶ. 결론

- 원장 트랜잭션은 **Aurora**, 대규모 키값은 **DynamoDB** 선택

#### 한줄 요약
- 클라우드 데이터베이스는 워크로드 특성에 맞추어 RDS, Aurora, DynamoDB를 유기적으로 조합할 때 최상의 엔터프라이즈 가치를 창출한다.