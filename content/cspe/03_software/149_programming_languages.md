---
title: 프로그래밍 언어의 역사 및 분류 (Programming Languages)
date: 2026-07-05
tags: [cspe-software]
weight: 149
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 인간의 의도를 컴퓨터가 실행할 수 있게 변환하는 체계적인 기호 시스템 |
| 배경 | 하드웨어 제어 중심에서 문제 해결 및 생산성 중심으로 진화 |
| 출제 의도 | 세대별 분류(1~5세대), 구현 방식(컴파일/스크립트), 패러다임 이해 |

## Ⅱ. 구성요소
```text
[ 1GL: Machine ] -> [ 2GL: Assembly ] -> [ 3GL: High-Level ]
                                                | (C, Java, Python)
                                         [ 4GL: SQL/Domain ]
                                                |
                                         [ 5GL: AI/Natural ]
```
| 세대 | 특징 | 대표 언어 |
|---|---|---|
| 3세대 | 절차적, 구조적 코딩, 범용성 | C, Fortran, Pascal |
| 4세대 | 비절차적, 특정 목적 지향, 생산성 | SQL, MATLAB, SAS |
| 5세대 | 인공지능, 지식 기반, 제약 조건 해결 | Prolog, LISP |
> 요약: 언어 세대 분류는 machine instruction·assembly symbol·high-level syntax·declarative constraint처럼 문제 표현 단위가 달라지는 흐름임.

## Ⅲ. 절차
```text
(Evolutionary Steps)
Machine-centric -> Structural -> OOP -> Functional -> Declarative
       |               |          |           |            |
     (Raw)          (Reuse)   (Data+Op)   (State-free)   (Result)
```
1. 기계 중심: 0과 1 또는 1:1 대응 니모닉으로 제어하던 초창기 단계.
2. 구조화/절차화: 고투(goto)문을 지양하고 루프와 조건문으로 흐름을 관리하는 시기.
3. 데이터 중심(OOP): 데이터와 이를 처리하는 로직을 객체로 묶어 복잡도 극복.
4. 추상화 고도화: 상태 변화를 최소화하거나 결과만 명시하는 선언적 코딩 확산.
> 요약: 언어는 memory·control flow·type·concurrency·domain rule을 서로 다른 abstraction으로 표현해 구현 세부의 직접 관리 범위를 줄임.

## Ⅳ. 문제점
- 언어의 다양화로 인한 개발자 기술 파편화 및 레거시 시스템 마이그레이션 비용.
- 고수준 언어의 추상화에 따른 성능 오버헤드 및 런타임 의존성 증가.

## Ⅴ. 개선방안
- 멀티 패러다임 언어(Python, Rust 등)를 통해 효율성과 생산성의 균형 도모.
- transpiler는 한 high-level language source를 호환되는 다른 language·version source로 변환함.

## Ⅵ. 전망
- No-Code/Low-Code: 프로그래밍 언어를 몰라도 비즈니스 로직을 구축하는 환경 확대.
- 생성형 AI 연동: 자연어로 의도를 전달하면 코드를 자동 생성/최적화하는 개발 혁신.
