+++
title = "139. 분산 로깅 (EFK/ELK Stack) - 중앙 집중 로그 관리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 로깅은 <strong>수십~수백 개 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a>의 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>를 중앙 수집·저장·검색하는 시스템</strong>이며, ELK([Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)·Logstash·[Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/))·EFK([Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)·Fluentd·[Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/))·[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) Loki가 대표 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이다.
> 2. **가치**: MSA에서 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 개별 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 가지면 장애 시 <strong>수십 서버를 일일이 <a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/">SSH</a> 접속</strong>해야 하지만, 중앙 로깅은 <strong>한 곳에서 전체 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>를 검색·필터·<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/325_correlation_analysis_pearson_spearman/">상관 분석</a></strong>한다.
> 3. **판단 포인트**: ELK는 **전문 검색에 강하지만 비용^**, Loki는 <strong>레이블 기반 경량(<a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 없음)</strong>이며, Fluentd/Fluent Bit가 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 표준 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/)기이다.

---

## Ⅰ. 개요 및 필요성

```text
ELK: Logstash(수집·파싱) -> Elasticsearch(저장·검색) -> Kibana(시각화)
EFK: Fluentd(수집, CNCF) -> Elasticsearch -> Kibana
Loki: Promtail(수집) -> Loki(레이블 저장) -> Grafana(시각화)
```

- **📢 섹션 요약 비유**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 로깅은 <strong>중앙 도서관</strong>이다. 각 교실([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))의 일기장을 한 곳에 모아 <strong>누구든 검색</strong>할 수 있게 한다.

---

## Ⅱ~Ⅴ. 결론

중앙 집중 로깅은 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 운영의 필수 인프라</strong>이며, ELK(전문 검색)와 Loki(경량)를 환경에 맞게 선택한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ELK** | [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/)+Logstash+[Kibana](/knowledge-base/studynote/16_bigdata/08_visualization/169_kibana/) |
| **EFK** | Fluentd 대체 ([CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/)) |
| **Loki** | 경량 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) (레이블 기반) |
| **Fluentd** | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/)기 |
| **Correlation ID** | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 추적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[syslog (1980s)] -> [ELK Stack (2012)]
    -> [EFK (Fluentd, CNCF)] -> [Grafana Loki (2018, 경량)]
    -> [현재: OTel Logs — 메트릭·트레이스 통합 수집]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 로깅은 <strong>중앙 도서관</strong>이에요. 각 교실의 일기장을 **한 곳에 모아요**.
2. 모아놓으면 <strong>누구든 쉽게 검색</strong>할 수 있어요. "3반 수학 일기는?"
3. 일일이 교실을 돌아다니지 않아도 **한 곳에서 다 찾을** 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 373

<- **이전**: [138. 로그 (Logs) - 구조화 로깅과 중앙 집중 관리](/knowledge-base/studynote/15_devops_sre/03_sre_observability/138_logs/)
**다음**: [140. 구조화 로깅 (Structured Logging) - JSON 포맷 표준화](/knowledge-base/studynote/15_devops_sre/03_sre_observability/140_structured_logging_json_format/) ->

---
