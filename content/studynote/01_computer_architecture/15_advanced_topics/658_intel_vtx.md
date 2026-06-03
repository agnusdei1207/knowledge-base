+++
title = "658. Intel VT-x"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Intel VT-x (Intel [Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/) Technology for x86)는 x86 아키텍처의 고전적 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 난제를 하드웨어로 푸는 실행 프레임워크다.
> 2. **가치**: VMX ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Extensions), [VMCS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/529_vmcs/) ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Control Structure), EPT (Extended [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tables), VPID (Virtual Processor [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)), VT-d ([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/) Technology for Directed I/O)가 CPU (Central Processing Unit), 메모리, 장치 경로를 나눠 맡으면서 소프트웨어 에뮬레이션 의존도를 크게 낮춘다.
> 3. **판단 포인트**: VT-x는 켜기만 하면 끝나는 기능이 아니라, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·[하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·메모리/장치 가속이 함께 맞아야 네이티브에 가까운 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나온다.

---

## Ⅰ. 개요 및 필요성

Intel VT-x는 Intel이 x86 서버와 개인용 컴퓨터 (Personal Computer, [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))에서 본격적인 [하드웨어 보조](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/527_hardware_assisted_virtualization/) [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)를 가능하게 만든 기술 묶음이다. 배경에는 "민감하지만 자동으로 [trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/) 되지 않는 명령"이라는 x86의 오래된 문제가 있었다. 이 때문에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 바이너리 번역이나 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)에 크게 의존했고, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), OS)를 수정하지 않으면서 높은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 얻기 어려웠다.

VT-x의 핵심 아이디어는 가상 머신 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이 직접 계산할 수 있는 구간과, [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 반드시 개입해야 하는 구간을 하드웨어가 분리해 주는 것이다. 즉 게스트 OS가 대부분의 코드를 실제 CPU 위에서 그대로 실행하되, 위험하거나 민감한 사건만 가상 머신 이탈 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Exit, [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)-Exit)로 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)에게 돌린다. 이렇게 해야 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 확보할 수 있다.

아래 그림은 VT-x가 "전부 에뮬레이션"이 아니라 "필요할 때만 개입"하는 구조임을 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Guest execution under VT-x</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">normal instruction ▶ direct run</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">control-sensitive event ▶ hypervisor path</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">memory access ▶ memory assist</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">device access ▶ device remap</div></div>
</div>
</div>



이 구조 덕분에 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 모든 명령을 해석하지 않아도 된다. 결국 VT-x는 "[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 가능한 하드웨어 질서"를 x86에 추가한 기술이라고 볼 수 있다.

- **📢 섹션 요약 비유**: VT-x는 고속도로 하이패스 차로와 같다. 대부분의 차는 멈추지 않고 지나가고, 확인이 필요한 차만 요금소로 유도한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Intel VT-x는 하나의 기능이 아니라 여러 하드웨어 구성요소의 협업이다. 먼저 VMX ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Extensions)가 실행 문맥을 나누고, 가상 머신 제어 구조체 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Control Structure, [VMCS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/529_vmcs/))가 상태와 가로채기 규칙을 담는다. 여기에 [확장 페이지 테이블](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/661_extended_page_table/) (Extended [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Tables, EPT)이 메모리 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)를 맡고, 가상 프로세서 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) (Virtual Processor [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/), VPID)가 주소 변환 캐시 ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/), [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)) 오염을 줄이며, VT-d ([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/) Technology for Directed I/O)가 장치 접근을 격리한다.

| 구성 요소 | 담당 영역 | 실무에서 중요한 이유 |
| :--- | :--- | :--- |
| VMX | 실행 문맥 분리 | 게스트를 수정 없이 실행할 기반 제공 |
| [VMCS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/529_vmcs/) | 상태 저장과 가로채기 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 어떤 사건이 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)-Exit 되는지 결정 |
| EPT | 메모리 주소 2차 변환 | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 관련 오버헤드 감소 |
| VPID | [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 태그 유지 | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 전환 때 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) flush 비용 절감 |
| VT-d | 입출력 (Input/Output, I/O) 및 장치 직접 할당 | 고성능 네트워크·스토리지·그래픽 처리 장치 ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 지원 |

