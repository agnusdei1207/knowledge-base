+++
title = "232. 정적 분기 예측 (Static Prediction)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) (Static Prediction)은 실행 중 이력 없이, 분기 명령의 형태·방향·컴파일러 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)만으로 다음 경로를 미리 정하는 고정 규칙 기반 예측이다.
> 2. **가치**: 분기 이력 테이블이나 복잡한 학습 회로 없이도 파이프라인의 빈 버블을 줄일 수 있어, 단순한 프로세서와 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 예측 단계에서 면적·전력 대비 효율이 높다.
> 3. **판단 포인트**: 루프처럼 반복성이 강한 코드는 BTFN (Backward Taken, [Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Not Taken) 규칙이 잘 맞지만, 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 따라 분기 방향이 자주 바뀌는 코드에서는 동적 예측기보다 한계가 분명하다.

---

## Ⅰ. 개요 및 필요성

정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) (Static Prediction)은 CPU (Central Processing Unit)가 분기 결과가 아직 확정되지 않았는데도, 미리 "이쪽으로 갈 가능성이 높다"고 가정하고 다음 명령어를 가져오는 방식이다. 분기 명령은 파이프라인에서 특히 치명적인데, 조건 비교가 끝나기 전까지 다음 [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))를 확정할 수 없기 때문이다. 예측이 없으면 분기를 만날 때마다 인출 단계가 멈추고, 단계 수가 깊어질수록 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 손실이 커진다. 정적 예측은 이 문제를 가장 낮은 비용으로 완화하려고 등장했다.

이 방식이 필요한 배경은 명확하다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [RISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/195_risc/) (Reduced [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Set Computer) 프로세서나 MCU ([Microcontroller](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) Unit) 같은 단순 코어는 동적 예측에 필요한 [BHT](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/235_bht/) (Branch History Table)나 패턴 테이블을 넣기 어렵다. 또한 고성능 코어도 전원이 켜진 직후나 문맥 전환 직후에는 학습된 이력이 없으므로, 첫 판단은 결국 간단한 기본 규칙에 기대야 한다. 즉 정적 예측은 "항상 이것만 쓰는 기술"이라기보다, 가장 단순한 프로세서의 주력 전략이자 복잡한 예측기의 기초 안전망이다.

- **📢 섹션 요약 비유**: 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)은 길 안내 앱이 꺼졌을 때 "출근 시간엔 큰길이 보통 덜 막힌다"는 상식만으로 먼저 방향을 잡는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

정적 예측의 핵심은 <strong>분기 결과를 기다리기 전에, 고정 규칙으로 다음 인출 주소를 선택하는 것</strong>이다. 구현은 단순하지만, 규칙을 어디에 두느냐에 따라 하드웨어 중심 방식과 컴파일러 중심 방식으로 나뉜다. 하드웨어 중심 방식은 분기 방향이나 [opcode](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/) 형태를 보고 즉시 판단하고, 컴파일러 중심 방식은 "이 분기는 대체로 참" 같은 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)를 코드 배치나 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 비트로 남긴다. 둘 다 공통적으로 실행 이력을 저장하지 않기 때문에 면적과 소비전력이 작다.

| 방식 | 판단 근거 | 장점 | 한계 |
| :--- | :--- | :--- | :--- |
| Always Not Taken | 항상 순차 실행 가정 | 구현이 가장 단순, 다음 주소가 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)+4라서 인출이 쉬움 | 루프 분기에 매우 약함 |
| Always Taken | 항상 분기 타겟 가정 | 반복문 위주 코드에서 유리 | 타겟 주소를 조기에 계산해야 함 |
| BTFN (Backward Taken, [Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Not Taken) | 뒤로 가는 분기는 Taken, 앞으로 가는 분기는 Not Taken | 루프/예외 처리의 전형적 패턴을 잘 반영 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존 분기에는 오차 큼 |
| 컴파일러 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) | 프로파일 또는 개발자 의도 | 코드 배치 최적화와 결합 가능 | [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)가 틀리면 오히려 손해 |

아래 그림은 정적 예측이 파이프라인 초반에서 어떤 결정을 내리는지 보여준다.

