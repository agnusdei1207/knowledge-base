+++
title = "156. 서버리스 벤더 락인과 Knative (Vendor Lock-in / Knative)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) (Function [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 각 벤더 고유의 이벤트 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 형식, SDK에 종속되어 코드·인프라를 다른 클라우드로 이식하기 어려운 벤더 락인 ([Vendor Lock-in](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/254_cloud_vendor_lock_in_avoidance_portability_multi_cloud/)) 리스크를 내포한다.
> 2. **가치**: Knative, OpenFaaS 같은 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 프레임워크를 활용하면 [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 위에서 벤더 중립적 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 환경을 구축해 이식성을 보장할 수 있다.
> 3. **판단 포인트**: 단일 벤더 생태계를 깊이 활용할수록 생산성이 높지만 전환 비용도 증가하므로, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 이식성 요구 수준과 운영 복잡도를 기준으로 락인 허용 범위를 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), Azure Functions, Google Cloud Functions는 강력하지만 각기 다른 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 인터페이스, [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 이벤트 형식, 배포 도구를 사용한다. Lambda의 이벤트 핸들러 함수 서명, EventBridge 규칙 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), SAM ([Serverless Application Model](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/113_aws_sam_serverless_model/)) 템플릿은 다른 벤더로 그대로 이전할 수 없다.

이 현상을 벤더 락인 ([Vendor Lock-in](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/254_cloud_vendor_lock_in_avoidance_portability_multi_cloud/))이라고 한다. [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)에서 특히 락인이 강한 이유는 실행 환경, 이벤트 소스, 인프라(네트워크, [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 등)가 벤더 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 깊이 통합되어 있어, 단순히 코드를 복사하는 것만으로는 이전이 불완전하기 때문이다.

기업 입장에서 특정 벤더에 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적으로 수 년간 의존하다 계약 조건·비용·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 등의 이유로 이전해야 할 상황이 오면 막대한 재작성 비용이 발생한다. 이를 방지하기 위해 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 레이어를 벤더 위에 올리거나, [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층을 설계하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필요하다.

📢 **섹션 요약 비유**: 벤더 락인은 특정 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 전용 소프트웨어 — Windows에서만 돌아가는 프로그램을 만들면 Mac으로 옮기려 할 때 처음부터 다시 만들어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) | Knative ([오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)) |
|:---|:---|:---|
| 실행 환경 | 벤더 관리 (불투명) | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 위 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) |
| 이벤트 모델 | 벤더 고유 형식 | CloudEvents 표준 |
| 배포 도구 | 벤더 CLI/콘솔 | [kubectl](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/077_kube_api_server_k8s_hub/), Tekton |
| 자동 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) | 벤더 자동 | Knative Autoscaler (KPA/[HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/)) |
| 이식성 | 어려움 | 모든 K8s 클러스터에서 동일 |
| 운영 부담 | 낮음 | 중간~높음 (K8s 관리 필요) |

```text
+----------------------------------------------------------------------+
|                  Knative 아키텍처 개요                               |
|                                                                      |
|  +---------------------------------------------------------------+  |
|  |                   Knative 레이어                              |  |
|  |                                                               |  |
|  |  +------------------+     +------------------------------+  |  |
|  |  |  Knative Serving |     |  Knative Eventing            |  |  |
|  |  |                  |     |                              |  |  |
|  |  |  -> HTTP 트래픽   |     |  -> CloudEvents 표준          |  |  |
|  |  |  -> 자동 스케일링 |     |  -> Broker/Trigger 라우팅    |  |  |
|  |  |  -> 0->N 스케일아웃|     |  -> Kafka/RabbitMQ 연동      |  |  |
|  |  |  -> 트래픽 분할   |     |                              |  |  |
|  |  +------------------+     +------------------------------+  |  |
|  +---------------------------------------------------------------+  |
|                         |                                           |
|  +---------------------- |--------------------------------------+  |
|  |          Kubernetes (GKE, EKS, AKS, on-prem)                 |  |
|  +--------------------------------------------------------------+  |
+----------------------------------------------------------------------+
```

📢 **섹션 요약 비유**: Knative는 범용 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)(USB-C) — 어떤 벤더의 기기(클라우드)에도 연결 가능하도록 표준 인터페이스를 제공한다.

---

## Ⅲ. 비교 및 연결

| 구분 | AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | Knative | OpenFaaS |
|:---|:---|:---|:---|
| 환경 | 완전 관리형 | K8s 필요 | K8s/[Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) Swarm |
| 이식성 | 낮음 | 높음 | 높음 |
| 운영 복잡도 | 낮음 | 중간 | 낮음~중간 |
| 이벤트 표준 | 벤더 고유 | CloudEvents | 다양 |
| 스케일 투 제로 | 지원 | 지원 | 지원 |
| 성숙도 | 매우 높음 | 높음 | 중간 |

