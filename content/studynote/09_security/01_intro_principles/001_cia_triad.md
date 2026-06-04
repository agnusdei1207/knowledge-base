+++
title = "1. 정보보안 3요소 — CIA (기밀성·무결성·가용성)"
description = "기밀성, 무결성, 가용성으로 구성된 정보보안의 3대 핵심 목표와 이들 간의 실무적 트레이드오프 분석"
date = 2023-10-24

[taxonomies]
tags = ["security"]

[extra]
tags = ["security"]
+++

# 정보보안 3요소 (CIA Triad)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)([Confidentiality](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))은 정보 자산을 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하기 위한 가장 근본적인 3대 목표이다.
> 2. **가치**: 보안 투자의 우선순위를 결정하는 척도가 되며, 특정 요소의 강화가 다른 요소의 약화로 이어지는 물리적 트레이드오프 관계를 지닌다.
> 3. **융합**: 현대 아키텍처에서는 [인증성](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/), 부인방지, 책임추적성 등을 더하여 단순 CIA의 한계를 보완한 확장된 보안 모델로 발전하고 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

정보보안 3요소 (CIA Triad)는 정보 자산의 안전성을 평가하고 설계하기 위한 근본적인 프레임워크다. 이는 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)으로 구성되며, 모든 정보보안 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 기술적 통제의 최종 목적지 역할을 한다. 초기의 컴퓨터 시스템은 물리적 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)에만 의존했으나, 네트워크로 연결된 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경이 도래하면서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 전송되고 저장되는 모든 상태에서 논리적인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 메커니즘이 필요해졌다. 이에 따라 시스템의 방어선을 체계화하기 위해 CIA 모델이 정립되었다.

보안은 단순히 해커를 막는 것을 넘어 비즈니스의 연속성을 보장하는 핵심 인프라다. CIA 3요소는 한쪽을 극단적으로 강화하면 필연적으로 다른 쪽이 취약해지거나 사용성이 저하되는 특성을 가진다. 실무에서는 무작정 높은 보안을 추구하는 것이 아니라, 자산의 가치와 위협 모델을 분석하여 이 세 가지 요소 간의 최적의 균형점을 찾는 것이 필수적이다.

이 도식은 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 서로 어떻게 상호작용하며 균형을 이뤄야 하는지를 직관적으로 보여준다.

```text
          [기밀성 (Confidentiality)]
          "비인가된 접근 및 유출 차단"
             /        \
   (암호화 오버헤드)   (가용성 저하 위험)
           /            \
          /              \
[무결성 (Integrity)] ---- [가용성 (Availability)]
"비인가된 위변조 차단"     "적시적, 중단 없는 접근 보장"
       (동기화 및 백업 오버헤드)
```

이 그림의 핵심은 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 독립적인 목표가 아니라 서로 팽팽하게 당기는 삼각형의 꼭짓점과 같다는 점이다. 복잡한 암호화를 통해 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)을 높이면 시스템 부하가 증가하여 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 떨어질 수 있으며, 반대로 편의성을 위해 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 극대화하면 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)이나 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)에 구멍이 생길 위험이 커진다. 실무에서는 비즈니스 요구사항에 따라 이 3요소 간의 최적의 균형점(Sweet Spot)을 찾는 것이 [보안 아키텍처](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/) 설계의 최우선 과제다.

