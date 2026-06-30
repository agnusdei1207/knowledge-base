---
title: "임계구역 (Critical Section)"
date: "2026-06-30"
weight: 38
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 공유자원에 접근하는 코드 영역으로, 한 시점에 하나의 프로세스만 실행되도록 보장되어야 하는 구간.

## Ⅱ. 구성요소 / 원리
- 진입구역(Entry Section): 임계구역 진입 허가 요청
- 임계구역(Critical Section): 공유자원 접근·조작
- 퇴출구역(Exit Section): 진입 해제 통지
- 잔여구역(Remainder Section): 그 외 코드
- 3대 요건 충족이 올바른 해법의 조건

## Ⅲ. 흐름도 / 구조
```text
do {
   [Entry Section]   ← 진입 허가 획득
   [Critical Section]← 공유자원 접근
   [Exit Section]    ← 진입 해제
   [Remainder]
} while (true);
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 공유자원의 상호배제적 접근 보장 |
| 장점 | 데이터 일관성 확보, 경쟁조건 방지 |
| 한계 | 잘못 설계 시 교착(Deadlock)·기아(Starvation) 유발 |

## Ⅴ. 기술사적 적용
- 3대 요건: ①상호배제(Mutual Exclusion) ②진행(Progress) ③한정대기(Bounded Waiting)
- SW해법(Peterson) → HW해법(TAS/CAS) → OS해법(Semaphore/Monitor)로 발전
- 멀티코어 성능 위해 임계구역 최소화(Lock Granularity 조정)
