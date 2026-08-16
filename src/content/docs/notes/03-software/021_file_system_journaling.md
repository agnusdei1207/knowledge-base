---
sidebar:
  order: 21
  label: "021. 파일 시스템 저널링 (File System Journaling)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "파일 시스템 저널링 (File System Journaling)"
date: "2026-08-13T13:43:00+09:00"
tags:
  - "notes-software"
weight: 21
extra:
  question_no: "021"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "저널링은 장애 후 일관성 복구 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Journaling (저널링)**: 파일 시스템의 메타데이터나 파일 데이터 변경 사항을 실제 디스크 블록(Home Block)에 반영하기 전, 순차 전용 저널 영역(Journal Log)에 1차로 커밋 기록하는 장애 복구 기술.
- **fsck (File System Check)**: 비저널링 파일 시스템 장애 발생 시 전체 디스크 블록을 풀스캔하여 일관성을 검사 및 수리하는 명령어로, 디스크 용량 증대에 따라 수 시간 이상 소모되는 한계 보유.

</details>

- 정의/개념: 변경 정보를 본래 블록보다 먼저 기록하는 **파일 시스템 저널링**
- 배경/필요성: 비정상 종료는 부분 갱신으로 **메타데이터 불일치** 유발

#### 한줄 요약

- 변경 선기록과 커밋 기반 파일 시스템 저널링이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Write-Ahead Logging (WAL)**: 실제 물리 블록 데이터 갱신에 앞서, 해당 트랜잭션 갱신 로그를 저널 영역에 먼저 기록 완료하는 기본 원칙.
- **Checkpoint (체크포인트)**: 저널 영역에 성공적으로 기록된 커밋 트랜잭션 데이터를 물리 디스크 Home Block으로 완전 동기화 이송하는 주기적 작업.

</details>

- **Write-Ahead Logging** 원칙으로 복구 대상 범위 축소
- 장애 시 커밋된 **Journal Log**를 재생해 일관성 복원
- 저널링 모드 설정(**Writeback, Ordered, Journal**)에 따른 성능 및 내구성 조율

#### 한줄 요약

- 보호 범위 확대에 따른 복구성과 쓰기 증폭의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Transaction Block**: 하나 이상의 파일 연산(Inode 변경, Block Allocation 등)을 묶어 단위 커밋 처리하는 저널 트랜잭션 단위.

</details>

```text
[트랜잭션 관리자] -------- [저널 영역] -------- [체크포인트 처리기]
                                 |
                                 |
                              [복구기]
```

선의 의미: 트랜잭션 관리자가 저널 영역에 WAL 로그를 기록하고, 체크포인트 처리기가 디스크로 이송하며, 장애 시 복구기가 로그를 Replay하여 비정상 종료를 복구하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| Transaction Manager | 파일 변경 연산을 트랜잭션 단위로 묶어 커밋 조율 |
| Journal Ring Buffer | **WAL** 로그, Transaction Metadata, Commit Block을 순차 수용하는 전용 영역 |
| Checkpoint Handler | 저널 영역 커밋 완료 트랜잭션을 실제 디스크 Home Block으로 **Checkpointing** 이송 |
| Recovery Replay Engine | 비정상 재부팅 시 저널의 커밋 레코드를 탐색하여 **Replay(Redo)** 또는 **Rollback(Undo)** 수행 |

#### 한줄 요약

- 트랜잭션, 체크포인트, 본래 블록의 결합이 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Journal Replay (REDO)**: 전원 정상 차단 실패 후 부팅 시, 저널에 Commit 표식이 완료된 트랜잭션을 디스크 Home Block으로 재적용하여 빠르게 정합성을 수습하는 과정.

</details>

```text
┌──────────────────────────────┐
│ 파일 시스템 변경           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 트랜잭션 구성           │
│ 2. 변경 레코드 지속화      │
│ 3. 커밋 레코드 지속화      │
└───────┬──────────────────────┘
        ├─ 정상 진행 ───────▶ [4. 체크포인트 반영]
        │
        └─ 장애•재마운트 ────▶ [5. 커밋 트랜잭션 재생 (Replay)]
```

### 동작 원리

1. **트랜잭션 구성**: 파일 생성/수정/삭제 작업을 저널 트랜잭션으로 패키징.
2. **변경 레코드 지속화**: 저널 영역에 Inode 및 데이터 갱신 로그(WAL) 기록.
3. **커밋 레코드 지속화**: 트랜잭션 완료 표식인 **Commit Block**을 저널에 디스크 이송.
4. **체크포인트 반영**: 정상 구동 중 체크포인터가 저널 기록을 디스크 **Home Block**으로 실제 물리 기록.
5. **커밋 트랜잭션 재생**: 장애 재부팅 시 Commit Block이 존재하는 저널에 대해 **REDO (Replay)** 수행.

#### 한줄 요약

- 변경 레코드 지속화와 장애 후 커밋 트랜잭션 재생이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Ordered Mode**: ext4의 기본 저널링 모드로, 파일 데이터 블록을 먼저 디스크 Home Block에 쓴 후 관련 메타데이터만을 저널 영역에 커밋하여 성능과 무결성을 균형 제어하는 방식.

</details>

| 저널링 모드 | ext4 저널링 방식 | 동작 매커니즘 | 장단점 및 특징 |
|:---|:---|:---|:---|
| Journal (Full) | 데이터와 메타데이터 저널링 | 본래 블록 반영 전 저널에 함께 기록 | 넓은 보호 범위 / 쓰기량 증가 |
| Ordered | 메타데이터 저널링과 데이터 선기록 | 관련 데이터 후 메타데이터 커밋 | 데이터 노출 완화 / 순서 제약 |
| Writeback | 메타데이터만 저널링 | 데이터와 메타데이터 순서 비보장 | 순서 제약 감소 / 장애 시 이전 데이터 가능 |

#### 한줄 요약

- 보호 범위에 따라 라이트백 모드, 오더드 모드, 저널 모드를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Barrier (Write Barrier)**: 현대 NVMe/SSD 장치의 휘발성 캐시 갱신 재정렬(Reordering)로 인해 저널 커밋 블록보다 Home Block이 먼저 쓰여 정합성이 파괴되는 것을 막는 디스크 동기화 벽.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 저장장치 캐시 재정렬에 따른 순서 붕괴 | **Flush•FUA•Write Barrier** 적용 | 커밋 전후 지속성 순서 확보 |
| 전체 저널링에 따른 쓰기량 증가 | 내구성 요구에 맞춰 **Ordered Mode** 검토 | 보호 범위와 처리량 절충 |
| SSD 장치 상에서 저널링으로 인한 쓰기 수명 차단 | **ext4 noatime / nodiratime** 튜닝 및 nvme 바이어스 인가 | 불필요한 메타 저널링 차단 |

> 사례: Linux ext4 마운트 옵션 `tune2fs -o journal_data_ordered /dev/sda1` 실무 적용

#### 한줄 요약

- 쓰기 순서 장벽, 그룹 커밋, 체크섬 기반 운영이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **저널링 모드 선택 기준(Journaling Mode Selection Criteria)**: 시스템 내구성 목표, I/O 스루풋 타깃 및 디스크 매체(HDD/SSD) 특성에 기반한 튜닝 체계.

</details>

- 일반 메타데이터 보호는 **Ordered**, 데이터까지 보호하면 **Full Journal** 선택

#### 한줄 요약

- 보호 범위•쓰기량•복구 시간에 맞는 정책 선택이 핵심이다.
