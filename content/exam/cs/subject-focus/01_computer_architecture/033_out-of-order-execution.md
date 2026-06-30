---
title: "비순차실행 (OoO, Out-of-Order Execution)"
date: "2026-06-30"
weight: 33
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 프로그램 순서와 무관하게 피연산자가 준비된 명령부터 먼저 실행하고, 완료(Commit)는 순서대로 처리하여 ILP를 높이는 실행 방식이다.

## Ⅱ. 구성요소 / 원리
- 인출·발행은 순차, 실행은 비순차, 완료(Retire)는 다시 순차
- 예약국(Reservation Station): 피연산자 대기·준비 시 발행
- 레지스터 리네이밍: WAR/WAW 가짜 의존성 제거
- ROB(Reorder Buffer): 결과 임시 보관 후 순서대로 커밋
- 정확한 예외(Precise Exception) 보장

## Ⅲ. 흐름도 / 구조
```text
In-order ─▶ Issue ─▶ [Reservation Station] ─▶ Out-of-order Execute
                                                   │
                                          [ROB] ─▶ In-order Commit
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 의존·지연 명령 대기 중 독립 명령 선실행 |
| 장점 | 스톨 은닉, ILP·IPC 향상 |
| 한계 | 리네이밍·ROB 등 하드웨어 복잡, 전력 증가 |

## Ⅴ. 기술사적 적용
- 토마술로 알고리즘이 OoO의 이론적 기반(예약국+CDB)
- 슈퍼스칼라와 결합해 현대 고성능 CPU의 표준 마이크로아키텍처
