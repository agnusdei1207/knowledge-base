+++
title = "718. EDAC (Error Detection and Correction)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EDAC ([Error Detection](/knowledge-base/studynote/02_operating_system/01_overview_architecture/040_error_detection/) and Correction)은 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 메모리와 메모리 컨트롤러가 발견·교정한 하드웨어 오류를 운영체제가 읽을 수 있는 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 바꾸는 소프트웨어 관측 계층이다.
> 2. **가치**: 조용히 고쳐진 단일 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류도 추세로 보면 DIMM, 채널, 전원부 열화의 전조가 되므로, EDAC는 장애 복구보다 <strong>장애 예방</strong>에 더 큰 가치를 가진다.
> 3. **판단 포인트**: EDAC 숫자는 단순 합계보다 위치·증가 속도·반복 패턴이 중요하며, 같은 슬롯에서 교정 가능 오류가 누적되면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 살아 있어도 교체와 점검을 앞당겨야 한다.

---

## Ⅰ. 개요 및 필요성

EDAC은 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 하드웨어 오류를 "운영 가능한 정보"로 바꾸기 위해 제공하는 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 서브시스템이다. 메모리 컨트롤러와 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) 회로는 단일 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류처럼 교정 가능한 문제를 순식간에 고쳐 버리지만, 그렇게 조용히 지나간 오류도 장기간 누적되면 DIMM, 채널, [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/), 전원부 열화의 중요한 전조가 된다. 즉 하드웨어가 스스로 고쳤다고 해서 운영자가 몰라도 되는 것은 아니다.

특히 대규모 서버 팜에서는 "오늘 한 번 고쳐진 오류"보다 "같은 슬롯에서 일주일 동안 500번 고쳐진 오류"가 더 중요하다. EDAC은 바로 이런 추세를 읽기 위해 존재한다. 하드웨어가 만든 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)와 상태 정보를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 읽어 사람과 모니터링 시스템이 이해할 수 있는 메시지로 노출함으로써, 시스템은 장애 이후 대응에서 장애 이전 예방으로 한 단계 올라선다.

- **📢 섹션 요약 비유**: 작은 누수가 생길 때마다 관리인이 바로 닦아 버리면 당장은 티가 안 나지만, EDAC은 어느 배관에서 물이 자주 새는지 기록해 큰 파열이 오기 전에 배관을 갈게 해 주는 점검표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EDAC의 동작은 <strong>하드웨어 검출 → 플랫폼 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a> 기록 → <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 드라이버 해석 → <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>/<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/">카운터</a> 노출</strong>의 흐름으로 이해하면 쉽다. 메모리 오류가 발생하면 메모리 컨트롤러는 이를 CE (Corrected Error) 또는 UE (Uncorrected Error)로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고, MCA ([Machine Check Architecture](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/717_memory_mca/)) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)나 메모리 컨트롤러 전용 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)에 상태를 남긴다. 이후 리눅스의 EDAC 드라이버가 주기적으로 값을 읽거나 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 경로를 받아, 어떤 메모리 컨트롤러, 채널, DIMM에서 문제가 생겼는지 디코딩한다.

