---
title: 160. 헬스 체크/프로브 (Health Check/Probes)
date: '2026-04-21'
tags:
- studynote-devops-sre
---

## 핵심 인사이트

> 1. **본질**: 헬스 체크와 프로브는 애플리케이션이 단순히 실행 중인지가 아니라, 기동이 끝났는지·트래픽을 받을 준비가 됐는지·재시작이 필요한 고장 상태인지를 구분해 판단하는 운영 [[130_signal|신호]]다.
> 2. **가치**: Liveness, Readiness, Startup 프로브를 분리하면 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]])가 잘못된 재시작과 잘못된 트래픽 [[339_routing_overview_best_path_selection|라우팅]]을 줄여, 배포 안정성과 장애 [[658_ir_recovery|복구]] 자동화를 함께 높일 수 있다.
> 3. **판단 포인트**: Liveness는 "살아 있는가", Readiness는 "받을 준비가 됐는가"를 묻는다. 외부 의존성 장애를 Liveness에 넣으면 재시작 폭풍이 나고, Startup을 빼면 느린 기동 애플리케이션이 정상인데도 죽었다고 오판한다.

---

## Ⅰ. 개요 및 필요성

[[561_container_based_deployment|컨테이너]] 환경에서는 프로세스가 떠 있다는 사실만으로 [[090_service_kubernetes_network_load_balancing|서비스]]가 정상이라고 볼 수 없다. 애플리케이션은 이미 실행 중이어도 캐시 워밍, [[002_database_definition|데이터베이스]] 연결, 마이그레이션, 모델 로딩 때문에 아직 요청을 받을 준비가 안 되었을 수 있다. 반대로 [[092_thread_lwp|스레드]] [[281_deadlock_definition|교착 상태]]나 [[142_event_loop|이벤트 루프]] 정지처럼 프로세스는 살아 있지만 실제로는 응답 불능인 경우도 있다. 그래서 오케스트레이터는 단순 PID [[396_validation|확인]]보다 더 정교한 상태 [[130_signal|신호]]가 필요하다.

이때 쓰는 것이 헬스 체크와 프로브다. Startup Probe는 "아직 기동 중이니 기다려도 되는가"를 판별하고, Readiness Probe는 "[[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트에 포함해도 되는가"를 결정하며, Liveness Probe는 "[[233_recovery_database_restoration_overview|회복]]을 위해 재시작해야 하는가"를 판단한다. 세 질문을 분리해야 자동 치유와 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]]가 동시에 가능해진다.

