---
title: 가상 머신 런타임 — JVM·CLR (VM Runtime)
date: 2026-07-05
tags: [cspe-software]
weight: 159
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 특정 언어로 작성된 바이트코드를 실제 하드웨어 명령으로 변환 실행하는 환경 |
| 배경 | "Write Once, Run Anywhere" 실현 및 메모리 관리의 자동화 요구 |
| 출제 의도 | 중립적 언어(Bytecode, CIL), JIT 컴파일러, 가비지 컬렉션 구조 이해 |

## Ⅱ. 구성요소
```text
[ Source Code ] -> [ Compiler ] -> [ Bytecode / IL ]
                                           |
+------------------------------------------v-----------+
|               Virtual Machine Runtime                |
|  +-------------+  +--------------+  +--------------+ |
|  | Class Loader|  | JIT Compiler |  |  Memory (GC) | |
|  +-------------+  +--------------+  +--------------+ |
+------------------------------------------+-----------+
                                           |
                                   [ Native Machine Code ]
```
| 항목 | JVM (Java) | CLR (.NET) |
|---|---|---|
| 중간 언어 | Java Bytecode (.class) | Common Intermediate Lang (CIL) |
| 컴파일 방식 | JIT (HotSpot) | JIT / AOT (Native Image) |
| 실행 환경 | JRE / JDK | .NET Runtime / SDK |
> 요약: 런타임은 하드웨어와 앱 사이의 추상화 계층으로 이식성과 보안을 제공함.

## Ⅲ. 절차
```text
Load Code -> Verify -> Interpret -> Profile -> JIT Compile -> Execute
  |          |          |          |          |              |
(로딩)     (검증)     (실행)     (분석)     (최적화)       (원어실행)
```
1. 로딩 및 검증: 바이트코드를 메모리에 올리고 문법/보안 위반 사항을 사전 체크.
2. 인터프리팅: 초기 실행 시 바이트코드를 한 줄씩 해석하여 즉시 실행.
3. 프로파일링: 런타임 중 자주 호출되는 'Hot Method'를 실시간 모니터링.
4. JIT 컴파일: 분석된 핵심 코드를 기계어로 직접 번역 및 최적화하여 속도 향상.
> 요약: 해석(Slow)으로 시작하여 컴파일(Fast)로 진화하는 동적 최적화 방식임.

## Ⅳ. 문제점
- 초기 구동 시 클래스 로딩 및 인터프리팅으로 인한 'Warm-up' 시간 소요.
- 가비지 컬렉션(GC) 수행 시 프로그램이 일시 정지하는 'Stop-the-world' 현상.

## Ⅴ. 개선방안
- GraalVM 등을 활용한 사전 컴파일(AOT) 기술 적용으로 구동 속도 획기적 개선.
- ZGC, Shenandoah 등 초저지연 GC 도입으로 일시 정지 시간을 ms 단위 이하로 단축.

## Ⅵ. 전망
- 다중 언어 지원(Polyglot): 하나의 런타임에서 Java, Python, JS 등을 혼용 실행.
- 클라우드 네이티브: 컨테이너 환경에 최적화된 초경량/초고속 런타임 이미지 개발 가속.
