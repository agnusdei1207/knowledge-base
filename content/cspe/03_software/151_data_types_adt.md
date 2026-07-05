---
title: 자료형 및 추상 자료형 ADT (Data Types ADT)
date: 2026-07-05
tags: [cspe-software]
weight: 151
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 데이터의 집합과 그 위에서 수행 가능한 연산을 정의한 논리적 명세 |
| 필요성 | 데이터 표현의 규격화, 논리적 설계와 물리적 구현의 분리(은닉) |
| 출제 의도 | 자료형의 분류, ADT의 개념 및 스택/큐 등의 명세화 역량 |

## Ⅱ. 구성요소
```text
[ Data Type ]
  - Basic: int, float, char
  - Composite: array, struct
[ Abstract Data Type (ADT) ]
  - Interface: push(), pop(), peek()
  - Specification: "Last In First Out"
  - (Hidden) Implementation: Array-based or Linked-list
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 자료형 | 컴퓨터가 처리하는 데이터의 형식과 범위 | 그릇의 크기와 종류 |
| 연산 (Operation) | 해당 데이터로 할 수 있는 행동 (Read/Write) | 그릇 사용법 |
| 캡슐화 | 내부 구현을 감추고 인터페이스만 제공 | 리모컨 버튼만 노출 |
> 요약: ADT는 '무엇(What)'을 수행하는지 정의하고, 구현은 '어떻게(How)'를 다룸.

## Ⅲ. 절차
```text
Logical Design -> ADT Specification -> Concrete Data Structure -> Implementation
      |                  |                        |                    |
  (문제분석)         (명세 작성)              (알고리즘 선택)        (코딩)
```
1. 문제 정의: 해결하려는 도메인의 핵심 데이터와 필요 행위 식별.
2. ADT 설계: 데이터의 논리적 특성과 제약 조건(LIFO/FIFO 등)을 명세화.
3. 자료구조 선택: 성능(O-notation)과 메모리 효율을 고려해 배열/연결리스트 결정.
4. 구현 및 검증: 선택한 언어로 코드를 작성하고 명세 준수 여부 테스트.
> 요약: ADT는 설계의 틀을 제공하여 코드의 재사용성과 유지보수성을 높임.

## Ⅳ. 문제점
- 지나친 추상화는 런타임 시 불필요한 레이어 오버헤드를 발생시킬 수 있음.
- 자료형 간의 암시적 형변환(Implicit Casting) 발생 시 정밀도 손실 및 오류 위험.

## Ⅴ. 개선방안
- 강타입(Strong Typing) 언어와 제네릭(Generic)을 활용하여 타입 안정성 확보.
- 성능이 중요한 영역에서는 추상화 레이어를 제거하는 'Zero-cost Abstraction' 적용.

## Ⅵ. 전망
- 지능형 타입 추론: 개발자의 의도를 파악하여 최적의 ADT를 추천/선택하는 IDE 진화.
- 대규모 분산 ADT: 네트워크 너머에 존재하는 대용량 데이터를 다루는 분산 자료형 대두.
