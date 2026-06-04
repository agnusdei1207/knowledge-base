+++
title = "210. 실행 사이클 (Execute Cycle)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 실행 사이클 (Execute Cycle)은 해독된 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 실제 하드웨어 동작으로 바꾸어, 산술 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 장치 ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/), [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) 연산·유효 주소 계산·분기 판단 같은 <strong>실제 상태 변화의 출발점</strong>을 만드는 단계다.
> 2. **가치**: 인출과 해독이 준비 작업이라면 실행은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 정합성이 동시에 시험되는 구간으로, [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) ([Data Hazard](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)), 분기 패널티, 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 상당수가 여기서 드러난다.
> 3. **판단 포인트**: 현대 프로세서에서 실행은 단순히 "계산 한 번"이 아니라, 파이프라인의 EX (Execute) 단계·메모리 주소 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·포워딩·비순차적 실행 (Out-of-Order Execution, OoO)의 중심축으로 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

실행 사이클 (Execute Cycle)은 중앙 처리 장치 (Central Processing Unit, CPU)가 이미 해독한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 바탕으로 실제 연산이나 제어 결정을 수행하는 단계다. 즉, "무엇을 하라"는 뜻을 이해한 뒤에, 그 뜻을 전기적 동작으로 옮겨 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값·상태 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)·프로그램 흐름을 바꾸는 구간이 바로 실행이다. 인출 사이클과 [해독 사이클](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/209_decode_cycle/)만으로는 시스템 내부에 아무 결과도 남지 않으므로, 실행이 빠지면 CPU는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 읽고 이해만 하는 기계에 머문다.

이 단계가 중요한 이유는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 성격에 따라 병목이 가장 먼저 현실화되는 지점이기 때문이다. 산술 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 핵심이고, 로드/스토어 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 유효 주소 (Effective Address) 계산이 필요하며, 분기 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 조건 비교와 [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)) 갱신 판단이 필요하다. 결국 실행은 단순한 "중간 단계"가 아니라, 어떤 자원이 언제 바빠지고 어디서 파이프라인이 막히는지를 결정하는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 분기점이다.

또한 실행 결과는 다음 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 운명도 바꾼다. 덧셈 결과가 아직 나오지 않았는데 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 그 값을 필요로 하면 [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)가 생기고, 분기 결과가 늦게 확정되면 잘못 인출한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들을 폐기해야 한다. 그래서 실행 사이클을 이해한다는 것은 계산 원리만이 아니라, 파이프라인 정지, 포워딩, [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 실패 비용까지 함께 이해한다는 뜻이다.

- **📢 섹션 요약 비유**: 실행 사이클은 요리사가 주문서를 읽은 뒤 실제로 칼질하고 불을 켜는 순간과 같다. 주문을 읽는 것만으로는 음식이 나오지 않으며, 주방의 병목도 바로 이 실제 조리 단계에서 드러난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

실행 단계의 핵심은 "[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 종류에 맞는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로를 열고 결과를 만들어 내는 것"이다. 이를 위해 CPU는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에서 읽어 온 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/), 즉치값 ([Immediate](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/)), [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/) ([Control Unit](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/))이 만든 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 결합해 적절한 실행 유닛으로 보낸다. 정수 연산이면 ALU가 동작하고, 메모리 명령이면 ALU가 주소 계산기로 동작하며, 분기 명령이면 [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/)와 덧셈기가 분기 여부와 목표 주소를 산출한다.

