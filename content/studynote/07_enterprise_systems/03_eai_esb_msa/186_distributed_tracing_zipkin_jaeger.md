---
title: 186. 분산 추적 (Distributed Tracing) 인프라 - 다수 서비스를 거치는 응용 프로그램 프로그래밍 인터페이스 (Application
  Programming Interface, API) 호출 구간(Span/Trace) 병목 파악 (Zipkin, Jaeger 연동)
date: '2026-05-06'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]])은 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[365_msa_microservice_architecture|Microservice Architecture]], [[619_msa_traffic_hardware|MSA]])에서 하나의 사용자 요청이 여러 [[090_service_kubernetes_network_load_balancing|서비스]]를 지나는 동안 같은 Trace ID와 Span 계층으로 연결해 전체 호출 여정을 복원하는 관측성 인프라다.
> 2. **가치**: [[568_logs_distributed_logging_elk_fluentd|로그]]가 흩어진 환경에서도 어느 구간에서 [[015_지연_데이터_관점|지연]]이 커졌고 어떤 하위 호출이 실패했는지를 시간축으로 보여 주어 평균 [[658_ir_recovery|복구]] 시간 (Mean Time To [[658_ir_recovery|Recovery]], [[451_mttr|MTTR]])을 크게 줄인다.
> 3. **판단 포인트**: Zipkin이나 Jaeger 같은 도구를 설치하는 것만으로는 부족하며, [[033_context|컨텍스트]] 전파, 샘플링 [[268_strategy_pattern|전략]], [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]] 연계가 함께 설계되어야 진짜 병목 분석 도구가 된다.

---

## Ⅰ. 개요 및 필요성

[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 여러 [[090_service_kubernetes_network_load_balancing|서비스]]로 쪼개진 시스템에서 단일 요청의 인과관계를 다시 이어 붙이기 위한 기술이다. 모놀리식 환경에서는 애플리케이션 [[568_logs_distributed_logging_elk_fluentd|로그]] 한 [[501_file_definition_logical_record|파일]]만 뒤져도 처리 흐름을 대략 따라갈 수 있었지만, MSA에서는 게이트웨이, 주문, 결제, 재고, [[145_message_broker_sync_async|메시지 브로커]], [[002_database_definition|데이터베이스]]가 모두 따로 움직이므로 요청 하나의 여정이 금방 파편화된다. 이때 단순 [[626_log_collection|로그 수집]]만으로는 "이 [[568_logs_distributed_logging_elk_fluentd|로그]]들이 같은 사용자 요청에 속하는가"를 즉시 판단하기 어렵다.

이 문제가 중요한 이유는 [[090_service_kubernetes_network_load_balancing|서비스]] [[015_지연_데이터_관점|지연]]이 전파되기 때문이다. 예를 들어 주문 [[090_service_kubernetes_network_load_balancing|서비스]] 응답이 2초 느릴 때, 진짜 원인이 주문 [[090_service_kubernetes_network_load_balancing|서비스]] 자체인지 결제 응용 프로그램 프로그래밍 인터페이스 ([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]]) 호출인지, 그 아래 [[002_database_definition|데이터베이스]] [[298_qkv_attention|쿼리]]인지 알 수 없다면 팀 간 책임 공방만 길어진다. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 요청마다 공통 [[289_identification_flags_fragmentation_offset|식별자]]를 부여하고, 각 구간의 시작·종료 시각과 부모-자식 [[083_relationship_in_er_model|관계]]를 기록해 이런 병목의 위치와 순서를 시각적으로 드러낸다.

또한 현대 시스템은 동기 [[461_http_stateless_connection_oriented|HTTP]] 호출만 있는 것이 아니라 [[389_mesh_topology|메시]]지 큐와 비동기 작업도 섞여 있다. 이때 Trace ID가 헤더나 [[389_mesh_topology|메시]]지 [[012_metadata|메타데이터]]를 따라 끊김 없이 전달되지 않으면, 관측성은 한 구간짜리 부분 지도에 그친다. 결국 [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]의 본질은 화면이 아니라 **문맥을 전파하는 규율**에 있다.

