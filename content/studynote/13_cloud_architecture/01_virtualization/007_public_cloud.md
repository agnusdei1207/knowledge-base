+++
title = "7. 퍼블릭 클라우드 (Public Cloud) - 다수의 기업이 공유하는 공용 인프라 (AWS, Azure, GCP)"
description = "초기 투자 없이 무한한 확장성을 제공하는 공용 인프라의 다중 테넌트 아키텍처 메커니즘과 실무 도입 전략"
date = 2024-05-24

[taxonomies]
tags = ["cloud_architecture"]

[extra]
tags = ["cloud_architecture"]
+++

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 글로벌 하이퍼스케일러(AWS, Azure, GCP)가 구축한 거대한 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 자원을 다수의 테넌트(고객)가 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 기술을 통해 논리적으로 나누어 쓰는 IT 인프라 온디맨드 제공 모델.
> 2. **가치**: 막대한 CAPEX(자본 지출)를 사용량 기반의 OPEX(운영 지출)로 전환하여, 비즈니스 아이디어를 즉각적으로 실험하고 글로벌 시장으로 즉시 진출할 수 있는 민첩성(Agility)을 부여.
> 3. **융합**: 고속 네트워크 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 기술, [컨테이너 오케스트레이션](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML) 매니지드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 융합되어 현대 기업의 IT 디지털 트랜스포메이션의 심장부 역할을 수행.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

**전통적 IT 인프라의 한계와 퍼블릭 클라우드의 혁신**
과거의 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) 환경에서는 새로운 비즈니스 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 론칭하려면 서버 하드웨어 발주, 네트워크 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 공사, OS 설치 등 수 개월의 리드 타임과 막대한 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 자본 투자가 수반되었다. 더욱이, 블랙 프라이데이와 같은 피크 트래픽을 대비해 구매한 장비들은 평상시에는 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20%의 활용률에 머무르며 막대한 유지보수 비용과 공간적 낭비를 발생시켰다.
퍼블릭 클라우드 (Public Cloud)는 이러한 물리적 경직성을 타파하고, 전기나 수도처럼 IT 자원을 "필요한 순간에 필요한 용량만큼만" API를 통해 끌어다 쓰고 요금을 지불하는 완벽한 유틸리티 컴퓨팅(Utility Computing) 모델을 실현했다. 

**💡 비유**: 예전에는 여행을 갈 때마다 자동차를 직접 사서 주차장을 마련하고 엔진오일을 갈아야 했다면, 퍼블릭 클라우드는 스마트폰 앱으로 전 세계 어디서나 즉시 차를 빌려 타고 달린 거리만큼만 결제하는 글로벌 카셰어링 혁신과 같다.

이 도식은 기존 CAPEX 기반 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)의 고정된 인프라 확장 방식과 퍼블릭 클라우드의 OPEX 기반 탄력적 확장을 비교한 문제 배경도이다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">인프라 조달 타이밍 및 비용 지출 구조의 한계</div></div>
<div class="kb-diagram-note">용량 (Capacity)</div>
<div class="kb-diagram-connector">▲</div>
<div class="kb-diagram-note">(유휴 자원 낭비 - 막대한 손실)</div>
<div class="kb-diagram-note">(트래픽 스파이크 시 용량 부족 = 시스템 다운!)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">On-Prem</div><div class="kb-diagram-cell">/ \</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">/ \ 트래픽 (실 수요 곡선)</div>
<div class="kb-diagram-note">Public Cloud / \</div>
<div class="kb-diagram-note">(Auto Scaling) / \</div>
<div class="kb-diagram-tree-item" style="--depth:0">시간 (Time)</div>
</div>
</div>


이 그림의 핵심은 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)(계단식 블록) 인프라 도입 방식이 가진 태생적 모순을 보여주는 데 있다. 장비 도입 속도가 트래픽 증가 속도를 따라가지 못하면 치명적인 장애를 겪고, 반대로 너무 미리 도입하면 빈 공간(유휴 자원)만큼 돈을 버리게 된다. 반면 퍼블릭 클라우드의 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 곡선(점선과 밀착)은 실제 수요를 그림자처럼 추적하여 비즈니스 민첩성을 극대화한다. 따라서 트래픽 변동성이 크거나 신규 사업 실험을 해야 하는 기업에게 퍼블릭 클라우드는 필수불가결한 선택이다.

**📢 섹션 요약 비유**: 두꺼운 겨울옷을 한여름에도 억지로 입고 다니던 방식에서 벗어나, 외부 온도 변화에 맞춰 스마트하게 실시간으로 옷의 두께가 조절되는 마법의 옷으로 갈아입은 격이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

