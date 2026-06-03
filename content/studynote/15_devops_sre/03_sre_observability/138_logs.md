---
title: 138. 로그 (Logs) - 구조화 로깅과 중앙 집중 관리
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[568_logs_distributed_logging_elk_fluentd|로그]]는 **시스템·애플리케이션이 발생시킨 이벤트의 시간순 텍스트 기록**이며, [[642_observability_telemetry|Observability]] 3대 축([[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces) 중 가장 상세한 정보를 제공한다.
> 2. **가치**: [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 "무엇이 이상한가", 트레이스는 "어디서 느린가"를 알려주지만, [[568_logs_distributed_logging_elk_fluentd|로그]]는 **"왜 발생했는가"의 상세 맥락(에러 [[389_mesh_topology|메시]]지·[[057_stack|스택]] 트레이스·요청 파라미터)**을 제공한다.
> 3. **판단 포인트**: [[140_structured_logging_json_format|구조화 로깅]]([[343_json|JSON]])이 필수이며, ELK([[302_cdc|Elasticsearch]]·Logstash·[[169_kibana|Kibana]]) 또는 [[168_grafana|Grafana]] Loki가 중앙 집중 [[568_logs_distributed_logging_elk_fluentd|로그]] 관리의 표준 [[057_stack|스택]]이다.

---

## Ⅰ. 개요 및 필요성

```text
비구조화: "2024-01-15 ERROR: Payment failed for user 123"
구조화(JSON): {"ts":"2024-01-15","level":"ERROR","msg":"Payment failed","user_id":123}
  → 검색·필터링·분석 용이
  → 중앙 집중: Loki/ELK로 수집 → 쿼리·대시보드
```

- **📢 섹션 요약 비유**: [[568_logs_distributed_logging_elk_fluentd|로그]]는 **비행기 블랙박스**이다. 사고(장애) 후 **원인을 상세히 추적**하는 유일한 기록이다.

---

## Ⅱ~Ⅴ. 결론

구조화 [[568_logs_distributed_logging_elk_fluentd|로그]] + 중앙 집중 관리(Loki/ELK)는 **장애 원인 분석의 핵심**이며, [[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이스와 [[325_correlation_analysis_pearson_spearman|상관 분석]]으로 완전한 관측을 달성한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[568_logs_distributed_logging_elk_fluentd|로그]]** | 상세 이벤트 기록 |
| **[[140_structured_logging_json_format|구조화 로깅]]** | [[343_json|JSON]] 형식 |
| **ELK** | [[302_cdc|Elasticsearch]]+Logstash+[[169_kibana|Kibana]] |
| **Loki** | [[168_grafana|Grafana]] [[568_logs_distributed_logging_elk_fluentd|로그]] 시스템 |
| **Correlation ID** | [[568_logs_distributed_logging_elk_fluentd|로그]]-트레이스 연결 |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 로그 (tail -f)] → [syslog (중앙 수집)]
    → [ELK Stack (2012)] → [Fluentd/Fluent Bit (CNCF)]
    → [Grafana Loki (2018, 경량)]
    → [현재: OTel Logs — 메트릭·트레이스 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[568_logs_distributed_logging_elk_fluentd|로그]]는 **비행기 블랙박스**예요. 무슨 일이 있었는지 **자세히 기록**해요.
2. 사고(장애)가 나면 블랙박스를 열어 **원인을 찾아요**.
3. JSON으로 **정리 정돈**하면 검색하기 쉽고 빨리 원인을 알 수 있어요!
