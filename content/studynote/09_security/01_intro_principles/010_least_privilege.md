+++
title = "10. 최소 권한 원칙 (Principle of Least Privilege) — 필요 알 권리"
description = "보안 위협 최소화 및 횡적 이동 차단을 위한 접근 제어의 근본 철학"
date = 2026-03-25

[taxonomies]
tags = ["security"]

[extra]
tags = ["security"]
+++

# 최소 권한 원칙 (Principle of Least Privilege, PoLP)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 최소 권한 원칙 (PoLP)은 사용자, 프로그램, 또는 프로세스가 주어진 업무나 기능을 수행하는 데 **정확히 필요한 최소한의 정보와 리소스에만, 필요한 시간 동안만** 접근할 수 있도록 권한을 제한하는 보안 설계의 근본 철학이다.
> 2. **가치**: 시스템 침해(계정 탈취, 악성코드 감염)가 발생하더라도, 공격자가 시스템 전체로 퍼져나가는 횡적 이동(Lateral Movement)을 물리적으로 차단하여 <strong>피해 범위(Blast <a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/">Radius</a>)를 극적으로 최소화</strong>한다.
> 3. **융합**: '알 필요성([Need-to-Know](/knowledge-base/studynote/09_security/01_intro_principles/013_need_to_know/))' 및 '[직무 분리](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/)([Separation of Duties](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/))'와 결합되어 [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)/[ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) 같은 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 모델로 구체화되며, 최근 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) 아키텍처와 [JIT](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/) ([Just-In-Time](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/)) 권한 부여의 핵심 기반이 되었다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

- **개념**: 최소 권한 원칙 (PoLP)은 시스템의 모든 개체(Subject: 사용자, 앱, 데몬 등)가 자신의 합법적인 목적을 달성하는 데 필수적인 최소한의 특권(Privilege)만을 가져야 한다는 원칙이다. 이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 시스템 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 메모리 영역 등 모든 자원(Object)에 적용된다.
- **필요성**: 개발 편의성이나 운영의 번거로움 때문에 많은 시스템이 루트(Root)나 관리자(Admin) 등 '과도한 권한(Over-privileged)'을 남발한다. 그러나 권한이 큰 계정 하나가 피싱이나 악성코드에 뚫리면, 공격자는 그 계정의 권한을 이용해 전체 인프라를 장악해버린다. 권한을 최소화하면 뚫려도 해당 계정의 좁은 접근 영역만 피해를 입는다.
- **💡 비유**: 회사 신입사원에게 회사 전체의 마스터키(과도한 권한)를 주지 않고, 오직 자신의 부서 사무실과 본인 책상 서랍만 열 수 있는 사원증(최소 권한)을 주는 것과 같습니다. 만약 사원증을 분실해도 도둑은 사장실이나 금고에 들어갈 수 없습니다.
- **등장 배경**: ① 군사 보안의 '[Need-to-Know](/knowledge-base/studynote/09_security/01_intro_principles/013_need_to_know/)(알 필요성)' 원칙에서 유래 -> ② 다중 사용자 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(Multics, UNIX)의 권한 분리 설계로 발전 -> ③ [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/) 공격의 횡적 이동(Lateral Movement) 방어를 위해 현대 클라우드 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 및 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)의 핵심 교리로 부상.

