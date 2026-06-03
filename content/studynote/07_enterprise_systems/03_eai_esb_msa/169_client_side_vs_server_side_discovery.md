+++
title = "169. 클라이언트 사이드 디스커버리 (Client-side Discovery) vs 서버 사이드 디스커버리"
date = 2026-04-10

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/)에서 차이는 "누가 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)를 조회하고 인스턴스를 고르는가"에 있다. 호출 애플리케이션이 직접 하면 클라이언트 사이드, [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)나 로드밸런서가 대신하면 서버 사이드다.
> 2. **가치**: 클라이언트 사이드는 홉이 적고 세밀한 제어가 가능하지만 애플리케이션 복잡도가 올라가고, 서버 사이드는 호출자 단순화와 중앙 통제가 쉽지만 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층의 운영이 중요해진다.
> 3. **판단 포인트**: 현대 플랫폼은 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) ([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)), [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/), 클라우드 로드밸런서 덕분에 서버 사이드를 선호하지만, 저지연 직접 호출이나 특수 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 제어가 필요하면 클라이언트 사이드도 여전히 유효하다.

---

## Ⅰ. 개요 및 필요성

클라이언트 사이드 디스커버리와 서버 사이드 디스커버리는 [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservice Architecture](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/365_msa_microservice_architecture/))에서 동적으로 바뀌는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 위치를 어떻게 해석할지에 대한 두 가지 책임 분담 방식이다. 둘 다 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이름과 실제 인터넷 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 주소 (IP, Internet [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))·[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) ([Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))를 분리한다는 점은 같지만, 조회와 선택을 누가 담당하는지가 다르다.

이 문제가 중요해진 이유는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), 오토스케일링, [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/) 환경에서 인스턴스 주소가 계속 변하기 때문이다. 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 2개에서 10개로 늘어나거나 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)로 새 노드에 떠도, 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 고정 IP를 몰라도 계속 호출할 수 있어야 한다. 그래서 "[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 위치를 누가 알아서 해결할 것인가"가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 설계의 핵심 질문이 된다.

결국 두 패턴의 차이는 단순 네트워크 홉 수가 아니라 애플리케이션과 인프라의 경계선에 있다. 클라이언트가 더 똑똑해질수록 제어력은 커지지만 코드가 무거워지고, 인프라가 더 많은 책임을 질수록 호출자는 단순해지지만 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층 품질이 중요해진다.

- **📢 섹션 요약 비유**: 직접 주소록을 뒤져 친구 집을 찾아갈지, 콜센터에 목적지만 말하고 길 안내를 맡길지의 차이라고 보면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

두 방식 모두 기본 재료는 같다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), 헬스 체크, 로드밸런싱 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 만료 처리, 재시도와 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)이 필요하다. 다만 클라이언트 사이드는 애플리케이션이 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)를 직접 조회해 살아 있는 인스턴스 목록을 가져오고, 서버 사이드는 로드밸런서나 애플리케이션 프로그래밍 인터페이스 ([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 게이트웨이가 이를 대신 수행한다.

| 구성 요소 | 클라이언트 사이드에서의 역할 | 서버 사이드에서의 역할 |
| :--- | :--- | :--- |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | 클라이언트가 직접 조회 | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)·로드밸런서가 조회 |
| 로드밸런싱 로직 | 애플리케이션 내부 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | 중앙 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 또는 플랫폼 계층 |
| 호출 코드 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 선택 책임 포함 | 목적지 이름만 전달 |
| 장애 전파 제어 | 클라이언트별 구현 품질 차이 큼 | 중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 쉬움 |

아래 그림은 두 패턴의 호출 흐름 차이를 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Who owns service instance selection?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Client-side Discovery</div><div class="kb-diagram-cell">Server-side Discovery</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Caller -&gt; Registry</div><div class="kb-diagram-cell">Caller -&gt; Proxy / LB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Caller gets instance list</div><div class="kb-diagram-cell">Proxy -&gt; Registry</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Caller selects one target</div><div class="kb-diagram-cell">Proxy selects one target</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Caller -&gt; Target instance</div><div class="kb-diagram-cell">Proxy -&gt; Target instance</div></div>
</div>
</div>



클라이언트 사이드는 소프트웨어 개발 키트 (SDK, Software Development Kit)나 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 품질이 곧 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질로 이어진다. 예를 들어 넷플릭스 유레카 (Eureka)와 리본 (Ribbon) 조합처럼, 클라이언트가 인스턴스 목록을 캐시하고 자체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 선택할 수 있다. 반면 서버 사이드는 [인그레스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) ([Ingress](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)), 리버스 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/), Envoy, 클라우드 로드밸런서가 중앙에서 같은 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용해 애플리케이션 코드를 단순화한다.

