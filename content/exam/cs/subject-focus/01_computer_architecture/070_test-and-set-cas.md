---
title: "Test-and-Set·CAS (Test-and-Set / Compare-And-Swap 원자적 연산)"
date: "2026-06-30"
weight: 70
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 락·동기화를 위한 하드웨어 원자적(atomic) 명령으로, 값을 설정하며 이전값을 반환하는 Test-and-Set과 기대값 일치 시 교체하는 Compare-And-Swap(CAS).

## Ⅱ. 구성요소 / 원리
- Test-and-Set(TAS): 메모리를 1로 설정하고 이전값 반환, 0이면 락 획득
- Compare-And-Swap(CAS): (주소, 기대값, 새값) — 현재값=기대값이면 교체·성공
- 읽기-수정-쓰기를 인터럽트 없이 원자적 수행
- 락프리(Lock-free) 자료구조의 기본 연산

## Ⅲ. 흐름도 / 구조
```text
[TAS]  old=lock; lock=1; if(old==0) 임계영역; else 재시도
[CAS]  if(*p==expected){ *p=new; return true } else false
        실패 시 루프 재시도(retry loop)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 다중 스레드 상호배제·원자적 갱신 보장 |
| 장점 | 락 구현·락프리 알고리즘 기반, 효율적 동기화 |
| 한계 | 경쟁 심하면 스핀·재시도 비용, CAS는 ABA 문제 |

## Ⅴ. 기술사적 적용
- x86 LOCK CMPXCHG, ARM LL/SC(LDREX/STREX)로 구현
- 스핀락·뮤텍스·세마포어 하부, 원자적 카운터
- ABA 대응: 버전 태그·LL/SC, 메모리 배리어와 결합
