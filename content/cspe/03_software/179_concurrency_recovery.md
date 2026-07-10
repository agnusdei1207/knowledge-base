---
title: 병행 제어 및 회복 기법 (Concurrency and Recovery)
date: 2026-07-05
tags: ["cspe-software"]
weight: 179
---

## Ⅰ. 개요
- 정의: 다수 사용자의 동시 접근 시 데이터 일관성을 유지(병행 제어)하고 장애 시 원복(회복)하는 기법
- 배경: 동시 실행 충돌과 장애 이후 미완료 트랜잭션으로 인한 데이터 불일치 방지
| 구분 | 내용 |
|------|------|
| 출제 의도 | Locking, MVCC, 2PL(병행 제어)과 Log, Checkpoint(회복)의 메커니즘 파악 |

## Ⅱ. 구성요소
  [ Transaction A ] <---(Conflict)---> [ Transaction B ]
  [ Failure ] --(Redo/Undo)--> [ Consistent State ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Locking | 자원 점유를 통해 타 트랜잭션 접근 차단 | 화장실 잠금 |
| MVCC | 데이터의 버전 관리를 통해 읽기/쓰기 동시 허용 | 복사본 작업 |
| Logging | 변경 전후 내용을 기록(WAL)하여 복구에 사용 | 항해 일지 |
> 요약: 락·버전으로 동시 실행을 제어하고 로그로 장애 전후 상태를 복구함

## Ⅲ. 절차
  Start -> Lock/Version -> Commit/Log -> Checkpoint
1. Isolation Management: 락 획득 또는 스냅샷 생성으로 격리성 확보
2. Execution: 버퍼 내 데이터 변경 및 로그 버퍼 기록
3. Commit/Flush: 로그를 물리 디스크에 기록(WAL) 후 완료
4. Recovery: 장애 시 로그 기반 Redo(재실행) 및 Undo(취소)
> 요약: 락 또는 스냅샷으로 격리성을 유지하고 WAL의 Redo·Undo로 원자성을 복구함

## Ⅳ. 문제점
- 과도한 락킹으로 인한 교착 상태(Deadlock) 및 처리량 저하
- 로그 증가에 따른 복구 시간(RTO) 지연 및 스토리지 부하

## Ⅴ. 개선방안
- MVCC 기반 Non-blocking 읽기 적용 및 락 단위 세분화
- 증분 체크포인트(Incremental Checkpoint) 도입으로 복구 범위 축소

## Ⅵ. 전망
- 하드웨어 트랜잭션 메모리(HTM)와 타임스탬프 기반 분산 병행 제어 적용 확대
