+++
weight = 4
title = "4. 가용성 (Availability) — HA 설계, RAID, 부하 분산, DDoS 방어, SLA"
description = "시스템의 무중단 운영과 적시적 자원 접근을 보장하기 위한 가용성의 아키텍처 원리, 다중화 설계 및 실무 방어 전략"
date = "2023-10-24"
[taxonomies]
tags = ["정보보안", "가용성", "고가용성(HA)", "DDoS", "단일장애점(SPOF)"]
categories = ["Security", "Principles"]
+++

# [[452_availability|가용성]] ([[452_availability|Availability]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[452_availability|가용성]]은 인가된 사용자가 필요로 하는 시점에 정보 자산과 시스템에 지연이나 중단 없이 즉시 접근할 수 있도록 보장하는 특성이다.
> 2. **가치**: [[002_confidentiality|기밀성]]과 [[003_integrity|무결성]]이 완벽하더라도 시스템이 다운되면 비즈니스 수익이 즉각 0원이 되므로, [[452_availability|가용성]]은 기업 생존과 직결된 가장 경제적인 보안 요소다.
> 3. **융합**: [[452_availability|가용성]]은 단순한 서버 [[456_dual_redundancy|이중화]]를 넘어 클라우드 기반의 탄력적 확장(Auto-scaling), DDoS 완화 아키텍처, 그리고 재해복구([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 체계와 결합된 통합 회복탄력성(Resilience)으로 진화하고 있다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[452_availability|가용성]] ([[452_availability|Availability]])은 정보보안 3요소 중에서 가장 가시적이며 비즈니스 임팩트가 즉각적인 영역이다. 고객의 개인정보가 암호화되어 안전하게 보관되어 있고([[002_confidentiality|기밀성]]), [[001_dikw_pyramid|데이터]]의 위변조가 전혀 일어나지 않았더라도([[003_integrity|무결성]]), 고객이 당장 쇼핑몰에 접속해 결제를 할 수 없다면 시스템은 가치를 상실한 것이다. 

현대의 비즈니스 환경은 1초의 다운타임(Downtime)이 수백만 달러의 손실과 치명적인 평판 하락으로 직결되는 24/365 상시 연결 체제다. 시스템 [[452_availability|가용성]]을 위협하는 요인은 악의적인 DDoS 공격이나 랜섬웨어뿐만 아니라 하드웨어 노후화, 네트워크 단선, 심지어 작업자의 [[009_config|설정]] 실수(Human Error) 등 매우 다양하다. 따라서 [[452_availability|가용성]] 확보란 단순히 공격을 막아내는 것을 넘어, 필연적으로 발생하는 장애 속에서도 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약([[085_sla|SLA]])을 달성할 수 있도록 시스템의 생존 능력을 설계하는 것을 의미한다.

다음 도식은 [[452_availability|가용성]]을 위협하는 [[454_spof|단일 장애점]]([[454_spof|SPOF]])의 문제점과 이를 해결하기 위한 [[071_다중화_Multiplexing|다중화]] 개념을 보여준다.

```text
[기존 구조: 단일 장애점(SPOF) 존재]
User ──> (라우터) ──> (웹 서버) ──> [DB 서버(장애발생!)] ──> 전체 서비스 마비 (가용성 0%)
                                        ▲ 병목 및 파괴 지점

[가용성 확보 구조: 다중화(Redundancy) 및 부하 분산]
               ┌─> (웹 서버 A) ─┐      ┌─> (DB Primary)
User ──> [L4 LB]                ├─[HA]─┤
               └─> (웹 서버 B) ─┘      └─> (DB Replica) (자동 Failover 전환)
```

이 그림의 핵심은 장애를 원천적으로 100% 막는 것은 물리적으로 불가능하므로, 시스템 구조 내에 존재하는 [[454_spof|단일 장애점]](Single Point of Failure)을 식별하고 대체 자원(Redundancy)을 배치하여 우회 경로를 만들어야 한다는 점이다. [[238_switch_operation_principles|스위치]] 하나가 고장나면 [[555_backup_and_restore_strategy|백업]] [[238_switch_operation_principles|스위치]]가 동작하고, 메인 DB가 멈추면 [[016_replication_factor|복제]] DB가 즉각 승격([[300_failover_architecture|Failover]])되어 사용자는 장애를 전혀 인지하지 못하게 만드는 것이 고가용성(HA) 설계의 핵심이다.

**📢 섹션 요약 비유**: 펑크가 나도 일정 거리를 계속 달릴 수 있는 런플랫(Run-flat) 타이어를 장착하거나, 엔진이 두 개인 쌍발기 비행기처럼 한쪽이 고장나도 추락하지 않고 목적지에 도착하게 만드는 공학적 설계입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[452_availability|가용성]]을 보장하는 아키텍처는 인프라 관점의 '[[071_다중화_Multiplexing|다중화]](Redundancy)'와 보안 관점의 '트래픽 정제([[605_golden_silver_ticket_mitigation|Mitigation]])' 기술로 구성된다.

