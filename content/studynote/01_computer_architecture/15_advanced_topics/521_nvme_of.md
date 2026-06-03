---
title: 521. NVMe 오버 패브릭 (NVMe-oF)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[482_nvme|NVMe]] 오버 패브릭 ([[499_nvme_over_fabrics|NVMe-oF]], [[482_nvme|Non-Volatile Memory Express]] over Fabrics)은 로컬 PCIe에 묶여 있던 [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]]) 명령·큐 모델을 네트워크 패브릭 위로 확장해, 원격 플래시를 거의 로컬처럼 쓰게 만드는 스토리지 전송 구조다.
> 2. **가치**: SCSI (Small Computer System Interface) 기반 스토리지보다 번역 오버헤드가 작고 [[430_index_fast_full_scan|병렬]] 큐를 깊게 유지할 수 있어, 수십 μs급 [[015_지연_데이터_관점|지연]]으로 플래시 [[285_pooling_layer|풀링]]·분리형 스토리지·JBOF (Just a Bunch Of Flash)를 실용화한다.
> 3. **판단 포인트**: [[482_nvme|NVMe]]/[[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]])는 최저 [[015_지연_데이터_관점|지연]], [[482_nvme|NVMe]]/[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]])는 도입 용이성, [[482_nvme|NVMe]]/[[696_fibre_channel_protocol|FC]] ([[696_fibre_channel_protocol|Fibre Channel]])는 기존 [[493_san_storage_area_network|SAN]] ([[493_san_storage_area_network|Storage Area Network]]) 재활용에 강하므로, 목표 [[015_지연_데이터_관점|지연]]·CPU (Central Processing Unit) 여유·네트워크 운영 역량을 함께 보고 전송 방식을 골라야 한다.

---

## Ⅰ. 개요 및 필요성

[[482_nvme|NVMe]]-oF는 [[327_ssd|SSD]] ([[327_ssd|Solid State Drive]]) 시대에 맞는 네트워크 스토리지 인터페이스다. 로컬 NVMe는 [[356_pcie|PCIe]] ([[355_pci|Peripheral Component Interconnect]] Express) 위에서 매우 낮은 [[015_지연_데이터_관점|지연]]과 깊은 [[430_index_fast_full_scan|병렬]] 큐를 제공했지만, 그 성능은 "서버 내부에 SSD가 꽂혀 있다"는 물리 조건에 묶여 있었다. 이 때문에 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]에서는 서버마다 남는 플래시 용량이 흩어지고, 컴퓨트와 스토리지를 독립적으로 증설하기 어려웠다.

기존 SAN은 원격 스토리지를 공유하게 해 주었지만, 대부분 SCSI 계열 명령과 오래된 소프트웨어 스택에 기반해 플래시 [[430_index_fast_full_scan|병렬]]성을 충분히 살리지 못했다. SSD는 수많은 큐와 짧은 명령 경로를 원하지만, 디스크 시대 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 상대적으로 얕은 큐와 큰 번역 비용을 남겼다. [[482_nvme|NVMe]]-oF는 바로 이 틈, 즉 "플래시는 빠른데 네트워크 스토리지 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 느리다"는 문제를 메우기 위해 등장했다.

