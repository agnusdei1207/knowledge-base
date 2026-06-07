---
title: "OOM Killer Kubernetes QoS cgroup Memory Limits"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 357
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out-of-Memory](/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/)) Killer는 Linux [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 물리 메모리 부족 시 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Score 기준으로 프로세스를 강제 종료하는 최후의 안전장치이며, [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스는 이 우선순위를 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 수준에서 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)화한다.
> 2. **가치**: cgroup v2의 memory.limit_in_bytes와 K8s Resource Request/Limit을 통해 노드 전체 메모리 고갈을 방어하고, BestEffort < Burstable < Guaranteed 순서로 중요 워크로드가 마지막에 종료되도록 보장한다.
> 3. **판단 포인트**: [OOM Killed](/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/) 반복 발생은 [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) 버그이거나 Limit [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 과소 추정으로, Prometheus의 container_memory_working_set_bytes [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)으로 실제 사용량을 측정해 Limit을 조정하고 [VPA](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/) ([Vertical Pod Autoscaler](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/))로 자동화해야 한다.

---

## Ⅰ. 개요 및 필요성

Linux [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 메모리 부족 상황에서 시스템 전체 마비를 막기 위해 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer를 실행한다. [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer는 /proc/[pid]/oom_score를 기준으로 종료 대상 프로세스를 선정하며, oom_score는 프로세스의 메모리 사용량, 실행 시간, nice 값을 종합해 계산된다. 점수가 높을수록 먼저 종료된다.

[Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경에서 단일 노드의 여러 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 메모리를 경쟁할 때, 중요한 시스템 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)(kube-apiserver, [kubelet](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/))보다 사용자 워크로드가 먼저 종료되어야 한다. K8s [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스는 이 우선순위를 [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)만으로 제어한다.

[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)화 환경에서 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed는 재시작 루프(CrashLoopBackOff)와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단의 주요 원인이다. 특히 Java 힙, Node.js [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/), ML 모델 로딩 실패가 자주 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)한다.

- 📢 섹션 요약 비유: [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer는 선박이 침몰하기 직전 화물을 버리는 것과 같다. 가장 무거운 화물을 먼저 버려 배를 구하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|             K8s QoS 클래스와 OOM Score 우선순위                  |
+------------------------------------------------------------------+
|  [BestEffort] oom_adj=1000 — 가장 먼저 종료                     |
|  Request=0, Limit=0 (설정 없음)                                  |
|                                                                  |
|  [Burstable] oom_adj=1~999 — 중간 우선순위                      |
|  Request < Limit 또는 일부 컨테이너만 설정                       |
|                                                                  |
|  [Guaranteed] oom_adj=-998 — 마지막에 종료                      |
|  Request == Limit (모든 컨테이너)                                |
|                                                                  |
|  cgroup v2 경계                                                  |
|  memory.limit_in_bytes 초과 시 해당 cgroup 내 프로세스 종료     |
+------------------------------------------------------------------+
```

| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스   | 조건                          | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 종료 순서 | oom_adj 범위 |
| :----------- | :---------------------------- | :------------ | :----------- |
| BestEffort   | Request/Limit 미설정           | 1순위 (먼저)  | 1000         |
| Burstable    | Request와 Limit 다름           | 2순위         | 1~999        |
| Guaranteed   | Request == Limit               | 3순위 (마지막)| -998         |

**cgroup v2 메모리 제어**: `memory.limit_in_bytes`는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 최대 메모리 경계다. 초과 시 해당 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 강제 종료가 발생한다.

<strong>Java <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a></strong>: JVM 힙은 `-Xmx` 미설정 시 호스트 전체 메모리의 1/4을 사용하려 시도한다. K8s에서는 `-XX:MaxRAMPercentage=75.0` 옵션으로 cgroup 인식을 강제해야 한다.

- 📢 섹션 요약 비유: [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) Guaranteed는 비행기 비즈니스석이다. 경제석(BestEffort) 승객이 먼저 내리고, 비즈니스석(Guaranteed) 승객은 마지막까지 자리를 지킨다.

---

## Ⅲ. 비교 및 연결

| 항목              | 전통 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 환경               | K8s cgroup 환경              |
| :---------------- | :------------------------- | :--------------------------- |
| 메모리 격리       | [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 수준       | cgroup v2 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 수준      |
| [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 제어          | OS 전체 메모리 경쟁        | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)별 Limit 경계        |
| 우선순위 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)     | OS nice/oom_adj 수동 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)  | K8s [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스 자동 매핑     |
| 자원 최적화       | 수동 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 사이즈 조정        | [VPA](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/) ([Vertical Pod Autoscaler](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/))|

<strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/">VPA</a> (<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/">Vertical Pod Autoscaler</a>)</strong>: Pod의 과거 메모리·CPU 사용량을 학습해 Request/Limit을 자동 권장하거나 적용한다. [OOM Killed](/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/) 반복 시 VPA가 자동으로 Limit을 높여 재시작 루프를 방지한다.

- 📢 섹션 요약 비유: JVM이 cgroup를 모르면 창고([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)) 안에 있는데 창고 바깥의 공간도 자기 것으로 착각하고 물건을 쌓다가 강제 종료된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/">OOM Killed</a> 방어 <a href="/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
1. 모든 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에 Resource Request/Limit [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (Guaranteed 권장)
2. [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) `kube_pod_container_status_last_terminated_reason == OOMKilled` 알람 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)
3. `container_memory_working_set_bytes` 기반 실제 사용량 측정 후 Limit 조정
4. Java: `-XX:MaxRAMPercentage=75.0`, Node.js: `--max-old-space-size` 명시
5. [VPA](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/) 도입 검토: Recommendation 모드로 시작

<strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
- Request 0, Limit 무한대 -> BestEffort로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/), 먼저 종료됨
- Limit을 Request의 10배 이상 -> 노드 메모리 오버커밋
- Java `-Xmx` 미설정 -> cgroup Limit 초과 [OOM Killed](/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/) 반복

- 📢 섹션 요약 비유: Resource Limit 없이 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 운영하는 것은 무한 리필 뷔페에서 접시 제한 없이 음식을 쌓는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

Guaranteed QoS와 VPA를 도입하면 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed로 인한 CrashLoopBackOff 빈도가 80% 이상 감소한다. 노드 메모리 사용률이 안정적 범위(70~80%)에서 유지되며 자원 낭비도 줄어든다.

미래는 cgroup v2와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자원 예측(Karpenter)이 사전 예방적 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)을 실현하는 방향이다.

- 📢 섹션 요약 비유: VPA는 스마트한 창고 관리 AI다. 과거 사용 패턴을 학습해 창고가 터지기 전에 미리 적정 크기로 조정한다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| cgroup v2                               | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 메모리/CPU 격리 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기본 메커니즘               |
| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스                              | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 종료 우선순위 결정, K8s [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에서 자동 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)        |
| [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Score                               | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [프로세스 종료](/studynote/02_operating_system/02_process_thread/107_process_termination/) 순서 결정하는 점수                   |
| [VPA](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/) ([Vertical Pod Autoscaler](/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/))           | 과거 사용량 기반 Request/Limit 자동 권장·적용             |
| container_memory_working_set_bytes      | [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 실제 메모리 사용량 측정               |

### 📈 관련 키워드 및 발전 흐름도

```text
Linux OOM Killer (커널 기반 프로세스 강제 종료)
    |
    v
cgroup v1 — 컨테이너 메모리 격리
    |
    v
K8s Resource Request/Limit + QoS 클래스
    |
    v
cgroup v2 — 계층적 메모리 제어 강화
    |
    v
VPA (Vertical Pod Autoscaler) — 자동 자원 최적화
    |
    v
AI 기반 사전 예측적 자원 관리 (Karpenter)
```

흐름은 "사후 강제 종료 -> 격리 경계 -> [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 우선순위 -> 자동 최적화 -> [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 예측"으로 진화한다.

### 👶 어린이를 위한 3줄 비유 설명

1. [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer는 물이 넘칠 때 가장 물을 많이 쓰는 수도꼭지를 먼저 잠그는 자동 안전장치예요.
2. K8s QoS는 중요한 앱(Guaranteed)은 물이 부족해도 마지막까지 쓸 수 있게 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)해줘요.
3. VPA는 스마트 전기 계량기처럼 내 앱이 얼마나 메모리를 쓰는지 학습해서 자동으로 적당한 용량을 배정해줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 357 / 373

<- **이전**: [356. 데이터옵스 CI/CD dbt 분석 파이프 자동망 (DataOps CI/CD with dbt)](/studynote/15_devops_sre/05_devsecops/356_ci_cd_dbt/)
**다음**: [358. 서드파티 API 통신 폴백 지터 백오프 설계 (Third-party API Fallback Jitter and Exponential](/studynote/11_design_supervision/06_exam_summary/358_architecture/) ->

---
