+++
weight = 52
title = "52. 클라우드 컴퓨팅 (Cloud Computing) - OS 관점"
date = "2026-05-01"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 컴퓨팅 (Cloud Computing)은 [[001_operating_system_purpose|운영체제]] (OS) 개념을 네트워크 너머의 자원 풀에 확장해, 하드웨어를 [[198_abstraction_control_data_process|추상화]]하고 공유하는 [[136_variance|분산]] 인프라 모델이다.
> 2. **가치**: [[015_virtualization|가상화]] ([[190_virtualization_computing_architecture_cloud|Virtualization]]), [[561_container_based_deployment|컨테이너]] ([[194_container_virtualization_docker_namespace|Container]]), [[073_container_orchestration_tools|오케스트레이션]] ([[073_container_orchestration_tools|Orchestration]])을 통해 격리 ([[195_isolation_concurrency_control|Isolation]])와 [[571_resiliency_fault_tolerance_patterns|탄력성]] (Elasticity)을 동시에 제공한다.
> 3. **판단 포인트**: [[598_vm_migration_nic|VM]] ([[598_vm_migration_nic|Virtual Machine]]), [[561_container_based_deployment|컨테이너]], [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]])는 같은 "자원 [[198_abstraction_control_data_process|추상화]]" 계열이지만, 제어권·시작 속도·격리 강도가 다르므로 워크로드에 맞춰 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[[001_operating_system_purpose|운영체제]]의 본질은 CPU, 메모리, 저장장치, 네트워크라는 희소 자원을 여러 프로그램에 공정하게 나눠 주는 것이다. 클라우드는 이 역할을 단일 컴퓨터가 아니라 여러 물리 서버 전체에 적용한다. 즉 OS가 프로세스와 [[501_file_definition_logical_record|파일]]을 [[198_abstraction_control_data_process|추상화]]하듯, 클라우드는 물리 서버와 네트워크를 [[090_service_kubernetes_network_load_balancing|서비스]] 단위로 [[198_abstraction_control_data_process|추상화]]한다.

이 모델이 필요한 이유는 기존 데이터센터가 과잉 [[528_provisioning|프로비저닝]] (Over-provisioning)에 의존했기 때문이다. 트래픽 폭증을 대비해 서버를 미리 사두면 낮은 가동률이 생기고, 반대로 부족하면 장애가 난다. 클라우드는 이 문제를 자원 풀링과 자동 확장으로 해결한다.

- **📢 섹션 요약 비유**: 클라우드는 각 집에 우물을 파지 않고, 마을 전체가 공동 수도관을 쓰는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OS 관점에서 클라우드는 하드웨어 위에 [[015_virtualization|가상화]] 층을 올리고, 그 위에 격리된 실행 환경을 다수 제공하는 구조다. [[054_hypervisor|하이퍼바이저]] ([[054_hypervisor|Hypervisor]])는 VM을, [[561_container_based_deployment|컨테이너]] 런타임은 프로세스 격리를, 오케스트레이터는 이 둘의 배치를 관리한다.

```text
┌──────────────────────────────────────────────────────────────┐
│               OS 관점의 클라우드 추상화 계층                │
├──────────────────────────────────────────────────────────────┤
│ 애플리케이션 / 서비스 / API                                  │
│          ▲                                                   │
│ VM / Container / Serverless                                 │
│          ▲                                                   │
│ 하이퍼바이저 · 런타임 · 오케스트레이터                       │
│          ▲                                                   │
│ CPU · Memory · Disk · Network · Hardware                    │
└──────────────────────────────────────────────────────────────┘
```

