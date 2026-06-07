---
title: "AWS Elastic Beanstalk, Heroku"
date: "2024-05-24"
tags:
  - "cloud_architecture"
  - "studynote-cloud-architecture"
weight: 3
---
# [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) (Platform [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: PaaS는 인프라([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) 위에서 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 미들웨어, 런타임, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 엔진까지 클라우드 벤더가 통합 관리하여, 개발자는 오직 '애플리케이션 코드'와 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'에만 집중할 수 있게 하는 플랫폼 임대 모델이다.
> 2. **가치**: OS 패치, 로드밸런싱 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), DB [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 등 지루한 인프라 운영 오버헤드([Toil](/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))를 완전히 제거함으로써 개발 주기를 극단적으로 단축하고 Time-to-Market을 달성한다.
> 3. **융합**: 현대의 PaaS는 단순한 런타임 제공을 넘어 [컨테이너 오케스트레이션](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)(Managed [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 및 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)/[FaaS](/studynote/12_it_management/05_security_compliance/342_faas/)) 아키텍처와 융합되어 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 생태계의 핵심 코어가 되고 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

[PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) (Platform [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)(인프라)와 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)(완제품 소프트웨어)의 중간에 위치하며, 애플리케이션의 개발, 실행, 관리에 필요한 완벽한 환경(플랫폼)을 제공한다. 대표적인 예로 AWS Elastic Beanstalk, Heroku, Google App 엔진, 그리고 완전 관리형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)인 AWS RDS 등이 있다.

[IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 환경에서는 가상 서버([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))를 불과 몇 분 만에 띄울 수 있지만, 그 위에 웹 서버(Nginx)를 설치하고, 자바(Java) 런타임을 맞추고, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 연동하고, 보안 패치를 챙기는 작업은 여전히 개발자(또는 운영자)의 몫이다. [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)([마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)) 시대가 도래하면서 개발팀은 수십 개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 독립적으로 배포해야 하는데, 매번 OS와 미들웨어를 세팅하는 것은 엄청난 시간 낭비이자 [인지 부하](/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/)([Cognitive Load](/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/))를 초래한다. PaaS는 이 지점을 타격하여, "코드를 가져오면 실행은 우리가 책임진다"는 철학으로 등장했다.

다음은 IaaS를 쓸 때와 PaaS를 쓸 때 개발자의 작업 포커스가 어떻게 달라지는지를 보여주는 문제 배경도이다.

```text
[IaaS 환경에서의 배포 병목 (개발자 인지 부하 발생)]
개발자 로직 완성 -> OS 버전/의존성 확인 -> Nginx/Tomcat 설치 -> 방화벽/LB 수동 연동 -> 배포 완료
                   ^ (인프라 및 미들웨어 설정에 시간 70% 소모)

[PaaS 환경에서의 배포 파이프라인 (골든 패스)]
개발자 로직(Git Push) --(PaaS 엔진 자동화)--> 컨테이너 빌드 & 무중단 라우팅 결합 -> 배포 완료
                   ^ (비즈니스 로직에 시간 100% 집중)
```

이 흐름의 핵심은 소프트웨어 개발 생명주기에서 '환경 구성(Configuration)' 단계를 클라우드 벤더의 표준화된 자동화 파이프라인으로 위임한다는 것이다. 실무에서는 개발자가 Git 저장소에 코드를 밀어 넣기만 하면 PaaS가 언어(Node.js, Python 등)를 자동 감지하여 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 감싸고, 오토스케일링 및 로드밸런서를 붙여 즉시 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 가능한 상태로 만든다. 따라서 개발팀은 인프라 장애나 패치 걱정 없이 하루에도 수십 번의 [지속적 배포](/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)(CD)를 안전하게 수행할 수 있다.

📢 **섹션 요약 비유**: IaaS가 텅 빈 부엌을 빌려주고 내가 냄비와 화구를 직접 설치해 요리해야 한다면, PaaS는 조리기구와 기본 불 조절 세팅이 완벽히 끝난 셰프용 최고급 주방을 제공해, 오직 '나만의 요리 레시피(코드)'에만 집중하게 해주는 것과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 플랫폼의 내부는 사용자 코드를 받아 실행 가능한 아티팩트로 변환하고 트래픽을 라우팅하는 복잡한 제어 엔진으로 구성된다.

| 구성 요소 | 역할 | 내부 동작 방식 | 실무 예시 | 비유 |
|:---|:---|:---|:---|:---|
| <strong>코드 <a href="/studynote/04_software_engineering/04_testing_quality/256_builder_pattern_step_by_step_creation/">빌더</a> (Build 엔진)</strong> | 소스코드를 런타임 이미지로 컴파일 | 빌드팩(Buildpack)이 언어를 감지하여 의존성 설치 및 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)화 | Heroku Buildpacks | 식재료를 조리 가능하게 다듬는 기계 |
| **미들웨어 & 런타임** | 애플리케이션 실행 환경 제공 | Java, Node, Python 인터프리터 및 WAS(Tomcat 등) 백그라운드 구동 | AWS Elastic Beanstalk | 요리를 익히는 가스레인지 |
| **트래픽 라우터 & LB** | 외부 요청을 내부 인스턴스로 분배 | L7 게이트웨이가 동적으로 변하는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) IP를 추적하여 트래픽 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | [Ingress](/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/), [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) | 서빙 직원의 주문 분배 |
| **상태 관리 및 모니터링** | 인스턴스 헬스체크 및 [로그 수집](/studynote/09_security/13_secops_ir_forensics/626_log_collection/) | 비정상 인스턴스 강제 종료 및 재생성, [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 중앙 적재 | Datadog, CloudWatch 연동 | 식당의 주방 감독관 |
| <strong>관리형 <a href="/studynote/15_devops_sre/01_culture_methodology/010_backend_services/">백엔드 서비스</a></strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 및 캐시 연동 | 클릭 한 번으로 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)된 RDBMS, [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 메모리 풀을 앱 환경 변수에 주입 | AWS RDS, ElastiCache | 대형 식재료 냉장고 |

다음 구조도는 개발자의 소스코드가 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 플랫폼을 거쳐 실제 클라우드 클러스터에 배포되는 내부 아키텍처 흐름을 보여준다.

```text
이 도식은 전형적인 PaaS(App Platform) 배포 파이프라인으로, 코드가 어떻게 이미지로 변환되어 라우팅되는지 핵심 계층 구조를 나타낸다.

+-------------- [Developer Workspace / 개발자 공간] --------------+
|  Git Push (Source Code: Java, Python, Node.js)      |
+-----------------------|-----------------------------+
                        v (Webhook Trigger)
+-------------- [PaaS Control Engine / PaaS 엔진] --------------+
| 1. [Buildpack / 빌드팩] : 코드 분석 및 라이브러리 다운로드 |
| 2. [Container Registry / 컨테이너 레지스트리] : 실행 불변 이미지 저장   |
| 3. [Scheduler / 스케줄러] : 여유 노드 탐색 및 인스턴스 배치  |
+-----------------------|-----------------------------+
                        v (Deploy)
+-------------- [PaaS Runtime Cluster / 런타임 클러스터] -------------+
| [External Load Balancer / 외부 로드밸런서] --------+                |
|    |                               |                |
|  [ App Instance (V1) ]    [ App Instance (V2) ]     |
|    +- Runtime / OS          +- Runtime / OS         |
|    +- IaaS VM (Hidden)      +- IaaS VM (Hidden)     |
|                                                     |
| +---------------- [Managed DB / 관리형 DB] -----------------+ |
| |  Master RDS  <====(Sync)====> Standby RDS     | |
| +-------------------------------------------------+ |
+-----------------------------------------------------+
```

이 구조도의 핵심은 가장 하단의 물리 서버([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) 영역이 개발자의 시야에서 완벽히 숨겨져(Hidden) 있다는 점이다. 개발자는 OS에 [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 접속을 할 필요가 없으며, [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 컨트롤 엔진이 무중단 [롤링 배포](/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/)([Rolling Update](/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/))나 블루-그린(Blue-Green) 배포까지 제어한다. 또한 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)(Managed DB) 역시 PaaS의 범주로 보며, 클러스터 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 및 자동 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)([Snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/))이 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 레벨에서 통제된다. 따라서 인프라 전담 인력이 부족한 스타트업이나, 비즈니스 로직 혁신이 최우선인 [애자일](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 조직에서 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 기준 최고의 효율을 낼 수 있다.

📢 **섹션 요약 비유**: 이 배포 시스템은 마치 자동차 조립 공장의 컨베이어 벨트와 같습니다. 철판(코드)을 올려놓기만 하면, 플랫폼 기계가 알아서 페인트를 칠하고(빌드), 엔진을 달고(런타임 결합), 출고 테스트(헬스체크)까지 마친 뒤 판매 라인(로드밸런서)에 올려놓습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

PaaS는 높은 생산성을 주지만, [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 대비 유연성이 떨어지는 트레이드오프(Trade-off)가 발생한다.

| 비교 항목 | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) (인프라 제어 중심) | [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) (생산성 중심) | 판단 포인트 |
|:---|:---|:---|:---|
| **제어 수준** | OS 루트(Root) 권한, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패치 가능 | 애플리케이션 코드, 환경변수 수준 제어 | 커스텀 바이너리 설치 필요성 |
| **운영 복잡도** | 매우 높음 (로드밸런싱, DB [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 직접 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)) | 낮음 (대부분 클라우드 벤더가 자동 관리) | 인프라 운영(Ops) 인력 보유 여부 |
| <strong>벤더 <a href="/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a></strong> | 상대적으로 낮음 | <strong>매우 높음 (벤더 전용 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 및 DB 구조에 결합)</strong> | 탈출 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(Exit [Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) 유무 |
| <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> 주체</strong> | 오토스케일링 그룹 등 조건 직접 세팅 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)된 임계치에 따라 PaaS가 내부적으로 자동 확장 | 트래픽 패턴의 예측 가능성 |

다음은 개발의 제어권(자유도)과 운영 효율성의 관계를 나타낸 의사결정 비교 매트릭스이다.

```text
이 매트릭스는 클라우드 스택이 상위로 갈수록 운영 오버헤드는 줄지만, 특정 벤더 아키텍처에 갇히게 되는 '종속성의 함정'을 시각화한다.

생산성/자동화 수준
  ^
  |                          [ SaaS ] (Office 365) - 완제품
  |                           /
  |            [ PaaS / FaaS ] (Heroku, Lambda) - 로직만 작성
  |             /
  |  [ IaaS ] (EC2, VPC) - 모든 환경 제어 가능
  |   /
  | /
  +-------------------------------------► 자유도 / 커스텀 제어권
           (Lock-in 리스크 상승)
```

이 비교에서 주의할 점은 PaaS의 벤더 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)([Lock-in](/studynote/12_it_management/05_security_compliance/362_lock_in_portability/))이다. 특정 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 환경(예: 특정 벤더의 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB나 특화된 빌드팩)에 과도하게 의존하게 되면, 추후 비용 문제로 다른 클라우드나 온프레미스로 이전해야 할 때 코드를 전면 재작성([Refactoring](/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/))해야 하는 기술 부채가 발생한다. 반면, 최근에는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))를 기반으로 하는 CaaS([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 IaaS의 이식성과 PaaS의 자동화 이점을 결합하며 PaaS의 표준 런타임으로 자리 잡고 있다.

📢 **섹션 요약 비유**: 맞춤 양복([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/))은 내 몸과 취향에 완벽히 맞출 수 있지만 재단에 시간이 오래 걸리고 수선도 직접 해야 합니다. 반면 기성복([PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/))은 당장 입고 나갈 수 있어 편리하지만, 체형이 독특하거나 디자인을 크게 바꾸고 싶을 때는 한계에 부딪히는 것과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 PaaS를 설계할 때는 애플리케이션의 상태 비저장([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) 요건과 플랫폼 제약을 명확히 인식해야 한다.

1. <strong>상태 비저장 (<a href="/studynote/15_devops_sre/05_devsecops/239_stateless_redis/">Stateless</a>) 설계 필수</strong>: [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 환경에서 인스턴스는 트래픽에 따라 수시로 파괴되고 재생성(Auto-scaling)된다. 만약 로컬 디스크나 메모리에 사용자 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 업로드된 이미지를 저장(Stateful)한다면, 인스턴스 교체 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 전부 증발한다. 따라서 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)은 관리형 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시에, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 S3 같은 오브젝트 스토리지에 저장하는 [12-Factor App](/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/) 원칙을 철저히 준수해야 한다.
2. <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/">콜드 스타트</a>(<a href="/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a>) 대처</strong>: 확장성을 극대화한 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 성격의 PaaS는 오랫동안 호출이 없으면 인스턴스를 0으로 내린다(Scale-to-Zero). 이후 첫 요청이 오면 런타임을 구동하느라 수 초의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(레이턴시)이 발생한다. 실시간성이 중요한 API라면 최소 1대의 인스턴스를 상시 유지(Provisioned)하는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 활성화해야 한다.
3. <strong><a href="/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 기반 <a href="/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/">PaaS</a> 도입 (탈출 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>)</strong>: 특정 [CSP](/studynote/09_security/05_web_app_security/475_csp/) 종속을 피하기 위해 대기업은 사내에 자체적인 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)([Internal Developer Platform](/studynote/13_cloud_architecture/04_devops_observability/200_internal_developer_platform_backstage/))를 구축한다. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 위에 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 플랫폼(예: Red Hat OpenShift, Cloud Foundry)을 얹어, 인프라가 AWS든 Azure든 상관없이 개발자에게는 동일한 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 배포 경험을 제공하는 [멀티 클라우드](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 구사한다.

```text
[실무 PaaS 장애 회피 및 상태 비저장(Stateless) 아키텍처 구조도]
이 흐름도는 PaaS 인스턴스가 파괴되더라도 시스템 일관성을 유지하기 위해 데이터 영속성을 외부로 빼낸 모범 설계다.

[Client Request / 클라이언트 요청]
        v
[PaaS Load Balancer / PaaS 로드밸런서] --(Round Robin)--+
        v                               v
+-[PaaS Instance A / 인스턴스 A]-+           +-[PaaS Instance B / 인스턴스 B]-+
| (Stateless Logic)   |           | (Stateless Logic)   |
+-+---------+---------+           +-+---------+---------+
  | Session | File                  | Session | File
  v         v                       v         v
[Redis]   [S3 Object / S3 객체]   [Redis]   [S3 Object / S3 객체]
(캐시)    (스토리지)              (캐시)    (스토리지)
```

이 구조의 핵심은 애플리케이션 로직을 담고 있는 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 인스턴스를 언제든지 버릴 수 있는 소모품(Cattle)으로 취급한다는 것이다. 실무에서는 이 지점을 간과하고 레거시 모놀리식 코드(로컬 디스크에 임시 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 쓰는 구조)를 그대로 PaaS에 올리면 확장 시 심각한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 유실 장애를 겪게 된다. 따라서 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 마이그레이션 전에는 반드시 코드 레벨의 [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 검진이 선행되어야 한다.

📢 **섹션 요약 비유**: [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 앱은 일회용 텐트와 같습니다. 언제든 비바람에 날아가고 새 텐트가 처질 수 있으므로, 귀중품(사용자 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 절대 텐트 안에 두지 말고 안전한 중앙 금고(외부 스토리지 및 캐시)에 보관해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 중심의 개발 체계는 조직에 진정한 '[데브옵스](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))' 문화를 안착시킨다. 인프라 운영(Ops)의 상당 부분을 클라우드 벤더가 흡수(NoOps 지향)하므로, 기업은 핵심 비즈니스 가치를 창출하는 개발(Dev) 인력의 밀도를 높일 수 있다.

| 기대 효과 | 도입 전 ([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)/[On-Premise](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) | 도입 후 ([PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 기반) | 정량/정성적 지표 변화 |
|:---|:---|:---|:---|
| 개발자의 인프라 작업 비중 | 전체 업무의 30~40% | 5% 미만 | 비즈니스 로직 구현 시간 대폭 증가 |
| 배포 파이프라인 ([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD) | [Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) 등 복잡한 스크립트 수동 구성 | [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 통합 빌드/배포 기능 활용 | 일일 배포 횟수(배포 빈도) 극대화 |
| 보안 패치 및 컴플라이언스 | 관리자가 주기적 점검 및 OS 패치 작업 | 벤더가 OS/미들웨어 취약점 자동 패치 | [Zero-Day](/studynote/02_operating_system/10_security/597_zero_day_exploit/) 취약점 노출 시간 최소화 |

미래의 PaaS는 애플리케이션을 넘어서 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 훈련 및 추론 환경을 제공하는 ML-[PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/)([머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 플랫폼, 예: AWS SageMaker)와, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파이프라인을 완전 관리해주는 Data-[PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) (예: [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/), [Databricks](/studynote/16_bigdata/03_spark/074_photon_engine/))로 분화 및 고도화되고 있다. 또한, [인지 부하](/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/)를 줄이기 위해 사내 개발자 포털([IDP](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/): [Internal Developer Platform](/studynote/13_cloud_architecture/04_devops_observability/200_internal_developer_platform_backstage/))을 구축하는 [플랫폼 엔지니어링](/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)([Platform 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)) 트렌드의 가장 강력한 엔진 기반이 될 것이다.

📢 **섹션 요약 비유**: PaaS는 무대 세트, 조명, 오케스트라가 모두 완벽하게 갖춰진 브로드웨이 극장입니다. 개발자는 연출가로서 훌륭한 대본(코드)과 배우([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 준비하면 언제든 최고의 공연([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))을 무대에 올릴 수 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- [12-Factor App](/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/) | [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 등 현대적 클라우드 환경에서 확장 가능하고 안정적인 앱을 만들기 위한 12가지 아키텍처 원칙
- [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) / [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/)) | PaaS의 궁극적 진화 형태로, 백그라운드 인스턴스조차 보이지 않고 함수 단위로 밀리초 과금되는 모델
- [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) | 작고 독립적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 환경에 각각 배포하여 결합도를 낮추는 설계 패턴
- [플랫폼 엔지니어링](/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/) ([Platform 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)) | 개발자의 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) [인지 부하](/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/)를 줄이기 위해 사내 표준 자동화 템플릿(골든 패스)을 제공하는 실무 조직 체계
- [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/)) & [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) | PaaS가 내부적으로 애플리케이션을 격리하고 런타임을 구동하는 핵심 기술 표준

### 📈 관련 키워드 및 발전 흐름도

```text
[12-Factor App]
    |
    v
[서버리스 (Serverless / FaaS)]
    |
    v
[마이크로서비스 아키텍처 (MSA)]
    |
    v
[플랫폼 엔지니어링 (Platform Engineering)]
    |
    v
[컨테이너 (Container) & 쿠버네티스]
```

이 흐름도는 12-Factor App에서 출발해 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/)) & [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 게임을 만들었는데, 이 게임을 전 세계 친구들이 다운받게 하려면 아주 복잡한 컴퓨터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 필요해요.
2. PaaS는 "네가 만든 게임 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)만 넘겨주면, 우리가 알아서 전 세계 컴퓨터에 깔고 접속할 수 있게 세팅해 줄게!" 하는 착한 로봇 조수예요.
3. 그래서 우리는 로봇이 일하는 동안 게임을 더 재미있게 업데이트하는 데에만 집중할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 2 / 371

<- **이전**: [2. IaaS (Infrastructure as a Service) - 서버(VM), 스토리지, 네트워크 인프라 제공 (AWS EC2,](/studynote/13_cloud_architecture/01_virtualization/002_iaas/)
**다음**: [4. SaaS (Software as a Service) - 브라우저 기반 완제품 소프트웨어 제공 (Google Workspace, Salesforce)](/studynote/13_cloud_architecture/01_virtualization/004_saas/) ->

---
