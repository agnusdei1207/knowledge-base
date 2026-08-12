---
sidebar:
  order: 32
  label: "032. RAID 레벨 0•1•5•6•10 비교 (RAID Levels)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "RAID 레벨 0•1•5•6•10 비교 (RAID Levels)"
date: "2026-08-08T16:43:00+09:00"
tags:
  - "notes-hardware"
weight: 32
extra:
  question_no: "032"
  source_status: "기출"
  source_history: "125회, 131회"
  priority: 70
  priority_note: "반복 기출•용량•장애•재구축 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **복수 디스크 독립 배열 (Redundant Array of Independent Disks, RAID)**: 복수의 물리 디스크(HDD/SSD)를 하나의 논리 저장 장치로 묶어 스트라이핑(Striping), 미러링(Mirroring), 패리티(Parity) 기법을 통해 입출력 대역폭 병렬 가속 및 장애 가용성(Fault Tolerance)을 보장하는 스토리지 아키텍처.
- **가용성 (Availability)**: 어레이 내부의 물리 디스크 1개 또는 2개가 고장 발생하더라도 서비스 정지 없이 읽기/쓰기를 지속 제공하는 시스템 안정성 지표.

</details>

- 정의/개념: 복수의 물리 디스크를 논리 어레이로 묶어 스트라이핑, 미러링, XOR 패리티 기술을 조합 적용함으로써 대역폭 가속 및 장애 가용성을 구현하는 **RAID(Redundant Array of Independent Disks)** 스토리지 아키텍처.
- 배경/필요성: 단일 물리 디스크의 억세스 속도 한계와 불시 하드웨어 고장(Disk Failure)에 따른 데이터 유실 위험을 방지하고, 미션 크리티컬 인프라의 24/365 고가용성을 유지하기 위해 도입.

#### 한줄 요약
- 복수 물리 디스크를 병렬 묶어 스트라이핑(성능), 미러링(복제), 패리티(XOR 연산) 조율을 통해 가용성 및 입출력 성능을 고도화하는 아키텍처.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **스트라이핑 (Striping / RAID 0)**: 데이터를 일정 블록 크기(Block Size, 예: 64KB)로 조각내어 여러 디스크에 분산 병렬 적재함으로써 입출력 대역폭을 극대화하는 방식.
- **미러링 (Mirroring / RAID 1)**: 동일한 데이터를 2개 이상의 디스크에 1:1 완벽 중복 복제 적재하여 고장 시 100% 즉시 복구를 제공하는 방식.
- **패리티 (Parity / RAID 5, 6)**: 디스크 고장 시 데이터 복원을 위해 XOR 산술 연산을 통해 생성해 두는 검사용 중복 데이터.
- **읽기-수정-쓰기 (Read-Modify-Write, RMW)**: RAID 5/6에서 부분 스트라이프 쓰기 발생 시, 기존 데이터와 기존 패리티를 읽어온 후(2 Reads) 신규 패리티를 계산하여 덮어쓰는(2 Writes) 4회 I/O 패널티 메커니즘.

</details>

- **스트라이핑(Striping)**을 통해 $N$개 디스크의 입출력 대역폭을 결합하여 병렬 읽기/쓰기 성능 극대화.
- **미러링(Mirroring)** 및 **XOR 패리티(Parity)**를 통해 물리 디스크 고장 발생 시에도 무중단 서비스 구동 및 데이터 실시간 복원.
- RAID 5/6의 경우 부분 블록 갱신 시 4회 I/O 지연이 수반되는 **읽기-수정-쓰기(Read-Modify-Write, RMW)** 쓰기 패널티 수반.

#### 한줄 요약
- Striping(입출력 가속), Mirroring(100% 복제), Parity(XOR 연산 데이터 복원)의 조합을 통해 스토리지의 용량, 성능, 내결함성을 트레이드오프함.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **RAID 컨트롤러 (RAID Controller)**: 호스트 CPU와 물리 디스크 배열 사이에서 하드웨어 ASIC 칩 형태로 스트라이핑 매핑, XOR 패리티 연산, Rebuild 및 Battery-Backed Cache를 통제하는 제어 장치.
- **스트라이프 매퍼 (Stripe Mapper)**: 호스트의 LBA(Logical Block Address) 주소를 물리 디스크 번호와 내부 블록 오프셋으로 분산 할당하는 매핑 엔진.
- **XOR 연산 엔진 (XOR Engine)**: RAID 5/6 하드웨어 컨트롤러 내에 탑재되어 초당 수 GB/s 속도로 XOR 패리티 계산 및 데이터 복원을 하드웨어 가속하는 연산 유닛.

</details>

