+++
title = "351. 버스 중재 (Bus Arbitration)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Arbitration)는 여러 [버스 마스터](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/350_bus_master/)가 하나의 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 동시에 원할 때, <strong>누가 먼저 쓸지 정해 충돌을 제어 가능한 순서로 바꾸는 메커니즘</strong>이다.
> 2. **가치**: 중재가 없으면 CPU (Central Processing Unit), [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) 제어기, 입출력 컨트롤러의 요청이 전기적으로 겹쳐 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손상과 시스템 정지를 부를 수 있다.
> 3. **판단 포인트**: 좋은 중재는 단순히 빠른 승자 선정보다, <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>시간·<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>·공정성·실시간성</strong> 사이에서 시스템 목적에 맞는 균형을 잡는 설계다.

---

## Ⅰ. 개요 및 필요성

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Arbitration)는 여러 장치가 하나의 시스템 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 공유할 때 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사용권을 배분하는 제어 방식이다. 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 본질적으로 한 순간에 한 마스터만 주소, 제어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 주도할 수 있으므로, 경쟁 상황을 질서로 바꾸는 규칙이 반드시 필요하다. 이 규칙이 없으면 두 장치가 동시에 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 구동하면서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 경합 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Contention)이 발생하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 틀어지거나 재시도가 폭증한다.

특히 멀티마스터 구조에서는 이 필요성이 더 커진다. 과거에는 CPU가 거의 유일한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 주도권자였지만, 현대 시스템은 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 제어기, 그래픽 장치, 네트워크 인터페이스가 직접 메모리 전송을 시도한다. 이때 "누가 먼저"를 정하지 않으면 장치 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 높을수록 오히려 전체 시스템은 더 불안정해진다.

중재는 단순한 선착순 문제가 아니다. 긴급한 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 연속 전송이 필요한 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 (Burst) 전송, 오래 기다린 저우선 장치의 [기아 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))를 함께 고려해야 한다. 즉 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 하드웨어 교통정리이면서, 시스템 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 물리 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 수준에 내리는 스케줄러라고 볼 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">공유 버스에서 중재가 필요한 이유</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Master A (CPU) ──</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">공유 시스템 버스</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">Main Memory</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Master C (I/O) ──</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중재 없음 : 동시에 구동 → 충돌/왜곡/재시도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중재 있음 : 한 번에 한 마스터만 점유 → 예측 가능한 전송</div></div>
</div>
</div>



이 그림의 핵심은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 넓은 네트워크가 아니라, 한 시점에 한 주체만 사실상 말할 수 있는 공용 배선이라는 점이다. 그래서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상은 선을 공유하는 방식 자체를 이해하는 데서 시작하고, 그 첫 관문이 바로 중재 설계다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 하나의 칠판을 여러 선생님이 함께 쓰는 상황과 같다. 분필을 먼저 잡을 사람을 정하지 않으면 서로 덧쓰게 되지만, 순서를 정하면 수업은 느려도 내용은 정확히 남는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재의 기본 흐름은 요청, 판정, 점유, 해제의 네 단계로 정리된다. [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 쓰고 싶은 장치는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 요청 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 내고, 중재기 또는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 논리가 승자를 정한 뒤, 선택된 장치에 사용권을 부여한다. 이후 승자는 일정 시간 동안 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 점유하고 전송을 끝낸 뒤 사용권을 반납한다.

대표 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 요청 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Request, BR), [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 승인 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Grant, BG), [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 점유 또는 사용 중 표시 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Busy, BB)로 설명할 수 있다. 이름은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 규격마다 다르지만 의미는 비슷하다. 핵심은 <strong>요청과 실제 점유를 분리</strong>해, 승자만 구동선을 활성화하게 만드는 것이다.

