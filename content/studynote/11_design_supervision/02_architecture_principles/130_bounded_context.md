+++
title = "130. 바운디드 컨텍스트 (Bounded Context)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) ([Bounded Context](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/))는 DDD의 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 패턴으로, 특정 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델이 유효하고 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 있게 적용되는 명확한 경계를 정의한다. 동일한 용어('고객')도 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)(주문 BC의 고객 vs 마케팅 BC의 고객)에 따라 다른 속성과 의미를 가질 수 있음을 명시적으로 구분한다.
> 2. **가치**: [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)는 MSA에서 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)의 경계를 결정하는 가장 신뢰할 수 있는 기준이며, 각 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)는 자신의 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스토리지, [유비쿼터스 언어](/knowledge-base/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/)를 소유하여 다른 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)와의 결합도를 낮춘다.
> 3. **판단 포인트**: [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 맵 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Map)은 [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) 간의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)(상류/하류, 공유 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/), [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/), Open Host [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 시각화하여 통합 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 명시적으로 결정하는 필수 산출물이며, 이것 없이는 BC 간 암묵적 의존성이 시스템을 다시 모놀리식으로 만든다.

---

## Ⅰ. 개요 및 필요성

소프트웨어에서 하나의 단어가 여러 의미를 가지면 모호성이 발생한다. '고객([Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/))'은 주문 시스템에서는 '배송 주소를 가진 구매자'이고, 마케팅 시스템에서는 '구매 이력을 가진 세그먼트 대상'이며, [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) 시스템에서는 '담당 영업사원과 연결된 계정'이다.

[바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)는 이 모호성을 해결한다. 각 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)는 자신만의 언어와 모델을 갖고, [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 경계 밖에서는 그 모델이 의미 없거나 다른 의미를 가진다고 명시적으로 선언한다.

```text
┌─────────────────────────────────────────────────────────────┐
│         동일 용어의 컨텍스트별 의미 차이                      │
├─────────────────────────────────────────────────────────────┤
│  [주문 바운디드 컨텍스트]          [마케팅 바운디드 컨텍스트] │
│  Customer: {                      Customer: {               │
│    orderId, shippingAddr,           segment, purchaseHist,  │
│    paymentMethod                    campaignTargets          │
│  }                                }                         │
│                                                             │
│  같은 'Customer'이지만 완전히 다른 모델 → BC로 명확히 분리  │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 국제법([컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 맵)에서 '국경([바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/))'이 각 나라의 주권([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델)이 유효한 영역을 정한다. 한국법은 한국 영토에서만 유효하고, 미국법은 미국 영토에서 유효하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 맵([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Map)은 [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) 간의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 시각화한다. 주요 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 패턴은 다음과 같다. ① 공유 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(Shared [Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)): 두 BC가 작은 공통 모델을 함께 소유·유지, ② 고객-공급자([Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/)-Supplier): 상류 BC가 하류 BC를 위한 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 제공, ③ 준수자(Conformist): 하류 BC가 상류 BC 모델을 그대로 따름, ④ [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)(Anti-Corruption Layer): 외부 모델을 변환하는 방어 레이어.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 공유 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) | 두 BC가 공통 모델 공유 | 높음 |
| 고객-공급자 | 상류 BC가 하류 BC 위해 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 제공 | 중간 |
| [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([부패 방지 레이어](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/133_anti_corruption_layer/)) | 외부 모델 변환으로 내부 모델 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | 낮음 |
| 오픈 호스트 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 공개 API로 다수 하류 BC 지원 | 낮음 |

```text
┌─────────────────────────────────────────────────────────────┐
│           컨텍스트 맵 예시 (전자상거래)                       │
├─────────────────────────────────────────────────────────────┤
│  [카탈로그 BC] ──Open Host──> [주문 BC] ──고객-공급자──>     │
│                                   │             [결제 BC]   │
│                                   │                         │
│                                ACL 변환                      │
│                                   │                         │
│                              [외부 PG API]                  │
│                              (외부 결제사 모델 차단)          │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 외교관([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))은 두 나라(BC)가 언어·문화가 달라도 서로 소통할 수 있게 해주는 중재자로, 한 나라의 문화(모델)가 다른 나라를 오염시키지 않게 막는다.

---
## Ⅲ. 비교 및 연결

[바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)와 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에서 흔한 오해는 '1 BC = 1 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)'가 강제 규칙이라는 것이다. 1 BC는 1개 이상의 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)로 구현될 수 있으며, 성숙도에 따라 처음에는 1 BC = 1 모듈러 모놀리스로 시작하고 나중에 분리할 수 있다.

