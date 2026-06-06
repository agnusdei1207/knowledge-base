---
title: "Hexagonal Architecture"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))은 애플리케이션 코어를 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)로 감싸 외부 입출력 채널을 교체 가능하게 만드는 구조다.
> 2. **가치**: 다양한 인터페이스를 같은 코어 규칙으로 수용하게 해 준다.
> 3. **판단 포인트**: [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)-[어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 “육각형 모양”보다 의존 경계와 테스트 격리에 초점을 두고 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

[헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))은 애플리케이션 코어를 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)로 감싸 외부 입출력 채널을 교체 가능하게 만드는 구조다. UI, 배치, 메시지, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스가 바뀌어도 핵심 규칙을 그대로 유지하려는 요구에서 등장했다. 이 개념이 필요한 이유는 애플리케이션 코어와 외부 채널을 명확히 분리하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 입력 채널이 달라질 때마다 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 코드가 외부 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 세부사항에 오염된다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
|  Request   |--->|    Hex     |--->|   Stable   |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 도시를 구획 없이 확장하면 길과 배관이 엉키는 것처럼, 구조 원칙이 없으면 시스템도 빨리 혼잡해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))의 핵심 원리는 "애플리케이션 코어와 외부 채널을 명확히 분리하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 입력 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 출력 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 정의하고, 웹·배치·DB·메시지 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)가 이를 구현하게 한다. 동시에 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 과도하게 늘리면 단순 시스템에도 배선 복잡도와 학습 비용이 커진다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 애플리케이션 코어와 외부 채널을 명확히 분리하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 입력 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 출력 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 정의하고, 웹·배치·DB·메시지 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)가 이를 구현하게 한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 과도하게 늘리면 단순 시스템에도 배선 복잡도와 학습 비용이 커진다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Client  |--->| Boundary |--->|   Core   |--->|  Infra   |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 도로망과 관제 센터가 분리된 도시처럼, 경계와 흐름을 함께 설계해야 운영이 안정된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **구조 적용 상태** 와 **경계 혼재 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 구조 적용 상태는 애플리케이션 코어와 외부 채널을 명확히 분리하는 일에 맞춰 영향 범위를 줄인다 | 경계 혼재 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 구조 적용 상태는 입력 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 출력 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 정의하고, 웹·배치·DB·메시지 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)가 이를 구현하게 한다 | 경계 혼재 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 구조 적용 상태는 다양한 인터페이스를 같은 코어 규칙으로 수용하게 해 준다 | 경계 혼재 상태는 입력 채널이 달라질 때마다 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 코드가 외부 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 세부사항에 오염된다 |

연결 개념으로는 [클린 아키텍처](/studynote/04_software_engineering/04_testing_quality/217_clean_architecture_dependency_rule/), [DIP](/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/) 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 계획도시와 무계획 확장을 비교해 보면 어디서 비용이 커지는지 바로 드러난다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))을 무조건 채택하기보다 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)-[어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 “육각형 모양”보다 의존 경계와 테스트 격리에 초점을 두고 설명해야 한다. 아래 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 경계와 책임이 코드·문서·배포 단위에서 일치하는가?
2. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권과 장애 전파 경로가 명확한가?
3. 관찰가능성, 보안, 배포 전략이 구조와 함께 설계되었는가?
4. 도입 복잡도가 조직 규모와 팀 성숙도에 맞는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 관제실의 운영 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)처럼, 경계·장애 전파·관찰가능성을 같이 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

[헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))의 기대효과는 분명하다. 다양한 인터페이스를 같은 코어 규칙으로 수용하게 해 준다. 다만 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 과도하게 늘리면 단순 시스템에도 배선 복잡도와 학습 비용이 커진다. 결국 기억할 관점은 애플리케이션 코어와 외부 채널을 명확히 분리하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 도시 운영 규정집처럼, 좋은 아키텍처는 기술보다 판단 기준을 오래 남긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [클린 아키텍처](/studynote/04_software_engineering/04_testing_quality/217_clean_architecture_dependency_rule/) | [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [DIP](/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/) | [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [어댑터 패턴](/studynote/11_design_supervision/06_exam_summary/383_adapter_pattern_summary/) | [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [테스트 더블](/studynote/12_it_management/05_security_compliance/1008_test_double_isolation/) | [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[채널별 개별 구현] -> [헥사고날 아키텍처] -> [멀티 채널 재사용]

### 👶 어린이를 위한 3줄 비유 설명
1. [헥사고날 아키텍처](/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) (Hexagonal [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))은 같은 충전기에 여러 모양의 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)를 끼워 쓰는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 애플리케이션 코어와 외부 채널을 명확히 분리하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 444 / 530

<- **이전**: [365. 클린 아키텍처 (Clean Architecture)](/studynote/11_design_supervision/06_exam_summary/365_architecture/)
**다음**: [367. 이벤트 주도 아키텍처 (Event-Driven Architecture, EDA)](/studynote/11_design_supervision/06_exam_summary/367_architecture/) ->

---
