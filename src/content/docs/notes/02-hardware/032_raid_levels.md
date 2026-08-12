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

- **RAID(Redundant Array of Independent Disks)**: 복수의 물리 디스크를 논리적으로 묶어 스트라이핑(Striping), 미러링(Mirroring), 패리티(Parity) 기법으로 성능과 가용성을 보장하는 스토리지 아키텍처.
- **가용성(Availability)**: 어레이 내부 디스크 고장 시에도 서비스 정지 없이 데이터 접근성을 유지하는 시스템 안정성.

</details>

- 정의: 복수 물리 디스크를 논리 어레이로 구성하여 병렬 I/O(Striping)와 복제/검사(Mirroring/Parity) 기술로 고성능·고가용성을 구현하는 스토리지 아키텍처.
- 배경: 단일 디스크의 성능 한계 극복 및 하드웨어 고장(Disk Failure)에 따른 데이터 유실 방지.

#### 한줄 요약
- Striping, Mirroring, Parity 조합을 통한 성능 및 장애 가용성 보장 아키텍처.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **스트라이핑(Striping)**: 데이터를 블록 단위로 분산 적재하여 입출력 대역폭을 가속하는 기법.
- **미러링(Mirroring)**: 데이터를 2개 이상 디스크에 1:1 복제하여 고장 시 즉시 복구를 지원하는 기법.
- **패리티(Parity)**: 디스크 고장 시 데이터 복원을 위한 XOR 연산 기반 검사 데이터.
- **RMW(Read-Modify-Write)**: RAID 5/6에서 부분 블록 갱신 시 4회 I/O 지연을 발생시키는 메커니즘.

</details>

- Striping: 물리 디스크 개수에 비례한 병렬 입출력 가속.
- Mirroring/Parity: 물리 디스크 장애 시에도 무중단 서비스 및 실시간 데이터 복원.
- 쓰기 패널티: RAID 5/6 환경에서 RMW로 인한 I/O 지연 발생.

#### 한줄 요약
- 성능(Striping), 복제(Mirroring), 복원(Parity) 조합을 통한 가용성·효율성 트레이드오프 기법.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **RAID 컨트롤러(RAID Controller)**: 스트라이핑 매핑, 패리티 연산, 재구축(Rebuild)을 통제하는 하드웨어 ASIC.
- **스트라이프 매퍼(Stripe Mapper)**: 호스트의 LBA를 물리 디스크 번호와 블록 오프셋으로 매핑하는 엔진.
- **XOR 엔진(XOR Engine)**: 패리티 생성 및 데이터 복원을 가속하는 연산 유닛.

</details>