**📢 섹션 요약 비유**: 마치 자동차 설계 시 '최고 속도', '차체 안전성', '연비'의 관계와 같습니다. 안전을 위해 장갑을 두껍게 하면 차가 무거워져 속도와 연비가 떨어지는 것처럼, 완벽한 보안이란 존재하지 않으며 용도에 맞는 최적의 튜닝이 필요합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CIA Triad를 구현하기 위해 시스템은 다양한 보안 통제([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Control)를 계층적으로 적용한다.

| 구성 요소 | 역할 및 목적 | 내부 동작 메커니즘 | 관련 기술 및 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 실무 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a> (<a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">Confidentiality</a>)</strong> | [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)되지 않은 주체의 정보 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) | [암호화 알고리즘](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/) 적용 및 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 기반의 [접근 제어 목록](/knowledge-base/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/)([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) 검사 | [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/), [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/), [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) | 금고의 자물쇠 |
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> (<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a>)</strong> | [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)되지 않은 주체에 의한 정보 위변조 방지 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해시값 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 및 비교, [전자서명](/knowledge-base/studynote/03_network/13_network_security_basics/675_digital_signature_process_asymmetric_key/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 변경 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | SHA-256, [HMAC](/knowledge-base/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/), [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/), [Checksum](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) | 편지의 봉인 씰 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong> | [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)된 주체의 적시적이고 연속적인 정보 접근 보장 | [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)(Redundancy) 배치를 통한 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) 제거 및 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | L4/L7 LB, [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/), [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/), DDoS [Mitigation](/knowledge-base/studynote/09_security/12_identity_threat_advanced/605_golden_silver_ticket_mitigation/) | 24시간 응급실 |
| <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a> (<a href="/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">Identification</a>)</strong> | 주체의 정체성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) (CIA 지원 요소) | 사용자 ID나 토큰을 시스템에 제시 | User ID, [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Token | 신분증 제시 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a>)</strong> | 제시된 정체성의 진위 여부 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 비밀번호, 생체 정보 등 자격증명 대조 | [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/), FIDO2, OAuth 2.0 | 신분증 사진 대조 |

보안 통제가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름에 어떻게 적용되는지 살펴보자. 다음은 클라이언트가 서버의 자산에 접근하는 과정에서 CIA 요소가 단계별로 개입하는 흐름도이다.

```text
[Client]
   │ (1. 기밀성: TLS 암호화 채널 형성)
   ▼
[API Gateway / WAF] -- (2. 가용성: 트래픽 필터링 및 Rate Limiting)
   │
   ├─> [인증/인가 서버] (3. 기밀성: RBAC 기반 권한 검증)
   │
   ▼
[Application Server]
   │
   ├─> (4. 무결성: 입력 데이터 Hash 검증 및 SQL Injection 방지)
   │
   ▼
[Database / Storage] -- (5. 가용성/무결성: Active-Standby 복제, 트랜잭션 처리)
```

이 도식의 핵심은 방어선이 네트워크 경계부터 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 내부까지 다계층([Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/))으로 구성되어 있다는 점이다. [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)은 진입점에서의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과 전송 구간 암호화로 달성되고, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 애플리케이션 계층의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 확보되며, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 게이트웨이의 부하 제어와 DB의 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)로 보장된다. 따라서 특정 계층이 뚫리더라도 다른 계층의 통제가 보완적 역할을 수행하여 전체 시스템의 붕괴를 막는다. 실무에서는 각 단계마다 오버헤드가 발생하므로 캐싱과 하드웨어 가속을 적절히 병행해야 한다.

**📢 섹션 요약 비유**: 마치 공항의 보안 검색대와 같습니다. 여권 검사([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)), 수하물 엑스레이([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)), 다중 검색 레인 운영([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))이 단계별로 촘촘히 배치되어 전체 항공 시스템의 안전을 보장합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

CIA 모델을 더욱 명확히 이해하기 위해, 보안 실패 시 발생하는 반대 개념인 DAD (Disclosure, Alteration, Destruction) 모델과 비교하고, 확장된 보안 프레임워크인 Parkerian Hexad와의 차이를 분석한다.