| 구성 요소 | 역할 및 목적 | 내부 동작 메커니즘 | 관련 기술 및 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
|:---|:---|:---|:---|
| **부하 [[136_variance|분산]] ([[196_hard_soft_real_time|Load Balancing]])** | 트래픽 집중으로 인한 서버 마비 방지 | [[178_round_robin_scheduling|라운드 로빈]], Least Connection 알고리즘으로 다수 서버에 부하 분배 | L4/L7 LB, [[511_dns_hierarchical_distributed_architecture|DNS]] 라운드로빈 |
| **[[071_다중화_Multiplexing|다중화]] 및 클러스터링** | 서버, 디스크, 네트워크 회선의 단일 장애 방지 | Active-Active 또는 Active-Standby 상태로 예비 자원 상시 대기 | [[483_raid_overview|RAID]], HAProxy, K8s Replica |
| **트래픽 스크러빙 (Scrubbing)** | DDoS 트래픽 차단 및 정상 트래픽만 통과 유도 | [[365_bgp_border_gateway_protocol_path_vector|BGP]] Anycast로 트래픽을 흡수 후 시그니처와 행위 기반으로 악성 패킷 폐기 | Anti-DDoS 인프라, [[506_cdn_content_delivery_network_edge_caching|CDN]] |
| **[[030_auto_scaling|Auto Scaling]]** | 예측 불가능한 트래픽 급증에 대한 탄력적 대응 | CPU/메모리 [[431_ssthresh_slow_start_threshold|임계치]] 초과 시 클라우드 VM을 동적으로 추가 증설 | AWS EC2 [[030_auto_scaling|Auto Scaling]] |
| **[[379_dr_architecture|재해 복구]] ([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]])** | 자연재해 등 물리적 파괴로부터 [[452_availability|가용성]] 복원 | 수백 km 떨어진 이종 센터로 [[001_dikw_pyramid|데이터]]를 비동기/동기 [[016_replication_factor|복제]] | [[177_rpo_recovery_point_objective|RPO]], [[176_rto_recovery_time_objective|RTO]] 지표 기반 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 센터 |

다음은 해커의 대규모 볼류메트릭(Volumetric) DDoS 공격이 발생했을 때, 방어 아키텍처가 [[452_availability|가용성]]을 지켜내는 순차 흐름도이다.

```text
[Botnet] (100Gbps 정크 트래픽) =====>       (임계치 초과 알람)
[정상 User] (10Mbps 정상 요청) ────>  [Edge 라우터 / BGP]
                                             │
   ┌─────────────────────────────────────────┘ (BGP 라우팅 우회 선언)
   │
   ▼
[Scrubbing Center (DDoS 방어 센터)]
   ├─ 1. 패킷 사이즈/Rate 검사 ────> (UDP Flood, ICMP 드랍)
   ├─ 2. 프로토콜 검사 ────────────> (SYN Flood 방어 - SYN Cookie 적용)
   ├─ 3. L7 행위 검사 ─────────────> (HTTP Slowloris 차단)
   │
   ▼
[정상 User 트래픽만 생존] ───────> [기업 Web Server] (가용성 유지 완료)
```

