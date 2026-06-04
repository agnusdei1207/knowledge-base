---
title: "221. 파이프라인 해저드 (Pipeline Hazards)"
date: "2026-04-20"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 파이프라인 해저드 ([Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) Hazards)는 여러 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 겹쳐 흘려보내는 순간, 자원 충돌·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존성·분기 불확실성 때문에 이상적인 흐름이 깨지는 병목 현상이다.
> 2. **가치**: 파이프라인의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 단순히 단 수를 늘리는 것으로 결정되지 않고, 해저드 때문에 생기는 스톨(Stall), 버블(Bubble), 플러시(Flush)를 얼마나 줄이느냐에 의해 실제 [CPI](/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/) ([Cycles Per Instruction](/studynote/01_computer_architecture/03_architecture_basics_performance/134_cpi/))가 좌우된다.
> 3. **판단 포인트**: 구조적·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·[제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)는 원인이 서로 다르므로, 자원 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [데이터 포워딩](/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) ([Data Forwarding](/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/)), [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) ([Branch Prediction](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)), 컴파일러 스케줄링을 같은 처방으로 다뤄서는 안 된다.

---

## Ⅰ. 개요 및 필요성

파이프라인 해저드는 [명령어 파이프라이닝](/studynote/01_computer_architecture/05_control_unit_pipelining/218_instruction_pipelining/) ([Instruction Pipelining](/studynote/01_computer_architecture/05_control_unit_pipelining/218_instruction_pipelining/))에서 여러 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 동시에 흐를 때 정상 진행을 방해하는 충돌 조건이다. 이상적으로 5단 파이프라인은 파이프가 채워진 뒤 매 클럭마다 결과를 하나씩 내야 하지만, 실제 프로그램은 서로 독립적이지 않다. 같은 자원을 동시에 요구하기도 하고, 앞선 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 결과를 뒤 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 바로 필요로 하며, 분기문은 다음에 무엇을 가져와야 할지 자체를 흔든다.

이 개념이 중요한 이유는 해저드가 파이프라인의 장점을 직접 깎아 먹기 때문이다. 클럭 주파수가 높아도 해저드가 많으면 유닛이 빈 채로 지나가는 클럭이 늘어나고, 결국 사용자 입장에서는 "빠른 CPU인데 생각보다 안 빠른" 상황이 된다. 따라서 파이프라인 설계의 핵심은 단계를 나누는 것에서 끝나지 않고, 그 단계들이 서로 부딪히지 않게 흐름을 통제하는 데 있다.

```text
+----------------------------------------------------------------------------+
|        이상적 파이프라인과 실제 파이프라인의 차이: 막힘이 성능을 결정        |
+------------------------------------------+---------------------------------+
| 이상적 흐름                              | 해저드가 있는 흐름              |
| I1  IF->ID->EX->MEM->WB                     | I1  IF->ID->EX->MEM->WB             |
| I2     IF->ID->EX->MEM->WB                  | I2     IF->ID->Stall->EX->MEM->WB    |
| I3        IF->ID->EX->MEM->WB               | I3        IF->ID->FLUSH           |
| I4           IF->ID->EX->MEM->WB            | I4              IF 재시작       |
+------------------------------------------+---------------------------------+
| 같은 5단 구조라도 해저드가 끼어들면 "매 클럭 1개 완료"라는 약속이 무너진다.  |
+----------------------------------------------------------------------------+
```

이 그림이 보여주는 핵심은 파이프라인 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 적이 "단 수 부족"만이 아니라는 점이다. 설계자가 해저드를 제어하지 못하면, 더 깊은 파이프라인은 더 많은 빈칸과 더 큰 재시작 비용만 남길 수 있다.

- **📢 섹션 요약 비유**: 여러 차선으로 넓힌 고속도로라도 사고, 합류, 갈림길 혼선이 많으면 차가 시원하게 달리지 못하듯, 파이프라인도 해저드를 다스리지 못하면 넓혀 놓은 길의 가치가 줄어든다.

---

## Ⅱ. 아키텍처 및 핵심 원리

파이프라인 해저드는 발생 원인에 따라 [구조적 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/) ([Structural Hazard](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/)), [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) ([Data Hazard](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)), [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/) ([Control Hazard](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/))로 나뉜다. 셋의 공통점은 모두 "다음 단계로 그냥 넘기면 틀리거나 위험하다"는 점이지만, 원인은 각각 하드웨어 부족, 논리적 선후 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 실행 경로 미확정으로 다르다. 그래서 감지 위치와 해결 회로도 달라진다.

