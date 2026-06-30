---
title: "뮤텍스 (Mutex)"
date: "2026-06-30"
weight: 41
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 상호배제(Mutual Exclusion)를 위한 이진 락(Binary Lock) 객체로, 잠근 주체만이 해제할 수 있는 소유권(Ownership) 개념을 가진 동기화 도구.

## Ⅱ. 구성요소 / 원리
- 상태: locked / unlocked 두 가지
- 연산: lock(획득), unlock(반납) — 원자적 수행
- 소유권: lock한 스레드만 unlock 가능
- 대기방식: 차단(Blocking) → 대기큐 진입, 문맥교환 발생
- 일반적으로 TAS/CAS 위에 OS 대기큐를 결합해 구현

## Ⅲ. 흐름도 / 구조
```text
Thread A: lock(m) ──► [임계구역] ──► unlock(m)
Thread B: lock(m) ──► (B blocked, 대기큐) ──┐
                                            ▼
                       A unlock 후 B 깨어나 획득
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 단일 자원에 대한 배타적 접근 보장 |
| 장점 | 소유권으로 안전, 대기 시 CPU 비점유(Blocking) |
| 한계 | 문맥교환 비용, 우선순위 역전·교착 가능 |

## Ⅴ. 기술사적 적용
- 비교: Mutex(소유권 O, 이진) vs Semaphore(소유권 X, 카운팅 가능)
- 짧은 임계구역엔 Spinlock, 긴 구역엔 Mutex 선택
- 우선순위 역전 대비 우선순위 상속(Priority Inheritance) Mutex 사용
