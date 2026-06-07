---
title: "Configmap Secret Kubernetes 12 Factor App"
date: "2026-04-10"
tags:
  - "studynote-cloud-architecture"
weight: 102
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨피그맵 (ConfigMap)과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) ([Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 애플리케이션의 소스코드 및 이미지와 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 데이터를 물리적으로 분리하여 주입하는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) ([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))의 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 관리 객체다.
> 2. **가치**: 12-Factor App의 "[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)과 코드 분리" 원칙을 실현하여, 하나의 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지를 여러 환경(개발, 스테이징, 운영)에서 재빌드 없이 재사용할 수 있는 불변성 (Immutability)을 보장한다.
> 3. **판단 포인트**: 일반 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)값은 컨피그맵에, 비밀번호 및 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 키는 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)에 보관하며, 변경 사항의 실시간 반영이 필요하다면 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) 주입 대신 볼륨 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) ([Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) [Mount](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)) 방식을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

컨피그맵 (ConfigMap)과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) ([Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))은 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경에서 애플리케이션이 필요로 하는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 정보와 민감한 데이터를 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 외부에서 보관하고 전달하는 핵심 리소스다. 이들은 애플리케이션 소스코드나 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) ([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 이미지 안에 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 주소나 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키를 직접 타이핑하는 하드코딩 (Hard-coding) 관행을 없애기 위해 등장했다.

만약 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)값이 이미지 내부에 하드코딩되어 있다면, 환경이 바뀔 때마다 (예: 개발망 -> 운영망) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지를 매번 새로 빌드해야 한다. 이는 배포 속도를 늦추고 이미지 관리의 복잡성을 극대화하며, 소스코드 저장소에 비밀번호가 노출되는 심각한 보안 사고를 유발한다. 컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 이러한 환경 종속성을 제거하여, 동일한 이미지를 여러 환경에서 그대로 실행할 수 있는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) ([Cloud Native](/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) 아키텍처의 필수 요건을 완성한다.

- **📢 섹션 요약 비유**: 로봇 장난감([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지) 안에 건전지([설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)값)를 아예 납땜해 버리면 건전지가 다 닳았을 때 로봇을 부수고 새로 만들어야 합니다. 컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 언제든 열어서 새 건전지로 갈아 끼울 수 있는 '건전지 덮개' 역할을 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 Key-Value 쌍으로 데이터를 저장하며, [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) ([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))가 생성될 때 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) (ENV) 또는 볼륨 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) ([Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) [Mount](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)) 형태로 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 내부에 주입된다. [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)의 경우 추가적으로 데이터를 Base64로 인코딩하여 저장하며, 노드의 디스크가 아닌 휘발성 메모리 (tmpfs)에 저장되어 보안을 강화한다.

```text
+--------------------------------------------------------------+
|       쿠버네티스 파드 설정 주입 아키텍처 (Config Injection)       |
+--------------------------------------------------------------+
|                                                              |
|  [ConfigMap] (일반 텍스트)       [Secret] (Base64 인코딩)    |
|  DB_PORT=3306                 DB_PASS=cGFzc3dvcmQ=           |
|       |                              |                       |
|       | (주입 방식 선택)             | (메모리 기반 마운트)  |
|       v                              v                       |
|  +----------------- 파드 (Pod) ---------------------------+  |
|  |                                                        |  |
|  | 1. 환경 변수 (ENV): OS 환경 변수로 일회성 로드         |  |
|  | 2. 볼륨 마운트 (Volume Mount): /etc/config/ 파일 연결  |  |
|  |                                                        |  |
|  | ----------> [컨테이너 프로세스 실행] <-----------        |  |
|  +--------------------------------------------------------+  |
+--------------------------------------------------------------+
```

