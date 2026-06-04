---
title: "101. K8s 보안 - 서비스 어카운트 (ServiceAccount) 및 RBAC 권한"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/))와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트 (ServiceAccount)는 클러스터 내외부의 주체(사용자 및 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))가 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버에 어떤 작업을 할 수 있는지 통제하는 권한 부여 메커니즘이다.
> 2. **가치**: [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))마다 최소한의 권한만 부여된 독립적인 신분증을 발급하여, 단일 애플리케이션 취약점이 클러스터 전체의 탈취로 이어지는 보안 사고(Blast [Radius](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 확산)를 차단한다.
> 3. **판단 포인트**: 편리함을 위해 기본(Default) 토큰을 방치하거나 ClusterRole을 남발하는 것은 시한폭탄과 같으므로, 반드시 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 단위의 격리와 명시적인 RoleBinding을 원칙으로 삼아야 한다.

---

## Ⅰ. 개요 및 필요성

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트 (ServiceAccount)는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)에서 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))와 같은 애플리케이션 프로세스가 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버와 통신할 때 사용하는 기계용 신분증이다. [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/))는 이 신분증을 가진 주체가 특정 자원(Resource)에 대해 어떤 행동(Verb)을 할 수 있는지를 정의하고 연결하는 프레임워크다.

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 초기나 설정이 미흡한 환경에서는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)될 때마다 기본적으로 막강한 권한을 가진 디폴트 토큰이 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 내부에 자동 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)(Auto-mount)된다. 만약 해커가 웹 서버 취약점을 통해 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 내부에 침투하면, 이 탈취한 토큰을 이용해 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버에 "모든 비밀번호([Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)) 조회"나 "다른 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 삭제"를 요청할 수 있다. 이러한 내부자 위협과 권한 탈취를 원천 차단하기 위해, 애플리케이션의 역할에 맞는 깡통 신분증을 만들고 필요한 권한만 정확히 부여하는 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) 체계가 필수적이다.

- **📢 섹션 요약 비유**: 회사에 비유하면 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버는 사장님 비서실이다. 신입사원([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))이 입사했는데, 아무 설정도 안 하면 비서실 프리패스 권한이 있는 마스터키(디폴트 토큰)를 목에 걸어주는 셈이다. RBAC는 사원증 색깔을 다르게 해서 "너는 1층 화장실만 가라"고 통제하는 보안 게이트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) 아키텍처는 "누가(Subject)", "어떤 자원에(Resource)", "어떤 행동을(Verb)" 할 수 있는지를 분리하여 정의하고, 이를 묶어주는(Binding) 3단 구조로 작동한다.

| 구성 요소 | 역할 설명 | 실무 예시 |
| :--- | :--- | :--- |
| **Subject** (주체) | 권한을 부여받는 대상 | User(사람), Group, **ServiceAccount(기계)** |
| **Role** (역할) | 자원에 대한 접근 권한(허용 규칙)의 모음 | "[Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 목록 보기(Get/List)", "[Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)" |
| **RoleBinding** (연결) | 주체(Subject)와 역할(Role)을 결합 | "ServiceAccount A에게 Role B를 부여하라" |

```text
+--------------------------------------------------------------+
|                  K8s RBAC 권한 부여 메커니즘                 |
+--------------------------------------------------------------+
|  [Subject]                         [Role]                    |
| ServiceAccount (Pod 신분증)        API Resources (Pod, SVC)  |
|       |                              ^    Verbs (Get, List)  |
|       |                              |                       |
|       +---------> [RoleBinding] ------+                       |
|                 (둘을 연결하는 결재 서류)                      |
|                                                              |
| API Server: "요청이 들어왔다. Binding을 확인해 허용/차단 판정!"|
+--------------------------------------------------------------+
```

이 그림이 보여주듯, 권한(Role)과 신분증(ServiceAccount)은 완전히 독립적으로 존재하며, RoleBinding을 통해서만 결합된다. [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 띄울 때 `spec.serviceAccountName`을 명시하면 해당 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 지정된 신분증을 지니게 되고, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버는 RoleBinding을 조회하여 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 요청을 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))하거나 거부(403 Forbidden)한다.

- **📢 섹션 요약 비유**: Role은 "총기 사용, 탱크 운전"이 적힌 행동 매뉴얼이고, ServiceAccount는 "김이병, 박대장"이라는 군번줄이다. RoleBinding은 사령관이 "김이병에게 소총 사격 권한을 부여한다"고 도장을 찍어주는 임명장이다.

---

## Ⅲ. 비교 및 연결

RBAC를 정확히 이해하기 위해서는 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 단위의 권한과 클러스터 전체의 권한을 구분해야 한다.

| 비교 항목 | Role & RoleBinding | ClusterRole & ClusterRoleBinding |
| :--- | :--- | :--- |
| **적용 범위** | 특정 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) ([Namespace](/studynote/02_operating_system/01_overview_architecture/061_namespace/)) 내부 | 클러스터 (Cluster) 전체 |
| **통제 자원** | Pods, Services, Deployments | Nodes, PersistentVolumes, 모든 NS의 자원 |
| **보안 위험도** | 낮음 (격리됨) | 매우 높음 (탈취 시 치명적) |
| **주요 사용처** | 특정 부서의 앱 배포, 모니터링 알바 | [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/) Controller, [CNI](/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인, 클러스터 관리자 |

Role은 101동 내부에서만 유효한 권한이므로, `dev` [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)의 Role을 가진 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 `prod` [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)의 자원을 건드릴 수 없다. 반면, ClusterRole은 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 벽을 허물고 노드 자체를 조작할 수 있는 권한이므로, 이 권한이 부여된 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 해킹되면 클러스터가 통째로 장악된다. 이 개념은 클라우드의 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/studynote/12_it_management/05_security_compliance/1013_management/))이나 리눅스의 sudoers 권한 분리와도 직접적으로 연결된다.

