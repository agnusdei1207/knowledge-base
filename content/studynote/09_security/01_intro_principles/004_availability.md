+++
title = "4. 가용성 (Availability) — HA 설계, RAID, 부하 분산, DDoS 방어, SLA"
description = "시스템의 무중단 운영과 적시적 자원 접근을 보장하기 위한 가용성의 아키텍처 원리, 다중화 설계 및 실무 방어 전략"
date = 2023-10-24

[taxonomies]
tags = ["security"]

[extra]
tags = ["security"]
+++

# [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 인가된 사용자가 필요로 하는 시점에 정보 자산과 시스템에 지연이나 중단 없이 즉시 접근할 수 있도록 보장하는 특성이다.
> 2. **가치**: [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 완벽하더라도 시스템이 다운되면 비즈니스 수익이 즉각 0원이 되므로, [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 기업 생존과 직결된 가장 경제적인 보안 요소다.
> 3. **융합**: [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 단순한 서버 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)를 넘어 클라우드 기반의 탄력적 확장(Auto-scaling), DDoS 완화 아키텍처, 그리고 재해복구([DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)) 체계와 결합된 통합 회복탄력성(Resilience)으로 진화하고 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))은 정보보안 3요소 중에서 가장 가시적이며 비즈니스 임팩트가 즉각적인 영역이다. 고객의 개인정보가 암호화되어 안전하게 보관되어 있고([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 위변조가 전혀 일어나지 않았더라도([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)), 고객이 당장 쇼핑몰에 접속해 결제를 할 수 없다면 시스템은 가치를 상실한 것이다.

현대의 비즈니스 환경은 1초의 다운타임(Downtime)이 수백만 달러의 손실과 치명적인 평판 하락으로 직결되는 24/365 상시 연결 체제다. 시스템 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 위협하는 요인은 악의적인 DDoS 공격이나 랜섬웨어뿐만 아니라 하드웨어 노후화, 네트워크 단선, 심지어 작업자의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 실수(Human Error) 등 매우 다양하다. 따라서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 확보란 단순히 공격을 막아내는 것을 넘어, 필연적으로 발생하는 장애 속에서도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))을 달성할 수 있도록 시스템의 생존 능력을 설계하는 것을 의미한다.

다음 도식은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 위협하는 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))의 문제점과 이를 해결하기 위한 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 개념을 보여준다.

```text
[기존 구조: 단일 장애점(SPOF) 존재]
User --> (라우터) --> (웹 서버) --> [DB 서버(장애발생!)] --> 전체 서비스 마비 (가용성 0%)
                                        ^ 병목 및 파괴 지점

[가용성 확보 구조: 다중화(Redundancy) 및 부하 분산]
               +-> (웹 서버 A) -+      +-> (DB Primary)
User --> [L4 LB]                +-[HA]-+
               +-> (웹 서버 B) -+      +-> (DB Replica) (자동 Failover 전환)
```

이 그림의 핵심은 장애를 원천적으로 100% 막는 것은 물리적으로 불가능하므로, 시스템 구조 내에 존재하는 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)(Single Point of Failure)을 식별하고 대체 자원(Redundancy)을 배치하여 우회 경로를 만들어야 한다는 점이다. [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 하나가 고장나면 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 동작하고, 메인 DB가 멈추면 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) DB가 즉각 승격([Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/))되어 사용자는 장애를 전혀 인지하지 못하게 만드는 것이 고가용성(HA) 설계의 핵심이다.

**📢 섹션 요약 비유**: 펑크가 나도 일정 거리를 계속 달릴 수 있는 런플랫(Run-flat) 타이어를 장착하거나, 엔진이 두 개인 쌍발기 비행기처럼 한쪽이 고장나도 추락하지 않고 목적지에 도착하게 만드는 공학적 설계입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 보장하는 아키텍처는 인프라 관점의 '[다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)(Redundancy)'와 보안 관점의 '트래픽 정제([Mitigation](/knowledge-base/studynote/09_security/12_identity_threat_advanced/605_golden_silver_ticket_mitigation/))' 기술로 구성된다.

