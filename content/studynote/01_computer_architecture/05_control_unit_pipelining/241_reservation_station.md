+++
title = "241. 예약역 (Reservation Station)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 예약역 (Reservation [Station](/knowledge-base/studynote/03_network/04_data_link_layer_error/218_hdlc_station_primary_secondary/), RS)은 해독된 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 실행 유닛 바로 앞에 붙잡아 두고, [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)가 모두 준비된 순간에만 내보내는 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>형 대기·선택 장치</strong>다.
> 2. **가치**: RS가 있으면 앞선 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 묶여도, 뒤의 독립 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 먼저 실행해 <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a> 수준 병렬성 (Instruction-Level Parallelism, ILP)</strong>을 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 바꿀 수 있다.
> 3. **판단 포인트**: RS는 클수록 병렬성이 늘 수 있지만, 웨이크업·선택 회로와 공통 [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) (Common [Data Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/), CDB) 비교 부하가 커지므로 <strong>엔트리 수·배치 방식·<a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">버스</a> 폭</strong>을 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

예약역 (Reservation [Station](/knowledge-base/studynote/03_network/04_data_link_layer_error/218_hdlc_station_primary_secondary/), RS)은 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution, OoO) 프로세서에서 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 실행 유닛 앞에 잠시 저장해 두고, 필요한 입력값이 모두 준비된 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)부터 발행하는 하드웨어 구조다. 순차 파이프라인에서는 앞 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되면 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)도 함께 멈추기 쉬웠다. 특히 메모리 접근, [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 곱셈, 분기 해소처럼 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 편차가 큰 연산이 섞이면 중앙처리장치 (Central Processing Unit, CPU)는 연산기가 남아 있어도 놀게 된다.

RS가 필요한 이유는 <strong>프로그램 순서와 실행 가능 순서를 분리</strong>하기 위해서다. 프로그램은 순서대로 해독되더라도, 실제 실행은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 준비된 순서대로 진행하는 편이 효율적이다. 즉 RS는 "먼저 들어온 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)"보다 "지금 당장 실행 가능한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)"를 우선시하여 읽기 후 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) ([Read After Write](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/), [RAW](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) 의존성만 남기고 불필요한 대기를 줄인다.

이 개념은 단순 버퍼와 다르다. 일반 큐는 순서만 저장하지만, RS는 각 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 어떤 값은 이미 갖고 있고 어떤 값은 아직 기다리는지까지 기록한다. 그래서 RS는 저장소이면서 동시에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스케줄러다.

- **📢 섹션 요약 비유**: RS는 병원 대기실이 아니라 수술실 앞 준비실에 가깝다. 접수 순서대로 줄 세우는 것이 아니라, 검사와 마취가 끝난 환자부터 바로 수술실로 보내 수술대를 놀리지 않게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RS 엔트리는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 하나를 위해 작은 상태표를 유지한다. 핵심은 "값이 이미 있는가"와 "없다면 누가 나중에 줄 것인가"를 동시에 적어 두는 것이다. 보통 연산 종류, 준비된 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 값, 아직 오지 않은 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)의 태그, 점유 여부, 목적 실행 유닛 정보가 들어간다.