<strong>탈출 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> (Exit <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">Strategy</a>) 설계</strong>
1. <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a> <a href="/knowledge-base/studynote/11_design_supervision/06_exam_summary/383_adapter_pattern_summary/">어댑터 패턴</a></strong>: 벤더 이벤트 형식을 내부 공통 형식으로 변환하는 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 계층 추가
2. **CloudEvents 표준 채택**: [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) ([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation) CloudEvents 스펙으로 이벤트 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 이미지 기반 배포</strong>: 함수를 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지로 패키징 -> Knative/[Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 모두 실행 가능
4. <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">인프라 코드</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a></strong>: [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), Pulumi로 벤더 리소스 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)

📢 **섹션 요약 비유**: CloudEvents 표준은 국제 표준 규격 콘센트 — 각국 콘센트 모양이 달라도 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 하나로 어디서나 전기를 쓸 수 있게 해준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>락인 수준별 대응 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>
- <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>적 락인 허용</strong>: 단일 벤더 올인으로 생산성 극대화, 탈출 비용은 장기 계획에 반영
- **아키텍처적 격리**: 비즈니스 로직을 벤더 API와 분리 ([헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) 적용)
- **Knative 하이브리드**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)·멀티클라우드 요구 시 Knative로 동일 [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 환경 구현
- <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/454_portability_test/">이식성 테스트</a></strong>: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인에 다른 환경 실행 테스트 포함

**기술사 시험 포인트**
- 벤더 락인의 세 유형(기술적, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 계약적)을 구분하고 [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 맥락에서 설명
- Knative Serving([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 트래픽 관리)과 Knative Eventing(이벤트 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))의 역할 구분
- CloudEvents 표준의 의미와 채택 이유

📢 **섹션 요약 비유**: 락인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 결정은 아파트 분양 vs 전세 — 분양(깊은 락인)은 장기 거주가 확정이면 경제적이지만 이사가 힘들고, 전세(이식성 확보)는 자유롭지만 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 세팅 비용이 있다.

---

## Ⅴ. 기대효과 및 결론

벤더 락인 리스크를 인식하고 적절한 수준의 이식성 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 설계하면, 비즈니스 요구가 변할 때 클라우드 전환 비용과 중단 리스크를 최소화할 수 있다. Knative는 특히 멀티클라우드·[하이브리드 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 채택한 대기업에서 실질적인 대안으로 채택되고 있다.

완전한 이식성은 운영 복잡도 증가를 수반한다. K8s 클러스터를 직접 관리하는 Knative 환경은 Lambda보다 훨씬 높은 운영 역량을 요구한다. 따라서 이식성 필요성이 명확하게 입증된 경우에만 Knative로 전환하고, 그 외에는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 레이어 + CloudEvents 표준 채택만으로 리스크를 관리하는 것이 현실적이다.

📢 **섹션 요약 비유**: Knative 도입은 자가 발전 설비 설치 — 전력 회사(벤더)에 종속되지 않는 자유를 얻지만, 발전기 관리(K8s 운영)라는 새로운 책임이 따른다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| Knative Serving | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 기반 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 워크로드 자동 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| Knative Eventing | CloudEvents 기반 이벤트 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |
| CloudEvents | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 이벤트 표준, 벤더 중립 이식성 |
| OpenFaaS | Knative 대안 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) 프레임워크 |
| [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) | 비즈니스 로직을 외부 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)에서 격리 |
| [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) ([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation) | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 표준 관리 단체 |

### 👶 어린이를 위한 3줄 비유 설명
1. 벤더 락인은 특정 회사 게임기 전용 게임 — PS5 게임은 Xbox에서 못 해요, 클라우드 함수도 마찬가지예요.

### 📈 관련 키워드 및 발전 흐름도

```text
CSP 전용 FaaS (벤더 종속)
    |
    v
Knative: K8s 기반 오픈소스 서버리스 프레임워크
    +-► Serving: 자동 스케일링 · 리비전 관리
    +-► Eventing: 이벤트 소스 바인딩
    |
    v
Cloud-Agnostic 서버리스 -> 멀티클라우드 이식성
```
2. Knative는 모든 게임기에서 돌아가는 온라인 게임 — 어느 회사 기기에서도 같은 게임을 즐길 수 있어요.
3. 자유롭게 게임기를 바꿀 수 있지만, 그러려면 온라인 게임 서버([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))를 직접 관리해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 155 / 371

<- **이전**: [155. 이벤트 트리거 기반 실행 (Event Trigger Serverless)](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/155_event_trigger_serverless_architecture/)
**다음**: [157. BFF / GraphQL API 집계 (BFF Pattern / GraphQL)](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/157_bdi_graphql_api_aggregation/) ->

---
