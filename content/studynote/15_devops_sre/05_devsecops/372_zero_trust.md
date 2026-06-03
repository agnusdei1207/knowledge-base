---
title: 372. 제로 트러스트 아키텍처 신원 기반 접근 제어 (Zero Trust Architecture ZTNA SASE NIST SP 800-207)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] ([[667_zero_trust_runtime_integrity_measurement|제로 트러스트]])는 "절대 신뢰하지 말고, 항상 [[395_verification_process_review|검증]]하라(Never Trust, Always Verify)"는 원칙으로, 기존 경계 기반 보안(내부는 신뢰)이 원격 근무·클라우드·[[309_saas|SaaS]] 환경에서 무효화된 현실에 대응하는 [[850_nist_sp_800_207|NIST SP 800-207]] 기반 아키텍처 패러다임이다.
> 2. **가치**: PEP/PDP ([[164_policy|Policy]] Enforcement/Decision Point) 기반 동적 접근 제어와 [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], SPIFFE/SPIRE [[090_service_kubernetes_network_load_balancing|서비스]] 신원 증명으로 내부망에서도 모든 요청을 [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]]·암호화하며, 마이크로세그멘테이션으로 수평 이동(Lateral Movement) 공격을 원천 차단한다.
> 3. **판단 포인트**: [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access)는 기존 VPN을 대체해 사용자-앱 단위 최소 권한 접근을 제공하고, [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] ([[288_sase|Secure Access Service Edge]])는 [[339_ztna|ZTNA]] + [[741_casb_cloud_access_security_broker|CASB]] + [[742_swg_secure_web_gateway|SWG]] + FWaaS를 클라우드에서 통합 제공하는 아키텍처다.

---

## Ⅰ. 개요 및 필요성

전통 경계 기반 보안([[936_perimeter_security|Perimeter Security]])은 [[690_firewall_generation_evolution|방화벽]]으로 내부망과 외부망을 분리하고 내부는 신뢰한다고 가정한다. 그러나 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]] 사용, 원격 근무([[983_vpn_virtual_private_network|VPN]]), [[309_saas|SaaS]] 도입으로 "내부망"의 개념이 사라졌다. 내부 직원이 악의적 행위자일 수 있고(내부자 위협), [[730_ransomware|랜섬웨어]]가 VPN을 통해 내부에 침투하면 내부망 전체가 위험하다.

2020년 SolarWinds 공격은 신뢰된 소프트웨어 [[520_supply_chain_attack_and_ci_cd_security|공급망]]을 통해 내부망에 침투해 수개월간 탐지되지 않았다. 2021년 Colonial [[082_pipeline|Pipeline]] 사태는 [[983_vpn_virtual_private_network|VPN]] 자격증명 유출로 시작됐다. 경계 기반 보안의 근본적 한계가 드러났다.

