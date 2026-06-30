---
title: "연속할당 (Contiguous Allocation, First/Best/Worst-Fit)"
date: "2026-06-30"
weight: 55
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 연속할당(Contiguous Allocation)은 각 프로세스를 메모리의 하나의 연속된 공간에 적재하는 방식으로, 가용 공간(Hole) 중 어디에 배치할지를 배치 알고리즘으로 결정한다.

## Ⅱ. 구성요소 / 원리
- 최초적합(First-Fit): 충분히 큰 첫 번째 가용공간에 할당, 탐색 빠름
- 최적적합(Best-Fit): 가장 작은 적합 공간에 할당, 작은 잔여 조각 다수 발생
- 최악적합(Worst-Fit): 가장 큰 공간에 할당, 잔여 공간 재활용 의도
- 가용공간 리스트(Free List)와 배치 정책으로 외부단편화 영향 결정

## Ⅲ. 흐름도 / 구조
```text
요청크기 ──▶ [가용공간 리스트 탐색]
              ├ First-Fit : 첫 적합 hole
              ├ Best-Fit  : 최소 적합 hole
              └ Worst-Fit : 최대 hole
            ──▶ 할당 후 잔여 hole 갱신
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 프로세스를 단일 연속영역에 효율 배치 |
| 장점 | 구조 단순, 주소변환 간단(base+limit) |
| 한계 | 외부단편화 발생, First/Best-Fit가 일반적 우수 |

## Ⅴ. 기술사적 적용
- First-Fit·Best-Fit는 평균적으로 Worst-Fit보다 공간/속도 효율 우수(50% 규칙)
- 외부단편화 한계로 압축(Compaction) 또는 페이징/세그멘테이션으로 발전
