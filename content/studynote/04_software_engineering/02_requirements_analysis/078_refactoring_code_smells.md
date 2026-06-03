+++
title = "78. 리팩토링 (Refactoring) - 외부 동작 변경 없이 내부 구조 개선"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) (Refactoring)은 외부 동작은 그대로 두고 내부 구조만 더 읽기 좋고 바꾸기 쉽게 만드는 작업이다.
> 2. **가치**: [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/)([code smell](/knowledge-base/studynote/12_it_management/05_security_compliance/365_5_solid_code_smell/))은 당장 버그가 아니더라도 설계 부채가 쌓였다는 신호다.
> 3. **판단 포인트**: 테스트가 없으면 바꾸는 순간 기능이 달라졌는지 알기 어려워서 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)이 아니라 도박이 된다.

---

## Ⅰ. 개요 및 필요성

[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)은 기능을 바꾸지 않고 구조를 바꾸는 활동이다. [코드 스멜](/knowledge-base/studynote/04_software_engineering/06_software_architecture/370_code_smell/)은 "이 코드가 앞으로 더 아파질 가능성이 높다"는 경고로 보면 된다.
빠르게만 만든 코드는 수정할수록 더 느려진다. 그래서 [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) ([Test-Driven Development](/knowledge-base/studynote/11_design_supervision/06_exam_summary/411_process/))와 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/))가 안전망이 된다.
```text
냄새 탐지 → 테스트 확보 → 작은 변경 → 회귀 검증 → 유지보수성 향상
```

- **📢 섹션 요약 비유**: 냄새는 버그보다 먼저 구조의 피로를 알린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

대표적인 스멜은 Duplicate [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), Long Method, Large Class, Feature Envy, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clumps, Shotgun Surgery다. 이들은 대부분 책임 분리 실패와 겹친다.
[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)은 작은 단계로만 진행하고, 각 단계마다 테스트를 통과시켜야 한다. 큰 한 번의 변경보다 여러 번의 안전한 변경이 더 싸다.
| 스멜 | 징후 | 대표 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) |
| --- | --- | --- |
| Duplicate [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) | 같은 로직이 여러 곳에 있다 | 함수 추출, 공통화 |
| Long Method | 한 함수가 너무 길다 | 메서드 분해, 의도 이름 부여 |
| Large Class | 책임이 너무 많다 | 클래스 분할, 책임 이동 |
| Feature Envy | 다른 객체 데이터에 집착한다 | 메서드 이동 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clumps | 같은 매개변수가 뭉친다 | 객체화, 파라미터 클래스 |
| Shotgun Surgery | 작은 수정이 곳곳을 건드린다 | [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) 개선, 경계 정리 |

- **📢 섹션 요약 비유**: 작은 단계와 테스트가 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)의 안전벨트다.

---

## Ⅲ. 비교 및 연결

[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)은 재작성(rewrite)과 다르고, 설계 전환(re-design)과도 다르다. 전자는 내부 구조를 조금씩 개선하는 일이지만, 후자는 문제 정의 자체를 다시 세우는 일이다.
[SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/) ([Single Responsibility Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/)), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/)), DRY (Don't Repeat Yourself) 같은 원칙은 스멜을 줄이는 기준이다. 다만 테스트 없이 원칙만 붙이면 오히려 복잡해질 수 있다.
| 기준 | [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | 재작성 | 재설계 |
| --- | --- | --- | --- |
| 목적 | 동작 유지 + 구조 개선 | 코드를 새로 씀 | 문제 정의를 다시 함 |
| 위험 | 낮음(테스트 전제) | 높음 | 중간~높음 |
| 적합 상황 | [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/) 개선 | 기술 부채가 극심할 때 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델이 잘못됐을 때 |

- **📢 섹션 요약 비유**: [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/), 재작성, 재설계는 목적과 위험이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 변경 비용이 올라갈 때, 같은 버그가 반복될 때, [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) ([Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)) 리뷰가 길어질 때 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 신호로 본다. 반대로 납기 직전에는 구조 개선보다 안정화가 우선일 수 있다.
TDD와 CI가 있으면 characterization test(캐릭터라이제이션 테스트)로 기존 동작을 고정한 뒤 안전하게 구조를 바꿀 수 있다.
### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 바꾸기 전에 회귀 테스트가 충분한가?
2. 작은 단계로 나눌 수 있는가?
3. 변경 후 의도가 더 분명해졌는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 테스트 없이 큰 규모로 한 번에 바꾸는 것
- 기능 변경과 구조 변경을 한 PR에 섞는 것

- **📢 섹션 요약 비유**: 테스트와 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 규율이 있어야 구조 개선이 가능하다.

---

## Ⅴ. 기대효과 및 결론

좋은 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)은 기능 속도를 늦추는 게 아니라 이후 변경 속도를 올린다. 결국 [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)은 지금의 개발 속도를 약간 줄여 미래의 속도를 크게 올리는 투자다.
앞으로는 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 분리와 아키텍처 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)이 기술 부채를 줄이는 핵심이 된다.
기술사는 이 주제를 "냄새를 줄여 변경 비용을 낮추는 습관"으로 기억하면 된다.

- **📢 섹션 요약 비유**: 지금 조금 고치면 다음 변경이 훨씬 쉬워진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [Code smell](/knowledge-base/studynote/12_it_management/05_security_compliance/365_5_solid_code_smell/) | 구조 피로의 증상이다 |
| Refactoring | 동작을 유지하며 구조를 바꾼다 |
| [Technical debt](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) | 미뤄진 설계 비용이다 |
| [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) | 안전망 역할을 한다 |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) | 변경 후 즉시 확인한다 |
| [SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/) | 책임 분리의 기준이다 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">스멜 발견</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">테스트 확보</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">작은 리팩토링</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">회귀 검증</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CI 통과 후 반영</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 장난감을 버리지 않고 상자만 정리하는 것과 같다.
2. 같은 장난감이 여러 상자에 있으면 찾기 힘들어서 먼저 모아둔다.
3. 정리할 때마다 이름표를 붙이면 다음에는 더 빨리 찾을 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 78 / 973

← **이전**: [77. 테스트 주도 개발 (TDD, Test Driven Development) - Red-Green-Refactor](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/077_tdd_test_driven_development/)
**다음**: [079. 메타포 (Metaphor - XP Practice)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/079_metaphor_xp_practice/) →

---
