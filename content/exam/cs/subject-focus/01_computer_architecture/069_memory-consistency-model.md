---
title: "메모리 일관성 모델 (Memory Consistency Model)"
date: "2026-06-30"
weight: 69
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 다중 프로세서에서 여러 메모리 위치에 대한 읽기·쓰기 연산이 관찰되는 순서를 규정하는 규칙으로, 하드웨어와 프로그래머 간의 메모리 순서 계약.

## Ⅱ. 구성요소 / 원리
- 순차 일관성(SC, Sequential Consistency): 모든 연산이 프로그램 순서대로 단일 순서 관찰
- 완화된 모델(Relaxed): 성능 위해 일부 순서 재배열 허용(TSO·Weak·Release)
- TSO(Total Store Order): 스토어-로드 재배열만 허용(x86)
- 동기화 연산(배리어·acquire/release)으로 순서 강제

## Ⅲ. 흐름도 / 구조
```text
[SC]    프로그램순서 = 관찰순서 (재배열 無)
[Relaxed] Store버퍼로 재배열 허용
         → Memory Barrier로 순서 보장 지점 삽입
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 멀티스레드 메모리 연산 순서의 정확성 보장 |
| 장점 | 완화모델은 성능↑, 명시적 동기화로 정확성 확보 |
| 한계 | SC는 성능 제약, 완화모델은 추론·디버깅 난해 |

## Ⅴ. 기술사적 적용
- 일관성(Coherence)은 단일 위치, 일관성 모델(Consistency)은 다수 위치 순서
- x86=TSO, ARM/RISC-V=Weak(약순서) 모델
- C++/Java 메모리 모델, atomic의 memory_order로 추상화