| 구성 요소 | 역할 및 목적 | 내부 동작 메커니즘 | 관련 기술 및 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
|:---|:---|:---|:---|
| <strong>부하 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> (<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/">Load Balancing</a>)</strong> | 트래픽 집중으로 인한 서버 마비 방지 | [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/), Least Connection 알고리즘으로 다수 서버에 부하 분배 | L4/L7 LB, [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 라운드로빈 |
| <strong><a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/">다중화</a> 및 클러스터링</strong> | 서버, 디스크, 네트워크 회선의 단일 장애 방지 | Active-Active 또는 Active-Standby 상태로 예비 자원 상시 대기 | [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/), HAProxy, K8s Replica |
| **트래픽 스크러빙 (Scrubbing)** | DDoS 트래픽 차단 및 정상 트래픽만 통과 유도 | [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/) Anycast로 트래픽을 흡수 후 시그니처와 행위 기반으로 악성 패킷 폐기 | Anti-DDoS 인프라, [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/">Auto Scaling</a></strong> | 예측 불가능한 트래픽 급증에 대한 탄력적 대응 | CPU/메모리 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 초과 시 클라우드 VM을 동적으로 추가 증설 | AWS EC2 [Auto Scaling](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a> (<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/">DR</a>)</strong> | 자연재해 등 물리적 파괴로부터 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 복원 | 수백 km 떨어진 이종 센터로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비동기/동기 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) 지표 기반 [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 센터 |

다음은 해커의 대규모 볼류메트릭(Volumetric) DDoS 공격이 발생했을 때, 방어 아키텍처가 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 지켜내는 순차 흐름도이다.

```text
[Botnet] (100Gbps 정크 트래픽) =====>       (임계치 초과 알람)
[정상 User] (10Mbps 정상 요청) ---->  [Edge 라우터 / BGP]
                                             |
   +-----------------------------------------+ (BGP 라우팅 우회 선언)
   |
   v
[Scrubbing Center (DDoS 방어 센터)]
   +- 1. 패킷 사이즈/Rate 검사 ----> (UDP Flood, ICMP 드랍)
   +- 2. 프로토콜 검사 ------------> (SYN Flood 방어 - SYN Cookie 적용)
   +- 3. L7 행위 검사 -------------> (HTTP Slowloris 차단)
   |
   v
[정상 User 트래픽만 생존] -------> [기업 Web Server] (가용성 유지 완료)
```

이 흐름의 핵심은 기업 내부의 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이나 대역폭만으로는 수백 기가비트에 달하는 현대의 DDoS 공격을 버틸 수 없다는 점이다. 회선 자체가 가득 차버리는([Pipe](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) Saturation) 상황에서는 서버 단의 방어 로직이 의미가 없다. 따라서 실무에서는 공격 트래픽을 아예 기업망 외부의 대규모 글로벌 클라우드([스크러빙 센터](/knowledge-base/studynote/09_security/03_network_security/250_scrubbing_center/)나 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/))로 [BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/)([Border Gateway Protocol](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/)) 라우팅을 우회시켜, 그곳에서 오물을 걸러낸 뒤 맑은 물(정상 트래픽)만 파이프로 들여보내는 아웃오브밴드(Out-of-band) 방어 구조를 필수적으로 채택한다.

