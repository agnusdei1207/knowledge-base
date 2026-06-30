---
title: "스핀락 (Spinlock)"
date: "2026-06-30"
weight: 42
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 락 획득 실패 시 차단되지 않고 루프를 돌며 반복 시도하는 바쁜대기(Busy Waiting) 기반 락으로, 짧은 임계구역과 멀티코어 환경에 적합.

## Ⅱ. 구성요소 / 원리
- 원자명령(TAS/CAS)으로 락 변수 반복 검사
- Busy Waiting: 대기 중 CPU를 점유한 채 회전(Spin)
- 문맥교환 없음 → 짧은 대기엔 저비용
- 단일코어에선 무의미(대기 시 락 소유자가 진행 못 함)
- 캐시 경합 완화: TTAS(Test-Test-And-Set), 백오프(Backoff)

## Ⅲ. 흐름도 / 구조
```text
while (TestAndSet(&lock) == true)
      ;   // CPU 점유한 채 회전(Spin)
   [Critical Section]  (매우 짧아야 함)
lock = false;          // 해제
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 멀티코어 짧은 임계구역의 저지연 동기화 |
| 장점 | 문맥교환 無, 빠른 락 획득, 커널 내부 적합 |
| 한계 | Busy Waiting로 CPU 낭비, 긴 구역·단일코어 부적합 |

## Ⅴ. 기술사적 적용
- 비교: Spinlock(Busy Wait) vs Mutex(Blocking)
- 적응형(Adaptive) Mutex: 짧으면 spin, 길면 sleep로 전환
- 리눅스 커널 인터럽트 핸들러 등 sleep 불가 영역에 활용