| 구성 요소 | 실행 단계에서 하는 일 | 핵심 설계 포인트 |
| :--- | :--- | :--- |
| 산술 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 장치 ([ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) | 덧셈, 뺄셈, AND, OR, 시프트 수행 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 연산 폭, 포워딩 연결 |
| [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) ([Comparator](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/)) | 두 값 비교 후 분기 조건 판단 | 조기 분기 판정 가능 여부 |
| 가산기 (Adder) | 분기 목표 주소, 메모리 유효 주소 계산 | 주소 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 |
| 상태 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) (Status [Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) | [Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/), Carry, Sign 등 결과 특성 반영 | 갱신 시점과 예외 처리 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| 실행 유닛 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 어떤 명령을 어느 유닛에 보낼지 결정 | [구조적 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/) 방지 |

아래 그림은 실행 단계가 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에 따라 서로 다른 세 갈래의 결과를 만든다는 점을 보여준다.

```text
+----------------------------------------------------------------------------+
|                    실행 사이클의 대표 데이터 경로                          |
+----------------------------------------------------------------------------+
| Decode 결과                                                                |
|  |                                                                         |
|  +---> ALU 연산 명령 ------> ALU 계산 ----------------> 결과/플래그 생성       |
|  |                                                                         |
|  +---> Load/Store 명령 --> Base + Offset 계산 ------> 유효 주소 전달           |
|  |                                                                         |
|  +---> Branch 명령 ------> 비교 + 목표 주소 계산 --> PC 갱신 여부 결정         |
|                                                                            |
| 공통 출력: 결과 버스, 포워딩 경로, 다음 단계(EX/MEM/WB)로 전달              |
+----------------------------------------------------------------------------+
```

이 그림의 핵심은 실행이 "하나의 연산기"가 아니라, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 종류에 따라 서로 다른 결정을 내리는 분기점이라는 점이다. 예를 들어 `ADD R1, R2, R3`는 계산 결과를 바로 다음 단계로 넘기지만, `LOAD R1, 8(R2)`는 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽는 것이 아니라 먼저 `R2 + 8`이라는 주소를 계산한다. `BEQ R1, R2, target`은 결과값 대신 비교 결과와 목표 주소를 만들어, 파이프라인의 다음 `PC`가 바뀌어야 하는지를 판단한다.

파이프라인 관점에서 보면 실행 단계의 대표 수식은 `실행 가능 시점 = 피연산자 준비 완료 시점 + 실행 유닛 가용 시점`이다. [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)가 늦게 오거나 같은 실행 유닛을 여러 명령이 동시에 요구하면 스톨 (Stall)이 발생한다. 그래서 현대 CPU는 포워딩 (Forwarding), 다중 실행 유닛, [예약역](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/) ([Reservation Station](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/)) 같은 구조를 통해 실행 단계의 대기 시간을 줄인다.

- **📢 섹션 요약 비유**: 실행 단계는 주방의 조리대와 같다. 같은 주방이라도 어떤 주문은 팬에서 볶고, 어떤 주문은 오븐에 넣고, 어떤 주문은 배달 경로를 다시 정해야 하듯이, 실행도 명령 종류에 따라 완전히 다른 작업대를 연다.

---

## Ⅲ. 비교 및 연결

실행 사이클을 정확히 이해하려면 [해독 사이클](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/209_decode_cycle/)과 메모리/기록 단계의 경계를 함께 봐야 한다. 해독은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 의미를 해석하고 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)를 준비하는 단계이고, 실행은 실제 계산 또는 판단을 수행하는 단계이며, 기록 단계는 그 결과를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)나 메모리에 최종 반영하는 단계다. 즉 실행은 "의미 해석"과 "상태 반영" 사이에 놓인 물리적 계산 중심축이다.

