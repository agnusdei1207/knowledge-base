+++
title = "625. 테스트 더블 Mock과 Stub의 차이"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 영화 촬영을 할 때 위험한 장면에서 진짜 배우 대신 '스턴트 더블(Stunt Double)'이 연기하듯, 소프트웨어 테스트에서도 진짜 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 대신 투입되는 가짜 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)를 제라드 메스자로스(Gerard Meszaros)가 '[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/)'이라고 명명했다. [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/)의 5가지 종류는 [Dummy](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/), [Fake](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/), [Stub](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/), [Spy](/knowledge-base/studynote/04_software_engineering/11_testing_validation/461_spy_test_double/), Mock이다.

- **필요성**: 회원 가입 로직을 테스트하려면 DB에 연결하고, 메일 서버([SMTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/488_smtp_simple_mail_transfer_protocol/))에 연결해야 한다. 만약 메일 서버가 점검 중이면 내 코드에 버그가 없어도 테스트는 실패(False Negative)한다. 또한 DB에 매번 데이터를 넣었다 지웠다 하면 테스트가 너무 느려져서 개발자가 테스트 실행 버튼을 누르기 싫어지게 된다. 진짜 객체를 빠르고 통제 가능한 '가짜([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))'로 갈아 끼워야만 완벽한 고립([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)) 테스트가 가능해진다.

- **💡 비유**: 조종사가 비행 연습을 할 때, 매번 진짜 수백억 원짜리 비행기를 타고 하늘로 올라가서 추락해 볼 수는 없습니다. 그래서 조종석과 똑같이 생겼지만 날지는 않는 '비행 시뮬레이터([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/))'에 앉아 연습을 하죠. 이때 버튼을 누르면 미리 입력된 풍속 수치를 화면에 띄워주는 것이 <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/">Stub</a></strong>이고, 비상 탈출 버튼을 매뉴얼 순서대로 정확하게 눌렀는지 기계가 감시하고 채점하는 것이 <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/">Mock</a></strong>입니다.

- **등장 배경 및 발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 단위 테스트의 어려움</strong>: 코드가 덩어리(Monolithic)로 짜여있어 외부 의존성을 끊어내고 테스트하기가 불가능에 가까웠다.
  2. <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/">의존성 주입</a>(<a href="/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/190_enterprise_di_framework_lifecycle/">DI</a>)의 확산</strong>: Spring 프레임워크처럼 생성자로 객체를 주입(Inject)받는 패턴이 표준화되면서, 운영 시에는 '진짜 DB'를 넣고 테스트 시에는 '가짜 DB'를 밀어 넣는 것이 매우 쉬워졌다.
  3. **Mockito 등 프레임워크의 대중화**: 수동으로 가짜 클래스를 코딩하던 시절을 지나, Mockito(Java), Jest(Node.js) 같은 라이브러리가 등장하며 어노테이션 한 줄로 Mock과 Stub을 찍어내는 [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) 시대가 열렸다.

- **📢 섹션 요약 비유**: 실제 배우(외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))가 스케줄이 안 맞거나 너무 비싸서 못 올 때, 감독(테스터)이 지시한 대사만 딱딱 읽어주는 엑스트라([Stub](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/))나, 주인공과 약속된 동작(합)을 정확히 맞추는지 감시해 주는 스턴트맨([Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/))을 대신 부르는 것과 같습니다.

---

다음은 [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  테스트 더블 Mock과 Stub의 차                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이의 핵심 원리는 **복잡성 분해**, **역할 분리**, <strong>품질 측정</strong>의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이 | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
테스트 더블 Mock과 Stub의 차이 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) Mock과 Stub의 차이은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 791 / 973

<- **이전**: [624. 클라우드 네이티브 12 Factor App](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/624_cloud_native_12_factor_app/)
**다음**: [626. V-모델 개발-테스트 매핑 구조](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/626_v_model_development_testing_mapping/) ->

---
