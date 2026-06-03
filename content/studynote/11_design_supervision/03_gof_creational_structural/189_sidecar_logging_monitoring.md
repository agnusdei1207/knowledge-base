+++
title = "189. 사이드카·로깅·모니터링 패턴 (Sidecar, Logging & Monitoring Pattern)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/) ([Sidecar Pattern](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/))은 주 애플리케이션 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 동일한 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))에 보조 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))를 배포하여, 로깅·모니터링·보안·네트워크 관리 등의 횡단 관심사(Cross-Cutting Concern)를 애플리케이션 코드에서 분리하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 패턴이다.
> 2. **가치**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 애플리케이션 코드를 변경하지 않고도 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/), [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집, [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 디스커버리를 추가할 수 있어, 다언어(Polyglot) [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서 운영 기능을 표준화한다.
> 3. **판단 포인트**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 애플리케이션과 생명주기를 공유하므로, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 장애가 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 전체에 영향을 주지 않도록 리소스 제한과 헬스체크를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 수가 너무 많으면 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)당 자원 소비가 급증하므로 필요한 기능만 선택적으로 적용한다.

---

## Ⅰ. 개요 및 필요성

모터사이클의 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)(보조 탑승공간)처럼, 주 애플리케이션 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에 보조 기능을 담당하는 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 붙이는 패턴이다. [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 여러 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 포함할 수 있고, 같은 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)들은 네트워크와 볼륨을 공유한다.

대표적인 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 활용: ① [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)(Fluentd, Filebeat): 앱 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)·Loki로 전송, ② [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) Exporter): 앱 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 포맷으로 노출, ③ [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)(Jaeger Agent): 추적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Jaeger 서버로 전송, ④ 앰배서더 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)(Envoy): [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신 관리.

```text
┌─────────────────────────────────────────────────────────────┐
│         사이드카 패턴 - Kubernetes 파드 구조                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Kubernetes Pod                                      │   │
│  │  ┌─────────────────┐  ┌────────────────────────────┐ │   │
│  │  │  Main App       │  │  Sidecar: Fluentd           │ │   │
│  │  │  Container      │  │  (로그 수집·전송)           │ │   │
│  │  │  /var/log/*.log ├─→│  → Elasticsearch           │ │   │
│  │  │  (공유 볼륨)    │  │  (공유 볼륨으로 로그 읽기) │ │   │
│  │  └─────────────────┘  └────────────────────────────┘ │   │
│  │  공유: 네트워크(localhost), 볼륨(/var/log)           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 모터사이클(주 앱)에 붙은 보조 탑승공간처럼, 주 앱을 수정하지 않고 보조 기능(로깅·모니터링)을 추가한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 아키텍처에서 중요한 원칙: ① 앱은 stdout/stderr나 공유 볼륨에만 기록, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)가 수집·전송 담당, ② [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 앱보다 먼저 종료되지 않도록 terminationGracePeriodSeconds [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), ③ [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 자원(CPU/메모리) 제한(Limits)을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여 앱 자원을 침범하지 않게 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/).

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) | 앱 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 중앙 저장소로 전송 | Fluentd, Filebeat |
| [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집 | 앱 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 포맷으로 노출 | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) Exporter |
| [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) | 추적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집·전송 | Jaeger Agent, Zipkin |
| 앰배서더 | 아웃바운드 통신 관리 | Envoy [Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) |

```text
┌─────────────────────────────────────────────────────────────┐
│       중앙화 로깅·모니터링 스택 (ELK + Prometheus)          │
├─────────────────────────────────────────────────────────────┤
│  [App] → stdout → [Fluentd 사이드카] → [Elasticsearch]     │
│                                           → [Kibana]        │
│                                                             │
│  [App] → /metrics → [Prometheus Exporter 사이드카]          │
│                           → [Prometheus] → [Grafana]        │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 건물(앱)에 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))와 화재 감지기(모니터링 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))를 설치하면, 건물 자체를 수정하지 않고도 모든 활동을 기록하고 이상을 감지한다.

---
## Ⅲ. 비교 및 연결

[사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/)과 DaemonSet의 차이를 명확히 해야 한다. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 수준(개별 앱별 보조 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)), DaemonSet은 노드 수준(모든 노드에 동일 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))으로 구분된다.