| 비교 항목 | [해독 사이클](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/209_decode_cycle/) (Decode) | 실행 사이클 (Execute) | 기록 단계 ([Write Back](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/)) |
| :--- | :--- | :--- | :--- |
| 핵심 질문 | 무엇을 하라는 명령인가 | 실제로 어떤 계산/판단을 할 것인가 | 결과를 어디에 확정할 것인가 |
| 대표 입력 | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 비트열, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 번호 | [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 값, 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) | 실행 결과 또는 메모리 읽기 값 |
| 대표 출력 | 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/), 즉치값, 소스 값 | [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 결과, 주소, 분기 판정 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 상태 변경 |
| 대표 병목 | [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 복잡도, 해저드 검사 | 유닛 경쟁, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존성, 분기 판정 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 충돌, 커밋 순서 |

단일 사이클 구조와 파이프라인 구조를 비교하면 실행의 의미가 더 분명해진다. 단일 사이클에서는 실행, 메모리 접근, 결과 기록이 사실상 한 클럭 안에 묶여 있어 실행 사이클의 경계가 넓고 모호하다. 반면 5단계 파이프라인에서는 보통 EX 단계가 연산과 주소 계산만 맡고, 실제 메모리 접근은 MEM (Memory Access) 단계, 결과 반영은 WB ([Write Back](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/)) 단계로 분리된다. 이 분리는 클럭을 짧게 만들지만, 그만큼 단계 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달과 해저드 제어가 중요해진다.

또한 실행 단계는 [데이터 포워딩](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/), [구조적 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/), 비순차적 실행과 직접 연결된다. 예를 들어 이전 명령의 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 결과가 아직 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 기록되지 않았더라도, 다음 명령의 실행 입력으로 바로 우회 전달하면 파이프라인 정지를 줄일 수 있다. 반대로 곱셈기처럼 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 긴 유닛이 하나뿐이라면, 여러 명령이 동시에 실행 대기를 하며 [구조적 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/)가 생긴다.

```text
+----------------------------+-----------------------------------------------+
| 단순 순차 실행             | 파이프라인/포워딩 기반 실행                  |
+----------------------------+-----------------------------------------------+
| 결과를 쓴 뒤 다음 명령 진행 | EX 결과를 바로 다음 EX 입력으로 우회 전달    |
| 의존성 만나면 쉽게 정지     | 해저드가 있어도 스톨 없이 이어질 수 있음      |
+----------------------------+-----------------------------------------------+
```

이 차이가 중요한 이유는 현대 CPU [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 상당 부분이 "더 빨리 계산하는 능력"보다 "실행 단계를 덜 멈추게 하는 능력"에서 나오기 때문이다. 따라서 실행 사이클은 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 개념 하나로 끝나는 주제가 아니라, 파이프라인 설계와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화의 교차점으로 봐야 한다.

- **📢 섹션 요약 비유**: 해독·실행·기록은 경기에서 작전 지시, 실제 슛, 점수판 반영의 관계와 같다. 작전이 좋아도 슛이 늦으면 기회를 놓치고, 슛을 했어도 점수판 반영 체계가 꼬이면 경기 운영이 흔들린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무와 시험에서 실행 사이클은 보통 "왜 여기서 파이프라인이 멈추는가"라는 질문으로 나타난다. 예를 들어 로드 명령 뒤에 바로 그 값을 사용하는 명령이 오면, 실행 단계에서는 주소만 계산되었고 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 아직 메모리 단계에서 오지 않았기 때문에 로드-유즈 해저드 (Load-Use Hazard)가 발생한다. 이때 설계자는 1사이클 스톨을 허용할지, 더 공격적인 포워딩을 넣을지, 컴파일러 스케줄링으로 숨길지를 판단해야 한다.

분기 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)도 중요한 판단 포인트다. 실행 단계에서 분기 조건을 판정하면 설계는 단순하지만, 그만큼 뒤에서 이미 인출한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 더 많이 폐기하게 된다. 반대로 분기 판정을 해독 단계 쪽으로 당기면 패널티는 줄지만, 앞단 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)가 무거워져 클럭 주기와 전력이 나빠질 수 있다. 즉 실행 사이클 설계는 언제나 "[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 감소"와 "회로 복잡도 증가" 사이의 절충이다.

### 설계 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 정수 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/), [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 장치 ([Floating Point](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) Unit, FPU), 곱셈기처럼 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 긴 유닛의 개수와 파이프라인화 정도가 workload와 맞는가?
2. 포워딩 경로를 넣었을 때 얻는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이득이 배선 복잡도와 전력 증가를 정당화하는가?
3. 분기 판정을 EX 단계에 둘지, 더 앞 단계로 당길지에 대한 명확한 목표가 있는가?
4. 비순차적 실행 구조라면 실행 완료 순서와 커밋 순서를 분리해 정확한 예외 (Precise Exception)를 보장하는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 실행 유닛 수만 늘리고, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 공급 폭이나 [예약역](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/) 크기는 그대로 두는 불균형 설계
- 로드-유즈 해저드를 무시하고 "포워딩만 있으면 다 해결된다"고 보는 단순화
- 긴 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 연산의 완료 순서를 통제하지 않아 커밋 단계에서 상태 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 깨지는 설계

기술사 답안에서는 실행 사이클을 "ALU가 계산하는 단계"라고만 쓰면 얕다. 더 좋은 설명은, 실행이 주소 계산·조건 판단·포워딩·OoO 스케줄링의 중심이며 여기서 드러나는 해저드를 어떻게 제어할지가 현대 CPU의 핵심 설계 포인트라는 점까지 연결하는 것이다.

- **📢 섹션 요약 비유**: 실행 단계 설계는 도로에 차선을 무작정 늘리는 일이 아니다. [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등, 진입 램프, 우회로까지 같이 설계해야 실제 정체가 줄어들듯, 실행 유닛도 공급·우회·정렬 체계와 함께 봐야 한다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 실행 사이클은 파이프라인의 실효 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 끌어올린다. [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)가 준비되는 즉시 적절한 실행 유닛에 배정되고, 결과가 포워딩을 통해 빠르게 재사용되면 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)당 사이클 수 ([Cycles Per Instruction](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/134_cpi/), [CPI](/knowledge-base/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/))는 낮아지고 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Instructions Per Cycle](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/135_ipc/), [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/))은 올라간다. 특히 분기 판정 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 로드-유즈 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄이면 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 크게 개선된다.

