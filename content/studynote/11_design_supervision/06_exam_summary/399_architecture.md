---
title: "Visitor Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))은 객체 구조는 유지한 채 새로운 연산을 외부 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)로 추가하는 행동 패턴이다.
> 2. **가치**: 구조를 건드리지 않고 다양한 연산을 추가하게 해 준다.
> 3. **판단 포인트**: [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)는 연산 추가가 빈번하고 구조는 안정적인 경우에 적합하다는 조건을 명확히 해야 한다.

---

## Ⅰ. 개요 및 필요성

[방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))은 객체 구조는 유지한 채 새로운 연산을 외부 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)로 추가하는 행동 패턴이다. 안정된 객체 구조 위에 보고서, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 변환 같은 새 기능이 자주 붙는 경우 구조 변경 없이 확장을 원한다. 이 개념이 필요한 이유는 구조와 연산의 변화 축을 분리하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 새 연산마다 객체 구조 클래스를 계속 수정해 안정된 모델까지 흔들리게 된다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
| Variation  |--->|   Visit    |--->|   Reuse    |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 공구함에서 맞는 도구를 고르지 못하면 같은 작업도 매번 힘으로 밀어붙이게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))의 핵심 원리는 "구조와 연산의 변화 축을 분리하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 요소가 accept를 제공하고 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)가 각 구체 요소별 visit 메서드로 이중 디스패치를 수행한다. 동시에 요소 타입 추가가 잦다면 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 인터페이스 수정 비용이 커져 오히려 불리하다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 구조와 연산의 변화 축을 분리하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 요소가 accept를 제공하고 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)가 각 구체 요소별 visit 메서드로 이중 디스패치를 수행한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 요소 타입 추가가 잦다면 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 인터페이스 수정 비용이 커져 오히려 불리하다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Client  |--->|  Visit   |--->|  Object  |--->|  Result  |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 조립식 부품처럼 협력 관계가 정리되면 기능을 더해도 기본 골격은 유지된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **패턴 적용 상태** 와 **즉흥 구현 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 패턴 적용 상태는 구조와 연산의 변화 축을 분리하는 일에 맞춰 영향 범위를 줄인다 | 즉흥 구현 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 패턴 적용 상태는 요소가 accept를 제공하고 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)가 각 구체 요소별 visit 메서드로 이중 디스패치를 수행한다 | 즉흥 구현 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 패턴 적용 상태는 구조를 건드리지 않고 다양한 연산을 추가하게 해 준다 | 즉흥 구현 상태는 새 연산마다 객체 구조 클래스를 계속 수정해 안정된 모델까지 흔들리게 된다 |

연결 개념으로는 이중 디스패치, 컴파일러 AST 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 즉흥 수리를 비교하면 패턴이 줄이는 복잡도가 분명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))을 무조건 채택하기보다 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/)는 연산 추가가 빈번하고 구조는 안정적인 경우에 적합하다는 조건을 명확히 해야 한다. 아래 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 반복되는 변화 축이 실제로 존재하는가?
2. 패턴이 줄이는 복잡도보다 추가 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용이 작은가?
3. 클라이언트가 다시 구체 구현에 묶이지 않는가?
4. 테스트와 디버깅 관점에서 협력 구조를 설명할 수 있는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 작업 전 안전 점검표처럼, 변화 축이 실제로 있는지 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))의 기대효과는 분명하다. 구조를 건드리지 않고 다양한 연산을 추가하게 해 준다. 다만 요소 타입 추가가 잦다면 [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 인터페이스 수정 비용이 커져 오히려 불리하다. 결국 기억할 관점은 구조와 연산의 변화 축을 분리하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 현장 표준 공법서처럼, 패턴은 이름보다 어떤 문제를 반복해서 줄여 주는지가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 이중 디스패치 | [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 컴파일러 AST | [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 오픈-클로즈드 | [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 리포트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[구조 클래스 직접 수정] -> [방문자 패턴] -> [연산 외부 확장]

### 👶 어린이를 위한 3줄 비유 설명
1. [방문자](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/) 패턴 ([Visitor Pattern](/studynote/04_software_engineering/05_devops_ci_cd/275_visitor_pattern/))은 전시품은 그대로 두고 해설사만 바꿔 여러 설명을 듣는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 구조와 연산의 변화 축을 분리하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 477 / 530

<- **이전**: [398. 메멘토 패턴 (Memento Pattern)](/studynote/11_design_supervision/06_exam_summary/398_process/)
**다음**: [400. 해석자 패턴 (Interpreter Pattern)](/studynote/11_design_supervision/06_exam_summary/400_process/) ->

---