이 그림은 왜 로컬 NVMe만으로는 대규모 자원 운영이 비효율적인지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│      로컬 NVMe는 빠르지만 PCIe 거리 제한 때문에 서버 밖 공유가 어렵다 │
├──────────────────────────────────────────────────────────────────────┤
│ Server A: CPU ─ PCIe ─ NVMe SSD                                      │
│ Server B: CPU ─ PCIe ─ NVMe SSD   → 자원은 서버 단위로 고정           │
│ Server C: CPU ─ PCIe ─ NVMe SSD                                      │
│                                                                      │
│ 결과                                                                   │
│   - 남는 SSD 용량을 다른 서버가 즉시 활용하기 어렵다                 │
│   - 컴퓨트 확장과 스토리지 확장이 함께 묶인다                        │
│   - 장애·운영 도메인도 서버 내부 장치 단위로 갇힌다                  │
│                                                                      │
│ 해법: NVMe 명령 의미는 유지하고, 운반 경로만 Fabric으로 연장          │
└──────────────────────────────────────────────────────────────────────┘
```

핵심은 스토리지를 네트워크화하더라도 NVMe의 [[430_index_fast_full_scan|병렬]] 처리 모델을 버리지 않는 데 있다. 그래서 [[482_nvme|NVMe]]-oF는 "원격 디스크"라기보다, "거리만 멀어진 [[482_nvme|NVMe]] 경로"로 이해하는 편이 정확하다.

- **📢 섹션 요약 비유**: [[482_nvme|NVMe]]-oF는 회사 책상 옆 서랍에만 두던 중요 문서를, 복도 끝 공용 보관실에 옮기되 여전히 내 전용 비밀번호와 서랍 체계를 유지하게 해 주는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[482_nvme|NVMe]]-oF의 핵심은 명령 의미와 운반 수단을 분리하는 것이다. 호스트는 여전히 관리 큐와 I/O 큐를 사용해 명령을 제출하고 완료를 받는다. 달라지는 것은 명령이 [[356_pcie|PCIe]] 링크를 건너는 대신 [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]), 파이버 채널 ([[696_fibre_channel_protocol|Fibre Channel]]), [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]]) 같은 패브릭 전송 위로 캡슐화된다는 점이다.

호스트는 먼저 디스커버리 컨트롤러를 통해 어떤 서브시스템이 있는지 찾고, NQN ([[482_nvme|NVMe]] Qualified Name) 기준으로 연결 대상을 식별한다. 이후 관리 연결을 만들고, 실제 [[001_dikw_pyramid|데이터]] 처리를 위한 I/O 큐 쌍을 여러 개 생성한다. 타깃 서브시스템은 컨트롤러와 [[061_namespace|네임스페이스]]를 노출하며, 명령 완료는 별도의 완료 큐를 통해 비동기적으로 돌아온다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 호스트 이니시에이터 | [[482_nvme|NVMe]] 명령 제출과 큐 관리 | CPU 코어 수와 큐 매핑 최적화 |
| 디스커버리 컨트롤러 | 서브시스템 탐색과 연결 정보 제공 | 대규모 환경에서 자동화 중요 |
| 패브릭 전송 | 캡슐 운반 | [[639_rdma_kernel_bypass|RDMA]]·[[696_fibre_channel_protocol|FC]]·TCP별 [[015_지연_데이터_관점|지연]]/운영성 차이 |
| 타깃 서브시스템 | [[061_namespace|네임스페이스]]와 실제 플래시 제공 | 다중 경로·장애 대응 구조 필요 |
| 완료 경로 | 비동기 완료 반환 | 큐 깊이와 tail [[141_latency|latency]] 관리가 핵심 |

이 그림은 [[482_nvme|NVMe]]-oF가 큐 구조를 유지한 채 원격 플래시로 확장되는 과정을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│        NVMe-oF는 '큐 의미'는 유지하고 '운반 경로'만 바꿔 보낸다       │
├──────────────────────────────────────────────────────────────────────┤
│ Host Server                                                          │
│  App                                                                 │
│   │                                                                  │
│   ▼                                                                  │
│ NVMe Driver ─ Submission Queue ── Capsules ──▶ Fabric Transport      │
│   ▲                                  │                │              │
│   │                                  │                ▼              │
│ Completion Queue ◀───────────────────┘       Target Controller       │
│                                                     │                │
│                                                     ├─ Namespace     │
│                                                     └─ Flash Media   │
│                                                                      │
│ Discovery Controller → NQN 확인 → 연결 생성 → I/O Queue Pair 운영    │
└──────────────────────────────────────────────────────────────────────┘
```

[[639_rdma_kernel_bypass|RDMA]] 계열 전송에서는 [[001_dikw_pyramid|데이터]] 이동을 [[587_nic_offloading|NIC]] (Network Interface Card)가 직접 처리해 CPU 개입을 줄일 수 있고, [[482_nvme|NVMe]]/TCP는 범용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 위에서 더 손쉽게 배치할 수 있다. 즉 [[482_nvme|NVMe]]-oF는 하나의 제품이 아니라, 같은 [[482_nvme|NVMe]] 의미를 여러 패브릭 위에 얹는 공통 아키텍처다.

- **📢 섹션 요약 비유**: [[482_nvme|NVMe]]-oF는 같은 [[561_container_based_deployment|컨테이너]] 규격을 트럭·기차·배에 공통으로 싣는 물류 시스템과 같다. 상자는 그대로 두고 운송 수단만 바꿔 멀리 보내는 구조다.

---

## Ⅲ. 비교 및 연결

[[482_nvme|NVMe]]-oF를 이해할 때 가장 중요한 경계는 "원격이어도 [[482_nvme|NVMe]] 의미를 유지한다"는 점이다. [[698_iscsi|iSCSI]] (Internet Small Computer Systems Interface)는 SCSI 명령을 전송 제어 [[295_protocol_field_tcp_udp_icmp|프로토콜]]/인터넷 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP)에 실어 보내는 구조라 디스크 시대의 추상화를 그대로 안고 가지만, [[482_nvme|NVMe]]-oF는 애초에 [[327_ssd|SSD]] [[430_index_fast_full_scan|병렬]]성을 전제로 설계된 [[482_nvme|NVMe]] 큐 모델을 그대로 원격화한다. 그래서 단순히 "더 빠른 [[493_san_storage_area_network|SAN]]"이 아니라, 스토리지 소프트웨어 스택의 세대 교체에 가깝다.

