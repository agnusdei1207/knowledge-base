+++
title = "663. 반가상화 (Paravirtualization) I/O"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) ([Paravirtualization](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)) I/O는 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 자신이 가상 환경에 있다는 사실을 알고, [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)와 합의한 전용 인터페이스로 입출력 (Input/Output, I/O)을 처리하는 방식이다.
> 2. **가치**: 하드웨어 장치 레지스터를 하나씩 흉내 내는 대신 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)와 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)로 요청을 전달해, 에뮬레이션 기반 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)보다 훨씬 낮은 지연과 높은 처리량을 얻는다.
> 3. **판단 포인트**: 대부분의 서버 워크로드에서는 가장 균형 잡힌 선택이지만, 전용 드라이버가 필요하므로 레거시 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)은 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)보다 낮다.

---

## Ⅰ. 개요 및 필요성

[반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 “가상 환경임을 숨기는” 대신 “가상 환경에 맞는 빠른 통로를 제공하는” 철학에서 출발한다. [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)에서는 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 실제 네트워크 카드나 디스크 컨트롤러를 만진다고 믿고 장치 레지스터를 조작한다. 그러면 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 그 동작을 하나하나 가로채어 해석해야 하므로, 패킷 하나와 디스크 요청 하나에도 수차례의 제어 전환과 에뮬레이션 비용이 붙는다. 서버 워크로드가 커질수록 중앙 처리 장치 (Central Processing Unit, CPU)는 일을 하는 시간보다 “손님이 무슨 말을 했는지 통역하는 시간”을 더 많이 쓰게 된다.

이 그림은 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O가 왜 빠른지, 그리고 어떤 통로를 새로 만든 것인지를 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│              반가상화 I/O의 기본 구조: 전용 통로로 직접 협력             │
├────────────────────────────────────────────────────────────────────────────┤
│ Guest 가상 머신                                                            │
│   App ─▶ Front-end Driver ─┐                                               │
│                            │ Shared Memory Ring                            │
│                            ├──────────────────────────────┐                │
│                            │                              ▼                │
│                        Notify / Hypercall         Back-end Driver          │
│                                                       │                    │
│                                                       ▼                    │
│                                                 Physical Device            │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로와 제어 경로를 분리하는 데 있다. 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 버퍼에 쌓아 두고, “처리 시작”이나 “완료 통지” 같은 최소한의 신호만 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)와 주고받는다. 그래서 게스트는 굳이 오래된 하드웨어 규약을 흉내 낼 필요가 없고, [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)도 복잡한 장치 동작을 전부 연기할 필요가 없다.

- **📢 섹션 요약 비유**: [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 손님과 주방이 서로의 일을 아는 오픈 키친과 같다. 손님이 냄비 위치를 하나씩 물어보는 대신 주문표만 정확히 넘기면 훨씬 빨리 식사가 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O의 구현은 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)마다 조금 다르지만 구조는 비슷하다. 게스트 안에는 프런트엔드 드라이버 (Front-end Driver)가 있고, [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 쪽에는 백엔드 드라이버 (Back-end Driver)가 있다. 프런트엔드는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에게는 일반 네트워크 장치나 블록 장치처럼 보이면서, 실제로는 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 큐에 요청 디스크립터를 넣는다. 백엔드는 이 큐를 읽어 실제 장치나 호스트 네트워크 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/), 스토리지 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 연결한다.

| 구성요소 | 역할 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 포인트 |
| :-- | :-- | :-- |
| Front-end Driver | 게스트 안에서 요청 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 게스트 커널과 자연스럽게 연결 |
| Back-end Driver | 호스트 쪽 실제 처리 담당 | 다수 가상 머신 요청을 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) 가능 |
| [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 링 | 요청과 완료 정보 전달 | 복사 횟수와 [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/) 수를 크게 줄임 |
| Notify / Event | 처리 시작과 완료 알림 | 짧은 제어 신호만 교환 |
| 다중 큐 | 코어별 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) I/O | 네트워크와 스토리지 병목 완화 |

