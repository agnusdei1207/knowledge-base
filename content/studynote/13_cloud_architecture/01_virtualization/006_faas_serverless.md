---
title: 6. FaaS (Function as a Service / Serverless) - 인프라 관리 없이 함수 코드 조각 단위로 배포/실행
  (AWS Lambda)
date: '2024-05-24'
description: 인프라 프로비저닝 없이 코드 조각 단위로 실행되는 FaaS의 근본 원리, 아키텍처, 그리고 콜드 스타트 최적화 전략
tags:
- cloud_architecture
---

# 6. [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) 및 [[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서버 인프라의 존재를 완벽히 추상화하고, 개발자가 작성한 비즈니스 로직(함수)을 이벤트 기반으로 실행하며 밀리초(ms) 단위로 자원을 동적 할당하는 [[052_cloud_computing_os|클라우드 컴퓨팅]] 모델.
> 2. **가치**: 유휴 자원 낭비 제로(Scale-to-[[585_zero_skipping|Zero]])와 무한한 자동 확장성([[030_auto_scaling|Auto Scaling]])을 제공하여, 예측 불가능한 트래픽 [[129_spike_agile_technical_investigation|스파이크]] 대응과 [[016_tco|TCO]](총소유비용) 절감에 극적인 효과를 발휘.
> 3. **융합**: [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]])의 극한 형태로, [[542_api_gateway|API Gateway]], [[035_nosql|NoSQL]], 비동기 메시지 큐 등 [[531_cloud_native_architecture|클라우드 네이티브]] 생태계와의 결합을 통해 진정한 [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]]([[064_eda|EDA]])를 완성.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

**[[206_serverless_cold_start|서버리스]]([[206_serverless_cold_start|Serverless]])와 FaaS의 도래**
[[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])는 [[052_cloud_computing_os|클라우드 컴퓨팅]]의 진화 과정에서 IaaS와 PaaS가 가진 물리적/논리적 인프라 관리의 부담을 최종적으로 제거한 패러다임이다. 전통적인 서버 기반 아키텍처에서는 트래픽 피크를 대비해 항상 자원을 '과잉 [[528_provisioning|프로비저닝]](Over-provisioning)'해야만 했으며, 이는 평상시 막대한 유휴 자원 낭비로 이어졌다. [[206_serverless_cold_start|서버리스]]는 "서버가 없다"는 뜻이 아니라, "사용자가 직접 관리할 서버가 없다"는 의미로, 인프라 운영 책임을 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]] 제공자([[475_csp|CSP]])에게 100% 위임한다. 이로 인해 개발자는 [[001_operating_system_purpose|운영체제]] 패치, 용량 계획, 로드 밸런싱에서 해방되어 핵심 비즈니스 로직에만 집중할 수 있게 되었다.

**💡 비유**: 마치 수도꼭지를 틀 때만 물이 나오고 쓴 양(밀리초)만큼만 요금을 내는 상수도 시스템과 같다. 물탱크(서버)를 직접 사서 옥상에 관리할 필요가 전혀 없다.

이 도식은 고정 자원을 할당하는 [[183_iaas_infrastructure_as_a_service|IaaS]] 환경과 요청에 따라 동적으로 자원이 매핑되는 [[342_faas|FaaS]] 환경의 리소스 사용 패턴 한계를 대조하여 보여준다.
```text
[자원 사용량 및 트래픽 타이밍 비교도]

트래픽    :    ___/\___        ___/\/\/\___     (실제 사용자 API 요청)

[IaaS / VM 배포 모델]
Provision : ----------------------------------- (VM 항상 켜져 있음)
낭비 구간 : ▒▒▒    ▒▒▒▒▒▒▒▒▒▒▒▒           ▒▒▒▒▒ (유휴 자원 비용 발생)

[FaaS / 서버리스 배포 모델]
Function  :    ___/\___        ___/\/\/\___     (요청 즉시 실행 및 소멸)
낭비 구간 : (없음 - Scale to Zero 메커니즘 동작)
```
이 도식의 핵심은 [[183_iaas_infrastructure_as_a_service|IaaS]] 기반 구조에서는 트래픽의 고점을 기준으로 인프라를 상시 구동해야 하므로 빈 공간(유휴 자원)만큼의 비용 누수가 지속해서 발생한다는 점이다. 반면 [[342_faas|FaaS]] 모델에서는 요청이 들어오는 순간(Trigger)에만 런타임이 기동되고 즉시 소멸(Scale to [[585_zero_skipping|Zero]])하므로 자원 낭비가 완벽하게 차단된다. 실무에서는 간헐적이거나 예측 불가능한 [[129_spike_agile_technical_investigation|스파이크]]가 발생하는 워크로드에 FaaS를 도입할 때 가장 극적인 재무적 이점을 거둘 수 있다.

