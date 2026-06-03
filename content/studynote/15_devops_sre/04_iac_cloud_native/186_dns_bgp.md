---
title: 186. DNS 캐시 중독 및 라우팅 BGP 하이재킹 모니터링망
date: '2026-04-28'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[511_dns_hierarchical_distributed_architecture|DNS]] ([[511_dns_hierarchical_distributed_architecture|Domain Name System]]) 캐시 중독과 [[365_bgp_border_gateway_protocol_path_vector|BGP]] ([[365_bgp_border_gateway_protocol_path_vector|Border Gateway Protocol]]) 하이재킹 [[229_monitor|모니터]]링망은 이름 해석 경로와 [[339_routing_overview_best_path_selection|라우팅]] 경로가 동시에 오염될 수 있다는 전제 아래, **응답 [[003_integrity|무결성]]·경로 [[003_integrity|무결성]]**을 함께 감시하는 관측 체계다.
> 2. **가치**: 사용자 트래픽이 [[752_phishing|피싱]] 사이트나 잘못된 [[344_as_autonomous_system_asn|AS]] (Autonomous System) 경로로 우회되기 전에 탐지해, [[090_service_kubernetes_network_load_balancing|서비스]] 장애와 보안 사고를 조기에 차단할 수 있다.
> 3. **판단 포인트**: [[518_dnssec_dns_security_extensions|DNSSEC]] ([[511_dns_hierarchical_distributed_architecture|Domain Name System]] [[283_security_tactics|Security]] Extensions)와 [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] ([[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|Resource Public Key Infrastructure]])는 [[053_preventive_controls|예방 통제]]이고, [[229_monitor|모니터]]링망은 실제 인터넷 경로에서 일어나는 이상 징후를 다중 시점에서 상시 관찰하는 [[054_detective_controls|탐지 통제]]라는 점이 중요하다.

---

## Ⅰ. 개요 및 필요성

인터넷 [[090_service_kubernetes_network_load_balancing|서비스]]가 정상 동작하려면 두 가지가 동시에 맞아야 한다. 사용자가 질의한 [[064_relation_domain|도메인]]이 올바른 IP 주소로 해석돼야 하고, 그 IP까지 가는 네트워크 경로도 정상이어야 한다. [[511_dns_hierarchical_distributed_architecture|DNS]] 캐시 중독은 [[014_recursion|재귀]] 리졸버(Recursive Resolver)의 응답 캐시를 오염시켜 사용자를 잘못된 주소로 보내고, [[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹은 인터넷 경로 광고를 탈취해 트래픽 자체를 공격자 쪽으로 우회시킨다.

문제는 두 공격 모두 사용자 입장에서는 “그냥 접속이 잘 된다”처럼 보일 수 있다는 점이다. 웹페이지가 열리더라도 공격자가 준비한 위장 서버일 수 있고, [[090_service_kubernetes_network_load_balancing|서비스]] 장애가 없더라도 중간 경로에서 트래픽이 가로채질 수 있다. 따라서 운영자는 단순한 업타임 체크만으로는 부족하고, [[511_dns_hierarchical_distributed_architecture|DNS]] 응답과 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 경로를 별도로 그리고 함께 관찰해야 한다.

특히 [[506_cdn_content_delivery_network_edge_caching|CDN]] (Content Delivery Network), Anycast, 멀티클라우드, 글로벌 [[090_service_kubernetes_network_load_balancing|서비스]]가 보편화되면서 지역별 응답과 경로가 달라지는 것이 정상 상태가 됐다. 이 때문에 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]는 더 어려워졌고, 다수 관측 지점과 정상 [[159_baseline_requirements_configuration_management|베이스라인]]이 필수 조건이 됐다.

- **📢 섹션 요약 비유**: 인터넷 [[090_service_kubernetes_network_load_balancing|서비스]]는 “주소를 제대로 알려 주는 안내판”과 “그 주소까지 가는 도로 표지판”이 모두 맞아야 도착한다. 하나만 틀려도 손님은 엉뚱한 곳으로 간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[229_monitor|모니터]]링망의 핵심은 서로 다른 관측 소스를 한곳에 모아 [[250_cross_validation_kfold|교차 검증]]하는 것이다. [[511_dns_hierarchical_distributed_architecture|DNS]] 측에서는 [[014_recursion|재귀]] 리졸버 응답, 권한 [[511_dns_hierarchical_distributed_architecture|DNS]] 서버 응답, [[294_ttl_time_to_live_looping_prevention|TTL]] ([[294_ttl_time_to_live_looping_prevention|Time To Live]]) 변화, NS·A·AAAA·CNAME 레코드 편차를 본다. [[365_bgp_border_gateway_protocol_path_vector|BGP]] 측에서는 Origin [[344_as_autonomous_system_asn|AS]] 변화, [[344_as_autonomous_system_asn|AS]] Path 길이 급증, Route Leak, ROA (Route Origin [[509_authorization_models_rbac_abac|Authorization]]) invalid 여부, 특정 지역에서만 보이는 경로 편차를 본다.

