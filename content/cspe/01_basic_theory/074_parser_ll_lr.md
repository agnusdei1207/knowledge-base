---
title: "파서 LL·LR (Parser LL LR)"
date: "2026-07-01"
tags:
  - "cspe-basic-theory"
weight: 74
---

# 📖 【암기용】 개념 완전 이해

> 목적: LL·LR 파서를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 토큰열이 문법에 맞는지 분석해 parse tree 또는 AST를 만드는 구문 분석 기법
- **왜 필요한가**: 컴파일러, SQL 엔진, JSON/YAML 파서, DSL 처리기는 문자열을 구조화된 트리로 바꿔야 후속 의미 분석과 실행이 가능하다.
- **핵심 직관**: LL은 위에서 아래로 예상하며 읽고, LR은 아래에서 위로 조각을 줄여가며 문장을 완성한다.

## 깊이 이해
- **배경·문제의식**: 어휘 분석이 token을 만들더라도 token 순서가 문법에 맞는지 별도 검사가 필요하다. 파서는 연산자 우선순위, 괄호 중첩, 블록 구조를 트리로 표현한다.
- **작동 원리**: LL parser는 Left-to-right 입력을 읽고 Leftmost derivation을 수행하는 top-down 방식이다. LR parser는 Left-to-right 입력을 읽고 Rightmost derivation의 역순을 수행하는 bottom-up 방식이며, shift/reduce 동작으로 스택을 갱신한다.
- **비유**: LL은 설계도를 머릿속에 두고 다음 부품을 예측하며 조립하는 방식이고, LR은 들어온 부품을 쌓다가 완성된 묶음이 보이면 큰 부품으로 접는 방식이다.
- **구체 예시**: `E -> E + T | T` 같은 좌재귀 문법은 LL 파서에서 무한 재귀 위험이 있어 제거가 필요하지만, LR 파서는 좌재귀 문법을 처리할 수 있다.
- **흔한 오해·주의점**: LL이 항상 구현 난도가 낮고 LR이 항상 정답은 아니다. LL은 오류 메시지와 수작업 구현에 유리하고, LR은 문법 수용 범위와 생성기 기반 컴파일러에 유리하다.

## 연결 개념
- CFG — 파서가 처리하는 문법 표현
- 컴파일러 구조 — 구문 분석 단계의 위치
- AST — 파싱 결과를 의미 분석과 코드 생성에 전달하는 트리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 파서는 token stream을 CFG 기준으로 분석해 parse tree/AST를 생성하는 구문 분석기임.
> 2. **가치**: 문법 오류를 조기에 탐지하고 AST를 생성해 타입 검사, 최적화, 실행 계획 수립의 입력을 제공함.
> 3. **판단 포인트**: LL은 예측 파싱과 수작업 구현, LR은 문법 수용 범위와 shift/reduce 기반 생성기 활용을 기준으로 선택함.

---

## Ⅰ. 개요 및 필요성

파서는 토큰열을 문법 트리로 변환한다. 언어 처리 시스템은 문자열을 직접 실행하지 않고, 문법 검증 후 AST로 바꿔 의미 분석과 코드 생성을 수행한다. LL·LR 파서 선택은 문법 형태, 오류 진단, 생성기 사용 여부에 따라 달라짐.

---

## Ⅱ. 구조 및 구성요소

```text
Token Stream -> Parser -> Parse Tree/AST -> Semantic Analyzer
                +-> Grammar CFG
                +-> Parse Table/Stack
                +-> Error Recovery
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Token Stream | lexer가 만든 입력 단위 | type, lexeme, position 포함 |
| Grammar | 허용 구문 규칙 제공 | CFG, precedence, associativity |
| Parse Stack/Table | 파싱 상태 관리 | LL table, LR action/goto table |
| AST Builder | 구문 트리를 의미 트리로 축약 | 불필요 괄호·구분자 제거 |

> 요약: 파서는 토큰, 문법, 상태 관리 구조를 이용해 AST를 생성하고 오류 위치를 보고함.

---

## Ⅲ. 동작원리 및 흐름도

```text
토큰 입력 -> 문법 선택 -> 파싱 동작 수행 -> AST 생성 -> 오류/성공 반환
             +-> LL: 예측/전개
             +-> LR: shift/reduce
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | FIRST/FOLLOW 또는 LR item 구성 | table conflict 0건 |
| 2 | 토큰을 좌에서 우로 읽기 | lookahead k개 기준 |
| 3 | LL 전개 또는 LR shift/reduce 수행 | stack underflow 0건 |
| 4 | AST 생성과 오류 복구 | syntax error 위치 line/column |

