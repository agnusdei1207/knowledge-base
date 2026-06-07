---
title: "Dns Bgp"
date: "2026-04-28"
tags:
  - "studynote-devops-sre"
weight: 186
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) 캐시 중독과 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) ([Border Gateway Protocol](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/)) 하이재킹 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망은 이름 해석 경로와 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 경로가 동시에 오염될 수 있다는 전제 아래, <strong>응답 <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>·경로 <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong>을 함께 감시하는 관측 체계다.
> 2. **가치**: 사용자 트래픽이 [피싱](/studynote/09_security/15_malware_attack_vectors/752_phishing/) 사이트나 잘못된 [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) (Autonomous System) 경로로 우회되기 전에 탐지해, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애와 보안 사고를 조기에 차단할 수 있다.
> 3. **판단 포인트**: [DNSSEC](/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Extensions)와 [RPKI](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/) ([Resource Public Key Infrastructure](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/))는 [예방 통제](/studynote/09_security/01_intro_principles/053_preventive_controls/)이고, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망은 실제 인터넷 경로에서 일어나는 이상 징후를 다중 시점에서 상시 관찰하는 [탐지 통제](/studynote/09_security/01_intro_principles/054_detective_controls/)라는 점이 중요하다.

---

## Ⅰ. 개요 및 필요성

