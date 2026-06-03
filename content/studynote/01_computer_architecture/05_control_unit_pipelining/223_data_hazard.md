+++
title = "223. 데이터 해저드 (Data Hazard)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Hazard)는 파이프라인에서 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 실행 순서는 겹치는데 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 순서는 겹칠 수 없어서, 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 아직 완성되지 않은 값을 너무 일찍 쓰려 할 때 생기는 시간 충돌이다.
> 2. **가치**: 이 문제를 잘 다루면 파이프라인의 평균 사이클당 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수를 높여 실효 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 지키고, 못 다루면 클럭은 빨라도 스톨 (Stall) 때문에 처리량이 급격히 무너진다.
> 3. **판단 포인트**: 산술 연산 간 의존성은 포워딩으로 상당수 숨길 수 있지만, 로드-유즈 (Load-Use)처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 늦게 도착하는 경우는 스톨, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 스케줄링, [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)의 조합으로 다뤄야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 파이프라인 안에서 앞선 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 결과가 아직 확정되지 않았는데, 뒤따르는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 그 값을 읽거나 덮어쓰려 할 때 발생하는 의존성 기반 충돌이다. 단일 사이클 구조에서는 한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 끝난 뒤 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 시작되므로 이런 문제가 잘 드러나지 않지만, 파이프라인은 여러 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 겹쳐 실행하므로 "계산 완료 시점"과 "사용 시점"이 어긋나기 시작한다.

문제의 핵심은 파이프라인이 빠르다는 사실 자체가 아니라, <strong>논리적 선후관계가 물리적 동시성에 의해 깨질 수 있다</strong>는 점이다. 예를 들어 `ADD R1, R2, R3`의 결과가 아직 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 파일에 기록되지 않았는데 바로 다음 `SUB R4, R1, R5`가 R1을 읽으려 하면, 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 최신 값이 아니라 과거 값을 보게 된다. 따라서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하의 원인이기 전에 먼저 <strong>정답을 망가뜨릴 수 있는 <a href="/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a> 문제</strong>다.

이 때문에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 파이프라인 설계에서 반드시 제어 유닛과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)패스가 함께 처리해야 하는 주제가 된다. 제어 유닛은 의존성을 감지해 멈출지, 우회할지, 다른 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 먼저 실행할지 결정하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)패스는 그 결정을 실제 배선과 [멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/)로 구현한다.

- **📢 섹션 요약 비유**: 앞사람이 계산기를 두드려 최종 숫자를 말하기도 전에, 뒷사람이 그 숫자를 받아 적어야 하는 회의와 같다. 숫자가 아직 안 나왔는데 먼저 적으면 틀리고, 기다리기만 하면 회의가 느려진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 보통 5단 파이프라인인 IF ([Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Fetch), ID ([Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Decode), EX (Execute), MEM (Memory Access), WB ([Write Back](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/))에서 설명한다. 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 보통 ID 단계에서 소스 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 읽고 EX 단계에서 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) 연산을 수행하는데, 앞 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 결과는 EX 또는 MEM 이후에야 준비된다. 즉 "필요한 시점"이 "완성 시점"보다 빠르면 해저드가 발생한다.

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존성 유형

| 유형 | 의미 | 발생 조건 | 5단 순차 파이프라인에서의 성격 |
| :--- | :--- | :--- | :--- |
| [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) ([Read After Write](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) | 앞 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 쓴 값을 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 읽음 | 읽기 시점이 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다 이름 | 가장 대표적인 진성 해저드 |
| [WAR](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/) ([Write After Read](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/)) | 앞 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 읽기 전에 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 먼저 씀 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시점이 읽기보다 이름 | 순차 완료 구조에서는 거의 숨겨짐 |
| [WAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) ([Write After Write](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/)) | 두 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 같은 목적지에 씀 | 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 먼저 끝남 | [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)에서 중요해짐 |

5단 순차 파이프라인에서는 실제로 가장 빈번하게 문제 되는 것이 RAW다. [WAR](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/) ([Write After Read](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/))와 [WAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) ([Write After Write](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/))는 대부분의 단순 파이프라인에서는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 순서대로 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 읽고 순서대로 기록하기 때문에 눈에 잘 띄지 않는다. 하지만 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)이나 다중 실행 유닛이 들어오면 이 두 유형도 즉시 현실 문제가 된다.

아래 그림은 RAW가 왜 생기는지, 그리고 왜 단순히 "[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 순서가 맞다"만으로는 충분하지 않은지를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RAW 데이터 해저드의 시간 충돌</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Cycle 1 2 3 4 5 6</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">I1: ADD IF ▶ ID ▶ EX ▶ MEM ──▶ WB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">I2: SUB IF ▶ ID ▶ EX ▶ MEM ──▶ WB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">R1 읽음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">R1 기록</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">충돌: I2는 Cycle 3에 R1이 필요하지만, I1의 최신 R1은 Cycle 5에 기록된다.</div></div>
</div>
</div>



이 간극을 메우기 위해 하드웨어는 두 가지 기본 수단을 사용한다. 첫째, 해저드 탐지 유닛 (Hazard [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) Unit)이 소스/목적지 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 번호를 비교해 충돌을 찾는다. 둘째, 포워딩 유닛 (Forwarding Unit)이 EX/MEM 또는 MEM/WB 파이프라인 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)의 값을 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 입력 [멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/) ([Multiplexer](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/), [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/))로 직접 보내거나, 그조차 안 되면 스톨을 발생시킨다.

