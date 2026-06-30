---
title: "메모리 계층구조 (Memory Hierarchy)"
date: "2026-06-30"
weight: 38
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 속도·용량·비용이 상이한 기억장치를 계층적으로 배치하여, 빠른 소량 장치와 느린 대용량 장치의 절충으로 평균 접근시간을 최소화하는 구조.

## Ⅱ. 구성요소 / 원리
- 계층 순서: 레지스터 → 캐시(L1/L2/L3) → 주기억장치(DRAM) → 보조기억장치(SSD/HDD)
- 상위로 갈수록: 고속·고가·소용량, 하위로 갈수록: 저속·저가·대용량
- 동작 기반: 참조의 지역성(Locality)으로 상위 계층 적중률 향상
- 포함관계(Inclusion): 상위 계층 데이터는 하위 계층의 부분집합
- 데이터 이동 단위: 캐시는 블록(Block/Line), 메모리는 페이지(Page)

## Ⅲ. 흐름도 / 구조
```text
[CPU Register]  ← 최고속·최소
     ↓
[Cache L1/L2/L3]
     ↓        지역성 기반 적중
[Main Memory(DRAM)]
     ↓
[Storage(SSD/HDD)] ← 최저속·최대
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 속도-용량-비용 trade-off 최적화, 평균 접근시간 단축 |
| 장점 | 적은 비용으로 고속 대용량에 근접한 성능 제공 |
| 한계 | 계층 간 일관성·포함성 유지 비용, 지역성 낮으면 효과 급감 |

## Ⅴ. 기술사적 적용
- 비교: 폰노이만 병목(Von Neumann Bottleneck) 완화 수단
- 실무: NUMA, HBM(High Bandwidth Memory) 적층 메모리로 계층 확장
- 최신: CXL(Compute Express Link) 기반 메모리 풀링·계층화