```text
+--------------------------------------------------------------------------+
|          정적 분기 예측의 위치: 분기 확정 전, 먼저 경로를 고른다         |
+--------------------------------------------------------------------------+
| IF (Instruction Fetch)                                                  |
|   |                                                                      |
|   +- 분기 아님 --------------------------------> 순차 주소 인출            |
|   |                                                                      |
|   +- 분기 명령 발견                                                      |
|         |                                                                |
|         +- 규칙 1: Always Not Taken ----------> PC + 4 인출               |
|         +- 규칙 2: Always Taken --------------> Branch Target 인출        |
|         +- 규칙 3: BTFN                                                  |
|                +- 뒤로 점프(루프) ------------> Taken 예측                |
|                +- 앞으로 점프(조건 예외) -----> Not Taken 예측            |
|                                                                          |
| EX (Execute)에서 실제 조건 계산                                          |
|   +- 예측 성공 ------------------------------> 파이프라인 유지            |
|   +- 예측 실패 ------------------------------> 잘못 가져온 명령 Flush     |
+--------------------------------------------------------------------------+
```

이 구조에서 중요한 점은 정적 예측이 <strong>정확도보다 결정 시점</strong>으로 가치를 만든다는 사실이다. 예측 정확도가 100%가 아니더라도, 매번 기다리는 것보다 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 좋아질 수 있다. 특히 BTFN은 반복문이 뒤로 점프하고, 오류 처리나 희귀 조건은 앞으로 빠지는 코드 배치 관례를 이용하므로 추가 저장장치 없이도 비교적 높은 적중률을 낸다. 반대로 분기 패턴이 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 따라 계속 바뀌는 경우에는 고정 규칙이 현실을 따라가지 못한다.

- **📢 섹션 요약 비유**: 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)은 신호등 고장 난 교차로에서 "출근길에는 직진 차가 많다"는 규칙으로 우선 통행 방향을 먼저 정하는 임시 수신호와 같다.

---

## Ⅲ. 비교 및 연결

정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)을 제대로 이해하려면 [동적 분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/233_dynamic_prediction/) (Dynamic [Branch Prediction](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/))과의 경계를 분명히 봐야 한다. 정적 방식은 분기 자체의 모양을 보고 판단하고, 동적 방식은 과거에 실제로 어떻게 움직였는지를 학습한다. 그래서 정적 예측은 비용과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 작고, 동적 예측은 정확도가 높다. 결국 둘의 차이는 "기억 없이 상식으로 판단하느냐"와 "이력을 보고 학습하느냐"의 차이로 요약된다.

| 비교 항목 | 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) | [동적 분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/233_dynamic_prediction/) |
| :--- | :--- | :--- |
| 정보 원천 | 분기 방향, [opcode](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/159_opcode/), 컴파일러 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) | 최근 실행 이력, 패턴 테이블 |
| 하드웨어 비용 | 매우 작음 | 큼 |
| [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상태 | 즉시 사용 가능 | Cold Start에 약함 |
| 평균 정확도 | 보통 | 높음 |
| 대표 활용 | 단순 코어, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 경로, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 부팅 | 고성능 CPU, 깊은 파이프라인 |

정적 예측은 컴파일러 최적화와도 강하게 연결된다. 예를 들어 PGO (Profile-Guided Optimization)는 실제 실행 통계를 바탕으로 자주 가는 경로를 fall-through 경로로 배치해, "Not Taken" 예측이 맞을 가능성을 높인다. 또한 likely/unlikely [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)는 프로그래머의 의도를 기계어 배치에 반영해 정적 예측과 명령 캐시 효율을 함께 개선한다. 따라서 정적 예측은 하드웨어만의 기법이 아니라, <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/">ISA</a> (<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/">Instruction Set Architecture</a>)·컴파일러·코드 배치</strong>가 만나는 경계 기술이다.

- **📢 섹션 요약 비유**: 정적 예측이 여행 책자의 "보통 이 코스로 갑니다"라면, 동적 예측은 실시간 교통앱이 지난 10분의 병목을 보고 우회로를 다시 계산하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "정적 예측이 좋은가"보다 <strong>어떤 조건에서 정적 예측만으로 충분한가</strong>를 판단해야 한다. 파이프라인이 짧고 전력 예산이 작은 임베디드 코어라면, 단순한 BTFN만으로도 면적과 전력 대비 만족스러운 결과를 얻을 수 있다. 반대로 분기 실패 한 번의 비용이 10사이클 이상으로 커지는 깊은 슈퍼스칼라 코어에서는 정적 예측만으로는 손실이 너무 크므로, 동적 예측기의 보조 전략으로 두는 편이 맞다. 즉 채택 기준은 정확도 자체보다 <strong>오예측 비용 대비 하드웨어 투자 가치</strong>에 있다.