**📢 섹션 요약 비유**: 댐으로 거대한 홍수(DDoS)가 밀려올 때, 댐의 수문을 닫아버리는 대신([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단), 거대한 예비 수로([스크러빙 센터](/knowledge-base/studynote/09_security/03_network_security/250_scrubbing_center/))를 열어 흙탕물을 걸러내고 깨끗한 물만 정수장(서버)으로 보내는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 설계를 위한 아키텍처 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 투자 비용과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간에 따라 뚜렷한 비교 우위를 가진다.

<strong>1. <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/">이중화</a> 아키텍처 모드 비교 매트릭스</strong>

```text
+------------+-----------------------------+-------------+---------------+
| 구성 방식  | 동작 특징 및 원리           | 장점 / 단점 | 실무 적용 판단|
+------------+-----------------------------+-------------+---------------+
| Active-    | 메인 시스템만 처리, 예비는  | 구성이 단순 / | 데이터베이스, |
| Standby    | 대기 상태. 장애 시 Failover | 자원 50% 낭비 | 상태 저장 세션|
+------------+-----------------------------+-------------+---------------+
| Active-    | 모든 노드가 동시 트래픽 처리| 리소스 100% | 무상태(Stateless)
| Active     | 로드밸런서로 부하 완벽 분산 | 활용 / DB 등  | 웹 서버, API  |
|            |                             | 동기화 복잡함 | 게이트웨이    |
+------------+-----------------------------+-------------+---------------+
```

이 매트릭스의 핵심은 Active-Active 구성이 무조건 좋은 것은 아니라는 점이다. 상태가 없는([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) 웹 서버는 Active-Active로 쉽게 늘릴 수 있지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 Active-Active로 구성하면 양쪽에서 동시 쓰기가 발생할 때 심각한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 충돌([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 침해)과 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 경합 오버헤드를 유발한다. 따라서 실무에서는 프론트엔드는 Active-Active로, 백엔드 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스는 Active-Standby 구조로 혼용하여 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)의 밸런스를 맞춘다.

<strong>2. 고가용성과 보안 통제(기밀/<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>) 간의 충돌 지점</strong>
[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 높이기 위해 로드밸런서 뒤에 웹 서버를 무한히 늘리면, 암호화 키 관리([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 통합([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 모니터링)이 기하급수적으로 복잡해진다. 모든 노드가 동일한 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 인증서를 가져야 하므로 키 유출 표면이 넓어진다. 반대로 보안팀이 검증을 위해 지나치게 무거운 보안 에이전트([EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/), 딥 [인스펙션](/knowledge-base/studynote/12_it_management/04_sdlc_testing/161_inspection_formal_review/) [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))를 서버에 띄우면, CPU 자원을 고갈시켜 스스로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 떨어뜨리는 자가당착(Self-[DoS](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/))에 빠질 수 있다. 실무에서는 보안 솔루션이 소모하는 자원 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) SLA에 반영하여 철저히 튜닝해야 한다.

**📢 섹션 요약 비유**: 수비수(보안 에이전트)를 그라운드에 너무 많이 배치하면 적(해커)은 막을 수 있겠지만, 아군 공격수([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))가 뛸 공간조차 없어져서 경기를 뛸 수 없게 되는 딜레마와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 확보는 기술 도입만으로 끝나지 않으며, [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/[RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 지표 기반의 냉정한 비즈니스적 의사결정을 동반한다.

1. <strong>시나리오 1: <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/">데이터센터</a> 화재로 인한 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 중단</strong>
   - **상황**: 주 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)(Primary DC)의 전원 공급 중단.
   - **판단**: 즉각 재해복구 센터([DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/))로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 전환해야 한다. 이때 핵심 판단 기준은 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/">RTO</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/">Recovery Time Objective</a>: <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 목표 시간)</strong>와 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/">RPO</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/">Recovery Point Objective</a>: <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 목표 시점)</strong>다. 금융권의 경우 RPO가 0([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 없음)이어야 하므로 평소에 동기식([Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 해야 하지만, 이로 인해 평상시 레이턴시가 증가한다. 일반 쇼핑몰은 [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 1시간을 허용하고 비동기 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 통해 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 오버헤드를 줄이는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 선택을 해야 한다.

2. <strong>시나리오 2: <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> 연쇄 장애 (Cascading Failure)</strong>
   - **상황**: A [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 B API를 호출하는데 B 서버가 느려짐. A가 응답을 기다리다 스레드가 고갈되어 A까지 다운됨.
   - **판단**: 단일 노드의 장애가 전체 시스템의 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 무너뜨리는 전형적인 패턴이다. 이 경우 클라우드 아키텍처의 핵심 디자인 패턴인 <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/">서킷 브레이커</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/">Circuit Breaker</a>)</strong>를 도입해야 한다. B의 응답이 계속 지연되면 A는 B로의 연결을 스스로 끊어버리고(Open 상태) 미리 준비된 캐시나 기본값([Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/))을 사용자에게 반환하여 A 시스템의 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 사수([Fail-Soft](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/460_fail_soft/))해야 한다.

다음은 시스템 장애 시 [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 패턴이 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 방어하는 상태 전이도이다.

```text
         (정상 응답률 하락 감지)
[CLOSED] -----------------------> [OPEN] (요청 즉시 차단, Fallback 응답)
(정상 통신)                         |
   ^                               | (일정 시간(Timeout) 대기)
   |                               v
   +-------- (테스트 패킷 성공) -- [HALF-OPEN] (소량의 테스트 요청만 허용)
```

이 상태 전이도의 핵심은 "망가진 서버에 계속 채찍질을 하면 완전히 죽어버린다"는 엔지니어링 원리다. 장애가 난 백엔드 서버가 스스로 회복할 시간을 주기 위해 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이나 애플리케이션 프록시가 알아서 트래픽을 차단(OPEN)해주는 것이 역설적으로 전체 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 살리는 길이다. 실무에서는 이러한 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)([Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)) 체계 설계 유무가 초급 아키텍처와 고급 아키텍처를 가르는 기준이 된다.

**📢 섹션 요약 비유**: 전력망에서 누전이 발생했을 때 두꺼비집([서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/))이 알아서 전기를 차단해주어 집안 전체에 화재가 번지는 것을 막고, 집 전체의 구조적 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 살리는 것과 정확히 같은 원리입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

견고하게 설계된 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 아키텍처는 기업의 브랜드 가치를 지키고 사용자 이탈을 막는 최고의 비즈니스 보험이다.

| 기대효과 구분 | [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 방치 환경 | 고가용성/[DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 아키텍처 적용 | 비즈니스 임팩트 ([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 가용 시간</strong> | 99% (연간 87.6시간 중단) | 99.999% (연간 5.26분 중단) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 최상위 등급 확보 |
| **장애 인지 및 대응**| 고객 신고 후 수동 재부팅 (수 시간) | L4/L7 헬스체크 및 자동 [Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) (수 초) | 무인 자동화 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계 실현 |
| **보안 공격 내성** | 소규모 [DoS](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격에도 쉽게 마비 | [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/)/Anycast로 초거대 DDoS 공격 흡수 | 외부 위협으로부터의 생존성 보장 |

미래의 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 기술은 물리적 서버의 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)를 넘어 클라우드 네이티브의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/">카오스 엔지니어링</a>(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/">Chaos 엔진ering</a>)</strong>과 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">Serverless</a>)</strong>로 진화하고 있다. 평상시에 일부러 서버에 장애를 발생시켜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시스템이 정상 동작하는지 테스트(Netflix의 [Chaos Monkey](/knowledge-base/studynote/15_devops_sre/03_sre_observability/149_chaos_monkey_chaos_mesh/) 등)함으로써 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 아키텍처의 약점을 선제적으로 도출하는 것이 글로벌 표준이 되고 있다. 정보보안 기술사 관점에서 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 막연히 '안 끊기는 것'이 아니라, [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), SLA라는 명확한 정량적 수치로 설계되고 비즈니스 요구사항에 의해 비용-효익이 검증되어야 하는 구조적 영역이다.

**📢 섹션 요약 비유**: 최고의 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 단순히 튼튼한 성벽을 짓는 것이 아니라, 성벽 일부가 무너져도 성 안의 사람들은 아무것도 느끼지 못한 채 벽이 스스로 수리되는 마법 같은 자가 치유(Self-Healing) 생태계를 구축하는 것입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a> (Single Point of Failure)</strong> | 시스템 전체를 마비시킬 수 있는 유일하고 치명적인 약점 노드
- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/">서킷 브레이커</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/">Circuit Breaker</a>)</strong> | 타 시스템 장애가 내 시스템으로 전파되는 것을 막는 소프트웨어 패턴
- <strong>DDoS (Distributed Denial of <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a>)</strong> | 해커가 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 파괴하기 위해 가장 흔하게 사용하는 자원 고갈 공격 기법
- <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a> (Disaster <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">Recovery</a>)</strong> | [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)/[RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) 지표를 기준으로 자연재해 시에도 비즈니스 연속성(BCP)을 유지하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)
- <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/">CDN</a> (Content Delivery Network)</strong> | 엣지 로케이션에 정적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 캐싱하여 메인 서버의 부하를 줄이고 글로벌 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 높이는 망

### 📈 관련 키워드 및 발전 흐름도

```text
[SPOF (Single Point of Failure)]
    |
    v
[서킷 브레이커 (Circuit Breaker)]
    |
    v
[DDoS (Distributed Denial of Service)]
    |
    v
[재해 복구 (Disaster Recovery)]
    |
    v
[CDN (Content Delivery Network)]
```

이 흐름도는 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure)에서 출발해 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) (Content Delivery Network)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong>: 내가 좋아하는 애니메이션을 보고 싶을 때, TV가 고장 나거나 채널이 안 나오는 일 없이 언제나 볼 수 있는 거예요.
2. **원리**: 거실 TV가 고장 나면 태블릿으로 바로 이어볼 수 있게 준비해 두고([다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)), 나쁜 마녀가 전파를 방해하면 요정들이 전파를 씻어서(스크러빙) 깨끗하게 만들어줘요.
3. **효과**: 그래서 비가 오나 눈이 오나, 언제 어디서든 내 애니메이션은 절대 끊기지 않고 재미있게 볼 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 4 / 1108

<- **이전**: [3. 무결성 (Integrity) — 해시, 전자서명, MAC, HMAC, 체크섬](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)
**다음**: [5. 인증성 (Authenticity) — 신원 확인, PKI, 디지털 서명, 메시지 인증](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/) ->

---