이 흐름의 핵심은 기업 내부의 [[690_firewall_generation_evolution|방화벽]]이나 대역폭만으로는 수백 기가비트에 달하는 현대의 DDoS 공격을 버틸 수 없다는 점이다. 회선 자체가 가득 차버리는([[123_pipe|Pipe]] Saturation) 상황에서는 서버 단의 방어 로직이 의미가 없다. 따라서 실무에서는 공격 트래픽을 아예 기업망 외부의 대규모 글로벌 클라우드([[250_scrubbing_center|스크러빙 센터]]나 [[506_cdn_content_delivery_network_edge_caching|CDN]])로 [[365_bgp_border_gateway_protocol_path_vector|BGP]]([[365_bgp_border_gateway_protocol_path_vector|Border Gateway Protocol]]) 라우팅을 우회시켜, 그곳에서 오물을 걸러낸 뒤 맑은 물(정상 트래픽)만 파이프로 들여보내는 아웃오브밴드(Out-of-band) 방어 구조를 필수적으로 채택한다.

**📢 섹션 요약 비유**: 댐으로 거대한 홍수(DDoS)가 밀려올 때, 댐의 수문을 닫아버리는 대신([[090_service_kubernetes_network_load_balancing|서비스]] 중단), 거대한 예비 수로([[250_scrubbing_center|스크러빙 센터]])를 열어 흙탕물을 걸러내고 깨끗한 물만 정수장(서버)으로 보내는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[452_availability|가용성]] 설계를 위한 아키텍처 [[268_strategy_pattern|전략]]은 투자 비용과 [[658_ir_recovery|복구]] 시간에 따라 뚜렷한 비교 우위를 가진다.

**1. [[456_dual_redundancy|이중화]] 아키텍처 모드 비교 매트릭스**

```text
┌────────────┬─────────────────────────────┬─────────────┬───────────────┐
│ 구성 방식  │ 동작 특징 및 원리           │ 장점 / 단점 │ 실무 적용 판단│
├────────────┼─────────────────────────────┼─────────────┼───────────────┤
│ Active-    │ 메인 시스템만 처리, 예비는  │ 구성이 단순 / │ 데이터베이스, │
│ Standby    │ 대기 상태. 장애 시 Failover │ 자원 50% 낭비 │ 상태 저장 세션│
├────────────┼─────────────────────────────┼─────────────┼───────────────┤
│ Active-    │ 모든 노드가 동시 트래픽 처리│ 리소스 100% │ 무상태(Stateless)
│ Active     │ 로드밸런서로 부하 완벽 분산 │ 활용 / DB 등  │ 웹 서버, API  │
│            │                             │ 동기화 복잡함 │ 게이트웨이    │
└────────────┴─────────────────────────────┴─────────────┴───────────────┘
```

이 매트릭스의 핵심은 Active-Active 구성이 무조건 좋은 것은 아니라는 점이다. 상태가 없는([[239_stateless_redis|Stateless]]) 웹 서버는 Active-Active로 쉽게 늘릴 수 있지만, [[001_dikw_pyramid|데이터]]베이스를 Active-Active로 구성하면 양쪽에서 동시 쓰기가 발생할 때 심각한 [[194_consistency_database_integrity|일관성]] 충돌([[003_integrity|무결성]] 침해)과 락([[510_lock|Lock]]) 경합 오버헤드를 유발한다. 따라서 실무에서는 프론트엔드는 Active-Active로, 백엔드 [[001_dikw_pyramid|데이터]]베이스는 Active-Standby 구조로 혼용하여 [[452_availability|가용성]]과 [[003_integrity|무결성]]의 밸런스를 맞춘다.