위 다이어그램은 외부에 저장된 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 데이터가 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 내부로 전달되는 흐름을 보여준다. [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/) 방식은 주입이 간단하지만 런타임에 동적으로 값을 업데이트할 수 없고, 볼륨 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 방식은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 형태로 제공되어 값이 변경되면 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 재시작 없이도 실시간 갱신 (Hot Reload)이 가능하다는 차이가 있다.

| 주입 방식 | 특징 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| <strong><a href="/studynote/02_operating_system/02_process_thread/156_environment_variables/">환경 변수</a> (ENV)</strong> | OS 전역 변수로 할당 | 접근이 직관적, [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 단순 | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 재시작 전까지 값 갱신 불가 |
| <strong>볼륨 <a href="/studynote/02_operating_system/09_file_system/516_mount_mechanism/">마운트</a> (<a href="/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/">Volume</a>)</strong> | 특정 디렉터리에 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 저장 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경 시 자동 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 가능 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 접근 로직 필요 |

- **📢 섹션 요약 비유**: [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/)는 출근 첫날 사원증에 직급을 적어주는 것과 같아 승진하면 사원증([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))을 새로 발급받아야 하고, 볼륨 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)는 온라인 사내 게시판과 같아서 규정이 바뀌면 언제든 새로고침하여 최신 정보를 읽을 수 있습니다.

---

## Ⅲ. 비교 및 연결

[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)값을 다루는 두 객체인 컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 용도와 저장 방식에서 뚜렷한 경계를 가진다.

| 항목 | 컨피그맵 (ConfigMap) | [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) ([Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)) |
| :--- | :--- | :--- |
| **주요 용도** | 일반 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (URL, [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), [테마](/studynote/04_software_engineering/03_design_architecture/184_theme_agile_requirements/) 등) | 민감 정보 (비밀번호, 토큰, [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서) |
| **저장 형식** | 일반 텍스트 (Plain Text) | Base64 인코딩 |
| **저장 위치** | 노드 디스크 및 [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) | 노드 휘발성 메모리 (tmpfs) 및 [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) |
| **접근 제어** | 일반적인 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 권한 | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/))로 엄격 통제 |

단순히 Base64 인코딩만으로 안전해지는 것은 아니므로, [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 RBAC를 통해 접근 권한을 제한하고, 필요시 외부 암호화 솔루션 (예: HashiCorp [Vault](/studynote/09_security/11_iam_access_control/567_vault/))이나 클라우드 제공자 ([KMS](/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/))와 연동하여 [etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 레벨에서의 암호화 ([Encryption at Rest](/studynote/09_security/16_data_privacy/834_encryption_at_rest/))를 추가로 적용해야 한다.

- **📢 섹션 요약 비유**: 컨피그맵은 냉장고에 붙여둔 "장보기 목록"처럼 누구나 봐도 상관없는 메모장이고, [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 비밀번호를 적어 금고에 넣어둔 "보안 카드"와 같아서 인가된 사람만 메모리에서 꺼내 볼 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 설계할 때는 "[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경 시 애플리케이션이 어떻게 반응할 것인가"와 "보안 사고를 어떻게 방지할 것인가"를 기준으로 판단해야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong><a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>: ConfigMap이 변경되었을 때 애플리케이션이 이를 감지하여 런타임에 핫 리로드 (Hot Reload)를 수행하는가? (스프링 부트의 Actuator 등 연동)
2. **권한 최소화**: Secret에 접근할 수 있는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트 ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Account) 권한이 최소한으로 부여되어 있는가?
3. **암호화 확장**: etcd에 저장된 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)이 정지 상태 (At [Rest](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/))에서 암호화되어 관리되고 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 소스코드나 `Dockerfile` 내부에 직접 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 비밀번호를 작성하는 행위
- Secret을 [환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/)(ENV)로만 주입하여 애플리케이션 크래시 로그에 패스워드가 노출되게 만드는 설계
- 하나의 거대한 ConfigMap에 모든 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 몰아넣어 의존성과 장애 반경을 키우는 구조

- **📢 섹션 요약 비유**: 은행 문을 열 때 모든 직원에게 마스터키를 주지 않듯이, 각 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에는 자신이 꼭 필요한 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(ConfigMap)과 비밀번호([Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))만 볼 수 있도록 권한을 쪼개어 전달해야 안전합니다.

---

## Ⅴ. 기대효과 및 결론

컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 도입하면 코드와 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)의 라이프사이클이 완벽히 분리된다. 이를 통해 [12-Factor App](/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/) 원칙을 준수하는 무결점의 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지를 생성할 수 있으며, 개발, 스테이징, 운영 환경 간의 이식성 (Portability)을 극대화할 수 있다.