```text
[ Hardware RAID Controller Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Host Bus Interface (PCIe / NVMe / SAS Host Adapter)       │
├───────────────────────────────────────────────────────────┤
│ Hardware RAID Controller ASIC                             │
│  ├─ Stripe Mapper (LBA to Disk/Offset Address Translation)│
│  ├─ XOR Hardware Engine (Parity Calculate & Rebuild)      │
│  └─ Battery-Backed Cache (NVRAM Write-Back Buffer)        │
├───────────────────────────────────────────────────────────┤
│ Array Disk Enclosure (Physical Disk 0, Disk 1 ... Disk N) │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 역할 및 작동 원리 | 차별점 및 실무 유용성 |
|:---|:---|:---|
| **RAID 컨트롤러** | 어레이 매핑, 패리티 연산, Write-Back 캐싱 및 Rebuild 총괄 | 전용 하드웨어 ASIC 적용으로 호스트 CPU 자원 소모 0% 실현 |
| **스트라이프 매퍼** | 호스트 LBA 주소를 $N$개 디스크의 스트라이프 단위로 쪼개어 배치 | 병렬 I/O 스트리밍 억세스 환경 조성 |
| **XOR 연산 엔진** | RAID 5($P = D_1 \oplus D_2 \oplus D_3$) 및 RAID 6(P+Q) 하드웨어 계산 | 패리티 생성 및 디스크 고장 시 실시간 복원 구동 |
| **Battery-Backed Cache**| 정전 시 캐시 메모리의 Write-Back 데이터를 NVRAM에 보호 | 정전 시 발생할 수 있는 **쓰기 구멍(Write Hole)** 현상 완벽 방지 |

#### 한줄 요약
- Hardware RAID Controller ASIC, Stripe Mapper, Hardware XOR Engine 및 Battery-Backed NVRAM Cache로 구동됨.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **부분 스트라이프 쓰기 (Partial Stripe Write)**: 전체 스트라이프 폭보다 작은 일부 블록 데이터만 갱신하는 억세스로, Read-Modify-Write 4회 I/O 지연을 유발하는 쓰기.
- **쓰기 구멍 (Write Hole)**: RAID 5/6 연산 중 데이터 갱신과 패리티 갱신 사이에 정전(Power Loss)이 발생하여 데이터와 패리티 불일치가 일어나는 결함 현상.

</details>

```text
[ RAID 5 Partial Stripe Write & RMW Flow ]
                      │
                      ▼
        [ 1. Host Write Request (Data D1') ]
                      │
                      ▼
   [ 2. Read Old Data (D1) & Old Parity (P) from Disks ] (2 Reads)
                      │
                      ▼
   [ 3. Calculate New Parity (P' = P XOR D1 XOR D1') ] (XOR Engine)
                      │
                      ▼
   [ 4. Write New Data (D1') & New Parity (P') to Disks ] (2 Writes)
                      │
                      ▼
   [ 5. Write-Back Cache Commit & Host Write Complete Response ]
```

### 동작 원리

1. **쓰기 요청 수신**: 호스트로부터 특정 블록 데이터($D_1'$) 쓰기 요청 수신.
2. **기존 블록 인출**: 4-I/O 패널티 메커니즘에 따라 기존 데이터($D_1$)와 기존 패리티($P$)를 디스크로부터 먼저 읽어옴(2 Reads).
3. **신규 패리티 계산**: **XOR 연산 엔진**이 $P' = P \oplus D_1 \oplus D_1'$ 산식을 계산함.
4. **신규 블록 파이프라인 기록**: 갱신된 데이터($D_1'$)와 신규 패리티($P'$)를 각각의 물리 디스크에 저장(2 Writes) 후 완료 반환.

#### 한줄 요약
- Host Request -> Read Old Data/Parity -> XOR Engine Calculate New Parity -> Write New Data/Parity 순의 4-I/O RMW 절차를 거침.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **RAID 0 (Striping)**: 미러/패리티 없이 데이터를 병렬 분산 전송하는 성능 위주 레벨 (가용성 없음).
- **RAID 1 (Mirroring)**: 100% 복제 적재를 제공하여 빠른 읽기 및 단순 복구를 보장하는 가용성 레벨 (용량 효율 50%).
- **RAID 5 (Distributed Single Parity)**: 1개 디스크 분량의 패리티를 전 디스크에 분산 저장하여 1개 디스크 고장을 버티는 레벨 (용량 $(N-1)S$).
- **RAID 6 (Distributed Dual Parity / P+Q)**: P패리티와 Q패리티(Reed-Solomon) 2개를 분산 저장하여 동시 2개 디스크 고장을 버티는 레벨 (용량 $(N-2)S$).
- **RAID 10 (Striping of Mirrors / 1+0)**: RAID 1 미러링 쌍을 먼저 묶고 이를 다시 RAID 0 스트라이핑으로 묶어 최상의 속도와 내결함성을 제공하는 고급 레벨.

</details>

| RAID 레벨 | RAID 0 | RAID 1 | RAID 5 | RAID 6 | RAID 10 (1+0) |
|:---|:---|:---|:---|:---|:---|
| **기본 메커니즘** | **Striping** | **Mirroring** | **Single Parity** | **Dual Parity (P+Q)**| **Mirror + Stripe** |
| **최소 디스크 수**| 2 개 | 2 개 | 3 개 | 4 개 | 4 개 |
| **실효 용량 비율**| $100\%$ ($N \cdot S$) | $50\%$ ($S$) | $\frac{N-1}{N} \cdot S$ | $\frac{N-2}{N} \cdot S$ | $50\%$ ($\frac{N}{2} \cdot S$) |
| **동시 허용 장애**| **0 개 (손실)** | 1 개 | **1 개** | **2 개** | 미러쌍 내 **1개씩** |
| **쓰기 패널티** | **없음** (1 Write) | 1 extra Write | **4 I/O (RMW)** | **6 I/O (RMW)** | **1 extra Write** |
| **주요 적용처** | 임시 고속 작업 | OS 부트 디스크 | 일반 웹/DB 서빙 | 대용량 백업 어레이 | **고성능 DBMS (OLTP)**|

#### 한줄 요약
- RAID 0(속도, 무보호), RAID 1(복제, 50% 용량), RAID 5(1개 고장 보호, RMW 패널티), RAID 6(2개 고장 보호), RAID 10(고성능 DB용 최상 조합)으로 나뉨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **핫 스페어 (Hot Spare)**: 디스크 배열에 예비로 꽂혀 있다가, 특정 디스크 고장 시 하드웨어가 자동으로 승격되어 Rebuild 데이터 복원을 시작하는 대기 디스크.
- **재구축 (Rebuild)**: 고장 디스크 교체 후 나머지 정상 디스크들의 패리티/미러 데이터를 읽어 새 디스크에 원래 데이터를 재생성 복원하는 고부하 작업.
- **순찰 읽기 (Patrol Read / Media Scan)**: 유휴 시간 중 어레이 전체 디스크 블록을 백그라운드 독출하여 배드 섹터(Bad Sector)를 미리 찾아 자동 치환하는 관리 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 대용량 HDD(16TB+) RAID 5 Rebuild 중 타 디스크 추가 고장으로 어레이 붕괴 | **RAID 6 (Dual Parity)** 및 **Hot Spare** 자동 승격 연동 | 동시 2개 고장 발생 시에도 어레이 복원 가용성 보장 |
| RAID 5/6 정전 발생 시 데이터-패리티 시점 불일치 **쓰기 구멍(Write Hole)** | 컨트롤러 내 **Battery-Backed NVRAM Cache** 및 Write Journal | 정전 발생 시 미완료 쓰기 원자적 완전 복구 |
| RAID 5 무작위 쓰기 시 Read-Modify-Write 4-I/O 패널티로 DB 속도 급락 | RMW 패널티가 없는 **RAID 10** 아키텍처로 변경 | OLTP 무작위 쓰기 처리량 3배 이상 대폭 상향 |
| 방치된 잠재 배드 섹터로 인해 Rebuild 시 Unrecoverable Read Error | 주기적 백그라운드 **순찰 읽기(Patrol Read)** 가동 | 배드 섹터 사전 감지 및 유휴 시간 미연 복구 |

#### 한줄 요약
- RAID 6 채택(Rebuild 중 2차 고장 방지), Battery-Backed NVRAM Cache, RAID 10 전환(RMW 소거) 및 Patrol Read를 구동함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **RAID 아키텍처 선택 기준 (RAID Decision Criteria)**: 대상 시스템의 입출력 워크로드(Random Write vs Sequential Read), 가용성 목표(1-disk vs 2-disk fault), 디스크 당 용량 크기 및 비용 효율성을 종합 평가하여 RAID 0/1/5/6/10을 확정하는 프레임워크.

</details>

- **RAID 아키텍처 선택 기준 (RAID Decision Criteria)**에 의거하여 OLTP 데이터베이스 등 무작위 쓰기가 극심한 하이엔드 시스템에는 RMW 패널티가 없는 **RAID 10**을 선택하고, 대용량 스토리지 인프라에는 이중 고장을 방지하는 **RAID 6** 및 **Battery-Backed Cache**와 Hot Spare 연동 체계 적용 필수.

#### 한줄 요약
- 데이터 가용성 및 성능 극대화를 위한 워크로드 맞춤형 RAID 레벨(RAID 10 / RAID 6) 채택 및 Battery-Backed Cache 기반 안정화 체계 적용.
