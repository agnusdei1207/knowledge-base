+++
title = "185. 접근 제어 메커니즘 (Access Control: MAC, DAC, RBAC, ABAC)"
date = 2026-05-06

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 접근 제어 ([Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/))는 "누가, 무엇에, 어떤 행위를, 어떤 조건에서 할 수 있는가"를 결정하는 체계이며, [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) (Mandatory [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)), DAC (Discretionary [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)), [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)), [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) ([Attribute-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/))은 그 결정을 내리는 기준이 서로 다르다.
> 2. **가치**: 최소 권한 ([Least Privilege](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/))과 [직무 분리](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/) ([Separation of Duties](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/))를 실제 시스템에 구현하는 핵심 수단이어서, 내부자 위협과 과도한 권한 부여를 줄이고 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능성을 높인다.
> 3. **판단 포인트**: 규제가 강하고 변경이 적은 환경은 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), 소유자 중심 협업은 DAC, 조직 운영은 [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), 동적 조건이 많은 클라우드·[제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 환경은 ABAC이 유리하며, 실무에서는 네 모델을 혼합하는 경우가 많다.

---

## Ⅰ. 개요 및 필요성

접근 제어는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)) 이후의 질문을 다룬다. 사용자가 누구인지 확인한 뒤에도, 그 사용자가 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 기능에 어느 범위까지 접근할 수 있는지는 별도의 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 결정해야 한다. 이 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 허술하면 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 아무리 강하게 해도 과도한 권한, 내부자 오남용, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출을 막기 어렵다.

역사적으로 접근 제어 모델은 군사·정부 환경의 기밀 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서 출발해, 일반 운영체제의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유, 기업의 조직형 권한 관리, 그리고 클라우드·[SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) (Software [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))·모바일 환경의 동적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 확장되었다. 즉 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), DAC, [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), ABAC은 단순한 이론 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 아니라, "권한을 누가 어떻게 설명 가능하게 관리할 것인가"에 대한 시대별 답변이다.

따라서 이 주제의 핵심은 약어를 외우는 것이 아니다. 어떤 조직에서 권한 변화가 얼마나 잦은지, 자산 민감도가 얼마나 높은지, 예외 승인과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 얼마나 중요한지를 보고 적절한 모델을 선택해야 한다. 접근 제어는 보안 기술이면서 동시에 운영 거버넌스의 문제다.

- **📢 섹션 요약 비유**: 접근 제어는 건물 출입 관리와 같아서, 사람을 확인하는 것만으로 끝나지 않고 어느 층, 어느 방, 언제 들어갈 수 있는지까지 정해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