실제 동작은 보통 네 단계다. 첫째, 게스트가 보낼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)나 읽을 버퍼 정보를 디스크립터로 적어 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 큐에 넣는다. 둘째, 짧은 하이퍼콜 (Hypercall)이나 이벤트 알림으로 백엔드에 새 요청이 있음을 알려 준다. 셋째, 백엔드는 여러 요청을 묶어 실제 장치에 전달하고 결과를 완료 큐에 기록한다. 넷째, 게스트는 완료 이벤트를 받고 후속 처리를 한다. 이 구조 덕분에 패킷마다 장치 레지스터를 읽고 쓰는 비용, 인터럽트마다 반복되는 문맥 전환, 불필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 횟수가 함께 줄어든다.

[반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O가 빠르다고 해서 항상 단순한 것은 아니다. 드라이버 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 불일치, [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) 기능 충돌, 큐 개수 부족 같은 실무 이슈가 발생할 수 있다. 하지만 이런 문제는 “합의된 규약 안에서 조정”하면 해결 가능하다. [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)가 물리 장치를 완벽하게 흉내 내는 부담을 안는다면, [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)는 처음부터 가상 환경에 맞는 계약을 맺고 시작하는 방식이다.

- **📢 섹션 요약 비유**: [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 회전초밥 레일과 같다. 손님은 접시에 주문표를 올려두고, 요리사는 레일을 따라 한꺼번에 처리한다. 자리에서 계속 일어나 전달할 필요가 없다.

---

## Ⅲ. 비교 및 연결

[반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O의 장점은 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)와 장치 패스스루 사이에서 가장 실용적인 균형을 만든다는 데 있다. [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)는 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이 뛰어나지만 느리고, 장치 패스스루는 매우 빠르지만 [라이브 마이그레이션](/knowledge-base/studynote/02_operating_system/10_security/629_live_migration_pre_copy/)과 장치 공유가 어렵다. [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)는 이 둘의 중간에서 “충분히 빠르면서도 운영 유연성이 높은 기본값” 역할을 맡는다.

| 비교 항목 | [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O | [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O | 장치 패스스루 |
| :-- | :-- | :-- | :-- |
| 게스트 수정 여부 | 수정 없이 가능 | 전용 드라이버 필요 | 전용 드라이버와 하드웨어 지원 필요 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 낮음 | 높음 | 매우 높음 |
| [라이브 마이그레이션](/knowledge-base/studynote/02_operating_system/10_security/629_live_migration_pre_copy/) | 쉬움 | 쉬움 | 어려움 |
| 장치 공유 | 쉬움 | 쉬움 | 제한적 |
| 대표 기술 | 에뮬레이션 장치 | Virtio, Xen용 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버, vmxnet3 | 하드웨어 패스스루 |

여기서 Virtio는 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O를 표준화한 대표 규약으로 기억하면 된다. [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 자체는 개념이고, Virtio는 그 개념을 다양한 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)에서 공통 장치 모델로 구현하는 대표적 실체다. 또한 단일 루트 입출력 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) (Single Root I/O [Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/), [SR-IOV](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/497_sr_iov_pcie_mapping/))는 장치 패스스루 쪽으로 더 기울어진 접근이라 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 높지만 운영 유연성은 줄어든다. 따라서 클라우드 기본값은 대개 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/), 극한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 구간은 패스스루, 레거시 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)은 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)로 정리하면 판단이 쉽다.

