---
title: 139. 분산 로깅 (EFK/ELK Stack) - 중앙 집중 로그 관리
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[136_variance|분산]] 로깅은 **수십~수백 개 [[532_microservices_decomposition_patterns|마이크로서비스]]의 [[568_logs_distributed_logging_elk_fluentd|로그]]를 중앙 수집·저장·검색하는 시스템**이며, ELK([[302_cdc|Elasticsearch]]·Logstash·[[169_kibana|Kibana]])·EFK([[302_cdc|Elasticsearch]]·Fluentd·[[169_kibana|Kibana]])·[[168_grafana|Grafana]] Loki가 대표 [[057_stack|스택]]이다.
> 2. **가치**: MSA에서 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 개별 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]을 가지면 장애 시 **수십 서버를 일일이 [[538_ssh_vs_telnet_secure_remote|SSH]] 접속**해야 하지만, 중앙 로깅은 **한 곳에서 전체 [[568_logs_distributed_logging_elk_fluentd|로그]]를 검색·필터·[[325_correlation_analysis_pearson_spearman|상관 분석]]**한다.
> 3. **판단 포인트**: ELK는 **전문 검색에 강하지만 비용↑**, Loki는 **레이블 기반 경량([[154_database_index_b_tree_search_optimization|인덱스]] 없음)**이며, Fluentd/Fluent Bit가 [[190_cncf_landscape_observability|CNCF]] 표준 [[626_log_collection|로그 수집]]기이다.

---

## Ⅰ. 개요 및 필요성

```text
ELK: Logstash(수집·파싱) → Elasticsearch(저장·검색) → Kibana(시각화)
EFK: Fluentd(수집, CNCF) → Elasticsearch → Kibana
Loki: Promtail(수집) → Loki(레이블 저장) → Grafana(시각화)
```

- **📢 섹션 요약 비유**: [[136_variance|분산]] 로깅은 **중앙 도서관**이다. 각 교실([[090_service_kubernetes_network_load_balancing|서비스]])의 일기장을 한 곳에 모아 **누구든 검색**할 수 있게 한다.

---

## Ⅱ~Ⅴ. 결론

중앙 집중 로깅은 **[[619_msa_traffic_hardware|MSA]] 운영의 필수 인프라**이며, ELK(전문 검색)와 Loki(경량)를 환경에 맞게 선택한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ELK** | [[302_cdc|Elasticsearch]]+Logstash+[[169_kibana|Kibana]] |
| **EFK** | Fluentd 대체 ([[190_cncf_landscape_observability|CNCF]]) |
| **Loki** | 경량 [[568_logs_distributed_logging_elk_fluentd|로그]] (레이블 기반) |
| **Fluentd** | [[190_cncf_landscape_observability|CNCF]] [[626_log_collection|로그 수집]]기 |
| **Correlation ID** | [[136_variance|분산]] [[568_logs_distributed_logging_elk_fluentd|로그]] 추적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[syslog (1980s)] → [ELK Stack (2012)]
    → [EFK (Fluentd, CNCF)] → [Grafana Loki (2018, 경량)]
    → [현재: OTel Logs — 메트릭·트레이스 통합 수집]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[136_variance|분산]] 로깅은 **중앙 도서관**이에요. 각 교실의 일기장을 **한 곳에 모아요**.
2. 모아놓으면 **누구든 쉽게 검색**할 수 있어요. "3반 수학 일기는?"
3. 일일이 교실을 돌아다니지 않아도 **한 곳에서 다 찾을** 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 373

← **이전**: [[138_logs|138. 로그 (Logs) - 구조화 로깅과 중앙 집중 관리]]
**다음**: [[140_structured_logging_json_format|140. 구조화 로깅 (Structured Logging) - JSON 포맷 표준화]] →

---