그러나 실행 단계 최적화에는 분명한 한계도 있다. 실행 유닛을 늘릴수록 면적과 전력이 증가하고, 포워딩 경로가 많아질수록 배선과 타이밍 검증이 어려워진다. 또한 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 매우 큰 워크로드에서는 실행 유닛이 많아도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공급 자체가 늦어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상이 제한된다.

앞으로의 실행 단계는 단순 정수 연산 중심에서 더 이질적인 구조로 확장된다. 벡터 실행 유닛, 텐서 가속기, [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 보조 로직, 더 깊은 OoO 스케줄링이 결합되면서 실행의 의미가 "계산기 한 개"에서 "다양한 계산 자원을 조율하는 백엔드 핵심"으로 넓어지고 있다. 따라서 실행 사이클은 "CPU가 실제로 일을 하는 순간"이면서도, 동시에 "현대 마이크로아키텍처의 복잡성이 집중되는 지점"으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: 좋은 실행 단계는 숙련된 주방의 핵심 조리 라인과 같다. 불판만 많이 놓는다고 식당이 빨라지는 것이 아니라, 재료 공급·조리 순서·완성 접시 전달까지 맞아떨어져야 진짜 회전율이 올라간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [해독 사이클](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/209_decode_cycle/) ([Decode Cycle](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/209_decode_cycle/)) | 실행에 필요한 제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)와 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)를 준비하는 바로 앞 단계 |
| [데이터 포워딩](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) ([Data Forwarding](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/)) | 실행 결과를 기록 전 단계에서 바로 다음 실행 입력으로 우회 전달 |
| [데이터 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) ([Data Hazard](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)) | 이전 실행 결과가 아직 확정되지 않았을 때 뒤 명령이 의존하며 발생 |
| [제어 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/) ([Control Hazard](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)) | 실행 단계의 분기 판단이 늦어 인출 경로가 흔들릴 때 발생 |
| 비순차적 실행 (OoO) | 준비된 명령부터 실행 유닛에 보내 실행 자원 활용도를 높이는 구조 |
| 재정렬 버퍼 ([Reorder Buffer](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB) | 실행 완료 순서와 프로그램 순서를 분리하면서 정확한 상태 반영을 보장 |

### 📈 관련 키워드 및 발전 흐름도

```text
명령어 해독 완료
    |
    v
ALU 중심 실행 단계
    |
    v
유효 주소 계산 · 분기 판정 분리
    |
    v
포워딩 · 해저드 제어를 포함한 파이프라인 EX
    |
    v
비순차적 실행 (OoO) · 다중 실행 유닛 스케줄링
    |
    v
벡터/텐서 실행 유닛을 포함한 이종 백엔드
```

이 흐름은 실행 사이클이 단순 계산 단계에서 출발해, 파이프라인 제어와 다중 실행 자원 스케줄링의 중심으로 확장된 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 쪽지를 읽고 나서야 진짜로 더하기를 하거나, 길을 바꾸거나, 물건을 꺼내러 가요.
2. 이처럼 "이제 실제로 행동하는 시간"이 바로 실행 사이클이에요.
3. 똑똑한 컴퓨터는 한 일이 끝나기만 기다리지 않고, 준비된 다른 일부터 먼저 해 보면서 시간을 아낀답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 210 / 803

<- **이전**: [209. 해독 사이클 (Decode Cycle)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/209_decode_cycle/)
**다음**: [211. 간접 사이클 (Indirect Cycle)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/211_indirect_cycle/) ->

---
