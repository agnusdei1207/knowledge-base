+++
title = "336. Contract Testing MSA API 소비자 주도 계약 테스트 (Contract Testing MSA Consumer-Driven Contract Testing Pact CDCT)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Contract Testing ([계약 테스트](/knowledge-base/studynote/15_devops_sre/05_devsecops/266_contract_testing_pact_msa_api/))은 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 인터페이스 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 소비자가 주도해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 방법론이다. 소비자(Consumer)가 기대하는 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답 형식을 "계약(Contract)"으로 정의하고, 공급자([Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/))가 이 계약을 충족하는지 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
> 2. **핵심 문제 해결**: [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) ([End-to-End](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/)) [통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/)는 MSA에서 수십 개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 동시에 실행해야 해 느리고 불안정하다. Contract Testing은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 분리해 독립적으로 빠르게 테스트하면서도 통합 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 보장한다.
> 3. **판단 포인트**: CDCT (Consumer-Driven Contract Testing, 소비자 주도 [계약 테스트](/knowledge-base/studynote/15_devops_sre/05_devsecops/266_contract_testing_pact_msa_api/))의 핵심은 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 변경의 영향 범위를 배포 전에 파악하는 것이다. 공급자가 API를 변경하면 Pact Broker가 자동으로 영향받는 소비자 계약을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

---

## Ⅰ. 개요 및 필요성

MSA에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 문제는 프로덕션 장애의 주요 원인이다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) A가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) B의 응답에서 특정 필드를 기대하는데, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) B가 해당 필드를 제거하거나 타입을 변경하면 A가 장애가 난다.