동작 흐름을 보면 VT-x의 역할이 더 분명해진다. 게스트가 일반 산술 연산이나 대부분의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드를 실행할 때는 CPU가 그대로 처리한다. 반면 제어 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 변경, 특정 명령 실행, 외부 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 주입처럼 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 개입이 필요한 사건은 가상 머신 이탈 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Exit, [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)-Exit)로 바뀌고, [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 처리 후 가상 머신 진입 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Entry, [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)-Entry)로 다시 돌려보낸다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">policy in VMCS</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Guest code</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">direct run or Exit</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">memory reference</div><div class="kb-diagram-cell">device access</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">EPT / TLB</div><div class="kb-diagram-cell">device remap path</div></div>
</div>
</div>



여기서 중요한 트레이드오프는 "가로채기 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)"다. 너무 많이 잡으면 느려지고, 너무 적게 잡으면 격리와 관찰이 약해진다. 따라서 VT-x 설계는 기능 목록 암기가 아니라, 어떤 경로를 하드웨어 fast path로 두고 어떤 경로만 Exit 시킬지 정하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 문제다.

- **📢 섹션 요약 비유**: VT-x는 대형 물류센터의 자동 분류기와 같다. 택배 대부분은 자동 레일로 바로 가고, 문제 짐만 사람이 확인대에서 처리한다.

---

## Ⅲ. 비교 및 연결

VT-x의 장점은 다른 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 방식과 비교할 때 더 분명해진다. 소프트웨어 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 모든 민감 동작을 번역해야 해서 구현이 무겁고, [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)는 게스트 OS 수정이 필요하다. VT-x는 게스트 수정 부담을 줄이면서도 하드웨어가 통제 지점을 제공하므로, 대규모 클라우드 운영에 훨씬 잘 맞는다.

| 항목 | 소프트웨어 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) | [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) | Intel VT-x |
| :--- | :--- | :--- | :--- |
| 게스트 OS 수정 | 불필요 | 필요 | 불필요 |
| 명령 처리 방식 | 바이너리 번역 중심 | 하이퍼콜 중심 | 하드웨어 직접 실행 + 선택적 Exit |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 특성 | 오버헤드 큼 | 효율 높지만 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 제한 | 높은 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)과 낮은 오버헤드 |
| 운영 난이도 | [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 구현 복잡 | 게스트 포팅 부담 | [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)/가속 옵션 조합이 중요 |

[AMD-V](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/659_amd_v/) (AMD [Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))는 같은 세대의 대응 기술이다. 큰 방향은 비슷하지만, Intel이 VMCS와 VMX 중심 설계를 택한 반면 AMD는 VMCB와 [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) 구조를 택했다. 또한 VT-x는 단순히 CPU만이 아니라 EPT, VPID, VT-d와 묶여 이해해야 실제 시스템 그림이 보인다.

이 연결 고리를 이해하면 "VT-x는 CPU 옵션 하나"라는 단순화가 왜 위험한지 알 수 있다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 메모리인지 장치인지 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)인지에 따라 병행 활성화해야 할 보조 기능이 달라지기 때문이다.

- **📢 섹션 요약 비유**: 소프트웨어 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)가 통역사가 모든 대화를 손으로 받아 적는 방식이라면, VT-x는 통역 시스템과 출입 통제가 건물 자체에 내장된 회의장에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 VT-x를 다룰 때 가장 먼저 볼 것은 "정말 하드웨어 경로를 제대로 쓰고 있는가"다. [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)에서 VT-x는 켰지만 EPT나 VT-d가 꺼져 있으면, CPU는 빨라졌는데 메모리나 장치 경로가 계속 소프트웨어 병목으로 남는다. 그래서 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 구축 체크리스트는 보통 VT-x 단독이 아니라 VT-x + EPT + VT-d + [Huge Page](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/) + 최신 마이크로코드 조합으로 구성된다.

