---
title: "Configuration Identification"
date: "2026-03-04"
tags:
  - "software_engineering"
  - "studynote-software-engineering"
weight: 21
---
# 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) (Configuration [Identification](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)은 소프트웨어 시스템을 관리 가능한 최소 단위인 형상 항목([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/), [Configuration Item](/studynote/12_it_management/02_itsm_itil/874_configuration_item/))으로 분해하고, 각각에 고유한 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)자와 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 체계를 부여하는 과정이다.
> 2. **가치**: 변경 통제의 대상 범위를 명확히 함으로써, 시스템의 복잡성을 낮추고 추적성([Traceability](/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/))을 확보하여 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) 전체 프로세스의 기반을 다진다.
> 3. **융합**: 단순한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 관리가 아닌 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경의 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)), [인프라스트럭처 애즈 코드](/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/)([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)), [소프트웨어 자재 명세서](/studynote/04_software_engineering/10_trends_pm_quality/690_sbom_software_supply_chain_security/)([SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))의 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 체계로 직접 이어진다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) (Configuration [Identification](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/))은 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) 프로세스의 가장 첫 번째 단계로, 전체 시스템 내에서 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)의 대상이 될 항목들을 찾아내고 이들에 대한 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 번호와 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 부여 규칙을 정의하는 활동이다. 이는 단순한 이름표 붙이기를 넘어, 소프트웨어를 구성하는 부품들의 생명주기를 어떻게 관리할 것인지에 대한 설계적 결단이다.

이 과정이 필수적인 이유는 대규모 시스템에서 발생하는 "변경의 연쇄 작용"을 통제하기 위해서다. 과거 단일(Monolithic) 시스템에서는 전체 소스코드를 하나의 덩어리로 관리하는 것이 가능했지만, 시스템이 커지고 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 간 의존성이 복잡해짐에 따라 특정 변경이 어느 모듈에 영향을 미치는지 추적하는 것이 불가능해졌다. 무엇을 관리할지(What to control) 정의하지 않으면, 변경 통제나 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 자체가 성립할 수 없다.

이러한 한계를 극복하기 위해, 전체 시스템을 기능적 혹은 물리적 단위로 분해하여 트리 구조의 형상 항목([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/))을 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고, 각 CI마다 명확한 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)([Baseline](/studynote/04_software_engineering/01_overview_principles/025_baseline/))과 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)자를 부여하는 혁신적인 관리 패러다임이 요구되었다. 현재의 비즈니스 환경에서는 코드뿐만 아니라 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 의존성, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지, 인프라 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)까지 모두 CI로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)해야만 무결성을 보장할 수 있다.

> **📢 섹션 요약 비유**: 마치 대형 마트에서 수만 개의 상품을 체계적으로 관리하기 위해 카테고리를 나누고 개별 상품마다 고유한 바코드(바코드 번호와 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))를 부여하는 것과 같습니다. 바코드가 없으면 재고 파악과 유통 기한 관리가 불가능한 것처럼, 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 없이는 소프트웨어 자산 관리가 불가능합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)의 아키텍처는 하향식 분해([Top-down](/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/) Decomposition) 메커니즘을 따른다. 전체 시스템을 점진적으로 분할하여, 더 이상 나눌 수 없거나 나눌 필요가 없는 관리의 최소 단위인 CI를 도출한다.

이 도식은 시스템이 어떻게 하위 CI로 분할되는지, 그리고 각 레벨에서 어떤 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)가 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)되는지를 보여준다. 최상위 시스템에서 시작해 기능 블록, 개별 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)로 이어지는 트리 구조를 이해하는 것이 핵심이다.

```text

+------------------------------------------------------------+
|                  System Level (Level 0 / 레벨 0)                    |
|                  [System-100-v1.0]                         |
+--------+------------------------------------------+--------+
         v                                          v
+---------------------+                    +---------------------+
| Subsystem (Level 1 / 레벨 1) |                    | Subsystem (Level 1 / 레벨 1) |
|  [CI-WEB-200-v1.1]  |                    |  [CI-DB-300-v1.0]   |
+----+-----------+----+                    +---------+-----------+
     v           v                                   v
+---------+ +---------+                         +---------+
| Module  | | Module  |                         | Config  |
| [M-201] | | [M-202] |                         | [C-301] |
+---------+ +---------+                         +---------+
```