```text
+--------------------------------------------------------------+
|           과도한 권한(Over-privileged) vs 최소 권한(PoLP) 비교           |
+--------------------------------------------------------------+
|                                                              |
| [과도한 권한 아키텍처 - ⚠ 위험]                                    |
|       공격자 탈취 (마케팅 직원 PC)                                  |
|           |                                                  |
|           v (Admin 권한 보유)                                 |
|   [마케팅 DB] ----(횡적 이동: 권한 남용)-----> [인사 DB], [재무 DB]    |
|   결과: 단 하나의 계정이 뚫려 전체 시스템 장악 및 데이터 대량 유출 발생        |
|                                                              |
|                                                              |
| [최소 권한 원칙 아키텍처 - ✅ 안전]                                   |
|       공격자 탈취 (마케팅 직원 PC)                                  |
|           |                                                  |
|           v (오직 '마케팅 DB Read' 권한만 보유)                   |
|   [마케팅 DB]       [인사 DB] (접근 차단 ✖)    [재무 DB] (접근 차단 ✖)|
|   결과: 해커가 다른 시스템으로 이동(Pivot) 불가. 피해를 마케팅 DB로만 국한.  |
+--------------------------------------------------------------+
```

**[다이어그램 해설]** 이 시각화는 최소 권한 원칙이 왜 '피해 범위(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/)) 최소화'의 핵심인지 극명하게 보여준다. [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/)([지능형 지속 위협](/knowledge-base/studynote/09_security/04_endpoint_security/374_apt/)) 공격자는 최초 침투([Initial Access](/knowledge-base/studynote/09_security/15_malware_attack_vectors/751_initial_access/)) 후 반드시 더 높은 권한을 찾아 내부망을 헤집고 다니는 횡적 이동(Lateral Movement)을 시도한다. PoLP가 적용된 환경에서는 탈취한 계정의 권한이 좁아 공격의 사슬이 끊어지며 방어자가 이상 징후를 탐지할 시간을 벌어준다.

- **📢 섹션 요약 비유**: 큰 배의 밑바닥을 여러 개의 작은 격실(격벽)로 쪼개어 설계하면, 빙산에 부딪혀 한 칸에 물이 차더라도 배 전체가 침몰하지 않고 떠 있을 수 있는 생존 설계와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 최소 권한 구현의 3대 핵심축

| 요소명 | 핵심 개념 및 역할 | 내부 동작 메커니즘 | 실무 적용 기술 | 비유 |
|:---|:---|:---|:---|:---|
| <strong>알 필요성 (<a href="/knowledge-base/studynote/09_security/01_intro_principles/013_need_to_know/">Need-to-Know</a>)</strong> | 업무 수행에 필요한 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(정보)"만 보이게 함 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/)) 등급과 사용자의 취급 [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)(Clearance) 레벨을 비교 | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([강제적 접근 제어](/knowledge-base/studynote/02_operating_system/10_security/579_mac_mandatory_access_control/)), [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/) | 1급 비밀 문서는 장군만 열람 |
| **권한 최소화 (Least Privilege)** | 정보뿐 아니라 "행동(기능, Write/Execute)" 권한을 최소로 제한 | Read-Only, 시간제한, 특정 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 엔드포인트 호출만 허용 | [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)/[ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/), 1인 1계정 통제 | 박물관 관람객은 '보기'만 가능 (만지기 불가) |
| <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/">직무 분리</a> (<a href="/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/">Separation of Duties</a>, SoD)</strong> | 혼자서 중요한 결정을 다 끝내지 못하게 권한을 쪼갬 | 승인자 / 실행자 / 감사자의 역할을 분리하여 상호 견제 (4-Eyes 원칙) | 권한 분할 결재 시스템, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 분리 | 회계팀의 '전표 작성자'와 '송금 결재자' 분리 |

### [JIT](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/) ([Just-In-Time](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/)) [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 기반의 동적 최소 권한 파이프라인

전통적인 PoLP는 "A는 영구적으로 B 권한을 갖는다"는 정적(Static) 할당 방식이었다. 하지만 현대 클라우드 환경에서는 평소에는 '0([Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)) 권한'을 유지하다가, 작업이 필요한 그 순간에만 한시적으로 권한을 부여하고 뺏어버리는 [JIT](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/)([Just-In-Time](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/)) 개념으로 발전했다.

