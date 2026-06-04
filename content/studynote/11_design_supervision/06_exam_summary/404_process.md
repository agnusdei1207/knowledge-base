+++
title = "404. 테스트 더블 (Test Double)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))은 실제 협력 객체 대신 테스트 목적에 맞게 대체하는 [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/), 목, [페이크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/), [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/461_spy_test_double/) 등의 총칭이다.
> 2. **가치**: 빠르고 결정적인 테스트를 통해 리팩터링 안전망을 만든다.
> 3. **판단 포인트**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/)은 종류별 목적 차이를 구분해 써야 하며, 모의 객체 남용의 위험도 함께 언급하는 것이 좋다.

---

## Ⅰ. 개요 및 필요성

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))은 실제 협력 객체 대신 테스트 목적에 맞게 대체하는 [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/), 목, [페이크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/), [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/461_spy_test_double/) 등의 총칭이다. 외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), DB, 시간, 메시지 큐를 실제로 붙여 테스트하면 느리고 불안정하며 재현성이 떨어진다. 이 개념이 필요한 이유는 협력 객체를 통제 가능한 대체물로 치환하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 테스트가 느리고 flaky해져 변경을 두려워하는 팀 문화가 생긴다.

아래 그림은 왜 이 주제가 “문제 인식 -> 설계 규칙 -> 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.

```text
+------------+   +------------+   +------------+
|    Data    |--->|   Double   |--->|  Boundary  |
+------------+   +------------+   +------------+
```

이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 접수 창구를 구분하지 않으면 민원, 결제, 안내가 한 줄에 엉키는 상황과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))의 핵심 원리는 "협력 객체를 통제 가능한 대체물로 치환하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/)은 정해진 응답, 목은 상호작용 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [페이크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/)는 간단한 대체 구현, [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/461_spy_test_double/)는 호출 기록 수집을 담당한다. 동시에 더블이 실제 동작과 지나치게 다르면 테스트 신뢰도가 떨어지므로 계약 기반 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필요하다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 협력 객체를 통제 가능한 대체물로 치환하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/)은 정해진 응답, 목은 상호작용 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [페이크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/)는 간단한 대체 구현, [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/461_spy_test_double/)는 호출 기록 수집을 담당한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 더블이 실제 동작과 지나치게 다르면 테스트 신뢰도가 떨어지므로 계약 기반 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필요하다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.

```text
+----------+   +----------+   +----------+   +----------+
|  Caller  |--->| Contract |--->|  Double  |--->|  Store   |
+----------+   +----------+   +----------+   +----------+
```

이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 물류 전달 벨트처럼 입력과 저장 사이의 책임이 분리되어야 흐름이 막히지 않는다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **경계 분리 상태** 와 **계층 혼재 상태** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 경계 분리 상태는 협력 객체를 통제 가능한 대체물로 치환하는 일에 맞춰 영향 범위를 줄인다 | 계층 혼재 상태는 변경이 주변 모듈로 번지기 쉽다 |
| 구조 안정성 | 경계 분리 상태는 [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/)은 정해진 응답, 목은 상호작용 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [페이크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/)는 간단한 대체 구현, [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/461_spy_test_double/)는 호출 기록 수집을 담당한다 | 계층 혼재 상태는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 경계 분리 상태는 빠르고 결정적인 테스트를 통해 리팩터링 안전망을 만든다 | 계층 혼재 상태는 테스트가 느리고 flaky해져 변경을 두려워하는 팀 문화가 생긴다 |

연결 개념으로는 [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/), [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/) 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 직접 전달과 중간 허브를 비교하면 경계의 가치가 더 뚜렷해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))을 무조건 채택하기보다 [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/)은 종류별 목적 차이를 구분해 써야 하며, 모의 객체 남용의 위험도 함께 언급하는 것이 좋다. 아래 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 계층 간 계약이 명확하고 중복 변환이 과도하지 않은가?
2. 비즈니스 규칙이 전송/저장 계층으로 새지 않는가?
3. 예외 처리와 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계가 문서화되어 있는가?
4. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화가 책임 분리를 무너뜨리지 않는가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 운영 체크시트처럼 계층 간 계약과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 일관성을 먼저 확인해야 한다.

---

## Ⅴ. 기대효과 및 결론

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))의 기대효과는 분명하다. 빠르고 결정적인 테스트를 통해 리팩터링 안전망을 만든다. 다만 더블이 실제 동작과 지나치게 다르면 테스트 신뢰도가 떨어지므로 계약 기반 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필요하다. 결국 기억할 관점은 협력 객체를 통제 가능한 대체물로 치환하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 업무 인수인계서처럼, 좋은 엔터프라이즈 패턴은 사람과 시스템 모두 이해하기 쉬워야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [스텁](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| 목([Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/)) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))을 설계하고 감리할 때 함께 보는 연관 개념 |
| [페이크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[실환경 의존 테스트] -> [테스트 더블 사용] -> [격리된 빠른 검증]

### 👶 어린이를 위한 3줄 비유 설명
1. [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))은 연습 경기에서 진짜 상대 대신 훈련용 인형과 친구를 상황별로 바꿔 쓰는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 협력 객체를 통제 가능한 대체물로 치환하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 482 / 530

<- **이전**: [403. 안티 패턴 (Anti-Patterns)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/403_architecture/)
**다음**: [405. MVC 패턴 (Model-View-Controller)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/405_mvc_m_v_c/) ->

---
