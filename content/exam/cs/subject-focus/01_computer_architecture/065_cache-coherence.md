---
title: "캐시 일관성 (Cache Coherence)"
date: "2026-06-30"
weight: 65
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 다중 프로세서가 동일 메모리 블록을 각자 캐시에 복사할 때, 모든 캐시 사본이 일관된 값을 보도록 보장하는 성질·메커니즘.

## Ⅱ. 구성요소 / 원리
- 쓰기 전파(Write Propagation): 한 캐시의 변경을 다른 사본에 전달
- 쓰기 직렬화(Write Serialization): 모든 프로세서가 쓰기 순서를 동일하게 관찰
- 무효화(Invalidate) vs 갱신(Update) 정책
- 프로토콜: 스누핑(Snooping)·디렉터리(Directory)

## Ⅲ. 흐름도 / 구조
```text
P0 write X=1 → coherence 메커니즘
   ├ Invalidate: P1캐시의 X 무효화
   └ 이후 P1 read X → 최신값 1 획득
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 다중 캐시 환경에서 데이터 정확성·정합성 보장 |
| 장점 | 공유 메모리 프로그래밍 모델 투명성 제공 |
| 한계 | 일관성 트래픽·지연, 확장성 비용(거짓공유 유발) |

## Ⅴ. 기술사적 적용
- MESI/MOESI 등 상태기반 프로토콜로 구현
- 일관성(Coherence)과 메모리 일관성 모델(Consistency)은 구분
- ccNUMA·멀티코어 인터커넥트(UPI·CCI)의 핵심 요건