**📢 섹션 요약 비유**: 빈 택시가 계속 시동을 켜고 대기하며 기름을 낭비하는 것이 기존 서버라면, [[206_serverless_cold_start|서버리스]]는 승객이 부를 때만 마법처럼 차가 나타나 이동 후 바로 사라지는 순간 이동 [[090_service_kubernetes_network_load_balancing|서비스]]와 같다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**[[342_faas|FaaS]] 내부 동작 및 [[136_variance|분산]] 아키텍처 구성**
[[342_faas|FaaS]] 환경은 함수 코드가 저장소에 대기하다가 특정 이벤트가 발생하면, 동적으로 격리된 실행 환경(마이크로VM 또는 샌드박스)을 할당받아 코드를 실행한 후 즉시 반환하는 고도의 [[073_container_orchestration_tools|오케스트레이션]] 라이프사이클을 갖는다.

| 구성 요소 ([[603_component_independent_deployment_unit|Component]]) | 역할 및 기능 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Event Source** | 실행 촉발 (Trigger) | [[461_http_stateless_connection_oriented|HTTP]], S3 업로드, [[179_kafka_flink_watermark_time_window|Kafka]] 알람 등 이벤트를 수집해 라우터에 전달 | [[014_api_posix|API]], AMQP | 119 출동 신고 |
| **[[542_api_gateway|API Gateway]]** | 클라이언트 접점 제공 | [[156_rest_representational_state_transfer|REST]] 엔드포인트 노출, [[303_authentication_authorization_patterns|인증]]/[[509_authorization_models_rbac_abac|인가]], Throttling 후 페이로드 전달 | OAuth, [[549_jwt_json_web_token|JWT]] | 접수처 데스크 |
| **[[342_faas|FaaS]] Controller** | 자원 [[073_container_orchestration_tools|오케스트레이션]] | 가용 워커 노드를 탐색하고, 필요 시 새로운 인스턴스 [[528_provisioning|프로비저닝]] 지시 | Kube-[[014_api_posix|API]] | 중앙 관제 센터 |
| **MicroVM / Sandbox**| 안전한 격리 실행 환경 | Firecracker 등을 이용해 밀리초 단위로 초경량 가상머신 부팅 ([[022_kernel_role|커널]] 격리) | Firecracker | 무균 수술실 |
| **[[239_stateless_redis|Stateless]] Runtime**| 비즈니스 로직 실행 | Node.js, Python 런타임을 로드해 코드 실행. 상태는 외부 저장소 의존 | V8 엔진 | 수술 집도의 |

