---
sidebar:
  order: 34
  label: "034. XP: 페어 프로그래밍•TDD (Extreme Programming)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "XP: 페어 프로그래밍•TDD (Extreme Programming)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Extreme Programming (XP)**: 1~2주 단위의 빠른 피드백, 개발자 간의 긴밀한 소통, 그리고 12가지 공학적 실천법(Practices)을 극단적으로 강조하여 소규모 팀의 생산성과 소프트웨어 품질을 극대화하는 애자일 방법론.
- **Pair Programming (짝 프로그래밍)**: 2명의 개발자가 1대의 모니터/키보드를 공유하며, 코드를 직접 작성하는 Driver와 객관적 검토 및 아키텍처를 제시하는 Navigator로 역할을 나누어 개발하는 실천법.
- **TDD (Test-Driven Development)**: 코드 작성 전 실패하는 단위 테스트(Red)를 먼저 만들고, 이를 통과하는 최소한의 구현 코드(Green)를 작성한 뒤, 리팩토링(Refactor)하는 3단계 개발 방법론.

</details>

- 정의/개념: 고객 참여와 12가지 양질의 공학적 실천법(Practices)을 극단적(Extreme)으로 실천하여 소프트웨어 품질 및 대응 민첩성을 최고조로 올리는 애자일 개발 프레임워크인 **XP (Extreme Programming)**
- 배경/필요성: 기존 방법론의 구두 테스트 및 사후 테스트로 인한 엄청난 재작업 비용 극복, 지속적 통합(CI) 및 개발자 중심 품질 내재화 요구성

#### 한줄 요약

- XP는 작은 변경과 공학 실천으로 빠른 피드백을 만든다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **5대 핵심 가치**: 의사소통(Communication), 단순성(Simplicity), 피드백(Feedback), 용기(Courage), 존중(Respect).
- **Collective Code Ownership (공동 코드 소유)**: 모든 코드에 대한 수정 및 리팩토링 권한을 특정 개인이 아닌 전체 개발자 팀원 모두가 보유한다는 원칙.

</details>

- 5대 핵심 가치 (**Communication, Simplicity, Feedback, Courage, Respect**)
- **개발자 중심의 12가지 공학적 실천법 (Core Practices)** 전면 집행
- **Pair Programming**을 통한 실시간 코드 리뷰 및 **Collective Code Ownership**

#### 한줄 요약

- 사용자 스토리, TDD, 페어 프로그래밍, 지속 통합의 결합이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Refactoring (리팩토링)**: 외부 동작 인터페이스(Behavior)는 유지한 채, 내부 코드의 가독성 및 아키텍처 구조를 지속적으로 개선하여 기술 부채를 소멸시키는 행위.

</details>

```text
                     [TDD•자동 테스트]
                      /              \
               [개발 페어] -- [리팩터링] -- [지속 통합]
```

선의 의미: Pair가 TDD 방식으로 실패 테스트를 만든 후 코딩하고, Refactoring을 통해 코드를 정제한 후 CI 빌드 서버에 통합하는 일련의 릴리스 루프.

| 12가지 실천법 분류 | 구체적 XP 실천법 (Practices) | 핵심 정의 및 내용 |
|:---|:---|:---|
| **개발자 실천법 (Dev)** | **Test-Driven Development (TDD)** | 실패하는 테스트 선작성 후 구현 및 리팩토링 |
| | **Pair Programming** | 2인 1조 (Driver + Navigator) 실시간 페어 개발 |
| | **Refactoring** | 가독성/성능 향상을 위한 지속적 코드 내부 구조 개선 |
| | **Collective Code Ownership** | 모든 팀원이 전체 코드를 자유롭게 수정할 권한과 책임 보유 |
| | **Continuous Integration (CI)** | 하루에 수차례 이상 공유 메인라인 서버에 코드 통합/빌드 |
| | **Coding Standard** | 팀 전체가 통일된 가독성 코딩 규칙 수용 |
| **고객/관리 실천법** | **Planning Game** | 사용자 스토리 카드 기반 우선순위 및 이터레이션 계획 수립 |
| | **Small Releases** | 짧은 주기(1~2주)로 작동하는 기능 조기 릴리스 |
| | **On-site Customer** | 상주 고객이 곁에서 요구사항 즉시 해석 및 판단 지원 |
| | **Metaphor** | 프로젝트 전체 구조를 쉽게 이해 가능한 비유로 공유 |
| | **Sustainable Pace (40-Hour Week)**| 과도한 야근을 금지하여 지속 가능한 개발자 생산성 유지 |

#### 한줄 요약

- 드라이버, 내비게이터, 리팩터링이 개발과 검토를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

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

<details><summary>핵심 용어</summary>

- **Scrum vs XP**: Scrum은 관리/절차적 프레임워크(역할, 이벤트, 아티팩트)인 반면, XP는 기술/공학적 개발 실천법(TDD, Pair, Refactoring, CI) 위주.

</details>

| 비교 항목 | XP (Extreme Programming) | Scrum (스크럼) |
|:---|:---|:---|
| 핵심 강조점 | **엔지니어링 공학 실천법 (TDD, Pair, CI)** | **조직 관리 및 프로세스 프레임워크 (3-5-3)** |
| 이터레이션 주기 | 1~2주 (매우 짧음) | 2~4주 |
| 개발 중 변경 | 이터레이션 내부에서 요구 변경 허용성 높음 | 스프린트 기간 중 백로그 변경 원칙적 거부 |
| 개발자 롤 | 명확한 전용 롤 없음 (팀원 전원) | PO, SM, Devs 롤 엄격 정의 |

#### 한줄 요약

- 잦은 변경은 XP, 안정 요구•승인은 단계 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Pair Fatigue (페어 피로도)**: 하루 종일 2인이 모니터를 마주보며 지속적 소통을 수행할 때 누적되는 정신적/체력적 피로감.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Pair Programming으로 인한 개발자의 정신적 피로 폭증 (**Pair Fatigue**) | 하루 3~4시간으로 페어 시간 제한 및 개인 작업 시간 보장 | 개발 지속성 및 생산성 균형 |
| TDD 도입 초기의 코드 작성 속도 저하 반발 | 단위 테스트 작성 문화 정착 및 자동화 툴 지원 | 장기적 버그 리셋 및 유지보수성 획득 |
| 상주 고객(On-site Customer) 확보 어려움 | PO 또는 도메인 분석가가 On-site Customer 역할 수행 | 요구사항 즉각 해석 가용성 확보 |

> 사례: **TDD + Pair Programming + CI/CD (GitHub Actions)** 조합의 현대적 DevOps 문화 접목

#### 한줄 요약

- 테스트 피라미드, 필수 검증 분리, 특성 테스트로 작은 변경을 보호한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **XP 실천법 정착 기준(XP Practices Adoption Criteria)**: 코드 품질 수준, 자동화 테스트 커버리지 및 팀의 TDD 숙련도에 의거한 체계.

</details>

- **XP 실천법 정착 기준**에 따라 애자일 구현 시 **Scrum (관리 프레임워크) + XP (공학 실천법: TDD/Pair)** 혼합 모델 채택

#### 한줄 요약

- 변경 빈도•자동화 가능성•단계 승인 요구를 함께 평가하는 것이 핵심이다.