| 해저드 유형 | 발생 이유 | 전형적 예시 | 대표 대응 |
| :--- | :--- | :--- | :--- |
| [구조적 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/) | 같은 자원을 같은 클럭에 동시에 요구 | IF ([Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Fetch)와 MEM (Memory Access)이 단일 메모리를 동시에 요청 | 자원 분리, 다중 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 자원 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) | 앞 결과가 아직 준비되지 않음 | `ADD R1,...` 직후 `SUB ...,R1,...` | 포워딩, 인터락(Interlock), 스톨 |
| [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/) | 다음 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))가 아직 확정되지 않음 | 조건 분기 직후 잘못된 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출 | [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/), [지연 분기](/studynote/01_computer_architecture/05_control_unit_pipelining/230_delayed_branch/), 플러시 |

해저드가 감지되면 제어 유닛은 보통 세 가지 동작 중 하나를 택한다. 첫째, [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 잠시 멈추는 스톨이다. 둘째, 비어 있는 사이클을 흘려보내는 버블 삽입이다. 셋째, 이미 잘못 들어온 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들을 버리는 플러시다. 현대 CPU는 여기에 더해 결과를 우회 전달하거나, 미래 경로를 예측하거나, 아예 독립적인 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 먼저 실행해 피해를 줄인다.

아래 시공간 도표는 세 해저드가 파이프라인에 어떤 모양의 손실을 남기는지 한눈에 보여준다.

```text
+----------------------------------------------------------------------------+
|                 해저드 유형별 파이프라인 손실 패턴 요약                    |
+--------------+-------------------------------------------------------------+
| 구조적       | C4에서 I1(MEM)과 I4(IF)가 같은 메모리 포트를 동시에 요구   |
| 해저드       | -> I4는 대기 -> 앞단 정지                                     |
+--------------+-------------------------------------------------------------+
| 데이터       | I2가 EX에서 R1이 필요하지만 I1의 결과는 아직 WB 전          |
| 해저드       | -> I2에 Bubble 1칸 삽입 또는 Forwarding 수행                 |
+--------------+-------------------------------------------------------------+
| 제어         | Branch 결과가 EX에서야 확정되는데 IF는 이미 다음 명령 인출  |
| 해저드       | -> 예측 성공 시 계속 진행, 실패 시 잘못 인출한 명령 Flush    |
+--------------+-------------------------------------------------------------+
```

중요한 점은 해저드가 모두 같은 비용을 내지 않는다는 것이다. 단일 메모리 충돌은 자원 추가로 비교적 직관적으로 줄일 수 있지만, 분기 실패는 깊은 파이프라인일수록 여러 단계가 한꺼번에 무효화되어 손실이 커진다. 따라서 해저드 제어는 단순한 오류 방지가 아니라, [파이프라인 깊이](/studynote/01_computer_architecture/05_control_unit_pipelining/220_pipeline_depth/)·클럭·전력·복잡도의 균형 설계 문제다.

- **📢 섹션 요약 비유**: 공장 라인이 멈추는 이유가 "망치가 하나뿐인 문제", "앞 공정 결과물이 아직 안 나온 문제", "다음 주문서 방향이 아직 안 정해진 문제"로 다르다면, 해결책도 도구 추가·급행 전달·예측 운영처럼 달라져야 한다.

---

## Ⅲ. 비교 및 연결

파이프라인 해저드를 제대로 이해하려면 세 유형을 단순 나열하지 말고 "무엇이 부족해서 막히는가"라는 축으로 비교해야 한다. [구조적 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/)는 자원 수가 부족한 문제이고, [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)는 시간상 너무 이른 접근의 문제이며, [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)는 미래 경로를 아직 모르는 문제다. 즉 각각 공간 충돌, 시간 충돌, 경로 충돌이라고 볼 수 있다.

| 비교 축 | [구조적 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/) | [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) | [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/) |
| :--- | :--- | :--- | :--- |
| 충돌 대상 | 물리 자원 | [피연산자](/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 값 | 다음 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 주소 |
| 대표 손실 | 자원 대기 | 결과 대기 | 잘못 인출 후 폐기 |
| 대표 완화법 | 하버드 구조, [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 확장 | 포워딩, 스케줄링 | [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/), [BTB](/studynote/01_computer_architecture/05_control_unit_pipelining/234_btb/) (Branch Target Buffer) |
| 깊은 파이프라인 영향 | 충돌 지점 증가 가능 | 우회 경로 복잡도 증가 | 패널티 급증 |

[데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) 내부에서도 더 세부적인 연결이 있다. [RAW](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) ([Read After Write](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/))는 순차 파이프라인에서 가장 현실적인 진성 의존성이고, [WAR](/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/) ([Write After Read](/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/))와 [WAW](/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/) ([Write After Write](/studynote/01_computer_architecture/05_control_unit_pipelining/227_waw/))는 [비순차 실행](/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution)과 [레지스터 리네이밍](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ([Register Renaming](/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/))을 배워야 본격적으로 중요해진다. [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)는 다시 [지연 분기](/studynote/01_computer_architecture/05_control_unit_pipelining/230_delayed_branch/), 정적 예측, 동적 예측으로 이어지고, [구조적 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/)는 [하버드 아키텍처](/studynote/01_computer_architecture/03_architecture_basics_performance/126_harvard_architecture/) ([Harvard Architecture](/studynote/01_computer_architecture/03_architecture_basics_performance/126_harvard_architecture/)), 다중 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 슈퍼스칼라 ([Superscalar](/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/)) 자원 배치와 연결된다.

결국 파이프라인 해저드는 뒤의 세부 주제들을 묶는 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 개념이다. 222번 [구조적 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/), 223번 [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/), 224번 [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)가 각론이라면, 이 문서는 "왜 파이프라인이 생각만큼 깔끔하게 흐르지 않는가"를 총괄하는 상위 프레임으로 읽어야 한다.

- **📢 섹션 요약 비유**: 길이 막히는 이유가 주차 공간 부족, 앞차 사고, 목적지 표지판 오류로 다르면 교통 대책도 주차장 증설·우회로 확보·내비게이션 개선으로 갈라지듯, 해저드도 병목의 원인별로 다뤄야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 파이프라인 해저드는 "무조건 없애기"보다 "어디까지 하드웨어로 줄이고 어디부터 소프트웨어와 타협할 것인가"의 문제로 등장한다. 예를 들어 저전력 마이크로컨트롤러는 면적과 소비전력이 중요하므로 일부 구조적 충돌이나 간단한 스톨을 감수할 수 있다. 반면 서버용 고성능 CPU는 분기 실패 몇 클럭의 손실도 누적 비용이 크기 때문에 예측기, 우회 회로, 발행 폭 제어에 더 큰 투자를 한다.

### 설계 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong>자원 병목 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 캐시와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시가 분리되어 있는가, [레지스터 파일 포트](/studynote/01_computer_architecture/15_advanced_topics/509_register_file_ports/) 수가 발행 폭을 감당하는가.
2. <strong>포워딩 한계 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 산술 결과는 우회 가능하지만, Load-Use처럼 메모리 응답이 늦는 경우는 몇 클럭 스톨이 남는가.
3. **분기 패널티 측정**: [파이프라인 깊이](/studynote/01_computer_architecture/05_control_unit_pipelining/220_pipeline_depth/)와 예측 적중률을 곱해 실제 손실 CPI를 추정했는가.
4. **컴파일러 협업 여부**: [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 스케줄링, [루프 언롤링](/studynote/01_computer_architecture/15_advanced_topics/538_loop_unrolling/), 분기 패턴 개선으로 하드웨어 부담을 줄일 수 있는가.
5. **PPA 균형**: [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)만이 아니라 PPA ([Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/), [Performance](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), Area) 전체에서 해저드 완화 비용이 정당한가.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 깊은 파이프라인을 설계해 놓고 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)기를 빈약하게 두는 것
- 포워딩 경로를 과도하게 늘려 오히려 임계 경로(Critical Path)를 길게 만드는 것
- 실제 워크로드의 분기 밀도와 메모리 접근 특성을 무시한 채 이상적 [CPI](/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/)=1만 바라보는 것

기술사 답안에서는 "해저드는 파이프라인 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하의 직접 원인이며, 원인별로 구조적/[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/제어로 분류하고 대응책도 자원 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)/포워딩/예측으로 분리해 설명한다"는 틀을 잡아 주면 좋다. 그 위에 PPA와 실제 [CPI](/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/) 판단을 붙이면 단순 정의를 넘어 설계 의사결정 답안이 된다.

- **📢 섹션 요약 비유**: 비싼 스포츠카를 만들 때는 엔진만 키우는 것이 아니라 브레이크, 서스펜션, 타이어를 함께 맞추듯, 빠른 파이프라인도 해저드 완화 장치를 같이 설계해야 진짜 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 난다.

---

## Ⅴ. 기대효과 및 결론

파이프라인 해저드를 정확히 다루면 같은 클럭과 같은 실행 유닛으로도 훨씬 높은 체감 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 얻을 수 있다. 스톨이 줄어들고, 잘못 인출한 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 버리는 횟수가 감소하며, 파이프라인이 더 안정적으로 채워지기 때문이다. 결국 해저드 관리의 목표는 "파이프라인을 더 복잡하게 만드는 것"이 아니라 "복잡해진 파이프라인이 실제로 일하게 만드는 것"이다.

다만 해저드 완화는 공짜가 아니다. 자원 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 면적과 전력을 늘리고, 포워딩은 배선과 제어를 복잡하게 만들며, 고도 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)은 큰 테이블과 학습 로직을 요구한다. 그래서 현대 프로세서는 해저드를 완전히 제거하기보다, 자주 발생하는 손실을 가장 경제적으로 줄이는 방향으로 진화한다.

앞으로의 확장 방향은 세 가지로 요약할 수 있다. 첫째, 더 정교한 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)과 프론트엔드 최적화다. 둘째, [비순차 실행](/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)과 리네이밍을 통한 [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/) 숨기기다. 셋째, 워크로드 특성에 따라 자원 사용을 조절하는 적응형 마이크로아키텍처다. 따라서 파이프라인 해저드는 "파이프라인의 예외 사항"이 아니라, 현대 CPU가 왜 이렇게 복잡해졌는지를 설명하는 중심 개념으로 기억해야 한다.

- **📢 섹션 요약 비유**: 좋은 공장장은 라인을 길게 만든 뒤 끝내는 것이 아니라, 어디서 자꾸 막히는지 보고 도구를 더 놓고, 순서를 바꾸고, 길을 미리 예측해 공장이 쉬지 않게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [파이프라인 스톨](/studynote/01_computer_architecture/05_control_unit_pipelining/229_pipeline_stall/) ([Pipeline Stall](/studynote/01_computer_architecture/05_control_unit_pipelining/229_pipeline_stall/)) | 해저드를 즉시 해결하지 못할 때 파이프라인을 멈추는 기본 대응 |
| 버블 (Bubble) | 유효한 작업 없이 한 사이클을 흘려보내는 빈 슬롯 |
| [데이터 포워딩](/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) ([Data Forwarding](/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/)) | [데이터 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/223_data_hazard/)의 대표적 하드웨어 우회 기법 |
| [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) ([Branch Prediction](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)) | [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)의 손실을 줄이는 핵심 프론트엔드 기술 |
| [BTB](/studynote/01_computer_architecture/05_control_unit_pipelining/234_btb/) (Branch Target Buffer) | 분기 목표 주소를 빠르게 제공해 [제어 해저드](/studynote/01_computer_architecture/05_control_unit_pipelining/224_control_hazard/)를 줄이는 캐시성 구조 |
| [비순차 실행](/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution) | 해저드로 막힌 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 기다리는 동안 다른 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 먼저 처리하는 확장 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
순차 실행 (Sequential Execution)
        |
        v
명령어 파이프라이닝 (Instruction Pipelining)
        |
        v
파이프라인 해저드 (Pipeline Hazards)
        |
        +--> 구조적 해저드 (Structural Hazard)
        |      +--> 자원 분리 · 포트 확장 · 하버드 구조
        |
        +--> 데이터 해저드 (Data Hazard)
        |      +--> 포워딩 · 인터락 · 스케줄링 · 리네이밍
        |
        +--> 제어 해저드 (Control Hazard)
               +--> 지연 분기 · 분기 예측 · BTB (Branch Target Buffer)
                   · BHT (Branch History Table)
                        |
                        v
슈퍼스칼라 · 비순차 실행 · 현대 마이크로아키텍처
```

이 흐름도는 "겹쳐 실행하기 시작함 -> 충돌이 드러남 -> 충돌별 전용 기법이 생김 -> 더 공격적인 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 구조로 확장됨"이라는 발전 축을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 공장에서 여러 친구가 한 줄로 서서 일을 빨리 하려면, 서로 같은 공구를 동시에 잡거나 앞 친구 결과를 너무 빨리 찾으면 안 돼요.
2. 또 갈림길에서 어느 길로 갈지 모르는데 그냥 뛰어가면, 나중에 잘못 간 친구들을 다시 불러와야 해요.
3. 그래서 컴퓨터는 공구를 더 놓아 두고, 필요한 것은 미리 건네주고, 길도 미리 짐작해서 공장이 멈추지 않게 만든답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 221 / 803

<- **이전**: [220. 파이프라인 깊이 (Pipeline Depth)](/studynote/01_computer_architecture/05_control_unit_pipelining/220_pipeline_depth/)
**다음**: [222. 구조적 해저드 (Structural Hazard)](/studynote/01_computer_architecture/05_control_unit_pipelining/222_structural_hazard/) ->

---