- **📢 섹션 요약 비유**: Role이 "우리 동네 파출소장" 발령장이라면, ClusterRole은 "전국을 휘젓고 다니는 FBI 요원" 발령장이다. FBI 배지를 아무 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에게나 주면 클러스터가 위험해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

운영 환경에서 K8s를 설계할 때, 편의성을 위해 최고 권한을 남용하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)을 가장 경계해야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 판단 기준
1. **디폴트 토큰 차단**: 모든 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)의 `default` [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트에는 권한을 비워두고, [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 템플릿에 `automountServiceAccountToken: false`를 설정하여 불필요한 토큰 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)를 원천 차단해야 한다.
2. **최소 권한의 원칙**: "필요할지도 모른다"는 이유로 `*` (와일드카드) 권한을 남발하지 마라. 읽기 전용(Get, List)이 필요한 모니터링 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에게 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Create, Delete) 권한을 주는 것은 보안 결함이다.
3. <strong>명시적 <a href="/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a> 할당</strong>: [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 배포할 때는 반드시 해당 애플리케이션 전용으로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한 `ServiceAccount`를 매핑하여 역할을 세분화해야 한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) 차트로 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 앱을 설치할 때, 묻지도 따지지도 않고 ClusterRoleBinding을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 매니페스트를 그대로 적용하는 행위.
- [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 파이프라인(예: [Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), ArgoCD)에 클러스터 어드민(cluster-admin) 권한을 통째로 줘버리는 설계.

- **📢 섹션 요약 비유**: 실무 보안은 호텔 방 키를 나눠주는 것과 같다. 청소부에게는 청소할 방의 출입 카드만 줘야지, 마스터키를 주면 언젠가 귀빈실이 털리는 대참사가 일어난다.

---

## Ⅴ. 기대효과 및 결론

RBAC와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트를 통한 엄격한 통제는 시스템의 폭발 반경(Blast [Radius](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/))을 최소화한다. 하나의 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 침해당하더라도, 해당 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에 부여된 권한만큼만 피해를 입고 클러스터 전체의 붕괴로는 이어지지 않는다. 또한 누가 어떤 자원에 접근할 수 있는지 명확해져 오딧([Audit](/studynote/12_it_management/05_security_compliance/363_audit/)) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 분석과 컴플라이언스 대응이 쉬워진다.

다만, 권한 설정이 복잡해질수록 관리 오버헤드가 증가하고, 개발자가 "권한이 없어서 안 뜬다"고 불평할 때마다 예외 처리를 해줘야 하는 한계가 있다. 그럼에도 불구하고 "모든 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 잠재적인 공격 벡터"라는 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) 관점에서, 촘촘하게 설계된 RBAC는 안전한 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 운영을 위한 대체 불가능한 필수 방어선이다.

- **📢 섹션 요약 비유**: 튼튼한 금고([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)) 안에 돈을 넣었다고 끝이 아니다. 금고 안에서도 서랍마다 자물쇠([RBAC](/studynote/09_security/11_iam_access_control/569_rbac/))를 달아놔야, 좀도둑이 들어와도 만 원짜리 한 장만 잃고 끝날 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> Server (kube-apiserver)</strong> | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) 규칙을 최종적으로 검사하고 승인/거부하는 K8s의 심장 |
| <strong><a href="/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/">OIDC</a> / Dex</strong> | 사람(User)의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 K8s 외부의 사내 AD/구글 계정과 연동하는 기술 |
| **Admission Controller** | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) 통과 후에도 요청의 내용을 한 번 더 뜯어보고 필터링하는 검문소 |
| <strong><a href="/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a></strong> | 내부 네트워크망에 들어와 있는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)조차도 믿지 않고 권한을 검증하는 철학 |

### 📈 관련 키워드 및 발전 흐름도

```text
기본 제공 마스터키의 남용 (보안 취약점)
    |
    v
ServiceAccount (기계용 신분증 분리)
    |
    v
RBAC (Role-Based Access Control 도입)
    |
    v
최소 권한의 원칙 (Least Privilege) 적용
    |
    v
네트워크 정책(NetworkPolicy)과 결합한 입체적 방어망 구성
```

이 흐름도는 "[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 부재 -> 신분증 도입 -> 권한 세분화 -> 최적화 -> 다계층 보안 방어"로 발전하는 K8s 클러스터 내부 보안의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 마을에는 '[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트'라는 로봇용 출입증이 있어요.
2. 예전에는 모든 로봇에게 모든 문이 열리는 만능 키를 줘서 도둑이 로봇을 조종하면 마을이 엉망이 됐어요.
3. 이제는 RBAC라는 규칙을 통해 로봇마다 꼭 필요한 방 문만 열리도록 열쇠의 모양을 다르게 깎아준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 371

<- **이전**: [100. CNI (Container Network Interface) - 파드 간 오버레이 통신 표준](/studynote/13_cloud_architecture/02_iaas_paas_saas/100_cni_container_network_interface_flannel_calico/)
**다음**: [102. 컨피그맵 (ConfigMap) / 시크릿 (Secret) - K8s 환경 변수 주입 객체](/studynote/13_cloud_architecture/02_iaas_paas_saas/102_configmap_secret_kubernetes_12_factor_app/) ->

---
