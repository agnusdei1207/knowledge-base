---
title: "Observer Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))은 한 객체의 상태 변화가 여러 구독자에게 자동 통지되도록 하는 행동 패턴이다.
> 2. **가치**: 발행자와 구독자를 느슨하게 결합해 확장성을 높인다.
> 3. **판단 포인트**: [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)는 이벤트 소싱처럼 이력 저장이 목적이 아니며, 구독 해지와 알림 품질이 중요하다는 점을 써야 한다.

---

## Ⅰ. 개요 및 필요성

[옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))은 한 객체의 상태 변화가 여러 구독자에게 자동 통지되도록 하는 행동 패턴이다. 상태 변경을 여러 화면, [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 후속 처리에 반영해야 할 때 직접 호출을 모두 나열하면 결합이 커진다. 이 개념이 필요한 이유는 상태 변화 전파를 느슨하게 연결하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 변경 대상이 늘어날수록 발행자가 구독자 상세를 알아야 해 구조가 경직된다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
| Variation  |--->|  Observe   |--->|   Reuse    |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 공구함에서 맞는 도구를 고르지 못하면 같은 작업도 매번 힘으로 밀어붙이게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))의 핵심 원리는 "상태 변화 전파를 느슨하게 연결하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 주제(subject)가 구독자 목록을 관리하고 변경 시 등록된 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)에게 알림을 보낸다. 동시에 알림 순서, 중복, [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/), 폭주를 관리하지 않으면 이벤트 홍수와 디버깅 난도가 커진다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 상태 변화 전파를 느슨하게 연결하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 주제(subject)가 구독자 목록을 관리하고 변경 시 등록된 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)에게 알림을 보낸다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 알림 순서, 중복, [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/), 폭주를 관리하지 않으면 이벤트 홍수와 디버깅 난도가 커진다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Client  |--->| Observe  |--->|  Object  |--->|  Result  |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 조립식 부품처럼 협력 관계가 정리되면 기능을 더해도 기본 골격은 유지된다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **패턴 적용 상태** 와 **즉흥 구현 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 패턴 적용 상태는 상태 변화 전파를 느슨하게 연결하는 일에 맞춰 영향 범위를 줄인다 | 즉흥 구현 상태는 변경이 주변 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 번지기 쉽다 |
| 구조 안정성 | 패턴 적용 상태는 주제(subject)가 구독자 목록을 관리하고 변경 시 등록된 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)에게 알림을 보낸다 | 즉흥 구현 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 패턴 적용 상태는 발행자와 구독자를 느슨하게 결합해 확장성을 높인다 | 즉흥 구현 상태는 변경 대상이 늘어날수록 발행자가 구독자 상세를 알아야 해 구조가 경직된다 |

연결 개념으로는 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/), 퍼블리시-서브스크라이브 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 즉흥 수리를 비교하면 패턴이 줄이는 복잡도가 분명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 무조건 채택하기보다 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)는 이벤트 소싱처럼 이력 저장이 목적이 아니며, 구독 해지와 알림 품질이 중요하다는 점을 써야 한다. 아래 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 반복되는 변화 축이 실제로 존재하는가?
2. 패턴이 줄이는 복잡도보다 추가 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용이 작은가?
3. 클라이언트가 다시 구체 구현에 묶이지 않는가?
4. 테스트와 디버깅 관점에서 협력 구조를 설명할 수 있는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 작업 전 안전 점검표처럼, 변화 축이 실제로 있는지 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))의 기대효과는 분명하다. 발행자와 구독자를 느슨하게 결합해 확장성을 높인다. 다만 알림 순서, 중복, [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/), 폭주를 관리하지 않으면 이벤트 홍수와 디버깅 난도가 커진다. 결국 기억할 관점은 상태 변화 전파를 느슨하게 연결하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 현장 표준 공법서처럼, 패턴은 이름보다 어떤 문제를 반복해서 줄여 주는지가 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/) | [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 퍼블리시-서브스크라이브 | [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 반응형 UI | [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) | [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[직접 후속 호출] -> [옵저버 패턴] -> [구독 기반 확장]

### 👶 어린이를 위한 3줄 비유 설명
1. [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) ([Observer Pattern](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))은 학교 종이 울리면 여러 반이 동시에 움직이는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 상태 변화 전파를 느슨하게 연결하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 468 / 530

<- **이전**: [389. 프록시 패턴 (Proxy Pattern)](/studynote/11_design_supervision/06_exam_summary/389_proxy_pattern_summary/)
**다음**: [391. 전략 패턴 (Strategy Pattern)](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ->

---
