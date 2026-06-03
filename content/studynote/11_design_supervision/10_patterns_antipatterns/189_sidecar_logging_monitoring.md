+++
title = "189. 사이드카 통합 로깅 및 모니터링 수집망 아키텍처 패턴 (Sidecar Integrated Logging and Monitoring Architecture Pattern)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
1. **본질**: [사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/)은 주 애플리케이션 옆에 보조 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 붙여 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 트레이스를 수집하게 함으로써 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드를 오염시키지 않고 관측성을 표준화하는 구조다.
2. **가치**: 언어·프레임워크별 SDK 편차를 줄이고, 운영 기능을 독립 배포·독립 업그레이드할 수 있어 MSA와 [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경에서 특히 효과적이다.
3. **판단 포인트**: 같은 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 내 수명주기 공유, 로컬 통신, 공유 볼륨이라는 장점이 있는 대신 자원 오버헤드·보안 경계·운영 복잡도까지 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성
[마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서는 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 직접 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 전송기, [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집기, 트레이스 에이전트를 내장하기 시작하면 언어별 구현 차이와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 부담이 빠르게 커진다. 결국 개발팀은 비즈니스 로직보다 운영 SDK 정합성에 더 많은 시간을 쓰게 되고, 장애 시에도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 문제인지 관측 도구 문제인지 분리하기 어려워진다.

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 통합 로깅 및 모니터링 수집망 아키텍처 패턴은 이 문제를 **애플리케이션 코드가 아니라 배포 구조 수준에서 해결**한다. 주 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 요청 처리와 비즈니스 규칙에 집중하고, 옆의 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수집, [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 노출, 트레이스 전달, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 같은 횡단 관심사를 담당한다.

```text
┌─────────────────────── 서비스 내부 직접 내장 방식의 문제 ───────────────────────┐
│ App A + Logging SDK + Metrics SDK + Trace SDK                                │
│ App B + Logging SDK + Metrics SDK + Trace SDK                                │
│ App C + Logging SDK + Metrics SDK + Trace SDK                                │
│                └─ 언어별 편차, 버전 충돌, 재배포 부담 증가                    │
└───────────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────── 사이드카 분리 방식 ───────────────────────────────────┐
│ App Container │ Sidecar Collector │ 공통 설정 │ 독립 업그레이드              │
└───────────────────────────────────────────────────────────────────────────────┘
```

감리·설계 관점에서 핵심은 “수집을 한다”가 아니라 “운영 기능을 어디에 배치할 것인가”다. 코드에 넣을지, 노드 단위로 둘지, [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 단위로 붙일지에 따라 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)와 장애 범위가 달라진다.
- **📢 섹션 요약 비유**: 선수(주 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))가 경기에만 집중하도록 옆에서 기록원과 심박 측정기가 붙어 다니는 구조가 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)다.

---

## Ⅱ. 아키텍처 및 핵심 원리
[사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/)의 핵심 원리는 **동일 배포 단위, 분리된 책임, 짧은 관측 경로**다. 주 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 같은 Pod에 있으므로 로컬호스트 통신이나 공유 볼륨을 사용할 수 있고, 동시에 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 분리되어 있어 운영 기능만 독립적으로 교체하거나 제한할 수 있다.

```text
┌──────────────────────────── Kubernetes Pod ────────────────────────────┐
│                                                                        │
│  ┌────────────────────┐        shared volume / localhost              │
│  │ Main Container     │──────────────────────────────────────┐         │
│  │ business logic     │                                      │         │
│  └────────────────────┘                                      │         │
│                                                              ▼         │
│  ┌────────────────────┐   collect / enrich / forward   ┌───────────┐  │
│  │ Sidecar Collector  │────────────────────────────────▶│ Backend   │  │
│  │ log·metric·trace   │                                 │ OTEL/ELK  │  │
│  └────────────────────┘                                 └───────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 핵심 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 주 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) | 비즈니스 로직 처리 | 관측 코드 최소화, 표준 출력 또는 공용 엔드포인트 제공 |
| [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 수집기 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·트레이스 수집 및 전달 | Fluent [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/), [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector, Envoy 등 역할 분리 |
| 백엔드 관측 플랫폼 | 저장·검색·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)·알림 | [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Tempo/Jaeger, Grafana와 연계 |

실무에서는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 테일링형 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/), localhost 스크레이핑형 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집, [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 기반 트레이스 주입 방식이 자주 쓰인다. 특히 [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector를 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)로 두면 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·트레이스를 단일 파이프라인으로 통합하기 좋다.
- **📢 섹션 요약 비유**: 가게 주인은 손님 응대만 하고, 옆 계산대 보조가 매출 기록·재고 집계·방문 흐름 체크를 동시에 맡는 모습과 같다.

---

## Ⅲ. 비교 및 연결
[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 “가까이 붙어 있는 공통 기능 분리”에 강하고, 다른 방식은 다른 범위에 강하다. 따라서 수집 범위와 운영 단위를 함께 비교해야 한다.

| 비교 항목 | 애플리케이션 내장형 에이전트 | 노드 에이전트([DaemonSet](/knowledge-base/studynote/11_design_supervision/06_exam_summary/334_process/)) | [사이드카 패턴](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/182_sidecar_pattern_proxy_container/) |
| :--- | :--- | :--- | :--- |
| [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드와 높음 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 낮음 | 코드와 낮고 Pod와 높음 |
| 세밀한 제어 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 가능 | 노드 단위 위주 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 세밀 제어 가능 |
| 배포 영향 | 도구 변경 시 앱 재배포 필요 | 노드 운영팀 중심 변경 | 수집기만 개별 재배포 가능 |
| 자원 효율 | 상대적으로 유리 | 가장 효율적 | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 수만큼 오버헤드 발생 |
| 적합 환경 | 소수 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 단순 앱 | 호스트 공통 수집 | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 분리 |

또한 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)의 Envoy [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/), 보안 인증서 갱신기, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 시행기 역시 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)의 확장된 활용이다. 즉 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 단순 로깅 도구가 아니라 **횡단 관심사를 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 경계에서 캡슐화하는 일반 패턴**으로 이해해야 한다.
- **📢 섹션 요약 비유**: 건물 전체 경비실(노드 에이전트)과 각 가게 점원(내장형) 사이에서, 매장마다 붙는 전담 매니저가 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 모든 워크로드에 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)를 무조건 붙이지 않는다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 많고 언어가 제각각이며 운영 표준화를 강하게 요구할수록 적합하고, 반대로 단일 프로세스 앱이나 극단적 고밀도 환경에서는 자원 오버헤드가 부담이 될 수 있다. 또한 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 권한, [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 우회 경로, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 장애 시 주 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 영향 범위, 재시작 순서까지 함께 설계해야 한다.

[서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)와 함께 쓸 때는 네트워크 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)와 관측성 수집 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)가 역할 중복 없이 구성되는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다. 감리 답안에서는 “언어 독립성 확보”와 “운영 표준화”를 장점으로 쓰되, “[Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 당 자원 증가”와 “운영 복잡도 상승”을 반대 논점으로 함께 제시하면 균형이 좋다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별로 다른 언어·런타임을 쓰고 있어 수집 방식 표준화가 필요한가?
- [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·트레이스 수집기를 애플리케이션과 분리 배포해야 하는가?
- [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 단위 자원 증가를 감수해도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 제어 이점이 더 큰가?
- [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 장애, 보안 권한, 재시작 순서에 대한 운영 기준이 준비되어 있는가?

특히 운영팀이 “[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)를 붙였으니 관측성이 끝났다”라고 생각하는 것이 대표적 오판이다. 실제로는 백엔드 저장소, 라벨 표준, 경보 규칙, 샘플링 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 연결되어야 완성된다.
- **📢 섹션 요약 비유**: 블랙박스를 차에 달아도 전원, 저장장치, 영상 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 체계가 없으면 사고 기록 장치로서 완성되지 않는 것과 같다.

---

## Ⅴ. 기대효과 및 결론
[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 통합 로깅 및 모니터링 수집망 아키텍처 패턴을 잘 적용하면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드는 단순해지고, 운영 기능은 표준화되며, 수집기 교체나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 강화도 빠르게 수행할 수 있다. 또한 장애 분석 시 애플리케이션과 관측 파이프라인 책임이 분리되어 원인 추적이 쉬워지고, 멀티언어 환경에서도 동일한 운영 기준을 유지할 수 있다.

결론적으로 이 패턴은 “관측 기능을 붙인다”보다 “운영 책임을 배포 구조로 캡슐화한다”는 관점으로 이해해야 한다. 기술사 답안에서는 **[Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 경계, 관측성 3대 축, 표준화, 오버헤드**를 함께 언급하면 실무성과 논리성이 모두 살아난다.
- **📢 섹션 요약 비유**: 가수는 노래만 하고, 옆의 음향팀이 녹음·모니터링·송출을 맡을 때 공연 전체 품질이 안정되는 것과 같다.

---

### 📌 관련 개념 맵
- **관측성([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 트레이스를 통해 시스템 내부 상태를 추론하는 운영 체계
- **[OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector**: 텔레메트리 수집·변환·전송을 통합하는 대표 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 구현체
- **[서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/))**: Envoy 같은 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 활용해 통신 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 인프라 계층으로 분리하는 구조
- **[DaemonSet](/knowledge-base/studynote/11_design_supervision/06_exam_summary/334_process/)**: 노드 단위 공통 에이전트 배포 방식으로, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)와 비교 대상이 되는 운영 패턴
- **[앰배서더 패턴](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/188_ambassador_pattern/)([Ambassador Pattern](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/188_ambassador_pattern/))**: 외부 통신을 보조 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)로 위임하는 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 계열 패턴

### 📈 관련 키워드 및 발전 흐름도
```text
서비스별 SDK 개별 내장
        │
        ▼
Pod 단위 로그·메트릭 수집 분리
        │
        ▼
OpenTelemetry 기반 통합 수집
        │
        ▼
서비스 메시·정책 제어·보안 텔레메트리 연계
```

### 👶 어린이를 위한 3줄 비유 설명
1. 축구 선수가 뛰는 동안 옆에서 기록 선생님이 몇 번 뛰었는지, 어디로 움직였는지 적어 주는 거예요.
2. 선수는 공 차는 일만 하면 되고, 기록은 옆 친구가 대신 맡아요.
3. 그래서 선수가 바뀌어도 기록 방법은 똑같이 맞출 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 248 / 530

← **이전**: [188. 앰배서더 패턴 (Ambassador Pattern)](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/188_ambassador_pattern/)
**다음**: [189. 사이드카·로깅·모니터링 패턴 (Sidecar, Logging & Monitoring Pattern)](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/189_sidecar_logging_monitoring/) →

---
