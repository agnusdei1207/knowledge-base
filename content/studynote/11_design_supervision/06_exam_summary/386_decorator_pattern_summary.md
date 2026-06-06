---
title: "Decorator Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))은 객체를 감싸며 기능을 동적으로 추가해 책임을 조합하는 구조 패턴이다.
> 2. **가치**: 조합 가능한 부가 기능을 런타임에 유연하게 붙일 수 있다.
> 3. **판단 포인트**: [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 대체 수단이지만 순서 의존성과 투명성을 함께 점검해야 한다.

---

## Ⅰ. 개요 및 필요성

[데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))은 객체를 감싸며 기능을 동적으로 추가해 책임을 조합하는 구조 패턴이다. [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)만으로 기능 조합을 표현하면 조합 수만큼 하위 클래스가 늘어나는 문제가 생긴다. 이 개념이 필요한 이유는 기본 기능 위에 부가 책임을 유연하게 쌓는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 기능 추가 조합마다 새로운 클래스를 만들어야 해 구조가 비대해진다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
| Variation  |--->|   Decor    |--->|   Reuse    |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 공구함에서 맞는 도구를 고르지 못하면 같은 작업도 매번 힘으로 밀어붙이게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))의 핵심 원리는 "기본 기능 위에 부가 책임을 유연하게 쌓는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 동일 인터페이스를 구현하는 장식 객체가 실제 객체를 감싸고 호출 전후로 책임을 추가한다. 동시에 장식 계층이 깊어지면 디버깅과 순서 추적이 어려워질 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 기본 기능 위에 부가 책임을 유연하게 쌓는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 동일 인터페이스를 구현하는 장식 객체가 실제 객체를 감싸고 호출 전후로 책임을 추가한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 장식 계층이 깊어지면 디버깅과 순서 추적이 어려워질 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Client  |--->|  Decor   |--->|  Object  |--->|  Result  |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 조립식 부품처럼 협력 관계가 정리되면 기능을 더해도 기본 골격은 유지된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **패턴 적용 상태** 와 **즉흥 구현 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 패턴 적용 상태는 기본 기능 위에 부가 책임을 유연하게 쌓는 일에 맞춰 영향 범위를 줄인다 | 즉흥 구현 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 패턴 적용 상태는 동일 인터페이스를 구현하는 장식 객체가 실제 객체를 감싸고 호출 전후로 책임을 추가한다 | 즉흥 구현 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 패턴 적용 상태는 조합 가능한 부가 기능을 런타임에 유연하게 붙일 수 있다 | 즉흥 구현 상태는 기능 추가 조합마다 새로운 클래스를 만들어야 해 구조가 비대해진다 |

연결 개념으로는 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 대체, AOP 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 즉흥 수리를 비교하면 패턴이 줄이는 복잡도가 분명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))을 무조건 채택하기보다 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 대체 수단이지만 순서 의존성과 투명성을 함께 점검해야 한다. 아래 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 반복되는 변화 축이 실제로 존재하는가?
2. 패턴이 줄이는 복잡도보다 추가 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용이 작은가?
3. 클라이언트가 다시 구체 구현에 묶이지 않는가?
4. 테스트와 디버깅 관점에서 협력 구조를 설명할 수 있는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 작업 전 안전 점검표처럼, 변화 축이 실제로 있는지 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))의 기대효과는 분명하다. 조합 가능한 부가 기능을 런타임에 유연하게 붙일 수 있다. 다만 장식 계층이 깊어지면 디버깅과 순서 추적이 어려워질 수 있다. 결국 기억할 관점은 기본 기능 위에 부가 책임을 유연하게 쌓는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 현장 표준 공법서처럼, 패턴은 이름보다 어떤 문제를 반복해서 줄여 주는지가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 대체 | [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| AOP | [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| I/O 스트림 | [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 책임 조합 | [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[상속 기반 기능 추가] -> [데코레이터 패턴] -> [런타임 책임 조합]

### 👶 어린이를 위한 3줄 비유 설명
1. [데코레이터 패턴](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/))은 기본 케이크 위에 크림과 과일을 원하는 만큼 올리는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 기본 기능 위에 부가 책임을 유연하게 쌓는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 464 / 530

<- **이전**: [385. 컴포지트 패턴 (Composite Pattern)](/studynote/11_design_supervision/06_exam_summary/385_composite_pattern_summary/)
**다음**: [387. 퍼사드 패턴 (Facade Pattern)](/studynote/11_design_supervision/06_exam_summary/387_facade_pattern_summary/) ->

---