- **📢 섹션 요약 비유**: [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 여러 역을 거치는 택배 상자에 같은 송장 번호를 계속 붙여 두는 것과 같다. 그래야 어느 물류센터에서 시간이 오래 걸렸는지 한눈에 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 크게 계측, 전파, 수집, 저장, 조회의 다섯 단계로 동작한다. 각 [[090_service_kubernetes_network_load_balancing|서비스]]는 트레이서 [[336_library_vs_framework|라이브러리]]나 [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] 계측 [[336_library_vs_framework|라이브러리]]를 통해 현재 요청의 Trace ID와 Span을 만들고, 이를 [[461_http_stateless_connection_oriented|HTTP]] 헤더나 [[389_mesh_topology|메시]]지 [[082_attribute_types_er_model|속성]]으로 다음 [[090_service_kubernetes_network_load_balancing|서비스]]에 넘긴다. 이후 [[087_process_state_transition|생성]]된 Span [[001_dikw_pyramid|데이터]]는 에이전트나 컬렉터로 보내지고, 저장소에 적재된 뒤 Zipkin이나 Jaeger 같은 사용자 인터페이스에서 조회된다.

아래 그림은 요청 흐름과 추적 수집 흐름을 함께 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Request path and tracing pipeline                                  │
├────────────────────────────────────────────────────────────────────┤
│ Client -> Gateway -> Order -> Payment -> DB                        │
│            │         │          │                                  │
│            │         │          └─ span-4 : SQL                    │
│            │         └──────────── span-3 : payment call           │
│            └────────────────────── span-2 : order handler          │
│ trace-1 ───────────────────────── span-1 : gateway                 │
│                                                                    │
│ Services export spans -> Collector -> Storage -> Zipkin / Jaeger   │
└────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [[303_trace_id|Trace ID]] | 하나의 요청 전체를 묶는 [[289_identification_flags_fragmentation_offset|식별자]] | [[090_service_kubernetes_network_load_balancing|서비스]] 간 전파가 끊기면 추적도 끊긴다. |
| Span | 개별 작업 구간의 단위 | 이름, 시작·종료 시각, 상태, 태그 설계가 중요하다. |
| [[570_trace_id_span_id_context_propagation|Context Propagation]] | 헤더와 [[389_mesh_topology|메시]]지에 [[289_identification_flags_fragmentation_offset|식별자]]를 전달 | HTTP뿐 아니라 비동기 [[389_mesh_topology|메시]]징까지 고려해야 한다. |
| Collector | 각 [[090_service_kubernetes_network_load_balancing|서비스]]의 Span을 수집 | 애플리케이션 경로와 분리해 비동기 수집하는 편이 안전하다. |
| Storage | 추적 [[001_dikw_pyramid|데이터]]를 저장 | 샘플링 비율과 보존 기간이 비용을 좌우한다. |
| 조회 인터페이스 | 시간축, [[090_service_kubernetes_network_load_balancing|서비스]] [[070_graph_datastructure|그래프]], 검색 제공 | `trace_id`와 [[568_logs_distributed_logging_elk_fluentd|로그]] 상관관계가 있으면 분석 속도가 빨라진다. |

여기서 핵심은 Span이 단순 시간 기록이 아니라 계층 구조를 가진다는 점이다. 부모 Span은 하위 호출 전체 시간을 품고, 자식 Span은 세부 구간의 [[015_지연_데이터_관점|지연]]을 보여 준다. 따라서 전체 [[015_지연_데이터_관점|지연]]이 1초일 때, 그중 700밀리초가 결제 호출이고 다시 그 안 500밀리초가 [[002_database_definition|데이터베이스]] [[298_qkv_attention|쿼리]]였다는 식으로 병목이 단계적으로 드러난다.

또 하나 중요한 축은 샘플링이다. 모든 요청을 100% 저장하면 가장 자세하지만 비용과 저장량이 급격히 커진다. 반대로 너무 적게 수집하면 희귀 오류를 놓친다. 그래서 일반 요청은 일부만 수집하고, 오류나 고지연 요청은 우선 저장하는 [[268_strategy_pattern|전략]]이 대규모 환경에서 자주 사용된다.

- **📢 섹션 요약 비유**: [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 마라톤 중계에서 선수 전체 기록뿐 아니라 구간 통과 시간까지 재는 것과 같다. 전체 순위만 보면 누가 늦었는지 모르지만, 구간 기록이 있으면 어디서 속도가 떨어졌는지 바로 보인다.

---

## Ⅲ. 비교 및 연결

[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 [[568_logs_distributed_logging_elk_fluentd|로그]]와 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 사이에서 독특한 역할을 한다. [[568_logs_distributed_logging_elk_fluentd|로그]]는 사건의 상세 문맥을, [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 [[178_as_is_to_be_analysis|현재 상태]]와 수치 추세를, 추적은 요청의 경로와 인과관계를 보여 준다. 따라서 장애 분석에서는 [[342_routing_metric_hop_bandwidth_delay|메트릭]]으로 이상 시점을 찾고, 추적으로 [[015_지연_데이터_관점|지연]] 구간을 좁히고, [[568_logs_distributed_logging_elk_fluentd|로그]]로 구체 오류 [[389_mesh_topology|메시]]지를 [[396_validation|확인]]하는 식의 조합이 가장 강력하다.

| [[130_signal|신호]] | 주로 답하는 질문 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 얼마나 느려지고 얼마나 실패했는가 | 경보와 추세 파악에 강함 | 개별 요청 문맥은 약함 |
| [[568_logs_distributed_logging_elk_fluentd|로그]] | 어떤 오류 [[389_mesh_topology|메시]]지와 상태가 발생했는가 | 상세 원인 분석에 강함 | 요청 간 인과관계 복원이 어렵다 |
| [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] | 어느 [[090_service_kubernetes_network_load_balancing|서비스]] 구간에서 병목이 생겼는가 | 호출 경로와 [[015_지연_데이터_관점|지연]] 분해에 강함 | 전파 누락 시 전체 흐름이 끊긴다 |

Zipkin과 Jaeger도 지향점이 조금 다르다. Zipkin은 비교적 단순하고 가벼운 배포 경험을 제공해 빠른 도입에 유리하고, Jaeger는 샘플링 [[268_strategy_pattern|전략]], [[090_service_kubernetes_network_load_balancing|서비스]] 의존성 [[003_bigdata_7v|시각화]], 대규모 배포 경험이 풍부해 [[531_cloud_native_architecture|클라우드 네이티브]] 환경에서 많이 선택된다. 최근에는 두 도구 모두 OpenTelemetry와 함께 쓰이거나, [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] Collector를 앞단에 두어 백엔드를 교체 가능한 구조로 가져가는 경우가 늘고 있다.

| 도구 | 강점 | 잘 맞는 환경 |
| :--- | :--- | :--- |
| Zipkin | 단순한 구조, 가벼운 시작, 빠른 학습 | 소규모~중간 규모, 빠른 [[501_file_definition_logical_record|파일]]럿 도입 |
| Jaeger | 풍부한 운영 옵션, 샘플링과 [[003_bigdata_7v|시각화]] 강점 | [[196_kubernetes_k8s_container_orchestration|쿠버네티스]], [[302_service_mesh_istio|서비스 메시]], 대규모 [[532_microservices_decomposition_patterns|마이크로서비스]] |

즉 도구 비교보다 먼저 따질 것은 추적 [[014_data_model_components|데이터 모델]]과 전파 표준이다. B3 헤더나 W3C (World Wide Web Consortium) Trace [[033_context|Context]] 같은 전파 규약이 맞지 않으면, Zipkin과 Jaeger 중 무엇을 쓰든 연결성이 약해진다. 관측성 인프라의 본질은 백엔드 제품이 아니라 **끊기지 않는 문맥 체인**이다.

- **📢 섹션 요약 비유**: [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 자동차 계기판이고, [[568_logs_distributed_logging_elk_fluentd|로그]]는 정비 기사 메모장이며, [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 자동차가 어느 길로 갔는지 그린 내비게이션 기록이다. 세 가지를 합쳐야 사고 원인을 가장 빨리 찾을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 [[014_api_posix|API]] 게이트웨이, 핵심 비즈니스 [[090_service_kubernetes_network_load_balancing|서비스]], 외부 호출 구간부터 우선 적용하는 것이 효과적이다. [[568_logs_distributed_logging_elk_fluentd|로그]]인, 주문, 결제, 검색처럼 사용자 체감이 큰 경로를 먼저 계측하면 작은 도입으로도 큰 가치를 얻을 수 있다. 특히 외부 결제사, 캐시, [[002_database_definition|데이터베이스]], [[145_message_broker_sync_async|메시지 브로커]]와 만나는 경계에 Span을 남기면 시스템 내부와 외부 중 어디가 느린지 빠르게 구분할 수 있다.

또한 추적은 [[568_logs_distributed_logging_elk_fluentd|로그]]와 연결될 때 훨씬 강력하다. 모든 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]에 `trace_id`를 함께 남기면 운영자는 Jaeger나 Zipkin에서 느린 구간을 찾고, 같은 [[289_identification_flags_fragmentation_offset|식별자]]로 [[568_logs_distributed_logging_elk_fluentd|로그]] 저장소에서 상세 오류를 바로 검색할 수 있다. 반대로 추적 화면만 있고 [[568_logs_distributed_logging_elk_fluentd|로그]] 상관관계가 없으면 "어디서 느린지"는 알아도 "왜 느린지"는 다시 수작업으로 찾아야 한다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 게이트웨이부터 하위 [[090_service_kubernetes_network_load_balancing|서비스]], [[389_mesh_topology|메시]]지 큐, [[002_database_definition|데이터베이스]] 호출까지 [[303_trace_id|Trace ID]] 전파가 끊기지 않는가?
2. Span 이름과 태그가 [[090_service_kubernetes_network_load_balancing|서비스]]명, [[014_api_posix|API]] 경로, 오류 코드, 외부 대상 등 분석 가능한 수준으로 설계되어 있는가?
3. 정상 트래픽과 오류 트래픽에 대해 샘플링 [[268_strategy_pattern|전략]]이 분리되어 있는가?
4. [[568_logs_distributed_logging_elk_fluentd|로그]]와 [[342_routing_metric_hop_bandwidth_delay|메트릭]]이 같은 [[289_identification_flags_fragmentation_offset|식별자]] 또는 공통 라벨로 연결되는가?
5. Zipkin 또는 Jaeger 도입 전에 [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] 같은 중립 계층을 둘 필요가 있는가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Trace ID를 게이트웨이까지만 넣고 내부 비동기 [[389_mesh_topology|메시]]지에는 전달하지 않는 경우
- 모든 요청을 100% 저장해 비용과 저장소를 감당하지 못하는 경우
- Span 이름을 `method1`, `call2`처럼 모호하게 지어 분석 가치가 떨어지는 경우
- 추적 대시보드만 믿고 [[568_logs_distributed_logging_elk_fluentd|로그]] 상관관계를 만들지 않는 경우

결론적으로 기술사 답안에서는 "Zipkin으로 본다"보다, **추적을 위해 문맥을 전파하고 샘플링하며 다른 관측성 [[130_signal|신호]]와 연결한다**는 설계 관점을 강조해야 한다. 도구는 수단이고, 병목의 인과관계를 복원하는 구조가 목적이다.

- **📢 섹션 요약 비유**: 도로마다 CCTV를 달아도 차량 번호가 계속 바뀌면 한 차의 이동 경로를 찾을 수 없다. 같은 번호판이 끝까지 이어져야 어디서 막혔는지 알 수 있는 것처럼 [[303_trace_id|Trace ID]] 전파가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]이 잘 구축되면 운영팀은 "느리다"는 현상을 구체적인 시간축과 호출 구조로 바꿔 볼 수 있다. [[090_service_kubernetes_network_load_balancing|서비스]] 간 책임 경계가 복잡한 [[619_msa_traffic_hardware|MSA]] 환경에서도 병목의 위치, 외부 의존성 [[015_지연_데이터_관점|지연]], 재시도 폭증, 팬아웃 호출 구조를 빠르게 파악할 수 있어 장애 대응 속도가 높아진다. 이는 단순 [[229_monitor|모니터]]링을 넘어 설계 개선에도 직접적인 피드백을 제공한다.

하지만 추적은 공짜가 아니다. 계측 코드, 헤더 전파, 샘플링, 저장 비용, [[781_personal_information|개인정보]] [[172_maas_mobility_as_a_service|마스]]킹, 대시보드 운영이 함께 필요하다. 특히 비동기 흐름과 배치 작업까지 추적하려면 표준화와 개발 규율이 따라와야 하므로, 도입 범위와 운영 목표를 명확히 잡는 것이 중요하다.

결국 [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 "예쁜 [[039_gantt_chart|간트 차트]] 도구"가 아니라, **[[136_variance|분산]] 시스템의 인과관계를 복원하는 운영 인프라**다. Zipkin과 Jaeger는 그 결과를 보여 주는 대표 구현일 뿐이며, 기억해야 할 핵심은 요청 문맥을 끊기지 않게 이어 주는 체계라는 점이다.

- **📢 섹션 요약 비유**: 거대한 놀이공원에서 아이가 어디서 길을 잃었는지 찾으려면 입장부터 놀이기구 탑승까지 같은 팔찌 번호가 계속 기록되어야 한다. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]도 요청에 그 팔찌를 채워 주는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[303_trace_id|Trace ID]] | 하나의 요청을 여러 [[090_service_kubernetes_network_load_balancing|서비스]] [[568_logs_distributed_logging_elk_fluentd|로그]]와 Span에 연결하는 기준 [[289_identification_flags_fragmentation_offset|식별자]]다. |
| Span | 세부 작업 구간의 시간과 상태를 표현하는 기본 단위다. |
| [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] | 계측과 수집을 표준화해 Zipkin, Jaeger 같은 백엔드를 유연하게 교체하게 해 준다. |
| 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]] | `trace_id`를 함께 남기면 추적과 [[568_logs_distributed_logging_elk_fluentd|로그]] 상관분석이 쉬워진다. |
| [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) | [[264_proxy_pattern_surrogate_access_control|프록시]] 계층에서 자동 계측과 [[033_context|컨텍스트]] 전파를 보조할 수 있다. |
| 샘플링 ([[056_표본화_Sampling|Sampling]]) | 비용과 가시성의 균형을 잡는 핵심 운영 [[164_policy|정책]]이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
모놀리식 디버깅 한계 없음
        │
        ▼
MSA 확산과 로그 파편화
        │
        ▼
Trace ID · Span 기반 문맥 전파
        │
        ▼
Zipkin / Jaeger 수집 · 시각화
        │
        ▼
OpenTelemetry 기반 통합 관측성
```

이 흐름은 단순 [[119_log_analysis|로그 분석]]에서 시작해, 요청 문맥 복원과 표준화된 관측성 플랫폼으로 성숙해 가는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]은 택배 상자에 같은 송장 번호를 붙여서 여러 창고를 지나도 같은 물건인지 알아보게 하는 방법이에요.
2. 그래서 어디 창고에서 오래 멈췄는지, 어디서 문제가 생겼는지 금방 찾을 수 있어요.
3. 번호가 중간에 사라지면 길을 잃어버리니까, 끝까지 같은 번호를 전해 주는 게 가장 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 482

← **이전**: [[185_log_aggregation_fluentd_elasticsearch|185. 로그 수집 통합 (Log Aggregation) 아키텍처 - Fluentd -> Elasticsearch 파이프라인]]
**다음**: [[187_strangler_fig_pattern_msa_migration|187. 스트랭글러 피그 패턴 (Strangler Fig Pattern) - 점진적 MSA 전환]] →

---
