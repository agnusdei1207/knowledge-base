---
title: "페이지교체 (Page Replacement: OPT·LRU·클럭)"
date: "2026-06-30"
weight: 54
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 페이지 폴트 시 빈 프레임이 없을 때 메모리에서 축출할 희생 페이지(victim)를 선택하는 알고리즘으로, 페이지 폴트율 최소화가 목표.

## Ⅱ. 구성요소 / 원리
- OPT(Optimal/Belady): 미래 최장기간 미사용 페이지 축출, 이론적 하한
- LRU(Least Recently Used): 가장 오래전 참조 페이지 축출, 지역성 활용
- FIFO: 적재 순서대로 축출(Belady 변칙 발생)
- 클럭(Clock/Second-Chance): 참조비트로 LRU 근사, 원형 포인터 순회
- NUR/Aging: 참조·변경 비트 조합 근사

## Ⅲ. 흐름도 / 구조
```text
Clock(2차 기회):
  포인터 → R=0 ? ─yes→ 축출
                 └no → R=0 설정 후 다음 칸 이동(한 번 더 기회)
  ○→○→○→○ (원형) 반복
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 페이지 폴트율 최소화로 가상메모리 성능 확보 |
| 장점 | OPT=최적 기준, LRU=현실 우수, 클럭=저비용 LRU 근사 |
| 한계 | OPT 구현 불가(미래), LRU 비용↑, FIFO 변칙 |

## Ⅴ. 기술사적 적용
- 비교: Belady 변칙(FIFO에서 프레임↑인데 폴트↑) 회피 위해 스택 알고리즘
- 실무: Linux는 LRU 근사 2-list(active/inactive) + 클럭
- 최신: WSClock, ML 기반 페이지 수명 예측
