---
title: 변수 범위 및 생명주기 (Variable Scope)
date: 2026-07-05
tags: [cspe-software]
weight: 154
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 프로그램 내에서 변수가 참조 가능한 영역(Scope)과 메모리에 유지되는 시간 |
| 배경 | 이름 충돌 방지, 메모리 관리 효율화 및 캡슐화 구현 필요 |
| 출제 의도 | 전역/지역/정적 변수의 특성, 정적/동적 스코프 차이 이해 |

## Ⅱ. 구성요소
```text
[ Storage Duration ]       [ Scope Level ]
- Static: Program end      - Global: All files
- Automatic: Block end     - File: Single file
- Dynamic: Manual free     - Block: Inside {}
```
| 변수 종류 | 저장 위치 | 생명주기 | 범위 |
|---|---|---|---|
| 지역 변수 | Stack | 블록 진입/탈출 시 | 해당 블록 내 |
| 전역 변수 | Data Segment | 프로그램 시작/종료 시 | 프로그램 전체 |
| 정적 변수 | Data Segment | 프로그램 시작/종료 시 | 선언된 범위 내 |
> 요약: 변수의 선언 위치와 예약어(static 등)에 따라 가시성과 수명이 결정됨.

## Ⅲ. 절차
```text
(Static Scope)
Function Def -> Outer Scope Bound -> Reference Check (Compile Time)
(Dynamic Scope)
Function Call -> Call Stack Search -> Reference Check (Runtime)
```
1. 심볼 등록: 컴파일러가 변수 선언을 발견하고 해당 스코프의 심볼 테이블에 기록.
2. 식별자 해석: 변수 사용 시 현재 스코프부터 상위 스코프 방향으로 정의를 탐색.
3. 저장 위치 결정: storage duration과 escape 여부에 따라 register·stack·static area·heap에 배치함.
4. 수명 종료: stack frame 반환, destructor·owner 해제, GC 도달성 판정 등 언어별 규칙으로 자원을 회수함.
> 요약: 대부분의 현대 언어는 코드 구조로 범위를 결정하는 정적 스코프를 사용함.

## Ⅳ. 문제점
- 전역 변수 남용 시 함수 간 결합도 상승으로 사이드 이펙트 추적 및 디버깅 곤란.
- 클로저(Closure) 사용 시 참조된 자유 변수의 수명이 예상보다 길어져 메모리 누수 위험.

## Ⅴ. 개선방안
- 변수 가시성을 최소화하는 '최소 권한의 원칙' 적용 (지역 변수 우선 권장).
- 모듈화 및 네임스페이스(Namespace)를 활용하여 전역 심볼 충돌 방지.

## Ⅵ. 전망
- Rust ownership·borrow checker는 compile time에 value lifetime과 aliasing 규칙을 검사함.
- 지능형 린터: 사용되지 않는 변수나 위험한 수명 주기를 AI가 사전 탐지 및 수정 제안.
