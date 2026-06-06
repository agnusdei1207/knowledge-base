---
title: "Kubernetes Cluster Architecture"
date: "2026-05-01"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터는 제어 평면 (Control Plane)과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane)으로 나뉜 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 시스템이다.
> 2. **가치**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Server, [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/), Scheduler, Controller Manager, Kubelet이 선언적 상태를 유지하며 자동 배치와 self-healing을 수행한다.
> 3. **판단 포인트**: 고가용성 (HA), [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/), [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/), 노드 풀, 리소스 제한이 설계의 핵심이며, 운영 환경에서는 단일 마스터를 피해야 한다.

---

## Ⅰ. 개요 및 필요성

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 수많은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 사람이 직접 관리하기 어렵기 때문에 등장했다. 클러스터 아키텍처는 이러한 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 묶어 배치, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 확장을 자동화하는 구조다. 핵심은 사용자가 원하는 최종 상태를 선언하면 시스템이 그 상태를 계속 유지한다는 점이다.

[클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자주 바뀌고 트래픽도 요동친다. 그래서 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)처럼 자동화된 클러스터 관리가 필요하다.

- **📢 섹션 요약 비유**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터는 항만 관제 시스템과 같다. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 화물선이고, 클러스터는 이 선박들을 자동으로 배치하는 항구다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터는 제어 평면과 워커 노드로 구성된다. 제어 평면은 상태를 결정하고, 워커 노드는 실제 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 실행한다. etcd는 상태 저장소이고, Scheduler는 배치 판단, Controller Manager는 원하는 상태와 실제 상태의 차이를 메운다.

```text
+--------------------------------------------------------------+
|                   Kubernetes Cluster Flow                   |
+--------------------------------------------------------------+
| kubectl -> API Server -> etcd                                 |
|                      -> Scheduler / Controller Manager       |
|                      -> Kubelet -> Container Runtime -> Pod    |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Server | 모든 요청의 접점 | [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/), [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) |
| [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) | 상태 저장 | [Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) 기반 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| Scheduler | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 배치 | 자원, 제약, 어피니티 고려 |
| Controller Manager | 상태 보정 | [desired state](/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/) 유지 |
| [Kubelet](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) | 노드 실행 에이전트 | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)/헬스체크 |
| Kube-proxy | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 네트워킹 | iptables/IPVS |

운영에서 중요한 것은 control plane의 가용성이다. 마스터가 하나면 그 자체가 SPOF가 되므로, HA를 위해 복수 마스터와 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) etcd가 필요하다.

- **📢 섹션 요약 비유**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 지휘자와 연주자로 나뉜 오케스트라 같다. 지휘자가 악보를 바꾸고, 연주자들이 실제 소리를 낸다.

---

## Ⅲ. 비교 및 연결

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 단순한 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행기가 아니다. [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) Swarm보다 유연하고, Mesos보다 생태계가 크며, 전통 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 운영보다 선언적 자동화가 강하다.

| 항목 | 직접 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 운영 | [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) Swarm | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) |
| :--- | :--- | :--- | :--- |
| [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 단위 | [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) |
| 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 낮음 | 중간 | 높음 |
| 생태계 | 전통적 | 제한적 | 매우 큼 |
| 운영 난이도 | 낮음~중간 | 낮음 | 중간~높음 |

또한 관리 방식에 따라 Managed K8s와 자체 구축으로 나뉜다. Managed는 편하지만 제어권이 줄고, 자체 구축은 자유롭지만 운영 복잡도가 커진다.

- **📢 섹션 요약 비유**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 자동 운항이 되는 공항 관제 시스템 같고, 직접 구축은 직접 활주로까지 만드는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 노드 수보다 더 중요한 것이 설계 원칙이다. 마스터 HA, [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 리소스 요청/제한, 네트워크 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 스토리지 클래스, 오토스케일링을 함께 봐야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 마스터 노드가 3대 이상인가?
2. [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 있는가?
3. [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/)/CSI와 Ingress가 표준화되어 있는가?
4. requests/limits와 네임스페이스로 자원을 통제하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단일 마스터로 운영하는 경우
- 리소스 제한 없이 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 몰아넣는 경우
- 네트워크와 스토리지 설계를 나중으로 미루는 경우

기술사 관점에서는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 왜 자동화와 회복력을 제공하는지, 그리고 어디서 복잡성이 생기는지까지 설명해야 한다. 운영은 편해지지만 설계는 더 중요해진다.

- **📢 섹션 요약 비유**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 자동으로 움직이는 물류창고다. 창고가 똑똑할수록 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 설계가 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터는 현대 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 운영의 표준이다. 배포, 확장, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 자동화해 운영 효율을 크게 높이고, 애플리케이션 팀이 코드에 집중하게 만든다.

하지만 자동화가 강할수록 설계와 관측이 중요해진다. 결국 클러스터 아키텍처는 "어떻게 빨리 띄우는가"보다 "어떻게 안정적으로 오래 돌리는가"의 문제다.

- **📢 섹션 요약 비유**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 여러 기계를 자동으로 돌리는 공장 라인이다. 버튼 하나로 움직이지만, 뒤에는 정교한 설계가 필요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Server | 클러스터 진입점 |
| [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) | 상태의 단일 진실 출처 |
| Scheduler | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 배치 |
| [Kubelet](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) | 노드 에이전트 |
| [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) / [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) | 네트워크/스토리지 인터페이스 |

### 📈 관련 키워드 및 발전 흐름도

```text
컨테이너 실행
    |
    v
오케스트레이션
    |
    v
쿠버네티스 제어 평면
    |
    v
워커 노드 / self-healing
    |
    v
멀티 클러스터 / 클라우드 네이티브
```

이 흐름은 단일 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 운영에서 대규모 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 운영으로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)는 장난감 상자를 정리해 주는 아주 똑똑한 정리함이에요.
2. 장난감이 늘어나면 어디에 둘지 알아서 정해 주고, 빠진 장난감도 다시 채워요.
3. 그래서 많은 장난감을 안전하게 같이 놀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 51 / 371

<- **이전**: [51. 벤더 종속 (Vendor Lock-in) - 클라우드 아키텍처의 함정](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)
**다음**: [53. 서비스와 파드 배포 (Service Pod Deployment)](/studynote/13_cloud_architecture/01_virtualization/053_service_pod_deployment/) ->

---
