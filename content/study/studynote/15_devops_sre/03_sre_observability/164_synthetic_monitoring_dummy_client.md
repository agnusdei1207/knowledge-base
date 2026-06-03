---
title: 164. 합성 모니터링 (Synthetic Monitoring)
date: '2026-04-21'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 합성 [[229_monitor|모니터]]링 (Synthetic Monitoring)은 실제 사용자를 기다리지 않고, [[459_dummy_test_double|더미]] 클라이언트가 미리 정의한 시나리오를 주기적으로 실행해 [[090_service_kubernetes_network_load_balancing|서비스]] 상태를 능동적으로 점검하는 방법이다.
> 2. **가치**: 무트래픽 시간대에도 장애를 발견하고, 외부 관점의 [[452_availability|가용성]]·[[015_지연_데이터_관점|지연]]시간·핵심 사용자 여정을 일관된 조건으로 측정할 수 있다.
> 3. **판단 포인트**: 단순 핑보다 중요한 것은 "사용자가 정말 하려는 일"을 얼마나 정확히 재현하느냐이므로, 시나리오 선정과 경보 [[431_ssthresh_slow_start_threshold|임계치]] 설계가 품질을 좌우한다.

---

## Ⅰ. 개요 및 필요성

합성 [[229_monitor|모니터]]링은 스크립트나 에이전트가 가짜 사용자 역할을 하며 [[090_service_kubernetes_network_load_balancing|서비스]]에 주기적으로 요청을 보내는 [[229_monitor|모니터]]링 기법이다. 실제 사용자 기반 [[001_dikw_pyramid|데이터]]에 의존하는 실사용자 [[229_monitor|모니터]]링 ([[163_rum_real_user_monitoring|Real User Monitoring]], [[163_rum_real_user_monitoring|RUM]])과 달리, 트래픽이 없어도 스스로 점검을 수행한다. 따라서 "사용자가 신고하기 전에 먼저 발견한다"는 점에서 사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]과 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약 ([[085_sla|Service Level Agreement]], [[085_sla|SLA]]) 관리에 매우 유용하다.

이 방식이 필요한 이유는 서버 내부 [[342_routing_metric_hop_bandwidth_delay|메트릭]]만으로는 사용자 경험을 완전히 알 수 없기 때문이다. 중앙 처리 장치 (Central Processing Unit, CPU)와 메모리가 정상이어도 [[064_relation_domain|도메인]] 네임 시스템 ([[511_dns_hierarchical_distributed_architecture|Domain Name System]], [[511_dns_hierarchical_distributed_architecture|DNS]]) 오류, 콘텐츠 전송 네트워크 (Content Delivery Network, [[506_cdn_content_delivery_network_edge_caching|CDN]]) 장애, [[303_authentication_authorization_patterns|인증]]서 만료, 특정 지역 [[339_routing_overview_best_path_selection|라우팅]] 문제로 실제 접속이 실패할 수 있다. 합성 [[229_monitor|모니터]]링은 외부 관점에서 [[568_logs_distributed_logging_elk_fluentd|로그]]인, 검색, 결제 같은 흐름을 실행해 이러한 공백을 메운다.

예를 들어 새벽 3시에 결제 응용 프로그래밍 인터페이스 ([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]]) 토큰이 만료되었다고 하자. 내부 애플리케이션은 살아 있어도 실제 주문은 실패한다. 이때 1분마다 [[459_dummy_test_double|더미]] 주문을 시도하는 합성 [[229_monitor|모니터]]링이 있다면, 첫 사용자 불만이 들어오기 전에 운영팀이 이상을 감지하고 대응할 수 있다. 그래서 합성 [[229_monitor|모니터]]링은 단순 업타임 체크보다 한 단계 높은 "[[090_service_kubernetes_network_load_balancing|서비스]] 동작 [[395_verification_process_review|검증]]"으로 봐야 한다.