**2. 고가용성과 보안 통제(기밀/[[003_integrity|무결성]]) 간의 충돌 지점**
[[452_availability|가용성]]을 높이기 위해 로드밸런서 뒤에 웹 서버를 무한히 늘리면, 암호화 키 관리([[002_confidentiality|기밀성]])와 [[568_logs_distributed_logging_elk_fluentd|로그]] 통합([[003_integrity|무결성]] 모니터링)이 기하급수적으로 복잡해진다. 모든 노드가 동일한 [[694_thread_local_storage_tls|TLS]] 인증서를 가져야 하므로 키 유출 표면이 넓어진다. 반대로 보안팀이 검증을 위해 지나치게 무거운 보안 에이전트([[325_edr|EDR]], 딥 [[161_inspection_formal_review|인스펙션]] [[690_firewall_generation_evolution|방화벽]])를 서버에 띄우면, CPU 자원을 고갈시켜 스스로 [[090_service_kubernetes_network_load_balancing|서비스]] [[452_availability|가용성]]을 떨어뜨리는 자가당착(Self-[[599_dos_ddos_attack|DoS]])에 빠질 수 있다. 실무에서는 보안 솔루션이 소모하는 자원 [[431_ssthresh_slow_start_threshold|임계치]]를 [[452_availability|가용성]] SLA에 반영하여 철저히 튜닝해야 한다.

**📢 섹션 요약 비유**: 수비수(보안 에이전트)를 그라운드에 너무 많이 배치하면 적(해커)은 막을 수 있겠지만, 아군 공격수([[452_availability|가용성]])가 뛸 공간조차 없어져서 경기를 뛸 수 없게 되는 딜레마와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실무에서 [[452_availability|가용성]] 확보는 기술 도입만으로 끝나지 않으며, [[176_rto_recovery_time_objective|RTO]]/[[177_rpo_recovery_point_objective|RPO]] 지표 기반의 냉정한 비즈니스적 의사결정을 동반한다.

1. **시나리오 1: [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 화재로 인한 [[090_service_kubernetes_network_load_balancing|서비스]] 중단**
   - **상황**: 주 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]](Primary DC)의 전원 공급 중단.
   - **판단**: 즉각 재해복구 센터([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]])로 [[090_service_kubernetes_network_load_balancing|서비스]]를 전환해야 한다. 이때 핵심 판단 기준은 **[[176_rto_recovery_time_objective|RTO]] ([[176_rto_recovery_time_objective|Recovery Time Objective]]: [[658_ir_recovery|복구]] 목표 시간)**와 **[[177_rpo_recovery_point_objective|RPO]] ([[177_rpo_recovery_point_objective|Recovery Point Objective]]: [[658_ir_recovery|복구]] 목표 시점)**다. 금융권의 경우 RPO가 0([[001_dikw_pyramid|데이터]] 유실 없음)이어야 하므로 평소에 동기식([[010_동기식_비동기식_전송|Synchronous]]) [[001_dikw_pyramid|데이터]] [[016_replication_factor|복제]]를 해야 하지만, 이로 인해 평상시 레이턴시가 증가한다. 일반 쇼핑몰은 [[177_rpo_recovery_point_objective|RPO]] 1시간을 허용하고 비동기 [[016_replication_factor|복제]]를 통해 [[452_availability|가용성]] 오버헤드를 줄이는 [[268_strategy_pattern|전략]]적 선택을 해야 한다.

