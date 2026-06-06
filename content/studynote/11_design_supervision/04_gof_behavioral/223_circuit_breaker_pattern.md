---
title: "Circuit Breaker Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) ([서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)) 패턴은 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)(Microservice) 환경에서 하나의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애가 전체 시스템으로 전파되는 연쇄 장애(Cascading Failure)를 차단하기 위해, 전기 차단기처럼 장애 감지 시 호출을 즉시 차단하고 자가 치유(Self-Healing)를 시도하는 패턴이다.
> 2. **가치**: [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)까지 기다리며 [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 소모하는 대신 즉시 [Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) ([폴백](/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)) 응답을 반환하여, 장애 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 격리하고 호출자를 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)한다.
> 3. **판단 포인트**: 세 가지 상태(Closed -> Open -> Half-Open)의 전이 조건인 **실패율 임계값(Failure Rate Threshold)** 과 **대기 시간(Wait Duration)** 이 핵심 튜닝 파라미터다.

---

## Ⅰ. 개요 및 필요성
```
마이크로서비스 의존 관계:
  서비스 A -> 서비스 B -> 서비스 C (장애 발생!)

장애 전파:
  1. 서비스 C 응답 지연 (10초 타임아웃)
  2. 서비스 B의 스레드가 C를 기다리며 블록
  3. 서비스 A의 요청이 밀리며 B의 스레드 풀 고갈
  4. 서비스 A 전체 응답 불가 -> 서비스 A도 장애
  5. 도미노처럼 전체 시스템 다운
```

[Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) 없는 시스템의 치명적 문제:
- 장애 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 호출하며 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 자원을 낭비
- 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 업스트림으로 전파
- 단일 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 -> 전체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 다운

