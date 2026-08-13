---
sidebar:
  order: 101
  label: "101. 데이터베이스 용량 산정 (Database Capacity Planning)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터베이스 용량 산정 (Database Capacity Planning)"
date: "2026-08-13T20:22:00+09:00"
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

- 정의/개념: 성장•피크 부하로 DB 자원과 증설 시점을 정하는 **용량 산정**
- 배경/필요성: 사전 예측 없이는 **자원 고갈•응답 지연** 방지 불가

#### 한줄 요약

- 현재 데이터량과 인덱스·로그·복제본 오버헤드, 피크 부하, 증가율, 증설 리드타임을 함께 산정해 저장·처리 용량과 증설 시점을 결정한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Multi-Vector Sizing (다차원 통합 산정)**: 단순 Disk GB 크기 산정이 아닌, TPS(처리 속도), IOPS(디스크 렌더링), Memory(Buffer Pool 적중률), Network 등 4대 축의 동시 산정.
- **Threshold-Driven Lead Time Scaling**: Disk 사용률 70~80% 선에 닿는 시점과 Lead Time을 역산하여 자원 선행 증설 수행.

</details>

- **다차원 산정(Multi-Vector Sizing)**: 저장 용량(`Storage`), 입출력(`IOPS`), 메모리(`Buffer Pool`), 처리 능력(`CPU`) 4대 축 기반 산정.
- **오버헤드 반영(Overhead Multiplier)**: 인덱스•로그•복제본을 실측 비율로 합산
- **선제적 대응(Lead Time Scaling)**: 자원 고갈 임계치(`Threshold`) 도달 전 사전 증설 수행.
#### 한줄 요약

- 평균치가 아니라 가장 붐비는 시간과 성장 속도, 새 자원의 준비 시간을 함께 계산한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Pure Table Size Calculation**: `(Row Count) × (Sum of Column Average Byte Lengths)`.
- **Total Storage Formula**: `(Pure Table Size + Index Size) × (Replication Factor) × (Growth Rate) × (Safety Margin 1.3)`.

</details>

| 산정 영역 | 핵심 산식 및 기준 지표 |
|:---|:---|
| **저장 용량** | 데이터•인덱스•로그•복제본•증가율 합산 |
| **메모리** | 활성 데이터와 버퍼 적중률로 산정 |
| **입출력** | 피크 TPS당 읽기•쓰기 IOPS 실측 |
| **처리 능력** | 질의 CPU 시간•동시성•목표 여유율 반영 |

#### 한줄 요약

- 데이터 증가율과 피크 부하를 부하 시험 결과로 검증하여 증설 시점을 결정한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Load Testing Verification**: nJMeter / Locust 등으로 피크 부하를 시뮬레이션하여 실제 자원 고갈 지점(Break Point)을 검증하는 프로세스.

</details>

```text
[1. 성장 지표 수집]
               │
               ▼
[2. 저장 오버헤드 산정]
               │
               ▼
[3. 피크 처리량 산정]
               │
               ▼
[4. 자원 고갈 시점 예측]
               │
               ▼
[5. 증설 착수일 결정]
```

### 동작 원리

1. **성장 지표 수집**: 행 수•보존 기간•증가율 측정
2. **저장 오버헤드 산정**: 데이터•인덱스•로그•복제본 합산
3. **피크 처리량 산정**: TPS•IOPS•메모리•CPU 요구량 계산
4. **자원 고갈 시점 예측**: 성장 추세와 안전 여유로 한계일 산출
5. **증설 착수일 결정**: 한계일에서 조달•이관 기간 역산

#### 한줄 요약

- 증가 속도로 한계일을 구하고 시험으로 보정한 뒤 공사 기간만큼 먼저 확장한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Vertical Capacity vs Horizontal Capacity**: 단일 고성능 서버의 CPU/RAM/NVMe 확장 산정 대 Read Replica / Sharding 기반 노드 수평 분산 산정.

</details>

| 비교 항목 | Scale-Up (수직 확장 용량 산정) | Scale-Out (수평 확장 용량 산정) |
|:---|:---|:---|
| 주요 증설 대상 | **단일 서버의 CPU, RAM, NVMe SSD 확장** | **Read Replica 노드 또는 Shard 노드 추가** |
| 산정 복잡도 | 비교적 단순 (단일 서버 사양 튜닝) | **높음 (노드 간 분산 비율 및 샤드 키 고려)** |
| 한계 지점 | 단일 장비 최대 사양과 중단 위험 | 네트워크•재분배•분산 조정 비용 |
| 적용 구조 | 단일 RDBMS (MySQL, Oracle) | **Replica Read 분산 DB, NoSQL, Sharding** |

#### 한줄 요약

- 자료를 담는 공간, 요청을 처리하는 능력, 고장 때 대신 일할 여유를 각각 계산해야 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Temp Table / Log Bloat**: 복잡한 `GROUP BY / ORDER BY` 쿼리가 Disk Temp Table을 생성하거나, 장시간 트랜잭션으로 WAL Log가 커져 사전 예측치보다 디스크가 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 인덱스•로그 누락으로 디스크 조기 고갈 | **실측 오버헤드•보존 기간 반영** | 저장량 오차 축소 |
| 피크 IOPS 부족으로 질의 지연 | **부하 시험•스토리지 등급 조정** | I/O 병목 완화 |
| 조달 지연 중 자원 고갈 | **한계일에서 리드타임 역산** | 선제 증설 착수 |

> 사례: **신규 서비스 오픈 전 3년 데이터 용량 계산 및 AWS RDS Storage Auto-Scaling 적용**

#### 한줄 요약

- 원본뿐 아니라 색인•로그•사본을 더하고 가장 바쁜 날과 고장 상황까지 시험한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **용량 산정 수립 기준(Database Capacity Planning Standards)**: 4대 자원 축(Storage, RAM, IOPS, CPU), 오버헤드 계수(2배) 및 Lead Time 역산성에 의거한 체계.

</details>

- 병목이 단일 자원이면 **Scale-Up**, 분산 가능하면 Scale-Out 결정

#### 한줄 요약

- 용량 증설 착수 기준은 성장과 피크를 계산해 준비 기간보다 먼저 자원을 늘리게 한다.