- **📢 섹션 요약 비유**: 병원에서 환자가 숨 쉬는지, 진료를 받을 준비가 됐는지, 수술 직후 [[233_recovery_database_restoration_overview|회복]] 중인지 따로 보는 것과 같다. 모두 건강 관련 질문이지만 의미와 대응 방식은 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[196_kubernetes_k8s_container_orchestration|쿠버네티스]]에서 프로브는 [[561_container_based_deployment|컨테이너]] 생애주기와 [[090_service_kubernetes_network_load_balancing|서비스]] [[339_routing_overview_best_path_selection|라우팅]]을 연결하는 제어 장치다. Startup Probe가 성공하기 전에는 일반적으로 Liveness와 Readiness 판단을 유예해 느린 기동 시간을 [[571_protection_vs_security|보호]]한다. 이후 Readiness가 성공하면 [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트에 등록되고, Liveness가 반복 실패하면 kubelet이 [[561_container_based_deployment|컨테이너]]를 재시작한다. 즉 같은 [[461_http_stateless_connection_oriented|HTTP]] 200 체크처럼 보여도, 뒤에 붙는 운영 동작은 완전히 다르다.

아래 그림은 세 가지 프로브와 그 결과가 어떻게 연결되는지를 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                Probe flow: startup gate, traffic gate, restart gate       │
├────────────────────────────────────────────────────────────────────────────┤
│ Container start                                                            │
│      │                                                                     │
│      ├─ Startup Probe fail ───────────────▶ keep waiting / restart later   │
│      │                                                                     │
│      └─ Startup Probe success                                              │
│               │                                                            │
│               ├─ Readiness success ───────▶ add pod to Service endpoints   │
│               ├─ Readiness fail ─────────▶ remove from traffic only        │
│               │                                                            │
│               ├─ Liveness success ───────▶ keep running                    │
│               └─ Liveness fail N times ─▶ restart container                │
└────────────────────────────────────────────────────────────────────────────┘
```

이 구조에서 중요한 점은 Readiness 실패가 곧바로 재시작을 뜻하지 않는다는 것이다. 준비가 안 된 [[085_pod_kubernetes_container_unit|파드]]는 살아 있을 수 있고, 살아 있는 [[085_pod_kubernetes_container_unit|파드]]가 요청을 받아서는 안 될 수도 있다. 그래서 엔드포인트 제어와 프로세스 [[658_ir_recovery|복구]]를 분리하는 것이 핵심 원리다.

| 프로브 | 질문 | 실패 시 동작 | 포함해야 할 [[130_signal|신호]] |
| :--- | :--- | :--- | :--- |
| Startup Probe | 기동이 끝났는가 | 일정 횟수 초과 시 재시작 | [[459_quic_fec_forward_error_correction|초기]]화 완료 여부, 앱 부팅 완료 |
| Readiness Probe | 지금 트래픽을 받을 수 있는가 | [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트 제외 | 필수 의존성 연결, 워밍 완료 |
| Liveness Probe | 자체 [[658_ir_recovery|복구]] 불가능한 고장 상태인가 | [[561_container_based_deployment|컨테이너]] 재시작 | [[281_deadlock_definition|교착 상태]], [[142_event_loop|이벤트 루프]] 정지, 내부 헬스 |

운영 튜닝에서는 `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`가 중요하다. 예를 들어 기동 시간이 긴 애플리케이션은 Startup Probe의 허용 시간을 충분히 길게 잡아야 하고, Readiness는 배포 중 빠르게 반응하도록 Liveness보다 주기를 짧게 두는 경우가 많다.

- **📢 섹션 요약 비유**: Startup은 "아직 출근 중", Readiness는 "자리에 앉아 일할 준비 완료", Liveness는 "의식이 있는가"를 묻는 [[130_signal|신호]]다. 세 질문을 섞으면 준비 중인 사람을 억지로 집에 돌려보내거나, 아픈 사람에게 일을 시키는 오류가 난다.

---

## Ⅲ. 비교 및 연결

프로브를 이해하려면 로드밸런서 헬스 체크, 얕은 검사 (Shallow Check), 깊은 검사 (Deep Check)와 비교해야 한다. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] Readiness는 [[090_service_kubernetes_network_load_balancing|서비스]] 내부 엔드포인트 편입을 제어하는 [[130_signal|신호]]이고, 외부 로드밸런서 헬스 체크는 더 상위 네트워크 계층에서 인스턴스 [[339_routing_overview_best_path_selection|라우팅]]을 제어한다. 또한 얕은 검사는 프로세스나 단순 [[461_http_stateless_connection_oriented|HTTP]] 응답만 [[396_validation|확인]]하고, 깊은 검사는 [[002_database_definition|데이터베이스]] 질의나 [[389_mesh_topology|메시]]지 큐 연결처럼 실제 의존성 상태까지 본다.

| 비교 항목 | Liveness | Readiness | Startup | 외부 LB 헬스 체크 |
| :--- | :--- | :--- | :--- | :--- |
| 목적 | 자동 재시작 판단 | 트래픽 수신 여부 판단 | 긴 [[459_quic_fec_forward_error_correction|초기]]화 [[571_protection_vs_security|보호]] | 외부 [[339_routing_overview_best_path_selection|라우팅]] 판단 |
| 실패 영향 | [[561_container_based_deployment|컨테이너]] 재시작 | 트래픽 제외 | [[459_quic_fec_forward_error_correction|초기]]화 실패 처리 | 인스턴스 제외 |
| 외부 의존성 포함 | 보통 제외 | 핵심 의존성만 제한적 포함 | [[459_quic_fec_forward_error_correction|초기]]화 과정에 따라 포함 가능 | 제한적 |
| 대표 오용 | DB 장애로 재시작 폭풍 | 모든 옵션 의존성을 포함 | 부재로 인한 오판 | 앱 내부 상태를 너무 단순하게 봄 |

Shallow Check는 가볍고 안정적이지만 실제 장애를 놓칠 수 있고, Deep Check는 정확하지만 [[138_response_time|응답 시간]]과 의존성 부하가 커질 수 있다. 따라서 Liveness는 가볍게, Readiness는 핵심 의존성 중심으로, 외부 [[008_dependencies|종속성]]이 많은 전체 진단은 별도 `/health` 상세 엔드포인트로 분리하는 설계가 일반적이다.

- **📢 섹션 요약 비유**: 학교 출석 체크는 자리에 앉았는지만 보면 되지만, 발표 준비 여부는 자료와 장비까지 봐야 한다. 같은 [[396_validation|확인]]이라도 목적이 다르면 검사 깊이도 달라져야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 프로브 엔드포인트를 애플리케이션의 운영 계약으로 다뤄야 한다. 예를 들어 `/health/live`는 외부 시스템 장애와 무관하게 프로세스가 스스로 [[233_recovery_database_restoration_overview|회복]] 불가능한 상태인지에만 집중해야 한다. 반면 `/health/ready`는 [[002_database_definition|데이터베이스]], 캐시, 필수 [[145_message_broker_sync_async|메시지 브로커]]처럼 요청 처리에 반드시 필요한 의존성만 반영하는 것이 맞다. 결제 API처럼 일시적으로 우회 가능한 외부 [[090_service_kubernetes_network_load_balancing|서비스]]까지 Readiness에 넣으면 전체 트래픽이 불필요하게 차단될 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 느린 부팅 [[090_service_kubernetes_network_load_balancing|서비스]]에 Startup Probe를 별도로 두었는가?
2. Liveness가 외부 의존성 장애 때문에 실패하지 않도록 설계했는가?
3. Readiness 실패 시에도 관측성 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 [[568_logs_distributed_logging_elk_fluentd|로그]]가 남아 원인 분석이 가능한가?
4. [[117_rolling_update_deployment|롤링 업데이트]], [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] ([[095_hpa_horizontal_pod_autoscaler_kubernetes|Horizontal Pod Autoscaler]]), [[302_service_mesh_istio|서비스 메시]]와의 상호작용을 [[395_verification_process_review|검증]]했는가?

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- Liveness와 Readiness를 같은 엔드포인트로 묶어 사용하는 경우
- [[459_quic_fec_forward_error_correction|초기]]화 시간이 긴 JVM, ML 모델 [[090_service_kubernetes_network_load_balancing|서비스]]에 Startup Probe를 두지 않는 경우
- 상세 진단을 프로브에 과도하게 넣어 검사 자체가 병목이 되는 경우

- **📢 섹션 요약 비유**: 건강 검진표를 출입증 검사, 응급실 판단, 입사 대기 [[396_validation|확인]]에 모두 똑같이 쓰면 혼란이 생긴다. 각 문서의 목적이 다르듯 프로브도 질문별로 나눠야 한다.

---

## Ⅴ. 기대효과 및 결론

올바르게 설계된 프로브는 준비되지 않은 [[085_pod_kubernetes_container_unit|파드]]로의 트래픽 유입을 막고, 고장 난 인스턴스를 자동으로 재시작하며, 느린 기동 [[090_service_kubernetes_network_load_balancing|서비스]]도 안정적으로 배포하게 해 준다. 이는 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]], 자동 치유, 운영 단순화에 직접 기여한다. 특히 [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]]) 관점에서는 [[451_mttr|MTTR]] (Mean Time To [[658_ir_recovery|Recovery]], 평균 [[658_ir_recovery|복구]] 시간)을 줄이는 중요한 자동화 장치다.

하지만 프로브가 만능은 아니다. 너무 단순하면 실제 장애를 놓치고, 너무 깊으면 검사 자체가 시스템 부담이 된다. 또한 프로브만으로 근본 원인을 설명할 수는 없으므로 [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스와 함께 관측성 체계 안에서 해석해야 한다. 기억할 핵심은 프로브가 단순한 URL 체크가 아니라, 오케스트레이터에게 "지금 어떤 운영 행동을 해야 하는지" 알려 주는 제어 [[130_signal|신호]]라는 점이다.

- **📢 섹션 요약 비유**: 프로브는 건물의 센서와 같다. 문이 열려야 할지, 잠시 막아야 할지, 비상 정지를 해야 할지를 센서가 구분해 알려 줘야 건물이 안전하게 운영된다.

---

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Startup Probe | 느린 [[459_quic_fec_forward_error_correction|초기]]화를 [[571_protection_vs_security|보호]]해 오판 재시작을 방지 |
| Readiness Probe | [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트 편입 여부를 제어 |
| Liveness Probe | 자동 재시작 [[507_acid_properties|트리거]]를 제공 |
| [[031_load_balancer|Load Balancer]] Health Check | 외부 네트워크 계층의 [[339_routing_overview_best_path_selection|라우팅]] [[130_signal|신호]] |
| [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] | 준비 상태와 [[249_scaling_normalization_standardization|스케일링]] 안정성에 간접 영향 |
| [[642_observability_telemetry|Observability]] | 프로브 실패 원인 분석을 위한 [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·트레이스 기반 |

### 관련 키워드 및 발전 흐름도

```text
프로세스 실행 여부 확인
    │
    ▼
Startup / Readiness / Liveness 분리
    │
    ▼
서비스 엔드포인트 제어 · 자동 재시작
    │
    ▼
롤링 업데이트 · 오토스케일링 안정화
    │
    ▼
관측성 기반 원인 분석 · 자동 치유 고도화
```

이 흐름은 단순 생존 [[396_validation|확인]]이 배포 제어와 자가 [[658_ir_recovery|복구]]로 확장되는 운영 발전 경로를 보여 준다.

### 어린이 비유 설명

1. Startup Probe는 아직 학교에 오는 중이니 조금만 기다려 달라는 [[130_signal|신호]]예요.
2. Readiness Probe는 지금 발표할 준비가 됐는지 [[396_validation|확인]]하는 [[130_signal|신호]]예요.
3. Liveness Probe는 정말 아파서 다시 쉬었다 와야 하는지 [[396_validation|확인]]하는 [[130_signal|신호]]예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 160 / 373

← **이전**: [[159_failover_failback_architecture|159. 페일오버/페일백 아키텍처 (Failover/Failback Architecture)]]
**다음**: [[161_aiops_anomaly_detection_auto_remediation|161. AIOps (Artificial Intelligence for IT Operations)]] →

---