<strong>퍼블릭 클라우드의 구조적 기반: <a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">멀티 테넌시</a>와 <a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a></strong>
퍼블릭 클라우드는 단일 기업이 물리 서버를 독점하는 것이 아니라, 거대한 서버 팜(Server Farm)을 다수의 고객이 안전하게 공유하는 [멀티 테넌시](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)([Multi-Tenancy](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)) 아키텍처를 근간으로 한다. 이를 가능하게 하는 핵심 기술이 강력한 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 기반의 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))와 논리적 네트워크 격리 기술([VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/))이다.

| 계층 (Layer) | 구성 요소 | 역할 및 핵심 기술 | 비유 |
|:---|:---|:---|:---|
| **Global Infra** | Region & AZ | 지진/정전 대비 물리적으로 분리된 글로벌 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 네트워크 | 전 세계 체인 호텔 지점 |
| <strong>Network (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a>)</strong>| [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) ([가상 사설망](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)) | 공용 망 내에서 특정 고객만의 논리적, 암호화된 독립 네트워크 구축 | 호텔 내 VIP 전용 프라이빗 층 |
| <strong>Compute (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>)</strong> | [Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) | 물리 CPU/RAM을 쪼개어 수십 개의 독립된 인스턴스(Guest OS) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 큰 홀을 나누는 방음 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) |
| <strong>Storage (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/">SDS</a>)</strong>| Block & Object | EBS([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 직접 [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/)) 및 S3([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반 무한 확장 객체 저장소) | 개인 금고 및 무한 공용 창고 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a></strong> | Control Plane | 사용자의 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청([프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/))을 수신해 하드웨어 자원을 할당 | 호텔 프런트 데스크 시스템 |

이 도식은 퍼블릭 클라우드의 물리적 가용성을 보장하는 리전(Region)과 가용 영역(AZ, [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) Zone), 그리고 그 위에서 동작하는 [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) 네트워크의 논리적 격리 아키텍처를 보여준다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Public Cloud (Global)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Region A (e.g., ap-northeast-2)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AZ 1 (물리적 독립 DC) ─ AZ 2 (물리적 독립) ──</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VPC (가상 사설망)</div><div class="kb-diagram-cell">VPC (확장 Subnet) ──</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">│ │</div><div class="kb-diagram-node">Web VM / 웹 VM</div><div class="kb-diagram-node">DB VM</div><div class="kb-diagram-note">│==│</div><div class="kb-diagram-node">Web VM / 웹 VM</div><div class="kb-diagram-node">DB VM</div><div class="kb-diagram-note">│ │</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(전원/네트워크/냉각 완전 분리)</div><div class="kb-diagram-cell">(초고속 전용 광케이블 연결)</div></div>
</div>
</div>


이 구조도의 핵심은 클라우드가 절대 죽지 않는 마법의 서버가 아니라, "하나의 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)(AZ)가 재난으로 완전히 파괴되어도 시스템이 생존하도록 물리적으로 설계된 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 네트워크"라는 점이다. AZ 1과 AZ 2는 지리적으로 수십 킬로미터 떨어져 1개 도시의 정전이나 홍수에도 동시 타격을 받지 않으며, 두 AZ 간은 밀리초 수준의 초고속망으로 연결되어 동기화된다. 따라서 실무 설계자는 반드시 이 다이어그램처럼 로드밸런서를 두고 웹과 DB를 두 개 이상의 AZ에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배치(Multi-AZ)하는 것을 클라우드 아키텍처의 제1원칙으로 삼아야 한다.

**📢 섹션 요약 비유**: 퍼블릭 클라우드는 거대한 아파트 단지([멀티 테넌시](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/))와 같다. 비록 다른 사람들과 같은 건물을 쓰지만 철저한 방음벽과 도어락([가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)/[VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/)) 덕분에 완벽한 사생활이 보장되며, A동에 불이 나면 즉시 B동의 똑같은 집으로 워프할 수 있는 첨단 시스템이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**인프라 환경 3대 모델 심층 비교**
퍼블릭 클라우드는 관리의 편리함을 주지만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주권과 보안, 장기 비용 측면에서는 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)나 [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) 대비 트레이드오프가 존재한다.