| 필드 | 의미 | 설계상 중요성 |
| :--- | :--- | :--- |
| Op | 수행할 연산 종류 | 어떤 실행 유닛으로 보낼지 결정 |
| Vj, Vk | 이미 준비된 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 값 | 즉시 실행 가능 여부 판단의 근거 |
| Qj, Qk | 아직 오지 않은 값의 생산자 태그 | CDB 방송을 들었을 때 어떤 결과를 받아야 하는지 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) |
| Busy | 엔트리 사용 여부 | 새 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수용 가능 여부 결정 |
| Dest/Tag | 결과를 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 태그 | 뒤 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)와 [재주문 버퍼](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) ([Reorder Buffer](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB) 연결 |

아래 그림은 RS가 <strong>발행 → 대기 → 웨이크업 → 선택 → 실행</strong>으로 이어지는 흐름을 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Reservation Station의 피연산자 대기 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Decode/Rename</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">RS0</div><div class="kb-diagram-note">Qj=Load3 Vk=8 Busy=1</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">RS1</div><div class="kb-diagram-note">Vj=5 Vk=2 Busy=1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CDB Broadcast</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ "Tag=Load3, Value=12"</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">RS0</div><div class="kb-diagram-note">Vj=12, Qj=empty</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Ready Check</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─</div><div class="kb-diagram-node">RS0</div><div class="kb-diagram-note">Vj,Vk 준비 완료 ─</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─</div><div class="kb-diagram-node">RS1</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">Select Logic ─▶ Execute Unit</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 오래 기다린 엔트리/우선순위 기준 선택</div></div>
</div>
</div>



이 구조의 핵심 연산은 두 가지다. 첫째, **웨이크업 (Wakeup)** 단계에서 CDB를 감시하던 엔트리가 자기 태그와 일치하는 결과를 받으면 Q 필드를 비우고 V 필드에 실제 값을 채운다. 둘째, <strong>선택 (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/">Select</a>)</strong> 단계에서 준비 완료된 엔트리들 중 실행 유닛에 보낼 대상을 고른다. 따라서 RS [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 단순 저장량보다 "얼마나 빠르게 깨우고, 그중 누굴 먼저 내보내는가"에 달려 있다.

또한 RS는 [데이터 포워딩](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/) ([Data Forwarding](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/228_data_forwarding/))과 직접 연결된다. 결과가 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 파일까지 기록되기를 기다리지 않고, 완료된 순간 바로 대기 엔트리에 흘려보내기 때문이다. 이 덕분에 실제 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 간 거리보다 훨씬 짧아질 수 있다.

- **📢 섹션 요약 비유**: RS는 택배 분류대와 같다. 상자가 아직 안 온 주문은 송장 번호만 들고 기다리다가, 택배차가 도착하면 자기 번호 상자를 바로 집어 들고 출고 라인으로 이동한다.

---

## Ⅲ. 비교 및 연결

RS를 제대로 이해하려면 [재주문 버퍼](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) ([Reorder Buffer](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB)와 구분해야 한다. RS는 <strong>언제 실행할지</strong>를 결정하고, ROB는 <strong>언제 공식 상태로 확정할지</strong>를 결정한다. 둘 다 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)에서 쓰이지만, 역할이 다르므로 서로 대체할 수 없다.

| 비교 항목 | 예약역 (RS) | [재주문 버퍼](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) (ROB) |
| :-------- | :---------- | :---------------- |
| 핵심 목적 | 실행 준비 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 대기 및 발행 | 완료 결과를 프로그램 순서대로 커밋 |
| 관심 정보 | [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 준비 여부, 실행 유닛 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 나이, 예외, 분기 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 동작 시점 | 실행 직전 | 실행 후 커밋 직전 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기여 | 유닛 활용률 향상, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 숨김 | 정밀한 예외, 순차적 상태 보장 |

또한 RS는 스코어보드 (Scoreboard)보다 더 세밀한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 제어를 제공한다. 스코어보드는 중앙에서 자원 충돌을 관리하는 색채가 강하지만, RS는 각 엔트리가 태그를 들고 직접 결과 방송을 기다린다. 이 차이 때문에 현대 고성능 코어는 중앙 집중식 단일보드보다 RS 또는 RS와 유사한 이슈 큐를 선호한다.

토마술로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Tomasulo's [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))과의 연결도 중요하다. 토마술로는 RS와 CDB를 결합해 "태그 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"을 체계화한 대표 사례다. 즉 토마술로가 설계 철학이라면, RS는 그 철학을 실제 회로로 구현한 대기실이라고 볼 수 있다.

다만 오늘날 모든 프로세서가 고전적 의미의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) RS만 쓰는 것은 아니다. 일부 설계는 통합 이슈 큐를 두고 내부적으로 RS와 비슷한 준비 비트와 태그 비교를 수행한다. 시험 답안에서는 "RS = 실행 직전 대기·발행 구조"라는 본질을 잡고, 구현이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)형인지 중앙형인지까지 한 단계 더 설명하면 좋다.

- **📢 섹션 요약 비유**: RS가 공항 게이트 앞 탑승 대기줄이라면, ROB는 도착 공항의 입국 심사 줄이다. 비행기를 언제 태울지와 나라에 언제 공식 입국시킬지는 서로 다른 문제다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 설계에서 RS는 "넣을 수 있는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수"보다 "제한된 클럭 안에 비교와 선택을 끝낼 수 있는가"가 더 중요하다. 엔트리가 많아질수록 더 많은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 숨길 수 있지만, 동시에 매 사이클 태그 [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) 수와 선택 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 복잡도가 증가한다. 그 결과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 발열, 전력 소모가 급격히 커진다.

### 설계 판단 포인트

1. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>형 vs 통합형</strong>: 정수 산술논리연산장치 ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/), [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)), [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 유닛, 로드/스토어 유닛 앞에 각각 작은 RS를 두면 선택 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 줄지만, 어떤 큐는 비고 어떤 큐는 포화되는 불균형이 생길 수 있다.
2. <strong>CDB <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong>: 여러 실행 유닛이 동시에 결과를 내도 방송 통로가 부족하면 깨워야 할 엔트리가 늦게 깨어난다. RS 크기 확대만으로는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 안 오르고, 결과 배포 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 함께 따라와야 한다.
3. <strong>엔트리 크기와 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 종류</strong>: 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 긴 서버 코어는 더 넓은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 윈도우가 유리하지만, 전력 제약이 큰 모바일 코어는 작은 RS와 공격적 전원 관리가 더 현실적일 수 있다.
4. <strong>선택 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>: 가장 오래 기다린 엔트리를 우선할지, 특정 유닛을 우선 채울지에 따라 공정성과 처리량이 달라진다.

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **무작정 큰 RS**: 병렬성보다 웨이크업 회로 부담이 먼저 커져 오히려 주파수와 전성비가 나빠질 수 있다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">버스</a> 폭 미고려</strong>: 결과 방송 병목을 해결하지 않으면 준비 완료 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 있어도 발행 효율이 낮다.
- **유닛별 불균형 방치**: 곱셈기 앞 RS는 가득 차고 가산기 앞 RS는 비는 구조가 계속되면 이론상 엔트리 수가 커도 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 제한된다.

기술사 관점에서는 "RS는 OoO [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 장치"라고만 쓰면 부족하다. <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 숨김 효과, 웨이크업·선택 복잡도, CDB 병목, ROB와의 역할 분담</strong>까지 함께 써야 답안의 깊이가 생긴다. 채택 판단은 결국 워크로드의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 특성과 허용 가능한 전력·면적 예산의 균형 문제다.

- **📢 섹션 요약 비유**: 주방 앞 대기대를 넓히는 것만으로 식당이 빨라지지는 않는다. 완성된 요리를 알려 주는 호출 시스템과, 어떤 주문을 먼저 조리대에 올릴지 고르는 주방장의 판단이 함께 좋아야 진짜 회전율이 오른다.

---

## Ⅴ. 기대효과 및 결론

RS의 가장 큰 효과는 실행 유닛을 가능한 한 쉬지 않게 만든다는 점이다. 앞선 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 하나가 오래 걸려도 뒤의 독립 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 먼저 실행시켜 전체 처리량을 높이고, 긴 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 어느 정도 흡수할 수 있다. 그래서 RS는 슈퍼스칼라와 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)의 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 만들어 내는 핵심 중간층이다.