2. **시나리오 2: [[532_microservices_decomposition_patterns|마이크로서비스]] 연쇄 장애 (Cascading Failure)**
   - **상황**: A [[090_service_kubernetes_network_load_balancing|서비스]]가 B API를 호출하는데 B 서버가 느려짐. A가 응답을 기다리다 스레드가 고갈되어 A까지 다운됨.
   - **판단**: 단일 노드의 장애가 전체 시스템의 [[452_availability|가용성]]을 무너뜨리는 전형적인 패턴이다. 이 경우 클라우드 아키텍처의 핵심 디자인 패턴인 **[[307_circuit_breaker_pattern|서킷 브레이커]]([[304_circuit_breaker|Circuit Breaker]])**를 도입해야 한다. B의 응답이 계속 지연되면 A는 B로의 연결을 스스로 끊어버리고(Open 상태) 미리 준비된 캐시나 기본값([[129_fallback|Fallback]])을 사용자에게 반환하여 A 시스템의 [[452_availability|가용성]]을 사수([[460_fail_soft|Fail-Soft]])해야 한다.

다음은 시스템 장애 시 [[307_circuit_breaker_pattern|서킷 브레이커]] 패턴이 [[452_availability|가용성]]을 방어하는 상태 전이도이다.

```text
         (정상 응답률 하락 감지)
[CLOSED] ───────────────────────> [OPEN] (요청 즉시 차단, Fallback 응답)
(정상 통신)                         │
   ▲                               │ (일정 시간(Timeout) 대기)
   │                               ▼
   └──────── (테스트 패킷 성공) ── [HALF-OPEN] (소량의 테스트 요청만 허용)
```

이 상태 전이도의 핵심은 "망가진 서버에 계속 채찍질을 하면 완전히 죽어버린다"는 엔지니어링 원리다. 장애가 난 백엔드 서버가 스스로 회복할 시간을 주기 위해 [[690_firewall_generation_evolution|방화벽]]이나 애플리케이션 프록시가 알아서 트래픽을 차단(OPEN)해주는 것이 역설적으로 전체 [[452_availability|가용성]]을 살리는 길이다. 실무에서는 이러한 [[171_fallback_resilience_pattern|폴백]]([[129_fallback|Fallback]]) 체계 설계 유무가 초급 아키텍처와 고급 아키텍처를 가르는 기준이 된다.

**📢 섹션 요약 비유**: 전력망에서 누전이 발생했을 때 두꺼비집([[307_circuit_breaker_pattern|서킷 브레이커]])이 알아서 전기를 차단해주어 집안 전체에 화재가 번지는 것을 막고, 집 전체의 구조적 [[452_availability|가용성]]을 살리는 것과 정확히 같은 원리입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

견고하게 설계된 [[452_availability|가용성]] 아키텍처는 기업의 브랜드 가치를 지키고 사용자 이탈을 막는 최고의 비즈니스 보험이다.

