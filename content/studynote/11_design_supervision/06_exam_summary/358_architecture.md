+++
title = "358. 인터페이스 분리 원칙 (Interface Segregation Principle, ISP)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))은 클라이언트가 사용하지 않는 메서드에 의존하지 않도록 인터페이스를 작게 나누는 설계 원칙이다.
> 2. **가치**: 의존성을 가볍게 만들고 구현 대체와 테스트 대역 작성을 쉽게 한다.
> 3. **판단 포인트**: 인터페이스 분리의 목적은 개수 늘리기가 아니라 클라이언트별 불필요 의존 제거임을 명확히 써야 한다.

---

## Ⅰ. 개요 및 필요성

인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))은 클라이언트가 사용하지 않는 메서드에 의존하지 않도록 인터페이스를 작게 나누는 설계 원칙이다. 거대한 인터페이스 하나에 모든 기능을 담으면 구현체와 호출자가 필요 이상의 약속을 떠안게 된다. 이 개념이 필요한 이유는 클라이언트별로 필요한 계약만 남기는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 미사용 메서드 변경이 여러 구현체와 테스트를 쓸데없이 흔든다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
|   Change   |--->|    ISP     |--->|   Stable   |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 서랍을 용도별로 나누지 않으면 필요한 물건을 찾을 때마다 전체를 뒤집어야 하는 상황과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))의 핵심 원리는 "클라이언트별로 필요한 계약만 남기는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 역할별 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 분리하고 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 조회/명령 같은 사용 문맥에 맞춰 인터페이스를 잘게 나눈다. 동시에 인터페이스를 지나치게 세분화하면 탐색성이 떨어지고 계약 수가 과도하게 늘 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 클라이언트별로 필요한 계약만 남기는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 역할별 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 분리하고 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 조회/명령 같은 사용 문맥에 맞춰 인터페이스를 잘게 나눈다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 인터페이스를 지나치게 세분화하면 탐색성이 떨어지고 계약 수가 과도하게 늘 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Reason  |--->| Boundary |--->|   ISP    |--->|   Test   |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 톱니가 맞게 설계된 기어처럼, 책임과 의존이 맞물려야 힘이 새지 않는다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **원칙 준수 구조** 와 **원칙 무시 구조** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 원칙 준수 구조는 클라이언트별로 필요한 계약만 남기는 일에 맞춰 영향 범위를 줄인다 | 원칙 무시 구조는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 원칙 준수 구조는 역할별 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 분리하고 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 조회/명령 같은 사용 문맥에 맞춰 인터페이스를 잘게 나눈다 | 원칙 무시 구조는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 원칙 준수 구조는 의존성을 가볍게 만들고 구현 대체와 테스트 대역 작성을 쉽게 한다 | 원칙 무시 구조는 미사용 메서드 변경이 여러 구현체와 테스트를 쓸데없이 흔든다 |

연결 개념으로는 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)-어댑터, [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 만능 공구를 비교해 보는 순간 어떤 문제가 줄어드는지가 선명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 무조건 채택하기보다 인터페이스 분리의 목적은 개수 늘리기가 아니라 클라이언트별 불필요 의존 제거임을 명확히 써야 한다. 아래 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 변경 이유를 한 문장으로 설명할 수 있는가?
2. 공개 인터페이스가 실제 책임보다 넓지 않은가?
3. 숨은 결합 없이 단위 테스트가 가능한가?
4. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 추가 비용이 얻는 안정성보다 크지 않은가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 출항 전 점검표처럼, 적용 조건을 확인해야 원칙이 장식이 아니라 안전장치가 된다.

---

## Ⅴ. 기대효과 및 결론

인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))의 기대효과는 분명하다. 의존성을 가볍게 만들고 구현 대체와 테스트 대역 작성을 쉽게 한다. 다만 인터페이스를 지나치게 세분화하면 탐색성이 떨어지고 계약 수가 과도하게 늘 수 있다. 결국 기억할 관점은 클라이언트별로 필요한 계약만 남기는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 반복해서 꺼내 보는 사용 설명서처럼, 오래 갈 설계일수록 핵심 규칙이 짧고 분명해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)-어댑터 | 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) | 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [의존성 주입](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) | 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/1008_test_double_isolation/) | 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[비대한 인터페이스] -> ISP 적용] -> [역할별 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 분리]

### 👶 어린이를 위한 3줄 비유 설명
1. 인터페이스 분리 원칙 ([Interface Segregation Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/246_isp_interface_segregation_principle/), [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/))은 필요한 버튼만 있는 리모컨을 사람마다 따로 주는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 클라이언트별로 필요한 계약만 남기는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 436 / 530

<- **이전**: [357. 리스코프 치환 원칙 (Liskov Substitution Principle, LSP)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/357_process/)
**다음**: [359. 의존 역전 원칙 (Dependency Inversion Principle, DIP)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/359_process/) ->

---