- **📢 섹션 요약 비유**: 합성 [[229_monitor|모니터]]링은 손님이 오기 전에 직원이 직접 문을 열고 계산도 해 보며 가게가 정말 영업 가능한지 [[396_validation|확인]]하는 점검표와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

합성 [[229_monitor|모니터]]링은 보통 시나리오 정의, [[136_variance|분산]] 실행, [[395_verification_process_review|검증]] 조건, 결과 수집, 경보 발송의 다섯 요소로 구성된다. 시나리오는 단일 하이퍼텍스트 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[461_http_stateless_connection_oriented|Hypertext Transfer Protocol]], [[461_http_stateless_connection_oriented|HTTP]]) 요청일 수도 있고, 브라우저 자동화 기반 다단계 사용자 여정일 수도 있다. 실행 지점은 여러 리전이나 네트워크에서 [[136_variance|분산]] 배치해 지역별 차이를 측정하고, 각 실행 결과는 중앙 대시보드에 집계되어 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표 ([[123_slo_service_level_objective|Service Level Objective]], [[181_slo_service_level_objective|SLO]])와 연결된다.

```text
┌──────────────────────────────────────────────────────────────┐
│               합성 모니터링의 실행 파이프라인               │
├──────────────────────────────────────────────────────────────┤
│ [시나리오 정의]                                              │
│   로그인 → 상품 검색 → 장바구니 → 결제 페이지 확인          │
│          │                                                   │
│          ▼                                                   │
│ [분산 에이전트 실행]  서울 / 도쿄 / 프랑크푸르트 / 버지니아  │
│          │                                                   │
│          ▼                                                   │
│ [검증] 상태 코드, 문서 객체 모델 (Document Object Model, DOM)│
│        요소, 응답 시간, 인증서 만료일                        │
│          │                                                   │
│          ▼                                                   │
│ [결과 집계] 성공률 · 95백분위 (p95) 지연시간 · 실패 단계    │
│          │                                                   │
│          ▼                                                   │
│ [경보] 다중 지역 실패 시 호출 · 온콜 전달                   │
└──────────────────────────────────────────────────────────────┘
```

합성 [[229_monitor|모니터]]링은 목적에 따라 여러 종류로 나뉜다. 단순 [[014_api_posix|API]] [[396_validation|확인]]은 빠르고 유지보수가 쉬우며, 브라우저 시나리오는 실제 사용자 경험을 더 잘 반영한다. 네트워크·[[303_authentication_authorization_patterns|인증]]서·[[511_dns_hierarchical_distributed_architecture|DNS]] 체크는 전송 제어 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]], [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]), 전송 계층 보안 (Transport Layer [[283_security_tactics|Security]], [[694_thread_local_storage_tls|TLS]]), [[511_dns_hierarchical_distributed_architecture|DNS]], 인터넷 제어 [[389_mesh_topology|메시]]지 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[318_icmp_internet_control_message_protocol_diagnostics|Internet Control Message Protocol]], [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]]) 수준의 외부 경로 문제를 조기에 잡는 데 유용하다. 중요한 것은 모든 시나리오를 같은 수준으로 다루지 않고, [[090_service_kubernetes_network_load_balancing|서비스]] 영향도에 따라 계층화하는 것이다.

| 유형 | [[395_verification_process_review|검증]] 대상 | 장점 | 주의점 |
| :--- | :--- | :--- | :--- |
| [[461_http_stateless_connection_oriented|HTTP]]/[[014_api_posix|API]] 체크 | 상태 코드, 응답 본문, [[015_지연_데이터_관점|지연]]시간 | 빠르고 저렴함 | 사용자 인터페이스 (User Interface, UI) 장애는 놓칠 수 있음 |
| 브라우저 시나리오 | [[568_logs_distributed_logging_elk_fluentd|로그]]인, 검색, 결제 같은 여정 | 실제 경험에 가까움 | 스크립트 유지비 높음 |
| 네트워크 체크 | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]], [[694_thread_local_storage_tls|TLS]], [[511_dns_hierarchical_distributed_architecture|DNS]], [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] | 외부 연결 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] | 비즈니스 기능 [[395_verification_process_review|검증]]은 약함 |
| [[303_authentication_authorization_patterns|인증]]서 체크 | 만료일, 체인 이상 | 예방 효과 큼 | 단독으로는 사용자 가치 부족 |