> 요약: LL은 예측 전개, LR은 shift/reduce로 토큰열을 문법 구조에 매핑함.

---

## Ⅳ. 특징

| 구분 | LL Parser | LR Parser | 판단 포인트 |
|:---|:---|:---|:---|
| 분석 방향 | Top-down | Bottom-up | 구현 방식 차이 |
| 유도 방식 | Leftmost derivation | Rightmost derivation 역순 | 문법 수용 범위 |
| 좌재귀 | 제거 필요 | 처리 가능 | 산술식 문법은 LR 후보 |
| 도구 | recursive descent, ANTLR LL(*) | Yacc/Bison, LALR(1) | 오류 진단과 생성기 생태계 |

> 요약: LL은 예측성과 오류 메시지, LR은 좌재귀 처리와 문법 수용 범위를 기준으로 선택함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구현 | recursive descent LL | LALR/CLR LR | 수작업이면 LL, 생성기 기반이면 LR |
| 문법 | 좌재귀 제거 문법 | 좌재귀 허용 문법 | 산술식·우선순위 문법은 LR 유리 |
| 진단 | 첫 오류 위치 제시 | conflict 분석 필요 | IDE 친화 오류 메시지는 LL 고려 |

> 요약: 개발자 경험은 LL, 문법 표현력과 전통 컴파일러 도구는 LR을 우선 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 무한 재귀 | LL에서 좌재귀 문법 사용 | left recursion elimination | 파서 생성 성공 |
| shift/reduce conflict | 모호 문법, 우선순위 미지정 | precedence/associativity 선언 | conflict 0건 |
| 오류 복구 미흡 | panic mode 부재 | synchronization token 설정 | 오류 1건당 복구 위치 1개 이상 |

> 요약: 좌재귀, conflict, 오류 복구는 문법 변환과 파서 생성기 리포트로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 문법 품질 | conflict 0건, 모호 parse 0건 | generator report |
| 처리 성능 | 평균 O(n), 1MB 입력 1초 이하 | benchmark |
| 오류 진단 | line/column 정확도 95% 이상 | negative test suite |

> 요약: 파서 도입은 문법 충돌, 처리시간, 오류 위치 정확도로 성공 여부를 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 문법 설계: CFG 작성 후 FIRST/FOLLOW 또는 LR item set으로 conflict 0건 확인
2. 도구 선택: DSL·IDE 플러그인은 ANTLR LL(*), 컴파일러·SQL 계열은 Bison/LALR(1) 검토
3. 검증: 양성/음성 문법 테스트 1,000건, fuzzing, 오류 복구 line/column 검증 수행

**결론 (2줄):**
- 기술사 판단: 오류 진단과 수작업 구현이 중요하면 LL, 좌재귀와 복잡 문법 수용이 중요하면 LR 선택
- 향후 방향: 파서는 IDE 실시간 분석, DSL, 보안 입력 검증과 결합되어 incremental parsing 요구가 증가함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "파서를 설명하시오", "LL·LR 파싱을 기술하시오" | token에서 AST까지 파싱 흐름 | LL/LR 방향, 유도, 좌재귀 처리 |
| 요구사항 명시형 | "LL과 LR을 비교하시오", "파서 설계 방안을 제시하시오" | conflict 검출과 오류 복구 절차 | 선택 기준, 리스크 대응, 검증 지표 |

> 요약: 설명형은 파싱 절차, 비교·설계형은 LL/LR 선택 기준과 conflict 대응을 중심으로 작성함.