네 가지 모델의 차이는 결국 "접근 허용 여부를 누가 무엇으로 판단하는가"에 있다. MAC은 시스템이 레이블과 [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 등급을 강제로 비교하고, DAC은 자원 소유자가 권한을 나눠 준다. RBAC은 사용자에게 직접 권한을 주기보다 역할을 매개로 권한을 묶고, ABAC은 주체·객체·환경 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진이 평가해 결정을 내린다.

```text
+----------------------------------------------------------------------+
| Access control decision lens                                        |
+----------------------------------------------------------------------+
| Request = Subject + Object + Action + Context                       |
|        |                                                            |
|        v                                                            |
| Decision model                                                      |
|   MAC  -> label vs clearance                                        |
|   DAC  -> owner / ACL                                               |
|   RBAC -> role -> permission map                                    |
|   ABAC -> attribute policy evaluation                               |
|        |                                                            |
|        v                                                            |
| Enforcement point -> allow / deny / log                             |
+----------------------------------------------------------------------+
```

이 구조가 보여 주는 핵심은 네 모델이 모두 "허용/거부"를 내리지만, 판단의 근거가 다르다는 점이다. 그래서 동일한 시스템이라도 규정 준수, 운영 편의성, 예외 처리 방식이 크게 달라진다. 예를 들어 MAC은 강력하지만 예외가 어렵고, ABAC은 유연하지만 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 품질과 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡도가 성패를 가른다.

| 모델 | 결정 기준 | 대표 구현/이론 | 강점 | 핵심 약점 |
| :--- | :--- | :--- | :--- | :--- |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) | 보안 등급과 레이블 | [Bell-LaPadula](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/), Biba, [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/) | 강한 중앙 통제, 규제 친화적 | 유연성 낮고 예외 처리 어려움 |
| DAC | 소유자와 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([Access Control List](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | Unix chmod, NTFS [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) | 사용이 직관적이고 공유가 쉬움 | 권한이 흩어져 통제 일관성이 약함 |
| [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) | 역할과 권한 매핑 | AD ([Active Directory](/knowledge-base/studynote/09_security/11_iam_access_control/548_active_directory/)), [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 권한 체계 | 조직 단위 운영에 적합 | 역할 폭증(Role Explosion) 가능 |
| [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)과 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 평가 | [XACML](/knowledge-base/studynote/09_security/11_iam_access_control/574_xacml/) (eXtensible [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Markup Language), [OPA](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) | 동적 상황 반영, 세밀한 통제 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 설계와 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 거버넌스가 어렵다 |

MAC의 대표 원리는 "No Read Up, No Write Down" 같은 보안 규칙이고, DAC의 핵심은 소유권이다. RBAC은 사용자 수가 많아질수록 직접 권한 대신 역할을 중심에 두어 운영 복잡도를 줄이며, ABAC은 부서·기기 상태·위치·시간대·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민감도까지 합쳐 판단한다. 즉 뒤로 갈수록 더 동적이고 더 문맥적인 접근 제어로 진화한다고 볼 수 있다.

- **📢 섹션 요약 비유**: MAC은 나라가 정한 출입등급표, DAC은 방 주인이 준 열쇠, RBAC은 직책별 출입카드, ABAC은 출입카드에 시간·장소·기기 상태까지 함께 보는 스마트 게이트에 가깝다.

---

## Ⅲ. 비교 및 연결

실무에서 네 모델은 경쟁 관계라기보다 적용 문맥이 다른 도구들이다. 예를 들어 기업 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))는 RBAC이 기본이지만, 중요 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대해서는 [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 겹쳐 적용할 수 있다. 반대로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유 시스템은 DAC으로 시작하되, 기밀 자료는 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 또는 별도 [DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/) ([Data Loss Prevention](/knowledge-base/studynote/09_security/16_data_privacy/823_dlp/)) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 보강할 수 있다.

| 비교 축 | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) | DAC | [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) | [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) |
| :--- | :--- | :--- | :--- | :--- |
| 권한 결정 주체 | 중앙 시스템 | 자원 소유자 | 보안/권한 관리자 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 |
| 변화 대응성 | 낮음 | 중간 | 중간 | 높음 |
| 운영 적합 환경 | 군사·정부·고규제 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유·개인 협업 | 기업 업무 시스템 | 클라우드·[제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) |
| [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 설명력 | 높음 | 낮을 수 있음 | 높음 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 품질에 따라 달라짐 |
| 주요 위험 | 과도한 경직성 | 권한 남발 | 역할 폭증 | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 오류·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡성 |

이 비교를 보면 RBAC이 오랫동안 기업의 기본 해법이었던 이유가 보인다. 조직도와 직무 체계를 역할로 묶으면 권한 부여와 회수를 설명하기 쉽기 때문이다. 하지만 예외가 많아지면 역할 수가 폭발하고, 이 한계를 메우기 위해 ABAC이나 Risk-Based Access가 추가된다. 즉 현대 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))은 RBAC만으로 끝나는 경우보다 [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) + [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) 조합이 훨씬 흔하다.

또한 접근 제어는 AAA ([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/), [Authorization](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/), Accounting)와 연결된다. 이 네 모델은 주로 Authorization을 설명하지만, 실제 보안 효과는 강한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 로그가 함께 있을 때 완성된다. [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) ([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) 역시 ABAC적 사고를 많이 차용한다. "역할만 맞으면 허용"보다 "지금 이 기기와 위치와 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 상태가 적절한가"를 함께 보기 때문이다.

- **📢 섹션 요약 비유**: RBAC이 부서별 사원증 체계라면, ABAC은 사원증에 현재 위치와 시간, 기기 상태까지 붙여서 문이 스스로 판단하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 답안에서 중요한 것은 모델 설명보다 선택 이유다. 규제기관 보고가 중요하고 정보 등급 체계가 명확한 환경은 MAC이 잘 맞는다. 반면 협업 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유처럼 소유자가 문서를 나누는 일이 많은 환경은 DAC이 자연스럽다. 조직의 직무 구조가 뚜렷한 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), 그룹웨어, 인사 시스템은 RBAC이 기본값이고, 멀티클라우드 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 접근이나 조건부 접속 통제는 ABAC이 더 적합하다.

실무에서는 단일 모델보다 하이브리드가 현실적이다. 예를 들어 "직무상 회계 권한"은 RBAC으로 주고, "회사 관리 단말 + 국내 접속 + 근무 시간"이라는 추가 조건은 ABAC으로 걸 수 있다. 또 최고 기밀 문서는 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 레이블로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) 위에 한 번 더 덮는 식의 계층화도 가능하다.

