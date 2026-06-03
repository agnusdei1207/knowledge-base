+++
title = "222. 구조적 해저드 (Structural Hazard)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 구조적 해저드 (Structural Hazard)는 파이프라인의 여러 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 같은 시점에 같은 하드웨어 자원을 요구할 때, 자원 수가 부족해 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 흐름이 멈추는 물리적 충돌이다.
> 2. **가치**: 이 문제를 이해하면 파이프라인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 단순 클럭 속도보다 자원 배치와 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수에 더 크게 좌우된다는 사실을 잡을 수 있다.
> 3. **판단 포인트**: 해결책은 자원 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 확장, 파이프라이닝, 스톨 허용으로 나뉘며, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표와 면적·전력 비용 사이의 균형이 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

구조적 해저드 (Structural Hazard)는 파이프라인 내부의 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들이 서로 논리적으로는 독립적이어도, 동시에 사용할 수 있는 하드웨어가 부족해서 발생하는 자원 충돌이다. 즉 문제의 본질은 "계산 순서가 틀렸다"가 아니라 "동시에 쓸 도구가 하나뿐이다"에 가깝다. [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)나 [제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)가 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에서 비롯된다면, 구조적 해저드는 아키텍처의 물리적 구성에서 직접 발생한다.

이 개념이 중요한 이유는 파이프라인이 본래 노리는 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 향상을 가장 정직하게 깎아먹기 때문이다. 이상적으로는 매 클럭마다 새 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 하나씩 진입해야 하지만, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근이 같은 메모리 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 공유하거나, 긴 곱셈기가 하나뿐이면 특정 클럭에서 누군가는 반드시 기다려야 한다. 결국 구조적 해저드는 <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/">CPI</a> (<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/134_cpi/">Cycles Per Instruction</a>)</strong>를 증가시키며, 하드웨어를 충분히 빠르게 설계했더라도 자원 배치가 좁으면 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 기대치에 못 미친다.

특히 단일 메모리 구조, 단일 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 다중 사이클 연산기, 좁은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 구조에서는 이런 충돌이 자주 나타난다. 그래서 파이프라인을 설계할 때는 단계 수를 늘리는 것만큼이나, 각 단계가 동시에 요구하는 자원의 개수와 충돌 빈도를 함께 계산해야 한다.

- **📢 섹션 요약 비유**: 구조적 해저드는 조리사는 여러 명인데 프라이팬이 하나뿐인 주방과 같다. 레시피는 서로 달라도 같은 팬을 동시에 쓸 수 없어서 결국 누군가는 줄을 서야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

구조적 해저드는 보통 [파이프라인 단계](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/219_pipeline_stages/)가 특정 자원을 같은 클럭에 동시에 요구할 때 드러난다. 고전적인 5단계 파이프라인에서는 IF ([Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Fetch), ID ([Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Decode/[Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) Read), EX (Execute), MEM (Memory Access), WB ([Write Back](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/))가 겹쳐 실행되므로, 각 단계가 필요로 하는 메모리·[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)·연산기 수가 맞지 않으면 충돌이 생긴다.

| 충돌 자원 | 동시에 요구하는 단계 예시 | 왜 충돌하는가 | 대표 대응 |
| :--- | :--- | :--- | :--- |
| 단일 메모리 | IF vs MEM | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 같은 메모리 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 요구 | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 메모리 분리, 캐시 분리 |
| [레지스터 파일 포트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/509_register_file_ports/) | ID vs WB | 읽기와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 같은 클럭에 몰리는데 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수가 부족 | 다중 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시점 분리 |
| [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/))·곱셈기 | EX vs EX | 여러 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 같은 실행 유닛을 동시에 요구 | 연산기 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 파이프라인형 연산기 |
| 공용 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)·메모리 뱅크 | 다수의 로드/스토어 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 경로가 좁아 한 번에 하나만 통과 가능 | [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 폭 확장, 뱅크 분할, 중재기 개선 |

아래 그림은 단일 메모리를 쓸 때 가장 자주 소개되는 구조적 해저드를 보여준다. 한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 MEM 단계에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽고, 뒤의 다른 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 같은 클럭에 IF 단계에서 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 가져오려 한다. 메모리 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 하나라면 둘 중 하나는 대기해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단일 메모리에서 발생하는 구조적 해저드의 시간 충돌</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Cycle 1 2 3 4 5 6</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">I1</div><div class="kb-diagram-node">IF</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ID</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">EX</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">MEM</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">WB</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">I2</div><div class="kb-diagram-node">IF</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ID</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">EX</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">MEM</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">WB</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">I3</div><div class="kb-diagram-node">IF</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ID</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">EX</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">MEM</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">I4</div><div class="kb-diagram-node">IF ?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ I1은 데이터 접근 필요 (MEM)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ I4는 명령어 인출 필요 (IF)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결과: 메모리 포트가 1개이면 I4는 Stall, 메모리 포트가 2개면 동시 진행</div></div>
</div>
</div>



이 문제를 수식으로 보면, 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 `실효 CPI = 이상적 CPI + 구조적 스톨 빈도`로 표현할 수 있다. 즉 구조적 해저드가 잦을수록 클럭 주파수가 높아도 체감 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 줄어든다. 그래서 현대 프로세서는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 캐시와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시를 분리하고, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 여러 읽기 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 두며, 자주 쓰는 실행 유닛을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 배치해 충돌을 줄인다.

- **📢 섹션 요약 비유**: 구조적 해저드는 톨게이트 차로가 하나뿐인 고속도로와 같다. 차가 빠르더라도 차로가 좁으면 결국 병목은 요금소에서 생긴다.

---

## Ⅲ. 비교 및 연결

구조적 해저드는 다른 해저드와 비교해야 경계가 선명해진다. 구조적 해저드는 **자원 부족**, [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)는 <strong>값의 선후 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong>, [제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)는 <strong>다음에 갈 경로의 불확실성</strong>이 원인이다. 따라서 구조적 해저드는 주로 하드웨어 자원 배치로 해결되고, [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)는 포워딩과 스케줄링, [제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)는 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)과 플러시 제어가 중심이 된다.

