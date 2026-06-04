---
title: "856. 서비스 가상화 (Service Virtualization)"
date: "2026-05-08"
tags:
  - "studynote-software-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))은(는) [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 실제 외부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 없어도 테스트가 가능하게 해 준다. [네트워크 지연](/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/), 장애, 비용 문제를 줄일 수 있다.

외부 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 결제 게이트웨이, 사내 시스템처럼 통제가 어려운 의존성에 적합하다.

- **📢 섹션 요약 비유**: 전화 상대가 없어도 응답 연습이 가능한 가짜 전화기다.

---

다음은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Vir의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  서비스 가상화 (Service Vir                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Vir가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

가상 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 요청을 받아 정해진 응답이나 조건부 응답을 돌려준다. 필요하면 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 오류, 비정상 응답도 흉내 낸다.

| 기능 | 설명 |
|:---|:---|
| 응답 모사 | 정상 응답 재현 |
| 오류 모사 | 장애 상황 재현 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 모사 | 느린 응답 재현 |

```text
테스트 대상 -> 가상 서비스 -> 응답/오류/지연
```

단순 Stub보다 더 풍부한 외부 환경을 제공할 수 있다.

- **📢 섹션 요약 비유**: 연습용 상대가 기분도 좋고 화도 내 줄 수 있는 것이다.

---

---

---

---

## Ⅲ. 비교 및 연결

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 Test Double의 확장판처럼 볼 수 있다. 외부 의존 전체를 통제하는 데 초점이 있다.

| 구분 | [Stub](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) |
|:---|:---|:---|
| 범위 | 단일 응답 | 외부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체 |
| 현실성 | 낮음~중간 | 중간~높음 |
| 활용 | [단위 테스트](/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) | [통합 테스트](/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) |

[MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [계약 테스트](/studynote/15_devops_sre/05_devsecops/266_contract_testing_pact_msa_api/), [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD와도 잘 맞는다.

- **📢 섹션 요약 비유**: 상대를 한 명 흉내 내는 것과 팀 전체를 모사하는 것은 다르다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 외부 결제, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 배송, SMS [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 대표 대상이다. 테스트 불안정성을 크게 줄여 준다.

체크 포인트는 다음과 같다.
1. 자주 실패하는 외부 의존부터 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)한다.
2. 정상/오류/[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시나리오를 모두 만든다.
3. 실제 계약과 응답 형식을 맞춘다.

- **📢 섹션 요약 비유**: 상대 팀 연습경기를 위해 가짜 선수단을 세우는 것이다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 [통합 테스트](/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/)의 독립성과 재현성을 높인다. 외부 시스템이 없어도 안정적인 검증이 가능하다.

결론적으로 이 개념은 "외부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 대신하는 테스트 환경"이다.

- **📢 섹션 요약 비유**: 진짜 길이 막혀도 모형 도로에서 먼저 달려 보는 것이다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/)) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
서비스 가상화 (Service Virtualization) 개념 정립
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

1. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 519 / 973

<- **이전**: [463. Fake (페이크) - 실제 동작하지만 프로덕션에는 적합하지 않은 축소판 (인메모리 DB 등)](/studynote/04_software_engineering/11_testing_validation/855_fake_test_double/)
**다음**: [464. 서비스 가상화 (Service Virtualization) - MSA 환경에서 외부 의존 API를 모사하는 스텁 서버](/studynote/04_software_engineering/11_testing_validation/856_service_virtualization/) ->

---