전기 차단기([Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/))에서 이름을 가져왔다:
- 정상: [전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/)(요청)가 흐름 (Closed)
- 과부하: 차단기 작동, 회로 차단 (Open)
- [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 테스트: 소량 [전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) 허용 (Half-Open)

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: Circuit Breaker는 집의 전기 차단기 — 과전류(장애)가 발생하면 즉시 회로를 차단(Open)해서 집 전체가 불타는 것을 막고, 안전해지면 다시 연결(Half-Open -> Closed)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+--------------------------------------------------------------+
|           Circuit Breaker State Machine                      |
|                                                              |
|  +-----------+                         +---------------+     |
|  |  CLOSED   |  실패율 > 임계값(50%)    |     OPEN      |     |
|  | (정상 운영)|------------------------->|  (호출 차단)   |     |
|  |           |  (예: 10번 중 5번 실패)  |               |     |
|  +-----+-----+                         +------+--------+     |
|        |                                      |              |
|        | 성공률 > 임계값(90%)                   | 대기시간 경과  |
|        | 충분한 시도 횟수                       | (예: 60초)    |
|        |                                      v              |
|        |                              +---------------+      |
|        +------------------------------|  HALF-OPEN    |      |
|                                       | (탐색/테스트)  |      |
|                                       |               |      |
|                                       | 실패 시 -> OPEN |      |
|                                       +---------------+      |
+--------------------------------------------------------------+
```

| 파라미터 | 설명 | 기본값 |
|:---|:---|:---|
| `failureRateThreshold` | Open 전환 실패율(%) | 50 |
| `slowCallRateThreshold` | 슬로우콜 비율(%) | 100 |
| `slowCallDurationThreshold` | 슬로우콜 기준 시간 | 60s |
| `slidingWindowSize` | 통계 계산 [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/) | 100 |
| `waitDurationInOpenState` | Open 상태 유지 시간 | 60s |
| `permittedNumberOfCallsInHalfOpenState` | Half-Open에서 테스트 호출 수 | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) |
| `minimumNumberOfCalls` | 통계 계산 최소 호출 수 | 100 |

```java
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .waitDurationInOpenState(Duration.ofSeconds(60))
    .permittedNumberOfCallsInHalfOpenState(10)
    .slidingWindowSize(100)
    .build();

CircuitBreaker cb = CircuitBreakerRegistry.of(config)
    .circuitBreaker("paymentService");

// 보호된 호출 + 폴백
String result = cb.executeWithFallback(
    () -> paymentService.charge(amount),     // 원본 호출
    ex -> "캐시된 응답 또는 기본값 반환"       // Fallback
);
```

- **📢 섹션 요약 비유**: Half-Open은 응급실 의사가 퇴원 전 환자에게 "조금 걸어봐, 괜찮으면 퇴원" — 몇 가지 테스트 호출(소량 시도)로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [회복](/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)됐는지 확인한다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 목적 | 적합한 실패 유형 |
|:---|:---|:---|
| [Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) | 장애 전파 차단, 자가 치유 | 지속적 장애 ([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 다운) |
| Retry (재시도) | 일시적 실패 극복 | 순간적 네트워크 오류 |
| [Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) ([타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)) | 무한 대기 방지 | 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| [Bulkhead](/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/) (격벽) | 자원 격리 | 특정 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 과부하 |
| Rate Limiter | 호출 빈도 제한 | 요청 과다 |

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 | 사용 시점 |
|:---|:---|:---|
| 캐시 응답 반환 | 최근 성공 결과 반환 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 중요도 낮을 때 |
| 기본값 반환 | 하드코딩된 안전한 값 | 부분 기능 제공 허용 시 |
| 대체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출 | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 구성 시 |
| 에러 응답 즉시 반환 | 빠른 실패(Fail Fast) | 클라이언트가 처리 가능할 때 |

| 비교 항목 | Netflix Hystrix | Resilience4j |
|:---|:---|:---|
| 상태 | 유지보수 중단 (2018) | 현재 표준 (활발히 개발) |
| [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 격리 | [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) 기본 | [Semaphore](/studynote/02_operating_system/04_synchronization/224_semaphore/)/[Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 선택 |
| 의존성 | 무거움 (RxJava 등) | 경량 ([FP](/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 기반) |
| Spring Boot 통합 | Spring Cloud Netflix | Spring Cloud [Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) |

- **📢 섹션 요약 비유**: Fallback은 비행기의 비상 착륙 절차 — 엔진(외부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에 문제가 생겨도 비상 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)([Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/))로 승객을 안전하게 착륙([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 유지)시킨다.

---

## Ⅳ. 실무 적용 및 기술사 판단
```yaml
# application.yml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        failure-rate-threshold: 50
        slow-call-rate-threshold: 100
        slow-call-duration-threshold: 2000ms
        wait-duration-in-open-state: 60s
        permitted-number-of-calls-in-half-open-state: 10
        sliding-window-type: COUNT_BASED
        sliding-window-size: 20
        minimum-number-of-calls: 5
```

```java
@Service
public class OrderService {
    @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
    public PaymentResult pay(Order order) {
        return paymentClient.charge(order);
    }

    private PaymentResult paymentFallback(Order order, Exception ex) {
        log.warn("결제 서비스 장애, 폴백 실행: {}", ex.getMessage());
        return PaymentResult.pending(order.getId()); // 보류 처리
    }
}
```

| 지표 | 설명 | 임계 경보 |
|:---|:---|:---|
| 실패율 (Failure Rate) | 최근 N번 중 실패 비율 | 30% 경고, 50% 차단 |
| 슬로우콜 비율 | 기준 시간 초과 비율 | 20% 경고 |
| 호출 차단 수 | Open 상태에서 거부된 요청 수 | 급증 시 즉시 알람 |
| [상태 전이](/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 횟수 | OPEN/HALF-OPEN 전환 빈도 | 반복 전환 -> 근본 원인 조사 |

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 해결하려는 변화 축이 분명한가?
2. [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용보다 변경 절감 효과가 큰가?
3. 테스트·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: [Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) 모니터링은 심전도 — 맥박(요청 성공률)이 정상(Closed), 불규칙([임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 초과), 심정지(Open), [회복](/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) 중(Half-Open) 상태를 실시간으로 보여준다.

---

## Ⅴ. 기대효과 및 결론
[Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) 패턴은 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 아키텍처의 핵심 복원력(Resilience) 패턴이다:

**기대효과**:
- **연쇄 장애 방지**: 하나의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애가 전체로 퍼지지 않음
- **빠른 실패(Fail Fast)**: [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 대기 없이 즉시 [폴백](/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 반환
- **자가 치유**: Half-Open 상태에서 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시도
- <strong>자원 <a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong>: [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/) 고갈 방지

**설계 원칙**:
- Circuit Breaker는 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 경계</strong>마다 설치 (각 외부 의존성마다 별도 인스턴스)
- Fallback은 **항상 정의** — "차단됐을 때 무엇을 할 것인가" 가 설계의 핵심
- 임계값은 <strong>실제 트래픽 패턴</strong>을 기반으로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (기본값 그대로 사용 금지)

기술사 시험에서는 **3가지 상태(Closed/Open/Half-Open) 전이 조건**, <strong><a href="/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/">Fallback</a> <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 종류</strong>, <strong>Retry와의 차이점</strong>을 명확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) 내장, ③ [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Circuit Breaker는 보험 + 안전망의 결합 — 사고(장애)가 나면 보험([Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/))이 즉시 처리하고, 안전망(Half-Open)이 상황이 안정됐는지 확인한 뒤 다시 정상 운영(Closed)으로 복귀한다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 복원력 ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) Resilience) | Circuit Breaker가 제공하는 핵심 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |
| 연관 패턴 | Retry Pattern | 일시적 실패를 위한 재시도 (Circuit Breaker와 조합) |
| 연관 패턴 | [Bulkhead Pattern](/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/) | [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/)/세마포어로 자원 격리 |
| 연관 패턴 | [Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) Pattern | 무한 대기 방지 ([Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)) |
| 구현체 | Resilience4j | 현재 표준 Java [Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) |
| 연관 개념 | [Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) ([폴백](/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)) | Open 상태에서 호출 시 대안 응답 |
| 연관 개념 | Exponential Backoff | Retry와 함께 사용하는 지수 백오프 |

### 📈 관련 키워드 및 발전 흐름도
[timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)·retry -> [서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 패턴 -> resilience [orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)

### 👶 어린이를 위한 3줄 비유 설명
1. Circuit Breaker는 집 전기 차단기 — 너무 많은 전기(장애 요청)가 흐르면 차단기가 내려가서(Open) 집 전체가 불타는 것을 막아줘.
2. 60초 후에 "이제 괜찮나?" 하고 조금씩 [전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/)를 흘려보고(Half-Open) 안전하면 다시 정상 운전(Closed), 아직도 문제면 다시 차단(Open)해.
3. 차단 중에도 집에 불(사용자 요청)이 들어오면 "지금 정전 중이에요, 대신 손전등([Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)) 쓰세요"라고 알려줘서 완전히 멈추지 않도록 해.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 284 / 530

<- **이전**: [222. 모킹과 단위 테스트 (Mocking / Unit Test / Test Double)](/studynote/11_design_supervision/04_gof_behavioral/222_mocking_unit_test_stub/)
**다음**: [224. 지수 백오프 재시도 패턴 (Exponential Backoff and Retry Pattern)](/studynote/11_design_supervision/04_gof_behavioral/224_exponential_backoff_retry/) ->

---