| 비교 항목 | CIA Triad (방어 관점) | DAD Triad (공격/실패 관점) | 방어 및 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a> ↔ 노출</strong> | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) ([Confidentiality](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)) 보장 | 노출/유출 (Disclosure) 발생 | 종단간 암호화(E2EE), [DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/) 적용 |
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> ↔ 변조</strong> | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)) 보장 | 변조/조작 (Alteration) 발생 | [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 렛저, HIPS, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 모니터링 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> ↔ 파괴</strong> | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 보장 | 파괴/중단 (Destruction) 발생 | [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)(재해복구) 센터, 불변([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) |

CIA 모델은 직관적이지만 현대의 복잡한 비즈니스 요구사항을 모두 담기에는 한계가 있다. 이에 따라 등장한 확장 모델과의 비교는 다음과 같다.

```text
┌───────────────┬─────────────────────────┬──────────────────────────┐
│ 모델 구분     │ 구성 요소               │ 한계점 및 특징             │
├───────────────┼─────────────────────────┼──────────────────────────┤
│ CIA Triad     │ 기밀성, 무결성, 가용성  │ 단순명료하나, 소유권과   │
│               │                         │ 책임 소재의 증명이 약함  │
├───────────────┼─────────────────────────┼──────────────────────────┤
│ Parkerian     │ CIA + 소유성(Possession)│ 데이터가 유출되었으나    │
│ Hexad         │ + 진본성(Authenticity)  │ 암호화되어 기밀성은 유지 │
│               │ + 유용성(Utility)       │ 되는 상태를 설명 가능함  │
├───────────────┼─────────────────────────┼──────────────────────────┤
│ 정보보안 6요소│ CIA + 인증성, 부인방지, │ 금융/전자상거래의 법적   │
│               │ 책임추적성              │ 분쟁 해결에 필수적임     │
└───────────────┴─────────────────────────┴──────────────────────────┘
```

이 매트릭스의 핵심은 순수한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)(CIA)를 넘어, 현대 보안은 '사람의 행위'에 대한 증명([인증성](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/), 부인방지)과 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 실질적 통제권'(소유성, 유용성)까지 영역을 확장하고 있다는 점이다. [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/)에 감염된 경우, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 위변조([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 침해)가 발생하지만 암호화되어 있어 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)은 유지될 수 있다. 그러나 '유용성'과 '소유성'은 상실된다. 따라서 실무에서는 CIA 모델을 뼈대로 하되, 산업군의 규제([Compliance](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/))에 맞춰 확장된 통제 항목을 결합하는 하이브리드 접근이 필수적이다.

**📢 섹션 요약 비유**: CIA가 건물의 '벽, 지붕, 문'이라는 기본적인 뼈대라면, 확장된 보안 모델은 건물 내부의 '[CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/), 출입 장부, 경비원 순찰 기록'까지 추가하여 총체적인 관리를 완성하는 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실제 침해 사고 시나리오에서 CIA 중 무엇을 최우선으로 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하고 포기할 것인지에 대한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 판단이 필요하다.

1. <strong>시나리오 1: 대규모 <a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/">랜섬웨어</a> 감염 (<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 및 <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 침해)</strong>
   - **상황**: 내부 DB가 암호화되어 접근 불가. 해커는 복호화 키를 조건으로 몸값을 요구함.
   - **판단**: 이미 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변형)과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(접근 불가)이 파괴된 상태다. 이 경우 네트워크를 물리적으로 분리(격리)하여 추가적인 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 유출 및 수평 이동(Lateral Movement)을 막는 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)([Containment](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 최우선이다. 이후 오프라인 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 통해 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)과 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 복원한다.

2. <strong>시나리오 2: 초당 100Gbps의 DDoS 공격 (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 침해)</strong>
   - **상황**: 대고객 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 웹사이트 마비 발생.
   - **판단**: 공격의 목적이 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 타격에 있다. 트래픽 스크러빙 센터로 우회시키고 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 캐싱을 극대화한다. 이때 일시적으로 무거운 [WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/)([웹 방화벽](/knowledge-base/studynote/03_network/19_frequent_topics_terms/993_waf_web_application_firewall/))의 정밀 검사 규칙을 완화하여 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))을 우선 확보할 것인가, 아니면 지연이 생기더라도 정밀 검사([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)/[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))를 유지할 것인가의 트레이드오프를 결정해야 한다.

다음은 침해 사고 발생 시 우선순위를 결정하는 의사결정 트리다.

```text
[보안 이벤트 발생]
       │
       ▼
[서비스 유형 판단]
 ├─ (금융/군사 시스템) ──> [기밀성/무결성 최우선] ──> 시스템 강제 종료 및 차단 (Fail-Secure)
 │                                                    (가용성 포기)
 │
 └─ (의료/통신 인프라) ──> [가용성 최우선] ────────> 격리된 네트워크에서 최소 기능 유지 (Fail-Safe)
                                                      (부분적 보안위험 감수)
```