| 상황 | 권장 모델 | 판단 이유 |
| :--- | :--- | :--- |
| 군사·국가 기밀 문서 | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) | 중앙 통제와 등급 일관성이 최우선 |
| 일반 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버 공유 | DAC + 검토 절차 | 소유자 중심 협업이 많음 |
| [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), HR, 전사 그룹웨어 | [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) | 직무/부서 구조와 권한 묶음이 잘 맞음 |
| 클라우드 콘솔, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 원격접속 | [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) + [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) | 역할 + 기기/위치/시간 조건을 함께 봐야 함 |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 권한을 사람에게 직접 주는지, 역할이나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 추상화했는지 구분했는가?
2. 예외 권한이 많아질 때 역할 폭증을 어떻게 통제할지 기준이 있는가?
3. ABAC를 쓴다면 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)의 원천 시스템인 인사 시스템(HR), 모바일 기기 관리([MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)), 엔드포인트 탐지 및 대응([EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/))이 신뢰할 만한가?
4. 고권한 계정은 [PAM](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/) ([Privileged Access Management](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/))으로 별도 통제하는가?
5. 권한 부여·변경·회수·정기 재검토가 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 로그로 남는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 고규제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 DAC만으로 맡겨 소유자 재량에 지나치게 의존하는 경우
- 모든 예외를 새 역할로만 해결해 RBAC가 유지 불가능해지는 경우
- [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 복잡하게 만들었지만 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 품질과 책임 주체를 정하지 않은 경우
- 관리자 권한을 일반 사용자 권한 모델 안에 섞어 두는 경우
- 모델은 정교하지만 권한 정기 검토와 회수 프로세스가 없는 경우

결국 접근 제어의 기술사적 포인트는 "어떤 모델이 최고인가"가 아니라, <strong>어떤 조직 문맥에서 어떤 모델 조합이 설명 가능하고 운영 가능한가</strong>다. 시스템이 커질수록 권한 자체보다 권한 변경과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 더 중요해진다.

- **📢 섹션 요약 비유**: 좋은 접근 제어는 열쇠 종류를 많이 만드는 것이 아니라, 누가 왜 어떤 문을 열 수 있는지 관리실이 설명할 수 있게 만드는 것이다.

---

## Ⅴ. 기대효과 및 결론

적절한 접근 제어 모델을 도입하면 과도한 권한을 줄이고, 인사 이동이나 퇴사 시 권한 회수를 표준화하며, 사고가 발생했을 때 누가 어떤 경로로 접근했는지 더 명확히 추적할 수 있다. 즉 보안성뿐 아니라 운영 효율과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응력까지 함께 좋아진다.

다만 모델이 고도화될수록 운영 전제가 중요해진다. MAC은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계가 흔들리면 의미가 없고, RBAC은 역할 설계가 빈약하면 곧바로 예외 폭증으로 무너진다. ABAC은 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 공급과 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 테스트 자동화가 없으면 오히려 더 이해하기 어려운 시스템이 될 수 있다. 좋은 모델보다 더 중요한 것은 좋은 거버넌스다.

결론적으로 이 주제는 "권한을 어떤 기준으로 묶고 설명할 것인가"로 기억하는 편이 좋다. <strong>MAC은 시스템 기준, DAC은 소유자 기준, RBAC은 역할 기준, ABAC은 문맥 기준의 접근 제어</strong>다. 실무의 정답은 대개 하나가 아니라, 이 기준들을 적절히 조합해 최소 권한과 설명 가능성을 동시에 확보하는 데 있다.

- **📢 섹션 요약 비유**: 접근 제어의 성숙도는 열쇠가 많은가보다, 관리실이 출입 규칙을 일관되게 설명하고 바로 수정할 수 있는가에서 갈린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([Access Control List](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | DAC의 대표 구현 방식으로 객체별 권한을 기록한다. |
| [Bell-LaPadula](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/) | MAC에서 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 원리를 설명하는 대표 모델이다. |
| Biba | MAC에서 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 관점의 접근 제어를 설명한다. |
| SoD ([Separation of Duties](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/)) | [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) 설계에서 역할 충돌을 막는 핵심 원칙이다. |
| [OPA](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) | [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 구현 예시로 자주 언급된다. |
| [PAM](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/) ([Privileged Access Management](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/)) | 고권한 계정 통제를 통해 접근 제어를 보강한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
기밀 등급 중심 통제
    |
    v
MAC (Mandatory Access Control)
    |
    v
파일 소유권 중심 공유
    |
    v
DAC (Discretionary Access Control)
    |
    v
조직 역할 중심 권한 묶음
    |
    v
RBAC (Role-Based Access Control)
    |
    v
속성 · 문맥 · 위험 기반 정책
    |
    v
ABAC 및 적응형 접근 제어
```

이 흐름은 접근 제어가 고정된 등급 통제에서 점점 더 조직적이고 문맥적인 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MAC은 선생님이 "이 책은 5학년만" 하고 정해 두면 아무도 바꿀 수 없는 규칙이에요.
2. RBAC은 반장, 도서부, 선생님처럼 맡은 역할에 따라 들어갈 수 있는 방이 달라지는 거예요.
3. ABAC은 여기에 지금 몇 시인지, 학교 안에 있는지까지 같이 보고 문이 열릴지 정하는 똑똑한 문이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 299 / 587

<- **이전**: [184. 제로 트러스트 아키텍처 (Zero Trust Architecture)](/knowledge-base/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/)
**다음**: [186. 데이터 유출 방지 (DLP, Data Loss Prevention) 시스템](/knowledge-base/studynote/12_it_management/05_security_compliance/186_dlp_data_loss_prevention/) ->

---