이 도식은 사용자의 [[014_api_posix|API]] 요청부터 [[342_faas|FaaS]] 백엔드 엔진이 어떻게 마이크로VM을 할당하고 반환하는지를 보여주는 계층 구조도이다.
```text
┌─────────────────────────────────────────────────────────────┐
│ 1. 클라이언트 요청 (HTTP / S3 이벤트 / Cron)                │
└───────┬──────────────────────────────────────────────┬──────┘
        │ (페이로드)                                   │ (응답)
┌───────▼──────────────────────────────────────────────┴──────┐
│ 2. API 게이트웨이 / 이벤트 라우터 (인증, 속도 제한)         │
└───────┬──────────────────────────────────────────────┬──────┘
        │ (함수 호출 이벤트)                           │
┌───────▼──────────────────────────────────────────────┴──────┐
│ 3. FaaS 컨트롤러 (스케일아웃 매니저)                        │
│   [ 유휴 워커 풀 ]       ==>   [ 콜드 워커 초기화 ]         │
└───────┬──────────────────────────────────────────────┬──────┘
        │ (디스패치)                                   │
┌───────▼──────────────────────────────────────────────┴──────┐
│ 4. 워커 노드 (물리 서버)                                    │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐    │
│ │ MicroVM (Warm) │ │ MicroVM (Cold) │ │ MicroVM (Term) │    │
│ │ - 노드 런타임  │ │ - OS/코드 부팅 │ │ - GC / 정리    │    │
│ │ - 실행()       │ │ - 패키지 다운  │ │                │    │
│ └────────────────┘ └────────────────┘ └────────────────┘    │
└───────┬──────────────────────────────────────────────┬──────┘
        │ (상태 읽기/쓰기 - 필수!)                     │
┌───────▼──────────────────────────────────────────────┴──────┐
│ 5. 외부 백엔드 서비스 (DynamoDB, S3, RDS)                   │
└─────────────────────────────────────────────────────────────┘
```
이 구조도의 핵심은 [[342_faas|FaaS]] 컨트롤러가 요청 인입 시 '유휴 워커(Warm)'가 있는지, '새로운 워커(Cold)'를 띄워야 하는지 판단하는 동적 스케줄링 계층에 있다. Worker Node 내부에서는 [[561_container_based_deployment|컨테이너]]보다 격리 수준이 높으면서도 부팅이 빠른 MicroVM(예: AWS Firecracker)이 사용된다. 또한 실행 환경 자체가 무상태([[239_stateless_redis|Stateless]])이므로, 모든 영구 데이터는 반드시 5번 계층(DB)에 의존해야 한다는 점이 아키텍처의 최대 제약이자 트레이드오프다.

**[[559_serverless_cold_start_mitigation|콜드 스타트]] ([[347_cold_start_problem|Cold Start]]) 메커니즘**
FaaS의 가장 치명적인 단점은 [[559_serverless_cold_start_mitigation|콜드 스타트]]다. 함수가 오랫동안 호출되지 않으면 클라우드는 비용 절감을 위해 해당 인스턴스를 회수(Kill)한다.
이 타이밍 그래프는 웜 스타트와 [[559_serverless_cold_start_mitigation|콜드 스타트]] 시 발생하는 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]]) 구간의 차이를 명확히 대조한다.
```text
[요청 시작] ──────────────────── 시간(ms) ─────────────────────► [응답 완료]

[Warm Start (최적)]
REQ ──►│ 실행(Execute) 10ms │──► ACK
       (이미 준비된 컨테이너/메모리 재사용)

[Cold Start (초기 지연 병목 발생)]
REQ ──►│ 1. 인스턴스/VM 부팅 (50ms) │
       │ 2. 런타임 초기화 (100ms)    │
       │ 3. 코드/패키지 로드 (200ms) │
       │ 4. DB 커넥션 맺기 (150ms)   │
       │ 5. 실행(Execute) (10ms)     │──► ACK (총 510ms 소요)
```
이 타이밍 도식의 핵심은 [[559_serverless_cold_start_mitigation|콜드 스타트]] 시 순수 비즈니스 로직(5번)의 실행 시간보다 인프라와 런타임이 준비되는 시간(1~4번)이 몇십 배 길게 소요된다는 점이다. [[241_machine_learning_basics|머신러닝]] 패키지처럼 크기가 크거나 JVM처럼 무거운 환경일수록 3번 구간의 [[015_지연_데이터_관점|지연]]이 치명적이다. 따라서 실시간 응답성이 극도로 중요한 경우, [[206_serverless_cold_start|서버리스]] 채택을 보류하거나 '[[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]]([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]])' 기능을 통해 강제로 웜 상태를 유지(비용 지불)하는 설계가 필요하다.