| 비교 축 | A | B |
|:---|:---|:---|
| 배포 단위 | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)별 개별 배포 | 모든 노드에 하나씩 |
| 자원 격리 | [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)별 분리 | 노드 전체 공유 |
| 앱별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 가능 ([파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)별 다름) | 어려움 (노드 단위) |
| 사용 사례 | 앱별 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) | 시스템 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 네트워크 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 각 자동차([파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))에 블랙박스([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))를 설치하는 것이고, DaemonSet은 도로(노드)마다 교통 카메라([DaemonSet](/knowledge-base/studynote/11_design_supervision/06_exam_summary/334_process/))를 설치하는 것이다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)는 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 주입([Sidecar](/knowledge-base/studynote/04_software_engineering/11_testing_validation/546_sidecar_proxy_pattern/) [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/))으로 Envoy 프록시를 자동으로 모든 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 배포한다. `kubectl label namespace default istio-injection=enabled`로 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 레벨에서 자동 주입을 활성화하면, 개발자가 직접 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하지 않아도 된다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)의 자원 제한(CPU/Memory Limits)이 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어 주 앱 자원을 침범하지 않는가?
2. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)가 주 앱보다 먼저 종료되지 않도록 종료 순서(terminationGracePeriodSeconds)가 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어 있는가?
3. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 수가 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)당 자원 오버헤드를 적정 수준으로 유지하는가?
4. [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)) 자동 주입이 가능한 환경인지 검토했는가?
5. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·추적 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)가 중앙 저장소([Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger)에 올바르게 연결되는가?

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 운전기사(앱)가 운전에만 집중할 수 있도록 내비게이션(로깅)·블랙박스(추적)·연료 계기판(모니터링)을 자동으로 관리하는 차량 보조 시스템이다.

---

## Ⅴ. 기대효과 및 결론

[사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/)을 적용하면 애플리케이션 코드의 횡단 관심사가 제거되어 코드가 단순해지고, 다언어 환경에서 로깅·모니터링을 표준화할 수 있다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)·[서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)와 자연스럽게 통합되어 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 관찰성([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))을 달성한다.

한계는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)당 추가 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 인한 자원 오버헤드와, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리의 복잡성이다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 많으면 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)의 자동 주입이 효율적이다.

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 헬퍼 드론처럼 주 비행체(앱)를 따라다니며 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집·통신·보안을 담당한다. 주 비행체는 임무(비즈니스 로직)에만 집중한다.

---

### 📌 관련 개념 맵

[횡단 관심사 분리 필요] → [사이드카 패턴] → [앰배서더 패턴] → [서비스 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 자동 주입] → eBPF 기반 무사이드카]

| 개념 | 연결 포인트 |
|:---|:---|
| [앰배서더 패턴](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/188_ambassador_pattern/) | 아웃바운드 통신 전담 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) |
| [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)) | [사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/)의 클러스터 전체 자동화 |
| [DaemonSet](/knowledge-base/studynote/11_design_supervision/06_exam_summary/334_process/) | 노드 수준 보조 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)의 노드 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)) |
| Fluentd / Filebeat | 대표적인 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 도구 |

### 📈 관련 키워드 및 발전 흐름도

[컨테이너 횡단 관심사] → [사이드카 패턴] → [앰배서더 패턴] → Istio 자동 주입] → eBPF [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기반 무사이드카]

### 👶 어린이를 위한 3줄 비유 설명

1. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 주인공(앱) 옆에서 지원 역할을 하는 조연처럼, 로깅·모니터링을 담당해요.
2. 주인공은 자기 역할(비즈니스 로직)에만 집중하고, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)가 나머지를 처리해요.
3. Kubernetes에서 같은 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 안에 여러 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 역할을 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 249 / 530

← **이전**: [189. 사이드카 통합 로깅 및 모니터링 수집망 아키텍처 패턴 (Sidecar Integrated Logging and Monitoring](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/189_sidecar_logging_monitoring/)
**다음**: [190. DI 프레임워크와 스프링 빈 생명주기 (DI Framework & Spring Bean Lifecycle)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/190_di_framework_spring_bean_lifecycle/) →

---