| 구분 | 구조적 해저드 | [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) | [제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/) |
| :--- | :--- | :--- | :--- |
| 원인 | 자원 수·[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수 부족 | 생산 전 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 소비 | 분기 결과 미확정 |
| 대표 사례 | IF와 MEM의 메모리 충돌 | [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) ([Read After Write](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) | Branch misprediction |
| 핵심 해결 | 자원 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·분리·중재 | 포워딩·스톨·리네이밍 | [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)·[BTB](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/234_btb/)·[지연 분기](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/230_delayed_branch/) |
| 설계 초점 | 면적·전력 vs [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로 타이밍 | 예측 정확도와 패널티 |

메모리 구조 관점에서는 폰 노이만 구조 ([Von Neumann Architecture](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/124_von_neumann/))와 하버드 구조 ([Harvard Architecture](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/126_harvard_architecture/))의 차이가 대표적이다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 같은 메모리 경로로 다루는 폰 노이만 구조는 단순하지만 IF와 MEM 충돌이 일어나기 쉽다. 반면 하버드 구조나 현대의 분리된 L1 캐시 ([Level 1 Cache](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/260_l1_cache/))는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 경로와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로를 나눠 구조적 해저드를 원천적으로 줄인다.

또한 구조적 해저드는 슈퍼스칼라 ([Superscalar](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/))와 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution)으로 갈수록 더 중요해진다. 한 클럭에 여러 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 동시에 발행하면, 같은 ALU나 로드/스토어 유닛을 두고 경쟁이 커지기 때문이다. 즉 고성능화는 해저드를 없애는 마법이 아니라, 더 많은 자원을 투입하고 더 정교한 중재 정책을 요구하는 방향으로 이어진다.

- **📢 섹션 요약 비유**: 구조적 해저드는 운동장에 공이 모자란 문제이고, [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)는 패스를 아직 못 받은 문제이며, [제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)는 어느 골대로 뛸지 아직 모르는 문제와 같다. 겉보기엔 모두 멈춤이지만, 막히는 이유는 서로 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 구조적 해저드 대응은 "자원을 더 넣을 것인가, 기다림을 감수할 것인가"의 판단이다. 서버용 CPU나 고성능 애플리케이션 프로세서는 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) ([Instructions Per Cycle](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/135_ipc/))를 높이기 위해 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 캐시·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시 분리, 다중 실행 유닛, 다중 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 적극 채택한다. 반대로 저가형 MCU ([Microcontroller](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) Unit)나 초저전력 칩은 면적과 전력을 아끼기 위해 일부 충돌을 허용하고, 필요한 순간에만 스톨하도록 설계한다.

### 설계 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 충돌이 빈번한 자원이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 상의 진짜 병목인가?
2. 자원 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)로 얻는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이득이 면적·전력 증가보다 큰가?
3. [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 수를 늘릴 때 임계 경로 (Critical Path)와 클럭 속도 저하가 생기지 않는가?
4. 스톨을 허용해도 목표 응답시간과 실시간성이 유지되는가?

### 대표 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

- <strong>자원 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a></strong>: [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/), 로드/스토어 유닛, 캐시 경로를 늘려 충돌 자체를 줄인다.
- **자원 분할**: 메모리 뱅킹이나 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분리처럼 경로를 나누어 경쟁을 완화한다.
- **파이프라인화**: 긴 연산기를 여러 단계로 쪼개 동시 처리 수용량을 높인다.
- **중재 허용**: 하드웨어 중재기(arbiter)로 순서를 정하고, 드문 충돌은 스톨로 흡수한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

[파이프라인 단계](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/219_pipeline_stages/) 수만 늘리고 실제 자원 수를 그대로 두는 설계는 대표적인 악수다. 겉으로는 깊은 파이프라인이라 고성능처럼 보이지만, 실전에서는 같은 메모리와 같은 실행 유닛을 두고 더 자주 부딪혀 스톨만 늘어난다. 즉 파이프라인 심화와 자원 확충은 함께 설계되어야 한다.

- **📢 섹션 요약 비유**: [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 직원만 10명으로 늘리고 계산대는 2대만 두면 손님은 빨라지지 않는다. 진짜 병목은 사람 수가 아니라 계산대 수에 있기 때문이다.

---

## Ⅴ. 기대효과 및 결론

구조적 해저드를 잘 다루면 파이프라인은 이상적인 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)에 더 가까워진다. 스톨이 줄어들면서 CPI가 개선되고, 고성능 코어에서는 여러 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 안정적으로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리할 수 있다. 또한 자원 충돌이 줄면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 가능성이 높아져 시스템 튜닝과 병목 분석도 쉬워진다.

다만 해결책은 공짜가 아니다. 자원 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 확장은 칩 면적, 소비전력, 배선 복잡도, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 난이도를 모두 증가시킨다. 특히 다중 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 메모리나 실행 유닛 증설은 단순히 "부품 하나 더 넣기"가 아니라 배선 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 발열, 스케줄링 정책까지 다시 설계해야 하는 문제다.

앞으로의 방향은 무조건적인 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)보다, 자주 충돌하는 자원만 선택적으로 확장하고 나머지는 뱅킹, 동적 스케줄링, 계층형 캐시 구조로 완화하는 쪽에 가깝다. 따라서 구조적 해저드는 "하드웨어가 부족해서 생기는 단순 충돌"로 외우기보다, <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 목표를 위해 어디까지 자원을 투자할지 묻는 아키텍처적 의사결정 문제</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 좋은 경기장은 관중석만 크게 짓지 않는다. 사람들이 몰리는 출입문, 매점, 화장실까지 함께 설계해야 진짜로 붐벼도 잘 돌아간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [파이프라인 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/221_pipeline_hazards/) ([Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) Hazard) | 구조적·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·[제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)를 묶는 상위 개념 |
| 하버드 구조 ([Harvard Architecture](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/126_harvard_architecture/)) | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로를 분리해 IF/MEM 충돌을 줄이는 대표 해법 |
| 다중 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Multi-ported [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) | 같은 클럭에 여러 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 허용해 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 충돌을 완화 |
| 슈퍼스칼라 ([Superscalar](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/)) | 동시 발행 폭이 넓어질수록 구조적 해저드 관리가 더 중요해지는 구조 |
| [파이프라인 스톨](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/229_pipeline_stall/) ([Pipeline Stall](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/229_pipeline_stall/)) | 구조적 해저드를 즉시 해결하지 못할 때 발생하는 직접적 결과 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">단일 실행 경로</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파이프라인 도입</div>
<div class="kb-diagram-tree-item" style="--depth:2">자원 동시 요구 증가</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">구조적 해저드 (Structural Hazard)</div>
<div class="kb-diagram-tree-item" style="--depth:2">자원 복제: ALU · 캐시 · 포트 확장</div>
<div class="kb-diagram-tree-item" style="--depth:2">자원 분리: Harvard Architecture · 메모리 뱅킹</div>
<div class="kb-diagram-tree-item" style="--depth:2">자원 중재: Stall · Arbiter</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">슈퍼스칼라 · 비순차 실행에서의 정교한 자원 스케줄링</div>
</div>
</div>



이 흐름은 파이프라인이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이는 동시에 자원 경쟁을 드러내고, 이후 아키텍처가 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·분리·중재 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 진화해 왔음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구 넷이 같이 그림을 그리고 싶은데 색연필 통이 하나뿐이면, 한 번에 한 명만 쓸 수 있어요.
2. 그래서 다른 친구들은 자기 차례가 올 때까지 잠깐 멈춰 서야 하는데, 그게 구조적 해저드예요.
3. 색연필을 더 준비하거나, 연필 통을 나눠 놓으면 친구들이 덜 기다리고 더 빨리 그림을 끝낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 222 / 803

← **이전**: [221. 파이프라인 해저드 (Pipeline Hazards)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/221_pipeline_hazards/)
**다음**: [223. 데이터 해저드 (Data Hazard)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) →

---