하지만 RS는 공짜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 아니다. 엔트리가 커질수록 태그 비교 회로, 결과 방송 배선, 선택 로직이 함께 무거워지고, 결국 클럭 주파수와 전력 효율을 압박한다. 따라서 현대 설계는 "가능한 많은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 넣는다"보다 "필요한 범위까지만 넓히고, 남는 병목은 예측·캐시·프리페치로 보완한다"는 방향으로 균형을 잡는다.

결국 예약역은 <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>를 저장하는 구조가 아니라 실행 가능성을 실시간으로 판단하는 구조</strong>로 기억해야 한다. 순서대로 들어온 일을 그대로 처리하는 파이프라인에서, 준비된 일부터 움직이는 지능형 파이프라인으로 넘어가게 만든 전환점이 바로 RS다.

- **📢 섹션 요약 비유**: RS는 단순 창고가 아니라 현장 반장이다. 자재가 다 모인 작업부터 바로 작업자에게 배정해 공사장을 멈추지 않게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution, OoO) | RS가 준비된 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)부터 먼저 실행하게 하므로 실제로 구현된다. |
| [레지스터 리네이밍](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/) ([Register Renaming](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/239_register_renaming/)) | 거짓 의존성을 줄여 RS가 다룰 수 있는 실행 후보를 넓힌다. |
| 공통 [데이터 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/) (Common [Data Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/345_data_bus/), CDB) | 완료 결과를 방송해 대기 중인 RS 엔트리를 깨운다. |
| [재주문 버퍼](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/) ([Reorder Buffer](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/), ROB) | RS에서 실행된 결과를 프로그램 순서대로 커밋하게 만든다. |
| 스코어보드 (Scoreboard) | 중앙식 자원 관리와 RS 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스케줄링을 비교할 때 기준이 된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">순차 파이프라인</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터 해저드 (Data Hazard) 인식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">레지스터 리네이밍 (Register Renaming)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">예약역 (Reservation Station)</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 토마술로 알고리즘 (Tomasulo's Algorithm)</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 공통 데이터 버스 (Common Data Bus, CDB)</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 재주문 버퍼 (Reorder Buffer, ROB) 결합</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">대규모 비순차 실행 코어</div>
</div>
</div>



이 흐름은 "해저드 회피 → 의존성 완화 → 실행 직전 대기·선택 → 순서 복원 결합"으로 현대 파이프라인이 진화한 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예약역은 숙제를 바로 못 하는 친구들을 잠깐 앉혀 두는 똑똑한 대기실이에요.
2. 연필과 공책이 먼저 준비된 친구부터 선생님이 불러서 먼저 숙제를 하게 해요.
3. 그래서 어떤 친구가 늦어도 교실 전체는 멈추지 않고 계속 움직일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 241 / 803

← **이전**: [240. 재주문 버퍼 (ROB, Reorder Buffer)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/240_reorder_buffer/)
**다음**: [242. 토마술로 알고리즘 (Tomasulo's Algorithm)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/242_tomasulo_algorithm/) →

---
