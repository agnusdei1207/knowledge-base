---
title: 53. DB 파서와 파스 트리 (DB Parser Parse Tree)
date: '2026-05-01'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DB 파서 (Parser)는 SQL 문장을 문법에 맞는 파스 트리 (Parse Tree)로 변환하는 첫 단계다.
> 2. **가치**: 파스 트리는 문법 오류를 잡고, 의미 분석과 최적화의 출발점을 제공한다.
> 3. **판단 포인트**: 파스 트리, AST (Abstract Syntax Tree), [[369_logic_bomb|논리]] 계획, [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 구분해야 [[502_dbms|DBMS]] ([[501_database|Database]] [[372_management|Management]] System) 설계를 정확히 설명할 수 있다.

---

## Ⅰ. 개요 및 필요성

DBMS는 SQL을 그대로 실행하지 않는다. 먼저 [[820_tokenization|토큰화]]하고, 문법을 검사하고, 구문 구조를 트리로 만든 뒤 의미 분석과 최적화를 [[216_progress_in_synchronization|진행]]한다.

파서와 파스 트리는 SQL 오류를 빠르게 찾게 하고, 이후 단계가 [[298_qkv_attention|쿼리]]의 의도를 이해하게 해 준다.

- **📢 섹션 요약 비유**: 파서와 파스 트리는 문장을 받아 맞춤법과 문장 구조를 먼저 검사하는 국어 선생님과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SQL 처리 흐름은 보통 lexer, parser, semantic analyzer, [[088_optimizer|optimizer]], executor 순서로 이어진다. 파서는 토큰을 문법 규칙에 맞춰 트리 구조로 조립한다.

```text
SQL Text → Tokens → Parse Tree → Semantic Check → Query Plan
```

| 단계 | 역할 | 결과 |
| :--- | :--- | :--- |
| Lexer | 문자 분리 | 토큰 |
| Parser | 문법 검사 | 파스 트리 |
| Semantic Analyzer | 의미 검사 | 타입/[[005_schema|스키마]] [[395_verification_process_review|검증]] |
| [[088_optimizer|Optimizer]] | 계획 선택 | [[369_logic_bomb|논리]]/물리 계획 |

파스 트리는 원문 문법 구조를 충실히 보존하고, AST는 의미 없는 문법 노드를 줄여 핵심 구조만 남긴다. [[502_dbms|DBMS]] 구현에서는 둘을 구분해 설명하는 것이 중요하다.

- **📢 섹션 요약 비유**: 파스 트리는 문장 전체를 다 적은 노트이고, AST는 핵심만 남긴 요약 노트다.

---

## Ⅲ. 비교 및 연결

파스 트리는 SQL 문법 설명에, AST는 [[298_qkv_attention|쿼리]] 최적화 설명에 자주 쓰인다. 또한 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]은 실제로 어떤 [[154_database_index_b_tree_search_optimization|인덱스]]를 쓰고 어떤 [[176_join_order_optimization|조인 순서]]를 택할지 보여 준다.

| 항목 | 파스 트리 | AST | [[166_execution_plan_optimizer_navigation_tree|실행 계획]] |
| :--- | :--- | :--- | :--- |
| 초점 | 문법 구조 | 의미 구조 | 실행 방법 |
| 상세도 | 높음 | 중간 | 낮음~중간 |
| 용도 | 파싱 결과 | 내부 처리 | 실제 수행 |

이 차이를 알아야 "SQL이 어떻게 실행되는가"를 단계별로 설명할 수 있다. 파서가 문법의 문지기라면, [[163_optimizer_sql_execution_plan_generator|옵티마이저]]는 실행 [[268_strategy_pattern|전략]]의 설계자다.

- **📢 섹션 요약 비유**: 파스 트리는 원본 지도, AST는 중요한 길만 남긴 약도, [[166_execution_plan_optimizer_navigation_tree|실행 계획]]은 실제 여행 경로다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 파서가 [[604_sql_injection|SQL injection]] (SQL 삽입 공격) 방어, 에러 리포트, [[298_qkv_attention|쿼리]] 리라이트, 캐시 처리의 기초가 된다. 문법 오류를 정확히 잡을수록 사용자 경험이 좋아진다.

### [[435_checklist_based_testing|체크리스트]]

1. 문법 오류를 파스 트리 단계에서 잡는가?
2. AST와 파스 트리를 구분해 설명할 수 있는가?
3. 의미 분석에서 [[005_schema|스키마]]와 타입을 검사하는가?
4. [[166_execution_plan_optimizer_navigation_tree|실행 계획]]까지 연계해 최적화를 설명하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 파스 트리와 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 같은 것으로 보는 경우
- 문법 오류와 의미 오류를 구분하지 않는 경우
- [[502_dbms|DBMS]] 내부 단계를 한 덩어리로만 설명하는 경우

기술사 관점에서는 파서가 단순 문장 분해가 아니라, DBMS의 안전성과 최적화의 첫 관문이라는 점을 강조해야 한다.

- **📢 섹션 요약 비유**: 파서는 식당 주문을 받는 직원이고, 파스 트리는 주문서를 정리한 종이 묶음이다.

---

## Ⅴ. 기대효과 및 결론

파서와 파스 트리는 SQL 처리의 출발점이다. 문법을 정확히 구조화해야 이후 최적화와 실행이 제대로 돌아간다.

정리하면, SQL이 "문장"에서 "실행 가능한 구조"로 바뀌는 첫 변환 단계가 파서다.

- **📢 섹션 요약 비유**: 파서와 파스 트리는 레고 설명서를 따라 블록을 조립하는 첫 단계다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Lexer | [[820_tokenization|토큰화]] |
| Parse Tree | 문법 구조 |
| AST | 의미 구조 |
| Query Plan | 실행 구조 |
| [[088_optimizer|Optimizer]] | 계획 선택 |

### 📈 관련 키워드 및 발전 흐름도

```text
SQL 문장
    │
    ▼
토큰화 (Lexer)
    │
    ▼
파스 트리 (Parser)
    │
    ▼
AST / 의미 분석
    │
    ▼
실행 계획 / 실행기
```

이 흐름은 사람이 읽는 SQL이 [[502_dbms|DBMS]] 내부에서 실행 가능한 구조로 바뀌는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 파서는 문장을 읽고 순서를 맞게 썼는지 [[396_validation|확인]]해요.
2. 맞게 쓰면 나무처럼 가지를 뻗은 그림으로 바꿔요.
3. 그 다음에야 실제로 일을 하게 시켜요.
