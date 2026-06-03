---
title: 162. APM (Application Performance Management)
date: '2026-04-21'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: APM (Application [[282_performance_tactics|Performance]] [[372_management|Management]])은 애플리케이션 요청을 코드·[[191_transaction_concept_states|트랜잭션]]·의존 [[090_service_kubernetes_network_load_balancing|서비스]] 수준까지 계측해, 느림과 오류의 원인을 빠르게 찾게 해 주는 [[282_performance_tactics|성능]] 관리 체계다.
> 2. **가치**: 인프라 [[342_routing_metric_hop_bandwidth_delay|메트릭]]만으로는 "서버는 멀쩡한데 왜 사용자 응답이 느린가"를 설명하기 어렵지만, APM은 요청 경로와 병목 구간을 한 화면에서 연결해 준다.
> 3. **판단 포인트**: APM의 효과는 계측 범위, 샘플링 [[268_strategy_pattern|전략]], 비용 통제에 달려 있다. 무조건 많이 수집하는 것보다 [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]])와 장애 대응 목적에 맞게 설계해야 운영 가치가 높다.

---

## Ⅰ. 개요 및 필요성

APM (Application [[282_performance_tactics|Performance]] [[372_management|Management]])은 애플리케이션 [[282_performance_tactics|성능]]을 지속적으로 측정하고, 문제가 발생했을 때 코드·[[298_qkv_attention|쿼리]]·외부 호출 수준까지 원인을 추적할 수 있게 하는 관리 체계다. 과거에는 CPU, 메모리, 디스크 같은 인프라 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 [[568_logs_distributed_logging_elk_fluentd|로그]]만으로 운영하는 경우가 많았지만, [[532_microservices_decomposition_patterns|마이크로서비스]]와 [[136_variance|분산]] 시스템이 보편화되면서 "느린 요청 하나"가 여러 [[090_service_kubernetes_network_load_balancing|서비스]]와 [[002_database_definition|데이터베이스]]를 거치는 구조가 되었다. 이 환경에서는 서버 자원 사용률만 봐서는 사용자 체감 [[282_performance_tactics|성능]]을 설명하기 어렵다.

APM이 필요한 핵심 이유는 원인 분석 시간을 줄이기 위해서다. 평균 [[138_response_time|응답 시간]]만 보고 있으면 어느 요청이 느렸는지, 어느 함수나 SQL이 병목인지, 외부 [[014_api_posix|API]] 호출이 원인인지 분리하기 어렵다. APM은 요청 단위로 실행 흐름을 남겨 [[282_performance_tactics|성능]] 저하를 재현 가능한 [[001_dikw_pyramid|데이터]]로 바꾸고, 평균이 아닌 P95·P99 [[015_지연_데이터_관점|지연]] 구간까지 다룰 수 있게 만든다.

오늘날 APM은 관측성 ([[642_observability_telemetry|Observability]])의 한 축으로 이해하는 것이 적절하다. [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스 중에서 APM은 특히 애플리케이션 내부 실행 흐름과 [[090_service_kubernetes_network_load_balancing|서비스]] 의존 경로를 해석하는 데 강하다.

- **📢 섹션 요약 비유**: APM은 병원 건강검진표가 아니라 수술 중 생체 [[229_monitor|모니터]]와 같다. 몸 상태가 나쁘다는 사실만이 아니라, 정확히 어느 부위에서 문제가 시작됐는지 바로 보여 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

APM은 보통 애플리케이션 에이전트, 텔레메트리 수집 경로, 분석 백엔드, [[003_bigdata_7v|시각화]] 대시보드로 구성된다. 에이전트는 애플리케이션 프로세스 안에서 [[461_http_stateless_connection_oriented|HTTP]] 요청, [[002_database_definition|데이터베이스]] 호출, 외부 [[014_api_posix|API]], 예외, 런타임 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 계측한다. 수집된 [[001_dikw_pyramid|데이터]]는 [[190_opentelemetry_cncf_observability_standard|오픈텔레메트리]] ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]]) 또는 벤더 전용 [[295_protocol_field_tcp_udp_icmp|프로토콜]]로 백엔드에 전송되고, 백엔드는 이를 [[191_transaction_concept_states|트랜잭션]] 뷰·[[090_service_kubernetes_network_load_balancing|서비스]] 맵·슬로우 [[298_qkv_attention|쿼리]] 분석으로 재구성한다.