- **📢 섹션 요약 비유**: 택배 상자가 창고 선반에 정식 등록되기 전에도 이미 배송 기사 손에는 들려 있다. 다음 사람이 그 물건이 필요하면 선반에서 꺼내기보다 기사 손에서 바로 받아야 빨라진다.

---

## Ⅲ. 비교 및 연결

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드를 제대로 이해하려면 "무조건 멈춤"과 "가능한 한 우회"를 구분해야 한다. 모든 의존성이 같은 난이도를 갖는 것은 아니며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 언제 만들어지는지에 따라 대응 전략이 달라진다.

| 상황 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점 | 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 필요 시점 | 대표 대응 | 결과 |
| :--- | :--- | :--- | :--- | :--- |
| 산술 → 산술 | EX 종료 직후 | 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) EX 시작 | 포워딩 (Forwarding) | 대개 무정지 |
| 산술 → 분기 비교 | EX 종료 직후 | 분기 비교 시점 | 포워딩 + [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) 입력 우회 | 짧은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 또는 무정지 |
| 로드 → 산술 | MEM 종료 직후 | 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) EX 시작 | 포워딩 + 1사이클 스톨 | 대표적 Load-Use |
| 긴 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 연산 → 후속 연산 | 실행 유닛 완료 시점 가변 | 후속 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) EX 시작 | 스코어보드, 예약 스테이션 | 동적 대기 |

특히 로드-유즈 해저드가 중요한 이유는, 메모리에서 읽은 값은 EX가 아니라 MEM 단계가 끝나야 비로소 준비되기 때문이다. 즉 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 EX에 진입하는 순간까지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 아직 물리적으로 존재하지 않을 수 있어, 포워딩이 있어도 미래의 값을 가져올 수는 없다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">포워딩 가능 구간과 불가능 구간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">산술 결과: EX 완료 ▶ 다음 EX로 우회 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">로드 결과: MEM 완료 ▶ 다음 EX로 우회</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Cycle 1 2 3 4 5 6</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LW IF ▶ ID ▶ EX ▶ MEM ──▶ WB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ADD IF ▶ ID ▶ Stall ▶ EX ▶ MEM</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이유: LW 데이터는 Cycle 4 끝에 생기므로, ADD는 Cycle 4 EX에 바로 못 쓴다.</div></div>
</div>
</div>



이 지점에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 다른 파이프라인 주제와 자연스럽게 연결된다. 구조적 해저드는 자원이 부족해서 생기고, 제어 해저드는 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 주소가 불확실해서 생기지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 **정답이 아직 완성되지 않았기 때문에** 생긴다. 또한 225번 [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/), 226번 [WAR](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/), 227번 [WAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) 문서는 각각의 의존성을 더 세밀하게 다루고, 228번 [데이터 포워딩](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) 문서는 그중 RAW를 줄이는 대표 기법을 독립적으로 설명한다.

- **📢 섹션 요약 비유**: 요리가 이미 다 된 음식은 주방에서 바로 옆 테이블로 전달할 수 있지만, 아직 냄비에서 끓는 중인 국은 아무리 급해도 완성되기 전에는 건네줄 수 없다. 모든 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 같은 종류의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 설계에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드를 "없애는" 것보다 "어떤 비용으로 얼마나 숨길지"를 판단해야 한다. 포워딩 경로를 많이 넣을수록 스톨은 줄어들지만, 배선이 늘고 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 입력의 [멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/)가 커져 임계 경로 (Critical Path)가 길어진다. 즉 해저드를 줄이려던 회로가 오히려 최대 클럭 주파수를 떨어뜨릴 수 있다.

컴파일러도 중요한 역할을 한다. 정적 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 스케줄링은 로드 다음에 바로 의존 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 배치하지 않고, 독립적인 산술이나 주소 계산을 사이에 끼워 넣어 하드웨어가 멈춰야 할 자리를 유효한 일로 채운다. 임베디드 프로세서처럼 하드웨어가 단순한 환경일수록 이 기법의 체감 효과가 크다.

