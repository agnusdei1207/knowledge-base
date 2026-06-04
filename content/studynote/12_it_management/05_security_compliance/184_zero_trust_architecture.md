---
title: "184. 제로 트러스트 아키텍처 (Zero Trust Architecture)"
date: "2026-05-06"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 아키텍처 ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/), [ZTA](/studynote/09_security/01_intro_principles/047_zta/))는 내부망 여부를 신뢰 근거로 삼지 않고, 모든 접근 요청마다 사용자·기기·워크로드·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민감도를 다시 평가하는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 보안 구조다.
> 2. **가치**: 원격근무, [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) (Software [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)), 멀티클라우드, 내부자 위협 환경에서 "한 번 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) (Virtual Private Network)에 들어오면 넓게 허용"하던 경계 보안의 약점을 줄이고, 측면 이동(Lateral Movement)을 세밀하게 제한한다.
> 3. **판단 포인트**: ZTA는 [MFA](/studynote/09_security/11_iam_access_control/552_mfa/) ([Multi-Factor Authentication](/studynote/09_security/11_iam_access_control/552_mfa/)) 하나를 추가하는 제품이 아니라, PEP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Enforcement Point)·PDP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Decision Point)·세분화된 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·지속적 텔레메트리가 함께 돌아가는 운영 체계여야 효과가 난다.

---

## Ⅰ. 개요 및 필요성

전통적인 경계 보안([Perimeter Security](/studynote/09_security/18_iot_ot_physical/936_perimeter_security/))은 "밖은 위험하고 안은 안전하다"는 가정 위에 세워졌다. 사내망과 인터넷 경계가 비교적 분명하고, 업무 시스템이 대부분 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 안에 있던 시기에는 이 모델이 일정 부분 통했다. 하지만 오늘날 사용자는 사무실뿐 아니라 재택·모바일·협력사 환경에서 접속하고, 업무 자산은 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)·클라우드·SaaS에 흩어져 있다. 더 이상 네트워크 위치만으로 신뢰를 결정하기 어려워졌다.

더 심각한 문제는 경계 내부에 들어온 뒤의 움직임이다. 공격자가 [피싱](/studynote/09_security/15_malware_attack_vectors/752_phishing/), 자격 증명 탈취, 취약한 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/), 내부자 오용을 통해 일단 내부 접근 권한을 얻으면, 넓게 열린 네트워크에서 다른 자산으로 이동하기 쉽다. 많은 침해 사고가 바로 이 측면 이동 단계에서 커졌다. 즉 경계 보안의 실패는 외부 침입 자체보다, <strong>내부를 너무 넓게 신뢰한 설계</strong>에서 자주 발생한다.

ZTA는 이 전제를 뒤집는다. 내부냐 외부냐가 아니라, 지금 이 요청이 누구의 것인지, 어떤 기기에서 왔는지, 자산 등급은 무엇인지, 최근 위협 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)는 없는지, 현재 권한이 이 행위에 정말 필요한지까지 본다. 그래서 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)의 본질은 "아무도 못 믿는다"가 아니라, <strong>신뢰를 위치에서 <a href="/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a>로 옮기는 것</strong>이다.

- **📢 섹션 요약 비유**: 예전 보안이 회사 건물 현관에서 한 번만 사원증을 보는 방식이었다면, [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)는 중요한 층과 방마다 다시 확인하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

NIST (National Institute of Standards and Technology) [SP](/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) 800-207 기준으로 보면 ZTA의 중심은 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 집행의 분리다. 실제 접근을 허용하거나 차단하는 지점은 PEP이고, 그 결정을 내리는 두뇌는 PDP다. PDP 내부에는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 PE ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진)와 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 관리자 PA ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Administrator)가 있고, 이들은 [IdP](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) ([Identity Provider](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)), 기기 상태, 위협 인텔리전스, [데이터 분류](/studynote/09_security/16_data_privacy/808_data_classification/), [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 이력 같은 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 받아 판단한다.

아래 그림은 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)의 의사결정 루프를 요약한다.