**📢 섹션 요약 비유**: 요리사가 주방에 요리 레시피(코드)만 던져놓으면, 주문이 들어올 때마다 클라우드가 0.1초 만에 도마와 가스레인지를 세팅하고 조리 후 바로 치워버리는 첨단 팝업 주방이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**[[206_serverless_cold_start|서버리스]], [[561_container_based_deployment|컨테이너]], 가상머신 아키텍처 심층 비교**
FaaS는 만능이 아니며 워크로드의 특성에 따라 [[183_iaas_infrastructure_as_a_service|IaaS]], CaaS 간의 명확한 판단이 필요하다.

| 비교 항목 | [[183_iaas_infrastructure_as_a_service|IaaS]] ([[598_vm_migration_nic|VM]], EC2) | CaaS ([[205_kubernetes_container_orchestration|Kubernetes]]) | [[342_faas|FaaS]] ([[206_serverless_cold_start|Serverless]], [[216_lambda_kappa_architecture_batch_realtime|Lambda]]) | 실무 판단 포인트 |
|:---|:---|:---|:---|:---|
| **배포 패키지** | OS 이미지 ([[162_ami_advanced_metering_infrastructure|AMI]]) | [[561_container_based_deployment|컨테이너]] 이미지 ([[063_docker_architecture|Docker]]) | 순수 코드 조각 (Function) | 개발자 [[686_cognitive_load_team_topologies|인지 부하]] 크기 |
| **[[249_scaling_normalization_standardization|스케일링]] 속도** | 수 분 (Minutes) | 수 초 (Seconds) | 밀리초 (Milliseconds) | 피크 트래픽 대응력 |
| **과금 기준** | VM이 켜진 시간 | 클러스터 할당 자원 풀 | [[294_function_calling_tool_use|함수 호출]] 횟수 + 실행 시간 | 유휴 시간 비율 |
| **상태([[272_state_pattern|State]]) 관리**| 자체 디스크 보존 | [[153_pv_planned_value|PV]]/[[269_pvc_vs_svc_virtual_circuits|PVC]] 활용 보존 가능 | 완전 무상태 ([[239_stateless_redis|Stateless]]) | 외부 [[002_database_definition|데이터베이스]] 의존도 |
| **제어 및 유연성** | 높음 ([[022_kernel_role|커널]] 단위 조작) | 중간 (네트워크 [[164_policy|정책]] 조작) | 매우 낮음 (벤더 환경 종속) | 벤더 락인([[362_lock_in_portability|Lock-in]]) [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] |

이 매트릭스는 "어느 기술이 우월한가"가 아니라 "통제권(Control)과 자동화(Automation) 사이의 저울질"을 나타낸다. FaaS는 운영 자동화의 정점에 있지만, 개발자의 통제권(인프라 디버깅, 네트워크 세밀 조정)을 앗아간다. IaaS는 통제권이 완벽하지만 인프라 운영 노동([[685_toil_automation_sre|Toil]])이 극심하다. 실무에서는 상시 트래픽은 CaaS로 처리하고 비동기 배치/알람은 FaaS로 분리하는 '하이브리드 [[619_msa_traffic_hardware|MSA]]' 전략이 보편적이다.

**📢 섹션 요약 비유**: 자가용([[183_iaas_infrastructure_as_a_service|IaaS]])은 내 마음대로 튜닝할 수 있고, 시내버스(CaaS)는 안정적인 노선을 달리며, 택시([[342_faas|FaaS]])는 편하지만 매일 장거리를 타면 요금 폭탄을 맞게 된다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

**[[342_faas|FaaS]] 실무 운영 시나리오 및 트러블슈팅**
[[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]]는 도입 초기에는 훌륭하지만, 트래픽이 거대해지면 기존 환경과는 전혀 다른 성격의 장애 병목을 유발한다.

