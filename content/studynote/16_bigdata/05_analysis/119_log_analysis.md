+++
title = "116. 로그 분석 (Log Analysis) — 이상 감지/보안 이벤트/패턴 발견"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석 (Log Analysis)은 시스템·애플리케이션·네트워크에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 대규모 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 수집·파싱·집계하여 이상 감지, 보안 위협, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목, 사용자 행동 패턴을 발굴하는 운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 기법이다.
> 2. **가치**: ELK ([Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)-Logstash-[Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/)) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 Fluentd를 통해 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 수천 개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 실시간으로 통합하고, [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) ([Security Information and Event Management](/knowledge-base/studynote/09_security/13_secops_ir_forensics/625_siem_architecture/))과 연계하여 보안 사고를 즉각 탐지한다.
> 3. **판단 포인트**: 비정형 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 Grok 패턴으로 파싱 후 구조화하고, [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계와 ILM ([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [Lifecycle Management](/knowledge-base/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle/)) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 수백 TB [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 비용을 결정하는 핵심 변수다.

---

## Ⅰ. 개요 및 필요성

[마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)에서 수백 개의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 초당 수백만 라인의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다. 특정 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 오류가 발생했을 때 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 수십 개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 수동으로 grep하는 것은 불가능하다. 통합 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석 플랫폼은 이 문제를 해결하는 현대 운영의 필수 인프라다.

보안 관점에서도 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석은 핵심이다. 2020년 SolarWinds 해킹처럼 고도화된 [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/) ([Advanced Persistent Threat](/knowledge-base/studynote/09_security/04_endpoint_security/374_apt/)) 공격은 몇 달에 걸쳐 조금씩 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 남긴다. 이를 탐지하려면 장기 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 통합 분석하고 이상 패턴을 자동 감지하는 SIEM이 필요하다.

- **📢 섹션 요약 비유**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석은 수십만 명의 일기를 읽고 누가 이상한 행동을 했는지 찾아내는 탐정이다. 한 줄 한 줄은 평범해 보여도 전체 패턴이 범죄를 드러낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+--------------------------------------------------------------------+
|               로그 분석 파이프라인 (ELK + Kafka)                    |
+--------------------------------------------------------------------+
|  [수집 (Collection)]                                               |
|   앱 서버 / 컨테이너 / 네트워크 장비 / OS                           |
|       |                                                            |
|       v                                                            |
|  [에이전트 (Agent)]                                                |
|   Fluentd / Filebeat / Logstash                                    |
|       |                                                            |
|       v                                                            |
|  [메시지 큐 (Message Queue)]                                       |
|   Apache Kafka (고가용성, 버퍼링)                                  |
|       |                                                            |
|       v                                                            |
|  [처리 (Processing)]                                               |
|   Logstash (파싱·필터링·변환) / Spark Streaming (복잡 분석)        |
|       |                                                            |
|       v                                                            |
|  [저장 (Storage)]                                                  |
|   Elasticsearch (검색 인덱스) / S3 (장기 아카이브)                 |
|       |                                                            |
|       v                                                            |
|  [시각화 & 알림]                                                   |
|   Kibana / Grafana / PagerDuty 알림 연동                           |
+--------------------------------------------------------------------+
```

### [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 파싱: Grok 패턴

```text
Grok 패턴 예시 (Apache Access Log):
%{IPORHOST:clientip} %{WORD:ident} %{WORD:auth} \[%{HTTPDATE:timestamp}\]
-> "192.168.1.1 - - [21/Apr/2026:10:30:00] 200 1234"
-> {clientip: "192.168.1.1", timestamp: "21/Apr/2026:10:30:00", status: 200}
```

### [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 레벨 및 이상 패턴

| 레벨 | 의미 | 분석 중점 |
|:---|:---|:---|
| **DEBUG** | 개발 디버깅용 상세 정보 | 개발 환경만 활성화 |
| **INFO** | 정상 운영 이벤트 | 사용자 행동 분석 |
| **WARN** | 잠재적 문제, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계속 | 증가 추세 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 |
| **ERROR** | 기능 실패 | 즉각 알림 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
| **FATAL** | 심각한 시스템 오류 | 온콜 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) |

- **📢 섹션 요약 비유**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 시스템이 쓰는 일기다. INFO는 오늘도 평범한 하루, WARN은 오늘 좀 이상했는데, ERROR는 오늘 큰일 났어, FATAL은 오늘 거의 죽을 뻔했어에 해당한다.

---

## Ⅲ. 비교 및 연결

| 항목 | ELK [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) | Datadog | [Splunk](/knowledge-base/studynote/09_security/13_secops_ir_forensics/630_splunk/) |
|:---|:---|:---|:---|
| **라이선스** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) (일부 유료) | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/) 완전관리형 | 엔터프라이즈 상용 |
| **셋업 비용** | 높음 (직접 구성) | 낮음 (클라우드) | 높음 |
| **확장성** | 매우 높음 | 높음 | 높음 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 언어</strong> | [Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/) Query Language (KQL) | Datadog Query | [Splunk](/knowledge-base/studynote/09_security/13_secops_ir_forensics/630_splunk/) [SPL](/knowledge-base/studynote/04_software_engineering/03_design_architecture/187_spl_software_product_line_variability/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>/ML</strong> | 별도 연동 필요 | 내장 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | 내장 ML |

[SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) ([Security Information and Event Management](/knowledge-base/studynote/09_security/13_secops_ir_forensics/625_siem_architecture/))은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석 + 상관 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 분석 + 위협 인텔리전스를 결합한 보안 특화 플랫폼이다. IBM [QRadar](/knowledge-base/studynote/09_security/13_secops_ir_forensics/632_qradar/), [Splunk](/knowledge-base/studynote/09_security/13_secops_ir_forensics/630_splunk/) ES, Microsoft Sentinel이 대표적이다.

- **📢 섹션 요약 비유**: ELK는 강력하지만 직접 조립해야 하는 조립 PC이고, Datadog/Splunk는 비싸지만 바로 쓰는 맥북이다. 규모와 예산에 따라 선택이 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적용 시나리오

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> 장애 추적</strong>: [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) ([OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))과 통합 -> [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 체인 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)
2. <strong>보안 <a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a></strong>: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인 실패 급증 -> [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) [상관 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/325_correlation_analysis_pearson_spearman/) -> 계정 탈취 시도 자동 차단
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 병목 분석</strong>: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 분포 분석 -> 95th/99th 퍼센타일 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 위반 탐지
4. <strong>컴플라이언스 <a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong>: 접근 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 90일 보관 + 비정상 접근 패턴 리포트 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

### 기술사 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) 시 PII (Personally Identifiable Information) [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹이 에이전트 단계에서 처리됐는가?
2. [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계 시 샤드 수와 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 수가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모에 맞게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)됐는가?
3. ILM [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 Hot->Warm->Cold->Frozen->Delete 단계가 정의됐는가?
4. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 누락 방지를 위한 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 재시도 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 데드레터 큐 (Dead Letter [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))가 있는가?
5. 알림 피로 (Alert Fatigue) 방지를 위해 동적 임계값 ([Anomaly Detection](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/))을 사용하는가?

- **📢 섹션 요약 비유**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 관리의 핵심은 "얼마나 오래 보관할 것인가"와 "얼마나 빨리 찾을 것인가"의 균형이다. 오래된 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 느린 스토리지로 이동하고, 최근 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 빠른 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에 두는 ILM이 그 해답이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 단축 | 장애 감지~해결 시간 ([MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)) 80% 단축 |
| 보안 강화 | [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/)·내부자 위협 실시간 탐지 |
| 운영 비용 절감 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 예측 유지보수로 장애 예방 |
| 규정 준수 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/1058_hipaa/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 자동 보관·리포트 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 | 지속적 [성능 모니터링](/knowledge-base/studynote/02_operating_system/10_security/609_performance_monitoring/)으로 병목 선제 해결 |

[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석은 시스템이 "말하는 언어"를 이해하는 기술이다. [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서 수천 개의 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되고 사라지면서 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 더욱 복잡해지고 있다. [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 표준화와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)의 결합이 차세대 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석의 방향이다.

- **📢 섹션 요약 비유**: 좋은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석 시스템은 수십만 명의 직원이 매일 쓰는 업무 일지를 자동으로 읽고, 이상한 행동이 있으면 즉시 보고하는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)관이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| ELK [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) ([Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)-Logstash-[Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/)) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석 표준 플랫폼 |
| Fluentd / Filebeat | [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) 에이전트 |
| Grok 패턴 | 비정형 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 [정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/002_structured_data/)로 파싱하는 패턴 언어 |
| [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) ([Security Information and Event Management](/knowledge-base/studynote/09_security/13_secops_ir_forensics/625_siem_architecture/)) | 보안 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 통합 분석 플랫폼 |
| ILM ([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [Lifecycle Management](/knowledge-base/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle/)) | [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 생명주기 관리 |
| [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) | [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 통합 표준 |
| [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 고가용성 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 버퍼 |

### 📈 관련 키워드 및 발전 흐름도

```text
[로그 수집 에이전트 (Fluentd / Filebeat) — 분산 노드 로그 수집]
    |
    v
[메시지 큐 (Apache Kafka) — 고처리량 버퍼링 및 스트리밍 전달]
    |
    v
[중앙 저장·인덱싱 (Elasticsearch / OpenSearch) — 전문 검색 및 집계]
    |
    v
[시각화 (Kibana / Grafana) — 대시보드 및 알림 규칙 설정]
    |
    v
[이상 감지 (ML 기반 Anomaly Detection) — 보안·장애 자동 탐지]
```
[로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) 에이전트에서 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [버퍼링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)을 거쳐 Elasticsearch로 인덱싱하고, Kibana로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)한 뒤 ML 기반 이상 감지로 보안·장애를 자동 탐지하는 것이 ELK [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)의 표준 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
- [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석은 컴퓨터가 매일 쓰는 일기를 읽고 "오늘 이상한 일이 있었나?"를 찾아내는 거예요.
- 수백 개의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 초당 수백만 줄의 일기를 쓰는데, ELK [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 그걸 모아서 한눈에 볼 수 있게 해줘요.
- 해커가 몰래 들어오려 할 때 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 흔적이 남는데, SIEM이 그 흔적을 자동으로 찾아내요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 119 / 262

<- **이전**: [115. 이미지 분석 (Image Analysis) — CNN 기반 대용량 이미지 배치 처리](/knowledge-base/studynote/16_bigdata/05_analysis/118_image_analysis/)
**다음**: [117. 클릭스트림 분석 (Clickstream Analysis) — 사용자 행동 패턴 최적화](/knowledge-base/studynote/16_bigdata/05_analysis/120_clickstream_analysis/) ->

---