```text
+--------------------------------------------------------------+
|           현대적 최소 권한의 진화: JIT (Just-In-Time) 권한 부여 흐름도      |
+--------------------------------------------------------------+
|                                                              |
| [DB 관리자 (DBA)]                                             |
|    평소 상태: 권한 없음 (Zero Standing Privileges, ZSP)            |
|                                                              |
|    1. 요청: "티켓 #123 (긴급 패치) 처리를 위해 프로덕션 DB 접근 필요"      |
|       |                                                      |
|       v                                                      |
|  [PAM (Privileged Access Management) 시스템]                   |
|    2. 검증: 티켓 유효성, 승인자 결재, 접속 IP 및 MFA 인증 확인         |
|       |                                                      |
|       v                                                      |
|    3. 생성: 일회용 임시 자격증명(토큰) 발급 및 DB 임시 권한(Read/Write) 주입|
|                                                              |
|       | (접속 세션 시작: 모든 행위 화면 녹화)                       |
|       v                                                      |
|    [ 프로덕션 DB 서버 ] --작업 수행 (수명: 2시간)--                  |
|                                                              |
|    4. 회수: 2시간 경과 후 권한 자동 박탈 (Revoke) 및 토큰 폐기           |
|    결과: 다시 '0(Zero) 권한' 상태로 복귀                             |
+--------------------------------------------------------------+
```

**[다이어그램 해설]** [JIT](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/) 파이프라인의 핵심은 '[Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Standing Privileges (ZSP)' 즉, 평상시 서 있는(상시 존재하는) 특권 계정을 아예 없애는 것이다. 공격자가 DBA의 노트북을 해킹하더라도 그 계정에는 아무런 권한이 없으므로 공격은 실패한다. 오직 정상적인 티켓 시스템과 다중 결재를 거친 '특정 시간(Time-bound)'에만 권한이 열리고, 시간이 지나면 자동으로 닫히기 때문에 공격 표면(Attack Surface)이 시간적으로도 극도로 최소화된다.

- **📢 섹션 요약 비유**: 첩보 영화에서 특수 요원에게 "이 지령 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지는 5초 뒤에 자동으로 폭파됩니다"라고 말하는 것처럼, 사용할 때만 찰나의 권한을 주고 임무가 끝나면 흔적 없이 사라지게 만드는 궁극의 보안 장치입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 모델에서의 최소 권한 구현 수준 비교 ([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) vs DAC vs [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) vs [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/))

