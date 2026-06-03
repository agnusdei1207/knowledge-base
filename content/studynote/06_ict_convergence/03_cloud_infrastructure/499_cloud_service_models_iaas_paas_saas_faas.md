+++
title = "499. 클라우드 서비스 모델 통합: IaaS~FaaS (Cloud Service Models IaaS PaaS SaaS FaaS)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [클라우드 서비스 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/201_cloud_service_models_iaas_paas_saas/)은 '제어권 vs 관리 부담'의 트레이드오프로, 위로 갈수록([IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)→[FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)) 관리할 것은 줄고 제어권도 줄어든다.
> 2. **가치**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델을 올바르게 선택하면 운영 비용 절감과 개발 속도 향상을 동시에 달성할 수 있다.
> 3. **판단 포인트**: 레거시 이전은 [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/), 빠른 개발은 [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/), 완제품 구독은 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/), 이벤트 기반 경량 로직은 FaaS로 판단한다.

---

## Ⅰ. 개요 및 필요성

클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 사용자가 직접 관리하는 영역을 어디까지 두느냐에 따라 계층적으로 분류된다. [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)(On-Premises)에서는 하드웨어부터 애플리케이션까지 모두 직접 관리하지만, 클라우드로 이동할수록 벤더가 더 많은 계층을 대신 운영한다.

<strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 모델 스펙트럼</strong>:
- [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)(Infrastructure [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)): CPU, 메모리, 스토리지, 네트워크 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 제공
- [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)(Platform [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)): 런타임, 미들웨어, DB, 배포 파이프라인 제공
- [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)(Software [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)): 완성된 애플리케이션을 구독 방식으로 제공
- [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)(Function [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)): 함수 단위의 실행 환경 — [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/))의 핵심
- [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/)(Backend [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)): [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 푸시, DB 등 백엔드 기능을 API로 제공

기업이 클라우드를 도입할 때 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델 선택은 아키텍처, 비용, 보안 책임 범위를 결정짓는 핵심 판단이다.

- **📢 섹션 요약 비유**: 레스토랑 선택과 같다 — 식재료만 받는 밀키트([IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)), 반조리 음식([PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)), 완성 도시락([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)), 한 입짜리 스낵([FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)). 더 편할수록 내 취향은 덜 반영된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**책임 공유 모델(Shared Responsibility Model)**:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">On-Premises → IaaS → PaaS → SaaS → FaaS</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">계층</div><div class="kb-diagram-cell">On-Prem IaaS PaaS SaaS FaaS</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Application</div><div class="kb-diagram-cell">고객 고객 고객 벤더 벤더</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Runtime</div><div class="kb-diagram-cell">고객 고객 벤더 벤더 벤더</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">OS</div><div class="kb-diagram-cell">고객 고객 벤더 벤더 벤더</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Virtualize</div><div class="kb-diagram-cell">고객 벤더 벤더 벤더 벤더</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Hardware</div><div class="kb-diagram-cell">고객 벤더 벤더 벤더 벤더</div></div>
<div class="kb-diagram-note">고객 관리 ◀ 벤더 관리 ▶</div>
</div>
</div>



| 모델 | 제어권 | 관리 부담 | 대표 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 적합 사례 |
|:---|:---:|:---:|:---|:---|
| [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) | 높음 | 높음 | AWS EC2, Azure [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 레거시 [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift |
| [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) | 중간 | 중간 | Heroku, GCP App Engine | 웹 앱 개발 |
| [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) | 낮음 | 낮음 | Salesforce, Google Workspace | 사무 생산성 |
| [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) | 낮음 | 매우 낮음 | AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), Azure Functions | 이벤트 처리 |
| [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) | 낮음 | 낮음 | Firebase, AWS Amplify | 모바일 앱 |

FaaS는 요청이 없을 때 비용이 발생하지 않는 **이벤트 드리븐(Event-Driven)** 모델로, 트래픽 패턴이 불규칙한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 최적이다. 단, [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)([Cold Start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/)) 지연이 존재한다.

- **📢 섹션 요약 비유**: IaaS는 빈 땅에 건물 짓기, PaaS는 인테리어만 하면 되는 분양 아파트, SaaS는 호텔 체크인, FaaS는 픽업 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) — 편하지만 경로는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 정한다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a> vs <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/">PaaS</a> 선택 기준</strong>:
- 실행 시간이 짧고(< 15분), 이벤트 기반 → [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)
- 장기 실행 프로세스, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 유지 필요 → [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 또는 CaaS([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))

<strong>BaaS와 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a> 결합</strong> = [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 풀스택: 프론트엔드는 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/), 백엔드는 [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) + [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) + Cognito 조합으로 서버 관리 없이 완전한 앱 구성 가능.

- **📢 섹션 요약 비유**: FaaS와 PaaS의 차이는 대리운전(호출 시만 요금)과 전속 기사(월 고정급) 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. 주어진 시나리오의 워크로드 특성(상태 유지 여부, 실행 시간, 트래픽 패턴)을 분석한다.
2. 책임 공유 모델에서 보안 책임 범위를 명확히 기술한다 — IaaS는 OS 패치가 고객 책임.
3. 비용 모델 차이: IaaS는 시간 단위 과금, FaaS는 호출 수 + 실행 시간 × 메모리.

**실무 시나리오**: 금융사 시스템 클라우드 전환 시 — 핵심 OLTP는 [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)(제어권 확보), 개발/테스트 환경은 [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)(속도), 이메일/협업은 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/), 배치 리포트는 [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)(야간 5분 실행)로 혼합 적용.

- **📢 섹션 요약 비유**: 올바른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델 선택은 음식점 선택과 같다 — 데이트엔 레스토랑([PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)), 혼밥엔 편의점([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)), 파티엔 케이터링([IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)), 출출할 때 자판기([FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)).

---

## Ⅴ. 기대효과 및 결론

[클라우드 서비스 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/201_cloud_service_models_iaas_paas_saas/)을 업무 특성에 맞게 선택하면:
- **비용 최적화**: 필요한 계층만 구매하여 과잉 투자 방지
- **운영 효율화**: 관리 부담 감소로 개발팀이 비즈니스 로직에 집중
- **민첩성 향상**: [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)/[FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 활용으로 배포 주기 단축(주 → 시간 단위)
- **보안 명확성**: 책임 공유 모델로 보안 공백 방지

결국 [클라우드 서비스 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/201_cloud_service_models_iaas_paas_saas/) 선택은 <strong>기술 문제가 아닌 비즈니스 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 결정</strong>이다.

- **📢 섹션 요약 비유**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델은 도구 선택이다. 못 박기에 드릴을 쓰지 않듯, 워크로드에 맞는 모델을 골라야 비용과 복잡성을 동시에 잡는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) (Infrastructure [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/), [Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) · 503 |
| [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) (Function [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | [Cold Start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/), [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) · 503 |
| 책임 공유 모델 (Shared Responsibility Model) | 보안, 컴플라이언스, OS 패치 · 500 |
| [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) (Backend [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | Firebase, Cognito, 모바일 백엔드 · 505 |
| [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) | 이벤트 드리븐, 스케일 투 제로 · 503 |

### 📈 관련 키워드 및 발전 흐름도

```text
[VM · 가상화] → [클라우드 서비스 모델 통합: IaaS~FaaS] → [이벤트 드리븐 · 스케일 투 제로]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 레고 블록([IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/))을 직접 조립하거나, 반쯤 완성된 세트([PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/))를 사거나, 완성된 장난감([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/))을 살 수 있어요.
2. 버튼 한 번에 동작하는 자판기 음식([FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/))은 기다리지 않아도 되지만, 내 입맛대로 바꾸기는 어려워요.
3. 편할수록 내가 조절할 수 있는 건 줄어들지만, 신경 써야 할 것도 함께 줄어든답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 499 / 552

← **이전**: [498. 스마트 팩토리, CPS, 마이크로그리드 통합 (Smart Factory CPS Microgrid Integration)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/498_smart_factory_cps_microgrid_integration/)
**다음**: [500. 멀티 클라우드 전략과 벤더 종속성 회피 (Multi-Cloud Strategy and Vendor Lock-in Avoidance)](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/500_multi_cloud_vendor_lock_in_avoidance/) →

---