아래 그림은 APM이 단순 [[568_logs_distributed_logging_elk_fluentd|로그]] 저장이 아니라 "요청 발생 → 계측 → 집계 → 병목 분석"의 폐쇄 루프라는 점을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────┐
│                    APM 데이터 처리 흐름                      │
├──────────────────────────────────────────────────────────────┤
│ 사용자 요청                                                  │
│     │                                                        │
│     ▼                                                        │
│ 애플리케이션 + APM Agent / OpenTelemetry SDK                │
│     │                                                        │
│     ├─ 트랜잭션 시간 · 오류 · 스팬(Span) 수집               │
│     ├─ DB 쿼리 · 외부 API · 런타임 메트릭 수집              │
│     ▼                                                        │
│ Collector / Vendor Ingest                                   │
│     │                                                        │
│     ▼                                                        │
│ APM Backend                                                  │
│     ├─ 서비스 맵(Service Map)                                │
│     ├─ 슬로우 트랜잭션 분석                                  │
│     ├─ 오류 상관관계 분석                                    │
│     ▼                                                        │
│ 운영자 대시보드 · 알람 · 최적화 액션                         │
└──────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 에이전트 (Agent) | 코드 실행 경로와 런타임 이벤트 계측 | 자동 계측 범위와 오버헤드 균형 |
| 컬렉터 (Collector) | 텔레메트리 수집·가공·전달 | 샘플링, 필터링, 보안 [[172_maas_mobility_as_a_service|마스]]킹 |
| APM 백엔드 | [[191_transaction_concept_states|트랜잭션]] 저장, 상관관계 분석, [[003_bigdata_7v|시각화]] | 보존 기간과 질의 [[282_performance_tactics|성능]] |
| 대시보드/알람 | 병목 탐지와 운영 대응 | [[181_slo_service_level_objective|SLO]] 기반 [[431_ssthresh_slow_start_threshold|임계치]], 팀별 뷰 분리 |

APM의 핵심 원리는 상관관계다. 단일 요청의 [[138_response_time|응답 시간]], 내부 함수 실행 시간, SQL [[015_지연_데이터_관점|지연]], 예외, 하위 [[090_service_kubernetes_network_load_balancing|서비스]] 호출을 하나의 [[191_transaction_concept_states|트랜잭션]] 맥락으로 묶어야 원인 분석이 가능하다. 그래서 APM은 단순 평균 지표보다 요청 샘플, 스팬 계층, 태그 [[268_strategy_pattern|전략]], [[090_service_kubernetes_network_load_balancing|서비스]] 명명 규칙이 더 중요할 때가 많다.

- **📢 섹션 요약 비유**: APM은 공장 전체 전력 사용량만 보는 계량기가 아니라, 어느 생산 라인 어느 기계가 병목인지까지 보여 주는 스마트 제어판과 같다.

---

## Ⅲ. 비교 및 연결

APM은 관측성 도구 중 하나이므로, 인프라 [[229_monitor|모니터]]링·[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]·실사용자 [[229_monitor|모니터]]링과의 경계를 이해해야 한다. 인프라 [[229_monitor|모니터]]링은 자원 상태를, [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]])은 [[090_service_kubernetes_network_load_balancing|서비스]] 간 호출 흐름을, 실사용자 [[229_monitor|모니터]]링 ([[163_rum_real_user_monitoring|RUM]], [[163_rum_real_user_monitoring|Real User Monitoring]])은 브라우저나 모바일 사용 경험을 본다. APM은 그중에서도 애플리케이션 내부 병목을 실무자가 바로 조치할 수 있는 수준으로 드릴다운하는 데 강하다.

| 관점 | APM | 인프라 [[229_monitor|모니터]]링 | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] | [[163_rum_real_user_monitoring|RUM]] |
| :--- | :--- | :--- | :--- | :--- |
| 주 대상 | 애플리케이션 요청·코드 경로 | CPU, 메모리, 네트워크 | [[090_service_kubernetes_network_load_balancing|서비스]] 간 호출 체인 | 사용자 화면 체감 [[282_performance_tactics|성능]] |
| 대표 질문 | 어느 코드·[[298_qkv_attention|쿼리]]가 느린가? | 서버 자원이 부족한가? | 어느 [[090_service_kubernetes_network_load_balancing|서비스]]에서 [[015_지연_데이터_관점|지연]]이 시작됐는가? | 사용자는 실제로 느린가? |
| 강점 | 원인 분석, 병목 [[655_ir_detection_analysis|식별]] | [[094_capacity_management|용량 관리]], 인프라 경보 | [[090_service_kubernetes_network_load_balancing|서비스]] 의존 [[083_relationship_in_er_model|관계]] 파악 | 프론트엔드 경험 [[396_validation|확인]] |
| 한계 | 비용·오버헤드 | 코드 수준 분석 부족 | 내부 메서드 분석은 제한적 | 백엔드 원인 자체는 못 봄 |