NIST [[166_sp|SP]] 800-207은 [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Architecture의 원칙과 구현 모델을 정의한다: (1) 모든 [[001_dikw_pyramid|데이터]] 소스·[[090_service_kubernetes_network_load_balancing|서비스]]를 자원으로 간주, (2) 모든 통신 보안 강제, (3) [[160_session_controlling_terminal|세션]]별 동적 접근 결정, (4) 자산·신원·행위 기반 [[164_policy|정책]], (5) 모든 자원 [[229_monitor|모니터]]링·[[395_verification_process_review|검증]].

- 📢 섹션 요약 비유: 전통 보안은 성벽([[690_firewall_generation_evolution|방화벽]])이 있는 중세 성이다. 성 안으로 들어오면 자유롭게 이동할 수 있다. [[585_zero_skipping|Zero]] Trust는 성 안에도 모든 방마다 열쇠가 있고, 신분증을 검사하는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│              NIST SP 800-207 Zero Trust 구조                    │
├──────────────────────────────────────────────────────────────────┤
│  [주체: 사용자/기기/서비스]                                      │
│         │                                                        │
│  [PEP: Policy Enforcement Point]                                │
│  접근 요청 중간자, 정책 집행                                     │
│         │                                                        │
│  [PE: Policy Engine + PA: Policy Administrator]                 │
│  PDP (Policy Decision Point)                                    │
│  신원(IdP), 기기 상태(MDM), 위협 인텔리전스 참조해 접근 결정    │
│         │                                                        │
│  [보호 자원: 앱/API/데이터/서비스]                               │
│  마이크로세그멘테이션으로 자원 간 격리                           │
└──────────────────────────────────────────────────────────────────┘
```

| 구성 요소          | 역할                                               | 구현 예시               |
| :----------------- | :------------------------------------------------- | :---------------------- |
| PEP                | 요청 가로채기, [[164_policy|정책]] 집행                            | Envoy [[264_proxy_pattern_surrogate_access_control|Proxy]], [[542_api_gateway|API Gateway]]|
| PE ([[164_policy|Policy]] Engine) | 접근 허용/거부 결정                                 | [[237_opa_open_policy_agent_gatekeeper|OPA]] ([[237_opa_open_policy_agent_gatekeeper|Open Policy Agent]]) |
| PA ([[164_policy|Policy]] Admin)  | [[160_session_controlling_terminal|세션]] 토큰 발급, PEP에 [[164_policy|정책]] 전달                    | [[526_iam|IAM]], SPIRE              |
| SPIFFE/SPIRE       | [[090_service_kubernetes_network_load_balancing|서비스]] 워크로드 신원 증명 (X.509 SVID)             | K8s + SPIRE             |
| [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]]               | [[090_service_kubernetes_network_load_balancing|서비스]] 간 양방향 [[694_thread_local_storage_tls|TLS]] 암호화                         | [[302_service_mesh_istio|Istio]] [[302_service_mesh_istio|서비스 메시]]       |
| [[339_ztna|ZTNA]]               | 사용자-앱 단위 최소 접근, [[983_vpn_virtual_private_network|VPN]] 대체                 | Cloudflare Access, Zscaler|

**[[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access)**: 사용자가 특정 애플리케이션에만 접근하며, 전체 네트워크 접근 권한을 부여하지 않는다. Agent-based (기기에 클라이언트 설치)와 Agentless (브라우저 기반)로 구분된다.

**[[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] ([[288_sase|Secure Access Service Edge]])**: Gartner 2019년 제안. [[339_ztna|ZTNA]] + [[741_casb_cloud_access_security_broker|CASB]] ([[829_casb|Cloud Access Security Broker]]) + [[742_swg_secure_web_gateway|SWG]] (Secure Web Gateway) + FWaaS ([[690_firewall_generation_evolution|Firewall]] [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) + SD-WAN을 클라우드 기반으로 통합. Cloudflare One, Zscaler [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Exchange가 대표 구현이다.

- 📢 섹션 요약 비유: ZTNA는 건물 내 모든 방의 열쇠가 개별 잠금장치로 되어 있는 것과 같다. 로비([[983_vpn_virtual_private_network|VPN]])에 들어왔다고 모든 방을 열 수 있는 것이 아니라, 각 방마다 신분증을 다시 [[396_validation|확인]]한다.

---

## Ⅲ. 비교 및 연결

| 항목           | 전통 [[983_vpn_virtual_private_network|VPN]]                      | [[339_ztna|ZTNA]]                          | [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]]                          |
| :------------- | :---------------------------- | :---------------------------- | :---------------------------- |
| 접근 범위      | 전체 네트워크                 | 특정 앱만                     | 클라우드 통합 전체            |
| 신뢰 모델      | 터널 내 신뢰                  | 요청별 [[395_verification_process_review|검증]]                   | 지속적 [[395_verification_process_review|검증]]                   |
| 인프라         | [[983_vpn_virtual_private_network|VPN]] 게이트웨이 [[061_on_premise_legacy_infrastructure|온프레미스]]     | 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]]               | [[531_cloud_native_architecture|클라우드 네이티브]]              |
| 가시성         | 낮음 (암호화 터널)            | 중간                          | 높음 (통합 대시보드)          |
| [[503_security_features_design|보안 기능]]      | 네트워크 격리                 | 신원·기기·[[033_context|컨텍스트]] [[509_authorization_models_rbac_abac|인가]]       | [[741_casb_cloud_access_security_broker|CASB]]+[[742_swg_secure_web_gateway|SWG]]+[[339_ztna|ZTNA]]+FWaaS 통합     |

[[205_kubernetes_container_orchestration|Kubernetes]] 환경에서 [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 구현: [[302_service_mesh_istio|Istio]] [[302_service_mesh_istio|서비스 메시]]의 PeerAuthentication([[831_mtls_mutual_tls_microservices_zero_trust|mTLS]])과 AuthorizationPolicy로 [[085_pod_kubernetes_container_unit|파드]] 간 최소 권한 통신을 구현한다. SPIFFE/SPIRE로 [[085_pod_kubernetes_container_unit|파드]] 신원을 X.509 SVID로 증명해 IP 기반 신뢰를 대체한다. [[237_opa_open_policy_agent_gatekeeper|OPA]] ([[237_opa_open_policy_agent_gatekeeper|Open Policy Agent]]) Gatekeeper로 K8s [[164_policy|정책]] 엔진을 구현한다.

- 📢 섹션 요약 비유: [[302_service_mesh_istio|서비스 메시]] mTLS는 편지 봉투마다 발신인과 수신인의 도장(서명)이 찍힌 등기 우편이다. 내부 네트워크에서도 모든 편지가 [[395_verification_process_review|검증]]되어, 사칭 편지([[598_spoofing|스푸핑]])를 원천 차단한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 도입 로드맵**
1. 신원 강화: [[552_mfa|MFA]] ([[552_mfa|Multi-Factor Authentication]]) 전사 적용, [[536_idp_identity_provider|IdP]] 통합 ([[551_okta_idaas|Okta]], Entra ID)
2. 기기 상태 [[395_verification_process_review|검증]]: [[539_mdm_master_data_management|MDM]] (Mobile Device [[372_management|Management]]), 기기 [[085_confidence_association_rule_conditional_probability|신뢰도]] 점수 연동
3. 네트워크 마이크로세그멘테이션: NSX-T 또는 [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] 기반 [[085_pod_kubernetes_container_unit|파드]]/[[598_vm_migration_nic|VM]] 격리
4. [[339_ztna|ZTNA]] 전환: [[983_vpn_virtual_private_network|VPN]] 단계적 대체, 사용자-앱 단위 접근 [[164_policy|정책]]
5. 지속적 [[229_monitor|모니터]]링: [[613_ueba|UEBA]] (User and Entity Behavior Analytics), [[624_siem|SIEM]] 통합

**판단 기준**
- 원격 근무·멀티클라우드: [[339_ztna|ZTNA]]/[[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] 도입 필수
- K8s [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신: [[302_service_mesh_istio|Istio]] [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] + SPIFFE/SPIRE
- 규제 산업(금융·의료): [[850_nist_sp_800_207|NIST SP 800-207]] 준거 아키텍처 필수
- 비용 최적화: 단계별 도입, 신원·[[552_mfa|MFA]] 먼저, [[339_ztna|ZTNA]] 이후, [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] 통합 마지막

**[[128_water_scrum_fall_anti_pattern|안티패턴]]**
- [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 선언 후 [[552_mfa|MFA]] 미적용 → 신원 [[395_verification_process_review|검증]] 없는 [[585_zero_skipping|Zero]] Trust는 허울뿐
- [[339_ztna|ZTNA]] 도입 후 레거시 [[983_vpn_virtual_private_network|VPN]] 병행 장기 유지 → 공격 경로 이중 노출
- 마이크로세그멘테이션 과도 분할 → 운영 복잡도 폭증, 합법 트래픽 차단 빈번

- 📢 섹션 요약 비유: [[585_zero_skipping|Zero]] Trust를 도입하면서 MFA를 안 하는 것은 은행 금고에 최신 잠금장치를 달았는데 열쇠를 공개된 곳에 두는 것과 같다. 도구보다 원칙(신원 [[395_verification_process_review|검증]])이 먼저다.

---

## Ⅴ. 기대효과 및 결론

[[339_ztna|ZTNA]]/[[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] 도입 기업은 [[983_vpn_virtual_private_network|VPN]] 대비 지원 비용 45% 절감, 내부 보안 사고 50% 감소, 원격 근무 생산성 향상을 보고한다. 마이크로세그멘테이션으로 [[730_ransomware|랜섬웨어]]의 수평 이동이 차단되어 침해 범위를 단일 세그먼트로 제한할 수 있다.

한계로는 모든 접근 요청에 대한 지속적 [[395_verification_process_review|검증]]으로 인한 레이턴시 증가([[339_ztna|ZTNA]] 컨트롤 플레인 병목), [[164_policy|정책]] 복잡도 증가, 레거시 시스템과의 통합 어려움이 있다. 또한 [[585_zero_skipping|Zero]] Trust는 기술이 아닌 [[268_strategy_pattern|전략]]으로, 완성이 아닌 지속적 여정이다.

미래는 [[190_ai_llm_requirements_specification|AI]] 기반 적응형 [[585_zero_skipping|Zero]] Trust로 사용자·기기·[[033_context|컨텍스트]]·행위 분석을 AI가 실시간으로 수행해 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 점수를 동적으로 산정하고, 이상 행위 감지 시 자동으로 접근을 차단하는 자율 보안 체계로 발전한다.

- 📢 섹션 요약 비유: [[585_zero_skipping|Zero]] Trust의 미래는 생체인식 스마트 빌딩이다. 직원이 출근할 때마다 얼굴·행동 패턴·위치를 실시간 분석해 "오늘 이 사람이 평소와 다른 행동을 한다"고 판단하면 자동으로 접근을 차단하는 지능형 보안이다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [[850_nist_sp_800_207|NIST SP 800-207]]                         | [[184_zero_trust_architecture|Zero Trust Architecture]] 국제 표준, PEP/PDP/PE/PA 정의   |
| [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access)        | 사용자-앱 단위 접근, [[983_vpn_virtual_private_network|VPN]] 대체                            |
| [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] ([[288_sase|Secure Access Service Edge]])       | [[339_ztna|ZTNA]]+[[741_casb_cloud_access_security_broker|CASB]]+[[742_swg_secure_web_gateway|SWG]]+FWaaS 클라우드 통합                       |
| [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] + SPIFFE/SPIRE                     | K8s [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 신원 증명                       |
| [[237_opa_open_policy_agent_gatekeeper|OPA]] ([[237_opa_open_policy_agent_gatekeeper|Open Policy Agent]]) Gatekeeper      | 선언적 K8s [[164_policy|정책]] 엔진                                     |
| 마이크로세그멘테이션                     | 수평 이동 차단, NSX-T/[[825_cilium_ebpf_kubernetes_networking_security|Cilium]] 구현                        |

### 📈 관련 키워드 및 발전 흐름도

```text
경계 기반 보안 (방화벽 내부 신뢰)
    │
    ▼
VPN (원격 접근 터널)
    │
    ▼
ZTNA (사용자-앱 단위 최소 접근)
    │
    ▼
NIST SP 800-207 ZTA (PEP/PDP/PE/PA)
    │
    ▼
SASE (ZTNA+CASB+SWG+FWaaS 통합)
    │
    ▼
AI 기반 적응형 Zero Trust (동적 리스크 점수)
```

흐름은 "경계 신뢰 → 터널 기반 원격 접근 → 앱 단위 접근 제어 → 아키텍처 표준화 → 클라우드 통합 → [[190_ai_llm_requirements_specification|AI]] 적응형"으로 진화한다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[585_zero_skipping|Zero]] Trust는 집에 들어왔다고 모든 방을 쓸 수 있는 게 아니라, 각 방마다 비밀번호를 입력해야 들어갈 수 있는 구조예요.
2. ZTNA는 회사 건물 전체에 들어가는 열쇠([[983_vpn_virtual_private_network|VPN]]) 대신, 내가 갈 사무실(앱) 문만 딱 열어주는 개인 열쇠예요.
3. SASE는 회사 경비 시스템이 클라우드로 이사 가서, 어디서든 내 신분증을 자동으로 [[396_validation|확인]]해주는 스마트 보안이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 372 / 373

← **이전**: [[371_process|371. DevOps 클라우드 기술사 핵심 키워드 통합 요약 (DevOps Cloud PE Integrated Keyword Summary)]]
**다음**: [[400_devops|400. 클라우드·DevOps·데이터·보안 차세대 통합 플랫폼 엔지니어링 최종 마스터 맵 (Integrated Platform Engineering]] →

---
