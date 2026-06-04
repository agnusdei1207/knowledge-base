+++
title = "358. 서드파티 API 통신 폴백 지터 백오프 설계 (Third-party API Fallback Jitter and Exponential Backoff Design)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서드파티](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 통신에서 지수 백오프 + 지터 (Jitter) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 재시도 폭풍(Thundering Herd)을 방지하면서 일시적 장애를 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 내결함성 통신 설계 패턴이다.
> 2. **가치**: [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)) 패턴과 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) ([Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 결합하면, 의존 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 시 자신의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 저하를 최소화하고 의존 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) 속도를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)할 수 있다.
> 3. **판단 포인트**: 재시도 예산(Retry Budget), [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 계층(연결/읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)), [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 상태 천이(Closed->Open->Half-Open) 설계가 실무 판단의 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 [서드파티](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)(결제, 지도, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론 등)는 외부 의존성의 전형이다. 이 의존성이 장애를 겪을 때 단순 재시도(Naive Retry)를 쓰면 장애 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 재시도 요청이 폭증해 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 더 어렵게 만드는 재시도 폭풍(Thundering Herd)이 발생한다.

2012년 AWS [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 재시도 폭풍으로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된 사례, Netflix가 [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 없이 Hystrix 이전 단계에서 겪은 연쇄 장애(Cascading Failure) 사례가 이 문제의 실증이다. 단순 재시도는 해결책이 아니라 장애를 증폭시킨다.

지수 백오프(Exponential Backoff)는 재시도 간격을 2^n 형태로 늘려 부하를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)한다. 그러나 여러 클라이언트가 동시에 같은 간격으로 재시도하면 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)된 부하 폭발이 발생한다. 지터(Jitter)는 재시도 간격에 무작위 값을 더해 이 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)를 깨뜨린다. Full Jitter [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 `sleep = random(0, min(cap, base * 2^attempt))`로 계산된다.

- 📢 섹션 요약 비유: 재시도 폭풍은 정전 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 에어컨이 동시에 켜지는 것과 같다. 지터는 에어컨이 무작위 간격으로 켜지게 해 전력망을 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+-------------------------------------------------------------------+
|               서킷 브레이커 상태 천이                             |
+-------------------------------------------------------------------+
|  [Closed] --실패율 임계 초과---> [Open] --대기시간 후---> [Half-Open]|
|     ^                              |                     |        |
|     |         즉시 폴백 응답       |  테스트 요청 성공 -> |        |
|     +------------------------------+       Closed 복귀   |        |
|                                            실패 -> Open   |        |
+-------------------------------------------------------------------+
```

| 상태       | 동작                                | 전환 조건                             |
| :--------- | :---------------------------------- | :------------------------------------ |
| Closed     | 정상 통신, 실패율 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링           | 실패율 > 임계값 (예: 50%, 10초)       |
| Open       | 즉시 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 반환, 외부 호출 없음       | 대기 시간 경과 (예: 30초)             |
| Half-Open  | 제한적 테스트 요청 허용              | 성공 -> Closed, 실패 -> Open           |

**지수 백오프 + 지터 비교**

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)             | 재시도 간격 계산                              | 특징                     |
| :--------------- | :-------------------------------------------- | :----------------------- |
| No Jitter        | `min(cap, base * 2^n)`                        | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 부하 폭발 위험    |
| Full Jitter      | `random(0, min(cap, base * 2^n))`             | 최대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), 권장           |
| Decorrelated     | `random(base, prev_sleep * 3)`                | 이전 간격 기반, 균일 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)|

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/">폴백</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 유형</strong>: 캐시 응답(Stale-While-Revalidate), 기본값 반환([Stub](/knowledge-base/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) Response), 기능 축소 모드(Degraded Mode), 큐 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 처리([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)-and-Retry). 결제처럼 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)이 없는 API는 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 대신 큐 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 처리가 안전하다.

- 📢 섹션 요약 비유: [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)는 집의 두꺼비집과 같다. 과전류 시 차단기가 내려가 전기 시스템([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 전체를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하고, 문제가 해결된 후 조심스럽게(Half-Open) 다시 올린다.

---

## Ⅲ. 비교 및 연결

| 항목               | 단순 재시도                     | 지수 백오프 + 지터              | [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)                   |
| :----------------- | :------------------------------ | :------------------------------ | :------------------------------ |
| 목적               | 일시적 오류 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)                 | 재시도 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)                 | 연쇄 장애 차단                  |
| 외부 영향          | 장애 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 부하 증폭            | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 증가, 부하 감소             | 요청 차단으로 완전 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)          |
| 구현 복잡도        | 낮음                             | 중간                             | 높음 (상태 관리 필요)            |
| 병용 가능 여부     | -                                | [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)와 함께 사용        | 백오프와 함께 사용               |

[벌크헤드](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/) ([Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/)) 패턴은 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 격리를 통해 특정 의존성 장애가 전체 시스템으로 전파되지 않도록 막는다. [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 계층은 연결 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) handshake, <1초), 읽기 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)(응답 수신, <5초), [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)(요청 전송)을 별도 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)한다.

- 📢 섹션 요약 비유: 지수 백오프는 문을 두드릴 때 점점 더 오래 기다리는 것이고, [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)는 아예 노크를 멈추고 집 앞을 떠나는 결정이다. 둘 다 없으면 문이 부서질 때까지 두드린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>재시도 설계 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
1. [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/): 멱등하지 않은 API는 재시도 전 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 발급 필요
2. 재시도 예산(Retry Budget): 전체 요청의 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 이하로 재시도 총량 제한
3. [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 계층 분리: 연결/읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 각각 독립 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)
4. [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 응답 신선도: 캐시 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)의 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) ([Time To Live](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/))과 스테일(Stale) 허용 범위 정의
5. [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 임계값: 실패율(%), 슬라이딩 윈도우(초), Half-Open 테스트 요청 수 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)

**판단 기준**
- 결제, 주문 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (비멱등): 재시도 없이 큐 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 처리 + [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) = "나중에 처리"
- 조회 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (멱등): Full Jitter 백오프 + [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) + 캐시 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (고지연): [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 공격적 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) + [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) Open 시 기본 모델 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
- 재시도 횟수만 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하고 간격 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 없음 -> Thundering Herd 재발
- [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 없이 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)만 구현 -> 장애 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계속 호출로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)
- 연결 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)과 읽기 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 동일하게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) -> 느린 응답과 연결 실패 구분 불가

- 📢 섹션 요약 비유: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 재시도 설계는 소방 훈련과 같다. 화재(장애) 시 모든 사람이 동시에 계단을 달리면 혼잡해지므로, 층별로 순서를 나눠(지터) 안전하게 대피한다.

---

## Ⅴ. 기대효과 및 결론

지수 백오프 + 지터 + [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 조합은 일시적 장애에 대한 자동 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)력과 연쇄 장애 방어를 동시에 달성한다. Netflix Hystrix, Resilience4j, AWS SDK의 기본 재시도 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 모두 Full Jitter를 적용하며, 이를 통해 [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 수십 분에서 수 분으로 단축한 사례가 있다.

한계로는 [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 임계값 튜닝이 잘못되면 정상 트래픽에서 Open 상태로 전환되는 오탐(False Positive)이 발생한다. 또한 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 응답이 잘못 설계되면 "가짜 성공"처럼 보이는 불완전한 응답이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치를 유발한다.

미래 방향은 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), Envoy)가 이 모든 패턴을 애플리케이션 코드 외부에서 자동 처리하는 방향이다. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 수준에서 재시도·[서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)·[타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 선언적으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해, 애플리케이션은 비즈니스 로직에만 집중한다.

- 📢 섹션 요약 비유: [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)와 백오프는 방어 운전의 두 기술이다. 백오프는 앞차와의 거리를 늘리는 것이고, [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)는 사고 구간에서 우회로를 찾는 결정이다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/))          | 연쇄 장애 차단, Closed/Open/Half-Open 상태 관리           |
| [Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/) ([벌크헤드](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/))                     | [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 격리로 장애 전파 차단                           |
| Retry Budget (재시도 예산)              | 전체 트래픽 대비 재시도 비율 상한 제어                    |
| Hystrix / Resilience4j                  | JVM 기반 [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)·[벌크헤드](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)               |
| [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)/Envoy)               | 인프라 수준 재시도·[서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 자동화                   |
| [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/))           | 재시도 예산이 [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 달성과 직결되는 연결 고리               |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 재시도 (Naive Retry) — 장애 증폭 위험
    |
    v
지수 백오프 (Exponential Backoff) — 부하 분산
    |
    v
지터 (Full Jitter) — Thundering Herd 제거
    |
    v
서킷 브레이커 (Circuit Breaker) — 연쇄 장애 차단
    |
    v
폴백 (Fallback) + 벌크헤드 (Bulkhead) — 그레이스풀 디그레이드
    |
    v
서비스 메시 (Istio/Envoy) — 인프라 레벨 자동화
```

흐름은 "재시도 증폭 -> [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 제어 -> 차단 -> 격리 -> 인프라 자동화"로 진화한다.

### 👶 어린이를 위한 3줄 비유 설명

1. API가 응답을 안 할 때 계속 두드리면 서버가 더 힘들어져요. 그래서 기다리는 시간을 점점 늘려요(지수 백오프).
2. 지터는 여러 친구가 동시에 문을 두드리지 않도록 각자 다른 시간에 두드리게 하는 거예요.
3. [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)는 "이 문은 고장났어"라고 판단하면 아예 두드리지 않고 다른 길을 찾는 현명한 결정이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 358 / 373

<- **이전**: [357. OOM Killed 커널 자원 제한 종료 방어망 (OOM Killer Kubernetes QoS cgroup Memory Limits)](/knowledge-base/studynote/15_devops_sre/05_devsecops/357_oom_killed/)
**다음**: [359. 시맨틱 캐시 RAG 비용 응답 단축 계층 (Semantic Cache for RAG Cost and Latency Reduction)](/knowledge-base/studynote/15_devops_sre/05_devsecops/359_metric/) ->

---
