---
title: 126. BDD (Behavior-Driven Development) - Given/When/Then 행위 기반 개발
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BDD는 **비즈니스 요구사항을 Given(전제)·When(행동)·Then(결과) 형식의 시나리오로 작성**하고, 이 시나리오가 곧 자동화 테스트가 되는 개발 방법론이다.
> 2. **가치**: TDD가 개발자 관점의 [[397_unit_test|단위 테스트]] 중심이라면, BDD는 **비즈니스 [[173_stakeholder_identification_impact_matrix|이해관계자]](PO·QA)도 읽고 검증할 수 있는 자연어 시나리오**로 요구사항과 테스트의 일치를 보장한다.
> 3. **판단 포인트**: Gherkin 문법(Given/When/Then)으로 시나리오를 작성하고, Cucumber·Behave 등 도구가 이를 자동화 테스트로 실행한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    BDD 시나리오 예시                                  │
├───────────────────────────────────────────────────────┤
│  Feature: 로그인                                      │
│                                                       │
│  Scenario: 올바른 비밀번호로 로그인                   │
│    Given 사용자 "홍길동"이 등록되어 있다              │
│    When 아이디 "hong"과 비밀번호 "1234"로 로그인     │
│    Then 대시보드 페이지가 표시된다                    │
│                                                       │
│  Scenario: 잘못된 비밀번호                            │
│    Given 사용자 "홍길동"이 등록되어 있다              │
│    When 아이디 "hong"과 비밀번호 "wrong"으로 로그인  │
│    Then "비밀번호가 틀립니다" 메시지가 표시된다       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: BDD는 연극의 **대본(시나리오)**이다. 감독(PO)·배우(개발자)·관객(QA) 모두가 같은 대본을 보고 연습(테스트)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[164_tdd_test_driven_development|TDD]] vs [[165_bdd_behavior_driven_development|BDD]]

| 비교 | [[164_tdd_test_driven_development|TDD]] | [[165_bdd_behavior_driven_development|BDD]] |
|:---|:---|:---|
| **관점** | 개발자 | **비즈니스 + 개발자** |
| **언어** | 코드 | **자연어 (Gherkin)** |
| **범위** | [[397_unit_test|단위 테스트]] | **[[406_acceptance_test_uat|인수 테스트]]** |
| **도구** | JUnit, pytest | **Cucumber, Behave** |

- **📢 섹션 요약 비유**: TDD는 부품 검사(단위), BDD는 완성차 시승(인수)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수동 [[406_acceptance_test_uat|인수 테스트]] | [[165_bdd_behavior_driven_development|BDD]] |
|:---|:---|:---|
| **문서** | 엑셀 | **실행 가능 시나리오** |
| **자동화** | 불가 | **자동 실행** |
| **유지보수** | 문서 갱신 누락 | **코드와 [[212_synchronization_mechanisms|동기화]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[165_bdd_behavior_driven_development|BDD]] 도구
- **Cucumber** (Java/Ruby): [[165_bdd_behavior_driven_development|BDD]] 대표.
- **Behave** (Python): Python [[165_bdd_behavior_driven_development|BDD]].
- **SpecFlow** (.NET): C# [[165_bdd_behavior_driven_development|BDD]].

---

## Ⅴ. 기대효과 및 결론

BDD는 **"살아있는 문서(Living [[378_software_documentation|Documentation]])"**를 통해 요구사항·테스트·코드의 일치를 보장하는 [[004_agile_relation|Agile]] 개발의 핵심 실천이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Given/When/Then** | [[165_bdd_behavior_driven_development|BDD]] 시나리오 문법 |
| **Gherkin** | [[165_bdd_behavior_driven_development|BDD]] 시나리오 언어 |
| **Cucumber** | [[165_bdd_behavior_driven_development|BDD]] 자동화 도구 |
| **[[164_tdd_test_driven_development|TDD]]** | BDD의 기반 (코드 레벨) |
| **[[710_atdd_acceptance_test_driven_development|ATDD]]** | 인수 [[077_tdd_test_driven_development|테스트 주도 개발]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[TDD (Kent Beck, 2003)]
    │
    ▼
[BDD (Dan North, 2006) — Given/When/Then]
    │
    ▼
[Cucumber (2008) — BDD 자동화 대표]
    │
    ▼
[Living Documentation (2015~)]
    │
    ▼
[현재: AI BDD — 자연어 요구사항 → 자동 시나리오 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BDD는 연극 **대본(시나리오)**이에요. "만약 이러면, 이렇게 하면, 이런 결과가 나와야 해!"
2. 감독(PO)·배우(개발자)·관객(QA) **모두가 같은 대본**을 보고 이해해요.
3. 대본대로 연습(테스트)하면 **진짜 공연(배포) 때 실수가 없어요!**