| 비교 축 | A | B |
|:---|:---|:---|
| 모델 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 전체 앱에서 하나의 [Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) | BC마다 독립된 [Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) 모델 |
| 변경 영향 | [Customer](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) 변경이 전체 영향 | 해당 BC 내에서만 영향 |
| 팀 자율성 | 낮음 | 높음 |
| [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용 | 낮음 | 높음 (경계 설계 필요) |

- **📢 섹션 요약 비유**: 국가(BC) 내에서는 자국 통화(모델)가 유효하지만, 국경을 넘을 때는 환전([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)·번역)이 필요하다. 각 국가가 독립된 통화 체계를 가져야 통화 위기(모델 오염)가 전파되지 않는다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) 경계 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)의 가장 어려운 실무 문제는 '경계를 너무 작게 나누는 것'이다. 경계가 너무 작으면 BC 간 호출이 많아져 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 문제가 심화된다. Event Storming 워크숍을 통해 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문가와 함께 자연스러운 경계를 찾는 것이 권장된다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 각 [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)가 독립된 [유비쿼터스 언어](/knowledge-base/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/)와 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델을 갖고 있는가?
2. [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 맵이 작성되어 BC 간 통합 패턴([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/), Open Host 등)이 명시되어 있는가?
3. 동일 용어가 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)마다 다른 의미를 갖는 경우가 명확히 문서화되어 있는가?
4. BC 경계가 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계와 정렬되어 있는가?
5. BC 경계가 너무 작아 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 문제를 과도하게 유발하지 않는가?

- **📢 섹션 요약 비유**: 지도에서 나라의 경계를 그릴 때 강·산맥 같은 자연적 경계([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자연적 경계)를 따라 그리면 오래 유지되지만, 인위적으로 직선(임의 분리)으로 그으면 분쟁(모델 충돌)이 끊이지 않는다.

---

## Ⅴ. 기대효과 및 결론

[바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)를 올바르게 설계하면 각 팀이 자신의 BC를 자율적으로 발전시킬 수 있어 개발 속도가 향상된다. 모델 오염 없이 각 BC가 최적화된 기술 스택과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스토리지를 선택할 수 있다.

한계는 BC 경계 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 자체가 어렵고, 잘못된 경계는 과도한 BC 간 통신과 [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 문제를 야기한다. [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 맵 유지보수가 지속적으로 필요하다.

미래 방향으로는 ① Event Storming 자동화 도구, ② [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 코드 분석을 통한 BC 경계 추천, ③ [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)·Event Sourcing과 BC의 자연스러운 통합이 발전하고 있다.

- **📢 섹션 요약 비유**: 도시 구획(BC 경계) 설계를 잘 하면 상업지구·주거지구가 서로 방해하지 않고 각자 발전하지만, 구획이 잘못되면 도시 기능이 혼재되어 교통 체증(시스템 병목)이 발생한다.

---

### 📌 관련 개념 맵

DDD [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 설계] → [바운디드 컨텍스트] → [컨텍스트 맵] → MSA [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계] → ACL·Event 통합]

| 개념 | 연결 포인트 |
|:---|:---|
| [DDD](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/) ([Domain-Driven Design](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/127_ddd_domain_driven_design/)) | [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)의 이론적 기반 |
| [유비쿼터스 언어](/knowledge-base/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/) | BC 내에서만 유효한 공통 언어 |
| [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) (Anti-Corruption Layer) | BC 간 모델 오염 방지 변환 레이어 |
| Event Storming | BC 경계를 자연스럽게 찾는 워크숍 방법론 |

### 📈 관련 키워드 및 발전 흐름도

[모놀리식 단일 모델 오염] → DDD [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) 패턴] → [컨텍스트 맵 통합 전략] → MSA [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계 정렬] → [Event Storming 워크숍] → AI 경계 추천]

### 👶 어린이를 위한 3줄 비유 설명

1. [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)는 나라(경계)마다 같은 단어가 다른 뜻을 가질 수 있다는 걸 인정해요.
2. 예를 들어 '고객'이란 단어가 주문 시스템과 마케팅 시스템에서 다른 의미를 가질 수 있어요.
3. 경계를 명확히 하면 한 팀의 변경이 다른 팀에 영향을 주지 않아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 530

← **이전**: [129. 도메인 주도 설계 (DDD: Domain-Driven Design)](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/129_ddd_domain_driven_design/)
**다음**: [131. 에그리게이트 루트 (Aggregate Root)](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/131_aggregate_root/) →

---