이 흐름의 핵심은 분할의 깊이(Granularity)를 결정하는 것이다. [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 트리를 너무 깊게 구성하면 관리 오버헤드가 급증하고, 너무 얕게 구성하면 변경 시 영향도를 정확히 파악하기 어렵다. 따라서 각 계층에서 관리해야 하는 정보의 성격에 맞춰 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 기준을 수립해야 한다.

#### 구성 요소 및 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)

| 요소명 | 역할 | 내부 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 체계 예시 | 비유 |
|:---|:---|:---|:---|:---|
| **System** | 전체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 최상위 집합 | 전체 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 배포 [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/) | `SYS-APP-v1.0` | 자동차 완성품 |
| **Subsystem** | 독립적으로 기능하는 주요 서브 단위 | 하위 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 리스트, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 명세 | `SUB-AUTH-v2.1` | 자동차 엔진 |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a> (<a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>)</strong> | [형상 통제](/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)의 최소 단위 (코드/문서) | 작성자, 의존성, [체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) | `MOD-LOGIN-v2.1.4` | 엔진 실린더 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a></strong> | 각 CI에 부여되는 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 정보 | ID, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 상태, 생성일 | `{"id":"M1", "ver":"1.0"}` | 부품 시리얼 번호 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">Relationship</a></strong> | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 간의 연결 구조 (의존성) | 부모-자식, 의존(Depends-on) | `Tree Structure` | 조립 설계도 |

형상 항목의 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 번호는 보통 `[프로젝트 식별자]-[시스템 구분]-[문서/모듈 종류]-[일련번호]-[버전]`의 구조를 갖는다. 예를 들어 `PRJ-AUTH-SRC-001-v1.2`와 같이 부여되며, 이는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)([CMDB](/studynote/12_it_management/02_itsm_itil/875_cmdb/))나 Git의 태그/해시값과 매핑되어 중앙에서 관리된다.

최근의 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 체계는 소스 코드의 컴파일 단위뿐만 아니라, `Dockerfile`, `docker-compose.yml`, [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 매니페스트와 같은 인프라 구성 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)까지 모두 CI로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하여 코드 변경과 인프라 변경을 동일한 선상에서 추적할 수 있도록 진화하고 있다.

> **📢 섹션 요약 비유**: 복잡한 레고 블록 성을 조립할 때, 성벽, 지붕, 문으로 큰 덩어리를 나눈 후 각 조각마다 일련번호를 매겨 "이 문은 지붕 3번과 연결된다"고 명세서를 쓰는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)에서 가장 중요한 결정은 CI의 크기(Granularity), 즉 '얼마나 잘게 쪼갤 것인가'이다. 이는 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))에서의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분리 기준과 매우 유사하다.

