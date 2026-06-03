+++
weight = 102
title = "에어 갭 (Air-gapped) 환경의 CI/CD: 폐쇄망 배포 전략"
date = "2026-03-04"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 에어 갭 (Air-gapped) 환경의 [[090_configuration_item|CI]]/CD는 외부 인터넷과 물리적으로 단절된 폐쇄망에서 애플리케이션 빌드, 반입, 배포를 안전하게 자동화하는 특수 [[123_pipe|파이프]]라인 [[268_strategy_pattern|전략]]이다.
> 2. **가치**: 소스코드, 의존성 [[336_library_vs_framework|라이브러리]], [[063_docker_architecture|도커]] ([[063_docker_architecture|Docker]]) 이미지를 타르볼 (Tarball) 형태의 패키지로 묶어 오프라인으로 반입함으로써, 군사/금융/국가 인프라 수준의 [[003_integrity|무결성]]과 [[186_dlp_data_loss_prevention|데이터 유출 방지]]를 보장한다.
> 3. **판단 포인트**: 의존성이 런타임에 동적으로 다운로드되는 것을 원천 차단해야 하며, 반입 전 보안 스캔과 [[001_dikw_pyramid|데이터]] [[011_diode|다이오드]] ([[001_dikw_pyramid|Data]] [[011_diode|Diode]]) 같은 일방향 전송 체계를 통해 보안과 배포 속도 간의 균형을 맞추어야 한다.

---

## Ⅰ. 개요 및 필요성

일반적인 [[531_cloud_native_architecture|클라우드 네이티브]] [[090_configuration_item|CI]]/CD 환경은 GitHub에서 코드를 가져오고, [[063_docker_architecture|Docker]] Hub나 NPM (Node Package Manager) 같은 외부 퍼블릭 저장소에 상시 연결되어 [[336_library_vs_framework|라이브러리]]를 동적으로 다운로드한다. 그러나 국가 안보 시설, 금융 코어 망, 원자력 발전소와 같은 에어 갭 (Air-gapped) 환경은 보안상의 이유로 외부 인터넷과의 물리적 연결이 완벽하게 차단되어 있다.

이러한 [[182_network_separation_model|망분리]] 환경에서는 `npm install`이나 `docker pull` 같은 일상적인 [[158_instruction|명령어]]가 모두 실패한다. 외부 통신이 불가능하다는 제약 조건 속에서도 개발 생산성을 유지하고 수동 배포로 인한 인적 오류 (Human Error)를 막기 위해서는, 오프라인 반입을 전제로 한 정적 패키징 및 자체 미러 (Mirror) 저장소 구축 중심의 특수한 [[090_configuration_item|CI]]/CD 아키텍처가 반드시 필요하다.

- **📢 섹션 요약 비유**: 일반 [[090_configuration_item|CI]]/CD가 수도관을 연결해 물을 콸콸 틀어 쓰는 방식이라면, 에어 갭 [[090_configuration_item|CI]]/CD는 밖에서 생수통을 안전하게 포장해 검문소를 거친 뒤 격리된 벙커 안으로 직접 들고 들어가는 생수 배달 방식입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

에어 갭 배포 아키텍처는 크게 외부망에서의 '정적 패키징', 물리적 '반입 및 [[395_verification_process_review|검증]]', 내부망에서의 '로컬 [[333_raid_1|미러링]] 및 배포' 3단계로 나뉜다. 모든 의존성은 외부망에서 하나의 아카이브 (Tarball 등)로 병합되어 반입된다.

```text
┌──────────────────────────────────────────────────────────────┐
│           에어 갭 (Air-gapped) CI/CD 반입 워크플로우           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [ 외부 인터넷 망 ]         [ 물리적 격리 구간 ]       [ 내부 폐쇄 망 ]  │
│                                                              │
│  1. 빌드 및 패키징         2. 보안 스캔/반입          3. 내부 배포       │
│  ┌────────────┐         ┌──────────────┐         ┌────────────┐  │
│  │ 외부 라이브러리│         │ 안티바이러스 │         │ 로컬 레지스트리│  │
│  │ 도커 베이스 이미지├─포장─▶ │ 단방향 전송망 │ ─반입─▶ │ 헬름 (Helm)  │  │
│  │ 자체 소스코드 │ (.tar) │ (Data Diode) │         │ K8s 클러스터 │  │
│  └────────────┘         └──────────────┘         └────────────┘  │
│      (모든 종속성              (물리적 망연계            (완전 오프라인    │
│       미리 포함)                 망분리 솔루션)            자동화 배포)    │
└──────────────────────────────────────────────────────────────┘
```

