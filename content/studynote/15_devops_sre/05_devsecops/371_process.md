---
title: 371. DevOps 클라우드 기술사 핵심 키워드 통합 요약 (DevOps Cloud PE Integrated Keyword Summary)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[652_devops_calms_culture|DevOps]]/SRE와 클라우드 영역의 기술사 시험은 개별 기술 암기보다 "왜 이 기술을 선택했는가, 어떤 트레이드오프가 있는가"를 [[369_logic_bomb|논리]]적으로 서술하는 능력을 측정하며, 각 개념이 어떤 문제를 해결하기 위해 등장했는지를 연결하는 것이 핵심이다.
> 2. **가치**: [[090_configuration_item|CI]]/CD → [[793_iac_idempotency_template|IaC]] → [[561_container_based_deployment|컨테이너]]/K8s → [[302_service_mesh_istio|서비스 메시]] → [[642_observability_telemetry|옵저버빌리티]] → [[100_sre_site_reliability_engineering_error_budget|SRE]]/[[181_slo_service_level_objective|SLO]] → [[751_chaos_engineering|카오스 엔지니어링]]으로 이어지는 [[652_devops_calms_culture|DevOps]] 발전 흐름을 하나의 스토리로 연결하면, 개별 문제에서 통합 아키텍처 답안을 구성할 수 있다.
> 3. **판단 포인트**: 기술사 답안에서는 장점만 나열하는 것이 아니라 "이 기술의 적합한 조건, 부적합한 조건, 그리고 한계"를 명시해야 심사관이 전문성을 인정한다.

---

## Ⅰ. [[652_devops_calms_culture|DevOps]]/[[100_sre_site_reliability_engineering_error_budget|SRE]] 핵심 키워드 맵

DevOps는 개발(Dev)과 운영(Ops)의 장벽을 제거해 소프트웨어 전달 속도와 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 동시에 높이는 문화·프랙티스·도구의 집합이다. [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]])는 [[181_slo_service_level_objective|SLO]]/[[102_sli_slo_service_level_indicator_objective|SLI]]/[[085_sla|SLA]] 기반 에러 버짓([[101_error_budget_sre|Error Budget]])으로 안정성과 혁신 속도의 균형을 수치화한다.

