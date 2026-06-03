+++
title = "248. 리팩토링 TDD 안전망 (Refactoring TDD Safety Net)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) ([Test-Driven Development](/knowledge-base/studynote/11_design_supervision/06_exam_summary/411_process/), [테스트 주도 개발](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/077_tdd_test_driven_development/)) 는 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)의 **안전망 (Safety Net)** 으로, "외부 동작 불변" 이라는 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)의 전제 조건을 테스트 스위트 (Test Suite) 가 자동으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
> 2. **가치**: 테스트 없는 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)은 낙하산 없는 스카이다이빙이며, 충분한 테스트 커버리지 (Test Coverage) 가 확보된 상태에서만 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)을 안전하게 반복할 수 있다.
> 3. **판단 포인트**: "[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 후 모든 테스트가 녹색(Green)[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)?" — Yes라면 동작이 보존되었다.

---

## Ⅰ. 개요 및 필요성
마틴 파울러 (Martin Fowler) 는 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)의 정의에 "외부에서 관찰 가능한 동작 (Observable Behavior) 을 바꾸지 않으면서 내부 구조를 개선하는 것"이라 명시한다. 이 전제를 **자동으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)**하는 수단이 바로 자동화 테스트 (Automated Test) 다.

```
┌──────────────────────────────────────────────────┐
│           TDD 레드-그린-리팩터 사이클            │
│                                                  │
│    RED          GREEN         REFACTOR           │
│  ┌──────┐     ┌──────┐     ┌──────────────┐     │
│  │실패  │ ──▶ │성공  │ ──▶ │내부 구조 개선 │ ──┐ │
│  │테스트│     │테스트│     │동작 변경 없음 │   │ │
│  └──────┘     └──────┘     └──────────────┘   │ │
│                                    ▲           │ │
│                                    └───────────┘ │
└──────────────────────────────────────────────────┘
```

- **기존 동작 파괴**: 코드 이동·변환 과정에서 의도치 않은 버그 도입
- **회귀 (Regression)**: 수정 이전에 정상 동작하던 기능이 이후 중단
- **두려움 (Fear)**: 테스트 없는 팀은 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 자체를 포기하고 코드 부채를 쌓는다

- **📢 섹션 요약 비유**: 낡은 다리를 보수할 때 아래에 안전망을 치고 작업하는 것 — 망이 없으면 실수 한 번에 끝이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
              ▲
             /E2E\       ← 종단 간 테스트 (느림, 비용 큼)
            /─────\
           / 통합  \     ← 통합 테스트 (Integration Test)
          /─────────\
         / 단위 테스트\  ← Unit Test (빠름, 비용 적음) ★ 리팩토링 주력
        /─────────────\
        ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
```

[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 안전망의 주력은 **[단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) ([Unit Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/))** 다. 빠른 [피드백 루프](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/) ([Feedback Loop](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)) 를 제공해 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 직후 즉시 결과를 확인한다.

| 커버리지 유형 | 설명 | [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 안전 기준 |
|:---|:---|:---|
| 라인 커버리지 (Line Coverage) | 실행된 코드 라인 비율 | 80%+ 권고 |
| 브랜치 커버리지 (Branch Coverage) | 분기(if/else) 경로 커버 | 75%+ 권고 |
| 변이 테스트 ([Mutation Testing](/knowledge-base/studynote/04_software_engineering/11_testing_validation/456_mutation_testing/)) | 코드 변이 감지율 | 60%+ 이상적 |

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/)) 은 의존 객체를 대체해 [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)의 독립성을 보장한다.

```
┌──────────────────────────────────────────────────┐
│               테스트 더블 유형                   │
├──────────────┬───────────────────────────────────┤
│  유형        │  역할                             │
├──────────────┼───────────────────────────────────┤
│  Stub        │ 고정 응답 반환 (상태 검증)        │
│  Mock        │ 호출 기대 검증 (행동 검증)        │
│  Fake        │ 실제 동작하는 경량 대체           │
│  Spy         │ 실제 동작 + 호출 기록             │
│  Dummy       │ 파라미터 채우기용 (미사용)        │
└──────────────┴───────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 항공기 시뮬레이터로 연습하면 실제 비행기를 추락시키지 않고 조종 실력을 기를 수 있다 — [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/)이 바로 그 시뮬레이터다.

---