아래 그림은 DNS와 BGP를 통합 감시하는 대표 구조다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                  DNS + BGP 통합 모니터링망 구성                             │
├──────────────────────────────────────────────────────────────────────────────┤
│ [External DNS Probes]      [Recursive Resolvers]      [Route Collectors]   │
│         │                           │                         │              │
│         ├──────────────┬────────────┴──────────────┬─────────┘              │
│         ▼              ▼                           ▼                        │
│  Answer Diff      TTL Drift / NXDOMAIN      Origin AS / AS Path            │
│         │              │                           │                        │
│         └──────────────┴──────────────┬────────────┘                        │
│                                       ▼                                     │
│                         [Correlation / Detection Engine]                    │
│                                       │                                     │
│                  ┌────────────────────┼────────────────────┐                │
│                  ▼                    ▼                    ▼                │
│          DNSSEC Validate       RPKI Validate      Baseline Compare         │
│                  │                    │                    │                │
│                  └────────────────────┴────────────────────┘                │
│                                       ▼                                     │
│                         [Alert / Ticket / Traffic Mitigation]               │
└──────────────────────────────────────────────────────────────────────────────┘
```

| 관측 항목 | 의미 | 이상 징후 예시 |
| :--- | :--- | :--- |
| [[511_dns_hierarchical_distributed_architecture|DNS]] 응답 편차 | 지역별 응답 값 비교 | 특정 지역만 다른 IP 응답 |
| [[294_ttl_time_to_live_looping_prevention|TTL]] 급감 | 캐시 재주입, 레코드 교체 시도 감지 | 평소 300초인데 갑자기 5초 |
| NS/DS 불일치 | 권한 체인 문제, 위조 가능성 | 서명 [[395_verification_process_review|검증]] 실패 |
| Origin [[344_as_autonomous_system_asn|AS]] 변경 | 원래 광고 주체와 다른 [[344_as_autonomous_system_asn|AS]] 출현 | 갑작스러운 해외 [[344_as_autonomous_system_asn|AS]] 기원 |
| [[344_as_autonomous_system_asn|AS]] Path 비정상 증가 | 우회 또는 누출 가능성 | 평소 4-hop인데 12-hop |
| [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] invalid | 허용되지 않은 경로 광고 | ROA와 다른 Origin 광고 |

핵심은 한 소스만 믿지 않는 것이다. [[511_dns_hierarchical_distributed_architecture|DNS]] 응답이 달라졌더라도 [[506_cdn_content_delivery_network_edge_caching|CDN]] [[164_policy|정책]] 변경일 수 있고, [[365_bgp_border_gateway_protocol_path_vector|BGP]] 경로가 길어졌더라도 일시적 [[339_routing_overview_best_path_selection|라우팅]] 변경일 수 있다. 하지만 [[511_dns_hierarchical_distributed_architecture|DNS]] 응답 편차와 Origin [[344_as_autonomous_system_asn|AS]] 이상이 같은 시각에 동시에 발생하면 사고 가능성이 급격히 높아진다. 그래서 통합 상관분석이 중요하다.

- **📢 섹션 요약 비유**: 길찾기 앱만 보고 가면 주소는 맞아도 도로가 막혔는지 모를 수 있다. 안내판과 도로 CCTV를 같이 봐야 진짜 이상을 빨리 알아차릴 수 있다.

---

## Ⅲ. 비교 및 연결

[[511_dns_hierarchical_distributed_architecture|DNS]] 캐시 중독과 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹은 모두 트래픽을 잘못된 곳으로 보내지만, 공격 지점과 통제 방식은 다르다. [[511_dns_hierarchical_distributed_architecture|DNS]] 중독은 이름 해석 계층을 공격하고, [[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹은 인터넷 [[339_routing_overview_best_path_selection|라우팅]] 계층을 공격한다. 따라서 DNSSEC만으로는 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 문제를 막을 수 없고, RPKI만으로는 위조 [[511_dns_hierarchical_distributed_architecture|DNS]] 응답을 막을 수 없다.

| 비교 축 | [[511_dns_hierarchical_distributed_architecture|DNS]] 캐시 중독 | [[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹 |
| :--- | :--- | :--- |
| 공격 대상 | [[014_recursion|재귀]] 리졸버 캐시, 이름 해석 | 인터넷 경로 광고 |
| 피해 양상 | 위조 IP 응답, [[752_phishing|피싱]] 유도 | 트래픽 우회, [[701_sniffing_eavesdropping_promiscuous|도청]], 블랙홀 |
| 예방 기술 | [[518_dnssec_dns_security_extensions|DNSSEC]], Source [[446_port_and_bus|Port]] Randomization | [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]], Prefix Filtering, [[014_irr_internal_rate_of_return|IRR]] [[395_verification_process_review|검증]] |
| 탐지 [[130_signal|신호]] | 응답 값 변화, [[294_ttl_time_to_live_looping_prevention|TTL]] 이상, 서명 실패 | Origin [[344_as_autonomous_system_asn|AS]] 변화, Path 이상, ROA invalid |
| 운영 주체 | [[511_dns_hierarchical_distributed_architecture|DNS]] 운영팀·보안팀 | 네트워크/[[100_sre_site_reliability_engineering_error_budget|SRE]] 팀·[[101_isp_information_strategy_planning_4_steps|ISP]] 협업 |

[[067_service_operation|서비스 운영]] 측면에서 이 주제는 [[642_observability_telemetry|Observability]], 인터넷 외부 의존성 관리, [[374_supply_chain_security|공급망 보안]]과도 연결된다. 단순 인프라 내부 [[229_monitor|모니터]]링만으로는 인터넷 경계 밖에서 벌어지는 경로 변조를 볼 수 없기 때문이다. 그래서 공개 Route Collector, Passive [[511_dns_hierarchical_distributed_architecture|DNS]], 외부 프로브, [[506_cdn_content_delivery_network_edge_caching|CDN]] 사업자 협업이 함께 필요하다.

- **📢 섹션 요약 비유**: [[511_dns_hierarchical_distributed_architecture|DNS]] 문제가 집 주소를 잘못 적는 일이라면, [[365_bgp_border_gateway_protocol_path_vector|BGP]] 문제는 지도 자체가 바뀌는 일이다. 주소책만 고치거나 지도만 고쳐서는 둘 다 해결되지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 “무엇을 볼 것인가”보다 “어디서 얼마나 자주 볼 것인가”가 더 중요하다. 글로벌 [[090_service_kubernetes_network_load_balancing|서비스]]는 최소한 다수 지역 외부 프로브를 두고, 내부 [[014_recursion|재귀]] 리졸버와 권한 서버 응답을 비교해야 한다. BGP는 자체 피어링이 없더라도 RouteViews, RIPE RIS, Cloud [[150_soa_triangle_architecture|provider]] telemetry 같은 외부 관측원을 활용해 정상 경로를 [[159_baseline_requirements_configuration_management|베이스라인]]으로 저장해야 한다.

### 운영 [[435_checklist_based_testing|체크리스트]]

1. 권한 [[511_dns_hierarchical_distributed_architecture|DNS]] 응답, [[014_recursion|재귀]] 리졸버 응답, 외부 사용자 시점 응답을 모두 수집하는가?
2. 주요 프리픽스(prefix)에 대해 Origin [[344_as_autonomous_system_asn|AS]], ROA 상태, [[344_as_autonomous_system_asn|AS]] Path 변화를 상시 저장하는가?
3. [[518_dnssec_dns_security_extensions|DNSSEC]] 실패와 [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] invalid 알람을 단순 경고가 아니라 사건 처리 흐름으로 연결하는가?
4. [[506_cdn_content_delivery_network_edge_caching|CDN]]·Anycast·멀티클라우드로 인한 정상 편차를 [[159_baseline_requirements_configuration_management|베이스라인]]에 반영했는가?
5. 탐지 후 조치(캐시 플러시, Route Withdraw, [[101_isp_information_strategy_planning_4_steps|ISP]] 연락, 공지)까지 [[637_playbook|플레이북]]이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 내부 헬스체크만으로 인터넷 전체에서의 이상을 본다고 착각하는 경우
- 외부 프로브를 한 지역에만 두어 지역성 공격을 놓치는 경우
- DNSSEC와 RPKI를 켰다는 이유만으로 상시 관측을 소홀히 하는 경우
- 정상 [[294_ttl_time_to_live_looping_prevention|TTL]] 변동, [[506_cdn_content_delivery_network_edge_caching|CDN]] 응답 차이, 교통 우회 [[164_policy|정책]]을 모른 채 오탐을 남발하는 경우

기술사 답안에서는 “[[518_dnssec_dns_security_extensions|DNSSEC]]/[[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] 도입”만 쓰지 말고, **다중 관측 지점, [[159_baseline_requirements_configuration_management|베이스라인]] 비교, 상관분석, 대응 [[637_playbook|플레이북]]**을 함께 써야 [[229_monitor|모니터]]링망 주제가 살아난다. [[053_preventive_controls|예방 통제]]와 [[054_detective_controls|탐지 통제]]를 분리해서 설명하면 더 구조적인 답안이 된다.

- **📢 섹션 요약 비유**: 화재경보기만 달아 놓고 대피 훈련을 안 하면 실제 불이 났을 때 우왕좌왕한다. [[229_monitor|모니터]]링망도 알람 자체보다 알람 이후 동작이 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[511_dns_hierarchical_distributed_architecture|DNS]]·[[365_bgp_border_gateway_protocol_path_vector|BGP]] 통합 [[229_monitor|모니터]]링망의 기대효과는 세 가지다. 첫째, [[752_phishing|피싱]]·경로 탈취 같은 외부 인터넷 사고를 조기에 감지한다. 둘째, 장애와 공격을 구분하는 시간이 짧아져 MTTD (Mean Time To Detect)를 줄인다. 셋째, 사고 시 근거 [[001_dikw_pyramid|데이터]]를 남겨 통신사, 클라우드 사업자, 보안 조직과의 공동 대응이 쉬워진다.

다만 인터넷은 본질적으로 외부 의존성이 큰 환경이어서, 모든 이상을 내부에서 통제할 수는 없다. 따라서 이 주제는 “내 시스템 [[568_logs_distributed_logging_elk_fluentd|로그]]를 잘 보는 법”이 아니라, **인터넷 전체 맥락 속에서 내 [[064_relation_domain|도메인]]과 프리픽스를 어떻게 관측할 것인가**의 문제로 이해해야 한다. DNSSEC와 RPKI가 안전벨트라면, [[229_monitor|모니터]]링망은 주행 중 계기판이다.

- **📢 섹션 요약 비유**: 안전벨트를 맸다고 해서 운전 중 계기판을 안 볼 수는 없다. DNSSEC와 RPKI가 예방 장치라면, [[229_monitor|모니터]]링망은 길이 잘못 들었는지 바로 알려 주는 내비게이션 경고등이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[518_dnssec_dns_security_extensions|DNSSEC]] | [[511_dns_hierarchical_distributed_architecture|DNS]] 응답 [[003_integrity|무결성]] [[395_verification_process_review|검증]] |
| Recursive Resolver | 캐시 중독이 직접 일어나는 지점 |
| Passive [[511_dns_hierarchical_distributed_architecture|DNS]] | 지역별 응답 편차 관측 |
| [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] ([[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|Resource Public Key Infrastructure]]) | [[365_bgp_border_gateway_protocol_path_vector|BGP]] Origin [[395_verification_process_review|검증]] 핵심 |
| ROA (Route Origin [[509_authorization_models_rbac_abac|Authorization]]) | 허용된 Origin [[344_as_autonomous_system_asn|AS]] 선언 정보 |
| Route Leak | [[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹과 유사한 경로 이상 |
| Anycast | 정상 응답 편차를 만드는 운영 요소 |
| [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]]) | 외부 인터넷 이상을 운영 관점에서 흡수하는 역할 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 가용성 모니터링
    │
    ▼
DNS 응답 무결성 점검 · DNSSEC
    │
    ▼
BGP 경로 관측 · RPKI · ROA 검증
    │
    ▼
Passive DNS + Route Collector 상관분석
    │
    ▼
인터넷 외부 의존성 관측 · 공격/장애 통합 대응
```

이 흐름은 “[[090_service_kubernetes_network_load_balancing|서비스]] 내부 상태 [[396_validation|확인]] → 인터넷 이름/경로 [[003_integrity|무결성]] [[396_validation|확인]] → 외부 인터넷 전체 관측”으로 [[100_sre_site_reliability_engineering_error_budget|SRE]] 관측 범위가 넓어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 인터넷에서 길을 찾으려면 집 주소도 맞아야 하고, 그 집까지 가는 도로도 맞아야 해요.
2. DNS는 주소책이고 BGP는 도로 표지판이라서 둘 중 하나가 속아도 엉뚱한 집에 가게 돼요.
3. 그래서 여러 곳에서 주소와 길을 같이 살펴보는 [[229_monitor|모니터]]링망이 꼭 필요해요.