### 실무 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 분기 실패 페널티가 작은 단순 파이프라인인가, 아니면 Flush 비용이 큰 깊은 파이프라인인가?
2. 저전력·저면적 제약 때문에 이력 테이블을 줄여야 하는가?
3. 루프, 오류 처리, fast path/slow path처럼 코드 패턴이 분명한가?
4. 컴파일러 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)나 PGO로 경로 배치를 보정할 수 있는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 분기를 likely/unlikely로 과장해 컴파일러의 기본 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)을 오히려 깨뜨리는 경우
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존 분기가 많은 서버 코드에 정적 예측만 믿고 동적 예측 비용을 과소평가하는 경우
- 분기 타겟 주소 계산 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 무시하고 Always Taken이 항상 유리하다고 오해하는 경우

기술사 답안에서는 "정적 예측은 단순해서 낙후된 기술"이라고 쓰면 부족하다. 정확한 평가는 <strong>저비용, 즉시 사용 가능, <a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a> 대응, 컴파일러와의 결합성</strong>을 장점으로 보고, <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 적응성 부족, 깊은 파이프라인에서의 손실 확대</strong>를 한계로 정리하는 것이다.

- **📢 섹션 요약 비유**: 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)은 작은 동네 가게에서 인기 메뉴를 미리 많이 준비해 두는 전략과 같다. 손님 취향이 매일 비슷하면 효율적이지만, 손님 구성이 자주 바뀌는 대형 매장에서는 실시간 판매 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)의 기대효과는 복잡한 장치 없이도 파이프라인 정지 시간을 줄여 <strong>평균 처리량을 안정적으로 끌어올리는 것</strong>이다. 특히 단순 코어에서는 적은 논리만으로 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 개선하고, 고성능 코어에서는 동적 예측기가 준비되기 전의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 판단과 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 경로를 제공한다. 또한 컴파일러 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)와 코드 레이아웃 최적화를 통해 하드웨어 추가 없이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보정할 여지도 있다.

다만 이 방식은 본질적으로 고정 규칙이므로, 입력 분포가 바뀌거나 분기 패턴이 복잡해지면 정확도가 급격히 떨어질 수 있다. 그래서 미래 방향도 정적 예측 단독 진화라기보다, <strong>정적 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/">휴리스틱</a> + 동적 학습 + 컴파일러 <a href="/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/">프로파일링</a></strong>의 결합으로 가고 있다. 결국 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)은 "정답을 늘 맞히는 기술"이 아니라, <strong>가장 적은 비용으로 첫 결정을 내려 주는 기본기</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)은 야구에서 초반 수비 위치를 기본 타구 방향 통계로 먼저 잡는 것과 같다. 완벽하진 않지만, 아무 준비 없이 서 있는 것보다는 훨씬 낫다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 분기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 슬롯 (Branch Delay Slot) | 예측이 약하던 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 파이프라인에서 분기 손실을 줄이기 위해 소프트웨어가 한 사이클을 메우는 방식 |
| BTFN (Backward Taken, [Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Not Taken) | 정적 예측의 대표 규칙으로, 루프와 예외 처리의 코드 구조를 이용한다 |
| [동적 분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/233_dynamic_prediction/) (Dynamic [Branch Prediction](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)) | 정적 예측의 한계를 보완하기 위해 실행 이력을 학습하는 방식 |
| PGO (Profile-Guided Optimization) | 실제 실행 통계를 컴파일 단계에 반영해 정적 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)와 코드 배치를 개선한다 |
| 파이프라인 Flush | 정적 예측 실패 시 잘못 인출한 명령을 비우면서 발생하는 직접 비용 |

### 📈 관련 키워드 및 발전 흐름도

```text
분기 명령으로 인한 파이프라인 정지
    |
    v
정적 분기 예측 (Always Taken / Always Not Taken)
    |
    v
BTFN (Backward Taken, Forward Not Taken)
    |
    v
컴파일러 힌트 · PGO (Profile-Guided Optimization)
    |
    v
동적 분기 예측 · 하이브리드 분기 예측
```

이 흐름은 "기다림 회피 -> 규칙 정교화 -> 소프트웨어 협력 -> 학습형 예측"으로 분기 처리 기술이 발전해 온 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 갈림길이 나오기 전에 "보통은 이쪽으로 가더라" 하고 먼저 길을 정하는 게 정적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)이에요.
2. 지난번에 어디로 갔는지는 기억하지 않아도, 길 모양만 보고 빨리 움직일 수 있어요.
3. 자주 가던 길에서는 잘 맞지만, 매번 길이 달라지면 틀릴 수도 있어서 더 똑똑한 지도와 함께 쓰면 좋아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 232 / 803

<- **이전**: [231. 분기 예측 (Branch Prediction)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)
**다음**: [233. 동적 분기 예측 (Dynamic Prediction)](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/233_dynamic_prediction/) ->

---
