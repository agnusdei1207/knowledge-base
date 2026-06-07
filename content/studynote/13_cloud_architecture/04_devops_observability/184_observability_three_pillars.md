---
title: "Observability Three Pillars"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 184
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) ([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))는 시스템의 외부 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)만으로 내부 상태를 추론하는 능력이며, 그 최소 공통 언어가 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) ([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) ([Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)), 트레이스 (Traces)의 3대 기둥이다.
> 2. **가치**: [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 이상 징후를 빠르게 감지하고, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 사건의 문맥을 남기며, [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) ([Distributed Tracing](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/))은 지연과 오류가 어느 구간에서 생겼는지 연결해 알려 준다.
> 3. **판단 포인트**: 좋은 관측성은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 많이 쌓는 일이 아니라, 표준 계측, 상관관계 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 카디널리티 관리, 샘플링 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계하는 일이다.

---

## Ⅰ. 개요 및 필요성

[옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)는 "시스템이 무엇을 하고 있는지"를 사후에 추리하는 기술이 아니라, 처음부터 "나중에 질문할 수 있게" 시스템을 설계하는 원칙이다. 단일 애플리케이션 시절에는 중앙 처리 장치 (Central Processing Unit, CPU), 메모리, 오류 개수 정도만 봐도 상태를 짐작할 수 있었지만, [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/), [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))와 멀티클라우드 환경에서는 한 번의 사용자 요청이 게이트웨이, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 비즈니스 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소를 연쇄 통과한다. 이 구조에서는 서버 한 대의 상태가 좋아 보여도 사용자는 느리거나 실패한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 체감할 수 있다.

전통적 모니터링이 "미리 정한 항목이 임계값을 넘었는가"를 보는 방식이라면, [옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)는 "왜 이런 현상이 벌어졌는가"를 뒤늦게라도 묻고 답할 수 있게 만드는 구조다. 그래서 3대 기둥은 단순 수집 항목이 아니라 서로 다른 질문을 맡는다. [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 숫자로 이상을 감지하고, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 사건의 경위를 남기고, 트레이스는 요청 경로를 이어서 인과관계를 복원한다.

문제가 생길 때 운영자가 가장 먼저 마주치는 질문도 이 순서를 따른다. "문제가 있나?"는 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이, "무슨 일이 있었나?"는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가, "어디서 막혔나?"는 트레이스가 가장 잘 답한다. 따라서 세 기둥 중 하나가 빠지면 관측성은 남은 두 기둥의 추측에 의존하게 된다.

- **📢 섹션 요약 비유**: [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 트레이스는 병원에서 체온계, 진료 기록, 컴퓨터 단층 촬영 (Computed Tomography, [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/))처럼 역할이 다르다. 셋 중 하나만 있으면 이상은 보이거나 기록은 남겠지만, 원인을 끝까지 짚어 내기는 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)의 핵심 원리는 "하나의 요청을 세 가지 관점으로 동시에 남긴다"는 데 있다. [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 집계된 시계열 숫자라서 경보와 추세 분석에 유리하고, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 텍스트 또는 구조화된 이벤트라서 예외와 비즈니스 문맥을 담기 쉽고, 트레이스는 요청 단위의 스팬 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)라서 병목 위치를 복원하기 좋다. 실무에서는 이 세 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 같은 `trace_id` 또는 `request_id`로 연결되어야 비로소 탐색 비용이 줄어든다.

이 그림은 하나의 요청이 3대 기둥으로 어떻게 투영되는지 보여 준다.

```text
+--------------------------------------------------------------------+
| One request, three observability pillars                          |
+--------------------------------------------------------------------+
| 사용자 요청                                                        |
|    |                                                               |
|    v                                                               |
| Gateway -> Auth -> Order -> Payment -> Database                    |
|    |          |       |         |                                  |
|    +- Metrics : 요청 수, 오류율, 95백분위수 지연시간               |
|    +- Logs    : 예외 메시지, 설정 변경, 비즈니스 이벤트            |
|    +- Traces  : span 연결, 서비스 간 호출 순서, 병목 구간          |
|                                                                    |
| Collector -> Metrics Store / Log Store / Trace Backend             |
|                    +- 공통 상관키(trace_id, service.name)          |
+--------------------------------------------------------------------+
```

이 구조에서 중요한 것은 세 기둥이 서로를 대체하지 않는다는 점이다. [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 집계값이라 값이 높아졌다는 사실은 알려 주지만 왜 높아졌는지는 말하지 못한다. [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 상세하지만 건수가 많아지면 검색 비용이 급증한다. 트레이스는 경로를 보여 주지만, 장기 추세나 정확한 오류 문장은 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이 보완해야 한다.

| 기둥 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형태 | 가장 잘 답하는 질문 | 강점 | 설계 시 주의점 |
| :--- | :--- | :--- | :--- | :--- |
| [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 시계열 숫자 | 얼마나 느린가, 얼마나 자주 실패하는가 | 경보, 용량 계획, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 지표 계산에 적합 | 사용자 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 같은 고카디널리티 라벨은 비용 급증 |
| [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 이벤트 기록 | 무슨 예외가 났는가, 어떤 입력에서 깨졌는가 | 상세 원인, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적, 변경 이력 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 구조화되지 않으면 검색과 상관분석이 어려움 |
| 트레이스 | 요청 경로 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) | 어느 홉에서 대기했는가, 어떤 호출이 연쇄 실패했는가 | 병목 위치, 인과관계, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계 추적 | [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 전파가 끊기면 전체 경로가 끊어짐 |

세 기둥을 실제 아키텍처로 묶을 때는 계측 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), 수집기, 저장소, 조회 계층이 필요하다. 최근에는 OpenTelemetry가 공통 계측 표준 역할을 하며, [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스를 같은 리소스 속성과 상관키로 묶는 데 널리 쓰인다. 이때 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 적은 비용으로 넓게, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 중요한 문맥 중심으로, 트레이스는 샘플링을 고려해 깊게 수집하는 식의 균형이 실무 핵심이다.

- **📢 섹션 요약 비유**: 같은 경기라도 전광판 점수판은 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 심판 기록지는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 중계 카메라 이동 경로는 트레이스에 가깝다. 점수판만 보면 누가 왜 실수했는지 모르고, 카메라만 보면 경기 전체 추세를 읽기 어렵다.

---

## Ⅲ. 비교 및 연결

3대 기둥의 차이는 "무엇을 먼저 보느냐"보다 "각 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 어디까지 믿을 수 있느냐"에서 드러난다. 장애 감지 자체는 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이 가장 빠르지만, 원인 파악은 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 트레이스가 맡아야 한다. 반대로 트레이스만 잘 되어 있어도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 지표 ([Service Level Indicator](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/), [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/))나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표 ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/), [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/))를 직접 운영하기는 어렵다. 결국 좋은 운영 흐름은 `메트릭으로 감지 -> 트레이스로 위치 파악 -> 로그로 원인 확인`의 삼각 루프다.

| 비교 축 | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 우위 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 우위 | 트레이스 우위 |
| :--- | :--- | :--- | :--- |
| 실시간 경보 | 매우 강함 | 약함 | 중간 |
| 장기 추세 분석 | 강함 | 약함 | 중간 |
| 개별 오류 원인 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 약함 | 매우 강함 | 강함 |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 인과관계 | 약함 | 중간 | 매우 강함 |
| 저장 비용 효율 | 높음 | 낮음 | 중간 |

[옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)는 전통적 모니터링과도 연결되지만 같은 개념은 아니다. 모니터링은 보통 "알고 있는 실패 패턴"을 감시하는 데 강하다. 반면 관측성은 알람이 울린 뒤 아직 정의되지 않은 질문을 던질 수 있어야 한다. 그래서 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 대시보드만 있는 시스템은 모니터링은 가능해도 [옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)는 약할 수 있다.

또한 3대 기둥은 그 자체로 끝나지 않는다. 이벤트, 지속적 [프로파일링](/studynote/02_operating_system/10_security/613_profiling_gprof/) (Continuous [Profiling](/studynote/02_operating_system/10_security/613_profiling_gprof/)), 배포 정보, 실험 이력까지 묶이면 관측성의 해상도가 더 높아진다. 그러나 그 확장 개념들도 결국 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스 위에서 연결되므로, 3대 기둥은 여전히 기본 골격으로 기억하는 편이 맞다.

- **📢 섹션 요약 비유**: [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 트레이스의 관계는 날씨 앱의 온도 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/), 기상 관측 일지, 태풍 이동 경로 지도와 비슷하다. 셋을 함께 봐야 오늘 왜 비가 오고 내일 어디로 이동하는지 제대로 이해할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 흔한 실패는 "세 기둥을 다 수집하면 관측성이 완성된다"고 생각하는 것이다. 실제로는 무엇을 계측하고 어떤 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)로 연결할지 결정하지 않으면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 많아지고 답은 오히려 늦어진다. 특히 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)에는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)명, 엔드포인트, 상태 코드처럼 집계 가능한 라벨만 두고, 사용자 번호·주문 번호 같은 고카디널리티 값은 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)나 트레이스로 보내는 것이 일반적이다.