EDAC의 진짜 가치는 단순 출력이 아니라 <strong>토폴로지 해석</strong>에 있다. 같은 "정정 오류 1회"라도 `mc0/channel1/dimm0`에서 난 것인지, CPU [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 2의 특정 랭크에서 난 것인지에 따라 운영 대응이 달라진다. EDAC은 이 정보를 `sysfs`, `dmesg`, `rasdaemon` 같은 사용자 영역 도구로 노출해 장기적인 관측과 알림 연계를 가능하게 한다.

| 계층 | 주체 | EDAC 관점의 역할 |
| :-- | :-- | :-- |
| 오류 검출 | [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 로직 / 메모리 컨트롤러 | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류를 교정하거나 UE로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 상태 기록 | MCA [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) / IMC [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | 주소, 뱅크, 오류 유형 저장 |
| 해석 | EDAC [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 드라이버 | 슬롯·채널·DIMM 정보로 디코딩 |
| 노출 | `sysfs`, `dmesg`, tracepoint | 운영자가 읽을 수 있는 형태로 가시화 |
| 운영 자동화 | `rasdaemon`, 모니터링 시스템 | [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 초과 알람, 교체 의사결정 지원 |

아래 그림은 EDAC이 오류를 "고치는 기술"이 아니라, 하드웨어의 조용한 복구를 밖으로 꺼내는 관측 파이프라인임을 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                     EDAC의 관측 파이프라인                          │
├──────────────────────────────────────────────────────────────────────┤
│ DIMM 비트 오류                                                      │
│     │                                                               │
│     ▼                                                               │
│ ECC / 메모리 컨트롤러 ──▶ CE 교정 또는 UE 판정                     │
│     │                                                               │
│     ▼                                                               │
│ MCA 레지스터 · IMC 카운터에 기록                                   │
│     │                                                               │
│     ▼                                                               │
│ EDAC 커널 드라이버가 슬롯/채널 정보로 디코딩                       │
│     │                                                               │
│     ├── /sys/devices/system/edac/... 카운터                         │
│     ├── dmesg / 커널 로그                                            │
│     └── rasdaemon · 모니터링 시스템으로 전달                        │
└──────────────────────────────────────────────────────────────────────┘
```

결국 EDAC의 핵심 원리는 <strong>하드웨어 오류를 시간축이 있는 운영 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>로 바꾸는 것</strong>이다. 이 덕분에 운영자는 일회성 노이즈와 지속적 열화를 구분할 수 있고, 장애가 현실화되기 전에 부품 교체를 예약할 수 있다.

- **📢 섹션 요약 비유**: 공장 기계가 순간순간 스스로 떨림을 보정하더라도, EDAC은 그 떨림 횟수를 센서 대시보드에 모아 보여 줘서 어떤 베어링이 곧 망가질지 미리 알려주는 설비 진단 시스템과 같다.

---

## Ⅲ. 비교 및 연결

EDAC을 제대로 이해하려면, "오류를 고치는 기술"과 "오류를 보여주는 기술"을 구분해야 한다. ECC는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로에서 즉시 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 고치는 회로이고, MCA는 오류 상태를 표준화해 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 남기는 하드웨어 보고 체계다. EDAC은 그 위에서 동작하는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 서브시스템이며, `rasdaemon`은 다시 그 이벤트를 수집·저장하는 사용자 영역 도구다. 즉 EDAC은 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 체계의 <strong>중간 번역기</strong>에 가깝다.

| 개념 | 계층 | 무엇을 하는가 | EDAC과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| :-- | :-- | :-- | :-- |
| [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | 메모리 하드웨어 | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류 교정/탐지 | EDAC의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천 |
| MCA ([Machine Check Architecture](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/717_memory_mca/)) | CPU/플랫폼 | 오류 상태 구조화 | EDAC이 읽는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 기반 |
| EDAC ([Error Detection](/knowledge-base/studynote/02_operating_system/01_overview_architecture/040_error_detection/) and Correction) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) | 오류 위치·횟수·유형 노출 | 운영자 가시성 제공 |
| `rasdaemon` | 사용자 영역 | [RAS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/449_ras/) 이벤트 저장/알림 | EDAC tracepoint 활용 |
| APEI/GHES | [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)-OS 인터페이스 | firmware-first 오류 전달 | 일부 플랫폼에서 EDAC과 병행 |

이 비교에서 중요한 포인트는 EDAC이 <strong>교정 자체를 담당하지 않는다</strong>는 점이다. EDAC이 꺼져 있어도 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 하드웨어는 오류를 고칠 수 있지만, 운영자는 문제를 늦게 알아차리게 된다. 반대로 EDAC [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 풍부하더라도 ECC가 없는 시스템이라면 실제 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 능력은 제한적이다. 따라서 EDAC은 반드시 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/), MCA, [BMC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 운영 모니터링과 함께 봐야 가치가 극대화된다.

- **📢 섹션 요약 비유**: 스프링클러가 불을 끄는 장치라면, EDAC은 어느 층 스프링클러가 몇 번 작동했는지 관리실 화면에 표시하는 설비 모니터다. 화면이 불을 끄는 것은 아니지만, 화면이 없으면 큰 화재를 미리 막기 어렵다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 EDAC은 예지 정비와 장애 격리의 기초 자료로 쓰인다. 예를 들어 특정 DIMM의 CE가 온도가 높아지는 오후 시간대에만 급증한다면, 단순 메모리 불량이 아니라 공조나 랙 배치 문제까지 의심해야 한다. 반대로 동일한 슬롯에서 UE가 반복되면 즉시 노드를 드레인(Drain)하고 DIMM 교체를 예약하는 편이 안전하다.

기술사 답안에서는 단순히 "EDAC으로 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 본다"가 아니라, <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>를 어떻게 의사결정으로 연결하느냐</strong>를 써야 한다. 같은 CE 100건이라도 하루 동안 여러 슬롯에 산발적으로 흩어졌는지, 한 슬롯에 집중됐는지에 따라 의미가 달라진다. 또한 [SMBIOS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/708_nvme_queue_management/) ([System Management BIOS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/708_nvme_queue_management/)) 또는 보드 벤더의 슬롯 매핑 정보가 부정확하면, EDAC 수치만 보고 잘못된 DIMM을 교체하는 운영 실수가 생길 수 있다.

### 운영 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. CE/UE가 특정 슬롯, 채널, [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)에 편중되는가?
2. EDAC [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 [BMC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/) 센서 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 동일한 시간대에 온도·[전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 이상을 보이는가?
3. `rasdaemon` 또는 중앙 모니터링에서 증가 추세를 시계열로 확인했는가?
4. 플랫폼이 EDAC 드라이버 기반인지, APEI/GHES 기반인지 파악했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- "교정 가능 오류니까 무시"라는 식으로 CE 누적을 방치하는 운영
- 슬롯 매핑 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 숫자만 보고 임의의 DIMM을 교체하는 대응
- 하드웨어 이상 신호를 소프트웨어 버그로만 오해하는 사고 조사

- **📢 섹션 요약 비유**: 자동차 계기판의 엔진 경고등이 잠깐 들어왔다고 무조건 차를 세울 필요는 없지만, 같은 경고가 출근길마다 반복되면 정비소 예약을 미루면 안 된다. EDAC 수치도 그런 반복 패턴으로 읽어야 한다.

---

## Ⅴ. 기대효과 및 결론

EDAC의 기대효과는 장애가 터진 뒤 원인을 찾는 시간을 줄이는 것에 그치지 않는다. 더 큰 가치는 작은 정정 오류를 장기 추세로 축적해, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 전에 부품 교체와 워크로드 이동을 계획할 수 있게 만드는 데 있다. 이는 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair) 단축뿐 아니라 [MTTF](/knowledge-base/studynote/04_software_engineering/06_software_architecture/360_mttf/) (Mean Time To Failure) 관리, 유지보수 비용 최적화, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상으로 이어진다.

하지만 EDAC에도 한계는 있다. EDAC은 <strong>관측과 해석</strong>을 제공할 뿐, 물리적으로 손상된 셀을 복구하지는 못한다. 플랫폼 드라이버 품질이 낮거나 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)가 슬롯 정보를 잘못 제공하면 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 신뢰도도 떨어진다. 앞으로는 EDAC [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 단독으로 소비되기보다, [BMC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/) 텔레메트리, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) [RAS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/449_ras/), 클러스터 스케줄러와 결합되어 더 자동화된 예지 정비 체계로 진화할 것이다.

따라서 EDAC은 "오류 정정 기술"이라기보다, <strong>하드웨어가 수행한 정정과 실패를 운영자가 이해하고 행동할 수 있게 번역하는 <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a> 관측 계층</strong>으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 건물의 누전 차단기가 사고를 막는 장치라면, EDAC은 어느 층에서 차단기가 자주 떨어지는지 기록해 전기 배선을 선제적으로 갈게 만드는 관리 일지다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| CE/UE (Corrected Error / Uncorrected Error) | EDAC이 가장 기본적으로 집계하는 오류 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| MCA ([Machine Check Architecture](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/717_memory_mca/)) | EDAC이 읽어 오는 대표적 하드웨어 오류 보고 경로 |
| [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | EDAC [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 출발점이 되는 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) 기법 |
| `rasdaemon` | EDAC 이벤트를 장기 저장·알림으로 연결하는 사용자 영역 도구 |
| [BMC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/) ([Baseboard Management Controller](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/710_bmc/)) | 온도·[전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 텔레메트리와 함께 봐야 정확한 원인 추적이 가능 |

### 📈 관련 키워드 및 발전 흐름도

```text
ECC 메모리 보호
    │
    ▼
MCA 기반 오류 기록
    │
    ▼
EDAC 커널 가시화
    │
    ▼
rasdaemon · 중앙 모니터링
    │
    ▼
예지 정비 · 자동 교체 판단 · 운영 RAS 고도화
```

이 흐름은 "하드웨어 내부 교정"에서 출발해 "운영 자동화"까지 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 관리가 확장되는 과정을 요약한다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 스스로 작은 실수를 고치는 부품이 있는데, EDAC은 그 실수 횟수를 적어 두는 노트예요.
2. 노트에 같은 자리 실수가 자꾸 쌓이면, 어른들은 그 부품을 미리 바꿔서 큰 고장을 막을 수 있어요.
3. 그래서 EDAC은 문제를 직접 고치기보다, 문제를 일찍 알아차리게 도와주는 똑똑한 기록장이라고 보면 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 719 / 803

← **이전**: [717. 메모리 MCA (Machine Check Architecture)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/717_memory_mca/)
**다음**: [719. CPU 클럭 다운클럭킹 (안전 모드)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/719_cpu_downclocking/) →

---
