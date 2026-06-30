---
title: "우선순위 역전·상속 (Priority Inversion/Inheritance)"
date: "2026-06-30"
weight: 48
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 저우선순위 작업이 점유한 락을 고우선순위 작업이 기다리는 사이, 중간 우선순위 작업이 끼어들어 고우선순위가 지연되는 현상과 그 해결 프로토콜.

## Ⅱ. 구성요소 / 원리
- 발생: 고(H)가 저(L) 보유 락 대기, 중(M)이 L을 선점하여 H 무한 지연
- 무한 역전(Unbounded Inversion): M의 실행으로 H 지연 누적
- 우선순위 상속(Priority Inheritance): L이 H의 우선순위를 일시 승계
- 우선순위 천장(Priority Ceiling): 락에 사용 가능한 최고 우선순위 부여
- 실시간(RTOS)·임무 시스템에서 치명적

## Ⅲ. 흐름도 / 구조
```text
[역전]  L:lock──► H:대기 ··· M 선점실행 ··· (H 무한 지연)
[상속]  L:lock(우선순위↑=H) ──► 빠르게 unlock ──► H 진행
              (M는 끼어들지 못함)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 실시간 시스템의 우선순위 보장·시한(Deadline) 준수 |
| 장점 | 상속/천장으로 무한 역전 차단, 예측가능성 확보 |
| 한계 | 상속 추적 오버헤드, 천장은 사전 우선순위 분석 필요 |

## Ⅴ. 기술사적 적용
- 사례: 1997 화성탐사선 Pathfinder 리셋 → 우선순위 상속으로 해결
- 비교: 상속(동적, 보유 즉시 발동) vs 천장(정적, 락 선점 시 즉시 상향)
- 적용: VxWorks/RTLinux의 PI Mutex(pthread PRIO_INHERIT)
