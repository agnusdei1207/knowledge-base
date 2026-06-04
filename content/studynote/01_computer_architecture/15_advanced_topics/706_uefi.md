+++
title = "706. UEFI (Unified Extensible Firmware Interface)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: UEFI (Unified Extensible [Firmware](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) Interface)는 레거시 BIOS를 대체한 표준 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 실행 환경으로, 전원 [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 직후부터 OS 로더 직전까지의 인터페이스와 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델을 규격화한다.
> 2. **가치**: 32/64비트 환경, [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) (GUID [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Table), [ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) (EFI System [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)), [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 같은 기능을 묶어 현대 디스크·보안·업데이트 체계를 가능하게 한다.
> 3. **판단 포인트**: UEFI는 단순히 "예쁜 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 화면"이 아니라 복잡한 부팅 플랫폼이므로, Boot 변수 관리·키 관리·[호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 잘못 다루면 오히려 부팅 장애와 보안 공백이 커질 수 있다.

---

## Ⅰ. 개요 및 필요성

UEFI는 플랫폼 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)와 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/) 사이를 표준화한 현대적 부팅 규격이다. 과거 BIOS는 16비트 real mode, [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 호출 기반 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) ([Master Boot Record](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)) 중심 구조에 묶여 있었다. 이 모델은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 시대에는 단순하고 충분했지만, 메모리 용량과 디스크 크기, 보안 요구가 커지면서 확장성이 급격히 떨어졌다.

가장 큰 문제는 세 가지였다. 첫째, BIOS는 레거시 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 옵션 롬 중심 구조라 드라이버 모델이 제한적이었다. 둘째, [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 기반 부팅은 약 2TiB 수준의 부팅 디스크 한계와 4개 기본 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 제약을 안고 있었다. 셋째, 부팅 과정 자체를 표준화된 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체계로 보호하기 어려워 부트킷과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 로더 변조에 취약했다.

UEFI는 이 한계를 넘기 위해 등장했다. [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 자체가 CPU의 native mode에서 더 풍부한 메모리와 드라이버 모델을 활용하고, 디스크는 GPT를, 부팅 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 ESP를, 보안은 Secure Boot와 NVRAM 변수 기반 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 관리하는 구조가 자리 잡았다. 즉 UEFI는 "부팅을 되게 하는 코드"를 넘어 "부팅을 운영 가능한 플랫폼"으로 바꾼 규격이다.

- **📢 섹션 요약 비유**: BIOS가 오래된 열쇠 한 개로 문만 겨우 여는 방식이었다면, UEFI는 출입 기록·전자키·안내판까지 갖춘 현대식 로비 시스템에 가깝다.

---

## Ⅱ. 아키텍처 및 핵심 원리

UEFI 부팅은 보통 [PI](/knowledge-base/studynote/12_it_management/01_governance_strategy/805_process_innovation/) (Platform Initialization) 흐름과 함께 이해한다. SEC ([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 단계가 CPU의 최소 실행 환경을 만들고, PEI (Pre-EFI Initialization) 단계가 메모리를 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화한다. DXE (Driver Execution [Environment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/)) 단계에서는 각종 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 드라이버와 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 로드되고, BDS (Boot Device [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/)) 단계가 실제 부팅 대상을 선택한다. 이후 OS 로더가 올라가 `ExitBootServices()`를 호출하면, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)의 부팅용 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 종료되고 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 메모리와 장치를 본격적으로 장악한다.

UEFI는 기능 면에서 두 층으로 나눠 보면 이해가 쉽다. Boot Services는 부팅 중에만 쓰이는 메모리 할당, [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 탐색, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 접근 같은 기능이고, Runtime Services는 부팅 후에도 제한적으로 남아 변수 읽기, 시간 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 같은 기능을 제공한다. 또한 부팅 대상은 [ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 안의 `.efi` 실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이며, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)는 NVRAM (Non-Volatile Random Access Memory)에 저장된 `BootOrder`, `Boot####` 변수를 읽어 어떤 로더를 먼저 실행할지 결정한다.

| 구성 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| SEC | CPU [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 실행 환경 형성 | 가장 먼저 실행되는 최소 코드 |
| PEI | [DRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화, 핸드오프 준비 | 메모리 사용 가능 상태 확보 |
| DXE | 드라이버·[프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 로드 | UEFI 기능의 대부분이 형성되는 단계 |
| BDS | 부팅 장치와 부트 엔트리 선택 | `BootOrder`와 [ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 탐색 |
| Boot Services | 부팅 중 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공 | `ExitBootServices()` 이후 종료 |
| Runtime Services | 부팅 후 제한적 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공 | 변수·시간 정보 등 유지 |

아래 그림은 UEFI의 부팅 경로를 단순화한 것이다.

```text
+--------------------------------------------------------------------+
|                     UEFI boot sequence                            |
+--------------------------------------------------------------------+
| Power on                                                          |
|   |                                                               |
|   v                                                               |
| SEC ---> PEI ---> DXE ---> BDS ---> ESP\EFI\*.efi                    |
|                             |                    |                |
|                             |                    v                |
|                             |             OS loader start         |
|                             v                    |                |
|                     Boot Services active          v                |
|                                         ExitBootServices()         |
|                                                   |                |
|                                                   v                |
|                                        OS takes hardware control   |
+--------------------------------------------------------------------+
```

중요한 점은 UEFI가 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 아니라는 사실이다. UEFI는 어디까지나 표준화된 pre-OS 환경이다. 하지만 그 환경이 충분히 풍부하기 때문에, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 접근, 네트워크 부팅, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 업데이트 캡슐 처리, [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 같은 기능이 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 이전 단계에서 이미 가능해진다.

- **📢 섹션 요약 비유**: UEFI는 공연 시작 전 무대 감독 시스템과 같다. 조명, 출연 순서, 출입 권한을 다 맞춘 뒤에야 본 공연인 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 올라온다.

---

## Ⅲ. 비교 및 연결

UEFI를 제대로 이해하려면 BIOS와 나란히 봐야 한다. BIOS는 단순하지만 기능이 적고 레거시 제약이 크다. UEFI는 더 복잡하지만, 그 복잡성 덕분에 현대 저장장치와 보안 기능을 수용할 수 있다. 즉 차이는 단순한 "구형 vs 새로운 유형의"이 아니라 "제한된 부팅 도구 vs 확장 가능한 부팅 플랫폼"에 가깝다.

| 항목 | 레거시 BIOS | UEFI |
| :--- | :--- | :--- |
| 실행 환경 | 16비트 real mode 중심 | 32/64비트 native mode 활용 |
| 디스크 부팅 방식 | [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 중심 | [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) + [ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) 중심 |
| 부팅 엔트리 관리 | 디스크 첫 섹터 의존 | NVRAM 변수 기반 |
| 드라이버 모델 | 제한적 option [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/) | DXE 드라이버·[프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 기반 |
| [보안 부팅](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) | 표준화 어려움 | [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 지원 |
| 업데이트 방식 | 벤더별 편차 큼 | Capsule update 등 표준화 가능 |

또한 UEFI는 다른 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 표준과도 연결된다. [ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/) (Advanced Configuration and [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Interface) 테이블은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 전력과 장치 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 이해하도록 돕고, [SMBIOS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/708_nvme_queue_management/) ([System Management BIOS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/708_nvme_queue_management/))는 시스템 인벤토리 정보를 제공한다. UEFI는 이런 테이블과 부팅 변수를 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에 넘기는 출발점 역할을 하므로, 현대 PC의 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 생태계에서 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 위치에 있다고 볼 수 있다.

Secure Boot도 이 연결 구조 속에서 이해해야 한다. UEFI는 Platform [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) (PK), [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Exchange [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) (KEK), 허용 서명 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(db), 차단 서명 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(dbx)를 기반으로 부트 로더와 옵션 바이너리의 서명을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다. 결국 UEFI는 "[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽어 OS를 시작하는 코드"를 넘어 "무엇을 믿고 시작할지 결정하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진"이기도 하다.

- **📢 섹션 요약 비유**: BIOS가 옛날 건물의 수동 차단기라면, UEFI는 출입 카드·감시 카메라·전광판이 연결된 통합 관제실에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 UEFI [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 하나가 부팅 성공 여부를 크게 바꾼다. 예를 들어 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설치 시 ESP가 손상되거나 `Boot####` 엔트리가 꼬이면 디스크 자체는 멀쩡해도 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)가 로더를 찾지 못한다. 또한 Secure Boot를 켠 상태에서 서명되지 않은 드라이버나 커스텀 부트 로더를 올리면 의도한 차단이 발생한다. 따라서 문제 해결은 "디스크가 고장 났나"보다 "[펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)가 어느 엔트리를 어떤 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 보고 있나"를 먼저 확인하는 쪽이 정확하다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. ESP가 FAT32로 정상 구성되어 있고, 부트 로더 경로가 올바른가?
2. `BootOrder`와 `Boot####` 엔트리가 중복·고아 상태 없이 정리되어 있는가?
3. [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 사용 시 서명 체인과 키 갱신 절차가 준비되어 있는가?
4. CSM ([Compatibility](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [Support](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) [Module](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)) 같은 레거시 호환 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 정말 필요한가?
5. [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 업데이트 시 [rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/) 경로와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 모드가 있는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 문제를 피하려고 무조건 끄고 끝내는 운영
- 레거시 장비 때문에 CSM을 상시 켜 두어 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)·보안 이점을 잃는 구성
- 듀얼 부팅 환경에서 여러 ESP와 부트 엔트리를 무질서하게 늘려 장애를 키우는 설계

기술사 관점에서는 "기능이 많다"보다 "[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 설계되었는가"를 묻는 것이 중요하다. 클라우드나 기업 환경에서는 캡슐 업데이트, 키 교체, 측정 부팅, 원격 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)까지 함께 설계되어야 UEFI의 복잡성을 이점으로 바꿀 수 있다. 반대로 이 운영 체계가 없다면, 풍부한 기능이 오히려 장애 표면이 될 수 있다.

- **📢 섹션 요약 비유**: UEFI 운용은 스마트 도어락 관리와 비슷하다. 기능이 많을수록 편리하지만, 카드 분실·비상 열쇠·관리자 권한까지 같이 준비해야 진짜 안전하다.

---

## Ⅴ. 기대효과 및 결론

UEFI의 가장 큰 효과는 부팅 경로의 표준화다. 디스크 구조, 부트 엔트리, 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 업데이트 방식이 공통 규격 위에 올라오면서 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 하드웨어 제조사 사이의 조합 가능성이 커졌다. 대용량 디스크 부팅, 네트워크 부팅, 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [보안 부팅](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 같은 현대 기능이 실용화된 배경에도 UEFI가 있다.

하지만 UEFI는 단순하지 않다. DXE 드라이버, 변수 저장소, 키 체인, 레거시 호환 모드까지 포함하면 오히려 BIOS보다 훨씬 큰 소프트웨어 스택이 된다. 그래서 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 실수, 벤더 구현 편차, 보안 취약점 관리가 항상 따라온다. 결국 UEFI의 가치는 기능 수보다 그 기능을 통제할 운영 성숙도에 달려 있다.

정리하면 UEFI는 현대 PC와 서버의 부팅을 가능하게 하는 공통 언어다. BIOS를 단순히 대체한 것이 아니라, 부팅·보안·업데이트를 하나의 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 가능한 플랫폼으로 묶어낸 규격으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: UEFI는 현대 공항의 관제 시스템과 같다. 비행기를 띄우는 일 자체보다, 어떤 순서로 어떤 허가를 받고 안전하게 이륙시키는지가 더 중요하다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) | UEFI 부트 로더와 도구가 저장되는 표준 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이다 |
| [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) | 대용량 디스크와 유연한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 구성을 가능하게 하는 디스크 레이아웃이다 |
| DXE | UEFI 드라이버와 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 본격적으로 형성되는 핵심 단계다 |
| [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) | 서명된 부트 체인을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 로더 변조를 막는다 |
| NVRAM 변수 | 부트 순서와 보안 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 저장되는 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 저장소다 |
| Capsule update | [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)나 관리 도구가 표준 방식으로 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 업데이트를 전달하는 구조다 |

### 📈 관련 키워드 및 발전 흐름도

```text
레거시 BIOS의 16비트 · MBR 제약
    |
    v
UEFI 표준 실행 환경 도입
    |
    v
GPT + ESP 기반 부팅 체계
    |
    v
Secure Boot · NVRAM 정책 관리
    |
    v
Capsule update · measured boot 확장
```

이 흐름은 부팅이 단순 점프 코드에서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 플랫폼으로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터가 켜질 때는 바로 공부를 시작하는 게 아니라, 먼저 교실 문을 열고 자리표를 확인해야 해.
2. UEFI는 누가 어디로 들어가야 하는지, 진짜 학생인지, 어떤 책을 먼저 꺼낼지 정해 주는 선생님 같은 규칙이야.
3. 그래서 큰 컴퓨터도 헷갈리지 않고 안전하게 수업인 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)를 시작할 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 707 / 803

<- **이전**: [705. 오픈소스 펌웨어 (Coreboot, LinuxBoot)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/705_open_source_firmware_coreboot/)
**다음**: [707. ACPI (Advanced Configuration and Power Interface)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/707_acpi/) ->

---
