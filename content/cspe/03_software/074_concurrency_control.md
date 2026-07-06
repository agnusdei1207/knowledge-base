---
title: 동시성 제어 — 락킹·타임스탬프 (Concurrency Control)
date: 2026-07-05
tags: [cspe-software]
weight: 74
---

## Ⅰ. 개요
- 다중 사용자 환경에서 트랜잭션들이 DB 일관성을 해치지 않고 동시에 실행되게 제어하는 기법임.
- 데이터 손실, 갱신 손실 등 병행 실행 시의 부작용을 방지하는 것이 목적임.
- 출제 의도: 직렬 가능성(Serializability) 보장을 위한 주요 알고리즘 비교 분석.

## Ⅱ. 구성요소
- 제어 기법 분류
[Pessimistic: Locking] | [Optimistic: Timestamp]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Locking | 트랜잭션이 접근할 데이터에 잠금을 설정함 | 화장실 문 잠금 |
| Timestamp | 각 Tx에 고유 시간을 부여하여 순서 결정함 | 대기표 발행 |
| 2PL (2-Phase Locking) | 확장(Lock)과 수축(Unlock) 단계로 구분 제어 | 예약 후 퇴실 시 반납 |
> 요약: 락킹은 충돌 방지 중심, 타임스탬프는 충돌 감지 중심임.

## Ⅲ. 절차
- 2단계 로킹 (2PL) 프로토콜
[Start] -> (Growing Phase) -> [Lock Point] -> (Shrinking Phase) -> [End]

1. 확장 단계: 필요한 모든 Lock을 획득하며, Unlock은 하지 않음.
2. 검사 단계: 모든 자원을 점유한 상태에서 트랜잭션 연산 수행함.
3. 수축 단계: 획득한 Lock을 순차적으로 해제하며, 새로운 Lock은 불가함.
4. 완료: 모든 자원을 반납하고 트랜잭션 종료함.
> 요약: Lock의 획득과 해제 시점을 분리하여 직렬 가능성을 보장함.

## Ⅳ. 문제점
- Locking 방식의 고질적인 교착상태(Deadlock) 및 Cascading Rollback 문제.

## Ⅴ. 개선방안
- Deadlock Detection 및 Timeout 설정, 낙관적 검증(Validation) 기법 병행.

## Ⅵ. 전망
- 락 프리(Lock-free) 알고리즘 및 하드웨어 트랜잭션 메모리(HTM) 적용 확대.
- 분산 환경에서의 글로벌 타임스탬프 관리를 위한 원자 시계 활용 기술 도입.
