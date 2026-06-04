---
title: "372. 제로 트러스트 아키텍처 신원 기반 접근 제어 (Zero Trust Architecture ZTNA SASE NIST SP 800-207)"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) ([제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/))는 "절대 신뢰하지 말고, 항상 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하라(Never Trust, Always Verify)"는 원칙으로, 기존 경계 기반 보안(내부는 신뢰)이 원격 근무·클라우드·[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 환경에서 무효화된 현실에 대응하는 [NIST SP 800-207](/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/) 기반 아키텍처 패러다임이다.
> 2. **가치**: PEP/PDP ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Enforcement/Decision Point) 기반 동적 접근 제어와 [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/), SPIFFE/SPIRE [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 신원 증명으로 내부망에서도 모든 요청을 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)·암호화하며, 마이크로세그멘테이션으로 수평 이동(Lateral Movement) 공격을 원천 차단한다.
> 3. **판단 포인트**: [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Network Access)는 기존 VPN을 대체해 사용자-앱 단위 최소 권한 접근을 제공하고, [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) ([Secure Access Service Edge](/studynote/09_security/03_network_security/288_sase/))는 [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) + [CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/) + [SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/) + FWaaS를 클라우드에서 통합 제공하는 아키텍처다.

---

## Ⅰ. 개요 및 필요성

전통 경계 기반 보안([Perimeter Security](/studynote/09_security/18_iot_ot_physical/936_perimeter_security/))은 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)으로 내부망과 외부망을 분리하고 내부는 신뢰한다고 가정한다. 그러나 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 사용, 원격 근무([VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)), [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 도입으로 "내부망"의 개념이 사라졌다. 내부 직원이 악의적 행위자일 수 있고(내부자 위협), [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/)가 VPN을 통해 내부에 침투하면 내부망 전체가 위험하다.

2020년 SolarWinds 공격은 신뢰된 소프트웨어 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)을 통해 내부망에 침투해 수개월간 탐지되지 않았다. 2021년 Colonial [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) 사태는 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 자격증명 유출로 시작됐다. 경계 기반 보안의 근본적 한계가 드러났다.

NIST [SP](/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) 800-207은 [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Architecture의 원칙과 구현 모델을 정의한다: (1) 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스·[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 자원으로 간주, (2) 모든 통신 보안 강제, (3) [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)별 동적 접근 결정, (4) 자산·신원·행위 기반 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), (5) 모든 자원 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/).

