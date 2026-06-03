---
title: 336. Contract Testing MSA API 소비자 주도 계약 테스트 (Contract Testing MSA Consumer-Driven
  Contract Testing Pact CDCT)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Contract Testing ([[266_contract_testing_pact_msa_api|계약 테스트]])은 [[619_msa_traffic_hardware|MSA]] ([[122_msa_microservices_architecture|Microservices Architecture]]) 환경에서 [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[014_api_posix|API]] 인터페이스 [[344_compatibility_usability|호환성]]을 소비자가 주도해 [[395_verification_process_review|검증]]하는 방법론이다. 소비자(Consumer)가 기대하는 [[014_api_posix|API]] 응답 형식을 "계약(Contract)"으로 정의하고, 공급자([[150_soa_triangle_architecture|Provider]])가 이 계약을 충족하는지 자동 [[395_verification_process_review|검증]]한다.
> 2. **핵심 문제 해결**: [[265_e2e_end_to_ui_selenium|E2E]] ([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) [[400_integration_testing|통합 테스트]]는 MSA에서 수십 개 [[090_service_kubernetes_network_load_balancing|서비스]]를 동시에 실행해야 해 느리고 불안정하다. Contract Testing은 [[090_service_kubernetes_network_load_balancing|서비스]]를 분리해 독립적으로 빠르게 테스트하면서도 통합 [[344_compatibility_usability|호환성]]을 보장한다.
> 3. **판단 포인트**: CDCT (Consumer-Driven Contract Testing, 소비자 주도 [[266_contract_testing_pact_msa_api|계약 테스트]])의 핵심은 [[014_api_posix|API]] 변경의 영향 범위를 배포 전에 파악하는 것이다. 공급자가 API를 변경하면 Pact Broker가 자동으로 영향받는 소비자 계약을 [[395_verification_process_review|검증]]한다.

---

## Ⅰ. 개요 및 필요성

MSA에서 [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[014_api_posix|API]] [[344_compatibility_usability|호환성]] 문제는 프로덕션 장애의 주요 원인이다. [[090_service_kubernetes_network_load_balancing|서비스]] A가 [[090_service_kubernetes_network_load_balancing|서비스]] B의 응답에서 특정 필드를 기대하는데, [[090_service_kubernetes_network_load_balancing|서비스]] B가 해당 필드를 제거하거나 타입을 변경하면 A가 장애가 난다.

전통적 방법인 [[265_e2e_end_to_ui_selenium|E2E]] 테스트는 이를 [[395_verification_process_review|검증]]하지만 수십 개 [[090_service_kubernetes_network_load_balancing|서비스]]를 모두 실행해야 하므로 CI에서 실행하기 비현실적이다. [[462_mock_test_double|Mock]] 기반 [[397_unit_test|단위 테스트]]는 빠르지만 Mock이 실제 공급자와 다를 수 있다([[462_mock_test_double|Mock]] 드리프트).

CDCT는 이 두 문제를 해결한다. 소비자가 [[462_mock_test_double|Mock]] 대신 실제 계약(Pact [[501_file_definition_logical_record|파일]])을 [[087_process_state_transition|생성]]하고, 공급자가 그 계약으로 자신을 테스트해 실제 [[344_compatibility_usability|호환성]]을 [[395_verification_process_review|검증]]한다.

> 📢 **섹션 요약 비유**: [[265_e2e_end_to_ui_selenium|E2E]] 테스트는 전체 오케스트라를 모아 리허설하는 것이고, Contract Testing은 각 악기 파트가 악보(계약)를 보고 독립적으로 연습하면서 [[344_compatibility_usability|호환성]]을 보장하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌────────────────────────────────────────────────────────────┐
│             Pact CDCT 흐름 (소비자 주도 계약 테스트)          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [소비자 서비스 (Consumer)]                                 │
│       │ 1. Pact Mock Server로 API 호출 테스트               │
│       │ 2. 실제 HTTP 상호작용 → Pact 파일 생성               │
│       ▼                                                    │
│  ┌───────────────────────────────┐                         │
│  │  Pact Broker (계약 저장소)      │                        │
│  │  - Pact 파일 저장               │                        │
│  │  - 호환성 매트릭스 관리          │                        │
│  └──────────────┬────────────────┘                         │
│                 │ 3. 공급자가 계약 검증                      │
│                 ▼                                          │
│  [공급자 서비스 (Provider)]                                  │
│       │ 4. Pact Broker에서 계약 다운로드                     │
│       │ 5. 실제 서비스로 계약 재생, 응답 검증                  │
│       ▼                                                    │
│  ✅ 통과: 배포 가능 / ❌ 실패: 소비자에게 피드백              │
└────────────────────────────────────────────────────────────┘
```

| 항목 | [[265_e2e_end_to_ui_selenium|E2E]] 테스트 | Contract Testing (CDCT) |
|:---|:---|:---|
| 실행 속도 | 느림 (모든 [[090_service_kubernetes_network_load_balancing|서비스]] 실행) | 빠름 ([[090_service_kubernetes_network_load_balancing|서비스]] 분리) |
| 안정성 | 낮음 (여러 [[090_service_kubernetes_network_load_balancing|서비스]] 의존) | 높음 (독립 실행) |
| 영향 범위 파악 | 배포 후 | 배포 전 자동 [[395_verification_process_review|검증]] |
| 테스트 환경 | 복잡한 통합 환경 필요 | 각 [[090_service_kubernetes_network_load_balancing|서비스]] 독립 실행 |

> 📢 **섹션 요약 비유**: Contract Testing은 두 나라가 조약(계약)을 체결하고, 각자 자국에서 조약을 지키는지 [[396_validation|확인]]하는 것이다. 매번 두 나라 대표를 모아 회의하지 않아도 된다.

---

## Ⅲ. 비교 및 연결

Pact(Consumer-Driven) vs Spring Cloud Contract([[150_soa_triangle_architecture|Provider]]-Driven):

| 항목 | Pact | Spring Cloud Contract |
|:---|:---|:---|
| 주도권 | 소비자 | 공급자 |
| 언어 지원 | 다국어 (JVM, Ruby, JS, Go) | JVM 중심 |
| 적합 환경 | 폴리글랏 [[619_msa_traffic_hardware|MSA]] | Spring 생태계 |

Can I Deploy: Pact Broker의 기능으로 "현재 [[288_version_ihl_tos_total_length|버전]]을 프로덕션에 배포해도 되는가?"를 자동으로 답해준다. 모든 관련 소비자/공급자 계약이 통과해야 배포가 허용된다.

> 📢 **섹션 요약 비유**: Can I Deploy는 퍼즐 맞추기 전 "이 조각이 여기 맞는가?" [[396_validation|확인]] 기능이다. 맞지 않는 조각은 넣지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Contract Testing 도입 단계

1. [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[014_api_posix|API]] 의존성 맵핑 (누가 누구의 API를 호출하는가)
2. 가장 취약한 소비자-공급자 쌍부터 Pact 계약 작성
3. CI에 Pact [[395_verification_process_review|검증]] 통합 (소비자 PR에서 계약 [[087_process_state_transition|생성]], 공급자 CI에서 [[395_verification_process_review|검증]])
4. Pact Broker(또는 PactFlow) 설치로 계약 중앙화
5. Can I Deploy 게이트로 배포 전 [[344_compatibility_usability|호환성]] 자동 [[395_verification_process_review|검증]]

### [[435_checklist_based_testing|체크리스트]]

1. 핵심 [[090_service_kubernetes_network_load_balancing|서비스]] 간 API에 Pact 계약이 정의되어 있는가?
2. 공급자 [[014_api_posix|API]] 변경 시 CI에서 소비자 계약 자동 [[395_verification_process_review|검증]]이 실행되는가?
3. Pact Broker에서 Can I Deploy가 배포 게이트로 통합되어 있는가?

> 📢 **섹션 요약 비유**: Can I Deploy 없이 [[619_msa_traffic_hardware|MSA]] 배포는 블라인드 운전이다. 내 차([[090_service_kubernetes_network_load_balancing|서비스]])가 다른 차들(의존 [[090_service_kubernetes_network_load_balancing|서비스]])과 충돌하지 않을지 보지 않고 출발한다.

---

## Ⅴ. 기대효과 및 결론

Contract Testing 도입으로 [[619_msa_traffic_hardware|MSA]] 환경에서 [[014_api_posix|API]] [[344_compatibility_usability|호환성]] 문제로 인한 프로덕션 장애가 대폭 감소한다. [[265_e2e_end_to_ui_selenium|E2E]] 테스트 의존도가 낮아지고 각 팀이 독립적으로 빠르게 개발·배포할 수 있다.

Contract Testing의 본질은 **"팀 간 신뢰를 코드화"**하는 것이다. [[014_api_posix|API]] 계약은 팀 간 대화의 결과물이고, 그 대화가 자동화된 테스트로 지속 [[395_verification_process_review|검증]]된다.

> 📢 **섹션 요약 비유**: Contract Testing은 공급자와 소비자가 서명한 납품 계약서다. 계약서(Pact [[501_file_definition_logical_record|파일]])가 있으면 품질을 매번 협의하지 않아도 자동으로 [[395_verification_process_review|검증]]된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Contract Testing | [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[014_api_posix|API]] 인터페이스 계약 [[395_verification_process_review|검증]] |
| CDCT (Consumer-Driven Contract Testing) | 소비자가 계약을 정의, 공급자가 [[395_verification_process_review|검증]] |
| Pact | [[191_oss_license_compliance|오픈소스]] CDCT 프레임워크 |
| Pact Broker | 계약 중앙 저장소, [[344_compatibility_usability|호환성]] 매트릭스 |
| Can I Deploy | 배포 전 계약 [[344_compatibility_usability|호환성]] 자동 [[395_verification_process_review|검증]] 게이트 |
| [[462_mock_test_double|Mock]] Drift | Mock이 실제 API와 달라지는 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
모놀리식 통합 테스트 시대      MSA Contract Testing 시대       자동화 성숙
──────────────────────   ──────────────────────────   ────────────────────────
E2E 통합 테스트 의존     →  Pact CDCT 등장             →  Pact Broker/PactFlow
느린 CI 파이프라인            Spring Cloud Contract          Can I Deploy 게이트
Mock 드리프트 문제             소비자-공급자 분리 테스트        API 버전 호환성 매트릭스
                               Pact Broker 중앙화              Bi-directional Contract
```

### 👶 어린이를 위한 3줄 비유 설명

1. Contract Testing은 두 친구가 "내가 이렇게 부르면 너는 이렇게 대답해"라는 약속(계약)을 미리 정해두는 거예요.
2. 약속이 바뀌면 컴퓨터가 자동으로 "이 약속이 맞는지" [[396_validation|확인]]해줘요.
3. 덕분에 두 친구가 따로 연습해도 합창할 때 박자가 맞아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 336 / 373

← **이전**: [[335_tdd_bdd|335. TDD BDD 인수테스트 Mock 격리 (TDD BDD Acceptance Testing Mock Stub Spy Test Pyramid]]
**다음**: [[337_audit|337. 뮤테이션 테스트 테스트 케이스 품질 평가 (Mutation Testing Mutant Survived PITest Stryker]] →

---
