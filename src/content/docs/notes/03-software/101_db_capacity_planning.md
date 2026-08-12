---
sidebar:
  order: 101
  label: "101. 데이터베이스 용량 산정 (Database Capacity Planning)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터베이스 용량 산정 (Database Capacity Planning)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 101
extra:
  question_no: "101"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출, 저장량•증가율 용량 산정"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Database Capacity Planning (데이터베이스 용량 산정 및 계획)**: 데이터베이스 서비스의 향후 비즈니스 성장률, 피크 타임 TPS/IOPS, 데이터 수명주기를 정량 분석하여, 디스크 Storage, Memory, CPU, Network 대역폭 사양과 증설 타임라인을 사전 설계하는 자원 관리 공학.
- **Overhead Multiplier (운영 오버헤드 계수)**: pure 순수 테이블 데이터 크기 외에 B+Tree 인덱스, WAL/Redo Log, Temp Table, DB Buffer Pool, Replication Replica 용량 오버헤드를 합산하기 위해 적용하는 승수 (보통 1.5~2.5배 체계).
- **Lead Time for Expansion (증설 조달 선행 시간)**: DB 자원 고갈 선(Threshold 80%) 도달 이전에 Hardware 주문, 인프라 승인, 데이터 마이그레이션을 완료하기 위해 미리 조치를 시작해야 하는 유예 기간.

</details>

- **정의**: 비즈니스 성장률, 피크 타임 성능(`TPS`/`IOPS`), 데이터 수명주기를 정량 분석하여 저장 공간, 메모리, CPU 사양 및 증설 타임라인을 사전 설계하는 자원 관리 공학인 **데이터베이스 용량 산정(Database Capacity Planning)**.
- **필요성**: 디스크 과부하(`Disk Full`)로 인한 서버 락업 예방 및 피크 타임 자원 고갈에 따른 쿼리 타임아웃 차단.

#### 한줄 요약

- 현재 데이터량과 인덱스·로그·복제본 오버헤드, 피크 부하, 증가율, 증설 리드타임을 함께 산정해 저장·처리 용량과 증설 시점을 결정한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Multi-Vector Sizing (다차원 통합 산정)**: 단순 Disk GB 크기 산정이 아닌, TPS(처리 속도), IOPS(디스크 렌더링), Memory(Buffer Pool 적중률), Network 등 4대 축의 동시 산정.
- **Threshold-Driven Lead Time Scaling**: Disk 사용률 70~80% 선에 닿는 시점과 Lead Time을 역산하여 자원 선행 증설 수행.

</details>

- **다차원 산정(Multi-Vector Sizing)**: 저장 용량(`Storage`), 입출력(`IOPS`), 메모리(`Buffer Pool`), 처리 능력(`CPU`) 4대 축 기반 산정.
- **오버헤드 반영(Overhead Multiplier)**: 순수 데이터 대비 인덱스, 로그, 복제본 등 2배 수준의 용량 산정.
- **선제적 대응(Lead Time Scaling)**: 자원 고갈 임계치(`Threshold`) 도달 전 사전 증설 수행.
#### 한줄 요약

- 평균치가 아니라 가장 붐비는 시간과 성장 속도, 새 자원의 준비 시간을 함께 계산한다.

## Ⅲ. 구조 및 구성요소 (DB 용량 산정 공식 및 4대 영역)

<details><summary>핵심 용어</summary>

- **Pure Table Size Calculation**: `(Row Count) × (Sum of Column Average Byte Lengths)`.
- **Total Storage Formula**: `(Pure Table Size + Index Size) × (Replication Factor) × (Growth Rate) × (Safety Margin 1.3)`.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Database Capacity Planning 4대 핵심 축               │
├─────────────────────┬───────────────────┬──────────────────────────────┤
│ 1. Disk Storage     │ 2. Memory Buffer  │ 3. IOPS & CPU                │
├─────────────────────┼───────────────────┼──────────────────────────────┤
│ • 순수 테이블 데이터│ • InnoDB Buffer   │ • Peak TPS 조건 처리         │
│ • B+Tree 인덱스 용량│   Pool (RAM 60~70%)│ • Random Disk Read/Write IOPS│
│ • WAL/Redo/Binlog   │ • OS Kernel Cache │ • Peak Concurrency           │
├─────────────────────┴───────────────────┴──────────────────────────────┤
│ 4. Replication & DR (Replica Node n개 오버헤드 합산)                  │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터베이스 용량 산정 시 디스크 용량, 인메모리 버퍼 풀, IOPS/CPU 처리 성능, 복제본 오버헤드 4대 영역을 통합 계산하는 아키텍처.

| 산정 영역 | 핵심 산식 및 기준 지표 | 실무 적용 튜닝 값 |
|:---|:---|:---|
| **Disk Storage (저장 용량)** | **`Total = (Pure Data + Index + Log) × Replica Factor × Growth Rate × 1.3`** | 순수 데이터 대비 **1.5~2.5배** 오버헤드 설정 |
| **Memory Buffer (메모리)** | **`InnoDB Buffer Pool = System RAM × 70%`** | Hot Data 인덱스 및 활성 튜플 100% 캐싱 |
| **IOPS (디스크 처리량)** | **`Peak TPS × (Read IOPS + Write IOPS per Transaction)`** | SSD NVMe 기반 **10,000~50,000 IOPS** 확보 |
| **CPU Cores (처리 능력)** | **`Peak TPS × Target Query CPU Time / Target CPU Util (70%)`** | 피크 시 CPU 사용률 **70% 이하** 타깃팅 |