고성능 프로세서에서는 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution, OoO)과 [레지스터 리네이밍](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ([Register Renaming](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/))이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드 대응을 한 단계 더 밀어 올린다. OoO는 의존성 없는 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 먼저 실행해 파이프라인 공회전을 줄이고, [레지스터 리네이밍](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/)은 WAR와 WAW처럼 이름 충돌로 보이는 가짜 의존성을 물리 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 분리로 제거한다.

### 설계 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) 해저드의 대부분을 포워딩으로 가릴 수 있는가?
2. Load-Use 패턴이 많은 코드라면 컴파일러 스케줄링이나 프리패치가 충분한가?
3. 포워딩 [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/) 증가로 임계 경로가 악화되지 않는가?
4. [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) 구조라면 [WAR](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/)/WAW를 리네이밍으로 분리했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 파이프라인은 깊게 만들었지만 포워딩 경로를 최소화해 스톨이 폭증하는 설계
- 로드 직후 즉시 사용 패턴이 많은 코드를 아무런 재배치 없이 그대로 두는 컴파일러/핸드코드
- 가짜 의존성까지 모두 진짜 병목처럼 취급해 실행 기회를 버리는 단순 스코어보드 설계

- **📢 섹션 요약 비유**: 도로 정체를 줄이려면 우회도로를 만들고, 출근 시간을 분산하고, 막힌 차선은 건너뛰어 다른 차부터 보내야 한다. 하나의 방법만으로는 도시 전체 흐름이 좋아지지 않는다.

---

## Ⅴ. 기대효과 및 결론

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드를 제대로 다루면 파이프라인은 단순히 "겹쳐 실행하는 구조"를 넘어, 의존성과 비의존성을 구별해 효율적으로 흘려보내는 구조가 된다. 그 결과 평균 사이클당 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수가 개선되고, 같은 주파수에서도 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 크게 벌어진다.

다만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 완전히 사라지지 않는다. 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 여전히 크고, 긴 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 연산이나 캐시 미스는 새로운 형태의 대기열을 만든다. 그래서 현대 아키텍처는 포워딩 하나에 의존하지 않고, 리네이밍·OoO·메모리 계층 최적화까지 결합해 해저드를 여러 층에서 흡수한다.

결국 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 "파이프라인의 약점"이면서 동시에 "현대 CPU (Central Processing Unit)를 똑똑하게 만든 원인"으로 기억하는 것이 좋다. 앞선 결과를 기다리는 문제를 얼마나 세련되게 다루느냐가, 단순한 빠른 회로와 진짜 고성능 프로세서를 가르는 기준이 된다.

- **📢 섹션 요약 비유**: 좋은 공장은 작업자가 서로 기다리느라 멈추지 않게 만든다. 누가 무엇을 끝내야 다음 사람이 일할 수 있는지를 잘 설계한 공장이 결국 가장 빨리 많이 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [파이프라인 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/221_pipeline_hazards/) ([Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) Hazard) | 구조적·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·제어 해저드로 나뉘는 상위 개념 |
| [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) ([Read After Write](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드의 가장 대표적인 진성 의존성 |
| [데이터 포워딩](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) ([Data Forwarding](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) / Bypassing) | RAW를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 기록 전에 우회 전달해 줄이는 핵심 기법 |
| [파이프라인 스톨](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/229_pipeline_stall/) ([Pipeline Stall](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/229_pipeline_stall/) / Bubble) | 포워딩으로 해결되지 않을 때 삽입하는 강제 대기 사이클 |
| [레지스터 리네이밍](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ([Register Renaming](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/)) | [WAR](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/)·[WAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) 같은 이름 충돌을 물리 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 분리로 완화 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">명령어 파이프라이닝 (Instruction Pipelining)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파이프라인 해저드 (Pipeline Hazard)</div>
<div class="kb-diagram-note">구조적 해저드 데이터 해저드 제어 해저드</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">RAW / WAR / WAW 의존성 분석</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">포워딩 · 스톨 · 명령어 스케줄링으로 1차 대응</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">비순차 실행 (OoO) · 레지스터 리네이밍으로 동적 확장</div>
</div>
</div>



이 흐름은 단순 파이프라인의 의존성 문제가, 점차 하드웨어 우회와 동적 스케줄링 기술로 확장되는 발전 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 앞 친구가 블록을 다 쌓아야 뒤 친구가 그 위에 다음 블록을 올릴 수 있는데, 뒤 친구가 너무 급하면 탑이 무너져요.
2. 그래서 선생님은 블록이 완성되자마자 바로 건네주거나, 잠깐 기다리게 하거나, 다른 친구 일을 먼저 시켜요.
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 해저드는 "아직 안 만들어진 것을 먼저 쓰려는 서두름"이라고 기억하면 쉬워요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 223 / 803

← **이전**: [222. 구조적 해저드 (Structural Hazard)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/)
**다음**: [224. 제어 해저드 (Control Hazard / Branch Hazard)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/) →

---