| 장애 증상 | 1차로 볼 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | 이유 | 바로 이어서 볼 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| :--- | :--- | :--- | :--- |
| 전체 오류율 상승 | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체 이상 여부를 가장 빨리 감지 | 트레이스로 실패 구간 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 예외 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 특정 요청만 느림 | 트레이스 | 경로별 대기 시간을 바로 볼 수 있음 | 해당 스팬의 구조화 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 배포 직후 이상 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경, 기능 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), 예외가 한꺼번에 드러남 | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)으로 영향 범위, 트레이스로 병목 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 장기적 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 추세와 용량 한계를 보기 쉬움 | 트레이스로 핫패스 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

기술사 관점에서 강조할 판단 포인트도 명확하다.

1. **계측 우선 설계**: 코드 배포 전에 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 이름, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 필드, 트레이스 전파 규칙을 먼저 정해야 한다.
2. <strong>상관관계 <a href="/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">식별자</a></strong>: `trace_id`, `span_id`, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)명, 배포 버전이 공통으로 남아야 장애 추적 속도가 급격히 빨라진다.
3. **카디널리티 관리**: [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 저장소는 집계 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 강하므로 무분별한 라벨 확장은 피해야 한다.
4. <strong>샘플링 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>: 정상 트래픽은 샘플링하고, 오류·고지연 요청은 우선 보존하는 방식이 비용 대비 효율적이다.
5. <strong>구조화 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>와 보안</strong>: [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 사람이 읽기 쉬운 문장만이 아니라 기계가 필터링할 수 있는 필드 구조를 가져야 하며, 개인정보는 마스킹해야 한다.

대표 안티패턴은 세 가지다. 첫째, 대시보드만 화려하고 코드 계측이 부실한 경우다. 둘째, 모든 값을 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 라벨로 밀어 넣어 저장 비용과 조회 지연을 폭증시키는 경우다. 셋째, 트레이스는 수집하지만 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐나 비동기 작업으로 넘어가면서 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 전파가 끊기는 경우다. 이런 시스템은 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 많은데 답은 없는" 상태에 빠진다.

- **📢 섹션 요약 비유**: 관측성 설계는 창고에 카메라를 많이 다는 일이 아니라, 박스에 같은 송장 번호를 붙이고 선반 체계를 맞추는 일과 같다. 번호 체계가 없으면 카메라가 많아도 물건을 못 찾는다.

---

## Ⅴ. 기대효과 및 결론

3대 기둥이 잘 설계되면 평균 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 (Mean Time To [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/))이 줄고, 배포 뒤 영향 범위를 더 빨리 알 수 있으며, 팀 간 책임 공방도 줄어든다. [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 경보를 빨리 울리고, 트레이스는 병목 구간을 좁히고, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 마지막 증거를 남기기 때문이다. 이 조합은 특히 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), 이벤트 기반 아키텍처처럼 경계가 많은 시스템에서 효과가 크다.

다만 비용과 운영 복잡도는 분명한 대가다. [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 저장 비용이 크고, 트레이스는 샘플링과 보존 기간 설계가 필요하며, [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 라벨 설계가 나쁘면 오히려 장애를 읽기 어렵게 만든다. 따라서 관측성의 성패는 "얼마나 많이 수집했는가"가 아니라 "어떤 질문에 답하게 설계했는가"로 판단해야 한다.

결국 [옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 3대 기둥은 세 가지 도구 이름이 아니라, 시스템을 바라보는 세 가지 렌즈다. 좋은 시스템은 이 세 렌즈가 같은 사건을 서로 다른 해상도로 보여 주도록 설계되어 있으며, 운영자는 그 겹침 덕분에 처음 보는 장애도 추론할 수 있다.

- **📢 섹션 요약 비유**: 3대 기둥은 같은 도시를 보는 지도, 거리 표지판, 폐쇄 회로 텔레비전 (Closed-Circuit Television, [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/)) 같은 것이다. 셋을 함께 봐야 길이 막힌 이유와 정확한 위치를 동시에 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) ([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)) | 경보, 추세 분석, [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 계산의 기초가 되는 집계 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) ([Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)) | 예외 문맥, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적, 배포 이력을 남기는 상세 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) ([Distributed Tracing](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 경로와 병목을 복원하는 요청 단위 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스를 공통 리소스 정보로 계측하는 표준 |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표 ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/), [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)) | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 연결하는 품질 목표 |
| 지속적 [프로파일링](/studynote/02_operating_system/10_security/613_profiling_gprof/) (Continuous [Profiling](/studynote/02_operating_system/10_security/613_profiling_gprof/)) | 3대 기둥을 보완해 코드 수준 병목을 찾는 확장 관측성 |

### 📈 관련 키워드 및 발전 흐름도

```text
인프라 모니터링
    |
    v
애플리케이션 메트릭 수집
    |
    v
중앙 로그 관리
    |
    v
분산 추적 도입
    |
    v
OpenTelemetry 기반 상관분석
    |
    v
프로파일링 · 이벤트 · 자동화 분석을 포함한 확장 관측성
```

### 👶 어린이를 위한 3줄 비유 설명

1. [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 "지금 열이 몇 도인지" 보는 체온계예요.
2. [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 "언제 어디가 아팠는지" 적어 놓은 진료 기록이에요.
3. 트레이스는 몸속에서 어디가 막혔는지 따라가는 지도라서, 셋을 같이 봐야 정확히 고칠 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 183 / 371

<- **이전**: [183. 에러 예산 (Error Budget) - 혁신 속도와 신뢰성의 운영 균형](/studynote/13_cloud_architecture/04_devops_observability/183_error_budget_sre_innovation_balance/)
**다음**: [185. 메트릭 (Metrics - Prometheus, Grafana)](/studynote/13_cloud_architecture/04_devops_observability/185_metrics_prometheus_grafana/) ->

---
