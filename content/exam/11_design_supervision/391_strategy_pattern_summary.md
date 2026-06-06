---
title: "Strategy Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))은 교체 가능한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 캡슐화해 런타임에 선택하도록 만드는 행동 패턴이다.
> 2. **가치**: [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 확장과 테스트 분리를 쉽게 한다.
> 3. **판단 포인트**: [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴은 단순 if 제거가 아니라 변화 축을 객체로 승격하는 설계라는 점을 강조해야 한다.

---

## Ⅰ. 개요 및 필요성

[전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))은 교체 가능한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 캡슐화해 런타임에 선택하도록 만드는 행동 패턴이다. 조건문으로 정렬, 할인, [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 규칙을 계속 늘리면 한 클래스에 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 분기가 과도하게 쌓인다. 이 개념이 필요한 이유는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변화를 독립 교체 가능하게 만드는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 새 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 추가마다 조건문이 길어지고 기존 코드 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 범위도 함께 커진다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
| Variation  |--->|  Strateg   |--->|   Reuse    |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 공구함에서 맞는 도구를 고르지 못하면 같은 작업도 매번 힘으로 밀어붙이게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))의 핵심 원리는 "[알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변화를 독립 교체 가능하게 만드는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 공통 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인터페이스를 두고 컨텍스트가 상황에 맞는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체를 선택해 위임한다. 동시에 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수가 많아질수록 선택 규칙 관리가 또 다른 복잡도가 될 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변화를 독립 교체 가능하게 만드는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 공통 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인터페이스를 두고 컨텍스트가 상황에 맞는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체를 선택해 위임한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수가 많아질수록 선택 규칙 관리가 또 다른 복잡도가 될 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Client  |--->| Strateg  |--->|  Object  |--->|  Result  |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 조립식 부품처럼 협력 관계가 정리되면 기능을 더해도 기본 골격은 유지된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **패턴 적용 상태** 와 **즉흥 구현 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 패턴 적용 상태는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변화를 독립 교체 가능하게 만드는 일에 맞춰 영향 범위를 줄인다 | 즉흥 구현 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 패턴 적용 상태는 공통 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 인터페이스를 두고 컨텍스트가 상황에 맞는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체를 선택해 위임한다 | 즉흥 구현 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 패턴 적용 상태는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 확장과 테스트 분리를 쉽게 한다 | 즉흥 구현 상태는 새 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 추가마다 조건문이 길어지고 기존 코드 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 범위도 함께 커진다 |

연결 개념으로는 [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/), [의존성 주입](/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 즉흥 수리를 비교하면 패턴이 줄이는 복잡도가 분명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 무조건 채택하기보다 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴은 단순 if 제거가 아니라 변화 축을 객체로 승격하는 설계라는 점을 강조해야 한다. 아래 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 반복되는 변화 축이 실제로 존재하는가?
2. 패턴이 줄이는 복잡도보다 추가 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용이 작은가?
3. 클라이언트가 다시 구체 구현에 묶이지 않는가?
4. 테스트와 디버깅 관점에서 협력 구조를 설명할 수 있는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 작업 전 안전 점검표처럼, 변화 축이 실제로 있는지 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))의 기대효과는 분명하다. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 확장과 테스트 분리를 쉽게 한다. 다만 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수가 많아질수록 선택 규칙 관리가 또 다른 복잡도가 될 수 있다. 결국 기억할 관점은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변화를 독립 교체 가능하게 만드는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 현장 표준 공법서처럼, 패턴은 이름보다 어떤 문제를 반복해서 줄여 주는지가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [의존성 주입](/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 객체 | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택기 | [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[조건문 분기] -> [전략 패턴] -> [정책 객체 교체]

### 👶 어린이를 위한 3줄 비유 설명
1. [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴 ([Strategy Pattern](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))은 같은 게임도 공격법 카드를 바꿔 끼우며 다르게 플레이하는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변화를 독립 교체 가능하게 만드는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 469 / 530

<- **이전**: [390. 옵저버 패턴 (Observer Pattern)](/studynote/11_design_supervision/06_exam_summary/390_observer_pattern_summary/)
**다음**: [392. 템플릿 메서드 패턴 (Template Method Pattern)](/studynote/11_design_supervision/06_exam_summary/392_process/) ->

---