전송 바인딩을 비교하면 선택 기준이 더 명확해진다.

| 전송 방식 | 강점 | 약점 | 잘 맞는 환경 |
| :--- | :--- | :--- | :--- |
| [[482_nvme|NVMe]]/[[639_rdma_kernel_bypass|RDMA]] | 가장 낮은 [[015_지연_데이터_관점|지연]], 낮은 CPU 오버헤드 | [[639_rdma_kernel_bypass|RDMA]] 패브릭 운영 난도 | [[231_ai_turing_test|인공지능]]/고성능 컴퓨팅, JBOF, 고성능 DB |
| [[482_nvme|NVMe]]/[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] | 범용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 활용, 도입 쉬움 | CPU 부담과 tail [[141_latency|latency]] 증가 | 일반 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]], 점진적 전환 |
| [[482_nvme|NVMe]]/[[696_fibre_channel_protocol|FC]] | 기존 [[696_fibre_channel_protocol|FC]] [[493_san_storage_area_network|SAN]] 재활용, 예측 가능한 운영 | [[696_fibre_channel_protocol|FC]] 인프라 비용과 유연성 한계 | 엔터프라이즈 [[493_san_storage_area_network|SAN]] |

로컬 NVMe와 비교하면 [[482_nvme|NVMe]]-oF는 네트워크 [[015_지연_데이터_관점|지연]]과 장애 도메인을 새로 안는다. 대신 서버와 플래시의 결합을 풀어 자원 활용률을 크게 높일 수 있다. 즉 경계는 "로컬이냐 원격이냐"보다, **원격화로 얻는 유연성이 추가 [[015_지연_데이터_관점|지연]]과 복잡도를 상쇄하는가**에 있다.

또한 [[482_nvme|NVMe]]-oF는 JBOF, [[672_spdk|SPDK]] (Storage [[282_performance_tactics|Performance]] Development Kit), 소프트웨어 정의 스토리지와 자연스럽게 연결된다. JBOF는 플래시 밀도를 높이고, 소프트웨어 스택은 어떤 서버에 어떤 [[061_namespace|네임스페이스]]를 붙일지 동적으로 결정함으로써 진짜 분리형 스토리지를 완성한다.

- **📢 섹션 요약 비유**: iSCSI가 구형 화물 엘리베이터라면, [[482_nvme|NVMe]]-oF는 [[561_container_based_deployment|컨테이너]] 전용 자동 물류 라인에 가깝다. 멀리 보내는 일은 같아도, 한 번에 처리하는 양과 방식이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "원격 스토리지를 얼마나 로컬에 가깝게 느끼게 할 것인가"가 핵심 판단이다. [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]]) 서버가 체크포인트나 학습 [[001_dikw_pyramid|데이터]]셋을 빠르게 공유해야 하는 [[231_ai_turing_test|인공지능]] 클러스터라면 [[482_nvme|NVMe]]/RDMA가 유리하다. 반대로 이미 25/100기가비트 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]이 넓게 깔려 있고 운영 단순성이 더 중요하다면 [[482_nvme|NVMe]]/TCP가 현실적인 선택이 된다. 기존 [[696_fibre_channel_protocol|FC]] SAN을 오래 운영한 금융·제조 환경은 [[482_nvme|NVMe]]/FC로 단계적 전환하는 경우가 많다.

기술사 답안에서는 단순 장점보다 선택 조건을 써야 깊이가 산다. 예를 들어 고성능 워크로드라도 네트워크가 과도하게 오버서브스크립션돼 있거나 tail [[141_latency|latency]] 관리가 약하면, 원격 NVMe는 기대만큼 빠르지 않다. 또한 다중 경로, 컨트롤러 장애 전환, [[061_namespace|네임스페이스]] 격리까지 함께 설계해야 운영 단계에서 "빠르지만 불안정한 스토리지"가 되지 않는다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. 애플리케이션의 허용 [[015_지연_데이터_관점|지연]] 예산이 수십 μs 수준인지, 수백 μs도 괜찮은지 구분했는가?
2. 패브릭 혼잡 제어와 다중 경로 구성이 스토리지 tail latency를 감당할 수준인가?
3. [[482_nvme|NVMe]]/TCP라면 CPU 여유와 [[448_polling_programmed_io|폴링]] 전략을, [[482_nvme|NVMe]]/RDMA라면 [[639_rdma_kernel_bypass|RDMA]] 운영 역량을 확보했는가?
4. 원격 스토리지 장애가 단일 애플리케이션 장애로 끝나는지, 랙 전체 장애로 번지는지 실패 도메인을 분리했는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 로컬 NVMe와 동일한 [[015_지연_데이터_관점|지연]]을 아무 조건 없이 기대하는 설계
- 손실 많은 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 위에 [[482_nvme|NVMe]]/RDMA를 얹고도 안정적 저지연을 기대하는 판단
- [[555_backup_and_restore_strategy|백업]]·대용량 배치 트래픽과 [[015_지연_데이터_관점|지연]] 민감한 [[499_nvme_over_fabrics|NVMe-oF]] 트래픽을 같은 클래스에 섞는 운영