최소 권한 원칙은 그 자체로는 철학일 뿐이며, 이를 시스템에 구현하는 물리적 수단이 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)([Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) 모델이다.

| 모델 | 권한 통제 기준 (누가 접근을 허용하는가?) | 최소 권한 (PoLP) 구현 수준 및 한계 |
|:---|:---|:---|
| <strong>DAC (Discretionary <a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/">AC</a>)</strong> | [데이터 소유자](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) (Owner) 재량 | **낮음**. 소유자가 마음대로 타인에게 권한을 넘겨줄 수 있어 최소 권한 원칙이 쉽게 깨짐 (예: 리눅스 `chmod 777`). |
| <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> (Mandatory <a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/">AC</a>)</strong> | 중앙 시스템 관리자 및 보안 레이블 | **매우 높음**. 사용자의 허가 등급과 문서의 기밀 등급을 강제로 매핑하여 Need-to-Know를 완벽히 보장. 단, 운영이 극히 경직됨 (예: [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/)). |
| <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a> (Role-Based <a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/">AC</a>)</strong> | 사용자의 '역할(Role)' | **중간~높음**. 'DB관리자', 'HR담당' 등 역할별로 묶어 최소 권한을 매핑. 실무 표준이나, 직무가 복잡해지면 'Role 폭발'이 일어나 권한 과잉 발생. |
| <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/">ABAC</a> (<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/">Attribute</a>-Based <a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/">AC</a>)</strong>| [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) (사용자+환경+객체 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 조건) | **최상 (동적 PoLP)**. "회계팀(역할)이 + 사내 IP에서(환경) + 근무시간(시간)에만" 접근 가능하도록 마이크로 통제 가능 (예: 클라우드 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)). |

현대의 최소 권한 적용은 단순한 역할 기반([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/))에서 컨텍스트를 고려하는 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반([ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/))으로 진화하고 있다.

```text
+--------------------------------------------------------------+
|           RBAC의 한계와 ABAC를 통한 '동적 최소 권한'의 완성              |
+--------------------------------------------------------------+
|                                                              |
| [RBAC의 함정: Role Explosion (역할 폭발)]                       |
|  "영업팀의 문서를 보려면 영업 Role이 필요하다"                         |
|  -> 철수가 영업팀 파견을 감 -> 철수에게 '영업 Role' 추가 (권한 부여)         |
|  -> 파견 복귀 후 Role을 안 지움 (Privilege Creep 발생, 권한 과잉)       |
|                                                              |
| [ABAC 기반 동적 제어 (Dynamic PoLP)]                           |
|  정책(Policy): "접근자 부서 == 리소스 소속팀 AND 상태 == 정직원"          |
|                                                              |
|  철수 부서: [마케팅] -> 영업 문서 접근 시도 ---> ❌ 접근 거부 (조건 불일치)   |
|  철수 부서: [영업] (인사DB 연동 자동변경) --> ✅ 자동 허용               |
|                                                              |
| 💡 효과: 관리자가 수동으로 권한을 줬다 뺐다 할 필요 없이, 상황(속성)에 따라 |
|          시스템이 실시간으로 '최소 권한'의 바운더리를 계산하여 적용함.       |
+--------------------------------------------------------------+
```

**[다이어그램 해설]** 이 비교는 실무에서 왜 RBAC만으로 최소 권한을 유지하기 힘든지를 설명한다. 시간이 지날수록 사람들의 부서 이동과 프로젝트 참여가 쌓이면서 권한이 줄어들지 않고 계속 커지는 현상(Privilege Creep)이 필연적으로 발생한다. 이를 극복하기 위해 ABAC는 권한을 사람의 '[속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))'에 묶어, 부서가 바뀌거나 퇴사하면 연동된 조건식이 깨져서 즉각적으로 권한이 회수되는 동적(Dynamic) 구조를 제공한다.

- **📢 섹션 요약 비유**: 수동 변속기([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) 자동차는 기어를 제때 안 낮추면 엔진이 고장 날 위험이 있지만, 자동 변속기([ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/))는 속도와 오르막 경사(환경 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))에 맞춰 알아서 가장 최적화된 기어(최소 권한)로 변속해주는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오: 클라우드(AWS/Azure) 인프라의 [컨테이너 보안](/knowledge-base/studynote/04_software_engineering/11_testing_validation/513_container_security/) 설계

1. **상황**: [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서 A [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(결제)와 B [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(이미지 처리)가 동일한 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 클러스터에서 돌고 있다. 개발자가 편의를 위해 노드의 공용 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 역할 하나를 모든 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))에 물려놓았다. 이미지 처리 앱에 원격 코드 실행(RCE) 취약점이 터졌다.
2. <strong>문제점 (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a>)</strong>: RCE로 뚫린 B [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 공용 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 역할을 타고 클라우드 S3 버킷에 저장된 고객 결제 정보를 전부 다운로드하여 유출했다. 이는 PoLP가 완전히 붕괴된 최악의 구조다.
3. **기술사적 교정 (PoLP 적용 아키텍처)**:
   - <strong>IRSA (<a href="/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/">IAM</a> Roles for <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> Accounts)</strong> 도입: 클러스터 공용 권한을 폐기하고, [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 단위로 독립적인 권한을 할당.
   - B [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(이미지) [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에는 '이미지 업로드용 S3 Read/Write' 권한만 부여. 결제 DB 접근은 `Deny`.
   - A [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(결제) [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)에만 '결제 DB Read/Write' 권한 부여.
   - 추가로 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 네트워크 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)(Network [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))을 통해 B [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 A [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 통신을 거는 내부 네트워크 경로 자체를 `Default Deny`로 차단.

```text
+--------------------------------------------------------------+
|           마이크로서비스 환경에서의 최소 권한 (PoLP) 설계 구조           |
+--------------------------------------------------------------+
|                                                              |
|  [AWS 환경]                                                    |
|                                                              |
|  +- Worker Node -------------------------------------------+ |
|  |                                                         | |
|  |  +- Pod: 이미지 처리 --+        +- Pod: 결제 처리 ----+      | |
|  |  | (권한: S3 이미지 버킷만) | ✖차단 | (권한: 결제 DB만)   |      | |
|  |  +-------------------+        +--------------------+      | |
|  +---------------------------------------------------------+ |
|         | (접근)                           | (접근)             |
|         v                                v                  |
|   [S3: 이미지 저장소]                 [RDS: 결제 데이터베이스]     |
|                                                              |
| 💡 결과: 이미지 Pod가 해킹되어도 결제 DB나 결제 Pod로 침투하는 횡적 이동 불가|
+--------------------------------------------------------------+
```

**[다이어그램 해설]** 이 구조는 인프라 레벨의 권한 최소화(Identity)와 네트워크 레벨의 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)(Network)이 결합된 모습이다. 애플리케이션 자체가 해킹당하는 것(Initial Breach)을 100% 막을 수는 없지만, PoLP가 적용되면 해커는 해당 애플리케이션의 좁은 감방(Sandbox)에 갇혀 더 이상 가치 있는 자산(결제 DB)으로 전진할 수 없다. 실무 클라우드 보안 설계의 핵심 중의 핵심이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **운영적**: 장기 방치된 권한(Stale Privileges)을 찾아내는 정기적인 '권한 [접근 검토](/knowledge-base/studynote/09_security/11_iam_access_control/580_access_review/)([Access Review](/knowledge-base/studynote/09_security/11_iam_access_control/580_access_review/))' 프로세스가 자동화되어 있는가?
- **코드/개발적**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인에서 배포 권한과 코드 승인 권한이 '[직무 분리](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/)(SoD)'되어 악의적인 [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 코드가 혼자서 프로덕션으로 배포되는 것을 막고 있는가?

- **📢 섹션 요약 비유**: 호텔을 지을 때 마스터키 하나로 모든 객실이 열리게 만들면 도둑 한 명에게 호텔 전체가 털리지만, 각 방마다 전용 카드키(최소 권한) 시스템을 적용하면 도둑이 빈방 하나를 털더라도 다른 손님의 방은 안전한 이치입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 과도한 권한 (도입 전) | 최소 권한 체계 (도입 후) | 파급 효과 |
|:---|:---|:---|:---|
| **정량** | 사고 발생 시 피해 범위(전체망) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 불가 | 탈취된 단일 계정/[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 격리 | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 대량 유출 및 <a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/">랜섬웨어</a> 전파 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a> 99% <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a></strong> |
| **정성** | '누구든 관리자가 될 수 있다'는 보안 불감증 | 모든 권한 요청과 회수가 투명화됨 | <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/">제로 트러스트 아키텍처</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/047_zta/">ZTA</a>) 도입을 위한 필수 토대 완성</strong> |

### 미래 전망
- <strong>CIEM (Cloud Infrastructure Entitlement <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a>)</strong>: [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) 환경이 되면서 권한(Entitlement)이 너무 복잡해져 사람이 수동으로 매핑하기 불가능해졌다. 향후에는 AI가 권한 사용 로그를 분석하여 "이 역할은 지난 90일 동안 이 권한을 쓴 적이 없으니 불필요한 과잉 권한이다"라고 판단해 자동으로 깎아버리는(Rightsizing) 자동화 도구가 필수가 될 것이다.
- **머신 아이덴티티(Machine Identity)의 부상**: 사람 사용자보다 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 함수, 봇(Bot) 간의 통신이 기하급수적으로 늘어나고 있다. 사람이 아닌 기계 간 통신에서도 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) 수준의 초미세 PoLP [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 동적으로 주입하는 기술이 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 보안의 표준이 될 것이다.

- **📢 섹션 요약 비유**: 최소 권한 원칙은 단지 문을 잠그는 자물쇠 기술이 아니라, 집 안의 모든 서랍과 금고를 지키는 가장 정교한 다이어트 과정입니다. 덜어내고 또 덜어낼수록(권한 축소) 역설적으로 우리의 시스템은 가장 무거운 공격을 버텨낼 수 있는 근육을 갖게 됩니다.

---

## 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">제로 트러스트</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a>)</strong> | 최소 권한 원칙을 전제로, 내부망이라도 절대 신뢰하지 않고 모든 접근을 검증하는 차세대 보안 철학.
- <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/">직무 분리</a> (<a href="/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/">Separation of Duties</a>, SoD)</strong> | 한 사람이 시스템을 훼손할 수 없도록, 권한과 책임을 여러 사람에게 분산시키는 최소 권한의 핵심 동반 원칙.
- <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a> &amp; <a href="/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/">ABAC</a></strong> | 역할(Role)이나 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))을 기준으로 시스템의 권한 할당을 물리적으로 구현하는 통제 모델.
- <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/">JIT</a> (<a href="/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/">Just-In-Time</a>) Access</strong> | 항구적인 권한 부여를 없애고, 오직 작업이 필요한 순간에만 한시적으로 특권을 부여하는 동적 권한 제어 방식.
- **횡적 이동 (Lateral Movement)** | 해커가 최초 침투 지점에서 벗어나 인프라 내부의 더 깊은 곳, 높은 권한으로 확산하려는 행위 (PoLP의 주 방어 대상).

---

## 📈 관련 키워드 및 발전 흐름도

```text
[최소 권한 원칙 (Least Privilege) — 최소한의 권한만 부여]
    |
    v
[직무 분리 (Separation of Duties) — 권한을 여러 주체로 분산]
    |
    v
[역할 기반 접근 제어 (RBAC) — 역할 단위 권한 집합 관리]
    |
    v
[속성 기반 접근 제어 (ABAC) — 상황·속성 기반 세분화 권한]
    |
    v
[제로 트러스트 (Zero Trust) — 기본 거부, 지속 인증·최소 권한 통합]
    |
    v
[PAM (특권 접근 관리) — 관리자 계정 최소 권한 통제 자동화]
```
최소 권한 원칙은 [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) -> [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) -> [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)로 이어지는 현대 보안 아키텍처의 핵심 토대이며, PAM으로 자동화·통합 관리된다.

## 👶 어린이를 위한 3줄 비유 설명
1. 여러분이 도서관에 갔을 때, 도서관 전체 문을 다 열 수 있는 마스터 열쇠를 받는 게 아니라 '어린이 책장'만 열 수 있는 열쇠를 받는 거예요.
2. 어른들 책이나 비밀 서고에는 아예 들어갈 수가 없죠. 이것이 바로 필요한 만큼만 권한을 주는 '최소 권한 원칙'이랍니다!
3. 혹시나 나쁜 도둑이 여러분의 열쇠를 훔쳐 가더라도, 도서관의 중요한 보물 창고는 열 수 없기 때문에 도서관 전체가 아주 안전해진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 10 / 1108

<- **이전**: [9. 사고 대응 (Incident Response)](/knowledge-base/studynote/09_security/01_intro_principles/009_incident_response/)
**다음**: [11. 직무 분리 원칙 (Separation of Duties) — 4눈 원칙, 분산 통제](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/) ->

---
