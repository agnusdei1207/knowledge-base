---
title: "캐시미스 3C (Compulsory·Capacity·Conflict Miss)"
date: "2026-06-30"
weight: 44
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 캐시 실패(Miss)를 발생 원인에 따라 강제(Compulsory)·용량(Capacity)·충돌(Conflict) 세 유형으로 분류한 모델로, 최적화 방향 도출에 활용.

## Ⅱ. 구성요소 / 원리
- 강제(Compulsory/Cold): 최초 참조 시 불가피한 미스(콜드 스타트)
- 용량(Capacity): 작업집합 > 캐시 용량으로 블록 축출 후 재참조 미스
- 충돌(Conflict/Collision): 같은 집합 경쟁으로 발생(완전연관에선 없음)
- 대응: 강제→프리패칭/블록↑, 용량→캐시↑, 충돌→연관도↑

## Ⅲ. 흐름도 / 구조
```text
Miss 원인 분류
 ├ Compulsory : 한 번도 적재 안 됨 (불가피)
 ├ Capacity   : 용량 부족 → 축출됨 (완전연관에도 존재)
 └ Conflict   : 집합 충돌 → 매핑 경쟁 (연관도↑로 감소)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 미스 원인 진단으로 캐시 최적화 우선순위 결정 |
| 장점 | 원인별 처방(용량·연관도·프리패치) 명확화 |
| 한계 | 멀티코어 공유 캐시의 Coherence Miss(4번째 C) 미포함 |

## Ⅴ. 기술사적 적용
- 비교: 멀티코어에서 Coherence Miss 추가한 4C 모델
- 실무: 빅팀(Victim) 캐시로 충돌 미스 흡수
- 최신: 프로파일링 기반 미스 분해로 자동 튜닝