APM은 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표 ([[181_slo_service_level_objective|SLO]], [[123_slo_service_level_objective|Service Level Objective]]) 운영과도 밀접하다. [[181_slo_service_level_objective|SLO]] 위반이 발생했을 때 단순히 알람만 울리는 것으로는 부족하고, 오류 예산([[101_error_budget_sre|Error Budget]])을 어디서 소진했는지 찾아야 한다. APM이 있으면 P99 [[015_지연_데이터_관점|지연]]을 유발한 엔드포인트와 [[298_qkv_attention|쿼리]]를 빠르게 좁힐 수 있어, 장애 대응과 [[282_performance_tactics|성능]] 개선 우선순위를 명확히 세울 수 있다.

또한 현대 APM은 [[190_opentelemetry_cncf_observability_standard|오픈텔레메트리]] 기반으로 [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이스를 통합하려는 방향으로 발전 중이다. 즉 독립 제품이라기보다 관측성 플랫폼의 애플리케이션 특화 계층으로 보는 시각이 점점 중요해지고 있다.

- **📢 섹션 요약 비유**: 인프라 [[229_monitor|모니터]]링이 건물 전기·수도 상태를 보는 것이라면, APM은 사무실 안에서 어떤 부서가 일을 막고 있는지까지 보는 관리 도구다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 APM 도입은 도구 구매보다 계측 [[268_strategy_pattern|전략]] 수립이 먼저다. 모든 [[191_transaction_concept_states|트랜잭션]]을 무제한 저장하면 비용과 저장소, 분석 복잡도가 급증하므로, 핵심 API와 고가치 사용자 흐름부터 우선 계측하는 것이 바람직하다. 특히 고트래픽 [[090_service_kubernetes_network_load_balancing|서비스]]에서는 샘플링 비율, [[782_sensitive_information|민감정보]] [[172_maas_mobility_as_a_service|마스]]킹, 태그 카디널리티(Cardinality) 통제가 [[282_performance_tactics|성능]]과 비용을 좌우한다.

### 도입 판단 [[435_checklist_based_testing|체크리스트]]

1. 장애 시 "느리다"는 사실은 알지만 원인 파악에 시간이 오래 걸리는가?
2. P95·P99 [[015_지연_데이터_관점|지연]]을 엔드포인트와 내부 의존성 수준으로 봐야 하는가?
3. [[532_microservices_decomposition_patterns|마이크로서비스]], [[002_database_definition|데이터베이스]], 외부 [[014_api_posix|API]] 호출이 얽혀 병목 위치가 불명확한가?
4. 규제·보안 요구에 따라 요청 [[819_data_masking|데이터 마스킹]] [[164_policy|정책]]을 설계했는가?
5. 상용 도구와 [[191_oss_license_compliance|오픈소스]] 조합 중 운영 역량과 예산에 맞는 선택이 가능한가?

### 실무 판단 포인트

- **상용 APM 선택**: 자동 계측 범위, [[241_machine_learning_basics|머신러닝]] 기반 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]], 지원 조직이 중요할 때 유리
- **[[191_oss_license_compliance|오픈소스]] 중심 선택**: [[190_opentelemetry_cncf_observability_standard|오픈텔레메트리]]와 자체 운영 역량이 있고 비용 통제가 중요할 때 유리
- **주의 사항**: 과도한 태그 추가, 전체 트레이스 무차별 저장, [[782_sensitive_information|민감정보]] 노출, 경고 과다 발생은 대표적 실패 패턴

실제 운영에서는 APM 대시보드를 SLO와 연결해야 가치가 커진다. 예를 들어 결제 API의 P99 [[015_지연_데이터_관점|지연]]이 [[431_ssthresh_slow_start_threshold|임계치]]를 넘으면, APM에서 슬로우 [[191_transaction_concept_states|트랜잭션]] 샘플을 열어 SQL 병목인지 외부 PG 호출인지 곧바로 [[396_validation|확인]]할 수 있어야 한다. 그래야 APM이 "보기 좋은 화면"이 아니라 [[451_mttr|MTTR]] (Mean Time To [[658_ir_recovery|Recovery]])을 줄이는 운영 도구가 된다.