하지만, [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 자체의 Base64 인코딩은 암호화가 아닌 [난독화](/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/) 수준이므로 이를 과신해서는 안 된다. 대규모 엔터프라이즈 환경에서는 외부 비밀값 관리 도구 (External Secrets [Operator](/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/) 등)를 연동하는 중앙 집중형 보안 관리가 필수적이다. 결론적으로 이 두 객체는 단순한 변수 전달 도구를 넘어, [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 시스템에서 환경 종속성을 끊어내는 가장 핵심적인 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층이다.

- **📢 섹션 요약 비유**: 무대에서 배우(이미지)는 똑같은 연기를 하지만, 컨피그맵과 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)이라는 조명과 배경막을 어떻게 바꿔 달아주느냐에 따라 낮 장면이 되기도 하고 밤 장면이 되기도 하는 완벽한 무대 장치입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/">12-Factor App</a></strong> | 코드와 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 분리하여 환경 이식성을 높이는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 설계 원칙 |
| <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">불변 인프라</a> (<a href="/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">Immutable Infrastructure</a>)</strong> | 한 번 생성된 이미지를 변경하지 않고 배포하는 개념으로, [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 분리가 필수적 |
| <strong><a href="/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a> (<a href="/studynote/09_security/11_iam_access_control/569_rbac/">Role-Based Access Control</a>)</strong> | [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 객체에 무단으로 접근하지 못하도록 통제하는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 권한 관리 시스템 |
| <strong>볼륨 <a href="/studynote/02_operating_system/09_file_system/516_mount_mechanism/">마운트</a> (<a href="/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/">Volume</a> <a href="/studynote/02_operating_system/09_file_system/516_mount_mechanism/">Mount</a>)</strong> | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경 시 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 재시작 없이 최신 값을 실시간으로 반영하기 위한 연결 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
하드코딩 (Hard-coding)
    |
    v
환경 변수 (OS ENV) 분리 · 12-Factor App
    |
    v
ConfigMap · Secret (쿠버네티스 네이티브 설정 주입)
    |
    v
볼륨 마운트 (Volume Mount) · 핫 리로드 (Hot Reload)
    |
    v
External Secrets Operator · KMS (Key Management Service) 연동
```

### 👶 어린이를 위한 3줄 비유 설명
1. 장난감 로봇(프로그램)을 만들 때, 건전지([설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)값)를 아예 로봇 안에 본드로 붙여버리면 나중에 고장이 나요.
2. 컨피그맵은 로봇 등 뒤에 일반 건전지를 꽂는 '투명한 배터리 통'이에요.
3. [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)은 아무나 열어볼 수 없게 자물쇠가 달린 '비밀 배터리 통'이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 101 / 371

<- **이전**: [101. K8s 보안 - 서비스 어카운트 (ServiceAccount) 및 RBAC 권한](/studynote/13_cloud_architecture/02_iaas_paas_saas/101_serviceaccount_rbac_kubernetes_authorization/)
**다음**: [103. 헬름 (Helm) - 쿠버네티스 패키지 매니저 및 템플릿 엔진](/studynote/13_cloud_architecture/02_iaas_paas_saas/103_helm_kubernetes_package_manager_chart_template/) ->

---