실무에서는 합성 [[229_monitor|모니터]]링을 블랙박스 검사로 본다. 시스템 내부 구조를 몰라도 외부에서 정해진 입력을 넣고 기대 결과를 [[395_verification_process_review|검증]]할 수 있기 때문이다. 예를 들어 [[138_response_time|응답 시간]]이 300밀리초에서 2초로 늘거나, 결제 버튼 클릭 후 특정 문구가 나타나지 않으면 즉시 실패로 판단한다. 이렇게 외부 체감 품질을 수치화해야 내부 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 사용자 경험 사이의 간극을 줄일 수 있다.

- **📢 섹션 요약 비유**: 합성 [[229_monitor|모니터]]링은 엘리베이터 안을 뜯어보는 것이 아니라, 버튼을 눌렀을 때 문이 열리고 원하는 층에 제대로 도착하는지 반복해서 시험하는 검사와 같다.

---

## Ⅲ. 비교 및 연결

합성 [[229_monitor|모니터]]링은 실사용자 [[229_monitor|모니터]]링과 대체 [[083_relationship_in_er_model|관계]]가 아니라 상호 보완 [[083_relationship_in_er_model|관계]]다. 합성 [[229_monitor|모니터]]링은 동일 조건에서 반복 측정하므로 비교 가능성이 높고, RUM은 실제 기기·브라우저·네트워크 조건을 반영하므로 현실성이 높다. 전자는 "문제가 생기기 전에 찾는 감시자"이고, 후자는 "실제 사용자가 어떻게 느끼는지 보여 주는 관찰자"다.

| 항목 | 합성 [[229_monitor|모니터]]링 | [[163_rum_real_user_monitoring|RUM]] ([[163_rum_real_user_monitoring|Real User Monitoring]]) |
| :--- | :--- | :--- |
| 실행 주체 | [[459_dummy_test_double|더미]] 클라이언트 | 실제 사용자 |
| 무트래픽 탐지 | 가능 | 불가 |
| 측정 [[194_consistency_database_integrity|일관성]] | 높음 | 낮음 |
| 현실 반영성 | 제한적 | 높음 |
| 사전 경보 | 강함 | 약함 |

또한 합성 [[229_monitor|모니터]]링은 배포 [[268_strategy_pattern|전략]]과도 깊게 연결된다. [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[115_canary_deployment_gradual_rollout|Canary Deployment]]) 직후 새 [[288_version_ihl_tos_total_length|버전]]에만 [[459_dummy_test_double|더미]] 시나리오를 먼저 태워 보면, 사용자 전체 오픈 전에 핵심 여정 실패를 잡을 수 있다. [[302_service_mesh_istio|서비스 메시]]나 응용 프로그래밍 인터페이스 ([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]]) 게이트웨이 같은 네트워크 계층과 결합하면 리전별, [[288_version_ihl_tos_total_length|버전]]별, [[339_routing_overview_best_path_selection|라우팅]] 경로별 품질 차이도 비교할 수 있다.