#### 한줄 요약

- 데이터 증가율과 피크 부하를 부하 시험 결과로 검증하여 증설 시점을 결정한다.

## Ⅳ. 흐름도 (용량 산정 및 선행 증설 5단계 절차)

<details><summary>핵심 용어</summary>

- **Load Testing Verification**: nJMeter / Locust 등으로 피크 부하를 시뮬레이션하여 실제 자원 고갈 지점(Break Point)을 검증하는 프로세스.

</details>

```text
[1. 비즈니스 성장 수치 수집 (일별 회원수, 주문건수)]
               │
               ▼
[2. 테이블별 Row Byte 크기 및 인덱스 오버헤드 산정]
               │
               ▼
[3. Peak TPS / IOPS / Buffer Pool 메모리 용량 확정]
               │
               ▼
[4. n년 후 자원 고갈 시점 (Threshold 80%) 산출]
               │
               ▼
[5. Lead Time 역산하여 Proactive 증설 일정 확정]
```

### 동작 원리

1. **Row Sizing**: 컬럼별 타입(BigInt: 8B, VarChar: Avg Byte) 합산 후 1건당 평균 Byte 산출.
2. **Growth Estimation**: 1년 후 튜플 증가량(예: 1억 건) 곱셈 후 B+Tree 인덱스 오버헤드(50%) 및 Binlog 용량 합산.
3. **Threshold Calculation**: 80% 디스크 채움 지점 도달 일자 산출 후 **Lead Time(2개월) 전 조치 착수**.

#### 한줄 요약

- 증가 속도로 한계일을 구하고 시험으로 보정한 뒤 공사 기간만큼 먼저 확장한다.

## Ⅴ. 종류 및 비교 (Scale-Up 대 Scale-Out 용량 산정)

<details><summary>핵심 용어</summary>

- **Vertical Capacity vs Horizontal Capacity**: 단일 고성능 서버의 CPU/RAM/NVMe 확장 산정 대 Read Replica / Sharding 기반 노드 수평 분산 산정.

</details>

| 비교 항목 | Scale-Up (수직 확장 용량 산정) | Scale-Out (수평 확장 용량 산정) |
|:---|:---|:---|
| 주요 증설 대상 | **단일 서버의 CPU, RAM, NVMe SSD 확장** | **Read Replica 노드 또는 Shard 노드 추가** |
| 산정 복잡도 | 비교적 단순 (단일 서버 사양 튜닝) | **높음 (노드 간 분산 비율 및 샤드 키 고려)** |
| 한계 지점 | 물리적 서버 최대 한계 (RAM 1TB, CPU 128 Core) | 무제한 수평 확장 가능 (네트워크 대역폭 한계) |
| 적용 구조 | 단일 RDBMS (MySQL, Oracle) | **Replica Read 분산 DB, NoSQL, Sharding** |

#### 한줄 요약

- 자료를 담는 공간, 요청을 처리하는 능력, 고장 때 대신 일할 여유를 각각 계산해야 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Temp Table / Log Bloat**: 복잡한 `GROUP BY / ORDER BY` 쿼리가 Disk Temp Table을 생성하거나, 장시간 트랜잭션으로 WAL Log가 커져 사전 예측치보다 디스크가 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 인덱스 및 로그 용량을 누락하여 예상보다 디스크 일찍 고갈 | **순수 데이터의 2배를 저장 오버헤드 기본값으로 산정** | Disk Full 사고 차단 |
| 피크 타임 IOPS 부족으로 쿼리 타임아웃 폭증 | **AWS EBS gp3 IOPS 튜닝 및 NVMe SSD 캐시 적용** | IOPS 병목 소멸 |
| 증설 승인 및 구동 수주 지연으로 자원 고갈 타격 | **자원 사용률 70% 도달 시 Lead Time 역산 선제 증설**| 선제적 안심 운용 |

> 사례: **신규 서비스 오픈 전 3년 데이터 용량 계산 및 AWS RDS Storage Auto-Scaling 적용**

#### 한줄 요약

- 원본뿐 아니라 색인•로그•사본을 더하고 가장 바쁜 날과 고장 상황까지 시험한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **용량 산정 수립 기준(Database Capacity Planning Standards)**: 4대 자원 축(Storage, RAM, IOPS, CPU), 오버헤드 계수(2배) 및 Lead Time 역산성에 의거한 체계.

</details>

- **용량 산정 수립 기준 적용** (신규 IT 시스템 구축 시 3년 주기 `Storage`/`Memory`/`IOPS` 선제 용량 산정 필수 수용)

#### 한줄 요약

- 용량 증설 착수 기준은 성장과 피크를 계산해 준비 기간보다 먼저 자원을 늘리게 한다.