- **📢 섹션 요약 비유**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)가 통역사를 끼고 말하는 방식이라면, [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)는 공용 업무 언어를 배우는 방식이고, 패스스루는 아예 자기 전용 직통전화를 쓰는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 웹 서버, 애플리케이션 서버, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), 메시지 큐, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 노드처럼 일반적인 서버 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 대부분에 가장 먼저 검토하는 선택지다. 예를 들어 가상 머신 안의 웹 서버가 초당 수만 개의 요청을 처리해야 한다면, 에뮬레이션 네트워크 장치로는 CPU가 패킷 해석 비용에 묶인다. 반면 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 네트워크 드라이버와 다중 큐를 적용하면 코어별 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리가 가능해지고, 동일 하드웨어에서 수용 가능한 가상 머신 수와 처리량이 함께 올라간다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버가 기본 포함되거나 안정적으로 설치 가능한가?
2. 네트워크와 블록 장치의 큐 개수가 가상 중앙 처리 장치 (virtual CPU, vCPU) 수와 워크로드 패턴에 맞는가?
3. [체크섬](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/), 세그먼트 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) 같은 기능이 게스트와 호스트에서 충돌하지 않는가?
4. 마이그레이션, [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 같은 운영 절차가 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 장치 모델과 호환되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설치가 쉽다는 이유만으로 [서비스 운영](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_service_operation/) 단계까지 에뮬레이션 장치를 그대로 두는 것
- [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버를 깔아 놓고도 단일 큐 설정으로 멀티코어 서버의 이점을 버리는 것
- 네트워크 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) 기능 불일치로 패킷 오류가 나는데도 원인을 애플리케이션으로만 돌리는 것

기술사 판단의 핵심은 “기본값으로 쓸 수 있는가”다. 일반적인 기업 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 클라우드 환경에서는 대부분 그렇다. 다만 오래된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 드라이버 설치가 불가능한 보안 제품, 특수 하드웨어를 직접 다뤄야 하는 저지연 장비처럼 예외 조건이 뚜렷하면 다른 선택지를 검토해야 한다.

- **📢 섹션 요약 비유**: [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 고속버스 전용차로와 같다. 조금의 규칙만 맞추면 대부분의 승객이 가장 빠르고 안정적으로 이동할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O의 기대효과는 단순한 벤치마크 수치 이상이다. 같은 서버에서 더 많은 가상 머신을 수용하고, 같은 애플리케이션에서 더 낮은 CPU 사용률로 더 높은 처리량을 내며, 마이그레이션과 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 같은 운영 편의도 유지할 수 있다. 그래서 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 “[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 기법”을 넘어 “[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)가 기본 인프라가 되게 만든 현실적 타협점”이라고 볼 수 있다.

한계는 분명하다. 게스트가 협력해야 하고, 드라이버 품질과 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리가 중요하며, 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 면에서는 패스스루를 완전히 대체하지 못한다. 그럼에도 불구하고 대부분의 서버 환경에서 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 가장 넓은 적용 범위를 가진다. 따라서 이 기술은 “가상 I/O의 기본형”으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 모두가 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 좋은 표준 배송 상자와 같다. [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 개인 전세기는 아니지만, 빠르고 싸고 관리하기 쉬워서 현실 세계의 대부분 배송이 이 방식으로 돌아간다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| Front-end / Back-end Driver | 게스트와 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 역할을 나누는 기본 구조 |
| [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 링 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로에서 복사와 [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)을 줄이는 핵심 장치 |
| Hypercall | 게스트가 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)에 최소 제어 신호를 보내는 방법 |
| Virtio | [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O를 표준화한 대표 규약 |
| [SR-IOV](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/497_sr_iov_pcie_mapping/) | 더 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 이후 검토하는 하드웨어 분할 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
장치 에뮬레이션 중심 I/O
    │
    ▼
게스트 협력형 반가상화 I/O
    │
    ▼
공유 메모리 링 · 하이퍼콜 · 다중 큐
    │
    ▼
Virtio 표준화
    │
    ▼
SR-IOV · vhost 같은 고성능 데이터 경로 최적화
```

이 흐름은 가상 I/O가 “[호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 우선”에서 “협력 기반 효율화”를 거쳐 “표준화와 고성능 분화”로 발전한 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O는 컴퓨터들이 서로 비밀 신호를 미리 약속해 두고 빠르게 이야기하는 방법이에요.
2. 그래서 매번 긴 설명을 하지 않아도 필요한 물건을 빨리 주고받을 수 있어요.
3. 대신 이 비밀 신호를 아는 친구들끼리만 가장 빠르게 움직일 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 664 / 803

← **이전**: [662. 그림자 페이지 테이블 (Shadow Page Table)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/662_shadow_page_table/)
**다음**: [664. 전가상화 (Full Virtualization) I/O](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/664_full_virtualization_io/) →

---
