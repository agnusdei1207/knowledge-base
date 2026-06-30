---
title: "거짓공유 (False Sharing)"
date: "2026-06-30"
weight: 68
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 서로 다른 프로세서가 논리적으로 독립된 변수를 수정하지만 같은 캐시 라인(Cache Line)에 위치해, 불필요한 일관성 트래픽으로 성능이 저하되는 현상.

## Ⅱ. 구성요소 / 원리
- 캐시 일관성은 캐시 라인(보통 64B) 단위로 동작
- 한 코어가 라인 내 변수 수정 시 전체 라인 무효화
- 다른 코어가 같은 라인의 별개 변수 접근 시 캐시 미스 재발생
- 진짜 공유는 없으나 라인 공유로 핑퐁(ping-pong) 발생

## Ⅲ. 흐름도 / 구조
```text
[Cache Line: varA | varB]  (같은 라인)
P0 write varA → 라인 Invalidate → P1의 varB도 미스
P1 write varB → 라인 Invalidate → P0의 varA도 미스 (핑퐁)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 다중코어 병렬 성능 저하 원인 식별·제거 |
| 장점 | 인지·해소 시 확장성·성능 큰 개선 |
| 한계 | 발견 곤란(논리적으론 정상), 프로파일링 필요 |

## Ⅴ. 기술사적 적용
- 해소: 패딩(Padding)·정렬(alignment)로 변수 분리, per-CPU 데이터
- 언어 지원: C++ alignas(hardware_destructive_interference_size)
- 멀티스레드 자료구조·락 설계 시 핵심 고려사항