핵심은 어느 쪽이든 "발견"만으로 끝나지 않는다는 점이다. 잘못된 헬스 체크, 과도한 캐시, 느슨한 만료 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있으면 죽은 인스턴스를 계속 호출하게 된다. 따라서 디스커버리는 주소 해석과 생존 정보 관리가 결합된 제어 루프로 이해해야 한다.

- **📢 섹션 요약 비유**: 클라이언트 사이드는 운전자가 직접 내비게이션을 보고 길을 고르는 방식이고, 서버 사이드는 기사님이 목적지만 듣고 최적 경로와 차량 배정을 알아서 처리하는 방식이다.

---

## Ⅲ. 비교 및 연결

둘의 차이는 단순히 "옛날 방식 vs 최신 방식"으로 볼 일이 아니다. 핵심 비교 축은 애플리케이션 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/), 운영 표준화, 관측성, [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/), 다중 언어 지원성이다. 호출 패턴과 플랫폼 역량이 다르면 최적 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 달라진다.

| 항목 | 클라이언트 사이드 | 서버 사이드 |
| :--- | :--- | :--- |
| 호출자 복잡도 | 높음 | 낮음 |
| 네트워크 홉 | 적음 | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 1단 추가 가능 |
| 언어별 구현 부담 | 큼 | 작음 |
| 중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 | 어려움 | 쉬움 |
| 대표 환경 | Eureka + [client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) LB | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), Envoy, [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) |
| 장애 지점 | 각 클라이언트 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 편차 | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 병목 및 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) ([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure) 관리 필요 |

클라이언트 사이드는 세밀한 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 제어가 필요한 환경에서 장점이 있다. 예를 들어 호출자별로 다른 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 주거나, 특정 지역 인스턴스를 직접 선호하게 만들 수 있다. 반면 서버 사이드는 다언어 환경과 조직 규모가 커질수록 유리하다. 자바, 고, 파이썬 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 섞여 있어도 중앙 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 일관된 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 제공하면 각 팀이 동일한 네트워크 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)를 다시 만들 필요가 없다.

