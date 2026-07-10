---
title: 자바 가상 머신 JVM 구조 (JVM Architecture)
date: 2026-07-05
tags: [cspe-software]
weight: 160
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 자바 바이트코드를 실행하기 위한 가상 컴퓨터 아키텍처 |
| 필요성 | class file의 platform별 실행, bytecode 검증, JIT compilation, garbage collection 제공 |
| 출제 의도 | 런타임 데이터 영역(Heap, Stack 등) 및 실행 엔진 작동 원리 측정 |

## Ⅱ. 구성요소
```text
+-----------------------------------------------------------+
|                     Class Loader System                   |
+-----------------------------------------------------------+
|   Runtime Data Areas (Memory)                             |
| +----------+ +----------+ +----------+ +-------+ +------+ |
| |  Method  | |   Heap   | |  Stack   | | PC Reg| |Native| |
| +----------+ +----------+ +----------+ +-------+ +------+ |
+-----------------------------------------------------------+
|   Execution Engine (Interpreter, JIT, GC)                 |
+-----------------------------------------------------------+
```
| 영역 | 설명 | 특징 |
|---|---|---|
| Method Area | 클래스 정보, 상수, 정적 변수 저장 | 모든 스레드 공유 |
| Heap | 동적으로 생성된 객체(Instance) 저장 | GC의 주 대상 |
| Stack | 메서드 호출 정보, 지역 변수 저장 | 스레드별 독립 생성 |
> 요약: 데이터 영역은 저장 용도별로 구분되며, 실행 엔진은 이를 가공해 동작함.

## Ⅲ. 절차
```text
.java -> javac -> .class -> Class Loader -> Runtime Data Areas -> Exec Engine
```
1. 로딩: 클래스 로더가 .class 파일을 읽어 메서드 영역에 데이터 적재.
2. 링크: 바이트코드 검증(Verify) 및 정적 변수 기본값 준비(Prepare).
3. 초기화: 정적 블록 실행 및 정적 변수에 실제 값 할당.
4. 실행: 인터프리터가 명령을 수행하며, 빈번한 코드는 JIT가 기계어로 변환.
> 요약: JVM은 class를 load·link·initialize하고 bytecode를 interpret하며 hot code를 JIT compile해 실행함.

## Ⅳ. 문제점
- 힙 영역의 과도한 객체 생성 시 GC 부하로 인한 애플리케이션 응답 지연.
- 스택 크기 설정 오류 시 딥 재귀 호출 등에 의한 StackOverflowError 발생.

## Ⅴ. 개선방안
- live set, allocation rate, pause 목표, container memory limit을 기준으로 Xms·Xmx와 GC를 조정함.
- G1 GC 또는 ZGC 선택 및 세대별 가설(Generational Hypothesis) 기반 튜닝.

## Ⅵ. 전망
- Project Valhalla: 값 객체(Value Object) 도입으로 힙 메모리 효율 및 캐시 지역성 혁신.
- 지능형 모니터링: AI 기반 프로파일러가 GC 패턴을 실시간 분석 및 자동 튜닝 제안.
