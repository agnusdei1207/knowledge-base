+++
title = "95. 시크릿 매니저 (Secret Manager)"
date = 2026-03-04

[taxonomies]
tags = ["cicd", "devsecops", "studynote-devops-sre"]

[extra]
tags = ["cicd", "devsecops", "studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저 ([Secret](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) Manager)는 애플리케이션의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 정보(DB 패스워드, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키, [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 등)를 소스코드와 분리하여 중앙 집중식으로 암호화 저장하고 배포하는 보안 인프라다.
> 2. **가치**: 코드 유출 시에도 핵심 자격 증명이 노출되는 것을 막고, 동적 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 발급과 자동 순환(Rotation)을 통해 영구적인 해킹 위험을 근본적으로 제거한다.
> 3. **판단 포인트**: [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 단순한 [키-값 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/036_key_value/)가 아니며, 애플리케이션(또는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))이 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 요청할 때 어떻게 신원을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/))할 것인지에 대한 강력한 접근 제어([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) 설계가 동반되어야 한다.

---

## Ⅰ. 개요 및 필요성

[시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저 ([Secret](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) Manager)는 시스템 접근에 필요한 민감 정보(Secrets)의 생명주기를 통제하고, 실행 시점에만 이를 안전하게 주입해 주는 보안 솔루션이다. HashiCorp [Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/), AWS Secrets Manager, Azure [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/) 등이 대표적이다.

이 개념이 등장한 배경은 '하드코딩의 저주' 때문이다. 과거에는 편의를 위해 소스코드 저장소(Git)나 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(YAML)에 평문으로 비밀번호를 적어두었고, 이는 소스코드 유출이 곧 전체 시스템 탈취로 이어지는 최악의 대형 사고를 유발했다. 이를 막기 위해 [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)로 빼내는 시도를 했으나, [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/) 역시 메모리 덤프나 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 노출될 위험이 컸다. 결국 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 완전히 분리 보관하고, 호출하는 주체를 철저히 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한 뒤에만 암호화된 터널로 잠시 빌려주는 전문적인 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저가 DevSecOps의 필수 요소가 되었다.

- **📢 섹션 요약 비유**: [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 집 문 열쇠(비밀번호)를 현관 매트 아래(소스코드) 숨겨두는 짓을 그만두고, 튼튼한 은행 금고에 맡긴 뒤 필요할 때만 신분증을 보여주고 잠시 빌려 쓰는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저의 핵심 원리는 '강력한 암호화 저장'과 '철저한 신원 기반의 접근 제어'다. 클라이언트([파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인)가 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 요청하면, [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 토큰이나 클라우드 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 권한을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 뒤 복호화하여 전달한다.

| 핵심 기능 | 작동 원리 | 보안적 이점 |
| :--- | :--- | :--- |
| <strong>정적 <a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/">시크릿</a> (Static Secrets)</strong> | [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value 형태의 고정된 비밀번호를 KMS를 통해 디스크에 암호화 보관 | 평문 저장 방지 ([Encryption at Rest](/knowledge-base/studynote/09_security/16_data_privacy/834_encryption_at_rest/)) |
| <strong>동적 <a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/">시크릿</a> (Dynamic Secrets)</strong> | 요청 즉시 짧은 [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)(만료 시간)을 가진 일회용 DB 계정을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 반환 | 자격 증명 유출 시 피해 시간 최소화 |
| **자동 순환 (Auto Rotation)** | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)된 주기(예: 30일)마다 백엔드 DB의 비밀번호를 스스로 변경 | 사람의 개입 및 실수 배제 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 로깅 (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/">Audit</a> <a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/526_security_logging_and_monitoring_failures/">Logging</a>)</strong> | "누가, 언제, 어떤 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 열람했는지" 상세 이력 기록 | 침해 사고 발생 시 완벽한 추적 가시성 제공 |

```text
┌──────────────────────────────────────────────────────────────┐
│           시크릿 매니저의 작동 흐름: K8s 파드 요청 시       │
├──────────────────────────────────────────────────────────────┤
│ 1. [K8s Pod 구동] ─▶ ServiceAccount 토큰 제시 ─▶ [Vault/ASM]│
│                                                     │        │
│ 2. [Vault/ASM] ─▶ 신원(RBAC) 검증 후 KMS 마스터키로 복호화   │
│                                                     │        │
│ 3. [Vault/ASM] ─▶ 메모리(tmpfs)에 안전하게 시크릿 주입 ─▶ Pod│
└──────────────────────────────────────────────────────────────┘
```

특히 백엔드 저장소는 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 키로 암호화되어 있어, 설령 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저의 디스크 자체가 통째로 털려도 공격자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽을 수 없다.

- **📢 섹션 요약 비유**: 은행 금고([시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저)는 아무나 열어주지 않는다. 지문 인식(신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))을 통과하면 금고 안의 진짜 열쇠를 복사해서 주는데, 이 복사된 열쇠(동적 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))는 10분 뒤에 스스로 녹아 없어진다.

---

## Ⅲ. 비교 및 연결

[시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 관리하는 방식은 인프라 성숙도에 따라 세 가지 레벨로 나눌 수 있으며, 이 차이는 해킹 발생 시의 파급력 차이로 직결된다.

| 항목 | 일반 [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/) (.env) | K8s Native Secrets | 전용 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저 ([Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/) 등) |
| :--- | :--- | :--- | :--- |
| **저장 방식** | 평문 노출 (위험) | Base64 인코딩 (암호화 아님) | [KMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/) 기반 초강력 암호화 |
| **생명 주기** | 수동 변경 필수 | 수동 변경 필수 | 동적 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 및 자동 순환 ([TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/">Audit</a>)</strong> | 추적 불가능 | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 제한적 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 모든 열람 기록의 중앙화된 로깅 |
| **적용 범위** | 단일 애플리케이션 | 단일 K8s 클러스터 내부 | [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/), [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 통합 통제 |

[쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 기본 [Secret](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 객체는 암호화가 아닌 단순 인코딩에 불과하여 [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 저장소가 털리면 그대로 노출된다. 반면 전용 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) 환경 전체를 아우르는 중앙 집중형 보안 컨트롤 타워 역할을 수행한다.

- **📢 섹션 요약 비유**: [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)는 일기장에 비밀번호를 적어두는 것이고, K8s Secret은 거꾸로 적어두는 것(금방 풀림)이며, [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 진짜 강철 금고에 넣어두는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저를 도입할 때 가장 큰 장벽은 '애플리케이션 코드 수정'과 '[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(Auth) 과정의 복잡성'이다. 이를 우회하면서도 강력한 보안을 챙기기 위한 아키텍처 판단이 필수적이다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **코드 비침투적 주입**: 애플리케이션이 [Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/) API를 직접 호출하도록 코드를 수정하는 대신, [Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/) Agent Injector나 External Secrets [Operator](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/)(ESO)를 활용하여 [컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/)에 메모리로 밀어 넣는 방식을 채택했는가?
2. <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>/CD <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인 <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong>: GitHub Actions나 [Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) 스크립트 내부에 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 하드코딩하지 않고, [OIDC](/knowledge-base/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/)([OpenID Connect](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/548_openid_connect/)) 연합을 통해 배포 시점에 임시 토큰을 교환하는 구조인가?
3. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/182_network_separation_model/">망분리</a> 및 HA 구성</strong>: [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저 자체가 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))가 되지 않도록 고가용성(High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 클러스터로 묶여 있고, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 철저한가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 중요도가 떨어지는 일반 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)([Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))까지 비싼 호출 비용을 지불하며 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저에 전부 때려 넣기 (AWS Parameter Store와 분리 필요)
- [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저에 접속하기 위한 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 토큰(Root Token)을 다시 소스코드나 슬랙에 공유해버리는 촌극

- **📢 섹션 요약 비유**: 튼튼한 금고를 사놓고 정작 금고 비밀번호를 포스트잇에 적어 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)에 붙여둔다면 아무 소용이 없다. 시스템 설계 자체가 비밀번호를 서로 공유하지 않는 구조여야 한다.

---

## Ⅴ. 기대효과 및 결론

[시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저의 도입은 소스코드 유출(Git 해킹)이 발생하더라도 실질적인 시스템 침해나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출로 이어지지 않게 막아주는 최후의 방어선([Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/))이다. 또한 인간의 개입 없이 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서와 비밀번호가 자동으로 갱신되므로 운영 피로도가 극적으로 줄어든다.

미래의 클라우드 인프라는 어떠한 고정된 비밀번호도 허용하지 않는 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">제로 트러스트</a>(<a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a>)</strong> 모델로 완전히 넘어갈 것이다. [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 단순히 패스워드를 저장하는 곳을 넘어, 애플리케이션 간의 신뢰를 동적으로 중재하고 만료시키는 "클라우드 보안의 심장"으로 기억해야 한다.

- **📢 섹션 요약 비유**: 완벽히 셋팅된 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저 환경에서는 도둑이 현관문 열쇠를 복사해 가도, 도착해 보면 이미 자물쇠 자체가 매시간 자동으로 바뀌어 있어 영원히 집에 들어갈 수 없다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [KMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/) ([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화할 때 사용하는 최상위 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 암호키 관리 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) (역할 기반 접근 제어) | 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 어떤 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 폴더에 접근할 수 있는지 결정하는 권한 통제 체계 |
| External Secrets [Operator](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/) (ESO) | 외부 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저의 값을 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 내부 리소스로 안전하게 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)해 주는 도구 |
| 동적 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) (Dynamic Secrets) | 미리 만들어진 비밀번호를 꺼내주는 게 아니라 요청 시마다 1회용 계정을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
평문 하드코딩 (.env 및 소스코드 노출 위험)
    │
    ▼
K8s Native Secrets (단순 Base64 인코딩, 파편화 한계)
    │
    ▼
전용 시크릿 매니저 (Vault, KMS 연동 정적 시크릿 암호화)
    │
    ▼
동적 시크릿 (Dynamic Secrets) 및 자동 순환 (Auto Rotation)
    │
    ▼
제로 트러스트 (Zero Trust) 기반 OIDC 연합 및 통합 인증 보안
```

이 흐름도는 "평문 노출 → 단순 [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/) → 중앙 집중 암호화 → 일회성/동적 발급 → 무신뢰 아키텍처"로 개념이 강화되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 매니저는 우리 집의 귀중한 열쇠(비밀번호)들을 아무 데나 두지 않고 아주 튼튼한 마법의 <strong>강철 금고</strong>에 보관하는 곳이에요.
2. 문을 열어야 할 때는 가족이나 허락받은 로봇에게만 딱 한 번 쓰고 버려지는 <strong>일회용 열쇠</strong>를 만들어 줘요.
3. 그래서 나쁜 도둑이 예전 열쇠를 훔쳐 가더라도, 이미 자물쇠가 바뀌어 있어서 절대로 문을 열 수 없게 막아준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 95 / 373

← **이전**: [94. 파이프라인 보안 락인 (Pipeline Security)](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/094_pipeline_security_lock_in_ci_cd/)
**다음**: [96. K8s Sealed Secrets - GitOps 시크릿 암호화 관리](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/096_k8s_sealed_secrets_gitops_encryption/) →

---