현대 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에서는 서버 사이드가 더 자주 선택된다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)), [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이름 시스템 ([DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/), [Domain Name System](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)), [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)가 기본 디스커버리와 트래픽 제어를 제공하기 때문이다. 다만 플랫폼이 약하거나 직접 연결의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 중요한 경우에는 클라이언트 사이드가 여전히 현실적인 선택이 된다.

- **📢 섹션 요약 비유**: 직접 운전하면 내 취향대로 골목길을 탈 수 있지만 피곤해지고, 기사에게 맡기면 편하지만 기사 실력이 전체 경험을 좌우하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대표적인 실무 사례는 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/)다. 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 인스턴스가 올라오고 옛 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 인스턴스가 내려가는 동안, 호출자는 준비 완료된 대상만 골라야 한다. 클라이언트 사이드라면 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 갱신 주기, 재시도, 로드밸런싱을 제대로 구현해야 하고, 서버 사이드라면 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층이 readiness와 draining을 정확히 반영해야 한다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 플랫폼이 기본 [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/)와 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층을 이미 제공하는가?
2. 다중 언어 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 각 언어별 클라이언트 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 품질을 동일하게 유지할 수 있는가?
3. 홉 1단 감소가 실제 비즈니스 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 의미 있는 수준인가?
4. 재시도, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/), 회로 차단기 ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/))를 어디에 둘지 책임이 명확한가?
5. [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 장애 시 우회 경로, [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), 관측성이 준비되어 있는가?

### 채택 / 회피 기준

- **클라이언트 사이드 채택**: 직접 로드밸런싱 제어가 필요하고, 언어 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 제한적이며, 추가 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 홉을 줄이고 싶은 환경
- **서버 사이드 채택**: 다중 언어 팀, 중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 통제, 플랫폼 내장 기능 활용, 운영 표준화가 중요한 환경
- **회피**: [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)만 두고 헬스 체크·재시도·만료 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 빈약하게 두는 반쪽짜리 설계

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 클라이언트마다 다른 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)·재시도 값을 써 장애 전파 양상이 제각각인 경우
- 서버 사이드 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 두고도 readiness, draining, [canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 운영하지 않는 경우
- 디스커버리를 도입했는데도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 주소를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 하드코딩하는 경우

- **📢 섹션 요약 비유**: 좋은 디스커버리 설계는 누가 길을 찾든 길 정보와 교통 통제가 항상 최신이어야 한다는 원칙을 지키는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

올바른 패턴을 선택하면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추고, [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/)·오토스케일링·장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 더 자연스럽게 운영할 수 있다. 클라이언트 사이드는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 세밀 제어에서, 서버 사이드는 표준화와 운영 효율에서 강점을 보인다. 중요한 것은 어떤 이름을 붙이느냐가 아니라, 조직과 플랫폼에 맞게 책임 경계를 분명히 두는 것이다.

물론 어느 쪽도 공짜는 아니다. 클라이언트 사이드는 코드와 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 관리 비용이 커지고, 서버 사이드는 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층의 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 관측성을 반드시 보장해야 한다. 따라서 이 주제는 "둘 중 누가 더 우월한가"보다 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 인스턴스 선택 책임을 어디에 둘 것인가</strong>라는 설계 문제로 기억해야 한다.

현대 환경에서는 서버 사이드가 기본값에 가까워졌지만, 특수 저지연 워크로드와 맞춤 로드밸런싱 요구에서는 클라이언트 사이드가 여전히 살아 있다. 결국 좋은 아키텍처는 패턴 이름보다도, 장애 전파와 운영 복잡도를 누가 감당하는지까지 명확하게 설계한 아키텍처다.

- **📢 섹션 요약 비유**: 누가 운전대를 잡든 목적지는 같지만, 차를 몰 사람의 실력과 도로 관리 체계까지 같이 정해야 안전한 여행이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) ([Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)) | 살아 있는 인스턴스 목록을 관리하는 공통 기반 |
| 로드밸런싱 ([Load Balancing](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/)) | 여러 인스턴스 중 실제 호출 대상을 고르는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 ([API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/)) | 서버 사이드 디스커버리의 대표 실행 위치 |
| [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) ([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) | 서버 사이드 디스커버리와 트래픽 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 강화 |
| 헬스 체크 (Health Check) | 죽은 인스턴스를 제거해 디스커버리 정확도를 유지 |
| 회로 차단기 ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)) | 잘못 선택된 대상이 장애를 전파하지 않도록 보완 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">정적 IP / 설정 파일 의존</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">서비스 레지스트리 도입</div>
<div class="kb-diagram-tree-item" style="--depth:2">클라이언트 사이드 디스커버리</div>
<div class="kb-diagram-note">─ App 내부 로드밸런싱</div>
<div class="kb-diagram-tree-item" style="--depth:2">서버 사이드 디스커버리</div>
<div class="kb-diagram-tree-item" style="--depth:5">Proxy / Gateway / Mesh</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Kubernetes Service · Service Mesh · Policy-driven traffic</div>
</div>
</div>



이 흐름은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템이 고정 주소 기반 통신에서, 상태 기반 [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/)과 플랫폼 자동화 중심으로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구 가게가 자주 이사하면, 내가 직접 주소록을 찾을 수도 있고 콜센터 아저씨에게 물어볼 수도 있어요.
2. 내가 직접 찾으면 빠를 수 있지만 매번 알아봐야 하고, 콜센터가 찾으면 나는 편하지만 콜센터가 똑똑해야 해요.
3. 그래서 중요한 건 누가 찾든 지금 열려 있는 가게를 정확히 알려주는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 169 / 482

← **이전**: [168. 서비스 디스커버리 (Service Discovery) 동적 컨테이너 위치 레지스트리](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/168_service_discovery/)
**다음**: [170. 서킷 브레이커 (Circuit Breaker) 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/170_circuit_breaker_pattern/) →

---
