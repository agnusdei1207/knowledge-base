---
sidebar:
  order: 34
  label: "034. XP: 페어 프로그래밍•TDD (Extreme Programming)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "XP: 페어 프로그래밍•TDD (Extreme Programming)"
date: "2026-08-13T14:28:00+09:00"
tags:
  - "notes-software"
weight: 34
extra:
  question_no: "034"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "129회 기출, XP 실천법•피드백 주기"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Extreme Programming (XP)**: 1~2주 단위의 빠른 피드백, 개발자 간의 긴밀한 소통, 그리고 12가지 공학적 실천법(Practices)을 극단적으로 강조하여 소규모 팀의 생산성과 소프트웨어 품질을 극대화하는 애자일 방법론.
- **Pair Programming (짝 프로그래밍)**: 2명의 개발자가 1대의 모니터/키보드를 공유하며, 코드를 직접 작성하는 Driver와 객관적 검토 및 아키텍처를 제시하는 Navigator로 역할을 나누어 개발하는 실천법.
- **TDD (Test-Driven Development)**: 코드 작성 전 실패하는 단위 테스트(Red)를 먼저 만들고, 이를 통과하는 최소한의 구현 코드(Green)를 작성한 뒤, 리팩토링(Refactor)하는 3단계 개발 방법론.

</details>

- 정의/개념: 짧은 피드백과 공학 실천을 결합한 **XP(Extreme Programming)**
- 배경/필요성: 후행 테스트와 대규모 변경은 **결함 원인 추적•재작업 비용** 증가

#### 한줄 요약

- XP는 작은 변경과 공학 실천으로 빠른 피드백을 만든다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **5대 핵심 가치**: 의사소통(Communication), 단순성(Simplicity), 피드백(Feedback), 용기(Courage), 존중(Respect).
- **Collective Code Ownership (공동 코드 소유)**: 모든 코드에 대한 수정 및 리팩토링 권한을 특정 개인이 아닌 전체 개발자 팀원 모두가 보유한다는 원칙.

</details>

- 5대 핵심 가치 (**Communication, Simplicity, Feedback, Courage, Respect**)
- TDD•페어•리팩터링•CI 등 공학 실천의 상호 강화
- **Pair Programming**을 통한 실시간 코드 리뷰 및 **Collective Code Ownership**

#### 한줄 요약

- 사용자 스토리, TDD, 페어 프로그래밍, 지속 통합의 결합이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Refactoring (리팩토링)**: 외부 동작 인터페이스(Behavior)는 유지한 채, 내부 코드의 가독성 및 아키텍처 구조를 지속적으로 개선하여 기술 부채를 소멸시키는 행위.

</details>

```text
                     [TDD•자동 테스트]
                      /              \
               [개발 페어] -- [리팩터링] -- [지속 통합]
```

선의 의미: Pair가 TDD 방식으로 실패 테스트를 만든 후 코딩하고, Refactoring을 통해 코드를 정제한 후 CI 빌드 서버에 통합하는 일련의 릴리스 루프.

| 구성요소 | 책임 |
|:---|:---|
| TDD•자동 테스트 | 작은 동작 기준과 회귀 안전망 제공 |
| 개발 페어 | Driver•Navigator로 구현과 실시간 검토 수행 |
| 리팩터링 | 외부 동작을 유지하며 내부 구조 개선 |
| 지속 통합 | 작은 변경을 자주 병합하고 전체 검증 수행 |

#### 한줄 요약

- 드라이버, 내비게이터, 리팩터링이 개발과 검토를 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Red-Green-Refactor Loop**: TDD의 3단계 사이클로, 1단계: 실패하는 테스트 작성(Red), 2단계: 테스트 통과 코드 구현(Green), 3단계: 코드 정제(Refactor).

</details>

```text
┌──────────────────────────────┐
│ 사용자 스토리•수용 기준    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 실패 테스트 작성 (Red)   │
│ 2. 예상 실패 확인            │
│ 3. 최소 구현•통과 (Green)   │
│ 4. 리팩터링 (Refactor)       │
│ 5. 자동 회귀 검증•통합 (CI) │
└──────────────────────────────┘
```

### 동작 원리

1. **실패 테스트 작성 (Red)**: 사용자 스토리 수용 기준 기반 `assert` 실패 테스트 코드 선작성.
2. **예상 실패 확인**: 해당 테스트를 실행하여 명확한 오류 메세지 확인.
3. **최소 구현·통과 (Green)**: 테스트를 통과(Pass)할 수 있는 가장 단순한 최소 코드 기재.
4. **리팩터링 (Refactor)**: 중복 제거, 가독성 향상, 패턴 적용 등 코드를 클린하게 정제.
5. **자동 회귀 검증·통합 (CI)**: CI 서버(Jenkins/GitHub Actions)에 커밋하여 전체 회귀 테스트 자동 수행.

#### 한줄 요약

- 실패 테스트 작성부터 자동 회귀 검증•통합까지의 짧은 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Scrum vs XP**: Scrum은 관리/절차적 프레임워크(역할, 이벤트, 아티팩트)인 반면, XP는 기술/공학적 개발 실천법(TDD, Pair, Refactoring, CI) 위주.

</details>

| 비교 항목 | XP (Extreme Programming) | Scrum (스크럼) |
|:---|:---|:---|
| 핵심 강조점 | **엔지니어링 공학 실천법 (TDD, Pair, CI)** | **조직 관리 및 프로세스 프레임워크 (3-5-3)** |
| 반복 주기 | 짧은 릴리스와 지속 피드백 강조 | 한 달 이하 스프린트 |
| 개발 중 변경 | 작은 변경과 고객 피드백 반영 | 스프린트 목표를 해치지 않게 범위 조정 가능 |
| 책무 구조 | 공학 실천과 공동 코드 소유 강조 | PO•SM•Developers 책무 정의 |

#### 한줄 요약

- 잦은 변경은 XP, 안정 요구•승인은 단계 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Pair Fatigue (페어 피로도)**: 하루 종일 2인이 모니터를 마주보며 지속적 소통을 수행할 때 누적되는 정신적/체력적 피로감.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장시간 페어 작업에 따른 **Pair Fatigue** | 작업 난도에 따라 페어•개인 작업 시간 조정 | 검토 효과와 집중 시간 균형 |
| TDD 도입 초기의 코드 작성 속도 저하 반발 | 단위 테스트 작성 문화 정착 및 자동화 툴 지원 | 장기적 버그 리셋 및 유지보수성 획득 |
| 상주 고객(On-site Customer) 확보 어려움 | PO 또는 도메인 분석가가 On-site Customer 역할 수행 | 요구사항 즉각 해석 가용성 확보 |

> 사례: **TDD + Pair Programming + CI/CD (GitHub Actions)** 조합의 현대적 DevOps 문화 접목

#### 한줄 요약

- 테스트 피라미드, 필수 검증 분리, 특성 테스트로 작은 변경을 보호한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **XP 실천법 정착 기준(XP Practices Adoption Criteria)**: 코드 품질 수준, 자동화 테스트 커버리지 및 팀의 TDD 숙련도에 의거한 체계.

</details>

- **XP 실천법 정착 기준**에 따라 애자일 구현 시 **Scrum (관리 프레임워크) + XP (공학 실천법: TDD/Pair)** 혼합 모델 채택

#### 한줄 요약

- 변경 빈도•자동화 가능성•단계 승인 요구를 함께 평가하는 것이 핵심이다.
