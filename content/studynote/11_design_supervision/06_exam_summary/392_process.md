---
title: 392. 템플릿 메서드 패턴 (Template Method Pattern)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])은 [[001_algorithm_definition|알고리즘]]의 뼈대를 상위 클래스에 두고 세부 단계를 하위 클래스가 재정의하게 하는 행동 패턴이다.
> 2. **가치**: 공통 절차 재사용과 순서 [[194_consistency_database_integrity|일관성]] 유지에 유리하다.
> 3. **판단 포인트**: [[269_template_method_pattern|템플릿 메서드]]는 [[234_uml_class_relationships_generalization_dependency|상속]] 기반 재사용이며, 조합 기반 [[391_strategy_pattern_summary|전략 패턴]]과의 차이를 같이 설명하면 좋다.

---

## Ⅰ. 개요 및 필요성

[[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])은 [[001_algorithm_definition|알고리즘]]의 뼈대를 상위 클래스에 두고 세부 단계를 하위 클래스가 재정의하게 하는 행동 패턴이다. 처리 순서는 같지만 일부 단계만 달라지는 로직을 매번 복사하면 중복과 순서 오류가 늘어난다. 이 개념이 필요한 이유는 고정된 처리 순서와 변경 가능한 단계를 구분하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 공통 순서가 여러 구현에서 조금씩 달라져 버그와 규칙 불일치가 생긴다.

아래 그림은 왜 이 주제가 “문제 인식 → 설계 규칙 → 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
┌────────────┐   ┌────────────┐   ┌────────────┐
│ Variation  │──▶│    Tmpl    │──▶│   Reuse    │
└────────────┘   └────────────┘   └────────────┘
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 공구함에서 맞는 도구를 고르지 못하면 같은 작업도 매번 힘으로 밀어붙이게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])의 핵심 원리는 "고정된 처리 순서와 변경 가능한 단계를 구분하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 상위 클래스가 [[001_algorithm_definition|알고리즘]] 흐름을 [[269_template_method_pattern|템플릿 메서드]]로 정의하고, 훅 메서드나 추상 메서드로 변동 단계를 열어 둔다. 동시에 [[234_uml_class_relationships_generalization_dependency|상속]] 기반이라 런타임 조합 유연성이 낮고, 계층이 깊어지면 이해가 어려워질 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 고정된 처리 순서와 변경 가능한 단계를 구분하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 상위 클래스가 [[001_algorithm_definition|알고리즘]] 흐름을 [[269_template_method_pattern|템플릿 메서드]]로 정의하고, 훅 메서드나 추상 메서드로 변동 단계를 열어 둔다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | [[234_uml_class_relationships_generalization_dependency|상속]] 기반이라 런타임 조합 유연성이 낮고, 계층이 깊어지면 이해가 어려워질 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Client  │──▶│   Tmpl   │──▶│  Object  │──▶│  Result  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [[346_maintainability_portability|유지보수성]], 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 조립식 부품처럼 협력 관계가 정리되면 기능을 더해도 기본 골격은 유지된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **패턴 적용 상태** 와 **즉흥 구현 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 패턴 적용 상태는 고정된 처리 순서와 변경 가능한 단계를 구분하는 일에 맞춰 영향 범위를 줄인다 | 즉흥 구현 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 패턴 적용 상태는 상위 클래스가 [[001_algorithm_definition|알고리즘]] 흐름을 [[269_template_method_pattern|템플릿 메서드]]로 정의하고, 훅 메서드나 추상 메서드로 변동 단계를 열어 둔다 | 즉흥 구현 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 패턴 적용 상태는 공통 절차 재사용과 순서 [[194_consistency_database_integrity|일관성]] 유지에 유리하다 | 즉흥 구현 상태는 공통 순서가 여러 구현에서 조금씩 달라져 버그와 규칙 불일치가 생긴다 |

연결 개념으로는 [[234_uml_class_relationships_generalization_dependency|상속]], 훅 메서드 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 즉흥 수리를 비교하면 패턴이 줄이는 복잡도가 분명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])을 무조건 채택하기보다 [[269_template_method_pattern|템플릿 메서드]]는 [[234_uml_class_relationships_generalization_dependency|상속]] 기반 재사용이며, 조합 기반 [[391_strategy_pattern_summary|전략 패턴]]과의 차이를 같이 설명하면 좋다. 아래 [[435_checklist_based_testing|체크리스트]]는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 반복되는 변화 축이 실제로 존재하는가?
2. 패턴이 줄이는 복잡도보다 추가 [[198_abstraction_control_data_process|추상화]] 비용이 작은가?
3. 클라이언트가 다시 구체 구현에 묶이지 않는가?
4. 테스트와 디버깅 관점에서 협력 구조를 설명할 수 있는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 작업 전 안전 점검표처럼, 변화 축이 실제로 있는지 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])의 기대효과는 분명하다. 공통 절차 재사용과 순서 [[194_consistency_database_integrity|일관성]] 유지에 유리하다. 다만 [[234_uml_class_relationships_generalization_dependency|상속]] 기반이라 런타임 조합 유연성이 낮고, 계층이 깊어지면 이해가 어려워질 수 있다. 결국 기억할 관점은 고정된 처리 순서와 변경 가능한 단계를 구분하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 현장 표준 공법서처럼, 패턴은 이름보다 어떤 문제를 반복해서 줄여 주는지가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[234_uml_class_relationships_generalization_dependency|상속]] | [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| 훅 메서드 | [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| [[391_strategy_pattern_summary|전략 패턴]] | [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])을 설계하고 감리할 때 함께 보는 연관 개념 |
| DRY | [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[절차 복사 구현] → [템플릿 메서드] → [공통 뼈대 재사용]

### 👶 어린이를 위한 3줄 비유 설명
1. [[269_template_method_pattern|템플릿 메서드]] 패턴 ([[269_template_method_pattern|Template Method Pattern]])은 요리 레시피는 같고 마지막 양념만 집마다 다르게 넣는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 고정된 처리 순서와 변경 가능한 단계를 구분하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 470 / 530

← **이전**: [[391_strategy_pattern_summary|391. 전략 패턴 (Strategy Pattern)]]
**다음**: [[393_undo|393. 커맨드 패턴과 실행 취소 (Command Pattern and Undo)]] →

---