- **📢 섹션 요약 비유**: APM 도입은 CCTV를 많이 다는 일이 아니라, 꼭 필요한 곳에 카메라를 두고 사고가 나면 바로 원인을 찾게 만드는 설계와 같다.

---

## Ⅴ. 기대효과 및 결론

APM을 잘 설계하면 장애 원인 분석 시간이 단축되고, [[282_performance_tactics|성능]] 회귀를 배포 직후 탐지할 수 있으며, 사용자 경험에 직접 영향을 주는 병목을 우선적으로 개선할 수 있다. 이는 단순 운영 편의가 아니라 [[090_service_kubernetes_network_load_balancing|서비스]] [[085_confidence_association_rule_conditional_probability|신뢰도]] 향상과 개발 생산성 개선으로 이어진다. 특히 개발팀과 [[100_sre_site_reliability_engineering_error_budget|SRE]] 팀이 같은 [[191_transaction_concept_states|트랜잭션]] [[001_dikw_pyramid|데이터]]를 보게 되면 "서버 문제냐 코드 문제냐"를 두고 소모적으로 논쟁할 시간도 줄어든다.

반면 비용, 계측 오버헤드, [[051_vendor_lock_in_cloud_computing|벤더 종속]]성은 분명한 제약이다. 또한 [[001_dikw_pyramid|데이터]]가 많다고 통찰이 자동으로 생기지는 않으므로, [[090_service_kubernetes_network_load_balancing|서비스]] 명명 규칙, 태그 [[268_strategy_pattern|전략]], 알람 기준, 대시보드 표준화가 함께 갖춰져야 한다. 결국 APM은 도구 하나가 아니라 운영 체계 일부로 정착해야 효과가 난다.

정리하면 APM은 "애플리케이션을 더 많이 보는 기술"이 아니라 "장애와 [[282_performance_tactics|성능]] 저하를 더 빨리 이해하는 체계"다. 따라서 도입 목적을 [[181_slo_service_level_objective|SLO]], 장애 대응, 최적화 우선순위와 연결해 설계하는 것이 가장 중요하다.

- **📢 섹션 요약 비유**: 좋은 APM은 경기 후 하이라이트 영상이 아니라, 경기 중 작전판처럼 지금 어디를 고쳐야 이길 수 있는지 바로 알려 주는 도구다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 관측성 ([[642_observability_telemetry|Observability]]) | APM은 [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이스 중 애플리케이션 실행 흐름 분석에 강한 축이다. |
| [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]]) | [[090_service_kubernetes_network_load_balancing|서비스]] 간 호출 흐름을 따라가며 APM의 [[191_transaction_concept_states|트랜잭션]] 분석과 결합된다. |
| [[163_rum_real_user_monitoring|RUM]] ([[163_rum_real_user_monitoring|Real User Monitoring]]) | 사용자 체감 [[282_performance_tactics|성능]]과 APM의 서버 내부 병목을 연결해 원인을 분리한다. |
| [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]) | APM 지표를 어떤 수준에서 관리할지 정하는 운영 기준이다. |
| [[190_opentelemetry_cncf_observability_standard|오픈텔레메트리]] ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]]) | 벤더 중립 계측 표준으로 현대 APM 수집 체계의 기반이 된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
인프라 모니터링
    │
    ▼
관측성 (Observability)
    │
    ├─▶ 메트릭 · 로그
    │
    └─▶ 분산 추적 (Distributed Tracing)
             │
             ▼
APM (Application Performance Management)
             │
             ├─▶ RUM (Real User Monitoring)
             ├─▶ Synthetic Monitoring
             └─▶ SLO 기반 성능 운영
```

이 흐름은 운영 관점이 서버 자원 감시에서 출발해, 애플리케이션 내부 분석과 사용자 경험 연계까지 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. APM은 컴퓨터 프로그램 안에서 어디가 느린지 찾아주는 현미경 같은 도구예요.
2. 그냥 "늦었어"라고 말하는 게 아니라, "여기 버튼을 누른 뒤 이 부분에서 오래 걸렸어"라고 정확히 알려줘요.
3. 그래서 고쳐야 할 곳을 빨리 찾을 수 있어서 [[090_service_kubernetes_network_load_balancing|서비스]]가 더 빠르고 튼튼해져요.