가장 핵심적인 원리는 벤더링 (Vendoring)이다. 외부망 빌드 단계에서 필요한 모든 [[336_library_vs_framework|라이브러리]]를 애플리케이션 [[506_directory_structure_symbol_table|디렉터리]]에 다운로드하여 묶고, [[068_docker_image_immutable_package|도커 이미지]] 역시 `docker save` 명령을 통해 `.tar` [[501_file_definition_logical_record|파일]]로 구워낸다. 이후 일방향 통신 장비 ([[001_dikw_pyramid|Data]] [[011_diode|Diode]])나 승인된 USB를 통해 반입되며, 폐쇄망 내부에 구축된 프라이빗 [[235_registry_immutable_tag|레지스트리]] (예: Harbor, Nexus)에 로드 (Load)되어 내부 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]가 이를 당겨간다.

| 배포 단계 | 주요 작업 | 사용 도구 및 기술 |
| :--- | :--- | :--- |
| **외부 준비** | 코드/이미지 빌드, 패키지 [[008_dependencies|종속성]] 완전 다운로드 | `docker save`, `npm pack`, Skopeo |
| **반입/검사** | 악성코드 검사, [[003_integrity|무결성]] 해시(SHA) [[395_verification_process_review|검증]], [[008_단방향_반이중_전이중|단방향]] 전송 | [[001_dikw_pyramid|Data]] [[011_diode|Diode]], 망연계 솔루션 |
| **내부 배포** | 로컬 [[235_registry_immutable_tag|레지스트리]] 업로드, [[119_gitops_single_source_of_truth|GitOps]] [[212_synchronization_mechanisms|동기화]] | Harbor, ArgoCD, `docker load` |

- **📢 섹션 요약 비유**: 우주정거장(폐쇄망)에 보급품을 보낼 때 우주에서는 물건을 살 수 없으므로, 지구(외부망)에서 나사 하나까지 전부 짐을 꾸려 우주선에 싣고 [[003_integrity|무결성]] 검사를 통과한 뒤에만 해치를 열어 물건을 꺼내는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

[[531_cloud_native_architecture|클라우드 네이티브]] 환경과 에어 갭 환경의 [[090_configuration_item|CI]]/CD는 속도와 보안의 트레이드오프를 명확히 보여준다.

| 항목 | 일반 클라우드 [[090_configuration_item|CI]]/CD | 에어 갭 (Air-gapped) [[090_configuration_item|CI]]/CD |
| :--- | :--- | :--- |
| **의존성 해결** | [[123_pipe|파이프]]라인 실행 시 동적 다운로드 | 사전 다운로드 후 정적 반입 (Vendoring) |
| **보안 통제** | [[690_firewall_generation_evolution|방화벽]], [[983_vpn_virtual_private_network|VPN]], 클라우드 [[526_iam|IAM]] | 망연계 솔루션, 물리적 [[121_transmission_media_guided_unguided|매체]] ([[359_usb|USB]], [[001_dikw_pyramid|Data]] [[011_diode|Diode]]) |
| **배포 [[015_지연_데이터_관점|지연]]** | 코드 커밋 후 수 분 내 즉각 배포 | 반입 심사 및 물리적 이동으로 인한 배치 (Batch) [[015_지연_데이터_관점|지연]] |
| **[[003_integrity|무결성]] [[395_verification_process_review|검증]]** | 런타임 보안 스캐닝 활용 | 반입 전 아카이브 해시(SHA) 및 악성코드 전수 검사 |

일반 환경이 [[123_pipe|파이프]]라인의 속도(Agility)에 집중한다면, 에어 갭 환경은 반입되는 [[075_artifact_management_nexus_docker_registry|아티팩트]] ([[075_artifact_management_nexus_docker_registry|Artifact]])가 변조되지 않았다는 확신(Trust)을 얻는 데 집중한다. 이는 최근 부상하는 [[890_sbom_cyclonedx_spdx|SBOM]] ([[690_sbom_software_supply_chain_security|소프트웨어 자재 명세서]])을 통한 [[374_supply_chain_security|공급망 보안]] [[164_policy|정책]]과도 직접적으로 연결된다.

- **📢 섹션 요약 비유**: 일반 [[090_configuration_item|CI]]/CD는 언제든 배달 앱으로 음식을 시켜 먹는 자유로운 가정집이고, 에어 갭 [[090_configuration_item|CI]]/CD는 외부에서 반입되는 모든 식자재를 독극물 검사 후 정해진 시간에만 들여보내는 왕의 수라간입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

폐쇄망 환경에서 아키텍처를 설계할 때는 "실수로 인터넷을 찾으려는 행위를 어떻게 방어할 것인가"가 가장 큰 판단 포인트다.

