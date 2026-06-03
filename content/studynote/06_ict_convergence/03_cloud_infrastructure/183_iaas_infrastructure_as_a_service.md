+++
title = "183. IaaS (Infrastructure as a Service) - 서버, 스토리지, 네트워크 가상화 제공"
date = 2026-05-06

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IaaS (Infrastructure [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공자 (Cloud [Service Provider](/knowledge-base/studynote/09_security/11_iam_access_control/535_sp_service_provider/), [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/))가 보유한 물리 서버·스토리지·네트워크를 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)해, 사용자가 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), OS) 수준 통제권을 가진 인프라를 주문형으로 임대하는 모델이다.
> 2. **가치**: 하드웨어 구매와 설치에 걸리던 주·월 단위 리드타임을 분 단위 프로비저닝으로 바꾸고, 자동 확장·[재해 복구](/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)·전역 배치 같은 인프라 민첩성을 소프트웨어처럼 다루게 해 준다.
> 3. **판단 포인트**: OS, 네트워크, 보안 장비 수준의 제어가 필요하고 이를 자동화·패치·[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)까지 직접 운영할 역량이 있을 때 강력하며, 그렇지 않으면 [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) (Platform [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))나 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) (Software [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 더 적합할 수 있다.

---

## Ⅰ. 개요 및 필요성

IaaS는 CSP가 운영하는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 자원을 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)해, 사용자가 가상 서버와 스토리지, 네트워크를 응용 프로그램 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))로 요청하고 즉시 쓰게 하는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델이다. 핵심은 "서버를 산다"에서 "인프라를 호출한다"로 바뀐 점이다. 물리 장비는 CSP가 소유하지만, 사용자는 자신의 서버처럼 자원을 할당받아 운영할 수 있다.

이 모델이 필요해진 이유는 전통적인 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 인프라가 너무 느리고 경직되어 있었기 때문이다. 트래픽 피크를 대비하려면 최대 부하 기준으로 장비를 먼저 사야 했고, 도입 절차와 설치 작업 때문에 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 시작 전부터 큰 시간과 비용이 묶였다. 반대로 실제 사용량이 낮은 시간에는 비싼 장비가 놀게 된다. IaaS는 이런 비효율을 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 자원 풀링으로 줄여, 필요한 순간에만 계산 자원과 저장공간을 배정받도록 만들었다.

기술적으로는 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)) 기반 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 소프트웨어 정의 인프라가 배경이다. 거대한 물리 서버 한 대를 여러 가상 머신 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))으로 나누고, 네트워크와 스토리지도 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 자원처럼 조합하면서 하드웨어 배포 속도를 소프트웨어 배포 속도에 가깝게 끌어올린 것이다. 그래서 IaaS의 등장은 단순 임대가 아니라 **인프라의 프로그래밍 가능화**로 이해해야 한다.

