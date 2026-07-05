---
title: "WAL (Write-Ahead Log)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 121
---

## Ⅰ. 개요
- **정의**: 변경 데이터를 디스크 반영 전에 로그에 먼저 기록하는 복구 기법
- **배경/필요성**: 트랜잭션 도중 장애 발생 시 커밋 여부를 판단할 근거가 없으면 데이터 정합성을 보장할 수 없음
- **비유**: 계약서 원본을 수정하기 전에 변경 이력을 별도 공증 문서에 먼저 남기는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 장애 복구 원리 이해 | Log-Force-at-Commit, Steal/No-Force 정책 | REDO/UNDO 구분 누락 주의 |

> 요약: 로그 선행 기록으로 트랜잭션 원자성과 지속성을 보장하는 기법임

## Ⅱ. 구성요소
```text
Transaction --> WAL Buffer --> WAL File --> Checkpoint --> Data File
                (메모리)       (디스크)      (동기화)       (디스크)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| WAL Buffer | 로그 레코드를 메모리에 임시 보관하는 버퍼 | 메모장 임시 메모 |
| WAL File | fsync로 디스크에 영속 기록된 로그 파일 | 공증 완료된 문서 |
| LSN | 로그 레코드의 순서를 식별하는 고유 번호 | 문서 일련번호 |
| Checkpoint | WAL과 데이터 파일 간 동기 시점을 기록하는 메커니즘 | 중간 저장 지점 |

> 요약: WAL Buffer-File-Checkpoint 구조로 로그 선행 기록과 주기적 동기화를 수행함

## Ⅲ. 절차
```text
BEGIN TX --> Write WAL Buffer --> Flush WAL to Disk --> Commit/Abort
                                       |
                                  Checkpoint ---> Data File Sync
```
- 1단계: 트랜잭션 시작 시 변경 전/후 값을 WAL Buffer에 기록함
- 2단계: 커밋 요청 시 WAL Buffer를 디스크의 WAL File로 fsync 수행함
- 3단계: WAL File 기록 성공 후 클라이언트에 커밋 완료 응답함
- 4단계: Checkpoint 시점에 Dirty Page를 데이터 파일에 일괄 반영함

> 요약: 로그 디스크 기록 완료 후 커밋 응답, 이후 Checkpoint에서 데이터 파일 동기화함

## Ⅳ. 문제점
- WAL 파일 비대화: 장기 운영 시 로그 누적으로 디스크 공간 부족 발생
- Checkpoint 지연: Dirty Page 과다 시 I/O 폭증으로 서비스 응답 지연 유발
- 복구 시간 증가: Checkpoint 간격이 길면 REDO 재생 구간이 확대되어 복구 시간 증가

> 요약: 로그 누적, Checkpoint I/O 부하, 복구 시간 증가가 주요 문제임

## Ⅴ. 개선방안
1. 단기: WAL 아카이빙 및 세그먼트 순환 삭제로 디스크 사용량 관리
2. 중기: 점진적 Checkpoint(Fuzzy Checkpoint) 도입으로 I/O 분산 처리
3. 장기: 병렬 REDO 복구 및 WAL 압축 적용으로 복구 시간 단축

> 요약: 세그먼트 관리, Fuzzy Checkpoint, 병렬 복구로 WAL 운영 효율을 개선함

## Ⅵ. 전망
- 발전 방향: NVMe·영속 메모리(PMEM) 환경에서 WAL 오버헤드 최소화 연구 진행 중
- 기술사적 판단: DBMS 핵심 복구 메커니즘으로 ACID 보장의 기반 기술에 해당함
- 기술사 제언: WAL 정책(Steal/No-Force)과 Checkpoint 전략을 워크로드 특성에 맞게 튜닝할 필요