| 기대효과 구분 | [[454_spof|단일 장애점]] 방치 환경 | 고가용성/[[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 아키텍처 적용 | 비즈니스 임팩트 ([[085_sla|SLA]]) |
|:---|:---|:---|:---|
| **[[090_service_kubernetes_network_load_balancing|서비스]] 가용 시간** | 99% (연간 87.6시간 중단) | 99.999% (연간 5.26분 중단) | [[090_service_kubernetes_network_load_balancing|서비스]] [[085_confidence_association_rule_conditional_probability|신뢰도]] 최상위 등급 확보 |
| **장애 인지 및 대응**| 고객 신고 후 수동 재부팅 (수 시간) | L4/L7 헬스체크 및 자동 [[300_failover_architecture|Failover]] (수 초) | 무인 자동화 [[658_ir_recovery|복구]] 체계 실현 |
| **보안 공격 내성** | 소규모 [[599_dos_ddos_attack|DoS]] 공격에도 쉽게 마비 | [[506_cdn_content_delivery_network_edge_caching|CDN]]/Anycast로 초거대 DDoS 공격 흡수 | 외부 위협으로부터의 생존성 보장 |

미래의 [[452_availability|가용성]] 기술은 물리적 서버의 [[456_dual_redundancy|이중화]]를 넘어 클라우드 네이티브의 **[[751_chaos_engineering|카오스 엔지니어링]]([[751_chaos_engineering|Chaos Engineering]])**과 **[[206_serverless_cold_start|서버리스]]([[206_serverless_cold_start|Serverless]])**로 진화하고 있다. 평상시에 일부러 서버에 장애를 발생시켜 [[658_ir_recovery|복구]] 시스템이 정상 동작하는지 테스트(Netflix의 [[149_chaos_monkey_chaos_mesh|Chaos Monkey]] 등)함으로써 [[452_availability|가용성]] 아키텍처의 약점을 선제적으로 도출하는 것이 글로벌 표준이 되고 있다. 정보보안 기술사 관점에서 [[452_availability|가용성]]은 막연히 '안 끊기는 것'이 아니라, [[176_rto_recovery_time_objective|RTO]], [[177_rpo_recovery_point_objective|RPO]], SLA라는 명확한 정량적 수치로 설계되고 비즈니스 요구사항에 의해 비용-효익이 검증되어야 하는 구조적 영역이다.

**📢 섹션 요약 비유**: 최고의 [[452_availability|가용성]]은 단순히 튼튼한 성벽을 짓는 것이 아니라, 성벽 일부가 무너져도 성 안의 사람들은 아무것도 느끼지 못한 채 벽이 스스로 수리되는 마법 같은 자가 치유(Self-Healing) 생태계를 구축하는 것입니다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[454_spof|SPOF]] (Single Point of Failure)** | 시스템 전체를 마비시킬 수 있는 유일하고 치명적인 약점 노드
- **[[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]])** | 타 시스템 장애가 내 시스템으로 전파되는 것을 막는 소프트웨어 패턴
- **DDoS (Distributed Denial of [[090_service_kubernetes_network_load_balancing|Service]])** | 해커가 [[452_availability|가용성]]을 파괴하기 위해 가장 흔하게 사용하는 자원 고갈 공격 기법
- **[[379_dr_architecture|재해 복구]] (Disaster [[658_ir_recovery|Recovery]])** | [[177_rpo_recovery_point_objective|RPO]]/[[176_rto_recovery_time_objective|RTO]] 지표를 기준으로 자연재해 시에도 비즈니스 연속성(BCP)을 유지하는 [[268_strategy_pattern|전략]]
- **[[506_cdn_content_delivery_network_edge_caching|CDN]] (Content Delivery Network)** | 엣지 로케이션에 정적 [[001_dikw_pyramid|데이터]]를 캐싱하여 메인 서버의 부하를 줄이고 글로벌 [[452_availability|가용성]]을 높이는 망

### 📈 관련 키워드 및 발전 흐름도

```text
[SPOF (Single Point of Failure)]
    │
    ▼
[서킷 브레이커 (Circuit Breaker)]
    │
    ▼
[DDoS (Distributed Denial of Service)]
    │
    ▼
[재해 복구 (Disaster Recovery)]
    │
    ▼
[CDN (Content Delivery Network)]
```

이 흐름도는 [[454_spof|SPOF]] (Single Point of Failure)에서 출발해 [[506_cdn_content_delivery_network_edge_caching|CDN]] (Content Delivery Network)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **[[452_availability|가용성]]**: 내가 좋아하는 애니메이션을 보고 싶을 때, TV가 고장 나거나 채널이 안 나오는 일 없이 언제나 볼 수 있는 거예요.
2. **원리**: 거실 TV가 고장 나면 태블릿으로 바로 이어볼 수 있게 준비해 두고([[071_다중화_Multiplexing|다중화]]), 나쁜 마녀가 전파를 방해하면 요정들이 전파를 씻어서(스크러빙) 깨끗하게 만들어줘요.
3. **효과**: 그래서 비가 오나 눈이 오나, 언제 어디서든 내 애니메이션은 절대 끊기지 않고 재미있게 볼 수 있답니다.