아래 그림은 왜 IaaS가 기존 조달 방식을 바꾸었는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ From hardware procurement to API provisioning                     │
├────────────────────────────────────────────────────────────────────┤
│ On-prem : plan -> buy -> rack -> cable -> install -> operate      │
│ IaaS    : request VM -> attach volume -> open network -> start    │
│                                                                    │
│ Physical assets stay in the data center                           │
│ Logical resources are carved out on demand                        │
└────────────────────────────────────────────────────────────────────┘
```

이 변화의 본질은 속도만이 아니다. 인프라가 물리 장비 단위에서 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 자원 단위로 바뀌면서, 규모 확장과 장애 대응, 테스트 환경 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)까지 모두 코드와 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 다룰 수 있게 되었다.

- **📢 섹션 요약 비유**: IaaS는 공장을 직접 짓는 대신, 필요한 크기의 작업실과 창고, 전기 설비를 갖춘 산업단지를 그때그때 빌려 쓰는 것과 같다. 건물은 남의 것이지만, 안에서 어떤 기계를 놓고 어떻게 운영할지는 사용자가 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IaaS의 핵심 원리는 제어 평면과 실행 평면의 분리다. 사용자는 콘솔이나 API로 자원을 요청하고, 제어 평면은 이미지·권한·[할당량](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)·네트워크 규칙을 확인한 뒤, 실행 평면에서 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)·스토리지·가상 네트워크를 실제로 붙여 준다. 이 과정이 표준화되어 있기 때문에 사람이 장비를 설치하지 않아도 몇 분 안에 새 서버를 만들 수 있다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ IaaS control flow                                                 │
├────────────────────────────────────────────────────────────────────┤
│ User / IaC template                                               │
│        │ API call                                                 │
│        ▼                                                          │
│ Control plane                                                     │
│   ├─ image catalog                                                │
│   ├─ scheduler / quota                                            │
│   ├─ Virtual Private Cloud (VPC) policy                           │
│   └─ monitoring / auto scaling                                    │
│        │                                                          │
│        ├─▶ Hypervisor cluster ─▶ Virtual Machine (VM)             │
│        └─▶ Storage service   ─▶ block / object data               │
└────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 컴퓨트 (Compute) | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 또는 베어메탈 인스턴스로 CPU·메모리를 제공 | 인스턴스 유형, 가용영역, 자동 확장 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 설계해야 함 |
| 블록 스토리지 (Block Storage) | VM에 붙는 영구 디스크 제공 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 등급, [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 중요 |
| 객체 스토리지 ([Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)) | 대용량 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장 | 내구성은 높지만 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템처럼 직접 마운트하지는 않음 |
| 가상 네트워크 ([VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/)) | 서브넷, [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 보안 그룹으로 네트워크 격리 제공 | 주소 체계, 인터넷 노출 범위, 동서 트래픽 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 미리 잡아야 함 |
| 이미지와 템플릿 | 동일 환경을 반복 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 기준점 | 표준 골든 이미지와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리가 운영 품질을 좌우 |
| 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) ([Auto Scaling](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/)) | 부하에 따라 인스턴스를 자동 증감 | 상태 비저장 설계와 헬스 체크가 선행되어야 함 |

IaaS에서는 공동 책임 모델 (Shared Responsibility Model)이 매우 중요하다. CSP는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 시설, 전원, 물리 장비, [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)를 책임지지만, 사용자는 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 내부 OS 패치, 미들웨어 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 애플리케이션 배포, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 접근 통제를 책임진다. 즉 IaaS는 자유도가 높은 대신 운영 책임을 함께 넘겨받는 모델이다.

이 때문에 IaaS의 설계는 단순한 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 아니라 이미지 관리, 네트워크 경계, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 키 관리, 모니터링 체계를 묶어 보는 작업이 된다. 특히 수작업 콘솔 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 아니라 인프라를 코드로 정의하는 [인프라스트럭처 애즈 코드](/knowledge-base/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) 방식이 결합될 때 IaaS의 강점이 제대로 살아난다.

- **📢 섹션 요약 비유**: IaaS는 전기와 수도, 창고, 작업대가 모두 연결된 빈 공장을 빌리는 것과 같다. 건물 골조와 전력 공급은 임대인이 책임지지만, 안에 어떤 설비를 놓고 안전수칙을 어떻게 지킬지는 임차인의 몫이다.

---

## Ⅲ. 비교 및 연결

IaaS를 정확히 이해하려면 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)와 [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 사이에서 어떤 위치를 차지하는지 봐야 한다. [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)는 가장 높은 통제권을 주지만 도입 속도가 느리고 확장성이 제한되며, PaaS는 운영 부담을 크게 줄여 주지만 런타임과 플랫폼 제약을 받아들여야 한다. IaaS는 그 중간에서 **빠른 조달과 높은 제어권을 함께 주는 대신, 운영 부담은 상당 부분 남겨 두는 모델**이다.

| 비교 항목 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) | IaaS | [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) |
| :--- | :--- | :--- | :--- |
| 자원 확보 속도 | 느림 | 빠름 | 매우 빠름 |
| OS·네트워크 제어 | 매우 높음 | 높음 | 제한적 |
| 운영 부담 | 매우 큼 | 큼 | 중간 이하 |
| [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자 | 큼 | 상대적으로 작음 | 작음 |
| 대표 활용 | 고정 대규모 시스템, 특수 장비 | 레거시 이관, 커스텀 인프라, 관리형 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반 | 표준 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 빠른 배포 중심 앱 |

이 비교가 중요한 이유는 IaaS가 단지 하위 모델이 아니라, 상위 클라우드 모델의 기반이 되기 때문이다. 관리형 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/), 일부 플랫폼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [재해 복구](/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) (Disaster [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)) 환경은 내부적으로 IaaS 자원을 활용한다. 즉 IaaS는 끝단 제품이면서 동시에 다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델의 기반 인프라다.

또한 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), 관리형 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 같은 상위 추상화와의 관계도 생각해야 한다. 예를 들어 애플리케이션은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 배포하더라도, 그 [컨테이너 오케스트레이션](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 클러스터 자체는 IaaS 위에서 돌아가는 경우가 많다. 따라서 IaaS를 이해하면 클라우드 전체 스택의 책임 경계가 더 선명해진다.

- **📢 섹션 요약 비유**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)가 내 건물을 직접 소유하는 것이라면, IaaS는 설비 좋은 공장을 빌려 직접 운영하는 것이고, PaaS는 필요한 생산라인까지 갖춰진 공장을 이용하는 것에 가깝다. 편의가 올라갈수록 손이 덜 가지만, 공장을 내 마음대로 개조할 자유는 줄어든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 IaaS는 세 가지 상황에서 특히 힘을 발휘한다. 첫째, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 특수 보안 에이전트, 자체 네트워크 장비처럼 OS·네트워크 수준 제어가 필요한 경우다. 둘째, 계절성 이벤트나 캠페인처럼 부하 변동이 커서 자동 확장의 경제성이 큰 경우다. 셋째, 기존 레거시 시스템을 클라우드로 이관하되 애플리케이션 구조를 한 번에 완전히 바꾸기 어려운 경우다.

반대로 항상 일정한 부하를 가진 시스템을 24시간 과다한 사양으로 켜 두면 IaaS는 생각보다 비쌀 수 있다. 또한 수작업으로 VM을 늘리고 줄이는 운영은 금세 구성 드리프트를 만들고, CSP가 OS 보안까지 대신해 줄 것이라고 오해하면 보안 사고로 이어진다. 따라서 IaaS 도입 판단은 기술뿐 아니라 운영 자동화 성숙도와 비용 관리 역량을 함께 봐야 한다.

아래 의사결정 흐름은 IaaS가 적합한지 빠르게 가르는 기준을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ When IaaS is the right fit                                        │
├────────────────────────────────────────────────────────────────────┤
│ Need OS / kernel / network appliance level control?               │
│        ├─ Yes ─▶ IaaS first                                        │
│        └─ No                                                      │
│             │                                                     │
│             ▼                                                     │
│ Need only code deployment on managed runtime?                     │
│        ├─ Yes ─▶ PaaS / managed container                         │
│        └─ No                                                      │
│             │                                                     │
│             ▼                                                     │
│ Is the workload mostly a finished business application?           │
│        ├─ Yes ─▶ SaaS                                             │
│        └─ No  ─▶ reconsider hybrid or IaaS + automation           │
└────────────────────────────────────────────────────────────────────┘
```

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 애플리케이션이 OS, 네트워크, 스토리지 세부 제어를 실제로 필요로 하는가?
2. OS 패치, 취약점 대응, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 모니터링을 담당할 운영 체계가 준비되어 있는가?
3. [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/), 표준 이미지, 자동 확장 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 수작업 구성을 줄일 수 있는가?
4. 유휴 자원 비용, 스토리지 비용, 네트워크 반출 비용까지 포함한 총비용을 계산했는가?
5. 고정 부하와 변동 부하를 구분해 예약 인스턴스, 스팟, 하이브리드 구성을 검토했는가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 콘솔에서 수작업으로만 서버를 만들어 동일한 환경을 재현하지 못하는 경우
- VM만 클라우드로 옮기고 자동 확장·이미지 표준화·[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 자동화를 하지 않는 경우
- CSP가 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 내부 OS 패치와 계정 통제까지 책임진다고 오해하는 경우
- 상태 저장 애플리케이션을 무계획으로 수평 확장해 세션과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 문제를 만드는 경우

기술사 답안에서는 IaaS를 "서버를 빌리는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)"라고만 쓰면 얕다. **[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/), 공동 책임, 자동화, 비용 구조, 상위 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와의 경계**를 함께 설명해야 실제 설계 판단으로 이어진다.

- **📢 섹션 요약 비유**: 대형 행사를 위해 설비 좋은 공연장을 빌리면 무대와 전기는 준비되어 있지만, 조명 세팅과 안전관리, 공연 운영은 주최 측이 직접 챙겨야 한다. 공연장을 빌렸다고 공연 준비 책임까지 사라지는 것은 아니다.

---

## Ⅴ. 기대효과 및 결론

IaaS가 잘 도입되면 인프라 조달 속도가 빨라지고, 환경 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 쉬워지며, 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)와 지역 확장 전략이 현실적인 옵션이 된다. 개발·테스트·운영 환경을 같은 방식으로 코드화할 수 있어 표준화와 자동화 수준도 높아진다. 이 점에서 IaaS의 가장 큰 효과는 단순 비용 절감보다 **인프라 실험 속도와 운영 민첩성 향상**에 있다.