```text
[ 하드웨어 RAID 컨트롤러 구조 ]
┌───────────────────────────────────────────────────────────┐
│ 호스트 버스 인터페이스 (PCIe / NVMe 등)                     │
├───────────────────────────────────────────────────────────┤
│ 하드웨어 RAID 컨트롤러 ASIC                                 │
│  ├─ 스트라이프 매퍼 (주소 변환)                              │
│  ├─ XOR 연산 엔진 (패리티 계산/복구)                         │
│  └─ 배터리 보호 캐시 (쓰기 버퍼)                             │
├───────────────────────────────────────────────────────────┤
│ 물리 디스크 배열 (Disk 0, Disk 1 ... Disk N)                │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 역할 및 원리 | 차별점 |
|:---|:---|:---|
| RAID 컨트롤러 | 어레이 통제 및 ASIC 기반 연산 | 호스트 CPU 자원 소모 제로 |
| 스트라이프 매퍼 | LBA 주소 분산 할당 | 병렬 I/O 스트리밍 조성 |
| XOR 엔진 | RAID 5/6 패리티 하드웨어 계산 | 실시간 데이터 복원 가속 |
| 배터리 캐시 | 정전 시 Write-Back 데이터 보호 | 쓰기 구멍(Write Hole) 원천 방지 |

#### 한줄 요약
- RAID ASIC 컨트롤러, 스트라이프 매퍼, XOR 연산 엔진 및 배터리 보호 캐시 기반 운용.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **부분 스트라이프 쓰기(Partial Stripe Write)**: 전체 스트라이프보다 작은 단위의 갱신으로 RMW 4회 I/O 지연 유발.
- **쓰기 구멍(Write Hole)**: 연산 도중 정전 발생 시 데이터/패리티 불일치 결함 현상.

</details>

```text
[ RAID 5 부분 스트라이프 쓰기(RMW) 흐름 ]
                      │
                      ▼
         [ 1. 데이터 쓰기 요청 (D1') ]
                      │
                      ▼
    [ 2. 기존 데이터(D1), 패리티(P) 읽기 ] (2 Reads)
                      │
                      ▼
    [ 3. 신규 패리티 계산 (P' = P XOR D1 XOR D1') ]
                      │
                      ▼
    [ 4. 신규 데이터(D1'), 패리티(P') 기록 ] (2 Writes)
                      │
                      ▼
    [ 5. 쓰기 완료 반환 ]
```

- 동작: 요청 수신 -> 데이터/패리티 읽기 -> XOR 엔진으로 신규 패리티 계산 -> 데이터/패리티 기록 순으로 RMW 절차 수행.

#### 한줄 요약
- Host Write 요청 -> RMW 기반 패리티 갱신 -> 신규 데이터 기록 절차.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **RAID 0(Striping)**: 성능 위주의 분산 저장, 가용성 미지원.
- **RAID 1(Mirroring)**: 100% 복제, 장애 시 즉시 복구(용량 효율 50%).
- **RAID 5(Distributed Parity)**: 분산 패리티로 1개 장애 허용, RMW 패널티 발생.
- **RAID 6(Dual Parity)**: P+Q 이중 패리티로 2개 장애 허용.
- **RAID 10(1+0)**: 미러링 후 스트라이핑, 고성능/내결함성 최상.

</details>

| RAID | 메커니즘 | 실효 용량 | 허용 장애 | 쓰기 패널티 | 적용처 |
|:---|:---|:---|:---|:---|:---|
| 0 | Striping | 100% | 0 | 없음 | 임시 고속 작업 |
| 1 | Mirroring | 50% | 1 | 1 Write | OS 부트 |
| 5 | Single Parity | (N-1)/N | 1 | 4 I/O | 웹/DB 서빙 |
| 6 | Dual Parity | (N-2)/N | 2 | 6 I/O | 대용량 백업 |
| 10 | Mirror+Stripe | 50% | 1(쌍별) | 1 Write | OLTP DB |

#### 한줄 요약
- 용량·성능·내결함성을 고려한 RAID 레벨별 매커니즘 및 워크로드 맞춤형 선택.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **핫 스페어(Hot Spare)**: 장애 시 자동 승격되어 재구축(Rebuild)을 수행하는 예비 디스크.
- **재구축(Rebuild)**: 장애 디스크 교체 후 나머지 데이터를 읽어 새 디스크에 원래 데이터를 재생성하는 복구 작업.
- **순찰 읽기(Patrol Read)**: 유휴 시간 중 백그라운드 독출로 배드 섹터를 사전 치환하는 관리 기법.

</details>

| 문제 원인 | 실무적 대책 | 기대 효과 |
|:---|:---|:---|
| 대용량 Rebuild 중 추가 장애 | RAID 6 및 핫 스페어 연동 | 동시 2개 장애 복원 가용성 |
| 정전 시 쓰기 구멍(Write Hole) | 배터리 보호 캐시 및 Write Journal | 미완료 쓰기 원자적 복구 |
| DB 무작위 쓰기 RMW 지연 | RAID 10 구조 전환 | 처리량 3배 이상 향상 |
| Rebuild 시 Unrecoverable Read Error | 순찰 읽기(Patrol Read) 수행 | 배드 섹터 사전 감지/복구 |

#### 한줄 요약
- RAID 6/10 채택, 배터리 캐시, Patrol Read를 통한 고가용성 구현.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **RAID 아키텍처 선택 기준 (RAID Decision Criteria)**: 대상 시스템의 입출력 워크로드(Random Write vs Sequential Read), 가용성 목표(1-disk vs 2-disk fault), 디스크 당 용량 크기 및 비용 효율성을 종합 평가하여 RAID 0/1/5/6/10을 확정하는 프레임워크.

</details>

- OLTP DB 등 하이엔드 시스템에는 RMW 패널티 없는 RAID 10을, 대용량 스토리지 인프라에는 이중 고장 방지용 RAID 6, 배터리 보호 캐시 및 Hot Spare 연동 체계.

#### 한줄 요약
- 데이터 가용성/성능 최적화를 위한 워크로드별 RAID 레벨 채택 및 하드웨어 안정화 체계 적용.
