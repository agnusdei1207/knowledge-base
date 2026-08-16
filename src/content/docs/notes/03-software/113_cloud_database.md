---
sidebar:
  order: 113
  label: "113. 클라우드 데이터베이스 - RDS•Aurora•DynamoDB 비교"
  badge:
    text: "기출 • 50%"
    variant: note
title: "클라우드 데이터베이스 - RDS•Aurora•DynamoDB 비교"
date: "2026-08-13T21:49:00+09:00"
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

- **Cloud Database (클라우드 데이터베이스)**: 퍼블릭 클라우드(AWS, GCP, Azure) 환경에서 인프라 프로비저닝, OS/DB 패치, 백업, Failover 고가용성을 완전 관리형(Fully-Managed PaaS/SaaS) 형태로 제공받는 데이터베이스 서비스.
- **Amazon RDS (Relational Database Service)**: 전통적 RDBMS(MySQL, PostgreSQL, Oracle) 엔진 인스턴스를 EC2 기반의 완전 관리형으로 제공하는 1세대 클라우드 DB.
- **Amazon Aurora**: 컴퓨팅 노드와 6방향(6-Way) 분산 스토리지 레이어를 물리적으로 분리하여, 기존 RDS 대비 5배 이상의 TPS 성능과 초고속 Failover를 달성한 Cloud-Native RDBMS.
- **Amazon DynamoDB**: AWS의 서버리스(Serverless) Key-Value / Document NoSQL로, 밀리초 단위의 무제한 수평 확장(Scale-Out)과 Auto-Scaling을 지원하는 완전 관리형 DB.

</details>

- 정의/개념: 배포•백업•복제를 사업자가 관리하는 **클라우드 DB**
- 배경/필요성: 자체 DB 운영은 **조달 지연•패치•장애 복구 부담** 증가

#### 한줄 요약

- 설치와 백업 및 장애 조치를 클라우드가 맡고 사용자는 용량을 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Decoupled Architecture (Aurora)**: Compute 노드와 Distributed Storage 레이어를 상호 독립 분리.
- **Serverless & On-Demand (DynamoDB)**: 프로비저닝 없이 쿼리 횟수 및 디스크 사용량 단위 자동 과금.

</details>

- **AWS RDS**: 인스턴스 단위 기반, Multi-AZ 동기식 복제 Failover 지원
- **AWS Aurora**: Compute/Storage 분리, 10GB~128TB 가변 자동 확장, 15개 Read Replica 수용
- **AWS DynamoDB**: 서버리스 NoSQL, 파티션 키 기반 자동 분산

#### 한줄 요약

- 운영 작업은 줄지만 서비스별 확장 단위•비용•종속성이 다르다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AWS Multi-AZ Deployment**: 2개 이상의 가용 영역(AZ)에 Primary DB와 Standby DB를 동기 복제(Synchronous Replication)하여 주 노드 다운 시 DNS 엔드포인트 자동 전환(Failover)을 보장하는 구조.

</details>

| 구성요소 | 책임 |
|:---|:---|
| 관리 제어면 | 프로비저닝•패치•백업 정책 수행 |
| 접속 엔드포인트 | 연결과 장애전환 대상을 추상화 |
| 컴퓨팅 계층 | SQL•키 기반 요청 처리와 자원 확장 |
| 스토리지 계층 | 데이터 복제•내구성•용량 관리 |
| 관측 계층 | 지연•용량•오류•비용 지표 제공 |

#### 한줄 요약

- 운영 관리자, 접속 주소, 요청 안내자, 처리부, 사본 저장부로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Aurora 6-Way Storage Replication**: Aurora는 데이터를 6개 조각으로 쪼개어 3개 가용 영역(AZ)에 2개씩 복제 후 4/6 Write Quorum 수용.

</details>

```text
[주 인스턴스 장애]
       │
       ▼
1. 상태 검사 실패
       │
       ▼
2. 장애전환 대상 선택
       │
       ▼
3. 새 쓰기 역할 승격
       │
       ▼
4. 엔드포인트 갱신
       │
       ▼
5. 연결•재시도 복구
```

### 동작 원리

1. **상태 검사 실패**: 제어면이 주 인스턴스 비정상 판정
2. **장애전환 대상 선택**: 복제 상태•우선순위로 후보 결정
3. **새 쓰기 역할 승격**: 후보 인스턴스에 쓰기 권한 부여
4. **엔드포인트 갱신**: 접속 주소를 새 쓰기 노드로 전환
5. **연결•재시도 복구**: 실패 요청을 정책에 따라 재처리

#### 한줄 요약

- 클라우드가 고장을 감지해 사본을 원본으로 바꾸고 같은 접속 주소를 새 원본에 연결한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cloud DB Selection Matrix**: 레거시 이관은 RDS, 고성능 대용량 RDBMS는 Aurora, 초고속 수평 분산 NoSQL은 DynamoDB 선택.

</details>

| 선택 기준 항목 | Amazon RDS | Amazon Aurora | Amazon DynamoDB |
|:---|:---|:---|:---|
| 적합 워크로드 | 온프레미스 레거시 DB 이관 | **대규모 OLTP 웹 서비스 (고성능)** | **서버리스, 초고속 세션/카탈로그** |
| 성능 특성 | 인스턴스•EBS 구성에 좌우 | **분산 스토리지•읽기 복제본** | 파티션 키•용량 모드에 좌우 |
| 비용 체계  | 인스턴스 사양 및 EBS 용량 고정 | 컴퓨팅 사양 + I/O 사용량 기반 | Read/Write Capacity Unit (RCU/WCU) |
| 트랜잭션 | 엔진별 관계형 트랜잭션 | **MySQL•PostgreSQL 호환 트랜잭션** | 제한 범위 내 트랜잭션 API |

#### 한줄 요약

- 기존 관계형 엔진은 RDS, 분산 저장형 관계형은 Aurora, 키 중심 자동 분산은 DynamoDB를 검토한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Vendor Lock-in**: DynamoDB 등 특정 클라우드 전용 API 사용 시 타 클라우드(GCP, Azure)나 온프레미스로 마이그레이션하기 극도로 어려워지는 현상.

</details>

| 위험 요소 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| Aurora 사용 시 I/O 비용 폭발 (**비용 폭탄**) | 빈번한 작은 쿼리 호출로 I/O 수천만 건 과금 | **Aurora Standard 대신 Aurora I/O-Optimized 요금제 변경** |
| DynamoDB Scan 쿼리로 RCU 폭증 | Key 조건 없이 전체 테이블 Scan 쿼리 투척 | **Global Secondary Index (GSI) 생성 및 Query 사용** |
| DynamoDB 전용 API 사용에 따른 **Vendor Lock-in** | AWS 독점 DynamoDB SDK 디펜던시 | **Spring Data DynamoDB / 래퍼 인터페이스 레이어 배치** |

> 사례: **배달의민족 / 당근마켓 Aurora PostgreSQL & DynamoDB Polyglot 아키텍처**

#### 한줄 요약

- 자동 전환 기능이 있어도 실제로 얼마나 멈추고 어떤 요청을 다시 보내야 하는지 시험해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **클라우드 DB 수립 기준(Cloud Database Standards)**: 엔진 호환성, RTO/RPO SLA, I/O 비용 분석 및 Serverless 요구성에 의거한 체계.

</details>

- 엔진 호환은 **RDS**, 분리형 관계 DB는 Aurora, 키 접근은 DynamoDB 선택

#### 한줄 요약

- 서비스 선택 축은 운영 자동화와 사용자의 설계•복구 책임을 함께 비교한다.