**시나리오: RDBMS 커넥션 풀 고갈 현상 (치명적 [[128_water_scrum_fall_anti_pattern|안티패턴]])**
가장 흔한 실패 사례는 FaaS에서 기존 온프레미스형 RDBMS(MySQL, [[188_pl_sql_t_sql_procedural|Oracle]])를 직접 호출하는 것이다. 
이 도식은 오토 [[249_scaling_normalization_standardization|스케일링]]되는 [[342_faas|FaaS]] 환경이 백엔드 DB 연결 병목을 어떻게 유발하는지 시각화한다.
```text
[Client / 클라이언트]        [API Gateway / API 게이트웨이]             [FaaS (AWS Lambda)]            [RDBMS]
                            ____(Scale-out)___
Requests =>    1,000 req => │ Func 1 (Conn 1) │ --- (TCP Handshake) ---> [DB Max Conn = 200]
                            │ Func 2 (Conn 1) │ --- (TCP Handshake) --->  │
                            │ ...             │                           │ (200개 초과 시 즉각 연결 거부!)
                            │ Func 1000 (Conn)│ --- (Conn Refused) ----X (전체 시스템 장애 발생)
                            -------------------
```
이 흐름의 핵심은 FaaS의 무한한 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]이 역설적으로 백엔드 [[002_database_definition|데이터베이스]]를 공격하는 자체 DDoS 형태가 된다는 점이다. 기존 WAS 서버는 한정된 [[092_thread_lwp|스레드]] 내에서 DB 커넥션 풀을 공유하지만, FaaS는 각각 독립된 마이크로VM이므로 풀을 공유하지 못하고 수천 개의 새로운 연결을 맺으려다 DB를 터뜨린다.
* **실무 판단**: 이를 방지하기 위해 [[342_faas|FaaS]] 전용 DB [[264_proxy_pattern_surrogate_access_control|프록시]](예: AWS RDS [[264_proxy_pattern_surrogate_access_control|Proxy]])를 중간에 두어 커넥션을 캐싱하거나, 아예 연결 오버헤드가 없는 [[461_http_stateless_connection_oriented|HTTP]] [[014_api_posix|API]] 기반의 [[136_variance|분산]] [[035_nosql|NoSQL]]([[545_dynamodb|DynamoDB]])로 전환해야 한다.

