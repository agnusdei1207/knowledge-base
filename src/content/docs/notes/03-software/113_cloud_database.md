---
sidebar:
  order: 113
  label: "113. 클라우드 데이터베이스 - RDS•Aurora•DynamoDB"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 데이터베이스 - RDS•Aurora•DynamoDB 비교"
date: "2026-08-31T10:48:00+09:00"
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
- 배경/필요성: 온프레미스 데이터베이스의 물리 하드웨어 프로비저닝 리드타임, 수동 OS/DBMS 패치 및 백업·복구 관리 오버헤드와 급격한 트래픽 변동에 대한 유연한 용량 확장(Elasticity) 한계를 극복하고, 클라우드 제공업체(CSP)가 인프라 유지보수와 고가용성(Multi-AZ)을 완전관리형(Fully-Managed)으로 전담하며 인스턴스형(RDS), 컴퓨팅-스토리지 분리형(Aurora), 서버리스 분산형(DynamoDB)을 워크로드별로 선택할 수 있는 클라우드 데이터베이스를 도입하여 **운영 TCO를 절감하고 비즈니스 민첩성과 인프라 가용성을 극대화**할 필요

#### 한줄 요약
- 관리형 DB는 운영 비용을 사업자에게 넘기는 대신 튜닝 여지와 이식성을 함께 반납하는 거래이므로, 선택 기준은 성능 수치보다 어느 수준의 통제를 포기할 수 있느냐가 된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Compute-Storage Decoupling**: Aurora에서 컴퓨팅 인스턴스와 분산 스토리지 계층을 분리하여 독립 확장 및 초고속 크래시 복구를 실현한 구조.
- **Multi-AZ Replication**: 여러 가용 영역에 복제본을 배치해 자동 장애조치를 지원하는 구성.

</details>

- OS 및 DBMS 패치, 자동 백업, 복구를 전담하는 **완전관리형(Fully-Managed) 서비스**
- Multi-AZ 복제와 스토리지 쿼럼을 통한 **고가용성** 지원
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
|   |-- Primary 인스턴스
|   `-- Standby 인스턴스
|-- 2. Amazon Aurora (컴퓨팅-스토리지 분리형 클라우드 네이티브 RDBMS)
|   |-- Writer·Read Replica
|   `-- 6-Way 분산 스토리지 계층 (3개 AZ에 6벌 복제, 4/6 쓰기 쿼럼)
`-- 3. Amazon DynamoDB (완전관리형 서버리스 NoSQL)
    |-- Request Router
    `-- 자동 파티션 노드
```

선의 의미: 계층 및 인스턴스형(RDS), 스토리지 분리형(Aurora), 서버리스 분산형(DynamoDB) 아키텍처 구조

| 구성요소 | 책임 |
|:---|:---|
| Amazon RDS | 표준 관계형 엔진의 관리형 인스턴스 제공 |
| Amazon Aurora | **컴퓨팅·스토리지 분리형 RDB** 제공 |
| Amazon DynamoDB | 파티션 기반 **관리형 NoSQL** 제공 |
| 자동 장애전환 | 장애 시 복제본 승격과 엔드포인트 갱신 |

#### 한줄 요약
- 세 서비스는 연산과 저장을 어디서 끊었는지로 갈려 RDS는 둘을 인스턴스에 함께 묶고 Aurora는 저장을 떼어 복제 비용을 낮추며 DynamoDB는 둘 다 감춰 확장을 얻는 대신 질의 자유도를 내준다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Multi-AZ Failover 절차**: Primary 장애 $\to$ 하트비트 타임아웃 $\to$ Replica를 Primary로 승격 $\to$ CNAME DNS 갱신 $\to$ 서비스 재개.

</details>

```text
주(Primary) DB 인스턴스에 하드웨어 크래시 발생
        │
   [장애 감지] 클라우드 제어면이 상태 확인 실패 감지
        │
   [승격 절차] Multi-AZ Standby 또는 최저 지연 Aurora Read Replica를 새 Writer로 승격
        │
   [DNS 엔드포인트 갱신] DB CNAME 레코드가 가리키는 IP를 신규 Writer로 자동 수정
        │
   클라이언트 커넥션 풀이 신규 Writer로 재연결해 서비스 재개
```

#### 한줄 요약
- 실제 복구 시간은 장애 감지보다 DNS 갱신이 클라이언트까지 전파되는 구간이 좌우하므로, 페일오버가 자동이라는 사실만으로 무중단이 되지 않고 연결 재시도 설계가 함께 있어야 한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RDS vs Aurora vs DynamoDB**: 표준 호환성(RDS), 고성능 트랜잭션(Aurora), 대규모 수평 확장(DynamoDB).

</details>

| 비교 항목 | Amazon RDS (표준 인스턴스) | Amazon Aurora (클라우드 네이티브) | Amazon DynamoDB (서버리스 NoSQL) |
|:---|:---|:---|:---|
| 아키텍처 모델 | **단일 인스턴스 + EBS 스토리지** | **컴퓨팅-스토리지 분리형 클러스터** | **완전관리형 서버리스 분산 NoSQL** |
| 읽기 확장 | 엔진별 읽기 복제본 | **공유 스토리지 읽기 복제본** | 파티션 기반 자동 확장 |
| 처리 특성 | 표준 관계형 엔진 특성 | 분산 스토리지 기반 관계형 처리 | 키 기반 분산 처리 |
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
| DynamoDB Scan에 따른 RCU 증가 | 접근 패턴별 **GSI·Query** 설계 | 읽기 비용과 지연 감소 |
| 특정 클라우드 DB 독점 API 사용에 따른 Vendor Lock-in | **Spring Data 추상화 계층 및 표준 인터페이스 래퍼 구축** | 멀티 클라우드 이식성 확보 |
| Multi-AZ 전환 중 커넥션 단절 | **재연결 정책·RDS Proxy** 적용 | 일시 오류와 복구 시간 완화 |

#### 한줄 요약
- I/O 최적화 요금제, GSI 설계, 표준 추상화 계층, RDS Proxy로 안정성을 확보한다.

## Ⅶ. 결론

- 현대 클라우드 네이티브 아키텍처 및 디지털 전환의 **표준 영속성 인프라 플랫폼**으로 확립되었으며, 실무 전환 시에는 **단순 Lift & Shift 마이그레이션에는 표준 RDS, 고성능 대규모 OLTP 및 엔터프라이즈 원장에는 컴퓨팅-스토리지 분리형 Aurora(I/O-Optimized), 트래픽 변동이 극심한 대규모 키-값/문서 처리에는 DynamoDB를 채택하고, 순간적인 커넥션 폭주를 방어하는 RDS Proxy와 복원력 있는 재연결(Retry) 패턴**을 결합하여 비용 최적화와 서비스 연속성을 동시 보증

#### 한줄 요약
- 엔진 호환은 RDS, 분리형 RDB는 Aurora, 키 접근은 DynamoDB를 선택한다.
