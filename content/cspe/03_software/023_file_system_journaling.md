---
title: "저널링 (File System Journaling)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 23
---

## Ⅰ. 개요
- **정의**: 파일 시스템 변경 사항을 별도 로그 영역에 기록하여 장애 시 복구를 보장하는 기법임
- **배경/필요성**: 쓰기 도중 비정상 종료 시 메타데이터와 데이터 간 불일치가 발생하므로 복구 수단이 필요함 (022 참조)
- **비유**: 은행 거래 시 장부(저널)에 먼저 기록한 뒤 실제 금고(디스크)를 갱신하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 저널링 모드별 차이와 복구 원리 | Write-Ahead Log 원리·3가지 모드 | fsck 전수 검사와 저널 복구를 혼동하지 않을 것 |

> 요약: WAL 기반으로 파일 시스템 정합성을 보장하는 기법임

## Ⅱ. 구성요소
```text
File System Area
  +-- Journal Area (Log)
  |     +-- Transaction Record
  |     +-- Commit Block
  +-- Metadata Area (inode/bitmap)
  +-- Data Block Area
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Journal Area | 변경 예정 내용을 순차 기록하는 전용 로그 영역 | 은행 거래 장부 |
| Transaction Record | 하나의 논리적 변경 단위를 묶은 로그 항목 | 장부의 한 줄 기록 |
| Commit Block | 트랜잭션 완료를 표시하는 마커 | 장부에 찍는 확인 도장 |

> 요약: 별도 Journal 영역에 트랜잭션 단위로 변경 이력을 기록함

## Ⅲ. 절차
```text
Journal Write -> Journal Commit -> Checkpoint -> Journal 해제
```
- 1단계: 변경할 메타데이터(+데이터)를 Journal Area에 순차 기록함
- 2단계: Commit Block을 기록하여 트랜잭션 완료를 확정함
- 3단계: Journal 내용을 실제 파일 시스템 영역(Metadata/Data Block)에 반영(Checkpoint)함
- 4단계: 반영 완료 후 해당 Journal 공간을 해제하여 재사용함

> 요약: 로그 선기록 후 실제 영역 반영의 2단계 쓰기로 정합성을 유지함

## Ⅳ. 문제점
- 이중 쓰기 오버헤드: 동일 데이터를 Journal과 본 영역에 두 번 기록하여 쓰기량이 증가함
- Journal 영역 병목: 모든 트랜잭션이 단일 Journal을 순차 사용하여 동시 쓰기 처리량이 제한됨
- Data 모드 성능 저하: Ordered/Writeback 모드 대비 Data 모드는 데이터까지 로깅하여 처리량이 감소함

> 요약: 이중 쓰기·단일 Journal 병목·모드별 성능 차이가 주요 문제임

## Ⅴ. 개선방안
1. 단기: Ordered 모드 채택으로 메타데이터만 로깅하여 이중 쓰기량 감소
2. 중기: 다중 Journal 영역 분할 또는 병렬 로깅으로 동시 쓰기 처리량 확대
3. 장기: CoW(Copy-on-Write) 파일 시스템(Btrfs·ZFS)으로 전환하여 별도 Journal 자체를 제거

> 요약: 로깅 범위 축소·병렬화·CoW 전환으로 오버헤드를 해소함

## Ⅵ. 전망
- 발전 방향: NVMe 저지연 매체에서 Journal 오버헤드 비율이 커져 CoW·로그 구조 파일 시스템이 부상함
- 기술사적 판단: 데이터 안전성과 쓰기 성능 간 트레이드오프를 워크로드별로 판단할 필요가 있음
- 기술사 제언: 미션 크리티컬 시스템은 Data 모드, 범용 서버는 Ordered 모드 적용을 권장함