인터넷 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 정상 동작하려면 두 가지가 동시에 맞아야 한다. 사용자가 질의한 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 올바른 IP 주소로 해석돼야 하고, 그 IP까지 가는 네트워크 경로도 정상이어야 한다. [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 캐시 중독은 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 리졸버(Recursive Resolver)의 응답 캐시를 오염시켜 사용자를 잘못된 주소로 보내고, [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 하이재킹은 인터넷 경로 광고를 탈취해 트래픽 자체를 공격자 쪽으로 우회시킨다.

문제는 두 공격 모두 사용자 입장에서는 “그냥 접속이 잘 된다”처럼 보일 수 있다는 점이다. 웹페이지가 열리더라도 공격자가 준비한 위장 서버일 수 있고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애가 없더라도 중간 경로에서 트래픽이 가로채질 수 있다. 따라서 운영자는 단순한 업타임 체크만으로는 부족하고, [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답과 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 경로를 별도로 그리고 함께 관찰해야 한다.

특히 [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) (Content Delivery Network), Anycast, 멀티클라우드, 글로벌 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 보편화되면서 지역별 응답과 경로가 달라지는 것이 정상 상태가 됐다. 이 때문에 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 더 어려워졌고, 다수 관측 지점과 정상 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)이 필수 조건이 됐다.

- **📢 섹션 요약 비유**: 인터넷 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 “주소를 제대로 알려 주는 안내판”과 “그 주소까지 가는 도로 표지판”이 모두 맞아야 도착한다. 하나만 틀려도 손님은 엉뚱한 곳으로 간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망의 핵심은 서로 다른 관측 소스를 한곳에 모아 [교차 검증](/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)하는 것이다. [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 측에서는 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 리졸버 응답, 권한 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 서버 응답, [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) ([Time To Live](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/)) 변화, NS·A·AAAA·CNAME 레코드 편차를 본다. [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 측에서는 Origin [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 변화, [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Path 길이 급증, Route Leak, ROA (Route Origin [Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)) invalid 여부, 특정 지역에서만 보이는 경로 편차를 본다.

아래 그림은 DNS와 BGP를 통합 감시하는 대표 구조다.

```text
+------------------------------------------------------------------------------+
|                  DNS + BGP 통합 모니터링망 구성                             |
+------------------------------------------------------------------------------+
| [External DNS Probes]      [Recursive Resolvers]      [Route Collectors]   |
|         |                           |                         |              |
|         +--------------+------------+--------------+---------+              |
|         v              v                           v                        |
|  Answer Diff      TTL Drift / NXDOMAIN      Origin AS / AS Path            |
|         |              |                           |                        |
|         +--------------+--------------+------------+                        |
|                                       v                                     |
|                         [Correlation / Detection Engine]                    |
|                                       |                                     |
|                  +--------------------+--------------------+                |
|                  v                    v                    v                |
|          DNSSEC Validate       RPKI Validate      Baseline Compare         |
|                  |                    |                    |                |
|                  +--------------------+--------------------+                |
|                                       v                                     |
|                         [Alert / Ticket / Traffic Mitigation]               |
+------------------------------------------------------------------------------+
```

| 관측 항목 | 의미 | 이상 징후 예시 |
| :--- | :--- | :--- |
| [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답 편차 | 지역별 응답 값 비교 | 특정 지역만 다른 IP 응답 |
| [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 급감 | 캐시 재주입, 레코드 교체 시도 감지 | 평소 300초인데 갑자기 5초 |
| NS/DS 불일치 | 권한 체인 문제, 위조 가능성 | 서명 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 실패 |
| Origin [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 변경 | 원래 광고 주체와 다른 [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 출현 | 갑작스러운 해외 [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 기원 |
| [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Path 비정상 증가 | 우회 또는 누출 가능성 | 평소 4-hop인데 12-hop |
| [RPKI](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/) invalid | 허용되지 않은 경로 광고 | ROA와 다른 Origin 광고 |

핵심은 한 소스만 믿지 않는 것이다. [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답이 달라졌더라도 [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경일 수 있고, [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 경로가 길어졌더라도 일시적 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 변경일 수 있다. 하지만 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답 편차와 Origin [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 이상이 같은 시각에 동시에 발생하면 사고 가능성이 급격히 높아진다. 그래서 통합 상관분석이 중요하다.

- **📢 섹션 요약 비유**: 길찾기 앱만 보고 가면 주소는 맞아도 도로가 막혔는지 모를 수 있다. 안내판과 도로 CCTV를 같이 봐야 진짜 이상을 빨리 알아차릴 수 있다.

---

## Ⅲ. 비교 및 연결

[DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 캐시 중독과 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 하이재킹은 모두 트래픽을 잘못된 곳으로 보내지만, 공격 지점과 통제 방식은 다르다. [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 중독은 이름 해석 계층을 공격하고, [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 하이재킹은 인터넷 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 계층을 공격한다. 따라서 DNSSEC만으로는 [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 문제를 막을 수 없고, RPKI만으로는 위조 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답을 막을 수 없다.

| 비교 축 | [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 캐시 중독 | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 하이재킹 |
| :--- | :--- | :--- |
| 공격 대상 | [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 리졸버 캐시, 이름 해석 | 인터넷 경로 광고 |
| 피해 양상 | 위조 IP 응답, [피싱](/studynote/09_security/15_malware_attack_vectors/752_phishing/) 유도 | 트래픽 우회, [도청](/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/), 블랙홀 |
| 예방 기술 | [DNSSEC](/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/), Source [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) Randomization | [RPKI](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/), Prefix Filtering, [IRR](/studynote/12_it_management/01_governance_strategy/809_irr_internal_rate_of_return/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 탐지 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | 응답 값 변화, [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 이상, 서명 실패 | Origin [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 변화, Path 이상, ROA invalid |
| 운영 주체 | [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 운영팀·보안팀 | 네트워크/[SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 팀·[ISP](/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) 협업 |

[서비스 운영](/studynote/12_it_management/02_itsm_itil/067_service_operation/) 측면에서 이 주제는 [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/), 인터넷 외부 의존성 관리, [공급망 보안](/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)과도 연결된다. 단순 인프라 내부 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링만으로는 인터넷 경계 밖에서 벌어지는 경로 변조를 볼 수 없기 때문이다. 그래서 공개 Route Collector, Passive [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/), 외부 프로브, [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 사업자 협업이 함께 필요하다.

- **📢 섹션 요약 비유**: [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 문제가 집 주소를 잘못 적는 일이라면, [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 문제는 지도 자체가 바뀌는 일이다. 주소책만 고치거나 지도만 고쳐서는 둘 다 해결되지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 “무엇을 볼 것인가”보다 “어디서 얼마나 자주 볼 것인가”가 더 중요하다. 글로벌 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 최소한 다수 지역 외부 프로브를 두고, 내부 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 리졸버와 권한 서버 응답을 비교해야 한다. BGP는 자체 피어링이 없더라도 RouteViews, RIPE RIS, Cloud [provider](/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/) telemetry 같은 외부 관측원을 활용해 정상 경로를 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)으로 저장해야 한다.

### 운영 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 권한 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답, [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 리졸버 응답, 외부 사용자 시점 응답을 모두 수집하는가?
2. 주요 프리픽스(prefix)에 대해 Origin [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/), ROA 상태, [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Path 변화를 상시 저장하는가?
3. [DNSSEC](/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/) 실패와 [RPKI](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/) invalid 알람을 단순 경고가 아니라 사건 처리 흐름으로 연결하는가?
4. [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/)·Anycast·멀티클라우드로 인한 정상 편차를 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)에 반영했는가?
5. 탐지 후 조치(캐시 플러시, Route Withdraw, [ISP](/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/) 연락, 공지)까지 [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/)이 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 내부 헬스체크만으로 인터넷 전체에서의 이상을 본다고 착각하는 경우
- 외부 프로브를 한 지역에만 두어 지역성 공격을 놓치는 경우
- DNSSEC와 RPKI를 켰다는 이유만으로 상시 관측을 소홀히 하는 경우
- 정상 [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 변동, [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 응답 차이, 교통 우회 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 모른 채 오탐을 남발하는 경우

기술사 답안에서는 “[DNSSEC](/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/)/[RPKI](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/) 도입”만 쓰지 말고, <strong>다중 관측 지점, <a href="/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/">베이스라인</a> 비교, 상관분석, 대응 <a href="/studynote/09_security/13_secops_ir_forensics/637_playbook/">플레이북</a></strong>을 함께 써야 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망 주제가 살아난다. [예방 통제](/studynote/09_security/01_intro_principles/053_preventive_controls/)와 [탐지 통제](/studynote/09_security/01_intro_principles/054_detective_controls/)를 분리해서 설명하면 더 구조적인 답안이 된다.

- **📢 섹션 요약 비유**: 화재경보기만 달아 놓고 대피 훈련을 안 하면 실제 불이 났을 때 우왕좌왕한다. [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망도 알람 자체보다 알람 이후 동작이 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

[DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)·[BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 통합 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망의 기대효과는 세 가지다. 첫째, [피싱](/studynote/09_security/15_malware_attack_vectors/752_phishing/)·경로 탈취 같은 외부 인터넷 사고를 조기에 감지한다. 둘째, 장애와 공격을 구분하는 시간이 짧아져 MTTD (Mean Time To Detect)를 줄인다. 셋째, 사고 시 근거 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 남겨 통신사, 클라우드 사업자, 보안 조직과의 공동 대응이 쉬워진다.

다만 인터넷은 본질적으로 외부 의존성이 큰 환경이어서, 모든 이상을 내부에서 통제할 수는 없다. 따라서 이 주제는 “내 시스템 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 잘 보는 법”이 아니라, <strong>인터넷 전체 맥락 속에서 내 <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>과 프리픽스를 어떻게 관측할 것인가</strong>의 문제로 이해해야 한다. DNSSEC와 RPKI가 안전벨트라면, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망은 주행 중 계기판이다.

- **📢 섹션 요약 비유**: 안전벨트를 맸다고 해서 운전 중 계기판을 안 볼 수는 없다. DNSSEC와 RPKI가 예방 장치라면, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망은 길이 잘못 들었는지 바로 알려 주는 내비게이션 경고등이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [DNSSEC](/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/) | [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| Recursive Resolver | 캐시 중독이 직접 일어나는 지점 |
| Passive [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) | 지역별 응답 편차 관측 |
| [RPKI](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/) ([Resource Public Key Infrastructure](/studynote/09_security/uncategorized/1069_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/)) | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) Origin [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 핵심 |
| ROA (Route Origin [Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)) | 허용된 Origin [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 선언 정보 |
| Route Leak | [BGP](/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) 하이재킹과 유사한 경로 이상 |
| Anycast | 정상 응답 편차를 만드는 운영 요소 |
| [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) ([Site Reliability 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/)) | 외부 인터넷 이상을 운영 관점에서 흡수하는 역할 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 가용성 모니터링
    |
    v
DNS 응답 무결성 점검 · DNSSEC
    |
    v
BGP 경로 관측 · RPKI · ROA 검증
    |
    v
Passive DNS + Route Collector 상관분석
    |
    v
인터넷 외부 의존성 관측 · 공격/장애 통합 대응
```

이 흐름은 “[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> 인터넷 이름/경로 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> 외부 인터넷 전체 관측”으로 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 관측 범위가 넓어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 인터넷에서 길을 찾으려면 집 주소도 맞아야 하고, 그 집까지 가는 도로도 맞아야 해요.
2. DNS는 주소책이고 BGP는 도로 표지판이라서 둘 중 하나가 속아도 엉뚱한 집에 가게 돼요.
3. 그래서 여러 곳에서 주소와 길을 같이 살펴보는 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링망이 꼭 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 373

<- **이전**: [185. 네트워크 지터 (Network Jitter) 및 패킷 손실 관측 메트릭](/studynote/15_devops_sre/04_iac_cloud_native/185_network_jitter/)
**다음**: [187. OOM (Out of Memory) 킬러 커널 로그 파싱 알람](/studynote/15_devops_sre/04_iac_cloud_native/187_oom_out_of_memory/) ->

---
