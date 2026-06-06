---
title: "143. Span Service Operation Unit"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Span은 <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 트레이스의 기본 단위</strong>로, 하나의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내 <strong>특정 오퍼레이션(<a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 요청·DB <a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a>·<a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>지 처리)</strong>의 시작·종료·[메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 기록하며, 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)로 트리를 형성한다.
> 2. **가치**: Span에 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>명·오퍼레이션명·상태코드·에러·태그·<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 이벤트</strong>가 포함되어, 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구간의 **소요 시간·에러 여부를 정확히** 파악할 수 있다.
> 3. **판단 포인트**: Root Span(최초 진입점)·Child Span(하위 호출)의 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 트레이스 트리를 형성하며, Span [Attributes](/studynote/02_operating_system/09_file_system/502_file_attributes_metadata/)(태그)로 커스텀 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 추가한다.

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

- **📢 섹션 요약 비유**: Span은 <strong>택배 추적의 각 물류센터 기록</strong>이다. 각 센터에서 <strong>언제 도착·출발·처리</strong>했는지 기록한다.

---

## Ⅱ~Ⅴ. 결론

Span은 <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/">분산 트레이싱</a>의 기본 단위</strong>이며, 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·[Attributes](/studynote/02_operating_system/09_file_system/502_file_attributes_metadata/)·Status로 상세 추적을 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Span** | 오퍼레이션 단위 |
| **Root Span** | 최초 진입점 |
| **Child Span** | 하위 호출 |
| <strong><a href="/studynote/02_operating_system/09_file_system/502_file_attributes_metadata/">Attributes</a></strong> | 커스텀 태그 |
| **Span Events** | Span 내 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper Span (Google, 2010)] -> [Zipkin Span (2012)]
    -> [OpenTracing Span (2016)]
    -> [OTel Span (2019, 표준 통합)]
    -> [현재: Span Links — 비동기 Span 연결]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Span은 택배 추적의 <strong>각 물류센터 기록</strong>이에요.
2. "서울 센터에서 **2시간 머물렀고**, 부산 센터로 보냈다"를 기록해요.
3. 어디서 **오래 걸렸는지** 한눈에 알 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 373

<- **이전**: [142. Trace·Span·Context Propagation - 분산 추적의 핵심 구성](/studynote/15_devops_sre/03_sre_observability/142_trace_request_context/)
**다음**: [144. Context Propagation & Trace ID 전파 상세](/studynote/15_devops_sre/03_sre_observability/144_context_propagation_trace_id/) ->

---