이 의사결정 트리의 핵심은 장애 발생 시 시스템을 어떻게 실패(Fail)시킬 것인가에 대한 철학이다. 금융 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 잘못된 값이 기록되거나 유출되는 것이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단보다 치명적이므로 시스템을 멈추는 Fail-Secure로 동작해야 한다. 반면, 생명 유지 장치나 통신망은 시스템이 멈추면 생명이 위협받으므로 성능이 저하되더라도 동작을 유지하는 [Fail-Safe](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/) 방향으로 설계된다. 실무에서는 자산 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 단계에서 이러한 [Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 명확히 정의해야 한다.

**📢 섹션 요약 비유**: 불이 난 병원에서 수술실의 전력을 끊어 화재 확산을 막을 것인가([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)/[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 우선), 아니면 화재 위험을 안고서라도 수술실 전력을 유지할 것인가([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선)를 사전에 매뉴얼로 정해두는 것과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

CIA Triad를 기반으로 설계된 [보안 아키텍처](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/)는 조직의 자산 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)와 비즈니스 연속성 확보에 결정적인 기여를 한다.

| 기대효과 구분 | 도입 전 (Ad-hoc 보안) | 도입 후 (CIA 기반 체계적 보안) | 정량/정성 지표 |
|:---|:---|:---|:---|
| **위협 가시성** | 위협 탐지 및 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 불가 | 자산별 취약점 매핑 및 대응 우선순위 명확화 | 보안 사고 인지 시간(MTTD) 감소 |
| **운영 효율성** | 모든 자산에 획일적 보안 적용 | 자산 중요도에 따른 통제 수준(Control Level) 차등화 | 보안 인프라 투자 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 30% 증가 |
| **규제 준수** | [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 지적 및 과태료 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | [ISMS-P](/knowledge-base/studynote/12_it_management/05_security_compliance/171_isms_p/), ISO 27001 등 글로벌 컴플라이언스 요건 충족 | 외부 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 통과율 100% |

향후 정보보안의 패러다임은 정적인 네트워크 경계 방어에서 벗어나, 모든 주체와 접근을 의심하는 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/))로 진화하고 있다. 하지만 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 역시 그 근간에는 철저한 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 통제와 상태 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 지속적 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 확보라는 CIA 원칙이 자리 잡고 있다.

```text
[과거: 경계 기반 보안]           [미래: 제로 트러스트 보안]
방화벽(기밀성) 중심       ==>    Micro-Segmentation (세밀한 기밀성)
서버 백업(가용성) 중심    ==>    Cloud-Native 자동 확장 (탄력적 가용성)
정적 권한(무결성) 중심    ==>    컨텍스트 기반 동적 신뢰 평가 (연속적 무결성)
```

이 비교도는 CIA 3요소가 사라지는 것이 아니라, 마이크로서비스와 클라우드 환경에 맞춰 더욱 동적이고 세분화된 형태로 녹아들고 있음을 보여준다. 결론적으로 정보보안 기술이 아무리 고도화되더라도 CIA Triad는 기술사적 설계의 출발점이자 종착점으로서 영원한 가치를 지닌다.

**📢 섹션 요약 비유**: 나침반이 수백 년 전이나 지금이나 항해의 기본이 되듯, CIA 3요소는 AI와 클라우드 시대에도 [보안 아키텍처](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/)가 길을 잃지 않도록 방향을 잡아주는 영원한 나침반입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/">접근 통제</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/">Access Control</a>)</strong> | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 강제하기 위한 구체적인 [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">제로 트러스트</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a>)</strong> | CIA 통제를 내부망에도 동일하게 적용하는 현대 보안 철학
- <strong>위험 관리 (<a href="/knowledge-base/studynote/09_security/17_framework_compliance/841_iso_27005_risk_management/">Risk Management</a>)</strong> | CIA 침해 시 발생하는 비즈니스 손실을 정량화하고 대응하는 프로세스
- <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/">암호학</a> (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/">Cryptography</a>)</strong> | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)(암호화)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)(해시)을 기술적으로 수학적으로 보장하는 학문
- <strong><a href="/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/056_bcp_business_continuity_plan_bia/">비즈니스 연속성 계획</a> (BCP)</strong> | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 완전히 파괴되었을 때 조직을 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 관리적 통제

### 📈 관련 키워드 및 발전 흐름도

```text
[접근 통제 (Access Control)]
    │
    ▼
[제로 트러스트 (Zero Trust)]
    │
    ▼
[위험 관리 (Risk Management)]
    │
    ▼
[암호학 (Cryptography)]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a></strong>: 일기장을 자물쇠로 잠가서 나만 볼 수 있게 하는 거예요. (비밀 유지)
2. <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong>: 내 일기장 내용을 동생이 몰래 지우거나 낙서하지 못하게 막는 거예요. (원본 유지)
3. <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong>: 내가 일기를 쓰고 싶을 때 언제든지 일기장과 펜을 꺼내 쓸 수 있는 거예요. (언제든 사용 가능)

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1 / 1108

← **이전**: (첫 번째 글입니다)

**다음**: [2. 기밀성 (Confidentiality) — 암호화, 접근 제어, DRM, 분류](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) →

---
