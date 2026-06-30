---
title: "캐시 사상 (Cache Mapping: 직접·완전연관·집합연관)"
date: "2026-06-30"
weight: 43
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 주기억장치의 블록을 캐시의 어느 라인에 배치할지 결정하는 규칙으로, 직접·완전연관·집합연관 사상 방식이 있다.

## Ⅱ. 구성요소 / 원리
- 직접 사상(Direct): 블록 → (블록번호 mod 라인수) 한 곳 고정, 단순·고속·충돌多
- 완전연관(Fully Associative): 블록을 임의 라인에 배치, 충돌 최소·탐색 비용↑
- 집합연관(Set Associative): 캐시를 N-way 집합으로 분할, 집합 내 임의 배치(절충)
- 주소 구성: 직접/집합=Tag+Index+Offset, 완전연관=Tag+Offset
- 비교: 연관도↑ → 충돌 미스↓, 비교기·전력↑

## Ⅲ. 흐름도 / 구조
```text
Direct   : Block → 단 1개 Line (mod)        탐색 1회
Set-Assoc: Block → Set 선택 → N-way 중 택1   탐색 N회
Full     : Block → 모든 Line 후보            탐색 전체
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 블록 배치 자유도와 탐색 비용의 균형 선택 |
| 장점 | 집합연관이 적중률·비용 절충으로 실무 표준 |
| 한계 | 직접=충돌 미스, 완전연관=비교기·전력 과다 |

## Ⅴ. 기술사적 적용
- 비교: 실제 L1=8~12way, L3=16way 이상 집합연관 채택
- 실무: way prediction으로 집합연관 지연·전력 절감
- 최신: 스큐드(Skewed)·해시 기반 사상으로 충돌 분산
