---
title: 컴파일러 vs 인터프리터 (Compiler vs Interpreter)
date: 2026-07-05
tags: [cspe-software]
weight: 145
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 고급 프로그래밍 언어를 기계가 이해할 수 있는 형태로 변환하는 번역기 |
| 배경 | 인간 중심 언어와 기계 중심 명령셋 사이의 간극 해소 필요 |
| 출제 의도 | 번역 시점, 실행 속도, 메모리 효율성 측면의 기술적 차이 분석 |

## Ⅱ. 구성요소
```text
[ Compiler ]: Source -> Object -> Executive -> [Run]
[ Interpreter ]: Source -> [Translate & Run at once]
[ JIT ]: Source -> Bytecode -> [Translate only hot parts] -> [Run]
```
| 항목 | 컴파일러 | 인터프리터 |
|---|---|---|
| 번역 단위 | 소스 전체 (일괄) | 한 줄씩 (순차) |
| 실행 속도 | 빠름 (사전 번역 완료) | 느림 (번역 병행) |
| 파일 형태 | 목적 파일 생성 (exe, obj) | 목적 파일 없음 |
> 요약: 컴파일러는 실행 전 번역을, 인터프리터는 실행 중 번역을 수행함.

## Ⅲ. 절차
```text
(Compiler Flow)
Lexical Analysis -> Syntax -> Semantic -> Intermediate Code -> Optimize -> Target
```
1. 어휘 분석: 소스 코드를 토큰(Token) 단위로 분리하고 식별자 분류.
2. 구문/의미 분석: 문법 규칙 준수 여부 확인 및 타입 체크, AST 생성.
3. 중간 코드 생성: 특정 하드웨어에 종속되지 않는 형태의 코드로 변환.
4. 최적화 및 생성: 중간 표현에 최적화 pass를 적용하고 target ISA의 object code를 생성함.
> 요약: compiler는 source를 분석해 intermediate representation과 object code를 만들고 linker가 실행 단위를 구성함.

## Ⅳ. 문제점
- 컴파일러: 소스 수정 시마다 전체 재컴파일이 필요하여 개발 초기 생산성 저하.
- 인터프리터: 실행 시마다 중복 번역이 발생하여 대규모 연산 시 성능 한계 명확.

## Ⅴ. 개선방안
- 하이브리드 방식(JIT: Just-In-Time)을 도입하여 자주 실행되는 코드를 런타임에 컴파일.
- 증분 컴파일(Incremental Compilation)을 통해 수정된 모듈만 부분 번역하여 시간 단축.

## Ⅵ. 전망
- profile-guided·auto-tuning compiler는 실행 profile과 target 비용 모델로 optimization pass와 code generation을 조정함.
- LLVM 기반 통합: 다양한 언어와 타겟 하드웨어를 유연하게 연결하는 모듈형 컴파일러 확산.