| 비교 항목 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) ([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) | [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) (Private) | 퍼블릭 클라우드 (Public) | 실무 판단 기준 |
|:---|:---|:---|:---|:---|
| **비용 구조** | 높은 CAPEX (자산) | 높은 CAPEX + 관리 비용 | 100% OPEX (종량제 운영비) | 재무 부서의 예산 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| **보안/통제력** | 최고 (물리적 완전 통제) | 매우 높음 (사내망 통제) | 중간 ([하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 신뢰 의존) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 법적 규제 준수 여부 |
| **확장성/민첩성**| 수 개월 (하드웨어 반입) | 수 일 (내부 자원 한계) | 무한대, 수 분 내 즉각 확장 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 글로벌 진출 및 트래픽 폭 |
| **관리 책임** | HW부터 App까지 100% | [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 인프라부터 App까지 | OS부터 App까지만 책임 | 내부 IT 운영 인력의 규모 |

이 매트릭스에서 도출해야 할 핵심은 퍼블릭 클라우드가 모든 면에서 우월한 정답은 아니라는 것이다. 국방, 금융 등 민감한 개인정보를 물리적으로 분리해야 하는 법적 규제가 있는 경우나, 페타바이트급 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 24시간 365일 분석해야 하는 초거대 고정 워크로드의 경우, 퍼블릭 클라우드의 트래픽 아웃바운드 비용([Egress](/knowledge-base/studynote/16_bigdata/09_platform/189_egress/) Fee)이 자가 구축 비용을 아득히 초과하는 현상이 발생한다.

이 도식은 퍼블릭 클라우드 도입 시 보안 사고의 원인을 규명하는 절대적 기준인 <strong>책임 공유 모델 (Shared Responsibility Model)</strong>을 보여준다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">고객 (Customer) 의 책임 영역 - Security "IN" Cloud</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 고객 데이터 및 파일 암호화 정책</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 애플리케이션 취약점 패치 및 IAM (계정/권한 접근 제어)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 방화벽(Security Group) 규칙 및 OS 패치 관리</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CSP (클라우드 벤더) 의 책임 영역 - Security "OF" Cloud</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 하이퍼바이저 / 가상화 엔진 보안 및 격리 패치</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 데이터센터 물리적 출입 통제 / 전원 / 랙 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 글로벌 네트워크 인프라 케이블링 및 기초 시설</div></div>
</div>
</div>


이 구조의 핵심은 "클라우드가 기본적으로 안전하다"는 믿음이 반은 맞고 반은 틀리다는 것이다. 벤더([CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/))는 물리적 서버 도난이나 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 엔진 해킹은 막아주지만, 고객이 실수로 S3 스토리지의 접근 권한을 '전체 공개(Public)'로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 유출된 사고는 100% 고객의 책임이다. 실무에서는 클라우드 보안 사고의 99%가 하단([CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/))이 아닌 상단(고객의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류)에서 발생함을 명심해야 한다.

**📢 섹션 요약 비유**: 퍼블릭 클라우드는 첨단 보안을 자랑하는 은행 대여금고와 같다. 은행([CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/))은 튼튼한 금고와 경비원을 제공하지만, 당신(고객)이 금고 열쇠를 길거리에 떨어뜨리거나 문을 열어두고 간 것까지 책임져주지는 않는다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

<strong>퍼블릭 클라우드 운영 시나리오 및 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
퍼블릭 클라우드의 "버튼 클릭 한 번으로 무한 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)"되는 성질은 통제되지 않으면 기업에 거대한 재앙을 초래한다.

<strong>시나리오: 섀도우 IT와 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/">FinOps</a>(비용 최적화) 부재에 따른 요금 폭탄</strong>
개발팀이 테스트용으로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한 최고 사양의 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 인스턴스나 고성능 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 주말 내내 끄지 않고 방치하거나, 필요 이상의 과도한 리소스를 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)(Over-provisioning)한 채로 잊어버리는 상황이 빈번하게 발생한다.
* **해결 판단**: 클라우드 비용을 투명하게 관리하는 [FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/) 체계를 구축해야 한다. 모든 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 리소스에 부서별 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 태그(Tagging)를 강제하고, 일과 시간이 끝나면 개발/테스트 환경의 인스턴스를 자동으로 종료(Stop)하는 [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)([Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)) 스케줄러를 배치해야 한다. 또한 상시 구동이 확정된 코어 시스템은 1~3년 약정(Reserved Instance)을 걸어 50% 이상 비용 할인을 확보하는 전략이 필수다.

<strong>도입 실패 (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a>) 방지 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
1. <strong>리프트 앤 시프트(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/">Lift</a> and Shift)의 한계</strong>: 기존 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)의 거대한 모놀리식 구조([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))를 아키텍처 변경 없이 클라우드 IaaS로 통째로 복사해서 올리면, 클라우드의 장점인 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)은 누리지 못하고 비싼 월세만 내는 꼴이 된다. 반드시 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)나 관리형 DB를 활용하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 리팩토링이 수반되어야 한다.
2. **단일 가용 영역(Single AZ) 배포**: 개발 편의성을 이유로 로드밸런서 없이 웹과 DB를 단일 AZ에 몰아넣는 것은 시한폭탄과 같다. AZ 장애 시 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할 방법이 전무하므로 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 배포는 선택이 아닌 강제 사항이다.

**📢 섹션 요약 비유**: 무제한으로 쓸 수 있는 법인카드를 전 직원에게 쥐여준 것과 같다. 카드(자원)를 자유롭게 쓰되 반드시 영수증(태그)을 붙이고, 중앙 모니터링 부서([FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/))가 이상 지출을 실시간으로 감시해 낭비를 막아야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**도입 기대 효과 (정량 / 정성)**

| 구분 | 도입 전 ([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) | 도입 후 (Public Cloud) | 비즈니스 파급 효과 |
|:---|:---|:---|:---|
| **시장 진입 속도 (Time-to-Market)**| 3~6개월 소요 | 1~2일 내 즉시 인프라 구축 | 혁신적 아이디어의 신속한 테스트 및 런칭 |
| **글로벌 인프라 확장** | 국가별 전산실 계약 필요 | 클릭 한 번으로 해외 리전 배포 | 규제 극복 및 초저지연 글로벌 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 실현 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a> (<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/">DR</a>) 구성</strong>| 비용으로 인해 구축 포기 빈번 | 클라우드 내 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)로 저렴히 확보 | [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)([복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 시간) 수 분 이내로 단축 |

**미래 전망과 아키텍처 진화**
퍼블릭 클라우드는 단순한 인프라([IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)) 대여를 넘어선 지 오래다. 수많은 오픈소스를 직접 설치/운영할 필요 없이 CSP가 대신 백업과 패치를 해주는 관리형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)([PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)), 그리고 이제는 거대한 파라미터의 초거대 언어 모델([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) API를 즉각 호출해 쓸 수 있는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)-as-a-Service의 핵심 플랫폼으로 진화했다. 향후에는 중앙 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 한계를 넘어 지연시간을 0으로 수렴시키기 위해 통신사 기지국이나 공장 내부까지 퍼블릭 클라우드의 컴퓨팅 파워가 확장되는 엣지 클라우드(Edge Cloud)와 [분산 클라우드](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/242_distributed_cloud_edge_computing_aws_outposts/) 모델이 표준으로 자리 잡을 것이다.

**📢 섹션 요약 비유**: 과거의 퍼블릭 클라우드가 단순한 '공용 창고 대여업'이었다면, 지금의 퍼블릭 클라우드는 공장, 분석 로봇, [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 비서까지 모두 갖춘 '글로벌 무한 생산 기지'로 진화했다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* 가상 [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) ([VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/)) | 퍼블릭 클라우드 내에서 다른 기업의 트래픽을 차단하고 논리적으로 격리하는 필수 네트워크 방어망
* 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) ([Auto Scaling](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/)) | CPU 사용량 임계치에 따라 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 대수를 자동으로 수평 확장([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 및 축소하는 엔진
* 책임 공유 모델 (Shared Responsibility Model) | 클라우드 해킹 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 사고 발생 시 CSP와 고객 간의 책임 경계를 명확히 긋는 규약
* [스팟 인스턴스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/209_spot_instance_cloud_cost_optimization/) ([Spot Instance](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/209_spot_instance_cloud_cost_optimization/)) | CSP의 남는 유휴 자원을 경매 방식으로 최대 90% 저렴하게 쓰는 대신 언제든 뺏길 수 있는 비용 절감형 컴퓨팅 모델
* [FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/) (클라우드 재무 관리) | 재무 부서와 엔지니어링 부서가 협력하여 낭비되는 클라우드 지출을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고 아키텍처를 최적화하는 문화

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">온프레미스 (On-Premises)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">IaaS 인프라 서비스 (Infrastructure as a Service)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">퍼블릭 클라우드 (Public Cloud)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">PaaS 플랫폼 서비스 (Platform as a Service)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SaaS 소프트웨어 서비스 (Software as a Service)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">멀티 클라우드 (Multi-Cloud)</div></div>
</div>
</div>



물리 인프라에서 IaaS를 거쳐 퍼블릭 클라우드의 다양한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층과 [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) 전략으로 진화하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 장난감을 갖고 놀고 싶을 때마다 비싼 돈을 주고 직접 사면, 나중에는 방에 자리가 부족해지고 돈도 많이 들어요.
2. 퍼블릭 클라우드는 장난감 백화점에서 스마트폰 버튼만 누르면 필요한 장난감을 1초 만에 빌려주는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)예요.
3. 빌려 쓴 시간만큼만 적은 돈을 내고, 다 놀면 바로 돌려주니까 방도 깨끗하고 다양한 장난감을 매일 바꿔가며 놀 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 6 / 371

← **이전**: [6. FaaS (Function as a Service / Serverless) - 인프라 관리 없이 함수 코드 조각 단위로 배포/실행](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/006_faas_serverless/)
**다음**: [8. 프라이빗 클라우드 (Private Cloud) - 단일 기업 전용으로 자체 데이터센터(On-Premise) 내부에 구축된 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) →

---
