---
title: "모니터·조건변수 (Monitor / Condition Variable)"
date: "2026-06-30"
weight: 44
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 공유데이터와 그에 대한 연산을 캡슐화해 한 시점에 하나의 스레드만 내부에 진입하도록 자동 상호배제를 보장하는 고수준(High-level) 동기화 구조.

## Ⅱ. 구성요소 / 원리
- 캡슐화: 공유변수 + 프로시저를 하나의 모듈로 보호
- 자동 상호배제: 모니터 진입 자체가 락 획득(언어/런타임 보장)
- 조건변수(Condition Variable): wait(대기·락 해제), signal(대기자 깨움)
- 진입큐 + 조건큐로 대기 관리
- signal 의미론: Hoare(즉시양도) vs Mesa(재검사 필요)

## Ⅲ. 흐름도 / 구조
```text
monitor M {
  condition c;
  proc P(){
     while(!조건) c.wait();   // 락 풀고 대기(Mesa: while)
     ... 임계작업 ...
     c.signal();             // 대기자 깨움
  }
}  // 진입=자동 락, 종료=자동 해제
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 동기화 오류 감소를 위한 고수준 추상화 |
| 장점 | 자동 상호배제, 캡슐화로 안전·가독성 향상 |
| 한계 | 언어/런타임 지원 필요, signal 의미론 주의 |

## Ⅴ. 기술사적 적용
- Hoare(signal 즉시 제어 양도) vs Mesa(깨운 후 재경쟁, while로 재검사)
- 구현: Java synchronized + wait/notify, POSIX 조건변수(pthread_cond)
- 세마포어 대비 오용 가능성 낮아 실무 동기화 표준
