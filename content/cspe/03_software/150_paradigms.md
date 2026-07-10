---
title: 절차적 vs 객체지향 vs 함수형 (Paradigms)
date: 2026-07-05
tags: [cspe-software]
weight: 150
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 프로그래밍의 접근 방식과 구조를 정의하는 근본적인 사고 체계 |
| 배경 | 대규모 시스템 개발의 복잡성 해결 및 유지보수성 향상 요구 |
| 출제 의도 | 각 패러다임의 핵심 원리(상태, 데이터, 함수) 및 차이점 비교 |

## Ⅱ. 구성요소
```text
[ Procedural ]     [ Object-Oriented ]     [ Functional ]
+------------+     +-----------------+     +------------+
|  Function  |     |   +---------+   |     |  Function  |
|     |      |     |   |  Data   |   |     | (No State) |
|  Data(Glob)|     |   +---------+   |     |     |      |
+------------+     +-----------------+     +------------+
  (Sequence)         (Encapsulation)        (Immutability)
```
| 패러다임 | 핵심 개념 | 대표 언어 |
|---|---|---|
| 절차적 | 명령의 순차적 실행, 전역 상태 공유 | C, Pascal |
| 객체지향 | 데이터+행위 캡슐화, 상속, 다형성 | Java, C++ |
| 함수형 | 순수 함수, 불변성, 고차 함수 | Haskell, LISP |
> 요약: 객체지향은 state와 behavior를 object에 캡슐화하고, 함수형은 immutable value와 function composition으로 state change를 제한함.

## Ⅲ. 절차
```text
(OOP) Obj.Method() -> Message Passing -> State Update -> Interaction
(FP)  Input -> Function A -> Function B -> Output (Immutable)
```
1. 절차적: 문제를 단계별 절차로 분해하고 공통 데이터를 함수들이 조작함.
2. 객체지향: 문제를 자율적인 객체들로 정의하고 메시지 교환으로 협력을 구현함.
3. 함수형: pure function·immutable value·higher-order function으로 계산을 합성하고 side effect 경계를 분리함.
4. 멀티 패러다임: 문제의 state·control·data transformation 특성에 따라 여러 모델을 함께 적용함.
> 요약: 절차형은 명령 순서, 객체지향은 책임과 상태, 함수형은 값 변환과 side effect 경계를 중심으로 구조화함.

## Ⅳ. 문제점
- OOP: 과도한 상속 계층과 캡슐화 오버헤드로 인한 복잡도 상승 및 성능 저하.
- FP: 상태가 없으므로 반복문 처리가 어렵고 대량의 메모리 복사가 발생할 수 있음.

## Ⅴ. 개선방안
- OOP의 '상속보다는 합성(Composition)' 원칙을 강조하여 유연성 확보.
- FP의 장점(불변성)을 일반 언어에 도입하여 멀티코어 환경의 스레드 안전성 강화.

## Ⅵ. 전망
- 융합형 언어 가속: Rust, Kotlin 등 현대 언어들의 함수형 기능 적극 채택.
- 데이터 사이언스: 데이터 변환과 처리에 최적화된 함수형 패러다임 활용 범위 지속 확대.