다음 매트릭스는 거친 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)([Coarse-grained](/studynote/01_computer_architecture/11_multicore_synchronization/398_coarse_grained_multithreading/))과 세밀한 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)([Fine-grained](/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/)) 방식의 아키텍처적 트레이드오프를 보여준다. [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 입도는 시스템의 관리 비용과 직결된다.

```text
+----------+--------------------------+--------------------------+----------------+
| 비교 항목| 거친 식별 (Coarse)       | 세밀한 식별 (Fine)       | 판단 포인트    |
+----------+--------------------------+--------------------------+----------------+
| CI 단위  | 서브시스템 단위 통관리   | 개별 소스파일/클래스 단위| 변경의 빈도    |
| 관리 비용| 낮음 (항목 수 적음)      | 높음 (항목 수 많음)      | 팀의 규모/역량 |
| 추적성   | 약함 (내부 변경 파악 난해)| 강함 (정밀한 의존성 파악)| 결함 추적 난이도|
| 적합 환경| 단일(Monolith) 레거시    | MSA, 컴포넌트 기반(CBD)  | 시스템 아키텍처|
+----------+--------------------------+--------------------------+----------------+
```

거친 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 방식은 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 도입 비용이 적지만, 단일 패키지 내부에서 발생하는 세부적인 충돌을 방지하기 어렵다. 반면 세밀한 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 방식은 단건 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 관리 오버헤드가 다소 크지만, 의존성 격리와 수평 확장성이 뛰어나기 때문에 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경처럼 독립적 배포가 잦은 구조에서는 전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 기준으로 유리하다.

**과목 융합 관점:**
- <strong>네트워크/보안 (<a href="/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a> 융합)</strong>: 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)을 통해 도출된 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 목록은 보안 관점에서 [소프트웨어 자재 명세서](/studynote/04_software_engineering/10_trends_pm_quality/690_sbom_software_supply_chain_security/)([SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/))로 직결된다. [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(Log4j 등) 각각이 CI로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)되어야만 [제로 데이](/studynote/02_operating_system/10_security/597_zero_day_exploit/) 취약점 발생 시 즉각적인 영향도 파악이 가능하다.
- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (<a href="/studynote/12_it_management/02_itsm_itil/875_cmdb/">CMDB</a> 모델링)</strong>: 도출된 CI와 그들 간의 연관 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)([Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))는 [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/) 기반의 [구성 관리](/studynote/12_it_management/02_itsm_itil/873_configuration_management/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)([CMDB](/studynote/12_it_management/02_itsm_itil/875_cmdb/)) 스키마를 설계하는 기초 자료가 된다.

> **📢 섹션 요약 비유**: 우편물을 관리할 때, '아파트 동' 단위로만 묶어서 배달할지(거친 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)), 아니면 '각 세대별'로 바코드를 붙여 배달할지(세밀한 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)) 결정하는 것과 같습니다. 세대별 바코드가 있으면 정확성은 높지만 우체부의 관리 작업은 훨씬 많아집니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)을 잘못 수행하면 시스템 전체의 [형상 통제](/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)가 마비되는 치명적 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)에 직면한다.

이 의사결정 트리는 실무 프로젝트에서 특정 산출물을 CI로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할지 말지를 판단하는 기준을 제시한다.

```text
[산출물 발생]
   v
[변경 가능성이 있는가?] --(No)--> 식별 제외 (단순 보관)
   |
 (Yes)
   v
[다른 모듈과 의존성을 가지는가?] --(No)--> 단일 문서로 관리
   |
 (Yes)
   v
[독립적으로 테스트 및 배포가 가능한가?] --(No)--> 상위 CI에 병합 관리
   |
 (Yes)
   v
[독립 CI로 식별 및 베이스라인 부여]
```

이 흐름의 핵심은 변경 가능성과 독립 배포 가능성 단계가 판단의 중심에 위치한다는 점이다. 따라서 불필요한 산출물(예: 임시 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 컴파일 중간 생성물)은 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) 항목에서 즉시 배제되며, 시스템 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하(형상 DB 오버헤드)를 방지할 수 있다. 실무에서는 이 지점의 독립성을 지속적으로 점검해야 한다.

#### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 및 치명적 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 사례
1. **모든 산출물의 CI화**: 개발 중 생성되는 모든 중간 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(.class, .o 등)까지 CI로 지정하는 경우. 관리비용 폭증으로 [형상 통제](/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)가 불가능해진다. **실무 판단**: 컴파일된 바이너리는 배포 [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/) 단위에서만 CI로 묶고 소스코드는 개별 CI로 관리해야 한다.
2. <strong>동적 구성 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 누락</strong>: [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)의 [Config](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 환경 변수를 CI에서 누락하는 경우. 코드 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)은 맞는데 환경 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 달라 배포에 실패하는 원인이 된다. **실무 판단**: `application.yml` 등의 인프라 구성 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)도 코드와 동일한 수준의 CI로 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)해야 한다.

> **📢 섹션 요약 비유**: 짐을 쌀 때, 언제든 버려도 되는 휴지조각까지 인벤토리 목록에 적어 넣으면 정작 중요한 여권과 지갑을 관리하기 힘들어지는 것과 같습니다. 중요한 물건만 인벤토리([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/))로 등록해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 체계적으로 구축되었을 때 얻는 정량적/정성적 효과는 다음과 같다.

