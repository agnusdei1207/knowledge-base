+++
title = "84. 컨테이너 런타임 (Container Runtime) - 파드 구동의 심장 containerd"
date = 2026-04-10

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/)은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 실제로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·시작·정지·삭제하는 실행 계층이고, 오케스트레이션과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 사이의 중간 다리다.
> 2. **가치**: containerd는 수명주기와 이미지/[스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)을 관리하고, runc는 [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) 규격에 맞춰 프로세스를 띄우며, CRI는 kubelet이 런타임과 대화하는 표준 인터페이스를 제공한다.
> 3. **판단 포인트**: 문제가 생기면 '[쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 안 된다'고 말하기보다 [kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/), CRI, containerd, [runc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/), [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 순서로 경로를 쪼개 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/)은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 실제로 실행하는 계층이다. [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) ([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), K8s)는 스케줄링과 상태 관리를 맡고, CRI ([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Runtime Interface)는 kubelet이 런타임과 대화하는 표준 인터페이스다. 따라서 런타임은 '[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 어떻게 실행할 것인가'를, 오케스트레이션은 '어느 노드에서 언제 실행할 것인가'를 책임진다.

Docker라는 이름이 널리 쓰이지만, 실제 현장에서는 containerd와 runc의 역할 분리가 더 중요하다. 이미지 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/), [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 수명 관리가 한 덩어리로 섞이면 디버깅이 어려워지기 때문이다.

```text
Pod spec
  |
  v
kubelet
  |  CRI
  v
containerd -- 이미지 / 스냅샷 관리
  |
  v
runc -- OCI bundle --> namespaces / cgroups
  |
  v
Linux kernel start process
```

- **📢 섹션 요약 비유**: 학교에서 담임은 출석과 자리 배치를 관리하고, 실제 의자는 행정실이 준비하며, 학생을 앉히는 손은 반장처럼 따로 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

containerd는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 상태 전환과 이미지 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/), [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), 실행된 프로세스의 수명을 관리한다. runc는 [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) ([Open Container Initiative](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) 규격을 따라 Linux namespace와 cgroup을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하고 실제 프로세스를 fork/exec 한다. containerd-shim은 런타임이 재시작돼도 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 프로세스가 살아 있게 만드는 완충 역할을 한다.

| 구성요소 | 역할 | 장애 시 징후 |
| :--- | :--- | :--- |
| [kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) | 노드 상태와 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 수명 제어 | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 이벤트는 보이는데 실행이 안 됨 |
| CRI | kubelet과 런타임 사이의 표준 계약 | 런타임 교체 시 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 문제 |
| containerd | 이미지·[스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)·[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 수명 관리 | pull / create / start 단계 실패 |
| [runc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) [프로세스 생성](/knowledge-base/studynote/02_operating_system/02_process_thread/104_process_creation/) | [namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) / cgroup 오류 |
| [kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) | 격리와 자원 제한 집행 | 권한·[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기능 부족 |

```text
containerd 는 '무엇을' 실행할지 관리하고
runc 는 '어떻게' 프로세스를 띄울지 처리한다.

즉, 관리와 실행을 분리해 장애 범위를 좁힌다.
```

이 분리는 운영상 중요하다. containerd가 관리 계층이라면 runc는 실행 계층이어서, 둘을 나눠야 이미지 문제와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 문제를 따로 추적할 수 있다. 인터페이스가 표준화될수록 런타임 교체와 보안 패치도 쉬워진다.

- **📢 섹션 요약 비유**: 여행 가방을 챙기는 사람과, 실제로 문 앞까지 들고 가는 사람이 다르면 역할을 나누기 쉽다.

---

## Ⅲ. 비교 및 연결

containerd와 runc는 같은 '런타임'으로 묶여 말하지만, 세밀하게 보면 범위가 다르다. containerd는 데몬 수준에서 이미지와 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 관리하고, runc는 낮은 수준에서 실제 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 프로세스를 만든다. CRI는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 이 둘을 호출하기 위한 계약이고, OCI는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 어떤 규격으로 만들어져야 하는지 정의한다.

| 구분 | 성격 | 주 역할 |
| :--- | :--- | :--- |
| CRI ([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Runtime Interface) | [kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) ↔ runtime 계약 | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 실행 명령 전달 |
| [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) ([Open Container Initiative](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행 규격 | 이미지 / 런타임 표준화 |
| containerd | 상위 런타임 데몬 | 생명주기 관리 |
| [runc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) | 저수준 실행기 | [프로세스 생성](/knowledge-base/studynote/02_operating_system/02_process_thread/104_process_creation/) |

[Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 엔진은 개발자 경험과 빌드·런·푸시를 한 제품에 묶은 반면, containerd와 runc는 운영 계층에 더 가깝다. 그래서 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 플랫폼을 설계할 때는 '도구 이름'보다 '어느 계층을 책임지는가'를 먼저 봐야 한다.

- **📢 섹션 요약 비유**: 차를 사는 것과, 엔진·변속기·브레이크 부품을 따로 관리하는 것은 같은 이동이라도 관리 방식이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/) 문제는 보통 Pod가 멈추거나, 이미지가 안 내려오거나, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 바로 죽는 형태로 드러난다. 이때는 [kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) 이벤트, CRI 통신, containerd [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), runc의 [namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) / cgroup [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 순서로 좁혀야 한다. 무조건 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 문제라고 보기보다, 실패 지점을 계층별로 나누는 것이 핵심이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 노드의 cgroup 드라이버와 런타임 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 일치하는가?
2. 이미지 pull 실패와 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) start 실패를 구분했는가?
3. containerd 재시작 시에도 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 유지되는가?
4. 권한 문제인지 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기능 문제인지 분리했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) CLI로 보이는 증상만 보고 runtime 계층을 구분하지 않는 경우
- build, [registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), runtime 문제를 한 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 뭉뚱그리는 경우
- 런타임 교체 후 CRI [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 검증하지 않는 경우

- **📢 섹션 요약 비유**: 고장 난 집을 볼 때 전등, 배전반, 건물 구조를 따로 확인해야 어디가 문제인지 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

[컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/)의 장점은 실행 경계를 분리해 포터블한 배포와 명확한 장애 분석을 가능하게 하는 데 있다. containerd와 [runc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/), CRI와 OCI의 계층 분리는 '어디서 문제가 나는가'를 빠르게 좁히게 해 준다. 그러나 런타임은 애플리케이션의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 오류나 잘못된 이미지 자체를 해결해 주지는 않는다.

따라서 [컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/)은 '[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 돌리는 엔진'이 아니라 '[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 어떤 규칙으로 돌릴지 정리한 실행 체계'로 기억하는 것이 맞다. 운영의 관점에서는 이 분리가 가장 큰 가치다.

- **📢 섹션 요약 비유**: 좋은 주방은 요리사가 바쁘더라도 [가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/), 칼, 그릇이 어디 있는지 바로 찾을 수 있게 정리돼 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) (K8s) | [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 스케줄링과 상태 관리 |
| CRI ([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Runtime Interface) | kubelet이 런타임과 대화하는 계약 |
| containerd | 이미지·[스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)·수명주기 관리 |
| [runc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) | 실제 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) [프로세스 생성](/knowledge-base/studynote/02_operating_system/02_process_thread/104_process_creation/) |
| [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) ([Open Container Initiative](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 표준 규격 |
| [namespaces](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/700_nvme_namespaces/) / [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) | 격리와 자원 제어의 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
Pod manifest
  |
  v
kubelet
  |  CRI
  v
containerd
  |
  v
runc
  |
  v
Linux kernel / container process
```

흐름을 끊지 않고 계층별로 보면 배포 문제와 실행 문제를 분리할 수 있다.

### 👶 어린이를 위한 3줄 비유 설명

1. 선생님은 누구를 어디에 앉힐지 정해요.
2. 이불을 까는 사람과 실제로 누워 자는 사람은 역할이 달라요.
3. 그래서 준비와 실행을 나누면 문제가 생겨도 어디서인지 찾기 쉬워요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 83 / 371

<- **이전**: [83. Kube-proxy - 노드 내부의 네트워크 라우팅 및 서비스 로드밸런싱 통신 규칙(iptables/IPVS) 설정](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/083_kube_proxy_iptables_ipvs_routing/)
**다음**: [85. Pod (파드) - K8s의 최소 배포 및 스케일링 단위](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) ->

---
