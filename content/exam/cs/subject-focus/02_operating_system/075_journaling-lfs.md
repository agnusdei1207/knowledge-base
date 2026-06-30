---
title: "저널링·LFS·COW 파일시스템 (Journaling/LFS/COW FS)"
date: "2026-06-30"
weight: 75
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 시스템 크래시 시 파일시스템 일관성(Crash Consistency)을 보장하기 위한 기법으로, 저널링(Journaling)·로그구조(LFS, Log-structured)·쓰기시복제(COW, Copy-on-Write) 방식이 있다.

## Ⅱ. 구성요소 / 원리
- 저널링(WAL, Write-Ahead Logging): 변경을 저널에 먼저 기록 후 본영역 반영, 크래시 시 재실행/롤백
- 메타데이터 저널링 vs 전체 저널링: 보호범위와 성능의 트레이드오프
- LFS(Log-structured FS): 모든 쓰기를 로그에 순차 추가, 임의쓰기를 순차쓰기로 전환
- COW(Copy-on-Write): 기존 블록을 덮어쓰지 않고 새 블록에 쓴 뒤 포인터 전환
- 스냅샷(Snapshot): COW 기반으로 특정 시점 일관 상태 보존

## Ⅲ. 흐름도 / 구조
```text
저널링: 변경 → [저널 기록(WAL)] → 본영역 반영 → 저널 정리
           크래시 시: 저널 재실행으로 복구
LFS   : 쓰기 → [로그 끝에 순차 append] → GC로 공간 회수
COW   : 변경 → [새 블록에 기록] → 포인터 원자적 전환(원본 보존)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 크래시 후 fsck 없이 빠른 복구와 일관성 보장 |
| 장점 | 저널=빠른 복구, LFS=순차쓰기 성능, COW=원자성·스냅샷 |
| 한계 | 저널=이중쓰기 오버헤드, LFS=GC 비용, COW=단편화·쓰기증폭 |

방식 비교

| 방식 | 일관성 기법 | 대표 FS |
|:---|:---|:---|
| 저널링 | WAL 로그 | ext3/4, NTFS |
| LFS | 순차 로그 | F2FS, NILFS |
| COW | 블록 복제 | ZFS, Btrfs |

## Ⅴ. 기술사적 적용
- 플래시(SSD) 친화적 순차쓰기 위해 F2FS 등 LFS 채택
- ZFS/Btrfs는 COW로 스냅샷·체크섬 기반 데이터 무결성 제공
- 저널링 모드(ordered/writeback/journal) 선택으로 성능·안전 균형