| 구분 | 도입 전 | 도입 후 (기대효과) |
|:---|:---|:---|
| **의존성 파악 시간** | 담당자 인터뷰에 의존 (수 시간~수 일) | [CMDB](/studynote/12_it_management/02_itsm_itil/875_cmdb/) 트리 조회 (수 분 이내) |
| <strong>장애 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 시간 (<a href="/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a>)</strong> | 원인 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 파악 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 대상 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 명확화로 단축 |
| **보안 취약점 대응** | 전수 수동 검사 | 특정 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 즉시 격리 |

**미래 전망**: [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/))와 결합하여 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 대상이 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 코드에서 물리적 인프라 스펙으로 확장되고 있다. 또한, 해시(Hash) 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 체계(Git 등)가 주류가 되면서, 중앙 집중적 번호 부여보다 커밋 해시(Commit Hash) 자체가 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)자로 활용되는 선언적 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 방식이 표준으로 자리 잡을 것이다. 관련하여 IEEE 828 ([Configuration Management](/studynote/12_it_management/02_itsm_itil/873_configuration_management/)) 및 ISO/IEC 12207 등에서 시스템의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)/물리적 항목 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)을 중요 프로세스로 권고하고 있다.

> **📢 섹션 요약 비유**: 제대로 된 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)은 얽히고설킨 털실 뭉치를 색깔별로 분류해 깔끔하게 실패에 감아두는 것과 같아, 필요할 때 즉시 원하는 색의 실을 당겨 쓸 수 있게 해줍니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

- <strong><a href="/studynote/04_software_engineering/01_overview_principles/022_configuration_control/">형상 통제</a> (<a href="/studynote/04_software_engineering/01_overview_principles/022_configuration_control/">Configuration Control</a>)</strong> | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 CI에 대한 변경 요청을 평가하고 승인하는 제어 위원회 프로세스
- <strong><a href="/studynote/04_software_engineering/01_overview_principles/025_baseline/">기준선</a> (<a href="/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a>)</strong> | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 각 CI들의 특정 시점 조합을 공식적으로 승인한 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 묶음
- <strong>형상 기록/보고 (<a href="/studynote/04_software_engineering/01_overview_principles/024_configuration_status_accounting/">Configuration Status Accounting</a>)</strong> | [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 CI의 모든 변경 이력을 기록하고 상태를 대시보드화하는 가시성 확보 활동
- <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/690_sbom_software_supply_chain_security/">소프트웨어 자재 명세서</a> (<a href="/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a>)</strong> | 소프트웨어 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 보안을 위해 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)와 모듈의 의존성 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 명세
- <strong><a href="/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/">마이크로서비스 아키텍처</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)</strong> | 시스템을 세분화된 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 묶음인 독립적 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 분리하여 배포하는 아키텍처 패턴

### 📈 관련 키워드 및 발전 흐름도

```text
[CI (형상 항목 — Configuration Item) 식별 및 명명]
    |
    v
[기준선 (Baseline) 설정 — 특정 시점 승인 버전 묶음]
    |
    v
[형상 통제 (Configuration Control) — CCB 변경 승인]
    |
    v
[형상 기록/보고 (Configuration Status Accounting)]
    |
    v
[형상 감사 (Configuration Audit) — 기능/물리 감사]
```
SCM의 4대 활동은 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)->[기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/)->통제->기록->[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 흐름으로 이어지며, [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 첫 단추로 모든 변경 추적성과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능성의 기반이 된다.

### 👶 어린이를 위한 3줄 비유 설명
1. 장난감 로봇을 만들 때, 그냥 섞어두지 않고 머리, 팔, 다리로 나누는 것을 형상 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이라고 해요.
2. 각각의 부품에 "로봇팔-1호"라고 이름표를 붙여야 잃어버렸을 때 쉽게 찾고 조립할 수 있어요.
3. 이렇게 이름표를 잘 붙여두면, 나중에 팔을 "로봇팔-2호"로 업그레이드할 때 다른 부품은 놔두고 팔만 딱 바꿀 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 21 / 973

<- **이전**: [20. 형상 관리 (SCM, Software Configuration Management)](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)
**다음**: [22. 형상 통제 (Configuration Control) - 변경 제어 위원회(CCB)](/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) ->

---