**[[206_serverless_cold_start|서버리스]] 도입 [[435_checklist_based_testing|체크리스트]]**
1. **장기 실행 제약**: FaaS는 최대 실행 시간 제한(예: 15분)이 존재한다. 동영상 인코딩 같은 작업은 [[206_serverless_cold_start|서버리스]] 대신 배치 전용 [[561_container_based_deployment|컨테이너]]로 넘겨야 한다.
2. **[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 필수**: [[568_logs_distributed_logging_elk_fluentd|로그]] 파일에 직접 접근할 수 없으므로, [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] 기반의 Trace ID를 코드에 심어 전체 호출 흐름을 엮는 중앙 집중형 로깅이 필수다.

**📢 섹션 요약 비유**: 수만 명의 아르바이트생([[342_faas|FaaS]])을 한 번에 고용해 일을 시킬 수는 있지만, 이들이 동시에 좁은 창고(DB) 문으로 뛰어들면 병목 사고가 발생하므로 반드시 효율적인 안내 요원(DB [[264_proxy_pattern_surrogate_access_control|프록시]])을 배치해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**도입 기대 효과 (정량 / 정성)**

| 구분 | 모놀리식/[[183_iaas_infrastructure_as_a_service|IaaS]] 도입 시 | [[342_faas|FaaS]]([[206_serverless_cold_start|서버리스]]) 적용 시 | 변동 차이 및 [[012_roi_return_on_investment|ROI]] |
|:---|:---|:---|:---|
| **비용 ([[344_finops|FinOps]])** | 월 100만 원 (상시 가동) | 월 5만 원 (가변) | 간헐적 트래픽 시스템 한정 최대 95% 절감 |
| **운영 공수 ([[685_toil_automation_sre|Toil]])**| 주 20시간 (OS/[[406_patch_management|패치 관리]]) | 주 2시간 (코드 관리) | [[100_sre_site_reliability_engineering_error_budget|SRE]] 엔지니어의 로드 80% 이상 감소 |
| **[[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]** | 분 단위 대기 ([[598_vm_migration_nic|VM]] 부팅) | 수십 밀리초 반응 | [[129_spike_agile_technical_investigation|스파이크]] 트래픽에 대한 무중단 대응력 확보 |

**미래 전망과 아키텍처 진화**
FaaS는 단순히 함수 조각을 넘어서, 진정한 [[531_cloud_native_architecture|클라우드 네이티브]]의 종착지로 나아가고 있다. 과거 [[475_csp|CSP]] 벤더 종속이 한계로 지적되었으나, 최근에는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 위에서 구동되는 [[191_oss_license_compliance|오픈소스]] [[206_serverless_cold_start|서버리스]] 플랫폼(Knative, OpenFaaS)이 표준으로 자리 잡으며 하이브리드 [[206_serverless_cold_start|서버리스]] 환경이 열리고 있다. 또한, [[559_serverless_cold_start_mitigation|콜드 스타트]]를 근본적으로 제거하기 위해 무거운 [[561_container_based_deployment|컨테이너]] 대신 [[319_webassembly_architecture|WebAssembly]]([[701_webassembly_wasm_frontend_performance|Wasm]]) 기술이 [[235_edge_computing_smart_factory|엣지 컴퓨팅]] 기반의 초경량 런타임(Cloudflare Workers)으로 통합 발전하는 추세다.

**📢 섹션 요약 비유**: FaaS는 레고 블록만 조립하면 알아서 거대한 건물이 지어지고 사라지는 마법이다. 미래에는 이 블록마저 사용자 바로 옆(엣지)에서 0.001초 만에 조립될 것이다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
* [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]] ([[064_eda|EDA]]) | FaaS의 비동기 실행을 촉발하는 근본적인 아키텍처 철학이자 설계 패턴
* AWS Firecracker | [[206_serverless_cold_start|서버리스]] 함수의 고속 부팅과 [[022_kernel_role|커널]] 격리를 동시에 보장하는 마이크로VM 엔진
* [[542_api_gateway|API Gateway]] | 외부 트래픽을 정제하고 FaaS로 안전하게 라우팅하는 단일 진입점 [[264_proxy_pattern_surrogate_access_control|프록시]] [[690_firewall_generation_evolution|방화벽]]
* [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]] ([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]]) | [[559_serverless_cold_start_mitigation|콜드 스타트]] [[015_지연_데이터_관점|지연]]을 방지하기 위해 [[561_container_based_deployment|컨테이너]]를 강제로 웜 상태로 유지하는 기법
* [[221_bounded_context_ddd_msa_boundary|Bounded Context]] | [[310_architecture|도메인 주도 설계]]([[310_architecture|DDD]])에서 하나의 [[342_faas|FaaS]] 함수 또는 [[090_service_kubernetes_network_load_balancing|서비스]]가 책임지는 논리적 경계

### 📈 관련 키워드 및 발전 흐름도

```text
[가상 머신 (VM, Virtual Machine)]
    │
    ▼
[컨테이너 (Container)]
    │
    ▼
[FaaS (Function as a Service)]
    │
    ▼
[이벤트 기반 아키텍처 (Event-Driven Architecture)]
```

이 흐름도는 VM과 [[561_container_based_deployment|컨테이너]]를 지나 FaaS와 [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]]로 발전하는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. 예전 컴퓨터는 우리가 사용하지 않을 때도 전기를 켜두고 요금을 내야 하는 비싼 장난감이었어요.
2. [[206_serverless_cold_start|서버리스]]([[342_faas|FaaS]])는 똑똑한 로봇 수도꼭지 같아서, 우리가 손을 댈 때만 딱 켜져서 일하고 그 1초만큼만 동전을 낸답니다.
3. 그래서 평소에 안 쓰는 기능들을 이걸로 만들면 컴퓨터 요금을 엄청나게 아낄 수 있고 고장도 안 나요!