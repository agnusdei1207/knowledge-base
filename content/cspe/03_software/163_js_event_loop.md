---
title: 자바스크립트 이벤트 루프 및 비동기 (JS Event Loop)
date: 2026-07-05
tags: ["cspe-software"]
weight: 163
---

## Ⅰ. 개요
- 정의: JS 실행 시 호출 스택을 감시하고 Task Queue의 작업을 처리하는 단일 쓰레드 기반 관리자
- 배경: 브라우저 환경의 비차단(Non-blocking) I/O 및 사용자 경험(UX) 최적화 필요
| 구분 | 내용 |
|------|------|
| 출제 의도 | Call Stack, Microtask Queue, Macrotask Queue 간의 우선순위와 실행 순서 명확화 |

## Ⅱ. 구성요소
  [ Call Stack ] <- [ Event Loop ] <- [ Task Queues ]
  (Main Thread)                         (Web APIs)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Call Stack | 현재 실행 중인 함수 프레임 저장소 | 책상 위 서류 |
| Microtask | Promise 등 우선순위가 높은 비동기 작업 | 급행 열차 |
| Macrotask | setTimeout, I/O 등 일반 비동기 작업 | 완행 열차 |
> 요약: 단일 쓰레드의 효율을 극대화하는 비동기 작업 스케줄링 시스템

## Ⅲ. 절차
  Execute Stack -> Microtask Flush -> Render -> Macrotask
1. Stack Clear: 현재 실행 중인 동기 코드를 모두 처리
2. Microtask Run: 큐가 빌 때까지 모든 Microtask 연속 실행
3. UI Render: 브라우저 화면 갱신 필요 시 렌더링 수행
4. Macrotask Run: Macrotask Queue에서 하나를 꺼내 Stack 이동
> 요약: 우선순위 기반 큐 처리를 통한 중단 없는 인터랙션 구현

## Ⅳ. 문제점
- 오래 걸리는 동기 작업 실행 시 메인 쓰레드 차단(Blocking)
- 비동기 콜백 지옥(Callback Hell) 및 실행 순서 예측 난해함

## Ⅴ. 개선방안
- Web Worker 활용으로 무거운 연산을 백그라운드 쓰레드로 분리
- Async/Await 및 제네레이터 도입으로 코드 가독성 및 흐름 제어 개선

## Ⅵ. 전망
- Edge Runtime 및 Node.js Worker Threads의 결합으로 서버/클라이언트 통합 비동기 아키텍처 진화
