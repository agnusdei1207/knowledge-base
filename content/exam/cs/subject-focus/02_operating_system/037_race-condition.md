---
title: "경쟁조건 (Race Condition)"
date: "2026-06-30"
weight: 37
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 둘 이상의 프로세스/스레드가 공유자원(Shared Resource)에 동시 접근하여, 실행 순서(Timing)에 따라 결과가 달라지는 비결정적(Non-deterministic) 상태.

## Ⅱ. 구성요소 / 원리
- 공유자원: 전역변수, 파일, 메모리 등 동시 접근 대상
- 비원자적(Non-atomic) 연산: read-modify-write가 여러 기계어로 분리 실행
- 인터리빙(Interleaving): 문맥교환(Context Switch) 시점에 따라 연산이 교차
- 비결정성: 동일 입력에도 실행마다 다른 결과 발생
- 근본원인: 상호배제(Mutual Exclusion) 미보장

## Ⅲ. 흐름도 / 구조
```text
[공유변수 count=5]
 T1: load count(5) ─┐          (선점)
 T2:                ├─ load count(5) → +1 → store(6)
 T1: +1 → store(6) ─┘
 결과 = 6  (기대값 7, Lost Update)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 동시성 환경에서 데이터 정합성 위협 요인 식별 |
| 장점 | 임계구역/동기화 기법 도입의 근거 제공 |
| 한계 | 비결정적이라 재현·디버깅 곤란(Heisenbug) |

## Ⅴ. 기술사적 적용
- 해결: 임계구역(Critical Section) 보호 → Mutex/Semaphore/Monitor 적용
- 멀티코어·MSA 환경에서 분산락(Distributed Lock)으로 확장 적용
- 정적분석·TSan(Thread Sanitizer)로 사전 탐지