관측성 ([[642_observability_telemetry|Observability]]) 관점에서는 [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스가 "왜 실패했는가"를 설명하고, 합성 [[229_monitor|모니터]]링이 "실제로 실패했는가"를 먼저 알려 준다. 즉 합성 [[229_monitor|모니터]]링은 증상 감지, 나머지 도구는 원인 분석에 강하다. 이 역할 분담을 이해해야 [[229_monitor|모니터]]링 예산과 도구 구성을 균형 있게 가져갈 수 있다.

- **📢 섹션 요약 비유**: 합성 [[229_monitor|모니터]]링은 정기 건강검진이고, RUM은 실제 생활 속 컨디션 기록이다. 검진만으로는 평소 습관을 다 알 수 없고, 생활 기록만으로는 숨어 있는 문제를 놓칠 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 중요한 것은 시나리오 선택이다. 단순히 홈 화면이 200 응답을 준다고 [[090_service_kubernetes_network_load_balancing|서비스]]가 정상인 것은 아니다. 전자상거래라면 [[568_logs_distributed_logging_elk_fluentd|로그]]인, 상품 조회, 장바구니, 결제 성공까지가 핵심이고, 금융 [[090_service_kubernetes_network_load_balancing|서비스]]라면 [[303_authentication_authorization_patterns|인증]]서 [[568_logs_distributed_logging_elk_fluentd|로그]]인, 계좌 조회, 이체 직전 [[395_verification_process_review|검증]]이 더 중요할 수 있다. 즉 합성 [[229_monitor|모니터]]링은 "가장 중요한 사용자 여정"부터 설계해야 한다.

[[459_dummy_test_double|더미]] 계정과 [[444_test_data_management|테스트 데이터]] 관리도 필수다. 브라우저 시나리오가 실제 주문을 만들어 버리면 운영 [[001_dikw_pyramid|데이터]] 오염과 비용 문제가 생긴다. 그래서 테스트 전용 계정, 결제 샌드박스, 주문 자동 정리 배치, 캡차 우회 [[164_policy|정책]] 같은 운영 장치를 함께 마련해야 한다. 경보 조건 역시 1회 실패 즉시 울리는 방식보다 3개 리전 중 2개 이상 연속 실패, 5분 이상 지속 같은 다단계 기준이 실무적이다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. **핵심 여정 우선순위가 명확한가**: [[568_logs_distributed_logging_elk_fluentd|로그]]인보다 결제가 더 중요할 수 있다.
2. **시나리오 유지비를 감당할 수 있는가**: 자주 바뀌는 화면은 브라우저 테스트를 최소화한다.
3. **다중 지역 [[395_verification_process_review|검증]]이 필요한가**: 글로벌 [[090_service_kubernetes_network_load_balancing|서비스]]라면 리전 [[136_variance|분산]]은 필수다.
4. **온콜 [[164_policy|정책]]과 연결되어 있는가**: 실패를 감지해도 대응 체계가 없으면 의미가 없다.
5. **배포 게이트로 활용하는가**: [[595_canary_stack_smashing_protector|카나리]] 단계에서 자동 합격·실패 판단 기준을 둘 수 있다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 [[286_page_frame|페이지]]를 브라우저 시나리오로 만들고 유지보수 비용을 폭증시키는 경우
- 단일 리전 실패만으로 과도한 경보를 발생시켜 노이즈를 만드는 경우
- 성공률만 보고 어느 단계에서 실패했는지 추적 정보를 남기지 않는 경우

예를 들어 [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]]) 팀이 체크아웃 경로를 1분마다 실행하고, p95 [[015_지연_데이터_관점|지연]]시간이 2초를 넘거나 결제 승인 단계가 두 번 연속 실패하면 자동으로 배포를 중단하도록 연결할 수 있다. 이처럼 합성 [[229_monitor|모니터]]링은 단순 경보 도구가 아니라 배포 안전장치와 [[090_service_kubernetes_network_load_balancing|서비스]] 품질 게이트로도 활용된다.

- **📢 섹션 요약 비유**: 합성 [[229_monitor|모니터]]링은 공연 시작 전 리허설과 같다. 마이크, 조명, 음향이 모두 맞는지 미리 [[396_validation|확인]]해야 관객이 들어왔을 때 사고가 나지 않는다.

---

## Ⅴ. 기대효과 및 결론