| 단계 | 핵심 동작 | 설계 포인트 |
| :--- | :--- | :--- |
| 요청 | 마스터가 BR [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 사용 의사 전달 | 동시 요청 감지 |
| 판정 | 중재기가 우선순위 비교 | 고정/가변 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 선택 |
| 점유 | 승자에게 BG 부여, [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 사용 | [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 길이, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) |
| 해제 | 전송 완료 후 BB 해제 | 다음 요청 전환 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 |

아래 흐름은 가장 전형적인 중앙 중재 시퀀스를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">버스 중재의 기본 핸드셰이크 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Master 1 BR ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Master 2 BR ▶</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Arbiter</div><div class="kb-diagram-node">요청 수집</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">우선순위 판정</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">BG to Master 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Master 2 BG 수신 → BB 활성 → 데이터 전송</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Others BB=1 동안 대기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Master 2 전송 종료 → BB 해제 → 다음 중재</div></div>
</div>
</div>



이 구조에서 병목은 두 군데에서 생긴다. 첫째, 요청자가 많을수록 판정 회로의 복잡도가 증가한다. 둘째, 승자에게 너무 긴 점유 시간을 주면 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 좋아질 수 있지만 다른 장치의 대기시간이 늘어난다. 따라서 중재는 단일 정답이 아니라 <strong>평균 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>과 최악 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>시간의 교환</strong>이다.

중재 방식은 구조와 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 나눠 생각하면 이해가 쉽다. 구조는 [중앙 집중식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/) ([Centralized Arbitration](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/))와 [분산식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/353_distributed_arbitration/) ([Distributed Arbitration](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/353_distributed_arbitration/))로, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 고정 우선순위 (Fixed Priority), [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/) (Round Robin), 시간 분할 기반 접근으로 나뉜다. 구조가 "누가 판정하느냐"를 다룬다면, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 "무슨 기준으로 판정하느냐"를 다룬다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 공연장 마이크 운영과 같다. 손을 든 사람을 보는 사회자 구조가 먼저 있고, 그다음 VIP부터 시킬지 차례대로 시킬지라는 규칙이 따로 붙는다.

---

## Ⅲ. 비교 및 연결

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재를 제대로 이해하려면 <strong>중재 구조</strong>와 <strong>중재 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>을 분리해서 비교해야 한다. [중앙 집중식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/)는 구현과 관리가 단순해 범용 시스템에 유리하지만, 단일 장애점인 [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure)를 만든다. 반대로 [분산식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/353_distributed_arbitration/)는 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 허용성이 높지만, 모든 노드가 동일한 중재 규칙을 하드웨어 수준에서 공유해야 하므로 복잡도와 비용이 커진다.

| 비교 축 | [중앙 집중식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/) | [분산식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/353_distributed_arbitration/) |
| :--- | :--- | :--- |
| 판정 위치 | 중앙 아비터 1곳 | 각 마스터 내부 또는 공용 규칙 |
| 장점 | 단순함, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경 용이 | [SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 완화, 고신뢰성 |
| 약점 | 아비터 장애에 취약 | 규격 통일과 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 부담 |
| 적합 환경 | 범용 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), 전통적 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) | 차량, 산업, 고신뢰 멀티마스터 |

[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 비교도 중요하다. 고정 우선순위는 긴급 장치에 매우 유리하지만 낮은 우선순위 장치를 굶길 수 있다. [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)은 공정성은 좋지만, 실시간 긴급 트래픽을 즉시 통과시키기 어렵다. 즉 <strong>우선순위는 응답성에 강하고, 순환 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>은 공평성에 강하다</strong>는 경계가 분명하다.

[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 다른 분야와도 이어진다. 운영체제의 CPU 스케줄링처럼 제한된 자원을 누구에게 먼저 줄지 결정한다는 점에서 사고방식이 같다. 또 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 중재, 네트워크 [매체 접근 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/183_mac_media_access_control/), [PCI](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/))에서 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express)로의 진화도 연결된다. 다만 PCIe는 전통적 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)보다 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기반 점대점 구조라, "한 선을 나눠 쓰는 중재"에서 "패킷 스위칭과 [버퍼링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)"으로 문제를 이동시켰다는 차이가 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">공유 버스 시대</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 버스 마스터 증가</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 중재 필요성 확대</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 정책 경쟁</div>
<div class="kb-diagram-tree-item" style="--depth:4">고정 우선순위 : 빠른 긴급 대응</div>
<div class="kb-diagram-tree-item" style="--depth:4">라운드 로빈 : 공평한 순환 보장</div>
</div>
</div>



이 비교에서 기억할 점은 "어느 방식이 더 좋다"가 아니라 "어느 병목과 어느 실패 모드를 감수할 것인가"다. [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 결국 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기술이면서도, 동시에 장애 모델을 설계하는 기술이다.

- **📢 섹션 요약 비유**: 중앙 집중식은 교통경찰 한 명이 사거리를 통제하는 방식이고, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)식은 모든 차가 같은 우선 통행 규칙을 아는 방식이다. 또 고정 우선순위는 구급차 우선이고, [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)은 번호표 순서라고 기억하면 경계가 선명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 "무엇이 더 이론적으로 우아한가"보다 "어떤 트래픽을 절대 늦추면 안 되는가"로 판단한다. 예를 들어 디스크, 네트워크, 그래픽 전송이 동시에 몰리는 시스템에서는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 전송 허용량과 우선순위 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 전체 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 좌우한다. 반면 제어 시스템에서는 평균 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)보다 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 더 중요하다.

### 설계 판단 기준

1. <strong>실시간 제어 중심</strong>이면 고정 우선순위가 유리하다. 브레이크 제어, 센서 샘플링처럼 마감시간이 명확한 경우에는 긴급 장치가 즉시 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 선점해야 한다.
2. <strong>범용 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a> 중심</strong>이면 [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/) 또는 가변 우선순위가 유리하다. 특정 장치가 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 과점하지 못하게 해야 전체 응답성이 좋아진다.
3. <strong>대량 연속 전송</strong>이 많으면 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 길이를 늘려 중재 오버헤드를 줄일 수 있다. 대신 다른 요청의 대기시간 상한을 반드시 계산해야 한다.