- **📢 섹션 요약 비유**: [[499_nvme_over_fabrics|NVMe-oF]] 도입은 냉동창고를 외부 물류센터로 옮기는 일과 같다. 창고를 크게 쓰는 이득은 크지만, 도로와 배송 체계를 제대로 설계하지 않으면 오히려 재고 회전이 늦어진다.

---

## Ⅴ. 기대효과 및 결론

[[482_nvme|NVMe]]-oF가 주는 가장 큰 효과는 플래시 자원을 서버 내부 부품이 아니라 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 공용 자산으로 바꾼다는 점이다. 이로 인해 스토리지 활용률이 높아지고, 컴퓨트와 용량을 독립적으로 증설할 수 있으며, 특정 애플리케이션에 고성능 플래시를 순간적으로 더 많이 붙이는 것도 쉬워진다. 즉 "빠른 [[327_ssd|SSD]]"를 넘어 "유연한 플래시 인프라"를 만드는 기술이다.

하지만 한계도 분명하다. 아무리 최적화해도 네트워크는 추가 홉과 혼잡 가능성을 가져오며, 운영 난도 역시 로컬 SSD보다 높다. 또한 [[482_nvme|NVMe]]-oF는 메모리 [[194_consistency_database_integrity|일관성]] 기술이 아니므로 [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]])처럼 메모리 확장을 담당하는 기술과 역할이 다르다. 하나는 블록 스토리지의 원격화이고, 다른 하나는 메모리 의미의 확장이다.

결론적으로 [[482_nvme|NVMe]]-oF는 "원격 스토리지의 성능을 올리는 기술"이라기보다, **플래시를 로컬 부품에서 네트워크 자원으로 승격시키는 아키텍처**로 기억해야 한다. 이 관점이 있어야 전송 방식 선택, 장애 설계, 스토리지 [[285_pooling_layer|풀링]] 전략이 한 줄로 연결된다.

- **📢 섹션 요약 비유**: [[482_nvme|NVMe]]-oF는 개인 금고를 모두 없애고, 건물 전체가 쓰는 [[148_5g_embb_urllc_mmtc|초고속]] 공동 금고실을 만드는 것과 같다. 문까지 가는 복도는 생기지만, 금고를 더 똑똑하게 나눠 쓸 수 있게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[482_nvme|NVMe]] 큐 쌍 ([[058_queue|Queue]] Pair) | [[482_nvme|NVMe]]-oF가 그대로 유지하는 [[430_index_fast_full_scan|병렬]] 명령 모델이다. |
| [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]) | 가장 낮은 [[015_지연_데이터_관점|지연]]의 [[499_nvme_over_fabrics|NVMe-oF]] 전송 바인딩을 제공한다. |
| [[482_nvme|NVMe]]/[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] | 범용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]에서 [[482_nvme|NVMe]]-oF를 확산시키는 실용적 방식이다. |
| JBOF (Just a Bunch Of Flash) | 여러 서버가 공유하는 플래시 풀의 대표 하드웨어 형태다. |
| 다중 경로 ([[500_multipath_io|Multipath]]) | 원격 스토리지의 장애 전환과 가용성을 책임진다. |
| 분리형 스토리지 (Disaggregated Storage) | [[482_nvme|NVMe]]-oF가 실현하는 운영 모델의 핵심 개념이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
SATA / SAS 기반 공유 스토리지
        │
        ▼
로컬 NVMe over PCIe
        │
        ▼
NVMe-oF (RDMA / FC / TCP)
        │
        ▼
JBOF · 플래시 풀링 · 분리형 스토리지
        │
        ▼
컴포저블 인프라 · 랙 단위 자원 조합
```

이 흐름은 "서버 내부 [[327_ssd|SSD]]"에서 출발해, "플래시를 네트워크 자원으로 재배치하는 방향"으로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[482_nvme|NVMe]]-oF는 아주 빠른 장난감 상자를 내 방 안에만 두지 않고, 복도 끝 공용 보관함에 넣어도 바로 꺼내 쓸 수 있게 해 주는 기술이에요.
2. 그래서 친구마다 장난감을 따로 많이 사 두지 않아도, 필요한 친구가 빠르게 같이 쓸 수 있어요.
3. 대신 복도 길이 막히지 않게 잘 정리해야 진짜 빠르게 놀 수 있답니다.