합성 [[229_monitor|모니터]]링의 가장 큰 효과는 장애를 사용자 체감 관점에서 먼저 발견한다는 점이다. 내부 서버가 살아 있다는 사실보다, 고객이 핵심 작업을 실제로 끝낼 수 있는지가 더 중요하기 때문이다. 또한 일정한 조건으로 반복 측정하므로 릴리스 전후 [[282_performance_tactics|성능]] 비교, 지역별 품질 [[107_gap_analysis_task_identification|차이 분석]], 외부 벤더 장애 감지에도 유리하다.

한계도 분명하다. 실제 사용자의 다양한 브라우저, 네트워크, 행동 변형을 모두 재현할 수는 없고, 브라우저 시나리오는 화면 구조가 바뀔 때마다 깨질 수 있다. 따라서 합성 [[229_monitor|모니터]]링만으로 전체 사용자 경험을 대변하려 해서는 안 되며, [[163_rum_real_user_monitoring|RUM]], [[568_logs_distributed_logging_elk_fluentd|로그]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]과 함께 사용해야 한다.

결론적으로 합성 [[229_monitor|모니터]]링은 "[[090_service_kubernetes_network_load_balancing|서비스]]가 살아 있는가"를 넘어서 "핵심 사용자 여정이 지금도 완주 가능한가"를 묻는 도구다. [[459_dummy_test_double|더미]] 클라이언트는 가짜 사용자이지만, 그 결과는 실제 비즈니스 품질을 지키는 가장 현실적인 조기 경보가 된다.

- **📢 섹션 요약 비유**: 합성 [[229_monitor|모니터]]링은 무대 뒤에서 미리 뛰어보는 대역 배우와 같다. 관객이 오기 전에 어디서 넘어질지 알아내면, 본 공연을 훨씬 안전하게 지킬 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[163_rum_real_user_monitoring|RUM]] ([[163_rum_real_user_monitoring|Real User Monitoring]]) | 실제 사용자 기반 [[282_performance_tactics|성능]]과 오류를 측정하는 상보적 기법 |
| [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]) | 합성 [[229_monitor|모니터]]링 결과를 목표치와 연결하는 운영 기준 |
| 블랙박스 [[229_monitor|모니터]]링 (Black-Box Monitoring) | 외부 관점에서 [[090_service_kubernetes_network_load_balancing|서비스]] 동작을 [[395_verification_process_review|검증]]하는 접근 |
| [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[115_canary_deployment_gradual_rollout|Canary Deployment]]) | 새 [[288_version_ihl_tos_total_length|버전]]을 제한 노출 후 합성 시나리오로 [[395_verification_process_review|검증]] |
| 블랙박스 익스포터 (Blackbox Exporter) | [[461_http_stateless_connection_oriented|HTTP]], [[511_dns_hierarchical_distributed_architecture|DNS]], [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 등을 외부에서 점검하는 대표 도구 |
| 온콜 (On-[[189_subroutine_call_return|call]]) | 합성 경보를 실제 대응 체계로 연결하는 운영 프로세스 |

### 📈 관련 키워드 및 발전 흐름도

```text
업타임 체크 · 핑 모니터링
    │
    ▼
HTTP/API 합성 점검
    │
    ▼
브라우저 기반 사용자 여정 검증
    │
    ▼
다중 지역 외부 가용성 측정
    │
    ▼
SLO 연계 경보 · 카나리 배포 게이트
    │
    ▼
RUM · 트레이스와 결합한 종합 관측성
```

이 흐름은 단순 생존 [[396_validation|확인]]에서 시작해, 실제 사용자 여정과 운영 의사결정까지 연결되는 합성 [[229_monitor|모니터]]링의 성숙 단계를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 합성 [[229_monitor|모니터]]링은 로봇 손님이 가게에 들어와 주문부터 계산까지 해 보는 연습이에요.
2. 진짜 손님이 없을 때도 로봇 손님이 계속 [[396_validation|확인]]해서 문제를 빨리 알려줘요.
3. 그래서 가게 주인은 손님이 오기 전에 고장 난 곳을 먼저 고칠 수 있어요.