### 자주 보는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 장치에 동일 우선순위를 준 채, 실제 긴급도 차이를 무시하는 설계
- 고정 우선순위를 채택해 놓고 [기아 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) 완화 장치가 없는 설계
- [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 전송을 과도하게 허용해 평균 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 높지만 인터랙티브 응답성이 급락하는 설계

예를 들어 오래된 [PCI](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) 기반 시스템에서 고속 네트워크 카드가 긴 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 DMA를 반복하면 CPU의 메모리 접근이 눈에 띄게 늦어질 수 있다. 반대로 차량 제어망에서는 짧더라도 가장 긴급한 프레임이 먼저 지나가야 안전성이 확보된다. 따라서 기술사 관점에서는 <strong>"평균 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>"과 "최악 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>" 중 무엇이 우선인지 먼저 선언하고, 그다음 중재 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>을 택하는 순서</strong>가 중요하다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재 설계는 병원 접수창구 운영과 같다. 응급실이면 중증 환자를 먼저 받아야 하고, 건강검진 센터면 번호표 순서가 더 공정하다. 같은 창구라도 목적이 다르면 좋은 규칙도 달라진다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)의 약점을 통제 가능한 수준으로 바꾼다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 충돌을 방지해 신뢰성을 높이고, 중재 오버헤드를 줄여 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 개선하며, 우선순위 체계를 통해 중요한 작업의 응답시간을 예측 가능하게 만든다. 특히 멀티마스터 시스템에서는 중재가 없으면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상보다 혼잡 확대가 먼저 오기 때문에, 중재는 선택 기능이 아니라 전제 조건이다.

물론 한계도 분명하다. 아무리 좋은 중재 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있어도 물리적으로 한 번에 한 장치만 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 쓸 수 있다는 제약은 남는다. 그래서 컴퓨터 구조는 전통적 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에서 점대점 링크, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 패브릭, 온칩 네트워크인 [NoC](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/367_noc/) ([Network on Chip](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/367_noc/))로 점차 이동해 왔다. 이는 중재가 사라졌다는 뜻이 아니라, <strong>중재의 위치와 대상이 <a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">버스</a> 선로에서 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>·버퍼·패킷 스케줄링으로 옮겨갔다</strong>는 뜻이다.

결론적으로 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 "누가 먼저 쓰는가"를 정하는 작은 회로가 아니다. 그것은 공유 자원 시스템이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 안정성, 공정성을 동시에 유지하기 위해 반드시 갖춰야 하는 하드웨어 수준의 운영 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. 이 개념을 기억할 때는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 이름보다도, <strong>경쟁을 통제된 순서로 바꾸는 설계 철학</strong>을 먼저 떠올리는 것이 정확하다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 좁은 외나무다리를 건널 때 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)수를 두는 일과 같다. 다리가 넓어지면 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)수 역할은 줄어들 수 있지만, 사람들이 몰리는 한 "누가 언제 건널지 정하는 규칙" 자체는 끝까지 사라지지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [버스 마스터](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/350_bus_master/) ([Bus Master](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/350_bus_master/)) | 중재를 요청하는 주체이며 CPU, [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 제어기, 고속 I/O 장치가 여기에 속한다. |
| [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 경합 ([Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) Contention) | 중재가 실패하거나 없을 때 발생하는 직접적인 충돌 상태다. |
| [중앙 집중식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/) ([Centralized Arbitration](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/)) | 단일 아비터가 승자를 판정하는 대표 구조다. |
| [분산식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/353_distributed_arbitration/) ([Distributed Arbitration](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/353_distributed_arbitration/)) | 각 노드가 공통 규칙으로 스스로 승패를 결정하는 구조다. |
| [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 전송 (Burst Transfer) | 중재 오버헤드를 줄이지만 대기시간을 늘릴 수 있어 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 판단과 연결된다. |
| [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express) | 공유 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 한계를 넘어 중재 문제를 스위칭과 패킷 처리로 재배치한 현대 인터커넥트다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 마스터 버스</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">멀티마스터 버스 확장</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">버스 중재 (Bus Arbitration)</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 중앙 집중식 중재 (Centralized Arbitration)</div>
<div class="kb-diagram-note">─▶ 고정 우선순위 (Fixed Priority)</div>
<div class="kb-diagram-note">─▶ 라운드 로빈 (Round Robin)</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 분산식 중재 (Distributed Arbitration)</div>
<div class="kb-diagram-tree-item" style="--depth:7">▶ 고신뢰 실시간 제어 버스</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">PCIe · 스위치 패브릭 · NoC (Network on Chip)</div>
</div>
</div>



이 흐름은 "공유 자원 증가 → 충돌 통제 → [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 세분화 → [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기반 확장"이라는 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 중재는 그네가 하나뿐인 놀이터에서 누가 먼저 탈지 정해 주는 규칙이에요.
2. 이 규칙이 없으면 친구들이 동시에 올라타서 그네도 멈추고 모두가 다칠 수 있어요.
3. 그래서 컴퓨터도 여러 부품이 같이 쓰는 길에서는 먼저 갈 사람을 꼭 정한답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 352 / 803

← **이전**: [350. 버스 마스터 (Bus Master)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/350_bus_master/)
**다음**: [352. 중앙 집중식 중재](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/352_centralized_arbitration/) →

---