- 📢 섹션 요약 비유: 전통 보안은 성벽([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))이 있는 중세 성이다. 성 안으로 들어오면 자유롭게 이동할 수 있다. [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust는 성 안에도 모든 방마다 열쇠가 있고, 신분증을 검사하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|              NIST SP 800-207 Zero Trust 구조                    |
+------------------------------------------------------------------+
|  [주체: 사용자/기기/서비스]                                      |
|         |                                                        |
|  [PEP: Policy Enforcement Point]                                |
|  접근 요청 중간자, 정책 집행                                     |
|         |                                                        |
|  [PE: Policy Engine + PA: Policy Administrator]                 |
|  PDP (Policy Decision Point)                                    |
|  신원(IdP), 기기 상태(MDM), 위협 인텔리전스 참조해 접근 결정    |
|         |                                                        |
|  [보호 자원: 앱/API/데이터/서비스]                               |
|  마이크로세그멘테이션으로 자원 간 격리                           |
+------------------------------------------------------------------+
```

| 구성 요소          | 역할                                               | 구현 예시               |
| :----------------- | :------------------------------------------------- | :---------------------- |
| PEP                | 요청 가로채기, [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 집행                            | Envoy [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/), [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/)|
| PE ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진) | 접근 허용/거부 결정                                 | [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) |
| PA ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) Admin)  | [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 토큰 발급, PEP에 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 전달                    | [IAM](/studynote/09_security/11_iam_access_control/526_iam/), SPIRE              |
| SPIFFE/SPIRE       | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 워크로드 신원 증명 (X.509 SVID)             | K8s + SPIRE             |
| [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/)               | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 양방향 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 암호화                         | [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)       |
| [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)               | 사용자-앱 단위 최소 접근, [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 대체                 | Cloudflare Access, Zscaler|

<strong><a href="/studynote/12_it_management/05_security_compliance/980_ztna/">ZTNA</a> (<a href="/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a> Network Access)</strong>: 사용자가 특정 애플리케이션에만 접근하며, 전체 네트워크 접근 권한을 부여하지 않는다. Agent-based (기기에 클라이언트 설치)와 Agentless (브라우저 기반)로 구분된다.

<strong><a href="/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/">SASE</a> (<a href="/studynote/09_security/03_network_security/288_sase/">Secure Access Service Edge</a>)</strong>: Gartner 2019년 제안. [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) + [CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/) ([Cloud Access Security Broker](/studynote/09_security/16_data_privacy/829_casb/)) + [SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/) (Secure Web Gateway) + FWaaS ([Firewall](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) + SD-WAN을 클라우드 기반으로 통합. Cloudflare One, Zscaler [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Exchange가 대표 구현이다.

- 📢 섹션 요약 비유: ZTNA는 건물 내 모든 방의 열쇠가 개별 잠금장치로 되어 있는 것과 같다. 로비([VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/))에 들어왔다고 모든 방을 열 수 있는 것이 아니라, 각 방마다 신분증을 다시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅲ. 비교 및 연결

| 항목           | 전통 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)                      | [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)                          | [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/)                          |
| :------------- | :---------------------------- | :---------------------------- | :---------------------------- |
| 접근 범위      | 전체 네트워크                 | 특정 앱만                     | 클라우드 통합 전체            |
| 신뢰 모델      | 터널 내 신뢰                  | 요청별 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)                   | 지속적 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)                   |
| 인프라         | [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 게이트웨이 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)     | 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)               | [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)              |
| 가시성         | 낮음 (암호화 터널)            | 중간                          | 높음 (통합 대시보드)          |
| [보안 기능](/studynote/04_software_engineering/11_testing_validation/895_security_features_design/)      | 네트워크 격리                 | 신원·기기·[컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)       | [CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/)+[SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/)+[ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)+FWaaS 통합     |

[Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경에서 [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 구현: [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)의 PeerAuthentication([mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/))과 AuthorizationPolicy로 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 간 최소 권한 통신을 구현한다. SPIFFE/SPIRE로 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 신원을 X.509 SVID로 증명해 IP 기반 신뢰를 대체한다. [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) Gatekeeper로 K8s [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진을 구현한다.

- 📢 섹션 요약 비유: [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) mTLS는 편지 봉투마다 발신인과 수신인의 도장(서명)이 찍힌 등기 우편이다. 내부 네트워크에서도 모든 편지가 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되어, 사칭 편지([스푸핑](/studynote/02_operating_system/10_security/598_spoofing/))를 원천 차단한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a> 도입 로드맵</strong>
1. 신원 강화: [MFA](/studynote/09_security/11_iam_access_control/552_mfa/) ([Multi-Factor Authentication](/studynote/09_security/11_iam_access_control/552_mfa/)) 전사 적용, [IdP](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) 통합 ([Okta](/studynote/09_security/11_iam_access_control/551_okta_idaas/), Entra ID)
2. 기기 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/): [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) (Mobile Device [Management](/studynote/12_it_management/05_security_compliance/1013_management/)), 기기 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 점수 연동
3. 네트워크 마이크로세그멘테이션: NSX-T 또는 [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) 기반 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)/[VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 격리
4. [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) 전환: [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 단계적 대체, 사용자-앱 단위 접근 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)
5. 지속적 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링: [UEBA](/studynote/09_security/12_identity_threat_advanced/613_ueba/) (User and Entity Behavior Analytics), [SIEM](/studynote/09_security/13_secops_ir_forensics/624_siem/) 통합

**판단 기준**
- 원격 근무·멀티클라우드: [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)/[SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) 도입 필수
- K8s [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신: [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) + SPIFFE/SPIRE
- 규제 산업(금융·의료): [NIST SP 800-207](/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/) 준거 아키텍처 필수
- 비용 최적화: 단계별 도입, 신원·[MFA](/studynote/09_security/11_iam_access_control/552_mfa/) 먼저, [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) 이후, [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) 통합 마지막

<strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
- [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 선언 후 [MFA](/studynote/09_security/11_iam_access_control/552_mfa/) 미적용 -> 신원 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없는 [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust는 허울뿐
- [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) 도입 후 레거시 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 병행 장기 유지 -> 공격 경로 이중 노출
- 마이크로세그멘테이션 과도 분할 -> 운영 복잡도 폭증, 합법 트래픽 차단 빈번

- 📢 섹션 요약 비유: [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust를 도입하면서 MFA를 안 하는 것은 은행 금고에 최신 잠금장치를 달았는데 열쇠를 공개된 곳에 두는 것과 같다. 도구보다 원칙(신원 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))이 먼저다.

---

## Ⅴ. 기대효과 및 결론

[ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)/[SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) 도입 기업은 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 대비 지원 비용 45% 절감, 내부 보안 사고 50% 감소, 원격 근무 생산성 향상을 보고한다. 마이크로세그멘테이션으로 [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/)의 수평 이동이 차단되어 침해 범위를 단일 세그먼트로 제한할 수 있다.

한계로는 모든 접근 요청에 대한 지속적 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 인한 레이턴시 증가([ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) 컨트롤 플레인 병목), [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡도 증가, 레거시 시스템과의 통합 어려움이 있다. 또한 [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust는 기술이 아닌 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로, 완성이 아닌 지속적 여정이다.

미래는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 적응형 [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust로 사용자·기기·[컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)·행위 분석을 AI가 실시간으로 수행해 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 점수를 동적으로 산정하고, 이상 행위 감지 시 자동으로 접근을 차단하는 자율 보안 체계로 발전한다.

- 📢 섹션 요약 비유: [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust의 미래는 생체인식 스마트 빌딩이다. 직원이 출근할 때마다 얼굴·행동 패턴·위치를 실시간 분석해 "오늘 이 사람이 평소와 다른 행동을 한다"고 판단하면 자동으로 접근을 차단하는 지능형 보안이다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [NIST SP 800-207](/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/)                         | [Zero Trust Architecture](/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/) 국제 표준, PEP/PDP/PE/PA 정의   |
| [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Network Access)        | 사용자-앱 단위 접근, [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 대체                            |
| [SASE](/studynote/03_network/14_network_security_threats/740_sase_secure_access_service_edge_sdwan_cloud/) ([Secure Access Service Edge](/studynote/09_security/03_network_security/288_sase/))       | [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/)+[CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/)+[SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/)+FWaaS 클라우드 통합                       |
| [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) + SPIFFE/SPIRE                     | K8s [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 신원 증명                       |
| [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) ([Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) Gatekeeper      | 선언적 K8s [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진                                     |
| 마이크로세그멘테이션                     | 수평 이동 차단, NSX-T/[Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) 구현                        |

### 📈 관련 키워드 및 발전 흐름도

```text
경계 기반 보안 (방화벽 내부 신뢰)
    |
    v
VPN (원격 접근 터널)
    |
    v
ZTNA (사용자-앱 단위 최소 접근)
    |
    v
NIST SP 800-207 ZTA (PEP/PDP/PE/PA)
    |
    v
SASE (ZTNA+CASB+SWG+FWaaS 통합)
    |
    v
AI 기반 적응형 Zero Trust (동적 리스크 점수)
```

흐름은 "경계 신뢰 -> 터널 기반 원격 접근 -> 앱 단위 접근 제어 -> 아키텍처 표준화 -> 클라우드 통합 -> [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 적응형"으로 진화한다.

### 👶 어린이를 위한 3줄 비유 설명

1. [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust는 집에 들어왔다고 모든 방을 쓸 수 있는 게 아니라, 각 방마다 비밀번호를 입력해야 들어갈 수 있는 구조예요.
2. ZTNA는 회사 건물 전체에 들어가는 열쇠([VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)) 대신, 내가 갈 사무실(앱) 문만 딱 열어주는 개인 열쇠예요.
3. SASE는 회사 경비 시스템이 클라우드로 이사 가서, 어디서든 내 신분증을 자동으로 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해주는 스마트 보안이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 372 / 373

<- **이전**: [371. DevOps 클라우드 기술사 핵심 키워드 통합 요약 (DevOps Cloud PE Integrated Keyword Summary)](/studynote/13_cloud_architecture/05_data_engineering/371_process/)
**다음**: [400. 클라우드·DevOps·데이터·보안 차세대 통합 플랫폼 엔지니어링 최종 마스터 맵 (Integrated Platform 엔진ering](/studynote/15_devops_sre/05_devsecops/400_devops/) ->

---