**[[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 핵심**:
- [[090_configuration_item|CI]] ([[019_continuous_integration|Continuous Integration]]): 코드 병합 시 자동 빌드·테스트. 도구: GitHub Actions, [[071_jenkins_ci_cd_pipeline_automation|Jenkins]], GitLab [[090_configuration_item|CI]]
- CD ([[164_continuous_delivery|Continuous Delivery]]): 언제든지 릴리즈 가능한 상태 유지
- 배포 [[268_strategy_pattern|전략]]: Blue-Green, [[595_canary_stack_smashing_protector|Canary]], [[083_rolling_update_deployment_zero_downtime_version_inconsistency|Rolling Update]]

**[[793_iac_idempotency_template|IaC]] ([[062_infrastructure_as_code|Infrastructure as Code]])**:
- [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]: 멀티클라우드 선언적 인프라 [[528_provisioning|프로비저닝]]
- [[198_ansible_os_configuration_management_ssh|Ansible]]: 에이전트리스 [[089_configuration_management|구성 관리]], YAML [[637_playbook|Playbook]]

- 📢 섹션 요약 비유: DevOps는 주방과 홀 직원이 실시간으로 소통하는 레스토랑이다. 요리사(개발)가 새 메뉴를 만들면 홀(운영)이 바로 손님에게 제공하며, 불만이 생기면 즉시 주방으로 피드백이 간다.

---

## Ⅱ. [[561_container_based_deployment|컨테이너]]/[[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 핵심 키워드

```text
┌──────────────────────────────────────────────────────────────────┐
│              K8s 핵심 구성 요소 요약                             │
├──────────────────────────────────────────────────────────────────┤
│  Control Plane: kube-apiserver, etcd, scheduler, controller-mgr  │
│  Worker Node: kubelet, kube-proxy, Container Runtime (containerd)│
│  핵심 오브젝트: Pod, Deployment, Service, Ingress, ConfigMap     │
│  스케일링: HPA (CPU/메트릭), VPA (메모리), KEDA (이벤트 기반)   │
│  스토리지: PV/PVC, StorageClass (동적 프로비저닝), CSI 드라이버 │
│  네트워킹: CNI (Cilium, Calico, Flannel), Service Mesh (Istio)  │
└──────────────────────────────────────────────────────────────────┘
```

**[[302_service_mesh_istio|서비스 메시]] ([[302_service_mesh_istio|Istio]], Linkerd)**:
- [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 자동 암호화, 트래픽 제어, Retry/[[319_timeout_prevention|Timeout]]/[[304_circuit_breaker|Circuit Breaker]]
- [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]](Jaeger), [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집([[136_prometheus|Prometheus]]), 가시성 제공

- 📢 섹션 요약 비유: Kubernetes는 [[561_container_based_deployment|컨테이너]] 오케스트라 지휘자다. 수백 개 악기([[561_container_based_deployment|컨테이너]])의 배치, 시작, 종료, 재시작을 자동으로 관리한다.

---

## Ⅲ. [[642_observability_telemetry|옵저버빌리티]] & [[100_sre_site_reliability_engineering_error_budget|SRE]] 핵심 키워드

**[[642_observability_telemetry|옵저버빌리티]] 3대 지주**:
- [[567_metrics_time_series_prometheus_grafana|Metrics]] ([[342_routing_metric_hop_bandwidth_delay|메트릭]]): [[136_prometheus|Prometheus]] + [[168_grafana|Grafana]]. RED [[342_routing_metric_hop_bandwidth_delay|메트릭]](Rate/Errors/Duration)
- [[568_logs_distributed_logging_elk_fluentd|Logs]] ([[568_logs_distributed_logging_elk_fluentd|로그]]): ELK [[057_stack|Stack]] ([[302_cdc|Elasticsearch]] + Logstash + [[169_kibana|Kibana]]), Loki + [[168_grafana|Grafana]]
- Traces (추적): Jaeger, Zipkin, [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]

**[[100_sre_site_reliability_engineering_error_budget|SRE]] 핵심 지표**:
- [[102_sli_slo_service_level_indicator_objective|SLI]] ([[102_sli_slo_service_level_indicator_objective|Service Level Indicator]]): 측정 가능한 지표 ([[452_availability|가용성]] %, 레이턴시 p99)
- [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]): 목표치 (99.9% [[452_availability|가용성]])
- [[101_error_budget_sre|Error Budget]]: SLO에서 허용하는 오류 허용치 (100% - [[181_slo_service_level_objective|SLO]]%)

**[[751_chaos_engineering|카오스 엔지니어링]]**: Netflix [[149_chaos_monkey_chaos_mesh|Chaos Monkey]], Chaos [[389_mesh_topology|Mesh]], Litmus로 프로덕션 장애 발생 전 시스템 약점을 발견한다.

- 📢 섹션 요약 비유: [[642_observability_telemetry|옵저버빌리티]]는 자동차 계기판이다. 속도([[342_routing_metric_hop_bandwidth_delay|메트릭]]), 경고 [[389_mesh_topology|메시]]지([[568_logs_distributed_logging_elk_fluentd|로그]]), GPS 경로(추적)가 함께 있어야 운전자([[100_sre_site_reliability_engineering_error_budget|SRE]])가 안전하게 운영한다.

---

## Ⅳ. 클라우드 아키텍처 핵심 패턴

**고가용성 패턴**:
- [[304_circuit_breaker|Circuit Breaker]] (Resilience4j): 연속 장애 시 빠른 실패 복귀
- Retry + Exponential Backoff + Jitter: 재시도 폭풍 방지
- [[308_bulkhead_pattern|Bulkhead]]: [[090_service_kubernetes_network_load_balancing|서비스]]별 [[092_thread_lwp|스레드]]풀 격리로 장애 전파 방지
- [[305_saga_pattern|Saga Pattern]]: [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 보상 로직

**[[531_cloud_native_architecture|클라우드 네이티브]] [[200_12_factor_app_cloud_native_principles|12-Factor App]]**: [[007_codebase|코드베이스]] 단일화, 의존성 명시, [[009_config|설정]] 환경변수 분리, [[012_stateless_processes|무상태 프로세스]], [[013_port_binding|포트 바인딩]], [[568_logs_distributed_logging_elk_fluentd|로그]] 스트림 등.

- 📢 섹션 요약 비유: Circuit Breaker는 전기 두꺼비집이다. 과부하(연속 장애)가 걸리면 자동으로 차단해 전체 회로(시스템)를 [[571_protection_vs_security|보호]]한다.

---

## Ⅴ. 보안([[653_devsecops_shift_left|DevSecOps]]) 핵심 키워드

**[[491_sast_static_analysis|SAST]]/[[492_dast_dynamic_analysis|DAST]]/[[453_sca|SCA]]**:
- [[491_sast_static_analysis|SAST]] (Static AST): 소스코드 취약점 분석 ([[079_sonarqube|SonarQube]])
- [[492_dast_dynamic_analysis|DAST]] (Dynamic AST): 실행 중 취약점 분석 ([[485_owasp_zap|OWASP ZAP]])
- [[453_sca|SCA]] ([[495_sca_software_composition_analysis|Software Composition Analysis]]): [[191_oss_license_compliance|오픈소스]] [[336_library_vs_framework|라이브러리]] 취약점 (Snyk)

**[[667_zero_trust_runtime_integrity_measurement|Zero Trust]]**: Never Trust, Always Verify 원칙. [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], SPIFFE/SPIRE로 [[090_service_kubernetes_network_load_balancing|서비스]] 간 신원 증명.

**[[374_supply_chain_security|공급망 보안]]**: [[890_sbom_cyclonedx_spdx|SBOM]] ([[890_sbom_cyclonedx_spdx|Software Bill of Materials]]), Cosign + Sigstore, SLSA ([[520_supply_chain_attack_and_ci_cd_security|Supply chain]] Levels for Software Artifacts).

- 📢 섹션 요약 비유: DevSecOps에서 SBOM은 식품 성분표이다. 소프트웨어에 어떤 [[191_oss_license_compliance|오픈소스]] 재료([[336_library_vs_framework|라이브러리]])가 들어있는지 명시해, 특정 재료에 문제가 생기면 즉시 [[396_validation|확인]]·교체할 수 있다.

---

### 📌 관련 개념 맵

| 개념                              | 연결 포인트                                               |
| :-------------------------------- | :-------------------------------------------------------- |
| [[100_sre_site_reliability_engineering_error_budget|SRE]] / [[101_error_budget_sre|Error Budget]]                | [[181_slo_service_level_objective|SLO]] 기반 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]과 개발 속도 균형 수치화                  |
| [[119_gitops_single_source_of_truth|GitOps]] ([[114_argocd_gitops_cd|Argo CD]], Flux)            | Git을 단일 진실의 원천으로 K8s 상태 선언적 관리          |
| [[344_finops|FinOps]]                            | [[227_cloud_cost_optimization|클라우드 비용 최적화]]                                     |
| [[109_platform_engineering_cognitive_load|Platform Engineering]]              | [[110_idp_internal_developer_platform_backstage|내부 개발자 플랫폼]]([[536_idp_identity_provider|IDP]]), 셀프서비스 인프라               |
| [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]                     | [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·추적 통합 관측성 표준                        |
| SLSA / [[890_sbom_cyclonedx_spdx|SBOM]]                       | 소프트웨어 [[374_supply_chain_security|공급망 보안]] 성숙도 프레임워크                 |

### 📈 관련 키워드 및 발전 흐름도

```text
Agile + CI/CD (개발·배포 자동화)
    │
    ▼
IaC + GitOps (인프라 코드화, 선언적 관리)
    │
    ▼
컨테이너 / K8s (불변 인프라, 오케스트레이션)
    │
    ▼
서비스 메시 + 옵저버빌리티 (가시성, mTLS)
    │
    ▼
SRE + Error Budget (신뢰성 수치화)
    │
    ▼
Platform Engineering + FinOps (내부 플랫폼화, 비용 최적화)
    │
    ▼
AI-assisted DevOps (자율 장애 탐지·복구)
```

### 👶 어린이를 위한 3줄 비유 설명

1. DevOps는 요리사(개발자)와 웨이터(운영자)가 팀을 이뤄 손님에게 최고의 [[090_service_kubernetes_network_load_balancing|서비스]]를 빠르게 전달하는 방식이에요.
2. SRE는 레스토랑이 얼마나 자주 문제가 생겨도 되는지(에러 버짓)를 숫자로 정해서 혁신과 안정성을 균형 있게 관리해요.
3. [[642_observability_telemetry|옵저버빌리티]]는 주방 [[933_cctv|CCTV]]([[568_logs_distributed_logging_elk_fluentd|로그]]), 온도계([[342_routing_metric_hop_bandwidth_delay|메트릭]]), 배달 추적(추적)이 모두 있어야 음식이 왜 문제가 생겼는지 알 수 있는 것과 같아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 371 / 373

← **이전**: [[370_did_zkp|370. DID 분산신원 ZKP 영지식증명 자기주권신원 (DID Decentralized Identity ZKP Self-Sovereign]]
**다음**: [[372_zero_trust|372. 제로 트러스트 아키텍처 신원 기반 접근 제어 (Zero Trust Architecture ZTNA SASE NIST SP 800-207)]] →

---
