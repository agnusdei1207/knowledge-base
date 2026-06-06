---
title: "607. Factory Method Vs Abstract Factory"
date: "2026-05-08"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)은(는) [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - **Factory (공장)**: 제품(객체)을 `new` 키워드로 찍어내는 역할을 전담하는 놈. 나([Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))는 공장한테 "A 제품 줘!" 텍스트만 던지고, 그게 안에서 어떻게 뚝딱뚝딱 복잡하게 조립되는지 1도 모름(캡슐화).
  - <strong><a href="/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/">Factory Method</a></strong>: 부모 클래스가 껍데기만 뚫어놓고, "진짜 어떤 놈을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할지는 내 밑에 있는 <strong>자식 클래스(공장장)</strong>들이 지 맘대로 결정해서 나한테 줘 ㅋ" 라며 책임을 아래로 짬때리는 마술 ([상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 템플릿 기반).
  - <strong><a href="/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/">Abstract Factory</a></strong>: "야 부품 1개 찍어내는 거 말고, <strong>(운전대+바퀴+엔진) 풀세트 덩어리</strong>를 1방에 일괄로 생산하는 거대 공장 단지(공장들의 껍데기)를 만들어봐!"

- <strong>필요성 (<code>new</code> 무지성 남발이 낳은 끔찍한 강결합 파국)</strong>: 신입 개발자가 메인 결제 로직에 `new KakaoPay()` 를 천만 번 복붙해놨다. 사장님이 "내일부터 카카오페이 버리고 네이버페이 써라 ㅋ" 지시했다. 주니어는 1만 줄 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 100개를 다 열어서 `new NaverPay()` 로 수작업 문자열 덮어쓰기 검색 교체(Find & Replace)를 하다가 손가락이 부러지고 오타가 나서 서버가 폭파됐다([OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) 폐쇄 원칙 박살). <strong>"아 ㅆㅂ!! 왜 객체 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 코드를 내 비즈니스 로직(결제) 뱃속에다 쳐박았지?! <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>하는 행위(<a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">new</a>)만 딱 '공장 텐트' 1곳으로 분리해서 짱박아뒀으면, 그냥 공장 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 1줄만 카카오 ➡ 네이버로 바꾸면 1초 컷으로 전사 시스템 싹 다 바뀌었을 거 아냐!!"</strong> 이 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 사용의 처절한 분리(Separation of Use from Creation) 갈망이 팩토리를 낳았다.

- **💡 비유**: 쌩 코딩(`new`)은 <strong>'내가 직접 망치로 쇠를 깎고 나사를 조여서(복잡한 세팅) 자동차(객체)를 1시간 동안 낑낑대며 만들어 타는 짓'</strong>입니다. 자동차 부품 1개 바뀌면 1시간 또 개고생이죠. 팩토리(Factory)는 <strong>'현대자동차 대리점(공장)'</strong>에 가는 겁니다. 딜러(Factory)한테 "그랜저 1대 줘요" 말 한마디(파라미터) 툭 던지면, 공장에서 어떻게 쇠를 깎았는지 난 1도 알 필요 없이 완벽히 세팅 완료된 차 키를 1초 만에 툭 던져줍니다. 공장 로봇(내부 조립 로직)을 지들 맘대로 100번 갈아엎어도, 나는 평생 "그랜저 줘!" 1마디로 꿀을 빠는 압도적 은폐(Hiding) 마술입니다.

- **등장 배경 및 발전 과정**:
  1. **단순 Factory (Simple Factory - 구석기)**: `if(A) new A(); else new B();` 팩토리 클래스 1개 뱃속에 if문 떡칠. 새로운 C 추가할 때마다 이 팩토리 클래스를 또 뜯어고쳐야 해서 [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) 살짝 어김.
  2. <strong><a href="/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/">Factory Method</a> (GoF 진화)</strong>: "야 팩토리 본체도 if문 수정하지 마! 그냥 A 찍어내는 팩토리 자식, B 찍어내는 팩토리 자식 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 10개로 찢어발겨! 확장만 치고 수정은 0으로 만들어!"
  3. <strong><a href="/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/">Abstract Factory</a> (거대 스케일)</strong>: GUI 버튼, 스크롤, 윈도우 창 100개 세트를 맥OS [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) ➡ 윈도우 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 통째로 한 번에 찰칵 스위칭해야 하는 대규모 뷰([View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 엔진 개발자들의 궁극의 필요성 땜에 탄생.
  4. <strong>Spring IoC/<a href="/studynote/11_design_supervision/10_patterns_antipatterns/661_enterprise_di_framework_lifecycle/">DI</a> (현재의 천하통일)</strong>: "야 니들 팩토리 클래스 100개 파느라 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 늘어나서 빡치지? 걍 팩토리 내가 뱃속에 하나(`BeanFactory`) 파둘게. 넌 걍 `@Autowired` 어노테이션 도장 1방 찍어. 내가 공장 돌려서 1초 만에 의존성 꽂아줌 ㅋ" 스프링 프레임워크의 압도적 대관식.

- **📢 섹션 요약 비유**: 이 혁명은 <strong>'맞춤 양복점(<a href="/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/">Factory Method</a>)'</strong>에서 <strong>'대형 백화점 코디 세트(<a href="/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/">Abstract Factory</a>)'</strong>로의 진화입니다. 양복점([Factory Method](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/))은 내가 상의(객체) 하나를 "여름용(A자식)으로 만들어줘, 겨울용(B자식)으로 만들어줘" 1개씩 부탁해서 완벽한 핏의 옷 하나를 뽑는 짓입니다. [백엔드 서비스](/studynote/15_devops_sre/01_culture_methodology/010_backend_services/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 1개에 딱입니다. 백화점 세트([Abstract Factory](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/))는 마네킹에 묶인 <strong>[모자+선글라스+신발 풀코디 세트 덩어리]</strong>를 다루는 겁니다. "여름 [테마](/studynote/04_software_engineering/03_design_architecture/184_theme_agile_requirements/) 세트 줘!" 하면 여름용 부품 3개가 한 번에 딸려옵니다. 서로 어울리는 부품들끼리 절.대.로 삑사리 나지 않고 한 덩어리로 찰칵! 묶어주는 거대 스케일의 [테마](/studynote/04_software_engineering/03_design_architecture/184_theme_agile_requirements/) 스위칭 장비입니다.

---

다음은 [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  팩토리 메서드 vs 추상 팩토리                           |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

[팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)의 핵심 원리는 **복잡성 분해**, **역할 분리**, <strong>품질 측정</strong>의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

[팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)을(를) 올바르게 적용하면 [소프트웨어 품질](/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)·[DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)에서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
팩토리 메서드 vs 추상 팩토리 개념 정립
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

이 흐름은 [소프트웨어 위기](/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [팩토리 메서드](/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) vs [추상 팩토리](/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 773 / 973

<- **이전**: [606. 옵저버 패턴 (Pub/Sub 연계)](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)
**다음**: [608. 전략 패턴 알고리즘 교체 용이성](/studynote/04_software_engineering/10_trends_pm_quality/608_strategy_pattern_algorithm_swap/) ->

---
