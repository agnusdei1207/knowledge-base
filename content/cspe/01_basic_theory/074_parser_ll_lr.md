---
title: "파서 — LL·LR 파싱 (Parser LL LR)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 74
---

# 파서 - LL·LR 파싱 (Parser LL LR)

## 1. 개요

- **정의/개념**: 파서는 토큰열이 문법에 맞는지 분석하고 구문 구조를 AST나 파스 트리로 구성하는 컴파일러 프론트엔드 구성요소이다.
- **배경/필요성**: 소스 코드나 DSL을 단순 문자열로 처리하면 중첩 구조와 우선순위를 정확히 해석하기 어렵기 때문에 문법 기반 분석기가 필요하다.

파서의 핵심은 토큰열을 문법 규칙에 맞춰 구조화하고, 오류 위치를 의미 있게 알려 주는 것이다.

## 2. 특징 및 비교

| 구분 | LL Parser | LR Parser |
|---|---|---|
| 방향 | Left-to-right, Leftmost derivation | Left-to-right, Rightmost derivation reverse |
| 방식 | top-down | bottom-up |
| 장점 | 구현·이해 쉬움 | 더 넓은 문법 처리 |
| 약점 | 좌재귀 취약 | 테이블·구현 복잡 |
| 대표 | recursive descent | Yacc/Bison 계열 |

선택 기준은 문법 복잡도, 오류 메시지 품질, 구현 난이도, parser generator 사용 여부이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Token Stream | lexer의 출력 | parser 입력 |
| Grammar | 생성 규칙 | 분석 기준 |
| Parse Table/Function | 다음 동작 결정 | LL/LR 차이 |
| Stack | 파싱 상태 관리 | LR에서 핵심 |
| AST | 구문 구조 산출물 | 이후 의미 분석 입력 |

```text
Source -> Lexer -> Token Stream -> Parser -> AST -> Semantic Analysis
```

파서는 lexer와 semantic analyzer 사이를 연결하므로, 토큰 정의와 문법 규칙이 일관되어야 한다.

## 4. 문제점 및 개선방안

1. **문법 모호성**
   - 하나의 토큰열에 여러 파스 트리가 가능하면 해석이 달라진다.
   - **개선방안**: 우선순위·결합 규칙을 명시하고 문법을 재작성한다.

2. **좌재귀와 LL 제약**
   - LL parser는 좌재귀 문법을 직접 처리하기 어렵다.
   - **개선방안**: 좌재귀 제거, left factoring, LR parser 적용을 검토한다.

3. **오류 복구 어려움**
   - 문법 오류 후 분석을 중단하면 사용성이 떨어진다.
   - **개선방안**: panic mode, synchronization token, 위치 기반 오류 메시지를 제공한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 프로그래밍 언어 | 문법 규칙으로 AST 생성 | 파싱 성공률 |
| DSL 처리 | 업무 언어를 recursive descent parser로 구현 | 오류 메시지 품질 |
| 정적 분석 | AST 기반 코드 품질·보안 검사 | 탐지율, 분석 시간 |

## 6. 결론

파서는 토큰열을 문법 구조로 바꾸는 컴파일러 핵심 단계이다. LL/LR 차이는 top-down과 bottom-up 방식, 문법 처리 범위, 오류 처리 전략으로 연결해야 실무 선택 기준이 분명해진다.
