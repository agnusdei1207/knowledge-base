---
title: MVCC 다중 버전 동시성 제어 (Multi-Version Concurrency Control)
date: 2026-07-05
tags: [cspe-software]
weight: 75
---

## Ⅰ. 개요
- 데이터의 여러 버전을 관리하여 읽기 작업과 쓰기 작업이 서로 방해하지 않게 하는 기법임.
- 쓰기 작업 중에도 읽기 작업은 기존 버전을 참조함으로써 동시성을 극대화함.
- 출제 의도: Undo 로그 및 스냅샷을 활용한 락 프리(Lock-free) 읽기 메커니즘 이해.

## Ⅱ. 구성요소
- MVCC 구조
[Current Data] <--- [Pointer] --- [Old Version (Undo Log)]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Undo Log | 변경 전 데이터를 저장하는 공간 | 과거 기록 보관소 |
| System Change No (SCN) | 데이터의 변경 시점을 나타내는 버전 번호 | 문서 수정 차수 |
| Snapshot | 특정 시점의 데이터 일관된 상태 | 카메라 사진 촬영 |
> 요약: 데이터 변경 시 원본 대신 복사본을 생성하여 병행 처리를 지원함.

## Ⅲ. 절차
- MVCC 데이터 읽기 과정
[Read Request] -> [Check SCN] -> [Compare with Undo] -> [Result]

1. 요청 수신: 읽기 트랜잭션의 시작 SCN을 확인함.
2. 버전 비교: 데이터 블록의 SCN과 트랜잭션 SCN을 대조함.
3. Undo 참조: 블록 SCN이 크면(최신이면) Undo 로그를 추적하여 과거 버전 찾음.
4. 데이터 반환: 트랜잭션 시작 시점에 유효했던 버전을 조립하여 반환함.
> 요약: 자신의 시점에 맞는 버전을 찾아 읽음으로써 Lock 없이 일관성 유지함.

## Ⅳ. 문제점
- 다중 버전 유지에 따른 저장 공간(Undo 영역) 압축 및 Garbage Collection 부하.

## Ⅴ. 개선방안
- 주기적 진공(Vacuum) 작업 수행 및 Undo Retention 파라미터 최적화.

## Ⅵ. 전망
- 스토리지 계층의 스냅샷 기능을 활용한 하드웨어 가속 MVCC 기술 발전.
- 타임 트래블 쿼리(Time Travel Query) 등 과거 이력 조회 기능과 연계 강화.