대표 시나리오는 두 가지다. 첫째, 데이터베이스나 자바 가상 머신 (Java [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), JVM) 기반 서비스처럼 메모리 민감한 워크로드는 EPT와 [Huge Page](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/) 정렬 여부가 지연시간 꼬리를 크게 바꾼다. 둘째, 고성능 네트워크 함수나 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 워크로드는 VT-d 기반 직접 장치 할당이 큰 이점을 주지만, 대신 [라이브 마이그레이션](/knowledge-base/studynote/02_operating_system/10_security/629_live_migration_pre_copy/) 유연성과 디버깅 편의성은 떨어질 수 있다.

기술사 관점의 판단 문장은 다음처럼 정리할 수 있다.

1. 게스트 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이 최우선이면 VT-x 기반 전가상화를 기본으로 둔다.
2. 메모리 병목이 크면 EPT와 [Huge Page](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/), [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) hit율을 먼저 점검한다.
3. 장치 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 절대적이면 VT-d passthrough를 고려하되 이동성과 운영 복잡도 손실을 받아들인다.
4. 중첩 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 개발 편의성은 높이지만 Exit 경로가 겹치므로 기본값으로 남발하지 않는다.

- **📢 섹션 요약 비유**: VT-x 운영은 좋은 스포츠카 세팅과 같다. 엔진만 켠다고 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나오지 않고, 타이어·서스펜션·브레이크를 함께 맞춰야 진짜 달릴 수 있다.

---

## Ⅴ. 기대효과 및 결론

Intel VT-x는 x86이 클라우드 시대의 표준 서버 플랫폼이 되는 데 결정적 역할을 했다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)를 거의 수정하지 않고도 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)를 실용화했고, CPU 실행·메모리 변환·장치 격리의 경계를 하드웨어로 나눠 대규모 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 밀도를 가능하게 했다. 그래서 VT-x는 단순한 기능이 아니라, 현대 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 기대는 실행 계약서에 가깝다.

한계도 분명하다. [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)-Exit가 완전히 사라지는 것은 아니며, 장치 passthrough는 운영 유연성을 줄일 수 있고, 측면 채널이나 [메모리 암호화](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/) 문제는 다른 계열 기술이 맡아야 한다. 따라서 VT-x는 "[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)를 켜는 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)"보다 "[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 격리의 기본 골조"로 기억하는 편이 정확하다.

- **📢 섹션 요약 비유**: VT-x는 고층 건물의 철골 구조와 같다. 눈에 잘 보이지는 않지만, 그 구조가 튼튼해야 위에 여러 층의 서비스가 안전하게 올라간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| VMX root / non-root | VT-x가 실행 문맥을 나누는 가장 기본 축 |
| [VMCS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/529_vmcs/) | VT-x [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 상태를 담는 핵심 제어 구조 |
| EPT | CPU [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)가 메모리 병목으로 무너지지 않게 받쳐 주는 기술 |
| VPID | 빈번한 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 전환에서 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) flush를 줄이는 보조 장치 |
| VT-d | 장치 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 직접 할당을 위한 I/O 격리 계층 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Popek-Goldberg virtualization challenge</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Binary translation and paravirtualization</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Intel VT-x (VMX + VMCS)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">EPT · VPID · VT-d</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Nested virtualization · device passthrough</div>
</div>
</div>



이 흐름은 "소프트웨어 우회 → 하드웨어 실행 분리 → 메모리/장치 가속 → 운영 고도화"의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. VT-x는 한 컴퓨터 안에 여러 개의 작은 방을 안전하게 만드는 기술이에요.
2. 보통 일은 각 방에서 스스로 하고, 위험한 일만 관리실이 도와줘요.
3. 그래서 여러 컴퓨터가 같이 사는 것처럼 보여도 서로 부딪히지 않고 빠르게 움직일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 659 / 803

← **이전**: [657. 가상화 VMX root 모드](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/657_vmx_root_mode/)
**다음**: [659. AMD-V](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/659_amd_v/) →

---