```text
+----------------------------------------------------------------------+
| Zero Trust decision loop                                            |
+----------------------------------------------------------------------+
| Subject: user + device + workload                                   |
|        | request                                                    |
|        v                                                            |
| PEP (Policy Enforcement Point)                                      |
|        | ask decision                                               |
|        v                                                            |
| PDP (Policy Decision Point)                                         |
|   +- PE (Policy Engine): risk / context evaluation                  |
|   +- PA (Policy Administrator): token / session issue               |
|        ^                                                            |
|        | signals                                                    |
| IdP + MFA | device posture | threat intel | data sensitivity        |
|        |                                                            |
|        v                                                            |
| allow / deny / step-up auth / short-lived session                   |
|        |                                                            |
|        v                                                            |
| resource-specific access + continuous re-evaluation                 |
+----------------------------------------------------------------------+
```

여기서 중요한 것은 "로그인 한 번으로 끝나지 않는다"는 점이다. [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 중에도 기기 보안 상태가 나빠지거나, 위치가 급변하거나, 이상 행위가 감지되면 접근을 다시 평가할 수 있어야 한다. 그래서 ZTA는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/))뿐 아니라 권한 부여([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)), 세분화([Micro-Segmentation](/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/)), [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 수명 관리, 지속 관찰(Telemetry)을 한 묶음으로 본다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| PEP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Enforcement Point) | 접근 허용·차단을 실제 집행 | [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/), 게이트웨이, 에이전트 등 배치 위치가 중요 |
| PDP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Decision Point) | 접근 여부를 판단 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 일관성과 응답 속도 확보 필요 |
| PE ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진) | [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 위험 평가 | 정적 규칙 + 동적 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 결합 |
| PA ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Administrator) | [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·토큰 생성과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 | 짧은 수명 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 즉시 철회 지원 |
| Device Posture | 기기 패치·[EDR](/studynote/09_security/04_endpoint_security/325_edr/) (Endpoint [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) and Response) 상태 반영 | 미준수 기기 격리 |
| [Micro-Segmentation](/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/) | 자산 단위 세분화 | 내부 진입 후 측면 이동 최소화 |

ZTA를 강하게 만드는 핵심 문장은 "최소 권한([Least Privilege](/studynote/09_security/01_intro_principles/010_least_privilege/))을 지속적으로 계산한다"는 것이다. 따라서 단순히 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 뒤에 MFA를 붙인 것만으로는 충분하지 않다. 사용자가 한번 연결되면 내부망 대부분에 닿을 수 있다면, 신원은 강화되었어도 신뢰 모델은 여전히 경계 중심에 머문다.

- **📢 섹션 요약 비유**: ZTA는 경비원이 혼자 모든 결정을 내리는 건물이 아니라, 현관 경비가 본사 보안실에 계속 질의하면서 출입문마다 다른 규칙을 적용하는 구조와 같다.

---

## Ⅲ. 비교 및 연결

[제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)는 기존 경계 보안, [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/), [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Network Access), [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) (Secure Access [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Edge), [SDP](/studynote/09_security/01_intro_principles/048_sdp/) (Software Defined Perimeter)와 자주 함께 언급된다. 이때 가장 중요한 구분은 ZTA가 상위 원칙이고, [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)·[SDP](/studynote/09_security/01_intro_principles/048_sdp/)·SASE는 그 원칙을 구현하는 접근이라는 점이다.

| 구분 | 전통 경계 보안 | [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 중심 접근 | [ZTA](/studynote/09_security/01_intro_principles/047_zta/) | [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) / [SDP](/studynote/09_security/01_intro_principles/048_sdp/) / [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) |
| :--- | :--- | :--- | :--- | :--- |
| 신뢰 기준 | 내부망 위치 | [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 접속 성공 | 요청별 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) | [ZTA](/studynote/09_security/01_intro_principles/047_zta/) 구현 수단 |
| 접근 단위 | 네트워크 세그먼트 | 내부망 전체 또는 광범위 | 애플리케이션·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 단위 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 세밀한 접속 |
| 재평가 | 거의 없음 | 접속 시 1회 중심 | 지속적 재평가 | 구현 방식에 따라 지원 |
| 측면 이동 방어 | 약함 | 보통~약함 | 강함 | [ZTA](/studynote/09_security/01_intro_principles/047_zta/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수준에 좌우 |
| 핵심 한계 | 내부 과신 | 연결되면 넓은 권한 | 설계·운영 복잡도 | 벤더 의존 가능성 |

[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 모델 측면에서는 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/))만으로는 부족할 때가 많다. ZTA는 사용자의 역할뿐 아니라 기기 등급, 위치, 시간, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민감도, 위험 점수를 함께 보므로 [ABAC](/studynote/09_security/11_iam_access_control/572_abac/) ([Attribute-Based Access Control](/studynote/09_security/11_iam_access_control/572_abac/))나 Risk-Based Access가 자주 결합된다. 즉 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)는 "누구인가"에 더해 "지금 어떤 상태인가"를 같이 묻는 구조다.

또한 망연계 시스템과의 연결도 생각할 수 있다. 망연계가 큰 경계 사이의 안전한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 통로라면, ZTA는 그 통로를 지난 뒤에도 사용자·[세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·리소스별 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 계속 수행하는 원리다. 하나는 경계 운영, 다른 하나는 경계 이후까지 이어지는 지속 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이라고 볼 수 있다.

- **📢 섹션 요약 비유**: ZTA가 보안 철학이라면, ZTNA는 그 철학으로 만든 출입 시스템이고, SASE는 출입 시스템과 보안 장비를 클라우드에 묶어 놓은 종합 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[ZTA](/studynote/09_security/01_intro_principles/047_zta/) 전환은 보통 "모든 것을 한 번에 바꾸는 프로젝트"가 아니라 성숙도 향상 여정으로 진행된다. 가장 먼저 해야 할 일은 사용자·기기·애플리케이션·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)과 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)다. [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상이 무엇인지 모르면 어떤 요청을 어디에서 차단해야 할지도 정할 수 없다. 따라서 자산 목록, 계정 정리, 관리되지 않는 기기 파악이 출발점이다.

그다음은 고가치 자산을 중심으로 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 좁혀 가는 방식이 현실적이다. 예를 들어 관리자 포털, 핵심 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)([Database](/studynote/05_database/04_transactions_concurrency/501_database/)), 개발자 배포 체계, 원격 접속 경로부터 [MFA](/studynote/09_security/11_iam_access_control/552_mfa/), 기기 준수 검사, 최소 권한, 짧은 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 세분화 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용한다. 이후 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신(Workload Identity), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근, 자동화 계정까지 확장하면 비로소 전사적 ZTA에 가까워진다.

| 단계 | 실무 초점 | 대표 통제 |
| :--- | :--- | :--- |
| 1단계: 가시화 | 자산·계정·기기 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | [IAM](/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/studynote/12_it_management/05_security_compliance/1013_management/)), 자산 인벤토리 |
| 2단계: 신원 강화 | 사용자 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 고도화 | [MFA](/studynote/09_security/11_iam_access_control/552_mfa/), [SSO](/studynote/09_security/11_iam_access_control/531_sso/) ([Single Sign-On](/studynote/09_security/11_iam_access_control/531_sso/)), 비정상 로그인 탐지 |
| 3단계: 기기·[세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 통제 | 준수 상태와 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 수명 반영 | Device Posture, [Conditional Access](/studynote/09_security/12_identity_threat_advanced/610_azure_ad_conditional_access/) |
| 4단계: 자산 세분화 | 리소스 단위 최소 권한 | [Micro-Segmentation](/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/), [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) |
| 5단계: 지속 대응 | 이상 징후 기반 재평가 | [SIEM](/studynote/09_security/13_secops_ir_forensics/624_siem/) ([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Information and [Event Management](/studynote/12_it_management/02_itsm_itil/074_event_management/)), [SOAR](/studynote/03_network/14_network_security_threats/745_soar_security_orchestration_automation_response/) ([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/), Automation, and Response) |

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)해야 할 고가치 자산과 사용자 군이 명확한가?
2. [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 연결 뒤에 넓은 내부망 접근이 그대로 남아 있지 않은가?
3. 사용자뿐 아니라 기기와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계정에도 신뢰 점수를 반영하는가?
4. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경 시 예외 승인, 비상 계정(Break-Glass), [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 로그가 준비되어 있는가?
5. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 효과를 측정할 텔레메트리와 운영 대시보드가 있는가?

### 자주 발생하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [MFA](/studynote/09_security/11_iam_access_control/552_mfa/) 도입만 하고 내부망 평면 구조는 그대로 두는 경우
- 기존 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 제품 이름만 바꿔 ZTA라고 부르는 경우
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민감도 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 없이 모든 자산에 똑같은 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용하는 경우
- 사용자 계정만 보고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출이나 배치 계정을 놓치는 경우
- 운영 예외 절차가 없어 보안 우회와 불편을 동시에 만드는 경우

기술사 답안에서는 "Never Trust, Always Verify"라는 구호만 쓰기보다, <strong>PEP/PDP 분리, 최소 권한, 기기 상태 반영, 지속적 재평가, 측면 이동 차단</strong>을 구조적으로 설명해야 점수가 살아난다. 특히 ZTA는 보안 제품명보다 운영 원칙이라는 점을 분명히 적는 것이 중요하다.

- **📢 섹션 요약 비유**: 좋은 [ZTA](/studynote/09_security/01_intro_principles/047_zta/) 전환은 오래된 집의 모든 문을 하루아침에 바꾸는 일이 아니라, 가장 중요한 방부터 스마트 잠금장치와 출입 기록을 단계적으로 붙여 가는 작업과 같다.

---

## Ⅴ. 기대효과 및 결론

잘 구현된 ZTA는 공격자의 이동 반경을 줄이고, 정상 사용자의 접속도 더 설명 가능하게 만든다. 누가 어떤 기기에서 어떤 자산에 왜 접근했는지가 로그로 남고, 위험 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 올라오면 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 줄이거나 추가 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 요구할 수 있다. 그래서 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)의 효과는 단순 차단률보다, <strong>사고가 나더라도 피해를 좁게 묶는 능력</strong>에서 크게 드러난다.

물론 비용과 복잡도는 분명하다. [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 설계가 서투르면 사용자 경험이 나빠지고, 자산 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) 정비 없이 도입하면 운영이 혼란스러워질 수 있다. 그러나 원격근무·클라우드·내부자 위협이 일상이 된 환경에서는 이 복잡도를 피하는 대신, 더 큰 사고 비용을 감수하게 된다.

결론적으로 ZTA는 "내부망을 더 안전하게 만드는 기술"이 아니라, <strong>신뢰의 기준을 네트워크 위치에서 신원·기기·행동·<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 맥락으로 옮기는 아키텍처 전환</strong>이다. 따라서 기억할 문장은 단순하다. "안에 있다고 믿지 말고, 지금 이 요청이 타당한지 계속 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하라."

- **📢 섹션 요약 비유**: [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)는 건물 한 번 들어왔다고 자유 출입을 허용하는 것이 아니라, 중요한 문마다 이유와 상태를 다시 확인하는 스마트 출입 체계와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PEP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Enforcement Point) | 실제 접근 허용·차단을 집행하는 관문이다. |
| PDP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Decision Point) | [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)를 바탕으로 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정을 내리는 두뇌다. |
| [MFA](/studynote/09_security/11_iam_access_control/552_mfa/) ([Multi-Factor Authentication](/studynote/09_security/11_iam_access_control/552_mfa/)) | 사용자 신원 강화를 위한 기본 통제지만 ZTA의 전부는 아니다. |
| [Micro-Segmentation](/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/) | 내부 진입 이후의 측면 이동을 줄이는 핵심 구조다. |
| [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Network Access) | [ZTA](/studynote/09_security/01_intro_principles/047_zta/) 원칙을 원격 접근 경로에 구현한 대표 방식이다. |
| [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) (Secure Access [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Edge) | ZTA와 여러 보안 기능을 클라우드 엣지에서 통합하는 프레임워크다. |

### 📈 관련 키워드 및 발전 흐름도

```text
경계 기반 보안
    |
    v
원격근무 · SaaS · 클라우드 확산
    |
    v
내부망 과신의 한계 노출
    |
    v
MFA + Device Posture + Least Privilege
    |
    v
PEP / PDP 기반 Zero Trust Architecture
    |
    v
ZTNA + Micro-Segmentation + Continuous Telemetry
```

이 흐름은 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)가 단순한 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 강화가 아니라, 경계 중심 신뢰 모델을 요청 중심 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 모델로 바꾸는 과정임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)는 학교 안에 들어왔다고 해서 아무 교실이나 들어가게 하지 않는 규칙이에요.
2. 문을 열 때마다 누구인지, 어떤 준비물을 가졌는지, 지금 들어가도 되는지 다시 확인해요.
3. 그래서 나쁜 사람이 한 번 안으로 들어와도 다른 방으로 쉽게 돌아다니지 못해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 298 / 587

<- **이전**: [183. 망연계 시스템 (Network Linkage System)](/studynote/12_it_management/05_security_compliance/183_network_linkage_system/)
**다음**: [185. 접근 제어 메커니즘 (Access Control: MAC, DAC, RBAC, ABAC)](/studynote/12_it_management/05_security_compliance/185_access_control_mac_dac_rbac_abac/) ->

---
