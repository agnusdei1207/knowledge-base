---
title: "Peterson 알고리즘 (Peterson's Algorithm)"
date: "2026-06-30"
weight: 39
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 두 프로세스 간 상호배제를 보장하는 소프트웨어 기법으로, 의사표시 변수 flag와 양보 변수 turn을 조합해 임계구역 3대 요건을 모두 만족.

## Ⅱ. 구성요소 / 원리
- flag[i]: 프로세스 i가 진입을 원함을 표시(Boolean)
- turn: 충돌 시 양보할 차례를 지정
- 진입조건: 상대가 원하지 않거나(`!flag[j]`) 내 차례(`turn==i`)일 때 진입
- 바쁜대기(Busy Waiting) 기반 → 두 프로세스에 한정
- 별도 HW 명령 불필요(순수 SW)

## Ⅲ. 흐름도 / 구조
```text
// 프로세스 i
flag[i] = true;          // 진입 의사
turn    = j;             // 상대에게 양보
while (flag[j] && turn==j)
        ;                // 대기(Busy Wait)
   [Critical Section]
flag[i] = false;         // 퇴출
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | HW 지원 없는 2프로세스 상호배제 |
| 장점 | 상호배제·진행·한정대기 3요건 모두 충족 |
| 한계 | 2프로세스 한정, Busy Waiting, 명령 재배열(Reordering)에 취약 |

## Ⅴ. 기술사적 적용
- N프로세스 확장: Bakery 알고리즘(Lamport)
- 현대 CPU의 Out-of-Order 실행에선 메모리 배리어(Memory Barrier) 필요
- 교육·이론적 의의 큼, 실무는 HW 원자명령(TAS/CAS) 사용