| OS 메커니즘 | 클라우드에서의 역할 | 핵심 기술 |
| :--- | :--- | :--- |
| 프로세스 스케줄링 | 다중 테넌트 자원 배분 | [[062_cgroups|cgroups]], CPU [[551_quota_disk_limit|quota]] |
| 메모리 관리 | 오버커밋과 격리 | [[381_virtual_memory|가상 메모리]], [[286_page_frame|page]] cache |
| [[501_file_definition_logical_record|파일]] 시스템 | 이미지/[[022_snapshot_backup_architecture|스냅샷]]/볼륨 제공 | 스토리지 [[015_virtualization|가상화]] |
| 네트워크 관리 | 가상 [[587_nic_offloading|NIC]], [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] | [[836_vpc_virtual_private_cloud_subnet_isolation|VPC]], [[633_sdn_whitebox|SDN]] |
| 보안/격리 | 테넌트 분리 | [[061_namespace|namespace]], [[583_selinux|SELinux]] |

클라우드의 핵심은 "공유하면서도 섞이지 않게" 만드는 것이다. OS가 하나의 서버에서 프로세스 간 간섭을 막듯, 클라우드는 서로 다른 테넌트가 같은 물리 자원을 써도 안전하도록 격리를 설계한다.

- **📢 섹션 요약 비유**: 클라우드 OS는 아파트 관리인과 같다. 같은 건물에 여러 세입자가 살아도, 각자 방은 잠겨 있고 공용 시설만 함께 쓴다.

---

## Ⅲ. 비교 및 연결

클라우드의 핵심 선택지는 [[598_vm_migration_nic|VM]], [[561_container_based_deployment|컨테이너]], [[206_serverless_cold_start|서버리스]]다. VM은 강한 격리와 OS 단위 제어가 좋고, [[561_container_based_deployment|컨테이너]]는 가볍고 빠르며, [[206_serverless_cold_start|서버리스]]는 실행 단위만 남겨 운영 부담을 최소화한다. 같은 자원 [[198_abstraction_control_data_process|추상화]]지만 목적이 다르다.

| 항목 | [[598_vm_migration_nic|VM]] | [[561_container_based_deployment|컨테이너]] | [[206_serverless_cold_start|서버리스]] |
| :--- | :--- | :--- | :--- |
| 격리 단위 | 게스트 OS | 프로세스/[[061_namespace|네임스페이스]] | 함수/이벤트 |
| 시작 속도 | 느림 | 빠름 | 매우 빠름 |
| 제어권 | 높음 | 중간 | 낮음 |
| 대표 용도 | 레거시, 강한 격리 | [[532_microservices_decomposition_patterns|마이크로서비스]] | 이벤트 기반 작업 |

또한 클라우드는 단순 호스팅이 아니라 OS 설계 원리를 대규모로 확장한 결과다. 스케줄러는 CPU를, [[501_file_definition_logical_record|파일]] 시스템은 오브젝트 스토리지를, 네트워크 스택은 VPC와 서브넷을 닮았다. 그래서 OS 지식이 있으면 클라우드의 병목과 장애를 훨씬 빠르게 이해할 수 있다.

- **📢 섹션 요약 비유**: VM은 개인 자가용, [[561_container_based_deployment|컨테이너]]는 카풀, [[206_serverless_cold_start|서버리스]]는 목적지만 말하면 태워주는 호출형 택시와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 워크로드 특성에 따라 형태를 고른다. 규제가 강하고 OS 레벨 제어가 필요하면 [[598_vm_migration_nic|VM]], 빠른 배포와 고밀도 운영이 중요하면 [[561_container_based_deployment|컨테이너]], 이벤트 중심이고 관리 부담을 줄여야 하면 [[206_serverless_cold_start|서버리스]]를 선택한다. 중요한 것은 "클라우드라서 무조건 좋다"가 아니라 "어떤 수준의 [[198_abstraction_control_data_process|추상화]]가 적절한가"다.

### [[435_checklist_based_testing|체크리스트]]