## Ⅲ. 비교 및 연결
| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 테스트 위치 | 속도 | [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 안전성 | 적합 대상 |
|:---|:---|:---|:---|:---|
| [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) ([Test-Driven Development](/knowledge-base/studynote/11_design_supervision/06_exam_summary/411_process/)) | 구현 전 작성 | 빠름 | 최고 | 신규 코드 |
| [BDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/) ([Behavior-Driven Development](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/126_bdd_behavior_driven_development_given_when_then/)) | 명세 기반 작성 | 중간 | 높음 | 비즈니스 로직 |
| 레거시 커버리지 추가 | 구현 후 작성 | 느림 | 중간 | 레거시 시스템 |
| 탐색적 테스트 (Exploratory Test) | 수동 | 매우 느림 | 낮음 | 엣지케이스 발굴 |

```
[ 안전한 리팩토링 워크플로우 ]
기존 코드
  │
  ├─ 테스트 커버리지 확인 (< 70%?)
  │     ├─ Yes ──▶ 테스트 먼저 추가 ──┐
  │     └─ No  ──────────────────────┤
  │                                  ↓
  ├─ 스멜 식별 (Code Smell Detection)
  │
  ├─ 리팩토링 기법 선택
  │
  ├─ 소규모 변경 + 즉시 테스트 실행 (빨간불?)
  │     ├─ 실패 ──▶ 즉시 롤백 (Revert)
  │     └─ 성공 ──▶ 다음 단계
  │
  └─ 커밋 (Commit) → 반복
```

- **📢 섹션 요약 비유**: 등산할 때 발을 딛을 때마다 발판을 확인하는 것처럼, [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)도 작은 변경마다 테스트로 확인한다.

---

## Ⅳ. 실무 적용 및 기술사 판단
마이클 페더스 (Michael Feathers) 의 『레거시 코드 활용 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) (Working Effectively with Legacy [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))』 에서 제안하는 접근:

1. **봉합부 (Seam) 찾기**: 테스트를 삽입할 수 있는 코드 경계 발견
2. **특성 테스트 (Characterization Test) 작성**: 현재 동작을 그대로 문서화
3. **안전망 확보 후 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 시작**
4. **커버리지 점진적 확대**: 수정하는 코드 주변부터 테스트 추가

[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)) 파이프라인에 테스트를 통합하면 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 후 자동으로 안전망이 작동한다.

```
개발자 커밋 → CI 파이프라인 자동 실행
  │
  ├─ 단위 테스트 실행 (< 5분 목표)
  ├─ 통합 테스트 실행
  ├─ 코드 커버리지 리포트 생성
  └─ 실패 시 Slack/이메일 알림
```

- **지속적 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) (Continuous [Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/))**: 스프린트마다 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 제거 시간을 스케줄링
- **보이 스카우트 규칙 (Boy Scout Rule)**: "캠프장을 발견했을 때보다 더 깨끗하게 떠나라" — 건드린 코드는 반드시 개선
- **안전망 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) ([Return on Investment](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/))**: 테스트 작성 투자 대비 버그 감소·[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 속도 향상 효과로 3~6개월 내 회수

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 단위를 작게 나눠 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 건물 리모델링 시 안전 진단 없이 벽을 허물면 건물이 무너진다 — 테스트가 구조 안전 진단이다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | 테스트 없는 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) 안전망 적용 |
|:---|:---:|:---:|
| [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 후 회귀 버그 발생률 | 높음 (35%+) | 낮음 (5% 이하) |
| [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 1회 소요 시간 | 길어짐 (불안) | 짧아짐 (자신감) |
| 팀 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 참여 의지 | 낮음 (두려움) | 높음 (안전) |
| 릴리즈 후 핫픽스 빈도 | 월 4~6건 | 월 0~1건 |

[TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) 안전망 ([TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) Safety Net) 은 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)을 **두려움 없는 반복 행위**로 전환한다. "테스트 없이 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)하지 말라"는 원칙은 단순한 관례가 아니라, 소프트웨어 진화 (Software Evolution) 를 지속 가능하게 만드는 **공학적 필수 조건**이다. 기술사 논술에서는 테스트 커버리지 목표 수치와 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 연동 방안을 함께 제시해야 설득력이 높다.

확장 방향은 ① [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 자동화, ② 아키텍처 적합성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), ③ 작은 단위의 상시 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 문화 정착이다.

- **📢 섹션 요약 비유**: 의사가 수술 전후 바이탈 사인(Vital Sign)을 측정하는 것처럼, [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 전후 테스트 스위트가 코드 건강 상태를 자동으로 확인한다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) ([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/)) | [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) 안전망이 지원하는 활동 |
| 핵심 수단 | [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) ([Test-Driven Development](/knowledge-base/studynote/11_design_supervision/06_exam_summary/411_process/)) | 안전망의 주요 구축 방법론 |
| 연관 개념 | 테스트 커버리지 (Test Coverage) | 안전망의 두께 지표 |
| 연관 개념 | 테스트 피라미드 (Test Pyramid) | 테스트 유형별 비율 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| 연관 개념 | 특성 테스트 (Characterization Test) | 레거시 코드 안전망 구축 |
| 연관 개념 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)) | 자동화 안전망 파이프라인 |
| 연관 개념 | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/)) | 격리된 [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 지원 |

### 📈 관련 키워드 및 발전 흐름도
characterization test → [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) 안전망 → continuous [refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/)

### 👶 어린이를 위한 3줄 비유 설명
1. 체조 선수가 새 기술을 연습할 때 처음에는 스펀지 매트 위에서 한다 — 매트가 테스트고, 연습이 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)이다.
2. 매트(테스트)가 있으면 실수해도 다시 일어나 계속 연습할 수 있다.
3. 테스트 없이 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)하는 것은 딱딱한 바닥에서 새 기술을 처음 시도하는 것이다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 309 / 530

← **이전**: [247. 클린 코드 네이밍 철학 (Clean Code Self-Documenting Naming)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/247_clean_code_naming_philosophy/)
**다음**: [249. 레거시 설계 부채와 ADR (Legacy Design Debt & Architecture Decision Record)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/249_legacy_design_debt_adr/) →

---
