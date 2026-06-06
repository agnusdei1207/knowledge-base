---
title: "Out-of-Order Execution, OoO"
date: "2026-04-20"
tags:
  - "studynote-computer-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비순차 실행 (Out-of-Order Execution, OoO)은 프로그램에 적힌 순서를 잠시 느슨하게 풀어, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 준비된 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)부터 먼저 실행함으로써 파이프라인의 빈 시간을 줄이는 동적 스케줄링 기법이다.
> 2. **가치**: 캐시 미스, 분기 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 긴 곱셈·나눗셈처럼 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간이 제각각인 현실에서 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수준 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 ([Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)-Level Parallelism, ILP)을 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 바꿔 주는 핵심 엔진이다.
> 3. **판단 포인트**: 실행은 비순차로 흩어져도 결과 확정은 반드시 원래 순서대로 해야 정밀 예외와 정확한 상태 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 가능하므로, [레지스터 리네이밍](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/)과 [재주문 버퍼](/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) ([Reorder Buffer](/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB)가 함께 설계되어야 한다.

---

## Ⅰ. 개요 및 필요성

비순차 실행은 <strong>앞선 <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>가 막혀 있어도, 뒤에 있는 독립 <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>를 먼저 실행하는 프로세서 기법</strong>이다. 전통적인 순차 실행 파이프라인에서는 맨 앞의 load 명령 하나가 L2 캐시 ([Level 2 Cache](/studynote/01_computer_architecture/06_memory_hierarchy_cache/261_l2_cache/))나 동적 램 ([DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/), Dynamic Random Access Memory)에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기다리는 동안, 뒤에 있던 정수 연산과 주소 계산까지 함께 멈추기 쉽다. 이 구조는 제어는 단순하지만 실행 유닛 활용률이 낮고, 특히 [수퍼스칼라](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/) ([Superscalar](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/)) 구조처럼 한 사이클에 여러 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 처리할 수 있는 코어에서는 낭비가 더 커진다.

문제가 커진 이유는 연산 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)보다 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 훨씬 커졌기 때문이다. 산술논리연산장치 ([ALU](/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/), [Arithmetic Logic Unit](/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) 덧셈은 보통 1사이클 근처에서 끝나지만, [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 실패는 수십 사이클, 마지막 수준 캐시 미스는 수십~수백 사이클을 유발할 수 있다. 이런 환경에서 "순서를 지킨다"는 원칙만 고집하면 CPU (Central Processing Unit)는 바쁘게 클럭을 소모하면서도 실제 유효 작업은 많이 못 한다.

아래 그림은 왜 OoO가 필요한지 보여준다. 핵심은 <strong>앞의 느린 명령이 전체 흐름을 멈추게 하지 않도록, 준비된 뒤 명령들을 먼저 흘려보내는 것</strong>이다.

```text
+----------------------------------------------------------------------------+
|            순차 실행 vs 비순차 실행: 지연을 대하는 방식의 차이            |
+----------------------------------------------------------------------------+
| 프로그램 순서:   I1(load miss)   I2(add)   I3(mul)   I4(store address)    |
|                                                                            |
| 순차 실행:      I1 대기 -------- 동안 I2, I3, I4도 함께 정지               |
|                                                                            |
| 비순차 실행:    I1 대기 중에도 I2, I3, I4 중 준비된 명령부터 먼저 실행     |
|                 +------------ 파이프라인 빈칸을 뒤 명령으로 메움 ----------+ |
+----------------------------------------------------------------------------+
```

즉 OoO는 "프로그램 의미를 바꾸는 기술"이 아니라 "기다리는 시간을 다른 일로 채우는 기술"이다. 프로그램이 요구한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존성만 지키면, 하드웨어는 내부 실행 순서를 유연하게 바꿔 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 지킨다.

- **📢 섹션 요약 비유**: 엘리베이터를 기다리는 사람이 한 명 있다고 건물 전체 업무가 멈추는 것은 비효율적이다. 비순차 실행은 엘리베이터가 올 때까지 다른 직원들이 처리 가능한 서류부터 먼저 끝내게 하는 사무실 운영 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OoO 코어는 보통 <strong>순차 인출·해독 -> 리네이밍·디스패치 -> 비순차 실행 -> 순차 커밋</strong>의 흐름으로 동작한다. 앞단은 프로그램 순서를 유지해 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 가져오고 해독하지만, 중간 실행 창(window)에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 준비된 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 골라 먼저 내보낸다. 마지막에는 ROB가 결과를 원래 순서대로 확정하여 외부에 보이는 상태를 일관되게 유지한다.

| 구성 요소 | 핵심 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [레지스터 리네이밍](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ([Register Renaming](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/)) | [WAR](/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/) ([Write After Read](/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/)), [WAW](/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) ([Write After Write](/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/)) 같은 가짜 의존성 제거 | 물리 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 수와 매핑 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| [예약역](/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/) ([Reservation Station](/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/), RS) | 실행 대기 중인 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 보관 | 대기열 크기와 선택 로직 복잡도 |
| 실행 유닛 | 준비된 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 실제 수행 | [ALU](/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/), [부동소수점](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 연산장치 (FPU, [Floating Point](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) Unit), 로드/스토어 유닛 균형 |
| 공통 [데이터 버스](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) (Common [Data Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/), CDB) 또는 결과 전달망 | 완료 결과를 대기 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에 방송 | 배선 길이, 전력, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| [재주문 버퍼](/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) ([Reorder Buffer](/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB) | 순차 커밋과 정밀 예외 보장 | 엔트리 수, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도 |

이 구조를 동작 관점에서 보면 아래와 같다.

```text
+----------------------------------------------------------------------------+
|                    OoO 코어의 내부 데이터 흐름과 제어 흐름                |
+----------------------------------------------------------------------------+
| Fetch/Decode --> Rename --> Dispatch --> Reservation Station                 |
|    |              |           |                    |                       |
|    |              |           |                    +- Ready? --> Execute    |
|    |              |           |                    |             |          |
|    |              |           +---------------> ROB <--------------+          |
|    |              |                                    |                    |
|    +-------- 프로그램 순서 유지 ------------------------+                    |
|                                                     Commit                  |
|                                                       |                     |
|                                         아키텍처 상태는 항상 순차 반영      |
+----------------------------------------------------------------------------+
```

핵심 원리는 세 가지다. 첫째, <strong>리네이밍</strong>으로 이름 충돌을 제거해 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 후보를 늘린다. 둘째, <strong>wakeup/<a href="/studynote/05_database/04_transactions_concurrency/520_select/">select</a></strong> 단계에서 피연산자가 준비된 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 골라 실행한다. 셋째, <strong>순차 커밋</strong>으로 예외, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/), 분기 실패가 생겨도 "어디까지가 확정 상태인가"를 명확히 만든다. 이 덕분에 내부는 자유롭게 움직여도 외부에서는 마치 순차 실행한 것처럼 보이는 정밀 예외 (Precise Exception)가 성립한다.

중요한 점은 OoO가 모든 의존성을 없애지는 못한다는 것이다. [RAW](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) ([Read After Write](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/))처럼 실제로 앞 결과가 필요한 진성 의존성은 그대로 남는다. 따라서 OoO의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 결국 "얼마나 많은 독립 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 창 안에 모아 둘 수 있는가"와 "그중 몇 개를 빠르게 골라낼 수 있는가"에 달려 있다.

- **📢 섹션 요약 비유**: 주방에서 주문표는 접수 순서대로 꽂아 두되, 재료가 먼저 준비된 메뉴부터 조리하고 마지막 계산서는 주문 번호대로 발행하는 식당 운영과 같다. 조리 순서는 유연하지만 손님에게 보이는 장부는 절대 흐트러지지 않는다.

---

## Ⅲ. 비교 및 연결

OoO를 제대로 이해하려면 순차 실행, [수퍼스칼라](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/), 정적 스케줄링과의 경계를 함께 봐야 한다. 순차 실행은 하드웨어가 단순하고 전력 효율이 좋지만, 긴 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 하나가 전체 처리량을 크게 떨어뜨린다. 반면 OoO는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 은닉 능력이 뛰어나지만, 검색·선택 회로와 상태 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 구조가 복잡해 전력과 면적 비용이 크다.

| 비교 항목 | 순차 실행 (In-Order) | 비순차 실행 (OoO) |
| :--- | :--- | :--- |
| [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 선택 기준 | 프로그램 순서 우선 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 여부 우선 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 대응 | 앞 명령이 막히면 뒤도 대기 | 독립 명령을 먼저 실행 |
| 하드웨어 복잡도 | 낮음 | 높음 |
| 전력·면적 비용 | 상대적으로 작음 | 상대적으로 큼 |
| 대표 적용 | [마이크로컨트롤러](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/), 효율 코어 | 고성능 데스크톱, 서버, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 코어 |

또한 OoO는 단독 기술이 아니라 여러 개념의 결합점이다. <strong><a href="/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/">수퍼스칼라</a></strong>가 여러 실행 차선을 제공하면, OoO는 그 차선을 빈칸 없이 채우는 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 역할을 한다. <strong><a href="/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/">레지스터 리네이밍</a></strong>은 가짜 의존성을 걷어내고, <strong><a href="/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/">예약역</a></strong>은 실행 대기실을 만들며, <strong>ROB</strong>는 순서를 다시 복원한다. <strong>토마술로 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> (Tomasulo's <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">Algorithm</a>)</strong>은 이런 동적 스케줄링의 고전적 원형이다.

정적 스케줄링 계열인 [VLIW](/studynote/01_computer_architecture/05_control_unit_pipelining/243_vliw/) (Very Long [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/))나 [EPIC](/studynote/01_computer_architecture/05_control_unit_pipelining/244_epic/) (Explicitly Parallel [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Computing)과의 차이도 중요하다. VLIW는 컴파일러가 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 배치를 미리 결정하지만, OoO는 실행 시점의 캐시 미스, 분기 결과, 실행 유닛 점유 상태를 보고 하드웨어가 실시간으로 판단한다. 즉 VLIW는 "미리 짠 계획표"에 가깝고, OoO는 "현장 상황을 보며 재배치하는 관리자"에 가깝다.

- **📢 섹션 요약 비유**: 순차 실행이 번호표 순서만 지키는 은행이라면, 비순차 실행은 업무 종류와 창구 상태를 보고 빨리 끝날 손님을 먼저 처리하는 스마트 창구다. 대신 이런 은행은 질서 유지를 위한 전산 시스템이 훨씬 정교해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 OoO는 "무조건 좋은 고성능 기능"이 아니라 <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 목표와 전력 예산이 허용할 때 채택하는 비싼 구조</strong>다. 서버 CPU나 노트북용 고성능 코어는 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 실패, 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 긴 [부동소수점](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 연산을 최대한 숨겨야 하므로 OoO가 사실상 필수다. 반대로 실시간 제어기나 초저전력 임베디드 코어는 예측 가능성, 회로 단순성, 발열이 더 중요해 순차 실행을 선택하는 경우가 많다.

### 설계 판단 체크포인트

1. **실행 창 크기**: ROB와 RS를 크게 하면 더 많은 독립 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 볼 수 있지만, 비교 회로와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 로직 전력이 빠르게 증가한다.
2. <strong><a href="/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/">분기 예측</a> 품질</strong>: OoO 창이 넓어도 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)이 자주 틀리면 잘못 실행한 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 대량 폐기해야 하므로 이득이 줄어든다.
3. **메모리 서브시스템**: L1 캐시 ([Level 1 Cache](/studynote/01_computer_architecture/06_memory_hierarchy_cache/260_l1_cache/)), Load/Store [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/), 메모리 의존성 예측이 약하면 OoO의 잠재력이 실행 유닛까지 전달되지 못한다.
4. <strong>정밀 예외와 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong>: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/), [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/), 예외 발생 시 어느 시점까지 상태가 확정되었는지 빠르게 복원할 수 있어야 한다.

### 채택과 회피의 기준

- **채택이 유리한 경우**: 데스크톱·서버처럼 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) ([Instructions Per Cycle](/studynote/01_computer_architecture/03_architecture_basics_performance/135_ipc/)) 향상이 중요하고, 워크로드의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 편차가 크며, 칩 면적과 전력 예산이 비교적 넉넉한 경우
- **회피가 유리한 경우**: 배터리 예산이 매우 작거나, 실시간 응답 예측 가능성이 더 중요하거나, 설계 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 비용을 최소화해야 하는 경우

실제 아키텍처에서는 이 절충이 뚜렷하다. Arm big.LITTLE 계열에서도 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 코어는 OoO, 효율 코어는 간결한 순차 실행을 택하는 경우가 많다. 결국 기술사 관점에서 중요한 답은 "OoO는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 은닉 능력을 사는 대신, 전력·면적·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 복잡도를 지불하는 구조"라는 균형 판단이다.

- **📢 섹션 요약 비유**: 비순차 실행은 숙련된 프로젝트 매니저를 두는 것과 같다. 일정이 꼬여도 할 수 있는 일을 먼저 돌려 전체 마감은 앞당기지만, 그만큼 관리 비용과 인건비가 커진다.

---

## Ⅴ. 기대효과 및 결론

OoO의 가장 큰 효과는 <strong>같은 클럭에서도 더 많은 일을 끝내게 만드는 것</strong>이다. 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 실행 유닛 편차를 숨겨 IPC를 끌어올리고, 넓은 [수퍼스칼라](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/) 구조의 활용도를 높이며, 실제 응용프로그램에서 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 개선한다. 특히 브라우저, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 컴파일러처럼 분기와 메모리 접근이 복잡한 워크로드에서 효과가 크다.

하지만 만능은 아니다. 창이 아무리 커도 ILP 자체가 부족하면 더 이상 꺼낼 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 없다. [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 실패가 잦거나 캐시 계층이 약하면 OoO 엔진이 바쁘게 재배치해도 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상은 제한된다. 따라서 OoO는 "순서를 깨서 무조건 빨라지는 기술"이 아니라, <strong>숨길 수 있는 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>과 찾을 수 있는 독립성의 범위 안에서만 빛나는 구조</strong>로 기억해야 한다.

앞으로의 방향도 단순 확장보다 효율 최적화에 가깝다. 더 큰 창만 추구하기보다, 선택 로직 전력 절감, 메모리 의존성 예측 개선, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 코어와 효율 코어의 이기종 조합이 중요해지고 있다. 결론적으로 OoO의 본질은 "프로그램의 의미는 지키되, 하드웨어 내부 일정표는 최대한 유연하게 운영하는 것"이다.

- **📢 섹션 요약 비유**: 공연 준비에서 모든 스태프가 대본 순서만 기다리면 무대 전환이 느리다. 비순차 실행은 조명이 준비되면 조명부터, 소품이 준비되면 소품부터 먼저 움직이게 하되, 관객 앞에서는 공연이 원래 순서대로 자연스럽게 보이게 만드는 무대 감독과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [수퍼스칼라](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/) ([Superscalar](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/)) | 여러 실행 차선을 제공하며, OoO는 그 차선을 실시간으로 채운다. |
| [레지스터 리네이밍](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ([Register Renaming](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/)) | [WAR](/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/), [WAW](/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) 같은 가짜 의존성을 제거해 OoO의 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 후보를 늘린다. |
| [재주문 버퍼](/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) ([Reorder Buffer](/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB) | 비순차로 끝난 결과를 원래 순서대로 커밋해 정밀 예외를 보장한다. |
| [예약역](/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/) ([Reservation Station](/studynote/01_computer_architecture/05_control_unit_pipelining/241_reservation_station/), RS) | 피연산자가 준비될 때까지 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 대기시키고 선택 대상으로 관리한다. |
| 토마술로 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Tomasulo's [Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) | OoO 동적 스케줄링의 대표 구현 원리다. |

### 📈 관련 키워드 및 발전 흐름도

```text
순차 파이프라인
    |
    v
해저드 관리 (RAW, WAR, WAW) · 데이터 포워딩
    |
    v
수퍼스칼라 (Superscalar) · 명령어 발급 폭 (Issue Width)
    |
    v
레지스터 리네이밍 (Register Renaming)
    |
    v
비순차 실행 (Out-of-Order Execution, OoO)
    |
    v
재주문 버퍼 (ROB) · 예약역 (RS) · 토마술로 알고리즘
    |
    v
고성능 멀티코어 · 이기종 코어 · 전력 효율 최적화
```

이 흐름은 단순 파이프라인이 해저드 대응을 넘어, 동적 스케줄링과 상태 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 갖춘 고성능 코어로 발전해 온 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구 네 명이 줄 서 있는데 맨 앞 친구가 준비물을 찾느라 늦어지면, 비순차 실행은 뒤에서 준비된 친구부터 먼저 발표하게 해 줘요.
2. 대신 선생님에게 점수표를 줄 때는 원래 번호 순서대로 다시 정리해서 내요.
3. 그래서 교실은 더 바쁘고 빨라지지만, 기록은 하나도 헷갈리지 않게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 238 / 803

<- **이전**: [237. 명령어 발급 폭 (Issue Width)](/studynote/01_computer_architecture/05_control_unit_pipelining/237_issue_width/)
**다음**: [239. 레지스터 리네이밍 (Register Renaming)](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ->

---