1. 강한 격리가 필요한가, 아니면 밀도와 속도가 더 중요한가?
2. 상태 저장 (Stateful) 워크로드인가, 무상태 ([[239_stateless_redis|Stateless]]) 워크로드인가?
3. 자동 확장과 관측 ([[642_observability_telemetry|Observability]])을 운영 체계에 포함했는가?
4. 과도한 [[051_vendor_lock_in_cloud_computing|벤더 종속]] ([[254_cloud_vendor_lock_in_avoidance_portability_multi_cloud|Vendor Lock-in]])을 허용할 만큼의 이점이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 것을 VM으로만 밀어 넣는 설계
- 상태ful [[090_service_kubernetes_network_load_balancing|서비스]]를 [[206_serverless_cold_start|서버리스]]로 억지 전환하는 설계
- 보안 경계 없이 [[561_container_based_deployment|컨테이너]]만 쌓아 올리는 설계

클라우드 도입은 OS를 버리는 것이 아니라, OS의 자원 관리 철학을 [[136_variance|분산]] 환경에 맞게 재배치하는 일이다. 그래서 클라우드 설계는 인프라 운영과 함께 격리, 스케줄링, 스토리지, 네트워크를 함께 봐야 한다.

- **📢 섹션 요약 비유**: 클라우드 선택은 짐을 넣는 여행 가방 고르기와 같다. 튼튼한 하드케이스가 필요한 짐도 있고, 가볍고 빠른 배낭이 더 맞는 짐도 있다.

---

## Ⅴ. 기대효과 및 결론

클라우드는 자원 효율과 확장성을 크게 높여 준다. OS 관점에서 보면, 클라우드는 "하나의 컴퓨터를 잘 쓰는 기술"이 아니라 "수천 대의 컴퓨터를 하나처럼 보이게 쓰는 기술"이다. 이 [[198_abstraction_control_data_process|추상화]] 덕분에 기업은 CAPEX를 OPEX로 바꾸고, [[090_service_kubernetes_network_load_balancing|서비스]]는 수요에 맞춰 빠르게 커졌다 작아진다.

하지만 [[198_abstraction_control_data_process|추상화]]가 강할수록 복잡성도 뒤로 숨어든다. 결국 클라우드를 잘 쓰려면 OS의 기본 원리, 특히 격리와 스케줄링과 자원 회수의 관점을 놓치지 않아야 한다.

- **📢 섹션 요약 비유**: 클라우드는 무대 뒤의 로봇 조명 시스템과 같다. 관객은 단추만 누르지만, 뒤에서는 수많은 기계가 정교하게 움직여 장면을 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[054_hypervisor|하이퍼바이저]] ([[054_hypervisor|Hypervisor]]) | VM을 만드는 [[015_virtualization|가상화]] 계층 |
| [[561_container_based_deployment|컨테이너]] ([[194_container_virtualization_docker_namespace|Container]]) | 프로세스 단위 경량 격리 |
| [[062_cgroups|cgroups]] / [[061_namespace|namespace]] | OS가 자원을 분리하는 핵심 메커니즘 |
| 오케스트레이터 | 배치, [[658_ir_recovery|복구]], 확장을 자동화 |
| [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]]) | 실행 단위만 남긴 극단적 [[198_abstraction_control_data_process|추상화]] |

### 📈 관련 키워드 및 발전 흐름도

```text
전통적 OS 자원 관리
    │
    ▼
가상화 (Virtualization)
    │
    ▼
VM (Virtual Machine) · 하이퍼바이저
    │
    ▼
컨테이너 (Container) · 오케스트레이션
    │
    ▼
클라우드 네이티브 · 서버리스
```

이 흐름은 로컬 자원 관리가 네트워크 규모의 [[090_service_kubernetes_network_load_balancing|서비스]] [[198_abstraction_control_data_process|추상화]]로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 클라우드는 컴퓨터를 여러 칸으로 나눠서 여러 사람이 안전하게 쓰게 하는 큰 건물이에요.
2. 어떤 칸은 벽이 두꺼운 방, 어떤 칸은 가벼운 텐트, 어떤 칸은 아예 필요한 순간만 열리는 방이에요.
3. 그래서 필요한 만큼만 쓰고, 필요할 때 빨리 늘릴 수 있어요.