그러나 IaaS는 "제로 운영"이 아니다. 높은 자유도만큼 보안 패치, 네트워크 설계, 용량 계획, 비용 최적화 책임이 남는다. 특히 VM을 오래 켜 둘수록 비용이 쌓이는 구조에서는 자동 종료, 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/), 예약 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 저장소 수명주기 같은 운영 규율이 필수다.

앞으로는 마이크로VM, [베어메탈 클라우드](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/629_bare_metal_cloud/), [분산 클라우드](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/242_distributed_cloud_edge_computing_aws_outposts/), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형 가속기처럼 형태가 더 다양해지더라도 본질은 크게 달라지지 않는다. IaaS는 "하드웨어가 사라진다"가 아니라, **하드웨어가 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 뒤로 숨는다**는 개념으로 기억하는 것이 맞다. 즉 인프라가 없어지는 것이 아니라, 프로그래밍 가능한 형태로 추상화되는 것이다.

- **📢 섹션 요약 비유**: 좋은 렌터카 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 차를 바로 빌려 주고 필요 없으면 반납하게 해 주지만, 운전과 연료 관리, 사고 예방은 여전히 운전자의 책임이다. IaaS도 편리한 대여 시스템이지, 책임까지 모두 없애 주는 마법은 아니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)) | 물리 서버를 여러 VM으로 나누어 IaaS 자원 풀을 만드는 핵심 기술이다. |
| 가상 머신 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) | 사용자가 OS 수준 제어권을 갖고 운영하는 IaaS의 대표 실행 단위다. |
| 가상 [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) ([Virtual Private Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/028_vpc/), [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/)) | 서브넷, [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 보안 그룹으로 네트워크 경계를 정의하는 기반이다. |
| 블록 스토리지 | VM에 부착되는 영구 디스크로 상태 저장 워크로드의 핵심이다. |
| 공동 책임 모델 (Shared Responsibility Model) | CSP와 사용자가 어디까지 책임지는지 구분하는 운영 원칙이다. |
| [인프라스트럭처 애즈 코드](/knowledge-base/studynote/12_it_management/05_security_compliance/207_iac_terraform_immutable_infrastructure/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) | IaaS 자원을 수작업이 아닌 선언적 코드로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·변경하게 해 준다. |
| 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) ([Auto Scaling](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/)) | 변동 부하에 따라 IaaS 인스턴스를 자동 증감시키는 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/) 메커니즘이다. |
| [재해 복구](/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) (Disaster [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)) | [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 다중 리전 구성을 통해 IaaS에서 구현되는 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 전략이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
물리 데이터센터 자원
        │
        ▼
가상화 · 자원 풀링
        │
        ▼
IaaS (Infrastructure as a Service)
        │
        ├──────────────► VM · VPC · Block Storage
        ├──────────────► IaC · Auto Scaling
        ├──────────────► DR · Multi-region 운영
        └──────────────► PaaS · Kubernetes 기반 인프라
```

이 흐름은 하드웨어 중심 사고가 소프트웨어 정의 인프라로 넘어가고, 다시 상위 플랫폼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 확장되는 경로를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. IaaS는 거대한 장난감 창고에서 필요한 블록과 책상, 전선을 바로 빌려 주는 가게와 비슷해요.
2. 그래서 장난감 방을 새로 꾸밀 때 오래 기다리지 않고 바로 만들 수 있어요.
3. 하지만 빌린 블록으로 무엇을 만들고 어떻게 정리할지는 여전히 우리가 직접 해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 183 / 552

← **이전**: [182. 클라우드 서비스 모델 (Cloud Service Models) 개요](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/182_cloud_service_models_overview/)
**다음**: [184. PaaS (Platform as a Service) - 애플리케이션 실행 플랫폼 제공](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) →

---