전통적 방법인 [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트는 이를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하지만 수십 개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 모두 실행해야 하므로 CI에서 실행하기 비현실적이다. [Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) 기반 [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)는 빠르지만 Mock이 실제 공급자와 다를 수 있다([Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) 드리프트).

CDCT는 이 두 문제를 해결한다. 소비자가 [Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) 대신 실제 계약(Pact [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, 공급자가 그 계약으로 자신을 테스트해 실제 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

> 📢 **섹션 요약 비유**: [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트는 전체 오케스트라를 모아 리허설하는 것이고, Contract Testing은 각 악기 파트가 악보(계약)를 보고 독립적으로 연습하면서 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 보장하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------+
|             Pact CDCT 흐름 (소비자 주도 계약 테스트)          |
+------------------------------------------------------------+
|                                                            |
|  [소비자 서비스 (Consumer)]                                 |
|       | 1. Pact Mock Server로 API 호출 테스트               |
|       | 2. 실제 HTTP 상호작용 -> Pact 파일 생성               |
|       v                                                    |
|  +-------------------------------+                         |
|  |  Pact Broker (계약 저장소)      |                        |
|  |  - Pact 파일 저장               |                        |
|  |  - 호환성 매트릭스 관리          |                        |
|  +--------------+----------------+                         |
|                 | 3. 공급자가 계약 검증                      |
|                 v                                          |
|  [공급자 서비스 (Provider)]                                  |
|       | 4. Pact Broker에서 계약 다운로드                     |
|       | 5. 실제 서비스로 계약 재생, 응답 검증                  |
|       v                                                    |
|  ✅ 통과: 배포 가능 / ❌ 실패: 소비자에게 피드백              |
+------------------------------------------------------------+
```

| 항목 | [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트 | Contract Testing (CDCT) |
|:---|:---|:---|
| 실행 속도 | 느림 (모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 실행) | 빠름 ([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분리) |
| 안정성 | 낮음 (여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 의존) | 높음 (독립 실행) |
| 영향 범위 파악 | 배포 후 | 배포 전 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 테스트 환경 | 복잡한 통합 환경 필요 | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립 실행 |

> 📢 **섹션 요약 비유**: Contract Testing은 두 나라가 조약(계약)을 체결하고, 각자 자국에서 조약을 지키는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이다. 매번 두 나라 대표를 모아 회의하지 않아도 된다.

---

## Ⅲ. 비교 및 연결

Pact(Consumer-Driven) vs Spring Cloud Contract([Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/)-Driven):

| 항목 | Pact | Spring Cloud Contract |
|:---|:---|:---|
| 주도권 | 소비자 | 공급자 |
| 언어 지원 | 다국어 (JVM, Ruby, JS, Go) | JVM 중심 |
| 적합 환경 | 폴리글랏 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) | Spring 생태계 |

Can I Deploy: Pact Broker의 기능으로 "현재 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 프로덕션에 배포해도 되는가?"를 자동으로 답해준다. 모든 관련 소비자/공급자 계약이 통과해야 배포가 허용된다.

> 📢 **섹션 요약 비유**: Can I Deploy는 퍼즐 맞추기 전 "이 조각이 여기 맞는가?" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 기능이다. 맞지 않는 조각은 넣지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Contract Testing 도입 단계

1. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 의존성 맵핑 (누가 누구의 API를 호출하는가)
2. 가장 취약한 소비자-공급자 쌍부터 Pact 계약 작성
3. CI에 Pact [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 통합 (소비자 PR에서 계약 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 공급자 CI에서 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))
4. Pact Broker(또는 PactFlow) 설치로 계약 중앙화
5. Can I Deploy 게이트로 배포 전 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 핵심 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 API에 Pact 계약이 정의되어 있는가?
2. 공급자 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 변경 시 CI에서 소비자 계약 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 실행되는가?
3. Pact Broker에서 Can I Deploy가 배포 게이트로 통합되어 있는가?

> 📢 **섹션 요약 비유**: Can I Deploy 없이 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 배포는 블라인드 운전이다. 내 차([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 다른 차들(의존 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))과 충돌하지 않을지 보지 않고 출발한다.

---

## Ⅴ. 기대효과 및 결론

Contract Testing 도입으로 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 문제로 인한 프로덕션 장애가 대폭 감소한다. [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트 의존도가 낮아지고 각 팀이 독립적으로 빠르게 개발·배포할 수 있다.

Contract Testing의 본질은 <strong>"팀 간 신뢰를 코드화"</strong>하는 것이다. [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 계약은 팀 간 대화의 결과물이고, 그 대화가 자동화된 테스트로 지속 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된다.

> 📢 **섹션 요약 비유**: Contract Testing은 공급자와 소비자가 서명한 납품 계약서다. 계약서(Pact [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))가 있으면 품질을 매번 협의하지 않아도 자동으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Contract Testing | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 인터페이스 계약 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| CDCT (Consumer-Driven Contract Testing) | 소비자가 계약을 정의, 공급자가 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| Pact | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) CDCT 프레임워크 |
| Pact Broker | 계약 중앙 저장소, [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 매트릭스 |
| Can I Deploy | 배포 전 계약 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 게이트 |
| [Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) Drift | Mock이 실제 API와 달라지는 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
모놀리식 통합 테스트 시대      MSA Contract Testing 시대       자동화 성숙
----------------------   --------------------------   ------------------------
E2E 통합 테스트 의존     ->  Pact CDCT 등장             ->  Pact Broker/PactFlow
느린 CI 파이프라인            Spring Cloud Contract          Can I Deploy 게이트
Mock 드리프트 문제             소비자-공급자 분리 테스트        API 버전 호환성 매트릭스
                               Pact Broker 중앙화              Bi-directional Contract
```

### 👶 어린이를 위한 3줄 비유 설명

1. Contract Testing은 두 친구가 "내가 이렇게 부르면 너는 이렇게 대답해"라는 약속(계약)을 미리 정해두는 거예요.
2. 약속이 바뀌면 컴퓨터가 자동으로 "이 약속이 맞는지" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해줘요.
3. 덕분에 두 친구가 따로 연습해도 합창할 때 박자가 맞아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 336 / 373

<- **이전**: [335. TDD BDD 인수테스트 Mock 격리 (TDD BDD Acceptance Testing Mock Stub Spy Test Pyramid](/knowledge-base/studynote/15_devops_sre/05_devsecops/335_tdd_bdd/)
**다음**: [337. 뮤테이션 테스트 테스트 케이스 품질 평가 (Mutation Testing Mutant Survived PITest Stryker](/knowledge-base/studynote/15_devops_sre/05_devsecops/337_audit/) ->

---
