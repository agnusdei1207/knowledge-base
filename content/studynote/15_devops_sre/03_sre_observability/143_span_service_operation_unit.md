---
title: 143. Span 상세 - 서비스·오퍼레이션 단위 추적
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Span은 **[[136_variance|분산]] 트레이스의 기본 단위**로, 하나의 [[090_service_kubernetes_network_load_balancing|서비스]] 내 **특정 오퍼레이션([[461_http_stateless_connection_oriented|HTTP]] 요청·DB [[298_qkv_attention|쿼리]]·[[389_mesh_topology|메시]]지 처리)**의 시작·종료·[[012_metadata|메타데이터]]를 기록하며, 부모-자식 [[083_relationship_in_er_model|관계]]로 트리를 형성한다.
> 2. **가치**: Span에 **[[090_service_kubernetes_network_load_balancing|서비스]]명·오퍼레이션명·상태코드·에러·태그·[[568_logs_distributed_logging_elk_fluentd|로그]] 이벤트**가 포함되어, 각 [[090_service_kubernetes_network_load_balancing|서비스]] 구간의 **소요 시간·에러 여부를 정확히** 파악할 수 있다.
> 3. **판단 포인트**: Root Span(최초 진입점)·Child Span(하위 호출)의 부모-자식 [[083_relationship_in_er_model|관계]]가 트레이스 트리를 형성하며, Span [[502_file_attributes_metadata|Attributes]](태그)로 커스텀 [[012_metadata|메타데이터]]를 추가한다.

---

## Ⅰ. 개요 및 필요성

```text
Span 구성:
  trace_id: 전체 요청 ID
  span_id: 이 Span의 고유 ID
  parent_span_id: 부모 Span ID
  operation_name: "POST /orders"
  start_time / end_time / duration
  status: OK / ERROR
  attributes: {http.method: POST, db.type: postgres}
```

- **📢 섹션 요약 비유**: Span은 **택배 추적의 각 물류센터 기록**이다. 각 센터에서 **언제 도착·출발·처리**했는지 기록한다.

---

## Ⅱ~Ⅴ. 결론

Span은 **[[112_distributed_tracing_microservices|분산 트레이싱]]의 기본 단위**이며, 부모-자식 [[083_relationship_in_er_model|관계]]·[[502_file_attributes_metadata|Attributes]]·Status로 상세 추적을 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Span** | 오퍼레이션 단위 |
| **Root Span** | 최초 진입점 |
| **Child Span** | 하위 호출 |
| **[[502_file_attributes_metadata|Attributes]]** | 커스텀 태그 |
| **Span Events** | Span 내 [[568_logs_distributed_logging_elk_fluentd|로그]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper Span (Google, 2010)] → [Zipkin Span (2012)]
    → [OpenTracing Span (2016)]
    → [OTel Span (2019, 표준 통합)]
    → [현재: Span Links — 비동기 Span 연결]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Span은 택배 추적의 **각 물류센터 기록**이에요.
2. "서울 센터에서 **2시간 머물렀고**, 부산 센터로 보냈다"를 기록해요.
3. 어디서 **오래 걸렸는지** 한눈에 알 수 있어요!
