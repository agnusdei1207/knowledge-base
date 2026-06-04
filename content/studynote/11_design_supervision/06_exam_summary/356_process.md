+++
title = "356. 개방-폐쇄 원칙 (Open-Closed Principle, OCP)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))은 기존 코드를 크게 수정하지 않고 확장으로 기능을 더하게 만드는 설계 원칙이다.
> 2. **가치**: 기존 안정 영역을 보존한 채 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 다양성을 수용하게 해 준다.
> 3. **판단 포인트**: 무조건 인터페이스를 만들기보다 반복될 변화 축이 실제로 존재하는지 확인한 뒤 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))은 기존 코드를 크게 수정하지 않고 확장으로 기능을 더하게 만드는 설계 원칙이다. 신규 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 들어올 때마다 조건문을 덧붙이면 안정된 코드까지 매번 건드리게 된다. 이 개념이 필요한 이유는 변화를 수정이 아니라 확장 지점으로 수용하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 새 기능 한 줄이 검증된 영역까지 흔들어 회귀 위험을 키운다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
|   Change   |--->|    OCP     |--->|   Stable   |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 서랍을 용도별로 나누지 않으면 필요한 물건을 찾을 때마다 전체를 뒤집어야 하는 상황과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))의 핵심 원리는 "변화를 수정이 아니라 확장 지점으로 수용하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/), [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체, 플러그인 지점을 두어 새로운 구현을 끼워 넣는 방식으로 설계한다. 동시에 확장 가능성을 과하게 앞당겨 설계하면 현재 요구보다 복잡한 골격만 남을 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 변화를 수정이 아니라 확장 지점으로 수용하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/), [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체, 플러그인 지점을 두어 새로운 구현을 끼워 넣는 방식으로 설계한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 확장 가능성을 과하게 앞당겨 설계하면 현재 요구보다 복잡한 골격만 남을 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Reason  |--->| Boundary |--->|   OCP    |--->|   Test   |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 톱니가 맞게 설계된 기어처럼, 책임과 의존이 맞물려야 힘이 새지 않는다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **원칙 준수 구조** 와 **원칙 무시 구조** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 원칙 준수 구조는 변화를 수정이 아니라 확장 지점으로 수용하는 일에 맞춰 영향 범위를 줄인다 | 원칙 무시 구조는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 원칙 준수 구조는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/), [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체, 플러그인 지점을 두어 새로운 구현을 끼워 넣는 방식으로 설계한다 | 원칙 무시 구조는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 원칙 준수 구조는 기존 안정 영역을 보존한 채 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 다양성을 수용하게 해 준다 | 원칙 무시 구조는 새 기능 한 줄이 검증된 영역까지 흔들어 회귀 위험을 키운다 |

연결 개념으로는 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/), 플러그인 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 만능 공구를 비교해 보는 순간 어떤 문제가 줄어드는지가 선명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 무조건 채택하기보다 무조건 인터페이스를 만들기보다 반복될 변화 축이 실제로 존재하는지 확인한 뒤 적용해야 한다. 아래 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 변경 이유를 한 문장으로 설명할 수 있는가?
2. 공개 인터페이스가 실제 책임보다 넓지 않은가?
3. 숨은 결합 없이 단위 테스트가 가능한가?
4. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 추가 비용이 얻는 안정성보다 크지 않은가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 출항 전 점검표처럼, 적용 조건을 확인해야 원칙이 장식이 아니라 안전장치가 된다.

---

## Ⅴ. 기대효과 및 결론

개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))의 기대효과는 분명하다. 기존 안정 영역을 보존한 채 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 다양성을 수용하게 해 준다. 다만 확장 가능성을 과하게 앞당겨 설계하면 현재 요구보다 복잡한 골격만 남을 수 있다. 결국 기억할 관점은 변화를 수정이 아니라 확장 지점으로 수용하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 반복해서 꺼내 보는 사용 설명서처럼, 오래 갈 설계일수록 핵심 규칙이 짧고 분명해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) | 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 플러그인 | 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) | 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/) | 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[조건문 확장] -> OCP 적용] -> [플러그인/[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 구조]

### 👶 어린이를 위한 3줄 비유 설명
1. 개방-폐쇄 원칙 ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/))은 새 레일만 끼우면 장난감 기차가 더 달릴 수 있는 트랙처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 변화를 수정이 아니라 확장 지점으로 수용하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 434 / 530

<- **이전**: [355. 단일 책임 원칙 (Single Responsibility Principle, SRP)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/355_process/)
**다음**: [357. 리스코프 치환 원칙 (Liskov Substitution Principle, LSP)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/357_process/) ->

---
