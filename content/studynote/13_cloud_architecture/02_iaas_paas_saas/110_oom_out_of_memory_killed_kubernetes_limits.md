---
title: "110. OOM Killed (Out of Memory) - K8s 파드 메모리 초과 강제 종료와 QoS 생존 전략"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 `resources.limits.memory`로 선언한 메모리 상한을 초과하는 순간, 리눅스 커널의 <strong><a href="/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> Killer가 SIGKILL(9번 시그널)로 프로세스를 즉시 사살</strong>하는 [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 기반 자원 통제 메커니즘이다.
> 2. **가치**: 이 사형 집행이 없으면 [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 1개가 노드 전체 RAM을 독점하여 <strong>같은 노드의 다른 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/">파드</a>·kubelet까지 동반 질식사(Node <a href="/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a>)</strong>하는 연쇄 붕괴를 야기한다.
> 3. **판단 포인트**: K8s [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스(Guaranteed > Burstable > BestEffort) 순으로 사살 우선순위가 결정되며, <strong>CPU 초과는 Throttling(감속)이지만 메모리 초과는 즉사</strong>라는 비대칭성이 핵심이다.

---

## Ⅰ. 개요 및 필요성

CPU를 초과하면 K8s는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 죽이지 않고 **속도를 늦춘다(Throttling)**. 하지만 메모리(RAM)는 "빌린 뒤 반환 불가능한" 자원이므로, 한도를 넘는 순간 리눅스 커널이 프로세스를 <strong>즉시 사살(<a href="/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> Killed)</strong>하여 다른 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 보호한다.

```text
+-------------------------------------------------------+
|      CPU 초과 vs 메모리 초과: 비대칭 대응               |
+-------------------------------------------------------+
|  [CPU 초과]                                           |
|   limits.cpu: 500m 초과 -> Throttling (감속)           |
|   파드는 살아있음, 응답만 느려짐                       |
|                                                       |
|  [Memory 초과]                                        |
|   limits.memory: 512Mi 초과 -> OOM Killed (즉사)       |
|   SIGKILL -> CrashLoopBackOff 무한 루프                |
|                                                       |
|  왜 즉사? -> 메모리는 "빌린 뒤 반환 불가"              |
|  방치 시 -> 노드 전체 RAM 소진 -> 동반 질식사           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: CPU 초과는 고속도로에서 서행(Throttling)하는 것이고, 메모리 초과는 밥그릇을 넘겨 먹은 손님을 식당에서 즉시 퇴장(Kill)시키는 것이다. 안 그러면 식당 전체가 굶는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스별 사살 우선순위

| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 클래스 | 조건 | 사살 순위 | 비유 |
|:---|:---|:---|:---|
| **BestEffort** | requests·limits 미지정 | **1순위 (최우선 사살)** | 무임승차 승객 |
| **Burstable** | requests < limits | **2순위** | 얌체 고무줄 승객 |
| **Guaranteed** | requests == limits | **최후 생존** | 1등석 정가 승객 |

### Java JVM [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 90% 원인

Java [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 OOM의 주범인 이유: JVM은 자신이 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 안에 갇힌 줄 모르고 <strong>노드 전체 RAM(32GB)</strong>을 자기 것으로 착각하여 Heap을 무한 확장한다. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) limits(512MB)를 넘는 순간 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed.

**해결**: `-XX:MaxRAMPercentage=75.0` 옵션으로 JVM Heap을 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) limits의 75%로 제한한다.

- **📢 섹션 요약 비유**: 50cm 어항([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))에 상어(JVM)를 넣으면 유리를 깨고 죽는다. 유전자 조작(-Xmx)으로 금붕어 체질로 만들어야 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | CPU Throttling | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed |
|:---|:---|:---|
| **대상 자원** | CPU (시간 분할 가능) | Memory (분할 불가) |
| **초과 시 대응** | 감속 (느려짐) | **즉사 (SIGKILL)** |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/">파드</a> 상태</strong> | Running (느림) | **CrashLoopBackOff** |
| **사용자 영향** | 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 중단</strong> |
| <strong><a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 방법</strong> | 자동 (부하 감소 시) | **재시작 + 원인 수정** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대처 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **즉시**: `kubectl describe pod` -> `Reason: OOMKilled` [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/).
2. **임시**: `limits.memory` 상향 (진통제, 근본 해결 아님).
3. **근본**: Java -> `-XX:MaxRAMPercentage=75.0`, Node.js -> `--max-old-space-size`.
4. **예방**: [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) + Grafana로 메모리 사용률 80% 알림 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/).

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **limits 미지정 (BestEffort)**: DB [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 limits를 안 걸어두면 노드 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 시 1순위 사살 대상.
- **limits 무조건 상향**: [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/) 버그를 방치하고 limits만 올리면 시한폭탄.

---

## Ⅴ. 기대효과 및 결론

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 효과 |
|:---|:---|
| Guaranteed [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) (DB) | 노드 OOM에서도 **최후까지 생존** |
| JVM [Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 제한 | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 발생률 **90% 감소** |
| limits 적정 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 리소스 낭비 없이 **안정 운영** |
| 모니터링 알림 | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 전 **사전 대응** 가능 |

[OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서 가장 빈번한 장애 원인이며, [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2와 K8s Memory [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)(KEP-2570)가 결합하여 더 세밀한 메모리 관리가 가능해지고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/062_cgroups/">cgroups</a></strong> | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer의 기반 기술, 리눅스 자원 격리 |
| <strong>K8s <a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> Class</strong> | Guaranteed·Burstable·BestEffort 사살 우선순위 |
| <strong>JVM <a href="/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/">Heap</a></strong> | Java [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) OOM의 90% 원인 |
| **CrashLoopBackOff** | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killed 후 재시작 반복 상태 |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/096_vpa_vertical_pod_autoscaler_kubernetes/">Vertical Pod Autoscaler</a></strong> | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 방지를 위한 자동 limits 조정 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[cgroups v1 (2007) — 프로세스별 메모리 제한 도입]
    |
    v
[Docker (2013) — 컨테이너별 메모리 limits 적용]
    |
    v
[K8s QoS Class (2015~) — Guaranteed·Burstable·BestEffort 분류]
    |
    v
[cgroups v2 + Memory QoS (2022~) — 세밀한 메모리 보호]
    |
    v
[현재: VPA + KEP-2570 — 자동 limits 튜닝 + 메모리 QoS]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 식당에서 밥그릇(512MB) 1개만 먹으라고 했는데, 욕심쟁이 손님([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))이 밥통을 통째로 먹으려 했어요.
2. 경비원([OOM Killer](/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/))이 즉시 그 손님을 쫓아냈어요. 안 그러면 다른 100명의 손님이 굶어요!
3. 해결법은 욕심쟁이 손님에게 "밥 1그릇만 먹는 체질(-Xmx)"로 바꿔주는 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 109 / 371

<- **이전**: [109. K8s 멀티 클러스터 및 연합(Federation) - Karmada·클라우드 버스팅](/studynote/13_cloud_architecture/02_iaas_paas_saas/109_multi_cluster_federation_karmada_cloud_bursting/)
**다음**: [111. 컨테이너 런타임 샌드박싱 - gVisor·Kata Containers·런타임 보안 격리](/studynote/13_cloud_architecture/02_iaas_paas_saas/111_container_runtime_sandboxing_gvisor_kata_containers/) ->

---
