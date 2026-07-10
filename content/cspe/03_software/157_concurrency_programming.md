---
title: 동시성 프로그래밍 — 비동기·멀티스레딩 (Concurrency Programming)
date: 2026-07-05
tags: [cspe-software]
weight: 157
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 여러 작업을 동시에 수행하거나 논리적으로 겹쳐서 실행하는 프로그래밍 기법 |
| 필요성 | 응답성 향상, 멀티코어 H/W 자원 활용 극대화 및 I/O 대기 시간 최소화 |
| 출제 의도 | 스레드 vs 프로세스, 동기 vs 비동기, Race Condition 해결 방안 이해 |

## Ⅱ. 구성요소
```text
[ Multi-Threading ]           [ Asynchronous I/O ]
+-------+ +-------+           App ----> Task A (Call & Return)
| T1    | | T2    |             |        | (Background Run)
+-------+ +-------+             +-----> Task B (Continue)
| Shared Memory   |             |        |
+-----------------+             + <---- Callback / Future
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 스레드 | 프로세스 내 실행 흐름, 코드/데이터 공유 | 한 주방의 여러 요리사 |
| 뮤텍스/세마포어 | 공유 자원 접근 제어를 위한 동기화 도구 | 화장실 열쇠 |
| 이벤트 루프 | 단일 스레드에서 여러 비동기 작업을 스케줄링 | 주문 접수 관리자 |
> 요약: 동시성은 작업의 '구조'이고, 병렬성은 작업의 '실제 동시 실행'임.

## Ⅲ. 절차
```text
Task Start -> Thread Spawn / Async Call -> [Context Switch] -> Critical Section
      ^                                          |               |
      +----- Result Join / Callback <------------+---- (Lock) ---+
```
1. 작업 분리: 독립적으로 실행 가능한 단위를 스레드로 생성하거나 비동기 함수 호출.
2. 동기화 설정: 여러 스레드가 동시에 접근하는 영역(Critical Section)에 Lock 적용.
3. 비차단 실행: I/O 요청 등록 후 thread를 대기시키지 않고 상태·future를 반환하며 완료 event를 별도로 처리함.
4. 결과 취합: join·future·callback·channel로 완료와 오류를 동기화함.
> 요약: 동시성 설계는 task의 대기·취소·오류·공유 상태 접근 순서를 synchronization과 message passing으로 통제함.

## Ⅳ. 문제점
- 두 개 이상의 스레드가 서로의 자원을 기다리며 멈추는 데드락(Deadlock) 위험.
- 잦은 컨텍스트 스위칭으로 인한 오버헤드가 실제 연산량보다 커지는 역효과.

## Ⅴ. 개선방안
- 락 프리(Lock-free) 자료구조 및 원자적 연산(Atomic)을 사용하여 경쟁 최소화.
- 불변 객체(Immutable Object) 사용을 통해 근본적으로 경합 조건(Race Condition) 제거.

## Ⅵ. 전망
- 구조적 동시성(Structured Concurrency): 자식 스레드의 수명을 부모와 묶어 안전성 강화.
- 가상 스레드(Project Loom): 커널 스레드보다 가벼운 수만 개의 스레드를 운용하는 기술 확산.