### [[435_checklist_based_testing|체크리스트]]
1. **베이스 이미지 최소화**: 반입 용량을 줄이기 위해 Distroless나 Alpine Linux 같이 불필요한 OS 패키지가 제거된 초경량 베이스 이미지를 사용하는가?
2. **로컬 미러 (Local Mirror) 구성**: 폐쇄망 내부에 NPM, Maven, [[063_docker_architecture|Docker]] Image를 [[456_caching|캐싱]]하는 통합 [[075_artifact_management_nexus_docker_registry|아티팩트]] 저장소 (Artifactory, Nexus 등)가 구성되어 있는가?
3. **오프라인 [[061_helm_charts|헬름 차트]] ([[056_helm_chart|Helm Chart]])**: [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 배포 시 [[061_helm_charts|헬름 차트]] 내부에 외부 이미지 저장소 URL이 하드코딩되지 않고 내부 [[235_registry_immutable_tag|레지스트리]]를 바라보도록 값이 치환되는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 개발자가 외부망에서 빌드된 `node_modules`를 OS 환경([[673_mac_message_authentication_code|Mac]]/Windows)이 다른 폐쇄망 리눅스 서버에 그대로 복사하여 실행 오류를 유발하는 방식
- 변경된 레이어 (Layer)만 추출하지 않고 매번 수 GB 단위의 전체 [[068_docker_image_immutable_package|도커 이미지]]를 반입하여 망연계 장비의 [[140_bandwidth|대역폭]]을 마비시키는 설계

- **📢 섹션 요약 비유**: 성안으로 식량을 나를 때 수레(망연계 장비)의 크기는 정해져 있으므로, 껍질이 다 까진 알맹이(경량 이미지)나 어제와 달라진 식량(증분 레이어)만 효율적으로 담아 날라야 성문이 막히지 않습니다.

---

## Ⅴ. 기대효과 및 결론

에어 갭 [[090_configuration_item|CI]]/CD [[268_strategy_pattern|전략]]을 구축하면 최고 수준의 보안 요구사항을 충족하면서도, 단절된 환경 내에서 [[561_container_based_deployment|컨테이너]] 기반의 현대적인 [[004_agile_relation|애자일]] ([[004_agile_relation|Agile]]) 배포 프로세스를 실현할 수 있다. 이는 외부 위협으로부터 시스템을 완전히 분리하면서도 개발팀의 릴리즈 [[194_consistency_database_integrity|일관성]]을 보장한다.

향후 폐쇄망 [[090_configuration_item|CI]]/CD는 단순히 [[501_file_definition_logical_record|파일]]을 옮기는 수준을 넘어, [[890_sbom_cyclonedx_spdx|SBOM]] 명세서를 통해 반입되는 모든 [[191_oss_license_compliance|오픈소스]]의 취약점을 내부망에서 오프라인 [[002_database_definition|데이터베이스]]로 매핑하여 능동적으로 방어하는 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) [[374_supply_chain_security|공급망 보안]] 생태계로 진화할 것이다. 결국 에어 갭 환경에서도 자동화는 불가능한 것이 아니라 정밀한 통제가 추가될 뿐이다.

- **📢 섹션 요약 비유**: 에어 갭 [[090_configuration_item|CI]]/CD는 외부와 완벽히 단절된 잠수함 안에서도 선원들이 쾌적하게 생활하고 임무를 수행할 수 있도록, 자체적인 공기 정화와 식량 보급 시스템을 완벽하게 오프라인 자동화해 두는 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[183_network_linkage_system|망연계 시스템]] ([[001_dikw_pyramid|Data]] [[011_diode|Diode]])** | 외부망에서 내부망으로 [[008_단방향_반이중_전이중|단방향]]으로만 [[001_dikw_pyramid|데이터]]를 전송하여 침입을 물리적으로 차단하는 보안 기술 |
| **벤더링 (Vendoring)** | 외부 의존성 패키지를 프로젝트 [[506_directory_structure_symbol_table|디렉터리]] 내부에 포함하여 오프라인 빌드를 가능하게 하는 기법 |
| **프라이빗 [[235_registry_immutable_tag|레지스트리]] (Private [[235_registry_immutable_tag|Registry]])** | 폐쇄망 내부에 구축되어 외부 [[063_docker_architecture|Docker]] Hub의 역할을 대신하는 내부 이미지 저장소 |
| **[[890_sbom_cyclonedx_spdx|SBOM]] ([[890_sbom_cyclonedx_spdx|Software Bill of Materials]])** | 폐쇄망 내부로 반입되는 소프트웨어 구성 요소의 투명성과 취약점 추적을 위한 명세서 |

### 📈 관련 키워드 및 발전 흐름도

```text
망분리 · 에어 갭 (Air-gapped) 환경 제약
    │
    ▼
오프라인 패키징 · 벤더링 (Vendoring) 적용
    │
    ▼
타르볼 (Tarball) 반입 · 망연계 솔루션 통과
    │
    ▼
프라이빗 레지스트리 구축 (Nexus, Harbor)
    │
    ▼
SBOM 기반 공급망 보안 · 내부 GitOps 배포 자동화
```

### 👶 어린이를 위한 3줄 비유 설명
1. 밖으로 절대 나갈 수 없고 택배 기사님도 들어올 수 없는 비밀 비밀기지가 있어요.
2. 기지 밖에서 엄마가 모든 장난감과 과자를 튼튼한 한 상자에 꽉꽉 담아 보안 요원에게 전달해요.
3. 보안 요원이 상자에 나쁜 벌레가 없는지 꼼꼼히 [[396_validation|확인]]한 뒤에만 기지 안으로 밀어 넣어 주는 배달 방법이에요.
