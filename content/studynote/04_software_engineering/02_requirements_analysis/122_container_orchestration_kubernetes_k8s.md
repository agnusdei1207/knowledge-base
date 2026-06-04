+++
title = "122. 컨테이너 오케스트레이션 (Container Orchestration) - K8s 핵심 개념과 아키텍처"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 오케스트레이션은 <strong>수백~수천 개 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>의 배포·<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a>·네트워킹·자동 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>를 자동화</strong>하는 시스템이며, [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)(K8s)가 사실상 유일한 산업 표준이다.
> 2. **가치**: 단일 [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 `docker run`으로 관리하지만, 프로덕션 환경에서 수백 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 <strong>헬스체크·오토스케일링·<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/">롤링 업데이트</a>·<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/">서비스 디스커버리</a></strong>를 수동 관리하는 것은 불가능하며, K8s가 이를 <strong>선언적으로 자동화</strong>한다.
> 3. **판단 포인트**: K8s의 핵심은 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/">Desired State</a> -> Reconciliation Loop</strong>이며, [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)·[Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)·[Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·Ingress의 4대 리소스와 Control Plane([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Server·[etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/)·Scheduler·Controller Manager)의 아키텍처를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    K8s 클러스터 아키텍처                              |
+-------------------------------------------------------+
|  [Control Plane (Master)]                             |
|   API Server <- kubectl / CI/CD                       |
|   etcd (상태 저장소)                                  |
|   Scheduler (Pod 배치)                                |
|   Controller Manager (Reconciliation)                 |
|                                                       |
|  [Worker Nodes]                                       |
|   kubelet -> Pod(Container) 실행                      |
|   kube-proxy -> 네트워크 라우팅                       |
|   Container Runtime (containerd)                      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: K8s는 항공 관제탑(Control Plane)이 수백 대 비행기([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))의 이착륙·경로·연료(리소스)를 자동 관리하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4대 핵심 리소스

| 리소스 | 역할 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/">Pod</a></strong> | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행 최소 단위 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a></strong> | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·[롤링 업데이트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/) 관리 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a></strong> | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 그룹에 안정적 네트워크 엔드포인트 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/">Ingress</a></strong> | 외부 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 트래픽 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |

- **📢 섹션 요약 비유**: Pod는 방([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)), Deployment는 아파트 동([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 관리), Service는 우편함(고정 주소), Ingress는 정문(외부 접근)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) Compose | K8s | Nomad |
|:---|:---|:---|:---|
| **규모** | 단일 호스트 | **멀티 노드 클러스터** | 멀티 노드 |
| **Self-healing** | 없음 | <strong>자동 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| **생태계** | 작음 | <strong>최대 (<a href="/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/">CNCF</a>)</strong> | 작음 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### K8s 도입 판단 기준
- [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 10개 이하: [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) Compose로 충분.
- [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 50개+, 멀티팀: K8s 도입 적합.
- [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 우선: AWS Fargate/Cloud Run 고려.

---

## Ⅴ. 기대효과 및 결론

K8s는 <strong>클라우드 네이티브의 운영 체제</strong>이며, [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 생태계([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)·ArgoCD·[Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·[Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/))와 결합하여 현대 인프라의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/">Pod</a></strong> | K8s 최소 실행 단위 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a></strong> | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·업데이트 관리 |
| **Control Plane** | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Server·[etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/)·Scheduler |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/">CNCF</a></strong> | K8s 생태계 재단 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/">Helm</a></strong> | K8s 패키지 매니저 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Docker (2013) — 컨테이너 런타임]
    |
    v
[Docker Swarm / Mesos (2014~) — 초기 오케스트레이션]
    |
    v
[Kubernetes (2014, Google->CNCF) — 산업 표준]
    |
    v
[Managed K8s (EKS/GKE/AKS, 2018~)]
    |
    v
[현재: K8s + Service Mesh + GitOps — 클라우드 네이티브 풀스택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K8s는 <strong>항공 관제탑</strong>이에요. 수백 대 비행기([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))를 자동으로 관리해요.
2. 비행기가 고장 나면 **자동으로 다른 비행기를 보내서(Self-healing)** [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 멈추지 않아요.
3. "비행기 3대 유지해"라고 말하면(선언적) **관제탑이 알아서** 3대를 유지한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 973

<- **이전**: [121. CI/CD 파이프라인 자동화 - 빌드·테스트·배포의 지속적 통합/전달 체계](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/121_cicd_pipeline_automation/)
**다음**: [123. 서버리스 & FaaS (Serverless / AWS Lambda) - 인프라 없는 함수 단위 컴퓨팅](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/123_serverless_faas_aws_lambda/) ->

---
